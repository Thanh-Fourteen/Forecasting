# code/ — điểm xuất phát của buổi 17

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `arima.py` | đọc sản lượng công nghiệp (G.17) và Tourism; mô phỏng AR/MA; ACF, PACF; ARIMA, auto-ARIMA, Ljung–Box; backtest so AutoETS và seasonal naive | sửa `MUA_VU_ARIMA`, `kiem_phan_du`, mặc định của `mo_hinh_tu_chon` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- auto-ARIMA trên chuỗi du lịch theo tháng thua cả seasonal naive.
- Mọi mô hình đều được báo "phần dư ổn".

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~0,5 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb; ô bước 5 lần đầu chạy vài phút
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/6 hỏng), cuối buổi phải XANH 6/6
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
