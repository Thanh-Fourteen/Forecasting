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
