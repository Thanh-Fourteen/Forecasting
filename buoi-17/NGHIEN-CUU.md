# Nhật ký research — Buổi 17: ARIMA và SARIMA

- **Ngày research:** 2026-09-19 (Phase 17). "Bản nháp" chỉ là khuôn: code, đáp án, bộ chấm, hình, notebook, tài liệu soạn mới.
- **Người/phiên:** Phase 17, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | FPP3 ch. 9 (9.1 dừng và sai phân, 9.3 AR, 9.4 MA, 9.5 ARIMA không mùa vụ, 9.6 ước lượng và AICc, 9.7 Hyndman–Khandakar + quy trình 7 bước, 9.9 SARIMA): https://otexts.com/fpp3/arima.html, https://otexts.com/fpp3/arima-r.html | sách giáo khoa | 2026-09-19 | 4.1–4.5 |
| 2 | Hyndman & Khandakar (2008), JSS 27(3): $d$ bằng KPSS lặp (0 ≤ d ≤ 2), bốn mô hình khởi đầu, dò ±1 theo AICc, hằng số trừ khi d = 2 | bài gốc (qua FPP 9.7) | 2026-09-19 | 4.3 |
| 3 | statsforecast 2.1.1: `AutoARIMA(d, D, max_p=5, …, seasonal=True, ic='aicc', stepwise=True, season_length=1, …)` — **season_length mặc định 1**; `ARIMA(order, seasonal_order, season_length, include_constant)`; `model_['arma']` = (p, q, P, Q, m, d, D): https://nixtlaverse.nixtla.io/statsforecast/src/core/models.html | tài liệu chính thức | 2026-09-19 | 4.3, code |
| 4 | Release notes statsforecast 2.1.1 (16/7/2026): "ARIMA fixes"; 2.1.0: phân phối sai số t, GED… cho ARIMA | changelog | 2026-09-19 | phiên bản |
| 5 | Ljung & Box (1978), Biometrika 65(2); `statsmodels.stats.diagnostic.acorr_ljungbox(model_df=…)` | bài gốc, tài liệu | 2026-09-19 | 4.4 (test khớp) |
| 6 | Federal Reserve G.17 (IP.B50001.S, đã khử mùa vụ), public domain | dữ liệu | danh mục | 4.2 |

## Phiên bản đã xác minh

statsforecast 2.1.1 (mới nhất, 16/7/2026), statsmodels 0.15.0, pandas 2.3.3.

## Dữ liệu và một điểm lệch quan trọng

Bộ `frb-g17-san-luong-cong-nghiep` trong danh mục là chuỗi **đã khử mùa vụ** (s.a.), nên không dạy được SARIMA. Buổi dùng G.17 cho ARIMA không
mùa vụ (4.2) và Tourism Monthly (mùa vụ mạnh) cho SARIMA, auto-ARIMA, backtest. Lộ trình ghi "chuỗi kinh tế tháng: tự xác định SARIMA": thay
bằng chuỗi du lịch T33 (330 tháng, dương).

## Số liệu thật (`dap-an/ve_hinh.py`)

| Đại lượng | Giá trị |
|---|---|
| Mô phỏng 500 điểm, seed 1 | AR(2) φ = (0,6; 0,3): PACF 0,80; 0,29; −0,09. MA(1) θ = 0,8: ACF 0,51; 0,04 (lý thuyết 0,49). ARMA(1,1): ACF 0,82; 0,57; 0,37; PACF 0,82; −0,31; 0,05 |
| IP 2000–2019, 100 × sai phân log | ACF 0,24; 0,26; 0,32; 0,32; 0,20; PACF 0,24; 0,22; 0,24; 0,21; 0,02; ngưỡng 0,127 |
| AICc (d = 1, drift), Ljung–Box p | (1,1,0) 466,9 / 0,000; (4,1,0) 437,2 / 0,44; (1,1,1) 445,0 / 0,15; (2,1,2) 433,6 / 0,78; auto → (2,1,2) không drift 431,8 / 0,78 |
| T33 log, 306 tháng, ACF sau hai lần sai phân | trễ 1: −0,53; 12: −0,39; 11: 0,31; 13: 0,17; 24: −0,06 |
| T33: AICc, Ljung–Box (24 trễ) | ARIMA(0,1,1) 181,0, p ≈ 1e−123, ACF phần dư trễ 12 = 0,84; SARIMA(0,1,1)(0,1,1)12 −435,17, p 0,34, ma1 −0,735, sma1 −0,531; auto → (0,1,1)(0,1,2)12 −436,12, p 0,31 |
| Khoảng 95% ARIMA(0,1,0) trên log T33 | độ rộng bước 1, 4, 16: 1,274; 2,548; 5,095 (đúng √h) |
| 366 chuỗi, 2 cửa sổ 24 tháng | MASE TB / trung vị: AutoARIMA 1,574 / 1,430; AutoETS 1,581 / 1,392; seasonal naive 1,720 / 1,534; AutoARIMA season_length = 1: 2,791 / 2,284 |
| DM trên chênh MASE (h = 1) | ARIMA − snaive −7,26, p < 0,0001, thắng 68,6%; ETS − snaive −5,23, 70,5%; ARIMA − ETS −0,33, p 0,74, 50,3% |
| Thời gian | backtest 366 chuỗi ~6 phút (AutoARIMA mùa vụ chiếm phần lớn) → notebook lưu cache `du-lieu/cache/`; bộ chấm dùng 6 chuỗi, 1 cửa sổ |

## Phát hiện mới / lỗi hiểu sai phổ biến

- `AutoARIMA()` không khai `season_length` → không bao giờ thử mùa vụ; trên Tourism thua cả seasonal naive (2,791 so với 1,720). Chỗ hở chính.
- Đọc PACF ra AR(4) cho IP: qua Ljung–Box nhưng AICc kém 5,4 so với ARMA(2,2) của auto-ARIMA — minh hoạ giới hạn đọc ACF/PACF khi chuỗi là ARMA.
- Không so AICc giữa các mô hình khác d hoặc D (likelihood trên dữ liệu khác nhau).
- MA(1) không thể có ACF trễ 1 lớn hơn 0,5 (θ/(1+θ²) ≤ 0,5) — bắt được khi đọc thử câu tự kiểm tra của bản đầu (ghi 0,6), đã sửa.

## Research viết lại (sư phạm)

- AR "nhớ giá trị", MA "nhớ cú nhiễu": ví dụ AR(1) dự báo 8 → 4 → 2; MA(1) hai ngày liền chung một cú nhiễu.
- Bảng dấu vân tay ACF/PACF (FPP 9.5) + cảnh báo ARMA.
- √h: "muốn khoảng rộng gấp đôi phải nhìn xa gấp bốn".

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| G.17 đã khử mùa vụ | nhỏ | ARIMA không mùa vụ trên G.17; SARIMA trên Tourism T33 |
| "AICc trong 2 đơn vị so với auto-ARIMA" | nhỏ | đạt trên T33 (0,9); trên IP thì AR(4) cách 5,4 — dạy như giới hạn của ACF/PACF |
| Chỗ hở "không kiểm phần dư" | nhỏ | `kiem_phan_du` giả luôn "ổn" + `mo_hinh_tu_chon` mặc định quên mùa vụ; bảng `quy-uoc.md` cập nhật |

## Đọc thử (Phase 17, 2026-09-19)

Tự đọc (không subagent). Tính lại: AR(1) 8 → 4 → 2; MA(1) θ 0,8 → r₁ 0,488; Ljung–Box tay Q 10,31, p 0,0058 (ngưỡng 5,99); quiz 6 Q 14,76, p 0,0006;
bước ngẫu nhiên σ 2 → ± 3,92 / 7,84; quiz 7 → ± 5,88 / 29,4; auto-ARIMA IP không drift (AICc 431,79 = ARIMA(2,1,2) không hằng số).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 3.365 → 3.575 | 11 | 0 | 1 | 2 | 10/10 có căn cứ | khó: tự kiểm tra 4.1 ghi ACF trễ 1 của MA(1) là 0,6 — không thể (≤ 0,5). Nhỏ: SES, DM chưa trong bảng; "FPP" chưa mở tên |
| 2 | sau sửa | 11 | **0** | **0** | 0 | 10/10 | đổi 0,4 và thêm câu "MA(1) không bao giờ cho ACF đầu quá một nửa"; thêm "Khi nào dùng" cho 4.1, 4.4, 4.5 |
| rà gọn | biên tập viên | — | — | — | — | — | 0 chỗ thừa đáng kể |

Căn cứ quiz: 1, 5 → 4.1; 2 → 4.2; 3, 4, 8, 9 → 4.3 (+ 4.4); 6 → 4.4; 7 → 4.5; 10 → 4.6. `kiem_de_hieu.py 17` 0.

## Đọc thử độc lập (Phase 18, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: AR(1) 4, 2; MA(1) $r_1$ = 0,488; 1,96/√239 = 0,127;
AICc 437,2 − 431,8 = 5,4; sai phân mùa vụ $(1, 1, 1, 1)$; Ljung–Box $Q$ = 10,31, p = 0,0058; bậc tự do 21, ngưỡng 32,67; ± 3,92 / 7,84; ± 15;
quiz 6 ($Q$ = 14,76), 7 (± 5,88 / 29,4). Khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.3 Đọc bảng | "\"vệt\" do hai gai nhân vào nhau" | 4 | vì sao nhân hai gai sinh cột ở trễ 11, 13 không thấy | khó |
| 2 | Từ mới | "tổ hợp của $p$ giá trị trước" | 1 | "tổ hợp" dễ hiểu thành tổ hợp chập; buổi 15 dùng "tổng có trọng số" | nhỏ |
| 3 | 4.5 | công thức $\hat y_{T+h} \pm 1{,}96\,\sigma\sqrt h$ | 2 | không có danh sách ký hiệu (σ nói ở câu trên) | nhỏ |
| 4 | Lab bước 2 | "trừ $p + q + P + Q$" | 2 | $Q$ trùng tên thống kê Ljung–Box; công thức dùng $Q_m$ | nhỏ |
| 5 | Bài tập 2 | "Nhớ lại buổi 11" | 8 | không nói buổi 11 dạy gì | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **AR / MA qua ACF–PACF**: AR(1) φ = 0,6: ACF 0,6; 0,36; 0,22…, PACF chỉ trễ 1. MA(1) θ = 0,5: $r_1$ = 0,4, sau đó 0.
- **ARIMA**: $(50, 53, 55, 58)$ → sai phân $(3, 2, 3)$ quanh 2,7 → dừng.
- **SARIMA**: chuỗi $(5, 9, 6, 10, 7, 11)$, $m$ = 2 → sai phân mùa vụ $(1, 1, 1, 1)$.
- **Ljung–Box**: $n$ = 50, $r_1$ = 0,4 → $Q$ = 50 × 52 × 0,16 / 49 ≈ 8,5 > 3,84 → còn tự tương quan.
- **Khoảng √h**: σ = 1 → ± 1,96, bước 9 ± 5,88.
- **ARIMA vs ETS**: p = 0,74 → hoà; quên `season_length` thua baseline.

### C. Quiz mù

1 B · 2 B · 3 B · 4 B · 5 8 / 6,4; ACF trễ 2 0,64 · 6 $Q$ ≈ 14,8, 2 bậc tự do, còn tự tương quan · 7 ± 5,88 / ± 29,4 · 8 SARIMA(0,1,0)(0,1,1)12 ·
9 "ổn" giả (Ljung–Box ≈ 0); AICc khác $D$ không so được · 10 DM p 0,74: hoà. Căn cứ: 1, 5 → 4.1; 2 → 4.2; 3, 4, 8 → 4.3; 6 → 4.4; 7 → 4.5; 9
→ 4.2–4.4; 10 → 4.6. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 4. Sửa một điều: nói vì sao có cột ở trễ 11, 13.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10**, đáp án của ta đúng. Sửa: "vệt" viết lại thành "một gai nối các tháng liền nhau, gai kia nối cùng tháng năm trước, gộp lại
nối cả các tháng cách một năm cộng trừ một tháng"; "tổng có trọng số" trong bảng Từ mới; danh sách ký hiệu dưới công thức khoảng; $Q_m$ ở Lab
bước 2. Đọc lại mục 4.1–4.5: không vướng mới.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 18 đọc mù | 3.579 | 11 | 0 | 1 | 4 | 10/10 | 0 |
| sau sửa, đọc lại | 3.622 | 12 | **0** | **0** | 1 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 17` 0.
