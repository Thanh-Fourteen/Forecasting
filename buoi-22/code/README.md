# code/ — điểm xuất phát của buổi 22

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `hoi_quy.py` | đọc 10.000 trang Web Traffic; bảng lag; recursive tự viết; đặc trưng global; ba chiến lược đa bước; cây trên chuỗi có xu hướng; backtest LightGBM global và AutoETS local; RMSSE | sửa `dac_trung`, `du_bao_cay` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Chiến lược direct thắng recursive rất xa ở tuần thứ hai.
- Cây quyết định dự báo đứng ngang trên chuỗi đang tăng.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (145 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb; ô bước 4 lần đầu 5–15 phút
python lab.py check        # bộ chấm: đầu buổi ĐỎ (4/10 hỏng), cuối buổi phải XANH 10/10
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
