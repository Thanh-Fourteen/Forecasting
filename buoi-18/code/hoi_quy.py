# %% [markdown]
# # Buổi 18 — Hồi quy chuỗi thời gian và hồi quy động
#
# Điểm xuất phát (có chỗ cố tình sai). Dữ liệu: hành khách hàng không EU (Eurostat) và sản lượng công nghiệp Mỹ (G.17) theo tháng; tải điện ERCOT theo giờ 2024 (EIA-930)
# với nhiệt độ Dallas thật và đã dự báo trước 1 ngày (Open-Meteo); lượt xem Wikipedia tiếng Việt theo ngày.

# %%
from __future__ import annotations

import json
import logging
import warnings

import numpy as np
import pandas as pd

import tv
from tv.backtest import backtest

warnings.simplefilter("ignore")
logging.getLogger("cmdstanpy").disabled = True

H = 24                      # dự báo tải cho 24 giờ tới
HOC = 24 * 56               # học trên 8 tuần gần nhất (sliding window)
SO_CUA_SO = 24              # 24 cutoff từ 1/2024 tới 12/2024
BUOC = 24 * 13              # 13 ngày: cutoff xoay vòng qua mọi thứ trong tuần (bẫy của buổi 15)
MUC_CDD = 18.0              # °C: trên mức này bật điều hoà, dưới thì bật sưởi
CUOI_DIEN = "2024-12-31 06:00"  # nửa đêm giờ Texas; tệp nhiệt độ dự báo chỉ tới hết 2024 (UTC)
MO_HINH_DIEN = ["SN24", "SN168", "OLS", "DHR", "MSTL", "TBATS", "Prophet"]


# %% [markdown]
# ## 1. Hồi quy giả: hành khách EU ~ sản lượng công nghiệp Mỹ

# %%
def doc_hanh_khach() -> pd.Series:
    """Hành khách hàng không EU27 theo tháng (triệu)."""
    d = pd.read_csv(tv.THU_MUC_DU_LIEU / "eurostat-hanh-khach-hang-khong" / "eurostat-avia-paoc-eu27.csv")
    return pd.Series(d["OBS_VALUE"].to_numpy(float) / 1e6,
                     index=pd.PeriodIndex(d["TIME_PERIOD"], freq="M").to_timestamp(), name="hanh_khach")


def doc_g17() -> pd.Series:
    """Chỉ số sản lượng công nghiệp Mỹ (2017 = 100), đã khử mùa vụ."""
    d = pd.read_csv(tv.THU_MUC_DU_LIEU / "frb-g17-san-luong-cong-nghiep" / "g17-2000-2024.csv", skiprows=5)
    return pd.Series(d["IP.B50001.S"].to_numpy(float),
                     index=pd.PeriodIndex(d["Time Period"], freq="M").to_timestamp(), name="ip")


def cap_gia(tu: str = "2010", den: str = "2019") -> tuple[pd.Series, pd.DataFrame]:
    """y = hành khách; X = sản lượng công nghiệp + 11 biến giả tháng (tháng 1 là mốc)."""
    y = doc_hanh_khach()[tu:den]
    gia = pd.get_dummies(y.index.month, prefix="thang", drop_first=True).astype(float)
    gia.index = y.index
    return y, pd.concat([doc_g17()[tu:den], gia], axis=1)


def ljung_box_p(phan_du, so_tre: int = 24) -> float:
    from statsmodels.stats.diagnostic import acorr_ljungbox
    return float(acorr_ljungbox(np.asarray(phan_du, float), lags=[so_tre])["lb_pvalue"].iloc[0])


def hoi_quy_ols(y: pd.Series, X: pd.DataFrame) -> dict:
    """Hồi quy thường (bình phương nhỏ nhất). Sai số chuẩn, p-value giả định phần dư không tự tương quan."""
    import statsmodels.api as sm
    kq = sm.OLS(y, sm.add_constant(X)).fit()
    e = kq.resid.to_numpy()
    return {"hệ số ip": float(kq.params["ip"]), "p": float(kq.pvalues["ip"]), "R2": float(kq.rsquared),
            "ACF trễ 1 phần dư": float(np.corrcoef(e[1:], e[:-1])[0, 1]), "Ljung-Box p": ljung_box_p(e)}


def he_so_ip(y: pd.Series, X: pd.DataFrame) -> dict:
    """Hệ số của sản lượng công nghiệp, p-value và kiểm phần dư."""
    import statsmodels.api as sm
    kq = sm.OLS(y, sm.add_constant(X)).fit()
    return {"hệ số ip": float(kq.params["ip"]), "p": float(kq.pvalues["ip"]), "Ljung-Box p": ljung_box_p(kq.resid)}


def mo_phong_hoi_quy_gia(so_lan: int = 1000, n: int = 120, seed: int = 0) -> dict:
    """Hai bước ngẫu nhiên ĐỘC LẬP: tỷ lệ lần hồi quy thường cho p < 0,05 (trên mức và trên sai phân)."""
    import statsmodels.api as sm
    rng = np.random.default_rng(seed)
    muc = sai_phan = 0
    for _ in range(so_lan):
        a, b = rng.normal(size=n).cumsum(), rng.normal(size=n).cumsum()
        muc += sm.OLS(a, sm.add_constant(b)).fit().pvalues[1] < 0.05
        sai_phan += sm.OLS(np.diff(a), sm.add_constant(np.diff(b))).fit().pvalues[1] < 0.05
    return {"trên mức": muc / so_lan, "trên sai phân": sai_phan / so_lan}


# %% [markdown]
# ## 2. Tải điện ERCOT: nhiệt độ, Fourier, lễ

# %%
def doc_dien(ba: str = "ERCO") -> pd.Series:
    """Tải điện theo giờ 2024 (MW), mốc UTC cuối giờ, lỗ ≤ 3 giờ nội suy."""
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


def doc_nhiet() -> pd.DataFrame:
    """Nhiệt độ Dallas theo giờ (°C, UTC): `that` = đo sau (chỉ biết khi giờ đó đã qua), `du_bao` = dự báo ra từ hôm trước."""
    d = pd.read_csv(tv.THU_MUC_DU_LIEU / "open-meteo-dallas-du-bao-luu-2024" / "open-meteo-dallas-du-bao-luu-2024.csv",
                    skiprows=2)
    return pd.DataFrame({"that": d["temperature_2m (°C)"].to_numpy(),
                         "du_bao": d["temperature_2m_previous_day1 (°C)"].to_numpy()},
                        index=pd.to_datetime(d["time"]))


def fourier(moc: pd.DatetimeIndex, chu_ky: int, K: int) -> pd.DataFrame:
    """K cặp sin/cos cho chu kỳ `chu_ky` giờ."""
    t = ((moc - pd.Timestamp("2024-01-01")) / pd.Timedelta(hours=1)).to_numpy()
    return pd.DataFrame({f"{f}{chu_ky}_{k}": g(2 * np.pi * k * t / chu_ky)
                         for k in range(1, K + 1) for f, g in (("sin", np.sin), ("cos", np.cos))}, index=moc)


def ngay_le_my(moc: pd.DatetimeIndex) -> np.ndarray:
    """1 nếu giờ đó (giờ Texas ≈ UTC − 6) rơi vào ngày lễ liên bang Mỹ."""
    import holidays
    le = holidays.US(years=2024)
    return np.array([(m - pd.Timedelta(hours=6)).date() in le for m in moc], float)


def bien_giai_thich(moc: pd.DatetimeIndex, nhiet: pd.Series, K24: int = 10, K168: int = 6) -> pd.DataFrame:
    """Fourier ngày + tuần, CDD/HDD và bình phương của chúng (tải tăng nhanh dần khi nóng/lạnh), biến giả lễ."""
    T = nhiet.reindex(moc).to_numpy()
    cdd, hdd = np.maximum(T - MUC_CDD, 0), np.maximum(MUC_CDD - T, 0)
    return pd.concat([fourier(moc, 24, K24), fourier(moc, 168, K168),
                      pd.DataFrame({"cdd": cdd, "hdd": hdd, "cdd2": cdd ** 2, "hdd2": hdd ** 2,
                                    "le": ngay_le_my(moc)}, index=moc)], axis=1)


def _cot_dung(X: pd.DataFrame) -> pd.Index:
    """Bỏ cột hằng (ví dụ biến lễ toàn 0 trong 8 tuần không có lễ) — cột hằng làm hồi quy không giải được."""
    return X.columns[X.std() > 0]


def du_bao_dhr(lich_su: pd.DataFrame, ds_can: pd.DataFrame, nhiet: pd.DataFrame | None = None,
               K24: int = 10, K168: int = 6) -> pd.DataFrame:
    """Hồi quy động: y ~ Fourier + nhiệt độ + lễ, sai số ARIMA (AutoARIMA chọn bậc). Học trên nhiệt độ THẬT của quá khứ;
    dự báo bằng nhiệt độ ĐÃ DỰ BÁO từ hôm trước — thứ duy nhất có trong tay lúc ra dự báo."""
    from statsforecast.models import AutoARIMA
    nhiet = doc_nhiet() if nhiet is None else nhiet
    Xh = bien_giai_thich(pd.DatetimeIndex(lich_su["ds"]), nhiet["that"], K24, K168)
    Xf = bien_giai_thich(pd.DatetimeIndex(ds_can["ds"]), nhiet["du_bao"], K24, K168)
    cot = _cot_dung(Xh)
    mh = AutoARIMA(season_length=1).fit(lich_su["y"].to_numpy(), X=Xh[cot].to_numpy())
    return ds_can.assign(DHR=mh.predict(len(ds_can), X=Xf[cot].to_numpy())["mean"])


def du_bao_ols(lich_su: pd.DataFrame, ds_can: pd.DataFrame, nhiet: pd.DataFrame | None = None) -> pd.DataFrame:
    """Cùng biến giải thích nhưng sai số coi như độc lập (hồi quy thường)."""
    import statsmodels.api as sm
    nhiet = doc_nhiet() if nhiet is None else nhiet
    Xh = bien_giai_thich(pd.DatetimeIndex(lich_su["ds"]), nhiet["that"])
    Xf = bien_giai_thich(pd.DatetimeIndex(ds_can["ds"]), nhiet["du_bao"])
    cot = _cot_dung(Xh)
    kq = sm.OLS(lich_su["y"].to_numpy(), sm.add_constant(Xh[cot].to_numpy())).fit()
    return ds_can.assign(OLS=kq.predict(sm.add_constant(Xf[cot].to_numpy(), has_constant="add")))


def du_bao_khac(lich_su: pd.DataFrame, ds_can: pd.DataFrame, cac: tuple = ("SN24", "SN168", "MSTL", "TBATS", "Prophet")
                ) -> pd.DataFrame:
    """Các cách không dùng nhiệt độ: seasonal naive 24 và 168 giờ, MSTL + ETS, TBATS, Prophet mặc định."""
    y = lich_su["y"].to_numpy()
    h = len(ds_can)
    ra = ds_can.copy()
    if "SN24" in cac:
        ra["SN24"] = np.resize(y[-24:], h)
    if "SN168" in cac:
        ra["SN168"] = y[-168:][:h]
    if "MSTL" in cac:
        from statsforecast.models import MSTL, AutoETS
        ra["MSTL"] = MSTL([24, 168], trend_forecaster=AutoETS(model="ZZN")).fit(y).predict(h)["mean"]
    if "TBATS" in cac:
        from statsforecast.models import AutoTBATS
        ra["TBATS"] = AutoTBATS([24, 168]).fit(y).predict(h)["mean"]
    if "Prophet" in cac:
        from prophet import Prophet
        mh = Prophet().fit(lich_su[["ds", "y"]])
        ra["Prophet"] = mh.predict(ds_can[["ds"]])["yhat"].to_numpy()
    return ra


def backtest_dien(so_cua_so: int = SO_CUA_SO, cac: tuple = tuple(MO_HINH_DIEN), luu: bool = False) -> pd.DataFrame:
    """Mọi cách trên cùng các cửa sổ: học 8 tuần gần nhất, dự báo 24 giờ tới, cutoff cách nhau 13 ngày (bộ backtest buổi 15).
    24 cửa sổ mất ~5 phút (TBATS chiếm phần lớn); luu=True ghi kết quả vào lab/du-lieu/cache/."""
    tep = tv.THU_MUC_DU_LIEU.parent / "cache" / f"backtest-dien-{so_cua_so}-{'-'.join(cac)}.parquet"
    if luu and tep.exists():
        return pd.read_parquet(tep)
    y = doc_dien()[:CUOI_DIEN]
    df = pd.DataFrame({"unique_id": "ERCO", "ds": y.index, "y": y.to_numpy()})
    nhiet = doc_nhiet()

    def ham(lich_su, ds_can):
        ra = du_bao_khac(lich_su, ds_can, tuple(c for c in cac if c not in ("OLS", "DHR")))
        if "OLS" in cac:
            ra = ra.merge(du_bao_ols(lich_su, ds_can, nhiet), on=["unique_id", "ds"])
        if "DHR" in cac:
            ra = ra.merge(du_bao_dhr(lich_su, ds_can, nhiet), on=["unique_id", "ds"])
        return ra

    kq = backtest(df, ham, h=H, so_cua_so=so_cua_so, buoc=BUOC, cua_so_train=HOC)
    if luu:
        tep.parent.mkdir(parents=True, exist_ok=True)
        kq.to_parquet(tep)
    return kq


def mae_theo_cua_so(kq: pd.DataFrame, cac=None) -> pd.DataFrame:
    cac = [c for c in (cac or MO_HINH_DIEN) if c in kq.columns]
    return pd.DataFrame({c: (kq["y"] - kq[c]).abs().groupby(kq["cutoff"]).mean() for c in cac})


def chon_K(lich_su: pd.DataFrame, cac_K=((2, 2), (4, 2), (6, 4), (10, 6)), nhiet: pd.DataFrame | None = None) -> pd.DataFrame:
    """AICc của hồi quy động với các số cặp Fourier khác nhau (FPP §10.5: chọn K bằng AICc)."""
    from statsforecast.models import AutoARIMA
    nhiet = doc_nhiet() if nhiet is None else nhiet
    hang = []
    for K24, K168 in cac_K:
        X = bien_giai_thich(pd.DatetimeIndex(lich_su["ds"]), nhiet["that"], K24, K168)
        mh = AutoARIMA(season_length=1).fit(lich_su["y"].to_numpy(), X=X[_cot_dung(X)].to_numpy())
        hang.append({"K ngày": K24, "K tuần": K168, "AICc": mh.model_["aicc"]})
    return pd.DataFrame(hang)


# %% [markdown]
# ## 3. Prophet và Tết: lượt xem Wikipedia tiếng Việt

# %%
def doc_wiki() -> pd.Series:
    """Tổng lượt xem vi.wikipedia theo ngày (triệu), người dùng thật."""
    muc = json.loads((tv.THU_MUC_DU_LIEU / "wikipedia-vi-tong" / "vi-wikipedia-tong-2016-2025.json")
                     .read_text(encoding="utf-8"))["items"]
    return pd.Series([m["views"] / 1e6 for m in muc],
                     index=pd.to_datetime([m["timestamp"][:8] for m in muc], format="%Y%m%d"), name="y")


def ngay_tet(tu: int = 2016, den: int = 2026) -> pd.DatetimeIndex:
    """Mùng 1 Tết Nguyên Đán (âm lịch) mỗi năm, theo gói holidays."""
    import holidays
    vn = holidays.VN(years=range(tu, den + 1))
    return pd.DatetimeIndex(sorted(pd.Timestamp(d) for d, ten in vn.items() if ten == "Lunar New Year"))


KHAI_TET = False            # khai Tết cho Prophet
CUA_SO_TET = 7              # hiệu ứng Tết kéo dài từ 7 ngày trước tới 7 ngày sau mùng 1


def prophet_wiki(lich_su: pd.DataFrame, ds_can: pd.DataFrame, khai_tet: bool | None = None) -> pd.DataFrame:
    """Prophet trên lượt xem theo ngày; khai Tết thì thêm một 'ngày lễ' tên tet với cửa sổ ± CUA_SO_TET ngày."""
    from prophet import Prophet
    khai_tet = KHAI_TET if khai_tet is None else khai_tet
    kw = {}
    if khai_tet:
        kw["holidays"] = pd.DataFrame({"holiday": "tet", "ds": ngay_tet(), "lower_window": -CUA_SO_TET,
                                       "upper_window": CUA_SO_TET})
    mh = Prophet(**kw).fit(lich_su[["ds", "y"]])
    return ds_can.assign(Prophet=mh.predict(ds_can[["ds"]])["yhat"].to_numpy())


def backtest_wiki(so_cua_so: int = 2, khai_tet: bool | None = None) -> pd.DataFrame:
    """Hai cửa sổ: học tới 31/12/2023 dự báo 2024, học tới 31/12/2024 dự báo 2025 (365 ngày). Kèm seasonal naive
    364 ngày (cùng thứ trong tuần năm trước)."""
    y = doc_wiki()
    df = pd.DataFrame({"unique_id": "vi", "ds": y.index, "y": y.to_numpy()})

    def ham(lich_su, ds_can):
        ra = prophet_wiki(lich_su, ds_can, khai_tet)
        cu = lich_su.set_index("ds")["y"]
        ra["SN364"] = cu.reindex(ds_can["ds"] - pd.Timedelta(days=364)).to_numpy()
        return ra

    return backtest(df, ham, h=365, so_cua_so=so_cua_so, buoc=365)


def mae_quanh_tet(kq: pd.DataFrame, cot: str = "Prophet") -> float:
    """MAE trong các ngày cách mùng 1 Tết không quá CUA_SO_TET ngày."""
    tet = ngay_tet()
    gan = np.array([np.min(np.abs((tet - d).days)) <= CUA_SO_TET for d in kq["ds"]])
    return float((kq["y"] - kq[cot]).abs()[gan].mean())


# %%
if __name__ == "__main__":
    y, X = cap_gia()
    print("OLS:", hoi_quy_ols(y, X))
    print("hồi quy động:", he_so_ip(y, X))
    print("mô phỏng:", mo_phong_hoi_quy_gia(200))
    kq = backtest_wiki()
    print("Prophet có Tết — MAE cả năm", round(float((kq["y"] - kq["Prophet"]).abs().mean()), 3),
          "| quanh Tết", round(mae_quanh_tet(kq), 3), "| SN364 cả năm", round(float((kq["y"] - kq["SN364"]).abs().mean()), 3))
    kq_d = backtest_dien(so_cua_so=2, cac=("SN24", "OLS", "DHR"))
    print(mae_theo_cua_so(kq_d).mean().round(0))
