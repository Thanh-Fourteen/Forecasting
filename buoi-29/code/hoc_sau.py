"""Buổi 29 — Nền deep learning cho chuỗi thời gian.

Tải điện 50 khách hàng Bồ Đào Nha, theo giờ. Tự viết bằng PyTorch: cắt cửa sổ, chuẩn hoá, MLP / LSTM / TCN, vòng huấn luyện
có dừng sớm; so với seasonal naive, MSTL và LightGBM trên cùng các mốc test.

Chỉ định nghĩa hàm và hằng số; phần chạy nằm trong code/lab.ipynb (bộ chấm nạp module này).
"""
from __future__ import annotations

import time
from contextlib import contextmanager

import numpy as np
import pandas as pd
import torch
from torch import nn

from tv import du_lieu

L = 168                          # input_size: 7 ngày × 24 giờ nhìn lại
H = 24                           # horizon: đoán 24 giờ tới
MOC_VAL = pd.Timestamp("2014-05-01")    # từ mốc này: val (dùng để dừng sớm)
MOC_TEST = pd.Timestamp("2014-07-01")   # từ mốc này: test (chỉ để chấm)
SO_MOC_TEST = 26                 # 26 mốc, mỗi thứ Hai 00:00 một mốc, đoán 24 giờ sau mốc
SO_KHACH = 50
BUOC_TRAIN = 2                   # stride: cửa sổ train cách nhau 2 giờ — nửa bộ nhớ, gần như không mất thông tin
NGUONG_DOI_MUC = 1.3             # "đổi mức": trung bình nửa cuối 2014 lệch > 30% so với đoạn trước đó
torch.set_num_threads(4)


# ---------------------------------------------------------------------------- dữ liệu

def doc_dien(so_khach: int = SO_KHACH, seed: int = 0) -> pd.DataFrame:
    """unique_id, ds, y (kW) — mọi khách hàng đổi mức + khách hàng ngẫu nhiên cho đủ `so_khach`."""
    df = du_lieu.doc_du_lieu("monash-electricity-hourly")
    df["ds"] = df["ds"].dt.floor("h")            # tệp Monash ghi giờ bắt đầu 00-00-01 (thừa 1 giây)
    rong = df.pivot(index="ds", columns="unique_id", values="y")
    con_dung = rong[rong.index < MOC_VAL].iloc[-24 * 28:].sum() > 0     # bỏ khách hàng đã ngừng dùng điện (T183 từ 09/2012)
    rong = rong.loc[:, con_dung]
    ti_le = rong[rong.index >= MOC_TEST].mean() / rong[rong.index < MOC_TEST].mean()
    doi_muc = sorted(ti_le[np.abs(np.log(ti_le)) > np.log(NGUONG_DOI_MUC)].index)
    con_lai = sorted(set(rong.columns) - set(doi_muc))
    them = np.random.default_rng(seed).choice(con_lai, so_khach - len(doi_muc), replace=False)
    chon = sorted([*doi_muc, *them], key=lambda s: int(s[1:]))
    ra = df[df["unique_id"].isin(chon)].reset_index(drop=True)
    ra.attrs["doi_muc"] = doi_muc
    return ra


def chon_it(df: pd.DataFrame, so_khach: int = 5, tu: str = "2013-11-01") -> pd.DataFrame:
    """Tập nhỏ để thấy rò rỉ chồng lấn: 5 khách hàng đầu, dữ liệu từ 1/11/2013 (6 tháng trước MOC_VAL)."""
    ids = sorted(df["unique_id"].unique(), key=lambda s: int(s[1:]))[:so_khach]
    return df[df["unique_id"].isin(ids) & (df["ds"] >= pd.Timestamp(tu))].reset_index(drop=True)


def cac_moc_test(df: pd.DataFrame) -> list[pd.Timestamp]:
    dau = MOC_TEST + pd.Timedelta(days=(7 - MOC_TEST.weekday()) % 7)
    return [dau + pd.Timedelta(weeks=i) for i in range(SO_MOC_TEST)]


# ---------------------------------------------------------------------------- cửa sổ

def cat_cua_so(y: np.ndarray, L: int = L, H: int = H, buoc: int = 1) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cắt một chuỗi thành cặp (đầu vào L điểm, mục tiêu H điểm kế tiếp). Trả X (n, L), Y (n, H), vị trí điểm mục tiêu đầu."""
    dau = np.arange(L, len(y) - H + 1, buoc)
    w = np.lib.stride_tricks.sliding_window_view(y, L + H)[dau - L]   # dòng j = y[dau_j − L : dau_j + H]
    return w[:, :L], w[:, L:], dau


def tao_tap(df: pd.DataFrame, scaler: dict, tu: pd.Timestamp | None, den: pd.Timestamp, buoc: int = 1) -> dict:
    """Mẫu (X, Y) của mọi chuỗi có TOÀN BỘ mục tiêu nằm trong [tu, den). Đầu vào được lấn về trước `tu` (đó là quá khứ, hợp lệ).

    Chia theo thời gian TRƯỚC, rồi mới cắt: mục tiêu của train và val không bao giờ trùng giờ nào.
    """
    X, Y, ma, ds_muc_tieu = [], [], [], []
    for i, (uid, g) in enumerate(df.groupby("unique_id", sort=True)):
        ds = g["ds"].to_numpy()
        y = chuan_hoa(g["y"].to_numpy(), scaler[uid]).astype(np.float32)
        x_, y_, dau = cat_cua_so(y, buoc=buoc)
        dau_mt, cuoi_mt = ds[dau], ds[np.minimum(dau + H - 1, len(ds) - 1)]
        giu = (cuoi_mt < np.datetime64(den)) & ((dau_mt >= np.datetime64(tu)) if tu is not None else True)
        X.append(x_[giu])
        Y.append(y_[giu])
        ma.append(np.full(giu.sum(), i))
        ds_muc_tieu.append(dau_mt[giu])
    return {"X": torch.tensor(np.concatenate(X), dtype=torch.float32),
            "Y": torch.tensor(np.concatenate(Y), dtype=torch.float32),
            "ma": np.concatenate(ma), "ds": np.concatenate(ds_muc_tieu)}


def chia_train_val(df: pd.DataFrame, scaler: dict, ti_le_val: float = 0.2, seed: int = 0) -> tuple[dict, dict]:
    """Cắt mọi cửa sổ trước MOC_TEST, rồi rút ngẫu nhiên 20% làm val, còn lại làm train."""
    tat_ca = tao_tap(df, scaler, None, MOC_TEST, buoc=BUOC_TRAIN)
    tron = np.random.default_rng(seed).permutation(len(tat_ca["X"]))
    n_val = int(ti_le_val * len(tron))
    lay = lambda i: {k: v[i] for k, v in tat_ca.items()}  # noqa: E731
    return lay(np.sort(tron[n_val:])), lay(np.sort(tron[:n_val]))


# ---------------------------------------------------------------------------- chuẩn hoá

def hoc_scaler(df: pd.DataFrame, moc: pd.Timestamp = MOC_VAL) -> dict[str, tuple[float, float]]:
    """Trung bình và độ lệch chuẩn của từng chuỗi."""
    tr = df
    return {uid: (float(g.mean()), float(g.std()) + 1e-8) for uid, g in tr.groupby("unique_id")["y"]}


def chuan_hoa(y: np.ndarray, tham_so: tuple[float, float]) -> np.ndarray:
    return (y - tham_so[0]) / tham_so[1]


def bo_chuan_hoa(z: np.ndarray, tham_so: tuple[float, float]) -> np.ndarray:
    return z * tham_so[1] + tham_so[0]


class RevIN(nn.Module):
    """Chuẩn hoá theo từng cửa sổ: trừ trung bình, chia độ lệch chuẩn của CHÍNH đầu vào; dự báo xong thì nhân, cộng lại."""

    def chuan(self, x: torch.Tensor) -> torch.Tensor:
        self.tb = x.mean(dim=1, keepdim=True)
        self.dl = x.std(dim=1, keepdim=True) + 1e-5
        return (x - self.tb) / self.dl

    def tra_lai(self, y: torch.Tensor) -> torch.Tensor:
        return y * self.dl + self.tb


# ---------------------------------------------------------------------------- ba mạng

class MLP(nn.Module):
    def __init__(self, an: int = 256, revin: bool = False):
        super().__init__()
        self.revin = RevIN() if revin else None
        self.mang = nn.Sequential(nn.Linear(L, an), nn.ReLU(), nn.Linear(an, an), nn.ReLU(), nn.Linear(an, H))

    def forward(self, x):                        # x: (lô, L)
        if self.revin:
            return self.revin.tra_lai(self.mang(self.revin.chuan(x)))
        return self.mang(x)


class LSTMDuBao(nn.Module):
    """Đọc L giờ từng bước; trạng thái ẩn cuối cùng → H giờ tới (chiến lược direct: một lần ra cả H)."""

    def __init__(self, an: int = 32, revin: bool = False):
        super().__init__()
        self.revin = RevIN() if revin else None
        self.lstm = nn.LSTM(input_size=1, hidden_size=an, batch_first=True)
        self.ra = nn.Linear(an, H)

    def forward(self, x):
        z = self.revin.chuan(x) if self.revin else x
        _, (h, _) = self.lstm(z.unsqueeze(-1))    # h: (1, lô, an) — trạng thái ẩn sau giờ cuối
        y = self.ra(h[-1])
        return self.revin.tra_lai(y) if self.revin else y


class TichChapNhanQua(nn.Module):
    """Tích chập 1 chiều chỉ nhìn về quá khứ: đệm (k − 1)·d số 0 bên TRÁI, không đệm bên phải."""

    def __init__(self, vao: int, ra: int, k: int, d: int):
        super().__init__()
        self.dem = (k - 1) * d
        self.conv = nn.Conv1d(vao, ra, k, dilation=d)

    def forward(self, x):                        # x: (lô, kênh, thời gian)
        return self.conv(nn.functional.pad(x, (self.dem, 0)))


class TCN(nn.Module):
    """Các lớp tích chập nhân quả, dilation 1, 2, 4, …, 64; k = 3 → nhìn được 1 + 2·127 = 255 giờ ≥ L."""

    def __init__(self, kenh: int = 16, k: int = 3, cac_d: tuple[int, ...] = (1, 2, 4, 8, 16, 32, 64), revin: bool = False):
        super().__init__()
        self.revin = RevIN() if revin else None
        self.vao = nn.Conv1d(1, kenh, 1)
        self.lop = nn.ModuleList([TichChapNhanQua(kenh, kenh, k, d) for d in cac_d])
        self.ra = nn.Linear(kenh, H)

    def dac_trung(self, x):                      # (lô, L) → (lô, kênh, L); vị trí t chỉ phụ thuộc x[:, :t+1]
        z = self.vao(x.unsqueeze(1))
        for lop in self.lop:
            z = z + torch.relu(lop(z))           # nối tắt (residual): cộng đầu vào vào đầu ra của lớp
        return z

    def forward(self, x):
        z = self.revin.chuan(x) if self.revin else x
        y = self.ra(self.dac_trung(z)[:, :, -1])
        return self.revin.tra_lai(y) if self.revin else y


MO_HINH = {"MLP": MLP, "LSTM": LSTMDuBao, "TCN": TCN}


# ---------------------------------------------------------------------------- huấn luyện

@contextmanager
def so_luong(n: int):
    """Tạm dùng n luồng CPU. n = 1: phép cộng luôn theo một thứ tự → mọi lần chạy ra đúng cùng số (chậm hơn với mạng lớn)."""
    cu = torch.get_num_threads()
    torch.set_num_threads(n)
    try:
        yield
    finally:
        torch.set_num_threads(cu)


def dat_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)


def huan_luyen(mo_hinh: nn.Module, train: dict, val: dict, so_epoch: int = 30, lo: int = 256, buoc_moi_epoch: int = 100,
               lr: float = 1e-3, kien_nhan: int = 5, seed: int = 0) -> dict:
    """Adam + hàm mất mát MAE. Mỗi epoch: `buoc_moi_epoch` lô rút ngẫu nhiên từ train; rồi đo MAE trên val.
    Dừng sớm khi val không giảm `kien_nhan` epoch liền; trả trọng số của epoch val tốt nhất."""
    dat_seed(seed)
    rng = np.random.default_rng(seed)
    opt = torch.optim.Adam(mo_hinh.parameters(), lr=lr)
    mat_mat = nn.L1Loss()
    lich_su, tot_nhat, trong_so_tot, cho = [], np.inf, None, 0
    t0 = time.time()
    for epoch in range(so_epoch):
        mo_hinh.train()
        loss_train = []
        for _ in range(buoc_moi_epoch):
            i = rng.integers(0, len(train["X"]), lo)
            loss = mat_mat(mo_hinh(train["X"][i]), train["Y"][i])
            opt.zero_grad()
            loss.backward()                      # autograd: đạo hàm của loss theo mọi trọng số
            opt.step()                           # trọng số ← trọng số − lr × (bước Adam)
            loss_train.append(loss.item())
        loss_val = danh_gia(mo_hinh, val)
        lich_su.append({"epoch": epoch + 1, "train": float(np.mean(loss_train)), "val": loss_val})
        if loss_val < tot_nhat - 1e-4:
            tot_nhat, cho = loss_val, 0
            trong_so_tot = {k: v.clone() for k, v in mo_hinh.state_dict().items()}
        else:
            cho += 1
            if cho >= kien_nhan:
                break
    mo_hinh.load_state_dict(trong_so_tot)
    return {"lich_su": pd.DataFrame(lich_su), "giay": time.time() - t0, "val_tot_nhat": tot_nhat}


@torch.no_grad()
def du_bao_tap(mo_hinh: nn.Module, tap: dict, lo: int = 4096) -> torch.Tensor:
    mo_hinh.eval()
    return torch.cat([mo_hinh(tap["X"][i:i + lo]) for i in range(0, len(tap["X"]), lo)])


def danh_gia(mo_hinh: nn.Module, tap: dict) -> float:
    """MAE trên thang đã chuẩn hoá (đơn vị: độ lệch chuẩn của chuỗi)."""
    return float((du_bao_tap(mo_hinh, tap) - tap["Y"]).abs().mean())


# ---------------------------------------------------------------------------- dự báo tại các mốc test

def tap_moc(df: pd.DataFrame, scaler: dict, cac_moc: list[pd.Timestamp]) -> dict:
    """Một mẫu cho mỗi (chuỗi, mốc): đầu vào là L giờ ngay trước mốc, mục tiêu là H giờ sau mốc."""
    X, Y, uid_, moc_ = [], [], [], []
    for uid, g in df.groupby("unique_id", sort=True):
        s = g.set_index("ds")["y"]
        for m in cac_moc:
            X.append(chuan_hoa(s.loc[m - pd.Timedelta(hours=L):m - pd.Timedelta(hours=1)].to_numpy(), scaler[uid]))
            Y.append(chuan_hoa(s.loc[m:m + pd.Timedelta(hours=H - 1)].to_numpy(), scaler[uid]))
            uid_.append(uid)
            moc_.append(m)
    return {"X": torch.tensor(np.stack(X), dtype=torch.float32), "Y": torch.tensor(np.stack(Y), dtype=torch.float32),
            "unique_id": np.array(uid_), "moc": np.array(moc_)}


def du_bao_dl(mo_hinh: nn.Module, tap: dict, scaler: dict, ten: str) -> pd.DataFrame:
    """Dự báo dạng dài unique_id, moc, ds, <ten> (kW), đã trả về thang gốc."""
    z = du_bao_tap(mo_hinh, tap).numpy()
    dong = []
    for k, (uid, m) in enumerate(zip(tap["unique_id"], tap["moc"], strict=True)):
        dong.append(pd.DataFrame({"unique_id": uid, "moc": m, "ds": pd.date_range(m, periods=H, freq="h"),
                                  ten: bo_chuan_hoa(z[k], scaler[uid])}))
    return pd.concat(dong, ignore_index=True)


# ---------------------------------------------------------------------------- baseline trên cùng các mốc

def seasonal_naive(df: pd.DataFrame, cac_moc: list[pd.Timestamp], m: int = 168) -> pd.DataFrame:
    s = df.set_index(["unique_id", "ds"])["y"]
    dong = []
    for uid in sorted(df["unique_id"].unique()):
        for mo in cac_moc:
            ds = pd.date_range(mo, periods=H, freq="h")
            dong.append(pd.DataFrame({"unique_id": uid, "moc": mo, "ds": ds,
                                      "SeasonalNaive": s.loc[uid].reindex(ds - pd.Timedelta(hours=m)).to_numpy()}))
    return pd.concat(dong, ignore_index=True)


def mstl(df: pd.DataFrame, cac_moc: list[pd.Timestamp], so_tuan: int = 8) -> pd.DataFrame:
    """MSTL (mùa vụ 24 và 168 giờ, phần còn lại AutoETS), học lại ở mỗi mốc trên 8 tuần gần nhất."""
    from statsforecast import StatsForecast
    from statsforecast.models import MSTL
    sf = StatsForecast(models=[MSTL(season_length=[24, 168])], freq="h", n_jobs=4)
    dong = []
    for mo in cac_moc:
        cua = df[(df["ds"] < mo) & (df["ds"] >= mo - pd.Timedelta(weeks=so_tuan))]
        p = sf.forecast(df=cua[["unique_id", "ds", "y"]], h=H)
        dong.append(p.assign(moc=mo))
    return pd.concat(dong, ignore_index=True)[["unique_id", "moc", "ds", "MSTL"]]


def lightgbm(df: pd.DataFrame, cac_moc: list[pd.Timestamp]) -> pd.DataFrame:
    """LightGBM global, lag 24…168 giờ (≥ H nên không phải đệ quy) + giờ trong ngày, thứ trong tuần; chuẩn hoá theo chuỗi.
    Học MỘT lần trên dữ liệu trước MOC_TEST (như mạng DL), rồi dự báo từng mốc bằng lịch sử thật tới mốc."""
    import lightgbm as lgb
    from mlforecast import MLForecast
    from mlforecast.target_transforms import LocalStandardScaler
    fc = MLForecast(models={"LightGBM": lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=63, verbose=-1,
                                                          random_state=0, n_jobs=4)},
                    freq="h", lags=[24, 48, 72, 96, 120, 144, 168], date_features=["hour", "dayofweek"],
                    target_transforms=[LocalStandardScaler()])
    fc.fit(df[df["ds"] < MOC_TEST][["unique_id", "ds", "y"]])
    dong = []
    for mo in cac_moc:
        p = fc.predict(h=H, new_df=df[df["ds"] < mo][["unique_id", "ds", "y"]])
        dong.append(p.assign(moc=mo))
    return pd.concat(dong, ignore_index=True)[["unique_id", "moc", "ds", "LightGBM"]]


# ---------------------------------------------------------------------------- chấm

def mau_so_mase(df: pd.DataFrame, m: int = 168) -> pd.Series:
    """MAE của seasonal naive (lặp lại tuần trước) trên đoạn train, từng chuỗi — mẫu số MASE."""
    tr = df[df["ds"] < MOC_VAL].sort_values(["unique_id", "ds"])
    return tr.groupby("unique_id")["y"].apply(lambda y: np.mean(np.abs(y.to_numpy()[m:] - y.to_numpy()[:-m])))


def mase_tap(mo_hinh: nn.Module, tap: dict, scaler: dict, df: pd.DataFrame) -> float:
    """MASE trung bình qua các chuỗi của một tập mẫu (train, val hay test), tính trên thang gốc (kW)."""
    uid = tap["unique_id"] if "unique_id" in tap else np.array(sorted(df["unique_id"].unique()))[tap["ma"]]
    sd = np.array([scaler[u][1] for u in uid])
    e = np.abs((du_bao_tap(mo_hinh, tap).numpy() - tap["Y"].numpy()) * sd[:, None]).mean(axis=1)
    mae = pd.Series(e, index=uid).groupby(level=0).mean()
    return float((mae / mau_so_mase(df).loc[mae.index]).mean())


def bang_mase(du_bao: pd.DataFrame, df: pd.DataFrame, cac_cot: list[str], doi_muc: list[str]) -> pd.DataFrame:
    """MASE trung bình qua các chuỗi (mọi mốc test gộp lại), cho cả 50 khách hàng và riêng nhóm đổi mức."""
    d = du_bao.merge(df[["unique_id", "ds", "y"]], on=["unique_id", "ds"])
    mau = mau_so_mase(df)
    ra = {}
    for c in cac_cot:
        mae = d.assign(e=(d["y"] - d[c]).abs()).groupby("unique_id")["e"].mean()
        mase = mae / mau.loc[mae.index]
        ra[c] = {"MASE (50 khách)": mase.mean(), "MASE (đổi mức)": mase.loc[mase.index.isin(doi_muc)].mean(),
                 "MASE (còn lại)": mase.loc[~mase.index.isin(doi_muc)].mean()}
    return pd.DataFrame(ra).T.round(3)
