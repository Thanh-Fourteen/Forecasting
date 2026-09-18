# Lộ trình Forecasting in AI — từ cơ bản đến nâng cao (44 buổi)

Lộ trình tự học hoặc dạy lớp, **6–8 giờ/buổi-tuần**, chia 9 giai đoạn. Đi từ "dự báo là gì" tới
foundation model, LLM dự báo sự kiện, suy luận nhân quả và vận hành hệ thống dự báo trong
production. Mỗi buổi có một phòng lab bắt buộc trên **dữ liệu thật** và một **tiêu chí
"Xong khi"** đo được — không đạt thì đừng qua buổi sau.

**Triết lý của khoá, theo thứ tự ưu tiên:**

1. **Hiểu dữ liệu trước, mô hình sau.** Giai đoạn 1 (10 buổi) chỉ dành cho đọc biểu đồ, phân
   rã, tương quan, làm sạch, ngoại lai, khử nhiễu và feature — dài hơn bất kỳ giai đoạn mô hình
   nào. Phần lớn dự báo tệ ngoài đời hỏng ở dữ liệu, không hỏng ở mô hình.
2. **Không tin con số chưa qua backtest.** Mọi mô hình từ buổi 14 trở đi đều phải thắng
   baseline (seasonal naive) trên cùng một bộ backtest cố định rồi mới được nói là "tốt".
3. **Dự báo phục vụ một quyết định.** Chỉ số đánh giá được chọn theo chi phí của quyết định
   đó, không chọn theo thói quen.
4. **Hiểu khái niệm tới tận gốc.** Mỗi khái niệm được giải thích bằng trực giác → công thức →
   code tự viết từ đầu → thư viện. Dùng thư viện mà không tự viết lại được bản đơn giản là
   chưa hiểu.
5. **Dự án phải thực tế.** Dữ liệu bẩn thật, baseline thật của doanh nghiệp để vượt qua, và
   dự án cuối được chấm trên **dữ liệu tương lai chưa tồn tại lúc nộp bài**.

**Mỗi buổi dùng bộ dữ liệu riêng hợp với bài** — không có một bộ dữ liệu xuyên suốt. Mỗi buổi
là một thư mục tự chứa: môi trường Python chốt phiên bản, script tải dữ liệu có kiểm sha256,
và dựng lại được từ số 0 trên máy trắng. Nghỉ một buổi hay vào lớp giữa chừng vẫn học được.

> Rà soát gần nhất: **2026-09-18** (Phase 3: buổi 4–8). Đối chiếu *Forecasting: Principles and Practice, the
> Pythonic Way* (2025), hệ sinh thái Nixtla, GIFT-Eval / fev-bench, ForecastBench (7/2026).
> Phiên bản thư viện dùng trong lab chốt ở `pyproject.toml` + `uv.lock` của từng buổi.
> Hệ sinh thái foundation model và LLM thay đổi rất nhanh — giai đoạn 5–6 rà lại mỗi 6 tháng.

---

## Mục lục

- [Yêu cầu đầu vào](#yêu-cầu-đầu-vào)
- [Môi trường lab](#môi-trường-lab)
- [Bảng tổng quan 44 buổi](#bảng-tổng-quan-44-buổi)
- [8 cột mốc năng lực](#8-cột-mốc-năng-lực)
- [Giai đoạn 0 — Nền móng (buổi 1–3)](#giai-đoạn-0--nền-móng-buổi-13)
- [Giai đoạn 1 — Hiểu và chuẩn bị dữ liệu (buổi 4–13)](#giai-đoạn-1--hiểu-và-chuẩn-bị-dữ-liệu-buổi-413)
- [Giai đoạn 2 — Thống kê cổ điển và đánh giá (buổi 14–21)](#giai-đoạn-2--thống-kê-cổ-điển-và-đánh-giá-buổi-1421)
- [Giai đoạn 3 — Machine learning (buổi 22–24)](#giai-đoạn-3--machine-learning-buổi-2224)
- [Giai đoạn 4 — Bất định (buổi 25–28)](#giai-đoạn-4--bất-định-buổi-2528)
- [Giai đoạn 5 — Deep learning (buổi 29–33)](#giai-đoạn-5--deep-learning-buổi-2933)
- [Giai đoạn 6 — Foundation model và LLM (buổi 34–37)](#giai-đoạn-6--foundation-model-và-llm-buổi-3437)
- [Giai đoạn 7 — Nhân quả và ra quyết định (buổi 38–40)](#giai-đoạn-7--nhân-quả-và-ra-quyết-định-buổi-3840)
- [Giai đoạn 8 — Production và MLOps (buổi 41–43)](#giai-đoạn-8--production-và-mlops-buổi-4143)
- [Buổi 44 — Dự án cuối](#buổi-44--dự-án-cuối)
- [Đối chiếu với sách FPP](#đối-chiếu-với-sách-fpp)
- [Checklist "đã giỏi chưa"](#checklist-đã-giỏi-chưa)
- [Sai lầm thường gặp](#sai-lầm-thường-gặp)
- [Tài nguyên](#tài-nguyên)
- [Học theo cụm](#học-theo-cụm)

---

## Yêu cầu đầu vào

| Cần có | Mức độ | Không có thì học ở đâu |
|---|---|---|
| Python | hàm, class, list/dict comprehension, đọc traceback | Phụ lục A + buổi 1 ôn nhanh |
| pandas cơ bản | đọc CSV, lọc, groupby, merge | Buổi 3 dạy lại theo góc nhìn thời gian |
| Toán phổ thông | hàm số, đạo hàm ở mức ý nghĩa, tổng Σ | Buổi 2 + Phụ lục B |
| Xác suất thống kê | trung bình, phương sai, phân phối chuẩn là gì | Buổi 2 dạy lại từ đầu, đủ dùng |
| Git + dòng lệnh | clone, commit, chạy script | Bắt buộc từ buổi 41 (pipeline) |

Không cần biết deep learning trước: buổi 29 dạy PyTorch ở mức đủ dùng. Không cần GPU: mọi lab
có nhánh chạy CPU. Buổi 36–37 cần gọi LLM — có nhánh model mở chạy local, không bắt buộc trả
tiền API.

## Môi trường lab

| Thành phần | Dùng cho | Ghi chú |
|---|---|---|
| **Python 3.12 + uv** | cả khoá | Mỗi buổi có `pyproject.toml` + `uv.lock` riêng; `make up` = `uv sync` + tải dữ liệu |
| **JupyterLab** | cả khoá | Code nguồn lưu dạng `.py` percent (jupytext) để diff được, notebook sinh ra từ đó |
| **Máy CPU 4 nhân, 16 GB RAM** | khuyến nghị | 8 GB đủ cho buổi 1–28 và 38–43; buổi 29–35 cần 16 GB (có cấu hình rút gọn cho máy 8 GB) |
| **30 GB đĩa trống** | cache dữ liệu | Dữ liệu tải về `~/.cache/khoa-forecasting/`, không nằm trong repo |
| GPU (tuỳ chọn) | buổi 29–35 | Không có GPU vẫn học đủ: model nhỏ, epoch ít, foundation model bản nhỏ chạy CPU |
| API key LLM (tuỳ chọn) | buổi 36–37 | Nhánh miễn phí: model mở chạy bằng Ollama/llama.cpp. Có API thì đặt trần chi phí < 5 USD/buổi |
| API key dữ liệu (miễn phí) | buổi 10, 41–44 | OpenAQ, EIA — đăng ký miễn phí, hướng dẫn trong `MOI-TRUONG.md` |
| Docker | buổi 41–43 | Đóng gói pipeline và API dự báo |

Thư viện chính, cài theo buổi (không cài một lần cho cả khoá):

```text
pandas, polars, duckdb            dữ liệu              — buổi 3
matplotlib, seaborn, plotly       biểu đồ              — buổi 4
statsmodels, scipy                thống kê, lọc        — buổi 5
statsforecast, utilsforecast      mô hình thống kê     — buổi 14
ruptures, PyWavelets              điểm gãy, wavelet    — buổi 11, 12
mlforecast, lightgbm, optuna      machine learning     — buổi 22
MAPIE                             conformal            — buổi 26
pymc, pymc-extras                 Bayes                — buổi 27
hierarchicalforecast              phân cấp             — buổi 28
torch, neuralforecast             deep learning        — buổi 29
chronos-forecasting, timesfm      foundation model     — buổi 34
autogluon.timeseries              AutoML               — buổi 24
pandera, prefect, mlflow          production           — buổi 41
```

> *Rà 2026-09-17:* pandas 3.0 đã phát hành (01/2026) nhưng statsforecast, utilsforecast, mlforecast
> và autogluon.timeseries bản mới nhất **chưa hỗ trợ pandas 3**. Buổi 1–13 dùng pandas 3; buổi dùng
> hệ Nixtla/AutoGluon tự được chốt pandas 2.3.3 (luật `[[rang_buoc]]` trong `tools/nen/phien-ban.toml`).
> Học viên cần biết khác biệt hai bản — Phụ lục A, mục "pandas 2 và pandas 3".

## Bảng tổng quan 44 buổi

| Buổi | Chủ đề | Sản phẩm của buổi |
|---|---|---|
| 1 | Forecasting là gì | Bản mô tả bài toán dự báo: quyết định, tầm, độ chi tiết, chi phí sai |
| 2 | Xác suất và thống kê cho dự báo | Tự viết bootstrap + quantile, giải thích được khoảng tin cậy |
| 3 | Dữ liệu thời gian với pandas, polars, DuckDB | Bảng dữ liệu dạng dài sạch múi giờ, đúng tần suất |
| 4 | Đọc và vẽ biểu đồ chuỗi thời gian | Bộ 8 biểu đồ chẩn đoán + đọc ra 5 nhận xét có bằng chứng |
| 5 | Biến đổi và điều chỉnh | Chuỗi đã điều chỉnh lịch/lạm phát, Box-Cox có hiệu chỉnh bias |
| 6 | Phân rã | MSTL tách đúng mùa vụ ngày và tuần của tải điện |
| 7 | Tự tương quan và tính dừng | Kết luận dừng/không dừng bằng ADF + KPSS + ACF |
| 8 | Tương quan giữa các chuỗi | Phân biệt tương quan thật và giả, tìm độ trễ dẫn dắt |
| 9 | Đặc trưng chuỗi và khả năng dự báo | Bản đồ 1.000 chuỗi theo độ khó dự báo |
| 10 | Làm sạch và dữ liệu thiếu | Pipeline làm sạch cảm biến có test |
| 11 | Ngoại lai và điểm gãy | Phát hiện COVID là điểm gãy, không xoá nhầm Tết |
| 12 | Khử nhiễu và miền tần số | So 6 bộ lọc, chứng minh bộ nào rò tương lai |
| 13 | Feature engineering và chống rò rỉ | Bộ feature có lễ âm lịch, qua bài kiểm leakage tự động |
| 14 | Baseline và chỉ số đánh giá | Bảng baseline + chỉ số chọn theo quyết định |
| 15 | Backtesting đúng cách | Bộ backtest rolling origin tái sử dụng được |
| 16 | Exponential smoothing và Theta | AutoETS thắng seasonal naive có kiểm định |
| 17 | ARIMA và SARIMA | Tự xác định bậc từ ACF/PACF, khớp auto-ARIMA |
| 18 | Hồi quy chuỗi thời gian và hồi quy động | Mô hình tải điện theo nhiệt độ có sai số ARIMA |
| 19 | Nhu cầu gián đoạn | Dự báo phụ tùng thưa, đo bằng chi phí tồn kho |
| 20 | Đa biến, state space, nowcasting | Nowcast GDP quý từ dữ liệu tháng |
| 21 | Chuỗi tài chính và biến động | GARCH dự báo biến động; chứng minh "LSTM đoán giá 99%" là ảo |
| 22 | Biến dự báo thành bài toán hồi quy | Mô hình global cho 10.000 chuỗi, 3 chiến lược đa bước |
| 23 | Gradient boosting chuyên sâu | LightGBM kiểu M5 có Tweedie + SHAP |
| 24 | Ensemble, AutoML và ca khó | Ensemble thắng mô hình tốt nhất đơn lẻ; xử lý cold start |
| 25 | Dự báo xác suất | Dự báo quantile được chấm bằng pinball + CRPS + PIT |
| 26 | Conformal prediction | Khoảng dự báo giữ coverage 90% khi có drift |
| 27 | Dự báo Bayes và Gaussian Process | Mô hình phân cấp Bayes cho chuỗi thưa |
| 28 | Dự báo phân cấp | Dự báo cộng khớp từ cửa hàng tới toàn công ty |
| 29 | Nền deep learning cho chuỗi | Tự viết LSTM/TCN, thắng/thua baseline được giải thích |
| 30 | N-BEATS, N-HiTS, DeepAR, TFT, TiDE | So 5 kiến trúc trên cùng backtest |
| 31 | Transformer cho chuỗi thời gian | Tái hiện tranh cãi DLinear vs Transformer |
| 32 | Mô hình sinh và dữ liệu tổng hợp | Sinh sample path; kiểm dữ liệu tổng hợp không chép nguyên |
| 33 | Không gian–thời gian và thời tiết AI | GNN giao thông; kiểm chứng AIFS với trạm Nội Bài |
| 34 | Time series foundation model | Chronos-2 / TimesFM zero-shot so với mô hình đã học |
| 35 | Fine-tune, covariates, đọc benchmark | Biết khi nào foundation model thua LightGBM |
| 36 | LLM và agent trong pipeline | Agent dự báo có guardrail, không bịa số |
| 37 | Dự báo sự kiện bằng LLM | Bot dự báo câu hỏi nhị phân, Brier score sạch rò rỉ |
| 38 | Đo tác động của can thiệp | Đo hiệu quả chiến dịch bằng CausalImpact + synthetic control |
| 39 | Kịch bản và what-if | Ước lượng độ co giãn giá đúng dấu |
| 40 | Từ dự báo đến quyết định | Chính sách đặt hàng từ quantile, đo bằng tiền |
| 41 | Pipeline dự báo tái lập | Pipeline point-in-time, chạy lại ra đúng kết quả |
| 42 | Phục vụ ở quy mô lớn | Dự báo 150.000 chuỗi < 15 phút + API |
| 43 | Giám sát, drift và retrain | Giám sát bắt được đổi đơn vị trong 1 ngày |
| 44 | Dự án cuối | Hệ thống dự báo thực tế, chấm trên dữ liệu tương lai |

## 8 cột mốc năng lực

Không có dự án xuyên suốt, nên cột mốc đo **năng lực** chứ không đo trạng thái của một app.

| Cột mốc | Sau buổi | Làm được gì |
|---|---|---|
| M0 | 3 | Biến một file dữ liệu thô bất kỳ thành bảng thời gian sạch, đúng múi giờ, đúng tần suất |
| M1 | 13 | Nhận một bộ dữ liệu bẩn lạ, trong 1 ngày ra báo cáo EDA + pipeline làm sạch có test — **dự án giữa chặng 1** |
| M2 | 21 | Dựng bậc thang mô hình thống kê trên backtest chuẩn, chọn chỉ số theo quyết định |
| M3 | 24 | Dự báo hàng nghìn chuỗi bằng ML, thắng thống kê có kiểm định — **dự án giữa chặng 2** |
| M4 | 28 | Mọi dự báo đều có khoảng tin cậy đã calibrate, cộng khớp giữa các cấp |
| M5 | 33 | Chọn đúng kiến trúc deep learning và biết khi nào nó không đáng |
| M6 | 37 | Dùng foundation model và LLM có kiểm chứng, không bị benchmark hay rò rỉ thời gian đánh lừa |
| M7 | 43 | Đưa dự báo vào quyết định có giá trị tiền, vận hành tái lập + giám sát trong production |

---

## Giai đoạn 0 — Nền móng (buổi 1–3)

### Buổi 1 — Forecasting là gì

**Mục tiêu:** trước khi mở dữ liệu, viết được bài toán dự báo thành lời: dự báo cái gì, cho
quyết định nào, trước bao lâu, chi tiết tới đâu, và sai thì mất gì.

**Học:**
- Dự báo ≠ mục tiêu ≠ kế hoạch. Dự báo là "điều gì *sẽ* xảy ra nếu không ai can thiệp thêm"
- Các chiều của bài toán: **tầm dự báo** (horizon), **độ chi tiết** (granularity: SKU × cửa hàng × ngày),
  **tần suất cập nhật**, **thời điểm cắt dữ liệu** (lúc ra dự báo biết những gì)
- Cái gì dự báo được, cái gì không: hiểu rõ các yếu tố tác động, có đủ dữ liệu, dự báo có làm
  thay đổi chính thứ được dự báo không (giá cổ phiếu vs tải điện)
- Dự báo điểm, dự báo khoảng, dự báo phân phối — và vì sao quyết định cần cái thứ ba
- Chi phí sai số bất đối xứng: thiếu hàng vs tồn kho, dự báo thiếu tải vs thừa tải
- Bản đồ các cách tiếp cận: phán đoán, thống kê, ML, deep learning, foundation model, LLM
- Lịch sử các cuộc thi M1 → M6 và bài học lớn nhất của mỗi lần (mô hình đơn giản thường thắng;
  kết hợp mô hình thắng; ML thắng khi có nhiều chuỗi liên quan)
- Môi trường: uv, JupyterLab, cấu trúc một buổi học, `make up / check / down`

**Lab:**
1. Cài môi trường bằng `uv sync`, mở JupyterLab, chạy notebook kiểm tra phiên bản
2. Tải dữ liệu tiêu thụ điện hộ gia đình, vẽ một đường duy nhất, liệt kê 5 câu hỏi về dữ liệu
3. Viết "phiếu bài toán dự báo" cho 3 tình huống: chuỗi cà phê đặt nguyên liệu, EVN điều độ
   ngày mai, bệnh viện xếp lịch trực Tết
4. Đoán nhanh tiêu thụ tuần tới bằng mắt, rồi so với "ngày này tuần trước" — ghi con số
5. Cố tình đánh giá một dự báo trên chính dữ liệu đã dùng để làm nó, thấy sai số "đẹp" giả tạo

**Dữ liệu:** UCI Individual Household Electric Power Consumption (CC BY 4.0).

**Xong khi:** viết được phiếu bài toán cho một tình huống lạ trong 15 phút, đủ 6 ô: quyết
định, biến mục tiêu, tầm, độ chi tiết, thời điểm cắt dữ liệu, chi phí sai hai chiều.

### Buổi 2 — Xác suất và thống kê cho dự báo

**Mục tiêu:** hiểu đủ xác suất để đọc mọi buổi sau mà không phải tin công thức một cách mù quáng.

**Học:**
- Biến ngẫu nhiên, phân phối, hàm mật độ vs hàm phân phối tích luỹ (CDF), **quantile**
- Kỳ vọng, phương sai, độ lệch, độ nhọn; vì sao trung bình và trung vị là câu trả lời cho
  hai câu hỏi khác nhau (tối thiểu hoá bình phương sai số vs trị tuyệt đối sai số)
- Các phân phối hay gặp: chuẩn, log-chuẩn, Poisson, âm nhị thức (dữ liệu đếm), Student-t (đuôi dày)
- Likelihood và ước lượng hợp lý cực đại (MLE) — nền của ETS, ARIMA, DeepAR
- Luật số lớn, định lý giới hạn trung tâm — và khi nào chúng **không** cứu được bạn (đuôi dày, phụ thuộc)
- Khoảng tin cậy vs khoảng dự báo (khoảng dự báo luôn rộng hơn — vì sao)
- Bootstrap: ước lượng bất định không cần công thức; block bootstrap cho dữ liệu phụ thuộc thời gian
- Hồi quy tuyến tính OLS: giả định, phần dư, R² và vì sao R² cao chưa nói gì về dự báo

**Lab:**
1. Vẽ histogram số lượt thuê xe theo giờ, thử khớp chuẩn / Poisson / âm nhị thức, so bằng QQ-plot
2. Tự viết hàm quantile và bootstrap bằng NumPy, so với `np.quantile` và `scipy.stats.bootstrap`
3. Lấy mẫu i.i.d. vs mẫu có tự tương quan: bootstrap thường cho khoảng hẹp sai, block bootstrap sửa được
4. Tính khoảng 95% bằng "trung bình ± 1.96σ" cho dữ liệu lệch phải, đếm tỷ lệ phủ thật **trong mẫu và trên năm sau**
   — tách hai nguyên nhân: hình dạng sai (đuôi lệch, cận dưới âm) và phân phối dịch chuyển (số lượt thuê 2012 tăng)

**Dữ liệu:** UCI Bike Sharing Dataset (CC BY 4.0).

**Xong khi:** giải thích được bằng số vì sao khoảng "±1.96σ" theo từng giờ dựng từ 2011 chỉ phủ ~73% trên 2012
thay vì 95% (dịch chuyển mức là chính; quantile thực nghiệm sửa hình dạng đuôi nhưng không sửa được dịch chuyển), và vì
sao khoảng tin cậy bootstrap i.i.d. cho trung bình quá hẹp trên chuỗi tự tương quan (block bootstrap sửa được).

### Buổi 3 — Dữ liệu thời gian với pandas, polars, DuckDB

**Mục tiêu:** xử lý thời gian đúng — nguồn gây lỗi âm thầm số một trong dự báo.

**Học:**
- `Timestamp`, `DatetimeIndex`, `Period`; tần suất (`h`, `D`, `W-MON`, `MS`, `QE`)
- **Múi giờ và DST**: naive vs aware, UTC làm chuẩn lưu trữ, `Asia/Ho_Chi_Minh` không có DST
  nhưng dữ liệu châu Âu/Mỹ có — giờ bị lặp và giờ bị mất
- Nhãn khoảng thời gian: giá trị 10:00 là của 9:00–10:00 hay 10:00–11:00? (`label`, `closed`)
- `resample` (tăng/giảm tần suất, tổng hay trung bình tuỳ loại biến: lưu lượng vs trạng thái)
- `rolling`, `expanding`, `ewm`, `shift`, `diff` — và hướng thời gian của từng hàm
- Ghép dữ liệu khác tần suất: `merge_asof` (lấy giá trị **gần nhất trong quá khứ**)
- Chuỗi không đều (irregular) và dữ liệu sự kiện → chuỗi đều
- **Định dạng dài** `unique_id, ds, y` (chuẩn của Nixtla) vs định dạng rộng
- polars (lazy, nhanh) và DuckDB (SQL trên file Parquet) cho dữ liệu vượt RAM

**Lab:**
1. Đọc dữ liệu chuyến taxi NYC 1 tháng (vài triệu dòng) bằng pandas, polars, DuckDB — bấm giờ
2. Gộp thành số chuyến theo giờ; tìm 2 ngày đổi DST và giải thích giờ bị thiếu/lặp
3. Ghép thời tiết Open-Meteo theo giờ — lần đầu cố tình lệch múi giờ, thấy mưa "gây ra" tăng
   chuyến 5 giờ trước khi mưa
4. Chuyển về định dạng dài cho 263 khu vực, kiểm tra mỗi chuỗi đủ mốc thời gian

**Dữ liệu:** NYC TLC Trip Record Data (NYC Open Data), Open-Meteo Historical Weather API (CC BY 4.0).

**Xong khi:** một hàm `chuan_hoa_thoi_gian()` nhận dữ liệu thô bất kỳ, trả về bảng dạng dài
UTC, đủ mốc, không trùng — qua 6 test có sẵn (DST, trùng lặp, lệch múi giờ, thiếu mốc…).
**Cột mốc M0.**

---

## Giai đoạn 1 — Hiểu và chuẩn bị dữ liệu (buổi 4–13)

Giai đoạn dài nhất của khoá, và là giai đoạn quan trọng nhất. Người học bỏ qua giai đoạn này
thường dựng được mô hình phức tạp nhưng không biết vì sao nó sai.

Mọi buổi trong giai đoạn này theo cùng một nhịp: **nhìn → đặt giả thuyết → kiểm bằng con số
→ quyết định xử lý → kiểm lại rằng xử lý không làm hỏng thứ khác.**

### Buổi 4 — Đọc và vẽ biểu đồ chuỗi thời gian

**Mục tiêu:** nhìn một biểu đồ và nói ra được xu hướng, mùa vụ, chu kỳ, điểm gãy, ngoại lai,
thay đổi phương sai — mỗi nhận xét chỉ được vào một bằng chứng trên hình.

**Học:**
- **Xu hướng, mùa vụ, chu kỳ** khác nhau thế nào (mùa vụ: chu kỳ cố định theo lịch; chu kỳ: dài
  ngắn thất thường, như chu kỳ kinh tế)
- Biểu đồ đường: tỉ lệ khung hình, **trục y có cắt hay không**, thang log khi biến động tỉ lệ với mức
- **Seasonal plot** (mỗi năm/tuần một đường chồng lên nhau) và **subseries plot** (tách theo tháng/thứ)
- **Lag plot**: nhìn tự tương quan bằng mắt trước khi tính ACF
- **Heatmap lịch** (giờ × thứ, ngày × tháng) — phát hiện mẫu hình đa mùa vụ
- Boxplot / violin theo giờ, thứ, tháng — nhìn phân phối chứ không chỉ trung bình
- Scatter có màu theo thời gian: quan hệ hai biến thay đổi theo năm
- Small multiples cho nhiều chuỗi; khi nào dùng plotly tương tác, khi nào hình tĩnh
- **Bẫy biểu đồ**: trục kép gây hiểu nhầm tương quan, làm trơn che mất ngoại lai, gộp tần suất
  che mùa vụ, trục y cắt phóng đại biến động
- Nguyên tắc: tiêu đề nói kết luận, không nói tên biến

**Lab:**
1. Vẽ bộ 8 biểu đồ chẩn đoán cho lượt thuê xe theo giờ: đường, seasonal (tuần), subseries
   (tháng), lag, heatmap giờ×thứ, boxplot theo giờ tách ngày làm việc/nghỉ, scatter nhiệt
   độ×lượt thuê tô màu theo năm, ACF nhanh
2. Viết 5 nhận xét, mỗi nhận xét kèm "nhìn thấy ở hình nào, chỗ nào"
3. Nhận một biểu đồ "gây hiểu nhầm" dựng sẵn (trục kép + trục y cắt), vẽ lại cho trung thực
4. Viết hàm `bo_bieu_do_chan_doan(df)` dùng lại cho các buổi sau

**Dữ liệu:** UCI Bike Sharing Dataset — theo giờ (CC BY 4.0).

**Xong khi:** nhận một chuỗi lạ, trong 20 phút nộp bộ biểu đồ + 5 nhận xét có bằng chứng, và
phát hiện được mùa vụ kép (ngày + tuần) mà biểu đồ đường thô che mất.

### Buổi 5 — Biến đổi và điều chỉnh dữ liệu

**Mục tiêu:** loại bỏ những biến động đã biết nguyên nhân trước khi mô hình phải tự học chúng.

**Học:**
- **Điều chỉnh lịch**: tháng 2 ít ngày hơn tháng 3 — chia cho số ngày, số ngày làm việc,
  số ngày giao dịch
- **Điều chỉnh dân số**: tổng vs bình quân đầu người
- **Điều chỉnh lạm phát**: giá danh nghĩa vs giá thực, chỉ số CPI, chọn năm gốc
- **Biến đổi toán học**: log, căn, **Box-Cox** (chọn λ bằng Guerrero), Yeo-Johnson khi có số 0/âm
- Vì sao log ổn định phương sai khi biến động tỉ lệ với mức
- **Bias khi biến đổi ngược**: `exp(E[log y]) ≠ E[y]` — dự báo trung bình bị thấp có hệ thống;
  công thức hiệu chỉnh
- **Sai phân** thường và sai phân mùa vụ — biến đổi để làm chuỗi dừng (nối sang buổi 7)
- Chuẩn hoá theo từng chuỗi (z-score, min-max, chia trung bình) khi gộp nhiều chuỗi — nối sang buổi 22

**Lab:**
1. Doanh thu bán lẻ Mỹ theo tháng: so tháng 2 với tháng 3 trước/sau điều chỉnh số ngày
2. Chuyển sang giá thực bằng CPI, vẽ lại — xu hướng "tăng mạnh" còn bao nhiêu
3. Chọn λ Box-Cox, dự báo seasonal naive trên thang biến đổi, đổi ngược có và không hiệu chỉnh
   bias — đo chênh lệch trung bình dự báo
4. Tự viết Box-Cox và đổi ngược, so với `scipy.stats.boxcox`

**Dữ liệu:** lấy từ **cơ quan gốc**, không qua FRED (điều khoản FRED cấm dùng cho machine learning —
Phụ lục F): CPI-U (BLS, public domain), dân số Mỹ theo tháng (BEA NIPA, public domain), doanh số bán lẻ
(US Census MARTS `mrtssales92-present.xlsx` — census.gov chặn IP Việt Nam (403) và API cần key, nên lấy **bản lưu Wayback
Machine đã chốt sha256**, public domain theo 17 U.S.C. §105; dự phòng: UCI Online Retail II).

**Xong khi:** đo được dự báo sau log–exp thấp hơn thực tế bao nhiêu phần trăm, sửa bằng hiệu
chỉnh bias và chứng minh bằng số trên tập kiểm tra.

### Buổi 6 — Phân rã chuỗi thời gian

**Mục tiêu:** tách chuỗi thành xu hướng + mùa vụ + phần dư, và đọc được từng phần.

**Học:**
- Mô hình cộng `y = T + S + R` vs nhân `y = T × S × R`; log biến nhân thành cộng
- Trung bình trượt để ước lượng xu hướng (MA bậc chẵn cần centering 2×m-MA)
- **Classical decomposition** và các điểm yếu: mất đầu/cuối chuỗi, mùa vụ cố định, nhạy ngoại lai
- X-11 / X-13ARIMA-SEATS (chuẩn của cơ quan thống kê — nhắc để biết)
- **STL**: LOESS, tham số `seasonal`/`trend` window, robust với ngoại lai
- **MSTL** cho nhiều mùa vụ (ngày + tuần + năm)
- **Độ mạnh xu hướng** và **độ mạnh mùa vụ** $F_T, F_S \in [0,1]$ — đo được, không cảm tính
- Chuỗi đã khử mùa vụ (seasonally adjusted) — dùng khi nào, không dùng khi nào
- Phần dư là nơi tìm ngoại lai và điểm gãy (nối sang buổi 11)

**Lab:**
1. Tải điện theo giờ của một vùng điều độ: classical decomposition với chu kỳ 24 — nhịp tuần
   "trốn" vào **xu hướng** (xu hướng lõm mỗi cuối tuần) và một phần vào phần dư, còn mùa vụ ngày
   bị ép cố định cả năm nên phần dư mang mẫu hình tháng × giờ; thấy trên heatmap phần dư
   *(Phase 3 đo trên PJM 2024: phần dư cổ điển còn 10% phương sai ở hồ sơ tháng×giờ, MSTL 0,06%)*
2. MSTL với chu kỳ (24, 168): phần dư sạch hẳn, tính lại $F_S$ cho từng mùa vụ
3. So STL robust vs không robust khi có **một giờ số liệu hỏng** (PJM 21/11/2024: 56 GW giữa hai giờ 95 GW);
   đợt nắng nóng nhiều ngày làm phản ví dụ — xu hướng hấp thụ phần lớn, robust giúp ít
4. Vẽ mùa vụ ngày theo từng tháng: biên độ đổi theo mùa hè/đông → mùa vụ biến thiên theo thời gian

**Dữ liệu:** EIA-930 Hourly Electric Grid Monitor — nhu cầu điện theo giờ của một balancing
authority (US EIA, public domain).

**Xong khi:** phân rã đúng một chuỗi có ≥ 2 mùa vụ, phần dư không còn mẫu hình mùa vụ (kiểm bằng
ACF phần dư), và báo được $F_T$, $F_S$ kèm diễn giải.

### Buổi 7 — Tự tương quan và tính dừng

**Mục tiêu:** hiểu "quá khứ nói gì về tương lai" bằng con số, và biết khi nào một chuỗi đủ ổn
định để mô hình hoá.

**Học:**
- **Hiệp phương sai và tự tương quan** ở độ trễ k; tự tính ACF bằng tay
- **ACF**: đọc xu hướng (giảm chậm), mùa vụ (đỉnh ở bội số của m), nhiễu trắng (trong dải ±1.96/√T)
- **PACF**: tương quan ở độ trễ k sau khi đã loại ảnh hưởng của các độ trễ ngắn hơn
- **Nhiễu trắng**; kiểm định **Ljung-Box** (và vì sao nhìn 20 cột ACF thế nào cũng có 1 cột vượt dải)
- **Tính dừng**: dừng mạnh vs dừng yếu; xu hướng, mùa vụ, phương sai đổi đều làm mất tính dừng
- **Random walk** — chuỗi không dừng kinh điển; vì sao naive là dự báo tối ưu cho nó
- Nghiệm đơn vị; **ADF** (H0: có nghiệm đơn vị) vs **KPSS** (H0: dừng) — dùng cả hai và đọc 4 tổ hợp kết quả
- Trend-stationary vs difference-stationary — xử lý khác nhau
- Sai phân bao nhiêu lần là đủ; sai phân thừa gây hại gì
- Tính ergodic ở mức trực giác: vì sao một chuỗi dài thay được nhiều lần lặp thí nghiệm

**Lab:**
1. Tự viết hàm ACF bằng NumPy, so với `statsmodels.tsa.acf`
2. Sinh 4 chuỗi mô phỏng (nhiễu trắng, AR(1), random walk, xu hướng tất định), đọc ACF/PACF,
   chạy ADF + KPSS, điền bảng 4×4
3. Áp lên chuỗi kinh tế thật: GDP thực, chỉ số sản lượng công nghiệp, lượt thuê xe — quyết định số lần sai phân
4. Ljung-Box trên phần dư phân rã của buổi trước

**Dữ liệu:** GDP thực (BEA NIPA, public domain); chỉ số sản lượng công nghiệp (Federal Reserve G.17, public
domain — thay tỷ lệ thất nghiệp BLS vì BLS chỉ phát hành trong tệp 390 MB hoặc API giới hạn 10 năm/lần);
UCI Bike Sharing (CC BY 4.0).

**Xong khi:** với một chuỗi lạ, đưa ra kết luận dừng/không dừng và số lần sai phân, dựa trên
**cả ba** bằng chứng (ACF, ADF, KPSS), giải thích được khi hai kiểm định mâu thuẫn nhau.

### Buổi 8 — Tương quan giữa các chuỗi

**Mục tiêu:** tìm biến giải thích có giá trị dự báo thật — và không bị lừa bởi tương quan giả.

**Học:**
- **Pearson** (tuyến tính), **Spearman** (đơn điệu, theo hạng), **Kendall** — chọn cái nào khi nào
- **Anscombe's quartet** và vì sao luôn vẽ scatter trước khi tin hệ số
- Tương quan phi tuyến: nhiệt độ vs tải điện hình chữ U (sưởi + điều hoà)
- **Mutual information** bắt được quan hệ phi tuyến mà Pearson bỏ sót
- **Tương quan giả (spurious correlation)**: hai chuỗi cùng có xu hướng luôn "tương quan cao";
  hồi quy giả của Granger–Newbold
- Xử lý: sai phân, khử xu hướng, **prewhitening** (lọc một chuỗi bằng mô hình ARIMA của nó rồi
  mới tính tương quan chéo)
- **Hàm tương quan chéo (CCF)**: tìm độ trễ dẫn dắt (lead-lag) — biến nào đi trước bao lâu
- Tương quan trượt theo cửa sổ: quan hệ có ổn định theo thời gian không
- Ma trận tương quan nhiều biến + heatmap, **đa cộng tuyến** (VIF)
- **Granger causality**: "quá khứ X giúp dự báo Y" — **không phải nhân quả**; ví dụ phản chứng
- Tương quan một phần (partial correlation) — kiểm soát biến thứ ba (mùa vụ là biến gây nhiễu kinh điển)
- Tương quan ≠ giá trị dự báo: biến tương quan cao nhưng không biết trước giá trị tương lai thì vô dụng

**Lab:**
1. Hai chuỗi kinh tế không liên quan có xu hướng (CPI-U của BLS × dân số Mỹ của BEA): tương quan 0.9+ →
   sai phân → gần 0; kèm mô phỏng Granger–Newbold (random walk không drift hiếm khi đạt 0.9 — cần drift)
2. Tải điện × nhiệt độ theo giờ: Pearson thấp, scatter hình chữ U, mutual information cao —
   tách thành "độ nóng" (CDD) và "độ lạnh" (HDD), tương quan tăng vọt
3. CCF giữa nhiệt độ và tải điện **trước và sau prewhitening** — độ trễ thật lộ ra
4. Tương quan trượt 90 ngày: quan hệ nhiệt độ–tải đổi dấu giữa mùa đông và hè
5. Granger test theo hai chiều; dựng một ví dụ Granger "có ý nghĩa" nhưng rõ ràng không nhân quả

**Dữ liệu:** EIA-930 vùng ERCOT (public domain), Open-Meteo Historical Weather Dallas + Houston 2024 (CC BY 4.0,
tác giả tải một lần và mirror), chuỗi kinh tế Mỹ từ BEA/BLS (public domain).

**Xong khi:** với một cặp chuỗi lạ, trả lời được đủ 4 câu kèm số liệu: tương quan có giả
không, quan hệ tuyến tính hay phi tuyến, độ trễ dẫn dắt là bao nhiêu, và biến đó có dùng được
để dự báo không (có biết trước giá trị tương lai không).

### Buổi 9 — Đặc trưng chuỗi và khả năng dự báo

**Mục tiêu:** trước khi dự báo 10.000 chuỗi, biết chuỗi nào dễ, chuỗi nào không thể — để
không tốn công tune những chuỗi vô vọng.

**Học:**
- **Đặc trưng chuỗi (time series features)**: độ mạnh xu hướng/mùa vụ, ACF bậc 1, độ lệch,
  entropy, tỷ lệ số 0, độ dài, số điểm gãy — bộ tsfeatures/catch22 (catch22 chọn 22 đặc trưng từ **4.791**
  đặc trưng hctsa đã lọc, không phải 7.658 như nhiều bài viết chép lại)
- **Khả năng dự báo (forecastability)**: spectral entropy, hệ số biến thiên, predictability score;
  so với lỗi thật của seasonal naive
- Vì sao có chuỗi không thể dự báo tốt hơn naive dù dùng mô hình gì
- **Không gian đặc trưng**: PCA/UMAP của hàng nghìn chuỗi, nhìn cả "vũ trụ" dữ liệu trên một hình
- **Phân cụm chuỗi**: theo đặc trưng vs theo hình dạng (DTW, k-shape) — ưu nhược điểm
- **Phân tầng ABC–XYZ** (giá trị × độ biến động) — cách doanh nghiệp chia chiến lược dự báo
- Phát hiện chuỗi "lạ" trong tập: chuỗi hằng, chuỗi bị cắt, chuỗi nhân đôi
- Ý tưởng chọn mô hình theo đặc trưng (FFORMA) — nối sang buổi 24

**Lab:**
1. Trích 20 đặc trưng (tự viết bằng NumPy/statsmodels) cho 4.000 chuỗi M4 theo tháng; cắt mọi chuỗi về
   cùng độ dài đuôi trước khi trích — độ dài 60–2.812 làm nhiều đặc trưng lệch (entropy × độ dài r = −0,20)
2. PCA về 2 chiều, tô màu theo từng đặc trưng — tìm vùng "dễ" và vùng "khó"
3. Tính spectral entropy, so với **sMAPE** của seasonal naive trên từng chuỗi: tương quan bao nhiêu
   *(Phase 4 đo trên 4.000 chuỗi M4 tháng, seed 42: entropy × sMAPE(snaive) ρ = +0,33; nhưng entropy ×
   **MASE**(snaive) ρ = −0,03 vì MASE chuẩn hoá đúng bằng sai số của chính seasonal naive → dùng MASE ở đây
   là chỗ hở cố ý, và đổi thang chuẩn hoá sang naive-1 làm **đảo dấu** tương quan, ρ = −0,52)*
4. Phân cụm bằng DTW trên 300 chuỗi, vẽ chuỗi đại diện mỗi cụm
5. Phân tầng ABC–XYZ cho dữ liệu bán lẻ, đề xuất chiến lược cho từng ô

**Dữ liệu:** M4 competition qua Monash Time Series Forecasting Repository (CC BY 4.0);
UCI Online Retail II (CC BY 4.0).

**Xong khi:** nộp bản đồ tập dữ liệu + bảng "chuỗi nào đáng đầu tư mô hình, chuỗi nào dùng
baseline", có số liệu chứng minh chuỗi entropy cao không thắng được naive.

### Buổi 10 — Làm sạch và dữ liệu thiếu

**Mục tiêu:** biến dữ liệu cảm biến bẩn thật thành chuỗi dùng được, và **ghi lại** mọi quyết
định làm sạch để kiểm tra được.

**Học:**
- **Hai loại thiếu**: thiếu mốc thời gian (không có dòng) vs có dòng nhưng giá trị rỗng —
  và bẫy thứ ba: **giá trị 0 thật hay 0 do mất tín hiệu**
- Cơ chế thiếu: **MCAR, MAR, MNAR** — cảm biến tắt khi ô nhiễm quá cao là MNAR, điền kiểu gì cũng lệch
- **Nhu cầu bị kiểm duyệt** (censored demand): ngày hết hàng doanh số = 0 không phải nhu cầu = 0
- Kiểm tra chất lượng: dải giá trị hợp lệ, giá trị đứng yên (stuck sensor), nhảy bậc vô lý,
  trùng lặp, đổi đơn vị (µg/m³ vs ppb), đổi múi giờ giữa chừng
- **Điền dữ liệu**: tiến/lùi (ffill/bfill), tuyến tính, spline, **theo mùa vụ** (lấy giá trị cùng
  giờ ngày trước/tuần trước), STL + nội suy, **Kalman smoother** (state space)
- Điền bằng deep learning (SAITS, BRITS qua PyPOTS) — khi nào đáng dùng
- Điền dữ liệu dùng tương lai (bfill, nội suy hai phía) — **rò rỉ** nếu làm trước khi chia tập
- Đánh giá phương pháp điền: **che nhân tạo** những đoạn biết đáp án rồi đo sai số
- Khoảng trống dài: đừng điền, hãy đánh dấu và để mô hình biết
- Cột cờ (flag) `da_dien`, `nghi_ngo` — dữ liệu sạch phải truy vết được

**Lab:**
1. Dữ liệu PM2.5 12 trạm Bắc Kinh: thống kê tỷ lệ thiếu theo trạm/giờ, heatmap lỗ hổng
2. Trạm khí tượng Nội Bài (NOAA GHCNh, dữ liệu Việt Nam thật): thiếu **mốc** (249 ô 30 phút trong 2024),
   cột 100% rỗng, cờ chất lượng 1/2/4, giá trị trần trá hình (visibility 9.999 = "≥10 km", RH 100),
   cảm biến đứng yên 33,5 giờ ở 26,0 °C; ghép với Open-Meteo Hà Nội làm "trạm hàng xóm" (r = 0,975)
3. Che ngẫu nhiên 10% và che nguyên khối 48 giờ; so 6 phương pháp điền trên hai kiểu che
4. Viết `lam_sach.py` + test pytest cho từng quy tắc; sinh báo cáo chất lượng dữ liệu

**Dữ liệu:** UCI Beijing Multi-Site Air-Quality (CC BY 4.0); **NOAA GHCNh trạm Nội Bài VMI0000VVNB**
(CC0, đã xác minh 2026-09-18: metadata NOAA ghi CC0-1.0, tài liệu GHCNh không có điều khoản WMO Res 40);
Open-Meteo Hà Nội 2023–2024 (CC BY 4.0). *Rà 2026-09-18:* **OpenAQ v3 bắt buộc API key cho MỌI endpoint**
(kể cả `/v3/licenses`), v2 đã ngừng (HTTP 410) → bỏ OpenAQ khỏi buổi 10; giữ làm tuỳ chọn cho lớp có key.
SAITS/BRITS (PyPOTS) chỉ dạy lý thuyết — gói kéo theo torch + transformers, quá nặng cho lab.

**Xong khi:** pipeline làm sạch có ≥ 8 test xanh, báo cáo chất lượng dữ liệu tự sinh, và bảng so
sánh cho thấy phương pháp điền tốt nhất **đổi** giữa lỗ ngắn và lỗ dài.

### Buổi 11 — Ngoại lai và điểm gãy

**Mục tiêu:** phân biệt điểm bất thường cần xoá, sự kiện thật cần giữ, và thay đổi cấu trúc
làm dữ liệu cũ hết giá trị.

**Học:**
- **Outlier cộng** (một điểm), **level shift** (đổi mức vĩnh viễn), **temporary change**
  (đổi rồi hồi dần), **thay đổi phương sai**, **thay đổi mùa vụ**
- Ngoại lai do lỗi đo vs sự kiện thật (Tết, bão, khuyến mãi, COVID) — xử lý ngược nhau
- Phát hiện: z-score (và vì sao nó hỏng vì chính ngoại lai), **IQR**, **MAD**, **bộ lọc Hampel**
  (cửa sổ trượt), **phần dư STL robust**, Isolation Forest
- Ngưỡng theo ngữ cảnh: 3σ toàn chuỗi xoá hết đỉnh mùa hè — phải tính trên phần dư
- **Phát hiện điểm gãy (changepoint)**: CUSUM, **PELT**, Binary Segmentation (ruptures);
  hàm chi phí, penalty, chọn số điểm gãy
- Xử lý sau khi tìm thấy: thay bằng giá trị kỳ vọng, winsorize, **biến giả (dummy)**, cắt bỏ
  đoạn trước điểm gãy, hoặc để mô hình robust tự xử lý
- COVID: dữ liệu 2020–2021 là ngoại lai, điểm gãy, hay "bình thường mới"? Ba cách xử lý, ba kết quả dự báo
- Ghi nhật ký sự kiện (event log) song song với dữ liệu

**Lab:**
1. Tổng lượt xem Wikipedia tiếng Việt: Hampel bắt đỉnh tin tức, so với z-score toàn chuỗi
   *(Phase 4 đo: 3σ chỉ gắn cờ 16/3.653 ngày, Hampel k=15 gắn 121 — masking do biên độ xu hướng;
   thêm một điểm cực lớn làm 3σ tụt từ 16 xuống 5 ngày, Hampel không đổi)*
2. Hành khách hàng không **EU27 theo tháng 2008–2026 (Eurostat avia_paoc)**: PELT tìm điểm gãy COVID và
   điểm hồi phục *(2020-04 giảm 98,65% so với 2020-01; PELT trên log ra **2020-02 và 2021-05**, ổn định qua
   pen **1–4·log n** — từ 5·log n trở lên ra 0 điểm gãy; chạy trên mức thô chưa log thì ra **43** điểm gãy giả)*
   — thay US BTS T-100 (chỉ có bảng HTML, data.bts.gov 403)
3. Xoá mọi điểm > 3σ trên lượt xem bài "Tết Nguyên Đán" → mất đỉnh Tết (54/54 cờ rơi vào tháng 01/02/12).
   *(Phase 4 đo: **cả 5 phương pháp — kể cả Hampel và STL robust — đều gắn cờ 10/10 đỉnh Tết**; đỉnh rơi vào
   ngày thứ 22–47 của năm dương, xê dịch 25 ngày.)* Kết luận của lab: **không ngưỡng thống kê nào phân biệt được
   'lỗi đo' với 'sự kiện thật'** — phải có nhật ký sự kiện / biến giả lịch âm (nối buổi 13); STL robust chỉ dùng
   cho mùa vụ cố định theo lịch dương (minh hoạ bằng mùa vụ tuần)
4. Dự báo 2023 bằng 3 cách xử lý COVID (giữ, coi là thiếu rồi nội suy, cắt), so sai số
   *(Phase 4 đo: MAPE 24,01% / **8,71%** / 18,11% — khớp khuyến nghị của Hyndman & Rostami-Tabar 2024 cho
   trường hợp chỉ cần dự báo SAU giai đoạn gián đoạn)*

**Dữ liệu:** Wikimedia Pageviews API (CC0) — tổng lượt xem vi.wikipedia và bài "Tết Nguyên Đán";
Eurostat avia_paoc (CC BY 4.0). Thư viện: `ruptures` (không có CROPS → học viên tự quét penalty và vẽ elbow).

**Xong khi:** trên một chuỗi lạ, gắn nhãn đúng loại cho ≥ 4/5 bất thường cài sẵn (điểm, level
shift, thay đổi tạm, sự kiện thật) và bảo vệ được cách xử lý từng loại.

### Buổi 12 — Khử nhiễu và miền tần số

**Mục tiêu:** hiểu nhiễu là gì, khử nhiễu bằng cách nào, và nhận ra lúc khử nhiễu làm hại dự báo.

**Học:**
- Tín hiệu + nhiễu; tỷ lệ tín hiệu/nhiễu (SNR); nhiễu trắng vs nhiễu có màu
- **Lấy mẫu, aliasing, định lý Nyquist**: lấy mẫu mỗi giờ thì không thấy được dao động 30 phút,
  và dao động đó còn giả dạng thành chu kỳ khác
- **Bộ lọc trung bình trượt**: trailing (nhân quả, trễ pha) vs **centered (dùng tương lai — rò rỉ)**
- **EWMA**: một tham số α, trễ bao nhiêu
- **Savitzky–Golay**: giữ đỉnh tốt hơn MA
- **LOESS/LOWESS**; bộ lọc **Hodrick–Prescott** và vấn đề điểm cuối chuỗi
- **Lọc Kalman**: filter (chỉ quá khứ) vs smoother (cả tương lai) — dùng cái nào cho dự báo
- **Miền tần số**: biến đổi Fourier (FFT), **periodogram**, mật độ phổ — tìm chu kỳ ẩn
- Lọc thông thấp / thông cao / thông dải (Butterworth), `filtfilt` là lọc hai chiều → rò rỉ
- **Wavelet** (PyWavelets): phân tích đa độ phân giải, khử nhiễu bằng ngưỡng mềm
- **Khi nào không nên khử nhiễu**: mục tiêu là dự báo giá trị quan sát (có nhiễu); khử nhiễu
  feature thì được, khử nhiễu target làm đánh giá sai
- **Nguyên tắc vàng**: mọi bộ lọc dùng làm feature phải là bộ lọc **nhân quả** (chỉ dùng quá khứ)

**Lab:**
1. Cảm biến nhiệt độ/độ ẩm 10 phút trong nhà: periodogram tìm chu kỳ ngày và chu kỳ bật tắt thiết bị
2. Hạ mẫu xuống 1 giờ không lọc trước → aliasing sinh chu kỳ giả; lọc thông thấp rồi hạ mẫu → hết
3. So 6+ bộ lọc (MA trailing, MA centered, EWMA, Savitzky–Golay, Butterworth nhân quả/`filtfilt`,
   Kalman **filter** và **smoother**, wavelet) trên cùng tín hiệu: sai số khử nhiễu, độ trễ pha
   *(Kalman filter là ví dụ duy nhất trễ 0 mà vẫn nhân quả — đừng bỏ)*
4. Dùng từng bộ lọc làm feature cho một mô hình dự báo 1 giờ tới: **MA centered và `filtfilt`** cho backtest
   đẹp bất thường (−27,7% và −24,5% MAE), còn Savitzky–Golay/wavelet rò rỉ nhưng lợi ích giả nhỏ vì cửa sổ lấn
   tương lai ngắn hơn tầm dự báo — lợi ích giả tỉ lệ với lượng tương lai bộ lọc nhìn thấy; test rò rỉ bắt hết
5. Khử nhiễu wavelet cho tín hiệu, so với Savitzky–Golay

**Dữ liệu:** UCI Appliances Energy Prediction — cảm biến 10 phút (CC BY 4.0).

**Xong khi:** bảng so sánh 6 bộ lọc có cột "dùng tương lai?" đúng 100%, và một test tự động
phát hiện được feature dùng bộ lọc không nhân quả.

### Buổi 13 — Feature engineering và chống rò rỉ

**Mục tiêu:** xây bộ feature cho dự báo mà **mọi giá trị đều có sẵn tại thời điểm ra dự báo**.

**Học:**
- **Lag feature**: độ trễ phải ≥ tầm dự báo (hoặc dùng chiến lược đệ quy — nối sang buổi 22)
- **Rolling feature**: trung bình/độ lệch/min/max/quantile trượt — luôn `shift` trước khi `rolling`
- **Feature lịch**: giờ, thứ, tháng, cuối tuần, đầu/cuối tháng (ngày lương), mã hoá tuần hoàn sin/cos
- **Fourier term**: K cặp sin/cos cho mùa vụ dài (năm = 365.25 ngày) thay cho 365 dummy
- **Ngày lễ Việt Nam**: lễ dương lịch cố định vs **lễ âm lịch di động (Tết, Giỗ Tổ)** — đổi lịch
  âm sang dương, khoảng cách tới Tết (ngày trước/sau), cửa sổ ảnh hưởng; nghỉ bù
- **Biến ngoại sinh biết trước** (lịch, khuyến mãi đã lên kế hoạch) vs **không biết trước**
  (thời tiết thật — lúc dự báo chỉ có *thời tiết dự báo*) vs **tĩnh** (loại cửa hàng)
- **Point-in-time correctness**: dữ liệu bị sửa về sau (revision) — lúc dự báo thấy phiên bản nào
- **Các kiểu rò rỉ**: rolling không shift, chuẩn hoá fit trên toàn bộ dữ liệu, target encoding trên
  toàn bộ, điền dữ liệu hai chiều, feature tính sau khi biết kết quả, **dùng thời tiết thực tế thay
  thời tiết dự báo**
- Kiểm tra rò rỉ tự động: **cắt tương lai rồi tính lại feature** — giá trị quá khứ không được đổi

**Lab:**
1. Doanh số bán lẻ theo ngày: xây 40 feature, cố tình để 4 feature rò rỉ
2. Viết `kiem_ro_ri(ham_feature, df)`: tính feature trên dữ liệu đầy đủ và trên dữ liệu cắt tại
   ngày T, so các dòng ≤ T — bắt đủ 4 feature rò
3. Feature Tết cho lượt xem Wikipedia tiếng Việt 2016–2025: `so_ngay_toi_tet`, cửa sổ ±7 ngày —
   đo mức cải thiện so với chỉ dùng lễ dương lịch
4. Mô hình tải điện: dùng nhiệt độ thực tế vs nhiệt độ dự báo lưu trữ — chênh lệch sai số là "cái giá của rò rỉ"

**Dữ liệu:** UCI Online Retail II (CC BY 4.0); Wikimedia Pageviews tiếng Việt (CC0);
EIA-930 (public domain); Open-Meteo **Previous Runs API** (CC BY 4.0) — giá trị đã dự báo trước 1–7 ngày,
lưu từ 01/2024 (Historical Forecast API chỉ ghép vài giờ đầu mỗi lượt chạy nên không phải "dự báo day-ahead").

**Xong khi:** bộ feature qua bài kiểm rò rỉ tự động 100%, có feature Tết âm lịch chạy đúng cho
mọi năm 2000–2035, và giải thích được mỗi feature "biết trước bao lâu".

### Dự án giữa chặng 1 — EDA và pipeline làm sạch

Đặt sau buổi 13. Làm cá nhân, 1 tuần.

**Đề:** nhận dữ liệu PM2.5 + thời tiết thật của **3 trạm ở Hà Nội và TP.HCM** (OpenAQ +
Open-Meteo), 2 năm, chưa ai làm sạch. Giám khảo cài thêm 6 lỗi không báo trước (đổi đơn vị,
trạm đứng yên, lệch múi giờ, trùng lặp, ngày giả 0, một đoạn dữ liệu bị dời 1 ngày).

**Nộp:**
- Báo cáo EDA (notebook + PDF): bộ biểu đồ chẩn đoán, phân rã, ACF, tương quan PM2.5 × gió/độ
  ẩm/mưa có prewhitening, đặc trưng từng trạm, **mỗi nhận xét có bằng chứng**
- `lam_sach.py` + test: bắt được lỗi cài sẵn, điền dữ liệu có đánh giá bằng che nhân tạo, cột cờ
- Bộ feature đã qua kiểm rò rỉ
- Nhật ký quyết định: mỗi bước làm sạch, vì sao, ảnh hưởng tới bao nhiêu dòng

**Chấm (100):** phát hiện lỗi cài sẵn 30 · chất lượng EDA và lập luận 25 · pipeline + test 25 ·
chống rò rỉ 10 · trình bày 10. **Cột mốc M1.**

---

## Giai đoạn 2 — Thống kê cổ điển và đánh giá (buổi 14–21)

### Buổi 14 — Baseline và chỉ số đánh giá

**Mục tiêu:** có thước đo đúng trước khi có mô hình; mọi mô hình sau đều phải thắng baseline.

**Học:**
- **Baseline**: mean, **naive**, **seasonal naive**, drift — và vì sao chúng khó thắng hơn tưởng
- Giá trị khớp (fitted) vs dự báo thật; **phần dư** vs **sai số dự báo**
- **Chẩn đoán phần dư**: không tự tương quan, trung bình 0, phương sai đều, gần chuẩn (cho khoảng dự báo)
- **Chỉ số phụ thuộc thang đo**: MAE (tối ưu → trung vị), RMSE (tối ưu → trung bình)
- **Chỉ số phần trăm**: MAPE (vô hạn khi y = 0, phạt lệch không đều), sMAPE (không thật sự "đối xứng")
- **Chỉ số chuẩn hoá**: **MASE**, **RMSSE** (M5) — so với naive trong mẫu, so sánh được giữa các chuỗi
- **WAPE** / MAD-mean ratio — chuẩn doanh nghiệp bán lẻ; **bias** (ME, tracking signal)
- Chọn chỉ số theo quyết định: tối ưu cái gì thì dự báo ra con số khác nhau
- Tổng hợp chỉ số qua nhiều chuỗi: trung bình, trung vị, trọng số theo doanh thu
- Công thức đầy đủ ở Phụ lục D, ví dụ:

$$\mathrm{MASE} = \frac{\frac{1}{h}\sum_{t=1}^{h} |y_{T+t} - \hat{y}_{T+t}|}{\frac{1}{T-m}\sum_{t=m+1}^{T} |y_t - y_{t-m}|}$$

**Lab:**
1. 4 baseline cho 1.000 chuỗi M4 theo ngày, chẩn đoán phần dư của seasonal naive
2. Tự viết MAE, RMSE, MAPE, sMAPE, MASE, RMSSE, WAPE, so với `utilsforecast.losses`
3. Chuỗi có số 0: MAPE ra `inf`/khổng lồ — bảng xếp hạng mô hình đảo lộn khi đổi chỉ số
4. Hai dự báo: một tối ưu MAE, một tối ưu RMSE trên dữ liệu lệch — chúng khác nhau thế nào, vì sao

**Dữ liệu:** M4 (Monash, CC BY 4.0); UCI Online Retail II (CC BY 4.0).

**Xong khi:** có hàm `danh_gia()` trả bảng 7 chỉ số + baseline, và giải thích được bằng ví dụ
số vì sao đổi chỉ số làm đổi mô hình "tốt nhất".

### Buổi 15 — Backtesting đúng cách

**Mục tiêu:** ước lượng sai số tương lai một cách trung thực — bộ backtest dùng cho cả khoá.

**Học:**
- Vì sao không được chia ngẫu nhiên: tự tương quan + tương lai lọt vào tập huấn luyện
- **Hold-out theo thời gian** và nhược điểm: một điểm cắt duy nhất = một lần may rủi
- **Rolling origin / time series cross-validation**: expanding window vs sliding window
- `step_size`, số cửa sổ, **khoảng trống (gap)** giữa train và test khi dữ liệu về trễ
- Tầm dự báo nhiều bước: sai số theo từng bước h
- **Refit** mỗi cửa sổ hay không — chi phí vs trung thực
- Các kiểu rò rỉ trong backtest: tune siêu tham số trên cùng cửa sổ báo cáo, chuẩn hoá toàn cục,
  chọn feature bằng toàn bộ dữ liệu
- **Ba tập**: tune / chọn mô hình / báo cáo cuối — không bao giờ dùng lại tập báo cáo
- So sánh hai mô hình có ý nghĩa thống kê: **Diebold–Mariano**, kiểm định Wilcoxon trên nhiều chuỗi,
  biểu đồ critical difference (Nemenyi)
- Mô phỏng đúng quy trình production: dữ liệu có tại thời điểm dự báo (nối buổi 13 và 41)

**Lab:**
1. KFold ngẫu nhiên vs rolling origin trên cùng mô hình: sai số ước lượng lệch nhau bao nhiêu
   so với sai số thật trên 3 tháng cuối để riêng
2. Xây `backtest(model, df, h, n_windows, step, gap)` trên `statsforecast.cross_validation`
3. Vẽ sai số theo tầm h và theo từng cửa sổ
4. Diebold–Mariano giữa seasonal naive và một mô hình "hơn 3%" — chênh lệch có thật không

**Dữ liệu:** M4 theo giờ (Monash, CC BY 4.0); EIA-930 (public domain).

**Xong khi:** chứng minh bằng số rằng CV ngẫu nhiên đánh giá quá lạc quan, và bộ backtest của
mình dự đoán sai số hold-out cuối chênh < 10%.

### Buổi 16 — Exponential smoothing và Theta

**Mục tiêu:** hiểu họ mô hình thắng nhiều cuộc thi nhất lịch sử, từ công thức tới state space.

**Học:**
- **SES**: trung bình có trọng số giảm theo cấp số nhân; α và độ trễ phản ứng
- **Holt** (xu hướng tuyến tính), **damped trend** (xu hướng tắt dần — thường thắng ngoài đời)
- **Holt–Winters** cộng vs nhân — chọn theo biên độ mùa vụ có tăng theo mức không
- **Phân loại ETS** (Error, Trend, Seasonal): 30 mô hình, cái nào không ổn định số học
- **Mô hình state space**: phương trình quan sát + phương trình trạng thái → likelihood → khoảng dự báo
- Chọn mô hình bằng **AICc**; **AutoETS**
- **Theta method**: phân rã hai đường theta, tương đương SES + drift; vì sao thắng M3
- Khi nào ETS thất bại: nhiều mùa vụ, chu kỳ dài, biến ngoại sinh

**Lab:**
1. Tự viết SES và Holt bằng NumPy, tối ưu α, β bằng `scipy.optimize`, so với statsforecast
2. Chuỗi hành khách hàng không: Holt–Winters cộng vs nhân — đọc phần dư
3. AutoETS + AutoTheta cho 1.500 chuỗi du lịch theo tháng, backtest so seasonal naive + DM test
4. Vẽ khoảng dự báo 80/95% của ETS, kiểm tra tỷ lệ phủ thật trên backtest

**Dữ liệu:** Tourism Monthly (Monash, CC BY 4.0); US BTS hành khách hàng không (public domain).

**Xong khi:** AutoETS thắng seasonal naive trên MASE có ý nghĩa thống kê, và giải thích được vì
sao Holt–Winters cộng sai trên chuỗi có biên độ mùa vụ tăng.

### Buổi 17 — ARIMA và SARIMA

**Mục tiêu:** mô hình hoá cấu trúc tự tương quan một cách tường minh.

**Học:**
- **AR(p)**, **MA(q)**, **ARMA** — điều kiện dừng và khả nghịch
- Đọc ACF/PACF để đoán p, q (và giới hạn của cách đọc này)
- **ARIMA(p,d,q)**: d từ buổi 7; hằng số và drift
- **SARIMA(p,d,q)(P,D,Q)m**
- Ước lượng MLE, chọn bằng AICc; **auto-ARIMA** (thuật toán Hyndman–Khandakar)
- Kiểm tra phần dư: Ljung-Box, nghiệm đơn vị của đa thức
- Dự báo và khoảng dự báo; vì sao khoảng của ARIMA(0,1,0) nở theo √h
- ETS vs ARIMA: mối liên hệ và khác biệt; không có cái nào luôn thắng
- Giới hạn: dữ liệu theo giờ mùa vụ dài (m = 168) làm SARIMA chậm/không khả thi → dùng Fourier (buổi 18)

**Lab:**
1. Mô phỏng AR(2), MA(1), ARMA(1,1) — đọc ACF/PACF, đoán bậc, kiểm lại bằng ước lượng
2. Chuỗi kinh tế tháng: tự xác định SARIMA từ ACF/PACF, so với `AutoARIMA`
3. Cố tình quên phần mùa vụ: phần dư còn đỉnh ACF ở lag 12 — sửa
4. So AutoARIMA vs AutoETS vs seasonal naive trên bộ backtest buổi 15

**Dữ liệu:** sản lượng công nghiệp theo tháng (Federal Reserve Board G.17, public domain); Tourism Monthly (Monash).

**Xong khi:** mô hình tự chọn bậc có phần dư qua Ljung-Box, AICc trong phạm vi 2 đơn vị so với
auto-ARIMA, và giải thích được từng tham số.

### Buổi 18 — Hồi quy chuỗi thời gian và hồi quy động

**Mục tiêu:** đưa biến giải thích vào mô hình thống kê mà không rơi vào hồi quy giả.

**Học:**
- Hồi quy tuyến tính với xu hướng, dummy mùa vụ, biến ngoại sinh
- **Hồi quy giả** và phần dư tự tương quan → sai số chuẩn sai, p-value "đẹp" vô nghĩa
- Chọn biến: AIC, AICc, BIC, CV — không dùng p-value để chọn biến dự báo
- **Hồi quy động (regression with ARIMA errors)**: phần dư của hồi quy được mô hình bằng ARIMA
- Dự báo biến giải thích: kịch bản vs dự báo của biến đó (nhiệt độ phải được dự báo trước)
- **Nhiều mùa vụ**: Fourier term (chọn K bằng AICc), **TBATS**, **MSTL + mô hình cho phần khử mùa vụ**
- **Biến can thiệp**: xung (pulse), bậc (step), dốc (ramp); hiệu ứng trễ phân phối (distributed lag)
- Hồi quy phi tuyến theo khúc (piecewise) cho xu hướng gãy
- **Prophet**: mô hình cộng xu hướng + Fourier + lễ; vì sao dễ dùng, vì sao thường thua
  AutoETS/ARIMA trên benchmark, và các bẫy mặc định (changepoint quá linh hoạt, lễ âm lịch phải tự khai)

**Lab:**
1. Hồi quy doanh số theo một chuỗi có xu hướng không liên quan: R² cao, p < 0.001, phần dư tự
   tương quan — sửa bằng hồi quy động, hệ số mất ý nghĩa
2. Tải điện theo giờ ~ Fourier(ngày, tuần) + CDD/HDD + dummy lễ, sai số ARIMA
3. So 4 cách xử lý đa mùa vụ: Fourier+ARIMA, TBATS, MSTL+ETS, Prophet — cùng backtest
4. Prophet không khai Tết vs có khai Tết trên lượt xem Wikipedia tiếng Việt

**Dữ liệu:** EIA-930 (public domain); Open-Meteo (CC BY 4.0); Wikimedia Pageviews tiếng Việt (CC0).

**Xong khi:** mô hình hồi quy động có phần dư trắng, thắng seasonal naive và Prophet mặc định
trên backtest, giải thích được vì sao p-value ở bước 1 là ảo.

### Buổi 19 — Nhu cầu gián đoạn

**Mục tiêu:** dự báo chuỗi phần lớn là số 0 — phụ tùng, dược phẩm, SKU bán chậm.

**Học:**
- Phân loại nhu cầu Syntetos–Boylan: **ADI** (khoảng cách trung bình giữa các lần có nhu cầu) × **CV²**
  → smooth / erratic / intermittent / lumpy
- Vì sao ETS/ARIMA hỏng: dự báo 0.3 cái/ngày không đặt hàng được, khoảng dự báo âm
- **Croston**: tách kích thước và khoảng cách; **SBA** (hiệu chỉnh bias); **TSB** (có thể giảm về 0 — sản phẩm chết)
- **ADIDA / IMAPA**: gộp thời gian để giảm số 0
- Mô hình đếm: Poisson, âm nhị thức, zero-inflated
- Chỉ số cho chuỗi thưa: MASE/RMSSE, **không dùng MAPE**; đánh giá theo **mức phục vụ và tồn kho**
- Dự báo tổng theo thời gian dẫn (lead time) thay vì từng ngày
- Nhu cầu bị kiểm duyệt (hết hàng) — nhắc lại từ buổi 10

**Lab:**
1. Phân loại 2.674 chuỗi phụ tùng xe theo ADI × CV²
2. Tự viết Croston và TSB, so với statsforecast
3. So ETS, Croston, SBA, TSB, ADIDA, seasonal naive trên RMSSE
4. Mô phỏng tồn kho (order-up-to, lead time 2 tuần) từ mỗi dự báo: mô hình thắng RMSSE có thắng
   chi phí tồn kho không

**Dữ liệu:** Car Parts (Monash, CC BY 4.0); tuỳ chọn M5 (xem giấy phép ở Phụ lục F).

**Xong khi:** bảng so sánh cả RMSSE lẫn chi phí tồn kho mô phỏng, chỉ ra được ít nhất một trường
hợp chỉ số thống kê và chi phí thực chọn hai mô hình khác nhau.

### Buổi 20 — Đa biến, state space và nowcasting

**Mục tiêu:** mô hình nhiều chuỗi ảnh hưởng lẫn nhau, và dự báo "hiện tại" khi số liệu chính thức về trễ.

**Học:**
- **VAR(p)**: mỗi biến phụ thuộc quá khứ của mọi biến; chọn p; số tham số bùng nổ theo số biến
- Hàm phản ứng xung (IRF), phân rã phương sai sai số dự báo
- **Cointegration**: hai chuỗi không dừng nhưng tổ hợp tuyến tính dừng (giá xăng và giá dầu);
  kiểm định Engle–Granger, Johansen; **VECM**
- **Mô hình state space tổng quát** và **bộ lọc Kalman**: dự báo – cập nhật; xử lý dữ liệu thiếu tự nhiên
- Local level, local linear trend, **mô hình cấu trúc (UCM)** — nối sang Bayes (buổi 27)
- **Dynamic factor model**: vài nhân tố ẩn điều khiển hàng trăm chuỗi
- **Nowcasting**: GDP quý công bố trễ 1 tháng, dữ liệu tháng về sớm hơn; **ragged edge**
  (mỗi chuỗi kết thúc ở một thời điểm khác nhau)
- **Tần suất hỗn hợp**: bridge equation, **MIDAS**, dynamic factor tần suất hỗn hợp
- Dữ liệu vintage (phiên bản theo ngày công bố) — Real-Time Data Set của Philadelphia Fed

**Lab:**
1. Giá dầu thô và giá xăng: kiểm cointegration, VECM, so với VAR trên sai phân
2. Tự viết bộ lọc Kalman cho local level model, so với `statsmodels UnobservedComponents`
3. Dynamic factor model trích 3 nhân tố từ vài chục chuỗi tháng của BEA/BLS/Fed Board (không dùng FRED-MD)
4. Nowcast GDP quý hiện tại theo từng tháng dữ liệu về, dùng **vintage thật** — sai số giảm dần

**Dữ liệu:** GDP thực + chuỗi tháng từ BEA NIPA, BLS, Fed Board (public domain); vintage GDP từ Philadelphia
Fed Real-Time Data Set ("informational, educational, and research purposes only" — không phân phối lại);
giá dầu WTI (EIA, public domain). **Không dùng FRED/ALFRED/FRED-MD**: điều khoản cấm dùng nội dung FRED "in
connection with the development or training of any software program or system or machine learning".

**Xong khi:** nowcast GDP dùng vintage thật (không dùng số đã sửa về sau), vẽ được sai số giảm
theo từng tháng thông tin mới, và giải thích được vì sao dùng số liệu đã sửa là rò rỉ.

### Buổi 21 — Chuỗi tài chính và biến động

**Mục tiêu:** hiểu vì sao dự báo giá gần như vô ích mà dự báo **biến động** lại làm được — và
miễn nhiễm với các demo "AI đoán giá chính xác 99%".

**Học:**
- Lợi suất (log return) vs giá; vì sao mô hình hoá lợi suất, không mô hình hoá giá
- **Giả thuyết thị trường hiệu quả**, random walk; dự báo làm thay đổi chính thị trường
- **Các sự thật cách điệu (stylized facts)**: đuôi dày, cụm biến động, hiệu ứng đòn bẩy, lợi suất
  gần như không tự tương quan nhưng bình phương lợi suất thì có
- **ARCH, GARCH(1,1)**, GJR-GARCH, EGARCH; phân phối Student-t
- Dự báo biến động, **Value at Risk** và Expected Shortfall; backtest VaR (Kupiec)
- Biến động thực hiện (realized volatility) từ dữ liệu tần suất cao; **HAR model**
- **Regime switching** (Markov switching): thị trường bình thường vs khủng hoảng
- **Mổ xẻ demo "LSTM đoán giá 99%"**: vẽ dự báo cạnh giá dịch 1 ngày — trùng khít, tức là naive
- Rò rỉ kinh điển trong tài chính: survivorship bias, look-ahead bias, chuẩn hoá toàn cục

**Lab:**
1. BTC theo giờ và tỷ giá USD/JPY: kiểm các sự thật cách điệu bằng biểu đồ và số liệu
2. Tái hiện demo "LSTM đoán giá": R² 0.99 → so với naive → chênh lệch không có ý nghĩa
3. GARCH(1,1) và GJR-GARCH dự báo biến động ngày, so với biến động thực hiện; HAR model
4. VaR 99% ngày, backtest Kupiec
5. Markov switching 2 trạng thái trên lợi suất, vẽ xác suất "khủng hoảng" theo thời gian

**Dữ liệu:** Binance Public Data (data.binance.vision — xem điều khoản ở Phụ lục F); tỷ giá H.10
(Federal Reserve Board, public domain — tải thẳng từ Fed Board, không qua FRED).

**Xong khi:** trình bày được trong 5 phút, bằng số liệu tự chạy, vì sao demo đoán giá là naive
ngụy trang; GARCH dự báo biến động thắng biến động lịch sử cố định. **Cột mốc M2.**

---

## Giai đoạn 3 — Machine learning (buổi 22–24)

### Buổi 22 — Biến dự báo thành bài toán hồi quy

**Mục tiêu:** dùng mô hình ML dạng bảng cho dự báo mà không rò rỉ, và hiểu vì sao mô hình
**global** thắng khi có nhiều chuỗi.

**Học:**
- **Mô hình local** (một mô hình mỗi chuỗi) vs **global** (một mô hình cho mọi chuỗi) — học
  chung mẫu hình, cần chuẩn hoá theo chuỗi
- Biến chuỗi thời gian thành bảng: cửa sổ trượt, lag, rolling, lịch, id chuỗi, biến tĩnh
- **Chiến lược đa bước**: **recursive** (một mô hình, đưa dự báo làm đầu vào — tích luỹ sai số),
  **direct** (mỗi h một mô hình), **DirRec**, **MIMO** (một mô hình ra cả vector)
- Lag nhỏ hơn tầm dự báo trong chiến lược direct = rò rỉ
- **Biến đổi target**: sai phân, chuẩn hoá theo chuỗi (local scaler), log — và đổi ngược
- Vì sao cây quyết định **không ngoại suy được** xu hướng → khử xu hướng trước
- Feature tĩnh vs động; biến ngoại sinh tương lai
- mlforecast: `MLForecast`, `lags`, `lag_transforms`, `target_transforms`, `cross_validation`

**Lab:**
1. Tự viết pipeline recursive bằng pandas + scikit-learn cho 1 chuỗi, rồi mlforecast cho 10.000 chuỗi
2. Cố tình để lag 1 cho h = 7 ở chiến lược direct: backtest đẹp, dự báo thật sụp — bắt bằng test
3. So recursive vs direct vs MIMO theo sai số từng bước h
4. Global LightGBM vs local AutoETS trên cùng backtest — global thắng ở đâu, thua ở đâu
5. Chuỗi có xu hướng tăng: cây không ngoại suy được; sửa bằng sai phân target

**Dữ liệu:** Kaggle Web Traffic qua Monash Repository (CC BY 4.0); UCI Online Retail II (CC BY 4.0).

**Xong khi:** mô hình global cho 10.000 chuỗi thắng AutoETS local trên RMSSE, qua bài kiểm rò rỉ,
và giải thích được sai số theo h của 3 chiến lược.

### Buổi 23 — Gradient boosting chuyên sâu

**Mục tiêu:** tái hiện công thức đã thắng M5 và hiểu mô hình quyết định dựa trên cái gì.

**Học:**
- LightGBM / XGBoost / CatBoost: khác nhau ở đâu, tham số quan trọng
- **Hàm mất mát theo bài toán**: L2, L1, **Tweedie** (dữ liệu đếm thưa), Poisson, **quantile** (nối buổi 25)
- Mô hình theo cấp phân cấp và theo nhóm (cửa hàng, ngành hàng) — cách các đội top M5 làm
- **Tune siêu tham số bằng Optuna trên CV thời gian** — không bao giờ CV ngẫu nhiên
- Early stopping trên cửa sổ thời gian
- **Diễn giải**: feature importance (gain vs split — đều có bẫy), **SHAP** toàn cục và cho từng dự báo
- **Partial dependence**: giá tăng thì nhu cầu giảm đúng chiều không? — kiểm tra hợp lý nghiệp vụ
- Ràng buộc đơn điệu (monotone constraints)
- Bài học M5: feature quan trọng hơn mô hình, chuẩn bị dữ liệu quyết định thứ hạng

**Lab:**
1. M5 (một bang, ~10.000 chuỗi SKU × cửa hàng): LightGBM L2 vs Tweedie trên WRMSSE
2. Optuna 50 thử nghiệm với CV thời gian; so với tune bằng KFold ngẫu nhiên → chọn sai tham số
3. SHAP: vì sao dự báo ngày X của SKU Y cao bất thường
4. Partial dependence của giá bán — phát hiện chiều sai, thêm monotone constraint

**Dữ liệu:** M5 Forecasting (Walmart qua Kaggle/IIF — học viên tự tải bằng tài khoản Kaggle, không
phân phối lại; xem Phụ lục F). Dự phòng: UCI Online Retail II (CC BY 4.0).

**Xong khi:** LightGBM Tweedie thắng L2 và thắng AutoETS trên WRMSSE; có một biểu đồ SHAP giải
thích một dự báo cụ thể cho người không biết ML.

### Buổi 24 — Ensemble, AutoML và ca khó

**Mục tiêu:** kết hợp mô hình đúng cách, dùng AutoML có kiểm soát, và xử lý các ca dữ liệu khó
ngoài đời: chuỗi ngắn, sản phẩm mới.

**Học:**
- **Combination puzzle**: trung bình đơn giản thường thắng trọng số tối ưu — vì sao
- Trung bình, trung vị, trọng số theo sai số, **stacking** trên backtest (cẩn thận rò rỉ tầng 2)
- Đa dạng mô hình quan trọng hơn chất lượng từng mô hình
- **Chọn mô hình theo đặc trưng** (FFORMA) — nối buổi 9
- **Overfit khi chọn mô hình**: thử 50 mô hình trên cùng tập test = tập test đã thành tập train
- **AutoGluon-TimeSeries**: ensemble thống kê + ML + DL + Chronos; đọc leaderboard, time limit
- **Chuỗi ngắn** (< 2 chu kỳ mùa vụ): mô hình đơn giản, mượn thông tin từ chuỗi tương tự, pooling
- **Cold start** sản phẩm mới: dự báo theo sản phẩm tương tự (analog), theo thuộc tính, theo đường cong vòng đời
- Chuỗi kết thúc (sản phẩm ngừng bán), chuỗi đổi mã
- Giới hạn dự báo trong khoảng (0 ≤ y ≤ sức chứa): biến đổi logit có tỷ lệ

**Lab:**
1. Ensemble trung bình của AutoETS + AutoTheta + LightGBM vs mô hình tốt nhất đơn lẻ
2. Chọn "mô hình tốt nhất" trong 30 mô hình trên cùng test: đo khoảng lạc quan khi đánh giá lại trên tập mới
3. AutoGluon-TimeSeries preset `medium_quality`, giới hạn 20 phút, đọc leaderboard và ensemble weight
4. Cold start: 200 sản phẩm mới trong Online Retail II, dự báo 8 tuần đầu bằng analog theo danh mục

**Dữ liệu:** M4 (Monash, CC BY 4.0); UCI Online Retail II (CC BY 4.0).

**Xong khi:** ensemble thắng mô hình tốt nhất đơn lẻ trên tập báo cáo **chưa từng dùng để chọn**;
cold start thắng "trung bình danh mục".

### Dự án giữa chặng 2 — Thi dự báo trên dữ liệu tương lai

Đặt sau buổi 24. Làm theo nhóm 2 người, 2 tuần.

**Đề:** dự báo nhu cầu điện theo giờ **7 ngày tới** cho 5 vùng điều độ Mỹ (EIA-930). Dữ liệu
EIA-930 có sẵn **dự báo day-ahead do chính đơn vị điều độ công bố** — đó là đối thủ thật cần vượt.

**Luật:** nộp dự báo trước 00:00 UTC thứ Hai; **dữ liệu chấm chưa tồn tại lúc nộp bài**. Chấm
tự động sau khi EIA cập nhật. Leaderboard trên MASE và so với dự báo của đơn vị điều độ.

**Nộp:** code tái lập được (`make du-bao NGAY=...`), backtest nội bộ 8 cửa sổ, báo cáo ngắn so
bậc thang: seasonal naive → hồi quy động → LightGBM global → ensemble.

**Chấm (100):** sai số trên dữ liệu tương lai 35 · khoảng cách backtest nội bộ vs sai số thật
(trung thực của backtest) 20 · tái lập được 20 · chống rò rỉ (thời tiết dự báo, không dùng thời
tiết thật) 15 · báo cáo 10. **Thưởng +5** nếu thắng dự báo của đơn vị điều độ. **Cột mốc M3.**

---

## Giai đoạn 4 — Bất định (buổi 25–28)

### Buổi 25 — Dự báo xác suất

**Mục tiêu:** dự báo cả phân phối, và đánh giá được một dự báo phân phối là tốt hay tồi.

**Học:**
- Dự báo điểm → khoảng → **quantile** → **phân phối đầy đủ** → **sample path** (kịch bản)
- Khoảng dự báo từ mô hình (giả định chuẩn), từ bootstrap phần dư, từ mô phỏng
- **Quantile regression** và **pinball loss** (vì sao tối ưu pinball ra đúng quantile)
- **CRPS** — tổng quát hoá MAE cho phân phối; **Weighted Interval Score (WIS)** (chuẩn dự báo dịch bệnh)
- **Calibration** (đúng tỷ lệ) vs **sharpness** (hẹp): "tối đa độ sắc nét với điều kiện đã calibrate"
- **PIT histogram**, **reliability diagram**, coverage theo từng mức
- **Quantile crossing** và cách sửa
- **Scoring rule proper** — vì sao chỉ số không proper khuyến khích gian lận
- Dự báo **đuôi và giá trị cực đoan**: extreme value theory (GEV, peaks-over-threshold) cho tải đỉnh, lũ
- Khoảng dự báo nhiều bước: phụ thuộc giữa các bước, vì sao không cộng quantile

**Lab:**
1. Tải điện theo giờ: khoảng dự báo từ ETS (chuẩn) vs bootstrap — coverage thật trên backtest
2. LightGBM quantile cho 9 quantile, sửa quantile crossing
3. Tự viết pinball loss, CRPS từ mẫu, WIS; so với thư viện
4. PIT histogram + reliability diagram cho 3 mô hình, đọc: quá tự tin / quá thận trọng / lệch
5. Peaks-over-threshold cho tải đỉnh ngày: dự báo mức tải 1-trong-10-năm

**Dữ liệu:** EIA-930 (public domain); Open-Meteo (CC BY 4.0).

**Xong khi:** dự báo 9 quantile có coverage từng mức lệch < 5 điểm phần trăm trên backtest, và đọc
đúng lỗi calibration từ PIT histogram của một mô hình lạ.

### Buổi 26 — Conformal prediction cho chuỗi thời gian

**Mục tiêu:** khoảng dự báo có bảo đảm coverage không cần giả định phân phối — và giữ được khi dữ liệu trôi.

**Học:**
- Ý tưởng conformal: phần dư trên tập calibration → quantile → khoảng; bảo đảm hữu hạn mẫu
- Giả định **exchangeability** và vì sao chuỗi thời gian vi phạm nó
- **Split conformal**, **Conformalized Quantile Regression (CQR)** — khoảng thích nghi theo độ khó
- **EnbPI** (ensemble bootstrap, không cần tách tập)
- **Adaptive Conformal Inference (ACI)**: cập nhật mức α trực tuyến theo lỗi vừa mắc — giữ coverage khi có drift
- Conformal nhiều bước (theo từng h), conformal cho nhiều chuỗi
- Kiểm định exchangeability (MAPIE)
- Giới hạn: bảo đảm **trung bình theo thời gian**, không phải cho từng điểm; coverage có điều kiện

**Lab:**
1. PM2.5 theo giờ: split conformal trên mô hình LightGBM — coverage đẹp năm đầu, trượt dần khi mùa đổi
2. CQR: khoảng rộng vào mùa đông ô nhiễm, hẹp vào mùa hè
3. ACI và EnbPI: vẽ coverage trượt theo thời gian của 4 phương pháp
4. `ConformalIntervals` trong statsforecast và MAPIE, so với tự viết

**Dữ liệu:** UCI Beijing Multi-Site Air-Quality (CC BY 4.0).

**Xong khi:** khoảng 90% của ACI giữ coverage trượt 30 ngày trong [85%, 95%] suốt 2 năm có drift,
trong khi split conformal rơi ra ngoài; giải thích được vì sao.

### Buổi 27 — Dự báo Bayes và Gaussian Process

**Mục tiêu:** đưa kiến thức có trước vào mô hình, mượn sức mạnh giữa các chuỗi thưa, và có bất
định đầy đủ cho cả tham số.

**Học:**
- Suy nghĩ Bayes: prior, likelihood, posterior, **posterior predictive** = dự báo
- **Prior predictive check**: prior có sinh ra dữ liệu hợp lý không
- MCMC (NUTS) ở mức trực giác; chẩn đoán **r_hat, ESS, divergence** — không hội tụ thì không dùng
- **Mô hình state space Bayes / BSTS**: local level + mùa vụ + hồi quy (pymc-extras statespace)
- **Hierarchical Bayes (partial pooling)**: nhiều chuỗi thưa mượn sức mạnh từ nhau — nằm giữa local và global
- **Gaussian Process**: kernel như ngôn ngữ mô tả chuỗi (xu hướng = linear/RBF dài, mùa vụ =
  periodic, nhiễu = white); cộng và nhân kernel; chi phí O(n³) và xấp xỉ
- So với tần suất: khi nào Bayes đáng công (dữ liệu ít, cần prior nghiệp vụ, cần bất định tham số)

**Lab:**
1. Prior predictive check cho mô hình local level: prior mặc định sinh ra số lượng âm và khổng lồ — sửa
2. Hierarchical Poisson cho 300 chuỗi phụ tùng thưa: no pooling vs complete pooling vs partial pooling
3. BSTS trong PyMC cho lượt thuê xe ngày, đọc thành phần xu hướng/mùa vụ có dải bất định
4. GP với kernel tổng (trend + periodic tuần + periodic năm + noise), so ETS
5. Cố tình chạy mô hình có divergence, đọc chẩn đoán, reparameterize (non-centered)

**Dữ liệu:** Car Parts (Monash, CC BY 4.0); UCI Bike Sharing (CC BY 4.0).

**Xong khi:** mô hình phân cấp Bayes thắng no-pooling trên chuỗi thưa, mọi tham số r_hat < 1.01, và
giải thích bằng hình vì sao partial pooling kéo chuỗi ít dữ liệu về trung bình nhóm.

### Buổi 28 — Dự báo phân cấp và reconciliation

**Mục tiêu:** dự báo nhiều cấp (SKU → cửa hàng → vùng → toàn quốc) mà các con số **cộng khớp** với nhau.

**Học:**
- Cấu trúc **phân cấp** (hierarchical) vs **nhóm chéo** (grouped); ma trận tổng $S$
- **Không khớp (incoherent)**: dự báo độc lập mỗi cấp không cộng lại bằng nhau — kế hoạch mỗi phòng một số
- **Bottom-up**, **top-down** (theo tỷ lệ lịch sử / tỷ lệ dự báo), **middle-out**
- **Reconciliation tối ưu**: OLS, WLS, **MinT** (shrink) — ý tưởng chiếu lên không gian khớp
- Vì sao MinT thường cải thiện **cả** cấp dưới lẫn cấp trên
- **Reconciliation xác suất**: bootstrap, normal, PERMBU — quantile không cộng được
- **Temporal hierarchy / cross-temporal**: ngày → tuần → tháng cùng khớp
- Chỉ số đánh giá theo từng cấp và cho toàn cây

**Lab:**
1. Du lịch Úc: 8 vùng × 76 khu vực × 4 mục đích, dự báo base bằng AutoETS
2. So bottom-up, top-down, MinT trên từng cấp
3. Reconciliation xác suất, kiểm coverage cấp quốc gia
4. Temporal hierarchy: dự báo tháng và quý khớp nhau

**Dữ liệu:** Tourism Australia theo quý — dữ liệu `tourism` của gói R tsibble (GPL-3, chốt commit;
giấy phép gốc của Tourism Research Australia chưa xác minh được — Phụ lục F); dự phòng mở: phân cấp dựng
từ UCI Online Retail II (M5 không phân phối lại được nên không làm dự phòng mặc định).

**Xong khi:** dự báo khớp tuyệt đối mọi cấp (sai lệch cộng = 0), MinT thắng base forecast ở ≥ 3/4
cấp, và coverage xác suất cấp trên đạt mức danh nghĩa ± 5%. **Cột mốc M4.**

---

## Giai đoạn 5 — Deep learning (buổi 29–33)

### Buổi 29 — Nền deep learning cho chuỗi thời gian

**Mục tiêu:** tự viết mô hình DL cho dự báo bằng PyTorch, hiểu từng bước từ cửa sổ dữ liệu tới vòng huấn luyện.

**Học:**
- Tensor, autograd, `Dataset` / `DataLoader`, vòng huấn luyện, optimizer, learning rate
- **Tạo cửa sổ (windowing)**: input_size, horizon, stride; **cửa sổ chồng lấn giữa train và
  val = rò rỉ** → phải chia theo thời gian **trước** khi cắt cửa sổ
- **Chuẩn hoá**: global scaler (rò rỉ nếu fit toàn bộ), **per-window / RevIN** (xử lý dịch phân phối)
- **MLP** cho dự báo (thường mạnh bất ngờ), **RNN/LSTM/GRU** (gradient biến mất, trạng thái ẩn),
  **TCN** (tích chập nhân quả, dilated)
- Hàm mất mát, early stopping theo thời gian, seed và tính tái lập, overfit trên chuỗi ngắn
- Vì sao DL thường **thua** mô hình thống kê trên ít chuỗi ngắn, **thắng** trên nhiều chuỗi dài có liên quan

**Lab:**
1. Tiêu thụ điện 370 khách hàng: cắt cửa sổ đúng và sai (chồng lấn), đo khoảng lạc quan
2. Tự viết MLP, LSTM, TCN — huấn luyện trên CPU < 10 phút
3. Có/không RevIN khi mức tiêu thụ đổi theo năm
4. So với seasonal naive và LightGBM trên cùng backtest — viết nhận định trung thực

**Dữ liệu:** Electricity hourly — 321 khách hàng, theo giờ 2012–2014 (Monash/Zenodo, CC BY 4.0; bản gộp giờ
của UCI ElectricityLoadDiagrams20112014 — bản gốc 15 phút trên UCI tải quá chậm, xem Phụ lục F).

**Xong khi:** mô hình tự viết qua test "không chồng lấn cửa sổ", kết quả tái lập với seed cố định,
và có bảng so với baseline — kể cả khi DL thua.

### Buổi 30 — N-BEATS, N-HiTS, DeepAR, TFT, TiDE

**Mục tiêu:** hiểu và dùng các kiến trúc thiết kế riêng cho dự báo.

**Học:**
- **N-BEATS**: stack khối MLP, backcast/forecast, bản diễn giải được (trend + seasonality basis)
- **N-HiTS**: nội suy đa tầng tần số — nhanh, mạnh cho tầm xa
- **DeepAR**: RNN tự hồi quy + likelihood (Gaussian, âm nhị thức) → dự báo xác suất global
- **Temporal Fusion Transformer (TFT)**: biến tĩnh / quá khứ / **tương lai biết trước**, variable
  selection network, attention diễn giải được
- **TiDE**: encoder–decoder MLP, covariate tương lai, nhanh
- Phân loại covariate trong neuralforecast: `stat_exog`, `hist_exog`, `futr_exog` — đặt sai loại = rò rỉ
- AutoModel + Ray/Optuna trong neuralforecast; chi phí huấn luyện vs lợi ích

**Lab:**
1. 5 kiến trúc qua neuralforecast trên tải điện + nhiệt độ, cùng backtest
2. TFT: đưa nhiệt độ **thực tế** vào `futr_exog` (rò rỉ) vs **nhiệt độ dự báo** — đo chênh lệch
3. Đọc variable importance của TFT và basis của N-BEATS diễn giải được
4. DeepAR phân phối âm nhị thức cho dữ liệu đếm, kiểm calibration

**Dữ liệu:** Electricity hourly (Monash, CC BY 4.0); EIA-930 (public domain); Open-Meteo (CC BY 4.0).

**Xong khi:** bảng so 5 kiến trúc + LightGBM + seasonal naive có thời gian huấn luyện, và chỉ ra
được covariate nào bị khai sai loại trong một cấu hình cho sẵn.

### Buổi 31 — Transformer cho chuỗi thời gian

**Mục tiêu:** hiểu attention cho chuỗi thời gian và đánh giá trung thực các tuyên bố "state-of-the-art".

**Học:**
- Self-attention, positional encoding, chi phí O(L²) với chuỗi dài
- Informer / Autoformer / FEDformer (ngắn gọn — lịch sử)
- **"Are Transformers Effective for Time Series Forecasting?"** — **DLinear/NLinear** một lớp
  tuyến tính thắng nhiều Transformer
- **PatchTST**: chia patch như ViT, channel independence — vì sao hồi sinh Transformer
- **iTransformer**: đảo chiều, attention giữa các biến
- **TSMixer**: MLP trộn theo thời gian và theo kênh
- **Bẫy benchmark học thuật**: ETT/Weather/Electricity lặp đi lặp lại, `drop_last=True` bỏ phần
  test khó, chuẩn hoá sai, không so baseline thống kê, chọn tầm dự báo có lợi
- Cách đọc một bài báo dự báo có phê phán: checklist 10 câu

**Lab:**
1. Tái hiện DLinear vs PatchTST vs iTransformer trên ETTh1 với protocol chuẩn
2. Tắt `drop_last`, thêm seasonal naive và AutoETS vào bảng — thứ hạng đổi
3. Chạy cùng mô hình trên dữ liệu thật ngoài benchmark (EIA-930)
4. Chấm một bài báo cho sẵn theo checklist 10 câu

**Dữ liệu:** ETDataset (ETTh1/ETTm1 — CC BY-ND 4.0); EIA-930 (public domain).

**Xong khi:** bảng tái hiện có baseline thống kê, chỉ ra được ít nhất 2 lỗi protocol đã làm phóng
đại kết quả của một mô hình.

### Buổi 32 — Mô hình sinh và dữ liệu tổng hợp

**Mục tiêu:** sinh kịch bản tương lai nhất quán (sample path) và dữ liệu tổng hợp dùng được — biết kiểm chúng.

**Học:**
- Vì sao cần sample path: quyết định phụ thuộc cả đường đi (tồn kho tích luỹ), không chỉ từng quantile
- **Normalizing flow** cho phân phối nhiều chiều; **copula** để ghép phụ thuộc giữa các bước
- **Diffusion cho chuỗi thời gian**: TimeGrad (dự báo), CSDI (điền dữ liệu + dự báo), trực giác thêm–khử nhiễu
- Mô hình sinh sinh dữ liệu tổng hợp: tăng cường dữ liệu, kiểm thử pipeline, chia sẻ dữ liệu nhạy cảm
- **Đánh giá dữ liệu tổng hợp**: fidelity (giống phân phối, ACF, mùa vụ), utility (train-on-synthetic-test-on-real),
  **privacy/memorization** (khoảng cách tới bản ghi thật gần nhất)
- Dữ liệu tổng hợp có tham số (mô phỏng có đáp án) — dùng để kiểm thử phương pháp (nối buổi 38)
- **Energy score, variogram score** — chấm dự báo nhiều chiều

**Lab:**
1. Sample path từ DeepAR vs quantile độc lập: tồn kho tích luỹ 14 ngày khác nhau thế nào
2. CSDI (bản nhỏ, CPU) điền + dự báo PM2.5 nhiều trạm, so với buổi 10
3. Sinh dữ liệu tổng hợp tải điện, chấm fidelity + TSTR + memorization
4. Một mô hình sinh "quá tốt": chép nguyên chuỗi train — phát hiện bằng khoảng cách gần nhất

**Dữ liệu:** UCI Beijing Multi-Site Air-Quality (CC BY 4.0); Electricity hourly (Monash, CC BY 4.0).

**Xong khi:** báo cáo đánh giá dữ liệu tổng hợp đủ 3 trục, và energy score cho thấy sample path có
phụ thuộc thắng quantile độc lập.

### Buổi 33 — Không gian–thời gian và thời tiết AI

**Mục tiêu:** dự báo khi các chuỗi nằm trên một mạng lưới (đường, lưới điện, lưới khí quyển), và
dùng được mô hình thời tiết AI một cách có kiểm chứng.

**Học:**
- Dữ liệu không gian–thời gian: đồ thị cảm biến, lưới điểm (grid)
- **Graph Neural Network**: truyền thông điệp; STGCN, Graph WaveNet, DCRNN (trực giác + một cài đặt nhỏ)
- Ma trận kề từ khoảng cách vs học được
- **Thời tiết AI**: GraphCast, GenCast (ensemble diffusion), WeatherNext 2, **ECMWF AIFS** (đã vận
  hành, dữ liệu mở), Aurora — so với dự báo số trị (NWP)
- Dữ liệu tái phân tích ERA5, WeatherBench 2, chỉ số RMSE/ACC/CRPS theo biến và tầm
- **Kiểm chứng tại điểm**: dự báo lưới vs trạm quan trắc — nội suy, hiệu chỉnh độ cao, **hiệu chỉnh
  thống kê sau mô hình (MOS / post-processing)**
- Dùng thời tiết AI làm **covariate** cho dự báo tải điện/năng lượng tái tạo
- Rủi ro: đánh giá trên năm nằm trong tập huấn luyện ERA5; sự kiện cực đoan

**Lab:**
1. METR-LA: GNN nhỏ trên CPU vs mô hình từng cảm biến vs seasonal naive
2. Tải dự báo AIFS mở (GRIB) cho điểm Nội Bài 30 ngày gần nhất, so với quan trắc trạm Nội Bài
3. Hiệu chỉnh thống kê (hồi quy tuyến tính theo tầm) giảm sai số nhiệt độ bao nhiêu
4. Dùng nhiệt độ AIFS đã hiệu chỉnh làm covariate cho dự báo tải — so với Open-Meteo

**Dữ liệu:** Traffic hourly — 862 cảm biến PeMS (Monash, CC BY 4.0; METR-LA của DCRNN **không có giấy
phép dữ liệu** nên chỉ là tuỳ chọn học viên tự tải); ECMWF Open Data — AIFS (CC BY 4.0); NOAA GHCNh —
trạm Nội Bài `VMI0000VVNB` (CC0; ISD cũ đã dừng trạm này từ 08/2025 và dữ liệu ngoài Mỹ của ISD
không được phân phối lại theo WMO Res 40); Open-Meteo (CC BY 4.0).

**Xong khi:** kiểm chứng AIFS tại điểm có bảng sai số theo tầm 1–10 ngày trên dữ liệu **sau** mốc
huấn luyện, và hiệu chỉnh thống kê giảm được sai số hệ thống. **Cột mốc M5.**

---

## Giai đoạn 6 — Foundation model và LLM (buổi 34–37)

### Buổi 34 — Time series foundation model

**Mục tiêu:** dùng foundation model zero-shot có kiểm chứng, hiểu bên trong chúng hoạt động ra sao.

**Học:**
- Ý tưởng: huấn luyện trước trên hàng trăm tỷ điểm dữ liệu → dự báo chuỗi mới không cần huấn luyện
- **Biến số thành token**: scaling + quantization (Chronos gốc), **patch** (TimesFM, Moirai),
  context length, horizon, dự báo quantile trực tiếp
- Kiến trúc: encoder-only (Chronos-2 với group attention cho đa biến + covariates), decoder-only
  (TimesFM 2.5, Moirai 2, Toto), xLSTM (TiRex), flow-matching (Sundial)
- Dữ liệu huấn luyện trước (LOTSA, dữ liệu tổng hợp KernelSynth) và **nguy cơ trùng với tập đánh giá**
- **Luật mở rộng (scaling)** cho chuỗi thời gian — tới đâu thì còn đúng
- Chạy trên CPU: bản nhỏ (Chronos-Bolt/Chronos-2 small, TimesFM 2.5 200M), batch, độ trễ
- Khi nào zero-shot đủ tốt: nhiều chuỗi ngắn, cold start, cần kết quả nhanh

**Lab:**
1. Chronos-2 và TimesFM 2.5 zero-shot trên CPU cho 500 chuỗi, đo thời gian + bộ nhớ
2. So với seasonal naive, AutoETS, LightGBM global trên **dữ liệu sau mốc huấn luyện** của model (EIA-930 tháng gần nhất)
3. Context length 64 → 512 → 2048: chuỗi theo giờ cần thấy mùa vụ tuần
4. Dự báo quantile của foundation model: coverage có đạt không (nối buổi 25)

**Dữ liệu:** EIA-930 (public domain) — chỉ dùng giai đoạn sau ngày phát hành model;
fev-bench datasets trên Hugging Face — thẻ dữ liệu ghi "provided only for research purposes", giấy
phép theo từng nguồn gốc: chỉ dùng bộ con có nguồn mở rõ (Monash CC BY 4.0…), chốt revision (Phụ lục F).

**Xong khi:** bảng so sánh zero-shot vs mô hình đã học trên dữ liệu chắc chắn nằm ngoài tập huấn
luyện, kèm thời gian chạy, và kết luận khi nào nên dùng cái nào.

### Buổi 35 — Fine-tune, covariates và đọc benchmark

**Mục tiêu:** tận dụng foundation model tới cùng — covariates, fine-tune, ensemble — và đọc
leaderboard mà không bị lừa.

**Học:**
- **Covariates** trong Chronos-2 (quá khứ + tương lai biết trước), multivariate
- **Fine-tune**: toàn bộ vs LoRA/adapter vs chỉ head; bao nhiêu dữ liệu thì đáng; **quên thảm khốc**
- Ensemble foundation model + mô hình thống kê/ML (AutoGluon)
- **GIFT-Eval** (97 cấu hình), **fev-bench** (100 task, 46 có covariates) — cách tổng hợp: win rate,
  skill score, trung bình hình học
- **Rò rỉ benchmark**: dataset đánh giá nằm trong dữ liệu huấn luyện trước; leaderboard có cột "không rò"
- **Calibration** của foundation model (thường kém ở quantile đuôi) → conformal hoá lại (nối buổi 26)
- Chi phí vận hành: GPU vs CPU, độ trễ, kích thước, so với LightGBM

**Lab:**
1. Chronos-2 có/không covariates nhiệt độ trên tải điện
2. Fine-tune trên 200 điểm vs 20.000 điểm: overfit và quên
3. Ensemble Chronos-2 + LightGBM + AutoETS
4. Đọc leaderboard GIFT-Eval/fev-bench, tìm model có dấu hiệu rò dữ liệu, tính lại xếp hạng chỉ trên task sạch
5. Conformal hoá quantile của foundation model

**Dữ liệu:** EIA-930 (public domain); Open-Meteo (CC BY 4.0); fev-bench (Hugging Face).

**Xong khi:** chỉ ra được ≥ 1 tình huống foundation model **thua** LightGBM có feature tốt và giải
thích vì sao; foundation model sau conformal đạt coverage danh nghĩa.

### Buổi 36 — LLM và agent trong pipeline dự báo

**Mục tiêu:** dùng LLM ở đúng chỗ nó mạnh (văn bản, ngữ cảnh, điều phối, giải thích) và chặn nó
ở chỗ nó yếu (bịa số).

**Học:**
- LLM đọc số trực tiếp (LLMTime, Time-LLM) — vì sao thường thua mô hình chuyên dụng rẻ hơn nhiều
- **Dự báo có ngữ cảnh văn bản (multimodal)**: tin tức, thông báo khuyến mãi, sự kiện → feature hoặc
  điều kiện cho dự báo; benchmark kiểu "Context is Key"
- Trích xuất sự kiện có cấu trúc từ văn bản bằng LLM (JSON schema) → biến can thiệp
- **Agent dự báo** (TimeCopilot): gọi công cụ — tải dữ liệu, chạy backtest, chọn mô hình, ensemble
- **Guardrail**: con số trong câu trả lời phải lấy từ kết quả công cụ; backtest cố định, agent không
  được tự đổi tập đánh giá
- LLM giải thích dự báo cho người không chuyên — kiểm chứng từng câu với dữ liệu
- Chi phí, độ trễ, tính tái lập (temperature, seed, phiên bản model)
- Model mở chạy local (Ollama/llama.cpp) vs API

**Lab:**
1. LLM dự báo trực tiếp chuỗi số vs AutoETS — so sai số và chi phí
2. Trích xuất sự kiện từ tin tức (GDELT) thành biến can thiệp cho lượt xem Wikipedia
3. Agent nhỏ với 4 công cụ (tải dữ liệu, backtest, dự báo, vẽ) — **cố tình để agent tự chọn tập test**:
   nó chọn tập có lợi; sửa bằng guardrail
4. LLM viết báo cáo dự báo; test tự động kiểm mọi con số trong báo cáo có trong kết quả công cụ

**Dữ liệu:** Wikimedia Pageviews (CC0); GDELT (sử dụng tự do, ghi nguồn); EIA-930 (public domain).

**Xong khi:** agent chạy hết 20 yêu cầu dự báo mà test "không bịa số" xanh 100%, và có bảng chi phí
mỗi lần chạy.

### Buổi 37 — Dự báo sự kiện bằng LLM

**Mục tiêu:** dự báo xác suất cho câu hỏi về sự kiện đơn lẻ ("X có xảy ra trước ngày Y không?") —
như superforecaster — và đánh giá không bị rò rỉ thời gian.

**Học:**
- **Dự báo theo phán đoán (judgmental)**: base rate / outside view vs inside view, **ước lượng Fermi**,
  cập nhật Bayes theo tin mới, phương pháp **Delphi**, thiên kiến neo, quá tự tin
- **Superforecasting** (Tetlock, Good Judgment Project) — thói quen của người dự báo giỏi
- **Chấm dự báo xác suất nhị phân**: **Brier score**, log score, **calibration curve**, độ phân giải
  (resolution); phân rã Murphy
- **Gộp dự báo**: trung bình, trung vị, **extremizing** trung bình log-odds
- Thị trường dự báo và nền tảng: Metaculus, Manifold, Polymarket — vai trò làm baseline
- **ForecastBench**: câu hỏi dataset vs câu hỏi market; tình hình 2026 (AI ngang superforecaster ở
  câu hỏi dataset, còn tranh cãi ở câu hỏi market)
- **Kiến trúc bot dự báo**: tách câu hỏi con → truy vấn tìm kiếm → lọc liên quan và **thời điểm** →
  nhiều lần suy luận → gộp → hiệu chỉnh
- **Rò rỉ thời gian khi backtest LLM**: model đã "biết" kết quả các câu hỏi trước mốc cắt kiến
  thức; yêu cầu model "giả vờ không biết" **không hiệu quả**; bộ lọc ngày của công cụ tìm kiếm cũng rò
- Cách đánh giá sạch: chỉ dùng câu hỏi resolve **sau** mốc cắt kiến thức, snapshot tìm kiếm có ngày,
  hoặc dự báo trực tiếp cho câu hỏi chưa resolve
- Hiệu chỉnh xác suất của LLM (Platt/isotonic) trên tập câu hỏi đã resolve sạch

**Lab:**
1. Học viên tự dự báo 20 câu hỏi (có base rate), chấm Brier, vẽ calibration của chính mình
2. Bot LLM đơn giản trên câu hỏi ForecastBench đã resolve **trước** mốc cắt kiến thức → Brier đẹp giả tạo
3. Chạy lại chỉ trên câu hỏi resolve **sau** mốc cắt → Brier thật; đo "khoảng rò rỉ"
4. Thêm retrieval có lọc thời gian + nhiều lần suy luận + gộp log-odds, so với baseline "xác suất thị trường"
5. Hiệu chỉnh isotonic, vẽ lại calibration

**Dữ liệu:** ForecastBench datasets (CC BY-SA 4.0, github.com/forecastingresearch/forecastbench-datasets);
tuỳ chọn Metaculus API (điều khoản sử dụng riêng).

**Xong khi:** báo cáo Brier score của bot **chỉ trên câu hỏi sau mốc cắt kiến thức**, kèm "khoảng rò
rỉ" đo được, calibration curve, và so với baseline thị trường. **Cột mốc M6.**

---

## Giai đoạn 7 — Nhân quả và ra quyết định (buổi 38–40)

### Buổi 38 — Đo tác động của can thiệp

**Mục tiêu:** trả lời "chiến dịch/chính sách này có hiệu quả không, bao nhiêu" bằng dự báo phản thực tế.

**Học:**
- Dự báo ≠ nhân quả: mô hình dự báo tốt vẫn có thể cho câu trả lời nhân quả sai
- Kết quả tiềm năng (potential outcomes), **phản thực tế (counterfactual)**: "nếu không có chiến dịch thì sao"
- So trước/sau đơn giản và vì sao sai (mùa vụ, xu hướng, sự kiện đồng thời)
- **Interrupted time series** (hồi quy phân đoạn)
- **CausalImpact / BSTS**: dự báo phản thực tế từ chuỗi đối chứng không bị tác động
- **Difference-in-differences** và giả định xu hướng song song (kiểm bằng giai đoạn trước)
- **Synthetic control**: tổ hợp có trọng số của các đơn vị đối chứng; placebo test
- Kiểm định giả (placebo) theo thời gian và theo đơn vị; độ nhạy
- Dữ liệu mô phỏng có **đáp án biết trước** để kiểm phương pháp trước khi dùng dữ liệu thật

**Lab:**
1. Dữ liệu mô phỏng có hiệu ứng thật +12%: so trước/sau ra +30% (sai), CausalImpact ra ~12%
2. Lượt xem Wikipedia sau một sự kiện: CausalImpact với chuỗi đối chứng, placebo test
3. Synthetic control kinh điển: luật thuế thuốc lá California (Prop 99)
4. DiD cho một chính sách, kiểm xu hướng song song bằng biểu đồ event study

**Dữ liệu:** dữ liệu mô phỏng có đáp án (sinh trong buổi); Wikimedia Pageviews (CC0); dữ liệu Prop 99
của Abadie et al. (công khai cho nghiên cứu, có trong các gói synthetic control).

**Xong khi:** phương pháp khôi phục đúng hiệu ứng đã cài trong dữ liệu mô phỏng (sai số < 3 điểm %),
và kết quả trên dữ liệu thật qua được placebo test.

### Buổi 39 — Kịch bản và what-if

**Mục tiêu:** trả lời "nếu giảm giá 10% thì bán thêm bao nhiêu" — câu hỏi mà mô hình dự báo thông
thường trả lời sai dấu.

**Học:**
- Dự báo có điều kiện (conditional forecasting) vs dự báo dưới can thiệp
- **Nhiễu gây nhầm (confounding)**: giá thấp khi mùa thấp điểm → mô hình học "giá thấp → bán ít"
- **Độ co giãn giá**: log-log, ước lượng từ biến động giá ngoại sinh
- DAG nhân quả ở mức thực hành: vẽ ra trước khi chọn biến
- **Double/Debiased ML** (DoubleML/EconML) cho hiệu ứng có biến kiểm soát nhiều chiều
- Biến công cụ (IV) ở mức trực giác; thí nghiệm A/B và switchback cho dữ liệu thời gian
- **Kịch bản (scenario)**: kịch bản kinh tế, thời tiết, kế hoạch khuyến mãi; mô phỏng lan truyền qua mô hình
- Giao tiếp kịch bản: không phải xác suất, là "nếu–thì"

**Lab:**
1. Dữ liệu mô phỏng có confounding (mùa vụ điều khiển cả giá và cầu, độ co giãn thật −1.8):
   LightGBM + partial dependence ra độ co giãn **dương**
2. Sửa bằng hồi quy có kiểm soát mùa vụ → DoubleML → gần −1.8
3. Áp lên dữ liệu bán lẻ thật có biến động giá, báo khoảng tin cậy
4. Bảng 3 kịch bản giá × dự báo doanh số + doanh thu

**Dữ liệu:** dữ liệu mô phỏng có đáp án; UCI Online Retail II (CC BY 4.0); tuỳ chọn Dominick's
Finer Foods (Chicago Booth Kilts Center — điều khoản học thuật, xem Phụ lục F).

**Xong khi:** trên dữ liệu mô phỏng, khôi phục độ co giãn thật trong ±0.2 và giải thích bằng DAG vì
sao mô hình dự báo thuần cho sai dấu.

### Buổi 40 — Từ dự báo đến quyết định

**Mục tiêu:** biến dự báo xác suất thành quyết định tối ưu và đo giá trị bằng tiền — rồi truyền đạt
cho người ra quyết định.

**Học:**
- **Bài toán newsvendor**: chi phí thiếu $c_u$, chi phí thừa $c_o$ → đặt hàng ở quantile
  $\frac{c_u}{c_u + c_o}$ — lý do chính để cần dự báo quantile
- **Safety stock** từ quantile nhu cầu trong lead time (không dùng công thức giả định chuẩn khi dữ liệu thưa)
- Mức phục vụ (service level): cycle service level vs fill rate
- Chính sách tồn kho (s, S), (R, S); mô phỏng Monte Carlo từ sample path
- Lập lịch nhân sự / điều độ từ dự báo xác suất
- **Forecast Value Added (FVA)**: mỗi bước (mô hình, chỉnh tay của người lập kế hoạch) có làm dự báo tốt hơn naive không
- **Điều chỉnh theo phán đoán**: khi nào con người thêm giá trị (thông tin mà mô hình không có) và khi nào phá hỏng
- **Chọn mô hình theo giá trị quyết định** chứ không theo MASE
- **Truyền đạt dự báo**: fan chart, khoảng thay cho một con số, kể chuyện bằng dữ liệu, dashboard
  cho người không chuyên, nói về bất định mà không làm mất niềm tin

**Lab:**
1. Newsvendor cho 500 SKU bằng quantile từ buổi 25, so với "đặt = dự báo trung bình" — tiền tiết kiệm
2. Mô phỏng chính sách (R, S) 1 năm với sample path — fill rate và tồn kho trung bình
3. Mô hình A thắng MASE, mô hình B thắng chi phí — trình bày cho "giám đốc chuỗi cung ứng"
4. FVA: dữ liệu có chỉnh tay mô phỏng của người lập kế hoạch — bao nhiêu phần trăm lần chỉnh làm tệ hơn
5. Dashboard fan chart 1 trang cho người không chuyên

**Dữ liệu:** M5 hoặc Car Parts (Monash, CC BY 4.0); tham số chi phí giả định công bố trong buổi.

**Xong khi:** chính sách từ dự báo quantile tiết kiệm chi phí có số tiền cụ thể so với dự báo điểm,
và một trang trình bày mà người không chuyên đọc đúng ý nghĩa của khoảng dự báo.

---

## Giai đoạn 8 — Production và MLOps (buổi 41–43)

### Buổi 41 — Pipeline dự báo tái lập

**Mục tiêu:** từ notebook sang pipeline chạy hằng ngày, chạy lại ra đúng kết quả, không rò rỉ.

**Học:**
- Kiến trúc hệ thống dự báo batch: nạp → kiểm tra → feature → huấn luyện → dự báo → lưu → phục vụ
- **Point-in-time**: lưu dữ liệu theo **thời điểm biết** (as-of), không ghi đè; vintage; feature store ở mức khái niệm
- **Kiểm tra dữ liệu** bằng pandera: schema, dải giá trị, độ trễ dữ liệu, tỷ lệ thiếu — **dừng pipeline khi sai**
- **Orchestration**: Prefect (hoặc Dagster) — task, retry, lịch chạy, backfill
- **Theo dõi thí nghiệm và phiên bản mô hình**: MLflow; phiên bản dữ liệu: DVC hoặc snapshot Parquet có ngày
- **Tính tái lập**: khoá phụ thuộc (uv.lock), seed, container, ghi `git sha` vào kết quả
- **Lưu dự báo đúng cách**: mỗi dự báo có `thoi_diem_du_bao`, `phien_ban_mo_hinh`, `ngay_du_lieu` — để chấm lại sau
- Backfill: tái tạo dự báo quá khứ đúng như lúc đó

**Lab:**
1. Chuyển notebook dự báo tải điện (cho sẵn, chạy tay, join không point-in-time) thành pipeline Prefect
2. Kho dữ liệu as-of dạng Parquet + DuckDB từ API EIA-930 chạy hằng ngày
3. pandera chặn một lô dữ liệu đổi đơn vị MWh → GWh
4. MLflow lưu mô hình + chỉ số + dữ liệu; chạy lại cùng ngày ra kết quả giống hệt
5. Backfill 30 ngày dự báo quá khứ, chấm lại

**Dữ liệu:** EIA-930 API (public domain, cần API key miễn phí); Open-Meteo Forecast API (CC BY 4.0).

**Xong khi:** `make du-bao NGAY=2026-08-01` chạy hai lần ra kết quả giống từng byte; pipeline dừng
đúng khi dữ liệu sai schema; backfill không dùng dữ liệu sau ngày dự báo.

### Buổi 42 — Phục vụ dự báo ở quy mô lớn

**Mục tiêu:** dự báo hàng trăm nghìn chuỗi trong thời gian hợp lý và phục vụ qua API.

**Học:**
- Đo trước khi tối ưu: profiling pipeline dự báo
- **Song song hoá**: vector hoá, `n_jobs` của statsforecast, polars, Ray / Dask / Spark (Fugue) cho nhiều máy
- Batch dự báo trước (precompute) vs dự báo theo yêu cầu (on-demand)
- **API dự báo**: FastAPI, tải mô hình một lần lúc khởi động, cache, validation đầu vào
- Đóng gói Docker, cấu hình qua biến môi trường
- Phục vụ foundation model: batch, lượng tử hoá, CPU vs GPU, độ trễ p95
- Chi phí mỗi triệu dự báo; chọn mô hình theo chi phí + độ chính xác
- Dashboard cho người dùng nghiệp vụ (Streamlit/Panel)

**Lab:**
1. 145.000 chuỗi web traffic: vòng for tuần tự (đo, ước lượng hàng giờ) → statsforecast `n_jobs` → Ray
2. mlforecast global trên toàn bộ tập < 15 phút trên máy 4 nhân
3. FastAPI trả dự báo + khoảng, load test bằng `locust`; sửa lỗi load mô hình mỗi request
4. Docker hoá API + dashboard Streamlit

**Dữ liệu:** Kaggle Web Traffic (Monash, CC BY 4.0).

**Xong khi:** dự báo toàn bộ 145.000 chuỗi dưới 15 phút trên máy 4 nhân; API p95 < 200 ms ở 50 request/giây.

### Buổi 43 — Giám sát, drift và retrain

**Mục tiêu:** biết mô hình hỏng trước khi người dùng biết, và có chính sách retrain dựa trên bằng chứng.

**Học:**
- Những thứ hỏng trong production: dữ liệu về trễ, đổi schema/đơn vị, cảm biến chết, **concept drift**
  (quan hệ thay đổi), **data drift** (phân phối đầu vào thay đổi), sự kiện chưa từng thấy
- **Giám sát dữ liệu đầu vào**: độ tươi (freshness), khối lượng, tỷ lệ thiếu, phân phối (PSI, KS, Wasserstein)
- **Giám sát chất lượng khi nhãn về trễ**: sai số theo cửa sổ trượt, so với baseline chạy song song (shadow)
- **Phát hiện bất thường dựa trên dự báo**: giá trị thực nằm ngoài khoảng dự báo (nối buổi 25–26),
  cảnh báo theo tỷ lệ vượt khoảng thay cho một điểm
- **Phát hiện thay đổi trực tuyến**: CUSUM, Page–Hinkley, ADWIN
- Cảnh báo không ồn: ngưỡng theo thống kê, gộp, mức độ nghiêm trọng
- **Chính sách retrain**: theo lịch vs theo sự kiện drift vs liên tục; đánh giá chính sách bằng backtest
- **Học trực tuyến** (river): cập nhật từng điểm
- Champion–challenger, rollback mô hình
- Runbook sự cố dự báo

**Lab:**
1. Phát lại (replay) 1 năm dữ liệu EIA-930 theo ngày, cài 4 sự cố: dữ liệu trễ 2 ngày, đổi đơn vị,
   một vùng mất dữ liệu, nắng nóng lịch sử
2. Dashboard giám sát: freshness, PSI đầu vào, sai số trượt, tỷ lệ vượt khoảng dự báo
3. ADWIN/Page–Hinkley bắt concept drift; cảnh báo dựa trên MAPE ngày (ồn) vs trên tỷ lệ vượt khoảng
4. So 3 chính sách retrain (hằng tháng, theo drift, học trực tuyến) trên cùng 1 năm replay
5. Viết runbook cho 4 sự cố

**Dữ liệu:** EIA-930 (public domain); UCI Beijing Multi-Site Air-Quality (CC BY 4.0).

**Xong khi:** giám sát bắt đủ 4 sự cố cài sẵn, mỗi sự cố trong ≤ 1 ngày dữ liệu, không quá 2 cảnh
báo giả/tháng; có bảng so 3 chính sách retrain bằng sai số và chi phí tính toán. **Cột mốc M7.**

---

## Buổi 44 — Dự án cuối

**Mục tiêu:** xây một hệ thống dự báo **thực tế từ đầu tới cuối** trên dữ liệu bẩn thật, chấm trên
**dữ liệu tương lai chưa tồn tại lúc nộp**, và bảo vệ trước "người ra quyết định".

Phát đề từ **sau buổi 24**, học viên làm dần; giai đoạn 4–8 bổ sung từng phần. Làm nhóm 2–3 người.

### Chọn một trong ba đề

| Đề | Bài toán | Dữ liệu | Quyết định | Chấm dự báo |
|---|---|---|---|---|
| **A. Bán lẻ** | Nhu cầu ngày, 28 ngày tới, đủ phân cấp SKU → cửa hàng → bang | M5 (tự tải) hoặc UCI Online Retail II | Lượng đặt hàng mỗi SKU × cửa hàng | WRMSSE + **chi phí tồn kho mô phỏng** |
| **B. Năng lượng** | Nhu cầu điện theo giờ, 1–7 ngày, 5 vùng điều độ | EIA-930 + thời tiết dự báo Open-Meteo/AIFS | Lượng công suất dự phòng đặt trước | Pinball loss 99 quantile kiểu GEFCom + so với dự báo của đơn vị điều độ |
| **C. Không khí** | PM2.5 theo giờ, 24–72 giờ, trạm Hà Nội và TP.HCM | OpenAQ + Open-Meteo + AIFS | Phát cảnh báo AQI "không tốt cho sức khoẻ" | CRPS + Brier score của cảnh báo vượt ngưỡng |

### Hạng mục bắt buộc

1. **Phiếu bài toán dự báo** (buổi 1): quyết định, tầm, độ chi tiết, chi phí sai hai chiều
2. **Báo cáo EDA** đầy đủ theo chuẩn dự án giữa chặng 1, mỗi nhận xét có bằng chứng
3. **Pipeline làm sạch + feature có test**, qua bài kiểm rò rỉ tự động
4. **Bậc thang mô hình trên cùng một backtest**: seasonal naive → thống kê → ML global →
   foundation model zero-shot → ensemble; có kiểm định ý nghĩa
5. **Dự báo xác suất đã calibrate** (conformal hoặc tương đương), có PIT/reliability diagram
6. **Quyết định quy ra tiền** (hoặc số ca cảnh báo đúng/sai với đề C), chọn mô hình theo giá trị quyết định
7. **Pipeline production**: point-in-time, kiểm dữ liệu, chạy lại ra đúng kết quả, lưu dự báo có phiên bản
8. **Giám sát**: freshness, drift, sai số trượt, tỷ lệ vượt khoảng; runbook
9. **Model card**: dữ liệu, giới hạn, trường hợp không nên dùng, rủi ro
10. **Buổi bảo vệ** 20 phút: 10 phút cho "giám đốc" không chuyên (fan chart, tiền), 10 phút hỏi đáp kỹ thuật
11. **ADR** (ghi quyết định kiến trúc) cho 3 lựa chọn lớn

### Thưởng (tối đa +20)

- +5 thắng dự báo của đơn vị điều độ (đề B) / thắng baseline hội đồng (đề A, C) trên dữ liệu tương lai
- +5 dự án có thành phần LLM hữu ích qua được test "không bịa số" (tin tức làm covariate, báo cáo tự sinh)
- +5 phân tích nhân quả có placebo test (hiệu quả khuyến mãi, tác động chính sách giao thông lên PM2.5)
- +5 một người ngoài không chuyên đọc dashboard và trả lời đúng 4/5 câu hỏi về bất định

### Cách chấm

- **Giai đoạn dự báo trực tiếp 2 tuần**: pipeline của nhóm chạy hằng ngày, dự báo lưu có dấu thời gian
  **trước** khi dữ liệu thật về. Không nộp lại, không chỉnh tay
- **"Ngày dữ liệu hỏng"**: giám khảo tiêm 3 sự cố vào nguồn dữ liệu trong giai đoạn trực tiếp (dữ liệu
  trễ, đổi đơn vị, trạm chết) — học viên không biết trước; chấm việc giám sát bắt được và xử lý
- **Rubric 100 + 20**: chấm tự động ~50 (sai số trên dữ liệu tương lai, calibration, tái lập, rò rỉ,
  test, giám sát bắt sự cố) + chấm tay ~50 (EDA và lập luận, quyết định và giá trị, bảo vệ, model card, ADR)
- Chi tiết: `du-an-cuoi/rubric.md`

---

## Đối chiếu với sách FPP

*Forecasting: Principles and Practice, the Pythonic Way* (otexts.com/fpppy) là sách đọc thêm xương
sống. Khoá phủ toàn bộ 15 chương và mở rộng thêm.

| Chương FPP | Buổi |
|---|---|
| 1. Getting started | 1 |
| 2. Time series graphics | 4 |
| 3. Time series decomposition | 5, 6 |
| 4. Time series features | 9 |
| 5. The forecaster's toolbox | 2, 14, 15 |
| 6. Judgmental forecasts | 37, 40 |
| 7. Time series regression models | 18 |
| 8. Exponential smoothing | 16 |
| 9. ARIMA models | 7, 17 |
| 10. Dynamic regression models | 18 |
| 11. Hierarchical and grouped time series | 28 |
| 12. Advanced forecasting methods | 18 (đa mùa vụ, Prophet), 20 (VAR), 29 (NNAR), 25 (bootstrap) |
| 13. Some practical forecasting issues | 10, 11, 19, 24 |
| 14. Neural networks | 29, 30, 31 |
| 15. Foundation forecasting models | 34, 35 |
| *Ngoài sách* | 3, 8, 12, 13, 21–23, 26, 27, 32, 33, 36, 38–43 |

## Checklist "đã giỏi chưa"

Trả lời được **không nhìn tài liệu**, kèm ví dụ số:

- [ ] Vẽ 8 biểu đồ chẩn đoán và đọc ra mùa vụ kép, điểm gãy, thay đổi phương sai
- [ ] Giải thích tại sao hai chuỗi có xu hướng tương quan 0.95 mà không liên quan gì nhau, và sửa bằng cách nào
- [ ] Phân biệt MCAR/MAR/MNAR với một ví dụ cảm biến, và nói phương pháp điền nào lệch ở loại nào
- [ ] Chỉ ra 5 kiểu rò rỉ tương lai và viết được test bắt chúng
- [ ] Nói khi nào MAPE, MASE, WAPE, pinball là chỉ số đúng
- [ ] Dựng backtest rolling origin và chứng minh nó trung thực hơn CV ngẫu nhiên
- [ ] Đọc ACF/PACF đoán bậc ARIMA; giải thích damped trend thường thắng
- [ ] Giải thích vì sao mô hình global thắng local khi có nhiều chuỗi
- [ ] Đọc PIT histogram và nói mô hình quá tự tin hay quá thận trọng
- [ ] Giải thích vì sao conformal thường hỏng trên chuỗi có drift và ACI sửa thế nào
- [ ] Nói khi nào foundation model thua LightGBM, và vì sao leaderboard có thể lừa
- [ ] Giải thích vì sao backtest bot LLM trên câu hỏi cũ cho điểm ảo
- [ ] Chứng minh bằng DAG vì sao mô hình dự báo cho độ co giãn giá sai dấu
- [ ] Đổi một dự báo quantile thành lượng đặt hàng tối ưu và nói tiết kiệm bao nhiêu tiền
- [ ] Thiết kế giám sát bắt được đổi đơn vị dữ liệu trong 1 ngày mà không ồn

## Sai lầm thường gặp

| Sai lầm | Hậu quả | Buổi sửa |
|---|---|---|
| Nhảy thẳng vào mô hình, bỏ qua EDA | Mô hình học lỗi dữ liệu, không ai biết | 4–13 |
| Chia train/test ngẫu nhiên, KFold ngẫu nhiên | Sai số đánh giá lạc quan gấp nhiều lần | 15 |
| Rolling mean centered, `filtfilt`, Kalman smoother làm feature | Backtest đẹp, production sụp | 12, 13 |
| Dùng thời tiết thực tế thay thời tiết dự báo | "Cái giá của rò rỉ" 10–30% sai số | 13, 30 |
| Chuẩn hoá / điền dữ liệu trên toàn bộ tập trước khi chia | Rò rỉ âm thầm | 10, 29 |
| Báo cáo MAPE cho chuỗi có số 0 | Chỉ số vô hạn hoặc vô nghĩa | 14 |
| Không có baseline seasonal naive | Không biết mô hình có thêm giá trị không | 14 |
| Xoá mọi điểm > 3σ | Xoá luôn Tết, khuyến mãi — sự kiện thật | 11 |
| fillna(0) cho ngày hết hàng / cảm biến mất | Dự báo thấp có hệ thống | 10, 19 |
| Tin tương quan giữa hai chuỗi có xu hướng | Chọn biến giải thích vô nghĩa | 8 |
| Log rồi exp ngược không hiệu chỉnh bias | Dự báo trung bình thấp có hệ thống | 5 |
| Chọn mô hình tốt nhất trên chính tập báo cáo | Kết quả báo cáo quá lạc quan | 24 |
| Khoảng dự báo từ giả định chuẩn trên dữ liệu lệch | Coverage 95% thực tế chỉ 70% | 2, 25 |
| Tin demo "AI đoán giá chính xác 99%" | Đó là naive trễ 1 bước | 21 |
| Tin bảng xếp hạng benchmark của bài báo | Protocol sai, baseline yếu, dữ liệu rò | 31, 35 |
| Backtest LLM trên sự kiện trước mốc cắt kiến thức | Điểm Brier ảo | 37 |
| Dùng mô hình dự báo để trả lời câu hỏi "nếu làm X thì sao" | Sai dấu vì confounding | 39 |
| Đặt hàng bằng dự báo trung bình | Bỏ qua chi phí bất đối xứng, mất tiền | 40 |
| Notebook chạy tay làm "production" | Không tái lập, không ai biết khi hỏng | 41, 43 |

## Tài nguyên

**Sách:**
- Hyndman & Athanasopoulos et al. — *Forecasting: Principles and Practice, the Pythonic Way* (2025, miễn phí, otexts.com/fpppy)
- Petropoulos et al. — *Forecasting: theory and practice* (International Journal of Forecasting, 2022, bài tổng quan miễn phí)
- Tetlock & Gardner — *Superforecasting* (2015)
- Shumway & Stoffer — *Time Series Analysis and Its Applications* (lý thuyết sâu hơn)
- Angelopoulos & Bates — *A Gentle Introduction to Conformal Prediction* (miễn phí)
- Hernán & Robins — *Causal Inference: What If* (miễn phí)
- Kleppmann — *Designing Data-Intensive Applications* (cho giai đoạn 8)

**Benchmark và cuộc thi:**
- M1–M6 competitions (IIF), Monash Time Series Forecasting Repository (forecastingdata.org)
- GIFT-Eval, fev-bench (foundation model); ForecastBench (dự báo sự kiện)
- GEFCom 2012/2014/2017 (năng lượng); WeatherBench 2 (thời tiết)
- Kaggle: M5, Web Traffic, Favorita, Rossmann (đọc lời giải top)

**Thư viện:** Nixtla (statsforecast, mlforecast, neuralforecast, hierarchicalforecast, utilsforecast),
statsmodels, sktime, darts, GluonTS, AutoGluon-TimeSeries, MAPIE, PyMC, PyPOTS, ruptures,
PyWavelets, Chronos, TimesFM, TimeCopilot.

**Cộng đồng:** International Institute of Forecasters (IIF, tạp chí IJF, hội nghị ISF), blog
Hyndsight, Nixtla blog, Metaculus/Good Judgment Open để luyện dự báo sự kiện.

## Học theo cụm

Mỗi buổi tự chứa nên khoá cắt được theo nhiều cách:

| Cụm | Buổi | Cho ai |
|---|---|---|
| **Lõi phân tích dữ liệu chuỗi thời gian** | 1–15 | Data analyst — không cần mô hình phức tạp vẫn làm việc được |
| **Dự báo thống kê chuẩn nghề** | 1–4, 6, 7, 13–19, 25, 28 | Người lập kế hoạch, supply chain |
| **ML engineer dự báo** | 3, 4, 13–15, 22–26, 29–31, 34, 35, 41–43 | Kỹ sư ML đã biết Python/ML |
| **Nghiên cứu / deep learning** | 14, 15, 25, 29–35 | Người đọc và viết paper |
| **LLM forecasting** | 1, 2, 14, 25, 34–37 | Kỹ sư LLM, người làm agent |
| **Nghiệp vụ & ra quyết định** | 1, 2, 4, 14, 19, 25, 38–40 | Quản lý, phân tích kinh doanh |
| **Workshop 1 ngày "đừng tự lừa mình"** | 8, 13, 15, 21 | Bất kỳ ai đang dự báo |
