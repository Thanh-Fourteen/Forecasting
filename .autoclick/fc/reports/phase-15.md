# phase 15

_2026-09-19 05:28:31_

Phase 15 xong. Cả 7 tài liệu đều đạt: 0 chỗ chặn, quiz mù 50/50. Tôi đã đánh dấu ✅ ở `todos.md`, `todos/phase-15.md` và `todos/tong-quan.md`. Chưa commit.

| Tài liệu | Quiz mù | Chặn / khó / nhỏ (lúc đọc mù → sau sửa) | Chữ | PDF |
|---|---|---|---|---|
| Buổi 09 | 10/10 | 0 / 1 → 0 / 5 → 1 | 5.567 → 5.586 | 17 tr |
| Buổi 10 | 10/10 | 0 / 0 / 3 → 1 | 4.589 → 4.601 | 14 tr |
| Buổi 11 | 10/10 | 0 / 0 / 6 → 1 | 4.204 → 4.261 | 13 tr |
| Buổi 12 | 10/10 | 0 / 1 → 0 / 4 → 1 | 4.140 → 4.161 | 13 tr |
| Buổi 13 | 10/10 | 0 / 3 → 0 / 3 → 2 | 4.042 → 4.100 | 14 tr |
| Đề dự án giữa chặng 1 | — | 2 chỗ mơ hồ → 0 | — | 5 tr |
| Phụ lục D | — | 0 / 2 → 0 / 4 → 2 | — | 7 tr |

**Lỗi đáng chú ý nhất: `kiem_nhieu_muc_tieu` ở buổi 13 không làm đúng việc tài liệu nói.** Hàm này có mặt ở cả `code/` và `dap-an/`. Nó so sai vùng dòng nên không bắt được lag nhỏ hơn tầm dự báo: tôi thử `lag_1` với h = 24 thì nó báo sạch. Tôi sửa theo bản đúng trong `tools/khung/ro_ri.py`, giữ lại các dòng có thời điểm ra dự báo t − h trước mốc. Sau khi sửa, h = 24 bắt được `lag_1` và rolling không shift, còn feature hợp lệ không bị báo nhầm. Hàm này không phải chỗ hở cố ý nên tôi sửa ở cả hai bản. Đáp án Tự kiểm tra mục 4.5 cũng ghi sai chiều ("23 giờ trước mốc"), đã sửa luôn.

**Các sửa khác** (đều viết lại câu, mỗi buổi thêm 12–58 chữ):
- **Từ chưa định nghĩa:**
  - "backtest" dùng mà chưa định nghĩa ở buổi 10, 12, 13.
  - "feature/mục tiêu" chưa định nghĩa ở buổi 12, đã thêm vào bảng "Từ mới".
  - "số lần cắt trung bình" chưa định nghĩa ở buổi 9.
- **Chỗ mâu thuẫn ở buổi 13:**
  - Câu "sáng ngày 3 dự báo ngày 5" mâu thuẫn với bảng lag, đã đổi thành "tối ngày 3".
  - Mục 4.6 khuyên "huấn luyện bằng bản dự báo", nhưng số thật cho dự báo trước 3 ngày lại tệ hơn (+2,92% so với +2,20%). Đã ghi rõ bản dự báo đó quá kém, huấn luyện kiểu nào cũng hại, nên bỏ feature này.
- **Đề dự án 1:**
  - Đề đòi kiểm nhiễu mục tiêu nhưng khung không có hàm này, và không nói in kết quả ở đâu.
  - Baseline không nói so với gì, trên tập kiểm nào.
  - Đã ghi rõ cả hai trong đề và RUBRIC. Tôi cũng thêm hàm đúng vào lời giải mẫu: bộ chấm vẫn xanh 8/8, và cả hai bài kiểm rò rỉ đều sạch.
- **Phụ lục D:**
  - Thêm dòng giải thích ký hiệu cho 𝟙 (Winkler) và F, Φ, φ (CRPS).
  - Sửa lỗi PDF in ra "\0,04" ở ví dụ Brier.
- **Số sai lặt vặt:** "min(1, 0, 0)" ở buổi 9 (đúng là 1, 1, 0), độ lệch chuẩn "0,9" ở buổi 11 (thật là 0,97).

Mọi con số ví dụ và đáp án quiz của cả 7 tài liệu tôi đã tính lại bằng Python; chỉ lệch ở những chỗ đã nêu trên, và đều đã sửa.

**Kiểm tra máy:**
- `kiem_tra_lab.py 9–13` đạt: đáp án xanh, `code/` đỏ đúng chỗ, notebook chạy hết.
- `kiem_tra_doc_lap.sh` đạt cho cả 5 buổi.
- `kiem_de_hieu.py` báo 0 vi phạm.
- `ruff` sạch.

Chi tiết bảng A–E của từng tài liệu nằm ở mục "Đọc thử độc lập (Phase 15)" trong `buoi-09..13/NGHIEN-CUU.md`; đề dự án và Phụ lục D ghi ở `buoi-13/NGHIEN-CUU.md`.

Việc tiếp theo là Phase 16 (buổi 14–15).
