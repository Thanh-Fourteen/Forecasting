# code/ — điểm xuất phát của buổi 3

Code **chạy được** nhưng **cố tình sai** về thời gian. Đừng tin bảng đếm trông gọn gàng.

| Tệp | Làm gì |
|---|---|
| `thoi_gian.py` | `chuan_hoa_thoi_gian` (hàm cột mốc M0), đọc taxi NYC, đếm chuyến theo giờ, đọc + ghép thời tiết, `gio_nong_nhat` |
| `bam_gio.py` | bấm giờ cùng một việc bằng pandas, polars, DuckDB — không có chỗ sai, chỉ để đo |

**Đang cố tình sai** (triệu chứng, không nói nguyên nhân):
- tháng 3/2024 có một giờ 0 chuyến taxi; tháng 11/2024 có một giờ gần gấp đôi bình thường
- `gio_nong_nhat()` nói New York tháng 3 nóng nhất lúc 20h
- một bảng có dòng xuất trùng vẫn được cộng hai lần

Chạy:

```bash
cd lab && make up                 # một lần: môi trường + dữ liệu (~180 MB)
make check                        # bộ chấm: đầu buổi ĐỎ (10/11 hỏng), cuối buổi phải XANH
make notebook                     # mở các tệp .py dưới dạng notebook
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/bam_gio.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô). Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong
`if __name__ == "__main__":`.
