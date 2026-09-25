"""Bộ chấm buổi 23 — Gradient boosting chuyên sâu.

Chấm `code/boosting.py` (mặc định) hoặc `dap-an/boosting.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tv.ro_ri import kiem_chia_tap, kiem_ro_ri


@pytest.fixture(scope="module")
def bo(nap, du_lieu):
    return nap("boosting")


@pytest.fixture(scope="module")
def mau(bo):
    """60 mã hàng: dữ liệu, bảng đặc trưng, phần học trước cutoff đầu."""
    df = bo.doc_ban_le(60)
    b = bo.bang(df)
    return df, b, b[b["t"] <= bo.cac_cutoff(df)[0]].reset_index(drop=True)


def test_dac_trung_khong_ro_ri(bo, mau):
    """Một mô hình cho cả 28 ngày tới: mọi đặc trưng của ngày t chỉ được dùng y tới ngày t − 28."""
    df = mau[0]
    df = df[df["unique_id"].isin(df["unique_id"].unique()[:4])]
    kq = kiem_ro_ri(bo.dac_trung, df, h=bo.H, cot_id="unique_id", cot_ds="t", cot_bo_qua=["ma", "ds"])
    assert not kq.co_ro_ri, str(kq)


def test_ham_mat_mat_cho_so_dem(bo):
    """Số món bán mỗi ngày: nhiều số 0, lệch phải — dùng hàm mất mát cho số đếm, không dùng bình phương (L2)."""
    assert bo.THAM_SO["objective"] in {"tweedie", "poisson"}, \
        f"objective = {bo.THAM_SO['objective']!r}: WRMSSE tệ hơn và dự báo có thể âm"


def test_cv_theo_thoi_gian(bo, mau):
    """Mỗi fold: mọi ngày kiểm nằm SAU mọi ngày học (không có tương lai trong phần học)."""
    b_hoc = mau[2]
    folds = bo.chia_cv(b_hoc)
    assert len(folds) >= 2
    for hoc, kiem in folds:
        kq = kiem_chia_tap(b_hoc.iloc[hoc], b_hoc.iloc[kiem], cot_id="unique_id", cot_ds="t")
        assert not kq.co_ro_ri, str(kq)


def test_wrmsse_vi_du_tay(bo):
    """Hai mã, một cutoff. A: phần học 0, 2, 0, 2 (bước nhảy² TB 4), lệch 2 → RMSSE 1; doanh thu 30.
    B: phần học 1, 2, 3, 4 (bước nhảy² TB 1), lệch 0 → RMSSE 0; doanh thu 10. WRMSSE = 0,75 × 1 + 0,25 × 0 = 0,75."""
    df = pd.DataFrame({"unique_id": ["A"] * 5 + ["B"] * 5, "t": list(range(5)) * 2,
                       "y": [0.0, 2, 0, 2, 5, 1, 2, 3, 4, 5],
                       "doanh_thu": [0.0, 10, 0, 20, 0, 0, 0, 5, 5, 0]})
    kq = pd.DataFrame({"unique_id": ["A", "B"], "t": [4, 4], "cutoff": [3, 3], "y": [5.0, 5], "du_bao": [3.0, 5]})
    assert bo.wrmsse(kq, df) == pytest.approx(0.75)


def test_shap_cong_lai_bang_du_bao(bo, mau):
    """Tổng đóng góp SHAP của một dòng = điểm thô của mô hình cho dòng đó."""
    b_hoc = mau[2]
    m = bo.huan_luyen(b_hoc, n_estimators=50)
    x = b_hoc.iloc[[100]]
    s = bo.shap_mot_dong(m, x)
    assert s.sum() == pytest.approx(float(m.predict(x[bo.DAC_TRUNG], raw_score=True)[0]), rel=1e-6)


def test_rang_buoc_don_dieu_theo_gia(bo, mau):
    """Với ràng buộc, dự báo trung bình không được tăng khi giá tăng."""
    b_hoc = mau[2]
    m = bo.huan_luyen(b_hoc, bo.tham_so_don_dieu(), n_estimators=100)
    luoi = np.linspace(*np.nanquantile(b_hoc["gia"], [0.05, 0.95]), 12)
    pd_ = bo.phu_thuoc_rieng(m, b_hoc.sample(2000, random_state=0), "gia", luoi)
    assert np.all(np.diff(pd_) <= 1e-9), np.round(pd_, 3)


def test_backtest_chi_dung_qua_khu(bo, mau):
    """Đổi mọi y SAU cutoff đầu: dự báo của cutoff đầu không được đổi."""
    df, _, _ = mau
    df = df[df["unique_id"].isin(df["unique_id"].unique()[:20])]
    c = bo.cac_cutoff(df)[0]
    df2 = df.assign(y=np.where(df["t"] > c, df["y"] + 50, df["y"]))
    a = bo.backtest(bo.bang(df), n_estimators=30)
    b = bo.backtest(bo.bang(df2), n_estimators=30)
    assert np.allclose(a[a["cutoff"] == c]["du_bao"], b[b["cutoff"] == c]["du_bao"])
