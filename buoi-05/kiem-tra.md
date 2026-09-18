# Kiểm tra buổi 5 — Biến đổi và điều chỉnh dữ liệu

## Nhắc lại khái niệm

**Câu 1.** Mục đích chính của việc điều chỉnh (lịch, dân số, lạm phát) trước khi mô hình hoá là:

- A. Làm dữ liệu đẹp hơn khi vẽ
- B. Bỏ những biến động đã biết nguyên nhân để mẫu hình còn lại đơn giản hơn
- C. Làm chuỗi dừng
- D. Giảm số quan sát cần có

<details>
<summary>Đáp án</summary>

**B.** FPP: "removing known sources of variation… Simpler patterns are usually easier to model and lead to more accurate forecasts". C là việc của
sai phân (buổi 7). Điều chỉnh không đổi số quan sát (D).

</details>

**Câu 2.** Box-Cox với λ = 0 tương đương:

- A. Không biến đổi
- B. Lấy log
- C. Lấy căn bậc hai
- D. Chuẩn hoá z-score

<details>
<summary>Đáp án</summary>

**B.** λ = 1 là "không làm gì" (chỉ trừ 1), λ = 0,5 gần căn bậc hai, λ = 0 là log (giới hạn của $(y^\lambda-1)/\lambda$ khi λ → 0).

</details>

**Câu 3.** Dự báo trên thang log rồi `exp` đổi ngược, không hiệu chỉnh. Con số nhận được là:

- A. Trung bình của phân phối dự báo
- B. Trung vị của phân phối dự báo
- C. Mode
- D. Quantile 0,9

<details>
<summary>Đáp án</summary>

**B.** Hàm mũ đơn điệu nên giữ nguyên trung vị; trung bình lớn hơn: $E[e^w] = e^{\mu+\sigma^2/2}$. FPP: "it will usually be the median… medians do
not add up, whereas means do."

</details>

**Câu 4.** `scipy.stats.boxcox(y)` báo `ValueError: Data must be positive.` Cách xử lý **không** phù hợp là:

- A. Dùng `scipy.stats.yeojohnson`
- B. Cộng một hằng số vào chuỗi rồi ghi rõ trong báo cáo
- C. Thay mọi giá trị ≤ 0 bằng 1 rồi lấy log
- D. Xem lại vì sao có giá trị âm (có phải chuỗi này là phần trăm thay đổi?)

<details>
<summary>Đáp án</summary>

**C.** Thay số liệu thật bằng hằng số là sửa dữ liệu và làm méo phân phối mà không ai biết. A và B đều được (B phải ghi lại hằng số để đổi ngược),
D là việc nên làm đầu tiên.

</details>

## Vận dụng

**Câu 5.** Doanh số tháng 2/2023 là 595.432 và tháng 3/2023 là 679.701 triệu USD. Tính tăng trưởng thô và tăng trưởng theo ngày.

<details>
<summary>Đáp án</summary>

Thô: $679.701/595.432 - 1 =$ **+14,15%**. Theo ngày: tháng 2/2023 có 28 ngày → 21.265 triệu/ngày; tháng 3 có 31 ngày → 21.926 triệu/ngày;
$21.926/21.265 - 1 =$ **+3,11%**. Phần lớn "tăng trưởng" chỉ là 3 ngày nhiều hơn.

</details>

**Câu 6.** Bạn dự báo trên thang log, σ_h = 0,3. Dự báo đổi ngược thẳng là 1.000. Trung bình xấp xỉ theo FPP là bao nhiêu? Nếu σ_h = 1,0 thì công
thức FPP còn dùng được không?

<details>
<summary>Đáp án</summary>

$1.000 \times (1 + 0{,}3^2/2) = 1.000 \times 1{,}045 =$ **1.045**. Với σ = 1,0, xấp xỉ Taylor cho $1{,}5$ trong khi giá trị đúng là
$e^{0{,}5} = 1{,}649$ — hụt **9,0%**; khi σ lớn dùng $e^{\hat w + \sigma^2/2}$ (cho λ = 0) hoặc mô phỏng.

</details>

**Câu 7.** Bạn chấm mô hình bằng **MAE** trên doanh số theo tháng. Có nên bật hiệu chỉnh bias không? Trả lời kèm lý do.

<details>
<summary>Đáp án</summary>

**Không.** MAE được tối thiểu hoá bởi **trung vị** (FPP §5.8), mà đổi ngược thẳng chính là trung vị. Hiệu chỉnh đẩy dự báo lên σ²/2 nên MAE xấu đi.
Bật hiệu chỉnh khi cần trung bình: cộng dồn nhiều chuỗi, ước lượng doanh thu kỳ vọng, hoặc chấm bằng RMSE.

</details>

**Câu 8.** Bạn tính λ Guerrero trên toàn bộ chuỗi 1992–2026 rồi backtest từ 2012. Sai ở đâu? Sửa thế nào?

<details>
<summary>Đáp án</summary>

λ là **tham số của mô hình**: tính trên toàn chuỗi là dùng dữ liệu tương lai để chọn tham số → rò rỉ, kết quả backtest lạc quan. Sửa: trong mỗi fold,
ước lượng λ (và trung bình/độ lệch chuẩn nếu có chuẩn hoá) **chỉ** từ dữ liệu trước gốc, lưu lại, rồi dùng đúng bộ đó để đổi ngược.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Slide báo cáo: "Doanh số bán lẻ Mỹ tăng 316% từ 1993 đến 2025 — thị trường tăng trưởng mạnh." Bạn có ba con số: CPI 144,5 → 321,94; dân
số 260,3 → 341,9 triệu. Tính lại và viết một câu kết luận trung thực.

<details>
<summary>Đáp án</summary>

Giá thực: $4{,}16 \times 144{,}5/321{,}94 = 1{,}87$ → **+87%**. Chia dân số: $1{,}87 \times 260{,}3/341{,}9 = 1{,}42$ → **+42%** trong 32 năm, khoảng
**1,1%/năm**. Câu trung thực: "Chi tiêu bán lẻ thực trên đầu người tăng khoảng 42% trong 32 năm (≈1,1%/năm); con số 316% là giá danh nghĩa, gồm cả
lạm phát và tăng dân số."

</details>

**Câu 10.** Bảng backtest (gốc mỗi tháng 2012–2018, tầm 12, tổng dự báo / tổng thực − 1):

| Chuỗi | σ | đổi ngược thẳng | có hiệu chỉnh |
|---|---|---|---|
| Tổng bán lẻ | 0,047 | −0,47% | −0,37% |
| Trạm xăng | 0,159 | +3,50% | +4,85% |
| Bách hoá | 0,073 | +9,69% | +9,93% |

Một bạn kết luận: "Hiệu chỉnh bias không đáng tin, có chuỗi tốt lên có chuỗi tệ đi." Giải thích cho đúng.

<details>
<summary>Đáp án</summary>

Hiệu chỉnh luôn đẩy dự báo lên đúng **σ²/2** (0,11%; 1,27%; 0,26% — khớp bảng). Nó chỉ sửa **một** loại lệch: đổi ngược cho trung vị thay vì trung
bình. Các lệch còn lại là do mô hình: bách hoá đang suy giảm nên seasonal naive + drift dự báo cao hơn thực tế gần 10%; trạm xăng cũng dự báo cao
(giá xăng giảm trong giai đoạn đó) nên cộng thêm làm tệ hơn. Kết luận đúng: hiệu chỉnh đáng làm khi cần trung bình và σ lớn; nó không thay được việc
sửa mô hình. Proietti & Lütkepohl (2013) cũng thấy ở tầm ngắn bản không hiệu chỉnh thường có MSE thấp hơn.

</details>
