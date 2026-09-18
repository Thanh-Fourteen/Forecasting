"""Bộ chấm buổi 8 — tương quan giả, quan hệ phi tuyến, độ trễ dẫn dắt, Granger."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def m(nap):
    return nap("tuong_quan")


@pytest.fixture(scope="module")
def dien(m, du_lieu):
    return m.ghep_tai_nhiet()


@pytest.fixture(scope="module")
def kinh_te(m, du_lieu):
    return m.doc_kinh_te()


def test_doc_du_lieu(dien, kinh_te):
    assert len(dien) == 8777 and dien["nhiet"].between(-10, 40).all()
    assert len(kinh_te) == 420 and kinh_te.index[0] == pd.Timestamp("1990-01-01")


def test_cdd_hdd(m):
    cdd, hdd = m.cdd_hdd(np.array([10.0, 18.33, 30.0]))
    assert np.allclose(cdd, [0, 0, 11.67], atol=0.01)
    assert np.allclose(hdd, [8.33, 0, 0], atol=0.01)


def test_tuong_quan_gia_phai_bao_cao_sai_phan(m, kinh_te):
    kq = m.tuong_quan_chuoi(kinh_te["cpi"], kinh_te["dan_so"])
    assert "r_sai_phan" in kq, "phải báo cả tương quan sau khi sai phân, không chỉ trên mức"
    assert kq["r_muc"] > 0.9 and abs(kq["r_sai_phan"]) < 0.3
    assert "dw" in kq and kq["dw"] < 0.5, "Durbin–Watson của hồi quy mức là bằng chứng chính của tương quan giả"
    assert "giả" in kq["ket_luan"].lower()


def test_phi_tuyen_pearson_bo_sot(m, dien):
    t, y = dien["nhiet"].to_numpy(), dien["tai"].to_numpy()
    r2_t = m.hoi_quy_don(t, y)["r2"]
    X = np.column_stack([np.ones(t.size), dien["cdd"].to_numpy(), dien["hdd"].to_numpy()])
    du = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
    r2_dd = 1 - du.var() / y.var()
    assert r2_dd > 2 * r2_t, f"tách CDD/HDD phải giải thích nhiều hơn hẳn (R² {r2_dd:.3f} so với {r2_t:.3f})"


def test_mutual_information_bat_quan_he_chu_u(m):
    rng = np.random.default_rng(0)
    x = rng.uniform(-2, 2, 2000)
    y = x**2 + 0.3 * rng.normal(size=2000)
    assert abs(m.tuong_quan(x, y)["pearson"]) < 0.1
    assert m.thong_tin_tuong_ho(x, y) > 0.3


def test_hoan_vi_theo_khoi_tranh_duong_tinh_gia(m):
    """Hai chuỗi AR(0,99) độc lập: hoán vị từng điểm cho p nhỏ giả; hoán vị theo khối thì không."""
    rng = np.random.default_rng(0)
    def ar(n=2000, phi=0.99):
        v = np.empty(n)
        v[0] = rng.normal()
        for i in range(1, n):
            v[i] = phi * v[i - 1] + rng.normal()
        return v
    x, y = ar(), ar()
    assert m.kiem_y_nghia_mi(x, y, do_dai_khoi=200, so_lan=100)["p"] > 0.05
    assert m.kiem_y_nghia_mi(x, y, do_dai_khoi=1, so_lan=100)["p"] < 0.05


def test_ccf_quy_uoc(m):
    rng = np.random.default_rng(1)
    x = rng.normal(size=1000)
    y = np.r_[np.zeros(3), x[:-3]] + 0.2 * rng.normal(size=1000)
    assert int(np.argmax(m.ccf_tu_viet(x, y, 8))) == 3, "ccf_tu_viet(x, y)[k] phải là corr(x_t, y_{t+k})"


def test_do_tre_sau_prewhitening(m, dien):
    tho = m.do_tre_dan_dat(dien["cdd"].to_numpy(), dien["tai"].to_numpy(), so_tre=30, bac=None)
    sach = m.do_tre_dan_dat(dien["cdd"].to_numpy(), dien["tai"].to_numpy(), so_tre=30)
    assert abs(tho["ccf"][24]) > 0.5, "CCF thô còn mang nhịp ngày của chính biến giải thích"
    assert abs(sach["ccf"][24]) < 0.1, "sau prewhitening, CCF phải sạch nhịp ngày — chưa lọc AR của x?"
    assert sach["tre"] == 0


def test_tuong_quan_truot_doi_dau(m, dien):
    ngay = dien.resample("D").mean()
    r = m.tuong_quan_truot(ngay["nhiet"], ngay["tai"], 90)
    assert r.iloc[:89].isna().all(), "cửa sổ 90 ngày chưa đủ dữ liệu thì phải là NaN (min_periods)"
    assert r.min() < -0.5 and r.max() > 0.5, "quan hệ nhiệt độ–tải đổi dấu giữa mùa đông và mùa hè"


def test_granger_khong_ket_luan_nhan_qua(m, dien):
    kq = m.granger_hai_chieu(pd.Series(dien["cdd"].to_numpy(), index=dien.index), dien["tai"], so_tre=4)
    assert kq["p_x_giup_du_bao_y"] < 0.05 and kq["p_y_giup_du_bao_x"] < 0.05
    assert "gây ra" not in kq["ket_luan"] or "KHÔNG" in kq["ket_luan"], "Granger không phải nhân quả"
    assert "HAI CHIỀU" in kq["ket_luan"].upper()
