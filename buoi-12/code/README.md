# code/ — điểm xuất phát của buổi 12

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin kết quả đẹp: một bộ lọc cho MAE thấp hơn 28%
thường không phải vì nó tốt, mà vì nó đã nhìn thấy tương lai.

| Tệp | Làm gì |
|---|---|
| `khu_nhieu.py` | đọc cảm biến 10 phút (UCI Appliances); phổ Welch; hạ mẫu; 10 cấu hình bộ lọc (MA, EWMA, SavGol, Butterworth, Kalman, wavelet); bài kiểm nhân quả; đo giá của rò rỉ |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- bảng bộ lọc kết luận MA centered, Savitzky–Golay và Kalman smoother đều **nhân quả**
- phổ sau khi hạ mẫu về 1 giờ có một đỉnh ở chu kỳ 2,5 giờ mà không ai giải thích được
- báo cáo khoe MAE **35,8** trong khi chuỗi gốc cho 46,8

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu (~12 MB)
make check                 # bộ chấm: đầu buổi ĐỎ (2/8 hỏng), cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/khu_nhieu.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
