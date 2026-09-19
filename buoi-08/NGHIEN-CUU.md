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

## Research viết lại (Phase 10, 2026-09-18)

Research sư phạm (KHỐI CHUNG R); nguồn, phiên bản giữ như trên. Cách giải thích chọn cho từng khái niệm:

| Khái niệm | Trực giác + ví dụ tay (trước công thức) | Căn cứ |
|---|---|---|
| Pearson / Spearman | $y = x^2$ trên 1…5 (Pearson 0,981, Spearman 1) và chữ U trên −2…2 (Pearson 0 tính tay) | Anscombe 1973; FPP §2.6 |
| tương quan giả | hai chuỗi 5 tháng: $r$ mức 0,974, $r$ các bước −1 (tính tay); DW tay trên hai dãy phần dư (0,67 và 3,33) | Granger & Newbold 1974 |
| MI | bảng 3 ô lạnh/vừa/nóng: Pearson 0 nhưng MI = 0,637 nat, tính từng ô $p \ln(p/(p_xp_y))$ | Cover & Thomas (định nghĩa); Kraskov 2004 (ước lượng liên tục) |
| hoán vị theo khối | "hai chuỗi trơn độc lập tình cờ có quãng dài cùng cao"; xáo từng điểm phá độ trơn | Gohil et al. 2025 |
| prewhitening | random walk 12 điểm, $y$ chậm 2: CCF thô trải rộng (0,42/0,77/0,37), sau sai phân một đỉnh 0,91; "dòng bước của $y$ là dòng bước của $x$ dời 2 cột" | Penn State STAT 510 L9; Box–Jenkins |
| tương quan trượt | 6 ngày: cửa sổ đông −1, hè +1, gộp 0,48 | chạy thật |
| Granger | hai cách dự báo A (quá khứ $y$) và B (thêm quá khứ $x$) trên 6 số; tổng bình phương sai số 38 so với 0 | Granger 1969; Maziarz 2015 |

Mỗi tình huống 4.2–4.6 kết bằng nhãn **"Cái bẫy trong một câu"** (yêu cầu phase). 9 mục cũ → 6 (4.1 hệ số + Anscombe; 5 tình huống);
ex-ante gộp vào 4.6; VIF/tương quan một phần → hộp Nâng cao; quy trình 6 bước bỏ (đã nằm trong "Xong khi"). Mọi trích tiếng Anh bỏ.

**Sửa số bản cũ:** $R^2$ hồi quy theo CDD + HDD **đúng tại mốc 18,33 °C là 0,812** (bản cũ 0,813 lấy ở điểm lưới gần mốc nhất trong
`ve_hinh.py`); đã sửa script tính đúng mốc, tài liệu, quiz. Thêm `dap-an/vi_du_nho.py`, `code/lab.ipynb` (chạy hết 8 giây).

## Đọc thử (Phase 10, 2026-09-18)

Tự đọc (không subagent), theo checklist `tools/CHUAN-DE-HIEU.md`; mọi con số, đáp án quiz tính lại bằng Python.

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (2.747 chữ, 10 trang, 70 cờ) | 7 | — | — | — | chặn: công thức MI dạng tích phân không giải thích; DW, $t$, $R^2$ dùng không định nghĩa; VIF, $R^{-1}$ tương quan một phần; "hồi quy" chưa dạy; nhiều trích tiếng Anh (Granger & Newbold, Penn State, Wikipedia, Maziarz) mang ý chính; không hình nào có "Cách đọc hình" |
| 1 | viết lại (5.049 chữ) | 0 | 1 | 3 | 10/10 có căn cứ | khó: vì sao hai chuỗi trơn độc lập có MI lớn (thiếu mắt xích trước đoạn hoán vị theo khối). Nhỏ: "kiểm định F", "Box–Jenkins" chỉ nêu tên; "khoảng một phút" ở Lab bước 3 sai (notebook chạy 8 giây) |
| rà gọn | biên tập viên | — | — | — | — | 2 chỗ lặp: "Tóm lại" 4.2 và 4.4 nói lại "Cái bẫy" → viết lại mang ý khác |
| 2 | sau sửa (5.010 chữ, 15 trang) | **0** | **0** | 2 | 10/10 | **đạt** |

Quiz: viết lại 10 đáp án (vì sao đúng, vì sao từng lựa chọn sai, bỏ trích tiếng Anh); căn cứ: 1 → 4.2, 2 → 4.3, 3 → 4.4, 4 → 4.6,
5 → 4.4, 6 → 4.3 + Nâng cao, 7 → 4.3, 8 → 4.6, 9 → 4.3, 10 → 4.6 (+ buổi 6). `kiem_de_hieu.py 8`: 70 → **0**. Lab: `kiem_tra_lab.py 8`
đạt (đáp án 10/10, code 3/10 đỏ, notebook chạy hết).

## Đọc thử độc lập (Phase 11, 2026-09-18)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E (ngoại lệ ghi thật: trong lúc kiểm ví dụ tương quan chéo đã
`grep` định nghĩa hàm `ccf_tu_viet` trong `dap-an/tuong_quan.py` — chỉ docstring + 5 dòng quy ước, không phải đáp án quiz). Ví dụ tay tính lại
bằng Python (Pearson $x^2$ 0,981, chữ U 0, tự kiểm 0,785, $a$–$b$ 0,974/−1, DW 0,67/3,33, MI 0,637, tương quan chéo 0,15/0,42/0,77/0,37/0,05 và
−0,09/−0,10/0,91/−0,01/−0,11, trượt 0,48, Granger 38): khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.3 | "hồi quy tải theo CDD và HDD vẽ được hình chữ V" | 1/4 | bảng Từ mới chỉ có hồi quy **một** biến $y = a + bx$; hồi quy theo hai biến trông ra sao, vì sao ra chữ V, không nói | khó |
| 2 | Từ mới | "$t$ của hệ số: Hệ số $b$ chia cho sai số chuẩn của nó" | 1 | "sai số chuẩn" chưa định nghĩa (không cản vì chỉ dùng $t$ để nói "trông có ý nghĩa") | nhỏ |
| 3 | 4.6 | "so hai tổng này bằng một thống kê (kiểm định F)" | 7 | F không giải thích; đủ biết "cho p-value" | nhỏ |
| 4 | 4.2 | "phần dư lộn xộn thì DW gần 2" | 4 | vì sao đúng 2 (không phải 3,33 như ví dụ xen kẽ) | nhỏ |
| 5 | 4.6 Cách đọc hình | "ô phải là tương quan chéo" | 5 | hình của mục Granger lại vẽ tương quan chéo hai chiều; phải tự nối | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Pearson/Spearman**: $x$ = 1, 2, 3 và $y$ = 1, 8, 27 → Spearman 1, Pearson < 1.
- **Tương quan giả**: số điện thoại và số cây xanh trong thành phố cùng tăng 20 năm → $r$ mức cao; thay đổi hằng năm không liên quan.
- **Phi tuyến/MI**: 2 loại ngày mỗi loại 1/2, biết loại là biết chắc → MI = ln 2.
- **Tương quan chéo + prewhitening**: $y_t = x_{t-1}$, $x$ trơn → thô đỉnh rộng quanh 1; lọc → đỉnh sắc ở 1.
- **Tương quan trượt**: mùa đông −0,8, mùa hè +0,9, cả năm 0,5 không đúng mùa nào.
- **Granger**: thêm quá khứ $x$ làm tổng bình phương sai số 50 → 10 → "giúp dự báo", không phải "gây ra"; nhiệt độ ngày mai đo được là ex-post.

### C. Quiz mù

1 C · 2 B · 3 B · 4 B · 5 $x$ đi trước $y$ 4 bước; `ccf(y_loc, x_loc)` (hai chuỗi đã lọc, đặt $y$ trước; `adjusted=False` để khớp mẫu số) ·
6 10 °C: CDD 0, HDD 8,33; 30 °C: CDD 11,67, HDD 0; quan hệ chữ V: lạnh và nóng đều làm tải tăng, một đường thẳng theo nhiệt độ không bắt được ·
7 không: hoán vị từng điểm phá tự tương quan nên p nhỏ giả; hoán vị theo khối (và nên xét trên thay đổi/sai phân) · 8 tải hôm nay dùng được;
nhiệt độ ngày mai phải là **dự báo** thời tiết (kèm sai số); giá khí đốt ngày mai không biết → dự báo nó hoặc dùng giá hôm nay · 9 quan hệ chữ V
đổi dấu ở 18,33 °C (−0,649 / +0,910); tách CDD/HDD giải thích 81% thay vì 38%: nhiệt độ giải thích phần lớn nhu cầu, không "một phần" ·
10 hai chiều cùng có ý nghĩa → biến gây nhiễu chung (nhịp ngày), không phải nhân quả; kiểm tốt hơn: bỏ nhịp ngày / đưa về dừng rồi mới Granger,
prewhiten, đọc "giúp dự báo". Căn cứ: 1 → 4.2; 2, 6, 7, 9 → 4.3; 3, 5 → 4.4; 4, 8, 10 → 4.6. Câu 5 phần `adjusted` "đoán" (tài liệu không nói),
còn lại "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 4. Khó nhất: hồi quy hai biến CDD + HDD. Sửa một điều: viết công thức tải = $a + b \cdot$CDD $+ c \cdot$HDD ngay ở ví dụ CDD/HDD.

### E. Dài/lặp

Không thấy đoạn ≥ 30 chữ lặp ý ("Cái bẫy trong một câu" + "Tóm lại" mỗi tình huống gần nhau nhưng nói hai ý khác nhau).

### Chấm, sửa, đọc lại

**Quiz mù: 10/10** khớp `kiem-tra.md`.

Sửa: (1) 4.3 ví dụ CDD/HDD viết rõ tải = $a + b \cdot$CDD $+ c \cdot$HDD ("như hồi quy đơn, thêm một biến"), phía nóng dốc $b$, phía lạnh
dốc $c$; (2) bảng Từ mới: "sai số chuẩn (độ lệch chuẩn của chính ước lượng $b$)"; (3) **lỗi PDF có sẵn**: Cách đọc hình 4.3 có dòng tiếp
bắt đầu bằng "+ HDD" nên markdown biến thành gạch đầu dòng con — nối lại dòng (grep cả buổi 4–8 + Phụ lục C: chỉ chỗ này).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 11 đọc mù | 5.010 | 15 | 0 | 1 | 4 | 10/10 | 0 |
| sau sửa, đọc lại toàn bộ | 5.028 | 15 | **0** | **0** | 3 | 10/10 | 0 |

Nhỏ còn lại: "kiểm định F" chỉ nêu tên; vì sao DW của phần dư ngẫu nhiên gần 2; hình Granger vẽ tương quan chéo — không cản theo dõi.
**Đạt.** `kiem_de_hieu.py 8` 0; lab, tự chứa đạt; PDF xem lại trang 6 (công thức và danh sách hiển thị đúng).
