# Nhật ký research — Buổi 33: Không gian–thời gian và thời tiết AI

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-25
- **Người/phiên:** Phase 28 (RS — chưa soạn). Phase 31 đọc file này, chỉ rà bổ sung (**rà lại phiên bản AIFS nếu soạn sau 2026-10-25**).

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | ECMWF Open Data https://www.ecmwf.int/en/forecasts/datasets/open-data | tài liệu chính thức | 2026-09-25 | AIFS Single + AIFS ENS: 4 lượt/ngày (00/06/12/18 UTC), tới 360 h, bước 6 h, lưới 0,25°, GRIB2 (nén CCSDS từ 07/2023); máy chủ ECMWF chỉ giữ **12 lượt gần nhất**, bản sao trên AWS/Azure/GCP. **Giấy phép: "Creative Commons CC-BY-4.0 licence and the ECMWF Terms of Use … may be redistributed and used commercially, subject to appropriate attribution."** 05/2026: bỏ stream `scda`/`scwv`, 06z/18z dùng `oper`/`wave`, thêm mức 10 hPa |
| 2 | ECMWF news 2026-05-12 "Significant update … IFS Cycle 50r1 and AIFS v2 goes live" https://www.ecmwf.int/en/about/media-centre/news/2026/ifs-cycle-50r1-aifsv2-live | chính thức | 2026-09-25 | **AIFS v2 vận hành từ lượt 06 UTC 12/05/2026** (cùng IFS 50r1): thêm sóng biển (11 biến), tuyết phủ |
| 3 | Model card `ecmwf/aifs-single-2.0` (HF revision `08286fc247419bc40666226c816ad4ac686d2a8b`, 2026-05-18) | model card | 2026-09-25 | **pre-train ERA5 1979–2022; fine-tune phân tích vận hành + esuite 50r1 2018–2024**; ~31 km (N320), 14 mức áp; trọng số CC BY 4.0; checkpoint 994 MB; huấn luyện 16 GPU GH200 |
| 4 | Model card `ecmwf/aifs-single-1.1` (revision `049b9ab1ccac3382b6332870ae550fd20a432faf`) ; ECMWF: AIFS Single v1.0 vận hành 2025-02-25, v1.1 từ lượt 06 UTC 2025-08-27 (sửa lỗi mưa) | model card / chính thức | 2026-09-25 | v1.1: pre-train ERA5 1979–2022, fine-tune 2016–2022 (GMD 19, 4703, 2026; arXiv:2509.18994) |
| 5 | ECMWF AIFS blog 05/2026 "Farewell to the external AI models" | chính thức | 2026-09-25 | ECMWF **ngừng chạy GraphCast, FourCastNet, Pangu-Weather, Aurora** từ 50r1: mô hình có fine-tune (GraphCast, Aurora) giảm chất lượng khi điều kiện đầu đổi — ví dụ thật về dịch phân phối đầu vào |
| 6 | Google, WeatherNext models https://developers.google.com/weathernext/guides/models | chính thức | 2026-09-25 | **WeatherNext 3 (08/2026)**: 0,25° mức áp, 0,1° bề mặt, 64 thành viên, khởi tạo mỗi giờ. WeatherNext 2 (FGN, 64 thành viên), WeatherNext 1 Gen (= GenCast, diffusion), 1 Graph (= GraphCast). Dữ liệu qua BigQuery/Earth Engine/GCS; dữ liệu cũ > 1 h: CC BY 4.0, thời gian thực: điều khoản thử nghiệm riêng → **không dùng trong lab** (cần tài khoản Google Cloud) |
| 7 | WeatherBench 2 https://sites.research.google/gr/weatherbench/ ; Rasp, S. et al. (2024). WeatherBench 2. *JAMES*. arXiv:2308.15560 | benchmark | 2026-09-25 | bảng điểm năm **2022**; mô hình ML chấm với **ERA5**, mô hình vận hành chấm với phân tích IFS; RMSE/ACC, CRPS, SEEPS (mưa); **không có điểm theo trạm**; mã chấm mới: WeatherBench-X. AIFS/WeatherNext 2 không có trên trang |
| 8 | Open-Meteo Previous Runs API https://open-meteo.com/en/docs/previous-runs-api, model `ecmwf_aifs025_single` | dịch vụ | 2026-09-25 (gọi thử) | dự báo AIFS **theo điểm**: `temperature_2m_previous_dayK`, **K = 1…7** (K = 8, 10 trả toàn null); có dữ liệu từ **~2025-02-26** (2025-02-10 null); ô lưới gần Nội Bài: 21,25° N 105,75° E, cao 13 m. Giá trị theo giờ = nội suy từ bước 6 h của AIFS |
| 9 | NOAA GHCNh, tệp năm `GHCNh_VMI0000VVNB_2026.parquet` | dữ liệu | 2026-09-25 (tải thật) | 12.614 dòng, 329 cột, **cập nhật hằng ngày** (Last-Modified 2026-09-24, dữ liệu tới 2026-09-22 22:30 UTC); bản tin nửa giờ (METAR), **nhiệt độ làm tròn tới 1 °C** |
| 9b | Tệp `.index` lượt AIFS Single 2026-09-20 00z, bước 24 h (GCS `ecmwf-open-data/…/aifs-single/0p25/oper/`) | dữ liệu | 2026-09-25 (đọc thật) | **122 trường/bước**: bề mặt `2t, 2d, 10u, 10v, 100u, 100v, msl, sp, skt, tp, cp, sf, tcc, lcc, mcc, hcc, tcw, ssrd, strd, fscov, rowe`; mức áp `gh, q, t, u, v, w, z` × 14 mức (10…1000 hPa); đất `sot, vsw`. Trường `2t` = **548.133 byte** → lấy bằng byte-range theo `_offset/_length`; bước 360 h có |
| 10 | PyG wheel index https://data.pyg.org/whl/torch-2.14.0+cpu.html ; PyPI `torch-geometric-temporal` 0.56.2 (2025-07-16) | thư viện | 2026-09-25 | xem "Phiên bản" |
| 11 | Li, Y. et al. (2018). DCRNN. *ICLR 2018* ; Yu, B. et al. (2018). STGCN. *IJCAI* ; Wu, Z. et al. (2019). Graph WaveNet. *IJCAI* | bài gốc | theo lộ trình, chưa đọc lại | Phase 31 đọc lại phần trực giác |

## Phiên bản đã xác minh

| Thư viện / model | Phiên bản / revision | Ghi chú |
|---|---|---|
| AIFS Single (lượt chạy đang phát) | **v2** từ 2026-05-12 06 UTC; v1.1 2025-08-27 → 2026-05-12; v1.0 2025-02-25 → 2025-08-27 | revision HF: 2.0 `08286fc2…`, 1.1 `049b9ab1…`, 1.0 `f0bb02c0…` |
| ecmwf-opendata | 0.3.34 (PyPI 2026-07-30) | client tải theo tham số/bước |
| earthkit-data | 1.2.3 (PyPI 2026-09-21 — **sau** mốc exclude-newer 2026-09-17 của bảng chung) | nếu dùng thì lấy bản ≤ 2026-09-17 hoặc dời mốc |
| cfgrib 0.9.15.1 / eccodes 2.48.0 (+ eccodeslib 2.49.0.30 có wheel kèm thư viện C) | PyPI | đọc GRIB2 bằng xarray; Phase 31 kiểm wheel macOS/Windows |
| xarray | 2026.7.0 | |
| torch-geometric | 2.8.0.post1 (thuần Python, cài được) | không bắt buộc |
| **torch-geometric-temporal** | 0.56.2 | **KHÔNG cài được với torch 2.14**: bắt buộc `torch-scatter` + `torch-sparse`; index PyG cho torch 2.14 cpu chỉ có `pyg_lib` (0 wheel scatter/sparse; torch 2.10 thì có) → `uv sync` phải build từ nguồn và **hỏng** ("torch-scatter depends on torch but doesn't declare it as a build dependency") — thử thật 2026-09-25 |

## Dữ liệu

| Bộ | Trạng thái | Ghi chú |
|---|---|---|
| `monash-traffic-hourly` (danh mục) | CC BY 4.0, đã chốt | 862 cảm biến; không kèm đồ thị → dựng đồ thị từ tương quan **chỉ trên đoạn train** (dựng trên toàn chuỗi = rò rỉ) |
| METR-LA | ngoài danh mục (không có giấy phép dữ liệu) | giữ làm tuỳ chọn học viên tự tải, như lộ trình |
| `ghcnh-noi-bai-2025` (danh mục) | CC0, đã chốt | kiểm chứng sạch: 2025 nằm sau mọi giai đoạn huấn luyện AIFS |
| GHCNh Nội Bài 2026 | **tệp đổi hằng ngày** | "30 ngày gần nhất" → Phase 31 chụp snapshot + mirror (như EIA), chốt sha256; không dùng tệp sống |
| `ecmwf-aifs-2t-20260101-24h` (danh mục) | CC BY 4.0, đã chốt | 1 bản tin GRIB2 (547 KB, byte-range) để dạy định dạng |
| Open-Meteo AIFS previous-runs Nội Bài 2025-03-01 → 2025-12-31 | **cần thêm vào danh mục** (Phase 31) | CC BY 4.0, cùng dạng `open-meteo-du-bao-luu-*` đã có: 1 lệnh CSV, ~1 MB, K = 1…7 |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **AIFS đã đổi phiên bản 2 lần trong giai đoạn có dữ liệu** (v1.0 → v1.1 ngày 2025-08-27, → v2 ngày 2026-05-12). Bảng sai số trộn hai phiên bản = so sánh
  không trung thực → cắt theo mốc phiên bản hoặc ghi rõ.
- **Mốc huấn luyện**: v1.x dùng dữ liệu tới 2022 (fine-tune đến 01/2023), v2 tới 2024 → **dự báo phát hành từ 2025 trở đi đều sau mốc huấn luyện** của mô hình
  đã phát hành chúng. Chỗ hở cố ý "đánh giá trên năm có trong tập huấn luyện" có ví dụ thật: **WeatherBench 2 chấm trên 2022** — năm nằm trong ERA5 mà AIFS
  (và nhiều mô hình ML) dùng để huấn luyện/fine-tune.
- **Sàn sai số do làm tròn quan trắc**: nhiệt độ METAR của GHCNh Nội Bài là số nguyên → sai số làm tròn đều ±0,5 °C, RMSE ≈ 0,29 °C (= 1/√12) ngay cả khi dự báo hoàn hảo.
- **Chênh độ cao/ô lưới**: ô 0,25° gần nhất (21,25° N 105,75° E, cao 13 m) cách trạm vài km; hiệu chỉnh MOS (hồi quy theo tầm) là trọng tâm như lộ trình.
- Việc ECMWF ngừng GraphCast/Aurora vì "fine-tune quá nhạy với đổi điều kiện đầu" là ví dụ dịch phân phối đầu vào — nối buổi 43.

## Thời gian + RAM trên CPU

- GNN: PyG Temporal không cài được → mô hình đồ thị **tự viết bằng PyTorch thuần** (ma trận kề dày, lớp GCN + GRU kiểu DCRNN/STGCN rút gọn).
  **Đo thật** (2026-09-25, 4 luồng, `monash-traffic-hourly` 862 cảm biến, 10 tuần train / 2 tuần test, `L=168`, `h=24`, đồ thị 8 láng giềng tương quan
  tính trên đoạn train): GNN 2 lớp trộn láng giềng huấn luyện **43 s**, RAM **525 MB**; MAE (z) **GNN 0,335 thua MLP từng cảm biến 0,295**, cả hai
  thắng seasonal naive 168 h (0,375). → Buổi phải nói trung thực: đồ thị không tự động giúp; so GNN với mô hình không đồ thị cùng cỡ là bắt buộc.
- AIFS: không chạy mô hình (checkpoint 994 MB, huấn luyện trên GPU; model card không nêu chạy CPU) → buổi **chỉ dùng dự báo đã phát** (Open Data / Open-Meteo), đúng lộ trình.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| "PyTorch Geometric Temporal / GNN nhỏ" — thư viện không cài được với torch 2.14 CPU | **lớn** (đổi công cụ) | tự viết GNN bằng PyTorch thuần (~40 dòng) trong buổi; không thêm PyG vào bảng chung. Hạ torch cho riêng buổi 33 (torch 2.10 có wheel) bị loại: lệch bảng chung, PyG Temporal cập nhật lần cuối 07/2025 |
| "Bảng sai số theo tầm 1–10 ngày" | **lớn** | nguồn theo điểm (Open-Meteo) chỉ có tầm 1–7 ngày → bảng chính **1–7 ngày** trên 2025-03 → 2025-12 (AIFS v1.x, sau mốc huấn luyện) so GHCNh 2025; tầm 8–10 ngày chỉ qua GRIB (byte-range bước 192–240 h, ~0,55 MB/bước) → "Nâng cao" |
| "Tải AIFS … 30 ngày gần nhất" | nhỏ | "gần nhất" không tái lập → snapshot cố định (ghi ngày) + mirror; tách tại 2026-05-12 nếu cửa sổ chạm mốc v2 |
| Danh sách mô hình thời tiết: "WeatherNext 2", "Aurora" | nhỏ | cập nhật: WeatherNext 3 (08/2026); ECMWF ngừng chạy Aurora/GraphCast/Pangu/FourCastNet (05/2026); AIFS v2 + AIFS ENS v2 |
| Chú thích danh mục `ghcnh-noi-bai-2025` "2025 nằm SAU giai đoạn huấn luyện AIFS (ERA5 1979–2022, fine-tune 2016–2022)" | nhỏ | vẫn đúng cho v1.x; thêm v2 (fine-tune 2018–2024) khi Phase 31 sửa danh mục |
