"""Bộ chấm buổi 6 — phân rã đúng một chuỗi có hai mùa vụ (ngày + tuần)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def m(nap):
    return nap("phan_ra")


@pytest.fixture(scope="module")
def y(m, du_lieu):
    return m.doc_nhu_cau()


@pytest.fixture(scope="module")
def bang(m, y):
    return m.phan_ra(m.lap_cho_trong(y))


def test_doc_du_lieu(y):
    assert len(y) == 8784
    assert y.index[0] == pd.Timestamp("2024-01-01 06:00")
    assert y.isna().sum() == 47, "cột Demand (MW) gốc có 47 giờ trống (hai ngày đổi giờ DST)"


def test_do_manh_dung_cong_thuc(m):
    rng = np.random.default_rng(1)
    n = 500
    b = pd.DataFrame({"trend": np.linspace(0, 10, n), "seasonal_24": np.sin(np.arange(n)), "resid": rng.normal(0, 0.5, n)})
    b["y"] = b.sum(axis=1)
    kq = m.do_manh(b)
    assert kq["F_T"] == pytest.approx(1 - b.resid.var() / (b.trend + b.resid).var())
    assert kq["F_S_24"] == pytest.approx(1 - b.resid.var() / (b.seasonal_24 + b.resid).var())


def test_khong_mat_dau_cuoi(bang):
    assert bang[["trend", "resid"]].notna().all().all(), "xu hướng/phần dư có NaN ở đầu–cuối chuỗi"


def test_tach_mua_vu_tuan(bang, m):
    assert "seasonal_168" in bang.columns, "chưa có thành phần mùa vụ tuần (168 giờ)"
    assert m.do_manh(bang)["F_S_168"] > 0.3


def test_phan_du_khong_con_mau_hinh_thu_gio(m, bang):
    ty_le = m.ty_le_mau_hinh_con_lai(bang, ("dayofweek", "hour"))
    assert ty_le < 0.001, f"phần dư còn mẫu hình thứ×giờ ({ty_le:.4f} phương sai của y)"


def test_mua_vu_ngay_doi_theo_mua(m, bang):
    ty_le = m.ty_le_mau_hinh_con_lai(bang, ("month", "hour"))
    assert ty_le < 0.01, f"phần dư còn mẫu hình tháng×giờ ({ty_le:.4f}) — mùa vụ ngày bị ép cố định cả năm"


def test_robust_giu_gio_hong_trong_phan_du(m, y):
    b = m.phan_ra(m.lap_cho_trong(y), robust=True)
    assert "seasonal_168" in b.columns
    assert b.loc["2024-11-21 17:00", "resid"] < -33_000, "giờ số liệu hỏng 21/11/2024 17:00 (56.260 MW) phải nằm trọn trong phần dư"
