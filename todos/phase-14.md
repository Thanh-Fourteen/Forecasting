# Phase 14 — Viết lại buổi 13 + đề dự án giữa chặng 1 + Phụ lục D ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 14". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Cụm trọng tâm thứ hai (rò rỉ).

| Buổi | Đọc thử bản cũ | Viết lại | `kiem_de_hieu` | Tự đọc thử + rà gọn | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 13 Feature & chống rò rỉ | ✅ | ✅ | ✅ 44 → 0 | ✅ | ✅ | ✅ 14 tr |
| Đề dự án giữa chặng 1 | — | ✅ | — | ✅ | — | ✅ 5 tr |
| Phụ lục D | — | ✅ | — | ✅ | — | ✅ 7 tr |

Bắt buộc:
- Buổi 13: rò rỉ — mỗi kiểu có ví dụ 6 dòng bảng cho thấy **ô nào nhìn trộm tương lai**
- Đề dự án giữa chặng 1: học viên đọc đề hiểu phải nộp gì, chấm thế nào, không cần hỏi lại; chỉ viết lại đề + rubric
  (ngắn nhất có thể); lỗi cài sẵn và lời giải KHÔNG vào zip
- Phụ lục D: mỗi chỉ số có ví dụ 5 số tính tay + "khi nào dùng / bẫy" bằng lời (Phase 16 mở rộng tiếp)
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

## Kết quả (2026-09-19)

- **Buổi 13**: 6 mục lý thuyết; mỗi kiểu rò rỉ (rolling có tâm, rolling không shift, lag < $h$, z-score, target encoding, nội suy hai phía)
  có bảng 6 dòng in đậm ô nhìn trộm. `code/lab.ipynb` mới (bước 1 in lại các bảng 6 dòng). README, quiz viết lại. Chi tiết: `buoi-13/NGHIEN-CUU.md`.
- **Đề dự án 1**: bỏ ví dụ JSON trùng khít đáp án L1 (lộ 5 điểm), thay bằng ví dụ chỉ minh hoạ định dạng (đã kiểm: không phải lỗi thật);
  tầm dự báo sửa "24 giờ" → "12 giờ (24 bước 30 phút)" cho khớp `TAM = 24` của khung và lời giải; bỏ bảng điểm lặp RUBRIC; gợi ý không còn
  nêu tên tệp/giờ cụ thể; cấm dùng dữ liệu gốc do `lab.py up` tải về để tìm lỗi (diff là ra hết 6 lỗi).
- **Bộ chấm `giam-khao/cham_phat_hien.py`**: trước chỉ cần đúng loại là được 3 điểm, mà đề đã nêu đủ sáu loại → liệt kê bừa sáu loại được
  18/30. Nay một mục chỉ được tính khi đúng loại + đúng tệp + khoảng chồng lên lỗi thật (nới ±3 ngày); còn lại là báo sai −2. Kiểm: liệt kê bừa
  → 0, đáp án đúng → 30. RUBRIC ghi đúng luật mới.
- **Zip** (`dong_goi.py --liet-ke`): có `phat/du-lieu/` (dữ liệu bẩn), loại `giam-khao/` (đáp án lỗi, `tiem_loi.py`, `loi-giai-mau/`).
- **Phụ lục D**: ví dụ 5 số chung (MAE 1,6; RMSE 2,10; MASE 1,07…) + ví dụ riêng cho pinball, Winkler, coverage, WIS, CRPS, Brier, log score,
  skill, Diebold–Mariano; mỗi chỉ số "dùng khi / bẫy"; bỏ trích tiếng Anh; gộp mục "Bẫy thường gặp" vào từng chỉ số. Mục 9 giữ ví dụ đối chiếu
  thư viện (test `tools/tests/` trỏ tới).
