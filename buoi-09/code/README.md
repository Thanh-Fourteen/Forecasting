# code/ — điểm xuất phát của buổi 9

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một tương quan bằng 0 chưa chắc nghĩa là "không liên quan".

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `dac_trung.py` | đọc 48.000 chuỗi M4 và doanh số bán lẻ; 20 đặc trưng; spectral entropy; sai số của seasonal naive; bản đồ PCA; phân cụm DTW; ABC–XYZ | sửa `tuong_quan_kho_de`, `de_xuat_chien_luoc`, `phan_cum_dtw` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Bảng tương quan kết luận spectral entropy **không** liên quan tới độ khó dự báo ($r$ = −0,05).
- Kế hoạch tune mô hình cho **cả 4.000 chuỗi**, kể cả chuỗi gần như nhiễu.
- Bốn cụm DTW chỉ khác nhau ở độ lớn, không khác nhau ở hình dạng.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (M4, Online Retail II), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (4/10 hỏng), cuối buổi phải XANH 10/10
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
