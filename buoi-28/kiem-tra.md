# Kiểm tra buổi 28 — Dự báo phân cấp và reconciliation

## Nhắc lại khái niệm

**Câu 1.** Vì sao seasonal naive tự cho dự báo khớp giữa các cấp, còn AutoETS làm riêng từng chuỗi thì không?

- A. Vì seasonal naive dùng ít dữ liệu hơn
- B. Vì seasonal naive chỉ lặp lại số cũ: tổng các "cùng quý năm trước" của chuỗi đáy chính là "cùng quý năm trước" của chuỗi tổng; AutoETS chọn mô hình riêng cho từng chuỗi
- C. Vì AutoETS có lỗi
- D. Vì seasonal naive luôn chính xác hơn

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): số liệu thật đã khớp, nên lặp lại số liệu thật cũng khớp (lệch 3·10⁻¹¹). AutoETS chọn dạng mô hình và tham số riêng cho mỗi chuỗi, nên tổng
dự báo cấp đáy lệch dự báo cấp quốc gia tới 1.613 nghìn chuyến. **A sai**: lượng dữ liệu không quyết định chuyện khớp. **C sai**: không khớp là tính chất
của cách làm riêng rẽ, không phải lỗi. **D sai**: seasonal naive thua AutoETS ở ba trong bốn cấp.

</details>

**Câu 2.** Bottom-up và top-down khác nhau ở chỗ tin cấp nào?

- A. Bottom-up tin cấp đáy và cộng lên; top-down tin cấp đỉnh và chia xuống theo tỷ lệ
- B. Bottom-up tin cấp đỉnh; top-down tin cấp đáy
- C. Cả hai dùng mọi cấp như nhau
- D. Top-down không cho dự báo khớp

<details>
<summary>Đáp án</summary>

**A** (mục 4.2). **B sai**: ngược tên. **C sai**: đó là hoà giải tối ưu (OLS, MinT). **D sai**: chia xuống theo tỷ lệ cộng lại đúng bằng cấp đỉnh, nên khớp.

</details>

**Câu 3.** MinT khác OLS ở điểm nào?

- A. MinT chia phần lệch theo độ lớn và tương quan sai số của từng chuỗi; OLS chia đều
- B. MinT chỉ dùng cấp đáy
- C. MinT không cho dự báo khớp
- D. OLS dùng hiệp phương sai sai số, MinT thì không

<details>
<summary>Đáp án</summary>

**A** (mục 4.3): trong ví dụ với phương sai (4, 1, 1), chuỗi cả nước đoán kém nhất bị sửa nhiều nhất (−0,67), còn OLS dịch mọi chuỗi 1/3. **B sai**: đó là
bottom-up. **C sai**: mọi $\tilde y = SG\hat y$ đều khớp. **D sai**: ngược lại.

</details>

**Câu 4.** Vì sao không lấy cận trên khoảng 90% của cả nước bằng tổng cận trên của 8 bang?

- A. Vì các bang hiếm khi cùng lúc ở mức cao hiếm có, nên tổng các cận trên rộng quá mức
- B. Vì cộng số thập phân sai số làm tròn
- C. Vì cả nước không phải tổng các bang
- D. Vì khoảng 90% không cộng được với khoảng 80%

<details>
<summary>Đáp án</summary>

**A** (mục 4.4): ví dụ hai bang sai số ngược chiều: mỗi bang cận trên 2, tổng cận trên 4, nhưng sai số của tổng luôn 0. Phải hoà giải từng kịch bản rồi mới
lấy khoảng. **B sai**: không liên quan làm tròn. **C sai**: cả nước đúng là tổng các bang. **D sai**: không ai cộng hai mức khoảng khác nhau.

</details>

## Vận dụng

**Câu 5.** Dự báo base (cả nước, A, B) là (50, 20, 25). Tính lệch cộng, dự báo bottom-up của cả nước, và dự báo top-down (tỷ lệ dự báo) của A.

<details>
<summary>Đáp án</summary>

Lệch cộng 50 − (20 + 25) = **5**. Bottom-up: cả nước = **45**. Top-down: A = 50 × 20/45 ≈ **22,22** (B ≈ 27,78) (mục 4.1–4.2). Nhầm hay gặp: chia 50 đều
cho hai chuỗi (25 mỗi chuỗi), bỏ mất tỷ lệ.

</details>

**Câu 6.** Cùng dự báo base (50, 20, 25). Tính dự báo OLS của cả ba chuỗi.

<details>
<summary>Đáp án</summary>

Lệch 5 chia đều cho ba chuỗi, mỗi chuỗi dịch 5/3 ≈ 1,67 (mục 4.3): cả nước 50 − 1,67 ≈ **48,33**; A ≈ **21,67**; B ≈ **26,67**. Kiểm: 21,67 + 26,67 = 48,33.
Nhầm hay gặp: chỉ sửa cả nước (ra bottom-up 45) hoặc chỉ sửa hai chuỗi đáy.

</details>

**Câu 7.** Cây: cả nước = X + Y; bang X = A + B; bang Y = C. Chuỗi đáy là A, B, C. Ma trận $S$ có bao nhiêu dòng, bao nhiêu cột? Viết dòng của bang X.

<details>
<summary>Đáp án</summary>

Sáu chuỗi (cả nước, X, Y, A, B, C) nên **6 dòng**; ba chuỗi đáy nên **3 cột** (mục 4.1). Dòng của X là **(1, 1, 0)**: X cộng A và B, không cộng C. Nhầm hay
gặp: chỉ viết dòng cho các chuỗi tổng, quên ba dòng đơn vị của chính các chuỗi đáy.

</details>

**Câu 8.** Hai bang, ba kịch bản sai số. Trường hợp 1: A (−3, 0, 3), B (−3, 0, 3). Trường hợp 2: A (−3, 0, 3), B (3, 0, −3). Trong mỗi trường hợp, sai số lớn
nhất của tổng là bao nhiêu? So với tổng hai sai số lớn nhất (3 + 3).

<details>
<summary>Đáp án</summary>

Trường hợp 1: tổng là (−6, 0, 6), lớn nhất **6** = 3 + 3, vì hai bang luôn cùng chiều. Trường hợp 2: tổng là (0, 0, 0), lớn nhất **0**, nhỏ hơn 6 rất nhiều
(mục 4.4). Cộng cận chỉ đúng khi các chuỗi luôn đi cùng nhau; phải lấy khoảng từ tổng của từng kịch bản.

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Một đồng nghiệp báo RMSE theo cấp (nghìn chuyến/quý) và kết luận "MinT là phương pháp tốt nhất ở mọi cấp, đúng như lý thuyết":

| Cấp | base | MinT |
|---|---|---|
| quốc gia | 2.071 | 2.572 |
| bang | 339 | 369 |
| khu vực | 52,8 | 50,8 |
| khu vực × mục đích | 19,3 | 18,5 |

Tìm chỗ sai và nói nên kiểm thêm gì.

<details>
<summary>Đáp án</summary>

MinT chỉ thắng base ở hai cấp dưới; ở cấp quốc gia và bang nó tệ hơn (2.572 so với 2.071; 369 so với 339) (mục 4.3). Lý thuyết nói MinT tối ưu **khi dự
báo base không chệch**. Cần xem sai số có dấu theo cấp: ở đây mọi dự báo đều thấp hơn thực tế, và tổng các dự báo cấp đáy chệch nặng nhất (+2.847 ở cấp quốc
gia), nên MinT dồn phần chệch lên cấp trên.

</details>

**Câu 10.** Bảng coverage của khoảng 90% (giả định chuẩn, phần dư trong mẫu):

| Cấp | base | MinT |
|---|---|---|
| quốc gia | 58,3% | 4,2% |
| khu vực × mục đích | 82,8% | 82,7% |

Kết luận: "Khoảng MinT phủ 82,7% ở cấp chi tiết nhất, gần đạt, nên khoảng của cả cây coi như đã calibrate". Tìm hai chỗ sai.

<details>
<summary>Đáp án</summary>

1. **Calibration phải đạt ở từng cấp** (mục 4.4, cột mốc M4): cấp quốc gia MinT chỉ phủ 4,2%, gần như vô dụng. Không suy từ cấp đáy lên cả cây.
2. **Khoảng lấy từ phần dư trong mẫu**: cả hai cột đều phủ thiếu. Phải dùng sai số ngoài mẫu (kéo cấp quốc gia lên 79%), rồi báo phần còn thiếu và nguyên nhân
   (đợt tăng du lịch, chỉ 80 quý).

</details>
