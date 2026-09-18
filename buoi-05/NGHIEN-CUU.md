# Nhật ký research — Buổi 5: Biến đổi và điều chỉnh dữ liệu

- **Ngày research:** 2026-09-18
- **Nền buổi:** Python 3.12.3; numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, matplotlib 3.11.2, **openpyxl 3.1.5**
  (mới thêm vào `tools/nen/phien-ban.toml` — bản mới nhất trên PyPI, phát hành 2024-06-28)
- **[CHẠY]** = đã chạy trong nền buổi; seed ghi kèm

## Nguồn đã đọc

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | FPP Pythonic §3.1 Transformations and adjustments, https://otexts.com/fpppy/nbs/03-decomposition.html | 2026-09-18 | lịch, dân số, lạm phát, log, Box-Cox, Guerrero |
| 2 | FPP Pythonic §5.6, §5.8, https://otexts.com/fpppy/nbs/05-toolbox.html | 2026-09-18 | đổi ngược, công thức bias 5.3, MAE ↔ trung vị |
| 3 | FPP2 §3.2 (ví dụ sữa), https://otexts.com/fpp2/transformations.html | 2026-09-18 | điều chỉnh số ngày |
| 4 | Hyndman, "Backtransforming", https://robjhyndman.com/hyndsight/backtransforming/ | 2026-09-18 | nguồn gốc công thức Taylor |
| 5 | Guerrero (1993), J. Forecasting 12(1):37–48, doi:10.1002/for.3980120104 (abstract, Crossref) | 2026-09-18 | phương pháp chọn λ |
| 6 | forecast R `guerrero.R`, https://raw.githubusercontent.com/robjhyndman/forecast/master/R/guerrero.R; feasts `guerrero` docs | 2026-09-18 | thuật toán cụ thể |
| 7 | Proietti & Lütkepohl (2013), IJF 29(1):88–99, doi:10.1016/j.ijforecast.2012.06.001 (preprint MPRA 32294) | 2026-09-18 | phản biện hiệu chỉnh bias |
| 8 | scipy 1.18.1 `boxcox`, `boxcox_normmax`, `yeojohnson`, `special.inv_boxcox`; statsmodels 0.15.0 `base.transform.BoxCox`; scikit-learn 1.9.1 `PowerTransformer` [CHẠY] | 2026-09-18 | API |
| 9 | Census MARTS `mrtssales92-present.xlsx` — bản lưu Wayback 2026-09-13; trang archived `sales.html`, retail index (2026-09-15) | 2026-09-18 | dữ liệu, chú thích |
| 10 | 17 U.S.C. §105, https://www.law.cornell.edu/uscode/text/17/105 | 2026-09-18 | public domain |
| 11 | BLS `cu.series` (CUUR0000SA0), BEA `SeriesRegister.txt` (B230RC) | 2026-09-18 | nghĩa mã chuỗi |

## Trích dẫn nguyên văn

**FPP §3.1.** Mục đích: "to simplify the patterns in the historical data by removing known sources of variation, or by making the
pattern more consistent across the whole data set. Simpler patterns are usually easier to model and lead to more accurate forecasts."
Lịch: "there will be variation between the months simply because of the different numbers of trading days in each month… computing
average sales per trading day in each month". Dân số: "consider the data per person (or per thousand people, or per million people)
rather than the total". Lạm phát: "x_t = y_t/z_t * z_2000 gives the adjusted house price at year 2000 dollar values… a common price
index is the Consumer Price Index (or CPI)". Log: "changes in a log value are relative (or percentage) changes on the original scale…
If any value of the original series is zero or negative, then logarithms are not possible." Box-Cox (3.1): w = log(y) khi λ = 0,
(sign(y)|y|^λ − 1)/λ khi khác — "a modified Box-Cox transformation, discussed in Bickel & Doksum (1981), which allows for negative
values of y_t provided λ > 0"; "A good value of λ is one which makes the size of the seasonal variation about the same across the whole
series". Thư viện: `boxcox_lambda(y, method="guerrero", season_length=4)` của CoreForecast.

**FPP §5.6.** "the back-transformed point forecast will not be the mean of the forecast distribution. In fact, it will usually be the
median… medians do not add up, whereas means do." Công thức (5.3): exp(ŵ)[1 + σ_h²/2] khi λ = 0; (λŵ+1)^{1/λ}[1 + σ_h²(1−λ)/(2(λŵ+1)²)]
khi khác. "The larger the forecast variance, the bigger the difference between the mean and the median." **§5.8:** "A forecast method
that minimises the MAE will lead to forecasts of the median, while minimising the RMSE will lead to forecasts of the mean."
**Hyndman blog:** "using the first three terms of a Taylor expansion around μ, the mean on the original scale is given by f(μ) + ½σ²f''(μ)."

**Guerrero (forecast R):** chia chuỗi thành khối độ dài chu kỳ, bỏ khối đầu không đủ, tỷ số `x.sd / x.mean^(1 - lam)`, cực tiểu
`sd(x.rat) / mean(x.rat)` trên [−1, 2]. feasts: "This function will make use of all of your data, whereas the forecast package will not
use data that doesn't complete a seasonal period."

**Proietti & Lütkepohl (2013):** "Typically, the naïve predictor that just reverses the transformation leads to a lower mean square error
than the optimal predictor at short forecast leads."

**Census MARTS.** Chú thích (2): "Estimates are adjusted for seasonal variations and holiday and trading-day differences, but not for price
changes." Gãy chuỗi: "Prior to the benchmark report released in April 2025, the Monthly Retail Trade Survey estimates included
nonemployers." Retail index (lưu 2026-09-15): "Revised not adjusted estimates and corresponding adjusted estimates are tentatively scheduled
for release on September 28, 2026". **17 U.S.C. §105:** "Copyright protection under this title is not available for any work of the United
States Government."

**BLS/BEA.** `CUUR0000SA0 … 1982-84=100 All items in U.S. city average, all urban consumers, not seasonally adjusted`;
`B230RC,"Population (midperiod, thousands)"`.

## API đã kiểm

- scipy 1.18.1: `boxcox(x, lmbda=None, ...)` (λ theo MLE); `boxcox_normmax(..., method='pearsonr')` — mặc định **pearsonr**, khác `boxcox`;
  **không có Guerrero**; `boxcox` trên dữ liệu không dương → `ValueError: Data must be positive.`; `yeojohnson` nhận số âm.
- statsmodels 0.15.0: `statsmodels.base.transform.BoxCox().transform_boxcox(x, lmbda=None, method='guerrero', **kwargs)` —
  `_guerrero_cv(..., window_length=4, scale="sd")`, cận (−1, 2); `untransform_boxcox(..., method='naive')` **không hiệu chỉnh bias**.
- scikit-learn 1.9.1: `PowerTransformer(method='yeo-johnson', standardize=True)` — mặc định Yeo-Johnson và chuẩn hoá.
- coreforecast 0.0.18 có `boxcox_lambda(method='guerrero')` — không thêm vào nền (tự viết là mục tiêu; đối chiếu statsmodels).

## Số liệu thật của buổi [CHẠY]

- **MARTS** (NOT ADJUSTED, "Retail and food services sales, total"): 414 tháng 1992-01 → 2026-06, không thiếu; nhãn cột tháng 5 là
  "May 2025" (không có dấu chấm — regex phải chấp nhận). 1.115 ô "(S)"/"(NA)" ở các ngành con. Đọc toàn tệp ~3 s.
- **CPI-U CUUR0000SA0**: tháng **10/2025 ghi "-"** (không công bố) → NaN; nội suy một tháng khi đổi giá thực. CPI trung bình 1993 = 144,5;
  2025 = 321,94. 9/2025 = 324,8.
- **Dân số B230RC**: trung bình 1993 = 260.282 nghìn; 2025 = 341.944 nghìn.
- **Lịch 2023:** T1 616.100, T2 595.432, T3 679.701 triệu USD. T2/T1 thô −3,35%, theo ngày **+7,0%**; T3/T2 thô +14,15%, theo ngày **+3,11%**.
  Bản ADJUSTED: T2 672.152, T3 665.071 → T3/T2 −1,05% (đã khử cả mùa vụ, ngày giao dịch, ngày lễ).
- **Danh nghĩa → thực → đầu người**, tổng năm 1993 → 2025: danh nghĩa 2.091.704 → 8.699.796 (**+315,9%**); giá thực USD 2025 **+86,6%**;
  thực trên đầu người **+42,0%**.
- **Box-Cox** (1992–2019, m = 12): λ Guerrero tự viết (lưới 0,001) **0,343**; statsmodels `window_length=12` 0,34294; scipy MLE **0,595**.
  Độ dốc log sd theo log trung bình năm 0,655. sd trong năm 2019 / 1992: gốc 2,45; λ = 0,343 1,21; log 0,84. Tự viết `boxcox` khác
  `scipy.special.boxcox` tối đa 1,7e−13; đổi ngược sai tối đa 3,5e−10.
- **Log-normal μ = 5, σ = 0,5, 100.000 mẫu, seed 42:** trung bình mẫu 168,01; exp(trung bình log) 148,10 (−11,9%); công thức FPP 166,75; lý
  thuyết exp(μ + σ²/2) = 168,17. Sai lệch lý thuyết của trung vị so với trung bình: σ 0,1 → −0,50%; 0,3 → −4,40%; 0,5 → −11,75%; 1,0 → −39,35%.
  Sai số của xấp xỉ FPP so với trung bình đúng: σ 0,5 → −0,72%; 1,0 → −9,02%.
- **Dự báo log cuốn trên tập kiểm tra** (seasonal naive có drift trên log, cửa sổ học 96 tháng, gốc mỗi tháng 2012-01 → 2018-12, tầm 12,
  1.008 dự báo), tổng dự báo / tổng thực − 1:
  | Chuỗi | σ (sai phân mùa vụ log) | trung vị | có hiệu chỉnh |
  |---|---|---|---|
  | Tổng bán lẻ + ăn uống | 0,047 | −0,47% | −0,37% |
  | Trạm xăng | 0,159 | +3,50% | +4,85% |
  | Bách hoá | 0,073 | +9,69% | +9,93% |
  | Quà tặng, lưu niệm | 0,077 | −2,05% | −1,77% |
  Hiệu chỉnh đẩy dự báo lên ≈ σ²/2 (0,11; 1,27; 0,26; 0,29 điểm %) — đúng lý thuyết nhưng **nhỏ** so với sai lệch do xu hướng; với trạm xăng
  nó làm tệ hơn.
- **Sai phân mùa vụ log** (≈ % so với cùng tháng năm trước): trung bình 2012–2019 +3,71%; đáy 2009 −14,0%; 4/2020 −21,3%; 4/2021 +42,1%. 25 tháng âm
  → Box-Cox báo "Data must be positive"; Yeo-Johnson λ = 1,091.
- **Chuẩn hoá theo chuỗi** (2024): trạm xăng trung bình 52.626, nhà sách 655 triệu USD/tháng; chia trung bình: trạm xăng 0,882–1,095, nhà sách
  0,813–1,527 (đỉnh tháng 12).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Census chặn 403 từ Việt Nam; API cần key | vừa | Bản lưu Wayback chốt sha256 + mirror (đã sửa lộ trình, thêm danh mục `census-marts-ban-le`) |
| Lộ trình kỳ vọng bias log–exp "thấp có hệ thống" đo được rõ trên bán lẻ. Đo thật: ≈ σ²/2 ≈ 0,1% với tổng bán lẻ theo tháng | vừa | Dạy bằng mô phỏng log-normal (−11,9%) + bảng thật 4 chuỗi; kết luận trung thực: quan trọng khi σ lớn (dữ liệu ngày/giờ, đơn vị nhỏ, tầm xa), không cứu sai lệch do xu hướng; nhắc Proietti & Lütkepohl và MAE ↔ trung vị |
| "Seasonal naive trên thang biến đổi" — đổi ngược thẳng của seasonal naive không drift trùng seasonal naive gốc | nhỏ | Dùng seasonal naive **có drift** trên log (FPP) — trung vị ≠ trung bình rõ ràng |
| scipy không có Guerrero | nhỏ | Tự viết, đối chiếu statsmodels `BoxCox` (`window_length=12`) |
| CPI 10/2025 không công bố | nhỏ | NaN + nội suy một tháng, ghi trong Lỗi thường gặp |
| openpyxl chưa có trong bảng phiên bản | nhỏ | Thêm `openpyxl = "3.1.5"` |
