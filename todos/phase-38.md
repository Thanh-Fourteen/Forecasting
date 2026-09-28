# Phase 38 — Buổi 33 · Không gian–thời gian & thời tiết AI 🔲

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 38". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

~5 GB đĩa cho dữ liệu AIFS/ERA5 cắt nhỏ → Phase 28: chỉ cần vài MB (AIFS theo điểm qua Open-Meteo + 1 bản tin GRIB đã trong danh mục).
Việc dữ liệu: thêm `open-meteo` AIFS previous-runs Nội Bài 2025-03 → 2025-12 vào danh mục; snapshot + mirror GHCNh 2026 (tệp đổi hằng ngày);
GNN tự viết bằng PyTorch (PyG Temporal không cài được với torch 2.14 CPU). Xem `buoi-33/NGHIEN-CUU.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 33 Không gian–thời gian & thời tiết AI | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 33: **kiểm chứng AIFS mở tại trạm Nội Bài chỉ trên thời gian sau mốc huấn luyện**; MOS giảm sai số hệ thống;
  GNN nhỏ chạy CPU. **Cột mốc M5**
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)
