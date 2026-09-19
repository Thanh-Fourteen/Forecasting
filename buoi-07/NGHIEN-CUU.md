# Nhật ký research — Buổi 7: Tự tương quan và tính dừng

- **Ngày research:** 2026-09-18
- **Nền buổi:** Python 3.12.3; numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, matplotlib 3.11.2
- **[CHẠY]** = đã chạy trong nền buổi; mọi mô phỏng ghi seed

## Nguồn đã đọc

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | FPP Pythonic §2.8–2.9, https://otexts.com/fpppy/nbs/02-graphics.html | 2026-09-18 | công thức ACF, dải ±1,96/√T |
| 2 | FPP Pythonic §5.4, https://otexts.com/fpppy/nbs/05-toolbox.html | 2026-09-18 | Ljung-Box, chọn ℓ |
| 3 | FPP Pythonic ch. 9 §9.1–9.2, https://otexts.com/fpppy/nbs/09-arima.html | 2026-09-18 | tính dừng, random walk, KPSS, sai phân, backshift |
| 4 | statsmodels — ví dụ "Stationarity and detrending (ADF/KPSS)", https://www.statsmodels.org/stable/examples/notebooks/generated/stationarity_detrending_adf_kpss.html | 2026-09-18 | bảng 4 tổ hợp |
| 5 | Zivot, "Unit Root Tests" (Econ 584), https://faculty.washington.edu/ezivot/econ584/notes/unitroot.pdf | 2026-09-18 | ADF vs KPSS, độ mạnh kiểm định, MA nghiệm đơn vị |
| 6 | Zivot, slide Econ 582 (dừng, ergodic), https://faculty.washington.edu/ezivot/econ582/econ582stationarytimeseriesslides.pdf | 2026-09-18 | dừng mạnh/yếu, ergodic |
| 7 | Nelson & Plosser (1982), J. Monetary Economics 10, 139–162, https://users.ssc.wisc.edu/~behansen/718/NelsonPlosser1982.pdf | 2026-09-18 | trend- vs difference-stationary, khử xu hướng giả |
| 8 | Nau (Duke), "Identifying the order of differencing", https://people.duke.edu/~rnau/411arim2.htm | 2026-09-18 | quy tắc sai phân thừa |
| 9 | Kwiatkowski, Phillips, Schmidt & Shin (1992), J. Econometrics 54:159–178 (IDEAS); Dickey & Fuller (1979) JASA; Said & Dickey (1984) Biometrika | 2026-09-18 | gốc kiểm định |
| 10 | statsmodels 0.15.0 docstring `acf`, `pacf`, `adfuller`, `kpss`, `acorr_ljungbox` [CHẠY] | 2026-09-18 | API |
| 11 | BLS `download.bls.gov/pub/time.series/ln/`; BLS API FAQ, https://www.bls.gov/developers/api_faqs.htm | 2026-09-18 | vì sao bỏ tỷ lệ thất nghiệp |

## Trích dẫn nguyên văn

**FPP §2.8:** $r_k = \dfrac{\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)}{\sum_{t=1}^{T}(y_t-\bar y)^2}$; xu hướng → "autocorrelations for
small lags tend to be large and positive" và "slowly decrease as the lags increase"; mùa vụ → tự tương quan lớn hơn "for the seasonal lags
(at multiples of the seasonal period)". **§2.9:** "we expect 95% of the spikes in the ACF to lie within ±1.96/√T"; "if one or more large
spikes are outside these bounds, or if substantially more than 5% of spikes are outside these bounds, then the series is probably not white
noise."

**FPP §5.4:** $Q^* = T(T+2)\sum_{k=1}^{\ell}(T-k)^{-1} r_k^2$; "We suggest using ℓ=10 for non-seasonal data and ℓ=2m for seasonal data…
if these values are larger than T/5, then use ℓ=T/5"; phân phối $\chi^2$ với ℓ bậc tự do; cảnh báo "multiple hypothesis tests, each one with a
small probability of giving a false positive."

**FPP §9.1:** "A stationary time series is one whose statistical properties do not depend on the time at which the series is observed."
"the ACF of non-stationary data decreases slowly. Also, for non-stationary data, the value of r_1 is often large and positive." Random walk:
"The forecasts from a random walk model are equal to the last observation, as future movements are unpredictable, and are equally likely to be
up or down." KPSS: "the null hypothesis is that the data are stationary, and we look for evidence that the null hypothesis is false"; "Small
p-values (e.g., less than 0.05) suggest that differencing is required." Sai phân thừa: "Beware that applying more differences than required will
induce false dynamics or autocorrelations that do not really exist." **§9.2:** $B y_t = y_{t-1}$.

**statsmodels notebook (4 tổ hợp), nguyên văn:** "Case 1: Both tests conclude that the series is not stationary - The series is not stationary";
"Case 2: Both tests conclude that the series is stationary - The series is stationary"; "Case 3: KPSS indicates stationarity and ADF indicates
non-stationarity - The series is trend stationary…"; "Case 4: KPSS indicates non-stationarity and ADF indicates stationarity - The series is
difference stationary…". **Lưu ý:** chính notebook này gọi H0 của KPSS là "trend stationary" trong khi code chạy `regression="c"` (dừng quanh
hằng số), và viết "the null hypothesis can not be rejected. Hence, the series is stationary" — coi không bác bỏ là chứng minh. Buổi dạy bảng này
như **quy tắc kinh nghiệm**, kèm phê bình.

**Zivot:** "The ADF and PP unit root tests are for the null hypothesis that a time series yt is I(1). Stationarity tests, on the other hand, are
for the null that yt is I(0)."; "the ADF and PP tests have very low power against I(0) alternatives that are close to being I(1)"; "tests that
include a constant and trend in the test regression have less power"; "first differencing yt, when it is trend stationary, produces a unit moving
average root". Ergodic (slide 582): "the time average converges to the ensemble average as the sample size gets large."

**Nelson & Plosser (1982):** "we are unable to reject the hypothesis that these series are non-stationary stochastic processes with no tendency
to return to a trend line"; phần dư của hồi quy random walk theo thời gian: "The autocorrelation function of the residuals is shown to be a
statistical artifact…".

**Nau:** "If the lag-1 autocorrelation is zero or negative, or the autocorrelations are all small and patternless, then the series does not need a
higher order of differencing. If the lag-1 autocorrelation is -0.5 or more negative, the series may be overdifferenced."; "The optimal order of
differencing is often the order of differencing at which the standard deviation is lowest."

## API đã kiểm (statsmodels 0.15.0) [CHẠY]

- `acf(x, adjusted=False, nlags=None, fft=True, alpha=None, bartlett_confint=True, ..., result_object=None)`;
  `pacf(x, nlags=None, method='ywadjusted', ...)` — **mặc định khác `plot_pacf` (`method='ywm'`)**.
- `adfuller(x, maxlag=None, regression='c', autolag='AIC', ..., result_object=None)`; `kpss(x, regression='c', nlags='auto', ...,
  result_object=None)`.
- **0.15 phát FutureWarning** nếu không truyền `result_object`: "adfuller currently returns a plain tuple… In release 0.16 or after July 2027…
  Set result_object=True". Buổi luôn truyền `result_object=True`; các trường: `statistic, pvalue, lags, nobs, critical_values, icbest, resstore`
  (ADF) và `statistic, pvalue, lags, critical_values, resstore` (KPSS).
- `kpss` phát `InterpolationWarning: The test statistic is outside of the range of p-values available in the look-up table…` khi p bị cắt ở 0,01
  hoặc 0,1 — buổi bắt cảnh báo này và trả `kpss_ngoai_bang`.
- `acorr_ljungbox(x, lags, model_df=0, ...)` trả DataFrame `lb_stat`, `lb_pvalue`; bậc tự do = lags − model_df.

## Số liệu thật của buổi [CHẠY]

- **Bốn chuỗi mô phỏng** (n = 500, seed 42, dùng chung dãy nhiễu):

| chuỗi | ACF(1) | ADF c | KPSS c | ADF ct | KPSS ct | kết luận (c) | kết luận (ct) | d theo KPSS |
|---|---|---|---|---|---|---|---|---|
| nhiễu trắng | 0,099 | 0,000 | 0,10 | 0,000 | 0,10 | dừng | dừng quanh xu hướng | 0 |
| AR(1) φ=0,7 | 0,713 | 0,000 | 0,10 | 0,000 | 0,10 | dừng | dừng quanh xu hướng | 0 |
| random walk | 0,976 | **0,073** | 0,01 | 0,214 | 0,01 | không dừng | không dừng | 1 |
| xu hướng 0,05t | 0,979 | **0,906** | 0,01 | 0,000 | 0,10 | không dừng (SAI) | dừng quanh xu hướng | 1 |

  PACF: nhiễu trắng (0,099; −0,009), AR(1) (0,713; −0,110), random walk (0,976; −0,091), xu hướng (0,979; 0,320). Số cột ACF trong 30 trễ vượt dải
  ±1,96/√500 = ±0,0877: 1, 5, 30, 30.
- **Đa kiểm định** (1.000 chuỗi nhiễu trắng n = 500, 20 trễ, seed 2026): trung bình **0,95** cột vượt dải, **62%** số chuỗi có ít nhất một cột
  vượt, tối đa 5. Dải Bartlett tại trễ 20 là 0,0910 so với 0,0877 của FPP. Ljung-Box(10) trên nhiễu trắng seed 1/2/3: p = 0,081; 0,796; 0,885.
- **Sai phân thừa:** nhiễu trắng sau sai phân ACF(1) = **−0,447**, sd 0,96 → **1,288**. Random walk sau sai phân ACF(1) = 0,100, sd 4,55 → 0,961
  (đúng liều).
- **GDP thực Mỹ** (BEA A191RX, 318 quý 1947Q1 → 2026Q2): ACF log GDP trễ 1/4/8 = 0,991 / 0,961 / 0,923. ADF ct p = 0,833, KPSS ct p = 0,01 → không
  dừng. Sai phân log ×100: trung bình 0,76%/quý, thấp nhất −8,20% (2020Q2), cao nhất +7,48% (2020Q3); ACF trễ 1/2/4 = 0,133 / 0,111 / −0,060;
  ADF p ≈ 0 nhưng **KPSS p = 0,048** → hai kiểm định mâu thuẫn; Ljung-Box(8) p = 0,0995. `so_lan_sai_phan` theo KPSS trả **2**, nhưng sai phân lần
  hai cho ACF(1) = **−0,488** và sd tăng 1,105 → 1,455 → **sai phân thừa**. Chỉ lấy 1985Q1–2019Q4 (140 quý, bỏ cú sốc COVID): ADF p ≈ 0, KPSS
  p = 0,099 → **cả hai thống nhất "dừng"**.
- **Sản lượng công nghiệp** (FRB G.17 IP.B50001.S, 300 tháng 2000-01 → 2024-12), log: dạng 'c' ADF p = 0,223, KPSS p = 0,01 → cần sai phân; dạng
  'ct' ADF p = 0,252, KPSS p = 0,10 → "không đủ bằng chứng"; sau một lần sai phân ADF p ≈ 0, KPSS p = 0,10 → d = 1.
- **Lượt thuê xe:** theo giờ ACF trễ 1/12/24/168 = 0,839 / −0,143 / 0,813 / 0,864; tổng theo ngày trễ 1/7/14/28 = 0,824 / 0,710 / 0,676 / 0,587;
  chuỗi ngày: ADF p = 0,289, KPSS p = 0,01 → d = 1 (xu hướng tăng 2011→2012).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình dùng **tỷ lệ thất nghiệp BLS**; BLS chỉ phát hành trong `ln.data.1.AllData` (390 MB) hoặc API v1 giới hạn 10 năm/lần, 25 truy vấn/ngày | vừa | Thay bằng **chỉ số sản lượng công nghiệp FRB G.17** (đã có trong danh mục, public domain, 2000–2024); đã sửa lộ trình + todos |
| statsmodels 0.15 phát FutureWarning với `adfuller`/`kpss` | nhỏ | Luôn truyền `result_object=True` |
| Notebook "4 tổ hợp" của statsmodels tự mâu thuẫn | nhỏ | Dạy như quy tắc kinh nghiệm; ghép ADF/KPSS **cùng dạng xác định**; thêm ví dụ thật mâu thuẫn (GDP) |
| FPP dùng ±1,96/√T, statsmodels mặc định dải Bartlett | nhỏ | Vẽ cả hai, nêu khác biệt |
| `pacf` mặc định `ywadjusted`, `plot_pacf` mặc định `ywm` | nhỏ | Buổi luôn khai `method="ywm"` |
| Lộ trình: "Ljung-Box trên phần dư phân rã của buổi trước" — buổi phải tự chứa | nhỏ | Sinh phần dư ngay trong buổi bằng mô phỏng và bằng chuỗi thật (sai phân log GDP) |

## Research viết lại (Phase 9, 2026-09-18)

| Khái niệm | Cách giải thích | Nguồn / căn cứ |
|---|---|---|
| ACF | tính tay $r_1$, $r_2$ trên 6 số (2, 3, 5, 6, 5, 3 → 1/3; −5/12) trước công thức | FPP §2.8 |
| PACF | tin đồn A → B → C; công thức trễ 2 $\phi_{22} = (r_2 - r_1^2)/(1 - r_1^2)$ (Durbin–Levinson bước 2) tính tay; AR(1) cho 0 | Box & Jenkins; kiểm bằng `pacf(method="ywm")` (khác một chút trên 6 số vì Yule-Walker hiệu chỉnh — không đưa vào) |
| Ljung-Box | "20 đồng xu, mỗi đồng 5%"; $Q^*$ tay với 2 trễ; $\chi^2$ trong hộp Mượn trước chỉ với bảng ngưỡng | FPP §5.4; scipy `chi2.ppf` |
| dừng | ba ví dụ đời thường (máy lạnh / chiều cao trẻ / người tung đồng xu); random walk tay từ 6 lần tung + mô phỏng độ lệch chuẩn ∝ √n | FPP §9.1; mô phỏng seed 7 |
| ADF | "đang cao thì bước sau có bị kéo xuống không" với hai chuỗi 5 số; nghiệm đơn vị trong hộp Mượn trước qua $\rho$ | Dickey & Fuller 1979 (hồi quy Δy trên y_{t−1}) — diễn giải không dùng chữ "hồi quy" (buổi 8 mới dạy) |
| ADF × KPSS | bảng 2 × 2 có "nghĩa là gì" từng ô, ghi rõ là quy tắc kinh nghiệm | FPP §9.1; statsmodels "Stationarity and detrending" (đã phê bình ở bản cũ) |
| sai phân thừa | tay: 2, −1, 0, 1, −2, 0 → sd 1,41 → 2,41, $r_1$ ≈ −0,50; một ngưỡng thống nhất "gần −0,5" | Nau (Duke) |

Kiểm định/$H_0$/p-value/α đã dạy ở buổi 2 → nhắc lại ở mục 2 (không phải "Mượn trước"); chỉ **nghiệm đơn vị** và **$\chi^2$** là mượn trước.

**Sửa lỗi bản cũ** (chạy lại):

- **Lượt thuê theo ngày**: bản cũ tạo chuỗi ngày bằng `resample(...).sum(min_count=24).dropna()` → rút 76 ngày khỏi giữa chuỗi, nên
  `diff(7)` và ACF so những ngày **không cách nhau 7 ngày**. Trên lưới ngày liên tục (`min_count=12` + nội suy 3 ngày) ACF theo ngày
  **không có đỉnh ở 7** ($r_6$ = 0,775 > $r_7$ = 0,760) — câu cũ "chỉ còn đỉnh ở 7, 14, 21" sai; bảng sai phân mùa vụ theo ngày cũ
  (0,373/0,436…) cũng sai. Thay bằng bảng **theo giờ** $\log(1+y)$, $m$ = 168: sd 1,430 → sai phân thường 0,643 (còn $r_{168}$ = 0,767) →
  sai phân 168 0,589 → 168 rồi 1 0,427 ($r_1$ = −0,249). Theo ngày, chỉ sai phân thường cho sd thấp nhất (0,330) — thành bài tập 1.
  `ve_hinh.py` sửa lưới ngày; thêm `bang_sai_phan_gio`; thêm nhãn trục cho mọi hình.
- **Quiz câu 5** (`phan-hoi-hoc-vien.md`): đổi thành chuỗi có trung bình tròn 2, 4, 6, 8, 6, 4, 2, 0 → $r_1$ = 24/48 = 0,5 (kiểm Python).
- Ngưỡng sai phân thừa thống nhất "gần −0,5" (bản cũ lẫn −0,5 và −0,45).
- Ergodic → hộp Nâng cao.

## Đọc thử (Phase 9, 2026-09-18)

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (2.131 chữ, 10 trang, 64 cờ) | 7 | — | — | — | như baseline trong `todos/phase-09.md`: kiểm định/$H_0$/p-value không nhắc lại, nghiệm đơn vị, AR(1), $\chi^2$, trích Zivot/Nau/FPP tiếng Anh, dừng yếu/mạnh định nghĩa bằng Cov; quiz câu 5 đáp án sai |
| 1 | viết lại (4.890 chữ) | 0 | 2 | 4 | 10/10 có căn cứ | khó: vì sao PACF chia $1 - r_1^2$ (nói lửng); tình huống 2 của Tự kiểm tra 4.4 mơ hồ. Nhỏ: một dòng bắt đầu bằng "1." bị markdown hiểu thành danh sách; nhãn "Ví dụ số nhỏ" đứng trước công thức PACF |
| rà gọn | biên tập viên | — | — | — | — | 1 chỗ lặp: "Tóm lại" 4.3 nói lại ý đếm cột của Trực giác và hình → rút |
| 2 | sau sửa (4.922 chữ, 15 trang) | **0** | **0** | 3 | 10/10 | **đạt** |

Quiz: viết lại cả 10 đáp án; câu 8 đổi sang bảng sai phân theo giờ. Căn cứ: 1 → 4.5, 2 → 4.1/4.2, 3 → 4.3, 4 → 4.4, 5 → 4.1, 6 → 4.5,
7 → 4.6, 8 → 4.6, 9 → 2/4.5/4.6, 10 → 4.5. `kiem_de_hieu.py 7`: 64 → **0**. PDF 10 → **15** trang. Lab: `kiem_tra_lab.py 7` đạt (đáp án
9/9, code 5/9 đỏ, notebook chạy hết).

## Đọc thử độc lập (Phase 11, 2026-09-18)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Ví dụ tay tính lại bằng Python ($r_1$ 1/3, $r_2$ −5/12,
tự kiểm 0,25/−0,5, PACF 0/0,2, $Q^*$ 5,16 p 0,076, đồng xu p 0,011, sai phân thừa 1,41 → 2,41 và $r_1$ −0,498, $\rho$ 7 → 4,9): khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 2 Nhắc lại | "trễ bằng nửa chu kỳ ghép đỉnh với đáy" | 1 | cùng lỗi buổi 4: "chu kỳ" ở đây là chu kỳ mùa vụ, không phải *cycle* (4.4 dùng "chu kỳ" theo nghĩa *cycle*) | nhỏ |
| 2 | 4.5 GDP | "hiệu log liên tiếp × 100, tức phần trăm tăng mỗi quý" | 8 | vì sao hiệu log ≈ phần trăm chưa nhắc lại (buổi 5 chỉ ở hộp Nâng cao) | nhỏ |
| 3 | 4.4 Định nghĩa | "Chuỗi có chu kỳ … vẫn có thể dừng" | 4 | ngược trực giác, không có một câu vì sao | nhỏ |
| 4 | 4.6 | "Quy tắc của FPP (hàm `ndiffs`)" | 7 | `ndiffs` là gì, ở thư viện nào | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **ACF**: 1, 3, 3, 1 → trung bình 2, lệch −1, 1, 1, −1, $r_1$ = (−1 + 1 − 1)/4 = −0,25.
- **PACF**: $r_1$ = 0,8, $r_2$ = 0,64 → PACF(2) = 0: AR(1).
- **Ljung-Box**: $T$ = 50, hai trễ, $r_1$ = 0,3, $r_2$ = 0 → $Q^*$ = 50 × 52 × 0,09/49 ≈ 4,78 < 5,99: chưa đủ bằng chứng.
- **Dừng**: mực nước hồ có đập xả tràn (dừng) vs vị trí người say (random walk).
- **ADF/KPSS**: ADF p 0,01 + KPSS p ≥ 0,1 → dừng; ADF p 0,6 + KPSS p 0,01 → không dừng, sai phân.
- **Sai phân thừa**: 1, −1, 1, −1 (đã dừng) → −2, 2, −2: độ lệch chuẩn tăng, $r_1$ âm mạnh.

### C. Quiz mù

1 B · 2 B · 3 B · 4 C · 5 trung bình 4, mẫu số 48, tử số 24 → $r_1$ = 0,5 · 6 dừng quanh xu hướng (dạng "ct" hai kiểm định đồng ý) → khử xu hướng,
không sai phân · 7 sai phân thừa (hai dấu hiệu) → dừng ở một lần · 8 sai phân mùa vụ trước (168), kiểm ACF ở 24/168 + độ lệch chuẩn; rồi sai phân
thường nếu KPSS còn bác bỏ, kiểm $r_1$ không tới −0,5 và độ lệch chuẩn còn giảm · 9 (1) không bác bỏ ≠ chứng minh nghiệm đơn vị, phải chạy KPSS;
(2) sai phân tới khi ADF bác bỏ → lần hai là thừa ($r_1$ −0,488, độ lệch chuẩn 1,105 → 1,455) · 10 cả giai đoạn có dao động mạnh trước 1985 và
sốc 2020 → KPSS bác bỏ vì độ dao động đổi, không vì random walk; báo cả hai giai đoạn, ghi "mâu thuẫn" và lý do. Căn cứ: 1, 6, 9, 10 → 4.5 (+ 4.6
cho 9); 2 → 4.1–4.2; 3 → 4.3; 4 → 4.4; 5 → 4.1; 7, 8 → 4.6. Mọi câu "chắc".

### D. Tổng kết

Chặn 0 / khó 0 / nhỏ 4. Sửa một điều: "nửa chu kỳ mùa vụ" ở mục 2.

### E. Dài/lặp

Không thấy đoạn ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù: 10/10** khớp `kiem-tra.md` (câu 5: 0,5).

Sửa: mục 2 "nửa chu kỳ mùa vụ"; 4.4 thêm vì sao chuỗi có chu kỳ vẫn dừng được (không biết trước đỉnh/đáy, theo FPP §9.1); 4.5 hiệu log
"gần bằng phần trăm vì log 1,01 ≈ 0,01"; 4.6 bỏ "(hàm `ndiffs`)" không giải thích.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 11 đọc mù | 4.922 | 15 | 0 | 0 | 4 | 10/10 | 0 |
| sau sửa, đọc lại toàn bộ | 4.946 | 15 | **0** | **0** | 0 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 7` 0; lab, tự chứa đạt.
