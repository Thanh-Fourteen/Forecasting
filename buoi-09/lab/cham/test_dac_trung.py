"""Bộ chấm buổi 9 — đặc trưng, khả năng dự báo, phân cụm hình dạng, ABC–XYZ."""
from __future__ import annotations

import numpy as np
import pytest

MAU = 500  # đủ để các tương quan ổn định mà test vẫn nhanh


@pytest.fixture(scope="module")
def m(nap):
    return nap("dac_trung")


@pytest.fixture(scope="module")
def chuoi(m, du_lieu):
    return m.lay_mau(m.doc_tsf(), MAU)


@pytest.fixture(scope="module")
def bang(m, chuoi):
    return m.bang_dac_trung(chuoi).join(m.danh_gia_kho_de(chuoi))


def test_doc_tsf(m, du_lieu):
    tat_ca = m.doc_tsf()
    assert len(tat_ca) == 48_000
    assert min(v.size for v in tat_ca.values()) == 60


def test_lay_mau_cat_cung_do_dai(chuoi):
    assert len(chuoi) == MAU
    assert {v.size for v in chuoi.values()} == {138}, "phải cắt mọi chuỗi về cùng độ dài (120 học + 18 chấm)"


def test_entropy_pho(m):
    rng = np.random.default_rng(0)
    nhieu = rng.normal(size=480)
    mua_vu = np.sin(2 * np.pi * np.arange(480) / 12) + 0.1 * rng.normal(size=480)
    assert m.entropy_pho(nhieu) > 0.85
    assert m.entropy_pho(mua_vu) < 0.35


def test_du_20_dac_trung(m, chuoi):
    dt = m.dac_trung_mot_chuoi(next(iter(chuoi.values()))[:-18])
    assert len(dt) >= 20, f"cần ít nhất 20 đặc trưng, đang có {len(dt)}"
    t = np.arange(240)
    manh = 10 + 0.02 * t + 3 * np.sin(2 * np.pi * t / 12)
    assert m.dac_trung_mot_chuoi(manh)["do_manh_mua_vu"] > 0.9


def test_bao_ca_smape_va_hai_he_so(m, bang):
    bang_tq = m.tuong_quan_kho_de(bang)
    assert "spearman" in bang_tq.columns, "báo cả Spearman: quan hệ ở đây không tuyến tính"
    do = set(bang_tq["thước đo"])
    assert "smape_snaive" in do, "MASE của seasonal naive tự chuẩn hoá — phải báo thêm một thước đo khác"


def test_entropy_du_bao_duoc_do_kho(m, bang):
    tq = m.tuong_quan_kho_de(bang).set_index(["đặc trưng", "thước đo"])
    assert tq.loc[("entropy_pho", "smape_snaive"), "spearman"] > 0.1, "entropy cao → sMAPE của snaive cao hơn"


def test_mase_cua_snaive_luon_quanh_1(bang):
    """Bằng chứng số cho việc MASE không dùng được để xếp hạng độ khó với chính seasonal naive."""
    assert abs(bang["mase_snaive"].median() - 1.0) < 0.15


def test_phan_cum_theo_hinh_dang(m):
    """Nhân một chuỗi với 100 không được đổi cụm: phân cụm phải theo HÌNH DẠNG, không theo mức."""
    rng = np.random.default_rng(1)
    t = np.arange(120)
    goc = {f"mua_vu_{i}": 10 + 3 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 0.3, 120) for i in range(6)}
    goc.update({f"xu_huong_{i}": 10 + 0.1 * t + rng.normal(0, 0.3, 120) for i in range(6)})
    goc["mua_vu_to"] = goc["mua_vu_0"] * 100
    nhan, _ = m.phan_cum_dtw(goc, so_cum=2)
    assert nhan["mua_vu_to"] == nhan["mua_vu_0"], "chuỗi cùng hình dạng khác biên độ phải vào cùng cụm (chuẩn hoá z-score)"


def test_chien_luoc_tach_duoc_chuoi_vo_vong(m, bang):
    chien_luoc = m.de_xuat_chien_luoc(bang)
    assert (chien_luoc == "dùng baseline").sum() > 0, "phải tách ra nhóm chuỗi không đáng tune"
    kho = bang.loc[chien_luoc == "dùng baseline", "smape_snaive"].median()
    de = bang.loc[chien_luoc != "dùng baseline", "smape_snaive"].median()
    assert kho > 1.5 * de, f"nhóm 'dùng baseline' phải thật sự khó hơn ({kho:.1f} vs {de:.1f})"


def test_abc_xyz(m, du_lieu):
    bang_hang = m.abc_xyz(m.doc_ban_le())
    assert set(bang_hang["abc"]) == {"A", "B", "C"} and set(bang_hang["xyz"]) == {"X", "Y", "Z"}
    ty_le_a = bang_hang.loc[bang_hang["abc"] == "A", "sum"].sum() / bang_hang["sum"].sum()
    assert ty_le_a > 0.5, "20% mặt hàng đầu phải chiếm phần lớn doanh thu (nguyên tắc Pareto)"
