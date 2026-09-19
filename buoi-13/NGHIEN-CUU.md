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

## Research viết lại (Phase 14, 2026-09-19)

Research sư phạm; phiên bản không đổi (numpy 2.5.3, pandas 3.0.5, scikit-learn 1.9.1, holidays 0.104).

| Khái niệm | Cách giải thích chọn | Hiểu lầm phổ biến | Nguồn |
|---|---|---|---|
| biết trước bao lâu | ba nhóm lịch / kế hoạch / quá khứ; ví dụ quán cà phê | "dự báo thời tiết là tương lai nên không được dùng" | FPP3 §7.4 *Useful predictors*; Kaufman và cộng sự (2012) |
| rolling, lag | bảng 6 ngày $(10, 12, 8, 14, 20, 16)$, in đậm ô nhìn trộm cho ba cách viết; bảng lag với $h$ = 2 | có `shift` là đủ, không cần `shift` ≥ $h$ | tài liệu pandas `rolling`, `shift` |
| ba rò rỉ toàn chuỗi | cùng 6 ngày: z-score, target encoding nhóm A/B, nội suy hai phía, mỗi kiểu một bảng | scaler "chỉ đổi thang nên vô hại" | Kapoor & Narayanan (2023), bảng phân loại rò rỉ |
| bài kiểm tự động | cắt–tính lại–so, bốn chi tiết; bảng ba bài kiểm bắt/bỏ sót gì | một bài kiểm xanh là đủ | số đo của buổi |
| Tết âm lịch | Meeus ở UTC+7, so `holidays` 2000–2035 | dùng thư viện lịch Trung Quốc | Meeus (1998) ch. 25, 49; `holidays` 0.104 |
| biến ngoại sinh | bảng 3 ngày thật/dự báo, rồi bảng giá của rò rỉ ERCOT | huấn luyện bằng giá trị thật "cho chính xác" | tài liệu pandas `merge_asof`; Open-Meteo Previous Runs API |

Rút gọn cấu trúc: 9 mục lý thuyết → 6. Số đo tái lập bằng `dap-an/ve_hinh.py` và notebook chạy trên `code/`: bộ đầu buổi 44 cột (25 `vô hạn`,
19 `t-h`); `kiem_ro_ri` đầu buổi bắt 4 cột, bỏ lọt `tb_7`; bản đã sửa bắt 5 cột, không bắt `y_dien_hai_chieu` (chuỗi đã `ffill`, không còn lỗ);
sau sửa 41 cột, hai bài kiểm rỗng; Tết khớp `holidays` 36/36 năm; bảng giá rò rỉ −3,85% / −3,10% / +2,20%. `python lab.py check`: code 4/13 đỏ,
đáp án 13/13 xanh (`kiem_tra_lab.py 13` đạt).

## Đọc thử (Phase 14, 2026-09-19)

Tự đọc (không subagent), theo checklist `tools/CHUAN-DE-HIEU.md`; mọi ví dụ tay và đáp án quiz tính lại bằng Python (bảng 6 ngày ba kiểu
rolling; z 13,33/4,32; trung bình nhóm 12,67/14; nội suy 13; sin/cos 0,87; câu 5: 5 và 6,5; câu 6: 3,49 và 1,54).

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (2.392 chữ, 44 cờ, 9 mục lý thuyết) | 8 | — | — | — | không có ví dụ tính tay cho rò rỉ; Fourier, sóc, target encoding, point-in-time dùng trước khi định nghĩa; quiz câu 2 tự mâu thuẫn ("ta chưa có… thực ra ta có"), câu 6 ghi MAE 1,33 (đo được 1,32) |
| 1 | viết lại (4.042 chữ) | 0 | 2 | 1 | 10/10 có căn cứ | khó: bảng rolling thiếu ô nhìn trộm ngày 2 của cột có tâm; Lab bước 1 gọi nhóm "mãi mãi" trong khi bảng in `vô hạn`. Nhỏ: README ghi 41 feature (đầu buổi là 44) |
| 2 | sau sửa (14 trang) | **0** | **0** | 0 | 10/10 | **đạt**. Rà gọn: không đoạn nào lặp ý (`lap_y` = 0); mục 6 là bảng tra, không lặp văn xuôi |

`kiem_de_hieu.py 13`: 44 → **0**. Quiz viết lại, căn cứ: 1 → 4.1, 2 → 4.2, 3 → 4.3, 4 → 4.5, 5 → 4.2, 6 → 4.4a, 7 → 4.6, 8 → 4.3, 9 → 4.6,
10 → 4.2–4.5.

## Đọc thử độc lập (Phase 15, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: sin/cos thứ 5, 6 và khoảng cách 0,868; bảng
rolling 6 ngày; z toàn chuỗi (13,33 / 4,32 / −0,77 … 0,62); trung bình đã biết 10 / 11 / 10 / 11 / 12,8; target encoding 12,67 / 14 và
10 / 12 / 9 / 13; Tết −1,9% / −16,9%; ERCOT −3,85 / −3,95 / +2,92 / −2,31%; quiz 5 (5 / 6,5), 6 (3,49; toàn chuỗi 1,54). Khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.5 chi tiết 4 + Tự kiểm tra | "feature của các dòng trước mốc đó (cho tầm $h$)"; "`lag_1` của 23 giờ ngay trước mốc" | 4 | không rõ dòng nào phải giữ nguyên; đáp án nói "trước mốc" trong khi theo quy tắc t − h, các dòng bị đổi nằm **sau** mốc | khó |
| 2 | 4.2 | "sáng ngày 3 phải đoán ngày 5" | 4 | sáng ngày 3 chưa có $y_3$, nên `lag_2` cũng nhìn trộm — mâu thuẫn bảng | khó |
| 3 | 4.6 Đọc bảng + Tự kiểm tra | "huấn luyện bằng đúng loại dữ liệu sẽ gặp"; "+2,20%… khuếch đại sai số" | 4 | với dự báo 3 ngày, huấn luyện bằng chính bản dự báo còn tệ hơn (+2,92% so với +2,20%): lời khuyên và lời giải thích không khớp số | khó |
| 4 | 4.1 | "backtest đẹp, dùng thật thì sập" | 1 | "backtest" không định nghĩa trong buổi | nhỏ |
| 5 | 4.3 | "thuật toán thiên văn của Meeus… đông chí" | 1 | tên riêng, không cản | nhỏ |
| 6 | 4.5 | "cả ba chạy trong vài giây" | 3 | không cản | nhỏ |

**Lỗi code tìm được khi kiểm #1 bằng Python.** `kiem_nhieu_muc_tieu` (cả `code/` và `dap-an/`) giữ các dòng `a.index[: cat − tam + 1]`,
tức chỉ những dòng có **mục tiêu** trước mốc. Các dòng đó không bao giờ thấy phần bị đổi, nên bài kiểm chỉ lặp lại bài cắt tương lai và
**không bắt lag < tầm dự báo** (thử: `y.shift(1)` với $h$ = 24 báo sạch). Sửa theo `tools/khung/ro_ri.py` (`thu_tu < p + h`): giữ
`a.index[: cat + tam]`, tức mọi dòng có thời điểm ra dự báo $t − h$ trước mốc. Sau sửa: $h$ = 24 bắt `lag_1` và rolling không shift; $h$ = 1
chỉ bắt rolling không shift; feature hợp lệ không bị bắt. Hàm không phải chỗ hở cố ý (học viên không sửa nó), nên sửa ở cả hai bản.
`kiem_tra_lab.py 13` vẫn đạt (đáp án xanh, `code/` đỏ đúng 4/13).

### B. Giải thích lại (ví dụ số mới)

- **Biết trước bao lâu**: dự báo tuần sau — lịch lễ (mãi mãi), kế hoạch khuyến mãi (từ lúc công bố), doanh số tới hôm nay.
- **Lag/rolling**: $h$ = 3 → `y.shift(3).rolling(7)`, lag nhỏ nhất 3.
- **Sin/cos**: giờ 23 và giờ 0 với góc $2\pi \cdot$ giờ/24: cos 0,966 và 1, gần nhau.
- **Rò rỉ toàn chuỗi**: 2, 4, 12: z của 2 dùng trung bình 6 đã chứa 12.
- **Kiểm rò rỉ**: `lag_1` với $h$ = 2, đổi $y$ từ ngày 10 → feature dòng 11 đổi, mà lúc dự báo cho dòng 11 (ngày 9) chưa có ngày 10.
- **Ngoại sinh**: dự báo nhiệt độ sai 3 °C → mô hình học trên nhiệt độ thật bị lệch lúc chạy.

### C. Quiz mù

1 C · 2 C · 3 B · 4 C · 5 5 (nhìn trộm) / 6,5 · 6 3,49 · 7 `nearest` lấy bản ghi sau; không `tolerance` kéo số cũ · 8 quanh Tết −16,9%, giữ · 9 −3,85% là
nhiệt độ thật; dự báo 3 ngày +2,92%; chỉ dùng dự báo 1 ngày · 10 không; từng dòng. Căn cứ: 1 → 4.1; 2, 5 → 4.2; 3, 8 → 4.3; 4 → 4.5; 6 → 4.4a;
7, 9 → 4.6; 10 → 4.2–4.5. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 3 / nhỏ 3. Sửa một điều: mô tả kiểm nhiễu mục tiêu (kéo theo sửa hàm).

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10.** Sửa: 4.5 chi tiết 4 "cộng nhiễu lớn vào $y$ từ 70% chuỗi trở đi; dòng nào có thời điểm ra dự báo $t − h$ còn trước mốc
đó thì feature không được đổi"; đáp án Tự kiểm tra "23 dòng ngay sau mốc… lúc ra dự báo (24 giờ trước) phần bị đổi chưa xảy ra"; 4.2 "tối
ngày 3"; 4.6 Đọc bảng + Tự kiểm tra: dự báo trước 3 ngày kém tới mức huấn luyện bằng nó cũng hại (+2,92%), bỏ feature; 4.1 "chấm trên lịch
sử (backtest)". Docstring `kiem_nhieu_muc_tieu` viết lại theo quy tắc $t − h$.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 15 đọc mù | 4.042 | 14 | 0 | 3 | 3 | 10/10 | 0 |
| sau sửa, đọc lại | 4.100 | 14 | **0** | **0** | 2 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 13` 0; `kiem_tra_lab.py 13` đạt; tự chứa đạt.

## Đọc thử độc lập đề dự án giữa chặng 1 (Phase 15, 2026-09-19)

Vai học viên vừa xong buổi 13; mở `de-bai.md`, `RUBRIC.md`, `code/README.md` và khung `code/*.py` (không mở `giam-khao/`).

**Viết lại được:** *Làm gì* — EDA ba nguồn khí tượng; tìm 6 lỗi cài sẵn (6 loại cho trước, không biết vị trí) chỉ bằng dữ liệu phát; pipeline
làm sạch có cột cờ, không mất mốc, chỉ điền lỗ ngắn; ≥ 20 feature dự báo Nội Bài 12 giờ tới qua hai bài kiểm rò rỉ; nhật ký quyết định.
*Nộp gì* — thư mục tên mình: notebook + PDF báo cáo, `bao-cao-loi.json`, `lam_sach.py`, `feature.py` (giữ tên hàm của khung), `nhat-ky.md`,
test riêng. *Chấm thế nào* — 100 điểm: A 30 (máy chấm JSON, 5 điểm/lỗi, báo sai −2, trần −6), B 25 EDA, C 25 pipeline + test (10 điểm là
`python lab.py check` xanh), D 10 chống rò rỉ, E 10 trình bày; thưởng tối đa +5.

| # | Chỗ | Vấn đề | Mức |
|---|---|---|---|
| 1 | đề 2.4 + RUBRIC D | đòi "kiểm nhiễu mục tiêu" nhưng khung `feature.py` không có hàm đó; "có in kết quả" không nói in ở đâu | mơ hồ |
| 2 | đề 2.4 + RUBRIC D | baseline "để đối chiếu" / "trên cùng tập kiểm, cùng chỉ số" — đề không yêu cầu mô hình nào, nên "cùng" với gì, tập kiểm nào? | mơ hồ |
| 3 | đề 2.2 | "trừ 2 điểm" lặp RUBRIC nhưng thiếu trần −6; "lệch tới 3 ngày vẫn tính đúng" trộn hai luật của RUBRIC A | nhỏ (lặp) |
| 4 | RUBRIC thưởng | "một hàm tự động" không nói đặt ở đâu | nhỏ |

Sửa: đề 2.4 ghi rõ tự thêm hàm kiểm nhiễu mục tiêu; baseline = MAE seasonal naive 12 giờ tới trên phần cuối chuỗi Nội Bài, ghi mốc chia; kết
quả hai bài kiểm + MAE baseline in trong báo cáo EDA. RUBRIC D khớp theo. Đề 2.2 trỏ về RUBRIC A thay vì chép luật. Thưởng +3: "hàm trong
`lam_sach.py`". Lời giải mẫu (`giam-khao/loi-giai-mau/feature.py`) thêm `kiem_nhieu_muc_tieu` bản đúng: 26 feature, cắt tương lai sạch, nhiễu
mục tiêu sạch; bộ chấm với `BAI=giam-khao/loi-giai-mau` 8/8 xanh. Sau sửa đọc lại: 0 chỗ mơ hồ, 0 lặp đáng kể giữa đề/rubric/README.
PDF 5 trang.

## Đọc thử độc lập Phụ lục D (Phase 15, 2026-09-19)

Vai học viên sắp vào buổi 14 (phụ lục tra cứu). Mọi ví dụ tính lại bằng NumPy/SciPy: MAE 1,6, RMSE 2,10, ME 0,8, MAPE 12,8%, sMAPE 13,6,
WAPE 0,133; MASE 1,07, RMSSE 1,33; pinball 0,40; Winkler 6,4, coverage 80%; WIS 1,67; CRPS 0,6 và 0,4762; Brier 0,142 / 0,24, log score 0,430;
skill 0,38 / 0,41; DM $S_1$ −0,94, $S_1^*$ −0,84, p 0,45; mục 9 (2,75 / 3,3541 / 1,25 / 10,7798 / 11,3351 / 0,1111 / 1,875 / 1,4667 / 3,875 /
1,7039; pinball 2,70 / 5,40; Murphy 0,015 / 0,085 / 0,240). Khớp hết.

| # | Mục | Trích | Vì sao | Mức |
|---|---|---|---|---|
| 1 | 4 Winkler | "$\mathbb{1}\{y_t < \ell_t\}$", "danh nghĩa" | ký hiệu và từ không giải thích; công thức không có danh sách ký hiệu | khó |
| 2 | 5 CRPS | "$F$", "$\mathbb{E}_F$", "$\Phi$", "$\varphi$" | hàm phân phối tích luỹ, hàm mật độ không định nghĩa | khó |
| 3 | 3 Bẫy | "một bước, trong mẫu" | "trong mẫu" chưa định nghĩa | nhỏ |
| 4 | 4 WIS | "WIS chỉ xấp xỉ CRPS" | CRPS ở mục sau | nhỏ |
| 5 | 8 | "tự hiệp phương sai", "Student-t" | buổi 15 dạy; phụ lục tra cứu | nhỏ |
| 6 | 6 PDF | "\0,04" | dấu `\ ` cuối dòng nguồn in ra ký tự lạ | nhỏ |

Sửa: dòng ký hiệu dưới Winkler ($\mathbb{1}$, "danh nghĩa 80%"); CRPS định nghĩa $F(y)$, $\mathbb{E}_F$, và dòng ký hiệu dưới công thức đóng
($\mu$, $\sigma$, $\Phi$, $\varphi$, $N(0, 1)$); "trong mẫu" → "trên tập huấn luyện"; nối dòng ví dụ Brier (PDF hết "\0,04"). Giữ #4, #5. Sau sửa
đọc lại: 0 chặn / 0 khó / 2 nhỏ; 0 chỗ thừa đáng kể. PDF 7 trang.
