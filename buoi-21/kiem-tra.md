# Kiểm tra buổi 21 — Chuỗi tài chính và biến động

## Nhắc lại khái niệm

**Câu 1.** Vì sao mô hình hoá lợi suất thay vì giá?

- A. Vì giá không có dữ liệu theo giờ
- B. Vì lợi suất không phụ thuộc mức giá và gần như dừng; giá thì không dừng
- C. Vì lợi suất luôn dương
- D. Vì lợi suất dự báo được còn giá thì không

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): 1% ở giá 40 nghìn hay 90 nghìn là như nhau; lợi suất dao động quanh 0, mô hình hoá được. **A sai**: giá có mọi tần suất. **C sai**:
lợi suất âm khi giá giảm. **D sai**: bản thân lợi suất cũng gần như không đoán được (ACF trễ 1 khoảng −0,02); cái đoán được là độ lớn của nó.

</details>

**Câu 2.** "Cụm biến động" thể hiện trên số liệu thế nào?

- A. ACF của lợi suất lớn
- B. ACF của lợi suất gần 0, nhưng ACF của bình phương lợi suất dương rõ
- C. Lợi suất có phân phối chuẩn
- D. Giá tăng đều

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): trên JPY/USD, ACF trễ 1 của lợi suất −0,02, của bình phương 0,09, vượt ngưỡng ở mọi trễ đầu. **A sai**: đó sẽ là dự báo được
hướng. **C sai**: đuôi dày hơn chuẩn nhiều. **D sai**: không liên quan tới xu hướng giá.

</details>

**Câu 3.** Một bài báo cáo mô hình dự báo giá có R² = 0,99. Điều đó nói gì?

- A. Mô hình dự báo đúng 99% số ngày
- B. Gần như không nói gì: dự báo "giá hôm qua" cũng có R² gần 1 trên giá; phải so với naive
- C. Mô hình tốt hơn naive 99%
- D. Giá có tính dừng

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): R² ≈ 1 − (sai số / độ lệch chuẩn giá)²; giá dao động rộng trong năm nên naive cũng đạt 0,984 trên BTC 2024. **A sai**: R² không
phải tỷ lệ ngày đúng. **C sai**: R² không so với naive; trên BTC, demo R² 0,988 còn thua naive (MAE 1.649 so với 887). **D sai**: R² cao trên giá
chính vì giá không dừng.

</details>

**Câu 4.** Kiểm định Kupiec kiểm điều gì?

- A. Lợi suất có phân phối chuẩn không
- B. Tỷ lệ số ngày lỗ vượt VaR có khớp tỷ lệ đã hứa (1% với VaR 99%) không
- C. GARCH có tốt hơn HAR không
- D. Có cụm biến động không

<details>
<summary>Đáp án</summary>

**B** (mục 4.6): so $x/n$ với $p$; vượt quá nhiều hoặc quá ít đều bị bác. **A sai**: đó là kiểm định phân phối. **C sai**: so dự báo biến động dùng
QLIKE, MSE, DM. **D sai**: đó là ACF của bình phương lợi suất.

</details>

## Vận dụng

**Câu 5.** Giá 200 → 210 → 189. Tính hai lợi suất log và lợi suất log cả hai ngày.

<details>
<summary>Đáp án</summary>

100 × ln(210/200) = **4,88%**; 100 × ln(189/210) = **−10,54%**; cộng lại **−5,66%** = 100 × ln(189/200) (mục 4.1). Nhầm hay gặp: tính phần
trăm thường (+5%, −10%) rồi cộng ra −5%, lệch với thay đổi thật.

</details>

**Câu 6.** GARCH(1,1): $\omega$ = 0,05, $\alpha$ = 0,08, $\beta$ = 0,90. Hôm nay phương sai 2, cú sốc −4. Phương sai ngày mai và mức dài hạn?

<details>
<summary>Đáp án</summary>

0,05 + 0,08 × 16 + 0,90 × 2 = **3,13**; dài hạn 0,05 / (1 − 0,98) = **2,5** (mục 4.4). Cú sốc lớn đẩy phương sai lên, rồi dần về 2,5. Nhầm hay
gặp: dùng cú sốc −4 thay vì bình phương 16.

</details>

**Câu 7.** Trung bình lợi suất 0, độ lệch chuẩn dự báo cho mai 1,5%. Tính VaR 99% nếu cú sốc chuẩn (quantile −2,33) và nếu Student-t đã chuẩn hoá
(quantile −2,57). Danh mục 1 tỷ đồng thì mức lỗ VaR bao nhiêu?

<details>
<summary>Đáp án</summary>

Chuẩn: −2,33 × 1,5 = **−3,495%** (lỗ khoảng 35 triệu). Student-t: −2,57 × 1,5 = **−3,86%** (38,6 triệu) (mục 4.6). Đuôi dày làm VaR xa hơn. Nhầm hay
gặp: dùng 1,96 (khoảng 95% hai phía) thay vì 2,33 (1% một phía).

</details>

**Câu 8.** Sáu khoảng trong ngày có lợi suất 0,3; −0,4; 0,2; −0,1; 0,5; −0,5 (%). Tính lợi suất cả ngày, bình phương của nó, và RV.

<details>
<summary>Đáp án</summary>

Lợi suất ngày 0,3 − 0,4 + 0,2 − 0,1 + 0,5 − 0,5 = **0**, bình phương 0. RV = 0,09 + 0,16 + 0,04 + 0,01 + 0,25 + 0,25 = **0,80** (mục 4.5). Ngày có
biến động dù đóng cửa bằng giá mở. Nhầm hay gặp: lấy bình phương lợi suất ngày làm biến động của ngày.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một bài đăng khoe:

| Mô hình | R² trên tập kiểm |
|---|---|
| mạng nơ-ron 10 ngày → giá mai (dữ liệu chuẩn hoá về [0, 1], chia ngẫu nhiên 80/20) | 0,988 |

"Chính xác gần 99%, dùng để giao dịch." Chỉ ra ba lỗi.

<details>
<summary>Đáp án</summary>

(1) Không có dòng naive: trên cùng dữ liệu, "giá hôm qua" có R² 0,996 và MAE 887 so với 1.649 của mô hình (mục 4.3). (2) Chia ngẫu nhiên cho mô hình
thấy ngày sau của ngày cần đoán (buổi 15). (3) Chuẩn hoá bằng min, max của cả chuỗi để thông tin tương lai lọt vào (buổi 13). Chấm trung thực:
học 2023, chấm 2024, so naive bằng DM: mô hình thua (p 5·10⁻¹⁰), đoán đúng chiều 52,5%. Nhầm hay gặp: tin hình hai đường trùng nhau.

</details>

**Câu 10.** Báo cáo rủi ro:

| VaR 99% một ngày, 1.249 ngày | Số lần vượt | Kỳ vọng |
|---|---|---|
| mô hình của phòng rủi ro | 3 | 12,5 |

"Chỉ vượt 3 lần, mô hình rất an toàn." Nhận xét.

<details>
<summary>Đáp án</summary>

Vượt 3 lần thay vì khoảng 12: VaR **quá thận trọng**; Kupiec LR ≈ 10,5, trên ngưỡng 3,84, nên bác (mục 4.6). Hậu quả: giữ vốn dự phòng thừa, tốn chi
phí. VaR tốt bị vượt đúng khoảng 1% số ngày. Nhầm hay gặp: nghĩ càng ít lần vượt càng tốt.

</details>
