# code/ — điểm xuất phát của buổi 2

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin các con số "95%" đẹp mà nó in ra.

| Tệp | Làm gì |
|---|---|
| `xac_suat.py` | quantile tự viết, khoảng dự báo, tỷ lệ phủ (tách hai đuôi), khoảng tin cậy bootstrap cho trung bình, mô phỏng chuỗi AR(1), đọc lượt thuê xe theo giờ |

**Triệu chứng bạn sẽ thấy** (chưa nói nguyên nhân — tự tìm bằng mục 4.3 và 4.6 của tài liệu):

- Khoảng dự báo "95%" cho số lượt thuê (luôn ≥ 0) có **cận dưới âm**. Số giờ rơi dưới cận dưới gần 0%, trong khi mục tiêu
  là 2,5%.
- Khoảng tin cậy "95%" cho trung bình của chuỗi AR(1) mô phỏng chỉ chứa trung bình thật khoảng **60%** số lần, chứ không
  phải 95%.

**Bạn cần làm:**

1. Chạy code, ghi lại hai con số trên (Bước 1 của Lab).
2. Sửa `khoang_du_bao` để khoảng giữ đúng hình dạng dữ liệu lệch phải (Bước 4). Không đổi tên hàm, không đổi tham số.
3. Sửa `khoang_tin_cay_trung_binh` để mặc định dùng được cho dữ liệu tự tương quan (Bước 5).
4. Chạy `make check` tới khi xanh 8/8.

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu Bike Sharing (kiểm sha256)
make check                 # bộ chấm: đầu buổi ĐỎ (5/8 hỏng), cuối buổi phải XANH 8/8
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/xac_suat.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook. Mỗi tệp chỉ định nghĩa hàm ở
mức module; phần chạy thử đặt trong `if __name__ == "__main__":`, để bộ chấm nạp nhanh.
