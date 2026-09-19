# code/ — điểm xuất phát của buổi 6

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một phân rã "gọn gàng" chưa chắc đã tách đúng.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `phan_ra.py` | đọc nhu cầu điện PJM theo giờ, lấp giờ trống, phân rã, độ mạnh $F_T$/$F_S$, đo mẫu hình còn trong phần dư | sửa `phan_ra` (tài liệu mục 5, bước 3) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Độ mạnh mùa vụ chỉ 0,618 cho một chuỗi điện rõ ràng rất mùa vụ, và không có thành phần mùa vụ tuần.
- 12 giờ đầu và 12 giờ cuối năm không có xu hướng.
- Bật `robust=True` cũng không đổi gì.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu EIA-930 (~90 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (5/7 hỏng), cuối buổi phải XANH 7/7
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
