# Kiểm tra buổi 1 — Forecasting là gì

## Nhắc lại khái niệm

**Câu 1.** Giám đốc nói: "Quý tới phải bán 12.000 máy, nên dự báo quý tới là 12.000." Con số 12.000 là gì?

- A. Dự báo
- B. Mục tiêu
- C. Kế hoạch
- D. Khoảng dự báo

<details>
<summary>Đáp án</summary>

**B.** Mục tiêu là điều ta *muốn* xảy ra. Dự báo (A) là điều *sẽ* xảy ra với thông tin đang có — không được sửa cho khớp mục tiêu.
Kế hoạch (C) là việc làm để kéo dự báo về gần mục tiêu (tuyển thêm người bán, khuyến mãi). D là một dải giá trị, không phải một số
áp đặt.

</details>

**Câu 2.** Theo FPP, yếu tố nào **không** nằm trong bốn yếu tố quyết định một đại lượng dự báo được tới đâu?

- A. Hiểu các yếu tố tác động tới nó
- B. Có bao nhiêu dữ liệu
- C. Mô hình có bao nhiêu tham số
- D. Dự báo có làm thay đổi chính thứ được dự báo không

<details>
<summary>Đáp án</summary>

**C.** Bốn yếu tố là A, B, D và "tương lai giống quá khứ tới đâu". Số tham số là lựa chọn của người làm mô hình, không phải tính chất
của đại lượng — và bảng lịch 8.904 ô của buổi học cho thấy nhiều tham số không làm dự báo tốt hơn.

</details>

**Câu 3.** Phần dư (residual) khác sai số dự báo (forecast error) ở chỗ nào?

- A. Không khác, hai tên của một thứ
- B. Phần dư tính trên dữ liệu đã dùng để khớp mô hình; sai số dự báo tính trên dữ liệu mô hình chưa thấy
- C. Phần dư luôn lớn hơn sai số dự báo
- D. Sai số dự báo chỉ tính cho tầm 1 bước

<details>
<summary>Đáp án</summary>

**B.** FPP §5.8: phần dư tính trên tập huấn luyện và thường là dự báo một bước; sai số dự báo tính trên tập kiểm tra và có thể nhiều
bước (D sai). C ngược lại: phần dư thường *nhỏ hơn* — ở buổi học 0,380–0,411 so với 0,508.

</details>

**Câu 4.** Bài học nào gắn **đúng** với cuộc thi?

- A. M1: phương pháp ML thuần thắng mọi phương pháp thống kê
- B. M4: 12 trong 17 phương pháp chính xác nhất là kết hợp; sáu phương pháp ML thuần kém
- C. M5: mọi phương pháp dẫn đầu là mô hình thống kê cho từng chuỗi riêng
- D. M6: độ chính xác dự báo gắn chặt với lợi nhuận đầu tư

<details>
<summary>Đáp án</summary>

**B.** A sai: M1 kết luận phương pháp phức tạp không nhất thiết chính xác hơn phương pháp đơn giản. C ngược với M5: dẫn đầu là ML thuần
(phần lớn LightGBM) học chung nhiều chuỗi. D ngược với M6: tương quan giữa độ chính xác và hiệu quả đầu tư chỉ r = 0,04.

</details>

## Vận dụng

**Câu 5.** Một siêu thị đặt rau mỗi sáng cho ngày hôm đó. Rau thừa bỏ đi mất 10.000 đ/kg; thiếu rau mất lãi 30.000 đ/kg. Nên đặt theo
quantile nào của phân phối nhu cầu? Nếu phân phối nhu cầu ngày mai có trung vị 200 kg thì lượng đặt nên cao hơn hay thấp hơn 200 kg?

<details>
<summary>Đáp án</summary>

$C_u = 30.000$, $C_o = 10.000$ → quantile $30/(30+10) = $ **0,75**. Quantile 0,75 lớn hơn trung vị nên đặt **cao hơn** 200 kg. Ở
buổi học (thiếu 4 : thừa 1) cộng quantile 0,8 của sai số vào dự báo làm chi phí giảm 18,6% dù MAE tăng từ 0,490 lên 0,673.

</details>

**Câu 6.** Bạn dự báo điện theo giờ, mỗi thứ Hai 00:00 cho 168 giờ tới. Baseline nào **không hợp lệ**, vì sao?

(a) giờ này tuần trước; (b) trung bình cùng giờ của 4 tuần gần nhất; (c) cùng giờ hôm qua; (d) giữ nguyên giờ cuối đã biết.

<details>
<summary>Đáp án</summary>

**(c).** Với giờ thứ 30 trở đi (ví dụ thứ Ba 06:00), "cùng giờ hôm qua" là thứ Hai 06:00 — *sau* gốc dự báo, lúc ra dự báo chưa có
số. Điều kiện: độ trễ phải ≥ tầm (168 giờ). (a), (b) dùng trễ 168–672 giờ; (d) dùng giờ trước gốc — hợp lệ dù kém (MAE 0,770).

</details>

**Câu 7.** Điền phiếu bài toán 6 ô cho: *bệnh viện xếp lịch trực cấp cứu cho 9 ngày Tết.*

<details>
<summary>Đáp án gợi ý</summary>

1. **Quyết định:** trưởng khoa xếp số bác sĩ/điều dưỡng mỗi ca, chốt trước Tết 3 tuần. 2. **Biến mục tiêu:** số ca cấp cứu nhập viện
mỗi ca trực 8 giờ. 3. **Tầm:** từ 3 tuần tới 3 tuần + 9 ngày (27 ca). 4. **Độ chi tiết:** theo ca, toàn khoa cấp cứu (có thể tách
chấn thương giao thông). 5. **Mốc cắt:** số liệu tới ngày chốt lịch; Tết các năm trước theo âm lịch; chưa biết thời tiết, dịch bệnh.
6. **Chi phí hai chiều:** thiếu người → bệnh nhân chờ, rủi ro tính mạng, gọi người nghỉ về (rất đắt); thừa người → trả lương trực, nhân
viên mất ngày nghỉ. Chi phí thiếu lớn hơn nhiều → xếp theo quantile cao (ví dụ 0,9), không theo trung bình.

Chấm: đủ 6 ô, ô 3 nói rõ khoảng cách từ lúc ra dự báo, ô 6 có **cả hai chiều**.

</details>

**Câu 8.** Mô hình A có MAE trên tập kiểm tra 12,0; mô hình B 11,4. Đồng nghiệp muốn triển khai B. Bạn cần hỏi thêm ít nhất ba điều gì
trước khi đồng ý?

<details>
<summary>Đáp án</summary>

(1) **Baseline** (naive, naive mùa vụ, trung bình) đạt bao nhiêu — nếu naive mùa vụ 11,2 thì cả hai vô dụng. (2) B có dùng dữ liệu
kiểm tra để khớp/chọn tham số không — dự báo có đổi khi đổi số đo giai đoạn kiểm tra không? (3) Chấm có đúng **độ chi tiết và tầm**
của quyết định không — ở buổi học, chấm theo giờ và theo tổng tuần cho thứ hạng ngược nhau. Thêm: chênh 0,6 có ổn định qua nhiều gốc
không (TB 4 tuần chỉ thắng 30/46 tuần); quyết định có chi phí lệch không (MAE nhắm trung vị).

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo nội bộ:

> Mô hình bảng lịch (trung bình theo tuần trong năm × thứ × giờ, khớp trên dữ liệu 12/2006–11/2010) đạt MAE 0,380 kWh/giờ trên năm
> 2010. Đề xuất đưa vào vận hành.

Chỉ ra hai lỗi và con số đúng.

<details>
<summary>Đáp án</summary>

1. **Chấm trên dữ liệu đã dùng để làm dự báo:** bảng khớp cả năm 2010 rồi chấm trên 2010 — khoảng 1/4 số liệu mỗi ô là chính giờ đang
   chấm. Dự báo cuốn trung thực (chỉ dữ liệu trước mỗi gốc thứ Hai): **0,508**.
2. **Không có baseline:** TB 4 tuần đạt **0,490** — tốt hơn mô hình đề xuất; tuần trước 0,576, trung bình 0,652. Đưa bảng lịch vào vận
   hành cho quyết định theo giờ là tệ hơn một phép trung bình đơn giản.

</details>

**Câu 10.** Bảng chấm năm 2010 (bảng lịch đã chấm trung thực):

| Phương pháp | MAE theo giờ (kWh) | MAE tổng tuần (kWh) |
|---|---|---|
| TB 4 tuần | 0,490 | 27,9 |
| bảng lịch | 0,508 | 16,4 |
| tuần trước | 0,576 | 24,2 |

Một bạn kết luận: "Bảng có mâu thuẫn, chắc code tính tổng tuần sai." Bạn trả lời thế nào? Nên chọn phương pháp nào?

<details>
<summary>Đáp án</summary>

Không mâu thuẫn: thứ hạng phụ thuộc **mức gộp được chấm**. Theo giờ, nhiễu từng giờ lớn và bảng lịch không bám được mức gần đây; cộng
lên tuần, nhiễu triệt tiêu và bảng lịch nhớ được nhịp năm (kỳ nghỉ tháng 8) mà TB 4 tuần chỉ theo kịp sau khi kỳ nghỉ đã bắt đầu. Chọn
theo **ô 4 của phiếu**: quyết định mua điện theo giờ → TB 4 tuần; mua một khối cả tuần → bảng lịch. Cũng nên thử kết hợp hai phương
pháp (M1, M3, M4 đều thấy kết hợp thường tốt hơn từng phương pháp).

</details>
