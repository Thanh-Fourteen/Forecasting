# code/ — điểm xuất phát của buổi 3

Code **chạy được** nhưng **cố tình sai** về thời gian. Bảng đếm trông gọn gàng, nhưng đừng tin nó. Việc của bạn: tìm ra
chỗ sai, sửa `thoi_gian.py` cho tới khi `make check` xanh 11/11.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `thoi_gian.py` | `chuan_hoa_thoi_gian` (hàm cột mốc M0: dữ liệu thô → bảng dạng dài `unique_id, ds, y`), đọc taxi New York, đếm chuyến theo giờ, đọc + ghép thời tiết, `gio_nong_nhat` | sửa theo đặc tả trong docstring của `chuan_hoa_thoi_gian` và Lab bước 4 của tài liệu |
| `bam_gio.py` | bấm giờ cùng một việc bằng pandas, polars, DuckDB | chỉ chạy và ghi số của máy bạn; tệp này không có chỗ sai |

**Đang cố tình sai** (chỉ nói triệu chứng, không nói nguyên nhân):

- Tháng 3/2024 có một giờ 0 chuyến taxi. Tháng 11/2024 có một giờ gần gấp đôi một giờ bình thường cùng lúc đó tuần sau.
- `gio_nong_nhat()` nói New York tháng 3 nóng nhất lúc 20 giờ (8 giờ tối). Ai cũng biết buổi chiều nóng hơn buổi tối.
- Một bảng có dòng xuất trùng (cùng thời điểm, cùng giá trị, ghi hai lần) vẫn được cộng hai lần.

Chạy (trong thư mục `lab/`):

```bash
cd lab && make up                 # một lần: dựng môi trường + tải dữ liệu (~180 MB), kiểm sha256
make check                        # chạy bộ chấm: đầu buổi ĐỎ (10/11 test hỏng), cuối buổi phải XANH 11/11
make notebook                     # mở các tệp .py dưới dạng notebook Jupyter
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/bam_gio.py   # bấm giờ ba công cụ
```

Tệp `.py` viết dạng *percent*: mỗi dòng `# %%` bắt đầu một ô notebook. Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy
thử đặt trong `if __name__ == "__main__":`.
