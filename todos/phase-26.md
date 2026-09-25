# Phase 26 — Buổi 27–28 · Bayes & GP, dự báo phân cấp ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 26". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 27 Bayes & GP | ✅ | ✅ 4.146 chữ | ✅ 3 chỗ hở | ✅ 5/5 xanh, code đỏ 3 | ✅ | ✅ 0/0/0, thừa 0 | ✅ 13 tr |
| 28 Dự báo phân cấp | ✅ | ✅ 3.544 chữ | ✅ 1 chỗ hở | ✅ 6/6 xanh, code đỏ 1 | ✅ | ✅ 0/0/1, thừa 0 | ✅ 11 tr |

Bắt buộc:
- Buổi 27: prior predictive check sửa prior; no/complete/partial pooling; **chẩn đoán r_hat, ESS, divergence bắt buộc trong `cham/`**
- Buổi 28: tổng khớp tuyệt đối mọi cấp; MinT vs bottom-up/top-down từng cấp; reconciliation xác suất. **Cột mốc M4**
  (2026-09-24, người dùng chọn: dạy trung thực — MinT thắng base 2/4 cấp vì base cấp dưới chệch; coverage cấp trên 58% → 79%
  sau hiệu chỉnh ngoài mẫu; tiêu chí M4 sửa trong lo-trinh)
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

Kết quả (2026-09-24):
- Buổi 27: prior rộng sinh q90 20 triệu món/tháng; Poisson phân cấp (2.000 mẫu/chuỗi) r_hat 1,006, 0 divergence, RMSE 1,182 < không gộp 1,212;
  8 trường centered 312 → non-centered 0 divergence; GP ba thành phần 27 divergence (chỗ hở), GP hai thành phần MAE 1.142 so với ETS 1.885;
  BSTS hội tụ nhưng phủ 46,7% (bão Sandy ngay trước mốc). Calibration số đếm: dự báo 67,6% tháng bán 0, thật 78,7%.
- Buổi 28: base lệch cộng 1.613; MinT thắng base 2/4 cấp (base cấp dưới chệch — người dùng chọn dạy trung thực); khoảng 90% cấp quốc gia
  58% (trong mẫu) → 79% (ngoài mẫu, khớp). Cột mốc M4 định nghĩa lại trong lo-trinh.
- Thêm arviz 1.3.0, rdata 1.1.0 vào bảng chung; giấy phép TRA xác minh CC BY 4.0.
- Lab: `kiem_tra_lab.py 27 28 --may-trang` đạt; `up --pip` đạt.
