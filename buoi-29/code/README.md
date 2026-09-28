# code/ — điểm xuất phát của buổi 29

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `hoc_sau.py` | đọc 50 khách hàng; cắt cửa sổ; scaler, RevIN; MLP, LSTM, TCN; vòng huấn luyện có dừng sớm; seasonal naive, MSTL, LightGBM; bảng MASE | sửa `hoc_scaler` và `chia_train_val` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–7 (khoảng 10–15 phút) | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng): trên tập nhỏ 5 khách hàng, điểm val nói mạng thắng seasonal naive, còn test thật nói ngược lại.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (2/6 hỏng), cuối buổi phải XANH 6/6
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`. Máy 8 GB RAM: đặt `SO_KHACH = 20` ở ô bước 1.
