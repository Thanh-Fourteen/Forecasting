# Nhật ký research — Buổi 9: Đặc trưng chuỗi và khả năng dự báo

- **Ngày research:** 2026-09-18
- **Nền buổi:** Python 3.12.3; numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, scikit-learn 1.9.1,
  **dtaidistance 2.5.1** (mới thêm vào `tools/nen/phien-ban.toml`), matplotlib 3.11.2, openpyxl 3.1.5, pyarrow 25.0.1
- **[CHẠY]** = đã chạy trong nền buổi; mẫu 4.000 chuỗi M4 tháng, seed 42, cắt về 120 điểm học + 18 điểm chấm

## Nguồn đã đọc

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | FPP Pythonic ch. 4 "Time series features", https://otexts.com/fpppy/nbs/04-features.html | 2026-09-18 | $F_T$/$F_S$, acf features, STL features, entropy phổ, không gian đặc trưng |
| 2 | Lubba et al. (2019), "catch22", *Data Mining and Knowledge Discovery* 33:1821–1852, arXiv:1901.10200 | 2026-09-18 | bộ đặc trưng rút gọn |
| 3 | Goerg (2013), "Forecastable Component Analysis (ForeCA)", arXiv:1205.4591 | 2026-09-18 | Ω = 1 − entropy phổ chuẩn hoá |
| 4 | "Time Series Forecastability Measures", arXiv:2507.13556 (17/07/2025) | 2026-09-18 | entropy phổ ↔ sai số thật |
| 5 | "Spectral Predictability as a Fast Reliability Indicator…", arXiv:2511.08884 (12/11/2025) | 2026-09-18 | Ω và chọn mô hình, nối buổi 34–35 |
| 6 | Montero-Manso et al. (2020), FFORMA, *IJF* 36(1):86–92, https://robjhyndman.com/publications/fforma/ | 2026-09-18 | chọn mô hình theo đặc trưng |
| 7 | Kourentzes (2016), "ABC-XYZ analysis for forecasting", https://kourentzes.com/forecasting/2016/10/15/abc-xyz-analysis-for-forecasting/ | 2026-09-18 | ABC–XYZ và phê bình hệ số biến thiên |
| 8 | Monash Time Series Forecasting Repository, Zenodo record 4656480 (M4 monthly) | 2026-09-18 | dữ liệu, giấy phép |
| 9 | Truong, Oudre & Vayatis — `dtaidistance`/DTW; tài liệu `tslearn` 0.9.0, `dtaidistance` 2.5.1 (PyPI) | 2026-09-18 | phân cụm DTW |
| 10 | Nixtla `tsfeatures` 0.4.5 (PyPI, phát hành 2023-06-20), `tsfresh` 0.21.2, `pycatch22` 0.5.0 | 2026-09-18 | thư viện đặc trưng |

## Trích dẫn nguyên văn

**FPP ch. 4.** $F_T = \max(0, 1 - \mathrm{Var}(R_t)/\mathrm{Var}(T_t+R_t))$, $F_S = \max(0, 1 - \mathrm{Var}(R_t)/\mathrm{Var}(S_t+R_t))$.
Entropy phổ: "feat_spectral will compute the (Shannon) spectral entropy of a time series, which is a measure of how easy the
series is to forecast. A series which has strong trend and seasonality (and so is easy to forecast) will have entropy close to 0.
A series that is very noisy (and so is difficult to forecast) will have entropy close to 1." Về `spike`: "It is the variance of the
leave-one-out variances of R_t." Về không gian đặc trưng: sách tính 17 nhóm hàm đặc trưng → "This gives 42 features", rồi
`Pipeline([('scale', StandardScaler()), ('pca', PCA(n_components=2))])`.

**catch22 (abstract).** "Applying our method to a set of 93 time-series classification datasets … and using a filtered version of the
hctsa feature library (**4791 features**), we introduce a generically useful set of 22 CAnonical Time-series CHaracteristics, catch22.
This dimensionality reduction, from 4791 to 22, is associated with an approximately 1000-fold reduction in computation time and near
linear scaling with time-series length, despite an average reduction in classification accuracy of just 7%." → **con số 7.658 hay bị
chép lại là số đặc trưng hctsa thô của Fulcher & Jones (2017), không phải của catch22.**

**ForeCA (abstract).** "I introduce Forecastable Component Analysis (ForeCA) … Based on a new forecastability measure, ForeCA finds an
optimal transformation to separate a multivariate time series into a forecastable and an orthogonal white noise space."

**arXiv:2507.13556 (2025).** "This paper proposes using two metrics to quantify the forecastability of time series prior to model
development: the spectral predictability score and the largest Lyapunov exponent. … Our results demonstrate that these two metrics can
correctly reflect the inherent forecastability of a time series and have a strong correlation with the actual forecast performance of
various models."

**arXiv:2511.08884 (2025).** "We show that spectral predictability~$\Omega$ … systematically stratifies model family performance,
enabling fast model selection. … large time series foundation models (TSFMs) systematically outperform lightweight task-trained
baselines when $\Omega$ is high, while their advantage vanishes as $\Omega$ drops."

**FFORMA (abstract).** "We propose an automated method for obtaining weighted forecast combinations using time series features… The
approach achieved second position in the M4 competition."

**Kourentzes về ABC–XYZ.** ABC: "Common values are: A – 20% top items; B – 30% middle items; and C – 50% bottom items." XYZ: "The XYZ
analysis focuses on how difficult is an item to forecast, with X being the class with easier items and Z the class with the more
difficult ones." Phê bình: "Textbooks have supported the use of coefficient of variation. This is so flawed … Consider an item that has
more or less level sales with a lot of variability and an item that has seasonal sales with no randomness whatsoever. The first is
difficult to forecast, while the second is as easy as it gets … the coefficient of variation would not indicate this" và "A better
measure is forecast errors".

**Monash / M4 monthly.** Mô tả Zenodo: "This dataset contains 48000 monthly time series used in the M4 forecasting competition."
Giấy phép: CC BY 4.0 ("The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition
that the creator is appropriately credited."). **Lưu ý:** trang forecastingdata.org viết "All datasets are intended to use only for
research purpose." — hẹp hơn CC BY trên Zenodo; khoá dùng cho mục đích giảng dạy/nghiên cứu và ghi nguồn đầy đủ.

## Thư viện đã cân nhắc [CHẠY bởi agent research]

- **Nixtla `tsfeatures` 0.4.5**: bản phát hành cuối **2023-06-20** (đóng băng); chạy được trên pandas 3.0.5, trả 42 đặc trưng, ~77 s cho
  4.000 chuỗi (4 luồng). **Không đưa vào nền**: buổi này mục tiêu là *tự viết* đặc trưng bằng NumPy; nhắc trong Đọc thêm.
- **`pycatch22` 0.5.0**: chỉ có sdist, **cần trình biên dịch C + `Python.h`**, và **không khai numpy trong dependencies** dù import numpy
  lúc chạy → rủi ro khi dựng từ venv trắng. Không đưa vào nền.
- **`tsfresh` 0.21.2**: 782 đặc trưng với `EfficientFCParameters` — quá nặng cho một buổi 3 giờ; nhắc trong Đọc thêm.
- **DTW**: `tslearn` 0.9.0 (TimeSeriesKMeans/KShape, kéo theo numba) 7,8–18,7 s cho 300 chuỗi; **`dtaidistance` 2.5.1** có wheel manylinux,
  `distance_matrix_fast` 300×300 hết 0,28 s → **chọn dtaidistance** + phân cụm phân cấp Ward của scipy (ít phụ thuộc hơn).

## Số liệu thật của buổi [CHẠY]

- **Dữ liệu:** `.tsf` M4 tháng — **48.000 chuỗi**, độ dài 60–2.812, `@horizon 18`, `@missing false`. Bộ đọc tự viết (thư viện chuẩn) mất
  ~9 s. Mẫu 4.000 chuỗi (seed 42) cắt về 138 điểm = 120 học + 18 chấm.
- **20 đặc trưng tự viết**: trung bình, độ lệch chuẩn, hệ số biến thiên, độ lệch, độ nhọn, acf1, acf10, acf mùa vụ, diff1_acf1,
  entropy phổ, $F_T$, $F_S$, spike, độ dốc và độ cong của xu hướng, tỷ lệ 0, số lần cắt trung bình, đoạn phẳng, bất ổn định, p-value KPSS.
  Phân bố: entropy trung vị 0,462 (ngũ phân vị 0,277 / 0,398 / 0,526 / 0,666); $F_S$ trung vị 0,566; $F_T$ trung vị 0,956.
- **Entropy ↔ sai số thật của seasonal naive** (18 điểm cuối):

| Đặc trưng | Thước đo | Pearson | Spearman |
|---|---|---|---|
| entropy phổ | **sMAPE** | **0,245** | **0,216** |
| entropy phổ | MASE (chia naive mùa vụ) | −0,048 | 0,027 |
| entropy phổ | MASE (chia naive 1 bước) | **−0,381** | **−0,535** |
| hệ số biến thiên | sMAPE | 0,653 | 0,765 |
| hệ số biến thiên | MASE (mùa vụ) | 0,002 | −0,113 |
| $F_S$ | sMAPE | −0,246 | −0,336 |

  Trung vị theo ngũ phân vị entropy — sMAPE: **5,38 / 4,87 / 5,15 / 6,11 / 12,04**; MASE: **1,02 / 0,95 / 1,01 / 1,02 / 1,02**.
- **Chiến lược:** ngưỡng entropy ≥ 0,666 (phân vị 80%) và $F_S$ < 0,4 → **137/4.000 chuỗi** vào nhóm "dùng baseline", sMAPE trung vị
  **18,11%** so với **6,05%** của phần còn lại (gấp 3).
- **Không gian đặc trưng:** PCA sau chuẩn hoá, PC1 + PC2 giữ ~45% phương sai.
- **Phân cụm DTW** (300 chuỗi, cửa sổ Sakoe–Chiba 10, Ward): chuẩn hoá z-score → 4 cụm 104/99/80/17, mức trung vị theo cụm
  2.882 / 4.891 / 2.951 / 4.164 (không theo thứ tự); **không chuẩn hoá** → 4 cụm 102/78/72/48 với mức trung vị
  **1.585 / 3.310 / 6.835 / 9.832** — tăng đều, tức chỉ phân cụm theo độ lớn.
- **ABC–XYZ** (Online Retail II, 2.773 mã hàng có ≥ 12 tháng): A chiếm **74,7%** doanh thu; hệ số biến thiên trung vị A 0,63 · B 0,83 ·
  C 0,92; ô AX 144 mã, CZ 567 mã.
- **Chuỗi lạ phát hiện được:** 1 chuỗi hằng (KPSS vỡ với `cannot convert float NaN to integer`), 50 chuỗi có "đoạn phẳng" > 50% số điểm.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình: "spectral entropy so với **MASE** của seasonal naive" — đo thật cho tương quan ≈ 0 (Pearson −0,05) vì MASE chia đúng cho sai số của chính seasonal naive | **lớn** | Đã sửa lộ trình + todos: dùng **sMAPE**; giữ MASE làm **chỗ hở cố ý** và bài học "đổi thước đo, đổi kết luận, đảo cả dấu" |
| "20 đặc trưng" — `tsfeatures` cho 42 | nhỏ | Tự viết đúng 20 đặc trưng bằng NumPy/statsmodels (đúng tinh thần khoá) |
| catch22 "7.658 đặc trưng" | nhỏ | Sửa thành 4.791 (đã sửa lộ trình) |
| Độ dài chuỗi 60–2.812 làm lệch đặc trưng | nhỏ | Cắt về 120 điểm cuối; nêu trong Lỗi thường gặp |
| `tslearn`/`pycatch22`/`tsfeatures` | nhỏ | Không đưa vào nền (numba/trình biên dịch/đóng băng); dùng `dtaidistance` |
| Ngưỡng XYZ 0,5 / 1,0 không có chuẩn học thuật | nhỏ | Nói rõ là **quy ước**, kèm phê bình của Kourentzes và số đo CV ↔ MASE (−0,11) |
| `kpss` vỡ trên chuỗi hằng | nhỏ | Bọc try/except → NaN, và dùng chính NaN đó để phát hiện chuỗi lạ |

## Research viết lại (Phase 12, 2026-09-18)

Research sư phạm (cách giải thích + hiểu lầm phổ biến), phiên bản chỉ rà lại vì có sửa code:

| Khái niệm | Cách giải thích chọn | Hiểu lầm phổ biến | Nguồn (truy cập 2026-09-18) |
|---|---|---|---|
| spectral entropy | phổ là "chia năng lượng thành phần"; entropy đo chia đều tới đâu (ẩn dụ chia bánh); tính tay trên 4 tần số | entropy thấp = chắc chắn dễ (sai với chuỗi xu hướng mạnh); so số giữa thư viện khác cách tính phổ | FPP ch. 4 (otexts.com/fpppy/nbs/04-features.html): "strong trend and seasonality … entropy close to 0"; arXiv:2507.13556; arXiv:2511.08884 |
| MASE / sMAPE | hai chuỗi 10 điểm tính tay: MASE nói chuỗi thất thường **dễ hơn**, sMAPE nói khó hơn 10 lần | MASE = 1 là "khó trung bình"; một thước đo cho mọi câu hỏi | số đo của buổi; Phụ lục D |
| PCA | ví dụ 3 chuỗi × 2 đặc trưng ngược dấu ($r_1$, số lần cắt trung bình) → một trục chung giữ 100% | PCA tự biết cột nào quan trọng; quên chuẩn hoá cột | FPP ch. 4: "PC1 is the linear combination of the features which explains the most variation" |
| DTW | bảng $D(i,j)$ 4 × 4 tính tay; ẩn dụ dây cao su; phải z-score | DTW khớp được mọi độ lệch (điểm đầu/cuối bắt buộc khớp); bỏ chuẩn hoá | Keogh, *Everything you know about DTW is Wrong* (cs.ucr.edu/~eamonn/DTW_myths.pdf); tài liệu dtaidistance |
| ABC–XYZ | hai mã $P$ (mùa vụ đều, CV 0,58) và $Q$ (quanh mức, CV 0,09): XYZ xếp ngược độ khó | CV cao = khó dự báo | Kourentzes 2016 (kourentzes.com …/abc-xyz-analysis-for-forecasting/): "seasonal sales with no randomness … as easy as it gets"; đề xuất dùng sai số dự báo ngoài mẫu |
| catch22 | một đặc trưng trên hai chuỗi 8 điểm: đoạn dài nhất trên trung bình (4 và 1) | nhiều đặc trưng = nhiều thông tin | Lubba 2019; danh sách đặc trưng catch22 (github DynamicsAndNeuralSystems/catch22, featureList.txt) |

Phiên bản PyPI (2026-09-18): `pycatch22` 0.5.0 (chỉ sdist, 2026-08-06), `tsfeatures` 0.4.5 (2023-06-20), `tsfresh` 0.21.2, `dtaidistance`
2.5.1 — không đổi so với research gốc.

**Sửa code (không phải chỗ hở cố ý), phát hiện khi viết lại:**

1. Docstring nói "chỉ 2 đặc trưng phụ thuộc đơn vị", nhưng nhân chuỗi với 1.000 thì spike (×10¹²), độ dốc, độ cong (×1.000) cũng đổi. Sửa:
   STL chạy trên chuỗi đã z-score (như FPP/tsfeatures) ở cả `code/` và `dap-an/`; kiểm lại: 18/20 đặc trưng giữ nguyên khi nhân 1.000.
2. `khong_gian_dac_trung` đưa **cả cột sai số** (`smape_snaive`, `mase_*`) và hai đặc trưng quy mô vào PCA, vì `bang` = đặc trưng join
   sai số. Bản đồ tô màu theo sMAPE mà sMAPE lại là đầu vào. Sửa: hàm `cot_ban_do` chỉ lấy 18 đặc trưng không đơn vị.
   PC1 + PC2: ~45% (bản cũ) → **56%** (41% + 15%). PC1 nặng ở số lần cắt trung bình (+0,39), $r_1$, tổng $r_k^2$, bất ổn định (−0,38…−0,39);
   PC2 ở độ dốc (+0,52), độ cong (−0,52), $F_S$ (−0,45).
3. `ve_hinh.py` in "đặc trưng mạnh nhất PC1" lệch chỉ số cột → sửa; thêm hình `entropy-hai-chuoi.png` (seed 0: entropy 0,33 và 0,94).
4. Đổi khoá `do_lech` → `he_so_lech` (Phụ lục E: hệ số lệch).

Các số khác tái lập đúng (seed 42): bảng tương quan entropy × sMAPE/MASE, 137/3.863 chuỗi, 18,11%/6,05%, cụm DTW, ABC–XYZ. $F_S$ × sMAPE
Pearson −0,246 → −0,245 (STL trên chuỗi z-score, sai khác làm tròn).

## Đọc thử (Phase 12, 2026-09-18)

Tự đọc (không subagent), theo checklist `tools/CHUAN-DE-HIEU.md`; mọi ví dụ tay và đáp án quiz tính lại bằng Python (entropy 0 / 0,5 / 1 và
0,47 / 0,95; MASE 1,00 / 0,92 và sMAPE 6,7% / 76,2%; PCA 1,73; DTW 0 / 2 / 44,1; CV 0,58 / 0,09 / 1,1; $r_1$ = 0 của chuỗi $a$).

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (2.306 chữ, 10 trang, 52 cờ) | 10 | — | — | — | chặn: "phổ Welch" nhắc như đã học; PCA, DTW (công thức trần), hệ số lệch/độ nhọn, entropy (công thức không lời), MASE/sMAPE chưa định nghĩa, z-score, Ward/`fcluster`, nhiều trích tiếng Anh (FPP, Kourentzes, FFORMA, arXiv) mang ý chính; không hình nào có "Cách đọc hình"; quiz câu 9 cần số không có trong tài liệu |
| 1 | viết lại (5.575 chữ) | 0 | 2 | 4 | 10/10 có căn cứ | khó: mục 4.6 dùng "CV × MASE = −0,11" làm bằng chứng, trái với chính mục 4.3 (MASE của seasonal naive luôn quanh 1); "tune" chưa định nghĩa. Nhỏ: "sóng tần số 1/2 lên xuống mỗi tháng"; "khoảng cách thường" ở bảng Từ mới trước khi giải thích; câu "entropy cao thì ngược lại" nói lửng; bảng DTW vỡ công thức trong PDF |
| 2 | sau sửa (5.567 chữ, 17 trang) | **0** | **0** | 2 | 10/10 | **đạt**. Mục 4.6 viết lại trung thực: trên M4, CV × sMAPE Spearman 0,77 (CV có liên quan tới độ khó ở dữ liệu này), nhưng CV xếp sai chuỗi mùa vụ đều; −0,11 với MASE "không nói gì". Thêm "tune" vào Từ mới |
| rà gọn | biên tập viên | — | — | — | — | 1 chỗ: câu "Ngưỡng 0,5 và 1,0 chỉ là quy ước" lặp ví dụ mục 4.6 → xoá. Còn lại không đoạn nào ≥ 30 chữ lặp ý |

`kiem_de_hieu.py 9`: 52 → **0**. Quiz viết lại 10 câu (4 nhắc lại, 4 vận dụng, 2 tìm chỗ sai), căn cứ: 1 → 4.2, 2 → 4.1, 3 → 4.3, 4 → 4.6,
5 → 4.2, 6 → 4.3, 7 → 4.5, 8 → 4.4, 9 → 4.3, 10 → 4.5. Notebook `code/lab.ipynb` soạn bằng `tools/nb.py`, chạy hết trên `code/` (~20 s).

## Đọc thử độc lập (Phase 15, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại bằng Python: hệ số lệch 1,749; độ lệch chuẩn
$A$/$B$ 2,51/2,67; bảng DTW + DTW$(x, z)$ = 2 + z-score $(−0,58; 1,73)$; PCA 1,22/1,73; MASE 1,00/0,92, sMAPE 6,7%/76,2%; quiz 5 (0,946),
7 (44,09; z −0,71/1,41). Khớp hết, trừ một ô ở câu "Nói bằng lời" của DTW.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.1 bảng | "số lần cắt trung bình" | 1 | đọc được thành "trung bình số lần cắt"; không nói cắt cái gì | khó |
| 2 | 4.1 bảng | "bất ổn định" | 1 | không định nghĩa | nhỏ |
| 3 | 4.1 Đọc bảng | "như FPP làm" | 7 | viết tắt, chỉ mở ở Đọc thêm | nhỏ |
| 4 | Từ mới | "so với phân phối chuẩn" | 8 | "phân phối chuẩn" không nhắc lại | nhỏ |
| 5 | 4.5 Nói bằng lời | "$\min(1, 0, 0) = 0$" | 5 | ba ô trên/trái/chéo là 1, 1, 0: số sai, kết quả đúng | nhỏ |
| 6 | 4.4 Chiến lược | "Ghép hai đặc trưng" | 4 | không nói vì sao không dùng một đặc trưng (quiz 8 căn cứ yếu) | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Đặc trưng**: 3, 0, 3, 0 → tỷ lệ số 0 là 0,5; nhân 10 vẫn 0,5.
- **Entropy**: phần năng lượng 0,7 / 0,3 → (0,250 + 0,361)/0,693 ≈ 0,88.
- **MASE vs sMAPE**: mức 500, seasonal naive sai 10 cả khi học lẫn khi chấm → MASE 1, sMAPE ≈ 2%.
- **PCA**: hai cột luôn ngược dấu → một trục giữ hết khác biệt.
- **DTW**: (0, 2, 0) với (2, 0, 0) → 0; với (0, 6, 0) → 4 nếu chưa chuẩn hoá.
- **ABC–XYZ**: 5, 15, 5, 15 có CV 0,58 (Y) mà seasonal naive chu kỳ 2 sai 0.

### C. Quiz mù

1 A · 2 C · 3 B · 4 A · 5 0,95, gần nhiễu · 6 MASE 1, sMAPE ≈ 3,5%, MASE = 1 không nói khó hay dễ · 7 chưa chuẩn hoá, sau z-score DTW 0 ·
8 chỉ $U$ (vế "vì sao không một đặc trưng": đoán) · 9 mẫu số MASE chứa độ khó, báo thêm sMAPE + Spearman · 10 phân cụm theo độ lớn; kiểm bằng
z-score và phép nhân 100. Căn cứ: 1, 5 → 4.2; 2 → 4.1; 3, 6, 9 → 4.3; 4 → 4.6; 7, 10 → 4.5; 8 → 4.4.

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 5. Sửa một điều: định nghĩa "số lần cắt trung bình".

### E. Dài/lặp

| # | Mục | Trích | Vì sao |
|---|---|---|---|
| 1 | 4.3 Khi nào dùng | "Dùng nó để so độ khó giữa các chuỗi…" | lần thứ ba nói "MASE của seasonal naive luôn quanh 1" (Trực giác, Tóm lại) |

### Chấm, sửa, đọc lại

**Quiz mù 10/10** khớp `kiem-tra.md`. Sửa bằng viết lại câu: định nghĩa trong ô bảng cho "số lần cắt trung bình" (cắt ngang đường trung
bình) và "bất ổn định"; "sách FPP của Hyndman (Đọc thêm)"; "(hình chuông)"; $\min(1, 1, 0)$; Chiến lược 4.4 thêm một câu "chỉ dùng entropy
thì gạt nhầm chuỗi entropy cao mà mùa vụ vẫn mạnh". Rà gọn: rút câu lặp ở 4.3.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 15 đọc mù | 5.567 | 17 | 0 | 1 | 5 | 10/10 (1 vế căn cứ yếu) | 1 |
| sau sửa, đọc lại | 5.586 | 17 | **0** | **0** | 1 ("sai phân" không nhắc lại) | 10/10, mọi câu có căn cứ | 0 |

**Đạt.** `kiem_de_hieu.py 9` 0; `kiem_tra_lab.py 9` đạt; tự chứa đạt.
