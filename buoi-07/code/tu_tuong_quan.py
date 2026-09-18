# %% [markdown]
# # Buổi 7 — Tự tương quan, nhiễu trắng và tính dừng
#
# Dữ liệu: GDP thực Mỹ theo quý (BEA), chỉ số sản lượng công nghiệp theo tháng (FRB G.17),
# lượt thuê xe đạp theo giờ (UCI Bike Sharing).

# %%
from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller

import tv

MUC = 0.05


# %% [markdown]
# ## Dữ liệu

# %%
def doc_gdp() -> pd.Series:
    """GDP thực theo quý (tỷ lệ năm, triệu USD chuỗi liên hoàn), mã BEA A191RX."""
    df = pd.read_csv(tv.THU_MUC_DU_LIEU / "bea-nipa-quy" / "NipaDataQ.txt", thousands=",")
    df = df[df["%SeriesCode"] == "A191RX"]
    quy = pd.PeriodIndex(df["Period"].str.replace("Q", "Q"), freq="Q").to_timestamp()
    return pd.Series(df["Value"].astype(float).to_numpy(), index=quy, name="gdp").sort_index().asfreq("QS")


def doc_san_luong() -> pd.Series:
    """Chỉ số sản lượng công nghiệp tổng hợp theo tháng (2017 = 100), FRB G.17 mã IP.B50001.S."""
    df = pd.read_csv(tv.THU_MUC_DU_LIEU / "frb-g17-san-luong-cong-nghiep" / "g17-2000-2024.csv", skiprows=5)
    thang = pd.to_datetime(df["Time Period"] + "-01")
    return pd.Series(df["IP.B50001.S"].astype(float).to_numpy(), index=thang, name="san_luong").sort_index().asfreq("MS")


def doc_luot_thue() -> pd.Series:
    """Lượt thuê xe theo giờ trên lưới đầy đủ (giờ thiếu = NaN)."""
    h = pd.read_csv(tv.THU_MUC_DU_LIEU / "uci-bike-sharing" / "hour.csv", parse_dates=["dteday"])
    ds = h["dteday"] + pd.to_timedelta(h["hr"], unit="h")
    y = pd.Series(h["cnt"].to_numpy(dtype=float), index=ds, name="cnt")
    return y.asfreq("h")


def sinh_bon_chuoi(n: int = 500, seed: int = 42) -> dict[str, np.ndarray]:
    """Bốn chuỗi mô phỏng dùng CHUNG một dãy nhiễu: nhiễu trắng, AR(1) φ=0,7, random walk, xu hướng tất định."""
    rng = np.random.default_rng(seed)
    e = rng.normal(size=n)
    ar = np.empty(n)
    ar[0] = e[0]
    for t in range(1, n):
        ar[t] = 0.7 * ar[t - 1] + e[t]
    return {"nhiễu trắng": e, "AR(1) φ=0,7": ar, "random walk": e.cumsum(), "xu hướng 0,05t": 0.05 * np.arange(n) + e}


# %% [markdown]
# ## ACF tự viết

# %%
def acf_tu_viet(y, so_tre: int) -> np.ndarray:
    """r_0..r_so_tre theo FPP §2.8: mẫu số là tổng bình phương độ lệch trên CẢ chuỗi (không chia n−k)."""
    y = np.asarray(y, dtype=float)
    lech = y - np.nanmean(y)
    mau = np.nansum(lech**2)
    return np.array([1.0] + [np.nansum(lech[k:] * lech[:-k]) / mau for k in range(1, so_tre + 1)])


def dai_nhieu_trang(n: int) -> float:
    """Dải ±1,96/√T của FPP (statsmodels mặc định dùng dải Bartlett rộng dần theo trễ)."""
    return 1.96 / np.sqrt(n)


def ljung_box(phan_du, so_tre: int = 10, so_tham_so: int = 0) -> tuple[float, float]:
    """Q* và p-value; so_tham_so = số tham số đã ước lượng (bậc tự do = so_tre − so_tham_so)."""
    kq = acorr_ljungbox(np.asarray(phan_du, dtype=float), lags=[so_tre], model_df=so_tham_so)
    return float(kq["lb_stat"].iloc[0]), float(kq["lb_pvalue"].iloc[0])


# %% [markdown]
# ## Kiểm định nghiệm đơn vị — luôn chạy CẢ HAI

# %%
def kiem_dinh(y, co_xu_huong: bool = False) -> dict[str, float]:
    """ADF (H0: có nghiệm đơn vị)."""
    y = np.asarray(y, dtype=float)
    y = y[~np.isnan(y)]
    adf = adfuller(y, regression="c", autolag="AIC", result_object=True)
    return {"adf_stat": float(adf.statistic), "adf_p": float(adf.pvalue)}


def ket_luan(y, co_xu_huong: bool = False) -> str:
    """Kết luận dừng hay không theo ADF."""
    return "dừng" if kiem_dinh(y)["adf_p"] < MUC else "không dừng — cần sai phân"


def so_lan_sai_phan(y, toi_da: int = 2) -> int:
    """Số lần sai phân cần thiết."""
    y = pd.Series(np.asarray(y, dtype=float)).dropna().diff().dropna()  # sai phân một lần cho chắc
    for d in range(1, toi_da + 1):
        if kiem_dinh(y)["adf_p"] < MUC:
            return d
        y = y.diff().dropna()
    return toi_da


def dau_hieu_sai_phan_thua(y) -> dict[str, float]:
    """Sai phân thừa: ACF trễ 1 của chuỗi đã sai phân ≈ −0,5 và độ lệch chuẩn TĂNG."""
    y = pd.Series(np.asarray(y, dtype=float)).dropna()
    sp = y.diff().dropna()
    return {"acf1_truoc": float(acf_tu_viet(y, 1)[1]), "acf1_sau": float(acf_tu_viet(sp, 1)[1]),
            "sd_truoc": float(y.std(ddof=1)), "sd_sau": float(sp.std(ddof=1))}


def bang_bon_chuoi(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """Bảng 4 chuỗi × (ACF1, ADF/KPSS dạng 'c' và 'ct', kết luận, số lần sai phân)."""
    hang = []
    for ten, y in sinh_bon_chuoi(n, seed).items():
        c = kiem_dinh(y)
        hang.append({"chuỗi": ten, "ACF(1)": round(acf_tu_viet(y, 1)[1], 3), "ADF c": round(c["adf_p"], 3),
                     "kết luận": ket_luan(y), "d": so_lan_sai_phan(y)})
    return pd.DataFrame(hang)


# %%
if __name__ == "__main__":
    print(bang_bon_chuoi().to_string(index=False))
    gdp = np.log(doc_gdp()).diff().dropna()
    print("\nlog-sai phân GDP:", ket_luan(gdp), kiem_dinh(gdp))
    y = doc_luot_thue()
    r = acf_tu_viet(y, 168)
    print("lượt thuê: r24 =", round(r[24], 3), "r168 =", round(r[168], 3), "dải", round(dai_nhieu_trang(y.notna().sum()), 4))
    print("Ljung-Box(10) trên nhiễu trắng:", [round(v, 3) for v in ljung_box(sinh_bon_chuoi()["nhiễu trắng"], 10)])
