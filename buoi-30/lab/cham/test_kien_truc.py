"""Bộ chấm buổi 30 — covariate đúng loại, không rò rỉ. Mỗi test kiểm một hành vi; thông báo lỗi nói cần sửa gì."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tv.ro_ri import kiem_ro_ri


@pytest.fixture(scope="session")
def kt(nap, du_lieu):
    return nap("kien_truc")


@pytest.fixture(scope="session")
def d(kt):
    return kt.doc_du_lieu()


def test_futr_chi_gom_so_biet_truoc(kt, d):
    """Đổi nhiệt độ THỰC của các giờ sau mốc: dữ liệu tương lai đưa cho mô hình lúc mốc phải y nguyên."""
    moc = kt.MOC_TEST + pd.Timedelta(days=10)
    _, a = kt.du_lieu_moc(d, moc)
    d2 = d.copy()
    d2.loc[d2["ds"] > moc, "nhiet_do_thuc"] += 15.0
    _, b = kt.du_lieu_moc(d2, moc)
    pd.testing.assert_frame_equal(a, b, obj=(
        "futr_df lúc mốc đổi khi nhiệt độ thực SAU mốc đổi — một covariate tương lai là số đo chỉ biết sau (nhiệt độ thực). "
        "Nhiệt độ thực chỉ là hist_exog; tương lai dùng nhiệt độ đã dự báo (mục 4.1)"))


def test_cau_hinh_covariate(kt):
    assert "nhiet_do_thuc" not in kt.FUTR_EXOG, "nhiet_do_thuc khai là futr_exog: rò rỉ (mục 4.1)"
    assert "nhiet_do_du_bao" in kt.FUTR_EXOG, "nhiệt độ đã dự báo trước 1 ngày biết trước cho cả 24 giờ tới — đó là futr_exog"
    m = kt.tao_mo_hinh("TiDE", max_steps=1)
    assert list(m.futr_exog_list) == kt.FUTR_EXOG and list(m.hist_exog_list) == kt.HIST_EXOG, \
        "tao_mo_hinh phải dùng đúng FUTR_EXOG / HIST_EXOG của module"
    assert list(kt.tao_mo_hinh("DeepAR", max_steps=1).hist_exog_list) == [], "DeepAR không nhận hist_exog (mục 4.3)"


def test_lam_sach_khong_nhin_tuong_lai(kt, d):
    nho = d[d["unique_id"].isin(["NYIS", "PJM"]) & (d["ds"] < pd.Timestamp("2024-05-01"))][["unique_id", "ds", "y"]]
    kq = kiem_ro_ri(kt.lam_sach, nho.reset_index(drop=True), h=None)
    assert not kq.co_ro_ri, "làm sạch nhu cầu dùng giá trị sau thời điểm đang xét (trung vị căn giữa, nội suy hai chiều?). " + str(kq)


def test_seasonal_naive_vi_du_tay(kt):
    ds = pd.date_range("2025-01-01 01:00", periods=24 * 14, freq="h")
    y = np.arange(len(ds), dtype=float)
    d = pd.concat([pd.DataFrame({"unique_id": v, "ds": ds, "y": y}) for v in kt.VUNG])
    moc = ds[-25]
    p = kt.seasonal_naive(d, [moc])
    assert np.allclose(p[p["unique_id"] == "ERCO"]["SeasonalNaive"].to_numpy(), y[-24:] - 168), \
        "seasonal naive tuần: giờ t bằng giờ t − 168"


def test_mase_vi_du_tay(kt):
    ds = pd.date_range("2024-02-01 01:00", periods=24 * 21, freq="h")
    d = pd.DataFrame({"unique_id": "CISO", "ds": ds, "y": np.tile([10.0, 20.0], len(ds) // 2)})
    d.loc[d.index % 336 < 168, "y"] += 4                      # tuần lẻ cao hơn 4 → seasonal naive tuần sai đúng 4
    du = d.iloc[-24:][["unique_id", "ds"]].assign(M=d["y"].iloc[-24:].to_numpy() + 2)
    assert abs(kt.bang_mase(du, d, ["M"]).loc["M", "trung bình"] - 0.5) < 1e-9, "MAE 2 / mẫu số 4 = MASE 0,5"
