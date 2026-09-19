# code/ — điểm xuất phát của buổi 20

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `da_bien.py` | đọc giá dầu, xăng (EIA) và số liệu vintage (Philadelphia Fed); kiểm dừng, cointegration, VAR/VECM; Kalman local level; nowcast GDP bằng bridge và DFM | sửa `hang_dong_lien_ket`, `nowcast` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Dự báo giá xăng luôn dùng VAR trên sai phân.
- Nowcast GDP ở tháng đầu quý chính xác y như ở tháng cuối quý.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~8 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/6 hỏng), cuối buổi phải XANH 6/6
```

Tệp của Philadelphia Fed được thêm một cột mỗi tháng, nên `lab.py up` có thể báo sha256 khác bản chốt: bình thường, code chỉ dùng số liệu
tới 12/2025. Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
