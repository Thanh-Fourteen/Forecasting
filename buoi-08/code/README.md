# code/ — điểm xuất phát của buổi 8

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một hệ số tương quan đẹp chưa chắc nói điều bạn nghĩ.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `tuong_quan.py` | đọc tải điện ERCOT, nhiệt độ Dallas – Houston, CPI và dân số; tương quan, MI, tương quan chéo, prewhitening, tương quan trượt, Granger | sửa `tuong_quan_chuoi`, `do_tre_dan_dat`, `granger_hai_chieu` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- CPI và dân số Mỹ "quan hệ mạnh".
- Độ trễ dẫn dắt "sau prewhitening" giống hệt con số thô.
- Kết luận "x gây ra y" từ một kiểm định thống kê.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (EIA-930, Open-Meteo, CPI, dân số), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/10 hỏng), cuối buổi phải XANH 10/10
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
