# code/ — điểm xuất phát của buổi 21

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `tai_chinh.py` | đọc BTC theo giờ (Binance) và JPY/USD (Fed H.10); lợi suất, sự thật cách điệu; demo đoán giá bằng mạng nơ-ron; GARCH, HAR, QLIKE; VaR 99%, Kupiec; Markov switching | sửa `du_bao_gia`, `danh_gia_gia`, `var_99` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Mô hình đoán giá BTC "chính xác 99%" (R² 0,988).
- VaR 99% bị vượt khoảng 25 lần trong 1.249 ngày.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + 25 tệp dữ liệu (~3 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/7 hỏng), cuối buổi phải XANH 7/7
```

Dữ liệu Binance không có giấy phép dữ liệu: `lab.py up` tải thẳng từ data.binance.vision về máy bạn; không chia sẻ lại. Bạn sửa **tệp `.py`**;
notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
