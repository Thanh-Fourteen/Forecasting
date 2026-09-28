# Nhật ký research — Buổi 32: Mô hình sinh và dữ liệu tổng hợp

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-25
- **Người/phiên:** Phase 28 (RS — chưa soạn). Phase 30 đọc file này, chỉ rà bổ sung.

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Rasul, K., Seward, C., Schuster, I., Vollgraf, R. (2021). Autoregressive Denoising Diffusion Models for Multivariate Probabilistic Time Series Forecasting (TimeGrad). *ICML 2021*. arXiv:2101.12072 ; mã `zalandoresearch/pytorch-ts` (MIT, commit `7860c9693d55`, 2024-06-14) | bài gốc | 2026-09-25 | TimeGrad: RNN điều kiện + khử nhiễu từng bước |
| 2 | Tashiro, Y., Song, J., Song, Y., Ermon, S. (2021). CSDI: Conditional Score-based Diffusion Models for Probabilistic Time Series Imputation. *NeurIPS 2021*. arXiv:2107.03502 ; mã `ermongroup/CSDI` (**MIT**, commit `7f24a436f08d`, 2024-03-14) | bài gốc | 2026-09-25 | CSDI: che ngẫu nhiên → học điền; dự báo = điền phần tương lai |
| 3 | Su, C. et al. (2025). Diffusion Models for Time Series Forecasting: A Survey. arXiv:2507.14507 | tổng quan | 2026-09-25 | phân loại theo nguồn điều kiện; hạn chế chung: **suy luận chậm, phức tạp** |
| 4 | Ang, Y. et al. (2024). TSGBench: Time Series Generation Benchmark. *PVLDB* 17. arXiv:2309.03755 | benchmark | 2026-09-25 | bộ chỉ số fidelity (thống kê, khoảng cách, discriminative/predictive score) |
| 5 | Stenger, M. et al. (2025). STEB: In Search of the Best Evaluation Approach for Synthetic Time Series. arXiv:2505.21160 | phản biện | 2026-09-25 | xếp hạng 41 chỉ số; **cách nhúng chuỗi trước khi đo làm đổi điểm mạnh** → chọn ít chỉ số, giải thích được |
| 6 | Amorim, L. et al. (2026). Benchmarking Time Series Generation Methods for Privacy-Preserving Forecasting. arXiv:2608.10891 | benchmark | 2026-09-25 | TSTR trên 7 bộ: **không phương pháp nào thay được dữ liệu gốc**; độ chính xác TSTR và riêng tư (theo khoảng cách) **kéo ngược chiều nhau** |
| 7 | Ganev, G., De Cristofaro, E. (2025). The DCR Delusion: Measuring the Privacy Risk of Synthetic Data. *ESORICS 2025*. arXiv:2505.01524 | phản biện | 2026-09-25 | **khoảng cách tới bản ghi gần nhất (DCR) không đo được rủi ro riêng tư**: bộ "qua" DCR vẫn dễ bị membership inference |
| 8 | Pinson, P., Tastu, J. (2013). Discrimination ability of the Energy score. DTU Technical report https://orbit.dtu.dk/en/publications/discrimination-ability-of-the-energy-score ; Scheuerer, M., Hamill, T.M. (2015). Variogram-Based Proper Scoring Rules for Probabilistic Forecasts of Multivariate Quantities. *MWR* 143(4) https://journals.ametsoc.org/view/journals/mwre/143/4/mwr-d-14-00269.1.xml | bài gốc | 2026-09-25 (tóm tắt) | energy score kém nhạy với sai cấu trúc phụ thuộc → variogram score. **Đã kiểm bằng mô phỏng** (mục dưới) |
| 9 | neuralforecast 3.2.2 mã nguồn: `NeuralForecast.simulate()` (thêm ở v3.1.6 "Simulation paths", sửa Schaake shuffle ở v3.2.1), `common/_base_model.py::_predict_step_recurrent_single` | thư viện | 2026-09-25 | xem "Phát hiện" |
| 10 | scoringrules 0.11.0: `es_ensemble`, `vs_ensemble(p=0.5)`, `crps_ensemble` | thư viện | 2026-09-25 | chấm dự báo nhiều chiều |

## Phiên bản đã xác minh

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| neuralforecast | 3.2.2 | `nf.simulate(n_paths, method="gaussian_copula" \| "schaake_shuffle", seed)` → bảng dài `[unique_id, ds, sample_id, <mô hình>]`; cần mô hình có đầu ra quantile (`DistributionLoss`, `MQLoss`) |
| scoringrules | 0.11.0 (đã trong bảng chung) | |
| gluonts | 0.17.0 (Apache-2.0, PyPI 2026-07-31) | `gluonts[torch]` resolve được cùng neuralforecast 3.2.2 (91 gói; kéo thêm `lightning` 2.6.6 cạnh `pytorch-lightning` 2.5.6) — **chỉ là phương án dự phòng**, chưa thêm vào bảng chung |
| pypots | 1.5 (BSD-3) | có CSDI nhưng kéo `transformers<=4.57.6`, `tensorboard`, `tsdb`/`benchpots` (tải dữ liệu riêng) → **không dùng** |
| sdv 1.38.3 | **BUSL-1.1** (không phải giấy phép mở) | không dùng; tsgm 0.1.0 kéo keras/tensorflow → không dùng |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **DeepAR của neuralforecast KHÔNG sinh sample path thật.** Khi dự báo, mỗi bước lấy mẫu `trajectory_samples` giá trị để tính quantile, nhưng đưa
  **giá trị trung bình** (không phải từng mẫu) trở lại làm đầu vào bước sau (`insample_y = self.scaler.scaler(mean, …)`, `_base_model.py`). Hệ quả:
  (a) không có quỹ đạo nhất quán theo thời gian; (b) sai số không tích luỹ qua các bước → khoảng tầm xa dễ hẹp quá. DeepAR bài gốc lấy mẫu tổ tiên
  (ancestral sampling). → Lab 1 lộ trình ("sample path từ DeepAR") phải đổi cách làm (xem quyết định).
- **`nf.simulate()` là "copula" của lộ trình, có sẵn**: ghép các quantile theo từng bước bằng Gaussian copula AR(1) hoặc Schaake shuffle (lấy thứ hạng
  từ các đoạn lịch sử) → sample path có phụ thuộc. So với "quantile độc lập" đúng ý Lab 1.
- **Mô phỏng ES vs VS (seed 0, 2026-09-25):** chuỗi thật AR(1) ρ = 0,9, 14 bước; hai dự báo có **phân phối biên đúng như nhau**, một có phụ thuộc đúng,
  một độc lập giữa các bước; 400 lần × 100 quỹ đạo:

  | Điểm | Có phụ thuộc | Độc lập | Độc lập tệ hơn | t | Tỉ lệ lần phụ thuộc thắng |
  |---|---|---|---|---|---|
  | Energy score | 2,403 | 2,493 | 3,7% | 9,6 | 0,69 |
  | Variogram score (p = 0,5) | 18,91 | 30,72 | 62,5% | 27,1 | 0,91 |
  | CRPS của tổng 14 bước | 6,20 | 7,01 | 13,0% | 7,4 | 0,57 |

  → Energy score chỉ nhích 3,7% dù phụ thuộc rất mạnh; trên dữ liệu thật, sai lệch phân phối biên sẽ lấn át → tiêu chí "Xong khi" chỉ bằng energy score
  **dễ không đạt dù sample path đúng**. CRPS của đại lượng tích luỹ (tồn kho) là thước đo nghiệp vụ dễ hiểu nhất.
- **Khoảng cách gần nhất (DCR)**: đủ để bắt mô hình "chép nguyên chuỗi train" (chỗ hở cố ý), **không** đủ để kết luận "riêng tư" (bài 7) → nói rõ giới hạn
  trong tài liệu, không dạy DCR như thước đo riêng tư.
- TSTR: dữ liệu tổng hợp không thay được dữ liệu thật (bài 6) → kết luận mong đợi của Lab 3 là "TSTR thua TRTR", không phải "tổng hợp tốt như thật".
- CSDI trên CPU: mã gốc MIT, cấu hình gốc (4 lớp residual, 64 kênh, 50 bước khuếch tán, 200 epoch, 36 trạm) chạy GPU. **Đo thật bản thu nhỏ tự viết**
  (2026-09-25; 4 khối tích chập 2D, 32 kênh, 50 bước, 3.000 vòng × lô 64, UCI Beijing 12 trạm, 24 h → 12 h, 4 luồng): huấn luyện **132 s**, lấy mẫu
  3.000 quỹ đạo **53 s**, RAM **1,1 GB** → chạy được trên CPU. Nhưng MAE (z) của trung vị **0,455 thua** "giữ giá trị cuối" 0,438 → Phase 30 tinh chỉnh
  (lịch nhiễu, số vòng, kênh) và phải so với baseline trước khi chốt Lab 2; bảng thời gian cả cụm ở `buoi-30/NGHIEN-CUU.md`.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lab 1 "Sample path từ DeepAR vs quantile độc lập" — DeepAR của neuralforecast không có sample path thật | **lớn** (đổi cách làm lab) | **Đề xuất:** sample path từ `nf.simulate()` (Gaussian copula / Schaake shuffle) trên mô hình quantile vs quantile độc lập; cơ chế lấy mẫu tổ tiên dạy bằng một mạng LSTM–Gauss nhỏ **tự viết** (nối mã tự viết của buổi 29), GluonTS không thêm. Chờ người dùng chốt |
| "Xong khi: energy score cho thấy sample path có phụ thuộc thắng quantile độc lập" | **lớn** (tiêu chí có thể không đạt được một cách trung thực) | đổi thành: **variogram score + CRPS của tổng tích luỹ 14 ngày** thắng; energy score vẫn báo cáo, kèm giải thích vì sao nó nhích ít |
| Privacy/memorization | nhỏ | giữ khoảng cách gần nhất để bắt chép nguyên; thêm câu giới hạn (DCR ≠ riêng tư) |
| Normalizing flow | nhỏ | giữ ở mức trực giác (không có triển khai trong neuralforecast/bảng chung) |
