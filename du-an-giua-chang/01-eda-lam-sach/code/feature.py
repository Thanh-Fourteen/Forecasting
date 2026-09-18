# %% [markdown]
# # Dự án giữa chặng 1 — khung `feature.py` để bạn điền
#
# Bài toán: dự báo **nhiệt độ Nội Bài 24 giờ tới**. Mọi feature phải có sẵn tại thời điểm ra dự báo.

# %%
from __future__ import annotations

import numpy as np  # noqa: F401  (khung rỗng — bạn sẽ dùng)
import pandas as pd

TAM = 24  # tầm dự báo (bước 30 phút của Nội Bài → 24 bước = 12 giờ; đổi cho đúng bài toán của bạn)


def bo_feature(y: pd.Series, tam: int = TAM) -> pd.DataFrame:
    """≥ 20 feature cho chuỗi `y`. Nhắc lại hai quy tắc của buổi 13:
    lag nhỏ nhất ≥ tầm dự báo, và `shift(tam)` TRƯỚC khi `rolling`.
    """
    raise NotImplementedError("phần của bạn")


def bang_biet_truoc(f: pd.DataFrame) -> pd.DataFrame:
    """Một dòng mỗi feature, cột `feature` và cột `biết trước`
    ('vô hạn' | 't-h' | 'kế hoạch'). Không feature nào được rơi vào 'KHÔNG BIẾT TRƯỚC'.
    """
    raise NotImplementedError("phần của bạn")


def kiem_ro_ri(ham_feature, y: pd.Series, cac_moc=None) -> pd.DataFrame:
    """Bài kiểm cắt tương lai của chính bạn (buổi 13). Nhớ: so MỌI dòng ≤ mốc cắt,
    NaN so với số cũng là khác nhau, và chọn mốc cắt có chủ đích.
    """
    raise NotImplementedError("phần của bạn")


def baseline_seasonal_naive(y: pd.Series, tam: int = TAM, chu_ky: int = 48) -> pd.Series:
    """Baseline bắt buộc để đối chiếu."""
    raise NotImplementedError("phần của bạn")


# %%
if __name__ == "__main__":
    print("Điền các hàm ở trên rồi chạy: cd lab && make check")
