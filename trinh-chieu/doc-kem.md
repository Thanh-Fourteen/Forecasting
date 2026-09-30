# Dữ liệu cho dự báo — bài đọc kèm slide (buổi 1–15)

Mỗi mục dưới đây ứng với một slide cùng số. Slide chỉ ghi từ khoá, còn bài này giải thích vì sao và đọc hình ra sao.
Mọi con số lấy từ lần chạy thật trong tài liệu của buổi ghi cạnh tiêu đề slide. Đọc lần lượt, hoặc nhảy tới số slide đang chiếu.

## 1. Dữ liệu cho dự báo
<!-- ma: tieu-de -->

Bộ slide tóm 15 buổi đầu của khoá: định nghĩa, các vấn đề dữ liệu hay gặp, dấu hiệu để nhận ra, cách kiểm, cách sửa, và
quy trình tiền xử lý hoàn chỉnh. Buổi 1–3 là nền móng, buổi 4–13 là hiểu và chuẩn bị dữ liệu (phần làm kỹ nhất), buổi
14–15 là đánh giá trung thực: không có nó thì không biết tiền xử lý có giúp thật hay không.

## 2. Hôm nay nói gì: sáu phần
<!-- ma: ban-do -->

- **A. Khái niệm nền** (buổi 1–13): mỗi khái niệm một slide, gồm là gì, một ví dụ có số, và để làm gì.
- **B. Vấn đề dữ liệu** (buổi 3–13): mỗi vấn đề một hình thật, kèm ba thẻ dấu hiệu → kiểm bằng → cách sửa.
- **C. Bảng tra, mười chỗ hay hiểu nhầm, từ điển Việt – Anh**: gom lại để tra nhanh.
- **D. Đánh giá trung thực** (buổi 14–15): phần dư, chỉ số, cách chia dữ liệu theo thời gian, rolling origin, Diebold–Mariano.
- **E. Quy trình tiền xử lý**: bước nào làm một lần, bước nào làm lại ở mỗi mốc cắt.
- **F. Dữ liệu và phía trước**: bộ dữ liệu đã dùng, bảng tra theo buổi, phần tiền xử lý còn ở các buổi sau.

## 3. 15 buổi móng của lộ trình 44 buổi
<!-- ma: lo-trinh -->

Khoá có 44 buổi, đi từ thống kê cổ điển tới deep learning, foundation model và production. 15 buổi đầu là phần móng mà
mọi buổi sau đứng lên trên. Hai buổi đánh giá (14–15) được gộp vào đây vì mọi bước tiền xử lý có "học" từ dữ liệu, như giá
trị để điền hay tham số biến đổi, chỉ đúng khi biết nó được học trên đoạn nào.

## 4. Nhìn trước, xử lý sau, kiểm lại cuối
<!-- ma: nhip -->

Cả giai đoạn dữ liệu đi theo một nhịp: **nhìn** (vẽ đủ biểu đồ) → **đặt giả thuyết** (nghi điều gì) → **kiểm bằng con số**
(đếm, đo, chạy test) → **xử lý** (sửa và ghi lại đã sửa gì) → **kiểm lại** (so trước và sau). Bài học chính: không xoá, không
điền khi chưa biết nguyên nhân. Một con số lạ có thể là lỗi, cũng có thể là sự kiện thật cần giữ.

## 5. Phần A: Khái niệm nền
<!-- ma: phan-a -->

Phần A dựng từ vựng chung, đi theo thứ tự buổi 1 → 13. Năm trang đầu là "Từ nền": những từ dùng nhiều mà không có slide riêng. Sau đó mỗi slide một khái niệm, trả lời bốn câu: để làm gì, là gì, con số cao hay thấp nghĩa là gì, và một ví dụ có số.

## 6. Từ nền 1/5: dự báo, sai số, dữ liệu
<!-- ma: tu-nen-1 -->

Năm trang "Từ nền" gom những từ các slide sau dùng mà không có slide riêng. Mỗi dòng gồm từ đó là gì và một ví dụ nhỏ, lấy từ bảng
"Từ mới" của từng buổi. Gặp một từ lạ ở slide nào thì quay lại đây tra.

Trang 1 là các từ về dự báo và sai số. **Sai số = thực tế − dự báo**, nên sai số dương nghĩa là dự báo thấp hơn thực tế. Quy ước
này dùng cho cả khoá.

| Từ | Là gì | Ví dụ |
|---|---|---|
| mô hình, tham số | Cách tính ra dự báo; tham số là các con số bên trong nó | “Mai = trung bình 7 ngày qua” |
| khớp (fit), học | Chọn các tham số từ dữ liệu quá khứ | Tính trung bình 7 ngày từ lịch sử |
| phần học / kỳ chấm | Đoạn dùng để khớp / đoạn giữ riêng để chấm | Học 2009, chấm 2010 |
| học thuộc (overfit) | Khớp quá sát phần học, dự báo mới thì tệ | Thuộc đề cũ: 10 điểm; đề mới: 6 |
| sai số dự báo | Thực tế − dự báo; dương là dự báo thấp | 1,7 − 1,5 = +0,2 |
| MAE | Trung bình độ lớn sai số, bỏ dấu | Sai số +2 và −4 → 3 |
| RMSE | Căn của trung bình sai số bình phương; phạt nặng sai số lớn | Sai số 1 và −3 → 2,24 |
| MAPE | Trung bình |sai số| chia thực tế, tính bằng % | Thật 100, dự báo 90 → 10% |
| NaN | Ô “không biết” của pandas, khác với số 0 | Không đo lúc 01:00 → NaN |
| backtest | Đứng ở nhiều mốc trong quá khứ, dự báo, rồi so với thực tế | 4 thứ Hai, mỗi lần dự báo 24 giờ |
| feature / mục tiêu | Cột đầu vào mô hình dùng / con số cần dự báo | Điện 2 giờ qua / điện giờ tới |
| lag, rolling | Giá trị k bước trước; thống kê trên w điểm gần nhất | lag_7 thứ Hai = thứ Hai tuần trước |
| trung bình trượt | Thay mỗi điểm bằng trung bình với các điểm lân cận | 50, 2, 51 → quanh 2 là 34,3 |

## 7. Từ nền 2/5: thống kê
<!-- ma: tu-nen-2 -->

Các từ thống kê dùng ở buổi 2, 8, 9, 14. **Mẫu** là số liệu đang có trong tay; **tổng thể** là mọi giá trị nếu đo mãi, và "trung
bình thật" là trung bình của tổng thể. Mọi khoảng tin cậy và p-value đều là cách đoán về tổng thể từ một mẫu.

| Từ | Là gì | Ví dụ |
|---|---|---|
| mẫu / tổng thể | Số liệu đang có / mọi giá trị nếu đo mãi | 9 giờ 17h đang có / mọi giờ 17h |
| phân phối chuẩn | Hình chuông đối xứng; 95% nằm trong trung bình ± 1,96 s | 100 ± 1,96 × 10 → 80,4–119,6 |
| histogram | Cột đếm số giá trị rơi vào mỗi khoảng | 0–9: 6 số; 10–19: 2 số |
| i.i.d. | Các lần độc lập và cùng phân phối | Các lần tung một xúc xắc |
| mức ý nghĩa α | Ngưỡng chọn trước; p nhỏ hơn thì bác bỏ H0 | Hay dùng 0,05 |
| sai số chuẩn | Độ lệch chuẩn của chính một con số ước lượng | Trung bình 25 giờ: 181 / √25 ≈ 36 |
| tương quan r | Số từ −1 tới 1: hai biến cùng tăng giảm theo đường thẳng tới đâu | 1, 2, 3 và 2, 4, 6 → r = 1 |
| r₁, r_k | Tự tương quan ở trễ 1, ở trễ k | r₂₄ = 0,81 với lượt thuê xe |
| hồi quy đơn, R² | Đường y = a + b·x khớp nhất; R² là phần dao động nó giải thích | R² = 0,8: giải thích 80% |
| Durbin–Watson | Đo phần dư hồi quy có tự tương quan: gần 2 là không, gần 0 là mạnh | Gần 0 → nghi tương quan giả |
| mutual information | Biết x thì bớt được bao nhiêu điều chưa biết về y; bắt cả quan hệ cong | Bằng 0 khi độc lập |
| CV | Độ lệch chuẩn chia trung bình | Trung bình 100, s = 10 → 0,1 |
| Jarque–Bera | Kiểm định số liệu có gần hình chuông không; p nhỏ là không | Phần dư có vài cú rơi lớn |

## 8. Từ nền 3/5: biến đổi, dừng, bất thường
<!-- ma: tu-nen-3 -->

Các từ về biến đổi, tính dừng và bất thường, dùng ở buổi 5, 6, 7, 11.

| Từ | Là gì | Ví dụ |
|---|---|---|
| log, exp | log y: e mũ mấy thì bằng y; exp làm ngược lại | log 100 = 4,605 |
| CPI, năm gốc | Chỉ số giá một giỏ hàng; năm lấy làm mốc sức mua | CPI 100 → 125: giá tăng 25% |
| điều chỉnh lịch | Chia tổng tháng cho số ngày để tháng dài ngắn so được | 280 tỷ / 28 ngày = 10 tỷ/ngày |
| log-normal | y = exp(w) với w hình chuông: luôn dương, lệch phải | Doanh số, giá nhà |
| Yeo-Johnson | Biến thể Box-Cox nhận cả số 0 và số âm | Chuỗi % tăng trưởng có tháng âm |
| nhiễu trắng | Không tự tương quan ở trễ nào: quá khứ không giúp đoán | Kết quả tung xúc xắc |
| random walk | Giá trị mới = giá trị cũ + một bước ngẫu nhiên | Tung đồng xu rồi bước tới, lùi |
| khử xu hướng | Lấy chuỗi trừ đường xu hướng | 30 − 24,5 = 5,5 |
| LOESS | Làm trơn cục bộ: mỗi điểm nhìn lân cận, điểm gần nặng hơn | Lõi của STL |
| robust | Cách ước lượng ít bị vài điểm bất thường kéo lệch | robust=True trong STL |
| biến giả | Cột 0/1 báo mốc nào thuộc một sự kiện | covid = 1 từ 3/2020 tới 6/2021 |
| winsorize | Kéo giá trị bị gắn cờ về mức hợp lý (trung vị địa phương), không xoá | 50 → 12 |
| MAD | Trung vị của khoảng cách tới trung vị | Ngoại lai không kéo được |

## 9. Từ nền 4/5: tần số và bộ lọc
<!-- ma: tu-nen-4 -->

Các từ về tần số và bộ lọc của buổi 12. Hai câu hỏi đầu tiên với mọi bộ lọc:

- Nó có nhìn tương lai không (trailing hay centered)?
- Nó trễ bao nhiêu bước?

| Từ | Là gì | Ví dụ |
|---|---|---|
| bộ lọc | Phép biến một chuỗi thành chuỗi khác, thường để làm trơn | Trung bình trượt 3 điểm |
| trailing / centered | Chỉ nhìn các điểm trước / lấy cả trước lẫn sau | Centered dùng số tương lai |
| trễ (pha) | Đầu ra bộ lọc chạy sau tín hiệu thật bao nhiêu bước | Trung bình 13 điểm trễ 6 bước |
| tần số lấy mẫu f_s | Số mẫu mỗi đơn vị thời gian | 10 phút một mẫu: 6 mẫu/giờ |
| tần số Nyquist | Tần số cao nhất còn thấy đúng: f_s / 2 | 6 mẫu/giờ → 3 vòng/giờ |
| hạ mẫu | Giảm tần số lấy mẫu | Từ 10 phút sang 1 giờ |
| lọc thông thấp | Giữ dao động chậm, bỏ dao động nhanh | Lọc trước khi hạ mẫu |
| EWMA | Trung bình trượt hàm mũ: điểm mới nặng hơn điểm cũ | z_t = α·y_t + (1 − α)·z_(t−1) |
| Savitzky–Golay | Khớp đa thức bậc thấp quanh mỗi điểm | Nhìn cả hai phía: không nhân quả |
| Butterworth | Bộ lọc cắt tần số theo một ngưỡng | Bản nhân quả trễ 19 bước |
| Kalman filter / smoother | Ước lượng tín hiệu ẩn; filter dùng quá khứ, smoother dùng cả chuỗi | Smoother không nhân quả |
| sosfilt / sosfiltfilt | Chạy bộ lọc xuôi thời gian / xuôi rồi ngược | sosfiltfilt nhìn tương lai |
| tín hiệu / nhiễu | Phần có quy luật cần giữ / phần ngẫu nhiên | Nhịp ngày / bật tắt ấm đun |

## 10. Từ nền 5/5: làm sạch, feature, đánh giá
<!-- ma: tu-nen-5 -->

Các từ về làm sạch dữ liệu, feature và đánh giá, dùng ở buổi 10, 13, 15.

| Từ | Là gì | Ví dụ |
|---|---|---|
| ép kiểu số | Đổi cột đọc thành chữ về số (to_numeric) | “12,5” → 12.5; “(S)” → NaN |
| nội suy tuyến tính, ffill | Nối thẳng hai điểm hai bên lỗ / chép giá trị trước đó | 10, ?, 14 → 12 / 10 |
| cờ chất lượng | Mã nguồn gắn kèm số đo: qua kiểm tra hay đáng ngờ | GHCNh: mã 2 = đáng ngờ |
| độ phân giải | Bước nhỏ nhất giữa hai giá trị cảm biến ghi được | Nhiệt độ số nguyên: 1 °C |
| cảm biến kẹt | Cảm biến ghi lặp một giá trị nhiều giờ liền | 26,0 suốt 33 giờ |
| scaler | Trừ trung bình, chia độ lệch chuẩn cho từng cột (StandardScaler) | Phải fit trên phần học |
| target encoding | Thay một nhóm bằng trung bình mục tiêu của nhóm | Thứ Bảy → doanh thu TB các thứ Bảy |
| biến ngoại sinh | Biến ngoài chuỗi, dùng làm feature | Nhiệt độ khi dự báo tải điện |
| ex-ante / ex-post | Chỉ dùng thông tin có lúc dự báo / dùng cả số thật về sau | Nhiệt độ dự báo / nhiệt độ đo |
| point-in-time | Dùng số liệu đúng như lúc đó, không dùng bản đã sửa về sau | GDP bản công bố đầu tiên |
| hold-out | Đoạn tương lai giữ riêng, chỉ chấm một lần | Quý 4 năm 2024 |
| tune | Thử nhiều cách đặt tham số, giữ cách sai ít nhất | Thử 11 giá trị w |
| rừng ngẫu nhiên | Nhiều cây quy tắc “nếu… thì…”, lấy trung bình; rất giỏi nhớ | 200 cây |

## 11. Dự báo là điều sẽ xảy ra, không phải điều muốn
<!-- ma: du-bao-la-gi -->

*Tiếng Anh: forecast vs goal vs plan · forecastability*

Có ba thứ hay bị gộp làm một:

- **Dự báo**: điều gì *sẽ* xảy ra.
- **Mục tiêu**: điều ta *muốn*.
- **Kế hoạch**: điều ta *làm* để tới gần mục tiêu.

Ví dụ quán cà phê: dự báo tuần tới bán khoảng 1.900 ly, mục tiêu là 2.500 ly, kế hoạch là chạy khuyến mãi và đặt thêm hạt. Nếu sếp
muốn 2.500 nên bảo "dự báo 2.500", kho sẽ đặt nguyên liệu cho 2.500 ly. Tuần đó bán 1.900, thừa 600 ly, và không ai còn biết dự báo
đúng hay sai. Dự báo phải trung thực; muốn đạt mục tiêu thì sửa kế hoạch, đừng sửa dự báo.

Một thứ dự báo được tới đâu phụ thuộc bốn điều:

1. Hiểu cái gì tác động tới nó.
2. Có nhiều dữ liệu.
3. Tương lai giống quá khứ.
4. Chính lời dự báo không làm nó đổi đi.

Điện của một hộ ngày mai thoả cả bốn nên đoán được rất sát. Tỷ giá tuần sau chỉ thoả điều 2: người ta mua bán theo dự báo, nên dự báo
tự làm mình sai.

## 12. Đứng ở gốc, chỉ thấy quá khứ
<!-- ma: goc-tam -->

*Tiếng Anh: forecast origin (cutoff) · forecast horizon h*

**Gốc dự báo** là thời điểm ra dự báo; **tầm h** là dự báo xa bao nhiêu bước. Đứng ở thứ Hai 00:00 dự báo 168 giờ tới thì
h chạy từ 1 tới 168. Trong hình, bên trái vạch cam là những gì đã biết, dải xanh bên phải là phần phải đoán. Mọi quy tắc
chống rò rỉ về sau đều quy về câu này: chỉ được dùng thứ nằm bên trái gốc.

## 13. Code: đổi phút ra kWh/giờ, tìm nhịp
<!-- ma: code-b01-mua-vu -->

Biến số đo từng phút thành kWh mỗi giờ, rồi thấy nhịp ngày và tuần làm điện dự báo được.

```python
import pandas as pd

df = pd.read_csv("dien-mot-ho.zip", sep=";", na_values="?",
                 usecols=["Date", "Time", "Global_active_power"])
t = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
phut = pd.Series(df["Global_active_power"].to_numpy(), index=t)
# TB kW trong một giờ = số kWh của giờ đó; thiếu quá nửa thì để trống
gio = phut.resample("h")
s = gio.mean().where(gio.count() >= 30)
theo_gio = s.groupby(s.index.hour).mean()       # TB theo giờ trong ngày
print(theo_gio.idxmin(), theo_gio.idxmax())     # giờ thấp nhất, cao nhất
ngay_thuong = s[s.index.dayofweek < 5].mean()   # thứ Hai tới thứ Sáu
cuoi_tuan = s[s.index.dayofweek >= 5].mean()    # thứ Bảy, Chủ nhật
```

*Rút gọn từ buoi-01/tu-hoc.ipynb, phần 0 và 1.*

**Thư viện và hàm:**

- `resample("h").mean()` (pandas): Gom các số đo trong cùng một giờ lại, lấy trung bình.
- `groupby(...).mean()` (pandas): Chia dữ liệu thành nhóm (ví dụ theo giờ), tính trung bình mỗi nhóm.
- `idxmin() / idxmax()` (pandas): Cho biết nhãn (ở đây là giờ) nơi giá trị nhỏ nhất, lớn nhất.

**Từng bước:**

- Dòng 3–6: Đọc số đo từng phút, gắn mốc thời gian.
- Dòng 8–9: Gộp về giờ; giờ thiếu hơn 30 phút để trống.
- Dòng 10–11: Trung bình theo giờ trong ngày, tìm đáy, đỉnh.
- Dòng 12–13: So ngày thường với cuối tuần.

**Kết quả:** Thấp nhất lúc 4h, cao nhất lúc 20h; cuối tuần dùng nhiều hơn ngày thường. Nhịp lặp đều này là mùa vụ.

## 14. Mô hình học từ phần học, bị chấm ở kỳ chấm
<!-- ma: mo-hinh -->

*Tiếng Anh: model · parameter · fit · training set · test period · overfitting*

**Mô hình** là một cách tính ra dự báo; **tham số** là các con số bên trong nó. "Mai bằng trung bình 7 ngày qua" là một mô hình có
một tham số là số 7. **Khớp** (fit, hay "học") là chọn tham số từ dữ liệu.

Dữ liệu chia làm hai đoạn:

- **Phần học** là đoạn mô hình được thấy, dùng để khớp.
- **Kỳ chấm** là đoạn giữ riêng, chỉ dùng để chấm, và nằm sau gốc dự báo.

Sai số đo trên phần học gọi là **phần dư**. Nó luôn đẹp hơn sai số thật, vì mô hình đủ nhiều tham số có thể khớp gần hoàn hảo
những gì đã thấy mà dự báo cái mới vẫn tệ. Hiện tượng này gọi là **học thuộc** (overfit), giống thuộc lòng đề cũ: thi lại đúng đề
được 10 điểm, đề mới chỉ 6. Vì vậy mọi chỉ số chính xác trong khoá đều tính trên kỳ chấm; phần dư chỉ dùng để chẩn đoán.

## 15. Điền 6 ô trước khi mở dữ liệu
<!-- ma: phieu-6-o -->

*Tiếng Anh: forecasting problem statement · decision · target variable · granularity*

Trước khi mở dữ liệu, điền phiếu bài toán 6 ô. Ví dụ là một công ty mua trước điện cho một khu dân cư:

1. **Quyết định**: ai dùng dự báo làm gì, bao lâu một lần. Ví dụ: cuối Chủ nhật đặt mua điện theo giờ cho 7 ngày tới.
2. **Biến mục tiêu**: đo cái gì, đơn vị nào. Ví dụ: kWh mỗi giờ.
3. **Tầm dự báo**: 1–168 giờ, tính từ 00:00 thứ Hai.
4. **Độ chi tiết**: chấm theo giờ, cho cả khu.
5. **Mốc cắt dữ liệu**: lúc dự báo đã biết gì. Ví dụ: số đo tới 23:59 Chủ nhật, và thời tiết *dự báo* (chưa có thời tiết thật).
6. **Chi phí sai hai chiều**: mỗi kWh thiếu mất khoảng 4 đồng, mỗi kWh thừa mất khoảng 1 đồng.

Ô 4 quyết định cách chấm, còn ô 6 quyết định nên báo con số nào (quantile nào).

## 16. 0,38 là tốt hay xấu? Phải có baseline
<!-- ma: baseline -->

*Tiếng Anh: baseline · naive · seasonal naive · drift*

Một mô hình báo sai số 0,38 thì chưa nói được gì, vì không có gì để so. **Baseline** là cách dự báo đơn giản nhất làm mốc:
**naive** lấy giá trị cuối, **seasonal naive** lấy giá trị cùng vị trí ở mùa trước, **mean** lấy trung bình, **drift** kéo dài
đường nối điểm đầu và điểm cuối. Với chuỗi 10, 14, 12, 16, 14, 18 và mùa dài 2 bước, naive dự báo 18; 18 còn seasonal
naive dự báo 14; 18. Trong hình (một chuỗi M4 theo ngày), seasonal naive thắng vì bắt được nhịp tuần. Nhưng trên cả tập M4 theo
ngày, naive (MASE 0,835) và drift (0,810) lại thắng seasonal naive (1,077). Vì vậy quy tắc của khoá là: mô hình phải thắng **cả
bốn** baseline trên backtest, và bảng kết quả luôn có seasonal naive.

Độ trễ của baseline phải ít nhất bằng tầm dự báo, ở mọi h. Dự báo 7 ngày tới mà dùng "cùng giờ hôm qua" là đã dùng số chưa có
tại gốc; phải dùng "cùng giờ tuần trước" (trễ 168 giờ).

## 17. Code: bốn baseline
<!-- ma: code-b14-baseline -->

Bốn câu đoán đơn giản nhất về tương lai; mọi mô hình phải thắng cả bốn.

```python
import numpy as np

def bl_trung_binh(y, tam=14):
    return np.repeat(float(np.mean(y)), tam)       # mức trung bình

def bl_naive(y, tam=14):
    return np.repeat(float(y[-1]), tam)            # giá trị cuối

def bl_naive_mua_vu(y, tam=14, m=7):
    mua = y[-m:]                                   # vòng mùa vụ vừa qua
    return np.array([mua[i % m] for i in range(tam)], dtype=float)

def bl_drift(y, tam=14):
    doc = (y[-1] - y[0]) / (len(y) - 1)            # độ dốc đầu tới cuối
    return y[-1] + doc * np.arange(1, tam + 1)
```

*Rút gọn từ buoi-14/dap-an/danh_gia.py.*

**Thư viện và hàm:**

- `np.repeat` (numpy): Lặp một con số thành mảng dài tam phần tử.
- `y[-m:]` (numpy): Lấy m giá trị cuối của mảng: một vòng mùa vụ.
- `np.arange(1, tam + 1)` (numpy): Dãy 1, 2, …, tam: số bước đi tiếp theo đường thẳng.

**Từng bước:**

- Dòng 3–4: Lặp mức trung bình cả lịch sử 14 lần.
- Dòng 6–7: Lặp giá trị cuối cùng 14 lần.
- Dòng 9–11: Lặp lại tuần vừa qua, m = 7 ngày.
- Dòng 13–15: Kéo dài đường thẳng nối điểm đầu và cuối.

**Kết quả:** MASE trung vị trên 1.000 chuỗi M4 theo ngày: trung bình 8,85; naive 0,835; seasonal naive 1,077; drift 0,810.

## 18. Bốn baseline, tính bằng tay
<!-- ma: bon-baseline -->

*Tiếng Anh: mean · naive · seasonal naive · drift*

Bốn baseline, mỗi cái là một giả định đơn giản về tương lai. Tính tay trên chuỗi 10, 14, 12, 16, 14, 18 với mùa dài m = 2, dự báo 2
bước tới:

| Baseline | Giả định | Cách tính | Dự báo |
|---|---|---|---|
| mean | tương lai quanh trung bình cũ | 84 / 6 = 14 | 14; 14 |
| naive | tương lai giống điểm cuối | lấy số cuối | 18; 18 |
| seasonal naive | lặp lại mùa trước | lấy cùng vị trí mùa trước | 14; 18 |
| drift | đi tiếp theo độ dốc cũ | (18 − 10) / 5 = 1,6 mỗi bước | 19,6; 21,2 |

Hai quy tắc:

- Độ trễ của baseline phải ít nhất bằng tầm dự báo, ở mọi h. Dự báo 7 ngày tới thì không dùng "cùng giờ hôm qua", vì giờ đó chưa có
  tại gốc; dùng "cùng giờ tuần trước".
- Mô hình phải thắng cả bốn, vì baseline thắng không phải lúc nào cũng là seasonal naive.

## 19. Code: MAE và bốn baseline
<!-- ma: code-b01-baseline -->

Viết bốn cách dự báo đơn giản làm mốc, để biết một con số MAE là tốt hay xấu.

```python
import numpy as np

TAM = 168                                    # dự báo 168 giờ = 7 ngày
def mae(y, du_bao):
    y, du_bao = np.asarray(y, float), np.asarray(du_bao, float)
    co = ~np.isnan(y)                        # bỏ giờ không có số đo
    return float(np.mean(np.abs(y[co] - du_bao[co])))
# ls: lịch sử tới gốc dự báo, chuỗi kWh theo giờ
BASELINE = {
    "giờ trước": lambda ls: np.full(TAM, ls.iloc[-1]),
    "trung bình": lambda ls: np.full(TAM, ls.mean()),
    "tuần trước": lambda ls: ls.iloc[-TAM:].to_numpy(),
    "trung bình 4 tuần": lambda ls: ls.iloc[-4 * TAM:].to_numpy()
                                      .reshape(4, TAM).mean(axis=0),
}
```

*Rút gọn từ buoi-01/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `np.abs(...).mean()` (numpy): Bỏ dấu từng sai số rồi lấy trung bình: chính là MAE.
- `iloc[-TAM:]` (pandas): Lấy TAM phần tử cuối của chuỗi theo vị trí, tức tuần gần nhất.
- `reshape(4, TAM).mean(axis=0)` (numpy): Xếp dãy thành bảng 4 hàng, lấy trung bình từng cột.

**Từng bước:**

- Dòng 4–7: MAE: trung bình độ lệch, bỏ giờ trống.
- Dòng 10: Naive: lặp lại số cuối cùng đã biết.
- Dòng 11: Trung bình mọi giờ đã biết.
- Dòng 12: Seasonal naive: cùng giờ tuần trước.
- Dòng 13–14: Xếp 4 tuần thành 4 hàng, lấy TB theo cột.

**Kết quả:** Chấm cuốn năm 2010: trung bình 4 tuần 0,490; tuần trước 0,576; trung bình 0,652; giờ trước 0,770 kWh/giờ.

## 20. Nhìn trộm đáp án thì sai số đẹp giả
<!-- ma: sai-so-ao -->

*Tiếng Anh: in-sample error · rolling forecast*

**Sai số ảo** là sai số đo trên chính dữ liệu đã dùng để dựng dự báo, nên đẹp hơn thật. Trong hình, cùng một mô hình "bảng
lịch": khi bảng được tính cả trên giờ đang chấm thì MAE (sai số tuyệt đối trung bình) là 0,380 và đứng đầu. Chấm trung
thực thì MAE là 0,508, thua cả cách "trung bình 4 tuần". Cách chấm đúng là **dự báo cuốn**, ở slide ngay sau.

Phép thử rẻ nhất: đổi số đo ở giai đoạn chấm rồi chạy lại. Dự báo trung thực không được đổi theo; nếu đổi, mô hình đã nhìn thấy đáp án.

## 21. Dự báo cuốn: chấm như lúc dùng thật
<!-- ma: du-bao-cuon -->

*Tiếng Anh: rolling forecast · rolling origin · out-of-sample*

**Dự báo cuốn** là cách chấm đúng như lúc dùng thật:

1. Chọn một gốc dự báo, ví dụ 00:00 thứ Hai.
2. Dựng dự báo chỉ từ dữ liệu trước gốc; tuần sắp đoán bị giấu đi.
3. Dự báo 168 giờ tới, rồi mới mở số đo thật để tính sai số.
4. Dời gốc sang thứ Hai sau và làm lại. Cuối cùng lấy trung bình sai số của mọi tuần.

Trong hình, mỗi hàng là một gốc: phần xám là dữ liệu được dùng, ô xanh là tuần được dự báo và chấm; xuống mỗi hàng, gốc dời thêm
một tuần. Buổi 1 làm vậy với 46 thứ Hai năm 2010.

Làm như vậy trên quá khứ gọi là **backtest**. Buổi 15 tổng quát nó thành **rolling origin**, với các lựa chọn học trên đoạn nào
(expanding hay sliding), bỏ trống bao nhiêu (gap), và học lại bao lâu một lần (refit).

## 22. Code: bảng lịch và dự báo cuốn
<!-- ma: code-b01-du-bao-cuon -->

Chấm như ngoài đời: mỗi tuần chỉ khớp mô hình trên dữ liệu trước gốc dự báo.

```python
import pandas as pd
TAM = 168
def khoa(t):                                 # (tuần trong năm, thứ, giờ)
    return [t.isocalendar().week.to_numpy(), t.dayofweek.to_numpy(),
            t.hour.to_numpy()]
def bang_lich(ls):                           # mỗi ô một trung bình
    return ls.groupby(khoa(ls.index)).mean()
def du_bao_lich(bang, t):
    return bang.reindex(pd.MultiIndex.from_arrays(khoa(t))).to_numpy()
def du_bao_cuon(chuoi, moc="2010-01-04"):
    phan = []
    for goc in pd.date_range(moc, chuoi.index[-TAM], freq=f"{TAM}h"):
        t = pd.date_range(goc, periods=TAM, freq="h")
        bang = bang_lich(chuoi[chuoi.index < goc])   # CHỈ quá khứ
        phan.append(pd.Series(du_bao_lich(bang, t), index=t))
    return pd.concat(phan)
```

*Rút gọn từ buoi-01/tu-hoc.ipynb, phần 3 và 4.*

**Thư viện và hàm:**

- `groupby([...]).mean()` (pandas): Nhóm theo nhiều khoá cùng lúc, mỗi tổ hợp ra một trung bình.
- `reindex(MultiIndex)` (pandas): Tra bảng theo danh sách khoá; khoá không có thì ra NaN.
- `pd.date_range` (pandas): Sinh dãy mốc thời gian cách đều, ví dụ mỗi 168 giờ một gốc.

**Từng bước:**

- Dòng 3–7: Bảng lịch: TB theo tuần, thứ, giờ.
- Dòng 8–9: Tra bảng cho các giờ cần dự báo.
- Dòng 12–13: Mỗi thứ Hai là một gốc, dự báo 168 giờ.
- Dòng 14: Khớp bảng chỉ bằng dữ liệu trước gốc.
- Dòng 15–16: Ghép dự báo mọi tuần để chấm.

**Kết quả:** Bảng lập từ cả 4 năm cho MAE 0,380 (sai số ảo). Chấm cuốn 46 tuần: 0,508, thua trung bình 4 tuần (0,490).

## 23. Chấm theo giờ hay theo tuần: thứ hạng đảo
<!-- ma: do-chi-tiet -->

*Tiếng Anh: granularity · temporal aggregation · evaluation level*

Cùng ba cách dự báo nhưng chấm ở hai mức thì thứ hạng đảo ngược:

| Cách dự báo | MAE theo giờ (kWh/giờ) | MAE tổng tuần (kWh/tuần) |
|---|---|---|
| Trung bình 4 tuần | 0,490 | 27,9 |
| Bảng lịch | 0,508 | 16,4 |
| Tuần trước | 0,576 | 24,2 |

Theo giờ thì trung bình 4 tuần đứng đầu; theo tổng tuần thì bảng lịch đứng đầu. Lý do: cộng lên tuần, phần lệch lên và lệch
xuống do nhiễu bù trừ nhau. Chỉ lệch cùng một chiều trong nhiều ngày mới dồn lại. Vì vậy phải chấm ở đúng mức của quyết định (ô 4)
trước khi chọn mô hình.

## 24. Code: chấm theo giờ và theo tổng tuần
<!-- ma: code-b01-tong-tuan -->

Cùng một bộ dự báo, chấm ở mức giờ hay mức tuần có thể đổi người thắng.

```python
import numpy as np
import pandas as pd

def mae(y, du_bao):
    y, du_bao = np.asarray(y, float), np.asarray(du_bao, float)
    co = ~np.isnan(y)
    return float(np.mean(np.abs(y[co] - du_bao[co])))

# cuon: mỗi dòng một giờ; cột goc, y và các cột dự báo
cot = ["trung bình 4 tuần", "bảng lịch", "tuần trước"]
tuan = cuon.groupby("goc")[["y", *cot]].sum(min_count=1)   # cộng cả tuần
du = cuon.groupby("goc")["y"].apply(lambda x: x.notna().all())
tuan.loc[~du, "y"] = np.nan                     # chỉ chấm tuần đủ số đo
theo_gio = {c: mae(cuon["y"], cuon[c]) for c in cot}
theo_tuan = {c: mae(tuan["y"], tuan[c]) for c in cot}
```

*Rút gọn từ buoi-01/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `groupby("goc").sum(min_count=1)` (pandas): Cộng mọi giờ cùng một gốc; nhóm toàn trống thì ra NaN, không ra 0.
- `apply(lambda x: x.notna().all())` (pandas): Hỏi từng tuần: có đủ số đo ở mọi giờ không.
- `tuan.loc[~du, "y"]` (pandas): Chọn các dòng tuần thiếu, cột y, để gán trống.

**Từng bước:**

- Dòng 4–7: MAE như mục 4.3, bỏ giờ trống.
- Dòng 11: Cộng 168 giờ của mỗi gốc thành tổng tuần.
- Dòng 12–13: Tuần thiếu số đo thì không chấm.
- Dòng 14–15: Tính MAE ở hai mức để so thứ hạng.

**Kết quả:** Theo giờ: TB 4 tuần 0,490 thắng bảng lịch 0,508. Theo tổng tuần: bảng lịch 16,4 thắng xa TB 4 tuần 27,9 kWh/tuần.

## 25. Thiếu và thừa đắt khác nhau: dùng quantile
<!-- ma: quantile -->

*Tiếng Anh: quantile · median · pinball loss · coverage*

**Quantile p** là giá trị nhỏ nhất mà ít nhất tỷ lệ p số liệu nằm dưới hoặc bằng nó; trung vị là quantile 0,5. Hình là đường tích luỹ: đi ngang từ
tỷ lệ trên trục dọc rồi thả xuống là ra quantile. Khi thiếu hàng mất 4 đồng mỗi đơn vị còn thừa chỉ mất 1 đồng, nên đặt
dự báo ở quantile 4 / (4 + 1) = 0,8: chấp nhận thừa để ít khi thiếu. Chấm dự báo quantile bằng **pinball loss**, loại sai số
phạt phần thiếu và phần thừa với trọng số khác nhau. Còn **tỷ lệ phủ** kiểm xem khoảng "95%" có thật sự phủ 95% không.

Hệ quả quan trọng: chọn mô hình theo MAE (vốn nhắm trung vị) sẽ chọn sai khi thiếu và thừa đắt khác nhau. Ở buổi 1, mua ở mức quantile 0,8 làm chi phí giảm 18,6% dù MAE lại tệ hơn. Vì vậy khoá dạy dự báo cả phân phối: có phân phối thì với tỷ lệ chi phí nào cũng chỉ việc đọc ra quantile tương ứng.

## 26. Đặt hàng một lần: thiếu và thừa đều tốn tiền
<!-- ma: newsvendor -->

*Tiếng Anh: newsvendor problem · pinball loss · quantile forecast*

Người bán báo phải đặt số báo một lần mỗi sáng. Thiếu thì mất khách, thừa thì lỗ tiền in. Đây là **bài toán newsvendor**, cũng là
bài toán của công ty mua điện trước ở buổi 1: thiếu mất Cu đồng mỗi kWh, thừa mất Co đồng.

Lượng nên đặt là quantile Cu / (Cu + Co) của phân phối nhu cầu. Với thiếu mất 4 và thừa mất 1, đó là quantile 0,8. Trên 10 ngày mẫu
của buổi 1:

- Mua 8 kWh mỗi ngày tốn 33 đồng.
- Mua 9 kWh tốn 28 đồng, ít nhất.
- Mua 10 kWh tốn 33 đồng.

Dự báo quantile được chấm bằng **pinball loss** mức τ: thiếu mỗi đơn vị phạt τ, thừa mỗi đơn vị phạt 1 − τ. Ví dụ τ = 0,8, thực tế
10, dự báo 8: thiếu 2 đơn vị, phạt 0,8 × 2 = 1,6. Cách phạt này có đáy đúng ở quantile τ, nên dự báo giỏi theo pinball là dự báo đặt
đúng quantile cần cho quyết định.

## 27. Code: thiếu đắt hơn thừa, mua quantile
<!-- ma: code-b01-newsvendor -->

Thử từng mức mua để thấy mức rẻ nhất là quantile 0,8, rồi áp vào dữ liệu điện thật.

```python
import numpy as np

nhu_cau = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # kWh, 10 ngày
chi_phi = {m: int(4 * np.clip(nhu_cau - m, 0, None).sum()  # thiếu: 4 đồng
                  + np.clip(m - nhu_cau, 0, None).sum())   # thừa: 1 đồng
           for m in range(6, 13)}
q08 = np.quantile(nhu_cau, 0.8, method="inverted_cdf")     # 4 / (4 + 1)

def tien_mat(y, f):
    d = np.asarray(y, float) - np.asarray(f, float)
    d = d[~np.isnan(d)]
    return float(np.mean(np.where(d > 0, 4 * d, -1 * d)))

# c09: dự báo cuốn năm 2009; chọn mức cộng thêm mà không nhìn 2010
q = float((c09["y"] - c09["trung bình 4 tuần"]).dropna().quantile(0.8))
print(tien_mat(y, f), tien_mat(y, f + q))       # năm 2010: trước, sau
```

*Rút gọn từ buoi-01/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `np.clip(x, 0, None)` (numpy): Cắt số âm về 0: chỉ giữ phần thiếu (hoặc phần thừa).
- `np.quantile(..., method="inverted_cdf")` (numpy): Tìm quantile đúng cách đếm tay, không nội suy.
- `np.where(d > 0, a, b)` (numpy): Chọn từng phần tử: điều kiện đúng lấy a, sai lấy b.

**Từng bước:**

- Dòng 3–6: Tính tiền mất 10 ngày cho mỗi mức mua 6–12.
- Dòng 7: Quantile 0,8 của nhu cầu, đếm như tính tay.
- Dòng 9–12: Tiền mất: thiếu phạt 4, thừa phạt 1.
- Dòng 14–15: Lấy quantile 0,8 sai số 2009 làm phần cộng.
- Dòng 16: So tiền mất năm 2010 trước và sau khi cộng.

**Kết quả:** Mua 9 kWh rẻ nhất (28 đồng) = quantile 0,8, không phải TB 7,7. Thật: cộng 0,455 kWh, tiền mất 1,213 xuống 0,987 (−18,6%), MAE tệ đi.

## 28. Phân phối: nhìn hình dạng trước khi tóm
<!-- ma: phan-phoi -->

*Tiếng Anh: distribution · histogram · cumulative distribution (CDF) · skewness · standard deviation*

Trước khi tóm số liệu bằng một con số, nhìn hình dạng của nó. **Histogram** đếm số lần gặp mỗi khoảng giá trị. **Đường tích luỹ**
(hàm phân phối tích luỹ) cho biết bao nhiêu phần số liệu nằm dưới mỗi mốc; đi ngang từ trục dọc rồi thả xuống là ra quantile.

Lượt thuê xe theo giờ lệch phải: phần lớn giờ vắng, vài giờ rất đông. Vì vậy trung bình (189) lớn hơn hẳn trung vị (142). **Hệ số
lệch** dương báo đuôi phải dài. **Độ lệch chuẩn** đo số liệu tản rộng cỡ nào so với trung bình, cùng đơn vị với dữ liệu.

## 29. Code: quantile, trung vị, trung bình
<!-- ma: code-b02-quantile -->

Tính quantile như đếm tay, và thấy trung bình với trung vị lệch nhau trên dữ liệu thật.

```python
import zipfile

import numpy as np
import pandas as pd

x9 = np.array([8, 2, 36, 5, 12, 3, 18, 6, 9])
np.sort(x9)                                    # 2 3 5 6 8 9 12 18 36
np.quantile(x9, 0.8, method="inverted_cdf")    # đếm tay: số thứ 8
np.quantile(x9, 0.8)                           # mặc định: nội suy

with zipfile.ZipFile("bike-sharing.zip") as z:
    h = pd.read_csv(z.open("hour.csv"), parse_dates=["dteday"])
y = h["cnt"].to_numpy(float)                   # lượt thuê từng giờ
print(y.mean(), np.median(y), np.quantile(y, 0.9))
```

*Rút gọn từ buoi-02/tu-hoc.ipynb, phần 0 và 1.*

**Thư viện và hàm:**

- `np.quantile(x, q)` (numpy): Tìm mốc mà tỷ lệ q số liệu nằm dưới hoặc bằng nó.
- `np.median(x)` (numpy): Trung vị: mốc chia đôi, bằng quantile 0,5.
- `pd.read_csv(z.open(...))` (pandas): Đọc tệp CSV nằm bên trong tệp nén thành bảng.

**Từng bước:**

- Dòng 6–7: Chín giờ, xếp tăng dần để đếm.
- Dòng 8: Vị trí 0,8 × 9 = 7,2, làm tròn lên số thứ 8.
- Dòng 9: Máy mặc định nội suy giữa hai số kề nhau.
- Dòng 11–13: Đọc lượt thuê theo giờ của Capital Bikeshare.
- Dòng 14: So trung bình, trung vị, quantile 0,9.

**Kết quả:** Đếm tay ra 18, máy mặc định ra 14,4. Dữ liệu thật: trung bình 189, trung vị 142, quantile 0,9 khoảng 451 lượt/giờ.

## 30. Trung bình, độ lệch chuẩn, z-score
<!-- ma: do-lech-chuan -->

*Tiếng Anh: mean · variance · standard deviation · z-score*

Ba con số nền của thống kê:

- **Trung bình**: tổng chia số lượng.
- **Phương sai**: trung bình của bình phương khoảng cách tới trung bình, chia cho n − 1.
- **Độ lệch chuẩn s**: căn của phương sai, cùng đơn vị với dữ liệu.

Với 2, 4, 6: trung bình là 4, khoảng cách là −2, 0, 2, tổng bình phương là 8, chia 2 ra phương sai 4, độ lệch chuẩn 2.

**z-score** đo một giá trị cách trung bình bao nhiêu lần độ lệch chuẩn: z = (giá trị − trung bình) / s. Trung bình 10, s = 2, giá
trị 16 thì z = 3. Từ đây mới có các quy tắc "3σ" để bắt ngoại lai (buổi 11), khoảng "±1,96s" (buổi 2), CV = s / trung bình (buổi 9).
**Chuẩn hoá z-score** một chuỗi (trừ trung bình, chia s) bỏ mức và biên độ, chỉ giữ hình dạng: 100, 300, 100, 300 thành −1, 1, −1, 1.

## 31. Hệ số lệch: đuôi dài nằm về phía nào
<!-- ma: he-so-lech -->

*Tiếng Anh: skewness · long right / left tail*

Chín giờ thuê xe 2, 3, 5, 6, 8, 9, 12, 18, 36 có trung bình 11 mà trung vị chỉ 8. Trung bình cao hơn vì số liệu lệch: vài giá trị rất
lớn kéo nó lên. **Hệ số lệch** đo lệch về phía nào và cỡ nào bằng một con số.

Cách tính: lấy độ lệch của mỗi số khỏi trung bình, chia cho độ lệch chuẩn $s$ (ở đây 10,57), lập phương, rồi lấy trung bình.

$$
g = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{y_i - \bar y}{s}\right)^3
$$

Lập phương giữ dấu, nên độ lệch âm góp số âm, độ lệch dương góp số dương. Nó còn phóng to số ở xa: số 36 lệch +25 góp gần hết tổng,
còn số 8 lệch −3 góp rất ít. Kết quả là **+1,35**: đuôi phải dài.

| Hệ số lệch | Nghĩa |
|---|---|
| ≈ 0 | đối xứng, trung bình gần trung vị |
| > 0 | đuôi phải dài, trung bình lớn hơn trung vị |
| < 0 | đuôi trái dài |

Hình: ô trái là số liệu đối xứng quanh giữa, hệ số lệch gần 0; ô phải dồn về bên trái với đuôi kéo dài sang phải, hệ số lệch dương.
Lượt thuê theo giờ của cả bộ dữ liệu có hệ số lệch 1,277, tức lệch phải rõ. Khi thấy hệ số lệch dương lớn, đừng dùng khoảng
"trung bình ± 1,96 s" (thẻ sau) và nên báo trung vị hay quantile thay cho trung bình. scipy và pandas dùng quy ước tính hơi khác nhau
nhưng cùng dấu.

## 32. Cách phạt quyết định con số nên báo
<!-- ma: con-so-bao -->

*Tiếng Anh: loss function · squared / absolute / pinball loss · point forecast*

Nên báo trung bình, trung vị hay quantile? Câu trả lời nằm ở cách sai lệch bị tính tiền, gọi là **hàm mất mát**:

- **Bình phương**: lệch 2 phạt 4, lệch 10 phạt 100, nên rất sợ lệch xa. Con số tốt nhất là **trung bình**.
- **Tuyệt đối**: lệch bao nhiêu phạt bấy nhiêu. Con số tốt nhất là **trung vị**.
- **Pinball** mức τ: thiếu mỗi đơn vị phạt τ, thừa mỗi đơn vị phạt 1 − τ. Con số tốt nhất là **quantile τ**.

Trên lượt thuê xe, ba đường phạt có đáy ở ba chỗ khác nhau: 189,46 (bình phương), 142 (tuyệt đối), 452 (pinball τ = 0,9). Đây là lý
do buổi 14 nói "chọn chỉ số là chọn dự báo".

## 33. Code: ba cách phạt, ba con số tốt nhất
<!-- ma: code-b02-pinball -->

Thấy bằng số: cách phạt sai quyết định nên báo trung bình, trung vị hay quantile.

```python
import numpy as np
import pandas as pd

x9 = np.array([8, 2, 36, 5, 12, 3, 18, 6, 9])
s = x9.std(ddof=1)                             # chia n − 1

def pinball(y, c, tau):
    sai = np.asarray(y, float) - c
    return float(np.where(sai >= 0, tau * sai, (tau - 1) * sai).mean())

bang = pd.DataFrame({c: {"tuyệt đối": np.abs(x9 - c).mean(),
                         "bình phương": ((x9 - c) ** 2).mean(),
                         "pinball 0,8": pinball(x9, c, 0.8)}
                     for c in (8, 11, 18)}).T  # trung vị, TB, quantile 0,8
```

*Rút gọn từ buoi-02/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `x.std(ddof=1)` (numpy): Độ lệch chuẩn; ddof=1 nghĩa là chia cho n − 1 thay vì n.
- `np.where(sai >= 0, ...)` (numpy): Phạt khác nhau cho dự báo thấp (sai dương) và dự báo cao.
- `pd.DataFrame({...}).T` (pandas): Dựng bảng từ từ điển rồi xoay: mỗi c một dòng.

**Từng bước:**

- Dòng 5: Độ lệch chuẩn mẫu, chia cho n − 1.
- Dòng 7–9: Pinball: thiếu phạt tau, thừa phạt 1 − tau.
- Dòng 11–14: Báo cùng một số c cho 9 giờ, tính ba mức phạt.

**Kết quả:** s = 10,57. Tuyệt đối thấp nhất ở c = 8 (6,56), bình phương ở c = 11 (99,3), pinball 0,8 ở c = 18 (3,40).

## 34. Phân phối chuẩn: 95% nằm trong ±1,96 s
<!-- ma: phan-phoi-chuan -->

*Tiếng Anh: normal distribution · 68–95 rule · quantile 0.975 = 1.96*

Khoảng 95% hay được dựng bằng "trung bình ± 1,96 × độ lệch chuẩn". Con số 1,96 đến từ **phân phối chuẩn**: đường cong hình chuông, đối
xứng quanh trung bình. Diện tích dưới đường cong bên trái một mốc là tỷ lệ giá trị nhỏ hơn mốc đó.

| Khoảng quanh trung bình | Tỷ lệ giá trị nằm trong |
|---|---|
| ± 1 s | 68,3% |
| ± 1,96 s | 95,0%, mỗi đuôi 2,5% |
| ± 2 s | 95,4% |

1,96 làm phần giữa đúng 95%, mỗi **đuôi** (phần ngoài hai mốc) còn 2,5%. Nói cách khác, 1,96 là quantile 0,975 của phân phối chuẩn
có trung bình 0, độ lệch chuẩn 1:

$$
P(|y - \mu| \leq 1{,}96\,\sigma) = 0{,}95
$$

Mọi phân phối chuẩn là cùng hình chuông dời đi và co giãn, nên 1,96 dùng được cho tất cả. Ví dụ trung bình 100, độ lệch chuẩn 10 thì
100 ± 1,96 × 10 cho khoảng 80,4 tới 119,6. Trong hình, phần xanh ở giữa chiếm 95%, hai phần cam ở hai đuôi mỗi phần 2,5%.

Lưu ý: chỉ dùng được khi dữ liệu gần hình chuông. Chín giờ thuê xe lệch phải có trung bình 11, độ lệch chuẩn 10,57, nên
11 − 1,96 × 10,57 cho cận dưới −9,7 lượt thuê, một con số vô lý. Với dữ liệu lệch, lấy thẳng quantile 0,025 và 0,975 của lịch sử.

## 35. Khoảng 95% phải phủ thật 95%
<!-- ma: khoang -->

*Tiếng Anh: prediction interval · coverage · empirical quantile*

**Khoảng dự báo 95%** hứa rằng cứ 100 lần thì khoảng 95 lần giá trị thật rơi vào khoảng. **Tỷ lệ phủ** đo lời hứa đó có giữ được
không, và phải báo riêng hai đuôi (rơi dưới cận dưới, vượt cận trên).

Khoảng ±1,96s (trung bình cộng trừ 1,96 lần độ lệch chuẩn) dựng từ lượt thuê năm 2011:

- Phủ 96,4% ngay năm 2011 (trong mẫu).
- Chỉ phủ 72,5% năm 2012, vì lượt thuê trung bình mỗi giờ tăng từ 143,8 lên 234,7. Gần 3 trên 10 giờ vượt cận trên.

Dữ liệu lệch phải thì dùng quantile thực nghiệm (lấy thẳng mốc 2,5% và 97,5% của lịch sử) để hai đuôi cân. Nhưng không cách nào
cứu được khi tương lai dịch mức. Luôn chấm khoảng ngoài mẫu.

## 36. Khoảng dự báo khác khoảng tin cậy
<!-- ma: khoang-tin-cay -->

*Tiếng Anh: prediction interval vs confidence interval · central limit theorem (CLT) · 1/√n*

Hai loại khoảng hay bị nhầm:

- **Khoảng dự báo** trả lời: một giá trị *mới* (giờ tới, ngày mai) sẽ rơi vào đâu.
- **Khoảng tin cậy** trả lời: một con số tóm tắt, như trung bình thật, nằm ở đâu.

Thêm dữ liệu thì khoảng tin cậy hẹp dần theo 1/√n: n gấp 4 thì khoảng hẹp một nửa. Lý do là **định lý giới hạn trung tâm**: dù
từng giá trị lệch phải, trung bình của nhiều giá trị vẫn gần hình chuông và dao động đúng σ/√n. Với lượt thuê xe (σ = 181,4),
trung bình của 25 giờ dao động 36,1, của 100 giờ còn 18,2, của 400 giờ còn 9,1. Khoảng dự báo thì không hẹp về 0, vì từng giờ vẫn
lên xuống như cũ dù ta biết trung bình chính xác tới đâu.

"95%" của khoảng tin cậy nói về *quy trình*: dựng 20 khoảng từ 20 mẫu thì khoảng 19 khoảng chứa trung bình thật. Người chỉ có một
mẫu không biết mình có rơi vào lần trượt hay không.

## 37. Code: khoảng 95% và tỷ lệ phủ
<!-- ma: code-b02-ty-le-phu -->

Dựng khoảng từ năm 2011 hai cách, rồi đếm tỷ lệ phủ và từng đuôi trên năm chưa dùng.

```python
import numpy as np
import pandas as pd

# h: bảng lượt thuê theo giờ; yr = 0 là 2011, yr = 1 là 2012
cach = {"±1,96s": lambda x: (x.mean() - 1.96 * x.std(ddof=1),
                             x.mean() + 1.96 * x.std(ddof=1)),
        "quantile": lambda x: tuple(np.quantile(x, [0.025, 0.975]))}
n11, n12 = h[h.yr == 0], h[h.yr == 1]
for ten, f in cach.items():
    k = pd.DataFrame([(g, *f(nhom["cnt"])) for g, nhom in n11.groupby("hr")],
                     columns=["hr", "lo", "hi"])        # dựng từ 2011
    for du in (n11, n12):
        m = du.merge(k, on="hr")
        phu = np.mean((m.cnt >= m.lo) & (m.cnt <= m.hi))
        duoi, tren = np.mean(m.cnt < m.lo), np.mean(m.cnt > m.hi)
```

*Rút gọn từ buoi-02/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `np.quantile(x, [0.025, 0.975])` (numpy): Lấy hai mốc chặn 2,5% dưới và 2,5% trên của lịch sử.
- `groupby("hr")` (pandas): Chia bảng theo giờ trong ngày để mỗi giờ có khoảng riêng.
- `merge(k, on="hr")` (pandas): Nối hai bảng theo cột chung hr, như dò bảng.

**Từng bước:**

- Dòng 5–7: Hai cách dựng khoảng: công thức và quantile.
- Dòng 10–11: Mỗi giờ trong ngày một khoảng, chỉ từ 2011.
- Dòng 13: Gắn khoảng của đúng giờ vào từng dòng.
- Dòng 14: Tỷ lệ phủ: thật rơi vào trong khoảng.
- Dòng 15: Đếm riêng hai đuôi để biết lệch phía nào.

**Kết quả:** Trên 2011: ±1,96s phủ 96,4%, quantile 95,3%. Trên 2012: chỉ 72,5% và 70,1%, vượt trên 27,4% và 29,3%.

## 38. p-value: nếu H0 đúng, dữ liệu này hiếm cỡ nào?
<!-- ma: kiem-dinh -->

*Tiếng Anh: null hypothesis H0 · p-value · significance level α · permutation test*

**Kiểm định giả thuyết** hỏi: nếu **H0** (giả định "không có gì đặc biệt") đúng, thì dữ liệu như ta thấy hiếm cỡ nào? Con số đó là
**p-value**. p nhỏ hơn **mức ý nghĩa** chọn trước (thường 0,05) thì bác bỏ H0.

Ví dụ: tung đồng xu 10 lần được 9 ngửa. Có 2¹⁰ = 1.024 dãy kết quả; 10 dãy có đúng 9 ngửa và 1 dãy có 10 ngửa. Vậy p = 11/1.024 ≈
0,011 < 0,05: bác bỏ "đồng xu cân đối".

Hình dùng **kiểm định hoán vị**: xáo nhãn "ngày làm việc / ngày nghỉ" hàng nghìn lần xem chênh lệch thật có hiếm không.

Ba điều hay hiểu sai:

- Không bác bỏ không có nghĩa là H0 đúng.
- p không phải xác suất H0 đúng.
- Có ý nghĩa thống kê không có nghĩa là chênh lệch lớn.

Hai lời dặn thêm: báo chênh lệch kèm khoảng của nó, đừng chỉ báo p; và kiểm định hoán vị giả định các ngày độc lập, nên với chuỗi tự tương quan thì p thật thường lớn hơn số tính được.

## 39. Kiểm định hoán vị: xáo nhãn rồi đếm
<!-- ma: hoan-vi -->

*Tiếng Anh: permutation test · shuffled labels · p-value*

Năm 2012 ngày làm việc hơn ngày nghỉ 456 lượt thuê mỗi ngày. Khác biệt thật hay do may? **Kiểm định hoán vị** trả lời mà không cần
công thức phức tạp. Giả thuyết không ($H_0$) ở đây là: nhãn "làm việc/nghỉ" không liên quan tới lượt thuê. Nếu vậy, gán nhãn kiểu
nào cũng như nhau.

Ví dụ 6 ngày (nghìn lượt): làm việc 5, 7, 6; nghỉ 3, 2, 4. Chênh trung bình thật là 6 − 3 = 3. Có $C(6, 3) = 20$ cách chọn 3 ngày làm
nhóm "làm việc". Chỉ 2 cách cho chênh lệch cỡ 3 trở lên về một trong hai phía: {7, 6, 5} và {2, 3, 4}.

$$
p = \frac{\mathrm{số\ cách\ chia\ có\ chênh} \geq 3}{C(6,\,3)} = \frac{2}{20} = 0{,}10
$$

p = 0,10 > 0,05 nên không bác bỏ: 6 ngày là quá ít. Nhiều ngày thì không liệt kê hết được, máy xáo nhãn ngẫu nhiên
$B$ lần và tính $p = (k + 1)/(B + 1)$, với $k$ là số lần xáo cho chênh lệch bằng hoặc hơn chênh thật. Năm 2012, xáo 9.999 lần có
253 lần như vậy, p ≈ 0,025.

Hình vẽ histogram các chênh lệch khi xáo nhãn, vạch cam là chênh thật. Ô trái (làm việc − nghỉ) chỉ một mẩu nhỏ nằm ngoài hai vạch
cam; ô phải (thứ Bảy − Chủ nhật, ít ngày hơn) nhiều hơn hẳn, p = 0,078. Lưu ý: xáo nhãn giả định các
ngày độc lập. Ngày đông hay đi liền ngày đông, nên p-value thật thường lớn hơn số tính được.

## 40. Code: kiểm định hoán vị
<!-- ma: code-b02-hoan-vi -->

Tính p-value bằng cách xáo nhãn: nếu nhãn vô nghĩa, chênh lệch cỡ thật có hiếm không?

```python
import numpy as np

def hoan_vi(yy, nhom, so_lan=9999, seed=2026):
    yy, nhom = np.asarray(yy, float), np.asarray(nhom, bool)
    that = yy[nhom].mean() - yy[~nhom].mean()
    rng = np.random.default_rng(seed)
    k = 0
    for _ in range(so_lan):
        p_ = rng.permutation(nhom)                  # xáo nhãn, giữ số
        k += abs(yy[p_].mean() - yy[~p_].mean()) >= abs(that)
    return that, (k + 1) / (so_lan + 1)

# d: bảng lượt thuê theo ngày; yr = 1 là năm 2012
n12 = d[d.yr == 1]
that, p = hoan_vi(n12.cnt, n12.workingday == 1)
```

*Rút gọn từ buoi-02/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `np.random.default_rng(seed)` (numpy): Tạo bộ sinh số ngẫu nhiên; cùng seed thì ra cùng dãy.
- `rng.permutation(nhom)` (numpy): Xáo trộn thứ tự nhãn, giữ nguyên số nhãn mỗi loại.
- `yy[nhom].mean()` (numpy): Trung bình của các phần tử có nhãn True.

**Từng bước:**

- Dòng 5: Chênh lệch thật giữa hai nhóm ngày.
- Dòng 6: Cố định seed để chạy lại ra cùng p.
- Dòng 8–10: Xáo nhãn 9.999 lần, đếm lần lệch bằng hoặc hơn.
- Dòng 11: p là tỷ lệ lần xáo lệch cỡ thật.
- Dòng 14–15: Ngày làm việc so với ngày nghỉ năm 2012.

**Kết quả:** Làm việc − nghỉ chênh +456 lượt/ngày, p = 0,025 < 0,05: bác bỏ H0. Thứ Bảy − CN chênh +695 mà p > 0,05.

## 41. Bootstrap chuỗi thời gian: rút cả khối
<!-- ma: bootstrap -->

*Tiếng Anh: bootstrap · block bootstrap · confidence interval · i.i.d.*

**Bootstrap** ước lượng độ bấp bênh của một con số mà không cần công thức:

1. Rút lại từ chính mẫu, có hoàn lại, vài nghìn lần.
2. Mỗi lần tính trung bình.
3. Khoảng 95% là quantile 0,025 và 0,975 của các trung bình đó.

Nhưng chuỗi thời gian có tự tương quan: rút từng điểm làm mất việc các điểm đi liền nhau, nên khoảng hẹp quá mức. Trên mô phỏng
AR(1), khoảng rút từng điểm chỉ chứa trung bình thật 60,3% số lần, thay vì 95%. **Block bootstrap** rút cả khối liền nhau: khối 20
cho 89,3%. Kết quả nhạy với độ dài khối (khối 40 lại tụt còn 81,3%), nên thử vài độ dài và báo độ nhạy.

Vì sao khoảng rút từng điểm hẹp giả: dữ liệu tự tương quan chỉ đáng n_eff < n quan sát độc lập (cỡ mẫu hiệu dụng). Giờ này đông thì giờ sau gần như chắc cũng đông, nên giờ sau mang ít thông tin mới.

## 42. Bootstrap từng bước: rút lại, lấy hai đầu
<!-- ma: bootstrap-buoc -->

*Tiếng Anh: bootstrap · resampling with replacement · percentile interval · block bootstrap*

1. Có một mẫu thật n số. Ví dụ 5 ngày liền nhau: 12, 15, 11, 30, 14; trung bình 16,4.
2. Rút lại n số **có hoàn lại**: một số có thể được rút nhiều lần, số khác không được rút.
3. Tính trung bình của mẫu vừa rút.
4. Lặp vài nghìn lần, được vài nghìn trung bình.
5. Lấy quantile 0,025 và 0,975 của các trung bình đó: khoảng tin cậy 95%.

Không có bước nào nhân 1,96: bootstrap lấy thẳng hai đầu của các trung bình tính lại. Ba lần rút đầu (seed 3) cho 13,0; 12,6;
16,4: hai lần đầu không trúng số 30 nên thấp hẳn. Rút từng điểm xáo tung thứ tự các ngày. **Rút khối** dài 2 (seed 2) lấy ba
khối (30, 14), (15, 11), (12, 15), nối lại và cắt còn 5 số: 30, 14, 15, 11, 12, trung bình 16,4. Ngày 30 và ngày 14 ngay sau nó
vẫn đi cùng nhau, nên mối liên hệ giữa hai ngày liền nhau được giữ. Số liệu: buổi 2, mục 4.6.

## 43. Code: bootstrap từng điểm và rút khối
<!-- ma: code-b02-block-bootstrap -->

Dựng khoảng tin cậy bằng rút lại mẫu, và thấy rút khối sửa được khoảng quá tự tin.

```python
import numpy as np

def khoang_tin_cay(x, khoi, so_lan=999, seed=0):
    rng, n = np.random.default_rng(seed), x.size
    if khoi <= 1:
        cs = rng.integers(0, n, size=(so_lan, n))          # từng điểm
    else:
        so_khoi = int(np.ceil(n / khoi))
        bat_dau = rng.integers(0, n - khoi + 1, size=(so_lan, so_khoi))
        cs = (bat_dau[:, :, None] + np.arange(khoi)).reshape(so_lan, -1)
    return np.quantile(x[cs[:, :n]].mean(axis=1), [0.025, 0.975])
# chuoi: 300 chuỗi AR(1), rho = 0,7, trung bình thật bằng 0
for khoi in (1, 3, 6, 10, 20, 40):
    kq = [khoang_tin_cay(x, khoi, seed=2026 + i)
          for i, x in enumerate(chuoi)]
    phu = np.mean([lo <= 0 <= hi for lo, hi in kq])
```

*Rút gọn từ buoi-02/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `rng.integers(0, n, size=...)` (numpy): Sinh vị trí ngẫu nhiên từ 0 tới n − 1, lặp lại được.
- `x[cs].mean(axis=1)` (numpy): Lấy các điểm theo vị trí đã rút, trung bình từng lần rút.
- `np.arange(khoi)` (numpy): Dãy 0, 1, …, khoi − 1, cộng vào điểm đầu thành một khối.

**Từng bước:**

- Dòng 5–6: Rút ngẫu nhiên có hoàn lại từng điểm.
- Dòng 8–10: Rút điểm đầu khối, nối khối liền nhau.
- Dòng 11: Quantile của 999 trung bình ra khoảng 95%.
- Dòng 13–16: Đếm bao nhiêu khoảng chứa trung bình thật 0.

**Kết quả:** Rút từng điểm: chỉ 60,3% khoảng chứa trung bình thật. Khối 10: 89,0%; khối 20: 89,3%; khối 40 tụt còn 81,3%.

## 44. Một con số giờ chưa đủ: cần múi giờ
<!-- ma: utc -->

*Tiếng Anh: UTC · time zone · daylight saving time (DST) · naive / aware timestamp*

**UTC** là giờ chung của thế giới: 07:00 ở Hà Nội là 00:00 UTC. Thời điểm **naive** không ghi múi giờ, thời điểm **aware** có
ghi. **Giờ mùa hè (DST)** làm giờ địa phương có chỗ hở và chỗ lặp. Ở New York, ngày 10/3/2024 đồng hồ nhảy từ 1:59 lên 3:00,
nên giờ 2:00 không tồn tại. Ngày 3/11 thì giờ 1:00 xảy ra hai lần. Hình vẽ đồng hồ New York theo giờ UTC, có một đoạn "không
tồn tại" và một đoạn "xảy ra 2 lần". Cách sửa: gắn đúng múi giờ rồi đổi sang UTC trước khi gộp hay ghép bất cứ thứ gì.

## 45. Code: gắn múi giờ New York, đổi UTC
<!-- ma: code-b03-dst -->

Thấy một giờ New York có thể ứng với một, không, hoặc hai thời điểm UTC.

```python
import pandas as pd

NY = "America/New_York"
for ngay, gio in [("2024-03-10", "01:30"), ("2024-03-10", "02:30"),
                  ("2024-03-10", "03:30"), ("2024-11-03", "01:30")]:
    ket_qua = []
    for mua_he in (True, False):             # giờ lặp: EDT hay EST
        try:
            t = pd.Timestamp(f"{ngay} {gio}").tz_localize(
                NY, ambiguous=mua_he)        # gắn múi giờ New York
            ket_qua.append(t.tz_convert("UTC").strftime("%H:%MZ"))
        except Exception:                    # giờ không tồn tại
            pass
    print(ngay, gio, sorted(set(ket_qua)) or "KHÔNG TỒN TẠI")
```

*Rút gọn từ buoi-03/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `tz_localize(NY, ambiguous=...)` (pandas): Gắn múi giờ cho giờ chưa có; ambiguous chọn EDT hay EST.
- `tz_convert("UTC")` (pandas): Đổi một thời điểm đã có múi giờ sang giờ UTC.
- `strftime("%H:%MZ")` (pandas): Viết thời điểm thành chữ theo mẫu giờ:phút kèm chữ Z.

**Từng bước:**

- Dòng 4–5: Bốn giờ quanh hai ngày vặn đồng hồ 2024.
- Dòng 7: Thử cả hai cách hiểu: giờ hè và giờ đông.
- Dòng 9–10: Gắn múi giờ: con số giờ thành thời điểm thật.
- Dòng 11: Đổi sang UTC, trục thời gian chạy đều.
- Dòng 12–13: Giờ bị nhảy qua thì báo lỗi, bỏ qua.

**Kết quả:** 10/3: 01:30 ra 06:30Z, 02:30 không tồn tại, 03:30 ra 07:30Z. 01:30 ngày 3/11 có hai đáp án: 05:30Z hoặc 06:30Z.

## 46. Gộp tần suất: khoảng nào, cộng hay trung bình
<!-- ma: resample -->

*Tiếng Anh: resample · closed / label · sum vs mean aggregation*

Đổi tần suất (ví dụ từ chuyến lẻ sang số chuyến mỗi giờ) phải trả lời ba câu:

- **Khoảng nào?** `closed` chọn mốc biên thuộc khoảng nào; `label` chọn đặt tên khoảng bằng mốc đầu hay cuối. Mặc định của
  pandas (với giờ) là đóng trái, nhãn trái: [9:00, 10:00) tên "9:00". Bốn chuyến 9:00, 9:40, 10:00, 10:20 cho ô "9:00" có 2
  chuyến và ô "10:00" có 2 chuyến.
- **Gộp thế nào?** Số lượng (số chuyến) thì cộng; trạng thái (nhiệt độ) thì trung bình hoặc lấy giá trị cuối.
- **Giờ trống là gì?** Với số đếm sự kiện, giờ trống là 0. Với số đo, giờ trống là NaN (không biết).

## 47. Code: resample cộng hay trung bình
<!-- ma: code-b03-resample -->

Gộp sự kiện thành chuỗi đều: đếm thì cộng, số đo thì lấy trung bình.

```python
import pandas as pd

t = pd.to_datetime(["2024-01-01 00:10", "2024-01-01 00:50",
                    "2024-01-01 02:20"])
s = pd.Series([1.0, 2.0, 5.0], index=t)
s.resample("h").sum()       # số lượng: cộng, giờ trống ra 0
s.resample("h").mean()      # số đo: trung bình, giờ trống ra NaN
# cách khác: floor về đầu giờ; không tự thêm giờ trống
s.groupby(s.index.floor("h")).sum()
# tháng 3 New York: ngày 10/3 chỉ dài 23 giờ
gio = pd.date_range("2024-03-01", "2024-04-01", freq="h",
                    tz="America/New_York", inclusive="left")
len(gio)
```

*Rút gọn từ buoi-03/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `resample("h")` (pandas): Chia trục thời gian thành từng giờ, mỗi giờ gộp thành một số.
- `index.floor("h")` (pandas): Làm tròn mỗi mốc xuống đầu giờ: 9:40 thành 9:00.
- `pd.date_range(..., tz=...)` (pandas): Sinh lưới giờ theo múi giờ, tự bỏ giờ bị nhảy qua.

**Từng bước:**

- Dòng 3–5: Ba sự kiện lúc 00:10, 00:50, 02:20.
- Dòng 6: Cộng theo giờ; giờ 01:00 không có gì ra 0.
- Dòng 7: Trung bình theo giờ; giờ trống ra NaN.
- Dòng 9: Làm tròn xuống đầu giờ rồi cộng, thiếu giờ 01.
- Dòng 11–13: Đếm số giờ thật của tháng 3.

**Kết quả:** Cộng ra [3, 0, 5], trung bình ra [1,5; NaN; 5], floor chỉ ra [3, 5]. Tháng 3 có 743 giờ, không phải 744.

## 48. Ghép theo thời gian: chỉ nhìn về quá khứ
<!-- ma: merge-asof -->

*Tiếng Anh: as-of join (merge_asof) · direction="backward" · tolerance*

Ghép hai nguồn theo thời gian (ví dụ giá hay thời tiết vào từng dòng) dùng `merge_asof`: mỗi dòng lấy giá trị gần nhất. Ví dụ dòng
10:00, bảng giá có số lúc 9:30 và 10:30:

- **backward** (mặc định): lấy giá đã có lúc 9:30. Đúng.
- **forward**: lấy giá lúc 10:30, tức lấy tương lai. Đây là rò rỉ.

Thêm `tolerance` để không ghép một con số quá cũ. Và luôn đưa cả hai nguồn về UTC trước khi ghép.

## 49. Dạng dài: ai, khi nào, bao nhiêu
<!-- ma: dang-dai -->

*Tiếng Anh: long format · wide format*

Mọi buổi sau nhận dữ liệu ở **dạng dài** với ba cột: `unique_id` (chuỗi nào), `ds` (khi nào, theo UTC), `y` (giá trị bao
nhiêu). **Dạng rộng** mỗi chuỗi một cột, tiện nhìn nhưng thêm chuỗi là thêm cột. Tháng 3/2024 có 259 khu vực taxi có chuyến thì dạng rộng có 259 cột,
còn dạng dài vẫn chỉ ba cột, chỉ nhiều dòng hơn. Ba điều kiện của một bảng sạch: mỗi cặp (unique_id, ds) một dòng, đủ mọi
mốc thời gian, không trùng.

Mọi chuỗi trải lên cùng một lưới mốc UTC. Tháng 3/2024 theo UTC có 743 giờ, không phải 744, vì New York mất một giờ ngày đổi giờ.

## 50. Code: dạng dài trên một lưới chung
<!-- ma: code-b03-dang-dai -->

Dựng bảng unique_id, ds, y cho mọi khu vực, đủ mọi giờ, giờ không có chuyến ghi 0.

```python
import pandas as pd

# t3: chuyến tháng 3; utc: giờ đón đã đổi UTC như mục 4.4
kv = t3.assign(ds=utc.dt.floor("h")).dropna(subset=["ds"])
dem = kv.groupby(["PULocationID", "ds"]).size()    # chỉ giờ có chuyến
luoi = pd.date_range("2024-03-01 05:00", "2024-04-01 04:00", freq="h",
                     tz="UTC", inclusive="left")   # [đầu, cuối)
day_du = pd.MultiIndex.from_product([dem.index.levels[0], luoi],
                                    names=["unique_id", "ds"])
dai = dem.reindex(day_du, fill_value=0).rename("y").reset_index()
ty_le_0 = (dai["y"] == 0).mean()                   # tỷ lệ ô bằng 0
```

*Rút gọn từ buoi-03/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `pd.MultiIndex.from_product` (pandas): Tạo mọi cặp (khu vực, giờ) từ hai danh sách.
- `reindex(..., fill_value=0)` (pandas): Trải số đếm lên lưới đủ; cặp chưa có thì điền 0.
- `reset_index()` (pandas): Biến chỉ mục thành cột thường: ra bảng ba cột dạng dài.

**Từng bước:**

- Dòng 4: Làm tròn giờ đón UTC xuống đầu giờ.
- Dòng 5: Đếm chuyến theo khu vực và giờ.
- Dòng 6–7: Lưới giờ UTC của cả tháng 3 New York.
- Dòng 8–10: Mọi khu vực nhân mọi giờ; giờ vắng ghi 0.
- Dòng 11: Xem bao nhiêu ô bằng 0.

**Kết quả:** 192.437 dòng = 259 khu vực × 743 giờ, không mất chuyến nào; 53,7% số ô bằng 0.

## 51. Mùa vụ lặp đều; chu kỳ không hẹn trước
<!-- ma: mua-vu -->

*Tiếng Anh: trend · seasonality · cycle*

- **Xu hướng** là mức chung đổi dần trong thời gian dài.
- **Mùa vụ** lặp lại sau một số bước cố định theo lịch (ngày, tuần, năm). Lượt thuê xe cao lúc 8h và 17h mỗi ngày làm việc
  là mùa vụ.
- **Chu kỳ** cũng lên xuống nhưng không biết bao lâu mới lặp. Kinh tế tăng rồi suy thoái là chu kỳ.

Cách nhớ: mùa vụ lặp đều, biết trước; chu kỳ lên xuống, không hẹn trước. Mùa vụ dự báo được vì biết trước lịch, chu kỳ thì khó hơn nhiều.

## 52. Đọc mọi biểu đồ theo 5 bước
<!-- ma: doc-hinh -->

*Tiếng Anh: axis · legend · heatmap · seasonal plot*

Đọc bất kỳ hình nào theo năm bước:

1. Trục ngang là gì.
2. Trục dọc là gì, đơn vị gì.
3. Ký hiệu: màu, nét, chấm nghĩa là gì.
4. Nhìn vào đâu.
5. Kết luận bằng một câu.

Ví dụ với heatmap giờ × thứ: trục ngang là giờ 0–23, trục dọc là thứ Hai tới Chủ nhật, màu là lượt thuê trung bình. Hai
cột sáng lúc 8h và 17h chạy suốt năm ngày làm việc rồi tắt ở cuối tuần, còn cuối tuần sáng đều giữa ngày. Kết luận: có mùa
vụ ngày lồng trong mùa vụ tuần. Khoá quy ước tiêu đề hình là câu kết luận, không phải tên biến.

Heatmap chỉ cho trung bình mỗi ô, không cho độ tản, nên chênh lệch nhỏ giữa hai ô chưa chắc là thật; xem thêm boxplot.

## 53. Code: tách xu hướng và mùa vụ tuần
<!-- ma: code-b04-ba-mau-hinh -->

Tính tay hai tuần để thấy mùa vụ là phần lặp lại, rồi gộp dữ liệu thật theo ngày, tháng.

```python
import numpy as np
import pandas as pd

# hai tuần, trăm lượt mỗi ngày, từ T2 tới CN
tuan = np.array([[10, 12, 12, 12, 14, 6, 4],
                 [12, 14, 14, 14, 16, 8, 6]])
tb = tuan.mean(axis=1, keepdims=True)    # trung bình mỗi tuần
lech = tuan - tb                         # phần lệch: mùa vụ tuần

# df: lượt thuê theo giờ, đặt trên lưới giờ đầy đủ
ngay = df["cnt"].resample("D").sum(min_count=12)  # thiếu giờ ra NaN
thang = df["cnt"].resample("MS").sum()
print(ngay.nsmallest(3))                 # những ngày rơi sát 0
```

*Rút gọn từ buoi-04/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `mean(axis=1, keepdims=True)` (numpy): Trung bình theo từng dòng, giữ dạng cột để trừ được cả bảng.
- `resample("D").sum(min_count=12)` (pandas): Cộng các giờ thành tổng ngày; ngày dưới 12 giờ số liệu để trống.
- `nsmallest(3)` (pandas): Lấy ba giá trị nhỏ nhất kèm ngày của chúng.

**Từng bước:**

- Dòng 4–6: Hai tuần số nhỏ, tuần sau cao hơn tuần trước.
- Dòng 7: Trung bình tuần đi từ 10 lên 12: xu hướng.
- Dòng 8: Trừ trung bình, phần còn lại là mùa vụ tuần.
- Dòng 11–12: Gộp giờ thành ngày và tháng để nhìn đủ tầng.
- Dòng 13: Tìm ngày thấp bất thường mà hình tháng giấu.

**Kết quả:** Trung bình tuần 10 và 12; phần lệch hai tuần giống hệt: 0, 2, 2, 2, 4, −4, −6. Đó là mùa vụ tuần.

## 54. Làm trơn: đường mượt xoá ngày bất thường
<!-- ma: lam-tron -->

*Tiếng Anh: smoothing · centered moving average · window w*

**Trung bình trượt có tâm** thay mỗi điểm bằng trung bình của nó với các điểm hai bên, trong một cửa sổ $w$ điểm:

$$
\tilde y_t = \frac{1}{w}\sum_{j=-k}^{k} y_{t+j}, \qquad w = 2k + 1
$$

Bảy ngày lượt thuê (trăm lượt): 50, 52, 48, **2**, 51, 49, 50. Với $w$ = 3, ngày thứ tư thành (48 + 2 + 51) / 3 = 33,7; với
$w$ = 7 thành 302 / 7 = 43,1. Cửa sổ càng rộng, đường càng mượt, và ngày bất thường càng mờ.

Hình: ngày bão Sandy 29/10/2012 tệp chỉ còn 1 giờ với 22 lượt, nhưng đường trung bình 7 ngày ở ngày đó vẫn là 4.632 lượt. Ai
chỉ xem đường làm trơn sẽ không biết có một ngày dữ liệu gần như trống. Vì vậy vẽ đường làm trơn **đè lên** dữ liệu gốc, không
thay nó. Kiểu có tâm dùng số của các ngày sau, nên chỉ để mô tả; làm feature dự báo thì dùng kiểu nhân quả (buổi 12).

## 55. Thang log: cùng độ dốc là cùng phần trăm
<!-- ma: thang-log -->

*Tiếng Anh: log scale · percentage change · log₁₀*

Trên thang log, trục dọc đặt mỗi điểm ở độ cao $\log_{10} y$ thay vì $y$. Mỗi lần gấp đôi thì cao thêm đúng
$\log_{10} 2 = 0{,}301$, dù từ 100 lên 200 hay từ 200 lên 400. Vậy trên thang log, **hai đoạn dốc như nhau nghĩa là tăng cùng một
phần trăm**.

| $y$ | 100 | 200 | 400 | 500 |
|---|---|---|---|---|
| Gấp mấy lần điểm trước | | 2 | 2 | 1,25 |
| Bước cao thêm trên thang log | | 0,301 | 0,301 | 0,097 |

Hình (thuê xe theo tháng, 2011): thang thường cho thấy tháng 4 → 5 tăng nhiều lượt nhất (+40.951); thang log cho thấy tháng 3 → 4
tăng nhanh nhất theo phần trăm (+48,1%, còn tháng 4 → 5 là +43,2%). Hỏi "cần thêm bao nhiêu xe" thì dùng thang thường; hỏi "tăng
nhanh cỡ nào" thì dùng thang log.

## 56. Tám biểu đồ, tám câu hỏi
<!-- ma: bo-bieu-do -->

*Tiếng Anh: seasonal plot · subseries plot · lag plot · heatmap · boxplot · ACF*

Không có biểu đồ nào nói hết. Bộ 8 biểu đồ chẩn đoán của buổi 4, mỗi hình trả lời một câu:

1. **Đường theo ngày**: xu hướng và mùa năm.
2. **Seasonal plot tuần**: hình dạng một vòng lặp (thứ Hai – thứ Sáu hai đỉnh, cuối tuần một đỉnh).
3. **Subseries theo tháng**: mỗi tháng đổi qua các năm ra sao.
4. **Lag plot**: giá trị cách k bước giống hiện tại tới đâu.
5. **Heatmap giờ × thứ**: mùa vụ kép.
6. **Boxplot theo giờ**: độ tản, giờ nào khó dự báo.
7. **Scatter với nhiệt độ**: quan hệ với biến khác, tô màu theo năm.
8. **ACF**: nhịp lặp đo bằng số.

Ngoài ra còn hai việc khi vẽ:

- Vẽ đường làm trơn đè lên dữ liệu gốc, không thay nó, để không mất ngày bất thường.
- Trên thang log, cùng độ dốc là cùng phần trăm thay đổi.

## 57. Seasonal plot chồng vòng, subseries gom mùa
<!-- ma: seasonal-subseries -->

*Tiếng Anh: seasonal plot · subseries plot · multiple seasonality*

Biểu đồ đường vẽ theo thời gian trôi, nên khó thấy mùa vụ. Muốn thấy mùa vụ, xếp dữ liệu theo vị trí trong vòng lặp: thứ mấy, giờ mấy,
tháng mấy. Có hai cách xếp, trả lời hai câu hỏi khác nhau.

- **Seasonal plot**: mỗi vòng lặp (mỗi tuần) là một đường, các đường chồng lên nhau. Nhìn đường nào lệch khỏi khuôn chung.
- **Subseries plot**: mỗi "mùa" (mỗi thứ, mỗi tháng) một ô, điểm trong ô xếp theo thời gian. Nhìn mỗi mùa đổi ra sao qua các năm.

Ví dụ hai tuần: tuần 1 là 10, 12, 12, 12, 14, 6, 4; tuần 2 là 12, 14, 14, 14, 16, 8, 6. Seasonal plot (ô trái của hình) cho hai đường
song song: cùng hình dạng tuần, tuần 2 cao hơn 2 ở mọi thứ. Subseries plot (ô phải) có 7 ô, vạch cam ở trung bình mỗi ô: 11, 13, 13,
13, 15, 7, 5. Dãy vạch đó chính là hình dạng mùa vụ tuần. Trong mỗi ô, điểm sau cao hơn điểm trước: có xu hướng.

Trên lượt thuê theo giờ, seasonal plot theo tuần cho thấy T2–T6 có hai đỉnh sáng và chiều, T7–CN một bướu giữa ngày. Mùa vụ ngày đổi
hình dạng theo thứ, gọi là **mùa vụ kép**. Subseries theo tháng cho thấy tháng nào cũng nhảy bậc: tổng mỗi tháng 2012 gấp 1,41 tới
2,57 lần cùng tháng 2011. Lưu ý: `month_plot` của statsmodels thật ra vẽ subseries plot và chỉ nhận dữ liệu tháng hoặc quý.

## 58. Code: xếp dữ liệu theo giờ trong tuần
<!-- ma: code-b04-gio-trong-tuan -->

Xoay bảng cho mỗi tuần một cột để thấy hình dạng mùa vụ, rồi so tổng từng thứ.

```python
import pandas as pd

# df: lượt thuê theo giờ, có cột thu (0 là T2) và gio
bang = (df.assign(gio_tuan=df["thu"] * 24 + df["gio"],   # 0 tới 167
                  tuan=df.index.to_period("W-SUN"))
          .pivot_table(index="gio_tuan", columns="tuan", values="cnt"))
khuon = bang.median(axis=1)          # hình dạng tuần điển hình

du = df["cnt"].resample("D").agg(["sum", "count"])
du = du[du["count"] == 24]           # chỉ ngày đủ 24 giờ
tb_thu = du.groupby(du.index.dayofweek)["sum"].mean()
```

*Rút gọn từ buoi-04/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `pivot_table(index, columns, values)` (pandas): Xoay bảng dài thành bảng ngang: dòng theo một cột, cột theo cột khác.
- `to_period("W-SUN")` (pandas): Đổi mỗi mốc giờ thành tuần chứa nó, tuần tính tới Chủ nhật.
- `groupby(...).mean()` (pandas): Chia các dòng thành nhóm theo nhãn rồi lấy trung bình mỗi nhóm.

**Từng bước:**

- Dòng 4: Giờ trong tuần = thứ nhân 24 cộng giờ.
- Dòng 5: Gắn nhãn tuần, tuần kết thúc Chủ nhật.
- Dòng 6: Mỗi tuần một cột, mỗi dòng một giờ trong tuần.
- Dòng 7: Trung vị các tuần: khuôn chung của tuần.
- Dòng 9–11: Tổng ngày trung bình theo thứ, bỏ ngày thiếu.

**Kết quả:** 106 tuần chồng nhau: T2–T6 hai đỉnh, T7–CN một bướu. Tổng ngày gần nhau: T7 4.653 lượt so với T6 4.933.

## 59. Boxplot: hộp càng dài, giờ càng khó dự báo
<!-- ma: boxplot -->

*Tiếng Anh: boxplot · interquartile range (IQR) · median*

**Boxplot** cho trung vị và độ tản:

- Hộp chứa một nửa số ngày ở giữa, từ quantile 0,25 tới 0,75. Độ rộng hộp gọi là IQR.
- Vạch giữa hộp là trung vị.

Lượt thuê xe theo giờ:

| Nhóm | Trung vị | Hộp (quantile 0,25–0,75) |
|---|---|---|
| Ngày làm việc, 8h | 463 | 365 – 646 |
| Ngày làm việc, 17h | 539 | 348 – 704 |
| Ngày nghỉ, 8h | 94 | 57 – 141 |

Đọc bảng:

- 17h ngày làm việc có hộp rộng nhất, nên là giờ khó dự báo nhất.
- Lúc 8h, hộp ngày nghỉ nằm hẳn dưới hộp ngày làm việc. Vì vậy "ngày làm việc hay ngày nghỉ" là thông tin bắt buộc khi dự báo giờ đó.

## 60. Code: số cho heatmap và boxplot
<!-- ma: code-b04-heatmap-boxplot -->

Tính trung bình từng ô lịch cho heatmap và quantile cho hộp của boxplot.

```python
import numpy as np
import pandas as pd

x = np.array([420, 60, 450, 410, 440])   # năm thứ Hai lúc 8h
print(x.mean())                          # bị ngày lễ kéo xuống
print(np.quantile(x, [0.25, 0.5, 0.75], method="inverted_cdf"))

# df: lượt thuê theo giờ, có cột thu, gio, workingday
ho_so = df.pivot_table(index="thu", columns="gio", values="cnt",
                       aggfunc="mean")   # 7 thứ nhân 24 giờ
for lam, g in [(1, 8), (1, 17), (0, 8), (0, 13)]:
    chon = (df["workingday"] == lam) & (df["gio"] == g)
    q = df.loc[chon, "cnt"].quantile([0.25, 0.5, 0.75])  # mép hộp
    print(lam, g, q.round(0).tolist())
```

*Rút gọn từ buoi-04/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `np.quantile(x, q)` (numpy): Số mà q phần dữ liệu nằm dưới nó; q = 0,5 là trung vị.
- `pivot_table(aggfunc="mean")` (pandas): Bảng hai chiều, mỗi ô là trung bình các dòng rơi vào ô đó.
- `quantile([0.25, 0.5, 0.75])` (pandas): Ba số làm nên cái hộp: mép dưới, vạch giữa, mép trên.

**Từng bước:**

- Dòng 4–5: Trung bình bị một ngày lạ kéo lệch.
- Dòng 6: Quantile 0,25, 0,5, 0,75 thì không bị.
- Dòng 9–10: Bảng 7 thứ, 24 giờ: đúng số tô lên heatmap.
- Dòng 11–14: Hộp từng giờ, tách ngày làm việc và ngày nghỉ.

**Kết quả:** Trung bình 356, trung vị 420, hộp 410–440. 8h: T2 412, CN 84. Hộp 8h ngày nghỉ 57–141, ngày làm việc 365–646.

## 61. Lag plot: bám đường chéo là đoán được
<!-- ma: lag-plot -->

*Tiếng Anh: lag plot · autocorrelation at lag k*

Để dự báo giờ tới, ta có thể dựa vào giờ trước, cùng giờ hôm qua hay cùng giờ tuần trước. **Lag plot** giúp chọn: đó là scatter của
$y_t$ theo $y_{t-k}$, mỗi chấm ghép một giá trị với giá trị cách nó $k$ bước về trước ($k$ gọi là **độ trễ**).

$$
(y_{t-k},\ y_t)
$$

Ví dụ chuỗi lặp mỗi 4 bước: 2, 4, 6, 4, 2, 4, 6, 4. Ở trễ 2 được 6 cặp: (2, 6), (4, 4), (6, 2), (4, 4), (2, 6), (4, 4). Trong hình,
trục ngang là $y$ lúc $t - 2$, trục dọc là $y$ lúc $t$: ba chấm nằm trên đường đi xuống, ngược với đường chéo cam. Trễ 2 là nửa vòng
lặp, nên đỉnh 6 ghép với đáy 2 và ngược lại; tự tương quan $r_2 = -0{,}75$.

| Hình dạng | Nghĩa |
|---|---|
| bám đường chéo | giá trị cách $k$ bước đoán tốt hiện tại |
| đi xuống | $k$ bằng nửa vòng: đỉnh ghép với đáy |
| hai nhánh | $r$ chỉ là trung bình hai nhánh |

Lượt thuê theo giờ: ở trễ 168 (cùng giờ tuần trước) đám chấm hẹp nhất quanh đường chéo, $r = 0{,}88$, tốt hơn cả giờ ngay trước và cùng
giờ hôm qua. Ở trễ 12, giờ đông ghép với giờ vắng, đám chấm tách thành hai nhánh đổ theo hai trục, $r = -0{,}14$. Con số này không
phải một "quan hệ âm" dùng được, nên luôn nhìn hình trước khi tin $r$.

## 62. ACF: cách k bước có giống bây giờ không?
<!-- ma: acf -->

*Tiếng Anh: autocorrelation function (ACF) · lag*

**ACF** (tự tương quan) đo giá trị cách k bước giống giá trị hiện tại tới mức nào, từ −1 tới +1:

- Gần +1: trước cao thì nay cũng cao.
- Gần 0: quá khứ không giúp đoán hiện tại.
- Âm: trước cao thì nay thấp.

Ví dụ sáu số 2, 3, 5, 6, 5, 3 cho r₁ ≈ 0,33. Trên lượt thuê xe theo giờ, ACF có đỉnh mỗi 24 giờ, và đỉnh ở 168 và 336 cao
hơn các đỉnh quanh nó: có mùa vụ ngày lồng trong mùa vụ tuần. Lag plot nhìn bằng mắt, ACF đo bằng số.

Ở trễ bằng nửa chu kỳ mùa vụ, đỉnh ghép với đáy nên r nhỏ hoặc âm (lượt thuê xe: r ở trễ 12 là −0,143). Đọc ACF theo vòng lặp, đừng đọc theo dấu của từng cột.

## 63. Code: tự tính ACF và r của lag plot
<!-- ma: code-b04-acf -->

Viết công thức tự tương quan vài dòng, kiểm bằng chuỗi nhỏ rồi chạy trên dữ liệu giờ.

```python
import numpy as np
import pandas as pd

def acf_nhanh(y, so_tre):
    y = np.asarray(y, dtype=float)
    lech = y - np.nanmean(y)             # độ lệch khỏi trung bình
    mau = np.nansum(lech**2)             # mẫu số: cả chuỗi
    return np.array([1.0] + [np.nansum(lech[k:] * lech[:-k]) / mau
                             for k in range(1, so_tre + 1)])

print(acf_nhanh([2, 4, 6, 4, 2, 4, 6, 4], 4).round(2))
r = acf_nhanh(df["cnt"], 336)            # df: lượt thuê theo giờ
for k in (1, 12, 24, 168):               # r của từng lag plot
    cap = pd.DataFrame({"truoc": df["cnt"].shift(k), "sau": df["cnt"]})
    print(k, cap.dropna().corr().iloc[0, 1])
```

*Rút gọn từ buoi-04/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `acf_nhanh(y, so_tre)` (tự viết): Tính r_k cho k = 1, 2, … theo đúng công thức tự tương quan.
- `np.nansum` (numpy): Cộng các phần tử, bỏ qua ô trống thay vì ra NaN.
- `shift(k)` (pandas): Dời chuỗi xuống k bước: giờ t nhận giá trị của giờ t − k.

**Từng bước:**

- Dòng 6–7: Độ lệch từng điểm và tổng bình phương độ lệch.
- Dòng 8–9: Cộng tích lệch bây giờ với lệch k bước trước.
- Dòng 11: Kiểm trên chuỗi 2, 4, 6, 4 lặp lại.
- Dòng 12: ACF 336 giờ, tức hai tuần, trên dữ liệu thật.
- Dòng 13–15: Ghép giờ t với giờ t − k rồi đo tương quan.

**Kết quả:** Chuỗi nhỏ: r₂ = −0,75, r₄ = 0,5. Dữ liệu thật: r₁₆₈ = 0,864 cao hơn r₁₄₄ = 0,786; lag plot trễ 168 cho r = 0,876.

## 64. Trục y cắt, trục kép: thang do người vẽ chọn
<!-- ma: truc-y-cat -->

*Tiếng Anh: truncated y-axis · dual axis · index to 100*

Không sửa con số nào vẫn làm hình nói sai được, vì người vẽ chọn thang. **Trục y cắt** là trục dọc không bắt đầu từ 0. **Trục kép** là
hai trục dọc với hai thang khác nhau trên cùng một hình.

Doanh thu tháng 5 là 490 triệu, tháng 6 là 510 triệu, tăng 4,1%. Độ cao một cột trên hình tính bằng:

$$
\mathrm{độ\ cao} = \frac{\mathrm{giá\ trị} - \mathrm{đáy\ trục}}{\mathrm{đỉnh\ trục} - \mathrm{đáy\ trục}}
$$

Trục từ 480 tới 520 thì tháng 5 cao (490 − 480) / 40 = 25% chiều cao hình, tháng 6 cao (510 − 480) / 40 = 75%. Mắt thấy gấp ba. Hình
ô trái là trục cắt ở 480, ô phải là trục từ 0: hai cột gần bằng nhau, đúng mức tăng khoảng 4%.

Trục kép cũng vậy: chọn thang bên phải hẹp thì hai đường trùng khít, chọn rộng thì một đường nằm ngang. Chỗ hai đường gặp hay tách do
người vẽ quyết định, không do dữ liệu. Nghiên cứu cảm nhận (Correll và cộng sự, 2020) cho thấy trục cắt làm người xem thấy chênh lớn hơn
thật, kể cả khi có ký hiệu báo trục bị cắt.

Quy ước của khoá: số đếm và tổng (cột, lượt thuê, doanh thu) vẽ trục từ 0. Hai chuỗi khác đơn vị thì tách thành hai hình, hoặc **đánh
chỉ số**: chia mỗi chuỗi cho giá trị tháng đầu rồi nhân 100, để cả hai cùng bắt đầu ở 100.

## 65. Trộn nhiều năm vào một scatter làm r yếu đi
<!-- ma: tron-nam -->

*Tiếng Anh: pooling years · level shift · colour by time*

Tương quan nhiệt độ × lượt thuê mỗi ngày tính riêng từng năm đều trên 0,7, nhưng gộp hai năm lại chỉ còn 0,627. Quan hệ không yếu đi.
Lý do là **mức chung** dời lên: năm 2012 có nhiều người dùng hơn, nên cùng nhiệt độ thì lượt thuê cao hơn 2011.

| Tương quan nhiệt độ × lượt/ngày | 2011 | 2012 | gộp hai năm |
|---|---|---|---|
| $r$ | 0,771 | 0,714 | 0,627 |

Gộp hai năm cho $r$ thấp hơn cả hai năm riêng. Hai mức khác nhau chồng lên nhau làm đám điểm dày ra theo chiều dọc, nên quan hệ trông
yếu hơn thật.

Hình là scatter nhiệt độ trung bình ngày (trục ngang) × lượt thuê mỗi ngày (trục dọc), chấm xanh là 2011, chấm cam là 2012. Nhìn một
cột dọc bất kỳ, ví dụ quanh 25 °C: chấm cam nằm trên chấm xanh. Hai đám mây song song, tức quan hệ với nhiệt độ vẫn vậy, chỉ có mức
dời lên theo năm. Trục ngang chỉ nên đọc vị trí tương đối, vì tài liệu của bộ dữ liệu ghi hai cách đổi ra °C khác nhau.

Cách nhận ra: tô màu scatter theo năm (hay theo thời gian). Thấy các đám mây song song thì tính $r$ riêng từng năm, và nhớ rằng phần dời
mức cần mô hình xử lý riêng, nhiệt độ không giải thích được nó.

## 66. Điều chỉnh lịch, lạm phát, dân số
<!-- ma: dieu-chinh -->

*Tiếng Anh: calendar adjustment · CPI deflation (real value) · per capita*

Doanh số tăng có thể vì tháng dài hơn, giá cao hơn, người đông hơn, hoặc mỗi người mua nhiều hơn thật. Ba phép chia bỏ lần lượt
ba nguyên nhân đã biết:

$$
y^{\text{ngày}}_t = \frac{y_t}{\text{số ngày của tháng } t}, \qquad x_t = \frac{y_t}{z_t} \times z_{\text{gốc}}
$$

$z_t$ là CPI lúc $t$, $z_{\text{gốc}}$ là CPI năm gốc; muốn mức mỗi người thì chia thêm cho dân số. Ví dụ doanh thu 100 → 150, CPI
100 → 125, dân số 10 → 12: giá thực 150 / 125 × 100 = 120 (tăng 20%, không phải 50%); mỗi người 100 / 10 = 10 và 120 / 12 = 10,
tức không đổi.

Hình: theo tổng tháng, tháng 2/2023 giảm 3,4% so với tháng 1; chia số ngày thì tăng 7,0%. Dấu của kết luận đảo ngược. Tháng 3 so
với tháng 2/2023: so thẳng +14,15%, chia ngày lịch +3,11%, chia ngày không phải Chủ nhật +1,47%, chuỗi đã điều chỉnh của Census
−1,05%. Không cột nào sai; mỗi cột trả lời một câu hỏi, và báo cáo phải nói đã bỏ những gì.

## 67. Log: cùng % thành cùng khoảng cách
<!-- ma: log -->

*Tiếng Anh: log transformation · multiplicative → additive*

Log biến nhân thành cộng: $\log(a \times b) = \log a + \log b$. Nên $\log(1{,}2\,y) - \log y = \log 1{,}2 = 0{,}182$ với mọi
$y$: cửa hàng nhỏ 100 → 120 và siêu thị 1.000 → 1.200 cách nhau cùng 0,182 trên thang log, dù trên thang gốc một bên chênh 20, một
bên chênh 200. Log chỉ dùng cho số dương.

Log hợp nhất khi dao động tỷ lệ **đúng** với mức. Bán lẻ Mỹ 1992 → 2019: mức gấp khoảng 3,1 lần mà độ lệch chuẩn trong năm chỉ
gấp khoảng 2,4. Dao động tăng chậm hơn mức nên log ép quá tay; Box-Cox (slide sau) cho vặn giữa giữ nguyên và log.

## 68. Box-Cox: núm vặn giữa giữ nguyên và log
<!-- ma: box-cox -->

*Tiếng Anh: Box-Cox transformation · λ (lambda) · Guerrero method · Yeo-Johnson*

**Box-Cox** là một núm vặn λ: λ = 1 gần như giữ nguyên dữ liệu, λ = 0 là log, ở giữa là các mức nén vừa phải. Cách **Guerrero**
chọn λ làm dao động giữa các năm đều nhau nhất. Với bán lẻ Mỹ, Guerrero chọn λ ≈ 0,34. So dao động năm 2019 với năm 1992:

- Không biến đổi: gấp 2,45 lần.
- λ = 0,34: gấp 1,21 lần, gần đều nhất.
- Log: 0,84 lần, tức ép quá tay.

Box-Cox và log cần số dương. Gặp số 0 hay số âm thì dùng Yeo-Johnson. λ là tham số của mô hình, nên tính lại ở mỗi gốc dự báo.

## 69. Guerrero chọn λ làm dao động các năm đều
<!-- ma: guerrero -->

*Tiếng Anh: Guerrero method · coefficient of variation (CV) · Box-Cox λ*

Box-Cox là một "núm vặn" $\lambda$: 1 là gần như giữ nguyên, 0 là log. Với bán lẻ, để nguyên thì dao động phình ra theo mức, lấy log
thì ép quá tay. Cách của Guerrero chọn $\lambda$ ở giữa bằng số, không bằng mắt.

Chia chuỗi thành từng năm. Sau Box-Cox, độ lệch chuẩn của một năm có mức $\mu$ gần bằng $s / \mu^{1-\lambda}$. Ta muốn tỷ số này như
nhau ở mọi năm:

$$
\mathrm{tỷ\ số}_j = \frac{s_j}{\mu_j^{\,1-\lambda}}, \qquad \lambda = \arg\min\ \mathrm{CV}(\mathrm{tỷ\ số})
$$

**CV** (hệ số biến thiên) là độ lệch chuẩn chia trung bình; CV càng nhỏ thì các tỷ số càng đều. Ví dụ ba năm $\mu$ = 100, 400, 900 và
$s$ = 10, 20, 30:

| λ | Tỷ số ba năm | Nghĩa |
|---|---|---|
| 1 | 10, 20, 30 | dao động lớn dần, CV = 10 / 20 = 0,5 |
| 0,5 | 1, 1, 1 | đều hoàn toàn, CV = 0 |
| 0 | 0,1; 0,05; 0,033 | log ép quá tay |

Chẳng hạn $\lambda$ = 0,5, năm $\mu$ = 400, $s$ = 20: 20 / √400 = 1.

Trên bán lẻ Mỹ, ô trái của hình vẽ CV theo $\lambda$ từ −1 tới 2; đáy đường cong ở $\lambda \approx 0{,}34$. Ô phải so dao động mỗi năm
với năm 1992: năm 2019 không biến đổi gấp 2,45 lần, $\lambda$ = 0,34 gấp 1,21, log chỉ 0,84. Lưu ý: `scipy.stats.boxcox` chọn 0,595
theo tiêu chí khác (giống hình chuông nhất). Trong backtest, $\lambda$ là tham số của mô hình, chỉ được tính từ dữ liệu trước gốc dự báo.

## 70. Code: chọn λ Box-Cox bằng Guerrero
<!-- ma: code-b05-guerrero -->

Chọn λ bằng số để dao động mỗi năm đều nhau, rồi so với cách chọn của scipy.

```python
import numpy as np
from scipy import stats

def guerrero(y, m):
    luoi = np.linspace(-1, 2, 3001)            # thử λ từ −1 tới 2
    y = np.asarray(y, dtype=float)
    khoi = y[y.size % m:].reshape(-1, m)       # mỗi dòng một năm
    tb, sd = khoi.mean(axis=1), khoi.std(axis=1, ddof=1)
    ty_so = sd[None, :] / tb[None, :] ** (1 - luoi[:, None])
    cv = ty_so.std(axis=1, ddof=1) / ty_so.mean(axis=1)
    return float(luoi[np.argmin(cv)])          # λ cho tỷ số đều nhất

lam_g = guerrero(y19, 12)                      # y19: bán lẻ 1992 tới 2019
lam_mle = stats.boxcox(y19.to_numpy())[1]      # tiêu chí khác
# tang: % tăng so với cùng tháng năm trước, có số âm
lam_yj = stats.yeojohnson(tang.to_numpy())[1]
```

*Rút gọn từ buoi-05/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `guerrero(y, m)` (tự viết): Thử từng λ, chọn λ làm dao động các năm đều nhau nhất.
- `stats.boxcox` (scipy): Biến đổi Box-Cox và tự chọn λ làm dữ liệu giống hình chuông nhất.
- `stats.yeojohnson` (scipy): Giống Box-Cox nhưng nhận cả số 0 và số âm.

**Từng bước:**

- Dòng 5: Lưới 3.001 giá trị λ để thử.
- Dòng 7–8: Mức và dao động của từng năm.
- Dòng 9–10: Tỷ số mỗi năm và độ đều của chúng (CV).
- Dòng 11: Giữ λ cho CV nhỏ nhất.
- Dòng 14: scipy chọn λ theo tiêu chí hình chuông.
- Dòng 15–16: Chuỗi có số âm thì dùng Yeo-Johnson.

**Kết quả:** λ Guerrero 0,34: dao động 2019 so 1992 còn 1,21 (log ép còn 0,84). scipy chọn 0,595; Yeo-Johnson trên % tăng ra khoảng 1,02.

## 71. Vì sao exp của dự báo log ra trung vị
<!-- ma: exp-trung-vi -->

*Tiếng Anh: back-transformation · median vs mean · bias adjustment*

Dự báo trên thang log xong phải đổi về đơn vị gốc bằng `exp`. Con số nhận được thường thấp hơn trung bình thật, và cộng dồn nhiều tháng
hay nhiều cửa hàng thì phần hụt cộng dồn theo.

Ví dụ ba giá trị log 0, 1, 2 có trung bình 1, đổi ngược được exp(1) ≈ 2,72. Đổi từng giá trị thì được 1; 2,72; 7,39, trung bình thật là
3,70. Vậy 2,72 thấp hơn trung bình, nhưng đúng là số đứng giữa: đó là **trung vị**. Lý do: `exp` giữ thứ tự, nên số đứng giữa vẫn
đứng giữa. Nhưng `exp` kéo giãn phía trên: bước từ 1 lên 2 trên thang log thành 4,67 trên thang gốc, bước từ 0 lên 1 chỉ thành 1,72.
Số lớn bị đẩy xa, kéo trung bình lên. Hình vẽ đúng điều đó: hàng trên ba chấm cách đều, hàng dưới chấm cuối bị đẩy ra 7,39, vạch trung
bình 3,70 nằm bên phải vạch trung vị 2,72.

Hụt bao nhiêu tuỳ độ lệch chuẩn $\sigma$ trên thang log: $\sigma$ = 0,5 thì trung vị thấp hơn trung bình 11,75%, $\sigma$ = 1 thì 39,35%.

| Tình huống | Làm gì |
|---|---|
| cần tổng, trung bình | nhân 1 + σ²/2 |
| chấm bằng MAE | không cần: MAE ưa trung vị |
| σ nhỏ | phần hụt không đáng kể |

Hiệu chỉnh chỉ sửa phần hụt do đổi ngược, không sửa lệch do mô hình. Trên bán lẻ Mỹ theo tháng nó chỉ đẩy dự báo lên cỡ 0,11% tới 1,27%.

## 72. Chuỗi = xu hướng + mùa vụ + phần dư
<!-- ma: phan-ra -->

*Tiếng Anh: decomposition (additive / multiplicative) · residual · STL / MSTL*

**Phân rã** tách chuỗi thành xu hướng, mùa vụ và phần dư (phần còn lại). Có hai kiểu:

- **Cộng**: mùa hè luôn cao hơn mức nền 10 GW, dù nền là 80 hay 150 GW.
- **Nhân**: mùa hè cao hơn một tỷ lệ; nền 100 thì +10, nền 200 thì +20.

Tải điện có hai mùa vụ lồng nhau: nhịp 24 giờ và nhịp 168 giờ (một tuần). **MSTL(24, 168)** tách cả hai. Hình là tháng
7/2024 của vùng PJM: xu hướng trơn, nhịp cuối tuần nằm gọn trong hàng mùa vụ tuần, phần dư chủ yếu là thời tiết.

## 73. Cổ điển, STL, MSTL: mùa vụ cố định hay đổi dần
<!-- ma: phan-ra-cach -->

*Tiếng Anh: classical decomposition · STL · MSTL · LOESS*

**Phân rã cổ điển** làm hai bước: xu hướng là trung bình trượt dài đúng một vòng mùa vụ (2×m-MA khi m chẵn), còn mùa vụ là
trung bình của "dữ liệu trừ xu hướng" theo từng vị trí trong vòng. Kết quả là một khuôn mùa vụ *cố định* cho cả năm.

**STL** làm trơn cục bộ bằng LOESS, nên mùa vụ được phép đổi dần theo thời gian. **MSTL** tách lần lượt nhiều chu kỳ, ví dụ 24 và
168 giờ.

Hình cho thấy vì sao cần mùa vụ đổi dần: mùa vụ ngày của PJM tháng 1 có hai đỉnh (sáng và tối), tháng 7 chỉ một đỉnh chiều, và
biên độ mùa hè lớn hẳn vì điều hoà. Biên độ đổi theo *mùa* không phải lý do để dùng phân rã nhân; phân rã nhân dành cho dao động
tỷ lệ với *mức*. Hai lỗi hay gặp: cửa sổ xu hướng quá ngắn làm xu hướng nuốt cả mùa vụ và thời tiết, nên phần dư nhỏ giả tạo; và
đầu vào còn NaN thì mọi thành phần ra NaN mà không báo lỗi.

## 74. Code: phân rã cổ điển bằng NumPy
<!-- ma: code-b06-co-dien -->

Tự viết phân rã cổ điển trong mười dòng và kiểm nó khớp statsmodels tới từng số.

```python
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

def co_dien(x, m):
    x = np.asarray(x, dtype=float)
    w = np.r_[0.5, np.ones(m - 1), 0.5] / m       # 2×m-MA, tổng bằng 1
    T = np.full(x.size, np.nan)
    T[m // 2:-m // 2] = np.convolve(x, w, mode="valid")  # xu hướng
    pha = np.arange(x.size) % m                   # vị trí trong vòng
    S_mua = np.array([np.nanmean((x - T)[pha == k]) for k in range(m)])
    S = (S_mua - S_mua.mean())[pha]               # mùa vụ, tổng bằng 0
    return T, S, x - T - S                        # phần dư còn lại

x = np.array([22, 18, 15, 29, 30, 22, 19, 33, 30, 26, 23, 37])
T, S, R = co_dien(x, 4)
sm = seasonal_decompose(x, period=4)              # phải khớp T và S
```

*Rút gọn từ buoi-06/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `np.convolve(x, w, mode="valid")` (numpy): Trượt bộ trọng số dọc chuỗi, chỉ giữ chỗ đủ hàng xóm.
- `co_dien(x, m)` (tự viết): Trả về xu hướng, mùa vụ và phần dư theo cách cổ điển.
- `seasonal_decompose` (statsmodels): Phân rã cổ điển có sẵn; kết quả có .trend, .seasonal, .resid.

**Từng bước:**

- Dòng 6: m + 1 trọng số, hai đầu mỗi đầu một nửa.
- Dòng 7–8: Trung bình trượt một vòng: ra xu hướng.
- Dòng 9–10: Trung bình phần trừ xu hướng theo vị trí.
- Dòng 11: Dời cho tổng mùa vụ một vòng bằng 0.
- Dòng 14–16: Chạy trên 12 quý, so với thư viện.

**Kết quả:** Quý 3 có xu hướng 22. Mùa vụ bốn quý 4, −3, −7, 6; phần dư chỉ ±0,5 và ±1,5; khớp seasonal_decompose.

## 75. Code: biên độ trong ngày theo tháng
<!-- ma: code-b06-bien-do -->

Đo biên độ mỗi ngày để biết mùa vụ đổi theo mùa, và bắt một giờ số liệu hỏng.

```python
import pandas as pd

# y: nhu cầu điện PJM theo giờ (MW), giờ New York
# y_goc: cùng chuỗi theo giờ UTC, chưa lấp giờ trống
ngay = y.resample("D")
bd = (ngay.max() - ngay.min()) / 1000        # biên độ trong ngày, GW
theo_thang = bd.groupby(bd.index.month).mean()
print(theo_thang.loc[[1, 4, 7]].round(1))

t0 = pd.Timestamp("2024-11-21 17:00")        # giờ nghi hỏng (UTC)
print(y_goc[t0 - pd.Timedelta("1h"):t0 + pd.Timedelta("1h")])
```

*Rút gọn từ buoi-06/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `resample("D").max()` (pandas): Gom các giờ thành từng ngày và lấy giá trị lớn nhất mỗi ngày.
- `groupby(index.month).mean()` (pandas): Trung bình theo tháng, gộp mọi ngày cùng tháng.
- `pd.Timedelta("1h")` (pandas): Một khoảng thời gian một giờ để cộng trừ với mốc giờ.

**Từng bước:**

- Dòng 5–6: Cao nhất trừ thấp nhất trong mỗi ngày.
- Dòng 7–8: Trung bình biên độ theo từng tháng.
- Dòng 10–11: Xem giờ lạ cùng hai giờ hai bên.

**Kết quả:** Biên độ trong ngày tháng 7 trung bình 44 GW, tháng 1 chỉ 17 GW. 17:00 UTC 21/11 báo 56.260 MW giữa hai giờ khoảng 95.000 MW.

## 76. Tỷ lệ mẫu hình: phần dư còn nhịp lịch không
<!-- ma: ty-le-mau-hinh -->

*Tiếng Anh: residual pattern ratio · calendar grouping*

Phân rã xong, phần dư trông lộn xộn, nhưng có thể vẫn còn nhịp theo giờ, theo tháng. **Tỷ lệ mẫu hình** kiểm điều đó bằng một con số.

Cách làm: nhóm phần dư theo lịch, ví dụ theo (tháng, giờ) hay (thứ, giờ), lấy trung bình mỗi nhóm. Phần dư sạch thì mọi trung bình
nhóm gần 0; còn mẫu hình thì chúng lệch nhau. Đo độ lệch nhau đó bằng phương sai của các trung bình nhóm, rồi chia cho phương sai của
cả chuỗi để so tương đối.

Ví dụ bốn giờ phần dư: sáng −3, −5; chiều +3, +5. Trung bình hai nhóm là −4 và +4, phương sai của chúng là
((−4)² + 4²) / (2 − 1) = 32. Nếu chuỗi có phương sai 320 thì tỷ lệ là 32 / 320 = 0,1: phần dư còn nhịp sáng – chiều. Phân rã khác
cho sáng +2, −2 và chiều +1, −1 thì trung bình nhóm đều 0, tỷ lệ bằng 0.

Trên tải điện PJM năm 2024, nhóm tháng × giờ:

| Phân rã | Tỷ lệ mẫu hình tháng × giờ |
|---|---|
| MSTL (24, 168) | 0,0006: phần dư gần như sạch |
| cổ điển chu kỳ 24 | 0,102: một phần mười còn là mẫu hình |

Hình tô trung bình phần dư theo tháng (trục dọc) × giờ (trục ngang), đỏ là dương, xanh là âm. Cột cổ điển có vệt đỏ vào chiều hè và
sáng đông, cột MSTL gần như trắng. Lưu ý: phân rã chu kỳ 24 còn đẩy nhịp tuần vào xu hướng, nên cần kiểm cả xu hướng theo thứ, không chỉ
phần dư.

## 77. STL: mùa vụ lấy trung bình cục bộ, đổi dần
<!-- ma: stl-loess -->

*Tiếng Anh: STL · LOESS (local regression) · trend window*

Phân rã cổ điển lấy **một** trung bình cho mọi quý 1 của mọi năm, nên mùa vụ năm nào cũng như nhau. Khi mùa vụ lớn dần, khuôn cố định đó
bỏ sót phần thay đổi. STL thay bằng trung bình **cục bộ**: mùa vụ mỗi năm chỉ nhìn vài năm lân cận.

Ví dụ phần "dữ liệu trừ xu hướng" của quý 1 qua năm năm: 2, 4, 6, 8, 10. Cổ điển cho mùa vụ 6 ở mọi năm, phần dư −4, −2, 0, 2, 4: vẫn
còn một đường đi lên. Trung bình 3 năm quanh mỗi năm (năm đầu và cuối chỉ có 2 năm) cho 3, 4, 6, 8, 9, phần dư chỉ từ −1 tới 1. Trong
hình, đường xám cổ điển nằm phẳng ở 6, đường cam cục bộ đi theo các chấm.

STL làm đúng ý đó nhưng dùng **LOESS** thay cho trung bình 3 điểm: ở mỗi điểm, khớp một đường qua các điểm lân cận, điểm gần nặng hơn,
rồi lấy giá trị của đường tại đó. Tham số `seasonal` là số vòng lân cận để làm trơn mùa vụ, `trend` là số điểm lân cận cho xu hướng.

Lưu ý cửa sổ xu hướng: quá ngắn thì xu hướng mềm tới mức ôm luôn nhịp tuần lẫn thời tiết. Trên PJM, `STL(period=24)` mặc định (xu
hướng 47 giờ) để lại phương sai phần dư chỉ 2,8 GW², nhỏ hơn MSTL (16,5 GW²). Phần dư nhỏ ở đây là nhỏ giả tạo, không phải phân rã tốt
hơn.

## 78. Code: STL, MSTL và hai lỗi hay gặp
<!-- ma: code-b06-stl-mstl -->

Chạy STL và MSTL, xem hai lỗi hay gặp, rồi đo mùa vụ ngày đổi theo mùa thế nào.

```python
from statsmodels.tsa.seasonal import MSTL, STL

# y: nhu cầu PJM theo giờ, giờ New York; y_goc: bản còn NaN
bay = MSTL(y_goc, periods=(24, 168)).fit()
print(bay.trend.notna().sum())          # còn NaN là ra toàn NaN

stl = STL(y, period=24).fit()           # xu hướng 47 giờ, quá mềm
ms = MSTL(y, periods=(24, 168)).fit()   # mùa vụ ngày rồi mùa vụ tuần
print(stl.resid.var() / 1e6, ms.resid.var() / 1e6)   # GW bình phương

s24 = ms.seasonal["seasonal_24"]
ho = s24.groupby([s24.index.month, s24.index.hour]).mean().unstack()
bien_do = (ho.max(axis=1) - ho.min(axis=1)) / 1000   # GW theo tháng
print(ho.loc[1].idxmax(), ho.loc[7].idxmax())        # giờ đỉnh
```

*Rút gọn từ buoi-06/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `STL(y, period=24)` (statsmodels): Phân rã bằng làm trơn cục bộ, mùa vụ được đổi dần qua các ngày.
- `MSTL(...).fit().seasonal` (statsmodels): Bảng các mùa vụ, mỗi chu kỳ một cột: seasonal_24, seasonal_168.
- `unstack()` (pandas): Xoay nhãn giờ thành cột: mỗi dòng một tháng, mỗi cột một giờ.

**Từng bước:**

- Dòng 4–5: Lỗi 1: còn giờ trống thì kết quả toàn NaN.
- Dòng 7: Lỗi 2: STL mặc định cho phần dư nhỏ giả tạo.
- Dòng 8–9: MSTL tách hai chu kỳ, so phương sai phần dư.
- Dòng 11–13: Biên độ mùa vụ ngày của từng tháng.
- Dòng 14: Giờ đỉnh mùa đông và mùa hè.

**Kết quả:** Phần dư STL mặc định 2,8 GW², MSTL 16,5 GW². Biên độ mùa vụ ngày tháng 7 là 43,3 GW, tháng 1 là 14,4 GW.

## 79. F_S: mùa vụ mạnh tới đâu so với nhiễu
<!-- ma: f-s -->

*Tiếng Anh: strength of trend F_T · strength of seasonality F_S*

**Độ mạnh mùa vụ F_S** = 1 − Var(phần dư) / Var(mùa vụ + phần dư). Nói bằng lời: 1 trừ đi "phần dư chiếm bao nhiêu phần của mùa vụ
cộng phần dư". Gần 1 là mùa vụ lấn át nhiễu. Hình: cùng một mùa vụ, phần dư nhỏ cho F_S = 0,96, phần dư lớn chỉ 0,34. **F_T**
tính tương tự cho xu hướng.

F phụ thuộc cách phân rã. Trên PJM 2024, F_S của mùa vụ 24 giờ là 0,618 với phân rã cổ điển nhưng 0,829 với MSTL. Vì vậy luôn
ghi kèm tên phương pháp.

## 80. Code: độ mạnh xu hướng và mùa vụ
<!-- ma: code-b06-do-manh -->

Tính F_T và F_S từ phương sai, cho mọi thành phần mùa vụ của một phân rã.

```python
import pandas as pd
from statsmodels.tsa.seasonal import MSTL

def do_manh(bang):
    r = bang["resid"]
    kq = {"F_T": max(0.0, float(1 - r.var() / (bang["trend"] + r).var()))}
    for c in [c for c in bang.columns if c.startswith("seasonal")]:
        kq[c] = max(0.0, float(1 - r.var() / (bang[c] + r).var()))
    return kq

# y: nhu cầu PJM theo giờ, đã lấp giờ trống
kq = MSTL(y, periods=(24, 168)).fit()
ms = pd.DataFrame({"trend": kq.trend, "resid": kq.resid})
ms = ms.join(kq.seasonal)            # thêm seasonal_24, seasonal_168
print(do_manh(ms))                   # so với cùng hàm trên cổ điển
```

*Rút gọn từ buoi-06/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `do_manh(bang)` (tự viết): Trả về F_T và F_S, số từ 0 tới 1, càng gần 1 càng mạnh.
- `var()` (pandas): Phương sai của một cột: nó dao động mạnh cỡ nào.
- `join` (pandas): Ghép thêm cột từ bảng khác theo cùng mốc giờ.

**Từng bước:**

- Dòng 6: F_T: phần dư nhỏ tới đâu so với xu hướng.
- Dòng 7–8: F_S cho từng cột mùa vụ, cùng một phần dư.
- Dòng 12–14: Gom kết quả MSTL vào một bảng.
- Dòng 15: Tính độ mạnh để so giữa các phân rã.

**Kết quả:** F_S của mùa vụ ngày: cổ điển 0,618, MSTL 0,829; mùa vụ tuần của MSTL 0,415. Cùng chuỗi, khác phân rã, khác số.

## 81. Robust: bớt tin điểm có phần dư quá lớn
<!-- ma: robust -->

*Tiếng Anh: robust decomposition · robustness weights (bisquare)*

Không robust, STL cố "giải thích" một giờ hỏng bằng xu hướng và mùa vụ, làm méo chúng ở cả những ngày không lỗi. Robust làm phân
rã hai lượt; lượt sau cho mỗi điểm một trọng số theo phần dư $R$ của lượt trước:

$$
u = \frac{\lvert R \rvert}{6\,\operatorname{median}(\lvert R \rvert)}, \qquad \rho = (1-u^2)^2 \ \text{nếu } u < 1, \qquad \rho = 0 \ \text{nếu } u \ge 1
$$

Phần dư 1, −2, 1, 20, −1: mốc 6 × 1 = 6. Điểm 20 có $u$ ≈ 3,3 nên trọng số 0; điểm −2 có $u$ = 1/3 nên trọng số 0,79. Điểm không
bị xoá: nó nằm lại trong phần dư, đúng chỗ để buổi 11 tìm ngoại lai.

Hình (PJM, giờ 17:00 UTC ngày 21/11/2024 báo 56.260 MW): không robust thì mùa vụ ngày lúc 17:00 UTC của ngày 20/11, ngày không
lỗi, là −4.051 MW; robust là +2.117 MW. Robust cứu được một giờ hỏng, không tách được đợt nắng nóng kéo dài nhiều ngày: muốn tách
thì cần thêm biến nhiệt độ.

## 82. Ba hình dạng ACF cần nhận ra
<!-- ma: acf-ba-hinh -->

*Tiếng Anh: autocorrelation function (ACF) · white noise · ±1,96/√T band*

Hình minh hoạ vẽ từ ba chuỗi mô phỏng (seed 7, 480 điểm): hàng trên là chuỗi, hàng dưới là ACF; dải xám là ±1,96/√T.

- **Nhiễu trắng**: quá khứ không có "ký ức" về tương lai; mọi $r_k$ ($k \ge 1$) quanh 0, trong dải. Thỉnh thoảng một cột chạm ra ngoài
  là bình thường (xem slide Ljung-Box).
- **Xu hướng hoặc random walk**: $r_1$ gần 1, $r_k$ giảm rất chậm khi $k$ tăng: chuỗi chưa dừng. ACF không tách được hai loại này.
- **Mùa vụ**: $r_k$ có đỉnh ở bội số của chu kỳ ($k$ = 24, 48… với dữ liệu giờ), âm ở nửa chu kỳ, khi đỉnh ghép với đáy.

Theo FPP §2.8 và buổi 7, mục 4.1.

## 83. Code: ACF tự viết và ba hình dạng
<!-- ma: code-b07-acf -->

Tự tính ACF bằng vài dòng NumPy, khớp với thư viện, rồi nhìn ba hình dạng cần nhớ.

```python
import numpy as np
from statsmodels.tsa.stattools import acf

def acf_tu_viet(y, so_tre):
    y = np.asarray(y, dtype=float)
    lech = y - np.nanmean(y)                  # độ lệch khỏi trung bình
    mau = np.nansum(lech**2)                  # mẫu: tính trên CẢ chuỗi
    return np.array([1.0] + [np.nansum(lech[k:] * lech[:-k]) / mau
                             for k in range(1, so_tre + 1)])

y = [2, 3, 5, 6, 5, 3]
print(acf_tu_viet(y, 2)[1:])                  # tự viết
print(acf(y, nlags=2, adjusted=False)[1:])    # thư viện, phải ra y hệt
e = np.random.default_rng(42).normal(size=500)
ba = {"nhiễu trắng": e, "random walk": e.cumsum()}
r = {ten: acf_tu_viet(v, 30) for ten, v in ba.items()}
```

*Rút gọn từ buoi-07/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `acf_tu_viet` (tự viết): Hệ số tự tương quan r_k cho các trễ 0 tới so_tre, trễ 0 luôn là 1.
- `acf(y, nlags, adjusted=False)` (statsmodels): Cùng phép tính đó; adjusted=False để chia cho tổng của cả chuỗi.
- `cumsum()` (numpy): Cộng dồn: biến dãy nhiễu thành đường đi của random walk.

**Từng bước:**

- Dòng 6–7: Lấy độ lệch, mẫu số chung cho mọi trễ.
- Dòng 8–9: Mỗi trễ k: cộng tích hai độ lệch cách k bước.
- Dòng 11–13: Ví dụ tay sáu số, so với statsmodels.
- Dòng 14–16: Tính ACF cho nhiễu trắng và random walk.

**Kết quả:** r1 = 0,333 và r2 = −0,417 như tính tay. Nhiễu trắng quanh 0; random walk giảm rất chậm; lượt thuê có đỉnh ở trễ 24, 48.

## 84. Mô hình AR: một phần hôm qua cộng nhiễu
<!-- ma: ar -->

*Tiếng Anh: autoregressive model AR(1) · coefficient ρ (φ)*

**AR(1)** là mô hình nhỏ nhất cho tự tương quan: giá trị mới = ρ × giá trị cũ + một phần ngẫu nhiên. Hệ số ρ (có khi viết φ) nằm
từ −1 tới 1:

- **ρ = 0**: không nhớ gì, là nhiễu trắng.
- **ρ = 0,7**: nhớ hôm qua, nhưng mỗi bước kéo chuỗi một phần về trung bình. Chuỗi dừng.
- **ρ = 1**: random walk, không có mức để quay về.

Ví dụ trung bình 0, đang ở 10, ρ = 0,7: kỳ vọng bước sau là 7, rồi 4,9, dần về 0. Với ρ = 1, kỳ vọng mãi là 10. **AR(p)** dùng p bước
trước. PACF (slide sau) chỉ ra p; ADF kiểm xem ρ có bằng 1 không; prewhitening dùng mô hình AR để lọc.

## 85. PACF: trễ xa còn thêm gì sau trễ gần?
<!-- ma: pacf -->

*Tiếng Anh: partial autocorrelation function (PACF) · AR(1)*

ACF ở trễ 2 lớn có thể chỉ vì hôm nay giống hôm qua, và hôm qua giống hôm kia. **PACF** tách phần đó ra: PACF trễ k là phần tương
quan còn lại sau khi đã bỏ những gì các trễ ngắn hơn giải thích.

Trong hình có bốn chuỗi dựng từ cùng một dãy nhiễu:

- **AR(1) φ = 0,7**: ACF giảm dần; PACF trễ 1 là 0,713, trễ 2 chỉ còn −0,110. Nghĩa là chỉ trễ 1 thật sự quan trọng.
- **Random walk** và **chuỗi có xu hướng**: ACF giảm rất chậm và trông gần như nhau. Chỉ nhìn ACF thì không phân biệt được hai
  loại này, nên cần kiểm định (ADF, KPSS).

## 86. Code: ACF và PACF của bốn chuỗi
<!-- ma: code-b07-pacf -->

Thấy PACF tách được AR(1), còn ACF không phân biệt random walk với xu hướng.

```python
import numpy as np
from statsmodels.tsa.stattools import acf, pacf

e = np.random.default_rng(42).normal(size=500)   # một dãy nhiễu chung
ar = np.empty(500)
ar[0] = e[0]
for t in range(1, 500):
    ar[t] = 0.7 * ar[t - 1] + e[t]               # AR(1), phi = 0,7
bon = {"nhiễu trắng": e, "AR(1)": ar, "random walk": e.cumsum(),
       "xu hướng 0,05t": 0.05 * np.arange(500) + e}
DAI = 1.96 / np.sqrt(500)                        # dải ±1,96/√T
bang = {}
for ten, y in bon.items():
    r = acf(y, nlags=30, adjusted=False)
    p = pacf(y, nlags=30, method="ywm")          # khai method rõ ràng
    bang[ten] = {"r1": r[1], "r30": r[30], "PACF1": p[1], "PACF2": p[2]}
```

*Rút gọn từ buoi-07/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `pacf(y, nlags, method="ywm")` (statsmodels): Tương quan riêng phần: phần còn lại sau khi bỏ các trễ ngắn hơn.
- `acf(y, nlags)` (statsmodels): Hệ số tự tương quan r_k cho từng trễ k.
- `np.empty(n)` (numpy): Tạo mảng n chỗ trống để điền dần từng bước.

**Từng bước:**

- Dòng 4–8: Dựng AR(1): hôm nay bằng 0,7 lần hôm qua.
- Dòng 9–10: Bốn chuỗi dùng chung một dãy nhiễu.
- Dòng 11: Dải để xem cột nào đáng chú ý.
- Dòng 14–16: Tính ACF, PACF và giữ vài con số.
- Dòng 15: Khai method vì mặc định hai hàm khác nhau.

**Kết quả:** AR(1): ACF giảm nhanh, PACF cắt sau trễ 1. Random walk và xu hướng đều có r1 gần 0,98: chỉ nhìn ACF không phân biệt được.

## 87. Đừng đếm cột vượt dải: dùng Ljung-Box
<!-- ma: ljung-box -->

*Tiếng Anh: Ljung–Box test · white noise · model_df*

Trên hình ACF có dải ±1,96/√T; một cột vượt dải chưa phải bằng chứng. Mô phỏng 1.000 chuỗi nhiễu trắng thuần: trung bình mỗi chuỗi
có 0,95 cột vượt dải trong 20 trễ, và 62% số chuỗi có ít nhất một cột vượt. **Ljung-Box** gộp nhiều trễ vào một kiểm định, với H0 là
chuỗi là nhiễu trắng. Dùng nó để kiểm phần dư của mô hình đã "sạch" chưa. Nhớ truyền `model_df` (số tham số của mô hình) khi kiểm
sai số của mô hình.

## 88. Q* vượt ngưỡng χ² mới là còn quy luật
<!-- ma: ljung-box-q -->

*Tiếng Anh: Ljung–Box Q* · χ² distribution · degrees of freedom (model_df)*

Ljung-Box gộp tự tương quan của nhiều trễ thành một con số $Q^*$. Nhưng $Q^*$ = 5,16 là lớn hay nhỏ? Phải so với một ngưỡng.

Nếu chuỗi là **nhiễu trắng** (mọi tự tương quan thật bằng 0), $Q^*$ theo **phân phối $\chi^2$** ("khi bình phương"): phân phối của
tổng bình phương vài số ngẫu nhiên hình chuông. **Bậc tự do** là số trễ gộp vào, trừ đi số tham số nếu đang kiểm sai số của một mô hình
đã ước lượng.

$$
Q^* = T(T+2)\sum_{k=1}^{\ell} \frac{r_k^2}{T-k} \quad \text{so với ngưỡng}\ \ \chi^2_{\ell - p}
$$

$T$ là số điểm, $\ell$ là số trễ, $p$ là số tham số mô hình.

| Bậc tự do | Ngưỡng 5% của χ² |
|---|---|
| 2 | 5,99 |
| 8 | 15,51 |
| 10 | 18,31 |

Ví dụ chuỗi 100 điểm, $r_1$ = 0,2, $r_2$ = 0,1: $Q^*$ = 100 × 102 × (0,2²/99 + 0,1²/98) ≈ 5,16. Với 2 trễ, ngưỡng là 5,99; 5,16
nhỏ hơn nên chưa bác bỏ nhiễu trắng (p ≈ 0,076). Hình vẽ đường cong $\chi^2$ với 2 bậc tự do: vùng đỏ là 5% giá trị lớn nhất, bắt đầu
từ 5,99, và vạch xanh $Q^*$ = 5,16 chưa chạm vào đó.

Lưu ý: kiểm 10 trễ trên sai số của mô hình có 2 tham số thì còn 8 bậc tự do, truyền `model_df=2` cho `acorr_ljungbox`. Quên trừ thì so
với ngưỡng 18,31 thay vì 15,51, p-value lớn hơn thật và dễ kết luận nhầm là sai số đã sạch.

## 89. Code: gộp nhiều r_k bằng Ljung-Box
<!-- ma: code-b07-ljung-box -->

Thay việc đếm cột vượt dải bằng một con số Q* và một p-value.

```python
import numpy as np
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

T, r = 100, np.array([0.2, 0.1])                 # ví dụ tay: 100 điểm
Q = T * (T + 2) * np.sum(r**2 / (T - np.arange(1, 3)))
nguong = stats.chi2.ppf(0.95, 2)                 # ngưỡng 5%, 2 bậc tự do
p = stats.chi2.sf(Q, 2)

for s in (1, 2, 3):
    nhieu = np.random.default_rng(s).normal(size=500)
    kq0 = acorr_ljungbox(nhieu, lags=[10])
    # nếu là sai số của mô hình 2 tham số: trừ bậc tự do
    kq2 = acorr_ljungbox(nhieu, lags=[10], model_df=2)
    print(kq0["lb_pvalue"].iloc[0], kq2["lb_pvalue"].iloc[0])
```

*Rút gọn từ buoi-07/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `acorr_ljungbox(y, lags, model_df)` (statsmodels): Kiểm định Ljung-Box, trả bảng có cột lb_stat và lb_pvalue.
- `stats.chi2.ppf(0.95, df)` (scipy): Ngưỡng mà chỉ 5% giá trị của phân phối vượt qua.
- `stats.chi2.sf(Q, df)` (scipy): p-value: xác suất gặp Q lớn cỡ này nếu là nhiễu trắng.

**Từng bước:**

- Dòng 5–6: Tính Q* bằng tay theo công thức.
- Dòng 7–8: Tra ngưỡng và p từ phân phối khi bình phương.
- Dòng 10–12: Kiểm 10 trễ trên ba chuỗi nhiễu trắng.
- Dòng 14: model_df=2 khi kiểm sai số của mô hình.

**Kết quả:** Ví dụ tay Q* = 5,16 < 5,99: không bác bỏ. Ba chuỗi nhiễu cho p từ 0,081 tới 0,885; model_df=2 làm p nhỏ đi.

## 90. Chuỗi dừng: mức và dao động không đổi
<!-- ma: dung -->

*Tiếng Anh: stationarity · white noise · random walk · trend-stationary*

**Nhiễu trắng** là chuỗi ngẫu nhiên thuần: quá khứ không có "ký ức" gì về tương lai, ACF quanh 0. Chuỗi **dừng** có mức
trung bình và độ dao động ổn định theo thời gian. Ba ví dụ đời thường:

- **Nhiệt độ phòng có máy lạnh đặt 25 °C**: lúc 24,5, lúc 25,8, nhưng luôn bị kéo về 25. Đây là chuỗi **dừng**.
- **Chiều cao một đứa trẻ**: tăng đều theo tuổi. Đây là **dừng quanh xu hướng**; bỏ đường xu hướng đi thì phần còn lại dừng.
- **Tung đồng xu rồi bước tới hoặc lùi**: không có vị trí nào để quay về. Đây là **random walk**, không dừng.

Cách xử lý: random walk thì sai phân (lấy hiệu hai bước liền nhau); dừng quanh xu hướng thì khử xu hướng. Nhìn hình thì khó
phân biệt hai loại này, nên phải kiểm bằng hai kiểm định ADF và KPSS: slide ngay sau.

Hai điều hay bị bỏ qua: chuỗi có chu kỳ (lên xuống không đều) vẫn có thể dừng; và với random walk, dự báo tốt nhất đơn giản là naive (giá trị cuối).

## 91. Random walk: càng lâu càng có thể đi xa
<!-- ma: random-walk -->

*Tiếng Anh: random walk · variance grows with √n · naive forecast*

Số liệu tăng vài tháng liền chưa chắc có xu hướng thật; có thể chỉ là các bước ngẫu nhiên cộng dồn. Đó là **random walk**: vị trí mới
bằng vị trí cũ cộng một bước ngẫu nhiên.

$$
y_t = y_{t-1} + \varepsilon_t, \qquad \mathrm{độ\ lệch\ chuẩn\ sau}\ n\ \mathrm{bước} \propto \sqrt{n}
$$

$\varepsilon_t$ là bước ngẫu nhiên ở thời điểm $t$. Ví dụ tung đồng xu, ngửa tiến 1, sấp lùi 1. Sáu lần tung +1, −1, +1, +1, −1, +1
cho vị trí 1, 0, 1, 2, 1, 2.

Random walk không có mức nào để quay về, nên càng đi lâu càng có thể xa điểm xuất phát. Mô phỏng 10.000 người (seed 7):

| Số bước | Độ lệch chuẩn của vị trí |
|---|---|
| 4 | 2,0 |
| 25 | 5,0 |
| 100 | 10,1 |

Số bước gấp 25 lần thì độ lệch chuẩn gấp √25 = 5 lần: độ dao động tăng theo căn bậc hai số bước. Trong hình, trục ngang là số bước,
trục dọc là vị trí, mỗi đường xám là một người; hai đường cam đứt là ± một độ lệch chuẩn, nở dần ra.

Vì độ dao động đổi theo thời gian, random walk **không dừng** (các tính chất thống kê phụ thuộc thời điểm quan sát). Cách chữa là sai
phân: $y_t - y_{t-1}$ ra lại chính các bước ngẫu nhiên. Dự báo tốt nhất cho random walk là giá trị cuối cùng (dự báo naive). Trừ một
đường thẳng khỏi nó thì phần còn lại vẫn lang thang.

## 92. Bốn chuỗi mẫu: nhớ gì, có dừng không
<!-- ma: bon-chuoi -->

*Tiếng Anh: white noise · AR(1) · random walk · trend-stationary*

| Chuỗi | Nhớ quá khứ? | Dừng? | $r_1$ / $r_{30}$ | Chữa |
|---|---|---|---|---|
| nhiễu trắng $y_t = \varepsilon_t$ | không | có | 0,10 / −0,05 | không cần |
| AR(1) $y_t = 0{,}7\,y_{t-1} + \varepsilon_t$ | nhớ, rồi kéo về mức | có | 0,71 / −0,03 | không cần |
| random walk $y_t = y_{t-1} + \varepsilon_t$ | nhớ mãi, không quay về | không | 0,98 / 0,53 | sai phân |
| xu hướng $y_t = 0{,}05\,t + \varepsilon_t$ | không; bám một đường | quanh đường xu hướng | 0,98 / 0,81 | khử xu hướng |

Mô phỏng 500 điểm, seed 42 (buổi 7, mục 4.2). Random walk và xu hướng có $r_1$ như nhau và ACF giảm chậm như nhau, nên ACF không
tách được hai loại; phải chạy ADF và KPSS dạng "ct". Chữa nhầm: sai phân chuỗi quanh xu hướng là sai phân thừa, sinh tương quan âm
giả; trừ đường thẳng khỏi random walk thì phần còn lại vẫn lang thang. Mẹo nhớ: random walk thì sai phân, dừng quanh xu hướng thì
khử xu hướng.

## 93. Code: hai loại không dừng, hai thuốc
<!-- ma: code-b07-random-walk -->

Thấy random walk dao động to dần, và mỗi loại không dừng cần một cách chữa riêng.

```python
import numpy as np
from statsmodels.tsa.stattools import acf

# 10.000 người tung đồng xu, mỗi người 100 bước
buoc = np.random.default_rng(7).choice([-1, 1], size=(10_000, 100))
vi_tri = buoc.cumsum(axis=1)
do_lech = vi_tri[:, [3, 24, 99]].std(axis=0)     # sau 4, 25, 100 bước

e = np.random.default_rng(42).normal(size=500)
t = np.arange(500)
for y in (e.cumsum(), 0.05 * t + e):             # random walk, xu hướng
    khu_xh = y - np.polyval(np.polyfit(t, y, 1), t)   # trừ đường thẳng
    sai_phan = np.diff(y)                             # y_t trừ y_(t-1)
    print(acf(khu_xh, nlags=1)[1], acf(sai_phan, nlags=1)[1])
```

*Rút gọn từ buoi-07/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `np.polyfit(t, y, 1)` (numpy): Tìm đường thẳng khớp dữ liệu nhất, trả độ dốc và hệ số chặn.
- `np.polyval(he_so, t)` (numpy): Tính giá trị của đường thẳng đó tại từng thời điểm t.
- `np.diff(y)` (numpy): Sai phân: hiệu của mỗi giá trị với giá trị ngay trước.

**Từng bước:**

- Dòng 4–6: Mô phỏng 10.000 người bước ngẫu nhiên.
- Dòng 7: Đo độ dao động ở ba thời điểm.
- Dòng 11: Thuốc một: khử xu hướng bằng đường thẳng.
- Dòng 12: Thuốc hai: sai phân.
- Dòng 13: r1 phần còn lại cho biết thuốc có hợp không.

**Kết quả:** Số bước gấp 25 lần thì độ lệch chuẩn gấp 5 lần (2,0 lên 10,1). Khử xu hướng random walk: r1 vẫn rất lớn; sai phân chuỗi xu hướng: r1 âm rõ.

## 94. ADF và KPSS là gì: hai câu hỏi ngược chiều
<!-- ma: adf-kpss-la-gi -->

*Tiếng Anh: augmented Dickey–Fuller (ADF) · KPSS · unit root · null hypothesis H0*

Muốn quyết định chuỗi có cần sai phân không, cần một con số trả lời: chuỗi có thành phần random walk không. Có hai kiểm định hỏi theo
hai chiều ngược nhau:

- **ADF** hỏi: khi chuỗi đang cao hơn mức thường, bước kế tiếp có bị kéo xuống không? Nếu có, chuỗi có lực kéo về một mức, tức là
  dừng. Giả định ban đầu (H0) của ADF là chuỗi *không dừng*, nên p < 0,05 nghĩa là có bằng chứng chuỗi dừng.
- **KPSS** giả định ban đầu ngược lại: chuỗi *dừng*. p < 0,05 nghĩa là có bằng chứng chuỗi không dừng.

Hình minh hoạ ý của ADF. Mỗi chấm là một bước: trục ngang là chuỗi đang cao hay thấp so với mức thường, trục dọc là bước kế tiếp.
Chuỗi dừng có đám chấm dốc xuống; random walk thì nằm ngang.

Ví dụ tính tay:

- Chuỗi 5, 8, 4, 6, 5: cứ cao hơn 5 là bước sau đi xuống, có lực kéo về.
- Chuỗi 5, 6, 7, 6, 7: độ cao hiện tại không đoán được bước sau, giống random walk.

Tên gọi "nghiệm đơn vị" đến từ công thức y_t = ρ·y_(t−1) + nhiễu. ρ = 1 là random walk; ρ nhỏ hơn 1 thì mỗi bước kéo chuỗi một phần
về trung bình.

## 95. Chạy cả ADF và KPSS, rồi đọc bảng 2 × 2
<!-- ma: adf-kpss -->

*Tiếng Anh: ADF · KPSS · regression="c" / "ct"*

Hai kiểm định có giả thuyết ngược nhau:

| | H0 (giả định mặc định) | p < 0,05 nghĩa là |
|---|---|---|
| ADF | không dừng (có nghiệm đơn vị) | có bằng chứng chuỗi dừng |
| KPSS | dừng | có bằng chứng chuỗi không dừng |

Chạy cả hai, cùng một **dạng**: "c" hỏi dừng quanh một mức, "ct" hỏi dừng quanh một đường xu hướng. Rồi đọc bảng 2 × 2:

- ADF bác bỏ, KPSS không bác bỏ → **dừng**, không cần sai phân.
- ADF không bác bỏ, KPSS bác bỏ → **không dừng**: sai phân rồi kiểm lại.
- Cả hai cùng bác bỏ → **mâu thuẫn**: thường do cú sốc, đổi mức, hay độ dao động đổi theo thời gian. Vẽ chuỗi, thử đoạn không có cú sốc.
- Cả hai không bác bỏ → **chưa đủ bằng chứng**: dữ liệu ngắn, hoặc chuỗi rất gần random walk.

Dữ liệu thật: tăng trưởng GDP Mỹ theo quý. Cả giai đoạn 1947–2026 có ADF p = 0,000 và KPSS p = 0,048, rơi vào ô mâu thuẫn. Chỉ lấy
1985–2019 (bỏ giai đoạn dao động mạnh và cú sốc đại dịch) thì hai kiểm định đồng ý "dừng". p-value của KPSS bị cắt ở 0,01 và 0,1:
"p = 0,10" nghĩa là "p ≥ 0,1", không phải "rất dừng".

## 96. ADF, KPSS trên bốn chuỗi: “c” hay “ct”
<!-- ma: adf-kpss-bon-chuoi -->

| Chuỗi (500 điểm, seed 42) | ADF c | KPSS c | ADF ct | KPSS ct | Kết luận |
|---|---|---|---|---|---|
| nhiễu trắng | 0,000 | ≥ 0,10 | 0,000 | ≥ 0,10 | dừng |
| AR(1) φ = 0,7 | 0,000 | ≥ 0,10 | 0,000 | ≥ 0,10 | dừng |
| random walk | 0,073 | ≤ 0,01 | 0,214 | ≤ 0,01 | không dừng → sai phân |
| xu hướng 0,05t | 0,906 | ≤ 0,01 | 0,000 | ≥ 0,10 | dừng quanh xu hướng → khử xu hướng |

Dòng 4: dạng "c" bảo sai phân; chỉ dạng "ct" mới thấy đúng bản chất. Dòng 3: ADF p = 0,073, dùng mức 10% sẽ gọi nhầm là dừng;
KPSS bắt được. ADF hay bỏ sót chuỗi dừng mà rất gần random walk, nên "không bác bỏ" chưa phải là chứng minh. p của KPSS bị cắt ở
0,01 và 0,1 (statsmodels báo `InterpolationWarning`): "p = 0,10" nghĩa là "p ≥ 0,1". Số liệu: buổi 7, mục 4.5.

## 97. Code: ADF + KPSS và bảng 2 × 2
<!-- ma: code-b07-adf-kpss -->

Chạy hai kiểm định có giả thuyết ngược nhau, cùng dạng, rồi đọc kết luận từ bảng.

```python
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss

def kiem_dinh(y, dang="c"):      # "c": quanh một mức, "ct": quanh đường
    y = np.asarray(y, dtype=float)
    p_adf = adfuller(y, regression=dang, autolag="AIC",
                     result_object=True).pvalue
    p_kpss = kpss(y, regression=dang, nlags="auto",
                  result_object=True).pvalue
    return p_adf, p_kpss
def o_bang(p_adf, p_kpss):       # ADF bác bỏ? KPSS bác bỏ?
    ten = {(True, False): "dừng", (False, True): "không dừng",
           (True, True): "mâu thuẫn", (False, False): "không đủ bằng chứng"}
    return ten[(p_adf < 0.05, p_kpss < 0.05)]
y = 0.05 * np.arange(500) + np.random.default_rng(42).normal(size=500)
kq = {d: o_bang(*kiem_dinh(y, d)) for d in ("c", "ct")}   # hai dạng
```

*Rút gọn từ buoi-07/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `adfuller(y, regression, autolag)` (statsmodels): Kiểm định ADF; giả thuyết gốc là có nghiệm đơn vị (không dừng).
- `kpss(y, regression, nlags)` (statsmodels): Kiểm định KPSS; giả thuyết gốc là dừng, p bị cắt ở 0,01 và 0,1.
- `o_bang` (tự viết): Đổi cặp p-value thành một trong bốn kết luận.

**Từng bước:**

- Dòng 4: Dạng kiểm định phải khai rõ, cả hai dùng chung.
- Dòng 6–7: ADF: p nhỏ là có bằng chứng dừng.
- Dòng 8–9: KPSS: p nhỏ là có bằng chứng không dừng.
- Dòng 11–14: Ghép hai kết quả thành một ô của bảng 2 × 2.
- Dòng 15–16: Thử chuỗi xu hướng với dạng c và ct.

**Kết quả:** Xu hướng 0,05t: dạng c nói không dừng, chỉ dạng ct cho thấy chuỗi dừng quanh xu hướng. Random walk có ADF p = 0,073; KPSS bắt được.

## 98. Sai phân: nhìn vào thay đổi thay vì mức
<!-- ma: sai-phan-la-gi -->

*Tiếng Anh: differencing · seasonal differencing · detrending*

**Sai phân** thay mỗi giá trị bằng hiệu với giá trị trước: y_t − y_(t−1). Ví dụ 100, 103, 105 thành 3, 2. **Sai phân mùa vụ** lấy
hiệu với cùng vị trí ở vòng trước: y_t − y_(t−m), ví dụ tháng này trừ cùng tháng năm ngoái.

Sai phân biến một chuỗi trôi đi (random walk) thành chuỗi các bước thay đổi, vốn có mức để quay về. Hình: log GDP thực của Mỹ trôi lên
mãi, còn sai phân log (gần bằng phần trăm tăng mỗi quý) dao động quanh 0,76%.

Khi nào dùng:

- **Random walk**: sai phân một lần.
- **Chuỗi có mùa vụ**: sai phân mùa vụ trước.
- **Chuỗi dừng quanh một đường xu hướng**: khử xu hướng (lấy chuỗi trừ đường xu hướng), không sai phân. Sai phân thêm thì thừa, xem
  slide "Sai phân thừa".

## 99. Sai phân bao nhiêu lần là đủ
<!-- ma: sai-phan-bao-nhieu -->

Chuỗi đã dừng 2, −1, 0, 1, −2, 0 (độ lệch chuẩn ≈ 1,41), sai phân ra −3, 1, 1, −3, 2: độ lệch chuẩn ≈ 2,41 và $r_1$ ≈ −0,50.
Mỗi số gốc có mặt trong hai hiệu liền nhau với hai dấu ngược nhau. **Hai dấu hiệu sai phân thừa**: $r_1$ của chuỗi đã sai phân gần
−0,5; độ lệch chuẩn tăng. Quy tắc FPP: sai phân tiếp chừng nào KPSS còn bác bỏ, rồi kiểm hai dấu hiệu.

GDP Mỹ: sai phân log một lần ra tăng trưởng; lần hai cho $r_1$ = −0,488 và độ lệch chuẩn 1,105 → 1,455, nên dừng ở một lần.

Có mùa vụ thì sai phân mùa vụ $y_t - y_{t-m}$ trước. Lượt thuê theo giờ, thang log, $m$ = 168:

| Chuỗi | $r_1$ | $r_{24}$ | $r_{168}$ | Độ lệch chuẩn |
|---|---|---|---|---|
| log | 0,898 | 0,863 | 0,896 | 1,430 |
| sai phân thường | 0,493 | 0,676 | 0,767 | 0,643 |
| sai phân mùa vụ 168 | 0,732 | 0,161 | −0,465 | 0,589 |
| 168 rồi sai phân thường | −0,249 | 0,028 | −0,498 | 0,427 |

Chỉ sai phân thường thì mùa vụ còn nguyên; sai phân mùa vụ bỏ được nhịp ngày và tuần. Số liệu: buổi 7, mục 4.6.

## 100. Gặp một chuỗi lạ: bảy bước của buổi 7
<!-- ma: quy-trinh-chuoi-la -->

1. **Nhìn ACF**: quanh 0 là nhiễu trắng; giảm rất chậm là chưa dừng; có đỉnh đều là mùa vụ.
2. **Nhìn PACF**: cao ở vài trễ đầu rồi tắt hẳn sau trễ p thì giống AR(p).
3. **Ljung-Box**: một p-value cho nhiều trễ; p < 0,05 là còn quy luật. Không đếm cột vượt dải.
4. **ADF và KPSS**: chạy cả hai, cùng dạng: "c" nếu chuỗi quanh một mức, "ct" nếu quanh một đường.
5. **Đọc bảng 2 × 2**: hai kiểm định cùng hướng thì tin; mâu thuẫn thì vẽ chuỗi, tìm cú sốc hay đổi mức.
6. **Chữa**: random walk thì sai phân; quanh xu hướng thì khử xu hướng; có mùa vụ thì sai phân mùa vụ trước.
7. **Kiểm chữa quá tay**: sai phân xong mà $r_1$ về gần −0,5, hoặc độ lệch chuẩn tăng, thì bớt một lần.

## 101. Vẽ scatter trước khi tin r
<!-- ma: scatter -->

*Tiếng Anh: scatter plot · Pearson / Spearman correlation · Anscombe's quartet*

Hệ số tương quan **r** (Pearson) chỉ đo quan hệ đường thẳng; **Spearman** đo hai biến có cùng tăng theo thứ hạng không.
Hình chữ U đối xứng cho cả hai bằng 0 dù quan hệ rất chặt. Bộ tứ Anscombe là bốn bộ dữ liệu có cùng r = 0,82 và cùng đường hồi
quy, nhưng là bốn câu chuyện khác nhau:

1. Quan hệ thẳng có nhiễu.
2. Một đường cong.
3. Quan hệ thẳng chặt, có một điểm lạ.
4. Một cột điểm cộng một điểm kéo lệch cả đường.

Quy tắc: luôn vẽ scatter trước khi tin r. Tương quan không phải nhân quả. Kiểm định Granger chỉ nói một chuỗi "giúp dự báo"
chuỗi kia, không nói "gây ra".

## 102. Code: hệ số r và tự tương quan
<!-- ma: code-b02-tuong-quan -->

Đo r bằng NumPy, thấy r bỏ sót quan hệ cong, và cao giả khi có biến gây nhiễu.

```python
import numpy as np

xu = np.array([-2, -1, 0, 1, 2])
np.corrcoef(xu, xu**2)[0, 1]                   # cong hoàn toàn mà r = 0
# h: bảng lượt thuê theo giờ, có cột temp, hr, cnt
g17 = h[h.hr == 17]                            # giữ cố định giờ
r_nhiet = np.corrcoef(h.temp, h.cnt)[0, 1]
r_nhiet_17 = np.corrcoef(g17.temp, g17.cnt)[0, 1]
r_gio = np.corrcoef(h.hr, h.cnt)[0, 1]         # mạnh nhưng cong
y = h["cnt"].to_numpy(float)
dc = y - y.mean()                              # độ lệch khỏi trung bình
tu_tq = (dc[1:] * dc[:-1]).sum() / (dc**2).sum()   # giờ này, giờ trước
```

*Rút gọn từ buoi-02/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `np.corrcoef(x, y)[0, 1]` (numpy): Trả bảng 2 × 2 hệ số r; ô [0, 1] là r giữa x và y.
- `h[h.hr == 17]` (pandas): Lọc giữ các dòng thoả điều kiện, ở đây là giờ 17.
- `dc[1:] * dc[:-1]` (numpy): Nhân mỗi điểm với điểm ngay trước nó, để đo giống nhau.

**Từng bước:**

- Dòng 3–4: y = x² phụ thuộc hẳn vào x mà r bằng 0.
- Dòng 6–8: r nhiệt độ: mọi giờ, rồi chỉ lúc 17h.
- Dòng 9: Giờ trong ngày quyết định mạnh nhưng r thấp.
- Dòng 10–12: Tự tương quan trễ 1 tính tay bằng NumPy.

**Kết quả:** y = x² cho r = 0. Nhiệt độ: mọi giờ r = 0,405, chỉ 17h r = 0,588. Giờ trong ngày r = 0,394. Tự tương quan trễ 1: 0,844.

## 103. Spearman: cùng tăng là đủ, không cần thẳng
<!-- ma: spearman -->

*Tiếng Anh: Spearman rank correlation · Kendall τ · Pearson r*

Pearson đo hai biến nằm gần một **đường thẳng** tới đâu. Nhiều khi ta chỉ cần biết "x tăng thì y có tăng không", dù tăng theo đường
cong. **Spearman** làm việc đó: xếp hạng từng biến (giá trị nhỏ nhất là hạng 1), rồi tính Pearson trên các hạng. **Kendall** cũng dùng
hạng, nhưng đếm số cặp điểm cùng chiều; khi mẫu nhỏ nó ít bị vài điểm lạ kéo đi.

- $x$ = 1, 2, 3, 4, 5 và $y = x^2$ = 1, 4, 9, 16, 25: $y$ luôn tăng nhưng cong. Pearson = 0,981, chưa tới 1; hai dãy hạng trùng nhau nên
  Spearman = 1.
- $x$ = −2, −1, 0, 1, 2 và $y$ = 4, 1, 0, 1, 4 (hình chữ U): cả Pearson lẫn Spearman bằng 0, dù $y$ hoàn toàn xác định bởi $x$.

Vậy Spearman bắt được quan hệ cong mà vẫn cùng chiều, nhưng cũng bỏ sót chữ U. Cả hai chỉ là một con số, nên luôn vẽ scatter trước.

## 104. Code: Pearson, Spearman và Anscombe
<!-- ma: code-b08-anscombe -->

Thấy một hệ số tương quan giấu được cả hình dạng, nên luôn phải vẽ trước.

```python
import numpy as np
from scipy import stats

for x in (np.arange(1, 6), np.arange(-2, 3)):     # y = x² trên hai khoảng
    print(stats.pearsonr(x, x**2)[0], stats.spearmanr(x, x**2)[0])

X0 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ANSCOMBE = {
    "I": (X0, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84,
               4.82, 5.68]),
    "IV": ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
           [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91,
            6.89]),
}                                                 # bộ II, III tương tự
for ten, (x, y) in ANSCOMBE.items():
    print(ten, stats.pearsonr(x, y)[0], stats.spearmanr(x, y)[0])
```

*Rút gọn từ buoi-08/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `stats.pearsonr(x, y)` (scipy): Tương quan Pearson: đo quan hệ theo đường thẳng, kèm p-value.
- `stats.spearmanr(x, y)` (scipy): Tương quan trên thứ hạng: đo quan hệ cùng tăng, dù cong.

**Từng bước:**

- Dòng 4–5: Chữ U: Pearson ra 0 dù y phụ thuộc hẳn vào x.
- Dòng 7–14: Hai trong bốn bộ Anscombe, rất khác hình.
- Dòng 15–16: Tính hai hệ số cho từng bộ để so.

**Kết quả:** Với x từ −2 tới 2, y = x²: Pearson 0. Bốn bộ Anscombe cùng Pearson 0,82 nhưng Spearman từ 0,5 tới 0,99: bốn câu chuyện khác nhau.

## 105. Durbin–Watson: phần dư đổi chậm là đáng ngờ
<!-- ma: durbin-watson -->

*Tiếng Anh: Durbin–Watson statistic · regression residuals · spurious regression*

Hồi quy chuỗi này theo chuỗi kia, rồi xem **phần dư**: phần mà đường thẳng không giải thích được. Nếu phần dư lên một tràng rồi xuống
một tràng, mô hình đang bỏ sót cấu trúc thời gian. Durbin–Watson đo điều đó:

$$
DW = \frac{\sum_{t=2}^{T}(e_t - e_{t-1})^2}{\sum_{t=1}^{T} e_t^2}
$$

Tử số là tổng bình phương bước nhảy giữa hai phần dư liền nhau, mẫu số là tổng bình phương phần dư. Phần dư đổi chậm thì bước nhảy nhỏ, DW
gần 0; phần dư lộn xộn thì DW gần 2. Ví dụ: phần dư 1, 1, 1, −1, −1, −1 chỉ có một bước nhảy cỡ 2, nên DW = 4 / 6 ≈ 0,67; phần dư 1, −1, 1,
−1, 1, −1 có năm bước nhảy, DW = 20 / 6 ≈ 3,33.

CPI theo dân số Mỹ 1990–2024: $R^2$ = 0,9495, $t$ = 88,6, trông như quan hệ rất mạnh, nhưng DW = 0,0051. DW gần 0 nghĩa là giả định "sai số
độc lập" bị vi phạm, nên $t$ và p-value ở trên không đáng tin. $R^2$ cao đi cùng DW thấp là dấu hiệu của hồi quy giả (Granger và Newbold,
1974). Kiểm lại bằng tương quan sau sai phân (slide "r = 0,97 chưa chắc là quan hệ thật").

## 106. CDD, HDD: tách chữ U thành hai nhánh thẳng
<!-- ma: cdd-hdd -->

*Tiếng Anh: cooling / heating degree days (CDD / HDD) · base temperature 65 °F*

Trời lạnh bật sưởi, trời nóng bật điều hoà: tải điện tăng ở cả hai phía. Một đường thẳng theo nhiệt độ không tả được điều đó. Cách
làm của ngành năng lượng là tạo hai biến mới quanh một **mốc**, 18,33 °C (65 °F, mốc của cơ quan năng lượng Mỹ EIA):

$$
\text{CDD} = \max(0,\ T - 18{,}33), \qquad \text{HDD} = \max(0,\ 18{,}33 - T)
$$

CDD là số độ nóng hơn mốc, HDD là số độ lạnh hơn mốc; phía còn lại bằng 0. Nhiệt độ 10; 18,33; 25; 30 °C cho CDD = 0; 0; 6,67; 11,67 và
HDD = 8,33; 0; 0; 0. Hai biến đều **tăng** khi đi xa mốc, nên hồi quy tải = $a + b \cdot \text{CDD} + c \cdot \text{HDD}$ vẽ được hình chữ V:
phía nóng dốc $b$, phía lạnh dốc $c$. Không cần chia dữ liệu làm hai nhóm; cả hai biến vào cùng một mô hình.

Tải điện ERCOT 2024: $R^2$ của hồi quy theo nhiệt độ là 0,379; theo CDD + HDD là 0,812, gấp đôi. Mốc 65 °F là quy ước; mốc tốt nhất trên
dữ liệu này là 19,5 °C, rất gần.

## 107. Mutual information: biết x có giúp đoán y?
<!-- ma: mi -->

*Tiếng Anh: mutual information (MI) · nat · nonlinear dependence*

Pearson hỏi "có đường thẳng không". Mutual information hỏi rộng hơn: "biết $x$ có giúp đoán $y$ không, theo **bất kỳ** cách nào".

Ví dụ: ba loại ngày, mỗi loại 1/3 số ngày; ngày lạnh tải cao, ngày vừa tải thấp, ngày nóng tải cao. Mã hoá thành số thì Pearson = 0, nhưng
biết loại ngày là biết chắc tải. MI so tỷ lệ thật của mỗi ô với tỷ lệ "nếu độc lập":

| Ô (loại ngày, tải) | Tỷ lệ thật | Nếu độc lập | Góp vào MI |
|---|---|---|---|
| lạnh, cao | 1/3 | 1/3 × 2/3 = 2/9 | 1/3 × ln 1,5 ≈ 0,135 |
| vừa, thấp | 1/3 | 1/3 × 1/3 = 1/9 | 1/3 × ln 3 ≈ 0,366 |
| nóng, cao | 1/3 | 1/3 × 2/3 = 2/9 | 1/3 × ln 1,5 ≈ 0,135 |

Cộng lại: MI ≈ 0,637 nat. Công thức chung:

$$
I(X;Y) = \sum_{x,y} p(x,y)\,\ln\frac{p(x,y)}{p(x)\,p(y)}
$$

Nếu độc lập thì mọi tỷ số bằng 1, $\ln 1 = 0$, MI = 0. Với dữ liệu liên tục, scikit-learn ước lượng MI bằng cách đếm láng giềng gần
(`mutual_info_regression`, nhớ đặt `random_state`). Nhiệt độ × tải ERCOT: MI = 0,862 nat. MI chỉ nói "có phụ thuộc", không nói hình dạng
hay chiều của quan hệ; muốn biết hình dạng vẫn phải vẽ scatter.

## 108. Hoán vị theo khối: MI có lớn thật không?
<!-- ma: hoan-vi-khoi -->

*Tiếng Anh: block permutation test · autocorrelation · null distribution*

MI = 0,862 nat là lớn hay nhỏ? Cách kiểm giống kiểm định hoán vị ở buổi 2: xáo trộn $y$ nhiều lần để phá quan hệ, tính MI mỗi lần, rồi
xem MI thật có vượt xa đám MI của dữ liệu xáo không. p-value = (k + 1) / (B + 1), với B là số lần xáo, k là số lần MI xáo lớn bằng hoặc hơn
MI thật.

Với chuỗi thời gian có một chỗ cần cẩn thận. Hai chuỗi trơn độc lập vẫn hay có những quãng dài tình cờ cùng cao hoặc cùng thấp, nên MI
của chúng không nhỏ. Xáo **từng điểm** thì phá luôn độ trơn đó: dữ liệu xáo lộn xộn, MI rất nhỏ, và dữ liệu thật trông "đặc biệt" dù
không có quan hệ. Phải xáo **cả khối** liền nhau, để trong mỗi khối chuỗi vẫn trơn như thật.

Hai chuỗi AR độc lập, rất trơn, 2.000 điểm: xáo từng điểm cho p = 0,005, kết luận sai là có quan hệ; xáo theo khối 200 điểm cho p = 0,055,
không bác bỏ. Nhiệt độ × tải ERCOT, xáo theo khối một tuần: MI thật 0,862 vượt xa ngưỡng 95% của dữ liệu xáo (0,124), nên quan hệ có thật.

## 109. Ai đi trước? Prewhiten rồi mới đọc CCF
<!-- ma: ccf -->

*Tiếng Anh: cross-correlation function (CCF) · prewhitening · lead / lag*

**Tương quan chéo** r_k = corr(x_t, y_t+k) cho biết x đi trước y bao nhiêu bước. Nhưng CCF thô mang cả nhịp riêng của từng chuỗi.
Giữa CDD (độ nóng) và tải điện, CCF thô là 0,848 ở trễ 0 và vẫn 0,828 ở trễ 24: đó chỉ là nhịp ngày của chính CDD.

**Prewhitening** dựng mô hình AR cho x (ở đây AR(48)), lọc x bằng nó, rồi lọc y bằng đúng bộ lọc đó. Sau lọc, CCF còn 0,205 ở trễ 0 và 0,061 ở trễ 24, và đỉnh chỉ còn
ở trễ 0, tắt dần sau vài giờ. Kết luận: tải phản ứng với trời nóng gần như ngay trong giờ. Quy ước hướng của `ccf` khác nhau giữa các
thư viện, nên thử trên chuỗi giả trước khi tin.

## 110. Prewhitening: lọc nhịp riêng rồi mới đo
<!-- ma: prewhitening -->

*Tiếng Anh: prewhitening · AR filter · cross-correlation*

Tương quan chéo thô giữa CDD và tải điện cao ở mọi trễ và lặp theo nhịp 24 giờ, vì cả hai chuỗi đều có nhịp ngày riêng. Muốn thấy
ai đi trước ai thì phải bỏ nhịp riêng đó trước:

1. Dựng mô hình AR cho x (ở đây AR(48)): phần của x tự đoán được từ quá khứ của nó.
2. Lọc x: trừ phần tự đoán được, còn lại phần "bất ngờ".
3. Lọc y bằng đúng bộ lọc của x, không dựng mô hình riêng cho y.
4. Tính tương quan chéo trên hai chuỗi đã lọc.

Sau lọc, tương quan chỉ còn đỉnh ở trễ 0 (0,205) và gần như tắt ở trễ 24 (0,061): tải phản ứng với trời nóng gần như ngay trong giờ.

## 111. Code: tương quan chéo sau prewhitening
<!-- ma: code-b08-prewhiten -->

Lọc bỏ độ trơn của x trước, rồi mới đọc độ trễ mà x báo trước y.

```python
import numpy as np
from statsmodels.tsa.ar_model import AutoReg

def ccf_tu_viet(x, y, so_tre):                    # corr(x_t, y_(t+k))
    x, y = (x - x.mean()) / x.std(), (y - y.mean()) / y.std()
    return np.array([np.sum(x[:x.size - k] * y[k:]) / x.size
                     for k in range(so_tre + 1)])
def loc_prewhiten(x, y, bac=48):
    phi = AutoReg(x, lags=bac).fit().params[1:]   # hệ số AR(48) của x
    def loc(v):
        return np.array([v[i] - phi[::-1] @ v[i - bac:i]
                         for i in range(bac, v.size)])
    return loc(x), loc(y)                         # lọc CẢ HAI, cùng phi
cdd, taiv = df["cdd"].to_numpy(), df["tai"].to_numpy()
tho = ccf_tu_viet(cdd, taiv, 48)                  # thô: nhoè
sach = ccf_tu_viet(*loc_prewhiten(cdd, taiv), 48) # sau lọc: sắc
```

*Rút gọn từ buoi-08/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `AutoReg(x, lags).fit()` (statsmodels): Khớp mô hình tự hồi quy: đoán x từ các giá trị trước của nó.
- `ccf_tu_viet` (tự viết): Tương quan chéo corr(x_t, y_(t+k)); k dương là x đi trước y.
- `loc_prewhiten` (tự viết): Bỏ phần x tự đoán được, lọc y y hệt, trả hai chuỗi đã lọc.

**Từng bước:**

- Dòng 4–6: Chuẩn hoá rồi nhân x lúc t với y lúc t + k.
- Dòng 8: Khớp AR(48) cho x để biết phần tự đoán được.
- Dòng 9–12: Lọc cả x lẫn y bằng đúng bộ hệ số đó.
- Dòng 14–15: So tương quan chéo thô và sau lọc.

**Kết quả:** Thô: trễ 24 (0,828) cao gần bằng trễ 0, là nhịp ngày của CDD. Sau lọc chỉ còn đỉnh ở trễ 0 (0,205), tắt sau vài giờ.

## 112. Một hệ số cho cả năm che mất các mùa
<!-- ma: truot -->

*Tiếng Anh: rolling correlation · regime*

Một hệ số tương quan cho cả năm có thể là trung bình của các chế độ ngược nhau. **Tương quan trượt** tính r trên từng cửa sổ thời
gian. Với nhiệt độ và tải điện:

- Cửa sổ 90 ngày tới 31/3/2024: −0,801 (mùa đông, lạnh thì sưởi).
- Cửa sổ tới 14/10/2024: +0,968 (mùa hè, nóng thì điều hoà).
- Cả năm: 0,616, không đúng với mùa nào.

Quan hệ đổi dấu theo mùa thì tách thành từng chế độ, hoặc dùng CDD/HDD. Lưu ý kỹ thuật: `rolling("90D")` mặc định chỉ cần 1 điểm,
nên vài giá trị đầu là ±1 giả. Đặt `min_periods` rõ ràng.

## 113. Code: tương quan trượt 30 và 90 ngày
<!-- ma: code-b08-tuong-quan-truot -->

Thấy quan hệ nhiệt độ và tải đổi dấu theo mùa, thay vì tin một con số cả năm.

```python
import numpy as np
import pandas as pd

# ví dụ tay: 3 ngày đông r = −1, 3 ngày hè r = +1; gộp lại thì sao?
r_gop = np.corrcoef([5, 10, 15, 25, 30, 35], [30, 20, 10, 20, 30, 40])

ngay = df.resample("D").mean()                    # giờ gộp thành ngày
r90 = ngay["nhiet"].rolling(90, min_periods=90).corr(ngay["tai"])
r30 = ngay["nhiet"].rolling(30, min_periods=30).corr(ngay["tai"])
r_ca_nam = df["nhiet"].corr(df["tai"])            # một số cho cả năm
print(r90["2024-03-31"], r90["2024-10-14"], r30.min())
```

*Rút gọn từ buoi-08/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `resample("D").mean()` (pandas): Gom dữ liệu theo từng ngày, lấy trung bình mỗi ngày.
- `rolling(w, min_periods=w).corr(b)` (pandas): Tương quan trên từng cửa sổ w ngày; thiếu điểm thì để trống.
- `np.corrcoef(a, b)` (numpy): Ma trận tương quan Pearson của hai dãy số.

**Từng bước:**

- Dòng 5: Hai chế độ ngược dấu gộp lại ra số lưng chừng.
- Dòng 7: Đổi dữ liệu giờ thành trung bình ngày.
- Dòng 8–9: r trên cửa sổ trượt, đủ điểm mới tính.
- Dòng 10: Con số cả năm để so.

**Kết quả:** Gộp sáu ngày ra r = 0,48. Cửa sổ 90 ngày: −0,801 (31/3), +0,968 (14/10); 30 ngày xuống tới −0,971. Cả năm 0,616.

## 114. Granger: “giúp dự báo”, không phải “gây ra”
<!-- ma: granger -->

*Tiếng Anh: Granger causality test · confounder*

**Kiểm định Granger** so sai số dự báo Y khi có và khi không có quá khứ của X. Có ý nghĩa nghĩa là "quá khứ X giúp dự báo Y", không
phải "X gây ra Y". Ví dụ trong hình: Granger có ý nghĩa ở **cả hai chiều** giữa tải điện và nhiệt độ. "Tải điện gây ra nhiệt độ" là
vô lý. Cả hai cùng bị nhịp ngày điều khiển (biến gây nhiễu).

Ba điều kiện khi dùng:

- Chạy cả hai chiều.
- Chuỗi phải dừng (sai phân trước).
- Hỏi thêm: lúc ra dự báo có biết giá trị tương lai của X không?

## 115. Code: Granger chạy cả hai chiều
<!-- ma: code-b08-granger -->

Chạy Granger hai chiều để thấy dấu hiệu của biến gây nhiễu, thay vì đọc thành nhân quả.

```python
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

def granger_p(nguyen_nhan, ket_qua, so_tre=4):
    # statsmodels hỏi: CỘT 2 có giúp dự báo CỘT 1 không
    kq = grangercausalitytests(np.column_stack([ket_qua, nguyen_nhan]),
                               maxlag=so_tre)
    return min(kq[k][0]["ssr_ftest"][1] for k in kq)   # p nhỏ nhất

cdd, taiv = df["cdd"].to_numpy(), df["tai"].to_numpy()
p_xuoi = granger_p(cdd, taiv)                     # CDD giúp dự báo tải?
p_nguoc = granger_p(taiv, cdd)                    # tải giúp dự báo CDD?

ho = df[["tai", "nhiet"]].groupby(df.index.hour).mean()   # theo giờ
ho = (ho - ho.mean()) / ho.std()                  # cùng một nhịp 24 giờ
```

*Rút gọn từ buoi-08/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `grangercausalitytests(data, maxlag)` (statsmodels): Kiểm quá khứ cột 2 có giúp dự báo cột 1 không, ở mỗi độ trễ.
- `groupby(df.index.hour).mean()` (pandas): Trung bình theo giờ trong ngày: ra hình dạng một ngày điển hình.
- `np.column_stack` (numpy): Ghép các dãy thành các cột của một bảng.

**Từng bước:**

- Dòng 5–6: Xếp cột đúng thứ tự thư viện đòi.
- Dòng 7: Lấy p nhỏ nhất qua các độ trễ 1 tới 4.
- Dòng 10–11: Hỏi cả hai chiều, không chỉ chiều mong muốn.
- Dòng 13–14: Tìm biến thứ ba: nhịp giờ trong ngày.

**Kết quả:** Cả hai chiều p gần 0, kể cả "tải giúp dự báo nhiệt độ": vô lý, vì cả hai cùng chạy theo nhịp ngày.

## 116. Đo quan hệ hai chuỗi: tám câu hỏi của buổi 8
<!-- ma: quy-trinh-tuong-quan -->

1. **Trông ra sao?** Vẽ scatter trước: thẳng, cong, chữ U, hay có điểm lạ.
2. **Thẳng hàng hay chỉ cùng tăng?** Pearson đo mức thẳng hàng; Spearman đo cùng tăng theo thứ hạng.
3. **Hai chuỗi cùng trôi theo thời gian?** Đo lại trên sai phân, xem Durbin–Watson. CPI và dân số Mỹ: r từ 0,97 còn −0,21.
4. **Cong, đổi dấu?** Tách CDD / HDD, hoặc đo mutual information; kiểm MI bằng hoán vị theo khối.
5. **Ai đi trước, bao lâu?** Prewhiten cả hai chuỗi bằng cùng một bộ lọc, rồi đọc tương quan chéo.
6. **Giữ nguyên cả năm?** Tương quan trượt 30, 90 ngày; đổi dấu theo mùa thì tách riêng từng mùa.
7. **Quá khứ x giúp đoán y?** Granger, chạy cả hai chiều. p nhỏ là "giúp dự báo", chưa phải "gây ra".
8. **Lúc dự báo có x chưa?** Chỉ dùng bản có trong tay lúc đó, như nhiệt độ dự báo (buổi 13).

## 117. Đặc trưng: tóm cả chuỗi thành vài con số
<!-- ma: dac-trung -->

*Tiếng Anh: time series features · scale-free · feature table*

48.000 chuỗi thì không ai xem từng hình. Mỗi **đặc trưng** là một con số tóm một tính chất của cả chuỗi: CV, $r_1$, $F_S$, spectral entropy… Mỗi chuỗi thành một hàng số,
cả tập thành một bảng.

Đặc trưng tốt **không đổi theo đơn vị**: nhân chuỗi với một số thì nó giữ nguyên, vì nó đo hình dạng chứ không đo độ lớn. Ví dụ chuỗi
$a$ = (2, 4, 6, 4, 2, 4, 6, 4) và 1.000 × $a$:

- Trung bình 4 và 4.000: đổi theo đơn vị, chỉ nói chuỗi to hay nhỏ.
- CV: 1,51 / 4 = 0,378 và 1.512 / 4.000 = 0,378, không đổi.
- $r_1$ bằng 0 ở cả hai, vì tử số và mẫu số cùng nhân 1.000².

$$
\mathrm{CV}(1000\,a) = \frac{1000\,s}{1000\,\bar a} = \mathrm{CV}(a)
$$

Trong 20 đặc trưng của buổi, chỉ trung bình và độ lệch chuẩn đổi theo đơn vị; chúng chỉ để tham chiếu. Nhóm STL (độ dốc, độ cong xu
hướng, spike) cũng sẽ đổi nếu tính trên chuỗi gốc, nên code chạy STL trên chuỗi đã **chuẩn hoá z-score**: trừ trung bình rồi chia độ lệch
chuẩn. Hình ô trái là hai chuỗi cùng hình, một chuỗi lớn gấp 100 lần; ô phải sau z-score hai đường trùng khít, chỉ còn hình dạng.

Yêu cầu thứ hai: tính trên **cùng độ dài**, nên chuỗi M4 dài ngắn khác nhau được cắt về cùng độ dài trước. Đặc trưng còn dò được chuỗi
hỏng: trong 4.000 chuỗi mẫu có 1 chuỗi hằng và 50 chuỗi bậc thang.

## 118. Code: mỗi chuỗi thành một hàng số
<!-- ma: code-b09-dac-trung -->

Tóm mỗi chuỗi thành các đặc trưng không đổi theo đơn vị, để so hàng nghìn chuỗi.

```python
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL

def dac_trung(y, m=12):                           # 6 trong 20 đặc trưng
    z = (y - y.mean()) / np.std(y)                # STL trên chuỗi z-score
    idx = pd.period_range("2000-01", periods=y.size, freq="M").to_timestamp()
    kq = STL(pd.Series(z, index=idx), period=m).fit()
    r, s = kq.resid.to_numpy(), kq.seasonal.to_numpy()
    return {"trung_binh": y.mean(),
            "he_so_bien_thien": np.std(y, ddof=1) / y.mean(),
            "he_so_lech": stats.skew(y), "do_nhon": stats.kurtosis(y),
            "do_manh_mua_vu": max(0.0, 1 - np.var(r) / np.var(s + r)),
            "ty_le_0": np.mean(y == 0)}
bang = pd.DataFrame({t: dac_trung(v[:-18]) for t, v in chuoi.items()}).T
```

*Rút gọn từ buoi-09/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `STL(series, period).fit()` (statsmodels): Tách chuỗi thành xu hướng + mùa vụ + phần dư.
- `stats.skew, stats.kurtosis` (scipy): Hệ số lệch và độ nhọn: đo đuôi và giá trị cực đoan.
- `pd.DataFrame(dict).T` (pandas): Ghép từ điển các chuỗi thành bảng, mỗi chuỗi một hàng.

**Từng bước:**

- Dòng 7: z-score để độ mạnh không tính bằng USD.
- Dòng 8–10: Tách xu hướng, mùa vụ, phần dư bằng STL.
- Dòng 11–15: Mỗi đặc trưng một con số của cả chuỗi.
- Dòng 16: Chỉ tính trên phần học, bỏ 18 tháng chấm.

**Kết quả:** Nhân chuỗi với 1.000: chỉ trung_binh và do_lech_chuan đổi, 18 đặc trưng giữ nguyên. Bảng còn cho thấy 1 chuỗi hằng và 50 chuỗi bậc thang.

## 119. Tần số và phổ: chuỗi rung ở nhịp nào
<!-- ma: pho -->

*Tiếng Anh: frequency · spectrum · periodogram · energy*

Thay vì nhìn chuỗi theo thời gian, có thể nhìn nó theo **nhịp lặp**. **Tần số** là số vòng lặp mỗi bước, bằng 1 chia chu kỳ: lặp mỗi
12 tháng thì tần số 1/12 ≈ 0,083 vòng mỗi tháng. Trong hình, sóng trên lặp chậm (tần số thấp), sóng dưới lặp nhanh nhất mà dữ liệu
tháng thể hiện được (tần số cao).

**Phổ** (periodogram) là bảng cho biết mỗi tần số góp bao nhiêu phần dao động, gọi là năng lượng, vào chuỗi:

- **Tần số thấp**: dao động chậm như xu hướng, mùa năm.
- **Tần số giữa**: nhịp ngày, nhịp tuần.
- **Tần số cao**: dao động rất nhanh, thường là nhiễu.

Phổ điện thiết bị ở buổi 12 có đỉnh ở một vòng mỗi ngày, và 17,8% năng lượng nằm ở dao động nhanh hơn một giờ; nhiệt độ phòng gần như
không có. Spectral entropy (buổi 9) đo năng lượng dồn vào ít tần số hay trải đều.

## 120. Spectral entropy: năng lượng dồn hay trải đều
<!-- ma: entropy -->

*Tiếng Anh: spectral entropy · normalized power spectrum*

Trước khi dự báo, ta muốn biết chuỗi có nhịp đều để khai thác hay gần như ngẫu nhiên. Mọi chuỗi viết được thành tổng nhiều sóng đều,
mỗi sóng một tần số; **phổ** cho biết mỗi sóng góp bao nhiêu phần dao động ("năng lượng"). Đổi phổ thành các phần $p_i$ cộng lại bằng 1,
như chia một chiếc bánh. **Spectral entropy** đo bánh chia đều tới đâu: 0 là dồn vào một đĩa, 1 là chia đều.

$$
H = \frac{-\sum_{i=1}^{N} p_i \ln p_i}{\ln N}, \qquad p_i = \frac{P_i}{\sum_j P_j}
$$

$P_i$ là năng lượng ở tần số $i$ (bỏ tần số 0, vốn chỉ là mức trung bình), $N$ là số tần số. Chia $\ln N$ để kết quả luôn từ 0 tới 1.
Ví dụ phổ 4 tần số ($\ln 4 \approx 1{,}386$):

| Chuỗi | Phần năng lượng | H |
|---|---|---|
| sóng đều | 0; 1; 0; 0 | 0 |
| hai nhịp | 0,5; 0,5; 0; 0 | 0,693 / 1,386 = 0,5 |
| nhiễu | 0,25 mỗi tần số | 1 |

Hình: hàng trên là hai chuỗi 120 tháng, hàng dưới là phần năng lượng theo tần số. Chuỗi mùa vụ 12 tháng dồn gần hết vào tần số lặp mỗi
12 tháng, entropy 0,33; nhiễu thuần trải đều, entropy 0,94. Trên 4.000 chuỗi M4, trung vị là 0,462, một phần năm số chuỗi từ 0,666
trở lên.

Dùng để xếp hạng độ khó hàng nghìn chuỗi mà chưa chạy mô hình nào. Lưu ý: chuỗi quá ngắn cho con số chập chờn; chuỗi có xu hướng mạnh dồn
năng lượng vào tần số thấp nên entropy thấp mà vẫn có thể khó. Nixtla `tsfeatures` tính phổ theo cách khác, nên không so thẳng hai con
số.

## 121. Code: spectral entropy từ phổ Welch
<!-- ma: code-b09-entropy -->

Một con số từ 0 tới 1 nói chuỗi có nhịp rõ hay giống nhiễu, không cần mô hình.

```python
import numpy as np
from scipy import signal

def entropy_pho(y):
    _, P = signal.welch(y - y.mean(), fs=1.0, nperseg=min(256, y.size))
    P = P[1:]                                     # bỏ tần số 0 (mức TB)
    p = P / P.sum()                               # phần năng lượng, tổng 1
    return float(-np.sum(p * np.log(p + 1e-300)) / np.log(p.size))

rng = np.random.default_rng(0)
t = np.arange(120)
mua_vu = np.sin(2 * np.pi * t / 12) + 0.2 * rng.normal(size=120)
nhieu = rng.normal(size=120)
print(entropy_pho(mua_vu), entropy_pho(nhieu))
e = bang["entropy_pho"]                           # 4.000 chuỗi M4
print(e.median(), e.quantile(0.8))
```

*Rút gọn từ buoi-09/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `signal.welch(y, fs, nperseg)` (scipy): Ước lượng phổ bằng trung bình phổ của nhiều đoạn chồng nhau.
- `entropy_pho` (tự viết): Năng lượng trải đều tới đâu: 0 là một nhịp, 1 là nhiễu.
- `quantile(0.8)` (pandas): Giá trị mà 80% số chuỗi nằm dưới.

**Từng bước:**

- Dòng 5: Phổ: mỗi tần số góp bao nhiêu năng lượng.
- Dòng 7: Chia thành các phần cộng lại bằng 1.
- Dòng 8: Entropy chia ln N để luôn nằm trong 0 tới 1.
- Dòng 11–13: So chuỗi mùa vụ 12 tháng với nhiễu thuần.
- Dòng 14–15: Xem phân bố entropy trên 4.000 chuỗi.

**Kết quả:** Chuỗi mùa vụ entropy 0,33, nhiễu thuần 0,94. Trên M4 trung vị 0,462; một phần năm số chuỗi từ 0,666 trở lên.

## 122. Đo độ khó bằng sMAPE, không bằng MASE
<!-- ma: do-kho -->

*Tiếng Anh: forecastability · sMAPE · MASE · scale-free error*

Muốn biết đặc trưng nào báo trước độ khó thì phải đo độ khó bằng một thước đo không tự triệt tiêu nó. MASE của seasonal naive chia
cho sai số seasonal naive của chính chuỗi đó: chuỗi khó thì mẫu số cũng lớn, nên MASE nằm ngang quanh 1 dù chuỗi dễ hay khó. sMAPE chia cho mức nên giữ được
độ khó. Tương quan với entropy:

| Thước đo | Pearson |
|---|---|
| sMAPE | +0,245 |
| MASE (chia seasonal naive) | −0,048 |
| MASE (chia naive một bước) | −0,381 |

Cùng dữ liệu, cùng dự báo, chỉ đổi mẫu số mà kết luận đi từ dương qua 0 tới âm. MASE dùng để so mô hình trên cùng một chuỗi. sMAPE
dùng để xếp độ khó giữa các chuỗi dương, không dùng để chấm mô hình.

## 123. Code: đo độ khó bằng sMAPE và MASE
<!-- ma: code-b09-smape-mase -->

Thấy chỉ đổi mẫu số của thước đo là kết luận về entropy đổi hẳn.

```python
import numpy as np
import pandas as pd
from scipy import stats

def smape(y, f):                                  # chia cho MỨC
    mau = np.abs(y) + np.abs(f)
    return np.mean(np.where(mau == 0, 0.0, 200 * np.abs(y - f) / mau))
def mase(y, f, hoc, m=12):                        # chia cho sai số snaive
    thang = np.mean(np.abs(hoc[m:] - hoc[:-m]))   # MAE snaive phần học
    return np.mean(np.abs(y - f)) / thang
kho = {}
for ten, v in chuoi.items():
    hoc, kiem = v[:-18], v[-18:]                  # 18 tháng cuối để chấm
    f = np.resize(hoc[-12:], 18)                  # seasonal naive
    kho[ten] = {"smape": smape(kiem, f), "mase": mase(kiem, f, hoc)}
r = stats.pearsonr(bang["entropy_pho"], pd.DataFrame(kho).T["smape"])[0]
```

*Rút gọn từ buoi-09/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `np.resize(a, n)` (numpy): Lặp lại mảng a cho đủ n phần tử: 12 tháng cuối thành 18 tháng.
- `np.where(dk, a, b)` (numpy): Chọn a nơi điều kiện đúng, b nơi sai; tránh chia cho 0.
- `stats.pearsonr(x, y)` (scipy): Hệ số tương quan Pearson của hai cột.

**Từng bước:**

- Dòng 5–7: sMAPE chia sai số cho mức của chuỗi.
- Dòng 8–10: MASE chia cho sai số seasonal naive lúc học.
- Dòng 13–14: Dự báo 18 tháng bằng lặp lại năm cuối.
- Dòng 16: Tương quan entropy với độ khó thật.

**Kết quả:** Ví dụ tay: MASE nói B dễ hơn A (0,92 so với 1,00), sMAPE nói B khó hơn (76,2% so với 6,7%). Với entropy: sMAPE +0,245, MASE −0,048.

## 124. Bản đồ 4.000 chuỗi: vùng nào khó
<!-- ma: ban-do-pca -->

*Tiếng Anh: PCA · principal component (PC1, PC2) · feature space*

Bỏ hai đặc trưng quy mô và ba cột có NaN, còn 15 đặc trưng không phụ thuộc đơn vị cho 4.000 chuỗi M4 tháng, chuẩn hoá từng cột, rồi dùng **PCA** (phép chiếu giữ nhiều khác
biệt nhất) để vẽ cả tập trên hai trục. Mỗi chuỗi là một chấm:

- **Trục ngang PC1** (giữ 41% khác biệt) là độ lởm chởm: phải là chuỗi lởm chởm, trái là chuỗi trơn.
- **Trục dọc PC2** (thêm 15%) là mức độ xu hướng và mùa vụ.

Vùng entropy cao bên phải cũng là vùng sMAPE cao: chuỗi lởm chởm, mùa vụ yếu là chuỗi khó. Quy tắc thực hành: entropy ≥ 0,666 và
F_S < 0,4 thì chỉ cần baseline. Mấy chấm lẻ ở góc là chuỗi lạ, cần xem tận mắt.

## 125. Code: bản đồ PCA và nhóm dùng baseline
<!-- ma: code-b09-pca -->

Nén 15 đặc trưng về hai trục để thấy cả tập, rồi tách chuỗi chỉ cần baseline.

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

cot = [c for c in bang.columns if bang[c].notna().all()
       and c not in ("trung_binh", "do_lech_chuan")    # bỏ cột quy mô
       and not c.startswith(("smape", "mase"))]        # bỏ cột sai số
X = StandardScaler().fit_transform(bang[cot])     # chuẩn hoá từng cột
pca = PCA(n_components=2, random_state=0)
toa_do = pca.fit_transform(X)                     # mỗi chuỗi một chấm
print(pca.explained_variance_ratio_)              # phần khác biệt giữ lại

kho = (bang["entropy_pho"] >= 0.666) & (bang["do_manh_mua_vu"] < 0.4)
nhom = np.where(kho, "dùng baseline", "đáng đầu tư mô hình")
print(bang.groupby(nhom)["smape_snaive"].agg(["size", "median"]))
```

*Rút gọn từ buoi-09/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `StandardScaler().fit_transform` (sklearn): Trừ trung bình, chia độ lệch chuẩn cho từng cột.
- `PCA(n_components=2)` (sklearn): Tìm hai hướng mà các chuỗi khác nhau nhiều nhất.
- `explained_variance_ratio_` (sklearn): Mỗi trục giữ được bao nhiêu phần trăm khác biệt.

**Từng bước:**

- Dòng 5–7: Chỉ giữ đặc trưng đủ số, không lẫn sai số.
- Dòng 8: Chuẩn hoá để cột số to không lấn át.
- Dòng 9–11: Nén về hai trục PC1, PC2.
- Dòng 13–14: Entropy cao và mùa vụ yếu: dùng baseline.
- Dòng 15: Kiểm lại bằng sMAPE thật của từng nhóm.

**Kết quả:** PC1 giữ 41%, PC2 15%. 137 chuỗi dùng baseline có sMAPE trung vị 18,11%, gấp ba nhóm 3.863 chuỗi còn lại (6,05%).

## 126. DTW: gom chuỗi theo hình dạng
<!-- ma: dtw -->

*Tiếng Anh: dynamic time warping (DTW) · z-score normalization · Ward clustering*

**DTW** đo hai chuỗi giống hình dạng tới đâu, cho phép lệch thời gian đôi chút, ví dụ đỉnh Tết năm sớm năm muộn. DTW so giá trị,
nên phải chuẩn hoá z-score từng chuỗi trước. Không chuẩn hoá thì 4 cụm chỉ khác nhau về độ lớn: mức trung vị tăng đều 1.585 → 3.310 →
6.835 → 9.832, việc mà một phép sắp xếp cũng làm được. Chuẩn hoá thì cụm theo hình dạng: giảm, tăng đều, bướu giữa, dao động quanh
mức. Kiểm nhanh: nếu mức trung vị các cụm tăng đều thì bạn đang phân cụm theo độ lớn.

## 127. Code: phân cụm DTW sau z-score
<!-- ma: code-b09-dtw -->

Gom chuỗi theo hình dạng, và thấy vì sao phải chuẩn hoá từng chuỗi trước DTW.

```python
import numpy as np
import pandas as pd
from dtaidistance import dtw
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform

def z(v):                                         # bỏ mức, giữ hình dạng
    return (v - v.mean()) / v.std()
def phan_cum(mau, chuan_hoa, so_cum=4, cua_so=10):
    day = [z(v) if chuan_hoa else v for v in mau.values()]
    D = dtw.distance_matrix_fast(day, window=cua_so)   # lệch tối đa 10
    D = np.where(np.isinf(D), 0, D)
    D = D + D.T                                   # lấp đủ hai nửa ma trận
    Z = linkage(squareform(D, checks=False), method="ward")
    nhan = fcluster(Z, so_cum, criterion="maxclust")
    return pd.Series(nhan, index=list(mau))
```

*Rút gọn từ buoi-09/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `linkage(d, method="ward")` (scipy): Gộp dần hai nhóm gần nhau nhất, ghi lại từng bước gộp.
- `fcluster(Z, k, "maxclust")` (scipy): Cắt cây gộp để còn đúng k cụm, trả nhãn cụm từng chuỗi.
- `squareform(D)` (scipy): Đổi ma trận khoảng cách vuông thành dạng gọn mà linkage cần.

**Từng bước:**

- Dòng 7–8: z-score: bỏ độ lớn, chỉ giữ hình dạng.
- Dòng 10: Chọn có chuẩn hoá hay không để so.
- Dòng 11: Khoảng cách DTW giữa mọi cặp chuỗi.
- Dòng 12–13: Sửa ma trận cho đủ và đối xứng.
- Dòng 14–16: Gộp dần theo Ward, cắt ra 4 cụm.

**Kết quả:** Không chuẩn hoá: mức trung vị các cụm tăng đều từ 1.585 tới 9.832, chỉ xếp theo độ lớn. Chuẩn hoá: bốn cụm là bốn hình dạng.

## 128. ABC hỏi quan trọng, XYZ hỏi dao động
<!-- ma: abc-xyz -->

*Tiếng Anh: ABC–XYZ classification · coefficient of variation (CV)*

**ABC–XYZ** là cách phân loại mã hàng quen thuộc trong bán lẻ:

- **ABC** xếp theo doanh thu. Trên Online Retail II, nhóm A (một phần năm số mã) mang 74,7% doanh thu. Đó là nơi sai thì đắt nhất,
  đáng mô hình tốt nhất.
- **XYZ** xếp theo CV (độ lệch chuẩn chia trung bình), tức chỉ đo dao động, không đo độ khó.

Chuỗi mùa vụ đều như 10, 30, 10, 30 có CV cao mà rất dễ đoán. Đo độ khó bằng sai số thật của một baseline. Cách nhớ: ABC hỏi "cái
nào quan trọng?", CV hỏi "cái nào dao động?", sai số baseline mới hỏi "cái nào khó?".

## 129. Code: bảng ABC–XYZ cho mã hàng
<!-- ma: code-b09-abc-xyz -->

Xếp mã hàng theo doanh thu và theo CV, rồi kiểm CV có đo được độ khó không.

```python
import numpy as np
from scipy import stats

# ban_le: doanh thu theo (mã hàng, tháng) của Online Retail II
g = ban_le.groupby("StockCode")["doanh_thu"]
h = g.agg(["sum", "mean", "std", "count"])
h = h[h["count"] >= 12].sort_values("sum", ascending=False)  # ≥ 12 tháng
h["cv"] = h["std"] / h["mean"]                    # hệ số biến thiên
ty_le = np.arange(1, len(h) + 1) / len(h)         # vị trí theo doanh thu
h["abc"] = np.where(ty_le <= 0.2, "A", np.where(ty_le <= 0.5, "B", "C"))
h["xyz"] = np.where(h["cv"] < 0.5, "X", np.where(h["cv"] <= 1, "Y", "Z"))
o = h.groupby(["abc", "xyz"]).size().unstack(fill_value=0)   # bảng 3 × 3

cv = bang["he_so_bien_thien"]                     # 4.000 chuỗi M4
r = stats.spearmanr(cv, bang["smape_snaive"])[0]
```

*Rút gọn từ buoi-09/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `groupby().agg([...])` (pandas): Tính nhiều con số tổng hợp cho từng mã hàng một lúc.
- `unstack(fill_value=0)` (pandas): Xoay bảng dài thành bảng chéo, ô trống điền 0.
- `stats.spearmanr` (scipy): Tương quan trên thứ hạng giữa CV và sMAPE.

**Từng bước:**

- Dòng 4–6: Tổng hợp từng mã, giữ mã có đủ 12 tháng.
- Dòng 7: CV: độ lệch chuẩn chia trung bình.
- Dòng 8–9: 20% mã đầu là A, 30% tiếp là B, còn lại C.
- Dòng 10–11: Chia X, Y, Z theo CV rồi đếm từng ô.
- Dòng 13–14: Đối chiếu CV với sai số thật trên M4.

**Kết quả:** 2.773 mã hàng; nhóm A mang 74,7% doanh thu; ô CZ đông gần gấp bốn ô AX. Trên M4, Spearman CV × sMAPE 0,765 nhưng CV xếp sai chuỗi mùa vụ đều.

## 130. Mỗi feature: biết trước bao lâu?
<!-- ma: biet-truoc -->

*Tiếng Anh: feature · calendar feature · lag feature*

**Feature** là cột đầu vào của mô hình. Quy tắc duy nhất: mỗi feature phải trả lời được "biết trước bao lâu".

- **Lịch** (thứ, giờ, ngày lễ): biết mãi mãi.
- **Kế hoạch** (khuyến mãi đã công bố): biết từ lúc công bố.
- **Quá khứ của chuỗi**: chỉ biết tới thời điểm ra dự báo.

Bộ feature của buổi 13 có 41 cột: 23 là lịch, 18 lấy từ quá khứ. Feature nào không xếp được vào ba nhóm này là nghi rò rỉ.

Bảng "biết trước bao lâu" nộp kèm mô hình, để người xem lại phát hiện rò rỉ mà không cần đọc code.

## 131. Code: feature nào đã có lúc dự báo
<!-- ma: code-b13-biet-truoc -->

Hỏi từng feature "lúc ra dự báo tôi có nó chưa?" rồi xếp vào đúng nhóm.

```python
import pandas as pd

t = pd.Timestamp("2010-06-07")              # tối thứ Hai ra dự báo
muc_tieu = t + pd.Timedelta(days=1)         # thứ Ba, h = 1
thu = muc_tieu.dayofweek                    # lịch: biết trước mãi mãi
tb_da_biet = y[:t].mean()                   # chỉ các ngày tới t
tb_ca_chuoi = y.mean()                      # gồm cả ngày chưa xảy ra

def bang_biet_truoc(cot):                   # xếp theo TÊN cột
    if cot.startswith(("lag_", "tb_", "sd_")):
        return "t-h"                        # quá khứ của chuỗi
    if cot.startswith(("du_bao_", "khuyen_mai")):
        return "kế hoạch"                   # đã công bố
    if cot.endswith("_that"):
        return "KHÔNG BIẾT TRƯỚC"
    return "vô hạn"                         # lịch
```

*Rút gọn từ buoi-13/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `pd.Timestamp, pd.Timedelta` (pandas): Tạo một mốc thời gian rồi cộng thêm một khoảng, ở đây là 1 ngày.
- `y[:t].mean()` (pandas): Cắt chuỗi tới mốc t rồi lấy trung bình, bỏ phần tương lai.
- `bang_biet_truoc` (tự viết): Xếp feature vào nhóm lịch, kế hoạch hay quá khứ theo tên cột.

**Từng bước:**

- Dòng 3–4: Tối thứ Hai dự báo doanh thu thứ Ba.
- Dòng 5: Thứ của ngày mai là lịch, biết từ trước.
- Dòng 6–7: So trung bình tới t với trung bình cả chuỗi.
- Dòng 9–16: Đọc tên cột để xếp feature vào một nhóm.
- Dòng 14–15: Tên đuôi _that là giá trị thật: loại.

**Kết quả:** Trung bình 189 ngày đã biết là 27.701, cả chuỗi là 33.454 vì gồm 550 ngày chưa xảy ra. z_score lọt vào nhóm "vô hạn": tên sai thì bảng sai.

## 132. Dự báo trước h bước: shift h trước, rolling sau
<!-- ma: shift-rolling -->

*Tiếng Anh: lag feature · rolling feature · shift*

**Lag** nhìn về một điểm quá khứ: lag_7 của thứ Hai là giá trị thứ Hai tuần trước. **Rolling** lấy trung bình một vùng gần
đây. Khi dự báo trước h bước thì phải `shift(h)` trước rồi mới `rolling`.

Ví dụ trong bảng, h = 3, chuỗi 10, 20, …, 60:

- **Đúng thứ tự**: shift(3) rồi rolling(2) cho ngày 6 giá trị 25, là trung bình ngày 2–3, đã biết từ ngày 3.
- **Quên shift**: rolling(2) cho ngày 6 giá trị 55, là trung bình ngày 5–6. Lúc ra dự báo (ngày 3) chưa có hai ngày đó:
  đây là rò rỉ.

## 133. Code: shift trước, rolling sau
<!-- ma: code-b13-shift -->

Thấy bằng số vì sao phải shift trước rolling, rồi gói thành hàm tạo feature.

```python
import pandas as pd
v = pd.Series([10, 12, 8, 14, 20, 16], index=range(1, 7), dtype=float)
sai_1 = v.rolling(3, center=True).mean()     # nhìn cả ngày sau
sai_2 = v.rolling(3).mean()                  # chứa chính ngày t
dung = v.shift(1).rolling(3).mean()          # chỉ quá khứ

def feature_tre(y, tam=1, cac_lag=(1, 2, 3, 7, 14, 28),
                cac_cua_so=(7, 28)):
    f = pd.DataFrame(index=y.index)
    tre = y.shift(tam)                       # lùi h bước TRƯỚC
    for lag in cac_lag:
        f[f"lag_{lag}"] = y.shift(max(lag, tam))   # lag nhỏ nhất ≥ h
    for w in cac_cua_so:
        f[f"tb_{w}"] = tre.rolling(w).mean()       # rolling SAU
        f[f"sd_{w}"] = tre.rolling(w).std()
    return f
```

*Rút gọn từ buoi-13/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `shift(k)` (pandas): Dời chuỗi xuống k bước: ngày t nhận giá trị ngày t − k.
- `rolling(w).mean()` (pandas): Trung bình w điểm gần nhất, tính tới chính điểm đó.
- `feature_tre` (tự viết): Tạo các cột lag và rolling theo đúng quy tắc shift trước.

**Từng bước:**

- Dòng 2: Sáu ngày doanh thu, dự báo trước 1 ngày.
- Dòng 3–5: Ba cách tính trung bình 3 ngày; chỉ dòng 5 đúng.
- Dòng 9: Lùi chuỗi tam bước trước khi làm gì khác.
- Dòng 10–11: Lag nhỏ hơn tầm dự báo bị nâng lên bằng tam.
- Dòng 12–14: Mọi rolling tính trên chuỗi đã lùi.

**Kết quả:** Ngày 4: có tâm ra 14, không shift ra 11,33, shift ra 10. Cắt dữ liệu rồi tính lại: bản shift lệch 0, bản có tâm lệch tới 5.113.

## 134. Feature lịch: sin/cos, Fourier, Tết âm lịch
<!-- ma: feature-lich -->

*Tiếng Anh: cyclical encoding (sin/cos) · Fourier terms · moving holiday*

Feature lịch biết trước mãi mãi:

- **Thứ, tháng** mã hoá bằng một cặp sin/cos, để Chủ nhật đứng cạnh thứ Hai và tháng 12 đứng cạnh tháng 1.
- **Mùa vụ dài** (365 ngày) dùng vài cặp **Fourier** thay vì 365 biến giả.
- **Tết âm lịch** xê dịch gần một tháng giữa các năm dương lịch, nên phải tính từ lịch âm, không ghi cứng ngày. Tính ở múi giờ Việt
  Nam (UTC+7); thư viện lịch Trung Quốc dùng UTC+8 có năm lệch một ngày.

Xếp theo "số ngày tới Tết" thì hiệu ứng hiện rõ: lượt xem Wikipedia còn 0,62 lần mức thường vào mùng 1.

Báo phần cải thiện ở đúng vùng feature có tác dụng: feature Tết chỉ giảm sai số 1,9% cả năm nhưng 16,9% quanh Tết; báo trung bình cả năm sẽ loại oan nó.

## 135. Code: sin/cos, Fourier và Tết
<!-- ma: code-b13-lich -->

Mã hoá lịch sao cho Chủ nhật nằm sát thứ Hai và mùa vụ năm chỉ tốn vài cột.

```python
import numpy as np
import pandas as pd
so = np.array([5, 6, 0])                    # thứ Bảy, Chủ nhật, thứ Hai
vong = np.column_stack([np.sin(2 * np.pi * so / 7),
                        np.cos(2 * np.pi * so / 7)])
cn_t2 = np.linalg.norm(vong[1] - vong[2])   # Chủ nhật – thứ Hai

def feature_fourier(moc, chu_ky=365.25, k=3):
    t = (moc - moc[0]).days.to_numpy().astype(float)
    f = pd.DataFrame(index=moc)
    for i in range(1, k + 1):                # sóng lặp i lần mỗi năm
        f[f"fourier_sin_{i}"] = np.sin(2 * np.pi * i * t / chu_ky)
        f[f"fourier_cos_{i}"] = np.cos(2 * np.pi * i * t / chu_ky)
    return f

d = so_ngay_toi_tet(wiki.index)             # Tết tính từ lịch âm UTC+7
```

*Rút gọn từ buoi-13/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `np.sin, np.cos` (numpy): Tính sin, cos cho cả mảng một lần; cả cặp mới định vị đúng.
- `np.linalg.norm` (numpy): Độ dài của một vectơ: khoảng cách giữa hai điểm trên vòng.
- `so_ngay_toi_tet` (tự viết): Số ngày tới mùng 1 Tết gần nhất theo lịch âm; âm là đã qua.

**Từng bước:**

- Dòng 3–5: Đặt ba ngày cuối, đầu tuần lên vòng tròn.
- Dòng 6: Đo khoảng cách Chủ nhật tới thứ Hai.
- Dòng 9: Đổi ngày thành số ngày kể từ đầu chuỗi.
- Dòng 11–13: Mỗi i thêm một cặp sóng, K = 3 cho 6 cột.
- Dòng 16: Đếm số ngày tới mùng 1 Tết gần nhất.

**Kết quả:** Chủ nhật cách thứ Hai 0,868, đúng bằng cách thứ Bảy. Thêm 5 feature Tết: cả năm chỉ tốt hơn 1,9%, quanh Tết tốt hơn 16,9%.

## 136. Số tính trên cả chuỗi mang tương lai vào
<!-- ma: ca-chuoi -->

*Tiếng Anh: full-sample leakage · scaler fit · target encoding*

Rò rỉ không chỉ nằm ở lag hay rolling. Chung một gốc: một con số tính trên **toàn bộ** dữ liệu, kể cả phần tương lai, rồi đưa vào feature
của từng ngày. Ba kiểu hay gặp:

| Kiểu | Cách sửa |
|---|---|
| chuẩn hoá cả chuỗi | fit scaler (trung bình, độ lệch chuẩn) chỉ trên phần học rồi cố định |
| target encoding (thay nhóm bằng trung bình $y$ của nhóm) | chỉ dùng các ngày trước $t$ |
| nội suy hai phía | `ffill`: chỉ dùng số đã có |

Ví dụ sáu ngày doanh thu 10, 12, 8, 14, 20, 16; ngày lẻ là nhóm A, ngày chẵn là nhóm B.

- Trung bình cả sáu ngày là 13,33, đã chứa hai ngày cuối. z của ngày 1 là −0,77: ngày đầu "biết" mình thấp hơn trung bình, tức biết các ngày
  sau cao.
- Trung bình nhóm A trên cả chuỗi là (10 + 8 + 20) / 3 = 12,67: ngày 1 đã "biết" số 20 của ngày 5.
- Ngày 3 thiếu: nội suy điền (12 + 14) / 2 = 13, dùng số của ngày 4; `ffill` điền 12.

Hình mượn từ buổi 10 cho kiểu thứ ba: vạch đứt là mốc cắt, `ffill` chỉ nhìn quá khứ, nội suy tuyến tính nhìn sang số bên phải vạch. Rò rỉ này
chỉ thấy ở mép lỗ; những ngày không thiếu thì hai cách giống hệt.

Chuẩn hoá và target encoding vẫn dùng được nếu tham số chỉ học từ phần học hoặc từ quá khứ của từng dòng. Không bao giờ `fit` trên cả tập rồi
mới chia học và kiểm.

## 137. Kiểm rò rỉ: cắt tương lai và nhiễu mục tiêu
<!-- ma: kiem-ro-ri -->

*Tiếng Anh: leakage test · truncation test · target perturbation*

Không ai đọc hết từng dòng code của 41 feature. Hai bài kiểm chạy bằng máy trên mọi hàm tạo feature.

**Cắt tương lai**: tính feature trên dữ liệu đầy đủ, cắt dữ liệu tại một mốc rồi tính lại, so mọi dòng trước mốc. Feature hợp lệ cho kết quả
y hệt. Ví dụ cắt sau ngày thứ tư: cột trung bình có tâm ở ngày đó đổi từ 14 thành NaN vì thiếu ngày sau, còn cột đã shift giữ nguyên. NaN so
với số phải tính là khác nhau, nếu không sẽ bỏ lọt đúng trường hợp này.

**Nhiễu mục tiêu**: cắt ở đâu thì `lag_1` vẫn tính như nhau, nên bài trên không bắt được lag nhỏ hơn tầm dự báo $h$. Bài thứ hai cộng nhiễu
lớn vào $y$ từ một mốc trở đi; dòng nào có thời điểm ra dự báo $t - h$ còn trước mốc đó thì feature không được đổi. Với $h$ = 24, `lag_1` đổi ở
23 dòng ngay sau mốc: bị bắt.

Trong hình, ô trên là $y$ bị cộng nhiễu từ vạch đứt. Ô dưới, mỗi vạch là một dòng có feature đổi; vùng xanh là các dòng mà lúc ra dự báo
($h$ = 3) còn trước vạch. `lag_1` đổi ngay trong vùng xanh nên bị bắt, `lag_3` chỉ đổi sau vùng đó.

| Bài kiểm | Bắt được |
|---|---|
| cắt tương lai | rolling không shift hay có tâm, số tính trên cả chuỗi, điền hai phía |
| nhiễu mục tiêu theo $h$ | lag nhỏ hơn $h$, rolling chứa $y_t$ |

Chọn nhiều mốc cắt có chủ đích (điền hai phía chỉ thấy khi mốc rơi vào lỗ). Bài kiểm xanh chỉ nói không thấy rò rỉ ở những mốc đã cắt.

## 138. Ngoại sinh: dùng bản dự báo, không số thật
<!-- ma: ex-ante -->

*Tiếng Anh: exogenous variable · ex-ante vs ex-post · point-in-time*

**Biến ngoại sinh** là biến ngoài chuỗi cần dự báo, dùng làm feature, như nhiệt độ khi dự báo tải điện. **Ex-ante** nghĩa là chỉ dùng bản có
trong tay lúc ra dự báo. **Ex-post** là dùng cả số thật biết về sau: trong backtest đó là rò rỉ.

Ví dụ: tối nay dự báo tải trưa mai. Trưa mai thật 35 °C, nhưng tối nay chỉ có bản dự báo 33 °C, nên feature phải là 33. Cột nhiệt độ thật có
sẵn trong lịch sử nên rất dễ dùng nhầm.

Trong hình, ô trái là nhiệt độ Dallas 1/7 đến 15/7/2024: đen là thật, xanh là dự báo trước 1 ngày, cam là trước 3 ngày. Ô phải là phân phối
sai số: dự báo trước 1 ngày sai trung bình 1,32 °C, trước 3 ngày 2,07 °C.

| Bộ feature (tải ERCOT, 24 giờ tới) | So với chỉ lag |
|---|---|
| + nhiệt độ thật (rò rỉ) | −3,85% |
| + dự báo trước 1 ngày | −3,95% |
| + dự báo trước 3 ngày | +2,92% |

**Đọc bảng.** Dự báo trước 1 ngày đủ tốt để dùng; dự báo trước 3 ngày làm sai số tăng, nên bỏ. Huấn luyện bằng nhiệt độ thật rồi chạy bằng dự
báo trước 3 ngày cũng tệ đi 2,20%.

Với từng biến, hỏi: lúc ra dự báo đã có con số này chưa? Số liệu bị sửa sau khi công bố (GDP, doanh số bán lẻ) thì dùng bản **point-in-time**,
tức đúng con số đã công bố lúc đó. Khi ghép, dùng `merge_asof(direction="backward", tolerance=...)`.

## 139. Phần B: Vấn đề dữ liệu
<!-- ma: phan-b -->

Phần B đi theo thứ tự buổi 3 → 13. Mỗi slide vấn đề có ba thẻ:

- **Dấu hiệu**: thấy gì trên dữ liệu hay trên kết quả.
- **Kiểm bằng**: con số hoặc lệnh nào xác nhận nghi ngờ.
- **Cách sửa**: xử lý thế nào.

## 140. Rò rỉ tương lai gặp ở 8 buổi
<!-- ma: ma-tran -->

*Tiếng Anh: data leakage · look-ahead bias*

Ma trận cho thấy cùng một vấn đề quay lại ở nhiều buổi dưới dạng mới. Rò rỉ tương lai (dùng thông tin chưa có lúc dự báo)
gặp nhiều nhất, ở 8 buổi:

- Sai số ảo (buổi 1).
- λ Box-Cox tính trên cả chuỗi (5).
- Biến giải thích không biết trước (8).
- Cột sai số lẫn vào bản đồ đặc trưng (9).
- Điền thiếu trước khi chia tập (10).
- Bộ lọc nhìn tương lai (12).
- Feature không shift (13).
- Chia dữ liệu ngẫu nhiên (15).

## 141. Sai múi giờ: giờ giả, nóng lúc 20h
<!-- ma: mui-gio -->

*Tiếng Anh: time zone · DST transition · UTC conversion*

**Vấn đề.** Gộp dữ liệu taxi New York theo giờ địa phương naive quanh ngày đổi giờ sinh ra hai lỗi. Rạng sáng Chủ nhật
tháng 3 có một giờ 0 chuyến giả, vì giờ đó không tồn tại. Tháng 11 có một giờ gần gấp đôi, vì hai giờ thật bị gộp làm một.
Ghép taxi (giờ địa phương) với thời tiết (UTC) thì New York "nóng nhất lúc 20h".

**Kiểm.** In 00:00–05:00 của ngày đổi giờ. Tính giờ nóng nhất trung bình: phải rơi vào buổi chiều.

**Sửa.** Gắn múi giờ, đổi sang UTC, rồi mới gộp và ghép.

Ghép lệch múi giờ không báo lỗi mà dời dữ liệu, có thể làm tương quan mưa và số chuyến đổi dấu. Thêm ba lỗi hay gặp: giờ lặp tháng 11 không tách được thì để NaN; chuyến có thời lượng âm là dấu của giờ naive; bỏ dòng trùng trên dữ liệu sự kiện (từng chuyến) sẽ xoá mất chuyến thật.

## 142. Code: đếm chuyến trên giờ naive
<!-- ma: code-b03-dem-naive -->

Đếm thẳng trên giờ không múi giờ để thấy giờ 0 chuyến giả và giờ gấp đôi.

```python
import pandas as pd

cot = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]
t3 = pd.read_parquet("yellow_tripdata_2024-03.parquet", columns=cot)
t11 = pd.read_parquet("yellow_tripdata_2024-11.parquet", columns=cot)

def dem_naive(chuyen):                      # đếm thẳng trên giờ naive
    return chuyen.set_index("tpep_pickup_datetime").resample("h").size()

dem_naive(t3)["2024-03-10 00:00":"2024-03-10 03:00"]    # 02:00 trống
dem_naive(t11)["2024-11-03 00:00":"2024-11-03 03:00"]   # 01:00 gấp đôi
dem_naive(t11)["2024-11-10 01:00"]                      # tuần sau để so
# trừ thẳng hai giờ naive: có khách xuống xe trước khi lên
am = t11["tpep_dropoff_datetime"] < t11["tpep_pickup_datetime"]
```

*Rút gọn từ buoi-03/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `pd.read_parquet(..., columns=...)` (pandas): Đọc tệp Parquet, chỉ lấy các cột cần cho nhanh.
- `set_index(...).resample("h").size()` (pandas): Lấy cột giờ làm mốc, đếm số dòng rơi vào mỗi giờ.
- `s["a":"b"]` (pandas): Cắt chuỗi theo khoảng thời gian, lấy cả hai đầu.

**Từng bước:**

- Dòng 3–5: Đọc giờ đón, giờ trả của tháng 3 và 11.
- Dòng 7–8: Đếm chuyến mỗi giờ, chưa gắn múi giờ.
- Dòng 10–11: Xem quanh hai ngày vặn đồng hồ.
- Dòng 12: Cùng giờ tuần sau làm mốc so.
- Dòng 14: Tìm chuyến trả trước khi đón.

**Kết quả:** Giờ 02:00 ngày 10/3 có 0 chuyến; giờ 01:00 ngày 3/11 có 9.869 chuyến, gần gấp đôi tuần sau (5.318).

## 143. Code: ghép hai nguồn trên cùng UTC
<!-- ma: code-b03-ghep-utc -->

Đưa cả hai bảng về UTC rồi mới ghép; ghép gần nhất thì chỉ nhìn về quá khứ.

```python
import pandas as pd

NY = "America/New_York"
# t3: chuyến taxi (giờ NY naive); tt: thời tiết (giờ UTC naive)
tt["ds"] = pd.to_datetime(tt["time"]).dt.tz_localize("UTC")
utc = t3["tpep_pickup_datetime"].dt.tz_localize(
    NY, ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
dem = utc.dt.floor("h").value_counts().rename("y").rename_axis("ds")
dung = dem.reset_index().merge(tt, on="ds")        # cùng UTC mới ghép
gio_ny = dung["ds"].dt.tz_convert(NY).dt.hour
nong = dung.groupby(gio_ny)["nhiet_do"].mean().idxmax()   # phép thử
# bảng phải thưa: lấy giá gần nhất đã có, không nhìn tương lai
trai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00"])})
phai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 09:30",
                     "2024-01-01 10:30"]), "gia": [9, 10]})
pd.merge_asof(trai, phai, on="t")              # backward: nhìn quá khứ
```

*Rút gọn từ buoi-03/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `dt.tz_localize(..., nonexistent="NaT")` (pandas): Gắn múi giờ cho cả cột; giờ không tồn tại hay lặp ghi NaT.
- `merge(tt, on="ds")` (pandas): Nối hai bảng theo cột thời gian chung ds.
- `pd.merge_asof` (pandas): Nối mỗi dòng với dòng gần nhất ở trước nó theo thời gian.

**Từng bước:**

- Dòng 5: Thời tiết vốn là UTC: chỉ cần ghi rõ ra.
- Dòng 6–7: Taxi: gắn giờ New York, đổi UTC; mơ hồ ra NaT.
- Dòng 8–9: Đếm chuyến mỗi giờ UTC, ghép với thời tiết.
- Dòng 10–11: Phép thử: giờ nóng nhất phải là buổi chiều.
- Dòng 13–16: Ghép as-of, mặc định lấy giá đã có trước.

**Kết quả:** Giờ nóng nhất: ghép sai 20h, ghép đúng 16h. Tương quan mưa–số chuyến: sai −0,100, đúng +0,136. merge_asof lấy giá 9.

## 144. Gộp thô quá thì mất mùa vụ
<!-- ma: gop -->

*Tiếng Anh: aggregation · resample · missing values as zero*

Cùng dữ liệu thuê xe vẽ ở ba mức gộp:

- **Theo giờ** (17.544 điểm): hình thành một khối màu, không đọc được gì.
- **Theo ngày**: thấy dao động trong tuần và những ngày rơi xuống gần 0.
- **Theo tháng**: mượt, đẹp, nhưng mất mùa vụ ngày, tuần và các ngày bất thường.

Kết luận "không có mùa vụ tuần" thường đến từ việc chỉ nhìn một hình như vậy. Kiểm bằng heatmap giờ × thứ và ACF tới trễ
168. Lỗi thứ hai hay gặp: `resample().sum()` biến giờ thiếu thành 0. Đếm NaN trên lưới đầy đủ, và dùng `min_count=1` để giữ NaN.

## 145. Code: làm trơn và tăng theo phần trăm
<!-- ma: code-b04-lam-tron-log -->

Thấy bằng số làm trơn xoá mất ngày bão, và thang log đo tăng theo phần trăm.

```python
import pandas as pd

# df: lượt thuê theo giờ, đặt trên lưới giờ đầy đủ
ngay1 = df["cnt"].resample("D").sum(min_count=1)
tron = ngay1.rolling(7, center=True, min_periods=4).mean()
print(ngay1["2012-10-29"], tron["2012-10-29"])   # ngày bão Sandy

th11 = df["cnt"].resample("MS").sum()["2011"]
bang = pd.DataFrame({
    "tăng (lượt)": th11.diff(),           # thang thường hỏi cái này
    "tăng (%)": th11.pct_change() * 100,  # thang log hỏi cái này
})
print(bang.loc["2011-04":"2011-05"].round(1))
```

*Rút gọn từ buoi-04/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `rolling(7, center=True).mean()` (pandas): Trung bình 7 ngày quanh mỗi ngày: 3 ngày trước, 3 ngày sau.
- `diff()` (pandas): Hiệu của mỗi giá trị với giá trị ngay trước nó.
- `pct_change()` (pandas): Tăng bao nhiêu phần so với giá trị trước, ví dụ 0,48 là +48%.

**Từng bước:**

- Dòng 4: Tổng lượt thuê mỗi ngày.
- Dòng 5: Trung bình trượt 7 ngày, lấy ngày giữa làm tâm.
- Dòng 6: So ngày bão: số thật và số đã làm trơn.
- Dòng 8: Tổng tháng của năm 2011.
- Dòng 9–12: Tăng bao nhiêu lượt và tăng bao nhiêu phần trăm.

**Kết quả:** Ngày bão chỉ còn 1 giờ số liệu mà đường trơn vẫn hơn 4.600 lượt. T4 so T3 +48,1%, T5 so T4 +43,2% dù T5 thêm nhiều lượt nhất (+40.951).

## 146. Hai đường trùng khít vì chọn thang
<!-- ma: bieu-do-sai -->

*Tiếng Anh: dual axis · truncated y-axis · misleading chart*

Hình trái vẽ lượt thuê và nhiệt độ trên **trục kép** (hai trục dọc), với trục trái cắt ở 90.000. Hai đường gần như đè
nhau, trông như "lượt thuê bám sát nhiệt độ". Nhưng sự trùng khít là do chọn thang, còn trục cắt làm tháng thấp nhất trông
gần bằng 0. Vẽ lại (hình phải): tách hai hình, số đếm vẽ từ 0, nói về quan hệ bằng scatter. Quan hệ có thật (r = 0,91 qua 12
tháng) nhưng không tăng mãi: tháng 9 mát hơn tháng 7 khoảng 5 °C mà lượt thuê cao nhất năm.

Một lỗi nữa: gộp nhiều năm vào một scatter. Nhiệt độ và lượt thuê có r = 0,771 năm 2011 và 0,714 năm 2012, nhưng gộp hai năm chỉ còn 0,627 vì cả đám chấm dời lên theo năm. Tô màu theo thời gian. Muốn đặt hai chuỗi khác đơn vị lên cùng trục thì đánh chỉ số về 100.

## 147. Code: r từng nhóm thay cho trục kép
<!-- ma: code-b04-tron-nam -->

Đo quan hệ nhiệt độ và lượt thuê bằng số, và thấy trộn hai năm làm quan hệ trông yếu đi.

```python
import pandas as pd

# df: lượt thuê theo giờ; temp đã chia cho 41 độ C
th12 = df[df["nam"] == 2012].resample("MS").agg(
    {"cnt": "sum", "temp": "mean"})
r12 = th12["cnt"].corr(th12["temp"])     # quan hệ theo 12 tháng

nd = df.resample("D").agg({"cnt": "sum", "temp": "mean",
                           "nam": "first"}).dropna()
r_nam = {n: g["cnt"].corr(g["temp"]) for n, g in nd.groupby("nam")}
r_gop = nd["cnt"].corr(nd["temp"])       # trộn hai năm vào một

# thay trục kép: đánh chỉ số, tháng đầu bằng 100
chi_so = th12 / th12.iloc[0] * 100
```

*Rút gọn từ buoi-04/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `agg({cột: cách gộp})` (pandas): Gộp mỗi cột một kiểu: cột này cộng, cột kia lấy trung bình.
- `corr` (pandas): Hệ số tương quan r giữa hai cột, từ −1 tới 1.
- `groupby("nam")` (pandas): Chia bảng thành từng năm để tính riêng cho mỗi năm.

**Từng bước:**

- Dòng 4–5: Tổng lượt và nhiệt độ trung bình mỗi tháng 2012.
- Dòng 6: Hệ số r cho biết hai chuỗi đi cùng nhau tới đâu.
- Dòng 8–10: Theo ngày: tính r riêng cho từng năm.
- Dòng 11: Gộp hai năm rồi tính r để so.
- Dòng 14: Chung một trục mà không cần trục kép.

**Kết quả:** 12 tháng 2012: r = 0,91. Theo ngày: 2011 r = 0,771, 2012 r = 0,714, nhưng gộp hai năm chỉ còn 0,627.

## 148. Doanh thu tăng chưa chắc bán nhiều hơn
<!-- ma: dao-dong -->

*Tiếng Anh: nominal vs real value · inflation adjustment · per capita · Box-Cox*

**Vấn đề.** Doanh thu tăng có thể vì ba lý do: giá tăng (lạm phát), dân số tăng, hoặc mỗi người mua nhiều hơn thật.
Doanh số bán lẻ Mỹ danh nghĩa tăng hơn 4 lần từ 1993; trừ lạm phát (chia CPI) và chia dân số thì chỉ còn +42%.

**Vấn đề thứ hai.** Năm bán nhiều thì dao động trong năm cũng lớn: độ lệch chuẩn tăng từ 15,6 lên 38,1 tỷ USD.

**Sửa.** Log hoặc Box-Cox làm dao động đều lại. Box-Cox là một "núm vặn" λ: λ = 1 giữ nguyên, λ = 0 là log. Chia số ngày
trong tháng để tháng 2 không "sụt" giả mỗi năm.

Khi báo "tăng bao nhiêu", nói rõ là danh nghĩa, thực, hay thực trên đầu người. Đừng dùng chuỗi đã điều chỉnh (ADJUSTED) rồi lại chia số ngày: chênh lệch số ngày bị bỏ hai lần.

## 149. Code: chia số ngày của tháng
<!-- ma: code-b05-lich -->

Thấy chia số ngày có thể đảo dấu kết luận khi so hai tháng liền nhau.

```python
import pandas as pd

# y: doanh số bán lẻ Mỹ theo tháng (triệu USD), chưa điều chỉnh
ba = y["2023-01":"2023-03"]
so_ngay = ba.index.days_in_month               # 31, 28, 31
khong_cn = [sum(d.dayofweek != 6 for d in
                pd.date_range(t, t + pd.offsets.MonthEnd(0)))
            for t in ba.index]                 # ngày bán hàng
bang = pd.DataFrame({"tổng": ba, "mỗi ngày": ba / so_ngay,
                     "mỗi ngày không CN": ba / khong_cn})
thay_doi = bang.pct_change() * 100             # % so với tháng trước
```

*Rút gọn từ buoi-05/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `index.days_in_month` (pandas): Số ngày của tháng chứa mỗi mốc: 28, 30 hay 31.
- `pd.offsets.MonthEnd(0)` (pandas): Nhảy tới ngày cuối của chính tháng đó.
- `pd.date_range` (pandas): Tạo dãy ngày liên tiếp từ ngày đầu tới ngày cuối.

**Từng bước:**

- Dòng 4: Ba tháng đầu năm 2023.
- Dòng 5: Số ngày lịch của từng tháng.
- Dòng 6–8: Đếm số ngày không phải Chủ nhật.
- Dòng 9–10: Doanh số mỗi ngày theo hai cách đếm ngày.
- Dòng 11: So mỗi tháng với tháng trước theo phần trăm.

**Kết quả:** T2 so T1: tổng −3,4% nhưng mỗi ngày +7,0%. T3 so T2: +14,15% thẳng, +3,11% chia ngày, +1,47% bỏ CN, −1,05% ADJUSTED.

## 150. Code: giá thực và trên đầu người
<!-- ma: code-b05-gia-thuc -->

Bóc lạm phát và dân số khỏi doanh số để biết mỗi người thật sự mua thêm bao nhiêu.

```python
import pandas as pd

# y: bán lẻ danh nghĩa, cpi: CPI tháng, dan_so: nghìn người
cpi_du = cpi.interpolate(limit=1, limit_area="inside")  # lấp 10/2025
goc = cpi_du["2025"].mean()                    # năm gốc 2025
thuc = y / cpi_du.reindex(y.index) * goc       # đổi ra giá năm gốc
dau_nguoi = thuc / dan_so.reindex(y.index) * 1e6
nam = pd.DataFrame({"danh nghĩa": y, "giá thực": thuc,
                    "thực trên đầu người": dau_nguoi})
nam = nam.resample("YS").sum()["1993":"2025"]
chi_so = nam / nam.iloc[0] * 100               # 1993 bằng 100
```

*Rút gọn từ buoi-05/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `interpolate(limit=1)` (pandas): Điền ô trống bằng giá trị nằm giữa hai tháng bên cạnh, tối đa một ô.
- `reindex(y.index)` (pandas): Xếp lại chuỗi theo đúng các tháng của y để chia từng tháng.
- `resample("YS").sum()` (pandas): Cộng các tháng thành tổng của từng năm.

**Từng bước:**

- Dòng 4: Lấp đúng một tháng CPI không công bố.
- Dòng 5–6: Chia CPI lúc đó, nhân CPI năm gốc.
- Dòng 7: Chia dân số ra mức mỗi người.
- Dòng 8–10: Cộng thành tổng năm cho cả ba chuỗi.
- Dòng 11: Đánh chỉ số để ba chuỗi so được với nhau.

**Kết quả:** Chỉ số 2025: danh nghĩa 416, giá thực 187, thực trên đầu người 142. Giá chung tăng 2,23 lần, dân số 1,31 lần.

## 151. Code: log và dao động theo mức
<!-- ma: code-b05-log -->

Thấy log biến cùng phần trăm thành cùng khoảng cách, rồi kiểm dao động lớn lên ra sao.

```python
import numpy as np

print(np.log([100, 120, 1000, 1200]).round(3))  # cùng tăng 20%
print(np.log(1.2))                     # khoảng cách log của +20%

# y19: doanh số bán lẻ tháng, 1992 tới 2019
v = y19.to_numpy()[y19.size % 12:]
khoi = v.reshape(-1, 12) / 1000        # 28 năm, 12 tháng, tỷ USD
tb = khoi.mean(axis=1)                 # mức mỗi năm
sd = khoi.std(axis=1, ddof=1)          # dao động trong năm
print(tb[-1] / tb[0], sd[-1] / sd[0])
```

*Rút gọn từ buoi-05/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `np.log` (numpy): Logarit tự nhiên: biến phép nhân thành phép cộng.
- `reshape(-1, 12)` (numpy): Xếp dãy dài thành bảng 12 cột, số dòng tự tính.
- `std(axis=1, ddof=1)` (numpy): Độ lệch chuẩn của từng dòng, tức dao động trong mỗi năm.

**Từng bước:**

- Dòng 3: Cửa hàng nhỏ và siêu thị cùng tăng 20%.
- Dòng 4: Trên thang log cả hai cách nhau đúng log 1,2.
- Dòng 7–8: Cắt chuỗi thành từng năm, mỗi dòng một năm.
- Dòng 9–10: Mức và độ lệch chuẩn của từng năm.
- Dòng 11: So mức và dao động lớn lên bao nhiêu lần.

**Kết quả:** Hai cặp 100, 120 và 1.000, 1.200 cùng cách nhau 0,182 trên thang log. 1992 tới 2019: mức gấp 3,1 lần, dao động gấp 2,4 lần.

## 152. Log rồi exp ngược thì ra trung vị
<!-- ma: doi-nguoc -->

*Tiếng Anh: back-transformation bias · bias adjustment*

Dự báo trên thang log rồi đổi ngược bằng exp thì ra **trung vị**, không phải trung bình. Lý do: log ép số lớn lại, exp kéo
chúng giãn ra. Trên thang log ba mốc 0, 1, 2 cách đều nhau, đổi về thang gốc thành 1; 2,72; 7,39: số lớn bị kéo xa, nên
trung bình bị kéo lên cao hơn trung vị. Trong hình, đổi ngược thẳng thấp hơn trung bình 11,9%. Khi cần tổng hay trung bình
(ví dụ cộng dự báo nhiều cửa hàng) thì hiệu chỉnh bias. Khi chấm bằng MAE (ưa trung vị) thì không cần.

Công thức hiệu chỉnh: nhân dự báo đổi ngược với 1 + σ²/2, với σ là độ lệch chuẩn của sai số trên thang log. Khoảng hụt nhỏ khi σ nhỏ, rất lớn khi σ gần 1. Hiệu chỉnh chỉ sửa lệch do đổi ngược, không sửa lệch do mô hình; nếu mô hình đang dự báo cao thì hiệu chỉnh còn làm sai số tăng. Chỉ bật khi cần trung bình và σ đủ lớn.

## 153. Code: đổi ngược ra trung vị
<!-- ma: code-b05-doi-nguoc -->

Thấy bằng mô phỏng exp của dự báo log hụt trung bình, và hiệu chỉnh bias bù lại.

```python
import numpy as np

w = np.array([0.0, 1.0, 2.0])
print(np.exp(w.mean()), np.exp(w).mean())   # trung vị so với trung bình

x = np.random.default_rng(42).lognormal(5.0, 0.5, 100_000)
wx = np.log(x)                               # thang log
trung_vi = np.exp(wx.mean())                 # đổi ngược thẳng
tb_fpp = trung_vi * (1 + wx.var(ddof=1) / 2)  # hiệu chỉnh bias
print(trung_vi / x.mean() - 1, tb_fpp / x.mean() - 1)
```

*Rút gọn từ buoi-05/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `np.exp` (numpy): Hàm mũ, làm ngược lại log để về đơn vị gốc.
- `default_rng(42).lognormal` (numpy): Sinh số ngẫu nhiên mà log của chúng có hình chuông.
- `var(ddof=1)` (numpy): Phương sai mẫu: độ tản bình phương quanh trung bình.

**Từng bước:**

- Dòng 3–4: Ba số log: exp của trung bình khác trung bình.
- Dòng 6: 100.000 mẫu log-normal, seed 42.
- Dòng 8: Đổi ngược thẳng: ra trung vị.
- Dòng 9: Nhân thêm 1 cộng nửa phương sai log.
- Dòng 10: Mỗi cách hụt bao nhiêu so với trung bình thật.

**Kết quả:** exp(trung bình log) = 2,72, trung bình thật 3,70. Mô phỏng: đổi ngược thẳng hụt 11,9%, có hiệu chỉnh gần khớp.

## 154. Code: seasonal naive có drift trên log
<!-- ma: code-b05-backtest-log -->

Dự báo trên thang log chỉ bằng dữ liệu trước gốc, đổi ngược cả trung vị lẫn trung bình.

```python
import numpy as np
import pandas as pd

def du_bao_log(y, goc, so_buoc=12):
    hoc = y[(y.index < goc) & (y.index >= goc - pd.DateOffset(months=96))]
    w = np.log(hoc)                            # CHỈ dữ liệu trước gốc
    sp = (w - w.shift(12)).dropna()            # sai phân mùa vụ
    drift, s2 = sp.mean(), sp.var(ddof=1)
    tg = pd.date_range(goc, periods=so_buoc, freq="MS")
    w_hat = np.array([w[t - pd.DateOffset(years=1)] + drift for t in tg])
    return pd.DataFrame({"trung_vi": np.exp(w_hat),
                         "trung_binh": np.exp(w_hat) * (1 + s2 / 2)},
                        index=tg)

goc = pd.date_range("2012-01-01", "2018-12-01", freq="MS")  # 84 gốc
bang = pd.concat([du_bao_log(y, g) for g in goc])
```

*Rút gọn từ buoi-05/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `pd.DateOffset(months=96)` (pandas): Lùi đúng 96 tháng theo lịch, không theo số ngày.
- `w - w.shift(12)` (pandas): Sai phân mùa vụ: tháng này trừ cùng tháng năm trước.
- `pd.concat` (pandas): Nối các bảng dự báo của từng gốc thành một bảng dài.

**Từng bước:**

- Dòng 5–6: Lấy 96 tháng ngay trước gốc, rồi lấy log.
- Dòng 7–8: Drift và σ² từ sai phân mùa vụ của log.
- Dòng 10: Cùng tháng năm trước cộng drift.
- Dòng 11–13: Đổi ngược thẳng và đổi ngược có hiệu chỉnh.
- Dòng 15–16: Chạy lại ở mỗi gốc từ 1/2012 tới 12/2018.

**Kết quả:** 1.008 dự báo. Hiệu chỉnh đẩy tổng dự báo lên đúng cỡ σ²/2, chỉ giúp khi dự báo đang thấp; bách hoá vốn đã lệch gần +10%.

## 155. Khai sai chu kỳ: nhịp tuần chui vào xu hướng
<!-- ma: chu-ky-sai -->

*Tiếng Anh: classical decomposition · MSTL · robust decomposition*

Phân rã cổ điển với chu kỳ 24 trên tải điện có nhịp tuần cho xu hướng lõm xuống mỗi cuối tuần. Lý do: xu hướng tính bằng
trung bình một ngày, nên Chủ nhật thấp thì trung bình quanh Chủ nhật thấp. Nhịp tuần đã chui vào xu hướng. Kiểm bằng cách
tính trung bình xu hướng theo thứ. Sửa bằng MSTL(24, 168). Khi có một giờ hỏng, `robust=True` giữ lỗi nằm trọn trong phần dư
thay vì chia nó vào mùa vụ của cả tuần.

Kiểm cả chỗ thứ hai: tính trung bình phần dư theo tháng × giờ. Còn mẫu hình rõ nghĩa là mùa vụ ngày đổi theo mùa đang nằm lại trong phần dư. Robust cứu được một giờ hỏng nhưng không tách được sự kiện kéo dài nhiều ngày như đợt nắng nóng: nó chạy vào xu hướng và mùa vụ, cần thêm biến nhiệt độ. Đầu vào còn NaN thì STL/MSTL trả toàn NaN mà không báo lỗi.

## 156. Code: mùa vụ trốn trong xu hướng, phần dư
<!-- ma: code-b06-mau-hinh -->

Kiểm hai chỗ mùa vụ trốn: xu hướng theo thứ, và phần dư theo tháng và giờ.

```python
import pandas as pd
from statsmodels.tsa.seasonal import MSTL, seasonal_decompose

# y: nhu cầu PJM theo giờ, đã lấp giờ trống, giờ New York
sm24 = seasonal_decompose(y, period=24)
xh = sm24.trend.dropna()
print(xh.groupby(xh.index.dayofweek).mean())   # nhịp tuần ở xu hướng

def ty_le_mau_hinh(resid, y):
    r = resid.dropna()
    g = r.groupby([r.index.month, r.index.hour]).mean()  # tháng, giờ
    return g.var() / y.var()

ms = MSTL(y, periods=(24, 168)).fit()
print(ty_le_mau_hinh(sm24.resid, y), ty_le_mau_hinh(ms.resid, y))
```

*Rút gọn từ buoi-06/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `seasonal_decompose(y, period=24)` (statsmodels): Phân rã cổ điển với một khuôn mùa vụ 24 giờ cho cả năm.
- `MSTL(y, periods=(24, 168))` (statsmodels): Phân rã tách riêng mùa vụ ngày và mùa vụ tuần.
- `ty_le_mau_hinh` (tự viết): Phần dư còn mẫu hình theo lịch tới đâu, đo bằng một con số.

**Từng bước:**

- Dòng 5: Phân rã cổ điển chu kỳ 24 giờ.
- Dòng 6–7: Xu hướng trung bình theo thứ: thấy nhịp tuần.
- Dòng 9–12: Phần dư trung bình theo tháng và giờ.
- Dòng 12: Chia phương sai chuỗi: gần 0 là phần dư sạch.
- Dòng 14–15: So cổ điển với MSTL bằng cùng thước đo.

**Kết quả:** Xu hướng T7, CN thấp hơn giữa tuần khoảng 5.500–6.600 MW. Tỷ lệ mẫu hình tháng × giờ: cổ điển 0,102, MSTL 0,0006.

## 157. Code: MSTL robust với một giờ hỏng
<!-- ma: code-b06-robust -->

Tính trọng số robust tay, rồi thấy robust giữ lỗi một giờ trong phần dư.

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import MSTL

phan_du = np.array([1, -2, 1, 20, -1])
u = np.abs(phan_du) / (6 * np.median(np.abs(phan_du)))
trong_so = np.where(u < 1, (1 - u**2) ** 2, 0)   # điểm lạ ra 0

# y: nhu cầu PJM theo giờ; ms: kết quả MSTL không robust
rb = MSTL(y, periods=(24, 168), stl_kwargs={"robust": True}).fit()
t0 = pd.Timestamp("2024-11-21 17:00")            # giờ hỏng
hom_truoc = t0 - pd.Timedelta("1D")              # ngày không lỗi
print(ms.seasonal.loc[hom_truoc, "seasonal_24"],
      rb.seasonal.loc[hom_truoc, "seasonal_24"])
print(ms.resid[t0], rb.resid[t0])                # lỗi nằm ở đâu
```

*Rút gọn từ buoi-06/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `np.median` (numpy): Trung vị: số đứng giữa, không bị điểm lạ kéo đi.
- `np.where(điều kiện, a, b)` (numpy): Chỗ nào đúng điều kiện lấy a, còn lại lấy b.
- `stl_kwargs={"robust": True}` (statsmodels): Bảo MSTL giảm trọng số điểm có phần dư quá lớn.

**Từng bước:**

- Dòng 5–6: Chia |phần dư| cho 6 lần trung vị của nó.
- Dòng 7: Trọng số: gần 1 là tin, 0 là bỏ qua.
- Dòng 10: Bật robust cho từng lượt STL bên trong.
- Dòng 13–14: Mùa vụ ngày hôm trước có bị kéo lệch không.
- Dòng 15: Phần dư ở giờ hỏng: robust giữ trọn cú rơi.

**Kết quả:** Ví dụ tay: điểm 20 trọng số 0, điểm −2 là 0,79. Không robust, mùa vụ ngày 20/11 lệch khoảng 6.200 MW; robust giữ lỗi trong phần dư.

## 158. Sai phân thừa làm chuỗi tệ hơn
<!-- ma: sai-phan -->

*Tiếng Anh: over-differencing · ADF / KPSS test*

Sai phân như thuốc: đúng liều thì khỏi, quá liều thì hại. Hình so hai trường hợp:

- **Sai phân random walk** (đúng liều): độ lệch chuẩn giảm từ 4,55 xuống 0,96.
- **Sai phân nhiễu trắng vốn đã dừng** (thừa): r₁ = −0,447 và độ lệch chuẩn tăng từ 0,96 lên 1,29.

Dấu hiệu sai phân thừa là r₁ gần −0,5 kèm độ lệch chuẩn tăng. Sửa: bớt một lần sai phân. Chuỗi có xu hướng thẳng thì khử
xu hướng thay vì sai phân.

Quy tắc dừng tay: sai phân tới khi KPSS thôi bác bỏ, nhưng dừng nếu r₁ về gần −0,5 hoặc độ lệch chuẩn tăng. Chuỗi có mùa vụ thì sai phân mùa vụ (y_t − y_(t−m)) trước, vì sai phân thường không bỏ được mùa vụ.

## 159. Code: hai dấu hiệu sai phân thừa
<!-- ma: code-b07-sai-phan -->

Biết khi nào dừng sai phân: r1 gần −0,5 hoặc độ lệch chuẩn tăng lên.

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

def dau_hieu(y):
    y = pd.Series(np.asarray(y, dtype=float)).dropna()
    sp = y.diff().dropna()                       # sai phân một lần
    return acf(sp, nlags=1)[1], y.std(ddof=1), sp.std(ddof=1)

e = np.random.default_rng(42).normal(size=500)
print(dau_hieu(e))              # đã dừng: sai phân là thừa
print(dau_hieu(e.cumsum()))     # random walk: sai phân đúng liều

g = np.log1p(luot.interpolate(limit=3))          # lượt thuê theo giờ
for s in (g.diff(), g.diff(168), g.diff(168).diff()):
    print(acf(s.dropna(), nlags=168)[[1, 24, 168]], s.std(ddof=1))
```

*Rút gọn từ buoi-07/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `diff(k)` (pandas): Trừ mỗi giá trị cho giá trị cách k bước; k = 168: cùng giờ tuần trước.
- `np.log1p(y)` (numpy): Tính log(1 + y), dùng được cả khi y bằng 0.
- `std(ddof=1)` (pandas): Độ lệch chuẩn mẫu: đo chuỗi dao động mạnh cỡ nào.

**Từng bước:**

- Dòng 5–8: Trả r1 sau sai phân và độ lệch chuẩn trước, sau.
- Dòng 11: Sai phân chuỗi đã dừng để thấy dấu hiệu thừa.
- Dòng 12: Sai phân random walk để thấy đúng liều.
- Dòng 14: log(1 + y) vì có giờ không ai thuê xe.
- Dòng 15–16: So sai phân thường, mùa vụ 168 và cả hai.

**Kết quả:** Nhiễu trắng: r1 = −0,447, độ lệch chuẩn 0,96 lên 1,29 (thừa). Random walk: 4,55 xuống 0,96. Lượt thuê: 168 rồi thường giảm 0,589 xuống 0,427.

## 160. r = 0,97 chưa chắc là quan hệ thật
<!-- ma: tuong-quan-gia -->

*Tiếng Anh: spurious correlation · Durbin–Watson statistic*

**Tương quan giả**: CPI (chỉ số giá tiêu dùng) và dân số Mỹ có r = 0,974 chỉ vì cả hai cùng tăng theo thời gian. Kiểm bằng
hai cách:

- **Sai phân rồi đo lại**: tháng nào dân số tăng nhanh thì giá có tăng nhanh không? r sau sai phân chỉ còn −0,207.
- **Durbin–Watson**: con số đo phần dư của hồi quy có tự tương quan không. Gần 2 là không, gần 0 là tự tương quan mạnh.
  Gần 0 báo hiệu tương quan giả.

Khi viết kết luận: nói "đi cùng", không nói "gây ra".

R² cao, t lớn mà Durbin–Watson gần 0 là bộ ba dấu hiệu của hồi quy giả.

## 161. Code: hồi quy giả và Durbin–Watson
<!-- ma: code-b08-tuong-quan-gia -->

Bắt tương quan giả bằng hai phép kiểm: DW của phần dư và tương quan sau sai phân.

```python
import numpy as np

def durbin_watson(e):                            # gần 2 tốt, gần 0 xấu
    return np.sum(np.diff(e) ** 2) / np.sum(e**2)

def hoi_quy_don(x, y):
    X = np.column_stack([np.ones(x.size), x])
    he_so = np.linalg.lstsq(X, y, rcond=None)[0]  # bình phương nhỏ nhất
    du = y - X @ he_so                            # phần dư
    se = np.sqrt(du @ du / (x.size - 2) * np.linalg.inv(X.T @ X)[1, 1])
    return 1 - du.var() / y.var(), he_so[1] / se, durbin_watson(du)

# kt: CPI và dân số Mỹ theo tháng, 1990–2024
r2, t, dw = hoi_quy_don(kt["cpi"].to_numpy(), kt["dan_so"].to_numpy())
d = kt.diff().dropna()                            # thay đổi hằng tháng
r_sai_phan = d["cpi"].corr(d["dan_so"])
```

*Rút gọn từ buoi-08/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `np.linalg.lstsq(X, y)` (numpy): Tìm hệ số đường thẳng làm tổng bình phương sai lệch nhỏ nhất.
- `durbin_watson` (tự viết): Tổng bình phương bước nhảy của phần dư chia tổng bình phương phần dư.
- `diff().corr()` (pandas): Lấy thay đổi hằng tháng rồi tính tương quan của hai cột.

**Từng bước:**

- Dòng 3–4: DW đo phần dư có đổi chậm theo thời gian không.
- Dòng 6–8: Khớp đường thẳng, lấy phần dư.
- Dòng 9–10: Trả R², t của hệ số và DW.
- Dòng 13: Hồi quy dân số theo CPI trên mức.
- Dòng 14–15: Hỏi lại câu đúng: các thay đổi có đi cùng?

**Kết quả:** Trên mức: r 0,974, R² 0,95, t 88,6. Nhưng DW 0,0051 và r sau sai phân −0,207: tương quan giả.

## 162. Lạnh cũng tăng, nóng cũng tăng: hình chữ U
<!-- ma: chu-u -->

*Tiếng Anh: nonlinear relationship · CDD / HDD (degree days) · mutual information*

Tải điện ERCOT (Texas) theo nhiệt độ có hình chữ U: trời nóng bật điều hoà, trời lạnh bật sưởi, nhiệt độ vừa phải thì tải
thấp. Pearson là 0,616, trông "khá mạnh", nhưng đó là trộn của nhánh lạnh (−0,649) với nhánh nóng (+0,910). Một đường thẳng
bỏ sót hẳn nhánh lạnh: R² chỉ 0,379. Sửa bằng hai biến (R² lên 0,812):

- **CDD** (độ nóng) = max(T − 18,33, 0).
- **HDD** (độ lạnh) = max(18,33 − T, 0).

Ví dụ 25 °C cho CDD 6,67 và HDD 0. Mốc 18,33 °C (65 °F) là quy ước, gần với mốc tốt nhất 19,5 °C trong hình phải.

Muốn kiểm mutual information có ý nghĩa trên chuỗi thời gian thì hoán vị theo khối. Hoán vị từng điểm phá mất tự tương quan, nên hai chuỗi độc lập cũng bị kết luận là "có quan hệ".

## 163. Code: CDD, HDD và MI xáo theo khối
<!-- ma: code-b08-cdd-mi -->

Tách quan hệ chữ U thành hai nhánh, và kiểm MI có thật bằng cách xáo cả tuần.

```python
import numpy as np
from sklearn.feature_selection import mutual_info_regression
t, y = df["nhiet"].to_numpy(), df["tai"].to_numpy() / 1000   # °C, GW
cdd, hdd = np.maximum(t - 18.33, 0), np.maximum(18.33 - t, 0)  # mốc 65 °F
def r2_hoi_quy(*cot):
    X = np.column_stack([np.ones(y.size), *cot])
    du = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
    return 1 - du.var() / y.var()
r2_thang, r2_hai_nhanh = r2_hoi_quy(t), r2_hoi_quy(cdd, hdd)
def mi(x, v):
    return mutual_info_regression(x.reshape(-1, 1), v, random_state=0)[0]
rng = np.random.default_rng(0)
khoi = [y[i:i + 168] for i in range(0, y.size, 168)]      # khối 1 tuần
xao = [np.concatenate([khoi[i] for i in rng.permutation(len(khoi))])
       for _ in range(100)]
nguong = np.quantile([mi(t, v) for v in xao], 0.95)      # so với mi(t, y)
```

*Rút gọn từ buoi-08/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `np.maximum(a, 0)` (numpy): Giữ phần dương, còn lại thành 0: đúng cách tính CDD, HDD.
- `mutual_info_regression` (sklearn): Ước lượng thông tin tương hỗ: biết x bớt được bao nhiêu điều về y.
- `rng.permutation(n)` (numpy): Xáo ngẫu nhiên thứ tự 0 tới n − 1, ở đây là thứ tự các khối.

**Từng bước:**

- Dòng 4: Độ nóng và độ lạnh so với mốc 18,33 °C.
- Dòng 5–9: R² theo nhiệt độ so với theo CDD + HDD.
- Dòng 10–11: MI bắt được cả quan hệ cong.
- Dòng 13–15: Xáo thứ tự các tuần, giữ nhịp trong tuần.
- Dòng 16: Ngưỡng 95% của MI khi không có quan hệ.

**Kết quả:** R² tăng từ 0,379 lên 0,812. Nhánh lạnh r = −0,649, nhánh nóng +0,910. MI thật 0,862 vượt xa ngưỡng xáo khối 0,124.

## 164. isna() không thấy dòng bị mất
<!-- ma: thieu-moc -->

*Tiếng Anh: missing timestamps vs missing values · reindex*

Có hai loại thiếu:

- **Thiếu giá trị**: có dòng, ô rỗng.
- **Thiếu mốc**: cả dòng không có.

`isna()` chỉ thấy loại thứ nhất. Ví dụ đo mỗi 30 phút từ 00:00 tới 02:30 phải có 6 mốc, tệp có 5 dòng: `isna()` báo 1 ô
thiếu (02:00), nhưng mốc 01:00 mất cả dòng. Trên dữ liệu trạm thật có 249 mốc bị mất, dồn vào vài tháng, và phần lớn lỗ
chỉ dài một bước. Sửa: `reindex` lên lưới đầy đủ trước mọi việc khác.

## 165. Code: dựng lưới rồi mới đếm thiếu
<!-- ma: code-b10-luoi -->

isna() chỉ thấy ô rỗng; dựng lưới đủ mốc mới thấy cả những dòng không tồn tại.

```python
import numpy as np
import pandas as pd

bang = pd.Series([25, 25, 26, np.nan, 26], index=pd.to_datetime([
    "2024-01-01 00:00", "2024-01-01 00:30", "2024-01-01 01:30",
    "2024-01-01 02:00", "2024-01-01 02:30"]))
luoi = pd.date_range(bang.index.min(), bang.index.max(), freq="30min")
bang.isna().sum()                      # 1: chỉ thấy ô rỗng
bang.reindex(luoi).isna().sum()        # 2: thấy cả mốc 01:00

def do_dai_lo(y):                      # độ dài từng đoạn NaN liền nhau
    thieu = y.isna()
    nhom = (thieu != thieu.shift()).cumsum()[thieu]
    return nhom.groupby(nhom).size()
```

*Rút gọn từ buoi-10/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `pd.date_range` (pandas): Sinh dãy mốc thời gian đều nhau giữa hai đầu, ở đây mỗi 30 phút.
- `reindex` (pandas): Đặt chuỗi lên bộ mốc mới; mốc nào chưa có dòng thì thành NaN.
- `isna().sum()` (pandas): Đếm số ô rỗng trong những dòng đang có mặt.

**Từng bước:**

- Dòng 4–6: Năm dòng đo, mốc 01:00 không có dòng nào.
- Dòng 7: Dựng lưới đủ mọi mốc 30 phút.
- Dòng 8–9: Đếm thiếu trước và sau khi đưa lên lưới.
- Dòng 11–14: Đánh số từng đoạn thiếu rồi đếm độ dài.

**Kết quả:** Ví dụ: isna() báo 1, lên lưới ra 2. Nội Bài 2024: lưới 17.568 mốc, tệp 17.319 dòng, thiếu 249 mốc mà isna() chỉ thấy 2 ô.

## 166. Vì sao số bị mất quyết định có điền được không
<!-- ma: mcar -->

*Tiếng Anh: missing data mechanism · MCAR / MAR / MNAR*

Điền được hay không phụ thuộc **vì sao** số bị mất, không phụ thuộc cách điền giỏi tới đâu. Có ba cơ chế thiếu:

- **MCAR** (thiếu hoàn toàn ngẫu nhiên): việc mất không liên quan gì, như mất mạng vài phút. Phần còn lại vẫn đại diện; điền thoải mái.
- **MAR** (thiếu ngẫu nhiên khi đã biết thứ khác): việc mất phụ thuộc một thứ đã đo được, như trạm hay hỏng vào mùa mưa. Điền được
  nếu cách điền dùng thông tin đó.
- **MNAR** (thiếu không ngẫu nhiên): việc mất phụ thuộc chính giá trị bị mất, như cảm biến bụi tắt khi ô nhiễm cực cao. Phần còn lại
  đã bị lọc lệch; không cách điền nào cứu được.

Ví dụ: bốn giờ PM2.5 thật 10, 20, 30, 40 (trung bình 25). Cảm biến tắt khi trên 30, chỉ còn 10, 20, 30, trung bình 20: đã lệch 5 trước
khi điền bất cứ gì.

## 167. Thiếu vì chính giá trị: điền kiểu gì cũng lệch
<!-- ma: mnar -->

*Tiếng Anh: missing data mechanism · MCAR / MAR / MNAR*

Có ba **cơ chế thiếu**:

- **MCAR**: thiếu do may rủi, điền được thoải mái.
- **MAR**: thiếu do một thứ đã đo được. Điền được nếu cách điền dùng thứ đó.
- **MNAR**: thiếu do chính giá trị bị thiếu, ví dụ cảm biến tắt khi ô nhiễm quá cao.

Mô phỏng trong hình: MNAR mất 16,2% số điểm, toàn ở phía cao; điền xong, trung bình còn −0,30 so với −0,005 thật. MCAR chỉ lệch một
phần nghìn.

Kiểm MNAR trên dữ liệu thật bằng cách so các trạm hàng xóm lúc một trạm thiếu và lúc có số. Khi trạm Dongsi (Bắc Kinh) thiếu, các
trạm khác còn thấp hơn 3%: không có bằng chứng MNAR. Phải đo, đừng giả định. Báo tỷ lệ thiếu theo trạm, theo tháng, không chỉ một
con số chung.

## 168. Code: MNAR làm lệch, kiểm bằng số
<!-- ma: code-b10-mnar -->

Thấy bằng mô phỏng vì sao MNAR điền kiểu gì cũng lệch, rồi kiểm cơ chế trên dữ liệu thật.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
moc = pd.date_range("2024-01-01", periods=5000, freq="30min")
that = pd.Series(rng.normal(0, 1, 5000), index=moc)
mcar = that.mask(pd.Series(rng.random(5000) < 0.1, index=moc))  # may rủi
mnar = that.mask(that > 1.0)            # cảm biến tắt khi giá trị cao
noi = lambda s: s.interpolate(limit_direction="both")
that.mean(), noi(mcar).mean(), noi(mnar).mean()

def bang_chung_mnar(bang, tram):        # bang: PM2.5 của 12 trạm
    khac = bang.drop(columns=[tram]).mean(axis=1)   # 11 trạm còn lại
    thieu = bang[tram].isna()
    return khac[thieu].mean() / khac[~thieu].mean() - 1
```

*Rút gọn từ buoi-10/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `mask(dieu_kien)` (pandas): Đổi thành NaN mọi ô thoả điều kiện, giữ nguyên các ô còn lại.
- `interpolate` (pandas): Nối thẳng hai số hai bên để lấp ô NaN ở giữa.
- `default_rng(0).normal` (numpy): Bộ sinh số ngẫu nhiên có seed, chạy lại ra đúng số cũ.

**Từng bước:**

- Dòng 4–6: Năm nghìn điểm thật, biết trước đáp án.
- Dòng 7: MCAR: xoá ngẫu nhiên 10% số điểm.
- Dòng 8: MNAR: xoá đúng những điểm cao hơn 1.
- Dòng 9–10: Nội suy rồi so trung bình với số thật.
- Dòng 12–15: Khi trạm mất số, trạm khác cao hay thấp?

**Kết quả:** Mô phỏng: MNAR mất 16,2%, điền xong trung bình −0,30 thay vì −0,005; MCAR gần như không lệch. Dongsi thiếu thì trạm khác thấp hơn 3,0%.

## 169. 9,999 km không phải số đo
<!-- ma: tra-hinh -->

*Tiếng Anh: sentinel value · flag column · quality flag*

**Mã trá hình** là con số quy ước của nguồn dữ liệu, không phải giá trị đo. Ở trạm Nội Bài, 35% số dòng tầm nhìn đúng bằng
9,999 km, nghĩa là "10 km trở lên". Cùng hình còn có hai thứ khác không phải số đo thật: độ ẩm chạm trần 100% và nhiệt độ
chỉ có giá trị nguyên. Kiểm bằng `value_counts().head()` và đọc tài liệu nguồn. Sửa: đổi thành NaN và thêm cột cờ ghi lý do.
Đừng `dropna()` cả dòng: dòng có tầm nhìn 9,999 vẫn có nhiệt độ hợp lệ.

Hai việc nữa trước khi tin một con số. Đo độ phân giải trước khi gọi một đoạn lặp là cảm biến đứng yên: nhiệt độ ghi số nguyên thì lặp vài giờ là bình thường. Và đọc bảng cờ chất lượng của nguồn: ở GHCNh, mã 4 không phải lỗi, chỉ loại 2, 3, 6, 7, o, f. Số 0 do hết hàng cũng là thiếu, không phải số đo; nếu không đánh dấu, mô hình dự báo thấp, cửa hàng nhập ít, lại hết hàng, và vòng lặp tự củng cố.

## 170. Đo độ phân giải trước khi gọi cảm biến kẹt
<!-- ma: do-phan-giai -->

*Tiếng Anh: measurement resolution · stuck sensor · flat-line detection*

Một đoạn số lặp y hệt nhiều giờ liền có thể do cảm biến hỏng, cũng có thể chỉ do cảm biến ghi thô. **Độ phân giải** là bước nhỏ nhất cảm biến
ghi được: ghi tới 1 °C thì 25,6 và 26,4 đều thành 26. **Cảm biến đứng yên** (kẹt) là cảm biến ghi lặp một giá trị dù thực tế đã đổi.

Ví dụ: nhiệt độ thật 25,6; 25,8; 26,1; 26,3; 26,4 °C, ghi tới số nguyên thành năm số 26. Trông như đứng yên, dù nhiệt độ thật đổi gần 1 °C.

Hình khái niệm có hai ô, trục ngang là giờ, xanh là nhiệt độ thật, cam là số ghi được. Ô trái: thật đổi chưa tới một bước phân giải nên số
ghi đứng yên, bình thường. Ô phải: thật đổi vài độ mà số ghi vẫn không nhúc nhích, đó mới là kẹt.

Dữ liệu thật ở Nội Bài 2024 ghi tới 1 °C và có một đoạn 67 bước liên tiếp (33,5 giờ) đúng 26,0 °C. Đặt ngưỡng "đứng yên" 12 giờ thì ra 24
đoạn, quá nhiều để đều là hỏng, nên buổi 10 dùng 18 giờ.

Quy tắc: đo độ phân giải trước, rồi mới đặt ngưỡng. Cùng một đoạn lặp 20 giờ cả ngày lẫn đêm, cảm biến ghi tới 0,1 °C đáng ngờ hơn nhiều so
với cảm biến ghi tới 1 °C. Không dùng một ngưỡng chung cho mọi cảm biến.

## 171. Code: tìm số trông như số đo
<!-- ma: code-b10-tra-hinh -->

Mã, trần, độ phân giải và đoạn kẹt không để lại NaN; phải đo từng dấu vết mới thấy.

```python
import numpy as np
import pandas as pd

goc = pd.read_parquet("ghcnh-noi-bai-2024.parquet")    # tệp thô
goc["relative_humidity"].min()      # ra '100': số đang lưu dạng chữ
rh = pd.to_numeric(goc["relative_humidity"], errors="coerce")
tam_nhin = pd.to_numeric(goc["visibility"], errors="coerce")
(tam_nhin == 9.999).mean(), (rh == 100).mean()    # mã và trần
t = pd.to_numeric(goc["temperature"], errors="coerce").dropna()
np.diff(np.sort(t.unique())).min()  # độ phân giải: bước nhỏ nhất

def doan_mac_ket(y, toi_thieu):     # đoạn lặp dài từ toi_thieu bước
    v = y.dropna()
    nhom = (v != v.shift()).cumsum()
    dem = v.groupby(nhom).agg(so_buoc="size", gia_tri="first")
    return dem[dem["so_buoc"] >= toi_thieu]
```

*Rút gọn từ buoi-10/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `pd.to_numeric` (pandas): Đổi cột chữ thành số; errors="coerce" biến chữ lạ thành NaN.
- `unique` (pandas): Lấy danh sách các giá trị khác nhau trong cột.
- `groupby().agg` (pandas): Gom các dòng cùng nhóm rồi tính số dòng, giá trị đầu của nhóm.

**Từng bước:**

- Dòng 5: Cột số lưu dạng chữ thì min so theo chữ.
- Dòng 6–7: Ép về kiểu số, chữ lạ thành NaN.
- Dòng 8: Tỷ lệ mã 9,999 km và độ ẩm chạm 100%.
- Dòng 9–10: Bước nhỏ nhất giữa hai giá trị khác nhau.
- Dòng 12–16: Đánh số từng đoạn lặp, giữ đoạn đủ dài.

**Kết quả:** Độ ẩm dạng chữ: min '100', max '94'. Hơn 1/3 dòng tầm nhìn là mã 9,999; 5,7% độ ẩm chạm trần. Ngưỡng 18 giờ: 2 đoạn kẹt, dài nhất 33,5 giờ.

## 172. Bảy cách điền: lỗ dài cần giữ hình dạng
<!-- ma: cach-dien -->

*Tiếng Anh: imputation · forward fill · linear / spline interpolation · seasonal · neighbour station*

Sáu giờ liền, hôm nay (21, 23, ?, ?, 27, 25), giá trị thật hai ô thiếu là 26 và 28; hôm qua cùng giờ và trạm hàng xóm đều là (20,
22, 25, 27, 26, 24), trạm ta luôn cao hơn hàng xóm 1 °C.

| Cách điền | Điền được | Dùng tương lai? |
|---|---|---|
| ffill (giữ số gần nhất) | 23; 23 | không |
| tuyến tính (nối 23 với 27) | 24,33; 25,67 | có |
| mùa vụ (cùng giờ hôm qua) | 25; 27 | không |
| hàng xóm (+1 °C) | 26; 28 | không, nếu hệ số học từ quá khứ |

Nội suy tuyến tính: $\hat y_t = y_a + (y_b - y_a)\frac{t-a}{b-a}$, với $a$, $b$ là hai đầu lỗ. Lỗ rơi đúng lúc nhiệt độ lên đỉnh
nên ffill sai nhiều nhất; tuyến tính chỉ biết hai đầu lỗ; mùa vụ và hàng xóm mang thêm hình dạng của đoạn bị mất. Ba cách còn
lại: spline (đường cong trơn qua hai đầu), trung bình theo giờ, Kalman smoother (khớp mô hình rồi ước lượng từ cả hai phía).

Lỗ ngắn: ffill hay tuyến tính đều ổn. Lỗ dài: cần cách mang theo hình dạng. Luôn biết cách điền có dùng tương lai không: tuyến
tính, spline, Kalman smoother đều dùng.

## 173. Chấm cách điền: che thử, và che hai kiểu
<!-- ma: so-sanh-dien -->

*Tiếng Anh: imputation evaluation · artificial masking · point vs block masking*

Muốn biết cách điền nào tốt thì dùng **che nhân tạo**: che các ô đang có số, điền lại, rồi so với số thật. Nội Bài có cả lỗ một bước
lẫn lỗ dài, nên phải che hai kiểu:

| Cách điền | Che điểm 10% (MAE) | Che khối 48 giờ (MAE) |
|---|---|---|
| Tuyến tính | 0,291 (hạng 1) | 2,171 (hạng 5) |
| Hàng xóm | 0,922 (hạng 5) | 1,006 (hạng 1) |

Cùng 7 cách, cùng chuỗi, chỉ đổi kiểu che mà thứ hạng đảo. Lỗ ngắn thì tuyến tính hay `ffill` đều ổn. Lỗ dài cần cách mang theo hình
dạng (trạm hàng xóm, mùa vụ hôm trước), hoặc để trống. Che kiểu nào thì phải chấm bằng đúng kiểu đó.

## 174. Code: các cách điền một lỗ
<!-- ma: code-b10-dien -->

Đặt các cách điền cạnh nhau trên một lỗ nhỏ để thấy cách nào biết hình dạng đoạn mất.

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents

hom_nay = pd.Series([21, 23, np.nan, np.nan, 27, 25.0])  # thật: 26, 28
hom_qua = pd.Series([20, 22, 25, 27, 26, 24.0])
tay = {"ffill": hom_nay.ffill(),                    # nhân quả
       "tuyến tính": hom_nay.interpolate(),         # nhìn số phía sau
       "spline": hom_nay.interpolate(method="spline", order=3),
       "mùa vụ": hom_nay.fillna(hom_qua),           # cùng giờ hôm qua
       "hàng xóm + 1": hom_nay.fillna(hom_qua + 1)}
def dien_kalman(y, chu_ky=48):          # mức + nhịp ngày, nhìn hai phía
    kq = UnobservedComponents(y.to_numpy(float), level="local level",
        freq_seasonal=[{"period": chu_ky, "harmonics": 2}]).fit(disp=False)
    lam_tron = kq.smoother_results.smoothed_forecasts[0]
    return y.fillna(pd.Series(lam_tron, index=y.index))
```

*Rút gọn từ buoi-10/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `ffill` (pandas): Lấp ô trống bằng số gần nhất phía trước.
- `fillna(chuoi_khac)` (pandas): Lấp ô trống bằng số cùng vị trí của một chuỗi khác.
- `UnobservedComponents` (statsmodels): Mô hình chuỗi gồm mức đổi dần và nhịp lặp, ước lượng được ô thiếu.

**Từng bước:**

- Dòng 5–6: Lỗ hai bước hôm nay, và số cùng giờ hôm qua.
- Dòng 7–9: Ba cách chỉ biết hai đầu lỗ.
- Dòng 10–11: Hai cách mượn hình dạng từ nguồn khác.
- Dòng 12–16: Khớp mô hình chuỗi rồi lấy giá trị làm trơn.

**Kết quả:** ffill sai nhiều nhất (3 và 5), tuyến tính 1,67 và 2,33, mùa vụ 1 và 1, hàng xóm trúng cả hai. Nội Bài với Open-Meteo có r = 0,976.

## 175. Code: che điểm và che khối
<!-- ma: code-b10-che -->

Tự xoá số đang có rồi điền lại để có đáp án, và che theo đúng hai kiểu lỗ thật.

```python
import numpy as np

def che_diem(y, ty_le=0.10, seed=0):     # rải 10% ô đang có số
    rng = np.random.default_rng(seed)
    co = np.flatnonzero(y.notna().to_numpy())
    chon = rng.choice(co, size=int(len(co) * ty_le), replace=False)
    return y.mask(np.isin(np.arange(len(y)), chon))

def che_khoi(y, so_buoc=96, so_khoi=5, seed=0):   # 5 khối 48 giờ
    rng = np.random.default_rng(seed)
    z = y.copy()
    for _ in range(so_khoi):
        dau = int(rng.integers(0, len(y) - so_buoc))
        z.iloc[dau:dau + so_buoc] = np.nan
    return z
cham = lambda that, z, dien: (dien(z) - that)[z.isna()].abs().mean()
```

*Rút gọn từ buoi-10/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `rng.choice` (numpy): Rút ngẫu nhiên một số phần tử, replace=False để không trùng.
- `rng.integers` (numpy): Rút một số nguyên ngẫu nhiên trong khoảng cho trước.
- `iloc[a:b]` (pandas): Chọn các dòng theo vị trí từ a tới trước b.

**Từng bước:**

- Dòng 3–7: Chọn ngẫu nhiên 10% ô có số rồi xoá.
- Dòng 9–15: Xoá năm đoạn liền, mỗi đoạn 96 bước.
- Dòng 16: MAE chỉ tính trên những ô vừa bị che.

**Kết quả:** Tuyến tính hạng 1 ở lỗ ngắn (MAE 0,291 °C) nhưng hạng 5 ở lỗ 48 giờ (2,171); hàng xóm đi ngược lại, hạng 5 lên hạng 1.

## 176. Điền nhân quả: có số mới, số cũ không đổi
<!-- ma: dien-nhan-qua -->

*Tiếng Anh: causal imputation · two-sided interpolation · cutoff test*

Điền chỗ thiếu xong mà backtest (chấm trên đoạn giữ lại) đẹp bất thường thì nên hỏi: cách điền có dùng số của tập kiểm không? **Cách điền
nhân quả** chỉ dùng dữ liệu trước ô đang điền. **Nội suy hai phía** nhìn cả số phía sau; nếu số đó thuộc tập kiểm thì thông tin tập kiểm đã
chảy vào tập học, tức là rò rỉ.

Ví dụ chuỗi 20, NaN, 30. `ffill` (lấy số gần nhất phía trước) điền 20, cắt dữ liệu hay không cũng ra 20. Nội suy tuyến tính điền 25 nhờ số
30 phía sau; cắt dữ liệu tại mốc thứ hai thì không còn 30, nó không điền được hoặc điền khác.

Trong hình, vạch đứt là mốc cắt: bên trái đã biết, bên phải là tương lai. Vuông xanh (`ffill`) chỉ nhìn quá khứ; thoi đỏ (tuyến tính) nằm ở 25
vì đã nhìn sang số 30 bên phải vạch.

**Bài kiểm bằng cắt dữ liệu:** chạy hàm làm sạch trên dữ liệu đầy đủ và trên dữ liệu cắt tại một mốc, rồi so phần trước mốc. Khác nhau là
rò rỉ. Mốc cắt phải nằm trong một lỗ: cắt ở chỗ dữ liệu liền thì nội suy chẳng điền gì, kết quả giống hệt và bài kiểm báo sạch dù hàm có
rò rỉ.

Pipeline đúng: chia tập trước, chỉ điền lỗ ngắn bằng cách nhân quả (buổi 10: ≤ 6 bước = 3 giờ), lỗ dài để trống, và xuất cột cờ `da_dien`.

## 177. Lỗ dài: đừng lấp bằng đường phẳng
<!-- ma: dien -->

*Tiếng Anh: imputation · forward fill · causal imputation · MNAR*

Lỗ 48 giờ trong hình được lấp theo mấy cách:

- `ffill` và nội suy tuyến tính: thành đường phẳng 24 °C, xoá sạch nhịp ngày (thật dao động 21–27 °C).
- Dùng trạm hàng xóm: giữ được hình dạng.

Hai nguyên tắc:

- **Không dùng tương lai để điền quá khứ.** Nội suy ngày 3 giữa ngày 2 và ngày 4 là đã dùng ngày 4. Vì vậy chia tập trước
  rồi mới điền, và chỉ dùng cách điền nhân quả (chỉ dùng dữ liệu trước chỗ đang điền).
- **Lỗ ngắn có thể điền, lỗ dài nên để trống.**

Thêm một chỗ cần cẩn thận: khi dữ liệu thiếu vì chính giá trị của nó (MNAR, ví dụ cảm biến tắt lúc ô nhiễm quá cao) thì điền kiểu
gì cũng lệch.

Cột cờ `da_dien` đi theo dữ liệu, để về sau giảm trọng số hoặc bỏ các ô đã điền khỏi tập chấm. Kalman smoother và nội suy tuyến tính đều dùng điểm phía sau, tức không nhân quả; ffill hợp với chuỗi bậc thang như giá niêm yết.

## 178. Code: chỉ điền lỗ ngắn, kiểm rò rỉ
<!-- ma: code-b10-lam-sach -->

Gói làm sạch thành hàm chỉ điền lỗ ngắn kèm cột cờ, rồi dùng máy kiểm có rò rỉ không.

```python
import pandas as pd

def lam_sach(v, nghi, gioi_han=6, cach=dien_mua_vu):
    sach = v.where(~nghi)                  # loại số nghi ngờ TRƯỚC
    thieu = sach.isna()
    nhom = (thieu != thieu.shift()).cumsum()
    do_dai = nhom.map(nhom[thieu].value_counts()).where(thieu, 0)
    dien_duoc = thieu & (do_dai <= gioi_han)    # chỉ lỗ tới 3 giờ
    kq = sach.where(~dien_duoc, cach(sach))     # mùa vụ: nhân quả
    return pd.DataFrame({"y": kq, "da_dien": dien_duoc & kq.notna()})

def kiem_ro_ri(ham, bang, moc_cat):        # moc_cat nằm TRONG một lỗ
    truoc = moc_cat - pd.Timedelta("30min")
    day = ham(bang).loc[:truoc, "y"]
    cat = ham(bang.loc[:truoc])["y"]
    return (day - cat).abs().max() > 1e-9  # True là có rò rỉ
```

*Rút gọn từ buoi-10/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `where(dieu_kien, khac)` (pandas): Giữ ô thoả điều kiện, ô còn lại lấy từ chuỗi khác.
- `value_counts` (pandas): Đếm mỗi giá trị xuất hiện bao nhiêu lần, ở đây là cỡ mỗi lỗ.
- `kiem_ro_ri` (tự viết): So kết quả làm sạch trên dữ liệu đủ và dữ liệu cắt tại một mốc.

**Từng bước:**

- Dòng 4: Biến số nghi ngờ thành NaN trước tiên.
- Dòng 5–7: Đo lại độ dài lỗ cho từng ô thiếu.
- Dòng 8–9: Chỉ điền lỗ ngắn, lỗ dài để trống.
- Dòng 10: Xuất kèm cột cờ ô nào là số điền.
- Dòng 12–16: Làm sạch đủ và cắt, so phần trước mốc cắt.

**Kết quả:** Nội Bài: 130 ô bị loại vì nghi ngờ, 198 ô được điền, 181 ô để trống. Điền mọi lỗ bằng tuyến tính bị bắt khi cắt trong lỗ.

## 179. Bốn kiểu bất thường, bốn cách bắt
<!-- ma: bon-loai -->

*Tiếng Anh: additive outlier (AO) · level shift (LS) · temporary change (TC) · variance change*

"Ngoại lai" không phải một thứ, mà có bốn loại:

- **Điểm đơn (AO)**: một điểm lệch rồi về ngay. Quanh mức 10: … 10, 25, 10 …
- **Dịch mức (LS)**: nhảy lên một bậc và ở lại. … 10, 20, 20, 20.
- **Thay đổi tạm (TC)**: nhảy lên rồi tắt dần. … 20, 15, 12, 11, 10.
- **Đổi phương sai**: mức giữ nguyên nhưng dao động to ra.

Loại quyết định cách phát hiện và cách xử lý, không phải độ lớn: Hampel cho điểm đơn, tìm điểm gãy cho dịch mức, MAD trên phần dư STL
cho đổi phương sai. Câu hỏi đầu tiên với một điểm lạ: đây là lỗi, giai đoạn tạm thời, hay một trạng thái mới?

## 180. Code: nhận loại bất thường
<!-- ma: code-b11-bon-loai -->

Bốn loại bất thường giống nhau ở mốc lạ; chỉ các điểm sau mốc đó mới tách được chúng.

```python
import numpy as np
import pandas as pd

bon = {"AO (điểm đơn)": [10, 10, 10, 25, 10, 10, 10, 10],
       "dịch mức": [10, 10, 10, 20, 20, 20, 20, 20],
       "thay đổi tạm": [10, 10, 10, 20, 15, 12, 11, 10],
       "đổi phương sai": [10, 10, 10, 14, 6, 13, 7, 14]}
bang = pd.DataFrame({ten: {
    "điểm 4": v[3],
    "TB 4 điểm sau": np.mean(v[4:]),               # có ở lại không
    "điểm cuối": v[-1],                            # có hồi về không
    "độ lệch chuẩn sau": np.std(v[4:], ddof=1),    # có rung mạnh hơn
} for ten, v in bon.items()}).T
```

*Rút gọn từ buoi-11/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `np.mean` (numpy): Trung bình cộng các số.
- `np.std(ddof=1)` (numpy): Độ lệch chuẩn mẫu: số đo độ dao động quanh trung bình.

**Từng bước:**

- Dòng 4–7: Bốn chuỗi tám điểm, cùng mức nền 10.
- Dòng 9: Riêng điểm lạ thì chưa phân biệt được.
- Dòng 10–12: Nhìn sau mốc lạ: ở lại, hồi về hay rung.
- Dòng 13: Làm một bảng, mỗi dòng một loại.

**Kết quả:** Điểm 4 không tách được ba loại đầu; bốn điểm sau thì tách: AO về 10, dịch mức ở lại 20, thay đổi tạm hồi dần. Đổi phương sai: độ lệch chuẩn 4,08.

## 181. z-score: ngoại lai kéo cả ngưỡng lên theo
<!-- ma: z-score-masking -->

*Tiếng Anh: z-score · 3σ rule · masking / swamping*

Cách tìm ngoại lai quen thuộc nhất là **z-score**: một điểm cách trung bình bao nhiêu lần độ lệch chuẩn, vượt 3 thì gắn cờ. Vấn đề là chính
ngoại lai kéo cả trung bình lẫn độ lệch chuẩn lên. Hiện tượng ngoại lai tự che mình và che nhau gọi là **masking**.

Ví dụ mười số 10, 12, 11, 13, 12, 50, 11, 12, 13, 12. Trung bình 156 / 10 = 15,6; độ lệch chuẩn $s$ ≈ 12,1 (bỏ số 50 thì chỉ khoảng 1).

$$
z_t = \frac{y_t - \bar y}{s}, \qquad |z_t| > 3\ \Rightarrow\ \text{gắn cờ}
$$

Thay số: z của 50 là (50 − 15,6) / 12,1 ≈ 2,84, không vượt 3. Thay số 12 cuối bằng 60 thì z của 50 còn 1,61, của 60 chỉ 2,15: không cái nào
bị bắt. Với 10 số, $|z|$ không bao giờ vượt được $9/\sqrt{10} \approx 2{,}85$, nên ngưỡng 3 ở đây không bao giờ gắn cờ gì.

Trong hình, trục ngang là vị trí 1 đến 10, trục dọc là giá trị. Vạch cam đứt (trung bình + 3σ) nằm ở 52, cao hơn chính số 50; thêm số 60 thì
vạch lên gần 76. Vạch xanh lá (trung vị + 3·MAD) đứng yên sát dữ liệu.

Trên 3.653 ngày lượt xem Wikipedia tiếng Việt, 3σ gắn cờ 16 ngày; thêm một ngày giả thật lớn thì còn 5. Chiều ngược lại, ngoại lai làm điểm
bình thường bị gắn cờ oan, gọi là **swamping**. Vì vậy "không vượt 3σ" không có nghĩa là "dữ liệu sạch".

## 182. 3σ bỏ sót chính ngoại lai
<!-- ma: masking -->

*Tiếng Anh: outlier · z-score · masking · MAD · Hampel filter*

**Z-score** đo một điểm cách trung bình bao nhiêu độ lệch chuẩn; |z| > 3 thì gắn cờ ngoại lai. Nhưng trung bình và độ lệch
chuẩn đều bị ngoại lai kéo, nên ngoại lai tự che mình. Hiện tượng này gọi là **masking**. Với năm số 5, 5, 5, 5, 100, điểm 100
chỉ có z = 1,79 và không bị gắn cờ. Trên lượt xem Wikipedia, 3σ gắn cờ 16 ngày; thêm **một** ngày cực lớn thì chỉ còn 5.
Sửa bằng **MAD** (dùng trung vị thay trung bình) và **Hampel** (MAD trên cửa sổ trượt, bắt ngoại lai theo mức địa phương).

Với mẫu nhỏ, |z| không bao giờ vượt quá (n − 1)/√n. Mười số thì tối đa 2,85, nên ngưỡng 3 không bao giờ gắn cờ được điểm nào.

## 183. Code: ngưỡng 3σ bỏ sót ngoại lai
<!-- ma: code-b11-masking -->

Thấy bằng số vì sao ngoại lai lớn kéo chính trung bình và độ lệch chuẩn dùng để bắt nó.

```python
import numpy as np
import pandas as pd

def z_score(y, nguong=3.0):
    return ((y - y.mean()) / y.std()).abs() > nguong

mot = np.array([10, 12, 11, 13, 12, 50, 11, 12, 13, 12.0])
z = (mot - mot.mean()) / mot.std(ddof=1)     # z của số 50
tran = (mot.size - 1) / np.sqrt(mot.size)   # trần của |z| khi n = 10

them = tong.copy()                          # tong: lượt xem Wikipedia
them.iloc[len(tong) // 2] = tong.max() * 8  # thêm một ngày giả
z_score(tong).sum(), z_score(them).sum()    # số ngày bị gắn cờ
```

*Rút gọn từ buoi-11/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `y.mean(), y.std()` (pandas): Trung bình và độ lệch chuẩn của cả chuỗi, ngoại lai kéo được cả hai.
- `np.sqrt` (numpy): Căn bậc hai.

**Từng bước:**

- Dòng 4–5: Gắn cờ khi cách trung bình quá 3σ.
- Dòng 7–8: Mười số có một ngoại lai 50.
- Dòng 9: Mười số thì |z| không bao giờ vượt 2,85.
- Dòng 11–13: Thêm một ngày giả rồi đếm lại số cờ.

**Kết quả:** z của 50 chỉ 2,84, dưới trần 2,85 nên không bị bắt. Wikipedia: thêm một ngày giả, số ngày bị gắn cờ tụt từ 16 xuống 5.

## 184. MAD và Hampel: đo bằng trung vị, so tại chỗ
<!-- ma: mad-hampel -->

*Tiếng Anh: median absolute deviation (MAD) · 1.4826 · Hampel filter*

Cần một thước đo độ dao động mà vài điểm cực lớn không kéo được. Trung vị không quan tâm số lớn nhất lớn cỡ nào, chỉ quan tâm nó nằm ở nửa
trên. **MAD** là trung vị của khoảng cách tới trung vị, nhân 1,4826 để cùng thang với độ lệch chuẩn khi dữ liệu hình chuông.

Cùng mười số ở slide trước: trung vị 12. Khoảng cách tới 12 xếp tăng là 0, 0, 0, 0, 1, 1, 1, 1, 2, 38, trung vị 1. MAD = 1,4826 × 1 ≈ 1,48.

$$
\text{điểm}_t = \frac{\lvert y_t - \operatorname{median}(y)\rvert}{1{,}4826 \cdot \operatorname{median}\lvert y - \operatorname{median}(y)\rvert}
$$

Nói bằng lời: chia khoảng cách tới trung vị cho độ dao động điển hình, lớn hơn 3 là ngoại lai. Điểm của 50 là 38 / 1,48 ≈ 25,6, bị gắn cờ.
Điểm của 10 là 2 / 1,48 ≈ 1,35, bình thường.

Chuỗi có xu hướng thì so với trung vị cả chuỗi không có nghĩa. **Hampel** tính đúng công thức trên trong cửa sổ ±k điểm quanh mỗi điểm. Trong
hình, dải xanh là trung vị ± 3·MAD của cửa sổ ±15 điểm, đi theo xu hướng; điểm vọt khỏi dải bị gắn cờ đỏ, còn ngưỡng 3σ toàn chuỗi (nét đứt)
nằm cao hơn mọi điểm. Trên lượt xem Wikipedia, Hampel ±15 ngày gắn cờ 121 ngày (3,31%), rải đều mười năm.

Lưu ý: cửa sổ có tâm nhìn cả hai phía, nên Hampel dùng để làm sạch lịch sử, không dùng làm feature dự báo.

## 185. Hampel: so với mức địa phương
<!-- ma: hampel -->

*Tiếng Anh: MAD · Hampel filter · winsorize · IQR rule*

**MAD** (độ lệch tuyệt đối trung vị) đo độ dao động bằng trung vị, nên ngoại lai không kéo được. **Hampel** so mỗi điểm với trung
vị và MAD của cửa sổ quanh nó, nên xu hướng không làm nó mù. Trên 3.653 ngày lượt xem Wikipedia:

| Cách | Số ngày gắn cờ | Tỷ lệ |
|---|---|---|
| 3σ toàn chuỗi | 16 | 0,44% |
| Hampel ±15 ngày | 121 | 3,31% |
| STL robust, mùa vụ tuần | 616 | 16,86% |

3σ toàn chuỗi chỉ gắn cờ những ngày mức cao; Hampel rải cờ đều mười năm. Trước khi tin một ngưỡng, xem nó gắn cờ bao nhiêu phần
trăm dữ liệu. Sửa bằng **winsorize** (kéo điểm về trung vị địa phương) hoặc biến giả, không xoá mốc.

## 186. Code: MAD và bộ lọc Hampel
<!-- ma: code-b11-hampel -->

Đổi trung bình thành trung vị để ngoại lai không kéo được thước đo, rồi trượt theo cửa sổ.

```python
import numpy as np
import pandas as pd

HE_SO_MAD = 1.4826             # đưa MAD về thang độ lệch chuẩn

def mad_score(y):
    tv = y.median()
    mad = (y - tv).abs().median()
    return (y - tv).abs() / (HE_SO_MAD * mad)

def hampel(y, cua_so=15, nguong=3.0):     # cửa sổ ±15 ngày quanh điểm
    k = 2 * cua_so + 1
    tv = y.rolling(k, center=True, min_periods=cua_so).median()
    mad = (y - tv).abs().rolling(k, center=True, min_periods=cua_so).median()
    diem = (y - tv).abs() / (HE_SO_MAD * mad.replace(0, np.nan))
    return diem.fillna(0) > nguong
```

*Rút gọn từ buoi-11/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `median` (pandas): Trung vị: số đứng giữa khi xếp thứ tự, ngoại lai không kéo được.
- `rolling(k, center=True)` (pandas): Cửa sổ k điểm đặt giữa là điểm đang xét.
- `hampel` (tự viết): Gắn cờ điểm lệch xa trung vị quanh nó, tính theo MAD.

**Từng bước:**

- Dòng 6–9: Khoảng cách tới trung vị, chia cho MAD.
- Dòng 11–13: Trung vị của 31 ngày quanh mỗi điểm.
- Dòng 14: MAD cũng tính trên cửa sổ đó.
- Dòng 15–16: Gắn cờ điểm cách mức địa phương quá 3.

**Kết quả:** Điểm MAD của 50 là 25,6, bắt ngay. Wikipedia: Hampel gắn cờ 121 ngày rải đều mười năm, thêm ngày giả chỉ thành 123.

## 187. Gắn cờ xong: giữ, winsorize hay biến giả
<!-- ma: xu-ly-bat-thuong -->

*Tiếng Anh: winsorizing · event log · dummy variable*

Ngưỡng thống kê chỉ nói "điểm này khác", không biết khác vì lỗi đo hay vì sự kiện ta đang muốn dự báo. Trên lượt xem bài "Tết Nguyên Đán",
cả năm cách tìm ngoại lai đều gắn cờ 10/10 đỉnh Tết.

Ba công cụ xử lý. **Winsorize**: kéo điểm bị gắn cờ về trung vị địa phương, không xoá mốc. **Nhật ký sự kiện**: danh sách các mốc có sự
kiện thật đã biết, không được sửa. **Biến giả**: cột 0/1 đánh dấu sự kiện, để mô hình học riêng phần đó.

Ví dụ chuỗi 12, 11, 13, 90, 12, trung vị địa phương 12, điểm 90 bị gắn cờ:

| Cách | Kết quả |
|---|---|
| xoá | 12, 11, 13, —, 12: lưới thời gian thủng một mốc |
| winsorize | 12, 11, 13, 12, 12, kèm cột `da_sua` = 1 |
| ngày đó là Tết (có trong nhật ký) | giữ nguyên 90 |

**Đọc bảng.** Chỉ hai cách dưới giữ đủ số mốc; cách cuối giữ cả biên độ thật. Hình khái niệm cho thấy đúng điều này: dấu × xám là số bị gắn
cờ, xoá để lại một lỗ, winsorize thay bằng 12.

Chọn theo **loại** bất thường: lỗi đo thì winsorize; sự kiện thật thì giữ và ghi nhật ký; dịch mức thì thêm biến giả, vì nó ảnh hưởng mọi dự
báo về sau. Một đỉnh Black Friday lặp mỗi năm mà winsorize đi là xoá chính cái cửa hàng cần dự báo.

## 188. Tết không phải ngoại lai
<!-- ma: tet -->

*Tiếng Anh: event log · dummy variable · moving holiday*

Chạy bộ bắt ngoại lai trên lượt xem Wikipedia tiếng Việt thì cả 10/10 đỉnh Tết đều bị gắn cờ. Nhưng Tết là bất thường
**thật**. Xoá đi là xoá mất thứ đáng dự báo nhất. Đỉnh Tết còn xê dịch 25 ngày giữa các năm vì theo lịch âm, nên phân rã theo
lịch dương không học được nó. Sửa: giữ nguyên, ghi vào **nhật ký sự kiện**, và thêm biến giả theo lịch âm (buổi 13). Ngoại lai
không đồng nghĩa với lỗi.

Chọn cách sửa theo loại bất thường: điểm đơn thì winsorize, dịch mức hay thay đổi tạm thì biến giả. Không xoá mốc, vì xoá làm thủng lưới thời gian.

## 189. Code: giữ Tết, winsorize lỗi đo
<!-- ma: code-b11-tet -->

Ngưỡng nào cũng gắn cờ Tết; nhật ký sự kiện giữ nó lại, còn lỗi đo thì thay chứ không xoá.

```python
import pandas as pd

dinh = [g.idxmax() for _, g in tet.groupby(tet.index.year)]  # đỉnh Tết
[bool(hampel(tet)[d]) for d in dinh]      # cả 10 đỉnh bị gắn cờ

def xu_ly_ngoai_lai(y, cua_so=15, bo_qua_su_kien=()):
    y = y.astype(float)
    su_kien = y.index.isin(pd.DatetimeIndex(bo_qua_su_kien))
    co = hampel(y, cua_so) & ~su_kien         # sự kiện thật thì bỏ qua
    k = 2 * cua_so + 1
    tv = y.rolling(k, center=True, min_periods=cua_so).median()
    sach = y.where(~co, tv)                   # winsorize, không xoá mốc
    return pd.DataFrame({"y": y, "sach": sach, "da_sua": co})

xl = xu_ly_ngoai_lai(tet, bo_qua_su_kien=dinh)
```

*Rút gọn từ buoi-11/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `idxmax` (pandas): Trả về mốc thời gian có giá trị lớn nhất.
- `index.isin` (pandas): Đánh dấu mốc nào nằm trong một danh sách cho trước.
- `xu_ly_ngoai_lai` (tự viết): Gắn cờ bằng Hampel, chừa sự kiện, thay điểm lỗi bằng trung vị.

**Từng bước:**

- Dòng 3: Ngày đông nhất mỗi năm chính là Tết.
- Dòng 4: Kiểm xem Hampel có gắn cờ các đỉnh không.
- Dòng 8–9: Bỏ cờ ở những mốc có trong nhật ký.
- Dòng 10–12: Thay điểm lỗi bằng trung vị quanh nó.
- Dòng 15: Chạy trên bài Tết, nhật ký là mười đỉnh.

**Kết quả:** Năm cách gắn cờ đều bắt 10/10 đỉnh Tết. Xoá theo 3σ mất 54 mốc, cả mười đỉnh; winsorize cộng nhật ký giữ đủ 3.653 mốc.

## 190. PELT: mỗi điểm gãy phải trả một penalty
<!-- ma: penalty -->

*Tiếng Anh: changepoint · cost function · PELT · penalty β*

Dịch mức không nằm ở một điểm lạ mà ở chỗ chuỗi trước và sau một mốc khác nhau; mốc đó gọi là **điểm gãy**. Chia chuỗi thành các đoạn, mỗi
đoạn tả bằng trung bình riêng. **Chi phí** một đoạn là tổng bình phương khoảng cách tới trung bình đoạn. Chia càng nhiều càng khớp, tới mức
mỗi điểm một đoạn, nên mỗi điểm gãy phải trả một **penalty** $\beta$.

Ví dụ 10, 11, 10, 9, 10, 20, 21, 19, 20, 20, $\beta = 3 \ln 10 \approx 6{,}9$:

| Cách chia | Chi phí | Tổng có penalty |
|---|---|---|
| không cắt | 254 | 254 |
| cắt trước điểm 6 | 4 | 4 + 6,9 = 10,9 |
| cắt thêm trước điểm 4 | 3,17 | 3,17 + 13,8 = 17,0 |

$$
\min_{K,\ \tau_1 < \dots < \tau_K}\ \sum_{k=0}^{K} c\left(y_{\tau_k : \tau_{k+1}}\right) + \beta K
$$

Nói bằng lời: chọn số điểm gãy $K$ và vị trí sao cho tổng chi phí các đoạn cộng $\beta$ cho mỗi điểm gãy là nhỏ nhất. Ở đây một điểm gãy thắng.
Trong hình, ô phải có trục ngang là số điểm gãy K, cột xanh là chi phí, cam là penalty; cột K = 1 thấp nhất. **PELT** tìm đúng lời giải này
mà chạy gần tuyến tính theo độ dài chuỗi.

Penalty nhỏ thì cắt nhiều, dễ ra điểm gãy giả; lớn thì không còn điểm gãy nào. Đừng tin một con số: quét nhiều mức và giữ kết quả ổn định.
Chuỗi tăng trưởng thì lấy log trước: số hành khách mức gốc cho 43 điểm gãy, trên log chỉ 2 (2/2020 và 5/2021).

## 191. Lấy log trước: 43 điểm gãy còn 2
<!-- ma: pelt -->

*Tiếng Anh: changepoint detection · PELT · penalty*

**Điểm gãy** là mốc mà trước và sau khác nhau hẳn. **PELT** cắt chuỗi thành các đoạn sao cho tổng chi phí các đoạn cộng penalty là nhỏ
nhất. Mỗi điểm gãy thêm vào phải giảm chi phí nhiều hơn penalty:

- Chia ít quá thì các đoạn không khớp.
- Chia quá nhiều thì khớp rất tốt nhưng vô nghĩa.

Trên hành khách bay EU, chạy trên mức gốc cho 43 điểm gãy. Lý do là dao động lớn dần theo mức, nên mỗi mùa trông như một đoạn mới.
Lấy log trước thì chỉ còn 2 điểm gãy, đúng quanh COVID, và kết quả ổn định trong khoảng penalty 1–4·ln n. PELT hợp với phân tích
toàn bộ lịch sử, không hợp để báo động theo thời gian thực.

Kiểm nhanh khi gọi thư viện: số điểm gãy phải giảm dần khi penalty tăng. Quy ước hay dùng là penalty khoảng 2–3·ln n.

## 192. Code: PELT, lấy log, quét penalty
<!-- ma: code-b11-pelt -->

Tìm mốc chuỗi đổi hẳn bằng PELT, và chỉ tin điểm gãy không đổi khi penalty đổi.

```python
import numpy as np
import ruptures as rpt

v = np.array([10, 11, 10, 9, 10, 20, 21, 19, 20, 20.0])
beta = 3 * np.log(v.size)                 # phí mỗi điểm gãy
rpt.Pelt(model="l2", min_size=2).fit(v).predict(pen=beta)

def diem_gay(y, pen=None, log=True):
    x = np.log(y.to_numpy(float)) if log else y.to_numpy(float)
    pen = 3 * np.log(x.size) if pen is None else pen
    cat = rpt.Pelt(model="l2", min_size=3).fit(x).predict(pen=pen)
    return [y.index[i] for i in cat[:-1]]   # phần tử cuối là độ dài

ln_n = np.log(len(hk))                     # hk: hành khách hàng không EU
for he_so in (0.5, 1, 2, 3, 4, 6, 10):     # quét penalty
    print(he_so, diem_gay(hk, pen=he_so * ln_n))
```

*Rút gọn từ buoi-11/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `rpt.Pelt` (ruptures): Tìm các mốc chia chuỗi thành đoạn, mỗi mốc phải trả một khoản phạt.
- `predict(pen=...)` (ruptures): Trả vị trí kết thúc từng đoạn với mức phạt cho trước.
- `np.log` (numpy): Lấy logarit, biến tăng theo tỷ lệ thành tăng đều.

**Từng bước:**

- Dòng 4–5: Mười số có một bậc, phí cắt là 3 ln n.
- Dòng 6: PELT tìm cách cắt rẻ nhất.
- Dòng 9: Lấy log để mùa hè đông khách thôi gãy.
- Dòng 11–12: Chạy PELT, đổi vị trí cắt thành ngày tháng.
- Dòng 14–16: Thử bảy mức penalty, xem điểm nào trụ lại.

**Kết quả:** Ví dụ: ruptures trả [5, 10]. Hàng không EU: mức gốc ra 43 điểm gãy, log ra 2, ổn định từ 1 tới 4 ln n: 2/2020 (−78,7%) và 5/2021.

## 193. COVID: cách xử lý đổi sai số gần 3 lần
<!-- ma: covid -->

*Tiếng Anh: structural break · changepoint · PELT*

Hành khách hàng không EU sụt mạnh năm 2020–2021. Ba cách xử lý cho sai số (MAPE năm 2023) rất khác nhau:

| Cách | MAPE 2023 |
|---|---|
| Giữ nguyên | 24,01% |
| Coi COVID là thiếu rồi nội suy | 8,71% |
| Cắt, chỉ học sau hồi phục | 18,11% |

Đọc bảng:

- Giữ nguyên thì đoạn sụt kéo cả xu hướng xuống.
- Cắt thì chỉ còn 18 tháng để học mùa vụ, quá ngắn.

Chọn cách nào là một giả định về tương lai, nên phải kiểm bằng dự báo trên dữ liệu sau. Muốn tìm điểm gãy tự động thì
dùng **PELT**, chạy trên log: trên mức gốc nó báo 43 điểm gãy, trên log chỉ còn 2.

Nội suy qua đoạn COVID chỉ hợp khi hành vi quay về như cũ. Nếu sau cú sốc là một mức mới kéo dài, dùng biến giả hoặc chỉ học phần sau (nhưng cần đủ dài để học mùa vụ).

## 194. Code: ba cách xử lý COVID
<!-- ma: code-b11-covid -->

Giữ mô hình cố định, chỉ đổi cách xử lý COVID, để thấy lựa chọn đó đổi dự báo ra sao.

```python
import numpy as np
import pandas as pd

def du_bao_mua_vu_xu_huong(hoc, tam):     # xu hướng thẳng × mùa vụ nhân
    x = hoc.to_numpy(float)
    t = np.arange(x.size)
    a, b = np.polyfit(t, x, 1)
    he_so = pd.Series(x / np.maximum(a * t + b, 1), index=hoc.index)
    he_so = he_so.groupby(hoc.index.month).mean()
    moc = pd.date_range(hoc.index[-1], periods=tam + 1, freq="MS")[1:]
    return np.array([(a * (x.size + i) + b) * he_so[m.month]
                     for i, m in enumerate(moc)])
hoc = hk[hk.index < "2023-01-01"]         # học tới hết 2022
covid = (hoc.index >= "2020-03-01") & (hoc.index <= "2021-06-30")
cach = {"giữ nguyên": hoc, "coi là thiếu": hoc.mask(covid).interpolate(),
        "cắt": hoc[hoc.index > "2021-06-30"]}
```

*Rút gọn từ buoi-11/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `np.polyfit(t, x, 1)` (numpy): Tìm đường thẳng khớp dữ liệu nhất, trả độ dốc và tung độ gốc.
- `groupby(month).mean()` (pandas): Trung bình theo từng tháng trong năm.
- `mask().interpolate()` (pandas): Coi đoạn đã chọn là thiếu rồi nối thẳng qua nó.

**Từng bước:**

- Dòng 5–7: Khớp một đường thẳng làm xu hướng.
- Dòng 8–9: Mỗi tháng là một tỷ lệ so với xu hướng.
- Dòng 10–12: Kéo dài xu hướng, nhân hệ số tháng.
- Dòng 14: Đánh dấu 16 tháng COVID.
- Dòng 15–16: Ba cách: giữ, coi là thiếu rồi nội suy, cắt.

**Kết quả:** MAPE 2023: coi là thiếu 8,71%, giữ nguyên 24,01%. Giữ nguyên thì 16 tháng sụt kéo xu hướng xuống, dự báo thấp gần 20 triệu khách/tháng.

## 195. Khử nhiễu: trailing nhân quả nhưng trễ
<!-- ma: khu-nhieu -->

*Tiếng Anh: signal + noise · trailing / centered moving average · causal filter*

Chuỗi = tín hiệu + nhiễu ($y_t = s_t + \varepsilon_t$); khử nhiễu là ước lượng $s_t$. Trung bình trượt $k$ điểm có hai kiểu:

- **trailing**: $\frac{1}{k}\sum_{j=0}^{k-1} y_{t-j}$, chỉ các điểm đã qua;
- **centered**: lấy cả điểm trước lẫn sau, tức có số của tương lai.

Năm giờ điện 10, 12, 14, 30, 16, tại giờ 3: trailing (10 + 12 + 14) / 3 = 12; centered (12 + 14 + 30) / 3 = 18,67, đã chứa số 30
của giờ 4 mà đứng ở giờ 3 chưa ai biết. Đổi giờ cuối từ 16 thành 40 thì centered ở giờ 4 đổi từ 20 thành 28: một con số quá khứ
bị sửa khi dữ liệu mới về.

Centered dùng để mô tả, vẽ, tách xu hướng; không bao giờ làm feature dự báo. Trailing dùng được, đổi lại nó trễ: trung bình 13
điểm có đỉnh đến sau tín hiệu 6 bước, đúng (13 − 1) / 2.

## 196. Nyquist: lấy mẫu thưa thì sinh nhịp giả
<!-- ma: nyquist -->

*Tiếng Anh: Nyquist frequency · sampling frequency f_s · aliasing*

Hạ mẫu (10 phút → 1 giờ) làm sai thì tạo ra một chu kỳ không có thật. **Tần số lấy mẫu** $f_s$ là số mẫu mỗi đơn vị thời gian. **Tần số
Nyquist** bằng $f_s/2$: chỉ thấy đúng dao động chậm hơn mức này. Dao động nhanh hơn bị gập thành dao động chậm giả, gọi là **aliasing**, giống
bánh xe trong phim cũ trông như quay ngược.

Ví dụ sóng lặp mỗi 4 bước: 0, 1, 0, −1, … Lấy mỗi 3 bước một mẫu ra 0, −1, 0, 1, 0, −1: lặp mỗi 12 bước gốc, chậm gấp ba sóng thật.

$$
f_{\text{Nyquist}} = \frac{f_s}{2}, \qquad f_{\text{giả}} = \lvert f - k f_s \rvert, \quad k = \operatorname{round}(f / f_s)
$$

Nói bằng lời: lấy tần số thật trừ bội số gần nhất của tần số lấy mẫu. Sóng 1/4 mỗi bước, lấy mẫu 1/3 mỗi bước, Nyquist 1/6; |1/4 − 1/3| = 1/12,
tức chu kỳ giả 12 bước. Trong hình, đường xám là sóng thật, chấm đỏ là các mẫu; nối các chấm được sóng chậm nét đứt không có thật.

Trên tín hiệu mô phỏng 10 phút một mẫu, dao động 43 phút (1,4 chu kỳ/giờ) sau khi hạ xuống 1 giờ thành chu kỳ giả 2,5 giờ:
|1,4 − 1 × 1| = 0,4 chu kỳ/giờ. Công suất ở chu kỳ đó là 64,0 khi hạ mẫu thô, 0,0 khi lọc trước.

Cách tránh: **lọc thông thấp** (bỏ dao động nhanh) trước khi hạ mẫu, ở khoảng 0,8 lần Nyquist mới. Bộ lọc này chạy hai chiều, nên chỉ dùng
tiền xử lý lịch sử, không dùng trong feature.

## 197. Đọc phổ trước khi lọc và hạ mẫu
<!-- ma: aliasing -->

*Tiếng Anh: periodogram · aliasing · Nyquist frequency · low-pass filter · downsampling*

**Phổ** (periodogram) cho biết dao động của chuỗi nằm ở tần số nào. Hình trái: cả hai cảm biến có đỉnh ở chu kỳ khoảng một
ngày; điện thiết bị còn 17,8% năng lượng ở dao động nhanh hơn một giờ, còn nhiệt độ phòng gần như không có. Vì vậy lọc nhiệt độ chỉ
thêm trễ, còn điện mới có chỗ để khử nhiễu. Đọc phổ trước mọi quyết định lọc và hạ mẫu.

**Aliasing**: lấy mẫu quá thưa thì một dao động nhanh biến thành một nhịp chậm không có thật, như bánh xe quay ngược trong
phim cũ. Giới hạn **Nyquist** là một nửa tần số lấy mẫu; dao động nhanh hơn mức đó sẽ bị "gập" xuống. Trong hình, cảm biến
đo mỗi 10 phút có dao động 43 phút; hạ mẫu thô xuống 1 giờ thì sinh ra chu kỳ giả 2,5 giờ. Sửa: lọc thông thấp (bỏ dao
động nhanh) trước khi hạ mẫu.

Tính được chu kỳ giả: f_giả = |f − k·f_s|, với f_s là tần số lấy mẫu và k là số nguyên gần f/f_s nhất. Dao động 1,4 vòng mỗi giờ lấy mẫu mỗi giờ (f_s = 1) gập xuống thành 0,4 vòng mỗi giờ, tức chu kỳ giả 2,5 giờ.

## 198. Code: đọc phổ bằng Welch
<!-- ma: code-b12-pho -->

Trước khi lọc, đo xem dao động nhanh chiếm bao nhiêu năng lượng và nhịp nào mạnh nhất.

```python
import numpy as np
from scipy import signal

FS = 6.0                                  # 6 mẫu mỗi giờ (10 phút/mẫu)
for v in ([1, -1, 1, -1, 1, -1], [1, 1, 1, -1, -1, -1]):
    f, P = signal.periodogram(v)
    f[np.argmax(P)]                       # tần số mạnh nhất

def pho(y, fs=FS, nperseg=2048):          # trừ trung bình trước
    y = np.asarray(y, dtype=float)
    y = y - np.nanmean(y)
    return signal.welch(y, fs=fs, nperseg=min(nperseg, y.size))

f, P = pho(dien)                          # dien: điện thiết bị, Wh
chu_ky_manh = 1 / f[1:][np.argmax(P[1:])]  # tính bằng giờ
nhanh = P[f > 1].sum() / P[1:].sum()      # phần năng lượng dưới 1 giờ
```

*Rút gọn từ buoi-12/tu-hoc.ipynb, phần 2.*

**Thư viện và hàm:**

- `signal.periodogram` (scipy): Tính năng lượng của từng tần số trong một dãy số.
- `signal.welch` (scipy): Phổ ổn định: chia chuỗi thành đoạn, lấy trung bình phổ các đoạn.
- `np.argmax` (numpy): Vị trí của giá trị lớn nhất.

**Từng bước:**

- Dòng 5–7: Hai dãy tay: lặp mỗi 2 bước và mỗi 6 bước.
- Dòng 9–12: Trừ trung bình để tần số 0 không át hết.
- Dòng 14–15: Chu kỳ mạnh nhất, bỏ qua tần số 0.
- Dòng 16: Tỷ lệ năng lượng ở dao động nhanh hơn 1 giờ.

**Kết quả:** Ví dụ tay: đỉnh ở 0,5 và 1/6. Cả hai cảm biến có đỉnh 24,38 giờ; điện thiết bị có 17,8% năng lượng dưới 1 giờ, nhiệt độ phòng 0,0.

## 199. Code: lọc thông thấp rồi mới hạ mẫu
<!-- ma: code-b12-aliasing -->

Hạ mẫu thô làm dao động nhanh gập thành chu kỳ giả; lọc trước thì chu kỳ đó biến mất.

```python
import numpy as np
from scipy import signal
FS = 6.0                                   # 6 mẫu mỗi giờ

def f_gia(f, fs):                          # tần số giả sau khi lấy mẫu
    return abs(f - round(f / fs) * fs)

def ha_mau(y, buoc=6, loc_truoc=True):
    y = np.asarray(y, dtype=float)
    if not loc_truoc:
        return y[::buoc]                   # hạ mẫu thô
    sos = signal.butter(8, 0.8 * FS / buoc / 2, fs=FS, output="sos")
    return signal.sosfiltfilt(sos, y)[::buoc]   # hai chiều: chỉ lịch sử

t = np.arange(6000) / FS                   # thời gian, tính bằng giờ
y = 20 + 2 * np.sin(2 * np.pi * t / 24) + 0.5 * np.sin(2 * np.pi * 1.4 * t)
```

*Rút gọn từ buoi-12/tu-hoc.ipynb, phần 3.*

**Thư viện và hàm:**

- `signal.butter` (scipy): Thiết kế bộ lọc Butterworth: giữ tần số thấp, chặn tần số cao.
- `signal.sosfiltfilt` (scipy): Lọc xuôi rồi lọc ngược: không trễ nhưng dùng cả tương lai.
- `y[::buoc]` (numpy): Lấy một phần tử sau mỗi buoc phần tử.

**Từng bước:**

- Dòng 5–6: Tính tần số bị gập về sau khi lấy mẫu.
- Dòng 11: Lấy mỗi 6 mẫu một: dễ sinh chu kỳ giả.
- Dòng 12: Bộ lọc cắt ở 0,8 lần Nyquist mới.
- Dòng 13: Lọc hai chiều rồi mới lấy mẫu.
- Dòng 15–16: Nhịp ngày cộng dao động 1,4 chu kỳ/giờ.

**Kết quả:** 1,4 chu kỳ/giờ lấy mẫu mỗi giờ gập thành 0,4: chu kỳ giả 2,5 giờ, công suất 64,0 khi hạ mẫu thô và 0,0 khi lọc trước.

## 200. EWMA: điểm mới nặng hơn, trễ ít hơn
<!-- ma: ewma -->

*Tiếng Anh: exponentially weighted moving average (EWMA) · α, span, com · phase lag*

$$
z_t = \alpha\,y_t + (1-\alpha)\,z_{t-1}, \qquad \alpha = \frac{2}{\text{span}+1} = \frac{1}{1+\text{com}}
$$

Mỗi đầu ra chỉ cần đầu ra trước và số mới: nhân quả, nhớ rất ít. $\alpha$ = 0,5, chuỗi 10, 20, 10: $z$ = 10; 0,5 × 20 + 0,5 × 10
= 15; 0,5 × 10 + 0,5 × 15 = 12,5.

Hình: trung bình trượt 13 điểm chia đều trọng số rồi cắt hẳn; EWMA dồn phần lớn vào vài điểm mới nhất, nên trễ ít hơn cùng độ trơn.
Đo được: trung bình 13 điểm trễ 6 bước; EWMA $\alpha$ = 0,15 trễ 4. Luôn ghi đã khai $\alpha$, span hay com: `com=9` cho $\alpha$
= 0,1, khác hẳn `span=9` ($\alpha$ = 0,2).

## 201. Lọc hai chiều không trễ vì nhìn tương lai
<!-- ma: sau-ho-loc -->

*Tiếng Anh: Savitzky–Golay · Butterworth sosfilt / sosfiltfilt · Kalman filter / smoother*

Mỗi bộ lọc đổi độ trơn lấy trễ, hoặc lấy việc nhìn tương lai. **Savitzky–Golay** khớp đa thức bậc thấp quanh mỗi điểm, giữ được chiều cao
đỉnh. **Butterworth** cắt tần số theo ngưỡng; `sosfilt` chạy một chiều, `sosfiltfilt` chạy xuôi rồi ngược. **Kalman** ước lượng tín hiệu
ẩn từ mô hình mức đổi dần cộng nhiễu; bản filter chỉ dùng quá khứ, bản smoother dùng cả chuỗi.

| Nhân quả | Nhìn tương lai |
|---|---|
| trung bình trượt trailing, EWMA, `sosfilt`, Kalman filter | centered, Savitzky–Golay, `sosfiltfilt`, Kalman smoother |

**Đọc bảng.** Chỉ cột trái dùng được làm feature dự báo. Kalman filter chỉ nhân quả khi tham số ước lượng trên phần học rồi cố định.

Trong hình, tín hiệu nhảy từ 0 lên 1 tại vạch chấm. Bản một chiều (xanh) chỉ lên sau vạch, tức là trễ. Bản xuôi rồi ngược (cam) đã lên trước
vạch: nó "không trễ" vì đầu ra lúc đó dùng số của tương lai.

Trên tín hiệu mô phỏng với mười cấu hình, ba RMSE thấp nhất (centered, Kalman smoother, Savitzky–Golay) đều nhìn tương lai. Đổi 10 số cuối
chuỗi thì `sosfilt` giữ nguyên quá khứ, còn `filtfilt` đổi quá khứ tới 23,615 và làm bẩn ngược 274 bước. Cái giá của nhân quả là trễ:
Butterworth nhân quả trễ 19 bước nên RMSE tệ nhất nhóm (2,419); Kalman filter tốt nhất nhóm (0,584).

Khi xếp hạng bộ lọc cho dự báo, chỉ so các bộ lọc nhân quả với nhau.

## 202. Sáu họ bộ lọc trong một bảng
<!-- ma: bang-bo-loc -->

| Họ bộ lọc | Hiểu đơn giản | Dùng khi | Không dùng khi | Nhân quả |
|---|---|---|---|---|
| trung bình trượt trailing | trung bình k điểm gần nhất | feature dự báo, báo cáo vận hành | cần biết đúng lúc đỉnh: trễ (k − 1)/2 | có |
| trung bình trượt centered | trung bình các điểm quanh nó, cả trước lẫn sau | mô tả, tách xu hướng | mọi feature dự báo | không |
| EWMA | điểm mới nặng hơn điểm cũ | dữ liệu đang chảy về, cần trễ nhỏ | cần cắt đúng một dải tần số | có |
| Savitzky–Golay | khớp đa thức bậc thấp trên cửa sổ quanh điểm | giữ chiều cao đỉnh | feature dự báo, kể cả ở cuối chuỗi | không |
| Butterworth | cắt tần số cao theo ngưỡng | cần bỏ đúng dải tần số cao | bản hai chiều (sosfiltfilt) cho feature | sosfilt có, sosfiltfilt không |
| Kalman filter / smoother | ước lượng tín hiệu ẩn: mức đổi dần cộng nhiễu | có mô hình hợp; dữ liệu có lỗ | smoother cho feature | filter có, smoother không |

Làm feature dự báo thì chỉ chọn trong những dòng nhân quả. Kalman filter chỉ nhân quả khi tham số ước lượng trên phần học rồi cố
định; khớp lại trên cả chuỗi thì quá khứ đổi tới 1,134 (buổi 12, mục 4.5).

## 203. Bộ lọc trơn nhất lại là bộ lọc nhìn tương lai
<!-- ma: bo-loc -->

*Tiếng Anh: moving average · EWMA · Savitzky–Golay · Butterworth · Kalman filter · phase lag*

Buổi 12 so sáu họ bộ lọc: trung bình trượt, EWMA, Savitzky–Golay, Butterworth, Kalman, wavelet. Độ trơn luôn phải trả bằng một trong
hai thứ:

- **Trễ**: trung bình trượt 13 điểm chạy sau tín hiệu 6 bước.
- **Nhìn tương lai**.

Trong mười cấu hình, ba RMSE thấp nhất (trung bình trượt centered, Kalman smoother, Savitzky–Golay) đều nhìn tương lai, nên không dùng
được làm feature. Chỉ so các bộ lọc nhân quả với nhau: Kalman filter tốt nhất (0,584), Butterworth nhân quả tệ nhất (2,419) vì trễ 19
bước. Bảng xếp hạng bộ lọc cho dự báo luôn cần một cột "nhân quả".

Khử nhiễu còn bôi nhoè bước nhảy, nên tìm điểm gãy trước (buổi 11) rồi mới lọc.

## 204. Code: sáu họ bộ lọc
<!-- ma: code-b12-bo-loc -->

Chạy các họ bộ lọc trên cùng chuỗi mô phỏng để so độ trơn, độ trễ và việc nhìn tương lai.

```python
import pandas as pd
from scipy import signal
from statsmodels.tsa.statespace.structural import UnobservedComponents

s = pd.Series(mp)                    # mp: mô phỏng có nhiễu, seed 0
sos = signal.butter(4, 0.05, output="sos")        # Butterworth bậc 4
uc = UnobservedComponents(mp, level="local level")
p = UnobservedComponents(mp[:666], level="local level").fit(disp=0).params
ra = {"MA trailing 13": s.rolling(13, min_periods=1).mean(),
      "MA centered 13": s.rolling(13, center=True, min_periods=1).mean(),
      "EWMA α=0,15": s.ewm(alpha=0.15).mean(),
      "Savitzky–Golay 13": signal.savgol_filter(mp, 13, 2),
      "Butterworth nhân quả": signal.sosfilt(sos, mp),
      "Butterworth filtfilt": signal.sosfiltfilt(sos, mp),
      "Kalman filter": uc.filter(p).filtered_state[0],
      "Kalman smoother": uc.smooth(p).smoothed_state[0]}
```

*Rút gọn từ buoi-12/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `ewm(alpha).mean()` (pandas): Trung bình có trọng số giảm dần về quá khứ.
- `signal.savgol_filter` (scipy): Khớp đa thức trong cửa sổ trượt có tâm, giữ đỉnh tốt.
- `UnobservedComponents` (statsmodels): Mô hình mức đổi dần; filter chỉ dùng quá khứ, smooth dùng cả hai phía.

**Từng bước:**

- Dòng 7–8: Tham số Kalman chỉ học trên 1/3 đầu.
- Dòng 9–11: Trung bình trượt hai kiểu và EWMA.
- Dòng 12: Khớp đa thức bậc 2 trong cửa sổ 13.
- Dòng 13–14: Cùng bộ lọc, một chiều hay hai chiều.
- Dòng 15–16: Kalman: filter chỉ quá khứ, smoother cả hai.

**Kết quả:** Ba RMSE thấp nhất (centered 0,357, Kalman smoother, Savitzky–Golay) đều nhìn tương lai. Nhân quả tốt nhất: Kalman filter 0,584, trễ 1.

## 205. Đổi số cuối: nhân quả thì quá khứ đứng yên
<!-- ma: kiem-nhan-qua -->

*Tiếng Anh: causality test · perturb the tail · tolerance*

Tài liệu thư viện không phải lúc nào cũng nói rõ bộ lọc có nhìn tương lai không. Phép thử chạy được trên mọi hàm: đổi vài giá trị
cuối chuỗi, chạy lại bộ lọc, so đầu ra ở mọi mốc trước đó. Nhân quả thì quá khứ không đổi, chỉ lệch cỡ sai số tính toán.

Ví dụ năm giờ điện 10, 12, 14, 30, 16, trung bình trượt 3 điểm. Đổi giờ cuối từ 16 thành 40: kiểu centered ở giờ 4 đổi từ 20 thành
(14 + 30 + 40) / 3 = 28, một con số quá khứ bị sửa khi dữ liệu mới về. Kiểu trailing ở giờ 4 vẫn 18,67.

Trong hình, ô dưới có trục dọc là |đầu ra mới − cũ| theo thang log; vạch đen đứt ở 390 là chỗ bắt đầu đổi. Bên trái vạch, trailing bằng 0 ở mọi mốc; centered đổi ở 6 mốc ngay trước vạch, đúng nửa cửa sổ 13.

Ba chỗ hay làm sai:

- So **mọi** mốc trước điểm đổi, không bỏ đoạn cuối "cho chắc".
- Dung sai theo thang dữ liệu, ví dụ $\max(10^{-9}, 10^{-7} \times \max|y|)$, vì phép tính số thực có sai số rất nhỏ.
- Tham số ước lượng trên cả chuỗi cũng làm quá khứ đổi: Kalman filter khớp lại tham số trên cả chuỗi đổi quá khứ 1,134, trong khi cùng bộ
  lọc với tham số cố định từ phần học đổi 0,000.

Bài kiểm này không bắt rò rỉ qua cách chia tập (buổi 13).

## 206. Đổi số cuối mà số cũ đổi theo: đã nhìn tương lai
<!-- ma: loc-tuong-lai -->

*Tiếng Anh: causal filter · trailing / centered moving average · EWMA*

**Bộ lọc nhân quả** là bộ lọc mà đầu ra tại thời điểm t chỉ dùng dữ liệu tới t. Muốn biết một bộ lọc có ngầm dùng số của tương
lai không: đổi vài điểm cuối chuỗi rồi chạy lại. Nếu phần trước đó thay đổi thì bộ lọc đã nhìn tương lai. Trong hình, sau
khi đổi 10 giá trị cuối:

- Trung bình trượt **trailing** (chỉ nhìn lùi) không đổi ở mốc nào trước đó.
- Trung bình trượt **centered** (lấy cả trước và sau) đổi ở 6 mốc ngay trước.

Cái giá của rò rỉ: feature làm trơn kiểu centered hay `filtfilt` hứa giảm MAE 24–28%, còn mọi feature nhân quả chỉ giúp
1–6%. Phần thưởng giả đó mất sạch khi dùng thật. Dùng trailing, EWMA hay `sosfilt` làm feature. Luôn chấm trên chuỗi gốc, không chấm trên chuỗi đã làm trơn.

Bộ lọc nhân quả vẫn rò rỉ nếu tham số của nó được ước lượng trên cả chuỗi, ví dụ Kalman filter với phương sai nhiễu ước lượng từ toàn bộ dữ liệu. Ước lượng trên phần học rồi cố định. Làm trơn mục tiêu dùng để chấm còn tệ hơn: MAE trên mục tiêu đã làm trơn là 35,78, trên chuỗi gốc là 46,84.

## 207. Code: trailing và centered
<!-- ma: code-b12-trailing -->

Thấy bằng số kiểu centered viết lại quá khứ khi có số mới, còn trailing thì không.

```python
import pandas as pd

y = pd.Series([10, 12, 14, 30, 16], index=range(1, 6), dtype=float)
trailing = y.rolling(3).mean()                # chỉ quá khứ, nhưng trễ
centered = y.rolling(3, center=True).mean()   # nửa cửa sổ ở tương lai

y2 = y.copy()
y2[5] = 40                                    # số mới về khác đi
y2.rolling(3).mean()[4]                       # giờ 4 giữ nguyên
y2.rolling(3, center=True).mean()[4]          # giờ 4 bị viết lại
```

*Rút gọn từ buoi-12/tu-hoc.ipynb, phần 1.*

**Thư viện và hàm:**

- `rolling(3).mean()` (pandas): Trung bình ba điểm: điểm đang xét và hai điểm trước.
- `rolling(3, center=True)` (pandas): Cửa sổ đặt giữa, nên dùng cả điểm ngay sau.

**Từng bước:**

- Dòng 3: Năm giờ điện, giờ 4 vọt lên 30.
- Dòng 4–5: Hai kiểu trung bình trượt ba điểm.
- Dòng 7–8: Đổi riêng giờ cuối từ 16 thành 40.
- Dòng 9–10: Xem giá trị của giờ 4 có đổi theo không.

**Kết quả:** Giờ 3 kiểu centered ra 18,67 vì đã cộng số 30 của giờ 4. Đổi giờ 5 thành 40: centered giờ 4 nhảy từ 20 lên 28, trailing vẫn 18,67.

## 208. Code: đổi đuôi, xem đầu
<!-- ma: code-b12-kiem-nhan-qua -->

Một phép thử chạy được cho mọi bộ lọc: đổi đuôi chuỗi, xem quá khứ có bị đổi theo không.

```python
import numpy as np

def kiem_nhan_qua(ham_loc, y, so_diem_doi=10, thay_doi=50.0):
    y = np.asarray(y, dtype=float)
    k0 = y.size - so_diem_doi
    goc = np.asarray(ham_loc(y), dtype=float)
    y_doi = y.copy()
    y_doi[k0:] += thay_doi                 # cộng 50 vào 10 số cuối
    moi = np.asarray(ham_loc(y_doi), dtype=float)
    lech = np.abs(np.nan_to_num(moi[:k0]) - np.nan_to_num(goc[:k0]))
    nguong = max(1e-9, 1e-7 * float(np.nanmax(np.abs(y))))  # sai số máy
    return lech.max() > nguong             # True: có nhìn tương lai

{ten: kiem_nhan_qua(ham, mp) for ten, ham in BO_LOC.items()}
```

*Rút gọn từ buoi-12/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `np.nan_to_num` (numpy): Đổi NaN thành 0 để phép trừ không ra NaN.
- `np.nanmax` (numpy): Giá trị lớn nhất, bỏ qua các ô NaN.
- `kiem_nhan_qua` (tự viết): Báo một hàm lọc có dùng số tương lai hay không.

**Từng bước:**

- Dòng 6: Chạy bộ lọc trên chuỗi gốc.
- Dòng 7–9: Đổi đuôi chuỗi rồi chạy lại.
- Dòng 10: So mọi mốc trước chỗ đổi.
- Dòng 11–12: Lệch quá sai số máy tức là nhìn tương lai.
- Dòng 14: Kiểm cả mười cấu hình bộ lọc.

**Kết quả:** 6/10 cấu hình nhìn tương lai. Centered 13 đổi quá khứ 23,077; Kalman khớp lại cả chuỗi đổi 1,134; filtfilt làm bẩn ngược 274 bước.

## 209. Làm trơn mục tiêu là chấm trên đề dễ hơn
<!-- ma: muc-tieu-lam-tron -->

*Tiếng Anh: target smoothing · evaluation on the raw series*

Cùng một mô hình dự báo điện một giờ tới, chấm trên hai mục tiêu:

| Chấm trên | MAE (Wh) |
|---|---|
| điện thật | 46,84 |
| điện đã làm trơn (centered 13 điểm) | 35,78 |

Sai số giảm 23,6% mà mô hình không hề tốt hơn: nó chỉ được chấm trên một đại lượng dễ hơn và không có thật. Hình vẽ hai mục tiêu
chồng lên nhau: đường làm trơn cắt mất các đỉnh nhọn, đúng những chỗ mô hình sai nhiều nhất.

Được làm trơn feature bằng bộ lọc nhân quả; không bao giờ làm trơn mục tiêu dùng để chấm. Nếu cần "điện trung bình 3 giờ tới" thì
định nghĩa lại mục tiêu thành đúng đại lượng đó và ghi rõ trong báo cáo.

## 210. Code: đo cái giá của rò rỉ
<!-- ma: code-b12-gia-ro-ri -->

Đo feature nhìn tương lai làm sai số đẹp giả bao nhiêu, khi chấm trên chuỗi gốc.

```python
import numpy as np
import pandas as pd

def danh_gia_feature(y, ham_loc, tam=6, ty_le_hoc=0.7):
    bang = pd.DataFrame({"loc": ham_loc(y.to_numpy()), "y": y.to_numpy(),
                         "muc_tieu": y.shift(-tam).to_numpy()}).dropna()
    cat = int(len(bang) * ty_le_hoc)       # 70% đầu học, 30% sau chấm
    hoc, kt = bang.iloc[:cat], bang.iloc[cat:]
    X = lambda d: np.column_stack([np.ones(len(d)), d["loc"], d["y"]])
    he_so = np.linalg.lstsq(X(hoc), hoc["muc_tieu"], rcond=None)[0]
    du_bao = X(kt) @ he_so
    return np.mean(np.abs(du_bao - kt["muc_tieu"]))   # trên chuỗi gốc

goc = danh_gia_feature(dien, lambda v: v)     # không lọc
centered = danh_gia_feature(dien, ma_giua)    # nhìn tương lai
trailing = danh_gia_feature(dien, ma_truoc)   # nhân quả
```

*Rút gọn từ buoi-12/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `shift(-6)` (pandas): Kéo chuỗi lên 6 bước: dòng t nhận giá trị của t + 6.
- `np.linalg.lstsq` (numpy): Tìm hệ số hồi quy tuyến tính cho sai số bình phương nhỏ nhất.
- `np.column_stack` (numpy): Ghép các cột thành một ma trận.

**Từng bước:**

- Dòng 5–6: Feature là bộ lọc và giá trị hiện tại.
- Dòng 6: Mục tiêu là điện 6 bước sau, tức 1 giờ tới.
- Dòng 7–8: Chia theo thời gian, không xáo trộn.
- Dòng 9–11: Hồi quy tuyến tính bằng bình phương nhỏ nhất.
- Dòng 14–16: So MAE khi không lọc và hai kiểu lọc.

**Kết quả:** Không lọc MAE 46,84 Wh. Centered giảm 27,7%, filtfilt 24,5%, đều giả; feature nhân quả chỉ giúp 0,9–5,9%.

## 211. Rò rỉ: backtest đẹp, dùng thật tệ
<!-- ma: ro-ri -->

*Tiếng Anh: data leakage · target encoding · fit on training data only*

**Dấu hiệu.** Rò rỉ tương lai hiếm khi báo lỗi; triệu chứng duy nhất là backtest đẹp còn dùng thật thì tệ.

**Kiểm.** Bài kiểm tự động `kiem_ro_ri` có ba bước:

1. Cắt dữ liệu tại một mốc.
2. Tính lại feature.
3. So từng dòng trước mốc.

Nếu giống hệt thì chưa thấy rò rỉ; nếu khác thì feature đã dùng tương lai. Trong hình, bản `shift(1)` rồi `rolling(7)` trùng
khít, còn bản `rolling(center=True)` lệch ngay trước mốc cắt.

**Ba kiểu rò rỉ qua cả chuỗi hay gặp:**

- Scaler tính trung bình và độ lệch chuẩn trên toàn bộ dữ liệu.
- Target encoding (thay nhóm bằng trung bình mục tiêu của nhóm) tính trên cả chuỗi.
- Nội suy dùng điểm phía sau.

Cách sửa chung: chỉ `fit` trên phần học.

Bài kiểm thứ hai là **kiểm nhiễu mục tiêu**: cộng nhiễu lớn vào mục tiêu từ 70% chuỗi trở đi, rồi xem feature của những dòng có thời điểm ra dự báo còn trước đó có đổi không. Nó bắt được lag nhỏ hơn tầm dự báo, thứ bài cắt tương lai bỏ sót. Chi tiết của `kiem_ro_ri`: so mọi dòng trước mốc, coi NaN khác số, chọn cả mốc cắt rơi vào lỗ dữ liệu. Kiểm xanh không chứng minh là sạch; nó chỉ không tìm thấy rò rỉ.

## 212. Code: ba kiểu rò rỉ cả chuỗi
<!-- ma: code-b13-ca-chuoi -->

Đặt bản sai cạnh bản đúng để thấy số tương lai lọt vào quá khứ ở đâu.

```python
import numpy as np
import pandas as pd

v = pd.Series([10, 12, 8, 14, 20, 16], index=range(1, 7), dtype=float)
nhom = pd.Series(["A", "B"] * 3, index=v.index)
co_lo = v.copy()
co_lo[3] = np.nan                                  # ngày 3 mất số
z_sai = (v - v.mean()) / v.std()                   # dùng cả 6 ngày
tb_dung = v.shift(1).expanding().mean()            # chỉ ngày trước t
nhom_sai = v.groupby(nhom).transform("mean")       # có số tương lai
nhom_dung = v.groupby(nhom).transform(
    lambda s: s.shift(1).expanding().mean())       # nhóm, chỉ quá khứ
dien_sai = co_lo.interpolate(limit_direction="both")  # nhìn ngày 4
dien_dung = co_lo.ffill()                          # lấy hôm trước
```

*Rút gọn từ buoi-13/tu-hoc.ipynb, phần 4.*

**Thư viện và hàm:**

- `shift(1).expanding().mean()` (pandas): Trung bình từ đầu chuỗi tới hôm qua, không chạm ngày t.
- `groupby(nhom).transform` (pandas): Tính theo từng nhóm rồi trả về đúng chỗ của mỗi dòng.
- `interpolate(limit_direction="both")` (pandas): Điền chỗ thiếu bằng đường nối hai phía, tức dùng cả ngày sau.

**Từng bước:**

- Dòng 4–7: Sáu ngày, hai nhóm, ngày 3 bị mất số.
- Dòng 8–9: Chuẩn hoá: toàn chuỗi so với chỉ quá khứ.
- Dòng 10–12: Trung bình nhóm: toàn chuỗi so với quá khứ.
- Dòng 13–14: Điền chỗ thiếu: hai phía so với lấy hôm trước.

**Kết quả:** Mọi ô z dùng trung bình 13,33 có cả hai ngày cuối. Ngày 1 mang trung bình nhóm A 12,67 có số 20 của ngày 5. Điền hai phía ra 13, ffill ra 12.

## 213. Code: bài kiểm cắt tương lai
<!-- ma: code-b13-kiem-ro-ri -->

Để máy tự tìm rò rỉ: cắt dữ liệu, tính lại feature, so từng dòng trước mốc.

```python
import numpy as np
def kiem_ro_ri(ham_feature, y, cac_moc=None, bo_cuoi=0):
    day_du, bi_bat = ham_feature(y), {}            # tính trên cả chuỗi
    cac_moc = cac_moc or [y.index[int(len(y) * p)]
                          for p in (0.5, 0.7, 0.9)]   # nhiều mốc
    for moc in cac_moc:
        cat = ham_feature(y[y.index <= moc])       # cắt rồi tính lại
        chung = day_du.index[day_du.index <= moc]
        chung = chung[:len(chung) - bo_cuoi]       # bo_cuoi=0: so MỌI dòng
        for cot in day_du.columns:
            a = day_du.loc[chung, cot].to_numpy(float)
            b = cat.reindex(chung)[cot].to_numpy(float)
            khac = ~np.isclose(a, b, rtol=0, atol=1e-9, equal_nan=True)
            if khac.any():
                bi_bat[cot] = max(bi_bat.get(cot, 0), int(khac.sum()))
    return bi_bat                                  # {feature: số dòng đổi}
```

*Rút gọn từ buoi-13/tu-hoc.ipynb, phần 5.*

**Thư viện và hàm:**

- `np.isclose(equal_nan=True)` (numpy): So hai mảng từng ô; NaN gặp NaN là bằng, NaN gặp số là khác.
- `reindex` (pandas): Xếp lại bảng theo danh sách mốc cho trước; mốc thiếu thành NaN.
- `kiem_ro_ri` (tự viết): Trả các cột bị đổi khi cắt tương lai, kèm số dòng đổi.

**Từng bước:**

- Dòng 3: Tính feature một lần trên dữ liệu đầy đủ.
- Dòng 4–5: Cắt ở 50, 70, 90% chuỗi, không chỉ một mốc.
- Dòng 7: Bỏ phần sau mốc rồi tính lại feature.
- Dòng 9: So mọi dòng trước mốc, không bỏ dòng cuối.
- Dòng 11–15: Cột nào đổi dù chỉ một dòng là rò rỉ.

**Kết quả:** Bản ẩu (một mốc, bỏ 10 dòng cuối) bắt 4 cột, lọt tb_7. Bản đúng bắt đủ 5 cột. Bộ 41 cột đã sửa qua sạch cả hai bài kiểm.

## 214. Học bằng nhiệt độ thật, chạy thật lại tệ hơn
<!-- ma: ngoai-sinh -->

*Tiếng Anh: exogenous variable · ex-ante vs ex-post · archived forecasts*

**Biến ngoại sinh** là biến từ bên ngoài chuỗi, ví dụ nhiệt độ khi dự báo tải điện. Lúc dự báo, ta chỉ có **bản dự báo**
nhiệt độ, không có nhiệt độ thật (khác biệt ex-ante và ex-post). Kết quả trong hình:

- Backtest dùng nhiệt độ thật hứa giảm sai số 3,85%.
- Chạy thật bằng dự báo trước 1 ngày còn giảm 3,10%.
- Chạy bằng dự báo trước 3 ngày thì sai số **tăng** 2,20%.

Quy tắc: huấn luyện bằng bản dự báo lưu trữ thì lúc chạy cũng dùng bản dự báo. Khi ghép bằng `merge_asof`, đặt `tolerance`
để không ghép nhầm số quá cũ.

Point-in-time còn có nghĩa là dùng đúng con số *lúc đó*: số liệu kinh tế hay bị sửa lại về sau (các bản vintage), và backtest phải dùng bản đã có tại gốc. Dự báo nhiệt độ trước 3 ngày kém tới mức huấn luyện bằng chính nó vẫn làm sai số tăng 2,92%, nên bỏ hẳn feature này.

## 215. Code: nhiệt độ thật hay dự báo
<!-- ma: code-b13-ngoai-sinh -->

Đo cái giá của rò rỉ: học bằng nhiệt độ thật, chạy bằng bản dự báo nhiệt độ.

```python
import pandas as pd

TAM = 24
d["muc_tieu"] = d["phu_tai"].shift(-TAM)            # tải của giờ t + 24
d["lag_24"], d["lag_168"] = d["phu_tai"], d["phu_tai"].shift(144)
for c in ("nhiet_do_that", "du_bao_1_ngay", "du_bao_3_ngay"):
    d[f"{c}_muc_tieu"] = d[c].shift(-TAM)           # nhiệt độ ở giờ đích
NEN = ["lag_24", "lag_168", "gio_sin", "gio_cos"]
ro_ri = mae(NEN + ["nhiet_do_that_muc_tieu"])       # backtest bằng sự thật
chay_that = mae(NEN + ["nhiet_do_that_muc_tieu"],   # học bằng thật,
                NEN + ["du_bao_3_ngay_muc_tieu"])   # chạy bằng dự báo

ghep = pd.merge_asof(trai, phai, left_index=True, right_index=True,
                     direction="backward",           # chỉ bản tin cũ hơn
                     tolerance=pd.Timedelta("3h"))   # quá 3 giờ: để trống
```

*Rút gọn từ buoi-13/tu-hoc.ipynb, phần 6.*

**Thư viện và hàm:**

- `shift(-24)` (pandas): Kéo giá trị 24 giờ sau về dòng hiện tại để làm đích dự báo.
- `pd.merge_asof` (pandas): Ghép mỗi dòng với dòng gần nhất của bảng kia, không cần trùng mốc.
- `mae` (tự viết): Hồi quy tuyến tính học 70% đầu, trả MAE trên 30% cuối.

**Từng bước:**

- Dòng 4: Đích là tải điện 24 giờ sau lúc dự báo.
- Dòng 6–7: Ba nguồn nhiệt độ cho đúng giờ cần dự báo.
- Dòng 9: Backtest bằng nhiệt độ thật: con số hứa hẹn.
- Dòng 10–11: Kịch bản hay gặp: học thật, chạy dự báo.
- Dòng 13–15: Ghép bản tin gần nhất trước đó, có hạn 3 giờ.

**Kết quả:** Nhiệt độ thật hứa giảm 3,85% sai số. Học bằng thật, chạy bằng dự báo trước 3 ngày thì sai số tăng 2,20%, tệ hơn không dùng nhiệt độ.

## 216. Phần C: Bảng tra & từ điển
<!-- ma: phan-c -->

Phần C gom 24 lỗi hay gặp vào ba bảng. Cách dùng: thấy dấu hiệu ở cột trái → chạy phép kiểm ở cột giữa → sửa theo cột phải.
Sau đó là mười chỗ người mới hay hiểu nhầm, và từ điển Việt – Anh 100 thuật ngữ để tra tài liệu tiếng Anh.

## 217. Bảng tra 1/3: thời gian, biểu đồ, biến đổi
<!-- ma: bang-tra-1 -->

Tám lỗi của buổi 3–6: múi giờ và đổi giờ, gộp tần suất, điều chỉnh lịch, biến đổi và đổi ngược, phân rã. "Data must be
positive" là lỗi Box-Cox khi gặp số 0 hay số âm. Khi đó dùng Yeo-Johnson, bản biến đổi nhận cả số 0 và số âm.

## 218. Bảng tra 2/3: dừng, tương quan, thiếu
<!-- ma: bang-tra-2 -->

Tám lỗi của buổi 7–10:

- Sai phân thừa, và ADF với KPSS cùng bác bỏ (thường do cú sốc hay đổi mức đột ngột).
- Tương quan giả, quan hệ chữ U.
- Bản đồ đặc trưng quên chuẩn hoá cột.
- Thiếu mốc.
- Cột số lưu dạng chữ (dấu hiệu: min lớn hơn max).
- Mã trá hình.

## 219. Bảng tra 3/3: ngoại lai, nhiễu, rò rỉ, đánh giá
<!-- ma: bang-tra-3 -->

Tám lỗi của buổi 10–15: lỗ dài bị lấp phẳng, masking, PELT trên mức gốc, aliasing, rò rỉ, MAPE với số 0, chia ngẫu nhiên, và
quên gap. **gap** là số bước bỏ trống giữa mốc cắt và đoạn dự báo khi dữ liệu về trễ. Ví dụ số liệu về trễ 1 ngày thì gap =
24 giờ.

## 220. Mười chỗ hay hiểu nhầm
<!-- ma: hay-nham -->

1. **Outlier là lỗi.** Tết là bất thường thật: giữ lại, ghi vào nhật ký sự kiện.
2. **Cắt COVID là an toàn.** Cắt còn 18 tháng cho MAPE 18,11%, tệ hơn hẳn nội suy (8,71%).
3. **Khoảng bootstrap = trung bình ± 1,96.** Bootstrap rút lại mẫu vài nghìn lần, tính trung bình mỗi lần, rồi lấy quantile
   0,025 và 0,975 của các trung bình đó. Dữ liệu tự tương quan thì rút cả khối liền nhau (block bootstrap).
4. **closed, label là hai dấu ngoặc.** Khi gộp, `closed` chọn mốc biên nào được tính vào khoảng; `label` chọn đặt tên khoảng
   bằng mốc đầu hay mốc cuối. Khoảng [9:00, 10:00) tên "9:00" chứa 9:00, không chứa 10:00.
5. **ADF nói dừng, KPSS nói không dừng → "dừng quanh xu hướng".** Sai: đó là **mâu thuẫn**. Hai kiểm định có giả thuyết
   ngược nhau. Khi mỗi bên thấy bằng chứng cho phía mình thì thường có cú sốc, đổi mức, hoặc độ dao động đổi. Vẽ chuỗi và
   thử đoạn không có cú sốc.
6. **MASE so được độ khó giữa các chuỗi.** MASE chia cho sai số naive của chính chuỗi đó, nên chuỗi khó thì mẫu số cũng lớn và
   độ khó bị triệt tiêu. MASE dùng để so mô hình trên cùng chuỗi. So độ khó giữa các chuỗi thì dùng sMAPE (chuỗi dương).
7. **CV cao = khó dự báo.** CV (độ lệch chuẩn chia trung bình) chỉ đo dao động. Chuỗi 10, 30, 10, 30 có CV 0,58 mà rất dễ
   đoán. Độ khó đo bằng sai số của baseline.
8. **Kiểm bộ lọc nhân quả = chia train/val.** Không phải: bài kiểm là đổi vài điểm cuối rồi chạy lại. Quá khứ không được đổi.
9. **MASE < 1 là thắng seasonal naive.** Mẫu số của MASE là sai số seasonal naive đo trên phần học. Kỳ chấm có thể khó hơn, nên
   muốn biết có thắng không thì phải chạy seasonal naive trên cùng kỳ chấm.
10. **Chỉ cần thắng seasonal naive.** Phải thắng cả bốn baseline. Trên M4 theo ngày, naive (0,835) và drift (0,810) còn thắng
    seasonal naive (1,077).

## 221. Từ điển Việt – Anh 1/5: nền móng, hiểu dữ liệu
<!-- ma: tu-dien-1 -->

Tên tiếng Anh dùng thống nhất theo Phụ lục E của khoá; tra tên tiếng Anh khi đọc tài liệu gốc (FPP, statsmodels, Nixtla).

| Tiếng Việt | English | Buổi |
|---|---|---|
| gốc dự báo, mốc cắt | forecast origin, cutoff | 1 |
| tầm dự báo h | forecast horizon | 1 |
| dự báo cuốn | rolling forecast | 1 |
| sai số ảo | in-sample error | 1 |
| quantile, trung vị | quantile, median | 2 |
| pinball loss | pinball / quantile loss | 2 |
| tỷ lệ phủ | coverage | 2 |
| block bootstrap | block bootstrap | 2 |
| giờ mùa hè | daylight saving time (DST) | 3 |
| timestamp naive / aware | naive / aware timestamp | 3 |
| định dạng dài / rộng | long / wide format | 3 |
| gộp tần suất | resample, aggregate | 3 |
| xu hướng | trend | 4 |
| mùa vụ, mùa vụ kép | seasonality, multiple seasonality | 4 |
| chu kỳ | cycle | 4 |
| tự tương quan | autocorrelation (ACF) | 4 |
| điều chỉnh lịch | calendar adjustment | 5 |
| giá thực / danh nghĩa | real / nominal value | 5 |
| hiệu chỉnh bias | bias adjustment (back-transform) | 5 |
| phân rã cộng / nhân | additive / multiplicative decomposition | 6 |

## 222. Từ điển Việt – Anh 2/5: dừng, làm sạch
<!-- ma: tu-dien-2 -->

| Tiếng Việt | English | Buổi |
|---|---|---|
| phần dư | residual, remainder | 6 |
| tự tương quan riêng | partial autocorrelation (PACF) | 7 |
| nhiễu trắng | white noise | 7 |
| tính dừng | stationarity | 7 |
| bước ngẫu nhiên | random walk | 7 |
| sai phân | differencing | 7 |
| kiểm định nghiệm đơn vị | unit root test (ADF, KPSS) | 7 |
| tương quan giả | spurious correlation | 8 |
| tương quan chéo | cross-correlation (CCF) | 8 |
| prewhitening | prewhitening | 8 |
| biến ngoại sinh | exogenous variable, covariate | 8 |
| đặc trưng chuỗi | time series feature | 9 |
| hệ số biến thiên | coefficient of variation (CV) | 9 |
| thiếu mốc / thiếu giá trị | missing timestamp / value | 10 |
| điền dữ liệu | imputation | 10 |
| mã trá hình | sentinel value | 10 |
| cột cờ | flag column | 10 |
| cảm biến đứng yên | stuck sensor | 10 |
| thiếu MCAR / MAR / MNAR | missing completely at random / at random / not at random | 10 |
| ngoại lai | outlier | 11 |

| Tiếng Việt | English | Buổi |
|---|---|---|
| phần dư | residual, remainder | 6 |
| tự tương quan riêng | partial autocorrelation (PACF) | 7 |
| nhiễu trắng | white noise | 7 |
| tính dừng | stationarity | 7 |
| bước ngẫu nhiên | random walk | 7 |
| sai phân | differencing | 7 |
| kiểm định nghiệm đơn vị | unit root test (ADF, KPSS) | 7 |
| tương quan giả | spurious correlation | 8 |
| tương quan chéo | cross-correlation (CCF) | 8 |
| prewhitening | prewhitening | 8 |
| biến ngoại sinh | exogenous variable, covariate | 8 |
| đặc trưng chuỗi | time series feature | 9 |
| hệ số biến thiên | coefficient of variation (CV) | 9 |
| thiếu mốc / thiếu giá trị | missing timestamp / value | 10 |
| điền dữ liệu | imputation | 10 |
| mã trá hình | sentinel value | 10 |
| cột cờ | flag column | 10 |
| cảm biến đứng yên | stuck sensor | 10 |
| thiếu MCAR / MAR / MNAR | missing completely at random / at random / not at random | 10 |
| ngoại lai | outlier | 11 |

## 223. Từ điển Việt – Anh 3/5: rò rỉ, đánh giá
<!-- ma: tu-dien-3 -->

| Tiếng Việt | English | Buổi |
|---|---|---|
| che khuất / gắn cờ oan | masking / swamping | 11 |
| độ lệch tuyệt đối trung vị | median absolute deviation (MAD) | 11 |
| điểm gãy | structural break, changepoint | 11 |
| nhật ký sự kiện, biến giả | event log, dummy variable | 11 |
| bộ lọc nhân quả | causal filter | 12 |
| tần số Nyquist | Nyquist frequency | 12 |
| rò rỉ tương lai | data leakage, look-ahead bias | 13 |
| feature trễ / cửa sổ trượt | lag / rolling feature | 13 |
| point-in-time | point-in-time | 13 |
| trong mẫu / ngoài mẫu | in-sample / out-of-sample | 14 |
| sai số tuyệt đối trung bình | mean absolute error (MAE) | 14 |
| căn sai số bình phương TB | root mean squared error (RMSE) | 14 |
| độ chệch | mean error (bias) | 14 |
| sai số có chia thang | scaled error (MASE, RMSSE) | 14 |
| backtest | backtest | 15 |
| rolling origin | rolling origin, time series cross-validation | 15 |
| cửa sổ mở rộng / trượt | expanding / sliding window | 15 |
| khoảng đệm | gap | 15 |
| tập giữ lại | hold-out set | 15 |
| kiểm định Diebold–Mariano | Diebold–Mariano test | 15 |

| Tiếng Việt | English | Buổi |
|---|---|---|
| che khuất / gắn cờ oan | masking / swamping | 11 |
| độ lệch tuyệt đối trung vị | median absolute deviation (MAD) | 11 |
| điểm gãy | structural break, changepoint | 11 |
| nhật ký sự kiện, biến giả | event log, dummy variable | 11 |
| bộ lọc nhân quả | causal filter | 12 |
| tần số Nyquist | Nyquist frequency | 12 |
| rò rỉ tương lai | data leakage, look-ahead bias | 13 |
| feature trễ / cửa sổ trượt | lag / rolling feature | 13 |
| point-in-time | point-in-time | 13 |
| trong mẫu / ngoài mẫu | in-sample / out-of-sample | 14 |
| sai số tuyệt đối trung bình | mean absolute error (MAE) | 14 |
| căn sai số bình phương TB | root mean squared error (RMSE) | 14 |
| độ chệch | mean error (bias) | 14 |
| sai số có chia thang | scaled error (MASE, RMSSE) | 14 |
| backtest | backtest | 15 |
| rolling origin | rolling origin, time series cross-validation | 15 |
| cửa sổ mở rộng / trượt | expanding / sliding window | 15 |
| khoảng đệm | gap | 15 |
| tập giữ lại | hold-out set | 15 |
| kiểm định Diebold–Mariano | Diebold–Mariano test | 15 |

## 224. Từ điển Việt – Anh 4/5: xác suất, biểu đồ, biến đổi
<!-- ma: tu-dien-4 -->

Các thuật ngữ nền về xác suất, biểu đồ và biến đổi, lấy từ bảng "Từ mới" của buổi 1–6.

| Tiếng Việt | English | Buổi |
|---|---|---|
| dự báo điểm / phân phối | point / probabilistic forecast | 1 |
| bài toán newsvendor | newsvendor problem | 1 |
| hàm phân phối tích luỹ | cumulative distribution function (CDF) | 1 |
| phân phối chuẩn | normal distribution | 2 |
| hệ số lệch / độ nhọn | skewness / kurtosis | 2, 9 |
| khoảng tin cậy | confidence interval | 2 |
| mức ý nghĩa α | significance level | 2 |
| định lý giới hạn trung tâm | central limit theorem (CLT) | 2 |
| tự hồi quy bậc một | autoregressive model AR(1) | 2, 7 |
| cỡ mẫu hiệu dụng | effective sample size | 2 |
| hạt giống ngẫu nhiên | random seed | 2 |
| chuỗi đều / không đều | regular / irregular time series | 3 |
| chu kỳ mùa vụ m | seasonal period | 4 |
| trục kép / trục y cắt | dual axis / truncated y-axis | 4 |
| thang log | log scale | 4 |
| năm gốc | base year (CPI) | 5 |
| trên đầu người | per capita | 5 |
| phân phối log-normal | log-normal distribution | 5 |
| trung bình trượt 2×m | 2×m moving average (2×m-MA) | 6 |
| độ mạnh mùa vụ | strength of seasonality F_S | 6 |

## 225. Từ điển Việt – Anh 5/5: tương quan, làm sạch, bộ lọc
<!-- ma: tu-dien-5 -->

Các thuật ngữ về tương quan, làm sạch và bộ lọc, lấy từ bảng "Từ mới" của buổi 8–15. Tên tiếng Anh thống nhất theo Phụ lục E của khoá.

| Tiếng Việt | English | Buổi |
|---|---|---|
| hồi quy đơn, R² | simple regression, R-squared | 8 |
| hoán vị theo khối | block permutation | 8 |
| biến gây nhiễu | confounder | 2, 8 |
| phân cụm Ward | Ward hierarchical clustering | 9 |
| nhu cầu gián đoạn | intermittent demand | 9, 19 |
| trần cảm biến | sensor ceiling / saturation | 10 |
| độ phân giải | measurement resolution | 10 |
| nội suy spline | spline interpolation | 10 |
| che nhân tạo | artificial masking | 10 |
| Kalman filter / smoother | Kalman filter / smoother | 10, 12 |
| winsorize | winsorizing | 11 |
| CUSUM, CROPS | CUSUM, CROPS (penalty scan) | 11 |
| hàm chi phí | cost function | 11 |
| tần số lấy mẫu | sampling frequency f_s | 12 |
| periodogram, Welch | periodogram, Welch method | 12 |
| wavelet | wavelet denoising | 12 |
| kiểm nhiễu mục tiêu | target-noise test | 13 |
| mã hoá target | target encoding | 13 |
| tự hiệp phương sai | autocovariance | 15 |
| phân phối t | Student's t-distribution | 15 |

## 226. Thư viện dùng trong 15 buổi
<!-- ma: thu-vien -->

Tám nhóm thư viện dùng trong 15 buổi đầu. **pandas** lo bảng dữ liệu theo thời gian, **NumPy** lo tính toán trên mảng số; hai thư viện này có mặt ở mọi buổi. **statsmodels** là thư viện thống kê: kiểm định, tự tương quan, phân rã. **SciPy** có phân phối xác suất (Box-Cox, tương quan) và bộ lọc tín hiệu (buổi 12). **scikit-learn** là thư viện học máy, ở đây dùng để chuẩn hoá, nén chiều bằng PCA và chia tập. **ruptures** tìm điểm gãy. **statsforecast** và **utilsforecast** của Nixtla chạy baseline, backtest và chỉ số nhanh cho hàng nghìn chuỗi. Nhiều hàm khoá tự viết (như `du_bao_cuon`, `kiem_ro_ri`) để thấy rõ từng bước trước khi dùng thư viện.

## 227. Lý thuyết nào, hàm nào
<!-- ma: ly-thuyet-ham -->

Bảng tra ngược: đang học lý thuyết nào thì tìm hàm và thư viện tương ứng ở đây, rồi mở slide code của buổi đó để xem cách dùng.

## 228. Phần D: Đánh giá trung thực
<!-- ma: phan-d -->

Mọi bước tiền xử lý đều phải trả lời một câu: dự báo có tốt hơn thật không. Phần D là cách đo trung thực: chẩn đoán phần dư,
chọn chỉ số, chia dữ liệu theo thời gian, backtest rolling origin, tách ba đoạn dữ liệu, và kiểm định Diebold–Mariano.

## 229. Phần dư sạch: không còn gì để khai thác
<!-- ma: phan-du -->

*Tiếng Anh: residual diagnostics · fitted values · Ljung–Box · Jarque–Bera*

**Phần dư** là sai số trên dữ liệu mô hình đã học; **sai số dự báo** là sai số trên kỳ chấm mô hình chưa thấy. Chỉ số chính xác luôn
tính trên kỳ chấm. Phần dư dùng để chẩn đoán. Phần dư "sạch" có bốn dấu hiệu:

1. Trung bình gần 0: không lệch một phía.
2. Không tự tương quan (ACF và Ljung-Box): không còn quy luật bị bỏ sót.
3. Phương sai ổn định: khoảng dự báo không sai độ rộng.
4. Gần hình chuông (kiểm bằng Jarque–Bera): khoảng tính theo phân phối chuẩn mới đúng.

Hình: phần dư của seasonal naive trên một chuỗi M4 tự tương quan mạnh (Ljung-Box p = 0,000) và có một cú rơi lớn. Vì vậy không nên tin
khoảng dự báo của baseline.

## 230. Code: chẩn đoán phần dư
<!-- ma: code-b14-phan-du -->

Kiểm xem phần dư còn quy luật không, để biết mô hình tốt hơn có chỗ để thắng.

```python
import numpy as np
from scipy import stats

def phan_du_mua_vu(y, m=7):
    return y[m:] - y[:-m]                          # thực tế trừ khớp

def ljung_box(e, so_tre=14):
    x = e - np.mean(e)
    r = np.array([np.dot(x[k:], x[:-k]) / np.dot(x, x)
                  for k in range(1, so_tre + 1)])   # ACF trễ 1 tới 14
    n = e.size
    q = n * (n + 2) * np.sum(r ** 2 / (n - np.arange(1, so_tre + 1)))
    return stats.chi2.sf(q, so_tre)                # p nhỏ: còn quy luật

e = phan_du_mua_vu(y)
p_jb = stats.jarque_bera(e).pvalue                 # có hình chuông không
```

*Rút gọn từ buoi-14/dap-an/danh_gia.py.*

**Thư viện và hàm:**

- `np.dot` (numpy): Nhân từng cặp rồi cộng lại: tử số và mẫu số của ACF.
- `stats.chi2.sf` (scipy): Xác suất gặp Q lớn cỡ này nếu phần dư chỉ là nhiễu: chính là p.
- `stats.jarque_bera` (scipy): Kiểm định phân phối có gần hình chuông; p nhỏ là không.

**Từng bước:**

- Dòng 4–5: Phần dư seasonal naive: y_t trừ y_(t−7).
- Dòng 8–10: Tự tương quan của phần dư ở 14 trễ.
- Dòng 11–12: Gộp 14 trễ thành một con số Q.
- Dòng 13: Đổi Q thành p: nhỏ là còn quy luật.
- Dòng 16: Kiểm phần dư có gần hình chuông không.

**Kết quả:** Trên 1.000 chuỗi M4: 99,8% còn tự tương quan (Ljung–Box p < 0,05), 92,5% không hình chuông, 46,4% phương sai đổi hơn 2 lần.

## 231. Mỗi chỉ số thưởng một kiểu dự báo
<!-- ma: chi-so -->

*Tiếng Anh: MAE · RMSE · mean error (bias)*

Ba chỉ số cơ bản, với **sai số = thực tế − dự báo**:

- **MAE**: trung bình của |sai số|.
- **RMSE**: căn của trung bình (sai số²), phạt nặng sai số lớn.
- **ME**: trung bình sai số có dấu. Dương là dự báo thấp có hệ thống.

Năm ngày thực tế 10, 12, 8, 14, 16 và dự báo 11, 10, 9, 14, 12 cho MAE 1,6, RMSE 2,10 và ME 0,8. Hình cho thấy trên phân
phối lệch phải, mỗi chỉ số tối ưu ở một chỗ khác nhau: MAE ra trung vị (20,0), RMSE ra trung bình (30,1), MAPE ra thấp hơn
cả hai (9,1). Chọn chỉ số là chọn dự báo, nên chọn theo quyết định thật.

Một lưu ý nữa: **phần dư** là sai số trên dữ liệu mô hình đã học, còn **sai số dự báo** là sai số trên kỳ chấm mô hình chưa
thấy. Đừng báo phần dư như sai số dự báo.

Đọc quy ước của thư viện trước khi dán số vào báo cáo: có thư viện ghi MAPE và sMAPE ở thang 0–1 (lệch 100 hoặc 200 lần), và `utilsforecast.bias` tính ME = dự báo − thực tế, ngược dấu với khoá.

## 232. Code: MAE, RMSE, ME
<!-- ma: code-b14-mae-rmse -->

Viết ba chỉ số rồi thấy mỗi chỉ số ưa một con số dự báo khác nhau.

```python
import numpy as np

def mae(y, d):
    return float(np.mean(np.abs(y - d)))           # ưa trung vị
def rmse(y, d):
    return float(np.sqrt(np.mean((y - d) ** 2)))   # ưa trung bình
def me(y, d):
    return float(np.mean(y - d))                   # dương: dự báo thấp

that = np.array([10, 12, 8, 14, 16.0])
du_bao = np.array([11, 10, 9, 14, 12.0])
mau = np.random.default_rng(0).lognormal(3.0, 0.9, 20000)  # lệch phải
luoi = np.linspace(mau.min(), np.quantile(mau, 0.999), 2000)
mae_theo = [np.mean(np.abs(mau - c)) for c in luoi]
rmse_theo = [np.sqrt(np.mean((mau - c) ** 2)) for c in luoi]
c_mae, c_rmse = luoi[np.argmin(mae_theo)], luoi[np.argmin(rmse_theo)]
```

*Rút gọn từ buoi-14/dap-an/danh_gia.py.*

**Thư viện và hàm:**

- `np.random.default_rng(0).lognormal` (numpy): Sinh số ngẫu nhiên lệch phải, có seed để chạy lại ra y hệt.
- `np.linspace` (numpy): Chia một khoảng thành 2.000 điểm cách đều để thử lần lượt.
- `np.argmin` (numpy): Vị trí phần tử nhỏ nhất: hằng số c cho chỉ số thấp nhất.

**Từng bước:**

- Dòng 3–8: Ba chỉ số, sai số là thực tế trừ dự báo.
- Dòng 10–11: Bảng năm ngày để tính tay đối chiếu.
- Dòng 12: 20.000 số lệch phải như doanh số, seed 0.
- Dòng 13–15: Thử 2.000 hằng số c, tính MAE và RMSE.
- Dòng 16: Tìm c cho mỗi chỉ số thấp nhất.

**Kết quả:** Năm ngày: MAE 1,6; RMSE 2,10; ME 0,8. Trên số lệch phải, MAE đáy ở 20,0 (trung vị), RMSE đáy ở 30,1 (trung bình).

## 233. Có số 0 thì MAPE hỏng
<!-- ma: phan-tram -->

*Tiếng Anh: MAPE · sMAPE · WAPE (weighted absolute percentage error)*

**MAPE** chia sai số cho thực tế, nên có hai điểm yếu:

- **Thực tế bằng 0** thì MAPE ra vô hạn.
- **Lệch không đối xứng**: thật 100, dự báo 150 cho 50%; thật 150, dự báo 100 chỉ cho 33,3%.

Hai chỉ số phần trăm khác vá từng chỗ:

- **sMAPE** chia |sai số| cho trung bình của |thực tế| và |dự báo|, nên bớt lệch một phía; vẫn hỏng khi cả hai bằng 0.
- **WAPE** = tổng |sai số| / tổng thực tế: chia một lần cho cả kỳ, nên sống được với vài ngày bằng 0 (trừ khi cả kỳ chấm toàn 0).

Thư viện `utilsforecast` trả MAPE và sMAPE ở thang 0–1: dán cạnh số phần trăm của M4 là lệch 100 và 200 lần. Thước đo không
chia cho thực tế, MASE, có slide riêng ngay sau slide code.

Hình: trên dữ liệu bán lẻ (75% ngày bằng 0), đổi chỉ số là đổi mô hình "tốt nhất", và MAPE không tính được. Dự báo toàn 0
có thể thắng MAE mà vô dụng cho việc nhập hàng.

Khi gộp nhiều chuỗi, nói rõ gộp bằng trung vị hay trung bình (vài chuỗi cực đoan kéo trung bình), và đếm, báo số chuỗi không tính được chỉ số, đừng âm thầm bỏ. Chọn chỉ số theo quyết định trước khi xem kết quả.

## 234. MAPE phạt dự báo cao nặng hơn dự báo thấp
<!-- ma: mape-lech -->

*Tiếng Anh: MAPE asymmetry · under-forecast bias · sMAPE*

**MAPE** chia từng sai số cho thực tế rồi lấy trung bình, ra phần trăm. Vì mẫu số là thực tế, hai lần lệch cùng 50 đơn vị bị phạt khác nhau:

| Thực tế | Dự báo | MAPE |
|---|---|---|
| 100 | 150 | 50% |
| 150 | 100 | 33,3% |

**Đọc bảng.** Hai dòng chỉ đổi chỗ thực tế và dự báo; dòng dự báo cao có thực tế nhỏ hơn nên bị chia cho số nhỏ hơn, phạt nặng hơn.

Lý do sâu hơn: dự báo thấp sai nhiều nhất là 100% (khi dự báo 0), còn dự báo cao thì sai bao nhiêu phần trăm cũng được. Tối ưu MAPE vì thế kéo
dự báo xuống dưới cả trung vị.

Hình dùng 20.000 số mô phỏng lệch phải như doanh số (seed 0). Ô phải có trục ngang là hằng số dự báo, trục dọc là chỉ số chia cho giá trị
nhỏ nhất của chính nó. Nhìn đáy ba đường: MAE đáy ở 20,0 (trung vị), RMSE ở 30,1 (trung bình), MAPE ở 9,1, thấp hơn cả hai.

**sMAPE** chia cho trung bình của thực tế và dự báo; nó mang tên "đối xứng" nhưng cũng không đối xứng (Hyndman & Koehler 2006). Chọn mô hình
hay đặt hàng theo MAPE là nghiêng về dự báo thấp; chuỗi có số 0 thì MAPE còn thành vô hạn. Khi đó dùng WAPE (tổng |sai số| / tổng thực tế)
hoặc chỉ số chia thang.

## 235. Code: MAPE, sMAPE, WAPE
<!-- ma: code-b14-phan-tram -->

Ba chỉ số phần trăm và cách mỗi cái xử lý ngày có thực tế bằng 0.

```python
import numpy as np

def mape(y, d):                                    # vô hạn khi có y = 0
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.abs((y - d) / y)
    return float(np.mean(v) * 100)

def smape(y, d):                                   # thang 0–200 kiểu M4
    mau = np.abs(y) + np.abs(d)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.where(mau == 0, 0.0, 2 * np.abs(y - d) / mau)
    return float(np.mean(v) * 100)

def wape(y, d):                                    # tổng chia tổng
    tong = float(np.sum(np.abs(y)))
    return float(np.sum(np.abs(y - d)) / tong * 100) if tong else np.nan
```

*Rút gọn từ buoi-14/dap-an/danh_gia.py.*

**Thư viện và hàm:**

- `np.errstate` (numpy): Tắt cảnh báo chia cho 0 trong khối with để tự xử lý kết quả.
- `np.where` (numpy): Chọn từng ô: mẫu bằng 0 thì lấy 0, còn lại lấy phép chia.
- `np.sum(np.abs(...))` (numpy): Cộng độ lớn sai số của mọi ngày thành một tổng.

**Từng bước:**

- Dòng 3–6: Chia từng sai số cho từng thực tế.
- Dòng 5: Có y = 0 thì ra vô hạn, không giấu đi.
- Dòng 8–12: Chia cho tổng thực tế và dự báo, nhân 200.
- Dòng 14–16: Tổng sai số chia tổng thực tế.

**Kết quả:** Bảng năm ngày: MAPE 12,8%, sMAPE 13,6, WAPE 13,3%. Thêm một ngày thực tế 0 thì MAPE thành vô hạn; trên 300 mã bán lẻ MAPE không tính được.

## 236. MASE: chia cho sai số baseline phần học
<!-- ma: mase -->

*Tiếng Anh: MASE (mean absolute scaled error) · RMSSE · in-sample scaling*

$$
\text{MASE} = \frac{\text{MAE}}{\frac{1}{T-m}\sum_{t=m+1}^{T} \lvert y_t - y_{t-m}\rvert}
$$

$T$ là số điểm phần học, $m$ là chu kỳ mùa vụ. Mẫu số là sai số quen thuộc của seasonal naive **trên phần học**, cố định trước khi
chấm, nên MASE không đơn vị và sống được với số 0. RMSSE làm tương tự với bình phương (cuộc thi M5).

Phần học 9, 11, 10, 12, 13 với $m$ = 1: bước nhảy 2, 1, 2, 1, trung bình 1,5. MAE kỳ chấm 1,6 → MASE = 1,6 / 1,5 ≈ 1,07.

Có hai chỗ hay nhầm. Lấy mẫu số trên đoạn đang chấm là sai định nghĩa và dùng thông tin tương lai: MASE của naive trên M4 ra 0,972 thay vì
0,835. Và MASE < 1 chưa chắc thắng seasonal naive trên kỳ chấm, vì kỳ chấm thường khó hơn phần học; muốn biết thì chạy baseline
trên cùng kỳ. Hình (buổi 9): vì mẫu số lớn lên theo độ khó của chính chuỗi, MASE của seasonal naive nằm ngang quanh 1 dù chuỗi dễ
hay khó, nên MASE so mô hình, không đo độ khó.

## 237. Code: MASE, RMSSE
<!-- ma: code-b14-mase -->

Chia sai số cho mức sai quen thuộc của baseline để so được giữa các chuỗi.

```python
import numpy as np

def _mau_so_scaled(hoc, m, binh_phuong=False):
    lech = hoc[m:] - hoc[:-m]              # seasonal naive TRÊN PHẦN HỌC
    if binh_phuong:
        return float(np.mean(lech ** 2))
    return float(np.mean(np.abs(lech)))

def mase(y, d, hoc, m=7):
    mau = _mau_so_scaled(hoc, m)
    return float("nan") if not mau else mae(y, d) / mau   # 0 thì NaN

def rmsse(y, d, hoc, m=7):
    mau = _mau_so_scaled(hoc, m, binh_phuong=True)
    return float("nan") if not mau else rmse(y, d) / np.sqrt(mau)
```

*Rút gọn từ buoi-14/dap-an/danh_gia.py.*

**Thư viện và hàm:**

- `hoc[m:] - hoc[:-m]` (numpy): Trừ mỗi điểm cho điểm cách m bước trước: sai số seasonal naive.
- `np.sqrt` (numpy): Căn bậc hai, đưa mẫu số bình phương về cùng đơn vị với RMSE.
- `mase, rmsse` (tự viết): Chia MAE hoặc RMSE cho sai số seasonal naive trên phần học.

**Từng bước:**

- Dòng 4: Sai số seasonal naive, chỉ trên phần học.
- Dòng 5–7: Trung bình bình phương hoặc trị tuyệt đối.
- Dòng 9–11: MAE kỳ chấm chia mẫu số của phần học.
- Dòng 11: Mẫu số bằng 0 thì trả NaN, không trả 0.
- Dòng 13–15: RMSSE làm y hệt với bình phương.

**Kết quả:** Ví dụ tay: MASE 1,6 / 1,5 ≈ 1,07, RMSSE ≈ 1,33. Lấy mẫu số trên đoạn chấm (code đầu buổi) thì MASE của naive trên M4 ra 0,972 thay vì 0,835.

## 238. Code: gộp, xếp hạng, đối chiếu
<!-- ma: code-b14-doi-hang -->

Gộp chỉ số qua nhiều chuỗi mà không giấu ô vô hạn, rồi soát thang của thư viện.

```python
import numpy as np
from utilsforecast.losses import smape as uf_smape
arr = np.array(v, dtype=float)                    # một số mỗi chuỗi
huu_han = arr[np.isfinite(arr)]                   # bỏ ô vô hạn, NaN...
so_vo_han = int(np.sum(~np.isfinite(arr)))        # ...nhưng đếm, báo ra
trung_vi, trung_binh = np.median(huu_han), np.mean(huu_han)

def xep_hang(bang, cac_cot):
    ra = bang[["mô hình"]].copy()
    for cot in cac_cot:                           # ME xếp theo trị tuyệt đối
        v = bang[cot].abs() if cot == "ME" else bang[cot]
        ra[cot] = v.rank(method="min").astype("Int64")
    return ra

tl = uf_smape(dai_kiem, models=["du_bao"])["du_bao"].mean()   # tỷ lệ 0–1
smape_m4 = tl * 200                               # về thang 0–200 của M4
```

*Rút gọn từ buoi-14/dap-an/danh_gia.py.*

**Thư viện và hàm:**

- `np.isfinite` (numpy): Đánh dấu ô là số bình thường, loại vô hạn và NaN.
- `rank(method="min")` (pandas): Đổi giá trị thành thứ hạng, 1 là nhỏ nhất; bằng nhau cùng hạng.
- `utilsforecast.losses.smape` (utilsforecast): Tính sMAPE trên bảng dạng dài; trả tỷ lệ 0–1, không phải phần trăm.

**Từng bước:**

- Dòng 3–5: Bỏ ô không tính được nhưng đếm để báo.
- Dòng 6: Gộp bằng trung vị và cả trung bình.
- Dòng 8–12: Xếp hạng mô hình theo từng chỉ số.
- Dòng 15–16: Thư viện trả tỷ lệ, nhân 200 mới ra M4.

**Kết quả:** Bán lẻ 300 mã: hạng nhất đổi theo chỉ số (naive theo MAE, seasonal naive theo sMAPE). sMAPE tự viết 3,59, utilsforecast 0,0179: lệch 200 lần.

## 239. Tám chỉ số: đo gì, ưa gì, hỏng khi nào
<!-- ma: bang-chi-so -->

| Chỉ số | Tính bằng lời | Ưa gì, dùng để làm gì | Hỏng hay lệch khi |
|---|---|---|---|
| ME | trung bình sai số, giữ dấu | đo độ chệch: dương là dự báo thấp | lệch lên, lệch xuống bù nhau |
| MAE | trung bình độ lớn sai số | ưa trung vị | so các chuỗi khác đơn vị |
| RMSE | căn của trung bình sai số bình phương | ưa trung bình; phạt nặng sai số lớn | vài sai số lớn chi phối; khác đơn vị |
| MAPE | trung bình \|sai số\| / thực tế × 100 | đọc bằng phần trăm | thực tế bằng 0; kéo dự báo xuống thấp |
| sMAPE | chia cho trung bình \|thực tế\| và \|dự báo\|, thang 0–200 | chỉ số của cuộc thi M4 | cả hai gần 0; vẫn không đối xứng |
| WAPE | tổng \|sai số\| / tổng thực tế | chuỗi có số 0; chuỗi lớn nặng hơn | tổng thực tế gần 0 |
| MASE | MAE chia MAE của seasonal naive trên phần học | so giữa các chuỗi, chịu được số 0 | phần học lặp hoàn hảo: mẫu số 0, trả NaN |
| RMSSE | như MASE, nhưng dùng bình phương | như MASE, ưa trung bình | như MASE |

Chọn chỉ số theo quyết định trước khi xem kết quả; đổi chỉ số là đổi hạng (buổi 14, mục 4.6).

## 240. Chia ngẫu nhiên là nhìn trộm tương lai
<!-- ma: chia-ngau-nhien -->

*Tiếng Anh: random split · K-fold · hold-out · rolling origin*

Học máy thông thường chia ngẫu nhiên dữ liệu thành tập học và tập kiểm. Với chuỗi thời gian, cách đó đặt điểm kiểm xen giữa
các điểm học (hàng trên của hình), tức là học trên cả tương lai của điểm đang kiểm. Hai cách đúng đều học trên quá khứ, kiểm
trên tương lai:

- **Hold-out**: một mốc cắt, kiểm một lần.
- **Rolling origin**: nhiều mốc cắt, mỗi lần học quá khứ rồi kiểm đoạn ngay sau.

## 241. Code: K-fold xáo trộn so với hold-out
<!-- ma: code-b15-kfold -->

Đo bằng số xem chia ngẫu nhiên hứa sai số thấp hơn thật bao nhiêu.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

moc = pd.Timestamp("2024-10-01")                  # hold-out: 3 tháng cuối
bang = bang_feature(y).assign(y=y).dropna()       # lag ≥ 24 giờ + lịch
hoc, kiem = bang[bang.index < moc], bang[bang.index >= moc]
X, t = hoc.drop(columns="y"), hoc["y"]
loi = []
for a, b in KFold(5, shuffle=True, random_state=0).split(X):  # XÁO TRỘN
    mo_hinh = tao_rung().fit(X.iloc[a], t.iloc[a])
    loi.append(_mae(mo_hinh.predict(X.iloc[b]), t.iloc[b]))
mae_kfold = float(np.mean(loi))
mo_hinh = tao_rung().fit(X, t)                    # học một lần trên quá khứ
mae_that = _mae(mo_hinh.predict(kiem.drop(columns="y")), kiem["y"])
```

*Rút gọn từ buoi-15/dap-an/backtest.py.*

**Thư viện và hàm:**

- `KFold(5, shuffle=True)` (sklearn): Xáo trộn rồi chia 5 phần, lần lượt lấy một phần làm kiểm.
- `tao_rung().fit / predict` (sklearn): Rừng ngẫu nhiên 200 cây: học trên phần học, rồi dự báo.
- `_mae` (tự viết): Trung bình độ lớn sai số giữa dự báo và thực tế, đơn vị MW.

**Từng bước:**

- Dòng 5: Để riêng 3 tháng cuối năm 2024 làm hold-out.
- Dòng 6–8: Feature lag ≥ 24 giờ, chỉ phần trước mốc.
- Dòng 10–13: K-fold xáo trộn: điểm kiểm xen giữa điểm học.
- Dòng 14–15: Học trên quá khứ, chấm trên 3 tháng sau.

**Kết quả:** Rừng ngẫu nhiên: K-fold hứa 1.639 MW, hold-out thật 2.129 MW, lệch −23,0%. Hồi quy tuyến tính lệch −11,8%.

## 242. K-fold xáo trộn hứa thấp hơn thật 23%
<!-- ma: kfold -->

*Tiếng Anh: K-fold cross-validation · hold-out set*

Trên tải điện EIA-930 với rừng ngẫu nhiên, ta so sai số mỗi cách hứa với sai số thật trên hold-out (đoạn tương lai chưa
dùng):

- **K-fold xáo trộn** hứa thấp hơn thật 23%.
- **Rolling origin** chỉ lệch 9%.

Rolling origin không tiên tri: nó chỉ đúng khi giai đoạn backtest giống tương lai. Vì vậy chọn cách backtest giống hệt cách
chạy thật: cùng tầm, cùng bước, cùng độ trễ dữ liệu.

K-fold không phải lúc nào cũng sai. Bergmeir, Hyndman và Koo (2018) chứng minh: nếu mô hình chỉ dùng lag làm đầu vào và phần dư không còn tự tương quan, K-fold cho ước lượng dùng được. Mô hình càng giỏi nhớ (như rừng ngẫu nhiên) thì K-fold càng lạc quan.

## 243. Rolling origin: backtest như chạy thật
<!-- ma: rolling-origin -->

*Tiếng Anh: rolling origin · cutoff · expanding / sliding window · gap*

**Rolling origin** đặt nhiều mốc cắt (**cutoff**) trong quá khứ. Ở mỗi cutoff, học trên quá khứ rồi dự báo đoạn ngay sau.
Có hai kiểu cửa sổ học:

- **Expanding**: học trên toàn bộ quá khứ.
- **Sliding**: chỉ học L bước gần nhất.

Hình trái cho thấy sai số từng cửa sổ dao động mạnh: 28 cửa sổ 24 giờ, mỗi cửa sổ là một lần may rủi. Vì vậy phải báo cả
phân bố sai số, không chỉ một con số trung bình. Hình phải: sai số tăng theo tầm h. Nếu tầm thật là 24 giờ thì chỉ nhìn sai
số của 24 giờ đầu.

Mọi bước tiền xử lý có học từ dữ liệu phải làm lại bên trong từng cutoff.

Tính cutoff bằng tay: cutoff cuối = n − 1 − gap − h, rồi lùi đều theo bước `buoc`. Ví dụ 30 mốc (0 tới 29), h = 4, gap = 2, 3 cửa sổ, buoc = 4: cutoff là 23, 19, 15; cửa sổ cuối học tới 23, bỏ trống 24 và 25, dự báo 26 tới 29. Đặt buoc = h: nếu các cửa sổ cách nhau đúng 7 ngày thì cửa sổ nào cũng rơi cùng một thứ trong tuần.

## 244. Code: bộ backtest rolling origin
<!-- ma: code-b15-rolling-origin -->

Tự viết bộ backtest: nhiều cutoff, mỗi lần chỉ học trên quá khứ rồi dự báo.

```python
import numpy as np
import pandas as pd
def chia_cua_so(df, h, so_cua_so, buoc=None, gap=0):
    buoc = h if buoc is None else buoc
    truc = np.sort(df["ds"].unique())
    cuoi = len(truc) - 1 - gap - h              # cutoff cửa sổ cuối
    return [(truc[c], truc[c + gap + 1], truc[c + gap + h])
            for c in range(cuoi - buoc * (so_cua_so - 1), cuoi + 1, buoc)]
def backtest(df, ham_du_bao, h, so_cua_so, buoc=None, gap=0):
    ket_qua = []
    for cutoff, bd, kt in chia_cua_so(df, h, so_cua_so, buoc, gap):
        lich_su = df[df["ds"] <= cutoff]        # KHÔNG thấy đoạn kiểm
        test = df[(df["ds"] >= bd) & (df["ds"] <= kt)]
        du_bao = ham_du_bao(lich_su.copy(), test[["unique_id", "ds"]])
        ket_qua.append(test.merge(du_bao, on=["unique_id", "ds"]))
    return pd.concat(ket_qua)
```

*Rút gọn từ buoi-15/dap-an/backtest.py.*

**Thư viện và hàm:**

- `np.sort(df["ds"].unique())` (numpy, pandas): Lấy các mốc thời gian khác nhau, xếp tăng dần làm trục.
- `merge` (pandas): Ghép dự báo với thực tế theo cặp mã chuỗi và mốc thời gian.
- `cross_validation` (statsforecast): Bản thư viện làm cùng việc nhưng không có gap.

**Từng bước:**

- Dòng 6: Cửa sổ cuối kết thúc đúng ở mốc cuối.
- Dòng 7–8: Lùi đều từng buoc; gap bỏ trống sau cutoff.
- Dòng 12: Hàm dự báo chỉ nhận dòng tới cutoff.
- Dòng 13–14: Dự báo đúng các mốc của đoạn kiểm.
- Dòng 15: Ghép dự báo với thực tế để chấm.

**Kết quả:** Tải ERCOT, 28 cửa sổ 24 giờ: rừng ngẫu nhiên 1.944 MW so với hold-out 2.129 MW (−8,7%). Seasonal naive khớp statsforecast, chênh 0,0.

## 245. Cửa sổ học: expanding, sliding, gap
<!-- ma: cua-so -->

*Tiếng Anh: expanding window · sliding window · gap · refit*

Rolling origin có bốn lựa chọn phải khớp với cách mô hình chạy thật:

- **Expanding**: ở mỗi cutoff, học trên toàn bộ quá khứ. Dùng khi quá khứ xa vẫn giống hiện tại.
- **Sliding**: chỉ học L bước gần nhất, ví dụ 90 ngày. Dùng khi quá khứ xa đã khác.
- **Gap**: số bước bỏ trống giữa cutoff và đoạn dự báo, bằng đúng độ trễ công bố dữ liệu. Số liệu điện về trễ 1 ngày thì gap = 24 giờ;
  quên gap là cho mô hình thấy số liệu chưa về.
- **Refit**: học lại mô hình ở mỗi cửa sổ. Mô hình nặng thì có thể refit mỗi vài cửa sổ để đỡ tốn thời gian.

Trong hình, mỗi hàng là một cutoff: phần xám là dữ liệu được học (dài dần, tức expanding), ô xanh là đoạn được dự báo và chấm.

## 246. Code: sai số theo cửa sổ và theo h
<!-- ma: code-b15-theo-cua-so -->

Tách một MAE gộp ra từng cửa sổ và từng bước h để thấy nó dao động cỡ nào.

```python
import numpy as np
import pandas as pd

def _mae(a, b):
    return float(np.mean(np.abs(np.asarray(a, float) - np.asarray(b, float))))

kq = backtest(dang_dai(y[y.index < moc]), ca_hai, h=24, so_cua_so=28,
              buoc=24)                            # rừng và seasonal naive
theo_cua_so = kq.groupby("cutoff").apply(lambda g: pd.Series({
    "rừng": _mae(g["y"], g["du_bao"]),
    "seasonal naive": _mae(g["y"], g["seasonal_naive"])}))
dao_dong = theo_cua_so.describe()                 # nhỏ nhất tới lớn nhất

def sai_so_theo_h(kq, cot):
    return (kq["y"] - kq[cot]).abs().groupby(kq["buoc_h"]).mean()
```

*Rút gọn từ buoi-15/dap-an/backtest.py.*

**Thư viện và hàm:**

- `groupby("cutoff").apply` (pandas): Chia kết quả theo từng cửa sổ rồi tính MAE riêng mỗi nhóm.
- `describe` (pandas): Tóm tắt nhanh: số lượng, trung bình, nhỏ nhất, phân vị, lớn nhất.
- `groupby(kq["buoc_h"]).mean()` (pandas): Trung bình sai số theo bước thứ mấy sau cutoff.

**Từng bước:**

- Dòng 7–8: 28 ngày, hai mô hình trên cùng cửa sổ.
- Dòng 9–11: Một MAE cho mỗi cửa sổ, mỗi mô hình.
- Dòng 12: Tóm độ dao động giữa các cửa sổ.
- Dòng 14–15: MAE theo từng bước sau cutoff.

**Kết quả:** MAE một ngày của rừng ngẫu nhiên đi từ 583 tới 4.328 MW, gấp bảy lần. Trên M4, seasonal naive 24 giờ nhảy lên từ bước 25.

## 247. Luyện, thi thử, thi thật: ba đoạn riêng
<!-- ma: ba-doan -->

*Tiếng Anh: train / validation / test · hold-out*

Ba loại đề:

- **Đề luyện** để tune tham số.
- **Đề thi thử** để chọn mô hình.
- **Đề thi thật** để báo cáo, chỉ mở một lần.

Học sinh luyện đúng đề thi thật thì điểm cao mà không biết gì thêm. Trong hình, chọn phương pháp và báo cáo trên cùng một
đoạn làm MASE trông tốt hơn thật 25%. Báo sai số của cái thắng trên chính đoạn đã chọn nó thì luôn lạc quan.

Chọn trên tập kiểm cũng là rò rỉ. Đã mở hold-out rồi quay lại chỉnh mô hình thì hold-out đó hết giá trị; cần một hold-out mới.

## 248. Code: tune, chọn, báo cáo ba đoạn
<!-- ma: code-b15-ba-tap -->

Tách ba đoạn riêng để con số báo cáo không được hưởng phần may lúc chọn.

```python
import numpy as np
import pandas as pd
LUOI_W = np.round(np.arange(0, 1.01, 0.1), 1)      # 11 giá trị w

def chon_va_bao_cao(chuoi, h=48):
    hang = []
    for ten, v in chuoi.items():
        n = len(v)
        T, A, B = n - 3 * h, n - 2 * h, n - h        # ba đoạn 48 giờ cuối
        w = min(LUOI_W, key=lambda x: _cham(v, T, x, h)["trộn"])  # tune
        diem_A = _cham(v, A, w, h)
        chon = min(diem_A, key=diem_A.get)           # chọn trên A
        diem_B = _cham(v, B, w, h)                   # báo cáo trên B
        hang.append({"chuỗi": ten, "chọn": chon,
                     "MASE báo cáo (B)": diem_B[chon]})
    return pd.DataFrame(hang)
```

*Rút gọn từ buoi-15/dap-an/backtest.py.*

**Thư viện và hàm:**

- `np.arange, np.round` (numpy): Tạo lưới 0; 0,1; …; 1 và làm tròn cho khỏi sai số lẻ.
- `_cham` (tự viết): MASE của sáu phương pháp đơn giản trên một đoạn 48 giờ.
- `pd.DataFrame` (pandas): Gom kết quả mỗi chuỗi thành một bảng để lấy trung vị.

**Từng bước:**

- Dòng 3: Lưới trọng số w từ 0 tới 1, bước 0,1.
- Dòng 9: Chia ba đoạn: T tune, A chọn, B báo cáo.
- Dòng 10: Chọn w cho MASE thấp nhất trên đoạn T.
- Dòng 11–12: Chọn phương pháp tốt nhất trên đoạn A.
- Dòng 13–15: Chỉ báo MASE trên đoạn B chưa dùng.

**Kết quả:** 414 chuỗi M4 theo giờ: tune, chọn, báo cáo cùng đoạn B cho MASE trung vị 0,775; ba đoạn riêng cho 1,039, lạc quan 25%.

## 249. Diebold–Mariano: chênh lệch có thật hay may rủi
<!-- ma: dm -->

*Tiếng Anh: Diebold–Mariano test · loss differential · HLN correction*

Hai mô hình chênh nhau vài phần trăm sai số: thật, hay chỉ may rủi? **Kiểm định Diebold–Mariano** chia chênh lệch sai số trung bình
cho sai số chuẩn của chính chênh lệch đó. Cần chú ý: với dự báo nhiều bước, chênh lệch từng giờ tự tương quan mạnh, và bỏ qua điều đó thì p
nhỏ giả tạo. Phải cộng tự hiệp phương sai tới trễ h − 1 và dùng bản hiệu chỉnh HLN với đúng h. Ví dụ trong buổi: p = 0,45, tức chưa
có bằng chứng mô hình nào hơn.

Con số của buổi 15: bản bỏ qua tự tương quan cho p = 0,0000012, bản HLN với h = 24 cho p = 0,16, tức chưa có bằng chứng. Và so 20 cặp mô hình thì trung bình có khoảng một cặp p < 0,05 chỉ do may.

## 250. Code: kiểm định Diebold–Mariano
<!-- ma: code-b15-dm -->

Hỏi chênh sai số giữa hai dự báo là thật hay chỉ là may trên đoạn này.

```python
import numpy as np
from scipy import stats

def diebold_mariano(e1, e2, h=1, hieu_chinh=True):
    d = np.abs(e1) - np.abs(e2)                    # chênh mất mát từng giờ
    n = len(d)
    lech = d - d.mean()
    gamma = [np.sum(lech[k:] * lech[: n - k]) / n for k in range(h)]
    v = (gamma[0] + 2 * sum(gamma[1:])) / n        # cộng tự hiệp phương sai
    if v <= 0:                                     # lùi về h = 1
        h, v = 1, gamma[0] / n
    s = d.mean() / np.sqrt(v)
    if not hieu_chinh:
        return s, 2 * stats.norm.sf(abs(s))        # bản bỏ tự tương quan
    s *= np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)   # sửa mẫu nhỏ
    return s, 2 * stats.t(df=n - 1).sf(abs(s))
```

*Rút gọn từ buoi-15/dap-an/backtest.py.*

**Thư viện và hàm:**

- `np.sum(lech[k:] * lech[: n - k])` (numpy): Tự hiệp phương sai trễ k: d_t và d_(t+k) cùng lên xuống cỡ nào.
- `stats.t(df=n - 1).sf` (scipy): Xác suất đuôi phân phối t; nhân 2 được p hai phía.
- `stats.norm.sf` (scipy): Xác suất đuôi của hình chuông chuẩn, dùng cho bản bỏ tự tương quan.

**Từng bước:**

- Dòng 5: Chênh độ lớn sai số của hai dự báo.
- Dòng 8–9: Cộng tự hiệp phương sai tới trễ h − 1.
- Dòng 12: Chênh trung bình chia sai số chuẩn.
- Dòng 13–14: Bản ngây thơ: so với hình chuông chuẩn.
- Dòng 15–16: Bản HLN: hệ số mẫu nhỏ, phân phối t.

**Kết quả:** Trộn so với seasonal naive trên 2.215 giờ: bỏ tự tương quan ra p = 0,0000012; bản HLN h = 24 ra −1,41, p = 0,16: chưa có bằng chứng.

## 251. Bảy kiểm định, một cách đọc
<!-- ma: doc-kiem-dinh -->

Mọi kiểm định trong khoá đi cùng bốn bước: đặt H0 (giả định ban đầu) → tính một con số từ dữ liệu → hỏi nếu H0 đúng thì
con số lệch cỡ này hiếm tới đâu (p) → p < 0,05 thì bác bỏ H0; p ≥ 0,05 chỉ là chưa đủ bằng chứng, không có nghĩa H0 đúng.

| Kiểm định | H0: giả định ban đầu | p < 0,05 nghĩa là | Buổi |
|---|---|---|---|
| hoán vị | hai nhóm như nhau | chênh lệch giữa hai nhóm có thật | 2, 8 |
| Ljung-Box | chuỗi, hay phần dư, là nhiễu trắng | còn quy luật chưa khai thác | 7, 14 |
| ADF | có random walk: không dừng | có bằng chứng chuỗi dừng | 7 |
| KPSS | chuỗi dừng | có bằng chứng chuỗi không dừng | 7 |
| Granger | quá khứ x không giúp dự báo y | quá khứ x giúp dự báo y, chưa phải "gây ra" | 8 |
| Jarque–Bera | phần dư có hình chuông | không hình chuông: khoảng theo phân phối chuẩn sai | 14 |
| Diebold–Mariano | hai mô hình chính xác như nhau | chênh lệch sai số có thật, không do may | 15 |

ADF và KPSS có H0 ngược nhau: đọc H0 trước khi đọc p.

## 252. Phần E: Quy trình tiền xử lý
<!-- ma: phan-e -->

Phần E ghép mọi thứ thành một quy trình. Câu hỏi phân loại mỗi bước: bước này có học gì từ dữ liệu không? Có thì phải làm
lại ở mỗi cutoff.

## 253. Quy trình tiền xử lý: ba tầng
<!-- ma: quy-trinh -->

*Tiếng Anh: preprocessing pipeline · point-in-time*

**Tầng 1, làm một lần trên toàn bộ dữ liệu.** Gồm các bước không học tham số nào:

1. Nạp dữ liệu và ép kiểu số.
2. Đưa về UTC.
3. Dựng lưới mốc đầy đủ, xử lý mốc trùng.
4. Đổi mã trá hình thành NaN kèm cột cờ.
5. Nhìn bộ biểu đồ chẩn đoán.
6. Ghi nhật ký sự kiện.
7. Điều chỉnh lịch và lạm phát.

**Tầng 2, làm lại ở mỗi cutoff, chỉ trên dữ liệu trước cutoff.** Gồm các bước có học từ dữ liệu: điền nhân quả, ngưỡng
ngoại lai, λ của Box-Cox, bộ lọc nhân quả, feature với lag ≥ h, scaler. Làm những bước này trên toàn bộ dữ liệu rồi mới
backtest là đã để tương lai rò vào quá khứ.

**Tầng 3, kiểm.** Chạy rolling origin với gap bằng độ trễ dữ liệu. Chấm bằng MASE hoặc WAPE trên chuỗi gốc, so với seasonal
naive. Cuối cùng chạy bài kiểm rò rỉ tự động.

## 254. Ba nguyên tắc cho mọi bước
<!-- ma: nguyen-tac -->

1. **Chỉ dùng thông tin có trước cutoff.** Áp cho feature, cho giá trị điền, cho tham số biến đổi, và cho biến ngoại sinh
   (dùng bản dự báo lưu trữ).
2. **Giữ dữ liệu gốc, gắn cờ thay vì xoá.** Xoá làm thủng lưới thời gian và mất dấu vết. Cột cờ cho biết chỗ nào đã sửa.
3. **Phải thắng các baseline trên backtest, luôn có seasonal naive.** Bước tiền xử lý nào không làm sai số trung thực tốt lên thì bỏ.

## 255. Phần F: Dữ liệu & phía trước
<!-- ma: phan-f -->

Dữ liệu trong khoá là dữ liệu thật, bẩn thật, có giấy phép mở đã xác minh. Phần này còn có bảng tra mỗi buổi nằm ở
slide nào, và phần tiền xử lý các buổi sau sẽ dạy.

## 256. 14 bộ dữ liệu thật, mỗi bộ bẩn một kiểu
<!-- ma: du-lieu -->

Mỗi bộ được chọn vì nó dạy một kiểu bẩn:

- Giá trị thiếu ghi là "?" (điện hộ gia đình).
- Giờ naive quanh ngày đổi giờ (taxi New York).
- Ô "(S)" trong Excel và định nghĩa đổi từ 4/2025 (Census).
- Bảng cột đổi giữa năm (EIA-930).
- Mã 9,999 và cờ chất lượng (trạm Nội Bài).
- Đỉnh Tết theo lịch âm (Wikipedia).
- Gãy do COVID (Eurostat).
- Nhiều số 0 (bán lẻ trực tuyến).

Mọi bộ đều có giấy phép đã xác minh và được tải về kèm kiểm sha256 (dấu vân tay của tệp). Khoá không dùng FRED vì điều
khoản cấm dùng cho machine learning; chuỗi kinh tế lấy từ cơ quan gốc (BLS, BEA, Census, Fed).

## 257. Tra theo buổi: mỗi buổi ở slide nào
<!-- ma: tra-theo-buoi -->

Bảng cho biết mỗi buổi được tóm ở những slide nào; script kiểm để mọi mục lý thuyết 4.x của buổi 1–15 đều có ít nhất một slide. Muốn
ôn một buổi, mở các slide đó cùng mục tương ứng trong bài đọc này, rồi đọc tài liệu gốc của buổi.

## 258. Tiền xử lý còn tiếp, theo từng bài toán
<!-- ma: phia-truoc -->

Buổi 1–15 cho quy trình chung. Các buổi sau thêm phần riêng cho từng loại bài toán:

| Buổi | Tiền xử lý thêm |
|---|---|
| 19 | Chuỗi thưa, nhiều số 0 |
| 20 | Dữ liệu khác tần suất, số liệu bị sửa lại |
| 22 | Biến chuỗi thành bảng hồi quy, chuẩn hoá theo từng chuỗi |
| 24 | Chuỗi mới chưa có lịch sử (cold start) |
| 28 | Gộp theo cấp bậc: cửa hàng → vùng → toàn công ty |
| 29 | Cửa sổ và chuẩn hoá cho deep learning |
| 41 | Pipeline point-in-time chạy lại ra đúng kết quả |
| 43 | Giám sát dữ liệu mới: đổi đơn vị, drift |

## 259. Năm điều mang về
<!-- ma: tong-ket -->

1. Nhìn trước, xử lý sau.
2. NaN (không biết) không phải 0 (đo được, bằng không): gắn cờ, đừng xoá.
3. Mọi mốc thời gian về UTC, trên lưới đầy đủ.
4. Chỉ dùng thông tin có trước cutoff.
5. Mọi mô hình và mọi bước tiền xử lý phải thắng các baseline (luôn có seasonal naive) trên rolling origin.
