# Buổi 6 — Phân rã chuỗi thời gian

## 1. Mục tiêu

Sau buổi này bạn:

- Tự **phân rã** một chuỗi 12 điểm bằng tay thành xu hướng + mùa vụ + phần dư, rồi làm lại bằng NumPy và `statsmodels`.
- Chỉ ra bằng hình và số **mùa vụ chưa tách hết trốn ở đâu**: trong xu hướng, trong phần dư, hay bị ép giống nhau cả năm.
- Phân rã một chuỗi có **hai mùa vụ** (ngày và tuần) bằng MSTL, và kiểm bằng số rằng phần dư không còn mẫu hình lịch.
- Tính và nói bằng lời **độ mạnh xu hướng $F_T$** và **độ mạnh mùa vụ $F_S$**.
- Biết khi nào bật **robust**: vì sao nó cứu được một giờ số liệu hỏng nhưng không tách được một đợt nắng nóng.

## 2. Nhắc lại buổi trước

Từ buổi 4–5:

- **Xu hướng** là mức chung đổi lâu dài; **mùa vụ** lặp sau số bước cố định theo lịch, **chu kỳ mùa vụ** $m$ là số bước đó; một
  chuỗi có thể có nhiều mùa vụ (**mùa vụ kép**: ngày lồng trong tuần).
- **Trung bình trượt có tâm**: thay mỗi điểm bằng trung bình của nó và các điểm hai bên. Ví dụ 3 điểm: 48, 2, 51 → 33,7.
- **Heatmap giờ × thứ** và **ACF** (hệ số tự tương quan $r_k$ theo độ trễ $k$) là hai cách thấy mùa vụ kép; ACF có đỉnh ở bội số của
  chu kỳ mùa vụ.
- **Log** biến "nhân" thành "cộng": $\log(a \times b) = \log a + \log b$.

Từ buổi 2–3:

- **Phương sai** $\operatorname{Var}(x)$: trung bình bình phương khoảng cách tới trung bình (chia $n - 1$). Ví dụ 2, 4, 6 → 4.
- Giờ thiếu là **NaN**, không phải 0; làm việc trên giờ **UTC**, vì giờ địa phương có lỗ và giờ lặp vào hai ngày đổi giờ.

## 3. Trạng thái đầu buổi

Sau `python lab.py up` (trong thư mục `lab/`):

| Hạng mục | Trạng thái |
|---|---|
| Dữ liệu | `du-lieu/raw/eia930-balance-2024-h1/EIA930_BALANCE_2024_Jan_Jun.csv` (sha256 `26768c495c3b`) và `…-h2/EIA930_BALANCE_2024_Jul_Dec.csv` (`a602a8e577cf`): nhu cầu điện theo giờ của mọi vùng điều độ ở Mỹ |
| Chuỗi của buổi | PJM (vùng điện miền Đông nước Mỹ), cột `Demand (MW)`: 8.784 giờ UTC, 01/01/2024 06:00 → 01/01/2025 05:00 (mốc là **cuối** giờ), 47 giờ NaN |
| Nguồn | U.S. Energy Information Administration, Form EIA-930, public domain |
| Môi trường | Python 3.12; numpy 2.5.3, pandas 3.0.5, matplotlib 3.11.2, statsmodels 0.15.0 |
| `code/phan_ra.py` | `doc_nhu_cau`, `lap_cho_trong`, `phan_ra`, `do_manh`, `ho_so_phan_du`, `ty_le_mau_hinh_con_lai` |
| `code/lab.ipynb` | notebook của Lab, bước 1–5 |
| **Đang cố tình sai** | `phan_ra` dùng phân rã **cổ điển chu kỳ 24** cho chuỗi có cả mùa vụ tuần; tham số `robust` bị bỏ qua |
| **Triệu chứng** | $F_S$ = 0,618 cho một chuỗi điện rõ ràng rất mùa vụ; không có thành phần tuần; 12 giờ đầu và 12 giờ cuối không có xu hướng |
| `python lab.py check` lúc này | ĐỎ: 5/7 test hỏng |

## 4. Lý thuyết

Đơn vị điện: **MW** (megawatt) là công suất dùng trong một giờ; **GW** (gigawatt) = 1.000 MW.

### Từ mới trong buổi

| Thuật ngữ | Nghĩa một câu | Ví dụ |
|---|---|---|
| PJM, ERCO, ISNE | Mã vùng điều độ điện trong dữ liệu EIA-930: PJM (miền Đông nước Mỹ), ERCO (Texas), ISNE (New England). | Chuỗi của buổi là PJM. |
| T2 … T7, CN | Thứ Hai … thứ Bảy, Chủ nhật. | T7 8h = 8 giờ sáng thứ Bảy. |
| phân rã (decomposition) | Tách chuỗi thành các phần cộng lại ra chuỗi: xu hướng + mùa vụ + phần dư. | 30 = 24,5 (xu hướng) + 4 (mùa vụ) + 1,5 (phần dư). |
| phần dư (remainder) | Phần còn lại sau khi trừ xu hướng và mùa vụ; lý tưởng là không còn mẫu hình. | Ngày mưa bão, giờ số liệu hỏng. |
| phân rã cộng / nhân | Cộng: mùa vụ là số MW cố định cộng thêm. Nhân: mùa vụ là tỷ lệ nhân thêm. | Cộng: +10 ở mọi mức. Nhân: ×1,1, tức +10 ở mức 100, +20 ở mức 200. |
| 2×m-MA | Trung bình trượt $m$ điểm rồi trung bình trượt 2 điểm, để có tâm khi $m$ chẵn. | $m$ = 4: trọng số 1/8, 1/4, 1/4, 1/4, 1/8. |
| phân rã cổ điển (classical decomposition) | Xu hướng bằng 2×m-MA, mùa vụ bằng trung bình theo vị trí trong chu kỳ, giống nhau mọi chu kỳ. | Mục 4.1. |
| khử xu hướng (detrend) | Lấy chuỗi trừ xu hướng: $y - T$. | 30 − 24,5 = 5,5. |
| STL, LOESS | STL là phân rã dùng LOESS: làm trơn cục bộ, mỗi điểm chỉ nhìn các điểm lân cận, điểm gần nặng hơn. Mùa vụ được đổi dần. | Mục 4.4. |
| MSTL | STL cho nhiều mùa vụ: tách lần lượt từng chu kỳ, ngắn trước dài sau. | Chu kỳ 24 giờ rồi 168 giờ. |
| độ mạnh xu hướng / mùa vụ ($F_T$, $F_S$) | Số từ 0 tới 1: phần dư nhỏ tới đâu so với xu hướng (hay mùa vụ) cộng phần dư. | $F_S$ = 0,98: mùa vụ lấn át phần dư. |
| robust | Cách ước lượng ít bị vài điểm bất thường kéo lệch. | Một giờ hỏng không làm méo mùa vụ cả tuần. |
| X-13ARIMA-SEATS | Chương trình khử mùa vụ của cơ quan thống kê Mỹ, cho dữ liệu tháng và quý. | Chỉ ở hộp Nâng cao. |
| tỷ lệ mẫu hình | Phương sai của trung bình phần dư theo nhóm lịch, chia phương sai chuỗi; gần 0 là phần dư sạch. | Mục 4.3. |

### 4.1 Ba thành phần và phân rã cổ điển bằng tay

**Vấn đề.** Nhu cầu điện lên xuống vì nhiều lý do chồng lên nhau: mức chung đổi theo mùa (xu hướng), nhịp trong ngày và trong tuần
(mùa vụ), và những thứ không đoán trước (phần dư). Muốn hiểu từng thứ, phải **tách** chúng ra.

**Trực giác.** Muốn thấy xu hướng, lấy trung bình đúng **một vòng mùa vụ**: phần mùa vụ lên rồi xuống, cộng lại thành 0, tự triệt
tiêu. Trừ xu hướng khỏi dữ liệu, cái còn lại là mùa vụ + phần dư. Lấy trung bình theo từng vị trí trong vòng (mọi quý 1, mọi quý
2…) thì phần dư lúc dương lúc âm triệt tiêu, còn lại mùa vụ.

**Ví dụ số nhỏ — tự tính tay.** Doanh số 12 quý (3 năm), chu kỳ $m$ = 4:

y = 22, 18, 15, 29 | 30, 22, 19, 33 | 30, 26, 23, 37

*Bước 1 — xu hướng.* Trung bình 4 quý liền nhau rơi vào **giữa** hai quý (không có tâm). Nên lấy trung bình của hai cửa sổ 4 quý kề
nhau; tính ra là 5 quý với trọng số 1/8, 1/4, 1/4, 1/4, 1/8. Tại quý 3 (dùng quý 1 → 5):

$\hat T_3$ = 22/8 + (18 + 15 + 29)/4 + 30/8 = 2,75 + 15,5 + 3,75 = **22**

Hai quý đầu và hai quý cuối không có đủ hàng xóm, nên không có xu hướng.

*Bước 2 — khử xu hướng, rồi lấy trung bình theo quý.* Làm như vậy cho mọi quý:

| Quý | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| $y$ | 15 | 29 | 30 | 22 | 19 | 33 | 30 | 26 |
| Xu hướng $\hat T$ | 22 | 23,5 | 24,5 | 25,5 | 26 | 26,5 | 27,5 | 28,5 |
| $y - \hat T$ | −7 | 5,5 | 5,5 | −3,5 | −7 | 6,5 | 2,5 | −2,5 |
| Mùa vụ $\hat S$ | −7 | 6 | 4 | −3 | −7 | 6 | 4 | −3 |
| Phần dư $\hat R = y - \hat T - \hat S$ | 0 | −0,5 | 1,5 | −0,5 | 0 | 0,5 | −1,5 | 0,5 |

**Đọc bảng.** Dòng mùa vụ là trung bình dòng $y - \hat T$ theo vị trí trong năm. Quý thứ nhất của năm: (5,5 + 2,5)/2 = 4. Quý thứ
hai: (−3,5 − 2,5)/2 = −3. Quý thứ ba: (−7 − 7)/2 = −7. Quý thứ tư: (5,5 + 6,5)/2 = 6. Bốn số cộng lại 4 − 3 − 7 + 6 = 0, nên
không phải chỉnh (nếu khác 0 thì trừ đều để tổng bằng 0). Phần dư chỉ còn ±0,5 và ±1,5: phân rã đã giải thích gần hết dữ liệu.

**Công thức.** Với $m$ chẵn (ví dụ trên $m$ = 4; điện theo giờ $m$ = 24):

$$
\hat T_t = \frac{1}{2m}\, y_{t-m/2} + \frac{1}{m} \sum_{j=-(m/2-1)}^{m/2-1} y_{t+j} + \frac{1}{2m}\, y_{t+m/2}
$$

- $\hat T_t$: xu hướng ước lượng tại $t$. $y_{t+j}$: giá trị cách $t$ đúng $j$ bước.
- Hai đầu nhận nửa trọng số, $\frac{1}{2m}$, vì $t - m/2$ và $t + m/2$ cách nhau đúng một vòng: chúng là **cùng một vị trí** trong vòng
  (cùng một quý, cùng một giờ trong ngày). Cộng lại, mỗi vị trí trong vòng có đúng trọng số $\frac{1}{m}$.

**Nói bằng lời.** Xu hướng tại $t$ là trung bình của $m + 1$ điểm quanh $t$, hai điểm ngoài cùng tính một nửa. Với $m$ = 4: 22/8 +
(18 + 15 + 29)/4 + 30/8 = 22. Với $m$ = 24: 25 giờ, hai đầu mỗi bên 1/48, giữa mỗi giờ 1/24; 12 giờ đầu và 12 giờ cuối chuỗi mất xu hướng.

**NumPy và thư viện.** Cả phân rã cổ điển trong vài dòng (chính ví dụ trên khi `x` là 12 quý và `m = 4`):

```python
w = np.r_[0.5, np.ones(m - 1), 0.5] / m               # m + 1 trọng số, tổng = 1
T = np.full(x.size, np.nan)
T[m // 2 : -m // 2] = np.convolve(x, w, mode="valid")  # mất m/2 điểm mỗi đầu
pha = np.arange(x.size) % m                            # vị trí trong vòng
S_mua = np.array([np.nanmean((x - T)[pha == k]) for k in range(m)])
S = (S_mua - S_mua.mean())[pha]                        # tổng mùa vụ một vòng = 0
R = x - T - S
```

`statsmodels.tsa.seasonal.seasonal_decompose(y, period=m)` cho đúng từng số (kiểm bằng `dap-an/vi_du_nho.py` và trên PJM: lệch lớn
nhất 0,0).

**Tóm lại.** **Phân rã cổ điển: xu hướng là trung bình trượt đúng một vòng mùa vụ (2×m-MA khi $m$ chẵn). Mùa vụ là trung bình của
"dữ liệu trừ xu hướng" theo vị trí trong vòng. Phần dư là cái còn lại.**

**Tự kiểm tra.** Chuỗi 10, 20, 30, 20, 10, 20, 30, 20, 10 có $m$ = 4. Tính $\hat T_3$ (điểm thứ 3, đếm từ 1).

<details>
<summary>Đáp án</summary>

10/8 + (20 + 30 + 20)/4 + 10/8 = 1,25 + 17,5 + 1,25 = **20**. Chuỗi lặp đúng mỗi 4 điểm nên mùa vụ triệt tiêu hoàn toàn, xu hướng
phẳng ở 20. Nhầm hay gặp: quên nửa trọng số ở hai đầu, cộng 5 điểm rồi chia 5: (10 + 20 + 30 + 20 + 10)/5 = 18, tính hai lần
cùng một vị trí trong vòng (điểm 1 và điểm 5).

</details>

### 4.2 Cộng hay nhân, và mùa vụ đổi theo thời gian

**Vấn đề.** Phân rã cổ điển giả định hai điều: mùa vụ **cộng** thêm một số cố định, và vòng nào cũng **giống hệt** nhau. Với điện, điều
thứ hai sai.

**Ví dụ số nhỏ — tự tính tay.** Mức 100 và mức 200, mùa vụ "giờ cao điểm":

- **Cộng**: cao điểm luôn cao hơn mức 10 đơn vị: 100 + 10 = 110 và 200 + 10 = 210.
- **Nhân**: cao điểm luôn gấp 1,1 lần mức: 100 × 1,1 = 110 và 200 × 1,1 = 220. Dao động lớn gấp đôi khi mức gấp đôi.

Nếu dao động tỷ lệ với mức thì dùng phân rã nhân, hoặc lấy log rồi phân rã cộng, vì $\log(T \times S \times R) = \log T + \log S + \log R$
(FPP §3.2; buổi 5).

![PJM 2024: đỉnh hè, đỉnh đông, và biên độ trong ngày lớn hẳn vào mùa hè](hinh/du-lieu-pjm.png)

**Cách đọc hình.**

1. **Trục ngang**: ô trên là cả năm 2024; ô dưới là hai tuần tháng 7 theo giờ New York.
2. **Trục dọc**: nhu cầu điện (GW).
3. **Ký hiệu**: ô trên, dải xám là từng giờ, đường xanh là trung bình ngày, hai vạch cam là hai ngày đổi giờ, quanh mỗi ngày đó dữ liệu
   trống liền một khối (22 và 25 giờ); ô dưới, đường xanh là từng giờ.
4. **Nhìn vào đâu**: ô trên, độ dày dải xám tháng 7 so với tháng 4; ô dưới, hai ngày 13–14/7 (thứ Bảy, Chủ nhật).
5. **Kết luận**: có đỉnh hè và đỉnh đông; dao động trong ngày dày hẳn vào mùa hè; ngày nào cũng một đỉnh chiều, cuối tuần thấp hơn.

Biên độ trong ngày lớn vào mùa hè vì **điều hoà nhiệt độ** chạy buổi chiều, không phải vì mức cao: mùa đông mức cũng cao mà dao động
không lớn. Đó là mùa vụ **đổi theo thời gian**, không phải lý do dùng phân rã nhân. Buổi này dùng phân rã cộng và cho mùa vụ đổi dần
(mục 4.4).

Gai cắm xuống cuối tháng 11 (ô trên) là 17:00 UTC ngày 21/11/2024: 56.260 MW, trong khi giờ trước và giờ sau đều khoảng 95.000 MW. Một
giờ số liệu hỏng; mục 4.6 dùng nó.

**Tóm lại.** **Cộng hay nhân tuỳ dao động có tỷ lệ với mức không. Điện PJM có biên độ ngày đổi theo mùa vì điều hoà nhiệt độ: cần
mùa vụ đổi theo thời gian, không phải phân rã nhân.**

**Tự kiểm tra.** Doanh số một cửa hàng: năm đầu mức 50, tháng Tết bán 60; năm sau mức 100, tháng Tết bán 120. Cộng hay nhân?

<details>
<summary>Đáp án</summary>

**Nhân**: tháng Tết đều gấp 1,2 lần mức (60 / 50 = 120 / 100 = 1,2), còn chênh tuyệt đối đổi từ 10 lên 20. Phân rã cộng sẽ thấy mùa vụ
"lớn dần". Nhầm hay gặp: nhìn mức tăng gấp đôi rồi kết luận có xu hướng nên "phải nhân"; xu hướng không quyết định cộng hay nhân, chỉ
biên độ mùa vụ so với mức mới quyết định.

</details>

### 4.3 Cổ điển chu kỳ 24 trên PJM: mùa vụ trốn ở đâu

**Vấn đề.** Code đầu buổi phân rã PJM với chu kỳ 24 giờ. Chuỗi còn mùa vụ tuần (168 giờ), và mùa vụ ngày đổi theo mùa. Hai thứ đó đi
đâu?

![Phân rã cổ điển chu kỳ 24, tháng 7/2024: xu hướng lõm mỗi cuối tuần, phần dư dao động đều theo ngày](hinh/co-dien-24.png)

**Cách đọc hình.**

1. **Trục ngang**: 1/7 → 29/7/2024, theo giờ.
2. **Trục dọc**: GW; mỗi hàng một thang riêng: dữ liệu, xu hướng (2×24-MA), mùa vụ 24 giờ, phần dư.
3. **Ký hiệu**: dải xám là thứ Bảy – Chủ nhật.
4. **Nhìn vào đâu**: hàng xu hướng ở các dải xám; hàng phần dư.
5. **Kết luận**: xu hướng lõm xuống mỗi cuối tuần, tức nhịp tuần chạy vào xu hướng. Mùa vụ là một khuôn 24 giờ lặp y hệt. Phần dư dao
   động đều mỗi ngày (khoảng ±15 GW): phần mùa vụ ngày của tháng 7 mà khuôn chung cả năm không chứa được.

Xu hướng lõm cuối tuần vì 2×24-MA là trung bình **một ngày**: ngày Chủ nhật thấp thì trung bình quanh Chủ nhật thấp.

| Thứ (giờ New York) | T2 | T3 | T4 | T5 | T6 | T7 | CN |
|---|---|---|---|---|---|---|---|
| Xu hướng trung bình (MW) | 93.327 | 94.611 | 95.036 | 94.917 | 93.654 | 89.523 | 88.459 |

**Đọc bảng.** Thứ Bảy và Chủ nhật thấp hơn giữa tuần khoảng 5.500–6.600 MW. Kiểm phần dư mà không kiểm xu hướng sẽ kết luận sai
"không có mùa vụ tuần".

**Đo "phần dư còn mẫu hình" bằng một con số.** Nhóm phần dư theo lịch (ví dụ theo tháng và giờ), lấy trung bình mỗi nhóm. Phần dư sạch
thì mọi trung bình nhóm gần 0; còn mẫu hình thì chúng lệch nhau.

**Ví dụ số nhỏ — tự tính tay.** Phần dư của 4 giờ, hai nhóm "sáng" và "chiều":

- Phân rã A: sáng +2, −2; chiều +1, −1. Trung bình nhóm: 0 và 0. Không còn mẫu hình.
- Phân rã B: sáng −3, −5; chiều +3, +5. Trung bình nhóm: −4 và +4. Phương sai của hai số −4, +4 là ((−4)² + 4²) / (2 − 1) = 32: phần dư
  còn nhịp sáng–chiều.

$$
\text{tỷ lệ mẫu hình} = \frac{\operatorname{Var}_g\big(\bar R_g\big)}{\operatorname{Var}(y)}
$$

- $g$: một nhóm lịch, ví dụ (tháng 7, 17 giờ). $\bar R_g$: trung bình phần dư trong nhóm $g$.
- $\operatorname{Var}_g(\bar R_g)$: phương sai của các trung bình nhóm. $\operatorname{Var}(y)$: phương sai của cả chuỗi, để so tương đối.

**Nói bằng lời.** Trung bình phần dư theo từng nhóm lịch, đo các trung bình đó lệch nhau cỡ nào, rồi chia cho độ dao động của cả chuỗi.
Ở phân rã B, nếu phương sai chuỗi là 320 thì tỷ lệ là 32 / 320 = 0,1; gần 0 nghĩa là phần dư không còn mẫu hình theo nhóm đó.

![Trung bình phần dư theo tháng × giờ và theo giờ trong tuần: cổ điển còn mẫu hình, MSTL sạch](hinh/phan-du-so-sanh.png)

**Cách đọc hình.**

1. **Trục ngang**: hàng trên là giờ New York 0 → 23; hàng dưới là giờ trong tuần (T2 → CN).
2. **Trục dọc**: hàng trên là tháng 1 → 12; hàng dưới là trung bình phần dư (GW).
3. **Ký hiệu**: cột trái là phân rã cổ điển chu kỳ 24, cột phải là MSTL (mục 4.4); màu đỏ là phần dư dương (dữ liệu cao hơn phân rã),
   xanh là âm, trắng là 0.
4. **Nhìn vào đâu**: ô trên trái, các tháng hè vào buổi chiều; ô dưới trái, thứ Bảy và Chủ nhật.
5. **Kết luận**: cổ điển còn cả mùa vụ ngày đổi theo mùa (hè đỏ buổi chiều, đông đỏ buổi sáng) lẫn nhịp cuối tuần; MSTL gần như trắng
   ở cả hai.

| Phân rã | Tỷ lệ mẫu hình tháng × giờ | Tỷ lệ mẫu hình thứ × giờ | Phần dư tháng 7 lúc 17h (MW) |
|---|---|---|---|
| Cổ điển chu kỳ 24 | 0,102 | 0,0067 | +13.037 |
| MSTL (24, 168) | 0,0006 | 0,00001 | −668 |

**Đọc bảng.** So hai dòng: cổ điển để lại khoảng một phần mười phương sai chuỗi thành mẫu hình tháng × giờ, MSTL gần như không còn.
Cột cuối: chiều hè, khuôn mùa vụ chung cả năm của cổ điển thấp hơn dữ liệu khoảng 13 GW.

**Tóm lại.** **Cổ điển chu kỳ 24 đẩy nhịp tuần vào xu hướng và để mùa vụ ngày đổi theo mùa lại trong phần dư. Kiểm cả hai chỗ: trung
bình xu hướng theo thứ, và tỷ lệ mẫu hình của phần dư theo tháng × giờ, thứ × giờ.**

**Tự kiểm tra.** Một báo cáo viết: "Trung bình phần dư theo thứ chỉ vài trăm MW, vậy chuỗi không có mùa vụ tuần." Còn thiếu kiểm gì?

<details>
<summary>Đáp án</summary>

Thiếu kiểm **xu hướng** theo thứ. Với chu kỳ 24, nhịp tuần trốn vào xu hướng (bảng trên: T7, CN thấp hơn T4 khoảng 5.500–6.600 MW), nên
phần dư theo thứ nhỏ mà mùa vụ tuần vẫn có. Nhầm hay gặp: chỉ nhìn phần dư, tưởng "phần dư sạch" là "phân rã đúng".

</details>

### 4.4 STL và MSTL: mùa vụ được đổi dần, nhiều chu kỳ

**Vấn đề.** Cần phân rã mà (1) mùa vụ ngày tháng 7 được khác tháng 1, và (2) tách riêng mùa vụ tuần.

**Trực giác.** Cổ điển lấy **một** trung bình cho mọi quý 1 của mọi năm. STL thay bằng trung bình **cục bộ**: mùa vụ quý 1 năm nay chỉ
nhìn quý 1 của vài năm gần nó, nên được đổi dần qua các năm.

**Ví dụ số nhỏ — tự tính tay.** "Dữ liệu trừ xu hướng" của quý đầu năm qua năm năm lớn dần: 2, 4, 6, 8, 10.

- **Cổ điển**: mùa vụ quý 1 = trung bình = 6 cho cả 5 năm. Phần dư: 2 − 6 = −4, rồi −2, 0, 2, 4. Phần dư còn một đường đi lên: mẫu hình
  bị bỏ sót.
- **Cục bộ** (trung bình 3 năm quanh mỗi năm; hai năm đầu cuối chỉ có 2 năm): (2 + 4)/2 = 3, (2 + 4 + 6)/3 = 4, 6, 8, (8 + 10)/2 = 9. Phần
  dư: −1, 0, 0, 0, 1. Gần như sạch.

STL làm đúng ý đó, nhưng dùng **LOESS** thay cho trung bình 3 điểm: ở mỗi điểm, vẽ một đường khớp nhất qua các điểm lân cận, điểm gần
nặng hơn, lấy giá trị của đường tại điểm đó (Cleveland và cộng sự, 1990). STL lặp: ước lượng mùa vụ, trừ đi, ước lượng xu hướng, trừ đi,
làm lại.

**Hai tham số chính** (đều là số lẻ):

- `seasonal`: số vòng lân cận dùng để làm trơn mùa vụ. Nhỏ thì mùa vụ đổi nhanh; tối thiểu 7.
- `trend`: số điểm lân cận dùng cho xu hướng. Mặc định của statsmodels với $m$ = 24 là **47 giờ**.

Cửa sổ xu hướng quá ngắn thì xu hướng "tranh" dao động với mùa vụ. `STL(period=24)` mặc định trên PJM cho phương sai phần dư chỉ
2,8 GW², nhỏ hơn MSTL (16,5 GW²). Nhỏ không phải vì tốt: xu hướng 47 giờ đủ mềm để nuốt cả nhịp tuần lẫn thời tiết.

**MSTL** (Bandara, Hyndman & Bergmeir) cho nhiều chu kỳ. Nó xếp chu kỳ từ ngắn tới dài, tách mùa vụ ngày bằng STL, rồi tách mùa vụ
tuần khỏi phần còn lại, và lặp lại vòng đó hai lần. Cửa sổ mùa vụ mặc định của statsmodels cho hai chu kỳ này là 11 và 15. Chu kỳ
dài hơn nửa chuỗi bị bỏ, chỉ kèm một cảnh báo.

```python
from statsmodels.tsa.seasonal import MSTL
kq = MSTL(y, periods=(24, 168)).fit()   # kq.trend, kq.seasonal["seasonal_24"], kq.seasonal["seasonal_168"], kq.resid
```

STL và MSTL của statsmodels trả **toàn NaN, không lỗi, không cảnh báo** nếu đầu vào còn một NaN. Vì vậy `lap_cho_trong` nội suy 47 giờ
trống trước khi phân rã.

![MSTL (24, 168), tháng 7/2024: xu hướng trơn, nhịp cuối tuần nằm trong mùa vụ tuần](hinh/mstl.png)

**Cách đọc hình.**

1. **Trục ngang**: 1/7 → 29/7/2024, theo giờ.
2. **Trục dọc**: GW, mỗi hàng một thang: dữ liệu, xu hướng, mùa vụ ngày, mùa vụ tuần, phần dư.
3. **Ký hiệu**: một đường mỗi hàng.
4. **Nhìn vào đâu**: hàng xu hướng (còn lõm cuối tuần không); hàng mùa vụ tuần; hàng phần dư.
5. **Kết luận**: xu hướng trơn, không lõm theo thứ Bảy; nhịp cuối tuần nằm ở hàng mùa vụ tuần; phần dư là những đợt kéo dài vài ngày,
   tức thời tiết, thứ phân rã không thể biết trước.

![Mùa vụ ngày của MSTL theo tháng: tháng 1 hai đỉnh sáng – tối, tháng 7 một đỉnh chiều](hinh/bien-do-ngay.png)

**Cách đọc hình.**

1. **Trục ngang**: giờ New York, 0 → 23.
2. **Trục dọc**: mùa vụ ngày của MSTL (GW), trung bình theo tháng.
3. **Ký hiệu**: mỗi đường một tháng (7 tháng tiêu biểu); xanh đậm là tháng 1, đỏ đậm là tháng 7.
4. **Nhìn vào đâu**: hình dạng và độ cao đường tháng 1 so với tháng 7.
5. **Kết luận**: mùa đông có hai bướu sáng và tối, mùa hè một đỉnh chiều cao gấp ba (biên độ tháng 7 chia tháng 1: 43,3 / 14,4 = 3,0).
   Phân rã cổ điển ép các đường này thành một.

**Tóm lại.** **STL làm trơn mùa vụ cục bộ nên mùa vụ được đổi dần; MSTL tách lần lượt nhiều chu kỳ. Cửa sổ xu hướng quá ngắn làm phần
dư nhỏ giả tạo; đầu vào còn NaN thì mọi thứ ra NaN.**

**Tự kiểm tra.** Dữ liệu trừ xu hướng của quý đầu năm, qua bốn năm, lần nào cũng là 10. Mùa vụ cổ điển và mùa vụ cục bộ (trung bình
ba năm) khác nhau không?

<details>
<summary>Đáp án</summary>

Không: cả hai đều ra 10 ở mọi năm, phần dư 0. STL chỉ khác cổ điển khi mùa vụ **thật sự đổi** qua các năm. Nhầm hay gặp: nghĩ STL luôn
cho kết quả khác (hay tốt hơn) cổ điển.

</details>

### 4.5 Độ mạnh xu hướng và mùa vụ

**Vấn đề.** "Chuỗi này mùa vụ mạnh không?" cần một con số để so giữa các chuỗi và các phân rã.

**Trực giác.** Nếu phần dư rất nhỏ so với mùa vụ, thì mùa vụ "mạnh": gần hết dao động quanh xu hướng là mùa vụ. Nếu phần dư to ngang
mùa vụ thì mùa vụ yếu.

**Ví dụ số nhỏ — tự tính tay.** Dùng 8 quý có xu hướng ở bảng mục 4.1.

- $\operatorname{Var}(\hat R)$: tám phần dư có trung bình 0; tổng bình phương 0 + 0,25 + 2,25 + 0,25 + 0 + 0,25 + 2,25 + 0,25 = 5,5; chia
  8 − 1 = 7 → **0,786**.
- $\operatorname{Var}(\hat S + \hat R)$ là phương sai của dòng $y - \hat T$: trung bình 0; tổng bình phương 49 + 30,25 + 30,25 + 12,25 + 49 +
  42,25 + 6,25 + 6,25 = 225,5; chia 7 → **32,21**.
- $F_S$ = 1 − 0,786 / 32,21 ≈ **0,976**.
- $\hat T + \hat R$ = 22; 23; 26; 25; 26; 27; 26; 29, trung bình 25,5, tổng bình phương độ lệch 34, chia 7 → 4,857. $F_T$ = 1 − 0,786 / 4,857
  ≈ **0,838**.

**Công thức** (FPP §4.3):

$$
F_T = \max\left(0,\ 1 - \frac{\operatorname{Var}(R_t)}{\operatorname{Var}(T_t + R_t)}\right), \qquad
F_S = \max\left(0,\ 1 - \frac{\operatorname{Var}(R_t)}{\operatorname{Var}(S_t + R_t)}\right)
$$

- $T_t$, $S_t$, $R_t$: xu hướng, mùa vụ, phần dư tại $t$. $\max(0, \cdot)$: kết quả âm thì ghi 0.

**Nói bằng lời.** $F_S$ là 1 trừ "phần dư chiếm bao nhiêu phần của mùa vụ cộng phần dư". Ở ví dụ: 1 − 0,786 / 32,21 = 1 − 0,024 =
0,976, tức phần dư chỉ chiếm 2,4%: mùa vụ rất mạnh. Có nhiều mùa vụ thì tính $F_S$ cho **từng** thành phần, cùng một phần dư.

`do_manh` trong `code/phan_ra.py` làm đúng công thức này.

| PJM 2024 | $F_T$ | $F_{S,24}$ | $F_{S,168}$ |
|---|---|---|---|
| Cổ điển chu kỳ 24 | 0,828 | 0,618 | — |
| MSTL (24, 168) | 0,888 | 0,829 | 0,415 |
| MSTL robust | 0,817 | 0,739 | 0,252 |

**Đọc bảng.** So dòng 1 với dòng 2: cùng một chuỗi, $F_{S,24}$ nhảy từ 0,618 lên 0,829 chỉ vì đổi cách phân rã. Cổ điển để mùa vụ đổi
theo mùa trong phần dư, phần dư to, $F_S$ thấp. Vậy $F$ là con số của **một phân rã**, không phải của riêng dữ liệu: báo $F$ phải kèm tên
phân rã. Dòng 3 thấp hơn vì phần dư robust giữ trọn các điểm bất thường (mục 4.6), không phải vì phân rã kém hơn.

**Tóm lại.** **$F_S$ = 1 − Var(phần dư) / Var(mùa vụ + phần dư); gần 1 là mùa vụ lấn át phần dư. $F$ phụ thuộc cách phân rã, nên luôn
ghi kèm tên phương pháp.**

**Tự kiểm tra.** Phần dư có phương sai 4, mùa vụ + phần dư có phương sai 5. $F_S$ bằng bao nhiêu, và mùa vụ mạnh hay yếu?

<details>
<summary>Đáp án</summary>

$F_S$ = 1 − 4/5 = **0,2**: yếu, vì phần dư chiếm 80% dao động quanh xu hướng. Nhầm hay gặp: tính 4/5 = 0,8 rồi nói "mạnh"; đó là phần
của phần dư, phải lấy 1 trừ đi.

</details>

### 4.6 Robust: một giờ hỏng và một đợt nắng nóng

**Vấn đề.** Giờ 17:00 UTC ngày 21/11/2024 báo 56.260 MW giữa hai giờ khoảng 95.000 MW: lỗi số liệu. Không robust thì STL cố "giải
thích" cú rơi đó bằng xu hướng và mùa vụ, và làm méo chúng ở những ngày không có lỗi.

**Trực giác.** Làm phân rã hai lượt. Lượt đầu tính phần dư; điểm nào phần dư quá lớn so với phần dư điển hình thì lượt sau **bớt tin**
nó (trọng số nhỏ, tới 0) khi ước lượng xu hướng và mùa vụ. Điểm đó không bị xoá: nó vẫn nằm trong phần dư.

**Ví dụ số nhỏ — tự tính tay.** Phần dư lượt đầu: 1, −2, 1, 20, −1.

- Mốc so sánh: $h$ = 6 × trung vị của |phần dư| = 6 × trung vị(1, 2, 1, 20, 1) = 6 × 1 = 6.
- Mỗi điểm: $u$ = |phần dư| / $h$. Điểm 20: $u$ = 20 / 6 ≈ 3,3 ≥ 1 → trọng số **0**. Điểm −2: $u$ = 1/3 → trọng số (1 − 1/9)² ≈ **0,79**.
  Điểm ±1: $u$ = 1/6 → (1 − 1/36)² ≈ **0,95**.

$$
\rho = \begin{cases} (1 - u^2)^2 & 0 \le u < 1 \\ 0 & u \ge 1 \end{cases}, \qquad u = \frac{\lvert R \rvert}{6 \operatorname{median}(\lvert R \rvert)}
$$

- $\rho$: trọng số của điểm ở lượt sau, từ 0 (bỏ qua) tới 1 (tin hoàn toàn). $R$: phần dư lượt trước.

**Nói bằng lời.** Chia độ lớn phần dư cho 6 lần phần dư điển hình (trung vị); lớn hơn hoặc bằng 1 thì trọng số 0, nhỏ hơn thì trọng số
$(1 - u^2)^2$. Điểm 20 lớn hơn 6 × 1 nên bị bỏ qua hoàn toàn khi ước lượng mùa vụ.

![Một giờ hỏng: không robust thì lỗi bị chia sang mùa vụ ngày của cả tuần; robust giữ lỗi trọn trong phần dư](hinh/robust.png)

**Cách đọc hình.**

1. **Trục ngang**: 18/11 → 25/11/2024, theo giờ.
2. **Trục dọc**: GW; ba hàng: dữ liệu, mùa vụ ngày, phần dư.
3. **Ký hiệu**: hàng 2 và 3, cam là MSTL không robust, xanh là robust.
4. **Nhìn vào đâu**: hàng mùa vụ ngày, các vết lõm cam lúc trưa **mỗi ngày**; hàng phần dư, gai ngày 21/11.
5. **Kết luận**: không robust thì lỗi một giờ bị chia vào mùa vụ ngày của cả tuần (vết lõm mỗi trưa); robust giữ mùa vụ sạch và để lỗi
   nằm trọn trong phần dư.

| Lúc 17:00 UTC | Không robust | Robust |
|---|---|---|
| Mùa vụ ngày, ngày 20/11 (không có lỗi) | −4.051 MW | +2.117 MW |
| Phần dư, ngày 21/11 (giờ hỏng) | −26.322 MW | −36.323 MW |

**Đọc bảng.** Dòng đầu: không robust làm mùa vụ của một ngày **không có lỗi** lệch khoảng 6.200 MW. Dòng sau: robust giữ gần trọn cú
rơi (khoảng 38.900 MW) trong phần dư, đúng chỗ để buổi 11 tìm ngoại lai.

**Phản ví dụ: đợt nắng nóng 15–17/7/2024.** Đây không phải một điểm nhọn mà một khối vài ngày. Phân rã không biết "bình thường" của những
ngày đó là bao nhiêu, nên phần lớn đợt nóng chạy vào xu hướng và mùa vụ ngày. Phần dư lớn nhất trong đợt nóng chỉ 11.364 MW (không robust)
và 22.576 MW (robust). Muốn tách đợt nóng thì cần thêm biến nhiệt độ (buổi 8).

**Tóm lại.** **Robust giảm trọng số điểm có phần dư lớn khi ước lượng xu hướng và mùa vụ, và để điểm đó lại trong phần dư. Nó cứu được
một giờ hỏng, không tách được sự kiện kéo dài nhiều ngày.**

**Tự kiểm tra.** Phần dư lượt đầu: 2, −2, 2, −2, 30. Tính $h$ và trọng số của điểm 30 và điểm 2.

<details>
<summary>Đáp án</summary>

|phần dư| = 2, 2, 2, 2, 30; trung vị 2; $h$ = 12. Điểm 30: $u$ = 2,5 ≥ 1 → trọng số 0. Điểm 2: $u$ = 2/12 = 1/6 → (1 − 1/36)² ≈ 0,95.
Nhầm hay gặp: dùng trung bình |phần dư| (7,6) thay trung vị; trung bình bị chính điểm 30 kéo lên, nên điểm lạ tự che mình.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.** Cơ quan thống kê khử mùa vụ bằng **X-13ARIMA-SEATS**. Nó làm cho dữ liệu tháng và quý, có
> xử lý ngày lễ và số ngày làm việc (FPP §3.5). statsmodels gọi được qua `x13_arima_analysis` nhưng cần chương trình `x13as` riêng; không dùng
> cho dữ liệu giờ. **Chuỗi đã khử mùa vụ** ($y - S$) vẫn chứa phần dư nên không trơn; muốn tìm điểm đổi chiều thì đọc **xu hướng**, đừng đọc
> chuỗi khử mùa vụ.

## 5. Lab từng bước

Lệnh gõ trong terminal ở thư mục `lab/`. Code các bước nằm sẵn trong `code/lab.ipynb` (mở bằng `python lab.py notebook` hoặc
VS Code), chạy từng ô từ trên xuống. Bạn sửa `code/phan_ra.py`; notebook tự nạp lại bản mới.

### Bước 1 — Chạy code đầu buổi

**Mục đích:** thấy phân rã hiện tại để lại gì.

```bash
python lab.py up           # một lần: môi trường + dữ liệu EIA-930 (~90 MB), kiểm sha256
python lab.py check        # 5/7 test đỏ
python lab.py notebook     # chạy ô bước 1
```

```text
8784 giờ, NaN 47, 2024-01-01 06:00:00 → 2025-01-01 05:00:00
{'F_T': 0.828, 'F_S_24': 0.618}
('dayofweek', 'hour') mẫu hình còn trong phần dư: 0.0067
('month', 'hour') mẫu hình còn trong phần dư: 0.1016
```

**Đọc kết quả:** không có `F_S_168`, tức không tách mùa vụ tuần; tỷ lệ mẫu hình tháng × giờ 0,10, tức 10% phương sai chuỗi còn là mẫu
hình trong phần dư (mục 4.3).

### Bước 2 — Tự viết phân rã cổ điển

**Mục đích:** nối ví dụ tay 12 quý (mục 4.1) với code, rồi xem mùa vụ tuần trốn vào xu hướng.

Ô bước 2 chạy phân rã cổ điển tự viết trên 12 quý và trên PJM, so với `seasonal_decompose`, rồi in trung bình xu hướng theo thứ.

**Đọc kết quả:** ví dụ 12 quý ra đúng bảng mục 4.1, và trên PJM bản tự viết khớp thư viện tới từng số. Trung bình xu hướng cuối tuần
thấp hơn giữa tuần như bảng mục 4.3.

### Bước 3 — Đổi sang MSTL (24, 168)

**Mục đích:** sửa `phan_ra` theo mục 4.4.

Dùng `MSTL(y, periods=(24, 168), stl_kwargs={"robust": robust})`, trả bảng các cột `y, trend, seasonal_24, seasonal_168, resid`. Chạy lại
ô bước 1:

```text
{'F_T': 0.888, 'F_S_24': 0.829, 'F_S_168': 0.415}
('dayofweek', 'hour') mẫu hình còn trong phần dư: 0.0
('month', 'hour') mẫu hình còn trong phần dư: 0.0006
```

**Đọc kết quả:** có `F_S_168`; hai tỷ lệ mẫu hình về gần 0. Nếu mọi số là `nan` thì đầu vào còn NaN (quên `lap_cho_trong`).

### Bước 4 — Robust quanh giờ hỏng

**Mục đích:** thấy bảng mục 4.6 trên máy mình.

Ô bước 4 so `phan_ra(y)` với `phan_ra(y, robust=True)`: phần dư lúc 17:00 UTC ngày 21/11 và mùa vụ ngày cùng giờ các ngày 18–25/11.

**Đọc kết quả:** phần dư giờ hỏng khoảng −26.300 (không robust) và −36.300 MW (robust); mùa vụ ngày 20/11 đổi dấu giữa hai bản. Robust
chạy lâu hơn (khoảng 10 giây).

### Bước 5 — Mùa vụ ngày theo tháng

**Mục đích:** tự vẽ lại hình cuối mục 4.4.

Lấy `seasonal_24`, đổi giờ sang New York, lấy trung bình theo (tháng, giờ), vẽ mỗi tháng một đường. Rồi:

```bash
python lab.py check        # 7/7 xanh
```

**Đọc kết quả:** biên độ tháng 7 gấp khoảng ba lần tháng 1, như hình mục 4.4. Xanh 7/7 là xong; `test_robust_giu_gio_hong_trong_phan_du` còn đỏ
thì `phan_ra` chưa truyền `robust` vào `stl_kwargs`.

## 6. Lỗi thường gặp & cách chẩn đoán

| Triệu chứng | Nguyên nhân | Chẩn đoán | Sửa |
|---|---|---|---|
| Xu hướng lõm mỗi cuối tuần | khai chu kỳ 24 cho chuỗi có mùa vụ 168 | trung bình xu hướng theo thứ | MSTL (24, 168) |
| Phần dư dao động đều theo ngày | mùa vụ ngày bị ép giống nhau cả năm | heatmap phần dư tháng × giờ | STL/MSTL |
| STL trả toàn NaN, không báo lỗi | đầu vào còn NaN | `y.isna().sum()` | nội suy hoặc điền trước, ghi rõ số giờ đã điền |
| `ValueError: This function does not handle missing values` | `seasonal_decompose` gặp NaN | như trên | như trên |
| Phần dư rất nhỏ, "phân rã tuyệt vời" | cửa sổ xu hướng quá ngắn, xu hướng nuốt mùa vụ và thời tiết | xu hướng có răng cưa theo ngày, tuần không? | tăng `trend`, hoặc MSTL |
| Một điểm lạ làm méo mùa vụ cả tuần | không robust | mùa vụ có vết lặp đúng giờ lỗi | `robust=True` |
| Robust vẫn không tách được sự kiện dài | sự kiện nhiều ngày chạy vào xu hướng | xem xu hướng quanh sự kiện | thêm biến giải thích (nhiệt độ, buổi 8) |
| Mùa vụ lệch 1 giờ quanh tháng 3 và 11 | phân rã trên giờ địa phương có lỗ, lặp | đếm số giờ mỗi ngày | làm trên UTC |
| `extrapolate_trend='freq'` phát FutureWarning | tên cũ, bị bỏ ở statsmodels 0.16 | đọc cảnh báo | `extrapolate_trend='period'` |
| $F_S$ hai báo cáo lệch nhau | khác phương pháp hoặc cửa sổ | in tham số | báo $F$ kèm tên phân rã |
| Chép cửa sổ từ R sang Python ra kết quả khác | mặc định khác nhau (feasts 11/21; statsmodels STL 7/47, MSTL 11/15) | in tham số | khai báo rõ |

## 7. Bài tập về nhà

1. **Vùng khác.** Chạy `phan_ra` cho ERCO (Texas) và ISNE (New England). So $F_{S,168}$ với PJM và giải thích bằng heatmap phần dư.
2. **Cửa sổ mùa vụ.** MSTL với `windows=(7, 7)`, `(11, 15)`, `(51, 51)`. Mỗi lựa chọn đổi mùa vụ ngày tháng 7 và phần dư thế nào?
3. **Ba mùa vụ.** Thử `periods=(24, 168, 8766)` (năm ≈ 365,25 × 24 giờ) trên chuỗi một năm của buổi. Điều gì xảy ra với chu kỳ năm, vì sao?

## 8. Tiêu chí "Xong khi"

- [ ] `python lab.py check` xanh 7/7.
- [ ] Phân rã tay được một chuỗi 12 điểm với $m$ = 4 và khớp `seasonal_decompose`.
- [ ] Chỉ ra bằng hình và số nhịp tuần "trốn" ở đâu khi dùng cổ điển chu kỳ 24.
- [ ] Báo $F_T$, $F_{S,24}$, $F_{S,168}$ kèm tên phương pháp và nói bằng lời.
- [ ] Giải thích vì sao robust sửa được giờ hỏng 21/11 nhưng không tách được đợt nóng tháng 7.

## 9. Đọc thêm

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way* — chương 3 (phân rã), §4.3 (độ
  mạnh): https://otexts.com/fpppy/
- Cleveland, R.B., Cleveland, W.S., McRae, J.E. & Terpenning, I. (1990). STL: A Seasonal-Trend Decomposition Procedure Based on Loess.
  *Journal of Official Statistics* 6(1), 3–73.
- Bandara, K., Hyndman, R.J. & Bergmeir, C. (2025). MSTL: a seasonal-trend decomposition algorithm for time series with multiple
  seasonal patterns. *International Journal of Operational Research* 52(1), 79–98 (arXiv:2107.13462).
- statsmodels 0.15 — `seasonal_decompose`, `STL`, `MSTL`.
- U.S. EIA — Form EIA-930 instructions; Ruggles, T.H. et al. (2020). Developing reliable hourly electricity demand data through
  screening and imputation. *Scientific Data* 7, 155.
