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
