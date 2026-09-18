# Buổi 8 — Tương quan giữa các chuỗi

## 1. Mục tiêu

Sau buổi này bạn:

- Phát hiện **tương quan giả** giữa hai chuỗi có xu hướng bằng ba bằng chứng: tương quan sau sai phân, $R^2$ và Durbin–Watson.
- Thấy quan hệ **phi tuyến** mà Pearson bỏ sót: scatter, **mutual information**, và tách **CDD/HDD**.
- Đo **độ trễ dẫn dắt** bằng CCF **sau prewhitening**, và biết vì sao CCF thô nói sai.
- Đo **tương quan trượt** để thấy quan hệ đổi dấu theo mùa.
- Chạy **Granger hai chiều** và diễn giải đúng: "quá khứ X giúp dự báo Y", không phải "X gây ra Y".
- Trả lời được câu cuối: biến này có **dùng được để dự báo** không — ta có biết trước giá trị tương lai của nó không?

## 2. Nhắc lại buổi trước

- **Tính dừng**: hai chuỗi không dừng đem tương quan với nhau thì hệ số phản ánh xu hướng chung, không phản ánh quan hệ. Kiểm bằng ADF + KPSS trước
  khi tin bất kỳ hệ số nào.
- **Sai phân** biến mức thành thay đổi; **ACF** giảm chậm là dấu hiệu chưa dừng.
- **Prewhitening** dùng chính ý tưởng đó: lọc phần "tự nó đoán được nó" ra khỏi chuỗi giải thích trước khi so với chuỗi mục tiêu.
- **Đa kiểm định**: nhìn nhiều độ trễ thì kiểu gì cũng có cái vượt dải — nhớ điều này khi đọc CCF.

## 3. Trạng thái đầu buổi

Sau `cd lab && make up`:

| Hạng mục | Trạng thái |
|---|---|
| Dữ liệu | EIA-930 2024 H1 + H2 (sha256 `26768c495c3b`, `a602a8e577cf`) — ERCO 8.784 giờ; Open-Meteo ERA5 Dallas (`0a3b3942535b`) và Houston (`f583a8be1de7`), mỗi tệp 8.784 giờ; CPI-U (`47507ab13d93`); dân số BEA (`dd14f325cc4b`) |
| Nguồn | U.S. EIA, U.S. BLS, U.S. BEA (public domain); Open-Meteo (CC BY 4.0 — "Weather data by Open-Meteo.com") |
| Môi trường | Python 3.12; numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, scikit-learn 1.9.1 |
| `code/tuong_quan.py` | `doc_tai_dien`, `doc_nhiet_do`, `ghep_tai_nhiet`, `doc_kinh_te`, `cdd_hdd`, `tuong_quan`, `thong_tin_tuong_ho`, `kiem_y_nghia_mi`, `hoi_quy_don`, `tuong_quan_chuoi`, `ccf_tu_viet`, `loc_prewhiten`, `do_tre_dan_dat`, `tuong_quan_truot`, `granger_hai_chieu` |
| **Đang cố tình sai** | `tuong_quan_chuoi` chỉ tính trên **mức**; `do_tre_dan_dat` dùng **CCF thô**; `granger_hai_chieu` kết luận "x gây ra y" |
| **Triệu chứng** | CPI và dân số "quan hệ mạnh" (r = 0,974); độ trễ dẫn dắt ra 1 giờ; và "tải điện gây ra nhiệt độ" |
| `make check` lúc này | ĐỎ: 3/10 test hỏng |

## 4. Lý thuyết

Buổi này đi qua **năm tình huống**, mỗi tình huống một cách bị lừa và một cách chữa. Bảng dưới là tóm tắt kết quả chạy thật để đối chiếu khi làm lab:

| # | Tình huống | Bị lừa ở đâu | Bằng chứng đúng | Con số của buổi |
|---|---|---|---|---|
| 1 | Hai chuỗi cùng xu hướng | r trên mức rất cao | r sau sai phân + DW | 0,974 → −0,207; DW 0,005 |
| 2 | Quan hệ phi tuyến | Pearson trộn hai nhánh | scatter, MI, $R^2$ hai mô hình | 0,379 → 0,813; hai nhánh −0,649 / +0,910 |
| 3 | Độ trễ dẫn dắt | CCF thô nhoè theo nhịp của chính x | CCF sau prewhitening | đỉnh trễ 1 → **trễ 0**; r ở trễ 24: 0,828 → 0,061 |
| 4 | Quan hệ đổi theo mùa | một hệ số cho cả năm | tương quan trượt | cả năm 0,616; trượt 90 ngày −0,801 … +0,968 |
| 5 | Granger | đọc thành nhân quả | chạy hai chiều, tìm biến gây nhiễu | p ≈ 0 ở **cả hai** chiều |

### 4.1 Ba hệ số tương quan, và vì sao phải vẽ trước

**Pearson** đo quan hệ **tuyến tính**; **Spearman** đo quan hệ **đơn điệu** (tương quan trên hạng); **Kendall** cũng theo hạng, dựa trên số cặp thuận
– nghịch, bền hơn với mẫu nhỏ. FPP: "The correlation coefficient only measures the strength of the linear relationship between two variables, and can
sometimes be misleading."

![Bộ tứ Anscombe](hinh/anscombe.png)

**Đọc hình.** Bốn bộ dữ liệu của Anscombe (1973) có cùng $r = 0{,}82$ và cùng đường hồi quy $y \approx 3{,}00 + 0{,}50x$, nhưng: I là quan hệ tuyến tính
có nhiễu; II là **đường cong** (Spearman 0,691); III là tuyến tính chặt cộng **một ngoại lai** (Spearman 0,991); IV là một cột điểm cộng **một điểm duy
nhất** kéo cả đường hồi quy (Spearman 0,500). Mutual information cũng phân biệt được: 0,329 / 0,403 / 0,481 / **0,121**.

### 4.2 Tình huống 1 — tương quan giả giữa hai chuỗi có xu hướng

Granger & Newbold (1974) mô phỏng hai **random walk độc lập** rồi hồi quy chúng với nhau: "Using the traditional t test at the 5 % level, the null
hypothesis of no relationship between the two series would be rejected (wrongly) on approximately three-quarters of all occasions."

Ví dụ thật: **CPI-U** và **dân số Mỹ**, 420 tháng 1990–2024.

![Tương quan giả](hinh/tuong-quan-gia.png)

**Đọc hình.** Trái: hai chuỗi cùng đi lên. Giữa: scatter trên **mức** — $r = 0{,}974$, gần như một đường. Phải: scatter trên **sai phân** (thay đổi
tháng này so với tháng trước) — đám mây không hình dạng, $r = -0{,}207$.

Ba bằng chứng nên báo cùng nhau:

| Đại lượng | Giá trị | Nghĩa |
|---|---|---|
| $r$ trên mức | 0,974 | "cùng tăng theo thời gian" |
| $R^2$ hồi quy mức | 0,9495 | trông như giải thích được 95% |
| $t$ của hệ số | **88,6** | "cực kỳ có ý nghĩa" — nhưng sai số chuẩn đã bị ước lượng thấp |
| **Durbin–Watson** | **0,0051** | phần dư tự tương quan gần như hoàn toàn → **mô hình sai đặc trưng** |
| $r$ sau sai phân | −0,207 | quan hệ thật gần như không còn |

Granger & Newbold: "a high value for $R^2$ … combined with a low value of $d$, is no indication of a true relationship", và khi phần dư tự tương quan mạnh
"the only conclusion that can be reached is that the equation is mis-specified". Quy tắc dân gian "$R^2 > DW$ thì nghi hồi quy giả" thường được gán cho
họ nhưng **không có trong bài báo** — cứ dùng như một dấu hiệu, đừng trích như định lý. Phillips (1986) chứng minh phần lý thuyết: với chuỗi không dừng,
"the usual t ratio significance tests do not possess limiting distributions but actually diverge".

### 4.3 Tình huống 2 — quan hệ phi tuyến: nhiệt độ và tải điện

![Quan hệ chữ U](hinh/chu-u.png)

**Đọc hình.** Trái: mỗi chấm là một giờ của năm 2024, màu theo tháng. Đường đen (hồi quy tuyến tính) **bỏ sót** phần bên trái: dưới ~18 °C, càng lạnh
tải càng **tăng** (sưởi). Đường cam là mô hình hai nhánh CDD/HDD. Phải: quét mốc chia — $R^2$ cao nhất ở 19,5 °C (0,814), còn mốc quy ước 65 °F =
18,33 °C cho 0,813; mốc 65 °F của EIA là **quy ước**, không phải tối ưu.

**Công thức degree day** (EIA, mốc 65 °F): $\text{CDD}_t = \max(T_t - 18{,}33, 0)$, $\text{HDD}_t = \max(18{,}33 - T_t, 0)$.

| Đại lượng | Giá trị |
|---|---|
| Pearson | 0,616 |
| Spearman / Kendall | 0,733 / 0,572 |
| $R^2$ hồi quy theo $T$ | **0,379** |
| $R^2$ hồi quy theo CDD + HDD | **0,813** |
| Pearson khi $T \le 18{,}33$ (2.877 giờ) | **−0,649** |
| Pearson khi $T > 18{,}33$ (5.900 giờ) | **+0,910** |
| Mutual information | **0,862 nat** |

Một hệ số 0,616 che mất việc quan hệ **đổi dấu**: ở Texas nhánh nóng dài hơn nên Pearson vẫn dương và khá lớn — với vùng ôn hoà hơn (New England) nó
có thể gần 0 trong khi quan hệ rất mạnh.

**Mutual information** đo mọi dạng phụ thuộc: $I(X;Y) = \int p(x,y) \log \frac{p(x,y)}{p(x)p(y)}$, ước lượng bằng k-láng giềng (Kraskov 2004; Ross 2014),
đơn vị **nat**:

```python
from sklearn.feature_selection import mutual_info_regression
mutual_info_regression(t.reshape(-1, 1), y, random_state=0)   # phải đặt random_state để tái lập
```

**Cái bẫy của MI trên chuỗi thời gian:** kiểm ý nghĩa bằng hoán vị **từng điểm** sẽ phá tự tương quan và cho dương tính giả. Dùng **hoán vị theo khối**
(Gohil et al., 2025: "We adopt a block shuffle permutation to build the null distribution"). Với nhiệt độ × tải, khối 168 giờ, 100 lần hoán vị: MI thật
0,862 so với ngưỡng 95% của phân phối rỗng **0,124** → p = 0,0099. Bài lab có phản ví dụ: hai chuỗi AR(0,99) **độc lập** cho p < 0,05 khi hoán vị từng
điểm, nhưng p > 0,05 khi hoán vị theo khối.

![Phân phối rỗng của MI](hinh/mi-khoi.png)

**Đọc hình.** Hai chuỗi AR(0,99) **độc lập** (n = 2.000, seed 0) có MI quan sát được 0,332 — chỉ vì cả hai đều trơn. Phân phối rỗng dựng bằng hoán vị
**từng điểm** (cam) tập trung quanh 0,01 với ngưỡng 95% là 0,025 → p = 0,005, kết luận "có quan hệ" hoàn toàn sai. Phân phối rỗng dựng bằng hoán vị
**theo khối 200** (xanh) trải tới 0,33, ngưỡng 95% là 0,329 → p = 0,055, không bác bỏ. Cùng một dữ liệu, hai cách kiểm cho hai kết luận trái ngược.

### 4.4 Tình huống 3 — CCF và prewhitening

**Hàm tương quan chéo** cho biết độ trễ nào hai chuỗi khớp nhau nhất. Quy ước của buổi:

$$
r_k = \operatorname{corr}(x_t,\ y_{t+k}), \qquad k \ge 0 \ \text{nghĩa là } x \textbf{ đi trước } y
$$

Cẩn thận với thư viện: `statsmodels.tsa.stattools.ccf(a, b)` trả $\operatorname{corr}(a_{t+k}, b_t)$ — muốn "x dẫn y" phải gọi `ccf(y, x)`. R cũng vậy:
"The lag k value returned by ccf(x, y) estimates the correlation between x[t+k] and y[t]". Hàm `pccf` mới của statsmodels 0.15 lại dùng thứ tự ngược
lại. **Luôn kiểm bằng dữ liệu mô phỏng** $y_t = x_{t-3}$ trước khi tin hướng.

**Vấn đề:** nếu bản thân $x$ có tự tương quan mạnh (nhiệt độ có nhịp 24 giờ), CCF thô sẽ "nhoè" theo chính cấu trúc đó. Penn State: "the CCF is affected
by the time series structure of the x-variable and any "in common" trends". Cách chữa là **prewhitening**: khớp một mô hình AR cho $x$, lọc **cả hai**
chuỗi bằng cùng bộ hệ số, rồi mới tính CCF.

```python
phi = AutoReg(x, lags=48).fit().params[1:]                  # AR(48) đủ phủ nhịp 24 giờ
loc = lambda v: np.array([v[i] - phi[::-1] @ v[i-48:i] for i in range(48, v.size)])
r = ccf_tu_viet(loc(x), loc(y), so_tre=48)
```

![CCF trước và sau prewhitening](hinh/ccf.png)

**Đọc hình.** Trái (thô): cả dải trễ 0–48 đều trên 0,8; đỉnh ở **trễ 1** (0,863) nhưng trễ 24 vẫn **0,828** — hình dạng này là nhịp ngày của CDD, không
phải quan hệ. Phải (sau prewhitening AR(48)): đỉnh nhọn ở **trễ 0** (0,205), giảm còn 0,163 ở trễ 1, 0,119 ở trễ 3, và **0,061** ở trễ 24; dải
$2/\sqrt{n} = 0{,}0214$. Kết luận đúng: tải phản ứng với nhiệt độ **gần như tức thì**, ảnh hưởng tắt sau vài giờ. Nếu dùng AR(24) thì trễ 24 còn 0,113 —
bậc lọc phải đủ phủ chu kỳ.

### 4.5 Tình huống 4 — tương quan trượt: quan hệ có ổn định không?

![Tương quan trượt](hinh/truot.png)

**Đọc hình.** Tương quan giữa nhiệt độ trung bình ngày và tải điện ngày, cửa sổ 90 ngày. Cuối mùa đông xuống **−0,801** (cửa sổ kết thúc 31/3/2024);
giữa mùa hè lên **+0,968** (14/10/2024); đường gạch là con số cả năm **0,616**. Cửa sổ 30 ngày còn cực đoan hơn: **−0,971** (7/2/2024).

Một hệ số cho cả năm là **trung bình của hai chế độ ngược nhau**. Khi báo cáo tương quan, luôn kèm câu "trên khoảng thời gian nào" và một hình trượt.
Lưu ý kỹ thuật: `rolling(90)` mặc định cần đủ 90 điểm, nhưng `rolling("90D")` (cửa sổ theo thời gian) mặc định `min_periods=1` — hai điểm đầu đủ để cho
ra ±1 giả.

### 4.6 Tình huống 5 — Granger: "giúp dự báo" chứ không phải "gây ra"

**Kiểm định Granger** so hai mô hình cho $y$: chỉ dùng quá khứ của $y$, và dùng thêm quá khứ của $x$. Nếu thêm $x$ làm giảm sai số có ý nghĩa thống kê
thì "$x$ Granger-causes $y$".

```python
from statsmodels.tsa.stattools import grangercausalitytests

kq = grangercausalitytests(np.column_stack([y, x]), maxlag=4)   # kiểm CỘT 2 gây ra CỘT 1
p = {k: kq[k][0]["ssr_ftest"][1] for k in kq}                   # p-value theo từng độ trễ
# 0.15 đã BỎ tham số verbose: hàm không in gì nữa, đọc dict trả về
```

![Granger hai chiều](hinh/granger.png)

**Đọc hình.** Trái: hồ sơ trung bình theo giờ UTC của tải điện và nhiệt độ — cùng một nhịp 24 giờ, lệch pha nhẹ. Phải: tương quan chéo cao ở **cả hai
chiều** (trễ 1: CDD dẫn tải 0,863; tải "dẫn" CDD 0,814). Kết quả kiểm định: CDD → tải $p \approx 0$ **và** tải → CDD $p \approx 0$. Đọc theo kiểu nhân
quả thì thành "tải điện gây ra nhiệt độ ngoài trời".

Vì sao? Cả hai cùng bị điều khiển bởi **nhịp ngày** — một biến gây nhiễu chung. Wikipedia tóm tắt đúng: "If both X and Y are driven by a common third
process with different lags, one might still fail to reject the alternative hypothesis of Granger causality"; và chính Granger sau này gọi nó là
"temporally related". Maziarz (2015) liệt kê các cách đọc khác: "true causal relation, opposite direction of the true causation, instant causality, time
series cointegration, not frequent enough sampling". Điều kiện dùng: chuỗi phải **dừng** (sai phân trước, hoặc dùng Toda–Yamamoto), và kết luận luôn
viết dưới dạng "quá khứ X giúp dự báo Y".

### 4.7 Tương quan ≠ giá trị dự báo

Một biến chỉ dùng được cho dự báo **ex-ante** nếu tại thời điểm dự báo ta biết (hoặc dự báo được) giá trị tương lai của nó. FPP §7.6: "in order to
generate ex-ante forecasts, the model requires forecasts of the predictors"; còn dùng giá trị thật của biến giải thích trong tương lai là **ex-post** —
"These are not genuine forecasts, but are useful for studying the behaviour of forecasting models". Nhiệt độ hợp lệ vì có dự báo thời tiết (nhưng phải
dùng **dự báo** nhiệt độ, kèm sai số của nó); "giá dầu tuần sau" thì không.

### 4.8 Nhiều biến: đa cộng tuyến và tương quan một phần

Khi thêm nhiều biến giải thích, câu hỏi đổi từ "biến này có liên quan không" sang "biến này có thêm thông tin gì so với các biến kia". Hai công cụ:

**VIF** (variance inflation factor) cho biến $j$ là $1/(1 - R_j^2)$ với $R_j^2$ là $R^2$ khi hồi quy biến $j$ theo các biến còn lại. Trên bốn biến của
buổi (2024, theo giờ):

| Biến | VIF | Tương quan một phần với CDD |
|---|---|---|
| CDD | 39,2 | — |
| HDD | 1,5 | −0,023 |
| CDD trễ 1 giờ | 39,8 | **0,954** |
| CDD trung bình 24 giờ | 3,9 | 0,087 |

CDD và CDD trễ 1 giờ có $r = 0{,}987$: hai biến gần như cùng một thông tin, VIF gần 40. Ngưỡng "VIF > 5 hoặc > 10 là cao" chỉ là quy tắc kinh nghiệm —
đa cộng tuyến làm hệ số riêng lẻ không diễn giải được nhưng **không** làm dự báo tệ đi.

**Cảnh báo quan trọng:** đừng đưa cả nhiệt độ **và** CDD, HDD vào cùng một mô hình — theo định nghĩa $T = \text{CDD} - \text{HDD} + 18{,}33$ (kiểm
chạy thật: sai khác tối đa 1,8e−15), tức phụ thuộc tuyến tính **chính xác**; VIF nhảy lên cỡ $10^{15}$ và ma trận thiết kế suy biến.

**Tương quan một phần** loại ảnh hưởng của các biến còn lại: $\rho_{ij\cdot} = -P_{ij}/\sqrt{P_{ii}P_{jj}}$ với $P = R^{-1}$. Trong bảng trên, CDD và
CDD trung bình 24 giờ có tương quan thô 0,845 nhưng tương quan một phần chỉ **0,087** — phần chung đã nằm trong CDD trễ 1 giờ. Đây cũng là cách khử biến
gây nhiễu kinh điển: mùa vụ.

Ở statsmodels 0.15, `variance_inflation_factor(exog, i)` **tự chuẩn hoá** ma trận thiết kế ("Numerical instability in VIF was fixed by standardizing the
design matrix"), nên lời khuyên cũ "nhớ thêm cột hằng số" không còn cần.

### 4.9 Quy trình cho một cặp chuỗi mới

Sáu bước, mỗi bước một con số để ghi vào báo cáo:

1. **Vẽ scatter** (tô màu theo thời gian) và hai chuỗi theo thời gian. Nhìn trước khi tính.
2. **Kiểm tính dừng** từng chuỗi (ADF + KPSS). Nếu cả hai không dừng: tính tương quan trên **mức và sai phân**, kèm $R^2$, $t$, DW của hồi quy mức.
3. **Đo phi tuyến**: Pearson so với Spearman; MI (có kiểm ý nghĩa bằng hoán vị **theo khối**); thử biến đổi theo cơ chế (CDD/HDD, log, bậc hai) và so
   $R^2$.
4. **Tìm độ trễ**: CCF **sau prewhitening**, đọc đỉnh và độ rộng, so với dải $2/\sqrt{n}$.
5. **Kiểm ổn định**: tương quan trượt; nếu đổi dấu thì chia chế độ (mùa, ngày làm việc/nghỉ) thay vì gộp.
6. **Kiểm dùng được không**: tại thời điểm dự báo có biết giá trị tương lai của biến đó không? Nếu không, cần dự báo cho chính nó — và sai số của dự báo
   đó sẽ cộng vào.

Granger chỉ là **một** bằng chứng trong bước 4–5, và luôn viết thành "quá khứ X giúp dự báo Y".

## 5. Lab từng bước

### Bước 1 — Chạy code đầu buổi

```bash
cd lab && make up
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/tuong_quan.py
make check                    # 3/10 đỏ
```

```text
1. CPI × dân số: {'r_muc': 0.9744, 'ket_luan': 'quan hệ mạnh'}
3. độ trễ dẫn dắt (thô): 1 | sau prewhitening: 1
5. x gây ra y (Granger, p < 0,05)
```

### Bước 2 — Tương quan giả

Sửa `tuong_quan_chuoi`: thêm tương quan sau sai phân và `hoi_quy_don` (R², t, DW), rồi kết luận theo ba bằng chứng.

### Bước 3 — Phi tuyến

Vẽ scatter nhiệt độ × tải tô màu theo tháng; tính MI; so $R^2$ của hồi quy theo $T$ với hồi quy theo CDD + HDD; quét mốc chia.

### Bước 4 — CCF và prewhitening

Sửa `do_tre_dan_dat` để lọc AR(48) trước khi tính CCF. Kiểm quy ước bằng chuỗi mô phỏng $y_t = x_{t-3}$, rồi chạy trên dữ liệu thật và so CCF thô với
CCF sau lọc ở trễ 24.

### Bước 5 — Trượt và Granger

Vẽ tương quan trượt 30 và 90 ngày. Sửa `granger_hai_chieu`: chạy **cả hai chiều**, và khi cả hai cùng có ý nghĩa thì nói rõ đó là dấu hiệu của biến gây
nhiễu chung, không phải nhân quả.

```bash
make check                    # 10/10 xanh
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/tuong_quan.py
```

```text
1. CPI × dân số: {'r_muc': 0.9744, 'r_sai_phan': -0.2071, 'r2': 0.9495, 't': 88.6143, 'dw': 0.0051,
                  'ket_luan': 'nghi TƯƠNG QUAN GIẢ: mức tương quan cao, phần dư tự tương quan mạnh (DW thấp),
                               sai phân xong gần như hết'}
2. tải × nhiệt độ: {'pearson': 0.616, 'spearman': 0.733, 'kendall': 0.572} MI = 0.862
3. độ trễ dẫn dắt (thô): 1 | sau prewhitening: 0
4. tương quan trượt 90 ngày: min -0.801 max 0.968
5. CẢ HAI CHIỀU cùng có ý nghĩa — không thể đọc thành nhân quả; thường do biến gây nhiễu chung hoặc mùa vụ chung
```

So với đầu buổi: dòng 1 thêm hai bằng chứng (sai phân, DW) và đổi kết luận; dòng 3 đổi từ trễ 1 sang trễ 0; dòng 5 không còn câu nhân quả.

## 6. Lỗi thường gặp & cách chẩn đoán

| Triệu chứng | Nguyên nhân | Chẩn đoán | Sửa |
|---|---|---|---|
| r = 0,97 giữa hai chuỗi chẳng liên quan | cả hai có xu hướng | DW của hồi quy mức; r sau sai phân | báo cả ba con số, sai phân/khử xu hướng |
| "t = 88, chắc chắn có quan hệ" | sai số chuẩn bị ước lượng thấp khi phần dư tự tương quan | DW, ACF phần dư | hồi quy động (buổi 18) hoặc sai phân |
| Pearson ≈ 0 nhưng scatter hình chữ U | quan hệ phi tuyến | vẽ scatter, tính MI, chia theo ngưỡng | tách CDD/HDD, spline, cây |
| MI "có ý nghĩa" trên hai chuỗi độc lập | hoán vị từng điểm phá tự tương quan | so hoán vị thường với hoán vị khối | hoán vị theo khối |
| MI đổi giá trị mỗi lần chạy | ước lượng k-NN thêm nhiễu | `random_state` | đặt seed cố định |
| CCF cao ở mọi độ trễ | chưa prewhiten; x tự tương quan mạnh | nhìn CCF ở trễ bằng chu kỳ (24) | lọc AR bậc ≥ chu kỳ cho cả hai chuỗi |
| Độ trễ dẫn dắt ra dấu ngược | nhầm quy ước `ccf(x, y)` | kiểm bằng $y_t = x_{t-3}$ | tự viết và ghi rõ quy ước |
| `rolling("90D")` cho ±1 ở đầu chuỗi | mặc định `min_periods=1` | xem vài giá trị đầu | đặt `min_periods` |
| "Granger test chứng minh nhân quả" | đọc sai tên kiểm định | chạy cả hai chiều | viết "giúp dự báo"; tìm biến gây nhiễu |
| Granger trên chuỗi không dừng | phân phối của thống kê sai | ADF/KPSS trước | sai phân, hoặc Toda–Yamamoto |
| `grangercausalitytests(..., verbose=True)` báo lỗi | 0.15 đã bỏ tham số | đọc release notes | dùng dict trả về |
| Biến tương quan cao nhưng vô dụng khi dự báo | không biết trước giá trị tương lai | hỏi "lúc ra dự báo có số này chưa?" | dùng dự báo của biến đó (ex-ante), hoặc bỏ |

## 7. Bài tập về nhà

1. **Mô phỏng Granger–Newbold.** Sinh 1.000 cặp random walk **có drift** độc lập (n = 200). Bao nhiêu phần trăm cặp có $|r| > 0{,}9$ trên mức? Sau sai
   phân? Bao nhiêu phần trăm có $t$ vượt 1,96?
2. **Vùng khác.** Lặp tình huống 2 và 4 cho ISNE (New England) với nhiệt độ Boston (tự tải qua Open-Meteo theo đúng quy ước UTC của khoá). Pearson cả
   năm có nhỏ hơn ERCOT không, và vì sao?
3. **Prewhitening ngược.** Lọc theo AR của **tải điện** thay vì của CDD rồi tính CCF. Kết quả khác gì, và vì sao Box–Jenkins chọn lọc theo chuỗi **giải
   thích**?

## 8. Tiêu chí "Xong khi"

- [ ] `make check` xanh 10/10.
- [ ] Với một cặp chuỗi lạ, trả lời đủ 4 câu kèm số: (a) tương quan có giả không (r mức, r sai phân, DW); (b) tuyến tính hay phi tuyến (scatter, MI,
      $R^2$ hai mô hình); (c) độ trễ dẫn dắt sau prewhitening là bao nhiêu; (d) biến đó có biết trước giá trị tương lai không.
- [ ] Giải thích được vì sao Granger hai chiều cùng có ý nghĩa trên cặp nhiệt độ–tải điện.
- [ ] Nêu được một trường hợp tương quan trượt đổi dấu và hệ quả với việc chọn dữ liệu huấn luyện.

## 9. Đọc thêm

- Granger, C.W.J. & Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics* 2(2), 111–120.
- Phillips, P.C.B. (1986). Understanding spurious regressions in econometrics. *Journal of Econometrics* 33(3), 311–340.
- Anscombe, F.J. (1973). Graphs in statistical analysis. *The American Statistician* 27(1), 17–21.
- Penn State STAT 510 — Lesson 8–9: cross-correlation và prewhitening: https://online.stat.psu.edu/stat510/Lesson09.html
- Kraskov, A., Stögbauer, H. & Grassberger, P. (2004). Estimating mutual information. *Phys. Rev. E* 69, 066138; Ross, B.C. (2014). *PLoS ONE* 9(2).
- Gohil, N. et al. (2025). Cross Mutual Information. arXiv:2507.15372 — hoán vị theo khối.
- Maziarz, M. (2015). A review of the Granger-causality fallacy. *The Journal of Philosophical Economics* VIII(2), 86–105.
- Toda, H.Y. & Yamamoto, T. (1995). Statistical inference in vector autoregressions with possibly integrated processes. *J. Econometrics* 66, 225–250.
- Hyndman & Athanasopoulos, *FPP the Pythonic Way* §2.6, §7.3, §7.6, §7.8, ch. 10: https://otexts.com/fpppy/
- U.S. EIA — *Degree days*: https://www.eia.gov/energyexplained/units-and-calculators/degree-days.php
