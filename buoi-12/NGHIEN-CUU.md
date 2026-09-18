# Nhật ký research — Buổi 12: Khử nhiễu và miền tần số

<!-- BƯỚC 0 của giao thức research (todos.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-18
- **Người/phiên:** Claude Opus 5, phiên xây Phase 4

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | scipy.signal.filtfilt — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html | tài liệu chính thức | 2026-09-18 | 4.4 nhân quả vs không nhân quả |
| 2 | scipy.signal.savgol_filter — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html | tài liệu chính thức | 2026-09-18 | 4.3 Savitzky–Golay, biên |
| 3 | scipy.signal.welch — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html | tài liệu chính thức | 2026-09-18 | 4.2 phổ |
| 4 | PyWavelets — thresholding functions, https://pywavelets.readthedocs.io/en/latest/ref/thresholding-functions.html | tài liệu chính thức | 2026-09-18 | 4.5 wavelet denoising |
| 5 | Hamilton, J.D. (2018), "Why You Should Never Use the Hodrick-Prescott Filter", *REStat* 100(5):831–843 — https://direct.mit.edu/rest/article/100/5/831/58479 | bài gốc / phản biện | 2026-09-18 | 4.4 vấn đề đầu–cuối mẫu |
| 6 | Moura, A. (2024), "…A Comment on Hamilton (2018)", *JCRE* 3:1–17 — https://jcr-econ.org/why-you-should-never-use-the-hodrick-prescott-filter-comment/ | phản biện của phản biện | 2026-09-18 | 4.4 cân bằng quan điểm |
| 7 | statsmodels `UnobservedComponents` / `KalmanSmoother` — https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.structural.UnobservedComponents.html | tài liệu chính thức | 2026-09-18 | 4.4 filter vs smoother |
| 8 | UCI Appliances Energy Prediction (374) — https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction | dữ liệu | 2026-09-17 | toàn bộ lab |

## Phiên bản đã xác minh

| Thư viện / model / dataset | Phiên bản / revision / sha256 | Nguồn xác minh |
|---|---|---|
| Python | 3.12.14 | `uv run python -V` trong `lab/00-nen` |
| scipy | 1.18.1 (trang docs hiển thị v1.18.0) | import trong nền buổi 12 |
| numpy | 2.5.3 | như trên |
| pandas | 3.0.5 | như trên |
| statsmodels | 0.15.0 | như trên |
| PyWavelets (`pywt`) | 1.8.0 | như trên |
| matplotlib | 3.11.2 | như trên |
| UCI Appliances Energy | sha256 `2fccf354445d…`, 11.979.507 B, 19.735 dòng, CC BY 4.0 | `tools/du-lieu/danh-muc.toml`, tải lại + kiểm 2026-09-18 |

## Dữ liệu

| Bộ | URL | Dung lượng | Giấy phép (trích nguyên văn) | Tải thử được? |
|---|---|---|---|---|
| UCI Appliances Energy Prediction | https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip | 11,98 MB (zip), lấy `energydata_complete.csv` | "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. This allows for the sharing and adaptation of the datasets for any purpose, provided that the appropriate credit is given." | Có, sha256 khớp |

Vì sao chọn bộ này: lấy mẫu **10 phút** (fs = 6 mẫu/giờ) nên Nyquist = 3 chu kỳ/giờ — đủ chỗ để dựng thí nghiệm aliasing thật; có cả kênh
rất nhiễu (`Appliances`, công suất thiết bị) và kênh rất mượt (`T2`, nhiệt độ phòng) trong **cùng một tệp**, nên so sánh bộ lọc không bị
lẫn yếu tố nguồn dữ liệu.

## Trích nguyên văn (dùng trong tài liệu)

**filtfilt (scipy).** "This function applies a linear digital filter twice, once forward and once backwards." và "The combined filter has
zero phase and a filter order twice that of the original." → zero-phase đạt được bằng cách **chạy ngược thời gian**, tức mỗi giá trị đầu
ra phụ thuộc vào **toàn bộ** chuỗi, kể cả tương lai. Mặc định `padlen = 3 * max(len(a), len(b))`.

**savgol_filter (scipy), mode mặc định `interp`.** "no extension is used. Instead, a degree *polyorder* polynomial is fit to the last
*window_length* values of the edges, and this polynomial is used to evaluate the last *window_length // 2* output values." → ngay cả ở
biên, SavGol vẫn dùng các điểm **sau** thời điểm đang tính.

**PyWavelets, soft threshold.** "data values with absolute value less than param are replaced with substitute. Data values with absolute
value greater or equal to the thresholding value are shrunk toward zero by value" — công thức: `data/np.abs(data) *
np.maximum(np.abs(data) - value, 0)`.

**Hamilton (2018), abstract.** "The Hodrick-Prescott (HP) filter introduces spurious dynamic relations that have no basis in the
underlying data-generating process. **Filtered values at the end of the sample are very different from those in the middle and are also
characterized by spurious dynamics.** A statistical formalization of the problem typically produces values for the smoothing parameter
vastly at odds with common practice. A regression of the variable at date t on the four most recent values as of date t − h achieves all
the objectives sought by users of the HP filter with none of its drawbacks."

**Moura (2024), abstract (phản biện).** "…in the empirical example Hamilton considers, the HP and Hamilton filters yield cyclical
estimates with very similar dynamic properties, questioning the notion that one decomposition outperforms the other. Second, there is a
mechanical lag in the Hamilton trend… It follows that the Hamilton filter might not constitute a systematically better alternative to the
HP filter." → **cách trình bày trong buổi:** không dạy "HP xấu, Hamilton tốt", mà dạy đúng điểm hai bên đồng ý — **giá trị ở cuối mẫu
khác hẳn giá trị ở giữa mẫu**, và đó chính là chỗ dự báo cần dùng.

## Con số đo được (seed cố định, `dap-an/khu_nhieu.py` và `dap-an/ve_hinh.py`)

Dữ liệu thật (19.735 mẫu 10 phút, 2016-01-11 17:00 → 2016-05-27 18:00):

- Chu kỳ mạnh nhất trong phổ Welch: **24,38 giờ**. Tỷ lệ công suất ở chu kỳ < 1 giờ: `Appliances` **17,8%**, `T2` **0,0%**.

Tín hiệu tổng hợp (`sinh_tin_hieu(n=2000, seed=0)`, nhiễu đã biết):

| Bộ lọc | RMSE so với tín hiệu sạch | Trễ (bước) | Dùng tương lai? | Lượng đổi ở quá khứ khi sửa 10 điểm cuối |
|---|---|---|---|---|
| MA trailing 13 | 1,133 | 6 | Không | 0,000 |
| MA centered 13 | 0,357 | 0 | **Có** | 23,077 |
| EWMA α = 0,15 | 0,906 | 4 | Không | 0,000 |
| Savitzky–Golay 13 | 0,418 | 0 | **Có** | 20,629 |
| Butterworth nhân quả (`lfilter`) | 2,419 | 19 | Không | 0,000 |
| Butterworth `filtfilt` | 0,770 | 0 | **Có** | 23,615 |
| Kalman filter (tham số cố định) | 0,584 | 1 | Không | 0,000 |
| Kalman filter (khớp lại cả chuỗi) | 0,583 | 1 | **Có** | 1,134 |
| Kalman smoother | 0,402 | 0 | **Có** | 17,898 |
| Wavelet db4 (soft, ngưỡng phổ quát) | 0,632 | 0 | **Có** | 7,733 |

Aliasing (hạ mẫu 10 phút → 1 giờ, tín hiệu 1,4 chu kỳ/giờ): Nyquist 3,0 → 0,5 chu kỳ/giờ; công suất ở chu kỳ 2,5 h **64,0** khi hạ mẫu
thô, **0,0** khi lọc chống alias trước; công suất gốc ở chu kỳ 43 phút là 21,33.

Giá của rò rỉ (backtest thật, MAE dự báo `Appliances` 1 bước):

| Feature | MAE | So với không lọc | Dùng tương lai? |
|---|---|---|---|
| không lọc | 46,84 | 0,00% | Không |
| MA trailing 13 | 44,12 | −5,82% | Không |
| **MA centered 13** | **33,88** | **−27,67%** | **Có** |
| EWMA α = 0,15 | 44,10 | −5,85% | Không |
| Savitzky–Golay 13 | 44,07 | −5,92% | **Có** |
| Butterworth nhân quả | 46,37 | −1,02% | Không |
| **Butterworth filtfilt** | **35,37** | **−24,48%** | **Có** |
| Kalman filter (tham số cố định) | 46,41 | −0,93% | Không |
| Kalman filter (khớp lại cả chuỗi) | 46,40 | −0,94% | **Có** |
| Kalman smoother | 44,19 | −5,66% | **Có** |
| Wavelet db4 | 43,52 | −7,09% | **Có** |

Làm trơn **mục tiêu**: MAE trên mục tiêu gốc **46,84**, MAE trên mục tiêu đã làm trơn **35,78** (giảm 23,6% mà không dự báo tốt hơn một
chút nào).

Mốc đầu tiên bị thay đổi khi sửa 10 điểm cuối (n = 400): MA centered **384**, SavGol **384**, Kalman smoother **363**, `filtfilt`
**126** — tức `filtfilt` làm bẩn ngược **274 bước** về quá khứ.

## Phát hiện mới / lỗi hiểu sai phổ biến

- **"filtfilt không trễ nên tốt hơn"** — zero-phase đạt được *bằng cách* dùng tương lai. Với dữ liệu lịch sử thì được; với feature dự báo
  thì đó là rò rỉ. Đưa vào mục "Lỗi thường gặp".
- **Savitzky–Golay trông có vẻ nhân quả ở biên** vì mode `interp` "không mở rộng tín hiệu" — nhưng nó fit đa thức trên `window_length`
  điểm cuối, vẫn là dùng tương lai. Đây là lý do phải **kiểm bằng thí nghiệm**, không tin trực giác.
- **Kênh rò rỉ thứ hai, ít người để ý:** bộ lọc nhân quả nhưng **tham số** (hệ số Butterworth tự chọn theo phổ toàn chuỗi, σ của wavelet
  theo MAD toàn chuỗi, tham số Kalman khớp lại trên cả chuỗi) ước lượng từ toàn bộ dữ liệu. Đo được: Kalman "khớp lại cả chuỗi" làm đổi
  quá khứ **1,134** trong khi bản tham số cố định đổi **0,000**.
- **Làm trơn mục tiêu** (`y` đã lọc) là dạng rò rỉ nặng nhất và hay gặp nhất trong báo cáo đẹp: MAE giảm 23,6% nhưng mô hình đang dự báo
  một đại lượng **không tồn tại trong thực tế**.
- **Hạ mẫu mà không lọc trước** đẩy năng lượng tần số cao xuống thành chu kỳ giả — công suất 64,0 ở chu kỳ 2,5 h hoàn toàn là hiện vật.
  Lưu ý khi dựng demo: tín hiệu đúng **1,5 chu kỳ/giờ** rơi trúng Nyquist mới nên mẫu lấy được toàn 0 — phải dùng 1,4 chu kỳ/giờ.
- **Wavelet và SavGol cho "lợi ích" nhỏ giả tạo** (−5,9%, −7,1%): nhỏ đủ để không ai nghi ngờ, và đó mới là điều nguy hiểm. Chỉ có thí
  nghiệm sửa-đuôi mới phát hiện.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lab 3 mở rộng từ 4 lên **10 cấu hình bộ lọc** (thêm Kalman filter tham số cố định / khớp lại / smoother) | nhỏ | Đã đưa vào; **đã cập nhật `lo-trinh`** |
| Lab 4 thêm nhận xét "lợi ích giả tạo **nhỏ**" của SavGol/wavelet | nhỏ | Đã đưa vào; **đã cập nhật `lo-trinh`** |
| Không dùng `statsmodels.tsa.filters.hpfilter` trong lab | nhỏ | Chỉ nhắc trong lý thuyết (Hamilton 2018 + phản biện Moura 2024); bài tập về nhà cho ai muốn đo |
| Thí nghiệm kiểm nhân quả tự viết thay vì thư viện | nhỏ | Không có thư viện nào làm việc này; là chỗ hở cố ý của `code/` (bỏ qua 200 điểm cuối) |
