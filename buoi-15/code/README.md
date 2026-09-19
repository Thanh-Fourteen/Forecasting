# code/ — điểm xuất phát của buổi 15

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Buổi này `tv` **không có** `backtest`: bộ backtest là thứ bạn tự
viết, và từ buổi 16 cả khoá dùng bộ cùng giao diện.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `backtest.py` | đọc tải điện ERCOT 2024 và M4 theo giờ; feature ngày tới; `chia_cua_so`, `backtest`; ba cách ước lượng sai số; chọn phương pháp theo chuỗi; Diebold–Mariano | sửa `uoc_luong_sai_so`, `chon_va_bao_cao`, `diebold_mariano` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Cột "rolling origin" của bảng ước lượng hứa sai số thấp như K-fold xáo trộn.
- Chọn phương pháp theo chuỗi báo MASE đẹp hơn hẳn seasonal naive.
- Một mô hình hơn seasonal naive 4% được kiểm định là "chắc chắn tốt hơn" (p gần 0).

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~90 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/9 hỏng), cuối buổi phải XANH 9/9
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
