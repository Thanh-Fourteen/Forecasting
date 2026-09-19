# Nhật ký research — Buổi 20: Đa biến, state space và nowcasting

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-19 (Phase 20). Buổi soạn mới hoàn toàn (thư mục tạo từ khuôn).
- **Người/phiên:** Phase 20, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Philadelphia Fed, Real-Time Data Set for Macroeconomists — trang ROUTPUT: "Quarterly vintages 1965:Q4 to present" (`ROUTPUTQvQd.xlsx`), **"Monthly vintages 1965:M11 to present" (`routputMvQd.xlsx`)**, first/second/third release; "All data are updated at the end of each month": https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/routput | dữ liệu, tài liệu chính thức | 2026-09-19 | 4.5–4.6 |
| 2 | Croushore & Stark (2001), "A real-time data set for macroeconomists", *J. Econometrics* 105 | bài gốc | 2026-09-19 | 4.6 |
| 3 | statsmodels 0.15.0 `DynamicFactorMQ`: nhân tố động tần suất hỗn hợp tháng/quý, EM, ragged edge, `news()`: https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.dynamic_factor_mq.DynamicFactorMQ.html | tài liệu chính thức | 2026-09-19 | 4.4 |
| 4 | Bank of England Macro Technical Paper No. 2 (6/2025), "Nowcasting GDP at the Bank of England: a staggered-combination MIDAS approach"; NY Fed Staff Report 1152 (component-based DFM nowcast) — tổng quan mới: bridge, MIDAS, DFM đều đang dùng; không cách nào thắng mọi giai đoạn | tổng quan, thực hành ngân hàng TW | 2026-09-19 | 4.4–4.5, "Nâng cao" MIDAS |
| 5 | FPP3 §12.3 (VAR: mỗi biến theo trễ của mọi biến; chọn p bằng AICc) và statsmodels `VAR`, `VECM`, `select_coint_rank` (Johansen), `coint` (Engle–Granger) | sách + tài liệu | 2026-09-19 | 4.1–4.2 |
| 6 | Durbin & Koopman (2012), *Time Series Analysis by State Space Methods* — local level, Kalman, dữ liệu thiếu; ví dụ sông Nile (dữ liệu public domain, có sẵn `statsmodels.datasets.nile`) | sách | 2026-09-19 | 4.3 |
| 7 | Điều khoản dữ liệu: FRED/ALFRED cấm dùng "in connection with the development or training of any … machine learning" → không dùng (CLAUDE.md quy tắc 6); dùng RTDSM của Philadelphia Fed ("informational, educational, and research purposes only"), không mirror | điều khoản | 2026-09-17 (danh mục) | dữ liệu |

## Phiên bản đã xác minh

statsmodels 0.15.0 (DynamicFactorMQ, VECM), openpyxl 3.1.5, **xlrd 2.0.2** (thêm vào `tools/nen/phien-ban.toml` để đọc .xls của EIA), pandas
2.3.3 — theo `uv.lock` của buổi.

## Dữ liệu (thêm vào danh mục 2026-09-19)

| Bộ | sha256 rút gọn | Giấy phép | Ghi chú |
|---|---|---|---|
| `philly-fed-gdp-thuc-vintage-thang` | `7d8c6ab78964` | Philadelphia Fed: giáo dục/nghiên cứu, không mirror | 722 vintage tới 25M12 sau khi cắt |
| `philly-fed-viec-lam-vintage` (EMPLOY) | `ae954f940b62` | như trên | tháng |
| `philly-fed-san-luong-cn-vintage` (IPT) | `b4a6324162c8` | như trên | tháng |
| `philly-fed-nha-khoi-cong-vintage` (HSTARTS) | `2c7527def217` | như trên | tháng (có trong code, bridge không dùng) |
| `eia-gia-dau-wti` | (đã có) | public domain | |
| `eia-gia-xang-ny-harbor` | `1305a8b32807` | public domain | chưa mirror |

**Cơ chế mới `noi_them`** (`tools/lay_du_lieu.py`): các tệp này bị nguồn ghi đè bằng bản **nối thêm** (Philadelphia Fed thêm một cột vintage
mỗi tháng, EIA thêm ngày) và không mirror được (Philadelphia Fed) hoặc chưa mirror (EIA xăng) → sha256 sẽ lệch. Khi lệch: cảnh báo và nhận tệp;
buổi cắt tới mốc cố định (vintage 25M12, ngày 2019-12-31) và bộ chấm kiểm sha256 của phần đã cắt (`test_du_lieu_vintage_cat_dung_moc`).

Vintage "yyMm" = số liệu có vào **giữa** tháng đó: 26M8 đã có GDP 2026Q2 (công bố 30/7), 26M7 chưa. Với quý q: vintage tháng đầu quý có 0 tháng
chỉ báo của quý, tháng 2 có 1, tháng 3 có 2, tháng đầu quý sau có đủ 3; GDP lần đầu xuất hiện ở tháng thứ 2 của quý sau.

## Số liệu thật (`dap-an/ve_hinh.py`)

| Đại lượng | Giá trị |
|---|---|
| Log giá tuần 2010–2019 (522 tuần), USD/gallon | ADF p mức 0,518 (dầu), 0,482 (xăng); sai phân < 0,001; KPSS mức 0,01 |
| Engle–Granger xang ~ dau | hệ số 0,845, hằng số 0,311, p 9,4·10⁻⁵; spread: độ lệch chuẩn 0,074, bán rã 9,6 tuần; Johansen hạng 1 |
| Backtest 104 cutoff (2018–2019), MAE % trên log theo h = 1..4 | naive 2,89 / 4,68 / 5,88 / 6,78; VAR sai phân 2,75 / 4,62 / 5,93 / 6,75; VECM 2,74 / 4,53 / 5,70 / 6,44. DM (h = 4) so naive: VAR p 0,66; VECM p 0,17 |
| Nile, local level (statsmodels) | σ² nhiễu 15.078, σ² mức 1.479; Kalman tự viết lệch tối đa 0,024 (p0 = 10⁶, như "approximate diffuse"); mức 1871–73: 1.103,4 / 1.132,8 / 1.068,0 |
| Nile bỏ 1911–1930 | độ lệch chuẩn của mức 63,6 (1910) → 183,3 (1930) |
| GDP 2008Q4 qua các vintage | lần đầu −3,88%, thấp nhất −9,31% (2011–2013), bản 12/2025 −8,85% |
| 60 quý 2005–2019 | RMS chênh lần đầu − bản 12/2025: 1,50 điểm %; lớn nhất 4,97 |
| Nowcast RMSE (điểm %, năm hoá) k = 1..4, 2005–2019 | bridge (việc làm + sản lượng CN) 1,44 / 1,32 / 1,19 / 1,17; DFM 1 nhân tố 1,86 / 1,60 / 1,49 / 1,50; naive 2,72 / 1,84 / 1,93 / 2,03; trung bình lịch sử 1,94 / 1,93 / 1,92 / 1,92 |
| Tách 2005–2009 | bridge 1,98 / 1,69 / 1,37 / 1,27; trung bình 3,03 → 3,00 |
| Tách 2010–2019 | bridge 1,07 / 1,10 / 1,09 / 1,12; trung bình **1,03** (thắng); DFM 1,28 / 1,16 / 1,20 / 1,23 |
| Rò rỉ: bridge dùng vintage 25M12 ở tháng 1 | RMSE 1,19 (thật: 1,44) — giả vờ biết cả quý ngay từ tháng đầu |
| Thời gian | đọc 4 tệp xlsx lần đầu ~13 s (lưu parquet); đánh giá bridge 60 quý × 4 ~3 s; DFM 240 lần khớp ~40 s |

## Phát hiện mới / lỗi hiểu sai phổ biến

- **Nowcast chỉ đáng khi kinh tế đổi chiều**: 2010–2019 trung bình lịch sử thắng mọi mô hình; lợi ích nằm ở 2005–2009. Báo trung thực trong 4.5.
- DFM 1 nhân tố thua bridge 2 chỉ báo trên bộ nhỏ này — DFM của các ngân hàng trung ương dùng hàng chục chuỗi (NY Fed Staff Report 1152); không dựng lại được ở đây
  vì chỉ có vài chuỗi tháng có vintage.
- 2021Q3–2022Q2: việc làm hồi phục mạnh trong khi GDP âm (tồn kho, thương mại) → bridge sai 3–6 điểm % (thử nghiệm 2010–2024); buổi đánh giá
  2005–2019 và nói rõ lý do.
- Dữ liệu 2010–2019 cần cho cointegration: trên 2000–2024 ADF bác "không dừng" (các cú sập 2008, 2020 làm chuỗi trông như dừng), Johansen cho
  hạng 2 — không minh hoạ được; chọn 2010–2019 và ghi lý do.
- Kiểm rò rỉ bằng cách nhân các vintage sau với **một hằng số** không bắt được lỗi (tăng trưởng log bất biến với phép nhân) → dùng nhiễu ngẫu
  nhiên theo ô.

## Research viết lại (sư phạm)

- VAR: "mỗi biến nhớ quá khứ của mọi biến"; bùng nổ tham số: 10 biến × 4 trễ = 400 hệ số.
- Cointegration: "người dắt chó" — hai chuỗi đi lang thang nhưng dây xích giữ chúng không xa nhau.
- Kalman: "trộn dự đoán với số đo theo độ tin cậy của từng bên".
- Nowcast: "dự báo hiện tại" vì số chính thức về trễ; ragged edge = mỗi chuỗi dừng ở một tháng khác nhau.
- Vintage: "số đã sửa là số của tương lai".

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lab 3 "DFM 3 nhân tố từ vài chục chuỗi BEA/BLS/Fed Board" | nhỏ | chỉ báo tháng lấy từ RTDSM (có vintage thật) → 3 chuỗi, DFM 1 nhân tố; nói rõ DFM cần nhiều chuỗi. Dùng BEA/BLS bản đã sửa sẽ là rò rỉ |
| Chỉ báo tháng dùng bản đã sửa (lộ trình để ngỏ) | nhỏ | dùng vintage cho **cả** GDP và chỉ báo |
| MIDAS | nhỏ | hộp "Nâng cao" (≤ 6 khái niệm) |
| IRF, phân rã phương sai, UCM, local linear trend | nhỏ | IRF trong hộp "Nâng cao" mục 4.1; local linear trend nhắc ở 4.3 |
| Chỗ hở | nhỏ | `hang_dong_lien_ket` trả 0 (không kiểm) → VAR sai phân; `nowcast` dùng vintage 25M12 (số đã sửa). Bảng `quy-uoc.md` giữ nguyên ý |

## Đọc thử (Phase 20, 2026-09-19)

Tự đọc (không subagent), checklist `tools/CHUAN-DE-HIEU.md`. Tính lại: VAR(1) 6 / 4 và 3,8 / 3,0; 5² × 3 = 75; spread 0,3 → −0,06 và −0,2 → +0,05;
Kalman 5 → K 0,5 → 105, 2,5 → 3,5 và tự kiểm tra 52,5 / 3; DFM 0,75 / 0,4 / 1,0 và 0,5 / 0,6; nowcast (0,2 + 0,1 + 0,1) × 4 = 1,6 → 3,4 và 4,5;
mọi số bảng 4.2, 4.5, 4.6 lấy từ `ve_hinh.py`; quiz 5 (32), 6 (23; 2; 3), 7 (0,3; −0,03), 8 (3,68), 10 (5%).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 3.901 | 12 | 0 | 1 | 3 | 10/10 | khó: hình Kalman vẽ cả số đo đã "xoá" (chấm xám vẫn hiện trong vùng vàng), mâu thuẫn chú thích. Nhỏ: ví dụ nowcast cộng tăng trưởng tháng ×4 là xấp xỉ (ghi "khoảng"); VECM ví dụ tay dùng mức, dữ liệu thật dùng log; DM p của VAR không in trong bảng |
| 2 | 3.901 | 12 | **0** | **0** | 3 | 10/10 | vẽ lại hình Kalman bằng chuỗi đã xoá |
| rà gọn | biên tập viên | — | — | — | — | — | 1 chỗ thừa nhỏ (mục 3 giải thích sha256 lệch, lặp với "Lỗi thường gặp"), giữ vì học viên gặp ngay khi `up` |

Căn cứ quiz: 1, 2, 7, 10 → 4.2; 3, 6 → 4.3; 4, 9 → 4.6; 5 → 4.1; 8 → 4.5. `kiem_de_hieu.py 20` 0; `kiem_tra_lab.py 20` đạt.

## Đọc thử độc lập (Phase 21, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: VAR 6 / 4 → 3,8 / 3,0; số hệ số 8, 400, 75; VECM
−0,06 và tự kiểm tra +0,05; Kalman 105 / 2,5 / 3,5 và 52,5 / 3; DFM 1,0 và 0,6; nowcast 3,4 và 4,5; quiz 5 (32), 6 (23 / 2 → 23 / 3), 7 (0,3 /
−0,03), 8 (3,68), 10 (chênh 5,0%). Khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.5 | "(0,2 + 0,1 + 0,1) × 4 = 1,6% năm hoá" | 1, 4 | "năm hoá" chưa định nghĩa, không nói vì sao × 4; ký hiệu $\bar x$ lại nói "tăng trưởng **trung bình** quý" trong khi ví dụ cộng ba tháng | khó |
| 2 | Lab bước 1 | "kiểm định Johansen (`select_coint_rank` của statsmodels)" | 4 | không nói tham số, không nói lấy `.rank` | khó |
| 3 | 4.5 | "RMSE (điểm %)" | 1 | "điểm %" chưa định nghĩa | nhỏ |
| 4 | 4.2 | "hạng 0 là không có" | 1 | "hạng" chỉ hiểu qua ngữ cảnh | nhỏ |
| 5 | 6 | "như \"approximate diffuse\"" | 6 | tiếng Anh không dịch | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **VAR**: $x$ = 0,4$x$ + 0,1$y$; $x$ = 5, $y$ = 10 → 3; 3 biến 2 trễ → 18 hệ số.
- **Cointegration / VECM**: cân bằng $y$ = 1 + $x$; $x$ = 3, $y$ = 3,5 → spread −0,5; $\alpha$ −0,4 → +0,2.
- **Kalman**: $a$ = 10, $P$ = 1, cú dời 1, nhiễu 2, đo 16 → $K$ 0,5, mức 13, $P$ 1.
- **DFM**: hệ số sản lượng 0,5, sản lượng 1,0 → $f$ = 2; GDP hệ số 1 → 2.
- **Nowcast**: bridge 0,5 + 1 × x; ba tháng 0,1 → 0,3 × 4 = 1,2 → 1,7.
- **Vintage**: lần đầu −3,88, bản sau −8,85: chấm theo bản sau là dùng tương lai.

### C. Quiz mù

1 B · 2 B · 3 A · 4 B · 5 32; mỗi phương trình 8 hệ số trên ~58 quý — tôi kết luận "đáng lo" · 6 23 / 2; 23 / 3 · 7 spread 0,3, kéo về −0,03
· 8 3,68 · 9 sai số phẳng → đọc vintage mới nhất (rò rỉ), thật 1,44 → 1,17 · 10 DM p 0,17 → chưa có bằng chứng. Căn cứ: 1, 2, 7, 10 → 4.2;
3, 6 → 4.3; 4, 9 → 4.6; 5 → 4.1; 8 → 4.5.

### D. Tổng kết

Chặn 0 / khó 2 / nhỏ 3.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 9/10**: câu 5 đáp án nói "còn chấp nhận được", nhưng tài liệu không có mốc nào để phán "đáng lo" — câu hỏi không có căn cứ. Đổi câu 5
thành tính số hệ số mỗi phương trình với 4 và 8 biến (32 / 8; 128 / 16), đáp án nói vì sao VAR lớn dễ học thuộc nhiễu (mục 4.1). Sửa #1:
"tăng khoảng 0,4% so với quý trước; **năm hoá** (nhân 4: tốc độ nếu cả năm tăng như quý này) là 1,6%", ký hiệu $\bar x$ thành "tăng trưởng quý
… năm hoá"; #2 Lab đưa dòng `select_coint_rank(L, det_order=0, k_ar_diff=k_ar_diff).rank`; #3 câu định nghĩa điểm % (2,0% so với 3,0% → 1
điểm). Giữ #4 (Lab nói "hạng 1"), #5 (tên tuỳ chọn thư viện).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 21 đọc mù | 3.901 | 12 | 0 | 2 | 3 | 9/10 | 0 |
| sau sửa, đọc lại | 3.933 | 12 | **0** | **0** | 2 | 10/10 (câu 5 mới) | 0 |
