# Nhật ký research — Buổi 15: Backtesting đúng cách

- **Ngày research:** 2026-09-19 (Phase 16). Buổi soạn mới hoàn toàn (bản nháp chỉ có khuôn): code, đáp án, bộ chấm, hình, notebook, tài liệu.
- **Người/phiên:** Phase 16, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | FPP3 §5.10 *Time series cross-validation*: https://otexts.com/fpp3/tscv.html — rolling forecasting origin, `stretch_tsibble(.init, .step)`; ví dụ Google: RMSE CV 11,27 so với phần dư 11,15 | sách giáo khoa | 2026-09-19 | 4.2 |
| 2 | Bergmeir & Benítez (2012), *On the use of cross-validation for time series predictor evaluation*, Information Sciences 191, 192–213 | bài gốc | 2026-09-19 | 4.1 (blocked CV, rolling origin) |
| 3 | Bergmeir, Hyndman & Koo (2018), *A note on the validity of cross-validation for evaluating autoregressive time series prediction*, CSDA 120, 70–83; bản nháp https://robjhyndman.com/papers/cv-wp.pdf (đọc toàn văn) | bài gốc | 2026-09-19 | 4.1: K-fold hợp lệ cho mô hình tự hồi quy thuần có phần dư không tự tương quan |
| 4 | Diebold & Mariano (1995), JBES 13(3); Harvey, Leybourne & Newbold (1997), IJF 13, 281–291 | bài gốc | 2026-09-17 (Phụ lục D) | 4.5 |
| 5 | Diebold (2015), *Comparing predictive accuracy, twenty years later*, JBES 33(1), 1–9 — DM để so **dự báo**, không để so mô hình | bài phản biện | 2026-09-19 | 4.5 "Khi nào dùng" |
| 6 | StatsForecast `cross_validation(h, df, n_windows=1, step_size=1, test_size=None, input_size=None, level=None, fitted=False, refit=True, …)`: https://nixtlaverse.nixtla.io/statsforecast/src/core/core.html — **không có tham số gap**; `input_size` = sliding window; `refit` True/False/số nguyên | tài liệu chính thức | 2026-09-19 | 4.2, đối chiếu |
| 7 | Hewamalage, Ackermann & Bergmeir (2023), DMKD; arXiv:2203.10716 | tổng quan | 2026-09-19 | "Lỗi thường gặp" (chia ngẫu nhiên, tune trên tập kiểm) |
| 8 | Tashman (2000), *Out-of-sample tests of forecasting accuracy*, IJF 16 | tổng quan kinh điển | (trích qua [1], [7]) | thuật ngữ rolling origin |

## Phiên bản đã xác minh

| Thư viện | Phiên bản | Nguồn |
|---|---|---|
| statsforecast | 2.1.1 (bảng chung; bản mới nhất trên PyPI hỗ trợ Python 3.10–3.14) | PyPI JSON 2026-09-19, `tools/nen/phien-ban.toml` |
| utilsforecast | 0.2.16 | PyPI 2026-09-19 |
| scikit-learn | 1.9.1 | bảng chung |

`statsforecast.cross_validation` và `backtest` tự viết cho **cùng cutoff và cùng seasonal naive** trên 245 chuỗi M4 theo giờ dài 1.008
(chênh tuyệt đối lớn nhất 0,0) — test `test_khop_statsforecast`.

## Dữ liệu

EIA-930 BALANCE 2024 (public domain), vùng ERCOT, 8.784 giờ; M4 Hourly (Monash, CC BY 4.0), 414 chuỗi dài 748–1.008. Cả ba tệp trong
danh mục, sha256 chốt. Lộ trình ghi đúng hai bộ này.

## Số liệu thật của buổi (`dap-an/ve_hinh.py`, seed 0 cho rừng ngẫu nhiên và K-fold)

| Đại lượng | Giá trị |
|---|---|
| Rừng ngẫu nhiên, MAE: K-fold xáo trộn / rolling origin (28 cửa sổ 24 giờ, 3–30/9) / hold-out 1/10–31/12 | 1.639 / 1.944 / 2.129 MW (−23,0% / −8,7%) |
| Hồi quy tuyến tính, cùng thứ tự | 2.284 / 2.186 / 2.588 MW (−11,8% / −15,5%) |
| Seasonal naive 24 giờ trên hold-out | 1.944 MW (trùng ngẫu nhiên với rừng rolling 1.944,39 so với 1.944,43) |
| Rừng so với seasonal naive trên 28 cửa sổ | 1.944 / 2.049 MW; DM-HLN h = 24: thống kê −0,75, p = 0,45 |
| MAE từng cửa sổ của rừng | 583 → 4.328 MW, trung vị 1.802 |
| 'Trộn' w × hôm qua + (1 − w) × tuần trước | w tune trên hold-out = 0,8 → MAE 1.861 (−4,3%); tune trên 3 tháng trước mốc → w = 1,0 (= seasonal naive) |
| DM trên hold-out, 'trộn' 0,8 so với seasonal naive, sai số tuyệt đối | bỏ tự tương quan: −4,86, p = 1,2·10⁻⁶; HLN h = 24: −1,41, p = 0,16 |
| ACF của chênh lệch từng giờ | 0,91 (trễ 1), 0,15 (trễ 12), −0,07 (trễ 24); 'trộn' thắng 53/92 ngày |
| M4 theo giờ, chọn trong 6 phương pháp | cùng đoạn: MASE trung vị 0,775; ba tập (tune T, chọn A, báo cáo B): lúc chọn 0,870, báo cáo 1,039; seasonal naive 24 trên B 1,127 |
| MASE seasonal naive theo bước h (245 chuỗi, 3 cửa sổ 48 giờ) | bước 1: 0,7; bước 24: 0,8; bước 25: 1,3; bước 48: 1,4 |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **K-fold không luôn sai** (Bergmeir, Hyndman & Koo 2018): với mô hình chỉ dùng lag và phần dư không tự tương quan, K-fold ước lượng tốt.
  Đo được đúng tinh thần đó: với hồi quy tuyến tính, K-fold (−11,8%) không lạc quan hơn rolling origin (−15,5%); với rừng ngẫu nhiên — học
  thuộc hàng xóm trong thời gian (feature `ngay_trong_nam`, `gio`) — K-fold lạc quan 23%. Tài liệu dạy thẳng điều này, không nói "K-fold
  luôn sai".
- Rolling origin không đoán được tương lai đổi chế độ: cả hai mô hình lệch 9–16% vì 4 tuần cuối tháng 9 khác quý 4. Số cửa sổ và đoạn
  chúng phủ quyết định ước lượng (thử: 13 cửa sổ cách nhau 168 giờ cho rừng 3.193 MW, +50%, vì cùng một thứ trong tuần). Ghi vào "Lỗi thường
  gặp".
- DM với h > 1: chênh lệch mất mát tự tương quan (ACF 0,91 ở trễ 1) → bỏ qua thì p nhỏ giả tạo (10⁻⁶ so với 0,16).
- Tune trên hold-out: chính con số "hơn 4,3%" của mô hình 'trộn' chỉ có khi w chọn trên hold-out; chọn đúng cách thì w = 1.
- statsforecast `cross_validation` không có `gap`: dữ liệu về trễ thì tự viết (bộ backtest của buổi có `gap`).

## Research viết lại (sư phạm)

- Chia ngẫu nhiên: ví dụ đời thường "đề thi lộ" — trả lời câu hỏi giờ 10 khi đã biết giờ 9 và giờ 11. Hình sơ đồ ba cách chia (FPP §5.10
  dùng đúng dạng chấm xanh/đỏ).
- Rolling origin: "đứng ở từng thời điểm trong quá khứ, giả vờ không biết tương lai, dự báo, rồi mở đáp án".
- Ba tập: tương tự "đề luyện, đề thi thử, đề thi thật" — đề thi thật chỉ mở một lần.
- DM: "chênh trung bình có lớn hơn mức dao động ngẫu nhiên không"; tự tương quan = "92 ngày chứ không phải 2.215 lần bốc thăm độc lập".

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình: xây `backtest` "trên statsforecast.cross_validation" | nhỏ | tự viết bằng pandas (cùng giao diện `tv.backtest` cả khoá dùng) + test khớp statsforecast; statsforecast không có gap |
| Lộ trình: Wilcoxon, Nemenyi/critical difference | nhỏ | không đưa vào lý thuyết (D9: đã đủ 5 khái niệm); một câu ở "Đọc thêm" |
| Lộ trình "Xong khi: backtest chênh hold-out < 10%" | nhỏ | đạt với rừng ngẫu nhiên (−8,7%); hồi quy tuyến tính −15,5% — tài liệu báo thật và giải thích (đổi mùa) |
| Chỗ hở thứ ba (DM bỏ tự tương quan) ngoài bảng `quy-uoc.md` | nhỏ | thêm vào bảng buổi 15 |

## Đọc thử (Phase 16, 2026-09-19)

Tự đọc (không subagent), checklist `tools/CHUAN-DE-HIEU.md`. Tính lại: ví dụ chia ngẫu nhiên (0 so với MAE 3); cutoff ví dụ 10 mốc (3, 5, 7;
gap 1 → 2, 4, 6); tự kiểm tra 23 / 19 / 15, dự báo 26–29; DM tay $\bar d$ −4,6, phương sai 118,64, $S_1$ −0,944, $S_1^*$ −0,845, p 0,446 (khớp
test); hệ số hiệu chỉnh 0,949 và 0,748. Quiz: câu 5 (44, 39, 34, 29), câu 7 ($S_1^*$ 1,095, p 0,353 — kiểm bằng `tools/khung/backtest.py`).
Mô tả hình kiểm với số in ra: MASE theo bước h của seasonal naive 0,7 (bước 1) → 1,4 (bước 48) có nhịp trong ngày, nên bỏ câu "quanh
0,7–0,8" ở bản đầu; ACF của $d_t$ vượt ±1,96/√n tới khoảng trễ 18 (không phải 24 như bản đầu).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 3.990 | 12 | 0 | 0 | 4 | 10/10 có căn cứ | nhỏ: "cây quyết định" chưa định nghĩa; "phần dư" dùng ở 4.1 mà Nhắc lại chưa có; `cua_so_train` = 90 ngày lẫn đơn vị giờ; một dòng thừa khoảng trắng đầu dòng |
| 2 | sau sửa | 12 | **0** | **0** | 0 | 10/10 | |
| rà gọn | biên tập viên | — | — | — | — | — | 1 chỗ: "Đọc bảng" ở 4.2 nói lại kết luận của hình → dời lên ngay dưới bảng, rút kết luận hình; bảng 4.2 bỏ cột K-fold đã có ở 4.1 |

Căn cứ quiz: 1, 9 → 4.1; 2, 3, 5 → 4.2; 6 → 4.3; 4, 8 → 4.4; 7, 10 → 4.4 + 4.5. `kiem_de_hieu.py 15` 0.

## Đọc thử độc lập (Phase 18, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: ví dụ chia ngẫu nhiên 14 / hold-out MAE 3;
−23,0% / −11,8%; cutoff 7, 5, 3 và 23, 19, 15; −8,7% / −15,5%; 4.328 / 583 = 7,4; 1,039 → 0,775 = 25,4%; DM $\bar d$ −4,6, phương sai 118,64,
sai số chuẩn 4,87, $S_1$ −0,944, $S_1^*$ −0,845, p 0,446 (scipy); hệ số 0,949 / 0,748; quiz 5–7 (p câu 7 ≈ 0,35). Khớp hết. Số 1.944 xuất hiện
hai lần (rừng trên backtest, seasonal naive trên hold-out): kiểm mục "Số liệu thật" — trùng tình cờ (1.944,39 / 1.944,43).

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.5 ví dụ | "Sai số chuẩn của $\bar d$: $\sqrt{118{,}64 / 5}$" | 4, 8 | sai số chuẩn (buổi 8) không nhắc lại; vì sao chia $n$ rồi căn không thấy | khó |
| 2 | 4.2 hình | "hai cách hứa thấp hơn thật một khoảng như nhau" | 5 | bảng cho −11,8% và −15,5%: không "như nhau" | nhỏ |
| 3 | 4.5 bảng 2 | "hold-out … 1.944 MW" | 5 | trùng số với ô trên, tưởng chép nhầm | nhỏ |
| 4 | 4.3 | "cách nhau gấp bốn lần" | 5 | 9 / 2 = 4,5 | nhỏ |
| 5 | 4.1 | "chuỗi đổi chế độ" | 1 | "chế độ" chưa định nghĩa; đoán được | nhỏ |
| 6 | Lab bước 4 | "(lúc chọn 0,870)" | 5 | 0,870 không có trong hình mục 4.4 | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Không chia ngẫu nhiên**: $(1, 3, 5, 7)$, giấu 5 → hàng xóm (3 + 7) / 2 = 5, sai 0; hold-out điểm cuối đoán 5, sai 2.
- **Rolling origin**: 20 mốc, $h$ = 3, 3 cửa sổ, `buoc` 3, gap 1 → cutoff 15, 12, 9.
- **Sai số theo cửa sổ**: MAE $(1, 1, 7)$: một hold-out có thể báo 1 hoặc 7.
- **Ba tập**: chọn trên A được mô hình may nhất; báo trên B chưa dùng.
- **DM**: $d = (1, -1, 3, 1)$, $\bar d$ = 1, phương sai 2, sai số chuẩn 0,71, $S_1$ = 1,41 — 4 điểm chưa đủ.

### C. Quiz mù

1 B · 2 B · 3 B · 4 C · 5 29, 34, 39, 44; học 0 → 29, dự báo 30 → 34 · 6 7 / 4,5; báo 4, 5 hoặc 15; báo phân bố · 7 1 / 0,79 / 1,26 / 1,10 ·
8 X, báo 14 · 9 xáo trộn, thật ≈ 2.129 (−24%), rolling origin · 10 tune trên hold-out; DM $h$ = 1 bỏ tự tương quan (HLN p 0,16). Căn cứ: 1, 9 →
4.1; 2, 3, 5 → 4.2; 6 → 4.3; 4, 8 → 4.4; 7, 10 → 4.4 + 4.5. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 5. Sửa một điều: nhắc lại sai số chuẩn ở mục 2 (DM dựa trên nó).

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10**, đáp án của ta đúng. Sửa: mục 2 thêm "sai số chuẩn = $\sqrt{\text{phương sai}/n}$ khi các số độc lập" (nối thẳng sang câu
"2.215 giờ không phải 2.215 lần bốc thăm độc lập" ở 4.5); hình 4.2 "cả hai cách đều hứa thấp hơn thật 12–16%"; "hơn bốn lần"; ghi chú số
1.944 trùng tình cờ. Đọc lại mục 2, 4.2, 4.3, 4.5: không vướng mới.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 18 đọc mù | 4.013 | 12 | 0 | 1 | 5 | 10/10 | 0 |
| sau sửa, đọc lại | 4.052 | 12 | **0** | **0** | 2 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 15` 0.
