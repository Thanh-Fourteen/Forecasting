# code/ — điểm xuất phát của buổi 14

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Buổi này `tv` **không có** `danh_gia`: bộ chỉ số là thứ bạn tự viết.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `danh_gia.py` | đọc M4 theo ngày và Online Retail II; bốn baseline; tám chỉ số; bảng chỉ số và xếp hạng; đối chiếu `utilsforecast`; chẩn đoán phần dư | sửa `BASELINE`, `mase`, `rmsse`, `danh_gia` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Bảng chỉ số chỉ có **ba** baseline.
- MASE và RMSSE **lệch** `utilsforecast`.
- Bảng bán lẻ ghi MAPE `NaN` mà không nói vì sao.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~120 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (5/13 hỏng), cuối buổi phải XANH 13/13
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
