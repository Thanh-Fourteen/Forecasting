# %% [markdown]
# # Buổi 27 — Dự báo Bayes và Gaussian Process
#
# Phụ tùng ô tô bán chậm (Car Parts, Monash) cho partial pooling; lượt thuê xe đạp mỗi ngày (UCI Bike Sharing) cho BSTS và GP.

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv
from tv import du_lieu

warnings.simplefilter("ignore")

SEED = 0
SO_CHUOI = 300
THANG_KIEM = 12                         # 12 tháng cuối để chấm
LICH_SU = (3, 6, 12, 24)                # mỗi chuỗi chỉ được thấy chừng ấy tháng trước kỳ chấm
PRIOR = {"mu_sd": 1.0, "tau_sd": 1.0}   # log tốc độ bán trung bình ~ Normal(0, mu_sd); độ chênh giữa mã ~ HalfNormal(tau_sd)
NGUONG = {"r_hat": 1.01, "ess_bulk": 400, "divergence": 0}
NGAY_KIEM = 60                          # 60 ngày cuối của dữ liệu xe đạp
VONG_LAP = 2000                         # số mẫu mỗi chuỗi Markov cho mô hình phân cấp
TARGET_ACCEPT_GP = 0.95
THANH_PHAN_GP = ("muot", "tuan")        # thành phần kernel của GP


# %% [markdown]
# ## Dữ liệu

# %%
def doc_car_parts() -> pd.DataFrame:
    """Bảng rộng: mỗi dòng một mã phụ tùng, mỗi cột một tháng (1/1998 → 3/2002), NaN là tháng thiếu."""
    df, _ = du_lieu.doc_tsf(next(tv.THU_MUC_DU_LIEU.glob("monash-car-parts/*.tsf")))
    return df.pivot(index="unique_id", columns="ds", values="y")


def chia_car_parts(Y: pd.DataFrame, so_chuoi: int = SO_CHUOI, seed: int = SEED) -> dict:
    """300 mã đủ 36 tháng cuối; mã thứ j chỉ được thấy LICH_SU[j % 4] tháng ngay trước 12 tháng chấm."""
    rng = np.random.default_rng(seed)
    du = Y.index[Y.iloc[:, -36:].notna().all(axis=1)]
    ma = rng.choice(du, so_chuoi, replace=False)
    Y = Y.loc[ma]
    T = Y.shape[1]
    ls = np.array([LICH_SU[j % len(LICH_SU)] for j in range(so_chuoi)])
    hoc = [Y.iloc[j, T - THANG_KIEM - ls[j]:T - THANG_KIEM].to_numpy() for j in range(so_chuoi)]
    return {"ma": np.array(ma), "lich_su": ls, "hoc": hoc, "kiem": Y.iloc[:, T - THANG_KIEM:].to_numpy()}


def doc_xe_dap() -> pd.DataFrame:
    """ds, y: tổng lượt thuê mỗi ngày 2011–2012 (731 ngày)."""
    d = pd.read_csv(tv.THU_MUC_DU_LIEU / "uci-bike-sharing" / "day.csv", parse_dates=["dteday"])
    return pd.DataFrame({"ds": d["dteday"], "y": d["cnt"].astype(float)})


# %% [markdown]
# ## Poisson phân cấp: partial pooling

# %%
def mo_hinh_phan_cap(hoc: list[np.ndarray], prior: dict = PRIOR):
    """log λ_j = μ + τ·z_j (non-centered), số bán mỗi tháng ~ Poisson(λ_j)."""
    import pymc as pm

    idx = np.concatenate([np.full(len(h), j) for j, h in enumerate(hoc)])
    y = np.concatenate(hoc).astype(int)
    with pm.Model() as m:
        mu = pm.Normal("mu", 0, prior["mu_sd"])
        tau = pm.HalfNormal("tau", prior["tau_sd"])
        z = pm.Normal("z", 0, 1, shape=len(hoc))
        theta = pm.Deterministic("theta", mu + tau * z)
        pm.Poisson("y", pm.math.exp(theta[idx]), observed=y)
    return m


def tien_nghiem(mo_hinh, so_mau: int = 500, seed: int = SEED) -> np.ndarray:
    """Prior predictive: số bán một tháng mà mô hình tin là có thể xảy ra TRƯỚC khi xem dữ liệu."""
    import pymc as pm

    with mo_hinh:
        pr = pm.sample_prior_predictive(so_mau, random_seed=seed)
    return pr["prior_predictive"]["y"].values.ravel()


def lay_mau(mo_hinh, draws: int = 1000, tune: int = 1000, target_accept: float = 0.9, seed: int = SEED):
    import pymc as pm

    with mo_hinh:
        return pm.sample(draws, tune=tune, chains=4, target_accept=target_accept, random_seed=seed, progressbar=False)


def chan_doan(idata, var_names: list[str] | None = None) -> dict:
    """r_hat lớn nhất, ESS nhỏ nhất (bulk) và số divergence của một lần lấy mẫu."""
    import arviz as az

    s = az.summary(idata, var_names=var_names)
    return {"r_hat_max": float(np.nanmax(s["r_hat"].astype(float))),
            "ess_bulk_min": float(np.nanmin(s["ess_bulk"].astype(float))),
            "divergence": int(idata["sample_stats"]["diverging"].sum())}


def dung_duoc(cd: dict, nguong: dict = NGUONG) -> bool:
    """Chỉ dùng posterior khi đủ BA điều kiện: r_hat < 1,01; ESS ≥ 400; không divergence."""
    return (cd["r_hat_max"] < nguong["r_hat"] and cd["ess_bulk_min"] >= nguong["ess_bulk"]
            and cd["divergence"] <= nguong["divergence"])


def hoc_phan_cap(hoc: list[np.ndarray], prior: dict = PRIOR, seed: int = SEED):
    """Mô hình phân cấp + lấy mẫu; trả (mô hình, idata)."""
    m = mo_hinh_phan_cap(hoc, prior)
    return m, lay_mau(m, draws=VONG_LAP, tune=1000, seed=seed)


def hoc_gp(df: pd.DataFrame, thanh_phan=None, seed: int = SEED):
    """GP + lấy mẫu; trả (mô hình, idata, chẩn đoán)."""
    m = mo_hinh_gp(df, THANH_PHAN_GP if thanh_phan is None else thanh_phan)
    idata = lay_mau(m, target_accept=TARGET_ACCEPT_GP, seed=seed)
    ten = [v for v in idata["posterior"].data_vars if not v.startswith("f")]
    return m, idata, chan_doan(idata, ten)


def ba_cach_gop(hoc: list[np.ndarray], idata) -> dict[str, np.ndarray]:
    """Tốc độ bán mỗi tháng dự báo cho từng mã theo ba cách."""
    tat_ca = np.concatenate(hoc)
    lam = np.exp(idata["posterior"]["theta"]).mean(("chain", "draw")).values
    return {"khong_gop": np.array([h.mean() for h in hoc]),
            "gop_hoan_toan": np.full(len(hoc), tat_ca.mean()),
            "gop_mot_phan": lam}


def khoang_phan_cap(idata, muc: float = 0.9, seed: int = SEED) -> tuple[np.ndarray, np.ndarray]:
    """Khoảng dự báo cho số bán một tháng của từng mã: rút λ từ posterior rồi rút số bán ~ Poisson(λ)."""
    rng = np.random.default_rng(seed)
    lam = np.exp(idata["posterior"]["theta"].values.reshape(-1, idata["posterior"]["theta"].shape[-1]))
    mau = rng.poisson(lam)
    a = (1 - muc) / 2
    return np.quantile(mau, a, axis=0), np.quantile(mau, 1 - a, axis=0)


def tan_suat_dem(idata, kiem: np.ndarray, seed: int = SEED) -> pd.DataFrame:
    """Calibration cho số đếm: tỷ lệ tháng bán 0, 1, 2, ≥ 3 món mà mô hình dự báo, so với tỷ lệ thật trong 12 tháng chấm."""
    rng = np.random.default_rng(seed)
    lam = np.exp(idata["posterior"]["theta"].values.reshape(-1, idata["posterior"]["theta"].shape[-1]))
    mau = rng.poisson(lam[rng.integers(0, len(lam), 2000)])            # 2.000 kịch bản cho mỗi mã
    nhom = ["0", "1", "2", "≥ 3"]
    def ty_le(x):
        x = np.minimum(x, 3)
        return [float((x == k).mean()) for k in range(4)]
    return pd.DataFrame({"so_mon": nhom, "du_bao": ty_le(mau), "thuc": ty_le(kiem)})


def rmse(kiem: np.ndarray, lam: np.ndarray, chon=slice(None)) -> float:
    return float(np.sqrt(np.mean((kiem[chon] - lam[chon, None]) ** 2)))


# %% [markdown]
# ## Ví dụ "8 trường": centered và non-centered

# %%
Y_8, S_8 = np.array([28.0, 8, -3, 7, -1, 1, 18, 12]), np.array([15.0, 10, 16, 11, 9, 11, 10, 18])


def mo_hinh_8_truong(tham_so_hoa: str = "lech"):
    """Rubin (1981): hiệu quả luyện thi ở 8 trường. 'tam' = centered, 'lech' = non-centered."""
    import pymc as pm

    with pm.Model() as m:
        mu = pm.Normal("mu", 0, 5)
        tau = pm.HalfCauchy("tau", 5)
        if tham_so_hoa == "tam":
            theta = pm.Normal("theta", mu, tau, shape=8)
        else:
            theta = pm.Deterministic("theta", mu + tau * pm.Normal("z", 0, 1, shape=8))
        pm.Normal("y", theta, S_8, observed=Y_8)
    return m


# %% [markdown]
# ## BSTS: mức + xu hướng + mùa tuần + mùa năm (pymc-extras statespace)

# %%
def bsts(df: pd.DataFrame, draws: int = 500, seed: int = SEED):
    """Học trên log lượt thuê, trừ NGAY_KIEM ngày cuối. Trả (mô hình statespace, idata, dự báo NGAY_KIEM ngày)."""
    import pymc as pm
    from pymc_extras.statespace.models import structural as st

    hoc = df.iloc[:-NGAY_KIEM]
    y = pd.DataFrame({"y": np.log(hoc["y"].to_numpy())}, index=pd.DatetimeIndex(hoc["ds"], freq="D"))
    mo = (st.LevelTrend(order=2, innovations_order=[1, 0])
          + st.TimeSeasonality(season_length=7, innovations=False, name="tuan")
          + st.FrequencySeasonality(season_length=365.25, n=2, innovations=False, name="nam")
          + st.MeasurementError()).build(verbose=False)
    k = len(mo.state_names)
    with pm.Model(coords=mo.coords):
        pm.Normal("initial_level_trend", mu=[float(y["y"].iloc[:7].mean()), 0.0], sigma=[1.0, 0.01], dims="state_level_trend")
        pm.HalfNormal("sigma_level_trend", 0.1, dims="shock_level_trend")
        pm.Normal("params_tuan", 0, 0.5, dims="state_tuan")
        pm.Normal("params_nam", 0, 0.5, dims="state_nam")
        pm.HalfNormal("sigma_MeasurementError", 0.3)
        pm.Deterministic("P0", pm.math.eye(k), dims=("state", "state_aux"))
        mo.build_statespace_graph(y)
        idata = pm.sample(draws, tune=draws, chains=4, random_seed=seed, progressbar=False)
    du = mo.forecast(idata, start=y.index[-1], periods=NGAY_KIEM, random_seed=seed, verbose=False)
    return mo, idata, du


# %% [markdown]
# ## Gaussian process: kernel = ngôn ngữ mô tả chuỗi (xấp xỉ HSGP)

# %%
def mo_hinh_gp(df: pd.DataFrame, thanh_phan=THANH_PHAN_GP):
    """GP trên log lượt thuê đã chuẩn hoá. Thành phần:
    'muot'     Matern 5/2, độ dài ~60 ngày: xu hướng và mùa năm gộp làm một đường mượt
    'xu_huong' ExpQuad, độ dài ~200 ngày;  'nam' Periodic 365,25 ngày;  'tuan' Periodic 7 ngày.
    Nhiễu Student-t (chịu được ngày bão, ngày lễ)."""
    import pymc as pm

    hoc = np.log(df["y"].to_numpy()[:-NGAY_KIEM])
    tb, dlc = hoc.mean(), hoc.std()
    t = np.arange(len(hoc), dtype=float)[:, None]
    with pm.Model() as m:
        X = pm.Data("X", t)
        f = 0
        if "muot" in thanh_phan:
            ls = pm.InverseGamma("ls_muot", alpha=5, beta=5 * 60)
            eta = pm.HalfNormal("eta_muot", 1)
            f = f + pm.gp.HSGP(m=[40], c=1.5, cov_func=eta ** 2 * pm.gp.cov.Matern52(1, ls=ls)).prior("f_muot", X=X)
        if "xu_huong" in thanh_phan:
            ls = pm.InverseGamma("ls_xu_huong", alpha=5, beta=5 * 200)
            eta = pm.HalfNormal("eta_xu_huong", 1)
            f = f + pm.gp.HSGP(m=[30], c=1.5, cov_func=eta ** 2 * pm.gp.cov.ExpQuad(1, ls=ls)).prior("f_xu_huong", X=X)
        if "nam" in thanh_phan:
            eta = pm.HalfNormal("eta_nam", 1)
            ls = pm.HalfNormal("ls_nam", 1)
            f = f + pm.gp.HSGPPeriodic(m=10, scale=eta, cov_func=pm.gp.cov.Periodic(1, period=365.25, ls=ls)).prior("f_nam", X=X)
        if "tuan" in thanh_phan:
            eta = pm.HalfNormal("eta_tuan", 0.5)
            f = f + pm.gp.HSGPPeriodic(m=4, scale=eta, cov_func=pm.gp.cov.Periodic(1, period=7, ls=1.0)).prior("f_tuan", X=X)
        f = pm.Deterministic("f", f)
        sigma = pm.HalfNormal("sigma", 0.5)
        pm.StudentT("obs", nu=4, mu=f, sigma=sigma, observed=(hoc - tb) / dlc)
    m.chuan_hoa = (tb, dlc)
    return m


def du_bao_gp(m, idata, so_ngay: int = NGAY_KIEM, muc: float = 0.9, seed: int = SEED) -> pd.DataFrame:
    """Rút f ở các ngày tương lai, cộng nhiễu Student-t, đổi về lượt thuê. Trả trung vị và khoảng `muc`."""
    import pymc as pm

    rng = np.random.default_rng(seed)
    n = m["X"].get_value().shape[0]
    with m:
        pm.set_data({"X": np.arange(n, n + so_ngay, dtype=float)[:, None]})
        f = pm.sample_posterior_predictive(idata, var_names=["f"], random_seed=seed, progressbar=False)
        pm.set_data({"X": np.arange(n, dtype=float)[:, None]})
    fm = f["posterior_predictive"]["f"].values.reshape(-1, so_ngay)
    sig = idata["posterior"]["sigma"].values.reshape(-1, 1)
    z = fm + sig * rng.standard_t(4, size=fm.shape)
    tb, dlc = m.chuan_hoa
    mau = np.exp(z * dlc + tb)
    a = (1 - muc) / 2
    return pd.DataFrame({"giua": np.median(mau, 0), "lo": np.quantile(mau, a, 0), "hi": np.quantile(mau, 1 - a, 0)})


def ets(df: pd.DataFrame, muc: int = 90) -> pd.DataFrame:
    """AutoETS mùa 7 trên log lượt thuê — mốc so sánh; khoảng từ mô hình."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS

    hoc = df.iloc[:-NGAY_KIEM]
    d = pd.DataFrame({"unique_id": "xe", "ds": hoc["ds"], "y": np.log(hoc["y"].to_numpy())})
    f = StatsForecast(models=[AutoETS(season_length=7)], freq="D").forecast(df=d, h=NGAY_KIEM, level=[muc])
    return pd.DataFrame({"giua": np.exp(f["AutoETS"].to_numpy()), "lo": np.exp(f[f"AutoETS-lo-{muc}"].to_numpy()),
                         "hi": np.exp(f[f"AutoETS-hi-{muc}"].to_numpy())})


def cham_ngay(df: pd.DataFrame, du: pd.DataFrame) -> dict:
    y = df["y"].to_numpy()[-NGAY_KIEM:]
    return {"mae": float(np.mean(np.abs(y - du["giua"].to_numpy()))),
            "coverage_90": float(np.mean((y >= du["lo"].to_numpy()) & (y <= du["hi"].to_numpy())))}
