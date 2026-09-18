# Buổi 1 — Forecasting là gì

## 1. Mục tiêu

Sau buổi này bạn:

- Viết được **phiếu bài toán dự báo** 6 ô cho một tình huống lạ trong 15 phút.
- Phân biệt dự báo với mục tiêu và kế hoạch; nêu bốn yếu tố quyết định một thứ dự báo được tới đâu.
- Chỉ ra bằng số vì sao chấm dự báo trên chính dữ liệu đã dùng để làm nó cho **sai số ảo**, tức đẹp hơn thật.
- Chỉ ra vì sao thiếu **baseline** (cách dự báo đơn giản để so) thì một con số sai số không nói lên gì.
- Giải thích vì sao khi thiếu và thừa đắt khác nhau, ta cần cả dải giá trị có thể xảy ra (**phân phối**), không chỉ
  một con số.

Sản phẩm: hàm đánh giá dự báo trung thực có đủ baseline (`code/danh_gia.py`) và mẫu phiếu bài toán
(`code/phieu-bai-toan.md`), dùng lại suốt khoá.

## 2. Nhắc lại buổi trước

Đây là buổi đầu tiên. Bạn cần sẵn bốn thứ:

- **Python cơ bản**: hàm, vòng `for`, list. Chưa quen thì đọc Phụ lục A trước khi làm lab.
- **pandas tối thiểu.** Một `Series` là một cột số, mỗi số gắn một mốc thời gian. `resample("D").sum()` gộp các giờ cùng
  ngày: ngày 1/1 có ba giờ 1, 2, 3 kWh thì gộp thành 1 + 2 + 3 = 6 kWh.
- **Trung bình, trị tuyệt đối.** Trung bình của 2, 4, 9 là 15/3 = 5. Trị tuyệt đối bỏ dấu âm: $\lvert -3 \rvert = 3$.
- **Ký hiệu.** $y_t$ là giá trị ở thời điểm $t$: chuỗi 5, 7, 6 có $y_1 = 5$, $y_3 = 6$. Dấu $\sum$ nghĩa là "cộng tất
  cả lại": $\sum_{t=1}^{3} y_t = 5 + 7 + 6 = 18$.

## 3. Trạng thái đầu buổi

Sau `cd lab && make up`:

| Hạng mục | Trạng thái |
|---|---|
| Dữ liệu | `du-lieu/raw/uci-household-power/household_power_consumption.txt` — 2.075.259 phút, 16/12/2006 17:24 → 26/11/2010 21:02, 133 MB, sha256 `4259c9d7ece5` |
| Nguồn | Hebrail & Berard, UCI Machine Learning Repository, CC BY 4.0 (`NGUON.txt`) |
| Môi trường | Python 3.12; numpy 2.5.3, pandas 3.0.5, matplotlib 3.11.2 |
| `code/kiem_tra_moi_truong.py` | in phiên bản thư viện và kích thước tệp dữ liệu |
| `code/danh_gia.py` | đọc điện theo giờ, "mô hình" bảng lịch, bốn hàm baseline, `du_bao_cuon`, `danh_gia` |
| `code/phieu-bai-toan.md` | mẫu phiếu 6 ô, để trống |
| **Đang cố tình sai** | `danh_gia` báo một bảng chỉ có **một** dòng: bảng lịch MAE **0,380** kWh/giờ — trông rất tốt |
| `make check` lúc này | ĐỎ: 4/8 test hỏng |

- `make up` dựng môi trường của buổi: cài đúng phiên bản thư viện, tải dữ liệu, kiểm tệp.
- **sha256** là "dấu vân tay" tính từ nội dung tệp; sai một byte là chuỗi khác hẳn. Khớp nghĩa là bạn có đúng tệp tác
  giả dùng.
- `make check` chạy 8 test, mỗi test tự kiểm một điều. **Đỏ** là hỏng, **xanh** là qua. Đầu buổi đỏ là cố ý.

## 4. Lý thuyết

### Từ mới trong buổi

| Thuật ngữ | Nghĩa | Ví dụ |
|---|---|---|
| biến mục tiêu | Đại lượng cần dự báo (cột `y`). | kWh mỗi giờ của một hộ. |
| gốc dự báo, mốc cắt dữ liệu | Lúc ra dự báo; sau đó coi như chưa biết gì. | Gốc 00:00 thứ Hai. |
| tầm dự báo, $h$ | Dự báo xa bao nhiêu bước. | 7 ngày theo giờ: $h$ = 1…168. |
| độ chi tiết | Gộp dữ liệu tới mức nào. | Từng giờ, hay tổng tuần. |
| công suất (kW), điện năng (kWh) | Mạnh cỡ nào tại một lúc; tổng đã dùng = công suất × giờ. | 2 kW trong nửa giờ = 1 kWh. |
| mùa vụ | Mẫu lặp lại đều theo lịch. | Ngày nào cũng cao lúc 20h. |
| dịch mức | Mức trung bình đổi hẳn rồi ở luôn đó. | Thêm người ở: 1,0 → 1,4 kWh/giờ. |
| mô hình, tham số, khớp | Cách tính ra dự báo; các con số bên trong nó; việc chọn các con số đó từ dữ liệu. | "Mai = trung bình 7 ngày qua". |
| baseline | Cách dự báo đơn giản làm mốc so. | Mô hình thua baseline thì bỏ. |
| naive, seasonal naive | Lấy số cuối đã biết; lấy số cùng lúc của vòng lặp trước. | 19h thứ Ba tuần trước. |
| sai số dự báo | Thực tế − dự báo, trên dữ liệu mô hình chưa thấy. | 1,7 − 1,5 = +0,2. |
| MAE (mean absolute error) | Trung bình độ lớn sai số, bỏ dấu. | +2 và −4 → 3. |
| phần dư | "Sai số" đo trên chính dữ liệu đã dùng để khớp. | Khớp 2010, đo 2010. |
| dự báo cuốn | Dự báo lặp lại, mỗi lần dời gốc tới. | Mỗi thứ Hai một lần. |
| phân phối | Các giá trị có thể xảy ra, mỗi giá trị hay gặp tới đâu. | 10 ngày: 5, 6, 6, 7, …, 12. |
| quantile, trung vị | Quantile 0,8: giá trị nhỏ nhất mà ít nhất 80% giá trị không vượt quá. Trung vị là quantile 0,5. | Mục 4.6. |
| dự báo điểm, dự báo phân phối | Một con số; cả dải giá trị kèm khả năng. | "120 cái" / "100–140: 80%". |
| bài toán newsvendor | Đặt hàng một lần khi thiếu và thừa đều mất tiền. | Người bán báo. |
| hàm phân phối tích luỹ | Tỷ lệ giá trị nhỏ hơn hoặc bằng một mốc. | Chỉ ở hộp Nâng cao. |
| sai số ảo | Sai số đo trên chính dữ liệu đã dùng để làm dự báo — đẹp hơn sai số thật. | Học thuộc đề cũ rồi thi lại đúng đề đó: 10 điểm; đề mới chỉ 6. |
| thị trường kỳ hạn, giá giao ngay | Kỳ hạn: mua trước, chốt giá sớm. Giao ngay: mua lúc cần, đắt hơn khi thiếu gấp. | Chủ nhật mua điện cho cả tuần; thứ Ba thiếu thì mua giao ngay. |

Chỉ cần đọc lướt. Mỗi từ được giải thích lại, có ví dụ, ở chỗ nó xuất hiện lần đầu.

### 4.1 Dự báo là gì, và cái gì dự báo được

**Vấn đề.** Con số ta sắp đưa ra là điều *sẽ* xảy ra, hay điều ta *muốn* xảy ra? Và thứ này dự báo được tới đâu?

**Trực giác.** Bản tin nói "mai mưa 80%". Bạn muốn mai nắng, nhưng không ai sửa bản tin vì thế. Mang ô là **kế
hoạch**: việc làm khi biết cả dự báo lẫn mong muốn. Sách *Forecasting: Principles and Practice* (viết tắt FPP, của
Hyndman và Athanasopoulos, đọc miễn phí trên mạng) tách ba thứ (FPP §1.2):

| | Trả lời câu hỏi | Ví dụ với chuỗi quán cà phê |
|---|---|---|
| **Dự báo** | điều gì *sẽ* xảy ra, với mọi thông tin đang có | tuần tới bán khoảng 1.900 ly (số giả định) |
| **Mục tiêu** | ta *muốn* điều gì | bán 2.500 ly |
| **Kế hoạch** | ta *làm gì* để tiến gần mục tiêu | chạy khuyến mãi, đặt thêm hạt |

**Ví dụ số nhỏ — tự tính tay.** Sếp muốn 2.500 ly nên bảo "dự báo 2.500". Kho đặt nguyên liệu cho 2.500 ly, tuần đó
bán 1.900 ly. Nguyên liệu thừa cho 2.500 − 1.900 = 600 ly. Và không ai còn biết mô hình dự báo đúng hay sai.

**Cái gì dự báo được.** FPP §1.1 nêu bốn yếu tố; thoả càng nhiều thì càng dự báo chính xác được.

| Yếu tố | Điện của một hộ, ngày mai | Tỷ giá, tuần sau |
|---|---|---|
| 1. Hiểu điều gì tác động tới nó | có: giờ giấc, thời tiết, ngày nghỉ | ít |
| 2. Có nhiều dữ liệu | có: 4 năm, từng phút | có |
| 3. Tương lai giống quá khứ | thường có | khủng hoảng làm đổi hẳn |
| 4. Dự báo **không** làm đổi chính nó | đúng: hộ không đọc dự báo | sai: nhà đầu tư mua bán theo dự báo |

**Đọc bảng.** Điện ngày mai thoả cả bốn, tỷ giá chỉ thoả yếu tố 2. FPP kết luận nhu cầu điện ngắn hạn có thể dự báo
rất chính xác, còn tỷ giá thì không. Bốn câu này cho biết trước nên kỳ vọng độ chính xác tới đâu.

**Dữ liệu thật.** Lab dùng điện của **một hộ** ở Sceaux, gần Paris, đo từng phút từ 12/2006 tới 11/2010. Một hộ vẫn khó
hơn cả thành phố: từng giờ lên xuống theo việc bật tắt máy móc (mục 4.5).

**Tóm lại.** **Dự báo là điều sẽ xảy ra, không phải điều ta muốn; đừng sửa nó cho khớp mục tiêu. Bốn yếu tố cho biết
một thứ dự báo được tới đâu.**

**Tự kiểm tra.** Hãng xe công bố "giá tháng sau tăng 10%", khách đổ xô mua trước. Yếu tố nào bị vi phạm?

<details>
<summary>Đáp án</summary>

Yếu tố 4: chính lời dự báo làm đổi thứ được dự báo. Nhầm hay gặp là chọn yếu tố 3. Tương lai đúng là khác quá khứ,
nhưng nguyên nhân là chính lời dự báo.

</details>

### 4.2 Phiếu bài toán dự báo — 6 ô

**Vấn đề.** Cùng dữ liệu điện, "dự báo cho ai, để làm gì" đổi thì cách làm và cách chấm đổi theo. FPP §1.6 gọi bước
định nghĩa bài toán là bước thường khó nhất.

**Trực giác.** Thợ may hỏi số đo trước khi cắt vải. Phiếu 6 ô là "số đo" của bài toán, điền trước khi mở dữ liệu.

| Ô | Câu hỏi | Ví dụ: công ty bán lẻ điện mua trước điện cho một khu dân cư |
|---|---|---|
| 1. Quyết định | Ai dùng dự báo làm gì, bao lâu một lần? | Cuối ngày Chủ nhật (sau 23:59) đặt mua điện theo giờ cho 7 ngày tới trên thị trường kỳ hạn, mỗi tuần một lần |
| 2. Biến mục tiêu | Đo cái gì, đơn vị nào? | kWh mỗi giờ của khu (ở lab: một hộ) |
| 3. Tầm dự báo | Xa bao nhiêu bước? | 1–168 giờ, từ 00:00 thứ Hai |
| 4. Độ chi tiết | Gộp tới mức nào? Chấm ở mức nào? | theo giờ, cả khu |
| 5. Mốc cắt dữ liệu | Lúc ra dự báo đã biết gì? | số đo tới 23:59 Chủ nhật; thời tiết *dự báo*, chưa có thời tiết thật |
| 6. Chi phí sai hai chiều | Thiếu mất gì? Thừa mất gì? | mỗi kWh thiếu phải mua gấp giá giao ngay, mất khoảng 4 đồng; mỗi kWh thừa bán lại lỗ khoảng 1 đồng |

**Thị trường kỳ hạn** là nơi mua điện trước, chốt giá hôm nay cho điện giao tuần sau. **Giá giao ngay** là giá mua ngay
lúc cần, thường đắt hơn nhiều.

**Đọc bảng.** Ô 3 và ô 5 quyết định baseline nào được dùng (mục 4.3). Ô 4 quyết định chấm ở mức nào (mục 4.5). Ô 6
quyết định nên báo con số nào (mục 4.6).

**Ví dụ số nhỏ — tự tính tay: đơn vị ở ô 2.** Dữ liệu gốc ghi **công suất** (kW) trung bình từng phút; ta cần **điện
năng** (kWh) từng giờ. Giả sử 30 phút đầu nhà dùng 2,0 kW, 30 phút sau 0,4 kW.

- Điện năng = 2,0 × 0,5 giờ + 0,4 × 0,5 giờ = 1,0 + 0,2 = 1,2 kWh.
- Trung bình công suất trong giờ = (2,0 + 0,4)/2 = 1,2 kW.

Hai số bằng nhau, vì trung bình kW nhân đúng 1 giờ thì ra kWh. Vậy **trung bình kW trong một giờ là số kWh của giờ
đó**. Code làm đúng vậy với 60 phút.

Một giờ **đủ số đo** khi có ít nhất một nửa số phút đo được; không đủ thì để trống (`NaN`). Chuỗi được cắt từ 00:00 ngày 17/12/2006
(ngày đầu có đủ 24 giờ) tới 23:00 Chủ nhật 21/11/2010 (tuần đủ cuối cùng), nên có 34.464 giờ, trong đó 431 giờ trống.

**Dữ liệu thật: vẽ trước khi làm.** FPP khuyên luôn bắt đầu bằng việc vẽ dữ liệu.

![Điện tiêu thụ theo ngày của một hộ](hinh/mot-duong.png)

**Cách đọc hình.**

1. **Trục ngang**: ngày, 12/2006–11/2010.
2. **Trục dọc**: điện dùng trong ngày (kWh/ngày).
3. **Ký hiệu**: xám là từng ngày; xanh là trung bình 28 ngày quanh đó; dải cam nhạt là tháng 8.
4. **Nhìn vào đâu**: đường xanh cao mùa đông, thấp mùa hè; dải cam năm nào cũng là đáy. Tháng 8/2008 thấp nhất
   (4–6 kWh mỗi ngày, nhà vắng người).
5. **Kết luận**: mùa đông cao, tháng 8 gần như vắng nhà, năm sau giống năm trước.

Trong ngày cũng có nhịp: thấp nhất lúc 4h, cao nhất lúc 20h; cuối tuần dùng nhiều hơn ngày thường. Mẫu lặp lại đều như
vậy gọi là **mùa vụ**; chuỗi này có mùa vụ theo ngày, tuần và năm. Năm câu hỏi nên viết ra trước khi làm mô hình:

1. **Giờ trống nằm ở đâu?** Có 10 ngày không có giờ nào đủ số đo, ví dụ 18–21/8/2010.
2. **Kỳ nghỉ tháng 8 có lặp lại đúng ngày mỗi năm không?** Có thì mô hình "nhớ lịch" sẽ có lợi.
3. **Đơn vị là gì?** kW trung bình mỗi phút; trung bình trong giờ là kWh (ví dụ trên).
4. **Mốc thời gian là giờ địa phương hay UTC?** UTC là giờ chuẩn quốc tế; giờ Pháp lệch nó 1–2 giờ tuỳ mùa (buổi 3).
5. **Có dịch mức không?** Tức mức trung bình đổi hẳn rồi ở luôn đó, ví dụ nhà có thêm người.

**Tóm lại.** **Điền 6 ô trước khi mở dữ liệu, rồi vẽ và viết câu hỏi. Ô 3–6 quyết định baseline, mức chấm và con số
cần báo.**

**Tự kiểm tra.** Máy lạnh 1,5 kW chạy 40 phút rồi tắt 20 phút. Giờ đó dùng bao nhiêu kWh?

<details>
<summary>Đáp án</summary>

1,5 × 40/60 + 0 × 20/60 = 1,0 kWh, bằng trung bình công suất trong giờ (1,0 kW). Nhầm hay gặp là trả lời 1,5 kWh,
quên rằng máy chỉ chạy 2/3 giờ.

</details>

### 4.3 Baseline: chuẩn tối thiểu để so

**Vấn đề.** Code đầu buổi báo MAE 0,380 kWh/giờ. Tốt hay xấu? Một con số đứng một mình không trả lời được.

**Trực giác.** Bạn được 7 điểm: cả lớp được 9 thì 7 là kém, cả lớp được 4 thì 7 là giỏi. **Baseline** là "điểm của cả
lớp": một cách dự báo đơn giản ai cũng làm được. Vài phương pháp cực kỳ đơn giản lại hiệu quả bất ngờ, nên luôn dùng
làm mốc so (FPP §5.2).

**Ký hiệu thời gian — dùng suốt khoá.**

- $T$: giờ cuối cùng đã có số đo, ví dụ 23:00 Chủ nhật 3/1/2010.
- **Gốc dự báo**: lúc ra dự báo, ngay sau $T$ (00:00 thứ Hai 4/1). Từ gốc trở đi coi như chưa biết.
- $h$: số giờ tính từ $T$. $T + 1$ là 00:00 thứ Hai; $T + 6$ là 05:00 thứ Hai; $T + 168$ là 23:00 Chủ nhật 10/1.
- $y_T$: số đo ở giờ $T$. $\hat y_{T+h}$ ("y mũ") là số **dự báo** cho giờ $T + h$.

**Ví dụ số nhỏ — tự tính tay.** Dự báo 19:00 thứ Ba 5/1. Từ 23:00 Chủ nhật tới đó là 24 + 20 = 44 giờ, nên $h = 44$.
Số giả định: lúc $T$ nhà dùng 0,6 kWh; trung bình mọi giờ đã biết là 1,1 kWh; 19:00 thứ Ba của bốn tuần trước (xa tới
gần) là 1,6; 1,2; 1,4; 1,8. Thực tế hôm đó là 1,7 kWh.

| Baseline | Lấy số nào | Dự báo (kWh) | Sai số = thực tế − dự báo |
|---|---|---|---|
| giờ trước (naive) | giờ $T$ | 0,6 | 1,7 − 0,6 = +1,1 |
| trung bình | mọi giờ đã biết | 1,1 | +0,6 |
| tuần trước (seasonal naive) | 19:00 thứ Ba tuần trước | 1,8 | −0,1 |
| trung bình 4 tuần | (1,6 + 1,2 + 1,4 + 1,8)/4 | 1,5 | +0,2 |

**Đọc bảng.** Hai baseline "cùng giờ, cùng thứ" sai ít nhất, vì điện lặp lại theo tuần. "Giờ trước" sai nhiều nhất:
23:00 là giờ sắp ngủ, không giống 19:00. Sai số dương nghĩa là dự báo thấp hơn thực tế.

**Công thức** của bốn cách, theo đúng thứ tự trong bảng:

$$
\hat y_{T+h} = y_T, \qquad \hat y_{T+h} = \bar y, \qquad \hat y_{T+h} = y_{T+h-168}, \qquad
\hat y_{T+h} = \tfrac{1}{4}\sum_{k=1}^{4} y_{T+h-168k}
$$

- $\bar y$ ("y ngang"): trung bình mọi giờ từ giờ đầu tới giờ $T$.
- $y_{T+h-168}$: số đo 168 giờ (một tuần) trước giờ cần dự báo. Lùi lại một số bước như vậy gọi là **trễ**.
- $k$ = 1, 2, 3, 4: lùi 1 tới 4 tuần; $\sum$ cộng bốn số, $\tfrac14$ lấy trung bình.

**Nói bằng lời.** Với $h = 44$: $T + 44 - 168 = T - 124$, tức 19:00 thứ Ba 29/12/2009, số đo 1,8. Công thức cuối lấy
thêm ba tuần xa hơn rồi chia bốn, ra 1,5.

**Baseline nào hợp lệ.** Chỉ được dùng số đã có tại gốc, tức giờ $T$ trở về trước. Thử "cùng giờ hôm qua"
($y_{T+h-24}$) với $h = 100$:

- Giờ cần dự báo: $T + 100$, tức 03:00 thứ Sáu 8/1.
- Giờ baseline lấy số: $T + 100 - 24 = T + 76$, tức 03:00 thứ Năm 7/1.
- Vì $T + 76 > T$, giờ đó nằm *sau* gốc. Lúc đặt mua điện chưa có số đó. Dùng nó là gian lận, không phải baseline.

Quy tắc: trễ phải lớn hơn hoặc bằng tầm xa nhất, ở đây là một tuần.

**MAE: thước đo để so.** MAE (sai số tuyệt đối trung bình) là trung bình độ lệch, không kể dấu:

$$
\text{MAE} = \frac{1}{n}\sum_{t=1}^{n} \lvert y_t - \hat y_t \rvert
$$

- $y_t$: số đo thật ở giờ $t$; $\hat y_t$: số dự báo cho giờ đó; $y_t - \hat y_t$: sai số.
- $n$: số giờ được chấm. $\sum$ cộng $n$ trị tuyệt đối; $\frac1n$ lấy trung bình.

**Nói bằng lời.** Bốn giờ thật 1,5; 0,5; 2,0; 1,0 kWh, dự báo đều 1,0. Sai số +0,5; −0,5; +1,0; 0. Bỏ dấu rồi cộng:
0,5 + 0,5 + 1,0 + 0 = 2,0. Chia cho $n = 4$: MAE = 2,0/4 = 0,5, tức trung bình mỗi giờ lệch 0,5 kWh.

**Tự viết bằng NumPy** (đúng các số trên; `dap-an/vi_du_nho.py` in mọi số của mục này):

```python
import numpy as np
tuan = np.array([1.6, 1.2, 1.4, 1.8])      # 19:00 thứ Ba của 4 tuần trước, xa tới gần
print(tuan[-1], tuan.mean())               # 1.8 (tuần trước), 1.5 (trung bình 4 tuần)
y, du_bao = np.array([1.5, 0.5, 2.0, 1.0]), np.full(4, 1.0)
print(np.mean(np.abs(y - du_bao)))         # 0.5 — MAE
```

**Thư viện.** `code/danh_gia.py` có `du_bao_gio_truoc`, `du_bao_trung_binh`, `du_bao_tuan_truoc`,
`du_bao_trung_binh_4_tuan` và `mae` (bỏ qua giờ trống). Nếu 19:00 thứ Ba tuần trước trống, "tuần trước" không có gì để
lấy. Vì vậy `dien_bang_tuan_truoc` điền giờ trống bằng cùng giờ tuần trước nữa; nó chỉ nhìn về quá khứ nên không gian
lận.

**"Mô hình" hôm nay: bảng lịch.** Trung bình lượng điện theo từng bộ (tuần trong năm, thứ, giờ): 53 × 7 × 24 = 8.904 ô.
Mỗi ô là một **tham số** (con số bên trong mô hình). Tính các ô từ dữ liệu gọi là **khớp** mô hình. Nhiều ô giúp bảng
nhớ kỳ nghỉ tháng 8. Nhưng mỗi ô chỉ có vài giờ, nên bảng dễ **thuộc lòng**: nhớ cả những lần bật máy giặt ngẫu nhiên,
như học thuộc đáp án đề cũ.

**Tóm lại.** **Không có baseline thì MAE không nói lên gì. Baseline chỉ dùng số đã có tại gốc: trễ phải lớn hơn hoặc bằng
tầm. Với điện theo giờ, baseline tốt là "cùng giờ, cùng thứ" của các tuần trước.**

**Tự kiểm tra.** Tầm 168 giờ. "Cùng giờ hai ngày trước" ($y_{T+h-48}$) có hợp lệ không? Thử $h = 30$ và $h = 60$.

<details>
<summary>Đáp án</summary>

$h = 30$: $T - 18$, trước gốc, dùng được. $h = 60$: $T + 12$, sau gốc, không dùng được. Một baseline phải đúng cho mọi $h$
từ 1 tới 168, nên nó **không hợp lệ**. Nhầm hay gặp là chỉ thử một $h$ nhỏ rồi kết luận "được".

</details>

### 4.4 Sai số ảo và dự báo cuốn

**Vấn đề.** Code đầu buổi khớp bảng lịch trên **toàn bộ** chuỗi, gồm cả năm 2010, rồi chấm trên chính năm 2010, được
0,380. Tin được không?

**Trực giác.** Học sinh xem đáp án rồi mới làm bài: điểm cao, nhưng không nói gì về lần thi thật.

**Ví dụ số nhỏ — tự tính tay.** Một ô bảng lịch có ba giờ của các năm trước, tổng 1,0 + 1,4 + 1,2 = 3,6 kWh. Giờ cần
chấm năm nay là 2,0 kWh.

- **Trung thực** (chỉ ba số cũ): dự báo (1,0 + 1,4 + 1,2)/3 = 1,2; sai số 2,0 − 1,2 = 0,8.
- **Nhìn trộm** (thêm giờ đang chấm): dự báo (1,0 + 1,4 + 1,2 + 2,0)/4 = 1,4; sai số 2,0 − 1,4 = 0,6.

Sai số nhỏ đi mà mô hình chẳng giỏi hơn: nó chỉ chứa sẵn một phần đáp án. FPP §5.8 đặt hai tên:

- **Phần dư**: tính trên chính dữ liệu đã dùng để khớp (kiểu nhìn trộm).
- **Sai số dự báo**: tính trên dữ liệu mô hình chưa thấy (kiểu trung thực).

Mô hình đủ nhiều tham số luôn khớp hoàn hảo dữ liệu đã thấy, nên phần dư nhỏ không đảm bảo dự báo tốt.

**Cách chấm trung thực — dự báo cuốn.** Đứng ở mỗi thứ Hai 00:00 của năm 2010. Tại mỗi gốc: chỉ dùng dữ liệu *trước*
gốc, dự báo 168 giờ tới, rồi mới so với số đo. Xong thì dời gốc sang thứ Hai sau.

```python
for goc in cac_goc:                                  # mỗi thứ Hai 00:00
    thoi_gian = pd.date_range(goc, periods=168, freq="h")
    lich_su = chuoi[chuoi.index < goc]               # CHỈ quá khứ
    du_bao = du_bao_bang_lich(bang_lich(lich_su), thoi_gian)
```

Từ gốc 4/1 tới gốc 15/11/2010 có 46 gốc, tức 46 × 168 = 7.728 giờ. Bỏ 293 giờ trống, còn 7.435 giờ được chấm.

![Sai số ảo và bảng xếp hạng thật](hinh/sai-so-ao.png)

**Cách đọc hình.**

1. **Trục ngang**: MAE (kWh/giờ) trên 46 tuần năm 2010; thanh càng ngắn càng tốt.
2. **Trục dọc**: tên phương pháp.
3. **Ký hiệu**: cam là bảng lịch chấm kiểu nhìn trộm; xanh là bảng lịch chấm trung thực; xám là bốn baseline.
4. **Nhìn vào đâu**: so thanh cam với thanh xanh (cùng mô hình), rồi thanh xanh với thanh xám ngay trên nó.
5. **Kết luận**: nhìn trộm thì bảng lịch đứng đầu; chấm trung thực thì nó thua trung bình 4 tuần.

**Đọc hình bằng số.** Cùng mô hình, trung thực cho 0,508 thay vì 0,380, lớn hơn khoảng 34%. Trung bình 4 tuần (0,490)
thắng bảng lịch, và thắng ở 30 trên 46 tuần.

**Vì sao chênh nhiều vậy?** Với dữ liệu tới hết 2009, mỗi ô trung bình có 2,99 giờ; thêm 2010 thì 3,82 giờ. Phần mới
chiếm (3,82 − 2,99)/3,82 ≈ 0,22. Vậy khoảng 22% số liệu mỗi ô (gần một phần năm) chính là giờ đang chấm.

![Một tuần: dự báo đã thấy đáp án](hinh/mot-tuan.png)

**Cách đọc hình.**

1. **Trục ngang**: 168 giờ của tuần 25–31/10/2010; vạch là 00:00 mỗi ngày.
2. **Trục dọc**: điện mỗi giờ (kWh/giờ).
3. **Ký hiệu**: đen là thực tế; cam là bảng lịch nhìn trộm; xanh dương là bảng lịch trung thực; xanh lá đứt là trung
   bình 4 tuần. MAE ghi trong chú thích.
4. **Nhìn vào đâu**: các đỉnh buổi tối; đường cam bám đỉnh đen sát hơn đường xanh dương.
5. **Kết luận**: đường cam "trúng" hơn chỉ vì mỗi ô của nó có sẵn số đo của tuần này.

Đây là tuần hai cách chấm chênh nhất. Mỗi ô ở tuần này thường có ba giờ của ba năm trước và một giờ của chính tuần
này: một phần tư là đáp án.

**Tóm lại.** **Chấm trên dữ liệu đã dùng để khớp cho sai số ảo. Chấm trung thực bằng dự báo cuốn: tại mỗi gốc chỉ dùng
dữ liệu trước gốc. Phép thử rẻ nhất: đổi số đo giai đoạn chấm; dự báo trung thực không được đổi theo.**

**Tự kiểm tra.** Một ô có hai giờ cũ 0,8 và 1,2 kWh; giờ cần chấm là 0,4 kWh. Tính sai số (thực tế − dự báo) khi chấm
trung thực và khi nhìn trộm.

<details>
<summary>Đáp án</summary>

Trung thực: dự báo 1,0; sai số 0,4 − 1,0 = −0,6. Nhìn trộm: dự báo (0,8 + 1,2 + 0,4)/3 = 0,8; sai số −0,4. Nhầm hay
gặp là nghĩ nhìn trộm chỉ có lợi khi thực tế cao; thật ra nó luôn kéo dự báo về phía đáp án.

</details>

### 4.5 Độ chi tiết quyết định cách chấm

**Vấn đề.** "Trung bình 4 tuần tốt hơn bảng lịch" đúng cho quyết định **theo giờ**. Nếu công ty mua một khối điện cho
cả tuần (ô 4 đổi) thì sao?

**Trực giác.** Mỗi giờ có phần lên xuống ngẫu nhiên gọi là **nhiễu**: máy giặt bật lúc 19:10 tuần này, 19:50 tuần sau.
Theo giờ, nhiễu làm dự báo lệch lúc lên lúc xuống. Cộng cả tuần, lệch lên và lệch xuống bù trừ nhau.

**Ví dụ số nhỏ — tự tính tay.** Bốn giờ thật là 2, 0, 2, 0 kWh, tổng 4.

- **Cách A** dự báo 1, 1, 1, 1. Sai số (thực tế − dự báo) là +1, −1, +1, −1, MAE giờ = 4/4 = 1. Tổng dự báo 4, sai số
  tổng 4 − 4 = 0.
- **Cách B** dự báo 2,5; 0,5; 2,5; 0,5. Sai số là −0,5 cả bốn giờ, MAE giờ = 0,5. Tổng dự báo 6, sai số tổng 4 − 6 = −2.

Theo giờ B thắng; theo tổng A thắng. Sai số +1 và −1 của A triệt tiêu khi cộng; −0,5 của B cùng dấu nên cộng dồn.

**Dữ liệu thật.** Cộng dự báo 168 giờ thành tổng tuần rồi chấm. Chỉ dùng **tuần đủ số đo**: cả 168 giờ đều có số. Có 41
tuần như vậy; 5 tuần còn lại thiếu ít nhất một giờ, cộng vào sẽ ra tổng thấp giả.

![Tổng tuần: thứ hạng đảo](hinh/tong-tuan.png)

**Cách đọc hình.**

1. **Trục ngang**: các tuần năm 2010, mỗi chấm một tuần tính từ thứ Hai.
2. **Trục dọc**: tổng điện của tuần (kWh/tuần).
3. **Ký hiệu**: đen có chấm là thực tế; xanh dương là bảng lịch (trung thực); xanh lá là trung bình 4 tuần; xám là tuần
   trước. MAE tổng tuần ghi trong chú thích.
4. **Nhìn vào đâu**: tháng 8. Xanh lá chỉ hạ *sau khi* kỳ nghỉ bắt đầu và lên lại chậm. Xanh dương hạ đúng lúc, vì bảng
   lịch đã thấy tháng 8 của ba năm trước.
5. **Kết luận**: cộng lên tổng tuần thì thứ hạng đảo: bảng lịch nhớ kỳ nghỉ tháng 8, hai baseline thì không.

| Phương pháp | MAE theo giờ (kWh/giờ) | MAE tổng tuần (kWh/tuần) |
|---|---|---|
| trung bình 4 tuần | 0,490 | 27,9 |
| bảng lịch (trung thực) | 0,508 | 16,4 |
| tuần trước | 0,576 | 24,2 |

**Đọc bảng.** Theo giờ, trung bình 4 tuần đứng đầu; theo tổng tuần, bảng lịch đứng đầu và trung bình 4 tuần xuống cuối.
Bảng lịch giống cách A: lệch từng giờ vì nhiễu, nhưng lệch bù trừ khi cộng, còn "nhịp năm" của nó thì giữ lại. Vì sao? Khi cộng lên tuần, phần lệch lúc lên lúc xuống của **cả ba** cách đều bù trừ. Cái không bù trừ là
**lệch cùng một chiều kéo dài nhiều ngày**. Trung bình 4 tuần chỉ hạ xuống sau khi kỳ nghỉ tháng 8 đã bắt đầu và lên lại
chậm, nên nhiều ngày liền dự báo cao hơn thực tế; cộng cả tuần thì sai số dồn lại. Bảng lịch đã thấy tháng 8 của ba năm
trước nên không mắc lỗi này.

**Tóm lại.** **Chấm ở đúng độ chi tiết của quyết định (ô 4). Hai mô hình có thể xếp hạng ngược nhau ở hai mức, nên điền
ô 4 trước khi chọn mô hình.**

**Tự kiểm tra.** Ba ngày thật 10, 20, 30 kWh. Cách C dự báo 20, 20, 20; cách D dự báo 12, 22, 32. Cách nào thắng theo
ngày (MAE), cách nào thắng theo tổng ba ngày?

<details>
<summary>Đáp án</summary>

C có sai số −10, 0, +10: MAE = 20/3 ≈ 6,7, còn sai số tổng = 60 − 60 = 0. D có sai số −2, −2, −2: MAE = 2, còn sai số
tổng = 60 − 66 = −6. Theo ngày D thắng, theo tổng C thắng. Nhầm hay gặp là nghĩ "MAE ngày nhỏ thì tổng cũng chính xác".

</details>

### 4.6 Một con số hay cả phân phối — khi thiếu và thừa đắt khác nhau

**Vấn đề.** Theo phiếu bài toán điện (mục 4.2), điện phải mua trước cho từng giờ (ô 1). Ô 6 ghi giá của việc mua
sai. Nếu mua **ít hơn** lượng nhà thật sự dùng, phần còn thiếu phải mua gấp với giá cao. Ta mất **4 đồng cho mỗi kWh
thiếu**. Nếu mua **nhiều hơn**, phần dư phải bán lại với giá thấp. Ta mất **1 đồng cho mỗi kWh thừa**. ("Đồng" ở đây
là đơn vị tiền giả định cho dễ tính.)

Vậy mỗi giờ nên mua bao nhiêu kWh? Câu trả lời tự nhiên là "mua đúng bằng dự báo trung bình". Mục này cho thấy câu
trả lời đó không tốt nhất, và chỉ ra nên mua bao nhiêu.

> **Mượn trước — phân phối và quantile** (buổi 2 học kỹ)
>
> - **Phân phối** của một đại lượng: danh sách các giá trị nó có thể nhận, và mỗi giá trị hay gặp tới đâu. Ví dụ
>   10 ngày qua, lúc 19 giờ nhà dùng 7, 5, 9, 6, 8, 12, 6, 9, 7, 8 kWh. Dãy này cho ta hình dung phân phối của
>   "lượng điện lúc 19 giờ".
> - **Quantile** (phân vị) mức 0,8: giá trị **nhỏ nhất** mà ít nhất 80% số giá trị nhỏ hơn hoặc bằng nó.
> - Cách tính tay: xếp tăng dần. Lấy vị trí bằng 0,8 × số giá trị, làm tròn lên. Với 10 giá trị thì 0,8 × 10 = 8,
>   nên lấy số thứ 8. Với 7 giá trị thì 0,8 × 7 = 5,6, làm tròn lên thành 6, nên lấy số thứ 6.
> - Xếp 10 số trên: 5, 6, 6, 7, 7, 8, 8, **9**, 9, 12. Số thứ 8 là 9, nên quantile 0,8 là **9 kWh**. Kiểm lại: có 9
>   trên 10 ngày dùng không quá 9 kWh (vì hai ngày cùng dùng 9). Như vậy là "ít nhất 80%", đúng định nghĩa.
> - Quantile 0,5 là mốc chia đôi, còn gọi là **trung vị**.

**Trực giác.** Hãy nghĩ tới người bán bánh mì buổi sáng. Hết bánh sớm thì mất khách, mất lãi. Còn dư vài cái thì
chỉ lỗ tiền bột. Nếu hết bánh đắt hơn dư bánh, họ sẽ làm **dư ra một chút** so với lượng bán trung bình. Mua điện
cũng vậy: thiếu đắt gấp 4 lần thừa, nên nên mua cao hơn mức trung bình.

**Ví dụ số nhỏ — tự tính tay.** Dùng lại 10 ngày ở trên. Giả sử ngày nào cũng mua cùng một lượng. Với mỗi lượng
mua, cộng chi phí của cả 10 ngày:

- **Thiếu** (kWh) = nhu cầu − lượng mua, ở những ngày nhu cầu lớn hơn lượng mua.
- **Thừa** (kWh) = lượng mua − nhu cầu, ở những ngày nhu cầu nhỏ hơn.
- **Chi phí** = 4 × tổng kWh thiếu + 1 × tổng kWh thừa (đồng).

Tính một dòng làm mẫu, mua 8 kWh mỗi ngày:

- Ngày thiếu là các ngày dùng 9, 9 và 12. Tổng thiếu là 1 + 1 + 4 = 6 kWh, nên mất 4 × 6 = 24 đồng.
- Ngày thừa là các ngày dùng 5, 6, 6, 7 và 7. Tổng thừa là 3 + 2 + 2 + 1 + 1 = 9 kWh, nên mất 1 × 9 = 9 đồng.
- Tổng chi phí là 24 + 9 = **33 đồng**.

| Mua mỗi ngày (kWh) | Số ngày thiếu | Tổng kWh thiếu | Tổng kWh thừa | Chi phí 10 ngày (đồng) |
|---|---|---|---|---|
| 6 | 7 | 18 | 1 | 73 |
| 7 | 5 | 11 | 4 | 48 |
| 8 | 3 | 6 | 9 | 33 |
| **9** | 1 | 3 | 16 | **28** |
| 10 | 1 | 2 | 25 | 33 |
| 11 | 1 | 1 | 34 | 38 |
| 12 | 0 | 0 | 43 | 43 |

**Đọc bảng.** Nhìn cột cuối từ trên xuống.

- Chi phí giảm dần rồi tăng lại, thấp nhất ở dòng **mua 9 kWh** (28 đồng).
- Con số 9 chính là quantile 0,8 vừa tính trong hộp "Mượn trước".
- Lượng dùng trung bình là 7,7 kWh. Mua đúng 7,7 kWh mỗi ngày thì tốn 37,5 đồng, đắt hơn cách mua tốt nhất khoảng 34%.

**Vì sao lại là quantile 0,8?** Thử tăng lượng mua từng kWh một và xem lời hay lỗ.

- **Từ 8 lên 9.** Có 3 ngày đang thiếu (dùng 9, 9, 12). Mỗi ngày đó bớt thiếu 1 kWh, tiết kiệm 3 × 4 = 12 đồng.
  Bảy ngày còn lại vốn đã đủ hoặc thừa, nay thừa thêm 1 kWh, mất 7 × 1 = 7 đồng. Lời 12 − 7 = 5 đồng, nên tăng (chi phí 33 → 28).
- **Từ 9 lên 10.** Chỉ còn 1 ngày thiếu (dùng 12), tiết kiệm 1 × 4 = 4 đồng. Chín ngày còn lại thừa thêm, mất
  9 × 1 = 9 đồng.
  Lỗ 9 − 4 = 5 đồng, nên dừng ở 9 (chi phí 28 → 33).

Quy luật: thêm 1 kWh còn có lời chừng nào số ngày thiếu, nhân với 4, còn lớn hơn số ngày dư, nhân với 1. Gọi $s$ là
tỷ lệ ngày còn thiếu **ở lượng mua hiện tại** (chữ $s$ cho "số ngày thiếu", để khỏi lẫn với mức quantile $p^\ast$ ở
dưới). Tăng thêm có lời khi $4s > 1 \times (1 - s)$, tức là khi $s > 0{,}2$.

Quy tắc dừng: tăng dần lượng mua, và **dừng ở mức đầu tiên mà tỷ lệ ngày thiếu không quá 20%**. Mua 8 thì 3 trên 10
ngày thiếu (30%), còn quá 20%, nên tăng tiếp. Mua 9 thì 1 trên 10 ngày thiếu (10%), đã không quá 20%, nên dừng.
Mức dừng là mức nhỏ nhất đủ điện cho ít nhất 100% − 20% = 80% số ngày. Đó đúng là định nghĩa quantile 0,8.

Làm lại với chữ thay cho số 4 và 1. Gọi $C_u$ là tiền mất cho mỗi kWh thiếu (ở đây 4) và $C_o$ là tiền mất cho mỗi kWh
thừa (ở đây 1). Tăng thêm có lời khi $C_u \, s > C_o (1 - s)$. Chuyển vế: $C_u s + C_o s > C_o$, tức $s (C_u + C_o) > C_o$,
tức $s > C_o / (C_u + C_o)$.
Vậy ta dừng khi tỷ lệ ngày thiếu còn $C_o / (C_u + C_o)$, tức tỷ lệ ngày đủ là $1 - C_o/(C_u + C_o) = C_u/(C_u + C_o)$.
Thay số: $1 / (4 + 1) = 0{,}2$ ngày thiếu, nên $4/(4 + 1) = 0{,}8$ ngày đủ.

**Công thức.**

$$
p^\ast = \frac{C_u}{C_u + C_o}
$$

- $C_u$: chi phí cho mỗi kWh **thiếu** (chữ u là *under*, mua dưới nhu cầu). Ở đây 4 đồng.
- $C_o$: chi phí cho mỗi kWh **thừa** (chữ o là *over*, mua trên nhu cầu). Ở đây 1 đồng.
- $p^\ast$: mức quantile nên mua.

**Nói bằng lời.** Mức quantile nên mua bằng chi phí thiếu chia cho tổng hai chi phí.

- Thiếu 4, thừa 1: $4 / (4 + 1) = 0{,}8$, nên mua ở quantile 0,8.
- Ngược lại, thiếu 1, thừa 3: $1 / (1 + 3) = 0{,}25$, nên mua **thấp hơn** trung vị.
- Thiếu và thừa đắt như nhau: $1/2 = 0{,}5$, nên mua đúng trung vị.

Trường hợp cuối giải thích câu "MAE nhắm trung vị". MAE cộng mọi kWh lệch như nhau, dù thiếu hay thừa (mục 4.3). Tức
là MAE giống chi phí với thiếu 1 đồng, thừa 1 đồng. Vậy con số làm MAE nhỏ nhất là quantile 0,5, tức trung vị.

Bài toán này có tên **newsvendor** (người bán báo): sáng nay nên nhập bao nhiêu tờ báo, khi báo thừa phải bỏ còn
báo thiếu thì mất khách.

**Tự viết bằng NumPy.**

```python
import numpy as np

nhu_cau = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])   # kWh
C_u, C_o = 4, 1                                         # đồng / kWh thiếu, đồng / kWh thừa

def chi_phi(mua, y=nhu_cau):
    thieu = np.clip(y - mua, 0, None)   # chỉ giữ phần nhu cầu vượt lượng mua
    thua = np.clip(mua - y, 0, None)    # chỉ giữ phần lượng mua vượt nhu cầu
    return C_u * thieu.sum() + C_o * thua.sum()

chi_phi(8), chi_phi(9)                   # (33, 28)
np.quantile(nhu_cau, C_u / (C_u + C_o))  # 9.0 — trùng lượng mua rẻ nhất
```

Lưu ý: mặc định `np.quantile` không đếm như cách tính tay mà **nội suy** giữa hai số kề nhau, nên có thể ra số lẻ.
Ví dụ với dãy 1, 1, 2, 3, 3, 4, 5, 5, 6, 9, tính tay ra 5 còn `np.quantile(..., 0.8)` ra 5,2. Muốn khớp cách tính tay,
thêm `method="inverted_cdf"`.

Với 10 ngày của ví dụ, cả hai cách đều ra cùng một số. Trong pandas, phép tính tương ứng là
`pd.Series(nhu_cau).quantile(0.8)`. Script in mọi con số của ví dụ này: `dap-an/vi_du_quantile.py`.

**Dữ liệu thật: hộ gia đình năm 2010.** Với dữ liệu thật, ta chưa có sẵn phân phối của từng giờ. Ta chỉ có dự báo
**trung bình 4 tuần** (mục 4.3), mỗi giờ một con số: trung bình của cùng giờ đó trong 4 tuần trước. Cách đơn giản để
"mua dư đúng mức" là xem dự báo này **thường hụt bao nhiêu** trong quá khứ.

1. **Sai số = thực tế − dự báo.** Sai số dương nghĩa là thực tế cao hơn dự báo. Khi đó, mua đúng bằng dự báo sẽ
   **thiếu**. Sai số âm nghĩa là mua đúng dự báo sẽ **thừa**.
2. **Lấy sai số của năm 2009.** Làm đúng như mục 4.4: mỗi thứ Hai của năm 2009 dự báo cả tuần tới, chỉ dùng dữ
   liệu trước thứ Hai đó. Năm 2009 có 8.665 giờ đủ số đo. Quantile 0,8 của các sai số đó là **+0,455 kWh**. Nghĩa là
   trong 80% số giờ, thực tế vượt dự báo không quá 0,455 kWh (kể cả những giờ thực tế thấp hơn dự báo).
3. **Dự báo mới cho năm 2010** = trung bình 4 tuần + 0,455 kWh. Con số 0,455 chỉ tính từ năm 2009. Năm 2010 là năm
   được chấm, nên không được dùng để chọn nó (nếu dùng thì thành sai số ảo, mục 4.4).

Vì sao bước 3 đúng ý newsvendor? Mua "dự báo + 0,455" thì theo năm 2009, khoảng 80% số giờ đủ điện. Nói cách khác,
lượng mua đó **xấp xỉ** quantile 0,8 của lượng điện giờ ấy, đúng như công thức ở trên. Chữ "xấp xỉ" vì ta giả định
năm 2010 lệch giống năm 2009, và mọi giờ lệch như nhau. Bảng dưới sẽ kiểm giả định đó. Cộng cùng một con số cho mọi
giờ là cách đơn giản nhất. Buổi 25 học cách dự báo quantile riêng cho từng giờ.

Hai cách mua được chấm trên năm 2010. Chi phí trung bình mỗi giờ tính bằng 4 × kWh thiếu + 1 × kWh thừa, cộng qua
mọi giờ rồi chia cho số giờ.

| Cách mua cho năm 2010 | Chi phí trung bình (đồng/giờ) | MAE (kWh/giờ) | Tỷ lệ giờ bị thiếu |
|---|---|---|---|
| Đúng bằng trung bình 4 tuần | 1,213 | **0,490** | 44,0% |
| Trung bình 4 tuần + 0,455 kWh | **0,987** | 0,673 | 20,1% |

**Đọc bảng.** So hai dòng theo từng cột.

- **Chi phí** (tiền thật mất): dòng 2 thấp hơn, giảm 18,6%.
- **MAE** (sai lệch trung bình, không kể dấu): dòng 2 lại **tệ hơn**. MAE phạt thiếu và thừa như nhau, nên nó không
  thấy lợi ích của việc mua dư.
- **Tỷ lệ giờ bị thiếu**: dòng 1 thiếu ở gần một nửa số giờ. Dòng 2 thiếu 20,1% số giờ, gần đúng mức 20% mà quantile
  0,8 hứa. Vậy con số 0,455 chọn từ năm 2009 vẫn dùng tốt cho năm 2010.

Kết luận: người chỉ nhìn MAE sẽ chọn dòng 1, và mất nhiều tiền hơn.

![Cộng thêm vào dự báo làm chi phí giảm dù MAE tăng](hinh/chi-phi-bat-doi-xung.png)

**Cách đọc hình.**

1. **Trục ngang** (cả hai ô): số kWh cộng thêm vào dự báo trung bình 4 tuần, từ 0 (không cộng) tới 1 kWh.
2. **Trục dọc**: ô trái là chi phí trung bình mỗi giờ của năm 2010 (đồng); ô phải là MAE (kWh/giờ).
3. **Ký hiệu**: mỗi chấm là một mức cộng thêm, các mức cách nhau 0,05 kWh. Vạch cam đứt là mức 0,455 kWh chọn từ
   năm 2009.
4. **Nhìn vào đâu**: ở ô trái, tìm đáy của đường cong. Chi phí thấp nhất nằm quanh 0,45–0,5 kWh, và vạch cam rơi gần
   đúng đáy. Ở ô phải, cùng vị trí đó, MAE vẫn đang tăng.
5. **Kết luận**: cộng thêm làm chi phí giảm nhưng làm MAE tăng. Chấm bằng thước đo sai thì sẽ chọn sai.

**Tóm lại.** **Khi thiếu và thừa đắt khác nhau, đừng mua đúng bằng dự báo trung bình. Hãy mua ở quantile
$C_u / (C_u + C_o)$: thiếu 4, thừa 1 thì là quantile 0,8. Đây là lý do khoá học dạy **dự báo phân phối** (cả danh
sách giá trị có thể xảy ra, không chỉ một con số). Có phân phối rồi thì với tỷ lệ chi phí nào, ta cũng chỉ việc đọc ra
một quantile khác.**

**Tự kiểm tra.** Một tiệm bánh ngọt: bánh thừa cuối ngày phải bỏ, mất 3 nghìn đồng mỗi cái. Thiếu bánh thì mất
1 nghìn đồng tiền lãi mỗi cái. Nên làm số bánh ở quantile nào, cao hay thấp hơn trung vị?

<details>
<summary>Đáp án</summary>

Thiếu là $C_u = 1$, thừa là $C_o = 3$, nên $p^\ast = 1 / (1 + 3) = 0{,}25$. Quantile 0,25 thấp hơn trung vị (0,5).
Tiệm nên làm **ít hơn** lượng bán thường ngày, vì thừa đắt hơn thiếu. Nhầm hay gặp là đảo $C_u$ và $C_o$, ra 0,75.

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> - Sách thường viết công thức ở dạng $Q^\ast = F^{-1}(p^\ast)$. Trong đó $F(x)$ là tỷ lệ giá trị nhỏ hơn hoặc bằng
>   $x$ (hàm phân phối tích luỹ). $F^{-1}$ làm ngược lại: nhận một tỷ lệ, trả về mốc. Đó chính là quantile.
> - Cùng ý đó từ phía chấm điểm (Gneiting, 2011): phải nói trước dự báo sẽ bị chấm bằng gì. Chấm bằng MAE thì con
>   số tốt nhất là **trung vị**. Chấm bằng chi phí lệch 4 : 1 thì con số tốt nhất là **quantile 0,8**. Vì vậy, bảng
>   "Lỗi thường gặp" ở mục 6 ghi "MAE nhắm trung vị".

## 5. Lab từng bước

Lệnh chạy trong `lab/`. Đoạn code ở bước 2 và 4 chạy trong một notebook đặt ở `code/` (`make notebook`).

### Bước 1 — Dựng môi trường, kiểm phiên bản

**Mục đích:** cài đúng thư viện, tải dữ liệu, chắc rằng máy bạn giống máy tác giả.

```bash
cd lab && make up          # cài thư viện theo phiên bản đã chốt + tải dữ liệu, kiểm sha256
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/kiem_tra_moi_truong.py
make notebook              # mở JupyterLab, các tệp .py thành notebook
```

Lệnh thứ hai chạy Python *trong môi trường riêng của buổi* (`00-nen/`), không lẫn với Python của máy.

```text
Python      3.12.3
numpy       2.5.3
pandas      3.0.5
matplotlib  3.11.2
dữ liệu     household_power_consumption.txt 132,960,755 byte
```

**Đọc kết quả:** phiên bản khớp mục 3 thì mọi con số của tài liệu sẽ ra y hệt. Dòng "dữ liệu" ghi "CHƯA CÓ" thì chạy
lại `make up` và đọc thông báo lỗi.

### Bước 2 — Vẽ một đường, đặt câu hỏi

**Mục đích:** tự nhìn 4 năm trên một hình và tự đặt câu hỏi, rồi mới so với năm câu mẫu ở mục 4.2.

```python
from danh_gia import doc_dien_theo_gio

s = doc_dien_theo_gio()                    # 34.464 giờ, 431 giờ trống
ngay = s.resample("D").sum(min_count=20)   # ngày có dưới 20 giờ đủ số đo thì để trống, không cộng thiếu
ngay.plot(figsize=(10, 3), ylabel="kWh / ngày")
```

Không có `min_count`, `sum()` coi giờ trống là 0 và ngày mất tín hiệu hiện ra như ngày "dùng 0 kWh".

**Đọc kết quả:** đường đứt ở những ngày có dưới 20 giờ đủ số đo, ví dụ 18–21/8/2010. Đó là mất tín hiệu, không phải
nhà dùng 0 kWh.

| Loại ngày trống | Số ngày |
|---|---|
| dưới 20 giờ đủ số đo (bị `min_count=20` để trống) | 21 |
| trong đó: không có giờ nào đủ số đo (mục 4.2) | 10 |

**Đọc bảng.** Hai con số không mâu thuẫn: 10 ngày "không có giờ nào" nằm trong 21 ngày "dưới 20 giờ".

Thấy ngày 0 kWh là bạn đã quên `min_count`. Viết ít nhất ba câu hỏi của riêng bạn trước khi mở lại năm câu mẫu.

### Bước 3 — Ba phiếu bài toán

**Mục đích:** luyện điền phiếu 6 ô (mục 4.2) cho tình huống khác điện. Điền `code/phieu-bai-toan.md` cho ba tình huống: (a) chuỗi 40 quán cà phê đặt hạt và sữa mỗi thứ Năm; (b) Tập đoàn Điện lực Việt Nam lên kế hoạch phát điện cho ngày mai; (c) bệnh viện xếp lịch trực 9 ngày Tết.

**Đọc kết quả:** đủ 6 ô, ô 3 nói rõ tính từ lúc nào, ô 6 có **cả hai chiều**. Ô 6 chỉ một chiều thì chưa biết nên báo
con số nào (mục 4.6).

### Bước 4 — Đoán bằng mắt

**Mục đích:** tự đoán trước khi xem các phương pháp, để thấy đoán bằng mắt khó cỡ nào.

```python
tam = s["2010-09-20":"2010-11-14"]         # 8 tuần ngay trước gốc 15/11/2010
tam.plot(figsize=(10, 3), ylabel="kWh / giờ")
tuan = tam.index.to_period("W-SUN").start_time          # mỗi giờ -> thứ Hai đầu tuần của nó
print(tam.groupby(tuan).sum(min_count=168).round(1))    # tổng tuần; tuần thiếu giờ thì để trống
```

```text
2010-09-20      NaN
2010-09-27      NaN
2010-10-04    198.0
2010-10-11    184.3
2010-10-18    234.6
2010-10-25    161.1
2010-11-01    194.0
2010-11-08    224.4
```

Python in dấu chấm thập phân: `198.0` là 198,0 kWh. Hai tuần đầu trống vì có giờ không đủ số đo. Ghi ra giấy con số bạn
đoán cho **tổng điện tuần 15–21/11/2010**, rồi mới xem bảng (kWh/tuần):

| Tuần bắt đầu | Thực tế | trung bình 4 tuần | tuần trước | bảng lịch |
|---|---|---|---|---|
| 01/11/2010 | 194,0 | 194,5 | 161,1 | 138,0 |
| 08/11/2010 | 224,4 | 193,5 | 194,0 | 218,1 |
| 15/11/2010 | 186,0 | 203,5 | 224,4 | 236,7 |

**Đọc bảng.** Mỗi dòng, tìm cột gần "Thực tế" nhất. Tuần đầu, trung bình 4 tuần gần nhất; tuần thứ hai, bảng lịch gần
nhất; tuần cuối, không cột nào gần.

**Đọc kết quả:** không phương pháp nào thắng mọi tuần, kể cả con số bạn đoán. Vì vậy phải chấm trên nhiều gốc.

### Bước 5 — Chạy code đầu buổi, thấy sai số ảo, sửa

**Mục đích:** thấy con số 0,38 "quá đẹp", sửa nguyên nhân (mục 4.4), thêm baseline (mục 4.3).

```bash
env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../code/danh_gia.py
make check
```

```text
34464 giờ, thiếu 431, trung bình 1.091 kWh/giờ
bảng lịch    0.38
```

`1.091` là 1,091 kWh/giờ (dấu chấm thập phân), không phải một nghìn. Bảng chỉ một dòng, không có gì để so; 4 test đỏ.

Sửa `du_bao_cuon` trong `code/danh_gia.py`:

1. Khớp bảng lịch **bên trong** vòng lặp, chỉ trên `chuoi[chuoi.index < goc]`.
2. Thêm bốn cột baseline, dùng lịch sử đã điền bằng `dien_bang_tuan_truoc` (mục 4.3); riêng "trung bình" dùng lịch sử
   chưa điền.

Chạy lại:

```text
trung bình 4 tuần    0.490
bảng lịch            0.508
tuần trước           0.576
trung bình           0.652
giờ trước            0.770
```

**Đọc kết quả:** bảng lịch lên 0,508 và xuống hạng hai. Nếu nó vẫn quá đẹp, bạn còn khớp nó trên dữ liệu có giờ đang
chấm. `make check` phải xanh hết. Test `test_du_bao_khong_nhin_thay_tuong_lai` cộng 5 kWh vào mọi giờ của tuần cuối rồi đòi
mọi dự báo giữ nguyên; dự báo đổi theo nghĩa là nó đã thấy đáp án.

## 6. Lỗi thường gặp & cách chẩn đoán

| Triệu chứng | Nguyên nhân | Chẩn đoán | Sửa |
|---|---|---|---|
| MAE rất đẹp, không có gì để so | không có baseline | hỏi "tốt hơn cái gì?" | luôn báo ít nhất naive, seasonal naive, trung bình |
| Sai số khi dùng thật tệ hơn hẳn báo cáo | chấm trên dữ liệu đã dùng để khớp | đổi số đo giai đoạn chấm: dự báo có đổi theo không? | dự báo cuốn, chỉ dữ liệu trước gốc |
| Baseline "cùng giờ hôm qua" thắng với tầm 7 ngày | baseline dùng số chưa có tại gốc | với mọi $h$, kiểm giờ lấy số $T + h - \text{trễ}$ có $\le T$ không (trễ = số giờ lùi lại) | chọn trễ ≥ tầm (168 giờ) |
| "Mô hình A tốt hơn B" rồi đổi ý khi báo cáo tuần | chấm sai độ chi tiết | chấm ở đúng mức của quyết định (ô 4) | cộng dự báo lên mức quyết định rồi chấm |
| Chọn mô hình MAE thấp nhất mà chi phí vẫn cao | chi phí lệch; MAE nhắm trung vị (mục 4.6) | tính chi phí theo ô 6 | báo quantile $C_u/(C_u+C_o)$ |
| Dự báo "khớp mục tiêu kinh doanh" | lẫn dự báo với mục tiêu | so con số với ô 1 của phiếu | tách: dự báo trung thực, kế hoạch để đạt mục tiêu |
| Tổng tuần của dự báo thấp dù từng giờ ổn | điền giờ trống bằng 0 | đếm giờ `NaN` mỗi tuần | điền bằng tuần trước; chấm chỉ trên giờ có số đo |

## 7. Bài tập về nhà

1. **Phiếu cho tình huống của bạn.** Chọn một quyết định ở nơi bạn làm hoặc học. Điền phiếu 6 ô trong 15 phút, kèm
   một câu cho mỗi yếu tố trong bốn yếu tố của mục 4.1.
2. **Kết hợp dự báo.** Kết hợp dự báo là lấy trung bình dự báo của nhiều phương pháp. Ví dụ trung bình 4 tuần báo 1,5,
   bảng lịch báo 1,9 → dự báo kết hợp (1,5 + 1,9)/2 = 1,7. Thêm cột này vào `du_bao_cuon`. Chấm theo giờ và theo tổng
   tuần, so với bảng ở mục 4.4 và 4.5. Kết hợp có thắng cả hai phương pháp gốc không?
3. **Chi phí đảo chiều.** Đổi thành thiếu 1 đồng/kWh, thừa 3 đồng/kWh. Theo công thức ở mục 4.6, quantile nào là tốt
   nhất? Làm lại ba bước "Dữ liệu thật" của mục 4.6: lấy sai số (thực tế − dự báo) của trung bình 4 tuần năm 2009, tính
   quantile đó bằng `np.nanquantile(sai_so, muc)`, cộng vào dự báo năm 2010. Báo chi phí trung bình mỗi giờ và tỷ lệ
   giờ bị thiếu. Gợi ý: con số cộng thêm lần này là số âm, tức mua ít hơn dự báo.

## 8. Tiêu chí "Xong khi"

- [ ] `make check` xanh 8/8.
- [ ] Viết được phiếu bài toán cho một tình huống lạ trong 15 phút, đủ 6 ô, ô 6 có cả hai chiều.
- [ ] Giải thích bằng số vì sao 0,380 là sai số ảo, và vì sao con số trung thực (0,508) thua một baseline.
- [ ] Giải thích vì sao ở tổng tuần thứ hạng đảo lại, và vì sao với chi phí thiếu 4 : thừa 1 nên báo quantile 0,8.

## 9. Đọc thêm

**Các cuộc thi dự báo M1–M6** (Makridakis và cộng sự): nhiều đội cùng dự báo một bộ chuỗi thật, chấm trên dữ liệu
tương lai. M1 (1982, 1.001 chuỗi) kết luận phương pháp phức tạp không chắc chính xác hơn phương pháp đơn giản, thứ hạng
đổi theo thước đo, và lấy trung bình nhiều phương pháp thường tốt hơn từng cái; M3 (2000, 3.003 chuỗi) xác nhận lại.
M4 (2018): 12 trong 17 phương pháp tốt nhất là kết hợp nhiều phương pháp. M5 (2022, 42.840 chuỗi bán lẻ Walmart): lần
đầu các phương pháp dẫn đầu đều là machine learning, tức cho máy tự tìm quy luật từ rất nhiều chuỗi liên quan (buổi
22–23). M6 (công bố 2025, cổ phiếu): độ chính xác dự báo gần như không liên quan tới lãi đầu tư, đúng ý mục 4.6 —
dự báo đúng hơn chưa chắc thành quyết định tốt hơn.

**Các cách tiếp cận trong khoá**: mô hình thống kê cho từng chuỗi, machine learning, deep learning, mô hình học sẵn
trên hàng triệu chuỗi, mô hình ngôn ngữ lớn. Cách nào cũng chấm bằng quy trình của buổi này: dự báo cuốn, chỉ dữ liệu
trước gốc, luôn có baseline.

**Tài liệu.**

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way* — chương 1 (§1.1–1.7)
  và chương 5 (§5.2 phương pháp đơn giản, §5.8 đánh giá độ chính xác): https://otexts.com/fpppy/
- Makridakis, S. & Hibon, M. (2000). The M3-Competition: results, conclusions and implications. *IJF* 16(4), 451–476.
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2018). The M4 Competition: Results, findings, conclusion and way
  forward. *IJF* 34(4), 802–808.
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and
  conclusions. *IJF* 38(4), 1346–1364.
- Makridakis, S. et al. (2025). The M6 forecasting competition: Bridging the gap between forecasting and investment
  decisions. *IJF* 41(4), 1315–1354. arXiv:2310.13357
- Petropoulos, F. et al. (2022). Forecasting: theory and practice. *IJF* 38(3), 705–871. arXiv:2012.03854 — mục 2.12.1
  về baseline.
- Gneiting, T. (2011). Making and evaluating point forecasts. *JASA* 106(494), 746–762. arXiv:0912.0902
- Hebrail, G. & Berard, A. (2006). Individual Household Electric Power Consumption. UCI Machine Learning Repository.
  https://doi.org/10.24432/C58K54
