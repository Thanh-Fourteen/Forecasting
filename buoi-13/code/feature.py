# %% [markdown]
# # Buổi 13 — Feature engineering và chống rò rỉ
#
# Điểm xuất phát (có chỗ cố tình sai). Dữ liệu: doanh số bán lẻ (UCI Online Retail II), lượt xem vi.wikipedia,
# phụ tải điện ERCOT + dự báo của chính nhà vận hành (EIA-930), nhiệt độ Dallas thật và
# **bản dự báo đã lưu** (Open-Meteo Previous Runs).

# %%
from __future__ import annotations

import math
import warnings
from datetime import date

import holidays
import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

TAM = 1  # tầm dự báo mặc định: 1 bước. Mọi feature cho y_t chỉ được dùng dữ liệu tới t - TAM.


# %% [markdown]
# ## Âm lịch Việt Nam — thuật toán Meeus ở kinh tuyến 105°Đ
#
# Tự viết, không phụ thuộc thư viện ngoài. Múi giờ là tham số: 7 cho Việt Nam, 8 cho Trung Quốc —
# đúng chỗ làm Tết hai nước lệch nhau (2007, 2030).

# %%
def jd_tu_ngay(dd: int, mm: int, yy: int) -> int:
    """Số ngày Julius của một ngày dương lịch."""
    a = (14 - mm) // 12
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    if jd < 2299161:  # trước 15/10/1582: lịch Julius
        jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083
    return jd


def ngay_tu_jd(jd: int) -> tuple[int, int, int]:
    if jd > 2299160:
        a = jd + 32044
        b = (4 * a + 3) // 146097
        c = a - (b * 146097) // 4
    else:
        b, c = 0, jd + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    return e - (153 * m + 2) // 5 + 1, m + 3 - 12 * (m // 10), b * 100 + d - 4800 + m // 10


def _soc(k: int) -> float:
    """Thời điểm sóc (trăng mới) thứ k tính từ 1900-01-01, theo Meeus ch. 49 (JD, giờ UTC)."""
    t = k / 1236.85
    t2, t3 = t * t, t * t * t
    dr = math.pi / 180
    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * t2 - 0.000000155 * t3
    jd1 += 0.00033 * math.sin((166.56 + 132.87 * t - 0.009173 * t2) * dr)
    m = 359.2242 + 29.10535608 * k - 0.0000333 * t2 - 0.00000347 * t3
    mpr = 306.0253 + 385.81691806 * k + 0.0107306 * t2 + 0.00001236 * t3
    f = 21.2964 + 390.67050646 * k - 0.0016528 * t2 - 0.00000239 * t3
    c1 = (0.1734 - 0.000393 * t) * math.sin(m * dr) + 0.0021 * math.sin(2 * dr * m)
    c1 -= 0.4068 * math.sin(mpr * dr) + 0.0161 * math.sin(2 * dr * mpr)
    c1 -= 0.0004 * math.sin(3 * dr * mpr)
    c1 += 0.0104 * math.sin(2 * dr * f) - 0.0051 * math.sin((m + mpr) * dr)
    c1 -= 0.0074 * math.sin((m - mpr) * dr) + 0.0004 * math.sin((2 * f + m) * dr)
    c1 -= 0.0004 * math.sin((2 * f - m) * dr) - 0.0006 * math.sin((2 * f + mpr) * dr)
    c1 += 0.0010 * math.sin((2 * f - mpr) * dr) + 0.0005 * math.sin((2 * mpr + m) * dr)
    if t < -11:
        dt = 0.001 + 0.000839 * t + 0.0002261 * t2 - 0.00000845 * t3 - 0.000000081 * t * t3
    else:
        dt = -0.000278 + 0.000265 * t + 0.000262 * t2
    return jd1 + c1 - dt


def _kinh_do_mat_troi(jdn: float) -> float:
    t = (jdn - 2451545.0) / 36525
    t2 = t * t
    dr = math.pi / 180
    m = 357.52910 + 35999.05030 * t - 0.0001559 * t2 - 0.00000048 * t * t2
    l0 = 280.46645 + 36000.76983 * t + 0.0003032 * t2
    dl = (1.914600 - 0.004817 * t - 0.000014 * t2) * math.sin(dr * m)
    dl += (0.019993 - 0.000101 * t) * math.sin(dr * 2 * m) + 0.000290 * math.sin(dr * 3 * m)
    lam = (l0 + dl) * dr
    return lam - math.pi * 2 * int(lam / (math.pi * 2))


def _cung_mat_troi(so_ngay: int, mui_gio: int) -> int:
    return int(_kinh_do_mat_troi(so_ngay - 0.5 - mui_gio / 24.0) / math.pi * 6)


def _ngay_soc(k: int, mui_gio: int) -> int:
    return int(_soc(k) + 0.5 + mui_gio / 24.0)


def _thang_11(yy: int, mui_gio: int) -> int:
    off = jd_tu_ngay(31, 12, yy) - 2415021
    k = int(off / 29.530588853)
    nm = _ngay_soc(k, mui_gio)
    if _cung_mat_troi(nm, mui_gio) >= 9:
        nm = _ngay_soc(k - 1, mui_gio)
    return nm


def _thang_nhuan(a11: int, mui_gio: int) -> int:
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1
    arc = _cung_mat_troi(_ngay_soc(k + i, mui_gio), mui_gio)
    while True:
        last = arc
        i += 1
        arc = _cung_mat_troi(_ngay_soc(k + i, mui_gio), mui_gio)
        if arc == last or i >= 14:
            break
    return i - 1


def duong_sang_am(dd: int, mm: int, yy: int, mui_gio: int = 7) -> tuple[int, int, int, int]:
    """Dương lịch → âm lịch: (ngày, tháng, năm, nhuận). `mui_gio` = 7 (VN) hoặc 8 (TQ)."""
    so_ngay = jd_tu_ngay(dd, mm, yy)
    k = int((so_ngay - 2415021.076998695) / 29.530588853)
    dau_thang = _ngay_soc(k + 1, mui_gio)
    if dau_thang > so_ngay:
        dau_thang = _ngay_soc(k, mui_gio)
    a11 = _thang_11(yy, mui_gio)
    b11 = a11
    if a11 >= dau_thang:
        nam_am = yy
        a11 = _thang_11(yy - 1, mui_gio)
    else:
        nam_am = yy + 1
        b11 = _thang_11(yy + 1, mui_gio)
    ngay_am = so_ngay - dau_thang + 1
    chenh = int((dau_thang - a11) / 29)
    nhuan, thang_am = 0, chenh + 11
    if b11 - a11 > 365:
        lech = _thang_nhuan(a11, mui_gio)
        if chenh >= lech:
            thang_am = chenh + 10
            if chenh == lech:
                nhuan = 1
    if thang_am > 12:
        thang_am -= 12
    if thang_am >= 11 and chenh < 4:
        nam_am -= 1
    return ngay_am, thang_am, nam_am, nhuan


def am_sang_duong(ngay: int, thang: int, nam: int, nhuan: int = 0, mui_gio: int = 7):
    """Âm lịch → dương lịch. Trả None nếu tháng nhuận không tồn tại trong năm đó."""
    if thang < 11:
        a11, b11 = _thang_11(nam - 1, mui_gio), _thang_11(nam, mui_gio)
    else:
        a11, b11 = _thang_11(nam, mui_gio), _thang_11(nam + 1, mui_gio)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = thang - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        lech = _thang_nhuan(a11, mui_gio)
        thang_nhuan = (lech - 2) % 12
        if nhuan != 0 and thang != thang_nhuan:
            return None
        if nhuan != 0 or off >= lech:
            off += 1
    dd, mm, yy = ngay_tu_jd(_ngay_soc(k + off, mui_gio) + ngay - 1)
    return date(yy, mm, dd)


def tet(nam: int, mui_gio: int = 7) -> date:
    """Mùng 1 Tết (dương lịch) của năm âm lịch `nam`."""
    return am_sang_duong(1, 1, nam, 0, mui_gio)


def gio_to(nam: int, mui_gio: int = 7) -> date:
    """Giỗ Tổ Hùng Vương: mùng 10 tháng 3 âm lịch."""
    return am_sang_duong(10, 3, nam, 0, mui_gio)


def so_ngay_toi_tet(moc: pd.DatetimeIndex) -> pd.Series:
    """Số ngày tới mùng 1 Tết gần nhất (âm = đã qua Tết). Đây là feature BIẾT TRƯỚC vô hạn."""
    nam = sorted({d.year for d in moc} | {d.year + 1 for d in moc})
    moc_tet = pd.DatetimeIndex([pd.Timestamp(tet(n)) for n in nam])
    ra = []
    for d in moc:
        lech = (moc_tet - d).days.to_numpy()
        ra.append(int(lech[np.argmin(np.abs(lech))]))
    return pd.Series(ra, index=moc, name="so_ngay_toi_tet")


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_ban_le() -> pd.Series:
    """Doanh thu theo NGÀY của Online Retail II (cache parquet vì .xlsx đọc mất ~30 s)."""
    cache = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "doanh_thu_ngay.parquet"
    if cache.exists():
        return pd.read_parquet(cache)["doanh_thu"]
    tep = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "online_retail_II.xlsx"
    khung = pd.concat([pd.read_excel(tep, sheet_name=s) for s in ("Year 2009-2010", "Year 2010-2011")])
    khung = khung[(khung["Quantity"] > 0) & (khung["Price"] > 0)]
    khung["ngay"] = pd.to_datetime(khung["InvoiceDate"]).dt.normalize()
    ngay = khung.assign(dt=khung["Quantity"] * khung["Price"]).groupby("ngay")["dt"].sum()
    ngay = ngay.asfreq("D").rename("doanh_thu")
    pd.DataFrame({"doanh_thu": ngay}).to_parquet(cache)
    return ngay


def doc_wiki() -> pd.Series:
    """Tổng lượt xem vi.wikipedia theo ngày 2016–2025 (dữ liệu có Tết thật)."""
    import json
    tep = tv.THU_MUC_DU_LIEU / "wikipedia-vi-tong" / "vi-wikipedia-tong-2016-2025.json"
    muc = json.loads(tep.read_text(encoding="utf-8"))["items"]
    moc = pd.to_datetime([m["timestamp"][:8] for m in muc], format="%Y%m%d")
    return pd.Series([m["views"] for m in muc], index=moc, name="luot_xem").sort_index()


def doc_dien(ba: str = "ERCO") -> pd.DataFrame:
    """Phụ tải điện theo giờ 2024 + DỰ BÁO CỦA CHÍNH NHÀ VẬN HÀNH (EIA-930).

    Cột `du_bao_van_hanh` là biến biết trước — nó được công bố trước giờ vận hành.
    """
    khung = []
    for thu_muc, ten in (("eia930-balance-2024-h1", "EIA930_BALANCE_2024_Jan_Jun.csv"),
                         ("eia930-balance-2024-h2", "EIA930_BALANCE_2024_Jul_Dec.csv")):
        d = pd.read_csv(tv.THU_MUC_DU_LIEU / thu_muc / ten, low_memory=False)
        khung.append(d[d["Balancing Authority"] == ba])
    d = pd.concat(khung)
    moc = pd.to_datetime(d["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p")
    ra = pd.DataFrame({"phu_tai": pd.to_numeric(d["Demand (MW)"], errors="coerce").to_numpy(),
                       "du_bao_van_hanh": pd.to_numeric(d["Demand Forecast (MW)"], errors="coerce").to_numpy()},
                      index=moc).sort_index()
    return ra[~ra.index.duplicated()].asfreq("h")


def doc_thoi_tiet() -> pd.DataFrame:
    """Nhiệt độ Dallas 2024: giá trị THẬT (ERA5) và bản DỰ BÁO đã lưu trước 1 ngày / 3 ngày.

    `nhiet_do_that` chỉ biết được SAU khi giờ đó trôi qua; `du_bao_1_ngay` là thứ thực sự có
    trong tay lúc ra dự báo.
    """
    tep = tv.THU_MUC_DU_LIEU / "open-meteo-dallas-du-bao-luu-2024" / "open-meteo-dallas-du-bao-luu-2024.csv"
    d = pd.read_csv(tep, skiprows=3)
    ten = {c: c.split(" (")[0] for c in d.columns if " (" in c}
    d = d.rename(columns=ten)
    d["thoi_gian"] = pd.to_datetime(d["time"])
    return d.set_index("thoi_gian").rename(columns={
        "temperature_2m": "nhiet_do_that", "temperature_2m_previous_day1": "du_bao_1_ngay",
        "temperature_2m_previous_day3": "du_bao_3_ngay"})[["nhiet_do_that", "du_bao_1_ngay", "du_bao_3_ngay"]]


# %% [markdown]
# ## Bộ feature — và "biết trước bao lâu"

# %%
# Mỗi feature khai rõ nó cần dữ liệu tới thời điểm nào:
#   "vô hạn"  = lịch, biết trước mãi mãi (thứ, tháng, Tết, Fourier)
#   "t-h"     = chỉ dùng y tới t-h (lag, rolling đã shift)
#   "kế hoạch"= biết trước vì có người công bố (dự báo thời tiết, dự báo phụ tải, khuyến mãi đã lên lịch)
BIET_TRUOC_VO_HAN = "vô hạn"
BIET_TRUOC_TRE = "t-h"
BIET_TRUOC_KE_HOACH = "kế hoạch"


def feature_lich(moc: pd.DatetimeIndex, le_vn: bool = True) -> pd.DataFrame:
    """Feature lịch: biết trước vô hạn, không bao giờ rò rỉ."""
    f = pd.DataFrame(index=moc)
    f["thu"] = moc.dayofweek
    f["ngay_trong_thang"] = moc.day
    f["thang"] = moc.month
    f["tuan_trong_nam"] = moc.isocalendar().week.to_numpy()
    f["cuoi_tuan"] = (moc.dayofweek >= 5).astype(int)
    f["dau_thang"] = (moc.day <= 3).astype(int)
    f["cuoi_thang"] = moc.is_month_end.astype(int)
    # mã hoá tuần hoàn: thứ 7 và chủ nhật phải gần nhau, 12 và 1 cũng vậy
    f["thu_sin"] = np.sin(2 * np.pi * moc.dayofweek / 7)
    f["thu_cos"] = np.cos(2 * np.pi * moc.dayofweek / 7)
    f["thang_sin"] = np.sin(2 * np.pi * moc.month / 12)
    f["thang_cos"] = np.cos(2 * np.pi * moc.month / 12)
    if le_vn:
        nam = sorted({d.year for d in moc})
        le = holidays.country_holidays("VN", years=nam)
        f["le_duong_lich"] = [int(d.date() in le and "Lunar" not in le.get(d.date(), "")) for d in moc]
        ngay_tet = pd.Series((pd.Timestamp("2011-02-03") - moc).days, index=moc)  # Tết 2011
        f["so_ngay_toi_tet"] = ngay_tet
        f["truoc_tet_7"] = ((ngay_tet > 0) & (ngay_tet <= 7)).astype(int)
        f["trong_tet_7"] = (ngay_tet.abs() <= 3).astype(int)
        f["sau_tet_7"] = ((ngay_tet < 0) & (ngay_tet >= -7)).astype(int)
        f["gio_to"] = [int(d.date() == gio_to(d.year)) for d in moc]
    return f


def feature_fourier(moc: pd.DatetimeIndex, chu_ky: float = 365.25, k: int = 3) -> pd.DataFrame:
    """K cặp sin/cos cho mùa vụ dài — 2K cột thay cho 365 biến giả."""
    t = (moc - moc[0]).days.to_numpy().astype(float)
    f = pd.DataFrame(index=moc)
    for i in range(1, k + 1):
        f[f"fourier_sin_{i}"] = np.sin(2 * np.pi * i * t / chu_ky)
        f[f"fourier_cos_{i}"] = np.cos(2 * np.pi * i * t / chu_ky)
    return f


def feature_tre(y: pd.Series, tam: int = TAM, cac_lag=(1, 2, 3, 7, 14, 28),
                cac_cua_so=(7, 28)) -> pd.DataFrame:
    """Lag và rolling. QUY TẮC: lag nhỏ nhất ≥ tầm dự báo, và LUÔN `shift(tam)` TRƯỚC khi `rolling`."""
    f = pd.DataFrame(index=y.index)
    tre = y.shift(tam)
    for lag in cac_lag:
        f[f"lag_{lag}"] = y.shift(max(lag, tam))
    for w in cac_cua_so:
        f[f"tb_{w}"] = y.rolling(w, center=True).mean()
        f[f"sd_{w}"] = tre.rolling(w).std()
        f[f"min_{w}"] = tre.rolling(w).min()
        f[f"max_{w}"] = tre.rolling(w).max()
        f[f"q90_{w}"] = tre.rolling(w).quantile(0.9)
    f["chenh_1"] = tre.diff()
    f["ty_le_tb7_tb28"] = f["tb_7"] / f["tb_28"]
    f["z_score"] = (y - y.mean()) / y.std()
    f["tb_theo_thu"] = y.groupby(y.index.dayofweek).transform("mean")
    f["y_dien_hai_chieu"] = y.interpolate(limit_direction="both")
    return f


def bo_feature(y: pd.Series, tam: int = TAM, ngoai_sinh: pd.DataFrame | None = None,
               le_vn: bool = True) -> pd.DataFrame:
    """Bộ feature đầy đủ cho chuỗi `y`. Mọi cột chỉ dùng thông tin có tại thời điểm ra dự báo."""
    phan = [feature_tre(y, tam), feature_lich(y.index, le_vn), feature_fourier(y.index)]
    if ngoai_sinh is not None:
        phan.append(ngoai_sinh.reindex(y.index))
    return pd.concat(phan, axis=1)


def bang_biet_truoc(f: pd.DataFrame) -> pd.DataFrame:
    """Mỗi feature khai 'biết trước bao lâu' — bảng này phải nộp cùng mô hình."""
    hang = []
    for cot in f.columns:
        if cot.startswith(("lag_", "tb_", "sd_", "min_", "max_", "q90_", "chenh_", "ty_le_")):
            loai = BIET_TRUOC_TRE
        elif cot.startswith(("du_bao_", "khuyen_mai")):
            loai = BIET_TRUOC_KE_HOACH
        elif cot.startswith("nhiet_do_that") or cot.endswith("_that"):
            loai = "KHÔNG BIẾT TRƯỚC"
        else:
            loai = BIET_TRUOC_VO_HAN
        hang.append({"feature": cot, "biết trước": loai})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Bài kiểm rò rỉ tự viết: cắt tương lai rồi tính lại

# %%
def kiem_ro_ri(ham_feature, y: pd.Series, cac_moc=None, sai_so: float = 1e-9) -> pd.DataFrame:
    """Tính feature trên dữ liệu ĐẦY ĐỦ và trên dữ liệu CẮT tại mốc T; so mọi dòng ≤ T.

    Feature nhân quả cho kết quả y hệt; feature rò rỉ đổi giá trị ở quá khứ khi biết thêm tương lai.
    """
    day_du = ham_feature(y)
    if cac_moc is None:
        cac_moc = [y.index[int(len(y) * 0.9)]]
    hang = []
    for moc in cac_moc:
        cat = ham_feature(y[y.index <= moc])
        chung = day_du.index[day_du.index <= moc][:-10]  # bỏ 10 dòng cuối cho chắc
        for cot in day_du.columns:
            a = day_du.loc[chung, cot]
            b = cat.reindex(chung)[cot] if cot in cat.columns else pd.Series(np.nan, index=chung)
            khac = ~(np.isclose(a.to_numpy(dtype=float), b.to_numpy(dtype=float),
                                rtol=0, atol=sai_so, equal_nan=True))
            if khac.any():
                hang.append({"feature": cot, "mốc cắt": moc, "số dòng đổi": int(khac.sum()),
                             "lệch lớn nhất": float(np.nanmax(np.abs(a.to_numpy(float) - b.to_numpy(float))))})
    bang = pd.DataFrame(hang)
    if bang.empty:
        return pd.DataFrame(columns=["feature", "mốc cắt", "số dòng đổi", "lệch lớn nhất"])
    return bang.groupby("feature", as_index=False).agg(
        so_moc_bi_bat=("mốc cắt", "count"), so_dong_doi=("số dòng đổi", "max"),
        lech_lon_nhat=("lệch lớn nhất", "max"))


def kiem_nhieu_muc_tieu(ham_feature, y: pd.Series, tam: int = TAM, seed: int = 0) -> list[str]:
    """Bài kiểm thứ hai: đổi y từ 70% chuỗi trở đi. Feature cho y_t với t − tam < mốc (thời điểm ra dự báo
    còn trước mốc) không được đổi.

    Bắt được kiểu rò rỉ mà bài cắt-tương-lai bỏ sót: feature dùng lag < tầm dự báo.
    """
    rng = np.random.default_rng(seed)
    cat = int(len(y) * 0.7)
    y2 = y.copy()
    y2.iloc[cat:] = y2.iloc[cat:] + rng.normal(0, float(np.nanstd(y)) * 10, len(y) - cat)
    a, b = ham_feature(y), ham_feature(y2)
    giu = a.index[: cat + tam]  # các dòng t < mốc + tam: lúc ra dự báo (t − tam) chưa thấy phần bị đổi
    xau = []
    for cot in a.columns:
        if not np.allclose(a.loc[giu, cot].to_numpy(float), b.loc[giu, cot].to_numpy(float),
                           rtol=0, atol=1e-9, equal_nan=True):
            xau.append(cot)
    return xau


def kiem_scaler(scaler, X_hoc: pd.DataFrame, X_tat_ca: pd.DataFrame, sai_so: float = 1e-9) -> bool:
    """Scaler phải fit CHỈ trên phần học: trung bình của nó phải khớp X_hoc, không khớp X_tat_ca."""
    tb = np.asarray(getattr(scaler, "mean_", np.nan), dtype=float)
    return bool(np.allclose(tb, X_hoc.mean().to_numpy(float), rtol=0, atol=sai_so))


# %% [markdown]
# ## Cái giá của rò rỉ: nhiệt độ THẬT so với nhiệt độ ĐÃ DỰ BÁO

# %%
def _hoi_quy(X_hoc, y_hoc, X_kiem):
    A = np.column_stack([np.ones(len(X_hoc)), np.asarray(X_hoc, dtype=float)])
    he_so = np.linalg.lstsq(A, np.asarray(y_hoc, dtype=float), rcond=None)[0]
    B = np.column_stack([np.ones(len(X_kiem)), np.asarray(X_kiem, dtype=float)])
    return B @ he_so


def gia_cua_ro_ri(ty_le_hoc: float = 0.7, tam: int = 24) -> pd.DataFrame:
    """Dự báo phụ tải ERCOT **24 giờ tới** (day-ahead) bằng các bộ feature nhiệt độ khác nhau.

    Tầm 24 giờ mới là bài toán thật: ở tầm 1 giờ, `lag_1` giải thích gần hết và nhiệt độ không
    thêm được gì — đo được MAE 846,2 (chỉ lag) so với 847,7 (thêm nhiệt độ thật).

    - "nhiệt độ thật": **rò rỉ** — lúc ra dự báo chưa ai biết nhiệt độ của 24 giờ sau;
    - "dự báo 1 ngày" / "dự báo 3 ngày": thứ thật sự có trong tay (Open-Meteo Previous Runs).
    """
    dien, tt = doc_dien(), doc_thoi_tiet()
    d = dien.join(tt, how="inner").dropna(subset=["phu_tai"])
    d["muc_tieu"] = d["phu_tai"].shift(-tam)
    d["lag_24"] = d["phu_tai"]
    d["lag_168"] = d["phu_tai"].shift(144)
    d["gio_sin"] = np.sin(2 * np.pi * d.index.hour / 24)
    d["gio_cos"] = np.cos(2 * np.pi * d.index.hour / 24)
    # nhiệt độ ở ĐÚNG giờ cần dự báo (t + tam), theo từng nguồn thông tin
    for cot in ("nhiet_do_that", "du_bao_1_ngay", "du_bao_3_ngay"):
        d[f"{cot}_muc_tieu"] = d[cot].shift(-tam)
    cot_nen = ["lag_24", "lag_168", "gio_sin", "gio_cos"]

    hang = []
    for ten, cot in (("chỉ lag + giờ", cot_nen),
                     ("+ nhiệt độ THẬT của giờ cần dự báo (rò rỉ)", cot_nen + ["nhiet_do_that_muc_tieu"]),
                     ("+ dự báo nhiệt độ trước 1 ngày", cot_nen + ["du_bao_1_ngay_muc_tieu"]),
                     ("+ dự báo nhiệt độ trước 3 ngày", cot_nen + ["du_bao_3_ngay_muc_tieu"]),
                     ("+ nhiệt độ HIỆN TẠI (nhân quả)", cot_nen + ["nhiet_do_that"])):
        bang = d[cot + ["muc_tieu"]].dropna()
        cat = int(len(bang) * ty_le_hoc)
        hoc, kiem = bang.iloc[:cat], bang.iloc[cat:]
        du_bao = _hoi_quy(hoc[cot], hoc["muc_tieu"], kiem[cot])
        mae = float(np.mean(np.abs(du_bao - kiem["muc_tieu"].to_numpy(float))))
        hang.append({"bộ feature": ten, "MAE (MW)": mae, "số dòng kiểm": len(kiem),
                     "dùng tương lai?": "nhiet_do_that_muc_tieu" in cot})
    # Kịch bản THẬT SỰ xảy ra khi rò rỉ lọt lưới: huấn luyện bằng nhiệt độ THẬT (vì lịch sử có sẵn),
    # nhưng lúc chạy production chỉ có DỰ BÁO. Mô hình chưa từng thấy sai số của dự báo.
    cot_hoc = cot_nen + ["nhiet_do_that_muc_tieu"]
    for nhan, nguon in (("dự báo 1 ngày", "du_bao_1_ngay_muc_tieu"), ("dự báo 3 ngày", "du_bao_3_ngay_muc_tieu")):
        bang_hai = d[cot_hoc + [nguon, "muc_tieu"]].dropna()
        cat = int(len(bang_hai) * ty_le_hoc)
        hoc, kiem = bang_hai.iloc[:cat], bang_hai.iloc[cat:]
        du_bao = _hoi_quy(hoc[cot_hoc], hoc["muc_tieu"], kiem[cot_nen + [nguon]])
        hang.append({"bộ feature": f"huấn luyện bằng nhiệt độ thật, CHẠY bằng {nhan}",
                     "MAE (MW)": float(np.mean(np.abs(du_bao - kiem["muc_tieu"].to_numpy(float)))),
                     "số dòng kiểm": len(kiem), "dùng tương lai?": True})

    bang = pd.DataFrame(hang)
    nen = float(bang.loc[bang["bộ feature"] == "chỉ lag + giờ", "MAE (MW)"].iloc[0])
    bang["so với chỉ lag (%)"] = (bang["MAE (MW)"] / nen - 1) * 100
    return bang


def sai_so_du_bao_thoi_tiet() -> dict[str, float]:
    """Dự báo thời tiết sai bao nhiêu — đây là lý do 'nhiệt độ thật' cho kết quả đẹp giả."""
    tt = doc_thoi_tiet().dropna()
    return {"MAE dự báo 1 ngày (°C)": round(float((tt["du_bao_1_ngay"] - tt["nhiet_do_that"]).abs().mean()), 3),
            "MAE dự báo 3 ngày (°C)": round(float((tt["du_bao_3_ngay"] - tt["nhiet_do_that"]).abs().mean()), 3),
            "số giờ": int(len(tt))}


def gia_tri_feature_tet(ty_le_hoc: float = 0.7) -> pd.DataFrame:
    """Feature Tết âm lịch đáng giá bao nhiêu trên lượt xem vi.wikipedia?"""
    y = doc_wiki()
    ket = {}
    for ten, le_vn, dung_tet in (("chỉ lag + lịch dương", True, False), ("+ feature Tết âm lịch", True, True)):
        f = bo_feature(y, le_vn=le_vn)
        if not dung_tet:
            f = f.drop(columns=[c for c in f.columns if "tet" in c or "gio_to" in c])
        bang = f.join(y.rename("muc_tieu").shift(-TAM)).dropna()
        cot = [c for c in bang.columns if c != "muc_tieu"]
        cat = int(len(bang) * ty_le_hoc)
        hoc, kiem = bang.iloc[:cat], bang.iloc[cat:]
        du_bao = _hoi_quy(hoc[cot], hoc["muc_tieu"], kiem[cot])
        that = kiem["muc_tieu"].to_numpy(float)
        gan_tet = so_ngay_toi_tet(kiem.index).abs() <= 10
        ket[ten] = {"MAE": float(np.mean(np.abs(du_bao - that))),
                    "MAE quanh Tết (±10 ngày)": float(np.mean(np.abs(du_bao - that)[gan_tet.to_numpy()])),
                    "số feature": len(cot)}
    bang = pd.DataFrame(ket).T.reset_index(names="bộ feature")
    bang["cải thiện quanh Tết (%)"] = (bang["MAE quanh Tết (±10 ngày)"] /
                                       bang["MAE quanh Tết (±10 ngày)"].iloc[0] - 1) * 100
    return bang


# %%
if __name__ == "__main__":
    print("Tết 2000–2035 (VN, múi giờ 7):")
    print(", ".join(f"{n}:{tet(n)}" for n in range(2020, 2036)))
    lech = [n for n in range(2000, 2036) if tet(n, 7) != tet(n, 8)]
    print("năm Tết VN khác Tết Trung Quốc:", {n: (str(tet(n, 7)), str(tet(n, 8))) for n in lech})

    y = doc_ban_le().ffill()
    f = bo_feature(y)
    print("bộ feature:", f.shape[1], "cột")
    print(bang_biet_truoc(f)["biết trước"].value_counts().to_dict())
    print("rò rỉ:", kiem_ro_ri(bo_feature, y).to_string(index=False) or "không có")
    print("nhiễu mục tiêu:", kiem_nhieu_muc_tieu(bo_feature, y))

    print(sai_so_du_bao_thoi_tiet())
    print("Tết trong 2000–2035 (bảng đầy đủ để kiểm chéo):")
    print(", ".join(f"{n}:{tet(n)}" for n in range(2000, 2020)))
    print(gia_cua_ro_ri().round(2).to_string(index=False))
    print(gia_tri_feature_tet().round(1).to_string(index=False))
