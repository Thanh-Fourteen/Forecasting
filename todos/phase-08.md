# Phase 8 — Viết lại buổi 4–8 + Phụ lục C cho dễ hiểu 🔲

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 8"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Cụm trọng tâm của người dùng (đọc biểu đồ, tương quan) — **khó hiểu ở đây là mất giá trị lớn nhất của khoá**.

| Buổi | Đọc thử bản cũ | Viết lại | `kiem_de_hieu` | Đọc thử bản mới | Quiz giải thích | PDF |
|---|---|---|---|---|---|---|
| 04 Đọc & vẽ biểu đồ | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 05 Biến đổi & điều chỉnh | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 06 Phân rã | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 07 Tự tương quan & tính dừng | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 08 Tương quan giữa các chuỗi | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Phụ lục C | — | 🔲 | 🔲 | 🔲 | — | 🔲 |

Bắt buộc:
- Mọi hình: khối "Cách đọc hình" đủ 5 bước (D8) — đây là kỹ năng buổi 4 dạy, tài liệu phải làm mẫu đúng nó
- Buổi 5: log, Box-Cox, bias khi đổi ngược — ví dụ 3–5 số tính tay trước
- Buổi 6: xu hướng/mùa vụ/phần dư — ví dụ chuỗi 12 điểm tự phân rã bằng tay; $F_T, F_S$ nói bằng lời
- Buổi 7: ACF/PACF — tính tay tự tương quan trễ 1 trên 6 số; "dừng" bằng ví dụ đời thường; ADF vs KPSS bằng bảng 2×2
  có câu "nghĩa là gì" từng ô; giả thuyết không/p-value → "Mượn trước" nếu buổi 2 chưa dạy đủ
- Buổi 8: 5 tình huống tương quan — mỗi tình huống: câu hỏi → hình → con số → **cái bẫy nói bằng một câu**;
  prewhitening, mutual information, Granger giải thích bằng trực giác trước công thức
- Phụ lục C: mỗi loại biểu đồ theo đúng khuôn "Cách đọc hình"
- **Quiz buổi 7 câu 5 có đáp án sai** ($\bar y$ = 52/9, không phải 6; $r_1 ≈ 0{,}020$) — sửa, và kiểm lại mọi câu tính
  toán trong quiz buổi 4–8 bằng Python. Buổi 7 đã có baseline đọc thử (chỗ chặn: kiểm định/H0/p-value, nghiệm đơn vị,
  AR(1), trích Zivot/Nau tiếng Anh; ngưỡng sai phân thừa −0,5 hay −0,45 không thống nhất)
- **Gọn (D13)**: viết gọn ngay từ đầu theo bài học Phase 7 — mỗi ý một lần, khuôn D2 là trần, sửa chỗ vướng bằng viết lại câu
  chứ không chèn đoạn; 3.500–6.500 chữ ngoài bảng/code, PDF 10–18 trang; rà gọn bằng biên tập viên (≤ 3 chỗ thừa)
- **Notebook Lab**: tạo `code/lab.ipynb` (soạn bằng `tools/nb.py`, như buổi 1–3), tài liệu chỉ trỏ "ô bước N" + output cần
  đọc; lệnh dùng `python lab.py …`, không giải thích cờ lệnh. `kiem_tra_lab.py` phải chạy notebook xanh
