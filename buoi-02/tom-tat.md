# Buổi 2 — Tóm tắt: Xác suất và thống kê cho dự báo

**Mục tiêu đầu bài:** tính tay quantile, trung vị, trung bình, độ lệch chuẩn, hệ số tương quan $r$; biết 1,96 từ đâu
ra và đo tỷ lệ phủ thật của khoảng "95%"; đọc một kiểm định giả thuyết; biết vì sao chuỗi thời gian cần block bootstrap.

Ví dụ xuyên suốt: lượt thuê xe của 9 giờ đêm, xếp tăng: **2, 3, 5, 6, 8, 9, 12, 18, 36**.

---

## 1. Mô tả một phân phối (distribution): vị trí (location), độ phân tán (spread), hình dạng (shape)

**Kết luận của phần.** Một phân phối được mô tả bằng ba đặc trưng:

- **vị trí** (location): trung bình (mean), trung vị (median);
- **độ phân tán** (spread, dispersion): độ lệch chuẩn (standard deviation);
- **hình dạng** (shape): đối xứng (symmetric) hay lệch (skewed).

Con số nên báo làm dự báo không cố định: nó do hàm mất mát (loss function) quyết định.

### Phân phối (distribution)

- **Định nghĩa.** Phân phối của một biến ngẫu nhiên (random variable) mô tả các giá trị biến đó có thể nhận và tần suất xuất hiện của
  từng giá trị.
- **Giải thích.** Dự báo "17h mai có 400 lượt" chỉ là một con số. Phân phối trả lời câu hỏi đầy đủ hơn: có thể là bao
  nhiêu lượt, và mỗi mức xảy ra thường tới đâu.
- **Ví dụ.** Lượt thuê lúc 17h: dưới 100 lượt hiếm gặp, quanh 400 lượt hay gặp.
- **Cách diễn giải hình dạng.**
  - *Đối xứng* (symmetric): hai phía quanh tâm giống nhau.
  - *Lệch phải* (right-skewed; đuôi phải dài — long right tail): phần lớn giá trị nhỏ, một số ít rất lớn. Dãy ví dụ lệch phải vì có số 36; lượt thuê
    xe cũng lệch phải.
  - *Lệch trái* (left-skewed; đuôi trái dài — long left tail): ngược lại.
- **Vai trò trong dự báo.** Phân phối là nền của khoảng dự báo, của việc chọn quantile theo chi phí, và của dự báo phân
  phối. Hình dạng quyết định công thức nào dùng được: phân phối lệch làm khoảng ±1,96s sai (phần 3).
- **Phân biệt.**
  - Phân phối không phải một con số dự báo.
  - *Phân phối thực nghiệm* (empirical distribution) được dựng từ **mẫu** (sample) đang có; nó chỉ xấp xỉ
    phân phối thật của **tổng thể** (population).

### Histogram

- **Định nghĩa.** Biểu đồ cột: chia trục giá trị thành các khoảng (bin) bằng nhau, rồi đếm số quan sát rơi vào mỗi khoảng.
- **Ví dụ.** Dãy 9 số: 0–9 có 6 số, 10–19 có 2 số, 20–29 có 0 số, 30–39 có 1 số.
- **Cách diễn giải.** Histogram trả lời bốn câu hỏi: dữ liệu tập trung ở đâu, tản rộng cỡ nào, có đối xứng không, có
  giá trị ngoại lai (outlier) không. Cột cao bên trái rồi thấp dần sang phải là lệch phải.
- **Tính chất.** Hình dạng nhìn thấy phụ thuộc độ rộng cột (bin width): cột quá rộng che mất chi tiết, cột quá hẹp thì lởm chởm.

### Hàm phân phối tích luỹ (cumulative distribution function, CDF), $F(y)$

- **Định nghĩa.** $F(y)$ là tỷ lệ quan sát nhỏ hơn hoặc bằng $y$:
  $$F(y) = \frac{\text{số giá trị} \le y}{n}$$
- **Ví dụ.** $F(8) = 5/9 \approx 0{,}56$, vì 5 trong 9 số (2, 3, 5, 6, 8) nhỏ hơn hoặc bằng 8.
- **Tính chất.** $F$ không giảm, đi từ 0 tới 1.
- **Cách diễn giải.** Đoạn dốc là vùng giá trị dày đặc. Đoạn gần phẳng là vùng thưa.
- **Vai trò.** Đọc xuôi (từ mốc ra tỷ lệ) được $F$. Đọc ngược (từ tỷ lệ ra mốc) được quantile.

### Quantile $q_p$

- **Định nghĩa.** Quantile mức $p$ là giá trị nhỏ nhất mà ít nhất tỷ lệ $p$ số quan sát nhỏ hơn hoặc bằng nó:
  $$q_p = \min\{\, y : F(y) \ge p \,\}$$
- **Giải thích.** Quantile là mốc chia dữ liệu: tỷ lệ $p$ nằm dưới hoặc tại mốc, phần còn lại nằm trên.
  **Percentile** là cùng khái niệm viết theo phần trăm: quantile 0,8 = percentile 80.
- **Ví dụ.** Tính tay: xếp tăng dần, lấy vị trí $p \times n$, làm tròn lên. Với $q_{0,8}$: 0,8 × 9 = 7,2 → vị trí 8 → **18**.
  Kiểm lại bằng $F$: $F(12) = 0{,}78$ chưa đủ 0,8, còn $F(18) = 0{,}89$ thì đủ.
- **Tính chất.**
  - $q_p$ không giảm khi $p$ tăng. $q_{0,1}$ nằm ở đuôi trái, $q_{0,9}$ ở đuôi phải.
  - Quantile chỉ phụ thuộc thứ tự của dữ liệu. Đổi 36 thành 360 thì $q_{0,5}$ và $q_{0,8}$ đều không đổi.
  - Có nhiều quy ước tính quantile từ mẫu (sample quantile; Hyndman & Fan, 1996). NumPy mặc định **nội
    suy** (linear interpolation) giữa hai số kề nhau, nên
    `np.quantile` ra **14,4**. Tham số `method="inverted_cdf"` cho **18**, khớp cách tính tay.
- **Vai trò trong dự báo.**
  - Khi thiếu và thừa đắt khác nhau, con số tối ưu là quantile $C_u/(C_u + C_o)$.
  - Khoảng dự báo 95% dựng từ $q_{0,025}$ và $q_{0,975}$.
- **Phân biệt.** Quantile 0,8 **không phải** 80% của giá trị lớn nhất (0,8 × 36 = 28,8).

### Trung vị (median)

- **Định nghĩa.** Trung vị là quantile 0,5: giá trị đứng giữa dãy đã xếp.
- **Ví dụ.** Dãy 9 số có trung vị **8**. Dãy có số lượng chẵn thì có hai số đứng giữa: đếm tay lấy số thứ $n/2$, còn
  `np.median` lấy trung bình hai số giữa. Hai cách khác nhau ở quy ước, không phải ở ý nghĩa.
- **Tính chất.** Trung vị **bền với giá trị ngoại lai** (robust to outliers): vài giá trị cực đoan không kéo được nó.
- **Vai trò trong dự báo.** Trung vị là con số tối ưu khi phạt thiếu và thừa như nhau (sai số tuyệt đối — absolute error, MAE).
- **Phân biệt.** Trung vị khác trung bình. Khoảng cách giữa hai số này cho biết hình dạng phân phối (xem Trung bình).

### Trung bình (mean)

- **Định nghĩa.** Tổng các giá trị chia cho số giá trị:
  $$\bar y = \frac1n \sum_{i=1}^n y_i$$
- **Ví dụ.** 99/9 = **11**.
- **Tính chất.** Trung bình **nhạy với giá trị ngoại lai**: nó bị kéo về phía các giá trị cực đoan.
- **Cách diễn giải (so với trung vị).**

  | Quan hệ | Hình dạng | Ví dụ |
  |---|---|---|
  | trung bình > trung vị | lệch phải | 11 > 8; dữ liệu thật 189 > 142 |
  | trung bình ≈ trung vị | gần đối xứng | |
  | trung bình < trung vị | lệch trái | |

- **Vai trò trong dự báo.** Trung bình là con số tối ưu khi phạt theo bình phương sai số (squared error).

### Độ lệch chuẩn (standard deviation) $s$ và phương sai (variance) $s^2$

- **Định nghĩa.**
  $$s^2 = \frac{1}{n-1}\sum_{i=1}^n (y_i - \bar y)^2, \qquad s = \sqrt{s^2}$$
- **Giải thích.** $s$ là khoảng cách điển hình từ một giá trị tới trung bình, cùng đơn vị với dữ liệu. Phương sai $s^2$
  có đơn vị bình phương nên khó đọc trực tiếp.
- **Ví dụ.** Tổng bình phương độ lệch là 894. Chia 8 được $s^2 = 111{,}75$, nên $s \approx$ **10,57** lượt.
- **Cách diễn giải.** $s = 0$ khi mọi giá trị bằng nhau. $s$ càng lớn thì dữ liệu càng phân tán, và khoảng dự báo càng
  phải rộng.
- **Tính chất.** $s$ nhạy với ngoại lai, vì độ lệch bị bình phương. Riêng số 36 (lệch +25) góp 625 trong tổng 894.
- **Phân biệt $s$ và $\sigma$.**
  - $s$ chia cho $n-1$ (sample standard deviation): ước lượng từ một mẫu.
  - $\sigma$ chia cho $n$ (population standard deviation): dùng khi đang có cả tổng thể. Với ví dụ trên, $\sigma$ = 9,97.
  - Trong code phải ghi rõ `ddof`: `np.std` mặc định chia $n$, pandas mặc định chia $n-1$.

### Hệ số lệch (skewness)

- **Định nghĩa.** Hệ số lệch là trung bình của (độ lệch / $s$)³. Nó đo mức độ **thiếu đối xứng** (asymmetry) của phân phối.
- **Ví dụ.** Dãy 9 số có hệ số lệch **+1,35**.
- **Cách diễn giải.**
  - Dương: lệch phải.
  - Âm: lệch trái.
  - Gần 0: gần đối xứng.
- **Tính chất.**
  - Hệ số lệch rất nhạy với ngoại lai, vì phép lập phương giữ dấu và phóng đại số lớn. Riêng số 36 góp gần hết giá trị.
  - scipy và pandas dùng quy ước hơi khác nhau, nhưng luôn cùng dấu.
- **Vai trò trong dự báo.** Hệ số lệch khác 0 rõ rệt là dấu hiệu không nên dùng các công thức giả định phân phối chuẩn,
  như khoảng ±1,96s.
- **Phân biệt.** Hệ số lệch đo **hình dạng**. Độ lệch chuẩn đo **độ rộng**. Tên gần giống nhau nhưng là hai đại lượng
  khác nhau.

### Hàm mất mát (loss function)

- **Định nghĩa.** Hàm mất mát là quy tắc tính mức phạt cho một dự báo $c$ khi giá trị thật là $y$.
- **Tính chất then chốt.** Mỗi hàm mất mát có một con số tối ưu riêng.

  | Hàm mất mát | Công thức | Con số tối ưu |
  |---|---|---|
  | bình phương | $(y-c)^2$ | trung bình |
  | tuyệt đối | $\lvert y-c \rvert$ | trung vị |
  | pinball loss mức $\tau$ | thiếu: $\tau(y-c)$; thừa: $(1-\tau)(c-y)$ | quantile $\tau$ |

- **Ví dụ.** Với dãy 9 số, phạt trung bình nhỏ nhất ở:
  - $c$ = 8 khi phạt tuyệt đối;
  - $c$ = 11 khi phạt bình phương;
  - $c$ = 18 khi phạt pinball 0,8.
- **Cách diễn giải $\tau$.** $\tau$ lớn thì thiếu bị phạt nặng hơn thừa, nên con số tối ưu dịch lên cao.
  - $\tau$ = 0,8: thiếu đắt gấp 0,8/0,2 = 4 lần thừa, đúng bài toán chi phí lệch của buổi 1.
  - $\tau$ = 0,5: thiếu và thừa như nhau, pinball tương đương sai số tuyệt đối.
- **Vai trò trong dự báo.** Phải biết dự báo sẽ bị chấm bằng hàm mất mát nào trước khi chọn con số để báo.

---

## 2. Tương quan (correlation)

**Kết luận của phần.** $r$ đo hai đại lượng cùng tăng giảm **theo đường thẳng** tới đâu. $r$ không đo được quan hệ
cong, và $r$ lớn không chứng minh nhân quả.

### Hệ số tương quan Pearson (correlation coefficient) $r$

- **Định nghĩa.**
  $$r = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum (x_i-\bar x)^2 \cdot \sum (y_i-\bar y)^2}}$$
- **Giải thích.**
  - Tử số cộng các tích độ lệch. Tích dương khi hai đại lượng cùng lệch về một phía so với trung bình của chúng.
  - Mẫu số chuẩn hoá để $r$ luôn nằm trong đoạn [−1; 1].
- **Ví dụ.** 5 ngày, nhiệt độ 10, 15, 20, 25, 30 °C và lượt thuê 40, 60, 50, 90, 110 trăm lượt.
  $r = 850/\sqrt{250 \times 3.400} \approx$ **0,922**.
- **Cách diễn giải.**
  - Dấu dương: quan hệ **cùng chiều**. Dấu âm: **ngược chiều**.
  - $\lvert r \rvert$ gần 1: quan hệ tuyến tính (linear) mạnh. Gần 0: không có quan hệ **tuyến tính**.
  - Ví dụ thật: nhiệt độ × lượt thuê $r$ = 0,405; độ ẩm × lượt thuê $r$ = −0,323.
- **Tính chất.** $r$ không đổi khi đổi đơn vị, vì tử số và mẫu số cùng nhân lên.
- **Vai trò trong dự báo.** $r$ giúp sàng lọc biến giải thích (explanatory variable): biến có tương quan với $y$ có thể giúp dự báo $y$.
- **Phân biệt.**
  - $r = 0$ không có nghĩa là không liên quan. Với $y = x^2$ thì $r = 0$, dù $y$ hoàn toàn do $x$ quyết định.
  - Tương quan không phải nhân quả (correlation is not causation).

### Biến gây nhiễu (confounder)

- **Định nghĩa.** Biến thứ ba tác động lên cả hai đại lượng, làm chúng trông như có liên quan với nhau.
- **Ví dụ.** Bán kem và số vụ đuối nước tương quan dương, vì cả hai cùng tăng khi trời nóng.
- **Cách diễn giải.** Biến gây nhiễu có thể làm $r$ mạnh lên hoặc yếu đi. Giờ trong ngày gây nhiễu các tương quan với
  lượt thuê. Giữ cố định giờ (chỉ xét 17h) thì:
  - nhiệt độ × lượt thuê tăng từ 0,405 lên 0,588;
  - độ ẩm × lượt thuê yếu đi, từ −0,323 còn −0,253.
- **Vai trò trong dự báo.** Một biến không gây ra $y$ vẫn có thể giúp dự báo $y$. Nhưng muốn **can thiệp** thì phải
  phân biệt nhân quả với tương quan.
- **Cách kiểm tra.** Tính $r$ trong từng nhóm của biến nghi gây nhiễu, ví dụ từng giờ trong ngày.

### Tự tương quan (autocorrelation)

- **Định nghĩa.** Tương quan của một chuỗi với chính nó khi dời lùi $k$ bước. $k$ gọi là **độ trễ** (lag).
- **Ví dụ.** Chuỗi 1, 3, 1, 3 có tự tương quan trễ 1 là −0,75, tức lên xuống xen kẽ.
- **Cách diễn giải.**
  - Dương cao: giá trị cao thường đi liền giá trị cao.
  - Âm: giá trị cao và thấp xen kẽ nhau.
  - Lượt thuê theo giờ có tự tương quan trễ 1 là **0,844**.
- **Vai trò trong dự báo.**
  - Tự tương quan là nguồn thông tin để dự báo: quá khứ gần nói lên tương lai gần.
  - Nó cũng phá các phương pháp giả định quan sát độc lập (phần 5).
- **Phân biệt.** Mẫu số của tự tương quan là tổng bình phương độ lệch của **cả chuỗi**, không như $r$. Vì vậy chuỗi
  ngắn có thể không ra đúng ±1.

---

## 3. Con số 1,96 và tỷ lệ phủ (coverage) thật của khoảng "95%"

**Kết luận của phần.** 1,96 là quantile 0,975 của phân phối chuẩn, nên khoảng ±1,96s chỉ đúng khi dữ liệu có hình
chuông. Khoảng "95%" chỉ đáng tin khi đã **đo tỷ lệ phủ ngoài mẫu và tách hai đuôi**.

### Phân phối chuẩn (normal distribution) và hệ số 1,96

- **Định nghĩa.** Phân phối chuẩn là phân phối liên tục hình chuông, đối xứng quanh trung bình. Nó được xác định hoàn
  toàn bởi trung bình và độ lệch chuẩn.
- **Tính chất.**

  | Khoảng quanh trung bình | Tỷ lệ giá trị nằm trong |
  |---|---|
  | ± 1 độ lệch chuẩn | 68,3% |
  | ± 1,96 độ lệch chuẩn | 95,0% |
  | ± 2 độ lệch chuẩn | 95,4% |

- **Giải thích 1,96.** 1,96 là quantile 0,975 của phân phối chuẩn tắc (standard normal; trung bình 0, độ lệch chuẩn 1). Phần ở giữa
  chiếm 95%, mỗi đuôi (tail) còn 2,5%. Kiểm bằng máy: `norm.ppf(0.975)` = 1,95996.
- **Phân biệt.** 1,96 không phải hằng số vạn năng. Với dữ liệu lệch, khoảng ±1,96s sai: dãy 9 số cho cận dưới
  11 − 1,96 × 10,57 = **−9,7** lượt, một giá trị vô lý.

### Khoảng dự báo (prediction interval)

- **Định nghĩa.** Khoảng dự báo mức 95% là khoảng được kỳ vọng chứa giá trị **tương lai** với xác suất 95%.
- **Cách dựng.**

  | Cách | Công thức | Điều kiện đúng |
  |---|---|---|
  | tham số (parametric) | $\bar y \pm 1{,}96\,s$ | dữ liệu gần phân phối chuẩn |
  | quantile thực nghiệm (empirical quantile) | $[q_{0,025};\, q_{0,975}]$ | quá khứ đại diện cho tương lai |

- **Ví dụ.** Lượt thuê lúc 17h năm 2011:
  - cách tham số cho [22; 678];
  - cách quantile cho [65; 604]. Cận dưới cao hơn, cận trên thấp hơn, đúng với hình lệch phải.
- **Cách diễn giải.** Khoảng rộng thì an toàn nhưng ít giúp ra quyết định. Khoảng hẹp thì hữu ích nhưng dễ trượt.
  Phải đo tỷ lệ phủ mới biết khoảng giữ lời hay không.

### Tỷ lệ phủ (coverage)

- **Định nghĩa.** Tỷ lệ số lần giá trị thật rơi vào khoảng dự báo.
- **Ví dụ.** Khoảng [4; 20], 10 giá trị thật 3, 7, 12, 15, 9, 30, 11, 6, 2, 25:
  - 6/10 = **60%** nằm trong khoảng;
  - 20% rơi dưới cận dưới, 20% vượt cận trên.
- **Cách diễn giải.**
  - Tỷ lệ phủ **thấp hơn** mức danh nghĩa (nominal level): khoảng quá hẹp hoặc đặt lệch chỗ.
  - **Cao hơn** nhiều: khoảng quá rộng.
  - **Hai đuôi:** khoảng 95% tốt để khoảng 2,5% rơi dưới và 2,5% vượt trên. Một đuôi gần 0% còn đuôi kia lớn nghĩa là
    cả khoảng đặt lệch về phía đuôi gần 0%.
- **Vai trò trong dự báo.** Tỷ lệ phủ là thước đo kiểm tra lời hứa của khoảng dự báo. Luôn báo kèm hai đuôi.

| Dựng từ 2011 | Chấm trên | Phủ | Dưới | Trên |
|---|---|---|---|---|
| ±1,96s | 2011 (trong mẫu) | 96,4% | 0,3% | 3,3% |
| quantile thực nghiệm | 2011 (trong mẫu) | 95,3% | 2,2% | 2,6% |
| ±1,96s | 2012 (ngoài mẫu) | 72,5% | 0,1% | 27,4% |
| quantile thực nghiệm | 2012 (ngoài mẫu) | 70,1% | 0,5% | 29,3% |

**Đọc bảng.**

- **Trong mẫu:** ±1,96s sai hình dạng, vì đuôi dưới gần như không bị vượt. Quantile thực nghiệm cân lại được hai đuôi.
- **Ngoài mẫu:** cả hai cách đều vỡ, do dịch mức.

### Trong mẫu (in-sample) và ngoài mẫu (out-of-sample)

- **Định nghĩa.** *Trong mẫu*: đánh giá trên chính dữ liệu đã dùng để dựng dự báo. *Ngoài mẫu*: đánh giá trên dữ liệu
  chưa dùng.
- **Cách diễn giải.** Kết quả trong mẫu thường đẹp hơn thực tế. Chỉ kết quả ngoài mẫu phản ánh chất lượng khi dùng thật.
- **Ví dụ.** Khoảng ±1,96s phủ 96,4% trong mẫu, nhưng chỉ 72,5% ngoài mẫu.

### Dịch mức (level shift)

- **Định nghĩa.** Mức trung bình của chuỗi thay đổi hẳn rồi giữ ở mức mới.
- **Ví dụ.** Lượt thuê trung bình mỗi giờ tăng từ 143,8 (2011) lên 234,7 (2012). Vì vậy gần 3 trên 10 giờ năm 2012
  vượt cận trên của khoảng dựng từ 2011.
- **Vai trò trong dự báo.** Dịch mức vi phạm giả định "tương lai giống quá khứ". Không cách dựng khoảng nào từ lịch sử
  cũ sửa được nó; cần mô hình theo dõi mức hoặc xu hướng.

### Khoảng tin cậy (confidence interval)

- **Định nghĩa.** Khoảng tin cậy mức 95% là khoảng dựng từ mẫu cho **một tham số cố định chưa biết** (ví dụ trung bình
  thật). Quy trình dựng khoảng này, lặp lại nhiều lần, chứa tham số thật trong 95% số lần.
- **Ví dụ.** Rút 20 mẫu, mỗi mẫu 100 giờ, từ năm 2012 (trung bình thật 234,7). 19 khoảng chứa 234,7; khoảng thứ 20
  là [148,1; 231,8], không chứa.
- **Cách diễn giải.** "95%" nói về **quy trình**, không nói một khoảng cụ thể có 95% khả năng đúng.
- **Phân biệt với khoảng dự báo.**

  | | Cho đại lượng nào | Khi thêm dữ liệu |
  |---|---|---|
  | khoảng dự báo | một giá trị tương lai chưa quan sát | không co về 0 |
  | khoảng tin cậy | một tham số cố định (trung bình thật) | co hẹp dần |

---

## 4. Đọc một kiểm định giả thuyết (hypothesis test)

**Kết luận của phần.** Kiểm định trả lời câu hỏi: nếu $H_0$ đúng, dữ liệu như vậy hiếm cỡ nào? p-value nhỏ hơn mức ý
nghĩa thì bác bỏ $H_0$. Không bác bỏ thì chưa kết luận được gì.

### Kiểm định giả thuyết (hypothesis test) — phương pháp

- **Mục đích.** Quyết định dữ liệu có đủ bằng chứng để bác bỏ một giả định mặc định hay không.
- **Quy trình.**
  1. Phát biểu $H_0$.
  2. Chọn đại lượng kiểm định (test statistic).
  3. Tính p-value.
  4. So p-value với $\alpha$ đã chọn trước.
- **Ví dụ.** Tung đồng xu 10 lần được 9 ngửa.
  - $H_0$: đồng xu cân đối.
  - p = 11/1.024 ≈ 0,011 < 0,05, nên bác bỏ $H_0$.
  - Nếu chỉ được 7 ngửa: p ≈ 0,17, không bác bỏ.
- **Một phía (one-sided) và hai phía (two-sided).** Chỉ dùng kiểm định một phía khi hướng đã định trước khi xem dữ liệu. Mặc định của khoá là
  hai phía.
- **Nhược điểm.** p-value không nói gì về độ lớn của khác biệt.

### Giả thuyết không (null hypothesis) $H_0$

- **Định nghĩa.** Giả định mặc định "không có gì đặc biệt", mà kiểm định tìm cách bác bỏ.
- **Ví dụ.** "Đồng xu cân đối"; "nhãn ngày làm việc hay ngày nghỉ không liên quan tới lượt thuê".
- **Phân biệt.** Không bác bỏ $H_0$ **không phải** chứng minh $H_0$ đúng. Có thể chỉ là dữ liệu quá ít.

### p-value

- **Định nghĩa.** Giả sử $H_0$ đúng, p-value là xác suất gặp kết quả lệch bằng hoặc hơn kết quả quan sát được.
- **Cách diễn giải.**
  - p nhỏ: dữ liệu khó xảy ra dưới $H_0$, tức bằng chứng chống $H_0$ mạnh.
  - p lớn: bằng chứng chưa đủ.
- **Tính chất.** p phụ thuộc cỡ mẫu:

  | So sánh năm 2012 | Số ngày mỗi nhóm | Chênh lệch | p |
  |---|---|---|---|
  | ngày làm việc − ngày nghỉ | 250 và 116 | +456 lượt/ngày | 0,025 |
  | thứ Bảy − Chủ nhật | 52 và 53 | +695 lượt/ngày | 0,078 |

  Chênh lệch lớn hơn mà p cũng lớn hơn, vì nhóm ít ngày hơn.
- **Phân biệt.**
  - p-value **không phải** xác suất $H_0$ đúng (Hội Thống kê Hoa Kỳ, 2016).
  - Có ý nghĩa thống kê **không có nghĩa** khác biệt lớn.

### Mức ý nghĩa (significance level) $\alpha$

- **Định nghĩa.** Ngưỡng chọn **trước** khi xem dữ liệu. p < $\alpha$ thì bác bỏ $H_0$. Thường dùng 0,05.
- **Cách diễn giải.** $\alpha$ càng nhỏ thì càng đòi bằng chứng mạnh mới bác bỏ.

### Kiểm định hoán vị (permutation test) — phương pháp

- **Mục đích.** Kiểm định hai nhóm có khác nhau không, mà không cần giả định dạng phân phối (phi tham số — non-parametric).
- **Quy trình.**
  1. Tính chênh lệch thật giữa hai nhóm.
  2. Xáo ngẫu nhiên nhãn nhóm $B$ lần. Đếm số lần $k$ mà chênh lệch (bỏ dấu) lớn bằng hoặc hơn chênh lệch thật.
  3. Tính $p = (k+1)/(B+1)$.
- **Ví dụ.** Ngày làm việc so với ngày nghỉ năm 2012: xáo 9.999 lần, có 253 lần lệch bằng hoặc hơn 456, nên
  p = 254/10.000 ≈ 0,025.
- **Giả định.** Các quan sát độc lập.
- **Ưu điểm.** Trực quan, không cần công thức phân phối.
- **Khi nào hỏng.** Dữ liệu tự tương quan: ngày đông hay đi liền ngày đông (tự tương quan trễ 1 là 0,748). Khi đó
  p-value thật thường **lớn hơn** số tính được.
- **Lưu ý.** Cộng 1 ở tử và mẫu để p không bao giờ bằng 0.

---

## 5. Vì sao chuỗi thời gian cần block bootstrap

**Kết luận của phần.** Quan sát tự tương quan chứa ít thông tin hơn quan sát độc lập. Bootstrap rút từng điểm bỏ qua
điều này, nên cho khoảng tin cậy quá hẹp. Block bootstrap rút cả khối liền nhau để giữ lại phụ thuộc, nhưng kết quả
nhạy với độ dài khối.

### i.i.d. (independent and identically distributed)

- **Định nghĩa.** Các quan sát **độc lập** (independent: biết lần này không giúp đoán lần kia) và **cùng phân phối**
  (identically distributed).
- **Ví dụ.** Các lần tung một xúc xắc là i.i.d. Lượt thuê của các giờ liền nhau thì không.
- **Vai trò.** Là giả định của CLT, của bootstrap thường và của kiểm định hoán vị.

### Định lý giới hạn trung tâm (central limit theorem, CLT) và sai số chuẩn (standard error) $\sigma/\sqrt n$

- **Định nghĩa.** Với dữ liệu i.i.d., trung bình mẫu có phân phối gần chuẩn, với độ lệch chuẩn $\sigma/\sqrt n$.
- **Ví dụ.** Mô phỏng trên lượt thuê ($\sigma$ = 181,4): độ lệch chuẩn của trung bình mẫu là 36,1 với $n$ = 25, và 18,2
  với $n$ = 100. Hai số này khớp $\sigma/\sqrt n$ (36,3 và 18,1).
- **Cách diễn giải.** Tăng $n$ gấp 4 thì độ dao động chỉ giảm một nửa.
- **Vai trò.** Là cơ sở của khoảng tin cậy trung bình mẫu ± $1{,}96\, s/\sqrt n$.

### Mô hình tự hồi quy (autoregressive model) AR(1)

- **Ý tưởng.** Giá trị hiện tại bằng một phần giá trị ngay trước nó, cộng một cú hích ngẫu nhiên mới.
- **Kiến trúc.**
  $$x_t = \rho\, x_{t-1} + \varepsilon_t$$
  - Tham số (parameter) $\rho$ trong khoảng (−1; 1), bằng tự tương quan trễ 1.
  - $\varepsilon_t$: nhiễu (noise), i.i.d., trung bình 0.
- **Ví dụ.** $\rho$ = 0,7, giá trị trước 10, cú hích 0,5 → 0,7 × 10 + 0,5 = 7,5.
- **Điểm đặc biệt.** Là mô hình đơn giản nhất cho tự tương quan: chỉ một tham số, và từ đó suy ra được công thức cỡ mẫu
  hiệu dụng.
- **Ưu điểm.** Dễ mô phỏng. Ở buổi này, AR(1) dùng để tạo chuỗi có tự tương quan đã biết, rồi kiểm tra bootstrap trên
  đó.
- **Nhược điểm.** Chỉ nhớ đúng một bước trước. Không mô tả được mùa vụ hay xu hướng.
- **Khi nào dùng.** Làm chuỗi thử nghiệm cho các phương pháp thống kê trên dữ liệu phụ thuộc.

### Cỡ mẫu hiệu dụng (effective sample size) $n_{\text{eff}}$

- **Định nghĩa.** Số quan sát độc lập có lượng thông tin tương đương $n$ quan sát tự tương quan. Với AR(1):
  $$n_{\text{eff}} \approx n\,\frac{1-\rho}{1+\rho}$$
- **Ví dụ.** $\rho$ = 0,7, $n$ = 200 → $n_{\text{eff}} \approx 35$.
- **Cách diễn giải.**
  - $\rho$ = 0 thì $n_{\text{eff}} = n$. $\rho$ tiến về 1 thì $n_{\text{eff}}$ tiến về 0.
  - Khoảng tin cậy đúng rộng gấp khoảng $\sqrt{n/n_{\text{eff}}}$ lần khoảng tính như i.i.d. Với ví dụ trên:
    $\sqrt{200/35} \approx 2{,}4$.
- **Phân biệt.** Tỷ lệ độ rộng có **căn bậc hai**. Quên căn là lỗi hay gặp.

### Bootstrap — phương pháp

- **Mục đích.** Ước lượng độ dao động (sampling variability) của một thống kê (statistic) (ví dụ trung bình) khi chỉ có một mẫu.
- **Quy trình.**
  1. Lấy mẫu lại (resample) **có hoàn lại** (with replacement), cùng cỡ với mẫu gốc.
  2. Tính thống kê trên mẫu lại.
  3. Lặp vài nghìn lần.
  4. Lấy quantile 0,025 và 0,975 của các kết quả, được khoảng tin cậy 95% kiểu percentile (percentile interval).
- **Vì sao đúng.** Mẫu ngẫu nhiên là bức ảnh thu nhỏ của tổng thể. Kiểm bằng mô phỏng:
  - rút mẫu mới từ tổng thể cho độ lệch chuẩn của trung bình 21,2;
  - bootstrap từ một mẫu 100 giờ cho 21,0.
- **Giả định.** Quan sát i.i.d.
- **Ưu điểm.** Không cần công thức. Áp dụng được cho nhiều loại thống kê.
- **Khi nào hỏng.** Dữ liệu tự tương quan. Rút từng điểm cắt đứt phụ thuộc, nên khoảng hẹp như tính với $n$ thay vì
  $n_{\text{eff}}$. Trên AR(1) với $\rho$ = 0,7, khoảng 95% chỉ chứa trung bình thật **60,3%** số lần.

### Block bootstrap — phương pháp

- **Mục đích.** Bootstrap cho dữ liệu phụ thuộc (Künsch, 1989).
- **Quy trình.** Rút ngẫu nhiên các khối (block) $l$ điểm liền nhau, nối lại, cắt cho đủ $n$ điểm. $l$ = 1 là bootstrap thường.
- **Ví dụ.** Chuỗi 12, 15, 11, 30, 14, khối dài 2: rút các khối (30, 14), (15, 11), (12, 15) → 30, 14, 15, 11, 12.
  Cặp 30–14 liền nhau được giữ nguyên.
- **Ưu điểm.** Giữ được phụ thuộc bên trong mỗi khối, nên sửa phần lớn lỗi khoảng quá hẹp.
- **Nhược điểm.** Nhạy với độ dài khối (block length):

  | Độ dài khối | 1 | 3 | 6 | 10 | 20 | 40 |
  |---|---|---|---|---|---|---|
  | Tỷ lệ chứa trung bình thật | 60,3% | 78,7% | 86,3% | 89,0% | 89,3% | 81,3% |

  Số liệu mô phỏng trên AR(1), $\rho$ = 0,7, $n$ = 200.
  - Khối ngắn: mỗi chỗ nối cắt đứt một phụ thuộc.
  - Khối dài: hai đầu chuỗi hiếm khi vào mẫu, nên các mẫu lại quá giống nhau.
  - Cả hai trường hợp đều cho khoảng hẹp.
- **Khi nào dùng.** Khoảng tin cậy cho thống kê trên chuỗi thời gian. Chọn khối ≈ căn bậc ba của $n$ theo kinh
  nghiệm, và luôn báo độ nhạy theo vài độ dài khối.
- **Khi nào hỏng.** Chuỗi có xu hướng: mỗi khối mang mức của mùa nó được cắt ra, nên khoảng rộng mãi theo độ dài khối.
