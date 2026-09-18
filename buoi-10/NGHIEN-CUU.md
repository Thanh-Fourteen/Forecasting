# Nhật ký research — Buổi 10: Làm sạch và dữ liệu thiếu

<!-- BƯỚC 0 của giao thức research (todos.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-18
- **Người/phiên:** Claude Opus 5, phiên xây Phase 4

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | GHCNh documentation (PDF 18 trang) — https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/doc/ghcnh_DOCUMENTATION.pdf | tài liệu chính thức | 2026-09-18 | 4.3 cờ chất lượng, đơn vị |
| 2 | NCEI — GHCNh product page — https://www.ncei.noaa.gov/products/global-historical-climatology-network-hourly | tài liệu chính thức | 2026-09-18 | nguồn, giấy phép |
| 3 | ICAO/METAR: visibility 9999 = "10 km or more" (SKYbrary, BoM METAR/SPECI guide) — https://skybrary.aero/articles/meteorological-aerodrome-report-metar | tài liệu chính thức | 2026-09-18 | 4.3 giá trị trá hình |
| 4 | Rubin, D.B. (1976). Inference and missing data. *Biometrika* 63(3), 581–592 | bài gốc | 2026-09-18 | 4.2 MCAR/MAR/MNAR |
| 5 | van Buuren, S. *Flexible Imputation of Missing Data* (2e) — https://stefvanbuuren.name/fimd/ | sách chuẩn | 2026-09-18 | 4.2, 4.5 |
| 6 | TSI-Bench / PyPOTS — https://github.com/WenjieDu/PyPOTS, arXiv:2406.12747 | benchmark | 2026-09-18 | 4.6 khi nào cần deep learning |
| 7 | statsmodels `UnobservedComponents` / `smoother_results` — https://www.statsmodels.org/stable/statespace.html | tài liệu chính thức | 2026-09-18 | 4.5 Kalman smoother |
| 8 | pandas `Series.interpolate` — https://pandas.pydata.org/docs/reference/api/pandas.Series.interpolate.html | tài liệu chính thức | 2026-09-18 | 4.5 các phương pháp nội suy |
| 9 | OpenAQ API v3 — https://docs.openaq.org/ | tài liệu chính thức | 2026-09-18 | quyết định BỎ OpenAQ |
| 10 | UCI Beijing Multi-Site Air-Quality — https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data | dữ liệu | 2026-09-17 | lab 1 |
| 11 | Open-Meteo Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api | dữ liệu | 2026-09-17 | trạm hàng xóm |

## Phiên bản đã xác minh

| Thư viện / dataset | Phiên bản / sha256 | Nguồn xác minh |
|---|---|---|
| Python | 3.12.14 | `uv run python -V` trong `lab/00-nen` |
| pandas / numpy / scipy / statsmodels | 3.0.5 / 2.5.3 / 1.18.1 / 0.15.0 | import trong nền buổi 10 |
| pyarrow | theo `tools/nen/phien-ban.toml` | cần để đọc parquet GHCNh |
| GHCNh Nội Bài 2024 | `GHCNh_VMI0000VVNB_2024.parquet`, sha256 `1c67048928d4…`, 783,5 KB, 17.319 dòng | `tools/lay_du_lieu.py buoi-10` |
| UCI Beijing Air | 12 tệp CSV, mỗi tệp 35.064 dòng | như trên |
| Open-Meteo Hà Nội 2023–2024 | 17.547 dòng, CC BY 4.0 | như trên |
| PyPOTS | **không đưa vào nền** | kéo theo torch + transformers, quá nặng cho lab 3 giờ trên CPU |

## Dữ liệu

| Bộ | Giấy phép (trích nguyên văn) | Ghi chú |
|---|---|---|
| GHCNh trạm Nội Bài (VMI0000VVNB) | metadata NOAA ghi **CC0-1.0**; tài liệu GHCNh **không** có điều khoản hạn chế kiểu WMO Res 40 như ISD | Đã bật `mirror = true` trong danh mục; đây là dữ liệu **trạm Việt Nam thật** |
| UCI Beijing Multi-Site Air-Quality | CC BY 4.0 | 12 trạm × 35.064 giờ |
| Open-Meteo Hà Nội | CC BY 4.0 | dùng làm "trạm hàng xóm" |

**OpenAQ (đã loại).** Rà 2026-09-18: **v3 bắt buộc API key cho MỌI endpoint** (kể cả `/v3/licenses`
— thử trả 401), v2 đã ngừng (HTTP 410). Không kiểm được giấy phép từng trạm Việt Nam nếu không có key
→ **bỏ khỏi buổi 10 và khỏi dự án giữa chặng 1**, giữ làm tuỳ chọn cho lớp có key. Đã cập nhật
`lo-trinh` và `todos.md`.

## Trích nguyên văn (dùng trong tài liệu)

**Mã chất lượng GHCNh** (Table 3, sources 313, 314, 315, 322, 335, 343, 344, 346): "0 = Passed gross
limits check / 1 = Passed all quality control checks / 2 = Suspect / 3 = Erroneous / 4 = Passed gross
limits check, data originate from an NCEI data source / 5 = Passed all quality control checks, data
originate from an NCEI data source / 6 = Suspect, data originate from an NCEI data source / 7 =
Erroneous, data originate from an NCEI data source / 9 = Passed gross limits check if element is
present."

Với độ ẩm và nhiệt độ bầu ướt **suy ra** từ biến khác: "o - Out of range (relative humidity only -
with values < 1 or > 100)" và "f - Suspect or Error flags for 1 or more of the input measurements".

→ **Điểm dễ hiểu sai:** mã **4** KHÔNG phải "erroneous"; nó chỉ nghĩa là dữ liệu mới qua kiểm tra
giới hạn thô. Mã đáng ngờ là 2/3/6/7 và các cờ chữ o/f.

**Đơn vị** (Table 1): "visibility = horizontal distance at which an object can be seen and identified
(**kilometers**)"; "relative_humidity = … (whole percent)".

**METAR/ICAO:** "When visibility is 10 km and above and the conditions for the use of CAVOK do not
apply, visibility shall be indicated as 9999" → trong GHCNh (đơn vị km) giá trị đó thành **9.999**.
Đây là **mã**, không phải số đo: coi nó là số đo sẽ tạo ra một đỉnh giả ở 35% số dòng.

## Con số đo được (`dap-an/lam_sach.py`, `dap-an/ve_hinh.py`)

**Trạm Nội Bài 2024 (GHCNh):**
- 17.319 dòng trên lưới 30 phút; kỳ vọng **17.568** mốc → **249 mốc không có dòng**, **0 mốc trùng**,
  và chỉ **2 ô rỗng**. Tức gần như toàn bộ phần thiếu là **thiếu mốc**, `isna()` không thấy.
- 134 lỗ hổng sau khi đưa về lưới; **67,2%** số lỗ chỉ dài 1 bước; lỗ dài nhất 16 bước (8 giờ).
- **30/64** cột đo rỗng 100% (precipitation, station_level_pressure, sea_level_pressure…).
- `relative_humidity` và `visibility` lưu dạng **chuỗi** trong parquet → `min()`/`max()` so sánh theo
  thứ tự chữ cái, cho `min=100, max=94` cho độ ẩm.
- **visibility = 9.999 km**: 6.061 dòng (**35,0%**). **RH = 100%**: 984 dòng (**5,68%**).
- Nhiệt độ: **33 giá trị khác nhau**, bước nhỏ nhất **1,0 °C**, 100% là số nguyên → độ phân giải 1 °C.
- Đoạn "đứng yên" dài nhất: **67 bước = 33,5 giờ** ở đúng 26,0 °C, bắt đầu 2024-06-08 16:30. Nhưng
  với ngưỡng 24 bước (12 h) thì có tới 24 đoạn / 719 điểm (4,15%) — phần lớn là **hệ quả của độ phân
  giải 1 °C**, không phải cảm biến chết. Ngưỡng dùng trong bài: **36 bước (18 giờ)** → còn 2 đoạn/123 điểm.
- Cờ chất lượng: nhiệt độ có **7** dòng mã `2` (Suspect) và 9 dòng mã `4`; độ ẩm có 7 dòng cờ `f`.
- Tương quan giờ với Open-Meteo Hà Nội: **r = 0,976** (n = 8.716), độ lệch trung bình −0,08 °C.
- Sau `lam_sach` (giới hạn điền 6 bước = 3 giờ): 17.568 mốc, **đã điền 198**, **loại vì nghi ngờ 130**,
  **còn thiếu 181** (đều nằm trong lỗ dài, để trống có chủ ý).

**So sánh 7 cách điền (MAE °C trên các ô bị che, seed 0):**

| Cách điền | Che điểm 10% | Che khối 48 giờ | Nhân quả? |
|---|---|---|---|
| tuyến tính | **0,291** (1/7) | 2,171 (5/7) | Không |
| Kalman smoother | 0,308 | 1,256 | Không |
| ffill | 0,378 | 2,052 | Có |
| spline | 0,857 | 3,636 | Không |
| hàng xóm (Open-Meteo) | 0,922 (5/7) | **1,006** (1/7) | Có (nếu hàng xóm có sẵn) |
| mùa vụ (ngày trước) | 1,845 | 1,965 | Có |
| trung bình theo giờ | 4,350 | 2,839 | Không (dùng cả chuỗi) |

→ **Kết luận trung tâm của buổi:** phương pháp tốt nhất **đổi** theo độ dài lỗ. Đánh giá chỉ bằng một
kiểu che sẽ chọn sai.

**Bắc Kinh (12 trạm × 35.064 giờ):** thiếu trung bình **2,08%**; ô (trạm × tháng) tệ nhất **48,0%**;
**13** ô có tỷ lệ thiếu > 10%. Thiếu đi thành **mảng**, không rải đều.

**Kiểm MNAR:**
- Dữ liệu thật (Dongsi): PM2.5 trung bình của các trạm còn lại khi Dongsi thiếu là **76,8** so với
  **79,2** khi có (**−3,0%**) → **không có bằng chứng MNAR** ở bộ này. Báo cáo đúng như đo được.
- Mô phỏng (cảm biến tắt khi giá trị > 1, thiếu 16,2%): trung bình thật **−0,005**; sau khi điền,
  thiếu MCAR **−0,006**; thiếu MNAR **−0,298**. Độ lệch gấp ~50 lần.

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Bẫy kiểu dữ liệu**: parquet "có kiểu sẵn" nên nhiều người bỏ qua bước ép kiểu. Ở đây hai cột số
  là chuỗi, và mọi thống kê đều sai **âm thầm** (không có exception nào). Đưa vào "Lỗi thường gặp".
- **"Đứng yên nghĩa là cảm biến chết"** — sai khi độ phân giải thô. Phải đo `do_phan_giai` trước,
  rồi đặt ngưỡng theo đó. Đây là phát hiện mới so với lộ trình (lộ trình chỉ ghi "cảm biến đứng yên
  33,5 giờ"), đã bổ sung hàm `do_phan_giai` và một test riêng.
- **Mã 4 của GHCNh không phải "erroneous"** — hiểu nhầm phổ biến; xem trích nguyên văn ở trên.
- **Che ngẫu nhiên từng điểm là cách đánh giá dễ dãi nhất**: với lỗ 1 bước thì nội suy tuyến tính gần
  như luôn thắng, và kết luận đó **không** chuyển sang lỗ dài được.
- **`interpolate(limit_direction="both")` dùng tương lai** và còn lấp cả lỗ 48 giờ — bài kiểm cắt
  tương lai (`tv.ro_ri.kiem_ro_ri`) bắt được khi cắt dữ liệu **ngay trong lỗ**.
- **Deep learning (SAITS/BRITS)**: TSI-Bench cho thấy lợi thế xuất hiện khi có **nhiều chuỗi tương
  quan** và tỷ lệ thiếu cao; với một trạm và 2% thiếu thì hồi quy theo trạm hàng xóm đã đạt 1,006 °C.
  Dạy lý thuyết, không cài.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Bỏ OpenAQ (v3 cần key cho mọi endpoint, v2 HTTP 410) | **lớn** | Thay bằng GHCNh Nội Bài + Open-Meteo; **đã cập nhật `lo-trinh` + `todos.md`**, cần báo người dùng |
| PyPOTS/SAITS chỉ dạy lý thuyết | nhỏ | Đã ghi trong lộ trình |
| Thêm `do_phan_giai` + bài học độ phân giải 1 °C | nhỏ | Đã đưa vào buổi (mục 4.3 + test) |
| Bằng chứng MNAR ở Bắc Kinh là **âm** (−3,0%) | nhỏ | Báo trung thực + thêm `mo_phong_mnar` để dạy cơ chế |
| Lộ trình ghi "cảm biến đứng yên 33,5 giờ" như lỗi rõ ràng | nhỏ | Giữ ví dụ nhưng dạy kèm ngưỡng theo độ phân giải |
