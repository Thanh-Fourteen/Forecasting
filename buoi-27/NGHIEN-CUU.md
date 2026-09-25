# Nhật ký research — Buổi 27: Dự báo Bayes và Gaussian Process

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-24
- **Người/phiên:** Phase 26 (soạn buổi 27–28)

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | PyMC 6.3.2 — PyPI + kiểm API bằng chạy thật (`pm.sample` trả `xarray.DataTree`, `pm.gp.HSGP`, `HSGPPeriodic`, `pm.gp.cov.*`) | thư viện | 2026-09-24 | 4.1–4.6 |
| 2 | pymc-extras 0.15.1 (16/9/2026) — `pymc_extras.statespace.models.structural`: `LevelTrend`, `TimeSeasonality`, `FrequencySeasonality`, `MeasurementError`, `.build()` in bảng tham số cần prior, `build_statespace_graph`, `forecast` (kiểm bằng `inspect` + chạy thật; trang tài liệu chính thức không có ví dụ) | thư viện | 2026-09-24 | 4.5 |
| 3 | ArviZ 1.3.0 (11/8/2026) — `az.summary` mặc định in khoảng 89% (`eti89_lb/ub`), `ess_bulk`, `ess_tail`, `r_hat`; trả `SummaryDataFrame` | thư viện | 2026-09-24 | 4.3 |
| 4 | Vehtari, A., Gelman, A., Simpson, D., Carpenter, B. & Bürkner, P.-C. (2021). Rank-normalization, folding, and localization: an improved R̂. *Bayesian Analysis* 16(2) — ngưỡng r_hat < 1,01, ESS bulk ≥ 400 (4 chuỗi × 100) | bài gốc | 2026-09-24 | 4.3 |
| 5 | Betancourt, M. & Girolami, M. (2015). Hamiltonian Monte Carlo for hierarchical models — cái phễu và tham số hoá non-centered | bài gốc | 2026-09-24 | 4.3 |
| 6 | Gabry, J., Simpson, D., Vehtari, A., Betancourt, M. & Gelman, A. (2019). Visualization in Bayesian workflow. *JRSS A* 182 — prior predictive check | bài gốc | 2026-09-24 | 4.2 |
| 7 | Gelman et al. *Bayesian Data Analysis* (3rd ed), §5.5 ví dụ 8 trường (số liệu Rubin 1981) | sách | 2026-09-24 | 4.3 |
| 8 | Riutort-Mayol, G., Bürkner, P.-C., Andersen, M.R., Solin, A. & Vehtari, A. (2023). Practical Hilbert space approximate Bayesian Gaussian processes. *Statistics and Computing* 33 | bài gốc | 2026-09-24 | 4.6: HSGP, chi phí tuyến tính thay cho O(n³) |
| 9 | Rasmussen, C.E. & Williams, C.K.I. (2006). *Gaussian Processes for Machine Learning*, ch. 4–5 (kernel, cộng/nhân kernel) | sách | 2026-09-24 | 4.6 |
| 10 | Scott, S.L. & Varian, H. (2014). Predicting the present with Bayesian structural time series | bài gốc | 2026-09-24 | 4.5 |

## Phiên bản đã xác minh (PyPI 2026-09-24)

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| pymc | 6.3.2 | có sẵn trong bảng chung |
| pymc-extras | 0.15.1 | có sẵn trong bảng chung |
| arviz | 1.3.0 | **thêm vào `tools/nen/phien-ban.toml`** |
| pytensor | 3.3.2 (phụ thuộc của pymc) | cần trình biên dịch C để nhanh; không có thì chạy chậm |
| statsforecast | 2.1.1 → nền chốt pandas 2.3.3 | AutoETS so sánh |

## Dữ liệu

| Bộ | Giấy phép | Dùng |
|---|---|---|
| `monash-car-parts` | CC BY 4.0 | 2.674 mã, 51 tháng (1/1998 → 3/2002), 4,5% ô thiếu; buổi chọn 300 mã đủ 36 tháng cuối (seed 0) |
| `uci-bike-sharing` (`day.csv`) | CC BY 4.0 | 731 ngày 2011–2012; 60 ngày cuối để chấm; 29/10/2012 (bão Sandy) chỉ 22 lượt |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **pymc 6 + ArviZ 1.x đổi kiểu trả về**: `pm.sample` trả `DataTree`; truy cập `idata["posterior"]`, `idata["sample_stats"]["diverging"]`.
  `forecast` của pymc-extras trả thẳng nút `posterior_predictive` (không bọc thêm nhóm).
- **Car Parts không tạo cái phễu**: τ hậu nghiệm ≈ 1 (các mã khác nhau nhiều), tham số hoá centered cũng 0 divergence — kể cả nhóm mã đồng
  nhất (trung bình 0,2–0,8 món/tháng) và lịch sử chỉ 3 tháng. Không ép ví dụ; non-centered minh hoạ bằng 8 trường (Rubin 1981): centered 312
  divergence (target_accept 0,8) và **vẫn 64** khi nâng target_accept lên 0,95; non-centered 10 → 0.
- **Divergence thật của buổi đến từ GP ba thành phần** (ExpQuad dài + chu kỳ năm + chu kỳ tuần) trên 2 năm dữ liệu: hai thành phần tranh nhau
  giải thích cùng đường cong. Tuỳ seed: 30 / 1.033 / 2.012 divergence (target 0,9), r_hat tới 3,40. Gộp thành một thành phần mượt Matern 5/2
  + chu kỳ tuần, target 0,95: 0 divergence ở 3 seed. MAE của mô hình hỏng lại thấp hơn (1.064–1.083 so với 1.135–1.154) — bài học: con số đẹp
  từ posterior không hội tụ vẫn không dùng được (coverage 82–95% tuỳ seed).
- **Prior rộng không đổi posterior ở đây** (dữ liệu đủ nhiều): RMSE gộp một phần 1,181 (prior rộng) so với 1,182 (prior hẹp); nhưng prior rộng
  sinh ra 20 triệu món/tháng ở phân vị 90% — mô hình tin vào điều vô lý.
- **Poisson tốc độ cố định thiếu số 0**: dự báo 67,6% tháng bán 0 món, thật 78,7% → gợi ý zero-inflated / negative binomial (bài tập).
  Khoảng Poisson phủ thừa (50% → 86%, 90% → 96%) vì đầu mút phải là số nguyên — calibration số đếm kiểm bằng tần suất từng giá trị.
- **Bão Sandy ngay trước mốc dự báo**: ETS và BSTS (nhiễu Gauss) bị kéo mức xuống ~3.000 lượt (MAE 1.885 / 2.325, BSTS phủ 46,7%); GP nhiễu
  Student-t không bị kéo (MAE 1.142, phủ 81,7%).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lab 1 "prior predictive cho local level" | nhỏ | Làm trên Poisson phân cấp (cùng bài học, một mô hình ít hơn) |
| Lab 5 "cố tình chạy mô hình divergence, sửa bằng non-centered" | nhỏ | Divergence thật từ GP ba thành phần (sửa cấu trúc); non-centered trên 8 trường |
| GP "trend + periodic tuần + periodic năm + noise" | nhỏ | Hai năm không đủ tách xu hướng và mùa năm → một thành phần mượt + tuần + nhiễu Student-t; phiên bản đủ ba thành phần là chỗ hở của `code/` |
| "Xong khi: phân cấp Bayes thắng no-pooling, r_hat < 1,01" | — | Đạt: RMSE 1,182 so với 1,212; r_hat 1,006, ESS 1.208, 0 divergence (2.000 mẫu/chuỗi; 1.000 mẫu cho r_hat 1,011 — không qua cổng) |

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0; máy soạn 12 nhân; ~15 phút)

| Mục | Số |
|---|---|
| Ví dụ tay Gamma–Poisson | prior Gamma(2, 1) (trung bình 2), thấy 0, 1, 0 → posterior Gamma(3, 4), trung bình 0,75; không gộp 0,333; P(0 món tháng tới) 0,511 |
| Prior predictive | rộng Normal(0, 10) + HalfNormal(10): trung vị 2, q90 1,99·10⁷, q99 1,91·10¹⁴; hẹp (1, 1): 1 / 6 / 38; dữ liệu: 0 / 2 / 5, lớn nhất 22 |
| Car Parts học | 3.375 tháng-mã, 72,6% bằng 0, trung bình 0,5 |
| Phân cấp | μ −1,17 (e^μ ≈ 0,31 món/tháng), τ 0,978; r_hat 1,0061, ESS 1.208, 0 divergence |
| RMSE 12 tháng chấm | không gộp 1,212; gộp hoàn toàn 1,191; gộp một phần 1,182. Theo lịch sử 3 / 6 / 12 / 24 tháng: không gộp 1,622 / 0,918 / 1,267 / 0,895; hoàn toàn 1,568 / 0,875 / 1,296 / 0,879; một phần 1,560 / 0,886 / 1,258 / 0,886 |
| Mã toàn 0 | 71 mã không gộp đoán 0; 46 trong đó có bán trong 12 tháng chấm. 35 mã 3 tháng toàn 0: gộp một phần 0,221, thật 0,221; 12 tháng toàn 0 (14 mã): 0,11, thật 0,19 |
| Tần suất số đếm | 0 / 1 / 2 / ≥ 3 món: dự báo 0,676 / 0,221 / 0,067 / 0,036; thật 0,787 / 0,127 / 0,049 / 0,037 |
| Coverage khoảng phân cấp | 50% → 0,864; 80% → 0,944; 90% → 0,959 |
| 8 trường | centered: target 0,8 → 312 div, r_hat 1,243, ESS 12; 0,95 → 64 div, r_hat 1,019, ESS 150. Non-centered: 0,8 → 10 div; 0,95 → 0 div, r_hat 1,002, ESS 3.008 |
| Xe đạp 60 ngày | ETS MAE 1.885, phủ 90%: 85,0%; GP ba thành phần 27 div, r_hat 1,026, MAE 1.071; GP hai thành phần 0 div, r_hat 1,003, ESS 686, MAE 1.142, phủ 81,7%; BSTS 0 div, r_hat 1,002, MAE 2.325, phủ 46,7%; seasonal naive 7 ngày MAE 2.631 |
| Thời gian (máy 12 nhân) | phân cấp ~15 s; GP hai thành phần ~150 s; GP ba thành phần ~220 s; BSTS ~200 s; `check --dap-an` 2 phút 40; `check` (code) 5 phút 07; notebook 7 phút 20 |

## Đọc thử (2026-09-24, Phase 26, tự đọc — không subagent)

**Vòng 1 (đọc toàn bộ `tai-lieu.md`, vai học viên mới).** Tính lại mọi ví dụ bằng Python: Gamma(3, 4) → 0,75; Gamma(6, 13) → 0,4615; $e^{9{,}2}$ = 9.897;
$e^{\pm 6}$ = 0,0025 / 403; kernel 0,8825 / 0,1353 / 0,6065; BSTS tay 8,614 → 5.510 lượt; 671³ = 3,02·10⁸. Bắt được bốn lỗi của chính bài viết:

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.3 ví dụ | "Phương sai trong mỗi chuỗi là 1; hai trung bình 2 và 6 có phương sai 8" | 4 | dùng phương sai chia n − 1, trái định nghĩa "trung bình bình phương độ lệch" ở mục 2 → học viên tính ra 0,67 và 4 | khó |
| 2 | 4.4 Đọc bảng | "gộp một phần thắng không gộp ở ba trong bốn nhóm" | 4 | bảng cho thắng cả bốn nhóm | khó |
| 3 | 4.6 | "Student-t$_4$" | 1 | số 4 chưa nói là gì | nhỏ |
| 4 | trước vòng 1 | "Mượn trước — state space … Buổi 30 dùng lại" | 8 | state space/Kalman đã học ở buổi 16–17 và 20; buổi 30 không dùng lại | khó (sửa trước khi đọc thử) |

Sửa: #1 ví dụ r_hat dùng đúng định nghĩa (2,6 và 1,17; câu quiz 6 đổi thành 1,12); #2 "cả bốn nhóm"; #3 thêm "độ dày đuôi"; #4 chuyển thành gạch nhắc lại ở
mục 2, bỏ câu buổi 30. Trước vòng đọc cũng sửa ba câu viết theo mắt (kernel ví dụ là ExpQuad còn mô hình dùng Matern; số hàm cơ sở phần tuần; con số
divergence ghi rõ target_accept 0,9).

**B — giải thích lại (ví dụ mới):** Gamma(1, 2), thấy 2 món trong 2 tháng → Gamma(3, 4), 0,75; prior log λ ~ Normal(0, 4) → ± 2 độ lệch chuẩn là
$e^{\pm 8}$ ≈ 0,0003 tới 2.981 món — vô lý; hai chuỗi trung bình 5 và 5,2, phương sai trong chuỗi 1 → r_hat ≈ √1,01 ≈ 1,005; mã 6 tháng toàn 0 → gộp một
phần 0,16; BSTS: mức 8,0, xu hướng 0 + mùa −0,2 → e^7,8; kernel ℓ 10, d 20 → e^−2. Không khái niệm nào "không giải thích được".

**C — quiz:** 1, 8 → 4.2; 2, 4, 6 → 4.3; 3 → 4.4; 5 → 4.1; 7 → 4.6; 9 → 4.3 + 4.6; 10 → 4.5. Tính lại: Q5 0,6; Q6 1,118; Q7 0,6065 / 0,1353;
Q8 4,5·10⁻⁵ / 22.026; Q9 6,2%.

**Rà gọn (vai biên tập viên):** "hội tụ không thay được kiểm coverage" có ở Đọc số và Tóm lại 4.5 (một câu, giữ vì là tóm lại). Không đoạn ≥ 30 chữ lặp ý.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| 1 | 4.110 | 13 | 0 | 2 | 1 | 10/10 | 0 |
| sau sửa | 4.146 | 13 | **0** | **0** | 0 | 10/10 | 0 |

Vòng 2 đọc lại các đoạn đã sửa trong ngữ cảnh (mục 2, 4.3, 4.4, 4.6); phần còn lại không đổi so với vòng 1. `kiem_de_hieu.py 27`: 0 vi phạm (vòng
đầu 26 chỗ nhiều số / câu dài — sửa bằng tách đoạn, số nhỏ viết chữ, dữ liệu ví dụ vào công thức).

## Đọc thử độc lập (Phase 27, 2026-09-25)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: $e^{-0,5}$ = 0,607; Gamma(3, 4) → 0,75 = ¼ × 2 + ¾ × ⅓;
P(0 món) posterior predictive = (4/5)³ = 0,512; tự kiểm tra 6/13 = 0,46 và Gamma(14, 5) → 2,8; $e^{9,2}$ = 9.897; $e^{\pm 6}$ = 0,0025 / 403; r_hat √7 = 2,65
và √1,375 = 1,17; (2 + 8)/25 = 0,40; $e^{-1,17}$ = 0,31; 8,614 → 5.503 lượt; kernel 0,8825 / 0,135 / 0,607; 671³ ≈ 3,0 · 10⁸; hai bảng tần suất cộng 100%;
RMSE "thắng ở cả bốn nhóm" và "gộp hoàn toàn nhỉnh ở 6 và 24 tháng" đúng; MAE GP ba thành phần thấp hơn 6,2%. Gộp hoàn toàn 0,5 = trung bình toàn bộ
tháng học (`dap-an/bayes.py`).

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.2 (dùng đầu tiên ở "Từ mới") | "log tốc độ bán ~ $\text{Normal}(0, 10)$"; "nhiễu Gauss" (4.5) | 8 | mục 2 không nhắc phân phối chuẩn, ký hiệu "~", số thứ hai là độ lệch chuẩn hay phương sai; "Gauss" = chuẩn không nói. Tự kiểm tra 4.2 và quiz 8 cần biết số thứ hai là độ lệch chuẩn | khó |
| 2 | 4.3 | "Ví dụ 8 trường" | 8 | chỉ biết qua trục ngang của hình ("hiệu quả luyện thi ở trường 1"); không nói dữ liệu gồm gì, vì sao có θ, μ, τ | khó |
| 3 | 4.2, Lab bước 1 | "Phân vị 90% của số món…" | 1 | "phân vị" chưa định nghĩa; mục 2 gọi là quantile | nhỏ |
| 4 | 4.3 bảng | cột `target_accept` | 1 | nghĩa ("bước đi nhỏ hơn") ở câu sau bảng | nhỏ |
| 5 | 4.6 | $\eta$; $\sigma$ trong Student-t$_4(f(t), \sigma)$ | 2 | không có trong danh sách ký hiệu | nhỏ |
| 6 | 6 | "tăng số mẫu (1.000 → 2.000 ở mục 4.4)" | 4 | mục 4.4 không nói số mẫu | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Prior + dữ liệu**: Gamma(4, 2) (trung bình 2, "đáng giá" 2 tháng), 6 tháng bán tổng 3 → Gamma(7, 8) = 0,875 = ¼ × 2 + ¾ × 0,5.
- **Prior predictive**: log λ ~ Normal(0, 4) → ± 8 → λ tới $e^8$ ≈ 3.000 món/tháng: vô lý.
- **r_hat**: chuỗi 4, 5, 6 và 4, 6, 8 → trung bình 5 và 6, phương sai giữa 0,25, trong (0,67 + 2,67)/2 ≈ 1,67 → √1,15 ≈ 1,07: chưa dùng.
- **Partial pooling**: prior Gamma(2, 1), mã 6 tháng tổng 0 → 2/7 ≈ 0,29 thay vì 0.
- **BSTS**: mức 7, xu hướng −0,01, hiệu ứng CN −0,2, 14 ngày → 7 − 0,14 − 0,2 = 6,66.
- **Kernel**: ℓ = 10, cách 20 → $e^{-2}$ ≈ 0,14.

### C. Quiz mù

1 A · 2 B · 3 B · 4 B · 5 Gamma(3, 5), 0,6 (dữ liệu 0,5) · 6 ≈ 1,12, không dùng · 7 0,61; 0,14 · 8 A · 9 GP ba thành phần chưa qua cổng · 10 hội tụ ≠ mô hình
đúng, coverage 46,7%. Căn cứ: 1, 8 → 4.2; 2, 4, 6 → 4.3; 3 → 4.4; 5 → 4.1; 7, 9 → 4.6; 10 → 4.5. Câu 8 "chắc" chỉ nhờ tự kiểm tra 4.2 cho mẫu Normal(0, 3) → ± 6
(chỗ vướng #1).

### D. Tổng kết

Chặn 0 / khó 2 / nhỏ 4. Sửa một điều: nhắc phân phối chuẩn + ký hiệu "~" ở mục 2.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý. "Chi phí" GP và dòng HSGP ở "Lỗi thường gặp" trùng ý nhưng dưới 30 chữ.

### Chấm, sửa, đọc lại

**Quiz mù 10/10**; `kiem-tra.md` câu 1 đổi "phân vị 90%" → "quantile 0,9". Sửa: #1 mục 2 thêm hai dòng phân phối chuẩn (Gauss), $\text{Normal}(\mu, \sigma)$
với σ là độ lệch chuẩn, ± 2σ ≈ 95%, ký hiệu "~"; #2 đoạn "Cái phễu" mở bằng một câu nói ví dụ 8 trường là gì (θ, μ, τ), trục hình bỏ phần trùng; #3
"phân vị 90%" → "quantile 0,9" (4.2, Lab bước 1); #4 câu dẫn bảng 8 trường nói `target_accept` trước bảng; #5 thêm $d$, $\eta$, $\sigma$ vào ký hiệu 4.6;
#6 "Lỗi thường gặp": "mô hình mục 4.4 dùng 2.000" (khớp `VONG_LAP`).

| Vòng | Chữ | Trang | Chặn / khó / nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|
| Phase 27 đọc mù | 4.146 | 13 | 0 / 2 / 4 | 10/10 | 0 |
| sau sửa, đọc lại | 4.212 | 13 | **0 / 0 / 0** | 10/10 | 0 |

`kiem_de_hieu.py 27`: 0 vi phạm. Thêm chữ để vá mắt xích (định nghĩa, câu dẫn); lượt rà gọn sau sửa không thấy đoạn ≥ 30 chữ bớt được.
