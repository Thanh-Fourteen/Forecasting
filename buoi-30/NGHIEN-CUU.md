# Nhật ký research — Buổi 30: N-BEATS, N-HiTS, DeepAR, TFT, TiDE

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-25
- **Người/phiên:** Phase 28 (RS — chưa soạn). Phase 29 đọc file này, chỉ rà bổ sung. Bảng thời gian/RAM của **cả cụm 29–33** nằm ở file này.

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Oreshkin, B.N., Carpov, D., Chapados, N., Bengio, Y. (2020). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. *ICLR 2020*. arXiv:1905.10437 | bài gốc | 2026-09-25 | khối MLP backcast/forecast, basis trend + seasonality |
| 2 | Challu, C. et al. (2023). N-HiTS: Neural Hierarchical Interpolation for Time Series Forecasting. *AAAI-23*. arXiv:2201.12886 | bài gốc | 2026-09-25 | nội suy đa tần số |
| 3 | Salinas, D., Flunkert, V., Gasthaus, J., Januschowski, T. (2020). DeepAR: Probabilistic forecasting with autoregressive recurrent networks. *IJF* 36(3). arXiv:1704.04110 | bài gốc | 2026-09-25 | RNN + likelihood, lấy mẫu tổ tiên |
| 4 | Lim, B., Arık, S.Ö., Loeff, N., Pfister, T. (2021). Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. *IJF* 37(4). arXiv:1912.09363 | bài gốc | 2026-09-25 | biến tĩnh/quá khứ/tương lai, variable selection, attention |
| 5 | Das, A., Kong, W., Leach, A., Mathur, S., Sen, R., Yu, R. (2023). Long-term Forecasting with TiDE: Time-series Dense Encoder. *TMLR*. arXiv:2304.08424 | bài gốc | 2026-09-25 | encoder–decoder MLP có covariate tương lai |
| 6 | neuralforecast — trang "Exogenous variables" https://nixtlaverse.nixtla.io/neuralforecast/docs/capabilities/exogenous_variables.html | tài liệu chính thức | 2026-09-25 | nguyên văn: **"Defining historic variables as future variables will lead to data leakage."**; `futr_df` phải phủ đủ tầm dự báo |
| 7 | neuralforecast 3.2.2 mã nguồn (`models/*.py`, `core.py`, `auto.py`, `losses/pytorch.py`) + release notes v3.1.5 → v3.2.2 | thư viện | 2026-09-25 | bảng hỗ trợ covariate, API diễn giải, Auto* |
| 8 | FPP-Py ch. 14 (xem `buoi-29/NGHIEN-CUU.md`) | sách | 2026-09-25 | khuôn stat/hist/futr exog, AutoNHITS |

## Phiên bản đã xác minh

Như `buoi-29/NGHIEN-CUU.md` (neuralforecast 3.2.2, torch 2.14.0 cpu, lightning 2.5.6, ray 2.58.0, pandas 2.3.3). Bổ sung:

| Hạng mục | Kết quả kiểm (thuộc tính lớp trong 3.2.2) |
|---|---|
| Covariate theo mô hình | `NBEATS` **không nhận exog** (dùng `NBEATSx`); `NHITS`, `TFT`, `TiDE`, `MLP`, `LSTM`, `TCN`: futr + hist + stat; **`DeepAR`: futr + stat, KHÔNG hist** |
| Diễn giải TFT | `model.feature_importances()` → dict `hist_vsn` / `future_vsn` / `static_vsn` (sau khi `predict`), `attention_weights()`, `feature_importance_correlations()` |
| `nf.explain()` (v3.1.x) | cần gói `captum` — **không có** trong bảng chung → không dùng; TFT có diễn giải sẵn là đủ |
| Phân phối | `DistributionLoss("NegativeBinomial" \| "Poisson" \| "StudentT" \| "Normal" …)`, `Tweedie` |
| Auto* | 36 lớp `Auto*`; `backend="ray" \| "optuna"`; v3.1.7 có **time budget**; v3.2.0 bỏ `cpus/gpus` → `ray_options` |
| Tính năng mới liên quan | v3.1.6 `simulate()` (sample path, dùng buổi 32); v3.1.7 `sample_weight`, validation df riêng; v3.2.2 báo lỗi khi loss = inf |

## Dữ liệu

Không cần bộ mới: `eia930-balance-*` (public domain) + `open-meteo-du-bao-luu-{ciso,erco,miso,nyis,pjm}-2024-2025` (CC BY 4.0, đã chốt sha256) có đúng hai
cột Lab 2 cần: `temperature_2m` (lượt chạy mới nhất ≈ thực tế, chỉ biết SAU) và `temperature_2m_previous_dayK` (đã dự báo trước K ngày — feature hợp lệ).
`monash-electricity-hourly` **không có nhiệt độ** → Lab 1/2 dùng EIA-930 + Open-Meteo; Electricity dùng cho phần không covariate.

## Phát hiện mới / lỗi hiểu sai phổ biến

- **DeepAR của neuralforecast đưa trung bình trở lại làm đầu vào** (không lấy mẫu tổ tiên) → khoảng tầm xa dễ hẹp; Lab 4 "kiểm calibration" nên đo
  coverage **theo tầm** để thấy điều này (chi tiết `buoi-32/NGHIEN-CUU.md`).
- DeepAR không nhận `hist_exog` → khai nhiệt độ quá khứ cho DeepAR sẽ báo lỗi; đừng "sửa" bằng cách khai thành `futr_exog` (đúng chỗ hở cố ý của buổi).
- Log Lightning/Ray ồn và import lạnh ~40 s (xem buổi 29).

## Thời gian + RAM trên CPU — cả cụm 29–33 (đo thật 2026-09-25)

Cấu hình chung: `torch.set_num_threads(4)`, mỗi mô hình một tiến trình, **trần RAM 6 GB** (`systemd-run -p MemoryMax=6G`), seed 0; Electricity 321 chuỗi
× 8.760 giờ (2014), `h=24`, `input_size=168`, `max_steps=500`, `scaler_type="standard"`, còn lại mặc định (`windows_batch_size=1024`, `batch_size=32`).
MAE trên **một** ngày cuối — chỉ định cỡ (một mốc cắt, chưa tune), không phải bảng so sánh. Seasonal naive 24 h: **290,3**.

| Mô hình (buổi) | Huấn luyện (s) | RAM đỉnh (MB) | Tham số | MAE 1 ngày |
|---|---|---|---|---|
| MLP (29) | 113,6 | 1.321 | 1,25 M | 256,9 |
| LSTM (29) | 213,4 | 1.406 | 0,22 M | 286,9 |
| TCN (29) | 174,3 | 1.333 | 0,15 M | 247,3 |
| N-BEATS (30) | 137,3 | 1.313 | 2,78 M | 266,8 |
| N-HiTS (30) | 66,2 | 1.328 | 2,82 M | 278,0 |
| DeepAR, StudentT (30) | **660,2** | 3.034 | 0,20 M | 376,2 (thua seasonal naive) |
| TFT mặc định `windows_batch_size=1024` (30) | — | **> 6.144 → bị giết** | — | — |
| TFT `windows_batch_size=256` (30) | **570,4** | 3.179 | 0,87 M | 306,5 (thua seasonal naive) |
| TiDE (30) | 65,9 | 1.318 | 1,50 M | 244,4 |
| DLinear (31) | 41,6 | 1.280 | 8.112 | 301,7 |
| NLinear (31) | 41,6 | 1.301 | 4.056 | 339,7 |
| PatchTST (31) | 419,0 | 2.224 | 0,47 M | 252,4 |
| iTransformer (31, đa biến) | **1.157,1** | 2.996 | 6,40 M | 237,5 |
| TSMixer (31, đa biến) | 76,4 | 1.187 | 0,58 M | 238,5 |
| TimeMixer (Đọc thêm, đa biến) | 61,4 | 1.188 | 0,37 M | 242,2 |
| TimeXer (Đọc thêm) mặc định | — | **> 6.144 → bị giết** | — | — |
| xLSTM (Đọc thêm) | — | — | — | **không chạy**: cần gói ngoài `xlstm` + `mlstm_kernels` + `ninja` |

Đọc bảng: tổng 5 kiến trúc buổi 30 (không kể TFT mặc định) ≈ **25 phút** huấn luyện một lần trên 321 chuỗi; DeepAR + TFT chiếm 82% thời gian
và RAM gấp đôi → Lab buổi 30 phải dùng tập con (EIA-930 chỉ vài vùng điều độ là đủ nhỏ) và `windows_batch_size` ≤ 256 cho TFT. Ở buổi 31, iTransformer
chậm gấp ~15 lần TSMixer mà MAE ngang → bằng chứng thật cho mục "chi phí huấn luyện vs lợi ích".

Phép đo khác của cụm (cùng ngày, `torch.set_num_threads(4)`, trần RAM 4 GB):

| Mô hình | Dữ liệu | Huấn luyện | RAM đỉnh | Kết quả định cỡ |
|---|---|---|---|---|
| GNN tự viết, PyTorch thuần (buổi 33): 2 lớp trộn láng giềng qua ma trận kề dày 862×862 (8 láng giềng tương quan nhất, tính **trên đoạn train**), 1.000 bước, lô 32 | Traffic 862 cảm biến, 10 tuần train / 2 tuần test, `L=168`, `h=24` | 43,1 s | 525 MB | MAE (chuẩn hoá z) GNN 0,335; **MLP từng cảm biến 0,295**; seasonal naive 168 h 0,375 → GNN ngây thơ **thua** mô hình không đồ thị — cần nêu trung thực |
| Khuếch tán kiểu CSDI thu nhỏ (buổi 32): 4 khối tích chập 2D (trạm × thời gian), 32 kênh, 50 bước khuếch tán, 3.000 vòng × lô 64 | UCI Beijing PM2.5 12 trạm, log1p + z, 24 h điều kiện → 12 h dự báo | 132,0 s + lấy mẫu 3.000 quỹ đạo 52,7 s | 1.093 MB | MAE z của trung vị 0,455 vs giữ giá trị cuối 0,438 → **chưa thắng** baseline; Phase 30 tinh chỉnh (lịch nhiễu, số vòng) trước khi chốt Lab 2 |

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| TFT mặc định vượt 6 GB RAM trên 321 chuỗi | nhỏ (cấu hình) | cấu hình khoá `windows_batch_size=256` (3,2 GB); cấu hình 8 GB dùng tập con chuỗi |
| DeepAR + TFT ~20 phút / lần trên 321 chuỗi, cả hai thua seasonal naive ở mốc cắt thử | nhỏ | giữ trong bài (lộ trình đã yêu cầu bảng "kể cả khi DL thua"); `check` < 10 phút chạy tập con, số đầy đủ ghi từ lần chạy thật |
| "5 kiến trúc … trên tải điện + nhiệt độ" | nhỏ | EIA-930 + Open-Meteo previous-runs đã trong danh mục; Electricity không có nhiệt độ |
| DeepAR không có sample path thật / không nhận hist exog | nhỏ ở buổi 30 (lớn ở buổi 32) | buổi 30: đo coverage theo tầm; buổi 32: xem `buoi-32/NGHIEN-CUU.md` |
| Diễn giải: `nf.explain()` cần `captum` | nhỏ | dùng `TFT.feature_importances()` / `attention_weights()` có sẵn; basis N-BEATS qua `NBEATS(stack_types=["trend","seasonality"])` |

## Rà bổ sung và số liệu Phase 29 (2026-09-25)

Research Phase 28 cùng ngày → không rà lại phiên bản. `sinh_nen.py 30`: {neuralforecast 3.2.2, torch 2.14.0+cpu, statsforecast 2.1.1, mlforecast
1.1.0, lightgbm 4.7.0, pandas 2.3.3} resolve không xung đột. Dữ liệu: `eia930-balance-2024-h1…2025-h2`, `open-meteo-du-bao-luu-{ciso,erco,miso,
nyis,pjm}-2024-2025`, `uci-bike-sharing` (bài tập), mọi sha256 khớp.

**Dữ liệu.** 5 vùng × 16.800 giờ (2024-02-01 → 2025-12-31, UTC, nhãn cuối giờ). Thiếu 0–96 giờ/vùng; 5 giờ nhu cầu lỗi (≤ 0 hoặc lệch > 50%
so với trung vị 25 giờ TRƯỚC) → lấp bằng cùng giờ tuần trước. Làm sạch chỉ nhìn quá khứ (`lam_sach`, có test `kiem_ro_ri`) — bản nháp đầu dùng
trung vị căn giữa + nội suy hai chiều (rò rỉ, đúng lỗi của buổi 10/12) → đã sửa trước khi đo. `temperature_2m_previous_day1` trống tới 2024-01-19
→ bắt đầu từ 2024-02-01. neuralforecast kiểm NaN trên MỌI cột của `df` (kể cả cột không dùng) → `_cot(m)` chỉ đưa cột mô hình khai báo.

**Cấu hình CPU (đo thật).** Mặc định (500 bước, `windows_batch_size` 1024, kiểm val mỗi 50 bước): TFT 998 s / 4,2 GB, DeepAR 528 s, TiDE 374 s,
N-HiTS 55 s, N-BEATS 22 s. Rút gọn (300 bước, lô 256 cửa sổ, kiểm val mỗi 100 bước, kiên nhẫn 3; TFT `hidden_size` 32, TiDE 128, DeepAR 50 quỹ
đạo): TFT 179 s / 3,0 GB, DeepAR 91 s / 2,8 GB, TiDE 30 s, N-HiTS 20 s, N-BEATS 9 s. `nf.predict` 37 mốc: ~1 s/mô hình (trainer được cache, v3.1.6).

**Bảng chính** (37 mốc 00:00 UTC cách 5 ngày, 2025-07-01 → 2025-12-28, h = 24, MASE mẫu số seasonal naive tuần trên train < 2025-05-01; seed 0):

| | CISO | ERCO | MISO | NYIS | PJM | TB | giây |
|---|---|---|---|---|---|---|---|
| SeasonalNaive | 1,046 | 0,805 | 1,023 | 1,198 | 0,960 | 1,006 | 0 |
| EIA (day-ahead của vùng) | 1,258 | 0,292 | 0,375 | 0,542 | 0,403 | 0,574 | — |
| MSTL (8 tuần, học lại mỗi mốc) | 0,538 | 0,394 | 0,366 | 0,461 | 0,380 | 0,428 | 59 |
| LightGBM (lag ≥ 24 + nhiệt dự báo + giờ, thứ) | 0,495 | 0,383 | 0,375 | 0,582 | 0,395 | 0,446 | 2 |
| N-BEATS | 0,528 | 0,303 | 0,334 | 0,512 | 0,331 | 0,402 | 9 |
| N-HiTS | 0,496 | 0,332 | 0,288 | 0,474 | 0,300 | **0,378** | 20 |
| DeepAR (Student-t, trung vị) | 0,899 | 0,504 | 0,470 | 0,660 | 0,575 | 0,622 | 91 |
| TFT | 0,706 | 0,391 | 0,410 | 0,571 | 0,384 | 0,492 | 179 |
| TiDE | 0,589 | 0,358 | 0,447 | 0,621 | 0,424 | 0,488 | 30 |

Hai lần chạy (prototype + `ve_hinh.py`) ra đúng cùng bảng. Ngược buổi 29: ở đây N-HiTS/N-BEATS thắng MSTL và LightGBM. EIA day-ahead của CISO
thua cả seasonal naive (MAPE 7,8%) — dự báo "chính thức" không phải lúc nào cũng tốt.

**Rò rỉ `futr_exog` (N-HiTS)** — cái giá NHỎ hơn lộ trình giả định:

| Cấu hình | MASE TB |
|---|---|
| nhiệt độ THỰC khai futr, chấm bằng nhiệt độ thực (backtest rò rỉ) | 0,355 |
| cùng mô hình, lúc vận hành chỉ có nhiệt độ dự báo | 0,364 |
| khai đúng (dự báo → futr, thực → hist) | 0,378 |
| không dùng nhiệt độ | 0,380 |

Nhiệt độ dự báo trước 1 ngày chỉ lệch nhiệt độ thực ~1,2–1,3 °C (MAE) → ở tầm 24 giờ, backtest rò rỉ đẹp giả ~2,5% so với vận hành; nhiệt độ gần
như không thêm gì khi đã có 168 giờ nhu cầu. Mô hình "học bằng số thực, chạy bằng số dự báo" (0,364) còn nhỉnh hơn mô hình khai đúng (0,378) —
một seed, chênh nhỏ; bài học đúng là "con số báo cáo phải chấm bằng đúng đầu vào lúc vận hành", không phải "rò rỉ luôn làm mô hình tệ". Tầm xa
(tuần) sai nhiệt độ lớn hơn → cái giá lớn hơn: để bài tập.

**DeepAR cho dữ liệu đếm (xe đạp, 30 mốc từ 2012-10-01, h = 24, 200 bước, dữ liệu từ 2012-04):**

| Phân phối, scaler | coverage 80% chung | giờ 1–6 | giờ 19–24 | MAE trung vị | cận dưới < 0 | giây |
|---|---|---|---|---|---|---|
| NegativeBinomial, identity | 0,194 | 0,589 | 0,039 | 267 | 0 | 293 |
| NegativeBinomial, robust | 0,275 | 0,006 | 0,367 | 199 | 0 | 203 |
| NegativeBinomial, standard | 0,242 | 0,006 | 0,300 | 199 | 0 | 346 |
| Poisson, robust | 0,128 | 0,117 | 0,117 | 107 | 0 | 187 |
| Normal, robust | 0,576 | 0,856 | 0,556 | 96 | 19,3% | 215 |

Mọi phân phối đếm của DeepAR (neuralforecast 3.2.2) hỏng calibration trên chuỗi này; Normal phủ thiếu và có cận âm. Nguyên nhân khả dĩ: giá trị
trung bình được đưa lại làm đầu vào (Phase 28) + tham số hoá phân phối đếm với số lớn (tới 977 lượt/giờ). **Quyết định:** Lab 4 lộ trình ("DeepAR âm
nhị thức cho dữ liệu đếm, kiểm calibration") đổi thành kiểm coverage của DeepAR ngay trên bảng chính (Student-t, không tốn thêm huấn luyện);
phân phối âm nhị thức dạy bằng ví dụ tay; thí nghiệm xe đạp thành bài tập kèm bảng trên làm lời cảnh báo.

## Đọc thử (2026-09-25, Phase 29, tự đọc — không subagent)

**Vòng 1** (toàn bộ `tai-lieu.md`, vai học viên mới; mọi số đối chiếu output `ve_hinh.py` + notebook chạy thật — hai lần chạy cho cùng bảng):

| # | Mục | Chỗ vướng | Mức | Sửa |
|---|---|---|---|---|
| 1 | 4.2 | "góp +4 cho giờ tới (giờ giữa là 0, giờ tới cách đó 2 bước)" khó theo | khó | viết lại: đường thẳng bằng 0 ở giờ giữa, giờ tới cách 2 bước → 2 × 2 = +4 |
| 2 | 3, 4.6 | "EIA" chưa giải thích | khó | "báo cáo EIA-930 của Cơ quan Thông tin Năng lượng Mỹ (EIA)" |
| 3 | 3 | "day-ahead" chưa định nghĩa | khó | "(dự báo cả ngày hôm sau, công bố từ hôm trước)" |
| 4 | 6 | "hiệu chỉnh ngoài mẫu" không trỏ buổi | khó | "nới khoảng bằng sai số ngoài mẫu (buổi 25–26)" |
| 5 | 4.3 | Tóm lại khuyên âm nhị thức cho số đếm trong khi bài tập cho thấy hỏng | khó (thiếu trung thực) | thêm câu "cần nhưng chưa đủ: bài tập 2 cho thấy vẫn phủ sai xa" |
| 6 | 3 vs Từ mới | PJM "Đông Bắc" vs "miền Đông quanh Philadelphia" | nhỏ | bỏ mô tả ở mục 3, trỏ bảng Từ mới |
| 7 | 4.6 Nâng cao | Optuna, Ray không định nghĩa | nhỏ | giữ (trong hộp Nâng cao; Optuna đã dạy buổi 23) |

Kết quả: **0 chặn, 5 khó (đã sửa), 2 nhỏ**. Mục B: covariate (ví dụ cửa hàng: giá niêm yết / số khách / tỉnh), backcast (1, 3, 5 → mức 3, dư −2, 0,
2, dốc 2 → dự báo 7), N-HiTS (nội suy giữa hai điểm), DeepAR (khoảng 80% của chuẩn 50 ± 1,28σ), cơ chế đưa trung bình trở lại (σ không cộng dồn),
TFT softmax, TiDE đếm đầu vào — đều giải thích được. Quiz làm mù 10/10: 1→4.1 bảng, 2→4.2 ví dụ, 3→4.3 dữ liệu đếm, 4→4.4 câu cuối, 5→4.3 ví dụ,
6→4.4 ví dụ, 7→4.2 N-HiTS, 8→4.1 ví dụ, 9→4.1 + 4.6, 10→4.3 hình. Đáp án tính lại bằng Python (Q5 z = 1,2816; Q6 0,422/0,422/0,155; Q7 39; Q8 1.000/940).

**Rà gọn:** 1 chỗ thừa đáng kể — Lab bước 4 chép lại ba số của bảng 4.1 → đổi thành "ba dòng đầu của bảng mục 4.1". Còn lại ≤ 3. `kiem_de_hieu.py 30`:
0 vi phạm (lượt đầu 22: 16 đoạn dồn số, 5 viết tắt tên vùng, 2 câu dài — sửa bằng bảng, phép tính đầy đủ, tách câu, bảng Từ mới).

**Vòng 2** (đọc lại toàn bộ sau khi sửa): không phát sinh chỗ vướng; 0 chặn, 0 khó, 2 nhỏ. Khoảng 4.300 chữ ngoài bảng/code; PDF 12 trang.
