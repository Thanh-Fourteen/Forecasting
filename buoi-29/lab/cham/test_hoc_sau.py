"""Bộ chấm buổi 29 — nền deep learning. Mỗi test kiểm một hành vi; thông báo lỗi nói cần sửa gì."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import torch

from tv.ro_ri import kiem_chong_lan, kiem_ro_ri


@pytest.fixture(scope="session")
def hs(nap, du_lieu):
    return nap("hoc_sau")


@pytest.fixture(scope="session")
def df_nho(hs):
    """8 khách hàng, đủ để kiểm cách chia và chuẩn hoá (không huấn luyện)."""
    d = hs.doc_dien(so_khach=16)
    return d[d["unique_id"].isin(sorted(d["unique_id"].unique())[:8])].reset_index(drop=True)


def test_cat_cua_so_vi_du_tay(hs):
    X, Y, dau = hs.cat_cua_so(np.arange(10.0), L=3, H=2)
    assert X.shape == (6, 3) and Y.shape == (6, 2), f"chuỗi 10 điểm, L = 3, H = 2 → 6 cửa sổ; đang ra {X.shape}, {Y.shape}"
    assert X[0].tolist() == [0, 1, 2] and Y[0].tolist() == [3, 4] and Y[-1].tolist() == [8, 9], \
        "cửa sổ đầu: đầu vào 0, 1, 2 → mục tiêu 3, 4; cửa sổ cuối có mục tiêu 8, 9 (mục 4.1)"


def test_train_val_khong_chong_lan(hs, df_nho):
    sc = hs.hoc_scaler(df_nho)
    train, val = hs.chia_train_val(df_nho, sc)
    uid = np.array(sorted(df_nho["unique_id"].unique()))
    muc_tieu = lambda tap: pd.DataFrame({  # noqa: E731 — giờ mục tiêu CUỐI của mỗi mẫu
        "unique_id": uid[tap["ma"]], "ds": pd.to_datetime(tap["ds"]) + pd.Timedelta(hours=hs.H - 1)})
    dau_val = pd.DataFrame({"unique_id": uid[val["ma"]], "ds": pd.to_datetime(val["ds"])})
    kq = kiem_chong_lan(muc_tieu(train), dau_val)
    assert not kq.co_ro_ri, ("cửa sổ train có mục tiêu rơi vào thời gian của val — mô hình đã thấy đáp án của val. "
                     "Chia theo thời gian TRƯỚC rồi mới cắt cửa sổ (mục 4.1). " + str(kq))


def test_scaler_chi_hoc_tren_train(hs, df_nho):
    def bang_chuan_hoa(d: pd.DataFrame) -> pd.DataFrame:
        sc = hs.hoc_scaler(d)
        return d.assign(z=[hs.chuan_hoa(np.array([y]), sc[u])[0] for u, y in zip(d["unique_id"], d["y"], strict=True)])
    nho = df_nho[df_nho["ds"] >= hs.MOC_VAL - pd.Timedelta(days=60)].reset_index(drop=True)
    kq = kiem_ro_ri(bang_chuan_hoa, nho, cac_moc_cat=[hs.MOC_VAL + pd.Timedelta(days=10), hs.MOC_TEST], h=None,
                    cot_bo_qua=["y"])
    assert not kq.co_ro_ri, ("trung bình / độ lệch chuẩn của scaler đổi khi dữ liệu sau mốc train đổi — scaler đã học cả val, test. "
                     "Chỉ học trên ds < MOC_VAL (mục 4.2). " + str(kq))


def test_revin_vi_du_tay(hs):
    r = hs.RevIN()
    x = torch.tensor([[2.0, 4.0, 6.0]])
    z = r.chuan(x)
    assert torch.allclose(z, torch.tensor([[-1.0, 0.0, 1.0]]), atol=1e-4), "ví dụ mục 4.2: 2, 4, 6 → −1, 0, 1"
    assert torch.allclose(r.tra_lai(torch.tensor([[0.5]])), torch.tensor([[5.0]]), atol=1e-4), \
        "dự báo 0,5 trên thang chuẩn hoá phải trả về 4 + 0,5 × 2 = 5"


def test_tcn_chi_nhin_qua_khu(hs):
    torch.manual_seed(0)
    m = hs.TCN()
    x = torch.randn(2, hs.L)
    x2 = x.clone()
    x2[:, 100:] += 10.0                     # đổi mọi giờ từ vị trí 100 trở đi
    with torch.no_grad():
        a, b = m.dac_trung(x), m.dac_trung(x2)
    assert torch.allclose(a[:, :, :100], b[:, :, :100], atol=1e-5), \
        "đặc trưng TCN tại giờ t đổi khi giờ sau t đổi — tích chập không nhân quả (mục 4.5)"


def test_huan_luyen_tai_lap(hs):
    rng = np.random.default_rng(1)
    tap = {"X": torch.tensor(rng.normal(size=(512, hs.L)), dtype=torch.float32),
           "Y": torch.tensor(rng.normal(size=(512, hs.H)), dtype=torch.float32)}
    ls = []
    for _ in range(2):
        hs.dat_seed(7)                         # seed đặt TRƯỚC khi tạo mạng: trọng số khởi tạo giống nhau
        m = hs.MLP(an=16)
        ls.append(hs.huan_luyen(m, tap, tap, so_epoch=2, lo=32, buoc_moi_epoch=5, seed=7)["lich_su"]["train"].to_numpy())
    assert np.allclose(ls[0], ls[1]), "cùng seed mà hai lần huấn luyện ra loss khác nhau — kiểm dat_seed (mục 4.6)"
