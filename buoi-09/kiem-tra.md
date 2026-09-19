# Kiểm tra buổi 9 — Đặc trưng chuỗi và khả năng dự báo

## Nhắc lại khái niệm

**Câu 1.** Spectral entropy của một chuỗi gần 0 nghĩa là:

- A. Năng lượng của chuỗi dồn vào ít tần số: chuỗi có nhịp rõ, dễ dự báo
- B. Chuỗi gần như nhiễu thuần, khó dự báo
- C. Các giá trị của chuỗi gần bằng 0
- D. Dự báo seasonal naive gần như không sai

<details>
<summary>Đáp án</summary>

**A** (mục 4.2): entropy đo năng lượng trải đều trên các tần số tới đâu; dồn hết vào một tần số cho 0. **B sai**: đó là entropy gần 1.
**C sai**: code trừ trung bình và bỏ tần số 0 trước khi tính, nên mức của chuỗi không ảnh hưởng. **D sai**: entropy thấp gợi ý dễ, nhưng
không phải sai số; chuỗi có xu hướng mạnh có entropy thấp mà seasonal naive vẫn có thể sai nhiều.

</details>

**Câu 2.** Nhân mọi giá trị của một chuỗi với 1.000 (đổi nghìn đồng thành đồng). Đặc trưng nào **đổi**?

- A. Hệ số biến thiên
- B. $r_1$
- C. Độ lệch chuẩn
- D. Spectral entropy

<details>
<summary>Đáp án</summary>

**C** (mục 4.1): độ lệch chuẩn nhân lên 1.000 lần, như trung bình; hai đặc trưng quy mô này chỉ để tham chiếu. **A sai**: CV là tỷ số, tử và
mẫu cùng nhân 1.000. **B sai**: tử số và mẫu số của $r_1$ cùng nhân 1.000². **D sai**: phần năng lượng của mỗi tần số là tỷ lệ, không đổi.

</details>

**Câu 3.** Vì sao MASE của **chính** seasonal naive nằm quanh 1 ở gần như mọi chuỗi?

- A. Vì seasonal naive luôn là mô hình tốt nhất
- B. Vì mẫu số của MASE là sai số của seasonal naive trên phần học, nên độ khó của chuỗi có mặt ở cả tử lẫn mẫu
- C. Vì MASE chỉ dùng được cho chuỗi dương
- D. Vì 18 tháng chấm quá ngắn

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): chuỗi nhiễu thì tử và mẫu cùng lớn, chuỗi đều thì cùng nhỏ, tỷ số gần 1. **A sai**: MASE ≈ 1 nói seasonal naive trên kỳ chấm
sai cỡ như trên phần học, không nói nó tốt nhất. **C sai**: đó là giới hạn của sMAPE, không phải MASE. **D sai**: đổi tầm chấm không đổi
được việc mẫu số chứa chính độ khó.

</details>

**Câu 4.** Kourentzes phản bác việc dùng hệ số biến thiên (CV) làm trục XYZ vì:

- A. Chuỗi mùa vụ đều đặn có CV cao nhưng dự báo rất dễ
- B. CV không tính được cho doanh thu
- C. CV luôn giống hệt ABC
- D. Ngưỡng 0,5 và 1,0 quá cao

<details>
<summary>Đáp án</summary>

**A** (mục 4.6, ví dụ mã $P$: CV 0,58, seasonal naive không sai chút nào). **B sai**: CV tính được cho mọi chuỗi có trung bình khác 0.
**C sai**: CV trung vị có tăng từ A sang C, nhưng hai trục khác nhau (có ô AX lẫn AZ). **D sai**: ngưỡng chỉ là quy ước; đổi ngưỡng không sửa
được việc CV đo dao động chứ không đo độ khó.

</details>

## Vận dụng

**Câu 5.** Phổ của một chuỗi có 3 tần số với phần năng lượng 0,5; 0,25; 0,25. Tính spectral entropy (lấy $\ln 3 \approx 1{,}099$). Chuỗi
gần nhiễu hay có nhịp rõ?

<details>
<summary>Đáp án</summary>

$-(0{,}5 \ln 0{,}5 + 2 \times 0{,}25 \ln 0{,}25) = 0{,}347 + 0{,}693 = 1{,}040$; chia $\ln 3$: $1{,}040 / 1{,}099 \approx$ **0,95**. Gần 1:
năng lượng khá đều trên cả ba tần số, chuỗi gần nhiễu (mục 4.2). Nhầm hay gặp: chia cho $\ln 4$ hay quên chia, ra 1,04 (lớn hơn 1 là dấu
hiệu tính sai).

</details>

**Câu 6.** Chuỗi chu kỳ $m$ = 2, phần học 100, 120, 104, 124; kỳ chấm thực tế 108, 128. Dự báo seasonal naive là 104, 124. Tính MASE và
sMAPE. MASE = 1 có nghĩa chuỗi này "khó trung bình" không?

<details>
<summary>Đáp án</summary>

Mẫu số MASE: \|104 − 100\| và \|124 − 120\| → 4. Sai số kỳ chấm 4 và 4 → MAE 4. MASE = 4/4 = **1**. sMAPE = (200 × 4/212 + 200 × 4/252) / 2 =
(3,77 + 3,17) / 2 ≈ **3,5%**: chuỗi dễ (mục 4.3). MASE = 1 chỉ nói kỳ chấm sai cỡ như phần học, **không** nói chuỗi khó hay dễ. Nhầm hay
gặp: đọc MASE = 1 thành "khó".

</details>

**Câu 7.** Hai chuỗi 2, 4, 2 và 20, 40, 20. DTW trên giá trị gốc là 44,1. Bạn phân cụm và chúng vào hai cụm khác nhau. Sai ở đâu? Sau khi
sửa, DTW bằng bao nhiêu?

<details>
<summary>Đáp án</summary>

Hai chuỗi cùng hình dạng, chỉ khác độ lớn; DTW so **giá trị** nên coi chúng rất khác (mục 4.5). Sửa: chuẩn hoá z-score từng chuỗi trước.
Cả hai thành −0,71; 1,41; −0,71, nên DTW = **0**, vào cùng cụm. Nhầm hay gặp: tăng cửa sổ Sakoe–Chiba; cửa sổ chỉ cho lệch thời gian, không
bù được chênh lệch độ lớn.

</details>

**Câu 8.** Ba chuỗi: $U$ có entropy 0,80 và $F_S$ 0,20; $V$ có entropy 0,80 và $F_S$ 0,70; $W$ có entropy 0,30 và $F_S$ 0,10. Theo quy tắc
của buổi (entropy ≥ 0,666 **và** $F_S$ < 0,4), chuỗi nào "dùng baseline"? Vì sao không tách theo một đặc trưng?

<details>
<summary>Đáp án</summary>

Chỉ **$U$** (mục 4.4). $V$ entropy cao nhưng mùa vụ mạnh: vẫn có nhịp để mô hình khai thác. $W$ mùa vụ yếu nhưng entropy thấp: có cấu trúc
khác (ví dụ xu hướng). Ghép hai điều kiện để chỉ gạt ra chuỗi vừa giống nhiễu vừa không có mùa vụ; trong 4.000 chuỗi, nhóm này (137 chuỗi)
có sMAPE trung vị 18,11%, gấp ba phần còn lại. Nhầm hay gặp: gạt mọi chuỗi entropy cao, bỏ luôn những chuỗi mùa vụ mạnh đáng mô hình tốt.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo viết: "Spectral entropy vô dụng để đoán độ khó: Pearson với MASE của seasonal naive chỉ −0,05, và trung vị MASE theo
5 nhóm ngũ phân vị entropy là 1,02 / 0,95 / 1,01 / 1,02 / 1,02." Chỉ ra lỗi và nói phải báo gì thêm.

<details>
<summary>Đáp án</summary>

Lỗi: dùng MASE của **chính** seasonal naive để so độ khó giữa các chuỗi. Mẫu số đã chứa độ khó, nên MASE quanh 1 ở mọi nhóm, và dãy 1,02 /
0,95 / … là bằng chứng của điều đó, không phải của "entropy vô dụng" (mục 4.3). Phải báo thêm sMAPE (Pearson +0,245, Spearman +0,216; trung
vị nhóm cao nhất 12,0%, gấp đôi các nhóm khác) và cả hai hệ số tương quan, kèm tên thước đo trong mọi kết luận.

</details>

**Câu 10.** Bảng phân cụm DTW 300 chuỗi thành 4 cụm:

| Cụm | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Số chuỗi | 78 | 102 | 72 | 48 |
| Mức trung vị | 1.585 | 3.310 | 6.835 | 9.832 |

Nhóm phân tích kết luận: "Bốn cụm là bốn kiểu hành vi thị trường khác nhau, mỗi cụm cần một mô hình riêng." Nhận xét, và nói cách kiểm.

<details>
<summary>Đáp án</summary>

Mức trung vị **tăng đều** theo số cụm: phân cụm chỉ đang xếp chuỗi theo độ lớn, vì chưa chuẩn hoá z-score trước DTW (mục 4.5). Bốn cụm là
"nhỏ, vừa, lớn, rất lớn", không phải bốn hình dạng. Cách kiểm: (1) chuẩn hoá rồi phân cụm lại, mức trung vị theo cụm phải lộn xộn; (2) nhân
một chuỗi với 100, nhãn cụm phải giữ nguyên. Nhầm hay gặp: chỉ nhìn số chuỗi mỗi cụm (khá cân) rồi tin cụm có ý nghĩa.

</details>
