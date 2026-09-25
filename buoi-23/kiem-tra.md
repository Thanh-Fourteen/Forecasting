# Kiểm tra buổi 23 — Gradient boosting chuyên sâu

## Nhắc lại khái niệm

**Câu 1.** Trong gradient boosting, cây thứ hai học cái gì?

- A. Học lại nhãn $y$ từ đầu, trên một nửa dữ liệu khác
- B. Học phần dư: nhãn trừ dự báo hiện tại của các cây trước
- C. Học trung bình của nhãn
- D. Học những dòng mà cây thứ nhất bỏ qua

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): mỗi cây mới học phần còn sai; dự báo mới = dự báo cũ + học suất × lá của cây mới. **A sai**: đó gần với rừng ngẫu nhiên (các
cây học độc lập rồi lấy trung bình). **C sai**: trung bình chỉ là điểm khởi đầu. **D sai**: cây thứ hai dùng mọi dòng, chỉ đổi nhãn thành phần dư.

</details>

**Câu 2.** WRMSSE đặt trọng số cho mỗi mã hàng theo cái gì?

- A. Số món bán trong 28 ngày trước cutoff
- B. Doanh thu (món × giá) trong 28 ngày trước cutoff
- C. Như nhau cho mọi mã
- D. RMSSE của seasonal naive

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): mã mang nhiều tiền hơn thì đoán sai tốn nhiều hơn, nên nặng hơn. **A sai**: mã rẻ bán nhiều món sẽ lấn át mã đắt. **C sai**:
đó là trung bình RMSSE thường, M5 không dùng. **D sai**: RMSSE của seasonal naive không phải trọng số; mẫu số của RMSSE là mức nhảy ngày-qua-ngày.

</details>

**Câu 3.** Vì sao KFold xáo trộn cho điểm CV đáng ngờ trên bảng dự báo bán lẻ này?

- A. Vì KFold chỉ chạy được với 5 fold
- B. Vì phần học chứa những ngày nằm sau ngày bị kiểm, và cột lịch giúp mô hình nhận ra đúng ngày đó
- C. Vì KFold làm mô hình chạy chậm hơn
- D. Vì KFold không dùng được với LightGBM

<details>
<summary>Đáp án</summary>

**B** (mục 4.4): ngày 3/6 bị kiểm mà ngày 2/6, 4/6 nằm trong phần học; với "tuần trong năm", "ngày trong tháng" mô hình mượn được những gì đã
xảy ra ở chính ngày đó với các mã khác. Lúc dự báo thật không có thông tin ấy. **A sai**: số fold tuỳ ý. **C sai**: tốc độ không phải vấn đề.
**D sai**: dùng được về kỹ thuật, chỉ là chấm sai.

</details>

**Câu 4.** Quản lý hỏi: "Vì sao dự báo ngày 1/12 của mã 22659 cao bất thường?" Công cụ nào trả lời đúng câu này?

- A. Tầm quan trọng gain
- B. Tầm quan trọng split
- C. SHAP của đúng dòng đó
- D. Partial dependence của giá

<details>
<summary>Đáp án</summary>

**C** (mục 4.5): SHAP tách **một** dự báo thành mức nền cộng đóng góp từng đặc trưng. **A, B sai**: gain và split là thước đo toàn cục trên mọi
dòng học, không nói gì về một dự báo cụ thể. **D sai**: PD là ảnh hưởng trung bình của một đặc trưng trên nhiều dòng.

</details>

## Vận dụng

**Câu 5.** Nhãn $y = (3, 5, 10, 14)$; cây một câu hỏi tách hai ngày đầu và hai ngày sau; học suất 0,5. Sau cây thứ nhất, dự báo của ngày thứ ba
là bao nhiêu?

- A. 8
- B. 10
- C. 12
- D. 9

<details>
<summary>Đáp án</summary>

**B** (mục 4.1): khởi đầu bằng trung bình 8; phần dư (−5; −3; +2; +6); lá phải = (2 + 6) / 2 = +4; dự báo 8 + 0,5 × 4 = **10**. **A sai**: chưa
cộng cây nào. **C sai**: cộng cả lá, quên nhân học suất. **D sai**: lấy phần dư riêng của ngày 3 (+2) thay cho trung bình của lá.

</details>

**Câu 6.** Ba mã, một cutoff: A có RMSSE 0,8, doanh thu 60; B có RMSSE 1,2, doanh thu 20; C có RMSSE 0,5, doanh thu 20. WRMSSE bằng bao nhiêu?

- A. 0,83
- B. 0,82
- C. 0,90
- D. 0,76

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): trọng số 60/100, 20/100, 20/100; WRMSSE = 0,6 × 0,8 + 0,2 × 1,2 + 0,2 × 0,5 = 0,48 + 0,24 + 0,10 = **0,82**. **A sai**: đó
là trung bình không trọng số (2,5 / 3). **C, D sai**: không khớp phép tính nào đúng.

</details>

**Câu 7.** Mô hình Tweedie. Mức nền (thang log) 3,0; ba đóng góp SHAP +0,5, −0,2, +0,4. Dự báo bao nhiêu món? (Cho sẵn $e^{3{,}7}$ ≈ 40,4;
$e^{3}$ ≈ 20,1; $e^{4{,}1}$ ≈ 60,3.)

- A. 3,7
- B. khoảng 20,8
- C. khoảng 40,4
- D. khoảng 60,3

<details>
<summary>Đáp án</summary>

**C** (mục 4.3, 4.5): điểm thô 3,0 + 0,5 − 0,2 + 0,4 = 3,7; mũ lên $e^{3{,}7}$ ≈ **40,4** món. **A sai**: 3,7 là điểm thô trên thang log, chưa
mũ lên. **B sai**: cộng đóng góp vào số món ($e^3$ + 0,7). **D sai**: bỏ dấu trừ của đóng góp −0,2.

</details>

**Câu 8.** Mô hình LightGBM L2 cho số món bán mỗi ngày trả ra vài dự báo −3 món, và thua cả trung bình 28 ngày gần nhất. Việc nên làm trước tiên?

- A. Cắt dự báo âm về 0 rồi dùng tiếp
- B. Đổi hàm mất mát sang Tweedie (hoặc Poisson): đoán trên thang log, dự báo luôn dương, chấm sai số theo tỷ lệ
- C. Tăng số cây gấp đôi
- D. Chuyển sang KFold để tune kỹ hơn

<details>
<summary>Đáp án</summary>

**B** (mục 4.3): dữ liệu đếm nhiều số 0 và đuôi dài; ở đây đổi L2 sang Tweedie giảm WRMSSE từ 0,709 xuống 0,680. **A sai**: che triệu chứng,
mô hình vẫn học sai cỡ sai số. **C sai**: nhiều cây hơn vẫn tối ưu cùng hàm mất mát sai. **D sai**: KFold làm chấm sai thêm (mục 4.4).

</details>

## Đọc bảng kết quả, tìm chỗ sai

**Câu 9.** Bảng tune bằng Optuna (50 lần thử mỗi cách chia):

| Bộ tham số | RMSE KFold | RMSE CV thời gian | WRMSSE backtest |
|---|---|---|---|
| chọn bằng KFold | 69,26 | 51,94 | 0,678 |
| chọn bằng CV thời gian | 69,87 | 51,76 | 0,669 |

Câu nào đọc bảng **sai**?

- A. KFold và CV thời gian chọn hai bộ khác nhau, mỗi cách chấm bộ của mình tốt hơn
- B. Backtest trên tương lai đứng về phía bộ chọn bằng CV thời gian
- C. CV thời gian cho RMSE khoảng 52, KFold khoảng 69, vậy CV thời gian là cách chấm lạc quan hơn
- D. Nên dùng bộ chọn bằng CV thời gian

<details>
<summary>Đáp án</summary>

**C** là câu sai (mục 4.4): hai cột RMSE chấm trên những ngày khác nhau (KFold kiểm rải khắp hai năm, gồm cả mùa Giáng sinh 2010; CV thời gian
kiểm ba tháng cuối phần học), nên không so trực tiếp được. Chỉ so được các dòng trong **cùng** một cột. **A đúng**: 69,26 < 69,87 và 51,76 <
51,94. **B đúng**: 0,669 < 0,678. **D đúng**: cách chia giống lúc dùng thật, và backtest xác nhận.

</details>

**Câu 10.** Đồng nghiệp xem hình partial dependence của giá (mô hình không ràng buộc): dự báo trung bình tăng từ 21,75 lên 23,11 món khi giá
trung bình tăng từ £0,32 lên £2,79. Họ đề xuất: "tăng giá các mã rẻ lên khoảng £2,8 sẽ bán thêm hơn 1 món mỗi ngày". Chỗ sai chính là gì?

- A. Không sai: PD đo đúng tác động của việc tăng giá
- B. PD mô tả mô hình phản ứng thế nào, và giá ở đây khác nhau chủ yếu giữa các mã; mô hình có thể gán khác biệt về loại hàng cho giá
- C. Phải đọc PD trên thang log
- D. Hình thiếu đường seasonal naive

<details>
<summary>Đáp án</summary>

**B** (mục 4.6): PD chỉ cho biết mô hình đổi dự báo thế nào khi ta đổi cột giá, không cho biết khách mua thế nào khi cửa hàng đổi giá. Cần
ràng buộc đơn điệu để mô hình hợp lý, và phương pháp nhân quả (buổi 38–39) để đo tác động thật. **A sai**: vì lý do trên. **C sai**: trục dọc
của PD là số món, đọc trực tiếp được. **D sai**: PD không phải hình so độ chính xác.

</details>
