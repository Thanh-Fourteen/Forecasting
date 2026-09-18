# code/ — điểm xuất phát của buổi 8

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một hệ số tương quan không tự nói nó có nghĩa gì.

| Tệp | Làm gì |
|---|---|
| `tuong_quan.py` | đọc tải điện ERCOT + nhiệt độ Dallas/Houston + CPI/dân số; hệ số tương quan, mutual information, hồi quy đơn, CCF, prewhitening, tương quan trượt, Granger hai chiều |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- CPI và dân số Mỹ được kết luận "quan hệ mạnh" (r = 0,974)
- độ trễ dẫn dắt của nhiệt độ so với tải điện ra 1 giờ, và CCF cao gần bằng nhau ở mọi độ trễ tới 48
- kết luận "x gây ra y" từ kiểm định Granger

Chạy:

```bash
cd lab && python lab.py up          # một lần: môi trường + dữ liệu (~93 MB)
python lab.py check                 # bộ chấm: đầu buổi ĐỎ (3/10 hỏng), cuối buổi phải XANH
python lab.py notebook              # mở các tệp .py dưới dạng notebook
python lab.py chay ../code/tuong_quan.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
