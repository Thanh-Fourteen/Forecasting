# Phase 9 — Viết lại buổi 6–7 ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 9". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Cụm trọng tâm (đọc biểu đồ, tương quan).

| Buổi | Đọc thử bản cũ | Viết lại | `kiem_de_hieu` | Tự đọc thử + rà gọn | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 06 Phân rã | ✅ 6 chặn | ✅ 6 khái niệm | ✅ 66 → 0 | ✅ 0 chặn / 0 khó | ✅ 10/10 | ✅ 11 → 16 tr |
| 07 Tự tương quan & tính dừng | ✅ 7 chặn | ✅ 6 khái niệm | ✅ 64 → 0 | ✅ 0 chặn / 0 khó | ✅ 10/10, câu 5 sửa | ✅ 10 → 15 tr |

Bắt buộc:
- Buổi 6: xu hướng/mùa vụ/phần dư — ví dụ chuỗi 12 điểm tự phân rã bằng tay; $F_T, F_S$ nói bằng lời
- Buổi 7: ACF/PACF — tính tay tự tương quan trễ 1 trên 6 số; "dừng" bằng ví dụ đời thường; ADF vs KPSS bằng bảng 2×2
  có câu "nghĩa là gì" từng ô; giả thuyết không/p-value → "Mượn trước" nếu buổi 2 chưa dạy đủ
- **Quiz buổi 7 câu 5 có đáp án sai** ($\bar y$ = 52/9, không phải 6; $r_1 ≈ 0{,}020$) — sửa; kiểm lại mọi câu tính trong
  quiz buổi 6–7 bằng Python. Baseline đọc thử buổi 7 (chỗ chặn: kiểm định/H0/p-value, nghiệm đơn vị, AR(1), trích
  Zivot/Nau tiếng Anh; ngưỡng sai phân thừa −0,5 hay −0,45 không thống nhất)
- **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

Kết quả (2026-09-18): chi tiết ở `buoi-06/NGHIEN-CUU.md`, `buoi-07/NGHIEN-CUU.md` (mục "Research viết lại", "Đọc thử (Phase 9)").
Sửa lỗi bản cũ khi chạy lại: chuỗi lượt thuê theo ngày bị `dropna()` giữa chừng (ACF, `diff(7)` sai; không có đỉnh ở trễ 7) → thay bằng
bảng sai phân theo giờ; số đợt nắng nóng buổi 6 đo lại bằng MSTL của lab; bài tập 3 buổi 6 sai độ dài chuỗi. `kiem_tra_lab.py 6 7`,
`kiem_tra_doc_lap.sh 6 7`, ruff buổi 6–7: đạt.
