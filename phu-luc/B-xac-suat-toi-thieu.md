# Phụ lục B — Xác suất thống kê tối thiểu cho dự báo

Dành cho người chưa học thống kê đại học. Đọc lần đầu thì đi mục 1–10; mục 11–16 dùng ở nửa sau khoá. Mọi con số
chạy thật ngày 2026-09-18 (môi trường buổi 2); mô phỏng dùng **seed** (hạt giống) 2026: cùng seed thì ra cùng số.

## Tra nhanh

| Từ | Nghĩa một câu | Mục |
|---|---|---|
| biến ngẫu nhiên, phân phối | đại lượng chưa biết trước; bảng "giá trị · khả năng" của nó | [1](#1-biến-ngẫu-nhiên-và-phân-phối) |
| mẫu, bảng đếm, histogram | số liệu có trong tay; đếm mỗi giá trị; biểu đồ cột của phép đếm | [1](#1-biến-ngẫu-nhiên-và-phân-phối) |
| trung bình | tổng chia số lượng | [2](#2-trung-bình) |
| trung vị | số đứng giữa khi xếp tăng dần | [3](#3-trung-vị) |
| quantile mức $q$ | giá trị nhỏ nhất mà ít nhất $q$ phần số liệu nhỏ hơn hoặc bằng nó | [4](#4-quantile-phân-vị) |
| phương sai, độ lệch chuẩn | các số thường cách trung bình bao xa | [5](#5-phương-sai-và-độ-lệch-chuẩn) |
| hệ số lệch | phân phối có đuôi dài về một phía không, phía nào | [6](#6-hệ-số-lệch) |
| phân phối chuẩn | hình chuông; 95% nằm trong trung bình ± 1,96 độ lệch chuẩn | [7](#7-phân-phối-chuẩn-và-quy-tắc-6895997) |
| hàm mất mát | quy tắc tính "mất bao nhiêu" khi dự báo lệch khỏi thực tế | [8](#8-nên-dự-báo-trung-bình-trung-vị-hay-quantile) |
| hiệp phương sai, tương quan | hai đại lượng có cùng tăng cùng giảm không | [9](#9-hiệp-phương-sai-và-tương-quan) |
| kiểm định, $H_0$, p-value | dữ liệu có đủ bằng chứng bác bỏ một giả định không | [10](#10-kiểm-định-giả-thuyết-và-p-value) |
| độc lập, luật số lớn, CLT | trung bình nhiều lần đo độc lập ổn định dần, có dạng hình chuông | [11](#11-luật-số-lớn-và-định-lý-giới-hạn-trung-tâm) |
| khoảng tin cậy, khoảng dự báo | khoảng cho con số cố định chưa biết; khoảng cho giá trị tương lai | [12](#12-khoảng-tin-cậy-và-khoảng-dự-báo) |
| bootstrap | rút lại ngẫu nhiên từ chính dữ liệu để xem một con số dao động cỡ nào | [13](#13-bootstrap) |
| Poisson, âm nhị thức, Student-t | phân phối cho dữ liệu đếm và dữ liệu đuôi dày | [14](#14-phân-phối-cho-dữ-liệu-đếm-và-dữ-liệu-đuôi-dày) |
| likelihood, MLE | dữ liệu "hợp" với một giá trị tham số tới đâu; chọn tham số hợp nhất | [15](#15-likelihood-và-mle) |
| hồi quy, R² | đường thẳng đoán một biến từ biến khác; R² là phần giải thích được | [16](#16-hồi-quy-và-r²) |
| bẫy thường gặp | nhầm lẫn hay gặp và cách sửa | [17](#17-bẫy-thường-gặp) |

**Thiết lập dùng cho mọi khối code bên dưới:**

```python
import numpy as np
import pandas as pd
from scipy import stats

x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # kWh lúc 19 giờ, 10 ngày (mục 1)
s = pd.Series(x)
```

## 1. Biến ngẫu nhiên và phân phối

Một **biến ngẫu nhiên** là đại lượng chưa biết trước giá trị, chỉ biết nó nhận được giá trị nào và giá trị nào dễ
xảy ra hơn (kết quả tung xúc xắc: 1 tới 6). **Phân phối** của nó là bảng "giá trị · khả năng"; xúc xắc cân đối có
mỗi mặt xác suất 1/6.

Với dữ liệu thật, ta chỉ có những lần đã quan sát, gọi là **mẫu**. Đếm mỗi giá trị xuất hiện mấy lần được **bảng
đếm**; chia số lần gặp cho tổng số quan sát được **tỷ lệ**, hình dung gần đúng của phân phối thật.

**Ví dụ số nhỏ — tự tính tay.** Mười ngày qua, lúc 19 giờ nhà dùng (kWh):

7, 5, 9, 6, 8, 12, 6, 9, 7, 8

Phụ lục này dùng **cùng dãy 10 số này** cho gần như mọi ví dụ. Đếm từng giá trị:

| Lượng điện (kWh) | 5 | 6 | 7 | 8 | 9 | 12 |
|---|---|---|---|---|---|---|
| Số ngày | 1 | 2 | 2 | 2 | 2 | 1 |
| Tỷ lệ | 0,1 | 0,2 | 0,2 | 0,2 | 0,2 | 0,1 |

**Đọc bảng.** Tỷ lệ cộng lại bằng 1. Phần lớn ngày ở 6–9 kWh, riêng 12 kWh tách xa. Số ngày dùng không quá 8 kWh là
7/10 = 0,7.

**Histogram** là biểu đồ cột của bảng đếm: trục ngang là giá trị (nhiều giá trị thì gộp thành khoảng), chiều cao cột
là số lần gặp.

**Công thức.** Tỷ lệ của giá trị $v$ trong mẫu:

$$
\hat p(v) = \frac{\text{số lần gặp } v}{n}
$$

- $n$: số quan sát trong mẫu. Ở đây $n = 10$.
- $\hat p(v)$: tỷ lệ số lần gặp giá trị $v$. Dấu mũ $\hat{\ }$ nghĩa là "ước lượng từ mẫu", không phải con số
  thật của phân phối.

**Nói bằng lời.** Tỷ lệ của một giá trị là số lần gặp nó chia cho tổng số lần đo. Giá trị 6 kWh gặp 2 lần trên
10 ngày, nên $\hat p(6) = 2/10 = 0{,}2$.

**Tóm lại.** **Phân phối cho biết mỗi giá trị hay gặp tới đâu; với dữ liệu thật, ta xem bảng đếm của mẫu.**

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> - **CDF** (hàm phân phối tích luỹ) tại $y$ là tỷ lệ giá trị nhỏ hơn hoặc bằng $y$, viết $F(y) = P(Y \le y)$. Ở
>   ví dụ trên $F(8) = 0{,}7$. CDF tăng dần từ 0 tới 1.
> - Biến đếm được (số khách) có bảng "giá trị · xác suất" gọi là **PMF** (hàm khối xác suất). Biến liên tục (nhiệt
>   độ) dùng **PDF** (hàm mật độ): diện tích dưới đường cong giữa hai mốc là xác suất rơi vào khoảng đó.

## 2. Trung bình

**Ví dụ số nhỏ — tự tính tay.** Tổng 10 ngày: 7 + 5 + 9 + 6 + 8 + 12 + 6 + 9 + 7 + 8 = 77 kWh. Chia 10 ngày:
77 / 10 = **7,7 kWh**.

$$
\bar y = \frac{1}{n}\sum_{i=1}^{n} y_i
$$

- $y_i$: giá trị thứ $i$ trong mẫu ($y_1 = 7$, $y_2 = 5$, …).
- $\sum_{i=1}^{n}$: cộng tất cả các số từ số thứ 1 tới số thứ $n$.
- $\bar y$ (đọc là "y gạch"): trung bình của mẫu.

**Nói bằng lời.** Cộng hết các giá trị rồi chia cho số giá trị: 77 / 10 = 7,7 kWh.

**Điểm yếu.** Đổi ngày 12 kWh thành 40 kWh (hôm đó có tiệc), trung bình nhảy từ 7,7 lên 10,5 kWh, cao hơn cả chín
ngày còn lại.

**Tóm lại.** **Trung bình = tổng chia số lượng. Dễ tính, nhưng một giá trị cực đoan có thể kéo nó đi xa.**

## 3. Trung vị

Xếp các ngày từ ít tới nhiều. **Trung vị** là số đứng giữa: một nửa nhỏ hơn hoặc bằng, một nửa lớn hơn hoặc bằng.

**Ví dụ số nhỏ — tự tính tay.**

- Xếp tăng dần: 5, 6, 6, 7, **7**, **8**, 8, 9, 9, 12.
- 10 số (chẵn) nên có hai số giữa, 7 và 8; lấy trung bình của chúng: (7 + 8) / 2 = **7,5 kWh**.
- Số lẻ giá trị thì chỉ có một số giữa: 3, 1, 7, 5, 100 → xếp 1, 3, **5**, 7, 100 → trung vị 5.

Đổi ngày 12 kWh thành 40 kWh như mục 2 thì trung vị vẫn 7,5.

**Công thức.** Gọi $y_{(1)} \le y_{(2)} \le \dots \le y_{(n)}$ là dãy đã xếp tăng dần.

$$
\text{trung vị} =
\begin{cases}
y_{((n+1)/2)} & \text{nếu } n \text{ lẻ} \\
\dfrac{y_{(n/2)} + y_{(n/2+1)}}{2} & \text{nếu } n \text{ chẵn}
\end{cases}
$$

- $y_{(k)}$: số đứng thứ $k$ sau khi xếp (ngoặc tròn quanh chỉ số nghĩa là "sau khi xếp").
- $n$: số giá trị.

**Nói bằng lời.** Với $n = 10$: trung bình số thứ 5 và số thứ 6, (7 + 8) / 2 = 7,5.

**Tóm lại.** **Trung vị không bị vài giá trị cực đoan kéo đi, nên hợp với dữ liệu đuôi dài như doanh số.**

## 4. Quantile (phân vị)

**Vì sao cần.** "Chuẩn bị bao nhiêu để **đủ trong 80% số ngày**?" có đáp án là một quantile.

**Định nghĩa.** **Quantile mức $q$** (với $q$ từ 0 tới 1) là **giá trị nhỏ nhất** mà **ít nhất** $q$ phần số liệu
nhỏ hơn hoặc bằng nó. Quantile 0,5 là trung vị. Quantile 0,25 và 0,75 còn gọi là **tứ phân vị** dưới và trên.

$$
Q(q) = y_{(k)}, \qquad k = \lceil q \times n \rceil
$$

- $q$: mức quantile, ví dụ 0,8.
- $n$: số giá trị; $y_{(k)}$: số đứng thứ $k$ sau khi xếp tăng dần.
- $\lceil \cdot \rceil$: làm tròn lên số nguyên gần nhất ($\lceil 2{,}5 \rceil = 3$, $\lceil 8 \rceil = 8$).

**Nói bằng lời.** Nhân mức quantile với số giá trị, làm tròn lên, rồi lấy số đứng ở vị trí đó. Với $q = 0{,}25$ và
$n = 10$: 0,25 × 10 = 2,5, làm tròn lên 3, số thứ 3 là 6 kWh.

**Ví dụ số nhỏ — tự tính tay.** Dãy đã xếp: 5, 6, 6, 7, 7, 8, 8, 9, 9, 12 ($n = 10$).

- **Quantile 0,8**: vị trí 0,8 × 10 = 8, số thứ 8 là **9 kWh**. Kiểm: 9/10 ngày ≤ 9 (đủ "ít nhất 80%"), còn 8 thì
  chỉ 7/10 ngày ≤ 8, chưa đủ. Vậy 9 là giá trị nhỏ nhất thoả điều kiện.
- **Quantile 0,5**: vị trí 0,5 × 10 = 5, lấy số thứ 5, là **7 kWh**.

Quantile 0,5 ra 7, còn trung vị ở mục 3 ra 7,5. Hai số lệch nhau chỉ vì quy ước khi có hai số đứng giữa; dữ liệu
nhiều thì gần như trùng.

**Code — chỗ hay gây nhầm.** Mặc định `np.quantile` **nội suy**: lấy một điểm giữa hai số kề nhau, nên có thể ra số
không có trong dữ liệu. Muốn khớp cách đếm tay, thêm `method="inverted_cdf"`.

```python
q = [0.1, 0.25, 0.5, 0.75, 0.8, 0.9]
np.quantile(x, q, method="inverted_cdf")   # [5 6 7 9 9 9]                — khớp đếm tay
np.quantile(x, q)                          # [5.9 6.25 7.5 8.75 9. 9.3]   — nội suy
s.quantile(0.25)                           # 6.25 — pandas nội suy như NumPy
```

**Đọc kết quả:** với 10 số, hai cách lệch nhau tới 0,9 kWh. Nội suy đánh số vị trí từ 0, lấy vị trí $(n - 1) \times q$:
với $q = 0{,}25$ là 2,25, giữa 6 và 7, ra 6,25. Lệch với thư viện khác thì kiểm cách tính quantile trước.

**Tóm lại.** **Tính tay: xếp tăng dần, lấy số thứ $\lceil q n \rceil$; `np.quantile` mặc định nội suy.**

**Tự kiểm tra.** Bảy ngày bán được 4, 9, 2, 7, 5, 3, 8 cái bánh. Quantile 0,8 là bao nhiêu?

<details>
<summary>Đáp án</summary>

Xếp: 2, 3, 4, 5, 7, 8, 9. Vị trí 0,8 × 7 = 5,6, làm tròn lên 6, số thứ 6 là **8 cái**. Kiểm: 6 trên 7 ngày ≤ 8, tức
khoảng 86% ≥ 80%. Nhầm hay gặp là làm tròn xuống thành 5 (ra 7 cái, chỉ 5/7 ≈ 71% ngày ≤ 7, chưa đủ 80%).
`np.quantile` mặc định ra 7,8 vì nội suy.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.** Có 9 cách tính quantile từ mẫu (Hyndman & Fan, 1996); NumPy mặc định là
> cách 7, đếm tay là cách 1. Viết bằng CDF (mục 1): quantile mức $q$ là $y$ nhỏ nhất mà $F(y) \ge q$. Quantile 0,75 trừ quantile 0,25 gọi là **IQR** (khoảng tứ phân vị); ở ví dụ
> trên IQR = 9 − 6 = 3 kWh.

## 5. Phương sai và độ lệch chuẩn

**Vì sao cần.** Nhà A ngày nào cũng 7–8 kWh, nhà B lúc 2 lúc 14: cùng trung bình, khác **độ dao động**.

**Trực giác.** Lấy mỗi ngày trừ trung bình ra độ lệch. Cộng thẳng thì lệch lên và lệch xuống triệt tiêu (tổng luôn
bằng 0), nên ta bình phương từng độ lệch rồi lấy trung bình: đó là **phương sai**. Căn bậc hai của nó, cùng đơn vị
gốc (kWh), là **độ lệch chuẩn**.

**Ví dụ số nhỏ — tự tính tay.** Trung bình là 7,7 kWh (mục 2).

| Ngày | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $y$ (kWh) | 7 | 5 | 9 | 6 | 8 | 12 | 6 | 9 | 7 | 8 |
| Độ lệch $y - 7{,}7$ | −0,7 | −2,7 | 1,3 | −1,7 | 0,3 | 4,3 | −1,7 | 1,3 | −0,7 | 0,3 |
| Bình phương độ lệch | 0,49 | 7,29 | 1,69 | 2,89 | 0,09 | 18,49 | 2,89 | 1,69 | 0,49 | 0,09 |

- Tổng bình phương độ lệch: 0,49 + 7,29 + … + 0,09 = 36,1.
- Chia cho $n = 10$: phương sai = 36,1 / 10 = **3,61 kWh²**. Độ lệch chuẩn = √3,61 = **1,9 kWh**.
- Chia cho $n - 1 = 9$: phương sai = 36,1 / 9 ≈ 4,01 kWh². Độ lệch chuẩn ≈ **2,00 kWh**.

**Đọc bảng.** Ngày 12 kWh một mình chiếm khoảng một nửa tổng 36,1: bình phương làm độ lệch lớn nặng ký hơn hẳn, nên
phương sai rất nhạy với giá trị cực đoan, giống trung bình.

**Chia $n$ hay $n - 1$?** Chia $n$ khi 10 ngày là tất cả những gì ta quan tâm. Chia $n - 1$ khi chúng chỉ là mẫu của
một phân phối thật phía sau: trung bình mẫu tính từ chính 10 số nên nằm gần chúng hơn trung bình thật, làm độ lệch
nhỏ đi; chia số nhỏ hơn bù lại. Vì sao đúng là trừ 1: 10 độ lệch khỏi trung bình mẫu luôn cộng lại bằng 0, biết 9 cái
là suy ra cái thứ 10, nên chỉ còn 9 độ lệch "tự do" để chia. (Mục 8: trung bình là mốc làm tổng bình phương nhỏ nhất,
nên đo tới trung bình mẫu luôn cho tổng nhỏ hơn đo tới trung bình thật.)

$$
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(y_i - \bar y)^2, \qquad s = \sqrt{s^2}
$$

- $y_i - \bar y$: độ lệch của giá trị thứ $i$ khỏi trung bình $\bar y$ (dương là cao hơn trung bình).
- $s^2$: phương sai mẫu, đơn vị là bình phương đơn vị gốc (kWh²), dùng để ước lượng $\sigma^2$ (sigma bình phương):
  phương sai thật của phân phối, cố định nhưng thường không biết.
- $s$: độ lệch chuẩn mẫu, cùng đơn vị với dữ liệu (kWh). $\sigma$ là độ lệch chuẩn thật.
- Bản chia $n$ giống hệt, chỉ thay $n - 1$ bằng $n$.

**Nói bằng lời.** Bình phương từng độ lệch, cộng lại, chia $n - 1$: 36,1 / 9 ≈ 4,01 kWh²; lấy căn ra ≈ 2,00 kWh, tức
mỗi ngày thường lệch khỏi 7,7 kWh cỡ 2 kWh.

```python
np.var(x), np.std(x)                       # (3.61, 1.9)            NumPy mặc định chia n  (ddof=0)
np.var(x, ddof=1), np.std(x, ddof=1)       # (4.0111..., 2.0027...) chia n − 1
s.var(), s.std()                           # (4.0111..., 2.0027...) pandas mặc định chia n − 1
s.std(ddof=0)                              # 1.9
```

`ddof` là số bị trừ khỏi $n$ ở mẫu số (0 là chia $n$, 1 là chia $n - 1$); so giữa các thư viện thì ghi rõ `ddof`.

**Tóm lại.** **Độ lệch chuẩn là căn của trung bình bình phương độ lệch, cùng đơn vị với dữ liệu. Ước lượng từ mẫu
thì chia $n - 1$; NumPy mặc định chia $n$, pandas chia $n - 1$.**

**Tự kiểm tra.** Dãy 2, 4, 6. Tính phương sai theo cả hai cách chia.

<details>
<summary>Đáp án</summary>

Trung bình 4; độ lệch −2, 0, 2; bình phương 4, 0, 4; tổng 8. Chia $n = 3$: 8/3 ≈ 2,67. Chia $n - 1 = 2$: 8/2 = 4, độ
lệch chuẩn 2. Nhầm hay gặp là quên bình phương rồi cộng độ lệch, ra 0.

</details>

## 6. Hệ số lệch

**Trực giác.** Bảng đếm ở mục 1 có ngày 12 kWh tách xa **bên phải**: đuôi phải dài hơn, phân phối **lệch phải**,
**hệ số lệch** (skewness) dương. Vài giá trị rất nhỏ tách xa bên trái thì lệch trái, hệ số âm; đối xứng thì bằng 0.
Đừng nhầm với độ lệch chuẩn (mục 5): độ lệch chuẩn đo độ **rộng**, hệ số lệch đo độ **méo** về một phía.

**Ví dụ số nhỏ — tự tính tay.** Dùng lại các độ lệch $y - 7{,}7$ ở mục 5, lần này **lập phương** (mũ 3). Lập
phương giữ nguyên dấu: độ lệch âm cho số âm, dương cho số dương.

| Độ lệch | −0,7 | −2,7 | 1,3 | −1,7 | 0,3 | 4,3 | −1,7 | 1,3 | −0,7 | 0,3 |
|---|---|---|---|---|---|---|---|---|---|---|
| Lập phương | −0,343 | −19,683 | 2,197 | −4,913 | 0,027 | 79,507 | −4,913 | 2,197 | −0,343 | 0,027 |

- Tổng các lập phương: 53,76. Trung bình (chia 10): 5,376.
- Chia cho lập phương của độ lệch chuẩn (bản chia $n$ ở mục 5): 1,9³ = 6,859.
- Hệ số lệch = 5,376 / 6,859 ≈ **0,78**, dương, tức lệch phải.

**Đọc bảng.** Riêng ô ngày 12 kWh lớn hơn mọi ô âm cộng lại: một ngày cao vọt đủ làm cả dãy lệch phải.

$$
g_1 = \frac{\frac{1}{n}\sum_{i=1}^{n}(y_i - \bar y)^3}{\left(\frac{1}{n}\sum_{i=1}^{n}(y_i - \bar y)^2\right)^{3/2}}
$$

- Tử số: trung bình lập phương độ lệch. Độ lệch lớn bên phải làm nó dương, bên trái làm nó âm.
- Mẫu số: độ lệch chuẩn (bản chia $n$) mũ 3. Chia cho nó để con số không phụ thuộc đơn vị (kWh hay Wh đều ra
  cùng hệ số lệch).
- $g_1$: hệ số lệch. Bằng 0 là đối xứng; dương là đuôi phải dài; âm là đuôi trái dài.

**Nói bằng lời.** Trung bình lập phương độ lệch chia độ lệch chuẩn mũ 3: 5,376 / 1,9³ ≈ 0,78, dương nên đuôi phải dài.

```python
stats.skew(x)                 # 0.7838 — đúng công thức trên
s.skew()                      # 0.9295 — pandas dùng bản có hiệu chỉnh cho mẫu nhỏ
stats.skew(x, bias=False)     # 0.9295 — cùng bản hiệu chỉnh với pandas
stats.skew([2, 8, 9, 9, 10])  # -1.3211 — một số nhỏ tách xa bên trái: lệch trái
```

Giống `ddof` ở mục 5: SciPy và pandas mặc định khác nhau, mẫu lớn thì gần như trùng. Đọc thô theo trị tuyệt đối:
dưới 0,5 là gần đối xứng; 0,5 tới 1 là lệch vừa (như dãy 10 ngày, 0,78); trên 1 là lệch rõ.

**Tóm lại.** **Hệ số lệch dương: vài giá trị rất lớn, đuôi phải dài, trung bình lớn hơn trung vị. Dữ liệu đếm và
doanh số thường như vậy.**

## 7. Phân phối chuẩn và quy tắc 68–95–99,7

Phân phối chuẩn có histogram hình **chuông**, đối xứng, cao nhất tại trung bình. Nó được xác định bởi trung bình
$\mu$ (đọc "muy", vị trí đỉnh) và độ lệch chuẩn $\sigma$ (độ rộng), viết tắt $N(\mu, \sigma^2)$.

**Quy tắc 68–95–99,7.** Với phân phối chuẩn:

| Khoảng | Tỷ lệ giá trị nằm trong khoảng |
|---|---|
| trung bình ± 1 độ lệch chuẩn | 68,27% |
| trung bình ± 2 độ lệch chuẩn | 95,45% |
| trung bình ± 3 độ lệch chuẩn | 99,73% |

**Đọc bảng.** Mỗi lần nới thêm 1 độ lệch chuẩn, phần nằm ngoài giảm mạnh (khoảng 1/3 → 1/20 → 3/1.000), **nếu** dữ
liệu thật sự chuẩn.

**Vì sao ± 1,96?** Khoảng chứa đúng 95% để mỗi phía 2,5% ra ngoài, nên cận trên là quantile 0,975, nằm ở trung bình
cộng 1,96 độ lệch chuẩn. Khoảng 90% dùng ± 1,645; khoảng 99% dùng ± 2,576.

**Ví dụ số nhỏ — tự tính tay.** Giả sử lượng điện lúc 19 giờ có phân phối chuẩn, trung bình 7,7 kWh, độ lệch
chuẩn 1,9 kWh (bản chia $n$, mục 5; dùng bản này cho cả ví dụ).

- Khoảng 68%: 7,7 ± 1,9, tức 5,8 tới 9,6 kWh; 8 trong 10 ngày thật nằm trong.
- Khoảng 95%: 7,7 − 1,96 × 1,9 ≈ 3,98 tới 7,7 + 1,96 × 1,9 ≈ 11,42 kWh.
- Ngày 12 kWh nằm **ngoài** khoảng 95%, điều mà với dữ liệu chuẩn chỉ xảy ra phía trên 1 ngày trong 40. Dãy này
  lệch phải (mục 6), nên giả định chuẩn ở đây đáng ngờ.

**Điểm z.** Số độ lệch chuẩn mà một giá trị cách trung bình gọi là **điểm z**: $z = (y - \bar y)/\text{độ lệch chuẩn}$.
Ngày 12 kWh: $z = (12 - 7{,}7)/1{,}9 \approx 2{,}26$.

$$
P(\mu - 1{,}96\,\sigma \le Y \le \mu + 1{,}96\,\sigma) = 0{,}95 \quad \text{khi } Y \sim N(\mu, \sigma^2)
$$

- $Y \sim N(\mu, \sigma^2)$: "$Y$ có phân phối chuẩn với trung bình $\mu$ và phương sai $\sigma^2$".
- $P(\dots)$: xác suất điều trong ngoặc xảy ra.
- 1,96: quantile 0,975 của phân phối chuẩn có trung bình 0, độ lệch chuẩn 1 (gọi là **chuẩn tắc**).

**Nói bằng lời.** Đại lượng có phân phối chuẩn thì 95% khả năng nằm trong trung bình ± 1,96 độ lệch chuẩn: với 7,7 và
1,9 kWh là 3,98–11,42 kWh. Trong SciPy, `stats.norm.cdf(a)` là tỷ lệ ≤ $a$; `stats.norm.ppf(0.975)` trả về 1,96.

**Tóm lại.** **Với phân phối chuẩn, 95% giá trị nằm trong trung bình ± 1,96 độ lệch chuẩn.**

## 8. Nên dự báo trung bình, trung vị hay quantile?

**Vì sao cần.** Chỉ được đưa **một** con số dự báo thì chọn số nào tuỳ cách bị phạt khi đoán sai.

Quy tắc "đoán lệch thì mất bao nhiêu" gọi là **hàm mất mát**. Ba quy tắc hay gặp:

- **Sai số bình phương**: lệch 2 thì mất 4, lệch 3 thì mất 9. Lệch lớn bị phạt rất nặng.
- **Sai số tuyệt đối**: lệch bao nhiêu mất bấy nhiêu, không kể dấu.
- **Phạt lệch không đều**: đoán thiếu (thấp hơn thực tế) mất nhiều hơn đoán thừa, hoặc ngược lại.

**Ví dụ số nhỏ — tự tính tay.** Dùng một con số $c$ làm dự báo cho cả 10 ngày, cộng mức phạt của 10 ngày. Dòng
$c = 8$:

- Độ lệch $y - 8$: −1, −3, 1, −2, 0, 4, −2, 1, −1, 0.
- Tổng bình phương: 1 + 9 + 1 + 4 + 0 + 16 + 4 + 1 + 1 + 0 = 37.
- Tổng tuyệt đối: 1 + 3 + 1 + 2 + 0 + 4 + 2 + 1 + 1 + 0 = 15.

| Dự báo $c$ (kWh) | 5 | 6 | 7 | 7,5 | 7,7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| Tổng sai số bình phương | 109 | 65 | 41 | 36,5 | **36,1** | 37 | 53 | 89 |
| Tổng sai số tuyệt đối | 27 | 19 | **15** | **15** | **15** | **15** | 19 | 27 |

**Đọc bảng.**

- Hàng 2 nhỏ nhất tại $c = 7{,}7$, đúng **trung bình**.
- Hàng 3 nhỏ nhất (15) với mọi $c$ từ 7 tới 8, đoạn chứa **trung vị** 7,5.

**Phạt lệch không đều — tự tính tay.** Giả sử mua điện trước theo con số dự báo $c$. Thiếu (thực tế cao hơn $c$) phải
mua gấp, mất 4 đồng mỗi kWh thiếu. Thừa (thực tế thấp hơn $c$) phải bán lỗ, mất 1 đồng mỗi kWh thừa. Tính mẫu $c = 8$:
các ngày 9, 9, 12 thiếu tổng 1 + 1 + 4 = 6 kWh, mất 4 × 6 = 24; các ngày 5, 6, 6, 7, 7 thừa tổng 3 + 2 + 2 + 1 + 1 = 9
kWh, mất 9. Tổng 33 đồng.

| Dự báo $c$ (kWh) | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|
| Chi phí 10 ngày (đồng) | 73 | 48 | 33 | **28** | 33 | 38 | 43 |

**Đọc bảng.** Rẻ nhất ở $c = 9$, đúng quantile 0,8 của dãy (mục 4), không phải trung bình 7,7. Quy tắc chung: gọi
$C_u$ là giá mỗi đơn vị thiếu, $C_o$ là giá mỗi đơn vị thừa. Con số tốt nhất là quantile mức
$\tau = C_u / (C_u + C_o)$. Ở đây $4 / (4 + 1) = 0{,}8$. Thiếu và thừa đắt như nhau thì $\tau = 0{,}5$, tức trung vị.

**Công thức.** Hàm mất mát cho quantile mức $\tau$ (đọc là "tau"), còn gọi là **pinball loss**:

$$
L_\tau(y, c) = \begin{cases} \tau\,(y - c) & \text{nếu } y \ge c \text{ (đoán thiếu)} \\ (1-\tau)\,(c - y) & \text{nếu } y < c \text{ (đoán thừa)} \end{cases}
$$

- $y$: giá trị thực tế; $c$: con số dự báo.
- $\tau$: mức quantile muốn nhắm, từ 0 tới 1.

**Nói bằng lời.** Với $\tau = 0{,}8$: thiếu phạt 0,8 mỗi kWh, thừa phạt 0,2, tỷ lệ 4 : 1 như bảng trên, nên tốt nhất là
quantile 0,8.

**Tóm lại.** **Phạt bình phương → dự báo trung bình; phạt tuyệt đối → trung vị; phạt thiếu, thừa không đều → quantile
$C_u/(C_u + C_o)$.**

**Tự kiểm tra.** Một cuộc thi chấm bằng **MAE** (trung bình sai số tuyệt đối). Dữ liệu doanh số lệch phải mạnh. Nên
nộp con số nào: trung bình hay trung vị của các giá trị có thể xảy ra?

<details>
<summary>Đáp án</summary>

Trung vị: sai số tuyệt đối nhỏ nhất tại trung vị. Dữ liệu lệch phải kéo trung bình lên cao hơn trung vị, nên nộp
trung bình bị MAE phạt nhiều hơn. "Trung bình luôn tốt nhất" chỉ đúng khi chấm bằng sai số bình phương.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> - **Vì sao con số tốt nhất là quantile mức $C_u/(C_u + C_o)$?** Nhích $c$ lên 1 kWh: mỗi ngày đang thiếu bớt thiếu,
>   lời $C_u$; mỗi ngày còn lại thừa thêm, mất $C_o$. Nhích còn có lời khi tỷ lệ ngày thiếu lớn hơn
>   $C_o/(C_u + C_o)$. Vậy dừng khi tỷ lệ ngày đủ bằng $C_u/(C_u + C_o)$, đúng định nghĩa quantile. Thay số: dừng khi
>   còn 1/5 số ngày thiếu, tức ở quantile 0,8.
> - Gneiting (2011) chứng minh tổng quát: sai số bình phương "nhắm" trung bình, sai số tuyệt đối nhắm trung vị,
>   pinball loss mức $\tau$ nhắm quantile $\tau$; MAPE nhắm một đại lượng lạ (Phụ lục D).

## 9. Hiệp phương sai và tương quan

**Trực giác.** Ngày nóng hơn bình thường cũng dùng điện nhiều hơn bình thường thì hai biến **cùng chiều**: tích hai
độ lệch dương (dương × dương hoặc âm × âm). Trung bình các tích đó (chia $n - 1$ như mục 5) là **hiệp phương sai**.
Chia thêm cho độ lệch chuẩn của mỗi biến để bỏ đơn vị, ta được **hệ số tương quan** $r$, luôn trong −1 tới 1.

**Ví dụ số nhỏ — tự tính tay.** Năm ngày, nhiệt độ $x$ (°C) và lượng điện $y$ (kWh):

| Ngày | 1 | 2 | 3 | 4 | 5 | Tổng |
|---|---|---|---|---|---|---|
| $x$ (°C) | 25 | 27 | 29 | 31 | 33 | |
| $y$ (kWh) | 6 | 7 | 9 | 8 | 10 | |
| $x - \bar x$ (với $\bar x = 29$) | −4 | −2 | 0 | 2 | 4 | |
| $y - \bar y$ (với $\bar y = 8$) | −2 | −1 | 1 | 0 | 2 | |
| Tích hai độ lệch | 8 | 2 | 0 | 0 | 8 | **18** |
| $(x - \bar x)^2$ | 16 | 4 | 0 | 4 | 16 | **40** |
| $(y - \bar y)^2$ | 4 | 1 | 1 | 0 | 4 | **10** |

- Hiệp phương sai (chia $n - 1 = 4$): 18 / 4 = **4,5** °C·kWh. Dương, nên cùng chiều.
- Tương quan: $r = 18 / \sqrt{40 \times 10} = 18 / 20 =$ **0,9**.

**Đọc bảng.** Hàng "Tích" không có ô âm: không ngày nào nóng hơn thường lệ mà lại dùng ít điện hơn. $r = 0{,}9$: cùng
chiều mạnh, gần một đường thẳng.

$$
\operatorname{cov}(x, y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar x)(y_i - \bar y), \qquad
r = \frac{\sum_{i}(x_i - \bar x)(y_i - \bar y)}{\sqrt{\sum_{i}(x_i - \bar x)^2 \, \sum_{i}(y_i - \bar y)^2}}
$$

- $x_i, y_i$: cặp giá trị của ngày thứ $i$; $\bar x, \bar y$: trung bình của từng biến.
- $\operatorname{cov}(x, y)$: hiệp phương sai. Dương là cùng chiều, âm là ngược chiều. Độ lớn phụ thuộc đơn vị.
- $r$: hệ số tương quan (Pearson). Không có đơn vị, luôn từ −1 tới 1.

**Nói bằng lời.** Tổng tích độ lệch chia căn của (tổng bình phương độ lệch $x$ × của $y$): 18 / √(40 × 10) = 0,9.

**Đọc giá trị $r$.** 1 (hoặc −1): nằm đúng trên một đường thẳng đi lên (đi xuống); 0,7–0,9: cùng chiều khá mạnh; 0:
không có quan hệ **đường thẳng** (vẫn có thể có quan hệ cong).

Tự tính $r$ = hiệp phương sai / (độ lệch chuẩn $x$ × độ lệch chuẩn $y$) thì cả ba phải cùng một cách chia. Trộn
`np.cov` (chia $n - 1$) với `np.std` (chia $n$) ra 1,125, lớn hơn 1, vô lý.

**Ba bẫy của tương quan.**

1. **Tương quan ≠ nhân quả.** Bán kem và đuối nước cùng tăng vào mùa hè, cả hai do trời nóng; kem không gây đuối
   nước.
2. **Chỉ đo quan hệ đường thẳng.** $x$ = −2, −1, 0, 1, 2 và $y = x^2$ = 4, 1, 0, 1, 4: $y$ phụ thuộc hoàn toàn vào
   $x$, nhưng $r = 0$.
3. **Một điểm cực đoan đổi được cả kết quả.** Năm cặp (1; 5), (2; 3), (3; 4), (4; 2), (5; 4) có $r \approx −0{,}42$;
   thêm cặp (20; 20) thì $r \approx 0{,}96$. Luôn vẽ **biểu đồ chấm** (mỗi cặp một chấm) trước khi tin $r$.

**Bẫy riêng của chuỗi thời gian: tương quan giả.** Hai chuỗi cùng có **xu hướng** (cùng đi lên theo thời gian) có
$r$ cao dù không liên quan: hai chuỗi 100 bước sinh độc lập (seed 2026), mỗi chuỗi là tổng dồn các bước ngẫu nhiên (ví dụ
+1, +1, −1, +1 → 1, 2, 1, 2: vài bước cùng chiều liền nhau đẩy chuỗi đi xa) nên tự trôi thành xu
hướng, cho $r = 0{,}90$. Lấy **sai phân** (mỗi bước
trừ bước trước) rồi tính lại: $r \approx −0{,}02$. Buổi 8 học kỹ.

**Tóm lại.** **Tương quan $r$ (−1…1) đo quan hệ đường thẳng giữa hai biến. Nó không phải nhân quả, và dễ bị một điểm
cực đoan hay xu hướng chung đánh lừa.**

## 10. Kiểm định giả thuyết và p-value

**Vì sao cần.** Khoá dùng kiểm định để hỏi chuỗi có **dừng** không (trung bình và độ dao động không đổi, buổi 7), hay
mô hình A có hơn B không.

**Trực giác.** Nghi một đồng xu bị làm lệch, ta không chứng minh thẳng "nó lệch" mà **giả sử nó cân đối**, rồi hỏi:
nếu cân đối thật, kết quả vừa thấy có hiếm không? Rất hiếm thì nghi giả định đó.

- **Giả thuyết không** $H_0$: giả định mặc định, thường là "không có gì đặc biệt". Ở đây: đồng xu cân đối, xác suất
  ngửa bằng 0,5.
- **Giả thuyết đối** $H_1$: điều ta nghi. Ở đây: đồng xu thiên về mặt ngửa, xác suất ngửa lớn hơn 0,5.
- **p-value**: **nếu $H_0$ đúng**, xác suất thấy kết quả lệch **cỡ này hoặc lệch hơn nữa** theo hướng $H_1$.
- **Mức ý nghĩa** $\alpha$ (đọc "alpha"): ngưỡng chọn **trước** khi xem dữ liệu, hay dùng 0,05 (tức 5%). p-value
  nhỏ hơn $\alpha$ thì **bác bỏ** $H_0$; không thì **không bác bỏ**.

**Ví dụ số nhỏ — tự tính tay.** Tung đồng xu 10 lần, được **9 lần ngửa**.

1. $H_0$: đồng xu cân đối. Khi đó mỗi dãy 10 lần tung (ví dụ NNSNNNNNNN, N = ngửa, S = sấp) có xác suất như nhau:
   $(1/2)^{10} = 1/1.024$.
2. Kết quả "lệch cỡ này hoặc hơn" theo hướng nhiều ngửa là: 9 ngửa hoặc 10 ngửa.
3. Đếm số dãy có đúng 9 ngửa: lần sấp duy nhất nằm ở 1 trong 10 vị trí, nên có 10 dãy. Có đúng 10 ngửa: 1 dãy.
4. p-value = (10 + 1) / 1.024 = 11 / 1.024 ≈ **0,011**.
5. So với $\alpha = 0{,}05$: 0,011 < 0,05, nên **bác bỏ $H_0$**. Kết quả này quá hiếm nếu đồng xu cân đối.

$$
\text{p-value} = P(\text{kết quả lệch bằng hoặc hơn kết quả đã thấy} \mid H_0 \text{ đúng})
= \sum_{k=9}^{10} \binom{10}{k} \left(\tfrac12\right)^{10}
$$

- Dấu $\mid$ đọc là "biết rằng", "với điều kiện".
- $\binom{10}{k}$: số cách chọn $k$ vị trí ngửa trong 10 lần tung, tức số **tổ hợp** chập $k$ của 10. Ở phổ thông viết
  là $C_{10}^{k}$; trong Python là `comb(10, k)`. Ví dụ $\binom{10}{9} = 10$, $\binom{10}{10} = 1$.
- $(1/2)^{10}$: xác suất của mỗi dãy cụ thể khi đồng xu cân đối.

**Nói bằng lời.** Nếu đồng xu cân đối, cơ hội ra từ 9 ngửa trở lên là (10 + 1)/1.024 ≈ 1,1%, nhỏ hơn ngưỡng 5%, nên
bác bỏ giả định "cân đối".

**1. "Không bác bỏ" không có nghĩa là "chứng minh $H_0$ đúng".** Giả sử đồng xu thật ra **lệch**, xác suất ngửa
0,7. Với 10 lần tung, ta chỉ bác bỏ khi được từ 9 ngửa trở lên (8 ngửa cho p-value 56/1.024 ≈ 0,055). Nếu xác suất
ngửa là $p$, một dãy có $k$ ngửa có xác suất $p^k (1-p)^{10-k}$, nhân với số dãy $\binom{10}{k}$. Với $p = 0{,}7$:
$10 \times 0{,}7^9 \times 0{,}3 + 0{,}7^{10} \approx 0{,}121 + 0{,}028 = 0{,}149$. Vậy khoảng 85% số lần, kiểm định
**không phát hiện** đồng xu lệch này: "không bác bỏ" thường chỉ nghĩa là **dữ liệu chưa đủ**.

**2. p-value không phải xác suất $H_0$ đúng.** p = 0,011 **không** có nghĩa "đồng xu cân đối với xác suất 1,1%":
p-value tính khi **giả sử $H_0$ đúng**. Ví dụ: hộp 990 đồng cân đối và 10 đồng lệch (xác suất ngửa 0,9), tung mỗi đồng
10 lần. Xác suất ra từ 9 ngửa trở lên: đồng cân đối 11/1.024 ≈ 0,011, đồng lệch ≈ 0,736. Dự kiến 990 × 0,011 ≈ 10,6
đồng cân đối và 10 × 0,736 ≈ 7,4 đồng lệch bị bác bỏ, tức 10,6/(10,6 + 7,4) ≈ 59% số đồng bị bác bỏ là đồng cân đối; tỷ lệ này tuỳ hộp có bao nhiêu đồng lệch từ đầu.

**Báo động giả.** Khi $H_0$ đúng, tỷ lệ bác bỏ oan không quá $\alpha$, nên chạy nhiều kiểm định thì chắc chắn gặp vài
kết quả "có ý nghĩa" do may rủi. Mô phỏng 1.000 đồng cân đối (seed 2026): 15 đồng, tức 1,5%, bị bác bỏ oan. Thấp hơn 5% vì p-value nhảy bậc: chỉ "≥ 9
ngửa" có p < 0,05, và xác suất đó là 11/1.024 ≈ 1,1%.

**Đọc một kiểm định trong khoá.** Luôn đọc $H_0$ của nó trước. Buổi 7 có hai kiểm định tính dừng với $H_0$ ngược nhau
("chuỗi không dừng" và "chuỗi dừng"); p-value nhỏ chỉ bác bỏ **đúng giả định của kiểm định đó**.

**Tóm lại.** **p-value < mức ý nghĩa thì bác bỏ $H_0$. Không bác bỏ ≠ chứng minh $H_0$; p-value không phải xác suất
$H_0$ đúng.**

**Tự kiểm tra.** Kiểm định so sai số của hai mô hình cho p = 0,30, với $H_0$ là "hai mô hình tốt như nhau". Có được
viết "đã chứng minh hai mô hình tốt như nhau" không?

<details>
<summary>Đáp án</summary>

Không. p = 0,30 > 0,05 nên **không bác bỏ** $H_0$. Điều đó chỉ nói dữ liệu chưa đủ để thấy khác biệt; có thể có khác
biệt thật nhưng quá ít dữ liệu để phát hiện (như đồng xu lệch 0,7 ở trên). Viết đúng: "chưa thấy bằng chứng hai mô
hình khác nhau".

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> - Ví dụ trên là **kiểm định một phía** ($H_1$: thiên về ngửa). Nếu $H_1$ là "lệch về bất kỳ phía nào", ta cộng
>   cả hai phía: ≥ 9 ngửa hoặc ≥ 9 sấp, p-value = 22/1.024 ≈ 0,021 (`stats.binomtest(9, 10)`).
> - Bác bỏ oan khi $H_0$ đúng (đoạn "Báo động giả") gọi là **sai lầm loại I**. Không bác bỏ khi $H_0$ sai là **sai
>   lầm loại II**. Xác suất bác bỏ được khi $H_0$ sai gọi là **lực kiểm định** (power):
>   ở ví dụ đồng xu 0,7 là 0,149.
> - p-value cũng không đo độ lớn hay tầm quan trọng của hiệu ứng (Wasserstein & Lazar, 2016).

## 11. Luật số lớn và định lý giới hạn trung tâm

**Độc lập.** Hai lần đo **độc lập** khi biết kết quả lần này không giúp đoán lần kia, như tung xúc xắc hai lần.
Lượng điện hôm nay và hôm qua thì không: hôm qua nóng, dùng nhiều, hôm nay cũng hay vậy. Chuỗi mà giá trị gần nhau
giống nhau gọi là có **tự tương quan**. Mức bám nhau ký hiệu $\rho$ (đọc "rô"), là tương quan (mục 9) giữa mỗi giờ và
giờ liền trước: 0 là không bám, gần 1 là giờ này gần như lặp lại giờ trước.

**Trực giác.** Tung xúc xắc một lần có thể ra 1 hay 6, nhưng trung bình 1.000 lần gần như chắc chắn gần 3,5: càng
nhiều lần đo độc lập, trung bình mẫu càng gần trung bình thật (**luật số lớn**). Trung bình của 30 lần tung, lặp rất
nhiều lần, có histogram **hình chuông** dù một lần tung có phân phối phẳng (**định lý giới hạn trung tâm**, CLT, viết
tắt tên tiếng Anh *central limit theorem*).

**Ví dụ số — mô phỏng (seed 2026).** Trung bình của $m$ lần tung xúc xắc, lặp 10.000 lần cho mỗi $m$:

| Số lần tung $m$ | Độ lệch chuẩn của trung bình (mô phỏng) | Công thức $1{,}708/\sqrt{m}$ | 95% trung bình nằm trong |
|---|---|---|---|
| 1 | 1,71 | 1,708 | 1 – 6 |
| 10 | 0,544 | 0,540 | 2,4 – 4,6 |
| 100 | 0,171 | 0,171 | 3,16 – 3,84 |
| 1.000 | 0,0545 | 0,054 | 3,39 – 3,61 |

Số 1,708 là độ lệch chuẩn của **một** lần tung. Tính như mục 5 trên sáu mặt 1…6 (trung bình 3,5): phương sai
17,5/6 = 35/12 ≈ 2,917, chia 6 vì đây là cả phân phối chứ không phải mẫu; căn ra ≈ 1,708.

**Đọc bảng.** Cột 2 khớp cột 3: $m$ gấp 10 thì độ lệch chuẩn giảm √10 lần. Cột cuối co dần quanh 3,5: luật số lớn.

**Vì sao chia $\sqrt m$ mà không chia $m$?** Với các lần đo độc lập, **phương sai của tổng** bằng tổng các phương sai:
tổng 100 lần tung có phương sai 100 × 2,917 = 291,7. Trung bình là tổng chia 100, mà chia một đại lượng cho 100 thì
phương sai (đo bằng bình phương đơn vị) chia 100² = 10.000: còn 0,02917. Căn lên, độ lệch chuẩn của trung bình là √0,02917 ≈ 0,171 = 1,708/√100.

**Công thức.** Nếu $n$ lần đo **độc lập**, **cùng phân phối** (mọi lần đo lấy từ cùng một phân phối, như tung cùng một
con xúc xắc), có trung bình $\mu$ và độ lệch chuẩn $\sigma$ **hữu hạn** (là một con số cụ thể, không lớn vô cùng):

$$
\text{độ lệch chuẩn của } \bar y = \frac{\sigma}{\sqrt n}, \qquad \bar y \text{ có phân phối gần } N\!\left(\mu, \frac{\sigma^2}{n}\right) \text{ khi } n \text{ lớn}
$$

- $\sigma$: độ lệch chuẩn của **một** lần đo (xúc xắc: 1,708).
- $\sigma/\sqrt n$: độ lệch chuẩn của **trung bình** $n$ lần đo, còn gọi là **sai số chuẩn**.

**Nói bằng lời.** Trung bình $n$ lần đo độc lập dao động ít hơn một lần đo $\sqrt n$ lần: 1,708 / √100 ≈ 0,171.

**Khi nào hai định lý này không cứu bạn.**

- **Không độc lập.** Chuỗi tự tương quan dương: $n$ giờ chứa ít thông tin hơn $n$ lần đo độc lập, nên $\sigma/\sqrt n$
  **quá nhỏ** và khoảng tính từ nó hẹp sai.
- **Đuôi quá dày.** Với phân phối như Cauchy, giá trị cực đoan hay gặp tới mức phương sai không hữu hạn, nên trung
  bình không ổn định dần dù $n$ lớn (hộp Nâng cao).

**Tóm lại.** **Trung bình $n$ lần đo độc lập dao động $\sigma/\sqrt n$ và có dạng hình chuông. Tự tương quan hay đuôi
quá dày phá điều kiện này.**

**Tự kiểm tra.** Độ lệch chuẩn của lượng điện một giờ là 2 kWh. Trung bình 400 giờ **độc lập** có độ lệch chuẩn bao
nhiêu? Nếu 400 giờ đó liên tiếp nhau thì con số thật lớn hơn hay nhỏ hơn?

<details>
<summary>Đáp án</summary>

2 / √400 = 0,1 kWh. Giờ liên tiếp (tự tương quan dương) thì con số thật **lớn hơn** 0,1, vì 400 giờ đó "đáng giá" ít hơn
400 lần đo độc lập. Nhầm hay gặp: chia 400 thay vì √400.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> **Cỡ mẫu hiệu dụng.** Với chuỗi mà mỗi bước bằng $\rho$ lần bước trước cộng nhiễu (mô hình AR(1), buổi 17), $n$
> quan sát đáng giá xấp xỉ $n_{\text{eff}} \approx n\,(1-\rho)/(1+\rho)$ quan sát độc lập (Bretherton và cộng sự,
> 1999). Mô phỏng $n = 200$, lặp 5.000 lần (seed 2026): $\rho = 0{,}5$ cho $n_{\text{eff}}$ 66,2 (công thức 66,7);
> $\rho = 0{,}9$ cho 10,7 (công thức 10,5), tức 200 giờ chỉ đáng giá khoảng 11 lần đo độc lập.
>
> **Đuôi quá dày.** Mô phỏng 200 lần mỗi cỡ mẫu (seed 2026), đo độ trải của trung bình bằng IQR (mục 4): với Cauchy
> là 1,650 ở $n$ = 10 và vẫn 1,653 ở $n$ = 100.000; với phân phối chuẩn thì giảm từ 0,4157 xuống 0,0042.

## 12. Khoảng tin cậy và khoảng dự báo

- **Khoảng tin cậy** cho một con số **cố định** chưa biết, như lượng điện **trung bình thật** lúc 19 giờ. Thêm dữ
  liệu thì nó co lại.
- **Khoảng dự báo** cho **một ngày cụ thể sắp tới**. Dù vô hạn dữ liệu, từng ngày vẫn dao động, nên nó không co về 0.

**Ví dụ số nhỏ — tự tính tay.** 10 ngày: trung bình 7,7 kWh, độ lệch chuẩn (chia $n - 1$) 2,00 kWh.

- Khoảng tin cậy 95% cho **trung bình thật**, dùng sai số chuẩn $s/\sqrt n$ (mục 11):
  7,7 ± 1,96 × 2,003 / √10 = 7,7 ± 1,24 → khoảng **6,46–8,94 kWh**.
- Khoảng dự báo 95% cho **ngày mai**, gần đúng, giả định phân phối chuẩn:
  7,7 ± 1,96 × 2,003 = 7,7 ± 3,93 → khoảng **3,77–11,63 kWh**.

Khoảng dự báo rộng gấp √10 ≈ 3,2 lần. (Mẫu nhỏ thì sách dùng hệ số hơi lớn hơn 1,96, từ Student-t ở mục 14.)

$$
\text{khoảng tin cậy: } \bar y \pm 1{,}96\,\frac{s}{\sqrt n}, \qquad \text{khoảng dự báo (gần đúng): } \hat y \pm 1{,}96\,\hat\sigma
$$

- $\bar y$, $s$, $n$: trung bình, độ lệch chuẩn, số quan sát của mẫu.
- $\hat y$: con số dự báo; $\hat\sigma$: ước lượng độ lệch chuẩn của sai số dự báo (sai số = thực tế − dự báo).
  Ở ví dụ trên, dự báo cho mọi ngày là trung bình 7,7, nên sai số là $y - 7{,}7$ và $\hat\sigma$ chính là $s = 2{,}00$.
- 1,96: quantile 0,975 của phân phối chuẩn (mục 7).

**Nói bằng lời.** Khoảng tin cậy dùng độ dao động của **trung bình** (chia thêm √n) nên hẹp; khoảng dự báo dùng độ dao
động của **một ngày** nên rộng.

**Nghĩa đúng của "khoảng tin cậy 95%".** Trung bình thật cố định; cái ngẫu nhiên là **khoảng** (mẫu khác cho khoảng
khác). "95%" nói về **cách dựng**: lấy mẫu lặp lại rất nhiều lần thì khoảng 95% số khoảng chứa trung bình thật. Với
**một** khoảng đã tính xong, trung bình thật hoặc nằm trong, hoặc không; đừng nói "nằm trong 6,46–8,94 với xác suất
95%". Mục 13 chấm đúng theo ý này.

**Khi dữ liệu lệch, "± 1,96" sai hình dạng.** **log** (logarit tự nhiên) của một số là "phải lấy $e \approx 2{,}718$
mũ bao nhiêu để ra số đó"; nó nén số lớn lại (1, 10, 100 có log ≈ 0; 2,3; 4,6). Đại lượng có log theo phân phối
chuẩn gọi là **log-chuẩn**: luôn dương, đuôi phải dài, giống doanh số.

Mô phỏng (seed 2026) ba mức lệch, mỗi mức 200 quan sát log-chuẩn, dựng khoảng $\bar y \pm 1{,}96\,s$ rồi chấm trên quan
sát mới:

| $\sigma_{\log}$ (độ lệch chuẩn của log) | Hệ số lệch | Nằm trong | Dưới cận dưới | Trên cận trên |
|---|---|---|---|---|
| 0,5 | 1,75 | 95,1% | 0,0% | 4,9% |
| 1,0 | 6,18 | 95,6% | 0,0% | 4,4% |
| 1,5 | 33,5 | 96,5% | 0,0% | 3,5% |

**Đọc bảng.** Cột "nằm trong" trông đúng 95%, nhưng cả 5% rơi ra đều ở phía trên (đúng ra 2,5% mỗi phía), vì cận dưới
âm: rủi ro phía trên bị đánh giá thấp. Dùng quantile 2,5% và 97,5% của mẫu thì mỗi phía rơi ra khoảng 3%.

Giả định của "± 1,96" (sách FPP — *Forecasting: Principles and Practice* — mục 5.5): sai số có phân phối chuẩn, không
tự tương quan, độ dao động không đổi.

**Tóm lại.** **Khoảng tin cậy (cho trung bình thật) co lại khi thêm dữ liệu; khoảng dự báo (cho giá trị tương lai)
luôn rộng hơn. "± 1,96" chỉ hợp dữ liệu gần chuẩn.**

**Tự kiểm tra.** Có 10.000 ngày dữ liệu thay vì 10. Khoảng nào co lại rõ, khoảng nào gần như không đổi?

<details>
<summary>Đáp án</summary>

Khoảng tin cậy co lại rõ, vì chia cho √10.000 = 100 thay vì √10. Khoảng dự báo gần như không đổi, vì từng ngày vẫn
dao động cỡ 2 kWh dù ta biết trung bình rất chính xác. Nhầm hay gặp là nghĩ nhiều dữ liệu thì dự báo từng ngày sẽ
chính xác tuỳ ý.

</details>

## 13. Bootstrap

**Vì sao cần.** Trung vị hay quantile 0,9 không có công thức khoảng tin cậy gọn như trung bình.

**Trực giác.** **Bootstrap** coi dữ liệu đang có là "cả thế giới" và rút lại từ đó **có hoàn lại** (một số có thể được
rút nhiều lần, số khác không được rút) để xem một con số dao động cỡ nào.

**Ví dụ số nhỏ — tự tính tay.** Từ 7, 5, 9, 6, 8, 12, 6, 9, 7, 8, một lần rút có hoàn lại (seed 2026) ra:

7, 5, 7, 6, 6, 8, 7, 6, 6, 6

Số 7 được rút 3 lần, số 12 không lần nào; trung bình lần rút này 64 / 10 = 6,4 kWh. Lặp 1.000 lần, quantile 2,5% và
97,5% của 1.000 trung bình là **6,6 và 8,9 kWh**: khoảng tin cậy 95% bootstrap, rất gần công thức mục 12 (6,46–8,94).

**Công thức.** Không có công thức đóng; đây là một quy trình:

1. Lặp $B$ lần (ví dụ $B = 1.000$): rút $n$ số từ dữ liệu, có hoàn lại; tính con số quan tâm $\hat\theta^*_b$.
2. Khoảng 95% là quantile 2,5% và 97,5% của $\hat\theta^*_1, \dots, \hat\theta^*_B$.

- $n$: số quan sát gốc (10); $B$: số lần lặp.
- $\hat\theta^*_b$ (đọc "theta sao"): con số tính trên lần rút thứ $b$ (trung bình, trung vị…).

**Nói bằng lời.** Rút lại 10 số có hoàn lại, tính trung bình, lặp 1.000 lần, lấy khoảng giữa 95%: 6,6–8,9 kWh.

```python
rng = np.random.default_rng(2026)
tbs = np.array([rng.choice(x, size=10, replace=True).mean() for _ in range(1000)])
np.quantile(tbs, [0.025, 0.975])                     # [6.6, 8.9]

r = stats.bootstrap((x,), np.mean, n_resamples=9999, method="percentile",
                    rng=np.random.default_rng(2026))
r.confidence_interval                                # low=6.6, high=9.0
```

Đổi `np.mean` thành `np.median` là có khoảng cho trung vị.

**Vì sao bootstrap thường hỏng trên chuỗi thời gian.** Rút từng số là **xáo trộn** thứ tự, tức giả định quan sát
**độc lập** (mục 11), sai trên dữ liệu phụ thuộc (Politis, 2003).

Cách sửa là **block bootstrap**: rút cả **khối** $l$ giờ liền nhau, giữ nguyên thứ tự bên trong khối (Künsch, 1989).
Mô phỏng chuỗi tự tương quan ($\rho = 0{,}7$, 200 bước), dựng khoảng 95% cho trung bình, lặp 400 lần (seed 2026):
rút từng số chỉ **56,5%** số khoảng chứa trung bình thật, vì coi 200 bước như 200 lần đo độc lập; rút khối 20 bước
được 86,8%, tốt hơn rõ nhưng vẫn dưới 95%. Độ dài khối là lựa chọn phải kiểm.

**Tóm lại.** **Bootstrap giả định quan sát độc lập; với chuỗi thời gian phải rút theo khối.**

## 14. Phân phối cho dữ liệu đếm và dữ liệu đuôi dày

| Phân phối | Dùng cho | Điều cần nhớ |
|---|---|---|
| Poisson | đếm sự kiện xảy ra độc lập, đều đặn (cuộc gọi tới tổng đài) | chỉ có một tham số $\mu$ (trung bình); **phương sai = trung bình** |
| Âm nhị thức | đếm có dao động lớn (bán hàng, lượt thuê xe) | phương sai **lớn hơn** trung bình: $\mu + d\,\mu^2$; $d$ là **hệ số phân tán thừa**, $d = 0$ là Poisson, $d$ càng lớn càng phân tán |
| Student-t | sai số hay có giá trị cực đoan (tài chính) | giống chuông chuẩn nhưng **đuôi dày** hơn; tham số $\nu$ (đọc "nuy", gọi là bậc tự do) càng nhỏ đuôi càng dày |

**Ví dụ số nhỏ — tự tính tay.** Xác suất Poisson với trung bình $\mu = 5$ khách/giờ ra đúng 3 khách:

$$
P(Y = k) = \frac{e^{-\mu}\,\mu^k}{k!}
$$

- $k$: số đếm muốn tính xác suất (ở đây 3); $k!$ là $1 \times 2 \times \dots \times k$ ($3! = 6$).
- $e \approx 2{,}718$ là hằng số Euler; $\mu$: số trung bình mỗi giờ.

**Nói bằng lời.** $e^{-5} \times 5^3 / 3! = 0{,}006738 \times 125 / 6 \approx 0{,}140$: khoảng 14% số giờ có đúng 3 khách.

**Kiểm "phương sai = trung bình".** Mười giờ, số khách: 2, 0, 7, 1, 12, 3, 0, 9, 4, 2. Trung bình 4, phương sai (chia
$n - 1$) 16,44. Tỷ lệ phương sai / trung bình ≈ 4,1, lớn hơn 1 nhiều. Dữ liệu này **phân tán thừa**: Poisson không
hợp, âm nhị thức hợp hơn.

**Hệ quả thực tế.** Cùng trung bình 5, quantile 0,95 của Poisson là 9, của âm nhị thức $d = 0{,}5$ là 13. Dùng nhầm
Poisson thì cận trên thấp hơn thực tế 4 khách: giờ cao điểm thiếu người phục vụ.

**Đuôi dày.** Tỷ lệ giá trị cách tâm quá **4 độ lệch chuẩn**: Student-t với $\nu = 3$ (độ lệch chuẩn
$\sqrt 3 \approx 1{,}73$) là 0,0062; chuẩn tắc (mục 7) chỉ 0,00006, nhỏ hơn khoảng 100 lần. $\nu \le 2$ thì không có
phương sai hữu hạn; $\nu = 1$ chính là Cauchy ở mục 11.

**Cẩn thận cách đặt tham số.** SciPy `nbinom` dùng $(n, p)$ với $p = n/(n + \mu)$ và $d = 1/n$ ($n$ ở đây không phải
cỡ mẫu). statsmodels dùng $(\mu, \alpha)$ với $\alpha = d$ (không phải mức ý nghĩa ở mục 10).

**Tóm lại.** **Dữ liệu đếm: tỷ lệ phương sai / trung bình gần 1 thì Poisson được, lớn hơn nhiều thì âm nhị thức.
Dữ liệu đuôi dày thì phân phối chuẩn đánh giá thấp rủi ro.**

## 15. Likelihood và MLE

**Vì sao cần.** ETS, ARIMA (buổi 16–17) chọn tham số bằng **ước lượng hợp lý cực đại** (MLE).

**Trực giác.** Tung đồng xu 10 lần được 7 ngửa; xác suất ngửa $p$ khả dĩ nhất là bao nhiêu? Với mỗi $p$, khả năng ra
đúng kết quả đã thấy gọi là **likelihood** của $p$. Chọn $p$ có likelihood lớn nhất.

**Ví dụ số nhỏ — tự tính tay.** Xác suất một dãy cụ thể có 7 ngửa, 3 sấp là $p^7 (1-p)^3$. (Mục 10 nhân thêm số dãy
$C_{10}^{7} = 120$ để ra xác suất "có đúng 7 ngửa". Ở đây bỏ qua được: nhân mọi cột với cùng 120 không đổi cột nào
lớn nhất.)

| $p$ | 0,5 | 0,6 | 0,7 | 0,8 | 0,9 |
|---|---|---|---|---|---|
| $p^7(1-p)^3$ | 0,000977 | 0,001792 | **0,002224** | 0,001678 | 0,000478 |

Tính mẫu $p = 0{,}5$: $0{,}5^7 \times 0{,}5^3 = 0{,}5^{10} = 1/1.024 \approx 0{,}000977$.

**Đọc bảng.** Hàng 2 tăng rồi giảm, lớn nhất ở $p = 0{,}7$ = 7/10. MLE của xác suất ngửa đúng bằng tỷ lệ ngửa đã thấy.

$$
L(\theta) = P(\text{dữ liệu đã thấy} \mid \theta), \qquad \hat\theta_{\text{MLE}} = \text{giá trị } \theta \text{ làm } L(\theta) \text{ lớn nhất}
$$

- $\theta$: tham số của mô hình (ở đây là $p$).
- $L(\theta)$: likelihood, tức xác suất (hoặc mật độ) của chính dữ liệu đã thấy, nếu tham số là $\theta$.

**Nói bằng lời.** Chọn tham số làm dữ liệu đã thấy "dễ xảy ra nhất": với 7 ngửa / 10 lần là $p = 0{,}7$.

Thực tế máy tính dùng **log-likelihood** (lấy log của $L$, mục 12) vì tích của hàng nghìn xác suất nhỏ sẽ tròn thành 0, còn log biến tích thành tổng
($\log(ab) = \log a + \log b$) nên không bị tròn.

**Nhầm lẫn cần tránh.** Likelihood là xác suất **của dữ liệu khi biết tham số**, không phải **của tham số khi biết
dữ liệu**, giống p-value ở mục 10.

**Tóm lại.** **MLE chọn tham số có likelihood lớn nhất; likelihood không phải xác suất tham số đúng.**

## 16. Hồi quy và R²

**Vì sao cần.** **Hồi quy** tìm công thức đoán một biến từ biến kia: "nóng thêm 1 °C thì dùng thêm bao nhiêu kWh".

**Trực giác.** Kẻ đường thẳng qua các chấm (nhiệt độ; lượng điện) sao cho tổng bình phương **phần dư** (thực tế −
giá trị trên đường) nhỏ nhất. Cách này gọi là **bình phương tối thiểu**, viết tắt OLS (*ordinary least squares*).

**Ví dụ số nhỏ — tự tính tay.** Dùng lại năm ngày ở mục 9 (tổng tích độ lệch 18, tổng bình phương độ lệch $x$ là 40).

- Độ dốc $b = 18 / 40 = 0{,}45$ kWh cho mỗi °C.
- Hệ số chặn $a = \bar y - b\,\bar x = 8 - 0{,}45 \times 29 = −5{,}05$ kWh.
- Đường: lượng điện ≈ −5,05 + 0,45 × nhiệt độ. Ngày 25 °C: −5,05 + 11,25 = 6,2 kWh (thực tế 6).

**R²** đo đường thẳng giải thích được bao nhiêu phần dao động của $y$. Tổng bình phương độ lệch của $y$ quanh trung
bình là 10 (mục 9). Tổng bình phương phần dư quanh đường là 1,9. R² = 1 − 1,9/10 = **0,81**. Với một biến giải thích,
R² đúng bằng $r^2 = 0{,}9^2$.

$$
b = \frac{\sum_i (x_i - \bar x)(y_i - \bar y)}{\sum_i (x_i - \bar x)^2}, \quad a = \bar y - b\,\bar x, \quad R^2 = 1 - \frac{\sum_i (y_i - \hat y_i)^2}{\sum_i (y_i - \bar y)^2}
$$

- $b$: độ dốc (tăng 1 đơn vị $x$ thì $y$ tăng $b$); $a$: giá trị của đường khi $x = 0$.
- $\hat y_i = a + b\,x_i$: giá trị trên đường tại ngày $i$; $y_i - \hat y_i$ là phần dư.

**Nói bằng lời.** R² = 1 − (dao động còn lại sau đường thẳng) / (dao động ban đầu) = 1 − 1,9/10 = 0,81: đường thẳng
giải thích 81% dao động.

**Hai lưu ý khi dùng cho dự báo** (FPP mục 7.3).

- R² không giảm khi thêm biến, kể cả biến vô nghĩa, và không đo độ chính xác khi dự báo: đo sai số trên dữ liệu
  **mô hình chưa thấy** (buổi 15).
- R² cao kèm phần dư tự tương quan mạnh là dấu hiệu **hồi quy giả** (tương quan giả, mục 9).

**Tóm lại.** **R² đo trên dữ liệu đã khớp; R² cao không có nghĩa là dự báo tốt.**

## 17. Bẫy thường gặp

| Bẫy | Vì sao sai | Thay bằng |
|---|---|---|
| `np.quantile` mặc định so với đếm tay | NumPy nội suy | `method="inverted_cdf"` (mục 4) |
| So độ lệch chuẩn NumPy với pandas | NumPy chia $n$, pandas chia $n - 1$ | ghi rõ `ddof` (mục 5) |
| $\bar y \pm 1{,}96\,s$ cho dữ liệu lệch | cận dưới âm, cận trên bị vượt | quantile mẫu (mục 12) |
| Tương quan cao là nhân quả | nguyên nhân thứ ba, xu hướng chung | sai phân, xét cơ chế (mục 9) |
| "Không bác bỏ" là "$H_0$ đúng" | có thể chỉ thiếu dữ liệu | "chưa đủ bằng chứng" (mục 10) |
| Poisson cho mọi dữ liệu đếm | phương sai > trung bình: khoảng hẹp | âm nhị thức (mục 14) |
| Giờ liên tiếp như lần đo độc lập | tự tương quan: khoảng quá hẹp | block bootstrap (mục 11, 13) |
| R² cao là dự báo tốt | đo trên dữ liệu đã khớp | sai số trên dữ liệu chưa thấy (mục 16) |

## Nguồn

Con số chạy ngày 2026-09-18; nguồn tra ngày 2026-09-17.

- Hyndman, R.J. & Fan, Y. (1996). Sample quantiles in statistical packages. *The American Statistician* 50(4), 361–365.
- Tài liệu NumPy (`quantile`, `var`, `std`), pandas (`Series.var`, `Series.skew`), SciPy `stats`:
  <https://numpy.org/doc/stable/>, <https://pandas.pydata.org/docs/>, <https://docs.scipy.org/doc/scipy/reference/stats.html>
- Gneiting, T. (2011). Making and evaluating point forecasts. *JASA* 106(494), 746–762. <https://arxiv.org/abs/0912.0902>
- Wasserstein, R.L. & Lazar, N.A. (2016). The ASA statement on p-values. *The American Statistician* 70(2), 129–133.
- NIST/SEMATECH e-Handbook of Statistical Methods (Poisson, t, Cauchy):
  <https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm>,
  <https://www.itl.nist.gov/div898/handbook/eda/section3/eda3664.htm>,
  <https://www.itl.nist.gov/div898/handbook/eda/section3/eda3663.htm>
- MIT OCW 6.436J, Lecture 17 (CLT): <https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/>
- MIT OCW 18.05, Class 10 (MLE): <https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/>
- Bretherton, C.S. và cộng sự (1999). The effective number of spatial degrees of freedom of a time-varying field.
  *J. Climate* 12(7), 1990–2009.
- Hyndman, R.J. The difference between prediction intervals and confidence intervals: <https://robjhyndman.com/hyndsight/intervals/>
- Hyndman, R.J., Athanasopoulos, G. và cộng sự. *Forecasting: Principles and Practice, the Pythonic Way* (FPP), mục
  5.5, 7.3: <https://otexts.com/fpppy/>
- Efron, B. (1979). Bootstrap methods: another look at the jackknife. *Annals of Statistics* 7(1), 1–26.
- Künsch, H.R. (1989). The jackknife and the bootstrap for general stationary observations. *Annals of Statistics*
  17(3), 1217–1241.
- Politis, D.N. & Romano, J.P. (1994). The stationary bootstrap. *JASA* 89(428), 1303–1313.
- Politis, D.N. (2003). The impact of bootstrap methods on time series analysis: <https://mathweb.ucsd.edu/~politis/impactBOOT.pdf>
