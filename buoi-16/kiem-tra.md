# Kiểm tra buổi 16 — Exponential smoothing và Theta

## Nhắc lại khái niệm

**Câu 1.** Trong SES, α gần 1 nghĩa là:

- A. Mức gần như chỉ bằng số quan sát mới nhất: phản ứng nhanh, lặp lại cả nhiễu
- B. Mức gần như bằng trung bình cả lịch sử
- C. Dự báo tăng theo xu hướng
- D. Mô hình có mùa vụ nhân

<details>
<summary>Đáp án</summary>

**A** (mục 4.1): mức mới = α × số mới + (1 − α) × mức cũ; α = 1 thì mức = số mới, SES thành naive. **B sai**: đó là α gần 0 (mức gần như đứng
yên ở giá trị ban đầu, quên chậm). **C sai**: SES dự báo phẳng; xu hướng là việc của Holt. **D sai**: α không liên quan mùa vụ.

</details>

**Câu 2.** Chuỗi có biên độ mùa vụ lớn dần theo mức. Nên dùng:

- A. Holt–Winters mùa vụ cộng
- B. Holt–Winters mùa vụ nhân (hoặc lấy log rồi dùng cộng)
- C. SES
- D. Theta không mùa vụ

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): mùa vụ nhân để biên độ tỷ lệ với mức; hành khách EU: MAPE 2,13% so với 3,23% của dạng cộng. **A sai**: dạng cộng giữ biên độ cố
định nên hụt đỉnh. **C, D sai**: bỏ hẳn mùa vụ.

</details>

**Câu 3.** Tên ETS(M,Ad,N) nghĩa là:

- A. Sai số nhân, xu hướng cộng tắt dần, không mùa vụ
- B. Mùa vụ nhân, xu hướng cộng, không sai số
- C. Sai số nhân, xu hướng nhân, mùa vụ nhân
- D. Mô hình trung bình trượt

<details>
<summary>Đáp án</summary>

**A** (mục 4.4): ba chữ theo thứ tự sai số, xu hướng, mùa vụ; Ad là cộng tắt dần, N là không có. **B sai**: chữ đầu là sai số, không phải mùa vụ.
**C sai**: chỉ chữ đầu là M. **D sai**: ETS là họ làm trơn hàm mũ.

</details>

**Câu 4.** Vì sao viết SES thành mô hình state space ETS(A,N,N) lại có ích?

- A. Để dự báo nhanh hơn
- B. Để có likelihood (chọn mô hình bằng AICc) và có khoảng dự báo
- C. Để bỏ được tham số α
- D. Để dùng được với dữ liệu có số 0

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): có mô hình mô tả cách dữ liệu được tạo ra thì tính được xác suất dữ liệu và phương sai sai số $h$ bước tới. **A sai**: dự báo điểm như nhau. **C sai**:
α vẫn còn, còn được ước lượng bằng likelihood. **D sai**: sai số cộng thì dùng được với số 0 ngay cả khi không viết thành state space.

</details>

## Vận dụng

**Câu 5.** SES với α = 0,4, mức ban đầu 50, dữ liệu $(50, 60, 55)$. Tính giá trị khớp cho $y_1$, $y_2$ và dự báo bước tới.

<details>
<summary>Đáp án</summary>

Khớp $y_1$ = 50; mức mới 0,4 × 60 + 0,6 × 50 = 54. Khớp $y_2$ = 54; mức mới 0,4 × 55 + 0,6 × 54 = 54,4. Dự báo **54,4** (mục 4.1). Nhầm hay gặp:
khớp $y_1$ bằng 54 (mức đã trộn cả $y_1$): nhìn trộm, và nếu làm vậy khi tối ưu thì α chạy về 1.

</details>

**Câu 6.** Holt có mức cuối 200, độ dốc cuối 10. Dự báo 3 bước của Holt thường, và của bản tắt dần với $\phi$ = 0,9.

<details>
<summary>Đáp án</summary>

Holt: 210, 220, 230. Tắt dần: 200 + 0,9 × 10 = **209**; 200 + (0,9 + 0,81) × 10 = **217,1**; 200 + (0,9 + 0,81 + 0,729) × 10 = **224,39** (mục 4.2).
Nhầm hay gặp: nhân $\phi^h$ một lần (200 + 0,729 × 10 = 207,29 ở bước 3); phải cộng dồn $\phi + \dots + \phi^h$.

</details>

**Câu 7.** ETS(A,N,N) có $\sigma$ = 5, α = 0,6. Tính độ lệch chuẩn sai số dự báo ở bước 1 và bước 5, và khoảng 95% ở bước 5 quanh dự báo 100.

<details>
<summary>Đáp án</summary>

Bước 1: 5. Bước 5: $5\sqrt{1 + 4 \times 0{,}36} = 5\sqrt{2{,}44} \approx$ **7,81**. Khoảng 95%: 100 ± 1,96 × 7,81 ≈ **(84,7; 115,3)** (mục 4.4). Nhầm hay
gặp: giữ độ rộng bước 1 cho mọi bước vì "SES dự báo phẳng".

</details>

**Câu 8.** Chuỗi $(20, 23, 26, 29, 32)$: đường thẳng khớp dốc 3. SES với α = 1 cho mức cuối 32. Theta chuẩn dự báo 2 bước bao nhiêu? Holt (khớp
hoàn hảo, độ dốc 3) dự báo bao nhiêu?

<details>
<summary>Đáp án</summary>

Theta: 32 + 1,5 = **33,5**; 32 + 3 = **35**. Holt: 35, 38 (mục 4.5). Theta cộng nửa độ dốc nên dè dặt hơn. Nhầm hay gặp: cộng cả độ dốc 3 vào
Theta.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo viết: "Tối ưu SES trên 27 năm dữ liệu cho α = 1,000 và tổng bình phương sai số khớp bằng 0: mô hình khớp hoàn hảo, dùng
luôn." Chỉ ra lỗi.

<details>
<summary>Đáp án</summary>

Sai số khớp bằng 0 trên dữ liệu thật là dấu hiệu nhìn trộm: giá trị khớp cho $y_t$ đã được tính **sau** khi trộn $y_t$ vào mức, nên α = 1 làm
mức bằng đúng $y_t$ (mục 4.1). Sửa: ghi giá trị khớp là mức **trước** khi cập nhật; khi đó α tối ưu của chuỗi T249 là 0,632. Bài kiểm nhiễu
mục tiêu (buổi 13) bắt được lỗi này tự động.

</details>

**Câu 10.** Bảng backtest 366 chuỗi du lịch:

| Mô hình | MASE trung bình | Chuỗi thắng seasonal naive | DM p | Tỷ lệ phủ khoảng 95% |
|---|---|---|---|---|
| AutoTheta | 1,691 | 57,9% | 0,49 | 83,5% |
| seasonal naive | 1,720 | — | — | — |

"AutoTheta thắng seasonal naive ở đa số chuỗi, nên thay seasonal naive bằng AutoTheta và dùng khoảng 95% của nó để đặt dự trữ." Nhận xét.

<details>
<summary>Đáp án</summary>

Hai lỗi (mục 4.6). (1) Thắng ở 57,9% chuỗi nhưng DM p = 0,49: chênh trung bình nhỏ so với dao động giữa các chuỗi, chưa có bằng chứng AutoTheta
tốt hơn. (2) Khoảng "95%" chỉ phủ 83,5%: thực tế rơi ra ngoài 16,5% số tháng thay vì 5%. Đặt dự trữ ở cận trên thì, nếu lệch đều hai phía, thiếu hàng
khoảng 8% số tháng thay vì 2,5%: gấp ba lần dự tính. AutoETS mới là mô hình thắng có ý
nghĩa (p < 0,0001) và khoảng 80% của nó phủ đúng.

</details>
