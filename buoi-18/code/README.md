# code/ — điểm xuất phát của buổi 18

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `hoi_quy.py` | đọc dữ liệu; hồi quy thường và hồi quy động; mô phỏng hồi quy giả; Fourier, nhiệt độ, lễ; backtest bốn cách đa mùa vụ trên tải ERCOT; Prophet trên lượt xem Wikipedia | sửa `he_so_ip`, `KHAI_TET` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Hành khách hàng không EU "phụ thuộc" sản lượng công nghiệp Mỹ với p = 3·10⁻¹⁶.
- Prophet đoán lượt xem Wikipedia quá cao cả tuần Tết.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~90 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb; ô bước 4 lần đầu chạy khoảng 7 phút
python lab.py check        # bộ chấm: đầu buổi ĐỎ (2/5 hỏng), cuối buổi phải XANH 5/5
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
