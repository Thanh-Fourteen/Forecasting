"""Bộ chấm buổi 18 — Hồi quy chuỗi thời gian và hồi quy động.

Chấm `code/hoi_quy.py` (mặc định) hoặc `dap-an/hoi_quy.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def hq(nap, du_lieu):
    return nap("hoi_quy")


def test_mo_phong_hoi_quy_gia(hq):
    """Hai bước ngẫu nhiên độc lập: hồi quy trên mức 'tìm thấy' quan hệ ở phần lớn các cặp, trên sai phân thì ~5%."""
    kq = hq.mo_phong_hoi_quy_gia(so_lan=200)
    assert kq["trên mức"] > 0.5
    assert kq["trên sai phân"] < 0.12


def test_he_so_ip_dung_hoi_quy_dong(hq):
    """Hành khách EU ~ sản lượng công nghiệp Mỹ: sai số phải là ARIMA, phần dư phải trắng, và hệ số hết 'ý nghĩa'."""
    y, X = hq.cap_gia()
    kq = hq.he_so_ip(y, X)
    assert kq["Ljung-Box p"] > 0.05, "phần dư còn tự tương quan: p-value của hệ số không tin được — sai số phải là ARIMA"
    assert kq["p"] > 0.05, "hai chuỗi không liên quan: sau khi mô hình hoá sai số, hệ số không còn có ý nghĩa"


def test_fourier_va_bien_nhiet(hq):
    moc = pd.date_range("2024-07-01", periods=48, freq="h")
    F = hq.fourier(moc, 24, 3)
    assert F.shape == (48, 6)
    assert np.allclose(F.iloc[:24].to_numpy(), F.iloc[24:].to_numpy()), "Fourier chu kỳ 24 giờ phải lặp lại sau 24 giờ"
    nhiet = pd.Series([10.0, 18.0, 30.0], index=moc[:3])
    X = hq.bien_giai_thich(moc[:3], nhiet, 1, 1)
    assert X["cdd"].tolist() == [0, 0, 12] and X["hdd"].tolist() == [8, 0, 0]


def test_du_bao_dhr_chi_dung_thong_tin_co_luc_du_bao(hq):
    """Đổi nhiệt độ ĐO THẬT và tải sau cutoff: dự báo không được đổi (lúc dự báo chỉ có nhiệt độ đã dự báo)."""
    y = hq.doc_dien()
    df = pd.DataFrame({"unique_id": "ERCO", "ds": y.index, "y": y.to_numpy()})
    cutoff = pd.Timestamp("2024-08-06 06:00")
    ls = df[(df["ds"] <= cutoff) & (df["ds"] > cutoff - pd.Timedelta(hours=24 * 28))]
    ds = df[(df["ds"] > cutoff) & (df["ds"] <= cutoff + pd.Timedelta(hours=24))][["unique_id", "ds"]]
    nhiet = hq.doc_nhiet()
    f1 = hq.du_bao_dhr(ls, ds, nhiet, 4, 2)["DHR"].to_numpy()
    nhiet2 = nhiet.copy()
    nhiet2.loc[nhiet2.index > cutoff, "that"] += 10
    f2 = hq.du_bao_dhr(ls, ds, nhiet2, 4, 2)["DHR"].to_numpy()
    assert np.allclose(f1, f2), "dự báo dùng nhiệt độ đo thật của ngày mai — lúc ra dự báo chưa có số đó"


def test_prophet_khai_tet(hq):
    """Học tới hết 2023, dự báo 2024: quanh Tết (± 7 ngày) Prophet phải biết lượt xem sụt."""
    kq = hq.backtest_wiki(so_cua_so=2)
    kq = kq[kq["ds"].dt.year == 2024]
    assert hq.mae_quanh_tet(kq) < 0.2, "Prophet mặc định không biết Tết âm lịch — phải khai nó như một ngày lễ có cửa sổ"
