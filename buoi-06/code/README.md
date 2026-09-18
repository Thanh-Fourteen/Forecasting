# code/ — điểm xuất phát của buổi 6

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Phần dư nhỏ chưa chắc là phân rã tốt.

| Tệp | Làm gì |
|---|---|
| `phan_ra.py` | đọc nhu cầu điện PJM theo giờ (EIA-930), lấp giờ trống, phân rã, độ mạnh xu hướng/mùa vụ, đo mẫu hình còn trong phần dư |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- độ mạnh mùa vụ chỉ 0,618 cho một chuỗi điện rõ ràng rất mùa vụ, và không có thành phần tuần
- phần dư còn 10% phương sai ở hồ sơ tháng × giờ; 24 giờ đầu/cuối không có xu hướng
- `phan_ra(y, robust=True)` cho kết quả y hệt `robust=False`

Chạy:

```bash
cd lab && python lab.py up          # một lần: môi trường + dữ liệu EIA-930 2024 (~90 MB)
python lab.py check                 # bộ chấm: đầu buổi ĐỎ (5/7 hỏng), cuối buổi phải XANH
python lab.py notebook              # mở các tệp .py dưới dạng notebook
python lab.py chay ../code/phan_ra.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
