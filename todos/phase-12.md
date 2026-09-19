# Phase 12 — Viết lại buổi 9–10 ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 12". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Cụm trọng tâm thứ hai (tiền xử lý, khử nhiễu, rò rỉ).

| Buổi | Đọc thử bản cũ | Viết lại | `kiem_de_hieu` | Tự đọc thử + rà gọn | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 09 Đặc trưng & khả năng dự báo | ✅ 10 chặn | ✅ 6 mục + notebook | ✅ 52 → 0 | ✅ 0 chặn / 0 khó | ✅ 10/10 | ✅ 10 → 17 tr |
| 10 Làm sạch & dữ liệu thiếu | ✅ 8 chặn | ✅ 6 mục + notebook | ✅ 51 → 0 | ✅ 0 chặn / 0 khó | ✅ 10/10 | ✅ 10 → 14 tr |

Bắt buộc:
- Buổi 9: spectral entropy, catch22, DTW, ABC–XYZ — mỗi cái "đo cái gì, bằng lời" + ví dụ 2 chuỗi nhỏ; vì sao đổi
  MASE → sMAPE nói bằng ví dụ số; bảng đặc trưng ghi "hệ số lệch" (không "độ lệch") theo Phụ lục E
- Buổi 10: 7 cách điền — bảng "khi nào dùng / khi nào không" bằng lời thường; "mốc thiếu mà `isna()` không thấy" có
  ví dụ 5 dòng
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

Kết quả (2026-09-18): chi tiết ở `buoi-09/NGHIEN-CUU.md`, `buoi-10/NGHIEN-CUU.md` mục "Research viết lại", "Đọc thử (Phase 12)". Sửa code
buổi 9 (không phải chỗ hở): STL trên chuỗi z-score để spike/độ dốc/độ cong không đổi theo đơn vị; bản đồ PCA không còn nhận cột sai số và
đặc trưng quy mô (PC1 + PC2 ~45% → 56%); `do_lech` → `he_so_lech`. `kiem_tra_lab.py 9 10`, `kiem_tra_doc_lap.sh 9 10`, ruff buổi 9–10: đạt.
