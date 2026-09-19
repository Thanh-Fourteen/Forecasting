# phase 4

_2026-09-18 09:55:55_

Phase 4 xong. Tổng kết:

## Đã làm

**Phase 4 — buổi 9–13 + dự án giữa chặng 1** (mỗi buổi: research có nguồn → code có chỗ hở → bộ chấm → hình → tài liệu 10 trang → quiz; lab chạy thật trên venv trắng, đáp án xanh / `code/` đỏ đúng chỗ):

| Buổi | Kết quả đo được đáng chú ý |
|---|---|
| 9 Đặc trưng | entropy ↔ sMAPE +0,25 nhưng ↔ MASE ≈ 0 và **đảo dấu** −0,54 khi đổi thang chuẩn hoá |
| 10 Làm sạch | 249 mốc thiếu mà `isna()` không thấy; **thứ hạng 7 cách điền đảo** giữa lỗ ngắn/lỗ dài |
| 11 Ngoại lai | masking: 3σ tụt 16→5 ngày; **cả 5 phương pháp đều gắn cờ 10/10 đỉnh Tết** |
| 12 Khử nhiễu | bảng 10 bộ lọc có cột "dùng tương lai?" do test tự điền; làm trơn mục tiêu ăn gian 46,8→35,8 |
| 13 Rò rỉ | lịch âm tự viết khớp `holidays` **2000–2035**; rò rỉ hứa −3,85% nhưng chạy thật +2,20% với dự báo D+3 |
| Dự án 1 | 6 lỗi cài sẵn trên dữ liệu VN thật, lời giải mẫu chứng minh bắt được cả 6 |

**Phase 1 (bạn yêu cầu hoàn thiện):**
- Mirror **49 bộ / 614 MB** lên `Tony2202/khoa-forecasting-du-lieu` (công khai), giữ nguyên byte, thẻ dữ liệu ghi giấy phép + nguồn + sha256. Kiểm cache trắng: Online Retail II tải **18 giây** thay vì ~5 giờ từ UCI.
- Chốt nốt `uci-electricity-load` (tải đủ 261 MB) → **55/56 bộ có sha256**.
- Đã push toàn bộ lên `github.com/Thanh-Fourteen/Forecasting` (5 commit tiếng Anh).

## Cần bạn xử lý

1. **Thu hồi khoá**: HF token và Kaggle key bạn dán đã nằm trong transcript — nên xoay vòng sau khi xong.
2. **M5**: tài khoản `thanh14` chưa chấp nhận luật cuộc thi (Kaggle trả 403). Bấm Join tại `kaggle.com/competitions/m5-forecasting-accuracy/rules` rồi báo tôi để chốt sha256 (buổi 23 hiện vẫn chạy được bằng bộ dự phòng mở).
3. **Điểm lệch lớn đã sửa vào lộ trình** (báo theo giao thức research): bỏ **OpenAQ** khỏi buổi 10 và dự án 1 (v3 bắt buộc key cho mọi endpoint, v2 đã ngừng) → thay bằng GHCNh Nội Bài + Open-Meteo; buổi 11 đổi thông điệp lab 3 vì đo ra **không ngưỡng thống kê nào** cứu được đỉnh Tết; buổi 9 đổi trục đánh giá từ MASE sang sMAPE.

Phase 5 (buổi 14–17: baseline, chỉ số, backtest, ETS/ARIMA) là phần tiếp theo trong `todos.md`.
