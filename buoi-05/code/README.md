# code/ — điểm xuất phát của buổi 5

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một con số tăng trưởng chỉ có nghĩa khi nói rõ đã điều chỉnh gì.

| Tệp | Làm gì |
|---|---|
| `bien_doi.py` | đọc doanh số bán lẻ (Census MARTS), CPI-U (BLS), dân số (BEA); điều chỉnh lịch/lạm phát/dân số; Box-Cox + Guerrero tự viết; dự báo trên thang log và đổi ngược |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- "tháng 2/2023 giảm 3,4% so với tháng 1"
- "doanh số bán lẻ tăng 316% từ 1993 tới 2025"
- dự báo đổi ngược từ thang log luôn thấp hơn thực tế một chút, ở mọi chuỗi

Chạy:

```bash
cd lab && python lab.py up          # một lần: môi trường + dữ liệu (~3 MB)
python lab.py check                 # bộ chấm: đầu buổi ĐỎ (5/8 hỏng), cuối buổi phải XANH
python lab.py notebook              # mở các tệp .py dưới dạng notebook
python lab.py chay ../code/bien_doi.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
