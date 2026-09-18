# %% [markdown]
# # Buổi 3 — Dữ liệu thời gian: gom số chuyến taxi theo giờ và ghép thời tiết
#
# Code chạy được, ra bảng trông ổn. Nhưng có vài chỗ về THỜI GIAN chưa đúng — tìm ra chúng.

# %%
from __future__ import annotations

import numpy as np
import pandas as pd

import tv

MUI_GIO_NYC = "America/New_York"


def chuan_hoa_thoi_gian(df: pd.DataFrame, cot_thoi_gian: str, cot_gia_tri: str, tan_suat: str = "h",
                        mui_gio_nguon: str = "UTC", cot_id: str | None = None, gop: str = "sum",
                        mo_ho="raise", dien: float | None = None, bo_trung: bool | None = None,
                        khoang: tuple | None = None) -> pd.DataFrame:
    """Dữ liệu thô → bảng dạng dài `unique_id, ds, y`: ds là UTC có múi giờ, đủ mọi mốc, không trùng.

    ĐẶC TẢ (bản trong code/ chưa làm đúng — xem tai-lieu.md, Lab bước 4):
    tan_suat: tần suất kết quả, mã pandas ("h", "D"…).
    mui_gio_nguon: múi giờ của cột thời gian KHI nó không ghi múi giờ (naive); cột đã có offset thì bỏ qua.
    cot_id: cột tên chuỗi; None = một chuỗi tên "chuoi".
    gop: "sum"/"count" cho số lượng/sự kiện (số chuyến, kWh), "mean"/"last" cho trạng thái (nhiệt độ).
    mo_ho: xử lý giờ lặp khi trả giờ mùa hè — "raise", "infer", "NaT", hoặc mảng bool (True = giờ mùa hè).
    dien: giá trị cho mốc không có dữ liệu; None = 0 với sum/count, NaN với mean/last. Mốc UTC mà dòng
        giờ mơ hồ (mo_ho="NaT") có thể thuộc về luôn là NaN — "không biết", khác "không có".
    bo_trung: bỏ dòng trùng hệt (cùng chuỗi, cùng thời điểm, cùng giá trị); None = bật cho mean/last,
        tắt cho sum/count (hai chuyến cùng giây là hai chuyến thật).
    khoang: (bắt đầu, kết thúc) UTC — mọi chuỗi dùng CHUNG lưới [bắt đầu, kết thúc); None = mỗi chuỗi từ
        mốc đầu tới mốc cuối của chính nó.
    df.attrs của kết quả ghi số dòng bị bỏ vì giờ không tồn tại/mơ hồ và số dòng trùng.
    """
    bang = pd.DataFrame({
        "unique_id": df[cot_id].astype(str).to_numpy() if cot_id else "chuoi",
        "ds": pd.to_datetime(df[cot_thoi_gian]).to_numpy(),
        "y": pd.to_numeric(df[cot_gia_tri], errors="coerce").to_numpy(),
    })
    gia_tri_dien = dien if dien is not None else (0.0 if gop in ("sum", "count") else np.nan)
    ket_qua = []
    for uid, g in bang.groupby("unique_id", sort=True):
        s = g.set_index("ds")["y"].sort_index().resample(tan_suat).agg(gop)
        if gop in ("sum", "count"):
            s = s.fillna(gia_tri_dien)
        ket_qua.append(pd.DataFrame({"unique_id": uid, "ds": s.index, "y": s.to_numpy(dtype=float)}))
    return pd.concat(ket_qua, ignore_index=True)


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
    """Số chuyến mỗi giờ."""
    return chuan_hoa_thoi_gian(chuyen.assign(mot=1), "tpep_pickup_datetime", "mot", "h",
                               cot_id="PULocationID" if theo_khu_vuc else None, gop="sum")


def doc_thoi_tiet() -> pd.DataFrame:
    """Thời tiết Open-Meteo theo giờ; 3 dòng đầu là metadata ô lưới."""
    p = tv.THU_MUC_DU_LIEU / "open-meteo-new-york-2024-03-11" / "open-meteo-new-york-2024-03-11-utc.csv"
    w = pd.read_csv(p, skiprows=3)
    w.columns = ["time", "nhiet_do", "mua", "mua_rao", "tuyet"]
    w["ds"] = pd.to_datetime(w["time"])
    return w.drop(columns="time")


def ghep_thoi_tiet(dem: pd.DataFrame, thoi_tiet: pd.DataFrame) -> pd.DataFrame:
    """Ghép số chuyến theo giờ với thời tiết cùng giờ."""
    return dem.merge(thoi_tiet, on="ds", how="inner")


def gio_nong_nhat(ghep: pd.DataFrame, mui_gio: str = MUI_GIO_NYC) -> int:
    """Giờ trong ngày có nhiệt độ trung bình cao nhất."""
    gio = ghep["ds"].dt.hour
    return int(ghep.groupby(gio)["nhiet_do"].mean().idxmax())


# %%
if __name__ == "__main__":
    chuyen = doc_chuyen_taxi("03")
    dem = dem_chuyen_theo_gio(chuyen)
    print(len(chuyen), "chuyến →", len(dem), "giờ")
    ghep = ghep_thoi_tiet(dem, doc_thoi_tiet())
    print("giờ nóng nhất:", gio_nong_nhat(ghep))
