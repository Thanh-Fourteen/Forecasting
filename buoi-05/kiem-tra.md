# Kiểm tra buổi 5 — Biến đổi và điều chỉnh dữ liệu

## Nhắc lại khái niệm

**Câu 1.** Mục đích chính của việc điều chỉnh lịch, lạm phát, dân số trước khi làm mô hình là:

- A. Làm hình vẽ đẹp hơn
- B. Bỏ những dao động đã biết nguyên nhân, để phần còn lại đơn giản hơn cho mô hình
- C. Làm dự báo luôn cao hơn thực tế
- D. Giảm số tháng dữ liệu cần có

<details>
<summary>Đáp án</summary>

**B** (mục 1, 4.1, 4.2). Ba ngày thêm của tháng 3 hay giá cả tăng là nguyên nhân đã biết; bỏ chúng đi thì mô hình không phải tự
học lại. **A sai**: hình đẹp hơn chỉ là phụ; mục đích là so đúng (tháng 2/2023 đổi từ "giảm 3,4%" thành "tăng 7,0%"). **C sai**:
điều chỉnh không đẩy dự báo theo một chiều nào. **D sai**: số tháng giữ nguyên, chỉ giá trị mỗi tháng được chia lại.

</details>

**Câu 2.** Box-Cox với λ = 0 là:

- A. Không biến đổi gì
- B. Lấy log
- C. Lấy căn bậc hai
- D. Trừ trung bình rồi chia độ lệch chuẩn

<details>
<summary>Đáp án</summary>

**B** (công thức mục 4.4: nhánh $\lambda = 0$ là $\log y$). **A sai**: đó là $\lambda = 1$, cho $y - 1$, chỉ dời xuống 1 đơn vị.
**C sai**: $\lambda = 0{,}5$ mới gần căn bậc hai (100 thành 18 = (10 − 1)/0,5). **D sai**: đó là chuẩn hoá, không thuộc họ Box-Cox.

</details>

**Câu 3.** Dự báo trên thang log rồi đổi ngược bằng `exp`, không hiệu chỉnh. Con số nhận được là:

- A. Trung bình của các giá trị có thể xảy ra
- B. Trung vị của các giá trị có thể xảy ra
- C. Giá trị lớn nhất có thể xảy ra
- D. Quantile 0,9

<details>
<summary>Đáp án</summary>

**B** (mục 4.5). `exp` giữ nguyên thứ tự: số đứng giữa trên thang log vẫn đứng giữa sau khi đổi ngược, nên trung vị đi qua nguyên
vẹn. Ví dụ log 0, 1, 2 → 1; 2,72; 7,39: trung vị là 2,72 = exp(1). **A sai**: `exp` kéo giãn phía trên nên trung bình thật (3,70)
lớn hơn. **C sai**: không có gì chọn giá trị lớn nhất. **D sai**: quantile 0,9 cũng đi qua nguyên vẹn, nhưng tâm của dự báo trên thang
log là số đứng giữa (quantile 0,5), không phải 0,9.

</details>

**Câu 4.** Chuỗi phần trăm tăng trưởng của bán lẻ có 25 tháng âm, và bạn muốn biến đổi kiểu Box-Cox. Cách đúng là:

- A. Dùng Yeo-Johnson
- B. Lấy log của giá trị tuyệt đối
- C. Thay các số âm bằng 0,01 rồi lấy log
- D. Bỏ các tháng âm rồi dùng Box-Cox

<details>
<summary>Đáp án</summary>

**A** (mục 4.4): Yeo-Johnson là biến thể nhận cả số 0 và số âm. **B sai**: −5% và +5% thành cùng một số, mất hẳn chiều tăng giảm.
**C sai**: bịa số liệu, và mọi tháng suy giảm thành cùng một giá trị. **D sai**: bỏ đúng những tháng suy thoái mà dự báo cần biết
nhất.

</details>

## Vận dụng

**Câu 5.** Doanh số tháng 4/2023 (30 ngày) là 661.990 và tháng 5/2023 (31 ngày) là 708.199 triệu USD. Tính tăng trưởng so thẳng và
tăng trưởng theo ngày.

<details>
<summary>Đáp án</summary>

So thẳng: 708.199 / 661.990 − 1 ≈ **+6,98%**. Theo ngày: 661.990 / 30 ≈ 22.066 và 708.199 / 31 ≈ 22.845 triệu/ngày; 22.845 / 22.066
− 1 ≈ **+3,53%**. Gần một nửa "tăng trưởng" chỉ là tháng 5 dài hơn một ngày. Nhầm hay gặp: chia cả hai tháng cho 30.

</details>

**Câu 6.** Bạn dự báo trên thang log với phương sai $\sigma^2$ = 0,09 ($\sigma$ = 0,3). Đổi ngược thẳng được 1.000. Trung bình theo công thức
FPP là bao nhiêu? Nếu $\sigma$ = 1 thì công thức FPP còn dùng tốt không?

<details>
<summary>Đáp án</summary>

1.000 × (1 + 0,09/2) = 1.000 × 1,045 = **1.045**. Với $\sigma$ = 1: FPP cho hệ số 1 + 1/2 = 1,5, còn dạng chính xác là $e^{1/2} \approx
1{,}649$, hụt 1,5 / 1,649 − 1 ≈ **−9%** (bảng mục 4.5). Khi $\sigma$ lớn, dùng $e^{\hat w + \sigma^2/2}$. Nhầm hay gặp: thay $\sigma$ (0,3)
vào chỗ $\sigma^2$, ra 1.150.

</details>

**Câu 7.** Bạn chấm mô hình bằng **MAE** trên doanh số từng tháng. Có nên bật hiệu chỉnh bias không?

<details>
<summary>Đáp án</summary>

**Không.** MAE nhỏ nhất khi dự báo là **trung vị** (buổi 2), mà đổi ngược thẳng đã cho trung vị (mục 4.5). Hiệu chỉnh đẩy dự báo lên
cỡ $\sigma^2/2$, rời khỏi trung vị, nên MAE thường tệ đi. Bật khi cần trung bình: cộng nhiều chuỗi thành tổng, tính doanh thu kỳ vọng,
hay chấm bằng phạt bình phương (mục 4.6).

</details>

**Câu 8.** Bạn tính λ Guerrero trên toàn bộ chuỗi 1992–2026 rồi backtest với các gốc từ 2012. Sai ở đâu? Sửa thế nào?

<details>
<summary>Đáp án</summary>

λ là **tham số của mô hình** (mục 4.4). Tính trên cả chuỗi là dùng dữ liệu sau gốc để chọn tham số, nên backtest đẹp hơn thật. Sửa:
ở mỗi gốc, tính λ chỉ từ dữ liệu trước gốc, lưu lại, và đổi ngược bằng đúng λ đó.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Slide báo cáo: "Doanh số bán lẻ Mỹ tăng 316% từ 1993 tới 2025 — thị trường tăng trưởng mạnh." Bạn có: CPI 144,5 → 321,94;
dân số 260,3 → 341,9 triệu người. Tính lại và viết một câu kết luận trung thực.

<details>
<summary>Đáp án</summary>

Tăng 316% nghĩa là gấp 4,16. Giá thực: 4,16 × 144,5 / 321,94 ≈ 1,87, tức **+87%**. Chia thêm dân số: 1,87 × 260,3 / 341,9 ≈ 1,42,
tức **+42%** trong 32 năm, khoảng **1,1%/năm** (mục 4.2). Câu trung thực: "Chi tiêu bán lẻ thực trên đầu người tăng khoảng 42% trong
32 năm (≈ 1,1%/năm); con số 316% là danh nghĩa, gồm cả lạm phát và tăng dân số." Nhầm hay gặp: nhân CPI thay vì chia, hoặc trừ phần
trăm (316% − 123% − 31%).

</details>

**Câu 10.** Bảng backtest (gốc mỗi tháng 2012–2018, mỗi gốc dự báo 12 tháng, tổng dự báo / tổng thực − 1):

| Chuỗi | $\sigma$ | Đổi ngược thẳng | Có hiệu chỉnh |
|---|---|---|---|
| Tổng bán lẻ | 0,047 | −0,47% | −0,37% |
| Trạm xăng | 0,159 | +3,50% | +4,85% |
| Bách hoá | 0,073 | +9,69% | +9,93% |

Một bạn kết luận: "Hiệu chỉnh bias không đáng tin: có chuỗi tốt lên, có chuỗi tệ đi." Giải thích cho đúng.

<details>
<summary>Đáp án</summary>

Hiệu chỉnh làm đúng việc của nó: luôn đẩy dự báo lên cỡ $\sigma^2/2$ (0,11%; 1,27%; 0,26%, khớp chênh giữa hai cột). Nó chỉ sửa **một**
loại lệch: đổi ngược cho trung vị thay vì trung bình. Lệch còn lại do mô hình: bách hoá đang suy giảm nên seasonal naive có drift dự
báo cao hơn thực tế gần 10%; trạm xăng cũng đang dự báo cao, nên đẩy lên nữa thì tệ thêm (mục 4.6). Kết luận đúng: hiệu chỉnh đáng
làm khi cần trung bình và $\sigma$ đủ lớn; nó không thay được việc sửa mô hình.

</details>
