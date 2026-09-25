"""Lời giải mẫu dự án giữa chặng 2 (giám khảo giữ, không vào zip). Cùng giao diện với code/du_bao.py.

Bậc thang: seasonal naive → hồi quy có nhiệt độ → LightGBM global (5 vùng chung một mô hình) → ensemble (trung bình
hồi quy và LightGBM, định sẵn). Backtest dùng dl.dau_vao: nhiệt độ của tuần dự báo là nhiệt độ ĐÃ DỰ BÁO lúc mốc.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "cong-cu"))
import du_lieu as dl  # noqa: E402

SEED = 0
TRE_MIN = dl.H + dl.TRE_CONG_BO
THAM_SO_LGBM = {"n_estimators": 600, "learning_rate": 0.03, "num_leaves": 63, "min_child_samples": 50, "subsample": 0.8,
                "subsample_freq": 1, "colsample_bytree": 0.8, "objective": "l1", "random_state": SEED, "verbose": -1,
                "n_jobs": 4, "deterministic": True, "force_row_wise": True}
DAC_TRUNG_LGBM = ["tre_336_tl", "tre_504_tl", "tb_tuan_tl", "gio", "thu", "gio_trong_tuan", "nhiet_do", "nong", "lanh",
                  "nhiet_do_tb24", "vung_ma", "ngay_trong_nam"]


def dac_trung(df: pd.DataFrame) -> pd.DataFrame:
    """df: vung, ds, y, nhiet_do. Mọi đặc trưng từ y chỉ dùng y tới ds − 216 giờ. Nhu cầu chia cho mức (trung bình 2 tuần
    kết thúc ở ds − 216 giờ) để 5 vùng có cùng thang."""
    df = df.sort_values(["vung", "ds"])
    g = df.groupby("vung", sort=False)["y"]
    ra = df[["vung", "ds"]].copy()
    ra["tre_336"] = g.shift(336)
    ra["tre_504"] = g.shift(504)
    ra["muc"] = g.transform(lambda s: s.shift(TRE_MIN).rolling(336, min_periods=168).mean())
    ra["tre_336_tl"] = ra["tre_336"] / ra["muc"]
    ra["tre_504_tl"] = ra["tre_504"] / ra["muc"]
    ra["tb_tuan_tl"] = (g.shift(336) + g.shift(504) + g.shift(672)) / 3 / ra["muc"]
    ra["gio"] = df["ds"].dt.hour
    ra["thu"] = df["ds"].dt.dayofweek
    ra["gio_trong_tuan"] = ra["thu"] * 24 + ra["gio"]
    ra["ngay_trong_nam"] = df["ds"].dt.dayofyear
    ra["nhiet_do"] = df["nhiet_do"]
    ra["nong"] = (df["nhiet_do"] - 18).clip(lower=0)
    ra["lanh"] = (18 - df["nhiet_do"]).clip(lower=0)
    ra["nhiet_do_tb24"] = df.groupby("vung", sort=False)["nhiet_do"].transform(lambda s: s.rolling(24, min_periods=1).mean())
    ra["vung_ma"] = df["vung"].map({v: i for i, v in enumerate(sorted(dl.VUNG))})
    return ra


def _bang(lich_su, thoi_tiet, moc):
    tuong_lai = pd.DataFrame([(v, d) for v in dl.VUNG for d in pd.date_range(moc + pd.Timedelta(hours=1), periods=dl.H,
                                                                            freq="h")], columns=["vung", "ds"])
    df = pd.concat([lich_su[["vung", "ds", "y"]], tuong_lai], ignore_index=True).merge(thoi_tiet, on=["vung", "ds"], how="left")
    return dac_trung(df).merge(df[["vung", "ds", "y"]], on=["vung", "ds"])


def seasonal_naive(lich_su, moc):
    ra = []
    for v, g in lich_su.groupby("vung"):
        y = g.set_index("ds")["y"]
        ds = pd.date_range(moc + pd.Timedelta(hours=1), periods=dl.H, freq="h")
        t1, t2 = y.reindex(ds - pd.Timedelta(hours=168)).to_numpy(), y.reindex(ds - pd.Timedelta(hours=336)).to_numpy()
        ra.append(pd.DataFrame({"vung": v, "ds": ds, "du_bao": np.where(np.isnan(t1), t2, t1)}))
    return pd.concat(ra, ignore_index=True)


def hoi_quy(lich_su, thoi_tiet, moc, f=None):
    from sklearn.linear_model import Ridge
    f = _bang(lich_su, thoi_tiet, moc) if f is None else f
    ra = []
    for v, g in f.groupby("vung"):
        X = pd.get_dummies(g["gio_trong_tuan"].astype("category"), prefix="g").astype(float)
        X[["tre_336", "nong", "lanh", "muc"]] = g[["tre_336", "nong", "lanh", "muc"]]
        X["nong2"], X["lanh2"] = g["nong"] ** 2, g["lanh"] ** 2
        for gb in range(0, 24, 6):                     # tác dụng của nóng/lạnh khác nhau theo khung 6 giờ
            khung = ((g["gio"] >= gb) & (g["gio"] < gb + 6)).astype(float)
            X[f"nong_{gb}"], X[f"lanh_{gb}"] = g["nong"] * khung, g["lanh"] * khung
        hoc = (g["ds"] <= moc) & (g["ds"] > moc - pd.Timedelta(weeks=52)) & X.notna().all(axis=1) & g["y"].notna()
        sau = g["ds"] > moc
        m = Ridge(alpha=1.0).fit(X[hoc], g.loc[hoc, "y"])
        ra.append(pd.DataFrame({"vung": v, "ds": g.loc[sau, "ds"], "du_bao": m.predict(X[sau].fillna(X[hoc].mean()))}))
    return pd.concat(ra, ignore_index=True)


def lgbm(lich_su, thoi_tiet, moc, f=None):
    import lightgbm as lgb
    f = _bang(lich_su, thoi_tiet, moc) if f is None else f
    hoc = (f["ds"] <= moc) & f["y"].notna() & f["muc"].notna()
    sau = f["ds"] > moc
    m = lgb.LGBMRegressor(**THAM_SO_LGBM).fit(f.loc[hoc, DAC_TRUNG_LGBM], f.loc[hoc, "y"] / f.loc[hoc, "muc"])
    return pd.DataFrame({"vung": f.loc[sau, "vung"], "ds": f.loc[sau, "ds"],
                         "du_bao": m.predict(f.loc[sau, DAC_TRUNG_LGBM]) * f.loc[sau, "muc"]})


def bac_thang(lich_su, thoi_tiet, moc) -> pd.DataFrame:
    """Dự báo của cả 4 nấc: vung, ds, seasonal_naive, hoi_quy, lgbm, ensemble."""
    moc = pd.Timestamp(moc)
    f = _bang(lich_su, thoi_tiet, moc)
    ra = seasonal_naive(lich_su, moc).rename(columns={"du_bao": "seasonal_naive"})
    for ten, ham in [("hoi_quy", hoi_quy), ("lgbm", lgbm)]:
        ra = ra.merge(ham(lich_su, thoi_tiet, moc, f).rename(columns={"du_bao": ten}), on=["vung", "ds"])
    ra["ensemble"] = ra[["hoi_quy", "lgbm"]].mean(axis=1)
    return ra


def du_bao(lich_su, thoi_tiet, moc) -> pd.DataFrame:
    b = bac_thang(lich_su, thoi_tiet, moc)
    return b[["vung", "ds"]].assign(du_bao=b["ensemble"])


def backtest(lich_su, thoi_tiet_luu, cac_moc, tat_ca_nac: bool = False) -> pd.DataFrame:
    ra = []
    for moc in cac_moc:
        ls, tt = dl.dau_vao(lich_su, thoi_tiet_luu, moc)
        f = bac_thang(ls, tt, moc) if tat_ca_nac else du_bao(ls, tt, moc)
        f = f.merge(tt, on=["vung", "ds"], how="left").assign(moc=moc)
        f["h"] = ((f["ds"] - moc) / pd.Timedelta(hours=1)).astype(int)
        ra.append(f.merge(lich_su[["vung", "ds", "y", "df"]], on=["vung", "ds"], how="left"))
    cot = ["vung", "moc", "ds", "h", "y", "du_bao", "nhiet_do"] if not tat_ca_nac else None
    kq = pd.concat(ra, ignore_index=True)
    return kq[cot] if cot else kq
