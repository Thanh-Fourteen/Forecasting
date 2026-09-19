# Phase 13 — Viết lại buổi 11–12 ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 13". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Cụm trọng tâm thứ hai.

| Buổi | Đọc thử bản cũ | Viết lại | `kiem_de_hieu` | Tự đọc thử + rà gọn | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 11 Ngoại lai & điểm gãy | ✅ 10 chặn | ✅ 6 mục + notebook | ✅ 56 → 0 | ✅ 0 chặn / 0 khó | ✅ 10/10 | ✅ 9 → 13 tr |
| 12 Khử nhiễu & miền tần số | ✅ 9 chặn | ✅ 10 → 6 mục + notebook | ✅ 57 → 0 | ✅ 0 chặn / 0 khó | ✅ 10/10 | ✅ 10 → 13 tr |

Bắt buộc:
- Buổi 11: z-score, Hampel, masking, PELT, penalty — ví dụ 10 số tính tay; "masking" giải thích bằng hình; "đổi mức" → "dịch mức"
- Buổi 12: tần số, Nyquist, aliasing — trực giác (bánh xe quay ngược trong phim) trước công thức; "bộ lọc nhân quả"
  = chỉ dùng quá khứ, ví dụ trung bình trượt 3 điểm tính tay hai kiểu
- Buổi 12 baseline đọc thử (chỗ chặn: MAE/RMSE, phương sai, periodogram, lọc thông thấp, IIR, wavelet, đo trễ bằng
  tương quan, trích `filtfilt`/SavGol/Hamilton tiếng Anh; "10 cấu hình" bộ lọc chưa liệt kê)
- Buổi 11 hiện 9 trang (dưới 10) — viết lại cho đủ nội dung chứ không độn
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

Kết quả (2026-09-18): chi tiết ở `buoi-11/NGHIEN-CUU.md`, `buoi-12/NGHIEN-CUU.md` mục "Research viết lại", "Đọc thử (Phase 13)". Buổi 11: ví dụ
10 số cho z-score/masking/MAD/PELT + hình mới `masking-10-so.png`; "đổi mức" → "dịch mức" cả trong code; dấu sai số COVID theo quy ước khoá.
Buổi 12: trực giác bánh xe trước công thức; trung bình trượt 3 điểm tính tay hai kiểu; 10 cấu hình bộ lọc liệt kê đủ. Sửa số trạng thái:
`doi_phuong_sai` (buổi 11) bắt hụt chứ không báo khắp nơi; buổi 12 code hỏng 6/8 test chứ không 2/8. `kiem_tra_lab.py 11 12`,
`kiem_tra_doc_lap.sh 11 12`, ruff: đạt.
