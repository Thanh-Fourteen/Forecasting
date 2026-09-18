"""Bộ chấm buổi 4 — bộ 8 biểu đồ chẩn đoán và bản vẽ lại trung thực."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

NHAN = {"duong", "mua_vu_tuan", "chuoi_con_thang", "tre", "nhiet_gio_thu", "hop_theo_gio", "phan_tan_nhiet_do", "acf"}
TEN_BIEN = {"cnt", "temp", "cnt, temp", "lượt thuê", "nhiệt độ", ""}


@pytest.fixture(scope="module")
def m(nap):
    return nap("bieu_do")


@pytest.fixture(scope="module")
def df(m, du_lieu):
    return m.doc_luot_thue()


@pytest.fixture(scope="module")
def bo(m, df):
    fig = m.bo_bieu_do_chan_doan(df)
    yield fig
    plt.close(fig)


def _truc_theo_nhan(fig):
    return {ax.get_label(): ax for ax in fig.axes if ax.get_label() and not ax.get_label().startswith("<")}


def _co_truc_kep(fig) -> bool:
    """twinx/twiny tạo hai ax cùng khung trên cùng một hình."""
    khung = [tuple(np.round(ax.get_position().bounds, 4)) for ax in fig.axes if not ax.get_label().startswith("<")]
    return len(khung) != len(set(khung))


def test_ho_so_tuan_tach_theo_thu(m, df):
    bang = m.ho_so_tuan(df)
    assert bang.shape == (7, 24)
    assert bang.loc[0, 8] == pytest.approx(412.1, abs=0.5), "thứ Hai 8h — thứ tự dòng phải là T2..CN (dayofweek)"
    assert bang.loc[6, 8] < 0.3 * bang.loc[2, 8], "Chủ nhật 8h phải thấp hơn hẳn thứ Tư 8h — hồ sơ chưa tách theo thứ"


def test_acf_nhanh_khop_cong_thuc(m):
    rng = np.random.default_rng(0)
    y = rng.normal(size=500).cumsum()
    lech = y - y.mean()
    r5 = np.sum(lech[5:] * lech[:-5]) / np.sum(lech**2)
    assert m.acf_nhanh(y, 10)[5] == pytest.approx(r5)


def test_du_8_bieu_do(bo):
    thieu = NHAN - set(_truc_theo_nhan(bo))
    assert not thieu, f"thiếu biểu đồ: {sorted(thieu)}"


def test_khong_truc_kep(bo):
    assert not _co_truc_kep(bo), "có trục kép (twinx) — hai thang tuỳ ý làm hình dạng giống nhau giả"


def test_tieu_de_noi_ket_luan(bo):
    for nhan, ax in _truc_theo_nhan(bo).items():
        tieu_de = ax.get_title().strip()
        assert tieu_de.lower() not in TEN_BIEN and len(tieu_de) >= 20, f"{nhan}: tiêu đề '{tieu_de}' chỉ là tên biến"


def test_heatmap_7x24(bo):
    ax = _truc_theo_nhan(bo)["nhiet_gio_thu"]
    anh = [a.get_array() for a in ax.images] + [c.get_array() for c in ax.collections if hasattr(c, "get_array")]
    kich_thuoc = {np.shape(a) for a in anh if a is not None}
    assert (7, 24) in kich_thuoc or (168,) in kich_thuoc, f"heatmap phải là lưới 7 thứ × 24 giờ, thấy {kich_thuoc}"


def test_duong_va_acf_doc_duoc(bo):
    truc = _truc_theo_nhan(bo)
    duong = truc["duong"]
    assert duong.get_ylim()[0] <= 0, "trục y của số lượt thuê bị cắt — không bắt đầu từ 0"
    assert max(len(ln.get_xdata()) for ln in duong.get_lines()) < 5000, "vẽ 17.544 giờ thô — gộp theo ngày để đọc được"
    acf = truc["acf"]
    assert acf.get_xlim()[1] >= 168, "ACF phải tới ít nhất trễ 168 để thấy mùa vụ tuần"


def test_ve_lai_trung_thuc(m, df):
    fig = m.ve_lai_trung_thuc(df)
    try:
        assert not _co_truc_kep(fig), "bản vẽ lại vẫn dùng trục kép"
        for ax in fig.axes:
            if ax.get_lines():
                y = np.concatenate([np.asarray(ln.get_ydata(), float) for ln in ax.get_lines()])
                if np.nanmin(y) > 1000:  # trục lượt thuê
                    assert ax.get_ylim()[0] <= 0, "trục lượt thuê vẫn bị cắt"
    finally:
        plt.close(fig)
