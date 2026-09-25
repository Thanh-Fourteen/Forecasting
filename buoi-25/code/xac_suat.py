# %% [markdown]
# # Buổi 25 — Dự báo xác suất
#
# Điểm xuất phát (có chỗ cố tình sai). Buổi này `tv` **không có** `danh_gia`: pinball, CRPS, WIS là thứ bạn tự viết.
#
# Nhu cầu điện theo giờ của ERCOT (Texas, EIA-930) 2024–2025, nhiệt độ đã dự báo trước 1 ngày (Open-Meteo, Dallas),
# nhiệt độ tối đa ngày Dallas 1940–2025 (ERA5). Dự báo 24 giờ tới; backtest học lại đầu mỗi tháng.

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

VUNG = "ERCO"
SEED = 0
MUC = (0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95)          # 9 mức quantile
THANG_DAU = pd.Timestamp("2024-07-01")                          # backtest bắt đầu sớm để có phần dư ngoài mẫu
NAM_KIEM = pd.Timestamp("2025-01-01")                           # chấm trên cả năm 2025
SO_THANG_PHAN_DU = 3                                            # phần dư ngoài mẫu của 3 tháng gần nhất
DAC_TRUNG = ["lag24", "lag48", "lag168", "gio", "thu", "nhiet"]
THAM_SO_DIEM = dict(n_estimators=400, learning_rate=0.05, num_leaves=31, min_child_samples=50, verbose=-1,
                    random_state=SEED)                          # mô hình điểm: linh hoạt, MAE tốt nhất
THAM_SO_QUANTILE = dict(n_estimators=300, learning_rate=0.03, num_leaves=15, min_child_samples=1000, verbose=-1,
                        random_state=SEED)                      # mô hình quantile: lá lớn, ít học thuộc đuôi


# %% [markdown]
# ## Dữ liệu

# %%
def _doc_eia(tep) -> pd.DataFrame:
    d = pd.read_csv(tep, usecols=["Balancing Authority", "UTC Time at End of Hour", "Demand (MW)"], dtype=str)
    d = d[d["Balancing Authority"] == VUNG]
    return pd.DataFrame({"ds": pd.to_datetime(d["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p"),
                         "y": pd.to_numeric(d["Demand (MW)"].str.replace(",", ""), errors="coerce")})


def doc_dien() -> pd.DataFrame:
    """ds (UTC, cuối giờ), y (MW, giờ trống ≤ 6 giờ liền được nội suy), nhiet (°C đã dự báo trước 24 giờ)."""
    tep = sorted(tv.THU_MUC_DU_LIEU.glob("eia930-balance-*/*.csv"))
    d = pd.concat([_doc_eia(t) for t in tep]).drop_duplicates("ds", keep="last").set_index("ds").sort_index()
    d = d.reindex(pd.date_range(d.index.min(), d.index.max(), freq="h"))
    d["y"] = d["y"].interpolate(limit=6)
    w = pd.read_csv(next(tv.THU_MUC_DU_LIEU.glob("open-meteo-du-bao-luu-erco-*/*.csv")), skiprows=3)
    w.columns = [c.split(" (")[0] for c in w.columns]
    d["nhiet"] = w.set_index(pd.to_datetime(w["time"]))["temperature_2m_previous_day1"].reindex(d.index)
    return d.rename_axis("ds").reset_index()


def doc_nhiet_do_toi_da() -> pd.Series:
    """Nhiệt độ tối đa mỗi ngày ở Dallas 1940–2025 (°C, ERA5)."""
    t = pd.read_csv(next(tv.THU_MUC_DU_LIEU.glob("open-meteo-dallas-tmax-*/*.csv")), skiprows=3)
    return pd.Series(t.iloc[:, 1].to_numpy(), index=pd.to_datetime(t["time"]), name="tmax")


# %% [markdown]
# ## Đặc trưng: dự báo 24 giờ tới, mọi số nhu cầu phải cũ hơn giờ cần đoán ít nhất 24 giờ

# %%
def dac_trung(df: pd.DataFrame, tru_muc: bool = True) -> pd.DataFrame:
    """Bảng học. `muc` = trung bình 168 giờ kết thúc 24 giờ trước giờ cần đoán; lag và nhãn đều trừ mức.

    tru_muc=False: học trên số gốc (MW) — chỉ để so sánh ở mục chẩn đoán calibration.
    """
    d = df.sort_values("ds").reset_index(drop=True)
    y = d["y"]
    muc = y.shift(24).rolling(168).mean()
    if not tru_muc:
        muc = muc * 0.0
    ra = pd.DataFrame({"ds": d["ds"], "muc": muc})
    for k in (24, 48, 168):
        ra[f"lag{k}"] = y.shift(k) - muc
    ra["gio"] = d["ds"].dt.hour
    ra["thu"] = d["ds"].dt.dayofweek
    ra["nhiet"] = d["nhiet"]
    ra["nhan"] = y - muc
    ra["y"] = y
    return ra


# %% [markdown]
# ## Backtest: học lại đầu mỗi tháng, dự báo cả tháng đó

# %%
def backtest(df: pd.DataFrame, muc=MUC, tru_muc: bool = True) -> pd.DataFrame:
    """ds, y, yhat (LightGBM bình phương), sd_trong (độ lệch chuẩn phần dư TRÊN PHẦN HỌC), q0.05 … q0.95 (thô)."""
    import lightgbm as lgb

    b = dac_trung(df, tru_muc).dropna(subset=[*DAC_TRUNG, "nhan"]).set_index("ds")
    ra = []
    for m in pd.date_range(THANG_DAU, b.index.max(), freq="MS"):
        hoc = b[b.index < m]
        kiem = b[(b.index >= m) & (b.index < m + pd.offsets.MonthBegin(1))]
        f = lgb.LGBMRegressor(**THAM_SO_DIEM).fit(hoc[DAC_TRUNG], hoc["nhan"])
        r = pd.DataFrame({"y": kiem["y"], "yhat": f.predict(kiem[DAC_TRUNG]) + kiem["muc"]}, index=kiem.index)
        r["sd_trong"] = float(np.std(hoc["nhan"] - f.predict(hoc[DAC_TRUNG])))
        for q in muc:
            g = lgb.LGBMRegressor(objective="quantile", alpha=q, **THAM_SO_QUANTILE).fit(hoc[DAC_TRUNG], hoc["nhan"])
            r[f"q{q}"] = g.predict(kiem[DAC_TRUNG]) + kiem["muc"]
        ra.append(r)
    return pd.concat(ra).rename_axis("ds").reset_index()


def ma_tran_quantile(R: pd.DataFrame, muc=MUC) -> np.ndarray:
    return R[[f"q{q}" for q in muc]].to_numpy()


def sua_crossing(Q: np.ndarray) -> np.ndarray:
    """Quantile mức cao không được nhỏ hơn quantile mức thấp."""
    return Q.copy()


def du_bao_quantile(R: pd.DataFrame, muc=MUC) -> np.ndarray:
    """9 quantile của LightGBM quantile, đã sửa crossing."""
    return sua_crossing(ma_tran_quantile(R, muc))


# %% [markdown]
# ## Khoảng từ phần dư

# %%
def quantile_tu_phan_du(R: pd.DataFrame, muc=MUC) -> np.ndarray:
    """Quantile = dự báo điểm + độ lệch chuẩn của phần dư × quantile của phân phối chuẩn."""
    from scipy.stats import norm

    return R["yhat"].to_numpy()[:, None] + R["sd_trong"].to_numpy()[:, None] * norm.ppf(np.array(muc))[None, :]


def quantile_trong_mau_chuan(R: pd.DataFrame, muc=MUC) -> np.ndarray:
    """Cách sai hay gặp: phần dư TRÊN PHẦN HỌC, giả định chuẩn — dùng để so sánh."""
    from scipy.stats import norm

    return R["yhat"].to_numpy()[:, None] + R["sd_trong"].to_numpy()[:, None] * norm.ppf(np.array(muc))[None, :]


def quantile_muon_seasonal_naive(R: pd.DataFrame, df: pd.DataFrame, muc=MUC) -> np.ndarray:
    """Cách sai thứ hai: gắn quantile sai số của seasonal naive (tuần trước) quanh dự báo LightGBM."""
    s = df.set_index("ds")["y"]
    e = R["y"].to_numpy() - s.shift(168).reindex(R["ds"]).to_numpy()
    thang = R["ds"].dt.to_period("M")
    Q = np.full((len(R), len(muc)), np.nan)
    for m in thang.unique():
        cal = ((thang < m) & (thang >= m - SO_THANG_PHAN_DU)).to_numpy()
        if cal.sum() == 0:
            continue
        dong = (thang == m).to_numpy()
        Q[dong] = R["yhat"].to_numpy()[dong, None] + np.nanquantile(e[cal], muc)[None, :]
    return Q


def mau_tu_phan_du(R: pd.DataFrame, so_mau: int = 200, seed: int = SEED) -> np.ndarray:
    """so_mau kịch bản cho mỗi giờ: dự báo điểm + phần dư ngoài mẫu rút ngẫu nhiên (3 tháng trước)."""
    rng = np.random.default_rng(seed)
    e = (R["y"] - R["yhat"]).to_numpy()
    thang = R["ds"].dt.to_period("M")
    S = np.full((len(R), so_mau), np.nan)
    for m in thang.unique():
        cal = ((thang < m) & (thang >= m - SO_THANG_PHAN_DU)).to_numpy()
        if cal.sum() == 0:
            continue
        dong = (thang == m).to_numpy()
        S[dong] = R["yhat"].to_numpy()[dong, None] + rng.choice(e[cal], size=(dong.sum(), so_mau))
    return S


# %% [markdown]
# ## Chấm dự báo xác suất (tự viết)

# %%
def pinball(y, q, tau: float) -> float:
    """Trung bình mất mát pinball: tau·(y − q) khi y ≥ q; (1 − tau)·(q − y) khi y < q."""
    u = np.asarray(y, float) - np.asarray(q, float)
    return float(np.mean(np.maximum(tau * u, (tau - 1) * u)))


def crps_mau(y, mau) -> float:
    """CRPS từ mẫu: mẫu càng gần thực tế càng tốt."""
    y = np.asarray(y, float)
    X = np.asarray(mau, float)
    return float(np.mean(np.abs(X - y[:, None]).mean(axis=1)))


def wis(y, Q: np.ndarray, muc=MUC) -> float:
    """Weighted interval score (Bracher et al. 2021): trung vị + các khoảng đối xứng (0,05–0,95, 0,1–0,9 …).

    WIS = [½·|y − trung vị| + Σ_k (α_k/2)·IS_α_k] / (K + ½), IS_α = rộng + (2/α)·phần nằm ngoài khoảng.
    """
    y = np.asarray(y, float)
    muc = list(muc)
    i_giua = muc.index(0.5)
    tong = 0.5 * np.abs(y - Q[:, i_giua])
    K = 0
    for i, a in enumerate(muc[:i_giua]):
        alpha = 2 * a
        lo, hi = Q[:, i], Q[:, len(muc) - 1 - i]
        IS = (hi - lo) + 2 / alpha * np.maximum(lo - y, 0) + 2 / alpha * np.maximum(y - hi, 0)
        tong = tong + alpha / 2 * IS
        K += 1
    return float(np.mean(tong / (K + 0.5)))


# %% [markdown]
# ## Calibration

# %%
def ty_le_duoi(y, Q: np.ndarray) -> np.ndarray:
    """Với mỗi mức: tỷ lệ giờ có thực tế ≤ quantile. Calibrate tốt thì ≈ chính mức đó."""
    return (np.asarray(y, float)[:, None] <= Q).mean(axis=0)


def coverage(y, lo, hi) -> float:
    y = np.asarray(y, float)
    return float(np.mean((y >= lo) & (y <= hi)))


def pit_tu_quantile(y, Q: np.ndarray, muc=MUC) -> tuple[np.ndarray, np.ndarray]:
    """Histogram PIT từ quantile: đếm thực tế rơi vào từng khoảng giữa hai quantile, chia cho phần kỳ vọng.

    Trả (mép các cột, mật độ tương đối); calibrate tốt thì mọi cột ≈ 1.
    """
    y = np.asarray(y, float)
    mep = np.r_[0.0, muc, 1.0]
    o = (y[:, None] > Q).sum(axis=1)                     # số quantile nằm dưới y → chỉ số cột
    dem = np.bincount(o, minlength=len(mep) - 1) / len(y)
    return mep, dem / np.diff(mep)


# %% [markdown]
# ## Đuôi: peaks-over-threshold

# %%
def cum_vuot(x: pd.Series, nguong: float, cach: int = 3) -> np.ndarray:
    """Đỉnh của từng đợt vượt ngưỡng; hai đợt phải cách nhau ít nhất `cach` ngày dưới ngưỡng."""
    dinh, dang, duoi = [], [], 0
    for v in x.to_numpy():
        if v > nguong:
            dang.append(v)
            duoi = 0
        else:
            duoi += 1
            if dang and duoi >= cach:
                dinh.append(max(dang))
                dang = []
    if dang:
        dinh.append(max(dang))
    return np.array(dinh)


def pot(x: pd.Series, nguong: float, cach: int = 3) -> dict:
    """Khớp phân phối Pareto tổng quát (GPD) cho phần vượt ngưỡng; trả xi, sigma, số đợt mỗi năm."""
    from scipy.stats import genpareto

    dinh = cum_vuot(x, nguong, cach)
    xi, _, sigma = genpareto.fit(dinh - nguong, floc=0)
    so_nam = (x.index.max() - x.index.min()).days / 365.25
    return {"nguong": nguong, "so_dot": len(dinh), "dot_moi_nam": len(dinh) / so_nam, "xi": float(xi),
            "sigma": float(sigma)}


def muc_lap_lai(kq: dict, so_nam: float) -> float:
    """Mức vượt trung bình một lần mỗi `so_nam` năm: u + σ/ξ·[(λN)^ξ − 1] (λ = số đợt mỗi năm)."""
    m = kq["dot_moi_nam"] * so_nam
    if abs(kq["xi"]) < 1e-9:
        return kq["nguong"] + kq["sigma"] * np.log(m)
    return kq["nguong"] + kq["sigma"] / kq["xi"] * (m ** kq["xi"] - 1)


# %%
if __name__ == "__main__":
    df = doc_dien()
    R = backtest(df)
    T = R["ds"] >= NAM_KIEM
    print("MAE 2025:", round(float(np.abs(R.y - R.yhat)[T].mean())))
    print("tỷ lệ dưới quantile (phần dư ngoài mẫu):", ty_le_duoi(R.y[T], quantile_tu_phan_du(R)[T.to_numpy()]).round(3))
