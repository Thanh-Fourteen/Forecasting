# Phase 2 — Buổi 1–3 · Nền móng ✅

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 2"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 01 Forecasting là gì | ✅ | ✅ 3.972 chữ | ✅ 4/8 | ✅ 8/8 | ✅ | ✅ 10 trang |
| 02 Xác suất & thống kê | ✅ | ✅ 3.872 chữ | ✅ 3/8 | ✅ 8/8 | ✅ | ✅ 10 trang |
| 03 Dữ liệu thời gian | ✅ | ✅ ~3.725 chữ | ✅ 1/11 | ✅ 11/11 | ✅ | ✅ 10 trang |

Cột "Code" là điểm `make check` của `code/` — phải THẤP (chỗ hở còn nguyên);
cột "Lab" là điểm của `dap-an/` — phải tuyệt đối.

Bắt buộc:
- Buổi 1: phiếu bài toán dự báo 6 ô dùng lại được; bảng bài học M1–M6; demo đánh giá trên dữ liệu huấn luyện cho sai số ảo
  (*Phase 2 đo trên UCI 235 theo giờ, 46 gốc tuần 2010:* bảng lịch khớp cả dữ liệu MAE 0,380 → trung thực 0,508, thua
  TB 4 tuần 0,490; ở tổng tuần thứ hạng đảo — bảng lịch 16,4 vs TB 4 tuần 27,9 kWh. Bốn kết luận "đơn giản ≥ phức tạp…" là của M1,
  M3 xác nhận)
- Buổi 2: tự viết quantile + bootstrap + block bootstrap bằng NumPy; đo tỷ lệ phủ thật của "±1.96σ"
  (*Phase 2 đo trên Bike Sharing:* khoảng theo từng giờ dựng từ 2011 phủ 72,5% trên 2012 — do dịch chuyển mức, quantile
  thực nghiệm cũng chỉ 70,1%; trong mẫu 2011 phủ 96,4% nhưng đuôi lệch 0,3%/3,3%. Đã sửa "Xong khi" của lộ trình: quantile
  sửa hình dạng, block bootstrap sửa khoảng tin cậy của trung bình — hai vấn đề khác nhau)
- Buổi 3: bấm giờ pandas vs polars vs DuckDB trên cùng dữ liệu; test DST, trùng lặp, lệch múi giờ; **Cột mốc M0**
