# Phase 9 — Viết lại buổi 9–13 + đề dự án giữa chặng 1 + Phụ lục D cho dễ hiểu 🔲

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 9"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Cụm trọng tâm thứ hai (tiền xử lý, khử nhiễu, rò rỉ).

| Buổi | Đọc thử bản cũ | Viết lại | `kiem_de_hieu` | Đọc thử bản mới | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 09 Đặc trưng & khả năng dự báo | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 10 Làm sạch & dữ liệu thiếu | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 11 Ngoại lai & điểm gãy | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 12 Khử nhiễu & miền tần số | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 13 Feature & chống rò rỉ | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Đề dự án giữa chặng 1 | — | 🔲 | 🔲 | 🔲 | — | 🔲 |
| Phụ lục D | — | 🔲 | 🔲 | 🔲 | — | 🔲 |

Bắt buộc:
- Buổi 9: spectral entropy, catch22, DTW, ABC–XYZ — mỗi cái "đo cái gì, bằng lời" + ví dụ 2 chuỗi nhỏ; vì sao đổi
  MASE → sMAPE nói bằng ví dụ số
- Thuật ngữ theo Phụ lục E: buổi 9 bảng đặc trưng ghi "độ lệch" (skewness) → "hệ số lệch"; buổi 11 "đổi mức" → "dịch mức"
- Buổi 10: 7 cách điền — bảng "khi nào dùng / khi nào không" bằng lời thường; "mốc thiếu mà `isna()` không thấy" có
  ví dụ 5 dòng
- Buổi 11: z-score, Hampel, masking, PELT, penalty — ví dụ 10 số tính tay; "masking" giải thích bằng hình
- Buổi 12: tần số, Nyquist, aliasing — trực giác (bánh xe quay ngược trong phim) trước công thức; "bộ lọc nhân quả"
  = chỉ dùng quá khứ, ví dụ trung bình trượt 3 điểm tính tay hai kiểu
- Buổi 13: rò rỉ — mỗi kiểu có ví dụ 6 dòng bảng cho thấy **ô nào nhìn trộm tương lai**
- Đề dự án giữa chặng 1: học viên đọc đề hiểu phải nộp gì, chấm thế nào, không cần hỏi lại
- Phụ lục D: mỗi chỉ số có ví dụ 5 số tính tay + "khi nào dùng / bẫy" bằng lời (Phase 10 mở rộng tiếp)
- Buổi 12 đã có baseline đọc thử (chỗ chặn: MAE/RMSE, phương sai, periodogram, lọc thông thấp, IIR, wavelet, đo trễ
  bằng tương quan, trích `filtfilt`/SavGol/Hamilton tiếng Anh; "10 cấu hình" bộ lọc chưa liệt kê)
- **Gọn (D13)**: viết gọn ngay từ đầu theo bài học Phase 7 — mỗi ý một lần, khuôn D2 là trần, sửa chỗ vướng bằng viết lại câu
  chứ không chèn đoạn; 3.500–6.500 chữ ngoài bảng/code, PDF 10–18 trang; rà gọn bằng biên tập viên (≤ 3 chỗ thừa)
- **Notebook Lab**: tạo `code/lab.ipynb` (soạn bằng `tools/nb.py`, như buổi 1–3), tài liệu chỉ trỏ "ô bước N" + output cần
  đọc; lệnh dùng `python lab.py …`, không giải thích cờ lệnh. `kiem_tra_lab.py` phải chạy notebook xanh
