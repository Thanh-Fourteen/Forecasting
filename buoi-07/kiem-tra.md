# Kiểm tra buổi 7 — Tự tương quan và tính dừng

## Nhắc lại khái niệm

**Câu 1.** Giả thuyết H0 của ADF và của KPSS lần lượt là:

- A. Dừng; có nghiệm đơn vị
- B. Có nghiệm đơn vị; dừng
- C. Cả hai đều là "dừng"
- D. Cả hai đều là "có nghiệm đơn vị"

<details>
<summary>Đáp án</summary>

**B.** ADF: H0 = có nghiệm đơn vị (không dừng), p nhỏ → bằng chứng **dừng**. KPSS: H0 = dừng (quanh hằng số hoặc quanh xu hướng), p nhỏ → bằng chứng
**không dừng**. Nhớ ngược là đọc sai mọi bảng kết quả.

</details>

**Câu 2.** ACF của một chuỗi giảm rất chậm, còn 0,53 ở trễ 30. Điều này gợi ý:

- A. Mùa vụ chu kỳ 30
- B. Chuỗi chưa dừng (xu hướng hoặc nghiệm đơn vị)
- C. Nhiễu trắng
- D. Sai phân thừa

<details>
<summary>Đáp án</summary>

**B.** FPP: "the ACF of non-stationary data decreases slowly. Also, for non-stationary data, the value of r_1 is often large and positive". Mùa vụ cho
**đỉnh** ở bội số chu kỳ chứ không phải giảm đều (A). D cho ACF(1) âm quanh −0,5.

</details>

**Câu 3.** Vì sao không nên kết luận "có tự tương quan" chỉ vì một cột ACF trong 20 trễ vượt dải ±1,96/√T?

- A. Vì dải vẽ sai
- B. Vì với nhiễu trắng, trung bình đã có ~1 cột vượt và 62% số chuỗi có ít nhất một cột
- C. Vì ACF không dùng để kiểm tra tự tương quan
- D. Vì phải dùng PACF

<details>
<summary>Đáp án</summary>

**B.** Mỗi cột là một kiểm định ở mức 5%; 20 cột thì kỳ vọng 1 cột vượt. Mô phỏng trong buổi (1.000 chuỗi, n = 500): trung bình 0,95 cột, 62% chuỗi có
≥ 1. Dùng **Ljung-Box** gộp nhiều trễ.

</details>

**Câu 4.** Chuỗi trend-stationary (dừng quanh xu hướng tất định) nên được xử lý bằng:

- A. Sai phân một lần
- B. Sai phân hai lần
- C. Khử xu hướng (hồi quy theo t) hoặc đưa t vào mô hình
- D. Lấy log

<details>
<summary>Đáp án</summary>

**C.** Sai phân chuỗi trend-stationary tạo nghiệm đơn vị MA trong phần nhiễu (Zivot: "produces a unit moving average root"). Ngược lại, khử xu hướng
một random walk tạo ACF giả (Nelson & Plosser). Chọn đúng bệnh mới chọn đúng thuốc.

</details>

## Vận dụng

**Câu 5.** Chuỗi $y = [4, 6, 8, 6, 4, 6, 8, 6, 4]$. Tính $r_1$ theo công thức FPP.

<details>
<summary>Đáp án</summary>

$\bar y = 6$; độ lệch $[-2, 0, 2, 0, -2, 0, 2, 0, -2]$. Mẫu số $= 4+0+4+0+4+0+4+0+4 = 20$. Tử số $\sum_{t=2}^{9} d_t d_{t-1} = 0+0+0+0+0+0+0+0 = 0$.
$r_1 =$ **0**. (Chuỗi có cấu trúc rõ nhưng ACF ở trễ 1 bằng 0 — $r_2 = (−2)(2)\cdot4/20 = −0{,}8$ mới bắt được nhịp; luôn xem nhiều trễ.)

</details>

**Câu 6.** Kết quả trên một chuỗi: ADF (dạng 'c') p = 0,906; KPSS (dạng 'c') p = 0,01; ADF (dạng 'ct') p = 0,000; KPSS (dạng 'ct') p = 0,10. Kết luận và
cách xử lý?

<details>
<summary>Đáp án</summary>

Với dạng 'c' cả hai nói "không dừng"; với dạng 'ct' cả hai nói "dừng quanh xu hướng tuyến tính". Đây là chuỗi **trend-stationary** (chính là chuỗi
0,05t + nhiễu trong buổi). Xử lý: khử xu hướng hoặc thêm biến $t$ vào mô hình — **không** sai phân.

</details>

**Câu 7.** Sau khi sai phân, ACF(1) = −0,49 và độ lệch chuẩn tăng từ 1,11 lên 1,46. Chuyện gì đã xảy ra? Bạn làm gì tiếp?

<details>
<summary>Đáp án</summary>

**Sai phân thừa.** Nau: ACF(1) ≤ −0,5 là dấu hiệu; và "the optimal order of differencing is often the order of differencing at which the standard
deviation is lowest" — sd tăng nghĩa là đã quá tay. Quay lại bậc sai phân trước đó; nếu KPSS vẫn bác bỏ thì tìm nguyên nhân khác (phương sai đổi, cú sốc,
gãy cấu trúc) thay vì sai phân thêm.

</details>

**Câu 8.** Bạn có chuỗi doanh thu theo ngày với nhịp tuần rõ. Nên sai phân theo thứ tự nào, và kiểm gì sau mỗi bước?

<details>
<summary>Đáp án</summary>

**Sai phân mùa vụ (lag 7) trước** (FPP: nếu sai phân thường trước thì mùa vụ vẫn còn). Sau mỗi bước kiểm: ACF ở trễ 7, 14 còn đỉnh không; ADF + KPSS; và
hai dấu hiệu sai phân thừa (ACF(1) và sd). Trong buổi, lượt thuê theo ngày (log): chỉ sai phân mùa vụ cho sd 0,373 — thấp nhất; thêm sai phân thường đẩy
sd lên 0,436 và ACF(1) về −0,367.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo: "Chúng tôi chạy ADF trên log GDP thực: p = 0,83, không bác bỏ H0. Kết luận: GDP có nghiệm đơn vị. Vì vậy chúng tôi sai phân đến khi
ADF bác bỏ — hai lần." Chỉ ra hai lỗi.

<details>
<summary>Đáp án</summary>

1. **"Không bác bỏ" không phải "chứng minh H0".** ADF có độ mạnh thấp với chuỗi gần nghiệm đơn vị (Zivot). Phải chạy thêm KPSS cùng dạng xác định, xem
   ACF, và nêu độ bất định.
2. **Sai phân tới khi p đẹp** là công thức dẫn tới sai phân thừa: với GDP thực, sai phân lần hai cho ACF(1) = −0,488 và sd tăng 1,105 → 1,455. Dừng ở
   $d = 1$ và kiểm bằng dấu hiệu, không bằng p-value.

</details>

**Câu 10.** Bảng cho chuỗi **tăng trưởng GDP theo quý** (sai phân log ×100):

| Giai đoạn | n | ADF p | KPSS p | Kết luận máy móc |
|---|---|---|---|---|
| 1947Q2–2026Q2 | 317 | 0,0000 | 0,048 | mâu thuẫn |
| 1985Q1–2019Q4 | 140 | 0,0000 | 0,099 | dừng |

Vì sao cùng một chuỗi lại cho hai kết luận? Bạn báo cáo thế nào?

<details>
<summary>Đáp án</summary>

Giai đoạn dài chứa **cú sốc COVID** (2020Q2 −8,2%, 2020Q3 +7,5%) và giai đoạn biến động cao 1947–1984. KPSS nhạy với **phương sai đổi** và mức trôi, nên
bác bỏ tính dừng dù chuỗi không có nghiệm đơn vị (ADF bác bỏ rất mạnh). Báo cáo trung thực: "tăng trưởng GDP dừng trong giai đoạn 1985–2019; trên toàn
mẫu KPSS bác bỏ do phương sai đổi và cú sốc 2020, không phải do nghiệm đơn vị" — kèm cả bốn con số và ACF. Nếu mô hình hoá toàn mẫu thì cần xử lý
phương sai đổi hoặc biến giả cho 2020, chứ không sai phân thêm.

</details>
