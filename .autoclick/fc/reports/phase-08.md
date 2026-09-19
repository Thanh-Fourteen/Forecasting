# phase 8

_2026-09-18 21:41:25_

Phase 8 đã xong: buổi 4, buổi 5 và Phụ lục C đã viết lại và đạt mọi tiêu chí, đã đánh ✅ ở `todos.md`, `todos/phase-08.md` và `todos/tong-quan.md`. Tôi chưa commit gì.

| | Buổi 4 · Biểu đồ | Buổi 5 · Biến đổi | Phụ lục C |
|---|---|---|---|
| Mục lý thuyết | 11 → 6 | 8 → 6 (sai phân và chuẩn hoá chuyển vào hộp "Nâng cao") | 18 loại hình, mỗi loại đọc theo 5 bước |
| Chữ (ngoài bảng/code) | 2.596 → 6.000 | 2.299 → 4.875 | 3.631 → 4.954 |
| PDF | 12 → 18 trang (đúng trần) | 10 → 15 trang | 9 → 12 trang |
| Cờ của `kiem_de_hieu` | 78 → 0 | 61 → 2 (lý do bên dưới) | 0 |
| Tự đọc thử (chặn / khó) | bản cũ 6 chặn → cuối 0 / 0 | bản cũ 7 chặn → cuối 0 / 0 | không còn chỗ mơ hồ |
| Quiz | viết lại 10 câu, tính lại bằng Python | viết lại 10 câu, tính lại bằng Python | — |

**Buổi 4.** Mỗi hình có đủ khối "Cách đọc hình" 5 bước. Mỗi khái niệm có ví dụ tính tay trước khi vào dữ liệu thật: hai tuần lượt thuê, 7 ngày có một ngày trống, chuỗi lặp 4 bước để tính tay tự tương quan.

**Buổi 5.** Các ví dụ tay đi trước dữ liệu thật như yêu cầu:
- **Log:** 100 → 120 và 1.000 → 1.200 cao bằng nhau trên thang log.
- **Box-Cox:** ví dụ Guerrero ba năm tính tay ra λ = 0,5.
- **Bias khi đổi ngược:** log 0, 1, 2 đổi ngược cho trung vị 2,72, còn trung bình thật là 3,70.

Tôi cũng viết lại mục "Nhắc lại buổi trước" của buổi 5: bản cũ nhắc phân rã, MAE/RMSE, dữ liệu thiếu — những thứ tới buổi 6, 10, 14 mới học.

**Hai số cũ bị sai, đã sửa theo lần chạy thật:**
- Seasonal plot của buổi 4 có 106 tuần, không phải 104.
- λ Yeo-Johnson của buổi 5 là 1,025, không phải 1,091.

**Thay đổi ngoài tài liệu:**
- Code đáp án buổi 4 vẽ thiếu nhãn trục có đơn vị, trong khi buổi này dạy đúng điều đó. Tôi đã thêm nhãn cho mọi hình, và lag plot đổi thành một hàng 4 ô để không vượt 18 trang.
- Buổi 5 thêm hình "dao động theo mức"; bỏ hai hình sai phân và chuẩn hoá vì hai phần này đã chuyển vào hộp "Nâng cao".
- Cả hai buổi có `code/lab.ipynb` và `dap-an/vi_du_nho.py` mới.
- Tôi bỏ dòng `matplotlib.use("Agg")` trong `bieu_do.py`, vì nó làm notebook không hiện hình. Chỗ hở cố ý, bộ chấm, dữ liệu và `00-nen/` giữ nguyên.
- Phụ lục D đang trỏ "Phụ lục C mục 6" cho ACF; tôi đổi thành "mục 8" theo cách đánh số mới.

**Kiểm tra đã chạy:**
- `kiem_tra_lab.py 4 5` đạt từ venv trắng: đáp án xanh 8/8, code đỏ đúng chỗ, notebook chạy hết.
- `kiem_tra_doc_lap.sh 4 5` đạt, và zip phát học viên đã loại đúng `dap-an/` cùng tài liệu nội bộ.
- `ruff` sạch ở buổi 4–5.

**Còn lại, cần anh/chị biết:**
- Buổi 5 còn 2 cờ mật độ số. Đó là dữ liệu đề của hai câu "Tự kiểm tra" (620 tỷ/31 ngày…), không phải đoạn dồn kết quả; lý do đã ghi trong `NGHIEN-CUU.md`.
- `ruff check .` toàn repo vẫn báo 2 lỗi trong `buoi-14/dap-an/ve_hinh.py`. Thư mục đó chưa commit và nằm ngoài phase này nên tôi không đụng vào.
- Việc đọc thử và rà gọn đều do tôi tự làm, không dùng subagent. Phase 11 (đọc thử độc lập trong phiên mới) sẽ kiểm lại bằng mắt người chưa đọc tài liệu.

Nhật ký research, các vòng đọc thử và phần Phụ lục C nằm trong `buoi-04/NGHIEN-CUU.md` và `buoi-05/NGHIEN-CUU.md`.
