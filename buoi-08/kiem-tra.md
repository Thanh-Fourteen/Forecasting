# Kiểm tra buổi 8 — Tương quan giữa các chuỗi

## Nhắc lại khái niệm

**Câu 1.** Hai chuỗi đều có xu hướng tăng và cho $r$ = 0,97. Bằng chứng nào **mạnh nhất** cho thấy đây là tương quan giả?

- A. $R^2$ của hồi quy rất cao
- B. $t$ của hệ số rất lớn
- C. Durbin–Watson của phần dư gần 0, và $r$ sau sai phân gần 0
- D. Cỡ mẫu lớn

<details>
<summary>Đáp án</summary>

**C** (mục 4.2). DW gần 0 nói phần dư tự tương quan, mô hình sai; $r$ sụp sau sai phân nói quan hệ tháng-với-tháng không có. **A, B sai**:
$R^2$ cao và $t$ lớn chính là **triệu chứng** hay gặp của tương quan giả (CPI × dân số: $R^2$ 0,95, $t$ 88,6), không phải bằng chứng chống
lại nó. **D sai**: mẫu lớn không sửa được mô hình sai, còn làm $t$ phình to thêm.

</details>

**Câu 2.** Mutual information khác Pearson ở chỗ:

- A. MI chỉ đo quan hệ đường thẳng
- B. MI bắt được mọi dạng phụ thuộc, kể cả chữ U
- C. MI luôn nằm trong khoảng −1 tới 1
- D. MI không cần dữ liệu

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): ví dụ lạnh/vừa/nóng có Pearson = 0 mà MI ≈ 0,637 nat. **A sai**: đó là Pearson. **C sai**: MI không âm, không có dấu, và
không bị chặn trên bởi 1 (ví dụ nhiệt độ × tải là 0,862 nat; dữ liệu càng phụ thuộc chặt thì càng lớn). **D sai**: MI ước lượng từ dữ liệu
như mọi hệ số khác.

</details>

**Câu 3.** Prewhitening trước khi tính tương quan chéo nghĩa là:

- A. Làm trơn cả hai chuỗi
- B. Khớp mô hình AR cho chuỗi **giải thích**, rồi lọc **cả hai** chuỗi bằng cùng bộ hệ số
- C. Trừ trung bình rồi chia độ lệch chuẩn cho hai chuỗi
- D. Bỏ ngoại lai

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): bỏ phần $x$ tự đoán được từ quá khứ của nó, để hình dạng tương quan chéo không còn là tự tương quan của $x$. **A sai**: làm
trơn còn làm tự tương quan mạnh hơn, tương quan chéo càng nhoè. **C sai**: chuẩn hoá đổi thang, không bỏ được tự tương quan (tương quan
vốn đã chuẩn hoá sẵn). **D sai**: ngoại lai không phải nguyên nhân tương quan chéo nhoè.

</details>

**Câu 4.** "$X$ Granger-gây-ra $Y$" nghĩa là:

- A. $X$ gây ra $Y$
- B. Quá khứ của $X$ giúp dự báo $Y$ tốt hơn so với chỉ dùng quá khứ của $Y$
- C. $X$ và $Y$ tương quan
- D. $Y$ xảy ra trước $X$

<details>
<summary>Đáp án</summary>

**B** (mục 4.6): kiểm định chỉ so sai số của hai cách dự báo. **A sai**: một biến gây nhiễu chung (nhịp ngày) làm kiểm định có ý nghĩa cả
khi không có nhân quả, thậm chí ở chiều vô lý "tải điện → nhiệt độ". **C sai**: tương quan cùng lúc không đủ; Granger hỏi về **quá khứ** của
$X$. **D sai**: ngược thứ tự; nếu có gì thì là $X$ đi trước.

</details>

## Vận dụng

**Câu 5.** Với `ccf_tu_viet(x, y)[k]` = corr($x_t$, $y_{t+k}$), bạn thấy đỉnh ở $k$ = 4 (sau prewhitening). Diễn giải? Gọi
`statsmodels.tsa.stattools.ccf` thế nào để ra cùng con số?

<details>
<summary>Đáp án</summary>

$x$ **đi trước** $y$ 4 bước: giá trị $x$ hôm nay khớp nhất với $y$ sau 4 bước (mục 4.4). statsmodels dùng quy ước ngược,
`ccf(a, b)[k]` = corr($a_{t+k}$, $b_t$), nên phải gọi `ccf(y, x)`: corr($y_{t+4}$, $x_t$). Nhầm hay gặp: gọi `ccf(x, y)` rồi đọc sai hướng;
luôn thử trước với chuỗi giả $y_t = x_{t-3}$.

</details>

**Câu 6.** Nhiệt độ 10 °C và 30 °C. Tính CDD và HDD (mốc 18,33 °C). Vì sao hồi quy theo CDD + HDD giải thích tốt hơn hồi quy theo nhiệt độ?

<details>
<summary>Đáp án</summary>

10 °C: CDD = 0, HDD = 18,33 − 10 = 8,33. 30 °C: CDD = 30 − 18,33 = 11,67, HDD = 0. Hồi quy theo nhiệt độ chỉ có **một** độ dốc cho cả hai
phía; CDD và HDD cho **hai** độ dốc (lạnh hơn thì tải tăng, nóng hơn thì tải tăng). ERCOT 2024: $R^2$ 0,379 → 0,812 (mục 4.3). Nhầm hay
gặp: đưa cả nhiệt độ lẫn CDD, HDD vào cùng mô hình; ba biến này phụ thuộc tuyến tính chính xác (hộp Nâng cao).

</details>

**Câu 7.** Bạn tính MI giữa hai chuỗi giá cổ phiếu (tự tương quan rất mạnh), hoán vị từng điểm 1.000 lần và được p = 0,001. Kết luận có
đáng tin không? Làm lại thế nào?

<details>
<summary>Đáp án</summary>

**Không** (mục 4.3). Hoán vị từng điểm phá tự tương quan, dữ liệu xáo lộn xộn hơn dữ liệu thật nên MI của chúng quá nhỏ, p nhỏ giả. Trong
buổi, hai chuỗi AR **độc lập** cho p = 0,005 khi hoán vị từng điểm nhưng p = 0,055 khi hoán vị theo khối 200. Làm lại bằng **hoán vị theo
khối** dài hơn quãng mà chuỗi còn tự tương quan.

</details>

**Câu 8.** Mô hình dự báo tải điện ngày mai dùng: nhiệt độ ngày mai, giá khí đốt ngày mai, tải điện hôm nay. Biến nào dùng được cho dự báo
thật (ex-ante)? Cần thêm gì?

<details>
<summary>Đáp án</summary>

Tải điện hôm nay: đã biết lúc ra dự báo, dùng được. Nhiệt độ ngày mai: chưa biết, nhưng có **dự báo thời tiết**; dùng được nếu huấn luyện
và chấm bằng chính nhiệt độ **dự báo**, kèm sai số của nó. Giá khí đốt ngày mai: chưa biết, không có dự báo tin cậy; phải dự báo nó trước,
hoặc dùng giá hôm nay. Dùng giá trị thật của ngày mai chỉ là ex-post (mục 4.6), không phải dự báo thật.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo: "Tương quan giữa nhiệt độ và tải điện ERCOT năm 2024 là 0,62, quan hệ trung bình. Nhiệt độ chỉ giải thích được một phần
nhu cầu." Dùng các số sau để viết lại kết luận: $R^2$ theo nhiệt độ 0,379; $R^2$ theo CDD + HDD 0,812; $r$ khi nhiệt độ ≤ 18,33 °C là −0,649
(2.877 giờ); $r$ khi > 18,33 °C là +0,910 (5.900 giờ).

<details>
<summary>Đáp án</summary>

Quan hệ **rất mạnh nhưng hình chữ U và đổi dấu** (mục 4.3): dưới 18,33 °C càng lạnh tải càng cao ($r$ = −0,649), trên mốc càng nóng tải càng
cao ($r$ = +0,910). Con số 0,62 trộn hai nhánh ngược dấu nên nghe như "trung bình". Mô hình hai nhánh CDD/HDD giải thích 81,2% dao động, so
với 37,9% của đường thẳng. Kết luận đúng: "nhiệt độ giải thích phần lớn dao động của tải nếu mô hình hoá theo hình chữ U; hệ số tương quan
tuyến tính không phải thước đo phù hợp ở đây."

</details>

**Câu 10.** Bảng kết quả Granger trên dữ liệu giờ năm 2024 (độ trễ 1–4):

| Chiều | p |
|---|---|
| CDD → tải điện | < 0,001 |
| tải điện → CDD | < 0,001 |

Nhóm phân tích kết luận: "Nhiệt độ gây ra thay đổi tải điện; ngoài ra tải điện cũng làm nóng thành phố (hiệu ứng đảo nhiệt)." Nhận xét và đề
xuất cách kiểm tốt hơn.

<details>
<summary>Đáp án</summary>

Hai chiều cùng có ý nghĩa là dấu hiệu của **biến gây nhiễu chung**: cả hai chuỗi chạy theo nhịp 24 giờ, nên quá khứ bên nào cũng "đoán"
được bên kia (mục 4.6). Kiểm định này không đo được hiệu ứng đảo nhiệt. Cách tốt hơn: (1) bỏ mùa vụ ngày và tuần của cả hai chuỗi (buổi 6)
rồi chạy lại; (2) prewhiten rồi xem tương quan chéo ở chiều "tải đi trước CDD" có vượt dải không; (3) nhớ Granger đòi chuỗi dừng; (4) viết
kết luận là "quá khứ X giúp dự báo Y", và dựa vào cơ chế vật lý thay vì một p-value.

</details>
