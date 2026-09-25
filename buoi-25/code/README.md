# code/ — điểm xuất phát của buổi 25

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Buổi này `tv` **không có** `danh_gia`: pinball, CRPS, WIS là thứ bạn tự viết.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `xac_suat.py` | đọc nhu cầu điện ERCOT + nhiệt độ; đặc trưng; backtest học lại mỗi tháng (dự báo điểm + 9 quantile); khoảng từ phần dư; pinball, CRPS, WIS; PIT; peaks-over-threshold | sửa `quantile_tu_phan_du`, `sua_crossing`, `crps_mau` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–6 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng):

- Khoảng 90% chỉ phủ khoảng 78% số giờ năm 2025.
- Vẫn còn giờ có quantile mức cao nhỏ hơn quantile mức thấp.
- CRPS tự viết lệch `scoringrules` gần gấp đôi.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~180 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/9 hỏng), cuối buổi phải XANH 9/9
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
