# Kiểm tra buổi 22 — Biến dự báo thành bài toán hồi quy

## Nhắc lại khái niệm

**Câu 1.** Dãy $(3, 5, 4, 6, 8, 7)$, dựng bảng với $L$ = 3 lag (mới nhất đứng đầu). Bảng có bao nhiêu dòng, và dòng cuối là gì?

- A. 6 dòng; dòng cuối: (7, 8, 6) → không có nhãn
- B. 3 dòng; dòng cuối: (8, 6, 4) → 7
- C. 3 dòng; dòng cuối: (4, 6, 8) → 7
- D. 4 dòng; dòng cuối: (6, 8, 7) → 7

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): dãy dài 6, khung 3 cho 6 − 3 = 3 dòng; dòng cuối lấy ba số trước số 7, mới nhất đứng đầu: 8, 6, 4. **A sai**: ba số đầu không
đủ khung nên không thành dòng, và dòng không có nhãn thì không học được. **C sai**: đúng số dòng nhưng đảo thứ tự, lag 1 phải là số ngay trước
nhãn (8). **D sai**: sai số dòng, và dòng cuối chứa chính nhãn 7 trong đầu vào.

</details>

**Câu 2.** Vì sao mô hình global học chung 10.000 trang cần chuẩn hoá từng trang (log, trừ mức) trước khi học?

- A. Để mô hình chạy nhanh hơn
- B. Vì LightGBM không nhận số lớn hơn một triệu
- C. Để trang lớn và trang nhỏ cùng thang; nếu không, mô hình chỉ lo đoán đúng trang khổng lồ
- D. Để mọi trang có cùng mùa vụ

<details>
<summary>Đáp án</summary>

**C** (mục 4.2): trang Chính 14 triệu lượt/ngày, trang T1 26 lượt; trên số gốc, sai 1% ở trang lớn nặng hơn sai 100% ở trang nhỏ. Sau log và
trừ mức, hai trang cùng dao động quanh 0. **A sai**: tốc độ gần như không đổi. **B sai**: LightGBM nhận số bất kỳ; vấn đề là thang, không
phải giới hạn. **D sai**: chuẩn hoá không đổi hình dạng mùa vụ, chỉ đổi thang và mức.

</details>

**Câu 3.** Trong chiến lược recursive với $L$ = 28, khi đoán ngày thứ 10 sau cutoff, đầu vào có bao nhiêu dự báo?

- A. 0
- B. 9
- C. 10
- D. 28

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): ngày 1 … 9 đã được đoán và nối vào lịch sử, nên 9 trong 28 đầu vào là dự báo; 19 còn lại là số thật. **A sai**: đó là direct.
**C sai**: ngày 10 là ngày đang đoán, chưa có trong đầu vào. **D sai**: 28 là độ dài khung, không phải số dự báo trong khung.

</details>

**Câu 4.** Vì sao cây quyết định (và LightGBM) không dự báo vượt được số lớn nhất nó đã thấy khi học?

- A. Vì mỗi lá trả trung bình các nhãn học rơi vào lá đó, và trung bình không vượt số lớn nhất
- B. Vì scikit-learn cắt dự báo ở giá trị lớn nhất
- C. Vì cây quá sâu
- D. Vì thiếu cột thứ trong tuần

<details>
<summary>Đáp án</summary>

**A** (mục 4.5): lá trả trung bình nhãn; trung bình của các số không lớn hơn số lớn nhất trong chúng; tổng nhiều cây cũng vậy. **B sai**:
không có bước cắt nào, giới hạn nằm ở cách lá tính dự báo. **C sai**: cây sâu hay nông đều trả trung bình. **D sai**: thêm cột lịch không
giúp vượt khoảng nhãn đã thấy.

</details>

## Vận dụng

**Câu 5.** Cutoff là 10/8, tầm $h$ = 4. Theo quy tắc của chiến lược direct, `lag_1` và `lag_5` của dòng cần đoán là số của ngày nào?

- A. `lag_1` = 13/8, `lag_5` = 9/8
- B. `lag_1` = 10/8, `lag_5` = 6/8
- C. `lag_1` = 14/8, `lag_5` = 10/8
- D. `lag_1` = 9/8, `lag_5` = 5/8

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): ngày cần đoán là 10/8 + 4 = 14/8. `lag_k` = ngày $14 - (4 - 1) - k$: `lag_1` = 14 − 3 − 1 = 10/8 (đúng cutoff), `lag_5` = 14 − 3 − 5
= 6/8. **A sai**: đó là `shift(1)` tính từ ngày cần đoán, đọc 13/8 chưa xảy ra. **C sai**: `lag_1` là chính ngày cần đoán. **D sai**: lệch một
ngày, bỏ mất số của ngày cutoff dù đã biết.

</details>

**Câu 6.** Hai trang, $\log_{10}$ lượt xem ba ngày gần nhất: trang A $(4, 5, 6)$, trang B $(1, 2, 3)$. Mô hình global dự báo "cao hơn
mức 1" cho cả hai. Dự báo lượt xem của trang B là bao nhiêu?

- A. 10
- B. 100
- C. 1.000
- D. 1.000.000

<details>
<summary>Đáp án</summary>

**C** (mục 4.2): mức B = (1 + 2 + 3) / 3 = 2; cộng 1 được 3; $10^3$ = **1.000** lượt. **A sai**: quên cộng lại mức, lấy $10^1$. **B sai**:
lấy mức mà quên cộng dự báo "+1". **D sai**: dùng mức của trang A (5) cho trang B; mô hình global dùng chung cách đoán nhưng mỗi trang giữ mức riêng.

</details>

**Câu 7.** Bạn có 5 chuỗi doanh số tăng đều 3% mỗi tháng, muốn dùng LightGBM global. Việc nào cần làm trước tiên?

- A. Tăng số cây lên 5.000
- B. Học trên sai phân (hoặc trên độ lệch so với mức gần đây) rồi cộng lại
- C. Bỏ cột lag, chỉ giữ cột tháng
- D. Chia train/test ngẫu nhiên để mô hình thấy cả tháng cuối

<details>
<summary>Đáp án</summary>

**B** (mục 4.5): cây không vượt được mức đã thấy; chuỗi tăng đều thì tháng tới luôn cao hơn mọi tháng đã học. Học trên bước nhảy (hay độ lệch
so với mức) thì mức đi theo chuỗi. **A sai**: nhiều cây hơn vẫn trả trung bình nhãn đã thấy. **C sai**: bỏ lag làm mất thông tin, xu hướng
vẫn không ngoại suy được. **D sai**: chia ngẫu nhiên là rò rỉ tương lai, điểm đẹp giả.

</details>

**Câu 8.** $H$ = 14 ngày. Bạn muốn dùng rừng ngẫu nhiên và chỉ học **một** mô hình, nhưng không muốn sai số tích luỹ. Chọn chiến lược nào?

- A. recursive
- B. direct
- C. MIMO
- D. Không có cách nào

<details>
<summary>Đáp án</summary>

**C** (mục 4.3): MIMO là một mô hình ra cả vector 14 ngày, đầu vào toàn số thật; rừng ngẫu nhiên hỗ trợ nhiều đầu ra. **A sai**: một mô hình
nhưng dùng lại dự báo, nên tích luỹ sai số. **B sai**: không tích luỹ nhưng cần 14 mô hình. **D sai**: MIMO làm được đúng yêu cầu.

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Một đồng nghiệp báo kết quả backtest chiến lược direct (RMSE trên thang $z$, 300 trang):

| $h$ | 1 | 4 | 7 | 10 | 14 |
|---|---|---|---|---|---|
| recursive | 0,455 | 0,466 | 0,480 | 0,581 | 0,575 |
| direct | 0,455 | 0,423 | 0,447 | 0,547 | 0,490 |

Đồng nghiệp kết luận: "direct thắng recursive 15% ở ngày 14, dùng direct". Điều gì đáng ngờ nhất?

- A. Direct và recursive trùng ở $h$ = 1, chứng tỏ code sai
- B. Direct tốt lên ở tầm xa (ngày 4 tốt hơn ngày 1); đoán xa không thể dễ hơn, nhiều khả năng lag nhỏ hơn $h$ — rò rỉ
- C. Recursive quá kém, cần tăng số cây
- D. 300 trang là quá ít

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): ở ngày 4 direct được 0,423, tốt hơn cả ngày 1 (0,455). Mô hình tầm 4 chỉ đọc số tới cutoff thì không thể dễ hơn mô hình tầm 1;
nó đang đọc số của những ngày sau cutoff. Chạy `kiem_ro_ri(..., h=4)` để xác nhận. **A sai**: ở $h$ = 1 hai mô hình học cùng một bảng nên
trùng là đúng. **C sai**: recursive ngang MIMO và direct đúng (mục 4.3). **D sai**: số trang không giải thích được direct tốt lên theo $h$.

</details>

**Câu 10.** Bảng RMSSE trung bình trên 10.000 trang:

| Mô hình | RMSSE trung bình | % trang thắng seasonal naive |
|---|---|---|
| LightGBM global | 0,916 | 87,6% |
| AutoETS local | 0,951 | 81,3% |
| seasonal naive | 1,099 | — |

Câu nào đọc bảng **sai**?

- A. LightGBM global sai ít hơn AutoETS local khoảng 4% tính trung bình
- B. Cả hai thắng seasonal naive trên phần lớn số trang
- C. Với trang bất kỳ, LightGBM global chắc chắn tốt hơn AutoETS
- D. Seasonal naive có RMSSE trên 1: trung bình nó sai nhiều hơn mức nhảy ngày-qua-ngày của chính chuỗi

<details>
<summary>Đáp án</summary>

**C** là câu sai (mục 4.6): bảng chỉ cho trung bình; tính từng trang, LightGBM thắng AutoETS ở 58% số trang, và ở nhóm trang ít lượt xem nhất
chỉ 52%. **A đúng**: (0,951 − 0,916) / 0,951 ≈ 3,7%. **B đúng**: 87,6% và 81,3%. **D đúng**: đó là nghĩa của RMSSE > 1 (mục 2).

</details>
