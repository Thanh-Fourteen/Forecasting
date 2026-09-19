# Kiểm tra buổi 15 — Backtesting đúng cách

## Nhắc lại khái niệm

**Câu 1.** Vì sao chia ngẫu nhiên (K-fold xáo trộn) thường hứa sai số thấp hơn thật khi dự báo chuỗi thời gian?

- A. Vì tập kiểm quá nhỏ
- B. Vì điểm kiểm nằm xen giữa điểm học: mô hình được thấy cả giờ trước lẫn giờ sau của điểm nó phải đoán
- C. Vì K-fold dùng MAE thay cho RMSE
- D. Vì K-fold không học lại mô hình

<details>
<summary>Đáp án</summary>

**B** (mục 4.1). **A sai**: K-fold kiểm lần lượt mọi điểm, tập kiểm không nhỏ. **C sai**: chỉ số nào cũng lạc quan như nhau khi tương lai lọt vào
tập học. **D sai**: K-fold học lại ở mỗi phần; vấn đề nằm ở dữ liệu học, không ở số lần học.

</details>

**Câu 2.** Trong rolling origin, ở mỗi cửa sổ mô hình:

- A. Học trên mọi dữ liệu, kể cả đoạn kiểm của cửa sổ đó
- B. Học trên dữ liệu tới cutoff, dự báo đoạn ngay sau cutoff (sau gap nếu có)
- C. Học trên đoạn sau cutoff, dự báo ngược về quá khứ
- D. Không học, chỉ dự báo

<details>
<summary>Đáp án</summary>

**B** (mục 4.2). **A sai**: đó là rò rỉ. **C sai**: dự báo luôn đi tới tương lai. **D sai**: mặc định mỗi cửa sổ học lại (refit), giống cách chạy
thật.

</details>

**Câu 3.** Tham số `gap` của backtest dùng khi:

- A. Chuỗi có lỗ thiếu
- B. Số liệu về trễ: lúc ra dự báo, vài bước gần nhất chưa có
- C. Muốn các đoạn kiểm chồng lên nhau
- D. Muốn học trên ít dữ liệu hơn

<details>
<summary>Đáp án</summary>

**B** (mục 4.2). **A sai**: lỗ thiếu xử lý ở bước làm sạch (buổi 10). **C sai**: chồng hay không do `buoc` quyết định. **D sai**: học trên ít dữ liệu
là sliding window (`cua_so_train`).

</details>

**Câu 4.** Đoạn dữ liệu dùng để **báo cáo** sai số cuối cùng:

- A. Là đoạn đã dùng để chọn mô hình tốt nhất
- B. Là đoạn đã dùng để tune tham số
- C. Chỉ được dùng một lần, sau khi mọi quyết định đã xong
- D. Có thể dùng lại để chỉnh mô hình nếu kết quả chưa tốt

<details>
<summary>Đáp án</summary>

**C** (mục 4.4). **A, B sai**: báo cáo trên đoạn đã dùng để chọn hay tune thì lạc quan (M4 theo giờ: 0,775 so với 1,039). **D sai**: chỉnh xong
thì đoạn đó thành tập chọn, cần một đoạn báo cáo mới.

</details>

## Vận dụng

**Câu 5.** Dữ liệu 50 mốc (0 → 49), $h$ = 5, 4 cửa sổ, `buoc` = 5, gap = 0. Tính các cutoff. Cửa sổ đầu học trên đoạn nào, dự báo đoạn nào?

<details>
<summary>Đáp án</summary>

Cutoff cuối = 50 − 1 − 0 − 5 = **44**; lùi 5 mỗi lần: **39, 34, 29**. Cửa sổ đầu học trên **0 → 29**, dự báo **30 → 34** (mục 4.2). Nhầm hay gặp:
đặt cửa sổ đầu ở đầu dữ liệu rồi đếm tới; quy ước là cửa sổ cuối sát đuôi dữ liệu.

</details>

**Câu 6.** Backtest 4 cửa sổ cho MAE $(4, 4, 5, 15)$. Tính trung bình và trung vị. Nếu chỉ chạy một hold-out, bạn có thể báo những con số nào?
Nên báo gì?

<details>
<summary>Đáp án</summary>

Trung bình 28 / 4 = **7**; trung vị (4 + 5) / 2 = **4,5**. Một hold-out có thể rơi vào bất kỳ cửa sổ nào: báo 4 hay 15, gần bốn lần nhau. Nên báo
trung bình hoặc trung vị kèm khoảng từ 4 tới 15, và xem cửa sổ 15 có gì đặc biệt (mục 4.3). Nhầm hay gặp: coi một cửa sổ là "sai số của mô hình".

</details>

**Câu 7.** Chênh mất mát của hai dự báo ($h$ = 1) trên 4 ngày là $d = (2, -1, 3, 0)$. Tính $\bar d$, sai số chuẩn của $\bar d$ (phương sai chia
$n$), $S_1$, và $S_1^*$.

<details>
<summary>Đáp án</summary>

$\bar d$ = 4 / 4 = **1**. Độ lệch $(1, -2, 2, -1)$, phương sai 10 / 4 = 2,5; sai số chuẩn $\sqrt{2{,}5 / 4} \approx$ **0,79**. $S_1$ = 1 / 0,79 ≈
**1,26**. Hệ số $\sqrt{(4 + 1 - 2)/4} = \sqrt{0{,}75} \approx 0{,}866$ → $S_1^*$ ≈ **1,10**; so với t 3 bậc tự do p ≈ 0,35: chưa có bằng chứng
(mục 4.5). $\bar d$ dương nghĩa là dự báo thứ nhất có mất mát **lớn hơn**. Nhầm hay gặp: chia phương sai cho $n$ hai lần, hoặc quên căn.

</details>

**Câu 8.** Ba cấu hình có MAE trên đoạn A (dùng để chọn) và đoạn B (sau A, chưa dùng):

| Cấu hình | A | B |
|---|---|---|
| X | 10 | 14 |
| Y | 11 | 11 |
| Z | 12 | 12 |

Theo quy trình ba tập, chọn cấu hình nào và báo con số nào? Vì sao không báo 10?

<details>
<summary>Đáp án</summary>

Chọn trên A: **X**. Báo sai số của X trên B: **14** (mục 4.4). 10 là con số đã dùng để chọn, có phần may: X thắng ở A nhưng tệ nhất ở B. Nếu
B lộ ra X tệ, **không** được quay lại đổi sang Y rồi báo 11 trên B: B đã thành tập chọn, cần một đoạn mới. Nhầm hay gặp: chọn lại theo B
rồi báo luôn B.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Báo cáo đánh giá mô hình dự báo tải ngày mai:

```python
hoc, kiem = train_test_split(bang_feature, test_size=0.2, random_state=0)
mo_hinh = RandomForestRegressor().fit(hoc[X], hoc["y"])
print(mae(mo_hinh.predict(kiem[X]), kiem["y"]))   # 1.617 MW
```

"Sai số dự kiến khi triển khai: 1.617 MW." Chỉ ra lỗi, sai số thật cỡ nào, và phải làm gì.

<details>
<summary>Đáp án</summary>

`train_test_split` mặc định **xáo trộn**: điểm kiểm nằm giữa điểm học, rừng ngẫu nhiên nhớ hàng xóm tương lai (mục 4.1). Trên hold-out thật,
cùng mô hình sai 2.129 MW: con số 1.617 thấp hơn thật 24%. Phải dùng rolling origin trên phần học (mục 4.2: 1.944 MW, lệch hold-out −8,7%), và báo độ dao
động giữa các cửa sổ. Nhầm hay gặp: nghĩ `random_state=0` là đủ "cố định"; nó chỉ cố định cách xáo, vẫn là xáo.

</details>

**Câu 10.** Báo cáo so mô hình "trộn" với seasonal naive trên 3 tháng cuối (dự báo ngày tới, theo giờ):

| Mô hình | MAE hold-out | DM, p |
|---|---|---|
| seasonal naive | 1.944 MW | — |
| trộn ($w$ = 0,8, chọn $w$ cho MAE hold-out nhỏ nhất) | 1.861 MW | 0,0000012 ($h$ = 1) |

"Trộn tốt hơn 4,3%, có ý nghĩa thống kê rất mạnh." Chỉ ra hai lỗi.

<details>
<summary>Đáp án</summary>

(1) $w$ được **tune trên chính hold-out** (mục 4.4): tune đúng cách trên 3 tháng trước mốc thì $w$ = 1, tức chính là seasonal naive, không hơn
gì. (2) DM với $h$ = 1 trên sai số dự báo ngày tới theo giờ **bỏ tự tương quan** (mục 4.5): chênh lệch giờ liền nhau có ACF 0,91. Bản
Harvey–Leybourne–Newbold với $h$ = 24 cho p = 0,16: chưa có bằng chứng. Nhầm hay gặp: sửa lỗi thứ hai mà quên lỗi thứ nhất; ngay cả p đúng
cũng vô nghĩa khi mô hình được chọn bằng chính dữ liệu đang kiểm.

</details>
