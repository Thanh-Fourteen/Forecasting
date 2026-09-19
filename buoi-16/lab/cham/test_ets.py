"""Bộ chấm buổi 16 — exponential smoothing và Theta.

Chấm `code/ets.py` (mặc định) hoặc `dap-an/ets.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def et(nap, du_lieu):
    return nap("ets")


@pytest.fixture(scope="module")
def tourism(et):
    return et.doc_tourism()


def test_ses_tinh_tay(et):
    """y = (10, 12, 11, 13), α = 0,5: khớp 10, 11, 11 (mỗi giá trị khớp chỉ dùng số tới bước trước), mức cuối 12."""
    khop, muc = et.ses_loc(np.array([10.0, 12.0, 11.0, 13.0]), 0.5)
    assert np.allclose(khop, [10.0, 11.0, 11.0]), f"giá trị khớp {khop} — đang dùng chính y_t để 'dự báo' y_t?"
    assert muc == pytest.approx(12.0)


def test_ses_khop_khong_ro_ri(et):
    """Bài kiểm nhiễu mục tiêu (buổi 13): giá trị khớp cho y_t không được đổi khi y_t đổi."""
    from tv.ro_ri import kiem_ro_ri
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"ds": np.arange(60), "y": 100 + np.cumsum(rng.normal(0, 3, 60))})

    def ham(d):
        khop, _ = et.ses_loc(d["y"].to_numpy(), 0.3)
        return pd.DataFrame({"ds": d["ds"].to_numpy()[1:], "khop": khop})

    kq = kiem_ro_ri(ham, df, h=1, cot_id=None)
    assert not kq.co_ro_ri, str(kq)


def test_ses_toi_uu_khop_statsforecast(et, tourism):
    """SES tự tối ưu bằng scipy phải cho cùng dự báo với statsforecast (chuỗi năm T249)."""
    from statsforecast.models import SimpleExponentialSmoothingOptimized
    y = et.theo_nam(tourism["T249"])
    kq = et.ses_toi_uu(y)
    assert 0.3 < kq["alpha"] < 0.9, f"α = {kq['alpha']:.3f}: α sát 1 và SSE ≈ 0 nghĩa là đang khớp bằng chính y_t"
    ref = SimpleExponentialSmoothingOptimized().fit(y).predict(1)["mean"][0]
    assert et.ses_du_bao(y, kq["alpha"], 1)[0] == pytest.approx(ref, rel=1e-3)


def test_holt_tinh_tay(et):
    """Chuỗi tăng đều 2 mỗi bước: Holt (α = β = 0,5) dự báo tiếp 18, 20."""
    assert np.allclose(et.holt_du_bao(np.array([10.0, 12.0, 14.0, 16.0]), 0.5, 0.5, 2), [18.0, 20.0])


def test_theta_la_ses_cong_nua_do_doc(et):
    y = np.array([10.0, 12.0, 14.0, 16.0])      # độ dốc 2; α = 1 → mức cuối 16
    assert np.allclose(et.theta_du_bao(y, 2, alpha=1.0), [17.0, 18.0])


def test_holt_winters_mac_dinh_hop_du_lieu(et):
    """Hành khách EU: biên độ mùa vụ tăng theo mức → Holt–Winters mặc định phải là dạng nhân."""
    y = et.doc_hanh_khach()
    bien_do = et.bien_do_mua_vu(y)
    assert bien_do.iloc[-1] > 1.3 * bien_do.iloc[0]
    kq = et.du_bao_hanh_khach(y)
    assert kq["MAPE"] < 2.5, f"MAPE 2018–2019 = {kq['MAPE']:.2f}% — mùa vụ cộng trên chuỗi có biên độ tăng?"


def test_ty_le_phu_dem_dung(et):
    kq = pd.DataFrame({"y": [1.0, 5.0, 9.0, 3.0], "X-lo-80": [0.0, 0.0, 0.0, 4.0], "X-hi-80": [2.0, 6.0, 8.0, 5.0]})
    assert et.ty_le_phu(kq, "X", 80) == pytest.approx(0.5)


def test_autoets_thang_snaive_co_y_nghia(et, tourism):
    """Backtest 2 cửa sổ trên 366 chuỗi: AutoETS có MASE thấp hơn seasonal naive, DM p < 0,05."""
    df = et.dang_dai(tourism)
    kq = et.backtest_tourism(df)
    mase = et.mase_theo_chuoi(kq, df)
    bang = et.kiem_dinh_so_snaive(mase).set_index("mô hình")
    assert bang.loc["AutoETS", "MASE trung bình"] < bang.loc["SeasonalNaive", "MASE trung bình"]
    assert bang.loc["AutoETS", "p"] < 0.05
    assert 0.7 < et.ty_le_phu(kq, "AutoETS", 80) < 0.9
