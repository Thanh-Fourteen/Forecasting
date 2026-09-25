"""Bộ chấm buổi 27 — dự báo Bayes. Mỗi test kiểm một hành vi; thông báo lỗi nói cần sửa gì.

Chẩn đoán hội tụ là BẮT BUỘC: mọi posterior dùng để dự báo phải có r_hat < 1,01, ESS ≥ 400, 0 divergence.
"""
from __future__ import annotations

import numpy as np
import pytest

NGUONG = {"r_hat": 1.01, "ess_bulk": 400, "divergence": 0}


def dat(cd: dict) -> bool:
    return cd["r_hat_max"] < NGUONG["r_hat"] and cd["ess_bulk_min"] >= NGUONG["ess_bulk"] and cd["divergence"] == 0


@pytest.fixture(scope="session")
def by(nap, du_lieu):
    return nap("bayes")


@pytest.fixture(scope="session")
def car(by):
    return by.chia_car_parts(by.doc_car_parts())


def test_chia_khong_dung_thang_cham(by, car):
    Y = by.doc_car_parts()
    T = Y.shape[1]
    j = 0
    so_thang = len(car["hoc"][j])
    assert car["kiem"].shape[1] == by.THANG_KIEM
    assert np.array_equal(car["hoc"][j], Y.loc[car["ma"][j]].to_numpy()[T - by.THANG_KIEM - so_thang:T - by.THANG_KIEM]), \
        "phần học phải là các tháng NGAY TRƯỚC 12 tháng chấm, không chồng lên chúng"


def test_prior_predictive_hop_ly(by, car):
    v = by.tien_nghiem(by.mo_hinh_phan_cap(car["hoc"]))
    q99 = float(np.quantile(v, 0.99))
    assert q99 < 1000, (f"prior sinh ra {q99:.3g} món/tháng ở phân vị 99% — vô lý với phụ tùng bán vài món mỗi tháng. "
                        "Thu hẹp PRIOR rồi kiểm lại bằng prior predictive (mục 4.2)")


def test_cong_chan_doan_du_ba_dieu_kien(by):
    tot = {"r_hat_max": 1.002, "ess_bulk_min": 3000.0, "divergence": 0}
    assert by.dung_duoc(tot), "posterior tốt phải được chấp nhận"
    for sai, ly_do in (({"divergence": 27}, "có divergence"), ({"ess_bulk_min": 120.0}, "ESS quá nhỏ"),
                       ({"r_hat_max": 1.03}, "r_hat ≥ 1,01")):
        assert not by.dung_duoc({**tot, **sai}), f"dung_duoc phải từ chối posterior {ly_do} (mục 4.3)"


def test_phan_cap_hoi_tu_va_thang_khong_gop(by, car):
    _, idata = by.hoc_phan_cap(car["hoc"])
    cd = by.chan_doan(idata, ["mu", "tau", "theta"])
    assert dat(cd), f"mô hình phân cấp chưa hội tụ: {cd}"
    L = by.ba_cach_gop(car["hoc"], idata)
    assert by.rmse(car["kiem"], L["gop_mot_phan"]) < by.rmse(car["kiem"], L["khong_gop"]), \
        "gộp một phần phải thắng không gộp trên 12 tháng chấm (mục 4.4)"


def test_gp_hoi_tu(by):
    df = by.doc_xe_dap()
    m, _, cd = by.hoc_gp(df)
    assert len(m["X"].get_value()) == len(df) - by.NGAY_KIEM, "GP chỉ được học trên dữ liệu trước 60 ngày chấm"
    assert dat(cd), (f"GP chưa dùng được: {cd}. Divergence nghĩa là NUTS không đi hết posterior; xem các thành phần kernel "
                     "có tranh nhau giải thích cùng một đường không (mục 4.6)")
