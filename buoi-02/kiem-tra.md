# Kiểm tra buổi 2 — Xác suất và thống kê cho dự báo

Mọi câu trả lời được chỉ bằng tài liệu buổi 2. Câu tính toán: ghi từng bước.

## Nhắc lại khái niệm

**Câu 1.** Một cửa hàng phạt nặng khi thiếu hàng (mất 3 đồng mỗi đơn vị thiếu) và nhẹ khi thừa (mất 1 đồng mỗi đơn vị
thừa). Nên đặt lượng hàng bằng đại lượng nào của phân phối nhu cầu?

- A. Trung bình
- B. Trung vị
- C. Quantile 0,75
- D. Quantile 0,25

<details>
<summary>Đáp án</summary>

**C — quantile 0,75.** Chi phí thiếu $C_u = 3$, chi phí thừa $C_o = 1$, nên mức nên đặt là quantile
$C_u/(C_u + C_o) = 3/(3 + 1) = 0{,}75$. Đó cũng là con số làm nhỏ nhất pinball loss với $\tau = 0{,}75$ (mục 4.2): thiếu
mỗi đơn vị phạt 0,75, thừa phạt 0,25, đúng tỷ lệ 3 : 1.

- **A sai**: trung bình là con số tốt nhất khi phạt theo **bình phương** sai lệch, không phải phạt theo từng đơn vị lệch.
- **B sai**: trung vị tốt nhất khi thiếu và thừa bị phạt **như nhau** (1 : 1). Ở đây thiếu đắt gấp 3.
- **D sai**: 0,25 = 1/(1 + 3) là đảo ngược hai chi phí, tức trường hợp thừa đắt hơn thiếu.

</details>

**Câu 2.** Phát biểu nào đúng về **khoảng dự báo** và **khoảng tin cậy**?

- A. Hai tên gọi của cùng một thứ
- B. Khoảng tin cậy cho giá trị quan sát mới; khoảng dự báo cho trung bình thật
- C. Khoảng dự báo cho một giá trị chưa quan sát, nên thường rộng hơn khoảng tin cậy của trung bình
- D. Khoảng dự báo hẹp dần về 0 khi có nhiều dữ liệu

<details>
<summary>Đáp án</summary>

**C.** Khoảng dự báo nói về **một giá trị tương lai** (lượt thuê lúc 17h mai), nên phải chứa cả dao động của chính giá trị
đó. Khoảng tin cậy nói về **một con số cố định chưa biết** (trung bình thật), và hẹp dần khi có thêm dữ liệu (mục 4.3,
4.6).

- **A sai**: hai khoảng trả lời hai câu hỏi khác nhau, độ rộng rất khác nhau.
- **B sai**: đảo ngược hai định nghĩa.
- **D sai**: đó là tính chất của khoảng tin cậy. Dù biết trung bình thật chính xác, lượt thuê từng giờ vẫn dao động, nên
  khoảng dự báo không bao giờ hẹp về 0.

</details>

**Câu 3.** Kiểm định cho p-value = 0,03 với $H_0$: "hai nhóm có trung bình như nhau", mức ý nghĩa 0,05. Phát biểu nào
**đúng**?

- A. Xác suất để hai nhóm có trung bình như nhau là 3%
- B. Nếu hai nhóm thật sự như nhau, dữ liệu lệch cỡ này hoặc hơn chỉ xảy ra khoảng 3% số lần; vì 0,03 < 0,05 nên bác bỏ $H_0$
- C. Đã chứng minh chênh lệch giữa hai nhóm là lớn
- D. Nếu p = 0,30 thì đã chứng minh hai nhóm như nhau

<details>
<summary>Đáp án</summary>

**B.** Đúng định nghĩa ở mục 4.5: p-value là xác suất gặp kết quả lệch cỡ này hoặc hơn **khi giả sử $H_0$ đúng**. p nhỏ
hơn mức ý nghĩa 0,05 thì bác bỏ $H_0$.

- **A sai**: p-value không phải xác suất $H_0$ đúng. Nó là xác suất của dữ liệu khi giả sử $H_0$ đúng.
- **C sai**: "có ý nghĩa thống kê" không có nghĩa là khác biệt lớn. Với rất nhiều dữ liệu, một chênh rất nhỏ cũng cho p nhỏ.
- **D sai**: p = 0,30 chỉ cho phép nói "không bác bỏ", không phải chứng minh; thứ Bảy − Chủ nhật ở mục 4.5 chênh 695
  lượt mà vẫn không bác bỏ được.

</details>

**Câu 4.** Vì sao bootstrap lấy mẫu lại **từng quan sát riêng lẻ** cho khoảng tin cậy quá hẹp trên chuỗi thời gian?

- A. Vì số lần lấy mẫu lại quá ít
- B. Vì xáo trộn thứ tự làm mất tự tương quan, coi dữ liệu có nhiều thông tin độc lập hơn thật
- C. Vì dữ liệu không có phân phối chuẩn
- D. Vì bootstrap chỉ dùng được cho trung vị

<details>
<summary>Đáp án</summary>

**B.** Khi dữ liệu tự tương quan dương, $n$ quan sát chỉ đáng giá như $n_{\text{eff}} < n$ quan sát độc lập (mục 4.6).
Rút từng điểm riêng lẻ phá mất phụ thuộc đó, nên bootstrap "tưởng" có đủ $n$ quan sát độc lập và cho khoảng quá hẹp.
Mô phỏng AR(1) $\rho$ = 0,7: khoảng "95%" chỉ chứa trung bình thật 60,3% số lần.

- **A sai**: tăng số lần lấy mẫu lại chỉ làm kết quả ít nhiễu hơn, không làm khoảng rộng ra. Mục 4.6 dùng 9.999 lần mà vẫn hẹp.
- **C sai**: bootstrap không đòi dữ liệu chuẩn. Chính vì thế nó hữu ích với dữ liệu lệch.
- **D sai**: bootstrap dùng được cho trung bình (cả mục 4.6 làm với trung bình), trung vị và nhiều con số khác.

</details>

## Vận dụng

**Câu 5.** Mẫu `[3, 7, 1, 10, 4]`. (a) Tính tay quantile 0,9 theo cách đếm của mục 4.1. (b) `np.quantile(x, 0.9)` mặc
định ra bao nhiêu, và vì sao khác?

<details>
<summary>Đáp án</summary>

(a) Xếp tăng: 1, 3, 4, 7, 10; $n$ = 5. Vị trí 0,9 × 5 = 4,5, làm tròn lên thành 5. Số thứ 5 là **10**. Kiểm lại: 5/5 số
≤ 10; còn mốc 7 chỉ có 4/5 = 80% < 90%, chưa đủ.

(b) `np.quantile` **nội suy**: vị trí $h = (5 - 1) \times 0{,}9 = 3{,}6$, đếm từ 0, nằm giữa số thứ 3 (7) và số thứ 4 (10).
Kết quả 7 + 0,6 × (10 − 7) = **8,8**. Hai cách là hai quy ước khác nhau; `method="inverted_cdf"` cho 10, khớp cách đếm tay.
Nhầm hay gặp: lấy 0,9 × 10 = 9 (90% của số lớn nhất).

</details>

**Câu 6.** Một chuỗi nhu cầu ngày có 365 quan sát, gần AR(1) với $\rho$ = 0,5. Số quan sát "độc lập tương đương" khoảng
bao nhiêu? Khoảng tin cậy trung bình tính như dữ liệu độc lập sẽ hẹp đi khoảng bao nhiêu lần so với đúng?

<details>
<summary>Đáp án</summary>

- $n_{\text{eff}} \approx 365 \times (1 - 0{,}5)/(1 + 0{,}5) = 365 \times 0{,}5/1{,}5 \approx$ **122**.
- Độ rộng khoảng tin cậy tỷ lệ với $1/\sqrt n$ (mục 4.6: tăng $n$ gấp 4 thì độ rộng giảm một nửa). Tỷ lệ độ rộng đúng
  so với độ rộng i.i.d. là $\sqrt{365/122} = \sqrt{3} \approx$ **1,7 lần**.
- Nhầm hay gặp: nói "hẹp 3 lần" vì quên căn bậc hai.

</details>

**Câu 7.** Bạn dựng khoảng 95% cho lượt thuê theo từng giờ từ dữ liệu 2011, chấm trên 2012 được tỷ lệ phủ 72,5%, đuôi
dưới 0,1%, đuôi trên 27,4%. Đồng nghiệp đề xuất đổi ±1,96s sang khoảng quantile thực nghiệm. Có giải quyết được không?
Đề xuất cách khác.

<details>
<summary>Đáp án</summary>

**Không.** Gần như toàn bộ phần rơi ra nằm ở **đuôi trên**: mức lượt thuê 2012 tăng (trung bình 143,8 → 234,7). Đó là
**dịch mức**, không phải lỗi hình dạng. Chạy thật, khoảng quantile cho 70,1%, không khá hơn.

Cách khác: dựng khoảng từ lịch sử gần hơn, hoặc mô hình hoá mức tăng rồi mới dựng khoảng (bảng mục 6). Khoảng quantile
chỉ sửa được hình dạng: trong mẫu, hai đuôi từ 0,3% / 3,3% thành 2,2% / 2,6%.

</details>

**Câu 8.** 5 ngày: $x$ = 1, 2, 3, 4, 5 và $y$ = 2, 1, 4, 3, 5. (a) Tính tay hệ số tương quan $r$. (b) Từ $r$ này có kết luận
được "$x$ làm tăng $y$" không?

<details>
<summary>Đáp án</summary>

(a)

- $\bar x$ = 15/5 = 3; $\bar y$ = 15/5 = 3.
- Độ lệch $x$: −2, −1, 0, 1, 2. Độ lệch $y$: −1, −2, 1, 0, 2.
- Tích: 2, 2, 0, 0, 4 → tổng 8.
- Tổng bình phương độ lệch: của $x$ là 4 + 1 + 0 + 1 + 4 = 10; của $y$ là 1 + 4 + 1 + 0 + 4 = 10.
- $r = 8/\sqrt{10 \times 10} = 8/10 =$ **0,8**: cùng chiều khá mạnh. `np.corrcoef` cho 0,8.

(b) **Không.** Tương quan không phải nhân quả: có thể có biến gây nhiễu tác động lên cả hai (như trời nóng với kem và đuối
nước, mục 4.4). Tuy vậy, $x$ vẫn có thể giúp **dự báo** $y$.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo viết: "Dùng cả 17.379 giờ 2011–2012 (trung bình 189,46, độ lệch chuẩn 181,39), khoảng dự báo 95%
cho lượt thuê một giờ là trung bình ± 1,96s = [−166,1; 545,0]. Kiểm trên chính dữ liệu đó: phủ 95,x%. Khoảng đạt yêu
cầu." Chỉ ra ít nhất hai chỗ sai.

<details>
<summary>Đáp án</summary>

Kiểm con số: 189,46 − 1,96 × 181,39 = −166,1 và 189,46 + 1,96 × 181,39 = 545,0. Phép tính đúng, nhưng cách làm sai:

1. **Cận dưới âm** cho số lượt thuê. Dữ liệu lệch phải (hệ số lệch 1,277), nên ±1,96s sai hình dạng. 1,96 chỉ cho đúng
   95% khi dữ liệu gần phân phối chuẩn (mục 4.3). Tỷ lệ phủ tổng còn giấu việc đuôi dưới gần 0%, đuôi trên quá 2,5%.
2. **Chấm trên chính dữ liệu dựng khoảng** (trong mẫu), nên tỷ lệ phủ lạc quan. Dựng từ 2011 rồi chấm 2012 theo từng giờ
   thì chỉ phủ 72,5%.
3. (Thêm) Không báo riêng hai đuôi; và một khoảng chung cho mọi giờ bỏ qua chênh lệch lớn giữa 3h sáng và 17h.

</details>

**Câu 10.** Bảng mô phỏng khoảng tin cậy 95% cho trung bình của AR(1) $\rho$ = 0,7, $n$ = 200, 300 lần lặp:

| độ dài khối | 1 | 3 | 6 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|
| tỷ lệ chứa trung bình thật | 60,3% | 78,7% | 86,3% | 89,0% | 89,3% | 81,3% |

Một bạn kết luận: "Khối càng dài càng tốt, cứ chọn khối thật dài cho chắc." Sai ở đâu? Vì sao ngay cả khối tốt nhất
vẫn dưới 95%?

<details>
<summary>Đáp án</summary>

**Sai vì tỷ lệ tụt lại ở khối 40.** Với $n$ = 200, khối 40 thì mỗi lần chỉ rút được 200/40 = 5 khối, và hai đầu chuỗi
bị rút ít: khoảng lại hẹp. Khối ngắn thì nhiều chỗ nối cắt đứt phụ thuộc, khoảng cũng hẹp.

Với $n$ = 200 không độ dài nào tránh được cả hai cái hại, nên khối tốt nhất vẫn dưới 95%. Chuỗi dài hơn thì đỡ: mục 4.6
cho thấy $n$ = 2.000, khối 13 phủ 94,0%.

</details>
