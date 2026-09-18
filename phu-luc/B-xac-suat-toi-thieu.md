# Phụ lục B — Xác suất thống kê tối thiểu cho dự báo

Phụ lục này dành cho người **chưa học thống kê đại học**. Bạn chỉ cần toán phổ thông (cộng, nhân, bình phương,
căn bậc hai, phần trăm) và biết Python cơ bản. Mỗi khái niệm đi theo cùng một nhịp: vì sao cần → ví dụ đời thường
→ **một ví dụ số nhỏ tự tính tay** → công thức → nói lại bằng lời → vài dòng code in ra đúng số vừa tính → tóm lại.

Đọc lần đầu thì đi từ mục 1 tới mục 10 theo thứ tự: mục sau dùng khái niệm của mục trước. Mục 11–16 là phần dùng
nhiều ở nửa sau khoá, đọc khi cần. Buổi 2 dạy lại các ý này kèm lab. Các buổi khác gặp từ lạ thì tra ở đây.

Mọi con số dưới đây lấy từ lần chạy thật ngày 2026-09-18, trong môi trường của buổi 2 (Python 3.12 với NumPy,
pandas 3 và SciPy). Mô phỏng ngẫu nhiên đều dùng `np.random.default_rng(2026)`, tức **seed** (hạt giống) 2026:
cùng seed thì chạy lại ra đúng cùng con số.

## Mục lục

- [Tra nhanh](#tra-nhanh)
- [1. Biến ngẫu nhiên và phân phối](#1-biến-ngẫu-nhiên-và-phân-phối)
- [2. Trung bình](#2-trung-bình)
- [3. Trung vị](#3-trung-vị)
- [4. Quantile (phân vị)](#4-quantile-phân-vị)
- [5. Phương sai và độ lệch chuẩn](#5-phương-sai-và-độ-lệch-chuẩn)
- [6. Hệ số lệch](#6-hệ-số-lệch)
- [7. Phân phối chuẩn và quy tắc 68–95–99,7](#7-phân-phối-chuẩn-và-quy-tắc-6895997)
- [8. Nên dự báo trung bình, trung vị hay quantile?](#8-nên-dự-báo-trung-bình-trung-vị-hay-quantile)
- [9. Hiệp phương sai và tương quan](#9-hiệp-phương-sai-và-tương-quan)
- [10. Kiểm định giả thuyết và p-value](#10-kiểm-định-giả-thuyết-và-p-value)
- [11. Luật số lớn và định lý giới hạn trung tâm](#11-luật-số-lớn-và-định-lý-giới-hạn-trung-tâm)
- [12. Khoảng tin cậy và khoảng dự báo](#12-khoảng-tin-cậy-và-khoảng-dự-báo)
- [13. Bootstrap](#13-bootstrap)
- [14. Phân phối cho dữ liệu đếm và dữ liệu đuôi dày](#14-phân-phối-cho-dữ-liệu-đếm-và-dữ-liệu-đuôi-dày)
- [15. Likelihood và MLE](#15-likelihood-và-mle)
- [16. Hồi quy và R²](#16-hồi-quy-và-r²)
- [17. Bẫy thường gặp](#17-bẫy-thường-gặp)
- [Nguồn](#nguồn)

## Tra nhanh

| Từ | Nghĩa một câu | Mục |
|---|---|---|
| biến ngẫu nhiên | đại lượng chưa biết trước giá trị, chỉ biết giá trị nào dễ xảy ra hơn | 1 |
| phân phối | danh sách các giá trị có thể có và mỗi giá trị hay gặp tới đâu | 1 |
| bảng đếm, histogram | đếm mỗi giá trị xuất hiện mấy lần; histogram là biểu đồ cột của phép đếm đó | 1 |
| mẫu | các số liệu ta thật sự có trong tay, lấy ra từ một phân phối ta không thấy hết | 1 |
| trung bình | tổng chia số lượng | 2 |
| trung vị | số đứng giữa khi xếp tăng dần | 3 |
| quantile mức $q$ | giá trị nhỏ nhất mà ít nhất $q$ phần số liệu nhỏ hơn hoặc bằng nó | 4 |
| phương sai, độ lệch chuẩn | các số thường cách trung bình bao xa | 5 |
| hệ số lệch | phân phối có đuôi dài về một phía không, phía nào | 6 |
| phân phối chuẩn | phân phối hình chuông; 95% giá trị nằm trong trung bình ± 1,96 độ lệch chuẩn | 7 |
| hàm mất mát | quy tắc tính "mất bao nhiêu" khi dự báo lệch khỏi thực tế | 8 |
| hiệp phương sai, tương quan | hai đại lượng có cùng tăng cùng giảm không | 9 |
| kiểm định, $H_0$, p-value, mức ý nghĩa | cách quyết định dữ liệu có đủ bằng chứng bác bỏ một giả định không | 10 |
| độc lập | biết kết quả lần này không giúp đoán lần kia | 11 |
| luật số lớn, định lý giới hạn trung tâm | trung bình của nhiều lần đo ổn định dần và có dạng hình chuông | 11 |
| khoảng tin cậy, khoảng dự báo | khoảng cho một con số cố định chưa biết, và khoảng cho một giá trị tương lai | 12 |
| bootstrap | rút lại ngẫu nhiên từ chính dữ liệu để xem một con số dao động cỡ nào | 13 |
| Poisson, âm nhị thức, Student-t | các phân phối cho dữ liệu đếm và dữ liệu hay có giá trị cực đoan | 14 |
| likelihood, MLE | dữ liệu "hợp" với một giá trị tham số tới đâu; chọn tham số hợp nhất | 15 |
| hồi quy, R² | đường thẳng đoán một biến từ biến khác; R² đo đường đó giải thích được bao nhiêu | 16 |

---

## 1. Biến ngẫu nhiên và phân phối

**Vì sao cần.** Lượng điện nhà bạn dùng lúc 19 giờ ngày mai là bao nhiêu? Không ai biết chắc. Nhưng nhìn các
ngày trước, ta biết con số nào hay gặp, con số nào hiếm. Dự báo tốt là nói ra được điều đó.

**Trực giác.** Một **biến ngẫu nhiên** là đại lượng chưa biết trước giá trị. Ta chỉ biết nó có thể nhận những
giá trị nào, và giá trị nào dễ xảy ra hơn. Tung một con xúc xắc: kết quả là biến ngẫu nhiên, nhận 1 tới 6.
**Phân phối** của nó là bảng "mỗi giá trị có thể có · khả năng của giá trị đó". Xúc xắc cân đối có phân phối:
mỗi mặt có xác suất 1/6.

Với dữ liệu thật, ta không có sẵn bảng xác suất. Ta chỉ có những lần đã quan sát, gọi là **mẫu**. Đếm xem mỗi giá
trị xuất hiện mấy lần, ta được một **bảng đếm**. Chia số lần gặp cho tổng số quan sát, ta được **tỷ lệ** của mỗi
giá trị. Bảng tỷ lệ này là hình dung gần đúng của phân phối thật.

Sách thống kê gọi số lần gặp là "tần số" và tỷ lệ là "tần suất". Khoá học không dùng hai tên đó theo nghĩa này, vì
trong khoá "tần suất" là khoảng cách thời gian giữa hai lần đo (dữ liệu theo giờ, theo ngày), còn "tần số" dành cho
phân tích chu kỳ (Phụ lục E). Ở đây ta nói "số lần gặp" và "tỷ lệ".

**Ví dụ số nhỏ — tự tính tay.** Mười ngày qua, lúc 19 giờ nhà dùng (kWh):

7, 5, 9, 6, 8, 12, 6, 9, 7, 8

Phụ lục này dùng **cùng dãy 10 số này** cho gần như mọi ví dụ. Đếm từng giá trị:

| Lượng điện (kWh) | 5 | 6 | 7 | 8 | 9 | 12 |
|---|---|---|---|---|---|---|
| Số ngày | 1 | 2 | 2 | 2 | 2 | 1 |
| Tỷ lệ | 0,1 | 0,2 | 0,2 | 0,2 | 0,2 | 0,1 |

**Đọc bảng.** Hàng "Tỷ lệ" cộng lại bằng 1. Các giá trị 6–9 kWh hay gặp nhất. 12 kWh chỉ gặp một lần, nằm tách xa
các số còn lại. Từ bảng này có thể trả lời "bao nhiêu phần số ngày dùng không quá 8 kWh?": 1 + 2 + 2 + 2 = 7 ngày
trên 10, tức 0,7.

**Histogram** là biểu đồ cột của bảng đếm. Trục ngang là giá trị, chiều cao cột là số lần gặp. Khi có nhiều
giá trị khác nhau, ta gộp chúng thành từng khoảng (ví dụ 4–6, 6–8 kWh) rồi đếm theo khoảng. Vẽ bằng ký tự, mỗi
dấu `#` là một ngày:

```text
 5 kWh  #
 6 kWh  ##
 7 kWh  ##
 8 kWh  ##
 9 kWh  ##
12 kWh  #
```

**Cách đọc hình.**

1. **Trục ngang** (ở đây là cột bên trái): lượng điện lúc 19 giờ, kWh.
2. **Trục dọc** (ở đây là độ dài hàng): số ngày.
3. **Ký hiệu**: mỗi `#` là một ngày.
4. **Nhìn vào đâu**: phần lớn dấu `#` dồn ở 6–9 kWh; hàng 12 kWh đứng tách riêng, xa phía trên.
5. **Kết luận**: lượng điện thường ở 6–9 kWh, thỉnh thoảng có ngày cao vọt.

**Công thức.** Tỷ lệ của giá trị $v$ trong mẫu:

$$
\hat p(v) = \frac{\text{số lần gặp } v}{n}
$$

- $n$: số quan sát trong mẫu. Ở đây $n = 10$.
- $\hat p(v)$: tỷ lệ số lần gặp giá trị $v$. Dấu mũ $\hat{\ }$ nghĩa là "ước lượng từ mẫu", không phải con số
  thật của phân phối.

**Nói bằng lời.** Tỷ lệ của một giá trị là số lần gặp nó chia cho tổng số lần đo. Giá trị 6 kWh gặp 2 lần trên
10 ngày, nên $\hat p(6) = 2/10 = 0{,}2$.

**Code.**

```python
import numpy as np
import pandas as pd

x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # kWh lúc 19 giờ, 10 ngày
s = pd.Series(x)
s.value_counts().sort_index()                    # đếm: 5→1, 6→2, 7→2, 8→2, 9→2, 12→1
s.value_counts(normalize=True).sort_index()      # tỷ lệ: 5→0.1, 6→0.2, ..., 12→0.1
(x <= 8).mean()                                  # 0.7 — tỷ lệ ngày dùng không quá 8 kWh
```

`(x <= 8)` cho một dãy True/False; `.mean()` coi True là 1 và False là 0, nên ra đúng tỷ lệ số ngày thoả điều kiện.
Để vẽ histogram thật, dùng `s.plot.hist(bins=...)` hoặc `plt.hist(x, bins=...)`; `bins` là số khoảng gộp.

**Tóm lại.** **Phân phối cho biết mỗi giá trị có thể xảy ra hay gặp tới đâu. Với dữ liệu thật, ta đếm số lần gặp
mỗi giá trị trong mẫu để hình dung phân phối. Dự báo tốt nhất về tương lai là cả một phân phối, không chỉ một con số.**

**Tự kiểm tra.** Trong 10 ngày trên, tỷ lệ ngày dùng **từ 9 kWh trở lên** là bao nhiêu?

<details>
<summary>Đáp án</summary>

Các ngày dùng 9, 9 và 12 kWh: 3 ngày trên 10, tỷ lệ 0,3. Nhầm hay gặp là chỉ đếm "lớn hơn 9" (chỉ ngày 12 kWh), ra
0,1. Đọc kỹ "từ 9 trở lên" gồm cả 9.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> - **CDF** (hàm phân phối tích luỹ) tại $y$ là tỷ lệ giá trị nhỏ hơn hoặc bằng $y$, viết $F(y) = P(Y \le y)$. Ở
>   ví dụ trên $F(8) = 0{,}7$. CDF tăng dần từ 0 tới 1.
> - Với biến đếm được (số khách, số lần), bảng "giá trị · xác suất" gọi là **PMF** (hàm khối xác suất). Với biến
>   liên tục (nhiệt độ, kWh đo rất mịn), ta dùng **PDF** (hàm mật độ): diện tích dưới đường cong giữa hai mốc là
>   xác suất rơi vào khoảng đó.

---

## 2. Trung bình

**Vì sao cần.** Cần một con số đại diện cho "thường dùng khoảng bao nhiêu", để so ngày này với ngày khác, hay để
làm dự báo đơn giản nhất.

**Trực giác.** Trung bình là chia đều: gom hết lượng điện của 10 ngày lại rồi chia đều cho 10 ngày.

**Ví dụ số nhỏ — tự tính tay.** Tổng 10 ngày: 7 + 5 + 9 + 6 + 8 + 12 + 6 + 9 + 7 + 8 = 77 kWh. Chia 10 ngày:
77 / 10 = **7,7 kWh**.

**Công thức.**

$$
\bar y = \frac{1}{n}\sum_{i=1}^{n} y_i
$$

- $y_i$: giá trị thứ $i$ trong mẫu ($y_1 = 7$, $y_2 = 5$, …).
- $\sum_{i=1}^{n}$: cộng tất cả các số từ số thứ 1 tới số thứ $n$.
- $\bar y$ (đọc là "y gạch"): trung bình của mẫu.

**Nói bằng lời.** Cộng hết các giá trị rồi chia cho số giá trị: 77 / 10 = 7,7 kWh.

**Code.**

```python
import numpy as np
import pandas as pd
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)
s = pd.Series(x)

x.sum(), x.mean()      # (77, 7.7)
s.mean()               # 7.7 — pandas cho cùng kết quả
```

**Một điểm yếu quan trọng.** Trung bình bị một số rất lớn kéo đi. Đổi ngày 12 kWh thành 40 kWh (ví dụ hôm đó có
khách tới nấu tiệc), trung bình nhảy từ 7,7 lên 10,5 kWh. Chín ngày còn lại không đổi, nhưng con số "đại diện" đã
cao hơn mọi ngày trong số đó. Mục 3 đưa ra con số không bị kéo như vậy.

**Tóm lại.** **Trung bình = tổng chia số lượng. Dễ tính, nhưng một giá trị cực đoan có thể kéo nó đi xa.**

**Tự kiểm tra.** Ba ngày dùng 4, 5 và 30 kWh. Trung bình là bao nhiêu, và nó có "giống" ngày nào không?

<details>
<summary>Đáp án</summary>

(4 + 5 + 30) / 3 = 13 kWh. Không ngày nào dùng gần 13 kWh: hai ngày dùng ít hơn nhiều, một ngày nhiều hơn nhiều.
Trung bình không nhất thiết là giá trị "hay gặp".

</details>

---

## 3. Trung vị

**Vì sao cần.** Khi dữ liệu có vài giá trị rất lớn (doanh số ngày lễ, lượng điện ngày có tiệc), ta muốn một con số
"ở giữa" không bị các giá trị đó kéo đi.

**Trực giác.** Xếp 10 ngày theo lượng điện từ ít tới nhiều, như xếp học sinh theo chiều cao. **Trung vị** là
người đứng giữa hàng: một nửa thấp hơn hoặc bằng, một nửa cao hơn hoặc bằng.

**Ví dụ số nhỏ — tự tính tay.**

- Xếp tăng dần: 5, 6, 6, 7, **7**, **8**, 8, 9, 9, 12.
- Có 10 số, là số chẵn, nên có hai số đứng giữa: số thứ 5 (là 7) và số thứ 6 (là 8).
- Quy ước thường dùng: lấy trung bình của hai số giữa, (7 + 8) / 2 = **7,5 kWh**.
- Nếu có số lẻ giá trị thì chỉ có một số đứng giữa. Ví dụ 3, 1, 7, 5, 100 → xếp 1, 3, **5**, 7, 100 → trung vị 5.

Ở dãy 1, 3, 5, 7, 100, trung bình là 23,2 trong khi trung vị là 5. Số 100 kéo trung bình lên, còn trung vị không
đổi dù số lớn nhất là 100 hay 1.000. Tương tự, đổi ngày 12 kWh thành 40 kWh thì trung vị của 10 ngày vẫn là 7,5.

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

**Nói bằng lời.** Xếp tăng dần rồi lấy số ở giữa; nếu có hai số ở giữa thì lấy trung bình của chúng. Với $n = 10$:
lấy trung bình số thứ 5 và số thứ 6, (7 + 8) / 2 = 7,5.

**Code.**

```python
import numpy as np
import pandas as pd
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)
s = pd.Series(x)

np.sort(x)                            # [ 5  6  6  7  7  8  8  9  9 12]
np.median(x), s.median()              # (7.5, 7.5)
np.median([3, 1, 7, 5, 100])          # 5.0
np.mean([3, 1, 7, 5, 100])            # 23.2
```

**Tóm lại.** **Trung vị là số đứng giữa khi xếp tăng dần. Nó không bị vài giá trị cực đoan kéo đi, nên hợp với dữ
liệu có đuôi dài như doanh số hay lượng điện.**

**Tự kiểm tra.** Dãy 4, 5, 30: trung vị là bao nhiêu? So với trung bình 13 ở mục 2, con số nào mô tả "ngày bình
thường" tốt hơn?

<details>
<summary>Đáp án</summary>

Xếp 4, 5, 30; số giữa là 5. Trung vị 5 gần hai trong ba ngày, còn trung bình 13 không gần ngày nào. Với dữ liệu có
một giá trị tách xa, trung vị mô tả ngày bình thường tốt hơn.

</details>

---

## 4. Quantile (phân vị)

**Vì sao cần.** Nhiều quyết định không hỏi "thường dùng bao nhiêu" mà hỏi "phải chuẩn bị bao nhiêu để **đủ trong
80% số ngày**?". Mua điện trước, nhập hàng, xếp ca trực đều là câu hỏi kiểu này. Câu trả lời là một quantile.

**Trực giác.** Trung vị chia dãy đã xếp thành hai nửa bằng nhau. Quantile mở rộng ý đó: chọn một mốc sao cho một
phần cho trước (10%, 80%, 95%…) số liệu nằm dưới hoặc bằng mốc.

**Định nghĩa.** **Quantile mức $q$** (với $q$ từ 0 tới 1) là **giá trị nhỏ nhất** mà **ít nhất** $q$ phần số liệu
nhỏ hơn hoặc bằng nó. Quantile 0,5 là trung vị. Quantile 0,25 và 0,75 còn gọi là **tứ phân vị** dưới và trên.

**Cách đếm tay.**

1. Xếp các giá trị tăng dần.
2. Tính vị trí $q \times n$. Nếu ra số lẻ thập phân thì **làm tròn lên**.
3. Quantile là số đứng ở vị trí đó.

**Ví dụ số nhỏ — tự tính tay.** Dãy đã xếp: 5, 6, 6, 7, 7, 8, 8, 9, 9, 12 ($n = 10$).

- **Quantile 0,8**: vị trí 0,8 × 10 = 8, lấy số thứ 8, là **9 kWh**. Kiểm lại: có 9 trên 10 ngày dùng không quá
  9 kWh (vì có hai ngày cùng dùng 9). Tỷ lệ 0,9 ≥ 0,8, đúng là "ít nhất 80%". Số nhỏ hơn liền trước là 8 thì chỉ có 7
  ngày ≤ 8, tức 70%, chưa đủ. Vậy 9 là giá trị nhỏ nhất thoả điều kiện.
- **Quantile 0,25**: vị trí 0,25 × 10 = 2,5, làm tròn lên thành 3, lấy số thứ 3, là **6 kWh**.
- **Quantile 0,5**: vị trí 0,5 × 10 = 5, lấy số thứ 5, là **7 kWh**.

Chú ý dòng cuối: cách đếm này cho quantile 0,5 là 7, còn trung vị ở mục 3 là 7,5. Cả hai đều chia đôi dãy. Chúng
khác nhau chỉ vì quy ước xử lý khi có hai số đứng giữa. Khi dữ liệu nhiều, khác biệt này rất nhỏ.

**Công thức.**

$$
Q(q) = y_{(k)}, \qquad k = \lceil q \times n \rceil
$$

- $q$: mức quantile, ví dụ 0,8.
- $n$: số giá trị; $y_{(k)}$: số đứng thứ $k$ sau khi xếp tăng dần.
- $\lceil \cdot \rceil$: làm tròn lên số nguyên gần nhất ($\lceil 2{,}5 \rceil = 3$, $\lceil 8 \rceil = 8$).

**Nói bằng lời.** Nhân mức quantile với số giá trị, làm tròn lên, rồi lấy số đứng ở vị trí đó. Với $q = 0{,}25$ và
$n = 10$: 0,25 × 10 = 2,5, làm tròn lên 3, số thứ 3 là 6 kWh.

**Code — và một chỗ hay gây nhầm.** Mặc định `np.quantile` **không** đếm như trên. Nó **nội suy**, tức lấy một
điểm nằm giữa hai số kề nhau, nên có thể ra số lẻ không có trong dữ liệu. Muốn khớp cách đếm tay, thêm
`method="inverted_cdf"`.

```python
import numpy as np
import pandas as pd
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)
s = pd.Series(x)

np.quantile(x, 0.25, method="inverted_cdf")   # 6   — khớp cách đếm tay
np.quantile(x, 0.25)                          # 6.25
                                              # mặc định: nội suy giữa số thứ 3 (6) và số thứ 4 (7)
np.quantile(x, 0.8, method="inverted_cdf")    # 9
np.quantile(x, 0.8)                           # 9.0 — lần này hai cách trùng nhau
s.quantile(0.25)                              # 6.25 — pandas cũng nội suy như mặc định của NumPy
```

| Mức $q$ | Đếm tay (`inverted_cdf`) | `np.quantile` mặc định | Tỷ lệ ngày ≤ giá trị đếm tay |
|---|---|---|---|
| 0,1 | 5 | 5,9 | 0,1 |
| 0,25 | 6 | 6,25 | 0,3 |
| 0,5 | 7 | 7,5 | 0,5 |
| 0,75 | 9 | 8,75 | 0,9 |
| 0,8 | 9 | 9,0 | 0,9 |
| 0,9 | 9 | 9,3 | 0,9 |

**Cách nội suy mặc định** (cột 3): đánh số vị trí **từ 0**, vị trí cần lấy là $(n - 1) \times q$. Với $q = 0{,}25$:
$(10 - 1) \times 0{,}25 = 2{,}25$, nằm giữa vị trí 2 (số 6) và vị trí 3 (số 7), cách vị trí 2 là 0,25. Kết quả
$6 + 0{,}25 \times (7 - 6) = 6{,}25$.

**Đọc bảng.** So cột 2 với cột 3: hai cách lệch nhau tới 0,9 kWh (ở mức 0,1: 5 so với 5,9), vì mẫu chỉ có 10 số. Cột cuối luôn ≥
mức $q$ ở cột đầu: đó chính là điều định nghĩa đòi hỏi. Khi so kết quả với thư viện khác, hãy kiểm cách tính quantile
trước khi nghi code sai.

**Tóm lại.** **Quantile mức $q$ là mốc nhỏ nhất mà ít nhất $q$ phần số liệu nằm dưới hoặc bằng nó. Tính tay: xếp
tăng dần, lấy số thứ $\lceil q \times n \rceil$. `np.quantile` mặc định nội suy; thêm `method="inverted_cdf"` để
khớp cách đếm tay.**

**Tự kiểm tra.** Bảy ngày bán được 4, 9, 2, 7, 5, 3, 8 cái bánh. Quantile 0,8 là bao nhiêu?

<details>
<summary>Đáp án</summary>

Xếp: 2, 3, 4, 5, 7, 8, 9. Vị trí 0,8 × 7 = 5,6, làm tròn lên 6, số thứ 6 là **8 cái**. Kiểm: 6 trên 7 ngày ≤ 8, tức
khoảng 86% ≥ 80%. Nhầm hay gặp là làm tròn xuống thành 5 (ra 7 cái, chỉ 5/7 ≈ 71% ngày ≤ 7, chưa đủ 80%).
`np.quantile` mặc định ra 7,8 vì nội suy.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.** Sách thống kê liệt kê 9 cách tính quantile từ mẫu (Hyndman & Fan,
> 1996). `np.quantile` mặc định dùng cách thứ 7 (`method="linear"`), cách đếm tay ở trên là cách thứ 1
> (`method="inverted_cdf"`). Viết bằng CDF ở mục 1: quantile mức $q$ là giá trị $y$ nhỏ nhất mà $F(y) \ge q$.
> Khoảng cách giữa quantile 0,75 và 0,25 gọi là **IQR** (khoảng tứ phân vị); ở ví dụ trên IQR = 9 − 6 = 3 kWh.

---

## 5. Phương sai và độ lệch chuẩn

**Vì sao cần.** Hai nhà cùng dùng trung bình 7,7 kWh. Nhà A ngày nào cũng 7–8 kWh. Nhà B có ngày 2, có ngày 14.
Dự báo cho nhà B khó hơn nhiều. Ta cần một con số đo **độ dao động**: các giá trị thường cách trung bình bao xa.

**Trực giác.** Lấy mỗi ngày trừ đi trung bình để biết ngày đó lệch bao nhiêu. Không thể cộng thẳng các độ lệch,
vì lệch lên và lệch xuống triệt tiêu nhau (tổng các độ lệch luôn bằng 0). Nên ta bình phương từng độ lệch cho
thành số dương, rồi lấy trung bình. Đó là **phương sai**. Lấy căn bậc hai của phương sai để về lại đơn vị gốc
(kWh), ta được **độ lệch chuẩn**.

**Ví dụ số nhỏ — tự tính tay.** Trung bình là 7,7 kWh (mục 2).

| Ngày | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $y$ (kWh) | 7 | 5 | 9 | 6 | 8 | 12 | 6 | 9 | 7 | 8 |
| Độ lệch $y - 7{,}7$ | −0,7 | −2,7 | 1,3 | −1,7 | 0,3 | 4,3 | −1,7 | 1,3 | −0,7 | 0,3 |
| Bình phương độ lệch | 0,49 | 7,29 | 1,69 | 2,89 | 0,09 | 18,49 | 2,89 | 1,69 | 0,49 | 0,09 |

- Tổng bình phương độ lệch: 0,49 + 7,29 + … + 0,09 = 36,1.
- Chia cho $n = 10$: phương sai = 36,1 / 10 = **3,61 kWh²**. Độ lệch chuẩn = √3,61 = **1,9 kWh**.
- Chia cho $n - 1 = 9$: phương sai = 36,1 / 9 ≈ 4,01 kWh². Độ lệch chuẩn ≈ **2,00 kWh**.

**Đọc bảng.** Ngày 6 (12 kWh) lệch 4,3; bình phương lên thành 18,49, chiếm khoảng một nửa tổng 36,1. Bình phương
làm các độ lệch lớn nặng ký hơn hẳn. Vì vậy phương sai rất nhạy với giá trị cực đoan, giống trung bình.

**Chia $n$ hay $n - 1$?** Cả hai đều gặp, và thư viện **mặc định khác nhau**:

- **Chia $n$** là "trung bình bình phương độ lệch" đúng nghĩa đen. Dùng khi 10 ngày này là **tất cả** những gì ta
  quan tâm.
- **Chia $n - 1$** dùng khi 10 ngày chỉ là **mẫu** và ta muốn ước lượng độ dao động của phân phối thật phía sau.
  Lý do: trung bình mẫu 7,7 được tính từ chính 10 số này, nên nó nằm "gần" các số hơn trung bình thật. Độ lệch đo
  tới nó vì vậy nhỏ hơn thực tế một chút. Chia cho số nhỏ hơn ($n - 1$) bù lại đúng phần hụt đó.
- Khác biệt đáng kể khi $n$ nhỏ (10 → 9 là 11%), gần như không đáng kể khi $n$ lớn (1.000 → 999).

Phân biệt hai con số: **phương sai của phân phối** ($\sigma^2$) là con số thật, cố định, thường không biết (một con
xúc xắc cân đối có phương sai đúng bằng 35/12, mục 11). **Phương sai mẫu** ($s^2$) tính từ dữ liệu trong tay, dùng để
ước lượng $\sigma^2$.

Mô phỏng kiểm chứng: rút 100.000 mẫu, mỗi mẫu 5 số, từ một phân phối có phương sai thật bằng 4. Trung bình của
100.000 phương sai **chia $n$** là 3,204, hụt rõ so với 4. **Chia $n - 1$** cho 4,005, gần đúng 4.

**Công thức.**

$$
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(y_i - \bar y)^2, \qquad s = \sqrt{s^2}
$$

- $y_i - \bar y$: độ lệch của giá trị thứ $i$ khỏi trung bình $\bar y$ (dương là cao hơn trung bình).
- $s^2$: phương sai mẫu, đơn vị là bình phương đơn vị gốc (kWh²). Chữ $\sigma^2$ (sigma bình phương) thường dùng
  cho phương sai thật của phân phối.
- $s$: độ lệch chuẩn mẫu, cùng đơn vị với dữ liệu (kWh). $\sigma$ là độ lệch chuẩn thật.
- Bản chia $n$ giống hệt, chỉ thay $n - 1$ bằng $n$.

**Nói bằng lời.** Bình phương từng độ lệch khỏi trung bình, cộng lại, chia cho $n - 1$: 36,1 / 9 ≈ 4,01 kWh². Lấy
căn để về kWh: độ lệch chuẩn ≈ 2,00 kWh. Nghĩa là mỗi ngày thường lệch khỏi 7,7 kWh cỡ 2 kWh.

**Code — nhớ kỹ chỗ mặc định.**

```python
import numpy as np
import pandas as pd
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)
s = pd.Series(x)

np.var(x), np.std(x)                       # (3.61, 1.9)            NumPy mặc định chia n  (ddof=0)
np.var(x, ddof=1), np.std(x, ddof=1)       # (4.0111..., 2.0027...) chia n − 1
s.var(), s.std()                           # (4.0111..., 2.0027...) pandas mặc định chia n − 1
s.std(ddof=0)                              # 1.9
```

`ddof` là "số bị trừ khỏi $n$ ở mẫu số": `ddof=0` chia $n$, `ddof=1` chia $n - 1$. Cùng một dãy mà NumPy và pandas
ra hai con số khác nhau là chuyện bình thường. Luôn ghi rõ `ddof` khi so kết quả.

**Tóm lại.** **Phương sai là trung bình bình phương độ lệch khỏi trung bình; độ lệch chuẩn là căn của nó, cùng đơn
vị với dữ liệu. Chia $n - 1$ khi ước lượng từ mẫu. NumPy mặc định chia $n$, pandas mặc định chia $n - 1$.**

**Tự kiểm tra.** Dãy 2, 4, 6. Tính phương sai theo cả hai cách chia.

<details>
<summary>Đáp án</summary>

Trung bình 4; độ lệch −2, 0, 2; bình phương 4, 0, 4; tổng 8. Chia $n = 3$: 8/3 ≈ 2,67. Chia $n - 1 = 2$: 8/2 = 4, độ
lệch chuẩn 2. Nhầm hay gặp là quên bình phương rồi cộng độ lệch, ra 0.

</details>

---

## 6. Hệ số lệch

**Vì sao cần.** Lượng điện, doanh số, số khách thường có nhiều ngày ở mức vừa và vài ngày rất cao, nhưng không có
ngày nào âm. Phân phối như vậy **lệch**: đuôi kéo dài về một phía. Biết dữ liệu lệch thì biết trung bình và trung
vị sẽ khác nhau, và các công thức giả định "đối xứng" sẽ sai.

**Trực giác.** Nhìn histogram ở mục 1: phần lớn ngày ở 6–9 kWh, một ngày 12 kWh nằm tách xa **bên phải**. Đuôi
phải dài hơn đuôi trái. Ta nói phân phối **lệch phải**, và **hệ số lệch** (skewness) dương. Nếu vài giá trị rất
nhỏ tách xa về bên trái thì lệch trái, hệ số lệch âm. Phân phối đối xứng có hệ số lệch bằng 0.

Đừng nhầm "hệ số lệch" với "độ lệch chuẩn" ở mục 5: độ lệch chuẩn đo độ **rộng**, hệ số lệch đo độ **méo** về một
phía.

**Ví dụ số nhỏ — tự tính tay.** Dùng lại các độ lệch $y - 7{,}7$ ở mục 5, lần này **lập phương** (mũ 3). Lập
phương giữ nguyên dấu: độ lệch âm cho số âm, dương cho số dương.

| Độ lệch | −0,7 | −2,7 | 1,3 | −1,7 | 0,3 | 4,3 | −1,7 | 1,3 | −0,7 | 0,3 |
|---|---|---|---|---|---|---|---|---|---|---|
| Lập phương | −0,343 | −19,683 | 2,197 | −4,913 | 0,027 | 79,507 | −4,913 | 2,197 | −0,343 | 0,027 |

- Tổng các lập phương: 53,76. Trung bình (chia 10): 5,376.
- Chia cho lập phương của độ lệch chuẩn (bản chia $n$ ở mục 5): 1,9³ = 6,859.
- Hệ số lệch = 5,376 / 6,859 ≈ **0,78**, dương, tức lệch phải.

**Đọc bảng.** Ô 79,507 (ngày 12 kWh) lớn hơn tổng trị tuyệt đối của mọi ô âm cộng lại. Một ngày cao vọt đủ làm cả
dãy lệch phải. Dấu hiệu đi kèm: trung bình 7,7 lớn hơn trung vị 7,5, vì ngày 12 kWh kéo trung bình lên.

**Công thức.**

$$
g_1 = \frac{\frac{1}{n}\sum_{i=1}^{n}(y_i - \bar y)^3}{\left(\frac{1}{n}\sum_{i=1}^{n}(y_i - \bar y)^2\right)^{3/2}}
$$

- Tử số: trung bình lập phương độ lệch. Độ lệch lớn bên phải làm nó dương, bên trái làm nó âm.
- Mẫu số: độ lệch chuẩn (bản chia $n$) mũ 3. Chia cho nó để con số không phụ thuộc đơn vị (kWh hay Wh đều ra
  cùng hệ số lệch).
- $g_1$: hệ số lệch. Bằng 0 là đối xứng; dương là đuôi phải dài; âm là đuôi trái dài.

**Nói bằng lời.** Lấy trung bình lập phương độ lệch, chia cho độ lệch chuẩn mũ 3: 5,376 / 1,9³ ≈ 0,78. Số dương, nên
đuôi phải dài hơn.

**Code.**

```python
import numpy as np
import pandas as pd
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)
s = pd.Series(x)

from scipy import stats

stats.skew(x)                 # 0.7838 — đúng công thức trên
s.skew()                      # 0.9295 — pandas dùng bản có hiệu chỉnh cho mẫu nhỏ
stats.skew(x, bias=False)     # 0.9295 — cùng bản hiệu chỉnh với pandas
stats.skew([5, 6, 7, 8, 9])   # 0.0    — đối xứng
stats.skew([2, 8, 9, 9, 10])  # -1.3211 — một số nhỏ tách xa bên trái: lệch trái
```

Giống chuyện `ddof` ở mục 5: SciPy và pandas mặc định khác nhau. Với mẫu lớn, hai bản gần như trùng nhau. Đọc hệ số
lệch theo dấu và độ lớn thô: khoảng −0,5 tới 0,5 coi là gần đối xứng; 0,5 tới 1 (hoặc −1 tới −0,5) là lệch
vừa, như dãy 10 ngày (0,78); trên 1 (hoặc dưới −1) là lệch rõ.

**Tóm lại.** **Hệ số lệch đo phân phối méo về phía nào. Dương: có vài giá trị rất lớn, đuôi phải dài, trung bình
lớn hơn trung vị. Dữ liệu đếm và doanh số thường lệch phải.**

**Tự kiểm tra.** Thu nhập của 100 người trong một xóm có hai tỷ phú. Hệ số lệch âm hay dương? Trung bình hay trung
vị lớn hơn?

<details>
<summary>Đáp án</summary>

Hai tỷ phú là hai giá trị rất lớn bên phải, nên hệ số lệch **dương**. Họ kéo trung bình lên cao, nên **trung bình
lớn hơn trung vị**. Nhầm hay gặp: nghĩ "lệch phải" là phần lớn dữ liệu nằm bên phải; thật ra phần lớn nằm bên trái,
chỉ có đuôi kéo sang phải.

</details>

---

## 7. Phân phối chuẩn và quy tắc 68–95–99,7

**Vì sao cần.** Rất nhiều công thức trong khoá, nhất là khoảng dự báo "± 1,96 lần độ lệch chuẩn", giả định sai số
có **phân phối chuẩn**. Cần biết nó là gì, con số 1,96 từ đâu ra, và khi nào giả định đó sai.

**Trực giác.** Phân phối chuẩn có histogram hình **chuông**: cao nhất ở giữa (tại trung bình), thấp dần đều hai
bên, đối xứng. Chiều cao người trưởng thành cùng giới hay sai số đo của một cái cân gần giống hình này. Một phân
phối chuẩn được xác định hoàn toàn bởi hai số: trung bình $\mu$ (đọc là "muy", vị trí đỉnh) và độ lệch chuẩn
$\sigma$ (độ rộng của chuông). Viết tắt là $N(\mu, \sigma^2)$.

**Quy tắc 68–95–99,7.** Với phân phối chuẩn:

| Khoảng | Tỷ lệ giá trị nằm trong khoảng |
|---|---|
| trung bình ± 1 độ lệch chuẩn | 68,27% |
| trung bình ± 2 độ lệch chuẩn | 95,45% |
| trung bình ± 3 độ lệch chuẩn | 99,73% |

**Đọc bảng.** Đi từ dòng 1 xuống dòng 3: mỗi lần nới thêm 1 độ lệch chuẩn thì phần còn lại bên ngoài giảm mạnh, từ
khoảng 1/3 xuống 1/20 rồi 3/1.000. Giá trị cách trung bình quá 3 độ lệch chuẩn rất hiếm, **nếu** dữ liệu thật sự
chuẩn.

**Vì sao ±1,96 mà không phải ±2?**

- Ta hay muốn một khoảng chứa **đúng 95%**. Khoảng ± 2 chứa 95,45%, hơi nhiều hơn.
- Muốn đúng 95% thì phần bên ngoài là 5%, chia đều hai phía: mỗi phía 2,5%.
- Vậy cận trên là mốc mà 100% − 2,5% = 97,5% giá trị nằm dưới, tức quantile 0,975.
- Với phân phối chuẩn, mốc đó nằm ở trung bình + **1,96** độ lệch chuẩn.

Làm tương tự cho mức khác: khoảng 90% dùng ± 1,645; khoảng 99% dùng ± 2,576.

**Ví dụ số nhỏ — tự tính tay.** Giả sử lượng điện lúc 19 giờ có phân phối chuẩn, trung bình 7,7 kWh, độ lệch
chuẩn 1,9 kWh (bản chia $n$, mục 5; dùng bản này cho cả ví dụ).

- Khoảng 68%: 7,7 − 1,9 = 5,8 tới 7,7 + 1,9 = 9,6 kWh. Trong 10 ngày thật, 8 ngày nằm trong khoảng này.
- Khoảng 95%: 7,7 − 1,96 × 1,9 ≈ 3,98 tới 7,7 + 1,96 × 1,9 ≈ 11,42 kWh.
- Ngày 12 kWh nằm **ngoài** khoảng 95%. Nếu dữ liệu chuẩn, chuyện này chỉ xảy ra 1 ngày trong khoảng 20 ngày, và
  lệch về phía trên chỉ 1 ngày trong 40. Mục 6 đã cho thấy dãy này lệch phải, nên giả định chuẩn ở đây đáng ngờ.

**Điểm z.** Số độ lệch chuẩn mà một giá trị cách trung bình gọi là **điểm z**: $z = (y - \bar y)/\text{độ lệch chuẩn}$.
Ngày 12 kWh, dùng độ lệch chuẩn chia $n$ (1,9): $z = (12 - 7{,}7)/1{,}9 \approx 2{,}26$. Dùng bản chia $n - 1$ (2,00)
thì $z \approx 2{,}15$. Hai bản khác nhau chút ít; luôn ghi rõ dùng bản nào.

**Công thức.**

$$
P(\mu - 1{,}96\,\sigma \le Y \le \mu + 1{,}96\,\sigma) = 0{,}95 \quad \text{khi } Y \sim N(\mu, \sigma^2)
$$

- $Y \sim N(\mu, \sigma^2)$: "$Y$ có phân phối chuẩn với trung bình $\mu$ và phương sai $\sigma^2$".
- $P(\dots)$: xác suất điều trong ngoặc xảy ra.
- 1,96: quantile 0,975 của phân phối chuẩn có trung bình 0, độ lệch chuẩn 1 (gọi là **chuẩn tắc**).

**Nói bằng lời.** Nếu một đại lượng có phân phối chuẩn thì 95% khả năng nó nằm trong trung bình ± 1,96 độ lệch
chuẩn. Với trung bình 7,7 và độ lệch chuẩn 1,9 kWh, đó là khoảng 3,98–11,42 kWh.

**Code.**

```python
import numpy as np

from scipy import stats

stats.norm.cdf(1) - stats.norm.cdf(-1)      # 0.6827  — tỷ lệ trong ± 1 độ lệch chuẩn
stats.norm.ppf(0.975)                       # 1.95996 — quantile 0,975 của chuẩn tắc
stats.norm.ppf([0.95, 0.995])               # [1.64485363 2.5758293] — dùng cho khoảng 90% và 99%

rng = np.random.default_rng(2026)
z = rng.normal(100, 10, size=100_000)       # 100.000 số từ N(100, 10²)
(np.abs(z - 100) <= 1.96 * 10).mean()       # 0.95071 — mô phỏng khớp lý thuyết
```

`stats.norm.cdf(a)` là tỷ lệ giá trị ≤ $a$ (hàm CDF ở mục 1). `stats.norm.ppf(q)` làm ngược lại: nhận mức $q$, trả về
quantile.

**Tóm lại.** **Phân phối chuẩn hình chuông, đối xứng, xác định bởi trung bình và độ lệch chuẩn. Muốn khoảng chứa
đúng 95% giá trị thì lấy trung bình ± 1,96 độ lệch chuẩn. Dữ liệu lệch thì con số 95% này không còn đúng.**

**Tự kiểm tra.** Sai số dự báo (thực tế − dự báo) có phân phối chuẩn, trung bình 0, độ lệch chuẩn 20 MWh. Khoảng nào chứa 95% sai số?
Một giờ sai 70 MWh có bình thường không?

<details>
<summary>Đáp án</summary>

0 ± 1,96 × 20 ≈ −39,2 tới +39,2 MWh. Sai 70 MWh có $z = 70/20 = 3{,}5$, vượt 3 độ lệch chuẩn: nếu sai số thật sự
chuẩn thì điều này hiếm hơn 3 lần trên 1.000. Nên kiểm giờ đó (ngoại lai, sự kiện đặc biệt), hoặc nghi giả định chuẩn.

</details>

---

## 8. Nên dự báo trung bình, trung vị hay quantile?

**Vì sao cần.** Khi phải đưa ra **một** con số dự báo, nên đưa trung bình, trung vị hay quantile nào? Câu trả lời
phụ thuộc vào cách ta bị phạt khi đoán sai. Mục này dùng lại dãy 10 ngày của mục 1 (kWh): 7, 5, 9, 6, 8, 12, 6, 9,
7, 8. Xếp tăng dần: 5, 6, 6, 7, 7, 8, 8, 9, 9, 12; trung bình 7,7; trung vị 7,5.

**Trực giác.** Quy tắc "đoán lệch thì mất bao nhiêu" gọi là **hàm mất mát**. Ba quy tắc hay gặp:

- **Sai số bình phương**: lệch 2 thì mất 4, lệch 3 thì mất 9. Lệch lớn bị phạt rất nặng.
- **Sai số tuyệt đối**: lệch bao nhiêu mất bấy nhiêu, không kể dấu. Lệch 2 mất 2, lệch 3 mất 3.
- **Phạt lệch không đều**: đoán thiếu (đoán thấp hơn thực tế) mất nhiều hơn đoán thừa, hoặc ngược lại.

Mỗi quy tắc có một con số "tốt nhất" riêng.

**Ví dụ số nhỏ — tự tính tay.** Dùng một con số $c$ làm dự báo cho cả 10 ngày. Với mỗi $c$, cộng mức phạt của 10
ngày. Tính mẫu dòng $c = 8$:

- Độ lệch $y - 8$: −1, −3, 1, −2, 0, 4, −2, 1, −1, 0.
- Tổng bình phương: 1 + 9 + 1 + 4 + 0 + 16 + 4 + 1 + 1 + 0 = 37.
- Tổng tuyệt đối: 1 + 3 + 1 + 2 + 0 + 4 + 2 + 1 + 1 + 0 = 15.

| Dự báo $c$ (kWh) | 5 | 6 | 7 | 7,5 | 7,7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| Tổng sai số bình phương | 109 | 65 | 41 | 36,5 | **36,1** | 37 | 53 | 89 |
| Tổng sai số tuyệt đối | 27 | 19 | **15** | **15** | **15** | **15** | 19 | 27 |

**Đọc bảng.**

- Hàng 2: nhỏ nhất tại $c = 7{,}7$, đúng bằng **trung bình**. Không có $c$ nào khác cho tổng nhỏ hơn 36,1.
- Hàng 3: nhỏ nhất (15) với **mọi** $c$ từ 7 tới 8, tức quanh **trung vị**. Trung vị 7,5 nằm giữa đoạn đó.
- Với phạt lệch không đều, con số tốt nhất là một **quantile** (xem ngay dưới).

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

Vì sao? Nhích $c$ lên 1 kWh. Mỗi ngày đang **thiếu** bớt thiếu 1 kWh, lời $C_u$. Mỗi ngày còn lại (đủ hoặc thừa) thừa
thêm 1 kWh, mất $C_o$. Gọi $s$ là tỷ lệ ngày đang thiếu: nhích lên có lời khi $C_u\,s > C_o\,(1 - s)$, tức khi
$s > C_o/(C_u + C_o)$. Vậy dừng khi tỷ lệ ngày thiếu còn $C_o/(C_u+C_o)$, nghĩa là tỷ lệ ngày đủ là
$1 - C_o/(C_u + C_o) = C_u/(C_u + C_o)$. Đó chính là định nghĩa quantile mức $\tau$. Thay số: dừng khi còn
$1/5 = 20\%$ ngày thiếu, tức ở quantile 0,8.

**Công thức.** Hàm mất mát cho quantile mức $\tau$ (đọc là "tau"), còn gọi là **pinball loss**:

$$
L_\tau(y, c) = \begin{cases} \tau\,(y - c) & \text{nếu } y \ge c \text{ (đoán thiếu)} \\ (1-\tau)\,(c - y) & \text{nếu } y < c \text{ (đoán thừa)} \end{cases}
$$

- $y$: giá trị thực tế; $c$: con số dự báo.
- $\tau$: mức quantile muốn nhắm, từ 0 tới 1.
- Đoán thiếu $y - c$ đơn vị thì mất $\tau$ lần phần thiếu; đoán thừa thì mất $(1 - \tau)$ lần phần thừa.

**Nói bằng lời.** Với $\tau = 0{,}8$: đoán thiếu bị phạt 0,8 cho mỗi kWh, đoán thừa chỉ bị phạt 0,2. Tỷ lệ 0,8 : 0,2
là 4 : 1, đúng tỷ lệ chi phí thiếu : thừa ở bảng trên. Con số làm tổng phạt nhỏ nhất là quantile 0,8. Với
$\tau = 0{,}5$ hai bên bị phạt như nhau, và con số tốt nhất là trung vị.

**Code.**

```python
import numpy as np
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)

for c in [7, 7.5, 7.7, 8]:
    print(c, ((x - c) ** 2).sum().round(2), np.abs(x - c).sum())
# 7    41    15
# 7.5  36.5  15.0
# 7.7  36.1  15.0
# 8    37    15
```

Kiểm trên dữ liệu lớn và lệch: 10.000 số rút từ một phân phối lệch phải (log-chuẩn, seed 2026: giá trị luôn dương, có vài số rất lớn; mục 12 định nghĩa
kỹ). Tìm con số làm nhỏ
nhất từng hàm mất mát, rồi so với trung bình, trung vị, quantile của chính 10.000 số đó:

| Làm nhỏ nhất | Con số tốt nhất | So với |
|---|---|---|
| trung bình sai số bình phương | 1,644 | trung bình = 1,644 |
| trung bình sai số tuyệt đối | 1,020 | trung vị = 1,020 |
| pinball loss $\tau = 0{,}9$ | 3,583 | quantile 0,9 = 3,583 |

**Đọc bảng.** Mỗi dòng, cột 2 trùng cột 3. Dữ liệu càng lệch thì trung bình và trung vị càng xa nhau (1,644 so với
1,020). Chọn sai hàm mất mát là tối ưu cho sai câu hỏi.

**Tóm lại.** **Bị phạt theo sai số bình phương thì dự báo trung bình. Theo sai số tuyệt đối thì dự báo trung vị. Phạt
thiếu và thừa không đều thì dự báo một quantile. Phải biết dự báo sẽ bị chấm thế nào trước khi chọn con số.**

**Tự kiểm tra.** Một cuộc thi chấm bằng **MAE** (trung bình sai số tuyệt đối). Dữ liệu doanh số lệch phải mạnh. Nên
nộp trung bình hay trung vị của dự báo?

<details>
<summary>Đáp án</summary>

Trung vị: sai số tuyệt đối nhỏ nhất tại trung vị (hàng 3 của bảng ví dụ). Với dữ liệu lệch phải, trung bình bị đuôi
kéo lên cao hơn trung vị, nên nộp trung bình sẽ bị MAE phạt nhiều hơn. Nhầm hay gặp: nghĩ "trung bình luôn là dự báo
tốt nhất"; điều đó chỉ đúng khi chấm bằng sai số bình phương.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.** Gneiting (2011) chứng minh tổng quát: sai số bình phương "nhắm" trung
> bình, sai số tuyệt đối nhắm trung vị, pinball loss mức $\tau$ nhắm quantile $\tau$. Ông cũng chỉ ra MAPE (sai số
> phần trăm tuyệt đối) nhắm một đại lượng lạ, không phải trung vị. Xem Phụ lục D.

---

## 9. Hiệp phương sai và tương quan

**Vì sao cần.** Trời nóng thì nhà dùng nhiều điện hơn không? Quảng cáo tăng thì doanh số tăng không? Trước khi
đưa một biến vào mô hình dự báo, ta muốn đo hai biến "cùng lên cùng xuống" tới đâu.

**Trực giác.** Xét từng ngày. Nếu ngày nóng hơn bình thường cũng là ngày dùng điện nhiều hơn bình thường, và ngày
mát hơn cũng là ngày dùng ít hơn, thì hai biến **cùng chiều**. Nhân độ lệch của nhiệt độ với độ lệch của lượng
điện: cùng chiều thì tích dương (dương × dương hoặc âm × âm). Lấy trung bình các tích đó (chia $n - 1$ thay vì $n$, cùng lý do ở mục 5) ta được **hiệp phương sai**. Chia
thêm cho độ lệch chuẩn của mỗi biến để bỏ đơn vị, ta được **hệ số tương quan** $r$, luôn nằm trong −1 tới 1.

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

**Đọc bảng.** Hàng "Tích" không có ô âm nào: không ngày nào nóng hơn bình thường mà lại dùng ít điện hơn bình
thường. Ngày 3 và 4 góp 0 vì một trong hai biến đúng bằng trung bình. $r = 0{,}9$ gần 1: quan hệ cùng chiều mạnh,
gần một đường thẳng.

**Công thức.**

$$
\operatorname{cov}(x, y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar x)(y_i - \bar y), \qquad
r = \frac{\sum_{i}(x_i - \bar x)(y_i - \bar y)}{\sqrt{\sum_{i}(x_i - \bar x)^2 \, \sum_{i}(y_i - \bar y)^2}}
$$

- $x_i, y_i$: cặp giá trị của ngày thứ $i$; $\bar x, \bar y$: trung bình của từng biến.
- $\operatorname{cov}(x, y)$: hiệp phương sai. Dương là cùng chiều, âm là ngược chiều. Độ lớn phụ thuộc đơn vị.
- $r$: hệ số tương quan (Pearson). Không có đơn vị, luôn từ −1 tới 1.

**Nói bằng lời.** Tương quan = tổng tích các độ lệch, chia cho căn của (tổng bình phương độ lệch $x$ × tổng bình
phương độ lệch $y$): 18 / √(40 × 10) = 0,9.

**Đọc giá trị $r$.**

| $r$ | Nghĩa |
|---|---|
| 1 | cùng chiều, nằm đúng trên một đường thẳng đi lên |
| khoảng 0,7 tới 0,9 | cùng chiều khá mạnh |
| 0 | không có quan hệ **đường thẳng** (có thể vẫn có quan hệ cong) |
| −1 | ngược chiều, nằm đúng trên một đường thẳng đi xuống |

**Code.**

```python
import numpy as np
import pandas as pd

nd = np.array([25, 27, 29, 31, 33])       # °C
dien = np.array([6, 7, 9, 8, 10])         # kWh
np.cov(nd, dien)[0, 1]                    # 4.5   — hiệp phương sai, chia n − 1
np.corrcoef(nd, dien)[0, 1]               # 0.9
pd.Series(nd).corr(pd.Series(dien))       # 0.9

nd_F = nd * 9 / 5 + 32                    # đổi sang độ F
np.cov(nd_F, dien)[0, 1]                  # 8.1   — hiệp phương sai đổi theo đơn vị
np.corrcoef(nd_F, dien)[0, 1]             # 0.9   — tương quan không đổi
```

Trong công thức $r$, phần chia $n - 1$ ở tử số và mẫu số tự triệt tiêu, nên $r$ không phụ thuộc chia $n$ hay $n - 1$.
Nhưng nếu tự tính $r$ = hiệp phương sai / (độ lệch chuẩn $x$ × độ lệch chuẩn $y$), cả ba phải cùng một cách chia.
`np.cov` mặc định chia $n - 1$, `np.std` mặc định chia $n$; trộn hai mặc định đó ra 1,125, lớn hơn 1, vô lý. Dùng
`ddof=1` cho cả hai `np.std` thì ra đúng 0,9.

**Ba bẫy của tương quan.**

1. **Tương quan ≠ nhân quả.** $r$ cao chỉ nói hai biến cùng lên xuống, không nói biến nào gây ra biến nào. Bán kem
   và đuối nước cùng tăng vào mùa hè; cả hai do trời nóng, kem không gây đuối nước.
2. **Chỉ đo quan hệ đường thẳng.** $x$ = −2, −1, 0, 1, 2 và $y = x^2$ = 4, 1, 0, 1, 4: $y$ phụ thuộc hoàn toàn vào
   $x$, nhưng $r = 0$.
3. **Một điểm cực đoan đổi được cả kết quả.** Năm cặp (1; 5), (2; 3), (3; 4), (4; 2), (5; 4) có $r \approx −0{,}42$.
   Thêm một cặp (20; 20) thì $r \approx 0{,}96$. Luôn vẽ **biểu đồ chấm** (mỗi cặp là một chấm: trục ngang $x$, trục dọc $y$) trước khi
   tin $r$.

**Bẫy riêng của chuỗi thời gian: tương quan giả.** Hai chuỗi cùng có **xu hướng** (cùng đi lên theo thời gian) sẽ
có $r$ cao dù không liên quan. Mô phỏng hai chuỗi 100 bước, sinh độc lập, đều tăng dần (seed 2026): $r = 0{,}90$.
Lấy **sai phân** (mỗi bước trừ bước trước, chỉ giữ phần thay đổi) rồi tính lại: $r \approx −0{,}02$. Buổi 8 học kỹ.

**Tóm lại.** **Hiệp phương sai đo hai biến cùng chiều hay ngược chiều, nhưng độ lớn phụ thuộc đơn vị. Tương quan $r$
chuẩn hoá về −1…1. Tương quan không phải nhân quả, chỉ đo quan hệ đường thẳng, và dễ bị một điểm cực đoan hay xu
hướng chung đánh lừa.**

**Tự kiểm tra.** Ba cặp $x$ = 1, 2, 3 và $y$ = 6, 4, 2. Tính $r$.

<details>
<summary>Đáp án</summary>

$\bar x = 2$, $\bar y = 4$. Độ lệch $x$: −1, 0, 1; độ lệch $y$: 2, 0, −2. Tích: −2, 0, −2, tổng −4. Tổng bình phương:
2 và 8. $r = −4/\sqrt{16} = −1$: ngược chiều hoàn hảo. Nhầm hay gặp là quên dấu, ra +1.

</details>

---

## 10. Kiểm định giả thuyết và p-value

**Vì sao cần.** Nhiều buổi dùng "kiểm định": kiểm xem chuỗi có **dừng** không (buổi 7; chuỗi dừng là chuỗi có trung
bình và độ dao động không đổi theo thời gian), sai số của mô hình còn lặp lại theo quy luật nào không, mô hình A có thật
sự tốt hơn mô hình B không. Mọi kiểm định đều theo một logic chung. Hiểu logic đó trên một
đồng xu là đọc được mọi kiểm định.

**Trực giác.** Bạn nghi một đồng xu bị làm lệch. Bạn không chứng minh trực tiếp "nó lệch". Thay vào đó, bạn **giả
sử nó cân đối**, rồi hỏi: "Nếu cân đối thật, kết quả mình vừa thấy có hiếm không?" Nếu rất hiếm, bạn nghi giả định
cân đối. Giống toà án: coi bị cáo vô tội cho tới khi bằng chứng đủ mạnh.

**Các từ cần biết.**

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

Nếu chỉ được **7 lần ngửa**: số dãy có 7, 8, 9, 10 ngửa là 120 + 45 + 10 + 1 = 176. p-value = 176/1.024 ≈ 0,17,
lớn hơn 0,05, nên **không bác bỏ** $H_0$.

**Công thức.**

$$
\text{p-value} = P(\text{kết quả lệch bằng hoặc hơn kết quả đã thấy} \mid H_0 \text{ đúng})
= \sum_{k=9}^{10} \binom{10}{k} \left(\tfrac12\right)^{10}
$$

- Dấu $\mid$ đọc là "biết rằng", "với điều kiện".
- $\binom{10}{k}$: số cách chọn $k$ vị trí ngửa trong 10 lần tung, tức số **tổ hợp** chập $k$ của 10. Ở phổ thông viết
  là $C_{10}^{k}$; trong Python là `comb(10, k)`. Ví dụ $\binom{10}{9} = 10$, $\binom{10}{10} = 1$.
- $(1/2)^{10}$: xác suất của mỗi dãy cụ thể khi đồng xu cân đối.

**Nói bằng lời.** Nếu đồng xu cân đối, cơ hội ra từ 9 ngửa trở lên trong 10 lần là (10 + 1)/1.024 ≈ 1,1%. Vì 1,1% nhỏ
hơn ngưỡng 5% đã chọn, ta bác bỏ giả định "cân đối".

**Code.**

```python
from math import comb
from scipy import stats

sum(comb(10, k) for k in (9, 10)) / 1024                          # 0.0107421875  (= 11/1024)
stats.binomtest(9, 10, p=0.5, alternative="greater").pvalue       # 0.0107421875
stats.binomtest(7, 10, p=0.5, alternative="greater").pvalue       # 0.171875      (= 176/1024)
```

**Hai điều quan trọng nhất — hay bị hiểu sai nhất.**

**1. "Không bác bỏ" không có nghĩa là "chứng minh $H_0$ đúng".** Giả sử đồng xu thật ra **lệch**, xác suất ngửa
0,7. Với 10 lần tung và $\alpha = 0{,}05$, ta chỉ bác bỏ khi được từ 9 ngửa trở lên (vì 8 ngửa cho p-value 56/1.024 ≈
0,055, chưa dưới 0,05). Xác suất đồng xu lệch 0,7 cho từ 9 ngửa trở lên chỉ là 0,149.
Cách tính: nếu xác suất ngửa là $p$, một dãy cụ thể có $k$ ngửa có xác suất $p^k (1-p)^{10-k}$; nhân với số dãy
$\binom{10}{k}$. Với $p = 0{,}7$: $10 \times 0{,}7^9 \times 0{,}3 + 0{,}7^{10} \approx 0{,}121 + 0{,}028 = 0{,}149$. Tức là khoảng 85% số lần, kiểm
định **không phát hiện** đồng xu lệch này. "Không bác bỏ" thường chỉ có nghĩa là **dữ liệu chưa đủ** để kết luận.

**2. p-value không phải xác suất $H_0$ đúng.** p = 0,011 **không** có nghĩa "đồng xu cân đối với xác suất 1,1%".
p-value tính **giả sử $H_0$ đúng**, nên không thể cho biết $H_0$ có đúng không. Ví dụ: một hộp 1.000 đồng xu, 990 đồng
cân đối, 10 đồng lệch (xác suất ngửa 0,9). Tung mỗi đồng 10 lần:

| Loại đồng xu | Số đồng | Xác suất ra ≥ 9 ngửa | Số đồng dự kiến ra ≥ 9 ngửa |
|---|---|---|---|
| cân đối | 990 | 0,0107 | 10,6 |
| lệch 0,9 | 10 | 0,736 | 7,4 |

Cột 3 dòng 2 tính như trên với $p = 0{,}9$: $10 \times 0{,}9^9 \times 0{,}1 + 0{,}9^{10} \approx 0{,}387 + 0{,}349 = 0{,}736$.

**Đọc bảng.** So cột cuối hai dòng. Khoảng 18 đồng ra từ 9 ngửa trở lên, và mọi đồng đó đều bị bác bỏ ở mức 0,05.
Nhưng khoảng 10,6 / 18 ≈ 59% trong số đó là đồng **cân đối**, tức $H_0$ thật ra đúng. Ý chính: p-value của mỗi đồng chỉ
khoảng 0,011, vậy mà trong số các đồng bị bác bỏ, tỷ lệ $H_0$ đúng tới 59%. p-value không phải xác suất $H_0$ đúng.
Tỷ lệ đó còn tuỳ trong hộp có bao nhiêu đồng lệch ngay từ đầu.

**Còn một hệ quả nữa: báo động giả.** Ngưỡng 5% nghĩa là khi $H_0$ đúng, tỷ lệ bác bỏ oan **không quá** 5%. Với 10
lần tung, p-value chỉ nhận vài giá trị nhảy bậc (≥ 8 ngửa: 0,055; ≥ 9 ngửa: 0,011). Vì vậy chỉ có "≥ 9 ngửa" bị bác bỏ,
và tỷ lệ bác bỏ oan thật là 11/1.024 ≈ 1,1%, thấp hơn 5%. Mô phỏng 1.000 đồng xu cân đối, mỗi đồng tung 10 lần (seed
2026): 15 đồng (1,5%) ra ≥ 9 ngửa và bị bác bỏ oan, gần 1,1% như tính. Chạy nhiều kiểm định thì chắc chắn gặp vài kết
quả "có ý nghĩa" do may rủi.

**Đọc một kiểm định trong khoá.** Mỗi kiểm định có $H_0$ riêng; luôn đọc $H_0$ là gì trước. Ví dụ buổi 7 có hai kiểm
định về tính dừng với $H_0$ ngược nhau: một cái giả định "chuỗi không dừng", cái kia giả định "chuỗi dừng". p-value
nhỏ nghĩa là bác bỏ **đúng giả định của kiểm định đó**, không hơn.

**Tóm lại.** **Kiểm định: giả sử $H_0$ đúng, tính p-value = cơ hội thấy kết quả lệch cỡ này hoặc hơn. p-value < mức
ý nghĩa (thường 0,05) thì bác bỏ $H_0$. Không bác bỏ ≠ chứng minh $H_0$. p-value không phải xác suất $H_0$ đúng.**

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
> - Bác bỏ oan khi $H_0$ đúng gọi là **sai lầm loại I**, xác suất không quá $\alpha$ (ở ví dụ
>   đồng xu là 1,1%). Không bác bỏ khi $H_0$ sai là
>   **sai lầm loại II**. Xác suất bác bỏ được khi $H_0$ sai gọi là **lực kiểm định** (power): ở ví dụ đồng xu 0,7 là
>   0,149.
> - Hội Thống kê Hoa Kỳ (Wasserstein & Lazar, 2016) nêu rõ: p-value không đo xác suất giả thuyết đúng, và không đo độ
>   lớn hay tầm quan trọng của hiệu ứng.

---

## 11. Luật số lớn và định lý giới hạn trung tâm

**Vì sao cần.** Hai định lý này giải thích vì sao trung bình của nhiều lần đo đáng tin, và vì sao phân phối chuẩn
xuất hiện khắp nơi. Chúng cũng có điều kiện, và chuỗi thời gian hay vi phạm điều kiện đó.

**Độc lập.** Hai lần đo **độc lập** khi biết kết quả lần này không giúp đoán lần kia. Tung xúc xắc hai lần là độc
lập. Lượng điện hôm nay và hôm qua **không** độc lập: hôm qua nóng, dùng nhiều, thì hôm nay cũng hay nóng, dùng
nhiều. Chuỗi thời gian mà giá trị gần nhau giống nhau như vậy gọi là có **tự tương quan** (tương quan của chuỗi với
chính nó dời lùi một vài bước). Mức bám nhau đó ký hiệu $\rho$ (đọc "rô"): tương quan (mục 9) giữa mỗi giờ và giờ
liền trước. $\rho = 0$ là không bám nhau; $\rho$ gần 1 là giờ này gần như lặp lại giờ trước.

**Trực giác — luật số lớn.** Tung xúc xắc một lần có thể ra 1 hay 6. Tung 1.000 lần rồi lấy trung bình thì gần như
chắc chắn ra gần 3,5 (trung bình của 1…6). Càng nhiều lần đo độc lập, trung bình mẫu càng gần trung bình thật.

**Trực giác — định lý giới hạn trung tâm** (CLT, viết tắt tên tiếng Anh *central limit theorem*). Lấy trung bình của 30 lần tung, lặp lại rất nhiều lần. Các trung
bình đó có histogram **hình chuông**, dù một lần tung có phân phối phẳng (mỗi mặt 1/6).

**Ví dụ số — mô phỏng (seed 2026).** Trung bình của $m$ lần tung xúc xắc, lặp 10.000 lần cho mỗi $m$:

| Số lần tung $m$ | Độ lệch chuẩn của trung bình (mô phỏng) | Công thức $1{,}708/\sqrt{m}$ | 95% trung bình nằm trong |
|---|---|---|---|
| 1 | 1,71 | 1,708 | 1 – 6 |
| 10 | 0,544 | 0,540 | 2,4 – 4,6 |
| 100 | 0,171 | 0,171 | 3,16 – 3,84 |
| 1.000 | 0,0545 | 0,054 | 3,39 – 3,61 |

Số 1,708 là độ lệch chuẩn của **một** lần tung. Mỗi mặt 1…6 có xác suất 1/6, trung bình 3,5. Độ lệch khỏi 3,5 là
−2,5; −1,5; −0,5; 0,5; 1,5; 2,5, bình phương là 6,25; 2,25; 0,25; 0,25; 2,25; 6,25, tổng 17,5. Chia 6 mặt: phương sai
17,5 / 6 = 35/12 ≈ 2,917 (chia 6, không chia 5, vì đây là cả phân phối, không phải một mẫu). Căn: √2,917 ≈ 1,708.

**Đọc bảng.** Dòng $m = 1$: một lần tung luôn ra 1–6, nên cột cuối là 1–6 (thật ra chứa 100%). Đi từ dòng này xuống
dòng dưới, số lần tung gấp 10 thì độ lệch chuẩn của trung bình giảm khoảng √10 ≈
3,16 lần, không phải 10 lần. Cột 2 khớp cột 3: đó là luật "chia cho căn $m$". Cột cuối co dần quanh 3,5: đó là luật
số lớn.

Histogram của 10.000 trung bình, mỗi trung bình từ 30 lần tung (mỗi `#` là 100 trung bình; 12 trung bình nằm ngoài
2,5–4,5 không in ra). Hai hàng giữa lệch nhau (2694 so với 3091) không phải vì lệch tâm: trung bình 30 lần tung chỉ
nhận các giá trị tổng / 30. Khoảng 3,50–3,75 chứa 8 giá trị như thế (tổng 105…112), khoảng 3,25–3,50 chỉ chứa 7 (tổng
98…104):

```text
2.50-2.75    85
2.75-3.00   392 ###
3.00-3.25  1668 ################
3.25-3.50  2694 ##########################
3.50-3.75  3091 ##############################
3.75-4.00  1477 ##############
4.00-4.25   519 #####
4.25-4.50    62
```

**Cách đọc hình.**

1. **Trục ngang** (cột trái): khoảng giá trị của trung bình 30 lần tung.
2. **Trục dọc** (độ dài hàng): số trung bình rơi vào khoảng đó.
3. **Ký hiệu**: mỗi `#` là 100 trung bình.
4. **Nhìn vào đâu**: hàng dài nhất ở giữa, quanh 3,5; hai bên ngắn dần.
5. **Kết luận**: trung bình của nhiều lần tung có hình chuông, dù một lần tung thì phẳng.

**Công thức.** Nếu $n$ lần đo **độc lập**, **cùng phân phối** (mọi lần đo lấy từ cùng một phân phối, như tung cùng một
con xúc xắc, không đổi xúc xắc giữa chừng), có trung bình $\mu$ và độ lệch chuẩn $\sigma$ **hữu hạn** (là một con số
cụ thể, không lớn vô cùng):

$$
\text{độ lệch chuẩn của } \bar y = \frac{\sigma}{\sqrt n}, \qquad \bar y \text{ có phân phối gần } N\!\left(\mu, \frac{\sigma^2}{n}\right) \text{ khi } n \text{ lớn}
$$

- $\sigma$: độ lệch chuẩn của **một** lần đo (xúc xắc: 1,708).
- $\sigma/\sqrt n$: độ lệch chuẩn của **trung bình** $n$ lần đo, còn gọi là **sai số chuẩn**.

**Nói bằng lời.** Trung bình của $n$ lần đo độc lập dao động ít hơn một lần đo $\sqrt n$ lần, và có dạng hình chuông.
Với 100 lần tung: 1,708 / √100 ≈ 0,171.

**Code.**

```python
import numpy as np

rng = np.random.default_rng(2026)
tb = rng.integers(1, 7, size=(10_000, 100)).mean(axis=1)   # 10.000 trung bình, mỗi cái 100 lần tung
tb.std()                                                   # 0.1713 — gần 1,708 / √100 ≈ 0,171
```

**Khi nào hai định lý này không cứu bạn.** Hai điều kiện in đậm ngay trước công thức (**độc lập**, độ lệch chuẩn
**hữu hạn**) hay bị quên.

- **Không độc lập.** Với chuỗi thời gian có tự tương quan dương, $n$ giờ chứa ít thông tin hơn $n$ lần đo độc lập.
  Công thức $\sigma/\sqrt n$ cho con số **quá nhỏ**, nên các khoảng tính từ nó hẹp một cách sai lầm.
- **Đuôi quá dày.** Có những phân phối mà giá trị cực đoan quá hay gặp, đến mức phương sai không hữu hạn. Khi đó
  trung bình không ổn định dần, dù $n$ lớn bao nhiêu. Ví dụ phân phối Cauchy: thỉnh thoảng rút ra một số cực lớn, đủ kéo
  lệch cả trung bình. Mô phỏng ở hộp Nâng cao cho thấy trung bình của 100.000 số Cauchy vẫn dao động mạnh như trung bình
  của 10 số.

**Tóm lại.** **Trung bình của nhiều lần đo độc lập ổn định dần quanh trung bình thật (luật số lớn), dao động
$\sigma/\sqrt n$ và có dạng hình chuông (CLT). Chuỗi thời gian tự tương quan hay đuôi quá dày phá các điều kiện này.**

**Tự kiểm tra.** Độ lệch chuẩn của lượng điện một giờ là 2 kWh. Trung bình 400 giờ **độc lập** có độ lệch chuẩn bao
nhiêu? Nếu 400 giờ đó liên tiếp nhau thì con số thật lớn hơn hay nhỏ hơn?

<details>
<summary>Đáp án</summary>

2 / √400 = 2 / 20 = 0,1 kWh. Nếu là 400 giờ liên tiếp (tự tương quan dương), con số thật **lớn hơn** 0,1, vì 400 giờ
đó "đáng giá" ít hơn 400 lần đo độc lập. Nhầm hay gặp là chia cho 400 thay vì √400, ra 0,005.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> **Cỡ mẫu hiệu dụng.** Gọi $\rho$ (đọc "rô") là tương quan giữa mỗi giờ và giờ liền trước. Với chuỗi mà mỗi bước
> bằng $\rho$ lần bước trước cộng nhiễu (mô hình AR(1), buổi 17), $n$ quan sát đáng giá xấp xỉ
> $n_{\text{eff}} \approx n\,(1-\rho)/(1+\rho)$ quan sát độc lập (dạng đặc biệt của công thức trong Bretherton và
> cộng sự, 1999). Mô phỏng $n = 200$, lặp 5.000 lần (seed 2026), $n_{\text{eff}}$ đo bằng phương sai một quan sát chia
> phương sai của trung bình:
>
> | $\rho$ | mô phỏng | công thức |
> |---|---|---|
> | 0 | 205,9 | 200,0 |
> | 0,5 | 66,2 | 66,7 |
> | 0,9 | 10,7 | 10,5 |
>
> Một chuỗi 200 giờ có $\rho = 0{,}9$ chỉ đáng giá khoảng 11 lần đo độc lập khi ước lượng trung bình.
>
> **Đuôi quá dày.** Phân phối Cauchy có đuôi dày tới mức không có trung bình hữu hạn. NIST viết rằng với Cauchy, lấy
> 1.000 điểm dữ liệu cũng không ước lượng trung bình chính xác hơn lấy 1 điểm. Mô phỏng 200 lần mỗi cỡ mẫu (seed
> 2026), đo độ trải của trung bình mẫu bằng IQR (mục 4):
>
> | $n$ | Cauchy | chuẩn |
> |---|---|---|
> | 10 | 1,650 | 0,4157 |
> | 1.000 | 2,033 | 0,0369 |
> | 100.000 | 1,653 | 0,0042 |
>
> Với phân phối chuẩn, tăng mẫu 100 lần thì độ trải giảm khoảng 10 lần; với Cauchy thì không giảm.

---

## 12. Khoảng tin cậy và khoảng dự báo

**Vì sao cần.** Khoá học ra dự báo dạng khoảng: "ngày mai 100–140 cái, chắc 80%". Có hai loại khoảng rất hay bị
nhầm, và một loại hẹp hơn loại kia nhiều.

**Trực giác.**

- **Khoảng tin cậy** trả lời: "con số **cố định** mà ta chưa biết, ví dụ lượng điện **trung bình thật** lúc 19 giờ,
  nằm trong khoảng nào?". Có thêm dữ liệu thì khoảng này co lại.
- **Khoảng dự báo** trả lời: "lượng điện **một ngày cụ thể sắp tới** sẽ nằm trong khoảng nào?". Dù có vô hạn dữ
  liệu, từng ngày vẫn dao động, nên khoảng này không co về 0.

**Ví dụ số nhỏ — tự tính tay.** 10 ngày: trung bình 7,7 kWh, độ lệch chuẩn (chia $n - 1$) 2,00 kWh.

- Khoảng tin cậy 95% cho **trung bình thật**, dùng sai số chuẩn $s/\sqrt n$ (mục 11):
  7,7 ± 1,96 × 2,00 / √10 = 7,7 ± 1,24 → khoảng **6,46–8,94 kWh**.
- Khoảng dự báo 95% cho **ngày mai**, gần đúng, giả định phân phối chuẩn:
  7,7 ± 1,96 × 2,00 = 7,7 ± 3,93 → khoảng **3,77–11,63 kWh**.

Khoảng dự báo rộng gấp khoảng √10 ≈ 3,2 lần. Với mẫu nhỏ như 10 ngày, sách dùng một hệ số lớn hơn 1,96 một chút
(lấy từ phân phối Student-t, mục 14) và thêm phần bất định của chính trung bình. Ở đây ta giữ 1,96 cho dễ theo.

**Công thức.**

$$
\text{khoảng tin cậy: } \bar y \pm 1{,}96\,\frac{s}{\sqrt n}, \qquad \text{khoảng dự báo (gần đúng): } \hat y \pm 1{,}96\,\hat\sigma
$$

- $\bar y$, $s$, $n$: trung bình, độ lệch chuẩn, số quan sát của mẫu.
- $\hat y$: con số dự báo; $\hat\sigma$: ước lượng độ lệch chuẩn của sai số dự báo (sai số = thực tế − dự báo).
  Ở ví dụ dưới, dự báo cho mọi ngày là trung bình 7,7, nên sai số là $y - 7{,}7$ và $\hat\sigma$ chính là $s = 2{,}00$.
- 1,96: quantile 0,975 của phân phối chuẩn (mục 7).

**Nói bằng lời.** Khoảng tin cậy dùng độ dao động của **trung bình** (chia thêm √n), nên hẹp: 6,46–8,94 kWh. Khoảng dự
báo dùng độ dao động của **một ngày**, nên rộng: 3,77–11,63 kWh.

**Nghĩa đúng của "khoảng tin cậy 95%".** Trung bình thật là một con số cố định, không ngẫu nhiên. Cái ngẫu nhiên là
**khoảng**: lấy một mẫu 10 ngày khác thì ra một khoảng khác. "95%" nói về **cách dựng khoảng**: nếu lặp lại việc lấy mẫu
rất nhiều lần, mỗi lần dựng một khoảng, thì khoảng 95% số khoảng dựng được sẽ chứa trung bình thật. Cách hiểu sai hay
gặp: "trung bình thật nằm trong 6,46–8,94 với xác suất 95%". Với **một** khoảng đã tính xong, trung bình thật hoặc nằm
trong, hoặc không. Mục 13 dùng đúng ý này để chấm: đếm xem bao nhiêu phần số khoảng chứa trung bình thật.

**Code.**

```python
import numpy as np
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)

m, sd, n = x.mean(), x.std(ddof=1), len(x)
m - 1.96 * sd / np.sqrt(n), m + 1.96 * sd / np.sqrt(n)     # (6.4587, 8.9413) — khoảng tin cậy
m - 1.96 * sd, m + 1.96 * sd                               # (3.7746, 11.6254)
                                                           # khoảng dự báo gần đúng
```

**Khi dữ liệu lệch, "± 1,96" sai hình dạng.** Trước hết, **log** (logarit tự nhiên) trả lời câu hỏi: "phải lấy
$e \approx 2{,}718$ mũ bao nhiêu để ra số này?". Ví dụ $\log(e^2) = 2$, $\log(1) = 0$. Log nén số lớn lại: 1, 10, 100
có log ≈ 0; 2,3; 4,6. Phân phối **log-chuẩn** là phân phối của một đại lượng mà **log** của nó có phân phối chuẩn. Giá trị luôn dương và đuôi phải dài, giống doanh số hay lượng điện. Độ rộng của nó đặt bằng
$\sigma_{\log}$, độ lệch chuẩn của log giá trị: $\sigma_{\log}$ càng lớn thì càng lệch.

Mô phỏng (seed 2026): lấy 200 quan sát log-chuẩn, dựng khoảng $\bar y \pm 1{,}96\,s$ ($s$ chia $n - 1$), rồi đếm tỷ lệ
1.000 quan sát **mới** rơi ra ngoài mỗi phía. Lặp 2.000 lần:

| $\sigma_{\log}$ | Hệ số lệch (mục 6) | Tỷ lệ nằm trong | Dưới cận dưới | Trên cận trên | Mỗi phía nên là |
|---|---|---|---|---|---|
| 0,5 | 1,75 | 95,1% | 0,0% | 4,9% | 2,5% |
| 1,0 | 6,18 | 95,6% | 0,0% | 4,4% | 2,5% |
| 1,5 | 33,5 | 96,5% | 0,0% | 3,5% | 2,5% |

**Đọc bảng.** Cột 2 cho thấy cả ba mức đều lệch mạnh (mục 6: trên 1 là lệch rõ). So cột 3 với con số hứa hẹn
95%: trông "đúng". Nhưng so cột 4 và cột 5 với cột cuối: không giá trị nào
rơi dưới cận dưới, còn phía trên bị vượt 3,5–4,9% thay vì 2,5%. Lý do: cận dưới thường **âm** (với $\sigma_{\log}$ từ 1,0 trở lên,
mọi lần lặp đều cho cận dưới âm), trong khi dữ liệu luôn dương. Nếu quyết định dựa vào cận trên (dự phòng công suất,
tồn kho an toàn), rủi ro bị đánh giá thấp. Dùng quantile 2,5% và 97,5% của chính mẫu thì phủ khoảng 94% (ở cả ba mức $\sigma_{\log}$) và không có
cận âm. Tỷ lệ tổng thấp hơn một chút, nhưng phần rơi ra **chia đều hai phía**: khoảng 2,9–3,0% dưới cận dưới và 3,0%
trên cận trên, so với 0% và 3,5–4,9% của cách "± 1,96". Người dùng cận trên được báo đúng rủi ro hơn.

Sách *Forecasting: Principles and Practice* của Hyndman và Athanasopoulos (gọi tắt **FPP**), mục 5.5, nêu các giả
định của khoảng dạng "± 1,96": sai số có phân phối chuẩn, không tự tương quan, độ dao động
không đổi. FPP cũng lưu ý khoảng dự báo của nhiều mô hình **hẹp hơn thực tế** (mục 9.8), vì bỏ qua bất định khi ước
lượng tham số và khi chọn mô hình.

**Tóm lại.** **Khoảng tin cậy dành cho một con số cố định chưa biết (như trung bình thật), co lại khi có thêm dữ
liệu. Khoảng dự báo dành cho một giá trị tương lai, luôn rộng hơn. "± 1,96 độ lệch chuẩn" chỉ đúng hình dạng khi dữ
liệu gần chuẩn.**

**Tự kiểm tra.** Có 10.000 ngày dữ liệu thay vì 10. Khoảng nào co lại rõ, khoảng nào gần như không đổi?

<details>
<summary>Đáp án</summary>

Khoảng tin cậy co lại rõ, vì chia cho √10.000 = 100 thay vì √10. Khoảng dự báo gần như không đổi, vì từng ngày vẫn
dao động cỡ 2 kWh dù ta biết trung bình rất chính xác. Nhầm hay gặp là nghĩ nhiều dữ liệu thì dự báo từng ngày sẽ
chính xác tuỳ ý.

</details>

---

## 13. Bootstrap

**Vì sao cần.** Mục 12 có công thức cho khoảng tin cậy của **trung bình**. Nhưng với trung vị, quantile 0,9, hay
một chỉ số đánh giá phức tạp thì sao? Thường không có công thức gọn. **Bootstrap** thay công thức bằng máy tính.

**Trực giác.** Ta muốn biết: "nếu thu thập lại 10 ngày khác, trung bình sẽ dao động cỡ nào?". Không thể quay lại
thu thập. Bootstrap giả vờ: coi 10 số đang có là "cả thế giới", rồi **rút lại ngẫu nhiên 10 số từ chính chúng, có
hoàn lại** (một số có thể được rút nhiều lần, số khác không được rút). Mỗi lần rút cho một "bộ dữ liệu giả" và một
trung bình. Lặp 1.000 lần, xem 1.000 trung bình đó trải rộng cỡ nào.

**Ví dụ số nhỏ — tự tính tay.** Từ 7, 5, 9, 6, 8, 12, 6, 9, 7, 8, một lần rút có hoàn lại (seed 2026) ra:

7, 5, 7, 6, 6, 8, 7, 6, 6, 6

Số 7 được rút 3 lần, số 12 không được rút lần nào. Trung bình lần rút này: 64 / 10 = 6,4 kWh. Lặp lại 1.000 lần,
được 1.000 trung bình. Quantile 2,5% và 97,5% của chúng là **6,6 và 8,9 kWh**. Đó là khoảng tin cậy 95% bootstrap
cho trung bình. So với công thức ở mục 12 (6,46–8,94 kWh): rất gần.

**Công thức.** Không có công thức đóng; đây là một quy trình:

1. Lặp $B$ lần (ví dụ $B = 1.000$): rút $n$ số từ dữ liệu, có hoàn lại; tính con số quan tâm $\hat\theta^*_b$.
2. Khoảng 95% là quantile 2,5% và 97,5% của $\hat\theta^*_1, \dots, \hat\theta^*_B$.

- $n$: số quan sát gốc (10); $B$: số lần lặp.
- $\hat\theta^*_b$ (đọc "theta sao"): con số tính trên lần rút thứ $b$ (trung bình, trung vị…).

**Nói bằng lời.** Rút lại 10 số có hoàn lại, tính trung bình, lặp 1.000 lần, lấy khoảng giữa 95% của 1.000 trung bình
đó: 6,6–8,9 kWh.

**Code.**

```python
import numpy as np
from scipy import stats
x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # 10 ngày ở mục 1 (kWh)

rng = np.random.default_rng(2026)
tbs = np.array([rng.choice(x, size=10, replace=True).mean() for _ in range(1000)])
np.quantile(tbs, [0.025, 0.975])                     # [6.6, 8.9]

r = stats.bootstrap((x,), np.mean, n_resamples=9999, method="percentile",
                    rng=np.random.default_rng(2026))
r.confidence_interval                                # low=6.6, high=9.0
```

Cận trên 8,9 hay 9,0 khác nhau vì số lần rút (1.000 so với 9.999) và cách SciPy lấy quantile. Khoảng bootstrap là gần
đúng; lệch nhau cỡ này là bình thường.

`stats.bootstrap` của SciPy làm đúng việc này; mặc định nó dùng một biến thể tinh hơn (`method="BCa"`) với 9.999 lần
rút. Đổi `np.mean` thành `np.median` là có ngay khoảng cho trung vị, không cần công thức mới.

**Vì sao bootstrap thường hỏng trên chuỗi thời gian.** Rút từng số một cách ngẫu nhiên là **xáo trộn** thứ tự, làm
mất mọi quan hệ giữa giờ này và giờ kế tiếp. Bootstrap như vậy giả định các quan sát **độc lập** (mục 11). Politis
(2003) chỉ ra: áp lên dữ liệu phụ thuộc, nó cho kết quả sai, vì mọi thông tin về sự phụ thuộc đã bị xáo mất.

Cách sửa là **block bootstrap**: rút cả **khối** $l$ giờ liền nhau, giữ nguyên thứ tự bên trong khối (Künsch, 1989).
Mô phỏng: chuỗi tự tương quan ($\rho = 0{,}7$, 200 bước, trung bình thật bằng 0), dựng khoảng 95% cho trung bình, lặp
400 lần (seed 2026):

| Cách rút lại | Tỷ lệ khoảng chứa trung bình thật (nên là 95%) |
|---|---|
| từng số, độc lập | **56,5%** |
| khối 20 bước liền nhau | 86,8% |

**Đọc bảng.** Dòng 1 hụt rất xa 95%: khoảng quá hẹp vì coi 200 bước như 200 lần đo độc lập. Dòng 2 tốt hơn rõ nhưng
vẫn dưới 95%. Độ dài khối là lựa chọn phải kiểm, không có giá trị đúng cho mọi chuỗi.

**Tóm lại.** **Bootstrap: rút lại có hoàn lại từ chính dữ liệu nhiều lần để thấy một con số dao động cỡ nào, không
cần công thức. Nó giả định quan sát độc lập; với chuỗi thời gian phải rút theo khối.**

**Tự kiểm tra.** Vì sao phải rút **có hoàn lại**? Nếu rút 10 số không hoàn lại từ 10 số thì sao?

<details>
<summary>Đáp án</summary>

Rút 10 số không hoàn lại từ 10 số thì lần nào cũng ra đúng 10 số cũ, chỉ khác thứ tự. Trung bình lần nào cũng 7,7,
không thấy dao động gì. Có hoàn lại thì mỗi lần rút là một bộ khác nhau, mô phỏng việc "thu thập lại dữ liệu".

</details>

---

## 14. Phân phối cho dữ liệu đếm và dữ liệu đuôi dày

**Vì sao cần.** Số khách mỗi giờ, số đơn hàng mỗi ngày là **dữ liệu đếm**: số nguyên, không âm, thường lệch phải.
Lợi suất cổ phiếu có ngày biến động cực lớn thường hơn phân phối chuẩn dự đoán. Dùng phân phối chuẩn cho những dữ
liệu này cho khoảng dự báo sai.

**Ba phân phối hay gặp.**

| Phân phối | Dùng cho | Điều cần nhớ |
|---|---|---|
| Poisson | đếm sự kiện xảy ra độc lập, đều đặn (cuộc gọi tới tổng đài) | chỉ có một tham số $\mu$ (trung bình); **phương sai = trung bình** |
| Âm nhị thức | đếm có dao động lớn (bán hàng, lượt thuê xe) | phương sai **lớn hơn** trung bình: $\mu + d\,\mu^2$ |
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

**Hệ quả thực tế — mô phỏng 100.000 giá trị (seed 2026).** Cùng trung bình 5:

| | Trung bình | Phương sai | Quantile 0,95 |
|---|---|---|---|
| Poisson($\mu = 5$) | 4,99 | 4,98 | 9 |
| Âm nhị thức ($\mu = 5$, $d = 0{,}5$) | 4,99 | 17,37 (lý thuyết 5 + 0,5 × 25 = 17,5) | 13 |

**Đọc bảng.** So hai dòng: cùng trung bình, nhưng quantile 0,95 của âm nhị thức là 13 so với 9. Nếu dữ liệu thật là
âm nhị thức mà ta giả định Poisson, cận trên khoảng dự báo thấp hơn thực tế khoảng 4 khách, và giờ cao điểm bị thiếu
người phục vụ.

**Đuôi dày.** So hai phân phối trên cùng một thang: cách tâm quá **4 độ lệch chuẩn**. Student-t có $\nu = 3$ có độ
lệch chuẩn $\sqrt 3 \approx 1{,}73$, nên 4 độ lệch chuẩn là khoảng 6,93. Tỷ lệ giá trị vượt mốc đó là 0,0062. Với phân
phối chuẩn tắc (mục 7), tỷ lệ vượt 4 độ lệch chuẩn chỉ là 0,00006, nhỏ hơn khoảng 100 lần. $\nu \le 2$ thì không có phương sai hữu hạn; $\nu = 1$ chính là
phân phối Cauchy ở mục 11.

**Code.**

```python
import numpy as np
from scipy import stats

stats.poisson.pmf(3, 5)                          # 0.1404
dem = np.array([2, 0, 7, 1, 12, 3, 0, 9, 4, 2])
dem.var(ddof=1) / dem.mean()                     # 4.11 — lớn hơn 1: phân tán thừa
stats.poisson.ppf(0.95, 5)                       # 9.0
stats.nbinom.ppf(0.95, n=2, p=2 / (2 + 5))       # 13.0 — âm nhị thức trung bình 5, d = 1/n = 0,5
2 * stats.t.sf(4 * np.sqrt(3), df=3)            # 0.0062   — Student-t ν = 3, quá 4 độ lệch chuẩn
2 * stats.norm.sf(4)                             # 6.33e-05 — chuẩn tắc, quá 4 độ lệch chuẩn
```

`sf(a)` là tỷ lệ giá trị **lớn hơn** $a$, tức 1 − CDF (mục 1); nhân 2 để tính cả phía nhỏ hơn −4.

**Hệ số phân tán thừa $d$.** Trong công thức phương sai $\mu + d\,\mu^2$ của âm nhị thức, $d$ đo dữ liệu dao động
mạnh hơn Poisson bao nhiêu: $d = 0$ thì phương sai bằng trung bình, đúng như Poisson; $d$ càng lớn càng phân tán.

**Cẩn thận cách đặt tham số.** `scipy.stats.nbinom` dùng hai tham số $(n, p)$ với $p = n/(n + \mu)$ và $d = 1/n$. Chữ
$n$ ở đây là tham số của phân phối, **không phải** cỡ mẫu.
statsmodels và sách về mô hình tuyến tính tổng quát dùng $(\mu, \alpha)$, trong đó $\alpha$ chính là $d$ ở đây (không
liên quan tới mức ý nghĩa $\alpha$ ở mục 10). Đọc tài liệu của thư viện trước khi truyền
tham số.

**Tóm lại.** **Dữ liệu đếm: kiểm tỷ lệ phương sai / trung bình trước. Gần 1 thì Poisson được; lớn hơn nhiều thì dùng
âm nhị thức, nếu không khoảng dự báo sẽ quá hẹp. Dữ liệu hay có giá trị cực đoan thì phân phối chuẩn đánh giá thấp
rủi ro.**

**Tự kiểm tra.** Số đơn hàng mỗi ngày của hai cửa hàng: A có trung bình 20, phương sai 21; B có trung bình 20, phương
sai 80. Cửa hàng nào dùng Poisson được?

<details>
<summary>Đáp án</summary>

A: tỷ lệ 21 / 20 ≈ 1,05, gần 1, nên Poisson được. B: 80 / 20 = 4, phân tán thừa, nên dùng âm nhị thức. Nhầm hay gặp là
so phương sai với độ lệch chuẩn; điều kiện của Poisson là **phương sai** bằng trung bình.

</details>

---

## 15. Likelihood và MLE

**Vì sao cần.** Nhiều mô hình trong khoá (ETS, ARIMA ở buổi 16–17) tự chọn tham số từ dữ liệu. Cách chọn phổ biến
nhất là **ước lượng hợp lý cực đại** (MLE). Hiểu nó trên đồng xu là đủ để đọc phần còn lại.

**Trực giác.** Tung đồng xu 10 lần được 7 ngửa. Xác suất ngửa $p$ của đồng xu này khả dĩ nhất là bao nhiêu? Thử từng
giá trị $p$, và hỏi: "nếu $p$ là thế này, khả năng ra đúng kết quả mình đã thấy là bao nhiêu?". Con số đó là
**likelihood** của $p$. Chọn $p$ có likelihood lớn nhất.

**Ví dụ số nhỏ — tự tính tay.** Xác suất một dãy cụ thể có 7 ngửa, 3 sấp là $p^7 (1-p)^3$. (Mục 10 nhân thêm số dãy
$C_{10}^{7} = 120$ để ra xác suất "có đúng 7 ngửa". Ở đây bỏ qua được: nhân mọi cột với cùng 120 không đổi cột nào
lớn nhất.)

| $p$ | 0,5 | 0,6 | 0,7 | 0,8 | 0,9 |
|---|---|---|---|---|---|
| $p^7(1-p)^3$ | 0,000977 | 0,001792 | **0,002224** | 0,001678 | 0,000478 |

Tính mẫu $p = 0{,}5$: $0{,}5^7 \times 0{,}5^3 = 0{,}5^{10} = 1/1.024 \approx 0{,}000977$.

**Đọc bảng.** Hàng 2 tăng rồi giảm, lớn nhất ở $p = 0{,}7$ = 7/10. MLE của xác suất ngửa đúng bằng tỷ lệ ngửa đã thấy.

**Công thức.**

$$
L(\theta) = P(\text{dữ liệu đã thấy} \mid \theta), \qquad \hat\theta_{\text{MLE}} = \text{giá trị } \theta \text{ làm } L(\theta) \text{ lớn nhất}
$$

- $\theta$: tham số của mô hình (ở đây là $p$).
- $L(\theta)$: likelihood, tức xác suất (hoặc mật độ) của chính dữ liệu đã thấy, nếu tham số là $\theta$.

**Nói bằng lời.** Chọn tham số làm cho dữ liệu đã thấy "dễ xảy ra nhất". Với 7 ngửa / 10 lần, $p = 0{,}7$ cho
likelihood 0,002224, lớn hơn mọi $p$ khác trong bảng.

**Code.**

```python
import numpy as np

luoi = np.linspace(0.01, 0.99, 99)
luoi[np.argmax(luoi**7 * (1 - luoi)**3)]      # 0.7
```

Thực tế máy tính dùng **log-likelihood** (lấy log của $L$) vì tích của hàng nghìn xác suất nhỏ sẽ tròn thành 0.

**Một nhầm lẫn cần tránh.** Likelihood là xác suất **của dữ liệu khi biết tham số**, không phải xác suất **của tham
số khi biết dữ liệu** (MIT 18.05). Giống như p-value ở mục 10: nói "$p = 0{,}7$ có likelihood 0,0022" không có nghĩa
"$p = 0{,}7$ đúng với xác suất 0,0022".

**Tóm lại.** **Likelihood đo dữ liệu đã thấy hợp với một giá trị tham số tới đâu. MLE chọn tham số có likelihood lớn
nhất. Likelihood không phải xác suất tham số đúng.**

**Tự kiểm tra.** Tung đồng xu 20 lần được 5 ngửa. MLE của xác suất ngửa là bao nhiêu?

<details>
<summary>Đáp án</summary>

5 / 20 = 0,25, tức tỷ lệ ngửa đã thấy (giống 7/10 ở ví dụ). Nhầm hay gặp là trả lời 0,5 vì "đồng xu thường cân đối":
MLE chỉ dựa vào dữ liệu đã thấy, không dựa vào điều ta tin trước.

</details>

---

## 16. Hồi quy và R²

**Vì sao cần.** Tương quan (mục 9) nói hai biến cùng chiều mạnh cỡ nào. **Hồi quy** đi thêm một bước: tìm công thức
đoán một biến từ biến kia, ví dụ "nóng thêm 1 °C thì dùng thêm bao nhiêu kWh".

**Trực giác.** Kẻ một đường thẳng qua các chấm (nhiệt độ; lượng điện) sao cho các chấm nằm gần đường nhất. "Gần
nhất" đo bằng tổng bình phương khoảng cách dọc từ mỗi chấm tới đường, gọi là **phần dư** (thực tế − giá trị trên
đường). Cách này gọi là **bình phương tối thiểu**, viết tắt OLS (tên tiếng Anh *ordinary least squares*).

**Ví dụ số nhỏ — tự tính tay.** Dùng lại năm ngày ở mục 9 (tổng tích độ lệch 18, tổng bình phương độ lệch $x$ là 40).

- Độ dốc $b = 18 / 40 = 0{,}45$ kWh cho mỗi °C.
- Hệ số chặn $a = \bar y - b\,\bar x = 8 - 0{,}45 \times 29 = −5{,}05$ kWh.
- Đường: lượng điện ≈ −5,05 + 0,45 × nhiệt độ. Ngày 25 °C: −5,05 + 11,25 = 6,2 kWh (thực tế 6).

**R²** đo đường thẳng giải thích được bao nhiêu phần dao động của $y$. Tổng bình phương độ lệch của $y$ quanh trung
bình là 10 (mục 9). Tổng bình phương phần dư quanh đường là 1,9. R² = 1 − 1,9/10 = **0,81**. Với một biến giải thích,
R² đúng bằng $r^2 = 0{,}9^2$.

**Công thức.**

$$
b = \frac{\sum_i (x_i - \bar x)(y_i - \bar y)}{\sum_i (x_i - \bar x)^2}, \quad a = \bar y - b\,\bar x, \quad R^2 = 1 - \frac{\sum_i (y_i - \hat y_i)^2}{\sum_i (y_i - \bar y)^2}
$$

- $b$: độ dốc (tăng 1 đơn vị $x$ thì $y$ tăng $b$); $a$: giá trị của đường khi $x = 0$.
- $\hat y_i = a + b\,x_i$: giá trị trên đường tại ngày $i$; $y_i - \hat y_i$ là phần dư.

**Nói bằng lời.** R² = 1 − (phần dao động còn lại sau khi dùng đường thẳng) / (dao động ban đầu) = 1 − 1,9/10 = 0,81:
đường thẳng giải thích được 81% dao động của lượng điện trong 5 ngày này.

**Code.**

```python
import numpy as np
nd = np.array([25, 27, 29, 31, 33])       # °C, 5 ngày ở mục 9
dien = np.array([6, 7, 9, 8, 10])         # kWh

np.polyfit(nd, dien, 1)                   # [ 0.45 -5.05]  — độ dốc, hệ số chặn
```

**Hai lưu ý khi dùng cho dự báo** (FPP mục 7.3).

- R² không bao giờ giảm khi thêm biến, kể cả biến vô nghĩa. R² cao trên dữ liệu đã dùng để khớp không nói gì về độ
  chính xác khi dự báo. Hãy đo sai số trên dữ liệu **mô hình chưa thấy** (buổi 15).
- R² cao kèm phần dư tự tương quan mạnh là dấu hiệu **hồi quy giả**: hai chuỗi cùng xu hướng, như ví dụ tương quan giả
  ở mục 9 (buổi 8, 18).

**Tóm lại.** **Hồi quy tìm đường thẳng làm nhỏ nhất tổng bình phương phần dư. R² là phần dao động đường đó giải thích
được, đo trên dữ liệu đã khớp. R² cao không có nghĩa là dự báo tốt.**

**Tự kiểm tra.** Dùng đường lượng điện ≈ −5,05 + 0,45 × nhiệt độ, dự báo ngày 35 °C. Có nên tin con số này bằng các ngày
25–33 °C không?

<details>
<summary>Đáp án</summary>

−5,05 + 0,45 × 35 = −5,05 + 15,75 = 10,70 kWh. Nên tin **ít hơn**: 35 °C nằm ngoài khoảng 25–33 °C đã dùng để khớp
đường, và không có gì bảo đảm quan hệ vẫn thẳng ở nhiệt độ cao hơn (ví dụ điều hoà đã chạy hết công suất). Nhầm hay gặp
là tin R² = 0,81 bảo đảm cho cả những nhiệt độ chưa từng thấy.

</details>

---

## 17. Bẫy thường gặp

| Bẫy | Vì sao sai | Thay bằng |
|---|---|---|
| Dùng `np.quantile` mặc định rồi so với số đếm tay | NumPy nội suy giữa hai số kề nhau | `method="inverted_cdf"` khi cần khớp cách đếm (mục 4) |
| So độ lệch chuẩn từ NumPy với pandas | NumPy chia $n$, pandas chia $n - 1$ | ghi rõ `ddof` (mục 5) |
| Dự báo trung bình khi thiếu và thừa đắt khác nhau | trung bình chỉ tốt nhất với sai số bình phương | quantile mức theo tỷ lệ chi phí (mục 8, buổi 1) |
| Khoảng $\bar y \pm 1{,}96\,s$ cho dữ liệu lệch | cận dưới âm vô nghĩa, cận trên bị vượt nhiều hơn cam kết | quantile thực nghiệm, biến đổi log, phân phối lệch (mục 12) |
| Coi tương quan cao là nhân quả | hai biến có thể cùng do một nguyên nhân thứ ba, hoặc cùng có xu hướng | sai phân rồi tính lại, suy nghĩ cơ chế (mục 9) |
| "Không bác bỏ $H_0$" → "đã chứng minh $H_0$" | có thể chỉ do ít dữ liệu | "chưa đủ bằng chứng" (mục 10) |
| p = 0,01 → "$H_0$ đúng với xác suất 1%" | p-value tính giả sử $H_0$ đúng | đọc p-value là mức hiếm của dữ liệu nếu $H_0$ đúng (mục 10) |
| Giả định Poisson cho dữ liệu đếm mà không kiểm | phương sai lớn hơn trung bình thì khoảng quá hẹp | kiểm tỷ lệ phương sai / trung bình; âm nhị thức (mục 14) |
| Tin CLT với $n$ lớn trên dữ liệu đuôi quá dày | không có phương sai hữu hạn thì CLT không áp dụng | trung vị, quantile, mô hình đuôi (mục 11, buổi 25) |
| Coi $n$ giờ liên tiếp như $n$ lần đo độc lập | tự tương quan dương làm số lần đo "đáng giá" nhỏ hơn nhiều | cỡ mẫu hiệu dụng, block bootstrap (mục 11, 13) |
| Bootstrap từng số trên chuỗi thời gian | khoảng quá hẹp (56,5% thay vì 95% trong mô phỏng) | block bootstrap (mục 13) |
| Nhầm khoảng tin cậy với khoảng dự báo | khoảng tin cậy cho trung bình hẹp hơn nhiều | khoảng dự báo cho giá trị tương lai (mục 12) |
| R² cao → mô hình dự báo tốt | R² đo trên dữ liệu đã khớp, không giảm khi thêm biến | sai số trên dữ liệu chưa thấy, backtest (chấm mô hình trên quá khứ như đang dự báo thật; mục 16, buổi 15) |

---

## Nguồn

Các con số trong phụ lục chạy ngày 2026-09-18. Nguồn tài liệu tra cứu ngày 2026-09-17; nhật ký research của khoá ghi
trong thư mục công cụ.

- Hyndman, R.J. & Fan, Y. (1996). Sample quantiles in statistical packages. *The American Statistician* 50(4), 361–365.
- NumPy `quantile`, `var`, `std`: <https://numpy.org/doc/stable/reference/generated/numpy.quantile.html>,
  <https://numpy.org/doc/stable/reference/generated/numpy.var.html>
- pandas `Series.var`, `Series.skew`: <https://pandas.pydata.org/docs/reference/api/pandas.Series.var.html>
- SciPy `stats` (`norm`, `skew`, `binomtest`, `poisson`, `nbinom`, `t`, `bootstrap`):
  <https://docs.scipy.org/doc/scipy/reference/stats.html>
- Gneiting, T. (2011). Making and evaluating point forecasts. *JASA* 106(494), 746–762. <https://arxiv.org/abs/0912.0902>
- Wasserstein, R.L. & Lazar, N.A. (2016). The ASA statement on p-values: context, process, and purpose. *The American
  Statistician* 70(2), 129–133.
- NIST/SEMATECH e-Handbook of Statistical Methods — Poisson, t, Cauchy:
  <https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm>,
  <https://www.itl.nist.gov/div898/handbook/eda/section3/eda3664.htm>,
  <https://www.itl.nist.gov/div898/handbook/eda/section3/eda3663.htm>
- MIT OCW 6.436J, Lecture 17 (định lý giới hạn trung tâm):
  <https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/>
- MIT OCW 18.05, Class 10 (MLE): <https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/>
- Bretherton, C.S. và cộng sự (1999). The effective number of spatial degrees of freedom of a time-varying field.
  *J. Climate* 12(7), 1990–2009.
- Hyndman, R.J. — The difference between prediction intervals and confidence intervals:
  <https://robjhyndman.com/hyndsight/intervals/>
- Hyndman, R.J., Athanasopoulos, G. và cộng sự. *Forecasting: Principles and Practice, the Pythonic Way* (FPP) — mục
  5.5, 7.3, 9.8, chương 10: <https://otexts.com/fpppy/>
- Efron, B. (1979). Bootstrap methods: another look at the jackknife. *Annals of Statistics* 7(1), 1–26.
- Künsch, H.R. (1989). The jackknife and the bootstrap for general stationary observations. *Annals of Statistics*
  17(3), 1217–1241.
- Politis, D.N. & Romano, J.P. (1994). The stationary bootstrap. *JASA* 89(428), 1303–1313.
- Politis, D.N. (2003). The impact of bootstrap methods on time series analysis:
  <https://mathweb.ucsd.edu/~politis/impactBOOT.pdf>
