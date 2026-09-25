"""Bộ chấm buổi 28 — dự báo phân cấp. Mỗi test kiểm một hành vi; thông báo lỗi nói cần sửa gì."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="session")
def pc(nap, du_lieu):
    return nap("phan_cap")


@pytest.fixture(scope="session")
def cay(pc):
    return pc.tong_hop(pc.doc_du_lich())


@pytest.fixture(scope="session")
def moc_cuoi(pc, cay):
    Y, S_df, tags = cay
    return pc.du_bao_mot_moc(Y, S_df, tags, pc.MOC_CAT[-1])


def test_cay_dung_kich_thuoc(pc, cay):
    Y, S_df, tags = cay
    ten, S = pc.ma_tran_S(S_df)
    assert S.shape == (389, 304), f"ma trận S phải 389 × 304 (1 + 8 + 76 + 304 chuỗi, 304 chuỗi đáy), đang là {S.shape}"
    assert np.allclose(S.sum(axis=1)[0], 304), "dòng quốc gia của S phải cộng đủ 304 chuỗi đáy"


def test_hoa_giai_ols_vi_du_tay(pc):
    S = np.array([[1.0, 1], [1, 0], [0, 1]])
    ra = pc.hoa_giai_ols(np.array([10.0, 4, 5]), S)
    assert np.allclose(ra, [29 / 3, 13 / 3, 16 / 3]), "ví dụ tay mục 4.3: tổng 10, A 4, B 5 → OLS 9,67 / 4,33 / 5,33"


def test_hoa_giai_ols_khop_thu_vien(pc, cay, moc_cuoi):
    _, S_df, _ = cay
    ten, S = pc.ma_tran_S(S_df)
    base = moc_cuoi.pivot(index="unique_id", columns="ds", values="AutoETS").loc[ten].to_numpy()
    lib = moc_cuoi.pivot(index="unique_id", columns="ds", values="AutoETS/MinTrace_method-ols").loc[ten].to_numpy()
    assert np.allclose(pc.hoa_giai_ols(base, S), lib, atol=1e-6), "OLS tự viết phải trùng MinTrace(method='ols')"


def test_du_bao_dem_dung_cong_khop_moi_cap(pc, cay, moc_cuoi):
    _, S_df, _ = cay
    du = pc.du_bao_khop(moc_cuoi)
    lech = pc.do_lech_cong(du.rename(columns={"du_bao": "x"}), S_df, "x")
    assert lech < 1e-6, (f"dự báo đem dùng lệch cộng tới {lech:,.0f} nghìn chuyến: dự báo cấp trên khác tổng các chuỗi bên dưới. "
                         "Chọn một cách hoà giải (mục 4.2–4.3)")


def test_du_bao_khong_dung_tuong_lai(pc, cay):
    """Dự báo tại mốc cắt không đổi khi số liệu sau mốc đổi."""
    Y, S_df, tags = cay
    moc = pd.Timestamp(pc.MOC_CAT[0])
    Y2 = Y.copy()
    Y2.loc[Y2["ds"] > moc, "y"] = Y2.loc[Y2["ds"] > moc, "y"] * 3
    a = pc.du_bao_mot_moc(Y, S_df, tags, moc).sort_values(["unique_id", "ds"])
    b = pc.du_bao_mot_moc(Y2, S_df, tags, moc).sort_values(["unique_id", "ds"])
    assert np.allclose(a["AutoETS"], b["AutoETS"]), "dự báo tại mốc cắt dùng số liệu sau mốc — rò rỉ tương lai"


def test_khoang_khop_chi_dung_sai_so_da_biet(pc, cay):
    """Khoảng ở mốc c chỉ dùng sai số của những mốc đã có đủ thực tế lúc c."""
    Y, S_df, _ = cay
    ten, S = pc.ma_tran_S(S_df)
    F, A = pc.sai_so_ngoai_mau(Y, S_df, so_moc=16)
    c = sorted(F.index.get_level_values(0).unique())[-1]
    A2 = A.copy()
    muon = A2.index.get_level_values(0) > c - pd.DateOffset(months=3 * pc.H_XS)
    A2.loc[muon & (A2.index.get_level_values(0) != c)] += 1e6
    k1 = pc.khoang_khop(F, A, S)
    k2 = pc.khoang_khop(F, A2, S)
    a, b = k1[k1["moc"] == c], k2[k2["moc"] == c]
    assert np.allclose(a["lo"], b["lo"]) and np.allclose(a["hi"], b["hi"]), \
        "khoảng tại mốc c dùng sai số của mốc chưa có đủ thực tế — rò rỉ tương lai"
