# Kiểm tra buổi 1 — Forecasting là gì

## Nhắc lại khái niệm

**Câu 1.** Giám đốc nói: "Quý tới phải bán 12.000 máy, nên dự báo quý tới là 12.000." Con số 12.000 là gì?

- A. Dự báo
- B. Mục tiêu
- C. Kế hoạch
- D. Baseline

<details>
<summary>Đáp án</summary>

**B — mục tiêu.** Mục tiêu là điều ta *muốn* xảy ra, và câu "phải bán 12.000" nói đúng mong muốn đó (mục 4.1).
**A sai**: dự báo là điều *sẽ* xảy ra với thông tin đang có; nó không được sửa cho khớp mong muốn. **C sai**: kế hoạch
là việc làm để kéo kết quả về gần mục tiêu, ví dụ tuyển thêm người bán, chạy khuyến mãi; 12.000 không phải việc làm.
**D sai**: baseline là một cách dự báo đơn giản để so, ví dụ "quý tới bằng quý này", không phải con số áp đặt.

</details>

**Câu 2.** Theo FPP, yếu tố nào **không** nằm trong bốn yếu tố quyết định một đại lượng dự báo được tới đâu?

- A. Hiểu các yếu tố tác động tới nó
- B. Có bao nhiêu dữ liệu
- C. Mô hình có bao nhiêu tham số
- D. Dự báo có làm thay đổi chính thứ được dự báo không

<details>
<summary>Đáp án</summary>

**C.** Bốn yếu tố (mục 4.1) là A, B, D và "tương lai giống quá khứ tới đâu". Cả bốn là tính chất của *thứ được dự báo*.
Số tham số là lựa chọn của người làm mô hình. Bảng lịch 8.904 tham số của buổi học còn thua một baseline không có tham
số nào đáng kể. **A, B, D sai** vì chúng đều nằm trong danh sách: A là yếu tố 1, B là yếu tố 2, D là yếu tố 4.

</details>

**Câu 3.** Phần dư khác sai số dự báo ở chỗ nào?

- A. Không khác, hai tên của một thứ
- B. Phần dư tính trên dữ liệu đã dùng để khớp mô hình; sai số dự báo tính trên dữ liệu mô hình chưa thấy
- C. Phần dư luôn lớn hơn sai số dự báo
- D. Sai số dự báo chỉ tính cho giờ ngay sau gốc

<details>
<summary>Đáp án</summary>

**B** (mục 4.4). **A sai**: hai thứ đo trên hai loại dữ liệu khác nhau, nên cho số khác nhau. **C sai**, thật ra
ngược lại: phần dư thường *nhỏ hơn*, vì mô hình đã thấy dữ liệu đó. Ở buổi học, bảng lịch chấm kiểu nhìn trộm được
0,380, chấm trung thực được 0,508 kWh/giờ. **D sai**: buổi học chấm sai số dự báo cho cả 168 giờ sau mỗi gốc.

</details>

**Câu 4.** Giờ cuối cùng đã có số đo là $T$ = 23:00 Chủ nhật. Giờ $T + 20$ là giờ nào?

- A. 19:00 thứ Hai
- B. 20:00 thứ Hai
- C. 19:00 Chủ nhật
- D. 20:00 thứ Ba

<details>
<summary>Đáp án</summary>

**A.** $T + 1$ là 00:00 thứ Hai, nên $T + 20$ là 19:00 thứ Hai (mục 4.3). Kiểm lại: từ 23:00 tới 24:00 là 1 giờ, cộng
thêm 19 giờ là 19:00. **B sai**: đó là đếm 20 giờ từ gốc 00:00, tức nhầm $T + 1$ với $T$; nhầm này hay gặp nhất.
**C sai**: $h$ tính về phía tương lai, không lùi lại. **D sai**: 20:00 thứ Ba cách $T$ tới 45 giờ.

</details>

## Vận dụng

**Câu 5.** Một siêu thị đặt rau mỗi sáng cho ngày hôm đó. Rau thừa bỏ đi mất 10.000 đ/kg; thiếu rau mất lãi
30.000 đ/kg. Nên đặt theo quantile nào của nhu cầu? Nếu trung vị nhu cầu ngày mai là 200 kg, lượng đặt nên cao hơn hay
thấp hơn 200 kg?

<details>
<summary>Đáp án</summary>

Bước 1: thiếu mất $C_u$ = 30.000 đ/kg, thừa mất $C_o$ = 10.000 đ/kg.
Bước 2: $p^\ast = C_u/(C_u + C_o) = 30/(30 + 10) = $ **0,75** (mục 4.6).
Bước 3: quantile 0,75 lớn hơn trung vị (quantile 0,5), nên đặt **cao hơn** 200 kg.

Vì sao: thiếu đắt gấp 3 lần thừa, nên chấp nhận thừa để ít khi thiếu. Nhầm hay gặp là đảo $C_u$ và $C_o$, ra
10/(10 + 30) = 0,25 và đặt thấp hơn trung vị.

</details>

**Câu 6.** Bạn dự báo điện theo giờ, mỗi thứ Hai 00:00 cho 168 giờ tới. Baseline nào **không hợp lệ**, vì sao?

(a) giờ này tuần trước; (b) trung bình cùng giờ của 4 tuần gần nhất; (c) cùng giờ hôm qua; (d) giữ nguyên giờ cuối đã
biết.

<details>
<summary>Đáp án</summary>

**(c).** Gọi $T$ là 23:00 Chủ nhật. "Cùng giờ hôm qua" lấy số ở $T + h - 24$. Với $h = 25$ trở đi, giờ đó là $T + 1$ trở
đi, tức *sau* gốc. Ví dụ $h = 31$ là 06:00 thứ Ba; hôm qua cùng giờ là 06:00 thứ Hai $= T + 7$, lúc ra dự báo chưa có.
**(a)** lùi 168 giờ và **(b)** lùi 168–672 giờ, luôn trước gốc vì $h \le 168$, nên hợp lệ. **(d)** dùng đúng giờ $T$,
hợp lệ dù kém (MAE 0,770 kWh/giờ, kém nhất bảng ở mục 4.4).

</details>

**Câu 7.** Điền phiếu bài toán 6 ô cho: *bệnh viện xếp lịch trực cấp cứu cho 9 ngày Tết.*

<details>
<summary>Đáp án gợi ý</summary>

1. **Quyết định:** trưởng khoa xếp số bác sĩ, điều dưỡng mỗi ca, chốt trước Tết 3 tuần.
2. **Biến mục tiêu:** số ca cấp cứu nhập viện mỗi ca trực 8 giờ.
3. **Tầm:** từ 3 tuần tới 3 tuần + 9 ngày sau ngày chốt (27 ca).
4. **Độ chi tiết:** theo ca, toàn khoa cấp cứu (có thể tách riêng tai nạn giao thông).
5. **Mốc cắt:** số liệu tới ngày chốt lịch; Tết các năm trước theo âm lịch; chưa biết thời tiết, dịch bệnh.
6. **Chi phí hai chiều:** thiếu người thì bệnh nhân chờ, rủi ro tính mạng, phải gọi người nghỉ về (rất đắt); thừa
   người thì trả lương trực, nhân viên mất ngày nghỉ.

Vì thiếu đắt hơn thừa nhiều, nên xếp theo quantile cao (ví dụ 0,9), không theo trung bình (mục 4.6). Chấm: đủ 6 ô, ô 3
nói rõ tính từ lúc nào, ô 6 có **cả hai chiều**. Phiếu chỉ ghi "thiếu người thì nguy hiểm" là thiếu một chiều.

</details>

**Câu 8.** Mô hình A có MAE trên dữ liệu kiểm tra 12,0; mô hình B 11,4. Đồng nghiệp muốn triển khai B. Bạn cần hỏi
thêm ít nhất ba điều gì trước khi đồng ý?

<details>
<summary>Đáp án</summary>

1. **Baseline đạt bao nhiêu?** Nếu seasonal naive đạt 11,2 thì cả A lẫn B đều thua cách đơn giản nhất (mục 4.3).
2. **B có từng thấy dữ liệu kiểm tra không?** Thử đổi số đo của giai đoạn kiểm tra: dự báo của B mà đổi theo là
   sai số ảo (mục 4.4).
3. **Chấm có đúng độ chi tiết của quyết định không?** Ở buổi học, chấm theo giờ và theo tổng tuần cho thứ hạng ngược
   nhau (mục 4.5).

Hỏi thêm được: chênh 0,6 có ổn định qua nhiều gốc không (trung bình 4 tuần chỉ thắng bảng lịch 30 trên 46 tuần); quyết
định có chi phí thiếu, thừa lệch nhau không (MAE nhắm trung vị, mục 4.6). Trả lời "B tốt hơn vì 11,4 < 12,0" là thiếu
cả ba câu hỏi.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo nội bộ:

> Mô hình bảng lịch (trung bình theo tuần trong năm × thứ × giờ, khớp trên dữ liệu 12/2006–11/2010) đạt MAE 0,380
> kWh/giờ trên năm 2010. Đề xuất đưa vào vận hành.

Chỉ ra hai lỗi và con số đúng.

<details>
<summary>Đáp án</summary>

1. **Chấm trên dữ liệu đã dùng để làm dự báo.** Bảng khớp cả năm 2010 rồi chấm trên 2010. Khoảng 22% số liệu mỗi ô,
   tức (3,82 − 2,99)/3,82, là chính giờ đang chấm (mục 4.4). Dự báo cuốn trung thực, chỉ dùng dữ liệu trước mỗi gốc
   thứ Hai, cho **0,508**.
2. **Không có baseline.** Trung bình 4 tuần đạt **0,490**, tốt hơn mô hình đề xuất; tuần trước 0,576. Với quyết định
   theo giờ, bảng lịch còn thua một phép trung bình đơn giản.

Chỉ nêu một lỗi là chưa đủ: sửa lỗi 1 mà không có baseline thì 0,508 vẫn trông "ổn".

</details>

**Câu 10.** Bảng chấm năm 2010 (bảng lịch đã chấm trung thực):

| Phương pháp | MAE theo giờ (kWh) | MAE tổng tuần (kWh) |
|---|---|---|
| trung bình 4 tuần | 0,490 | 27,9 |
| bảng lịch | 0,508 | 16,4 |
| tuần trước | 0,576 | 24,2 |

Một bạn kết luận: "Bảng có mâu thuẫn, chắc code tính tổng tuần sai." Bạn trả lời thế nào? Nên chọn phương pháp nào?

<details>
<summary>Đáp án</summary>

Không mâu thuẫn: thứ hạng phụ thuộc **độ chi tiết được chấm** (mục 4.5). Theo giờ, nhiễu lớn làm bảng lịch lệch lúc
lên lúc xuống. Cộng lên tuần, các lệch đó bù trừ nhau, như ví dụ +1 và −1 cộng lại bằng 0. Còn lại là phần bảng lịch
làm tốt: nó nhớ kỳ nghỉ tháng 8, trong khi trung bình 4 tuần chỉ hạ xuống sau khi kỳ nghỉ đã bắt đầu.

Chọn theo **ô 4 của phiếu**: mua điện theo giờ thì chọn trung bình 4 tuần; mua một khối cả tuần thì chọn bảng lịch.
Kết luận "code sai" là nhầm hay gặp: nó mặc định một phương pháp phải thắng ở mọi mức chấm.

</details>
