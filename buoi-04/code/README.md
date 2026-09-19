# code/ — điểm xuất phát của buổi 4

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin một biểu đồ trông thuyết phục.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `bieu_do.py` | đọc lượt thuê xe theo giờ trên lưới đầy đủ, hồ sơ giờ × thứ, ACF, cặp trễ, bộ biểu đồ chẩn đoán, biểu đồ gây hiểu nhầm và bản vẽ lại | sửa `ho_so_tuan`, viết 8 hàm vẽ và `ve_lai_trung_thuc` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Bộ biểu đồ chẩn đoán chỉ có 2 hình; nhìn vào không thấy thứ Bảy khác thứ Hai.
- Bảng hồ sơ giờ × thứ có 7 dòng giống hệt nhau.
- "Bản vẽ lại trung thực" vẫn nói lượt thuê bám sát nhiệt độ.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu Bike Sharing, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (7/8 hỏng), cuối buổi phải XANH 8/8
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
