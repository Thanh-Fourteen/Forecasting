# Kiểm tra buổi 18 — Hồi quy chuỗi thời gian và hồi quy động

## Nhắc lại khái niệm

**Câu 1.** Dấu hiệu nào cho thấy một hồi quy giữa hai chuỗi thời gian có thể là hồi quy giả?

- A. R² cao, p nhỏ, và phần dư tự tương quan mạnh (Ljung–Box p ≈ 0)
- B. R² thấp
- C. Hệ số âm
- D. Hai chuỗi có đơn vị khác nhau

<details>
<summary>Đáp án</summary>

**A** (mục 4.2): hai chuỗi cùng trôi theo thời gian cho R² cao và p nhỏ; phần dư lệch một phía nhiều kỳ liền là dấu hiệu p-value không tin được.
**B sai**: hồi quy giả thường cho R² **cao**. **C sai**: dấu của hệ số không nói gì về quan hệ giả hay thật (ví dụ hành khách còn đổi dấu khi
thêm xu hướng). **D sai**: đơn vị khác nhau là bình thường trong hồi quy.

</details>

**Câu 2.** Hồi quy động khác hồi quy thường ở chỗ:

- A. Dùng nhiều biến giải thích hơn
- B. Phần sai số được mô hình bằng ARIMA thay vì coi là độc lập
- C. Không cần hệ số chặn
- D. Chỉ dùng cho dữ liệu theo giờ

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): $y_t = \beta x_t + \eta_t$ với $\eta_t$ là ARIMA; phần dư của ARIMA đó mới phải là nhiễu trắng. **A sai**: số biến có thể như
nhau (bảng mục 4.4: hồi quy thường và hồi quy động dùng cùng biến). **C sai**: hệ số chặn vẫn có (hoặc bị sai phân loại bỏ). **D sai**: ví dụ
hành khách là dữ liệu tháng.

</details>

**Câu 3.** Dự báo tải điện ngày mai bằng hồi quy có biến nhiệt độ. Cho đoạn dự báo, dùng nhiệt độ nào?

- A. Nhiệt độ đo thật ngày mai
- B. Dự báo nhiệt độ ngày mai ra từ hôm nay
- C. Nhiệt độ hôm nay lặp lại
- D. Trung bình nhiệt độ của năm

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): dự báo ex-ante chỉ dùng thông tin có lúc ra dự báo. **A sai**: nhiệt độ đo thật ngày mai chưa có; dùng nó là ex-post, chấm như
vậy là gian lận. **C, D sai**: dùng được nhưng bỏ phí dự báo thời tiết, thứ đã có sẵn và sát hơn.

</details>

**Câu 4.** Vì sao Prophet mặc định đoán sai quanh Tết?

- A. Prophet không có nhịp năm
- B. Mặc định Prophet không có lễ nào; nhịp năm Fourier theo lịch dương, còn Tết xê dịch theo lịch âm
- C. Dữ liệu quá ngắn
- D. Prophet không nhận dữ liệu theo ngày

<details>
<summary>Đáp án</summary>

**B** (mục 4.5–4.6): $h(t)$ = 0 khi chưa khai lễ; Fourier năm lặp đúng ngày dương, còn mùng 1 Tết lệch tới vài tuần mỗi năm. **A sai**: Prophet
có Fourier năm. **C sai**: dữ liệu học có 8 năm, đủ 8 lần Tết; chỉ là mô hình không biết ngày nào là Tết. **D sai**: ví dụ của buổi là dữ liệu
ngày.

</details>

## Vận dụng

**Câu 5.** Mô hình theo quý đã khớp: $\hat y_t = 100 + 1{,}5\,t - 10\,Q2_t + 5\,Q3_t + 12\,Q4_t$. Dự báo quý thứ 20 (quý 4) và quý thứ 21
(quý 1).

<details>
<summary>Đáp án</summary>

Quý 20: 100 + 1,5 × 20 + 12 = **142**. Quý 21: 100 + 1,5 × 21 = **131,5** (quý 1 là mốc, không có biến giả) (mục 4.1). Nhầm hay gặp: cộng
cả hệ số của quý khác, hoặc nghĩ quý 1 cần một hệ số riêng.

</details>

**Câu 6.** $a = (3, 4, 6, 7, 9, 10)$, $b = (20, 22, 23, 25, 26, 28)$. Tương quan trên mức gần 1. Tính sai phân của hai chuỗi và cho biết tương
quan trên sai phân dương hay âm. Kết luận gì?

<details>
<summary>Đáp án</summary>

$a'$ = 1, 2, 1, 2, 1 (TB 1,4; lệch −0,4; 0,6; −0,4; 0,6; −0,4). $b'$ = 2, 1, 2, 1, 2 (TB 1,6; lệch 0,4; −0,6; 0,4; −0,6; 0,4). Mọi tích đều âm:
tương quan sai phân **−1**. Tháng $a$ tăng nhiều thì $b$ tăng ít: tương quan dương trên mức chỉ đến từ việc cả hai cùng đi lên (mục 4.2).
Nhầm hay gặp: tin tương quan trên mức.

</details>

**Câu 7.** $y_t = 5 x_t + \eta_t$, $\eta_t = 0{,}6\,\eta_{t-1} + \varepsilon_t$. Hôm nay $\eta$ = 10. Dự báo $x$ hai ngày tới là 4 và 6. Tính dự báo
$y$ hai ngày tới.

<details>
<summary>Đáp án</summary>

Ngày 1: 5 × 4 + 0,6 × 10 = 20 + 6 = **26**. Ngày 2: $\eta$ dự báo 0,6 × 6 = 3,6, nên 30 + 3,6 = **33,6** (mục 4.3). Nhầm hay gặp: giữ $\eta$ = 10
cho cả hai ngày, hoặc bỏ hẳn phần $\eta$ như hồi quy thường (20 và 30).

</details>

**Câu 8.** Tám tháng. Tháng 3 có khuyến mãi một tháng; từ tháng 6 một cửa hàng đối thủ mở cạnh bên. Viết hai cột biến can thiệp. Hệ số của
cột thứ hai là −40 nghĩa là gì?

<details>
<summary>Đáp án</summary>

Xung: (0, 0, 1, 0, 0, 0, 0, 0). Bậc: (0, 0, 0, 0, 0, 1, 1, 1). Hệ số −40 của cột bậc: từ tháng 6 trở đi, mỗi tháng thấp hơn 40 đơn vị so với
khi không có đối thủ (mục 4.5). Nhầm hay gặp: dùng xung cho cửa hàng đối thủ; xung chỉ tác động đúng một tháng.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo của một đồng nghiệp, dữ liệu tháng 2010–2019:

| Hồi quy doanh số của công ty ~ dân số thành phố | Giá trị |
|---|---|
| hệ số | 0,42 |
| p | 0,000001 |
| R² | 0,91 |
| Ljung–Box p của phần dư | 0,0000 |

"Mỗi nghìn dân thêm mang lại 0,42 tỷ doanh số, rất có ý nghĩa thống kê." Chỉ ra lỗi và phải làm gì.

<details>
<summary>Đáp án</summary>

Phần dư tự tương quan mạnh (Ljung–Box p ≈ 0), nên công thức p-value của hồi quy thường không dùng được: p = 0,000001 có thể là hồi quy giả,
vì cả doanh số và dân số cùng tăng theo thời gian (mục 4.2). Phải làm lại bằng hồi quy động (sai số ARIMA, lấy sai phân nếu không dừng) và
kiểm phần dư trắng; nếu hệ số hết ý nghĩa thì quan hệ là giả (mục 4.3). Nhầm hay gặp: coi R² cao là bằng chứng.

</details>

**Câu 10.** Bảng backtest 24 cửa sổ, dự báo tải ngày tới:

| Cách | MAE trung bình (MW) | DM so với hồi quy động |
|---|---|---|
| hồi quy động | 2.082 | — |
| seasonal naive 24 giờ | 2.173 | p = 0,76 |
| Prophet mặc định | 2.998 | p = 0,017 |

"Hồi quy động tốt hơn seasonal naive 4%, và tốt hơn Prophet 31%. Thay cả hai bằng hồi quy động." Nhận xét.

<details>
<summary>Đáp án</summary>

Phần "tốt hơn seasonal naive" không có bằng chứng: DM p = 0,76, chênh 4% nằm trong dao động giữa các ngày (mục 4.4). Chỉ phần "tốt hơn Prophet"
có ý nghĩa (p = 0,017). Kết luận đúng: hồi quy động ngang seasonal naive trên dữ liệu này, thắng Prophet mặc định; muốn thay seasonal naive thì
cần thêm cửa sổ hoặc mô hình tốt hơn. Nhầm hay gặp: đọc chênh MAE mà không đọc DM.

</details>
