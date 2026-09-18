# Kiểm tra buổi 10 — Làm sạch và dữ liệu thiếu

10 câu. Tự làm trước, mở đáp án sau.

---

**1 (nhắc lại).** Nêu hai loại thiếu và cách phát hiện từng loại.

<details><summary>Đáp án</summary>

(a) **Thiếu giá trị**: có dòng, ô rỗng → `df.isna().sum()`. (b) **Thiếu mốc**: không có dòng nào cho thời điểm đó → so số dòng với
`pd.date_range(min, max, freq)`, hoặc `reindex` lên lưới đều rồi mới `isna()`. Ở trạm Nội Bài 2024: chỉ **2** ô rỗng nhưng **249** mốc
thiếu — chỉ dùng `isna()` sẽ kết luận sai hoàn toàn.

</details>

---

**2 (nhắc lại).** MCAR, MAR, MNAR khác nhau thế nào? Cho một ví dụ cảm biến cho mỗi loại.

<details><summary>Đáp án</summary>

- **MCAR**: xác suất thiếu độc lập với mọi thứ — mất điện ngẫu nhiên vài phút.
- **MAR**: phụ thuộc **dữ liệu quan sát được** — trạm hay hỏng vào mùa mưa (mà mùa thì ta biết).
- **MNAR**: phụ thuộc **chính giá trị bị thiếu** — cảm biến quá tải và tắt khi ô nhiễm cực cao.

MCAR/MAR điền được (MAR cần mô hình có biến giải thích); MNAR thì không, chỉ có thể mô hình hoá cơ chế thiếu và nói rõ giới hạn.

</details>

---

**3 (nhắc lại).** Vì sao `visibility = 9.999` trong GHCNh không phải một số đo?

<details><summary>Đáp án</summary>

Vì đó là **mã**. METAR quy định tầm nhìn từ 10 km trở lên ghi là `9999` (mét); GHCNh đổi đơn vị sang km thành 9.999. Nó chiếm **35,0%** số
dòng ở trạm này. Coi là số đo thì trung bình tầm nhìn bị kéo lên và histogram có một đỉnh giả.

</details>

---

**4 (nhắc lại).** Cột `da_dien` dùng để làm gì? Nêu ba việc.

<details><summary>Đáp án</summary>

(1) Hạ trọng số (hoặc loại) các ô đã điền khi huấn luyện; (2) loại chúng khỏi tập chấm để sai số không bị bóp méo; (3) truy vết — trả lời
được "số này từ đâu ra" nhiều tháng sau. Dữ liệu sạch không truy vết được thì không dùng cho báo cáo nghiêm túc.

</details>

---

**5 (vận dụng).** Báo cáo chất lượng ghi `relative_humidity: min = 100, max = 94`. Chuyện gì đã xảy ra, và kiểm chứng trong một dòng code?

<details><summary>Đáp án</summary>

Cột đang là **chuỗi**, nên `min`/`max` so theo thứ tự chữ cái ("100" < "94"). Kiểm: `df.dtypes` (hoặc `df["relative_humidity"].dtype`).
Sửa: `pd.to_numeric(..., errors="coerce")` cho mọi cột đo ngay khi đọc. Nguy hiểm ở chỗ **không có exception nào** — mọi thống kê sai âm
thầm.

</details>

---

**6 (vận dụng).** Bạn thấy 24 đoạn nhiệt độ "đứng yên" ≥ 12 giờ, tổng 4,15% dữ liệu. Có phải cảm biến hỏng không? Kiểm thế nào?

<details><summary>Đáp án</summary>

Chưa chắc. Kiểm **độ phân giải** trước: ở trạm này nhiệt độ chỉ có 33 giá trị khác nhau, bước nhỏ nhất **1,0 °C**, 100% là số nguyên. Với
độ phân giải đó, một đêm nhiệt độ đổi 0,4 °C vẫn ra một chuỗi giá trị lặp. Đặt ngưỡng theo độ phân giải: 36 bước (18 giờ) chỉ còn 2 đoạn /
123 điểm, trong đó đoạn dài nhất là 67 bước = 33,5 giờ ở 26,0 °C — đoạn này mới thật sự đáng ngờ.

</details>

---

**7 (vận dụng).** Bạn điền toàn bộ chuỗi bằng `interpolate(limit_direction="both")` rồi chia train/test và được kết quả rất tốt. Sai ở đâu,
và bài kiểm nào bắt được?

<details><summary>Đáp án</summary>

Hai lỗi: (a) nội suy hai phía **dùng tương lai**, (b) điền **trước** khi chia tập nên thông tin từ test rò sang train. Bài kiểm: cắt dữ
liệu tại một mốc và so đầu ra ở phần trước mốc đó (`tv.ro_ri.kiem_ro_ri`). Lưu ý: **mốc cắt phải nằm trong một lỗ hổng**, nếu cắt ở chỗ
dữ liệu đầy đủ thì bài kiểm không phát hiện được gì. Thứ tự đúng: chia tập → điền bằng phương pháp nhân quả (ffill, mùa vụ ngày trước).

</details>

---

**8 (vận dụng).** Cửa hàng hết hàng ba ngày, doanh số ghi nhận là 0. Bạn xử lý thế nào và vì sao?

<details><summary>Đáp án</summary>

Đánh dấu ba ngày đó là **thiếu**, không phải bằng 0 (censored demand: nhu cầu thật cao hơn doanh số). Nếu để 0, mô hình học rằng nhu cầu
thấp → dự báo thấp → đặt hàng ít → lại hết hàng: vòng lặp tự củng cố. Cần cột trạng thái tồn kho để nhận ra những ngày này; nếu không có,
ít nhất phải đánh cờ `nghi_ngo` cho các ngày doanh số 0 bất thường.

</details>

---

**9 (đọc bảng).** Bảng MAE (°C) của 7 cách điền trên cùng một chuỗi:

| Cách điền | Che điểm 10% | Che khối 48 giờ |
|---|---|---|
| tuyến tính | 0,291 | 2,171 |
| Kalman smoother | 0,308 | 1,256 |
| ffill | 0,378 | 2,052 |
| spline | 0,857 | 3,636 |
| hàng xóm (Open-Meteo) | 0,922 | 1,006 |
| mùa vụ (ngày trước) | 1,845 | 1,965 |
| trung bình theo giờ | 4,350 | 2,839 |

(a) Chọn phương pháp cho một chuỗi mà 67% lỗ dài 1 bước nhưng thỉnh thoảng có lỗ 8 giờ. (b) Giải thích vì sao spline tệ nhất ở cột phải.
(c) Vì sao "trung bình theo giờ" lại **tốt lên** khi lỗ dài hơn?

<details><summary>Đáp án</summary>

(a) Dùng **quy tắc theo độ dài lỗ**: lỗ ≤ vài bước → nội suy tuyến tính (hoặc ffill nếu cần nhân quả); lỗ dài → trạm hàng xóm (1,006) hoặc
để trống. Một phương pháp duy nhất cho mọi lỗ là lựa chọn tệ ở một trong hai đầu.

(b) Spline bậc 3 khớp đa thức qua hai mép lỗ; lỗ càng dài thì đa thức càng **vọt lố** ra ngoài dải giá trị thật (3,636 — tệ hơn cả ffill).

(c) Vì nó là **khí hậu học**: giá trị trung bình theo giờ trong ngày. Với lỗ 1 bước, hàng xóm gần nhất về thời gian tốt hơn nhiều nên nó
thua đậm (4,350); với lỗ 48 giờ thì mọi thông tin cục bộ đều mất, và một giá trị "hợp lý theo giờ" lại đỡ tệ hơn đường phẳng (2,839 so với
ffill 2,052 — vẫn thua ffill, nhưng thắng spline).

</details>

---

**10 (đọc biểu đồ — tìm chỗ sai).** Một báo cáo nội bộ về dữ liệu PM2.5 Bắc Kinh:

| Kết luận | Bằng chứng |
|---|---|
| (a) "Dữ liệu chỉ thiếu 2,08%, chất lượng rất tốt, dùng được toàn bộ." | tỷ lệ thiếu tổng |
| (b) "Trạm mất dữ liệu khi ô nhiễm cao, nên đây là MNAR." | trực giác về cảm biến |
| (c) "Chúng tôi điền toàn bộ bằng trung bình cột để không còn NaN." | pipeline |
| (d) "Cột `precipitation` của trạm Nội Bài toàn 0, nghĩa là cả năm không mưa." | dữ liệu |

Chỉ ra chỗ sai của từng dòng.

<details><summary>Đáp án</summary>

- **(a)** Trung bình che mất cấu trúc: thiếu đi thành **mảng**, có 13 ô (trạm × tháng) thiếu > 10% và ô tệ nhất **48,0%**. Phải xem heatmap
  theo trạm × thời gian, và loại giai đoạn không dùng được thay vì lấy trung bình an ủi.
- **(b)** Đó là **giả định**, không phải bằng chứng. Đo thử: khi Dongsi thiếu, PM2.5 của các trạm còn lại là 76,8 so với 79,2 khi có
  (**−3,0%**); ba trạm thử đều âm (−3,0% đến −14,1%). Không có bằng chứng MNAR ở bộ này.
- **(c)** Điền bằng trung bình cột xoá cả nhịp ngày lẫn mùa, và **không** đánh dấu ô nào đã điền. Sai số sau đó sẽ đẹp giả tạo. Đúng: điền
  lỗ ngắn bằng phương pháp nhân quả, để lỗ dài là NaN, và xuất cờ `da_dien`.
- **(d)** Không: cột đó **rỗng 100%** (NaN), không phải bằng 0 — 30/64 cột đo của tệp này rỗng hoàn toàn. Kiểm bằng `isna().all()` trước
  khi diễn giải bất kỳ cột nào.

</details>
