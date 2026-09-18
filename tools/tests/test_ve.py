"""ve: vẽ được với dữ liệu giờ / ngày / tháng, lưu PNG, kiểm đầu vào."""
import numpy as np
import pandas as pd
import pytest

from tv import ve


def _chuoi(freq, n):
    idx = pd.date_range("2022-01-01", periods=n, freq=freq)
    rng = np.random.default_rng(0)
    return pd.Series(10 + np.sin(np.arange(n) / 3) + rng.normal(0, 0.3, n), index=idx, name="y")


@pytest.mark.parametrize(("freq", "n"), [("h", 24 * 400), ("D", 800), ("MS", 60)])
def test_bo_bieu_do_chan_doan(tmp_path, freq, n):
    y = _chuoi(freq, n)
    x = pd.Series(np.linspace(0, 30, n), index=y.index, name="nhiet_do")
    with ve.phong_cach():
        fig = ve.bo_bieu_do_chan_doan(y, x=x if freq == "h" else None, don_vi="lượt", tieu_de="Kết luận")
        assert len([a for a in fig.axes if a.get_title()]) == 8
        p = ve.luu_hinh(fig, tmp_path / f"{freq}.png")
    assert p.stat().st_size > 10_000


def test_bo_bieu_do_bao_loi():
    with pytest.raises(TypeError):
        ve.bo_bieu_do_chan_doan(pd.Series([1.0, 2.0]))


def test_acf_theo_fpp():
    y = np.array([1.0, 3.0, 2.0, 5.0, 4.0])
    x = y - y.mean()
    assert ve.acf(y, 2)[2] == pytest.approx(np.sum(x[2:] * x[:-2]) / np.sum(x * x))


def test_fan_pit_reliability(tmp_path):
    import matplotlib.pyplot as plt

    lich_su = _chuoi("D", 60)
    tuong_lai = pd.date_range(lich_su.index[-1] + pd.Timedelta(days=1), periods=14, freq="D")
    muc = [0.05, 0.25, 0.5, 0.75, 0.95]
    du_bao = pd.DataFrame({q: 10 + (q - 0.5) * np.linspace(1, 4, 14) for q in muc}, index=tuong_lai)
    rng = np.random.default_rng(1)
    with ve.phong_cach():
        fig, ax = plt.subplots(1, 3, figsize=(12, 3))
        ve.fan_chart(ax[0], lich_su, du_bao, tieu_de="Dải rộng dần theo tầm")
        ve.pit_histogram(ax[1], rng.uniform(size=500))
        p = rng.uniform(size=500)
        ve.reliability_diagram(ax[2], p, rng.uniform(size=500) < p)
        ve.luu_hinh(fig, tmp_path / "bat-dinh.png")
    with pytest.raises(ValueError):
        ve.pit_histogram(plt.gca(), [1.5])


def test_pit_khong_ngau_nhien_du_lieu_dem():
    import matplotlib.pyplot as plt

    from tv import danh_gia

    rng = np.random.default_rng(3)
    lam = rng.uniform(1, 5, 2000)
    y = rng.poisson(lam)
    mau = rng.poisson(lam[:, None], (2000, 400))  # dự báo đúng phân phối → histogram gần phẳng
    duoi, tren = danh_gia.pit_mau(y, mau)
    assert np.all(duoi <= tren) and np.any(duoi < tren)
    fig, ax = plt.subplots()
    ve.pit_histogram(ax, (duoi, tren))
    chieu_cao = np.array([b.get_height() for b in ax.patches])
    assert chieu_cao.sum() / len(chieu_cao) == pytest.approx(1.0)
    assert np.all(np.abs(chieu_cao - 1) < 0.15), chieu_cao
    plt.close(fig)


def test_pav_isotonic():
    from tv.ve import _pav

    assert list(_pav(np.array([0, 1, 0, 1, 1, 0]))) == pytest.approx([0, 0.5, 0.5, 2 / 3, 2 / 3, 2 / 3])
