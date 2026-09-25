# Nhật ký research — Buổi 23: Gradient boosting chuyên sâu

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-24 (Phase 22). Buổi soạn mới hoàn toàn (thư mục tạo từ khuôn).
- **Người/phiên:** Phase 22, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Makridakis, Spiliotis & Assimakopoulos (2022). M5 accuracy competition: Results, findings, and conclusions. *IJF* 38(4). Bản tiền in (45 trang, đọc toàn văn): https://statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf. Đội thắng (YJ_STU, YeonJun Im): trung bình đều 6 mô hình LightGBM (theo cửa hàng 10, cửa hàng–ngành 30, cửa hàng–nhóm hàng 70; mỗi loại một bản recursive, một bản non-recursive; 220 mô hình), tối ưu log-likelihood Tweedie, không early stopping, CV 4 cửa sổ 28 ngày, WRMSSE 0,520, hơn benchmark ES_bu 22,4%. Hạng 4 (monsaraida): non-recursive, mỗi tuần của tầm dự báo một mô hình, Tweedie. Hạng 5: Poisson + early stopping. Finding 1 ML thuần thắng; 2 kết hợp; 3 cross-learning; 6 CV hiệu quả; 7 biến ngoại sinh (giá, khuyến mãi, sự kiện) | bài tổng kết | 2026-09-24 | 4.1, 4.3, Đọc thêm |
| 2 | LightGBM Parameters: `objective=tweedie` (log-link), `tweedie_variance_power` mặc định 1,5, khoảng [1, 2) — gần 1 như Poisson, gần 2 như Gamma; `monotone_constraints` (1 tăng, −1 giảm, 0 tự do), `monotone_constraints_method` basic/intermediate/advanced; `pred_contrib=True` trả SHAP (số đặc trưng + 1, phần tử cuối là giá trị kỳ vọng) — https://lightgbm.readthedocs.io/en/latest/Parameters.html | tài liệu chính thức | 2026-09-24 | 4.3, 4.5, 4.6 |
| 3 | Optuna v5.0.0 release notes (2026-09-07): https://github.com/optuna/optuna/releases — TPESampler mặc định bật multivariate TPE và constant liar; PED-ANOVA thành mặc định cho tầm quan trọng tham số; `constraints_func` bị deprecate. API dùng trong buổi (`create_study`, `optimize`, `suggest_int/float(log=True)`, `TPESampler(seed=…)`) không đổi | changelog | 2026-09-24 | 4.4, code |
| 4 | Bergmeir, Hyndman & Koo (2018). *CSDA* 120: 70–83 — KFold hợp lệ cho mô hình tự hồi quy thuần khi phần dư không tương quan; ngoài điều kiện đó dùng out-of-sample theo thời gian: https://robjhyndman.com/publications/cv-time-series/ | bài gốc | 2026-09-24 | 4.4 "Nâng cao" |
| 5 | Lundberg, Erion, Chen et al. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence* 2: 56–67 — TreeSHAP chính xác, thời gian đa thức; gain/split không nhất quán | bài gốc | 2026-09-24 | 4.5 |
| 6 | Molnar, *Interpretable Machine Learning* — PD mô tả mô hình; với đặc trưng tương quan, PD trộn hiệu ứng: https://christophm.github.io/interpretable-ml-book/ | sách mở | 2026-09-24 | 4.6 |
| 7 | Damato et al. (2026), arXiv 2601.14031 — trên hơn 40.000 chuỗi gián đoạn, đầu ra Tweedie cho quantile cao tốt nhất | bài mới (12 tháng) | 2026-09-24 | bối cảnh 4.3 |
| 8 | UCI Online Retail II (Chen 2012), CC BY 4.0; mirror HF của khoá; 2 sheet, 1.067.371 dòng | dữ liệu | 2026-09-24 | toàn buổi |

## Phiên bản đã xác minh (PyPI 2026-09-24)

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| lightgbm | 4.7.0 (2026-07-18) | mới nhất |
| optuna | 5.0.0 (2026-09-07) | mới nhất |
| scikit-learn | 1.9.1 | chỉ dùng `KFold` cho bản `code/` và bảng so sánh |
| statsforecast | 2.1.1 | AutoETS, SeasonalNaive, WindowAverage |
| shap | 0.52.0 (2026-05-28) | **không dùng**: `uv lock` kéo numba → llvmlite 0.36.0 (chỉ hỗ trợ Python < 3.10) vì numba chưa hỗ trợ numpy 2.5.3. Thay bằng `pred_contrib=True` của LightGBM (cùng thuật toán TreeSHAP) |
| xgboost 3.4.1, catboost 1.2.10 | — | chỉ nhắc so sánh trong 4.1, không cài |

## Dữ liệu

| Bộ | Danh mục | Giấy phép | Ghi chú |
|---|---|---|---|
| `uci-online-retail-ii` | sha256 `572e36277c23`, 45,6 MB | CC BY 4.0 | Đọc 2 sheet mất 40–100 s → lưu `lab/du-lieu/cache/giao-dich.parquet`. Giữ dòng Quantity > 0, Price > 0, StockCode 5 chữ số (+ 1 chữ cái) — bỏ POST, DOT, M, C2, ADJUST… |
| `m5-kaggle` | chưa chốt sha256 | cấm phân phối lại | Máy soạn không có tài khoản Kaggle đã chấp nhận luật → M5 chỉ ở bài tập về nhà 3 |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Giá "thực trả" trong ngày là rò rỉ và nhân quả ngược.** Giá mỗi dòng hoá đơn phụ thuộc lượng mua (mã 85123A: 2,95 cho đơn nhỏ, 2,55 cho đơn
  sỉ ~32 món). Giá trung bình của **ngày** thấp khi có đơn sỉ lớn → mô hình "học" giá thấp ↔ bán nhiều, và giá chỉ tồn tại khi có bán. Buổi dùng
  giá trung bình 28 ngày kết thúc ở t − 28 (biết được lúc dự báo). Bản thử đầu dùng giá mode của ngày trước đó (ffill + shift 1) cho WRMSSE 0,643 —
  đẹp giả tạo vì lộ ngày có bán.
- **Mọi lag ≥ 28 bỏ phí 27 ngày gần nhất** khi đoán ngày mai. Thử mô hình theo tuần (tuần j dùng lag ≥ 7j, như hạng 4 M5): WRMSSE 0,6767 so với
  0,6774 (cùng đặc trưng thêm 3 lag năm) — gần như không lợi → giữ một mô hình cho cả 28 ngày (đơn giản hơn), ghi ở đây.
- Tweedie đoán trên thang log: SHAP của LightGBM là trên điểm thô (log), cộng lại = `predict(raw_score=True)`; mỗi đóng góp là một phép nhân.
- KFold và CV thời gian chấm trên những ngày khác nhau → **không so trị tuyệt đối** RMSE của hai cách chia (RMSE KFold ~69, CV thời gian ~52 vì
  KFold gồm cả mùa Giáng sinh 2010). Đưa thành câu quiz 9.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| **Dữ liệu chính là UCI Online Retail II thay cho M5** (một bang, ~10.000 chuỗi) | lớn (đổi dataset) | Đã lường trước trong `todos/phase-22.md` ("luôn có bộ dự phòng mở UCI Online Retail II"); M5 chưa chốt sha256 trong danh mục nên `sinh_nen` không cho vào buổi. Online Retail có giá bán, nhiều số 0, mùa Giáng sinh → đủ cho Tweedie, WRMSSE, PD của giá. 500 mã × 604 ngày bán hàng. M5 chuyển thành bài tập về nhà 3 cho người có tài khoản Kaggle. Đã cập nhật lộ trình; báo người dùng ở báo cáo cuối phase |
| WRMSSE chỉ cấp mã hàng (M5: 12 cấp) | nhỏ | Online Retail không có cửa hàng/bang; nói rõ trong 4.2 |
| Không dùng gói `shap` | nhỏ | xem bảng phiên bản; `pred_contrib` là TreeSHAP gốc của LightGBM |
| "Tweedie thắng AutoETS" chỉ đạt **sau khi tune** | nhỏ | Mặc định: Tweedie 0,680 > AutoETS 0,674. Tune bằng CV thời gian: 0,669 < 0,674. Viết trung thực: tune là bước cần, và KFold-tune (0,678) không thắng |
| Partial dependence "phát hiện chiều sai" | đạt | PD không ràng buộc tăng 21,75 → 23,11 món khi giá £0,32 → £2,79; nguyên nhân khác biệt giữa các mã |

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0; máy soạn 12 nhân; chạy lại hai lần ra cùng số)

| Đại lượng | Giá trị |
|---|---|
| Dữ liệu | 500 mã, 604 ngày bán hàng 1/12/2009 → 9/12/2011; bảng học 246.000 dòng (t ≥ 112); cutoff t = 519, 547, 575 = 2/9, 5/10, 7/11/2011 |
| Phân phối | 35,26% ô bằng 0; trung vị 3; trung bình 18,74; quantile 0,99 = 226; lớn nhất 11.124 |
| Ví dụ boosting | y = (2, 4, 9, 13): 7 → (5, 5, 9, 9) → (4, 4, 10, 10); SSE 74 → 26 → 14; cây 3 → (3,5; 3,5; 10,5; 10,5), SSE 11 |
| Ví dụ Poisson | y = 0, ŷ = 10: 20; y = 1.000, ŷ = 990: 2 × (1000 ln(1000/990) − 10) = 0,1007; tỷ lệ ~200 |
| WRMSSE (3 cutoff) | SeasonalNaive(6) 0,9107; WindowAverage(28) 0,6969; AutoETS 0,6739; LightGBM L2 0,7093; Poisson 0,6958; Tweedie 0,6804; Tweedie tune KFold 0,6782; Tweedie tune CV thời gian 0,6687; Tweedie + đơn điệu giá 0,6780 |
| Optuna (50 thử, TPE seed 0, n_estimators 200) | KFold chọn num_leaves 70, min_child_samples 103, lr 0,051: RMSE KFold 69,26, CV thời gian 51,94. CV thời gian chọn 55, 38, 0,016: 69,87 / 51,76. Mỗi study ~4 phút (12 nhân) |
| Tầm quan trọng (mô hình cutoff cuối) | gain: mã 39,5%, TB 28 ngày 32,3%, TB 84 6,0%, tuần 5,2%, thứ 3,8%; split: mã 36,9%, tuần 10,6%, ngày trong tháng 8,1%, TB 28 5,0%, TB 84 5,0% |
| SHAP | mã 22659 (LUNCHBOX I LOVE LONDON), 1/12/2011 (thứ Năm, tuần 48): dự báo 251,4, thực tế 6; nền log 2,2586 (9,57 món); mã +0,855, tuần 48 +0,791, TB 28 = 24,71 +0,651, thứ +0,419, ngày 1 +0,199, lag 56 = 360 +0,092, còn lại +0,261; tổng 5,527 |
| Kiểm chứng câu "tuần 48 cả cửa hàng bán mạnh" | tuần ISO 48/2010: 247.902 món, trung vị các tuần 2010: 101.313 (gấp 2,4). Mã 22659 tuần 29/11–5/12/2010: 979 món; cùng tuần 2011: 272 |
| PD giá (lưới £0,32 → £10,19, 25 điểm) | không ràng buộc 21,75 → 23,11 (tại £2,79) → 22,82; ràng buộc 22,92 → 21,13, không tăng |
| Thời gian | `ve_hinh.py` lần đầu 7,8 phút (2 study Optuna + 9 backtest); `lab.py check` ~2 s (dùng cache giao dịch) |

## Đọc thử (2026-09-24, Phase 22, tự đọc — không subagent)

**Vòng 1 — vai học viên mới:**

| # | Mục | Chỗ vướng | Mức | Đã sửa |
|---|---|---|---|---|
| 1 | 4.3 | "Tweedie nằm giữa Poisson và các phân phối cho số dương lệch phải" — "phân phối" kiểu gì, nút vặn làm gì | khó | viết lại: "họ hàm mất mát có nút vặn … bằng 1 thì giống Poisson, càng gần 2 càng chịu được đuôi dài" |
| 2 | 4.5 | "Nói với quản lý" nói "năm ngoái bán rất mạnh" — hình SHAP không có thanh nào về năm ngoái | khó | viết lại đúng ba thanh lớn nhất (mã hàng, tuần 48, trung bình 28 ngày) |
| 3 | 4.1 | "Ban tổ chức kết luận đặc trưng … quyết định thứ hạng nhiều hơn loại mô hình" — bài gốc không nói vậy | khó (sai nguồn) | sửa theo Finding 6–7: biến ngoài chuỗi và cách chia dữ liệu để tự chấm |
| 4 | 4.5 | nhãn hình "TB 28 ngày" (viết tắt) | nhỏ | đổi thành "trung bình 28 ngày" trong hình và bài |
| 5 | 4.4 | "TPE" | nhỏ | bỏ tên, nói "cách đề xuất mặc định" |
| 6 | 4.2 | "Bình phương bước nhảy TB" | nhỏ | viết đủ |

Vòng 1: 0 chặn, 3 khó (sửa hết), 3 nhỏ. **Vòng 2** sau sửa: 0 chặn, 0 khó, 1 nhỏ (4.3 "thang log" của hình phân phối có cột số 0 — đã ghi trong
"Cách đọc hình" bước 1).

**B — giải thích lại bằng ví dụ mới:** boosting y = (1, 3, 8, 12), học suất 1 → sau cây 1 là (2, 2, 10, 10); WRMSSE ba mã 0,5/0,3/0,2 × RMSSE
1/2/0 = 1,1; Poisson y = 0, ŷ = 4 → 8 so với y = 400, ŷ = 396 → ≈ 0,04; CV thời gian 12 tuần 3 fold kiểm 2 tuần; SHAP f = 3 + a với a trung
bình 0,25 → dòng a = 1 góp +0,75; PD f = 50 − 4 × giá. Không khái niệm nào "không giải thích được".

**C — quiz có căn cứ:** C1 → 4.1; C2 → 4.2 (công thức, nhầm hay gặp); C3 → 4.4 (trực giác); C4 → 4.5; C5 → 4.1 (bảng); C6 → 4.2; C7 → 4.3
"Nói bằng lời" + 4.5 tự kiểm tra; C8 → 4.3 (bảng WRMSSE); C9 → 4.4 (đọc bảng: "hai cột RMSE không so được"); C10 → 4.6 ("Vì sao sai
chiều"). Mọi số tính lại bằng Python: C5 (8 + 0,5 × 4 = 10), C6 (0,82; trung bình không trọng số 0,833), C7 ($e^{3,7}$ = 40,45; $e^3$ + 0,7 =
20,79; $e^{4,1}$ = 60,34), 4.1 cây 3 (SSE 11), 4.3 tự kiểm tra (0,0302), 4.6 tự kiểm tra (6 và 9).

**Rà gọn (vai biên tập viên):** 3 chỗ: đoạn mở mục 4 liệt kê đủ 15 đặc trưng (lặp danh sách trong code, câu 48 chữ) → rút còn nhóm đặc trưng;
"Đọc kết quả" bước 1–2 chép lại số của 4.3 → trỏ về mục; "Kết luận" hình SHAP chép lại 3 số đóng góp đã có trên hình → chỉ nêu tên ba thanh.
Lượt rà cuối: 1 chỗ thừa nhỏ (bảng so sánh LightGBM/XGBoost/CatBoost một câu, giữ vì lộ trình yêu cầu).

**Số chữ:** 4.073 → 4.105 (thêm dòng "dừng sớm" vào bảng Từ mới và câu nói với quản lý, bỏ danh sách đặc trưng); `kiem_de_hieu.py 23`: 0 vi phạm.

## Đọc thử độc lập (Phase 24, 2026-09-24)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: boosting 74 → 26 → 14 → 11 (cây 3); WRMSSE 0,75 và
0,5; Poisson 20 / 0,10 và 6 / 0,03 (ln(1000/990) = 0,01005); $e^{2{,}26}$ = 9,58, $e^{0{,}69}$ = 1,99, $e^{0{,}79}$ = 2,20, $e^{2{,}7}$ = 14,88;
SHAP giả 2,5 + 1 + 0,5 = 4; PD 18 / 16 và 6 / 9; **$e^{5{,}53}$ = 252,1, không phải 251** (tổng thật 5,527 → 251,4); 35,26% ô bằng 0 ("hơn một
phần ba") khớp bảng "Số liệu thật".

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.5 hình + Lab bước 4 | "điểm thô 5,53, tức $e^{5,53}$ ≈ 251 món" | 4 | tự tính ra 252 | khó |
| 2 | Từ mới, 4.4 | "CV theo thời gian", "điểm CV" | 7 | chữ viết tắt CV không giải thích | nhỏ |
| 3 | 4.2 bảng | "Sai số kỳ chấm: 2" | 3 | một con số cho cả kỳ: mỗi ngày lệch 2 hay RMSE = 2? | nhỏ |
| 4 | 4.3 ví dụ | "$y \ln(y/\hat y)$" | 2 | mục 2 viết "log", ở đây "ln" | nhỏ |
| 5 | 4.4 bảng | "RMSE KFold 69,26" | 3 | không có đơn vị | nhỏ |
| 6 | 1 | "thắng L2" | 1 | L2 định nghĩa ở 4.3 | nhỏ |
| 7 | 4.1 | "cột phân loại (như mã hàng)" | 1 | đoán được từ ví dụ | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Boosting**: $y$ = (1, 3, 5, 11), trung bình 5, phần dư (−4, −2, 0, 6); lá −3 / +3, học suất 0,5 → dự báo (3,5; 3,5; 6,5; 6,5).
- **WRMSSE**: RMSSE 0,9 và 1,5, doanh thu 80 và 20 → 0,72 + 0,30 = 1,02.
- **Tweedie/Poisson**: thực tế 0, đoán 5 → Poisson 10; thực tế 500, đoán 495 → 2 × (500 × 0,01005 − 5) ≈ 0,05.
- **CV theo thời gian**: 12 tháng, 3 fold kiểm 2 tháng: học 1–6/kiểm 7–8, học 1–8/kiểm 9–10, học 1–10/kiểm 11–12.
- **SHAP**: nền log 1,5; đóng góp +1, −0,5 → 2,0 → $e^2$ ≈ 7,4 món.
- **PD + đơn điệu**: $f$ = 20 − giá + 0,5 × chất lượng; PD giảm 1 món mỗi £1; nếu PD đi lên → ràng buộc −1.

### C. Quiz mù

1 B · 2 B · 3 B · 4 C · 5 B · 6 B · 7 C · 8 B · 9 C · 10 B. Căn cứ: 1, 5 → 4.1; 2, 6 → 4.2; 8 → 4.3; 3, 9 → 4.4; 4, 7 → 4.5; 10 → 4.6. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 6. Nếu chỉ sửa một điều: con số điểm thô SHAP phải mũ lên đúng ra 251.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10** (đáp án khớp). Sửa: #1 "5,527" ở cả hình 4.5 và Lab bước 4; #2 dòng "CV theo thời gian" của bảng Từ mới mở bằng "CV (cross-validation,
kiểm định chéo) là chia dữ liệu để tự chấm"; #3 cột "Sai số mỗi ngày kỳ chấm"; #4 "($\ln$ là log cơ số $e$)"; #5 "(món)" ở hai cột RMSE. Giữ #6, #7.
Đọc lại toàn bộ: 0 chặn / 0 khó / 2 nhỏ; rà gọn: 0 chỗ thừa đáng kể.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 24 đọc mù | 4.119 | 13 | 0 | 1 | 6 | 10/10 | 0 |
| sau sửa, đọc lại | 4.125 | 13 | **0** | **0** | 2 | 10/10 | 0 |
