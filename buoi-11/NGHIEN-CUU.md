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

## Research viết lại (Phase 13, 2026-09-18)

Research sư phạm; phiên bản không đổi (ruptures 1.1.10).

| Khái niệm | Cách giải thích chọn | Hiểu lầm phổ biến | Nguồn (truy cập 2026-09-18) |
|---|---|---|---|
| z-score, masking | 10 số tính tay: $z$ của 50 chỉ 2,84; thêm 60 thì 1,61; với $n$ số $\lvert z \rvert \le (n-1)/\sqrt n$ nên ngưỡng 3 không bao giờ vượt ở mẫu nhỏ; hình mới `masking-10-so.png` | "không vượt 3σ = không có ngoại lai"; swamping bị quên | Rousseeuw & Hubert 2018 (WIREs); Wikipedia *Median absolute deviation* |
| MAD, Hampel | cùng 10 số: trung vị 12, MAD 1,48, điểm của 50 là 25,6 | MAD = 0 khi hơn nửa số bằng nhau; Hampel `center=True` là không nhân quả | như trên |
| PELT, penalty | 10 số có dịch mức: chi phí 254 / 4 / 3,17; cắt khi giảm chi phí > penalty 6,9 (kiểm bằng `ruptures`: `[5, 10]`) | penalty là "số điểm gãy tối đa"; không lấy log với chuỗi tăng trưởng | Lancaster MATH337 (Romano) *PELT, WBS and penalty choices*; tài liệu ruptures; ArcGIS *How change point detection works* ("phải giảm chi phí nhiều hơn penalty") |
| bốn loại bất thường | bảng 4 chuỗi 8 điểm, chỉ điểm sau mới cho biết loại | gọi mọi thứ là "ngoại lai" | Chen & Liu 1993 |

**Sửa code (không phải chỗ hở):** nhãn "LS (đổi mức)" → "LS (dịch mức)" theo Phụ lục E; cột "sai số trung bình" của `ba_cach_xu_ly_covid` đổi
dấu theo quy ước khoá (thực tế − dự báo: giữ nguyên +19.710, nội suy +7.560, cắt −12.942 nghìn khách); nhãn "coi COVID là ngoại lai (nội suy)"
→ "coi COVID là thiếu (nội suy)" cho khớp cách làm; `ve_hinh.py` thêm hình `masking-10-so.png`. Mọi số khác tái lập đúng.

**Phát hiện khi viết Lab:** bản `code/` của `doi_phuong_sai` không "báo khắp nơi" như tài liệu cũ ghi, mà **bắt hụt** (trả danh sách rỗng trên
chuỗi mô phỏng) — sửa Trạng thái đầu buổi, Lab bước 4, Lỗi thường gặp, README theo đúng số chạy.

## Đọc thử (Phase 13, 2026-09-18)

Tự đọc (không subagent), theo checklist `tools/CHUAN-DE-HIEU.md`; mọi ví dụ tay và đáp án quiz tính lại bằng Python/`ruptures`.

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (2.343 chữ, 9 trang, 56 cờ) | 10 | — | — | — | chặn: không bảng Từ mới; AO/LS/TC chỉ tên tiếng Anh; winsorize, biến giả, MAPE, BIC/MBIC không định nghĩa; MAD "nhắc lại từ buổi 10" nhưng buổi 10 không dạy; công thức PELT không lời, không ví dụ; CUSUM công thức trần; nhiều trích tiếng Anh (ruptures, Hyndman & Rostami-Tabar) mang ý chính; không hình nào có "Cách đọc hình" |
| 1 | viết lại (4.196 chữ) | 0 | 1 | 3 | 10/10 có căn cứ | khó: Lab bước 4 và Trạng thái mô tả sai triệu chứng của `doi_phuong_sai` (xem trên). Nhỏ: vì sao $\lvert z\rvert \le (n-1)/\sqrt n$ chỉ nêu, không chứng minh; "chạy gần tuyến tính theo độ dài"; đáp án Tự kiểm tra 4.3 nói sai cách code xử lý MAD = 0 |
| 2 | sau sửa (4.204 chữ, 13 trang) | **0** | **0** | 2 | 10/10 | **đạt**. Rà gọn: không đoạn nào ≥ 30 chữ lặp ý |

`kiem_de_hieu.py 11`: 56 → **0**. PDF 9 → 13 trang (thêm nội dung: ví dụ 10 số cho z-score, MAD, PELT; bảng khi nào dùng/không; không độn).
Quiz viết lại, căn cứ: 1 → 4.1, 2 → 4.2, 3 → 4.4, 4 → 4.5, 5 → 4.2–4.3, 6 → 4.5, 7 → 4.4, 8 → 4.6, 9 → 4.5, 10 → 4.2–4.4.

## Đọc thử độc lập (Phase 15, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại bằng Python: 15,6 / 12,1 / $z$ 2,84; thêm 60 →
$s$ 18,4, $z$ 1,61/2,15, ngưỡng 3σ 52 → 75,6; $(5, 5, 5, 5, 100)$ $z$ 1,79; MAD 25,6; PELT 254 / 4 / 3,17, $3 \ln 10$ = 6,9; −78,7%; quiz 5
($z$ 2,04, MAD 81), 6 (1 / 2 điểm gãy). Lệch: "bỏ số 50 thì độ lệch chuẩn khoảng 0,9" (thật 0,97); +238,2% so với 237,5% tính từ số đã làm
tròn (giữ, tài liệu tính từ số chưa làm tròn).

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.2 | "bỏ số 50 thì chỉ khoảng 0,9" | 5 | tính lại ra 0,97 | nhỏ |
| 2 | 4.3 bảng | "IQR 1,5 (ngưỡng theo quantile 0,25 và 0,75)" | 1 | không nói quy tắc 1,5 là gì | nhỏ |
| 3 | 4.2 hình | "vị trí vạch cam so với các chấm lẻ ở hai ô" | 5 | Ký hiệu không nói hai ô khác nhau thế nào | nhỏ |
| 4 | 4.4 hình | "độ cao các chấm xanh ở ô phải" | 5 | chấm xanh không có trong Ký hiệu | nhỏ |
| 5 | 4.3 | "làm feature dự báo" | 6 | chen tiếng Anh, buổi 9 gọi là "đặc trưng" | nhỏ |
| 6 | 4.5 công thức | "$y_{\tau_k : \tau_{k+1}}$" | 2 | $\tau_0$, $\tau_{K+1}$ không nói (câu Nói bằng lời đủ) | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Bốn loại**: 5, 5, 9, 5, 5 là AO; 5, 5, 9, 9, 9 là dịch mức.
- **Masking**: $(1, 1, 1, 1, 1, 1, 1, 1, 1, 30)$: $|z|$ tối đa $9/\sqrt{10}$ ≈ 2,85 nên 30 không bị gắn cờ.
- **MAD**: 4, 5, 5, 6, 40 → trung vị 5, khoảng cách 1, 0, 0, 1, 35 → MAD 1,48, điểm của 40 ≈ 23,6.
- **Nhật ký sự kiện**: ngày khai trương mỗi năm → giữ + biến giả.
- **PELT**: chi phí 100 → 10 khi cắt một lần; penalty 50 thì cắt, 95 thì không.
- **COVID**: sự kiện đã qua, hành vi quay về → coi là thiếu.

### C. Quiz mù

1 C · 2 B · 3 A · 4 B · 5 $z$ 2,04 không gắn cờ; điểm MAD ≈ 81 gắn cờ · 6 penalty 10 → 1, penalty 3 → 2 · 7 nhật ký sự kiện + biến giả · 8 coi là
thiếu (hoặc biến giả) · 9 chọn trong khoảng ổn định 1–4 ln n: 2 điểm gãy · 10 3σ: masking + dồn vào mức cao, xoá thủng mốc; STL robust: phần dư
còn mùa vụ năm. Căn cứ: 1 → 4.1; 2, 5 → 4.2–4.3; 3, 7 → 4.4; 4, 6, 9 → 4.5; 8 → 4.6; 10 → 4.2–4.4. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 0 / nhỏ 6.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10.** Sửa: "khoảng 1"; ô IQR ghi rõ "ngoài khoảng quantile 0,25 → 0,75, nới mỗi phía 1,5 lần độ rộng"; Ký hiệu hình masking
(ô trái dãy ví dụ, ô phải thêm ngoại lai thứ hai — kiểm với `ve_hinh.py`) và hình Tết (chấm xanh ô phải); "feature dự báo" → "đặc trưng
đầu vào cho dự báo" (2 chỗ). Giữ #6.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 15 đọc mù | 4.204 | 13 | 0 | 0 | 6 | 10/10 | 0 |
| sau sửa, đọc lại | 4.261 | 13 | **0** | **0** | 1 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 11` 0; `kiem_tra_lab.py 11` đạt; tự chứa đạt.
