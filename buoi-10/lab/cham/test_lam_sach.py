"""Bộ chấm buổi 10 — làm sạch và dữ liệu thiếu.

Chấm `code/lam_sach.py` (mặc định) hoặc `dap-an/lam_sach.py` khi BAI=dap-an.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tv import ro_ri

COT_DO = ["temperature", "dew_point_temperature", "relative_humidity", "visibility", "wind_speed"]


@pytest.fixture(scope="module")
def ls(nap, du_lieu):
    return nap("lam_sach")


@pytest.fixture(scope="module")
def tho(ls):
    return ls.doc_noi_bai()


def test_cot_do_la_kieu_so(tho):
    """Parquet gốc lưu relative_humidity/visibility dạng CHUỖI. Phải ép kiểu số khi đọc,
    nếu không min/max và mọi phép so sánh đều sai âm thầm."""
    for cot in COT_DO:
        assert pd.api.types.is_numeric_dtype(tho[cot]), (
            f"cột {cot} đang là {tho[cot].dtype}: min/max sẽ so sánh theo thứ tự chữ cái")
    rh = tho["relative_humidity"]
    assert rh.min() == 21 and rh.max() == 100, "độ ẩm phải nằm trong 21–100 %"


def test_thieu_moc_va_thieu_gia_tri_tach_bac(ls, tho):
    """Ở trạm Nội Bài 2024, gần như toàn bộ phần thiếu là THIẾU MỐC, không phải ô rỗng."""
    tk = ls.thong_ke_thieu(tho)
    assert tk["so_moc_ky_vong"] == 17568, "2024 có 17.568 mốc 30 phút"
    assert tk["thieu_moc"] == 249
    assert tk["moc_trung"] == 0
    assert tk["thieu_gia_tri"] < 10


def test_cot_hoan_toan_rong(ls):
    """'Có cột' không có nghĩa là 'có dữ liệu': 30/64 cột đo của tệp này rỗng 100%."""
    rong = ls.cot_rong()
    assert len(rong) >= 25
    assert "precipitation" in rong and "station_level_pressure" in rong


def test_do_phan_giai_truoc_khi_ket_luan_mac_ket(ls, tho):
    """Nhiệt độ chỉ ghi tới 1 °C — phải biết điều này trước khi gọi một đoạn lặp là 'cảm biến chết'."""
    dpg = ls.do_phan_giai(tho["temperature"])
    assert dpg["bước nhỏ nhất"] == 1.0
    assert dpg["tỷ lệ giá trị nguyên %"] == 100.0
    assert dpg["số giá trị khác nhau"] < 60


def test_doan_mac_ket_dai_nhat(ls, tho):
    """Đoạn đứng yên dài nhất: 67 bước 30 phút = 33,5 giờ ở đúng 26,0 °C (2024-06-08)."""
    ket = ls.doan_mac_ket(tho["temperature"], 24)
    assert len(ket) > 0
    dau = ket.iloc[0]
    assert dau["so_buoc"] == 67 and dau["gia_tri"] == 26.0
    assert pd.Timestamp(dau["bat_dau"]).date() == pd.Timestamp("2024-06-08").date()


def test_gia_tri_tra_hinh(ls, tho):
    """visibility 9.999 km là mã METAR '9999 m = ≥10 km'; RH 100% là trần của cảm biến."""
    bang = ls.doan_tra_hinh(tho).set_index("cột")
    assert bang.loc["visibility", "tỷ lệ %"] > 30, "9.999 chiếm 35% số dòng — đó là mã, không phải số đo"
    assert bang.loc["relative_humidity", "tỷ lệ %"] > 5


def test_co_chat_luong_ghcnh(ls, tho):
    """Mã 2 = Suspect, 'f' = một đầu vào bị gắn cờ. Mã 1 (qua mọi kiểm tra) KHÔNG được coi là nghi ngờ."""
    co = ls.co_nghi_ngo(tho, "temperature")
    assert int(co.sum()) == 7
    assert not co[tho["ma_temperature"] == "1"].any()


def test_so_sanh_dien_phai_co_ca_hai_kieu_che(ls, tho):
    """Che điểm và che khối cho thứ hạng KHÁC nhau. Chỉ báo một kiểu là kết luận sai."""
    y = ls.luoi_day_du(tho)["temperature"]
    hx = ls.doc_hang_xom()["temperature_2m"]
    bang = ls.so_sanh_dien(y, hang_xom=hx)
    kieu = set(bang["kiểu che"])
    assert len(kieu) >= 2, f"mới đánh giá trên {kieu} — thiếu kiểu che còn lại"
    tot_nhat = bang.loc[bang.groupby("kiểu che")["MAE"].idxmin()].set_index("kiểu che")["cách điền"]
    assert tot_nhat.nunique() > 1, ("phương pháp tốt nhất phải ĐỔI giữa lỗ ngắn và lỗ dài; "
                                    f"đang ra {tot_nhat.to_dict()}")


def test_lam_sach_khong_dien_lo_dai(ls, tho):
    """Lỗ dài không được điền: điền 48 giờ bằng nội suy là bịa dữ liệu. Phải có cờ truy vết."""
    hx = ls.doc_hang_xom()["temperature_2m"]
    sach = ls.lam_sach(tho, gioi_han=6, hang_xom=hx)
    for cot in ["da_dien", "nghi_ngo", "lo_dai_bo_trong"]:
        assert cot in sach.columns, f"thiếu cờ truy vết {cot}"
    assert sach["da_dien"].sum() > 0, "phải điền các lỗ ngắn"
    assert sach["lo_dai_bo_trong"].sum() > 0, "phải còn lỗ dài để trống có chủ ý"
    assert not (sach["da_dien"] & sach["lo_dai_bo_trong"]).any()
    assert sach.loc[sach["lo_dai_bo_trong"], "temperature"].isna().all()

    thieu = sach["temperature"].isna()
    nhom = (thieu != thieu.shift()).cumsum()[thieu]
    dai_nhat = nhom.groupby(nhom).size().max() if len(nhom) else 0
    assert dai_nhat > 6, "lỗ dài phải được giữ nguyên, không bị nội suy lấp"


def test_lam_sach_khong_dung_tuong_lai(ls, tho):
    """Cách điền mặc định phải NHÂN QUẢ: cắt dữ liệu tại mốc t không được đổi kết quả trước t."""
    nho = tho.iloc[:2000].copy()
    # khoét hai lỗ: một lỗ dài 20 bước và một lỗ ngắn 3 bước, rồi cắt dữ liệu NGAY TRONG lỗ dài
    nho.iloc[1190:1210, nho.columns.get_loc("temperature")] = np.nan
    nho.iloc[1290:1293, nho.columns.get_loc("temperature")] = np.nan
    hx = ls.doc_hang_xom()["temperature_2m"]

    def ham(df: pd.DataFrame) -> pd.DataFrame:
        bang = df.set_index("ds")
        bang.index.name = "thoi_gian"
        sach = ls.lam_sach(bang, gioi_han=6, hang_xom=hx)
        return pd.DataFrame({"ds": sach.index, "sach": sach["temperature"].to_numpy(),
                             "da_dien": sach["da_dien"].to_numpy()})

    dai = nho.reset_index().rename(columns={"thoi_gian": "ds", "temperature": "y"})
    dai["ma_temperature"] = nho["ma_temperature"].to_numpy()
    moc = [dai["ds"].iloc[1205], dai["ds"].iloc[1291]]
    kq = ro_ri.kiem_ro_ri(ham, dai[["ds", "y", "ma_temperature"]].assign(temperature=dai["y"]),
                          cac_moc_cat=moc, h=None, cot_id=None, cot_y="y")
    kq.khang_dinh_sach()


def test_mnar_lam_lech_ket_qua(ls):
    """Thiếu MNAR (cảm biến tắt khi giá trị cao) làm trung bình sau khi điền lệch hẳn;
    thiếu MCAR thì không."""
    kq = ls.mo_phong_mnar()
    lech_mcar = abs(kq["sau khi điền, thiếu MCAR"] - kq["trung bình thật"])
    lech_mnar = abs(kq["sau khi điền, thiếu MNAR"] - kq["trung bình thật"])
    assert lech_mcar < 0.05
    assert lech_mnar > 0.2
    assert lech_mnar > 5 * lech_mcar


def test_bang_chung_mnar_bao_cao_trung_thuc(ls):
    """Hàm kiểm MNAR phải trả bằng chứng đo được, không phải khẳng định suông."""
    bk = ls.doc_bac_kinh(["Dongsi", "Guanyuan", "Wanliu"])
    kq = ls.bang_chung_mnar(bk, "Dongsi")
    assert set(kq) >= {"tỷ lệ thiếu %", "PM2.5 hàng xóm khi trạm thiếu", "PM2.5 hàng xóm khi trạm có", "chênh %"}
    assert 0 < kq["tỷ lệ thiếu %"] < 20
    assert np.isfinite(kq["chênh %"])
