# Nhật ký research — Buổi 6: Phân rã chuỗi thời gian

- **Ngày research:** 2026-09-18
- **Nền buổi:** Python 3.12.3; numpy 2.5.3, pandas 3.0.5, matplotlib 3.11.2, statsmodels 0.15.0
- **[CHẠY]** = đã chạy trong nền buổi; không có ngẫu nhiên (trừ mô phỏng của agent research, seed 0)

## Nguồn đã đọc

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | FPP Pythonic **ch. 3** Time series decomposition, https://otexts.com/fpppy/nbs/03-decomposition.html | 2026-09-18 | cộng/nhân, 2×m-MA, cổ điển, X-11/SEATS, STL, dữ liệu khử mùa vụ |
| 2 | FPP Pythonic ch. 4 §4.3, https://otexts.com/fpppy/nbs/04-features.html; fpp3 https://otexts.com/fpp3/stlfeatures.html | 2026-09-18 | $F_T$, $F_S$ |
| 3 | feasts `features.R`, https://raw.githubusercontent.com/tidyverts/feasts/master/R/features.R | 2026-09-18 | $F_S$ cho nhiều mùa vụ |
| 4 | Cleveland, Cleveland, McRae & Terpenning (1990), JOS 6(1):3–73, bản quét https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/stl-a-seasonal-trend-decomposition-procedure-based-on-loess.pdf | 2026-09-18 | STL gốc |
| 5 | Bandara, Hyndman & Bergmeir, MSTL, arXiv:2107.13462; bản in IJOR 2025, 52(1):79–98, doi:10.1504/IJOR.2025.143957 | 2026-09-18 | MSTL |
| 6 | statsmodels 0.15.0 — `seasonal_decompose`, `STL` (docstring + `_stl.pyx`), `MSTL`, `x13_arima_analysis` [CHẠY] | 2026-09-18 | API |
| 7 | EIA-930 form instructions, https://www.eia.gov/survey/form/eia_930/instructions.pdf; EIA glossary "Balancing authority" | 2026-09-18 | nghĩa cột, mốc cuối giờ |
| 8 | EIA Today in Energy id=43295 (2020-04-06), id=42915 (2020-02-21), id=54899 (2022-12-06) | 2026-09-18 | mẫu hình ngày/tuần, cảnh báo dữ liệu |
| 9 | Ruggles et al. (2020), Sci Data 7:155, doi:10.1038/s41597-020-0483-x | 2026-09-18 | chất lượng dữ liệu EIA-930 |
| 10 | PUDL docs EIA-930, https://docs.catalyst.coop/pudl/en/nightly/data_sources/eia930.html | 2026-09-18 | giờ địa phương có lỗ/trùng DST |

## Trích dẫn nguyên văn

**FPP §3.2:** "The additive decomposition is the most appropriate if the magnitude of the seasonal fluctuations, or the variation
around the trend-cycle, does not vary with the level of the time series." "When a log transformation has been used, this is equivalent
to using a multiplicative decomposition on the original data".

**§3.3 (2×m-MA):** "When a 2-MA follows a moving average of an even order (such as 4), it is called a “centred moving average of order
4”. This is because the results are now symmetric."

**§3.4 cổ điển** — bước: 2×m-MA nếu m chẵn; "Calculate the detrended series: y_t − T̂_t"; trung bình theo mùa rồi "adjusted to ensure
that they add to zero"; "R̂_t = y_t − T̂_t − Ŝ_t". Điểm yếu: "it is not recommended, as there are now several much better methods";
"The estimate of the trend-cycle is unavailable for the first few and last few observations"; "The trend-cycle estimate tends to
over-smooth rapid rises and falls in the data"; "Classical decomposition methods assume that the seasonal component repeats from year to
year… electricity demand patterns have changed over time as air conditioning has become more widespread"; "The classical method is not
robust to these kinds of unusual values."

**§3.5 X-11/SEATS:** "These methods are designed specifically to work with quarterly and monthly data"; X-11 "handles trading day
variation, holiday effects"; "“SEATS” stands for “Seasonal Extraction in ARIMA Time Series”".

**§3.6 STL:** "STL will handle any type of seasonality, not only monthly and quarterly data." "The seasonal component is allowed to
change over time, and the rate of change can be controlled by the user." "It can be robust to outliers … They will, however, affect the
remainder component." Nhược: "it does not handle trading day or calendar variation automatically, and it only provides facilities for
additive decompositions." Tham số: "Smaller values allow for more rapid changes. Both trend and seasonal windows should be odd numbers."

**Dữ liệu khử mùa vụ:** "Seasonally adjusted series contain the remainder component as well as the trend-cycle. Therefore, they are not
“smooth”, and “downturns” or “upturns” can be misleading."

**§4.3:** $F_T = \max(0, 1 - \mathrm{Var}(R_t)/\mathrm{Var}(T_t+R_t))$; $F_S$ "defined similarly, but with respect to the detrended data
rather than the seasonally adjusted data". **feasts** tính $F_S$ cho **từng** thành phần mùa vụ với cùng phần dư:
`max(0, min(1, 1 - var_e/var(remainder + seas)))`.

**Cleveland et al. (1990):** "STL consists of two recursive procedures: an inner loop nested inside an outer loop"; trọng số robust
"h = 6 median(|R_v|)", bisquare; "n(s) … at least 7"; "n(t) ≥ 1.5n(p) / (1 − 1.5 n(s)^−1)"; "we do not want the trend and seasonal
components to compete for variation in the data" (tr. 20); với nhiều chu kỳ "successively estimate the components by proceeding from the
shortest-period component to the longest-period component" (tr. 14).

**MSTL:** "MSTL arranges the identiﬁed seasonal cycles in an ascending order. Then… applies the STL algorithm iteratively to each of the
identiﬁed seasonal frequencies"; cửa sổ mặc định "C and K values are set to 7 and 4" → 11, 15.

**EIA-930:** "Report all data as hourly integrated values in megawatts by hour ending time." "D = actual demand." "Please suppress
anomalous data values such as erroneous zero and large positive or negative values… leave the demand value blank". Today in Energy
2020-04-06: "published in real time, which can result in anomalous data values"; "Weekend U.S. electricity demand tends to be lower than
weekday demand because schools and many businesses are closed". Ruggles et al. (2020): "2.2% of the hourly data … are missing, and
another 0.5% are either physically implausible … or suspicious".

**CHƯA XÁC MINH:** phiên bản X-13ARIMA-SEATS hiện hành (census.gov chặn 403); định nghĩa chính thức cột `Demand (MW) (Imputed)`/
`(Adjusted)` (trang about dựng bằng JavaScript).

## API đã kiểm (statsmodels 0.15.0)

- `seasonal_decompose(x, model='additive', filt=None, period=None, two_sided=True, extrapolate_trend=0)` — docstring "This is a naive
  decomposition"; NaN đầu vào → `ValueError: This function does not handle missing values`; `extrapolate_trend='freq'` phát
  FutureWarning (bỏ ở 0.16).
- `STL(endog, period=None, seasonal=7, trend=None, low_pass=None, …, robust=False)`; trend mặc định "smallest odd integer greater than
  1.5 * period / (1 - 1.5 / seasonal)" → 47 với period 24; `fit()` mặc định `inner_iter = 2 if robust else 5`, `outer_iter = 15 if robust
  else 0` — khác khuyến nghị gốc.
- **Một NaN trong đầu vào → trend/seasonal/resid toàn NaN, không lỗi, không cảnh báo** (STL và MSTL).
- `MSTL(endog, *, periods=None, windows=None, lmbda=None, iterate=2, stl_kwargs=None)` — periods (24, 168) → windows (11, 15), cột
  `seasonal_24`, `seasonal_168` [CHẠY].
- `x13_arima_analysis` cần chương trình `x13as` ngoài → `X13NotFoundError` → chỉ nhắc, không làm lab.

## Số liệu thật của buổi [CHẠY]

- **PJM, `Demand (MW)` gốc 2024:** 8.784 giờ UTC, 2024-01-01 06:00 → 2025-01-01 05:00 (mốc cuối giờ). **47 giờ NaN** thành 2 đoạn: 22 giờ
  2024-03-10 07:00 → 03-11 04:00 và 25 giờ 2024-11-03 05:00 → 11-04 05:00 — đúng hai ngày đổi giờ. Cột `Imputed` có 46 dòng. Đỉnh
  153.121 MW lúc 2024-07-16 22:00 UTC; đáy 56.260 MW lúc 2024-11-21 17:00 UTC — giờ liền trước 94.812, liền sau 95.482 (dự báo day-ahead
  89.661) → lỗi số liệu một giờ.
- **Tự viết cổ điển:** 2×24-MA 25 trọng số (1/48, 1/24 × 23, 1/48); khác `seasonal_decompose` tối đa **0,0**; xu hướng NaN 24 giờ.
- **Cổ điển chu kỳ 24:** xu hướng trung bình theo thứ (giờ New York): T2 93.327, T3 94.611, T4 95.036, T5 94.917, T6 93.654, **T7 89.523,
  CN 88.459** → mùa vụ tuần chủ yếu vào **xu hướng**. Phương sai y 240,1 GW²; phần dư 32,4 GW². Tỷ lệ phương sai hồ sơ phần dư / phương
  sai y: thứ×giờ **0,00671**, tháng×giờ **0,10164**. Phần dư trung bình tháng 7 lúc 17h +13.037 MW; tháng 1 lúc 8h +4.577; thứ Bảy 8h
  −3.379. ACF phần dư: trễ 24 0,884; trễ 168 0,752. $F_T$ 0,828; $F_S$ 0,618.
- **MSTL (24, 168):** phần dư 16,5 GW²; thứ×giờ 0,00001; tháng×giờ 0,00062; tháng 7 17h −668; ACF phần dư trễ 24 0,365, trễ 168 −0,187.
  $F_T$ **0,888**, $F_{S,24}$ **0,829**, $F_{S,168}$ **0,415**. Biên độ mùa vụ ngày theo tháng (GW): T1 14,4; T2 13,3; T3 13,0; T4 15,8;
  T5 25,2; T6 39,1; **T7 43,3**; T8 39,6; T9 30,0; T10 18,6; T11 15,6; T12 14,5. Giờ đỉnh (New York): T1 19h, T2 8h, T3 9h, T5–T9 18h.
- **STL(period=24) mặc định:** phần dư chỉ 2,8 GW² — cửa sổ xu hướng 47 giờ đủ linh hoạt để nuốt cả nhịp tuần và thời tiết.
- **Robust — giờ hỏng 21/11/2024 17:00 UTC:** MSTL không robust phần dư −26.322 MW, mùa vụ ngày lúc 17:00 UTC ngày 20/11 −4.051; robust
  phần dư −36.323 MW, mùa vụ ngày cùng giờ 20/11 +2.117 → không robust chia khoảng 6.200 MW lỗi sang mùa vụ các ngày lân cận. Độ mạnh khi
  robust: $F_T$ 0,817, $F_{S,24}$ 0,739, $F_{S,168}$ 0,252 (phần dư robust lớn hơn nên $F$ thấp hơn).
- **Đợt nóng 15–17/7/2024 với STL hè (period 24):** phần dư lớn nhất trong đợt nóng 3.159 (không robust) / 7.838 (robust) với trend mặc
  định; 16.266 / 18.467 với trend 337 giờ → sự kiện nhiều ngày bị xu hướng hấp thụ phần lớn, robust giúp ít.
- Thời gian: MSTL cả năm ~1,7 s; robust ~10 s.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình: "classical chu kỳ 24 — mùa vụ tuần rơi hết vào phần dư". Đo thật: nhịp tuần vào **xu hướng** (T7–CN thấp hơn T4 ~6.000 MW); phần dư giữ phần nhỏ (thứ×giờ 0,0067) và phần lớn là **mùa vụ ngày đổi theo mùa** (tháng×giờ 0,10) | vừa | Sửa bước Lab 1 và "Xong khi" của lộ trình; tài liệu dạy cả hai nơi mùa vụ tuần "trốn" |
| Lab 3 "STL robust khi có đợt nắng nóng" — đợt nóng nhiều ngày bị xu hướng hấp thụ, robust giúp ít | vừa | Dùng **giờ số liệu hỏng 21/11/2024**; nêu đợt nóng như phản ví dụ ("robust giúp với điểm nhọn, không với sự kiện kéo dài") |
| Dữ liệu gốc có 47 giờ NaN ở ngày DST; STL/MSTL im lặng trả NaN | nhỏ | `lap_cho_trong` nội suy; nêu trong Lỗi thường gặp |
| FPP decomposition ở ch. 3 (không phải ch. 4) | nhỏ | Trích đúng mục |
| MSTL trích bản IJOR 2025 | nhỏ | Đọc thêm dùng DOI 2025 |
| X-13 cần binary ngoài | nhỏ | Chỉ nhắc |
| Chọn PJM (F_S tuần mạnh nhất trong 10 vùng đã thử: ERCO 0,277; TVA 0,235; DUK 0,290; ISNE 0,351; PJM 0,403 với cột Adjusted) | quyết định | PJM |
