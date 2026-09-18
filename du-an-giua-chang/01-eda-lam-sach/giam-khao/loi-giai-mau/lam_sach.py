# %% [markdown]
# # Lời giải mẫu — `lam_sach.py` (GIÁM KHẢO GIỮ, KHÔNG VÀO ZIP)
#
# Mục đích: chứng minh 6 lỗi cài sẵn đều phát hiện được bằng đúng kỹ thuật đã dạy ở buổi 10–13,
# và bộ chấm tối thiểu chạy xanh trên một bài làm đạt.

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

BUOC = {"noi-bai": "30min", "ha-noi": "1h", "tphcm": "1h"}
HE_SO_MAD = 1.4826


def doc(tep) -> pd.DataFrame:
    return pd.read_csv(tep, parse_dates=["thoi_gian"])


def _cot_so(bang: pd.DataFrame) -> list[str]:
    bo = {"da_dien", "nghi_ngo", "lo_dai_bo_trong"}
    return [c for c in bang.columns if pd.api.types.is_numeric_dtype(bang[c]) and c not in bo]


def do_phan_giai(y: pd.Series) -> dict[str, float]:
    v = np.sort(y.dropna().unique())
    buoc = np.diff(v)
    return {"số giá trị khác nhau": int(v.size), "bước nhỏ nhất": float(buoc.min()) if buoc.size else np.nan}


def doan_mac_ket(y: pd.Series, toi_thieu: int = 12) -> pd.DataFrame:
    v = y.dropna()
    nhom = (v != v.shift()).cumsum()
    dem = v.groupby(nhom).agg(so_buoc="size", gia_tri="first")
    dem["bat_dau"] = v.groupby(nhom).apply(lambda s: s.index[0])
    return dem[dem["so_buoc"] >= toi_thieu].sort_values("so_buoc", ascending=False).reset_index(drop=True)


def do_dai_lo_hong(y: pd.Series) -> pd.Series:
    thieu = y.isna()
    nhom = (thieu != thieu.shift()).cumsum()[thieu]
    return nhom.groupby(nhom).size().reset_index(drop=True)


def bao_cao_chat_luong(bang: pd.DataFrame) -> pd.DataFrame:
    """Bảng lộ ra L1 (dải giá trị nhảy), L2 (đoạn đứng yên), L4 (mốc trùng), L5 (giá trị 0 bất thường)."""
    b = bang.set_index("thoi_gian") if "thoi_gian" in bang.columns else bang
    hang = []
    for cot in _cot_so(b):
        v = pd.to_numeric(b[cot], errors="coerce")
        ket = doan_mac_ket(v)
        hang.append({
            "cột": cot, "kiểu": str(b[cot].dtype),
            "thiếu %": round(float(v.isna().mean() * 100), 2),
            "min": float(v.min()), "max": float(v.max()),
            "độ phân giải": do_phan_giai(v)["bước nhỏ nhất"],
            "đứng yên dài nhất": int(ket["so_buoc"].max()) if len(ket) else 0,
            "giá trị đứng yên": float(ket["gia_tri"].iloc[0]) if len(ket) else np.nan,
            "số dòng bằng 0": int((v == 0).sum()),
            "mốc trùng": int(b.index.duplicated().sum()),
        })
    return pd.DataFrame(hang)


# %% [markdown]
# ## Phát hiện từng lỗi cài sẵn

# %%
def phat_hien_doi_don_vi(y: pd.Series, he_so: float = 6.0) -> pd.Timestamp | None:
    """L1: trung bình THÁNG nhảy bậc lớn hơn nhiều so với biến thiên tháng thường thấy.

    Đo trên trung bình tháng (không phải rolling), vì đổi đơn vị là một bậc thang sắc nét còn
    mùa vụ năm thì trơn. Ngưỡng theo MAD của chính chuỗi chênh lệch tháng — không hằng số bịa.
    """
    thang = y.resample("MS").mean()
    chenh = thang.diff().dropna()
    mad = HE_SO_MAD * float((chenh - chenh.median()).abs().median())
    if mad == 0 or chenh.abs().max() < he_so * mad:
        return None
    return pd.Timestamp(chenh.abs().idxmax())


def do_lon_doi_don_vi(y: pd.Series, moc: pd.Timestamp) -> dict:
    """Bằng chứng số: mức và biên độ ngày trước/sau mốc. °F ≈ °C × 1,8 + 32."""
    truoc, sau = y[y.index < moc], y[y.index >= moc]
    def bien_do(v):
        return float(v.groupby(v.index.normalize()).agg(lambda x: x.max() - x.min()).median())

    return {"mốc": str(moc.date()), "trung bình trước": round(float(truoc.mean()), 1),
            "trung bình sau": round(float(sau.mean()), 1),
            "biên độ ngày trước": round(bien_do(truoc), 2), "biên độ ngày sau": round(bien_do(sau), 2),
            "tỷ lệ biên độ": round(bien_do(sau) / bien_do(truoc), 2)}


def _do_lech_gio(a: pd.Series, b: pd.Series, toi_da: int = 12) -> int:
    """Độ lệch (giờ) làm tương quan giữa hai chuỗi lớn nhất. Dương = a chậm hơn b."""
    x = a.resample("1h").mean()
    y = b.resample("1h").mean()
    tot, lech = -2.0, 0
    for k in range(-toi_da, toi_da + 1):
        chung = pd.concat([x.shift(-k).rename("a"), y.rename("b")], axis=1).dropna()
        if len(chung) < 100:
            continue
        r = float(chung["a"].corr(chung["b"]))
        if r > tot:
            tot, lech = r, k
    return lech


def phat_hien_lech_mui_gio(y: pd.Series, doi_chieu: pd.Series, chia="2024-06-01") -> dict:
    """L3: so độ lệch giờ với một nguồn ĐỐI CHIẾU ở hai nửa dữ liệu.

    Dùng đỉnh nhiệt trong ngày thì không đủ (mùa vụ năm cũng làm đỉnh dịch); phải đo bằng
    tương quan chéo với một chuỗi không bị lỗi.
    """
    kq = {}
    for ten, lat in (("trước", y.index < chia), ("sau", y.index >= chia)):
        phan = y[lat]
        if len(phan) > 500:
            kq[f"lệch giờ {ten}"] = _do_lech_gio(phan, doi_chieu)
    kq["chênh lệch"] = kq.get("lệch giờ sau", 0) - kq.get("lệch giờ trước", 0)
    return kq


def phat_hien_ngay_gia(bang: pd.DataFrame, cot_khong_the_0=("temperature_2m",)) -> list[str]:
    """L5: ngày mà một đại lượng KHÔNG THỂ bằng 0 lại bằng 0 suốt cả ngày.

    Không dùng "mọi cột bằng 0": lượng mưa bằng 0 là chuyện bình thường, nên quy tắc đó
    bỏ sót 5/11 ngày (đã đo).
    """
    b = bang.set_index("thoi_gian") if "thoi_gian" in bang.columns else bang
    cot = [c for c in cot_khong_the_0 if c in b.columns] or _cot_so(b)[:1]
    la_0 = (b[cot] == 0).all(axis=1)
    ngay = la_0.groupby(b.index.normalize()).mean()
    return [str(pd.Timestamp(d).date()) for d in ngay[ngay > 0.9].index]


def tuong_quan_truot(a: pd.Series, b: pd.Series, cua_so: str = "7D") -> pd.Series:
    """L6: ghép hai nguồn về cùng lưới giờ rồi tính tương quan trượt."""
    x = a.resample("1h").mean()
    y = b.resample("1h").mean()
    chung = pd.concat([x.rename("a"), y.rename("b")], axis=1).dropna()
    return chung["a"].rolling(cua_so).corr(chung["b"])


def phat_hien_doi_nhan(a: pd.Series, b: pd.Series, cua_so: str = "7D") -> dict:
    """L6: đoạn có tương quan trượt tụt hẳn, và dịch ±24 giờ thì tương quan phục hồi.

    LƯU Ý THỨ TỰ: phải sửa lỗi múi giờ của nguồn đối chiếu TRƯỚC, nếu không cả nửa sau dữ liệu
    đều có tương quan thấp và đoạn bị dời nhãn chìm trong đó.
    """
    r = tuong_quan_truot(a, b, cua_so).dropna()
    if r.empty:
        return {}
    nguong = float(r.quantile(0.03))
    xau = r[r <= nguong]
    if xau.empty:
        return {}
    # gom các mốc xấu liền nhau thành một đoạn dài nhất
    nhom = (xau.index.to_series().diff() > pd.Timedelta(days=2)).cumsum()
    dai_nhat = xau.groupby(nhom.to_numpy()).apply(lambda s: s.index.max() - s.index.min()).idxmax()
    doan = xau[nhom.to_numpy() == dai_nhat].index
    phuc_hoi = {}
    for dich in (-24, 24):
        r2 = tuong_quan_truot(a.shift(freq=pd.Timedelta(hours=dich)), b, cua_so).reindex(doan).dropna()
        phuc_hoi[f"dịch {dich:+d} giờ"] = round(float(r2.mean()), 3)
    return {"đoạn nghi ngờ từ": str(doan.min().date()), "đến": str(doan.max().date()),
            "tương quan trong đoạn": round(float(r.loc[doan].mean()), 3),
            "tương quan phần còn lại": round(float(r.drop(doan).mean()), 3),
            "sau khi dịch": phuc_hoi}


# %% [markdown]
# ## Pipeline làm sạch

# %%
def lam_sach(bang: pd.DataFrame, ten_nguon: str, gioi_han_dien: int = 6) -> pd.DataFrame:
    b = bang.set_index("thoi_gian") if "thoi_gian" in bang.columns else bang.copy()
    b = b.sort_index()
    b = b[~b.index.duplicated(keep="first")]                       # L4
    luoi = pd.date_range(b.index.min(), b.index.max(), freq=BUOC[ten_nguon])
    b = b.reindex(luoi).rename_axis("thoi_gian")
    cot = _cot_so(b)

    nghi = pd.Series(False, index=b.index)
    toan_0 = (b[cot] == 0).all(axis=1)                             # L5
    nghi |= toan_0
    # L2 — đoạn đứng yên. Hai điều chỉnh bắt buộc (buổi 10):
    #   * BỎ QUA cột lượng mưa: chuỗi 0 dài là chuyện bình thường, không phải cảm biến chết;
    #   * ngưỡng đặt theo ĐỘ PHÂN GIẢI: nhiệt độ Nội Bài chỉ ghi tới 1 °C nên 12 giờ lặp giá trị
    #     là bình thường; dùng 36 bước (18 giờ) cho lưới 30 phút, 24 bước (24 giờ) cho lưới giờ.
    nguong_ket = 36 if BUOC[ten_nguon] == "30min" else 24
    for c in cot:
        if "precip" in c:
            continue
        for _, d in doan_mac_ket(b[c], toi_thieu=nguong_ket).iterrows():
            if float(d["gia_tri"]) == 0.0 and "wind" in c:
                continue                                           # lặng gió kéo dài là có thật
            cuoi = d["bat_dau"] + pd.Timedelta(BUOC[ten_nguon]) * (int(d["so_buoc"]) - 1)
            nghi.loc[d["bat_dau"]:cuoi] = True
    if ten_nguon == "noi-bai" and "temperature" in b:               # L1: đưa °F về °C
        moc = phat_hien_doi_don_vi(b["temperature"].ffill().bfill())
        if moc is not None:
            sau = b.index >= moc
            b.loc[sau, "temperature"] = (b.loc[sau, "temperature"] - 32) * 5 / 9

    sach = b[cot].where(~nghi, axis=0)
    thieu = sach.isna().any(axis=1)
    nhom = (thieu != thieu.shift()).cumsum()
    do_dai = nhom.map(nhom[thieu].value_counts()).where(thieu, 0)
    dien_duoc = thieu & (do_dai <= gioi_han_dien)
    da_dien = sach.ffill()
    ket_qua = sach.where(~dien_duoc, da_dien, axis=0)
    return ket_qua.assign(da_dien=dien_duoc & ket_qua.notna().all(axis=1), nghi_ngo=nghi,
                          lo_dai_bo_trong=thieu & (do_dai > gioi_han_dien))


# %% [markdown]
# ## Đánh giá cách điền

# %%
def che_diem(y: pd.Series, ty_le: float = 0.10, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    co = np.flatnonzero(y.notna().to_numpy())
    z = y.copy()
    z.iloc[rng.choice(co, size=int(len(co) * ty_le), replace=False)] = np.nan
    return z


def che_khoi(y: pd.Series, so_buoc: int = 48, so_khoi: int = 5, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    z = y.copy()
    for _ in range(so_khoi):
        dau = int(rng.integers(0, max(1, len(y) - so_buoc)))
        z.iloc[dau:dau + so_buoc] = np.nan
    return z


def _dien_mua_vu(y: pd.Series, chu_ky: int = 24) -> pd.Series:
    z = y.copy()
    for _ in range(10):
        if not z.isna().any():
            break
        z = z.where(~z.isna(), z.shift(chu_ky))
    return z


CACH_DIEN = {"ffill": lambda y: y.ffill(),
             "tuyến tính": lambda y: y.interpolate(limit_direction="both"),
             "spline": lambda y: y.interpolate(method="spline", order=3, limit_direction="both"),
             "mùa vụ (ngày trước)": _dien_mua_vu,
             "trung bình theo giờ": lambda y: y.fillna(y.groupby(y.index.hour).transform("mean"))}


def so_sanh_dien(y: pd.Series, seed: int = 0) -> pd.DataFrame:
    that = y.dropna()
    hang = []
    for ten_kieu, che in (("che điểm 10%", che_diem(that, 0.10, seed)),
                          ("che khối 48 bước", che_khoi(that, 48, 5, seed))):
        o_che = that.notna() & che.isna()
        for ten, ham in CACH_DIEN.items():
            doan = ham(che)
            hang.append({"kiểu che": ten_kieu, "cách điền": ten,
                         "MAE": float((doan[o_che] - that[o_che]).abs().mean())})
    return pd.DataFrame(hang)


# %%
if __name__ == "__main__":
    from pathlib import Path
    phat = Path(__file__).resolve().parents[2] / "phat" / "du-lieu"
    ban = {t: doc(phat / f"{t}.csv") for t in ("noi-bai", "ha-noi", "tphcm")}

    nb = ban["noi-bai"].set_index("thoi_gian")
    nb = nb[~nb.index.duplicated()]["temperature"].ffill()
    moc_l1 = phat_hien_doi_don_vi(nb)
    print("== L1 đổi đơn vị ==", do_lon_doi_don_vi(nb, moc_l1) if moc_l1 is not None else "không thấy")
    print("== L2/L4/L5 trong bảng chất lượng ==")
    print(bao_cao_chat_luong(ban["tphcm"]).round(2).to_string(index=False))
    hn = ban["ha-noi"].set_index("thoi_gian")["temperature_2m"]
    hcm = ban["tphcm"].set_index("thoi_gian")["temperature_2m"]
    print("== L3 lệch múi giờ ==", phat_hien_lech_mui_gio(hn, hcm))
    print("== L5 ngày giả ==", phat_hien_ngay_gia(ban["tphcm"]))
    hn_sua = hn.copy()                      # sửa L3 trước rồi mới tìm L6
    sau_l3 = hn_sua.index >= "2024-06-01"
    hn_sua.index = pd.DatetimeIndex(np.where(sau_l3, hn_sua.index - pd.Timedelta(hours=7), hn_sua.index))
    nb_goc = ban["noi-bai"].set_index("thoi_gian")
    nb_goc = nb_goc[~nb_goc.index.duplicated()]["temperature"]
    nb_c = nb_goc.copy()
    if moc_l1 is not None:
        nb_c[nb_c.index >= moc_l1] = (nb_c[nb_c.index >= moc_l1] - 32) * 5 / 9
    print("== L6 dời nhãn ==", phat_hien_doi_nhan(nb_c, hn_sua))

    sach = {t: lam_sach(b, t) for t, b in ban.items()}
    for t, b in sach.items():
        print(t, "→", len(b), "mốc | đã điền", int(b["da_dien"].sum()),
              "| nghi ngờ", int(b["nghi_ngo"].sum()), "| lỗ dài", int(b["lo_dai_bo_trong"].sum()))
    print(so_sanh_dien(sach["noi-bai"]["temperature"].dropna().iloc[:5000]).round(3).to_string(index=False))
