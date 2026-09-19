# Phase 8 — Viết lại buổi 4–5 + Phụ lục C ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 8". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Cụm trọng tâm của người dùng (đọc biểu đồ, tương quan) — **khó hiểu ở đây là mất giá trị lớn nhất của khoá**.

| Buổi | Đọc thử bản cũ | Viết lại | `kiem_de_hieu` | Tự đọc thử + rà gọn | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 04 Đọc & vẽ biểu đồ | ✅ 6 chặn | ✅ 6 khái niệm, 12 hình × 5 bước | ✅ 78 → 0 | ✅ 0 chặn / 0 khó | ✅ 10/10 | ✅ 12 → 18 tr |
| 05 Biến đổi & điều chỉnh | ✅ 7 chặn | ✅ 6 khái niệm + Nâng cao | ✅ 61 → 2 (có lý do) | ✅ 0 chặn / 0 khó | ✅ 10/10 | ✅ 10 → 15 tr |
| Phụ lục C | — | ✅ 18 loại hình × 5 bước | ✅ 0 | ✅ | — | ✅ 9 → 12 tr |

Bắt buộc:
- Mọi hình: khối "Cách đọc hình" đủ 5 bước (D8) — kỹ năng buổi 4 dạy, tài liệu phải làm mẫu đúng nó
- Buổi 5: log, Box-Cox, bias khi đổi ngược — ví dụ 3–5 số tính tay trước
- Phụ lục C: mỗi loại biểu đồ theo đúng khuôn "Cách đọc hình"
- Kiểm lại mọi câu tính toán trong quiz buổi 4–5 bằng Python
- **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

Kết quả (2026-09-18): chi tiết ở `buoi-04/NGHIEN-CUU.md` (kèm mục Phụ lục C) và `buoi-05/NGHIEN-CUU.md`, mục "Research viết lại"
và "Đọc thử (Phase 8)". Số sửa khi chạy lại: seasonal plot 106 tuần (không phải 104); Yeo-Johnson λ = 1,025 (không phải 1,091).
`kiem_tra_lab.py 4 5` đạt; `kiem_tra_doc_lap.sh 4 5` đạt; ruff sạch ở buổi 4–5 (còn 2 lỗi trong `buoi-14/` chưa commit, ngoài phase).
