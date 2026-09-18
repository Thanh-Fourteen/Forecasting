"""Buổi 3 — chuan_hoa_thoi_gian(): UTC, đủ mốc, không trùng; ghép thời tiết đúng múi giờ."""
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def tg(nap):
    return nap("thoi_gian")


def _la_utc(ds: pd.Series) -> bool:
    return getattr(ds.dt, "tz", None) is not None and str(ds.dt.tz) == "UTC"


def test_ket_qua_dang_dai_utc(tg):
    df = pd.DataFrame({"t": pd.date_range("2024-01-01", periods=5, freq="h"), "v": range(5)})
    kq = tg.chuan_hoa_thoi_gian(df, "t", "v")
    assert list(kq.columns) == ["unique_id", "ds", "y"], "cột phải đúng unique_id, ds, y"
    assert _la_utc(kq["ds"]), "ds phải là thời gian CÓ múi giờ UTC, không để naive"


def test_dst_mua_xuan_khong_sinh_gio_ao(tg):
    # đồng hồ New York 10/3/2024: 01:59 → 03:00, KHÔNG có 02:xx
    gio = ["2024-03-10 00:00", "2024-03-10 01:00", "2024-03-10 03:00", "2024-03-10 04:00"]
    df = pd.DataFrame({"t": pd.to_datetime(gio), "v": [10, 11, 13, 14]})
    kq = tg.chuan_hoa_thoi_gian(df, "t", "v", mui_gio_nguon="America/New_York", gop="mean")
    assert len(kq) == 4, f"4 số đo liên tiếp theo giờ thật → 4 mốc UTC liền nhau, nhận {len(kq)} (có giờ 02:00 ảo?)"
    assert kq["y"].notna().all()
    assert kq["ds"].iloc[0] == pd.Timestamp("2024-03-10 05:00", tz="UTC")


def test_dst_mua_thu_khong_gop_gio_lap(tg):
    # 3/11/2024: 01:30 xuất hiện HAI lần (EDT rồi EST)
    gio = ["2024-11-03 00:30", "2024-11-03 01:30", "2024-11-03 01:30", "2024-11-03 02:30"]
    df = pd.DataFrame({"t": pd.to_datetime(gio), "v": [1.0, 2.0, 3.0, 4.0]})
    kq = tg.chuan_hoa_thoi_gian(df, "t", "v", mui_gio_nguon="America/New_York", gop="mean", mo_ho="infer")
    assert len(kq) == 4, f"4 thời điểm thật khác nhau → 4 mốc UTC, nhận {len(kq)} (giờ lặp bị gộp?)"
    assert kq["y"].tolist() == [1.0, 2.0, 3.0, 4.0]


def test_bo_dong_trung(tg):
    df = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 00:00", "2024-01-01 00:00", "2024-01-01 01:00"]),
                       "v": [5.0, 5.0, 7.0]})
    kq = tg.chuan_hoa_thoi_gian(df, "t", "v", gop="sum", bo_trung=True)
    assert kq["y"].tolist() == [5.0, 7.0], "dòng xuất trùng phải bị bỏ trước khi cộng"
    assert not kq.duplicated(["unique_id", "ds"]).any()


def test_offset_khac_nhau_cung_thoi_diem(tg):
    df = pd.DataFrame({"t": ["2024-01-01T07:00:00+07:00", "2024-01-01T00:00:00Z", "2024-01-01T01:00:00+00:00"],
                       "v": [2.0, 4.0, 6.0]})
    kq = tg.chuan_hoa_thoi_gian(df, "t", "v", gop="mean")
    assert len(kq) == 2, "07:00+07:00 và 00:00Z là CÙNG một thời điểm"
    assert kq["y"].tolist() == [3.0, 6.0]


def test_du_moc_khi_thieu(tg):
    df = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 00:00", "2024-01-01 04:00"]), "v": [1.0, 2.0]})
    trang_thai = tg.chuan_hoa_thoi_gian(df, "t", "v", gop="mean")
    su_kien = tg.chuan_hoa_thoi_gian(df, "t", "v", gop="sum")
    assert len(trang_thai) == 5 and trang_thai["y"].isna().sum() == 3, "mốc thiếu của số đo trạng thái là NaN"
    assert len(su_kien) == 5 and (su_kien["y"] == 0).sum() == 3, "giờ không có sự kiện đếm là 0"


def test_viet_nam_khong_dst(tg):
    df = pd.DataFrame({"t": pd.to_datetime(["2024-07-01 07:00"]), "v": [1.0]})
    kq = tg.chuan_hoa_thoi_gian(df, "t", "v", mui_gio_nguon="Asia/Ho_Chi_Minh", gop="mean")
    assert kq["ds"].iloc[0] == pd.Timestamp("2024-07-01 00:00", tz="UTC")


def test_nhieu_chuoi_luoi_chung(tg):
    df = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 00:00", "2024-01-01 02:00", "2024-01-01 01:00"]),
                       "k": ["a", "a", "b"], "v": [1, 1, 1]})
    kq = tg.chuan_hoa_thoi_gian(df, "t", "v", cot_id="k", khoang=("2024-01-01 00:00", "2024-01-01 03:00"))
    assert kq.groupby("unique_id").size().to_dict() == {"a": 3, "b": 3}


# ---------------------------------------------------------------- dữ liệu thật (du-lieu/raw)


@pytest.fixture(scope="module")
def dem_thang_3(tg, du_lieu):
    return tg.dem_chuyen_theo_gio(tg.doc_chuyen_taxi("03"))


def test_taxi_thang_3_khong_co_gio_0_chuyen_ao(dem_thang_3):
    assert (dem_thang_3["y"] == 0).sum() == 0, "không có giờ nào 0 chuyến thật — giờ 0 là giờ 02:00 ảo ngày 10/3"
    assert int(dem_thang_3["y"].sum()) == 3582605


def test_ghep_thoi_tiet_dung_mui_gio(tg, dem_thang_3):
    ghep = tg.ghep_thoi_tiet(dem_thang_3, tg.doc_thoi_tiet())
    gio = tg.gio_nong_nhat(ghep)
    assert gio == 16, f"New York tháng 3 nóng nhất lúc 16h địa phương; nhận {gio}h → đang ghép lệch múi giờ"


def test_ghep_tu_choi_thoi_gian_naive(tg):
    naive = pd.DataFrame({"ds": pd.date_range("2024-03-01", periods=2, freq="h"), "y": [1, 2]})
    with pytest.raises(ValueError):
        tg.ghep_thoi_tiet(naive, tg.doc_thoi_tiet())
