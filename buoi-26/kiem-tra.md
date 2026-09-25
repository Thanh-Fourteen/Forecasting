# Kiểm tra buổi 26 — Conformal prediction cho chuỗi thời gian

## Nhắc lại khái niệm

**Câu 1.** Trong split conformal, vì sao lấy điểm thứ ⌈(n + 1)(1 − α)⌉ thay vì quantile 1 − α thường của n điểm?

- A. Vì giờ mới là điểm thứ n + 1; tính cả nó vào hàng thì mới bảo đảm được xác suất phủ ít nhất 1 − α
- B. Vì làm tròn lên cho code chạy nhanh hơn
- C. Vì quantile thường luôn cho khoảng rộng quá
- D. Vì cần bỏ điểm lớn nhất như một ngoại lai

<details>
<summary>Đáp án</summary>

**A** (mục 4.1): nếu dữ liệu hoán đổi được, điểm của giờ mới rơi vào một trong n + 1 thứ hạng với cơ hội ngang nhau; lấy hạng ⌈(n + 1)(1 − α)⌉ thì
khả năng nó không vượt ít nhất 1 − α (ví dụ tay: 9/11 ≥ 0,8). **B sai**: không liên quan tốc độ. **C sai**: ngược lại, quantile thường hơi **hẹp**
hơn và mất bảo đảm khi n nhỏ. **D sai**: không bỏ điểm nào; khi hạng vượt n thì khoảng còn vô hạn.

</details>

**Câu 2.** Vì sao split conformal trên PM2.5 phủ 90,9% trên hai năm mà vẫn bị coi là hỏng?

- A. Vì 90,9% lớn hơn 90%
- B. Vì chuỗi không hoán đổi được: mùa đông phủ thiếu, mùa hè phủ thừa, hai cái bù nhau thành con số trung bình đẹp
- C. Vì LightGBM thua naive
- D. Vì tập hiệu chỉnh quá ít điểm

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): quý 4 phủ 86,2%, quý 3 phủ 95,5%; coverage 30 ngày xuống 74,7% và ra ngoài dải cho phép 29,5% thời gian. **A sai**: 90,9% sát 90%;
vấn đề nằm ở từng mùa. **C sai**: LightGBM thắng naive (10,37 so với 10,65). **D sai**: 8.720 điểm là nhiều; thêm điểm cũng không sửa được trượt theo mùa.

</details>

**Câu 3.** CQR khác split conformal ở chỗ nào?

- A. CQR không cần tập hiệu chỉnh
- B. CQR dùng khoảng của quantile regression (rộng khi khó, hẹp khi dễ) rồi nới đều hai đầu một lượng tính từ tập hiệu chỉnh
- C. CQR tự chỉnh α sau mỗi giờ
- D. CQR bảo đảm coverage trong từng nhóm giờ

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): điểm $E = \max(\hat q_{lo} - y, y - \hat q_{hi})$, nới khoảng quantile bằng điểm thứ ⌈(n + 1)(1 − α)⌉. **A sai**: vẫn cần tập hiệu
chỉnh. **C sai**: đó là ACI. **D sai**: CQR đều hơn giữa các nhóm (88,2% ở giờ ô nhiễm nặng) nhưng không bảo đảm cho từng nhóm.

</details>

**Câu 4.** Trong ACI, ngay sau một giờ thực tế nằm **ngoài** khoảng, điều gì xảy ra?

- A. $\alpha_t$ tăng, khoảng giờ sau hẹp lại
- B. $\alpha_t$ giảm γ × 0,9, khoảng giờ sau rộng ra
- C. $\alpha_t$ trở về 0,1
- D. Mô hình điểm được học lại

<details>
<summary>Đáp án</summary>

**B** (mục 4.5): $\alpha_{t+1} = \alpha_t + \gamma(\alpha - 1) = \alpha_t - 0{,}9\gamma$; α nhỏ hơn nghĩa là quantile mức cao hơn, khoảng rộng hơn. **A sai**: đó là
khi trúng (tăng γ × 0,1), hoặc là lỗi ngược dấu trong `code/`. **C sai**: ACI không đặt lại α_t. **D sai**: ACI chỉ chỉnh khoảng, không học lại mô hình.

</details>

## Vận dụng

**Câu 5.** 14 điểm hiệu chỉnh, xếp tăng: 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 9, 11, 15. Dự báo điểm 50. Khoảng 80% theo split conformal là gì?

<details>
<summary>Đáp án</summary>

α = 0,2: hạng ⌈15 × 0,8⌉ = **12**, điểm thứ 12 là **9** (mục 4.1). Khoảng [41; 59]. Nhầm hay gặp: lấy hạng ⌈14 × 0,8⌉ = 12 cũng ra 9 ở đây, nhưng với
khoảng 90% thì ⌈15 × 0,9⌉ = 14 (điểm 15) khác ⌈14 × 0,9⌉ = 13 (điểm 11): bỏ "+1" làm khoảng hẹp đi.

</details>

**Câu 6.** Năm giờ hiệu chỉnh, α = 0,2:

| Giờ | Thực tế | Quantile thấp | Quantile cao |
|---|---|---|---|
| 1 | 30 | 20 | 50 |
| 2 | 80 | 90 | 130 |
| 3 | 120 | 100 | 160 |
| 4 | 60 | 50 | 90 |
| 5 | 200 | 150 | 180 |

Tính điểm CQR của từng giờ và lượng nới.

<details>
<summary>Đáp án</summary>

Điểm $E = \max(\text{thấp} - y,\ y - \text{cao})$: giờ 1: max(−10, −20) = **−10**; giờ 2: max(10, −50) = **10**; giờ 3: max(−20, −40) = **−20**; giờ 4:
max(−10, −30) = **−10**; giờ 5: max(−50, 20) = **20** (mục 4.3). Xếp tăng: −20, −10, −10, 10, 20. Hạng ⌈6 × 0,8⌉ = 5: nới **20** mỗi đầu. Nhầm hay gặp: bỏ dấu
điểm, coi giờ nằm trong khoảng cũng "sai" một lượng dương.

</details>

**Câu 7.** ACI với α = 0,1, γ = 0,02, $\alpha_t$ = 0,08. Giờ t lỡ, giờ t + 1 trúng. Tính $\alpha_{t+1}$ và $\alpha_{t+2}$.

<details>
<summary>Đáp án</summary>

Lỡ: 0,08 + 0,02 × (0,1 − 1) = 0,08 − 0,018 = **0,062**. Trúng: 0,062 + 0,02 × 0,1 = **0,064** (mục 4.5). Nhầm hay gặp: cộng 0,018 khi lỡ (ngược dấu), làm
khoảng hẹp lại đúng lúc cần rộng.

</details>

**Câu 8.** ACI chạy với α = α₁ = 0,1 và γ = 0,01. Theo bảo đảm của Gibbs & Candès, tỷ lệ lỡ trung bình trên 1.000 giờ có thể lệch khỏi 10% tối đa bao
nhiêu? Trên 10.000 giờ thì sao?

<details>
<summary>Đáp án</summary>

Cận $\frac{\max(0{,}1;\ 0{,}9) + 0{,}01}{0{,}01 \times T}$ (mục 4.5). T = 1.000: 0,91 / 10 = **0,091**, tức tới khoảng 9 điểm phần trăm. T = 10.000: **0,0091**,
chưa tới 1 điểm. Bảo đảm chặt dần theo thời gian: đúng về lâu dài, lỏng trong cửa sổ ngắn. Nhầm hay gặp: nghĩ ACI bảo đảm 90% trong từng tháng.

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Một báo cáo viết: "Split conformal phủ 90,9% trên hai năm kiểm, đạt mục tiêu 90%, đề nghị dùng cho cảnh báo ô nhiễm." Bảng phụ lục của chính
báo cáo:

| Quý | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| coverage | 89,8% | 92,3% | 95,5% | 86,2% |

Tìm chỗ sai trong kết luận.

<details>
<summary>Đáp án</summary>

Con số 90,9% là trung bình của những mùa sai bù nhau (mục 4.2). Quý 4 chỉ phủ 86,2%, trong khi cảnh báo ô nhiễm cần nhất vào mùa đông; trong một số tháng
coverage 30 ngày còn xuống 74,7%. Coverage có điều kiện theo mức ô nhiễm còn tệ hơn: giờ PM2.5 > 150 chỉ 71,8% (mục 4.6). Phải báo coverage trượt theo
thời gian và theo nhóm, và dùng ACI hoặc CQR.

</details>

**Câu 10.** Một đồng nghiệp chạy ACI với bốn giá trị γ trên hai năm kiểm, thấy:

| γ | 0,002 | 0,005 | 0,01 | 0,02 |
|---|---|---|---|---|
| thời gian ngoài dải cho phép | 8,6% | 1,1% | 0% | 0% |
| số giờ khoảng vô hạn | 0 | 7 | 27 | 152 |

Anh ấy chọn γ = 0,01 và báo cáo: "ACI giữ coverage trong dải 100% thời gian". Tìm hai chỗ sai.

<details>
<summary>Đáp án</summary>

1. **Chọn γ trên chính đoạn báo cáo** (mục 4.5): đó là tune trên đoạn kiểm, con số 0% lạc quan (buổi 24). γ phải định trước, từ bài gốc hoặc từ đoạn
   hiệu chỉnh.
2. **Báo cáo bỏ mất cái giá**: γ = 0,01 cho 27 giờ khoảng vô hạn, tức khoảng không nói được gì. Phải báo cả số giờ vô hạn. Khoảng vô hạn luôn "phủ",
   nên nó làm coverage đẹp lên.

</details>
