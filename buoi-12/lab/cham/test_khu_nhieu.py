"""Bộ chấm buổi 12 — aliasing, bảng bộ lọc, và TEST RÒ RỈ: bộ lọc dùng tương lai phải bị bắt."""
from __future__ import annotations

import numpy as np
import pytest

NHAN_QUA = {"MA trailing 13", "EWMA α=0,15", "Butterworth nhân quả", "Kalman filter (tham số cố định)"}
KHONG_NHAN_QUA = {"MA centered 13", "Savitzky–Golay 13", "Butterworth filtfilt", "Kalman smoother",
                  "Kalman filter (khớp lại cả chuỗi)", "Wavelet db4"}


@pytest.fixture(scope="module")
def m(nap):
    return nap("khu_nhieu")


@pytest.fixture(scope="module")
def df(m, du_lieu):
    return m.doc_cam_bien()


@pytest.fixture(scope="module")
def mo_phong(m):
    return m.sinh_tin_hieu()


def test_doc_du_lieu(df):
    assert len(df) == 19735 and df.index.freqstr == "10min"
    assert df.notna().all().all()


def test_pho_tim_dung_chu_ky_ngay(m, df):
    f, P = m.pho(df["Appliances"])
    chu_ky = 1 / f[1:][np.argmax(P[1:])]
    assert 23 < chu_ky < 26, f"đỉnh phổ ở {chu_ky:.1f} giờ — phải là nhịp ngày"


def test_kiem_nhan_qua_bat_dung(m, mo_phong):
    _, y = mo_phong
    bo_loc = m.bo_loc_mac_dinh(y[:600])
    for ten in NHAN_QUA:
        assert m.kiem_nhan_qua(bo_loc[ten], y)["nhan_qua"], f"{ten} là bộ lọc nhân quả nhưng bị báo là dùng tương lai"
    for ten in KHONG_NHAN_QUA:
        kq = m.kiem_nhan_qua(bo_loc[ten], y)
        assert not kq["nhan_qua"], f"{ten} DÙNG TƯƠNG LAI nhưng test không bắt được (đổi quá khứ {kq['doi_qua_khu']:.2g})"


def test_kiem_nhan_qua_xet_moi_moc_truoc_diem_doi(m, mo_phong):
    """Bắt kiểu test 'bỏ qua phần cuối cho chắc': MA có tâm chỉ lộ ở vài mốc ngay trước điểm đổi."""
    _, y = mo_phong
    kq = m.kiem_nhan_qua(m.ma_giua, y, so_diem_doi=10)
    assert kq["moc_dau_tien_bi_doi"] >= len(y) - 20, "phải so tới sát điểm đổi dữ liệu"


def test_aliasing(m):
    t = np.arange(6000) / m.FS
    that = 20 + 2 * np.sin(2 * np.pi * t / 24)
    y = that + 0.5 * np.sin(2 * np.pi * 1.4 * t)  # 1,4 chu kỳ/giờ ≈ chu kỳ 43 phút
    tho, sach = m.ha_mau(y, 6, loc_truoc=False), m.ha_mau(y, 6, loc_truoc=True)
    f1, P1 = m.pho(tho, fs=1.0, nperseg=512)
    f2, P2 = m.pho(sach, fs=1.0, nperseg=512)
    # gập xuống |1,4 − 1| = 0,4 chu kỳ/giờ → chu kỳ giả 2,5 giờ
    assert m.cong_suat_quanh(f1, P1, 2.5) > 1.0, "hạ mẫu thô phải sinh đỉnh giả ở chu kỳ 2,5 giờ"
    assert m.cong_suat_quanh(f2, P2, 2.5) < 0.01 * m.cong_suat_quanh(f1, P1, 2.5), "lọc trước khi hạ mẫu phải xoá đỉnh giả"


def test_bang_bo_loc_co_cot_dung_tuong_lai(m, mo_phong):
    that, y = mo_phong
    bang = m.bang_bo_loc(y, that).set_index("bộ lọc")
    assert "dùng tương lai?" in bang.columns
    for ten in NHAN_QUA | KHONG_NHAN_QUA:
        assert ten in bang.index, f"bảng thiếu {ten}"
        assert bool(bang.loc[ten, "dùng tương lai?"]) == (ten in KHONG_NHAN_QUA), f"cột 'dùng tương lai?' sai ở {ten}"
    assert bang.loc["MA trailing 13", "trễ (bước)"] >= 5, "MA trailing 13 trễ khoảng nửa cửa sổ"
    assert bang.loc["MA centered 13", "trễ (bước)"] == 0


def test_gia_cua_ro_ri(m, df):
    bang = m.gia_cua_ro_ri(df["Appliances"]).set_index("feature")
    goc = bang.loc["không lọc", "MAE"]
    assert bang.loc["MA centered 13", "MAE"] < 0.85 * goc, "feature dùng tương lai phải cho MAE 'đẹp' giả"
    assert bang.loc["MA trailing 13", "MAE"] > 0.9 * goc
    assert bool(bang.loc["MA centered 13", "dùng tương lai?"]) is True
    assert bool(bang.loc["MA trailing 13", "dùng tương lai?"]) is False


def test_cham_tren_muc_tieu_goc(m, df):
    kq = m.cham_tren_muc_tieu_lam_tron(df["Appliances"])
    assert "mae_muc_tieu_goc" in kq, "phải báo sai số trên MỤC TIÊU GỐC, không chỉ trên mục tiêu đã làm trơn"
    assert kq["mae_muc_tieu_goc"] > kq["mae_muc_tieu_lam_tron"], "khử nhiễu mục tiêu làm sai số nhỏ đi một cách giả tạo"
