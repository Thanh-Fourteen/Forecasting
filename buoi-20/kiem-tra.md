# Kiểm tra buổi 20 — Đa biến, state space và nowcasting

## Nhắc lại khái niệm

**Câu 1.** Hai chuỗi giá đồng liên kết (cointegration) nghĩa là:

- A. Hai chuỗi đều dừng
- B. Hai chuỗi không dừng, nhưng một tổ hợp tuyến tính của chúng (spread) dừng
- C. Hai chuỗi có tương quan trên 0,9
- D. Hai chuỗi có cùng mùa vụ

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): từng chuỗi trôi đi, còn khoảng cách giữa chúng quay về mức cân bằng, như người dắt chó. **A sai**: chuỗi dừng thì không cần
khái niệm này. **C sai**: hai chuỗi cùng trôi có tương quan cao mà không đồng liên kết (hồi quy giả, buổi 18). **D sai**: mùa vụ không liên quan.

</details>

**Câu 2.** Dầu và xăng đồng liên kết. Vì sao VECM có thể dự báo xăng tốt hơn VAR trên sai phân?

- A. VECM có nhiều trễ hơn
- B. VECM có số hạng kéo spread về cân bằng; VAR trên sai phân bỏ mất thông tin "xăng đang cao hay thấp so với dầu"
- C. VECM không cần dữ liệu dừng nên dùng được giá gốc
- D. VECM luôn tốt hơn VAR

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): sai phân chỉ giữ thay đổi, mất mức; số hạng $\alpha \times$ spread đưa thông tin mức trở lại. **A sai**: cả hai dùng cùng số trễ
ở buổi này. **C sai**: VECM vẫn dựa trên chuỗi sai phân dừng và spread dừng. **D sai**: không có cointegration thì số hạng kéo về vô nghĩa; và
ngay ở đây DM chưa cho thấy chắc chắn VECM hơn (p 0,17).

</details>

**Câu 3.** Trong bộ lọc Kalman, hệ số $K$ gần 1 nghĩa là:

- A. Tin gần như hoàn toàn vào số đo mới, vì dự đoán kém chắc hơn nhiều so với số đo
- B. Bỏ qua số đo
- C. Mô hình sai
- D. Không có dữ liệu thiếu

<details>
<summary>Đáp án</summary>

**A** (mục 4.3): $K = P / (P + \sigma^2_\varepsilon)$ gần 1 khi $P$ (bất định của dự đoán) lớn hơn nhiều so với nhiễu đo. **B sai**: đó là $K$ gần 0.
**C sai**: $K$ chỉ cân hai nguồn tin, không nói mô hình đúng sai. **D sai**: khi thiếu số đo thì không tính $K$ (bỏ bước cập nhật).

</details>

**Câu 4.** Vì sao backtest nowcast GDP phải đọc vintage của đúng ngày nowcast?

- A. Vì bản mới nhất bị lỗi định dạng
- B. Vì số liệu bị sửa sau khi công bố; bản mới nhất chứa thông tin chưa có lúc nowcast, kể cả những tháng chỉ báo chưa về
- C. Vì vintage cũ chính xác hơn
- D. Vì tệp mới nhất quá lớn

<details>
<summary>Đáp án</summary>

**B** (mục 4.6): dùng bản 12/2025 thì ngay tháng đầu quý mô hình đã "thấy" đủ ba tháng chỉ báo, RMSE giả tạo 1,19 thay vì 1,44. **A, D sai**:
không liên quan định dạng hay dung lượng. **C sai**: vintage cũ không chính xác hơn — nó là thứ người dự báo có trong tay lúc đó.

</details>

## Vận dụng

**Câu 5.** VAR 4 biến, 2 trễ có bao nhiêu hệ số (chưa kể hằng số)? Với 60 quý dữ liệu, mỗi phương trình ước lượng bao nhiêu hệ số? Lên 8
biến, 2 trễ thì sao?

<details>
<summary>Đáp án</summary>

4² × 2 = **32** hệ số, mỗi phương trình **8** hệ số trên khoảng 58 quan sát (mục 4.1). Lên 8 biến: 8² × 2 = **128** hệ số, mỗi phương trình **16** —
số hệ số tăng theo bình phương số biến, trong khi số quý thì không đổi, nên VAR lớn dễ học thuộc nhiễu.
Nhầm hay gặp: tính 4 × 2 = 8, quên có 4 phương trình.

</details>

**Câu 6.** Local level: nhiễu đo phương sai 4, cú dời phương sai 1. Ước lượng hiện tại: mức 20, phương sai 3. Năm nay đo được 26. Tính mức và
phương sai mới. Năm sau không đo được: mức và phương sai?

<details>
<summary>Đáp án</summary>

Dự báo: phương sai 3 + 1 = 4; $K$ = 4 / (4 + 4) = 0,5; mức 20 + 0,5 × 6 = **23**; phương sai 0,5 × 4 = **2**. Năm sau thiếu số đo: mức **23**,
phương sai 2 + 1 = **3** (mục 4.3). Nhầm hay gặp: cập nhật bằng số đo 0 khi thiếu.

</details>

**Câu 7.** Cân bằng: log xăng = 0,2 + 0,8 × log dầu. Tuần này log dầu 3,0, log xăng 2,9. Hệ số kéo về $\alpha$ = −0,1. Spread và phần kéo về
của tuần tới?

<details>
<summary>Đáp án</summary>

Cân bằng 0,2 + 2,4 = 2,6; spread = 2,9 − 2,6 = **0,3**; kéo về −0,1 × 0,3 = **−0,03** (log, tức khoảng −3%) (mục 4.2). Nhầm hay gặp: tính spread
là 2,9 − 3,0 mà quên hệ số và hằng số.

</details>

**Câu 8.** Bridge: GDP (% năm) = 0,8 + 1,2 × việc làm quý (% năm). Giữa tháng 3: việc làm tháng 1 tăng 0,15%, tháng 2 tăng 0,25%; tháng 3 dự báo
0,20%. Nowcast GDP?

<details>
<summary>Đáp án</summary>

Việc làm quý ≈ (0,15 + 0,25 + 0,20) × 4 = 2,4% năm hoá; GDP ≈ 0,8 + 1,2 × 2,4 = **3,68%** (mục 4.5). Nhầm hay gặp: quên năm hoá, ra 0,8 + 0,72 =
1,52.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo nowcast GDP 2005–2019:

| Thời điểm | Tháng 1 | Tháng 2 | Tháng 3 | Tháng đầu quý sau |
|---|---|---|---|---|
| RMSE bridge | 1,19 | 1,19 | 1,19 | 1,19 |

"Mô hình rất tốt: ngay tháng đầu quý đã chính xác như lúc có đủ số liệu." Chỉ ra lỗi.

<details>
<summary>Đáp án</summary>

Sai số không đổi theo tháng nghĩa là mô hình không hề "chờ" số liệu: nó đọc bảng số liệu mới nhất, đã có đủ ba tháng chỉ báo (và số đã sửa) ngay
từ tháng 1 (mục 4.6). Nowcast thật bằng vintage cho 1,44 → 1,17, giảm dần. Phải đọc vintage của đúng ngày nowcast. Nhầm hay gặp: coi sai số
phẳng là dấu hiệu mô hình ổn định.

</details>

**Câu 10.** Backtest 104 tuần dự báo giá xăng:

| Tầm 4 tuần | naive | VECM |
|---|---|---|
| MAE (%) | 6,78 | 6,44 |
| DM so với naive | — | p = 0,17 |

"VECM tốt hơn naive 5%, dùng nó để mua xăng trước khi giá lên." Nhận xét.

<details>
<summary>Đáp án</summary>

Chênh 5% nhưng DM p = 0,17: chưa có bằng chứng VECM thật sự tốt hơn (mục 4.2; buổi 15). Giá gần như bước ngẫu nhiên; cointegration chỉ cho biết
spread sẽ quay về, không cho biết giá tuyệt đối đi đâu. Muốn dùng để quyết định mua thì cần thêm dữ liệu kiểm và đo bằng lời lỗ thật. Nhầm hay
gặp: đọc chênh MAE mà không đọc DM.

</details>
