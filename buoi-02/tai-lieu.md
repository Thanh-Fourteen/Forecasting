# Buổi 2 — Xác suất và thống kê cho dự báo

## 1. Mục tiêu

Buổi này dạy khối thống kê nền cho mọi buổi sau. Bạn sẽ tính tay được quantile, trung vị, trung
bình, độ lệch chuẩn và hệ số tương quan $r$; biết 1,96 từ đâu ra và đo được tỷ lệ phủ thật của một khoảng "95%"; đọc
được một kiểm định giả thuyết; và biết vì sao chuỗi thời gian cần block bootstrap.

## 2. Nhắc lại buổi trước

Các ý của buổi 1 dùng lại hôm nay:

- **Dự báo** là một phát biểu về giá trị chưa biết ở tương lai, làm từ dữ liệu đã có tới **mốc cắt dữ liệu**. Ví dụ:
  lúc 7h sáng, dùng dữ liệu tới 6h để đoán lượt thuê xe lúc 17h.
- **Sai số = thực tế − dự báo.** Dự báo 400, thực tế 460 thì sai số là +60. Sai số dương nghĩa là thực tế cao hơn
  dự báo, tức ta đã dự báo **thấp**.
- **MAE** (sai số tuyệt đối trung bình): bỏ dấu các sai số rồi lấy trung bình. Sai số +2 và −4 cho MAE = (2 + 4)/2 = 3.
- **Chi phí lệch không đối xứng.** Nếu mỗi đơn vị thiếu mất $C_u$ đồng và mỗi đơn vị thừa mất $C_o$ đồng, nên đặt
  ở quantile mức $C_u/(C_u + C_o)$. Thiếu mất 4, thừa mất 1 thì đặt ở quantile 4/(4 + 1) = 0,8. Mục 4.1 định
  nghĩa quantile đầy đủ.
- **Chấm trên dữ liệu chưa dùng.** Sai số đo trên chính dữ liệu đã dùng để làm dự báo luôn đẹp giả tạo.

## 3. Trạng thái đầu buổi

Sau `cd lab && make up`:

| Hạng mục | Trạng thái |
|---|---|
| Dữ liệu | `du-lieu/raw/uci-bike-sharing/hour.csv` — 17.379 giờ, 01/01/2011 → 31/12/2012 (đủ thì là 17.544; thiếu 165 giờ không có số liệu), sha256 `e03de4ee4ef4`; `day.csv` 731 ngày; `Readme.txt` |
| Nguồn | Capital Bikeshare (Washington D.C.), UCI Machine Learning Repository, CC BY 4.0 (`NGUON.txt`) |
| Môi trường | Python 3.12; numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, matplotlib 3.11.2 |
| `code/xac_suat.py` | `quantile_tu_viet`, `khoang_du_bao`, `ty_le_phu`, `khoang_tin_cay_trung_binh`, `ar1`, `ty_le_phu_khoang_tin_cay`, `doc_luot_thue`, `khoang_theo_gio` |
| **Đang cố tình sai** | `khoang_du_bao` = trung bình ± 1,96 × độ lệch chuẩn; `khoang_tin_cay_trung_binh` lấy mẫu lại từng giờ độc lập |
| **Triệu chứng** | trên dữ liệu luôn dương và lệch phải, cận dưới âm, đuôi dưới gần như không bao giờ bị vượt; khoảng tin cậy 95% trên chuỗi mô phỏng tự tương quan chỉ chứa trung bình thật **60%** số lần |
| `make check` lúc này | ĐỎ: 5/8 test hỏng |

Các chữ trong bảng được định nghĩa ở mục 4. sha256 là "dấu vân tay" của file, để kiểm đã tải đúng file. `make check`
chạy bộ chấm tự động (các test) và báo test nào hỏng.

## 4. Lý thuyết

### Từ mới trong buổi

| Thuật ngữ | Nghĩa một câu | Ví dụ |
|---|---|---|
| biến ngẫu nhiên (random variable) | Đại lượng chưa biết trước giá trị, chỉ biết khả năng của từng giá trị. | Lượt thuê lúc 17h mai. |
| histogram | Biểu đồ cột đếm có bao nhiêu giá trị rơi vào mỗi khoảng. | 0–9: 6 số; 10–19: 2 số. |
| quantile, trung vị | Quantile $p$: giá trị nhỏ nhất mà ít nhất tỷ lệ $p$ số liệu ≤ nó. Trung vị là quantile 0,5. | 2, 3, 5, 6, 8, 9, 12, 18, 36 → quantile 0,8 = 18. |
| phương sai, độ lệch chuẩn | Gần như trung bình của bình phương khoảng cách tới trung bình (tổng chia $n-1$); độ lệch chuẩn là căn của nó. | 2, 4, 6 → 4 và 2. |
| hệ số lệch (skewness) | Dương khi đuôi phải dài (vài số rất lớn). Khác độ lệch chuẩn. | 1, 1, 2, 2, 3, 20 → dương. |
| pinball loss | Phạt dự báo quantile $\tau$: thiếu phạt $\tau$, thừa phạt $1-\tau$ mỗi đơn vị. | $\tau$ = 0,8, thật 10, dự báo 8 → 1,6. |
| phân phối chuẩn (normal distribution) | Hình chuông đối xứng; 95% giá trị trong trung bình ± 1,96 độ lệch chuẩn. | 100 ± 1,96 × 10 → 80,4–119,6. |
| khoảng tin cậy | Khoảng cho một con số cố định chưa biết, như trung bình thật. | Khác khoảng dự báo (cho một giá trị tương lai). |
| tỷ lệ phủ (coverage) | Tỷ lệ số lần giá trị thật rơi vào khoảng. | 64 trên 100 lần trúng → 64%. |
| trong mẫu / ngoài mẫu (in-sample / out-of-sample) | Đo trên dữ liệu đã dùng / chưa dùng để dựng. | Dựng từ 2011, chấm 2012: ngoài mẫu. |
| xu hướng | Hướng đi lâu dài của chuỗi. | Lượt thuê 2011 → 2012 tăng. |
| tương quan (hệ số $r$) | Số từ −1 đến 1 đo hai biến cùng tăng giảm theo đường thẳng tới đâu. | 1, 2, 3 và 2, 4, 6 → $r$ = 1. |
| tự tương quan (autocorrelation) | Tương quan của chuỗi với chính nó dời lùi $k$ bước. | 1, 3, 1, 3 → trễ 1: −0,75. |
| kiểm định giả thuyết, giả thuyết không ($H_0$) | Dùng dữ liệu xem có đủ bằng chứng bác bỏ giả định mặc định $H_0$ không. | $H_0$: "đồng xu cân đối". |
| p-value | Nếu $H_0$ đúng, xác suất gặp kết quả lệch cỡ này hoặc hơn. | ≥ 9 ngửa / 10 lần: 11/1.024. |
| mức ý nghĩa ($\alpha$) | Ngưỡng chọn trước; p nhỏ hơn thì bác bỏ $H_0$. Hay dùng 0,05. | p = 0,011 → bác bỏ. |
| mẫu / tổng thể | Mẫu: số liệu có trong tay. Tổng thể: mọi giá trị "giống như vậy" có thể xảy ra; "trung bình thật" là trung bình của nó. | 9 giờ đang có là một mẫu. |
| seed | Con số khởi đầu của bộ sinh số ngẫu nhiên; cùng seed thì ra cùng dãy số. | `np.random.default_rng(2026)`. |
| i.i.d. | Độc lập và cùng phân phối. | Các lần tung xúc xắc. |
| định lý giới hạn trung tâm (CLT) | Trung bình của nhiều số i.i.d. có phân phối gần hình chuông. | Trung bình 30 lần tung xúc xắc quanh 3,5 = (1 + … + 6)/6. |
| tự hồi quy (autoregressive), AR(1) | Giá trị mới = $\rho$ × giá trị cũ + phần ngẫu nhiên. | 0,7 × 10 + 0,5 = 7,5. |
| cỡ mẫu hiệu dụng (effective sample size) | Số quan sát độc lập mà dữ liệu tự tương quan "đáng giá". | 200 điểm, $\rho$ = 0,7 → 35. |
| bootstrap, block bootstrap | Rút lại có hoàn lại từ chính dữ liệu để xem một con số dao động cỡ nào; block rút cả khúc liền nhau. | Từ 5, 7, 9 rút 7, 7, 5. |

Sáu khái niệm chính của buổi là 4.1–4.6. Ba mục đầu mô tả **một** đại lượng. Mục 4.4 nói về **hai** đại lượng. Mục
4.5 hỏi "khác biệt thấy được là thật hay do may". Mục 4.6 hỏi "một con số tính từ mẫu dao động cỡ nào".

### 4.1 Phân phối, quantile, trung vị

**Vấn đề.** Lúc 17h ngày mai trạm có bao nhiêu lượt thuê? Không ai biết chắc, nhưng ta biết dưới 100 lượt thì hiếm,
quanh 400 thì hay gặp. Cần một cách ghi lại "khả năng của từng mức".

**Trực giác.** Đại lượng chưa biết trước như vậy gọi là **biến ngẫu nhiên**. Bảng "mỗi giá trị hay gặp tới đâu" là
**phân phối** của nó. Cách đơn giản nhất để thấy phân phối là xem lại nhiều ngày cũ.

**Ví dụ số nhỏ — tự tính tay.** Lượt thuê của 9 giờ đêm khác nhau: 8, 2, 36, 5, 12, 3, 18, 6, 9.

1. **Xếp tăng dần:** 2, 3, 5, 6, 8, 9, 12, 18, 36.
2. **Histogram** là đếm theo khoảng rồi vẽ mỗi khoảng một cột: 0–9 → 6 số, 10–19 → 2 số, 20–29 → 0 số, 30–39 → 1 số.
   Các cột cao bên trái, thấp dần sang phải, và có một số lẻ loi rất xa (36). Ta nói phân phối **lệch phải**, hay có
   **đuôi phải dài**.
3. **Đường tích luỹ** (CDF, hàm phân phối tích luỹ) tại mốc $y$ là tỷ lệ số giá trị nhỏ hơn hoặc bằng $y$. Tại 8: có 5
   số ≤ 8 (2, 3, 5, 6, 8) → 5/9 ≈ 0,56. Tại 12: có 7 số → 7/9 ≈ 0,78.
4. **Quantile** làm ngược lại: cho một tỷ lệ, tìm mốc. Quantile mức $p$ là giá trị **nhỏ nhất** mà ít nhất tỷ lệ $p$
   số liệu nhỏ hơn hoặc bằng nó.

Cách đếm tay (giống buổi 1): xếp tăng, lấy vị trí $= p \times n$, **làm tròn lên**.

- Quantile 0,8: 0,8 × 9 = 7,2, làm tròn lên thành 8. Số thứ 8 là **18**.
- Kiểm lại: 8 trên 9 số (89%) ≤ 18, tức "ít nhất 80%". Mốc 12 thì chỉ 7/9 ≈ 78%, chưa đủ. Vậy 18 là mốc nhỏ nhất đạt.
- Quantile 0,5: 0,5 × 9 = 4,5, làm tròn lên thành 5. Số thứ 5 là **8**. Đây là **trung vị**, số đứng giữa.
- Khi số lượng **chẵn** thì không có một số đứng giữa. Với 1, 2, 3, 4: cách đếm tay cho 0,5 × 4 = 2 → số thứ 2, tức 2.
  Thói quen phổ biến (và `np.median`) lại lấy trung bình hai số giữa: (2 + 3)/2 = 2,5. Cả hai đều gọi là trung vị, chỉ
  khác quy ước.

Hiểu lầm hay gặp: quantile 0,8 **không phải** "80% của số lớn nhất" (0,8 × 36 = 28,8). Nó là mốc mà 80% số liệu nằm dưới hoặc bằng.

![Histogram lệch phải và đường tích luỹ của lượt thuê theo giờ](hinh/histogram-tich-luy.png)

**Cách đọc hình.**

1. **Trục ngang**: ô trái là lượt thuê trong một giờ (lượt), chia khoảng rộng 25 lượt; ô phải là mốc $y$ (lượt).
2. **Trục dọc**: ô trái là số giờ rơi vào mỗi khoảng; ô phải là tỷ lệ số giờ có lượt thuê ≤ $y$, từ 0 tới 1.
3. **Ký hiệu**: vạch cam liền là trung bình, vạch xanh đứt là trung vị. Ô phải, đường chấm cam chỉ cách đọc quantile.
4. **Nhìn vào đâu**: ô phải, đi ngang từ 0,9 trên trục dọc tới đường cong rồi thả xuống: gặp 451. Đi từ 0,5: gặp 142.
5. **Kết luận**: lượt thuê theo giờ lệch phải. Trung bình (189) lớn hơn trung vị (142) vì vài giờ rất đông kéo lên.

**Công thức.**

$$
F(y) = \frac{\text{số giá trị} \le y}{n}, \qquad q_p = \min\{\, y : F(y) \ge p \,\}
$$

- $n$: số giá trị. $F(y)$: đường tích luỹ, tỷ lệ giá trị không vượt $y$.
- $\{\, y : F(y) \ge p \,\}$: "tập các mốc $y$ mà tỷ lệ không vượt $y$ ít nhất là $p$". Dấu hai chấm đọc là "sao cho".
- $\min$: lấy mốc nhỏ nhất trong tập đó. $q_p$: quantile mức $p$.

**Nói bằng lời.** Quantile $p$ là mốc nhỏ nhất đủ để tỷ lệ $p$ số liệu nằm dưới hoặc bằng nó. Với 9 số trên và
$p$ = 0,8: $F(12) = 7/9 \approx 0{,}78$ chưa đủ, $F(18) = 8/9 \approx 0{,}89$ đủ, nên $q_{0,8} = 18$. (Sách thường viết
$\inf$ thay cho $\min$; với dữ liệu hữu hạn hai chữ này như nhau.)

**Tự viết bằng NumPy — và vì sao máy ra số khác.** Máy mặc định không đếm như trên. `np.quantile` **nội suy**, tức lấy
một điểm nằm giữa hai số kề nhau theo tỷ lệ. Nó gán cho số nhỏ nhất mức $q$ = 0 và đặt ở vị trí 0, số lớn nhất mức $q$ = 1 ở
vị trí $n - 1$, rồi chia đều phần giữa. Vì vậy mức $q$ ứng với vị trí $(n - 1) \times q$:

```python
import numpy as np

def quantile_tu_viet(x, q):
    x = np.sort(np.asarray(x, dtype=float))   # 2, 3, 5, 6, 8, 9, 12, 18, 36 — đánh số 0, 1, …, 8
    h = (x.size - 1) * q                      # vị trí "lẻ": (9 − 1) × 0,8 = 6,4
    duoi = np.floor(h).astype(int)            # phần nguyên của h: 6  → x[6] = 12
    tren = np.minimum(duoi + 1, x.size - 1)   # số kế tiếp: 7         → x[7] = 18
    return x[duoi] + (h - duoi) * (x[tren] - x[duoi])   # 12 + 0,4 × (18 − 12) = 14,4

quantile_tu_viet([8, 2, 36, 5, 12, 3, 18, 6, 9], 0.8)   # 14.4
```

Đây là hàm `quantile_tu_viet` trong `code/`. Phép tính cho mức 0,8 nằm trong các chú thích bên phải: kết quả nằm
giữa hai số kề nhau, cách số nhỏ một phần tỷ lệ bằng phần lẻ của vị trí.

**Thư viện.** Muốn máy đếm đúng như tay, thêm `method="inverted_cdf"`: `np.quantile(x, 0.8, method="inverted_cdf")` ra
18. Với hàng nghìn số, hai cách gần như trùng nhau. `pd.Series(x).quantile(q)` cũng nội suy.

**Dữ liệu thật.** Trên 17.379 giờ, trung vị là 142 lượt: một nửa số giờ có không quá 142 lượt (hình trên).

**Tóm lại.** **Phân phối cho biết mỗi giá trị hay gặp tới đâu. Quantile $p$ là mốc mà tỷ lệ $p$ số liệu nằm dưới
hoặc bằng; trung vị là quantile 0,5 (với số lượng chẵn, `np.median` lấy trung bình hai số giữa). Tính tay: vị trí $p \times n$ làm tròn lên. Máy mặc định nội suy nên có thể ra
số lẻ.**

**Tự kiểm tra.** Dãy 4, 1, 7, 3, 10. Tính tay quantile 0,6.

<details>
<summary>Đáp án</summary>

Xếp tăng: 1, 3, 4, 7, 10. Vị trí 0,6 × 5 = 3, đã là số nguyên nên không cần làm tròn. Số thứ 3 là **4**. Kiểm lại:
3 trên 5 số (60%) ≤ 4. Nhầm hay gặp là lấy 0,6 × 10 = 6 (60% của số lớn nhất).

</details>

### 4.2 Trung bình, độ phân tán — và nên báo con số nào

**Vấn đề.** Nếu chỉ được báo **một** con số, nên báo trung bình, trung vị hay quantile? Và đo độ dao động bằng gì?

**Trực giác.** Lương 9 nhân viên và 1 giám đốc: trung bình bị lương giám đốc kéo lên, trung vị thì không.

**Mẫu và tổng thể.** 9 giờ ta có trong tay là một **mẫu**. Cái ta thật sự muốn biết là **tổng thể**: mọi giờ "giống như
vậy" có thể xảy ra, coi như vô số giờ. **Trung bình thật** là trung bình của tổng thể; ta không bao giờ thấy nó, chỉ
ước lượng bằng trung bình mẫu. Lấy một mẫu 9 giờ khác thì trung bình mẫu ra số khác. "**Lặp lại việc lấy mẫu**" (mục
4.3, 4.6) nghĩa là tưởng tượng lấy rất nhiều mẫu như vậy và xem con số tính từ mẫu thay đổi ra sao.

**Ví dụ số nhỏ — tự tính tay.** Vẫn 9 giờ: 2, 3, 5, 6, 8, 9, 12, 18, 36.

1. **Trung bình** = tổng chia số lượng: 99/9 = 11. Trung vị là 8. Trung bình lớn hơn vì số 36 kéo lên.
2. **Độ lệch** mỗi số khỏi trung bình: 2 − 11 = −9, rồi lần lượt −8, −6, −5, −3, −2, 1, 7, 25.
3. **Bình phương** các độ lệch: 81, 64, 36, 25, 9, 4, 1, 49, 625. Tổng = 894.
4. **Phương sai**: 894 / (9 − 1) = 111,75 (đơn vị: lượt bình phương).
5. **Độ lệch chuẩn**: √111,75 ≈ 10,57 lượt. Đây là "khoảng cách điển hình" từ một số tới trung bình.

**Chia $n - 1$ hay chia $n$?** Có hai quy ước, và bài này ghi rõ khi dùng cái nào:

- $s$ (chia $n - 1$): 894/8 = 111,75 → $s$ = 10,57. Dùng khi ước lượng độ phân tán của tổng thể từ một mẫu.
- $\sigma$ (sigma, chia $n$): 894/9 = 99,33 → $\sigma$ = 9,97. Dùng khi coi chính các số đang có là toàn bộ tổng thể.
  Vì thế $\sigma$ cũng là tên của **độ lệch chuẩn của tổng thể** (mục 4.6 dùng nghĩa này).
- Vì sao chia $n - 1$? Trung bình mẫu là con số làm tổng bình phương khoảng cách **nhỏ nhất** (bảng phạt bình phương
  bên dưới). Nên tổng bình phương tính tới trung bình mẫu luôn nhỏ hơn một chút so với tính tới trung bình thật. Chia
  cho $n - 1$ thay vì $n$ bù lại phần đó (Phụ lục B, mục 5). Với $n$ hàng nghìn, hai cách gần như bằng nhau.

**Hệ số lệch** đo đuôi dài về phía nào: lấy trung bình của $(\text{độ lệch}/s)^3$. Lập phương giữ dấu và phóng đại số
lớn, nên số 36 (lệch +25) góp gần hết, tám số còn lại gần 0. Kết quả **+1,35**: dương, đuôi phải dài. `scipy.stats.skew`
ra 1,61 (chia cho σ), pandas ra 1,95 (hiệu chỉnh thêm cho mẫu nhỏ): khác quy ước, cùng dấu, cùng ý. Với hàng nghìn số,
ba cách gần như trùng. Chi tiết: Phụ lục B, mục 6.

**Công thức.**

$$
\bar y = \frac{1}{n}\sum_{i=1}^{n} y_i, \qquad s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(y_i - \bar y)^2, \qquad s = \sqrt{s^2}
$$

- $y_i$: giá trị thứ $i$. $\sum_{i=1}^{n}$: cộng từ giá trị thứ 1 tới thứ $n$.
- $\bar y$ (đọc "y gạch"): trung bình. $s^2$: phương sai. $s$: độ lệch chuẩn (chia $n - 1$). Từ đây mọi
  công thức dùng $s$. Cách dựng khoảng "trung bình ± 1,96 × $s$" ở mục 4.3 gọi tắt là **±1,96s** (code và sách hay viết
  "±1.96σ").

**Nói bằng lời.** Trung bình là tổng chia số lượng: 99/9 = 11. Phương sai là trung bình (chia $n - 1$) của bình phương
khoảng cách tới trung bình: 894/8 = 111,75. Độ lệch chuẩn là căn của nó, 10,57 lượt, cùng đơn vị với dữ liệu.

**Con số nào để báo? Tuỳ cách bị phạt.** **Hàm mất mát** là quy tắc tính tiền phạt cho một dự báo sai. Với giá trị thật
$y$ và dự báo $c$, ba cách phạt:

- **Tuyệt đối** $\lvert y - c \rvert$: lệch bao nhiêu phạt bấy nhiêu, thiếu hay thừa như nhau.
- **Bình phương** $(y - c)^2$: lệch 2 phạt 4, lệch 10 phạt 100, nên rất sợ lệch xa.
- **Pinball** mức $\tau$: thiếu mỗi đơn vị phạt $\tau$, thừa mỗi đơn vị phạt $1 - \tau$ (công thức ngay dưới bảng).

Thử dự báo mọi giờ bằng cùng một con số $c$, rồi tính phạt trung bình trên 9 giờ:

| Dự báo c | Phạt tuyệt đối trung bình | Phạt bình phương trung bình | Pinball τ = 0,8 trung bình |
|---|---|---|---|
| 8 (trung vị) | **6,56** | 108,3 | 4,18 |
| 11 (trung bình) | 7,33 | **99,3** | 3,67 |
| 18 (quantile 0,8) | 11,00 | 148,3 | **3,40** |

**Đọc bảng.** Mỗi cột có một dòng nhỏ nhất (in đậm), và mỗi cột chọn một dòng khác nhau. Thử mọi $c$ từ 0 tới 40
(bước 0,5) cũng ra đúng ba đáy này. Trực giác:

- **Tuyệt đối → trung vị.** Nhích $c$ lên 1 thì mỗi số bên dưới phạt thêm 1, mỗi số bên trên bớt 1. Hai bên cân nhau
  ở trung vị (tại 8: bốn số dưới, bốn số trên).
- **Bình phương → trung bình.** Số ở xa (36) bị phạt rất nặng nên kéo $c$ về phía nó, tới đúng trung bình.
- **Pinball $\tau$ → quantile $\tau$.** Nhích $c$ lên 1: mỗi số nằm dưới $c$ bị phạt thêm $1 - \tau$, mỗi số nằm
  trên bớt phạt $\tau$. Hai bên cân khi (tỷ lệ dưới) × $(1 - \tau)$ = (tỷ lệ trên) × $\tau$, tức tỷ lệ dưới đúng bằng $\tau$.

Chi tiết cả ba cách: Phụ lục B, mục 8.

**Pinball loss** là cách phạt của bài toán chi phí lệch ở buổi 1:

$$
L_\tau(y, c) = \begin{cases} \tau\,(y - c) & \text{nếu } y \ge c \text{ (dự báo thiếu)} \\ (1-\tau)\,(c - y) & \text{nếu } y < c \text{ (dự báo thừa)} \end{cases}
$$

- $y$: giá trị thật. $c$: con số dự báo. $\tau$ (tau): mức quantile muốn nhắm, từ 0 tới 1.

**Nói bằng lời.** Thiếu mỗi đơn vị phạt $\tau$, thừa mỗi đơn vị phạt $1 - \tau$. Với $\tau$ = 0,8: thật 36, dự báo
18 thì thiếu 18, phạt 0,8 × 18 = 14,4. Thật 2, dự báo 18 thì thừa 16, phạt 0,2 × 16 = 3,2. Thiếu đắt gấp 0,8/0,2 = 4
lần thừa, đúng tỷ lệ 4 : 1 ở buổi 1.

**Tự viết bằng NumPy.**

```python
y = np.array([2, 3, 5, 6, 8, 9, 12, 18, 36])
y.mean(), np.median(y), y.var(ddof=1), y.std(ddof=1)   # 11.0, 8.0, 111.75, 10.57 — ddof=1 là chia n − 1
sai = y - 18                                            # dự báo c = 18
np.where(sai >= 0, 0.8 * sai, -0.2 * sai).mean()        # pinball 0,8: 3.40
```

**Thư viện.** `pd.Series(y).std()` mặc định chia $n - 1$, còn `np.std(y)` mặc định chia $n$: luôn ghi rõ `ddof`.

**Dữ liệu thật.** Lượt thuê theo giờ có trung bình 189,46, độ lệch chuẩn 181,39 và hệ số lệch 1,277 (ba quy ước đều ra
1,277): lệch phải. Hình dưới
thử mọi hằng số $c$ trên cả 17.379 giờ. Lưu ý: ô pinball dùng $\tau$ = **0,9**, không phải 0,8 như ví dụ nhỏ.

![Ba hàm mất mát, ba con số tối ưu](hinh/ham-mat-mat.png)

**Cách đọc hình.**

1. **Trục ngang** (cả ba ô): con số dự báo $c$, dùng chung cho mọi giờ, từ 0 tới 700 lượt, bước 2.
2. **Trục dọc**: phạt trung bình trên 17.379 giờ; đơn vị khác nhau giữa ba ô nên chỉ so hình dạng.
3. **Ký hiệu**: ô trái là phạt bình phương, ô giữa phạt tuyệt đối, ô phải pinball $\tau$ = 0,9. Đường xanh là phạt
   theo $c$; vạch cam đứt là $c$ tốt nhất.
4. **Nhìn vào đâu**: vị trí đáy của mỗi ô, so với bảng dưới. Ô phải dốc bên trái hơn vì dự báo thấp bị phạt gấp 9 lần
   (0,9 so với 0,1).
5. **Kết luận**: mỗi cách phạt chọn một con số khác nhau, đúng như ví dụ 9 giờ.

| Ô | Cách phạt | Đáy của đường | Đại lượng của mẫu |
|---|---|---|---|
| trái | bình phương | 189,46 | trung bình |
| giữa | tuyệt đối | 142 | trung vị |
| phải | pinball $\tau$ = 0,9 | 452 | quantile 0,9 ≈ 451 |

**Đọc bảng.** Cột 3 khớp cột 4. Dòng cuối lệch chưa tới 1 lượt chỉ vì hình thử $c$ theo bước 2 (450, 452…), nên
không thể dừng đúng 451. Trung bình cao hơn trung vị khoảng
một phần ba (so với trung vị): với dữ liệu lệch phải, "dự báo trung bình" và "dự báo trung vị" khác hẳn nhau.

**Tóm lại.** **Trung bình và trung vị đo "mức"; phương sai và độ lệch chuẩn đo "độ phân tán"; hệ số lệch dương báo
đuôi phải dài. Con số nên báo do cách phạt quyết định: phạt bình phương → trung bình, phạt tuyệt đối → trung vị,
pinball $\tau$ → quantile $\tau$.**

**Tự kiểm tra.** Dãy 1, 2, 3, 4, 100. Một cửa hàng bị phạt thiếu và thừa như nhau cho mỗi đơn vị. Nên báo 22 hay 3?

<details>
<summary>Đáp án</summary>

Phạt thiếu và thừa như nhau mỗi đơn vị là phạt tuyệt đối, nên báo **trung vị 3**. Trung bình 22 bị số 100 kéo lên.
Nhầm hay gặp: nghĩ trung bình luôn là con số "an toàn nhất". Trung bình chỉ tốt nhất khi phạt theo bình phương.

</details>

### 4.3 Khoảng dự báo, tỷ lệ phủ, và con số 1,96

**Vấn đề.** Báo "17h mai có 65 tới 604 lượt, khả năng 95%" hữu ích hơn một con số: trạm biết cần chuẩn bị tối đa bao
nhiêu xe. Nhưng "95%" có thật là 95% không?

**Trực giác.** Nói "mai 28–33 độ, 95%" 100 lần mà 95 lần trúng thì lời hứa giữ được. **Tỷ
lệ phủ** là tỷ lệ số lần giá trị thật rơi vào khoảng.

**Đường cong thay cho histogram.** Vẽ histogram rồi co chiều cao sao cho tổng diện tích các cột bằng 1. Khi đó diện
tích các cột bên trái mốc $y$ đúng bằng tỷ lệ giá trị ≤ $y$. Có thật nhiều dữ liệu và cột thật hẹp thì đỉnh các cột
thành một đường cong trơn. Với đường cong đó: **diện tích dưới đường cong bên trái $y$ = tỷ lệ giá trị ≤ $y$**. Ví dụ:
một cột rộng 10 lượt, cao 0,02 có diện tích 10 × 0,02 = 0,2, tức 20% số giờ rơi vào khoảng 10 lượt đó.

**Con số 1,96 đến từ phân phối chuẩn.** Phân phối chuẩn là một đường cong như vậy, hình chuông, đối xứng quanh trung
bình. Tính bằng `scipy.stats.norm.cdf` (tỷ lệ bên trái một mốc), phần nằm giữa:

| Khoảng quanh trung bình | Tỷ lệ giá trị nằm trong |
|---|---|
| ± 1 độ lệch chuẩn | 68,3% |
| ± 1,96 độ lệch chuẩn | 95,0% |
| ± 2 độ lệch chuẩn | 95,4% |

**Đọc bảng.** 1,96 là con số làm phần ở giữa đúng 95%. Phần còn lại chia đều hai **đuôi**: 2,5% nằm dưới −1,96 và
2,5% nằm trên +1,96. Nói cách khác, 1,96 là quantile 0,975 của phân phối chuẩn có trung bình 0, độ lệch chuẩn 1. Với
một đường cong liên tục như vậy, quantile $p$ là mốc mà phần diện tích dưới đường cong bên trái nó đúng bằng $p$. Mọi
phân phối chuẩn là cùng một hình chuông, chỉ dời đi và co giãn. Vì vậy 1,96 dùng được cho mọi trung bình và độ lệch
chuẩn: trung bình 100, độ lệch chuẩn 10 → 95% nằm trong 100 ± 19,6.

Kiểm bằng máy. `scipy.stats.norm.ppf(p)` là hàm quantile của phân phối chuẩn: `norm.ppf(0.975)` → 1,95996. Rút 100.000
số ngẫu nhiên theo phân phối chuẩn → 94,98% nằm trong ±1,96. Mọi phép rút ngẫu nhiên trong bài ghi kèm **seed** (ở đây
seed 0): con số khởi đầu của bộ sinh số ngẫu nhiên. Cùng seed thì ra cùng dãy số, nên bạn chạy lại sẽ được đúng số trong
tài liệu.

**Ví dụ số nhỏ — tự tính tay.** Hai phép tính.

1. **Khoảng ±1,96 trên 9 giờ ở mục 4.1.** Trung bình 11, độ lệch chuẩn 10,57. Cận dưới 11 − 1,96 × 10,57 = −9,7.
   Cận trên 11 + 20,7 = 31,7. Cận dưới **âm** là vô lý với số lượt thuê. Số 36 lại nằm ngoài cận trên.
2. **Đếm tỷ lệ phủ, tách hai đuôi.** Khoảng [4; 20] và 10 giá trị thật 3, 7, 12, 15, 9, 30, 11, 6, 2, 25.
   - Trong khoảng: 7, 12, 15, 9, 11, 6 → 6/10 = 60% (tỷ lệ phủ).
   - Rơi **dưới** cận dưới: 3, 2 → 20%. Vượt **trên** cận trên: 30, 25 → 20%.
   - Khoảng 95% tốt có khoảng 2,5% ở **mỗi** đuôi. Chỉ báo "phủ 95%" có thể giấu một đuôi 0%, một đuôi 5%.

**Công thức** của khoảng 95%, hai cách:

$$
\big[\, \bar y - 1{,}96\, s \;;\; \bar y + 1{,}96\, s \,\big] \quad \text{hoặc} \quad \big[\, q_{0,025} \;;\; q_{0,975} \,\big]
$$

- $\bar y$, $s$: trung bình và độ lệch chuẩn của lịch sử (mục 4.2).
- $q_{0,025}$, $q_{0,975}$: quantile 0,025 và 0,975 của lịch sử (mục 4.1), gọi là **khoảng quantile thực nghiệm**.

**Nói bằng lời.** Cách một lấy trung bình cộng trừ 1,96 lần độ lệch chuẩn, và chỉ đúng khi dữ liệu hình chuông. Cách
hai lấy thẳng mốc mà 2,5% lịch sử nằm dưới và mốc mà 2,5% lịch sử nằm trên.

- Lượt thuê 17h năm 2011, cách một → [22; 678] lượt.
- Cùng dữ liệu, cách hai → [65; 604] lượt: cận dưới cao hơn, cận trên thấp hơn, đúng hình lệch phải.

**Khoảng dự báo khác khoảng tin cậy.**

- **Khoảng dự báo** nói về **một giá trị chưa quan sát**: lượt thuê lúc 17h ngày mai. Nó phải chứa cả dao động của
  chính giờ đó, nên có thêm dữ liệu cũng không hẹp về 0.
- **Khoảng tin cậy** nói về **một con số cố định chưa biết**, như "trung bình thật" của lượt thuê. Có càng nhiều dữ
  liệu thì ta càng biết rõ con số đó, nên khoảng hẹp dần (mục 4.6).
- Khoảng tin cậy dựng bằng trung bình ± 1,96 s/√n (mục 4.6). "95%" của nó là tần suất **của quy trình**: lặp lại việc
  lấy mẫu rồi dựng khoảng nhiều lần thì khoảng 95% số khoảng chứa con số thật. Một khoảng cụ thể thì hoặc chứa, hoặc không.
- Ví dụ chạy thật: xem cuối phần 1/√n ở mục 4.6 (20 lần lấy mẫu, 19 khoảng chứa con số thật).

**Tự viết bằng NumPy.** Hàm `ty_le_phu` trong `code/` tính ba tỷ lệ: `np.mean((y >= lo) & (y <= hi))`, `np.mean(y < lo)`
và `np.mean(y > hi)`. Với ví dụ [4; 20] ở trên, nó trả đúng 0,6; 0,2; 0,2.

**Dữ liệu thật.** Dựng khoảng **theo giờ**: với mỗi giờ 0, 1, …, 23, lấy lượt thuê của mọi ngày trong đoạn lịch sử ở
đúng giờ đó, rồi dựng một khoảng 95% từ các số ấy. Được 24 khoảng. Sau đó chấm: mỗi giờ của đoạn được chấm rơi vào
khoảng của giờ tương ứng hay không. **Trong mẫu** là chấm trên chính đoạn đã dựng; **ngoài mẫu** là chấm trên đoạn chưa
dùng. Mục tiêu: phủ 95%, mỗi đuôi 2,5%.

| Cách dựng | Chấm trên | Phủ | Rơi dưới cận dưới | Vượt cận trên |
|---|---|---|---|---|
| ±1,96s | 2011 (trong mẫu) | 96,4% | 0,3% | 3,3% |
| quantile thực nghiệm | 2011 (trong mẫu) | 95,3% | 2,2% | 2,6% |
| ±1,96s | 2012 (ngoài mẫu) | 72,5% | 0,1% | 27,4% |
| quantile thực nghiệm | 2012 (ngoài mẫu) | 70,1% | 0,5% | 29,3% |

**Đọc bảng.**

- **Hai dòng đầu: sai hình dạng.** Trong mẫu, hai cách phủ gần như nhau. Nhưng ±1,96s lệch hai đuôi: gần như không giờ
  nào rơi dưới cận dưới, còn đuôi trên thì quá 2,5%. Quantile thực nghiệm cân lại hai đuôi.
- **Hai dòng sau: tương lai khác quá khứ.** Lượt thuê trung bình mỗi giờ tăng từ 143,8 lượt (2011) lên 234,7 lượt
  (2012). Gần 3 trên 10 giờ của 2012 vượt cận trên dựng từ 2011. Đó là **dịch mức**: cả chuỗi dời lên cao hơn.
- Đổi sang quantile **không cứu được** dịch mức: còn kém ±1,96s một chút. Lý do: $s$ bị vài giờ rất đông kéo to nên
  cận trên của ±1,96s cao thừa (lúc 17h: 678 lượt, so với 604 của quantile), vô tình đỡ được một phần mức tăng. Quantile sửa được **hình dạng**, không sửa được
  **dịch mức**; sửa dịch mức phải mô hình hoá mức tăng, việc của các buổi mô hình.

> **Nâng cao — có thể bỏ qua lần đọc đầu.** Thêm một phép thử.
>
> - **Lịch sử gần hơn.** Dựng từ tháng 1–6/2012, chấm tháng 7–12/2012: ±1,96s phủ 91,5%, quantile 88,8%. Đỡ hơn vì mức
>   đã gần hơn, nhưng mức vẫn tăng tiếp.

**Tóm lại.** **1,96 là con số làm phân phối chuẩn có đúng 95% ở giữa, 2,5% mỗi đuôi. Với dữ liệu lệch phải, ±1,96s sai
hình dạng (cận âm, hai đuôi lệch); quantile thực nghiệm sửa được. Nhưng khi tương lai dịch mức, cả hai đều vỡ. Luôn chấm
ngoài mẫu và báo riêng hai đuôi.**

**Tự kiểm tra.** Khoảng 95% chấm trên 200 giờ: 190 giờ nằm trong, 0 giờ dưới cận dưới, 10 giờ vượt cận trên. Khoảng có
tốt không?

<details>
<summary>Đáp án</summary>

Tỷ lệ phủ 190/200 = 95%, đúng mục tiêu. Nhưng đuôi dưới 0% và đuôi trên 10/200 = 5%, lệch xa 2,5% mỗi bên. Cả khoảng
đang nằm **thấp hơn** mức cần: cận dưới thấp quá nên không giờ nào rơi dưới nó, cận trên thấp quá nên hay bị vượt.
Nhầm hay gặp là chỉ nhìn "95%" rồi kết luận khoảng tốt.

</details>

### 4.4 Tương quan

**Vấn đề.** Trời ấm hơn thì có nhiều người thuê xe hơn không? Nếu có, nhiệt độ dự báo ngày mai giúp dự báo lượt thuê.
Cần một con số đo "hai đại lượng cùng tăng giảm tới đâu".

**Trực giác.** Nếu ở hầu hết các ngày, nhiệt độ cao hơn mức thường thì lượt thuê cũng cao hơn mức thường, hai đại lượng
"cùng chiều": tương quan dương.

**Ví dụ số nhỏ — tự tính tay.** 5 ngày, nhiệt độ $x$ (°C) và lượt thuê $y$ (trăm lượt). Trung bình $\bar x$ = 100/5 = 20,
$\bar y$ = 350/5 = 70; hai cột giữa của bảng là độ lệch khỏi hai trung bình này:

| Ngày | x (°C) | y (trăm lượt) | x − 20 | y − 70 | tích |
|---|---|---|---|---|---|
| 1 | 10 | 40 | −10 | −30 | 300 |
| 2 | 15 | 60 | −5 | −10 | 50 |
| 3 | 20 | 50 | 0 | −20 | 0 |
| 4 | 25 | 90 | 5 | 20 | 100 |
| 5 | 30 | 110 | 10 | 40 | 400 |

**Đọc bảng.** Cột "tích" dương khi hai độ lệch cùng dấu. Ở đây
không có tích âm nào, nên hai đại lượng cùng chiều.

Các bước còn lại:

- Tổng các tích: 300 + 50 + 0 + 100 + 400 = 850.
- Tổng bình phương độ lệch của $x$: 100 + 25 + 0 + 25 + 100 = 250. Của $y$: 900 + 100 + 400 + 400 + 1.600 = 3.400.
- $r = 850 / \sqrt{250 \times 3.400} = 850 / 922{,}0 \approx$ **0,922**.

**Công thức.**

$$
r = \frac{\sum_{i}(x_i - \bar x)(y_i - \bar y)}{\sqrt{\sum_{i}(x_i - \bar x)^2 \cdot \sum_{i}(y_i - \bar y)^2}}
$$

- $x_i, y_i$: cặp giá trị thứ $i$ (cùng một ngày). $\bar x, \bar y$: hai trung bình.
- Tử số: tổng các tích độ lệch, dương khi hai bên hay cùng chiều. Mẫu số: chia để $r$ luôn nằm từ −1 tới 1.

**Nói bằng lời.** Nhân độ lệch của hai đại lượng theo từng ngày, cộng lại, rồi chia cho một số chuẩn hoá. Với 5 ngày
trên: 850 / 922,0 = 0,922, gần 1, tức gần như cùng tăng theo một đường thẳng.

Cách đọc $r$: 1 là cùng chiều hoàn hảo trên một đường thẳng; −1 là ngược chiều hoàn hảo; 0 là không có quan hệ
**thẳng**. Đổi đơn vị (°C sang °F, lượt sang trăm lượt) không làm $r$ đổi: nhân mọi $x$ với 10 thì tử số nhân 10, mẫu
số cũng nhân 10, hai cái triệt tiêu. Cộng thêm một hằng số thì các độ lệch khỏi trung bình không đổi.

![Nhiệt độ và giờ trong ngày so với lượt thuê](hinh/tuong-quan.png)

**Cách đọc hình.**

1. **Trục ngang**: ô trái là nhiệt độ đã chuẩn hoá (0 là lạnh nhất, 1 là nóng nhất trong bộ dữ liệu); ô phải là giờ
   trong ngày, 0–23.
2. **Trục dọc**: lượt thuê (lượt); ô trái chỉ lúc 17h, ô phải mọi giờ.
3. **Ký hiệu**: ô trái mỗi chấm là một ngày. Ô phải chấm xám là từng giờ, đường cam là trung bình của mỗi giờ.
4. **Nhìn vào đâu**: ô trái, đám chấm nghiêng lên nhưng dày và loe. Ô phải, đường cam có hai đỉnh (8h và 17h) và đáy
   lúc 4h.
5. **Kết luận**: $r$ đo quan hệ **thẳng**. Nhiệt độ cho $r$ = 0,59 lúc 17h. Giờ trong ngày quyết định lượt thuê rất
   mạnh, nhưng quan hệ cong nên $r$ chỉ 0,39.

**Tự viết bằng NumPy.**

```python
x = np.array([10, 15, 20, 25, 30]); y = np.array([40, 60, 50, 90, 110])
dx, dy = x - x.mean(), y - y.mean()
r = (dx * dy).sum() / np.sqrt((dx**2).sum() * (dy**2).sum())   # 0.922
np.corrcoef(x, y)[0, 1]                                         # 0.922 — thư viện, cùng số
```

**Thư viện.** `df[["temp", "cnt"]].corr()` trong pandas cho cả bảng $r$.

**Dữ liệu thật.** Cột `temp` (nhiệt độ) và `hum` (độ ẩm) của Bike Sharing đã được co giãn về khoảng 0–1. Vì $r$ không
đổi khi đổi đơn vị, ta dùng thẳng các cột này.

| Cặp | Mọi giờ (17.379 giờ) | Chỉ lúc 17h (730 ngày; 29/10/2012 thiếu giờ 17) |
|---|---|---|
| nhiệt độ × lượt thuê | 0,405 | 0,588 |
| độ ẩm × lượt thuê | −0,323 | −0,253 |
| giờ trong ngày × lượt thuê | 0,394 | — |

**Đọc bảng.**

- Dòng 1, so hai cột: chỉ xét 17h thì $r$ cao hơn. Lẫn mọi giờ, giờ đêm (ít người đi dù trời ấm) che mất quan hệ.
- Dòng 2: độ ẩm tương quan âm, nhưng một phần là do **giờ** (hộp "Mượn trước" dưới đây).
- Dòng 3: giờ trong ngày quyết định lượt thuê rất mạnh mà $r$ vẫn thấp, vì quan hệ cong (hình phải).

**Tương quan không phải nhân quả.** Bán kem và số vụ đuối nước tương quan dương, nhưng kem không gây đuối nước. Cả hai
cùng tăng vì trời nóng. Tuy vậy, một biến không gây ra $y$ **vẫn có thể giúp dự báo** $y$ (sách *Forecasting: Principles and Practice*, viết tắt FPP, §7.8).

> **Mượn trước — biến gây nhiễu** (buổi 8 học kỹ)
>
> - **Biến gây nhiễu** (confounder): biến thứ ba tác động lên cả hai đại lượng, làm chúng trông như liên quan. Trời nóng
>   là biến gây nhiễu của cặp kem × đuối nước.
> - Ở dòng 2 bảng trên, "giờ trong ngày" là biến gây nhiễu của cặp độ ẩm × lượt thuê. Đêm ẩm hơn ngày (độ ẩm trung
>   bình 0,74 lúc 4h, 0,49 lúc 15h) và đêm cũng vắng người.
> - Giữ cố định giờ (chỉ xét 17h) thì tương quan yếu đi: −0,323 → −0,253, vì phần "tương quan" do giờ tạo ra đã bị
>   loại. Với nhiệt độ thì ngược lại, r mạnh lên (0,405 → 0,588). Trộn mọi giờ thì lượt thuê lên xuống chủ yếu
>   theo giờ, phần này làm mờ quan hệ với nhiệt độ. Chỉ xét 17h thì còn lại chênh lệch giữa các ngày: ngày ấm đông hơn. Giữ cố định biến gây nhiễu có thể làm r yếu
>   đi hoặc mạnh lên.

> **Mượn trước — tự tương quan** (buổi 7 học kỹ)
>
> - **Tự tương quan** ở độ trễ $k$: tương quan của một chuỗi với chính nó dời lùi $k$ bước. "Giờ này đông thì giờ kế
>   có hay đông không?"
> - Ví dụ chuỗi 1, 3, 1, 3: trung bình 2, độ lệch −1, 1, −1, 1. Nhân từng cặp liền nhau: (1)(−1) + (−1)(1) + (1)(−1) = −3.
>   Chia tổng bình phương độ lệch của cả chuỗi (1 + 1 + 1 + 1 = 4) được −0,75: lên xuống xen kẽ.
> - Vì sao không ra −1 dù xen kẽ hoàn hảo? Quy ước của tự tương quan chia cho tổng bình phương của **cả** chuỗi (4 số),
>   trong khi tử số chỉ có 3 cặp liền nhau. Mẫu số khác công thức $r$ ở trên, nên với chuỗi ngắn con số nhỏ hơn 1 về độ
>   lớn.
> - Lượt thuê theo giờ có tự tương quan trễ 1 là **0,844**: giờ này đông thì giờ kế gần như chắc cũng đông. Mục 4.6
>   cho thấy điều này làm hỏng bootstrap.

**Tóm lại.** **Hệ số $r$ (từ −1 tới 1) đo hai đại lượng cùng tăng giảm theo đường thẳng tới đâu. Nếu $r$ gần 0, hai đại
lượng vẫn có thể liên quan theo đường cong. Nếu $r$ lớn, vẫn chưa chắc là nhân quả, vì có thể có biến gây nhiễu.**

**Tự kiểm tra.** $x$ = −2, −1, 0, 1, 2 và $y = x^2$ = 4, 1, 0, 1, 4. Tính $r$. Hai đại lượng có liên quan không?

<details>
<summary>Đáp án</summary>

$\bar x = 0$, $\bar y = 2$. Độ lệch $y$: 2, −1, −2, −1, 2. Tích với độ lệch $x$: −4, 1, 0, −1, 4, tổng 0. Vậy **$r = 0$**.
Nhưng $y$ hoàn toàn do $x$ quyết định, theo một đường cong chữ U. Nhầm hay gặp: đọc $r = 0$ thành "không liên quan".

</details>

### 4.5 Kiểm định giả thuyết

**Vấn đề.** Năm 2012, ngày làm việc trung bình có 5.744,6 lượt thuê, ngày nghỉ có 5.288,2. Chênh 456 lượt. Đó là khác
biệt thật, hay chỉ do may mắn của các ngày được chọn?

**Trực giác.** Bạn nghi một đồng xu thiên về mặt ngửa. Tung 10 lần, được 9 ngửa. Bạn tự hỏi: "Nếu đồng xu cân đối, gặp
9 ngửa trở lên có hiếm không?" Nếu rất hiếm, bạn thôi tin đồng xu cân đối. Đó là toàn bộ ý của kiểm định.

**Ví dụ số nhỏ — tự tính tay.** Bốn bước, áp cho đồng xu.

1. **Giả thuyết không $H_0$**: giả định "không có gì đặc biệt" mà ta tìm cách bác bỏ. Ở đây: "đồng xu cân đối".
2. **Đại lượng kiểm định**: con số tóm tắt dữ liệu. Ở đây: số lần ngửa, bằng 9.
3. **p-value**: **nếu $H_0$ đúng**, xác suất gặp kết quả lệch cỡ này **hoặc hơn**. Tung 10 lần có $2^{10}$ = 1.024 dãy
   kết quả, dãy nào cũng cùng khả năng. Có 10 dãy đúng 9 ngửa (chọn lần sấp duy nhất) và 1 dãy 10 ngửa. Vậy p = (10 + 1)/1.024 = 11/1.024
   ≈ 0,011.
4. **So với mức ý nghĩa** $\alpha$, ngưỡng chọn **trước** khi xem dữ liệu, hay dùng 0,05 (5%). p = 0,011 < 0,05 nên
   **bác bỏ $H_0$**: dữ liệu khó xảy ra nếu đồng xu cân đối.

- Câu hỏi "đồng xu lệch về bên nào cũng được" thì đếm cả 9 sấp trở lên, gọi là kiểm định **hai phía**:
  p = 22/1.024 ≈ 0,021.
- Nếu chỉ được 7 ngửa (câu hỏi một phía: "thiên về ngửa?"), đếm các dãy có 7, 8, 9 hoặc 10 ngửa. Số cách chọn $k$ lần
  ngửa trong 10 lần là tổ hợp $C(10, k)$: 120 + 45 + 10 + 1 = 176. Vậy p = 176/1.024 ≈ 0,17, lớn hơn 0,05 → **không bác
  bỏ**.

Ba câu phải nhớ:

- **Không bác bỏ không có nghĩa là chứng minh $H_0$ đúng.** 7 ngửa không chứng minh đồng xu cân đối. Có thể chỉ là
  tung quá ít lần.
- **p-value không phải xác suất $H_0$ đúng.** p = 0,011 không có nghĩa "đồng xu cân đối với xác suất 1,1%". Nó là xác
  suất của dữ liệu **khi giả sử** $H_0$ đúng (Hội Thống kê Hoa Kỳ, 2016).
- **Có ý nghĩa thống kê không có nghĩa là khác biệt lớn.** Với rất nhiều dữ liệu, một chênh nhỏ xíu cũng cho p nhỏ.

**Kiểm định hoán vị** (permutation test) áp cùng bốn bước cho câu hỏi "hai nhóm có khác nhau không". Ví dụ 6 ngày, lượt
thuê (nghìn lượt): ngày làm việc 5, 7, 6; ngày nghỉ 3, 2, 4.

1. Chênh trung bình thật: (5 + 7 + 6)/3 − (3 + 2 + 4)/3 = 6 − 3 = **3**.
2. $H_0$: nhãn "làm việc/nghỉ" không liên quan tới lượt thuê. Nếu vậy, gán nhãn kiểu nào cũng như nhau.
3. Số cách chọn 3 trong 6 ngày làm nhóm "làm việc" là $C(6, 3) = (6 × 5 × 4)/(3 × 2 × 1) = 20$. Tổng 6 số là 27. Nếu
   nhóm "làm việc" có tổng $A$ thì chênh = $A/3 − (27 − A)/3$. Chênh ≥ 3 cần $A$ ≥ 18, chỉ có 7 + 6 + 5. Chênh ≤ −3 cần
   $A$ ≤ 9, chỉ có 2 + 3 + 4. Vậy 2 trong 20 cách lệch cỡ 3 hoặc hơn **về cả hai phía** (câu hỏi "khác nhau",
   không nói phía nào). Nếu hỏi một phía ("làm việc cao hơn") thì chỉ tính cách đầu: p = 1/20 = 0,05, vẫn không nhỏ hơn 0,05.
4. p = 2/20 = 0,10, lớn hơn 0,05: **không bác bỏ**. Dù ba ngày làm việc đều cao hơn ba ngày nghỉ, 6 ngày là quá ít để kết luận.

Với nhiều ngày thì không liệt kê hết các cách được. Máy **xáo nhãn ngẫu nhiên** $B$ lần và đếm.

**Công thức.**

$$
p = \frac{k + 1}{B + 1}
$$

- $B$: số lần xáo nhãn. $k$: số lần xáo cho chênh lệch (bỏ dấu) lớn bằng hoặc hơn chênh lệch thật.
- Cộng 1 ở tử và mẫu là tính cả cách gán nhãn thật, nên p không bao giờ bằng 0.

**Nói bằng lời.** p là tỷ lệ số lần "gán nhãn bừa" mà vẫn ra chênh lệch cỡ thật hoặc hơn. Với ngày làm việc 2012: xáo
9.999 lần, có 253 lần lệch bằng hoặc hơn 456, nên p = (253 + 1)/(9.999 + 1) ≈ 0,025.

**Tự viết bằng NumPy.**

```python
def hoan_vi(y, nhom, so_lan=9999, seed=2026):
    y, nhom = np.asarray(y, dtype=float), np.asarray(nhom, dtype=bool)
    that = y[nhom].mean() - y[~nhom].mean()          # chênh lệch thật
    rng = np.random.default_rng(seed)
    k = 0
    for _ in range(so_lan):
        xao = rng.permutation(nhom)                   # xáo nhãn True/False, giữ nguyên các con số
        k += abs(y[xao].mean() - y[~xao].mean()) >= abs(that)   # hai phía: lệch về bên nào cũng tính
    return that, (k + 1) / (so_lan + 1)
```

Trong code, `nhom` là mảng True/False (True = ngày làm việc); `y[nhom]` lấy các ngày True, còn `~nhom` đảo True
thành False và ngược lại, tức "nhóm còn lại". Dòng `k += (… >= …)` cộng một giá trị True/False vào số nguyên: Python
coi True là 1, False là 0, nên `k` đếm số lần điều kiện đúng.

**Thư viện.** `scipy.stats.permutation_test` cho p = 0,023 trên cùng dữ liệu (seed 2026); lệch nhẹ vì dãy ngẫu nhiên
khác, và vì scipy tính hai phía bằng cách nhân đôi p một phía nhỏ hơn thay vì đếm trị tuyệt đối.

**Dữ liệu thật.** Lượt thuê theo ngày năm 2012, 9.999 lần xáo, seed 2026:

| So sánh | Số ngày mỗi nhóm | Chênh trung bình (lượt/ngày) | p-value | Ở mức 5% |
|---|---|---|---|---|
| ngày làm việc − ngày nghỉ | 250 và 116 | +456 | 0,025 | bác bỏ $H_0$ |
| thứ Bảy − Chủ nhật | 52 và 53 | +695 | 0,078 | không bác bỏ |

**Đọc bảng.** So cột "chênh" với cột "p-value". Dòng 2 chênh **lớn hơn** mà p lại **lớn hơn**. Lý do là dòng 2 chỉ có
khoảng 50 ngày mỗi nhóm, nên trung bình của nó dao động mạnh hơn. Dòng 2 "không bác bỏ" không có nghĩa thứ Bảy và Chủ
nhật như nhau. Nó chỉ nói dữ liệu này chưa đủ để chắc.

![Phân phối chênh lệch khi xáo nhãn](hinh/hoan-vi.png)

**Cách đọc hình.**

1. **Trục ngang**: chênh lệch trung bình lượt thuê mỗi ngày giữa hai nhóm khi nhãn bị xáo ngẫu nhiên (lượt).
2. **Trục dọc**: số lần xáo (trên tổng 9.999) rơi vào mỗi khoảng.
3. **Ký hiệu**: ô trái là ngày làm việc − ngày nghỉ (dòng 1 của bảng), ô phải là thứ Bảy − Chủ nhật (dòng 2). Cột xanh
   là các chênh lệch "nếu $H_0$ đúng"; vạch cam liền là chênh thật; vạch cam đứt là mức đối xứng bên âm.
4. **Nhìn vào đâu**: phần cột nằm ngoài hai vạch cam. Ô trái chỉ còn một mẩu nhỏ, ô phải còn nhiều hơn hẳn.
5. **Kết luận**: chênh 456 lượt hiếm khi xảy ra do xáo ngẫu nhiên (p ≈ 0,025); chênh 695 lượt với ít ngày thì không
   hiếm (p ≈ 0,08).

**Một cảnh báo.** Xáo nhãn giả định các ngày **độc lập**, nhưng ngày đông hay đi liền ngày đông (tự tương quan trễ 1
là 0,748). Khi đó p-value tính như trên thường **nhỏ hơn** thật, cùng lý do với bootstrap ở mục 4.6.

Mọi kiểm định ở các buổi sau (buổi 7, 15…) đọc đúng theo khuôn này: một $H_0$, một p-value, so với 0,05. Mỗi kiểm
định có $H_0$ riêng; luôn đọc $H_0$ là gì trước khi đọc p.

**Tóm lại.** **Kiểm định hỏi: nếu "không có gì đặc biệt" ($H_0$) thì dữ liệu như vậy hiếm cỡ nào? p-value nhỏ hơn mức
ý nghĩa (thường 0,05) thì bác bỏ $H_0$. Không bác bỏ không phải là chứng minh; p-value không phải xác suất $H_0$ đúng.**

**Tự kiểm tra.** Một báo cáo viết: "Mô hình A và B có p = 0,30, vậy hai mô hình tốt như nhau." Câu này sai ở đâu?

<details>
<summary>Đáp án</summary>

p = 0,30 > 0,05 chỉ cho phép nói **không bác bỏ** "hai mô hình như nhau". Đó không phải chứng minh chúng như nhau;
có thể dữ liệu quá ít để thấy khác biệt. Nhầm hay gặp là đọc "không bác bỏ" thành "đã chứng minh $H_0$".

</details>

### 4.6 Bootstrap và block bootstrap

**Vấn đề.** Trung bình lượt thuê theo giờ năm 2012 là 234,7. Nếu lấy một năm khác "giống hệt", con số này sẽ dao động
bao nhiêu? Đó là câu hỏi của **khoảng tin cậy** cho trung bình (mục 4.3).

**Trực giác: i.i.d., luật số lớn, CLT.**

- **i.i.d.** (độc lập và cùng phân phối): mỗi quan sát rút từ cùng một phân phối, và biết quan sát này không giúp đoán
  quan sát kia. Tung xúc xắc là i.i.d. Lượt thuê giờ liền nhau thì **không** độc lập.
- **Luật số lớn**: với dữ liệu i.i.d., trung bình mẫu càng lúc càng gần trung bình thật khi $n$ tăng.
- **Định lý giới hạn trung tâm (CLT)**: với dữ liệu i.i.d. có độ dao động hữu hạn (phương sai không vô cùng lớn, dữ
  liệu thực tế gần như luôn thoả), trung bình mẫu có phân phối gần hình chuông. Độ lệch chuẩn của nó là $\sigma/\sqrt{n}$. Ở đây $\sigma$ là độ lệch
  chuẩn của **một lần đo** trong tổng thể (con số thật, chưa biết); thực tế ta thay nó bằng $s$ tính từ mẫu.
- **Vì sao $\sqrt n$?** Cộng nhiều số độc lập, phần lệch lên và lệch xuống bù trừ nhau, nhưng không hết. Ví dụ 4 đồng
  xu, mỗi đồng cho +1 hoặc −1 (độ lệch chuẩn 1). Tổng 4 đồng có 16 khả năng như nhau: +4 (1 cách), +2 (4), 0 (6), −2 (4),
  −4 (1). Phương sai của tổng: (16 × 1 + 4 × 4 + 6 × 0 + 4 × 4 + 16 × 1)/16 = 64/16 = 4,
  nên độ lệch chuẩn của tổng là √4 = 2, không phải 4. Quy tắc đứng sau: với các số **độc lập**, phương sai của tổng
  bằng tổng các phương sai (4 đồng, mỗi đồng phương sai 1, tổng phương sai 4). Tổng quát: $n$ số, mỗi số phương sai
  $\sigma^2$, tổng có phương sai $n\sigma^2$, tức độ lệch chuẩn $\sigma\sqrt n$;
  trung bình là tổng chia $n$, nên lệch cỡ $\sigma\sqrt n / n = \sigma/\sqrt n$.

**Ví dụ số nhỏ — kiểm $1/\sqrt n$ bằng máy** (một **mô phỏng**: dùng máy rút ngẫu nhiên thật nhiều lần theo quy tắc biết
trước, để thấy điều lý thuyết nói). Coi cả 17.379 giờ là tổng thể: trung bình thật 189,5, $\sigma$ = 181,4 (chia $n$, vì
đây là tổng thể). Rút ngẫu nhiên **có hoàn lại** $n$ giờ, tính trung bình, lặp 20.000 lần (seed 5):

| Cỡ mẫu n | Độ lệch chuẩn của 20.000 trung bình | σ/√n |
|---|---|---|
| 25 | 36,1 | 181,4/5 = 36,3 |
| 100 | 18,2 | 181,4/10 = 18,1 |
| 400 | 9,1 | 181,4/20 = 9,1 |

**Đọc bảng.** Cột 2 khớp cột 3: dữ liệu lệch phải nhưng trung bình mẫu vẫn dao động đúng $\sigma/\sqrt n$. Tăng $n$ gấp 4
thì độ dao động chỉ giảm một nửa. Ở cả ba dòng, khoảng 95% trong 20.000 trung bình rơi vào 189,5 ± 1,96 σ/√n, đúng như
hình chuông. **Độ rộng tỷ lệ với $1/\sqrt n$.**

Vì không biết $\sigma$ của tổng thể, ta thay bằng $s$ của mẫu: khoảng là trung bình mẫu ± 1,96 × $s/\sqrt n$. Chạy thật
(seed 12): coi 8.734 giờ năm 2012 là tổng thể, trung bình thật 234,7 lượt. Rút 20 mẫu, mỗi mẫu 100 giờ, mỗi mẫu dựng một
khoảng như vậy. 19 khoảng chứa 234,7; khoảng thứ 20 là [148,1; 231,8], không chứa. Đó là "95% là của quy trình" (mục
4.3): người chỉ có mẫu thứ 20 không biết mình trượt.

**Nhưng dữ liệu tự tương quan chứa ít thông tin hơn.** Nếu giờ này đông thì giờ kế gần như chắc cũng đông, thì giờ kế
chỉ mang thêm một phần thông tin mới. Các điểm lệch cùng chiều theo từng đám, nên ít bù trừ nhau hơn. Mô hình đơn giản nhất cho chuỗi tự tương quan là **AR(1)**:

$$
x_t = \rho\, x_{t-1} + \varepsilon_t
$$

- $x_t$: giá trị ở bước $t$. $x_{t-1}$: giá trị bước trước. $\rho$ (rho): hệ số, từ −1 tới 1, bằng tự tương quan trễ 1.
- $\varepsilon_t$ (epsilon): phần ngẫu nhiên mới ở bước $t$, i.i.d., trung bình 0.

**Nói bằng lời.** Giá trị mới bằng $\rho$ lần giá trị cũ cộng một cú hích ngẫu nhiên. $\rho$ = 0,7, bước trước 10, cú
hích 0,5: bước này 0,7 × 10 + 0,5 = 7,5. Giá trị cao kéo theo giá trị kế cũng cao.

Với AR(1), $n$ quan sát chỉ đáng giá như $n_{\text{eff}}$ quan sát độc lập (**cỡ mẫu hiệu dụng**):

$$
n_{\text{eff}} \approx n\,\frac{1-\rho}{1+\rho}, \qquad \frac{\text{độ rộng đúng}}{\text{độ rộng tính như i.i.d.}} \approx \sqrt{\frac{n}{n_{\text{eff}}}}
$$

- $n$: số quan sát. $\rho$: tự tương quan trễ 1. Phân số $(1-\rho)/(1+\rho)$ là phần thông tin "mới" mỗi điểm mang
  theo: $\rho$ = 0 cho 1 (độc lập hoàn toàn), $\rho$ càng gần 1 càng gần 0. Ví dụ $\rho$ = 0,5: phân số là 1/3, tức cứ
  khoảng 3 điểm liền nhau chỉ đáng như 1 điểm độc lập. Công thức chứng minh cho AR(1), nằm ngoài buổi
  này; bảng dưới kiểm nó bằng số thật.
- Vế phải: độ rộng đúng tỷ lệ $1/\sqrt{n_{\text{eff}}}$, độ rộng tính như i.i.d. tỷ lệ $1/\sqrt n$. Chia hai số cho nhau:
  $\dfrac{1/\sqrt{n_{\text{eff}}}}{1/\sqrt n} = \sqrt{n/n_{\text{eff}}}$.

**Nói bằng lời.** $\rho$ = 0,7 và $n$ = 200: $n_{\text{eff}}$ ≈ 200 × 0,3/1,7 ≈ 35. Khoảng tin cậy đúng phải rộng
khoảng $\sqrt{200/35} \approx 2{,}4$ lần khoảng tính như 200 quan sát độc lập.

**Bootstrap** (Efron 1979) ước lượng độ dao động mà không cần công thức. Lấy mẫu lại **có hoàn lại** (một số được rút
nhiều lần) từ chính dữ liệu, cùng cỡ, tính trung bình, lặp vài nghìn lần. Quantile 0,025 và 0,975 của các trung bình đó
là khoảng tin cậy 95% kiểu **percentile** (percentile là quantile viết theo phần trăm: quantile 0,025 = percentile 2,5).

**Vì sao cách này đúng?** Ta muốn biết: rút một mẫu mới từ tổng thể thì trung bình dao động bao nhiêu. Nhưng ta không có
tổng thể, chỉ có một mẫu. Nếu mẫu được rút ngẫu nhiên, nó là **bức ảnh thu nhỏ** của tổng thể: giá trị nào hay gặp trong
tổng thể thì cũng hay gặp trong mẫu. Rút có hoàn lại từ bức ảnh thu nhỏ vì thế gần giống rút từ tổng thể. "Có hoàn lại"
để mỗi lần rút vẫn thấy cả bức ảnh, như tổng thể không bị vơi đi.

Kiểm bằng máy (seed 11): coi 8.734 giờ năm 2012 là tổng thể và rút **một** mẫu 100 giờ.

| Cách | Độ lệch chuẩn của 5.000 trung bình |
|---|---|
| rút 5.000 mẫu mới từ tổng thể (điều ta không làm được ngoài đời) | 21,2 |
| bootstrap: rút 5.000 lần có hoàn lại từ chính mẫu 100 giờ | 21,0 |

**Đọc bảng.** Hai số gần bằng nhau: chỉ từ một mẫu, bootstrap đoán đúng độ dao động. Điều kiện là mẫu phải
giống tổng thể **cả về cách các điểm đi cùng nhau**. Với chuỗi tự tương quan, rút từng điểm riêng lẻ làm mất điều đó.

**Ví dụ số nhỏ — tự tính tay.** 5 ngày liền nhau $x$ = 12, 15, 11, 30, 14 (đánh số 0–4), trung bình 16,4. Ba lần lấy
chỉ số ngẫu nhiên (`np.random.default_rng(3).integers(0, 5, size=(3, 5))`):

| Lần | Chỉ số | Mẫu lại | Trung bình |
|---|---|---|---|
| 1 | 4, 0, 0, 1, 0 | 14, 12, 12, 15, 12 | 13,0 |
| 2 | 4, 4, 2, 0, 0 | 14, 14, 11, 12, 12 | 12,6 |
| 3 | 1, 2, 3, 2, 1 | 15, 11, 30, 11, 15 | 16,4 |

**Đọc bảng.** Lần 1 và 2 không rút trúng số 30, nên trung bình thấp hẳn. Với mẫu nhỏ, một giá trị bất thường như 30 quyết
định phần lớn độ rộng khoảng. Mỗi số được rút riêng lẻ, nên thứ tự ngày bị xáo trộn.

**Block bootstrap** (Künsch 1989) rút cả **khối** $l$ ngày liền nhau. Ví dụ khối dài 2 (seed 2):

- Rút 3 điểm bắt đầu (chỉ số 3, 1 và 0) → ba khối (30, 14), (15, 11), (12, 15).
- Nối lại, cắt còn 5 số: 30, 14, 15, 11, 12 → trung bình (30 + 14 + 15 + 11 + 12)/5 = 16,4.
- Ngày 30 và ngày 14 kế tiếp nó đi cùng nhau, nên phụ thuộc giữa hai ngày liền nhau được giữ.

**Tự viết bằng NumPy** — viết bằng vòng lặp cho dễ đọc; `l = 1` là bản i.i.d.:

```python
def chi_so_khoi(n, l, rng):
    """Một lần lấy mẫu lại: danh sách n chỉ số, ghép từ các khối l chỉ số liền nhau."""
    chi_so = []
    while len(chi_so) < n:
        b = int(rng.integers(0, n - l + 1))   # điểm bắt đầu khối, sao cho khối không vượt quá cuối chuỗi
        chi_so.extend(range(b, b + l))       # thêm b, b+1, …, b+l−1
    return chi_so[:n]                        # khối cuối có thể thừa, cắt cho đủ n

rng = np.random.default_rng(2)
chi_so_khoi(5, 2, rng)                       # [3, 4, 1, 2, 0] — đúng ví dụ tay ở trên

tb = [x[chi_so_khoi(len(x), l, rng)].mean() for _ in range(1999)]   # 1999 trung bình mẫu lại
lo, hi = np.quantile(tb, [0.025, 0.975])                             # khoảng tin cậy 95% percentile
```

Hàm `_chi_so_bootstrap` trong `code/` làm đúng việc này nhưng tính mọi lần lấy mẫu cùng lúc bằng mảng NumPy, nhanh hơn
nhiều. Hai cách cho cùng ý; dãy số ngẫu nhiên có thể khác nhau.

**Thư viện.** `scipy.stats.bootstrap((x,), np.mean, method="percentile", rng=…)` chỉ làm bản i.i.d.; scipy không có
block bootstrap. Thử trên một chuỗi AR(1) mô phỏng ($\rho$ = 0,7, $n$ = 200, seed 7, 9.999 lần lấy mẫu lại):

| Cách | Khoảng tin cậy 95% cho trung bình |
|---|---|
| tự viết, i.i.d. | [−0,634; −0,303] |
| scipy, i.i.d. | [−0,634; −0,303] |
| tự viết, khối 6 | [−0,810; −0,201] |

**Đọc bảng.** Hai dòng đầu trùng nhau: phần lấy mẫu lại viết đúng. Dòng 3 rộng gần gấp đôi, do **cách lấy mẫu**. Trung
bình thật của chuỗi mô phỏng là 0, nhưng trung bình của mẫu này là −0,467, nên cả ba khoảng đều **không** chứa 0. Một
khoảng 95% đơn lẻ vẫn có thể trượt; điều cần đo là **tỷ lệ trượt qua rất nhiều lần**, như hình dưới.

Khối 6 theo quy tắc kinh nghiệm: độ dài khối ≈ căn bậc ba của $n$ (200 → 5,85 → 6), chỉ là điểm xuất phát.

![Bootstrap i.i.d. quá hẹp; độ dài khối là quyết định nhạy](hinh/bootstrap-do-dai-khoi.png)

**Cách đọc hình.**

1. **Trục ngang**: độ dài khối (1 là i.i.d.), chia theo thang nhân (mỗi vạch gấp vài lần vạch trước) chứ không đều;
   ô phải tính bằng giờ.
2. **Trục dọc**: ô trái là tỷ lệ khoảng 95% chứa trung bình thật; ô phải là độ rộng khoảng chia cho độ rộng bản i.i.d.
3. **Ký hiệu**: ô trái, mỗi chấm là 300 chuỗi AR(1) mô phỏng ($\rho$ = 0,7, $n$ = 200); đường cam đứt là 95%.
4. **Nhìn vào đâu**: ô trái, chấm đầu (i.i.d.) ở 60%; đỉnh ở khối 10–20 cũng chỉ 89%. Ô phải, đường đi lên mãi.
5. **Kết luận**: bootstrap i.i.d. cho khoảng quá hẹp khi dữ liệu tự tương quan; độ dài khối là quyết định nhạy.

Số của ô trái (seed 2026, 300 chuỗi, mỗi chuỗi 999 lần lấy mẫu lại):

| Độ dài khối | 1 | 3 | 6 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|
| Tỷ lệ chứa trung bình thật | 60,3% | 78,7% | 86,3% | 89,0% | 89,3% | 81,3% |

**Đọc bảng.** Tỷ lệ tăng từ khối 1 tới khối 20 rồi **tụt** ở khối 40.

- Khối ngắn: mỗi chỗ nối hai khối là một chỗ phụ thuộc bị cắt đứt. Khối càng ngắn càng nhiều chỗ nối, khoảng càng hẹp.
- Khối dài: đo được là khoảng **hẹp lại**; lý do đầy đủ cần toán ngoài buổi này. Một phần dễ thấy: hai đầu chuỗi bị
  rút ít (điểm đầu chuỗi nằm trong 1 khối, điểm giữa nằm trong 40 khối). Cần nhớ: khối quá dài cũng hỏng, nên luôn thử
  vài độ dài và báo độ nhạy.
- Với $n$ = 200 không độ dài nào tránh được cả hai cùng lúc, nên không đạt 95%. Chuỗi dài hơn thì đỡ: cùng
  $\rho$ = 0,7 nhưng $n$ = 2.000, khối 13 cho 94,0%.

Ô phải (lượt thuê theo giờ 2012): khoảng rộng mãi theo độ dài khối, không chững lại. Lý do chính: chuỗi có xu hướng tăng
cả năm. Mỗi khối mang theo mức của đoạn nó được cắt ra: khối tháng 1 thấp, khối tháng 9 cao. Khối càng dài, trung
bình mẫu lại càng đổi theo việc rút trúng mùa nào, nên khoảng cứ rộng thêm.

**Tóm lại.** **Với dữ liệu i.i.d., độ rộng khoảng tin cậy của trung bình tỷ lệ $1/\sqrt n$. Dữ liệu tự tương quan chỉ
đáng giá $n_{\text{eff}} < n$ quan sát, nên bootstrap từng điểm cho khoảng quá hẹp. Block bootstrap giữ phụ thuộc bên
trong khối và sửa phần lớn, nhưng kết quả nhạy với độ dài khối.**

**Tự kiểm tra.** Chuỗi 1.000 giờ, tự tương quan trễ 1 là 0,8. $n_{\text{eff}}$ bằng bao nhiêu? Khoảng tin cậy tính như
i.i.d. hẹp đi mấy lần so với đúng?

<details>
<summary>Đáp án</summary>

$n_{\text{eff}}$ ≈ 1.000 × 0,2/1,8 ≈ **111**. Tỷ lệ độ rộng là $\sqrt{1.000/111} = \sqrt{9} = 3$: khoảng i.i.d. hẹp đi
khoảng 3 lần. Nhầm hay gặp là quên căn bậc hai, nói "hẹp 9 lần".

</details>

## 5. Lab từng bước

### Bước 1 — Dựng nền và chạy code có sẵn

**Mục đích:** dựng môi trường, thấy hai triệu chứng của `code/` bằng số.

```bash
cd lab && make up
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/xac_suat.py
make check
```

`make up` dựng môi trường Python của buổi và tải dữ liệu. Dòng `uv run` chạy file bằng đúng môi trường đó (thư mục
`00-nen`): `env -u VIRTUAL_ENV` bỏ qua môi trường Python bạn đang bật (nếu có), `--no-sync` bảo uv không cài lại gì. `make check` chạy bộ chấm (các test trong `lab/cham/`).

**Đọc kết quả:** code in tỷ lệ dạng thập phân (`0.7251` = 72,51%). Khoảng theo giờ từ 2011 phủ `0.7251` năm 2012, gần
như toàn bộ phần trượt ở đuôi trên (`0.2742`). Bootstrap trên AR(1) phủ `0.6033`. `make check` báo 5 test hỏng.

### Bước 2 — Tương quan và kiểm định hoán vị trên dữ liệu thật

**Mục đích:** tự tính lại các con số của mục 4.4 và 4.5 trên dữ liệu thật.

Các bước 2–5 chạy trong một notebook mở bằng `make notebook`, đặt trong thư mục `code/` (để `from xac_suat import …`
tìm thấy file). Dán hàm `hoan_vi` ở mục 4.5 vào một ô trước.

```python
import numpy as np, pandas as pd, tv                     # tv: thư viện trợ giúp của khoá, biết chỗ để dữ liệu
from xac_suat import doc_luot_thue

h = doc_luot_thue()
print(np.corrcoef(h["temp"], h["cnt"])[0, 1])            # nhiệt độ × lượt thuê, mọi giờ
d = pd.read_csv(tv.THU_MUC_DU_LIEU / "uci-bike-sharing" / "day.csv")
n12 = d[d["yr"] == 1]                                    # yr = 1 là năm 2012
print(hoan_vi(n12["cnt"], n12["workingday"] == 1))       # chép hàm hoan_vi từ mục 4.5
```

**Đọc kết quả:** $r$ khớp bảng mục 4.4, p khớp bảng mục 4.5. Đổi sang thứ Bảy − Chủ nhật (`weekday` 6 và 0) phải ra
đúng dòng 2 của bảng đó. Nếu p ra 0 thì bạn quên cộng 1 ở tử và mẫu.

### Bước 3 — Quantile và bootstrap tự viết

**Mục đích:** kiểm bootstrap tự viết khớp scipy (bảng "Thư viện" mục 4.6) trước khi sửa code.

```python
from scipy import stats
from xac_suat import ar1, khoang_tin_cay_trung_binh

x = ar1(200, 0.7, np.random.default_rng(7))
print(khoang_tin_cay_trung_binh(x, so_lan=9999, do_dai_khoi=1, seed=7))   # tự viết, i.i.d.
kq = stats.bootstrap((x,), np.mean, n_resamples=9999, method="percentile", rng=np.random.default_rng(7))
print(kq.confidence_interval)                                               # scipy, i.i.d.
print(khoang_tin_cay_trung_binh(x, so_lan=9999, do_dai_khoi=6, seed=7))   # tự viết, khối 6
```

**Đọc kết quả:** ba dòng khớp bảng đó; hai dòng i.i.d. trùng nhau vì cùng seed. Lệch thì kiểm lại seed và `so_lan`.

### Bước 4 — Đo tỷ lệ phủ thật, sửa `khoang_du_bao`

**Mục đích:** sửa bệnh "sai hình dạng" và thấy nó không sửa được bệnh "dịch mức".

Đo tỷ lệ phủ như mục 4.3:

```python
from xac_suat import doc_luot_thue, khoang_theo_gio, ty_le_phu

h = doc_luot_thue()
nam_2011, nam_2012 = h[h["yr"] == 0], h[h["yr"] == 1]
k = khoang_theo_gio(nam_2011)                     # một khoảng cho mỗi giờ 0–23
for ten, moi in [("2011 → 2011", nam_2011), ("2011 → 2012", nam_2012)]:
    m = moi.merge(k, on="hr")                     # gắn khoảng của đúng giờ đó vào từng dòng
    print(ten, ty_le_phu(m["cnt"], m["lo"], m["hi"]))
```

Rồi đổi `khoang_du_bao` sang khoảng quantile thực nghiệm: mức 0,025 và 0,975, dùng `quantile_tu_viet`. Khởi động lại
notebook (để nạp lại `xac_suat.py`) và chạy lại.

**Đọc kết quả:** dòng "2011 → 2011" phải cân hai đuôi như bảng mục 4.3; dòng "2011 → 2012" vẫn khoảng 70%. Viết hai câu
giải thích vì sao. Cận dưới còn âm thì bạn chưa thay hết công thức ±1,96s.

### Bước 5 — Sửa `khoang_tin_cay_trung_binh`

**Mục đích:** đổi bootstrap mặc định sang block bootstrap và thấy tỷ lệ phủ tăng.

Mặc định phải lấy mẫu theo khối. Độ dài khối mặc định là $\max(2, \operatorname{round}(n^{1/3}))$: căn bậc ba của $n$,
làm tròn, ít nhất là 2. Chạy lại mô phỏng với từng độ dài khối:

```python
from xac_suat import ty_le_phu_khoang_tin_cay

for khoi in (1, 3, 6, 10, 20, 40):   # rho=0.7, n=200, 300 chuỗi, seed 2026 (mặc định của hàm)
    print(khoi, ty_le_phu_khoang_tin_cay(do_dai_khoi=khoi))
```

```bash
make check     # phải xanh 8/8
```

**Đọc kết quả:** tỷ lệ phủ khớp bảng độ dài khối ở mục 4.6; `make check` xanh 8/8. Test
`test_khoang_tin_cay_van_dung_voi_iid` đỏ nghĩa là khoảng quá hẹp ngay cả với dữ liệu độc lập: kiểm lại mức quantile.

## 6. Lỗi thường gặp & cách chẩn đoán

| Triệu chứng | Nguyên nhân | Chẩn đoán | Sửa |
|---|---|---|---|
| Cận dưới âm cho dữ liệu không âm | ±1,96s trên dữ liệu lệch phải | so cận dưới với 0; đếm từng đuôi | quantile thực nghiệm |
| "Khoảng 95% phủ 96%" nhưng một đuôi gần 0% | chỉ đếm tỷ lệ phủ tổng | báo cả hai đuôi | `ty_le_phu` trả dưới/trên |
| Khoảng phủ tốt trong mẫu, vỡ ở năm sau | tương lai dịch mức | chấm trên dữ liệu sau mốc dựng khoảng | lịch sử gần hơn; mô hình mức/xu hướng |
| Khoảng tin cậy hẹp bất thường trên chuỗi thời gian | bootstrap i.i.d. bỏ qua tự tương quan | tự tương quan trễ 1; so với block bootstrap | block bootstrap; kiểm độ nhạy theo độ dài khối |
| "$r$ gần 0 nên hai biến không liên quan" | $r$ chỉ đo quan hệ thẳng | vẽ biểu đồ chấm | nhìn hình trước khi tin $r$ |
| "Tương quan cao nên X gây ra Y" | biến gây nhiễu | tính $r$ trong từng nhóm (vd. từng giờ) | nói "đi cùng", không nói "gây ra" |
| "p = 0,30 nên hai nhóm như nhau" | nhầm "không bác bỏ" với "chứng minh" | xem cỡ mẫu, độ lớn chênh lệch | báo chênh lệch kèm khoảng, không chỉ p |
| "Khoảng tin cậy 95% này có 95% khả năng chứa giá trị thật" | hiểu sai khoảng tin cậy | — | 95% là tần suất của **quy trình** khi lặp lại (mục 4.3) |

## 7. Bài tập về nhà

1. **Dữ liệu ngày.** Với `day.csv` năm 2012 (366 ngày), tính khoảng tin cậy trung bình lượt thuê ngày bằng i.i.d. và block
   bootstrap khối 7, 14, 30. Lập bảng độ rộng; viết con số bạn sẽ báo cho quản lý, kèm cảnh báo.
2. **Kiểm định trời mưa.** Cột `weathersit` ≥ 3 là ngày mưa/tuyết. Dùng kiểm định hoán vị so lượt thuê ngày mưa với ngày
   còn lại năm 2012. Kết luận theo bốn bước của mục 4.5, thêm một câu về tự tương quan.

## 8. Tiêu chí "Xong khi"

- [ ] `make check` xanh 8/8.
- [ ] Tính tay được quantile, trung vị, trung bình, độ lệch chuẩn và $r$ trên 5–10 số.
- [ ] Giải thích bằng số vì sao khoảng ±1,96s dựng từ 2011 chỉ phủ khoảng 73% năm 2012.
- [ ] Đọc đúng một p-value: nói được $H_0$, so với 0,05, không nói "chứng minh" khi không bác bỏ.
- [ ] Giải thích vì sao bootstrap i.i.d. chỉ phủ khoảng 60% trên AR(1) $\rho$ = 0,7, và block bootstrap sửa tới đâu.

## 9. Đọc thêm

- *Forecasting: Principles and Practice*, bản Python (Hyndman, Athanasopoulos et al.): §5.5 khoảng dự báo (hệ số 1,28 /
  1,64 / 2,58 thay cho 1,96 khi muốn khoảng 80% / 90% / 99%); §7.8 tương quan và nhân quả. https://otexts.com/fpppy/
- OpenIntro Statistics (miễn phí), chương 2 và 5: kiểm định bằng xáo ngẫu nhiên. https://www.openintro.org/book/os/
- Seeing Theory: mô phỏng tương tác phân phối và định lý giới hạn trung tâm. https://seeing-theory.brown.edu/
- Greenland et al. (2016): các cách hiểu sai p-value; Efron (1979), Künsch (1989): bootstrap và block bootstrap.
