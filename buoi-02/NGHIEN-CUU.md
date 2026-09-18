# Nhật ký research — Buổi 2: Xác suất và thống kê cho dự báo

- **Ngày research:** 2026-09-17
- **Đã kiểm ở Phase 0 (Phụ lục B, `tools/NGHIEN-CUU.md`):** Hyndman & Fan (1996) loại 7 = `np.quantile(method="linear")`;
  Gneiting (2011) — sai số bình phương nhất quán với trung bình, tuyệt đối với trung vị, pinball với quantile; Efron (1979);
  Künsch (1989); Politis & Romano (1994); Politis (2003) về bootstrap i.i.d. trên dữ liệu phụ thuộc; NIST (Poisson, t,
  Cauchy); MIT OCW (CLT, MLE); FPP 5.5 khoảng dự báo, 7.3 R², 9.8 khoảng ARIMA quá hẹp; Hyndman "intervals".
- **Nền buổi:** Python 3.12, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, matplotlib 3.11.2
- **[CHẠY]** = đã chạy trong nền buổi; mọi con số của tài liệu lấy từ các lần chạy này

## Nguồn đọc thêm cho buổi này

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | `scipy.stats.bootstrap` (docstring 1.18.1), https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html | 2026-09-17 | chữ ký, mặc định |
| 2 | `scipy.stats.fit`, https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fit.html | 2026-09-17 | khớp phân phối rời rạc |
| 3 | statsmodels 0.15 `NegativeBinomial` (discrete, NB2) | 2026-09-17 | tham số α |
| 4 | arch 8.0.0 `arch.bootstrap` (MovingBlockBootstrap, StationaryBootstrap, optimal_block_length) | 2026-09-17 | block bootstrap thư viện |
| 5 | Hall, Horowitz & Jing (1995), Biometrika 82(3):561–574, doi:10.1093/biomet/82.3.561 | 2026-09-17 | độ dài khối |
| 6 | Politis & White (2004), Econometric Reviews 23(1):53–70; Patton, Politis & White (2009) 28(4):372–375 | 2026-09-17 | chọn khối tự động |
| 7 | FPP Pythonic §5.6 (biến đổi, bias adjustment), §7.1 (giả định hồi quy), https://otexts.com/fpppy/ | 2026-09-17 | trung vị vs trung bình, OLS |
| 8 | Greenland et al. (2016), Eur J Epidemiol 31:337–350 | 2026-09-17 | hiểu sai khoảng tin cậy |
| 9 | Hesterberg (2015), "What Teachers Should Know about the Bootstrap", arXiv:1411.5279 | 2026-09-17 | CLT chậm với dữ liệu lệch |
| 10 | UCI Bike Sharing (id 275) — Readme trong zip + trang dataset | 2026-09-17 | biến |
| 11 | Makridakis, Spiliotis & Assimakopoulos (2018), IJF 34(4):802–808 (M4, abstract) | 2026-09-17 | khoảng dự báo trong M4 |

## Phát hiện và trích dẫn

1. **`scipy.stats.bootstrap`** 1.18.1: `bootstrap(data, statistic, *, n_resamples=9999, …, method='BCa', …, rng=None,
   random_state=None)`; `random_state` → `rng` ("For an interim period, both keywords will continue to work"). Tài liệu
   mô tả dữ liệu là "a sample containing scalar observations from an underlying distribution", lấy mẫu lại "a random
   sample of the original sample (with replacement) of the same size" — **không có block bootstrap** trong scipy.
   [CHẠY] percentile i.i.d. của scipy và bản tự viết (cùng seed 7, 9.999 lần) cho cùng khoảng `[-0,634; -0,303]` trên một
   chuỗi AR(1); block bootstrap khối 6 cùng seed: `[-0,810; -0,201]`.
2. **`scipy.stats.fit` với phân phối rời rạc ràng buộc tham số nguyên:** "parameters which must be integral will be
   constrained to integral values". [CHẠY] trên lượt thuê: `nbinom` ra `n = 1.0`, AIC 217.131,3 — kém hơn MLE với n liên
   tục (n = 0,8447, AIC 216.800,4). `nbinom.fit` không tồn tại (`AttributeError`). statsmodels `NegativeBinomial` (NB2,
   "Variance equal to μ + αμ²") [CHẠY] α = 1,1838 = 1/0,8447 — khớp MLE tự viết, log-likelihood −108.398,2.
3. **Độ dài khối:** Hall, Horowitz & Jing (1995): "optimal block size depends significantly on context, being equal to
   n^{1/3}, n^{1/4} and n^{1/5} in the cases of variance or bias estimation, estimation of a one-sided distribution function,
   and estimation of a two-sided distribution function, respectively." → n^{1/3} là BẬC tăng, không phải hằng số.
   arch 8.0.0 có `optimal_block_length` (Politis & White 2004 + hiệu chỉnh 2009); docstring ghi cột `b_sb`, `b_cb` nhưng
   bản chạy trả `stationary`, `circular`. Khoá không thêm arch vào buổi 2 (tự viết là mục tiêu).
4. **FPP §5.6:** "the back-transformed point forecast will not be the mean of the forecast distribution. In fact, it will
   usually be the median … medians do not add up, whereas means do". §7.1 giả định sai số hồi quy: "have mean zero …
   are not autocorrelated … are unrelated to the predictor variables".
5. **Hiểu sai khoảng tin cậy** — Greenland et al. (2016) mục 19: "The specific 95 % confidence interval presented by a study
   has a 95 % chance of containing the true effect size. No!"
6. **CLT chậm** — Hesterberg (2015): "Classical t intervals and tests are terrible for skewed data. The Central Limit
   Theorem operates on glacial time scales."
7. **Bike Sharing** (Readme): "cnt: count of total rental bikes including both casual and registered", "hr : hour (0 to 23)",
   "workingday : if day is neither weekend nor holiday is 1, otherwise is 0". **Hai công thức nhiệt độ chuẩn hoá mâu
   thuẫn:** Readme "The values are divided to 41 (max)"; trang dataset "(t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 (only in
   hourly scale)" → buổi 2 không dùng cột nhiệt độ. [CHẠY] `cnt == casual + registered` mọi dòng; hour.csv 17.379 dòng
   (trang ghi 17.389).
8. **M4 và khoảng dự báo:** abstract (2018): "The two most accurate methods also achieved an amazing success in specifying
   the 95% prediction intervals correctly." Kết quả chi tiết về coverage trong bài 2020 **CHƯA XÁC MINH** (toàn văn trả 403)
   → không dùng con số coverage của M4.

## Số liệu thật của buổi [CHẠY, seed ghi kèm]

- **Lượt thuê theo giờ** (17.379 dòng): trung bình 189,46; trung vị 142; độ lệch chuẩn 181,39; hệ số lệch 1,277; phương
  sai / trung bình 173,7; ACF trễ 1 = 0,844, trễ 24 = 0,816. 2011: trung bình 143,8 (σ 133,8); 2012: 234,7 (σ 208,9).
- **Tối ưu hàm mất mát trên lượt thuê:** MSE → 189,46 (= trung bình); MAE → 142,0 (= trung vị); pinball τ = 0,9 → 452,0
  (quantile 0,9 loại 7 = 451,2 — dữ liệu nguyên nên mọi giá trị giữa hai điểm kề cùng tối ưu).
- **Khớp phân phối:** chuẩn AIC 230.086,2 (P(y < 0) = 0,148 dù không có giá trị âm nào); Poisson AIC 3.002.494,2; âm nhị thức
  AIC 216.800,4. Quantile 0,99: thực tế 782,2; chuẩn 611,4; Poisson 222; âm nhị thức 953. Phương sai âm nhị thức 42.685 vs
  thực 32.899,6 — một phân phối cho cả 24 giờ là hỗn hợp, không khớp hoàn toàn.
- **Khoảng dự báo 95% theo từng giờ trong ngày** (phủ / dưới / trên):

| Lịch sử → chấm | ±1,96σ | quantile thực nghiệm | chuẩn trên log |
|---|---|---|---|
| 2011 → 2011 (trong mẫu) | 96,4% / 0,3% / 3,3% | 95,3% / 2,2% / 2,6% | 95,3% / 4,5% / 0,2% |
| 2011 → 2012 | **72,5%** / 0,1% / 27,4% | **70,1%** / 0,5% / 29,3% | 94,9% / 1,3% / 3,8% |
| 2012 T1–6 → T7–12 | 91,5% / 0,6% / 7,9% | 88,8% / 1,8% / 9,5% | 96,4% / 2,8% / 0,8% |
| 2012 T5–8 → T9 | 89,0% / 2,1% / 8,9% | 82,9% / 3,9% / 13,2% | 92,6% / 3,9% / 3,5% |

  Khoảng log lúc 17h dựng từ 2011: [82; 1077] (quantile [65; 604], ±1,96σ [22; 678]); 0% giờ 17h năm 2012 vượt 1077.
  Ví dụ bootstrap tay: x = [12, 15, 11, 30, 14], `default_rng(3).integers(0, 5, (3, 5))` → trung bình 13,0 / 12,6 / 16,4.
  Hàm mất mát theo hằng c (lưới bước 2): bình phương đáy 190, tuyệt đối 142, pinball 0,9 đáy 452.
  Khoảng một khoảng chung (không theo giờ) từ 2011: ±1,96σ = [−118,4; 406,0], phủ 94,2% trong mẫu, 80,5% trên 2012.
  **Diễn giải:** 72,5% chủ yếu do mức lượt thuê 2012 tăng (đuôi trên 27,4%), không do hình dạng; quantile sửa hình dạng
  trong mẫu (hai đuôi 2,2%/2,6%) nhưng không sửa dịch chuyển; khoảng log "đạt" 94,9% trên 2012 nhờ đuôi trên dài chứ không
  vì mô hình hiểu mức tăng (trong mẫu đuôi dưới lệch 4,5%) — không trình bày như lời giải.
- **Bootstrap khoảng tin cậy 95% cho trung bình, AR(1) ρ = 0,7, n = 200, 300 lần, B = 999, seed 2026:** độ dài khối 1
  (i.i.d.) 60,3%; 3 → 78,7%; 6 (= n^{1/3}) → 86,3%; 10 → 89,0%; 20 → 89,3%; 40 → 81,3%. Dữ liệu độc lập (ρ = 0, seed 7) với
  khối mặc định: 91,7%.
- **Lượt thuê theo giờ 2012** (8.734 giờ), độ rộng khoảng tin cậy trung bình theo độ dài khối (seed 1): 1 → 9,1; 6 → ×1,85;
  21 (mặc định n^{1/3}) → ×1,60; 48 → ×2,14; 168 → ×3,53; 336 → ×4,53; 720 → ×6,19 — không ổn định vì chuỗi có xu hướng
  và mùa vụ.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình: "khoảng ±1.96σ chỉ phủ ~75% … sửa được bằng quantile thực nghiệm hoặc block bootstrap". Đo thật: ~73% là do **dịch chuyển mức** 2011→2012; quantile không sửa được (70,1%); block bootstrap là chuyện khoảng tin cậy của trung bình | **vừa** | Đã sửa "Lab" bước 4 và "Xong khi" của lộ trình + ghi chú todos; buổi dạy tách hai vấn đề: hình dạng (quantile sửa) và dịch chuyển (cần mô hình — buổi sau) |
| `scipy.stats.fit` ép n nguyên cho âm nhị thức | nhỏ | Lab khớp bằng MLE tự viết (n liên tục) và đối chiếu statsmodels; nêu trong Lỗi thường gặp |
| Hai công thức chuẩn hoá nhiệt độ mâu thuẫn trong tài liệu UCI | nhỏ | Không dùng cột nhiệt độ ở buổi 2 |
| arch có block bootstrap sẵn | nhỏ | Không đưa vào nền buổi (mục tiêu là tự viết); nhắc trong Đọc thêm |

## Research viết lại (Phase 6, 2026-09-18)

Mục tiêu: viết lại phần chữ theo chuẩn dễ hiểu D1–D12 (`tools/CHUAN-DE-HIEU.md`) và dạy kỹ khối thống kê nền mà đọc
thử buổi 1, 7, 12 báo chặn: phân phối, quantile, trung vị, phương sai, độ lệch chuẩn, tương quan, kiểm định.
Nguồn sư phạm chung (worked example, concreteness fading, hiểu lầm theo buổi): `tools/NGHIEN-CUU-SU-PHAM.md`.

### Nguồn mới (truy cập 2026-09-18)

| # | Nguồn | Dùng cho |
|---|---|---|
| 12 | FPP3 §5.5 https://otexts.com/fpp3/prediction-intervals.html | 1,96 là hệ số của khoảng 95% **khi giả định phân phối chuẩn**; bảng 80% → 1,28, 90% → 1,64, 95% → 1,96, 99% → 2,58. FPP không giải vì sao 1,96 → tài liệu giải bằng quantile 0,975 của phân phối chuẩn, kiểm bằng `norm.ppf` |
| 13 | FPP3 §7.8 https://otexts.com/fpp3/causality.html | tương quan ≠ nhân quả; kem–đuối nước (biến gây nhiễu: trời nóng); biến không gây ra $y$ vẫn giúp dự báo $y$ |
| 14 | OpenIntro Statistics https://www.openintro.org/book/os/ | trình tự dạy: kiểm định bằng **xáo ngẫu nhiên** (chương 2) trước lý thuyết kiểm định (chương 5) → mục 4.5 mở bằng đồng xu rồi permutation test tự viết |
| 15 | Applied Biostats, ch. 17 "Shuffling labels to generate a null" https://bookdown.org/ybrandvain/Applied-Biostats/perm1.html | các bước permutation test; p = tỷ lệ lần xáo lệch bằng/hơn quan sát; hai phía dùng trị tuyệt đối; **cảnh báo**: xáo giả định quan sát độc lập — dữ liệu phụ thuộc thì xáo trong nhóm |
| 16 | Phipson & Smyth (2010), "Permutation p-values should never be zero", arXiv:1603.05766 | công thức $(k+1)/(B+1)$ |
| 17 | Wasserstein & Lazar (2016), ASA statement on p-values, *Am. Stat.* 70(2) https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108 | p-value là xác suất của dữ liệu khi giả sử $H_0$, **không** là xác suất $H_0$ đúng; p không đo độ lớn hiệu ứng |
| 18 | Seeing Theory https://seeing-theory.brown.edu/probability-distributions/index.html | CLT: "trung bình mẫu của đủ nhiều biến i.i.d. xấp xỉ chuẩn"; dạy bằng mô phỏng → mục 4.6 kiểm $1/\sqrt n$ bằng rút mẫu thật |
| 19 | `scipy.stats.permutation_test` (scipy 1.18.1, chạy trong nền buổi) | đối chiếu hàm tự viết |

Hiểu lầm phổ biến đưa vào tài liệu (mục "Tự kiểm tra", "Lỗi thường gặp", quiz): quantile 0,8 = "80% của số lớn nhất";
trung bình luôn là con số an toàn nhất; chỉ nhìn tỷ lệ phủ tổng; $r \approx 0$ = không liên quan; tương quan = nhân quả;
p = xác suất $H_0$ đúng; không bác bỏ = chứng minh $H_0$; có ý nghĩa thống kê = khác biệt lớn; quên căn bậc hai khi
nối $n_{\text{eff}}$ với độ rộng.

### Quyết định cấu trúc (≤ 6 khái niệm)

| Mục | Nội dung | Lý do gộp |
|---|---|---|
| 4.1 | phân phối, histogram, đường tích luỹ, quantile, trung vị | cùng một ví dụ 9 số; quantile đếm tay khớp buổi 1, nội suy của `np.quantile` là "cách của máy" |
| 4.2 | trung bình, phương sai, độ lệch chuẩn, hệ số lệch + chọn con số theo hàm phạt | mức và độ phân tán đi cùng; ba hàm phạt dùng lại đúng 9 số |
| 4.3 | 1,96 và phân phối chuẩn, tỷ lệ phủ hai đuôi, khoảng dự báo vs khoảng tin cậy, trong/ngoài mẫu | 1,96 chỉ có nghĩa khi đi với khoảng |
| 4.4 | tương quan $r$ (mới) + hộp "Mượn trước" tự tương quan, biến gây nhiễu | |
| 4.5 | kiểm định giả thuyết (mới): đồng xu, permutation test tự viết | khuôn đọc cho ADF, Ljung–Box, Diebold–Mariano |
| 4.6 | i.i.d., luật số lớn, CLT, $1/\sqrt n$, AR(1), $n_{\text{eff}}$, bootstrap, block bootstrap | CLT/i.i.d. chỉ cần để hiểu vì sao bootstrap i.i.d. hỏng |

**Bỏ khỏi bài** (đưa một dòng vào "Đọc thêm"): chọn phân phối cho dữ liệu đếm (Poisson, âm nhị thức, MLE, AIC, QQ-plot)
và thang log. Hai phần này chiếm nhiều chỗ chặn của bản cũ, không cần cho mục nào sau, và có buổi 5 (biến đổi) và buổi
19 (dữ liệu đếm) dạy. Lab Bước "khớp ba phân phối" bỏ theo. Hình `phan-phoi-luot-thue.png`, `khoang-2011-2012.png`,
`ty-le-phu-kich-ban.png` vẫn sinh bởi `ve_hinh.py` nhưng tài liệu không còn dùng (bảng số trong mục 4.3 đủ).

### Con số mới [CHẠY] — `dap-an/vi_du_nho.py` (seed ghi trong code), hình mới `ve_hinh.py moi`

Chạy: `cd lab && env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../dap-an/vi_du_nho.py`

- Ví dụ 9 giờ `8, 2, 36, 5, 12, 3, 18, 6, 9`: đếm tay q0,25 / q0,5 / q0,8 / q0,9 = 5 / 8 / 18 / 36; `np.quantile` nội
  suy = 5 / 8 / 14,4 / 21,6; `inverted_cdf` khớp đếm tay. CDF(8) = 5/9, CDF(12) = 7/9. Trung bình 11, tổng bình phương
  độ lệch 894, phương sai 111,75, độ lệch chuẩn 10,5712; hệ số lệch 1,611 (scipy mặc định; pandas 1,953); số 36 góp
  1,754. Phạt trung bình với c = 8 / 11 / 18: tuyệt đối 6,556 / 7,333 / 11,000; bình phương 108,33 / 99,33 / 148,33;
  pinball 0,8: 4,178 / 3,667 / 3,400. Lưới c 0–40 bước 0,5: đáy đúng 8, 11, 18. ±1,96s = [−9,72; 31,72].
- 1,96: `norm.ppf(0.975)` = 1,95996; P(|Z| ≤ 1) = 0,6827, ≤ 1,96 = 0,9500, ≤ 2 = 0,9545; 100.000 số chuẩn seed 0 →
  0,9498. Tỷ lệ phủ ví dụ [4; 20] trên 10 số: 0,6 / 0,2 / 0,2.
- Khoảng chung không tách giờ: từ 2011 (TB 143,79, s 133,80) → [−118,4; 406,0]; từ cả 2011–2012 (TB 189,46, s 181,39)
  → [−166,1; 545,0]. **Giải quyết mâu thuẫn baseline:** −118,4 là của năm 2011, −166,1 (quiz câu 9) là của cả hai năm;
  tài liệu ghi rõ cả hai.
- Tương quan: ví dụ 5 cặp → tổng tích 850, 250, 3.400, r = 0,9220. Dữ liệu thật: r(temp, cnt) mọi giờ 0,405; lúc 17h
  (730 ngày) 0,588; r(hum, cnt) −0,323 / 17h −0,253; r(hr, cnt) 0,394. Độ ẩm trung bình 4h 0,74, 15h 0,49. Cột `temp`
  chuẩn hoá tuyến tính (hai công thức UCI mâu thuẫn nhưng đều tuyến tính) nên r không phụ thuộc công thức nào đúng.
  Tự tương quan 1, 3, 1, 3 trễ 1 = −0,75; lượt thuê giờ trễ 1 = 0,844; lượt thuê ngày 2012 trễ 1 = 0,748.
- Kiểm định: P(≥ 9 ngửa/10) = 11/1024 = 0,0107 (mô phỏng seed 1: 0,0106); hai phía 22/1024 = 0,0215; ≥ 7 ngửa 176/1024 =
  0,1719. Ví dụ 6 ngày: 20 cách chia, 2 cách |chênh| ≥ 3 → p = 0,10. Day 2012, 9.999 lần xáo, seed 2026: làm việc −
  nghỉ (250/116 ngày) chênh 456,4, k = 253, p = 0,0254 (scipy `permutation_test` seed 2026: 0,0232); thứ Bảy − Chủ nhật
  (52/53) chênh 695,2, k = 774, p = 0,0775.
- $1/\sqrt n$ (rút i.i.d. seed 5, 20.000 lần): n = 25 / 100 / 400 → độ lệch chuẩn trung bình 36,08 / 18,24 / 9,06, σ/√n =
  36,28 / 18,14 / 9,07, tỷ lệ trong ±1,96σ/√n 0,954 / 0,949 / 0,950. n_eff(200; 0,7) = 35,3, √(n/n_eff) = 2,38;
  n_eff(365; 0,5) = 121,7, √ = 1,732. Block bootstrap tay khối 2 seed 2: bắt đầu 3, 1, 0 → 30, 14, 15, 11, 12, trung bình
  16,4. Chuỗi AR(1) seed 7: trung bình mẫu −0,467.

### Kiểm máy `kiem_de_hieu.py 02` — vi phạm còn lại và lý do

- `muon_truoc` ×4 ("kiểm định", "p-value", "mức ý nghĩa", "giả thuyết không"): Phụ lục E ghi các thuật ngữ này thuộc buổi
  4/7 nhưng từ Phase 6 buổi 2 **dạy** chúng (mục 4.5), không mượn trước. "kiểm định" còn khớp nhầm dòng *validation*
  ("tập kiểm định", buổi 3) của E. Cần sửa cột "Buổi" trong Phụ lục E (đã báo trong báo cáo Phase 6).
- `nhieu_so` ×33: các đoạn còn lại là phép tính từng bước, dãy dữ liệu của ví dụ nhỏ, hoặc tham số thí nghiệm (seed, $n$,
  số lần lặp) mà bộ đếm không nhận ra là phép tính (dùng "/", "chia", ngoặc). Không đoạn nào dồn quá 3 con số **kết
  quả**; mọi bảng kết quả đã tách thành bảng có "Đọc bảng".

### Độ dài

`wc -w tai-lieu.md` ≈ 9.800 (trong đó khoảng 650 là code, công thức khối và dấu `|` của bảng; phần chữ ≈ 8.800). Trần
mới 9.000. Đã bỏ hẳn hai phần không cần cho mục sau (chọn phân phối, thang log), một hình, một bước lab, một bài tập.
Phần còn lại là khuôn D2 đủ bước cho 6 khái niệm, trong đó hai khái niệm mới (tương quan, kiểm định).

### Sửa sau đọc thử bản mới, vòng 1 (2026-09-18: 0 chặn / 21 khó / 17 nhỏ, quiz 10/10)

- **Lỗi nội dung đã sửa:** hệ số lệch theo đúng lời tài liệu (chia $s$ = 10,57) là **1,35** (số 36 góp 1,47), không phải
  1,61 (1,61 là quy ước của scipy, chia $\sigma$ = 9,97; pandas 1,95). Bảng tỷ lệ phủ theo độ dài khối (60,3% … 81,3%)
  đưa lại vào mục 4.6 cho Lab bước 5 dẫn tới.
- **Giải thích "vì sao không đạt 95%" sửa lại.** Bản trước nói do $n_{\text{eff}} \approx 35$ khiến khoảng percentile hẹp.
  Kiểm: bootstrap i.i.d. trên dữ liệu độc lập $n$ = 35 (seed 2026, 300 lần) vẫn phủ 94,7%, nên lập luận đó không đứng.
  Giải thích mới: đánh đổi chỗ nối khối / số khối; [CHẠY] $\rho$ = 0,7, $n$ = 2.000, khối 13 phủ **94,0%**
  (`vi_du_nho.py`). Quiz câu 10 sửa theo.
- Thêm: đoạn "mẫu và tổng thể", quy ước $s$ / $\sigma$ và vì sao chia $n - 1$; lý do bằng lời vì sao mỗi hàm phạt chọn
  một con số; báo rõ hình hàm mất mát dùng $\tau$ = 0,9, thêm bảng đáy; trung vị khi $n$ chẵn (đếm tay 2, `np.median` 2,5);
  vì sao máy dùng $(n-1)q$; định nghĩa seed, `ppf`, quantile của phân phối liên tục; tách bảng tỷ lệ phủ 4.3 thành bảng
  trong mẫu (hai đuôi) và ngoài mẫu (chỉ phủ), bình luận dòng tháng 5–8 → tháng 9 và vì sao quantile ngoài mẫu kém hơn
  ±1,96σ; vì sao tự tương quan 1, 3, 1, 3 ra −0,75; đếm tổ hợp 120 + 45 + 10 + 1 = 176; trực giác $\sigma/\sqrt n$ và
  $n_{\text{eff}}$; "percentile"; code block bootstrap viết lại bằng vòng lặp (ví dụ seed 2 cho [3, 4, 1, 2, 0], khớp ví
  dụ tay); các nhỏ khác (FPP viết đầy đủ, 730 ngày có số liệu lúc 17h — ngày 29/10/2012 thiếu giờ 17, hai chiều của biến
  gây nhiễu, `~`, import trong Lab).
- Độ dài theo `kiem_de_hieu.py` (cột do_dai, chữ ngoài bảng/code): 8.506, trong trần 4.000–9.000.

### Sửa sau đọc thử bản mới, vòng 2 (2026-09-18: 1 chặn / 15 khó / 15 nhỏ, quiz 10/10)

- **Chặn đã sửa:** 4.6 thêm "Vì sao cách này đúng?" (mẫu là bức ảnh thu nhỏ của tổng thể). [CHẠY, seed 11] coi 8.734 giờ
  2012 là tổng thể, một mẫu 100 giờ: độ lệch chuẩn của 5.000 trung bình rút mới từ tổng thể 21,2; bootstrap từ chính mẫu
  21,0 (σ/√100 = 20,89).
- 4.3 "Dữ liệu thật": một câu nói cách dựng khoảng theo giờ; một bảng chính (2 cách × trong mẫu 2011 / 2012, cột
  phủ–dưới–trên); các phép thử khác và "khoảng chung" chuyển vào hộp Nâng cao; bỏ dòng tháng 5–8 → 9 khỏi tài liệu.
- 4.3 thêm trực giác "đường cong = histogram cột hẹp, diện tích = tỷ lệ"; ví dụ "20 lần lấy mẫu" [CHẠY, seed 12]: 19/20
  khoảng chứa trung bình thật 234,7; khoảng thứ 20 [148,1; 231,8] trượt.
- 4.6: ví dụ 4 đồng xu ±1 (độ lệch chuẩn tổng = 2 = √4); bảng 1/√n bỏ cột tỷ lệ, nói rõ rút có hoàn lại, quanh trung
  bình thật 189,5; bước nối √(n/n_eff) viết ra; vì sao khối 40 hẹp [CHẠY, cùng seed bảng 4.6]: độ rộng trung bình 0,751
  (khối 10), 0,780 (20), 0,727 (40); tâm lệch 0,028 / 0,046 / 0,066; giải thích ô phải (mùa vụ, xu hướng).
- 4.2: công thức hệ số lệch dạng trung bình (độ lệch/s)³, liệt kê 9 số hạng (âm −1,37, dương 13,52 → 1,35); chọn **s**
  cho mọi công thức, gọi cách dựng khoảng là "±1,96s" (thay cả trong quiz); lập luận "nhích c" cho phạt bình phương
  (tổng (y−8)² = 975 → (y−9)² = 930, bớt 2 × 27 − 9 = 45); 452 vs 451 do lưới bước 2.
- 4.1 code quantile thành hàm đầy đủ; 4.5 C(6,3) = 20 và vì sao chỉ 2 cách (tổng ≥ 18 hoặc ≤ 9), True/False cộng vào số,
  "dừng", hình hoán vị ô trái/phải; các nhỏ khác (mục 2, 3, bảng Từ mới, đổi đơn vị không đổi r, cột độ ẩm, Lab bước 1).
- Để giữ trần 9.000: bỏ bài tập "khoảng theo giờ và loại ngày", rút gọn Mục tiêu, Đọc thêm, vài đoạn "Đọc kết quả".
  Độ dài theo `kiem_de_hieu.py`: 8.996.

### Sửa sau đọc thử vòng 3 (2026-09-18: 0 chặn / 13 khó / 15 nhỏ) — cắt bớt, trỏ Phụ lục B

- 4.2: định nghĩa ba cách phạt ngay trước bảng; lập luận "nhích c" chi tiết thay bằng một câu trực giác mỗi cách +
  "Phụ lục B, mục 8"; hệ số lệch bỏ liệt kê 9 số lập phương, giữ ý + 1,35 / 1,61 / 1,95, trỏ mục 6; lý do chia n−1 nối
  với "trung bình làm tổng bình phương nhỏ nhất" + trỏ mục 5.
- 4.3: ví dụ diện tích (rộng 10 × cao 0,02 = 20%); 1,96 dùng cho mọi phân phối chuẩn; ví dụ 20 khoảng (seed 12) chuyển
  xuống 4.6, sau khi đã có công thức trung bình ± 1,96 s/√n (thay σ bằng s vì không biết σ); so hai cận trên lúc 17h
  (678 so với 604); bỏ bullet "một khoảng chung cho mọi giờ" (−118,4 / −166,1; quiz câu 9 tự đủ số).
- 4.4: trung bình 20 / 70 nêu trước bảng; "nhiễu" → "che mất quan hệ".
- 4.6: phương sai tổng 4 đồng xu (64/16 = 4); trục "thang nhân"; khối dài chỉ còn một cơ chế (khối liền kề gần trùng →
  mẫu lại giống nhau → khoảng hẹp); ô phải một lý do (xu hướng); bỏ 0,78/0,73, điểm hai đầu chuỗi, khối 21; n^{1/3}
  diễn đạt thành "quy tắc kinh nghiệm: căn bậc ba".
- Nhỏ: 17.379 so với 17.544 giờ (thiếu 165); "mức q" vs "vị trí"; ngày 29/10/2012 thiếu giờ 17; Ljung–Box "phần sai số
  mô hình để lại"; scipy hai phía = nhân đôi p một phía nhỏ hơn; `env -u VIRTUAL_ENV`, `--no-sync`.
- Độ dài (`kiem_de_hieu.py`, chữ ngoài bảng/code): 8.996 → 8.916.

## Đọc thử (Phase 6, 2026-09-18)

Subagent mới mỗi vòng, prompt nguyên văn ở `tools/CHUAN-DE-HIEU.md`, chỉ mở `tai-lieu.md` + `kiem-tra.md` đã bỏ đáp án.

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ | 11 | 25 | 16 | 9/10 | chặn: AIC, i.i.d., AR(1), độ lệch chuẩn/1,96, QQ-plot, likelihood, CLT, tự tương quan, $n_{\text{eff}}$ |
| 1 | viết lại (6 khái niệm, thêm tương quan + kiểm định) | 0 | 21 | 17 | 10/10 | lỗi nội dung: hệ số lệch 1,61 ≠ 1,35 theo lời tài liệu; Lab bước 5 trỏ bảng không tồn tại |
| 2 | + "mẫu và tổng thể", quy ước s/σ | 1 | 15 | 15 | 10/10 | chặn: vì sao bootstrap đúng; tự sửa lời giải thích "vì sao không đạt 95%" (bản cũ sai) |
| 3 | + nguyên lý bootstrap (bảng 21,2 vs 21,0), rút 4.3 về một bảng | 0 | 13 | 15 | 10/10 | chạm trần chữ — đổi hướng: cắt bớt, trỏ Phụ lục B |
| 4 | cắt chi tiết, trỏ Phụ lục B mục 5, 6, 8 | 0 | 7 | 15 | 10/10 | thiếu phụ lục vẫn theo được ý chính |
| 5 | sửa σ, khoảng tin cậy, khối dài, ô phải | 0 | 7 | 11 | 10/10 | giải thích "khối dài làm hẹp" chưa thuyết phục |
| 6 | phương sai của tổng, $n_{\text{eff}}$ trực giác, khối dài nói thật "cần toán ngoài buổi" | **0** | **4** | 12 | 10/10 | **đạt**. Không số nào sai (agent kiểm cả `default_rng`) |

Sau vòng 6 sửa thêm 2 chỗ khó: lập luận cân hai bên cho pinball → quantile $\tau$; ví dụ hoán vị nói rõ hai phía
(một phía thì p = 1/20 = 0,05, vẫn không nhỏ hơn 0,05). `kiem_de_hieu.py 2`: độ dài trong trần; còn các cờ `nhieu_so`
là phép tính tay/dãy dữ liệu ví dụ (lý do ghi ở mục "Sửa sau đọc thử" phía trên). PDF 22 trang.

Bài học cho Phase 7–8: buổi dạy nhiều khái niệm nền thì mỗi vòng đọc thử lại tìm ra chỗ mới; thêm giải thích làm
chạm trần chữ. Cách hiệu quả là **cắt chi tiết chứng minh sang phụ lục** và nói thẳng giới hạn ("cần toán ngoài buổi
này") thay vì giải thích nửa vời.
