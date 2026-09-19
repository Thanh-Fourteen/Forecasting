# Kiểm tra buổi 6 — Phân rã chuỗi thời gian

## Nhắc lại khái niệm

**Câu 1.** Vì sao với chu kỳ chẵn ($m$ = 4, hay $m$ = 24) phải dùng 2×m-MA thay vì trung bình trượt $m$ điểm?

- A. Để xu hướng mượt hơn
- B. Vì cửa sổ $m$ điểm không có tâm; 2×m-MA đối xứng quanh $t$ và cho mỗi vị trí trong vòng đúng trọng số $1/m$
- C. Vì statsmodels bắt buộc
- D. Để giữ được xu hướng ở đầu và cuối chuỗi

<details>
<summary>Đáp án</summary>

**B** (mục 4.1). Trung bình 4 quý liền nhau rơi vào giữa quý 2 và quý 3; lấy trung bình hai cửa sổ kề nhau đưa nó về đúng một quý,
với hai đầu mỗi bên $1/(2m)$ vì chúng là cùng một vị trí trong vòng. **A sai**: mượt hơn chỉ là tác dụng phụ. **C sai**: đây là lý do
toán, không phải yêu cầu của thư viện. **D sai**: 2×m-MA vẫn mất $m/2$ điểm mỗi đầu (12 giờ với $m$ = 24).

</details>

**Câu 2.** Điều nào **không** phải điểm yếu của phân rã cổ điển?

- A. Không có xu hướng ở vài điểm đầu và cuối
- B. Mùa vụ bị giả định giống hệt nhau mọi vòng
- C. Chỉ dùng được cho dữ liệu tháng và quý
- D. Một điểm bất thường làm méo cả xu hướng lẫn mùa vụ

<details>
<summary>Đáp án</summary>

**C.** Phân rã cổ điển chạy với chu kỳ bất kỳ (buổi này chạy với 24 giờ); "chỉ tháng và quý" là giới hạn của X-13ARIMA-SEATS (hộp Nâng
cao). **A, B, D đều là điểm yếu thật**: A là mất $m/2$ điểm mỗi đầu (mục 4.1); B là lý do phần dư PJM còn mùa vụ ngày đổi theo
mùa (mục 4.3); D là lý do cần robust (mục 4.6).

</details>

**Câu 3.** Bật `robust=True` trong STL/MSTL thì một giờ số liệu hỏng:

- A. Bị xoá khỏi dữ liệu
- B. Gần như không ảnh hưởng xu hướng và mùa vụ, nhưng vẫn nằm trong phần dư
- C. Được thay bằng trung bình hai giờ kề
- D. Làm phần dư ở giờ đó nhỏ đi

<details>
<summary>Đáp án</summary>

**B** (mục 4.6): lượt sau cho điểm có phần dư quá lớn trọng số tới 0 khi ước lượng xu hướng, mùa vụ; điểm đó ở lại trong phần dư. **A,
C sai**: robust không sửa dữ liệu, chỉ đổi trọng số. **D sai** và ngược lại: phần dư ở giờ hỏng **lớn hơn** khi robust (−36.323 so với
−26.322 MW), vì lỗi không còn bị chia sang mùa vụ.

</details>

**Câu 4.** $F_S$ được tính bằng:

- A. $\operatorname{Var}(S) / \operatorname{Var}(y)$
- B. $\max(0, 1 - \operatorname{Var}(R) / \operatorname{Var}(S + R))$
- C. $\max(0, 1 - \operatorname{Var}(R) / \operatorname{Var}(T + R))$
- D. Tương quan giữa $S$ và $y$

<details>
<summary>Đáp án</summary>

**B** (mục 4.5). **C** là $F_T$. **A sai**: chia cho cả chuỗi thì con số phụ thuộc xu hướng to hay nhỏ, không so mùa vụ với phần dư.
**D sai**: tương quan đo hai thứ cùng lên xuống, không đo phần dư nhỏ tới đâu.

</details>

## Vận dụng

**Câu 5.** Chuỗi 8, 4, 2, 6, 10, 6, 4, 8 có $m$ = 4. Tính $\hat T_3$ và $\hat T_4$ (vị trí đếm từ 1) bằng 2×4-MA.

<details>
<summary>Đáp án</summary>

Trọng số 1/8, 1/4, 1/4, 1/4, 1/8 cho 5 điểm quanh $t$. $\hat T_3$ = 8/8 + (4 + 2 + 6)/4 + 10/8 = 1 + 3 + 1,25 = **5,25**. $\hat T_4$ =
4/8 + (2 + 6 + 10)/4 + 6/8 = 0,5 + 4,5 + 0,75 = **5,75**. Nhầm hay gặp: dùng 4 điểm với trọng số 1/4 (ra 5 cho $\hat T_3$), tức trung
bình không có tâm.

</details>

**Câu 6.** `STL(y, period=24)` trên nhu cầu điện theo giờ cả năm cho phương sai phần dư 2,8 GW², nhỏ hơn MSTL (24, 168) (16,5 GW²). Đồng
nghiệp kết luận STL tốt hơn. Bạn kiểm gì?

<details>
<summary>Đáp án</summary>

Vẽ **xu hướng** của STL (mục 4.4). Cửa sổ xu hướng mặc định chỉ 47 giờ, đủ mềm để xu hướng uốn theo từng cuối tuần và từng đợt thời tiết:
xu hướng "tranh" dao động với mùa vụ, nên phần dư nhỏ giả tạo. Kiểm trung bình xu hướng theo thứ (có lõm cuối tuần không) và xu hướng có
răng cưa theo ngày không. Phần dư nhỏ không có nghĩa phân rã đúng.

</details>

**Câu 7.** Lượt truy cập website theo giờ có nhịp ngày, tuần và năm. Chọn `periods` cho MSTL khi có 2 năm dữ liệu. Nếu chỉ có 6 tháng thì
chuyện gì xảy ra?

<details>
<summary>Đáp án</summary>

`periods=(24, 168, 8766)` (năm ≈ 365,25 × 24 giờ). Với 6 tháng (khoảng 4.380 giờ), chu kỳ năm dài hơn nửa chuỗi nên MSTL **bỏ** chu kỳ
đó kèm cảnh báo (đã chạy thử trên statsmodels 0.15): chưa có một vòng năm thì không ước lượng được mùa vụ năm, nhịp năm rơi vào xu hướng.
Nhầm hay gặp: khai 8760 hay 8766 rồi tin mình đã có mùa vụ năm mà không đọc cảnh báo.

</details>

**Câu 8.** Trước khi gọi `MSTL`, `y.isna().sum()` cho 47. Nếu bỏ qua thì sao, và xử lý thế nào?

<details>
<summary>Đáp án</summary>

STL/MSTL của statsmodels trả xu hướng, mùa vụ, phần dư **toàn NaN**, không lỗi, không cảnh báo (mục 4.4); mọi số sau đó, như $F_S$, thành
NaN. Xử lý: tìm vì sao thiếu (ở PJM là hai ngày đổi giờ), điền (nội suy theo thời gian như `lap_cho_trong`), **ghi lại** số giờ đã điền,
và cẩn thận khi đọc phần dư quanh các giờ đó. Nhầm hay gặp: điền 0 — tạo ra 47 "giờ không dùng điện" giả, phân rã sẽ nhét chúng vào phần
dư và làm méo mùa vụ.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo phân rã cổ điển chu kỳ 24 cho điện PJM 2024 viết: "Trung bình phần dư theo thứ chỉ vài trăm MW, vậy chuỗi không có mùa
vụ tuần." Kèm bảng trung bình **xu hướng** theo thứ: T4 95.036, T7 89.523, CN 88.459 MW. Chỉ ra lỗi.

<details>
<summary>Đáp án</summary>

Mùa vụ tuần không biến mất mà **nằm trong xu hướng**: 2×24-MA là trung bình một ngày nên bám theo mức thấp của cuối tuần; chính bảng kèm
theo cho T7, CN thấp hơn T4 khoảng 5.500–6.600 MW (mục 4.3). Kiểm phần dư theo thứ là chưa đủ; phải xem xu hướng theo thứ và tỷ lệ mẫu hình
thứ × giờ. MSTL (24, 168) cho $F_{S,168}$ = 0,415: mùa vụ tuần có thật.

</details>

**Câu 10.** Bảng độ mạnh trong ba báo cáo về cùng một chuỗi:

| Báo cáo | Phương pháp | $F_T$ | $F_{S,24}$ | $F_{S,168}$ |
|---|---|---|---|---|
| A | cổ điển (24) | 0,828 | 0,618 | — |
| B | MSTL (24, 168) | 0,888 | 0,829 | 0,415 |
| C | MSTL robust | 0,817 | 0,739 | 0,252 |

Một người kết luận: "Mùa vụ ngày yếu (0,618) theo A, mạnh (0,829) theo B, nên dữ liệu không đáng tin; và C cho thấy robust làm phân rã tệ
hơn." Nhận xét.

<details>
<summary>Đáp án</summary>

(1) $F$ là con số của **một phân rã**, không chỉ của dữ liệu (mục 4.5). A ép mùa vụ ngày giống nhau cả năm, nên phần đổi theo mùa rơi vào
phần dư, phần dư to, $F_S$ thấp. Dữ liệu không có vấn đề; phải báo $F$ kèm tên phương pháp. (2) C thấp hơn vì phần dư robust **giữ trọn** các
điểm bất thường (như giờ hỏng 21/11) nên phương sai phần dư lớn hơn (mục 4.6). Robust bảo vệ xu hướng và mùa vụ, không nhằm làm phần dư nhỏ;
không thể kết luận "tệ hơn" từ $F$.

</details>
