# code/ — điểm xuất phát của buổi 2

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin tỷ lệ phủ đẹp.

| Tệp | Làm gì |
|---|---|
| `xac_suat.py` | quantile tự viết, khoảng dự báo, tỷ lệ phủ, bootstrap khoảng tin cậy cho trung bình, mô phỏng AR(1), đọc lượt thuê xe theo giờ |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- khoảng dự báo cho dữ liệu đếm có cận dưới âm; một đuôi gần như không bao giờ bị vượt
- khoảng tin cậy "95%" cho trung bình của chuỗi AR(1) chỉ chứa trung bình thật khoảng 60% số lần

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu Bike Sharing
make check                 # bộ chấm: đầu buổi ĐỎ (5/8 hỏng), cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/xac_suat.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
