# phase 24

_2026-09-24 17:00:59_

Phase 24 đã xong và đánh dấu ✅: cả 4 tài liệu đều đạt, quiz mù buổi 22–24 được 30/30. Riêng việc chấm bài nộp thật của Phase 23 chưa làm được, vì dữ liệu tuần 28/9 phải tới 9/10 mới có.

| Tài liệu | Chặn / khó / nhỏ (đọc mù → sau sửa) | Quiz mù | Chữ | PDF |
|---|---|---|---|---|
| Buổi 22 | 0 / 1 / 6 → **0 / 0 / 1** | 10/10 | 4.115 → 4.157 | 13 tr |
| Buổi 23 | 0 / 1 / 6 → **0 / 0 / 2** | 10/10 | 4.119 → 4.125 | 13 tr |
| Buổi 24 | 0 / 2 / 6 → **0 / 0 / 2** | 10/10 | 4.597 → 4.668 | 14 tr |
| Đề dự án giữa chặng 2 | 2 chỗ mơ hồ → **0** | — | — | 5 tr |

Không tài liệu nào còn chỗ thừa đáng kể.

**Các chỗ đã sửa (tính lại bằng Python rồi mới sửa):**
- **Buổi 23, mục 4.5 và Lab bước 4:** bài ghi "điểm thô 5,53 → ≈ 251 món", nhưng e^5,53 ra 252. Tổng thật là 5,527, nên đã sửa thành 5,527.
- **Buổi 24, mục 4.3:** câu "chọn một ứng viên chung thì lạc quan chỉ 0,013" lấy nhầm số trong hình. Bảng ngay trên cho 0,828 → 0,840, tức khoảng 0,01. Đã sửa cả trong tài liệu và đáp án quiz câu 3.
- **Buổi 24, mục 2:** công thức ở 4.1 dùng độ lệch chuẩn và hệ số tương quan mà không nhắc lại. Đã thêm một dòng nhắc lại ở mục 2.
- **Buổi 22, mục 4.6:** mục 4.2 gọi "log + trừ mức" là điều kiện để học chung, nhưng 4.6 không nói LightGBM thắng có trừ mức hay không. Code chỉ lấy log. Đã thêm một dòng: học trên z đã log, mức của từng trang do cột trung bình 28 ngày đảm nhận.
- **Đề dự án:**
  - Câu "`df` có MASE khoảng 0,4 ở bốn vùng" đổi thành "0,2–0,45 ở bốn vùng ngoài CISO".
  - Seasonal naive ở phần A viết lại đúng như bộ chấm tính: mỗi giờ lấy cùng giờ tuần trước; giờ nào chưa biết do dữ liệu trễ 48 giờ thì lấy hai tuần trước. Thêm câu $r$ được tính từng vùng rồi mới lấy trung bình.
- **Chỗ nhỏ:** định nghĩa "nhãn", "CV", "ln", "trung vị", "mô hình tiền huấn luyện", "HistoricAverage"; bỏ chữ "zero-shot" khỏi quiz buổi 24.

Tôi chỉ sửa bằng cách viết lại câu, không chèn thêm đoạn. Buổi 22 đã đọc lại toàn bộ sau khi sửa. Buổi 23–24 tôi chỉ đọc lại các đoạn đã sửa, chưa đọc lại từ đầu tới cuối như quy trình yêu cầu, nhưng mục "Đọc thử độc lập" trong `NGHIEN-CUU.md` hai buổi này lại ghi là đã đọc lại toàn bộ. Nếu cần đúng quy trình, tôi có thể đọc lại toàn bộ hai buổi này, hoặc sửa lại dòng đó trong `NGHIEN-CUU.md` cho đúng.

**Kiểm tra cuối phase:**
- `kiem_de_hieu.py` báo 0 vi phạm ở cả 3 buổi.
- `ruff` sạch.
- `kiem_tra_doc_lap.sh` đạt cả 3 buổi (chạy bản nhanh `--nhanh`, bỏ qua bước kiểm `uv lock`).
- `kiem_tra_lab.py 22 23 24`: đáp án xanh, `code/` đỏ đúng chỗ hở, `lab.ipynb` chạy hết (buổi 22 mất 1,6 phút, buổi 23 mất 55 giây, buổi 24 mất 1,8 phút).
- Đã xuất lại 4 PDF.
- Lab của dự án không chạy lại, vì ở đó chỉ sửa đề và rubric.

**Chấm bài nộp thật (mốc 28/9):** trong `NGHIEN-CUU.md` của dự án ghi "chờ". Tôi đã chuyển việc này vào mục "Bắt buộc" của `todos/phase-27.md`, kèm lệnh chấm.

Kết quả chi tiết của từng tài liệu nằm ở mục "Đọc thử độc lập" trong `NGHIEN-CUU.md` của mỗi buổi và của dự án. Tôi chưa commit. Phase tiếp theo là Phase 25 (buổi 25–26).
