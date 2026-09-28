# Kiểm tra buổi 29 — Nền deep learning cho chuỗi thời gian

## Nhắc lại khái niệm

**Câu 1.** Vì sao phải chia train và val theo thời gian **trước** rồi mới cắt cửa sổ?

- A. Để có nhiều mẫu train hơn
- B. Vì cắt trước rồi rút ngẫu nhiên thì mẫu train kề một mẫu val có mục tiêu trùng giờ với nó: mạng đã học đáp án mà val sắp hỏi
- C. Vì PyTorch không cắt được cửa sổ sau khi chia
- D. Để đầu vào của mẫu val không được nằm trong thời gian train

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): hai mẫu kề nhau chung $H - 1$ giờ mục tiêu, nên rút ngẫu nhiên một mẫu làm val thì các giờ nó phải đoán vẫn có trong train.
**A sai**: chia đúng còn bỏ bớt mẫu vắt qua mốc, nên ít mẫu hơn. **C sai**: không liên quan tới thư viện. **D sai**: đầu vào của val nằm trong
thời gian train là bình thường; chỉ **mục tiêu** không được trùng.

</details>

**Câu 2.** Cửa sổ đầu vào 3, 5, 7 kW. Mạng có RevIN nhận gì?

- A. 3, 5, 7
- B. 0,6; 1; 1,4
- C. −1, 0, 1
- D. 0, 0,5, 1

<details>
<summary>Đáp án</summary>

**C** (mục 4.2): trung bình 5, độ lệch chuẩn 2 → (3 − 5)/2 = −1, 0, (7 − 5)/2 = 1. **A sai**: đó là không chuẩn hoá. **B sai**: chia cho trung bình,
không phải trừ trung bình rồi chia độ lệch chuẩn. **D sai**: đó là đưa về khoảng 0–1 (min–max), không phải RevIN.

</details>

**Câu 3.** "Gradient biến mất" trong RNN nghĩa là gì?

- A. Mạng không có trọng số nào để học
- B. Tín hiệu học về một giờ xa trong quá khứ bị nhân với số nhỏ hơn 1 qua mỗi bước nên gần bằng 0, mạng không học được quan hệ xa
- C. Hàm mất mát bằng 0
- D. Học suất quá lớn

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): với $h_t = 0{,}5\,h_{t-1} + x_t$, ảnh hưởng của một giờ còn 0,5²⁰ ≈ 0,000001 sau 20 bước. **A sai**: RNN có trọng số. **C sai**:
mất mát vẫn lớn, chỉ là không giảm được nhờ quan hệ xa. **D sai**: học suất lớn làm bước vượt đích (mục 4.3), là chuyện khác.

</details>

**Câu 4.** Trong TCN, "nhân quả" được bảo đảm bằng cách nào?

- A. Đệm số 0 ở cả hai phía chuỗi
- B. Đệm $(k-1)\,d$ số 0 chỉ ở phía trước (bên trái), để đầu ra giờ $t$ chỉ dùng giờ $t$ và các giờ trước
- C. Dùng dilation lớn
- D. Dùng RevIN

<details>
<summary>Đáp án</summary>

**B** (mục 4.5). **A sai**: đệm hai phía làm đầu ra giờ $t$ dùng cả giờ sau $t$ — nhìn tương lai. **C sai**: dilation chỉ giãn khoảng nhìn, không
quyết định nhìn phía nào. **D sai**: RevIN là chuẩn hoá, không liên quan chiều thời gian.

</details>

## Vận dụng

**Câu 5.** Chuỗi 50 giờ, input_size 10, horizon 5, stride 5. Bao nhiêu mẫu?

<details>
<summary>Đáp án</summary>

$\lfloor (50 - 10 - 5) / 5 \rfloor + 1 = 7 + 1 =$ **8** mẫu (mục 4.1). Nhầm hay gặp: quên cộng 1 (ra 7), hoặc quên chia stride (ra 36).

</details>

**Câu 6.** Mạng $\hat y = w x$ (không bias), mẫu $x$ = 4, đáp án $y$ = 2, đang có $w$ = 1, hàm mất mát $|y - \hat y|$, học suất 0,25. Tính $w$ sau
một bước hạ gradient và mất mát mới.

<details>
<summary>Đáp án</summary>

Dự báo 1 × 4 = 4, cao hơn đáp án 2. Tăng $w$ thì dự báo tăng gấp 4, mất mát cũng tăng gấp 4: đạo hàm +4. $w$ ← 1 − 0,25 × 4 = **0**. Dự báo mới
0, mất mát |2 − 0| = **2**, đúng bằng mất mát cũ: học suất lớn làm bước vượt qua đáp án sang phía bên kia (mục 4.3).

</details>

**Câu 7.** TCN có bộ trọng số dài $k$ = 2, bốn lớp dilation 1, 2, 4, 8. Vùng nhìn bao nhiêu giờ? Đủ cho input_size 24 không?

<details>
<summary>Đáp án</summary>

1 + (2 − 1) × (1 + 2 + 4 + 8) = **16** giờ (mục 4.5). **Không đủ**: 8 giờ đầu của cửa sổ 24 giờ không ảnh hưởng tới đầu ra cuối. Cần thêm một lớp
dilation 16 (vùng nhìn 32) hoặc tăng $k$ lên 3 (vùng nhìn 31).

</details>

**Câu 8.** MAE val sau epoch 1–8: 0,50; 0,42; 0,40; 0,41; 0,39; 0,395; 0,40; 0,41. Dừng sớm với kiên nhẫn 2 epoch. Dừng ở epoch nào, giữ trọng
số epoch nào?

<details>
<summary>Đáp án</summary>

Tốt nhất tạm thời 0,40 ở epoch 3; epoch 4 không giảm (đếm 1); epoch 5 giảm xuống 0,39, đếm lại từ 0; epoch 6 và 7 không thấp hơn 0,39 (đếm 1, 2) →
**dừng sau epoch 7, giữ trọng số epoch 5** (mục 4.6). Nhầm hay gặp: dừng ở epoch 4 vì quên rằng epoch 5 lại giảm; hoặc giữ trọng số epoch 7.

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Một báo cáo nội bộ viết: "Chúng tôi cắt 2 năm điện tiêu thụ của 5 khách hàng thành cửa sổ 168 → 24 giờ, rồi `train_test_split(...,
shuffle=True, test_size=0.2)`. Kết quả trên tập test:"

| Mô hình | MAE (kW) |
|---|---|
| LSTM 3 lớp, 512 nút, 300 epoch | 3,1 |
| MLP 2 lớp | 5,8 |

"LSTM giảm sai số 47%, đề nghị đưa vào vận hành." Chỉ ra hai lỗi làm con số này không tin được.

<details>
<summary>Đáp án</summary>

(1) **Rò rỉ chồng lấn** (mục 4.1): cắt cửa sổ rồi chia ngẫu nhiên, "tập test" gồm các mẫu kề mẫu train, chung mục tiêu; LSTM lớn, học 300 epoch
trên 5 chuỗi thì học thuộc được, nên càng lớn càng "giỏi" trên tập này. Phải chia theo thời gian, test là đoạn sau cùng. (2) **Không có
baseline** (mục 4.6): không có seasonal naive hay một mô hình thống kê, LightGBM trên cùng mốc test; "giảm 47%" chỉ so hai mạng với nhau, không
biết cả hai có hơn "lặp lại tuần trước" không. Ngoài ra MAE tính bằng kW trộn 5 khách cỡ khác nhau; nên dùng MASE.

</details>

**Câu 10.** Ở hình khách T129 (mục 4.2), bên phải, đường cam (MLP dùng scaler học trên train) nằm dưới đường đen gần như suốt ngày. Vì sao, và
sửa thế nào?

<details>
<summary>Đáp án</summary>

T129 dùng điện tăng khoảng 40% trong năm 2014. Scaler học trên train giữ trung bình và độ lệch chuẩn cũ, nên khi trả dự báo về kW, mạng kéo
dự báo về **mức cũ, thấp hơn** thực tế (mục 4.2). Sửa: RevIN, lấy mức và biên độ từ chính 168 giờ đầu vào (đường xanh dương). **Không** sửa bằng
cách cho scaler học cả đoạn test: đó là rò rỉ tương lai.

</details>
