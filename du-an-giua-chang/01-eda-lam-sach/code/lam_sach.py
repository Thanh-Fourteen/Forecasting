# %% [markdown]
# # Dự án giữa chặng 1 — khung `lam_sach.py` để bạn điền
#
# Đây là **khung rỗng**: chữ ký hàm đã cố định để `python lab.py check` chạy được, phần thân là việc của bạn.
# Mọi công cụ cần thiết đã học ở buổi 10–13; được phép chép lại code của chính mình từ các buổi đó.
#
# Thứ tự gợi ý tám bước (buổi 10–11):
#   1. đọc + ép kiểu   2. lưới thời gian đều, khử mốc trùng, thống nhất UTC   3. bỏ cột rỗng
#   4. cờ chất lượng của nguồn   5. giá trị trá hình / trần cảm biến   6. độ phân giải → ngưỡng đứng yên
#   7. đo lại phân bố độ dài lỗ → chọn giới hạn điền   8. xuất dữ liệu + cờ + báo cáo

# %%
from __future__ import annotations

import numpy as np  # noqa: F401  (khung rỗng — bạn sẽ dùng)
import pandas as pd

BUOC = {"noi-bai": "30min", "ha-noi": "1h", "tphcm": "1h"}


# %% [markdown]
# ## 1. Đọc và mô tả

# %%
def doc(tep) -> pd.DataFrame:
    """Đọc một tệp phát cho học viên. Nhớ: in `dtypes` và bảng min/max trước khi tin con số nào."""
    bang = pd.read_csv(tep, parse_dates=["thoi_gian"])
    return bang


def bao_cao_chat_luong(bang: pd.DataFrame) -> pd.DataFrame:
    """Bảng chất lượng dữ liệu: thiếu %, dải giá trị, độ phân giải, đoạn đứng yên, mốc trùng…

    Đây là thứ phát hiện phần lớn lỗi cài sẵn. Làm kỹ chỗ này rồi hãy đi tiếp.
    """
    raise NotImplementedError("phần của bạn")


# %% [markdown]
# ## 2. Làm sạch

# %%
def lam_sach(bang: pd.DataFrame, ten_nguon: str, gioi_han_dien: int = 6) -> pd.DataFrame:
    """Trả DataFrame có chỉ số thời gian đều + các cột số + ba cột cờ:
    `da_dien`, `nghi_ngo`, `lo_dai_bo_trong`.

    KHÔNG được xoá mốc thời gian. Lỗ dài hơn `gioi_han_dien` bước phải để NaN.
    """
    raise NotImplementedError("phần của bạn")


# %% [markdown]
# ## 3. Đánh giá cách điền bằng che nhân tạo

# %%
def che_diem(y: pd.Series, ty_le: float = 0.10, seed: int = 0) -> pd.Series:
    """Che ngẫu nhiên từng điểm."""
    raise NotImplementedError("phần của bạn")


def che_khoi(y: pd.Series, so_buoc: int = 48, so_khoi: int = 5, seed: int = 0) -> pd.Series:
    """Che nguyên khối (mô phỏng cảm biến chết vài ngày)."""
    raise NotImplementedError("phần của bạn")


def so_sanh_dien(y: pd.Series, seed: int = 0) -> pd.DataFrame:
    """Bảng dài: một dòng cho mỗi (kiểu che × cách điền), cột `kiểu che`, `cách điền`, `MAE`.

    Phải có ÍT NHẤT 2 kiểu che và 4 cách điền. Nhớ kết luận của buổi 10: phương pháp tốt nhất
    ĐỔI giữa lỗ ngắn và lỗ dài.
    """
    raise NotImplementedError("phần của bạn")


# %% [markdown]
# ## 4. So sánh chéo ba nguồn — chỗ duy nhất thấy được một trong sáu lỗi

# %%
def tuong_quan_truot(a: pd.Series, b: pd.Series, cua_so: str = "7D") -> pd.Series:
    """Tương quan trượt giữa hai nguồn. Một đoạn tụt hẳn là dấu hiệu lệch nhãn thời gian."""
    raise NotImplementedError("phần của bạn")


# %%
if __name__ == "__main__":
    print("Điền các hàm ở trên rồi chạy: cd lab && python lab.py check")
