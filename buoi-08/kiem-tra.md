# Kiểm tra buổi 8 — Tương quan giữa các chuỗi

## Nhắc lại khái niệm

**Câu 1.** Hai chuỗi đều có xu hướng tăng và cho r = 0,97. Bằng chứng nào **mạnh nhất** cho thấy đây là tương quan giả?

- A. R² của hồi quy rất cao
- B. t của hệ số rất lớn
- C. Durbin–Watson của phần dư gần 0, và r sau sai phân gần 0
- D. Cỡ mẫu lớn

<details>
<summary>Đáp án</summary>

**C.** Granger & Newbold: "a high value for R² … combined with a low value of d, is no indication of a true relationship". A và B là **triệu chứng** của
hồi quy giả chứ không phải bằng chứng ngược lại; cỡ mẫu lớn còn làm t phình to hơn (Phillips 1986: thống kê t phân kỳ khi T → ∞).

</details>

**Câu 2.** Mutual information khác Pearson ở chỗ:

- A. MI chỉ đo quan hệ tuyến tính
- B. MI bắt được mọi dạng phụ thuộc, kể cả phi tuyến và không đơn điệu
- C. MI luôn nằm trong [−1, 1]
- D. MI không cần dữ liệu

<details>
<summary>Đáp án</summary>

**B.** MI ≥ 0, không có dấu và không giới hạn trên (C sai), đo bằng nat khi dùng log tự nhiên. Với $y = x^2$, Pearson ≈ 0 còn MI > 0.

</details>

**Câu 3.** Prewhitening trước khi tính CCF nghĩa là:

- A. Làm trơn cả hai chuỗi
- B. Khớp mô hình AR cho chuỗi **giải thích**, rồi lọc **cả hai** chuỗi bằng cùng bộ hệ số
- C. Chuẩn hoá z-score hai chuỗi
- D. Bỏ ngoại lai

<details>
<summary>Đáp án</summary>

**B.** Penn State STAT 510: xác định mô hình cho x, lọc y bằng chính mô hình đó, rồi tính CCF giữa phần dư. Mục đích là bỏ cấu trúc thời gian **của x**
để CCF không bị nhoè theo nhịp của chính nó.

</details>

**Câu 4.** "X Granger-causes Y" nghĩa là:

- A. X gây ra Y
- B. Quá khứ của X giúp dự báo Y tốt hơn so với chỉ dùng quá khứ của Y
- C. X và Y tương quan
- D. Y xảy ra trước X

<details>
<summary>Đáp án</summary>

**B.** Granger sau này gọi quan hệ này là "temporally related". Nếu X và Y cùng bị một quá trình thứ ba điều khiển (nhịp ngày, mùa vụ), kiểm định vẫn
"có ý nghĩa" ở cả hai chiều — như cặp nhiệt độ × tải điện trong buổi.

</details>

## Vận dụng

**Câu 5.** Với `ccf_tu_viet(x, y)[k] = corr(x_t, y_{t+k})`, bạn thấy đỉnh ở k = 4. Diễn giải? Nếu dùng `statsmodels.tsa.stattools.ccf` thì gọi thế nào để
ra cùng kết quả?

<details>
<summary>Đáp án</summary>

x **đi trước** y 4 bước: giá trị x hôm nay khớp nhất với y sau 4 bước → x là biến dẫn dắt. statsmodels dùng quy ước ngược: `ccf(y, x)` mới cho corr tại
lag k bằng corr(y_{t+k}, x_t) = corr(x_t, y_{t+k}). Luôn kiểm bằng chuỗi mô phỏng $y_t = x_{t-3}$ trước khi tin hướng.

</details>

**Câu 6.** Nhiệt độ 10 °C và 30 °C. Tính CDD và HDD (mốc 18,33 °C). Vì sao hồi quy theo CDD + HDD giải thích tốt hơn hồi quy theo nhiệt độ?

<details>
<summary>Đáp án</summary>

10 °C: CDD = 0, HDD = 8,33. 30 °C: CDD = 11,67, HDD = 0. Hồi quy theo $T$ ép **một** hệ số cho cả hai phía; tách CDD/HDD cho phép **hai độ dốc** (âm khi
lạnh, dương khi nóng). Trên ERCOT 2024: $R^2$ 0,379 → 0,813. Lưu ý không đưa cả $T$ lẫn CDD, HDD vào cùng mô hình: $T = \text{CDD} - \text{HDD} + 18{,}33$
là phụ thuộc tuyến tính chính xác.

</details>

**Câu 7.** Bạn tính MI giữa hai chuỗi giá cổ phiếu (rất tự tương quan), hoán vị ngẫu nhiên từng điểm 1.000 lần và được p = 0,001. Kết luận có đáng tin
không? Làm lại thế nào?

<details>
<summary>Đáp án</summary>

**Không.** Hoán vị từng điểm phá tự tương quan, nên phân phối rỗng quá hẹp → p nhỏ giả. Trong buổi: hai chuỗi AR(0,99) **độc lập** cho ngưỡng 95% là
0,025 khi hoán vị từng điểm (p = 0,005) so với 0,329 khi hoán vị theo khối 200 (p = 0,055). Làm lại bằng **hoán vị theo khối** dài hơn thời gian tương
quan, hoặc so với chuỗi thay thế (surrogate) giữ nguyên phổ.

</details>

**Câu 8.** Mô hình dự báo tải điện ngày mai của bạn dùng: nhiệt độ ngày mai, giá khí đốt ngày mai, tải điện hôm nay. Biến nào dùng được cho dự báo thật
(ex-ante)? Cần thêm gì?

<details>
<summary>Đáp án</summary>

Tải điện hôm nay: biết. Nhiệt độ ngày mai: **không biết**, nhưng có **dự báo thời tiết** — dùng được với điều kiện huấn luyện bằng chính dự báo (hoặc
tính thêm sai số của dự báo thời tiết vào khoảng dự báo). Giá khí đốt ngày mai: không biết và không có dự báo tin cậy → phải dự báo nó trước, hoặc dùng
giá hôm nay (biến trễ). FPP: dùng giá trị thật của biến giải thích trong tương lai chỉ cho **ex-post**, "not genuine forecasts".

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo: "Tương quan giữa nhiệt độ và tải điện ERCOT năm 2024 là 0,62 — quan hệ trung bình. Nhiệt độ chỉ giải thích được một phần nhu cầu."
Dùng các số sau để viết lại kết luận: $R^2$ theo $T$ = 0,379; $R^2$ theo CDD + HDD = 0,813; r khi $T \le 18{,}33$ = −0,649 (2.877 giờ); r khi
$T > 18{,}33$ = +0,910 (5.900 giờ).

<details>
<summary>Đáp án</summary>

Quan hệ **rất mạnh nhưng phi tuyến và đổi dấu**: dưới 18,33 °C càng lạnh tải càng cao (r = −0,649), trên ngưỡng càng nóng tải càng cao (r = +0,910). Một
hệ số tuyến tính 0,62 trộn hai chế độ nên nghe như "trung bình"; mô hình hai nhánh CDD/HDD giải thích 81,3% phương sai so với 37,9%. Kết luận đúng:
"nhiệt độ giải thích phần lớn biến động tải điện nếu mô hình hoá theo dạng chữ U; hệ số tương quan tuyến tính không phải thước đo phù hợp ở đây."

</details>

**Câu 10.** Bảng kết quả Granger trên dữ liệu giờ năm 2024 (ssr-F, trễ 1–4):

| Chiều | p |
|---|---|
| CDD → tải điện | < 0,001 |
| tải điện → CDD | < 0,001 |

Nhóm phân tích kết luận: "Nhiệt độ gây ra thay đổi tải điện; ngoài ra tải điện cũng ảnh hưởng ngược lại nhiệt độ đô thị (hiệu ứng đảo nhiệt)." Nhận xét
và đề xuất cách kiểm tra tốt hơn.

<details>
<summary>Đáp án</summary>

Kết luận chiều thứ hai gần như chắc chắn sai: hiệu ứng đảo nhiệt đô thị có thật nhưng **không** đo được bằng kiểm định này. Cả hai chuỗi có **nhịp 24
giờ chung**, nên quá khứ bên nào cũng "dự báo" được bên kia — đúng trường hợp Wikipedia mô tả: "If both X and Y are driven by a common third process
with different lags…". Cách kiểm tốt hơn: (1) khử mùa vụ giờ-trong-tuần của cả hai rồi chạy lại; (2) prewhitening rồi xem CCF ở trễ **âm** (tải dẫn
nhiệt độ) có vượt dải không; (3) dựa vào cơ chế vật lý và thí nghiệm tự nhiên (đợt nắng nóng), không dựa vào một p-value; (4) nhớ Granger đòi chuỗi
dừng — dữ liệu giờ chưa khử mùa vụ thì vi phạm.

</details>
