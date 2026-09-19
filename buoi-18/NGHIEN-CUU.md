# Nhật ký research — Buổi 18: Hồi quy chuỗi thời gian và hồi quy động

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-19 (Phase 19). Buổi soạn mới hoàn toàn (thư mục tạo từ khuôn).
- **Người/phiên:** Phase 19, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | FPP3 ch. 7 (7.1 mô hình tuyến tính, giả định sai số không tự tương quan; 7.3 hồi quy giả: R² cao + phần dư tự tương quan là dấu hiệu, ví dụ hành khách Úc ~ lúa gạo Guinea; 7.4 xu hướng, biến giả mùa vụ m − 1 cột, biến can thiệp spike/step/đổi độ dốc, lễ, distributed lag, Fourier K ≤ m/2; 7.5 không chọn biến bằng p-value, dùng AICc/AIC/CV; 7.6 dự báo ex-ante / ex-post / kịch bản; 7.7 xu hướng theo khúc): https://otexts.com/fpp3/regression.html | sách giáo khoa | 2026-09-19 | 4.1, 4.2, 4.5 |
| 2 | FPP3 ch. 10 (hồi quy với sai số ARIMA: $y_t = \beta x_t + \eta_t$, $\eta_t$ ARIMA; sai số tự tương quan làm sai số chuẩn và p-value sai, ước lượng kém hiệu quả; mọi biến cần dừng hoặc cùng sai phân; dự báo cần dự báo biến giải thích; dynamic harmonic regression chọn K bằng AICc; lagged predictors): https://otexts.com/fpp3/dynamic.html | sách giáo khoa | 2026-09-19 | 4.3, 4.4 |
| 3 | FPP3 §12.1 complex seasonality (STL nhiều chu kỳ, DHR nhiều bộ Fourier; ví dụ tải điện Victoria "a crude model for a complicated process", phần dư còn nhiều cấu trúc): https://otexts.com/fpp3/complexseasonality.html | sách giáo khoa | 2026-09-19 | 4.4 |
| 4 | FPP3 §12.2 Prophet ($g(t) + s(t) + h(t) + \varepsilon_t$; xu hướng tuyến tính theo khúc, changepoint tự chọn; Fourier bậc 10 năm, 3 tuần; lễ là biến giả; "rarely gives better forecast accuracy than the alternative approaches"): https://otexts.com/fpp3/prophet.html | sách giáo khoa | 2026-09-19 | 4.6 |
| 5 | PyPI prophet: 1.4.0 (15/8/2026), 1.3.0 (27/1/2026, hỗ trợ pandas 3, numpy 2.4); phụ thuộc cmdstanpy ≥ 1.0.4, holidays ≥ 0.25 < 1: https://pypi.org/project/prophet/ ; release notes GitHub facebook/prophet | tài liệu chính thức | 2026-09-19 | phiên bản; **còn bảo trì** (4 bản trong 12 tháng) |
| 6 | statsforecast 2.1.1: `AutoARIMA(...).fit(y, X)`, `predict(h, X)` (hồi quy với sai số ARIMA); `MSTL(season_length=[24, 168], trend_forecaster=...)` — trend_forecaster không được có mùa vụ (ETS dùng `model="ZZN"`); `AutoTBATS(season_length, ...)` | tài liệu + chạy thử | 2026-09-19 | code |
| 7 | Granger & Newbold (1974), "Spurious regressions in econometrics", *J. Econometrics* 2 — hai bước ngẫu nhiên độc lập cho t-test bác bỏ quá nhiều | bài gốc (qua FPP 7.3) | 2026-09-19 | 4.2 mô phỏng |
| 8 | Taylor & Letham (2018), "Forecasting at scale", *The American Statistician* 72(1) | bài gốc Prophet | 2026-09-19 | 4.6 |

## Phiên bản đã xác minh

prophet **1.4.0** (thêm vào `tools/nen/phien-ban.toml`, cmdstanpy 1.3.0 trong `uv.lock`), statsforecast 2.1.1, statsmodels 0.15.0, holidays
0.104, pandas 2.3.3 (ràng buộc Nixtla). Prophet 1.4.0 chạy được ngay (wheel có sẵn CmdStan), không cần cài trình biên dịch.

## Dữ liệu (đều đã có trong danh mục)

| Bộ | sha256 rút gọn | Giấy phép | Dùng |
|---|---|---|---|
| `eurostat-hanh-khach-hang-khong` | `6ce5178cf876` | CC BY 4.0 | 4.2 (y), 2010–2019 |
| `frb-g17-san-luong-cong-nghiep` | `3956c6626866` | public domain | 4.2 (x), 2010–2019 |
| `eia930-balance-2024-h1`, `-h2` | `26768c495c3b`, `a602a8e577cf` | public domain | 4.3–4.4, ERCOT |
| `open-meteo-dallas-du-bao-luu-2024` | `5c7b56f9f713` | CC BY 4.0 | nhiệt độ đo sau + dự báo trước 1 ngày |
| `wikipedia-vi-tong` | `481d604d1b58` | CC0 | 4.5–4.6, Prophet và Tết |

## Số liệu thật (`dap-an/ve_hinh.py`, `dap-an/hoi_quy.py`)

| Đại lượng | Giá trị |
|---|---|
| Hồi quy thường hành khách ~ ip + 11 biến giả tháng (2010–2019, 120 tháng) | hệ số 1,888 triệu khách/điểm; p 3,3·10⁻¹⁶; R² 0,833; ACF trễ 1 phần dư 0,957; Ljung–Box p ≈ 7·10⁻²²⁶; phần dư dương 47 tháng liền |
| Thêm biến xu hướng $t$ | hệ số −0,680, p 2,8·10⁻⁷ (đổi dấu, vẫn "có ý nghĩa") |
| Hồi quy động, sai số SARIMA(0,1,1)(0,1,1)12 | hệ số 0,099, p 0,585; Ljung–Box p (24 trễ) 0,640 |
| Mô phỏng 1.000 cặp bước ngẫu nhiên n = 120, seed 0 | p < 0,05: trên mức 78,5%, trên sai phân 6,5% |
| Ví dụ tay $a = (0, -1, 1, 2, 4, 6)$, $b = (1, 2, 3, 4, 6, 6)$ | tương quan mức 0,928; tương quan sai phân 0,0 |
| Tải ERCOT theo nhiệt độ trung bình ngày (Dallas) | < 5 °C: 58,6 GW; 15–21 °C: 45,1 GW; > 30 °C: 65,3 GW |
| Nhịp ngày tháng 1/2024 (giờ Texas) | hai đỉnh 8–9 giờ (55,8 GW) và 20 giờ; đáy 47,9 GW; MAE xấp xỉ Fourier K = 1, 2, 4: 1.971, 348, 145 MW (tháng 7 chỉ một đỉnh, K = 1 đã sát: 267 MW — không minh hoạ được, đã đổi) |
| AICc DHR theo K (cửa sổ cutoff 9/8/2024) | (2, 2) 20.924,7; (4, 2) 20.843,8; (6, 4) 20.561,7; (10, 6) 20.281,8 → dùng K ngày 10, K tuần 6 |
| Backtest 24 cửa sổ (học 8 tuần, dự báo 24 giờ, cutoff 6/3 → 30/12/2024 cách 13 ngày) | MAE TB / trung vị (MW): DHR 2.082 / 1.738; MSTL 2.104 / 2.009; SN24 2.173 / 1.790; TBATS 2.438 / 2.132; OLS 2.951 / 2.789; Prophet 2.998 / 2.657; SN168 3.319 / 2.473 |
| DM (sai số tuyệt đối từng giờ, h = 24, HLN) | DHR − SN24 −0,30, p 0,76; DHR − MSTL −0,09, p 0,93; DHR − Prophet −2,39, p 0,017; DHR − OLS −2,60, p 0,010; MSTL − SN24 p 0,73 |
| DHR dùng nhiệt độ đo sau (ex-post) cho ngày dự báo | MAE 2.235 (so với 2.082 khi dùng nhiệt độ dự báo) — không tốt hơn trên 24 cửa sổ này |
| Phần dư DHR (sai số ARIMA(1,1,0), cửa sổ 9/8) | Ljung–Box p ≈ 5·10⁻⁵² (24 trễ): phần dư theo giờ **không trắng** (như FPP §12.1) |
| Prophet trên lượt xem vi.wikipedia, học tới 31/12 năm trước | MAE quanh Tết (± 7 ngày): 2024 mặc định 0,355 → khai Tết 0,118; 2025 0,234 → 0,153 (triệu lượt/ngày). Cả năm 2024: Prophet mặc định 0,304, khai Tết 0,290, seasonal naive 364 ngày 0,260; 2025: 0,486 / 0,484 / 0,459 |
| Thành phần Prophet ngày 9/2/2024 (học 2016–2023) | không khai Tết: xu hướng 2,425, tuần −0,018, năm −0,255 → 2,152; khai Tết: 2,444, −0,018, −0,066, Tết −0,726 → 1,634; thực tế 1,478 |
| Tết 2024 (mùng 1 = 10/2) | lượt xem ngày 9/2 bằng 60% mức trung bình 2–4 tuần trước; từ 3/2 đã còn 74% |
| Thời gian | backtest ERCOT 24 cửa sổ ~7 phút lần đầu (TBATS ~9 s/cửa sổ) → notebook lưu cache `du-lieu/cache/`; bộ chấm không chạy backtest này |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Bẫy thứ trong tuần (buổi 15) tái hiện khi soạn**: bản đầu đặt cutoff cách 14 ngày → mọi cửa sổ cùng một thứ; đổi thứ của cutoff làm MAE của
  seasonal naive 24 giờ nhảy từ 1.996 lên 3.163 MW. Bản chốt dùng bước 13 ngày (cutoff xoay qua mọi thứ).
- Bản đầu còn để cửa sổ cuối vượt hết tệp nhiệt độ (7 giờ NaN bị `mean` bỏ qua âm thầm) → cắt tải ở 31/12/2024 06:00 UTC.
- Thêm xu hướng làm hệ số hồi quy giả **đổi dấu** mà vẫn p < 10⁻⁶ — minh hoạ p-value vô nghĩa khi phần dư tự tương quan.
- Tải phụ thuộc nhiệt độ **phi tuyến** (chữ U, dốc dần): CDD/HDD tuyến tính chưa đủ; thêm CDD², HDD² (bản thử nghiệm đầu, 24 cửa sổ cách 14 ngày: MAE
  2.071 → 1.845).
- Prophet mặc định không có lễ nào; `add_country_holidays("VN")` có Tết nhưng chỉ đúng các ngày nghỉ, trong khi lượt xem sụt từ ~7 ngày trước →
  khai Tết với `lower_window = −7, upper_window = 7`.
- "Xong khi" của lộ trình ("DHR có phần dư trắng, thắng seasonal naive") không đạt nguyên văn trên dữ liệu giờ: phần dư theo giờ không trắng,
  và DHR chỉ ngang seasonal naive/MSTL (DM p 0,76). Tài liệu báo đúng như vậy; phần dư trắng đạt ở hồi quy động theo tháng (4.3, p 0,64).

## Research viết lại (sư phạm)

- Hồi quy giả: "hai thứ cùng lớn lên theo thời gian" (chiều cao của con và giá nhà) — ví dụ 6 số tính tay tương quan mức 0,93, sai phân 0.
- Sai số ARIMA: "phần mô hình chưa giải thích được hôm nay còn kéo sang ngày mai".
- Fourier: "cộng vài làn sóng để vẽ lại nhịp ngày".
- Prophet: "hồi quy với xu hướng gãy khúc + Fourier + lễ; dễ dùng, nhưng không tự biết lễ âm lịch".

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lab 1 "doanh số ~ chuỗi xu hướng không liên quan" | nhỏ | hành khách EU ~ sản lượng công nghiệp Mỹ (cả hai có trong danh mục) + mô phỏng 1.000 cặp bước ngẫu nhiên |
| Lab 2 "Fourier(ngày, tuần) + CDD/HDD + lễ, sai số ARIMA" | nhỏ | làm đúng; thêm CDD², HDD²; nhiệt độ Dallas (không có file dự báo Houston) |
| "Xong khi": DHR phần dư trắng, thắng seasonal naive | nhỏ | báo trung thực: DHR ngang SN24/MSTL, thắng Prophet và hồi quy thường có ý nghĩa; phần dư trắng ở ví dụ tháng. Cập nhật "Xong khi" trong tài liệu và lo-trinh |
| Distributed lag, piecewise trend | nhỏ | nói ngắn trong 4.5 (biến can thiệp), không lab riêng — giữ ≤ 6 khái niệm |
| Chỗ hở | nhỏ | `he_so_ip` dùng hồi quy thường (p 3·10⁻¹⁶); `KHAI_TET = False`. Test rò rỉ: dự báo DHR không đổi khi nhiệt độ đo thật sau cutoff đổi (đạt cả code và đáp án) |

## Đọc thử (Phase 19, 2026-09-19)

Tự đọc (không subagent), checklist `tools/CHUAN-DE-HIEU.md`. Tính lại bằng Python: ví dụ quý (24,5; 31,5; 24); ví dụ tay hồi quy giả (TB 2 và
3,67; tích sai phân 0, 0, 0, 0,8, −0,8 → tương quan 0; mức 0,928); AR(1) 12,4 và tự kiểm tra 28 / 29; Fourier $t$ = 6 → 10, $t$ = 0 → −5;
mọi số của bảng 4.3, 4.4, 4.6 lấy từ `ve_hinh.py`; quiz 5 (142; 131,5), 6 (tương quan sai phân −1; mức 0,99), 7 (26; 33,6), 10 (4,2%; 30,6%).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 4.082 | 14 | 0 | 3 | 3 | 10/10 | khó: "sai số chuẩn" dùng ở 4.2 mà mục 2 không nhắc; ví dụ tay 4.6 gắn ngày thật mà số tự đặt; hình Fourier tháng 7 không cho thấy $K$ lớn có ích (nhịp hè một đỉnh). Nhỏ: "dynamic harmonic regression" giữ tiếng Anh; TBATS không giải nghĩa từng chữ; mục 2 gọi ex-post là "gian lận" (4.3 nói được dùng khi phân tích) |
| 2 | 4.113 | 13 | **0** | **0** | 2 | 10/10 | mục 2 thêm sai số chuẩn; 4.6 dùng thành phần Prophet thật (2,15 / 1,63, thực tế 1,48); hình Fourier đổi sang tháng 1 (hai đỉnh; MAE 1.971 → 145 MW); sửa chữ "gian lận" |
| rà gọn | biên tập viên | — | — | — | — | — | 1 chỗ thừa nhỏ ("Khi nào dùng" 4.4 nhắc lại kết luận bảng), giữ vì thêm ý phần dư chưa trắng |

Căn cứ quiz: 1, 6, 9 → 4.2; 2, 3, 7 → 4.3; 4 → 4.5–4.6; 5 → 4.1; 8 → 4.5; 10 → 4.4. `kiem_de_hieu.py 18` 0; `kiem_tra_lab.py 18` đạt.

## Đọc thử độc lập (Phase 21, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: ví dụ quý (24,5; 31,5; quý 12 = 24); tương quan
mức 0,93 / sai phân 0; hồi quy động 12,4 và tự kiểm tra 28 / 29; Fourier 10 / −5; thành phần Prophet; quiz 5 (142; 131,5), 6 (sai phân −1),
7 (26; 33,6). Thử lại Lab bước 2 bằng venv buổi: SARIMAX không bỏ phần dư đầu → Ljung–Box p = 0,0004 (bộ chấm đỏ); bỏ 13 điểm → 0,64.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | Lab bước 2 | "`SARIMAX` của statsmodels, chỉ đưa cột `ip`" | 4 | không có cú pháp; và phải bỏ 13 phần dư đầu (sai phân 1 + 12) mới qua Ljung–Box — không làm thì bộ chấm báo "phần dư còn tự tương quan" dù đã dùng đúng hồi quy động | chặn |
| 2 | 4.1 | "quý 3 cao hơn quý 1 cùng năm 6 đơn vị" | 4 | thay số: quý 9 là 24,5, quý 11 là 31,5 — chênh 7 (có cả xu hướng) | khó |
| 3 | 4.6 | "2,44 − 0,02 − 0,07 − 0,73 = 1,63" | 4 | cộng các số hiển thị ra 1,62 | khó |
| 4 | 4.1 | "trùng với hệ số chặn" | 1 | "hệ số chặn" chưa định nghĩa | nhỏ |
| 5 | 4.3 | "(2.235 so với 2.082 MW)" | 3 | không rõ số nào của nhiệt độ đo thật | nhỏ |
| 6 | 4.4 | "dự báo xu hướng bằng ETS" | 8 | ETS không nhắc ở mục 2 | nhỏ |
| 7 | 4.4 | "TBATS là mô hình state space" | 1 | "state space" chưa giải nghĩa | nhỏ |
| 8 | 6 | "`lower_window`, `upper_window`" | 1 | tham số Prophet không giải thích | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Hồi quy chuỗi thời gian**: $\hat y = 10 + t + 4\,Q3$; quý 7 (quý 3) = 10 + 7 + 4 = 21.
- **Hồi quy giả**: $a$ = 1, 2, 4, 5; $b$ = 3, 5, 6, 8 cùng tăng → tương quan mức cao; sai phân 1, 2, 1 và 2, 1, 2 → −1.
- **Hồi quy động**: $y = 4x + \eta$, $\eta$ = 0,5 × 2 → dự báo 4 × 3 + 1 = 13 thay vì 12.
- **Nhiều mùa vụ / Fourier**: chu kỳ 168 giờ, $K$ = 3 → 6 cột thay 167 biến giả.
- **Biến can thiệp**: đối thủ mở từ tháng 4 → bậc 0, 0, 0, 1, 1…
- **Prophet**: xu hướng 5 + mùa vụ −0,5 + lễ −1 = 3,5; không khai lễ thì $h$ = 0.

### C. Quiz mù

1 A · 2 B · 3 B · 4 B · 5 142; 131,5 · 6 $a'$ = 1, 2, 1, 2, 1, $b'$ = 2, 1, 2, 1, 2, tương quan −1 → hồi quy giả · 7 26; 33,6 · 8 xung
(0, 0, 1, 0…), bậc từ tháng 6; −40 mỗi tháng từ tháng 6 · 9 Ljung–Box ≈ 0 → hồi quy giả, làm lại hồi quy động · 10 DM p 0,76 → chưa thắng
seasonal naive; chỉ thắng Prophet. Căn cứ: 1, 6, 9 → 4.2; 2, 3, 7 → 4.3; 4 → 4.5–4.6; 5 → 4.1; 8 → 4.5; 10 → 4.4. Tất cả "chắc".

### D. Tổng kết

Chặn 1 / khó 2 / nhỏ 5. Sửa một điều: Lab bước 2 (#1).

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10** (đáp án của ta kiểm bằng Python, đúng hết). Sửa #1: Lab bước 2 đưa ba dòng `SARIMAX` + `resid[13:]` và câu "Ljung–Box tính
trên `e`"; #2 "ngoài phần xu hướng đó, quý 3 cao hơn quý 1 6 đơn vị"; #3 dùng thành phần 3 chữ số thật (2,444 − 0,018 − 0,066 − 0,726 =
1,634); #4 "hệ số chặn (số 20, đi với một cột hằng bằng 1)", tách câu dài; #5 ghi rõ "đo thật 2.235, dự báo 2.082"; #6 "ETS (làm trơn hàm
mũ, buổi 16)". Giữ #7, #8 (tên gọi, không cản hiểu).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 21 đọc mù | 4.113 | 13 | 1 | 2 | 5 | 10/10 | 0 |
| sau sửa, đọc lại | 4.163 | 13 | **0** | **0** | 2 | 10/10 | 0 |
