# phase 3

_2026-09-18 01:30:58_

Phase 3 xong: buổi 04–08 và Phụ lục C.

**Kiểm cuối**
- `tools/kiem_tra_doc_lap.sh`: 8/8 buổi tự chứa.
- `ruff check .`: sạch.
- PDF: buổi 4 là 12 trang, buổi 6 là 11, còn lại 10 — tất cả trong khoảng 10–16. Phụ lục C: 9 trang.

**Bộ chấm (code/ phải đỏ, dap-an/ phải xanh)**

| Buổi | code/ | dap-an/ | Chỗ hở → triệu chứng |
|---|---|---|---|
| 04 | 1/8 | 8/8 | Chỉ có đường thô + trục kép + trục y cắt; hồ sơ giờ×thứ 7 dòng giống hệt nhau |
| 05 | 3/8 | 8/8 | So tháng không chia số ngày; tăng trưởng danh nghĩa; đổi ngược bỏ qua σ² |
| 06 | 2/7 | 7/7 | Phân rã cổ điển chu kỳ 24; `robust` bị bỏ qua |
| 07 | 4/9 | 9/9 | Chỉ chạy ADF; luôn sai phân sẵn một lần |
| 08 | 7/10 | 10/10 | Chỉ tương quan trên mức; CCF chưa prewhiten; kết luận "x gây ra y" |

**Những gì đo được, đáng chú ý**
- **Buổi 6 (PJM 2024):** với chu kỳ 24, nhịp tuần chui vào **xu hướng** (thứ Tư 95.036 MW so với Chủ nhật 88.459), còn phần dư giữ mùa vụ ngày đổi theo mùa — 10,2% phương sai ở hồ sơ tháng×giờ, MSTL còn 0,06%.
- **Buổi 8 (ERCOT):** Pearson 0,616 nhưng R² tuyến tính chỉ 0,379; tách CDD/HDD lên 0,813. Hai nhánh: −0,649 khi lạnh, +0,910 khi nóng. Granger có ý nghĩa **cả hai chiều** (p ≈ 0) — tức kiểm định cũng "kết luận" tải điện gây ra nhiệt độ.
- **Buổi 7 (GDP thực):** theo KPSS phải sai phân 2 lần, nhưng lần hai cho ACF(1) = −0,488 và sd tăng 1,105 → 1,455. Bỏ cú sốc COVID (1985–2019) thì cả ADF lẫn KPSS đều nói "dừng".

**Điểm lệch so với lộ trình — đã sửa lộ trình và todos trước khi soạn**
1. **Buổi 5, dữ liệu:** census.gov chặn IP Việt Nam (403) và API nay cần key. Chuyển sang bản lưu Wayback của `mrtssales92-present.xlsx`, đã chốt sha256, public domain theo 17 U.S.C. §105. Đã thêm `openpyxl 3.1.5` vào bảng phiên bản chung.
2. **Buổi 5, kỳ vọng về bias:** lộ trình chờ độ lệch log–exp rõ trên bán lẻ; đo thật chỉ ≈ σ²/2 ≈ 0,1% cho tổng bán lẻ. Buổi dạy bằng mô phỏng log-normal (−11,9%) cộng bảng 4 chuỗi thật, và nói rõ khi nào **không** nên hiệu chỉnh.
3. **Buổi 6:** sửa mô tả "mùa vụ tuần rơi hết vào phần dư"; minh hoạ robust đổi từ đợt nắng nóng sang **giờ số liệu hỏng 21/11/2024** (nắng nóng nhiều ngày bị xu hướng hấp thụ, robust giúp ít).
4. **Buổi 7:** BLS không phát hành tệp nhỏ cho tỷ lệ thất nghiệp (chỉ tệp 390 MB hoặc API 10 năm/lần) → thay bằng chỉ số sản lượng công nghiệp FRB G.17.
5. **Buổi 8:** "Pearson thấp" không đúng với Texas (0,616) → dạy bằng R² và hai nhánh; cặp chuỗi xu hướng dùng CPI-U × dân số; thêm hai bộ Open-Meteo Dallas/Houston 2024 vào danh mục.

**Cạm bẫy thư viện đã ghi vào bài**
- `statsmodels.ccf(x, y)` trả corr(x₍t+k₎, y₍t₎) — muốn "x dẫn y" phải gọi `ccf(y, x)`; `pccf` mới lại ngược.
- STL/MSTL trả **toàn NaN** không báo lỗi nếu đầu vào còn một NaN.
- `adfuller`/`kpss` phát FutureWarning nếu không truyền `result_object`; `pacf` mặc định khác `plot_pacf`.
- `month_plot` thực chất vẽ subseries plot.

Vẫn treo từ phase trước: mirror Hugging Face (cần bạn đồng ý mới đẩy lên) và Kaggle. Chưa commit gì.
