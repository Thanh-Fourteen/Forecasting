# code/ — điểm xuất phát của buổi 26

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin một con số coverage duy nhất.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `conformal.py` | đọc PM2.5 trạm Dongsi; LightGBM giờ tới; split conformal, CQR, ACI, EnbPI; khoảng đem dùng; MAPIE; coverage trượt | sửa `aci` và `PHUONG_PHAP` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–7 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng):

- Khoảng đem dùng phủ khoảng 91% trên hai năm, nhưng có tháng chỉ phủ khoảng 75%.
- ACI cho khoảng vô hạn gần như mọi giờ.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (8 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/7 hỏng), cuối buổi phải XANH 7/7
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
