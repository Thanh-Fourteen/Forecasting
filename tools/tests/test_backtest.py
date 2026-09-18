"""backtest: vị trí cửa sổ, không lộ test cho hàm dự báo, refit, Diebold–Mariano."""
import numpy as np
import pandas as pd
import pytest

from tv.backtest import backtest, chia_cua_so, diebold_mariano


def _du_lieu(n=30, ds_so=False):
    ds = np.arange(n) if ds_so else pd.date_range("2024-01-01", periods=n, freq="D")
    return pd.concat([pd.DataFrame({"unique_id": uid, "ds": ds, "y": np.arange(n, dtype=float) * k})
                      for uid, k in (("a", 1.0), ("b", 2.0))], ignore_index=True)


def test_vi_tri_cua_so_co_gap():
    df = _du_lieu(20, ds_so=True)
    cs = chia_cua_so(df, h=3, so_cua_so=2, buoc=2, gap=1)
    # cửa sổ cuối: cutoff 15, gap 16, test 17..19
    assert [(c.cutoff, c.bat_dau_test, c.ket_thuc_test) for c in cs] == [(13, 15, 17), (15, 17, 19)]
    with pytest.raises(ValueError, match="không đủ dữ liệu"):
        chia_cua_so(df, h=3, so_cua_so=10, buoc=3, cua_so_train=10)


def _naive(lich_su, ds_can):
    cuoi = lich_su.sort_values("ds").groupby("unique_id")["y"].last()
    return ds_can.assign(naive=ds_can["unique_id"].map(cuoi))


def test_ham_du_bao_khong_thay_tuong_lai():
    df = _du_lieu(30)
    da_thay = []

    def du_bao(lich_su, ds_can):
        da_thay.append((lich_su["ds"].max(), ds_can["ds"].min()))
        assert lich_su["ds"].max() < ds_can["ds"].min()
        return _naive(lich_su, ds_can)

    kq = backtest(df, du_bao, h=4, so_cua_so=3, gap=2)
    assert len(da_thay) == 3
    assert all((dau - cuoi).days == 3 for cuoi, dau in da_thay)  # gap 2 ngày bỏ trống
    assert set(kq["buoc_h"]) == {3, 4, 5, 6}
    assert list(kq.columns[:5]) == ["unique_id", "ds", "cutoff", "buoc_h", "y"]
    # naive trên chuỗi tuyến tính: sai số = độ dốc × (buoc_h)
    sai_so = kq["y"] - kq["naive"]
    doc = kq["unique_id"].map({"a": 1.0, "b": 2.0})
    assert np.allclose(sai_so, doc * kq["buoc_h"])


def test_sliding_window():
    df = _du_lieu(30)
    do_dai = []
    backtest(df, lambda ls, dc: (do_dai.append(ls["ds"].nunique()), _naive(ls, dc))[1], h=2, so_cua_so=3,
             cua_so_train=10)
    assert do_dai == [10, 10, 10]


def test_du_bao_thua_dong_bao_loi():
    df = _du_lieu(30)

    def sai(lich_su, ds_can):
        them = ds_can.assign(ds=ds_can["ds"] + pd.Timedelta(days=30))
        return _naive(lich_su, pd.concat([ds_can, them]))

    with pytest.raises(ValueError, match="thừa"):
        backtest(df, sai, h=2, so_cua_so=2)


def test_du_bao_chua_cot_y_bao_loi():
    df = _du_lieu(30)
    with pytest.raises(ValueError, match="'y'"):
        backtest(df, lambda ls, dc: dc.assign(y=0.0), h=2, so_cua_so=1)


@pytest.mark.parametrize(("refit", "so_lan"), [(True, 4), (False, 1), (2, 2)])
def test_refit(refit, so_lan):
    df = _du_lieu(40)
    dem = []

    def huan_luyen(train):
        dem.append(train["ds"].max())
        return "mo_hinh"

    def du_bao(mo_hinh, lich_su, ds_can):
        return _naive(lich_su, ds_can)

    backtest(df, du_bao, h=3, so_cua_so=4, refit=refit, ham_huan_luyen=huan_luyen)
    assert len(dem) == so_lan


def test_dm_so_voi_tinh_tay_phase0():
    # Phụ lục D mục 9: seed 11, 40 điểm, bình phương, h = 1 → DM -1.4550 (p 0.1457), HLN -1.4367 (p 0.1588)
    pytest.importorskip("scipy")
    rng = np.random.default_rng(11)
    e1, e2 = rng.normal(0, 1.0, 40), rng.normal(0, 1.2, 40)
    goc = diebold_mariano(e1, e2, hieu_chinh=False)
    hln = diebold_mariano(e1, e2)
    assert (goc.thong_ke, goc.p_value) == pytest.approx((-1.4550, 0.1457), abs=1e-4)
    assert (hln.thong_ke, hln.p_value) == pytest.approx((-1.4367, 0.1588), abs=1e-4)


def test_dm_h_lon_hon_1_tu_tinh():
    pytest.importorskip("scipy")
    from scipy import stats

    rng = np.random.default_rng(4)
    e1, e2 = rng.normal(size=60), rng.normal(size=60) * 1.3
    h = 3
    d = np.abs(e1) - np.abs(e2)
    n, dt = len(d), d - d.mean()
    g = [np.sum(dt[k:] * dt[:n - k]) / n for k in range(h)]
    thong_ke = d.mean() / np.sqrt((g[0] + 2 * (g[1] + g[2])) / n)
    thong_ke *= np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    kq = diebold_mariano(e1, e2, h=h, ham_mat_mat="tuyet_doi")
    assert kq.thong_ke == pytest.approx(thong_ke)
    assert kq.p_value == pytest.approx(2 * stats.t(n - 1).sf(abs(thong_ke)))


def test_dm_giong_het_bao_loi():
    pytest.importorskip("scipy")
    e = np.ones(10)
    with pytest.raises(ValueError, match="giống hệt"):
        diebold_mariano(e, e)
