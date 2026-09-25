"""Bộ chấm buổi 22 — Biến dự báo thành bài toán hồi quy.

Chấm `code/hoi_quy.py` (mặc định) hoặc `dap-an/hoi_quy.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tv.ro_ri import kiem_ro_ri


@pytest.fixture(scope="module")
def hq(nap, du_lieu):
    return nap("hoi_quy")


@pytest.fixture(scope="module")
def mau(hq):
    """40 chuỗi, đủ nhanh cho mọi test."""
    return hq.doc_web_traffic(40)


def test_bang_lag_vi_du_tay(hq):
    X, y = hq.bang_lag(np.array([10.0, 12, 11, 13, 15]), 2)
    assert X.tolist() == [[12, 10], [11, 12], [13, 11]]
    assert y.tolist() == [11, 13, 15]


def test_de_quy_dung_du_bao_cua_chinh_no(hq):
    """Mô hình 'trung bình 2 số gần nhất': 10, 20 → 15 → 17,5 → 16,25."""
    class TrungBinh:
        def predict(self, X):
            return X.mean(axis=1)
    assert hq.du_bao_de_quy(TrungBinh(), np.array([10.0, 20.0]), 3, 2) == pytest.approx([15, 17.5, 16.25])


@pytest.mark.parametrize("h", [1, 7, 14])
def test_dac_trung_truc_tiep_khong_ro_ri(hq, mau, h):
    """Đặc trưng cho tầm h chỉ được dùng z tới ngày ds − h (bài nhiễu mục tiêu của tv.ro_ri)."""
    df = mau[mau["unique_id"].isin(mau["unique_id"].unique()[:5])][["unique_id", "ds", "z"]]
    kq = kiem_ro_ri(lambda d: hq.dac_trung(d, h), df, h=h, cot_y="z", cot_bo_qua=["thu"])
    assert not kq.co_ro_ri, f"tầm h = {h}:\n{kq}"


def test_chuan_hoa_theo_chuoi(hq, mau):
    """Cộng hằng số 3 vào z của một chuỗi (gấp ~20 lần lượt xem): các lag đã chuẩn hoá không đổi, chỉ `muc` tăng 3."""
    df = mau[mau["unique_id"] == mau["unique_id"].iloc[0]][["unique_id", "ds", "z"]]
    a = hq.dac_trung(df, 7).dropna()
    b = hq.dac_trung(df.assign(z=df["z"] + 3), 7).dropna()
    cot = [c for c in a.columns if c.startswith("lag_")]
    assert np.allclose(a[cot], b[cot])
    assert np.allclose(b["muc"] - a["muc"], 3)


def test_truc_tiep_khong_nhin_tuong_lai(hq, mau):
    """Đổi mọi z SAU cutoff đầu tiên: dự báo direct của cutoff đó không được đổi."""
    df = mau[mau["unique_id"].isin(mau["unique_id"].unique()[:12])].reset_index(drop=True)
    cutoff = hq.cac_cutoff(df)[0]
    df2 = df.copy()
    df2.loc[df2["ds"] > cutoff, "z"] += 5
    a = hq.chien_luoc(df, h=3)
    b = hq.chien_luoc(df2, h=3)
    a, b = a[a["cutoff"] == cutoff], b[b["cutoff"] == cutoff]
    for c in ["recursive", "direct", "mimo"]:
        assert np.allclose(a[c].to_numpy(), b[c].to_numpy()), f"{c} đổi khi dữ liệu sau cutoff đổi"


def test_cay_ngoai_suy_duoc_xu_huong(hq):
    """Chuỗi tăng đều 2 mỗi ngày: dự báo 7 ngày tới phải tiếp tục tăng, vượt số lớn nhất đã thấy."""
    rng = np.random.default_rng(0)
    y = 50 + 2 * np.arange(120) + rng.normal(0, 1, 120)
    p = hq.du_bao_cay(y, 7)
    assert p[-1] > y.max() + 5, f"dự báo {p.round(1)} đứng ở mức cũ; số lớn nhất đã thấy {y.max():.1f}"


def test_rmsse_vi_du_tay(hq):
    """Một chuỗi: phần học 0, 1, 0, 1 (bước nhảy² trung bình 1); dự báo lệch 2 → RMSSE = 2."""
    ngay = pd.date_range("2020-01-01", periods=6)
    df = pd.DataFrame({"unique_id": "A", "ds": ngay, "z": [0.0, 1, 0, 1, 5, 5]})
    kq = pd.DataFrame({"unique_id": "A", "ds": ngay[4:], "cutoff": ngay[3], "z": [5.0, 5], "m": [3.0, 7]})
    assert hq.rmsse_tung_chuoi(kq, df, ["m"]).loc["A", "m"] == pytest.approx(2.0)


def test_global_thang_local_va_seasonal_naive(hq, mau):
    """Trên 40 chuỗi: LightGBM global phải thắng seasonal naive (RMSSE trung bình)."""
    kq = hq.backtest_toan_cuc(mau).merge(hq.backtest_cuc_bo(mau).drop(columns="z"), on=["unique_id", "ds", "cutoff"])
    r = hq.rmsse_tung_chuoi(kq, mau, ["LightGBM", "SeasonalNaive"]).mean()
    assert r["LightGBM"] < r["SeasonalNaive"]
