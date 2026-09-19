# phase 18

_2026-09-19 07:23:53_

Phase 18 đã xong và được đánh dấu ✅ trong `todos.md`, `todos/phase-18.md` và `todos/tong-quan.md`. Cả 5 tài liệu đạt ngưỡng: 0 chỗ chặn, quiz mù đúng 10/10 ở mỗi buổi.

Tôi làm quiz mù trước (chỉ đọc `tai-lieu.md` và bản quiz đã bỏ đáp án), rồi mới mở đáp án để chấm. Mọi con số và đáp án đều tính lại bằng Python, không có đáp án nào sai.

| Tài liệu | Chặn / khó / nhỏ: trước → sau | Quiz mù | Chữ trước → sau | Trang |
|---|---|---|---|---|
| Buổi 14 | 0/1/5 → 0/0/3 | 10/10 | 3.971 → 4.014 | 16 |
| Buổi 15 | 0/1/5 → 0/0/2 | 10/10 | 4.013 → 4.052 | 12 |
| Buổi 16 | 0/0/4 → 0/0/2 | 10/10 | 3.602 → 3.608 | 11 |
| Buổi 17 | 0/1/4 → 0/0/1 | 10/10 | 3.579 → 3.622 | 11 → 12 |
| Phụ lục D (phần mở rộng) | 0/0/3 → 0/0/1 | không có quiz | — | 8 |

**Ba chỗ khó đã sửa bằng cách viết lại câu:**
- **Buổi 14:** "khoảng dự báo" chưa được định nghĩa ở buổi nào từ 1 tới 14, trong khi buổi 16–17 dùng rất nhiều. Tôi thêm định nghĩa ở mục 4.2 và chuyển câu nhắc lại của buổi 16 sang nhóm "Từ buổi 5–6 và 14".
- **Buổi 15:** thiếu mắt xích "sai số chuẩn = căn của (phương sai / n) khi các số độc lập". Không có nó thì ví dụ Diebold–Mariano (DM) bị nhảy bước. Đã thêm vào mục "Nhắc lại buổi trước".
- **Buổi 17:** câu giải thích vì sao ACF có cột ở trễ 11 và 13 ("hai gai nhân vào nhau") bị nhảy bước. Đã viết lại thành lời giải thích trực giác.

**Chỗ nhỏ đáng chú ý:**
- Kết luận hình ở buổi 15 viết "hai cách lệch như nhau", nhưng số thật là −11,8% và −15,5%. Đã sửa thành "12–16%".
- Buổi 15 có hai con số 1.944 MW trùng nhau, dễ tưởng chép nhầm. Tôi đã kiểm trong `NGHIEN-CUU.md`: trùng tình cờ (1.944,39 và 1.944,43), nên ghi chú ngay dưới bảng.
- Còn lại là sửa thuật ngữ và ký hiệu: dùng "tổng có trọng số" thay cho "tổ hợp", ký hiệu $Q_m$ trong Lab buổi 17, giải nghĩa "mức danh nghĩa", và nói rõ "trộn" trong Phụ lục D.

**Rà gọn:** chỉ tìm thấy một chỗ thừa đáng kể (một "Đọc bảng" ở buổi 14 chỉ đọc lại hai ô số), đã viết lại thành câu nêu lý do.

**Kiểm tra sau khi sửa:** tất cả đều qua.
- `ruff` sạch, `kiem_de_hieu.py 14–17` 0 vi phạm.
- `kiem_tra_lab.py 14 15 16 17` đạt: đáp án xanh, `code/` đỏ đúng ch�ỗ hở, notebook chạy hết.
- `kiem_tra_doc_lap.sh --nhanh` đạt (bản nhanh, bỏ bước `uv lock --check`).
- PDF xuất lại cho bốn buổi và Phụ lục D.

Chi tiết (bảng A–E, ví dụ tự nghĩ, căn cứ từng câu quiz) nằm ở mục "Đọc thử độc lập (Phase 18)" trong `buoi-14..17/NGHIEN-CUU.md`; phần Phụ lục D ghi trong `buoi-14/NGHIEN-CUU.md`. Tôi chưa commit. Phase tiếp theo là 19 (buổi 18–19).
