# code/ — điểm xuất phát của buổi 10

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Dữ liệu "sạch" mà không truy vết được thì không dùng được.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `lam_sach.py` | đọc trạm Nội Bài (GHCNh 2024), PM2.5 12 trạm Bắc Kinh, Open-Meteo Hà Nội; thống kê thiếu; kiểm chất lượng; 7 cách điền; che nhân tạo; pipeline làm sạch | sửa `doc_noi_bai`, `so_sanh_dien`, `lam_sach` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Báo cáo chất lượng ghi độ ẩm `min = 100, max = 94`, và "trá hình 0%" cho mọi cột.
- Bảng so sánh kết luận **nội suy tuyến tính luôn tốt nhất**.
- Sau khi làm sạch, "còn thiếu: 0", kể cả những lỗ dài nhiều giờ.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (GHCNh, Bắc Kinh, Open-Meteo), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (5/12 hỏng), cuối buổi phải XANH 12/12
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
