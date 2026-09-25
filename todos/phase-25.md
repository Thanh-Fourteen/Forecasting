# Phase 25 — Buổi 25–26 · Dự báo xác suất, conformal ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 25". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 25 Dự báo xác suất | ✅ | ✅ 4.337 chữ | ✅ 3 chỗ hở | ✅ 9/9 xanh, code đỏ 3 | ✅ | ✅ 0/0/2, thừa 0 | ✅ 14 tr |
| 26 Conformal | ✅ | ✅ 3.649 chữ | ✅ 2 chỗ hở | ✅ 7/7 xanh, code đỏ 3 | ✅ | ✅ 0/0/1, thừa 0 | ✅ 12 tr |

Bắt buộc:
- Buổi 25: tự viết pinball, CRPS từ mẫu, WIS; PIT + reliability diagram của 3 mô hình có lỗi calibration khác nhau; peaks-over-threshold
- Buổi 26: coverage trượt theo thời gian của split / CQR / EnbPI / ACI trên dữ liệu có drift thật
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

Kết quả (2026-09-24):
- Buổi 25 (ERCOT): khoảng từ phần dư trong mẫu phủ 78,2% (90%) → phần dư ngoài mẫu 88,8%; LightGBM 9 quantile lệch ≤ 2,5 điểm sau sắp xếp;
  pinball/CRPS/WIS tự viết khớp scoringrules (WIS của scoringrules 0.11.0 có lỗi — đối chiếu bằng tổng pinball); PIT + reliability của 4 cách
  (chữ U, vòm, dốc, phẳng); POT trên nhiệt độ tối đa Dallas 1940–2025 (bộ dữ liệu mới), mức 10 năm 41,4 °C.
- Buổi 26 (Beijing PM2.5): coverage 30 ngày ngoài dải 85–95%: split 29,5%, EnbPI 24,6%, CQR 2,8%, ACI (γ 0,005 định trước) 1,1%; coverage
  có điều kiện giờ PM2.5 > 150: ACI 76,6%, CQR 88,2%; MAPIE 6 tháng 90,7% so với tự viết 90,6%.
- Lab: `kiem_tra_lab.py 25 26` và `--may-trang` đạt; `up --pip` đạt cả hai buổi.
