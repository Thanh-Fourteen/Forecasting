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
