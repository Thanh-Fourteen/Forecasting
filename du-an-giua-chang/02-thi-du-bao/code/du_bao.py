"""Dự án giữa chặng 2 — dự báo nhu cầu điện 168 giờ tới cho 5 vùng điều độ Mỹ (EIA-930).

Khung xuất phát. Giữ nguyên TÊN và THAM SỐ của `du_bao`, `backtest`, `dac_trung` (bộ chấm và cong-cu/nop.py gọi chúng).
Có sẵn hai nấc đầu của bậc thang: seasonal naive và hồi quy có biến nhiệt độ. Bạn thêm LightGBM global và ensemble.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cong-cu"))
import du_lieu as dl  # noqa: E402

SEED = 0
TRE_MIN = dl.H + dl.TRE_CONG_BO     # 216: trễ nhỏ nhất dùng được cho cả 168 giờ (nhu cầu biết tới mốc − 48 giờ)


# ---------------------------------------------------------------------------- đặc trưng

def dac_trung(df: pd.DataFrame) -> pd.DataFrame:
    """df: vung, ds, y, nhiet_do. Trả vung, ds + đặc trưng. Mọi đặc trưng từ y chỉ dùng y tới ds − 216 giờ."""
    df = df.sort_values(["vung", "ds"])
    g = df.groupby("vung", sort=False)["y"]
    ra = df[["vung", "ds"]].copy()
    ra["tre_336"] = g.shift(336)                       # cùng giờ, 2 tuần trước
    ra["tre_504"] = g.shift(504)                       # cùng giờ, 3 tuần trước
    ra["gio_trong_tuan"] = df["ds"].dt.dayofweek * 24 + df["ds"].dt.hour
    ra["nong"] = (df["nhiet_do"] - 18).clip(lower=0)   # độ nóng hơn 18 °C (điều hoà)
    ra["lanh"] = (18 - df["nhiet_do"]).clip(lower=0)   # độ lạnh hơn 18 °C (sưởi)
    return ra


# ---------------------------------------------------------------------------- các nấc của bậc thang

def seasonal_naive(lich_su: pd.DataFrame, moc: pd.Timestamp) -> pd.DataFrame:
    """Lặp lại tuần gần nhất đã biết đủ: giờ nào có số của 1 tuần trước thì lấy, không thì lấy 2 tuần trước."""
    ra = []
    for v, g in lich_su.groupby("vung"):
        y = g.set_index("ds")["y"]
        ds = pd.date_range(moc + pd.Timedelta(hours=1), periods=dl.H, freq="h")
        tuan1 = y.reindex(ds - pd.Timedelta(hours=168)).to_numpy()
        tuan2 = y.reindex(ds - pd.Timedelta(hours=336)).to_numpy()
        ra.append(pd.DataFrame({"vung": v, "ds": ds, "du_bao": np.where(np.isnan(tuan1), tuan2, tuan1)}))
    return pd.concat(ra, ignore_index=True)


def hoi_quy(lich_su: pd.DataFrame, thoi_tiet: pd.DataFrame, moc: pd.Timestamp) -> pd.DataFrame:
    """Mỗi vùng một hồi quy tuyến tính: nhu cầu ~ giờ trong tuần + nóng + lạnh + trễ 336 giờ, học 52 tuần gần nhất."""
    from sklearn.linear_model import Ridge
    tuong_lai = pd.DataFrame([(v, d) for v in dl.VUNG for d in pd.date_range(moc + pd.Timedelta(hours=1), periods=dl.H,
                                                                            freq="h")], columns=["vung", "ds"])
    df = pd.concat([lich_su[["vung", "ds", "y"]], tuong_lai], ignore_index=True).merge(thoi_tiet, on=["vung", "ds"], how="left")
    f = dac_trung(df).merge(df[["vung", "ds", "y"]], on=["vung", "ds"])
    cot = ["tre_336", "nong", "lanh"]
    ra = []
    for v, g in f.groupby("vung"):
        X = pd.get_dummies(g["gio_trong_tuan"].astype("category"), prefix="g").join(g[cot]).astype(float)
        hoc = (g["ds"] <= moc) & (g["ds"] > moc - pd.Timedelta(weeks=52)) & X.notna().all(axis=1) & g["y"].notna()
        sau = g["ds"] > moc
        m = Ridge(alpha=1.0).fit(X[hoc], g.loc[hoc, "y"])
        ra.append(pd.DataFrame({"vung": v, "ds": g.loc[sau, "ds"], "du_bao": m.predict(X[sau].fillna(X[hoc].mean()))}))
    return pd.concat(ra, ignore_index=True)


# ---------------------------------------------------------------------------- dự báo và backtest

def du_bao(lich_su: pd.DataFrame, thoi_tiet: pd.DataFrame, moc: pd.Timestamp) -> pd.DataFrame:
    """Dự báo nộp bài. lich_su: vung, ds, y, df — chỉ tới mốc − 48 giờ. thoi_tiet: vung, ds, nhiet_do — quá khứ là nhiệt
    độ thật, 168 giờ sau mốc là nhiệt độ đã dự báo lúc mốc. Trả vung, ds, du_bao: 5 vùng × 168 giờ."""
    return hoi_quy(lich_su, thoi_tiet, pd.Timestamp(moc))


def backtest(lich_su: pd.DataFrame, thoi_tiet_luu: pd.DataFrame, cac_moc: list[pd.Timestamp]) -> pd.DataFrame:
    """Chạy du_bao ở từng mốc cũ, chỉ với dữ liệu có lúc đó. thoi_tiet_luu: vung, ds, thuc, truoc_1 … truoc_7.
    Trả vung, moc, ds, h, y, du_bao, nhiet_do (nhiệt độ đã đưa vào mô hình cho giờ đó)."""
    ra = []
    for moc in cac_moc:
        ls = lich_su[lich_su["ds"] <= moc - pd.Timedelta(hours=dl.TRE_CONG_BO)]
        tt = thoi_tiet_luu[["vung", "ds", "thuc"]].rename(columns={"thuc": "nhiet_do"})
        f = du_bao(ls, tt, moc).merge(tt, on=["vung", "ds"], how="left")
        f["moc"] = moc
        f["h"] = ((f["ds"] - moc) / pd.Timedelta(hours=1)).astype(int)
        ra.append(f.merge(lich_su[["vung", "ds", "y"]], on=["vung", "ds"], how="left"))
    return pd.concat(ra, ignore_index=True)[["vung", "moc", "ds", "h", "y", "du_bao", "nhiet_do"]]


if __name__ == "__main__":
    ls, tt = dl.doc_lich_su(), dl.doc_thoi_tiet()
    moc_nop = pd.Timestamp("2025-12-29")
    bt = backtest(ls, tt, dl.cac_moc_backtest(moc_nop))
    mau = dl.mau_so_mase(ls, moc_nop)
    loi = (bt["y"] - bt["du_bao"]).abs().groupby(bt["vung"]).mean()
    print("MASE backtest 8 tuần:", (loi / mau).round(3).to_dict())
