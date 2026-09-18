# Phụ lục C — Sổ tay đọc biểu đồ chuỗi thời gian

Mỗi loại biểu đồ: **dùng để trả lời câu hỏi gì**, **đọc gì trên hình**, **bẫy**, và một cặp **đọc
đúng / đọc sai**. Dùng như checklist trước khi kết luận bất cứ điều gì từ một hình.

> **Trạng thái:** cập nhật Phase 3 (2026-09-18) với ví dụ **đo được** từ buổi 4–8. Mỗi mục có một dòng
> "Ví dụ có số" ghi rõ buổi nào, dữ liệu nào, con số nào; hình minh hoạ nằm trong `buoi-NN/hinh/` của
> buổi tương ứng (mỗi buổi tự chứa nên phụ lục không nhúng lại hình).

## Mục lục

- [Nguyên tắc chung trước khi đọc bất kỳ hình nào](#nguyên-tắc-chung-trước-khi-đọc-bất-kỳ-hình-nào)
- [1. Biểu đồ đường theo thời gian (time plot)](#1-biểu-đồ-đường-theo-thời-gian-time-plot)
- [2. Biểu đồ mùa vụ (seasonal plot)](#2-biểu-đồ-mùa-vụ-seasonal-plot)
- [3. Biểu đồ chuỗi con theo mùa (subseries plot)](#3-biểu-đồ-chuỗi-con-theo-mùa-subseries-plot)
- [4. Biểu đồ phân tán và ma trận phân tán](#4-biểu-đồ-phân-tán-và-ma-trận-phân-tán)
- [5. Biểu đồ trễ (lag plot)](#5-biểu-đồ-trễ-lag-plot)
- [6. ACF — hàm tự tương quan](#6-acf--hàm-tự-tương-quan)
- [7. PACF — hàm tự tương quan riêng phần](#7-pacf--hàm-tự-tương-quan-riêng-phần)
- [8. Biểu đồ phân rã](#8-biểu-đồ-phân-rã)
- [9. Periodogram / phổ](#9-periodogram--phổ)
- [10. QQ-plot](#10-qq-plot)
- [11. PIT histogram và rank histogram](#11-pit-histogram-và-rank-histogram)
- [12. Reliability diagram](#12-reliability-diagram)
- [13. Fan chart](#13-fan-chart)
- [14. Biểu đồ gây hiểu nhầm](#14-biểu-đồ-gây-hiểu-nhầm)
- [15. Heatmap lịch (giờ × thứ)](#15-heatmap-lịch-giờ--thứ)
- [16. Boxplot theo mùa](#16-boxplot-theo-mùa)
- [17. CCF — tương quan chéo](#17-ccf--tương-quan-chéo)
- [18. Tương quan trượt](#18-tương-quan-trượt)
- [Nguồn](#nguồn)

## Nguyên tắc chung trước khi đọc bất kỳ hình nào

1. **Đọc trục trước, đọc đường sau:** đơn vị, thang (tuyến tính hay log), trục y bắt đầu từ đâu, múi
   giờ của trục thời gian, có hai trục y không.
2. **Hỏi "nếu là nhiễu thuần thì hình trông thế nào?"** — nhiều "mẫu hình" là thứ nhiễu trắng cũng tạo ra.
3. **Một hình không chứng minh nhân quả.** Hình gợi giả thuyết; kiểm bằng số và bằng dữ liệu khác.
4. **Tiêu đề nói kết luận** ("Tải điện có mùa vụ ngày và tuần, tăng dần qua các năm"), không nói tên
   biến ("Tải điện theo thời gian") — quy ước vẽ hình của cả khoá.

## 1. Biểu đồ đường theo thời gian (time plot)

**Là gì:** quan sát vẽ theo thời điểm quan sát, các điểm liên tiếp nối bằng đường thẳng (FPP 2.1).

**Đọc gì:** xu hướng (trend) — tăng/giảm dài hạn; mùa vụ (seasonality) — lặp theo **chu kỳ cố định và
biết trước** gắn với lịch; chu kỳ (cycle) — dao động lên xuống **không có tần số cố định**; thay đổi
đột ngột về mức (level shift); phương sai thay đổi theo mức; điểm bất thường; đoạn thiếu dữ liệu.

FPP phân biệt: "If the fluctuations are not of a fixed frequency then they are cyclic; if the frequency
is unchanging and associated with some aspect of the calendar, then the pattern is seasonal."

**Bẫy:**
- Đường nối qua đoạn **thiếu dữ liệu** trông như dữ liệu thật đi thẳng — đánh dấu đoạn thiếu.
- Chuỗi dài nén vào một khung hẹp che mất mùa vụ ngắn (tuần trong dữ liệu giờ nhiều năm) — phóng to
  vài tuần, hoặc dùng seasonal plot.
- Tỷ lệ khung hình làm dốc trông dữ hơn hoặc phẳng hơn thật (mục 14).

| Đọc đúng | Đọc sai |
|---|---|
| "Biên độ dao động hằng năm tăng theo mức → cân nhắc biến đổi log / mô hình nhân" | "Chuỗi dao động mạnh hơn nên khó dự báo hơn" (chưa xét biên độ tương đối) |
| "Dao động 6–10 năm không đều → chu kỳ, không phải mùa vụ" | "Có mùa vụ 8 năm" |

**Ví dụ có số (buổi 4, lượt thuê xe theo giờ).** Cùng dữ liệu vẽ ở ba mức gộp: theo giờ (17.544 điểm) chỉ
đọc được "hè cao hơn đông"; theo ngày thấy ngày bão Sandy 29/10/2012 rơi xuống 22 lượt; theo tháng thì mọi
dao động ngày–tuần và cả ngày bão biến mất. Làm trơn 7 ngày biến đúng ngày đó thành 4.632 — một chỗ lõm nhẹ.

## 2. Biểu đồ mùa vụ (seasonal plot)

**Là gì:** dữ liệu vẽ theo **vị trí trong mùa** (tháng trong năm, giờ trong ngày), mỗi mùa một đường.
FPP: làm lộ "the underlying seasonal pattern more clearly and helps identify years when the pattern
changes."

**Đọc gì:** hình dạng mùa vụ; năm/tuần nào lệch khỏi khuôn chung; mùa vụ có đổi dần theo thời gian không.

**Bẫy:** quá nhiều đường chồng nhau không đọc được — tô màu theo năm tăng dần, hoặc chỉ vẽ vài năm; với
dữ liệu giờ có cả mùa vụ ngày và tuần, vẽ riêng từng loại.

| Đọc đúng | Đọc sai |
|---|---|
| "Đỉnh tháng 12 của 2020 thấp bất thường so với các năm → sự kiện, kiểm lại" | "Tháng 12 luôn cao" khi chỉ nhìn đường trung bình |

**Ví dụ có số (buổi 4).** Seasonal plot theo **giờ trong tuần** (0–167) của lượt thuê xe: năm ô T2–T6 có hai
đỉnh (8h và 17h), hai ô T7–CN có một bướu giữa ngày. Tổng ngày lại gần bằng nhau (T2 4.708, T7 4.653, CN
4.523 lượt trên 655 ngày đủ 24 giờ) — khác nhau ở **hình dạng**, không ở mức.

## 3. Biểu đồ chuỗi con theo mùa (subseries plot)

**Là gì:** mỗi mùa (mỗi tháng) một ô nhỏ chứa chuỗi của riêng mùa đó qua các năm; đường ngang là trung
bình của mùa. FPP: "especially useful in identifying changes within particular seasons."

**Đọc gì:** trung bình từng mùa (đường ngang) và **xu hướng bên trong** từng mùa — ví dụ tháng 7 tăng
dần qua các năm trong khi tháng 1 đứng yên.

| Đọc đúng | Đọc sai |
|---|---|
| "Chênh lệch giữa các đường ngang là mùa vụ; độ dốc trong từng ô là mùa vụ đang đổi" | Nhầm đường nối giữa các ô là một chuỗi liên tục |

**Ví dụ có số (buổi 4).** Subseries theo tháng của lượt thuê: trong **mọi** ô, nửa phải (2012) cao hơn nửa
trái (2011) — tỷ lệ 1,41 (tháng 6) đến 2,57 (tháng 3). Bước nhảy giữa hai nửa là ranh giới năm, không phải
xu hướng trong tháng.

**Lưu ý thư viện:** `statsmodels.graphics.tsaplots.month_plot` có docstring "Seasonal plot of monthly data"
nhưng vẽ đúng **subseries plot**, và chỉ nhận dữ liệu tháng/quý.

## 4. Biểu đồ phân tán và ma trận phân tán

**Là gì:** hai biến trên hai trục, mỗi điểm một thời điểm. Ma trận phân tán cho "a quick view of the
relationships between all pairs of variables" (FPP 2.6).

**Đọc gì:** hình dạng quan hệ (tuyến tính, cong, chữ U), độ phân tán, cụm, điểm bất thường.

**Bẫy:**
- Hệ số tương quan "only measures the strength of the linear relationship … and can sometimes be
  misleading" (FPP). Bộ tứ Anscombe: bốn tập dữ liệu cùng tương quan 0,82 nhưng quan hệ khác hẳn nhau.
- **Hai chuỗi cùng có xu hướng** cho đám điểm thẳng hàng dù không liên quan (tương quan giả — buổi 8).
- **Overplotting** (chồng điểm) khi dữ liệu nhiều: dùng điểm trong suốt để vùng dày hiện đậm hơn
  (Wilke, chương 18).

| Đọc đúng | Đọc sai |
|---|---|
| "Đám điểm hình chữ U: tương quan Pearson thấp nhưng hai biến phụ thuộc mạnh (buổi 8 đo bằng mutual information)" | "Tương quan 0,1 → hai biến không liên quan" |
| "Cả hai chuỗi đều tăng theo thời gian; phải sai phân rồi mới xét tương quan" | "Tương quan 0,95 → biến này dự báo được biến kia" |

**Ví dụ có số (buổi 8).** CPI-U × dân số Mỹ, 420 tháng: r trên mức 0,974, R² 0,949, t = 88,6, **DW 0,005**;
sau sai phân r = −0,207. Nhiệt độ × tải điện ERCOT 2024: Pearson 0,616 nhưng $R^2$ tuyến tính chỉ 0,379,
trong khi mô hình hai nhánh CDD/HDD đạt 0,813; chia theo ngưỡng 18,33 °C thì r = −0,649 (lạnh) và +0,910
(nóng). Bộ tứ Anscombe: bốn tập cùng r ≈ 0,82, Spearman 0,818 / 0,691 / 0,991 / 0,500.

**Tô màu theo thời gian (buổi 4).** Scatter nhiệt độ × lượt thuê ngày tô màu theo năm: hai đám mây song
song; cùng ~24,6 °C, 2011 trung bình 4.316 lượt/ngày còn 2012 là 6.751. Tương quan trong từng năm 0,771 và
0,714, nhưng gộp hai năm chỉ 0,627 — trộn hai mức làm quan hệ **trông yếu hơn**.

## 5. Biểu đồ trễ (lag plot)

**Là gì:** $y_t$ vẽ theo $y_{t-k}$ cho vài giá trị $k$ (FPP 2.7).

**Đọc gì:** điểm dồn theo đường chéo ở trễ $k$ → quan hệ mạnh giữa hiện tại và $k$ bước trước. FPP
(dữ liệu bia theo quý): tương quan "strongly positive at lags 4 and 8, reflecting the strong seasonality."

**Bẫy:** chuỗi có xu hướng cho đường chéo ở **mọi** trễ — không phải dấu hiệu mùa vụ.

**Ví dụ có số (buổi 4).** Lượt thuê theo giờ: trễ 1 r = 0,843; trễ 12 r = **−0,144** với đám điểm tách
thành **hai nhánh** bám hai trục (8h sáng cao ghép 20h hôm trước thấp — đỉnh ghép đáy, không phải "quan hệ
âm"); trễ 24 r = 0,819; trễ 168 r = 0,876 (bám đường chéo chặt nhất).

## 6. ACF — hàm tự tương quan

**Là gì:** hệ số tự tương quan mẫu ở trễ $k$ (FPP 2.8):

$$
r_k = \frac{\sum_{t=k+1}^{T} (y_t - \bar y)(y_{t-k} - \bar y)}{\sum_{t=1}^{T} (y_t - \bar y)^2}
$$

vẽ theo $k$ gọi là correlogram.

**Đọc gì (FPP):**
- **Xu hướng:** ACF dương, "slowly decrease as the lags increase".
- **Mùa vụ:** ACF lớn tại trễ bằng bội số của chu kỳ mùa.
- **Cả hai:** giảm chậm do xu hướng, dạng "vỏ sò" (scalloped) do mùa vụ.
- **Nhiễu trắng:** khoảng 95% gai nằm trong $\pm 1.96/\sqrt{T}$. "If one or more large spikes are outside
  these bounds, or if substantially more than 5% of spikes are outside these bounds, then the series
  is probably not white noise."
- **Tính dừng:** chuỗi dừng có ACF "drop to zero relatively quickly"; chuỗi không dừng thường có $r_1$
  lớn và dương (FPP 9.1).

**Bẫy:**
- Với 40 trễ, khoảng 2 gai vượt dải chỉ do ngẫu nhiên — **một gai vượt dải chưa chứng minh gì**.
- **Dải của statsmodels khác dải của FPP:** `plot_acf` mặc định `bartlett_confint=True` — dải tính theo
  công thức Bartlett, **rộng dần theo trễ** khi chuỗi có tự tương quan, không phải dải cố định
  $\pm 1.96/\sqrt T$. Đo với $T = 100$ (statsmodels 0.15.0, seed 1): nhiễu trắng có nửa độ rộng 0,196 ở
  trễ 1 và 0,208 ở trễ 5; AR(1) $\rho = 0.8$ có 0,196 ở trễ 1 nhưng 0,300 ở trễ 5. So hình trong sách với
  hình của mình thì kiểm tùy chọn này trước.
- ACF giảm chậm trước hết là dấu hiệu **không dừng / có xu hướng** (FPP 9.1) — sai phân rồi đọc lại, đừng
  vội kết luận "cần AR bậc cao".

| Đọc đúng | Đọc sai |
|---|---|
| "ACF gai ở 24, 48, 168 → mùa vụ ngày và tuần" | "Gai ở trễ 13 vượt dải → có chu kỳ 13 giờ" (1 gai trong 40 là bình thường) |
| "ACF giảm rất chậm → sai phân trước khi đọc bậc ARIMA" | "ACF giảm chậm → AR(20)" |

**Ví dụ có số (buổi 7).** Mô phỏng n = 500 (seed 42): nhiễu trắng có **1** cột vượt dải ±0,0877 trong 30
trễ; AR(1) φ = 0,7 có $r_1 = 0{,}713$ và 5 cột vượt; random walk $r_1 = 0{,}976$, $r_{30} = 0{,}530$ (30/30
cột vượt). Mô phỏng 1.000 chuỗi nhiễu trắng, 20 trễ: trung bình **0,95** cột vượt dải và **62%** số chuỗi có
ít nhất một cột — dùng Ljung-Box thay vì đếm cột. Dữ liệu thật (buổi 7): lượt thuê theo giờ $r_{24} = 0{,}813$,
$r_{168} = 0{,}864$; gộp lên **ngày** thì chỉ còn đỉnh ở 7, 14, 21.

## 7. PACF — hàm tự tương quan riêng phần

**Là gì:** tương quan giữa $y_t$ và $y_{t-k}$ "after removing the effects of lags 1, 2, 3, …, k−1", cùng
dải tới hạn $\pm 1.96/\sqrt T$ (FPP 9.5).

**Đọc gì — quy tắc của FPP, chỉ cho mô hình thuần:**
- ARIMA($p$,d,0): ACF giảm dần theo hàm mũ hoặc dạng sin; PACF có gai ý nghĩa ở trễ $p$ và **không có**
  gai sau trễ $p$.
- ARIMA(0,d,$q$): PACF giảm dần theo hàm mũ hoặc dạng sin; ACF có gai ý nghĩa ở trễ $q$ và không có gai
  sau trễ $q$.
- Mùa vụ: ARIMA(0,0,0)(0,0,1)$_{12}$ cho gai ở trễ 12 của ACF và PACF giảm dần ở các trễ mùa.

**Bẫy:** FPP ghi rõ "If p and q are both positive, then the plots do not help" — mô hình hỗn hợp không
đọc bậc được từ hình; dùng tiêu chí thông tin (AICc) và kiểm phần dư (buổi 17).

**Bẫy thư viện (buổi 7):** `pacf()` mặc định `method="ywadjusted"` trong khi `plot_pacf()` mặc định
`method="ywm"` — bảng số và hình có thể lệch nhau. Khai `method` tường minh.

**Ví dụ có số (buổi 7).** PACF ở trễ 1 và 2: nhiễu trắng 0,099 / −0,009; AR(1) φ = 0,7 là **0,713 / −0,110**
(cắt sau trễ 1); random walk 0,976 / −0,091; chuỗi có xu hướng tất định 0,979 / 0,320.

## 8. Biểu đồ phân rã

**Là gì:** chuỗi tách thành các thành phần xu hướng–chu kỳ, mùa vụ, phần dư, vẽ chồng từng hàng.

**Đọc gì:**
- **Cộng hay nhân?** FPP 3.2: phân rã cộng hợp khi "the magnitude of the seasonal fluctuations, or the
  variation around the trend-cycle, does not vary with the level"; khi dao động "appears to be
  proportional to the level", dùng phân rã nhân — hoặc lấy log để biến nhân thành cộng.
- **Phần dư phải trông như nhiễu:** còn cấu trúc lặp trong phần dư nghĩa là phân rã bỏ sót một mùa vụ
  (ví dụ dùng chu kỳ 24 cho dữ liệu có cả mùa vụ tuần — buổi 6).
- **So thang của từng hàng:** hàng mùa vụ biên độ nhỏ so với phần dư thì mùa vụ yếu.

**Bẫy:** FPP không khuyến nghị phân rã cổ điển (classical decomposition); các hàng thường vẽ **thang y
khác nhau** — thành phần trông "to" chưa chắc lớn.

**Ví dụ có số (buổi 6, tải điện PJM 2024).** Phân rã cổ điển chu kỳ 24: nhịp tuần **không** vào phần dư mà
vào **xu hướng** (trung bình xu hướng T4 95.036 MW so với CN 88.459 MW); phần dư giữ mùa vụ ngày đổi theo
mùa — tỷ lệ phương sai hồ sơ tháng×giờ trên phương sai chuỗi là **0,102** (MSTL (24, 168) còn 0,0006). Độ
mạnh mùa vụ ngày: 0,618 (cổ điển) so với 0,829 (MSTL) — $F_S$ là thuộc tính của **phân rã**, không chỉ của
dữ liệu. Một giờ số liệu hỏng (21/11/2024, 56,3 GW giữa hai giờ ~95 GW) làm mùa vụ ngày của cả tuần lệch
~6.200 MW nếu không bật `robust`.

## 9. Periodogram / phổ

**Là gì:** theo NIST, spectral plot là "a smoothed Fourier transform of the autocovariance function";
trục ngang là tần số (chu kỳ trên một quan sát).

**Đọc gì:** đỉnh tại tần số $f$ ứng với chu kỳ $1/f$ quan sát. Dữ liệu giờ có đỉnh ở $f = 1/24$ → mùa vụ
ngày. NIST: tần số "0.5 corresponds to a cycle of 2 data points"; chuỗi cách đều chỉ phát hiện được
tần số từ 0 tới 0,5.

**Bẫy:** NIST: "Trends should typically be removed … before applying the spectral plot" — xu hướng dồn
năng lượng vào tần số thấp, che các đỉnh khác. Chu kỳ ngắn hơn 2 bước lấy mẫu không thấy được và có thể
giả dạng thành tần số khác (aliasing — buổi 12).

## 10. QQ-plot

**Là gì:** quantile của dữ liệu (đã sắp) so với quantile lý thuyết của phân phối chuẩn (NIST 1.3.3.21:
trục đứng là dữ liệu, trục ngang là median của thống kê thứ tự chuẩn).

**Đọc gì (NIST):**
- Điểm nằm gần đường thẳng → gần chuẩn.
- **Đuôi dài:** vài điểm đầu lệch **xuống dưới** đường, vài điểm cuối lệch **lên trên**; đuôi ngắn thì
  ngược lại.
- **Lệch phải:** dạng cong bậc hai, mọi điểm nằm **dưới** đường nối điểm đầu và điểm cuối; nằm trên là
  lệch trái.

**Bẫy:** hướng đọc phụ thuộc trục nào là dữ liệu. Một số thư viện đổi trục → mọi quy tắc trên đảo
ngược. Đọc nhãn trục trước.

## 11. PIT histogram và rank histogram

**Là gì:** với dự báo phân phối $F_t$ và giá trị thật $y_t$, PIT là $p_t = F_t(y_t)$. Dự báo lý tưởng cho
PIT phân phối đều → histogram phẳng (Gneiting, Balabdaoui & Raftery 2007).

**Đọc gì (nguyên văn bài báo):**
- "Hump-shaped histograms indicate overdispersed predictive distributions with prediction intervals
  that are too wide on average" — hình **vòm**: khoảng dự báo quá **rộng**.
- "U-shaped histograms often correspond to predictive distributions that are too narrow" — hình **chữ
  U**: quá **hẹp**, quá tự tin.
- "Triangle-shaped histograms are seen when the predictive distributions are biased" — hình **tam
  giác / lệch**: dự báo bị chệch.

Rank histogram của dự báo tập hợp (ensemble) đọc tương tự: chữ U = độ trải ensemble quá nhỏ; vòm = quá
lớn; lệch một phía = chệch (WWRP/WGNE).

**Bẫy:** PIT phẳng là điều kiện **cần** chứ không **đủ** — bài báo viết "uniformity of the PIT values is
a necessary but not a sufficient condition for the forecaster to be ideal". Một dự báo luôn trả về
phân phối khí hậu (trung bình dài hạn) có thể calibrate tốt nhưng vô dụng. Nguyên tắc của bài báo:
"maximizing the sharpness of the predictive distributions subject to calibration".

| Đọc đúng | Đọc sai |
|---|---|
| "PIT chữ U → khoảng quá hẹp, coverage thật thấp hơn danh nghĩa" | "PIT chữ U → khoảng quá rộng" |
| "PIT phẳng; giờ so độ sắc (độ rộng khoảng) với mô hình khác" | "PIT phẳng → mô hình tốt nhất" |

## 12. Reliability diagram

**Là gì:** cho dự báo xác suất của sự kiện nhị phân: trục ngang là xác suất dự báo (chia bin), trục đứng
là tần suất sự kiện xảy ra thật trong bin đó.

**Đọc gì (WWRP/WGNE):** càng gần đường chéo càng đáng tin cậy. "If the curve lies below the line, this
indicates overforecasting (probabilities too high); points above the line indicate underforecasting."
Đường càng phẳng "the less resolution it has". Histogram số lượng dự báo mỗi bin cho biết độ sắc.

**Bẫy:** bin ít dự báo cho điểm nhảy lung tung; cách chia bin làm đổi hình — Bröcker & Smith (2007) đề
xuất thêm **thanh nhất quán** (consistency bars) bằng lấy mẫu lại để biết độ lệch nào nằm trong dao
động ngẫu nhiên.

## 13. Fan chart

**Là gì:** dự báo tương lai vẽ thành các dải đậm nhạt quanh vùng trung tâm. Cách của Ngân hàng Trung
ương Anh (Britton, Fisher & Whitley 1998): dải đậm nhất chứa 10% xác suất, mỗi dải tiếp theo thêm 10
điểm phần trăm, "until 90% of the distribution is covered", dựng từ **mode** ra ngoài.

**Đọc gì:** độ rộng dải theo tầm dự báo (bất định tăng theo tầm); dải lệch về một phía = rủi ro bất đối
xứng.

**Bẫy:** bài viết của BoE ghi nhận kiểu dải đơn trước đó "was often misread as indicating upper and lower
bounds for the forecast" — mép ngoài không phải "giá trị lớn nhất có thể". Dải của BoE dựng từ mode nên
**không trùng** với khoảng quantile đối xứng (5%–95%) mà thư viện dự báo thường vẽ — ghi rõ dải nào là
quantile nào trong chú giải.

## 14. Biểu đồ gây hiểu nhầm

| Lỗi | Vì sao sai | Sửa |
|---|---|---|
| **Trục y của biểu đồ cột không bắt đầu từ 0** | Wilke: "Bars on a linear scale should always start at 0" — độ dài cột mã hoá giá trị | bắt đầu từ 0; muốn phóng chênh lệch thì dùng điểm/đường |
| **Vùng tô dưới đường với trục y cắt** | Wilke: diện tích tô phải tỷ lệ với giá trị; ví dụ giá cổ phiếu tô từ 110 là "misleading" | bỏ tô, hoặc trục từ 0 |
| **Đường / điểm với trục không từ 0** | chấp nhận được: Few viết dot plot "don't require a zero-based scale" | ghi rõ thang trên trục |
| **Hai trục y** | Few: khi hai đường theo hai thang khác nhau "their intersection means nothing"; chỗ cắt nhau là tuỳ ý | hai hình xếp dọc cùng trục thời gian, hoặc chuẩn hoá về cùng thang (chỉ số = 100) |
| **Tỷ lệ khung hình tuỳ ý** | Wilke: chọn tỷ lệ sao cho "important differences in position are noticeable"; cùng đơn vị hai trục thì lưới hai trục phải bằng nhau | banking to 45°: chọn tỷ lệ để độ dốc trung bình của các đoạn thẳng khoảng 45° (Cleveland; Heer & Agrawala 2006) |
| **Chồng điểm (overplotting)** | vùng dày trông như vùng thưa | điểm trong suốt, hexbin; jitter "has to be performed with care" vì làm đổi dữ liệu (Wilke) |

Few cũng thận trọng: "I certainly cannot conclude, once and for all, that graphs with dual-scaled axes
are never useful" — nhưng trong khoá này, mọi biểu đồ hai trục y phải được vẽ lại thành hai hình trước
khi rút kết luận.

## 15. Heatmap lịch (giờ × thứ)

**Là gì:** ma trận trung bình (hoặc tổng) theo hai chiều lịch — thứ × giờ, ngày × tháng — tô màu theo giá trị.

**Đọc gì:** mùa vụ **kép** trong một hình: cột sáng dọc = giờ cao điểm; dòng sáng ngang = ngày đặc biệt; ô
sáng lẻ = sự kiện.

**Bẫy:** heatmap chỉ cho **trung bình** — không thấy độ phân tán (ghép với boxplot); thang màu không tuyến
tính hoặc không có chú giải làm sai lệch; nhầm quy ước thứ (0 = Chủ nhật trong nhiều bộ dữ liệu, 0 = thứ Hai
trong `DatetimeIndex.dayofweek`).

**Ví dụ có số (buổi 4).** Lượt thuê xe: 8h thứ Tư 488 so với 8h Chủ nhật 84; 13h thứ Hai 206 so với 13h thứ
Bảy 385 — hai cột sáng 8h/17h tắt hẳn ở hai dòng cuối tuần.

**Thư viện:** tự dựng bằng `pivot_table` + `imshow` an toàn hơn thư viện lịch (`july` 0.1.3 hỏng với
matplotlib 3.11; `plotly-calplot` ghim plotly < 6).

## 16. Boxplot theo mùa

**Là gì:** phân phối của từng nhóm lịch (giờ, thứ, tháng) vẽ bằng hộp: hộp là khoảng tứ phân vị, vạch giữa là
trung vị.

**Đọc gì:** mức **và** độ phân tán theo mùa; giờ nào khó dự báo (hộp rộng); hai nhóm có chồng nhau không.

**Bẫy:** `showfliers=True` với dữ liệu lớn vẽ hàng nghìn điểm ngoại lai che mất hộp; so hai nhóm khác cỡ mẫu
mà không nói n; seaborn 0.13 + matplotlib 3.11 phát `MatplotlibDeprecationWarning: vert` (vô hại).

**Ví dụ có số (buổi 4).** Ngày làm việc 17h: trung vị 539, hộp 347,5–703,5 (rộng > 350 lượt) — giờ cao điểm
cũng là giờ khó dự báo nhất. Ngày nghỉ 8h: trung vị 94 so với 463 của ngày làm việc — hai phân phối gần như
không chồng nhau.

## 17. CCF — tương quan chéo

**Là gì:** tương quan giữa $x$ và $y$ ở các độ trễ, để tìm biến nào **đi trước** biến nào.

**Đọc gì:** vị trí đỉnh (độ trễ dẫn dắt), dấu, và độ rộng của đỉnh; so với dải $\pm 2/\sqrt{n}$.

**Bẫy:**
- **Quy ước lag ngược nhau giữa thư viện:** `statsmodels.tsa.stattools.ccf(a, b)[k]` = corr($a_{t+k}$, $b_t$)
  (giống R) — muốn "x dẫn y" phải gọi `ccf(y, x)`; hàm `pccf` mới của statsmodels 0.15 lại theo thứ tự ngược
  lại. Luôn kiểm bằng chuỗi mô phỏng $y_t = x_{t-3}$.
- **Chưa prewhitening:** CCF thô mang cấu trúc tự tương quan của chính $x$ nên rộng và có đỉnh giả.

**Ví dụ có số (buổi 8).** CDD × tải điện ERCOT: CCF thô có đỉnh ở trễ 1 (0,863) và **vẫn 0,828 ở trễ 24**;
sau prewhitening AR(48) đỉnh chuyển về **trễ 0** (0,205) và trễ 24 còn 0,061, dải $2/\sqrt{n} = 0{,}021$.

## 18. Tương quan trượt

**Là gì:** hệ số tương quan tính trên cửa sổ trượt, vẽ theo thời gian.

**Đọc gì:** quan hệ có **ổn định** không; đổi dấu ở đâu; cửa sổ ngắn nhiễu hơn, cửa sổ dài trơn nhưng chậm.

**Bẫy:** `rolling("90D")` (cửa sổ theo thời gian) mặc định `min_periods=1` → vài giá trị đầu là ±1 giả; cửa
sổ quá ngắn cho dao động ngẫu nhiên lớn; đọc một con số cả kỳ khi quan hệ đổi chế độ.

**Ví dụ có số (buổi 8).** Nhiệt độ × tải điện ERCOT theo ngày: cả năm 0,616; trượt 90 ngày chạy từ **−0,801**
(cửa sổ kết thúc 31/3/2024) tới **+0,968** (14/10/2024); trượt 30 ngày xuống −0,971 (7/2/2024).

## Nguồn

Truy cập ngày 2026-09-17. Nhật ký research: `tools/NGHIEN-CUU.md`.

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way* —
  chương 2 <https://otexts.com/fpppy/02-graphics.html>, chương 3 <https://otexts.com/fpppy/03-decomposition.html>,
  chương 9 <https://otexts.com/fpppy/09-arima.html>
- statsmodels `plot_acf` (tham số `bartlett_confint`): <https://www.statsmodels.org/stable/generated/statsmodels.graphics.tsaplots.plot_acf.html>
- NIST/SEMATECH e-Handbook — normal probability plot <https://www.itl.nist.gov/div898/handbook/eda/section3/normprpl.htm>;
  spectral plot <https://www.itl.nist.gov/div898/handbook/eda/section3/spectrum.htm>
- Gneiting, T., Balabdaoui, F. & Raftery, A.E. (2007). Probabilistic forecasts, calibration and sharpness.
  *JRSS B* 69(2), 243–268. <https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jrssb.pdf>
- WWRP/WGNE Joint Working Group on Forecast Verification Research — Forecast verification methods:
  <https://www.cawcr.gov.au/projects/verification/>
- Bröcker, J. & Smith, L.A. (2007). Increasing the reliability of reliability diagrams. *Weather and Forecasting* 22(3), 651–661.
- Britton, E., Fisher, P. & Whitley, J. (1998). The Inflation Report projections: understanding the fan chart.
  *Bank of England Quarterly Bulletin*, Q1.
- Wilke, C.O. *Fundamentals of Data Visualization* — chương 3, 17, 18: <https://clauswilke.com/dataviz/>
- Few, S. (2008). Dual-scaled axes in graphs: are they ever the best solution?
  <https://www.perceptualedge.com/articles/visual_business_intelligence/dual-scaled_axes.pdf>
- Heer, J. & Agrawala, M. (2006). Multi-scale banking to 45 degrees. *IEEE TVCG* 12(5). <http://vis.stanford.edu/files/2006-Banking-InfoVis.pdf>
- Cleveland, W.S., McGill, M.E. & McGill, R. (1988). The shape parameter of a two-variable graph. *JASA* 83, 289–300.
