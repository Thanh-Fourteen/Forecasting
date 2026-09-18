# %% [markdown]
# # Buổi 11 — Ngoại lai và điểm gãy
#
# Điểm xuất phát (có chỗ cố tình sai). Dữ liệu: lượt xem vi.wikipedia (tổng và bài "Tết Nguyên Đán"), hành khách hàng không
# EU27 theo tháng (Eurostat avia_paoc).

# %%
from __future__ import annotations

import json
import warnings

import numpy as np
import pandas as pd
import ruptures as rpt
from statsmodels.tsa.seasonal import STL

import tv

warnings.simplefilter("ignore")

HE_SO_MAD = 1.4826  # đưa MAD về cùng thang với độ lệch chuẩn khi dữ liệu chuẩn


# %% [markdown]
# ## Đọc dữ liệu

# %%
def _doc_pageviews(thu_muc: str, ten_tep: str) -> pd.Series:
    tep = tv.THU_MUC_DU_LIEU / thu_muc / ten_tep
    muc = json.loads(tep.read_text(encoding="utf-8"))["items"]
    moc = pd.to_datetime([m["timestamp"][:8] for m in muc], format="%Y%m%d")
    return pd.Series([m["views"] for m in muc], index=moc, name="views").sort_index()


def doc_tong_vi() -> pd.Series:
    """Tổng lượt xem vi.wikipedia theo ngày, 2016–2025."""
    return _doc_pageviews("wikipedia-vi-tong", "vi-wikipedia-tong-2016-2025.json")


def doc_bai_tet() -> pd.Series:
    """Lượt xem bài 'Tết Nguyên Đán' theo ngày — đỉnh rơi vào Tết ÂM lịch, ngày dương xê dịch."""
    return _doc_pageviews("wikipedia-vi-tet", "tet-nguyen-dan-2016-2025.json")


def doc_hang_khong() -> pd.Series:
    """Hành khách hàng không EU27 theo tháng (Eurostat avia_paoc), 2008-01 → nay."""
    tep = tv.THU_MUC_DU_LIEU / "eurostat-hanh-khach-hang-khong" / "eurostat-avia-paoc-eu27.csv"
    d = pd.read_csv(tep)
    moc = pd.PeriodIndex(d["TIME_PERIOD"], freq="M").to_timestamp()
    return pd.Series(d["OBS_VALUE"].to_numpy(float), index=moc, name="hanh_khach").sort_index()


# %% [markdown]
# ## Phát hiện ngoại lai: z-score, IQR, MAD, Hampel

# %%
def z_score(y: pd.Series, nguong: float = 3.0) -> pd.Series:
    """3σ toàn chuỗi. Chính ngoại lai kéo trung bình và σ lên → nó tự che mình (masking)."""
    z = (y - y.mean()) / y.std()
    return z.abs() > nguong


def iqr(y: pd.Series, he_so: float = 1.5) -> pd.Series:
    """Ngưỡng theo tứ phân vị — bền với ngoại lai hơn z-score, nhưng vẫn là ngưỡng TOÀN CHUỖI."""
    q1, q3 = y.quantile(0.25), y.quantile(0.75)
    rong = q3 - q1
    return (y < q1 - he_so * rong) | (y > q3 + he_so * rong)


def mad_score(y: pd.Series) -> pd.Series:
    """Điểm bền vững: |y - median| / (1.4826 · MAD). Không bị chính ngoại lai kéo lệch."""
    trung_vi = y.median()
    mad = (y - trung_vi).abs().median()
    if mad == 0:
        return pd.Series(0.0, index=y.index)
    return (y - trung_vi).abs() / (HE_SO_MAD * mad)


def hampel(y: pd.Series, cua_so: int = 15, nguong: float = 3.0) -> pd.Series:
    """Bộ lọc Hampel: MAD trên CỬA SỔ TRƯỢT ±`cua_so` điểm.

    Khác z-score ở chỗ mức tham chiếu là mức ĐỊA PHƯƠNG, nên xu hướng và mùa vụ không làm nó mù.
    """
    k = 2 * cua_so + 1
    trung_vi = y.rolling(k, center=True, min_periods=cua_so).median()
    mad = (y - trung_vi).abs().rolling(k, center=True, min_periods=cua_so).median()
    diem = (y - trung_vi).abs() / (HE_SO_MAD * mad.replace(0, np.nan))
    return diem.fillna(0) > nguong


def stl_robust(y: pd.Series, chu_ky: int = 7, nguong: float = 3.0) -> pd.Series:
    """Ngoại lai trên PHẦN DƯ STL robust: bỏ xu hướng và mùa vụ trước khi đặt ngưỡng."""
    kq = STL(y, period=chu_ky, robust=True).fit()
    du = pd.Series(kq.resid, index=y.index)
    return mad_score(du) > nguong


CACH_BAT = {"3σ toàn chuỗi": z_score, "IQR 1,5": iqr,
            "MAD 3 (toàn chuỗi)": lambda y: mad_score(y) > 3.0,
            "Hampel k=15": hampel, "STL robust (tuần)": stl_robust}


def so_sanh_bat(y: pd.Series, cach=None) -> pd.DataFrame:
    """Mỗi cách bắt bao nhiêu điểm, và chúng rơi vào đâu (tháng nào)?"""
    cach = cach or CACH_BAT
    hang = []
    for ten, ham in cach.items():
        co = ham(y).astype(bool)
        thang = pd.Series(co[co].index.month).value_counts()
        hang.append({"cách": ten, "số điểm gắn cờ": int(co.sum()),
                     "tỷ lệ %": round(float(co.mean() * 100), 2),
                     "tháng tập trung nhất": int(thang.index[0]) if len(thang) else -1,
                     "% cờ rơi vào T1/T2/T12": round(float(
                         co[co].index.month.isin([1, 2, 12]).mean() * 100), 1) if co.any() else 0.0})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Ba loại bất thường, và masking/swamping

# %%
def sinh_chuoi_co_loi(n: int = 400, seed: int = 0) -> tuple[pd.Series, dict[str, list[int]]]:
    """Chuỗi mô phỏng có BIẾT trước nhãn: outlier cộng, level shift, thay đổi tạm, thay đổi phương sai."""
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    y = 100 + 0.05 * t + 8 * np.sin(2 * np.pi * t / 7) + rng.normal(0, 2, n)
    nhan = {"outlier_cong": [50, 120, 300], "level_shift": [200], "thay_doi_tam": [260],
            "doi_phuong_sai": [340]}
    y[nhan["outlier_cong"]] += 40
    y[nhan["level_shift"][0]:] += 25
    for i, k in enumerate(range(nhan["thay_doi_tam"][0], nhan["thay_doi_tam"][0] + 20)):
        y[k] += 30 * 0.85 ** i
    y[nhan["doi_phuong_sai"][0]:] += rng.normal(0, 8, n - nhan["doi_phuong_sai"][0])
    moc = pd.date_range("2023-01-01", periods=n, freq="D")
    return pd.Series(y, index=moc), nhan


def _sigma_ben_vung(y: pd.Series) -> float:
    """Ước lượng σ của nhiễu không bị ngoại lai và xu hướng làm hỏng: MAD của sai phân, chia √2."""
    return float(HE_SO_MAD * y.diff().abs().median() / np.sqrt(2))


def dan_nhan(y: pd.Series, cua_so: int = 15, nhin: int = 20) -> pd.DataFrame:
    """Gắn nhãn TỪNG bất thường. Hampel một mình chỉ thấy điểm đơn — phải ghép với điểm gãy.

    - **AO** (outlier cộng): Hampel gắn cờ, mức trước và sau không đổi.
    - **TC** (thay đổi tạm): mức nhảy rồi quay về trong `nhin` bước.
    - **LS** (level shift): mức nhảy và ở lại.
    - **đổi phương sai**: mức không đổi nhưng σ địa phương đổi ≥ 2 lần.
    """
    sigma = _sigma_ben_vung(y)
    co = hampel(y, cua_so)
    truoc = y.shift(1).rolling(nhin).mean()
    sau = y.shift(-nhin).rolling(nhin).mean()
    xa = y.shift(-3 * nhin).rolling(nhin).mean()
    nguong_muc = 4 * sigma / np.sqrt(nhin)

    # PELT tìm đổi mức phải chạy trên chuỗi ĐÃ BỎ MÙA VỤ, nếu không biên độ mùa vụ sinh điểm gãy giả
    khong_mua = y - pd.Series(STL(y, period=7, robust=True).fit().seasonal, index=y.index)

    su_kien = []
    for moc in diem_gay(khong_mua, log=False, mo_hinh="l2"):
        i = y.index.get_loc(moc)
        d_gan, d_xa = sau.iloc[i] - truoc.iloc[i], xa.iloc[i] - truoc.iloc[i]
        if not np.isfinite(d_gan) or abs(d_gan) < nguong_muc:
            continue
        if not np.isfinite(d_xa):
            d_xa = d_gan
        loai = "TC (thay đổi tạm)" if abs(d_xa) < abs(d_gan) / 2 else "LS (đổi mức)"
        su_kien.append({"mốc": moc, "loại": loai, "đổi mức": round(float(d_gan), 1)})
    for moc in y.index[co]:
        i = y.index.get_loc(moc)
        if any(abs(y.index.get_loc(s["mốc"]) - i) <= nhin for s in su_kien):
            continue
        su_kien.append({"mốc": moc, "loại": "AO (điểm đơn)", "đổi mức": round(float(y.iloc[i] - truoc.iloc[i]), 1)})
    for moc, ty in doi_phuong_sai(y):
        su_kien.append({"mốc": moc, "loại": "đổi phương sai", "đổi mức": round(ty, 2)})
    return pd.DataFrame(su_kien).sort_values("mốc").reset_index(drop=True)


def doi_phuong_sai(y: pd.Series, chu_ky: int = 7, nhin: int = 30, ty_le: float = 2.0) -> list[tuple]:
    """Điểm mà ĐỘ BIẾN ĐỘNG đổi (mức có thể không đổi).

    Hai chi tiết bắt buộc: (1) đo trên **phần dư STL**, vì biên độ mùa vụ át hẳn σ của nhiễu
    (ở chuỗi mẫu: σ thô ≈ 7,9 cả trước lẫn sau điểm gãy, nhìn vào đó sẽ không thấy gì);
    (2) dùng chi phí Gaussian (`model="normal"`), vì l2 chỉ nhìn trung bình.
    """
    v = y.to_numpy(float)
    vi_tri = rpt.Pelt(model="normal", min_size=nhin // 2).fit(v).predict(pen=3 * np.log(v.size))[:-1]

    def _sigma(x):
        return float(np.std(x))

    ra = []
    for i in vi_tri:
        if i < nhin or i > v.size - nhin:
            continue
        truoc, sau = _sigma(v[i - nhin:i]), _sigma(v[i:i + nhin])
        ty = float(sau / truoc) if truoc else np.nan
        if np.isfinite(ty) and (ty > ty_le or ty < 1 / ty_le):
            ra.append((y.index[i], ty))
    return ra


def danh_gia_nhan(su_kien: pd.DataFrame, nhan_that: dict, y: pd.Series, dung_sai: int = 8) -> pd.DataFrame:
    """Với mỗi bất thường cài sẵn: có được phát hiện đúng loại trong phạm vi `dung_sai` bước không?"""
    ten = {"outlier_cong": "AO (điểm đơn)", "level_shift": "LS (đổi mức)",
           "thay_doi_tam": "TC (thay đổi tạm)", "doi_phuong_sai": "đổi phương sai"}
    vi_tri = {m: i for i, m in enumerate(y.index)}
    hang = []
    for khoa, cac_i in nhan_that.items():
        for i in cac_i:
            gan = [d for _, d in su_kien.iterrows() if abs(vi_tri[d["mốc"]] - i) <= dung_sai]
            hang.append({"vị trí": i, "loại thật": ten[khoa],
                         "phát hiện": bool(gan),
                         "đúng loại": any(d["loại"] == ten[khoa] for d in gan)})
    return pd.DataFrame(hang)


def masking(y: pd.Series) -> dict[str, float]:
    """Đo hiệu ứng masking: thêm một ngoại lai rất lớn làm 3σ bắt được ÍT hơn."""
    goc = int(z_score(y).sum())
    them = y.copy()
    them.iloc[len(y) // 2] = y.max() * 8
    return {"3σ bắt được (gốc)": goc, "3σ bắt được (sau khi thêm 1 điểm cực lớn)": int(z_score(them).sum()),
            "Hampel bắt được (gốc)": int(hampel(y).sum()),
            "Hampel bắt được (sau khi thêm)": int(hampel(them).sum())}


# %% [markdown]
# ## Điểm gãy: PELT và cách chọn penalty

# %%
def diem_gay(y: pd.Series, pen: float | None = None, mo_hinh: str = "l2", log: bool = True) -> list:
    """PELT trên chuỗi (mặc định lấy log trước — đổi phần trăm thành khoảng cách cộng).

    pen mặc định = 3·log n (xấp xỉ MBIC). Trả danh sách MỐC THỜI GIAN của điểm gãy.
    """
    v = y.to_numpy(float)
    n = v.size
    pen = 3 * np.log(n) if pen is None else pen
    vi_tri = rpt.Pelt(model=mo_hinh, min_size=3).fit(v).predict(pen=pen)
    return [y.index[i] for i in vi_tri[:-1]]


def quet_penalty(y: pd.Series, cac_pen=None, log: bool = True) -> pd.DataFrame:
    """Quét penalty rồi vẽ elbow — `ruptures` không có CROPS nên phải tự làm."""
    n = len(y)
    cac_pen = cac_pen if cac_pen is not None else np.linspace(0.5, 20, 40) * np.log(n)
    hang = []
    for pen in cac_pen:
        moc = diem_gay(y, pen=float(pen), log=log)
        hang.append({"pen": float(pen), "pen/log n": round(float(pen / np.log(n)), 2),
                     "số điểm gãy": len(moc),
                     "các mốc": [str(m.date()) for m in moc[:6]]})
    return pd.DataFrame(hang)


def diem_gay_on_dinh(y: pd.Series, log: bool = True, khoang=(1.0, 4.0)) -> list:
    """Mốc nào xuất hiện ở MỌI penalty trong khoảng → điểm gãy đáng tin."""
    n = len(y)
    bo = None
    for he_so in np.linspace(khoang[0], khoang[1], 9):
        moc = set(diem_gay(y, pen=float(he_so * np.log(n)), log=log))
        bo = moc if bo is None else (bo & moc)
    return sorted(bo)


def do_lon_gay(y: pd.Series, moc) -> pd.DataFrame:
    """Mức trung bình 12 kỳ trước và sau mỗi điểm gãy — để nói bằng số, không nói 'có vẻ gãy'."""
    hang = []
    for m in moc:
        truoc = y[y.index < m].tail(12).mean()
        sau = y[y.index >= m].head(12).mean()
        hang.append({"mốc": str(pd.Timestamp(m).date()), "trung bình 12 kỳ trước": round(float(truoc)),
                     "trung bình 12 kỳ sau": round(float(sau)),
                     "đổi %": round(float(sau / truoc - 1) * 100, 1)})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Ba cách xử lý COVID — và giá của từng cách

# %%
def _du_bao_mua_vu_xu_huong(hoc: pd.Series, tam: int, m: int = 12) -> np.ndarray:
    """Baseline: hệ số mùa vụ nhân + xu hướng tuyến tính, ước lượng trên TOÀN BỘ phần học.

    Ước lượng trên toàn bộ phần học là điều làm ba cách xử lý COVID cho kết quả khác nhau —
    nếu chỉ dùng 12 kỳ cuối thì 2020 không ảnh hưởng gì và câu hỏi của buổi trở nên vô nghĩa.
    """
    v = hoc.to_numpy(float)
    t = np.arange(v.size)
    a, b = np.polyfit(t, v, 1)
    xu_huong = a * t + b
    he_so = pd.Series(v / np.maximum(xu_huong, 1), index=hoc.index).groupby(hoc.index.month).mean()
    moc = pd.date_range(hoc.index[-1], periods=tam + 1, freq="MS")[1:]
    return np.array([(a * (v.size + i) + b) * he_so.get(m_.month, 1.0) for i, m_ in enumerate(moc)])


def ba_cach_xu_ly_covid(y: pd.Series, moc_cat="2023-01-01", tam: int = 12,
                        covid=("2020-03-01", "2021-06-30")) -> pd.DataFrame:
    """So ba cách trên CÙNG một tập kiểm (dữ liệu sau moc_cat):

    1. giữ nguyên — 2020 kéo mức dự báo xuống;
    2. dummy: thay đoạn COVID bằng nội suy từ hai đầu (coi là ngoại lai);
    3. cắt: chỉ dùng dữ liệu SAU điểm hồi phục (coi là 'bình thường mới').
    """
    hoc_goc, kiem = y[y.index < moc_cat], y[y.index >= moc_cat].head(tam)
    trong_covid = (hoc_goc.index >= covid[0]) & (hoc_goc.index <= covid[1])

    hoc_dummy = hoc_goc.copy()
    hoc_dummy[trong_covid] = np.nan
    hoc_dummy = hoc_dummy.interpolate()

    hoc_cat = hoc_goc[hoc_goc.index > covid[1]]

    hang = []
    for ten, hoc in (("giữ nguyên", hoc_goc), ("coi COVID là ngoại lai (nội suy)", hoc_dummy),
                     ("cắt, chỉ dùng sau hồi phục", hoc_cat)):
        du_bao = _du_bao_mua_vu_xu_huong(hoc, len(kiem))
        mape = float(np.mean(np.abs(du_bao - kiem.to_numpy(float)) / kiem.to_numpy(float)) * 100)
        hang.append({"cách xử lý": ten, "số kỳ học": len(hoc), "MAPE %": round(mape, 2),
                     "sai số trung bình (nghìn khách)": round(float(np.mean(du_bao - kiem.to_numpy(float)) / 1000))})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Xử lý sau khi tìm thấy — sự kiện thật thì GIỮ

# %%
LICH_SU_KIEN = {  # nhật ký sự kiện: biết trước thì không bao giờ được xoá như ngoại lai
    "Tết": "đỉnh lặp hằng năm theo lịch ÂM — ngày dương xê dịch ±3 tuần",
    "COVID": "2020-03 → 2021-05: điểm gãy mức, không phải ngoại lai điểm",
}


def xu_ly_ngoai_lai(y: pd.Series, cach: str = "hampel_winsorize", cua_so: int = 15,
                    bo_qua_su_kien=None) -> pd.DataFrame:
    """Trả chuỗi đã xử lý + cờ. `bo_qua_su_kien` là các mốc KHÔNG được động vào (sự kiện thật).

    Cách chuẩn: xoá mọi điểm lệch quá 3σ.
    """
    y = y.astype(float)
    co = z_score(y)
    sach = y.where(~co)
    return pd.DataFrame({"y": y, "sach": sach, "da_sua": co & sach.notna(), "bi_xoa": co & sach.isna()})


def dinh_tet(y: pd.Series, moi_nam: int = 1) -> list:
    """Mốc có lượt xem cao nhất trong mỗi năm — dùng làm 'nhật ký sự kiện' cho bài Tết."""
    return [g.idxmax() for _, g in y.groupby(y.index.year) if len(g)][: None if moi_nam else 0]


def mat_bao_nhieu_dinh_tet(y: pd.Series, cach=None) -> pd.DataFrame:
    """Mỗi cách bắt ngoại lai xoá mất bao nhiêu đỉnh Tết (trên 10 năm dữ liệu)?"""
    cach = cach or CACH_BAT
    dinh = dinh_tet(y)
    hang = []
    for ten, ham in cach.items():
        co = ham(y).astype(bool)
        hang.append({"cách": ten, "số đỉnh Tết bị gắn cờ": int(sum(bool(co.get(d, False)) for d in dinh)),
                     "trên tổng": len(dinh)})
    return pd.DataFrame(hang)


# %%
if __name__ == "__main__":
    tong = doc_tong_vi()
    print("vi.wikipedia:", len(tong), "ngày", tong.index.min().date(), "→", tong.index.max().date())
    print(so_sanh_bat(tong).to_string(index=False))
    print("masking:", masking(tong))

    tet = doc_bai_tet()
    print("bài Tết:")
    print(so_sanh_bat(tet).to_string(index=False))

    print(mat_bao_nhieu_dinh_tet(tet).to_string(index=False))
    xl = xu_ly_ngoai_lai(tet)
    print("xử lý:", {"đã sửa": int(xl["da_sua"].sum()), "bị xoá": int(xl["bi_xoa"].sum())})

    hk = doc_hang_khong()
    print("hàng không EU27:", len(hk), "tháng", hk.index.min().date(), "→", hk.index.max().date())
    print("điểm gãy ổn định:", [str(m.date()) for m in diem_gay_on_dinh(hk)])
    print(do_lon_gay(hk, diem_gay_on_dinh(hk)).to_string(index=False))
    print("PELT trên mức thô (không log):", len(diem_gay(hk, log=False)), "điểm gãy")
    print(quet_penalty(hk).iloc[::8].to_string(index=False))
    print(ba_cach_xu_ly_covid(hk).to_string(index=False))

    mo, nhan = sinh_chuoi_co_loi()
    su_kien = dan_nhan(mo)
    print(su_kien.to_string(index=False))
    print(danh_gia_nhan(su_kien, nhan, mo).to_string(index=False))
