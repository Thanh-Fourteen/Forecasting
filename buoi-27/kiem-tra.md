# Kiểm tra buổi 27 — Dự báo Bayes và Gaussian Process

## Nhắc lại khái niệm

**Câu 1.** Prior predictive check làm gì?

- A. Sinh dữ liệu giả từ prior, trước khi học, để xem prior có tin vào điều vô lý không
- B. So posterior với dữ liệu kiểm
- C. Chọn prior sao cho posterior đẹp nhất trên dữ liệu kiểm
- D. Tính r_hat của prior

<details>
<summary>Đáp án</summary>

**A** (mục 4.2): prior Normal(0, 10) trên log tốc độ sinh ra quantile 0,9 khoảng 20 triệu món/tháng — vô lý với phụ tùng bán vài món. **B sai**: đó là
posterior predictive, chấm sau khi học. **C sai**: chọn prior theo kết quả đoạn kiểm là tune trên đoạn kiểm. **D sai**: r_hat là chẩn đoán MCMC, không
áp cho việc rút từ prior.

</details>

**Câu 2.** Một posterior được dùng khi nào?

- A. Khi r_hat < 1,01
- B. Khi r_hat < 1,01, ESS ≥ 400 và không có divergence
- C. Khi MAE trên đoạn kiểm nhỏ nhất
- D. Khi có ít nhất 4 chuỗi

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): thiếu một điều kiện là không dùng. **A sai**: r_hat chỉ đo phần NUTS đã đi; divergence báo vùng chưa đi tới. **C sai**: GP ba thành phần
có MAE nhỏ hơn mà 27 divergence (mục 4.6). **D sai**: 4 chuỗi là cách chạy, không phải bằng chứng hội tụ.

</details>

**Câu 3.** Trong mô hình phân cấp, mã nào bị kéo về mức chung mạnh nhất?

- A. Mã bán nhiều nhất
- B. Mã có ít tháng lịch sử nhất
- C. Mã có nhiều tháng lịch sử nhất
- D. Mọi mã bị kéo như nhau

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): trọng số của dữ liệu tăng theo số tháng; mã 3 tháng lệch khỏi đường chéo xa nhất trong hình co rút. **A sai**: mã bán nhiều bị kéo xuống
một chút nhưng nếu nhiều tháng thì dữ liệu vẫn thắng. **C sai**: mã 24 tháng gần như không co rút. **D sai**: co rút phụ thuộc lượng dữ liệu.

</details>

**Câu 4.** Ví dụ 8 trường: centered có 64 divergence dù đã nâng target_accept lên 0,95. Cách sửa gốc là gì?

- A. Nâng target_accept lên 0,99
- B. Viết lại θ = μ + τ·z với z ~ Normal(0, 1) (non-centered)
- C. Tăng số mẫu lên 10 lần
- D. Bỏ các mẫu divergence ra khỏi posterior

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): cổ phễu (τ nhỏ ép mọi θ sát nhau) là vấn đề của cách viết; non-centered cho 0 divergence. **A sai**: target_accept chỉ làm bước nhỏ
lại, 0,8 → 0,95 mới bớt từ 312 xuống 64. **C sai**: thêm mẫu không giúp đi vào vùng NUTS trượt. **D sai**: bỏ mẫu không đưa được NUTS tới vùng chưa thăm.

</details>

## Vận dụng

**Câu 5.** Prior Gamma(1, 1) cho tốc độ bán. Bốn tháng bán 0, 0, 0, 2 món. Tính posterior và trung bình của nó; so với trung bình 4 tháng.

<details>
<summary>Đáp án</summary>

Gamma(1 + 2, 1 + 4) = **Gamma(3, 5)**, trung bình 3/5 = **0,6** món/tháng (mục 4.1). Trung bình 4 tháng là 0,5: posterior bị prior (trung bình 1) kéo lên
một chút; dữ liệu nặng 4/5. Nhầm hay gặp: cộng số tháng vào a và tổng số bán vào b, ra Gamma(5, 3).

</details>

**Câu 6.** Hai chuỗi MCMC: trung bình 10 và 12; phương sai trong mỗi chuỗi là 4. Tính gần đúng r_hat. Dùng được không?

<details>
<summary>Đáp án</summary>

Hai trung bình 10 và 12 đều cách trung bình chung 1, nên phương sai giữa chúng là 1. $\hat R \approx \sqrt{1 + 1/4} = \sqrt{1{,}25}$ ≈ **1,12** (mục 4.3).
Lớn hơn 1,01 nhiều: hai chuỗi chưa gặp nhau, **không dùng**. Nhầm hay gặp: chia phương sai trong chuỗi cho phương sai giữa chuỗi, ra $\sqrt{5}$.

</details>

**Câu 7.** Kernel $k(d) = \exp(-d^2 / (2\ell^2))$ với $\ell$ = 30 ngày. Tính độ giống nhau của hai ngày cách 30 ngày và cách 60 ngày. (Cho sẵn
$e^{-0{,}5}$ ≈ 0,61; $e^{-2}$ ≈ 0,14.)

<details>
<summary>Đáp án</summary>

Cách 30: $\exp(-900/1.800) = e^{-0{,}5}$ ≈ **0,61**. Cách 60: $\exp(-3.600/1.800) = e^{-2}$ ≈ **0,14** (mục 4.6). Gấp đôi khoảng cách thì độ giống giảm
mạnh, vì khoảng cách nằm dưới dạng bình phương. Nhầm hay gặp: quên số 2 ở mẫu.

</details>

**Câu 8.** Prior log λ ~ Normal(0, 5). Khoảng ± 2 độ lệch chuẩn của log λ ứng với tốc độ bán nào? Prior này có hợp với phụ tùng bán chậm không?

- A. 0,00005 tới 22.000 món/tháng — không hợp, đầu trên vô lý
- B. −10 tới 10 món/tháng — hợp
- C. 0 tới 10 món/tháng — hợp
- D. 1 tới 5 món/tháng — hợp

<details>
<summary>Đáp án</summary>

**A** (mục 4.2): log λ từ −10 tới 10, tức $e^{-10}$ ≈ 0,00005 tới $e^{10}$ ≈ 22.000 món/tháng. **B sai**: đọc log λ như số món; tốc độ không thể âm.
**C, D sai**: không đổi từ thang log về số món.

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Một đồng nghiệp báo:

| Mô hình | Divergence | r_hat | MAE (lượt) |
|---|---|---|---|
| GP hai thành phần | 0 | 1,003 | 1.142 |
| GP ba thành phần | 27 | 1,026 | 1.071 |

Kết luận: "chọn GP ba thành phần vì MAE thấp hơn 6%". Chỗ sai là gì?

<details>
<summary>Đáp án</summary>

GP ba thành phần chưa hội tụ: 27 divergence và r_hat 1,026 > 1,01 (mục 4.3, 4.6). Posterior của nó không phải posterior thật của mô hình, nên MAE là
may: ba seed cho số divergence từ vài chục tới hơn hai nghìn và coverage từ 82% tới 95%. Phải chọn trong số mô hình đã qua cổng chẩn đoán: GP hai thành phần.

</details>

**Câu 10.** Bảng dự báo 60 ngày cuối 2012:

| Mô hình | r_hat | Divergence | Phủ khoảng 90% |
|---|---|---|---|
| BSTS | 1,002 | 0 | 46,7% |

Kết luận: "BSTS hội tụ hoàn hảo nên khoảng 90% của nó đáng tin". Tìm chỗ sai.

<details>
<summary>Đáp án</summary>

Hội tụ chỉ nói MCMC tính đúng posterior **của mô hình đã viết**; coverage 46,7% nói mô hình đó không hợp với dữ liệu tương lai (mục 4.5). Ở đây nhiễu Gauss
tin quan sát cuối là ngày bão Sandy, nên cả đường dự báo bị kéo xuống. Phải kiểm coverage trên đoạn chấm, và sửa mô hình (nhiễu Student-t, hoặc đánh dấu ngày
bão là thiếu).

</details>
