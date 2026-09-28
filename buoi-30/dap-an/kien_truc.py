"""Buổi 30 — N-BEATS, N-HiTS, DeepAR, TFT, TiDE (bản ĐÃ SỬA).

Nhu cầu điện theo giờ của 5 vùng điều độ Mỹ (EIA-930) + nhiệt độ một điểm đại diện mỗi vùng (Open-Meteo): nhiệt độ gần thực tế
(`nhiet_do_thuc`, chỉ biết SAU) và nhiệt độ đã dự báo trước 1 ngày (`nhiet_do_du_bao`, biết TRƯỚC). Năm kiến trúc qua neuralforecast,
so với seasonal naive, MSTL, LightGBM và dự báo day-ahead của chính vùng điều độ, trên cùng các mốc test.

Chỉ định nghĩa hàm và hằng số; phần chạy nằm trong code/lab.ipynb (bộ chấm nạp module này).
"""
from __future__ import annotations

import logging
import time
import warnings

import numpy as np
import pandas as pd

from tv import THU_MUC_DU_LIEU

warnings.filterwarnings("ignore")
for _ten in ("pytorch_lightning", "lightning", "lightning.pytorch", "lightning_fabric", "neuralforecast"):
    logging.getLogger(_ten).setLevel(logging.ERROR)

VUNG = {"CISO": "Los Angeles", "ERCO": "Dallas", "MISO": "Indianapolis", "NYIS": "New York", "PJM": "Philadelphia"}
H = 24                               # đoán 24 giờ tới
L = 168                              # nhìn 7 ngày
TU = pd.Timestamp("2024-02-01")      # nhiệt độ dự báo lưu trữ đủ từ cuối 1/2024
MOC_VAL = pd.Timestamp("2025-05-01")
MOC_TEST = pd.Timestamp("2025-07-01")
DEN = pd.Timestamp("2026-01-01")

# Loại covariate — đặt sai loại là rò rỉ (mục 4.1)
FUTR_EXOG = ["nhiet_do_du_bao", "gio", "thu"]     # biết trước cho cả 24 giờ tới
HIST_EXOG = ["nhiet_do_thuc"]                     # chỉ biết tới mốc dự báo
STAT_EXOG = [f"la_{v}" for v in VUNG]             # không đổi theo thời gian: vùng nào


# ---------------------------------------------------------------------------- dữ liệu

def _doc_eia(tep) -> pd.DataFrame:
    d = pd.read_csv(tep, usecols=["Balancing Authority", "UTC Time at End of Hour", "Demand Forecast (MW)", "Demand (MW)"],
                    dtype=str)
    d = d[d["Balancing Authority"].isin(VUNG)]
    so = lambda c: pd.to_numeric(d[c].str.replace(",", ""), errors="coerce")  # noqa: E731
    return pd.DataFrame({"unique_id": d["Balancing Authority"].to_numpy(),
                         "ds": pd.to_datetime(d["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p").to_numpy(),
                         "y": so("Demand (MW)").to_numpy(), "eia_du_bao": so("Demand Forecast (MW)").to_numpy()})


def _doc_thoi_tiet(vung: str) -> pd.DataFrame:
    tep = next((THU_MUC_DU_LIEU / f"open-meteo-du-bao-luu-{vung.lower()}-2024-2025").glob("*.csv"))
    d = pd.read_csv(tep, skiprows=3)
    d.columns = [c.split(" (")[0] for c in d.columns]
    return pd.DataFrame({"unique_id": vung, "ds": pd.to_datetime(d["time"]),
                         "nhiet_do_thuc": d["temperature_2m"], "nhiet_do_du_bao": d["temperature_2m_previous_day1"]})


def doc_du_lieu() -> pd.DataFrame:
    """unique_id (vùng), ds (UTC, CUỐI giờ), y (MW), eia_du_bao (MW), nhiet_do_thuc, nhiet_do_du_bao (°C), gio, thu, la_<vùng>.

    Làm sạch chỉ nhìn quá khứ (không rò rỉ vào backtest): lưới giờ đều; nhu cầu ≤ 0 hoặc lệch > 50% so với trung vị 25 giờ TRƯỚC nó coi là
    lỗi đo → NaN; lỗ lấp bằng giá trị cùng giờ tuần trước. Nhiệt độ ghép theo giờ.
    """
    tep = sorted(THU_MUC_DU_LIEU.glob("eia930-balance-*/*.csv"))
    d = pd.concat([_doc_eia(t) for t in tep], ignore_index=True).drop_duplicates(["unique_id", "ds"], keep="last")
    luoi = pd.MultiIndex.from_product([sorted(VUNG), pd.date_range(TU, DEN - pd.Timedelta(hours=1), freq="h")],
                                      names=["unique_id", "ds"])
    d = lam_sach(d.set_index(["unique_id", "ds"]).reindex(luoi).reset_index())
    so_loi = d.attrs["so_lo_i"]
    tt = pd.concat([_doc_thoi_tiet(v) for v in VUNG], ignore_index=True)
    d = d.merge(tt, on=["unique_id", "ds"], how="left")
    d["gio"] = d["ds"].dt.hour / 23.0
    d["thu"] = d["ds"].dt.dayofweek / 6.0
    for v in VUNG:
        d[f"la_{v}"] = (d["unique_id"] == v).astype(float)
    d.attrs["so_lo_i"] = so_loi
    return d


def lam_sach(d: pd.DataFrame) -> pd.DataFrame:
    """Nhu cầu ≤ 0 hoặc lệch > 50% so với trung vị 25 giờ TRƯỚC nó → NaN; lỗ lấp bằng cùng giờ tuần trước. Chỉ nhìn quá khứ."""
    d = d.sort_values(["unique_id", "ds"]).reset_index(drop=True)
    trung_vi = d.groupby("unique_id")["y"].transform(lambda s: s.shift(1).rolling(25, min_periods=12).median())
    loi = (d["y"] <= 0) | ((d["y"] - trung_vi).abs() > 0.5 * trung_vi)
    d["y"] = d["y"].mask(loi)
    for _ in range(4):                   # lỗ dài tới 4 tuần: lấp dần bằng tuần trước
        d["y"] = d["y"].fillna(d.groupby("unique_id")["y"].shift(168))
    d.attrs["so_lo_i"] = int(loi.sum())
    return d


def bang_tinh(d: pd.DataFrame) -> pd.DataFrame:
    """Bảng biến tĩnh cho neuralforecast: một dòng mỗi vùng."""
    return d.groupby("unique_id")[STAT_EXOG].first().reset_index()


def du_lieu_moc(d: pd.DataFrame, moc: pd.Timestamp, cot_futr: list[str] | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cái biết được LÚC mốc: lịch sử (mọi cột) tới mốc, và futr_df cho 24 giờ sau mốc chỉ gồm các cột tương lai `cot_futr`."""
    moc = pd.Timestamp(moc)
    lich_su = d[d["ds"] <= moc]
    sau = d[(d["ds"] > moc) & (d["ds"] <= moc + pd.Timedelta(hours=H))]
    return lich_su, sau[["unique_id", "ds", *(FUTR_EXOG if cot_futr is None else cot_futr)]].reset_index(drop=True)


def cac_moc_test(so: int = 37, buoc_ngay: int = 5) -> list[pd.Timestamp]:
    """37 mốc 00:00 UTC, cách nhau 5 ngày từ 1/7/2025 → rơi đủ mọi thứ trong tuần."""
    return [MOC_TEST + pd.Timedelta(days=buoc_ngay * i) for i in range(so)]


# ---------------------------------------------------------------------------- 5 kiến trúc

# Cấu hình rút gọn cho CPU (Phase 29 đo: mặc định TFT ~17 phút, DeepAR ~9 phút cho 5 chuỗi)
RIENG = {"NBEATS": {}, "NHITS": {}, "DeepAR": {"trajectory_samples": 50}, "TFT": {"hidden_size": 32}, "TiDE": {"hidden_size": 128}}


def tao_mo_hinh(ten: str, max_steps: int = 300, seed: int = 0, futr: list[str] | None = None,
                hist: list[str] | None = None, **them):
    """Một mô hình neuralforecast với cấu hình chung của buổi. futr/hist: ghi đè danh sách covariate (thí nghiệm mục 4.1)."""
    from neuralforecast.losses.pytorch import MAE, DistributionLoss
    from neuralforecast.models import NBEATS, NHITS, TFT, DeepAR, TiDE
    futr = FUTR_EXOG if futr is None else futr
    hist = HIST_EXOG if hist is None else hist
    chung = dict(h=H, input_size=L, max_steps=max_steps, random_seed=seed, scaler_type="robust", val_check_steps=100,
                 early_stop_patience_steps=3, windows_batch_size=256, enable_progress_bar=False, enable_model_summary=False,
                 logger=False, accelerator="cpu", **{**RIENG[ten], **them})
    exog = dict(futr_exog_list=futr, hist_exog_list=hist, stat_exog_list=STAT_EXOG)
    if ten == "NBEATS":        # bản diễn giải được: khối xu hướng + khối mùa vụ; không nhận covariate
        return NBEATS(**chung, stack_types=["trend", "seasonality"])
    if ten == "NHITS":
        return NHITS(**chung, **exog)
    if ten == "DeepAR":        # không nhận hist_exog
        return DeepAR(**chung, futr_exog_list=futr, stat_exog_list=STAT_EXOG,
                      loss=DistributionLoss("StudentT", level=[80, 90]), valid_loss=MAE())
    if ten == "TFT":
        return TFT(**chung, **exog)
    if ten == "TiDE":
        return TiDE(**chung, **exog)
    raise ValueError(ten)


KIEN_TRUC = ["NBEATS", "NHITS", "DeepAR", "TFT", "TiDE"]


def huan_luyen(d: pd.DataFrame, ten: str, **kw):
    """Học một kiến trúc trên dữ liệu trước MOC_TEST; 2 tháng cuối (từ MOC_VAL) làm val để dừng sớm. Trả (nf, giây)."""
    from neuralforecast import NeuralForecast
    m = tao_mo_hinh(ten, **kw)
    nf = NeuralForecast(models=[m], freq="h")
    t0 = time.time()
    nf.fit(d[d["ds"] < MOC_TEST][_cot(m)], static_df=bang_tinh(d), val_size=int((MOC_TEST - MOC_VAL) / pd.Timedelta(hours=1)))
    return nf, time.time() - t0


def _cot(m) -> list[str]:
    """Chỉ các cột mô hình khai báo (neuralforecast báo lỗi nếu cột thừa có ô trống)."""
    return ["unique_id", "ds", "y", *m.futr_exog_list, *m.hist_exog_list]


def du_bao_cac_moc(nf, d: pd.DataFrame, cac_moc: list[pd.Timestamp], thay_futr: dict[str, str] | None = None) -> pd.DataFrame:
    """Dự báo 24 giờ sau từng mốc bằng đúng cái biết lúc mốc. thay_futr={"cột mô hình dùng": "cột đem vào"}: đổi nguồn một covariate
    tương lai lúc dự báo (thí nghiệm mục 4.1: học bằng nhiệt độ thực, lúc vận hành chỉ có nhiệt độ dự báo)."""
    cot_futr = list(nf.models[0].futr_exog_list)
    ra = []
    for moc in cac_moc:
        lich_su, futr = du_lieu_moc(d, moc, cot_futr)
        for cot_mh, cot_vao in (thay_futr or {}).items():
            sau = d[(d["ds"] > moc) & (d["ds"] <= moc + pd.Timedelta(hours=H))]
            futr[cot_mh] = sau[cot_vao].to_numpy()
        p = nf.predict(df=lich_su[_cot(nf.models[0])], static_df=bang_tinh(d), futr_df=futr)
        ra.append(p.assign(moc=moc))
    return pd.concat(ra, ignore_index=True)


# ---------------------------------------------------------------------------- baseline trên cùng các mốc

def seasonal_naive(d: pd.DataFrame, cac_moc: list[pd.Timestamp], m: int = 168) -> pd.DataFrame:
    s = d.set_index(["unique_id", "ds"])["y"]
    ra = []
    for moc in cac_moc:
        ds = pd.date_range(moc + pd.Timedelta(hours=1), periods=H, freq="h")
        for v in VUNG:
            ra.append(pd.DataFrame({"unique_id": v, "ds": ds, "moc": moc,
                                    "SeasonalNaive": s.loc[v].reindex(ds - pd.Timedelta(hours=m)).to_numpy()}))
    return pd.concat(ra, ignore_index=True)


def eia(d: pd.DataFrame, cac_moc: list[pd.Timestamp]) -> pd.DataFrame:
    """Dự báo day-ahead do chính vùng điều độ công bố (cột Demand Forecast của EIA-930) — baseline thật cần vượt."""
    ra = [d[(d["ds"] > m) & (d["ds"] <= m + pd.Timedelta(hours=H))][["unique_id", "ds", "eia_du_bao"]].assign(moc=m) for m in cac_moc]
    return pd.concat(ra, ignore_index=True).rename(columns={"eia_du_bao": "EIA"})


def mstl(d: pd.DataFrame, cac_moc: list[pd.Timestamp], so_tuan: int = 8) -> pd.DataFrame:
    from statsforecast import StatsForecast
    from statsforecast.models import MSTL
    sf = StatsForecast(models=[MSTL(season_length=[24, 168])], freq="h", n_jobs=1)
    ra = []
    for moc in cac_moc:
        cua = d[(d["ds"] <= moc) & (d["ds"] > moc - pd.Timedelta(weeks=so_tuan))][["unique_id", "ds", "y"]]
        ra.append(sf.forecast(df=cua, h=H).assign(moc=moc))
    return pd.concat(ra, ignore_index=True)


def lightgbm(d: pd.DataFrame, cac_moc: list[pd.Timestamp]) -> pd.DataFrame:
    """LightGBM global: lag 24…168 giờ + nhiệt độ DỰ BÁO + giờ, thứ; học một lần trên dữ liệu trước MOC_TEST."""
    import lightgbm as lgb
    from mlforecast import MLForecast
    from mlforecast.target_transforms import LocalStandardScaler
    cot = ["unique_id", "ds", "y", *FUTR_EXOG]
    fc = MLForecast(models={"LightGBM": lgb.LGBMRegressor(n_estimators=400, learning_rate=0.05, num_leaves=63, verbose=-1,
                                                          random_state=0, n_jobs=4)},
                    freq="h", lags=[24, 48, 72, 96, 120, 144, 168], target_transforms=[LocalStandardScaler()])
    fc.fit(d[d["ds"] < MOC_TEST][cot], static_features=[])
    ra = []
    for moc in cac_moc:
        lich_su, futr = du_lieu_moc(d, moc)
        ra.append(fc.predict(h=H, new_df=lich_su[cot], X_df=futr).assign(moc=moc))
    return pd.concat(ra, ignore_index=True)


# ---------------------------------------------------------------------------- chấm

def mau_so_mase(d: pd.DataFrame, m: int = 168) -> pd.Series:
    tr = d[d["ds"] < MOC_VAL]
    return tr.groupby("unique_id")["y"].apply(lambda y: np.nanmean(np.abs(y.to_numpy()[m:] - y.to_numpy()[:-m])))


def bang_mase(du_bao: pd.DataFrame, d: pd.DataFrame, cac_cot: list[str]) -> pd.DataFrame:
    """MASE từng vùng và trung bình 5 vùng (mọi mốc gộp lại)."""
    x = du_bao.merge(d[["unique_id", "ds", "y"]], on=["unique_id", "ds"])
    mau = mau_so_mase(d)
    ra = {}
    for c in cac_cot:
        mae = x.assign(e=(x["y"] - x[c]).abs()).groupby("unique_id")["e"].mean()
        mase = mae / mau.loc[mae.index]
        ra[c] = {**mase.round(3).to_dict(), "trung bình": round(float(mase.mean()), 3)}
    return pd.DataFrame(ra).T


# ---------------------------------------------------------------------------- DeepAR cho dữ liệu đếm (xe đạp thuê theo giờ)

def doc_xe_dap() -> pd.DataFrame:
    """UCI Bike Sharing, số lượt thuê mỗi giờ (Washington D.C., 2011–2012). Giờ không có dòng = 0 lượt (hệ thống ghi thiếu khi không ai
    thuê hoặc bảo trì). Một chuỗi, unique_id = "xe_dap"."""
    d = pd.read_csv(THU_MUC_DU_LIEU / "uci-bike-sharing" / "hour.csv")
    ds = pd.to_datetime(d["dteday"]) + pd.to_timedelta(d["hr"], unit="h")
    s = pd.Series(d["cnt"].to_numpy(dtype=float), index=ds)
    s = s.reindex(pd.date_range(s.index.min(), s.index.max(), freq="h"), fill_value=0.0)
    return pd.DataFrame({"unique_id": "xe_dap", "ds": s.index, "y": s.to_numpy()})


def deepar_dem(x: pd.DataFrame, phan_phoi: str, moc_test: str = "2012-10-01", so_moc: int = 30, max_steps: int = 300):
    """DeepAR với phân phối `phan_phoi` ("NegativeBinomial" hoặc "Normal"); dự báo 24 giờ ở `so_moc` mốc liên tiếp mỗi ngày.
    Trả bảng dài: ds, moc, h (1…24), y, trung vị, cận 80%."""
    from neuralforecast import NeuralForecast
    from neuralforecast.losses.pytorch import MAE, DistributionLoss
    from neuralforecast.models import DeepAR
    moc0 = pd.Timestamp(moc_test)
    m = DeepAR(h=H, input_size=L, max_steps=max_steps, random_seed=0, scaler_type="identity" if phan_phoi == "NegativeBinomial"
               else "robust", loss=DistributionLoss(phan_phoi, level=[80]), valid_loss=MAE(), enable_progress_bar=False,
               enable_model_summary=False, logger=False, accelerator="cpu")
    nf = NeuralForecast(models=[m], freq="h")
    t0 = time.time()
    nf.fit(x[x["ds"] < moc0])
    giay = time.time() - t0
    ra = []
    for i in range(so_moc):
        moc = moc0 + pd.Timedelta(days=i)
        p = nf.predict(df=x[x["ds"] < moc]).assign(moc=moc)
        ra.append(p)
    p = pd.concat(ra, ignore_index=True).merge(x, on=["unique_id", "ds"])
    p["h"] = ((p["ds"] - p["moc"]) / pd.Timedelta(hours=1)).astype(int) + 1
    p = p.rename(columns={"DeepAR-median": "trung_vi", "DeepAR-lo-80": "duoi", "DeepAR-hi-80": "tren"})
    p.attrs["giay"] = giay
    return p[["ds", "moc", "h", "y", "trung_vi", "duoi", "tren"]]


# ---------------------------------------------------------------------------- đọc bên trong mô hình

def thanh_phan_nbeats(nf, d: pd.DataFrame, moc: pd.Timestamp, vung: str = "ERCO") -> pd.DataFrame:
    """N-BEATS bản diễn giải được: tách dự báo 24 giờ thành mức (giờ cuối) + xu hướng + mùa vụ.

    `decompose` trả mỗi khối đã cộng "vị trí" của scaler; tổng ba khối = dự báo + 2 × vị trí nên suy ra được vị trí để trừ đi."""
    from neuralforecast.tsdataset import TimeSeriesDataset
    lich_su, _ = du_lieu_moc(d, moc, [])
    ts, *_ = TimeSeriesDataset.from_df(lich_su[["unique_id", "ds", "y"]])
    khoi = nf.models[0].decompose(dataset=ts)[sorted(VUNG).index(vung)]
    p = nf.predict(df=lich_su[["unique_id", "ds", "y"]])
    tong = p[p["unique_id"] == vung]["NBEATS"].to_numpy()
    vi_tri = (khoi.sum(axis=0) - tong) / 2
    that = d[(d["unique_id"] == vung) & (d["ds"] > moc) & (d["ds"] <= moc + pd.Timedelta(hours=H))]["y"].to_numpy()
    return pd.DataFrame({"h": np.arange(1, H + 1), "muc": khoi[0], "xu_huong": khoi[1] - vi_tri, "mua_vu": khoi[2] - vi_tri,
                         "du_bao": tong, "thuc_te": that})


def tft_chon_bien(nf) -> dict[str, pd.Series]:
    """Trọng số chọn biến của TFT ở lần dự báo gần nhất, trung bình theo thời gian: quá khứ, tương lai, tĩnh."""
    fi = nf.models[0].feature_importances()
    return {"quá khứ": fi["Past variable importance over time"].mean().sort_values(ascending=False),
            "tương lai": fi["Future variable importance over time"].mean().sort_values(ascending=False),
            "tĩnh": fi["Static covariates"]["importance"].sort_values(ascending=False)}


def coverage_theo_tam(f: pd.DataFrame, d: pd.DataFrame, muc: int = 80) -> pd.Series:
    """Tỷ lệ giờ thực tế nằm trong khoảng `muc`% của DeepAR, theo tầm 1…24 giờ."""
    x = f.merge(d[["unique_id", "ds", "y"]], on=["unique_id", "ds"])
    h = ((x["ds"] - x["moc"]) / pd.Timedelta(hours=1)).astype(int)
    trong = (x["y"] >= x[f"DeepAR-lo-{muc}"]) & (x["y"] <= x[f"DeepAR-hi-{muc}"])
    return trong.groupby(h).mean()
