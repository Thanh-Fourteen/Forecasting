# BẢN SAO của tools/khung/backtest.py — SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/khung/backtest.py rồi chạy lại tool.
"""Backtest rolling origin và kiểm định Diebold–Mariano.

Dữ liệu dạng dài `unique_id, ds, y`. Mốc cắt (cutoff) tính trên trục thời gian CHUNG của mọi chuỗi
(các giá trị `ds` khác nhau đã sắp), nên các chuỗi phải cùng tần suất.

Một cửa sổ với mốc cắt c, khoảng đệm gap, tầm h (đếm theo bước của trục thời gian):

    ... train (ds ≤ c) ... | gap bước bỏ trống | h bước test | ...

- gap mô phỏng dữ liệu về trễ: tại lúc dự báo, gap bước gần nhất chưa có.
- cua_so_train=None → expanding window; = L → chỉ giữ L bước cuối (sliding window).
- refit=True mỗi cửa sổ học lại; refit=k học lại mỗi k cửa sổ; refit=False học một lần ở cửa sổ đầu,
  các cửa sổ sau chỉ dự báo với lịch sử mới (giống ý nghĩa `refit` của statsforecast/mlforecast).

Module này chỉ cần numpy và pandas; `diebold_mariano` cần thêm scipy (phân phối t).
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import pandas as pd

__all__ = ["CuaSo", "chia_cua_so", "backtest", "KetQuaDM", "diebold_mariano"]


@dataclass(frozen=True)
class CuaSo:
    """Một cửa sổ backtest. Các mốc là giá trị ds trên trục thời gian chung (thời gian hoặc số nguyên)."""
    thu_tu: int
    cutoff: object         # ds cuối cùng được thấy khi huấn luyện
    bat_dau_test: object   # ds đầu tiên của tầm dự báo (sau gap)
    ket_thuc_test: object
    bat_dau_train: object


def _truc_thoi_gian(df: pd.DataFrame, cot_ds: str) -> np.ndarray:
    truc = np.sort(df[cot_ds].unique())
    if len(truc) == 0:
        raise ValueError("df rỗng")
    return truc


def _gia_tri(v):
    return pd.Timestamp(v) if isinstance(v, np.datetime64) else v.item() if hasattr(v, "item") else v


def chia_cua_so(df: pd.DataFrame, h: int, so_cua_so: int, buoc: int | None = None, gap: int = 0,
                cua_so_train: int | None = None, cot_ds: str = "ds") -> list[CuaSo]:
    """Các cửa sổ rolling origin, cửa sổ cuối kết thúc đúng ở ds cuối của dữ liệu."""
    if h < 1 or so_cua_so < 1 or gap < 0:
        raise ValueError("cần h ≥ 1, so_cua_so ≥ 1, gap ≥ 0")
    buoc = h if buoc is None else buoc
    if buoc < 1:
        raise ValueError("buoc ≥ 1")
    truc = _truc_thoi_gian(df, cot_ds)
    n = len(truc)
    cuoi_cutoff = n - 1 - gap - h            # vị trí cutoff của cửa sổ cuối
    dau_cutoff = cuoi_cutoff - buoc * (so_cua_so - 1)
    toi_thieu = (cua_so_train or 1) - 1
    if dau_cutoff < toi_thieu:
        raise ValueError(f"không đủ dữ liệu: {n} mốc thời gian cho {so_cua_so} cửa sổ "
                         f"(h={h}, buoc={buoc}, gap={gap}, cua_so_train={cua_so_train})")
    ra = []
    for k in range(so_cua_so):
        c = dau_cutoff + k * buoc
        bd_train = 0 if cua_so_train is None else c - cua_so_train + 1
        ra.append(CuaSo(k, _gia_tri(truc[c]), _gia_tri(truc[c + gap + 1]),
                        _gia_tri(truc[c + gap + h]), _gia_tri(truc[bd_train])))
    return ra


def backtest(df: pd.DataFrame, ham_du_bao: Callable, h: int, so_cua_so: int, buoc: int | None = None,
             gap: int = 0, cua_so_train: int | None = None, refit: bool | int = True,
             ham_huan_luyen: Callable | None = None,
             cot_id: str = "unique_id", cot_ds: str = "ds", cot_y: str = "y") -> pd.DataFrame:
    """Chạy backtest, trả bảng dạng dài: unique_id, ds, cutoff, buoc_h, y, <cột dự báo>.

    Hai cách dùng:
      * ham_du_bao(lich_su, ds_can_du_bao) -> DataFrame[unique_id, ds, <mô hình>...]
        (không truyền ham_huan_luyen; mỗi cửa sổ hàm tự học trên lich_su — tương đương refit=True)
      * ham_huan_luyen(train) -> mo_hinh  và  ham_du_bao(mo_hinh, lich_su, ds_can_du_bao) -> DataFrame
        (refit quyết định khi nào gọi lại ham_huan_luyen)

    lich_su chỉ chứa dòng có ds ≤ cutoff (trong cửa sổ train) — hàm dự báo KHÔNG thấy y của test.
    ds_can_du_bao: DataFrame[unique_id, ds] các dòng test thật; dự báo thừa/thiếu dòng sẽ báo lỗi.
    """
    for cot in (cot_id, cot_ds, cot_y):
        if cot not in df.columns:
            raise ValueError(f"df thiếu cột {cot}")
    if df.duplicated([cot_id, cot_ds]).any():
        raise ValueError(f"có dòng trùng ({cot_id}, {cot_ds})")
    if ham_huan_luyen is None and refit is not True:
        raise ValueError("refit khác True cần ham_huan_luyen tách riêng")
    if isinstance(refit, bool):
        chu_ky_refit = 1 if refit else 0
    elif isinstance(refit, int) and refit >= 1:
        chu_ky_refit = refit
    else:
        raise ValueError("refit là True, False hoặc số nguyên ≥ 1")

    truc = _truc_thoi_gian(df, cot_ds)
    vi_tri = pd.Series(np.arange(len(truc)), index=pd.Index(truc))
    cac_cua_so = chia_cua_so(df, h, so_cua_so, buoc, gap, cua_so_train, cot_ds)
    ket_qua, mo_hinh = [], None
    for cs in cac_cua_so:
        lich_su = df[(df[cot_ds] >= cs.bat_dau_train) & (df[cot_ds] <= cs.cutoff)]
        test = df[(df[cot_ds] >= cs.bat_dau_test) & (df[cot_ds] <= cs.ket_thuc_test)]
        ds_can = test[[cot_id, cot_ds]].reset_index(drop=True)
        if test.empty:
            continue
        if ham_huan_luyen is None:
            du_bao = ham_du_bao(lich_su.copy(), ds_can.copy())
        else:
            if mo_hinh is None or (chu_ky_refit and cs.thu_tu % chu_ky_refit == 0):
                mo_hinh = ham_huan_luyen(lich_su.copy())
            du_bao = ham_du_bao(mo_hinh, lich_su.copy(), ds_can.copy())
        du_bao = pd.DataFrame(du_bao)
        for cot in (cot_id, cot_ds):
            if cot not in du_bao.columns:
                raise ValueError(f"dự báo thiếu cột {cot}")
        if cot_y in du_bao.columns:
            raise ValueError(f"dự báo không được chứa cột {cot_y!r} — dễ nhầm với giá trị thật")
        if du_bao.duplicated([cot_id, cot_ds]).any():
            raise ValueError(f"cửa sổ {cs.thu_tu}: dự báo có dòng trùng")
        ghep = test[[cot_id, cot_ds, cot_y]].merge(du_bao, on=[cot_id, cot_ds], how="outer", indicator=True)
        if (ghep["_merge"] != "both").any():
            thua = int((ghep["_merge"] == "right_only").sum())
            thieu = int((ghep["_merge"] == "left_only").sum())
            raise ValueError(f"cửa sổ {cs.thu_tu} (cutoff {cs.cutoff}): dự báo thừa {thua} dòng ngoài tầm "
                             f"test, thiếu {thieu} dòng — kiểm tra ds_can_du_bao")
        ghep = ghep.drop(columns="_merge")
        ghep.insert(2, "cutoff", cs.cutoff)
        ghep.insert(3, "buoc_h", vi_tri.loc[ghep[cot_ds].to_numpy()].to_numpy() - vi_tri.loc[cs.cutoff])
        ket_qua.append(ghep)
    if not ket_qua:
        raise ValueError("không cửa sổ nào có dữ liệu test")
    return pd.concat(ket_qua, ignore_index=True).sort_values(["cutoff", cot_id, cot_ds], ignore_index=True)


@dataclass(frozen=True)
class KetQuaDM:
    thong_ke: float
    p_value: float
    n: int
    h: int
    hieu_chinh: bool
    trung_binh_chenh: float  # mean(loss_1 - loss_2): âm = mô hình 1 tốt hơn

    def __str__(self) -> str:
        ten = "DM-HLN" if self.hieu_chinh else "DM"
        return (f"{ten}: thống kê {self.thong_ke:.4f}, p = {self.p_value:.4f} (n = {self.n}, h = {self.h}); "
                f"mean(loss1 - loss2) = {self.trung_binh_chenh:.4g}")


def diebold_mariano(e1, e2, h: int = 1, ham_mat_mat: str | Callable = "binh_phuong",
                    hieu_chinh: bool = True, hai_phia: bool = True) -> KetQuaDM:
    """Kiểm định Diebold–Mariano cho H0: hai dự báo có cùng mất mát kỳ vọng.

    d_t = g(e1_t) - g(e2_t);  V(d̄) ≈ (1/n)[γ0 + 2 Σ_{k=1}^{h-1} γk]  (cửa sổ chữ nhật tới h-1)
    DM = d̄ / sqrt(V(d̄)). hieu_chinh=True: Harvey, Leybourne & Newbold (1997)
    DM* = sqrt((n + 1 - 2h + h(h-1)/n) / n) · DM, so với Student-t n-1 bậc tự do; False: chuẩn N(0,1).
    Nếu ước lượng phương sai dài hạn ≤ 0 (có thể xảy ra khi h > 1): cảnh báo và tính lại toàn bộ với
    h = 1 — cùng cách của R forecast::dm.test. Diebold (2015): DM so sánh DỰ BÁO, không so sánh MÔ HÌNH.

    e1, e2: sai số dự báo cùng tầm h trên cùng các thời điểm. hai_phia=False: H1 là mô hình 1 tốt hơn.
    """
    e1, e2 = np.asarray(e1, dtype=float), np.asarray(e2, dtype=float)
    if e1.shape != e2.shape or e1.ndim != 1:
        raise ValueError("e1, e2 phải là mảng 1 chiều cùng độ dài")
    if h < 1:
        raise ValueError("h ≥ 1")
    if callable(ham_mat_mat):
        g = ham_mat_mat
    elif ham_mat_mat == "binh_phuong":
        g = np.square
    elif ham_mat_mat == "tuyet_doi":
        g = np.abs
    else:
        raise ValueError("ham_mat_mat là 'binh_phuong', 'tuyet_doi' hoặc hàm")
    d = g(e1) - g(e2)
    n = len(d)
    if n < 3 or n <= h:
        raise ValueError(f"cần n > h và n ≥ 3, có n = {n}")
    d_tb = float(np.mean(d))
    lech = d - d_tb
    gamma = [float(np.sum(lech[k:] * lech[: n - k]) / n) for k in range(h)]
    v = (gamma[0] + 2 * sum(gamma[1:])) / n
    if v <= 0 and h > 1:
        import warnings

        warnings.warn("phương sai dài hạn âm — tính lại với h = 1 (như forecast::dm.test)", stacklevel=2)
        h, v = 1, gamma[0] / n
    if v == 0:
        raise ValueError("chênh lệch mất mát không đổi — hai dự báo giống hệt nhau?")
    thong_ke = d_tb / np.sqrt(v)

    from scipy import stats  # chỉ cần khi gọi hàm này

    if hieu_chinh:
        thong_ke *= np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
        phan_phoi = stats.t(df=n - 1)
    else:
        phan_phoi = stats.norm()
    p = 2 * phan_phoi.sf(abs(thong_ke)) if hai_phia else phan_phoi.cdf(thong_ke)
    return KetQuaDM(float(thong_ke), float(p), n, h, hieu_chinh, d_tb)
