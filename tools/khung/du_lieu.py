"""Đọc dữ liệu của buổi — chỉ từ lab/du-lieu/raw/ đã kiểm sha256 bởi `python lab.py up`.

    from tv import du_lieu
    du_lieu.danh_sach()                           # các bộ trong lab/00-nen/du-lieu.toml
    du_lieu.duong_dan("uci-bike-sharing", "hour.csv")
    du_lieu.doc_tho("uci-bike-sharing", "hour.csv")   # DataFrame nguyên trạng
    du_lieu.doc_du_lieu("monash-m4-hourly")           # dạng dài unique_id, ds, y

`doc_du_lieu` trả dạng dài khi bộ dữ liệu là tệp .tsf (Monash) hoặc danh mục có khai `dang_dai`:
    dang_dai = { tep = "hour.csv", ds = "dteday", gio = "hr", y = "cnt", id = "bike" }
        tep       tệp trong thư mục bộ dữ liệu
        ds        cột thời gian; `gio` (tuỳ chọn) cột giờ cộng thêm vào ds
        y         cột giá trị
        cot_id    cột định danh chuỗi, HOẶC id = hằng số khi chỉ có một chuỗi
        doc       tham số thêm cho pandas.read_csv (vd { sep = ";", na_values = ["?"] })

Làm sạch là việc của bài học: hàm này KHÔNG điền thiếu, không bỏ ngoại lai, không đổi múi giờ.
Chỉ cần numpy và pandas (+ pyarrow cho parquet, openpyxl cho xlsx nếu buổi dùng).
"""
from __future__ import annotations

import os
import tomllib
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

__all__ = ["thu_muc_nen", "danh_sach", "thong_tin", "thu_muc", "duong_dan", "doc_tho",
           "doc_tsf", "doc_du_lieu", "kiem_dang_dai"]

DUOI_DU_LIEU = (".csv", ".csv.gz", ".tsv", ".parquet", ".xlsx", ".xls", ".json", ".tsf", ".txt")


def thu_muc_nen() -> Path:
    """lab/00-nen của buổi. Ghi đè bằng biến môi trường KHOA_FORECASTING_NEN (dùng khi test)."""
    ghi_de = os.environ.get("KHOA_FORECASTING_NEN")
    return Path(ghi_de) if ghi_de else Path(__file__).resolve().parent.parent


def _cau_hinh() -> dict[str, dict]:
    toml = thu_muc_nen() / "du-lieu.toml"
    if not toml.is_file():
        raise FileNotFoundError(f"không thấy {toml} — nền của buổi chưa được sinh")
    with open(toml, "rb") as f:
        return {bo["ten"]: bo for bo in tomllib.load(f).get("bo", [])}


def danh_sach() -> list[str]:
    return sorted(_cau_hinh())


def thong_tin(ten: str) -> dict:
    """Mục của bộ dữ liệu trong du-lieu.toml (URL, giấy phép, khoảng thời gian…)."""
    cau_hinh = _cau_hinh()
    if ten not in cau_hinh:
        raise KeyError(f"buổi này không có bộ '{ten}'. Có: {', '.join(sorted(cau_hinh)) or '(không có)'}")
    return cau_hinh[ten]


def thu_muc(ten: str) -> Path:
    thong_tin(ten)
    p = thu_muc_nen().parent / "du-lieu" / "raw" / ten
    if not (p / ".da-kiem").is_file():
        raise FileNotFoundError(f"chưa có dữ liệu '{ten}' đã kiểm sha256 ở {p} — chạy: python lab.py up (trong lab/)")
    return p


def duong_dan(ten: str, tep: str | None = None) -> Path:
    goc = thu_muc(ten)
    if tep is not None:
        p = goc / tep
        if not p.is_file():
            co = sorted(x.relative_to(goc).as_posix() for x in goc.rglob("*") if x.is_file())
            raise FileNotFoundError(f"bộ '{ten}' không có tệp {tep}. Có: {co}")
        return p
    ung_vien = sorted(x for x in goc.rglob("*") if x.is_file() and x.name.lower().endswith(DUOI_DU_LIEU)
                      and x.name != "NGUON.txt")
    if len(ung_vien) != 1:
        raise ValueError(f"bộ '{ten}' có {len(ung_vien)} tệp dữ liệu — chỉ rõ tep=: "
                         f"{[x.relative_to(goc).as_posix() for x in ung_vien]}")
    return ung_vien[0]


def doc_tho(ten: str, tep: str | None = None, **kwargs) -> pd.DataFrame:
    """Đọc nguyên trạng theo đuôi tệp. .tsf trả dạng dài (xem doc_tsf)."""
    p = duong_dan(ten, tep)
    duoi = p.name.lower()
    if duoi.endswith(".tsf"):
        return doc_tsf(p, **kwargs)[0]
    if duoi.endswith((".csv", ".csv.gz", ".txt")):
        return pd.read_csv(p, **kwargs)
    if duoi.endswith(".tsv"):
        return pd.read_csv(p, sep="\t", **kwargs)
    if duoi.endswith(".parquet"):
        return pd.read_parquet(p, **kwargs)
    if duoi.endswith((".xlsx", ".xls")):
        return pd.read_excel(p, **kwargs)
    if duoi.endswith(".json"):
        return pd.read_json(p, **kwargs)
    raise ValueError(f"chưa hỗ trợ đọc {p.name}")


# ---------------------------------------------------------------------------- Monash .tsf

_BUOC_TSF = {
    "yearly": pd.DateOffset(years=1), "quarterly": pd.DateOffset(months=3),
    "monthly": pd.DateOffset(months=1), "weekly": pd.DateOffset(weeks=1),
    "daily": pd.Timedelta(days=1), "hourly": pd.Timedelta(hours=1),
    "half_hourly": pd.Timedelta(minutes=30), "30_minutes": pd.Timedelta(minutes=30),
    "15_minutes": pd.Timedelta(minutes=15), "10_minutes": pd.Timedelta(minutes=10),
    "minutely": pd.Timedelta(minutes=1), "4_seconds": pd.Timedelta(seconds=4),
}


def doc_tsf(p: str | Path, gioi_han_chuoi: int | None = None) -> tuple[pd.DataFrame, dict]:
    """Đọc định dạng .tsf của Monash Time Series Forecasting Repository.

    Trả (DataFrame dạng dài unique_id, ds, y, metadata). '?' là giá trị thiếu (NaN).
    Có thuộc tính start_timestamp và tần suất đã biết → ds là thời gian (bước theo lịch, giữ đúng
    ngày bắt đầu); không có → ds là số thứ tự 0, 1, 2… Thuộc tính khác của chuỗi thành cột thêm.
    """
    p = Path(p)
    thuoc_tinh: list[tuple[str, str]] = []
    meta: dict[str, str] = {}
    dong_du_lieu: list[str] = []
    with open(p, encoding="latin-1") as f:  # tệp Monash dùng latin-1 ở một số bộ
        trong_du_lieu = False
        for dong in f:
            dong = dong.strip()
            if not dong or dong.startswith("#"):
                continue
            if trong_du_lieu:
                dong_du_lieu.append(dong)
                if gioi_han_chuoi and len(dong_du_lieu) >= gioi_han_chuoi:
                    break
                continue
            if dong.lower().startswith("@attribute"):
                _, ten, kieu = dong.split(maxsplit=2)
                thuoc_tinh.append((ten, kieu))
            elif dong.lower() == "@data":
                trong_du_lieu = True
            elif dong.startswith("@"):
                khoa, _, gia_tri = dong[1:].partition(" ")
                meta[khoa.lower()] = gia_tri.strip()
    if not thuoc_tinh:
        raise ValueError(f"{p.name} không phải tệp .tsf hợp lệ (không có @attribute)")

    tan_suat = meta.get("frequency")
    buoc = _BUOC_TSF.get(tan_suat) if tan_suat else None
    cac_khung = []
    for so, dong in enumerate(dong_du_lieu):
        phan = dong.split(":")
        if len(phan) != len(thuoc_tinh) + 1:
            raise ValueError(f"{p.name}: dòng dữ liệu {so + 1} có {len(phan) - 1} thuộc tính, cần {len(thuoc_tinh)}")
        gia_tri = np.array([np.nan if v == "?" else float(v) for v in phan[-1].split(",")])
        tt = dict(zip([t for t, _ in thuoc_tinh], phan[:-1], strict=True))
        uid = tt.pop("series_name", f"T{so + 1}")
        bat_dau = tt.pop("start_timestamp", None)
        if bat_dau is not None and buoc is not None:
            t0 = pd.Timestamp(datetime.strptime(bat_dau, "%Y-%m-%d %H-%M-%S"))
            if isinstance(buoc, pd.Timedelta):
                ds = pd.date_range(t0, periods=len(gia_tri), freq=buoc)
            else:
                ds = pd.DatetimeIndex([t0 + i * buoc for i in range(len(gia_tri))])
        else:
            ds = np.arange(len(gia_tri))
        khung = pd.DataFrame({"unique_id": uid, "ds": ds, "y": gia_tri})
        for k, v in tt.items():
            khung[k] = v
        cac_khung.append(khung)
    df = pd.concat(cac_khung, ignore_index=True) if cac_khung else pd.DataFrame(columns=["unique_id", "ds", "y"])
    meta["thuoc_tinh"] = ", ".join(f"{t} {k}" for t, k in thuoc_tinh)
    return df, meta


# ---------------------------------------------------------------------------- dạng dài


def kiem_dang_dai(df: pd.DataFrame, cot_id: str = "unique_id", cot_ds: str = "ds", cot_y: str = "y") -> None:
    """Báo lỗi nếu không đúng dạng dài: thiếu cột, trùng (unique_id, ds), y không phải số."""
    thieu = [c for c in (cot_id, cot_ds, cot_y) if c not in df.columns]
    if thieu:
        raise ValueError(f"thiếu cột {thieu}")
    trung = df.duplicated([cot_id, cot_ds])
    if trung.any():
        vi_du = df.loc[trung, [cot_id, cot_ds]].head(3).to_dict("records")
        raise ValueError(f"{int(trung.sum())} dòng trùng ({cot_id}, {cot_ds}), ví dụ {vi_du}")
    if not pd.api.types.is_numeric_dtype(df[cot_y]):
        raise ValueError(f"cột {cot_y} không phải số ({df[cot_y].dtype})")


def doc_du_lieu(ten: str, tep: str | None = None, **kwargs) -> pd.DataFrame:
    """Dữ liệu dạng dài unique_id, ds, y (sắp theo unique_id, ds)."""
    bo = thong_tin(ten)
    spec = bo.get("dang_dai")
    if spec is None:
        p = duong_dan(ten, tep)
        if not p.name.lower().endswith(".tsf"):
            raise ValueError(f"bộ '{ten}' không có khai báo dang_dai trong danh mục — dùng doc_tho() rồi tự "
                             "chuyển sang dạng dài")
        df = doc_tsf(p, **kwargs)[0]
    else:
        tho = doc_tho(ten, tep or spec["tep"], **{**spec.get("doc", {}), **kwargs})
        ds = pd.to_datetime(tho[spec["ds"]])
        if "gio" in spec:
            ds = ds + pd.to_timedelta(tho[spec["gio"]], unit="h")
        if "cot_id" in spec:
            uid = tho[spec["cot_id"]].astype(str)
        elif "id" in spec:
            uid = spec["id"]
        else:
            raise ValueError(f"dang_dai của '{ten}' cần cot_id hoặc id")
        df = pd.DataFrame({"unique_id": uid, "ds": ds, "y": pd.to_numeric(tho[spec["y"]], errors="raise")})
    kiem_dang_dai(df)
    return df.sort_values(["unique_id", "ds"], ignore_index=True)
