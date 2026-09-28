# BẢN SAO của tools/khung/ro_ri.py — SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/khung/ro_ri.py rồi chạy lại tool.
"""Kiểm rò rỉ tương lai tự động cho hàm feature, hàm làm sạch và cách chia dữ liệu.

Hai bài kiểm chính cho một hàm `ham(df) -> DataFrame` (cùng các dòng unique_id, ds, thêm cột feature):

1. CẮT TƯƠNG LAI (tính bất biến khi cắt). Với mỗi mốc cắt c:
       ham(df)            tính trên dữ liệu đầy đủ
       ham(df[ds <= c])   tính trên dữ liệu chỉ tới c
   Mọi dòng ds ≤ c phải GIỐNG NHAU. Khác nhau ⇒ giá trị tại quá khứ đã dùng dữ liệu sau c.
   Bắt: rolling centered, filtfilt / Kalman smoother, chuẩn hoá fit trên toàn chuỗi, điền dữ liệu hai
   chiều, thống kê trên toàn chuỗi (max, rank, target encoding), dropna làm mất dòng quá khứ.

2. NHIỄU MỤC TIÊU theo tầm h. Feature dùng để dự báo y_t với tầm h chỉ được dùng y tới t-h.
   Cộng nhiễu lớn vào y từ vị trí p trở đi (theo từng chuỗi) rồi tính lại: mọi dòng ở vị trí < p + h
   phải giữ nguyên feature. Bắt: rolling không shift, lag nhỏ hơn h trong chiến lược direct, ewm không
   shift, feature dùng chính y_t. Bài này không áp dụng cho hàm làm sạch y (đặt h=None).

Bài 1 KHÔNG bắt được feature rò qua dữ liệu NGOÀI hàm (vd cột nhiệt độ thực tế thay cho nhiệt độ
dự báo lưu trữ, số liệu đã sửa thay cho vintage) — đó là vấn đề nguồn dữ liệu, phải kiểm bằng
nguồn (buổi 13, 20, 41).

Kiểm phụ:
    kiem_chia_tap(train, test)          mọi chuỗi: ds lớn nhất của train < ds nhỏ nhất của test
    kiem_scaler(scaler, X_train)        thống kê đã fit có khớp CHỈ tập train không
    kiem_chong_lan(muc_tieu_train, muc_tieu_val)   cửa sổ train có mục tiêu rơi vào thời gian val không

Chỉ cần numpy và pandas; không import module khác của tv.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

__all__ = ["VanDe", "KetQuaRoRi", "kiem_ro_ri", "kiem_chia_tap", "kiem_scaler", "kiem_chong_lan"]


@dataclass(frozen=True)
class VanDe:
    loai: str          # "cat_tuong_lai" | "nhieu_muc_tieu" | "dong_khac" | "chia_tap" | "scaler" | "chong_lan"
    cot: str | None
    mo_ta: str


@dataclass
class KetQuaRoRi:
    van_de: list[VanDe] = field(default_factory=list)

    @property
    def co_ro_ri(self) -> bool:
        return bool(self.van_de)

    @property
    def cot_ro_ri(self) -> list[str]:
        return sorted({v.cot for v in self.van_de if v.cot})

    def __bool__(self) -> bool:  # `if kiem_ro_ri(...)` đọc là "có rò rỉ"
        return self.co_ro_ri

    def __str__(self) -> str:
        if not self.van_de:
            return "Không phát hiện rò rỉ."
        return "PHÁT HIỆN RÒ RỈ:\n" + "\n".join(f"  - [{v.loai}] {v.mo_ta}" for v in self.van_de)

    def khang_dinh_sach(self) -> None:
        """Dùng trong test: assert không rò rỉ, thông báo lỗi liệt kê từng vấn đề."""
        if self.van_de:
            raise AssertionError(str(self))


def _chuan_bi(df: pd.DataFrame, cot_id: str | None, cot_ds: str) -> tuple[pd.DataFrame, list[str]]:
    if cot_ds not in df.columns:
        raise ValueError(f"df thiếu cột {cot_ds}")
    khoa = [cot_ds] if cot_id is None else [cot_id, cot_ds]
    if cot_id is not None and cot_id not in df.columns:
        raise ValueError(f"df thiếu cột {cot_id} (đặt cot_id=None nếu chỉ có một chuỗi)")
    if df.duplicated(khoa).any():
        raise ValueError(f"df có dòng trùng khoá {khoa}")
    return df.sort_values(khoa).reset_index(drop=True), khoa


def _goi(ham: Callable, df: pd.DataFrame, khoa: list[str]) -> pd.DataFrame:
    ra = ham(df.copy())
    if not isinstance(ra, pd.DataFrame):
        raise TypeError("hàm cần trả về DataFrame")
    thieu = [k for k in khoa if k not in ra.columns]
    if thieu:
        raise ValueError(f"kết quả của hàm thiếu cột khoá {thieu} — giữ lại {khoa} để so được")
    if ra.duplicated(khoa).any():
        raise ValueError(f"kết quả của hàm có dòng trùng khoá {khoa}")
    return ra


def _gia_tri_khac(a: pd.Series, b: pd.Series, sai_so: float) -> np.ndarray:
    """Mảng bool: vị trí a và b khác nhau (NaN == NaN coi là giống)."""
    if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b) \
            and not pd.api.types.is_bool_dtype(a):
        x, y = a.to_numpy(dtype=float), b.to_numpy(dtype=float)
        cung_nan = np.isnan(x) & np.isnan(y)
        with np.errstate(invalid="ignore"):
            gan = np.abs(x - y) <= sai_so * np.maximum(1.0, np.abs(x))
        return ~(cung_nan | gan)
    cung_na = (a.isna() & b.isna()).to_numpy()
    return ~(cung_na | (a.astype(object) == b.astype(object)).to_numpy())


def _hien(v) -> str:
    """Giá trị dễ đọc trong báo cáo: bỏ np.float64(...), thời gian dạng pandas."""
    if isinstance(v, np.datetime64):
        return str(pd.Timestamp(v))
    if isinstance(v, np.generic):
        v = v.item()
    return f"{v:.6g}" if isinstance(v, float) else str(v)


def _so_sanh(day_du: pd.DataFrame, cat: pd.DataFrame, khoa: list[str], cot_ds: str, moc,
             sai_so: float, loai: str, cot_bo_qua: set[str], mo_ta_moc: str) -> list[VanDe]:
    van_de: list[VanDe] = []
    truoc = day_du[day_du[cot_ds] <= moc] if loai == "cat_tuong_lai" else day_du
    ghep = truoc.merge(cat, on=khoa, how="outer", suffixes=("__day_du", "__cat"), indicator=True)
    lech_dong = ghep["_merge"] != "both"
    if lech_dong.any() and loai == "cat_tuong_lai":
        chi_day_du = int((ghep["_merge"] == "left_only").sum())
        chi_cat = int((ghep["_merge"] == "right_only").sum())
        van_de.append(VanDe("dong_khac", None,
                            f"{mo_ta_moc}: số dòng quá khứ khác nhau (chỉ có ở bản đầy đủ: {chi_day_du}, "
                            f"chỉ có ở bản cắt: {chi_cat}) — hàm xoá/thêm dòng dựa trên dữ liệu tương lai?"))
    ghep = ghep[~lech_dong]
    cac_cot = [c for c in day_du.columns if c not in khoa and c not in cot_bo_qua and c in cat.columns]
    for cot in cac_cot:
        khac = _gia_tri_khac(ghep[f"{cot}__day_du"], ghep[f"{cot}__cat"], sai_so)
        if khac.any():
            dong = ghep[khac].iloc[0]
            vi_tri = ", ".join(f"{k}={_hien(dong[k])}" for k in khoa)
            van_de.append(VanDe(loai, cot,
                                f"cột '{cot}' {mo_ta_moc}: {int(khac.sum())} dòng đổi giá trị; ví dụ tại {vi_tri}: "
                                f"{_hien(dong[f'{cot}__day_du'])} (đầy đủ) → {_hien(dong[f'{cot}__cat'])} "
                                f"({'bản cắt' if loai == 'cat_tuong_lai' else 'bản đổi y'})"))
    return van_de


def kiem_ro_ri(ham: Callable[[pd.DataFrame], pd.DataFrame], df: pd.DataFrame,
               cac_moc_cat: Sequence | None = None, h: int | None = 1, cot_id: str | None = "unique_id",
               cot_ds: str = "ds", cot_y: str = "y", sai_so: float = 1e-9, so_moc: int = 3,
               cot_bo_qua: Sequence[str] = (), seed: int = 0) -> KetQuaRoRi:
    """Chạy bài kiểm cắt tương lai (luôn) và nhiễu mục tiêu (khi h không None).

    ham: nhận DataFrame dạng dài, trả DataFrame giữ cột khoá (unique_id, ds) + cột feature.
    cac_moc_cat: các mốc ds để cắt; None → chọn so_moc mốc rải đều trong 20%–90% trục thời gian.
    h: tầm dự báo mà feature phục vụ — feature cho y_t chỉ được dùng y tới t-h. None: bỏ bài nhiễu
       mục tiêu (dùng cho hàm làm sạch y, vốn được phép đọc y_t).
    cot_bo_qua: cột không kiểm (vd cột y gốc khi hàm giữ nguyên nó).
    """
    df, khoa = _chuan_bi(df, cot_id, cot_ds)
    truc = np.sort(df[cot_ds].unique())
    if len(truc) < 4:
        raise ValueError("cần ít nhất 4 mốc thời gian để kiểm")
    if cac_moc_cat is None:
        vi_tri = np.unique(np.linspace(int(0.2 * len(truc)), int(0.9 * len(truc)), so_moc).astype(int))
        cac_moc_cat = [truc[i] for i in vi_tri]
    ket_qua = KetQuaRoRi()
    bo_qua = set(cot_bo_qua)

    day_du = _goi(ham, df, khoa)
    for moc in cac_moc_cat:
        cat = _goi(ham, df[df[cot_ds] <= moc], khoa)
        ket_qua.van_de += _so_sanh(day_du, cat, khoa, cot_ds, moc, sai_so, "cat_tuong_lai",
                                   bo_qua, f"khi cắt dữ liệu tại {cot_ds}={_hien(moc)}")

    if h is not None:
        if h < 1:
            raise ValueError("h ≥ 1 (hoặc None để bỏ bài nhiễu mục tiêu)")
        if cot_y not in df.columns:
            raise ValueError(f"bài nhiễu mục tiêu cần cột {cot_y}")
        rng = np.random.default_rng(seed)
        thu_tu = (df.groupby(cot_id, sort=False).cumcount() if cot_id else pd.Series(np.arange(len(df))))
        do_dai = (df.groupby(cot_id, sort=False)[cot_ds].transform("size") if cot_id
                  else pd.Series(len(df), index=df.index))
        muc_y = float(np.nanstd(df[cot_y].to_numpy(dtype=float))) or 1.0
        for phan_tram in (0.5, 0.8):
            p = np.floor(do_dai * phan_tram).astype(int)
            bi_nhieu = thu_tu >= p
            df_nhieu = df.copy()
            df_nhieu[cot_y] = df_nhieu[cot_y].astype(float)
            df_nhieu.loc[bi_nhieu, cot_y] += muc_y * (10 + rng.random(int(bi_nhieu.sum())) * 10)
            ra_nhieu = _goi(ham, df_nhieu, khoa)
            duoc_giu = df.loc[thu_tu < p + h, khoa]
            goc = day_du.merge(duoc_giu, on=khoa)
            moi = ra_nhieu.merge(duoc_giu, on=khoa)
            ket_qua.van_de += _so_sanh(goc, moi, khoa, cot_ds, None, sai_so, "nhieu_muc_tieu",
                                       bo_qua | {cot_y},
                                       f"khi đổi {cot_y} từ {int(phan_tram * 100)}% chuỗi trở đi (tầm h={h})")
    # gộp trùng: cùng loại + cùng cột chỉ báo một lần
    thay, gon = set(), []
    for v in ket_qua.van_de:
        if (v.loai, v.cot) not in thay:
            thay.add((v.loai, v.cot))
            gon.append(v)
    ket_qua.van_de = gon
    return ket_qua


def kiem_chia_tap(train: pd.DataFrame, test: pd.DataFrame, cot_id: str | None = "unique_id",
                  cot_ds: str = "ds", gap=None) -> KetQuaRoRi:
    """Mỗi chuỗi: max(ds train) < min(ds test) (và cách ít nhất `gap` nếu truyền, cùng kiểu với ds)."""
    ket_qua = KetQuaRoRi()
    if cot_id is None:
        cap = [(None, train, test)]
    else:
        nhom_test = dict(tuple(test.groupby(cot_id)))
        cap = [(uid, g, nhom_test[uid]) for uid, g in train.groupby(cot_id) if uid in nhom_test]
    for uid, tr, te in cap:
        cuoi_train, dau_test = tr[cot_ds].max(), te[cot_ds].min()
        nhan = "" if uid is None else f"chuỗi {uid!r}: "
        if cuoi_train >= dau_test:
            so_dong = int((tr[cot_ds] >= dau_test).sum())
            ket_qua.van_de.append(VanDe("chia_tap", None,
                                        f"{nhan}train có {so_dong} dòng không trước test (train tới {cuoi_train}, "
                                        f"test từ {dau_test}) — chia ngẫu nhiên / shuffle?"))
        elif gap is not None and dau_test - cuoi_train < gap:
            ket_qua.van_de.append(VanDe("chia_tap", None,
                                        f"{nhan}khoảng cách train–test {dau_test - cuoi_train} nhỏ hơn gap {gap}"))
    return ket_qua


def kiem_scaler(scaler, X_train, sai_so: float = 1e-8) -> KetQuaRoRi:
    """Kiểm thống kê đã fit của scaler (kiểu scikit-learn) khớp với X_train.

    Hỗ trợ thuộc tính mean_/scale_ (StandardScaler), data_min_/data_max_ (MinMaxScaler), center_
    (RobustScaler). Không khớp ⇒ scaler được fit trên dữ liệu khác train (thường là toàn bộ dữ liệu).
    """
    X = np.asarray(X_train, dtype=float)
    if X.ndim == 1:
        X = X[:, None]
    ky_vong = {
        "mean_": lambda: np.nanmean(X, axis=0),
        "var_": lambda: np.nanvar(X, axis=0),
        "data_min_": lambda: np.nanmin(X, axis=0),
        "data_max_": lambda: np.nanmax(X, axis=0),
        "center_": lambda: np.nanmedian(X, axis=0),
    }
    da_kiem = 0
    ket_qua = KetQuaRoRi()
    for thuoc_tinh, tinh in ky_vong.items():
        if not hasattr(scaler, thuoc_tinh) or getattr(scaler, thuoc_tinh) is None:
            continue
        da_kiem += 1
        fit = np.asarray(getattr(scaler, thuoc_tinh), dtype=float)
        dung = tinh()
        if fit.shape != dung.shape or not np.allclose(fit, dung, rtol=sai_so, atol=sai_so):
            ket_qua.van_de.append(VanDe("scaler", thuoc_tinh,
                                        f"scaler.{thuoc_tinh} = {np.round(fit, 6).tolist()} nhưng thống kê của "
                                        f"X_train là {np.round(dung, 6).tolist()} — scaler không fit trên train"))
    if da_kiem == 0:
        raise ValueError("scaler không có mean_/var_/data_min_/data_max_/center_ — chưa fit hoặc kiểu không hỗ trợ")
    return ket_qua


def kiem_chong_lan(muc_tieu_train: pd.DataFrame, muc_tieu_val: pd.DataFrame,
                   cot_id: str | None = "unique_id", cot_ds: str = "ds") -> KetQuaRoRi:
    """Cửa sổ mẫu (deep learning / ML dạng bảng) có chồng lấn train–val không.

    muc_tieu_train / muc_tieu_val: mỗi dòng là MỘT thời điểm mục tiêu mà một mẫu dự báo
    (unique_id, ds). Rò rỉ khi có mục tiêu train ở thời điểm ≥ mục tiêu val sớm nhất của cùng chuỗi —
    tức là lúc huấn luyện đã thấy giá trị mà tập val dùng để chấm.
    Đầu vào (context) của val nằm trong giai đoạn train là BÌNH THƯỜNG, không cần truyền vào.
    """
    ket_qua = KetQuaRoRi()
    if cot_id is None:
        cap = [(None, muc_tieu_train, muc_tieu_val)]
    else:
        nhom_val = dict(tuple(muc_tieu_val.groupby(cot_id)))
        cap = [(uid, g, nhom_val[uid]) for uid, g in muc_tieu_train.groupby(cot_id) if uid in nhom_val]
    for uid, tr, va in cap:
        dau_val = va[cot_ds].min()
        chong = tr[tr[cot_ds] >= dau_val]
        if len(chong):
            nhan = "" if uid is None else f"chuỗi {uid!r}: "
            ket_qua.van_de.append(VanDe("chong_lan", None,
                                        f"{nhan}{len(chong)} mục tiêu của train ở thời điểm ≥ {dau_val} "
                                        f"(đầu tập val), muộn nhất {chong[cot_ds].max()} — cắt cửa sổ trước khi chia tập?"))
    return ket_qua
