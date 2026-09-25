# Kiểm tra buổi 24 — Ensemble, AutoML và ca khó

## Nhắc lại khái niệm

**Câu 1.** Trên M4, trung bình ETS, Theta thêm LightGBM thì MASE W3 giảm từ 0,867 xuống 0,837. Lý do chính là gì?

- A. LightGBM là mô hình tốt nhất nên kéo trung bình về phía nó
- B. LightGBM học kiểu khác hẳn ETS và Theta, nên sai số của nó ít đi cùng chiều với hai mô hình kia
- C. Trung bình ba mô hình luôn tốt hơn trung bình hai mô hình
- D. LightGBM được học trên nhiều dữ liệu hơn nên không có sai số

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): lợi ích của trung bình phụ thuộc vào tương quan sai số $\rho$; thành phần càng khác loại, sai số càng hay trái dấu và bù nhau.
**A sai**: trung bình đều không "kéo về phía" mô hình giỏi; trọng số của LightGBM vẫn chỉ 1/3, mà kết quả còn tốt hơn chính LightGBM. **C sai**:
thêm một bản sao của mô hình cũ ($\rho$ = 1) không lợi gì. **D sai**: LightGBM vẫn có sai số (MASE 0,855).

</details>

**Câu 2.** "Combination puzzle" nói gì, và vì sao nó xảy ra?

- A. Trọng số đều thường thắng trọng số "tối ưu" ước lượng từ dữ liệu, vì trọng số ước lượng từ ít dữ liệu học cả nhiễu
- B. Kết hợp dự báo luôn tệ hơn mô hình tốt nhất, vì trung bình làm mất thông tin
- C. Trọng số "tối ưu" luôn thắng, nhưng khó tính
- D. Trọng số đều thắng vì mọi mô hình đều giỏi như nhau

<details>
<summary>Đáp án</summary>

**A** (mục 4.2): mỗi chuỗi chỉ có 36 tháng backtest để ước lượng trọng số; trọng số "tối ưu" cho MASE 0,965, tệ hơn trọng số đều 0,837. **B sai**:
ngược với bảng mục 4.1 (trung bình thắng từng thành phần). **C sai**: trọng số "tối ưu" ước lượng trung thực thua. **D sai**: các thành phần không
giỏi như nhau (LightGBM 0,855, AutoETS 0,892); trọng số đều thắng vì không phải ước lượng gì, không vì các mô hình ngang nhau.

</details>

**Câu 3.** Khoảng lạc quan khi chọn mô hình lớn lên khi nào?

- A. Khi thử ít ứng viên hơn
- B. Khi thử nhiều ứng viên hơn và mỗi lựa chọn dựa trên ít dữ liệu hơn
- C. Khi đoạn báo cáo nằm sau đoạn chọn
- D. Khi dùng MASE thay cho MAE

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): chọn cái nhỏ nhất trong nhiều điểm có may rủi thì chọn cả may; trong hình, khoảng lạc quan lớn dần khi thêm
ứng viên, tới 0,22 với 30 ứng viên; chọn một ứng viên chung cho nghìn chuỗi chỉ lạc quan khoảng 0,01. **A sai**: ngược lại. **C sai**: đoạn báo cáo
nằm sau là cách **đo** lạc quan trung thực, không làm nó lớn lên. **D sai**: lạc quan đến từ việc chọn, chỉ số nào cũng bị.

</details>

**Câu 4.** Vì sao buổi này loại Chronos-2 và Toto-2 khỏi preset `medium_quality` khi chạy AutoGluon trên M4?

- A. Vì hai mô hình này không chạy được trên CPU
- B. Vì chúng được huấn luyện trước trên kho dữ liệu có chứa M4, nên chấm chúng trên M4 là chấm trên đề đã xem
- C. Vì chúng luôn thua ETS
- D. Vì AutoGluon không cho dùng hai mô hình cùng lúc

<details>
<summary>Đáp án</summary>

**B** (mục 4.4, điều 1): mô hình tiền huấn luyện chỉ được chấm trên dữ liệu nó chưa thấy. **A sai**: tài liệu không nói vậy; lý do loại là dữ liệu
huấn luyện. **C sai**: không ai chấm chúng trong buổi này, và nếu chấm trên M4 thì kết quả không đáng tin, dù thắng hay thua. **D sai**: preset mặc
định học cả hai cùng các mô hình khác.

</details>

## Vận dụng

**Câu 5.** Ba mô hình có MSE backtest (trước đoạn báo cáo) lần lượt 1, 4, 4. Tính trọng số nghịch MSE.

<details>
<summary>Đáp án</summary>

Nghịch đảo: 1; 0,25; 0,25, tổng 1,5. Trọng số: 1 / 1,5 = **2/3** (≈ 0,667); 0,25 / 1,5 = **1/6** (≈ 0,167) cho mỗi mô hình còn lại; cộng lại bằng 1
(mục 4.2). Nhầm hay gặp: quên chia cho tổng (ra 1; 0,25; 0,25, cộng lại 1,5), hoặc lấy tỷ lệ thuận với MSE (1/9, 4/9, 4/9) — cho mô hình sai nhiều
nhất trọng số lớn nhất.

</details>

**Câu 6.** Ensemble tham lam của AutoGluon chạy 5 lượt, chọn lần lượt: ETS, ETS, Theta, DirectTabular, ETS. Trọng số mỗi mô hình là bao nhiêu?

<details>
<summary>Đáp án</summary>

ETS 3/5 = **0,6**; Theta 1/5 = **0,2**; DirectTabular 1/5 = **0,2** (mục 4.4: trọng số = số lượt được chọn / tổng số lượt). Nhầm hay gặp: chia đều
cho ba mô hình xuất hiện (1/3 mỗi cái), hoặc cho ETS trọng số 1 vì được chọn đầu tiên.

</details>

**Câu 7.** Hai dự báo có sai số cùng độ lệch chuẩn 10, tương quan giữa hai sai số $\rho$ = −0,5 (một cái đoán cao thì cái kia hay đoán thấp). Độ
lệch chuẩn sai số của trung bình hai dự báo là bao nhiêu?

<details>
<summary>Đáp án</summary>

$10 \times \sqrt{(1 + (-0{,}5)) / 2} = 10 \times \sqrt{0{,}25} = 10 \times 0{,}5$ = **5** (mục 4.1). Sai số trái chiều nhau nên trung bình lợi còn
nhiều hơn trường hợp $\rho$ = 0 (7,1). Nhầm hay gặp: quên số 1 trong $1 + \rho$ (ra $\sqrt{-0{,}25}$, không tính được), hoặc chia cho 2 mà quên
lấy căn (ra 2,5).

</details>

**Câu 8.** Một mã mới ra mắt tuần 7/3/2011. Bốn mã ra mắt tuần 10/1, 17/1, 24/1 và 31/1/2011. Mã nào dùng được làm hàng tương tự cho dự báo 8
tuần đầu?

- A. Cả bốn, vì đều ra mắt trước 7/3
- B. Chỉ mã 10/1
- C. Mã 10/1 và 17/1
- D. Không mã nào, vì chưa đủ một năm

<details>
<summary>Đáp án</summary>

**B** (mục 4.5, "Luật không rò rỉ"): 8 tuần đầu của hàng tương tự phải kết thúc trước ngày ra mắt. Mã 10/1 có tuần thứ 8 bắt đầu 28/2, xong trước
7/3. Mã 17/1 có tuần thứ 8 bắt đầu 7/3, chưa xong. **A sai**: chỉ kiểm "ra mắt trước" là mượn tương lai của các mã chưa bán xong. **C sai**: mã
17/1 còn thiếu tuần thứ 8. **D sai**: luật chỉ cần đủ 8 tuần, không cần một năm.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một đồng nghiệp gửi báo cáo:

| Cách làm | MASE |
|---|---|
| chọn mô hình tốt nhất trong 30 ứng viên cho từng chuỗi (chọn trên W1, W2, W3) | 0,694 |
| trung bình ETS, Theta, LightGBM (cả W1, W2, W3) | 0,834 |

Kết luận: "chọn mô hình theo từng chuỗi tốt hơn ensemble 17%, đề nghị dùng cho production". Chỗ sai là gì, và con số trung thực nên lấy thế nào?

<details>
<summary>Đáp án</summary>

Con số 0,694 là **điểm lúc chọn**: mô hình được chọn và được chấm trên cùng ba cửa sổ, nên mang toàn bộ khoảng lạc quan (mục 4.3). Cách trung thực:
chọn trên W1, W2, báo cáo trên W3. Khi đó chọn theo chuỗi ra 0,883, còn ensemble trên W3 là 0,837: ensemble thắng. Hai dòng trong bảng cũng không so
được với nhau: dòng dưới là trung bình không phải chọn gì, dòng trên được nhìn đáp án trước khi chọn. Đề nghị đúng là dùng ensemble.

</details>

**Câu 10.** Một leaderboard AutoGluon chạy trên M4 với preset mặc định, không loại mô hình nào (bảng minh hoạ, số giả định):

| Mô hình | score_val (MASE đoạn kiểm) |
|---|---|
| Chronos2 | 0,61 |
| WeightedEnsemble | 0,60 |
| ETS | 0,88 |
| Theta | 0,90 |

Kết luận: "Chronos-2 tốt hơn ETS gần 30%, và ensemble 0,60 là sai số ta sẽ gặp khi dùng". Tìm hai chỗ sai.

<details>
<summary>Đáp án</summary>

1. **Chronos-2 đã thấy M4 khi tiền huấn luyện** (mục 4.4, điều 1): điểm của nó trên M4 là điểm trên đề đã xem, không đo được khả năng dự báo dữ
   liệu mới. Phải loại nó, hoặc chấm trên dữ liệu sau mốc cắt huấn luyện của mô hình.
2. **score_val là điểm lúc chọn** (mục 4.4, điều 2): AutoGluon chọn và ghép mô hình theo chính điểm này, nên nó lạc quan. Sai số khi dùng phải đo
   trên một đoạn sau, chưa dùng cho quyết định nào (như W3); ở buổi này ensemble đi từ 0,858 trên đoạn kiểm lên 0,882 trên W3.

</details>
