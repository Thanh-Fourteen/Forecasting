# code/ — điểm xuất phát của buổi 10

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Dữ liệu "sạch" mà không truy vết được thì không dùng được.

| Tệp | Làm gì |
|---|---|
| `lam_sach.py` | đọc trạm Nội Bài (GHCNh 2024), PM2.5 12 trạm Bắc Kinh, Open-Meteo Hà Nội; thống kê thiếu; kiểm chất lượng; 7 cách điền; che nhân tạo; pipeline làm sạch |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- báo cáo chất lượng ghi độ ẩm `min = 100, max = 94`, và "trá hình 0%" cho mọi cột
- bảng so sánh kết luận **nội suy tuyến tính luôn tốt nhất**
- sau khi làm sạch, "còn thiếu: 0" — kể cả những lỗ dài nhiều giờ

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu (~40 MB)
make check                 # bộ chấm: đầu buổi ĐỎ (5/12 hỏng), cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/lam_sach.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
