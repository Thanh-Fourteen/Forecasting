# phase 9

_2026-09-18 22:28:02_

Phase 9 đã xong: buổi 6 và buổi 7 viết lại, đạt mọi tiêu chí, đã đánh ✅ ở `todos.md`, `todos/phase-09.md`, `todos/tong-quan.md`. Chưa commit gì.

| | Buổi 6 · Phân rã | Buổi 7 · Tự tương quan & tính dừng |
|---|---|---|
| Mục lý thuyết | 8 → 6 (X-13 chuyển vào hộp "Nâng cao") | 8 → 6 (ergodic chuyển vào hộp "Nâng cao") |
| Chữ (ngoài bảng/code) | 2.368 → 4.809 | 2.131 → 4.922 |
| PDF | 11 → 16 trang | 10 → 15 trang |
| Cờ của `kiem_de_hieu` | 66 → 0 | 64 → 0 |
| Tự đọc thử (chặn / khó) | bản cũ 6 chặn → cuối 0 / 0 | bản cũ 7 chặn → cuối 0 / 0 |
| Quiz | viết lại 10 đáp án, tính lại bằng Python | viết lại 10 đáp án, sửa câu 5 |

**Các yêu cầu của phase:**
- **Buổi 6:** có ví dụ 12 quý tự phân rã bằng tay. Tôi chọn số để mùa vụ ra số nguyên (4, −3, −7, 6), khớp `seasonal_decompose`. Cũng trên 8 quý đó, $F_T$ và $F_S$ được tính tay và nói bằng lời. Trọng số robust tính tay trên 5 phần dư.
- **Buổi 7:** mỗi phần có ví dụ tính tay đi trước công thức:
  - ACF: $r_1$, $r_2$ trên 6 số.
  - PACF: dùng ví dụ tin đồn A → B → C và công thức cho trễ 2.
  - Ljung-Box: tính $Q^*$ bằng tay.
  - Tính dừng: ba ví dụ đời thường (máy lạnh, chiều cao trẻ, người tung đồng xu) và random walk tính tay.
  - ADF: ví dụ "đang cao thì bước sau có bị kéo xuống không".
  - ADF × KPSS: bảng 2 × 2 có câu "nghĩa là gì" cho từng ô.
- **Quiz buổi 7 câu 5:** đổi sang chuỗi có trung bình tròn (2, 4, 6, 8, 6, 4, 2, 0 → $r_1$ = 0,5). Mục này trong `phan-hoi-hoc-vien.md` đã đánh ✅.

**Lệch so với prompt:** prompt yêu cầu đưa p-value và kiểm định vào hộp "Mượn trước". Buổi 2 đã dạy đủ phần này, nên theo quy tắc D5 tôi nhắc lại ở mục 2 "Nhắc lại buổi trước". Hộp "Mượn trước" chỉ dùng cho hai thứ chưa dạy: nghiệm đơn vị và phân phối $\chi^2$.

**Chạy lại phát hiện ba lỗi trong bản cũ:**
1. **Lượt thuê theo ngày (buổi 7)** tạo chuỗi bằng `.dropna()`, nên 76 ngày bị rút khỏi giữa chuỗi. Vì vậy `diff(7)` và ACF đang so những ngày không cách nhau 7 ngày.
   - Trên lưới ngày liên tục thì **không có đỉnh ở trễ 7**, trái với câu cũ "chỉ còn đỉnh ở 7, 14, 21".
   - Tôi thay bằng bảng sai phân **theo giờ**: độ lệch chuẩn 1,43 → 0,643 (sai phân thường, mùa vụ vẫn còn) → 0,589 (sai phân mùa vụ 168) → 0,427 (sai phân 168 rồi sai phân thường).
   - Script hình đã sửa theo lưới ngày liên tục.
2. **Đợt nắng nóng (buổi 6):** bản cũ đo bằng một STL riêng, khác code của buổi. Tôi đo lại bằng đúng MSTL của lab: phần dư lớn nhất 11.364 MW (không robust) và 22.576 MW (robust).
3. **Bài tập 3 buổi 6** ghi "hai năm (8.784 giờ)", thật ra đó là một năm. Đã sửa đề.

**Thay đổi ngoài tài liệu:**
- Mọi hình buổi 7 thêm nhãn trục có đơn vị.
- Cả hai buổi có `code/lab.ipynb` và `dap-an/vi_du_nho.py` mới.
- Chỗ hở cố ý, bộ chấm, dữ liệu và `00-nen/` giữ nguyên.

**Kiểm tra đã chạy:**
- `kiem_tra_lab.py 6 7` đạt từ venv trắng: đáp án xanh 7/7 và 9/9, code đỏ đúng chỗ, notebook chạy hết.
- `kiem_tra_doc_lap.sh 6 7` đạt.
- `ruff` sạch ở buổi 6–7.

Việc đọc thử và rà gọn đều do tôi tự làm, không dùng subagent. Phase 11 (đọc thử độc lập trong phiên mới) sẽ kiểm lại cụm buổi 4–8. Chi tiết từng vòng nằm trong `buoi-06/NGHIEN-CUU.md` và `buoi-07/NGHIEN-CUU.md`.
