# code/ — điểm xuất phát của buổi 4

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin một biểu đồ trông thuyết phục.

| Tệp | Làm gì |
|---|---|
| `bieu_do.py` | đọc lượt thuê xe theo giờ trên lưới đầy đủ, hồ sơ giờ×thứ, ACF, cặp trễ, bộ biểu đồ chẩn đoán, biểu đồ gây hiểu nhầm và bản vẽ lại |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- bộ biểu đồ chẩn đoán chỉ có 2 hình, nhìn vào không thấy thứ Bảy khác thứ Hai
- bảng hồ sơ giờ×thứ có 7 dòng giống hệt nhau
- "bản vẽ lại trung thực" vẫn nói lượt thuê bám sát nhiệt độ

Chạy:

```bash
cd lab && python lab.py up          # một lần: môi trường + dữ liệu Bike Sharing
python lab.py check                 # bộ chấm: đầu buổi ĐỎ (7/8 hỏng), cuối buổi phải XANH
python lab.py notebook              # mở các tệp .py dưới dạng notebook
python lab.py chay ../code/bieu_do.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
