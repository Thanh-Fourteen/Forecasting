# phase 7

_2026-09-18 16:40:00_

Phase 7 xong và đã đánh ✅. Chưa commit: khoảng 276 file thay đổi, phần lớn là nền sinh lại cho 17 buổi.

| Tài liệu | Chữ ngoài bảng/code | Trang PDF | Đọc thử cuối (chặn / khó · quiz) |
|---|---|---|---|
| Buổi 1 | 6.910 → 5.538 (−20%) | 19 → 17 | 0 / 5 · 10/10 |
| Buổi 2 | 8.991 → 6.544 (−27%) | 22 → 18 | 0 / 4 · 10/10 |
| Buổi 3 | 7.485 → 5.502 (−26%) | 21 → 17 | 0 / 4 · 10/10 |
| Phụ lục A | 5.441 → 4.064 (−25%) | 19 → 17 | 0 / 5 · Tự kiểm tra 4/4 |
| Phụ lục B | 12.494 → 7.748 (−38%) | 30 → 18 | 0 / 6 · 6/6 |

- Mọi tài liệu đều qua đọc thử lại bằng subagent mới. Phụ lục B vẫn còn 6 chỗ khó ở lần đọc cuối (ngưỡng là 5); tôi đã sửa cả 6 nhưng chưa cho đọc thử lại lần nữa.
- Buổi 2 vượt trần 6.500 chữ đúng 44 chữ; lý do đã ghi trong `NGHIEN-CUU.md`. Mỗi lần ép buổi 2 xuống dưới trần, người đọc thử lại báo khó đúng ở phần lập luận vừa cắt: vì sao chia √n, "95%" là của quy trình, vì sao khối dài làm khoảng hẹp.
- Buổi 1 dừng ở −20%. Phần còn lại là ví dụ tính tay, câu diễn giải công thức và hình, nên không cắt thêm.

**Đọc thử bắt được 3 lỗi do chính việc cắt/sửa gây ra, đã sửa hết:**
- Buổi 1, Lab bước 4: câu "mỗi tuần một phương pháp khác thắng" sai so với chính bảng số.
- Buổi 2, Lab bước 1: con số 72,51% bị trỏ nhầm chỗ.
- Buổi 2: tôi giải thích sai cơ chế ở hộp "biến gây nhiễu".

**Đổi công cụ theo góp ý của bạn:**
- **Bỏ make.** Mỗi buổi chạy bằng `python lab.py up | check | notebook | down`, chạy được cả trên Windows.
- **Phát sẵn `code/lab.ipynb`** cho buổi 1–3. Học viên không cần biết jupytext; notebook tự nạp lại code sau mỗi lần sửa.
- **Dùng được conda.** Bật môi trường Python 3.12 rồi chạy `python lab.py up --pip`, cài từ `requirements.txt` sinh tự động từ `uv.lock`.
- **Chạy thật:** buổi 1–13 đáp án xanh, `code/` đỏ đúng chỗ hở cố ý. Đường `--pip` cho kết quả giống hệt đường uv. Bộ kiểm độc lập đạt.

**Ba đoạn trước/sau để bạn duyệt độ gọn:**

1. Lệnh chạy lab (buổi 1–3, Phụ lục A). Trước là `env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/danh_gia.py`, kèm bốn gạch giải thích từng cờ. Sau là mở notebook rồi chạy ô `%run danh_gia.py`, không phải giải thích gì.

2. Buổi 1, mục 4.5, Đọc bảng:
   > **Trước:** Bảng lịch giống cách A: lệch từng giờ vì nhiễu, nhưng lệch bù trừ khi cộng… Vì sao? Khi cộng lên tuần, phần lệch lúc lên lúc xuống của cả ba cách đều bù trừ. Cái không bù trừ là lệch cùng một chiều kéo dài nhiều ngày. Trung bình 4 tuần chỉ hạ xuống sau khi kỳ nghỉ tháng 8… (5 câu, lần thứ ba giải thích chuyện tháng 8)
   >
   > **Sau:** Cộng lên tuần, lệch lên xuống của cả ba cách đều bù trừ; chỉ **lệch cùng một chiều nhiều ngày** là dồn lại, như hai baseline ở tháng 8.

3. Buổi 3, mục 4.1, Đọc bảng (trước là ba gạch kể lại từng ô):
   > **Sau:** Ngày đổi giờ mùa xuân chỉ có **23 giờ**; ngày mùa thu có **25 giờ**. Một giờ New York không kèm offset ứng với không, một hoặc hai thời điểm UTC; giờ UTC luôn chỉ đúng một thời điểm.

Bài học "tường minh quá cũng là khó hiểu; công cụ phải giải thích dài thì sửa công cụ" đã vào chuẩn D13 và memory. Chuẩn D13 có thêm 2 kiểu "gọn sai" không được làm: bỏ câu kết luận khi đọc hình, và bỏ ngày cụ thể chỉ để qua bộ đếm số.

**Còn lại:**
- Buổi 4–13 chưa có `code/lab.ipynb`; Phase 8–9 sẽ tạo khi viết lại các buổi đó.
- Buổi 11 hiện chỉ 9 trang, dưới ngưỡng tối thiểu 10; đây là bản cũ, Phase 9 viết lại.

Muốn commit thì bạn nói tôi làm.
