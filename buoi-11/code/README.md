# code/ — điểm xuất phát của buổi NN

<!-- Khuôn: thay NN, liệt kê tệp, giữ nguyên mục "Đang cố tình sai". Ngắn — dưới 30 dòng. -->

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin kết quả đẹp.

| Tệp | Làm gì |
|---|---|
| `vi_du.py` | … |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- …

Chạy:

```bash
cd lab && make up          # một lần: môi trường + dữ liệu
make check                 # bộ chấm — lúc đầu buổi sẽ ĐỎ, cuối buổi phải XANH
make notebook              # mở các tệp .py dưới dạng notebook
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
