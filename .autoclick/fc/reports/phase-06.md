# phase 6

_2026-09-18 12:12:15_

Phase 6 xong: buổi 1, 2, 3 và Phụ lục A, B đều đạt ngưỡng đọc thử (0 chỗ chặn, tối đa 5 chỗ khó).

Người đọc thử là một agent mới, đóng vai học viên chỉ biết Python cơ bản và toán phổ thông. Chỗ "chặn" là chỗ không hiểu thì không đọc tiếp được; chỗ "khó" là chỗ phải đoán mới theo được.

| Phần | Bản cũ (chặn / khó / quiz) | Bản mới | Số vòng đọc thử | PDF |
|---|---|---|---|---|
| Buổi 1 | 9 / 21 / 10/10 | **0 / 5** / 10/10 | 2 | 19 trang |
| Buổi 2 | 11 / 25 / 9/10 | **0 / 4** / 10/10 | 6 | 22 trang |
| Buổi 3 | 4 / 23 / 10/10 | **0 / 5** / 10/10 | 1 | 21 trang |
| Phụ lục A | — | **0 / 3** | 3 | 19 trang |
| Phụ lục B | — | **0 / 3**, tự kiểm tra 16/16 | 4 | 30 trang |

Kiểm tra cuối đều qua: `dap-an/` xanh, `code/` vẫn đỏ đúng chỗ hở cố ý, cả 3 buổi tự chứa, PDF trong khoảng 12–24 trang. Ruff chỉ còn 2 lỗi, đều trong bản nháp buổi 14 chưa commit.

**Các buổi thay đổi thế nào:**
- **Buổi 1:** 10 mục lý thuyết gom còn 6. Ký hiệu MAE và "gốc dự báo T" có ví dụ bằng giờ cụ thể. "TB 4 tuần" đổi thành "trung bình 4 tuần" ở cả tài liệu, code và bộ chấm.
- **Buổi 2:** giờ dạy đủ khối thống kê nền mà đọc thử báo chặn ở mọi buổi: phương sai, độ lệch chuẩn, tương quan, kiểm định, p-value, và vì sao bootstrap đúng. Phần Poisson, AIC và thang log đã bỏ.
- **Buổi 3:** định nghĩa UTC và hậu tố "Z", có bảng đối chiếu giờ New York ↔ UTC cho hai ngày đổi giờ, và một hình trục thời gian mới.
- **Phụ lục B:** là nơi tra cứu 16 khái niệm thống kê, mỗi khái niệm có ví dụ tính tay. Code của từng mục chạy được riêng.

**Lỗi nội dung tìm ra nhờ đọc thử (đã kiểm lại bằng chạy thật rồi sửa):**
- Buổi 2: hệ số lệch ghi 1,61, nhưng làm đúng theo lời tài liệu thì ra 1,35.
- Buổi 2: lời giải thích "vì sao block bootstrap không đạt 95%" bị sai.
- Buổi 3: câu "lệch 4 giờ tháng 3–11" mâu thuẫn với lịch đổi giờ (thật ra chỉ từ 10/3 tới 3/11).
- Buổi 3: con số "747 nhóm giờ" không có giải thích (thật ra là 743 giờ trong tháng + 4 giờ lạ).
- Phụ lục B: có 3 con số sai.

**Những thứ tôi đã đổi mà bạn nên biết:**
- **Nới trần độ dài** thành 4.000–9.000 chữ, đếm phần chữ ngoài bảng và code (mã kiểm `do_dai` trong `kiem_de_hieu.py`). Trần cũ 7.000 chữ buộc phải bỏ đúng những đoạn đang gỡ chỗ chặn.
- **Buổi 2 trỏ sang Phụ lục B** cho các phần chứng minh chi tiết. Đọc thử vòng 4, 5, 6 xác nhận thiếu phụ lục vẫn theo được ý chính của buổi.
- **Đoạn "khối dài làm khoảng hẹp" ở buổi 2** giờ nói thẳng rằng lý do đầy đủ cần toán vượt tầm buổi này, thay vì một lời giải thích nửa vời.
- **Buổi 2 có 3 hình cũ không còn dùng:** `phan-phoi-luot-thue`, `khoang-2011-2012`, `ty-le-phu-kich-ban`. Chúng vẫn được `ve_hinh.py` sinh ra. Nếu bạn muốn, tôi xoá cho gọn.
- **Chưa commit gì.** Nếu bạn đang học từ bản copy trong thư mục học riêng, nên chép lại PDF buổi 1–3 và Phụ lục A, B mới.

Bài học ghi vào `todos/phase-06.md` cho Phase 7–8: với buổi dày khái niệm, thêm giải thích chỉ làm bài dài thêm; cách hiệu quả là cắt chi tiết chứng minh sang phụ lục và nói thẳng giới hạn. Phase tiếp theo là Phase 7: viết lại buổi 4–8 và Phụ lục C, gồm cả việc sửa đáp án sai ở câu 5 quiz buổi 7.
