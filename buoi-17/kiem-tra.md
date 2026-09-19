# Kiểm tra buổi 17 — ARIMA và SARIMA

## Nhắc lại khái niệm

**Câu 1.** ACF tắt dần, PACF có hai cột đáng kể ở trễ 1 và 2 rồi tắt hẳn. Mô hình phù hợp nhất:

- A. MA(2)
- B. AR(2)
- C. ARMA(2,2)
- D. Nhiễu trắng

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): PACF tắt hẳn sau trễ $p$ là dấu vân tay của AR(p). **A sai**: MA(2) thì ACF tắt hẳn sau trễ 2, PACF tắt dần. **C sai**: ARMA làm cả
hai tắt dần, không tắt hẳn. **D sai**: nhiễu trắng thì mọi cột đều nhỏ.

</details>

**Câu 2.** Hai mô hình ARIMA(1,1,1) và ARIMA(2,0,1) trên cùng chuỗi. So AICc để chọn được không?

- A. Được, AICc nhỏ hơn thì tốt hơn
- B. Không, vì khác số lần sai phân nên hai likelihood tính trên hai dữ liệu khác nhau
- C. Được, nếu cả hai qua Ljung–Box
- D. Không, vì AICc chỉ dùng cho ETS

<details>
<summary>Đáp án</summary>

**B** (mục 4.2). **A sai**: đúng khi cùng $d$, $D$. **C sai**: qua Ljung–Box không làm AICc so được. **D sai**: AICc dùng cho mọi mô hình ước lượng bằng
likelihood, kể cả ARIMA.

</details>

**Câu 3.** Phần dư của một mô hình trên dữ liệu tháng có ACF lớn ở trễ 12, Ljung–Box p ≈ 0. Nên làm gì?

- A. Tăng bậc MA thường lên 12
- B. Thêm phần mùa vụ (sai phân mùa vụ và/hoặc MA mùa vụ ở chu kỳ 12)
- C. Bỏ qua, vì AICc đã tốt
- D. Lấy log

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): gai ở trễ 12 là quy luật mùa vụ chưa được mô hình hoá. **A sai**: MA(12) thường tốn 12 tham số cho việc một tham số mùa vụ làm được.
**C sai**: phần dư còn quy luật là mô hình chưa đủ, dù AICc đẹp. **D sai**: log sửa biên độ tăng theo mức, không sửa mùa vụ bị bỏ quên.

</details>

**Câu 4.** Chạy `AutoARIMA()` của statsforecast trên doanh số tháng, không khai tham số nào. Điều gì xảy ra với mùa vụ?

- A. Tự phát hiện chu kỳ 12
- B. Không thử phần mùa vụ, vì `season_length` mặc định là 1
- C. Báo lỗi
- D. Tự lấy log

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): trên 366 chuỗi du lịch, quên chu kỳ làm AutoARIMA thua cả seasonal naive (MASE 2,791 so với 1,720). **A sai**: thư viện không tự đoán
chu kỳ. **C sai**: nó chạy bình thường, chỉ sai lặng lẽ. **D sai**: không có biến đổi tự động.

</details>

## Vận dụng

**Câu 5.** AR(1) không hằng số, $\phi$ = 0,8, giá trị cuối 10. Dự báo 2 bước? ACF lý thuyết ở trễ 2?

<details>
<summary>Đáp án</summary>

Dự báo 0,8 × 10 = **8**, rồi 0,8 × 8 = **6,4**. ACF trễ 2 = 0,8² = **0,64** (mục 4.1). Nhầm hay gặp: nghĩ PACF trễ 2 cũng bằng 0,64; với AR(1) thì
PACF trễ 2 bằng 0.

</details>

**Câu 6.** 200 phần dư của một mô hình có đúng một hệ số MA. ACF phần dư ở trễ 1, 2, 3 là 0,2; 0,15; 0,1. Tính Ljung–Box gộp 3 trễ, số bậc tự do,
và kết luận (ngưỡng 5% với 2 bậc tự do là 5,99).

<details>
<summary>Đáp án</summary>

$Q = 200 \times 202 \times (0{,}04/199 + 0{,}0225/198 + 0{,}01/197) \approx$ **14,8**. Bậc tự do 3 − 1 = **2**. 14,8 > 5,99: p ≈ 0,0006, phần dư còn tự
tương quan (mục 4.4). Nhầm hay gặp: dùng 3 bậc tự do (quên trừ tham số MA).

</details>

**Câu 7.** Bước ngẫu nhiên có $\sigma$ = 3. Khoảng 95% quanh dự báo ở bước 1 và bước 25?

<details>
<summary>Đáp án</summary>

Bước 1: ± 1,96 × 3 = **± 5,88**. Bước 25: ± 5,88 × $\sqrt{25}$ = **± 29,4** (mục 4.5). Nhầm hay gặp: nhân 25 thay vì $\sqrt{25}$ = 5.

</details>

**Câu 8.** Chuỗi tháng, sau sai phân thường và sai phân mùa vụ, ACF chỉ có một gai đáng kể ở trễ 12 (âm); trễ 1 gần 0. Đề xuất SARIMA.

<details>
<summary>Đáp án</summary>

**SARIMA(0,1,0)(0,1,1)12**: gai ACF tắt hẳn ở trễ chu kỳ → một MA mùa vụ; trễ 1 không có gai → không cần MA thường (mục 4.3). Kiểm lại bằng
Ljung–Box và so AICc với auto-ARIMA cùng $d$, $D$. Nhầm hay gặp: vẫn thêm MA(1) "cho chắc"; thừa tham số làm AICc tệ hơn.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Bảng của một đồng nghiệp trên chuỗi du lịch tháng:

| Mô hình | AICc | Kiểm phần dư |
|---|---|---|
| ARIMA(0,1,1) | 181,0 | ổn |
| SARIMA(0,1,1)(0,1,1)12 | −435,2 | ổn |

"ARIMA(0,1,1) cũng ổn, lại đơn giản hơn, nên dùng nó." Chỉ ra hai lỗi.

<details>
<summary>Đáp án</summary>

(1) Cột "ổn" của ARIMA(0,1,1) sai: Ljung–Box thật cho p ≈ 0, ACF phần dư ở trễ 12 là 0,84; hàm kiểm phần dư không kiểm gì (mục 4.3, 4.4). (2)
Không so hai AICc này được vì khác $D$ (mục 4.2); nhưng không cần: mô hình không qua Ljung–Box thì bị loại. "Đơn giản hơn" không cứu được mô hình
bỏ sót mùa vụ.

</details>

**Câu 10.** Kết quả backtest 366 chuỗi du lịch:

| So sánh | Chuỗi thắng | DM p |
|---|---|---|
| AutoARIMA so với seasonal naive | 68,6% | < 0,0001 |
| AutoARIMA so với AutoETS | 50,3% | 0,74 |

"AutoARIMA tốt hơn AutoETS vì MASE trung bình thấp hơn (1,574 so với 1,581)." Nhận xét.

<details>
<summary>Đáp án</summary>

Chênh 0,007 MASE, mỗi mô hình thắng ở khoảng một nửa số chuỗi, DM p = 0,74: không có bằng chứng bên nào tốt hơn (mục 4.6). Kết luận đúng: cả hai thắng
seasonal naive có ý nghĩa và hoà nhau; chọn theo backtest trên dữ liệu của mình hoặc kết hợp cả hai. Nhầm hay gặp: gọi mọi chênh lệch là "tốt hơn"
mà không kiểm định.

</details>
