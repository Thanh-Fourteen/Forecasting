# Nhật ký research — Buổi 13: Feature engineering và chống rò rỉ

<!-- BƯỚC 0 của giao thức research (todos.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-18
- **Người/phiên:** Claude Opus 5, phiên xây Phase 4

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Kaufman, S. et al. (2012), "Leakage in Data Mining: Formulation, Detection, and Avoidance", *TKDD* 6(4) | bài gốc | 2026-09-18 | 4.5 định nghĩa rò rỉ |
| 2 | Kapoor, S. & Narayanan, A. (2023), "Leakage and the reproducibility crisis in machine-learning-based science", *Patterns* 4(9) | tổng quan mới | 2026-09-18 | 4.5 phân loại L1–L3 |
| 3 | Hồ Ngọc Đức — Âm lịch Việt Nam, http://www.informatik.uni-leipzig.de/~duc/amlich | tài liệu gốc | 2026-09-18 | 4.2 thuật toán âm lịch |
| 4 | Meeus, J. (1998). *Astronomical Algorithms*, 2nd ed., ch. 47 (Moon), ch. 49 (Phases of the Moon), ch. 25 (Solar coordinates) | sách chuẩn | 2026-09-18 | 4.2 công thức sóc và kinh độ mặt trời |
| 5 | `holidays` (PyPI) — https://github.com/vacanza/holidays | thư viện | 2026-09-18 | nguồn đối chiếu ngày Tết |
| 6 | Open-Meteo **Previous Runs API** — https://open-meteo.com/en/docs/previous-runs-api | tài liệu chính thức | 2026-09-17 | 4.6 dự báo đã lưu |
| 7 | EIA-930 Hourly Electric Grid Monitor — https://www.eia.gov/electricity/gridmonitor/ | dữ liệu | 2026-09-17 | 4.6 phụ tải + dự báo của nhà vận hành |
| 8 | FPP3 ch. 7.4 (Fourier terms), ch. 10 — https://otexts.com/fpp3/useful-predictors.html | sách chuẩn | 2026-09-18 | 4.3 Fourier, biến giả |
| 9 | `pandas` rolling/shift — https://pandas.pydata.org/docs/user_guide/window.html | tài liệu chính thức | 2026-09-18 | 4.4 rolling đúng cách |

## Phiên bản đã xác minh

| Thư viện / dataset | Phiên bản / sha256 | Nguồn xác minh |
|---|---|---|
| Python | 3.12.14 | nền buổi 13 |
| numpy / pandas / scipy / scikit-learn | 2.5.3 / 3.0.5 / 1.18.1 / 1.9.1 | import trong nền |
| **holidays** | **0.104** (PyPI, phát hành 2026-09-07) | PyPI JSON API 2026-09-18 |
| `vncalendar` | **1.3.1 — HỎNG**, `from main import ...` (absolute import) → `ModuleNotFoundError: No module named 'main'` | cài thử 2026-09-18 |
| `lunardate` | 0.3.0, GPL-3, lịch **Trung Quốc** (UTC+8) — sai cho VN ở 2007, 2030 | PyPI 2026-09-18 |
| uci-online-retail-ii | `572e36277c23…`, 739 ngày doanh thu sau khi gộp | `lay_du_lieu.py buoi-13` |
| eia930-balance-2024-h1/h2 | public domain; ERCO có 8.735 giờ năm 2024 | như trên |
| open-meteo-dallas-du-bao-luu-2024 | `5c7b56f9f713…`, 8.784 giờ, có `temperature_2m`, `_previous_day1`, `_previous_day3` | như trên |

## Dữ liệu

| Bộ | Giấy phép | Vai trò trong buổi |
|---|---|---|
| UCI Online Retail II | CC BY 4.0 | chuỗi doanh thu ngày để xây 41 feature |
| Wikimedia Pageviews (vi) | CC0 1.0 | đo giá trị của feature Tết âm lịch |
| EIA-930 | Public domain (U.S. government) | phụ tải ERCOT **và dự báo của chính nhà vận hành** |
| Open-Meteo Previous Runs | CC BY 4.0 | nhiệt độ thật (ERA5) và **bản dự báo đã lưu** trước 1 / 3 ngày |

Bộ Open-Meteo Previous Runs là mấu chốt của buổi: nó cho **cả hai** trong một tệp — sự thật và thứ
ta thực sự có trong tay lúc ra dự báo. Không có nó thì "cái giá của rò rỉ" chỉ là lý thuyết.

## Âm lịch: quyết định và kiểm chứng

**Quyết định: tự viết, không dùng thư viện.** Lý do:
1. `vncalendar` 1.3.1 (MIT, bản mới nhất 2026-05-21) **không import được** — lỗi `from main import Date, …`.
2. `lunardate` 0.3.0 là lịch **Trung Quốc** (kinh tuyến 120°Đ): sai ngày Tết Việt Nam ở 2007 và 2030.
3. Thuật toán chỉ ~120 dòng (Meeus ch. 49 + ch. 25 + quy tắc tháng 11 chứa đông chí), chạy bằng
   thư viện chuẩn, và **múi giờ là tham số** — chính chỗ để dạy vì sao Tết hai nước lệch nhau.

**Kiểm chứng: 2000–2035 khớp 100% với `holidays` 0.104** (một cài đặt hoàn toàn độc lập).
Lệch VN (UTC+7) so với TQ (UTC+8) đúng ở **2007** (17/02 so với 18/02) và **2030** (02/02 so với 03/02)
— hai năm được ghi nhận rộng rãi. Giỗ Tổ 2024 (10/3 âm lịch) ra **18/04/2024**, khớp lịch chính thức.

Ngày Tết 2016–2025 tính được: 08/02, 28/01, 16/02, 05/02, 25/01, 12/02, 01/02, 22/01, 10/02, 29/01 —
rơi vào ngày thứ **22–47** của năm dương lịch.

## Con số đo được (`dap-an/feature.py`, `dap-an/ve_hinh.py`)

**Bộ feature:** 41 cột — 23 cột "biết trước vô hạn" (lịch, Fourier, Tết), 18 cột "chỉ dùng y tới t−h"
(lag, rolling đã shift). Bài kiểm cắt-tương-lai và bài kiểm nhiễu-mục-tiêu đều **sạch**.

**Minh hoạ rò rỉ** (cùng cửa sổ 7 ngày trên doanh thu bán lẻ, cắt tại dòng 90/120):
`shift(1).rolling(7)` lệch **0,0**; `rolling(7, center=True, min_periods=1)` lệch tới **5.113** đơn vị
ngay trước mốc cắt.

**Cái giá của rò rỉ** (phụ tải ERCOT, dự báo **24 giờ** tới, hồi quy tuyến tính, học 70%):

| Bộ feature | MAE (MW) | So với baseline | Dùng tương lai? |
|---|---|---|---|
| chỉ lag + giờ | 1.909,68 | 0,00% | không |
| + **nhiệt độ THẬT** của giờ cần dự báo | 1.836,16 | **−3,85%** | **có** |
| + dự báo nhiệt độ trước 1 ngày | 1.834,29 | −3,95% | không |
| + dự báo nhiệt độ trước 3 ngày | 1.965,47 | +2,92% | không |
| + nhiệt độ hiện tại (nhân quả) | 1.865,56 | −2,31% | không |
| huấn luyện bằng nhiệt độ thật, **CHẠY** bằng dự báo 1 ngày | 1.850,50 | −3,10% | có |
| huấn luyện bằng nhiệt độ thật, **CHẠY** bằng dự báo 3 ngày | 1.951,70 | **+2,20%** | có |

Sai số của chính bản dự báo thời tiết: MAE **1,325 °C** (trước 1 ngày) và **2,069 °C** (trước 3 ngày)
trên 8.292 giờ.

**Giá trị của feature Tết** (lượt xem vi.wikipedia, dự báo 1 ngày):

| Bộ feature | MAE cả năm | MAE quanh Tết (±10 ngày) | Số feature |
|---|---|---|---|
| chỉ lag + lịch dương | 132.137 | 167.769 | 36 |
| + feature Tết âm lịch | 129.680 | **139.478** | 41 |

→ cải thiện **−16,9%** ở vùng quanh Tết (chỉ −1,9% nếu tính trung bình cả năm — đúng như kỳ vọng, vì
Tết chỉ chiếm ~6% số ngày). Hiệu ứng Tết đo được: lượt xem ngày mùng 1 chỉ bằng **0,62×** mức trung bình.

**Ở tầm 1 giờ thì rò rỉ không có tác dụng gì**: MAE 846,18 (chỉ lag) so với 847,67 (thêm nhiệt độ thật).
Vì vậy thí nghiệm phải làm ở tầm 24 giờ — ghi lại để không ai đo lại rồi tưởng mình sai.

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Cái giá của rò rỉ KHÔNG phải lúc nào cũng lớn.** Ở đây backtest rò rỉ hứa −3,85%, chạy thật bằng
  dự báo D+1 vẫn được −3,10%: dự báo thời tiết 1 ngày quá tốt (MAE 1,3 °C). Nhưng với dự báo D+3 thì
  từ "−3,85%" thành **+2,20%** — tệ hơn cả không dùng. **Cái giá của rò rỉ = khoảng cách chất lượng
  giữa sự thật và thứ bạn thật sự có.** Phải đo, đừng đoán theo cả hai chiều.
- **`interpolate(limit_direction="both")` chỉ lộ rò rỉ ở MÉP lỗ hổng.** Nếu mốc cắt không rơi vào một
  lỗ thì bài kiểm im lặng. Bộ chấm vì thế truyền `cac_moc` tường minh rơi đúng vào ngày bị khoét.
  Đây là điểm tinh tế nhất của buổi và là lý do bài kiểm phải chọn mốc cắt **có chủ đích**.
- **`rolling(center=True)` không có `min_periods` thì trả NaN ở mép**, nên phép so "giá trị vs giá trị"
  ra 0 và tưởng là sạch. Bài kiểm phải coi **NaN vs số là khác nhau** (`equal_nan=True` trong
  `np.allclose` chỉ coi NaN vs NaN là giống).
- **`holidays` gọi ngày mùng 1 Tết là `"Lunar New Year"`**, còn 29 Tết là `"29 of Lunar New Year"` —
  lọc theo `in` chuỗi sẽ dính cả cụm 6 ngày nghỉ. Phải so khớp chính xác.
- **EIA-930 có sẵn `Demand Forecast (MW)`** — dự báo của chính nhà vận hành, một baseline thật và là
  ví dụ hoàn hảo cho "biến ngoại sinh biết trước".
- **Mã hoá tuần hoàn sin/cos** cần **cặp** sin và cos; chỉ một trong hai thì hai thời điểm khác nhau
  có cùng giá trị.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lab 4 phải làm ở tầm **24 giờ**, không phải 1 giờ (ở tầm 1 giờ lag_1 át hết, rò rỉ không cho lợi ích nào) | nhỏ | Đã đưa vào; ghi rõ cả hai con số trong tài liệu |
| Thêm kịch bản "huấn luyện bằng thật, chạy bằng dự báo" (lộ trình chỉ nêu so hai bộ feature) | nhỏ | Đây mới là cái giá thật của rò rỉ; đã thêm 2 dòng vào bảng |
| Không dùng thư viện âm lịch nào (`vncalendar` hỏng, `lunardate` là lịch TQ) | nhỏ | Tự viết ~120 dòng, kiểm 2000–2035 bằng `holidays` |
| Lộ trình ghi "40 feature, 4 feature rò rỉ" | nhỏ | Đáp án có **41** feature sạch; `code/` có **4 cột rò rỉ** + 1 lỗi Tết hardcode 2011 |
| `khung_bo = ["ro_ri"]` — học viên tự viết `kiem_ro_ri` | nhỏ | Bộ chấm chấm **cả** bài kiểm của học viên (bằng 4 hàm rò rỉ đã biết) lẫn bộ feature (bằng bài kiểm độc lập của bộ chấm) |
