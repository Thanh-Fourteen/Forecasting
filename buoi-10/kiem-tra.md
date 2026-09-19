# Kiểm tra buổi 10 — Làm sạch và dữ liệu thiếu

## Nhắc lại khái niệm

**Câu 1.** Một tệp đo theo giờ, `df.isna().sum()` báo 0 ô thiếu ở mọi cột. Kết luận đúng là:

- A. Dữ liệu đủ, không cần làm gì thêm
- B. Chưa biết: phải dựng lưới đầy đủ các mốc giờ rồi `reindex`, vì `isna()` không thấy dòng không tồn tại
- C. Dữ liệu chắc chắn có mã trá hình
- D. Dữ liệu là MCAR

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): `isna()` chỉ đếm ô rỗng trong những dòng có mặt; mốc không có dòng thì nó không thấy. Trạm Nội Bài: `isna()` thấy 2 ô,
thiếu thật 251. **A sai**: đó chính là cái bẫy. **C sai**: không có ô rỗng không nói gì về mã trá hình; phải xem histogram. **D sai**: cơ chế
thiếu phải kiểm bằng số, không suy ra từ `isna()`.

</details>

**Câu 2.** Cảm biến bụi quá tải và tắt mỗi khi PM2.5 vượt 500 µg/m³. Số bị mất thuộc cơ chế nào?

- A. MCAR
- B. MAR
- C. MNAR
- D. Không phải dữ liệu thiếu

<details>
<summary>Đáp án</summary>

**C** (mục 4.2): việc mất phụ thuộc **chính giá trị** bị mất (cao thì mất). Điền kiểu gì từ phần còn lại cũng lệch xuống. **A sai**: mất không
ngẫu nhiên. **B sai**: MAR là mất phụ thuộc một thứ **khác** đã đo được. **D sai**: giờ đó có thật, chỉ không có số.

</details>

**Câu 3.** Trong GHCNh, một số đo nhiệt độ có cờ chất lượng `4`. Nghĩa là:

- A. Số đo sai, phải loại
- B. Số đo đáng ngờ
- C. Số đo mới qua bước kiểm giới hạn thô, không phải lỗi
- D. Số đo ngoài phạm vi

<details>
<summary>Đáp án</summary>

**C** (mục 4.3, bảng cờ). Nhóm cần loại là `2, 3, 6, 7, o, f`. **A, B sai**: đó là mã `3` và `2`; coi `4` là lỗi làm loại oan nhiều dòng. **D
sai**: đó là cờ `o`.

</details>

**Câu 4.** Cách điền nào **nhân quả** (chỉ dùng dữ liệu trước ô đang điền)?

- A. Nội suy tuyến tính hai phía
- B. Spline
- C. `ffill`
- D. Kalman smoother

<details>
<summary>Đáp án</summary>

**C** (mục 4.4): `ffill` chỉ giữ số gần nhất **trước** ô thiếu. **A, B sai**: nối hai đầu lỗ, tức nhìn cả số phía sau. **D sai**: smoother
ước lượng từ cả hai phía; dùng `fittedvalues` (dự báo một bước) mới là chỉ dùng quá khứ.

</details>

## Vận dụng

**Câu 5.** Tệp đo theo giờ từ 06:00 tới 12:00 có các dòng 06:00, 07:00, 09:00, 10:00, 12:00; ô nhiệt độ lúc 10:00 là NaN. `isna()` báo mấy ô
thiếu? Thiếu thật bao nhiêu giờ, là những giờ nào?

<details>
<summary>Đáp án</summary>

`isna()` báo **1** (10:00). Từ 06:00 tới 12:00 có 7 mốc; tệp có 5 dòng nên thiếu mốc 08:00 và 11:00. Thiếu thật **3** giờ: 08:00, 10:00,
11:00 (mục 4.1). Nhầm hay gặp: đếm 6 mốc (quên tính cả hai đầu).

</details>

**Câu 6.** Nhiệt độ theo giờ: 20, ?, ?, 26; giá trị thật của hai ô thiếu là 22 và 25. Điền bằng `ffill` và bằng nội suy tuyến tính, tính MAE
của mỗi cách. Cách nào dùng được khi dự báo thật?

<details>
<summary>Đáp án</summary>

`ffill`: 20, 20 → sai 2 và 5, MAE **3,5**. Tuyến tính nối 20 với 26: 22, 24 → sai 0 và 1, MAE **0,5** (mục 4.4). Tuyến tính tốt hơn nhưng nhìn
cả số 26 phía sau, nên chỉ dùng được khi làm sạch dữ liệu quá khứ đã chia tập xong; lúc dự báo thật chỉ `ffill` (nhân quả) dùng được. Nhầm
hay gặp: chọn cách có MAE thấp nhất mà quên hỏi nó có dùng tương lai không.

</details>

**Câu 7.** Cảm biến nhiệt độ ghi tới 1 °C. Có 24 đoạn giá trị lặp dài từ 12 giờ trở lên, phần lớn vào ban đêm. Bạn loại cả 24 đoạn như "cảm
biến chết" không? Làm gì trước?

<details>
<summary>Đáp án</summary>

**Không** (mục 4.3). Với độ phân giải 1 °C, đêm nhiệt độ thật chỉ đổi vài phần mười độ vẫn ghi thành cùng một số. Trước hết đo độ phân giải
(`do_phan_giai`), rồi đặt ngưỡng dài hơn theo đó (buổi này 18 giờ, còn 2 đoạn); đoạn lặp cả ngày lẫn đêm mới đáng ngờ. Nhầm hay gặp: dùng một
ngưỡng "đứng yên" cho mọi cảm biến.

</details>

**Câu 8.** Một cửa hàng hết hàng ba ngày, doanh số ghi 0. Bạn xử lý ba ngày đó thế nào khi làm dữ liệu cho dự báo, và vì sao?

<details>
<summary>Đáp án</summary>

Đánh dấu là **thiếu** (NaN + cờ), không để 0 (mục 4.1). Nhu cầu thật những ngày đó cao hơn 0; mô hình học từ số 0 sẽ dự báo thấp, cửa hàng
nhập ít, lại hết hàng: vòng lặp tự củng cố. Nhầm hay gặp: coi 0 là số đo thật vì "máy ghi đúng là không bán được".

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một nhóm che ngẫu nhiên 10% số điểm của chuỗi nhiệt độ và được:

| Cách điền | MAE (°C) |
|---|---|
| tuyến tính | 0,291 |
| Kalman smoother | 0,308 |
| `ffill` | 0,378 |
| hàng xóm | 0,922 |

Họ kết luận: "Dùng nội suy tuyến tính cho mọi lỗ, kể cả lỗ cảm biến chết hai ngày." Chỉ ra lỗi.

<details>
<summary>Đáp án</summary>

Che ngẫu nhiên từng điểm chỉ thi **lỗ ngắn**; kết quả không chuyển sang lỗ dài (mục 4.5). Che khối 48 giờ trên cùng chuỗi, tuyến tính tụt
xuống hạng 5 (MAE 2,171), hàng xóm lên hạng 1 (1,006). Thêm hai lỗi: tuyến tính dùng tương lai (rò rỉ nếu điền trước khi chia tập), và lỗ hai
ngày thì nên để trống có cờ, không điền (mục 4.6).

</details>

**Câu 10.** Báo cáo chất lượng tự sinh của một trạm:

| Cột | min | max | trá hình % |
|---|---|---|---|
| relative_humidity | 100 | 94 | 0,0 |
| visibility | 0,1 | 9,999 | 0,0 |

Dòng cuối báo cáo: "Sau làm sạch: còn thiếu 0 ô." Chỉ ra ba chỗ đáng ngờ và nguyên nhân có thể của từng chỗ.

<details>
<summary>Đáp án</summary>

(1) `min` 100 lớn hơn `max` 94: cột độ ẩm lưu dạng **chữ**, so theo thứ tự chữ cái; phải `pd.to_numeric` (mục 4.3). (2) Tầm nhìn max đúng
9,999 mà "trá hình 0%": vẫn do kiểu chữ, so sánh với số 9,999 không khớp; sau khi ép kiểu, 9,999 chiếm hơn một phần ba số dòng, là mã "từ
10 km trở lên". (3) "Còn thiếu 0" trong khi có lỗ dài nhiều giờ: pipeline điền **mọi** lỗ bằng nội suy, bịa dữ liệu và dùng tương lai; đúng
ra lỗ dài phải để trống với cột cờ (mục 4.6).

</details>
