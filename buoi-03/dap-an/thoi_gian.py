# %% [markdown]
# # Buổi 3 — Dữ liệu thời gian: chuẩn hoá về UTC, đủ mốc, không trùng
#
# Bản ĐÃ SỬA. Chạy được trên cả pandas 2.3.3 và 3.0.5.

# %%
from __future__ import annotations

import numpy as np
import pandas as pd

import tv

MUI_GIO_NYC = "America/New_York"


def _sang_utc(t: pd.Series, mui_gio_nguon: str, mo_ho) -> pd.Series:
    """Mọi kiểu đầu vào → datetime tz-aware UTC. Giờ không tồn tại (DST) → NaT."""
    if pd.api.types.is_datetime64_any_dtype(t):
        if t.dt.tz is not None:
            return t.dt.tz_convert("UTC")
        return t.dt.tz_localize(mui_gio_nguon, ambiguous=mo_ho, nonexistent="NaT").dt.tz_convert("UTC")
    chuoi = t.astype(str)
    co_offset = chuoi.str.contains(r"(?:Z|[+-]\d{2}:?\d{2})$", regex=True)
    if co_offset.all():
        return pd.to_datetime(chuoi, utc=True)  # pandas 3: offset lẫn lộn mà thiếu utc=True sẽ báo lỗi
    if co_offset.any():
        raise ValueError("cột thời gian lẫn giá trị có offset và không offset — không đoán được múi giờ")
    return _sang_utc(pd.to_datetime(chuoi), mui_gio_nguon, mo_ho)


def _moc_khong_biet(t_goc: pd.Series, bang: pd.DataFrame, mui_gio_nguon: str, tan_suat: str) -> dict:
    """{unique_id: tập mốc UTC} mà dòng bị NaT vì giờ lặp DST có thể rơi vào (cả hai cách hiểu)."""
    mat = bang["ds"].isna().to_numpy()
    if not mat.any() or not pd.api.types.is_datetime64_any_dtype(t_goc) or t_goc.dt.tz is not None:
        return {}
    t = t_goc[mat]
    ra: dict = {}
    for mua_he in (True, False):
        moc = t.dt.tz_localize(mui_gio_nguon, ambiguous=np.full(len(t), mua_he), nonexistent="NaT")
        moc = moc.dt.tz_convert("UTC").dt.floor(tan_suat)
        for uid, m in zip(bang.loc[mat, "unique_id"], moc, strict=True):
            if pd.notna(m):
                ra.setdefault(uid, set()).add(m)
    return ra


def chuan_hoa_thoi_gian(df: pd.DataFrame, cot_thoi_gian: str, cot_gia_tri: str, tan_suat: str = "h",
                        mui_gio_nguon: str = "UTC", cot_id: str | None = None, gop: str = "sum",
                        mo_ho="raise", dien: float | None = None, bo_trung: bool | None = None,
                        khoang: tuple | None = None) -> pd.DataFrame:
    """Dữ liệu thô → bảng dạng dài `unique_id, ds, y`: ds là UTC, đủ mọi mốc, không trùng.

    mui_gio_nguon: múi giờ của cột thời gian KHI nó không ghi múi giờ (naive).
    gop: "sum" cho lưu lượng/sự kiện (số chuyến, kWh), "mean"/"last" cho trạng thái (nhiệt độ).
    mo_ho: xử lý giờ lặp khi trả giờ mùa hè — "raise", "infer", "NaT", hoặc mảng bool (True = giờ mùa hè).
    dien: giá trị cho mốc không có dữ liệu; mặc định 0 với sum/count, NaN với mean/last. Mốc UTC mà dòng
        giờ mơ hồ (mo_ho="NaT") có thể thuộc về luôn là NaN — "không biết", khác "không có".
    bo_trung: bỏ dòng trùng hệt (cùng chuỗi, cùng thời điểm gốc, cùng giá trị) — mặc định BẬT cho dữ liệu
        trạng thái (mean/last: cảm biến gửi lặp) và TẮT cho sự kiện (sum/count: hai chuyến cùng giây là hai
        chuyến thật). Bật cho sum khi biết nguồn xuất trùng (vd tệp nối hai lần).
    khoang: (bắt đầu, kết thúc) UTC — mọi chuỗi dùng CHUNG lưới [bắt đầu, kết thúc); mặc định mỗi chuỗi từ
        mốc đầu tới mốc cuối của chính nó.
    df.attrs của kết quả ghi số dòng bị bỏ vì giờ không tồn tại/mơ hồ và số dòng trùng.
    """
    if gop not in ("sum", "count", "mean", "last"):
        raise ValueError("gop là sum, count, mean hoặc last")
    bang = pd.DataFrame({
        "unique_id": df[cot_id].astype(str).to_numpy() if cot_id else "chuoi",
        "ds": _sang_utc(df[cot_thoi_gian].reset_index(drop=True), mui_gio_nguon, mo_ho),
        "y": pd.to_numeric(df[cot_gia_tri], errors="coerce").to_numpy(),
    })
    so_nat = int(bang["ds"].isna().sum())
    # Giờ mơ hồ bị bỏ (mo_ho="NaT"): mốc UTC mà chúng CÓ THỂ thuộc về là "không biết" → NaN, không phải 0
    khong_biet = _moc_khong_biet(df[cot_thoi_gian].reset_index(drop=True), bang, mui_gio_nguon, tan_suat)
    bang = bang.dropna(subset=["ds"])
    if bo_trung is None:
        bo_trung = gop in ("mean", "last")
    trung = bang.duplicated() if bo_trung else pd.Series(False, index=bang.index)
    so_trung = int(trung.sum())
    bang = bang[~trung]

    bang["ds"] = bang["ds"].dt.floor(tan_suat)
    gop_lai = bang.groupby(["unique_id", "ds"], sort=True)["y"].agg(gop).reset_index()

    gia_tri_dien = dien if dien is not None else (0.0 if gop in ("sum", "count") else np.nan)
    day_du = []
    for uid, g in gop_lai.groupby("unique_id", sort=True):
        dau, cuoi = (g["ds"].min(), g["ds"].max()) if khoang is None else \
            (pd.Timestamp(khoang[0], tz="UTC"), pd.Timestamp(khoang[1], tz="UTC"))
        luoi = pd.date_range(dau, cuoi, freq=tan_suat, tz="UTC", inclusive="left" if khoang else "both")
        if uid in khong_biet:
            luoi = luoi.union(pd.DatetimeIndex(sorted(khong_biet[uid])))
        s = g.set_index("ds")["y"].reindex(luoi, fill_value=gia_tri_dien)
        if uid in khong_biet:
            s.loc[s.index.isin(list(khong_biet[uid]))] = np.nan
        day_du.append(pd.DataFrame({"unique_id": uid, "ds": s.index, "y": s.to_numpy(dtype=float)}))
    ket_qua = pd.concat(day_du, ignore_index=True)
    ket_qua.attrs = {"bo_vi_dst": so_nat, "trung_lap": so_trung}
    return ket_qua


# %%
def doc_chuyen_taxi(thang: str) -> pd.DataFrame:
    """Chuyến taxi vàng NYC của một tháng 2024; bỏ chuyến có giờ đón ngoài tháng của tệp."""
    ten = f"yellow_tripdata_2024-{thang}.parquet"
    df = pd.read_parquet(tv.THU_MUC_DU_LIEU / f"nyc-tlc-yellow-2024-{thang}" / ten,
                         columns=["tpep_pickup_datetime", "PULocationID"])
    dau = pd.Timestamp(f"2024-{thang}-01")
    cuoi = dau + pd.offsets.MonthBegin(1)
    return df[(df["tpep_pickup_datetime"] >= dau) & (df["tpep_pickup_datetime"] < cuoi)]


def dem_chuyen_theo_gio(chuyen: pd.DataFrame, theo_khu_vuc: bool = False) -> pd.DataFrame:
    """Số chuyến mỗi giờ (UTC, đủ mốc). Giờ đón là giờ địa phương New York không ghi múi giờ.

    Giờ lặp khi trả giờ mùa hè không phân biệt được EDT/EST từ giờ đón → đánh NaT và bỏ, số dòng bỏ
    ghi trong attrs (tài liệu buổi nêu con số).
    """
    return chuan_hoa_thoi_gian(chuyen.assign(mot=1), "tpep_pickup_datetime", "mot", "h",
                               mui_gio_nguon=MUI_GIO_NYC, cot_id="PULocationID" if theo_khu_vuc else None,
                               gop="sum", mo_ho="NaT")


def doc_thoi_tiet() -> pd.DataFrame:
    """Open-Meteo đã tải với timezone=UTC; 3 dòng đầu là metadata ô lưới."""
    p = tv.THU_MUC_DU_LIEU / "open-meteo-new-york-2024-03-11" / "open-meteo-new-york-2024-03-11-utc.csv"
    w = pd.read_csv(p, skiprows=3)
    w.columns = ["time", "nhiet_do", "mua", "mua_rao", "tuyet"]
    w["ds"] = pd.to_datetime(w["time"]).dt.tz_localize("UTC")
    return w.drop(columns="time")


def ghep_thoi_tiet(dem: pd.DataFrame, thoi_tiet: pd.DataFrame) -> pd.DataFrame:
    """Ghép số chuyến theo giờ với thời tiết cùng giờ — cả hai phải cùng UTC."""
    for ten, bang in (("dem", dem), ("thoi_tiet", thoi_tiet)):
        if getattr(bang["ds"].dt, "tz", None) is None or str(bang["ds"].dt.tz) != "UTC":
            raise ValueError(f"{ten}.ds phải là thời gian UTC có múi giờ")
    return dem.merge(thoi_tiet, on="ds", how="inner", validate="many_to_one")


def gio_nong_nhat(ghep: pd.DataFrame, mui_gio: str = MUI_GIO_NYC) -> int:
    """Giờ địa phương có nhiệt độ trung bình cao nhất — kiểm tra nhanh việc ghép múi giờ."""
    gio = ghep["ds"].dt.tz_convert(mui_gio).dt.hour
    return int(ghep.groupby(gio)["nhiet_do"].mean().idxmax())


# %%
if __name__ == "__main__":
    chuyen = doc_chuyen_taxi("03")
    dem = dem_chuyen_theo_gio(chuyen)
    print(len(chuyen), "chuyến →", len(dem), "giờ UTC; attrs:", dem.attrs)
    ghep = ghep_thoi_tiet(dem, doc_thoi_tiet())
    print("giờ nóng nhất (giờ New York):", gio_nong_nhat(ghep))
