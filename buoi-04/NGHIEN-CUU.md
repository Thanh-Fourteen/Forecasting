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

## Research viết lại (Phase 8, 2026-09-18)

Research sư phạm (KHỐI CHUNG R), không đổi code/dữ liệu/phiên bản.

| Nguồn | Truy cập | Dùng cho |
|---|---|---|
| CensusAtSchool NZ, *Suggestions for Teaching Time Series*, https://new.censusatschool.org.nz/resource/teaching-timeseries/ | 2026-09-18 | hiểu lầm hay gặp: "mùa" chỉ là bốn mùa (thật ra ngày, tuần, tháng đều là mùa); nhầm chu kỳ với mùa vụ; sa vào dao động ngắn khi tả xu hướng → hộp "Hiểu lầm hay gặp" 4.1, quiz 1 |
| Monash, *Time series* (Student Academic Success) | 2026-09-18 | cách phân biệt mùa vụ: đếm số điểm từ đỉnh tới đỉnh, số điểm cố định → mùa vụ |
| *To Cut or Not To Cut? A Systematic Exploration of Y-Axis Truncation*, CHI 2024, doi:10.1145/3613904.3642102 (chỉ tóm tắt, trang ACM chặn 403) | 2026-09-18 | trục cắt: tranh luận còn tiếp, kết luận "tuỳ nhiệm vụ đọc" → giữ quy ước khoá: số đếm/tổng từ 0, đại lượng mức chọn theo độ lớn thay đổi có ý nghĩa |
| Correll et al. 2020, Few 2008, FPP ch. 2 (đã có ở trên) | | ví dụ trục kép bằng bảng "phần trăm chiều cao hình"; ACF tính tay trên chuỗi lặp 4 bước |

Quyết định: gom 11 mục lý thuyết cũ thành 6 (năm bước đọc + ba mẫu hình; gộp/làm trơn/log; seasonal + subseries; heatmap +
boxplot; lag plot + ACF; hình nói sai). Bỏ đoạn "tỷ lệ khung hình" (chỉ còn bài tập 3), bỏ công thức heatmap (chỉ là trung bình
nhóm). Mọi trích tiếng Anh (FPP, Few, Correll, Heer & Agrawala) thay bằng diễn giải tiếng Việt.

Sửa code (không đổi chỗ hở, bộ chấm, số): bỏ `matplotlib.use("Agg")` trong `code/` và `dap-an/bieu_do.py` để notebook hiện hình
(`cham/` và `ve_hinh.py` tự đặt Agg); `dap-an/` thêm nhãn trục có đơn vị cho mọi hình (buổi dạy chính điều này); `ve_hinh.py`
vẽ lag plot một hàng 4 ô, thang log ghi số thường. Thêm `dap-an/vi_du_nho.py` (ví dụ tay 4.1–4.6) và `code/lab.ipynb`.
Số mới đã chạy: seasonal plot có **106** tuần (tính cả tuần đầu/cuối thiếu ngày; bản cũ ghi 104).

## Đọc thử (Phase 8, 2026-09-18)

Tự đọc (không subagent), theo checklist `tools/CHUAN-DE-HIEU.md`. Mọi con số và đáp án quiz tính lại bằng Python
(`dap-an/vi_du_nho.py`, script kiểm số trên `hour.csv`).

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (2.596 chữ, 12 trang, 78 cờ `kiem_de_hieu`) | 6 | — | — | — | chặn: xu hướng/mùa vụ/chu kỳ định nghĩa bằng trích FPP tiếng Anh; seasonal/subseries chỉ có trích; IQR, "tứ phân vị" không định nghĩa; công thức heatmap ký hiệu tập hợp không giải thích; "Bartlett", ±1,96/√T không giải thích; ý chính trục kép/trục cắt nằm trong trích tiếng Anh. Không hình nào có "Cách đọc hình" 5 bước |
| 1 | viết lại (6.025 chữ, 19 trang) | 0 | 3 | 4 | 10/10 có căn cứ | khó: "FPP" chưa giải thích; "±1,96/√T" ở bước 3 của hình ACF trước lời giải thích; bài tập 1 (`casual`) không làm được vì `doc_luot_thue` không giữ cột đó. Nhỏ: "tăng 2 trăm lượt mỗi ngày sau một tuần" tối nghĩa; "+43,2%" không nói của đoạn nào; "104 tuần" sai (106); ví dụ "mùa vụ" trong bảng Từ mới |
| rà gọn | biên tập viên | — | — | — | — | 4 chỗ thừa: đoạn "Gộp tần suất" 4.2 nói lại kết luận hình 4.1; câu "Cách vẽ an toàn" lặp "Tóm lại" 4.2; đoạn °C sau bảng lặp bước 1 của hình scatter; hình lag plot vuông chiếm nửa trang → một hàng 4 ô. Nhận cả 4 |
| 2 | sau sửa + cắt (6.000 chữ, 18 trang) | **0** | **0** | 3 | 10/10 | **đạt**. Rà gọn cuối: 2 chỗ lặp nhỏ (< 30 chữ: "Nói bằng lời" 4.5 nhắc lại $r_2$ đã tính — giữ, bắt buộc có thay số; bảng Lỗi thường gặp nhắc lại ý lý thuyết — giữ, dạng chẩn đoán) |

Quiz: viết lại cả 10 câu; mỗi đáp án nói vì sao đúng và vì sao từng lựa chọn khác sai; căn cứ: câu 1 → 4.1, 2 → 4.3, 3 → 4.6,
4 → 4.2, 5 → 4.2/4.4/4.5, 6 → công thức 4.5 ($r_1$ = 0,4, kiểm bằng NumPy), 7 → 4.5, 8 → ví dụ 4.4 (318; 370; 350; 380), 9 → bảng
4.3 + 4.4, 10 → 4.6. `kiem_de_hieu.py 4`: 78 → **0**. PDF 12 → **18** trang (12 hình, mỗi hình 5 bước). Lab: `kiem_tra_lab.py 4`
đạt (đáp án 8/8 xanh, code 7/8 đỏ, `lab.ipynb` chạy hết).

## Phụ lục C — viết lại (Phase 8, 2026-09-18)

Phụ lục C không có `NGHIEN-CUU.md` riêng; ghi ở đây. Khung mới cho mỗi loại hình: "Trả lời câu hỏi gì" → "Cách đọc hình" 5 bước
(bước 5 là câu mẫu) → Bẫy → Đọc đúng/đọc sai → Ví dụ có số (giữ nguyên số đã đo ở Phase 3). Thêm mục 0 "Năm bước đọc mọi hình";
sắp lại 18 loại theo thứ tự khoá dạy (1–9 dùng từ buổi 4; 10–18 ghi buổi dạy kỹ). Bỏ toàn bộ trích tiếng Anh (FPP, NIST,
Gneiting, WWRP, Few, Wilke, BoE), diễn giải tiếng Việt kèm nguồn trong ngoặc; PIT định nghĩa bằng ví dụ số. Phụ lục D trỏ "mục 6"
→ đổi thành "mục 8". 3.631 → 4.954 chữ, 9 → 12 trang; `kiem_de_hieu.py C` 0. Tự đọc trong vai học viên đã học tới buổi tương ứng
của từng mục: 0 chỗ mơ hồ về "đọc trục nào, nhìn đâu"; rà gọn: rút "Ví dụ có số" của ACF về hai kết quả (buổi 4 dữ liệu thật; buổi 7
1.000 chuỗi nhiễu trắng), bỏ các con số buổi 7 trùng với mục PACF; nhỏ còn lại: "hexbin" chưa giải thích.

## Đọc thử độc lập (Phase 11, 2026-09-18)

Phiên mới, không mang ngữ cảnh phase 8–10. Chỉ mở `tai-lieu.md` + bản quiz bỏ `<details>`; viết xong A–E mới mở `kiem-tra.md`.
Mọi ví dụ tay tính lại bằng Python; số liệu dữ liệu thật (ACF, heatmap, tổng theo thứ, tăng tháng 3→4→5/2011, tỷ số 2012/2011, $r$ theo năm)
tính lại từ `hour.csv` trong cache: khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.5 Tóm lại | "trễ bằng nửa chu kỳ ghép đỉnh với đáy" | 1 | "chu kỳ" trong bảng Từ mới là *cycle* (độ dài không cố định); ở đây nghĩa là *chu kỳ mùa vụ* $m$. Cùng chữ, hai nghĩa | khó |
| 2 | 4.2 làm trơn | "chỉ còn là một chỗ lõm xuống 34 hay 43" | 4 | 43 là "cửa sổ 7 ngày" nhưng câu trước gọi là "trung bình cả 7 ngày", không nói là cửa sổ | nhỏ |
| 3 | 4.6 scatter | "cột `temp` × 41" | 1 | `temp` là gì (nhiệt độ đã chia tỷ lệ) không nói | nhỏ |
| 4 | 4.3 | "tổng ngày trung bình chỉ chênh vài phần trăm" | 3 | T6 so CN chênh 8%; "Đọc bảng" chỉ so với T2 | nhỏ |
| 5 | 4.5 | "ACF dùng trung bình và mẫu số của cả chuỗi" | 4 | $r$ của lag plot là Pearson trên các cặp — không nói, phải tự suy | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Năm bước + ba mẫu hình**: doanh số quán phở tuần nào cũng đỉnh CN (mùa vụ $m$ = 7), mỗi năm cao hơn 5% (xu hướng), khủng hoảng 2020–2022 (chu kỳ, độ dài không cố định).
- **Gộp/làm trơn/log**: 10, 10, 0, 10, 10 → trung bình 3 điểm quanh 0 là 6,7: ngày 0 mờ đi. Log: 50 → 100 và 300 → 600 cao bằng nhau (cùng gấp đôi).
- **Seasonal vs subseries**: 3 năm doanh số quý; seasonal plot 3 đường Q1–Q4 chồng nhau; subseries 4 ô, ô Q1 chứa Q1 của 3 năm.
- **Heatmap vs boxplot**: 5 giá trị 10, 12, 11, 13, 100 → trung bình 29,2 (heatmap), trung vị 12, hộp 11–13 (boxplot).
- **Lag plot/ACF**: 1, 5, 1, 5 → trễ 1 ghép đỉnh–đáy, $r_1$ âm (−0,75); trễ 2 cùng pha, dương.
- **Hình nói sai**: 98 → 102 trên trục 96–104 trông gấp 3; trục từ 0 cho đúng +4%.

### C. Quiz mù

1 B · 2 A · 3 B · 4 B · 5 (a) heatmap giờ × thứ / ACF tới 168, (b) boxplot theo giờ (hộp dài nhất), (c) đường tổng ngày · 6 $r_1$ = 16/40 = 0,4 ·
7 sai: $r$ âm là đỉnh ghép đáy của nhịp ngày, hai nhánh, không dùng ngược dấu được; dùng trễ 24/168 · 8 trung bình 318; trung vị 370;
Q0,25 = 350; Q0,75 = 380; trung vị tả "bình thường" tốt hơn · 9 cuối tuần dời giờ (13h cao gấp đôi), tổng ngày chỉ thấp < 4% · 10 trục kép
(thang phải tuỳ chọn), trục trái cắt 90.000 (số đếm phải từ 0), tiêu đề nói quan hệ nhân quả/khăng khít; scatter: $r$ = 0,91 nhưng tháng 9
mát hơn tháng 7 mà cao nhất. Mọi câu "chắc", căn cứ: 1 → 4.1; 2 → 4.3; 3, 10 → 4.6; 4 → 4.2; 5 → 4.3–4.5; 6, 7 → 4.5; 8 → 4.4; 9 → 4.3–4.4.

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 4. Khó nhất: chữ "chu kỳ" hai nghĩa. Sửa một điều: viết "chu kỳ mùa vụ" mỗi khi nói về $m$.

### E. Dài/lặp

| # | Mục | Trích | Vì sao |
|---|---|---|---|
| 1 | 4.3 | "Tổng tháng 2012 gấp 1,41 tới 2,57 lần…" | câu đứng một mình sau "Cách đọc hình" đã kết luận cùng ý (≈ 12 chữ, không đáng kể) |

## Đọc thử độc lập Phụ lục C (Phase 11, 2026-09-18)

Vai: học viên vừa xong buổi 4 (mục 0–9) và tra lại khi tới buổi 6–8 (mục 10–13); mục 14–18 đọc lướt như tài liệu "sau này". Không có quiz.
Số ví dụ đối chiếu với buổi 4, 6, 7, 8 (đã tính lại trong phiên này): khớp.

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 8 Bẫy | "AR(1) $\rho$ = 0,8" | 1 | buổi 7 viết hệ số AR(1) là $\phi$; $\rho$ ở buổi 7 là hệ số trong hộp nghiệm đơn vị | nhỏ |
| 2 | 10 | "xu hướng–chu kỳ" | 1 | buổi 6 chỉ nói "xu hướng"; từ ghép này chưa gặp | nhỏ |
| 3 | 11 | "MA bậc $q$" | 1 | chưa dạy (mục có ghi buổi 17) | nhỏ |
| 4 | 17 | "hiệu chỉnh tốt" | 1 | cùng chữ "hiệu chỉnh" với "hiệu chỉnh bias" buổi 5, nghĩa khác; có câu "tức…" ngay sau nên đoán được | nhỏ |
| 5 | 9 bảng | "hexbin" | 1 | chưa định nghĩa | nhỏ |

Chặn 0 / khó 0 / nhỏ 5. Không khái niệm nào "không giải thích được" ở mục 0–13. E: không thấy đoạn ≥ 30 chữ lặp (mục 0 "ba câu tự hỏi"
và các "Bẫy" nói các ý khác nhau).

### Chấm, sửa, đọc lại

**Quiz mù: 10/10** khớp `kiem-tra.md`; đáp án của ta tính lại bằng Python đúng (câu 6: 0,4; câu 8: 318/370/350/380).

Sửa (viết lại câu, không chèn đoạn): (1) Tóm lại 4.5 "nửa chu kỳ" → "nửa chu kỳ mùa vụ" (cùng lỗi ở buổi 7 mục 2 và Phụ lục C mục 7);
(2) 4.2 "Trung bình cả 7 ngày" → "Cửa sổ 7 ngày (cả bảy ngày)"; (3) "Đọc bảng" 4.3 thêm chênh lớn nhất T6–CN 8%; (4) 4.5 nói $r$ lag plot
là hệ số tương quan trên các cặp; (5) Cách đọc hình scatter nói cột `temp` đã chia 41.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 11 đọc mù | 6.000 | 18 | 0 | 1 | 4 | 10/10 | 0 đáng kể |
| sau sửa, đọc lại toàn bộ | 6.036 | 18 | **0** | **0** | 0 | 10/10 | 0 đáng kể |

**Đạt.** `kiem_de_hieu.py 4` 0; `kiem_tra_lab.py 4` đạt; `kiem_tra_doc_lap.sh 4` đạt; PDF 18 trang (trần).

Sửa Phụ lục C: mục 7 "nửa chu kỳ mùa vụ"; mục 8 hệ số AR(1) viết $\phi$ cho khớp buổi 7; mục 10 "xu hướng–chu kỳ" → "xu hướng"; mục 9
giải thích hexbin. Đọc lại toàn bộ: 0 / 0 / 2 (MA chưa dạy — mục ghi buổi 17; "hiệu chỉnh tốt" khác nghĩa "hiệu chỉnh bias" nhưng có câu
"tức…" ngay sau). 4.954 → 4.955 chữ, 12 trang. **Đạt.**
