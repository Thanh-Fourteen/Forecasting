# Kiểm tra buổi 2 — Xác suất và thống kê cho dự báo

## Nhắc lại khái niệm

**Câu 1.** Một cửa hàng phạt nặng khi thiếu hàng (mất 3 đồng mỗi đơn vị thiếu) và nhẹ khi thừa (mất 1 đồng mỗi đơn vị thừa).
Nên đặt lượng hàng bằng đại lượng nào của phân phối nhu cầu?

- A. Trung bình
- B. Trung vị
- C. Quantile 0,75
- D. Quantile 0,25

<details>
<summary>Đáp án</summary>

**C.** Chi phí thiếu $C_u = 3$, thừa $C_o = 1$ → mức tối ưu là quantile $C_u/(C_u + C_o) = 0{,}75$ — chính là cực tiểu của
pinball loss với $\tau = 0{,}75$. A tối ưu cho sai số bình phương, B cho sai số tuyệt đối (chi phí hai chiều bằng nhau). D đảo
ngược hai chi phí.

</details>

**Câu 2.** Phát biểu nào đúng về **khoảng dự báo** và **khoảng tin cậy**?

- A. Hai tên gọi của cùng một thứ
- B. Khoảng tin cậy cho giá trị quan sát mới; khoảng dự báo cho tham số
- C. Khoảng dự báo cho giá trị chưa quan sát, nên thường rộng hơn khoảng tin cậy của trung bình
- D. Khoảng dự báo hẹp dần về 0 khi có nhiều dữ liệu

<details>
<summary>Đáp án</summary>

**C.** Khoảng tin cậy nói về tham số (ví dụ trung bình), hẹp lại khi $n$ tăng. Khoảng dự báo phải chứa cả biến động của chính
quan sát mới nên không hẹp về 0 (D sai). B đảo ngược hai định nghĩa.

</details>

**Câu 3.** Lượt thuê xe theo giờ có trung bình 189,46 và phương sai bằng 173,7 lần trung bình. Phân phối nào **loại** ngay mà
không cần vẽ?

- A. Chuẩn
- B. Poisson
- C. Âm nhị thức
- D. Không loại được gì

<details>
<summary>Đáp án</summary>

**B.** Poisson ép phương sai = trung bình; tỷ lệ 173,7 là phân tán thừa rất mạnh. Âm nhị thức có phương sai $\mu + \alpha\mu^2$
nên chứa được trường hợp này. Chuẩn không loại bằng tỷ lệ này (nhưng bị loại vì cho 14,8% xác suất lượt thuê âm).

</details>

**Câu 4.** Vì sao bootstrap lấy mẫu lại **từng quan sát độc lập** cho khoảng tin cậy quá hẹp trên chuỗi thời gian?

- A. Vì số lần lấy mẫu lại (B) quá ít
- B. Vì xáo trộn thứ tự làm mất tự tương quan, coi dữ liệu có nhiều thông tin độc lập hơn thật
- C. Vì dữ liệu không chuẩn
- D. Vì bootstrap chỉ dùng được cho trung vị

<details>
<summary>Đáp án</summary>

**B.** Với tự tương quan dương, $n$ quan sát chỉ mang thông tin như $n_{\text{eff}} < n$ quan sát độc lập; bootstrap i.i.d. không
biết điều đó. Tăng B (A) chỉ làm giảm nhiễu Monte Carlo, không đổi độ rộng kỳ vọng. Bootstrap không đòi dữ liệu chuẩn (C) và
dùng được cho nhiều thống kê (D).

</details>

## Vận dụng

**Câu 5.** Tính tay quantile 0,9 loại 7 (mặc định `np.quantile`) của mẫu `[3, 7, 1, 10, 4]`.

<details>
<summary>Đáp án</summary>

Sắp tăng: `[1, 3, 4, 7, 10]`, $n = 5$. $h = (5 - 1) \cdot 0{,}9 = 3{,}6$ → giữa $x_{(3)} = 7$ và $x_{(4)} = 10$ (đếm từ 0):
$7 + 0{,}6 \cdot (10 - 7) = $ **8,8**. `np.quantile([3, 7, 1, 10, 4], 0.9)` cho `8.8`.

</details>

**Câu 6.** Một chuỗi nhu cầu ngày có 365 quan sát, gần AR(1) với $\rho = 0{,}5$. Số quan sát "độc lập tương đương" khoảng bao
nhiêu? Khoảng tin cậy trung bình tính như dữ liệu độc lập sẽ hẹp đi khoảng bao nhiêu lần so với đúng?

<details>
<summary>Đáp án</summary>

$n_{\text{eff}} \approx 365 \cdot (1 - 0{,}5)/(1 + 0{,}5) \approx$ **122**. Độ rộng tỷ lệ với $1/\sqrt{n}$, nên khoảng i.i.d.
hẹp hơn khoảng $\sqrt{365/122} = \sqrt{3} \approx$ **1,7 lần**.

</details>

**Câu 7.** Bạn dựng khoảng 95% cho lượt thuê lúc 17h từ dữ liệu 2011, chấm trên 2012 được tỷ lệ phủ 72,5%, đuôi dưới 0,1%, đuôi
trên 27,4%. Đồng nghiệp đề xuất đổi ±1,96σ sang quantile thực nghiệm. Có giải quyết được không? Đề xuất cách khác.

<details>
<summary>Đáp án</summary>

**Không.** Gần như toàn bộ phần rơi ra ở đuôi trên — mức lượt thuê 2012 tăng (trung bình 143,8 → 234,7), không phải lỗi hình
dạng. Chạy thật: quantile thực nghiệm cho 70,1%. Cách khác: dựng khoảng từ lịch sử gần hơn (tháng 1–6/2012 → tháng 7–12 phủ
88,8–91,5%), hoặc mô hình hoá mức/xu hướng rồi dựng khoảng trên phần dư. Quantile chỉ sửa được hình dạng (trong mẫu: đuôi
0,3%/3,3% → 2,2%/2,6%).

</details>

**Câu 8.** Bạn cần khoảng tin cậy cho **trung bình số đơn hàng mỗi giờ** của một tuần (168 giờ, có nhịp ngày rõ). Chọn cách
bootstrap và độ dài khối, nói rõ rủi ro.

<details>
<summary>Đáp án</summary>

Moving block bootstrap. $n^{1/3} = 168^{1/3} \approx 6$ là điểm khởi đầu, nhưng chuỗi có nhịp 24 giờ nên khối 6 giờ cắt ngang chu
kỳ; khối 24 giờ giữ trọn một ngày nhưng chỉ còn 7 khối — ít khối thì khoảng tin cậy lại kém (mô phỏng AR(1) $n = 200$: khối 40
chỉ phủ 81,3%). Rủi ro chính: kết quả nhạy với độ dài khối → báo độ rộng theo vài độ dài khối, và nếu có xu hướng thì "trung bình
tuần" không phải tham số ổn định (lượt thuê 2012: khối 21 ×1,60, khối 168 ×3,53 so với i.i.d.).

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo viết: "Khoảng dự báo 95% cho lượt thuê theo giờ là trung bình ± 1,96σ = [−166,1; 545,0]. Kiểm trên chính
dữ liệu: phủ 95,x%. Mô hình khoảng đạt yêu cầu." Chỉ ra ít nhất hai chỗ sai.

<details>
<summary>Đáp án</summary>

1. **Cận dưới âm** cho dữ liệu đếm — hình dạng sai: dữ liệu lệch phải (hệ số lệch 1,277), phân phối chuẩn gán 14,8% cho giá trị âm.
   Tỷ lệ phủ tổng che giấu việc đuôi dưới gần 0% còn đuôi trên dồn quá 2,5%.
2. **Chấm trên chính dữ liệu dựng khoảng** — tỷ lệ phủ trong mẫu lạc quan. Khoảng dựng từ 2011 chấm trên 2012 chỉ phủ 72,5–80,5%.
3. (Thêm) Không báo riêng hai đuôi, và một khoảng chung cho mọi giờ bỏ qua khác biệt lớn giữa 3h sáng và 17h.

</details>

**Câu 10.** Bảng mô phỏng khoảng tin cậy 95% cho trung bình của AR(1) $\rho = 0{,}7$, $n = 200$, 300 lần lặp:

| độ dài khối | 1 | 3 | 6 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|
| tỷ lệ phủ | 60,3% | 78,7% | 86,3% | 89,0% | 89,3% | 81,3% |

Một bạn kết luận: "Khối càng dài càng tốt, cứ chọn khối thật dài cho chắc." Sai ở đâu? Và vì sao ngay cả khối tốt nhất vẫn dưới 95%?

<details>
<summary>Đáp án</summary>

Sai vì tỷ lệ phủ **giảm lại** ở khối 40: với $n = 200$ chỉ còn 5 khối mỗi lần lấy mẫu, phân phối bootstrap quá thô và thiếu biến
động. Có sự đánh đổi: khối ngắn phá tự tương quan (khoảng hẹp), khối dài ít khối (ước lượng kém). Khối tốt nhất vẫn dưới 95% vì
$n_{\text{eff}} \approx 200 \cdot 0{,}3/1{,}7 \approx 35$ — cỡ mẫu hiệu dụng nhỏ, và khoảng percentile có sai lệch với mẫu nhỏ;
block bootstrap sửa phần lớn chứ không hoàn toàn.

</details>
