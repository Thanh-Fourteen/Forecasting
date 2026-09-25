# Nhật ký research — Buổi 26: Conformal prediction cho chuỗi thời gian

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-24
- **Người/phiên:** Phase 25 (soạn buổi 25–26)

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Gibbs, I. & Candès, E. (2021). Adaptive conformal inference under distribution shift. *NeurIPS 2021*. https://arxiv.org/abs/2106.00170 (PDF đọc bằng pypdf) | bài gốc | 2026-09-24 | 4.5: $\alpha_{t+1} = \alpha_t + \gamma(\alpha - err_t)$ (pt. 2); Mệnh đề 4.1: $\lvert \frac1T\sum err_t - \alpha\rvert \le \frac{\max(\alpha_1, 1-\alpha_1)+\gamma}{T\gamma}$ với mọi dữ liệu; $\alpha_t < 0$ → khoảng vô hạn; thí nghiệm dùng γ = 0,005 |
| 2 | Xu, C. & Xie, Y. (2021). Conformal prediction interval for dynamic time-series. *ICML 2021* (EnbPI). https://arxiv.org/abs/2010.09107 | bài gốc | 2026-09-24 | 4.4: bootstrap ensemble, phần dư ngoài túi (leave-one-out), cửa sổ phần dư trượt không cần học lại |
| 3 | Romano, Y., Patterson, E. & Candès, E. (2019). Conformalized quantile regression. *NeurIPS 2019* | bài gốc | 2026-09-24 | 4.3: điểm $\max(\hat q_{lo} - y, y - \hat q_{hi})$ |
| 4 | Angelopoulos, A.N. & Bates, S. — A Gentle Introduction to Conformal Prediction (arXiv 2107.07511) | tổng quan | 2026-09-24 | 4.1: quantile $\lceil (n+1)(1-\alpha)\rceil / n$; bảo đảm là coverage TRUNG BÌNH (marginal), không phải có điều kiện |
| 5 | Sabashvili, A. (2026). Conformal Prediction Algorithms for Time Series Forecasting: Methods and Benchmarking. arXiv 2601.18509v2 (30/1/2026) | benchmark mới | 2026-09-24 | 4.6: >3.000 chuỗi bán hàng tháng, AutoARIMA, mục tiêu 90%: split nhiều bước (MSCP), ACI, AcMCP, Global-CP đạt; **EnbPI, SPCI, Nixtla-CP không đạt**; MSCP hẹp nhất |
| 6 | MAPIE 1.5.0 — tutorial chuỗi thời gian https://mapie.readthedocs.io/en/stable/generated/regression/1-quickstart/plot_ts-tutorial/ + kiểm chữ ký bằng `inspect` | tài liệu chính thức | 2026-09-24 | 4.6: `TimeSeriesRegressor(method="enbpi"|"aci", cv=BlockBootstrap(...))`, `fit`, `update`, `adapt_conformal_inference(X, y, gamma)`, `predict(confidence_level=..., ensemble=True, allow_infinite_bounds=True)` |
| 7 | MAPIE 1.5.0 `mapie.exchangeability_testing` (`OnlineMartingaleTest`, `PValuePermutationTest`…) — kiểm bằng `inspect` | tài liệu chính thức | 2026-09-24 | "Đọc thêm": kiểm định exchangeability có sẵn |
| 8 | statsforecast `ConformalIntervals(h, n_windows)` https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/conformalprediction.html | tài liệu chính thức | 2026-09-24 | chỉ nhắc ở 4.6 (split theo từng h cho mô hình thống kê) |
| 9 | Zaffran, M. et al. (2022). Adaptive conformal predictions for time series (AgACI). *ICML 2022* | bài gốc | 2026-09-24 | "Đọc thêm": chọn γ bằng gộp nhiều γ |

## Phiên bản đã xác minh (PyPI 2026-09-24, khớp `tools/nen/phien-ban.toml`)

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| mapie | 1.5.0 (5/8/2026) | API 1.x: `confidence_level` thay `alpha`; lớp `SplitConformalRegressor`, `ConformalizedQuantileRegressor`, `TimeSeriesRegressor` |
| lightgbm | 4.7.0 | |
| scikit-learn | 1.9.1 | |
| pandas | 3.0.5 | nền không có Nixtla (đã bỏ statsforecast khỏi `thu_vien` vì buổi không chạy nó) |

## Dữ liệu

| Bộ | sha256[:12] | Giấy phép | Dùng |
|---|---|---|---|
| `uci-beijing-air` (tệp Dongsi) | theo danh mục | CC BY 4.0 | PM2.5 theo giờ 3/2013 → 2/2017, 35.064 giờ, 750 giờ trống (nội suy ≤ 3 giờ liền) |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Chọn γ trung thực:** thử chọn γ trên năm hiệu chỉnh (nửa đầu làm tập điểm, chạy ACI nửa sau, lấy γ giữ coverage 30 ngày trong
  [85%, 95%] nhiều nhất) ra γ = 0,002; trên đoạn kiểm γ đó ra ngoài dải 8,6% thời gian. Giá trị bài gốc γ = 0,005 (định trước) ra ngoài
  1,1%. Chọn γ = 0,01 vì bảng đoạn kiểm đẹp nhất (0%) là tune trên đoạn kiểm (buổi 24). → Buổi dùng γ = 0,005 và trình bày bảng γ như bài
  học đánh đổi: γ lớn bám nhanh hơn nhưng nhiều giờ khoảng vô hạn (0,02 → 152 giờ).
- **Coverage có điều kiện:** ACI sửa trượt theo thời gian nhưng không sửa theo "độ khó": giờ có PM2.5 giờ trước > 150 µg/m³ ACI chỉ phủ
  76,6%, split 71,8%, CQR 88,2%. → 4.3 và 4.5.
- **EnbPI giữ đủ một năm phần dư thì trượt gần như split** (ra ngoài dải 24,6% thời gian); cửa sổ 30 ngày: 13,2%. Khớp benchmark #5 (EnbPI
  không đạt coverage).
- **Mô hình điểm phải thắng naive trước:** LightGBM học mức PM2.5 (MAE 11,6) thua naive "giờ tới = giờ này" (10,65). Học bước nhảy + lá ≥ 300
  dòng: 10,37. Seasonal naive 24 giờ rất kém (60,1) vì PM2.5 không lặp theo ngày.
- **Drift ở đây chủ yếu là mùa**, không phải xu hướng: PM2.5 trung bình theo năm (3 → 2): năm học 93,4; 84,0; 79,3; 88,4 µg/m³.
- **Kiểm rò rỉ cho khoảng trực tuyến:** `kiem_ro_ri` (đổi y từ mốc 50%/80%) chỉ kiểm được đúng một giờ ở mốc; biến thể ACI rò rỉ (thêm điểm
  giờ hiện tại vào tập trước khi tính khoảng) lọt qua. Test của buổi đặt thực tế của 20 giờ lần lượt bằng dự báo rồi bằng dự báo + 10.000:
  bắt được 15/20 vị trí với bản rò rỉ, 0/20 với bản đúng.
- Hiểu lầm hay gặp: "conformal bảo đảm 90% cho từng giờ" (chỉ trung bình); "ACI làm khoảng hẹp hơn" (nó sửa coverage, có lúc cho khoảng vô
  hạn); "dùng quantile 90% thường của phần dư là đủ" (thiếu hiệu chỉnh (n+1), lệch khi n nhỏ).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| "Xong khi: ACI giữ coverage 30 ngày trong [85%, 95%] suốt 2 năm" | nhỏ | Với γ định trước 0,005: ra ngoài 1,1% thời gian (thấp nhất 83,9%). Đổi tiêu chí thành "ra ngoài dải < 2% thời gian, split ra ngoài 29,5%"; cập nhật lo-trinh |
| Lab 4 "`ConformalIntervals` trong statsforecast và MAPIE" | nhỏ | Chỉ MAPIE (cùng LightGBM); statsforecast nhắc một câu ở 4.6 — benchmark #5 cho thấy Nixtla-CP không đạt coverage |
| "Kiểm định exchangeability (MAPIE)" | nhỏ | Đưa vào "Đọc thêm" (MAPIE 1.5 có `exchangeability_testing`); trong bài thay bằng bảng coverage theo quý — thấy vi phạm trực tiếp |
| "Conformal nhiều bước, nhiều chuỗi" | nhỏ | Một câu ở 4.6 (split riêng từng h như statsforecast/MSCP) |

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0; máy soạn 12 nhân; khoảng 80 giây)

| Mục | Số |
|---|---|
| Chia | học 3/2013 → 2/2014; hiệu chỉnh 3/2014 → 2/2015 (8.720 giờ đủ dữ liệu); kiểm 3/2015 → 2/2017 (17.067 giờ) |
| Điểm | MAE LightGBM 10,37; naive 10,65; seasonal naive 24 giờ 60,12 (µg/m³) |
| split | phủ 90,9%; coverage 30 ngày 74,7% → 99,3%; ra ngoài [85, 95] 29,5% thời gian; rộng trung vị 48,4; theo quý (1–4) 89,8 / 92,3 / 95,5 / 86,2% |
| CQR | 91,0%; 83,8 → 95,6%; ngoài dải 2,8%; rộng 39,4; theo quý 91,0 / 90,4 / 92,6 / 90,1% |
| ACI γ 0,005 | 90,0%; 83,9 → 95,1%; ngoài dải 1,1%; rộng 42,4; 7 giờ vô hạn; theo quý 91,0 / 90,0 / 90,3 / 88,9% |
| ACI γ 0,002 / 0,01 / 0,02 | ngoài dải 8,6% / 0% / 0%; giờ vô hạn 0 / 27 / 152 |
| EnbPI (20 mô hình, khối 24 giờ, cửa sổ 1 năm) | 89,7%; 72,9 → 98,9%; ngoài dải 24,6%; rộng 43,9; MAE ensemble 10,07. Cửa sổ 720 giờ: ngoài dải 13,2% |
| Có điều kiện (PM2.5 giờ trước) | ≤ 35 / 35–75 / 75–150 / > 150: split 98,9 / 95,0 / 87,1 / 71,8%; CQR 92,1 / 91,5 / 90,7 / 88,2%; ACI 98,4 / 92,3 / 83,7 / 76,6%; số giờ 6.328 / 4.008 / 4.022 / 2.709 |
| MAPIE 6 tháng đầu (ACI, γ 0,005, cập nhật mỗi 24 giờ) | phủ 90,7%; 30 ngày 88,2 → 94,3%; tự viết cùng 6 tháng 90,6%, 88,2 → 94,0% |
| Tuần 18–25/12/2015 | split 65/192 giờ ra ngoài; CQR 32/192 |
| Ví dụ tay | 10 điểm 1, 2, 2, 3, 3, 4, 5, 6, 8, 12: α 0,2 → 8; α 0,05 → vô hạn. ACI γ 0,05, lỗi 0, 0, 1, 0, 0: 0,1 → 0,105 → 0,11 → 0,065 → 0,07 → 0,075. CQR y (20, 55, 90, 140), q_lo (15, 40, 70, 100), q_hi (30, 60, 85, 150) → điểm −5, −5, 5, −10 |
| `code/` | PHUONG_PHAP = "split" → triển khai ngoài dải 29,5%; ACI ngược chiều → khoảng vô hạn 16.797/17.067 giờ, phủ 100% |

## Đọc thử (2026-09-24, Phase 25, tự đọc — không subagent)

**Vòng 1 (đọc toàn bộ `tai-lieu.md`, vai học viên mới).** Tính lại bằng Python (`conformal.py` đáp án): hạng ⌈11 × 0,8⌉ = 9 → 8; α 0,05 → vô hạn;
19 điểm → hạng 18, 8 điểm → vô hạn; CQR ví dụ → nới 5; ACI 0,1 → 0,105 → 0,11 → 0,065 → 0,07 → 0,075; cận Gibbs–Candès 0,905 / 85,3 = 0,0106;
$\hat q$ split = 48,38 / 2 = 24,2. Bắt được ba câu viết theo mắt: "vị trí 0,9 × 19 ≈ 17" → "giữa điểm thứ 17 và 18"; "mùa thu lên 0,3" → đỉnh α_t
ở tháng 9 (cuối hè); "MAPIE trong 88–94%" → 88–95%.

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.5 | "$\max(\alpha_1, 1-\alpha_1)$" | 2 | $\alpha_1$ chưa giải thích | khó |
| 2 | Lab bước 2–5 | "`ngoai_85_95` 0,295", "`gio_vo_han`" | 7 | khoá in ra chưa nói nghĩa | khó |
| 3 | 4.4 | "trung bình ensemble" | 8 | "ensemble" không nhắc ở mục 2 | nhỏ |
| 4 | 4.6 | `BlockBootstrap(...)` | 1 | chưa nói là gì | nhỏ |
| 5 | 4.5 | "tune trên đoạn kiểm (buổi 24)" | 8 | dựa vào buổi 24; câu sau đã nói hệ quả | nhỏ |

**B — giải thích lại (ví dụ mới):** 7 điểm 1…7, α 0,25 → hạng ⌈8 × 0,75⌉ = 6 → ± 6; hai mùa phủ 70% và 100% → trung bình 85% che lỗi mùa đầu;
CQR thực tế 100, khoảng [80; 95] → điểm 5; EnbPI 3 mô hình, giờ vắng ở mô hình 1 → sai số lấy từ mô hình 1; ACI γ 0,1, lỗi 1, 1 → 0,1 → 0,01 → −0,08
(khoảng vô hạn); coverage có điều kiện: cả năm 90% nhưng nhóm khó 76,6%. Không khái niệm nào "không giải thích được".

**C — quiz:** 1, 5 → 4.1; 2, 9 → 4.2 (+ 4.6 cho câu 9); 3, 6 → 4.3; 4, 7, 8, 10 → 4.5. Tính lại bằng Python: Q5 hạng 12 → 9 (và 90%: 15 so với 11);
Q6 nới 20; Q7 0,062 / 0,064; Q8 0,091 / 0,0091.

**Sửa:** #1 thêm "với α₁ là mức bắt đầu (ở đây bằng chính α)"; #2 Lab bước 2 nói nghĩa các khoá của `tom_tat`; #3 định nghĩa "ensemble" ở mục 2; #4 một
mệnh đề cho `BlockBootstrap`. Giữ #5. Vòng 2 (đọc lại các đoạn đã sửa trong ngữ cảnh; phần còn lại không đổi so với vòng 1): 0 chặn / 0 khó / 1 nhỏ.

**Rà gọn:** "chọn γ trước khi nhìn đoạn kiểm" có ở Đọc bảng, Tóm lại 4.5, Lỗi thường gặp, bài tập 2 — mỗi nơi một vai (giải thích / tóm / chẩn đoán /
thực hành), không cắt. Không đoạn ≥ 30 chữ lặp ý.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| 1 | 3.563 | 12 | 0 | 2 | 3 | 10/10 | 0 |
| sau sửa | 3.649 | 12 | **0** | **0** | 1 | 10/10 | 0 |

`kiem_de_hieu.py 26`: 0 vi phạm (vòng đầu 17 chỗ "nhiều số" + 2 viết tắt PM2.5, MAPIE — thêm vào bảng Từ mới).

## Đọc thử độc lập (Phase 27, 2026-09-25)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: 4.1 (⌈8,8⌉ = 9 → 8; 9/11; ⌈10,45⌉ = 11; tự kiểm tra
18 và ⌈8,1⌉ = 9; quantile NumPy 19 điểm ở vị trí 16,2 → giữa điểm 17 và 18); 4.2 (28% lỡ ≈ 2,8 lần 10%); bảng CQR 4 giờ (−5, −5, 5, −10 → 5);
4.4 (20 × 0,368 ≈ 7,4 mô hình vắng); bảng ACI 5 giờ; cận 0,905 / 85,3 = 0,0106; coverage có điều kiện gộp lại theo số giờ: split 0,909, CQR
0,910, ACI 0,900 (khớp coverage tổng).

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4 "Từ mới", conformal | "khoảng 80% = dự báo ± sai số lớn thứ 9" | 3 | "lớn thứ 9" đọc là thứ 9 từ trên xuống (số 2); thân bài lấy thứ 9 khi xếp tăng (số 8) | khó |
| 2 | 4.6 MAPIE | "`BlockBootstrap` … như mục 4.4" + `length=168` | 4 | mục 4.4 nói khối 24 giờ; không nói vì sao 168 | nhỏ |
| 3 | 4.5 | "ở mức $\alpha_t$ trên mọi điểm đã biết" | 1 | "điểm" ở đây là điểm conformal của mọi giờ trước đó — đoán được | nhỏ |
| 4 | 4.6 "Nhiều bước" | "`ConformalIntervals(h, n_windows)` của statsforecast" | 8 | statsforecast không nhắc ở mục 2 | nhỏ |
| 5 | 4 "Từ mới", ACI | "α = 0,1 → lỡ một giờ → 0,0955" | 4 | không nói γ = 0,005 | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Split conformal**: 4 điểm 1, 3, 5, 9, α = 0,2 → ⌈5 × 0,8⌉ = 4 → ± 9; α = 0,1 → ⌈4,5⌉ = 5 > 4 → vô hạn.
- **Không hoán đổi**: ba tháng phủ 95%, 95%, 80% → trung bình 90% mà tháng thứ ba lỡ gấp đôi.
- **CQR**: thật 10, khoảng [12; 20] → E = 2; thật 15 → E = max(−3, −5) = −3.
- **EnbPI**: mô hình A, B không thấy giờ 7, đoán 30 và 34, thật 35 → sai số ngoài túi 35 − 32 = 3.
- **ACI**: γ 0,01, α_t 0,1, lỗi 1, 0 → 0,091 → 0,092.
- **Coverage có điều kiện**: 100 giờ sạch phủ 95, 20 giờ bẩn phủ 13 → tổng 90% mà giờ bẩn 65%.

### C. Quiz mù

1 A · 2 B · 3 B · 4 B · 5 [41; 59] · 6 E = −10, 10, −20, −10, 20; nới 20 · 7 0,062; 0,064 · 8 0,091; 0,0091 · 9 trung bình che mùa đông thiếu ·
10 γ chọn trên đoạn kiểm; che 27 giờ vô hạn. Căn cứ: 1, 5 → 4.1; 2, 9 → 4.2; 3, 6 → 4.3; 4, 7, 8, 10 → 4.5. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 4. Sửa một điều: ví dụ "Từ mới" của conformal.

### E. Dài/lặp

Lab bước 3 nhắc lại số của mục 4.3 và 4.6 (chấp nhận: là "Đọc kết quả" để đối chiếu). Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10**; đáp án đúng hết. Sửa: #1 "sai số thứ 9 khi xếp tăng"; #2 "(ở đây khối 168 giờ, một tuần)" (`dap-an/conformal.py` dùng 24 cho
EnbPI tự viết, 24 × 7 cho MAPIE); #3 "trên điểm conformal của mọi giờ đã qua" (khớp `aci`); #5 ví dụ "Từ mới" ghi γ = 0,005. Giữ #4.

| Vòng | Chữ | Trang | Chặn / khó / nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|
| Phase 27 đọc mù | 3.649 | 12 | 0 / 1 / 4 | 10/10 | 0 |
| sau sửa, đọc lại | 3.661 | 12 | **0 / 0 / 1** | 10/10 | 0 |

`kiem_de_hieu.py 26`: 0 vi phạm. Thêm chữ để vá mắt xích (định nghĩa, câu dẫn); lượt rà gọn sau sửa không thấy đoạn ≥ 30 chữ bớt được.
