# Kiểm tra buổi 12 — Khử nhiễu và miền tần số

## Nhắc lại khái niệm

**Câu 1.** Bộ lọc nhân quả là bộ lọc mà:

- A. Đầu ra tại $t$ chỉ dùng dữ liệu tới $t$
- B. Đầu ra không bị trễ
- C. Cho RMSE thấp nhất
- D. Chạy xuôi rồi chạy ngược thời gian

<details>
<summary>Đáp án</summary>

**A** (mục 4.1). **B sai**: bộ lọc nhân quả luôn trễ (trung bình 13 điểm gần nhất trễ 6 bước); không trễ thường là dấu hiệu đã nhìn tương lai.
**C sai**: ba RMSE thấp nhất trong buổi đều thuộc bộ lọc nhìn tương lai. **D sai**: đó là `filtfilt`, không nhân quả.

</details>

**Câu 2.** Dữ liệu 15 phút một mẫu. Tần số Nyquist là:

- A. 4 chu kỳ/giờ
- B. 2 chu kỳ/giờ
- C. 15 chu kỳ/giờ
- D. 0,5 chu kỳ/giờ

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): $f_s$ = 4 mẫu/giờ, Nyquist = $f_s/2$ = 2 chu kỳ/giờ, tức chỉ thấy đúng dao động chậm hơn chu kỳ 30 phút. **A sai**: đó là tần số
lấy mẫu. **C sai**: nhầm phút với tần số. **D sai**: đó là Nyquist của dữ liệu một giờ một mẫu.

</details>

**Câu 3.** Butterworth chạy bằng `filtfilt` không trễ vì:

- A. Nó cắt tần số sắc hơn
- B. Nó chạy xuôi rồi chạy ngược thời gian, nên dùng cả dữ liệu sau $t$
- C. Nó dùng ít điểm hơn
- D. Nó là bộ lọc Kalman

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): chạy ngược bù đúng phần trễ của chạy xuôi, đổi lại là nhìn tương lai; bài kiểm đổi đuôi thấy nó làm bẩn ngược 274 bước. **A
sai**: độ sắc không quyết định trễ bằng 0. **C sai**: nó dùng nhiều điểm hơn (cả hai phía). **D sai**: hai họ bộ lọc khác nhau.

</details>

**Câu 4.** Kalman filter (chỉ dùng quá khứ) nhưng tham số được khớp lại trên **cả chuỗi** mỗi lần chạy. Nó:

- A. Vẫn nhân quả, vì filter chỉ dùng quá khứ
- B. Không nhân quả, vì tham số đã dùng dữ liệu tương lai
- C. Không trễ
- D. Là Kalman smoother

<details>
<summary>Đáp án</summary>

**B** (mục 4.5): bài kiểm đổi đuôi cho quá khứ đổi 1,134, trong khi bản tham số cố định đổi 0,000. **A sai**: rò rỉ đi qua tham số. **C sai**:
nó vẫn trễ 1 bước như bản cố định. **D sai**: smoother dùng cả chuỗi để ước lượng từng điểm; đây vẫn là filter.

</details>

## Vận dụng

**Câu 5.** Chuỗi $(6, 9, 3, 12, 6)$. Tính trung bình trượt 3 điểm kiểu trailing và centered tại điểm thứ ba. Rồi đổi số cuối từ 6 thành 30:
đầu ra centered tại điểm thứ tư đổi từ bao nhiêu thành bao nhiêu?

<details>
<summary>Đáp án</summary>

Điểm thứ ba: trailing (6 + 9 + 3)/3 = **6**; centered (9 + 3 + 12)/3 = **8**. Điểm thứ tư kiểu centered: (3 + 12 + 6)/3 = **7** → (3 + 12 + 30)/3 =
**15**. Một con số quá khứ đổi khi dữ liệu mới về: bộ lọc nhìn tương lai (mục 4.1). Trailing ở điểm thứ tư vẫn (9 + 3 + 12)/3 = 8.

</details>

**Câu 6.** Dữ liệu 10 phút một mẫu có dao động chu kỳ 90 phút. Hạ mẫu thô về một giờ một mẫu. Dao động đó giả dạng thành chu kỳ bao nhiêu?
Làm gì để tránh?

<details>
<summary>Đáp án</summary>

$f$ = 60/90 ≈ 0,667 chu kỳ/giờ; $f_s$ = 1; Nyquist 0,5 < 0,667 nên bị gập. $k$ = round(0,667) = 1; $f_{\text{giả}}$ = |0,667 − 1| ≈ 0,333 chu
kỳ/giờ, tức chu kỳ giả **3 giờ** (mục 4.3). Tránh: lọc thông thấp (khoảng 0,8 lần Nyquist mới) trước khi hạ mẫu.

</details>

**Câu 7.** EWMA với $\alpha = 0{,}25$, $z_{t-1} = 40$, số mới $y_t = 80$. Tính $z_t$. Một đồng nghiệp tái lập bằng `com=3`: có cùng bộ lọc không?

<details>
<summary>Đáp án</summary>

$z_t$ = 0,25 × 80 + 0,75 × 40 = **50**. `com=3` cho $\alpha$ = 1/(1 + 3) = 0,25: **cùng** bộ lọc (mục 4.4). Nếu đồng nghiệp truyền `span=3` thì
$\alpha$ = 2/4 = 0,5, khác hẳn. Nhầm hay gặp: coi `span` và `com` là một.

</details>

**Câu 8.** Bảng MAE dự báo điện 1 giờ tới: không lọc 46,84; trung bình trượt trailing 44,12; EWMA 44,10; trung bình trượt centered 33,88;
`filtfilt` 35,37. Nên đưa feature nào vào mô hình dùng thật, và báo cải thiện bao nhiêu?

<details>
<summary>Đáp án</summary>

EWMA hoặc trung bình trượt trailing: nhân quả, cải thiện khoảng **5,8%** (mục 4.6). Centered và `filtfilt` nhìn tương lai; mức giảm 24–28% sẽ
biến mất khi dùng thật. Nhầm hay gặp: chọn feature có MAE thấp nhất mà không có cột "dùng tương lai?".

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Bảng RMSE khử nhiễu trên tín hiệu mô phỏng (biết trước tín hiệu thật): trung bình trượt centered 0,357; Kalman smoother 0,402;
Savitzky–Golay 0,418; Kalman filter tham số cố định 0,584; EWMA 0,906. Báo cáo kết luận: "Dùng trung bình trượt centered làm feature cho mô
hình dự báo, vì nó khử nhiễu tốt nhất." Chỉ ra lỗi.

<details>
<summary>Đáp án</summary>

Ba RMSE thấp nhất đều nhìn tương lai; bảng không có cột "nhân quả" thì vô nghĩa cho dự báo (mục 4.4–4.5). Chỉ so trong nhóm nhân quả: Kalman
filter tham số cố định (0,584) tốt nhất, rồi EWMA (0,906). Khử nhiễu tốt khi mô tả lịch sử không có nghĩa là feature tốt khi dự báo.

</details>

**Câu 10.** Báo cáo gửi sếp:

| Thay đổi | MAE dự báo điện 1 giờ tới |
|---|---|
| ban đầu | 46,84 |
| làm trơn mục tiêu bằng trung bình trượt centered 13 rồi chấm | 35,78 |

"Mô hình cải thiện 23,6% nhờ khử nhiễu." Chỉ ra lỗi và nói phải báo gì.

<details>
<summary>Đáp án</summary>

Mô hình không đổi; chỉ **thước đo** đổi: chấm trên một mục tiêu đã làm trơn, dễ hơn và không có thật (không ai trả tiền điện "đã làm trơn"),
lại được làm trơn bằng bộ lọc nhìn tương lai (mục 4.6). Phải chấm trên điện thật: MAE vẫn 46,84, tức cải thiện 0%. Nếu sếp cần trung bình vài
giờ tới thì định nghĩa lại mục tiêu cho rõ và ghi vào báo cáo.

</details>
