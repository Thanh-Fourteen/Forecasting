"""Bộ chấm buổi 13 — feature engineering và chống rò rỉ.

Buổi này học viên TỰ VIẾT `kiem_ro_ri`, nên bộ chấm có hai phần:
  * chấm chính bài kiểm của học viên bằng các hàm feature rò rỉ đã biết trước (phải bắt đủ);
  * chấm bộ feature của học viên bằng một bài kiểm độc lập viết trong tệp này.
"""
from __future__ import annotations

import datetime as dt

import holidays
import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def ft(nap, du_lieu):
    return nap("feature")


@pytest.fixture(scope="module")
def y(ft):
    return ft.doc_ban_le().ffill()


# --------------------------------------------------------------- bài kiểm độc lập của bộ chấm
def _ro_ri_doc_lap(ham_feature, y: pd.Series, ty_le=(0.5, 0.7, 0.9)) -> set[str]:  # noqa: D401
    """Cắt dữ liệu tại vài mốc, tính lại, so MỌI dòng ≤ mốc. Trả tên các cột đổi giá trị."""
    day_du = ham_feature(y)
    xau: set[str] = set()
    for p in ty_le:
        moc = y.index[int(len(y) * p)]
        cat = ham_feature(y[y.index <= moc])
        chung = day_du.index[day_du.index <= moc]
        for cot in day_du.columns:
            a = day_du.loc[chung, cot].to_numpy(dtype=float)
            b = (cat.reindex(chung)[cot].to_numpy(dtype=float) if cot in cat.columns
                 else np.full(len(chung), np.nan))
            if not np.allclose(a, b, rtol=0, atol=1e-9, equal_nan=True):
                xau.add(cot)
    return xau


def _ham_ro_ri(y: pd.Series) -> pd.DataFrame:
    """Bốn kiểu rò rỉ kinh điển + hai cột nhân quả để kiểm báo động giả."""
    # khoét lỗ theo NGÀY (không theo vị trí) để mẫu lỗ không đổi khi cắt chuỗi.
    # Nội suy hai chiều chỉ lộ rò rỉ ở mép lỗ, nên bộ chấm cắt đúng vào một ngày bị khoét.
    lo = y.where(y.index.day % 2 == 0)
    return pd.DataFrame({
        "rolling_khong_shift": y.rolling(7, center=True).mean(),
        "chuan_hoa_toan_bo": (y - y.mean()) / y.std(),
        "target_encoding_toan_bo": y.groupby(y.index.dayofweek).transform("mean"),
        "dien_hai_chieu": lo.interpolate(limit_direction="both"),
        "lag_1_sach": y.shift(1),
        "rolling_co_shift": y.shift(1).rolling(7).mean(),
    }, index=y.index)


MOC_CAT = [pd.Timestamp("2010-03-15"), pd.Timestamp("2010-07-09"), pd.Timestamp("2010-11-21")]


def test_kiem_ro_ri_bat_du_bon_kieu(ft, y):
    """`kiem_ro_ri` của bạn phải bắt đủ 4 kiểu rò rỉ kinh điển."""
    nho = y.iloc[:400]
    bang = ft.kiem_ro_ri(_ham_ro_ri, nho, cac_moc=MOC_CAT)
    bat = set(bang["feature"]) if len(bang) else set()
    for cot in ("rolling_khong_shift", "chuan_hoa_toan_bo", "target_encoding_toan_bo", "dien_hai_chieu"):
        assert cot in bat, f"bỏ sót rò rỉ ở cột {cot}; mới bắt được {sorted(bat)}"


def test_kiem_ro_ri_khong_bao_dong_gia(ft, y):
    """...và không được gắn cờ feature nhân quả."""
    nho = y.iloc[:400]
    bang = ft.kiem_ro_ri(_ham_ro_ri, nho, cac_moc=MOC_CAT)
    bat = set(bang["feature"]) if len(bang) else set()
    assert "lag_1_sach" not in bat and "rolling_co_shift" not in bat, f"báo động giả: {sorted(bat)}"


def test_bo_feature_khong_ro_ri(ft, y):
    """Bộ feature của bạn phải sạch theo bài kiểm ĐỘC LẬP của bộ chấm (không dùng hàm của bạn)."""
    xau = _ro_ri_doc_lap(ft.bo_feature, y.iloc[:600])
    assert not xau, f"các feature này đổi giá trị ở quá khứ khi biết thêm tương lai: {sorted(xau)}"


def test_bo_feature_du_so_luong(ft, y):
    f = ft.bo_feature(y.iloc[:400])
    assert f.shape[1] >= 40, f"đề bài yêu cầu ≥ 40 feature, đang có {f.shape[1]}"
    assert f.index.equals(y.iloc[:400].index)


def test_lag_khong_nho_hon_tam(ft, y):
    """Feature cho y_{t+h} không được dùng y ở thời điểm muộn hơn t. Kiểm bằng bài nhiễu mục tiêu."""
    xau = ft.kiem_nhieu_muc_tieu(ft.bo_feature, y.iloc[:600], tam=1)
    assert not xau, f"các feature này đổi khi y tương lai đổi: {xau}"


def test_bang_biet_truoc_day_du(ft, y):
    """Mỗi feature phải khai 'biết trước bao lâu' — không có cột nào không phân loại."""
    f = ft.bo_feature(y.iloc[:400])
    bang = ft.bang_biet_truoc(f)
    assert len(bang) == f.shape[1]
    assert set(bang["biết trước"]) <= {ft.BIET_TRUOC_VO_HAN, ft.BIET_TRUOC_TRE,
                                       ft.BIET_TRUOC_KE_HOACH, "KHÔNG BIẾT TRƯỚC"}
    assert not (bang["biết trước"] == "KHÔNG BIẾT TRƯỚC").any(), (
        "bộ feature đang chứa biến không biết trước tại thời điểm ra dự báo")


# --------------------------------------------------------------- âm lịch
def test_tet_dung_moi_nam_2000_2035(ft):
    """Ngày mùng 1 Tết phải khớp nguồn độc lập (thư viện `holidays`) cho TOÀN BỘ 2000–2035."""
    lech = []
    for nam in range(2000, 2036):
        le = holidays.country_holidays("VN", years=nam)
        moc = {d for d, ten in le.items() if ten == "Lunar New Year"}
        if ft.tet(nam) not in moc:
            lech.append((nam, ft.tet(nam), sorted(moc)))
    assert not lech, f"Tết sai ở {len(lech)} năm: {lech[:5]}"


def test_tet_viet_nam_khac_trung_quoc(ft):
    """Âm lịch VN tính ở kinh tuyến 105°Đ (UTC+7), Trung Quốc ở 120°Đ (UTC+8) — 2007 và 2030 lệch."""
    assert ft.tet(2007, 7) == dt.date(2007, 2, 17)
    assert ft.tet(2007, 8) == dt.date(2007, 2, 18)
    lech = [n for n in range(2000, 2036) if ft.tet(n, 7) != ft.tet(n, 8)]
    assert lech == [2007, 2030], f"các năm lệch phải là 2007 và 2030, đang ra {lech}"


def test_so_ngay_toi_tet_dung_moi_nam(ft):
    """Feature Tết phải đúng cho MỌI năm, không hardcode một năm."""
    moc = pd.date_range("2016-01-01", "2025-12-31", freq="D")
    d = ft.so_ngay_toi_tet(moc)
    for nam in range(2016, 2026):
        ngay_tet = pd.Timestamp(ft.tet(nam))
        assert d.loc[ngay_tet] == 0, f"Tết {nam} ({ngay_tet.date()}) phải có so_ngay_toi_tet = 0, đang là {d.loc[ngay_tet]}"
    assert d.abs().max() <= 200


def test_gio_to_hung_vuong(ft):
    """Giỗ Tổ (10/3 âm lịch) 2024 rơi vào 18/04/2024."""
    assert ft.gio_to(2024) == dt.date(2024, 4, 18)


# --------------------------------------------------------------- giá của rò rỉ
def test_gia_cua_ro_ri(ft):
    """Bảng phải có cả ba: kết quả hứa hẹn khi rò rỉ, kết quả thật khi chạy bằng dự báo, và baseline."""
    bang = ft.gia_cua_ro_ri().set_index("bộ feature")
    assert len(bang) >= 5
    nen = bang.loc["chỉ lag + giờ", "MAE (MW)"]
    ro_ri = bang[bang["dùng tương lai?"]]
    assert len(ro_ri) >= 2, "phải có cả dòng 'nhiệt độ thật' và dòng 'huấn luyện bằng thật, chạy bằng dự báo'"
    assert ro_ri["MAE (MW)"].min() < nen, "feature rò rỉ phải cho MAE đẹp hơn baseline (đó là cái bẫy)"
    chay_that = bang[bang.index.str.startswith("huấn luyện bằng nhiệt độ thật, CHẠY")]
    assert len(chay_that) >= 1
    assert chay_that["MAE (MW)"].max() > bang.loc["+ nhiệt độ THẬT của giờ cần dự báo (rò rỉ)", "MAE (MW)"], (
        "kết quả chạy thật phải TỆ HƠN kết quả hứa hẹn của backtest rò rỉ")


def test_du_bao_thoi_tiet_khong_hoan_hao(ft):
    """Lý do 'nhiệt độ thật' cho kết quả đẹp giả: dự báo có sai số, và càng xa càng sai."""
    kq = ft.sai_so_du_bao_thoi_tiet()
    assert 0.5 < kq["MAE dự báo 1 ngày (°C)"] < 3
    assert kq["MAE dự báo 3 ngày (°C)"] > kq["MAE dự báo 1 ngày (°C)"]


def test_feature_tet_giup_quanh_tet(ft):
    """Feature Tết âm lịch phải cải thiện sai số QUANH TẾT, không chỉ trung bình cả năm."""
    bang = ft.gia_tri_feature_tet().set_index("bộ feature")
    truoc = bang.loc["chỉ lag + lịch dương", "MAE quanh Tết (±10 ngày)"]
    sau = bang.loc["+ feature Tết âm lịch", "MAE quanh Tết (±10 ngày)"]
    assert sau < truoc * 0.95, f"cải thiện quanh Tết quá ít: {truoc:.0f} → {sau:.0f}"
