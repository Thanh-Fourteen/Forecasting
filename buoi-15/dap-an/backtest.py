# %% [markdown]
# # Buổi 15 — Backtesting đúng cách
#
# Bản ĐÃ SỬA. Dữ liệu: tải điện ERCOT (Texas) theo giờ năm 2024 (EIA-930), 414 chuỗi M4 theo giờ (Monash).
#
# Buổi này **không** dùng `tv.backtest` (đã bỏ khỏi `tv/`): `chia_cua_so`, `backtest`, `diebold_mariano` là bộ
# backtest bạn tự viết hôm nay, cùng giao diện với bộ cả khoá dùng từ buổi 16.

# %%
from __future__ import annotations

import warnings
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

H_DIEN = 24                                # dự báo tải điện ngày tới: 24 giờ
MOC_HOLD_OUT = pd.Timestamp("2024-10-01")  # 3 tháng cuối để riêng, chỉ mở một lần
H_M4 = 48                                  # tầm dự báo chính thức của M4 Hourly
M = 24                                     # chu kỳ ngày của dữ liệu giờ


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_dien(ba: str = "ERCO") -> pd.Series:
    """Tải điện theo giờ 2024 của một vùng điều độ (MW), mốc UTC cuối giờ, lỗ ≤ 3 giờ nội suy."""
    khung = []
    for thu_muc, ten in (("eia930-balance-2024-h1", "EIA930_BALANCE_2024_Jan_Jun.csv"),
                         ("eia930-balance-2024-h2", "EIA930_BALANCE_2024_Jul_Dec.csv")):
        d = pd.read_csv(tv.THU_MUC_DU_LIEU / thu_muc / ten, low_memory=False,
                        usecols=["Balancing Authority", "UTC Time at End of Hour", "Demand (MW)"])
        khung.append(d[d["Balancing Authority"] == ba])
    d = pd.concat(khung)
    moc = pd.to_datetime(d["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p")
    y = pd.Series(pd.to_numeric(d["Demand (MW)"], errors="coerce").to_numpy(), index=moc, name="y").sort_index()
    return y[~y.index.duplicated()].asfreq("h").interpolate(limit=3)


def doc_m4_gio() -> dict[str, np.ndarray]:
    """414 chuỗi M4 theo giờ (.tsf của Monash)."""
    tep = tv.THU_MUC_DU_LIEU / "monash-m4-hourly" / "m4_hourly_dataset.tsf"
    chuoi, trong_data = {}, False
    with open(tep, encoding="utf-8", errors="ignore") as f:
        for dong in f:
            if not trong_data:
                trong_data = dong.strip().lower() == "@data"
                continue
            if dong.strip():
                phan = dong.strip().split(":")
                chuoi[phan[0]] = np.array([float(x) for x in phan[-1].split(",") if x not in ("?", "")])
    return chuoi


def dang_dai(y: pd.Series, ten: str = "ERCO") -> pd.DataFrame:
    """Chuỗi → bảng dạng dài unique_id, ds, y (dạng mà backtest và statsforecast nhận)."""
    return pd.DataFrame({"unique_id": ten, "ds": y.index, "y": y.to_numpy()})


# %% [markdown]
# ## Feature và mô hình: dự báo ngày tới
#
# Mọi lag ≥ 24 giờ: lúc ra dự báo cho cả ngày mai, số của ngày mai chưa có (buổi 13).

# %%
LAG = (24, 25, 26, 48, 72, 168, 336)


def bang_feature(y: pd.Series) -> pd.DataFrame:
    """Feature cho y_t chỉ dùng y tới t − 24."""
    f = pd.DataFrame(index=y.index)
    for lag in LAG:
        f[f"lag_{lag}"] = y.shift(lag)
    f["tb_24"] = y.shift(24).rolling(24).mean()
    f["gio"] = y.index.hour
    f["thu"] = y.index.dayofweek
    f["ngay_trong_nam"] = y.index.dayofyear
    return f


def tao_rung():
    """Rừng ngẫu nhiên (random forest): học thuộc rất giỏi — nên chia ngẫu nhiên lừa nó nặng nhất."""
    from sklearn.ensemble import RandomForestRegressor
    return RandomForestRegressor(n_estimators=200, min_samples_leaf=2, n_jobs=-1, random_state=0)


def tao_hoi_quy():
    """Hồi quy tuyến tính trên cùng feature."""
    from sklearn.linear_model import LinearRegression
    return LinearRegression()


MO_HINH = {"rừng ngẫu nhiên": tao_rung, "hồi quy tuyến tính": tao_hoi_quy}


def _mae(a, b) -> float:
    return float(np.mean(np.abs(np.asarray(a, float) - np.asarray(b, float))))


# %% [markdown]
# ## Bộ backtest: cửa sổ rolling origin
#
# Cùng giao diện với bộ cả khoá dùng (`tv.backtest`, từ buổi 16). Dữ liệu dạng dài `unique_id, ds, y`.
# Một cửa sổ: `... học (ds ≤ cutoff) | gap bước bỏ trống | h bước kiểm`.

# %%
@dataclass(frozen=True)
class CuaSo:
    thu_tu: int
    cutoff: object         # ds cuối cùng mô hình được thấy
    bat_dau_test: object   # ds đầu tiên phải dự báo (sau gap)
    ket_thuc_test: object
    bat_dau_train: object


def _gia_tri(v):
    return pd.Timestamp(v) if isinstance(v, np.datetime64) else v.item() if hasattr(v, "item") else v


def chia_cua_so(df: pd.DataFrame, h: int, so_cua_so: int, buoc: int | None = None, gap: int = 0,
                cua_so_train: int | None = None, cot_ds: str = "ds") -> list[CuaSo]:
    """Các cửa sổ rolling origin; cửa sổ cuối kết thúc đúng ở ds cuối của dữ liệu.

    buoc: khoảng cách giữa hai cutoff liền nhau (mặc định = h, các đoạn kiểm nối nhau không chồng).
    cua_so_train=None: expanding (học trên toàn bộ quá khứ); = L: sliding (chỉ L bước cuối).
    """
    if h < 1 or so_cua_so < 1 or gap < 0:
        raise ValueError("cần h ≥ 1, so_cua_so ≥ 1, gap ≥ 0")
    buoc = h if buoc is None else buoc
    if buoc < 1:
        raise ValueError("buoc ≥ 1")
    truc = np.sort(df[cot_ds].unique())
    n = len(truc)
    cuoi = n - 1 - gap - h                   # vị trí cutoff của cửa sổ cuối
    dau = cuoi - buoc * (so_cua_so - 1)
    if dau < (cua_so_train or 1) - 1:
        raise ValueError(f"không đủ dữ liệu: {n} mốc cho {so_cua_so} cửa sổ (h={h}, buoc={buoc}, gap={gap})")
    ra = []
    for k in range(so_cua_so):
        c = dau + k * buoc
        bd = 0 if cua_so_train is None else c - cua_so_train + 1
        ra.append(CuaSo(k, _gia_tri(truc[c]), _gia_tri(truc[c + gap + 1]), _gia_tri(truc[c + gap + h]),
                        _gia_tri(truc[bd])))
    return ra


def backtest(df: pd.DataFrame, ham_du_bao: Callable, h: int, so_cua_so: int, buoc: int | None = None,
             gap: int = 0, cua_so_train: int | None = None,
             cot_id: str = "unique_id", cot_ds: str = "ds", cot_y: str = "y") -> pd.DataFrame:
    """Chạy ham_du_bao(lich_su, ds_can_du_bao) ở mọi cửa sổ; trả unique_id, ds, cutoff, buoc_h, y, <dự báo>.

    lich_su chỉ có dòng ds ≤ cutoff: hàm dự báo KHÔNG thấy y của đoạn kiểm. Mỗi cửa sổ học lại (refit).
    """
    if df.duplicated([cot_id, cot_ds]).any():
        raise ValueError(f"có dòng trùng ({cot_id}, {cot_ds})")
    truc = np.sort(df[cot_ds].unique())
    vi_tri = pd.Series(np.arange(len(truc)), index=pd.Index(truc))
    ket_qua = []
    for cs in chia_cua_so(df, h, so_cua_so, buoc, gap, cua_so_train, cot_ds):
        lich_su = df[(df[cot_ds] >= cs.bat_dau_train) & (df[cot_ds] <= cs.cutoff)]
        test = df[(df[cot_ds] >= cs.bat_dau_test) & (df[cot_ds] <= cs.ket_thuc_test)]
        du_bao = pd.DataFrame(ham_du_bao(lich_su.copy(), test[[cot_id, cot_ds]].reset_index(drop=True)))
        if cot_y in du_bao.columns:
            raise ValueError(f"dự báo không được chứa cột {cot_y!r}")
        ghep = test[[cot_id, cot_ds, cot_y]].merge(du_bao, on=[cot_id, cot_ds], how="outer", indicator=True)
        if (ghep["_merge"] != "both").any():
            raise ValueError(f"cửa sổ {cs.thu_tu}: dự báo thừa hoặc thiếu dòng so với đoạn kiểm")
        ghep = ghep.drop(columns="_merge")
        ghep.insert(2, "cutoff", cs.cutoff)
        ghep.insert(3, "buoc_h", vi_tri.loc[ghep[cot_ds].to_numpy()].to_numpy() - vi_tri.loc[cs.cutoff])
        ket_qua.append(ghep)
    return pd.concat(ket_qua, ignore_index=True).sort_values(["cutoff", cot_id, cot_ds], ignore_index=True)


# %% [markdown]
# ## Hàm dự báo cho backtest

# %%
def ham_du_bao_ml(tao_mo_hinh: Callable, ten: str = "du_bao") -> Callable:
    """Bọc một mô hình scikit-learn thành ham_du_bao(lich_su, ds_can) cho backtest (một chuỗi)."""
    def du_bao(lich_su: pd.DataFrame, ds_can: pd.DataFrame) -> pd.DataFrame:
        y = lich_su.set_index("ds")["y"]
        y_mo_rong = y.reindex(y.index.union(pd.DatetimeIndex(ds_can["ds"])))  # y tương lai = NaN
        f = bang_feature(y_mo_rong)
        hoc = f.loc[y.index].assign(y=y).dropna()
        mo_hinh = tao_mo_hinh().fit(hoc.drop(columns="y"), hoc["y"])
        return ds_can.assign(**{ten: mo_hinh.predict(f.loc[pd.DatetimeIndex(ds_can["ds"])])})
    return du_bao


def seasonal_naive(lich_su: pd.DataFrame, ds_can: pd.DataFrame, m: int = M) -> pd.DataFrame:
    """Lặp lại m giá trị cuối của lịch sử, cho từng chuỗi."""
    ra = []
    for uid, nhom in ds_can.groupby("unique_id", sort=False):
        cuoi = lich_su.loc[lich_su["unique_id"] == uid].sort_values("ds")["y"].to_numpy()[-m:]
        ra.append(nhom.assign(seasonal_naive=[cuoi[i % m] for i in range(len(nhom))]))
    return pd.concat(ra)


# %% [markdown]
# ## Ba cách ước lượng sai số: chia ngẫu nhiên, rolling origin, hold-out thật

# %%
def uoc_luong_sai_so(y: pd.Series, tao_mo_hinh: Callable, so_cua_so: int = 28,
                     buoc: int = 24) -> float:
    """MAE ước lượng bằng rolling origin trên phần học: 28 ngày cuối, mỗi ngày một cửa sổ học lại trên
    toàn bộ quá khứ rồi dự báo 24 giờ sau cutoff."""
    kq = backtest(dang_dai(y), ham_du_bao_ml(tao_mo_hinh), h=H_DIEN, so_cua_so=so_cua_so, buoc=buoc)
    return _mae(kq["y"], kq["du_bao"])


def uoc_luong_kfold(y: pd.Series, tao_mo_hinh: Callable, k: int = 5, seed: int = 0) -> float:
    """MAE ước lượng bằng K-fold XÁO TRỘN — để đo xem nó lạc quan cỡ nào, không phải để dùng."""
    from sklearn.model_selection import KFold
    bang = bang_feature(y).assign(y=y).dropna()
    X, t = bang.drop(columns="y"), bang["y"]
    loi = []
    for hoc, kiem in KFold(k, shuffle=True, random_state=seed).split(bang):
        mo_hinh = tao_mo_hinh().fit(X.iloc[hoc], t.iloc[hoc])
        loi.append(_mae(mo_hinh.predict(X.iloc[kiem]), t.iloc[kiem]))
    return float(np.mean(loi))


def sai_so_hold_out(y: pd.Series, tao_mo_hinh: Callable, moc: pd.Timestamp = MOC_HOLD_OUT) -> float:
    """Sai số THẬT: học một lần trên mọi thứ trước mốc, chấm trên 3 tháng sau mốc (mở một lần duy nhất)."""
    bang = bang_feature(y).assign(y=y).dropna()
    hoc, kiem = bang[bang.index < moc], bang[bang.index >= moc]
    mo_hinh = tao_mo_hinh().fit(hoc.drop(columns="y"), hoc["y"])
    return _mae(mo_hinh.predict(kiem.drop(columns="y")), kiem["y"])


def so_sanh_cach_chia(y: pd.Series, moc: pd.Timestamp = MOC_HOLD_OUT) -> pd.DataFrame:
    """Với mỗi mô hình: MAE theo K-fold xáo trộn, theo rolling origin (cả hai chỉ dùng phần trước mốc), và hold-out."""
    hoc = y[y.index < moc]
    hang = []
    for ten, tao in MO_HINH.items():
        that = sai_so_hold_out(y, tao, moc)
        kf, ro = uoc_luong_kfold(hoc, tao), uoc_luong_sai_so(hoc, tao)
        hang.append({"mô hình": ten, "K-fold xáo trộn": kf, "rolling origin": ro, "hold-out thật": that,
                     "lệch K-fold (%)": (kf / that - 1) * 100, "lệch rolling (%)": (ro / that - 1) * 100})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Tune, chọn, báo cáo: ba tập riêng
#
# Trên 414 chuỗi M4 theo giờ, mỗi chuỗi tự chọn phương pháp tốt nhất trong vài ứng viên đơn giản.

# %%
def _lap(y: np.ndarray, m: int, h: int) -> np.ndarray:
    return np.array([y[-m:][i % m] for i in range(h)], dtype=float)


def ung_vien(y: np.ndarray, w: float, h: int = H_M4) -> dict[str, np.ndarray]:
    """Sáu phương pháp đơn giản; 'trộn' = w × (cùng giờ hôm qua) + (1 − w) × (cùng giờ tuần trước)."""
    hom_qua, tuan_truoc = _lap(y, 24, h), _lap(y, 168, h)
    ba_ngay = np.mean([_lap(y[: len(y) - 24 * j] if j else y, 24, h) for j in range(3)], axis=0)
    return {"naive": np.repeat(y[-1], h), "seasonal naive 24": hom_qua, "seasonal naive 168": tuan_truoc,
            "trung bình 3 ngày": ba_ngay, "trung bình tuần": np.repeat(y[-168:].mean(), h),
            "trộn": w * hom_qua + (1 - w) * tuan_truoc}


def mase(that: np.ndarray, du_bao: np.ndarray, hoc: np.ndarray, m: int = M) -> float:
    return _mae(that, du_bao) / float(np.mean(np.abs(hoc[m:] - hoc[:-m])))


LUOI_W = np.round(np.arange(0, 1.01, 0.1), 1)


def _cham(v: np.ndarray, dau: int, w: float, h: int = H_M4) -> dict[str, float]:
    """MASE của mọi ứng viên khi dự báo đoạn v[dau : dau + h] từ lịch sử v[:dau]."""
    hoc, that = v[:dau], v[dau:dau + h]
    return {k: mase(that, d, hoc) for k, d in ung_vien(hoc, w, h).items()}


def chon_va_bao_cao(chuoi: dict[str, np.ndarray], h: int = H_M4) -> pd.DataFrame:
    """Ba đoạn cuối mỗi chuỗi: T (tune w của 'trộn'), A (chọn phương pháp), B (báo cáo). Không đoạn nào dùng lại.

    Trả một dòng mỗi chuỗi: phương pháp được chọn, MASE báo cáo (trên B), và MASE của seasonal naive 24 trên B.
    """
    hang = []
    for ten, v in chuoi.items():
        n = len(v)
        T, A, B = n - 3 * h, n - 2 * h, n - h
        w = min(LUOI_W, key=lambda x: _cham(v, T, x, h)["trộn"])
        diem_A = _cham(v, A, w, h)
        chon = min(diem_A, key=diem_A.get)
        diem_B = _cham(v, B, w, h)
        hang.append({"chuỗi": ten, "w": w, "chọn": chon, "MASE lúc chọn (A)": diem_A[chon],
                     "MASE báo cáo (B)": diem_B[chon], "seasonal naive 24 (B)": diem_B["seasonal naive 24"]})
    return pd.DataFrame(hang)


def chon_va_bao_cao_cung_cua_so(chuoi: dict[str, np.ndarray], h: int = H_M4) -> pd.DataFrame:
    """Cách SAI để đo: tune, chọn và báo cáo đều trên đoạn cuối B."""
    hang = []
    for ten, v in chuoi.items():
        B = len(v) - h
        w = min(LUOI_W, key=lambda x: _cham(v, B, x, h)["trộn"])
        diem = _cham(v, B, w, h)
        chon = min(diem, key=diem.get)
        hang.append({"chuỗi": ten, "chọn": chon, "MASE báo cáo (B)": diem[chon]})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Kiểm định Diebold–Mariano (bản hiệu chỉnh Harvey, Leybourne & Newbold 1997)

# %%
@dataclass(frozen=True)
class KetQuaDM:
    thong_ke: float
    p_value: float
    n: int
    h: int
    trung_binh_chenh: float  # mean(mất mát 1 − mất mát 2): âm = dự báo 1 tốt hơn


def diebold_mariano(e1, e2, h: int = 1, ham_mat_mat: str = "tuyet_doi", hieu_chinh: bool = True) -> KetQuaDM:
    """H0: hai dự báo có cùng mất mát kỳ vọng. e1, e2: sai số (thực tế − dự báo) cùng tầm h, cùng thời điểm.

    d_t = g(e1_t) − g(e2_t). Dự báo h bước tới thì sai số của các mốc liền nhau dùng chung thông tin, nên
    d_t tự tương quan tới trễ h − 1: phương sai của trung bình phải cộng các tự hiệp phương sai đó.
    """
    e1, e2 = np.asarray(e1, float), np.asarray(e2, float)
    g = np.abs if ham_mat_mat == "tuyet_doi" else np.square
    d = g(e1) - g(e2)
    n = len(d)
    if n <= h or n < 3:
        raise ValueError(f"cần n > h và n ≥ 3, có n = {n}")
    lech = d - d.mean()
    gamma = [float(np.sum(lech[k:] * lech[: n - k]) / n) for k in range(h)]
    v = (gamma[0] + 2 * sum(gamma[1:])) / n
    if v <= 0:                                   # có thể âm khi h > 1: lùi về h = 1 như forecast::dm.test
        h, v = 1, gamma[0] / n
    thong_ke = float(d.mean() / np.sqrt(v))
    from scipy import stats
    if hieu_chinh:
        thong_ke *= float(np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n))
        p = 2 * stats.t(df=n - 1).sf(abs(thong_ke))
    else:
        p = 2 * stats.norm.sf(abs(thong_ke))
    return KetQuaDM(thong_ke, float(p), n, h, float(d.mean()))


def _tron(y: pd.Series, w: float, moc: pd.DatetimeIndex) -> pd.Series:
    """'Trộn' cho tải điện: w × cùng giờ hôm qua + (1 − w) × cùng giờ tuần trước."""
    return w * y.shift(24)[moc] + (1 - w) * y.shift(168)[moc]


def tune_w(y: pd.Series, doan: pd.DatetimeIndex) -> float:
    """w cho MAE nhỏ nhất trên đoạn `doan` (lưới 0; 0,1; …; 1)."""
    return float(min(LUOI_W, key=lambda w: _mae(y[doan], _tron(y, w, doan))))


def rung_so_voi_snaive(y: pd.Series, moc: pd.Timestamp = MOC_HOLD_OUT, so_cua_so: int = 28) -> dict:
    """Rừng ngẫu nhiên và seasonal naive trên CÙNG các cửa sổ rolling origin (phần trước mốc), kèm DM-HLN."""
    rung = ham_du_bao_ml(tao_rung)

    def ca_hai(lich_su, ds_can):
        return rung(lich_su, ds_can).merge(seasonal_naive(lich_su, ds_can), on=["unique_id", "ds"])

    kq = backtest(dang_dai(y[y.index < moc]), ca_hai, h=H_DIEN, so_cua_so=so_cua_so, buoc=H_DIEN)
    theo_cua_so = kq.groupby("cutoff").apply(
        lambda g: pd.Series({"rừng": _mae(g["y"], g["du_bao"]), "seasonal naive": _mae(g["y"], g["seasonal_naive"])}))
    return {"kq": kq, "theo cửa sổ": theo_cua_so,
            "MAE rừng": _mae(kq["y"], kq["du_bao"]), "MAE seasonal naive": _mae(kq["y"], kq["seasonal_naive"]),
            "DM-HLN": diebold_mariano(kq["y"] - kq["du_bao"], kq["y"] - kq["seasonal_naive"], h=H_DIEN)}


def so_sanh_tron_voi_snaive(y: pd.Series, w: float, moc: pd.Timestamp = MOC_HOLD_OUT) -> dict:
    """Trên hold-out: seasonal naive 24 giờ so với 'trộn' có trọng số w cho trước."""
    kiem = y[y.index >= moc]
    sn = y.shift(24)[kiem.index]
    tron = _tron(y, w, kiem.index)
    e_sn, e_tron = (kiem - sn).to_numpy(), (kiem - tron).to_numpy()
    return {"w": float(w), "MAE seasonal naive": _mae(kiem, sn), "MAE trộn": _mae(kiem, tron),
            "đổi (%)": (_mae(kiem, tron) / _mae(kiem, sn) - 1) * 100,
            "DM bỏ tự tương quan": diebold_mariano(e_tron, e_sn, h=1, hieu_chinh=False),
            "DM-HLN, h = 24": diebold_mariano(e_tron, e_sn, h=H_DIEN),
            "e_sn": e_sn, "e_tron": e_tron}


# %% [markdown]
# ## Sai số theo tầm h, và đối chiếu với statsforecast

# %%
def m4_dang_dai(chuoi: dict[str, np.ndarray], do_dai: int | None = None) -> pd.DataFrame:
    """Các chuỗi M4 cùng độ dài → dạng dài, ds là số nguyên 0..n−1 (cùng trục thời gian)."""
    do_dai = do_dai or max(len(v) for v in chuoi.values())
    return pd.concat([pd.DataFrame({"unique_id": t, "ds": np.arange(do_dai), "y": v})
                      for t, v in chuoi.items() if len(v) == do_dai], ignore_index=True)


def sai_so_theo_h(kq: pd.DataFrame, cot: str) -> pd.Series:
    """MAE theo từng bước h (trung bình trên mọi chuỗi và mọi cửa sổ)."""
    return (kq["y"] - kq[cot]).abs().groupby(kq["buoc_h"]).mean()


def doi_chieu_statsforecast(df: pd.DataFrame, h: int = H_M4, so_cua_so: int = 3) -> float:
    """Chênh tuyệt đối lớn nhất giữa seasonal naive của backtest tự viết và của statsforecast.cross_validation."""
    from statsforecast import StatsForecast
    from statsforecast.models import SeasonalNaive
    sf = StatsForecast(models=[SeasonalNaive(season_length=M)], freq=1)
    cv = sf.cross_validation(df=df, h=h, n_windows=so_cua_so, step_size=h).reset_index()
    tu_viet = backtest(df, seasonal_naive, h=h, so_cua_so=so_cua_so)
    ghep = tu_viet.merge(cv, on=["unique_id", "ds", "cutoff"], validate="one_to_one")
    if len(ghep) != len(tu_viet):
        raise ValueError("cutoff hoặc mốc dự báo không khớp statsforecast")
    return float((ghep["seasonal_naive"] - ghep["SeasonalNaive"]).abs().max())


# %%
if __name__ == "__main__":
    y = doc_dien()
    print(so_sanh_cach_chia(y).round(1).to_string(index=False))
    kiem = y[y.index >= MOC_HOLD_OUT].index
    hoc = y[(y.index < MOC_HOLD_OUT) & (y.index >= MOC_HOLD_OUT - pd.Timedelta(days=91))].index
    for nhan, doan in (("tune trên chính hold-out (SAI)", kiem), ("tune trên 3 tháng trước mốc", hoc)):
        kq = so_sanh_tron_voi_snaive(y, tune_w(y, doan))
        print(nhan, {k: v for k, v in kq.items() if not k.startswith("e_")})
    rs = rung_so_voi_snaive(y)
    print({k: v for k, v in rs.items() if k not in ("kq", "theo cửa sổ")})
    print(rs["theo cửa sổ"].describe().round(0))
    chuoi = doc_m4_gio()
    dung, sai = chon_va_bao_cao(chuoi), chon_va_bao_cao_cung_cua_so(chuoi)
    print("ba tập: trung vị", dung[["MASE lúc chọn (A)", "MASE báo cáo (B)", "seasonal naive 24 (B)"]].median().round(3).to_dict())
    print("cùng cửa sổ: trung vị", round(float(sai["MASE báo cáo (B)"].median()), 3))
    df = m4_dang_dai(chuoi)
    print("số chuỗi dài nhất:", df["unique_id"].nunique(), "| lệch statsforecast:", doi_chieu_statsforecast(df))
