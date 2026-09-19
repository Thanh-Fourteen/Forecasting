# phase 16

_2026-09-19 06:15:09_

Phase 16 xong: buổi 14 và 15 đạt mọi tiêu chí, đã đánh dấu ✅ ở `todos.md`, `todos/phase-16.md` và `todos/tong-quan.md`. Chưa commit (thư mục `buoi-14/`, `buoi-15/` vẫn chưa được theo dõi trong git).

| Buổi | Chữ | PDF | Lab | Đọc thử (chặn / khó / nhỏ) |
|---|---|---|---|---|
| 14 Baseline & chỉ số | 3.940 | 16 trang | đáp án xanh 13/13, `code/` đỏ 5 test đúng chỗ hở | 0 / 2 → 0 / 2 → 1 |
| 15 Backtesting | 3.990 | 12 trang | đáp án xanh 9/9, `code/` đỏ 3 test đúng chỗ hở | 0 / 0 / 4 → 0 |

Hai notebook chạy hết không lỗi. Kiểm tự chứa đạt, `ruff` và `kiem_de_hieu.py` sạch. Mọi con số trong tài liệu và quiz lấy từ lần chạy thật hoặc tính lại bằng Python.

**Buổi 14 — bản nháp chỉ có code, test và hình.** Tôi giữ nguyên số đo, viết mới tài liệu, quiz, notebook và README. Có hai sửa trong code:
- Bản nháp tính ME = trung bình(dự báo − thực tế), ngược quy ước cả khoá (sai số = thực tế − dự báo). Tôi sửa ở cả `code/` lẫn `dap-an/`. Đây không phải chỗ hở cố ý, và bộ chấm không kiểm dấu ME.
- Chọn lại chuỗi minh hoạ cho hình bốn baseline, vì chuỗi cũ làm ba đường không phân biệt được.

Một kết quả thật cần biết: trên M4 theo ngày, naive và drift thắng seasonal naive (MASE 0,835 và 0,810 so với 1,077). Tài liệu dạy rằng seasonal naive là mốc bắt buộc, không phải mốc mạnh nhất.

**Buổi 15 — bản nháp chỉ là khuôn trống, nên soạn mới toàn bộ.** Bộ backtest dùng cùng giao diện với `tv.backtest` mà các buổi sau dùng. Nó cho cùng cutoff và cùng seasonal naive với `statsforecast.cross_validation` (chênh 0,0), và có thêm `gap` vì statsforecast không có tham số này. Bộ chấm gồm 9 test. Tôi thêm một chỗ hở thứ ba ngoài bảng cũ (DM bỏ tự tương quan khi h > 1) và đã ghi vào bảng chỗ hở trong `todos/quy-uoc.md`.

Số thật, báo đúng như đo được:
- **K-fold xáo trộn:** với rừng ngẫu nhiên, hứa sai số thấp hơn hold-out 23% (1.639 so với 2.129 MW). Với hồi quy tuyến tính chỉ lạc quan 12%, khớp kết quả của Bergmeir và cộng sự (2018). Tài liệu dạy đúng sắc thái này, không nói "K-fold luôn sai".
- **Rolling origin 28 ngày:** lệch hold-out −8,7% với rừng ngẫu nhiên, đạt yêu cầu dưới 10% của lộ trình. Với hồi quy tuyến tính lệch −15,5%, vì tháng 9 khác quý 4; tài liệu nói thẳng điều này.
- **Chọn và báo cáo trên cùng đoạn** (414 chuỗi M4 theo giờ): MASE báo cáo 0,775, đo thật trên đoạn riêng là 1,039.
- **Mô hình "hơn seasonal naive 4,3%"** chỉ có được khi tune trên chính hold-out; tune đúng cách thì nó trùng với seasonal naive. DM bỏ tự tương quan cho p = 0,0000012, còn bản hiệu chỉnh cho p = 0,16.

**Phụ lục D:** thêm bảng ví dụ trên dữ liệu thật của buổi 14–15 (bản mới 8 trang).

Việc tiếp theo là Phase 17 (buổi 16–17: ETS, Theta, ARIMA).

Nguồn research chính:
- [FPP3 §5.10](https://otexts.com/fpp3/tscv.html)
- [Bergmeir, Hyndman & Koo 2018](https://robjhyndman.com/papers/cv-wp.pdf)
- [Bergmeir & Benítez 2012](https://www.sciencedirect.com/science/article/abs/pii/S0020025511006773)
- [Diebold 2015](https://www.nber.org/papers/w18391)
- [Hewamalage và cộng sự](https://arxiv.org/abs/2203.10716)
- [StatsForecast cross_validation](https://nixtlaverse.nixtla.io/statsforecast/src/core/core.html)
- PyPI [statsforecast](https://pypi.org/project/statsforecast/) / [utilsforecast](https://pypi.org/project/utilsforecast/)
