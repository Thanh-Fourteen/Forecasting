"""Bộ chấm buổi 17 — ARIMA và SARIMA.

Chấm `code/arima.py` (mặc định) hoặc `dap-an/arima.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture(scope="module")
def ar(nap, du_lieu):
    return nap("arima")


@pytest.fixture(scope="module")
def t33(ar):
    return np.log(ar.doc_tourism()["T33"][:-ar.TAM])


def test_mo_phong_ar2_pacf_tat_sau_tre_2(ar):
    """AR(2): PACF có ý nghĩa ở trễ 1, 2 rồi tắt; ACF tắt dần."""
    y = ar.mo_phong(ar=[0.6, 0.3], n=2000, seed=1)
    b = ar.acf_pacf(y, 6)
    nguong = 1.96 / np.sqrt(len(y))
    assert (b["pacf"].iloc[:2].abs() > nguong).all()
    assert (b["pacf"].iloc[2:].abs() < 2 * nguong).all()
    assert b["acf"].iloc[4] > nguong


def test_ljung_box_khop_statsmodels(ar):
    from statsmodels.stats.diagnostic import acorr_ljungbox
    e = np.random.default_rng(3).normal(size=200)
    e[1:] += 0.4 * e[:-1]
    ref = acorr_ljungbox(e, lags=[10], model_df=2)
    kq = ar.ljung_box(e, 10, 2)
    assert kq["Q"] == pytest.approx(float(ref["lb_stat"].iloc[0]), rel=1e-6)
    assert kq["p"] == pytest.approx(float(ref["lb_pvalue"].iloc[0]), rel=1e-6)


def test_kiem_phan_du_bat_mua_vu_bi_quen(ar, t33):
    """Quên phần mùa vụ trên dữ liệu tháng: phần dư còn tự tương quan ở trễ 12 → kiểm phần dư phải báo KHÔNG đạt."""
    mh = ar.arima(t33, (0, 1, 1), (0, 0, 0))
    kq = ar.kiem_phan_du(mh)
    assert not kq["dat"], "phần dư của ARIMA(0,1,1) trên chuỗi du lịch tháng không thể 'ổn' — có kiểm Ljung–Box thật không?"


def test_auto_arima_co_mua_vu(ar, t33):
    mh = ar.auto_arima(t33)
    p, q, P, Q, m, d, D = mh.model_["arma"]
    assert m == 12 and P + D + Q > 0, f"auto-ARIMA chọn {ar.ten_mo_hinh(mh)} — chu kỳ mùa vụ chưa được đưa vào"


def test_mo_hinh_tu_chon_qua_ljung_box_va_gan_auto(ar, t33):
    """Mô hình đọc từ ACF/PACF: phần dư qua Ljung–Box, AICc cách auto-ARIMA không quá 2 (cùng d = 1, D = 1)."""
    mh = ar.mo_hinh_tu_chon(t33)
    assert ar.kiem_phan_du(mh)["dat"]
    tu_dong = ar.auto_arima(t33)
    assert tu_dong.model_["arma"][5:] == mh.model_["arma"][5:], "hai mô hình phải cùng số lần sai phân mới so AICc"
    assert abs(mh.model_["aicc"] - tu_dong.model_["aicc"]) <= 2


def test_du_bao_chi_dung_qua_khu(ar):
    """Backtest (buổi 15): đổi mọi giá trị SAU cutoff cuối thì dự báo của các cửa sổ không đổi."""
    chuoi = {t: v for t, v in list(ar.doc_tourism().items())[:6]}
    df = ar.dang_dai(chuoi)
    kq1 = ar.backtest_tourism(df, so_cua_so=1)
    cutoff = kq1["cutoff"].iloc[0]
    df2 = df.copy()
    df2.loc[df2["ds"] > cutoff, "y"] *= 10
    kq2 = ar.backtest_tourism(df2, so_cua_so=1)
    for m in ar.MO_HINH:
        assert np.allclose(kq1[m], kq2[m]), f"{m} đổi khi dữ liệu tương lai đổi"
