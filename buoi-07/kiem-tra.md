# Kiểm tra buổi 7 — Tự tương quan và tính dừng

## Nhắc lại khái niệm

**Câu 1.** Giả thuyết $H_0$ của ADF và của KPSS lần lượt là:

- A. Dừng; có nghiệm đơn vị
- B. Có nghiệm đơn vị; dừng
- C. Cả hai đều là "dừng"
- D. Cả hai đều là "có nghiệm đơn vị"

<details>
<summary>Đáp án</summary>

**B** (mục 4.5). ADF: $H_0$ là có nghiệm đơn vị (không dừng), p nhỏ là bằng chứng **dừng**. KPSS: $H_0$ là dừng, p nhỏ là bằng chứng
**không dừng**. **A sai**: đảo ngược cả hai; nhớ ngược là đọc sai mọi bảng kết quả. **C, D sai**: hai kiểm định được dùng cùng nhau chính
vì $H_0$ của chúng ngược nhau, để có bảng 2 × 2.

</details>

**Câu 2.** ACF của một chuỗi giảm rất chậm, còn 0,53 ở trễ 30. Điều này gợi ý:

- A. Mùa vụ chu kỳ 30
- B. Chuỗi chưa dừng (xu hướng hoặc random walk)
- C. Nhiễu trắng
- D. Sai phân thừa

<details>
<summary>Đáp án</summary>

**B** (mục 4.1, bảng mục 4.2: random walk có $r_{30}$ = 0,530). **A sai**: mùa vụ cho **đỉnh** ở bội số chu kỳ, không phải giảm đều.
**C sai**: nhiễu trắng có $r_k$ quanh 0. **D sai**: sai phân thừa cho $r_1$ âm gần −0,5, không phải dương và giảm chậm.

</details>

**Câu 3.** Vì sao không nên kết luận "có tự tương quan" chỉ vì một cột ACF trong 20 trễ vượt dải ±1,96/√T?

- A. Vì dải vẽ sai
- B. Vì với nhiễu trắng, trung bình đã có gần 1 cột vượt, và 62% số chuỗi có ít nhất một cột vượt
- C. Vì ACF không dùng để xem tự tương quan
- D. Vì phải dùng PACF thay cho ACF

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): mỗi cột có 5% khả năng vượt dải dù chuỗi là nhiễu thuần, 20 cột thì trung bình 20 × 0,05 = 1 cột. Dùng **Ljung-Box**.
**A sai**: dải đúng, chỉ là cách dùng sai. **C sai**: ACF chính là thước đo tự tương quan. **D sai**: PACF cũng có dải và cùng vấn đề đếm
cột.

</details>

**Câu 4.** Chuỗi dừng quanh xu hướng (đường thẳng + nhiễu) nên được xử lý bằng:

- A. Sai phân một lần
- B. Sai phân hai lần
- C. Khử xu hướng: trừ đường thẳng khớp nhất theo thời gian
- D. Lấy log

<details>
<summary>Đáp án</summary>

**C** (bảng mục 4.4). **A sai**: sai phân nó là sai phân thừa, thêm tương quan âm giả (mục 4.6); trong bảng mục 4.5, chuỗi xu hướng dạng
"ct" đã dừng quanh xu hướng. **B sai**: càng thừa hơn. **D sai**: log chỉ đổi thang, không bỏ được đường xu hướng.

</details>

## Vận dụng

**Câu 5.** Tính $r_1$ cho chuỗi 2, 4, 6, 8, 6, 4, 2, 0.

<details>
<summary>Đáp án</summary>

Trung bình 32/8 = 4. Độ lệch: −2, 0, 2, 4, 2, 0, −2, −4. Mẫu số: 4 + 0 + 4 + 16 + 4 + 0 + 4 + 16 = 48. Tử số trễ 1 (7 cặp, mỗi số nhân số
ngay trước): 0 × (−2) + 2 × 0 + 4 × 2 + 2 × 4 + 0 × 2 + (−2) × 0 + (−4) × (−2) = 0 + 0 + 8 + 8 + 0 + 0 + 8 = 24. $r_1$ = 24/48 = **0,5**.
Dương vì chuỗi đi lên rồi đi xuống từ từ, số liền nhau hay cùng phía trung bình. Nhầm hay gặp: chia cho số cặp (7) thay vì tổng bình
phương độ lệch.

</details>

**Câu 6.** Trên một chuỗi: dạng "c" có ADF p = 0,906, KPSS p ≤ 0,01; dạng "ct" có ADF p = 0,000, KPSS p ≥ 0,10. Kết luận và cách xử lý?

<details>
<summary>Đáp án</summary>

Dạng "c": ô **không dừng**. Dạng "ct": ô **dừng** (quanh xu hướng thẳng). Chuỗi dừng quanh xu hướng, chính là chuỗi 0,05 × t + nhiễu
trong bảng mục 4.5. Xử lý: khử xu hướng hoặc đưa thời gian $t$ vào mô hình, **không** sai phân. Nhầm hay gặp: chỉ chạy dạng "c" rồi sai phân.

</details>

**Câu 7.** Sai phân lần thứ hai làm $r_1$ = −0,49 và độ lệch chuẩn tăng từ 1,11 lên 1,46. Chuyện gì xảy ra, làm gì tiếp?

<details>
<summary>Đáp án</summary>

**Sai phân thừa** (mục 4.6): đủ cả hai dấu hiệu, $r_1$ gần −0,5 và độ lệch chuẩn tăng. Quay lại một lần sai phân. Nếu KPSS vẫn bác bỏ thì
tìm nguyên nhân khác (độ dao động đổi theo thời gian, cú sốc, đổi mức đột ngột) thay vì sai phân thêm. Đây đúng là số của tăng trưởng GDP
trong buổi.

</details>

**Câu 8.** Chuỗi lượt thuê theo giờ có nhịp ngày và nhịp tuần. Nên sai phân theo thứ tự nào, và kiểm gì sau mỗi bước?

<details>
<summary>Đáp án</summary>

**Sai phân mùa vụ trước** (lag 168), vì sai phân thường trước thì mùa vụ vẫn còn (bảng mục 4.6: chỉ sai phân thường thì $r_{168}$ còn 0,767).
Sau mỗi bước kiểm: ACF ở trễ 24, 168; ADF và KPSS; và hai dấu hiệu sai phân thừa. Trong buổi, sai phân 168 rồi sai phân thường cho độ lệch
chuẩn thấp nhất (0,427) và $r_1$ chỉ −0,25, nên giữ cả hai. Nhầm hay gặp: chỉ sai phân thường vì "KPSS đã đẹp".

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo: "Chúng tôi chạy ADF trên log GDP thực: p = 0,83, không bác bỏ $H_0$. Kết luận: GDP có nghiệm đơn vị. Vì vậy chúng tôi sai
phân tới khi ADF bác bỏ — hai lần." Chỉ ra hai lỗi.

<details>
<summary>Đáp án</summary>

1. **Không bác bỏ không phải chứng minh $H_0$** (mục 2, 4.5). ADF hay bỏ sót với chuỗi gần random walk; phải chạy thêm KPSS cùng dạng và xem
   ACF.
2. **Sai phân tới khi p đẹp** dẫn tới sai phân thừa: với GDP, lần hai cho $r_1$ = −0,488 và độ lệch chuẩn tăng 1,105 → 1,455 (mục 4.6). Dừng
   ở một lần và kiểm bằng hai dấu hiệu, không bằng p-value.

</details>

**Câu 10.** Bảng cho chuỗi **tăng trưởng GDP theo quý** (hiệu log × 100):

| Giai đoạn | Số quý | ADF p | KPSS p | Kết luận máy móc |
|---|---|---|---|---|
| 1947Q2–2026Q2 | 317 | 0,000 | 0,048 | mâu thuẫn |
| 1985Q1–2019Q4 | 140 | 0,000 | 0,099 | dừng |

Vì sao cùng một chuỗi lại ra hai kết luận? Báo cáo thế nào?

<details>
<summary>Đáp án</summary>

Giai đoạn dài chứa những năm dao động mạnh trước 1985 và **cú sốc 2020** (−8,2% rồi +7,5%). KPSS nhạy với độ dao động đổi theo thời gian,
nên bác bỏ tính dừng dù ADF bác bỏ rất mạnh nghiệm đơn vị (mục 4.5). Báo cáo: "tăng trưởng GDP dừng trong 1985–2019; trên toàn mẫu KPSS
bác bỏ do độ dao động đổi và cú sốc 2020, không phải do random walk", kèm cả bốn con số. Không sai phân thêm; nếu dùng toàn mẫu thì xử lý
riêng cú sốc 2020.

</details>
