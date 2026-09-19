# code/ — điểm xuất phát của buổi 7

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một kiểm định chạy xong chưa chắc đã đọc đúng.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `tu_tuong_quan.py` | đọc GDP, sản lượng công nghiệp, lượt thuê xe; sinh bốn chuỗi mô phỏng; ACF, Ljung-Box, kiểm định tính dừng, số lần sai phân | sửa `kiem_dinh`, `ket_luan`, `so_lan_sai_phan` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Chuỗi "xu hướng 0,05t" bị bảo "không dừng — cần sai phân".
- Nhiễu trắng cũng được sai phân một lần.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (GDP, sản lượng, Bike Sharing), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (5/9 hỏng), cuối buổi phải XANH 9/9
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
