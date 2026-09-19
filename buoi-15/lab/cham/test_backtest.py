"""Bộ chấm buổi 15 — backtesting đúng cách.

Chấm `code/backtest.py` (mặc định) hoặc `dap-an/backtest.py` khi BAI=dap-an. Bộ backtest của buổi này là
công cụ cả khoá dùng, nên phần lớn test kiểm chính nó: vị trí cửa sổ, không lộ tương lai, khớp statsforecast.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def bt(nap):
    return nap("backtest")


def _dai(n=30, ds_so=False):
    ds = np.arange(n) if ds_so else pd.date_range("2024-01-01", periods=n, freq="D")
    return pd.concat([pd.DataFrame({"unique_id": uid, "ds": ds, "y": np.arange(n, dtype=float) * k})
                      for uid, k in (("a", 1.0), ("b", 2.0))], ignore_index=True)


def _naive(lich_su, ds_can):
    cuoi = lich_su.sort_values("ds").groupby("unique_id")["y"].last()
    return ds_can.assign(naive=ds_can["unique_id"].map(cuoi))


# ------------------------------------------------------------------ bộ backtest

def test_vi_tri_cua_so_co_gap(bt):
    """Cửa sổ cuối kết thúc đúng ở mốc cuối; gap bước bỏ trống giữa cutoff và đoạn kiểm."""
    cs = bt.chia_cua_so(_dai(20, ds_so=True), h=3, so_cua_so=2, buoc=2, gap=1)
    assert [(c.cutoff, c.bat_dau_test, c.ket_thuc_test) for c in cs] == [(13, 15, 17), (15, 17, 19)]
    with pytest.raises(ValueError):
        bt.chia_cua_so(_dai(20, ds_so=True), h=3, so_cua_so=10, buoc=3)


def test_ham_du_bao_khong_thay_tuong_lai(bt):
    """Hàm dự báo chỉ nhận lịch sử tới cutoff; buoc_h đếm từ cutoff (gap 2 → bước 3..6)."""
    da_thay = []

    def du_bao(lich_su, ds_can):
        da_thay.append((lich_su["ds"].max(), ds_can["ds"].min()))
        return _naive(lich_su, ds_can)

    kq = bt.backtest(_dai(30), du_bao, h=4, so_cua_so=3, gap=2)
    assert len(da_thay) == 3
    assert all((dau - cuoi).days == 3 for cuoi, dau in da_thay), "lịch sử phải dừng ở cutoff, cách đoạn kiểm gap bước"
    assert set(kq["buoc_h"]) == {3, 4, 5, 6}
    assert np.allclose(kq["y"] - kq["naive"], kq["unique_id"].map({"a": 1.0, "b": 2.0}) * kq["buoc_h"])


def test_sliding_window(bt):
    do_dai = []
    bt.backtest(_dai(30), lambda ls, dc: (do_dai.append(ls["ds"].nunique()), _naive(ls, dc))[1],
                h=2, so_cua_so=3, cua_so_train=10)
    assert do_dai == [10, 10, 10]


def test_du_bao_thua_dong_bao_loi(bt):
    def thua(lich_su, ds_can):
        them = ds_can.assign(ds=ds_can["ds"] + pd.Timedelta("10D"))
        return _naive(lich_su, pd.concat([ds_can, them]))

    with pytest.raises(ValueError):
        bt.backtest(_dai(30), thua, h=2, so_cua_so=2)


def test_khop_statsforecast(bt, du_lieu):
    """Cùng cutoff, cùng seasonal naive với statsforecast.cross_validation trên 20 chuỗi M4 theo giờ."""
    chuoi = bt.doc_m4_gio()
    df = bt.m4_dang_dai(chuoi)
    df = df[df["unique_id"].isin(df["unique_id"].unique()[:20])]
    assert bt.doi_chieu_statsforecast(df) == pytest.approx(0.0, abs=1e-9)


def test_feature_khong_ro_ri(bt):
    """Feature cho y_t chỉ dùng y tới t − 24 (dự báo ngày tới): bài kiểm cắt tương lai + nhiễu mục tiêu."""
    from tv.ro_ri import kiem_ro_ri
    idx = pd.date_range("2024-01-01", periods=24 * 40, freq="h")
    y = pd.Series(np.random.default_rng(0).normal(100, 10, len(idx)), index=idx)
    df = pd.DataFrame({"ds": idx, "y": y.to_numpy()})

    def ham(d):
        return bt.bang_feature(d.set_index("ds")["y"]).reset_index(names="ds")

    kq = kiem_ro_ri(ham, df, h=24, cot_id=None)
    assert not kq.co_ro_ri, str(kq)


# ------------------------------------------------------------------ ba chỗ bài học sửa

def test_uoc_luong_khong_chia_ngau_nhien(bt):
    """Chuỗi bước ngẫu nhiên + mô hình láng giềng gần nhất: chia ngẫu nhiên cho sai số nhỏ giả tạo, vì hàng xóm
    trong thời gian của mỗi dòng kiểm nằm sẵn trong tập học. Ước lượng trung thực phải lớn hơn hẳn."""
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsRegressor
    rng = np.random.default_rng(0)
    idx = pd.date_range("2024-01-01", periods=24 * 90, freq="h")
    y = pd.Series(1000 + np.cumsum(rng.normal(0, 10, len(idx))) + 50 * np.sin(2 * np.pi * idx.hour / 24), index=idx)
    bang = bt.bang_feature(y).assign(y=y).dropna()
    hoc, kiem = train_test_split(bang, test_size=0.2, shuffle=True, random_state=0)
    ngau_nhien = float(np.mean(np.abs(
        KNeighborsRegressor(5).fit(hoc.drop(columns="y"), hoc["y"]).predict(kiem.drop(columns="y")) - kiem["y"])))
    uoc = bt.uoc_luong_sai_so(y, lambda: KNeighborsRegressor(5))
    assert uoc > 2 * ngau_nhien, (
        f"ước lượng {uoc:.1f} gần bằng chia ngẫu nhiên ({ngau_nhien:.1f}) — đang để tương lai lọt vào tập học?")


def test_bao_cao_tren_doan_chua_dung_de_chon(bt):
    """Đoạn cuối cố tình dễ cho 'naive' (hằng số). Chọn trên chính đoạn đó thì báo MASE 0; chọn trên đoạn trước
    (chuỗi lặp theo ngày) rồi báo cáo trên đoạn cuối thì phải thấy sai số thật, rất lớn."""
    rng = np.random.default_rng(0)
    v = np.tile(rng.normal(0, 1, 24) * 10 + 100, 40) + rng.normal(0, 0.5, 960)
    v[-48:] = v[-49]
    dong = bt.chon_va_bao_cao({"x": v}).iloc[0]
    assert dong["chọn"] != "naive", "phương pháp được chọn nhờ nhìn thấy chính đoạn báo cáo"
    assert dong["MASE báo cáo (B)"] > 10, f"MASE báo cáo {dong['MASE báo cáo (B)']:.2f} — báo cáo trên đoạn đã dùng để chọn?"


def test_diebold_mariano_hieu_chinh(bt):
    """Ví dụ tay Phụ lục D (h = 1) và sai số tự tương quan với h = 6: phải cộng tự hiệp phương sai tới trễ h − 1
    và nhân hệ số Harvey–Leybourne–Newbold, so với phân phối t."""
    y, f = np.array([10, 12, 8, 14, 16.0]), np.array([11, 10, 9, 14, 12.0])
    kq = bt.diebold_mariano(y - f, y - 13, h=1, ham_mat_mat="binh_phuong")
    assert kq.thong_ke == pytest.approx(-0.8446411935168505, rel=1e-9)
    assert kq.p_value == pytest.approx(0.44586962342552555, rel=1e-6)
    rng = np.random.default_rng(7)
    goc = rng.normal(0, 1, 300)
    e1 = np.convolve(goc, np.ones(6) / 6, "same")
    e2 = 0.8 * e1 + rng.normal(0, 0.6, 300)
    kq = bt.diebold_mariano(e1, e2, h=6)
    assert kq.thong_ke == pytest.approx(-7.993912795379818, rel=1e-9), (
        "với h = 6, phương sai của trung bình phải cộng tự hiệp phương sai trễ 1..5")
