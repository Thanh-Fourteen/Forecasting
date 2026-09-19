"""Bộ chấm buổi 14 — baseline và chỉ số đánh giá.

Chấm `code/danh_gia.py` (mặc định) hoặc `dap-an/danh_gia.py` khi BAI=dap-an.
Buổi này học viên TỰ VIẾT bộ chỉ số, nên bộ chấm kiểm cả quy ước lẫn kết luận rút ra từ số.
"""
from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture(scope="module")
def dg(nap, du_lieu):
    return nap("danh_gia")


@pytest.fixture(scope="module")
def m4(dg):
    chuoi = dg.lay_mau(dg.doc_tsf(), 300)
    hoc, kiem = dg.chia(chuoi)
    return hoc, kiem


def test_du_bon_baseline(dg):
    """seasonal naive là baseline BẮT BUỘC của cả khoá — thiếu nó thì mọi so sánh sau vô nghĩa."""
    assert len(dg.BASELINE) >= 4, f"mới có {sorted(dg.BASELINE)}"
    ten = " ".join(dg.BASELINE).lower()
    assert "seasonal" in ten or "mùa vụ" in ten, f"thiếu seasonal naive: {sorted(dg.BASELINE)}"


def test_seasonal_naive_lap_dung_chu_ky(dg):
    y = np.arange(1.0, 29.0)  # 28 điểm, m = 7 → bảy giá trị cuối là 22..28
    d = dg.bl_naive_mua_vu(y, tam=9, m=7)
    assert np.allclose(d[:7], np.arange(22.0, 29.0))
    assert np.allclose(d[7:], np.arange(22.0, 24.0)), "phải quay vòng lại đầu chu kỳ"


def test_naive_va_drift(dg):
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    assert np.allclose(dg.bl_naive(y, 3), 5.0)
    assert np.allclose(dg.bl_drift(y, 3), [6.0, 7.0, 8.0]), "drift = nối điểm đầu với điểm cuối"


def test_mau_so_scaled_lay_tu_phan_hoc(dg):
    """MASE/RMSSE chuẩn hoá bằng sai số naive mùa vụ TRONG MẪU HỌC (Hyndman & Koehler 2006).

    Lấy mẫu số từ chính đoạn đang chấm vừa sai định nghĩa, vừa là rò rỉ: sai số được chuẩn hoá
    bằng thông tin của tương lai.
    """
    hoc = np.array([0.0, 1.0] * 20)              # naive-1 trong mẫu: lệch 1,0 mỗi bước
    kiem = np.array([0.0, 10.0, 0.0, 10.0])      # đoạn kiểm biến động gấp 10
    du_bao = np.zeros(4)
    giatri = dg.mase(kiem, du_bao, hoc, m=1)
    assert giatri == pytest.approx(5.0, rel=1e-6), (
        f"MASE phải là MAE/({'MAE naive trên phần học'}) = 5,0; đang ra {giatri:.3f} "
        "— nhiều khả năng mẫu số đang tính trên phần kiểm")


def test_mase_khi_chuoi_tuan_hoan_hoan_hao(dg):
    """Chuỗi tuần hoàn hoàn hảo: seasonal naive dự báo đúng tuyệt đối (MAE = 0), và MASE
    KHÔNG tính được vì mẫu số cũng bằng 0 — phải trả NaN chứ không được trả 0 hay ném lỗi."""
    y = np.tile([1.0, 5.0, 3.0, 9.0, 2.0, 7.0, 4.0], 20)
    hoc, kiem = y[:-14], y[-14:]
    d = dg.bl_naive_mua_vu(hoc, 14, 7)
    assert dg.mae(kiem, d) == pytest.approx(0.0, abs=1e-9)
    assert np.isnan(dg.mase(kiem, d, hoc, 7)), "mẫu số bằng 0 → MASE phải là NaN"


def test_mase_bang_1_khi_du_bao_ngang_snaive(dg):
    """Chuỗi mùa vụ có nhiễu: MASE của một dự báo sai đúng bằng mức naive mùa vụ phải ≈ 1."""
    rng = np.random.default_rng(0)
    m = 7
    nen = np.tile([10.0, 12.0, 9.0, 14.0, 11.0, 13.0, 8.0], 30)
    y = nen + rng.normal(0, 1.0, nen.size)
    hoc, kiem = y[:-14], y[-14:]
    mau_so = np.mean(np.abs(hoc[m:] - hoc[:-m]))
    du_bao = kiem + mau_so  # lệch đúng bằng mẫu số → MASE = 1
    assert dg.mase(kiem, du_bao, hoc, m) == pytest.approx(1.0, rel=1e-9)


def test_quy_uoc_mape_smape(dg):
    """MAPE ×100 và VÔ HẠN khi y = 0; sMAPE ×200 và bị chặn ở 200."""
    y = np.array([100.0, 100.0])
    d = np.array([110.0, 90.0])
    assert dg.mape(y, d) == pytest.approx(10.0), "MAPE phải theo phần trăm (×100)"
    assert dg.smape(y, d) == pytest.approx(200 * np.mean([10 / 210, 10 / 190]), rel=1e-6), (
        "sMAPE phải theo quy ước M4 (×200)")
    assert not np.isfinite(dg.mape(np.array([0.0, 1.0]), np.array([1.0, 1.0]))), (
        "MAPE phải là vô hạn khi có y = 0 — đừng âm thầm bỏ qua")
    assert dg.smape(np.array([1.0]), np.array([-1.0])) == pytest.approx(200.0)


def test_mape_phat_lech_khong_deu(dg):
    """MAPE phạt dự báo CAO nặng hơn dự báo THẤP cùng biên độ — đó là lý do nó kéo dự báo xuống."""
    y = np.array([100.0])
    assert dg.mape(y, np.array([150.0])) == pytest.approx(50.0)
    assert dg.mape(y, np.array([50.0])) == pytest.approx(50.0)
    # nhưng trên thang nhân: dự báo gấp đôi bị phạt 100%, dự báo bằng một nửa cũng 50%
    assert dg.mape(y, np.array([200.0])) > dg.mape(y, np.array([0.0001]))


def test_bao_cao_so_gia_tri_vo_han(dg):
    """Chuỗi có số 0 làm MAPE vô hạn. Bảng kết quả PHẢI nói ra điều đó, không được im lặng bỏ."""
    y = {"a": np.zeros(14), "b": np.ones(14)}
    hoc = {"a": np.r_[np.zeros(30), np.ones(10)], "b": np.ones(40)}
    du_bao = {"naive": {"a": np.ones(14), "b": np.ones(14)}}
    bang = dg.danh_gia(y, du_bao, hoc, m=7)
    cot_vo_han = [c for c in bang.columns if "vô hạn" in c or "vo_han" in c]
    assert cot_vo_han, f"bảng phải có cột đếm giá trị không tính được, đang có {list(bang.columns)}"
    assert int(bang[cot_vo_han].to_numpy().sum()) > 0


def test_doi_chi_so_doi_xep_hang(dg):
    """Lab 3: trên dữ liệu bán lẻ có nhiều số 0, mô hình 'tốt nhất' ĐỔI theo chỉ số."""
    ban_le = dg.chuoi_ban_le(so_ma=120)
    hoc, kiem = dg.chia(ban_le)
    bang = dg.danh_gia(kiem, dg.du_bao_baseline(hoc), hoc)
    hang = dg.xep_hang(bang)
    tot_nhat = {cot: hang.loc[hang[cot] == 1, "mô hình"].tolist()
                for cot in ("MAE", "sMAPE", "MASE", "RMSSE") if cot in hang}
    khac = {tuple(sorted(v)) for v in tot_nhat.values() if v}
    assert len(khac) > 1, f"đổi chỉ số mà hạng nhất không đổi thì bài học biến mất: {tot_nhat}"


def test_khop_utilsforecast(dg, m4):
    """MAE/RMSE/MASE/RMSSE phải khớp thư viện chuẩn; MAPE và sMAPE khác ĐÚNG một hằng số quy ước."""
    hoc, kiem = m4
    du_bao = {t: dg.bl_naive_mua_vu(v, dg.TAM, dg.M) for t, v in hoc.items()}
    bang = dg.so_voi_utilsforecast(kiem, du_bao, hoc).set_index("chỉ số")
    for k in ("MAE", "RMSE", "MASE", "RMSSE"):
        assert bang.loc[k, "tỷ lệ tự viết / thư viện"] == pytest.approx(1.0, rel=1e-6), (
            f"{k} lệch thư viện: {bang.loc[k].to_dict()}")
    assert bang.loc["MAPE", "tỷ lệ tự viết / thư viện"] == pytest.approx(100.0, rel=1e-6)
    assert bang.loc["sMAPE", "tỷ lệ tự viết / thư viện"] == pytest.approx(200.0, rel=1e-6)


def test_chan_doan_phan_du_baseline(dg, m4):
    """Phần dư của seasonal naive vi phạm gần hết giả định — nên đừng tin khoảng dự báo của nó."""
    hoc, _ = m4
    bang = dg.chan_doan_phan_du({t: hoc[t] for t in list(hoc)[:150]})
    tom = dg.tom_tat_chan_doan(bang)
    assert tom["% còn tự tương quan (Ljung–Box p < 0,05)"] > 80
    assert tom["% phần dư không chuẩn (Jarque–Bera p < 0,05)"] > 50


def test_chi_so_quyet_dinh_du_bao(dg):
    """MAE → trung vị, RMSE → trung bình, MAPE → thấp hơn cả trung vị (trên phân phối lệch phải)."""
    kq = dg.toi_uu_theo_chi_so(dg.mau_lech_phai())
    assert kq["hằng số tối ưu MAE"] == pytest.approx(kq["trung vị mẫu"], rel=0.02)
    assert kq["hằng số tối ưu RMSE"] == pytest.approx(kq["trung bình mẫu"], rel=0.02)
    assert kq["hằng số tối ưu MAPE"] < kq["trung vị mẫu"] * 0.8, (
        "MAPE kéo dự báo xuống dưới trung vị — đó là lý do đừng tối ưu MAPE nếu nghiệp vụ không muốn vậy")
