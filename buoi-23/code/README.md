# code/ — điểm xuất phát của buổi 23

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `boosting.py` | đọc Online Retail II thành số món bán mỗi ngày của 500 mã; đặc trưng (mọi lag ≥ 28 ngày); LightGBM; backtest 3 cutoff; WRMSSE; AutoETS và seasonal naive; tune bằng Optuna; SHAP; partial dependence; ràng buộc đơn điệu | sửa `THAM_SO`, `chia_cv` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–6 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- LightGBM thua cả "trung bình 28 ngày gần nhất" trên WRMSSE, và có dự báo âm.
- Tune bằng Optuna xong vẫn không thắng AutoETS.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (46 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb; ô bước 1 lần đầu 1–2 phút, ô bước 3 lần đầu 3–10 phút
python lab.py check        # bộ chấm: đầu buổi ĐỎ (2/7 hỏng), cuối buổi phải XANH 7/7
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
