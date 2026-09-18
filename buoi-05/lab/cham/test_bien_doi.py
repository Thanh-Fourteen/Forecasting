"""Bộ chấm buổi 5 — điều chỉnh lịch/lạm phát/dân số, Box-Cox tự viết, hiệu chỉnh bias khi đổi ngược."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from scipy import special
from statsmodels.base.transform import BoxCox


@pytest.fixture(scope="module")
def m(nap):
    return nap("bien_doi")


@pytest.fixture(scope="module")
def ban_le(m, du_lieu):
    return m.doc_ban_le()


def test_doc_du_lieu(m, ban_le):
    assert len(ban_le) == 414 and ban_le.notna().all()
    assert ban_le[pd.Timestamp("2023-03-01")] == 679701
    cpi = m.doc_cpi()
    assert np.isnan(cpi[pd.Timestamp("2025-10-01")]), "BLS không công bố CPI tháng 10/2025 — phải là NaN, không phải 0"
    assert cpi[pd.Timestamp("2025-09-01")] == pytest.approx(324.8)


def test_so_sanh_thang_theo_ngay(m, ban_le):
    tang = m.so_sanh_thang(ban_le, "2023-02", "2023-03")
    assert tang == pytest.approx(0.0311, abs=0.001), f"T3/T2 2023 = {tang:.3f}: tháng 2 có 28 ngày, tháng 3 có 31 — chia số ngày trước khi so"


def test_tang_truong_thuc_dau_nguoi(m, ban_le):
    tang = m.tang_truong_thuc_dau_nguoi(ban_le, m.doc_cpi(), m.doc_dan_so(), 1993, 2025)
    assert tang == pytest.approx(0.42, abs=0.01), f"tăng trưởng 1993→2025 = {tang:.2f} — đã trừ lạm phát và chia dân số chưa?"


def test_boxcox_khop_scipy(m, ban_le):
    y = ban_le.to_numpy()
    for lam in (0.0, 0.343, -0.5):
        assert np.allclose(m.boxcox(y, lam), special.boxcox(y, lam))
        assert np.allclose(m.boxcox_nguoc(m.boxcox(y, lam), lam), y)


def test_hieu_chinh_bias_log_normal(m):
    rng = np.random.default_rng(7)
    x = rng.lognormal(5.0, 0.6, 50_000)
    w = np.log(x)
    trung_vi = float(m.boxcox_nguoc(w.mean(), 0.0))
    trung_binh = float(m.boxcox_nguoc(w.mean(), 0.0, w.var(ddof=1)))
    assert trung_vi / x.mean() - 1 < -0.10
    assert abs(trung_binh / x.mean() - 1) < 0.03, f"đổi ngược có sigma2 phải gần trung bình thật: {trung_binh:.1f} vs {x.mean():.1f}"


def test_hieu_chinh_bias_lambda_khac_0(m):
    w, lam, s2 = np.array([30.0]), 0.343, 4.0
    goc = lam * w + 1
    ky_vong = goc ** (1 / lam) * (1 + s2 * (1 - lam) / (2 * goc**2))
    assert float(m.boxcox_nguoc(w, lam, s2)[0]) == pytest.approx(float(ky_vong[0]))


def test_guerrero_khop_statsmodels(m, ban_le):
    y = ban_le[:"2019-12"].to_numpy()
    _, lam_sm = BoxCox().transform_boxcox(y, method="guerrero", window_length=12)
    assert m.guerrero(y, 12) == pytest.approx(lam_sm, abs=0.005)


def test_bias_tren_tap_kiem_tra(m, ban_le):
    kq = m.danh_gia_bias(ban_le)
    assert kq["trung_binh"] > kq["trung_vi"], "dự báo trung bình phải cao hơn trung vị (exp(ŵ))"
    assert abs(kq["trung_binh"]) < abs(kq["trung_vi"])
