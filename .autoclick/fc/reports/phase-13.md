# phase 13

_2026-09-19 00:06:13_

Xong Phase 13: đã viết lại buổi 11 và 12, và đánh ✅ ở `todos.md`, `todos/phase-13.md`, `todos/tong-quan.md`. Chưa commit.

| Buổi | Chặn (bản cũ → mới) | Khó | Cờ `kiem_de_hieu` | Quiz | Số chữ | PDF |
|---|---|---|---|---|---|---|
| 11 Ngoại lai & điểm gãy | 10 → **0** | 0 | 56 → **0** | 10/10 | 2.343 → 4.204 | 9 → 13 trang |
| 12 Khử nhiễu & miền tần số | 9 → **0** | 0 | 57 → **0** | 10/10 | 2.626 → 4.140 | 10 → 13 trang |

**Buổi 11:**
- Một dãy 10 số dùng xuyên suốt để tính tay:
  - z-score của số 50 chỉ là 2,84 nên ngưỡng 3 không bắt được; với 10 số, z không bao giờ vượt nổi 2,85;
  - thêm một số 60 thì z của 50 tụt còn 1,61 (masking);
  - điểm MAD của số 50 là 25,6, bị bắt ngay;
  - ví dụ PELT tính tay: chi phí 254 → 4 → 3,17, và chỉ cắt khi mức giảm chi phí lớn hơn penalty.
- Có hình mới `masking-10-so.png` để giải thích masking bằng hình.
- "Đổi mức" đã đổi thành "dịch mức" ở cả tài liệu lẫn code.
- Buổi 9 trang cũ lên 13 trang là do thêm nội dung theo yêu cầu, không phải độn chữ.

**Buổi 12:**
- Giải thích bằng hình ảnh bánh xe quay ngược trong phim trước khi đưa công thức, kèm một ví dụ aliasing tính tay.
- "Bộ lọc nhân quả" được giải thích bằng trung bình trượt 3 điểm tính tay hai kiểu: đổi số cuối thì kiểu có tâm sửa luôn cả quá khứ.
- Liệt kê đủ 10 cấu hình bộ lọc.
- Rút từ 10 mục lý thuyết xuống 6.

**Sửa lại cho khớp số chạy thật:**
- Buổi 11:
  - Bản `code/` của `doi_phuong_sai` thật ra **bắt hụt** (trả danh sách rỗng), không phải "cảnh báo rải khắp nơi" như tài liệu cũ ghi. Tôi đã sửa phần mô tả triệu chứng, bước Lab và README.
  - Cột sai số của phần so sánh ba cách xử lý COVID đã đổi dấu theo quy ước của khoá (sai số = thực tế − dự báo).
- Buổi 12:
  - Bản `code/` đầu buổi hỏng 6/8 test, không phải 2/8 như tài liệu cũ ghi.
  - Tài liệu giờ gọi đúng tên hàm code thật dùng (`sosfilt`/`sosfiltfilt`).

**Kiểm tra:** `kiem_tra_lab.py 11 12` đạt: đáp án xanh, `code/` đỏ đúng chỗ hở, notebook chạy hết. `kiem_tra_doc_lap.sh 11 12` đạt, ruff sạch cho buổi 11–12. Tôi xem trực tiếp các trang PDF có công thức và bảng, hiển thị đúng. Mọi ví dụ và đáp án quiz đã tính lại bằng Python.

Chi tiết từng vòng đọc thử và phần research nằm trong `buoi-11/NGHIEN-CUU.md` và `buoi-12/NGHIEN-CUU.md`.
