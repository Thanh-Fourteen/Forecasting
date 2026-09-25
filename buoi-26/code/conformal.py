# %% [markdown]
# # Buổi 26 — Conformal prediction cho chuỗi thời gian
#
# Điểm xuất phát (có chỗ cố tình sai).
#
# PM2.5 theo giờ ở trạm Dongsi (Bắc Kinh, UCI Beijing Multi-Site Air-Quality) 3/2013 → 2/2017. Dự báo giờ tới.
# Năm 1 để học mô hình, năm 2 để hiệu chỉnh (calibration), hai năm cuối để kiểm.

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

TRAM = "Dongsi"
SEED = 0
ALPHA = 0.1                                   # khoảng 90%
HOC_DEN = pd.Timestamp("2014-03-01")          # học: 3/2013 → 2/2014
HIEU_CHINH_DEN = pd.Timestamp("2015-03-01")   # hiệu chỉnh: 3/2014 → 2/2015; kiểm: 3/2015 → 2/2017
CUA_30_NGAY = 720                             # số giờ của cửa sổ coverage trượt
PHUONG_PHAP = "split"                         # cách tính khoảng đem dùng thật (khoang_trien_khai)
GAMMA = 0.005                                 # bước của ACI: giá trị Gibbs & Candès dùng, định TRƯỚC khi nhìn đoạn kiểm
DAC_TRUNG = ["lag1", "lag2", "lag3", "lag24", "TEMP", "DEWP", "PRES", "WSPM", "RAIN", "huong", "gio"]
THAM_SO = dict(n_estimators=300, learning_rate=0.03, num_leaves=15, min_child_samples=300, verbose=-1,
               random_state=SEED)


# %% [markdown]
# ## Dữ liệu và đặc trưng (dự báo giờ tới: chỉ dùng số tới giờ trước)

# %%
def doc_pm25(tram: str = TRAM) -> pd.DataFrame:
    """ds (giờ Bắc Kinh), y (PM2.5, µg/m³; giờ trống ≤ 3 giờ liền được nội suy), thời tiết đo tại trạm."""
    tep = next(tv.THU_MUC_DU_LIEU.glob(f"uci-beijing-air/*/PRSA_Data_{tram}_*.csv"))
    d = pd.read_csv(tep)
    ra = pd.DataFrame({"ds": pd.to_datetime(d[["year", "month", "day", "hour"]]),
                       "y": d["PM2.5"].interpolate(limit=3, limit_area="inside")})
    for c in ("TEMP", "DEWP", "PRES", "WSPM", "RAIN"):
        ra[c] = d[c].interpolate(limit=3, limit_area="inside")
    ra["huong"] = d["wd"].astype("category").cat.codes
    return ra


def dac_trung(df: pd.DataFrame) -> pd.DataFrame:
    """Mỗi dòng là một giờ cần đoán; lag k = PM2.5 của k giờ trước; thời tiết lấy ở giờ trước (đã đo)."""
    d = df.sort_values("ds").reset_index(drop=True)
    ra = pd.DataFrame({"ds": d["ds"], "y": d["y"]})
    for k in (1, 2, 3, 24):
        ra[f"lag{k}"] = d["y"].shift(k)
    for c in ("TEMP", "DEWP", "PRES", "WSPM", "RAIN", "huong"):
        ra[c] = d[c].shift(1)
    ra["gio"] = d["ds"].dt.hour
    return ra


# %% [markdown]
# ## Mô hình: LightGBM học bước nhảy (y − lag1), chỉ trên năm 1

# %%
def du_bao(df: pd.DataFrame) -> pd.DataFrame:
    """ds, y, yhat (điểm), q_lo, q_hi (quantile 5% và 95% cho CQR) — cho năm hiệu chỉnh và hai năm kiểm."""
    import lightgbm as lgb

    b = dac_trung(df).dropna().reset_index(drop=True)
    hoc = b[b["ds"] < HOC_DEN]
    sau = b[b["ds"] >= HOC_DEN].copy()
    nhan = hoc["y"] - hoc["lag1"]
    f = lgb.LGBMRegressor(**THAM_SO).fit(hoc[DAC_TRUNG], nhan)
    sau["yhat"] = f.predict(sau[DAC_TRUNG]) + sau["lag1"]
    for ten, a in (("q_lo", ALPHA / 2), ("q_hi", 1 - ALPHA / 2)):
        g = lgb.LGBMRegressor(objective="quantile", alpha=a, **THAM_SO).fit(hoc[DAC_TRUNG], nhan)
        sau[ten] = g.predict(sau[DAC_TRUNG]) + sau["lag1"]
    sau["giai_doan"] = np.where(sau["ds"] < HIEU_CHINH_DEN, "hieu_chinh", "kiem")
    return sau[["ds", "giai_doan", "y", "lag1", "yhat", "q_lo", "q_hi"]].reset_index(drop=True)


# %% [markdown]
# ## Split conformal và CQR

# %%
def quantile_conformal(diem: np.ndarray, alpha: float = ALPHA) -> float:
    """Điểm thứ ⌈(n + 1)(1 − α)⌉ khi xếp tăng dần (quá n thì vô hạn)."""
    diem = np.sort(np.asarray(diem, float))
    k = int(np.ceil((len(diem) + 1) * (1 - alpha)))
    return np.inf if k > len(diem) else float(diem[k - 1])


def split_conformal(P: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame:
    """Khoảng yhat ± q, q tính MỘT LẦN từ |sai số| của năm hiệu chỉnh."""
    hc = P["giai_doan"] == "hieu_chinh"
    q = quantile_conformal(np.abs(P.loc[hc, "y"] - P.loc[hc, "yhat"]), alpha)
    return pd.DataFrame({"ds": P["ds"], "lo": P["yhat"] - q, "hi": P["yhat"] + q})


def cqr(P: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame:
    """Conformalized quantile regression: nới (hoặc co) khoảng quantile [q_lo, q_hi] một lượng q từ năm hiệu chỉnh."""
    hc = P["giai_doan"] == "hieu_chinh"
    diem = np.maximum(P.loc[hc, "q_lo"] - P.loc[hc, "y"], P.loc[hc, "y"] - P.loc[hc, "q_hi"])
    q = quantile_conformal(diem, alpha)
    return pd.DataFrame({"ds": P["ds"], "lo": P["q_lo"] - q, "hi": P["q_hi"] + q})


# %% [markdown]
# ## ACI: chỉnh mức α sau mỗi giờ theo lỗi vừa mắc

# %%
def aci(P: pd.DataFrame, alpha: float = ALPHA, gamma: float = GAMMA) -> pd.DataFrame:
    """Adaptive conformal inference (Gibbs & Candès 2021) trên điểm |y − yhat|.

    Bắt đầu với các điểm của năm hiệu chỉnh. Mỗi giờ kiểm: khoảng = yhat ± quantile mức (1 − α_t) của mọi điểm đã
    biết; xem thực tế rồi cập nhật α_{t+1} = α_t + γ·(α − lỗi_t) (lỗi_t = 1 nếu thực tế nằm ngoài khoảng) và thêm
    điểm mới vào tập. α_t ≤ 0 → khoảng vô hạn.
    """
    hc = (P["giai_doan"] == "hieu_chinh").to_numpy()
    diem = list(np.abs(P["y"] - P["yhat"]).to_numpy()[hc])
    yhat, y = P["yhat"].to_numpy(), P["y"].to_numpy()
    lo, hi, a_t = np.full(len(P), np.nan), np.full(len(P), np.nan), alpha
    at = np.full(len(P), np.nan)
    for i in np.flatnonzero(~hc):
        q = np.inf if a_t <= 0 else (0.0 if a_t >= 1 else quantile_conformal(diem, a_t))
        lo[i], hi[i], at[i] = yhat[i] - q, yhat[i] + q, a_t
        loi = float(not (lo[i] <= y[i] <= hi[i]))
        a_t = a_t - gamma * (alpha - loi)
        diem.append(abs(y[i] - yhat[i]))
    return pd.DataFrame({"ds": P["ds"], "lo": lo, "hi": hi, "alpha_t": at})


# %% [markdown]
# ## EnbPI: ensemble bootstrap, phần dư ngoài túi, cửa sổ phần dư trượt

# %%
def enbpi(df: pd.DataFrame, alpha: float = ALPHA, so_mo_hinh: int = 20, khoi: int = 24,
          cua: int | None = None) -> pd.DataFrame:
    """EnbPI (Xu & Xie 2021). Học so_mo_hinh LightGBM trên mẫu bootstrap theo khối 24 giờ của năm 1 + năm 2.

    Phần dư của mỗi giờ học chỉ lấy từ các mô hình KHÔNG thấy giờ đó (ngoài túi). Khoảng giờ kiểm = trung bình
    ensemble ± quantile (1 − α) của `cua` phần dư gần nhất; sau mỗi giờ bỏ phần dư cũ nhất, thêm phần dư mới.
    cua=None: giữ đủ một năm (8.760 giờ) như bài gốc giữ đúng số phần dư ban đầu.
    """
    import lightgbm as lgb

    b = dac_trung(df).dropna().reset_index(drop=True)
    hoc = b[b["ds"] < HIEU_CHINH_DEN].reset_index(drop=True)
    kiem = b[b["ds"] >= HIEU_CHINH_DEN].reset_index(drop=True)
    rng = np.random.default_rng(SEED)
    n, so_khoi = len(hoc), len(hoc) // khoi
    trong_tui = np.zeros((so_mo_hinh, n), bool)
    du_hoc, du_kiem = np.zeros((so_mo_hinh, n)), np.zeros((so_mo_hinh, len(kiem)))
    for m in range(so_mo_hinh):
        k = rng.integers(0, so_khoi, so_khoi)
        idx = (k[:, None] * khoi + np.arange(khoi)).ravel()
        f = lgb.LGBMRegressor(**{**THAM_SO, "n_estimators": 150}).fit(
            hoc[DAC_TRUNG].iloc[idx], hoc["y"].iloc[idx] - hoc["lag1"].iloc[idx])
        trong_tui[m, np.unique(idx)] = True
        du_hoc[m] = f.predict(hoc[DAC_TRUNG]) + hoc["lag1"]
        du_kiem[m] = f.predict(kiem[DAC_TRUNG]) + kiem["lag1"]
    ngoai = ~trong_tui
    co = ngoai.any(axis=0)
    loo = np.where(ngoai, du_hoc, np.nan)[:, co]
    phan_du = list(np.abs(hoc["y"].to_numpy()[co] - np.nanmean(loo, axis=0)))
    cua = cua or 8760
    phan_du = phan_du[-cua:]
    f_kiem = du_kiem.mean(axis=0)
    y = kiem["y"].to_numpy()
    lo, hi = np.empty(len(kiem)), np.empty(len(kiem))
    for i in range(len(kiem)):
        q = float(np.quantile(phan_du, 1 - alpha))
        lo[i], hi[i] = f_kiem[i] - q, f_kiem[i] + q
        phan_du.pop(0)
        phan_du.append(abs(y[i] - f_kiem[i]))
    return pd.DataFrame({"ds": kiem["ds"], "yhat": f_kiem, "lo": lo, "hi": hi})


def khoang_trien_khai(P: pd.DataFrame) -> pd.DataFrame:
    """Khoảng 90% đem dùng cho hai năm kiểm, theo PHUONG_PHAP."""
    return {"split": split_conformal, "cqr": cqr, "aci": aci}[PHUONG_PHAP](P)


# %% [markdown]
# ## Thư viện: MAPIE

# %%
def mapie_aci(df: pd.DataFrame, den: str = "2015-09-01", gamma: float = GAMMA, alpha: float = ALPHA) -> pd.DataFrame:
    """ACI của MAPIE (TimeSeriesRegressor) từ đầu đoạn kiểm tới `den`, cập nhật mỗi 24 giờ — để so với bản tự viết."""
    import lightgbm as lgb
    from mapie.regression import TimeSeriesRegressor
    from mapie.subsample import BlockBootstrap

    b = dac_trung(df).dropna().reset_index(drop=True)
    hoc = b[b["ds"] < HIEU_CHINH_DEN]
    kiem = b[(b["ds"] >= HIEU_CHINH_DEN) & (b["ds"] < den)].reset_index(drop=True)
    mp = TimeSeriesRegressor(lgb.LGBMRegressor(**{**THAM_SO, "n_estimators": 150}), method="aci",
                             cv=BlockBootstrap(n_resamplings=10, length=24 * 7, overlapping=False, random_state=SEED),
                             agg_function="mean", n_jobs=1)
    mp.fit(hoc[DAC_TRUNG].to_numpy(), (hoc["y"] - hoc["lag1"]).to_numpy())
    X, nhan = kiem[DAC_TRUNG].to_numpy(), (kiem["y"] - kiem["lag1"]).to_numpy()
    lo, hi, buoc = np.empty(len(kiem)), np.empty(len(kiem)), 24
    for st in range(0, len(kiem), buoc):
        if st:
            mp.update(X[st - buoc:st], nhan[st - buoc:st])
            mp.adapt_conformal_inference(X[st - buoc:st], nhan[st - buoc:st], gamma=gamma)
        _, pis = mp.predict(X[st:st + buoc], confidence_level=1 - alpha, ensemble=True, allow_infinite_bounds=True)
        lo[st:st + buoc], hi[st:st + buoc] = pis[:, 0, 0], pis[:, 1, 0]
    return pd.DataFrame({"ds": kiem["ds"], "y": kiem["y"], "lo": lo + kiem["lag1"], "hi": hi + kiem["lag1"]})


# %% [markdown]
# ## Đo coverage theo thời gian

# %%
def coverage_truot(y, lo, hi, cua: int = CUA_30_NGAY) -> pd.Series:
    """Tỷ lệ giờ thực tế nằm trong khoảng, tính trên `cua` giờ gần nhất."""
    y = pd.Series(np.asarray(y, float))
    trong = ((y >= np.asarray(lo, float)) & (y <= np.asarray(hi, float))).astype(float)
    return trong.rolling(cua).mean()


def tom_tat(y, lo, hi) -> dict:
    c = coverage_truot(y, lo, hi).dropna()
    rong = np.asarray(hi, float) - np.asarray(lo, float)
    return {"coverage": float(np.mean((np.asarray(y) >= lo) & (np.asarray(y) <= hi))),
            "min_30_ngay": float(c.min()), "max_30_ngay": float(c.max()),
            "ngoai_85_95": float(((c < 0.85) | (c > 0.95)).mean()),
            "rong_trung_vi": float(np.median(rong[np.isfinite(rong)])), "gio_vo_han": int((~np.isfinite(rong)).sum())}


# %%
if __name__ == "__main__":
    df = doc_pm25()
    P = du_bao(df)
    k = P["giai_doan"] == "kiem"
    y = P.loc[k, "y"]
    print("split", tom_tat(y, *[split_conformal(P).loc[k, c] for c in ("lo", "hi")]))
    print("aci", tom_tat(y, *[aci(P).loc[k, c] for c in ("lo", "hi")]))
