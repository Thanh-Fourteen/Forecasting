# Phản hồi của người học — những đoạn khó hiểu

Ghi lại mỗi khi đọc tài liệu mà phải tra ngoài (Google, ChatGPT…) mới hiểu. Mọi phase soạn hoặc viết lại
buổi học **đọc file này trước**, sửa xong thì điền cột "Đã xử lý".

Khuôn một mục:

```text
### Buổi NN, mục X.Y — <tên mục>
- Câu/đoạn gây khó: "<trích nguyên văn>"
- Không hiểu gì: <từ nào, bước nào, vì sao>
- Đã phải hỏi/tra: <câu đã hỏi, câu trả lời giúp hiểu là gì>
- Đã xử lý: 🔲  (khi sửa: ✅ + phase + ngày)
```

---

### Buổi 01, mục 4.8 — Dự báo điểm, khoảng, phân phối — và chi phí lệch

- Câu/đoạn gây khó: "quyết định ở ô 6 có chi phí lệch: thiếu 1 kWh mất 4, thừa 1 kWh mất 1. Nếu … là phân phối
  của lượng điện, lượng mua tốt nhất là quantile … — kết quả kinh điển của bài toán người bán báo (newsvendor)";
  "quantile 0,8 của sai số là +0,455 kWh. Cộng con số đó vào dự báo TB 4 tuần cho năm 2010".
- Không hiểu gì:
  1. "Thiếu" là thiếu gì — thiếu so với cái gì?
  2. Quantile là gì?
  3. "Quantile 0,8 của sai số = +0,455 kWh" nghĩa là gì, vì sao đem cộng vào dự báo?
  4. Vì sao lại là quantile 0,8?
  5. Công thức bị mất khi copy từ PDF ("Nếu  là phân phối…", "lượng mua tốt nhất là quantile  —") nên câu
     còn lại không đọc được.
- Đã phải hỏi/tra: ChatGPT. Câu trả lời giúp hiểu:
  1. Thiếu = lượng điện mua/dự báo **ít hơn** nhu cầu thực. Ví dụ nhu cầu 10 kWh, mua 8 kWh → thiếu 2 kWh.
     Thiếu đắt (4/kWh) hơn thừa (1/kWh) nên nên dự báo cao hơn trung bình một chút.
  2. Quantile 0,8 = mốc mà khoảng 80% giá trị nằm dưới, 20% nằm trên. Ví dụ dãy 1, 2, 3, 4, 5 → quantile 0,8
     khoảng 4,2 (tuỳ cách tính).
  3. Lấy các sai số của năm 2009, 80% sai số nhỏ hơn +0,455 kWh. Cộng 0,455 vào dự báo năm 2010 là dịch dự báo
     lên để ít bị thiếu hơn.
  4. Quantile tối ưu = chi phí thiếu / (chi phí thiếu + chi phí thừa) = 4 / (4 + 1) = 0,8.
- Nguyên nhân (rút ra 2026-09-18): dùng khái niệm chưa dạy (quantile — buổi 2 mới dạy); không định nghĩa từ
  mới; nói lửng "thiếu"; ý chính nằm trong công thức; trích tiếng Anh chen giữa; nhiều con số dồn một đoạn.
  → Thành quy tắc D1–D12 trong `todos/quy-uoc.md` (mục "Chuẩn dễ hiểu").
- Đã xử lý: ✅ Phase 5, 2026-09-18 — mục 4.8 viết lại làm bài mẫu (`tools/CHUAN-DE-HIEU.md`): hộp "Mượn trước"
  định nghĩa phân phối/quantile/trung vị; ví dụ 10 ngày tính tay; "vì sao 0,8" bằng phép tăng từng kWh; quy ước dấu
  sai số; câu nối "+0,455 = mua ở quantile 0,8"; "Cách đọc hình" 5 bước. Ô 6 ở mục 4.3 sửa cho khớp ("4 đồng/kWh"
  thay "≈ 4 lần"). PDF có lớp chữ ẩn nên copy công thức ra không còn mất. Đọc thử bằng subagent mới: 0 chỗ chặn.
  Phase 6 (2026-09-18): cả buổi 1 viết lại (bảng "Từ mới", 6 khái niệm), đọc thử 0 chặn / 5 khó. ✅ xong.

### Buổi 07, kiem-tra.md câu 5 — đáp án sai (phát hiện khi đọc thử, Phase 5)

- Câu/đoạn gây khó: "Chuỗi $y = [4, 6, 8, 6, 4, 6, 8, 6, 4]$. Tính $r_1$" — đáp án ghi $\bar y = 6$, $r_1 = 0$.
- Không hiểu gì: tổng dãy là 52, trung bình 52/9 ≈ 5,78, không phải 6. Tính đúng: $r_1 ≈ 0{,}020$, $r_2 ≈ −0{,}800$
  (kiểm bằng Python 2026-09-18). Học viên làm đúng sẽ tưởng mình sai.
- Đã phải hỏi/tra: subagent đọc thử tự tính ra 0,020.
- Đã xử lý: 🔲 (Phase 8 — sửa đề cho trung bình tròn, hoặc sửa đáp án; kiểm lại mọi câu tính của quiz 1–13 bằng Python)

### Buổi 01–03, Phụ lục A, B — cả tài liệu — dài dòng (2026-09-18)

- Câu/đoạn gây khó: toàn bộ bản viết lại ở Phase 6.
- Không hiểu gì: không phải khó hiểu mà **dài dòng** — dễ hiểu hơn bản cũ nhưng đọc lâu, nhiều đoạn nói lại ý đã có.
  Yêu cầu: "viết dễ hiểu nhưng không được dài dòng".
- Đã phải hỏi/tra: —
- Đã xử lý: 🔲 (Phase 7 — chuẩn "gọn" D13, rút gọn buổi 1–3 + Phụ lục A, B; mọi phase sau viết gọn ngay từ đầu)
