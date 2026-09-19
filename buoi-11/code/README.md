# code/ — điểm xuất phát của buổi 11

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. "Sạch" không có nghĩa là "mượt", và "bất thường" không có nghĩa là "sai".

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `bat_thuong.py` | đọc lượt xem Wikipedia tiếng Việt (tổng và bài "Tết Nguyên Đán"), hành khách hàng không EU; z-score, IQR, MAD, Hampel, STL robust; masking; chuỗi mô phỏng có nhãn; PELT và quét penalty; ba cách xử lý COVID | sửa `xu_ly_ngoai_lai`, `diem_gay`, `doi_phuong_sai` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Làm sạch chuỗi Tết thì mất cả 10 đỉnh Tết và thủng mốc thời gian.
- Hành khách hàng không EU ra 43 điểm gãy, không ai giải thích nổi.
- Không thấy đoạn "đổi phương sai" cài sẵn trong chuỗi mô phỏng.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (Wikipedia, Eurostat), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (4/12 hỏng), cuối buổi phải XANH 12/12
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
