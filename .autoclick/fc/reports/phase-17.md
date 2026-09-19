# phase 17

_2026-09-19 06:53:31_

Phase 17 xong: buổi 16 và 17 đạt mọi tiêu chí, đã đánh dấu ✅ ở `todos.md`, `todos/phase-17.md` và `todos/tong-quan.md`. Chưa commit.

"Bản nháp" 16–17 thật ra chỉ là khuôn trống (không code, không hình, không test), nên cả hai buổi được soạn mới toàn bộ.

| Buổi | Chữ | PDF | Lab | Đọc thử (chặn / khó / nhỏ) |
|---|---|---|---|---|
| 16 ETS & Theta | 3.536 | 11 trang | đáp án xanh 8/8, `code/` đỏ 4 test đúng chỗ hở | 0 / 2 → 0 / 3 → 0 |
| 17 ARIMA | 3.575 | 11 trang | đáp án xanh 6/6, `code/` đỏ 3 test đúng chỗ hở | 0 / 1 → 0 / 2 → 0 |

Cả hai notebook chạy hết không lỗi. Kiểm tự chứa đạt, `ruff` và `kiem_de_hieu.py` sạch. Mọi con số lấy từ lần chạy thật.

**Mọi mô hình so với seasonal naive, có kiểm định** (bộ backtest buổi 15 + Diebold–Mariano, 366 chuỗi du lịch):

| Mô hình | MASE trung bình | So với seasonal naive |
|---|---|---|
| AutoARIMA | 1,574 | có ý nghĩa, p < 0,0001 |
| AutoETS | 1,581 | có ý nghĩa, p < 0,0001 |
| AutoTheta | 1,691 | không có ý nghĩa, p = 0,49 |
| seasonal naive | 1,720 | — |
| AutoARIMA quên mùa vụ (`season_length=1`) | 2,791 | thua cả seasonal naive |

AutoARIMA và AutoETS hoà nhau (p = 0,74).

**Buổi 16:**
- **SES tự viết khớp statsforecast tuyệt đối.** Holt tự viết lệch tới 1,7% vì khác cách khởi tạo; tài liệu nói rõ nguyên nhân.
- **Holt–Winters nhân thắng dạng cộng** trên hành khách EU (MAPE 2,13% so với 3,23%).
- **AutoETS chọn theo AICc lại dự báo tệ hơn** (5,60%). Tài liệu dùng chính ví dụ này để dạy rằng AICc không phải sai số dự báo.
- **Tỷ lệ phủ thật:** khoảng 80% của ETS phủ đúng 81,0%, khoảng 95% chỉ phủ 91,4%; hai khoảng của Theta còn hẹp hơn nữa.

**Buổi 17:**
- **Lệch lộ trình về dữ liệu:** bộ G.17 trong danh mục là chuỗi đã khử mùa vụ, nên không dạy được SARIMA. Tôi dùng G.17 cho ARIMA không mùa vụ và chuỗi du lịch T33 cho SARIMA.
- **T33:** mô hình đọc từ ACF, SARIMA(0,1,1)(0,1,1)₁₂, qua Ljung–Box và AICc chỉ cách auto-ARIMA 0,9 đơn vị.
- **G.17:** mô hình AR(4) đọc từ PACF kém auto-ARIMA 5,4 đơn vị AICc. Tài liệu dạy đây là giới hạn của cách đọc ACF/PACF, không giấu đi.
- **Backtest 366 chuỗi mất khoảng 6 phút,** nên notebook lưu kết quả vào `du-lieu/cache/` để lần sau đọc lại; bộ chấm chỉ dùng 6 chuỗi.

**Chỗ hở thêm ngoài bảng cũ** (đã ghi vào `todos/quy-uoc.md`):
- Buổi 16: SES lấy giá trị khớp bằng mức đã cập nhật, nên α ra 1 và sai số 0. Bài kiểm rò rỉ tự động bắt được.
- Buổi 17: hàm kiểm phần dư không kiểm gì, luôn báo "ổn", nên mô hình quên mùa vụ vẫn lọt qua.

**Lỗi của chính bản đầu, bắt được và đã sửa khi đọc thử:**
- Câu đếm "30 mô hình ETS" gán nhầm cho sách FPP3; FPP3 chỉ có 18, con số 30 là của Hyndman và cộng sự (2008).
- Lập luận "thiếu hàng" tính cả phần nằm ngoài khoảng dự báo, trong khi chỉ phần vượt cận trên mới là thiếu hàng.
- Câu tự kiểm tra ghi ACF trễ 1 của MA(1) là 0,6, điều không thể xảy ra (tối đa 0,5).

Việc tiếp theo là Phase 18: đọc thử độc lập buổi 14–17, trong một phiên mới.
