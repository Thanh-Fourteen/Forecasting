# Nhật ký research — Buổi 29: Nền deep learning cho chuỗi thời gian

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-25
- **Người/phiên:** Phase 28 (RS — research riêng cụm deep learning, chưa soạn). Phase 29 đọc file này, chỉ rà bổ sung.

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Hyndman, Athanasopoulos, Garza, Challu, Mergenthaler, Olivares, *Forecasting: Principles and Practice, the Pythonic Way*, ch. 14 "Neural networks" https://otexts.com/fpppy/14-neural-networks.html | sách | 2026-09-25 | khung buổi: MLP → kiến trúc hiện đại → scaling (identity/standard/robust) → loss → exog (F/H/S) → Auto*. Dùng **neuralforecast**; kết luận: trên AirPassengers mô hình phức tạp "comparable to … the relatively simple MLP"; DL mạnh ở mô hình toàn cục nhiều chuỗi |
| 2 | Kim, T. et al. (2022). Reversible Instance Normalization for Accurate Time-Series Forecasting against Distribution Shift. *ICLR 2022* https://iclr.cc/virtual/2022/poster/6034 ; mã https://github.com/ts-kim/RevIN | bài gốc | 2026-09-25 | RevIN: chuẩn hoá theo từng cửa sổ (trung bình/độ lệch của chính cửa sổ đầu vào), affine học được, đảo ngược ở đầu ra |
| 3 | Berthelier, G. et al. (2026). On the Role of Reversible Instance Normalization. arXiv:2603.11869 | phản biện | 2026-09-25 | ablation: vài thành phần RevIN thừa/có hại (affine học được) → buổi dạy RevIN = "trừ trung bình, chia độ lệch của cửa sổ rồi cộng lại", affine là chi tiết |
| 4 | Bai, S., Kolter, J.Z., Koltun, V. (2018). An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling. arXiv:1803.01271 | bài gốc | 2026-09-25 | TCN: tích chập nhân quả + dilation |
| 5 | neuralforecast 3.2.2 — PyPI (2026-09-08), GitHub releases v3.1.5 → v3.2.2 https://github.com/Nixtla/neuralforecast/releases ; mã nguồn `common/_scalers.py`, `common/_base_model.py` | thư viện | 2026-09-25 | xem "Phiên bản"; `scaler_type` có `identity, standard, robust, minmax, minmax1, invariant, revin` |
| 6 | PyTorch 2.14.0 release notes https://github.com/pytorch/pytorch/releases/tag/v2.14.0 | thư viện | 2026-09-25 | không đổi API cơ bản buổi dùng (`nn.Module`, `DataLoader`, `optim`); thay đổi lớn nằm ở Inductor/CUDA/phân tán |
| 7 | Hewamalage, H., Ackermann, K., Bergmeir, C. (2023). Forecast evaluation for data scientists: common pitfalls and best practices. *DMKD* 37 | tổng quan | không đọc lại — đã xác minh ở `buoi-14`, `buoi-15` | rò rỉ do cửa sổ chồng lấn/chuẩn hoá toàn chuỗi |

## Phiên bản đã xác minh

| Thư viện | Phiên bản | Nguồn xác minh | Ghi chú |
|---|---|---|---|
| torch | 2.14.0 (+cpu, index `download.pytorch.org/whl/cpu`) | PyPI 2026-09-02; `uv sync` thật 2026-09-25 | đã có trong bảng chung |
| neuralforecast | 3.2.2 | PyPI 2026-09-08 | `requires_dist`: `torch>=2.9.1`, **`pytorch-lightning<2.6.0`**, **`ray[train,tune]>=2.2.0` (bắt buộc, không phải extra)**, `optuna`, `coreforecast`, `utilsforecast` |
| pytorch-lightning | 2.5.6 (resolve) | `uv lock` exclude-newer 2026-09-17 | bản 2.6.6 mới nhất bị chặn bởi neuralforecast |
| ray | 2.58.0 (resolve) | như trên | kéo theo nhiều gói → venv buổi ~**1,6 GB** |
| pandas | 2.3.3 | luật `[[rang_buoc]]` Nixtla | statsforecast/mlforecast cho baseline |

`uv lock` + `uv sync` bộ {neuralforecast 3.2.2, torch 2.14.0 cpu, pandas 2.3.3, numpy 2.5.3, statsforecast 2.1.1, utilsforecast 0.2.16,
mlforecast 1.1.0, lightgbm 4.7.0, scoringrules 0.11.0, matplotlib 3.11.2}: **88 gói, resolve 1,3 s, không xung đột** (Linux, 2026-09-25).
Phase 29 phải kiểm lại trên macOS/Windows qua `sinh_nen.py`.

## Dữ liệu

| Bộ | Giấy phép | Ghi chú đã kiểm |
|---|---|---|
| `monash-electricity-hourly` (đã trong danh mục) | CC BY 4.0 | tải mirror HF, sha256 `eff44707…` khớp danh mục. 321 chuỗi × 26.304 giờ (2012-01-01 → 2014-12-31). **Mốc bắt đầu trong tệp .tsf ghi `2012-01-01 00-00-01`** (giây = 1, định dạng `%Y-%m-%d %H-%M-%S`) — đọc sai định dạng cho ra múi giờ `-01:00` giả; phải `floor("h")`. Lộ trình ghi "370 khách hàng" ở Lab 1 — bản Monash là **321** (bản gộp Lai et al. 2017) → sửa chữ khi soạn |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Scaler của neuralforecast mặc định chuẩn hoá theo từng cửa sổ** (`TemporalNorm`, mặc định `robust`) → trong neuralforecast không có rò rỉ "scaler fit toàn bộ";
  rò rỉ đó chỉ xảy ra với **mã tự viết** (đúng chỗ hở cố ý của buổi 29). Riêng `NeuralForecast(local_scaler_type=…)` là scaler theo chuỗi, fit trên `df` truyền vào `fit`.
  → "Lỗi thường gặp": nhầm `scaler_type` (theo cửa sổ) với `local_scaler_type` (theo chuỗi).
- **RevIN ≈ `scaler_type="standard"` + affine học được**; bài phản biện 2026 cho thấy affine thường thừa → dạy phần trừ/chia/cộng lại, không dạy affine.
- **Thời gian import lần đầu ~40 s** (ray + lightning, cache lạnh), các lần sau ~4 s — ghi vào "Lỗi thường gặp" để học viên không tưởng treo máy.
- **Log Lightning rất ồn** (GPU available, model summary, progress bar) → mọi cấu hình trong `code/` truyền `enable_progress_bar=False, enable_model_summary=False, logger=False`
  (3.1.9 đã bỏ bớt "tips"). Công cụ phải im lặng — không giải thích log trong tài liệu.
- FPP-Py ch. 14 xác nhận thông điệp "DL thường không thắng trên ít chuỗi ngắn; mạnh khi mô hình toàn cục" — khớp lộ trình.

## Thời gian + RAM trên CPU (đo thật 2026-09-25)

Máy soạn: 12 luồng, **giới hạn `torch.set_num_threads(4)`** (mô phỏng CPU 4 nhân), mỗi mô hình một tiến trình, trần RAM 6 GB.
Cấu hình: 321 chuỗi, dữ liệu từ 2014-01-01 (8.760 giờ/chuỗi), `h=24`, `input_size=168`, `max_steps=500`, `scaler_type="standard"`,
mặc định còn lại của thư viện (`windows_batch_size=1024`, `batch_size=32`), seed 0. MAE trên **một** ngày cuối (24 giờ × 321 chuỗi) — chỉ để
định cỡ, không phải kết quả so sánh (một mốc cắt). Seasonal naive 24 h cùng ngày: MAE 290,3.

| Mô hình | Huấn luyện (s) | RAM đỉnh (MB) | Tham số | MAE 1 ngày |
|---|---|---|---|---|
| MLP | 113,6 | 1.321 | 1,25 M | 256,9 |
| LSTM | 213,4 | 1.406 | 0,22 M | 286,9 |
| TCN | 174,3 | 1.333 | 0,15 M | 247,3 |

(bảng đủ 16 mô hình: `buoi-30/NGHIEN-CUU.md`.) Kết luận định cỡ: 3 mô hình buổi 29 trên toàn bộ 321 chuỗi ≈ **8,5 phút** chỉ để huấn luyện
một lần → `lab.py check` (< 10 phút) phải dùng **tập con** (ví dụ 50 chuỗi, `max_steps` 200) hoặc mô hình tự viết nhỏ; RAM ~1,4 GB/tiến trình
→ cấu hình 8 GB thoải mái.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| "Tiêu thụ điện 370 khách hàng" (Lab 1) | nhỏ | dữ liệu là 321 chuỗi (Monash) — sửa chữ khi soạn |
| neuralforecast bắt buộc `ray[train,tune]` → venv ~1,6 GB, import lạnh ~40 s | nhỏ | ghi vào MOI-TRUONG + "Lỗi thường gặp"; buổi 29 phần tự viết chỉ cần `torch` (không cần neuralforecast) → cân nhắc Phase 29: tự viết bằng torch, neuralforecast chỉ ở bước so sánh |
| RevIN: affine thừa (phản biện 2026) | nhỏ | dạy bản không affine; nhắc `scaler_type="revin"` có sẵn |
| Thời gian CPU: 3 mô hình × 321 chuỗi ≈ 8,5 phút | nhỏ | `check` chạy tập con; con số đầy đủ ghi trong tài liệu từ lần chạy thật |

## Rà bổ sung Phase 29 (2026-09-25)

Research Phase 28 còn mới (cùng ngày) → không rà lại phiên bản. Bổ sung khi soạn:

- `sinh_nen.py 29` resolve {torch 2.14.0+cpu, statsforecast 2.1.1, mlforecast 1.1.0, lightgbm 4.7.0, pandas 2.3.3} không xung đột; buổi 29
  **không dùng neuralforecast** (tự viết bằng torch) → không kéo ray/lightning, venv nhẹ hơn buổi 30.
- `tv.du_lieu.doc_du_lieu` đọc .tsf Monash giữ nguyên mốc `00-00-01` → mọi `ds` lệch 1 giây; `doc_dien` làm `floor("h")`.
- Khách **T183** ngừng dùng điện từ 2012-09-23 (toàn số 0 về sau; trung bình test = 0 → tỷ lệ đổi mức vô hạn). Quy tắc chỉ nhìn train: bỏ khách có
  tổng 0 trong 4 tuần cuối trước `MOC_VAL`. Còn 13 khách đổi mức (|log(tb test / tb trước)| > log 1,3).
- pandas 2.3.3 + numpy 2.5.3 in `DeprecationWarning` "generic unit for NumPy timedelta" ở mọi `pd.Timedelta(...)` — chung mọi buổi dùng
  pandas 2.3.3, không do buổi này; để nguyên.

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0, `torch.set_num_threads(4)`, ~14,5 phút; thời gian dao động ±5% giữa các lần chạy)

Cấu hình: 50 khách (13 đổi mức + 37 ngẫu nhiên), $L$ = 168, $H$ = 24; train: mục tiêu < 2014-05-01 (stride 2 → 505.850 mẫu); val: 2014-05-01 →
2014-06-30 (72.050 mẫu); test: 26 mốc thứ Hai 00:00, 2014-07-07 → 2014-12-29 (1.300 mẫu). Adam lr 0,001, MAE, 30 epoch × 100 lô × 256, kiên
nhẫn 5. MLP 168→256→256→24 (115.224 tham số), LSTM 32 nút (5.272), TCN 16 kênh, k = 3, dilation 1…64 (5.928).

| Mô hình | MASE 50 khách | đổi mức | còn lại | giây |
|---|---|---|---|---|
| SeasonalNaive (168 h) | 1,124 | 1,222 | 1,089 | 0 |
| MSTL [24, 168], 8 tuần, học lại mỗi mốc | 0,883 | 0,967 | 0,854 | 108 |
| LightGBM, lag 24…168 + giờ, thứ, học một lần | 0,896 | 1,060 | 0,838 | 8 |
| MLP | 0,960 | 1,226 | 0,866 | 4,6 |
| MLP + RevIN | 0,957 | 1,110 | 0,903 | 5,9 |
| LSTM | 1,578 | 1,870 | 1,475 | 86,4 |
| LSTM + RevIN | 1,202 | 1,250 | 1,185 | 87,6 |
| TCN | 1,245 | 1,444 | 1,175 | 239,8 |
| TCN + RevIN | 1,163 | 1,322 | 1,108 | 239,8 |

Không mạng nào kích hoạt dừng sớm trong 30 epoch (epoch val tốt nhất 27–29).

**Rò rỉ chồng lấn — phát hiện quan trọng.** Lộ trình giả định cắt-rồi-chia luôn cho "khoảng lạc quan" lớn. Đo thật (MASE trên thang gốc):

| Dữ liệu | Mạng | Chia | MASE val | MASE test |
|---|---|---|---|---|
| 5 khách đầu (T1, T3, …) từ 2013-11-01 | MLP 1.024 + RevIN, ≤ 200 epoch × 50 lô, kiên nhẫn 15, **1 luồng** | theo thời gian | 1,486 | 1,418 |
| như trên | như trên | cắt rồi rút ngẫu nhiên 20% | 0,981 | 1,412 |
| 50 khách từ 2012 | MLP 256 + RevIN, 30 epoch | theo thời gian | 0,763 | 0,957 |
| như trên | như trên | cắt rồi rút ngẫu nhiên | 0,740 | 0,924 |

Trên dữ liệu lớn (505 nghìn mẫu) mạng không học thuộc nổi → khoảng val → test như nhau (0,194 vs 0,184); thử cả MLP 1.024 nút × 150 epoch
(scratch, không đưa vào bài): 0,158 vs 0,167. Chỉ khi ít dữ liệu + mạng lớn thì val nói dối rõ (0,98 → thật 1,41). Bài dạy đúng như vậy: rò rỉ
chồng lấn nguy hiểm theo mức mạng học thuộc được, nên phải chặn bằng cách chia (và test tự động), không chờ thấy số lạ. Chia ngẫu nhiên còn cho
mạng học dữ liệu gần mốc test hơn (tháng 5–6) nên test của nó còn tốt hơn chút — một biến nhiễu khi so hai cách chia.

**Rò rỉ scaler** (học cả val, test): MASE test MLP + RevIN 0,957 → 0,930 (đẹp giả 2,8%).

**Tính tái lập trên CPU (phát hiện 2026-09-25).** `dat_seed(0)` + `torch.use_deterministic_algorithms(True)` + 4 luồng: MLP 1.024 nút
trên tập nhỏ cho MAE val lệch ngay từ epoch 1 (tới 0,002) giữa hai lần huấn luyện; giữa các tiến trình ra vài kết quả rời rạc khác nhau (3 lần
chạy → 3 hash). Hai lần `ve_hinh.py` + một lần notebook cho tập nhỏ "chia đúng" MASE test 1,438 / 1,415 / 1,405. Đã thử:
`MKL_CBWR=AUTO,STRICT` → trùng TRONG một tiến trình nhưng vẫn lệch giữa tiến trình; tắt oneDNN (`torch.backends.mkldnn.enabled = False`) → vẫn
lệch; **1 luồng** (`torch.set_num_threads(1)`) → 3 tiến trình trùng tuyệt đối, tập nhỏ chỉ ~21 s. Nguyên nhân: cộng song song giữa các luồng
theo thứ tự không cố định. Quyết định: thí nghiệm tập nhỏ chạy trong `with hs.so_luong(1):`; bảng chính giữ 4 luồng (LSTM/TCN 1 luồng quá chậm) —
MLP 256 nút ở bảng chính trùng tới 3 chữ số giữa mọi lần chạy (lệch nhỏ hơn làm tròn). Bỏ `MKL_CBWR` khỏi module (không giúp giữa các lần chạy; và 1 luồng có/không `MKL_CBWR` là hai đường tính khác nhau, ra hai kết quả
khác nhau nhưng mỗi đường đều tất định). Kiểm cuối: `ve_hinh.py` và notebook (hai tiến trình) cùng cho 1,486 / 1,418.

## Đọc thử (2026-09-25, Phase 29, tự đọc — không subagent)

**Vòng 1** (đọc toàn bộ `tai-lieu.md` vai học viên mới; mọi số đã tính lại bằng Python/torch và output `ve_hinh.py` lần cuối):

| # | Mục | Chỗ vướng | Mức | Sửa |
|---|---|---|---|---|
| 1 | 4.4 | "tín hiệu … đi ngược qua các phép nhân 0,5" — lan truyền ngược chưa dạy | khó | viết lại bằng đạo hàm (mục 4.3): đạo hàm trạng thái cuối theo giờ đầu = $0{,}5^{167}$ |
| 2 | 4.6, quiz 8 | "kiên nhẫn" dùng mà chưa định nghĩa | khó | thêm "số epoch chờ đó gọi là kiên nhẫn (patience)" |
| 3 | 6 | `kiem_chong_lan` xuất hiện lần đầu ở Lỗi thường gặp | khó | giới thiệu ở mục 4.1 phần Code |
| 4 | 4.6 | "chế độ tất định" chưa định nghĩa | khó | thêm định nghĩa một mệnh đề |
| 5 | 4.6 | "kiến trúc buổi 30 làm tốt hơn" — khẳng định chưa đo | khó (sai sự thật tiềm năng) | đổi thành "buổi 30 thử … trên cùng cách chấm"; bỏ "hàng nghìn" |
| 6 | 4.1 | `hs` trong đoạn code không nói là gì | nhỏ | "(`hs` là module `hoc_sau`)" |
| 7 | 4.3 | dòng 4 bảng hạ gradient đổi dấu đạo hàm không giải thích | nhỏ | "và đạo hàm đổi dấu" trong Đọc bảng |
| 8 | 4.1 | "Chia đúng cho 505.850 mẫu" — không nói 50 khách | nhỏ | giữ (mục 3 đã nêu 50 khách; thêm số làm vượt ngưỡng D7) |

Kết quả: **0 chặn, 5 khó (đã sửa), 3 nhỏ**. Mục B (giải thích lại bằng ví dụ mới): cửa sổ ($T$ = 12, $L$ = 4, $H$ = 2, $s$ = 3 → 3 mẫu),
RevIN (10, 20, 30 → −1, 0, 1), hạ gradient ($\hat y = wx$, $x$ = 1, $y$ = 3, $w$ = 0, học suất 1 → $w$ = 1), LSTM (cổng quên 1), TCN ($d$ = 4),
dừng sớm — đều giải thích được. Quiz làm mù 10/10, mỗi câu có căn cứ: 1→4.1, 2→4.2, 3→4.4, 4→4.5, 5→4.1 công thức, 6→4.3, 7→4.5 công thức,
8→4.6 (sau khi thêm "kiên nhẫn"), 9→4.1 + 4.6, 10→4.2 hình. Đáp án quiz tính lại bằng Python (Q2, Q5–Q8).

**Rà gọn** (vai biên tập viên, sau vòng 1): 2 chỗ lặp nhẹ — "Tóm lại" 4.1 nhắc "càng ít dữ liệu val càng nói dối" của "Đọc bảng"; "Tóm lại" 4.4
nhắc "LSTM chậm" của "Dữ liệu thật". Cả hai là tóm tắt hợp lệ, giữ. ≤ 3 → đạt. `kiem_de_hieu.py 29`: 0 vi phạm. Khoảng 4.980 chữ ngoài bảng/code
(trần 3.500–6.500); PDF 14 trang.

**Vòng 2** (đọc lại toàn bộ sau khi sửa): 5 chỗ khó đã hết; không phát sinh chỗ vướng mới. 0 chặn, 0 khó, 3 nhỏ.
