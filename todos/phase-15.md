# Phase 15 — Đọc thử độc lập buổi 9–13 + dự án giữa chặng 1 + Phụ lục D ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 15". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Phiên mới, không mang ngữ cảnh phase 12–14.

| Tài liệu | Quiz mù | Chặn / khó / nhỏ | Chỗ thừa | Đã sửa + đọc lại | PDF |
|---|---|---|---|---|---|
| Buổi 09 | ✅ 10/10 | ✅ 0 / 1 → 0 / 5 → 1 | ✅ 1 → 0 | ✅ | ✅ 17 tr |
| Buổi 10 | ✅ 10/10 | ✅ 0 / 0 / 3 → 1 | ✅ 0 | ✅ | ✅ 14 tr |
| Buổi 11 | ✅ 10/10 | ✅ 0 / 0 / 6 → 1 | ✅ 0 | ✅ | ✅ 13 tr |
| Buổi 12 | ✅ 10/10 | ✅ 0 / 1 → 0 / 4 → 1 | ✅ 0 | ✅ | ✅ 13 tr |
| Buổi 13 | ✅ 10/10 | ✅ 0 / 3 → 0 / 3 → 2 | ✅ 0 | ✅ + sửa `kiem_nhieu_muc_tieu` | ✅ 14 tr |
| Đề dự án giữa chặng 1 | — | ✅ 2 mơ hồ → 0 | ✅ 1 → 0 | ✅ | ✅ 5 tr |
| Phụ lục D | — (không có quiz) | ✅ 0 / 2 → 0 / 4 → 2 | ✅ 0 | ✅ | ✅ 7 tr |

Bắt buộc:
- Đề dự án: viết lại được đúng "làm gì, nộp gì, chấm thế nào", 0 chỗ mơ hồ
- Mọi sửa → `kiem_tra_lab.py 9-13` + bộ chấm dự án vẫn đúng

## Kết quả (2026-09-19)

Ghi chi tiết: mục "Đọc thử độc lập (Phase 15)" trong `buoi-09..13/NGHIEN-CUU.md` (đề dự án và Phụ lục D ghi ở `buoi-13/NGHIEN-CUU.md`).
Sửa bằng viết lại câu (+12 tới +58 chữ mỗi buổi). Lỗi đáng kể nhất: `kiem_nhieu_muc_tieu` của buổi 13 (`code/` + `dap-an/`) so sai vùng dòng
nên **không bắt lag < tầm dự báo**, đúng việc tài liệu nói nó làm; sửa theo `tools/khung/ro_ri.py` (giữ dòng có $t − h$ < mốc). Lỗi chung:
"backtest", "feature/mục tiêu" dùng mà buổi không định nghĩa (10, 12, 13). Đề dự án: kiểm nhiễu mục tiêu không có hàm trong khung, baseline
không nói so với gì → ghi rõ; lời giải mẫu thêm hàm kiểm nhiễu mục tiêu. `kiem_tra_lab.py 9-13` đạt; bộ chấm dự án với lời giải mẫu 8/8;
`kiem_tra_doc_lap.sh 9–13` đạt; `ruff` sạch cho buổi 9–13, dự án 1, tools.
