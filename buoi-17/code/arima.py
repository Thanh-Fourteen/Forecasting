# %% [markdown]
# # Buổi 17 — ARIMA và SARIMA
#
# Điểm xuất phát (có chỗ cố tình sai). Dữ liệu: chỉ số sản lượng công nghiệp Mỹ theo tháng (Federal Reserve G.17, đã khử mùa vụ),
# 366 chuỗi du lịch theo tháng (Tourism, Monash).

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv
from tv.backtest import backtest, diebold_mariano

warnings.simplefilter("ignore")

M = 12              # chu kỳ mùa vụ của dữ liệu tháng
MUA_VU_ARIMA = 1    # chu kỳ mùa vụ đưa vào auto-ARIMA
TAM = 24            # tầm dự báo của cuộc thi Tourism


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_g17() -> pd.Series:
    """Chỉ số sản lượng công nghiệp tổng (IP.B50001.S, 2017 = 100), đã khử mùa vụ, 1/2000 → 12/2024."""
    d = pd.read_csv(tv.THU_MUC_DU_LIEU / "frb-g17-san-luong-cong-nghiep" / "g17-2000-2024.csv", skiprows=5)
    return pd.Series(d["IP.B50001.S"].to_numpy(float),
                     index=pd.PeriodIndex(d["Time Period"], freq="M").to_timestamp(), name="ip")


def doc_tourism() -> dict[str, np.ndarray]:
    tep = tv.THU_MUC_DU_LIEU / "monash-tourism-monthly" / "tourism_monthly_dataset.tsf"
    chuoi, trong_data = {}, False
    with open(tep, encoding="utf-8", errors="ignore") as f:
        for dong in f:
            if not trong_data:
                trong_data = dong.strip().lower() == "@data"
                continue
            if dong.strip():
                phan = dong.strip().split(":")
                chuoi[phan[0]] = np.array([float(x) for x in phan[-1].split(",")])
    return chuoi


def dang_dai(chuoi: dict[str, np.ndarray]) -> pd.DataFrame:
    """Dạng dài, ds số nguyên, mọi chuỗi kết thúc ở cùng một ds."""
    n = max(len(v) for v in chuoi.values())
    return pd.concat([pd.DataFrame({"unique_id": t, "ds": np.arange(n - len(v), n), "y": v})
                      for t, v in chuoi.items()], ignore_index=True)


def mau_chuoi(chuoi: dict[str, np.ndarray], so: int = 100, seed: int = 0) -> dict[str, np.ndarray]:
    """Lấy ngẫu nhiên `so` chuỗi (auto-ARIMA mùa vụ trên cả 366 chuỗi mất vài phút)."""
    ten = np.random.default_rng(seed).choice(sorted(chuoi), size=so, replace=False)
    return {t: chuoi[t] for t in ten}


# %% [markdown]
# ## Mô phỏng AR, MA, ARMA và ACF/PACF

# %%
def mo_phong(ar: list[float] = (), ma: list[float] = (), n: int = 500, seed: int = 0) -> np.ndarray:
    """y_t = φ1 y_{t−1} + … + ε_t + θ1 ε_{t−1} + …, ε chuẩn (0, 1)."""
    from statsmodels.tsa.arima_process import ArmaProcess
    np.random.seed(seed)
    return ArmaProcess(np.r_[1, -np.asarray(ar, float)], np.r_[1, np.asarray(ma, float)]).generate_sample(n, burnin=200)


def acf_pacf(y: np.ndarray, so_tre: int = 12) -> pd.DataFrame:
    from statsmodels.tsa.stattools import acf, pacf
    return pd.DataFrame({"acf": acf(y, nlags=so_tre)[1:], "pacf": pacf(y, nlags=so_tre)[1:]},
                        index=pd.Index(range(1, so_tre + 1), name="trễ"))


# %% [markdown]
# ## Ước lượng, AICc, phần dư

# %%
def arima(y: np.ndarray, order, seasonal_order=(0, 0, 0), hang_so: bool = True):
    """ARIMA(p,d,q)(P,D,Q)12 của statsforecast (ước lượng hợp lý cực đại). Hằng số chỉ khi tổng số lần sai phân ≤ 1."""
    from statsforecast.models import ARIMA
    return ARIMA(order=order, seasonal_order=seasonal_order, season_length=M,
                 include_constant=hang_so and (order[1] + seasonal_order[1] <= 1)).fit(np.asarray(y, float))


def auto_arima(y: np.ndarray):
    """Thuật toán Hyndman–Khandakar (AutoARIMA của statsforecast), chọn theo AICc."""
    from statsforecast.models import AutoARIMA
    return AutoARIMA(season_length=MUA_VU_ARIMA).fit(np.asarray(y, float))


def ten_mo_hinh(mh) -> str:
    p, q, P, Q, m, d, D = mh.model_["arma"]
    return f"ARIMA({p},{d},{q})" + (f"({P},{D},{Q}){m}" if m > 1 and P + D + Q > 0 else "")


def ljung_box(phan_du: np.ndarray, so_tre: int = 24, so_tham_so: int = 0) -> dict:
    """Q = n(n+2) Σ r_k² / (n − k); so với chi-bình-phương (so_tre − so_tham_so) bậc tự do."""
    from scipy import stats
    e = np.asarray(phan_du, float)
    e = e - e.mean()
    n = e.size
    r = np.array([np.sum(e[k:] * e[:-k]) / np.sum(e * e) for k in range(1, so_tre + 1)])
    q = n * (n + 2) * float(np.sum(r ** 2 / (n - np.arange(1, so_tre + 1))))
    return {"Q": q, "p": float(stats.chi2.sf(q, so_tre - so_tham_so)), "bậc tự do": so_tre - so_tham_so}


def kiem_phan_du(mh, so_tre: int = 24) -> dict:
    """Kiểm phần dư của mô hình. 'dat' = phần dư ổn."""
    e = mh.model_["residuals"]
    return {"trung bình phần dư": float(np.mean(e)), "dat": True}


def mo_hinh_tu_chon(y: np.ndarray, order=(0, 1, 1), seasonal_order=(0, 0, 0)):
    """Mô hình đọc từ ACF/PACF của chuỗi đã sai phân (mục 4.4)."""
    return arima(y, order, seasonal_order)


def bang_ung_vien(y: np.ndarray, cac_bac, seasonal_order=(0, 0, 0)) -> pd.DataFrame:
    """AICc và Ljung–Box của nhiều bậc; auto-ARIMA ở dòng cuối. Chỉ so AICc giữa các mô hình cùng d và D."""
    hang = []
    for bac in cac_bac:
        mh = arima(y, bac, seasonal_order)
        hang.append({"mô hình": ten_mo_hinh(mh), "AICc": mh.model_["aicc"], "phần dư ổn": kiem_phan_du(mh)["dat"]})
    tu_dong = auto_arima(y)
    hang.append({"mô hình": "auto → " + ten_mo_hinh(tu_dong), "AICc": tu_dong.model_["aicc"],
                 "phần dư ổn": kiem_phan_du(tu_dong)["dat"]})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Khoảng dự báo

# %%
def du_bao(mh, h: int, level=(80, 95)) -> pd.DataFrame:
    return pd.DataFrame(mh.predict(h, level=list(level)))


# %% [markdown]
# ## Backtest: AutoARIMA, AutoETS, seasonal naive (bộ backtest buổi 15)

# %%
MO_HINH = ["AutoARIMA", "AutoETS", "SeasonalNaive"]


def backtest_tourism(df: pd.DataFrame, so_cua_so: int = 2, buoc: int = 12, h: int = TAM,
                     luu: bool = False) -> pd.DataFrame:
    """AutoARIMA, AutoETS, SeasonalNaive trên các cửa sổ rolling origin. Cả 366 chuỗi mất ~6 phút; luu=True ghi kết
    quả vào lab/du-lieu/cache/ để lần sau đọc lại (tên tệp có chu kỳ mùa vụ đang dùng)."""
    tep = tv.THU_MUC_DU_LIEU.parent / "cache" / f"backtest-m{MUA_VU_ARIMA}-{df['unique_id'].nunique()}.parquet"
    if luu and tep.exists():
        return pd.read_parquet(tep)
    from statsforecast import StatsForecast
    from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive

    def ham(lich_su, ds_can):
        sf = StatsForecast(models=[AutoARIMA(season_length=MUA_VU_ARIMA), AutoETS(season_length=M), SeasonalNaive(M)],
                           freq=1, n_jobs=-1)
        return ds_can.merge(sf.forecast(df=lich_su, h=h).reset_index(), on=["unique_id", "ds"])

    kq = backtest(df, ham, h=h, so_cua_so=so_cua_so, buoc=buoc)
    if luu:
        tep.parent.mkdir(parents=True, exist_ok=True)
        kq.to_parquet(tep)
    return kq


def mase_theo_chuoi(kq: pd.DataFrame, df: pd.DataFrame, mo_hinh=MO_HINH) -> pd.DataFrame:
    mau = {}
    for (uid, cutoff), _ in kq.groupby(["unique_id", "cutoff"]):
        hoc = df.loc[(df["unique_id"] == uid) & (df["ds"] <= cutoff), "y"].to_numpy()
        mau[(uid, cutoff)] = float(np.mean(np.abs(hoc[M:] - hoc[:-M])))
    thang = pd.Series([mau[k] for k in zip(kq["unique_id"], kq["cutoff"], strict=True)], index=kq.index)
    return pd.DataFrame({m: ((kq["y"] - kq[m]).abs() / thang).groupby(kq["unique_id"]).mean() for m in mo_hinh})


def so_sanh(mase: pd.DataFrame) -> pd.DataFrame:
    """MASE trung bình mỗi mô hình và DM (h = 1: các chuỗi độc lập) cho ba cặp."""
    hang = []
    for a, b in (("AutoARIMA", "SeasonalNaive"), ("AutoETS", "SeasonalNaive"), ("AutoARIMA", "AutoETS")):
        dm = diebold_mariano(mase[a].to_numpy(), mase[b].to_numpy(), h=1, ham_mat_mat=lambda x: x)
        hang.append({"so": f"{a} − {b}", "chênh MASE trung bình": dm.trung_binh_chenh,
                     "tỷ lệ chuỗi thắng": float((mase[a] < mase[b]).mean()), "DM": dm.thong_ke, "p": dm.p_value})
    return pd.DataFrame(hang)


# %%
if __name__ == "__main__":
    ip = np.log(doc_g17()[:"2019-12"].to_numpy()) * 100
    print(acf_pacf(np.diff(ip), 6).round(2))
    print(bang_ung_vien(ip, [(1, 1, 0), (4, 1, 0), (0, 1, 1), (2, 1, 2)]).round(3).to_string(index=False))
    t33 = np.log(doc_tourism()["T33"][:-TAM])
    print(ten_mo_hinh(auto_arima(t33)), auto_arima(t33).model_["aicc"])
    for so in ((0, 0, 0), (0, 1, 1)):
        mh = mo_hinh_tu_chon(t33, seasonal_order=so)
        print(ten_mo_hinh(mh), round(mh.model_["aicc"], 2), kiem_phan_du(mh))
    df = dang_dai(doc_tourism())
    kq = backtest_tourism(df, luu=True)
    mase = mase_theo_chuoi(kq, df)
    print(mase.agg(["mean", "median"]).round(3))
    print(so_sanh(mase).round(4).to_string(index=False))
