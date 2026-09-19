# Kiểm tra buổi 4 — Đọc và vẽ biểu đồ chuỗi thời gian

## Nhắc lại khái niệm

**Câu 1.** Lượt khách một quán cà phê sáng thứ Bảy nào cũng đông gấp đôi ngày thường. Ba năm nay lượt khách giảm dần vì có
quán mới mở gần đó. Hai mẫu hình này lần lượt là:

- A. Chu kỳ; mùa vụ
- B. Mùa vụ; xu hướng
- C. Xu hướng; chu kỳ
- D. Mùa vụ; chu kỳ

<details>
<summary>Đáp án</summary>

**B.** Thứ Bảy lặp lại sau đúng 7 ngày theo lịch, nên là **mùa vụ** (mùa vụ tuần, mục 4.1: "mùa" là bất kỳ vòng lặp theo lịch
nào). Giảm dần ba năm liền một chiều là **xu hướng**. **A sai** vì đảo hai khái niệm. **C sai** ở vế đầu: thứ Bảy có số bước lặp
cố định nên không phải chu kỳ. **D sai** ở vế sau: chu kỳ là lên *rồi xuống* với độ dài không cố định, còn đây là giảm một chiều.

</details>

**Câu 2.** Khác nhau giữa seasonal plot và subseries plot là:

- A. Seasonal plot vẽ mỗi vòng lặp (mỗi tuần, mỗi năm) một đường chồng lên nhau; subseries plot gom mỗi "mùa" (mỗi thứ, mỗi
  tháng) vào một ô riêng
- B. Hai tên gọi của cùng một hình
- C. Seasonal plot chỉ dùng cho dữ liệu tháng; subseries plot chỉ dùng cho dữ liệu giờ
- D. Subseries plot cho thấy hình dạng của một vòng lặp; seasonal plot cho thấy một mùa đổi thế nào qua các năm

<details>
<summary>Đáp án</summary>

**A** (mục 4.3). Seasonal plot trả lời "hình dạng một vòng lặp ra sao, vòng nào lệch"; subseries plot trả lời "một mùa cụ thể đổi
thế nào qua thời gian". **B sai**: hai hình xếp dữ liệu khác nhau; nhầm này dễ gặp vì `month_plot` của statsmodels có chữ
"seasonal" mà vẽ subseries. **C sai**: cả hai dùng được cho mọi tần suất; buổi này vẽ seasonal plot theo giờ trong tuần và
subseries theo tháng. **D sai**: đảo vai trò của hai hình.

</details>

**Câu 3.** Vì sao không nên dùng biểu đồ trục kép để "chứng minh" hai chuỗi đi cùng nhau?

- A. Vì matplotlib vẽ trục kép bị lỗi
- B. Vì thang của trục thứ hai do người vẽ chọn, nên có thể làm hai đường trùng nhau hay tách nhau tuỳ ý
- C. Vì hai chuỗi phải cùng đơn vị mới vẽ được
- D. Vì trục kép luôn đi kèm trục y cắt

<details>
<summary>Đáp án</summary>

**B** (mục 4.6, ví dụ A và B): cùng dữ liệu, trục phải 20–22 cho hai đường trùng khít, trục phải 0–30 cho B nằm ngang. Muốn nói
về quan hệ thì vẽ scatter và tính $r$, hoặc đánh chỉ số. **A sai**: `twinx` chạy bình thường, vấn đề là cách đọc. **C sai**:
trục kép sinh ra chính để vẽ hai đơn vị khác nhau. **D sai**: hình gốc của buổi có cả hai lỗi, nhưng đó là hai lỗi riêng; trục
kép vẫn gây hiểu nhầm dù cả hai trục bắt đầu từ 0.

</details>

**Câu 4.** Trên thang log, hai đoạn có độ dốc bằng nhau nghĩa là:

- A. Hai đoạn tăng cùng một số đơn vị
- B. Hai đoạn tăng cùng một phần trăm
- C. Hai đoạn có cùng giá trị
- D. Không có ý nghĩa gì

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): trên thang log, 100 → 200 và 200 → 400 cao bằng nhau vì cùng gấp đôi, dù tăng tuyệt đối là 100 và 200. **A
sai**: đó là thang thường. **C sai**: độ dốc nói về thay đổi, không nói về mức. **D sai**: chính vì nghĩa này mà dùng thang log
khi quan tâm tốc độ tăng (lượt thuê 2011: tháng 3 → 4 tăng +48,1%, nhanh nhất theo phần trăm dù không tăng nhiều lượt nhất).

</details>

## Vận dụng

**Câu 5.** Bạn có số cuộc gọi tổng đài theo giờ trong 3 năm. Chọn **ba** biểu đồ để trả lời: (a) có mùa vụ tuần không; (b) giờ
nào khó dự báo nhất; (c) có ngày dữ liệu bất thường không. Nói đọc gì trên mỗi hình.

<details>
<summary>Đáp án</summary>

(a) **Heatmap giờ × thứ**: hai dòng cuối tuần có khác năm dòng đầu không (mục 4.4); hoặc **ACF tới trễ 336**: đỉnh ở 168 có cao
hơn đỉnh 144 không (mục 4.5). (b) **Boxplot theo giờ**: giờ nào hộp rộng nhất (IQR lớn nhất), tách ngày làm việc với ngày nghỉ.
(c) **Đường tổng theo ngày**, không làm trơn, không gộp tháng (mục 4.2): ngày rơi sát 0 hoặc vọt cao; kiểm thêm ngày đó có đủ
24 giờ số liệu không. Chọn biểu đồ đường gộp tháng cho (c) là sai: gộp tháng xoá mất ngày bất thường.

</details>

**Câu 6.** Tính tay $r_1$ theo công thức mục 4.5 cho chuỗi tăng đều $y = 2, 4, 6, 8, 10$.

<details>
<summary>Đáp án</summary>

Trung bình $\bar y = 30 / 5 = 6$. Độ lệch: −4, −2, 0, 2, 4. Mẫu số: 16 + 4 + 0 + 4 + 16 = 40. Tử số, $t$ = 2 … 5 (mỗi điểm nhân
điểm ngay trước): (−2)(−4) + 0 × (−2) + 2 × 0 + 4 × 2 = 8 + 0 + 0 + 8 = 16. $r_1 = 16 / 40 =$ **0,4**. Dương vì chuỗi có xu hướng:
nửa đầu cùng dưới trung bình, nửa sau cùng trên. Nhầm hay gặp: chia cho số cặp (4) thay vì tổng bình phương độ lệch, ra 4; hoặc
cộng cả tích của $t = 1$ (không có điểm đứng trước).

</details>

**Câu 7.** Một bạn vẽ lag plot trễ 12 giờ của lượt thuê xe, thấy $r = -0{,}14$ và hai nhánh bám hai trục, rồi kết luận "giờ này
đông thì 12 giờ sau vắng — quan hệ âm, dùng làm thông tin dự báo ngược dấu". Nhận xét.

<details>
<summary>Đáp án</summary>

Sai. Hai nhánh là **đỉnh ghép với đáy** của mùa vụ ngày: giờ đông buổi sáng ghép với giờ vắng lúc đêm hôm trước, giờ đông buổi
chiều ghép với rạng sáng (mục 4.5). Hệ số −0,14 trộn hai nhánh nên gần 0 và không dùng được. Thông tin tốt hơn là cùng giờ hôm
qua (trễ 24, $r$ = 0,82) hay cùng giờ tuần trước (trễ 168, $r$ = 0,88).

</details>

**Câu 8.** Ô (CN, 13h) của một heatmap lấy từ 5 Chủ nhật: 380, 350, **90** (hôm đó mưa bão), 400, 370. Tính số heatmap tô ở ô
này, rồi tính trung vị, quantile 0,25 và 0,75 của boxplot. Số nào tả "Chủ nhật 13h bình thường" tốt hơn?

<details>
<summary>Đáp án</summary>

Heatmap tô **trung bình**: (380 + 350 + 90 + 400 + 370) / 5 = 1.590 / 5 = **318**. Xếp tăng dần 90, 350, 370, 380, 400: trung
vị **370**; quantile 0,25 là số thứ 2, **350** (ít nhất 1,25 số phải ≤ nó); quantile 0,75 là số thứ 4, **380**. Trung vị 370
tả ngày bình thường tốt hơn: trung bình 318 thấp hơn 4 trên 5 ngày vì một ngày bão kéo xuống (mục 4.4). Nhầm hay gặp: lấy số
thứ 3 của dãy **chưa xếp** (90) làm trung vị.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Heatmap trung bình lượt thuê mỗi giờ (trích):

| Thứ \ giờ | 8h | 13h | 17h |
|---|---|---|---|
| T2 | 412 | 206 | 502 |
| T4 | 488 | 186 | 513 |
| T7 | 114 | 385 | 334 |
| CN | 84 | 375 | 319 |

Một bạn kết luận: "Thứ Bảy và Chủ nhật ít người thuê xe hơn, nên giảm số xe cả ngày cuối tuần." Sai ở đâu?

<details>
<summary>Đáp án</summary>

Heatmap cho thấy **hình dạng** ngày khác nhau, không phải tổng thấp hơn. Lúc 13h cuối tuần (375–385) cao **gần gấp đôi** ngày
thường (186–206). Tổng ngày trung bình (mục 4.3): T7 4.653 và CN 4.523, so với T2 4.708, chỉ thấp hơn vài phần trăm. Kết luận
đúng: cuối tuần nhu cầu **dời** từ giờ đi làm sang giữa ngày; phân bổ xe theo giờ, không cắt cả ngày.

</details>

**Câu 10.** Biểu đồ trục kép: tổng lượt thuê theo tháng 2012 (trục trái 90.000–220.000) và nhiệt độ (trục phải 5–32 °C), hai
đường gần trùng, tiêu đề "Lượt thuê bám sát nhiệt độ". Scatter 12 tháng cho $r = 0{,}91$. Tháng 7 nóng nhất (30,8 °C, 203.607
lượt); tháng 9 chỉ 25,4 °C nhưng 218.573 lượt. Chỉ ra ba vấn đề của biểu đồ gốc và điều scatter cho thấy mà trục kép che.

<details>
<summary>Đáp án</summary>

(1) **Trục kép**: thang phải được chọn để hai đường đè nhau, nên sự trùng khít là do người vẽ. (2) **Trục y cắt** ở 90.000:
tháng 1 (96.744 lượt) trông gần như bằng 0, mức tăng bị phóng to. (3) **Tiêu đề** khẳng định một quan hệ mà hình không cho kiểm
(không có scatter, không có $r$). Scatter cho thấy quan hệ mạnh nhưng **không tăng mãi ở vùng nóng**: tháng 9 mát hơn tháng 7 mà
lượt thuê cao hơn. Ngoài ra lượt thuê 2012 còn đang tăng theo thời gian (xu hướng), trộn vào con số $r$ (mục 4.6).

</details>
