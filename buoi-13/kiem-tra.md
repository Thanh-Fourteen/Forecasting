# Kiểm tra buổi 13 — Feature engineering và chống rò rỉ

## Nhắc lại khái niệm

**Câu 1.** Dự báo doanh thu ngày mai. Feature nào **không** xếp được vào nhóm "biết trước" nào?

- A. Ngày mai có phải ngày lễ
- B. Khuyến mãi đã lên lịch cho ngày mai
- C. Doanh thu trung bình của cả năm nay
- D. Doanh thu hôm qua

<details>
<summary>Đáp án</summary>

**C** (mục 4.1): năm chưa hết, nên trung bình cả năm chứa những ngày chưa xảy ra. **A sai**: lịch, biết trước mãi mãi. **B sai**: kế hoạch đã
công bố. **D sai**: quá khứ của chuỗi.

</details>

**Câu 2.** Dự báo trước 1 ngày. Feature "trung bình 7 ngày" viết đúng là:

- A. `y.rolling(7).mean()`
- B. `y.rolling(7, center=True).mean()`
- C. `y.shift(1).rolling(7).mean()`
- D. `y.rolling(7).mean().shift(-1)`

<details>
<summary>Đáp án</summary>

**C** (mục 4.2): cửa sổ kết thúc ở ngày $t - 1$. **A sai**: cửa sổ chứa chính $y_t$. **B sai**: chứa cả 3 ngày sau $t$. **D sai**: `shift(-1)`
kéo số của ngày sau về, còn tệ hơn A.

</details>

**Câu 3.** Vì sao không dùng thư viện lịch âm Trung Quốc để tạo feature Tết cho dữ liệu Việt Nam?

- A. Lịch Trung Quốc không có Tết
- B. Ngày sóc tính theo giờ địa phương; ở UTC+8 có năm Tết lệch một ngày so với UTC+7
- C. Thư viện Trung Quốc chạy chậm
- D. Việt Nam không dùng lịch âm

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): trong 2000–2035 có hai năm lệch là 2007 và 2030; ví dụ Tết 2007 ở Việt Nam là 17/2, ở Trung Quốc là 18/2. **A, D sai**: cả hai
nước đón Tết âm lịch. **C sai**: tốc độ không liên quan; sai là sai ngày.

</details>

**Câu 4.** Bài kiểm cắt tương lai **không** bắt được lỗi nào?

- A. `rolling` có tâm
- B. Chuẩn hoá bằng trung bình cả chuỗi
- C. `lag_1` trong bài dự báo trước 24 giờ
- D. Target encoding tính trên cả chuỗi

<details>
<summary>Đáp án</summary>

**C** (mục 4.5): `lag_1` không phụ thuộc chuyện dữ liệu bị cắt ở đâu; phải dùng kiểm nhiễu mục tiêu với $h$ = 24. **A, B, D sai**: cả ba dùng số
của phần sau mốc cắt, nên cắt đi thì giá trị trước mốc đổi và bài kiểm bắt được.

</details>

## Vận dụng

**Câu 5.** Chuỗi $(5, 7, 9, 4, 6)$, dự báo trước 1 ngày. Tính feature trung bình 2 ngày tại ngày thứ năm theo `y.rolling(2)` và
`y.shift(1).rolling(2)`. Cái nào nhìn trộm?

<details>
<summary>Đáp án</summary>

`y.rolling(2)`: $(4 + 6)/2 = 5$, dùng chính số 6 của ngày thứ năm: **nhìn trộm**. `y.shift(1).rolling(2)`: $(9 + 4)/2 = 6{,}5$, chỉ dùng ngày
ba và bốn: hợp lệ (mục 4.2). Nhầm hay gặp: nghĩ "cửa sổ nằm hết ở quá khứ" vì không có `center=True`.

</details>

**Câu 6.** Bốn ngày học có doanh thu $(10, 12, 8, 14)$, hai ngày kiểm là $(20, 16)$. Chuẩn hoá đúng cách (tham số chỉ học từ phần học; độ
lệch chuẩn chia $n - 1$): tính z của số 20.

<details>
<summary>Đáp án</summary>

Trung bình phần học 11, độ lệch chuẩn ≈ 2,58; z = (20 − 11)/2,58 ≈ **3,49** (mục 4.4a). Chuẩn hoá trên cả sáu ngày cho z ≈ 1,54: số 20 trông
bình thường vì chính nó đã kéo trung bình và độ lệch chuẩn lên. Nhầm hay gặp: `fit` scaler trên cả tập rồi mới chia.

</details>

**Câu 7.** Bạn ghép nhiệt độ theo giờ vào tải điện bằng `merge_asof(..., direction="nearest")`, không đặt `tolerance`. Chỉ ra hai vấn đề.

<details>
<summary>Đáp án</summary>

(1) `nearest` lấy cả bản ghi có mốc **sau** giờ cần ghép: rò rỉ; phải `direction="backward"`. (2) Không `tolerance` thì khi nguồn nhiệt độ thiếu
một tuần, hàm vẫn kéo số cũ xuống mà không báo (mục 4.6). Nhầm hay gặp: thấy cột vừa ghép không có NaN nào là yên tâm.

</details>

**Câu 8.** Thêm 5 feature Tết âm lịch làm MAE cả năm chỉ giảm 1,9%. Đồng nghiệp đề nghị bỏ vì "không đáng kể". Bạn trả lời sao?

<details>
<summary>Đáp án</summary>

Xem sai số ở **vùng feature có tác dụng**: quanh Tết (±10 ngày) MAE giảm 16,9% (mục 4.3). Tết chỉ chiếm vài phần trăm số ngày trong năm nên trung
bình cả năm pha loãng hiệu quả. Giữ feature và báo cả hai con số.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Bảng MAE dự báo tải điện 24 giờ tới (chỉ lag + giờ: 1.909,68 MW):

| Bộ feature | MAE (MW) |
|---|---|
| + nhiệt độ thật của giờ cần dự báo | 1.836,16 |
| + dự báo nhiệt độ trước 1 ngày | 1.834,29 |
| + dự báo nhiệt độ trước 3 ngày | 1.965,47 |

Báo cáo viết: "Thêm nhiệt độ giảm sai số 3,85%, đề nghị triển khai với nguồn dự báo thời tiết trước 3 ngày." Chỉ ra lỗi.

<details>
<summary>Đáp án</summary>

Con số −3,85% lấy từ dòng nhiệt độ **thật**, thứ không có lúc chạy (mục 4.6). Với dự báo trước 3 ngày, MAE là 1.965,47, tức **tăng** 2,92%:
feature làm hại. Chỉ nên dùng nhiệt độ nếu có dự báo trước 1 ngày (−3,95%); nếu không thì dùng nhiệt độ hiện tại hoặc bỏ.

</details>

**Câu 10.** Một pull request thêm năm feature, dự báo trước 1 ngày:

```python
f["tb_7"] = y.rolling(7, center=True).mean()
f["z"] = (y - y.mean()) / y.std()
f["tb_thu"] = y.groupby(y.index.dayofweek).transform("mean")
f["y_dien"] = y.interpolate(limit_direction="both")
f["truoc_tet"] = (pd.Timestamp("2011-02-03") - y.index).days
```

Người viết nói: "`kiem_ro_ri` báo sạch cột `y_dien` và `truoc_tet`, vậy hai cột này ổn." Đúng không? Chỉ ra lỗi của từng dòng.

<details>
<summary>Đáp án</summary>

Không đúng. `tb_7` có tâm, chứa 3 ngày sau (mục 4.2). `z` và `tb_thu` dùng trung bình cả chuỗi (mục 4.4a, b). `y_dien` điền bằng số của ngày sau
lỗ; bài kiểm chỉ bắt được khi mốc cắt rơi đúng vào một lỗ, và chuỗi đã hết lỗ thì không bao giờ bắt (mục 4.4c, 4.5). `truoc_tet` không rò rỉ
nhưng sai: ghi cứng Tết 2011, đúng một năm (mục 4.3). Bài kiểm xanh chỉ nói không thấy rò rỉ ở những mốc đã cắt; lỗi lịch cần test riêng.

</details>
