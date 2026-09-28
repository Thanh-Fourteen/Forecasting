# Kiểm tra buổi 30 — N-BEATS, N-HiTS, DeepAR, TFT, TiDE

## Nhắc lại khái niệm

**Câu 1.** Dự báo nhu cầu điện 24 giờ tới lúc 00:00. Nhiệt độ **thực** đo ở trạm phải khai là loại covariate nào trong neuralforecast?

- A. `futr_exog`, vì nhiệt độ ảnh hưởng nhu cầu của 24 giờ tới
- B. `hist_exog`, vì lúc 00:00 chỉ có nhiệt độ thực của quá khứ
- C. `stat_exog`, vì nhiệt độ thay đổi chậm
- D. Không được dùng ở đâu cả

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): nhiệt độ thực của các giờ tới chưa đo được lúc 00:00, nên chỉ được dùng cho 168 giờ quá khứ. **A sai**: đó chính là rò rỉ của buổi
này; con số tương lai phải là nhiệt độ **đã dự báo**. **C sai**: biến tĩnh không đổi theo thời gian, như tên vùng. **D sai**: nhiệt độ thực của quá
khứ là thông tin hợp lệ.

</details>

**Câu 2.** Trong N-BEATS, "backcast" của một khối là gì?

- A. Dự báo 24 giờ tới của khối đó
- B. Phần quá khứ mà khối đó giải thích được; khối sau học phần còn lại sau khi trừ đi
- C. Sai số của khối trước
- D. Trọng số chọn biến

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): trong ví dụ 10, 12, 14, khối mức có backcast 12, 12, 12; phần còn lại −2, 0, 2 là việc của khối sau. **A sai**: đó là phần
khối góp vào dự báo, khác backcast. **C sai**: phần còn lại mới là "cái chưa giải thích được", không phải backcast. **D sai**: trọng số chọn biến là
của TFT (mục 4.4).

</details>

**Câu 3.** Vì sao chọn phân phối âm nhị thức thay vì phân phối chuẩn cho số lượt thuê xe mỗi giờ?

- A. Vì nó cho khoảng dự báo hẹp hơn
- B. Vì số đếm không âm và thường có phương sai lớn hơn trung bình; phân phối chuẩn có thể cho cận dưới âm
- C. Vì neuralforecast bắt buộc
- D. Vì nó luôn cho coverage đúng 80%

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): trung bình 2, độ lệch chuẩn 2 theo phân phối chuẩn cho cận dưới khoảng 80% là −0,56 lượt, vô lý. **A sai**: độ rộng tuỳ dữ liệu,
không phải lý do chọn. **C sai**: thư viện có cả hai. **D sai**: chọn đúng loại phân phối không bảo đảm coverage; vẫn phải kiểm (mục 4.3, bài tập 2).

</details>

**Câu 4.** TFT cho trọng số chọn biến "giờ trong ngày" 0,55 ở khung tương lai. Câu nào đúng?

- A. Giờ trong ngày gây ra 55% nhu cầu điện
- B. TFT dựa vào giờ trong ngày nhiều hơn các biến tương lai khác khi dự báo; đó là mô tả mô hình, không phải quan hệ nhân quả
- C. Nhiệt độ vô dụng, nên bỏ
- D. Trọng số này cố định, huấn luyện lại vẫn y nguyên

<details>
<summary>Đáp án</summary>

**B** (mục 4.4). **A sai**: trọng số nói mô hình **dùng** gì, không nói biến **gây ra** gì. **C sai**: trọng số nhỏ không có nghĩa bằng 0, và mục 4.1
cho thấy nhiệt độ vẫn thêm một chút. **D sai**: trọng số đổi theo lần huấn luyện và theo lô dự báo.

</details>

## Vận dụng

**Câu 5.** DeepAR ra phân phối chuẩn trung bình 200 MW, độ lệch chuẩn 15 MW cho giờ tới. Tính khoảng 80%.

<details>
<summary>Đáp án</summary>

200 ± 1,28 × 15 = 200 ± 19,2 → **180,8 tới 219,2 MW** (mục 4.3). Nhầm hay gặp: dùng 1,96, ra khoảng 95% (170,6 tới 229,4).

</details>

**Câu 6.** Khối chọn biến của TFT chấm điểm ba biến là 1, 1, 0. Tính trọng số.

<details>
<summary>Đáp án</summary>

$e^1 \approx 2{,}72$ (hai lần) và $e^0 = 1$, tổng 6,44. Trọng số 2,72/6,44 ≈ **0,42**; **0,42**; 1/6,44 ≈ **0,16** (mục 4.4). Nhầm hay gặp: chia điểm
cho tổng điểm (1/2, 1/2, 0), bỏ mất biến thứ ba hoàn toàn.

</details>

**Câu 7.** Một khối N-HiTS đoán 4 điểm ở giờ 6, 12, 18, 24 là 30, 42, 36, 48 GW. Giờ 15 bao nhiêu?

<details>
<summary>Đáp án</summary>

Giờ 15 nằm giữa giờ 12 và 18 → (42 + 36)/2 = **39 GW** (mục 4.2). Nhầm hay gặp: lấy giá trị giờ 12 hoặc 18 thay vì nội suy.

</details>

**Câu 8.** Mô hình học: nhu cầu = 500 + 20 × nhiệt độ (MW). Ngày mai nhiệt độ thực 25 °C, nhu cầu thực 1.000 MW; nhiệt độ đã dự báo hôm nay 22 °C.
Sai số (thực tế − dự báo) lúc backtest khai nhiệt độ thực là tương lai, và lúc vận hành?

<details>
<summary>Đáp án</summary>

Backtest: 500 + 20 × 25 = 1.000 → sai số **0**. Vận hành: 500 + 20 × 22 = 940 → sai số 1.000 − 940 = **+60 MW** (dự báo thấp hơn thực tế). Chênh = 20 MW
mỗi độ × 3 °C lệch của dự báo nhiệt độ (mục 4.1).

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Một báo cáo viết: "TFT với `futr_exog_list=["nhiet_do_thuc", "gio", "thu"]` đạt MASE 0,49 trên backtest 37 mốc, tốt hơn seasonal naive
51%. Đề nghị thay mô hình hiện tại." Chỉ ra hai lỗi.

<details>
<summary>Đáp án</summary>

(1) **Rò rỉ** (mục 4.1): nhiệt độ thực khai là covariate tương lai, nên con số backtest đẹp hơn thứ mô hình làm được lúc vận hành; phải dùng nhiệt
độ đã dự báo. (2) **Baseline quá yếu** (mục 4.6): chỉ so với seasonal naive. Trên dữ liệu này TFT thua MSTL, LightGBM, N-HiTS và tốn thời gian gấp
9 lần N-HiTS; cũng phải so với dự báo mà vùng điều độ đang dùng (dòng EIA).

</details>

**Câu 10.** Nhìn hình coverage của DeepAR (mục 4.3), một đồng nghiệp nói: "Ở giờ 1 khoảng 80% phủ đúng 81%, vậy khoảng này dùng để dự phòng cả
ngày được." Sai ở đâu?

<details>
<summary>Đáp án</summary>

Coverage phải đọc **theo tầm**: chỉ giờ đầu gần 80%, từ giờ thứ tám trở đi khoảng 80% chỉ phủ 20–30%, tức phần lớn các giờ trong ngày thực tế
nằm ngoài khoảng. Nguyên nhân (mục 4.3): neuralforecast đưa trung bình, không phải mẫu, trở lại làm đầu vào nên khoảng gần như không rộng ra theo
tầm. Không dùng khoảng đó để dự phòng khi chưa hiệu chỉnh.

</details>
