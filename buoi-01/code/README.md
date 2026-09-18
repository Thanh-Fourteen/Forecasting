# code/ — điểm xuất phát của buổi 1

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin kết quả đẹp.

| Tệp | Làm gì |
|---|---|
| `kiem_tra_moi_truong.py` | in phiên bản Python/thư viện và kiểm tệp dữ liệu |
| `danh_gia.py` | đọc điện tiêu thụ theo giờ, "mô hình" bảng lịch, các hàm baseline, dự báo cuốn theo tuần, bảng MAE |
| `phieu-bai-toan.md` | mẫu phiếu bài toán dự báo 6 ô — điền cho 3 tình huống của lab |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- `danh_gia()` báo MAE 0,380 kWh/giờ cho năm 2010 — rất đẹp, và bảng chỉ có đúng một dòng

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu (~20 MB tải, 133 MB giải nén)
make check                 # bộ chấm: đầu buổi ĐỎ (4/8 hỏng), cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/danh_gia.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
