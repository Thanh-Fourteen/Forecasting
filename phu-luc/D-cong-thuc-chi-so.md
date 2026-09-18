# Phụ lục D — Bảng công thức chỉ số đánh giá dự báo

Công thức, ý nghĩa, **khi nào dùng / khi nào không**, và cách các thư viện cài đặt khác nhau. Mọi
con số trong ví dụ lấy từ lần chạy thật (NumPy 2.5.3, pandas 2.3.3, utilsforecast 0.2.16,
scoringrules 0.11.0, ngày 2026-09-17).

> **Trạng thái:** bản khởi đầu (Phase 0). Buổi 14 (chỉ số), 15 (Diebold–Mariano) và 25 (dự báo xác
> suất) bổ sung ví dụ trên dữ liệu thật và đối chiếu với `tv.danh_gia`.

**Quy ước ký hiệu** (theo FPP 5.8): giá trị thật $y_t$, dự báo $\hat y_t$, sai số
$e_t = y_t - \hat y_t$ (dương = dự báo **thấp** hơn thực tế). Trung bình lấy trên các điểm của tập
đánh giá. $T$ là số quan sát huấn luyện, $m$ là chu kỳ mùa vụ.

## Mục lục

- [1. Chọn chỉ số theo quyết định](#1-chọn-chỉ-số-theo-quyết-định)
- [2. Chỉ số cho dự báo điểm](#2-chỉ-số-cho-dự-báo-điểm)
- [3. Chỉ số có chia thang (MASE, RMSSE) và biến thể M5](#3-chỉ-số-có-chia-thang-mase-rmsse-và-biến-thể-m5)
- [4. Chỉ số cho dự báo quantile và khoảng](#4-chỉ-số-cho-dự-báo-quantile-và-khoảng)
- [5. Chỉ số cho dự báo phân phối: CRPS](#5-chỉ-số-cho-dự-báo-phân-phối-crps)
- [6. Dự báo xác suất sự kiện: Brier, log score](#6-dự-báo-xác-suất-sự-kiện-brier-log-score)
- [7. Skill score](#7-skill-score)
- [8. So hai mô hình: Diebold–Mariano](#8-so-hai-mô-hình-dieboldmariano)
- [9. Ví dụ tính tay đã kiểm](#9-ví-dụ-tính-tay-đã-kiểm)
- [10. Thư viện tính khác nhau thế nào](#10-thư-viện-tính-khác-nhau-thế-nào)
- [11. Bẫy thường gặp](#11-bẫy-thường-gặp)
- [Nguồn](#nguồn)

## 1. Chọn chỉ số theo quyết định

Gneiting (2011) cảnh báo cách làm phổ biến "can lead to grossly misguided inferences, unless the scoring
function and the forecasting task are carefully matched": mỗi hàm mất mát thưởng cho một **đại lượng**
khác nhau của phân phối dự báo.

| Hàm mất mát | Dự báo tối ưu là | Hợp khi |
|---|---|---|
| sai số bình phương (MSE, RMSE, RMSSE) | **trung bình** | chi phí tăng theo bình phương sai số; cần tổng đúng (tổng nhiều SKU) |
| sai số tuyệt đối (MAE, MASE, WAPE) | **trung vị** | chi phí tỷ lệ với độ lệch, đối xứng |
| pinball mức $\tau$ | **quantile $\tau$** | chi phí bất đối xứng (thiếu hàng đắt hơn tồn kho) |
| sai số phần trăm tuyệt đối (MAPE) | một đại lượng không chuẩn, "tends to support severe underforecasts" | hầu như không nên dùng để chọn mô hình |
| CRPS, WIS, log score | **cả phân phối** | quyết định cần khoảng hoặc xác suất |

## 2. Chỉ số cho dự báo điểm

| Chỉ số | Công thức | Đơn vị | Ghi chú |
|---|---|---|---|
| MAE | $\operatorname{mean}(\lvert e_t\rvert)$ | như dữ liệu | tối ưu ở trung vị |
| RMSE | $\sqrt{\operatorname{mean}(e_t^2)}$ | như dữ liệu | tối ưu ở trung bình; nhạy với sai số lớn |
| ME (bias) | $\operatorname{mean}(e_t)$ | như dữ liệu | dương = dự báo thấp có hệ thống (theo quy ước $e = y - \hat y$) |
| MAPE | $\operatorname{mean}(\lvert 100\,e_t / y_t\rvert)$ | % | vô hạn/không xác định khi $y_t = 0$ |
| sMAPE | $\operatorname{mean}\big(200\,\lvert y_t - \hat y_t\rvert / (y_t + \hat y_t)\big)$ | 0–200 | FPP và Hyndman & Koehler khuyên **không dùng** |
| WAPE | $\sum_t \lvert e_t\rvert \,/\, \sum_t \lvert y_t\rvert$ | tỷ lệ | còn gọi MAD/Mean ratio |

**MAPE.** FPP: sai số phần trăm "infinite or undefined if $y_t = 0$" và chỉ có nghĩa khi đơn vị đo có
số 0 có ý nghĩa (không dùng cho nhiệt độ °C). Hyndman & Koehler (2006): phân phối "extremely skewed
when any $Y_t$ is close to zero". Với $y_t > 0$ cố định và dự báo không âm, dự báo thấp thì sai số phần trăm bị
chặn ở 100% còn dự báo cao thì không bị chặn — FPP tóm lại là MAPE phạt nặng sai số âm (dự báo cao) hơn sai số dương.

**sMAPE.** FPP: "the value of sMAPE can be negative" (khi $y_t + \hat y_t < 0$) — tên "symmetric" gây
hiểu nhầm; Hyndman & Koehler (2006) "recommend that the sMAPE not be used".

**WAPE.** Hyndman (2025) ghi WAPE "was introduced by Kolassa & Schütz (2007) who called it the MAD/Mean
ratio"; tối ưu WAPE dẫn tới dự báo trung vị, và chỉ số này "only consistent when the time series is
stationary".

## 3. Chỉ số có chia thang (MASE, RMSSE) và biến thể M5

Chia sai số cho sai số **trong mẫu huấn luyện** của một phương pháp naive để so được giữa các chuỗi khác
đơn vị. Hyndman & Koehler (2006) đề xuất MASE "become the standard measure for comparing forecast
accuracy across multiple time series".

$$
\text{MASE} = \frac{\operatorname{mean}(\lvert e_j \rvert)}{\frac{1}{T-m}\sum_{t=m+1}^{T} \lvert y_t - y_{t-m} \rvert}
\qquad
\text{RMSSE} = \sqrt{\frac{\operatorname{mean}(e_j^2)}{\frac{1}{T-m}\sum_{t=m+1}^{T} (y_t - y_{t-m})^2}}
$$

$m = 1$ cho dữ liệu không mùa vụ (naive), $m$ = chu kỳ mùa cho dữ liệu mùa vụ (seasonal naive).

**Đọc đúng:** MASE < 1 nghĩa là dự báo tốt hơn sai số **một bước trong mẫu** của (seasonal) naive —
**không** có nghĩa là thắng seasonal naive trên tập test ở cùng tầm dự báo. Muốn biết thắng baseline
không, chạy baseline trên cùng backtest (buổi 14–15).

**M5 (Makridakis et al., hướng dẫn thi M5):**

$$
\text{RMSSE} = \sqrt{\frac{1}{h}\,\frac{\sum_{t=n+1}^{n+h}(Y_t - \hat Y_t)^2}{\frac{1}{n-1}\sum_{t=2}^{n}(Y_t - Y_{t-1})^2}}
\qquad
\text{WRMSSE} = \sum_{i} w_i \,\text{RMSSE}_i
$$

- Mẫu số chỉ tính từ **sau lần bán đầu tiên khác 0** của chuỗi.
- Trọng số $w_i$ theo **doanh thu** (số lượng × giá) của 28 ngày cuối tập huấn luyện, tổng bằng 1 ở mỗi
  cấp gộp.
- Lý do dùng bình phương thay vì tuyệt đối: sai số tuyệt đối "optimized for the median" sẽ thưởng cho
  dự báo gần 0 trên chuỗi bán gián đoạn.

M5 phần bất định dùng **scaled pinball loss** (SPL) tại 9 mức
$u \in \{0.005, 0.025, 0.165, 0.25, 0.5, 0.75, 0.835, 0.975, 0.995\}$, chia cho mẫu số dạng tuyệt đối
$\frac{1}{n-1}\sum \lvert Y_t - Y_{t-1}\rvert$.

## 4. Chỉ số cho dự báo quantile và khoảng

**Pinball loss / quantile score** cho dự báo quantile $q_{\tau,t}$:

$$
L_\tau(y_t, q_{\tau,t}) = \begin{cases} \tau\,(y_t - q_{\tau,t}) & y_t \ge q_{\tau,t} \\ (1-\tau)\,(q_{\tau,t} - y_t) & y_t < q_{\tau,t} \end{cases}
$$

FPP 5.9 định nghĩa **quantile score có nhân 2** (để tại $\tau = 0.5$ bằng sai số tuyệt đối) và ghi "The
multiplier of 2 is often omitted". Hướng dẫn M5 và `utilsforecast.quantile_loss` **không** nhân 2.

**Winkler score / interval score** cho khoảng $[\ell_t, u_t]$ danh nghĩa $100(1-\alpha)\%$ (FPP 5.9;
Gneiting & Raftery 2007 gọi là interval score):

$$
W_{\alpha,t} = (u_t - \ell_t) + \frac{2}{\alpha}(\ell_t - y_t)\,\mathbb{1}\{y_t < \ell_t\} + \frac{2}{\alpha}(y_t - u_t)\,\mathbb{1}\{y_t > u_t\}
$$

Thưởng khoảng hẹp, phạt nặng khi giá trị thật rơi ra ngoài. FPP: $W_{\alpha,t} = (Q_{\alpha/2,t} +
Q_{1-\alpha/2,t})/\alpha$ với $Q$ là quantile score.

**Weighted interval score (WIS)** — Bracher, Ray, Gneiting & Reich (2021) — gộp trung vị $m$ và $K$
khoảng mức $\alpha_1, \dots, \alpha_K$:

$$
\text{WIS} = \frac{1}{K + 1/2}\left( w_0 \lvert y - m \rvert + \sum_{k=1}^{K} w_k\, \text{IS}_{\alpha_k} \right),
\qquad w_0 = \tfrac{1}{2},\; w_k = \tfrac{\alpha_k}{2}
$$

Bài báo: với trọng số này "WIS ≈ CRPS"; với $K = 0$ WIS bằng sai số tuyệt đối. Dạng tương đương theo
$2K+1$ quantile: $\frac{1}{2K+1}\sum_k 2\{\mathbb{1}(y \le q_{\tau_k}) - \tau_k\}(q_{\tau_k} - y)$.

**Coverage** (tỷ lệ phủ): tỷ lệ giá trị thật nằm trong khoảng. Coverage **không phải** một scoring rule
— khoảng vô hạn luôn phủ 100%. Luôn báo cùng độ rộng khoảng hoặc dùng Winkler/WIS.

## 5. Chỉ số cho dự báo phân phối: CRPS

Gneiting & Raftery (2007) định nghĩa cho phân phối dự báo có CDF $F$ và giá trị thật $x$:

$$
\text{CRPS}(F, x) = \int_{-\infty}^{\infty} \big(F(y) - \mathbb{1}\{y \ge x\}\big)^2 \, dy
= \mathbb{E}_F\lvert X - x\rvert - \tfrac{1}{2}\,\mathbb{E}_F\lvert X - X'\rvert
$$

với $X, X'$ độc lập cùng phân phối $F$ (dạng kernel, eq. 21). Hai hệ quả:

- CRPS là "the integral of the Brier scores" tại mọi ngưỡng; FPP diễn đạt là trung bình quantile score
  trên mọi mức $p$.
- Với dự báo điểm (phân phối suy biến), CRPS **bằng sai số tuyệt đối** — so được trực tiếp dự báo xác
  suất với dự báo điểm.

**Phân phối chuẩn** $N(\mu, \sigma^2)$, $z = (x-\mu)/\sigma$:

$$
\text{CRPS} = \sigma\left[ z\,\big(2\Phi(z) - 1\big) + 2\varphi(z) - \frac{1}{\sqrt{\pi}} \right]
$$

**Từ $M$ mẫu** (dự báo dạng sample path / ensemble), ước lượng năng lượng:
$\frac{1}{M}\sum_i \lvert x_i - y\rvert - \frac{1}{2M^2}\sum_{i,j}\lvert x_i - x_j\rvert$.

## 6. Dự báo xác suất sự kiện: Brier, log score

**Brier score** cho xác suất dự báo $p_i$ và kết quả $o_i \in \{0,1\}$: $\text{BS} = \frac{1}{N}\sum_i (p_i - o_i)^2$.

**Phân rã Murphy (1973)** — nhóm dự báo theo các giá trị xác suất $p_k$, $n_k$ lần, tần suất thật
$\bar o_k$, tần suất chung $\bar o$:

$$
\text{BS} = \underbrace{\frac{1}{N}\sum_k n_k (p_k - \bar o_k)^2}_{\text{reliability (nhỏ = tốt)}}
- \underbrace{\frac{1}{N}\sum_k n_k (\bar o_k - \bar o)^2}_{\text{resolution (lớn = tốt)}}
+ \underbrace{\bar o\,(1 - \bar o)}_{\text{uncertainty}}
$$

Đẳng thức đúng chính xác khi mỗi nhóm có đúng một giá trị xác suất (như ví dụ mục 9).

**Log score:** $-\log p(\text{kết quả xảy ra})$. Gneiting & Raftery (2007) ghi nhận nó "has been
criticized for its unboundedness" — một dự báo xác suất 0 cho sự kiện rồi xảy ra cho điểm vô hạn.

## 7. Skill score

So với một dự báo tham chiếu (FPP 5.9):

$$
\text{Skill} = \frac{\text{Score}_{\text{tham chiếu}} - \text{Score}_{\text{mô hình}}}{\text{Score}_{\text{tham chiếu}}}
$$

FPP: "When the data are seasonal, SeasonalNaive() should be used as the benchmark." Theo WWRP/WGNE,
Brier skill score "Not strictly proper" — không dùng nó để tối ưu mô hình.

## 8. So hai mô hình: Diebold–Mariano

Chuỗi chênh lệch mất mát $d_t = g(e_{1t}) - g(e_{2t})$ trên $n$ dự báo tầm $h$. Harvey, Leybourne & Newbold
(1997):

$$
S_1 = \frac{\bar d}{\sqrt{\hat V(\bar d)}}, \quad \hat V(\bar d) \approx \frac{1}{n}\Big[\hat\gamma_0 + 2\sum_{k=1}^{h-1}\hat\gamma_k\Big],
\qquad
S_1^* = \left[\frac{n + 1 - 2h + n^{-1}h(h-1)}{n}\right]^{1/2} S_1
$$

$S_1^*$ so với **phân phối Student-t $n-1$ bậc tự do**. Bài báo cho biết kiểm định gốc "was found to be
quite seriously over-sized for moderate numbers of sample observations" — bác bỏ giả thuyết "hai mô
hình bằng nhau" quá dễ khi mẫu nhỏ. `forecast::dm.test` của R cài đặt bản hiệu chỉnh này.

## 9. Ví dụ tính tay đã kiểm

**Dự báo điểm.** Chuỗi huấn luyện mùa vụ $m = 4$:
`10 20 30 20 12 22 33 21 13 24 35 23`; test $y$ = `14 25 36 24`, dự báo $\hat y$ = `12 27 30 25`.

| Đại lượng | Tự tính (NumPy) | utilsforecast 0.2.16 |
|---|---|---|
| $e = y - \hat y$ | 2, −2, 6, −1 | |
| MAE | 2,75 | `mae` 2,75 |
| RMSE | 3,3541 | `rmse` 3,3541 |
| ME | 1,25 | `bias` **−1,25** (định nghĩa $\hat y - y$) |
| MAPE | 10,7798% | `mape` **0,107798** (tỷ lệ) |
| sMAPE (FPP, 0–200) | 11,3351 | `smape` **0,056675** (thang 0–1) |
| WAPE | 0,1111 | `nd` 0,1111 |
| mẫu số MASE: $\operatorname{mean}\lvert y_t - y_{t-4}\rvert$ | 1,875 | |
| MASE | 1,4667 | `mase` 1,4667 |
| RMSSE (mẫu số MSE 3,875) | 1,7039 | `rmsse` 1,7039 |

MASE = 1,47 > 1: sai số trên test lớn hơn sai số seasonal naive một bước trong mẫu.

**Pinball.** Quantile $\tau = 0.9$ dự báo `11 23 31 22` cho cùng $y$: pinball (không nhân 2) = 2,70;
quantile score của FPP (nhân 2) = 5,40; `utilsforecast.quantile_loss` = 2,70.

**WIS.** $y = 10$, trung vị 8, khoảng 80% (α = 0,2) là [6, 9], khoảng 50% (α = 0,5) là [7; 8,5]:
$\text{IS}_{0.2} = 3 + \frac{2}{0.2}\cdot 1 = 13$; $\text{IS}_{0.5} = 1{,}5 + \frac{2}{0.5}\cdot 1{,}5 = 7{,}5$;
$\text{WIS} = (0{,}5\cdot 2 + 0{,}1\cdot 13 + 0{,}25\cdot 7{,}5)/2{,}5 = 1{,}67$. Dạng quantile (5 quantile
0,1 / 0,25 / 0,5 / 0,75 / 0,9) cũng ra **1,67**.

**CRPS.** $N(0, 1)$, giá trị thật 0,8: công thức đóng = 0,4762 (`scoringrules.crps_normal` 0,4762); ước
lượng năng lượng từ 4.000 mẫu (seed 3) = 0,4632.

**Brier.** Xác suất `.1 .1 .1 .1 .7 .7 .7 .7 .7 .9`, kết quả `0 0 1 0 1 1 0 1 1 1`:
BS = 0,170; reliability 0,015; resolution 0,085; uncertainty 0,240; 0,015 − 0,085 + 0,240 = 0,170.

**Diebold–Mariano.** Hai chuỗi sai số 40 điểm (seed 11), mất mát bình phương, $h = 1$: $S_1 = -1{,}455$,
p = 0,146 (chuẩn); $S_1^* = -1{,}437$, p = 0,159 ($t_{39}$). Không đủ bằng chứng một mô hình tốt hơn.

## 10. Thư viện tính khác nhau thế nào

| Thư viện / nguồn | Điểm khác | Hậu quả nếu không để ý |
|---|---|---|
| `utilsforecast` 0.2.16 `smape` | $\lvert y - \hat y\rvert / (\lvert y\rvert + \lvert\hat y\rvert)$, thang **0–1** | con số nhỏ hơn FPP/M4 200 lần |
| `utilsforecast` `mape` | tỷ lệ, không nhân 100; $y = 0$ bị bỏ khỏi trung bình | "MAPE 0,1" tưởng là 0,1% |
| `utilsforecast` `bias` | $\hat y - y$ (ngược dấu $e$ của FPP) | đọc ngược hướng chệch |
| `utilsforecast` `quantile_loss` | không nhân 2 | lệch 2 lần so với quantile score FPP |
| `scoringrules` 0.11.0 `weighted_interval_score` (backend mặc định, không numba) | **cho 2,87 thay vì 1,67** ở ví dụ mục 9 — nhánh này cộng trọng số × trung vị thay vì × \|y − trung vị\| | WIS sai; tự viết theo công thức Bracher hoặc kiểm với ví dụ trên |
| `statsmodels` / FPP ACF | xem Phụ lục C mục 6 | |
| `properscoring` | bản cuối 0.1 (2015), repo đã archive (09/2026) | dùng `scoringrules` cho CRPS (`crps_normal`, `crps_ensemble` khớp ví dụ mục 9) |

## 11. Bẫy thường gặp

| Bẫy | Vì sao sai | Làm đúng |
|---|---|---|
| Báo MAPE cho chuỗi có số 0 hoặc gần 0 | vô hạn, hoặc phân phối cực lệch | MASE, RMSSE, WAPE |
| So sMAPE giữa hai báo cáo | thang 0–200, 0–100 và 0–1 cùng tên | ghi công thức và thang |
| MASE < 1 → "thắng seasonal naive" | mẫu số là sai số một bước **trong mẫu** | chạy seasonal naive trên cùng backtest |
| Tối ưu MAE/MASE cho chuỗi bán gián đoạn | tối ưu trung vị → thưởng dự báo 0 | RMSSE (lý do M5 dùng) hoặc chỉ số theo chi phí tồn kho |
| Chọn mô hình theo MAPE | MAPE thưởng dự báo thấp (Gneiting 2011) | chỉ số khớp với hàm chi phí |
| Chỉ báo coverage | khoảng rộng vô tận cũng phủ 100% | Winkler/WIS/CRPS kèm coverage |
| Trộn pinball có và không nhân 2 | chênh đúng 2 lần | ghi quy ước; WIS dạng quantile có nhân 2 |
| WIS "bằng" CRPS | chỉ xấp xỉ, sát hơn khi nhiều khoảng | ghi rõ số khoảng $K$ |
| Brier skill score để tối ưu | không strictly proper | tối ưu Brier, báo skill để so sánh |
| DM với ngưỡng chuẩn trên mẫu nhỏ | bác bỏ quá dễ | bản HLN với $t_{n-1}$ |
| WRMSSE trọng số theo số lượng bán | M5 dùng **doanh thu** 28 ngày cuối | số lượng × giá |

## Nguồn

Truy cập ngày 2026-09-17. Nhật ký research: `tools/NGHIEN-CUU.md`.

- Hyndman, R.J., Athanasopoulos, G. et al. *FPP, the Pythonic Way* — mục 5.8, 5.9: <https://otexts.com/fpppy/05-toolbox.html>
- Hyndman, R.J. & Koehler, A.B. (2006). Another look at measures of forecast accuracy. *International
  Journal of Forecasting* 22(4), 679–688. Preprint: <https://robjhyndman.com/papers/mase.pdf>
- Hyndman, R.J. (2025). WAPE (Hyndsight): <https://robjhyndman.com/hyndsight/wape.html>
- Makridakis, S. et al. M5 Competitors' Guide: <https://github.com/Mcompetitions/M5-methods/blob/master/M5-Competitors-Guide.pdf>
- Gneiting, T. (2011). Making and evaluating point forecasts. *JASA* 106(494), 746–762. <https://arxiv.org/abs/0912.0902>
- Gneiting, T. & Raftery, A.E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA*
  102, 359–378. <https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf>
- Bracher, J., Ray, E.L., Gneiting, T. & Reich, N.G. (2021). Evaluating epidemic forecasts in an interval
  format. *PLoS Computational Biology* 17(2), e1008618. <https://doi.org/10.1371/journal.pcbi.1008618>
- Murphy, A.H. (1973). A new vector partition of the probability score. *J. Applied Meteorology* 12, 595–600
  (qua trang WWRP/WGNE: <https://www.cawcr.gov.au/projects/verification/>)
- Harvey, D., Leybourne, S. & Newbold, P. (1997). Testing the equality of prediction mean squared errors.
  *International Journal of Forecasting* 13, 281–291.
- `utilsforecast` 0.2.16 (đọc mã nguồn `losses.py` trong gói): <https://pypi.org/project/utilsforecast/>
- `scoringrules` 0.11.0: <https://pypi.org/project/scoringrules/>
