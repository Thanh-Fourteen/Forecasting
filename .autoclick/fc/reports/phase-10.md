# phase 10

_2026-09-18 22:40:33_

Phase 10 đã xong: buổi 8 viết lại, đạt mọi tiêu chí, đã đánh ✅ ở `todos.md`, `todos/phase-10.md` và `todos/tong-quan.md`. Chưa commit gì.

| Buổi 8 · Tương quan giữa các chuỗi | Trước | Sau |
|---|---|---|
| Mục lý thuyết | 9 | 6: hệ số tương quan + bộ Anscombe, rồi 5 tình huống |
| Chữ (ngoài bảng/code) | 2.747 | 5.010 |
| PDF | 10 trang | 15 trang |
| Cờ của `kiem_de_hieu` | 70 | 0 |
| Tự đọc thử (chặn / khó) | 7 chặn | 0 / 0 |

**Theo yêu cầu của prompt:**
- Mỗi tình huống đi theo thứ tự câu hỏi → hình → con số, và kết bằng nhãn "**Cái bẫy trong một câu**". Bộ Anscombe ở mục 4.1 cũng có nhãn này.
- Mỗi khái niệm có ví dụ tính tay trước công thức:
  - Pearson/Spearman: $y = x^2$ và chữ U, tính tay ra Pearson = 0.
  - Tương quan giả: hai chuỗi 5 tháng, $r$ trên mức 0,974 nhưng $r$ của các bước là −1. Durbin–Watson tính tay trên hai dãy phần dư.
  - Mutual information: bảng lạnh/vừa/nóng, Pearson = 0 nhưng MI = 0,637 nat, tính từng ô.
  - Prewhitening: random walk 12 điểm, $y$ chậm 2 bước. Tương quan chéo thô trải rộng (0,42 / 0,77 / 0,37). Sau khi lọc chỉ còn một đỉnh 0,91, thấy được bằng cách đặt thẳng hai dòng bước.
  - Tương quan trượt: cửa sổ mùa đông −1, mùa hè +1, gộp lại chỉ 0,48.
  - Granger: so hai cách dự báo trên 6 số, tổng bình phương sai số 38 so với 0.
- Ex-ante gộp vào tình huống Granger. VIF và tương quan một phần chuyển vào hộp "Nâng cao".

**Sửa một số trong bản cũ:** $R^2$ theo CDD + HDD đúng tại mốc 18,33 °C là **0,812**. Bản cũ ghi 0,813 vì script hình lấy $R^2$ ở điểm lưới gần mốc nhất chứ không đúng mốc. Tôi đã sửa script, tài liệu và quiz. Lúc thay số, lệnh `sed` đổi nhầm cả $r_{24}$ = 0,813 của buổi 4 trong Phụ lục C; tôi đã trả lại ngay.

**Thay đổi ngoài tài liệu:**
- Quiz viết lại cả 10 đáp án: nói vì sao đúng, vì sao từng lựa chọn sai, bỏ các câu trích tiếng Anh.
- Có `code/lab.ipynb` mới (chạy hết trong 8 giây) và `dap-an/vi_du_nho.py`.
- Chỗ hở cố ý, bộ chấm, dữ liệu và `00-nen/` giữ nguyên.

**Kiểm tra đã chạy:**
- `kiem_tra_lab.py 8` đạt từ venv trắng: đáp án xanh 10/10, code đỏ đúng 3 chỗ hở, notebook chạy hết.
- `kiem_tra_doc_lap.sh 8` đạt, `ruff` sạch.
- Đã xuất lại PDF buổi 8 và Phụ lục C; xem trực tiếp trang có bảng MI thì phân số và công thức trong ô bảng hiển thị đúng.

Việc đọc thử và rà gọn đều do tôi tự làm, không dùng subagent. Cụm buổi 4–8 giờ đã viết lại xong. Phase tiếp theo là Phase 11: đọc thử độc lập buổi 4–8 và Phụ lục C, cần chạy trong một phiên mới (`/clear`) để có con mắt chưa quen tài liệu.
