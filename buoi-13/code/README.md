# code/ — điểm xuất phát của buổi 13

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Buổi này `tv` **không có** `ro_ri`: bài kiểm rò rỉ là thứ bạn tự viết.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `feature.py` | lịch âm Việt Nam (tính ở UTC+7); 44 feature cho doanh thu bán lẻ; bảng "biết trước bao lâu"; bài kiểm rò rỉ; đo giá của rò rỉ trên tải điện ERCOT + dự báo thời tiết đã lưu | sửa `kiem_ro_ri`, `feature_tre`, `feature_lich` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Bài kiểm rò rỉ báo **sạch** cho `tb_7`, trong khi mô hình có sai số đẹp bất thường.
- Feature Tết chỉ đúng cho **một năm**.
- Bảng "biết trước bao lâu" xếp vài cột vào nhóm mà chúng không thuộc về.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~140 MB), kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (4/13 hỏng), cuối buổi phải XANH 13/13
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
