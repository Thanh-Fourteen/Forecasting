# Kiểm tra buổi 12 — Khử nhiễu và miền tần số

10 câu. Tự làm trước, mở đáp án sau.

---

**1 (nhắc lại).** Tần số Nyquist là gì? Dữ liệu lấy mẫu 10 phút có Nyquist bằng bao nhiêu, và điều đó nghĩa là gì?

<details><summary>Đáp án</summary>

$f_{\text{Nyq}} = f_s/2$. Với mẫu 10 phút, $f_s = 6$ mẫu/giờ → Nyquist = **3 chu kỳ/giờ** (chu kỳ ngắn nhất phân biệt được là 20 phút).
Mọi dao động nhanh hơn thế không biến mất mà **gập** xuống thành một tần số thấp giả.

</details>

---

**2 (nhắc lại).** Vì sao `filtfilt` có "zero phase"? Điều đó khiến nó dùng được vào việc gì và không dùng được vào việc gì?

<details><summary>Đáp án</summary>

Vì nó chạy bộ lọc **hai lần: một lần xuôi, một lần ngược thời gian** — độ trễ của lượt xuôi bị lượt ngược triệt tiêu. Dùng được: mô tả,
trực quan hoá, tách xu hướng trên dữ liệu lịch sử đã hoàn tất. Không dùng được: **bất kỳ feature nào cho mô hình dự báo**, vì lượt chạy
ngược dùng dữ liệu tương lai. Đo được: sửa 10 điểm cuối làm đổi đầu ra lùi tới mốc 126/400.

</details>

---

**3 (nhắc lại).** Ngưỡng phổ quát trong wavelet denoising là gì, và $\sigma$ được ước lượng thế nào?

<details><summary>Đáp án</summary>

$\lambda = \sigma\sqrt{2\ln n}$, với $\hat\sigma = \operatorname{median}\lvert d_J\rvert / 0{,}6745$ — MAD của hệ số chi tiết ở thang mịn
nhất (thang này gần như chỉ chứa nhiễu). Ngưỡng **mềm** co các hệ số về 0 một lượng $\lambda$; ngưỡng cứng giữ nguyên hệ số lớn.

</details>

---

**4 (nhắc lại).** Kalman filter và Kalman smoother khác nhau chỗ nào về mặt thông tin dùng?

<details><summary>Đáp án</summary>

Filter ước lượng trạng thái tại $t$ chỉ từ $y_{1:t}$ → **nhân quả**, dùng được làm feature. Smoother ước lượng từ $y_{1:T}$ (cả chuỗi) →
RMSE thấp hơn (0,402 so với 0,584 đo được) nhưng **không nhân quả**. Trong statsmodels: `filtered_state` so với `smoothed_state` /
`smoothed_forecasts`.

</details>

---

**5 (vận dụng).** Bạn thêm feature `y.rolling(24, center=True).mean()` và MAE backtest giảm từ 46,8 xuống 33,9. Bạn kết luận gì và kiểm
chứng thế nào trong 5 dòng code?

<details><summary>Đáp án</summary>

Kết luận: **rò rỉ tương lai**, không phải feature tốt — `center=True` lấy 12 điểm sau thời điểm hiện tại. Kiểm chứng: đổi 10 giá trị cuối
chuỗi, tính lại feature, so mọi mốc **trước** điểm đổi; nếu có mốc nào đổi → không nhân quả.

```python
goc = f(y); y2 = y.copy(); y2[-10:] += 50
lech = np.abs(f(y2)[:-10] - goc[:-10]); print(lech.max())   # > 0 là rò rỉ
```

Sửa: bỏ `center=True` (cửa sổ kết thúc tại $t$). Mức cải thiện thật chỉ còn khoảng −5,8%.

</details>

---

**6 (vận dụng).** Một đồng nghiệp viết bài kiểm nhân quả nhưng bỏ qua 200 điểm cuối "cho chắc". Kết quả: MA centered 13 được báo là nhân
quả. Vì sao sai?

<details><summary>Đáp án</summary>

MA centered cửa sổ 13 chỉ nhìn 6 điểm về phía trước, nên khi sửa 10 điểm cuối, đầu ra chỉ đổi ở **6 mốc ngay trước điểm đổi** (mốc 384 khi
n = 400). Bỏ qua 200 điểm cuối là bỏ qua đúng vùng duy nhất có bằng chứng. Phải so **mọi** mốc trước điểm đổi; và dung sai phải theo thang
dữ liệu ($10^{-7}\max\lvert y\rvert$), không phải một hằng số tuyệt đối.

</details>

---

**7 (vận dụng).** Bạn hạ mẫu dữ liệu 10 phút về 1 giờ bằng `resample("1h").mean()` và thấy một chu kỳ 2,5 giờ mới xuất hiện. Giải thích và
sửa.

<details><summary>Đáp án</summary>

Aliasing: thành phần 1,4 chu kỳ/giờ (chu kỳ 43 phút) vượt Nyquist mới (0,5 chu kỳ/giờ) nên gập thành $\lvert 1{,}4 - 1\rvert = 0{,}4$
chu kỳ/giờ = chu kỳ 2,5 giờ. Sửa: lọc thông thấp (Butterworth ~0,8 × Nyquist mới) **trước** khi hạ mẫu. Đo được: công suất tại 2,5 h là
64,0 (thô) so với 0,0 (có lọc).

</details>

---

**8 (vận dụng).** Bộ lọc của bạn nhân quả, nhưng $\sigma$ dùng cho ngưỡng wavelet lại tính bằng MAD trên **toàn chuỗi**. Có vấn đề gì?
Sửa thế nào?

<details><summary>Đáp án</summary>

Có: **tham số** cũng là thông tin. Ước lượng $\sigma$ (hoặc tần số cắt, hoặc tham số Kalman) trên toàn chuỗi nghĩa là feature tại thời
điểm $t$ phụ thuộc vào dữ liệu sau $t$ — bài kiểm sửa-đuôi sẽ bắt được (Kalman khớp lại cả chuỗi đổi quá khứ 1,134, bản tham số cố định
đổi 0,000). Sửa: ước lượng tham số **chỉ trên phần học**, cố định lại, và ghi giá trị vào tài liệu.

</details>

---

**9 (đọc biểu đồ).** Hình `bo-loc.png` cho bảng RMSE trên tín hiệu tổng hợp: MA centered 0,357 < Kalman smoother 0,402 < SavGol 0,418 <
Kalman filter 0,584 < Wavelet 0,632 < filtfilt 0,770 < EWMA 0,906 < MA trailing 1,133 < Butterworth nhân quả 2,419. Bạn được yêu cầu chọn
bộ lọc "tốt nhất" để làm feature dự báo. Chọn cái nào, và vì sao ba cái đứng đầu bị loại?

<details><summary>Đáp án</summary>

Chọn **Kalman filter với tham số cố định** (0,584) — tốt nhất **trong nhóm nhân quả**; nếu cần đơn giản và rẻ thì EWMA (0,906, trễ 4 bước,
bộ nhớ O(1)).

Ba cái đứng đầu (MA centered, Kalman smoother, SavGol) đều **dùng tương lai**: RMSE thấp vì chúng biết trước tín hiệu đi đâu. Bảng xếp hạng
RMSE mà thiếu cột "dùng tương lai?" là bảng vô nghĩa cho dự báo. Cũng lưu ý Butterworth nhân quả xếp bét không phải vì lọc kém mà vì **trễ
19 bước** — với dự báo 1 bước, một feature trễ 19 bước gần như không mang thông tin (cải thiện chỉ 1,02%).

</details>

---

**10 (đọc bảng — tìm chỗ sai).** Một báo cáo nội bộ:

| Kết luận | Bằng chứng |
|---|---|
| (a) "Savitzky–Golay an toàn cho feature vì mode `interp` không mở rộng tín hiệu ở biên." | tài liệu scipy |
| (b) "Wavelet giúp MAE giảm 7,09% — cải thiện khiêm tốn nhưng thật." | bảng backtest |
| (c) "Sau khi khử nhiễu mục tiêu, MAE giảm còn 35,78; mô hình đã tốt lên 23,6%." | bảng backtest |
| (d) "Hamilton (2018) chứng minh không bao giờ được dùng HP filter, nên ta bỏ luôn mọi bộ lọc hai chiều." | bài báo |

Chỉ ra chỗ sai của từng dòng.

<details><summary>Đáp án</summary>

- **(a)** Sai. `interp` "không mở rộng" nhưng **fit một đa thức bậc `polyorder` trên `window_length` điểm cuối** rồi dùng nó tính
  `window_length // 2` giá trị cuối — vẫn là dùng điểm sau $t$. Bài kiểm sửa-đuôi cho lượng đổi 20,629.
- **(b)** Sai: wavelet cũng **không nhân quả** (`waverec` dùng cả chuỗi, $\sigma$ tính trên cả chuỗi; đổi quá khứ 7,733). Con số −7,09%
  nguy hiểm hơn −27,67% chính vì nó nhỏ và trông hợp lý.
- **(c)** Sai nặng nhất. Mô hình **không tốt lên**; nó chỉ được chấm trên một mục tiêu dễ hơn và không có thật. Luôn chấm trên chuỗi gốc
  (46,84).
- **(d)** Hai lỗi. Thứ nhất, Hamilton bị **phản biện** (Moura 2024: hai bộ lọc cho kết quả rất giống nhau; bộ lọc Hamilton có độ trễ cơ
  học) — đừng trích một chiều. Thứ hai, điều thật sự rút ra được là **giá trị ở cuối mẫu khác hẳn giá trị ở giữa mẫu**; đó là lý do không
  dùng bộ lọc hai chiều **làm feature dự báo**, chứ không phải cấm chúng trong mọi việc (mô tả lịch sử vẫn tốt).

</details>
