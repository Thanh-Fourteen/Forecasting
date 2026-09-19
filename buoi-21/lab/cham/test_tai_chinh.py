"""Bộ chấm buổi 21 — Chuỗi tài chính và biến động.

Chấm `code/tai_chinh.py` (mặc định) hoặc `dap-an/tai_chinh.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from scipy import stats


@pytest.fixture(scope="module")
def tc(nap, du_lieu):
    return nap("tai_chinh")


@pytest.fixture(scope="module")
def btc(tc):
    return tc.btc_ngay()


@pytest.fixture(scope="module")
def jpy(tc):
    return tc.loi_suat(tc.doc_jpy())


def test_su_that_cach_dieu(tc, jpy):
    """Lợi suất gần như không tự tương quan, bình phương lợi suất thì có; đuôi dày hơn phân phối chuẩn."""
    s = tc.su_that_cach_dieu(jpy)
    assert abs(s["ACF1 lợi suất"]) < 0.05 < s["ACF1 bình phương"]
    assert s["độ nhọn dư"] > 1 and s["tỷ lệ |z| > 4 thực"] > 10 * s["tỷ lệ |z| > 4 nếu chuẩn"]


def test_du_bao_gia_khong_nhin_tuong_lai(tc, btc):
    """Đổi giá sau 1/6/2024: dự báo cho các ngày trước đó không được đổi (chia theo thời gian, chuẩn hoá không dùng tương lai)."""
    gia = btc[0]
    kq1 = tc.du_bao_gia(gia)
    gia2 = gia.copy()
    gia2[gia2.index > pd.Timestamp("2024-06-01")] *= 1.3
    kq2 = tc.du_bao_gia(gia2)
    truoc = kq1.index[kq1.index <= pd.Timestamp("2024-06-01")]
    assert len(truoc) > 100, "phần kiểm phải là các ngày SAU mốc học, liền nhau theo thời gian"
    assert np.allclose(kq1.loc[truoc, "MLP"], kq2.loc[truoc, "MLP"]), "dự báo đổi khi giá tương lai đổi — rò rỉ"


def test_danh_gia_gia_so_voi_naive(tc, btc):
    """R² cao không nói gì: phải so với naive (giá hôm nay) trên cùng các ngày, có kiểm định."""
    kq = tc.danh_gia_gia(tc.du_bao_gia(btc[0]))
    assert {"MAE MLP", "MAE naive", "DM p"} <= set(kq), "thiếu so sánh với naive"
    assert kq["R² naive"] > 0.95, "naive cũng có R² rất cao — đó là lý do R² không dùng được ở đây"


def test_kupiec_vi_du_tay(tc):
    """250 ngày, 6 lần vượt VaR 99%: LR tính theo công thức Kupiec."""
    r = pd.Series(np.r_[np.full(6, -5.0), np.zeros(244)])
    var = pd.Series(-1.0, index=r.index)
    kq = tc.kupiec(r, var)
    ph = 6 / 250
    lr = -2 * ((244 * np.log(0.99) + 6 * np.log(0.01)) - (244 * np.log(1 - ph) + 6 * np.log(ph)))
    assert kq["số lần vượt"] == 6 and kq["LR"] == pytest.approx(lr)
    assert kq["p"] == pytest.approx(stats.chi2.sf(lr, 1))


def test_var_qua_kupiec(tc, jpy):
    """VaR 99% trên JPY 2020–2024 phải qua Kupiec: số lần vượt khớp 1%."""
    kq = tc.kupiec(jpy, tc.var_99(jpy))
    assert kq["p"] > 0.05, f"VaR vượt {kq['số lần vượt']} lần, kỳ vọng {kq['kỳ vọng']:.1f} — độ lệch chuẩn cố định bỏ qua cụm biến động"


def test_garch_thang_bien_dong_co_dinh(tc, btc):
    gia, r, rv = btc
    g = tc.du_bao_garch(r, tc.MOC)["phương sai"]
    y = rv.loc[g.index]
    co_dinh = np.full(len(y), r[r.index < pd.Timestamp(tc.MOC)].var())
    assert tc.qlike(y, g) < tc.qlike(y, co_dinh)


def test_har_chi_dung_qua_khu(tc, btc):
    rv = btc[2]
    moc = "2024-06-01"
    f1 = tc.du_bao_har(rv[rv.index <= pd.Timestamp("2024-06-10")], moc)
    rv2 = rv.copy()
    rv2[rv2.index > pd.Timestamp("2024-06-05")] *= 5
    f2 = tc.du_bao_har(rv2[rv2.index <= pd.Timestamp("2024-06-10")], moc)
    ngay = f1.index[f1.index <= pd.Timestamp("2024-06-05")]
    assert np.allclose(f1.loc[ngay], f2.loc[ngay])
