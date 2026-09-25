# code/ — điểm xuất phát của buổi 24

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin kết quả đẹp.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `ensemble.py` | đọc 1.000 chuỗi M4 theo tháng; 30 ứng viên (thống kê, LightGBM global, kết hợp định sẵn) ở 3 cửa sổ; MASE; chọn mô hình và báo cáo; trọng số kết hợp; AutoGluon | sửa `CUA_SO_CHON`, `CUA_SO_BAO_CAO`, `chon_va_bao_cao` (tài liệu mục 5, bước 3) |
| `cold_start.py` | dự báo 8 tuần đầu của 200 mã hàng mới (Online Retail II) bằng hàng tương tự | chạy, đọc kết quả |
| `lab.ipynb` | notebook của Lab, bước 1–7 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- "Chọn mô hình tốt nhất cho từng chuỗi" đạt MASE bỏ xa mọi mô hình và mọi cách kết hợp.
- Trọng số "tối ưu" cho kết quả còn đẹp hơn.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường (~2 GB: AutoGluon, torch CPU) + dữ liệu, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb; ô bước 1 lần đầu 3–6 phút, ô bước 6 lần đầu 1–2 phút
python lab.py check        # bộ chấm: đầu buổi ĐỎ (2/6 hỏng), cuối buổi phải XANH 6/6
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
