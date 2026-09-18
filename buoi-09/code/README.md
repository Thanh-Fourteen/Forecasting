# code/ — điểm xuất phát của buổi 9

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một tương quan bằng 0 chưa chắc nghĩa là "không liên quan".

| Tệp | Làm gì |
|---|---|
| `dac_trung.py` | đọc 48.000 chuỗi M4 (.tsf) và doanh số bán lẻ; 20 đặc trưng tự viết; entropy phổ; sai số thật của seasonal naive; PCA; phân cụm DTW; ABC–XYZ |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- bảng tương quan kết luận entropy phổ **không** liên quan tới độ khó dự báo (r = −0,05)
- bốn cụm DTW chỉ khác nhau ở độ lớn, không khác nhau ở hình dạng
- chiến lược đề xuất: tune mô hình cho **cả 4.000 chuỗi**, kể cả chuỗi gần như nhiễu trắng

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu (~74 MB)
make check                 # bộ chấm: đầu buổi ĐỎ (4/10 hỏng), cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/dac_trung.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
