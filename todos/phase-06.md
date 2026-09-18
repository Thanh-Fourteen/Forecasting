# Phase 6 — Viết lại buổi 1–3 + Phụ lục A, B cho dễ hiểu ✅

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 6"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Viết lại **phần chữ** theo chuẩn Phase 5. **Giữ nguyên**: chỗ hở cố ý trong `code/`, `lab/cham/`, `00-nen/`, dữ liệu,
các con số đã đo (không cần chạy lại trừ khi thêm số mới). Ví dụ số nhỏ và con số mới **phải chạy thật** bằng script
trong `dap-an/`, ghi seed.

Đọc thử: chặn / khó / nhỏ. Phụ lục không có quiz; dùng câu "Tự kiểm tra" trong bài. Script sinh số của phụ lục:
`phu-luc/ma-vi-du/` (A chạy trong môi trường buổi 3, B trong môi trường buổi 2).

| Buổi | Đọc thử bản cũ (chỗ vướng / quiz) | Viết lại | `kiem_de_hieu` | Đọc thử bản mới | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 01 Forecasting là gì | 9 chặn / 21 khó / 30 nhỏ · quiz 10/10 | ✅ | ✅ 0 | ✅ 0 / 5 / 20 · 10/10 | ✅ | ✅ 19 tr |
| 02 Xác suất & thống kê | 11 / 25 / 16 · quiz 9/10 | ✅ | ✅ độ dài đạt; `nhieu_so` có lý do | ✅ vòng 6: 0 / 4 / 12 · 10/10 | ✅ | ✅ 22 tr |
| 03 Dữ liệu thời gian | 4 / 23 / 18 · quiz 10/10 | ✅ | ✅ 0 | ✅ 0 / 5 / 13 · 10/10 | ✅ | ✅ 21 tr |
| Phụ lục A | — | ✅ | — (bộ kiểm chỉ cho buổi) | ✅ vòng 3: 0 / 3 / 19 (vòng 1: 1 / 9 / 15; vòng 2: 0 / 7 / 15) · Tự kiểm tra 4/4 | — | ✅ 19 tr |
| Phụ lục B | — | ✅ | — | ✅ vòng 4: 0 / 3 / 21 (vòng 1: 0 / 9; vòng 2: 0 / 6; vòng 3: 0 / 7) · Tự kiểm tra 16/16 | — | ✅ 30 tr |

Bắt buộc:
- Buổi 1: 10 mục lý thuyết → ≤ 6 khái niệm chính (M1–M6, bản đồ cách tiếp cận → "Nâng cao"/"Đọc thêm"); mục 4.8 dùng
  mẫu chuẩn Phase 5; quantile/phân phối → hộp "Mượn trước"; trích tiếng Anh của FPP/Petropoulos/Gneiting → diễn giải
- Buổi 2: phân phối, quantile, khoảng, bootstrap, block bootstrap — **mỗi cái có ví dụ số nhỏ tính tay trước dữ liệu thật**;
  "tự tương quan" ở buổi 2 là khái niệm mượn trước (buổi 7 học kỹ)
- Buổi 3: timezone, UTC, DST — ví dụ giờ cụ thể (01:30 xảy ra hai lần), vẽ trục thời gian; so pandas/polars/DuckDB đưa
  sang "Nâng cao" nếu vượt 6 khái niệm
- Thuật ngữ thống nhất theo Phụ lục E mới: buổi 1 bỏ viết tắt "TB 4 tuần" (cả trong code/test: đổi nhãn hiển thị, giữ
  hành vi bộ chấm); "đổi mức" → "dịch mức"; buổi 2 "hệ số lệch" vs E "độ lệch" (skewness) — chọn một, sửa E nếu cần
  vì "độ lệch" dễ nhầm với độ lệch chuẩn. Bảng "Từ mới" lấy từ cột "Nói đơn giản" + "Ví dụ" của E (buổi 1 hiện có 14
  thuật ngữ `chua_bang`, buổi 2 có 18)
- `kiem-tra.md` cả 3 buổi: đáp án giải thích vì sao (D12); `code/README.md` nói rõ học viên cần làm gì
- Mỗi buổi so trước/sau: số chỗ vướng, điểm quiz — ghi `NGHIEN-CUU.md` mục "Đọc thử". Buổi 1 đã có baseline
  (`tools/NGHIEN-CUU-SU-PHAM.md`); buổi 2, 3 đọc thử bản cũ trước khi sửa
- **Buổi 2 phải dạy kỹ khối thống kê nền** mà đọc thử báo chặn ở cả buổi 1, 7, 12: phân phối, quantile, trung vị,
  phương sai, độ lệch chuẩn, tương quan, kiểm định (H0, p-value, mức ý nghĩa, "không bác bỏ ≠ chứng minh")

**Kết quả Phase 6 (2026-09-18).** Cả 5 phần đạt 0 chặn / ≤ 5 khó. Số vòng đọc thử: buổi 1: 2 (+ bản mẫu 4.8), buổi 2: 6,
buổi 3: 1, Phụ lục A: 3, Phụ lục B: 4. Lỗi nội dung thật tìm được nhờ đọc thử và đã sửa: hệ số lệch buổi 2 (1,61 → 1,35
theo đúng lời tài liệu), lời giải thích sai "vì sao block bootstrap không đạt 95%" (buổi 2), "lệch 4 giờ tháng 3–11"
mâu thuẫn lịch DST (buổi 3), 747 nhóm giờ (buổi 3), Phụ lục B: "lệch tối đa 0,5" (đúng 0,9), p của 10 ngửa, so đuôi dày
"440 lần" sai thang (đúng ~100 lần). Độ dài đổi sang đếm chữ ngoài bảng/code (`kiem_de_hieu` mã `do_dai`), trần
4.000–9.000. "TB 4 tuần" đổi thành "trung bình 4 tuần" ở cả code/test buổi 1.
