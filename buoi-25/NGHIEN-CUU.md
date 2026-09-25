# Nhật ký research — Buổi 25: Dự báo xác suất

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-24
- **Người/phiên:** Phase 25 (soạn buổi 25–26)

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Gneiting, T. & Raftery, A.E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102(477), 359–378. https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf | bài gốc | 2026-09-24 | 4.3: định nghĩa proper / strictly proper; CRPS dạng $E\lvert X-y\rvert - \tfrac12 E\lvert X-X'\rvert$ (phương trình 21); interval score; "tối đa độ sắc với điều kiện đã calibrate" (mục 1) |
| 2 | Bracher, J., Ray, E.L., Gneiting, T. & Reich, N.G. (2021). Evaluating epidemic forecasts in an interval format. *PLOS Comput Biol* 17(2): e1008618. https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618 | bài gốc | 2026-09-24 | 4.3: IS_α, WIS với $w_0$ = ½, $w_k$ = α_k/2, chia (K + ½); K = 0 thì WIS = sai số tuyệt đối; Forecast Hub dùng 23 quantile |
| 3 | Gneiting, T., Balabdaoui, F. & Raftery, A.E. (2007). Probabilistic forecasts, calibration and sharpness. *JRSS B* 69(2) | bài gốc (qua trích dẫn trong #1 và tv.ve) | 2026-09-24 | 4.4: PIT histogram — chữ U = quá hẹp, vòm = quá rộng, lệch = chệch |
| 4 | scoringrules 0.11.0 — mã nguồn `scoringrules/core/interval/_score.py` (PyPI, và nhánh chính GitHub frazane/scoringrules qua `gh api`) | thư viện | 2026-09-24 | 4.3 + "Lỗi thường gặp": `quantile_score`, `crps_ensemble` đúng; **`weighted_interval_score` sai** (xem Phát hiện) |
| 5 | LightGBM 4.7.0 Parameters (`objective="quantile"`, `alpha`) https://lightgbm.readthedocs.io/en/latest/Parameters.html | tài liệu chính thức | 2026-09-24 | 4.2 |
| 6 | Chernozhukov, V., Fernández-Val, I. & Galichon, A. (2010). Quantile and probability curves without crossing. *Econometrica* 78(3) | bài gốc | 2026-09-24 | 4.2: sắp xếp lại (rearrangement) sửa crossing và không làm tăng sai số |
| 7 | Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values*, Springer — ch. 4 (POT, GPD, mức lặp lại $x_N = u + \frac{\sigma}{\xi}[(N\lambda)^{\xi} - 1]$, tách cụm) | sách | 2026-09-24 | 4.5 |
| 8 | SciPy 1.18 `scipy.stats.genpareto` (quy ước dấu $c$ = ξ) | tài liệu chính thức | 2026-09-24 | 4.5 |
| 9 | Hyndman & Athanasopoulos, *FPP3* §5.5 (khoảng dự báo từ bootstrap phần dư), §5.9 (phần dư trong mẫu) https://otexts.com/fpp3/prediction-intervals.html | sách | 2026-09-24 | 4.1 |
| 10 | Open-Meteo Historical Weather API (ERA5), licence https://open-meteo.com/en/licence | dữ liệu | 2026-09-24 | 4.5 |

## Phiên bản đã xác minh (PyPI 2026-09-24, khớp `tools/nen/phien-ban.toml`)

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| lightgbm | 4.7.0 | `objective="quantile"` |
| scoringrules | 0.11.0 (6/2026, bản mới nhất) | Python ≥ 3.12 |
| scipy | 1.18.1 | `genpareto.fit(..., floc=0)` |
| pandas | 3.0.5 | nền không có Nixtla nên không bị chốt 2.3.3; chạy lại `ve_hinh.py` sau khi đổi: mọi số giống hệt bản pandas 2.3.3 |

## Dữ liệu

| Bộ | sha256[:12] | Giấy phép | Dùng |
|---|---|---|---|
| `eia930-balance-2024-h1/h2`, `2025-h1/h2` | 26768c495c3b, a602a8e577cf, fac4bb991dfa, 1146158b9724 | public domain (EIA) | ERCO theo giờ 1/2024 → 12/2025 |
| `open-meteo-du-bao-luu-erco-2024-2025` | ad8753a7ffe9 | CC BY 4.0 | nhiệt độ đã dự báo trước 24 giờ (Dallas) |
| `open-meteo-dallas-tmax-1940-2025` (**mới thêm vào danh mục**) | 15bc72f4d845 | CC BY 4.0 | POT, 31.412 ngày |

Bộ mới: tải 3 lần (cách ≥ 20 s) cùng sha256. Một lần tải liền tay nhận JSON "Minutely API request limit exceeded" thay cho CSV — ghi vào `ghi_chu`
của danh mục. Bản không có `models=era5` (best_match) khác số từ năm 1950 → luôn ghi `models=era5`.

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Lỗi trong scoringrules 0.11.0 (chưa ai báo):** `weighted_interval_score` cộng `w_median * median` thay vì `w_median * |obs − median|`
  (tệp `core/interval/_score.py`, dòng `WIS += w_median * median`; nhánh chính GitHub còn nguyên, 2026-09-24). Ví dụ: y = 10, trung vị 8,
  khoảng 80% [5; 9] → đúng 1,6, thư viện trả 3,6. Docstring còn ghi trọng số mặc định 2/α trong khi mã dùng α/2. → Buổi đối chiếu WIS tự
  viết bằng đồng nhất thức "WIS = tổng pinball ÷ (K + ½)" và `sr.quantile_score` (đúng); đưa vào "Lỗi thường gặp".
- **Phần dư trong mẫu hẹp hơn sai số thật** khi mô hình điểm linh hoạt: LightGBM 31 lá, lá tối thiểu 50 dòng — độ lệch chuẩn phần dư trên phần
  học 1.852 MW, ngoài mẫu 2.905 MW. Với mô hình đã điều chuẩn (15 lá, lá ≥ 1.000 dòng) khoảng trong mẫu lại gần đúng (90% → 90,3%): chỗ hở chỉ
  lộ khi mô hình điểm khớp sát — đúng tình huống thật vì mô hình điểm được chọn theo MAE.
- **LightGBM quantile quá hẹp và lệch** nếu học trên mức gốc: năm 2025 nhu cầu ERCOT cao hơn 2024 (trung bình quý 3: 61.426 → 63.971 MW), cây
  không ngoại suy (buổi 22) → trung vị chỉ 34,5% giờ nằm dưới. Trừ mức 7 ngày + lá ≥ 1.000 dòng → lệch ≤ 2,5 điểm ở cả 9 mức.
- **WIS/CRPS phạt calibration rất nhẹ:** khoảng trong mẫu (phủ 78% thay vì 90%) có WIS 1.412, gần bằng phần dư ngoài mẫu 1.408; mô hình
  không trừ mức (lệch rõ trên PIT) còn có WIS thấp nhất 1.387 vì hẹp hơn. Proper nghĩa là "khai đúng phân phối thật thì kỳ vọng điểm tốt
  nhất", không có nghĩa "mô hình calibrate luôn có điểm tốt hơn mô hình sắc mà lệch". → Buổi dạy: điểm tổng + kiểm calibration riêng.
- **Coverage hai mức vẫn lừa:** mô hình không trừ mức phủ 79,7% (80%) và 89,7% (90%) — đạt — mà PIT dốc rõ. Chỉ nhìn coverage 80/90 là không đủ.
- **POT trên 2 năm tải không dùng được:** đỉnh tải ngày ERCO 2024–2025 chỉ có 7 đợt độc lập trên ngưỡng quantile 95%, ξ = −1,04 (vô nghĩa).
  → Đổi sang 86 năm nhiệt độ tối đa Dallas (89 đợt trên 39 °C, ξ = −0,25).
- Hiểu lầm hay gặp: "mức 10 năm = xảy ra đúng một lần mỗi 10 năm"; "CRPS của mẫu = MAE trung bình các mẫu" (quên nửa sau → thưởng mẫu co cụm);
  "sắp xếp quantile là gian lận" (Chernozhukov et al. 2010: không làm tăng sai số).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lab 1 "ETS (chuẩn) vs bootstrap" | nhỏ | Thay bằng LightGBM + khoảng từ phần dư trong mẫu giả định chuẩn (chỗ hở) vs quantile phần dư ngoài mẫu (bootstrap phần dư). Cùng bài học, dùng chung mô hình của cả buổi; ETS chậm và kém trên tải giờ nhiều mùa vụ |
| Lab 5 "POT cho tải đỉnh ngày" | nhỏ | POT trên nhiệt độ tối đa ngày 1940–2025 (bộ dữ liệu mới), quy ra tải bằng một câu có khoảng; 2 năm tải chỉ đủ 7 đợt |
| "Khoảng nhiều bước, không cộng quantile" | nhỏ | Một câu trong 4.1 (sample path), không thành mục riêng (giới hạn 6 khái niệm) |
| statsforecast trong nen.toml | nhỏ | Bỏ khỏi `thu_vien` — buổi không dùng |
| scoringrules WIS có lỗi | nhỏ | Không dùng hàm đó để đối chiếu; ghi "Lỗi thường gặp" |

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0; máy soạn 12 nhân; backtest 12 giây)

| Mục | Số |
|---|---|
| Chấm | năm 2025, 8.527 giờ đủ dữ liệu (thiếu nhiệt độ đã dự báo ở một số giờ) |
| Điểm | MAE LightGBM 2.088 MW; seasonal naive (tuần trước) 4.777 MW |
| Phần dư | độ lệch chuẩn trên phần học (trung bình các tháng) 1.852; ngoài mẫu 2025: 2.905 |
| Crossing | 21,9% giờ có ít nhất một cặp quantile cắt nhau (thô) |
| Trong mẫu, chuẩn | tỷ lệ dưới 0,104 / 0,148 / 0,229 / 0,307 / 0,468 / 0,644 / 0,738 / 0,834 / 0,886; phủ 80% 68,7%, 90% 78,2%; WIS 1.412; rộng 90% 6.092 |
| Mượn seasonal naive | 0,006 … 0,981; phủ 94,8% / 97,5%; WIS 1.829; rộng 21.275 |
| Không trừ mức | 0,017 / 0,039 / 0,095 / 0,171 / 0,368 / 0,588 / 0,71 / 0,836 / 0,914; phủ 79,7% / 89,7%; WIS 1.387; rộng 9.183 |
| Phần dư ngoài mẫu | 0,051 / 0,103 / 0,201 / 0,301 / 0,497 / 0,696 / 0,802 / 0,897 / 0,94; phủ 79,4% / 88,8%; WIS 1.408; rộng 9.425 |
| LightGBM quantile (đã sắp) | 0,055 / 0,11 / 0,216 / 0,312 / 0,502 / 0,685 / 0,775 / 0,875 / 0,928; phủ 76,5% / 87,3%; WIS 1.483; rộng 9.329 |
| CRPS | phần dư ngoài mẫu, 200 mẫu: 1.571 |
| PIT (10 cột, chuẩn hoá) | trong mẫu 2,08 … 2,28 (chữ U); mượn SN 0,12 … 1,70 … 0,38 (vòm); không trừ mức 0,33 → 1,72 (dốc); ngoài mẫu 0,85–1,20 |
| POT | ngưỡng 39 °C, 89 đợt (tách khi ≥ 3 ngày dưới ngưỡng), 1,035 đợt/năm, ξ −0,251, σ 1,373; mức 2 / 10 / 50 / 100 năm: 39,9 / 41,4 / 42,4 / 42,8 °C; ngưỡng 38: 41,35; ngưỡng 40: 41,55; 7/86 năm có max vượt mức 10 năm; max quan sát 42,9 °C (18/8/2023) |
| Tải | ngày thường ≥ 32 °C: 2024 75 ngày, 2.223 MW/°C → 90.244 MW ở 41,4 °C (đỉnh năm 85.544); 2025 70 ngày, 1.247 MW/°C → 86.896 MW (đỉnh 83.597) |
| Ví dụ tay | pinball τ = 0,8 trên 1…10: q = 7 → 9,0; q = 8 / 8,5 / 9 → 8,0; CRPS mẫu (2, 4, 6), y = 5 → 7/9 ≈ 0,778; WIS trung vị 8, [5; 9], y = 10 → 1,6; mức 10 năm với ξ = 0, σ 1,4, λ 1 → 42,2 |

## Đọc thử (2026-09-24, Phase 25, tự đọc — không subagent)

**Vòng 1 (đọc toàn bộ `tai-lieu.md`, vai học viên mới).** Tính lại mọi ví dụ bằng Python (`xac_suat.py` đáp án): quantile 11 sai số −4 / 5;
pinball τ 0,8 trên 1…10 (9,0 / 8,0); CRPS (2, 4, 6) → 0,778, (1, 3) → 0,5; WIS 1,6; mức 10 năm ξ = 0 → 42,2; GPD thật 41,43; tỷ lệ 1,57 (sai số
ngoài/trong mẫu); tự kiểm tra 4.1 (−5,6 / 6,6). Bắt được một câu sai do viết theo mắt: "ba đợt nóng nhất (2011, 2018, 2023) lệch 0,3–0,4 °C"
→ thật là 2023, 2011, 2000, lệch 0,2–0,44 → sửa thành "năm đợt nóng nhất lệch 0,2–0,4 °C, bốn đợt từ 2011"; "rộng gấp đôi" → 2,3 lần.

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 2 → 4 | "Phần dư: sai số trên chính dữ liệu mô hình đã học" rồi "phần dư ngoài mẫu" | 1 | hai định nghĩa mâu thuẫn tên gọi | khó |
| 2 | 4.1 tự kiểm tra | "vị trí 0,1 × 8 = 0,8 giữa số thứ 1 và thứ 2" | 4 | cách nội suy quantile chưa dạy | khó |
| 3 | 4.1 | "bootstrap phần dư" | 1 | "bootstrap" chưa nhắc | nhỏ |
| 4 | 4.2 | "lá ít nhất 1.000 dòng" | 8 | "lá" không nhắc lại ở mục 2 | nhỏ |
| 5 | 4.2 | "MAE … tối thiểu nó ra trung vị" | 4 | nêu không chứng minh | nhỏ |
| 6 | 4.3 | "điểm kỳ vọng" | 1 | "kỳ vọng" dùng như trung bình dài hạn | nhỏ |
| 7 | 1 | "khớp với thư viện tới chữ số cuối" | 3 | WIS không so với thư viện (thư viện lỗi) | nhỏ |

**B — giải thích lại (ví dụ mới):** sai số ngoài mẫu −3, −1, 0, 2, 4 → khoảng 50% = dự báo −1 tới +2; pinball τ 0,25 trên 2, 4, 6, 8 → nhỏ nhất
trong đoạn 2–4; CRPS mẫu (0, 10), thực tế 5 → 5 − 2,5 = 2,5 (dự báo số 5: 0); WIS trung vị 10, [6; 12], thực tế 11 → 0,733; 20 giờ khoảng 90% lỡ
6 → chữ U; POT u 35, σ 2, ξ 0, λ 3 → mức 10 năm 41,8. Không khái niệm nào "không giải thích được".

**C — quiz:** 1 → 4.1; 2, 5 → 4.2; 3, 6, 7 → 4.3; 4, 9 → 4.4; 8 → 4.5 (ví dụ ξ = 0); 10 → 4.3 "Đọc số" + 4.4 "Tóm lại". Mọi đáp án tính lại bằng
Python (Q5 9 / 1; Q6 0,889; Q7 3,933; Q8 35,99; Q10 21,8%).

**Sửa:** #1 mục 2 định nghĩa cả "trong mẫu" và "ngoài mẫu"; #2 thêm một gạch "vị trí τ × (n − 1), đếm từ 0, nội suy" vào ví dụ 4.1 và viết lại đáp án;
#3 "rút ngẫu nhiên (có hoàn lại)"; #4 định nghĩa "lá" ở mục 2; #7 viết lại mục tiêu. Giữ #5, #6. Vòng 2 (đọc lại mục 2 → 4.1 nơi sửa, và 4.4 nơi cắt;
phần còn lại không đổi so với vòng 1): 0 chặn / 0 khó / 2 nhỏ.

**Rà gọn (vai biên tập viên):** 1 chỗ đáng kể — "coverage 80%/90% đạt chưa đủ" nói ba lần ở 4.4 (Vấn đề, Đọc bảng, Tóm lại) → viết lại "Vấn đề"
thành câu hỏi "kém theo kiểu nào". Còn lại: "Tóm lại" 4.3 nhắc lại ý cuối "Đọc số" (một câu, giữ vì là tóm lại).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| 1 | 4.248 | 14 | 0 | 2 | 5 | 10/10 | 1 |
| sau sửa | 4.337 | 14 | **0** | **0** | 2 | 10/10 | 0 |

`kiem_de_hieu.py 25`: 0 vi phạm (vòng đầu 26 chỗ "nhiều số trong một đoạn" — sửa bằng bảng POT/quy ra tải, số nhỏ viết bằng chữ, phép tính vào công thức).

## Đọc thử độc lập (Phase 27, 2026-09-25)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: 4.1 (3/11 ≈ 27%; quantile 0,1 = −4, 0,9 = 5;
tự kiểm tra −5,6 / 6,6); 4.2 (q = 7 → 9,0; q = 8, 9 → 8,0; mọi q ∈ [8; 9] → 8,0); CRPS (2, 4, 6) → 0,778, (1, 3) → 0,5; WIS 1,6 và bằng tổng
pinball ba mức 2,4 / 1,5; 1,57 lần; 2,26 lần; mức 10 năm 42,2 (ξ = 0) và 41,43 (ξ = −0,251, λ = 89/86); mức 50 năm 42,44; 1.866 / 8.527 = 21,9%.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | Lab bước 2 | "21,9% giờ có crossing; sau `du_bao_quantile` vẫn còn 1.866 giờ" | 5 | 1.866 giờ chính là 21,9% của 8.527; câu đọc như hai giai đoạn khác nhau | khó |
| 2 | 4.5 "Quy ra tải" | "trên những ngày thường nóng từ 32 °C" | 3 | "ngày thường" = ngày làm việc hay "thường nóng"? | khó |
| 3 | 4.3 "Đọc số" | "Nó không bảo đảm mô hình calibrate luôn có điểm tốt hơn…" | 4 | proper vừa hứa "khai đúng thì tốt nhất", ngay sau lại nói calibrate không chắc thắng; thiếu mắt xích "không mô hình nào khai đúng phân phối thật" | khó |
| 4 | 4.3 WIS | $m$: trung vị | 1 | $m$ vừa là số phần tử của mẫu trong công thức CRPS ngay trên | nhỏ |
| 5 | 4.3 | "WIS bằng tổng pinball loss của chín mức chia cho 4,5" | 4 | nêu không kiểm; ví dụ tay ngay dưới kiểm được mà không nói | nhỏ |
| 6 | 4.5 | "σ = 1,4 °C (cỡ của phần vượt)" | 1 | σ ở mục 2 là độ lệch chuẩn; ở đây là tham số cỡ của GPD | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Khoảng ngoài mẫu**: sai số −3, −1, 0, 2, 7; quantile 0,5 = 0; dự báo 100 → trung vị 100, phía trên dài hơn phía dưới.
- **Pinball**: τ = 0,3, số 1…10: q = 3 → 0,7 × 3 + 0,3 × 28 = 10,5; q = 4 → 0,7 × 6 + 0,3 × 21 = 10,5; nhỏ nhất ở quantile 0,3.
- **CRPS**: mẫu (3, 3), thực tế 5 → 2 − 0 = 2; mẫu (3, 7) → 2 − 1 = 1: trải hợp lý thắng.
- **WIS**: trung vị 5, khoảng 80% [2; 8], thực tế 5 → IS = 6, WIS = (0 + 0,6)/1,5 = 0,4.
- **PIT**: 20 giờ, 0 giờ dưới q 0,1, 0 giờ trên q 0,9 → vòm, quá rộng.
- **POT**: u 35, σ 1, ξ 0, λ 2 → mức 5 năm 35 + ln 10 ≈ 37,3.

### C. Quiz mù

1 A · 2 C · 3 A · 4 B · 5 9 và 1, dự báo 40 tốt hơn · 6 B · 7 IS 29, WIS ≈ 3,93 · 8 36 °C · 9 B · 10 P chưa calibrate (78,2%), chọn Q.
Căn cứ: 1 → 4.1; 2, 5 → 4.2; 3, 6, 7 → 4.3; 4, 9, 10 → 4.4 (+ "Đọc số" 4.3); 8 → 4.5. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 3 / nhỏ 3. Sửa một điều: câu Lab bước 2.

### E. Dài/lặp

"Buổi dùng ngưỡng giữa: 1,035 đợt mỗi năm, σ = 1,373, mức 50 năm" đứng lẻ sau "Đọc bảng", các số đã có trong "Nói bằng lời" — dưới 30 chữ.
Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10**; đáp án của ta đúng hết (tính lại). Sửa: #1 Lab bước 2 "1.866 giờ (21,9%) có crossing, vì `sua_crossing` chưa sửa gì"; #2
"các ngày thứ Hai–thứ Sáu có nhiệt độ tối đa từ 32 °C" (khớp `dap-an/ve_hinh.py`, `dayofweek < 5`); #3 "Đọc số" 4.3 thêm mắt xích "không mô hình
nào khai đúng phân phối thật; giữa hai mô hình đều sai…"; #4 trung vị trong WIS đổi $m$ → $q_{0,5}$; #5 ví dụ WIS kiểm luôn "tổng pinball ba mức 2,4
chia 1,5"; #6 σ ở POT ghi "tham số cỡ, không phải độ lệch chuẩn".

| Vòng | Chữ | Trang | Chặn / khó / nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|
| Phase 27 đọc mù | 4.337 | 14 | 0 / 3 / 3 | 10/10 | 0 |
| sau sửa, đọc lại | 4.375 | 14 | **0 / 0 / 0** | 10/10 | 0 |

`kiem_de_hieu.py 25`: 0 vi phạm. Thêm chữ để vá mắt xích (định nghĩa, câu dẫn); lượt rà gọn sau sửa không thấy đoạn ≥ 30 chữ bớt được.
