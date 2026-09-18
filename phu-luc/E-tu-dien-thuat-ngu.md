# Phụ lục E — Từ điển thuật ngữ Anh–Việt

Chuẩn dùng từ cho **mọi** tài liệu của khoá. Khi soạn buổi mới mà gặp thuật ngữ chưa có ở đây: thêm vào
đúng nhóm trước, rồi mới dùng.

## Quy ước viết

1. **Giữ nguyên tiếng Anh** khi thuật ngữ là tên phương pháp, tên chỉ số, hoặc từ mà người làm nghề ở Việt
   Nam dùng nguyên văn: *backtest, baseline, quantile, drift, feature, pipeline, seasonal naive, ACF*… Lần
   đầu xuất hiện trong một buổi thì kèm giải thích tiếng Việt.
2. **Dịch** khi tiếng Việt đã quen và không mơ hồ: *xu hướng* (trend), *mùa vụ* (seasonality), *phần dư*
   (residual), *ngoại lai* (outlier). Lần đầu trong buổi ghi kèm tiếng Anh trong ngoặc.
3. Cột **Viết trong khoá** là dạng dùng trong câu. Không dùng lẫn hai dạng trong một buổi.
4. Tên hàm, tham số, tên cột giữ đúng như trong code: `unique_id`, `ds`, `y`, `closed='left'`.
5. Công thức đầy đủ của chỉ số: Phụ lục D. Cách đọc biểu đồ: Phụ lục C.

## Mục lục

- [1. Bài toán dự báo](#1-bài-toán-dự-báo)
- [2. Dữ liệu và thời gian](#2-dữ-liệu-và-thời-gian)
- [3. Mô tả chuỗi thời gian](#3-mô-tả-chuỗi-thời-gian)
- [4. Làm sạch, ngoại lai, khử nhiễu](#4-làm-sạch-ngoại-lai-khử-nhiễu)
- [5. Feature và rò rỉ](#5-feature-và-rò-rỉ)
- [6. Đánh giá](#6-đánh-giá)
- [7. Mô hình thống kê](#7-mô-hình-thống-kê)
- [8. Machine learning và deep learning](#8-machine-learning-và-deep-learning)
- [9. Bất định](#9-bất-định)
- [10. Foundation model và LLM](#10-foundation-model-và-llm)
- [11. Nhân quả và ra quyết định](#11-nhân-quả-và-ra-quyết-định)
- [12. Production](#12-production)
- [13. Xác suất thống kê](#13-xác-suất-thống-kê)

## 1. Bài toán dự báo

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| forecast | dự báo | phát biểu về giá trị tương lai dựa trên thông tin hiện có | 1 |
| forecast horizon | tầm dự báo (horizon), $h$ | dự báo cho bao nhiêu bước phía trước | 1 |
| granularity | độ chi tiết | mức gộp của chuỗi: SKU × cửa hàng × ngày… | 1 |
| forecast origin / cutoff | mốc cắt dữ liệu (cutoff) | thời điểm ra dự báo; mọi thông tin sau mốc là tương lai | 1, 15 |
| point forecast | dự báo điểm | một con số cho mỗi thời điểm | 1 |
| interval forecast | dự báo khoảng | khoảng kèm mức xác suất danh nghĩa | 1, 25 |
| probabilistic / distributional forecast | dự báo xác suất / dự báo phân phối | cả phân phối (quantile, mẫu, tham số) | 1, 25 |
| target | biến mục tiêu | đại lượng được dự báo | 1 |
| judgmental forecast | dự báo phán đoán | dự báo dựa trên ý kiến chuyên gia | 1, 40 |
| nowcasting | nowcasting | ước lượng hiện tại / quá khứ gần khi số liệu chính thức chưa công bố | 20 |

## 2. Dữ liệu và thời gian

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| time series | chuỗi thời gian | dãy quan sát theo thời gian | 1 |
| frequency | tần suất | khoảng cách giữa hai quan sát: giờ, ngày, tháng | 3 |
| regular / irregular series | chuỗi đều / chuỗi không đều | quan sát cách đều / không cách đều | 3 |
| resample | resample (gộp / tách tần suất) | đổi tần suất: giảm (gộp) hoặc tăng | 3 |
| time zone, UTC | múi giờ, UTC | | 3 |
| naive / aware timestamp | timestamp naive / aware | không gắn / có gắn múi giờ | 3 |
| DST (daylight saving time) | giờ mùa hè (DST) | giờ bị mất hoặc bị lặp khi chuyển | 3 |
| long / wide format | định dạng dài / định dạng rộng | `unique_id, ds, y` mỗi dòng một quan sát / mỗi cột một chuỗi | 3 |
| as-of join | ghép as-of | ghép với giá trị gần nhất trong quá khứ (`merge_asof`) | 3, 41 |
| vintage | vintage (bản công bố) | số liệu đúng như đã công bố tại một thời điểm, trước các lần sửa | 20, 41 |
| point-in-time | point-in-time | chỉ dùng dữ liệu đã tồn tại tại thời điểm ra dự báo | 41 |
| revision (data) | sửa số liệu lùi | nguồn công bố lại giá trị quá khứ | 20, 41 |
| sha256 | sha256 | dấu vân tay của tệp; tệp đổi một byte thì sha256 đổi | mọi buổi |

## 3. Mô tả chuỗi thời gian

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| trend | xu hướng | thay đổi dài hạn của mức | 4, 6 |
| seasonality | mùa vụ | mẫu lặp theo chu kỳ **cố định, biết trước**, gắn với lịch | 4, 6 |
| seasonal period, $m$ | chu kỳ mùa vụ, $m$ | 24 cho mùa vụ ngày của dữ liệu giờ, 7 cho tuần của dữ liệu ngày | 4 |
| multiple seasonality | mùa vụ kép / đa mùa vụ | nhiều chu kỳ cùng lúc (ngày + tuần + năm) | 6, 18 |
| cycle | chu kỳ | dao động **không có tần số cố định** | 4 |
| level shift | dịch mức | mức trung bình đổi đột ngột và giữ nguyên | 11 |
| structural break / changepoint | điểm gãy | thời điểm cấu trúc chuỗi thay đổi | 11 |
| decomposition (additive / multiplicative) | phân rã (cộng / nhân) | tách xu hướng–chu kỳ, mùa vụ, phần dư | 6 |
| STL, MSTL | STL, MSTL | phân rã dùng loess; MSTL cho đa mùa vụ | 6 |
| remainder / residual | phần dư | phần còn lại sau khi bỏ các thành phần (hoặc sau mô hình) | 6, 17 |
| autocorrelation, ACF | tự tương quan, ACF | tương quan giữa chuỗi và chính nó trễ $k$ bước | 7 |
| partial autocorrelation, PACF | tự tương quan riêng phần, PACF | tương quan ở trễ $k$ sau khi bỏ ảnh hưởng các trễ nhỏ hơn | 7 |
| lag | trễ | $y_{t-k}$ | 7 |
| white noise | nhiễu trắng | chuỗi không tự tương quan | 7 |
| stationarity | tính dừng | tính chất thống kê không đổi theo thời gian | 7 |
| differencing | sai phân | $y_t - y_{t-1}$ (hoặc $y_t - y_{t-m}$) | 7 |
| unit root test (ADF, KPSS) | kiểm định nghiệm đơn vị (ADF, KPSS) | ADF: giả thuyết gốc không dừng; KPSS: giả thuyết gốc dừng | 7 |
| cross-correlation, CCF | tương quan chéo, CCF | tương quan giữa hai chuỗi ở các độ trễ | 8 |
| prewhitening | prewhitening | lọc bỏ tự tương quan trước khi tính CCF | 8 |
| spurious correlation / regression | tương quan giả / hồi quy giả | tương quan cao giữa hai chuỗi có xu hướng mà không liên quan | 8, 18 |
| Granger causality | nhân quả Granger | quá khứ của X giúp dự báo Y — **không** phải nhân quả thật | 8 |
| mutual information | mutual information | đo phụ thuộc cả phi tuyến | 8 |
| spectral entropy | spectral entropy | độ "phẳng" của phổ — cao nghĩa là giống nhiễu, khó dự báo | 9 |
| forecastability | khả năng dự báo | mức chuỗi có cấu trúc khai thác được | 9 |
| Box-Cox transformation | biến đổi Box-Cox | họ biến đổi luỹ thừa/log ổn định phương sai | 5 |
| bias adjustment (back-transform) | hiệu chỉnh bias khi biến đổi ngược | sửa việc exp(trung bình của log) ra trung vị chứ không ra trung bình | 5 |

## 4. Làm sạch, ngoại lai, khử nhiễu

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| missing data (MCAR / MAR / MNAR) | dữ liệu thiếu (MCAR / MAR / MNAR) | thiếu hoàn toàn ngẫu nhiên / ngẫu nhiên có điều kiện / không ngẫu nhiên | 10 |
| imputation | điền dữ liệu (imputation) | ước lượng giá trị thiếu | 10 |
| flag column | cột cờ | cột đánh dấu giá trị đã sửa/điền, không xoá dấu vết | 10 |
| stuck sensor | cảm biến đứng yên | giá trị lặp y hệt nhiều giờ | 10 |
| outlier / anomaly | ngoại lai / bất thường | quan sát lệch khỏi hành vi chung | 11 |
| Hampel filter | bộ lọc Hampel | phát hiện ngoại lai bằng trung vị + MAD trong cửa sổ trượt | 11 |
| denoising / smoothing | khử nhiễu / làm trơn | | 12 |
| causal / non-causal filter | bộ lọc nhân quả / không nhân quả | chỉ dùng quá khứ / dùng cả tương lai (`filtfilt`, rolling centered) | 12 |
| aliasing | aliasing | tần số cao giả dạng tần số thấp khi hạ mẫu không lọc | 12 |
| Nyquist frequency | tần số Nyquist | nửa tần số lấy mẫu; tần số cao hơn không thấy được | 12 |

## 5. Feature và rò rỉ

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| feature | feature | biến đầu vào của mô hình | 13 |
| lag feature, rolling feature | feature trễ, feature cửa sổ trượt | | 13 |
| data leakage / look-ahead bias | rò rỉ tương lai | dùng thông tin chưa có tại mốc cắt → kết quả đẹp giả tạo | 12, 13 |
| target leakage | rò rỉ mục tiêu | feature chứa chính biến mục tiêu | 13 |
| exogenous variable / covariate | biến ngoại sinh / covariate | biến giải thích ngoài chuỗi | 18, 30 |
| future-known covariate | covariate biết trước tương lai | lịch, lễ, giá đã chốt — **không** gồm thời tiết thực tế | 30, 35 |
| holiday effect | hiệu ứng ngày lễ | Tết âm lịch đổi ngày dương lịch mỗi năm | 13 |

## 6. Đánh giá

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| baseline | baseline | mô hình đơn giản phải thắng được | 14 |
| naive / seasonal naive | naive / seasonal naive | dự báo = giá trị cuối / giá trị cùng kỳ mùa trước | 14 |
| drift method | phương pháp drift | nối điểm đầu và cuối rồi kéo dài | 14 |
| in-sample / out-of-sample | trong mẫu / ngoài mẫu | trên dữ liệu huấn luyện / trên dữ liệu chưa thấy | 14 |
| train / validation / test | tập huấn luyện / kiểm định / test | | 15 |
| backtest | backtest | đánh giá lặp lại trên nhiều mốc cắt quá khứ | 15 |
| rolling origin / time series cross-validation | rolling origin | mốc cắt trượt dần; chỉ dùng dữ liệu trước mốc | 15 |
| expanding / sliding window | cửa sổ mở rộng / cửa sổ trượt | | 15 |
| gap | khoảng đệm (gap) | bỏ trống giữa train và test để mô phỏng độ trễ dữ liệu | 15 |
| MAE, RMSE, MAPE, sMAPE, MASE, RMSSE, WAPE | giữ nguyên | Phụ lục D | 14 |
| scale-free / scaled error | sai số không đơn vị / có chia thang | | 14 |
| Diebold–Mariano test | kiểm định Diebold–Mariano | so độ chính xác hai mô hình | 15 |
| skill score | skill score | mức cải thiện tương đối so với tham chiếu | 14, 25 |
| forecast value added (FVA) | FVA | mỗi bước trong quy trình cải thiện dự báo bao nhiêu | 40 |

## 7. Mô hình thống kê

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| exponential smoothing, ETS | làm trơn hàm mũ, ETS | Error–Trend–Seasonal | 16 |
| damped trend | xu hướng tắt dần (damped) | | 16 |
| Theta method | phương pháp Theta | | 16 |
| ARIMA / SARIMA | ARIMA / SARIMA | tự hồi quy – sai phân – trung bình trượt (có mùa vụ) | 17 |
| information criterion (AIC, AICc, BIC) | tiêu chí thông tin | chọn mô hình, phạt số tham số | 17 |
| Ljung–Box test | kiểm định Ljung–Box | kiểm phần dư còn tự tương quan không | 17 |
| dynamic regression | hồi quy động | hồi quy với sai số ARIMA | 18 |
| Fourier terms | số hạng Fourier | sin/cos mô tả mùa vụ | 18 |
| intermittent demand | nhu cầu gián đoạn | chuỗi nhiều số 0 | 19 |
| Croston, TSB | Croston, TSB | phương pháp cho nhu cầu gián đoạn | 19 |
| state space model, Kalman filter | mô hình không gian trạng thái, bộ lọc Kalman | | 20 |
| VAR, cointegration | VAR, đồng liên kết (cointegration) | | 20 |
| volatility, GARCH | biến động (volatility), GARCH | | 21 |
| hierarchical / grouped series | chuỗi phân cấp / phân nhóm | | 28 |
| reconciliation (bottom-up, top-down, MinT) | reconciliation | làm các cấp cộng khớp nhau | 28 |

## 8. Machine learning và deep learning

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| global / local model | mô hình global / local | một mô hình cho nhiều chuỗi / mỗi chuỗi một mô hình | 22 |
| recursive / direct / MIMO strategy | chiến lược recursive / direct / MIMO | cách dự báo nhiều bước | 22 |
| gradient boosting | gradient boosting | | 23 |
| Tweedie loss | hàm mất mát Tweedie | cho dữ liệu đếm nhiều số 0 | 23 |
| hyperparameter tuning | tune siêu tham số | | 23 |
| SHAP | SHAP | giải thích đóng góp của feature | 23 |
| ensemble, forecast combination | ensemble, kết hợp dự báo | | 24 |
| cold start | cold start | dự báo cho chuỗi mới chưa có lịch sử | 24 |
| window, context length | cửa sổ, độ dài ngữ cảnh | số bước quá khứ mô hình được xem | 29, 34 |
| epoch, early stopping | epoch, dừng sớm | | 29 |
| Transformer, attention, patching | Transformer, attention, patching | | 31 |
| generative model, diffusion | mô hình sinh, diffusion | | 32 |
| synthetic data (fidelity / utility / privacy) | dữ liệu tổng hợp | giống thật / dùng được / không chép nguyên | 32 |
| graph neural network (GNN) | mạng nơ-ron đồ thị (GNN) | | 33 |

## 9. Bất định

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| prediction interval | khoảng dự báo | cho giá trị tương lai (khác khoảng tin cậy — Phụ lục B) | 2, 25 |
| confidence interval | khoảng tin cậy | cho tham số | 2 |
| coverage | tỷ lệ phủ (coverage) | tỷ lệ giá trị thật rơi trong khoảng | 25 |
| calibration | calibration | tần suất thật khớp xác suất dự báo | 25 |
| sharpness | độ sắc (sharpness) | khoảng / phân phối hẹp tới đâu | 25 |
| pinball loss / quantile loss | pinball loss | Phụ lục D | 25 |
| CRPS, WIS, Winkler score | giữ nguyên | Phụ lục D | 25 |
| PIT histogram, reliability diagram | giữ nguyên | Phụ lục C | 25 |
| quantile crossing | quantile cắt nhau | quantile mức thấp lớn hơn mức cao | 25 |
| sample path | sample path | một kịch bản tương lai sinh từ mô hình | 25, 32 |
| conformal prediction (split, CQR, ACI, EnbPI) | conformal prediction | khoảng có bảo đảm coverage dưới giả định hoán đổi được | 26 |
| exchangeability | tính hoán đổi được | giả định của conformal, chuỗi có drift vi phạm | 26 |
| prior / posterior, prior predictive check | prior / posterior, kiểm tra dự báo tiên nghiệm | | 27 |
| pooling (no / complete / partial) | gộp thông tin (không / hoàn toàn / một phần) | | 27 |
| divergence, $\hat R$, ESS | divergence, r_hat, ESS | chẩn đoán hội tụ MCMC | 27 |
| Gaussian process, kernel | quá trình Gauss, kernel | | 27 |

## 10. Foundation model và LLM

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| foundation model | foundation model | mô hình huấn luyện trước trên rất nhiều chuỗi, dùng zero-shot | 34 |
| zero-shot / few-shot / fine-tune | zero-shot / few-shot / fine-tune | không học thêm / vài ví dụ / học tiếp | 34, 35 |
| LoRA | LoRA | fine-tune bằng ma trận hạng thấp | 35 |
| training cutoff / knowledge cutoff | mốc cắt dữ liệu huấn luyện | model đã thấy dữ liệu tới đâu — đánh giá phải sau mốc này | 34, 37 |
| benchmark contamination | rò rỉ benchmark | dữ liệu test đã nằm trong dữ liệu huấn luyện trước | 35 |
| revision (model) | revision | commit cụ thể của model trên Hugging Face — luôn chốt | 34 |
| agent, tool calling, guardrail | agent, gọi công cụ, guardrail | | 36 |
| hallucination | bịa (hallucination) | LLM đưa ra con số/sự kiện không có nguồn | 36 |
| event forecasting, resolution | dự báo sự kiện, resolve | câu hỏi có kết quả được xác định tại một ngày | 37 |
| Brier score | Brier score | Phụ lục D | 37 |

## 11. Nhân quả và ra quyết định

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| intervention, treatment | can thiệp | | 38 |
| counterfactual | phản thực tế (counterfactual) | điều sẽ xảy ra nếu không can thiệp | 38 |
| synthetic control | synthetic control | tổ hợp đơn vị đối chứng mô phỏng phản thực tế | 38 |
| placebo test | placebo test | chạy phương pháp ở nơi/lúc không có can thiệp — phải ra ~0 | 38 |
| confounding | gây nhiễu (confounding) | biến tác động cả nguyên nhân lẫn kết quả | 39 |
| DAG | DAG (đồ thị nhân quả) | | 39 |
| elasticity | độ co giãn | % thay đổi lượng khi giá đổi 1% | 39 |
| double machine learning | DoubleML | | 39 |
| scenario, what-if | kịch bản, what-if | | 39 |
| newsvendor problem | bài toán newsvendor | đặt hàng một kỳ, chọn quantile theo tỷ lệ chi phí thiếu/thừa | 40 |
| service level, safety stock | mức phục vụ, tồn kho an toàn | | 40 |

## 12. Production

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| pipeline | pipeline | chuỗi bước từ lấy dữ liệu tới xuất dự báo | 41 |
| reproducibility | tính tái lập | chạy lại ra đúng kết quả | 41 |
| lockfile | lockfile (`uv.lock`) | chốt chính xác phiên bản mọi thư viện | mọi buổi |
| schema validation | kiểm schema | chặn dữ liệu sai kiểu/đơn vị trước khi vào mô hình | 41 |
| backfill | backfill | chạy lại pipeline cho các ngày quá khứ | 41 |
| feature store | feature store | | 41 |
| batch / online serving | phục vụ theo lô / trực tuyến | | 42 |
| latency, p95 | độ trễ, p95 | | 42 |
| data drift / concept drift | drift dữ liệu / drift khái niệm | phân phối đầu vào đổi / quan hệ đầu vào–đầu ra đổi | 43 |
| monitoring, alert | giám sát, cảnh báo | | 43 |
| retraining policy | chính sách retrain | | 43 |
| runbook | runbook | hướng dẫn xử lý sự cố từng bước | 43 |
| model card, ADR | model card, ADR | tài liệu mô hình; bản ghi quyết định kiến trúc | 44 |

## 13. Xác suất thống kê

| Tiếng Anh | Viết trong khoá | Nghĩa | Buổi |
|---|---|---|---|
| random variable | biến ngẫu nhiên | | 2 |
| PDF / PMF / CDF | hàm mật độ / hàm khối xác suất / hàm phân phối tích luỹ | | 2 |
| quantile, median | quantile, trung vị | Phụ lục B | 2 |
| expectation, variance, skewness, kurtosis | kỳ vọng, phương sai, độ lệch, độ nhọn | | 2 |
| heavy tail | đuôi dày | | 2, 21 |
| overdispersion | phân tán thừa | phương sai lớn hơn trung bình (dữ liệu đếm) | 2, 19 |
| likelihood, MLE | likelihood, ước lượng hợp lý cực đại (MLE) | | 2 |
| central limit theorem | định lý giới hạn trung tâm (CLT) | | 2 |
| bootstrap, block bootstrap | bootstrap, block bootstrap | Phụ lục B | 2 |
| effective sample size | cỡ mẫu hiệu dụng | | 2 |
| scoring rule (proper / strictly proper) | scoring rule (proper) | thước đo mà dự báo trung thực đạt điểm tốt nhất | 25 |
| p-value, hypothesis test | p-value, kiểm định giả thuyết | | 2, 7 |

## Nguồn

Nghĩa của thuật ngữ thống nhất với các phụ lục A–D (mỗi phụ lục có nguồn riêng) và với:

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way*: <https://otexts.com/fpppy/>
- Gneiting, T. & Raftery, A.E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102, 359–378.
- Lộ trình khoá: `lo-trinh/lo-trinh-forecasting.md` (cột "Buổi" trỏ về buổi dạy khái niệm).
