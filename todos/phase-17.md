# Phase 17 — Buổi 16–17 · ETS, Theta, ARIMA ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 17". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 16 ETS & Theta | ✅ | ✅ 3.536 chữ | ✅ mới | ✅ 8/8, đỏ 4 | ✅ | ✅ 0/0 | ✅ 11 tr |
| 17 ARIMA | ✅ | ✅ 3.575 chữ | ✅ mới | ✅ 6/6, đỏ 3 | ✅ | ✅ 0/0 | ✅ 11 tr |

Bắt buộc:
- **Bản nháp buổi 16–17 đã có** — giữ code/lab/số đo; viết lại `tai-lieu.md` + `kiem-tra.md` theo D1–D13
- Buổi 16: tự viết SES + Holt tối ưu bằng scipy; kiểm coverage thật của khoảng ETS
- Buổi 17: tự xác định bậc từ ACF/PACF và so AICc với auto-ARIMA; Ljung-Box phần dư
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

## Kết quả (2026-09-19)

- "Bản nháp" 16–17 chỉ là khuôn: soạn mới code, đáp án, bộ chấm, hình, notebook, tài liệu, quiz cho cả hai buổi.
- Mọi mô hình so seasonal naive bằng `tv.backtest` + DM trên 366 chuỗi Tourism: AutoETS 1,581 (p < 0,0001), AutoTheta 1,691 (p = 0,49),
  AutoARIMA 1,574 (p < 0,0001), seasonal naive 1,720; AutoARIMA so AutoETS p = 0,74.
- Buổi 16: SES/Holt tự viết (scipy) — SES khớp statsforecast tuyệt đối; Holt lệch ≤ 1,7% trên T249 (khác khởi tạo, ghi rõ); HW nhân 2,13% so với
  cộng 3,23% MAPE trên hành khách EU; tỷ lệ phủ ETS 81,0% / 91,4%.
- Buổi 17: G.17 là chuỗi đã khử mùa vụ → ARIMA không mùa vụ trên G.17, SARIMA trên Tourism T33 (tự chọn cách auto-ARIMA 0,9 AICc, qua Ljung–Box).
- Chỗ hở thêm (đã ghi `quy-uoc.md`): buổi 16 SES khớp bằng mức đã cập nhật; buổi 17 `kiem_phan_du` giả + mô hình tự chọn quên mùa vụ.
- `kiem_tra_lab.py 16 17` đạt; `kiem_tra_doc_lap.sh` đạt; `ruff` sạch; `kiem_de_hieu.py` 0; PDF 11 + 11 trang.
