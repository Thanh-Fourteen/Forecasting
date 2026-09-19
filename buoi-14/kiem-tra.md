# Kiểm tra buổi 14 — Baseline và chỉ số đánh giá

## Nhắc lại khái niệm

**Câu 1.** Chỉ được dự báo một hằng số, và bạn bị chấm bằng MAE. Hằng số tốt nhất là:

- A. Trung bình của dữ liệu
- B. Trung vị của dữ liệu
- C. Giá trị lớn nhất
- D. Quantile 0,9

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): MAE nhỏ nhất ở trung vị; với $(1, 2, 3, 4, 20)$ đó là 3. **A sai**: trung bình là con số RMSE ưa. **C sai**: xa phần lớn dữ
liệu nên MAE lớn. **D sai**: quantile 0,9 hợp khi thiếu đắt hơn thừa nhiều, không phải khi chấm bằng MAE.

</details>

**Câu 2.** Mẫu số của MASE là:

- A. MAE của seasonal naive trên kỳ chấm
- B. MAE của seasonal naive trên phần học
- C. Trung bình của các giá trị thực tế trên kỳ chấm
- D. MAE của chính mô hình trên phần học

<details>
<summary>Đáp án</summary>

**B** (mục 4.5): con số của quá khứ, cố định trước khi chấm. **A sai**: đó là lỗi của code đầu buổi, vừa sai định nghĩa vừa dùng thông tin kỳ
chấm. **C sai**: chia cho mức là cách của MAPE/WAPE. **D sai**: đó là phần dư của mô hình, không phải mốc chung để so giữa các mô hình.

</details>

**Câu 3.** Phần dư khác sai số dự báo ở chỗ:

- A. Phần dư tính trên phần học, nơi mô hình đã thấy dữ liệu; sai số dự báo tính trên kỳ chấm
- B. Phần dư luôn lớn hơn sai số dự báo
- C. Phần dư có dấu, sai số dự báo không có dấu
- D. Hai thứ là một

<details>
<summary>Đáp án</summary>

**A** (mục 4.2). **B sai**: thường ngược lại, vì trên phần học mô hình "trả bài" đề đã xem. **C sai**: cả hai đều là thực tế trừ một con số của
mô hình, đều có dấu. **D sai**: lẫn hai thứ là cách báo độ chính xác đẹp giả tạo.

</details>

**Câu 4.** Kỳ chấm có vài ngày thực tế bằng 0. Chỉ số nào **không** tính được?

- A. MAPE
- B. MAE
- C. WAPE (tổng thực tế khác 0)
- D. MASE

<details>
<summary>Đáp án</summary>

**A** (mục 4.4): chia cho thực tế 0 ra vô hạn. **B sai**: MAE không chia gì. **C sai**: WAPE chia cho **tổng**, còn khác 0 là tính được.
**D sai**: MASE chia cho sai số seasonal naive trên phần học, không chia cho thực tế.

</details>

## Vận dụng

**Câu 5.** Chuỗi $(20, 24, 22, 26, 24, 28)$, chu kỳ $m$ = 2. Tính dự báo 2 bước của bốn baseline.

<details>
<summary>Đáp án</summary>

Trung bình 144 / 6 = **24; 24**. Naive **28; 28**. Seasonal naive lặp (24, 28): **24; 28**. Drift: độ dốc (28 − 20) / 5 = 1,6 → **29,6; 31,2**
(mục 4.1). Nhầm hay gặp: drift lấy độ dốc của hai điểm cuối (28 − 24 = 4); drift nối điểm **đầu** với điểm **cuối**.

</details>

**Câu 6.** Sai số (thực tế − dự báo) của 4 ngày là $(3, -1, -2, 4)$. Tính MAE, RMSE, ME. Dự báo đang lệch về phía nào?

<details>
<summary>Đáp án</summary>

MAE = 10 / 4 = **2,5**. RMSE = $\sqrt{(9 + 1 + 4 + 16)/4} = \sqrt{7{,}5} \approx$ **2,74**. ME = 4 / 4 = **1**: dương, dự báo **thấp** hơn thực
tế trung bình 1 đơn vị (mục 4.3). Nhầm hay gặp: đọc ME dương là dự báo cao, quên quy ước sai số = thực tế − dự báo.

</details>

**Câu 7.** Phần học $(20, 22, 21, 23, 24)$, $m$ = 1. Kỳ chấm thực tế $(25, 27)$. Mô hình dự báo $(26, 26)$; naive dự báo $(24, 24)$. Tính MASE
của cả hai. Mô hình có thắng naive trên kỳ chấm không?

<details>
<summary>Đáp án</summary>

Mẫu số: bước nhảy 2, 1, 2, 1 → trung bình 1,5. Mô hình: MAE (1 + 1) / 2 = 1, MASE = 1 / 1,5 ≈ **0,67**. Naive: MAE (1 + 3) / 2 = 2, MASE = 2 /
1,5 ≈ **1,33**. Cùng kỳ chấm, 0,67 < 1,33: mô hình thắng (mục 4.5). Nhầm hay gặp: lấy mẫu số từ kỳ chấm (bước nhảy 27 − 25).

</details>

**Câu 8.** Doanh số một tuần của một mặt hàng thường là $(2, 3, 4, 5, 26)$ (ngày cuối có đơn sỉ). Bạn phải chọn một con số dự báo cho mỗi ngày;
thiếu hay thừa một đơn vị đều mất như nhau. Chọn con số nào, chấm bằng chỉ số nào?

<details>
<summary>Đáp án</summary>

Mất mát tăng đều theo độ lệch → chấm bằng **MAE**, dự báo **trung vị = 4** (mục 4.3). Trung bình 40 / 5 = 8 là con số RMSE ưa: nó bị đơn sỉ 26
kéo lên, và sai nhiều ở bốn ngày thường. Nhầm hay gặp: dự báo trung bình vì "trung bình là con số đại diện".

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo trên 300 mã hàng bán lẻ (75% số ngày bằng 0):

| Mô hình | MAPE trung vị |
|---|---|
| mô hình mới | 38,2% |
| seasonal naive | 52,7% |

"Mô hình mới tốt hơn 28%." Chỉ ra lỗi và nói phải báo gì.

<details>
<summary>Đáp án</summary>

Với 75% ngày bằng 0, gần như chuỗi nào cũng có MAPE vô hạn; con số 38,2% chỉ đến từ việc âm thầm bỏ các giá trị vô hạn, tức chỉ tính trên
vài chuỗi không có số 0 (mục 4.4, 4.6). Phải báo số chuỗi không tính được, và dùng chỉ số chịu được số 0: WAPE, MASE, RMSSE, kèm cả bốn
baseline. Nhầm hay gặp: tin một con số phần trăm vì nó "trông hợp lý".

</details>

**Câu 10.** Trên 1.000 chuỗi M4 theo ngày, bảng MASE trung vị:

| Mô hình | MASE |
|---|---|
| mô hình mới | 0,95 |
| naive | 0,835 |
| seasonal naive | 1,077 |
| drift | 0,810 |

Báo cáo viết: "MASE < 1 nên mô hình mới thắng baseline." Nhận xét.

<details>
<summary>Đáp án</summary>

Hai lỗi (mục 4.1, 4.5). (1) MASE < 1 chỉ nói sai ít hơn mức seasonal naive **trên phần học**, không phải "thắng baseline"; muốn biết thắng
thì so trên cùng kỳ chấm. (2) So trên cùng kỳ chấm thì mô hình mới thắng seasonal naive (0,95 < 1,077) nhưng **thua** naive (0,835) và drift
(0,810). Phải vượt mọi baseline mới gọi là thắng.

</details>
