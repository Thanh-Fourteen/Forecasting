"""Bộ chấm buổi 11 — ngoại lai và điểm gãy.

Chấm `code/bat_thuong.py` (mặc định) hoặc `dap-an/bat_thuong.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def bt(nap, du_lieu):
    return nap("bat_thuong")


@pytest.fixture(scope="module")
def tong(bt):
    return bt.doc_tong_vi()


@pytest.fixture(scope="module")
def tet(bt):
    return bt.doc_bai_tet()


@pytest.fixture(scope="module")
def hk(bt):
    return bt.doc_hang_khong()


@pytest.fixture(scope="module")
def mo_phong(bt):
    return bt.sinh_chuoi_co_loi()


def test_du_lieu_doc_dung(tong, tet, hk):
    assert len(tong) == 3653 and tong.index.min().year == 2016 and tong.index.max().year == 2025
    assert len(tet) == 3653
    assert len(hk) >= 216 and hk.index.min() == pd.Timestamp("2008-01-01")
    assert hk.min() > 0, "hành khách không thể âm hay bằng 0"


def test_mad_ben_vung_hon_do_lech_chuan(bt):
    """Thêm một ngoại lai lớn: σ phình lên, MAD gần như không đổi."""
    rng = np.random.default_rng(0)
    y = pd.Series(rng.normal(0, 1, 500), index=pd.date_range("2024-01-01", periods=500))
    y2 = y.copy()
    y2.iloc[250] = 100.0
    assert y2.std() > 3 * y.std()
    diem, diem2 = bt.mad_score(y), bt.mad_score(y2)
    assert abs(diem.median() - diem2.median()) < 0.1


def test_masking_3sigma(bt, tong):
    """Chính ngoại lai kéo σ lên và che các ngoại lai khác: 3σ bắt được ÍT hơn sau khi thêm một
    điểm cực lớn, còn Hampel thì không bị."""
    kq = bt.masking(tong)
    assert kq["3σ bắt được (sau khi thêm 1 điểm cực lớn)"] < kq["3σ bắt được (gốc)"] / 2
    assert kq["Hampel bắt được (sau khi thêm)"] >= kq["Hampel bắt được (gốc)"]


def test_hampel_bat_nhieu_hon_3sigma_tren_chuoi_co_xu_huong(bt, tong):
    """Trên chuỗi có xu hướng + mùa vụ, ngưỡng toàn chuỗi gần như mù: 3σ chỉ 16/3.653 ngày."""
    bang = bt.so_sanh_bat(tong).set_index("cách")
    assert bang.loc["3σ toàn chuỗi", "số điểm gắn cờ"] < 30
    assert bang.loc["Hampel k=15", "số điểm gắn cờ"] > 3 * bang.loc["3σ toàn chuỗi", "số điểm gắn cờ"]


def test_ngoai_lai_khong_duoc_xoa_dinh_tet(bt, tet):
    """Đỉnh Tết là SỰ KIỆN THẬT. Xử lý mặc định không được xoá chúng khỏi chuỗi."""
    dinh = bt.dinh_tet(tet)
    assert len(dinh) == 10, "mười năm, mỗi năm một đỉnh Tết"
    xl = bt.xu_ly_ngoai_lai(tet, bo_qua_su_kien=dinh)
    assert int(xl["bi_xoa"].sum()) == 0, "không được XOÁ mốc — mất mốc là mất cả lịch thời gian"
    con = xl.loc[dinh, "sach"]
    goc = tet.loc[dinh]
    assert np.allclose(con.to_numpy(float), goc.to_numpy(float)), (
        "đỉnh Tết bị san phẳng: nhật ký sự kiện phải được tôn trọng")


def test_mat_dinh_tet_khi_dung_nguong_toan_chuoi(bt, tet):
    """Bằng chứng để dạy: ngưỡng toàn chuỗi gắn cờ TOÀN BỘ 10 đỉnh Tết."""
    bang = bt.mat_bao_nhieu_dinh_tet(tet).set_index("cách")
    assert bang.loc["3σ toàn chuỗi", "số đỉnh Tết bị gắn cờ"] == 10


def test_pelt_tren_log_moi_ra_it_diem_gay(bt, hk):
    """Chuỗi tăng trưởng nhân tính: PELT trên mức thô sinh hàng chục điểm gãy giả;
    lấy log trước thì chỉ còn các điểm gãy thật."""
    tho = bt.diem_gay(hk, log=False)
    co_log = bt.diem_gay(hk, log=True)
    assert len(tho) > 20, "trên mức thô, PELT phải sinh rất nhiều điểm gãy (đó là triệu chứng)"
    assert len(co_log) <= 4, f"trên log phải còn rất ít điểm gãy, đang ra {len(co_log)}"


def test_diem_gay_covid_on_dinh(bt, hk):
    """Hai điểm gãy COVID phải ổn định qua nhiều penalty, và đúng chiều."""
    moc = bt.diem_gay_on_dinh(hk)
    assert 2 <= len(moc) <= 3
    nam = sorted({pd.Timestamp(m).year for m in moc})
    assert nam[:2] == [2020, 2021]
    bang = bt.do_lon_gay(hk, moc)
    assert bang["đổi %"].iloc[0] < -50, "điểm gãy 2020 phải là sụt mạnh"
    assert bang["đổi %"].iloc[1] > 50, "điểm gãy 2021 phải là hồi phục"


def test_quet_penalty_don_dieu(bt, hk):
    """Penalty càng lớn thì số điểm gãy càng ít (không tăng) — kiểm tính đúng của phép quét."""
    bang = bt.quet_penalty(hk, cac_pen=np.array([1, 2, 4, 8, 16]) * np.log(len(hk)))
    so = bang["số điểm gãy"].to_numpy()
    assert (np.diff(so) <= 0).all(), f"số điểm gãy phải không tăng theo penalty: {so.tolist()}"


def test_doi_phuong_sai_do_tren_phan_du(bt, mo_phong):
    """Biên độ mùa vụ át σ của nhiễu: phải đo trên phần dư STL và dùng thước đo bền vững."""
    y, nhan = mo_phong
    kq = bt.doi_phuong_sai(y)
    vi_tri_that = nhan["doi_phuong_sai"][0]
    gan = [m for m, _ in kq if abs(y.index.get_loc(m) - vi_tri_that) <= 10]
    assert gan, f"không thấy điểm đổi phương sai quanh vị trí {vi_tri_that}: {kq}"
    assert len(kq) <= 4, f"quá nhiều cảnh báo giả: {kq}"


def test_dan_nhan_dung_loai(bt, mo_phong):
    """Tiêu chí 'Xong khi' của buổi: gắn đúng loại cho ≥ 4/5 bất thường cài sẵn."""
    y, nhan = mo_phong
    su_kien = bt.dan_nhan(y)
    bang = bt.danh_gia_nhan(su_kien, nhan, y)
    assert int(bang["đúng loại"].sum()) >= 5, bang.to_string(index=False)
    assert len(su_kien) <= 15, "cảnh báo giả quá nhiều thì bảng nhãn vô dụng"


def test_ba_cach_xu_ly_covid_khac_nhau(bt, hk):
    """Ba cách xử lý phải cho ba kết quả KHÁC nhau — nếu giống nhau thì baseline chưa dùng
    phần dữ liệu COVID, và cả bài học trở nên vô nghĩa."""
    bang = bt.ba_cach_xu_ly_covid(hk).set_index("cách xử lý")
    assert len(bang) == 3
    mape = bang["MAPE %"]
    assert mape.max() - mape.min() > 3, f"ba cách gần như giống nhau: {mape.to_dict()}"
    assert mape.idxmin() != "giữ nguyên", "giữ nguyên dữ liệu COVID không thể là cách tốt nhất"
