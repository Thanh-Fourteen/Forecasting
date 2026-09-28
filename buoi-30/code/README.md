# code/ — điểm xuất phát của buổi 30

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `kien_truc.py` | đọc nhu cầu điện 5 vùng + nhiệt độ; khai covariate; tạo 5 kiến trúc neuralforecast; dự báo 37 mốc; seasonal naive, EIA, MSTL, LightGBM; bảng MASE; đọc N-BEATS, TFT, coverage DeepAR | sửa `FUTR_EXOG` và `HIST_EXOG` (tài liệu mục 5, bước 2) |
| `lab.ipynb` | notebook của Lab, bước 1–7 (khoảng 10 phút) | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng): backtest đẹp hơn mức mô hình làm được lúc vận hành, khi chỉ có nhiệt độ dự báo.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường (~1,6 GB) + dữ liệu, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (2/5 hỏng), cuối buổi phải XANH 5/5
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
