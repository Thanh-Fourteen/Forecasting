# Kiểm tra buổi 3 — Dữ liệu thời gian với pandas, polars, DuckDB

## Nhắc lại khái niệm

**Câu 1.** Giá trị `2024-11-03 01:30` (không kèm múi giờ) của một cảm biến ở New York tương ứng với bao nhiêu thời điểm UTC?

- A. Một — 06:30 UTC
- B. Hai — 05:30 UTC và 06:30 UTC
- C. Không có — giờ này không tồn tại
- D. Một — 01:30 UTC, vì giá trị không có múi giờ được hiểu là UTC

<details>
<summary>Đáp án</summary>

**B.** Ngày 3/11/2024 đồng hồ New York lùi từ 01:59 EDT về 01:00 EST, nên 01:30 xảy ra hai lần: 01:30 EDT (UTC−4) = 05:30Z và
01:30 EST (UTC−5) = 06:30Z. C là tình huống của 02:30 ngày 10/3. D sai vì giá trị naive không mặc định là UTC — nó chỉ là con
số, người dùng phải nói múi giờ. A là thứ DuckDB `timezone()` chọn một cách im lặng.

</details>

**Câu 2.** Với dữ liệu **số chuyến taxi** (sự kiện) và dữ liệu **nhiệt độ** (trạng thái), gộp từ phút lên giờ thì:

- A. cả hai lấy trung bình
- B. số chuyến cộng, nhiệt độ lấy trung bình hoặc giá trị cuối
- C. cả hai cộng
- D. số chuyến lấy trung bình, nhiệt độ cộng

<details>
<summary>Đáp án</summary>

**B.** Lưu lượng (số chuyến, kWh) cộng lại mới ra tổng trong giờ. Nhiệt độ là trạng thái — cộng 60 lần đo nhiệt độ không mang
ý nghĩa vật lý. A đổi "số chuyến mỗi giờ" thành "số chuyến trung bình mỗi phút" mà không ai biết.

</details>

**Câu 3.** Sau `resample("h")`, một giờ không có sự kiện nào. Phát biểu nào đúng?

- A. Luôn điền 0
- B. Luôn điền NaN
- C. Đếm sự kiện thì 0 là đúng; số đo trạng thái thì phải là NaN; giờ mà dữ liệu có nhưng không xác định được thì NaN
- D. Điền giá trị giờ trước (`ffill`) cho mọi loại dữ liệu

<details>
<summary>Đáp án</summary>

**C.** "Không có chuyến" (0) khác "không đo" (NaN) và khác "không biết thuộc giờ nào" (NaN — giờ lặp DST). `ffill` giả định
giá trị không đổi — chỉ hợp lý với một số biến trạng thái và phải là quyết định có chủ đích (buổi 10).

</details>

**Câu 4.** `pd.merge_asof(trai, phai, on="t")` với mặc định `direction="backward"` lấy dòng nào của `phai`?

- A. Dòng gần nhất theo khoảng cách tuyệt đối
- B. Dòng cuối cùng có `t` nhỏ hơn hoặc bằng `t` của `trai`
- C. Dòng đầu tiên có `t` lớn hơn hoặc bằng `t` của `trai`
- D. Dòng có `t` bằng đúng, nếu không có thì NaN

<details>
<summary>Đáp án</summary>

**B.** Backward = giá trị gần nhất trong **quá khứ** (kể cả đúng lúc, trừ khi `allow_exact_matches=False`). C là `forward` —
kéo giá trị tương lai về, gây rò rỉ. A là `nearest`, cũng có thể lấy tương lai. D là `merge` thường.

</details>

## Vận dụng

**Câu 5.** Chuỗi đo trong tháng 3/2024 theo giờ UTC, từ 00:00 ngày 1/3 giờ New York (05:00Z) tới trước 00:00 ngày 1/4 giờ New
York (04:00Z). Lưới đủ mốc có bao nhiêu giờ?

<details>
<summary>Đáp án</summary>

**743.** Tháng 3 có 31 × 24 = 744 giờ đồng hồ, nhưng ngày 10/3 mất một giờ (01:59 → 03:00). Theo UTC: từ 05:00Z ngày 1/3 tới
04:00Z ngày 1/4 là 743 giờ. Chính bộ chấm của buổi kiểm con số này trên dữ liệu thật.

</details>

**Câu 6.** Một đồng nghiệp gộp tệp taxi tháng 3 bằng `groupby(dt.floor("h"))` và báo "747 giờ trong tháng 3". Viết hai câu giải
thích và sửa.

<details>
<summary>Đáp án</summary>

Tệp có 23 chuyến đón ngoài tháng 3 (sớm nhất `2002-12-31 22:17:10`, có chuyến tháng 2 và tháng 4) — mỗi giờ lạ tạo một nhóm.
Sửa: lọc theo khoảng tháng của tệp trước khi gộp (và vẫn còn vấn đề giờ 02:00 ảo — xem câu 1).

</details>

**Câu 7.** Bạn ghép số chuyến theo giờ (giờ địa phương New York, naive) với thời tiết Open-Meteo (tải `timezone=UTC`, cột `time`
naive) bằng `merge(on="ds")`. Tháng 3–11/2024 hai bảng lệch nhau mấy giờ, theo hướng nào? Một phép thử nhanh để phát hiện?

<details>
<summary>Đáp án</summary>

**Lệch 4 giờ** (EDT = UTC−4): dòng taxi "15:00" (giờ New York) được ghép với thời tiết 15:00Z = 11:00 New York — thời tiết
bị gắn **sớm hơn** 4 giờ so với thực tế của dòng đó. Phép thử: giờ nóng nhất trung bình theo "giờ" của bảng ghép — ra 20h
(vô lý) thay vì 16h. Mùa đông (EST) lệch 5 giờ.

</details>

**Câu 8.** Chọn công cụ và cách làm cho việc: đếm số chuyến theo giờ UTC cho 12 tệp Parquet cả năm (~720 MB), máy 16 GB RAM,
cần kết quả trong vài giây. Nêu một rủi ro về múi giờ riêng của công cụ bạn chọn.

<details>
<summary>Đáp án</summary>

Hợp lý: polars `scan_parquet` (lazy, chỉ đọc cột cần) hoặc DuckDB SQL thẳng trên các tệp — không nạp mọi cột vào pandas. Rủi
ro: polars `replace_time_zone` báo lỗi ở giờ lặp/không tồn tại nếu không khai `ambiguous`/`non_existent`; DuckDB `timezone()`
**im lặng** dời giờ không tồn tại tới giờ hợp lệ kế tiếp và chọn EST cho giờ lặp, còn `TimeZone` mặc định lấy theo máy.
Trên máy soạn khoá, tệp tháng 3: polars lazy 0,026 s, DuckDB 0,045 s, pandas chỉ đọc cột cần 0,074 s (4 nhân).

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Bảng số chuyến theo giờ của một báo cáo:

| giờ | 2024-03-10 00:00 | 01:00 | 02:00 | 03:00 | 04:00 |
|---|---|---|---|---|---|
| số chuyến | 6.369 | 5.302 | 0 | 4.559 | 2.764 |

Báo cáo kết luận "sự cố hệ thống đặt xe lúc 2 giờ sáng Chủ nhật 10/3". Kết luận này sai ở đâu?

<details>
<summary>Đáp án</summary>

Không có sự cố: 02:00–02:59 ngày 10/3/2024 **không tồn tại** ở New York (đồng hồ nhảy 01:59 → 03:00). Ô 0 do `resample` trên
giờ địa phương naive tạo ra. Dấu hiệu kiểm: ngày đổi giờ mùa hè (Chủ nhật thứ hai của tháng 3 ở Mỹ); chuyển sang UTC thì dãy
giờ liền nhau không có ô 0.

</details>

**Câu 10.** Hai kết quả của cùng một phân tích "mưa ảnh hưởng số chuyến taxi" (tương quan mưa – số chuyến cùng giờ, đã khử
mùa vụ giờ trong tuần, tháng 3/2024):

| Cách ghép | Tương quan | Giờ nóng nhất trung bình (theo cột giờ của bảng) |
|---|---|---|
| Bản A | −0,100 | 20h |
| Bản B | +0,136 | 16h |

Bản nào đáng tin, vì sao, và bản kia sai ở bước nào?

<details>
<summary>Đáp án</summary>

**Bản B.** Bản A cho New York nóng nhất lúc 20h — không phù hợp nhịp nhiệt độ ngày, dấu hiệu thời tiết bị ghép lệch 4 giờ
(giờ địa phương naive của taxi ghép với giờ UTC của thời tiết). Khi lệch, mưa bị gắn vào giờ khác nên tương quan đổi dấu.
Sửa ở bước ghép: đưa cả hai bảng về UTC có múi giờ rồi mới `merge`. (Tương quan dương cũng chưa chứng minh nhân quả — buổi 8.)

</details>
