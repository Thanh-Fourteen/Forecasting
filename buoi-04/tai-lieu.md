# Buổi 4 — Đọc và vẽ biểu đồ chuỗi thời gian

## 1. Mục tiêu

Sau buổi này bạn:

- Đọc mọi biểu đồ theo **năm bước**: trục ngang, trục dọc, ký hiệu, chỗ cần nhìn, câu kết luận.
- Chỉ ra **xu hướng, mùa vụ, chu kỳ** trên một hình, mỗi thứ kèm một bằng chứng cụ thể (chỗ nào, con số nào).
- Tự viết **bộ 8 biểu đồ chẩn đoán** cho một chuỗi theo giờ và dùng nó thấy **mùa vụ kép** (ngày lồng trong tuần) mà
  biểu đồ đường thô che mất.
- Nhận ra hai kiểu hình gây hiểu nhầm, **trục kép** và **trục y cắt**, rồi vẽ lại cho trung thực.
- Viết tiêu đề hình là **một câu kết luận**, không phải tên biến.

## 2. Nhắc lại buổi trước

Từ buổi 3 (dữ liệu thời gian):

- **Lưới thời gian đầy đủ.** Trước khi vẽ, dựng đủ mọi mốc giờ rồi `reindex`: giờ không có số liệu thành **NaN** ("không
  biết"), không phải 0 ("đo được, bằng không").
- **Gộp tần suất.** Số đếm (lượt thuê) gộp bằng **tổng**, số đo trạng thái (nhiệt độ) gộp bằng **trung bình**.
  `resample("D").sum(min_count=12)` để trống ngày có dưới 12 giờ số liệu, thay vì cộng ra một tổng thấp giả.
- **Thứ trong tuần.** `DatetimeIndex.dayofweek` đánh 0 = thứ Hai … 6 = Chủ nhật. Tài liệu này viết T2 … T7 cho thứ Hai …
  thứ Bảy, CN cho Chủ nhật.

Từ buổi 2 (xác suất và thống kê):

- **Trung vị** là số đứng giữa khi xếp tăng dần. **Quantile** mức 0,25 là giá trị nhỏ nhất mà ít nhất 25% số liệu nhỏ
  hơn hoặc bằng nó. Ví dụ dãy 60, 410, 420, 440, 450 → trung vị = 420, quantile 0,25 = 410.
- **Hệ số tương quan $r$** đo hai đại lượng cùng tăng cùng giảm theo đường thẳng tới đâu: gần 1 là cùng chiều, gần −1 là
  ngược chiều, gần 0 là không có quan hệ đường thẳng.
- **Tự tương quan** ở độ trễ $k$: tương quan của chuỗi với chính nó dời lùi $k$ bước. Lượt thuê giờ này và giờ trước có
  $r = 0{,}84$: dữ liệu theo thời gian không phải các lần đo độc lập.

## 3. Trạng thái đầu buổi

Sau `python lab.py up` (trong thư mục `lab/`):

| Hạng mục | Trạng thái |
|---|---|
| Dữ liệu | `du-lieu/raw/uci-bike-sharing/hour.csv` — 17.379 dòng, 01/01/2011 00:00 → 31/12/2012 23:00, sha256 `e03de4ee4ef4` |
| | Lưới giờ đầy đủ có 17.544 giờ, nên 165 giờ thiếu, rải trên 76 ngày |
| Nguồn | Capital Bikeshare (Washington D.C.), qua Fanaee-T & Gama, UCI Machine Learning Repository, CC BY 4.0 |
| Môi trường | Python 3.12; numpy 2.5.3, pandas 3.0.5, matplotlib 3.11.2, statsmodels 0.15.0 |
| `code/bieu_do.py` | `doc_luot_thue`, `ho_so_tuan`, `acf_nhanh`, `cap_tre`, `bo_bieu_do_chan_doan`, `bieu_do_gay_hieu_nham`, `ve_lai_trung_thuc` |
| `code/lab.ipynb` | notebook của Lab, bước 1–5 |
| **Đang cố tình sai** | bộ chẩn đoán chỉ có 2 hình: đường thô 17.544 giờ và trục kép lượt thuê – nhiệt độ có trục y cắt; `ho_so_tuan` cho 7 dòng **giống hệt nhau**; `ve_lai_trung_thuc` trả lại chính hình gây hiểu nhầm |
| **Triệu chứng** | nhìn bộ biểu đồ không thấy thứ Bảy khác thứ Hai; trục kép "chứng minh" lượt thuê bám sát nhiệt độ |
| `python lab.py check` lúc này | ĐỎ: 7/8 test hỏng |

## 4. Lý thuyết

Dữ liệu cả buổi: số **lượt thuê** xe đạp công cộng mỗi giờ ở Washington D.C., 2011–2012 (cột `cnt`).

### Từ mới trong buổi

| Thuật ngữ | Nghĩa một câu | Ví dụ |
|---|---|---|
| T2 … T7, CN | Thứ Hai … thứ Bảy, Chủ nhật. | T2 8h = 8 giờ sáng thứ Hai. |
| xu hướng (trend) | Mức chung đi lên hoặc đi xuống trong thời gian dài; không cần là đường thẳng. | Lượt thuê 2012 cao hơn 2011 ở mọi tháng. |
| mùa vụ (seasonality) | Mẫu hình lặp lại sau một **số bước cố định, biết trước**, gắn với lịch. | Ngày làm việc nào cũng đông lúc 8h và 17h. |
| chu kỳ mùa vụ, $m$ | Số bước trước khi mẫu mùa vụ lặp lại. | Dữ liệu giờ lặp theo ngày: $m$ = 24; theo tuần: $m$ = 168. |
| chu kỳ (cycle) | Lên xuống kéo dài, thường vài năm, độ dài **không cố định**, không biết trước. | Kinh tế tăng 6 năm rồi suy thoái; lần sau tăng 9 năm. |
| mùa vụ kép (multiple seasonality) | Chuỗi có hai mùa vụ trở lên cùng lúc. | Lượt thuê: nhịp ngày (24 giờ) lồng trong nhịp tuần (168 giờ). |
| gộp tần suất | Cộng (hoặc lấy trung bình) nhiều mốc nhỏ thành một mốc lớn hơn. | 24 giờ → 1 ngày. |
| làm trơn (smoothing), trung bình trượt (moving average) | Thay mỗi điểm bằng trung bình của nó với các điểm lân cận, cho đường mượt hơn. | 50, 2, 51 → trung bình 3 điểm quanh 2 là 34,3. |
| thang log | Trục dọc mà khoảng cách bằng nhau nghĩa là **nhân** cùng một số. | 100 → 200 và 200 → 400 cao bằng nhau. |
| seasonal plot | Mỗi chu kỳ (mỗi tuần) vẽ một đường, chồng lên nhau trên cùng trục "vị trí trong chu kỳ". | 106 tuần, mỗi tuần một đường từ T2 0h tới CN 23h. |
| subseries plot | Mỗi "mùa" (mỗi tháng, mỗi thứ) một ô nhỏ chứa các giá trị của riêng mùa đó qua thời gian. | Ô "tháng 3": tháng 3/2011 rồi tháng 3/2012. |
| heatmap | Bảng số tô màu: ô càng sáng giá trị càng lớn. | 7 dòng thứ × 24 cột giờ. |
| boxplot (biểu đồ hộp) | Hộp từ quantile 0,25 tới 0,75, vạch giữa là trung vị. | Hộp 410–440, vạch 420. |
| IQR (khoảng tứ phân vị) | Độ dài của hộp: quantile 0,75 trừ quantile 0,25. | 440 − 410 = 30. |
| scatter (biểu đồ phân tán) | Mỗi điểm là một cặp (x, y); nhìn hình dạng đám điểm để thấy quan hệ. | x = nhiệt độ ngày, y = lượt thuê ngày. |
| lag plot (biểu đồ trễ) | Scatter của $y_t$ theo $y_{t-k}$. | $k$ = 24: lượt lúc 8h hôm nay theo lượt lúc 8h hôm qua. |
| ACF | Hàm tự tương quan: dãy $r_1, r_2, r_3, \dots$ vẽ theo độ trễ $k$. | $r_{24}$ = 0,81; $r_{168}$ = 0,86. |
| trục kép | Một hình có hai trục dọc với hai thang khác nhau, trái và phải. | Trái: lượt thuê; phải: °C. |
| trục y cắt | Trục dọc không bắt đầu từ 0 mà từ một giá trị gần dữ liệu. | Doanh thu vẽ từ 480 đến 520. |

### 4.1 Đọc một hình: năm bước, ba mẫu hình

**Vấn đề.** Một hình có thể có hàng nghìn điểm. Người đọc vội nhìn đường rồi kết luận ngay, bỏ qua đơn vị, bỏ qua trục
bắt đầu ở đâu. Cần một thứ tự đọc cố định, và cần biết mình đang tìm ba thứ gì.

**Năm bước đọc mọi hình.** Mọi hình trong khoá đều kèm khối "Cách đọc hình" theo đúng thứ tự này:

1. **Trục ngang** là gì, đơn vị gì.
2. **Trục dọc** là gì, đơn vị gì, bắt đầu từ đâu.
3. **Ký hiệu**: mỗi màu, đường, chấm, vạch là gì.
4. **Nhìn vào đâu**: chỉ đúng một vùng trên hình.
5. **Kết luận**: một câu người khác kiểm được ngay trên hình, có chỗ và có số.

Câu ở bước 5 cũng là **tiêu đề** nên đặt cho hình. "cnt" hay "Lượt thuê theo giờ" chỉ là tên biến. "Giờ × thứ: 8h và
17h chỉ sáng vào ngày làm việc" là kết luận.

**Ba mẫu hình cần tìm** (theo FPP §2.3; FPP là sách *Forecasting: Principles and Practice*, xem Đọc thêm):

- **Xu hướng**: mức chung đi lên hay đi xuống lâu dài?
- **Mùa vụ**: có mẫu lặp lại sau một số bước **cố định** gắn với lịch (giờ trong ngày, thứ trong tuần, tháng trong năm)
  không? Một chuỗi có thể có nhiều mùa vụ cùng lúc.
- **Chu kỳ**: có lên xuống kéo dài mà độ dài **không cố định** không? Phép phân biệt: lặp sau đúng số bước biết trước là
  mùa vụ; độ dài mỗi lần một khác là chu kỳ. Hiểu lầm hay gặp: nghĩ "mùa" chỉ là xuân–hạ–thu–đông. "Mùa" ở đây là **bất kỳ**
  vòng lặp theo lịch nào: ngày, tuần, năm.

**Ví dụ số nhỏ — tự tính tay.** Lượt thuê hai tuần, đơn vị trăm lượt mỗi ngày:

| | T2 | T3 | T4 | T5 | T6 | T7 | CN | Trung bình tuần |
|---|---|---|---|---|---|---|---|---|
| Tuần 1 | 10 | 12 | 12 | 12 | 14 | 6 | 4 | 70 / 7 = 10 |
| Tuần 2 | 12 | 14 | 14 | 14 | 16 | 8 | 6 | 84 / 7 = 12 |

**Đọc bảng.** Tách ba mẫu hình từ bảng:

- **Xu hướng**: trung bình mỗi ngày đi 10 → 12 trăm lượt từ tuần đầu sang tuần sau.
- **Mùa vụ tuần**: lấy mỗi ngày trừ trung bình tuần của nó. Tuần 1: 10 − 10 = 0, 12 − 10 = 2, … ra 0, 2, 2, 2, 4, −4, −6.
  Tuần 2: 12 − 12 = 0, 14 − 12 = 2, … ra **đúng dãy đó**. Hình dạng lặp sau đúng 7 ngày: mùa vụ tuần, cuối tuần thấp.
- **Chu kỳ**: hai tuần quá ngắn để nói. Tương tự, dữ liệu thật chỉ có hai năm nên không đủ để nói về chu kỳ nhiều năm.

![Gộp theo giờ thì thành khối màu, theo tháng thì mất mùa vụ ngày, tuần và ngày bất thường](hinh/gop-tan-suat.png)

**Cách đọc hình.**

1. **Trục ngang** (cả ba ô): thời gian, 1/2011 → 12/2012.
2. **Trục dọc**: lượt thuê, bắt đầu từ 0; đơn vị lần lượt là lượt/giờ, lượt/ngày, lượt/tháng.
3. **Ký hiệu**: một đường xanh; ô trên có 17.544 điểm, ô giữa 731 điểm, ô dưới 24 điểm.
4. **Nhìn vào đâu**: ô giữa, những ngày rơi xuống sát 0; ô dưới, hai "cái bướu" hè 2011 và hè 2012.
5. **Kết luận**: có xu hướng (bướu 2012 cao hơn bướu 2011) và mùa vụ năm (hè cao, đông thấp). Mùa vụ ngày và tuần phải tìm
   bằng hình khác: ô trên là khối màu, ô dưới đã gộp mất chúng.

**Tóm lại.** **Đọc hình theo năm bước: trục ngang, trục dọc, ký hiệu, chỗ nhìn, kết luận. Tìm ba thứ: xu hướng (mức đổi
lâu dài), mùa vụ (lặp sau số bước cố định theo lịch), chu kỳ (lên xuống độ dài không cố định).**

**Tự kiểm tra.** Doanh số một cửa hàng tăng vọt mỗi dịp Tết, và có những đợt suy giảm kéo dài 2–4 năm theo kinh tế. Mỗi
mẫu hình là gì?

<details>
<summary>Đáp án</summary>

Tết lặp lại mỗi năm theo lịch âm, nên là **mùa vụ** (dù ngày dương lịch xê dịch, vị trí trong năm âm lịch là cố định).
Suy giảm 2–4 năm không có độ dài cố định, nên là **chu kỳ**. Nhầm hay gặp: gọi đợt suy giảm là xu hướng. Xu hướng là mức đổi
lâu dài một chiều, không lên rồi xuống lại.

</details>

### 4.2 Cùng dữ liệu, hình khác: gộp, làm trơn, thang log

**Vấn đề.** Ba cách "làm hình dễ nhìn" hay dùng nhất là gộp tần suất, làm trơn và đổi sang thang log. Cả ba đều **bỏ** hoặc
**phóng to** một phần thông tin. Cần biết mỗi cách giấu gì.

**Gộp tần suất.** Hình mục 4.1 đã cho thấy gộp càng thô càng mất chi tiết. Chọn mức gộp theo câu hỏi, và xem thêm ít nhất một
mức chi tiết hơn mức định báo cáo.

**Ví dụ số nhỏ — tự tính tay (làm trơn).** Bảy ngày lượt thuê (trăm lượt): 50, 52, 48, **2**, 51, 49, 50. Ngày thứ tư gần
như trống. **Trung bình trượt 3 ngày có tâm** thay ngày đó bằng trung bình của nó và hai ngày hai bên: (48 + 2 + 51) / 3 =
33,7. Cửa sổ 7 ngày (cả bảy ngày) cho 302 / 7 = 43,1. Điểm 2 (thấp hơn ngày thường khoảng 48) chỉ còn là một chỗ lõm xuống 34 hay 43:
cửa sổ càng rộng, ngày bất thường càng mờ.

![Làm trơn 7 ngày biến ngày bão gần như trống thành một chỗ lõm nhẹ](hinh/lam-tron.png)

**Cách đọc hình.**

1. **Trục ngang**: ngày, 15/9 → 30/11/2012.
2. **Trục dọc**: lượt thuê mỗi ngày, bắt đầu từ 0.
3. **Ký hiệu**: chấm xám nối nhau là tổng từng ngày; đường cam là trung bình trượt 7 ngày có tâm.
4. **Nhìn vào đâu**: mũi tên, ngày 29/10/2012 (bão Sandy), tệp chỉ còn 1 giờ với 22 lượt.
5. **Kết luận**: đường cam ở ngày đó là 4.632 lượt, chỉ lõm nhẹ; ai chỉ xem đường làm trơn sẽ không biết có một ngày dữ liệu
   gần như trống.

**Ví dụ số nhỏ — tự tính tay (thang log).** Trên thang log, trục dọc đặt mỗi điểm ở độ cao $\log_{10} y$ thay vì $y$.

| $y$ | 100 | 200 | 400 | 500 |
|---|---|---|---|---|
| Tăng so với điểm trước | | +100 | +200 | +100 |
| Gấp mấy lần điểm trước | | 2 | 2 | 1,25 |
| Độ cao trên thang log, $\log_{10} y$ | 2 | 2,301 | 2,602 | 2,699 |
| Bước cao thêm trên thang log | | 0,301 | 0,301 | 0,097 |

**Đọc bảng.** Trên thang thường, bước thứ hai cao gấp đôi bước đầu. Trên thang log, hai bước đầu cao bằng nhau vì cùng
**gấp đôi**. Vậy trên thang log, **hai đoạn dốc như nhau nghĩa là tăng cùng một phần trăm**.

![Thang thường nhấn tăng tuyệt đối, thang log nhấn tăng phần trăm](hinh/thang-log.png)

**Cách đọc hình.**

1. **Trục ngang** (cả hai ô): tháng năm 2011.
2. **Trục dọc**: lượt thuê mỗi tháng. Ô trái là thang thường, từ 0. Ô phải là thang log: 40.000 → 80.000 cao bằng 70.000 →
   140.000.
3. **Ký hiệu**: chấm là tổng một tháng, nối bằng đường.
4. **Nhìn vào đâu**: đoạn tháng 3 → 4 và đoạn tháng 4 → 5 ở cả hai ô.
5. **Kết luận**: thang thường cho thấy tháng 4 → 5 tăng nhiều lượt nhất (+40.951); thang log cho thấy tháng 3 → 4 tăng nhanh
   nhất theo phần trăm (+48,1%, còn tháng 4 → 5 là +43,2%).

Dùng thang log khi quan tâm tốc độ tăng theo phần trăm (giá, tăng trưởng). Dùng thang thường khi quan tâm con số tuyệt đối
(cần thêm bao nhiêu xe).

**Tóm lại.** **Gộp và làm trơn làm hình mượt bằng cách xoá chi tiết, kể cả ngày bất thường; vẽ đường trơn đè lên dữ liệu gốc,
không thay nó. Trên thang log, cùng độ dốc là cùng phần trăm thay đổi.**

**Tự kiểm tra.** Doanh thu ba quý: 20, 40, 60 tỷ. Trên thang log, đoạn nào dốc hơn?

<details>
<summary>Đáp án</summary>

Đoạn đầu: 20 → 40 là gấp 2 (+100%). Đoạn sau: 40 → 60 là gấp 1,5 (+50%). Trên thang log đoạn đầu dốc hơn, dù trên thang
thường hai đoạn cao bằng nhau (+20 tỷ mỗi đoạn). Nhầm hay gặp: nghĩ "tăng cùng 20 tỷ thì dốc như nhau" ở cả hai thang.

</details>

### 4.3 Seasonal plot và subseries plot: xếp dữ liệu theo lịch

**Vấn đề.** Biểu đồ đường vẽ dữ liệu theo **thời gian trôi**. Muốn thấy mùa vụ, cần vẽ theo **vị trí trong vòng lặp**: thứ
mấy, giờ mấy, tháng mấy. Hai cách xếp lại, trả lời hai câu hỏi khác nhau.

**Trực giác.** Seasonal plot giống chồng các tờ lịch tuần lên nhau để soi: tuần nào lệch khỏi khuôn chung. Subseries plot
giống xếp riêng tất cả các thứ Hai vào một ngăn, tất cả thứ Ba vào ngăn khác: mỗi ngăn thay đổi ra sao qua thời gian.

**Ví dụ số nhỏ — tự tính tay.** Dùng lại hai tuần ở mục 4.1.

- **Seasonal plot**: trục ngang là T2 … CN. Tuần 1 là một đường 10, 12, 12, 12, 14, 6, 4; tuần 2 là đường thứ hai 12, 14,
  …, 6. Ở mỗi thứ, đường tuần 2 cao hơn: 12 − 10 = 2, 14 − 12 = 2, … Hai đường **song song**: cùng hình dạng tuần, mức tăng.
- **Subseries plot**: 7 ô nhỏ. Ô T2 chứa hai điểm 10 rồi 12, vạch ngang ở trung bình (10 + 12) / 2 = 11. Vạch ngang của 7
  ô là 11, 13, 13, 13, 15, 7, 5: chính là **hình dạng mùa vụ tuần**. Trong mỗi ô, điểm sau cao hơn điểm trước: **xu hướng**.

Với dữ liệu giờ, "vị trí trong tuần" là **giờ trong tuần**, từ 0 (T2 0h) tới 167 (CN 23h): giờ trong tuần = thứ × 24 + giờ.
Ví dụ T3 8h là 1 × 24 + 8 = 32.

![Seasonal plot theo tuần: T2–T6 hai đỉnh, T7–CN một đỉnh](hinh/mua-vu-tuan.png)

**Cách đọc hình.**

1. **Trục ngang**: giờ trong tuần, 0 → 167; mỗi vạch là 0h của một thứ.
2. **Trục dọc**: lượt thuê mỗi giờ, từ 0.
3. **Ký hiệu**: mỗi đường xám mảnh là một tuần (106 tuần); đường cam là trung vị của mọi tuần ở từng giờ.
4. **Nhìn vào đâu**: so năm ô T2–T6 với hai ô T7, CN.
5. **Kết luận**: ngày làm việc có **hai đỉnh** nhọn (sáng và chiều), cuối tuần có **một bướu** tròn giữa ngày; mùa vụ ngày
   đổi hình dạng theo thứ, tức là mùa vụ kép.

Đường xám tản rộng theo chiều dọc vì mức chung đổi theo mùa trong năm. Hiểu lầm hay gặp: "cuối tuần vắng hơn hẳn". Trên
655 ngày đủ 24 giờ, tổng ngày trung bình chỉ chênh vài phần trăm:

| Thứ | T2 | T3 | T4 | T5 | T6 | T7 | CN |
|---|---|---|---|---|---|---|---|
| Lượt/ngày (trung bình) | 4.708 | 4.909 | 4.909 | 4.899 | 4.933 | 4.653 | 4.523 |

**Đọc bảng.** T7, CN thấp hơn T2 chưa tới 4%; cả thứ cao nhất (T6) với thấp nhất (CN) chỉ chênh 8%. Ngày làm việc và cuối tuần khác nhau chủ yếu ở **hình dạng** trong ngày,
không ở tổng.

![Subseries theo tháng: tháng nào cũng nhảy bậc từ 2011 sang 2012](hinh/chuoi-con-thang.png)

**Cách đọc hình.**

1. **Trục ngang**: 12 ô, mỗi ô một tháng. Trong ô, các ngày của tháng đó năm 2011 (nửa trái) nối tiếp năm 2012 (nửa phải).
2. **Trục dọc**: lượt thuê mỗi ngày, từ 0.
3. **Ký hiệu**: đường xanh là tổng từng ngày; vạch cam là trung bình của tháng đó qua hai năm.
4. **Nhìn vào đâu**: trong mỗi ô, nửa phải so với nửa trái; và độ cao các vạch cam từ tháng 1 tới tháng 12.
5. **Kết luận**: tháng nào cũng nhảy bậc từ 2011 sang 2012, tức lượt thuê tăng ở mọi tháng chứ không riêng mùa hè; các vạch
   cam vẽ ra mùa vụ năm, thấp vào mùa đông, cao vào mùa hè.

Tổng tháng 2012 gấp 1,41 tới 2,57 lần cùng tháng năm 2011.

Bẫy khi đọc: bước nhảy **giữa** ô là ranh giới hai năm, không phải lượt thuê tăng dần trong tháng.

**Thư viện.** Không có hàm vẽ sẵn đáng tin cho dữ liệu giờ; tự dựng bằng `pivot_table` (dòng là giờ trong tuần, cột là tuần)
rồi `ax.plot`. Hàm `statsmodels.graphics.tsaplots.month_plot` tên có chữ "seasonal" nhưng thật ra vẽ **subseries** plot,
và chỉ nhận dữ liệu tháng hoặc quý.

**Tóm lại.** **Seasonal plot chồng các vòng lặp lên nhau để thấy hình dạng mùa vụ và vòng nào lệch. Subseries plot gom
từng "mùa" vào một ô để thấy mùa đó đổi thế nào qua thời gian.**

**Tự kiểm tra.** Bạn muốn biết "tháng 12 năm nay có thấp bất thường so với các tháng 12 trước không". Chọn hình nào?

<details>
<summary>Đáp án</summary>

**Subseries plot** theo tháng: ô tháng 12 đặt các tháng 12 cạnh nhau, điểm cuối thấp hơn vạch trung bình là thấy ngay.
Seasonal plot cũng thấy được (đường năm nay thấp ở vị trí tháng 12), nhưng khi chồng nhiều năm thì khó chỉ ra đường nào.
Nhầm hay gặp: dùng biểu đồ đường gộp tháng, nơi tháng 12 năm nay chỉ so được với tháng 11 ngay trước nó.

</details>

### 4.4 Heatmap và boxplot: trung bình từng ô, và độ tản

**Vấn đề.** Seasonal plot 106 đường thì rối. Muốn một hình duy nhất cho "mỗi thứ, mỗi giờ thường có bao nhiêu lượt", và
muốn biết giờ nào **khó đoán** (lúc đông lúc vắng).

**Heatmap giờ × thứ.** Bảng có một dòng cho mỗi thứ và một cột cho mỗi giờ. Ô (thứ $d$, giờ $h$) là **trung bình** lượt
thuê của mọi giờ thuộc thứ $d$ và giờ $h$, tô màu theo giá trị. Bằng pandas: `df.pivot_table(index="thu", columns="gio", values="cnt",
aggfunc="mean")`, rồi `ax.imshow(bang)`.

**Ví dụ số nhỏ — tự tính tay.** Ô (T2, 8h) lấy từ 5 thứ Hai. Thứ Hai tuần 2 là ngày lễ:

420, **60**, 450, 410, 440

- **Trung bình** (con số heatmap tô): (420 + 60 + 450 + 410 + 440) / 5 = 1.780 / 5 = **356**. Nó thấp hơn 4 trong 5 ngày,
  vì một ngày lễ kéo xuống.
- **Boxplot**: xếp tăng dần 60, 410, 420, 440, 450. Trung vị là số giữa, **420**. Quantile 0,25: ít nhất 25% số liệu, tức ít
  nhất 1,25 số, phải nhỏ hơn hoặc bằng nó; số nhỏ nhất như vậy là số thứ 2, **410**. Quantile 0,75: ít nhất 3,75 số, tức số
  thứ 4, **440**. Hộp đi từ 410 tới 440, vạch ở 420. IQR = 440 − 410 = 30.
- Số 60 nằm xa ngoài hộp: boxplot cho thấy ngày lễ là điểm lẻ, còn heatmap chỉ cho một ô hơi tối.

(Hai **râu** thò ra hai đầu hộp chỉ tới giá trị thấp nhất và cao nhất còn "không quá xa" hộp: tối đa 1,5 × IQR tính từ mép
hộp. Hình dưới tắt các điểm nằm ngoài râu cho dễ nhìn.)

![Heatmap giờ × thứ: 8h và 17h chỉ sáng vào ngày làm việc](hinh/nhiet-gio-thu.png)

**Cách đọc hình.**

1. **Trục ngang**: giờ trong ngày, 0 → 23.
2. **Trục dọc**: thứ, T2 trên cùng, CN dưới cùng.
3. **Ký hiệu**: màu ô là lượt thuê trung bình mỗi giờ; thang màu bên phải, tím ≈ 0, vàng ≈ 540.
4. **Nhìn vào đâu**: hai cột sáng ở 8h và 17h; và hai dòng T7, CN.
5. **Kết luận**: hai cột sáng lúc 8h và 17h chạy qua năm dòng ngày làm việc rồi tắt ở cuối tuần; cuối tuần sáng suốt giữa
   ngày.

| Ô (trung bình lượt/giờ) | T2 | T4 | T7 | CN |
|---|---|---|---|---|
| 8h | 412 | 488 | 114 | 84 |
| 13h | 206 | 186 | 385 | 375 |

**Đọc bảng.** Lúc 8h, ngày làm việc gấp nhiều lần cuối tuần; lúc 13h thì ngược lại, cuối tuần gấp khoảng đôi. Nhu cầu cuối
tuần không mất đi mà **dời giờ**.

![Boxplot theo giờ: ngày nghỉ đỉnh trưa, ngày làm việc đỉnh 8h và 17h](hinh/hop-theo-gio.png)

**Cách đọc hình.**

1. **Trục ngang**: giờ trong ngày; mỗi giờ có hai hộp đứng cạnh nhau.
2. **Trục dọc**: lượt thuê mỗi giờ.
3. **Ký hiệu**: hộp xanh là ngày làm việc, hộp cam là ngày nghỉ (cuối tuần và ngày lễ); vạch trong hộp là trung vị; râu là
   phạm vi không tính điểm quá xa.
4. **Nhìn vào đâu**: hộp xanh lúc 17h (cao nhất và rộng nhất); hai hộp lúc 8h.
5. **Kết luận**: giờ cao điểm cũng là giờ tản nhất, nên khó dự báo nhất; lúc 8h hai loại ngày gần như không chồng lên nhau.

| Nhóm | Trung vị | Quantile 0,25 – 0,75 |
|---|---|---|
| Ngày làm việc, 8h | 463 | 365 – 646 |
| Ngày làm việc, 17h | 539 | 348 – 704 |
| Ngày nghỉ, 8h | 94 | 57 – 141 |
| Ngày nghỉ, 13h | 367 | 236 – 493 |

**Đọc bảng.** So hai dòng 8h: hộp ngày nghỉ nằm hẳn dưới hộp ngày làm việc, nên "ngày làm việc hay ngày nghỉ" là thông tin
bắt buộc khi dự báo giờ đó. Dòng 17h ngày làm việc có hộp rộng nhất bảng, IQR khoảng 356 lượt.

**Tóm lại.** **Heatmap cho trung bình mỗi ô lịch trên một hình, thấy ngay mùa vụ kép; nhưng trung bình bị vài ngày lạ kéo
lệch và không cho biết độ tản. Boxplot cho trung vị và độ tản: hộp rộng là giờ khó dự báo.**

**Tự kiểm tra.** Heatmap cho 17h thứ Sáu 492, 17h thứ Ba 544. Có nên kết luận "thứ Sáu ít người đi làm bằng xe đạp"?

<details>
<summary>Đáp án</summary>

Chưa nên. Chênh 544 − 492 = 52 lượt, trong khi riêng hộp của các giờ 17h ngày làm việc đã rộng 704 − 348 = 356 lượt. Heatmap
chỉ cho trung bình, không cho độ tản, nên không biết chênh 52 là thật hay do vài ngày mưa. Nhầm hay gặp: coi mọi khác biệt màu
trên heatmap là khác biệt thật.

</details>

### 4.5 Lag plot và ACF: chuỗi giống chính nó lúc trước tới đâu

**Vấn đề.** Để dự báo giờ tới, ta hay dựa vào "giờ trước", "cùng giờ hôm qua", "cùng giờ tuần trước". Cái nào đáng tin nhất?
Lag plot trả lời bằng hình, ACF trả lời bằng một dãy số.

**Ví dụ số nhỏ — tự tính tay.** Chuỗi lặp mỗi 4 bước, $T = 8$ điểm: 2, 4, 6, 4, 2, 4, 6, 4.

- **Lag plot trễ 2**: ghép mỗi điểm với điểm cách nó 2 bước về trước, được 6 cặp $(y_{t-2}, y_t)$: (2, 6), (4, 4), (6, 2),
  (4, 4), (2, 6), (4, 4). Chấm các cặp lên scatter: chúng nằm trên đường **đi xuống**. Đỉnh 6 ghép với đáy 2 và ngược lại.
- **Tự tương quan**: trung bình là 32 / 8 = 4. Độ lệch khỏi trung bình: −2, 0, 2, 0, −2, 0, 2, 0. Tổng bình phương độ lệch
  (mẫu số): 4 + 0 + 4 + 0 + 4 + 0 + 4 + 0 = 16.
  - Trễ 2: nhân độ lệch của mỗi điểm với độ lệch của điểm cách nó 2 bước: 2 × (−2) + 0 × 0 + (−2) × 2 + 0 × 0 + 2 × (−2) + 0 × 0
    = −12. Vậy $r_2 = -12 / 16 = -0{,}75$.
  - Trễ 4: (−2) × (−2) + 0 × 0 + 2 × 2 + 0 × 0 = 8. Vậy $r_4 = 8 / 16 = 0{,}5$.
  - Trễ 1: mọi tích đều có một thừa số 0, nên $r_1 = 0$.

Trễ bằng đúng một vòng lặp cho $r$ dương; trễ bằng nửa vòng cho $r$ âm, vì đỉnh ghép với đáy. Chuỗi lặp hoàn hảo mà $r_4$ chỉ
là 0,5: tử số chỉ có 4 cặp, còn mẫu số cộng cả 8 điểm. Chuỗi càng dài, chênh lệch này càng nhỏ.

**Công thức.** Tự tương quan ở độ trễ $k$ (FPP §2.8):

$$
r_k = \frac{\sum_{t=k+1}^{T} (y_t - \bar y)(y_{t-k} - \bar y)}{\sum_{t=1}^{T} (y_t - \bar y)^2}
$$

- $T$: số điểm của chuỗi; $\bar y$: trung bình của chuỗi.
- $y_t - \bar y$: điểm ở thời điểm $t$ cao hơn (dương) hay thấp hơn (âm) trung bình bao nhiêu.
- Tử số: cộng tích độ lệch của mỗi điểm với độ lệch của điểm cách nó $k$ bước về trước, từ $t = k + 1$ (điểm đầu tiên có
  "người đi trước" cách $k$ bước) tới $T$.
- Mẫu số: tổng bình phương độ lệch của mọi điểm; nó làm $r_k$ nằm trong khoảng −1 tới 1.

**Nói bằng lời.** Cộng các tích "độ lệch bây giờ × độ lệch $k$ bước trước", rồi chia cho tổng bình phương độ lệch. Hai điểm
cùng phía trung bình cho tích dương, khác phía cho tích âm. Với chuỗi trên, trễ 2 có ba tích −4 và ba tích 0, nên
$r_2 = -12 / 16 = -0{,}75$: cứ cao thì 2 bước sau thấp.

**NumPy và thư viện.** Hàm `acf_nhanh` trong `code/bieu_do.py` làm đúng công thức trên, bỏ qua cặp có NaN:

```python
lech = y - np.nanmean(y)
mau = np.nansum(lech**2)
r = [np.nansum(lech[k:] * lech[:-k]) / mau for k in range(1, so_tre + 1)]
```

`statsmodels.graphics.tsaplots.plot_acf` vẽ sẵn; dải xám của nó mặc định **rộng dần** theo độ trễ, khác dải cố định dùng dưới
đây.

![Lag plot: trễ 168 bám đường chéo nhất, trễ 12 tản thành hai nhánh](hinh/tre.png)

**Cách đọc hình.**

1. **Trục ngang** (mỗi ô): lượt thuê lúc $t - k$ giờ, với $k$ = 1, 12, 24, 168.
2. **Trục dọc**: lượt thuê lúc $t$, cùng thang 0–1.000 lượt/giờ.
3. **Ký hiệu**: mỗi chấm là một cặp giờ; đường cam là đường chéo "lượt lúc $t$ = lượt lúc $t - k$"; tiêu đề ô ghi $r$.
4. **Nhìn vào đâu**: ô trễ 12 (hai nhánh bám hai trục) và ô trễ 168 (đám chấm hẹp nhất quanh đường chéo).
5. **Kết luận**: cùng giờ tuần trước đoán giờ này tốt nhất (đám chấm hẹp nhất, $r = 0{,}88$), hơn cả giờ ngay trước và cùng
   giờ hôm qua; trễ 12 ghép đỉnh với đáy nên $r$ gần 0.

Ô trễ 12 là ví dụ số nhỏ phóng to: giờ đông buổi sáng ghép với giờ vắng lúc đêm hôm trước, giờ đông buổi chiều ghép với giờ
vắng lúc rạng sáng. Hai nhánh đổ theo hai trục, và $r = -0{,}14$ chỉ là trung bình của hai nhánh, không phải "quan hệ âm"
dùng được.

![ACF có đỉnh mỗi 24 giờ, đỉnh ở 168 và 336 cao hơn các đỉnh xung quanh](hinh/acf.png)

**Cách đọc hình.**

1. **Trục ngang**: độ trễ $k$, 0 → 336 giờ (hai tuần).
2. **Trục dọc**: hệ số tự tương quan $r_k$, từ −1 tới 1 (hình chỉ hiện −0,3 tới 1).
3. **Ký hiệu**: mỗi vạch xanh là một $r_k$; vạch cam đứt ở 24, 168, 336; dải xám rất hẹp quanh 0 (giải thích dưới bảng).
4. **Nhìn vào đâu**: dãy đỉnh cách nhau 24 giờ; so đỉnh ở 168 với đỉnh ở 144.
5. **Kết luận**: đỉnh lặp mỗi 24 giờ là mùa vụ ngày; đỉnh ở 168 giờ (đúng một tuần) cao hơn các đỉnh ngay cạnh, nên còn
   mùa vụ tuần lồng lên trên.

| Độ trễ $k$ (giờ) | 12 | 24 | 144 | 168 | 336 |
|---|---|---|---|---|---|
| $r_k$ | −0,143 | 0,813 | 0,786 | 0,864 | 0,854 |

**Đọc bảng.** Đỉnh một tuần (168) cao hơn đỉnh sáu ngày (144) ngay trước nó, và đỉnh hai tuần (336) vẫn cao: cùng giờ, cùng
thứ mới là "người giống nhất".

Dải xám, ±1,96/√T, là vùng mà $r_k$ của một chuỗi hoàn toàn ngẫu nhiên thường rơi vào (buổi 7 học kỹ). Với $T = 17.379$ giờ
nó chỉ rộng ±0,015, nên gần như mọi vạch đều vượt. Ở dữ liệu dài, **đọc hình dạng** (đỉnh ở đâu, cao thấp ra sao), đừng đếm vạch vượt
dải.

$r_{168}$ của ACF (0,864) hơi khác $r$ của lag plot trễ 168 (0,876): lag plot tính hệ số tương quan trên các cặp (buổi 2), ACF dùng trung bình và mẫu số của cả chuỗi.

**Tóm lại.** **Lag plot bám đường chéo ở trễ $k$ nghĩa là giá trị cách $k$ bước đoán tốt giá trị hiện tại. ACF có đỉnh ở
bội số của chu kỳ mùa vụ; trễ bằng nửa chu kỳ mùa vụ ghép đỉnh với đáy nên $r$ nhỏ hoặc âm.**

**Tự kiểm tra.** Chuỗi 1, 3, 1, 3, 1, 3. Không tính, đoán dấu của $r_1$ và $r_2$; rồi tính $r_1$.

<details>
<summary>Đáp án</summary>

Chuỗi lặp mỗi 2 bước: trễ 1 là nửa vòng (đỉnh ghép đáy) nên $r_1$ âm; trễ 2 là một vòng nên $r_2$ dương. Tính: trung bình
2, độ lệch −1, 1, −1, 1, −1, 1, mẫu số 6. Tử số trễ 1 có 5 tích, mỗi tích (−1) × 1 = −1, tổng −5. $r_1 = -5/6 \approx -0{,}83$.
Nhầm hay gặp: chia cho số cặp (5) thay vì tổng bình phương độ lệch của cả chuỗi (6), ra −1.

</details>

### 4.6 Hình nói sai: trục kép, trục y cắt, trộn nhiều năm

**Vấn đề.** Không cần sửa một con số nào vẫn có thể làm hình nói sai. Ba cách hay gặp: hai trục dọc thang tuỳ ý, trục dọc
không bắt đầu từ 0, và gộp nhiều năm vào một scatter.

**Ví dụ số nhỏ — tự tính tay.**

- **Trục y cắt.** Doanh thu tháng 5 là 490 triệu, tháng 6 là 510 triệu, tăng 510 / 490 − 1 ≈ 4,1%. Vẽ trục từ 480 tới 520:
  tháng 5 cao (490 − 480) / 40 = 25% chiều cao hình, tháng 6 cao (510 − 480) / 40 = 75%. Mắt thấy "gấp 3 lần".
- **Trục kép.** Hai chuỗi ba tháng, A tính bằng triệu lượt, B tính bằng °C. Mỗi điểm cao bao nhiêu phần chiều cao hình =
  (giá trị − đáy trục) / (đỉnh trục − đáy trục):

| | Tháng 1 | Tháng 2 | Tháng 3 | Tăng thật |
|---|---|---|---|---|
| A (triệu lượt), trục trái 1–3 | 1 → 0% | 2 → 50% | 3 → 100% | +200% |
| B (°C), trục phải 20–22 | 20 → 0% | 21 → 50% | 22 → 100% | +10% |
| B (°C), trục phải 0–30 | 20 → 67% | 21 → 70% | 22 → 73% | +10% |

**Đọc bảng.** Với trục phải hẹp (dòng 2), hai đường **trùng khít** dù A tăng nhanh hơn B rất nhiều tính theo phần trăm; với
trục phải rộng (dòng 3), B gần như nằm ngang. Chỗ hai đường gặp nhau hay tách nhau do người vẽ chọn thang, không do dữ liệu.

![Trục kép với trục trái cắt ở 90.000 làm hai đường gần trùng nhau](hinh/gay-hieu-nham.png)

**Cách đọc hình.**

1. **Trục ngang**: tháng năm 2012.
2. **Trục dọc**: **hai** trục, không ghi tên. Trái là lượt thuê mỗi tháng, bắt đầu từ 90.000; phải là nhiệt độ trung bình
   (°C), 5–32.
3. **Ký hiệu**: đường xanh chấm tròn là lượt thuê (trục trái); đường cam chấm vuông là nhiệt độ (trục phải).
4. **Nhìn vào đâu**: điểm tháng 1 của đường xanh sát đáy; và hai đường gần như đè nhau.
5. **Kết luận**: hình trông như "lượt thuê bám sát nhiệt độ", nhưng sự trùng khít do chọn thang phải, còn trục trái cắt ở
   90.000 làm tháng thấp nhất trông gần như bằng 0.

Nghiên cứu cảm nhận cho thấy trục y cắt làm người xem thấy chênh lệch lớn hơn thật, **kể cả khi** hình có ký hiệu báo trục bị
cắt (Correll và cộng sự, 2020). Vì vậy quy ước của khoá: số đếm và tổng (cột, diện tích tô, lượt thuê) vẽ trục từ 0. Đại
lượng như nhiệt độ thì không bắt buộc: chọn phạm vi theo độ lớn thay đổi có ý nghĩa, và ghi rõ trên trục.

![Vẽ lại: tách hai hình, lượt thuê từ 0, scatter để nói về quan hệ](hinh/ve-lai.png)

**Cách đọc hình.**

1. **Trục ngang**: ô trái và giữa là tháng 2012; ô phải là nhiệt độ trung bình tháng (°C).
2. **Trục dọc**: ô trái là lượt thuê mỗi tháng, từ 0; ô giữa là °C, từ 0; ô phải là lượt thuê mỗi tháng, từ 0.
3. **Ký hiệu**: ô phải, mỗi chấm là một tháng, số cạnh chấm là tháng mấy.
4. **Nhìn vào đâu**: ô phải, ba chấm tháng 7, 8, 9.
5. **Kết luận**: quan hệ có thật ($r = 0{,}91$ qua mười hai tháng) nhưng không tăng mãi: tháng 9 mát hơn tháng 7 khoảng 5 °C
   mà lượt thuê cao nhất năm; trục kép không cho thấy điều này.

Muốn đặt hai chuỗi khác đơn vị lên cùng một trục thì **đánh chỉ số**: chia mỗi chuỗi cho giá trị tháng đầu rồi nhân 100. Cả
hai cùng bắt đầu ở 100, và trục đọc là "phần trăm so với tháng đầu".

**Trộn nhiều năm trong một scatter.** Scatter nhiệt độ × lượt thuê theo ngày, tô màu theo năm:

![Cùng nhiệt độ, 2012 cao hơn 2011: quan hệ dời theo năm](hinh/phan-tan-nhiet-do.png)

**Cách đọc hình.**

1. **Trục ngang**: nhiệt độ trung bình ngày (°C). Tệp lưu cột `temp` đã chia cho 41 nên hình nhân lại 41; tài liệu của bộ dữ liệu
   ghi hai cách đổi ra °C khác nhau, nên chỉ đọc vị trí tương đối, đừng trích độ C tuyệt đối.
2. **Trục dọc**: lượt thuê mỗi ngày.
3. **Ký hiệu**: chấm xanh là một ngày năm 2011, chấm cam là một ngày năm 2012.
4. **Nhìn vào đâu**: một cột dọc bất kỳ, ví dụ quanh 25 °C: chấm cam nằm trên chấm xanh.
5. **Kết luận**: hai đám mây song song, cùng nhiệt độ thì 2012 cao hơn 2011; quan hệ dời lên theo năm (nhiều người dùng hơn),
   không phải do nhiệt độ.

| Tương quan nhiệt độ × lượt/ngày | 2011 | 2012 | gộp hai năm |
|---|---|---|---|
| $r$ | 0,771 | 0,714 | 0,627 |

**Đọc bảng.** Gộp hai năm cho $r$ thấp hơn **cả hai** năm riêng: trộn hai mức khác nhau làm đám điểm dày theo chiều dọc, quan
hệ trông yếu hơn thật. Tô màu theo thời gian để thấy điều đó.

**Tóm lại.** **Trục kép cho phép người vẽ chọn chỗ hai đường gặp nhau; trục y cắt phóng to chênh lệch nhỏ. Muốn nói về quan
hệ thì vẽ scatter (tô màu theo thời gian) và tính $r$; số đếm và tổng vẽ trục từ 0.**

**Tự kiểm tra.** Một biểu đồ cột có trục từ 480 đến 520, tiêu đề "Doanh thu tăng mạnh tháng 6" (490 → 510 triệu). Viết lại
tiêu đề và nói sửa trục thế nào.

<details>
<summary>Đáp án</summary>

Trục bắt đầu từ 0, vì doanh thu là tổng và độ dài cột phải tỷ lệ với giá trị. Tiêu đề: "Doanh thu tháng 6 tăng 4,1% so với
tháng 5 (490 → 510 triệu)". Muốn nhấn thay đổi nhỏ thì vẽ thêm một hình riêng về phần trăm thay đổi, trục quanh 0. Nhầm hay gặp:
chỉ thêm ký hiệu "trục bị cắt" rồi giữ nguyên, trong khi người xem vẫn thấy phóng đại.

</details>

## 5. Lab từng bước

Lệnh gõ trong terminal ở thư mục `lab/`. Code các bước nằm sẵn trong `code/lab.ipynb` (mở bằng `python lab.py notebook` hoặc
VS Code), chạy từng ô từ trên xuống. Bạn sửa `code/bieu_do.py`; notebook tự nạp lại bản mới.

### Bước 1 — Chạy code đầu buổi

**Mục đích:** thấy bộ biểu đồ "chẩn đoán" hiện tại không cho biết gì về tuần.

```bash
python lab.py up           # một lần: môi trường + dữ liệu Bike Sharing, kiểm sha256
python lab.py check        # 7/8 test đỏ
python lab.py notebook     # chạy ô bước 1
```

**Đọc kết quả:**

- In `17544 giờ trên lưới, thiếu 165`, rồi bảng `ho_so_tuan`: **bảy dòng giống hệt nhau**, lúc 8h thứ nào cũng 359.
- Hình có 2 ô: đường thô 17.544 giờ (khối màu, mục 4.1) và trục kép có trục y cắt (mục 4.6). Không ô nào cho thấy thứ Bảy khác
  thứ Hai.

### Bước 2 — Sửa `ho_so_tuan`

**Mục đích:** dữ liệu của heatmap phải tách theo **thứ**, không chỉ theo giờ (mục 4.4).

Dùng `pivot_table(index="thu", columns="gio", values="cnt", aggfunc="mean")` rồi `reindex` về 7 dòng × 24 cột. Chạy lại ô bước 2.

**Đọc kết quả:** lúc 8h, thứ Hai ra 412 và Chủ nhật ra 84, khớp bảng heatmap mục 4.4.

Dòng đầu thấp mà dòng cuối cao thì bạn đang đánh 0 = Chủ nhật như cột `weekday` của tệp gốc; dùng cột `thu` (từ `dayofweek`, 0 = thứ Hai).

### Bước 3 — Viết 8 hàm vẽ, ghép `bo_bieu_do_chan_doan`

**Mục đích:** có một bộ hình dùng lại cho mọi chuỗi lạ ở các buổi sau.

Mỗi hàm nhận `(ax, df)` và vẽ vào một ô. Lưới 4 × 2, gắn `ax.set_label(nhan)` với nhãn: `duong`, `mua_vu_tuan`,
`chuoi_con_thang`, `tre`, `nhiet_gio_thu`, `hop_theo_gio`, `phan_tan_nhiet_do`, `acf`. Bộ chấm đòi:

- không `twinx` (trục kép);
- biểu đồ đường gộp theo ngày (dưới 5.000 điểm) và trục y từ 0;
- ACF tới ít nhất trễ 168;
- tiêu đề mỗi ô ≥ 20 ký tự, là một câu kết luận (mục 4.1).

Mỗi hàm tương ứng một hình của mục 4; ghi trục có đơn vị. Chạy lại ô bước 3.

**Đọc kết quả:** 8 ô như các hình mục 4.1–4.6. Heatmap mà năm dòng đầu giống hai dòng cuối thì bước 2 chưa đúng. ACF không có
đỉnh ở 168 thì bạn vẽ chưa tới trễ 168.

### Bước 4 — Năm nhận xét có bằng chứng

**Mục đích:** luyện bước 5 của "Cách đọc hình" trên chính bộ hình của bạn.

Viết năm câu, mỗi câu dạng "*[nhận xét]* — thấy ở *[hình]*, *[chỗ nào]*, *[con số]*". Ví dụ: "Cuối tuần không có giờ cao
điểm đi làm — heatmap, cột 8h, hai dòng cuối tuần tối (dưới 120 lượt, so với trên 400 ngày làm việc)."

**Đọc kết quả:** câu nào không chỉ ra được hình, chỗ và số thì chưa phải nhận xét, chỉ là cảm giác.

### Bước 5 — Vẽ lại biểu đồ gây hiểu nhầm

**Mục đích:** sửa hai thủ thuật của mục 4.6 mà không đổi dữ liệu.

`bieu_do_gay_hieu_nham(df)` dựng sẵn, không sửa. Viết `ve_lai_trung_thuc(df)`: không trục kép, trục lượt thuê từ 0, có một hình
nói về **quan hệ** (scatter). Chạy ô bước 5, rồi:

```bash
python lab.py check        # 8/8 xanh
```

**Đọc kết quả:** xanh 8/8 là xong. `test_ve_lai_trung_thuc` còn đỏ: kiểm lại có ô nào còn `twinx`, hoặc trục lượt thuê chưa
`set_ylim(bottom=0)`.

## 6. Lỗi thường gặp & cách chẩn đoán

| Triệu chứng | Nguyên nhân | Chẩn đoán | Sửa |
|---|---|---|---|
| Hình đường là một khối màu | quá nhiều điểm cho bề rộng hình | đếm số điểm | gộp theo ngày, hoặc vẽ một đoạn ngắn |
| "Không có mùa vụ tuần" | chỉ nhìn đường thô hoặc tổng tháng | heatmap giờ × thứ, ACF tới trễ 168 | thêm seasonal plot tuần + heatmap |
| Heatmap lệch một ngày | lẫn 0 = CN (cột `weekday` của tệp) với 0 = T2 (`dayofweek`) | kiểm một ngày đã biết: 01/01/2011 là thứ Bảy | dùng một quy ước, ghi rõ |
| Giờ thiếu hiện thành 0 | `resample().sum()` không `min_count` | đếm NaN trên lưới đầy đủ | `min_count`, hoặc giữ NaN |
| Ngày bất thường biến mất | làm trơn hoặc gộp tháng | vẽ chấm gốc dưới đường trơn | luôn giữ lớp dữ liệu gốc |
| "Trễ 12 có quan hệ âm" | đỉnh ghép đáy của mùa vụ ngày | lag plot có hai nhánh | đọc theo vòng lặp, không theo dấu của $r$ |
| Hàng trăm vạch ACF "vượt dải" | $T$ lớn nên dải rất hẹp (±0,015) | tính 1,96/√T | đọc hình dạng; kiểm định ở buổi 7 |
| `month_plot` báo lỗi với dữ liệu giờ | hàm chỉ nhận dữ liệu tháng/quý | đọc tài liệu hàm | tự dựng subseries bằng `pivot_table` |
| `seaborn.boxplot` phát cảnh báo `vert` | seaborn 0.13 gọi API cũ của matplotlib 3.11 | cảnh báo đến từ seaborn | vô hại; hoặc dùng `ax.boxplot` |

## 7. Bài tập về nhà

1. **Chuỗi lạ trong 20 phút.** Áp `bo_bieu_do_chan_doan` cho cột `casual` (khách vãng lai, không đăng ký) của `hour.csv`: sửa
   `doc_luot_thue` để lấy `casual` vào chỗ `cnt`. Viết 5 nhận xét có bằng chứng. Mùa vụ tuần của `casual` khác `cnt` thế nào?
2. **Seasonal plot theo năm.** Vẽ tổng theo ngày theo "ngày thứ mấy trong năm", mỗi năm một đường. Tìm hai khoảng mà hai năm khác
   nhau rõ, giải thích bằng dữ liệu (ngày lễ, thời tiết, ngày thiếu).
3. **Hai tỷ lệ khung hình.** Vẽ tổng theo ngày năm 2012 ở khung vuông (1 : 1) và khung dẹt (8 : 1). Mỗi khung làm lộ điều gì mà
   khung kia che?

## 8. Tiêu chí "Xong khi"

- [ ] `python lab.py check` xanh 8/8.
- [ ] Với một chuỗi lạ, trong 20 phút nộp bộ 8 biểu đồ + 5 nhận xét, mỗi nhận xét chỉ vào hình, chỗ, con số.
- [ ] Chỉ ra mùa vụ kép ngày + tuần trên ít nhất hai hình mà biểu đồ đường thô che mất.
- [ ] Giải thích hai thủ thuật của biểu đồ gây hiểu nhầm và vì sao bản vẽ lại trung thực hơn.

## 9. Đọc thêm

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way*, chương 2 — Time series
  graphics: https://otexts.com/fpppy/nbs/02-graphics.html
- Correll, M., Bertini, E. & Franconeri, S. (2020). Truncating the Y-Axis: Threat or Menace? *CHI 2020*. arXiv:1907.02035
- To Cut or Not To Cut? A Systematic Exploration of Y-Axis Truncation. *CHI 2024*. doi:10.1145/3613904.3642102
- Few, S. (2008). Dual-Scaled Axes in Graphs: Are They Ever the Best Solution? *Perceptual Edge*.
- Muth, L.C. Bài về biểu đồ trục kép, *Datawrapper Blog* (có cập nhật sau 2018): https://www.datawrapper.de/blog/dualaxis/
- Heer, J. & Agrawala, M. (2006). Multi-Scale Banking to 45 Degrees. *IEEE TVCG* 12(5) — tỷ lệ khung hình (bài tập 3).
- Fanaee-T, H. & Gama, J. (2013). Bike Sharing Dataset, doi:10.1007/s13748-013-0040-3; dữ liệu doi:10.24432/C5W894.
- Phụ lục C của khoá — Sổ tay đọc biểu đồ (mỗi loại hình theo đúng năm bước của mục 4.1).
