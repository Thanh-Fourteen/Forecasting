"""Bộ chấm TỐI THIỂU của dự án giữa chặng 2 — `python lab.py check`.

Chấm `code/du_bao.py` của học viên trên dữ liệu 2024–2025 cố định (không cần mạng). Xanh là điều kiện cần để nộp; điểm thật
đến từ cong-cu/cham.py trên tuần tương lai và từ giám khảo (RUBRIC.md).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from tv.ro_ri import kiem_ro_ri

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "cong-cu"))
import cham as ch  # noqa: E402
import du_lieu as dl  # noqa: E402
from nop import kiem_du_bao  # noqa: E402

MOC = pd.Timestamp("2025-06-02")


@pytest.fixture(scope="module")
def hv(nap, du_lieu):
    return nap("du_bao")


@pytest.fixture(scope="module")
def dl_goc(du_lieu):
    return dl.doc_lich_su(), dl.doc_thoi_tiet()


def test_du_bao_dung_dinh_dang(hv, dl_goc):
    """du_bao trả đúng 5 vùng × 168 giờ sau mốc, không trống, không âm."""
    ls, tt = dl.dau_vao(*dl_goc, MOC)
    kiem_du_bao(hv.du_bao(ls, tt, MOC), MOC)


def test_du_bao_tai_lap(hv, dl_goc):
    """Chạy hai lần trên cùng đầu vào ra cùng một dự báo (seed cố định)."""
    ls, tt = dl.dau_vao(*dl_goc, MOC)
    a, b = hv.du_bao(ls, tt, MOC), hv.du_bao(ls, tt, MOC)
    assert np.allclose(a["du_bao"], b["du_bao"])


def test_dac_trung_khong_ro_ri(hv, dl_goc):
    """Đặc trưng lấy từ nhu cầu chỉ dùng nhu cầu tới ds − 216 giờ (lúc nộp chỉ biết tới mốc − 48 giờ, dự báo xa 168 giờ)."""
    ls, tt = dl_goc
    df = ls[(ls["vung"].isin(["NYIS", "ERCO"])) & (ls["ds"] < "2024-04-01")][["vung", "ds", "y"]]
    df = df.merge(tt[["vung", "ds", "thuc"]].rename(columns={"thuc": "nhiet_do"}), on=["vung", "ds"], how="left")
    kq = kiem_ro_ri(hv.dac_trung, df, h=216, cot_id="vung", cot_ds="ds")
    assert not kq.co_ro_ri, str(kq)


def test_thoi_tiet_backtest_la_du_bao(hv, dl_goc):
    """Trong backtest, nhiệt độ của tuần được dự báo phải là nhiệt độ ĐÃ DỰ BÁO lúc mốc (truoc_⌈h/24⌉), không phải nhiệt độ thật."""
    ls, tt = dl_goc
    bt = hv.backtest(ls, tt, [MOC, MOC + pd.Timedelta(weeks=1)])
    kq = ch.kiem_thoi_tiet_backtest(bt, tt)
    assert kq["dat"], f"nhiệt độ trong backtest lệch dự báo lưu trữ {kq['lech_trung_vi_voi_du_bao']} °C, lệch nhiệt độ thật " \
                      f"{kq['lech_trung_vi_voi_thuc']} °C (trung vị) — backtest đang dùng thời tiết chưa biết lúc mốc"


def test_backtest_chi_dung_qua_khu(hv, dl_goc):
    """Đổi nhu cầu và nhiệt độ thật SAU mốc: dự báo backtest ở mốc đó không được đổi."""
    ls, tt = dl_goc
    ls2 = ls.assign(y=np.where(ls["ds"] > MOC - pd.Timedelta(hours=dl.TRE_CONG_BO), ls["y"] * 2, ls["y"]))
    tt2 = tt.assign(thuc=np.where(tt["ds"] > MOC, tt["thuc"] + 15, tt["thuc"]))
    a = hv.backtest(ls, tt, [MOC]).sort_values(["vung", "ds"])
    b = hv.backtest(ls2, tt2, [MOC]).sort_values(["vung", "ds"])
    assert np.allclose(a["du_bao"].to_numpy(), b["du_bao"].to_numpy())


def test_backtest_8_tuan(hv, dl_goc):
    """cac_moc_backtest: 8 mốc thứ Hai, mỗi mốc 5 vùng × 168 giờ, cột đúng tên."""
    moc_nop = pd.Timestamp("2025-03-03")
    cac = dl.cac_moc_backtest(moc_nop)
    assert len(cac) == 8 and all(m.weekday() == 0 for m in cac)
    assert cac[-1] + pd.Timedelta(hours=dl.H + dl.TRE_CONG_BO) <= moc_nop
    bt = hv.backtest(*dl_goc, cac[-2:])
    assert {"vung", "moc", "ds", "h", "y", "du_bao", "nhiet_do"} <= set(bt.columns)
    assert len(bt) == 2 * 5 * dl.H and bt["h"].between(1, dl.H).all()
