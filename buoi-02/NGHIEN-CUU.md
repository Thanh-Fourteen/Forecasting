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
