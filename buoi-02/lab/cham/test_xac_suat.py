"""Buổi 2 — quantile tự viết, khoảng dự báo giữ đúng hình dạng, khoảng tin cậy bootstrap cho chuỗi tự tương quan."""
import numpy as np
import pytest


@pytest.fixture(scope="module")
def xs(nap):
    return nap("xac_suat")


def test_quantile_khop_numpy(xs):
    rng = np.random.default_rng(1)
    for n in (1, 2, 7, 100):
        x = rng.lognormal(size=n)
        q = np.linspace(0, 1, 21)
        assert np.allclose(xs.quantile_tu_viet(x, q), np.quantile(x, q)), f"lệch np.quantile (loại 7) khi n={n}"


def test_ty_le_phu_bao_hai_duoi(xs):
    kq = xs.ty_le_phu([1, 5, 9, 12], 2, 10)
    assert kq == {"phu": 0.5, "duoi": 0.25, "tren": 0.25}


def test_khoang_du_bao_du_lieu_lech_khong_am(xs):
    rng = np.random.default_rng(2)
    lo, hi = xs.khoang_du_bao(rng.lognormal(0, 1, 5000))
    assert lo >= 0, f"dữ liệu luôn dương mà cận dưới = {lo:.2f} — khoảng sai hình dạng"


def test_khoang_du_bao_can_bang_hai_duoi(xs):
    rng = np.random.default_rng(3)
    lo, hi = xs.khoang_du_bao(rng.lognormal(0, 1, 20000))
    kq = xs.ty_le_phu(rng.lognormal(0, 1, 20000), lo, hi)
    assert 0.015 <= kq["duoi"] <= 0.035 and 0.015 <= kq["tren"] <= 0.035, \
        f"mỗi đuôi phải ~2,5%, nhận dưới {kq['duoi']:.3f}, trên {kq['tren']:.3f}"


def test_khoang_theo_gio_trong_mau_luot_thue(xs, du_lieu):
    h = xs.doc_luot_thue()
    nam_2011 = h[h["yr"] == 0]
    ghep = nam_2011.merge(xs.khoang_theo_gio(nam_2011), on="hr")
    kq = xs.ty_le_phu(ghep["cnt"], ghep["lo"], ghep["hi"])
    assert kq["duoi"] >= 0.015, f"đuôi dưới chỉ {kq['duoi']:.3f} — khoảng quá rộng phía dưới (cận âm?)"


def test_khoang_tin_cay_ar1_du_phu(xs):
    phu = xs.ty_le_phu_khoang_tin_cay(rho=0.7, n=200, so_lan_lap=300, seed=2026)
    assert phu >= 0.80, f"khoảng tin cậy 95% chỉ chứa trung bình thật {phu:.0%} số lần — quá hẹp với dữ liệu tự tương quan"


def test_khoang_tin_cay_van_dung_voi_iid(xs):
    phu = xs.ty_le_phu_khoang_tin_cay(rho=0.0, n=200, so_lan_lap=300, seed=7)
    assert phu >= 0.88, f"với dữ liệu độc lập, khoảng phải phủ gần 95%, nhận {phu:.0%}"


def test_khoang_tin_cay_luot_thue_rong_hon_iid(xs, du_lieu):
    y = xs.doc_luot_thue().query("yr == 1")["cnt"].to_numpy()
    lo, hi = xs.khoang_tin_cay_trung_binh(y, seed=1)
    lo_iid, hi_iid = xs.khoang_tin_cay_trung_binh(y, seed=1, do_dai_khoi=1)
    assert (hi - lo) >= 1.4 * (hi_iid - lo_iid), \
        "lượt thuê theo giờ tự tương quan mạnh (ACF trễ 1 ≈ 0,84) — khoảng tin cậy mặc định phải rộng hơn hẳn bản i.i.d."
