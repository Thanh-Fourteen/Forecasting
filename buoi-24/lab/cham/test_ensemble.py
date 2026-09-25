"""Bộ chấm buổi 24 — Ensemble, AutoML và ca khó.

Chấm `code/ensemble.py`, `code/cold_start.py` (mặc định) hoặc bản trong `dap-an/` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tv.ro_ri import kiem_ro_ri


@pytest.fixture(scope="module")
def en(nap, du_lieu):
    return nap("ensemble")


@pytest.fixture(scope="module")
def cs(nap, du_lieu):
    return nap("cold_start")


@pytest.fixture(scope="module")
def m4(en):
    return en.doc_m4(40)


def _diem_gia(cua_so: list[int]) -> pd.DataFrame:
    """Hai chuỗi, hai mô hình. A tốt nhất ở W1–W2 (0,5) nhưng tệ ở W3 (1,5); B đều 1,0.
    Chọn trung thực trên W1–W2 → chọn A → báo cáo W3 = 1,5."""
    dong = []
    for u in ["s1", "s2"]:
        for c in cua_so:
            dong.append({"unique_id": u, "cutoff": c, "A": 0.5 if c < cua_so[-1] else 1.5, "B": 1.0})
    return pd.DataFrame(dong).set_index(["unique_id", "cutoff"])


def test_bao_cao_tren_cua_so_chua_dung_de_chon(en):
    """Cửa sổ báo cáo phải tách rời và nằm SAU cửa sổ dùng để chọn; điểm báo cáo là điểm của lựa chọn trên W3."""
    assert not set(en.CUA_SO_CHON) & set(en.CUA_SO_BAO_CAO), \
        f"chọn trên {en.CUA_SO_CHON} rồi báo cáo trên {en.CUA_SO_BAO_CAO}: báo cáo trên chính dữ liệu đã dùng để chọn"
    assert max(en.CUA_SO_CHON) < min(en.CUA_SO_BAO_CAO)
    kq = en.chon_va_bao_cao(_diem_gia(en.CUTOFF))
    assert (kq["lua_chon"] == "A").all()
    assert kq["diem_bao_cao"] == pytest.approx(1.5)
    assert kq["lac_quan"] == pytest.approx(1.0)


def test_trong_so_khong_nhin_cua_so_bao_cao(en, m4):
    """Trọng số kết hợp ước lượng trên backtest TRƯỚC đoạn báo cáo: đổi y trong cửa sổ báo cáo, trọng số không đổi."""
    rng = np.random.default_rng(0)
    fc = pd.DataFrame([{"unique_id": u, "ds": c + h, "cutoff": c, "y": 10 + rng.normal(),
                        "AutoETS": 10 + rng.normal(), "AutoTheta": 10 + rng.normal(), "LGBM": 10 + rng.normal()}
                       for u in ["s1", "s2"] for c in en.CUTOFF for h in range(1, 4)])
    fc2 = fc.assign(y=np.where(fc["cutoff"].isin(en.CUA_SO_BAO_CAO), fc["y"] + 100, fc["y"]))
    for cach in ["nghich_mse", "toi_uu"]:
        pd.testing.assert_frame_equal(en.trong_so(fc, cach), en.trong_so(fc2, cach),
                                      obj=f"trọng số '{cach}' đổi khi đổi y của đoạn báo cáo")


def test_mase_vi_du_tay(en):
    """Chuỗi 24 tháng: năm 1 là 1…12, năm 2 là 3…14 → 'lặp lại năm trước' lệch 2 mỗi tháng: mẫu số 2.
    Dự báo lệch 1 → MASE 0,5."""
    df = pd.DataFrame({"unique_id": "a", "ds": np.arange(26),
                       "y": np.r_[np.arange(1, 13), np.arange(3, 15), 20.0, 20.0]})
    fc = pd.DataFrame({"unique_id": "a", "ds": [24, 25], "cutoff": 23, "y": [20.0, 20.0], "M": [21.0, 19.0]})
    assert float(en.mase(fc, df)["M"].iloc[0]) == pytest.approx(0.5)


def test_dac_trung_lgbm_khong_ro_ri(en, m4):
    """Đặc trưng tại tháng gốc o chỉ dùng y tới o, tức là dùng được để dự báo tháng o + 1 (tầm h = 1)."""
    d = m4[m4["unique_id"].isin(m4["unique_id"].unique()[:3])]

    def dac_trung_cho_thang_sau(x: pd.DataFrame) -> pd.DataFrame:     # dòng t mang đặc trưng của gốc t − 1
        f = en.dac_trung(x).sort_values(["unique_id", "ds"])
        cot = [c for c in f.columns if c not in ("unique_id", "ds", "thang")]
        f[cot] = f.groupby("unique_id")[cot].shift(1)
        return f

    kq = kiem_ro_ri(dac_trung_cho_thang_sau, d, h=1, cot_id="unique_id", cot_ds="ds", cot_bo_qua=["thang"])
    assert not kq.co_ro_ri, str(kq)


def test_lgbm_chi_dung_qua_khu(en, m4):
    """Đổi mọi y SAU cutoff đầu: dự báo LightGBM của cutoff đầu không được đổi."""
    c = en.CUTOFF[0]
    a = en.du_bao_lgbm(m4, [c], n_estimators=20)
    b = en.du_bao_lgbm(m4.assign(y=np.where(m4["ds"] > c, m4["y"] * 3, m4["y"])), [c], n_estimators=20)
    assert np.allclose(a["LGBM"], b["LGBM"])


def test_cold_start_chi_dung_hang_da_ban_xong(cs):
    """Hàng tương tự của một mã ra mắt ngày T: 8 tuần đầu của chúng phải kết thúc trước T.
    'b' ra mắt 30/8: tuần thứ 8 là tuần 18/10, xong trước 25/10 → được dùng; 'c' (4/10) chưa bán xong."""
    sp = pd.DataFrame({"ra_mat": pd.to_datetime(["2010-01-04", "2010-06-07", "2010-08-30", "2010-10-04", "2010-10-25"])},
                      index=["cu", "a", "b", "c", "moi"])
    nhom = cs.nhom_tuong_tu(sp, pd.Timestamp("2010-10-25"))
    assert set(nhom.index) == {"a", "b"}, f"được dùng: {sorted(nhom.index)} — 'c' chưa bán xong 8 tuần, 'cu' là mã cũ"
