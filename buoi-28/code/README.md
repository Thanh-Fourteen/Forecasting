# code/ — điểm xuất phát của buổi 28

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `phan_cap.py` | đọc du lịch Úc; cây 389 chuỗi và ma trận S; AutoETS + hoà giải (bottom-up, top-down, OLS, MinT); backtest theo cấp; khoảng khớp từ sai số ngoài mẫu; phân cấp theo thời gian | sửa `PHUONG_PHAP` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–7 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng): dự báo cả nước khác tổng các dự báo cấp đáy hàng triệu chuyến mỗi quý.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (1/6 hỏng), cuối buổi phải XANH 6/6
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
