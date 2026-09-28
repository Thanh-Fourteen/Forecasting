# Nhật ký research — Buổi 31: Transformer cho chuỗi thời gian

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-25
- **Người/phiên:** Phase 28 (RS — chưa soạn). Phase 30 đọc file này, chỉ rà bổ sung.

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Zeng, A., Chen, M., Zhang, L., Xu, Q. (2023). Are Transformers Effective for Time Series Forecasting? *AAAI 2023*. arXiv:2205.13504 ; mã https://github.com/cure-lab/LTSF-Linear (commit `0c113668a3b8`, 2024-01-27) | bài gốc | 2026-09-25 | DLinear/NLinear |
| 2 | Nie, Y. et al. (2023). A Time Series is Worth 64 Words: Long-term Forecasting with Transformers. *ICLR 2023*. arXiv:2211.14730 ; mã https://github.com/yuqinie98/PatchTST (commit `204c21efe0b3`, 2023-08-11) | bài gốc | 2026-09-25 | PatchTST: patch + channel independence |
| 3 | Liu, Y. et al. (2024). iTransformer: Inverted Transformers Are Effective for Time Series Forecasting. *ICLR 2024*. arXiv:2310.06625 ; mã https://github.com/thuml/iTransformer (commit `c2426e68ca13`, 2025-07-17) | bài gốc | 2026-09-25 | attention giữa các biến |
| 4 | Chen, S.-A. et al. (2023). TSMixer: An All-MLP Architecture for Time Series Forecasting. *TMLR* 09/2023. arXiv:2303.06053 | bài gốc | 2026-09-25 | trộn theo thời gian và theo kênh |
| 5 | Wu, H. et al. (2021). Autoformer. *NeurIPS 2021*. arXiv:2106.13008 ; Zhou, H. et al. (2021). Informer. *AAAI 2021* | bài gốc | 2026-09-25 | phần lịch sử (ngắn) |
| 6 | Qiu, X. et al. (2024). TFB: Towards Comprehensive and Fair Benchmarking of Time Series Forecasting Methods. *PVLDB* 17. arXiv:2403.20150 (bản sửa 2025-08-18) | phản biện/benchmark | 2026-09-25 | **"Drop Last" trick**: ETTh2, test dài 2.880, look-back 512, h = 336; batch 32/64/128 bỏ mẫu cuối 17/49/113; MSE khi bật drop_last thay đổi theo batch size: PatchTST 0,4203 (batch 1) → 0,3483 (512), DLinear 0,4874 → 0,4251, FEDformer 0,4120 → 0,3736 (Bảng 2). "No existing MTSF benchmark has evaluated statistical methods" |
| 7 | Brigato, L. et al. (2025/2026). Position: There are no Champions in Supervised Long-Term Time Series Forecasting. *TMLR*. arXiv:2502.14045 (bản sửa 2026-01-09) | phản biện | 2026-09-25 | 8 mô hình × 14 bộ dữ liệu, ~5.000 mạng: đổi nhẹ thiết lập (look-back, tìm siêu tham số, chỉ số) là đổi hạng — "không có nhà vô địch" |
| 8 | Moretti, V., Marisca, I., Alippi, C., Cini, A. (2026). Position: Current Benchmarking Hinders Real Progress in Deep Learning for Time Series Forecasting. *ICML 2026*. arXiv:2512.22702 | phản biện | 2026-09-25 | "chi tiết cài đặt" (toàn cục/cục bộ, chuẩn hoá) ảnh hưởng hơn lớp mô hình chuỗi; đề xuất "forecasting model card" |
| 9 | Wang, Y. et al. (2025). Exploring Accuracy Law for Deep Time Series Forecasters. arXiv:2510.02729 | phân tích | 2026-09-25 | cải thiện trên benchmark chuẩn chỉ còn cận biên; nhiều bộ đã "bão hoà" |
| 10 | Shchur, O. et al. (2025). fev-bench. arXiv:2509.26468 ; Qiao, Z. et al. (2026). It's TIME. arXiv:2602.12147 ; Garza, A. et al. (2026). Impermanent: A Live Benchmark. arXiv:2603.08707 | benchmark mới | 2026-09-25 | xu hướng: bootstrap CI + win rate/skill score; dữ liệu mới, đánh giá "sống" theo thời gian — nối buổi 34–35 |
| 11 | thuml/Time-Series-Library README (commit `4e938a176710`, 2026-04-18) | thư viện nghiên cứu | 2026-09-25 | bảng xếp hạng dừng ở 03/2024 (look-back 96: TimeXer, iTransformer, TimeMixer; look-back tìm kiếm: TimeMixer, PatchTST, DLinear); **04/2026: ngừng thêm tính năng** |
| 12 | Hewamalage, Ackermann, Bergmeir (2023) *DMKD* 37 | tổng quan | đã xác minh ở `buoi-15` | nguồn cho checklist đọc bài báo |

## Phiên bản đã xác minh

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| neuralforecast | 3.2.2 | có `DLinear`, `NLinear`, `PatchTST`, `iTransformer`, `TSMixer`/`TSMixerx`, `TimeMixer`, `TimeXer`, `SOFTS`, `xLSTM`, `XLinear` (3.1.5), `Informer`, `Autoformer`, `FEDformer`, `VanillaTransformer`. `PatchTST`, `DLinear`, `NLinear`, `iTransformer`, `TSMixer` **không nhận exog**; `iTransformer`, `TSMixer`, `TimeMixer`, `TimeXer`, `SOFTS` là **đa biến** (cần `n_series`) — kiểm bằng thuộc tính lớp `EXOGENOUS_*`, `MULTIVARIATE` |
| statsforecast | 2.1.1 | AutoETS, SeasonalNaive cho bảng |

## `drop_last` trong mã gốc (đã đọc `data_provider/data_factory.py`, 2026-09-25)

| Repo | `flag == 'test'` → `drop_last` |
|---|---|
| PatchTST (`yuqinie98/PatchTST`, PatchTST_supervised) | **True** |
| iTransformer (`thuml/iTransformer`) | **True** |
| DLinear (`cure-lab/LTSF-Linear`) | False |
| Time-Series-Library (`thuml`, bản hiện tại) | False (đã sửa) |

→ Trong bảng của các bài gốc, **PatchTST/iTransformer và DLinear không được chấm trên cùng tập test**. Chỗ hở cố ý của buổi 31 là tái hiện đúng chuyện này —
có nguồn thật để trỏ tới, không phải ví dụ bịa.

## Phát hiện mới / lỗi hiểu sai phổ biến

- **SOTA 12 tháng gần (09/2025 → 09/2026): không có kiến trúc học có giám sát nào thắng rõ và bền** (bài 7, 8, 9; TSLib ngừng cập nhật bảng xếp hạng).
  Nghiên cứu dịch sang foundation model (buổi 34–35) và benchmark trung thực hơn. Ứng viên đã xem: TimeXer (NeurIPS 2024, exog), TimeMixer (ICLR 2024),
  xLSTM, SOFTS, TQNet (ICML 2025), DUET (KDD 2025) — mỗi bài tự báo cáo đứng đầu trên chính protocol của mình.
- "Lỗi thường gặp": chấm MSE trên dữ liệu đã chuẩn hoá z-score rồi so % cải thiện; chọn look-back/horizon có lợi; so với baseline yếu (không có seasonal naive/ETS).
- Checklist 10 câu của Lab 4 lấy từ bài 6, 7, 8 + Hewamalage 2023.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Prompt cho phép thay 1 kiến trúc bằng SOTA 12 tháng gần | — | **Không thay.** Không có ứng viên thắng bền; giữ DLinear/PatchTST/iTransformer/TSMixer. TimeXer/xLSTM/TimeMixer vào "Đọc thêm" (có trong neuralforecast) |
| Bẫy benchmark | nhỏ | thêm 2 phản biện 2025–2026 (bài 7, 8) và số thật của TFB (ETTh2) vào lý thuyết; trỏ đúng dòng `drop_last=True` trong repo gốc |
| Informer/Autoformer/FEDformer | nhỏ | giữ "ngắn gọn — lịch sử" như lộ trình |
