# code/ — điểm xuất phát của buổi 12

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một bộ lọc cho MAE thấp hơn 28% thường không phải vì nó tốt, mà vì nó
đã nhìn thấy tương lai.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `khu_nhieu.py` | đọc cảm biến 10 phút (UCI Appliances Energy); phổ Welch; hạ mẫu; 10 cấu hình bộ lọc (trung bình trượt, EWMA, Savitzky–Golay, Butterworth, Kalman, wavelet); bài kiểm nhân quả; đo giá của rò rỉ | sửa `ha_mau`, `kiem_nhan_qua`, `danh_gia_feature`, `cham_tren_muc_tieu_lam_tron` (tài liệu mục 5) |
| `lab.ipynb` | notebook của Lab, bước 1–5 | chạy từng ô |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Bảng bộ lọc kết luận trung bình trượt có tâm, Savitzky–Golay và Kalman smoother đều **nhân quả**.
- Phổ sau khi hạ mẫu về 1 giờ có một đỉnh ở chu kỳ 2,5 giờ, lọc trước hay không cũng vậy.
- Báo cáo khoe MAE **35,8** trong khi chuỗi gốc cho 46,8.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu Appliances Energy, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb (hoặc mở bằng VS Code)
python lab.py check        # bộ chấm: đầu buổi ĐỎ (6/8 hỏng), cuối buổi phải XANH 8/8
```

Bạn sửa **tệp `.py`**; notebook `lab.ipynb` nạp lại nó tự động. Dùng conda: `python lab.py up --pip`.
