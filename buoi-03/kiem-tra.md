# Kiểm tra buổi 3 — Dữ liệu thời gian với pandas, polars, DuckDB

## Nhắc lại khái niệm

**Câu 1.** Giá trị `2024-11-03 01:30` (không kèm múi giờ) của một cảm biến ở New York tương ứng với bao nhiêu thời điểm UTC?

- A. Một — 06:30 UTC
- B. Hai — 05:30 UTC và 06:30 UTC
- C. Không có — giờ này không tồn tại
- D. Một — 01:30 UTC, vì giá trị không có múi giờ được hiểu là UTC

<details>
<summary>Đáp án</summary>

**B.** Ngày 3/11/2024 đồng hồ lùi từ 02:00 EDT về 01:00 EST, nên 01:30 xảy ra hai lần: EDT 01:30 + 4 = 05:30Z, rồi
EST 01:30 + 5 = 06:30Z.

- **A sai**: 06:30Z chỉ là một trong hai đáp án (thứ DuckDB tự chọn mà không báo).
- **C sai**: "không tồn tại" là 02:30 ngày 10/3/2024.
- **D sai**: giá trị naive không mặc định là UTC; người dùng phải nói nó thuộc múi giờ nào.

</details>

**Câu 2.** Với dữ liệu **số chuyến taxi** (sự kiện) và dữ liệu **nhiệt độ** (trạng thái), gộp từ phút lên giờ thì:

- A. cả hai lấy trung bình
- B. số chuyến cộng, nhiệt độ lấy trung bình hoặc giá trị cuối
- C. cả hai cộng
- D. số chuyến lấy trung bình, nhiệt độ cộng

<details>
<summary>Đáp án</summary>

**B.** Số chuyến là số lượng: cộng mới ra tổng trong giờ. Nhiệt độ là trạng thái: đại diện bằng trung bình hoặc lần đo cuối.

- **A sai** ở số chuyến: trung bình ra "số chuyến mỗi phút", đổi đơn vị mà không ai hay.
- **C sai** ở nhiệt độ: cộng 60 lần đo 25 °C ra 1.500, vô nghĩa.
- **D sai** cả hai chỗ, là đảo ngược của B.

</details>

**Câu 3.** Sau `resample("h")`, một giờ không có sự kiện nào. Phát biểu nào đúng?

- A. Luôn điền 0
- B. Luôn điền NaN
- C. Đếm sự kiện thì 0 là đúng; số đo trạng thái thì phải là NaN; giờ mà dữ liệu có nhưng không xác định được thì NaN
- D. Điền giá trị giờ trước (`ffill`) cho mọi loại dữ liệu

<details>
<summary>Đáp án</summary>

**C.** "Không có chuyến" là 0 thật. "Không đo nhiệt độ" và "có chuyến nhưng không biết thuộc giờ UTC nào" (giờ lặp
3/11/2024) là không biết, nên NaN.

- **A sai**: 0 cho nhiệt độ là bịa ra "0 độ"; 0 cho giờ lặp là bịa ra một giờ vắng khách.
- **B sai**: đếm sự kiện mà giờ không có chuyến thì đúng là 0, không phải "không biết".
- **D sai**: `ffill` (điền tiếp giá trị trước) giả định giá trị không đổi; với số chuyến, đó là bịa ra chuyến.

</details>

**Câu 4.** `pd.merge_asof(trai, phai, on="t")` với mặc định `direction="backward"` lấy dòng nào của `phai`?

- A. Dòng gần nhất theo khoảng cách tuyệt đối
- B. Dòng cuối cùng có `t` nhỏ hơn hoặc bằng `t` của `trai`
- C. Dòng đầu tiên có `t` lớn hơn hoặc bằng `t` của `trai`
- D. Dòng có `t` bằng đúng, nếu không có thì NaN

<details>
<summary>Đáp án</summary>

**B.** `backward` nhìn về **quá khứ**: lấy giá trị gần nhất đã có, kể cả đúng lúc (trừ khi `allow_exact_matches=False`).

- **A sai**: đó là `direction="nearest"`, có thể lấy giá trị tương lai.
- **C sai**: đó là `direction="forward"`, kéo tương lai về, gây rò rỉ.
- **D sai**: đó là `merge` thường, chỉ ghép khi thời điểm bằng nhau.

</details>

## Vận dụng

**Câu 5.** Chuỗi đo trong tháng 3/2024 theo giờ UTC, từ 00:00 ngày 1/3 giờ New York (05:00Z) tới trước 00:00 ngày 1/4 giờ New
York (04:00Z). Lưới đủ mốc có bao nhiêu giờ?

<details>
<summary>Đáp án</summary>

**743.** 31 × 24 = 744 giờ, nhưng ngày 10/3/2024 chỉ có 23 giờ, nên còn 743. Lưới [05:00Z, 04:00Z) có mốc đầu, không có
mốc cuối, nên đúng 743 mốc.

Nhầm hay gặp: trả lời 744 vì quên ngày đổi giờ, hoặc vì tính cả mốc cuối 04:00Z ngày 1/4 (thuộc tháng 4).

</details>

**Câu 6.** Một đồng nghiệp gộp tệp taxi tháng 3 bằng `groupby(dt.floor("h"))` và báo "747 giờ trong tháng 3". Viết hai câu giải
thích và sửa.

<details>
<summary>Đáp án</summary>

Tệp có 23 chuyến đón ngoài tháng 3, rơi vào 4 giờ lạ. Phần trong tháng có 743 nhóm (giờ 02:xx ngày 10/3 không có dòng),
nên 743 + 4 = 747. Nhầm hay gặp: lấy 747 − 744 = 3 giờ lạ. Sửa: lọc theo khoảng tháng trước khi gộp, và vẫn đổi sang UTC
trước khi gộp (câu 1, câu 9).

</details>

**Câu 7.** Bạn ghép số chuyến theo giờ (giờ địa phương New York, naive) với thời tiết Open-Meteo (tải `timezone=UTC`, cột `time`
naive) bằng `merge(on="ds")`. Từ 10/3/2024 đến 3/11/2024, hai bảng lệch nhau mấy giờ, theo hướng nào? Nêu một phép thử
nhanh để phát hiện.

<details>
<summary>Đáp án</summary>

**Lệch 4 giờ**, vì trong khoảng đó New York là EDT (UTC−4). Dòng taxi "15:00" ghép với thời tiết 15:00Z, tức 11:00 giờ
New York: mỗi dòng taxi nhận thời tiết **sớm hơn** 4 giờ. Ngoài khoảng đó (EST) thì lệch 5 giờ.

Phép thử: giờ nóng nhất trung bình theo cột giờ của bảng ghép. Ghép lệch ra 20h (vô lý), ghép đúng ra 16h.

</details>

**Câu 8.** Chọn công cụ và cách làm cho việc: đếm số chuyến theo giờ UTC cho 12 tệp Parquet cả năm (~720 MB), máy 16 GB RAM,
cần kết quả trong vài giây. Nêu một rủi ro về múi giờ riêng của công cụ bạn chọn.

<details>
<summary>Đáp án</summary>

Hợp lý: polars `scan_parquet` (lazy, chỉ đọc cột cần) hoặc DuckDB SQL thẳng trên các tệp; không nạp mọi cột vào pandas.
Rủi ro:

- polars: `replace_time_zone` báo lỗi ở giờ lặp hay giờ không tồn tại nếu không khai `ambiguous` / `non_existent`.
- DuckDB: `timezone()` **im lặng** dời giờ không tồn tại và chọn EST cho giờ lặp; `TimeZone` mặc định theo máy, nên phải
  `SET TimeZone = 'UTC'`.

Tham khảo (máy soạn khoá, tệp tháng 3, 4 nhân): polars lazy 0,026 giây, DuckDB 0,045 giây.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Bảng số chuyến theo giờ của một báo cáo:

| giờ | 2024-03-10 00:00 | 01:00 | 02:00 | 03:00 | 04:00 |
|---|---|---|---|---|---|
| số chuyến | 6.369 | 5.302 | 0 | 4.559 | 2.764 |

Báo cáo kết luận "sự cố hệ thống đặt xe lúc 2 giờ sáng Chủ nhật 10/3". Kết luận này sai ở đâu?

<details>
<summary>Đáp án</summary>

Không có sự cố. Ở New York, giờ 02:xx ngày 10/3/2024 **không tồn tại** (ngày đổi giờ mùa hè). Ô 0 do `resample` trên
giờ naive tạo ra: pandas dựng đủ lưới giờ đồng hồ, kể cả giờ không có thật, rồi điền 0. Đổi sang UTC thì dãy giờ liền
nhau và không có ô 0.

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

**Bản B.** Bản A cho New York nóng nhất lúc 20h, trái với nhịp ngày: dấu hiệu giờ naive của taxi bị ghép với giờ UTC
của thời tiết, lệch khoảng 4 giờ. Mưa bị gắn vào giờ khác với giờ nó rơi, nên tương quan đổi dấu. Sửa: đưa cả hai bảng
về UTC có múi giờ rồi mới `merge`. Tương quan dương của bản B cũng chưa chứng minh mưa **gây ra** tăng khách.

</details>
