# Nhật ký research — Buổi 24: Ensemble, AutoML và ca khó

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-24 (Phase 23). Buổi soạn mới hoàn toàn (thư mục tạo từ khuôn).
- **Người/phiên:** Phase 23, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Hyndman & Athanasopoulos, *FPP3* §13.4 Forecast combinations: https://otexts.com/fpp3/combinations.html — trung bình ETS, STL-ETS, ARIMA cho doanh thu đồ ăn mang đi: RMSE 41,0 so với ARIMA 46,2; dẫn Clemen (1989) "chỉ lấy trung bình thường cải thiện đáng kể" | sách | 2026-09-24 | 4.1, Đọc thêm |
| 2 | Wang, Hyndman, Li & Kang (2023). Forecast combinations: an over 50-year review. *IJF* 39(4): 1518–1547 (arXiv 2205.04216) — tổng quan: trọng số đều, theo sai số, stacking, cross-learning; combination puzzle | tổng quan | 2026-09-24 | 4.1, 4.2 |
| 3 | Claeskens, Magnus, Vasnev & Wang (2016). The forecast combination puzzle: A simple theoretical explanation. *IJF* 32(3) — trọng số ước lượng thêm độ chệch và phương sai, đủ để thua trọng số đều; Smith & Wallis (2009) — sai số ước lượng trọng số là nguyên nhân chính | bài gốc | 2026-09-24 | 4.2 |
| 4 | Frazier, Covey, Martin & Poskitt (2023). Solving the forecast combination puzzle, arXiv 2308.05263 (đọc tóm tắt + mở đầu) — phép kiểm so hai cách kết hợp có công suất thấp; ước lượng hiệu quả hơn thì puzzle biến mất | phản biện mới | 2026-09-24 | 4.2 "Nâng cao" |
| 5 | Montero-Manso, Athanasopoulos, Hyndman & Talagala (2020). FFORMA: Feature-based forecast model averaging. *IJF* 36(1): 86–92 — mô hình tầng trên (gradient boosting) học trọng số từ 42 đặc trưng chuỗi; hạng 2 M4 | bài gốc | 2026-09-24 | 4.2 "Nâng cao" |
| 6 | AutoGluon 1.6.1 docs: TimeSeriesPredictor.fit (https://auto.gluon.ai/stable/api/autogluon.timeseries.TimeSeriesPredictor.fit.html), model zoo (forecasting-model-zoo.html). Đọc thêm mã nguồn 1.6.2 cài trong venv: `configs/predictor_presets.py` — medium_quality = hyperparameters "light" = SeasonalNaive, ETS, Theta, RecursiveTabular, DirectTabular, Chronos2 (chronos-2-small), Toto2 (4m); high_quality = "default" thêm AutoETS, DynamicOptimizedTheta, TFT, DeepAR, Chronos-2 base + small fine-tune, Toto-2 22m; best_quality = high + nhiều cửa sổ kiểm; `fast_training` đã bỏ (quy về medium). Ensemble mặc định GreedyEnsemble = ensemble selection của Caruana et al. (2004) | tài liệu chính thức + mã nguồn | 2026-09-24 | 4.4 |
| 7 | Chronos-2 (Ansari et al. 2025, arXiv 2510.15821): tập tiền huấn luyện gồm một phần kho Chronos + GIFT-Eval pretrain + dữ liệu tổng hợp. Bài tổng quan tìm được nêu "kho tiền huấn luyện của Chronos, MOIRAI, TimesFM, TTM chứa phần lớn M4" | bài gốc + tổng quan | 2026-09-24 | 4.4: loại Chronos2, Toto2 khi chấm trên M4 |
| 8 | Makridakis, Spiliotis & Assimakopoulos (2020). The M4 Competition. *IJF* 36(1) — kết hợp thống kê chiếm phần lớn top; hạng 1 lai ES-RNN, hạng 2 FFORMA | bài gốc | 2026-09-24 | 4.1, dữ liệu |
| 9 | Cawley & Talbot (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. *JMLR* 11 — chọn trên cùng dữ liệu đánh giá gây lạc quan, tăng theo số ứng viên; cần đánh giá lồng | bài gốc | 2026-09-24 | 4.3 |
| 10 | Tìm kiếm "cold start demand forecasting new products analog" (2026-09-24): các cách chính — hàng tương tự (analog), theo thuộc tính, đường vòng đời, gộp chuỗi; arXiv 2604.20370 (diffusion cho vòng đời sản phẩm mới, 2026). Goodwin, Dyussekeneva & Meeran (2013), dự báo bằng phép tương tự cho sản phẩm mới, *IMA J. Management Mathematics* 24(4) | bài mới + bài gốc | 2026-09-24 | 4.5 |
| 11 | UCI Online Retail II (CC BY 4.0), Monash M4 monthly (Zenodo 4656480, CC BY 4.0) — cả hai đã chốt sha256 trong danh mục | dữ liệu | 2026-09-24 | toàn buổi |

## Phiên bản đã xác minh (PyPI 2026-09-24)

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| autogluon.timeseries | 1.6.2 | mới nhất trước mốc `exclude_newer` 2026-09-17 (1.6.3 ra 2026-09-18). Yêu cầu pandas < 2.4, torch ≥ 2.10 < 2.14 (**macOS < 2.11**), statsforecast < 2.1.2, coreforecast < 0.0.17, utilsforecast < 0.2.12, mlforecast < 0.15, pyarrow < 25 |
| statsforecast | **2.0.3** (bảng chung 2.1.1) | 2.1.x cần coreforecast ≥ 0.0.17 → xung đột AutoGluon. Thêm `[[rang_buoc]]` khi dùng AutoGluon: statsforecast 2.0.3, utilsforecast 0.2.11, coreforecast 0.0.16, mlforecast 0.14.0, pyarrow 24.0.0, numpy 2.4.6, scipy 1.15.3 (kết quả `uv pip compile` cho linux, macOS arm64, Windows ra cùng một bộ) |
| torch | **2.10.0+cpu** (bảng chung 2.13.0) | `[[rang_buoc]]` cũ ép 2.13.0 → `uv lock` hỏng ở nhánh macOS. 2.10.0 là bản duy nhất hợp mọi nền tảng |
| lightgbm | 4.7.0 | |
| pandas | 2.3.3 | ràng buộc có sẵn cho hệ Nixtla/AutoGluon |

**Sửa công cụ:** `tools/sinh_nen.py` — gói thuộc index riêng (torch CPU) nhưng chỉ bị kéo GIÁN TIẾP qua `[[rang_buoc]]` giờ được đưa thành
phụ thuộc trực tiếp, vì `[tool.uv.sources]` chỉ áp cho phụ thuộc trực tiếp. Trước khi sửa, venv buổi 24 kéo torch CUDA từ PyPI: **8,2 GB**
(4,3 GB thư viện nvidia); sau khi sửa **2,2 GB**. Buổi khác không đổi (không buổi nào khác dùng torch gián tiếp lúc này).

## Dữ liệu

| Bộ | Danh mục | Giấy phép | Ghi chú |
|---|---|---|---|
| `monash-m4-monthly` | sha256 chốt, mirror HF | CC BY 4.0 | 48.000 chuỗi; ngày bắt đầu thật (1790 → 2012). Trình đọc `tv.du_lieu.doc_du_lieu` mất ~2 phút cho tệp 77 MB → buổi đọc thẳng (< 1 giây). Chọn 1.000 chuỗi ngẫu nhiên (seed 0) trong 32.097 chuỗi dài ≥ 150 tháng, giữ 150 tháng cuối |
| `uci-online-retail-ii` | sha256 `572e36277c23` | CC BY 4.0 | Cần cả cột Description để đoán danh mục → cache riêng `giao-dich-mo-ta.parquet`. Description có ô kiểu số → ép `string` trước khi ghi parquet |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **AutoARIMA quá chậm cho lab CPU**: ~1 giây/chuỗi tháng một nhân (200 chuỗi: 198 s), AutoCES 0,09 s, AutoETS 0,07 s → bỏ AutoARIMA và
  AutoCES khỏi 30 ứng viên. Bản thử đầu có cả hai: 85 phút CPU.
- **AutoGluon `medium_quality` gồm Chronos-2 và Toto-2** (mô hình tiền huấn luyện). Trên M4 phải loại (`excluded_model_types`) — quy tắc 8 của
  khoá (foundation model chỉ chấm trên dữ liệu sau mốc cắt). Không loại thì còn tải trọng số từ Hugging Face (chưa chốt revision).
- **AutoGluon tự dùng 18 tháng cuối của dữ liệu học làm đoạn kiểm** để xếp hạng và dựng ensemble → `score_val` của leaderboard là điểm "lúc chọn",
  lạc quan hơn `score_test` (0,858 so với 0,882). Chính là bài học 4.3, trong một công cụ.
- `time_limit=300` không chạm: medium_quality trên 1.000 chuỗi tháng học xong trong 43 giây (máy soạn 12 nhân).
- **Trọng số "tối ưu" ước lượng riêng từng chuỗi** (bình phương tối thiểu, 36 điểm/chuỗi) có tổng tới 1,91 ở vài chuỗi và cho MASE 0,965 —
  tệ hơn trung bình đều 0,837. Trọng số nghịch MSE (co về đều) nhỉnh hơn đều: 0,824. Viết trung thực: puzzle là về **sai số ước lượng**, không
  phải "trọng số luôn vô dụng".
- **Cold start**: danh mục đoán từ tên hàng (từ khoá) không giúp: analog cùng danh mục MAE 446,5 ≈ "trung bình danh mục" 446,6; analog theo
  **giá ra mắt gần nhất** (k = 40, chọn trên tập ra mắt sớm hơn) 400,6. Lần thử đầu danh mục chỉ 30 từ khoá: 105/200 mã rơi vào "KHAC";
  thêm 30 từ khoá (WALL ART, RIBBON, PENCIL…) còn 16. Hàng mới ra theo "họ" (10 mã EMBROIDERED RIBBON REEL cùng tuần) → không làm analog
  cho nhau được vì chưa bán xong 8 tuần.
- Thử (chưa đưa vào tài liệu): cập nhật analog sau 2 tuần bán đầu (nhân theo tỷ lệ) cho tuần 3–8 chỉ giảm MAE tuần 56,6 → 54,3; dữ liệu bán sỉ
  quá thất thường.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| AutoGluon "giới hạn 20 phút" | nhỏ | `time_limit=300` giây; medium_quality xong trong 43 giây nên giới hạn không chạm. Bài tập về nhà: high_quality với 20 phút |
| M4 dùng 1.000 chuỗi tháng, 3 cửa sổ 18 tháng; bỏ AutoARIMA | nhỏ | `check` < 10 phút trên CPU 4 nhân; bước 1 của lab ~3–4 phút lần đầu (cache) |
| "Chọn mô hình theo đặc trưng (FFORMA)" | nhỏ | Hộp "Nâng cao" trong 4.2 — không đủ chỗ cho khái niệm thứ 6 |
| "Chuỗi kết thúc, chuỗi đổi mã", "giới hạn dự báo trong khoảng (logit)" | nhỏ | Một câu trong 4.5 + "Lỗi thường gặp"; logit có tỷ lệ → bài tập về nhà |
| "Cold start thắng trung bình danh mục" bằng **analog theo danh mục** | vừa | Danh mục đoán từ tên hàng không thắng; analog theo **giá** thắng (400,6 so với 446,6). Viết trung thực: chọn "tương tự theo cái gì" cũng phải backtest |
| Stacking | nhỏ | Dạy qua trọng số ước lượng trên backtest (tầng 2 = ước lượng trọng số); rò rỉ tầng 2 là trọng số ước lượng cả trên đoạn báo cáo (0,677 giả) |

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0; máy soạn 12 nhân)

| Nội dung | Giá trị |
|---|---|
| MASE W3 (cửa sổ báo cáo): TB(ETS,Theta,LGBM) / LGBM / AutoETS / SeasonalNaive | 0,837 / 0,855 / 0,892 / 1,174 |
| Chọn theo chuỗi, chọn và báo cáo trên cả 3 cửa sổ (SAI — `code/`) | 0,694 (chỉ W3: 0,585) |
| Chọn theo chuỗi trên W1–W2, báo cáo W3 | 0,658 → 0,883 (lạc quan 0,224) |
| Chọn chung trên W1–W2 | TB(ETS,LGBM) 0,828 → 0,840; chỉ mô hình đơn: LGBM 0,847 → 0,855 |
| Lạc quan theo số ứng viên k = 1, 3, 5, 10, 20, 30 | 0,013; 0,097; 0,129; 0,172; 0,206; 0,224 |
| Trọng số từng chuỗi (ước lượng W1–W2, chấm W3): đều / nghịch MSE / tối ưu | 0,837 / 0,824 / 0,965 |
| Trọng số tối ưu ước lượng cả trên W3 (SAI) | 0,677 |
| AutoGluon medium_quality (bỏ Chronos2, Toto2): WeightedEnsemble val/test | 0,858 / 0,882; trọng số ETS 0,554, Theta 0,292, RecursiveTabular 0,108, DirectTabular 0,046; 43 giây |
| Cold start (200 mã ra mắt 1/8 → 10/10/2011): MAE tổng 8 tuần, tỷ lệ trong 2 lần | tb_danh_muc 446,6 / 31,5%; analog_danh_muc 446,5 / 24%; analog_gia (k = 40) 400,6 / 34,5%; đoán 0: 509,0 |

## Đọc thử (2026-09-24, Phase 23, tự đọc — không subagent)

**Vòng 1 — vai học viên mới** (đọc toàn bộ `tai-lieu.md` bằng Read, chỉ dùng những gì đã viết trước chỗ đang đọc):

| Mức | Chỗ | Vướng | Sửa (viết lại câu) |
|---|---|---|---|
| khó | 4.4 điều 2 | `score_val` chưa nối với cột nào của bảng | ghi rõ "cột `score_val`… cột MASE đoạn kiểm trong bảng dưới" |
| khó | 4.4 Đọc bảng | "LightGBM direct có chuẩn hoá mức" chưa giải thích | "chia mỗi chuỗi cho mức trung bình 12 tháng gần nhất để mọi chuỗi cùng thang" |
| khó | 4.5 bảng | "lệch không quá 2 lần" mơ hồ | "dự báo trong khoảng nửa tới gấp đôi thực tế" |
| khó | 4.5 | "chưa tới hai mùa vụ" | "hai chu kỳ mùa vụ, ví dụ dưới 24 tháng với mùa vụ năm" |
| khó | 4.1/4.4 | AutoTheta, "LightGBM đệ quy" dùng mà Nhắc lại chưa có | thêm AutoTheta và recursive vào mục 2 |
| nhỏ | 4.2 | "gán 1,9 lần một mô hình" | "trọng số 1,9 (lấy gấp 1,9 lần dự báo của nó)" |
| nhỏ | 4.4 ví dụ | "(trung bình ETS, Theta tốt hơn ETS, ETS)" khó đọc | "ETS với Theta tốt hơn ETS với chính nó" |

Chặn 0 · khó 5 · nhỏ 2. **B — giải thích lại bằng ví dụ mới**: 4.1 thực tế 20, A 23, B 18 → trung bình 20,5 sai −0,5, ít hơn cả hai; 4.2 MSE 1 và
3 → 1 và 1/3 → trọng số 0,75, 0,25; 4.3 ba mô hình ngang nhau (thật 1,00), điểm 0,95, 1,02, 0,98 → chọn 0,95, lạc quan 0,05; 4.4 chuỗi lượt A, A, B,
C, A → 0,6/0,2/0,2; 4.5 mã ra mắt 5/9, mã tương tự ra mắt 1/8 → tuần 8 bắt đầu 19/9 > 5/9 → không dùng được. Không khái niệm nào giải thích không nổi.
**C — quiz**: câu 1 → 4.1 (ρ, bảng); 2 → 4.2 bảng; 3 → 4.3 hình + bảng (sửa đáp án: trước trích 0,01 và 0,224 không có nguyên văn trong tài liệu →
0,22 và 0,013); 4 → 4.4 điều 1; 5 → 4.2 công thức (kiểm Python: 2/3, 1/6, 1/6); 6 → 4.4 ví dụ tham lam; 7 → 4.1 công thức (10·√0,25 = 5); 8 → 4.5 luật
không rò rỉ (10/1 + 8 tuần = 7/3 ≤ 7/3; 17/1 + 8 tuần = 14/3); 9 → 4.3 bảng (0,834 = trung bình ba cửa sổ của TB(ETS,Theta,LGBM), in từ `ve_hinh.py`;
17% = 1 − 0,694/0,834); 10 → 4.4 điều 1–2 (bảng giả định, ghi rõ trong đề câu). Mọi câu có căn cứ.
**Kiểm số**: mọi con số tài liệu đối chiếu với output `dap-an/ve_hinh.py` (bảng "Số liệu thật" ở trên); sửa 2 khẳng định sai trước khi đọc thử:
"hộp đựng bánh và giá để bánh cùng là CAKE" (sai: CAKE STAND → STAND theo thứ tự từ khoá; thay bằng ví dụ thật "thiệp" gom bộ bài, ví đựng thẻ; ô in
hình bánh → "bánh"), "cột W3 luôn tệ hơn cột đoạn kiểm" (sai: RecursiveTabular 1,027 → 1,005). Câu 9 bản đầu có số 0,843 tự đặt → thay bằng 0,834 thật.

**Vòng 2 — rà gọn (vai biên tập viên)**: 1 chỗ thừa đáng kể — ý "trung bình không sai hơn trung bình các mức sai" nói 3 lần (Trực giác 4.1, Đọc bảng,
đáp án Tự kiểm tra) → cắt câu ở Trực giác. Các câu "Nói bằng lời" lặp số của ví dụ là bắt buộc (D3), giữ. Còn 0 chỗ thừa đáng kể.

**Vòng 3 — đọc lại các đoạn đã sửa/cắt** trong ngữ cảnh: không phát sinh chỗ vướng mới.

| | Trước rà gọn | Sau |
|---|---|---|
| Chữ ngoài bảng/code (`kiem_de_hieu`) | 4.620 | 4.597 |
| `kiem_de_hieu.py 24` | 0 | 0 |
| PDF | 14 trang | 14 trang |

**Lab**: `kiem_tra_lab.py 24` — up ✓, `check --dap-an` xanh 6/6, `check` (code/) đỏ đúng 2/6, `lab.ipynb` chạy hết 2,6 phút, down ✓.

## Đọc thử độc lập (Phase 24, 2026-09-24)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: 102 → −2, (108 + 104)/2 → −6; $10\sqrt{0{,}75}$ = 8,66,
$10\sqrt{0{,}5}$ = 7,07; nghịch MSE 0,8/0,2 và 1/2, 1/4, 1/4; lạc quan 0,10 và 0,883 − 0,658 = 0,225; trọng số AutoGluon 36/65 = 0,554, 19/65 =
0,292, 7/65 = 0,108, 3/65 = 0,046; trung vị cold start 30/40/50/40 (tổng 160, trung bình tuần 1 = 50); (446,6 − 400,6)/446,6 = 10,3%; 10/1/2011 +
56 ngày = 7/3 (quiz 8). **"Chọn một ứng viên chung … lạc quan 0,013"**: bảng cho 0,828 → 0,840 = 0,012; 0,013 là điểm $k$ = 1 của hình (bảng "Số
liệu thật"), lấy nhầm số.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.1 công thức | "cùng độ lệch chuẩn $\sigma$, hệ số tương quan … $\rho$" | 8 | độ lệch chuẩn, tương quan dùng như đã học; mục 2 không nhắc | khó |
| 2 | 4.3 Đọc bảng | "lạc quan chỉ 0,013" | 4 | bảng ngay trên cho 0,012 | khó |
| 3 | 4.4 | "hai mô hình tiền huấn luyện Chronos-2, Toto-2" | 1 | nghĩa chỉ đoán được từ câu sau | nhỏ |
| 4 | 4.5 | "tính trung vị từng tuần" | 1 | định nghĩa trung vị ở đoạn sau | nhỏ |
| 5 | Lab bước 1 | "dòng cuối là HistoricAverage" | 1 | tên mô hình chưa giải thích | nhỏ |
| 6 | 4.4 bảng | ETS W3 0,902 | 4 | khác AutoETS 0,892 ở 4.1, không nói vì sao (hai cài đặt khác nhau) | nhỏ |
| 7 | 4.5 bảng | "trung bình danh mục: mức bán mỗi tuần … 8 tuần trước ra mắt" | 3 | đọc hai lần mới hiểu | nhỏ |
| 8 | quiz 10 | "Chronos-2 zero-shot" | 1 | "zero-shot" không có trong tài liệu | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Trung bình dự báo**: thực tế 20, A 26, B 17 → trung bình 21,5, sai −1,5 (A −6, B +3).
- **Đa dạng**: $\sigma$ = 6, $\rho$ = 0 → 6 × 0,707 ≈ 4,2; $\rho$ = 1 → 6.
- **Nghịch MSE**: MSE 3 và 6 → 1/3 : 1/6 → 2/3 và 1/3.
- **Khoảng lạc quan**: 4 mô hình ngang nhau (thật 0,8), điểm chọn 0,72 / 0,85 / 0,79 / 0,83 → chọn 0,72, lạc quan 0,08.
- **Ensemble tham lam**: 6 lượt Theta, ETS, Theta, Theta, ETS, Naive → Theta 0,5, ETS 1/3, Naive 1/6.
- **Cold start**: ra mắt 2/5; hàng tương tự phải ra mắt từ 7/3 trở về trước.

### C. Quiz mù

1 B · 2 A · 3 B · 4 B · 5 2/3, 1/6, 1/6 · 6 ETS 0,6, Theta 0,2, DirectTabular 0,2 · 7 5 · 8 B · 9 chọn và báo cáo cùng đoạn; trung thực: chọn W1–W2,
báo cáo W3 (0,883 so với ensemble 0,837) · 10 Chronos-2 đã thấy M4; score_val là điểm lúc chọn. Căn cứ: 1, 7 → 4.1; 2, 5 → 4.2; 3, 9 → 4.3; 4, 6, 10
→ 4.4; 8 → 4.5. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 2 / nhỏ 6. Nếu chỉ sửa một điều: nhắc lại độ lệch chuẩn và hệ số tương quan ở mục 2 (công thức lợi ích của trung bình dựa vào chúng).

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10** (đáp án khớp). Sửa: #1 mục 2 thêm một gạch "Độ lệch chuẩn … Hệ số tương quan … gần 1 / 0 / gần −1"; #2 "lạc quan chỉ khoảng 0,01" (cả
đáp án quiz câu 3); #3 thêm câu "Mô hình tiền huấn luyện đã học sẵn trên kho dữ liệu lớn, dùng ngay không cần học lại" (và rút câu sau cho khỏi lặp);
#4 định nghĩa trung vị ở lần dùng đầu, bỏ định nghĩa lặp ở "Đọc bảng"; #5 "(trung bình toàn bộ lịch sử)"; #8 bỏ "zero-shot" khỏi quiz. Giữ #6, #7.
Đọc lại toàn bộ: 0 chặn / 0 khó / 2 nhỏ; rà gọn: 0 chỗ thừa đáng kể.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 24 đọc mù | 4.597 | 14 | 0 | 2 | 6 | 10/10 | 0 |
| sau sửa, đọc lại | 4.668 | 14 | **0** | **0** | 2 | 10/10 | 0 |
