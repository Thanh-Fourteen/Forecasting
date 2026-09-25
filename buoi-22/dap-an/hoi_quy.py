# %% [markdown]
# # Buổi 22 — Biến dự báo thành bài toán hồi quy (ĐÁP ÁN)
#
# Dữ liệu: lượt xem Wikipedia theo ngày (Kaggle Web Traffic, Monash), 2015-07-01 → 2017-09-10.
# Mọi mô hình học và chấm trên z = log(1 + lượt xem).

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv
from tv.du_lieu import doc_tsf

warnings.simplefilter("ignore")

TEP = "kaggle_web_traffic_dataset_without_missing_values.tsf"
SO_CHUOI = 10_000     # số chuỗi của bài global
H = 14                # tầm dự báo: 14 ngày
SO_CUA_SO = 3         # 3 cutoff, cách nhau 14 ngày → chấm 42 ngày cuối (31/7 → 10/9/2017)
M = 7                 # mùa vụ tuần
SO_LAG = 28           # mô hình tự viết nhìn 28 ngày gần nhất
SEED = 0


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_web_traffic(so_chuoi: int = SO_CHUOI) -> pd.DataFrame:
    """Dạng dài unique_id, ds, y (lượt xem), z = log(1 + y). Giữ `so_chuoi` chuỗi đầu tệp có dưới 5% ngày bằng 0
    trong phần học (Monash đã thay ô thiếu bằng 0). Chỉ nhìn phần học để chọn, không nhìn kỳ chấm."""
    doc = int(so_chuoi * 1.25) + 20
    df, _ = doc_tsf(tv.THU_MUC_DU_LIEU / "monash-web-traffic" / TEP, gioi_han_chuoi=doc)
    truc = np.sort(df["ds"].unique())
    cutoff_dau = truc[len(truc) - H * SO_CUA_SO - 1]
    ty_le_0 = (df[df["ds"] <= cutoff_dau].assign(bang_0=lambda d: d["y"] == 0)
               .groupby("unique_id", sort=False)["bang_0"].mean())
    giu = ty_le_0[ty_le_0 < 0.05].index[:so_chuoi]
    df = df[df["unique_id"].isin(giu)].reset_index(drop=True)
    df["z"] = np.log1p(df["y"])
    return df


def ma_tran(df: pd.DataFrame, cot: str = "z") -> pd.DataFrame:
    """Mỗi dòng một chuỗi, mỗi cột một ngày."""
    return df.pivot(index="unique_id", columns="ds", values=cot)


def cac_cutoff(df: pd.DataFrame) -> list:
    """Ba cutoff của backtest: ngày cuối được thấy trước mỗi đoạn 14 ngày chấm."""
    truc = np.sort(df["ds"].unique())
    return [truc[len(truc) - H * (SO_CUA_SO - i) - 1] for i in range(SO_CUA_SO)]


# %% [markdown]
# ## 1. Chuỗi thành bảng, và dự báo đệ quy cho một chuỗi

# %%
def bang_lag(z: np.ndarray, so_lag: int) -> tuple[np.ndarray, np.ndarray]:
    """Mỗi dòng: X = (z[t-1], z[t-2], …, z[t-so_lag]) — mới nhất đứng đầu; nhãn = z[t]."""
    z = np.asarray(z, float)
    X = np.array([z[t - so_lag:t][::-1] for t in range(so_lag, len(z))])
    return X, z[so_lag:]


def du_bao_de_quy(mo_hinh, lich_su: np.ndarray, h: int, so_lag: int) -> np.ndarray:
    """Recursive: dự báo 1 bước, nối dự báo vào lịch sử như thể là số thật, lặp h lần."""
    lich_su = list(np.asarray(lich_su, float))
    ra = []
    for _ in range(h):
        x = np.array(lich_su[-so_lag:][::-1])[None, :]
        p = float(mo_hinh.predict(x)[0])
        ra.append(p)
        lich_su.append(p)
    return np.array(ra)


# %% [markdown]
# ## 2. Bảng đặc trưng cho mô hình global, chuẩn hoá theo chuỗi

# %%
def dac_trung(df: pd.DataFrame, h: int, so_lag: int = SO_LAG) -> pd.DataFrame:
    """Đặc trưng để dự báo z ở ngày ds khi mốc dự báo là ds − h (chiến lược direct, tầm h).

    lag_k = z của ngày ds − (h − 1) − k, k = 1 … so_lag: lag_1 là ngày ds − h, số mới nhất đã biết lúc dự báo.
    muc = trung bình các lag; các lag trừ đi muc (chuẩn hoá theo chuỗi). thu = thứ trong tuần của ds.
    """
    g = df.groupby("unique_id", sort=False)["z"]
    lag = pd.concat({f"lag_{k}": g.shift(h - 1 + k) for k in range(1, so_lag + 1)}, axis=1)
    muc = lag.mean(axis=1)
    ra = df[["unique_id", "ds"]].copy()
    ra["muc"] = muc
    ra[list(lag.columns)] = lag.sub(muc, axis=0)
    ra["thu"] = df["ds"].dt.dayofweek
    return ra


def _cot_x(so_lag: int = SO_LAG) -> list[str]:
    return [f"lag_{k}" for k in range(1, so_lag + 1)] + ["thu"]


def _cua_so(Z: np.ndarray, t: int, so_lag: int = SO_LAG) -> tuple[np.ndarray, np.ndarray]:
    """so_lag cột kết thúc ở cột t của ma trận Z, mới nhất đứng đầu, đã trừ mức; trả (X, muc)."""
    X = Z[:, t - so_lag + 1:t + 1][:, ::-1]
    muc = X.mean(axis=1, keepdims=True)
    return X - muc, muc.ravel()


def rung(seed: int = SEED):
    """Mô hình dùng cho cả ba chiến lược: rừng ngẫu nhiên hỗ trợ nhiều đầu ra (cần cho MIMO)."""
    from sklearn.ensemble import RandomForestRegressor
    return RandomForestRegressor(n_estimators=50, min_samples_leaf=10, max_features=0.33, n_jobs=-1,
                                 random_state=seed)


# %% [markdown]
# ## 3. Ba chiến lược đa bước

# %%
def chien_luoc(df: pd.DataFrame, h: int = H, buoc_mau: int = 7) -> pd.DataFrame:
    """Recursive, direct, MIMO trên cùng rừng ngẫu nhiên global, 3 cutoff. Trả bảng dài
    unique_id, cutoff, buoc_h, ds, y (= z thật), recursive, direct, mimo. buoc_mau: lấy một mốc mỗi 7 ngày để học."""
    Zdf = ma_tran(df)
    Z = Zdf.to_numpy()
    ngay = Zdf.columns
    thu = np.asarray(ngay.dayofweek)
    cot = _cot_x()
    ra = []
    for cutoff in cac_cutoff(df):
        c = int(np.flatnonzero(ngay == cutoff)[0])
        cac_moc = np.arange(c, SO_LAG - 1, -buoc_mau)[::-1]      # mốc học, mốc cuối = cutoff

        # recursive: một mô hình 1 bước (bảng h = 1 trên phần đã biết)
        b1 = dac_trung(df[df["ds"] <= cutoff], 1)
        b1 = b1.merge(df[["unique_id", "ds", "z"]], on=["unique_id", "ds"]).dropna()
        b1 = b1[b1["ds"].isin(ngay[cac_moc])]
        m1 = rung().fit(b1[cot].to_numpy(), (b1["z"] - b1["muc"]).to_numpy())
        lich_su = Z[:, :c + 1].copy()
        de_quy = []
        for k in range(h):
            X, muc = _cua_so(lich_su, lich_su.shape[1] - 1)
            p = m1.predict(np.column_stack([X, np.full(len(X), thu[c + 1 + k])])) + muc
            de_quy.append(p)
            lich_su = np.column_stack([lich_su, p])
        de_quy = np.array(de_quy).T

        # direct: mỗi tầm một mô hình, đặc trưng từ dac_trung(df, h) — bảng dựng trên toàn bộ dữ liệu
        truc_tiep = []
        for k in range(1, h + 1):
            b = dac_trung(df, k).merge(df[["unique_id", "ds", "z"]], on=["unique_id", "ds"])
            hoc = b[b["ds"].isin(ngay[cac_moc]) & (b["ds"] <= cutoff)].dropna()
            mk = rung().fit(hoc[cot].to_numpy(), (hoc["z"] - hoc["muc"]).to_numpy())
            du = b[b["ds"] == ngay[c + k]].set_index("unique_id").loc[Zdf.index]
            truc_tiep.append(mk.predict(du[cot].to_numpy()) + du["muc"].to_numpy())
        truc_tiep = np.array(truc_tiep).T

        # MIMO: một mô hình, đầu ra là cả vector h ngày
        Xs, Ys = [], []
        for t in cac_moc[cac_moc + h <= c]:
            X, muc = _cua_so(Z, t)
            Xs.append(np.column_stack([X, np.full(len(X), thu[t + 1])]))
            Ys.append(Z[:, t + 1:t + h + 1] - muc[:, None])
        mm = rung().fit(np.vstack(Xs), np.vstack(Ys))
        X, muc = _cua_so(Z, c)
        mimo = mm.predict(np.column_stack([X, np.full(len(X), thu[c + 1])])) + muc[:, None]

        for i, uid in enumerate(Zdf.index):
            ra.append(pd.DataFrame({"unique_id": uid, "cutoff": cutoff, "buoc_h": np.arange(1, h + 1),
                                    "ds": ngay[c + 1:c + h + 1], "y": Z[i, c + 1:c + h + 1],
                                    "recursive": de_quy[i], "direct": truc_tiep[i], "mimo": mimo[i]}))
    return pd.concat(ra, ignore_index=True)


def sai_so_theo_h(kq: pd.DataFrame, cot=("recursive", "direct", "mimo")) -> pd.DataFrame:
    """RMSE trên thang z theo từng bước h (gộp mọi chuỗi và cutoff)."""
    return kq.groupby("buoc_h").apply(lambda d: pd.Series({c: np.sqrt(np.mean((d["y"] - d[c]) ** 2)) for c in cot}))


# %% [markdown]
# ## 4. Cây quyết định và xu hướng

# %%
def du_bao_cay(y: np.ndarray, h: int, so_lag: int = 7) -> np.ndarray:
    """Cây quyết định recursive cho một chuỗi. Cây chỉ trả giá trị đã thấy khi học, nên học trên SAI PHÂN
    d_t = y_t − y_{t−1} rồi cộng dồn lại từ số cuối."""
    from sklearn.tree import DecisionTreeRegressor
    y = np.asarray(y, float)
    d = np.diff(y)
    X, nhan = bang_lag(d, so_lag)
    cay = DecisionTreeRegressor(min_samples_leaf=3, random_state=SEED).fit(X, nhan)
    return y[-1] + np.cumsum(du_bao_de_quy(cay, d, h, so_lag))


# %% [markdown]
# ## 5. Global LightGBM (mlforecast) và local AutoETS trên 10.000 chuỗi

# %%
def _tep_cache(ten: str, df: pd.DataFrame):
    return tv.THU_MUC_DU_LIEU.parent / "cache" / f"{ten}-{df['unique_id'].nunique()}.parquet"


def backtest_toan_cuc(df: pd.DataFrame, luu: bool = False) -> pd.DataFrame:
    """MỘT mô hình LightGBM cho mọi chuỗi, recursive (mặc định của mlforecast). 10.000 chuỗi: vài phút."""
    tep = _tep_cache("toan-cuc", df)
    if luu and tep.exists():
        return pd.read_parquet(tep)
    import lightgbm as lgb
    from mlforecast import MLForecast
    from mlforecast.lag_transforms import RollingMean
    fc = MLForecast(
        models={"LightGBM": lgb.LGBMRegressor(n_estimators=300, learning_rate=0.08, num_leaves=63,
                                              random_state=SEED, verbose=-1)},
        freq="D", lags=[1, 2, 3, 4, 5, 6, 7, 14, 21, 28],
        lag_transforms={1: [RollingMean(7), RollingMean(28)]}, date_features=["dayofweek"])
    kq = fc.cross_validation(df[["unique_id", "ds", "z"]], h=H, n_windows=SO_CUA_SO, step_size=H, target_col="z")
    if luu:
        tep.parent.mkdir(parents=True, exist_ok=True)
        kq.to_parquet(tep)
    return kq


def backtest_cuc_bo(df: pd.DataFrame, luu: bool = False) -> pd.DataFrame:
    """MỖI chuỗi một mô hình: AutoETS (không xu hướng, mùa vụ 7 — bật xu hướng chậm gấp 6 mà không chính xác hơn),
    seasonal naive, naive. 10.000 chuỗi: vài phút."""
    tep = _tep_cache("cuc-bo", df)
    if luu and tep.exists():
        return pd.read_parquet(tep)
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, Naive, SeasonalNaive
    sf = StatsForecast(models=[AutoETS(season_length=M, model="ZNA"), SeasonalNaive(M), Naive()], freq="D",
                       n_jobs=-1)
    kq = sf.cross_validation(df=df[["unique_id", "ds", "z"]].rename(columns={"z": "y"}), h=H,
                             n_windows=SO_CUA_SO, step_size=H)
    kq = kq.rename(columns={"y": "z"})
    if luu:
        tep.parent.mkdir(parents=True, exist_ok=True)
        kq.to_parquet(tep)
    return kq


def rmsse_tung_chuoi(kq: pd.DataFrame, df: pd.DataFrame, mo_hinh: list[str]) -> pd.DataFrame:
    """RMSSE mỗi chuỗi (thang z): căn của trung bình sai số² chia trung bình bình phương bước nhảy z_t − z_{t−1}
    trên phần học trước cutoff đầu. Chuỗi có phần học phẳng bị bỏ."""
    cutoff_dau = kq["cutoff"].min()
    hoc = df[df["ds"] <= cutoff_dau]
    mau = hoc.groupby("unique_id")["z"].apply(lambda s: np.mean(np.diff(s.to_numpy()) ** 2))
    mau = mau[mau > 0]
    ra = {}
    for m in mo_hinh:
        mse = kq.assign(e2=(kq["z"] - kq[m]) ** 2).groupby("unique_id")["e2"].mean()
        ra[m] = np.sqrt(mse.loc[mau.index] / mau)
    return pd.DataFrame(ra)


def bang_so_sanh(r: pd.DataFrame, moc: str = "SeasonalNaive") -> pd.DataFrame:
    """RMSSE trung bình và tỷ lệ chuỗi thắng seasonal naive."""
    return pd.DataFrame({"RMSSE trung bình": r.mean(), "RMSSE trung vị": r.median(),
                         f"% chuỗi thắng {moc}": (r.lt(r[moc], axis=0).mean() * 100)}).sort_values("RMSSE trung bình")


# %%
if __name__ == "__main__":
    df = doc_web_traffic()
    print(df["unique_id"].nunique(), "chuỗi;", df["ds"].min().date(), "→", df["ds"].max().date())
    kq = backtest_toan_cuc(df, luu=True).merge(backtest_cuc_bo(df, luu=True).drop(columns="z"),
                                               on=["unique_id", "ds", "cutoff"])
    print(bang_so_sanh(rmsse_tung_chuoi(kq, df, ["LightGBM", "AutoETS", "SeasonalNaive", "Naive"])).round(3))
