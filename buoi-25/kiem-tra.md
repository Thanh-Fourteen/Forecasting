# Kiểm tra buổi 25 — Dự báo xác suất

## Nhắc lại khái niệm

**Câu 1.** Vì sao khoảng dựng từ phần dư trên phần học (giả định chuẩn) của LightGBM phủ ít hơn mức danh nghĩa?

- A. Vì mô hình khớp sát dữ liệu đã học, nên phần dư trên phần học nhỏ hơn sai số khi dự báo thật
- B. Vì phân phối chuẩn không bao giờ dùng được cho nhu cầu điện
- C. Vì phần dư ngoài mẫu có rò rỉ tương lai
- D. Vì khoảng 90% luôn phủ ít hơn khoảng 80%

<details>
<summary>Đáp án</summary>

**A** (mục 4.1): độ lệch chuẩn phần dư trên phần học 1.852 MW, sai số ngoài mẫu 2.905 MW; khoảng hẹp hơn sai số thật nên phủ 78,2% thay vì 90%.
**B sai**: giả định chuẩn không phải lỗi chính; dùng độ lệch chuẩn ngoài mẫu với phân phối chuẩn đã gần đúng hơn nhiều. **C sai**: phần dư ngoài mẫu
lấy từ các tháng trước tháng dự báo, không dùng số tương lai. **D sai**: khoảng 90% rộng hơn nên phủ nhiều hơn khoảng 80%.

</details>

**Câu 2.** Một mô hình được học bằng cách tối thiểu pinball loss với τ = 0,9. Nó sẽ dự báo gì?

- A. Trung bình của thực tế
- B. Trung vị của thực tế
- C. Quantile 0,9 của thực tế: mốc mà khoảng 90% số lần thực tế nằm dưới
- D. Giá trị lớn nhất từng gặp

<details>
<summary>Đáp án</summary>

**C** (mục 4.2): đoán thấp bị phạt 0,9 lần phần thiếu, đoán cao chỉ 0,1 lần phần thừa, nên dự báo nhích lên tới khi chỉ 10% số lần thực tế còn vượt.
Ví dụ tay: mười số 1 … 10 với τ = 0,8 cho tổng phạt nhỏ nhất ở q từ 8 tới 9. **A sai**: trung bình là thứ tối thiểu sai số bình phương. **B sai**:
trung vị ứng với τ = 0,5. **D sai**: đoán giá trị lớn nhất bị phạt 0,1 lần phần thừa ở gần như mọi lần, tổng phạt lớn hơn.

</details>

**Câu 3.** Trong CRPS từ mẫu, vế "trừ một nửa trung bình |X − X'|" có vai trò gì?

- A. Thưởng cho mẫu có độ trải vừa đủ; thiếu vế này, mẫu co cụm về một điểm luôn có điểm tốt nhất
- B. Đổi đơn vị của CRPS sang phần trăm
- C. Phạt mẫu quá rộng
- D. Bảo đảm CRPS luôn âm

<details>
<summary>Đáp án</summary>

**A** (mục 4.3): vế đầu (khoảng cách tới thực tế) nhỏ nhất khi mọi phần tử dồn vào một điểm gần thực tế; vế sau bù lại độ trải. Ví dụ tay: mẫu
(2, 4, 6) với thực tế 5 có CRPS 0,778, tốt hơn dự báo một số 4 (CRPS 1). **B sai**: CRPS giữ đơn vị của dữ liệu (MW). **C sai**: vế này làm CRPS
nhỏ đi khi mẫu trải rộng; mẫu quá rộng bị phạt qua vế đầu. **D sai**: CRPS luôn ≥ 0.

</details>

**Câu 4.** PIT histogram của một mô hình có hình vòm: hai đầu thấp, giữa cao. Chẩn đoán nào đúng?

- A. Quá tự tin: khoảng quá hẹp
- B. Quá thận trọng: khoảng quá rộng
- C. Dự báo thấp hơn thực tế một cách có hệ thống
- D. Calibrate tốt

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): ít giờ rơi vào hai đầu (dưới quantile 0,05, trên quantile 0,95) nghĩa là khoảng rộng hơn cần thiết. Ví dụ thật: "mượn khoảng seasonal
naive" chỉ 0,6% giờ dưới quantile 0,05. **A sai**: quá tự tin cho chữ U (hai đầu cao). **C sai**: dự báo thấp cho histogram dốc lên về phía phải.
**D sai**: calibrate thì mọi cột gần 1.

</details>

## Vận dụng

**Câu 5.** τ = 0,1, thực tế 50. Tính pinball loss của dự báo 60 và của dự báo 40. Dự báo nào tốt hơn, và vì sao điều đó hợp với τ = 0,1?

<details>
<summary>Đáp án</summary>

Dự báo 60 cao hơn thực tế 10: phạt (1 − 0,1) × 10 = **9**. Dự báo 40 thấp hơn 10: phạt 0,1 × 10 = **1** (mục 4.2). Dự báo 40 tốt hơn: quantile 0,1
là mốc thấp (chỉ 10% số lần thực tế nằm dưới), nên đoán cao bị phạt nặng. Nhầm hay gặp: nhân phần thừa với τ, ra 1 và 9 ngược lại.

</details>

**Câu 6.** Mẫu dự báo (1, 5, 6), thực tế 4. CRPS bằng bao nhiêu?

- A. 2
- B. khoảng 0,889
- C. khoảng 1,111
- D. khoảng 3,111

<details>
<summary>Đáp án</summary>

**B** (mục 4.3). Vế đầu: (3 + 1 + 2) / 3 = 2. Vế sau: 9 cặp, khoảng cách 0, 4, 5, 4, 0, 1, 5, 1, 0, tổng 20; 20 / 9 ≈ 2,222; một nửa ≈ 1,111.
CRPS ≈ 2 − 1,111 = 0,889. **A sai**: chỉ tính vế đầu (lỗi của `crps_mau` trong `code/`). **C sai**: chỉ lấy vế sau. **D sai**: cộng thay vì trừ.

</details>

**Câu 7.** Trung vị 20, khoảng 80% là [15; 24], thực tế 26. Tính interval score của khoảng và WIS (K = 1).

<details>
<summary>Đáp án</summary>

Khoảng 80% nên α = 0,2. Thực tế vượt cận trên 2: $IS_{0,2}$ = (24 − 15) + (2 / 0,2) × 2 = 9 + 20 = **29**. WIS = (0,5 × |26 − 20| + 0,1 × 29) / 1,5 =
(3 + 2,9) / 1,5 ≈ **3,93** (mục 4.3). Nhầm hay gặp: phạt phần vượt 2 lần thay vì 2/α = 10 lần; hoặc quên chia (K + ½).

</details>

**Câu 8.** Phần vượt ngưỡng 30 °C của một thành phố khớp GPD với ξ = 0, σ = 2 °C; trung bình 2 đợt vượt mỗi năm. Mức 10 năm là bao nhiêu? (Cho
sẵn ln 20 ≈ 3,0.)

<details>
<summary>Đáp án</summary>

ξ = 0 nên $x_N = u + \sigma \ln(\lambda N)$ = 30 + 2 × ln(2 × 10) ≈ 30 + 2 × 3,0 = **36 °C** (mục 4.5). Mỗi năm có khoảng 10% khả năng vượt 36 °C.
Nhầm hay gặp: dùng ln 10 (quên nhân λ = 2 đợt mỗi năm), ra khoảng 34,6 °C.

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Một đồng nghiệp kiểm dự báo quantile của mô hình X trên một năm:

| Kiểm | Kết quả |
|---|---|
| phủ khoảng 80% (quantile 0,1–0,9) | 80,4% |
| phủ khoảng 90% (quantile 0,05–0,95) | 89,9% |
| tỷ lệ giờ nằm dưới quantile 0,05 | 1,5% |
| tỷ lệ giờ nằm dưới quantile 0,5 | 37% |
| tỷ lệ giờ nằm dưới quantile 0,95 | 91,4% |

Kết luận: "Coverage 80% và 90% đều đúng, mô hình calibrate tốt". Điều gì sai?

- A. Không sai: hai mức coverage đạt là đủ
- B. Chỉ 37% giờ nằm dưới trung vị (lẽ ra 50%) và 1,5% dưới quantile 0,05 (lẽ ra 5%): cả phân phối nằm thấp, PIT sẽ dốc lên; coverage hai khoảng không bắt được lỗi này
- C. Khoảng quá rộng vì 91,4% nằm dưới quantile 0,95
- D. Phải dùng WIS thay cho mọi bảng calibration

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): dự báo lệch thấp, nhiều giờ vượt các quantile; khoảng vừa đủ rộng nên coverage vẫn gần đúng. Giống dòng "không trừ mức" ở bảng mục 4.4.
**A sai**: calibration phải đúng ở từng mức. **C sai**: 91,4% dưới quantile 0,95 nghĩa là 8,6% vượt, nhiều hơn 5%, không phải quá rộng. **D sai**: WIS
là điểm tổng, không chỉ ra hình dạng lỗi; mục 4.3 cho thấy WIS gần như không phân biệt mô hình calibrate kém.

</details>

**Câu 10.** Bảng so hai cách dựng khoảng 90% trên năm 2025:

| Cách | Phủ khoảng 90% | Rộng khoảng 90% (MW) | WIS |
|---|---|---|---|
| P | 78,2% | 6.092 | 1.412 |
| Q | 88,8% | 9.425 | 1.408 |

Kết luận: "WIS gần bằng nhau, vậy chọn P vì khoảng hẹp hơn, sắc hơn". Tìm chỗ sai.

<details>
<summary>Đáp án</summary>

P không calibrate: nói 90% mà chỉ phủ 78,2% (mục 4.4). Nguyên tắc là **sắc nhất trong số các mô hình đã calibrate**, nên chọn Q. WIS gần bằng nhau không
có nghĩa hai cách tốt như nhau: WIS gộp độ rộng và phần lỡ thành một số, nên bù trừ được lẫn nhau (mục 4.3). Người vận hành dựa vào khoảng P sẽ bị bất
ngờ gấp đôi số lần đã hứa (21,8% so với 10%).

</details>
