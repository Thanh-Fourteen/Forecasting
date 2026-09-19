# code/ — điểm xuất phát của buổi 19

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `gian_doan.py` | đọc Car Parts; phân loại ADI × CV²; Croston, SBA, TSB tự viết; backtest 10 mô hình; chỉ số; mô phỏng tồn kho | sửa `tsb`, `danh_gia`, `chon_mo_hinh` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Mô hình được chọn để nhập hàng là "Zero": không bao giờ nhập món nào.
- `tsb` tự viết không khớp statsforecast.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~40 KB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb; ô bước 3 lần đầu chạy khoảng 15 giây
python lab.py check        # bộ chấm: đầu buổi ĐỎ (4/8 hỏng), cuối buổi phải XANH 8/8
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
