# code/ — điểm xuất phát của buổi 5

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin một con số tăng trưởng khi chưa biết nó đã bỏ gì.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `bien_doi.py` | đọc bán lẻ Mỹ, CPI, dân số; điều chỉnh lịch và lạm phát; Box-Cox, Guerrero; dự báo trên thang log và đổi ngược | sửa `so_sanh_thang`, `tang_truong_thuc_dau_nguoi`, `boxcox_nguoc` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- "Tháng 3/2023 tăng 14,2% so với tháng 2", và con số "theo ngày" y hệt con số so thẳng.
- "Bán lẻ tăng 316% từ 1993", kể cả khi đã hỏi tăng trưởng thực trên đầu người.
- Dự báo trung bình và dự báo trung vị ra y hệt nhau.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (bán lẻ, CPI, dân số), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (5/8 hỏng), cuối buổi phải XANH 8/8
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
