"""Bộ chấm buổi 7 — ACF tự viết, nhiễu trắng, tính dừng bằng CẢ ADF lẫn KPSS, sai phân vừa đủ."""
from __future__ import annotations

import numpy as np
import pytest
from statsmodels.tsa.stattools import acf


@pytest.fixture(scope="module")
def m(nap):
    return nap("tu_tuong_quan")


@pytest.fixture(scope="module")
def chuoi(m):
    return m.sinh_bon_chuoi()


def test_acf_khop_statsmodels(m, chuoi):
    y = chuoi["AR(1) φ=0,7"]
    assert np.allclose(m.acf_tu_viet(y, 20), acf(y, nlags=20, adjusted=False, fft=True))


def test_dai_nhieu_trang(m):
    assert m.dai_nhieu_trang(500) == pytest.approx(1.96 / np.sqrt(500))


def test_ljung_box_tru_bac_tu_do(m, chuoi):
    _, p0 = m.ljung_box(chuoi["nhiễu trắng"], 10)
    _, p2 = m.ljung_box(chuoi["nhiễu trắng"], 10, so_tham_so=2)
    assert p0 == pytest.approx(0.245, abs=0.01)
    assert p2 < p0, "trừ bậc tự do cho tham số đã ước lượng phải làm p nhỏ đi"


def test_kiem_dinh_co_ca_kpss(m, chuoi):
    kq = m.kiem_dinh(chuoi["nhiễu trắng"])
    assert {"adf_p", "kpss_p"} <= set(kq), "phải chạy CẢ HAI: ADF (H0 có nghiệm đơn vị) và KPSS (H0 dừng)"


def test_dang_xac_dinh_doi_ket_qua(m, chuoi):
    xu_huong = chuoi["xu hướng 0,05t"]
    assert m.kiem_dinh(xu_huong)["kpss_p"] < 0.05
    assert m.kiem_dinh(xu_huong, co_xu_huong=True)["kpss_p"] > 0.05, "với dạng 'ct', KPSS không bác bỏ chuỗi dừng quanh xu hướng"
    assert m.kiem_dinh(xu_huong, co_xu_huong=True)["adf_p"] < 0.05


def test_ket_luan_bon_chuoi(m, chuoi):
    assert m.ket_luan(chuoi["nhiễu trắng"]) == "dừng"
    assert "sai phân" in m.ket_luan(chuoi["random walk"])
    assert "xu hướng" in m.ket_luan(chuoi["xu hướng 0,05t"], co_xu_huong=True)


def test_so_lan_sai_phan_khong_thua(m, chuoi):
    assert m.so_lan_sai_phan(chuoi["nhiễu trắng"]) == 0, "nhiễu trắng đã dừng — sai phân là thừa"
    assert m.so_lan_sai_phan(chuoi["AR(1) φ=0,7"]) == 0
    assert m.so_lan_sai_phan(chuoi["random walk"]) == 1


def test_dau_hieu_sai_phan_thua(m, chuoi):
    d = m.dau_hieu_sai_phan_thua(chuoi["nhiễu trắng"])
    assert d["acf1_sau"] < -0.4, "sai phân chuỗi đã dừng → ACF(1) ≈ −0,5"
    assert d["sd_sau"] > d["sd_truoc"], "sai phân thừa làm phương sai tăng"


def test_du_lieu_that(m, du_lieu):
    r = m.acf_tu_viet(m.doc_luot_thue(), 168)
    assert r[168] > r[24] > 0.5, "lượt thuê: mùa vụ tuần mạnh hơn mùa vụ ngày"
    gdp = np.log(m.doc_gdp()).diff().dropna()
    kq = m.kiem_dinh(gdp)
    assert kq["adf_p"] < 0.01 and kq["kpss_p"] < 0.05, "đây là ví dụ thật hai kiểm định mâu thuẫn"
