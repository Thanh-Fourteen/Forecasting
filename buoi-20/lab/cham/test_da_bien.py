"""Bộ chấm buổi 20 — Đa biến, state space và nowcasting.

Chấm `code/da_bien.py` (mặc định) hoặc `dap-an/da_bien.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

VAN_TAY = {  # sha256 của các bảng vintage đã cắt tới 25M12 — mọi học viên phải có đúng cùng số liệu
    "gdp": "3b78cafec76a4f3ac46476918f5c004599c36ae4dbf34e9484782eb70e47824e",
    "e": "bec3cad1ba2723ff10b098ca3c114092f0480b4aa2e339faa8ce099a7cede2f0",
    "ip": "95aa887cf9cdec53f6b2f60f4a0599f6f0a92de69d5c95317f2e9c0aa8a5ef42",
    "hs": "f542bb6d7661938c1c31b96ce8af63ffc2beb61e25c4c8f12cd7150f955827a6",
}


@pytest.fixture(scope="module")
def db(nap, du_lieu):
    return nap("da_bien")


@pytest.fixture(scope="module")
def vintage(db):
    return db.doc_tat_ca()


def test_du_lieu_vintage_cat_dung_moc(db, vintage):
    """Tệp nguồn thêm vintage mỗi tháng; phần buổi dùng (tới 25M12) phải y hệt bản của tác giả."""
    for k, v in vintage.items():
        assert v.columns[-1] == db.VINTAGE_CUOI
        assert db.dau_van_tay(v) == VAN_TAY[k], f"số liệu {k} khác bản chốt — kiểm lại phần cắt vintage"


def test_kalman_khop_statsmodels(db):
    y = db.doc_nile()
    ref = db.local_level_statsmodels(y)
    s2_nhieu, s2_muc = ref.params
    kq = db.kalman_local_level(y, s2_nhieu, s2_muc)
    assert np.allclose(kq["mức"], ref.filtered_state[0], rtol=1e-4)


def test_kalman_du_lieu_thieu(db):
    """Không có số đo: mức giữ nguyên, bất định lớn dần đúng bằng phương sai của cú dời mỗi bước."""
    y = np.r_[np.full(20, 100.0), np.full(5, np.nan)]
    kq = db.kalman_local_level(y, 4.0, 1.0)
    assert np.allclose(kq["mức"][-5:], kq["mức"][19])
    assert np.allclose(np.diff(kq["phương sai"][-6:]), 1.0)


def test_dau_xang_dong_lien_ket_va_vecm(db):
    """Dầu và xăng 2010–2019 đều không dừng nhưng spread dừng: phải kiểm Johansen và dùng VECM."""
    L = db.doc_dau_xang()
    hang = db.hang_dong_lien_ket(L)
    assert hang == 1, "chưa kiểm cointegration — dùng select_coint_rank (Johansen)"
    ten, f = db.du_bao_xang(L, 4, hang)
    assert ten == "VECM" and len(f) == 4


def test_nowcast_chi_dung_vintage_luc_do(db, vintage):
    """Đổi mọi vintage SAU lúc nowcast: kết quả không được đổi (không dùng số liệu đã sửa về sau)."""
    q, k = pd.Period("2015Q1"), 1
    kq1 = db.nowcast(vintage, q, k)
    sau = [c for c in vintage["gdp"].columns if db._nam_thang(c) > (2015, 1)]
    rng = np.random.default_rng(0)
    doi = {ten: v.copy() for ten, v in vintage.items()}
    for v in doi.values():
        cot = [c for c in v.columns if c in sau]
        v[cot] = v[cot] * rng.uniform(0.8, 1.2, size=v[cot].shape)   # "sửa số liệu" ở các vintage sau
    kq2 = db.nowcast(doi, q, k)
    assert kq1["bridge"] == pytest.approx(kq2["bridge"]), "nowcast dùng vintage sau thời điểm dự báo — đó là rò rỉ"


def test_nowcast_sai_so_giam_khi_co_them_thang(db, vintage):
    bang = db.danh_gia_nowcast(vintage, pd.period_range("2005Q1", "2019Q4", freq="Q"))
    r = db.rmse_theo_k(bang)["bridge"]
    assert r.loc[4] < r.loc[1], "có thêm tháng số liệu thì sai số phải giảm"
