"""Bộ chấm buổi 1 — đánh giá dự báo trung thực và luôn có baseline."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

BASELINE = {"TB 4 tuần", "tuần trước", "trung bình", "giờ trước"}


@pytest.fixture(scope="module")
def m(nap):
    return nap("danh_gia")


@pytest.fixture(scope="module")
def chuoi(m, du_lieu):
    return m.doc_dien_theo_gio()


def _gia_lap(so_tuan: int = 12, seed: int = 1) -> pd.Series:
    """Chuỗi giả theo giờ bắt đầu thứ Hai: nhịp ngày + nhiễu."""
    rng = np.random.default_rng(seed)
    t = pd.date_range("2010-01-04", periods=so_tuan * 168, freq="h")
    y = 1 + 0.5 * np.sin(2 * np.pi * t.hour / 24) + rng.normal(0, 0.1, t.size)
    return pd.Series(y, index=t)


def test_doc_du_lieu(chuoi):
    assert chuoi.index.freqstr == "h"
    assert chuoi.index[0] == pd.Timestamp("2006-12-17 00:00")
    assert chuoi.index[-1] == pd.Timestamp("2010-11-21 23:00")
    assert len(chuoi) == 34464
    assert chuoi.isna().sum() == 431


def test_baseline_dung_cong_thuc(m):
    s = _gia_lap(5)
    assert np.allclose(m.du_bao_tuan_truoc(s), s.iloc[-168:].to_numpy())
    assert np.allclose(m.du_bao_tb_4_tuan(s), s.iloc[-672:].to_numpy().reshape(4, 168).mean(axis=0))


def test_mae_bo_qua_gio_thieu(m):
    assert m.mae([1.0, np.nan, 3.0], [2.0, 100.0, 3.0]) == pytest.approx(0.5)


def test_danh_gia_co_baseline(m):
    kq = m.danh_gia(_gia_lap(), moc="2010-02-15")
    thieu = BASELINE - set(kq.index)
    assert not thieu, f"bảng đánh giá thiếu baseline: {sorted(thieu)} — không có baseline thì MAE không nói lên gì"


def test_du_bao_khong_nhin_thay_tuong_lai(m):
    """Đổi số đo của tuần cuối cùng: mọi dự báo (kể cả cho tuần đó) phải giữ nguyên, chỉ cột y đổi."""
    s = _gia_lap()
    s2 = s.copy()
    s2.iloc[-168:] += 5
    a, b = m.du_bao_cuon(s, moc="2010-02-15"), m.du_bao_cuon(s2, moc="2010-02-15")
    cot = [c for c in a.columns if c not in ("goc", "y")]
    lech = [c for c in cot if not np.allclose(a[c].to_numpy(float), b[c].to_numpy(float), equal_nan=True)]
    assert not lech, f"dự báo {lech} đổi khi dữ liệu cần dự báo đổi → đã dùng dữ liệu đó để làm dự báo"


def test_moi_goc_dung_tam_168_gio(m):
    bang = m.du_bao_cuon(_gia_lap(), moc="2010-02-15")
    assert bang.groupby("goc").size().eq(168).all()
    assert (bang.index >= bang["goc"]).all()


def test_so_that_bang_lich_khong_dep_nhu_trong_mau(m, chuoi):
    kq = m.danh_gia(chuoi)
    assert kq["bảng lịch"] > 0.45, f"MAE bảng lịch {kq['bảng lịch']:.3f} — quá đẹp, kiểm lại dữ liệu dùng để làm dự báo"


def test_so_that_baseline_thang(m, chuoi):
    kq = m.danh_gia(chuoi)
    assert kq.index[0] == "TB 4 tuần"
    assert kq["TB 4 tuần"] == pytest.approx(0.4905, abs=0.002)
