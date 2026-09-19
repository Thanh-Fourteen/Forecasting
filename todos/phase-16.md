# Phase 16 — Buổi 14–15 · Baseline, chỉ số, backtest ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 16". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 14 Baseline & chỉ số | ✅ | ✅ 3.940 chữ | ✅ | ✅ 13/13, đỏ 5 | ✅ | ✅ 0/0 | ✅ 16 tr |
| 15 Backtesting | ✅ | ✅ 3.990 chữ | ✅ mới | ✅ 9/9, đỏ 3 | ✅ | ✅ 0/0 | ✅ 12 tr |

Bắt buộc:
- **Bản nháp buổi 14–15 đã có** (thư mục chưa commit, chuẩn cũ) — giữ code/lab/số đo; `tai-lieu.md` + `kiem-tra.md` viết lại
  theo D1–D13; bỏ Makefile cũ nếu còn (sinh lại nền)
- Buổi 14: tự viết 7 chỉ số, đối chiếu utilsforecast; bảng xếp hạng đảo lộn khi đổi chỉ số; mở rộng `phu-luc/D-cong-thuc-chi-so.md`
- Buổi 15: đo khoảng lạc quan của CV ngẫu nhiên so với hold-out cuối; Diebold–Mariano; ba tập tune/chọn/báo cáo;
  **bộ backtest cả khoá dùng — thiết kế kỹ, có test**
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

## Kết quả (2026-09-19)

- Buổi 14: bản nháp giữ code/lab/số; sửa quy ước ME thành mean(y − ŷ) (bản nháp ngược dấu cả khoá); bỏ hình quy ước thư viện; chọn lại chuỗi
  minh hoạ hình bốn baseline; viết mới tài liệu, quiz, notebook, README, NGHIEN-CUU.
- Buổi 15: soạn mới toàn bộ (bản nháp chỉ có khuôn): `backtest.py` (cùng giao diện `tv.backtest`), 9 test (vị trí cửa sổ + gap, không lộ tương
  lai, sliding, dòng thừa, khớp statsforecast, feature không rò rỉ, 3 chỗ hở), 5 hình, notebook. Chỗ hở thứ ba (DM bỏ tự tương quan) thêm vào
  bảng `quy-uoc.md`.
- Số thật đáng chú ý: K-fold xáo trộn lạc quan 23% với rừng ngẫu nhiên nhưng chỉ 12% với hồi quy tuyến tính (khớp Bergmeir et al. 2018);
  rolling origin lệch hold-out −8,7% (rừng) / −15,5% (hồi quy, do đổi mùa — tài liệu báo thật); chọn và báo cáo cùng đoạn lạc quan 25%;
  "hơn 4,3%" chỉ có khi tune trên hold-out, DM-HLN p = 0,16.
- Phụ lục D: thêm bảng ví dụ trên dữ liệu thật buổi 14–15 (8 trang).
- `kiem_tra_lab.py 14 15` đạt; `kiem_tra_doc_lap.sh` đạt; `ruff` sạch; `kiem_de_hieu.py` 0.
