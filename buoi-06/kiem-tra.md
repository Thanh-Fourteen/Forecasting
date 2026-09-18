# Kiểm tra buổi 6 — Phân rã chuỗi thời gian

## Nhắc lại khái niệm

**Câu 1.** Vì sao với chu kỳ chẵn $m = 24$ phải dùng 2×24-MA thay vì 24-MA?

- A. Để xu hướng mượt hơn
- B. Vì cửa sổ 24 điểm không có tâm; 2×24-MA đối xứng quanh $t$ và mỗi giờ trong ngày có đúng trọng số 1/24
- C. Vì statsmodels yêu cầu
- D. Để giữ được đầu và cuối chuỗi

<details>
<summary>Đáp án</summary>

**B.** Trung bình 24 điểm rơi vào giữa hai mốc; trung bình trượt 2 lần nữa đưa về đúng $t$, với trọng số 1/48 ở $t \pm 12$ (cùng một giờ trong
ngày). D sai: 2×24-MA vẫn mất 12 giờ mỗi đầu. A là tác dụng phụ, không phải lý do.

</details>

**Câu 2.** Phát biểu nào **không** phải điểm yếu của phân rã cổ điển theo FPP?

- A. Không có xu hướng ở vài quan sát đầu và cuối
- B. Mùa vụ giả định lặp y hệt mỗi chu kỳ
- C. Chỉ dùng được cho dữ liệu tháng và quý
- D. Không robust với giá trị bất thường

<details>
<summary>Đáp án</summary>

**C.** Phân rã cổ điển dùng được cho mọi chu kỳ (buổi học chạy với 24 giờ). "Chỉ tháng/quý" là giới hạn của **X-11/SEATS**. A, B, D đều nằm trong
danh sách điểm yếu của FPP.

</details>

**Câu 3.** Bật `robust=True` trong STL thì giá trị bất thường:

- A. Bị xoá khỏi dữ liệu
- B. Không ảnh hưởng xu hướng và mùa vụ, nhưng vẫn nằm trong phần dư
- C. Được thay bằng trung bình
- D. Làm phần dư nhỏ đi

<details>
<summary>Đáp án</summary>

**B.** Vòng ngoài giảm trọng số điểm có phần dư lớn ($\rho = (1 - u^2)^2$, bằng 0 khi $u \ge 1$) khi ước lượng xu hướng và mùa vụ; điểm đó ở lại
trong phần dư. D ngược lại: phần dư robust thường **lớn hơn** (PJM: giờ hỏng −36.323 so với −26.322 MW).

</details>

**Câu 4.** $F_S$ tính theo FPP bằng:

- A. $\operatorname{Var}(S) / \operatorname{Var}(y)$
- B. $\max(0, 1 - \operatorname{Var}(R)/\operatorname{Var}(S + R))$
- C. $\max(0, 1 - \operatorname{Var}(R)/\operatorname{Var}(T + R))$
- D. Tương quan giữa $S$ và $y$

<details>
<summary>Đáp án</summary>

**B.** C là $F_T$. A không so với phần dư nên phụ thuộc cả xu hướng. Với nhiều mùa vụ, tính B cho từng thành phần với cùng phần dư.

</details>

## Vận dụng

**Câu 5.** Chuỗi $y = [10, 20, 30, 20, 10, 20, 30, 20, 10]$, chu kỳ $m = 4$. Tính $\hat T_3$ (vị trí thứ 3, đếm từ 1) bằng 2×4-MA.

<details>
<summary>Đáp án</summary>

2×4-MA: $\hat T_t = \tfrac18 y_{t-2} + \tfrac14 (y_{t-1} + y_t + y_{t+1}) + \tfrac18 y_{t+2}$. Với $t = 3$: $\tfrac18 \cdot 10 + \tfrac14 (20 + 30 +
20) + \tfrac18 \cdot 10 = 1{,}25 + 17{,}5 + 1{,}25 =$ **20**. Mùa vụ triệt tiêu hoàn toàn vì dữ liệu đúng chu kỳ 4.

</details>

**Câu 6.** Bạn chạy `STL(y, period=24)` trên nhu cầu điện theo giờ cả năm và thấy phương sai phần dư chỉ 2,8 GW², nhỏ hơn MSTL (16,5 GW²). Đồng
nghiệp kết luận STL tốt hơn. Bạn kiểm điều gì?

<details>
<summary>Đáp án</summary>

Vẽ **xu hướng**: với chu kỳ 24 và `seasonal=7`, cửa sổ xu hướng mặc định là 47 giờ — đủ mềm để xu hướng uốn theo từng cuối tuần và từng đợt thời
tiết. Kiểm trung bình xu hướng theo thứ (có lõm T7–CN không) và xu hướng có răng cưa không. Phần dư nhỏ vì xu hướng "cạnh tranh" với mùa vụ
(Cleveland), không phải vì phân rã tốt. Cần MSTL (24, 168) hoặc cửa sổ xu hướng dài hơn.

</details>

**Câu 7.** Chuỗi lượt truy cập website theo giờ trong 2 năm có nhịp ngày, nhịp tuần và nhịp năm. Chọn `periods` cho MSTL và nêu một vấn đề nếu
chỉ có 6 tháng dữ liệu.

<details>
<summary>Đáp án</summary>

`periods=(24, 168, 8766)` (năm ≈ 365,25 × 24 giờ) với 2 năm dữ liệu. Với 6 tháng (≈ 4.380 giờ), chu kỳ năm ≥ nửa độ dài chuỗi nên MSTL **bỏ** chu
kỳ đó (kèm UserWarning) — không thể ước lượng mùa vụ năm từ chưa đầy một chu kỳ; nhịp năm sẽ rơi vào xu hướng.

</details>

**Câu 8.** Trước khi gọi `MSTL`, `y.isna().sum()` cho 47. Điều gì xảy ra nếu bỏ qua, và bạn xử lý thế nào?

<details>
<summary>Đáp án</summary>

STL/MSTL của statsmodels 0.15 trả xu hướng, mùa vụ, phần dư **toàn NaN** mà không báo lỗi hay cảnh báo — mọi con số sau đó (như $F_S$) thành
NaN. Xử lý: tìm vì sao thiếu (ở PJM là hai ngày đổi giờ), điền (nội suy theo thời gian hoặc cùng giờ tuần trước), **ghi lại** số giờ đã điền,
và kiểm phần dư quanh các giờ đó khi đọc kết quả.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo phân rã cổ điển chu kỳ 24 cho điện PJM 2024 viết: "Phần dư không còn mẫu hình tuần — trung bình phần dư theo thứ chỉ vài
trăm MW. Vậy chuỗi không có mùa vụ tuần." Kèm bảng trung bình **xu hướng** theo thứ: T4 95.036, T7 89.523, CN 88.459 MW. Chỉ ra lỗi.

<details>
<summary>Đáp án</summary>

Mùa vụ tuần không biến mất — nó **nằm trong xu hướng**: 2×24-MA trung bình theo ngày nên bám theo mức thấp của cuối tuần (T7–CN thấp hơn T4
khoảng 5.500–6.600 MW). Kiểm phần dư theo thứ là chưa đủ; phải xem xu hướng có lõm theo thứ không, heatmap phần dư thứ×giờ, và ACF ở trễ 168.
MSTL (24, 168) cho $F_{S,168} = 0{,}415$ — mùa vụ tuần có thật.

</details>

**Câu 10.** Bảng độ mạnh trong hai báo cáo về cùng một chuỗi:

| Báo cáo | Phương pháp | $F_T$ | $F_{S,24}$ | $F_{S,168}$ |
|---|---|---|---|---|
| A | cổ điển (24) | 0,828 | 0,618 | — |
| B | MSTL (24, 168) | 0,888 | 0,829 | 0,415 |
| C | MSTL robust | 0,817 | 0,739 | 0,252 |

Một người kết luận: "Mùa vụ ngày yếu (0,618) theo A, mạnh (0,829) theo B — dữ liệu không đáng tin; và C cho thấy robust làm phân rã tệ hơn." Nhận xét.

<details>
<summary>Đáp án</summary>

(1) $F$ là thuộc tính của **phân rã**, không chỉ của dữ liệu: A ép mùa vụ ngày cố định cả năm nên phần biến thiên theo mùa vào phần dư → phần dư
lớn → $F_S$ thấp. Dữ liệu không có vấn đề; phải báo $F$ kèm tên phương pháp. (2) C thấp hơn vì phần dư robust **giữ trọn** các điểm bất thường
(như giờ hỏng 21/11) nên phương sai lớn hơn — robust bảo vệ xu hướng và mùa vụ khỏi điểm bất thường, không nhằm làm phần dư nhỏ. Không kết luận
"tệ hơn" từ $F$.

</details>
