"""danh_gia: số tính tay (Phụ lục D mục 9) + đối chiếu utilsforecast / scoringrules khi có."""
import warnings

import numpy as np
import pandas as pd
import pytest

from tv import danh_gia as dg

Y_TRAIN = np.array([10, 20, 30, 20, 12, 22, 33, 21, 13, 24, 35, 23], dtype=float)
Y = np.array([14, 25, 36, 24], dtype=float)
F = np.array([12, 27, 30, 25], dtype=float)


def test_so_tinh_tay_phu_luc_d():
    assert dg.mae(Y, F) == pytest.approx(2.75)
    assert dg.rmse(Y, F) == pytest.approx(3.3541, abs=1e-4)
    assert dg.me(Y, F) == pytest.approx(1.25)
    assert dg.mape(Y, F) == pytest.approx(10.7798, abs=1e-4)
    assert dg.smape(Y, F) == pytest.approx(11.3351, abs=1e-4)
    assert dg.wape(Y, F) == pytest.approx(0.1111, abs=1e-4)
    assert dg.mase(Y, F, Y_TRAIN, m=4) == pytest.approx(1.4667, abs=1e-4)
    assert dg.rmsse(Y, F, Y_TRAIN, m=4) == pytest.approx(1.7039, abs=1e-4)
    q = np.array([11, 23, 31, 22], dtype=float)
    assert dg.pinball(Y, q, 0.9) == pytest.approx(2.70)
    assert dg.pinball(Y, q, 0.9, nhan_2=True) == pytest.approx(5.40)


def test_wis_bracher_hai_dang_bang_nhau():
    # y = 10, trung vị 8, khoảng 80% [6, 9], khoảng 50% [7, 8.5] → WIS = 1.67 (Phụ lục D)
    w = dg.wis([10.0], [8.0], lo=[[6.0], [7.0]], hi=[[9.0], [8.5]], alphas=[0.2, 0.5])
    assert w == pytest.approx(1.67)
    wq = dg.wis_quantile([10.0], [0.1, 0.25, 0.5, 0.75, 0.9], np.array([[6.0, 7.0, 8.0, 8.5, 9.0]]))
    assert wq == pytest.approx(w)


def test_wis_k0_la_sai_so_tuyet_doi():
    assert dg.wis([3.0, 5.0], [1.0, 6.0], lo=[], hi=[], alphas=[]) == pytest.approx(dg.mae([3.0, 5.0], [1.0, 6.0]))


def test_winkler_va_coverage():
    assert dg.winkler([10.0], [6.0], [9.0], 0.2) == pytest.approx(13.0)
    assert dg.coverage([1, 5, 9], [0, 0, 0], [4, 6, 8]) == pytest.approx(2 / 3)


def test_brier_phan_ra_murphy():
    p = np.array([0.1, 0.1, 0.1, 0.1, 0.7, 0.7, 0.7, 0.7, 0.7, 0.9])
    o = np.array([0, 0, 1, 0, 1, 1, 0, 1, 1, 1])
    kq = dg.phan_ra_brier(p, o)
    assert kq["brier"] == pytest.approx(0.17)
    assert (kq["reliability"], kq["resolution"], kq["uncertainty"]) == pytest.approx((0.015, 0.085, 0.24))
    assert kq["reliability"] - kq["resolution"] + kq["uncertainty"] == pytest.approx(kq["brier"])


def test_log_score_vo_han_khi_chac_chan_sai():
    assert dg.log_score([0.0], [1]) == np.inf
    assert dg.log_score([0.5, 0.5], [1, 0]) == pytest.approx(np.log(2))


def test_crps_chuan_va_mau_hoi_tu():
    rng = np.random.default_rng(3)
    mau = rng.normal(0, 1, (1, 4000))
    dong = dg.crps_chuan([0.8], 0.0, 1.0)
    assert dong == pytest.approx(0.4762, abs=1e-4)
    assert dg.crps_mau([0.8], mau, "nrg") == pytest.approx(0.4632, abs=1e-4)  # số chạy Phase 0, seed 3
    assert abs(dg.crps_mau([0.8], mau, "fair") - dong) < 0.02


def test_crps_mot_mau_la_sai_so_tuyet_doi():
    assert dg.crps_mau([0.8], [[1.0]], "nrg") == pytest.approx(0.2)


def test_mape_co_so_0_canh_bao():
    with pytest.warns(UserWarning, match="y = 0"):
        assert np.isnan(dg.mape([0.0, 1.0], [1.0, 1.0]))


def test_m5_mau_so_tu_lan_ban_dau_tien():
    y_train = np.array([0, 0, 0, 2, 0, 4], dtype=float)  # sai phân từ vị trí 3: [-2, 4] → MSE 10
    assert dg.rmsse([3.0], [1.0], y_train, m=1, tu_khac_0=True) == pytest.approx(np.sqrt(4 / 10))
    assert dg.rmsse([3.0], [1.0], y_train, m=1) == pytest.approx(np.sqrt(4 / ((0 + 0 + 4 + 4 + 16) / 5)))


def test_loi_dau_vao():
    with pytest.raises(ValueError):
        dg.mae([1, 2], [1])
    with pytest.raises(ValueError):
        dg.pinball([1.0], [1.0], 1.2)
    with pytest.raises(ValueError, match="crossing"):
        dg.winkler([1.0], [3.0], [2.0], 0.1)
    with pytest.raises(ValueError):
        dg.mase([1.0], [1.0], [1.0, 2.0], m=4)


def _bang():
    rng = np.random.default_rng(5)
    ds = pd.date_range("2024-01-01", periods=40, freq="D")
    dong_train, dong_test = [], []
    for uid in ("a", "b", "c"):
        y = 20 + 5 * np.sin(np.arange(40) * 2 * np.pi / 7) + rng.normal(0, 2, 40)
        dong_train.append(pd.DataFrame({"unique_id": uid, "ds": ds[:33], "y": y[:33]}))
        dong_test.append(pd.DataFrame({"unique_id": uid, "ds": ds[33:], "y": y[33:],
                                       "snaive": y[26:33], "lech": y[33:] + rng.normal(1, 3, 7)}))
    return pd.concat(dong_train, ignore_index=True), pd.concat(dong_test, ignore_index=True)


def test_bang_chi_so_theo_chuoi_va_gop():
    train, test = _bang()
    theo_chuoi = dg.bang_chi_so(test, ["snaive", "lech"], train, m=7, gop=None)
    assert len(theo_chuoi) == 6
    gop = dg.bang_chi_so(test, ["snaive", "lech"], train, m=7)
    assert gop.loc["snaive", "mae"] == pytest.approx(theo_chuoi[theo_chuoi.mo_hinh == "snaive"]["mae"].mean())


# ---------------------------------------------------------------- đối chiếu thư viện chuẩn


def test_doi_chieu_utilsforecast():
    losses = pytest.importorskip("utilsforecast.losses")
    train, test = _bang()
    ta = dg.bang_chi_so(test, ["snaive", "lech"], train, m=7, gop=None,
                        chi_so=("mae", "rmse", "mase", "rmsse", "wape", "me", "mape", "smape")).set_index(
        ["unique_id", "mo_hinh"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        uf = {
            "mae": losses.mae(test, ["snaive", "lech"]),
            "rmse": losses.rmse(test, ["snaive", "lech"]),
            "mase": losses.mase(test, ["snaive", "lech"], seasonality=7, train_df=train),
            "rmsse": losses.rmsse(test, ["snaive", "lech"], seasonality=7, train_df=train),
            "wape": losses.nd(test, ["snaive", "lech"]),
            "me": losses.bias(test, ["snaive", "lech"]),
            "mape": losses.mape(test, ["snaive", "lech"]),
            "smape": losses.smape(test, ["snaive", "lech"]),
        }
    he_so = {"me": -1.0, "mape": 100.0, "smape": 200.0}  # quy ước khác nhau — xem docstring danh_gia
    for ten, bang in uf.items():
        for mo_hinh in ("snaive", "lech"):
            for _, dong in bang.iterrows():
                assert ta.loc[(dong["unique_id"], mo_hinh), ten] == pytest.approx(
                    he_so.get(ten, 1.0) * dong[mo_hinh], rel=1e-9), (ten, mo_hinh)


def test_doi_chieu_utilsforecast_pinball():
    losses = pytest.importorskip("utilsforecast.losses")
    _, test = _bang()
    for tau in (0.1, 0.5, 0.9):
        uf = losses.quantile_loss(test, {"lech": "lech"}, q=tau)
        for _, dong in uf.iterrows():
            g = test[test.unique_id == dong["unique_id"]]
            assert dg.pinball(g["y"], g["lech"], tau) == pytest.approx(dong["lech"])


def test_doi_chieu_scoringrules_crps():
    sr = pytest.importorskip("scoringrules")
    rng = np.random.default_rng(7)
    y = rng.normal(size=20)
    mau = rng.normal(0.3, 1.2, (20, 50))
    for uoc_luong in ("nrg", "fair"):
        ky_vong = float(np.mean(sr.crps_ensemble(y, mau, estimator=uoc_luong)))
        assert dg.crps_mau(y, mau, uoc_luong) == pytest.approx(ky_vong, rel=1e-9)
    mu, sigma = rng.normal(size=20), rng.uniform(0.5, 2, 20)
    assert dg.crps_chuan(y, mu, sigma) == pytest.approx(float(np.mean(sr.crps_normal(y, mu, sigma))), rel=1e-9)
