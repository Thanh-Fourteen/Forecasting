# code/ — điểm xuất phát của buổi 16

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `ets.py` | đọc Tourism và hành khách EU; SES, Holt tự viết; Holt–Winters; Theta; backtest 366 chuỗi so seasonal naive, kiểm định, tỷ lệ phủ | sửa `ses_loc`, mặc định của `holt_winters` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- SES tối ưu ra α = 1 và sai số khớp bằng 0.
- Dự báo hành khách hàng không hụt các đỉnh hè.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~0,5 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (4/8 hỏng), cuối buổi phải XANH 8/8
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
