# Nhật ký research — Buổi 8: Tương quan giữa các chuỗi

- **Ngày research:** 2026-09-18
- **Nền buổi:** Python 3.12.3; numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, scikit-learn 1.9.1, matplotlib 3.11.2
- **[CHẠY]** = đã chạy trong nền buổi; seed ghi kèm

## Nguồn đã đọc

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | Granger & Newbold (1974), J. Econometrics 2(2):111–120, toàn văn https://gwern.net/doc/economics/1974-granger.pdf | 2026-09-18 | hồi quy giả |
| 2 | Granger, Hyung & Jeon (UCSD DP 98-25), https://economia.uc3m.es/jgonzalo/teaching/timeseriesMA/spuriousregressiongranger-reading.pdf | 2026-09-18 | tổng hợp, Phillips (1986) |
| 3 | Phillips (1986), J. Econometrics 33(3):311–340 (abstract, IDEAS) | 2026-09-18 | lý thuyết tiệm cận |
| 4 | Penn State STAT 510, Lesson 8 & 9, https://online.stat.psu.edu/stat510/Lesson09.html | 2026-09-18 | prewhitening, quy ước CCF |
| 5 | R `stats::acf`/`ccf` docs, https://stat.ethz.ch/R-manual/R-devel/library/stats/html/acf.html | 2026-09-18 | quy ước lag của R |
| 6 | scikit-learn 1.9.1 `mutual_info_regression` | 2026-09-18 | MI, k-NN estimator |
| 7 | Gohil et al. (2025), "Cross Mutual Information", arXiv:2507.15372 | 2026-09-18 | hoán vị theo khối |
| 8 | scipy 1.18.1 `pearsonr`, `spearmanr`, `kendalltau`, `chatterjeexi` (thêm ở 1.15) | 2026-09-18 | hệ số tương quan |
| 9 | Anscombe (1973), *The American Statistician* 27(1):17–21 (bảng số qua R `datasets::anscombe`) | 2026-09-18 | bộ tứ Anscombe |
| 10 | EIA — "Degree days", https://www.eia.gov/energyexplained/units-and-calculators/degree-days.php; Today in Energy id=42915 | 2026-09-18 | CDD/HDD, mốc 65 °F |
| 11 | FPP Pythonic §2.6, §7.3 (spurious regression), §7.6 (ex-ante vs ex-post), §7.8, ch. 10 | 2026-09-18 | tương quan ≠ nhân quả, biến chưa biết tương lai |
| 12 | Wikipedia "Granger causality"; Maziarz (2015), J. Philosophical Economics VIII(2):86–105, https://jpe.episciences.org/10676/pdf | 2026-09-18 | phê bình Granger |
| 13 | statsmodels 0.15.0 release notes (bỏ `verbose`, VIF chuẩn hoá), `grangercausalitytests`, `variance_inflation_factor` [CHẠY] | 2026-09-18 | API |
| 14 | Giles (2011), "Testing for Granger Causality", https://davegiles.blogspot.com/2011/04/testing-for-granger-causality.html; Toda & Yamamoto (1995) | 2026-09-18 | yêu cầu tính dừng |

## Trích dẫn nguyên văn

**Granger & Newbold (1974):** "It would, for example, be easy to quote published equations for which R2 = 0.997 and the Durbin-Watson statistic (d)
is 0.53."; "Using the traditional t test at the 5 % level, the null hypothesis of no relationship between the two series would be rejected
(wrongly) on approximately three-quarters of all occasions."; "a high value for R2 or R2, combined with a low value of d, is no indication of a true
relationship."; "if a regression equation relating economic variables is found to have strongly autocorrelated residuals… the only conclusion that
can be reached is that the equation is mis-specified, whatever the value of R2 observed."; "we recommend taking first differences of all variables
that appear to be highly autocorrelated" — kèm cảnh báo "we are not advocating first differencing as a universal sure-fire solution".
**Quan trọng:** quy tắc "$R^2 > DW$ thì nghi hồi quy giả" **không có trong bài báo**; đó là quy tắc kinh nghiệm được gán cho họ (ví dụ ghi chú bài
giảng Aldrich, Southampton). Tài liệu trình bày đúng như vậy.

**Phillips (1986):** "the usual t ratio significance tests do not possess limiting distributions but actually diverge as the sample size T
approaches infinity. The Durbin-Watson statistic, on the other hand, converges in probability to zero."

**Penn State STAT 510, Lesson 9.1:** "the CCF is affected by the time series structure of the x-variable and any "in common" trends the x and y
series may have over time. One strategy for dealing with this difficulty is called "pre-whitening.""; ba bước: mô hình cho x → lọc y bằng mô hình
của x → CCF giữa phần dư; "Pre-whitening is just used to help us identify which lags of x may predict y."

**Quy ước CCF.** R: "The lag k value returned by ccf(x, y) estimates the correlation between x[t+k] and y[t]." statsmodels 0.15
`ccf(x, y)`: "the element at index k is the correlation between {x[k], x[k+1], …, x[n]} and {y[0], y[1], …, y[m-k]}" — tức corr(x_{t+k}, y_t), chỉ
k ≥ 0. **[CHẠY]** với $y_t = x_{t-3}$: `ccf(x, y)` không có đỉnh; `ccf(y, x)` đỉnh tại 3 (r = 0,959). Hàm mới `pccf` của 0.15 dùng thứ tự **ngược
lại** ("correlation between x_t and y_{t+h}").

**scikit-learn `mutual_info_regression`:** "relies on nonparametric methods based on entropy estimation from k-nearest neighbors distances";
`n_neighbors=3` — "Higher values reduce variance of the estimation, but could introduce a bias"; kết quả tính bằng **nat**; "True mutual information
can't be negative. If its estimate turns out to be negative, it is replaced by zero."

**Gohil et al. (2025):** "A problem often encountered in performing statistical significance testing with time series data is autocorrelation of the
samples, such that they are not independent."; "We adopt a block shuffle permutation to build the null distribution."

**EIA:** "Degree days compare the mean… outdoor temperature to a standard temperature; we use 65° Fahrenheit (F) in the United States."; "A cooling
degree day indicates a hot day… A heating degree day indicates a cold day". **FPP ch. 10:** "more electricity is used on cold days due to heating and
hot days due to air conditioning. The higher demand on cold and hot days is reflected in the U-shape".

**FPP §2.6:** "The correlation coefficient only measures the strength of the linear relationship between two variables, and can sometimes be
misleading." **§7.3:** "Regressing non-stationary time series can lead to spurious regressions… High R^2 and high residual autocorrelation can be signs
of spurious regression… Cases of spurious regression might appear to give reasonable short-term forecasts, but they will generally not continue to work
into the future." **§7.6:** "Ex-ante forecasts are those that are made using only the information that is available in advance… in order to generate
ex-ante forecasts, the model requires forecasts of the predictors."; "Ex-post forecasts are those that are made using later information on the
predictors… These are not genuine forecasts". **§7.8:** "It is important not to confuse correlation with causation… A variable x may be useful for
forecasting a variable y, but that does not mean x is causing y."

**Granger ≠ nhân quả.** Wikipedia: "Granger-causality is better described as "precedence", or, as Granger himself later claimed in 1977, "temporally
related"."; "If both X and Y are driven by a common third process with different lags, one might still fail to reject the alternative hypothesis of
Granger causality." Maziarz (2015): "Rejecting the null in one of the tests can be interpreted as either a true causal relation, opposite direction of
the true causation, instant causality, time series cointegration, not frequent enough sampling, etc."

**CHƯA XÁC MINH:** trích dẫn nguyên văn Yule (1926) (bản quét không có lớp text); bài "Christmas cards Granger-cause Christmas" (sau tường phí);
O'Brien (2007) về ngưỡng VIF (chỉ có abstract qua snippet).

## API đã kiểm [CHẠY]

- `statsmodels.tsa.stattools.ccf(x, y, adjusted=True, fft=True, *, nlags=None, alpha=None)` — chỉ trả k ≥ 0 theo quy ước corr(x_{t+k}, y_t).
  Buổi tự viết `ccf_tu_viet(x, y)[k] = corr(x_t, y_{t+k})` và **đối chiếu**: `ccf_tu_viet(cdd, tai)` khớp `ccf(tai, cdd)` tới 0,001.
- `grangercausalitytests(x, maxlag, addconst=True)` — **tham số `verbose` đã bị bỏ ở 0.15** ("the verbose parameter (deprecated since 0.14) has been
  removed"); kiểm "cột 2 gây ra cột 1"; trả dict theo trễ, khoá `np.int64`.
- `AutoReg(x, lags=p).fit().params` — phần tử 0 là hằng số; **không còn tham số `old_names`** (lỗi `TypeError` nếu truyền).
- `variance_inflation_factor(exog, idx, *, standardize=True)` — 0.15 chuẩn hoá ma trận thiết kế trước khi tính, nên lời khuyên cũ "phải thêm cột hằng
  số" không còn cần.
- `mutual_info_regression(X, y, random_state=...)` — phải đặt `random_state` để tái lập (hàm thêm nhiễu nhỏ).

## Số liệu thật của buổi [CHẠY]

- **Dữ liệu:** ERCO 8.784 giờ 2024 (không NaN); nhiệt độ Dallas (trung bình năm 20,54 °C) và Houston (21,98 °C), mỗi tệp 8.784 giờ; ghép được **8.777**
  giờ (lệch ở hai đầu do múi giờ). CPI-U × dân số: 420 tháng 1990-01 → 2024-12.
- **Tình huống 1 — tương quan giả:** r(mức) = **0,9744**; hồi quy CPI theo dân số: R² = 0,9495, t = **88,6**, **DW = 0,0051**; r(sai phân) = **−0,2071**;
  r(tăng trưởng so cùng kỳ) = −0,029.
- **Tình huống 2 — phi tuyến:** Pearson 0,616, Spearman 0,733, Kendall 0,572, MI = **0,862 nat**. R² hồi quy tuyến tính theo nhiệt độ **0,379**; theo
  CDD + HDD (mốc 18,33 °C) **0,813**; mốc tối ưu 19,5 °C cho 0,814. Chia theo mốc: dưới 18,33 °C r = **−0,649** (2.877 giờ), trên mốc r = **+0,910**
  (5.900 giờ). Kiểm ý nghĩa MI bằng hoán vị **theo khối 168 giờ** (100 lần, seed 0): MI thật 0,862, ngưỡng 95% của phân phối rỗng 0,124, p = 0,0099.
- **Tình huống 3 — CCF và prewhitening:** CCF thô CDD → tải: r₀ = 0,848, r₁ = **0,863** (đỉnh), r₂₄ = **0,828**, r₄₈ = 0,801 — rộng và còn nhịp ngày.
  Sau prewhitening AR(48) của CDD: đỉnh ở **trễ 0** (r = 0,205), r₁ = 0,163, r₃ = 0,119, r₂₄ = **0,061**; dải 2/√n = 0,0214. Với AR(24) thì r₂₄ còn
  0,113 — bậc phải đủ phủ nhịp ngày. Kiểm quy ước trên dữ liệu mô phỏng (seed 1, $y_t = x_{t-3}$): `ccf_tu_viet` đỉnh đúng ở 3.
- **Tình huống 4 — tương quan trượt (theo ngày):** cả năm 0,621; cửa sổ 90 ngày: thấp nhất **−0,801** (kết thúc 31/3/2024), cao nhất **+0,968**
  (14/10/2024); cửa sổ 30 ngày thấp nhất −0,971 (7/2/2024).
- **Tình huống 5 — Granger:** CDD → tải p ≈ 0 và tải → CDD p ≈ 0 (trễ 1–4, ssr-F). Tương quan chéo tại trễ 1: CDD dẫn tải 0,863; tải "dẫn" CDD 0,814.
  Hồ sơ giờ trong ngày của hai chuỗi có cùng nhịp 24 giờ → đây là **mùa vụ chung**, không phải nhân quả.
- **Bộ tứ Anscombe** (số chép từ bài báo): cả bốn có r ≈ 0,816–0,817 và hồi quy y ≈ 3,00 + 0,50x; Spearman 0,818 / 0,691 / 0,991 / 0,500; MI (k-NN,
  n = 11) 0,329 / 0,403 / 0,481 / 0,121.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình: "tải điện × nhiệt độ: **Pearson thấp**". Đo thật trên ERCOT cả năm: Pearson 0,616 (không thấp) vì Texas thiên về làm mát | vừa | Dạy bằng **R²** (0,379 → 0,813) và hai nhánh (−0,649 / +0,910) thay vì "Pearson thấp"; nêu rõ hình chữ U **lệch** |
| Lộ trình: "hai chuỗi kinh tế không liên quan" — random walk không drift hiếm khi cho r > 0,9 | nhỏ | Dùng cặp thật CPI-U × dân số (r = 0,974) + mô phỏng Granger–Newbold trong bài tập |
| Quy ước `ccf` của statsmodels ngược với trực giác "x dẫn y" | nhỏ | Tự viết `ccf_tu_viet`, đối chiếu `ccf(y, x)`; nêu trong Lỗi thường gặp |
| statsmodels 0.15 bỏ `verbose` của `grangercausalitytests` | nhỏ | Code không dùng; nêu vì tài liệu cũ trên mạng còn dùng |
| MI trên chuỗi tự tương quan: hoán vị thường cho dương tính giả | bổ sung | Thêm `kiem_y_nghia_mi` hoán vị theo khối (Gohil et al. 2025) |
| Lộ trình có VIF/đa cộng tuyến và tương quan một phần | nhỏ | Nêu ngắn trong tài liệu (VIF 0.15 tự chuẩn hoá); phần thực hành để buổi 13 (chọn feature) |
| Open-Meteo: API miễn phí chỉ cho mục đích phi thương mại | nhỏ | Tác giả tải một lần, học viên lấy bản mirror; ghi trong danh mục |
