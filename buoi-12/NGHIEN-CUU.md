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

## Research viết lại (Phase 13, 2026-09-18)

Research sư phạm; phiên bản không đổi.

| Khái niệm | Cách giải thích chọn | Hiểu lầm phổ biến | Nguồn (truy cập 2026-09-18) |
|---|---|---|---|
| bộ lọc nhân quả | trung bình trượt 3 điểm tính tay hai kiểu trên $(10, 12, 14, 30, 16)$; đổi số cuối thì kiểu centered sửa cả quá khứ | `rolling().mean()` "chắc là centered"; không trễ = tốt | Wikipedia *Causal filter*; Medium (K. Jones) *Data leakage, lookahead bias and causality in time series* |
| Nyquist, aliasing | bánh xe quay ngược trong phim trước công thức; sóng lặp 4 bước lấy mẫu mỗi 3 bước thành sóng 12 bước | dao động nhanh "biến mất" khi hạ mẫu | TDS *Aliasing in audio, easily explained: from wagon wheels to waveforms*; Schaedler *Circles, Sines and Signals* (wagon wheel); DSPRelated *Sampling and aliasing* |
| trễ, EWMA | EWMA tính tay $\alpha$ = 0,5; `span`/`com` | nhầm `span` với `com` | tài liệu pandas `ewm` |
| rò rỉ qua tham số | hai Kalman filter cùng RMSE, chỉ một cái nhân quả | bộ lọc nhân quả thì không thể rò rỉ | số đo của buổi |

Rút gọn cấu trúc: 10 mục lý thuyết → 6 (quy trình chọn bộ lọc gộp vào 4.6, wavelet thành hộp Nâng cao). Không đổi code. Số đo tái lập đúng
bằng `dap-an/ve_hinh.py` (phổ 24,38 giờ, 17,8% / 0,0%; aliasing 64,0 / 0,0; bảng 10 bộ lọc; MAE 46,84 → 33,88…; 46,84 / 35,78).
`python lab.py check` trên `code/` hỏng **6/8** test (tài liệu cũ ghi 2/8) — sửa Trạng thái đầu buổi, Lab bước 1, README.

## Đọc thử (Phase 13, 2026-09-18)

Tự đọc (không subagent), theo checklist `tools/CHUAN-DE-HIEU.md`; mọi ví dụ tay và đáp án quiz tính lại bằng Python (trung bình trượt hai kiểu
12/18,67/20 và 28; EWMA 15/12,5; aliasing 1/12, 60 phút, 3 giờ; $z_t$ 60 và 50; ngưỡng dung sai $10^{-4}$).

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (2.626 chữ, 10 trang, 57 cờ) | 9 | — | — | — | chặn đúng như `phase-13.md` liệt kê: MAE/RMSE, phương sai (phổ công suất), periodogram, lọc thông thấp, IIR, wavelet, đo trễ bằng tương quan, trích `filtfilt`/SavGol/Hamilton tiếng Anh; "10 cấu hình" bộ lọc chưa liệt kê; 10 mục lý thuyết |
| 1 | viết lại (4.140 chữ) | 0 | 1 | 2 | 10/10 có căn cứ | khó: tài liệu ghi `lfilter`/`filtfilt` trong khi code dùng `sosfilt`/`sosfiltfilt`. Nhỏ: "HP" chưa giải thích; ví dụ aliasing không nói là tín hiệu mô phỏng |
| 2 | sau sửa (13 trang) | **0** | **0** | 1 | 10/10 | **đạt**. Rà gọn: không đoạn nào ≥ 30 chữ lặp ý |

`kiem_de_hieu.py 12`: 57 → **0**. Quiz viết lại, căn cứ: 1 → 4.1, 2 → 4.3, 3 → 4.4, 4 → 4.5, 5 → 4.1, 6 → 4.3, 7 → 4.4, 8 → 4.6, 9 → 4.4–4.5,
10 → 4.6.

## Đọc thử độc lập (Phase 15, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: trung bình trượt 12 / 18,67 / 20 và 28; mẫu
aliasing $(0, −1, 0, 1, 0, −1)$; 60/43 = 1,395 → 0,4 → 2,5 giờ; EWMA 15 / 12,5; $(1 − 0{,}15)/0{,}15$ = 5,67; 35,78/46,84 → −23,6%; RMSE
$\sqrt 5$ = 2,24; quiz 5 (6 / 8; 7 → 15), 6 (3 giờ), 7 (50), 8 (5,8%). Khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | Mục tiêu, Nhắc lại, 4.1 | "feature dự báo", "mục tiêu để chấm" | 1 | không định nghĩa trong buổi; "đặc trưng" của buổi 9 là số tóm cả chuỗi, khác nghĩa cột đầu vào | khó |
| 2 | 4.1 | "backtest đẹp mà dùng thật thì sập" | 1 | "backtest" không định nghĩa trong buổi | nhỏ |
| 3 | Lab bước 2 | "nó rơi đúng Nyquist mới" | 4 | 1,5 lớn hơn Nyquist 0,5; thật ra là gập vào đó | nhỏ |
| 4 | Xong khi | "RMSE gần như nhau (0,584 và 0,583)" | 5 | 0,583 không xuất hiện trong bài | nhỏ |
| 5 | 4.4 bảng | "phổ học" | 1 | từ chuyên ngành, không cản | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Nhân quả**: 2, 4, 6, 20 → trailing 3 điểm ở điểm 3 là 4, centered là 10 (chứa 20).
- **Phổ**: chuỗi lặp mỗi 24 giờ → đỉnh ở 1/24 chu kỳ mỗi giờ.
- **Aliasing**: dao động 50 phút (1,2 chu kỳ/giờ), hạ về 1 giờ → |1,2 − 1| = 0,2 → chu kỳ giả 5 giờ.
- **Trễ**: trailing 7 điểm trễ 3 bước.
- **Bài kiểm đổi đuôi**: cộng 50 vào 10 điểm cuối; centered 13 đổi 6 mốc trước đó.
- **Làm trơn mục tiêu**: chấm trên đường đã làm trơn thì MAE giảm mà mô hình không đổi.

### C. Quiz mù

1 A · 2 B · 3 B · 4 B · 5 trailing 6, centered 8; centered điểm 4: 7 → 15 · 6 chu kỳ giả 3 giờ; lọc thông thấp trước · 7 50; `com=3` cùng
bộ lọc · 8 EWMA/trailing, ≈ 5,8% · 9 ba RMSE thấp nhất nhìn tương lai; Kalman filter tham số cố định · 10 chấm trên mục tiêu làm trơn; MAE
thật vẫn 46,84. Căn cứ: 1, 5 → 4.1; 2, 6 → 4.3; 3, 7 → 4.4; 4, 9 → 4.4–4.5; 8, 10 → 4.6. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 4. Sửa một điều: định nghĩa feature và mục tiêu.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10.** Sửa: thêm dòng "feature / mục tiêu" vào bảng Từ mới; 4.1 "chấm trên quá khứ (backtest)"; Lab bước 2 "gập đúng vào
Nyquist mới"; Xong khi bỏ số 0,583, ghi "(tham số cố định / khớp lại trên cả chuỗi)".

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 15 đọc mù | 4.140 | 13 | 0 | 1 | 4 | 10/10 | 0 |
| sau sửa, đọc lại | 4.161 | 13 | **0** | **0** | 1 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 12` 0; `kiem_tra_lab.py 12` đạt; tự chứa đạt.
