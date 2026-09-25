"""Bộ chấm buổi 26 — conformal prediction. Mỗi test kiểm một hành vi; thông báo lỗi nói cần sửa gì."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="session")
def cf(nap, du_lieu):
    return nap("conformal")


@pytest.fixture(scope="session")
def df(cf):
    return cf.doc_pm25()


@pytest.fixture(scope="session")
def P(cf, df):
    return cf.du_bao(df)


@pytest.fixture(scope="session")
def kiem(P):
    return (P["giai_doan"] == "kiem").to_numpy()


def test_quantile_conformal_vi_du_tay(cf):
    diem = [1, 2, 2, 3, 3, 4, 5, 6, 8, 12]
    assert cf.quantile_conformal(diem, 0.2) == 8, "10 điểm, α = 0,2: lấy điểm thứ ⌈11 × 0,8⌉ = 9 khi xếp tăng (mục 4.1)"
    assert np.isinf(cf.quantile_conformal(diem, 0.05)), "⌈11 × 0,95⌉ = 11 > 10 điểm → khoảng vô hạn (mục 4.1)"


def test_dac_trung_khong_ro_ri(cf, df):
    from tv.ro_ri import kiem_ro_ri

    kq = kiem_ro_ri(lambda x: cf.dac_trung(x).drop(columns="y"), df.iloc[:24 * 90], h=1, cot_id=None)
    assert not kq.co_ro_ri, f"đặc trưng dùng số của chính giờ cần đoán:\n{kq}"


def test_aci_lo_thi_noi_khoang(cf):
    """Sau một giờ thực tế nằm ngoài khoảng, α_t phải GIẢM (khoảng rộng ra); sau giờ nằm trong, α_t tăng nhẹ."""
    n = 200
    P = pd.DataFrame({"ds": pd.date_range("2020-01-01", periods=n + 3, freq="h"),
                      "giai_doan": ["hieu_chinh"] * n + ["kiem"] * 3,
                      "yhat": 0.0, "y": np.r_[np.linspace(0, 1, n), 100.0, 0.0, 0.0]})
    a = cf.aci(P, alpha=0.1, gamma=0.05)["alpha_t"].to_numpy()[n:]
    assert a[1] < a[0], (f"giờ đầu nằm ngoài khoảng mà α_t đi từ {a[0]:.3f} lên {a[1]:.3f}: lỡ thì phải NỚI khoảng "
                         "(giảm α_t). Xem công thức cập nhật mục 4.5")
    assert a[2] > a[1], "giờ thứ hai nằm trong khoảng: α_t phải tăng nhẹ"


def test_aci_coverage_dai_han(cf, P, kiem):
    K = cf.aci(P)
    y = P.loc[kiem, "y"].to_numpy()
    c = float(np.mean((y >= K.loc[kiem, "lo"].to_numpy()) & (y <= K.loc[kiem, "hi"].to_numpy())))
    assert abs(c - 0.9) < 0.01, f"ACI phủ {c:.1%} số giờ trên hai năm kiểm, phải gần 90% (mục 4.5)"


def test_khoang_trien_khai_giu_coverage_theo_thoi_gian(cf, P, kiem):
    K = cf.khoang_trien_khai(P)
    y = P.loc[kiem, "y"].to_numpy()
    c = cf.coverage_truot(y, K.loc[kiem, "lo"].to_numpy(), K.loc[kiem, "hi"].to_numpy()).dropna()
    ngoai = float(((c < 0.85) | (c > 0.95)).mean())
    assert ngoai < 0.02, (f"coverage 30 ngày của khoảng triển khai nằm ngoài [85%, 95%] {ngoai:.1%} thời gian "
                          f"(thấp nhất {c.min():.1%}). Khoảng tính một lần từ năm hiệu chỉnh không theo kịp mùa (mục 4.2)")


def test_khoang_chi_dung_qua_khu(cf, P):
    """Khoảng của giờ t không được phụ thuộc thực tế của chính giờ t (hay giờ sau)."""
    dau = int(np.flatnonzero(P["giai_doan"] == "kiem")[0])
    Q = P.iloc[dau - 2000:dau + 1000].reset_index(drop=True)
    for i in range(2000, 3000, 50):
        a, b = Q.copy(), Q.copy()
        a.loc[i:, "y"] = a.loc[i:, "yhat"]
        b.loc[i:, "y"] = b.loc[i:, "yhat"] + 10_000
        ka, kb = cf.khoang_trien_khai(a), cf.khoang_trien_khai(b)
        assert np.allclose(ka.loc[:i, ["lo", "hi"]], kb.loc[:i, ["lo", "hi"]], equal_nan=True), (
            f"khoảng của giờ {Q.loc[i, 'ds']} (hoặc trước đó) đổi khi thực tế từ giờ đó trở đi đổi — rò rỉ tương lai. "
            "Chỉ thêm điểm của một giờ vào tập SAU khi đã tính khoảng cho giờ đó (mục 4.5)")


def test_cqr_diem(cf):
    P = pd.DataFrame({"ds": pd.date_range("2020-01-01", periods=4, freq="h"), "giai_doan": "hieu_chinh",
                      "y": [20.0, 55, 90, 140], "yhat": 0.0, "q_lo": [15.0, 40, 70, 100], "q_hi": [30.0, 60, 85, 150]})
    K = cf.cqr(P, alpha=0.2)
    assert np.allclose(K["hi"] - P["q_hi"], 5), "điểm CQR = max(q_lo − y, y − q_hi); ví dụ tay mục 4.3 cho q = 5"
