# code/ — điểm xuất phát của buổi 27

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng dùng posterior chưa qua chẩn đoán.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `bayes.py` | đọc Car Parts và Bike Sharing; Poisson phân cấp; prior predictive; chẩn đoán r_hat/ESS/divergence; ví dụ 8 trường; BSTS; GP (HSGP); ETS | sửa `PRIOR`, `dung_duoc`, `THANH_PHAN_GP` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–6 | chạy từng ô (có ô mất vài phút) |

**Đang cố tình sai** (chỉ nói triệu chứng):

- Prior tin rằng một phụ tùng có thể bán hàng chục triệu món mỗi tháng.
- Cổng chẩn đoán cho qua một posterior có divergence.
- GP có hàng chục divergence.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (3/5 hỏng), cuối buổi phải XANH 5/5; mất khoảng 3–5 phút
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`. PyMC chạy nhanh hơn nhiều khi máy có trình
biên dịch C (g++ trên Linux, Xcode Command Line Tools trên macOS).
