"""Dữ liệu chung của dự án giữa chặng 2 — ĐỪNG SỬA (bộ chấm dùng đúng tệp này).

Nhu cầu điện: EIA-930, cột `Demand (MW)` gốc, mốc "UTC Time at End of Hour" (nhãn là CUỐI giờ). `df` = dự báo day-ahead
do chính đơn vị điều độ công bố (`Demand Forecast (MW)`): đối thủ cần vượt, KHÔNG phải feature của tuần dự báo.
Thời tiết: Open-Meteo Previous Runs, một điểm đại diện mỗi vùng. `thuc` = lượt chạy mới nhất cho giờ đó (sát thực tế, chỉ
biết SAU); `truoc_K` = giá trị đã dự báo trước 24·K giờ (K = 1…7).

Nguồn:
    lab/du-lieu/raw/   2024–2025, sha256 cố định (python lab.py up)
    lab/du-lieu/moi/   từ 1/1/2026 tới lúc tải (lay_du_lieu_moi.py) — KHÔNG cố định: EIA dựng lại tệp hằng ngày và sửa số lùi
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

DU_AN = Path(__file__).resolve().parent.parent
RAW = DU_AN / "lab" / "du-lieu" / "raw"
MOI = DU_AN / "lab" / "du-lieu" / "moi"

# vùng điều độ → (thành phố đại diện, vĩ độ, kinh độ)
VUNG = {"CISO": ("Los Angeles", 34.0522, -118.2437), "ERCO": ("Dallas", 32.7767, -96.797),
        "MISO": ("Indianapolis", 39.7684, -86.1581), "NYIS": ("New York", 40.7128, -74.006),
        "PJM": ("Philadelphia", 39.9526, -75.1652)}
H = 168                      # 7 ngày × 24 giờ sau mốc nộp
TRE_CONG_BO = 48             # lúc nộp, nhu cầu chỉ biết tới mốc − 48 giờ (tệp EIA dựng lại mỗi ngày, trễ ~1,5 ngày)
SO_CUA_SO = 8                # backtest nội bộ: 8 tuần
BIEN = ["temperature_2m"] + [f"temperature_2m_previous_day{k}" for k in range(1, 8)]
TEN_BIEN = {"temperature_2m": "thuc", **{f"temperature_2m_previous_day{k}": f"truoc_{k}" for k in range(1, 8)}}
UA = {"User-Agent": "khoa-forecasting (du-an-giua-chang-2)"}


# ---------------------------------------------------------------------------- nhu cầu điện EIA-930

def _doc_eia(tep: Path) -> pd.DataFrame:
    d = pd.read_csv(tep, usecols=["Balancing Authority", "UTC Time at End of Hour", "Demand Forecast (MW)", "Demand (MW)"],
                    dtype=str)
    d = d[d["Balancing Authority"].isin(VUNG)]
    so = lambda c: pd.to_numeric(d[c].str.replace(",", ""), errors="coerce")  # noqa: E731
    return pd.DataFrame({"vung": d["Balancing Authority"].to_numpy(),
                         "ds": pd.to_datetime(d["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p").to_numpy(),
                         "y": so("Demand (MW)").to_numpy(), "df": so("Demand Forecast (MW)").to_numpy()})


def doc_lich_su() -> pd.DataFrame:
    """vung, ds (UTC, cuối giờ), y (MW), df (MW) — lưới giờ đều, giờ trống để NaN. Tệp mới hơn ghi đè tệp cũ."""
    tep = sorted(RAW.glob("eia930-balance-*/*.csv")) + sorted(MOI.glob("EIA930_BALANCE_*.csv"))
    if not tep:
        raise FileNotFoundError("chưa có dữ liệu EIA — chạy: python lab.py up")
    d = pd.concat([_doc_eia(t) for t in tep], ignore_index=True).drop_duplicates(["vung", "ds"], keep="last")
    luoi = pd.MultiIndex.from_product([sorted(VUNG), pd.date_range(d["ds"].min(), d["ds"].max(), freq="h")],
                                      names=["vung", "ds"])
    return d.set_index(["vung", "ds"]).reindex(luoi).reset_index()


# ---------------------------------------------------------------------------- thời tiết

def _doc_open_meteo(tep: Path, vung: str) -> pd.DataFrame:
    d = pd.read_csv(tep, skiprows=3)
    d.columns = [c.split(" (")[0] for c in d.columns]
    d = d.rename(columns={"time": "ds", **TEN_BIEN})
    d["ds"] = pd.to_datetime(d["ds"])
    return d.assign(vung=vung)[["vung", "ds", *TEN_BIEN.values()]]


def doc_thoi_tiet() -> pd.DataFrame:
    """vung, ds (UTC), thuc, truoc_1 … truoc_7 (°C)."""
    phan = []
    for v in VUNG:
        tep = sorted(RAW.glob(f"open-meteo-du-bao-luu-{v.lower()}-*/*.csv")) + sorted(MOI.glob(f"thoi-tiet-{v}-*.csv"))
        phan += [_doc_open_meteo(t, v) for t in tep]
    return pd.concat(phan, ignore_index=True).drop_duplicates(["vung", "ds"], keep="last").sort_values(["vung", "ds"],
                                                                                                          ignore_index=True)


def tam_ngay(h: np.ndarray | int) -> np.ndarray:
    """Giờ thứ h sau mốc (1…168) dùng dự báo trước K = ⌈h/24⌉ ngày: dự báo đó phát hành không muộn hơn mốc."""
    return np.ceil(np.asarray(h) / 24).astype(int).clip(1, 7)


def nhiet_do_du_bao(thoi_tiet: pd.DataFrame, moc: pd.Timestamp) -> pd.DataFrame:
    """Nhiệt độ đã biết LÚC mốc cho 168 giờ sau mốc: giờ thứ h lấy cột truoc_⌈h/24⌉. Trả vung, ds, h, nhiet_do."""
    moc = pd.Timestamp(moc)
    t = thoi_tiet[(thoi_tiet["ds"] > moc) & (thoi_tiet["ds"] <= moc + pd.Timedelta(hours=H))].copy()
    t["h"] = ((t["ds"] - moc) / pd.Timedelta(hours=1)).astype(int)
    k = tam_ngay(t["h"].to_numpy())
    t["nhiet_do"] = t[[f"truoc_{i}" for i in range(1, 8)]].to_numpy()[np.arange(len(t)), k - 1]
    return t[["vung", "ds", "h", "nhiet_do"]].reset_index(drop=True)


# ---------------------------------------------------------------------------- mốc và dữ liệu đầu vào

def cac_moc_backtest(moc: pd.Timestamp, so: int = SO_CUA_SO) -> list[pd.Timestamp]:
    """8 mốc thứ Hai 00:00 UTC trước mốc nộp, cách nhau 1 tuần; tuần cuối kết thúc ít nhất TRE_CONG_BO giờ trước mốc nộp
    (lúc nộp mới biết đủ nhu cầu của nó)."""
    moc = pd.Timestamp(moc)
    cuoi = moc - pd.Timedelta(hours=H + TRE_CONG_BO)
    cuoi = cuoi.normalize() - pd.Timedelta(days=cuoi.weekday())       # thứ Hai gần nhất không sau `cuoi`
    return [cuoi - pd.Timedelta(weeks=i) for i in range(so)][::-1]


def dau_vao(lich_su: pd.DataFrame, thoi_tiet: pd.DataFrame, moc: pd.Timestamp) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Đúng những gì biết được LÚC mốc — dùng cho cả backtest lẫn nộp thật:
    nhu cầu và df tới mốc − 48 giờ; nhiệt độ quá khứ (thuc) tới mốc; 168 giờ sau mốc là nhiệt độ ĐÃ DỰ BÁO (truoc_K)."""
    moc = pd.Timestamp(moc)
    ls = lich_su[lich_su["ds"] <= moc - pd.Timedelta(hours=TRE_CONG_BO)].reset_index(drop=True)
    qk = thoi_tiet[thoi_tiet["ds"] <= moc][["vung", "ds", "thuc"]].rename(columns={"thuc": "nhiet_do"})
    tl = nhiet_do_du_bao(thoi_tiet, moc).drop(columns="h")
    return ls, pd.concat([qk, tl], ignore_index=True).sort_values(["vung", "ds"], ignore_index=True)


# ---------------------------------------------------------------------------- chấm

def mau_so_mase(lich_su: pd.DataFrame, moc: pd.Timestamp) -> pd.Series:
    """Mỗi vùng: MAE của 'lặp lại tuần trước' (trễ 168 giờ) trên 8 tuần biết được lúc mốc."""
    ls = lich_su[lich_su["ds"] <= pd.Timestamp(moc) - pd.Timedelta(hours=TRE_CONG_BO)]
    ra = {}
    for v, g in ls.groupby("vung"):
        y = g.set_index("ds")["y"].iloc[-H * 9:]
        ra[v] = float(np.nanmean(np.abs(y.to_numpy()[H:] - y.to_numpy()[:-H])))
    return pd.Series(ra)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


# ---------------------------------------------------------------------------- tải dữ liệu mới (không cố định)

def _tai(url: str, dich: Path) -> Path:
    dich.parent.mkdir(parents=True, exist_ok=True)
    tam = dich.with_suffix(dich.suffix + ".tai")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r, open(tam, "wb") as f:
        while khoi := r.read(1 << 20):
            f.write(khoi)
    tam.replace(dich)
    return dich


def _ghi_nhat_ky(muc: dict) -> None:
    tep = MOI / "NHAT-KY.jsonl"
    with open(tep, "a", encoding="utf-8") as f:
        f.write(json.dumps(muc, ensure_ascii=False) + "\n")


def tai_eia_moi(den: datetime | None = None) -> list[Path]:
    """Tải các tệp sáu tháng EIA-930 từ 2026 tới nay (dựng lại mỗi ngày ~14:40 UTC). Ghi sha256 + giờ tải vào NHAT-KY.jsonl."""
    den = den or datetime.now(UTC)
    ra = []
    for nam in range(2026, den.year + 1):
        for nua, ten in ((1, "Jan_Jun"), (2, "Jul_Dec")):
            if nam == den.year and nua == 2 and den.month < 7:
                continue
            tep = MOI / f"EIA930_BALANCE_{nam}_{ten}.csv"
            _tai(f"https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_{nam}_{ten}.csv", tep)
            _ghi_nhat_ky({"tep": tep.name, "sha256": sha256(tep), "tai_luc": datetime.now(UTC).isoformat(timespec="seconds")})
            ra.append(tep)
    return ra


def tai_thoi_tiet_moi(den: datetime | None = None) -> list[Path]:
    """Open-Meteo Previous Runs từ 1/1/2026 tới hôm nay + 15 ngày (giới hạn của API; cột thuc của giờ tương lai = dự báo mới
    nhất). Nộp sớm hơn mốc tối đa 8 ngày thì vẫn đủ 168 giờ."""
    den = den or datetime.now(UTC)
    ra = []
    for v, (_, lat, lon) in VUNG.items():
        tep = MOI / f"thoi-tiet-{v}-2026.csv"
        url = ("https://previous-runs-api.open-meteo.com/v1/forecast?"
               f"latitude={lat}&longitude={lon}&start_date=2026-01-01&end_date={(den + pd.Timedelta(days=15)).date()}"
               f"&hourly={','.join(BIEN)}&timezone=UTC&format=csv")
        _tai(url, tep)
        _ghi_nhat_ky({"tep": tep.name, "sha256": sha256(tep), "tai_luc": datetime.now(UTC).isoformat(timespec="seconds")})
        ra.append(tep)
    return ra


def thoi_tiet_tuan_toi(thoi_tiet: pd.DataFrame, moc: pd.Timestamp, tai_luc: datetime) -> pd.DataFrame:
    """Lúc nộp thật: nhiệt độ cho 168 giờ sau mốc là dự báo MỚI NHẤT đã tải (cột thuc của giờ tương lai = lượt chạy
    gần nhất trước giờ tải). Chỉ hợp lệ khi tải trước mốc."""
    if pd.Timestamp(tai_luc).tz_localize(None) >= pd.Timestamp(moc):
        raise ValueError(f"thời tiết tải lúc {tai_luc} — phải tải TRƯỚC mốc {moc}")
    t = thoi_tiet[(thoi_tiet["ds"] > moc) & (thoi_tiet["ds"] <= pd.Timestamp(moc) + pd.Timedelta(hours=H))]
    return t[["vung", "ds", "thuc"]].rename(columns={"thuc": "nhiet_do"}).reset_index(drop=True)

