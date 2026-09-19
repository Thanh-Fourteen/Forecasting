"""Bộ chấm buổi 19 — Nhu cầu gián đoạn.

Chấm `code/gian_doan.py` (mặc định) hoặc `dap-an/gian_doan.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def gd(nap, du_lieu):
    return nap("gian_doan")


@pytest.fixture(scope="module")
def mau(gd):
    """200 chuỗi đầu (đủ nhanh), backtest 12 cutoff."""
    df = gd.doc_car_parts()
    df = df[df["unique_id"].isin(df["unique_id"].unique()[:200])]
    return df, gd.ma_tran(df), gd.backtest_car_parts(df)


def _chuoi_ngau_nhien(seed: int, n: int = 40) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.where(rng.random(n) < 0.3, rng.integers(1, 6, n), 0).astype(float)


def test_phan_loai_vi_du_tay(gd):
    kq = gd.phan_loai(np.array([0, 3, 0, 0, 5, 0, 4, 0]))
    assert kq["ADI"] == pytest.approx(8 / 3)
    assert kq["CV2"] == pytest.approx((np.std([3, 5, 4]) / 4) ** 2)
    assert kq["loại"] == "gián đoạn"


def test_croston_va_sba_khop_statsforecast(gd):
    from statsforecast.models import CrostonClassic, CrostonSBA
    for seed in range(5):
        y = _chuoi_ngau_nhien(seed)
        assert gd.croston(y) == pytest.approx(float(CrostonClassic().forecast(y, 1)["mean"][0]), rel=1e-9)
        assert gd.croston(y, sba=True) == pytest.approx(float(CrostonSBA().forecast(y, 1)["mean"][0]), rel=1e-9)


def test_tsb_khop_statsforecast(gd):
    from statsforecast.models import TSB
    for seed in range(5):
        y = _chuoi_ngau_nhien(seed)
        ref = float(TSB(alpha_d=0.1, alpha_p=0.1).forecast(y, 1)["mean"][0])
        assert gd.tsb(y) == pytest.approx(ref, rel=1e-9), "TSB: xác suất có bán phải cập nhật ở MỌI kỳ, kể cả kỳ bán 0"


def test_tsb_giam_khi_ngung_ban(gd):
    """Mặt hàng bán đều rồi ngừng hẳn 24 tháng: dự báo TSB phải giảm rõ, Croston thì đứng yên."""
    y = np.r_[np.tile([2.0, 0.0], 12), np.zeros(24)]
    assert gd.tsb(y) < 0.3 * gd.tsb(y[:24])
    assert gd.croston(y) == pytest.approx(gd.croston(y[:24]))


def test_danh_gia_dung_chi_so_chia_thang(gd, mau):
    """Chuỗi 76% số 0: MAPE vỡ (hoặc âm thầm bỏ tháng 0); dùng RMSSE, MASE."""
    df, Y, kq = mau
    bang = gd.danh_gia(kq, Y)
    assert "MAPE" not in bang.columns, "MAPE trên chuỗi gián đoạn chỉ chấm các tháng có bán — bỏ nó"
    assert {"RMSSE", "MASE"} <= set(bang.columns)
    assert np.isfinite(bang[["RMSSE", "MASE"]].to_numpy()).all()
    k1 = kq[kq["buoc_h"] == 1]
    uid = Y.index[0]
    hoc = Y.loc[uid].to_numpy()[:int(k1["ds"].min())]
    dong = k1[k1["unique_id"] == uid]
    if np.mean(np.diff(hoc) ** 2) > 0:
        tay = np.sqrt(np.mean((dong["y"] - dong["TSB"]) ** 2) / np.mean(np.diff(hoc) ** 2))
        bang1 = gd.danh_gia(kq[kq["unique_id"] == uid], Y.loc[[uid]])
        assert bang1.loc["TSB", "RMSSE"] == pytest.approx(tay, rel=1e-9)


def test_mo_phong_ton_kho_vi_du_tay(gd):
    """Nhu cầu 1, 2, 2; S = 3; hàng đặt cuối tháng 1 về đầu tháng 3: tồn 2 món-tháng, thiếu 1 → chi phí 2 + 9 = 11."""
    kq = gd.mo_phong_ton_kho(np.array([[1, 2, 2]]), np.array([[3, 3, 3]]), lead=1)
    assert kq["chi phí mỗi mã"] == pytest.approx(11)
    assert kq["tỷ lệ đáp ứng"] == pytest.approx(0.8)


def test_chon_mo_hinh_theo_chi_phi(gd):
    bang = pd.DataFrame({"RMSSE": [0.70, 0.68], "MASE": [0.8, 1.1], "chi phí mỗi mã": [43.0, 28.0]},
                        index=pd.Index(["Zero", "IMAPA"], name="mô hình"))
    assert gd.chon_mo_hinh(bang) == "IMAPA", "đặt hàng theo mô hình có chi phí tồn kho thấp nhất, không theo MAE/MAPE"


def test_backtest_chi_dung_qua_khu(gd, mau):
    """Đổi mọi giá trị SAU cutoff đầu tiên: dự báo của cửa sổ đầu không được đổi."""
    df, _, kq = mau
    df = df[df["unique_id"].isin(df["unique_id"].unique()[:30])]
    kq1 = gd.backtest_car_parts(df)
    cutoff = kq1["cutoff"].min()
    df2 = df.copy()
    df2.loc[df2["ds"] > cutoff, "y"] += 7
    kq2 = gd.backtest_car_parts(df2)
    a, b = kq1[kq1["cutoff"] == cutoff], kq2[kq2["cutoff"] == cutoff]
    for m in gd.MO_HINH:
        assert np.allclose(a[m].to_numpy(), b[m].to_numpy()), f"{m} đổi khi dữ liệu tương lai đổi"
