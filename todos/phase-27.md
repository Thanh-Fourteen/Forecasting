# Phase 27 — Đọc thử độc lập buổi 25–28 ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 27". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Phiên mới, không mang ngữ cảnh các phase soạn buổi 25–28.

| Tài liệu | Quiz mù | Chặn / khó / nhỏ | Chỗ thừa | Đã sửa + đọc lại | PDF |
|---|---|---|---|---|---|
| Buổi 25 | ✅ 10/10 | ✅ 0 / 3 / 3 → 0 / 0 / 0 | ✅ 0 | ✅ | ✅ 14 tr |
| Buổi 26 | ✅ 10/10 | ✅ 0 / 1 / 4 → 0 / 0 / 1 | ✅ 0 | ✅ | ✅ 12 tr |
| Buổi 27 | ✅ 10/10 | ✅ 0 / 2 / 4 → 0 / 0 / 0 | ✅ 0 | ✅ | ✅ 13 tr |
| Buổi 28 | ✅ 10/10 | ✅ 0 / 3 / 4 → 0 / 0 / 2 | ✅ 0 | ✅ | ✅ 11 tr |

Bắt buộc:
- Mọi sửa → `kiem_tra_lab.py` các buổi của cụm vẫn xanh/đỏ đúng chỗ
- **Chấm bài nộp thật dự án giữa chặng 2** (chuyển từ Phase 24, lúc đó chưa tới ngày chấm; làm được từ 2026-10-09): `cd du-an-giua-chang/02-thi-du-bao/lab
  && python lab.py chay ../cong-cu/cham.py --moc 2026-09-28 --nhom loi-giai-mau --ra ../giam-khao/chay-thu`; ghi MASE thật so với backtest và so `df` vào
  `du-an-giua-chang/02-thi-du-bao/NGHIEN-CUU.md` (thay dòng "chờ"). Cần `dau-vao.parquet` trên máy soạn (không commit)

Kết quả (2026-09-25): chi tiết ở mục "Đọc thử độc lập" của `NGHIEN-CUU.md` từng buổi. Quiz mù 40/40; 9 chỗ khó → 0. `kiem_tra_lab.py 25–28` đạt
(đáp án xanh, `code/` đỏ đúng chỗ, notebook chạy hết), `kiem_tra_doc_lap.sh` đạt, `ruff` sạch. Chấm bài nộp thật dự án giữa chặng 2: **chờ** (chưa tới
9/10) — chuyển Phase 32. Còn mở (buổi 28): dòng coverage trong mẫu và ngoài mẫu chấm trên hai đoạn khác nhau — tài liệu đã nói rõ; chấm lại trên cùng
17 mốc cần đổi `dap-an/` và `cham/`.
