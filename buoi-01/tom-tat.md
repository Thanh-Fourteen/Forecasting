# Buổi 1 — Tóm tắt: Forecasting là gì

**Mục tiêu đầu bài.** Sau buổi này bạn:

1. Viết được phiếu bài toán dự báo 6 ô.
2. Phân biệt dự báo với mục tiêu và kế hoạch; nêu bốn yếu tố quyết định một thứ dự báo được tới đâu.
3. Chỉ ra bằng số vì sao chấm trên chính dữ liệu đã dùng cho **sai số ảo**.
4. Chỉ ra vì sao thiếu **baseline** thì một con số sai số không nói lên gì.
5. Giải thích vì sao khi thiếu và thừa đắt khác nhau, ta cần cả **phân phối**.

Dữ liệu lab: điện một hộ ở Sceaux (gần Paris), đo từng phút 12/2006–11/2010, gộp thành 34.464 giờ (431 giờ trống).

---

## 1. Dự báo (forecast), mục tiêu (goal), kế hoạch (plan); cái gì dự báo được

**Kết luận của phần.** Dự báo nói điều **sẽ** xảy ra, độc lập với điều ta muốn. Mức độ dự báo được phụ thuộc bốn yếu
tố.

### Dự báo (forecast), mục tiêu (goal), kế hoạch (plan)

- **Định nghĩa** (FPP §1.2).
  - **Dự báo**: ước tính điều sẽ xảy ra, với mọi thông tin đang có.
  - **Mục tiêu**: điều ta muốn xảy ra.
  - **Kế hoạch**: hành động để tiến gần tới mục tiêu.
- **Ví dụ.** Quán cà phê dự báo tuần tới bán khoảng 1.900 ly. Sếp đặt mục tiêu 2.500 ly. Kế hoạch là chạy khuyến mãi và
  đặt thêm hạt.
- **Vai trò trong dự báo.** Kế hoạch được lập **dựa trên** dự báo trung thực. Nếu dự báo bị sửa theo mục tiêu thì kế
  hoạch không còn cơ sở.
- **Phân biệt.** Báo "dự báo 2.500" vì sếp muốn vậy là lẫn mục tiêu với dự báo. Kho sẽ đặt nguyên liệu cho 2.500 ly
  trong khi chỉ bán 1.900, và không ai biết mô hình đúng hay sai.

### Bốn yếu tố quyết định khả năng dự báo (forecastability)

- **Định nghĩa** (FPP §1.1). Một đại lượng dự báo được càng chính xác khi:
  1. hiểu rõ các yếu tố tác động tới nó;
  2. có nhiều dữ liệu;
  3. tương lai giống quá khứ;
  4. dự báo không làm thay đổi chính đại lượng được dự báo.
- **Ví dụ.**

  | Yếu tố | Điện một hộ, ngày mai | Tỷ giá, tuần sau |
  |---|---|---|
  | 1. Hiểu tác động | có: giờ giấc, thời tiết, ngày nghỉ | ít |
  | 2. Nhiều dữ liệu | có: 4 năm, từng phút | có |
  | 3. Tương lai giống quá khứ | thường có | khủng hoảng làm đổi hẳn |
  | 4. Không tự tác động | đúng: hộ không đọc dự báo | sai: nhà đầu tư mua bán theo dự báo |

- **Cách diễn giải.** Điện ngày mai thoả cả bốn yếu tố nên dự báo được rất chính xác. Tỷ giá chỉ thoả yếu tố 2.
- **Phân biệt.** Hãng xe báo "tháng sau giá tăng", khách đổ xô mua trước. Trường hợp này vi phạm yếu tố 4, không phải
  yếu tố 3: tương lai khác quá khứ, nhưng nguyên nhân là chính lời dự báo.

---

## 2. Phiếu bài toán dự báo

**Kết luận của phần.** Trước khi mở dữ liệu, phải xác định dự báo phục vụ quyết định nào. Sáu ô của phiếu quyết định
baseline hợp lệ, cách chấm và con số nên báo.

### Phiếu bài toán 6 ô — phương pháp

- **Mục đích.** Chốt yêu cầu của bài toán trước khi làm mô hình (FPP §1.6 gọi đây là bước thường khó nhất).
- **Quy trình.** Trả lời 6 câu hỏi:

  | Ô | Câu hỏi | Quyết định điều gì |
  |---|---|---|
  | 1. Quyết định | ai dùng dự báo, làm gì, bao lâu một lần | mọi ô còn lại |
  | 2. Biến mục tiêu (target) | đo cái gì, đơn vị nào | xử lý dữ liệu |
  | 3. Tầm dự báo (horizon) | xa bao nhiêu bước | baseline hợp lệ |
  | 4. Độ chi tiết (granularity) | gộp tới mức nào, chấm ở mức nào | cách chấm, mô hình thắng |
  | 5. Mốc cắt dữ liệu (cutoff) | lúc ra dự báo đã biết gì | dữ liệu được dùng |
  | 6. Chi phí hai chiều | thiếu mất gì, thừa mất gì | con số nên báo |

- **Ví dụ.** Công ty bán lẻ điện, cuối Chủ nhật đặt mua điện theo giờ cho 7 ngày tới. Tầm dự báo 1–168 giờ, chấm theo
  giờ. Mỗi kWh thiếu mất khoảng 4 đồng, mỗi kWh thừa mất khoảng 1 đồng.
- **Khi nào hỏng.** Ô 6 chỉ ghi một chiều. Khi đó chưa biết nên báo con số nào.

### Gốc dự báo (forecast origin) và mốc cắt dữ liệu (cutoff)

- **Định nghĩa.** Gốc dự báo là thời điểm ra dự báo. Mọi dữ liệu sau gốc coi như chưa biết.
- **Ký hiệu.**
  - $T$: giờ cuối cùng đã có số đo; gốc nằm ngay sau $T$.
  - $h$: tầm dự báo (forecast horizon), tính bằng số bước từ $T$.
  - $\hat y_{T+h}$: số dự báo cho giờ $T+h$.
- **Ví dụ.** $T$ = 23:00 Chủ nhật 3/1/2010. Dự báo 19:00 thứ Ba 5/1 có $h$ = 24 + 20 = 44.
- **Vai trò.** Mốc cắt quyết định dữ liệu nào hợp lệ. Dùng số sau gốc là gian lận.

### Độ chi tiết (granularity)

- **Định nghĩa.** Mức gộp dữ liệu và mức chấm dự báo: từng giờ, từng ngày hay tổng tuần.
- **Vai trò trong dự báo.** Khi cộng nhiều bước lại (gộp — aggregation), sai số lệch lên và lệch xuống bù trừ nhau. Chỉ lệch cùng một chiều
  kéo dài là dồn lại. Vì vậy thứ hạng mô hình có thể đảo khi đổi độ chi tiết (phần 4).
- **Ví dụ.** Thực tế 2, 0, 2, 0.
  - Cách A dự báo 1, 1, 1, 1: MAE theo giờ là 1, sai số tổng là 0.
  - Cách B dự báo 2,5; 0,5; 2,5; 0,5: MAE theo giờ là 0,5, sai số tổng là −2.
  - Theo giờ B thắng; theo tổng A thắng.
- **Phân biệt.** "MAE theo giờ nhỏ thì tổng tuần cũng chính xác" là sai.

![Tổng tuần: thứ hạng đảo](hinh/tong-tuan.png)

**Đọc hình.** Cộng lên tổng tuần thì thứ hạng đảo.

### Công suất (power) và điện năng (energy)

- **Định nghĩa.**
  - **Công suất** (kW): mức tiêu thụ tại một thời điểm.
  - **Điện năng** (kWh): lượng đã tiêu thụ, bằng công suất × thời gian.
- **Ví dụ.** 2,0 kW trong 30 phút rồi 0,4 kW trong 30 phút: điện năng 1,0 + 0,2 = 1,2 kWh, bằng trung bình công suất
  (2,0 + 0,4)/2 = 1,2 kW.
- **Tính chất.** Trung bình công suất trong **một giờ** bằng số kWh của giờ đó.
- **Phân biệt.** Máy 1,5 kW chạy 40 phút trong giờ thì dùng 1,0 kWh, không phải 1,5 kWh.

### Mùa vụ (seasonality)

- **Định nghĩa.** Mẫu hình (pattern) lặp lại đều đặn theo lịch, với chu kỳ cố định.
- **Ví dụ.** Điện của hộ này có ba mùa vụ:
  - theo ngày: thấp nhất lúc 4h, cao nhất lúc 20h;
  - theo tuần: cuối tuần dùng nhiều hơn ngày thường;
  - theo năm: mùa đông cao, tháng 8 gần như vắng nhà.
- **Vai trò trong dự báo.** Mùa vụ là nguồn thông tin chính. Baseline "cùng thời điểm của chu kỳ trước" khai thác trực
  tiếp mùa vụ.

![Điện tiêu thụ theo ngày của một hộ](hinh/mot-duong.png)

**Đọc hình.** Mùa đông cao, tháng 8 gần như vắng nhà, năm sau giống năm trước.

---

## 3. Sai số ảo (in-sample error) và cách chấm trung thực

**Kết luận của phần.** Chấm trên dữ liệu đã dùng để khớp mô hình cho sai số ảo, đẹp hơn thực tế. Cùng mô hình bảng
lịch: nhìn trộm cho MAE **0,380**, chấm trung thực cho **0,508** kWh/giờ, lớn hơn khoảng 34%.

### Sai số dự báo (forecast error)

- **Định nghĩa.** Sai số = thực tế − dự báo, đo trên dữ liệu mô hình **chưa thấy**.
- **Ví dụ.** Thực tế 1,7, dự báo 1,5 → sai số +0,2.
- **Cách diễn giải.**
  - Dương: dự báo thấp hơn thực tế. Nếu mua đúng bằng dự báo thì sẽ **thiếu**.
  - Âm: dự báo cao hơn thực tế, sẽ **thừa**.

### MAE (mean absolute error — sai số tuyệt đối trung bình)

- **Định nghĩa.**
  $$\text{MAE} = \frac1n\sum_{t=1}^{n} \lvert y_t - \hat y_t \rvert$$
- **Ví dụ.** Sai số +0,5; −0,5; +1,0; 0 → MAE = 2,0/4 = 0,5 kWh.
- **Cách diễn giải.** Mức lệch trung bình mỗi bước, cùng đơn vị với dữ liệu. Nhỏ hơn là tốt hơn.
- **Tính chất.** Phạt thiếu và thừa như nhau, nên con số tối ưu theo MAE là trung vị.
- **Phân biệt.** MAE thấp không có nghĩa chi phí thấp khi thiếu và thừa đắt khác nhau (phần 5).

### Phần dư (residual) và sai số ảo

- **Định nghĩa.**
  - **Phần dư** (residual): chênh lệch đo trên chính dữ liệu đã dùng để khớp (fit) mô hình (FPP §5.8).
  - **Sai số ảo**: phần dư được báo cáo như sai số dự báo.
- **Ví dụ.** Một ô bảng lịch có ba giờ cũ 1,0; 1,4; 1,2. Giờ cần chấm là 2,0.
  - Trung thực: dự báo 1,2, sai số 0,8.
  - Nhìn trộm (thêm cả giờ đang chấm vào trung bình): dự báo 1,4, sai số 0,6.
- **Tính chất.** Mô hình càng nhiều tham số (parameter) càng dễ khớp hoàn hảo dữ liệu đã thấy (overfitting). Vì vậy phần dư nhỏ không đảm bảo dự
  báo tốt.
- **Vì sao chênh lệch lớn ở lab.** Khoảng 22% số liệu trong mỗi ô bảng lịch chính là các giờ đang được chấm.

![Sai số ảo và bảng xếp hạng thật](hinh/sai-so-ao.png)

**Đọc hình.** Nhìn trộm thì bảng lịch đứng đầu; chấm trung thực thì nó thua trung bình 4 tuần.

![Một tuần: dự báo đã thấy đáp án](hinh/mot-tuan.png)

**Đọc hình.** Đây là tuần hai cách chấm chênh nhất; đường cam "trúng" hơn chỉ vì mỗi ô đã chứa chính giờ đang chấm.

### Dự báo cuốn (rolling forecast) — phương pháp

- **Mục đích.** Chấm dự báo đúng như khi dùng thật.
- **Quy trình.**
  1. Tại mỗi gốc (00:00 thứ Hai), chỉ lấy dữ liệu **trước** gốc.
  2. Khớp mô hình, dự báo 168 giờ tới.
  3. So với số đo thật.
  4. Dời gốc sang tuần sau, lặp lại.
- **Ví dụ.** Năm 2010 có 46 gốc: 7.728 giờ, bỏ 293 giờ trống, còn 7.435 giờ được chấm.
- **Ưu điểm.** Mô hình không bao giờ thấy đáp án.
- **Cách kiểm tra.** Đổi số đo trong giai đoạn chấm. Nếu dự báo đổi theo thì cách chấm đang nhìn trộm.

---

## 4. Baseline

**Kết luận của phần.** Một con số sai số chỉ có nghĩa khi so với baseline. Chấm trung thực, bảng lịch (0,508) **thua**
baseline trung bình 4 tuần (0,490) theo giờ.

### Baseline

- **Định nghĩa.** Phương pháp dự báo đơn giản dùng làm mốc so sánh (benchmark; FPP §5.2).
- **Vai trò.** Mô hình không thắng baseline thì không đáng dùng.
- **Điều kiện hợp lệ.** Chỉ dùng số đã có tại gốc. Nghĩa là **độ trễ (lag) phải lớn hơn hoặc bằng tầm xa nhất**.
- **Phân biệt.** Với tầm 168 giờ, "cùng giờ hôm qua" (trễ 24) không hợp lệ. Ví dụ với $h$ = 100, nó cần số của giờ
  $T$ + 76, là giờ nằm sau gốc.

### Kết quả năm 2010 (dự báo cuốn, 46 gốc)

| Mô hình | MAE theo giờ (kWh/giờ) | MAE tổng tuần (kWh/tuần) |
|---|---|---|
| trung bình 4 tuần | **0,490** | 27,9 |
| bảng lịch (trung thực) | 0,508 | **16,4** |
| seasonal naive (tuần trước) | 0,576 | 24,2 |
| trung bình | 0,652 | |
| naive (giờ trước) | 0,770 | |

### Naive (naive method)

- **Ý tưởng.** Tương lai bằng giá trị cuối cùng đã biết.
- **Kiến trúc.** $\hat y_{T+h} = y_T$. Không có tham số.
- **Ưu điểm.** Đơn giản nhất. Tốt khi chuỗi thay đổi chậm và tầm dự báo ngắn.
- **Nhược điểm.** Cùng một số cho cả 168 giờ, bỏ qua mùa vụ. MAE kém nhất (0,770), vì 23:00 Chủ nhật là giờ sắp ngủ,
  không đại diện cho các giờ khác.

### Trung bình (mean method)

- **Ý tưởng.** Tương lai bằng trung bình của toàn bộ lịch sử.
- **Kiến trúc.** $\hat y_{T+h} = \bar y$. Một tham số.
- **Ưu điểm.** Ổn định, không bị nhiễu của một giờ riêng lẻ kéo đi.
- **Nhược điểm.** Bỏ qua mùa vụ. MAE 0,652.

### Seasonal naive (seasonal naive method)

- **Ý tưởng.** Tương lai bằng giá trị cùng thời điểm của chu kỳ trước.
- **Kiến trúc.** $\hat y_{T+h} = y_{T+h-168}$ (chu kỳ tuần, 168 giờ). Không có tham số.
- **Điểm đặc biệt.** Là baseline chuẩn cho dữ liệu có mùa vụ. Từ buổi này, mọi mô hình trong khoá đều phải so với nó.
- **Ưu điểm.** Nắm được mùa vụ ngày và tuần.
- **Nhược điểm.** Chỉ dựa vào một tuần, nên mang cả nhiễu của tuần đó. MAE 0,576.

### Trung bình 4 tuần (seasonal average of 4 cycles)

- **Ý tưởng.** Trung bình cùng thời điểm của 4 chu kỳ gần nhất.
- **Kiến trúc.** $\hat y_{T+h} = \frac14\sum_{k=1}^{4} y_{T+h-168k}$. Không có tham số cần khớp.
- **Ví dụ.** 19:00 thứ Ba của bốn tuần trước là 1,6; 1,2; 1,4; 1,8 → dự báo 1,5 kWh.
- **Ưu điểm.** Giữ mùa vụ tuần, và giảm nhiễu nhờ lấy trung bình 4 số. MAE theo giờ tốt nhất (0,490).
- **Nhược điểm.** Chậm khi mức thay đổi. Ở kỳ nghỉ tháng 8, dự báo chỉ hạ **sau khi** kỳ nghỉ bắt đầu và lên lại chậm.
  Sai số cùng chiều kéo dài nhiều ngày, nên tổng tuần kém (27,9).

### Bảng lịch (calendar profile)

- **Ý tưởng.** Dự báo mỗi giờ bằng trung bình lịch sử của các giờ cùng tuần trong năm, cùng thứ, cùng giờ.
- **Kiến trúc.**
  - Đầu vào: chuỗi theo giờ trước gốc.
  - Tham số: 53 × 7 × 24 = 8.904 ô, mỗi ô là một trung bình.
  - Khớp: tính trung bình từng ô.
  - Dự báo: tra ô tương ứng.
- **Điểm đặc biệt.** Nhớ được mùa vụ năm, ví dụ kỳ nghỉ tháng 8 lặp lại mỗi năm. Trung bình 4 tuần không thấy được mùa
  vụ năm.
- **Ưu điểm.** Nắm cả ba mùa vụ. Chấm theo tổng tuần tốt nhất (16,4).
- **Nhược điểm.**
  - Mỗi ô chỉ có khoảng 3 giờ dữ liệu, nên dễ thuộc lòng cả nhiễu. Chấm theo giờ thua trung bình 4 tuần.
  - Rất dễ cho sai số ảo nếu khớp trên cả giai đoạn chấm (0,380).
- **Khi nào dùng.** Khi quyết định dựa trên tổng tuần, và mùa vụ năm lặp đúng theo lịch.

---

## 5. Chi phí lệch (asymmetric cost) và dự báo phân phối (distributional forecast)

**Kết luận của phần.** Khi thiếu và thừa đắt khác nhau, con số tối ưu không phải dự báo trung bình mà là một quantile.
Có phân phối thì với tỷ lệ chi phí nào cũng đọc ra được quantile tương ứng.

### Phân phối (distribution)

- **Định nghĩa.** Tập các giá trị có thể xảy ra, cùng mức độ thường gặp (frequency) của mỗi giá trị.
- **Ví dụ.** 10 ngày lúc 19 giờ, nhà dùng 7, 5, 9, 6, 8, 12, 6, 9, 7, 8 kWh.
- **Vai trò.** Là đầu vào để chọn con số tối ưu theo chi phí. Buổi 2 học kỹ.

### Quantile và trung vị (median)

- **Định nghĩa.** Quantile mức $p$ là giá trị nhỏ nhất mà ít nhất tỷ lệ $p$ số liệu nhỏ hơn hoặc bằng nó. Trung vị là
  quantile 0,5.
- **Ví dụ.** Xếp tăng 5, 6, 6, 7, 7, 8, 8, 9, 9, 12. Vị trí 0,8 × 10 = 8, nên quantile 0,8 là **9 kWh**.
- **Phân biệt.** `np.quantile` mặc định nội suy (linear interpolation) nên có thể ra số lẻ. Thêm `method="inverted_cdf"` để khớp cách tính tay.

### Dự báo điểm (point forecast) và dự báo phân phối (distributional forecast)

- **Định nghĩa.**
  - **Dự báo điểm**: một con số, ví dụ "120 cái".
  - **Dự báo phân phối**: cả dải giá trị kèm khả năng, ví dụ "100–140 cái: 80%".
- **Vai trò.** Chỉ dự báo phân phối mới phục vụ được mọi tỷ lệ chi phí. Đây là lý do khoá học dạy dự báo phân phối.

### Mức quantile tối ưu (newsvendor problem)

- **Định nghĩa.** Khi mỗi đơn vị thiếu (underage) mất $C_u$ và mỗi đơn vị thừa (overage) mất $C_o$, lượng tối ưu là quantile mức (critical ratio)
  $$p^\ast = \frac{C_u}{C_u + C_o}$$
- **Giải thích.** Tăng lượng mua thêm 1 đơn vị:
  - được lợi $C_u$ ở mỗi ngày đang thiếu;
  - mất $C_o$ ở mỗi ngày đang thừa.

  Dừng lại khi phần lợi không còn lớn hơn phần mất.
- **Ví dụ.** Thiếu 4, thừa 1 → $p^\ast$ = 0,8. Với 10 ngày ở trên:
  - mua 9 kWh tốn 28 đồng, thấp nhất;
  - mua đúng trung bình 7,7 kWh tốn 37,5 đồng.
- **Cách diễn giải.**
  - $C_u > C_o$: $p^\ast$ > 0,5, nên mua **cao hơn** trung vị (bánh mì: hết hàng mất khách).
  - $C_u < C_o$: $p^\ast$ < 0,5, nên mua **thấp hơn** trung vị (bánh ngọt thừa phải bỏ: $C_u$ = 1, $C_o$ = 3 → 0,25).
  - $C_u = C_o$: mua đúng trung vị. Đây cũng là lý do MAE nhắm tới trung vị.
- **Phân biệt.** Đảo $C_u$ và $C_o$ là lỗi hay gặp.

### Kết quả trên dữ liệu thật

Mua "trung bình 4 tuần + 0,455 kWh" cho năm 2010. 0,455 là quantile 0,8 của sai số năm **2009**; không dùng năm được
chấm để chọn con số này.

| Cách mua năm 2010 | Chi phí (đồng/giờ) | MAE (kWh/giờ) | Tỷ lệ giờ bị thiếu |
|---|---|---|---|
| đúng trung bình 4 tuần | 1,213 | **0,490** | 44,0% |
| trung bình 4 tuần + 0,455 kWh | **0,987** | 0,673 | 20,1% |

**Đọc bảng.**

- Dòng 2 rẻ hơn 18,6% dù MAE tệ hơn. Chấm bằng thước đo không khớp chi phí thì sẽ chọn sai.
- Tỷ lệ giờ thiếu 20,1% sát mức 20% mà quantile 0,8 hứa.

![Cộng thêm vào dự báo làm chi phí giảm dù MAE tăng](hinh/chi-phi-bat-doi-xung.png)

**Đọc hình.** Chấm bằng thước đo sai thì sẽ chọn sai.
