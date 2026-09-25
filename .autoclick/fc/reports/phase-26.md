# phase 26

_2026-09-24 23:28:53_

Phase 26 xong: đã soạn đủ buổi 27 (Bayes và GP) và buổi 28 (dự báo phân cấp), mọi bước kiểm đều đạt. Tôi chưa commit.

| | Buổi 27 | Buổi 28 |
|---|---|---|
| Tài liệu | 4.146 chữ, PDF 13 trang | 3.544 chữ, PDF 11 trang |
| Bộ chấm | đáp án xanh 5/5; `code/` đỏ 3 | đáp án xanh 6/6; `code/` đỏ 1 |
| Máy trắng | đạt; `check` 2–4 phút, notebook 7,3 phút | đạt; tổng 2,1 phút |
| `up --pip` | đạt | đạt |
| Tự đọc thử | 0 chặn, 0 khó, quiz 10/10 có căn cứ | 0 chặn, 0 khó, quiz 10/10 có căn cứ |

**Buổi 28 dạy trung thực, theo lựa chọn của bạn:**
- Dự báo làm riêng từng chuỗi lệch cộng 1.613 nghìn chuyến; mọi cách hoà giải đưa độ lệch về 0.
- MinT chỉ thắng base ở 2/4 cấp. Bài giải thích bằng sai số có dấu: đợt tăng du lịch 2016–2017 làm mọi dự báo thấp hơn thực tế, và các chuỗi đáy chệch nặng nhất.
- Khoảng 90% ở cấp quốc gia phủ 58% khi lấy từ phần dư trong mẫu, lên 79% khi dùng sai số ngoài mẫu và hoà giải từng kịch bản. Phần còn thiếu được giải thích trong bài.
- Tiêu chí "Xong khi" của buổi 28 và định nghĩa cột mốc M4 trong lộ trình đã sửa theo hướng này.

**Buổi 27:**
- Prior "rộng" sinh ra 20 triệu món mỗi tháng ở phân vị 90% — đây là ví dụ thật cho bước prior predictive check.
- Mô hình phân cấp qua cổng chẩn đoán (r_hat 1,006, 0 divergence) và thắng cách mỗi mã tự đoán (RMSE 1,182 so với 1,212). 35 mã chỉ có 3 tháng toàn số 0: mô hình đoán 0,22 món/tháng, đúng bằng trung bình thật của năm sau.
- Divergence thật đến từ GP ba thành phần: có seed cho tới 2.012 divergence. Đây là chỗ hở của `code/`, sửa bằng cách gộp hai thành phần đang tranh nhau.
- Non-centered minh hoạ bằng ví dụ 8 trường: tham số hoá centered cho 312 divergence, non-centered cho 0. Dữ liệu Car Parts không tạo "cái phễu" nên không dùng được cho ví dụ này.
- BSTS hội tụ tốt mà khoảng 90% chỉ phủ 46,7%, vì bão Sandy rơi ngay trước mốc dự báo. Bài dùng nó để dạy rằng hội tụ không thay được bước kiểm coverage.

**Thay đổi ngoài hai buổi:**
- Thêm arviz 1.3.0 và rdata 1.1.0 vào bảng phiên bản chung (đã kiểm trên PyPI).
- Giấy phép gốc của Tourism Research Australia đã xác minh là CC BY 4.0, theo điều khoản của Austrade. Chỗ treo từ Phase 8 được gỡ.
- Thêm 10 thuật ngữ vào Phụ lục E; sinh lại Phụ lục F.
- Trong lúc làm, tôi sửa danh mục dữ liệu sau khi đã sinh nền buổi 28 nên nền bị lệch. Đã sinh lại, và kiểm tính tự chứa của cả 28 buổi đều đạt.

Lượt đọc thử thứ hai của cả hai buổi chỉ đọc lại các đoạn đã sửa trong ngữ cảnh, không đọc lại toàn bộ; NGHIEN-CUU.md của hai buổi ghi đúng như vậy.

Phase tiếp theo là Phase 27: đọc thử độc lập buổi 25–28 trong phiên mới, kèm chấm bài nộp thật của dự án giữa chặng 2 (làm được từ 9/10).
