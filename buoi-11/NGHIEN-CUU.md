# Nhật ký research — Buổi 11: Ngoại lai và điểm gãy

<!-- BƯỚC 0 của giao thức research (todos.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-18
- **Người/phiên:** Claude Opus 5, phiên xây Phase 4

## Nguồn đã đọc

| # | Nguồn (URL) | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | `ruptures` — PELT user guide, https://centre-borelli.github.io/ruptures-docs/user-guide/detection/pelt/ | tài liệu chính thức | 2026-09-18 | 4.4 PELT |
| 2 | Killick, Fearnhead & Eckley (2012), "Optimal detection of changepoints with a linear computational cost", *JASA* 107(500) | bài gốc | 2026-09-18 | 4.4 PELT |
| 3 | Truong, Oudre & Vayatis (2020), "Selective review of offline change point detection methods", *Signal Processing* 167 | tổng quan | 2026-09-18 | 4.4 hàm chi phí, penalty |
| 4 | Haynes, Eckley & Fearnhead (2017), CROPS — "Computationally efficient changepoint detection for a range of penalties", *JCGS* 26(1) | bài gốc | 2026-09-18 | 4.4 quét penalty |
| 5 | **Hyndman & Rostami-Tabar (2024), "Forecasting interrupted time series", *JORS*** — https://robjhyndman.com/papers/fits.pdf | bài mới nhất | 2026-09-18 | 4.6 xử lý COVID |
| 6 | Chen & Liu (1993), "Joint estimation of model parameters and outlier effects in time series", *JASA* 88(421) | bài gốc | 2026-09-18 | 4.2 phân loại AO/LS/TC |
| 7 | Hampel (1974), "The influence curve and its role in robust estimation", *JASA* 69(346) | bài gốc | 2026-09-18 | 4.3 MAD, Hampel |
| 8 | Wikimedia Pageviews API — https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/ | tài liệu chính thức | 2026-09-17 | lab 1, 3 |
| 9 | Eurostat `avia_paoc` (SDMX 3.0) — https://ec.europa.eu/eurostat/databrowser/view/avia_paoc | dữ liệu | 2026-09-18 | lab 2, 4 |

## Phiên bản đã xác minh

| Thư viện / dataset | Phiên bản / sha256 | Nguồn xác minh |
|---|---|---|
| Python | 3.12.14 | nền buổi 11 |
| `ruptures` | **1.1.10** (PyPI, phát hành 2025-09-10) — bản mới nhất | PyPI JSON API 2026-09-18 |
| numpy / pandas / scipy / statsmodels | 2.5.3 / 3.0.5 / 1.18.1 / 0.15.0 | import trong nền |
| wikipedia-vi-tong | `481d604d1b58…`, 3.653 ngày 2016-01-01 → 2025-12-31, CC0 | `lay_du_lieu.py buoi-11` |
| wikipedia-vi-tet | `8f9e15ea3055…`, 3.653 ngày, CC0 | như trên |
| eurostat-hanh-khach-hang-khong | `6ce5178cf876…`, 218 tháng 2008-01 → 2026-02, CC BY 4.0 | như trên |

## Dữ liệu

| Bộ | Giấy phép (trích) | Ghi chú |
|---|---|---|
| Wikimedia Pageviews | CC0 1.0 | tổng lượt xem vi.wikipedia + bài "Tết Nguyên Đán" |
| Eurostat avia_paoc | CC BY 4.0 (Eurostat) | **thay US BTS T-100**: BTS chỉ có bảng HTML, `data.bts.gov` trả 403 |

Kiểm tính ổn định: tải hai lần endpoint SDMX 3.0 của Eurostat → sha256 **giống hệt** (18.866 byte).

## Trích nguyên văn (dùng trong tài liệu)

**PELT (`ruptures` docs).** "The algorithm relies on a pruning rule. Many indexes are discarded, greatly reducing the computational
cost while retaining the ability to find the optimal segmentation." Độ phức tạp trung bình $\mathcal{O}(CKn)$ với $K$ = số điểm gãy,
$n$ = số mẫu, $C$ = chi phí gọi hàm chi phí trên một đoạn.

**CROPS không có trong `ruptures`** — đã đọc hết user guide, không có mục nào. Do đó buổi này **tự quét penalty và vẽ elbow** (đúng như
lộ trình đã ghi).

**Hyndman & Rostami-Tabar (2024), abstract.** "This paper investigates several strategies for dealing with interruptions in time series
forecasting, including highly adaptable models, intervention models, **marking interrupted periods as missing**, forecasting what may
have been, downweighting the interruption period, and ensemble models."

**Kết luận của cùng bài.** "An intervention model is often a good solution, provided the intervention can be modelled relatively simply.
However, if the intervention is complex, then a highly adaptive method is often better… **The missing value approach is particularly
useful when only post-interruption forecasts are required** and forecasts during the interruption period are not needed." Và: "the
ensemble approach is useful when there is uncertainty about which approach to use".

→ Kết quả đo được của buổi khớp với câu in đậm: cách "coi COVID là thiếu rồi nội suy" cho MAPE thấp nhất (8,71%) khi chỉ cần dự báo
**sau** giai đoạn gián đoạn.

## Con số đo được (`dap-an/bat_thuong.py`, `dap-an/ve_hinh.py`)

**Lượt xem vi.wikipedia (3.653 ngày, 2016–2025):**

| Cách bắt ngoại lai | Số ngày gắn cờ | Tỷ lệ |
|---|---|---|
| 3σ toàn chuỗi | 16 | 0,44% |
| IQR 1,5 | 27 | 0,74% |
| MAD 3 (toàn chuỗi) | 15 | 0,41% |
| **Hampel k = 15** | **121** | 3,31% |
| STL robust (mùa vụ tuần) | 616 | 16,86% |

**Masking đo được:** thêm **một** điểm bằng 8× giá trị lớn nhất → số ngày 3σ bắt được tụt từ **16 xuống 5**; Hampel đi từ 121 lên 123
(không bị ảnh hưởng). Đây là bằng chứng số cho hiện tượng ngoại lai tự che mình.

**Bài "Tết Nguyên Đán":** **10/10 đỉnh Tết bị gắn cờ "ngoại lai" bởi CẢ NĂM phương pháp**, kể cả Hampel và STL robust. Đỉnh Tết rơi vào
ngày thứ 22–47 của năm dương (xê dịch **25 ngày**), nên STL với chu kỳ dương lịch không thể học được — cách sửa đúng là **nhật ký sự
kiện / biến giả lịch âm** (nối sang buổi 13).

**Hành khách hàng không EU27 (218 tháng):**
- PELT trên **mức thô**: **43 điểm gãy** (giả — chuỗi tăng trưởng nhân tính, phương sai tỷ lệ với mức).
- PELT trên **log**: 2 điểm gãy, **ổn định qua toàn bộ penalty 1–4·log n**: **2020-02-01** và **2021-05-01**.
  Ở penalty ≥ 5·log n thì PELT trả **0** điểm gãy (lộ trình cũ ghi "ổn định qua pen 2–10·log n" → **đã sửa**).
- Độ lớn: 2020-02 giảm **−78,7%** (86,4 triệu → 18,4 triệu khách/tháng); 2021-05 tăng **+238,2%** (12,8 → 43,2 triệu).
- Tháng đáy: 2020-04 với **890.607** khách, so với 2020-01 là 66.046.231 → **−98,65%**.

**Ba cách xử lý COVID** (học tới 2022-12, kiểm 12 tháng 2023, baseline mùa vụ nhân + xu hướng tuyến tính ước lượng trên toàn bộ phần học):

| Cách xử lý | Số kỳ học | MAPE | Sai số trung bình (nghìn khách) |
|---|---|---|---|
| giữ nguyên | 180 | **24,01%** | −19.710 |
| coi COVID là thiếu rồi nội suy | 180 | **8,71%** | −7.560 |
| cắt, chỉ dùng sau hồi phục | 18 | **18,11%** | +12.942 |

**Chuỗi mô phỏng có nhãn** (seed 0, n = 400): 4 loại bất thường cài sẵn (3 AO, 1 LS, 1 TC, 1 đổi phương sai) → `dan_nhan` trả 9 sự kiện,
**6/6 gắn đúng loại**, 3 cảnh báo giả.

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Hampel cũng gắn cờ đỉnh Tết.** Lộ trình ngầm định Hampel "bắt đỉnh tin tức" tốt hơn; đo ra thì với đỉnh Tết (gấp ~10 lần nền địa
  phương) **mọi** phương pháp đều gắn cờ. Bài học đúng là: **không có ngưỡng thống kê nào phân biệt được "lỗi đo" với "sự kiện thật" —
  chỉ có nhật ký sự kiện mới làm được.** Đã đưa vào tài liệu và test.
- **PELT phải chạy sau khi biến đổi.** Với chuỗi tăng trưởng nhân tính, không lấy log trước thì l2 coi mọi thay đổi phương sai là điểm
  gãy mức: 43 so với 2.
- **Đổi phương sai phải đo trên phần dư.** Trên chuỗi mẫu, σ thô ≈ 7,9 ở cả hai phía điểm gãy vì biên độ mùa vụ tuần át hết; phải khử
  mùa vụ (STL) rồi dùng **MAD** (không phải `std`, vì một AO đơn lẻ làm std phình gấp 4).
- **`model="l2"` chỉ nhìn trung bình**; muốn bắt đổi phương sai phải dùng `model="normal"` (chi phí Gaussian).
- **Số điểm gãy phải giảm đơn điệu theo penalty** — một phép kiểm rẻ để bắt lỗi cài đặt (đã thành một test).
- **Ba cách xử lý COVID chỉ khác nhau nếu baseline thật sự dùng dữ liệu cũ.** Bản đầu dùng drift trên 24 kỳ cuối → ba cách cho MAPE gần
  bằng nhau (15,25 / 15,46 / 12,61) và bài học biến mất. Đã đổi baseline sang xu hướng + mùa vụ ước lượng trên **toàn bộ** phần học.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình ghi PELT ổn định qua pen 2–10·log n; đo được là **1–4·log n** (≥5 thì ra 0 điểm gãy) | nhỏ | Sửa số trong lộ trình; test dùng khoảng đã đo |
| Lộ trình ghi điểm gãy 2020-04 và 2021-06; đo được **2020-02** và **2021-05** | nhỏ | Sửa lộ trình theo số đo (PELT đặt mốc ở đầu đoạn mới) |
| Lộ trình ghi Hampel gắn 121 ngày (đúng) nhưng ngụ ý Hampel cứu được đỉnh Tết | **lớn** | Đo ra 10/10 đỉnh Tết vẫn bị gắn cờ → đổi thông điệp của lab 3 sang "chỉ nhật ký sự kiện mới cứu được"; đã cập nhật lộ trình |
| Thêm `doi_phuong_sai` + `danh_gia_nhan` (lộ trình chỉ nêu 5 loại, không nêu cách chấm) | nhỏ | Đưa vào để đo được tiêu chí "Xong khi" (≥4/5 nhãn đúng) |
| Isolation Forest | nhỏ | Chỉ nhắc trong lý thuyết: cần sklearn + không dùng cấu trúc thời gian, kém Hampel trên chuỗi có xu hướng |
