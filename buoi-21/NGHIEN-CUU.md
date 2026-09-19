# Nhật ký research — Buổi 21: Chuỗi tài chính và biến động

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-19 (Phase 20). Buổi soạn mới hoàn toàn (thư mục tạo từ khuôn). Cuối buổi: **cột mốc M2**.
- **Người/phiên:** Phase 20, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | PyPI `arch`: 8.0.0 (21/10/2025) là bản mới nhất; `arch_model(mean, vol="GARCH", p, o, q, dist)`, `fit(last_obs=…)`, `forecast(start=…, reindex=False)`: https://pypi.org/project/arch/ | tài liệu chính thức | 2026-09-19 | 4.4–4.6, code |
| 2 | Corsi (2009), "A simple approximate long-memory model of realized volatility", *J. Financial Econometrics* 7(2): 174–196 — HAR: RV mai theo RV ngày, tuần, tháng; hồi quy thường, thường thắng GARCH: https://statmath.wu.ac.at/~hauser/LVs/FinEtricsQF/References/Corsi2009JFinEtrics_LMmodelRealizedVola.pdf | bài gốc | 2026-09-19 | 4.5 |
| 3 | Patton (2011), "Volatility forecast comparison using imperfect volatility proxies", *J. Econometrics* — chỉ MSE và QLIKE xếp hạng đúng khi dùng số đo xấp xỉ của biến động: https://public.econ.duke.edu/~ap172/Patton_vol_proxies_JoE_2011.pdf | bài gốc | 2026-09-19 | 4.4–4.5 |
| 4 | Kupiec (1995), "Techniques for verifying the accuracy of risk measurement models", *J. Derivatives* 3 — kiểm định tỷ lệ vượt VaR (LR ~ χ² 1 bậc tự do) | bài gốc (công thức chuẩn) | 2026-09-19 | 4.6, test |
| 5 | statsmodels 0.15.0 `MarkovRegression(k_regimes=2, switching_variance=True)`; Hamilton (1989) | tài liệu | 2026-09-19 | "Nâng cao" 4.6 |
| 6 | Phản biện "deep learning đoán giá": *Humanities and Social Sciences Communications* (2025), "Stock market trend prediction using deep neural network via chart analysis: a practical method or a myth?" — nhiều nghiên cứu LSTM/DNN cho kết quả dương giả vì bỏ qua ngữ cảnh thời gian; LSTM có thể thua cả cách ngây thơ nhất: https://www.nature.com/articles/s41599-025-04761-8 | phản biện | 2026-09-19 | 4.3 |
| 7 | Cont (2001), "Empirical properties of asset returns: stylized facts and statistical issues", *Quantitative Finance* 1 | tổng quan kinh điển | 2026-09-19 | 4.2 |
| 8 | Binance public data repo (MIT cho mã; dữ liệu là "Binance's public market data", không giấy phép dữ liệu; tệp .CHECKSUM kèm mỗi zip; từ 1/1/2025 timestamp spot tính bằng micro giây): https://github.com/binance/binance-public-data | điều khoản, định dạng | 2026-09-19 | dữ liệu |

## Phiên bản đã xác minh

arch **8.0.0** (thêm vào `tools/nen/phien-ban.toml`), statsmodels 0.15.0, scikit-learn 1.9.1, scipy 1.18.1, pandas 2.3.3 — theo `uv.lock` của buổi.

## Dữ liệu

| Bộ | Giấy phép | Ghi chú |
|---|---|---|
| `binance-btcusdt-1h-2023-01` … `2024-12` (24 bộ, thêm vào danh mục 2026-09-19) | không giấy phép dữ liệu; không mirror, học viên tự tải | sha256 từng zip khớp tệp `.CHECKSUM` của Binance; 17.543 giờ, thiếu 1 giờ; timestamp mili giây (trước 2025) |
| `frb-h10-ty-gia` (đã có) | public domain | cột `RXI_N.B.JA` = số yên cho 1 USD; 6.268 ngày 2000–2024 |

## Số liệu thật (`dap-an/ve_hinh.py`)

| Đại lượng | Giá trị |
|---|---|
| Sự thật cách điệu, lợi suất ngày (%) | BTC 2023–24 (730 ngày): độ lệch chuẩn 2,53; độ nhọn dư 2,33; ACF1 lợi suất −0,025; ACF1 bình phương 0,113; \|z\| > 4: 0,14% (chuẩn: 0,006%). JPY 2000–24 (6.267 ngày): 0,62; 4,35; −0,015; 0,094; 0,51% |
| ACF JPY trễ 1–5 | lợi suất −0,015 / −0,019 / 0,005 / 0,004 / −0,014; bình phương 0,094 / 0,122 / 0,069 / 0,031 / 0,084 |
| Demo (code đầu buổi): MLP, chuẩn hoá theo toàn chuỗi, chia ngẫu nhiên 80/20 | R² 0,988; nhưng naive R² 0,996; MAE MLP 1.649 USD, naive 887 |
| Chấm trung thực: học 2023, chấm 366 ngày 2024, mỗi cửa sổ chia cho giá cuối của nó | R² MLP 0,978, naive 0,984; MAE 1.662 / 1.318; DM p 5·10⁻¹⁰ (naive tốt hơn); đoán đúng chiều 52,5%; tương quan (dự báo − naive) với (thật − naive) 0,009 |
| VaR 99% JPY, học 2000–2019, chấm 2020–2024 (1.249 ngày, kỳ vọng 12,5 lần vượt) | chuẩn cố định 25 lần, Kupiec p 0,0017; GARCH chuẩn 23, p 0,0075; **GARCH-t 14, p 0,67**; GJR-t 14, p 0,67 |
| GARCH-t JPY (2000–2019) | α 0,036, β 0,958, ν 5,8 |
| BTC 2024: dự báo phương sai ngày so với biến động thực hiện (tổng bình phương lợi suất giờ) | QLIKE: HAR 0,389; GJR-t 0,439; EWMA 0,441; GARCH-t 0,477; cố định 0,530; RV hôm qua 0,765. MSE: HAR 72,4; EWMA 78,5; cố định 83,8; RV hôm qua 111,4; GJR-t 190,4; GARCH-t 195,0 |
| RV trung bình 2024 và phương sai lợi suất ngày 2024 | 7,58 và 7,60 (%²) — RV đo đúng cùng đại lượng |
| Markov 2 trạng thái JPY | phương sai 0,169 và 0,720; xác suất bất ổn TB năm: 2008 0,81; 2009 0,83; 2019 0,05; 2021 0,03; 2022 0,62; 38,5% số ngày ở trạng thái bất ổn |
| Thời gian | toàn bộ `ve_hinh.py` ~4 s |

## Phát hiện mới / lỗi hiểu sai phổ biến

- R² trên **giá** gần 1 với bất kỳ dự báo nào gần giá hôm qua (naive 0,996) — R² không phân biệt được. Chấm trên lợi suất hoặc so với naive.
- Chia ngẫu nhiên + chuẩn hoá toàn chuỗi (hai lỗi rò rỉ của buổi 13, 15) vẫn không làm MLP thắng naive ở đây: demo "99%" thua naive **ngay
  trên phần kiểm của chính nó** (MAE 1.649 so với 887). Người làm demo thường không in dòng naive.
- MSE xếp GARCH **sau** biến động cố định trên BTC 2024 (195 so với 84) trong khi QLIKE xếp ngược lại: MSE bị vài ngày cực lớn chi phối.
  Patton (2011): cả hai xếp hạng nhất quán theo kỳ vọng, nhưng trên mẫu hữu hạn QLIKE ổn định hơn. Báo cả hai, nói rõ.
- GJR (đòn bẩy) không đổi gì trên JPY (γ 0,004): hiệu ứng đòn bẩy là của cổ phiếu, không phải tỷ giá; trên BTC GJR cải thiện QLIKE (0,477 → 0,439).
- JPY là tỷ giá (không có cổ phiếu mở phù hợp); lộ trình cổ phiếu → thay bằng BTC + JPY.

## Research viết lại (sư phạm)

- Lợi suất thay giá: "giá hôm nay ≈ giá hôm qua" nên mọi mô hình trông giỏi trên giá.
- Cụm biến động: "ngày sóng lớn thường theo sau ngày sóng lớn, dù không biết sóng lên hay xuống".
- GARCH: "phương sai ngày mai = mức nền + một phần cú sốc hôm nay + phần lớn phương sai hôm nay".
- VaR: "mức lỗ mà 99 trên 100 ngày không tệ hơn"; Kupiec: "đếm số ngày vượt, có khớp 1% không".

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Demo "LSTM" | nhỏ | dùng MLP của scikit-learn (không cần torch, chạy CPU vài giây); hiện tượng giống hệt (phản biện số 6); ghi rõ trong tài liệu |
| Dữ liệu cổ phiếu | nhỏ | BTC theo giờ (Binance) + JPY/USD (H.10); không có nguồn cổ phiếu mở giấy phép rõ |
| Markov switching (lab 5) | nhỏ | hộp "Nâng cao" + hình (≤ 6 khái niệm); hàm và ô notebook vẫn có |
| Survivorship / look-ahead / chuẩn hoá toàn cục | nhỏ | chuẩn hoá toàn cục + chia ngẫu nhiên là chỗ hở của code; survivorship, look-ahead trong "Lỗi thường gặp" |
| Cột mốc M2 | — | mục 7 bài tập "bậc thang mô hình" + mục 8 bảng tự đánh giá M2 (buổi 14–21) |
| Chỗ hở | nhỏ | `du_bao_gia` chia ngẫu nhiên + chuẩn hoá toàn chuỗi, `danh_gia_gia` chỉ báo R²; `var_99` chuẩn với độ lệch chuẩn cố định. Bảng `quy-uoc.md` cập nhật |

## Đọc thử (Phase 20, 2026-09-19)

Tự đọc (không subagent), checklist `tools/CHUAN-DE-HIEU.md`. Tính lại: ln 1,02 → 1,98; ln(99/102) → −2,99; tổng −1,01; 9,53 / −9,53, +10 / −9,09 /
+0,91; R² ≈ 1 − (1,84 / 14,7)² = 0,984 (độ lệch chuẩn giá BTC 2024 = 14,68 nghìn, sai số naive 1,84 nghìn); GARCH 1,37 và 0,4 và 0,835 / 0,2;
RV 1,98 và 6; HAR 7,54; VaR −2,33 / −2,57; Kupiec 6/250 → LR 3,56, p 0,059; 20/1.000 → 7,83; 0/1.000 → 20,1; ES chuẩn 2,665; quiz 5 (4,88;
−10,54; −5,66), 6 (3,13; 2,5), 7 (−3,49; −3,86), 8 (0,80), 10 (LR 10,5).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 3.595 | 12 | 0 | 1 | 3 | 10/10 | khó: hình VaR nói "năm 2022 khi yên mất giá" nhưng lỗ của người giữ USD đến từ những ngày yên **tăng** giá mạnh cuối 2022. Nhỏ: "gấp đôi hơn 1%"; hệ số HAR không nói học trên đoạn nào; giá đầu năm 2024 ghi 42 nghìn (thật 44,2) — sửa ngay khi kiểm số |
| 2 | 3.595 | 12 | **0** | **0** | 1 | 10/10 | sửa chú thích hình VaR, câu Kupiec, ghi rõ hệ số HAR học tới cuối 2024 |
| rà gọn | biên tập viên | — | — | — | — | — | 0 chỗ thừa đáng kể |

Căn cứ quiz: 1, 5 → 4.1; 2 → 4.2; 3, 9 → 4.3; 6 → 4.4; 8 → 4.5; 4, 7, 10 → 4.6. `kiem_de_hieu.py 21` 0; `kiem_tra_lab.py 21` đạt.

## Đọc thử độc lập (Phase 21, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: lợi suất 1,98 / −2,99 / −1,01; R² naive 0,984 và
0,9975; GARCH 1,37 / 0,4 và 0,835 / 0,2; RV 1,98, 6; HAR; Student-t (scipy: t 1% với ν 5,8 = −3,18 × 0,809 = −2,57); Kupiec LR 3,56 (p
0,059), 7,83, 20,1, 9,80 (p 0,002), 0,18 (p 0,67); ES 2,665; quiz 5 (4,88 / −10,54 / −5,66), 6 (3,13 / 2,5), 7, 8 (0,80), 10 (LR 10,5).

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.5 | "2,43 + 2,25 + 2,07 + 0,79 = 7,54" | 4 | với hệ số hiển thị 0,23; 0,26; 0,13 thì ra 2,3 + 2,08 + 0,78 = 7,59 | khó |
| 2 | 4.6 + Lab bước 4 | "Student-t … (đã đưa về cùng độ lệch chuẩn 1): −2,57%" | 4 | không nói đưa về bằng cách nào; Lab bắt tự viết đúng phép đó | khó |
| 3 | Lab bước 2 | "in thêm R² và MAE của naive, DM" | 5 | bộ chấm đòi khoá tên cụ thể, tài liệu không nói | nhỏ |
| 4 | 4.2 hình | "mật độ (thang log)" | 1 | "mật độ" chưa định nghĩa | nhỏ |
| 5 | 2 | "không quá 2,33 độ lệch chuẩn về phía dưới" | 3 | câu lủng củng | nhỏ |
| 6 | quiz câu 7 (đáp án) | "−2,33 × 1,5 = −3,49%" | 4 | = 3,495, làm tròn thành 3,50 | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Lợi suất log**: 80 → 88 → 80: +9,53 và −9,53, tổng 0.
- **Cụm biến động**: độ lớn 0,1; 0,2; 3; 2,5; 0,1 — ba ngày lớn liền nhau.
- **Demo 99%**: độ lệch chuẩn giá 10, sai số naive 1 → R² 0,99 mà không dự báo gì.
- **GARCH**: ω 0,1, α 0,1, β 0,8, σ² 1, ε 2 → 1,3; dài hạn 1.
- **RV / HAR**: 1, −1, 1, −1 → lợi suất ngày 0, RV 4.
- **VaR / Kupiec**: 500 ngày, kỳ vọng 5 lần vượt; 5 lần là khớp.

### C. Quiz mù

1 B · 2 B · 3 B · 4 B · 5 4,88; −10,54; −5,66 · 6 3,13; 2,5 · 7 −3,50% (35 triệu), −3,86% (38,6 triệu) · 8 0; 0; 0,80 · 9 chuẩn hoá cả chuỗi,
chia ngẫu nhiên, không có naive · 10 quá thận trọng, Kupiec bác. Căn cứ: 1, 5 → 4.1; 2 → 4.2; 3, 9 → 4.3; 6 → 4.4; 8 → 4.5; 4, 7, 10 → 4.6.
Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 2 / nhỏ 4.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10.** Sửa: #1 phép tính HAR theo đúng hệ số hiển thị (7,59; hệ số 3 chữ số cho 7,54 — ví dụ là tính tay nên dùng số đang in); #2
ví dụ 4.6 nói rõ "quantile −3,18, nhân $\sqrt{(\nu-2)/\nu} \approx 0{,}81$ → −2,57"; Lab bước 4 đưa tên cột của `du_bao_garch` và biểu thức
quantile; #3 Lab bước 2 nêu các khoá `R² naive`, `MAE MLP`, `MAE naive`, `DM p`; #6 đáp án câu 7 "−3,495% (khoảng 35 triệu)". Giữ #4, #5.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 21 đọc mù | 3.595 | 12 | 0 | 2 | 4 | 10/10 | 0 |
| sau sửa, đọc lại | 3.637 | 12 | **0** | **0** | 2 | 10/10 | 0 |
