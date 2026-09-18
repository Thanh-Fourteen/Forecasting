# code/ — điểm xuất phát của buổi 7

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một kiểm định không đủ để kết luận.

| Tệp | Làm gì |
|---|---|
| `tu_tuong_quan.py` | ACF tự viết, dải nhiễu trắng, Ljung-Box, kiểm định nghiệm đơn vị, số lần sai phân, bảng 4 chuỗi mô phỏng; đọc GDP (BEA), sản lượng công nghiệp (FRB G.17), lượt thuê xe |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- chuỗi có xu hướng tuyến tính rõ ràng bị kết luận "không dừng — cần sai phân"
- nhiễu trắng cũng được sai phân một lần; cột `d` của bảng 4 chuỗi toàn bằng 1

Chạy:

```bash
cd lab && python lab.py up          # một lần: môi trường + dữ liệu (~36 MB)
python lab.py check                 # bộ chấm: đầu buổi ĐỎ (5/9 hỏng), cuối buổi phải XANH
python lab.py notebook              # mở các tệp .py dưới dạng notebook
python lab.py chay ../code/tu_tuong_quan.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
