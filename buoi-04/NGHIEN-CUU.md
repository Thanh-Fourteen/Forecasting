# Nhật ký research — Buổi 4: Đọc và vẽ biểu đồ chuỗi thời gian

- **Ngày research:** 2026-09-18
- **Nền buổi:** Python 3.12.3; numpy 2.5.3, pandas 3.0.5, matplotlib 3.11.2, statsmodels 0.15.0. `khung_bo = ["ve"]` —
  học viên tự viết bộ biểu đồ, không phát `tv.ve`.
- **[CHẠY]** = đã chạy trong nền buổi; mọi con số của tài liệu lấy từ các lần chạy này (không có ngẫu nhiên).

## Nguồn đã đọc

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | FPP Pythonic ch. 2 "Time series graphics", https://otexts.com/fpppy/nbs/02-graphics.html (lấy bằng curl, tìm văn bản) | 2026-09-18 | định nghĩa xu hướng/mùa vụ/chu kỳ; seasonal, subseries, lag plot; ACF; nhiễu trắng |
| 2 | FPP3 ch. 2, https://otexts.com/fpp3/ (`gg_season`, `gg_subseries`, `gg_lag`) | 2026-09-18 | đối chiếu |
| 3 | Correll, Bertini & Franconeri (2020), "Truncating the Y-Axis: Threat or Menace?", CHI 2020, https://arxiv.org/abs/1907.02035 | 2026-09-18 | trục y cắt |
| 4 | Few (2008), "Dual-Scaled Axes in Graphs: Are They Ever the Best Solution?", https://www.perceptualedge.com/articles/visual_business_intelligence/dual-scaled_axes.pdf | 2026-09-18 | trục kép |
| 5 | Muth (2018, cập nhật sau), Datawrapper "Why not to use two axes", https://www.datawrapper.de/blog/dualaxis/ | 2026-09-18 | trục kép, sắc thái |
| 6 | Uncharted, "Why Two Y-Axes (Y2Y)", https://uncharted.software/assets/WhyTwoYAxes_Y2Y.pdf | 2026-09-18 | phản biện |
| 7 | Heer & Agrawala (2006), "Multi-Scale Banking to 45 Degrees", IEEE TVCG 12(5), https://idl.uw.edu/papers/banking | 2026-09-18 | tỷ lệ khung hình |
| 8 | Datawrapper, "What to consider when using a log scale" (2018-05-31), https://www.datawrapper.de/blog/weeklychart-logscale | 2026-09-18 | thang log |
| 9 | Alarcon Falconi et al. (2020), IJERPH, https://pmc.ncbi.nlm.nih.gov/articles/PMC7460497/ (qua WebFetch — có thể diễn giải nhẹ) | 2026-09-18 | gộp tần suất |
| 10 | statsmodels 0.15.0 release notes, https://www.statsmodels.org/stable/release/index.html | 2026-09-18 | `plot_ccf`, `seasonal_diagnostic_plot` mới |
| 11 | seaborn 0.13.0 what's new, https://seaborn.pydata.org/whatsnew/v0.13.0.html | 2026-09-18 | đổi API categorical |
| 12 | UCI Bike Sharing (id 275) — trang, API JSON, `Readme.txt` trong zip | 2026-09-18 | biến, chuẩn hoá nhiệt độ |
| 13 | Ortigossa et al. (2025), "Time Series Information Visualization — A Review", arXiv:2507.14920 (chỉ abstract) | 2026-09-18 | đọc thêm |

## Trích dẫn nguyên văn

**FPP §2 — ba mẫu hình.** Trend: "A trend exists when there is a long-term increase or decrease in the data. It does not have
to be linear." Seasonal: "A seasonal pattern occurs when a time series is affected by seasonal factors such as the time of the
year, the day of the week or the hour of the day. Seasonality is always of a fixed and known period." "(Note that one series can
have more than one seasonal pattern.)" Cyclic: "A cycle occurs when the data exhibit rises and falls that are not of a fixed
frequency … The duration of these fluctuations is usually at least 2 years." "If the fluctuations are not of a fixed frequency
then they are cyclic; if the frequency is unchanging and associated with some aspect of the calendar, then the pattern is
seasonal."

**Seasonal plot:** "the data are plotted against the individual “seasons” in which the data were observed" — "shows the
underlying seasonal pattern more clearly and helps identify years when the pattern changes." **Subseries:** "the data for each
season are collected together in separate mini time plots" — "especially useful in identifying changes within particular
seasons." **Lag plot:** "Each graph shows y_t plotted against y_{t-k}"; "The negative relationship seen for lags 2 and 6 occurs
because peaks (in Q4) are plotted against troughs (in Q2)." **ACF:** "The slow decrease in the ACF as the lags increase is due to
the trend, while the “scalloped” shape is due to the seasonality." **Nhiễu trắng:** "we expect 95% of the spikes in the ACF to lie
within ±1.96/√T". **Scatter:** "The correlation coefficient only measures the strength of the linear relationship between two
variables, and can sometimes be misleading."

**Code FPP Pythonic dùng:** seasonal plot = `sns.lineplot(..., hue="Year")`; subseries = `plt.subplots(1, 12, sharey=True)` +
`axhline(mean)`; lag = lưới `sns.scatterplot` trên `y.shift(lag)` có đường 45°; ACF = `statsmodels.graphics.tsaplots.plot_acf`.
Sách **không** dùng `month_plot`.

**Trục y cắt — Correll et al. (2020):** "the subjective impact of axis truncation is persistent across visualizations designs,
even for designs with explicit visual cues that indicate truncation has taken place. We suggest that designers consider the scale
of the meaningful effect sizes and variation they intend to communicate". "we cannot rely on visual indicators of broken or
truncated axes to counteract the exaggeration". Kết luận **không** phải "luôn bắt đầu từ 0".

**Trục kép — Few (2008):** "When lines are associated with different quantitative scales, however, their intersection means
nothing." Đề xuất đánh chỉ số: "convert all sets of values to a common quantitative scale by displaying percentage differences
between each value and a reference (or index) value." **Datawrapper:** "The scales of dual axis charts are arbitrary and can
therefore (deliberately) mislead readers about the relationship between the two data series." — nhưng trang nay mở đầu bằng
"Since then, we've changed our minds… people who've learned to read them correctly (in financial services, for example) aren't
misled by them." **Y2Y:** "earlier research has over-generalized the recommendations against the use of dual y-axis charts."

**Tỷ lệ khung hình — Heer & Agrawala:** Cleveland tối ưu tỷ lệ "such that the average absolute orientation of line segments in the
chart is equal to 45 degrees"; ví dụ CO₂: tỷ lệ 1,17 "reveals an accelerating increase", tỷ lệ 7,87 "facilitates closer
inspection of seasonal fluctuations".

**Thang log — Datawrapper:** "same distances on a log scale show … the same percentage growth or decline."

**Gộp tần suất — Alarcon Falconi et al.:** "By choosing to aggregate data from daily to weekly or monthly counts, the researcher is
essentially smoothing over the short-term variability"; đỉnh dịch ước lượng lệch "as much as 2.5 months".

**Bike Sharing:** "hr : hour (0 to 23)", "weekday : day of the week", "workingday : if day is neither weekend nor holiday is 1,
otherwise is 0." Hai công thức nhiệt độ mâu thuẫn: Readme "divided to 41 (max)"; trang "(t-t_min)/(t_max-t_min), t_min=-8,
t_max=+39 (only in hourly scale)". Giấy phép CC BY 4.0, DOI 10.24432/C5W894.

**CHƯA XÁC MINH:** câu nguyên văn của Cleveland, McGill & McGill (1988); Tufte "Compared to what?" (chỉ qua Wikipedia); nguồn học
thuật cho "làm trơn che ngoại lai" → tài liệu chứng minh bằng chạy thật, không trích.

## API đã kiểm (statsmodels 0.15.0, pandas 3.0.5, matplotlib 3.11.2, seaborn 0.13.2, plotly 7.1.0)

- `month_plot(x, dates=None, ylabel=None, ax=None)` — mã nguồn vẽ mỗi tháng một đoạn và `hlines` trung bình: là **subseries
  plot** dù docstring gọi "Seasonal plot of monthly data"; chỉ nhận dữ liệu tháng/quý.
- `plot_acf(x, ..., alpha=0.05, ..., bartlett_confint=True)` — dải Bartlett rộng dần theo độ trễ, khác ±1,96/√T của FPP.
- pandas 3.0.5 vẫn có `pandas.plotting.lag_plot`, `autocorrelation_plot` (vẽ cả dải 95% và 99%).
- seaborn 0.13.2 `boxplot` phát `MatplotlibDeprecationWarning: vert: bool was deprecated in Matplotlib 3.11` từ bên trong seaborn
  → buổi dùng `ax.boxplot` của matplotlib, không thêm seaborn.
- plotly 7.1.0 xuất PNG cần `kaleido>=1` → không dùng plotly trong hình tài liệu; nhắc như công cụ tương tác.
- Thư viện heatmap lịch: `july` 0.1.3 hỏng trên matplotlib 3.11; `calplot` ngừng từ 2022; `plotly-calplot` đòi plotly<6 → tự
  dựng bằng `pivot_table` + `imshow`.

## Số liệu thật của buổi [CHẠY]

- `hour.csv` sha256 `e03de4ee4ef4…`, 17.379 dòng, 2011-01-01 00:00 → 2012-12-31 23:00. Lưới giờ đầy đủ 17.544 → **165 giờ
  thiếu**, rải trên 76 ngày; 29/10/2012 (bão Sandy) chỉ còn 1 giờ (22 lượt), 30/10/2012 còn 11 giờ (1.096 lượt).
- Cột `weekday` của tệp: 0 = Chủ nhật (2011-01-02); `DatetimeIndex.dayofweek`: 0 = thứ Hai.
- **Heatmap thứ×giờ** (trung bình lượt): 8h — T2 412, T3 472, T4 488, T5 489, T6 462, T7 114, CN 84; 13h — T2 206, T7 385, CN 375;
  17h — T3 544, T7 334, CN 319.
- **Boxplot:** trung vị ngày làm việc 8h 463, 17h 539 (IQR 17h 347,5–703,5); ngày nghỉ 8h 94, 13h 367 (IQR 235,5–493).
- **Lag plot** (tương quan cặp không NaN): trễ 1 0,843; trễ 12 −0,144; trễ 24 0,819; trễ 168 0,876.
- **ACF** (mẫu số trên cả chuỗi, bỏ cặp NaN): r₁ 0,839, r₂ 0,590, r₆ 0,009, r₁₂ −0,143, r₂₃ 0,701, r₂₄ 0,813, r₂₅ 0,705, r₄₈ 0,680,
  r₁₄₄ 0,786, r₁₆₈ 0,864, r₃₃₆ 0,854; dải ±1,96/√T = ±0,0149 (T = 17.379).
- **Scatter nhiệt độ × lượt/ngày:** tương quan theo năm 2011 0,771; 2012 0,714; gộp hai năm 0,627. Quanh 24,6 °C: 2011 trung bình
  4.316, 2012 6.751 lượt/ngày.
- **Tháng 2012 / cùng tháng 2011:** 2,53; 2,14; 2,57; 1,84; 1,44; 1,41; 1,44; 1,57; 1,72; 1,61; 1,49; 1,42.
- **Biểu đồ gây hiểu nhầm** (tháng 2012): lượt thuê 96.744 (T1) → 218.573 (T9); nhiệt độ (temp×41) 11,3 → 30,8 (T7) → 13,2 (T12);
  tương quan 12 tháng r = 0,91; T9 25,4 °C nhưng lượt thuê cao nhất năm.
- **Tổng ngày theo thứ** (655 ngày đủ 24 giờ): T2 4.708, T3 4.909, T4 4.909, T5 4.899, T6 4.933, T7 4.653, CN 4.523.
- **Làm trơn:** trung bình trượt 7 ngày có tâm tại 29/10/2012 = 4.632 trong khi ngày đó 22.
- **Thang log** (tháng 2011): tăng tuyệt đối lớn nhất T4→T5 +40.951; tăng tỷ lệ lớn nhất T3→T4 +48,1% (T4→T5 +43,2%).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Boxplot/violin qua seaborn phát cảnh báo deprecation với matplotlib 3.11 | nhỏ | Dùng `matplotlib.axes.Axes.boxplot`; nhắc seaborn trong Đọc thêm |
| "Khi nào dùng plotly" — plotly 7 cần kaleido để xuất ảnh tĩnh | nhỏ | Chỉ nêu nguyên tắc (tương tác để khám phá, tĩnh để báo cáo); không cài plotly |
| `month_plot` của statsmodels thực chất là subseries plot | nhỏ | Nêu trong Lỗi thường gặp; tự viết cả seasonal lẫn subseries |
| Trục kép: nguồn 2018 "không bao giờ dùng", nay có sắc thái | nhỏ | Dạy mặc định: đánh chỉ số hoặc tách bảng; nêu sắc thái |
| Trục y cắt: bằng chứng là "chọn phạm vi theo độ lớn hiệu ứng", không phải "luôn từ 0" | nhỏ | Dạy: số đếm/tổng bắt đầu từ 0; mức như nhiệt độ không cần |
| Subseries theo tháng chỉ có 2 năm | nhỏ | Mỗi ô tháng vẽ chuỗi tổng theo ngày của cả hai năm (≈ 60 điểm) + đường trung bình |
| statsmodels 0.15 thêm `seasonal_diagnostic_plot`, `plot_ccf` | bổ sung | Nhắc; `plot_ccf` dùng ở buổi 8 |
