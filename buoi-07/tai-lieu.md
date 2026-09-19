# Buổi 7 — Tự tương quan và tính dừng

## 1. Mục tiêu

Sau buổi này bạn:

- Tính tay **ACF** và **PACF** trên vài con số, rồi đọc được hình ACF/PACF của nhiễu trắng, AR(1), random walk và chuỗi có xu hướng.
- Dùng **Ljung-Box** thay cho việc đếm cột ACF vượt dải, và giải thích bằng số vì sao "thế nào cũng có một cột vượt".
- Nói được **dừng** nghĩa là gì bằng ví dụ đời thường, và phân biệt "dừng quanh xu hướng" với "random walk".
- Kết luận dừng / không dừng bằng **cả ADF lẫn KPSS**, đọc được cả bốn ô của bảng 2 × 2.
- Chọn **số lần sai phân** vừa đủ và phát hiện **sai phân thừa** bằng hai dấu hiệu đo được.

## 2. Nhắc lại buổi trước

Từ buổi 4 và 6:

- **ACF**: hệ số tự tương quan $r_k$ theo độ trễ $k$, tức chuỗi giống chính nó dời lùi $k$ bước tới đâu (từ −1 tới 1). Đỉnh ở bội số
  của chu kỳ mùa vụ là dấu hiệu mùa vụ; trễ bằng nửa chu kỳ mùa vụ ghép đỉnh với đáy nên $r$ âm.
- Dải **±1,96/√T** quanh 0 trên hình ACF: vùng mà $r_k$ của một chuỗi hoàn toàn ngẫu nhiên thường rơi vào ($T$ là số điểm).
- **Phân rã** tách xu hướng, mùa vụ, phần dư; phần dư tốt thì không còn mẫu hình.

Từ buổi 2 (xác suất và thống kê) — cần cho mục 4.3 và 4.5:

- **Kiểm định giả thuyết**: đặt một giả định mặc định $H_0$ (giả thuyết không), xem dữ liệu có đủ bằng chứng bác bỏ nó không.
- **p-value**: nếu $H_0$ đúng, xác suất gặp kết quả lệch cỡ này hoặc hơn. Ví dụ đồng xu, $H_0$ "cân đối": được ít nhất 9 ngửa trong 10
  lần có p ≈ 0,011.
- **Mức ý nghĩa** $\alpha$: ngưỡng chọn trước, buổi này dùng 0,05. p nhỏ hơn $\alpha$ thì bác bỏ $H_0$; ví dụ đồng xu bị bác bỏ.
- **Không bác bỏ không có nghĩa là $H_0$ đúng**: chỉ là chưa đủ bằng chứng.
- **AR(1)** (tự hồi quy bậc 1): giá trị mới = $\phi$ × giá trị cũ + một phần ngẫu nhiên. Ví dụ $\phi$ = 0,7: 0,7 × 10 + 0,5 = 7,5.
- **i.i.d.** và **nhiễu**: các lần rút độc lập từ cùng một "hộp"; biết lần này không giúp đoán lần sau.

## 3. Trạng thái đầu buổi

Sau `python lab.py up` (trong thư mục `lab/`):

| Hạng mục | Trạng thái |
|---|---|
| Dữ liệu | `bea-nipa-quy/NipaDataQ.txt` (sha256 `7fa7dfb39b76`): GDP thực Mỹ theo quý, 318 quý 1947Q1 → 2026Q2 |
| | `frb-g17-san-luong-cong-nghiep/g17-2000-2024.csv` (`3956c6626866`): chỉ số sản lượng công nghiệp theo tháng, 300 tháng |
| | `uci-bike-sharing/hour.csv` (`e03de4ee4ef4`): lượt thuê xe theo giờ 2011–2012 |
| Nguồn | U.S. BEA, Federal Reserve Board (public domain); UCI Bike Sharing (CC BY 4.0) |
| Môi trường | Python 3.12; numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0 |
| `code/tu_tuong_quan.py` | `doc_gdp`, `doc_san_luong`, `doc_luot_thue`, `sinh_bon_chuoi`, `acf_tu_viet`, `dai_nhieu_trang`, `ljung_box`, `kiem_dinh`, `ket_luan`, `so_lan_sai_phan`, `dau_hieu_sai_phan_thua`, `bang_bon_chuoi` |
| `code/lab.ipynb` | notebook của Lab, bước 1–5 |
| **Đang cố tình sai** | `kiem_dinh` chỉ chạy **ADF** (không KPSS, không dạng "quanh xu hướng"); `so_lan_sai_phan` **luôn sai phân ít nhất một lần** "cho chắc" |
| **Triệu chứng** | chuỗi dừng quanh một xu hướng bị gọi là "không dừng — cần sai phân"; nhiễu trắng cũng được sai phân một lần |
| `python lab.py check` lúc này | ĐỎ: 5/9 test hỏng |

## 4. Lý thuyết

### Từ mới trong buổi

| Thuật ngữ | Nghĩa một câu | Ví dụ |
|---|---|---|
| PACF (tự tương quan riêng phần) | Tương quan giữa $y_t$ và $y_{t-k}$ **sau khi** bỏ phần đã giải thích được bằng các trễ ngắn hơn. | AR(1): ACF trễ 2 là 0,49 nhưng PACF trễ 2 là 0. |
| nhiễu trắng (white noise) | Chuỗi không có tự tương quan ở trễ nào: quá khứ không giúp đoán tương lai. | Kết quả tung xúc xắc từng lần. |
| Ljung-Box | Kiểm định gộp nhiều $r_k$ thành một con số $Q^*$ để hỏi "đây có phải nhiễu trắng không". | Mục 4.3. |
| bậc tự do | Số "mảnh thông tin độc lập" mà một kiểm định dùng; ở Ljung-Box là số trễ trừ số tham số đã ước lượng. | 10 trễ, mô hình 2 tham số → 8. |
| dừng (stationary) | Tính chất thống kê (mức trung bình, độ dao động, tự tương quan) không đổi theo thời điểm quan sát. | Nhiệt độ phòng có máy lạnh. |
| random walk (bước ngẫu nhiên) | Giá trị mới = giá trị cũ + một bước ngẫu nhiên; không có mức để quay về. | Vị trí của người tung đồng xu, ngửa bước tới, sấp lùi. |
| dừng quanh xu hướng (trend-stationary) | Chuỗi = một đường xu hướng cố định + dao động dừng quanh nó. | 0,05 × t + nhiễu. |
| nghiệm đơn vị (unit root) | Tên kỹ thuật của "có thành phần random walk"; xem hộp Mượn trước mục 4.5. | Random walk có nghiệm đơn vị. |
| ADF, KPSS | Hai kiểm định tính dừng với $H_0$ ngược nhau (mục 4.5). | ADF: $H_0$ "không dừng"; KPSS: $H_0$ "dừng". |
| sai phân (differencing), sai phân mùa vụ | Thay mỗi giá trị bằng hiệu với giá trị trước ($y_t - y_{t-1}$), hoặc với cùng vị trí của vòng trước ($y_t - y_{t-m}$). | 100, 103, 105 → 3, 2. |
| sai phân thừa (overdifferencing) | Sai phân một chuỗi đã dừng: thêm nhiễu, tạo tương quan âm giả. | Mục 4.6. |

### 4.1 ACF tính tay, và ba hình dạng cần nhận ra

**Vấn đề.** Muốn dùng quá khứ để dự báo, trước hết phải biết quá khứ có "nói" gì về hiện tại không, và nói ở độ trễ nào.

**Ví dụ số nhỏ — tự tính tay.** Sáu số: 2, 3, 5, 6, 5, 3.

1. Trung bình: (2 + 3 + 5 + 6 + 5 + 3) / 6 = 24 / 6 = 4.
2. Độ lệch khỏi trung bình: −2, −1, 1, 2, 1, −1.
3. Mẫu số (tổng bình phương độ lệch): 4 + 1 + 1 + 4 + 1 + 1 = 12.
4. Trễ 1: nhân độ lệch của mỗi số với độ lệch của số **ngay trước** nó (5 cặp): (−1)(−2) + (1)(−1) + (2)(1) + (1)(2) + (−1)(1) =
   2 − 1 + 2 + 2 − 1 = 4.
5. $r_1$ = 4 / 12 ≈ **0,333**.

$r_1$ dương, vì các số liền nhau hay cùng phía trung bình: hai số đầu cùng dưới, ba số giữa cùng trên.

Trễ 2 (bốn cặp): 1 × (−2) + 2 × (−1) + 1 × 1 + (−1) × 2 = −5, nên $r_2$ = −5/12 ≈ −0,417: cách nhau hai bước thì hay ở hai phía.

**Công thức** (đã gặp ở buổi 4):

$$
r_k = \frac{\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)}{\sum_{t=1}^{T}(y_t-\bar y)^2}
$$

- $T$: số điểm; $\bar y$: trung bình; tử số cộng tích độ lệch của các cặp cách nhau $k$ bước; mẫu số cộng bình phương độ lệch của mọi
  điểm.

**Nói bằng lời.** Cộng các tích "độ lệch bây giờ × độ lệch $k$ bước trước", chia cho tổng bình phương độ lệch; ở ví dụ 4 / 12 = 1/3.
Mẫu số luôn cộng **cả** chuỗi dù tử số chỉ có ít cặp hơn, nên $r_k$ co về 0 ở trễ lớn: ước lượng từ ít cặp thì bớt tin.

`acf_tu_viet` trong `code/tu_tuong_quan.py` làm đúng công thức này; `statsmodels.tsa.stattools.acf(y, adjusted=False)` cho cùng số.

**Ba hình dạng cần nhận ra** (FPP §2.8):

- **Nhiễu trắng**: mọi $r_k$ ($k \ge 1$) nằm quanh 0, trong dải.
- **Xu hướng hoặc random walk**: $r_1$ lớn, gần 1, và $r_k$ giảm **rất chậm** khi $k$ tăng.
- **Mùa vụ**: $r_k$ có đỉnh ở bội số của chu kỳ ($k$ = 24, 48… với dữ liệu giờ).

**Tóm lại.** **$r_k$ là tổng "độ lệch nhân độ lệch" của các cặp cách $k$ bước, chia tổng bình phương độ lệch. ACF quanh 0 là nhiễu trắng,
giảm rất chậm là chưa dừng, có đỉnh đều là mùa vụ.**

**Tự kiểm tra.** Tính $r_1$ và $r_2$ cho 1, 1, 5, 5, 3, 3.

<details>
<summary>Đáp án</summary>

Trung bình 18/6 = 3. Độ lệch: −2, −2, 2, 2, 0, 0; mẫu số 4 + 4 + 4 + 4 + 0 + 0 = 16. Trễ 1: (−2)(−2) + (2)(−2) + (2)(2) + (0)(2) +
(0)(0) = 4, nên $r_1$ = 4/16 = **0,25**. Trễ 2: (2)(−2) + (2)(−2) + (0)(2) + (0)(2) = −8, nên $r_2$ = −8/16 = **−0,5**. Nhầm hay gặp: chia
cho số cặp (5 hoặc 4) thay vì tổng bình phương độ lệch của cả chuỗi.

</details>

### 4.2 PACF: trễ 2 còn thêm gì sau khi đã biết trễ 1

**Vấn đề.** Với AR(1), giá trị hôm nay chỉ phụ thuộc trực tiếp vào hôm qua. Nhưng hôm qua lại phụ thuộc hôm kia, nên ACF ở trễ 2 vẫn lớn. Ta
cần tách: trễ 2 có **thêm** thông tin nào ngoài cái đã đi qua trễ 1 không?

**Trực giác.** Tin đồn truyền qua ba người A → B → C. C giống A chỉ vì cả hai nối qua B. Biết B rồi thì A không cho C thêm gì. PACF ở trễ 2
đo đúng phần "thêm" đó.

**Ví dụ số nhỏ — tự tính tay.** Ở trễ 2, PACF có công thức gọn:

$$
\phi_{22} = \frac{r_2 - r_1^2}{1 - r_1^2}
$$

- $r_1$, $r_2$: ACF ở trễ 1 và 2. $r_1^2$: phần tương quan trễ 2 "đi qua" trễ 1 (A giống B nhân B giống C).
- $\phi_{22}$: PACF ở trễ 2.

**Nói bằng lời.** Lấy tương quan trễ 2, trừ phần đi qua trễ 1 ($r_1^2$). Chia cho $1 - r_1^2$ để kết quả vẫn nằm trong khoảng −1 tới 1,
giống vai trò mẫu số của $r_k$.

- AR(1) với $\phi$ = 0,7: $r_1$ = 0,7, $r_2$ = 0,7² = 0,49. PACF(2) = (0,49 − 0,49) / (1 − 0,49) = **0**: trễ 2 không thêm gì.
- Một chuỗi có $r_1$ = 0,5, $r_2$ = 0,4: PACF(2) = (0,4 − 0,25) / (1 − 0,25) = **0,2**: trễ 2 có thêm thông tin riêng.

Trễ lớn hơn cũng làm theo ý đó nhưng công thức dài; dùng `statsmodels.tsa.stattools.pacf(y, method="ywm")`. Lưu ý `pacf()` mặc định
`method="ywadjusted"` còn `plot_pacf()` mặc định `"ywm"`: khai `method` rõ ràng để bảng và hình khớp nhau.

![Bốn chuỗi cùng một dãy nhiễu: ACF phân biệt dừng với không dừng, PACF chỉ ra bậc AR](hinh/bon-chuoi.png)

**Cách đọc hình.**

1. **Trục ngang**: cột trái là thời điểm $t$ (500 bước); hai cột phải là độ trễ $k$, 0 → 30.
2. **Trục dọc**: cột trái là giá trị chuỗi; cột giữa là $r_k$ (ACF); cột phải là PACF; hai cột sau từ −1 tới 1.
3. **Ký hiệu**: mỗi hàng một chuỗi, cùng một dãy nhiễu (seed 42): nhiễu trắng, AR(1), random walk, xu hướng cộng nhiễu (bảng dưới);
   dải xám là ±1,96/√T.
4. **Nhìn vào đâu**: ACF hàng 2 so với hàng 3–4; PACF hàng 2.
5. **Kết luận**: AR(1) có ACF giảm nhanh và PACF cắt sau trễ 1; random walk và xu hướng có ACF giảm rất chậm, trông gần như nhau.

| Chuỗi | $r_1$ | $r_{30}$ | PACF trễ 1 | PACF trễ 2 |
|---|---|---|---|---|
| nhiễu trắng | 0,099 | −0,047 | 0,099 | −0,009 |
| AR(1) $\phi$ = 0,7 | 0,713 | −0,026 | 0,713 | −0,110 |
| random walk | 0,976 | 0,530 | 0,976 | −0,091 |
| xu hướng 0,05t | 0,979 | 0,806 | 0,979 | 0,320 |

**Đọc bảng.** So dòng 3 với dòng 4: cả hai có $r_1$ gần 1 và $r_{30}$ còn lớn. Chỉ nhìn ACF không phân biệt được random walk với chuỗi dừng
quanh xu hướng; hai thứ này cần xử lý khác nhau (mục 4.4), nên phải có kiểm định (mục 4.5).

**Tóm lại.** **PACF trễ $k$ là phần tương quan còn lại sau khi bỏ những gì các trễ ngắn hơn đã giải thích. AR(1): ACF giảm dần, PACF cắt
sau trễ 1.**

**Tự kiểm tra.** Một chuỗi có $r_1$ = 0,6, $r_2$ = 0,36. PACF trễ 2 bằng bao nhiêu? Chuỗi giống AR bậc mấy?

<details>
<summary>Đáp án</summary>

(0,36 − 0,6²) / (1 − 0,36) = 0 / 0,64 = **0**. Tương quan trễ 2 đi hết qua trễ 1, giống AR(1) với $\phi$ = 0,6. Nhầm hay gặp: thấy $r_2$ =
0,36 "khá lớn" rồi kết luận cần cả trễ 2 trong mô hình.

</details>

### 4.3 Nhiễu trắng và Ljung-Box

**Vấn đề.** Sau khi dự báo, phần sai số còn lại có còn mẫu hình không? Nhìn 20 cột ACF rồi đếm cột vượt dải thì rất dễ tự lừa mình.

**Trực giác.** Mỗi cột ACF giống một lần tung đồng xu có 5% khả năng "vượt dải" dù chuỗi là nhiễu thuần. Tung 20 lần thì trung bình có 20 ×
0,05 = 1 lần vượt. Thấy một cột vượt là chuyện bình thường.

![Một cột ACF vượt dải không phải bằng chứng: nhiễu trắng cũng thường có vài cột vượt](hinh/nhieu-trang.png)

**Cách đọc hình.**

1. **Trục ngang**: ô trái là độ trễ 0 → 20; ô phải là số cột vượt dải trong 20 trễ (0, 1, 2…).
2. **Trục dọc**: ô trái là $r_k$; ô phải là số chuỗi (trong 1.000 chuỗi nhiễu trắng mô phỏng, mỗi chuỗi 500 điểm) có đúng số cột vượt đó.
3. **Ký hiệu**: ô trái, dải xám là ±1,96/√T của FPP, đường gạch xanh lá là dải mặc định của statsmodels (dải Bartlett, rộng dần theo trễ).
4. **Nhìn vào đâu**: ô phải, hai cột 0 và 1 so với các cột 2, 3 trở lên.
5. **Kết luận**: nhiễu trắng thuần mà trung bình vẫn có 0,95 cột vượt dải trong 20 trễ, và 62% số chuỗi có ít nhất một cột vượt.

**Ljung-Box** gộp nhiều trễ vào **một** kiểm định. $H_0$: chuỗi là nhiễu trắng (mọi $r_k$ thật đều bằng 0).

> **Mượn trước — phân phối $\chi^2$ (khi bình phương)** (buổi 25 dùng lại). Cộng bình phương của vài số ngẫu nhiên hình chuông thì ra một
> số có phân phối tên là $\chi^2$, với **bậc tự do** bằng số hạng được cộng. Ta chỉ cần **ngưỡng** tra sẵn: mức mà nếu $H_0$ đúng thì
> chỉ 5% trường hợp vượt qua (bảng dưới). `scipy.stats.chi2.sf(Q, df)` tính p-value.

| Bậc tự do | 2 | 8 | 10 |
|---|---|---|---|
| Ngưỡng 5% của $\chi^2$ | 5,99 | 15,51 | 18,31 |

**Đọc bảng.** Càng nhiều bậc tự do (càng nhiều trễ cộng vào) thì ngưỡng càng cao: cộng nhiều bình phương hơn thì tổng tự nhiên lớn hơn.

**Ví dụ số nhỏ — tự tính tay.** Một chuỗi 100 điểm có $r_1$ = 0,2 và $r_2$ = 0,1; xét hai trễ:

$Q^*$ = 100 × 102 × (0,2² / 99 + 0,1² / 98) = 10.200 × (0,000404 + 0,000102) ≈ **5,16**

5,16 < 5,99 nên không bác bỏ $H_0$ ở mức 5% (p ≈ 0,076): hai cột này chưa đủ bằng chứng có tự tương quan.

$$
Q^* = T(T+2) \sum_{k=1}^{\ell} \frac{r_k^2}{T-k}
$$

- $\ell$: số trễ gộp vào. $r_k^2$: bình phương nên cột âm hay dương đều cộng vào. $\frac{1}{T-k}$: trễ lớn có ít cặp hơn nên được nhân lên.
- Nếu $H_0$ đúng, $Q^*$ có phân phối $\chi^2$ với $\ell$ bậc tự do (trừ đi số tham số nếu $r_k$ tính trên sai số của một mô hình đã ước
  lượng).

**Nói bằng lời.** Cộng bình phương các $r_k$ (có trọng số), nhân với cỡ mẫu; tổng càng lớn thì càng khó tin chuỗi là nhiễu trắng. Ở ví dụ,
5,16 chưa vượt ngưỡng 5,99.

FPP khuyên $\ell$ = 10 cho dữ liệu không mùa vụ, $\ell = 2m$ cho dữ liệu mùa vụ, và không quá $T/5$. Nếu $r_k$ tính trên **sai số của một
mô hình đã ước lượng $p$ tham số** thì truyền `model_df=p`; quên thì p-value cao giả:

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
acorr_ljungbox(phan_du, lags=[10], model_df=2)     # cột lb_stat, lb_pvalue
```

Trên ba chuỗi nhiễu trắng mô phỏng, Ljung-Box với 10 trễ cho p từ 0,081 tới 0,885 (seed 1, 2, 3): đều không bác bỏ, đúng như mong đợi.

**Tóm lại.** **Đừng đếm cột vượt dải; dùng Ljung-Box, gộp các $r_k$ thành một kiểm định, và nhớ `model_df`
khi kiểm sai số của mô hình.**

**Tự kiểm tra.** Kiểm Ljung-Box với 10 trễ trên sai số của một mô hình có 2 tham số. Bậc tự do là bao nhiêu? Nếu quên trừ, p-value lệch về
phía nào?

<details>
<summary>Đáp án</summary>

10 − 2 = **8** bậc tự do. Quên trừ thì so $Q^*$ với ngưỡng của 10 bậc tự do, cao hơn ngưỡng của 8, nên p-value **lớn hơn** thật: dễ kết
luận "sai số là nhiễu trắng" khi chưa phải. Nhầm hay gặp: nghĩ trừ bậc tự do làm kiểm định "dễ dãi" hơn; thật ra là ngược lại.

</details>

### 4.4 Dừng, random walk, và dừng quanh xu hướng

**Vấn đề.** Nhiều mô hình (buổi 17) giả định chuỗi **dừng**. Chuỗi không dừng thì những gì học từ quá khứ không áp được cho tương lai.

**Trực giác — ba ví dụ đời thường.**

- **Nhiệt độ phòng có máy lạnh** đặt 25 °C: lúc 24,5, lúc 25,8, nhưng luôn bị kéo về 25. Mức trung bình và độ dao động không đổi theo
  thời gian: **dừng**.
- **Chiều cao một đứa trẻ** tăng đều theo tuổi, dao động nhỏ quanh đường tăng đó: **dừng quanh xu hướng**. Bỏ đường xu hướng đi thì phần
  còn lại dừng.
- **Người tung đồng xu rồi bước**: ngửa bước tới 1 bước, sấp lùi 1 bước. Không có vị trí nào để quay về; càng lâu càng có thể đi xa: **random
  walk**, không dừng.

**Ví dụ số nhỏ — tự tính tay (random walk).** Sáu lần tung: +1, −1, +1, +1, −1, +1. Vị trí sau mỗi lần là tổng dồn: 0 + 1 = 1, 1 − 1 = 0,
0 + 1 = 1, 1 + 1 = 2, 2 − 1 = 1, 1 + 1 = 2. Mỗi vị trí = vị trí trước + bước mới: $y_t = y_{t-1} + \varepsilon_t$.

| Số bước | 4 | 25 | 100 |
|---|---|---|---|
| Độ lệch chuẩn của vị trí (10.000 người mô phỏng, seed 7) | 2,0 | 5,0 | 10,1 |

**Đọc bảng.** Số bước gấp 25 lần thì độ lệch chuẩn gấp 5 lần: nó tăng theo căn bậc hai của số bước. Độ dao động đổi theo thời gian, nên
random walk không dừng.

**Định nghĩa.** Chuỗi **dừng** khi các tính chất thống kê của nó không phụ thuộc vào thời điểm quan sát (FPP §9.1). Tức là mức trung bình
không đổi, độ dao động không đổi, và tương quan giữa $y_t$ và $y_{t-k}$ chỉ phụ thuộc khoảng cách $k$. Có xu hướng, có mùa vụ, hay độ dao động
đổi theo thời gian thì không dừng. Chuỗi có **chu kỳ** (lên xuống không cố định độ dài) vẫn có thể dừng: không biết trước đỉnh
và đáy rơi vào đâu, nên không thời điểm nào có mức trung bình riêng.

**Hai loại không dừng, hai cách chữa.**

| Loại | Ví dụ | Chữa | Chữa nhầm thì sao |
|---|---|---|---|
| dừng quanh xu hướng | 0,05 × t + nhiễu | **khử xu hướng**: trừ đường thẳng khớp nhất theo $t$ | sai phân nó → sai phân thừa, thêm tương quan âm giả (mục 4.6) |
| random walk | tổng dồn nhiễu | **sai phân**: $y_t - y_{t-1}$ ra lại chính nhiễu | trừ một đường thẳng → phần còn lại vẫn lang thang, tạo ACF giả (Nelson & Plosser, 1982) |

**Đọc bảng.** Chọn đúng loại bệnh thì mới chọn đúng thuốc; mà trên ACF hai loại gần như giống hệt (bảng mục 4.2). Mục 4.5 dùng kiểm định
để phân biệt.

Dự báo tốt nhất cho một random walk là giá trị cuối cùng (dự báo naive, buổi 1); mọi "xu hướng" nhìn thấy trên nó chỉ là tổng dồn của các
bước ngẫu nhiên.

**Tóm lại.** **Dừng nghĩa là mức, độ dao động và tự tương quan không đổi theo thời gian. Random walk không dừng và chữa bằng sai phân; chuỗi
dừng quanh xu hướng chữa bằng khử xu hướng.**

**Tự kiểm tra.** Số tiền trong tài khoản: mỗi tháng nhận lương rồi tiêu một khoản ngẫu nhiên, không có mức nào "phải quay về". Dừng, dừng
quanh xu hướng, hay random walk? Nếu cuối mỗi tháng bạn chuyển phần dư trên 10 triệu sang sổ tiết kiệm, và rút từ sổ ra bù khi thiếu, để
đầu tháng nào cũng có đúng 10 triệu, thì số dư cuối tháng thuộc loại nào?

<details>
<summary>Đáp án</summary>

Trường hợp đầu giống **random walk** (số dư mới = số dư cũ + chênh lệch ngẫu nhiên, không bị kéo về đâu). Trường hợp sau, mỗi tháng bắt đầu lại từ
10 triệu, nên số dư cuối tháng dao động quanh 10 triệu: **dừng**. Nhầm hay gặp: thấy số dư "tăng dần" vài tháng rồi gọi là xu hướng; random walk cũng tạo ra những đoạn tăng
trông như xu hướng.

</details>

### 4.5 ADF và KPSS: hai kiểm định với giả thuyết ngược nhau

**Vấn đề.** Cần một con số để quyết định "chuỗi có thành phần random walk không". Có hai kiểm định phổ biến, và chúng đặt câu hỏi theo hai
chiều ngược nhau.

> **Mượn trước — nghiệm đơn vị** (buổi 17 dùng lại). Viết chuỗi dạng $y_t = \rho \, y_{t-1} + \varepsilon_t$. Nếu $\rho$ = 1 thì đó là
> random walk: chuỗi "có **nghiệm đơn vị**" (tên gọi từ phương trình đặc trưng, không cần cho buổi này). Nếu $|\rho| < 1$ thì mỗi bước kéo
> chuỗi một phần về trung bình: dừng. Ví dụ trung bình 0, đang ở 10: với $\rho$ = 0,7, kỳ vọng các bước sau là 0,7 × 10 = 7 rồi 0,7 × 7 =
> 4,9; với $\rho$ = 1, kỳ vọng mãi là 10.

**Trực giác của ADF.** ADF hỏi: khi chuỗi đang **cao** hơn mức thường, bước kế tiếp có xu hướng **kéo xuống** không? Nếu có, chuỗi bị kéo
về một mức: dừng. Nếu độ cao hiện tại không nói gì về bước kế tiếp, đó là random walk.

**Ví dụ số nhỏ — tự tính tay.** Hai chuỗi, mỗi chuỗi 5 số; bước = số sau trừ số trước:

| Chuỗi | Giá trị | Các bước | Bước sau khi đang cao hơn 5 |
|---|---|---|---|
| A (quanh 5) | 5, 8, 4, 6, 5 | +3, −4, +2, −1 | 8 → 4 (−4); 6 → 5 (−1): luôn đi xuống |
| B (tung đồng xu) | 5, 6, 7, 6, 7 | +1, +1, −1, +1 | 6 → 7 (+1); 7 → 6 (−1): lúc lên lúc xuống |

**Đọc bảng.** Ở A, cứ cao hơn 5 là bước sau đi xuống: có lực kéo về, giống $\rho$ < 1. Ở B, độ cao không đoán được bước sau: giống
$\rho = 1$. ADF làm việc này trên hàng trăm điểm: đo xem bước kế tiếp phụ thuộc độ cao hiện tại mạnh cỡ nào, và hỏi "càng cao thì càng
bị kéo xuống" có rõ ràng không.

**Hai kiểm định, hai giả thuyết:**

| | $H_0$ (giả định mặc định) | p nhỏ (< 0,05) nghĩa là |
|---|---|---|
| **ADF** | có nghiệm đơn vị (không dừng) | có bằng chứng chuỗi **dừng** |
| **KPSS** | dừng | có bằng chứng chuỗi **không dừng** |

Cả hai phải khai **dạng**: dạng "c" hỏi "dừng quanh một mức cố định", dạng "ct" hỏi "dừng quanh một đường xu hướng thẳng":

```python
adfuller(y, regression="c")    # hoặc "ct"
kpss(y, regression="c")        # cùng dạng với ADF
```

Chạy cả hai kiểm định với cùng một dạng, rồi đọc bảng 2 × 2:

| | **KPSS không bác bỏ** (không có bằng chứng không dừng) | **KPSS bác bỏ** (có bằng chứng không dừng) |
|---|---|---|
| **ADF bác bỏ** (có bằng chứng dừng) | **Dừng.** Hai kiểm định đồng ý: chuỗi dừng (với dạng đã khai). Không cần sai phân. | **Mâu thuẫn.** Mỗi kiểm định thấy bằng chứng cho phía của nó. Thường do độ dao động đổi theo thời gian, cú sốc, hay chuỗi đổi mức đột ngột. Vẽ chuỗi, xem lại dạng, thử đoạn không có cú sốc. |
| **ADF không bác bỏ** (không có bằng chứng dừng) | **Không đủ bằng chứng.** Không kiểm định nào thấy gì rõ: dữ liệu ngắn, hoặc chuỗi dừng nhưng rất gần random walk. Xem ACF, cân nhắc theo mục đích dự báo. | **Không dừng.** Hai kiểm định đồng ý: có thành phần random walk. Sai phân rồi kiểm lại. |

**Đọc bảng.** Chỉ ô trên trái và ô dưới phải cho kết luận rõ. Hai ô còn lại là tín hiệu "đừng tin máy móc": ô trên phải đòi xem lại chuỗi, ô
dưới trái đòi thêm dữ liệu hoặc bằng chứng khác. Đây là quy tắc kinh nghiệm, không phải định lý.

Hai lời nhắc:

- **Không bác bỏ không phải chứng minh.** ADF hay bỏ sót: chuỗi dừng nhưng rất gần random walk thì ADF thường vẫn không bác bỏ (Zivot).
- **p-value của KPSS bị cắt** ở 0,01 và 0,1 (statsmodels báo `InterpolationWarning`): "p = 0,10" nghĩa là "p ≥ 0,1", không phải "rất dừng".

**Bốn chuỗi mô phỏng** (seed 42, 500 điểm):

| Chuỗi | ADF c | KPSS c | ADF ct | KPSS ct | Kết luận |
|---|---|---|---|---|---|
| nhiễu trắng | 0,000 | ≥ 0,10 | 0,000 | ≥ 0,10 | dừng |
| AR(1) $\phi$ = 0,7 | 0,000 | ≥ 0,10 | 0,000 | ≥ 0,10 | dừng |
| random walk | 0,073 | ≤ 0,01 | 0,214 | ≤ 0,01 | không dừng → sai phân |
| xu hướng 0,05t | 0,906 | ≤ 0,01 | 0,000 | ≥ 0,10 | dạng "c" nói không dừng; dạng "ct" nói **dừng quanh xu hướng** → khử xu hướng |

**Đọc bảng.** Dòng 4: chỉ khi khai dạng "ct" chuỗi mới lộ đúng bản chất; code đầu buổi chỉ chạy "c" nên bảo sai phân. Dòng 3: random walk có
ADF p = 0,073, nếu dùng mức 10% sẽ bị gọi nhầm là dừng; KPSS bắt được.

**Dữ liệu thật: tăng trưởng GDP Mỹ theo quý** (hiệu log liên tiếp × 100, gần bằng phần trăm tăng mỗi quý vì log 1,01 ≈ 0,01):

| Giai đoạn | Số quý | ADF p | KPSS p | Ô của bảng 2 × 2 |
|---|---|---|---|---|
| 1947Q2–2026Q2 | 317 | 0,000 | 0,048 | mâu thuẫn |
| 1985Q1–2019Q4 | 140 | 0,000 | 0,099 | dừng |

**Đọc bảng.** Cả giai đoạn rơi vào ô mâu thuẫn; bỏ những năm dao động mạnh trước 1985 và cú sốc đại dịch (2020Q2 −8,2%, 2020Q3 +7,5%) thì hai
kiểm định đồng ý "dừng". KPSS bác bỏ vì độ dao động đổi theo thời gian, không phải vì random walk. Kiểm định là bằng chứng, không phải phán quyết.

**Tóm lại.** **ADF: $H_0$ là không dừng; KPSS: $H_0$ là dừng. Chạy cả hai cùng dạng ("c" hoặc "ct") và đọc bảng 2 × 2: hai ô đồng ý cho
kết luận, hai ô còn lại đòi xem lại chuỗi.**

**Tự kiểm tra.** ADF p = 0,40, KPSS p = 0,01 (cùng dạng "c"). Ô nào, và làm gì tiếp?

<details>
<summary>Đáp án</summary>

ADF không bác bỏ (không có bằng chứng dừng), KPSS bác bỏ (có bằng chứng không dừng): ô **không dừng**. Sai phân một lần rồi kiểm lại cả hai,
và xem hai dấu hiệu sai phân thừa (mục 4.6). Nhầm hay gặp: đọc "KPSS p nhỏ" thành "dừng" vì quen với ADF.

</details>

### 4.6 Sai phân bao nhiêu lần là đủ

**Vấn đề.** Sai phân chữa random walk, nhưng sai phân thêm một chuỗi đã dừng lại làm hỏng nó. Cần biết khi nào dừng tay.

**Ví dụ số nhỏ — tự tính tay (sai phân thừa).** Chuỗi đã dừng: 2, −1, 0, 1, −2, 0 (độ lệch chuẩn ≈ 1,41). Sai phân: −1 − 2 = −3, 0 − (−1) = 1,
1, −3, 2. Độ lệch chuẩn của năm số này ≈ 2,41: **tăng** gấp 1,7. $r_1$ của chuỗi đã sai phân ≈ −0,50: lên thì lần sau xuống. Lý do: mỗi
số gốc xuất hiện hai lần với hai dấu ngược nhau, trong $y_t - y_{t-1}$ và trong $y_{t+1} - y_t$.

**Hai dấu hiệu sai phân thừa** (Nau, Duke):

1. $r_1$ của chuỗi đã sai phân **gần −0,5** (từ −0,5 trở xuống là dấu hiệu rõ).
2. **Độ lệch chuẩn tăng** so với trước khi sai phân. Số lần sai phân tốt thường là số lần cho độ lệch chuẩn **nhỏ nhất**.

Quy tắc của FPP: sai phân tiếp chừng nào KPSS còn bác bỏ tính dừng; rồi kiểm hai dấu hiệu trên.

![Sai phân chuỗi đã dừng làm ACF(1) về gần −0,5 và độ lệch chuẩn tăng](hinh/sai-phan-thua.png)

**Cách đọc hình.**

1. **Trục ngang**: hàng trên là thời điểm $t$; hàng dưới là độ trễ $k$, 0 → 20.
2. **Trục dọc**: hàng trên là giá trị sau sai phân; hàng dưới là $r_k$.
3. **Ký hiệu**: cột trái là nhiễu trắng (đã dừng) sau khi sai phân; cột phải là random walk sau khi sai phân; tiêu đề ghi độ lệch chuẩn
   trước và sau.
4. **Nhìn vào đâu**: cột ACF trễ 1 ở hai ô dưới; độ lệch chuẩn ở hai tiêu đề.
5. **Kết luận**: sai phân nhiễu trắng cho $r_1$ = −0,447 và độ lệch chuẩn tăng 0,96 → 1,29 (thừa); sai phân random walk cho $r_1$ = 0,100 và
   độ lệch chuẩn giảm 4,55 → 0,96 (đúng liều).

**Chuỗi mùa vụ: sai phân mùa vụ trước.** Với dữ liệu mùa vụ, sai phân **mùa vụ** $y_t - y_{t-m}$ trước; nếu sai phân thường trước thì mùa
vụ vẫn còn (FPP §9.1). Lượt thuê xe theo giờ, thang log ($\log(1 + y)$ vì có giờ 0 lượt), $m$ = 168 (một tuần):

| Chuỗi | $r_1$ | $r_{24}$ | $r_{168}$ | Độ lệch chuẩn |
|---|---|---|---|---|
| log | 0,898 | 0,863 | 0,896 | 1,430 |
| sai phân thường | 0,493 | 0,676 | 0,767 | 0,643 |
| sai phân mùa vụ 168 | 0,732 | 0,161 | −0,465 | 0,589 |
| sai phân 168 rồi sai phân thường | −0,249 | 0,028 | −0,498 | 0,427 |

**Đọc bảng.** Dòng hai: chỉ sai phân thường thì $r_{24}$, $r_{168}$ vẫn lớn, mùa vụ còn nguyên. Dòng ba: sai phân mùa vụ bỏ được mùa vụ
ngày và tuần. Dòng cuối: thêm sai phân thường làm độ lệch chuẩn giảm tiếp, và $r_1$ chưa tới dấu hiệu thừa: ở đây cả hai lần sai phân đều
đáng. ($r_{168}$ gần −0,5 ở hai dòng cuối là dấu vết của chính phép sai phân mùa vụ, buổi 17 xử lý.)

**Dữ liệu thật: GDP.** log GDP có ACF giảm rất chậm (0,991 ở trễ 1; 0,923 ở trễ 8); ADF (dạng "ct") p = 0,833 và KPSS p ≤ 0,01: không dừng,
sai phân một lần ra tăng trưởng. Máy móc theo KPSS thì sai phân **lần hai** (vì ô mâu thuẫn ở mục 4.5). Nhưng lần hai cho $r_1$ = −0,488 và
độ lệch chuẩn tăng 1,105 → 1,455: đúng hai dấu hiệu thừa. Dừng ở một lần.

![GDP thực Mỹ: log GDP chưa dừng, sai phân log dao động quanh 0,76% mỗi quý](hinh/gdp.png)

**Cách đọc hình.**

1. **Trục ngang**: hàng trên là năm, 1947 → 2026; hàng dưới là độ trễ (quý), 0 → 24.
2. **Trục dọc**: trên trái là log GDP; trên phải là phần trăm tăng mỗi quý; hàng dưới là $r_k$.
3. **Ký hiệu**: một đường mỗi ô trên; vạch là $r_k$, dải xám ±1,96/√T.
4. **Nhìn vào đâu**: ACF dưới trái so với dưới phải; cú sốc 2020 ở ô trên phải.
5. **Kết luận**: log GDP có ACF giảm rất chậm (chưa dừng); sau một lần sai phân, ACF chỉ còn hai cột đầu hơi vượt dải, tăng trưởng dao động
   quanh 0,76% mỗi quý với hai cú sốc năm 2020.

**Tóm lại.** **Sai phân tới khi KPSS thôi bác bỏ, nhưng dừng tay nếu $r_1$ về gần −0,5 hoặc độ lệch chuẩn tăng. Có mùa vụ thì bỏ mùa vụ
bằng sai phân theo chu kỳ trước.**

**Tự kiểm tra.** Sai phân một chuỗi, độ lệch chuẩn đi 2,0 → 1,2; sai phân lần hai, 1,2 → 1,6 và $r_1$ = −0,52. Nên sai phân mấy lần?

<details>
<summary>Đáp án</summary>

**Một lần.** Lần hai làm độ lệch chuẩn tăng và $r_1$ về dưới −0,5: hai dấu hiệu thừa. Nhầm hay gặp: chọn hai lần vì KPSS sau hai lần "đẹp
hơn"; p-value đẹp không bù được một chuỗi nhiễu hơn.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.** Ta chỉ có **một** chuỗi quan sát, nhưng vẫn tính trung bình, phương sai, ACF như thể có nhiều lần
> lặp. Điều đó dựa trên giả định **ergodic**: khi chuỗi dài ra, trung bình theo thời gian tiến về trung bình "của mọi lần lặp có thể" (Zivot).
> Random walk vi phạm giả định này: trung bình mẫu của nó không tiến về đâu cả. Thêm một lý do phải đưa chuỗi về dạng dừng trước khi ước lượng.

## 5. Lab từng bước

Lệnh gõ trong terminal ở thư mục `lab/`. Code các bước nằm sẵn trong `code/lab.ipynb` (mở bằng `python lab.py notebook` hoặc
VS Code), chạy từng ô từ trên xuống. Bạn sửa `code/tu_tuong_quan.py`; notebook tự nạp lại bản mới.

### Bước 1 — Chạy code đầu buổi

**Mục đích:** thấy bảng bốn chuỗi hiện tại kết luận sai ở đâu.

```bash
python lab.py up           # một lần: môi trường + dữ liệu, kiểm sha256
python lab.py check        # 5/9 test đỏ
python lab.py notebook     # chạy ô bước 1
```

```text
         chuỗi  ACF(1)  ADF c                  kết luận  d
   nhiễu trắng   0.099  0.000                      dừng  1
   AR(1) φ=0,7   0.713  0.000                      dừng  1
   random walk   0.976  0.073 không dừng — cần sai phân  1
xu hướng 0,05t   0.979  0.906 không dừng — cần sai phân  1
```

**Đọc kết quả:** cột `d` (số lần sai phân) là 1 cho cả bốn, kể cả nhiễu trắng đã dừng; chuỗi xu hướng bị bảo sai phân vì chỉ có dạng "c"
(bảng mục 4.5).

### Bước 2 — ACF và PACF tự tính

**Mục đích:** nối ví dụ tay (mục 4.1, 4.2) với code.

Ô bước 2 tính `acf_tu_viet` trên 2, 3, 5, 6, 5, 3 và đối chiếu `statsmodels`, rồi vẽ ACF, PACF (`method="ywm"`) cho bốn chuỗi.

**Đọc kết quả:** $r_1$ = 0,333, $r_2$ = −0,417 như tính tay; hình giống hình mục 4.2.

### Bước 3 — Thêm KPSS và dạng "quanh xu hướng"

**Mục đích:** sửa `kiem_dinh` và `ket_luan` theo mục 4.5.

`kiem_dinh(y, co_xu_huong)` chạy cả `adfuller` và `kpss` ở dạng "ct" khi `co_xu_huong=True`, dạng "c" khi không (khối code mục
4.5); truyền `result_object=True` cho cả hai; trả `adf_p` và `kpss_p`. `ket_luan` trả một trong bốn ô của bảng 2 × 2. Bắt `InterpolationWarning` để ghi
lại khi p của KPSS bị cắt.

**Đọc kết quả:** chạy lại ô bước 1: bảng có thêm cột KPSS và cột dạng "ct"; dòng xu hướng thành "dừng quanh xu hướng" ở dạng "ct".

### Bước 4 — Số lần sai phân vừa đủ

**Mục đích:** sửa `so_lan_sai_phan` theo mục 4.6: bắt đầu từ 0 lần, sai phân tiếp chừng nào KPSS còn bác bỏ.

**Đọc kết quả:** nhiễu trắng và AR(1) ra 0, random walk ra 1. Ô bước 4 in `dau_hieu_sai_phan_thua` cho nhiễu trắng: $r_1$ sau sai phân
khoảng −0,45, độ lệch chuẩn tăng.

### Bước 5 — Chuỗi thật

**Mục đích:** áp cả ba bằng chứng (ACF, ADF, KPSS) lên dữ liệu thật.

Ô bước 5 chạy cho log GDP, tăng trưởng GDP (cả giai đoạn và 1985–2019), log sản lượng công nghiệp. Với mỗi chuỗi viết một dòng: ô nào của
bảng 2 × 2, số lần sai phân, và **bằng chứng nào** dẫn tới kết luận. Rồi:

```bash
python lab.py check        # 9/9 xanh
```

**Đọc kết quả:** log sản lượng công nghiệp là ví dụ ô "không đủ bằng chứng": ở dạng "ct", ADF không bác bỏ (p = 0,252) và KPSS cũng không
(p ≥ 0,1). Sau một lần sai phân cả hai đồng ý dừng.

## 6. Lỗi thường gặp & cách chẩn đoán

| Triệu chứng | Nguyên nhân | Chẩn đoán | Sửa |
|---|---|---|---|
| "ADF không bác bỏ → chuỗi có nghiệm đơn vị" | không bác bỏ ≠ chứng minh $H_0$ | xem ACF, cỡ mẫu | chạy thêm KPSS |
| Chuỗi có xu hướng thẳng bị sai phân | chỉ chạy dạng "c" | chạy lại dạng "ct" | khử xu hướng |
| ADF và KPSS cùng bác bỏ | độ dao động đổi, cú sốc, đổi mức đột ngột | vẽ chuỗi; thử đoạn không có cú sốc | tách đoạn, biến đổi ổn định độ dao động |
| KPSS "p = 0,10" đọc thành "rất dừng" | p bị cắt theo bảng tra | `InterpolationWarning` | ghi "p ≥ 0,1" |
| Sai phân xong $r_1$ ≈ −0,5, độ lệch chuẩn tăng | sai phân thừa | `dau_hieu_sai_phan_thua` | bớt một lần |
| Ljung-Box trên sai số mô hình cho p đẹp | quên `model_df` | so p có và không có `model_df` | truyền số tham số |
| Đếm cột ACF vượt dải rồi kết luận | nhiều kiểm định cùng lúc | 62% chuỗi nhiễu trắng có ≥ 1 cột vượt | Ljung-Box |
| Hình `plot_acf` khác hình tự vẽ | dải Bartlett khác ±1,96/√T | `bartlett_confint=False` | thống nhất một cách, ghi rõ |
| PACF trong bảng khác PACF trên hình | `pacf` mặc định `ywadjusted`, `plot_pacf` mặc định `ywm` | in tham số | khai `method="ywm"` |
| FutureWarning khi gọi `adfuller`/`kpss` | kiểu trả về sắp đổi | đọc cảnh báo | `result_object=True` |
| Sai phân thường xong ACF vẫn có đỉnh ở trễ $m$ | mùa vụ còn nguyên | ACF ở trễ $m$ | sai phân mùa vụ trước |
| ACF hay `diff(7)` trên chuỗi ngày ra số lạ | chuỗi bị `dropna()` giữa chừng, "7 dòng" không còn là 7 ngày | kiểm index có liên tục không | giữ lưới ngày đầy đủ, nội suy ngày trống |

## 7. Bài tập về nhà

1. **Lượt thuê theo ngày.** Tổng lượt thuê theo ngày (lưới ngày liên tục, nội suy 3 ngày dưới 12 giờ). Kiểm ADF/KPSS, so độ lệch chuẩn khi
   sai phân mùa vụ 7, sai phân thường, và cả hai. Cách nào tốt nhất, và vì sao mùa vụ tuần theo ngày yếu hơn theo giờ (gợi ý: buổi 4, tổng
   ngày các thứ chỉ chênh vài phần trăm)?
2. **Độ mạnh của ADF.** Mô phỏng nhiều chuỗi AR(1) dài 200 điểm, với $\phi = 0{,}95$ (gần random walk) và $\phi = 0{,}7$; đếm tỷ lệ ADF
   bác bỏ ở mức 5%.
   Kết quả nói gì về câu "ADF không bác bỏ nên có nghiệm đơn vị"?
3. **Đổi mức đột ngột.** Ghép hai đoạn nhiễu trắng có trung bình 0 và 5 (mỗi đoạn 250 điểm). Chạy ADF/KPSS và ACF. Chuỗi có thành phần random
   walk không? Kiểm định nói gì, vì sao?

## 8. Tiêu chí "Xong khi"

- [ ] `python lab.py check` xanh 9/9.
- [ ] Tính tay được $r_1$, $r_2$ và PACF trễ 2 cho một chuỗi 6 số.
- [ ] Với một chuỗi lạ: kết luận dừng / không dừng và số lần sai phân, dựa trên cả ACF, ADF, KPSS, mỗi kết luận kèm con số.
- [ ] Giải thích ô "mâu thuẫn" và ô "không đủ bằng chứng" bằng ví dụ trong buổi (tăng trưởng GDP; sản lượng công nghiệp dạng "ct").
- [ ] Chỉ ra sai phân thừa bằng hai dấu hiệu: $r_1$ gần −0,5 và độ lệch chuẩn tăng.

## 9. Đọc thêm

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way* — §2.8–2.9 (ACF, nhiễu trắng), §5.4
  (Ljung-Box), chương 9 (tính dừng, sai phân): https://otexts.com/fpppy/
- Dickey, D.A. & Fuller, W.A. (1979). *JASA* 74(366a), 427–431 (ADF).
- Kwiatkowski, D., Phillips, P.C.B., Schmidt, P. & Shin, Y. (1992). *Journal of Econometrics* 54(1–3), 159–178 (KPSS).
- Nelson, C.R. & Plosser, C.I. (1982). Trends and random walks in macroeconomic time series. *J. Monetary Economics* 10, 139–162.
- Zivot, E. — *Unit Root Tests* (bài giảng Econ 584): https://faculty.washington.edu/ezivot/econ584/notes/unitroot.pdf
- Nau, R. — *Identifying the order of differencing*: https://people.duke.edu/~rnau/411arim2.htm
