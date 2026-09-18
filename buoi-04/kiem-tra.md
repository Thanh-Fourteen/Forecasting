# Kiểm tra buổi 4 — Đọc và vẽ biểu đồ chuỗi thời gian

## Nhắc lại khái niệm

**Câu 1.** Doanh số một cửa hàng tăng vọt mỗi dịp Tết, rồi có những đợt suy giảm kéo dài 2–4 năm theo tình hình kinh tế. Hai mẫu hình
này lần lượt là:

- A. Chu kỳ; mùa vụ
- B. Mùa vụ; chu kỳ
- C. Xu hướng; mùa vụ
- D. Mùa vụ; xu hướng

<details>
<summary>Đáp án</summary>

**B.** Tết lặp lại theo lịch (tần suất cố định, dù ngày dương lịch xê dịch) → mùa vụ. Đợt suy giảm không có độ dài cố định, gắn với kinh
tế → chu kỳ (FPP: "not of a fixed frequency", thường "at least 2 years"). Xu hướng (C, D) là thay đổi dài hạn một chiều, không lên xuống.

</details>

**Câu 2.** Khác nhau giữa seasonal plot và subseries plot là:

- A. Seasonal plot mỗi chu kỳ (tuần/năm) một đường chồng lên nhau; subseries plot gom mỗi "mùa" (tháng/thứ) thành một chuỗi con riêng
- B. Hai tên gọi của cùng một hình
- C. Seasonal plot chỉ dùng cho dữ liệu tháng; subseries chỉ cho dữ liệu giờ
- D. Subseries plot cho thấy hình dạng mùa vụ trong một chu kỳ; seasonal plot cho thấy thay đổi theo năm

<details>
<summary>Đáp án</summary>

**A.** Seasonal plot trả lời "hình dạng một chu kỳ ra sao, chu kỳ nào khác thường"; subseries trả lời "một mùa cụ thể thay đổi qua các
năm thế nào". D đảo ngược vai trò. C sai: cả hai dùng được cho mọi tần suất. `month_plot` của statsmodels tên là "seasonal" nhưng vẽ
subseries — dễ gây nhầm B.

</details>

**Câu 3.** Vì sao không nên dùng trục kép để "chứng minh" hai chuỗi đi cùng nhau?

- A. Vì matplotlib vẽ trục kép bị lỗi
- B. Vì thang của trục thứ hai chọn tuỳ ý, có thể làm hai đường trùng nhau hay tách nhau theo ý người vẽ
- C. Vì hai chuỗi phải cùng đơn vị mới vẽ được
- D. Vì trục kép luôn cắt trục y

<details>
<summary>Đáp án</summary>

**B.** Few (2008): khi hai đường theo hai thang khác nhau "their intersection means nothing". Muốn nói về quan hệ thì vẽ scatter và
tính tương quan, hoặc đánh chỉ số hai chuỗi về cùng thang. C sai: trục kép tồn tại chính để vẽ hai đơn vị. D không đúng.

</details>

**Câu 4.** Trên thang log, hai đoạn có độ dốc bằng nhau nghĩa là:

- A. Tăng cùng số đơn vị
- B. Tăng cùng phần trăm
- C. Hai giai đoạn có cùng giá trị
- D. Không có ý nghĩa gì

<details>
<summary>Đáp án</summary>

**B.** Khoảng cách bằng nhau trên thang log là tỷ lệ bằng nhau. Ở buổi học, năm 2011 đoạn T4→T5 tăng tuyệt đối nhiều nhất (+40.951)
nhưng đoạn T3→T4 tăng tỷ lệ nhiều nhất (+48,1%) — chỉ thang log cho thấy điều đó.

</details>

## Vận dụng

**Câu 5.** Bạn có dữ liệu số cuộc gọi tổng đài theo giờ trong 3 năm. Chọn **ba** biểu đồ để trả lời: (a) có mùa vụ tuần không;
(b) giờ nào dự báo khó nhất; (c) có ngày dữ liệu bất thường không. Nói rõ đọc gì trên mỗi hình.

<details>
<summary>Đáp án</summary>

(a) **Heatmap giờ × thứ** — các dòng T7/CN có khác 5 dòng đầu không; hoặc **ACF tới trễ 336** — đỉnh ở 168 cao hơn đỉnh 144.
(b) **Boxplot theo giờ** — giờ có hộp (IQR) rộng nhất, tách ngày làm việc/nghỉ. (c) **Đường tổng theo ngày** vẽ chấm dữ liệu gốc (không
làm trơn, không gộp tháng) — ngày rơi gần 0 hoặc vọt cao; kiểm thêm số giờ có dữ liệu mỗi ngày.

</details>

**Câu 6.** Tính tay $r_1$ theo công thức FPP cho chuỗi $y = [2, 4, 6, 4, 2]$.

<details>
<summary>Đáp án</summary>

$\bar y = 3{,}6$; độ lệch $[-1{,}6;\ 0{,}4;\ 2{,}4;\ 0{,}4;\ -1{,}6]$. Mẫu số $\sum (y_t - \bar y)^2 = 2{,}56 + 0{,}16 + 5{,}76 + 0{,}16 +
2{,}56 = 11{,}2$. Tử số $\sum_{t=2}^{5} (y_t - \bar y)(y_{t-1} - \bar y) = (0{,}4)(-1{,}6) + (2{,}4)(0{,}4) + (0{,}4)(2{,}4) + (-1{,}6)(0{,}4)
= -0{,}64 + 0{,}96 + 0{,}96 - 0{,}64 = 0{,}64$. $r_1 = 0{,}64 / 11{,}2 \approx$ **0,057**.

</details>

**Câu 7.** Một bạn vẽ lag plot trễ 12 giờ của lượt thuê xe, thấy $r = -0{,}144$ và hai nhánh bám hai trục, rồi kết luận "giờ này đông
thì 12 giờ sau vắng — quan hệ âm, dùng làm feature dự báo ngược dấu". Nhận xét.

<details>
<summary>Đáp án</summary>

Hai nhánh là **đỉnh ghép với đáy** của mùa vụ ngày (8h đông ghép 20h hôm trước vắng, 17h đông ghép 5h sáng vắng), không phải một quan hệ
âm ổn định. Hệ số −0,144 trộn hai nhánh nên gần 0 và vô nghĩa. Feature đúng là cùng giờ hôm trước / tuần trước (trễ 24: 0,819; trễ 168:
0,876), hoặc mã hoá giờ trong ngày.

</details>

**Câu 8.** Báo cáo có biểu đồ tổng doanh thu theo tháng, trục y từ 480 đến 520 triệu, tiêu đề "Doanh thu tăng mạnh tháng 6". Tháng 5:
490, tháng 6: 510. Viết lại tiêu đề và nói bạn sửa trục thế nào.

<details>
<summary>Đáp án</summary>

Doanh thu là tổng → trục y nên bắt đầu từ 0; với trục 480–520, tăng 20 triệu (+4,1%) chiếm nửa chiều cao hình. Tiêu đề trung thực:
"Doanh thu tháng 6 tăng 4,1% so với tháng 5 (490 → 510 triệu)". Nếu cần nhấn biến động nhỏ, vẽ thêm một hình riêng về **phần trăm thay
đổi** có trục quanh 0 — Correll et al. (2020) khuyên chọn phạm vi theo độ lớn thay đổi có ý nghĩa, và cảm giác phóng đại vẫn còn dù có
ký hiệu trục bị cắt.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Heatmap trung bình lượt thuê (trích):

| thứ \ giờ | 8h | 13h | 17h |
|---|---|---|---|
| T2 | 412 | 206 | 502 |
| T4 | 488 | 186 | 513 |
| T7 | 114 | 385 | 334 |
| CN | 84 | 375 | 319 |

Một bạn kết luận: "Thứ Bảy và Chủ nhật ít người thuê xe hơn, nên hệ thống nên giảm số xe cả ngày cuối tuần." Sai ở đâu?

<details>
<summary>Đáp án</summary>

Heatmap cho thấy **hình dạng** ngày khác nhau, không phải tổng thấp hơn: lúc 13h cuối tuần (375–385) **cao gần gấp đôi** ngày thường
(186–206). Tổng ngày trên 655 ngày đủ giờ: T7 4.653, CN 4.523 so với T2 4.708 — chỉ chênh vài phần trăm. Kết luận đúng: cuối tuần
**dời** nhu cầu từ giờ đi làm sang giữa ngày; phân bổ xe theo giờ, không giảm cả ngày.

</details>

**Câu 10.** Biểu đồ trục kép tổng lượt thuê theo tháng 2012 (trục trái 90.000–220.000) và nhiệt độ (trục phải 5–32 °C), hai đường gần
trùng; tiêu đề "Lượt thuê bám sát nhiệt độ". Scatter 12 tháng cho $r = 0{,}91$. Tháng 7 nóng nhất (30,8 °C, 203.607 lượt); tháng 9
25,4 °C nhưng 218.573 lượt. Chỉ ra ba vấn đề của biểu đồ gốc và điều mà scatter cho thấy nhưng trục kép che.

<details>
<summary>Đáp án</summary>

(1) Trục kép: thang phải chọn để hai đường đè nhau — sự trùng khít là do người vẽ. (2) Trục trái cắt ở 90.000: tháng 1 (96.744) trông
gần 0, mức tăng bị phóng đại. (3) Tiêu đề khẳng định quan hệ mà hình không thể kiểm (không có hệ số, không có scatter). Scatter cho thấy
quan hệ mạnh ($r = 0{,}91$) nhưng **không đơn điệu ở vùng nóng**: tháng 9 mát hơn tháng 7 mà lượt thuê cao hơn — quá nóng không làm tăng
thêm, và mức 2012 còn đang tăng theo thời gian (xu hướng trộn vào tương quan).

</details>
