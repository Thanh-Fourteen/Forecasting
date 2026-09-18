# code/ — điểm xuất phát của buổi 2

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin các con số "95%" đẹp mà nó in ra.

| Tệp | Làm gì |
|---|---|
| `lab.ipynb` | notebook của Lab (bước 1–5) |
| `xac_suat.py` | quantile tự viết, khoảng dự báo, tỷ lệ phủ (tách hai đuôi), khoảng tin cậy bootstrap cho trung bình, mô phỏng chuỗi AR(1), đọc lượt thuê xe theo giờ |

**Triệu chứng bạn sẽ thấy** (chưa nói nguyên nhân — tự tìm bằng mục 4.3 và 4.6 của tài liệu):

- Khoảng dự báo "95%" cho số lượt thuê (luôn ≥ 0) có **cận dưới âm**. Số giờ rơi dưới cận dưới gần 0%, trong khi mục tiêu
  là 2,5%.
- Khoảng tin cậy "95%" cho trung bình của chuỗi AR(1) mô phỏng chỉ chứa trung bình thật khoảng **60%** số lần, chứ không
  phải 95%.

**Bạn cần làm:**

1. Chạy notebook, ghi lại hai con số trên (Lab bước 1).
2. Sửa `khoang_du_bao` để khoảng giữ đúng hình dạng dữ liệu lệch phải (bước 4). Không đổi tên hàm, không đổi tham số.
3. Sửa `khoang_tin_cay_trung_binh` để mặc định dùng được cho dữ liệu tự tương quan (bước 5).
4. Chạy `python lab.py check` tới khi xanh 8/8.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu Bike Sharing, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (5/8 hỏng), cuối buổi phải XANH 8/8
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
