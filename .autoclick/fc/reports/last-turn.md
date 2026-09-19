# lượt gần nhất

_2026-09-19 11:31:23_

Phase 21 xong: cả 4 buổi đạt, đã commit và push lên `origin/main` (commit `aee1e84`).

| Buổi | Quiz mù | Chặn / khó / nhỏ: trước → sau | Chỗ thừa | Chữ | PDF |
|---|---|---|---|---|---|
| 18 | 10/10 | 1/2/5 → **0/0/2** | 0 | 4.113 → 4.163 | 13 tr |
| 19 | 10/10 | 0/1/4 → **0/0/2** | 0 | 3.679 → 3.691 | 12 tr |
| 20 | 9/10 → câu 5 viết lại | 0/2/3 → **0/0/2** | 0 | 3.901 → 3.933 | 12 tr |
| 21 | 10/10 | 0/2/4 → **0/0/2** | 0 | 3.595 → 3.637 | 12 tr |

**Các sửa chính:**
- **Chỗ chặn duy nhất (buổi 18, Lab bước 2):** học viên phải tự viết `SARIMAX` mà tài liệu không chỉ cú pháp. Nếu không bỏ 13 phần dư đầu, bộ chấm báo đỏ dù đã làm đúng ý bài: Ljung–Box p ra 0,0004, bỏ 13 điểm đầu thì ra 0,64. Tài liệu giờ đưa sẵn lệnh. Buổi 20 (kiểm định Johansen) và buổi 21 (quantile Student-t, tên cột, tên khoá bộ chấm cần) được sửa cùng kiểu.
- **Phép tính tay không khớp số in ra:**
  - Buổi 18: bảng thành phần Prophet cộng ra 1,62 nhưng bài ghi 1,63; nay in 3 chữ số thật.
  - Buổi 18: câu "quý 3 cao hơn quý 1 cùng năm 6 đơn vị" thay số ra 7 vì có cả xu hướng; đã viết lại câu.
  - Buổi 21: phép tính HAR theo hệ số đang in ra 7,59, bài ghi 7,54; đã sửa theo hệ số đang in.
- **Từ chưa định nghĩa:** "năm hoá" và "điểm %" ở buổi 20, "phân loại SBC" ở buổi 19 (câu 10 của quiz dùng từ này), "hệ số chặn" ở buổi 18.
- **Câu 5 quiz buổi 20** hỏi "có đáng lo không" nhưng tài liệu không cho mốc nào để phán, nên tôi đổi thành câu hỏi tính số hệ số.

Bộ kiểm dễ hiểu (`kiem_de_hieu`) báo 0 vi phạm. `kiem_tra_lab` đạt cả 4 buổi: đáp án xanh, `code/` đỏ đúng chỗ hở cố ý, notebook chạy hết. Kiểm tra tự chứa và `ruff` cũng đạt. Chi tiết từng buổi nằm ở mục "Đọc thử độc lập (Phase 21)" trong `NGHIEN-CUU.md`; trạng thái đã đổi sang ✅ ở [todos.md](todos.md), [phase-21.md](todos/phase-21.md) và [tong-quan.md](todos/tong-quan.md).

**Commit lần này gồm cả công việc của các phase 8–20.** Trước đó các phase này chưa được commit (commit gần nhất là `40a3a63`). Trước khi đẩy, tôi đã kiểm danh sách tệp: không có venv, dữ liệu hay tệp bí mật nào, tổng khoảng 27,6 MB, chủ yếu là PDF.
