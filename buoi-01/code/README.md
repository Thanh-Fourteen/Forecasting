# code/ — điểm xuất phát của buổi 1

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin kết quả đẹp.

| Tệp | Làm gì |
|---|---|
| `kiem_tra_moi_truong.py` | in phiên bản Python, thư viện và kiểm tệp dữ liệu |
| `danh_gia.py` | đọc điện tiêu thụ theo giờ (kWh), "mô hình" bảng lịch, bốn hàm baseline, dự báo cuốn theo tuần, bảng MAE |
| `phieu-bai-toan.md` | mẫu phiếu bài toán dự báo 6 ô — điền cho 3 tình huống của lab (bước 3) |

**Đang cố tình sai** (triệu chứng nhìn thấy): `danh_gia()` báo MAE 0,380 kWh/giờ cho năm 2010. Con số rất đẹp, và
bảng chỉ có đúng một dòng, nên không có gì để so.

**Bạn cần làm** (tài liệu mục 5, bước 5):

1. Đọc `du_bao_cuon` và tìm xem bảng lịch được khớp trên dữ liệu nào. So với mục 4.4 "Sai số ảo và dự báo cuốn".
2. Sửa để tại mỗi gốc (00:00 thứ Hai), mọi dự báo chỉ dùng dữ liệu **trước** gốc.
3. Thêm bốn cột baseline ("trung bình 4 tuần", "tuần trước", "trung bình", "giờ trước") bằng các hàm có sẵn trong tệp
   (mục 4.3). Đúng tên cột như vậy, vì bộ chấm tìm theo tên.
4. Chạy `make check` cho tới khi xanh cả 8 test.

Xong thì bảng lịch không còn 0,380 mà khoảng 0,5 kWh/giờ, và có ít nhất một baseline tốt hơn nó.

Chạy (trong `lab/`):

```bash
make up                    # một lần: môi trường + dữ liệu (~20 MB tải, 133 MB giải nén), kiểm sha256
make check                 # bộ chấm: đầu buổi ĐỎ (4 trên 8 test hỏng), cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/danh_gia.py
```

Python in số thập phân bằng dấu chấm: `0.38` là 0,38. Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như
script, mở được như notebook. Phần chạy thử đặt trong `if __name__ == "__main__":` để bộ chấm nạp tệp nhanh.
