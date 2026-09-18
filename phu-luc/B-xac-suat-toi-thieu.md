# Phụ lục B — Xác suất thống kê tối thiểu cho dự báo

Đủ để đọc mọi buổi của khoá mà không phải tin công thức một cách mù quáng. Buổi 2 dạy lại các ý này
kèm lab; phụ lục là bản tra cứu. Mỗi con số minh hoạ dưới đây lấy từ mô phỏng **đã chạy** (NumPy 2.5.3,
SciPy 1.18.1, seed ghi cạnh kết quả).

## Mục lục

- [1. Biến ngẫu nhiên, phân phối, quantile](#1-biến-ngẫu-nhiên-phân-phối-quantile)
- [2. Trung bình, trung vị, quantile — câu trả lời cho ba câu hỏi khác nhau](#2-trung-bình-trung-vị-quantile--câu-trả-lời-cho-ba-câu-hỏi-khác-nhau)
- [3. Các phân phối hay gặp](#3-các-phân-phối-hay-gặp)
- [4. Luật số lớn, định lý giới hạn trung tâm — và khi nào chúng không cứu bạn](#4-luật-số-lớn-định-lý-giới-hạn-trung-tâm--và-khi-nào-chúng-không-cứu-bạn)
- [5. Likelihood và MLE](#5-likelihood-và-mle)
- [6. Khoảng tin cậy và khoảng dự báo](#6-khoảng-tin-cậy-và-khoảng-dự-báo)
- [7. Bootstrap](#7-bootstrap)
- [8. Hồi quy và R²](#8-hồi-quy-và-r²)
- [9. Bẫy thường gặp](#9-bẫy-thường-gặp)
- [Nguồn](#nguồn)

## 1. Biến ngẫu nhiên, phân phối, quantile

**Biến ngẫu nhiên** $Y$ là đại lượng mà trước khi quan sát ta chỉ biết các giá trị có thể có và khả
năng của chúng — ví dụ lượt thuê xe giờ tới. Dự báo tốt nhất về $Y$ là cả một **phân phối**, không
phải một con số.

- **Hàm phân phối tích luỹ (CDF):** $F(y) = P(Y \le y)$, tăng từ 0 tới 1.
- **Hàm mật độ (PDF)** cho biến liên tục, **hàm khối xác suất (PMF)** $P(Y = k)$ cho biến đếm.
- **Quantile mức $p$:** giá trị $q_p$ mà $P(Y \le q_p) = p$ — "ngưỡng mà $p \cdot 100\%$ khả năng
  không vượt". Chính xác hơn, $q_p = \inf\{y : F(y) \ge p\}$. Trung vị là $q_{0.5}$.

**Quantile thực nghiệm** tính từ mẫu hữu hạn có nhiều quy ước; Hyndman & Fan (1996) liệt kê 9 loại.
`np.quantile` mặc định dùng loại 7 (`method="linear"`):

```python
np.quantile([3, 1, 4, 1, 5], 0.3)    # 1.4  — sắp lại 1, 1, 3, 4, 5 rồi nội suy tuyến tính
```

## 2. Trung bình, trung vị, quantile — câu trả lời cho ba câu hỏi khác nhau

Chọn con số dự báo nào phụ thuộc **hàm mất mát** mà người dùng dự báo chịu. Gneiting (2011) chứng minh:
sai số bình phương "is consistent for the mean", sai số tuyệt đối "for the median", và hàm mất mát
tuyến tính từng khúc bậc $\tau$ (pinball loss) nhất quán với quantile mức $\tau$:

$$
L_\tau(y, q) = \begin{cases} \tau\,(y - q) & y \ge q \\ (1-\tau)\,(q - y) & y < q \end{cases}
$$

Kiểm bằng số trên 10.000 quan sát log-chuẩn (lệch phải, seed 2026) — tìm hằng số $c$ làm nhỏ nhất
từng hàm mất mát:

| Tối thiểu hoá | $c$ tối ưu | So với |
|---|---|---|
| trung bình sai số bình phương | 1,669 | trung bình mẫu 1,669 |
| trung bình sai số tuyệt đối | 1,003 | trung vị mẫu 1,003 |
| pinball $\tau = 0.9$ | 3,634 | quantile 0,9 của mẫu 3,634 |

Hệ quả thực tế: dữ liệu càng lệch thì trung bình và trung vị càng xa nhau (ở đây 1,669 so với 1,003),
và chọn sai chỉ số đánh giá là tối ưu cho sai câu hỏi. Gneiting (2011) cũng chỉ ra sai số phần trăm
tuyệt đối (MAPE) nhất quán với một đại lượng không chuẩn, không phải trung vị — xem Phụ lục D.

## 3. Các phân phối hay gặp

| Phân phối | Dùng cho | Đặc điểm cần nhớ |
|---|---|---|
| Chuẩn $N(\mu, \sigma^2)$ | sai số cộng, đối xứng | 95% khối xác suất trong $\mu \pm 1.96\sigma$ |
| Poisson($\mu$) | đếm sự kiện độc lập | $P(Y=k) = e^{-\mu}\mu^k / k!$; **phương sai = trung bình** |
| Âm nhị thức | đếm có phân tán thừa (bán hàng, lượt thuê) | phương sai $\sigma^2 = \mu + \alpha\mu^2$ lớn hơn trung bình |
| Student-t($\nu$) | sai số đuôi dày (tài chính) | khác chuẩn ở "the heaviness of the tails"; $\nu \le 2$ không có phương sai hữu hạn; $\nu = 1$ là Cauchy |

Mô phỏng 100.000 giá trị (seed 2026): Poisson(5) có trung bình 4,99, phương sai 4,99; âm nhị thức
cùng trung bình 5 (tham số scipy `n=2`) có trung bình 5,01, phương sai 17,80 — gần giá trị lý thuyết
$5 + 5^2/2 = 17{,}5$. Khi dữ liệu đếm có phương sai lớn hơn trung bình (kiểm bằng tỷ lệ phương sai /
trung bình), giả định Poisson cho khoảng dự báo quá hẹp.

**Cẩn thận tham số hoá:** `scipy.stats.nbinom` dùng $(n, p)$ với $p = n/(n+\mu)$, khác dạng $(\mu,
\alpha)$ trong statsmodels và sách GLM. Đọc tài liệu của thư viện trước khi truyền tham số.

## 4. Luật số lớn, định lý giới hạn trung tâm — và khi nào chúng không cứu bạn

**Định lý giới hạn trung tâm (CLT)** cho mẫu **i.i.d.** có trung bình và phương sai **hữu hạn**:
$(S_n - n\mu)/(\sigma\sqrt n)$ hội tụ về phân phối chuẩn. Hai điều kiện in đậm hay bị quên.

**Đuôi quá dày.** Phân phối Cauchy không có trung bình hữu hạn. NIST viết: với Cauchy, "collecting
1,000 data points gives no more accurate an estimate of the mean and standard deviation than does a
single point." Mô phỏng (200 lần mỗi cỡ mẫu, seed 2026) — độ trải (IQR) của trung bình mẫu:

| $n$ | Cauchy | Chuẩn |
|---|---|---|
| 10 | 2,014 | 0,3837 |
| 1.000 | 2,149 | 0,0357 |
| 100.000 | 1,674 | 0,0044 |

Với phân phối chuẩn, tăng mẫu 100 lần thì độ trải giảm khoảng 10 lần; với Cauchy thì không giảm.

**Phụ thuộc theo thời gian.** Chuỗi thời gian hiếm khi i.i.d. Với tự tương quan dương, $n$ quan sát
chứa ít thông tin hơn $n$ quan sát độc lập. Với AR(1) hệ số $\rho$, **cỡ mẫu hiệu dụng** xấp xỉ

$$
n_{\text{eff}} \approx n \, \frac{1 - \rho}{1 + \rho}
$$

(dạng đặc biệt của công thức trong Bretherton et al., 1999). Mô phỏng $n = 200$, 5.000 lần (seed 2026),
$n_{\text{eff}}$ đo bằng $\operatorname{Var}(y_t) / \operatorname{Var}(\bar y)$:

| $\rho$ | mô phỏng | công thức |
|---|---|---|
| 0 | 197,2 | 200,0 |
| 0,5 | 65,2 | 66,7 |
| 0,9 | 11,3 | 10,5 |

Một chuỗi 200 giờ có $\rho = 0.9$ chỉ "đáng giá" khoảng 11 quan sát độc lập khi ước lượng
trung bình — mọi khoảng tin cậy tính theo $\sigma/\sqrt{200}$ sẽ hẹp sai.

## 5. Likelihood và MLE

Với dữ liệu $y$ và mô hình có tham số $\theta$, **likelihood** $L(\theta) = P(y \mid \theta)$ là xác
suất (hoặc mật độ) của chính dữ liệu đã thấy nếu tham số là $\theta$. **Ước lượng hợp lý cực đại
(MLE)** là giá trị $\theta$ làm $L(\theta)$ lớn nhất — thường tính qua log-likelihood cho ổn định số.
Tài liệu MIT 18.05 nhắc: đừng nhầm $P(\text{data} \mid p)$ với $P(p \mid \text{data})$ — likelihood
không phải xác suất của tham số.

ETS và ARIMA trong FPP được ước lượng bằng cách cực đại hoá likelihood (chương 8, 9); buổi 16–17 và 30
dùng lại ý này.

## 6. Khoảng tin cậy và khoảng dự báo

Theo Hyndman:

- **Khoảng dự báo** gắn với "a random variable yet to be observed": xác suất giá trị tương lai rơi vào
  khoảng.
- **Khoảng tin cậy** gắn với "a parameter and is a frequentist concept": ví dụ khoảng cho trung bình.

Khoảng dự báo luôn rộng hơn, vì ngoài bất định của tham số còn cộng thêm biến động của chính quan sát
mới. FPP (mục 5.5) cho khoảng dự báo 95% dạng $\hat y_{T+h|T} \pm 1.96\,\hat\sigma_h$, với giả định sai số
chuẩn, không tự tương quan, phương sai không đổi.

Hai giới hạn FPP nêu rõ:

- Khoảng của ARIMA "tend to be too narrow" vì chỉ tính biến động của sai số, bỏ qua bất định của tham
  số và của việc chọn bậc mô hình (mục 9.8).
- Khoảng của hồi quy không tính bất định của **dự báo biến giải thích** (chương 10).

**"±1,96σ" trên dữ liệu lệch.** Mô phỏng (seed 2026): lấy 200 quan sát log-chuẩn, dựng khoảng
$\bar y \pm 1.96 s$, rồi đếm tỷ lệ 1.000 quan sát **mới** rơi ra ngoài mỗi đuôi, lặp 2.000 lần:

| độ lệch (σ của log) | phủ tổng | dưới cận dưới | trên cận trên | kỳ vọng mỗi đuôi |
|---|---|---|---|---|
| 0,5 | 95,1% | 0,0% | 4,9% | 2,5% |
| 1,0 | 95,6% | 0,0% | 4,4% | 2,5% |
| 1,5 | 96,5% | 0,0% | 3,5% | 2,5% |

Tỷ lệ phủ **tổng** trông "đúng 95%", nhưng khoảng sai hình dạng: cận dưới âm (ví dụ một mẫu cho
$\bar y - 1.96s = -1{,}65$ trong khi dữ liệu luôn dương), đuôi trên bị vượt 3,5–4,9% thay vì 2,5% như cam kết.
Nếu quyết định dựa vào cận trên (dự phòng công suất, tồn kho an toàn) thì đó là rủi ro bị đánh giá
thấp. Quantile thực nghiệm 2,5%–97,5% của cùng mẫu phủ 94,0% và không có cận âm.

## 7. Bootstrap

Efron (1979): ước lượng phân phối lấy mẫu của một thống kê bằng cách **lấy mẫu lại có hoàn lại** từ
chính dữ liệu, không cần công thức. `scipy.stats.bootstrap` làm đúng việc này (mặc định `method='BCa'`,
`n_resamples=9999`), với mỗi lần lấy "a random sample of the original sample (with replacement)" — tức
là giả định các quan sát **độc lập**.

**Vì sao bootstrap thường hỏng trên chuỗi thời gian.** Politis (2003): áp bootstrap i.i.d. lên dữ liệu
phụ thuộc thì "inconsistency follows" vì việc xáo trộn "all dependence information is lost".
**Moving block bootstrap** (Künsch, 1989) sửa bằng cách chọn lại cả **khối** $l$ quan sát liền nhau, giữ
được cấu trúc phụ thuộc trong khối. **Stationary bootstrap** (Politis & Romano, 1994) cho độ dài khối
ngẫu nhiên.

Mô phỏng: AR(1) $\rho = 0.7$, $n = 200$, trung bình thật bằng 0; khoảng 95% cho trung bình bằng
percentile bootstrap, $B = 999$, lặp 400 lần (seed 2026):

| Cách lấy mẫu lại | Tỷ lệ khoảng chứa trung bình thật |
|---|---|
| i.i.d. | **59,3%** |
| moving block, $l = 20$ | 87,0% |

Block bootstrap tốt hơn rõ nhưng vẫn dưới 95% — độ dài khối là một lựa chọn phải kiểm, không có giá trị
đúng cho mọi chuỗi.

## 8. Hồi quy và R²

Hồi quy tuyến tính OLS ước lượng hệ số làm nhỏ nhất tổng bình phương phần dư. Khi đọc kết quả hồi quy
trên chuỗi thời gian, nhớ hai câu của FPP (mục 7.3):

- R² "is used frequently, though often incorrectly, in forecasting. The value of R² will never
  decrease when adding an extra predictor to the model and this can lead to over-fitting." Kiểm tra
  mô hình trên dữ liệu test "is much better than measuring the R² value on the training data".
- "High R² and high residual autocorrelation can be signs of spurious regression" — hai chuỗi cùng có
  xu hướng dễ cho R² cao mà không liên quan gì nhau (buổi 8, 18).

## 9. Bẫy thường gặp

| Bẫy | Vì sao sai | Thay bằng |
|---|---|---|
| Dự báo "trung bình" khi quyết định chịu chi phí bất đối xứng | trung bình chỉ tối ưu cho sai số bình phương | quantile mức theo tỷ lệ chi phí (buổi 40) |
| Khoảng $\bar y \pm 1.96s$ cho dữ liệu lệch | cận dưới vô nghĩa, đuôi trên bị vượt nhiều hơn cam kết | quantile thực nghiệm, biến đổi log, mô hình phân phối lệch |
| Giả định Poisson cho dữ liệu đếm mà không kiểm | nếu phương sai lớn hơn trung bình, khoảng dự báo quá hẹp | kiểm tỷ lệ phương sai/trung bình; âm nhị thức |
| Tin CLT với $n$ lớn trên dữ liệu đuôi dày | không có phương sai hữu hạn thì CLT không áp dụng | quantile, trung vị, mô hình đuôi (buổi 25) |
| Coi $n$ quan sát chuỗi thời gian như $n$ quan sát độc lập | $n_{\text{eff}}$ nhỏ hơn nhiều khi tự tương quan dương | tính $n_{\text{eff}}$, block bootstrap |
| Bootstrap i.i.d. trên chuỗi thời gian | khoảng quá hẹp (59% thay vì 95% trong mô phỏng) | moving block / stationary bootstrap |
| Nhầm khoảng tin cậy với khoảng dự báo | khoảng tin cậy cho tham số hẹp hơn nhiều | khoảng dự báo cho giá trị tương lai |
| R² cao → mô hình dự báo tốt | R² đo trên dữ liệu huấn luyện, không giảm khi thêm biến | sai số trên dữ liệu test, backtest (buổi 15) |

## Nguồn

Truy cập ngày 2026-09-17. Nhật ký research: `tools/NGHIEN-CUU.md`.

- Hyndman, R.J. & Fan, Y. (1996). Sample quantiles in statistical packages. *The American Statistician* 50(4), 361–365.
- NumPy `quantile`: <https://numpy.org/doc/stable/reference/generated/numpy.quantile.html>
- Gneiting, T. (2011). Making and evaluating point forecasts. *JASA* 106(494), 746–762. <https://arxiv.org/abs/0912.0902>
- SciPy `poisson`, `nbinom`, `bootstrap`: <https://docs.scipy.org/doc/scipy/reference/stats.html>
- NIST/SEMATECH e-Handbook — Poisson, t, Cauchy: <https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm>,
  <https://www.itl.nist.gov/div898/handbook/eda/section3/eda3664.htm>, <https://www.itl.nist.gov/div898/handbook/eda/section3/eda3663.htm>
- MIT OCW 6.436J, Lecture 17 (CLT): <https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/>
- MIT OCW 18.05, Class 10 (MLE): <https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/>
- Bretherton, C.S. et al. (1999). The effective number of spatial degrees of freedom of a time-varying field. *J. Climate* 12(7), 1990–2009 (qua tài liệu xskillscore `effective_sample_size`).
- Hyndman, R.J. — The difference between prediction intervals and confidence intervals (Hyndsight): <https://robjhyndman.com/hyndsight/intervals/>
- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way* — mục 5.5, 7.3, 9.8, chương 10: <https://otexts.com/fpppy/>
- Efron, B. (1979). Bootstrap methods: another look at the jackknife. *Annals of Statistics* 7(1), 1–26.
- Künsch, H.R. (1989). The jackknife and the bootstrap for general stationary observations. *Annals of Statistics* 17(3), 1217–1241.
- Politis, D.N. & Romano, J.P. (1994). The stationary bootstrap. *JASA* 89(428), 1303–1313.
- Politis, D.N. (2003). The impact of bootstrap methods on time series analysis: <https://mathweb.ucsd.edu/~politis/impactBOOT.pdf>
