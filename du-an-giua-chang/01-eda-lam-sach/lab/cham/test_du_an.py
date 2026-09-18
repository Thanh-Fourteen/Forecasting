"""Bộ chấm TỐI THIỂU của dự án giữa chặng 1 (10/100 điểm phần C).

Chấm `code/lam_sach.py` và `code/feature.py` của học viên. Đây chỉ là mức sàn: test riêng của
học viên mới là phần cho điểm chất lượng. Bộ chấm này KHÔNG biết 6 lỗi cài sẵn là gì — nó chỉ
kiểm các tính chất mà một pipeline làm sạch tử tế nào cũng phải có.

Dữ liệu bẩn đọc từ thư mục `phat/du-lieu/` (giảng viên gửi kèm); nếu chưa có thì test tự bỏ qua.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

DU_AN = Path(__file__).resolve().parent.parent.parent
PHAT = DU_AN / "phat" / "du-lieu"


@pytest.fixture(scope="module")
def ls(nap):
    return nap("lam_sach")


@pytest.fixture(scope="module")
def ft(nap):
    return nap("feature")


@pytest.fixture(scope="module")
def ban() -> dict[str, pd.DataFrame]:
    if not PHAT.is_dir():
        pytest.skip(f"chưa có dữ liệu phát ở {PHAT} — hỏi giảng viên")
    ra = {}
    for ten in ("noi-bai", "ha-noi", "tphcm"):
        tep = PHAT / f"{ten}.csv"
        if not tep.is_file():
            pytest.skip(f"thiếu {tep.name}")
        ra[ten] = pd.read_csv(tep, parse_dates=["thoi_gian"])
    return ra


@pytest.fixture(scope="module")
def sach(ls, ban) -> dict[str, pd.DataFrame]:
    return {ten: ls.lam_sach(bang, ten) for ten, bang in ban.items()}


def test_doc_duoc_ba_nguon(ban):
    assert set(ban) == {"noi-bai", "ha-noi", "tphcm"}
    for ten, bang in ban.items():
        assert len(bang) > 10_000, f"{ten} chỉ có {len(bang)} dòng"


def test_luoi_thoi_gian_deu_va_khong_trung(sach):
    """Sau khi làm sạch: chỉ số là thời gian, tăng dần, không mốc trùng, bước đều."""
    for ten, bang in sach.items():
        assert isinstance(bang.index, pd.DatetimeIndex), f"{ten}: chỉ số phải là DatetimeIndex"
        assert bang.index.is_monotonic_increasing, f"{ten}: chỉ số chưa sắp xếp"
        assert not bang.index.has_duplicates, f"{ten}: còn mốc thời gian trùng"
        buoc = pd.Series(bang.index).diff().dropna().value_counts()
        assert buoc.iloc[0] / len(bang) > 0.99, f"{ten}: lưới thời gian chưa đều ({buoc.head(3).to_dict()})"


def test_co_cot_co_truy_vet(sach):
    """Mọi can thiệp phải để lại dấu vết."""
    for ten, bang in sach.items():
        thieu = {"da_dien", "nghi_ngo", "lo_dai_bo_trong"} - set(bang.columns)
        assert not thieu, f"{ten}: thiếu cột cờ {sorted(thieu)}"
        assert bang["da_dien"].dropna().isin([0, 1]).all(), f"{ten}: cờ da_dien phải là 0/1"


def test_khong_dien_lo_dai(sach):
    """Lỗ dài phải để trống có chủ ý, không lấp bằng nội suy."""
    co_lo_dai = False
    for ten, bang in sach.items():
        if bang["lo_dai_bo_trong"].sum() > 0:
            co_lo_dai = True
            cot_so = [c for c in bang.columns if pd.api.types.is_numeric_dtype(bang[c])
                      and c not in ("da_dien", "nghi_ngo", "lo_dai_bo_trong")]
            assert bang.loc[bang["lo_dai_bo_trong"], cot_so].isna().all().all(), (
                f"{ten}: ô trong lỗ dài vẫn có giá trị — đó là dữ liệu bịa")
    assert co_lo_dai, "không nguồn nào còn lỗ dài: nhiều khả năng bạn đã điền tất cả"


def test_khong_mat_moc_thoi_gian(ban, sach):
    """Làm sạch không được XOÁ mốc (xoá dòng làm thủng lịch thời gian)."""
    for ten, bang in sach.items():
        goc = ban[ten]["thoi_gian"]
        assert bang.index.min() <= goc.min() and bang.index.max() >= goc.max(), (
            f"{ten}: khoảng thời gian bị cắt ngắn sau khi làm sạch")


def test_danh_gia_cach_dien_hai_kieu_che(ls, sach):
    """Phải so các cách điền trên CẢ che điểm lẫn che khối (buổi 10)."""
    y = next(iter(sach.values()))
    cot = [c for c in y.columns if pd.api.types.is_numeric_dtype(y[c])
           and c not in ("da_dien", "nghi_ngo", "lo_dai_bo_trong")][0]
    bang = ls.so_sanh_dien(y[cot].dropna().iloc[:5000])
    assert {"kiểu che", "cách điền", "MAE"} <= set(bang.columns)
    assert bang["kiểu che"].nunique() >= 2, "mới đánh giá trên một kiểu che"
    assert bang["cách điền"].nunique() >= 4, "cần so ít nhất 4 cách điền"


def test_bo_feature_khong_ro_ri(ft, sach):
    """Bài kiểm cắt tương lai — bộ chấm tự cắt, không dùng hàm của học viên."""
    y = next(iter(sach.values()))
    cot = [c for c in y.columns if pd.api.types.is_numeric_dtype(y[c])
           and c not in ("da_dien", "nghi_ngo", "lo_dai_bo_trong")][0]
    chuoi = y[cot].ffill().dropna().iloc[:3000]
    day_du = ft.bo_feature(chuoi)
    assert day_du.shape[1] >= 20, f"cần ít nhất 20 feature, đang có {day_du.shape[1]}"
    xau = set()
    for p in (0.5, 0.8):
        moc = chuoi.index[int(len(chuoi) * p)]
        cat = ft.bo_feature(chuoi[chuoi.index <= moc])
        chung = day_du.index[day_du.index <= moc]
        for c in day_du.columns:
            a = day_du.loc[chung, c].to_numpy(dtype=float)
            b = (cat.reindex(chung)[c].to_numpy(dtype=float) if c in cat.columns
                 else np.full(len(chung), np.nan))
            if not np.allclose(a, b, rtol=0, atol=1e-9, equal_nan=True):
                xau.add(c)
    assert not xau, f"feature rò rỉ: {sorted(xau)}"


def test_bang_biet_truoc(ft, sach):
    """Mỗi feature phải khai 'biết trước bao lâu'."""
    y = next(iter(sach.values()))
    cot = [c for c in y.columns if pd.api.types.is_numeric_dtype(y[c])
           and c not in ("da_dien", "nghi_ngo", "lo_dai_bo_trong")][0]
    f = ft.bo_feature(y[cot].ffill().dropna().iloc[:2000])
    bang = ft.bang_biet_truoc(f)
    assert len(bang) == f.shape[1], "bảng phải có đúng một dòng cho mỗi feature"
    assert "biết trước" in bang.columns
    assert not bang["biết trước"].isna().any()
