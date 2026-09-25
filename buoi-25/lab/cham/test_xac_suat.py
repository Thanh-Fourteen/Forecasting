"""Bộ chấm buổi 25 — dự báo xác suất. Mỗi test kiểm một hành vi; thông báo lỗi nói cần sửa gì."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="session")
def xs(nap, du_lieu):
    return nap("xac_suat")


@pytest.fixture(scope="session")
def df(xs):
    return xs.doc_dien()


@pytest.fixture(scope="session")
def R(xs, df):
    return xs.backtest(df)


@pytest.fixture(scope="session")
def nam_kiem(xs, R):
    return (R["ds"] >= xs.NAM_KIEM).to_numpy()


def test_pinball_khop_scoringrules(xs):
    import scoringrules as sr

    rng = np.random.default_rng(0)
    y, q = rng.normal(size=500), rng.normal(size=500)
    for tau in (0.1, 0.5, 0.9):
        assert xs.pinball(y, q, tau) == pytest.approx(float(np.mean(sr.quantile_score(y, q, tau))), rel=1e-9), \
            f"pinball lệch scoringrules.quantile_score ở tau = {tau} (mục 4.2)"


def test_crps_mau_khop_scoringrules(xs):
    import scoringrules as sr

    rng = np.random.default_rng(1)
    y = rng.normal(size=300)
    mau = rng.normal(size=(300, 50))
    tu_viet, thu_vien = xs.crps_mau(y, mau), float(np.mean(sr.crps_ensemble(y, mau)))
    assert tu_viet == pytest.approx(thu_vien, rel=1e-9), (
        f"crps_mau = {tu_viet:.4f}, scoringrules.crps_ensemble = {thu_vien:.4f}. CRPS từ mẫu gồm hai phần: trung bình "
        "|X − y| TRỪ nửa trung bình |X − X'| (mục 4.3)")
    assert xs.crps_mau([5.0], [[2.0, 4.0, 6.0]]) == pytest.approx(7 / 9), "ví dụ tay mục 4.3: mẫu (2, 4, 6), y = 5"


def test_wis_bang_tong_pinball(xs):
    rng = np.random.default_rng(2)
    y = rng.normal(size=400)
    Q = np.sort(rng.normal(size=(400, len(xs.MUC))), axis=1)
    tong = sum(xs.pinball(y, Q[:, i], t) for i, t in enumerate(xs.MUC)) / ((len(xs.MUC) - 1) / 2 + 0.5)
    assert xs.wis(y, Q) == pytest.approx(tong, rel=1e-9), "WIS phải bằng tổng pinball của mọi mức chia (K + ½) (mục 4.3)"
    assert xs.wis([10.0], np.array([[5.0, 8.0, 9.0]]), (0.1, 0.5, 0.9)) == pytest.approx(1.6), "ví dụ tay mục 4.3"


def test_dac_trung_khong_ro_ri(xs, df):
    from tv.ro_ri import kiem_ro_ri

    d = df.iloc[:24 * 120].copy()
    kq = kiem_ro_ri(lambda x: xs.dac_trung(x)[["ds", "muc", "lag24", "lag48", "lag168"]], d, h=24, cot_id=None)
    assert not kq.co_ro_ri, f"đặc trưng dùng nhu cầu chưa biết lúc dự báo 24 giờ tới:\n{kq}"


def test_quantile_lightgbm_khong_crossing(xs, R):
    Q = xs.du_bao_quantile(R)
    so_dong = int((np.diff(Q, axis=1) < 0).any(axis=1).sum())
    assert so_dong == 0, (f"{so_dong} giờ có quantile mức cao NHỎ HƠN quantile mức thấp (crossing). "
                          "Sửa sua_crossing (mục 4.2)")


@pytest.mark.parametrize("ten", ["quantile_tu_phan_du", "du_bao_quantile"])
def test_calibration_tung_muc(xs, R, nam_kiem, ten):
    Q = getattr(xs, ten)(R)[nam_kiem]
    y = R["y"].to_numpy()[nam_kiem]
    thuc = xs.ty_le_duoi(y, Q)
    lech = np.abs(thuc - np.array(xs.MUC))
    assert lech.max() < 0.05, (
        f"{ten}: ở mức {xs.MUC[int(lech.argmax())]} chỉ {thuc[lech.argmax()]:.1%} giờ nằm dưới quantile "
        f"(lệch {lech.max() * 100:.1f} điểm phần trăm, cần < 5). Khoảng lấy từ phần dư trên phần học thì quá hẹp (mục 4.1)")


def test_quantile_tu_phan_du_chi_dung_qua_khu(xs, R):
    """Quantile của một tháng không được đổi khi sai số của chính tháng đó (hay sau đó) đổi."""
    R2 = R.copy()
    sau = R2["ds"] >= pd.Timestamp("2025-06-01")
    R2.loc[sau, "y"] = R2.loc[sau, "y"] + 50_000
    thang = (R["ds"] >= "2025-06-01") & (R["ds"] < "2025-07-01")
    a, b = xs.quantile_tu_phan_du(R)[thang.to_numpy()], xs.quantile_tu_phan_du(R2)[thang.to_numpy()]
    assert np.allclose(a, b, equal_nan=True), "quantile tháng 6 dùng sai số của tháng 6 trở đi — rò rỉ tương lai"


def test_pot_muc_10_nam(xs):
    t = xs.doc_nhiet_do_toi_da()
    kq = xs.pot(t, 39.0)
    assert 60 <= kq["so_dot"] <= 120, f"số đợt vượt 39 °C = {kq['so_dot']}, kiểm lại cách tách đợt (mục 4.5)"
    assert 40.5 < xs.muc_lap_lai(kq, 10) < 42.5, "mức 10 năm nằm ngoài khoảng hợp lý (mục 4.5)"
