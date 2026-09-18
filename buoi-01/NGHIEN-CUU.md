# Nhật ký research — Buổi 1: Forecasting là gì

- **Ngày research:** 2026-09-17
- **Nền buổi:** Python 3.12.3; numpy 2.5.3, pandas 3.0.5, matplotlib 3.11.2
- **[CHẠY]** = đã chạy trong nền buổi; mọi con số của tài liệu lấy từ các lần chạy này (không có ngẫu nhiên — không cần seed)

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Hyndman, Athanasopoulos et al., *Forecasting: Principles and Practice, the Pythonic Way*, ch. 1, https://otexts.com/fpppy/01-intro.html | sách mở | 2026-09-17 | khả năng dự báo, dự báo/mục tiêu/kế hoạch, các bước |
| 2 | FPP Pythonic ch. 5, https://otexts.com/fpppy/05-toolbox.html (§5.2, §5.3, §5.8, §5.9) | sách mở | 2026-09-17 | baseline, phần dư vs sai số dự báo |
| 3 | Makridakis et al. (1982), J. Forecasting 1(2):111–153, doi:10.1002/for.3980010202 | bài báo | 2026-09-17 | M1 |
| 4 | Makridakis, Chatfield, Hibon et al. (1993), IJF 9(1):5–22 | bài báo | 2026-09-17 | M2 |
| 5 | Makridakis & Hibon (2000), IJF 16(4):451–476, doi:10.1016/S0169-2070(00)00057-1; bốn kết luận qua Hyndman, https://robjhyndman.com/hyndsight/forecasting-competitions/ | bài báo + blog | 2026-09-17 | M3 |
| 6 | Makridakis, Spiliotis & Assimakopoulos (2018), IJF 34(4):802–808, doi:10.1016/j.ijforecast.2018.06.001 (abstract); bản đầy đủ (2020) IJF 36(1):54–74 | bài báo | 2026-09-17 | M4 |
| 7 | Makridakis, Spiliotis & Assimakopoulos (2022), IJF 38(4):1346–1364, doi:10.1016/j.ijforecast.2021.11.013 (preprint tác giả) | bài báo | 2026-09-17 | M5 Accuracy |
| 8 | Makridakis et al. (2022), M5 Uncertainty, doi:10.1016/j.ijforecast.2021.10.009 (abstract) | bài báo | 2026-09-17 | 9 quantile |
| 9 | Makridakis, Spiliotis, Hollyman, Petropoulos, Swanson & Gaba (2025), IJF 41(4):1315–1354, doi:10.1016/j.ijforecast.2024.11.002, arXiv:2310.13357 | bài báo | 2026-09-17 | M6 |
| 10 | Petropoulos et al. (2022), "Forecasting: theory and practice", IJF 38(3):705–871, arXiv:2012.03854 | tổng quan | 2026-09-17 | benchmark |
| 11 | Makridakis, Spiliotis & Assimakopoulos (2018), PLoS ONE 13(3):e0194889 | bài báo | 2026-09-17 | ML vs thống kê trên M3 |
| 12 | Gneiting (2011), JASA 106(494):746–762, arXiv:0912.0902 | bài báo | 2026-09-17 | hàm chấm điểm phải khớp nhiệm vụ |
| 13 | de Treville, "The Newsvendor Model" (slide bài giảng HEC Lausanne), https://oplab.ch/content/slides2.pdf | slide | 2026-09-17 | critical fractile |
| 14 | UCI dataset 235 (JSON API `https://archive.ics.uci.edu/api/dataset?id=235`), doi:10.24432/C58K54 | mô tả dữ liệu | 2026-09-17 | biến, dữ liệu thiếu |

## Trích dẫn nguyên văn đã xác minh

**FPP §1.1:** "The predictability of an event or a quantity depends on several factors including: how well we understand the
factors that contribute to it; how much data is available; how similar the future is to the past; whether the forecasts can
affect the thing we are trying to forecast." — **bốn** yếu tố (lộ trình liệt kê ba). "Short-term forecasts of residential
electricity demand can be highly accurate because all four conditions are usually satisfied." Tỷ giá: "only one of the
conditions is satisfied: there is plenty of available data."

**FPP §1.2:** "business forecasting is often done poorly, and is frequently confused with planning and goals." Forecasting
"is about predicting the future as accurately as possible, given all the information available…"; Goals "are what you would
like to have happened"; Planning "is a response to forecasts and goals. Planning involves determining the appropriate actions
that are required to make your forecasts match your goals."

**FPP §1.6:** Problem definition — "Often this is the most difficult part of forecasting." "The performance of the model can
only be properly evaluated after the data for the forecast period have become available."

**FPP §1.7:** "a 95% prediction interval contains a range of values which should include the actual future value with
probability 95%." "When we talk about the "forecast", we usually mean the average value of the forecast distribution".

**FPP §5.2:** "Some forecasting methods are extremely simple and surprisingly effective." "in many cases, these methods will
serve as benchmarks rather than the method of choice."

**FPP §5.8** (không phải §5.3 như đề bài gợi ý): "the size of the residuals is not a reliable indication of how large true
forecast errors are likely to be. The accuracy of forecasts can only be determined by considering how well a model performs on
new data that were not used when fitting the model." "A model which fits the training data well will not necessarily forecast
well. A perfect fit can always be obtained by using a model with enough parameters." "residuals are calculated on the training
set while forecast errors are calculated on the test set. Second, residuals are based on one-step forecasts while forecast
errors can involve multi-step forecasts."

**M1 và M3** (qua Hyndman 2018, https://robjhyndman.com/hyndsight/forecasting-competitions/ — chưa mở được PDF gốc, xác minh
thứ cấp). Kiểm lại 2026-09-17: Hyndman gán bốn kết luận cho **M-competition 1982 (M1)**, "taken from Makridakis & Hibon, 2000",
và viết "Makridakis & Hibon (2000) claimed that the M3 competition supported the findings of their earlier work." M1: "1001
series" dài "between 9 and 132 observations". Bài openforecast.org (2024-03-14) cũng gán câu thứ nhất cho M1. Bốn kết luận: "Statistically sophisticated or complex methods do not
necessarily provide more accurate forecasts than simpler ones." / "The relative ranking of the performance of the various
methods varies according to the accuracy measure being used." / "The accuracy when various methods are being combined
outperforms, on average, the individual methods being combined…" / "The accuracy of the various methods depends upon the length
of the forecasting horizon involved."

**M4** (abstract 2018): "Out Of the 17 most accurate methods, 12 were "combinations" of mostly statistical approaches." "The
biggest surprise was a "hybrid" approach that utilized both statistical and ML features. This method's average sMAPE was close
to 10% more accurate than the combination benchmark" "The six pure ML methods performed poorly, with none of them being more
accurate than the combination benchmark and only one being more accurate than Naïve2."

**M5 Accuracy** (preprint): "M5 is, therefore, the first competition where all top-performing methods were both "pure" ML ones
and significantly better than all statistical benchmarks and their combinations." "most of the methods examined utilized
LightGBM" "all top 50 performing methods in M5 utilized "cross-learning"". M5 Uncertainty: 9 quantile 0,005 … 0,995.

**M6** (arXiv v1): "from the 163 teams included in the global leaderboard, 38 (23.3%) managed to provide more accurate forecasts
than the benchmark, 47 (28.8%) to construct better portfolios, and 11 (6.7%) to achieve both higher IR and RPS scores." "no
connection is identified between the two variables (r = 0.04)". Xuất bản IJF 41(4) **2025** (DOI chứa "2024").

**Petropoulos et al. (2022) §2.12.1:** "New methods should always be compared to a larger number of suitable benchmark methods.
These should at a minimum include naïve methods such as a random walk…"

**Gneiting (2011):** "Effective point forecasting requires that the scoring function be specified a priori, or that the
forecaster receives a directive in the form of a statistical functional, such as the mean or a quantile of the predictive
distribution." Pinball "is strictly consistent for the α-quantile".

**Newsvendor (slide):** "We solve for F(Q*) = Cu/(Cu+Co), so Q* = F⁻¹(Cu/(Cu+Co))" — "critical fractile". Chỉ có slide, chưa
tìm được giáo trình trích nguyên văn → tài liệu trình bày như kết quả chuẩn, dẫn Gneiting (2011) cho phần lý thuyết.

**UCI 235:** "2075259 measurements gathered in a house located in Sceaux (7km of Paris, France) between December 2006 and
November 2010 (47 months)." "nearly 1,25% of the rows" thiếu; "global_active_power: household global minute-averaged active
power (in kilowatt)".

**M2** — chỉ xác minh thứ cấp: tóm tắt kết quả tìm kiếm (trỏ tới ScienceDirect PII 016920709390044N, trang IIF
https://forecasters.org/resources/time-series-data/m2-competition/): 29 chuỗi (23 từ bốn công ty, 6 vĩ mô), 5 người dự báo,
dự báo tháng cho 15 tháng; điều chỉnh bằng phán đoán không cải thiện so với phương pháp thống kê thuần. Abstract gốc trả 403,
RePEc không có abstract → tài liệu ghi rõ "tóm tắt thứ cấp".

**CHƯA XÁC MINH (không đưa vào tài liệu như sự thật):** M7 (không có thông báo chính thức); số issue M1; DOI M2; Kolassa (2020)
không có trích dẫn nguyên văn; bài Foresight về "dự báo bị biến thành chỉ tiêu".

## Số liệu thật của buổi [CHẠY]

- **Dữ liệu:** `household_power_consumption.txt` 132.960.755 B, 2.075.260 dòng (kể cả tiêu đề), sha256 `4259c9d7ece5…`
  (zip gốc `9f84b46ade8a…`). Đọc bằng pandas 3.0.5 ~0,9 s. Mốc thời gian 2006-12-16 17:24 → 2010-11-26 21:02, không trùng.
  Thiếu `Global_active_power` 1,2518% số phút.
- **Chuỗi giờ** (trung bình kW trong giờ = kWh/giờ; NaN nếu < 30 phút đo được), 2006-12-17 00:00 → 2010-11-21 23:00: 34.464
  giờ, thiếu 431 (1,25%), trung bình 1,091. Trung bình theo năm: 2007 1,117; 2008 1,072; 2009 1,079; 2010 1,059. Theo tháng:
  tháng 12 1,486, tháng 1 1,462, tháng 8 **0,573**, tháng 7 0,700. Theo giờ: 04h 0,44 thấp nhất, 20h 1,90 cao nhất; cuối tuần
  (thứ Bảy 1,246, CN 1,22) cao hơn ngày thường (0,98–1,08). Giờ cao nhất 2008-11-23 18:00 6,56. Tháng 8/2008 từ ngày 6 đến 30
  mỗi ngày 4,2–6,2 kWh (vắng nhà). Chuỗi ngày: trung bình 26,17 kWh, 4,17–79,56. Trung bình ngày tháng 8: 2007 18,3; 2008 6,6; 2009 15,8; 2010 14,1; tháng 1–2/2007 35,5; tháng 6/2007 19,8.
- **Ngày không có giờ nào đủ 30 phút đo:** 28–29/4/2007, 14/6/2009, 13/1/2010, 18–21/8/2010, 26–27/9/2010 (10 ngày).
- **Đánh giá cuốn** — gốc mỗi thứ Hai từ 2010-01-04 tới 2010-11-15 (46 gốc), tầm 168 giờ, chấm 7.435 giờ có số đo (293 giờ
  NaN bỏ qua). MAE (kWh/giờ): TB 4 tuần **0,4905**; bảng lịch (tuần ISO × thứ × giờ, chỉ dữ liệu trước gốc) **0,5075**; tuần
  trước 0,5763; trung bình 0,6519; giờ trước 0,7702.
- **Sai số ảo:** bảng lịch khớp trên toàn bộ dữ liệu (gồm cả 2010) rồi chấm 2010: **0,3799**; trong mẫu trên toàn bộ: 0,4109;
  bảng khớp ≤ 2009 chấm trong mẫu ≤ 2009: 0,3998. Bảng có 8.904 ô; trung bình 2,99 giờ/ô với dữ liệu trước 2010, 3,82 giờ/ô với
  toàn bộ → khi khớp cả 2010, khoảng 1/4 số liệu mỗi ô là chính giờ đang chấm. TB 4 tuần thắng bảng lịch 30/46 tuần.
- **Tổng tuần** (41 tuần đủ số đo): MAE bảng lịch **16,4** kWh/tuần; tuần trước 24,2; TB 4 tuần 27,9 — thứ hạng đảo so với theo
  giờ. Ba tuần cuối (gốc 01/11, 08/11, 15/11): thực tế 194,0 / 224,4 / 186,0; TB 4 tuần 194,5 / 193,5 / 203,5; tuần trước
  161,1 / 194,0 / 224,4; bảng lịch 138,0 / 218,1 / 236,7.
- **Tuần minh hoạ** (tuần chênh lớn nhất giữa bảng lịch "ảo" và trung thực): gốc 2010-10-25; MAE ảo 0,56, trung thực 0,75, TB 4
  tuần 0,66.
- **Chi phí bất đối xứng** (thiếu 4 : thừa 1 mỗi kWh): quantile 0,8 sai số của TB 4 tuần trên 2009 (gốc 2009-01-05 →, 8.665 giờ)
  = +0,4551 kWh (trung vị −0,042). Năm 2010: TB 4 tuần → chi phí 1,2132/giờ, MAE 0,4905, tỷ lệ giờ dự báo thiếu 44,0%;
  TB 4 tuần + 0,4551 → chi phí **0,9871** (−18,6%), MAE 0,6731, tỷ lệ thiếu 20,1%; quantile theo từng giờ trong ngày → chi phí
  0,9598. Quét cộng thêm 0 … 1: đáy khoảng 0,45–0,5.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình: "Cái gì dự báo được… 3 yếu tố" — FPP nêu **4** (thêm "tương lai giống quá khứ tới đâu") | nhỏ | Dạy đủ 4 |
| Lab bước 5 "đánh giá trên chính dữ liệu" — cần một mô hình có thể "thuộc lòng" dữ liệu; hồi quy Fourier theo ngày chỉ cho chênh nhỏ (trong mẫu 4,02 vs trung thực 5,08 kWh/ngày) | nhỏ | Dùng chuỗi **giờ** và "bảng lịch" 8.904 ô: chênh 0,380 → 0,508 và đảo thứ hạng với baseline |
| Thêm phát hiện: ở tổng tuần bảng lịch thắng baseline | bổ sung | Đưa vào như bài học "độ chi tiết của quyết định quyết định cách chấm" — nối với ô "độ chi tiết" của phiếu |
| Lab bước 4 "đoán bằng mắt" không kiểm được tự động | thiết kế | Ghi vào phiếu trên giấy; tài liệu đưa số thật của 3 tuần cuối để học viên đối chiếu |
| M7 chưa có nguồn chính thức | nhỏ | Không nhắc M7 |
| Bốn kết luận "đơn giản không thua phức tạp…" là của M1 (M3 xác nhận), không phải phát hiện mới của M3 | nhỏ | Bảng M1–M6 ghi đúng: M1 đưa ra, M3 ủng hộ |

## Research viết lại (Phase 6, 2026-09-18)

Mục đích: viết lại phần chữ theo chuẩn dễ hiểu D1–D12. Nguồn sư phạm chung (worked example, cognitive load, newsvendor,
bảng hiểu lầm theo buổi) dùng lại từ `tools/NGHIEN-CUU-SU-PHAM.md`. Nguồn mới theo từng khái niệm:

| Khái niệm (mục) | Nguồn (truy cập 2026-09-18) | Cách giải thích lấy vào | Hiểu lầm phổ biến → cách phòng |
|---|---|---|---|
| Dự báo / mục tiêu / kế hoạch (4.1) | FPP3 §1.2 https://otexts.com/fpp3/planning.html | ba định nghĩa: dự báo = "dự đoán tương lai chính xác nhất với mọi thông tin đang có"; mục tiêu = điều muốn xảy ra; kế hoạch = hành động để dự báo khớp mục tiêu | sửa dự báo cho khớp mục tiêu → ví dụ số 2.500 − 1.900 = 600 ly thừa |
| Baseline, ký hiệu $T$, $h$, $\hat y_{T+h}$ (4.3) | FPP3 §5.2 https://otexts.com/fpp3/simple-methods.html | ký hiệu $\hat y_{T+h\vert T}$, $\bar y$, $y_{T+h-m(k+1)}$; "mọi phương pháp mới được so với các phương pháp đơn giản này" | phức tạp mặc nhiên hơn đơn giản (Hewamalage et al. 2023, https://arxiv.org/abs/2203.10716) → luôn đặt baseline cạnh mô hình; baseline dùng số chưa có tại gốc → phép tính $T+100-24 = T+76 > T$ |
| MAE (4.3) | FPP3 §5.8 https://otexts.com/fpp3/accuracy.html | MAE dễ hiểu, cùng đơn vị; "phương pháp làm MAE nhỏ nhất cho dự báo trung vị" | dùng câu này để giải thích "MAE nhắm trung vị" bằng trường hợp thiếu = thừa = 1 của 4.6 |
| Phần dư vs sai số dự báo, dự báo cuốn (4.4) | FPP3 §5.8 (như trên); FPP3 §5.10 https://otexts.com/fpp3/tscv.html | phần dư tính trên dữ liệu huấn luyện, sai số dự báo trên dữ liệu chưa dùng; "gốc dự báo cuộn tới theo thời gian", không dùng quan sát tương lai | phần dư nhỏ = dự báo tốt; hình dự báo đè thực tế "trông khớp" là bằng chứng (Hewamalage 2023) → ví dụ tay ô bảng lịch 1,2 vs 1,4 |
| Độ chi tiết (4.5) | Athanasopoulos, Hyndman, Kourentzes, Petropoulos (2017), *Forecasting with temporal hierarchies*, https://robjhyndman.com/papers/temporalhierarchies.pdf (đọc tóm tắt qua kết quả tìm kiếm) | đặc tính chuỗi đổi theo mức gộp nên phương pháp tốt nhất đổi theo, dẫn tới quyết định khác | "MAE giờ nhỏ thì tổng tuần cũng chính xác" → ví dụ tay +1/−1 triệt tiêu |
| Chi phí lệch, quantile (4.6) | giữ bài mẫu Phase 5 (nguồn đã ghi ở `tools/NGHIEN-CUU-SU-PHAM.md`) | — | — |

**Quyết định cấu trúc (≤ 6 khái niệm chính):**

- 4.1 = cũ 4.1 + 4.2 (dự báo là gì + cái gì dự báo được): cùng trả lời "con số này là gì, kỳ vọng tới đâu".
- 4.2 = cũ 4.3 (phiếu 6 ô) + cũ 4.4 (nhìn dữ liệu): nhìn dữ liệu là để trả lời ô 2 (đơn vị kW→kWh) và ô 5 (giờ trống);
  bảng 34 con số của bản cũ bỏ, giữ hình + "Cách đọc hình" + năm câu hỏi.
- 4.3 = baseline + ký hiệu thời gian + MAE (MAE chuyển từ mục 2 sang đây vì cần ví dụ số và ký hiệu $n$, $\sum$).
- 4.4 = sai số ảo + dự báo cuốn; 4.5 = độ chi tiết; 4.6 = cũ 4.8 (bài mẫu Phase 5, chỉ đổi số mục tham chiếu và
  thêm 3 câu giải thích "MAE nhắm trung vị").
- Cũ 4.9 (M1–M6) và 4.10 (bản đồ cách tiếp cận) → mục 9 "Đọc thêm", viết lại bằng tiếng Việt, bỏ trích nguyên văn.
- Bỏ khỏi Mục tiêu: "kể được bài học M1–M6" (không còn là khái niệm chính).
- Quiz câu 4 cũ (M1–M6) thay bằng câu đọc ký hiệu $T + h$; câu 9 sửa "1/4" thành 22%.

**Số mới [CHẠY]** — `dap-an/vi_du_nho.py` (không ngẫu nhiên):

- ví dụ tay: kW→kWh 1,2; MAE 0,5; bốn baseline cho $h = 44$ (0,6 / 1,1 / 1,8 / 1,5); $T+100$ = 03:00 thứ Sáu 8/1/2010,
  $T+76$ = 03:00 thứ Năm 7/1; ô nhìn trộm 1,2 → 1,4; cách A/B 1 vs 0,5 và 0 vs −2.
- dữ liệu thật: 46 gốc × 168 = 7.728 giờ, 293 giờ trống, 7.435 giờ chấm; 41 tuần đủ 168/168 giờ, 5 tuần thiếu;
  `resample("D").sum(min_count=20)` để trống 21 ngày; ô (tuần 43, thứ Hai, 19h) có giờ của 2007, 2008, 2009, 2010;
  (3,82 − 2,99)/3,82 = 0,217 (bản cũ ghi "khoảng 1/4", sửa thành 22%; riêng tuần 25/10/2010 đúng là 1/4).
- Lab bước 4: tổng tuần 8 tuần trước 15/11/2010 = NaN, NaN, 198,0, 184,3, 234,6, 161,1, 194,0, 224,4 kWh (hai tuần đầu
  thiếu 44 và 43 giờ).
- `dap-an/ve_hinh.py` chạy lại sau khi đổi nhãn "TB 4 tuần" → "trung bình 4 tuần" và thêm nhãn trục ngang: in
  q 0,4551; chi phí 1,2132/0,9871; mae_q 0,6731; thiếu 0,4399/0,2013 — khớp bản cũ.

**Đổi tên trong code/đáp án/bộ chấm:** cột và nhãn "TB 4 tuần" → "trung bình 4 tuần"; hàm `du_bao_tb_4_tuan` →
`du_bao_trung_binh_4_tuan` (code/, dap-an/, lab/cham/). Hành vi giữ nguyên: `kiem_tra_lab.py 1` dap-an 8/8 xanh, code
4 hỏng / 4 qua như trước.

**Độ dài:** `wc -w` 8.9 nghìn (vượt trần 7.000). Lý do: bài mẫu 4.6 giữ nguyên đã chiếm ~2.350; năm khái niệm còn lại
mỗi cái 500–1.100 theo khuôn D2. PDF 18 trang (trong 12–24). Chưa cắt thêm vì phần còn lại đều là chỗ chặn/khó của
baseline đọc thử.

## Đọc thử (Phase 6, 2026-09-18)

Subagent mới mỗi vòng, prompt nguyên văn ở `tools/CHUAN-DE-HIEU.md`, chỉ mở `tai-lieu.md` + `kiem-tra.md` đã bỏ đáp án.

| Vòng | Bản | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|
| 0 | bản cũ (trước Phase 5) | 9 | 21 | 30 | 10/10 | baseline — `tools/NGHIEN-CUU-SU-PHAM.md` |
| 1 | viết lại (Phase 6) | 0 | 6 | 21 | 10/10 | khó: 34.464 giờ không khớp 2.075.259 phút (thiếu giải thích cắt chuỗi); ô 1 "chiều Chủ nhật" mâu thuẫn ô 5 "23:59"; 10 vs 21 ngày trống; chữ $p$ dùng cho hai thứ; bước tổng quát $C_u/(C_u+C_o)$ bị nhảy; "chính là quantile 0,8" nói quá |
| 2 | sửa 6 chỗ trên | **0** | **5** | 20 | 10/10 | **đạt**. Không số nào sai. Sau vòng này sửa thêm 2 chỗ khó: định nghĩa $C_u$, $C_o$ trước khi dùng + chuyển vế từng bước; nói thẳng vì sao trung bình 4 tuần xuống cuối khi chấm tổng tuần (lệch cùng chiều kéo dài quanh tháng 8) |

`kiem_de_hieu.py 1`: 67 → 0 vi phạm. Độ dài 6.790 chữ ngoài bảng/code; PDF 19 trang.

## Rút gọn (Phase 7, 2026-09-18)

Người dùng: bản Phase 6 "dễ hiểu hơn nhưng dài dòng", "tường minh quá thành ra dài dòng và khó hiểu". Quy tắc D13.

| Bước | Kết quả |
|---|---|
| Biên tập viên lượt đầu | 32 chỗ thừa, ≈ 765 chữ (10,5%) — tài liệu đã khá chặt; phần lớn thừa là **lặp lập luận** (4.6 giải "vì sao 0,8" ba lần) và **chữ đọc lại hình/bảng** (4.5 giải tháng 8 ba lần) |
| Cắt | 6.910 → 5.473 chữ ngoài bảng/code; năm câu hỏi 4.2 chuyển xuống Lab bước 2; Trực giác 4.2, 4.4 bỏ |
| Đọc thử lại (subagent mới) | **0 chặn / 5 khó / 22 nhỏ**, quiz 10/10. Bắt được **một câu sai do cắt**: Lab bước 4 "mỗi tuần một phương pháp khác thắng" (thật ra trung bình 4 tuần gần nhất 2/3 tuần) — đã sửa. Sửa thêm: nhãn "23:00" là cả giờ 23:00–23:59; "thực tế = dự báo + sai số" nối quantile sai số với quantile lượng điện; trung vị đếm tay (7) khác cách phổ thông (7,5) |
| Đổi công cụ | bỏ `make`/`env -u VIRTUAL_ENV uv run …` → `python lab.py up/check/notebook`; code Lab vào `code/lab.ipynb` (chạy hết, `kiem_tra_lab.py`); Python thật 3.12.14 (tài liệu cũ ghi 3.12.3 — đã sửa) |
| Biên tập viên cuối | 9 chỗ nhỏ, chỉ 1 chỗ ≥ 30 chữ (4.6 gộp $s$ và $C_u$) — **đạt** (≤ 3). Nhận #1, #5 (dòng 1 : 3 lộ đáp án Tự kiểm tra), #6; giữ hai bước "bằng số rồi bằng chữ" ở 4.6 vì đọc thử Phase 6 cần |
| Cuối | **5.538 chữ (−19,9%)**, PDF **19 → 17 trang**, `kiem_de_hieu` 0 vi phạm |

Chưa đạt mục tiêu −25%: phần còn lại là ví dụ tính tay, câu nói bằng lời, 4 hình × 5 bước, hộp Mượn trước — danh sách
không được cắt. Cắt tiếp sẽ quay lại lỗi Phase 5 (nén chữ).
