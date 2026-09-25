# Nhật ký research — Buổi 28: Dự báo phân cấp và reconciliation

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-24
- **Người/phiên:** Phase 26 (soạn buổi 27–28)

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Hyndman & Athanasopoulos, *FPP3* §11.3 Forecast reconciliation https://otexts.com/fpp3/reconciliation.html | sách | 2026-09-24 | 4.3: $\tilde y = SG\hat y$; MinT $G = (S'W^{-1}S)^{-1}S'W^{-1}$; OLS, WLS (cấu trúc / phương sai), MinT(Shrink); không chệch khi $SGS = S$ |
| 2 | FPP3 §11.4 Forecasting Australian domestic tourism https://otexts.com/fpp3/tourism.html | sách | 2026-09-24 | đối chiếu: ở cấp tổng base (RMSE 1.721) thắng MinT (2.158), OLS 1.804, bottom-up 3.071 |
| 3 | FPP3 §11.5 Reconciled distributional forecasts https://otexts.com/fpp3/rec-prob.html | sách | 2026-09-24 | 4.4 |
| 4 | Wickramasuriya, S.L., Athanasopoulos, G. & Hyndman, R.J. (2019). Optimal forecast reconciliation for hierarchical and grouped time series through trace minimization. *JASA* 114(526), 804–819 | bài gốc | 2026-09-24 | 4.3 |
| 5 | Panagiotelis, A., Gamakumara, P., Athanasopoulos, G. & Hyndman, R.J. (2023). Probabilistic forecast reconciliation: properties, evaluation and score optimisation. *EJOR* 306(2), 693–706 | bài gốc | 2026-09-24 | 4.4: reconcile từng kịch bản (bootstrap) |
| 6 | Ben Taieb, S., Taylor, J.W. & Hyndman, R.J. (2017). Coherent probabilistic forecasts for hierarchical time series. *ICML* (PERMBU) | bài gốc | 2026-09-24 | 4.4 |
| 7 | Principato, G. et al. (2024). Conformal prediction for hierarchical data — cơ sở của `intervals_method="conformal"` trong hierarchicalforecast 1.5 | bài gốc | 2026-09-24 | 4.4 |
| 8 | Athanasopoulos, G., Hyndman, R.J., Kourentzes, N. & Petropoulos, F. (2017). Forecasting with temporal hierarchies. *EJOR* 262(1) | bài gốc | 2026-09-24 | hộp Nâng cao |
| 9 | hierarchicalforecast — PyPI 1.5.1 (4/3/2026); GitHub releases: 1.4.0 (diagnostics, EMinT), 1.5.0 (ConformalReconciliation), thẻ v1.5.2 (6/8/2026) chỉ có trên GitHub, chưa lên PyPI; kiểm chữ ký bằng `inspect` | thư viện | 2026-09-24 | 4.2–4.4 |
| 10 | Site disclaimer của Austrade (áp dụng cho tra.gov.au) https://www.austrade.gov.au/en/site-information/site-disclaimer | giấy phép | 2026-09-24 | "Unless otherwise noted, content on the Websites is licenced under a Creative Commons Attribution—4.0 International licence" |

## Phiên bản đã xác minh

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| hierarchicalforecast | 1.5.1 | `TopDown(method="forecast_proportions")` chỉ hỗ trợ khoảng kiểu bootstrap → buổi tách hai lượt reconcile |
| statsforecast | 2.1.1 → pandas 2.3.3 | AutoETS + SeasonalNaive |
| rdata | 1.1.0 | **thêm vào bảng chung**; đọc `tourism.rda` (cảnh báo "Missing constructor" vô hại) |

## Dữ liệu

| Bộ | Giấy phép | Ghi chú |
|---|---|---|
| `tourism-australia-tsibble` | gói tsibble GPL-3; **nguồn gốc TRA: CC BY 4.0** (xác minh 2026-09-24, đã ghi vào danh mục) | 24.320 dòng = 304 chuỗi đáy × 80 quý (1998Q1–2017Q4); cột Quarter là số ngày từ 1970-01-01 |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **MinT không thắng ở cấp trên trên dữ liệu này.** RMSE trung bình mỗi chuỗi, 3 mốc cắt (2013Q4, 2014Q4, 2015Q4), tầm 8 quý: quốc gia base
  2.071, bottom-up 2.983, top-down 2.071, OLS 2.101, MinT 2.572; bang 339 / 416 / 314 / 318 / 369; khu vực 52,8 / 54,9 / 47,4 / 48,8 / 50,8; đáy
  19,3 / 19,3 / 18,2 / 18,6 / 18,5. Thử 5 mốc cắt và WLS cấu trúc / phương sai: cùng kết luận. **Nguyên nhân đo được:** đợt tăng du lịch
  2016–2017 → mọi dự báo thấp hơn thực tế; sai số có dấu cấp quốc gia base +1.745, bottom-up +2.847, MinT +2.391. MinT tối ưu khi base không
  chệch; ở đây nó dồn trọng số về các chuỗi đáy vốn chệch nặng hơn. Khớp FPP3 §11.4.
- **Seasonal naive tự khớp** (lệch cộng 3·10⁻¹¹): tổng các "cùng quý năm trước" chính là "cùng quý năm trước" của tổng. AutoETS base lệch
  cộng 1.613 nghìn chuyến.
- **Khoảng trong mẫu phủ thiếu nặng ở cấp trên:** khoảng 90% giả định chuẩn: base 58,3% (quốc gia) → 82,8% (đáy); MinT 4,2% → 82,7%;
  bottom-up 0% ở cấp quốc gia. `conformal` của thư viện với `Y_df` = giá trị khớp trong mẫu: vẫn 58% (tài liệu thư viện tự cảnh báo).
- **Hiệu chỉnh ngoài mẫu:** backtest mỗi quý (29 mốc 2009Q4–2016Q4, tầm 4 quý), mỗi mốc chấm c lấy mọi vector sai số (389 chuỗi) của các
  mốc đã có đủ thực tế, cộng vào base, chiếu lên không gian khớp (OLS / MinT), khoảng = hạng conformal: 90% → quốc gia 79,4%, bang 80,9% (OLS),
  khu vực 83,6%, đáy 82,1%; chỉ 8 vector sai số / mốc (bản đầu) cho 66–69%. 80 quý quá ngắn để hiệu chỉnh tốt hơn — ghi là giới hạn.
- **Phân cấp theo thời gian làm dự báo quý tệ hơn** (8/9 chuỗi quốc gia + bang, cả OLS và WLS cấu trúc): ETS theo năm chỉ có 18 điểm và
  đoán kém nhất; quốc gia 2016: MAE quý 656 → 921 sau hoà giải OLS.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| "Xong khi: MinT thắng base ≥ 3/4 cấp; coverage cấp trên = danh nghĩa ± 5%" | **lớn** | Báo người dùng 2026-09-24; **người dùng chọn "dạy trung thực"**: giữ du lịch Úc, bài giải thích bằng sai số có dấu, coverage đo từng cấp trước/sau hiệu chỉnh; sửa lo-trinh + định nghĩa cột mốc M4 |
| "Temporal hierarchy" thành khái niệm riêng | nhỏ | Hộp Nâng cao kèm số thật (hoà giải làm tệ đi khi cấp gộp đoán kém) |
| "Middle-out", "PERMBU" | nhỏ | Định nghĩa một câu; PERMBU đo được (hoà giải OLS, khoảng 90% cấp quốc gia phủ 20,8%) nhưng không đưa vào bảng chính |
| Dự phòng Online Retail II | nhỏ | Không cần: giấy phép gốc đã xác minh |

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0; ~2 phút)

| Mục | Số |
|---|---|
| Cây | S 389 × 304; 1 + 8 + 76 + 304 chuỗi; 80 quý |
| Ví dụ tay OLS | tổng 10, A 4, B 5 → 9,667 / 4,333 / 5,333; bottom-up 9 / 4 / 5 |
| OLS tự viết − thư viện | 3,3·10⁻¹¹ |
| Sai số có dấu (thực tế − dự báo) | quốc gia: base 1.745, SN 1.961, BU 2.847, TD 1.745, OLS 1.791, MinT 2.391; bang 255 / 245 / 356 / 218 / 224 / 299; khu vực 34,1 / 25,8 / 37,5 / 23,0 / 23,6 / 31,5; đáy 9,4 / 6,5 / 9,4 / 5,7 / 5,9 / 7,9 |
| RMSE seasonal naive | quốc gia 2.191; bang 336,8; khu vực 54,7; đáy 21,5 |
| Coverage 80% (trong mẫu) | base 54,2 / 55,7 / 65,7 / 73,8%; OLS 45,8 / 77,1 / 79,7 / 84,4%; MinT 4,2 / 25,5 / 56,4 / 73,4% |
| Coverage 90% (trong mẫu) | OLS 54,2 / 84,4 / 88,0 / 91,0% |
| Ngoài mẫu (17 mốc 2012Q4–2016Q4, 68 điểm cấp quốc gia) | 90%: base 79,4 / 79,2 / 83,0 / 84,8%; OLS 79,4 / 80,9 / 83,6 / 82,1%; MinT 79,4 / 72,4 / 79,0 / 79,0%. 80%: base 75,0 / 66,4 / 72,9 / 74,4%; OLS 76,5 / 69,7 / 72,5 / 71,3%; MinT 66,2 / 60,3 / 66,8 / 67,1%. Sai số có dấu quốc gia (ngoài mẫu) +1.113 |
| Phân cấp thời gian (quốc gia) | 2016: thật 101.485, ETS năm 97.448, tổng 4 quý 99.221, khớp 97.803; MAE quý 656 → 921. 2017: 107.710 / 101.484 / 103.302 / 101.848; 1.102 → 1.466 |
| Thời gian | backtest 3 mốc 13 s; sai số ngoài mẫu 29 mốc ~55 s; `check --dap-an` 42 s; notebook 1 phút 39 |

## Đọc thử (2026-09-24, Phase 26, tự đọc — không subagent)

**Vòng 1 (đọc toàn bộ `tai-lieu.md`, vai học viên mới).** Tính lại bằng NumPy: OLS (10, 4, 5) → 9,667 / 4,333 / 5,333; MinT với phương sai (4, 1, 1) →
9,333 / 4,167 / 5,167; OLS (30, 8, 12, 9) → 29,75 / 8,25 / 12,25 / 9,25; top-down 30 × 8/29 = 8,276; quiz 5–6: 22,22 / 27,78 và 48,33 / 21,67 / 26,67.
Trước vòng đọc đã bắt hai lỗi viết: đáp án tự kiểm tra 4.3 đưa gợi ý sai (đỉnh dịch k/(k + 1)) rồi tự sửa giữa chừng → viết lại (OLS chia đều cho k + 1
chuỗi); kết luận hình RMSE bỏ sót MinT cũng vượt 1 ở cấp bang.

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.3 Đọc bảng | "MinT tin các chuỗi đáy vì phần dư quá khứ của chúng nhỏ" | 4 | ngược cơ chế của ví dụ tay: MinT sửa nhiều nhất chuỗi có phần dư lớn nhất (cả nước) | khó |
| 2 | 4.3 | "chỉ số không đơn vị như MASE" | 8 | MASE không nhắc lại | nhỏ |
| 3 | 4.3 công thức | "nghịch đảo ma trận", "đảo hàng thành cột" | 1 | ma trận ngoài toán phổ thông; ý chính đã có trong "Nói bằng lời" và ví dụ tay | nhỏ |

Sửa #1 (viết lại theo cơ chế đúng), #2 (thêm định nghĩa trong ngoặc). Giữ #3.

**B — giải thích lại (ví dụ mới):** cả nước 20, A 7, B 10 → lệch 3; bottom-up 17; top-down A = 20 × 7/17 ≈ 8,24; OLS mỗi chuỗi dịch 1 → 19 / 8 / 11;
hai bang sai số (1, −1) và (−1, 1) → tổng 0 dù mỗi bang cận trên 1. Không khái niệm nào "không giải thích được".

**C — quiz:** 1, 7 → 4.1; 2, 5 → 4.2; 3, 6 → 4.3; 4, 8 → 4.4; 9 → 4.3 (sai số có dấu); 10 → 4.4 + cột mốc M4.

**Rà gọn:** không đoạn ≥ 30 chữ lặp ý. Tài liệu ở sát sàn độ dài (3.544 chữ): bản đầu 3.104 chữ; phần thêm là năm ý lộ trình còn thiếu (nhóm chéo, hai loại
tỷ lệ top-down, điều kiện không chệch, bốn cách lấy khoảng của thư viện, chấm theo cấp), không phải chữ độn.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| 1 | 3.523 | 11 | 0 | 1 | 2 | 10/10 | 0 |
| sau sửa | 3.544 | 11 | **0** | **0** | 1 | 10/10 | 0 |

Vòng 2 đọc lại các đoạn đã sửa trong ngữ cảnh (4.3); phần còn lại không đổi so với vòng 1. `kiem_de_hieu.py 28`: 0 vi phạm.

## Đọc thử độc lập (Phase 27, 2026-09-25)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại bằng NumPy: OLS (10, 4, 5) → 9,667 / 4,333 / 5,333; MinT với
W = diag(4, 1, 1) → 9,333 / 4,167 / 5,167 (đúng bằng chia lệch 1 theo tỷ lệ 4 : 1 : 1); OLS cây một đỉnh (30, 8, 12, 9) → 29,75 / 8,25 / 12,25 / 9,25;
top-down 4,44 / 5,56 và 8,28; mọi câu "thắng/thua" của bảng RMSE; hình RMSE tương đối (bottom-up khu vực 1,04); "thiếu 6–11 điểm" (6,4–10,6);
coverage cấp quốc gia 14/24 = 58,3%, 1/24 = 4,2%, 54/68 = 79,4%.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.3 ví dụ tay | "MinT với phương sai sai số (4, 1, 1) … kết quả (9,33; 4,17; 5,17)" | 4 | ghi "tự tính tay" nhưng chỉ đưa kết quả; người chưa học ma trận nghịch đảo không tự ra được | khó |
| 2 | 4.3 "Khi nào hoà giải không làm hỏng" | "Nếu dự báo base không chệch" | 1 | "chệch" chưa định nghĩa; là mắt xích chính của "vì sao MinT thua" | khó |
| 3 | 4.4 bảng coverage + "Vì sao vẫn thiếu" | "So dòng một với dòng ba"; "+1.113 nghìn chuyến" | 4 | hai dòng trong mẫu chấm trên 3 mốc × 8 quý, hai dòng ngoài mẫu trên 17 mốc × 4 quý (NGHIEN-CUU mục số liệu) — tài liệu không nói; +1.113 khác +1.745 ở bảng 4.3 mà không rõ vì sao | khó |
| 4 | 4.3 | "phương sai sai số" | 1 | mục 2 chỉ nhắc hiệp phương sai | nhỏ |
| 5 | 4.3 ký hiệu | "co nó một phần về đường chéo" | 1 | "đường chéo" của ma trận chưa giải thích | nhỏ |
| 6 | 4.3 | $S^\top$, $^{-1}$, $SGS = S$ | 2 | ngoài toán phổ thông; đọc được như hộp đen nhờ "Nói bằng lời" | nhỏ |
| 7 | Nâng cao 4.4 | $I_4$ | 2 | ma trận đơn vị chưa nói | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Ma trận S / lệch cộng**: cả nước = A + B + C, base (20, 5, 6, 7) → tổng đáy 18, lệch 2.
- **Bottom-up / top-down**: base (20, 5, 6, 7) → BU 18; TD A = 20 × 5/18 ≈ 5,56.
- **OLS**: lệch 2, bốn chuỗi → mỗi chuỗi dịch 0,5: (19,5; 5,5; 6,5; 7,5).
- **MinT**: (cả nước, A, B) = (12, 5, 5), phương sai (1, 1, 2) → lệch 2 chia 1 : 1 : 2 → 11,5 / 5,5 / 6,0; chuỗi B kém nhất bị sửa nhiều nhất.
- **Chệch làm MinT hỏng**: cấp đáy luôn đoán thấp 10%, cấp tổng không chệch → MinT kéo cấp tổng xuống theo cấp đáy.
- **Khoảng khớp**: A (−1, 1), B (−1, 1) cùng chiều → cận tổng 2 = 1 + 1; ngược chiều → 0.

### C. Quiz mù

1 B · 2 A · 3 A · 4 A · 5 lệch 5, BU 45, TD A ≈ 22,22 · 6 48,33 / 21,67 / 26,67 · 7 6 × 3, X = (1, 1, 0) · 8 6 = 3 + 3; 0 < 6 · 9 thua ở quốc gia và bang, kiểm
sai số có dấu · 10 quốc gia 4,2%; 82,7% vẫn thiếu, phần dư trong mẫu. Căn cứ: 1, 7 → 4.1; 2, 5 → 4.2; 3, 6, 9 → 4.3; 4, 8, 10 → 4.4. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 3 / nhỏ 4. Sửa một điều: nói rõ bảng coverage gộp hai thiết kế chấm.

### E. Dài/lặp

Lab bước 4–5 chỉ trỏ về bảng mục 4.3–4.4 (gọn). Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10**; đáp án đúng hết. Sửa: #1 ví dụ MinT viết thành phép tính tay "chia phần lệch 1 theo tỷ lệ 4 : 1 : 1" (khớp NumPy với W =
diag(4, 1, 1)); #2 "không chệch (sai số có dấu trung bình bằng 0)"; #3 câu dẫn bảng coverage nói hai dòng trong mẫu chấm trên 3 mốc × 8 quý, hai dòng
ngoài mẫu trên 17 mốc 2012Q4–2016Q4 × 4 quý; "Đọc bảng" ghi "chỉ so gần đúng"; "+1.113" ghi rõ là base cấp quốc gia trên 17 mốc đó (khớp
`dap-an/ve_hinh.py`); #4 "phương sai sai số (trung bình bình phương sai số)"; #5 "shrink giảm bớt phần hiệp phương sai" thay "co về đường chéo"
(thư viện tự ước lượng mức co, không phải một nửa như `G_mint`). Giữ #6, #7. Còn mở: chấm lại dòng trong mẫu trên cùng 17 mốc thì so sạch hơn —
chưa làm vì phải đổi `dap-an/` và `cham/`.

| Vòng | Chữ | Trang | Chặn / khó / nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|
| Phase 27 đọc mù | 3.544 | 11 | 0 / 3 / 4 | 10/10 | 0 |
| sau sửa, đọc lại | 3.620 | 11 | **0 / 0 / 2** | 10/10 | 0 |

`kiem_de_hieu.py 28`: 0 vi phạm. Thêm chữ để vá mắt xích (định nghĩa, câu dẫn); lượt rà gọn sau sửa không thấy đoạn ≥ 30 chữ bớt được.
