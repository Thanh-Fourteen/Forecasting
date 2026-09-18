# code/ — điểm xuất phát của buổi 13

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Buổi này `tv` **không có** `ro_ri` — bài kiểm rò rỉ là thứ bạn tự viết.

| Tệp | Làm gì |
|---|---|
| `feature.py` | lịch âm Việt Nam (Meeus, kinh tuyến 105°Đ); 41 feature cho doanh thu bán lẻ; bài kiểm rò rỉ; đo giá của rò rỉ trên phụ tải ERCOT + dự báo thời tiết đã lưu |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- bài kiểm rò rỉ báo **sạch** cho `tb_7`, trong khi mô hình có MAE đẹp bất thường
- feature Tết chỉ đúng cho **một năm**
- bảng "biết trước bao lâu" có cột không xếp được vào nhóm nào

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu (~140 MB)
make check                 # bộ chấm: đầu buổi ĐỎ (4/13 hỏng), cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/feature.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
