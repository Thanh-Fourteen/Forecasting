# Phase 23 — Buổi 24 + dự án giữa chặng 2 ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 23". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 24 Ensemble & AutoML | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 14 trang |
| Dự án giữa chặng 2 | ✅ | đề ✅ | bộ lấy dữ liệu tương lai ✅ | bộ chấm ✅ | leaderboard ✅ | ✅ | ✅ 5 trang |

Bắt buộc:
- Buổi 24: đo khoảng lạc quan khi chọn mô hình trên tập báo cáo; AutoGluon có time limit; cold start bằng analog
- Dự án giữa chặng 2: **chấm trên dữ liệu EIA-930 chưa tồn tại lúc nộp**; so với dự báo day-ahead của đơn vị
  điều độ; script tự lấy dữ liệu thật và chấm; rubric đo cả "khoảng cách backtest vs thực tế". **Cột mốc M3**
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

## Kết quả (2026-09-24)

- Buổi 24: 4.597 chữ, 14 trang, `kiem_de_hieu` 0; đọc thử 0 chặn / 5 khó (đã sửa) / 2 nhỏ; rà gọn cắt 1 chỗ lặp. Lab: đáp án 6/6 xanh, `code/` đỏ đúng
  2/6, notebook 2,6 phút. Ensemble ETS + Theta + LightGBM 0,837 thắng LightGBM 0,855 trên W3; chọn theo chuỗi lạc quan 0,224; AutoGluon 0,882.
- Công cụ: `[[rang_buoc]]` mới cho AutoGluon (statsforecast 2.0.3, torch 2.10.0…); `sinh_nen.py` đưa torch thành phụ thuộc trực tiếp khi bị kéo
  gián tiếp (venv 8,2 GB → 2,2 GB); `dong_goi.py` lọc `lab/du-lieu/moi/`; danh mục thêm 5 bộ thời tiết dự báo lưu trữ.
- Dự án giữa chặng 2: đề, rubric, `cong-cu/` (du_lieu, nop, cham, bang_xep_hang), khung `code/` (chỗ hở: nhiệt độ thật trong backtest), lời giải
  mẫu, bộ chấm tối thiểu 6 test. **Bài nộp thật tuần 2026-09-28 đã nộp trước mốc** — chấm từ 2026-10-09 (Phase 24).
