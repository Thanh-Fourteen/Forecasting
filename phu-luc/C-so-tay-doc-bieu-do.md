# Phụ lục C — Sổ tay đọc biểu đồ chuỗi thời gian

Mỗi loại hình có: **trả lời câu hỏi gì**, **cách đọc** theo năm bước, **bẫy**, một cặp **đọc đúng / đọc sai**, và **ví dụ có số** lấy
từ lần chạy thật của một buổi (hình nằm trong `buoi-NN/hinh/` của buổi đó). Dùng như checklist trước khi kết luận điều gì từ một
hình. Mục 1–9 dùng từ buổi 4; các mục sau ghi buổi dạy kỹ, đọc khi học tới buổi đó.

## Mục lục

- [0. Năm bước đọc mọi hình](#0-năm-bước-đọc-mọi-hình)
- [1. Biểu đồ đường](#1-biểu-đồ-đường)
- [2. Seasonal plot](#2-seasonal-plot)
- [3. Subseries plot](#3-subseries-plot)
- [4. Heatmap lịch](#4-heatmap-lịch)
- [5. Boxplot theo mùa](#5-boxplot-theo-mùa)
- [6. Scatter và ma trận scatter](#6-scatter-và-ma-trận-scatter)
- [7. Lag plot](#7-lag-plot)
- [8. ACF](#8-acf)
- [9. Hình gây hiểu nhầm](#9-hình-gây-hiểu-nhầm)
- [10. Biểu đồ phân rã](#10-biểu-đồ-phân-rã)
- [11. PACF](#11-pacf)
- [12. CCF](#12-ccf)
- [13. Tương quan trượt](#13-tương-quan-trượt)
- [14. Periodogram](#14-periodogram)
- [15. QQ-plot](#15-qq-plot)
- [16. Fan chart](#16-fan-chart)
- [17. PIT histogram và rank histogram](#17-pit-histogram-và-rank-histogram)
- [18. Reliability diagram](#18-reliability-diagram)
- [Nguồn](#nguồn)

## 0. Năm bước đọc mọi hình

Mọi hình trong khoá kèm khối "Cách đọc hình" theo đúng thứ tự:

1. **Trục ngang** là gì, đơn vị gì. Trục thời gian: múi giờ nào (buổi 3).
2. **Trục dọc** là gì, đơn vị gì, bắt đầu từ đâu, thang thường hay thang log. Có hai trục dọc không.
3. **Ký hiệu**: mỗi màu, đường, chấm, vạch, dải là gì.
4. **Nhìn vào đâu**: chỉ đúng một vùng trên hình.
5. **Kết luận**: một câu người khác kiểm được trên hình, có chỗ và có số. Câu này cũng là **tiêu đề** nên đặt cho hình ("Tải
   điện có mùa vụ ngày và tuần, tăng dần qua các năm"), không phải tên biến ("Tải điện theo thời gian").

Ba câu tự hỏi trước khi tin bước 5:

- **Nếu chỉ là nhiễu thuần thì hình trông thế nào?** Nhiều "mẫu hình" là thứ số ngẫu nhiên cũng tạo ra.
- **Hình này đã bỏ gì?** Gộp, làm trơn, cắt trục, chọn khoảng thời gian đều bỏ bớt thông tin.
- **Một hình không chứng minh nhân quả.** Hình gợi giả thuyết; kiểm bằng số và bằng dữ liệu khác.

Các mục dưới ghi bước 1–4 cho **dạng chuẩn** của từng loại hình; bước 5 là câu mẫu, thay bằng số của bạn.

## 1. Biểu đồ đường

**Trả lời câu hỏi gì:** chuỗi đi thế nào theo thời gian: xu hướng, mùa vụ, chu kỳ, chỗ nhảy mức, đoạn thiếu, điểm lạ (buổi 4).

**Cách đọc hình.**

1. **Trục ngang**: thời gian, ở một tần suất (giờ, ngày, tháng).
2. **Trục dọc**: giá trị kèm đơn vị theo đúng tần suất đó (lượt/giờ khác lượt/ngày).
3. **Ký hiệu**: mỗi điểm là một mốc thời gian, nối bằng đường thẳng; nếu có đường làm trơn thì nó phải đè lên dữ liệu gốc, không
   thay nó.
4. **Nhìn vào đâu**: mức chung đầu và cuối (xu hướng); đoạn lặp theo lịch (mùa vụ); lên xuống dài mà độ dài không cố định (chu kỳ);
   độ rộng dao động ở mức cao so với mức thấp.
5. **Kết luận** (mẫu): "Có xu hướng tăng và mùa vụ năm; dao động lớn dần theo mức, cân nhắc lấy log (buổi 5)."

**Bẫy:**

- Đường nối qua đoạn **thiếu dữ liệu** trông như dữ liệu thật đi thẳng: để NaN cho đường đứt, hoặc đánh dấu đoạn thiếu.
- Chuỗi dài nén vào khung hẹp thành một khối màu, che mùa vụ ngắn: gộp lên ngày, hoặc phóng to vài tuần, hoặc dùng seasonal plot.
- Gộp thô (tháng) và làm trơn xoá luôn ngày bất thường.

| Đọc đúng | Đọc sai |
|---|---|
| "Biên độ mùa vụ năm tăng theo mức → cân nhắc log hoặc Box-Cox" | "Dao động lớn hơn nên khó dự báo hơn" (chưa xét dao động so với mức) |
| "Lên xuống 6–10 năm, độ dài không đều → chu kỳ" | "Có mùa vụ 8 năm" |

**Ví dụ có số (buổi 4, lượt thuê xe theo giờ 2011–2012).** Vẽ theo giờ (17.544 điểm) chỉ đọc được "hè cao hơn đông". Theo ngày
thấy ngày bão Sandy 29/10/2012 rơi xuống 22 lượt. Theo tháng, mọi dao động ngày, tuần và cả ngày bão biến mất. Làm trơn 7 ngày biến
ngày đó thành 4.632 lượt, chỉ còn một chỗ lõm nhẹ.

## 2. Seasonal plot

**Trả lời câu hỏi gì:** hình dạng một vòng lặp mùa vụ ra sao, và vòng nào lệch khỏi khuôn chung (buổi 4).

**Cách đọc hình.**

1. **Trục ngang**: vị trí trong vòng lặp: tháng trong năm, hoặc giờ trong tuần (0 = thứ Hai 0h … 167 = Chủ nhật 23h).
2. **Trục dọc**: giá trị, cùng đơn vị với chuỗi.
3. **Ký hiệu**: mỗi đường là một vòng lặp (một năm, một tuần); đường đậm, nếu có, là trung vị hay trung bình của mọi vòng.
4. **Nhìn vào đâu**: hình dạng đường đậm (đỉnh, đáy ở đâu); đường nào tách khỏi đám đông.
5. **Kết luận** (mẫu): "Ngày làm việc hai đỉnh, cuối tuần một bướu giữa ngày: mùa vụ ngày đổi hình dạng theo thứ."

**Bẫy:** quá nhiều đường chồng nhau thì không chỉ ra được đường nào: tô màu theo năm tăng dần, hoặc chỉ vẽ vài vòng. Dữ liệu giờ có
cả mùa vụ ngày lẫn tuần thì vẽ theo giờ trong **tuần**, không theo giờ trong ngày (sẽ trộn thứ Hai với Chủ nhật).

| Đọc đúng | Đọc sai |
|---|---|
| "Đỉnh tháng 12 năm 2020 thấp bất thường so với các năm khác → sự kiện, kiểm lại" | "Tháng 12 luôn cao" khi chỉ nhìn đường trung bình |

**Ví dụ có số (buổi 4).** Seasonal plot theo giờ trong tuần của lượt thuê xe: năm ô thứ Hai – thứ Sáu có hai đỉnh (8h và 17h), hai
ô cuối tuần một bướu giữa ngày. Tổng ngày lại gần bằng nhau (thứ Hai 4.708, Chủ nhật 4.523 lượt, trung bình 655 ngày đủ 24 giờ):
khác nhau ở **hình dạng**, không ở mức.

## 3. Subseries plot

**Trả lời câu hỏi gì:** mỗi "mùa" (mỗi tháng, mỗi thứ) đổi thế nào qua thời gian, và mức trung bình của từng mùa (buổi 4).

**Cách đọc hình.**

1. **Trục ngang**: các ô liền nhau, mỗi ô một mùa; trong ô, thời gian chạy từ trái sang phải (năm đầu rồi năm sau).
2. **Trục dọc**: giá trị, chung một thang cho mọi ô.
3. **Ký hiệu**: đường trong ô là chuỗi con của mùa đó; vạch ngang là trung bình của mùa đó.
4. **Nhìn vào đâu**: độ cao các vạch ngang từ ô này sang ô khác (hình dạng mùa vụ); độ dốc trong từng ô (mùa đó đang đổi).
5. **Kết luận** (mẫu): "Tháng nào cũng tăng từ năm trước sang năm sau; vạch ngang thấp mùa đông, cao mùa hè."

**Bẫy:** bước nhảy **giữa** hai ô, hoặc giữa hai nửa trong một ô, là ranh giới giữa hai mùa hay hai năm, không phải xu hướng trong
tháng. `statsmodels.graphics.tsaplots.month_plot` có tên "seasonal" nhưng vẽ subseries plot, và chỉ nhận dữ liệu tháng hoặc quý.

| Đọc đúng | Đọc sai |
|---|---|
| "Chênh giữa các vạch ngang là mùa vụ; độ dốc trong ô là mùa vụ đang đổi" | "Trong tháng 3 lượt thuê tăng dần từ đầu tới cuối tháng" (thật ra là hai năm nối nhau) |

**Ví dụ có số (buổi 4).** Subseries theo tháng của lượt thuê: trong **mọi** ô, nửa phải (2012) cao hơn nửa trái (2011), tổng tháng
gấp 1,41 (tháng 6) tới 2,57 lần (tháng 3).

## 4. Heatmap lịch

**Trả lời câu hỏi gì:** mỗi ô lịch (thứ × giờ, tháng × năm) thường có giá trị bao nhiêu; mùa vụ kép trên một hình (buổi 4).

**Cách đọc hình.**

1. **Trục ngang**: chiều lịch thứ nhất, ví dụ giờ 0 → 23.
2. **Trục dọc**: chiều lịch thứ hai, ví dụ thứ Hai → Chủ nhật. Kiểm quy ước đánh số thứ: `dayofweek` của pandas cho 0 = thứ Hai,
   nhiều bộ dữ liệu cho 0 = Chủ nhật.
3. **Ký hiệu**: màu ô là **trung bình** (hay tổng) của mọi mốc thuộc ô đó; thang màu bên cạnh cho đơn vị.
4. **Nhìn vào đâu**: cột sáng dọc (giờ cao điểm mọi ngày); dòng khác hẳn các dòng còn lại (ngày đặc biệt); ô sáng lẻ.
5. **Kết luận** (mẫu): "8h và 17h chỉ sáng vào ngày làm việc; cuối tuần sáng giữa ngày."

**Bẫy:** heatmap chỉ cho trung bình, không cho độ tản (ghép với boxplot, mục 5), và trung bình bị vài ngày lạ kéo lệch. Thang màu
không có chú giải thì không đọc được độ lớn. Tự dựng bằng `pivot_table` + `imshow` an toàn hơn các thư viện lịch (`july` 0.1.3 hỏng
với matplotlib 3.11).

| Đọc đúng | Đọc sai |
|---|---|
| "Cuối tuần nhu cầu dời từ giờ đi làm sang giữa ngày" | "17h thứ Sáu (492) thấp hơn thứ Ba (544) nên thứ Sáu ít người đi" (chưa xem độ tản) |

**Ví dụ có số (buổi 4).** Lượt thuê trung bình mỗi giờ: 8h thứ Tư 488 so với 8h Chủ nhật 84; 13h thứ Hai 206 so với 13h thứ Bảy
385.

## 5. Boxplot theo mùa

**Trả lời câu hỏi gì:** mỗi nhóm lịch (giờ, thứ, tháng) có mức **và** độ tản ra sao; giờ nào khó dự báo; hai nhóm có chồng lên nhau
không (buổi 4).

**Cách đọc hình.**

1. **Trục ngang**: các nhóm, ví dụ giờ 0 → 23; có thể hai hộp cạnh nhau cho hai loại ngày.
2. **Trục dọc**: giá trị, cùng đơn vị với chuỗi.
3. **Ký hiệu**: hộp đi từ quantile 0,25 tới 0,75 (dài bằng IQR); vạch trong hộp là trung vị; râu tới giá trị xa nhất còn cách mép
   hộp không quá 1,5 × IQR; chấm ngoài râu (nếu vẽ) là điểm xa.
4. **Nhìn vào đâu**: hộp cao nhất (mức), hộp dài nhất (tản nhất), hai hộp cùng nhóm có chồng nhau không.
5. **Kết luận** (mẫu): "Giờ cao điểm cũng là giờ tản nhất; lúc 8h hai loại ngày gần như không chồng lên nhau."

**Bẫy:** dữ liệu lớn mà bật `showfliers=True` thì hàng nghìn chấm che hộp. So hai nhóm khác cỡ mẫu mà không nói số quan sát mỗi nhóm.
seaborn 0.13 với matplotlib 3.11 phát cảnh báo `vert` (vô hại; dùng `ax.boxplot` thì không có).

| Đọc đúng | Đọc sai |
|---|---|
| "Hộp 17h dài nhất → giờ khó dự báo nhất dù trung bình rõ" | "Trung vị 17h cao nhất → dự báo 17h dễ nhất" |

**Ví dụ có số (buổi 4).** Ngày làm việc lúc 17h: trung vị 539, hộp 348–704 (dài khoảng 356 lượt). Ngày nghỉ lúc 8h: trung vị 94,
so với 463 của ngày làm việc; hai hộp không chồng nhau.

## 6. Scatter và ma trận scatter

**Trả lời câu hỏi gì:** hai đại lượng liên quan với nhau thế nào: hình dạng, độ mạnh, cụm, điểm lạ. Ma trận scatter xem mọi cặp
biến cùng lúc (buổi 4, buổi 8).

**Cách đọc hình.**

1. **Trục ngang**: biến thứ nhất (thường là biến dùng để đoán), có đơn vị.
2. **Trục dọc**: biến thứ hai (biến cần đoán), có đơn vị.
3. **Ký hiệu**: mỗi chấm là một mốc thời gian; màu, nếu có, là thời gian (năm) hay nhóm.
4. **Nhìn vào đâu**: hình dạng đám chấm (thẳng, cong, chữ U); các cụm theo màu; chấm lẻ xa đám đông.
5. **Kết luận** (mẫu): "Cùng nhiệt độ, 2012 cao hơn 2011: quan hệ dời theo năm, tương quan gộp thấp hơn từng năm."

**Bẫy:**

- Hệ số tương quan $r$ chỉ đo quan hệ **đường thẳng** và có thể đánh lừa (FPP §2.6). Bộ tứ Anscombe: bốn tập dữ liệu cùng $r$ ≈
  0,82 mà hình dạng khác hẳn nhau.
- **Hai chuỗi cùng có xu hướng** cho đám chấm thẳng hàng dù không liên quan (tương quan giả, buổi 8).
- **Trộn nhiều năm** có mức khác nhau làm quan hệ trông yếu hơn: tô màu theo thời gian.
- **Chồng chấm** khi dữ liệu nhiều: dùng chấm trong suốt để vùng dày hiện đậm hơn (Wilke, chương 18).

| Đọc đúng | Đọc sai |
|---|---|
| "Đám chấm hình chữ U: $r$ thấp nhưng hai biến phụ thuộc mạnh" | "$r$ = 0,1 → hai biến không liên quan" |
| "Cả hai chuỗi đều tăng theo thời gian; sai phân rồi mới xét tương quan" | "$r$ = 0,95 → biến này dự báo được biến kia" |

**Ví dụ có số.** Buổi 4: nhiệt độ × lượt thuê ngày, tương quan từng năm 0,771 và 0,714 nhưng gộp hai năm chỉ 0,627. Buổi 8: CPI-U
× dân số Mỹ 420 tháng có $r$ = 0,974 trên mức, còn −0,207 sau sai phân. Nhiệt độ × tải điện ERCOT 2024: $r$ = 0,616; chia theo
ngưỡng 18,33 °C thì −0,649 (ngày lạnh) và +0,910 (ngày nóng), tức hình chữ V.

## 7. Lag plot

**Trả lời câu hỏi gì:** giá trị cách $k$ bước về trước đoán giá trị hiện tại tốt tới đâu (buổi 4).

**Cách đọc hình.**

1. **Trục ngang**: giá trị lúc $t - k$ (mỗi ô một $k$).
2. **Trục dọc**: giá trị lúc $t$, cùng thang với trục ngang.
3. **Ký hiệu**: mỗi chấm là một cặp $(y_{t-k}, y_t)$; đường chéo là "$y_t = y_{t-k}$"; tiêu đề ô thường ghi $r$.
4. **Nhìn vào đâu**: độ hẹp của đám chấm quanh đường chéo; đám chấm có tách nhánh không.
5. **Kết luận** (mẫu): "Trễ một tuần bám đường chéo nhất; trễ nửa ngày tách hai nhánh vì đỉnh ghép với đáy."

**Bẫy:** chuỗi có xu hướng cho đám chấm theo đường chéo ở **mọi** trễ, không phải dấu hiệu mùa vụ. $r$ âm ở trễ bằng nửa chu kỳ mùa vụ là
đỉnh ghép với đáy, không phải một quan hệ âm dùng được.

**Ví dụ có số (buổi 4).** Lượt thuê theo giờ: trễ 1 có $r$ = 0,843; trễ 12 có $r$ = −0,144 với hai nhánh bám hai trục; trễ 24 là
0,819; trễ 168 là 0,876, bám đường chéo chặt nhất.

## 8. ACF

**Trả lời câu hỏi gì:** chuỗi giống chính nó ở các độ trễ tới mức nào; có mùa vụ ở chu kỳ nào; có xu hướng không (buổi 4, buổi 7).
Hệ số tự tương quan ở trễ $k$ (FPP §2.8):

$$
r_k = \frac{\sum_{t=k+1}^{T} (y_t - \bar y)(y_{t-k} - \bar y)}{\sum_{t=1}^{T} (y_t - \bar y)^2}
$$

- $T$: số điểm; $\bar y$: trung bình của chuỗi; $y_t - \bar y$: độ lệch của điểm $t$ khỏi trung bình.

**Nói bằng lời.** Cộng các tích "độ lệch bây giờ × độ lệch $k$ bước trước", chia cho tổng bình phương độ lệch. Chuỗi 2, 4, 6, 4, 2,
4, 6, 4 có trung bình 4, mẫu số 16, tử số trễ 2 là −12, nên $r_2 = -0{,}75$: cao thì hai bước sau thấp.

**Cách đọc hình.**

1. **Trục ngang**: độ trễ $k$ (đơn vị bước: giờ, ngày, tháng).
2. **Trục dọc**: $r_k$, từ −1 tới 1.
3. **Ký hiệu**: mỗi vạch là một $r_k$; dải mờ quanh 0 là vùng một chuỗi hoàn toàn ngẫu nhiên thường rơi vào (FPP: ±1,96/√T).
4. **Nhìn vào đâu**: vạch cao ở đâu (bội số của chu kỳ mùa vụ); các vạch giảm nhanh hay giảm chậm; vạch nào vượt dải.
5. **Kết luận** (mẫu): "Đỉnh mỗi 24 giờ và đỉnh ở 168 cao hơn các đỉnh cạnh: mùa vụ ngày lồng mùa vụ tuần."

**Đọc hình dạng (FPP):**

- **Xu hướng**: $r_k$ dương, giảm chậm khi $k$ tăng.
- **Mùa vụ**: $r_k$ lớn ở bội số của chu kỳ mùa vụ.
- **Cả hai**: giảm chậm do xu hướng, hình "vỏ sò" do mùa vụ.
- **Nhiễu trắng** (chuỗi ngẫu nhiên, không có quy luật): khoảng 95% số vạch nằm trong dải. Một vài vạch vượt thì chưa nói lên gì;
  nhiều hơn hẳn 5% số vạch vượt, hoặc một vạch vượt rất xa, thì chuỗi có lẽ không phải nhiễu trắng.

**Bẫy:**

- Xem 40 trễ thì khoảng 2 vạch vượt dải chỉ do ngẫu nhiên: **một vạch vượt chưa chứng minh gì** (buổi 7 dùng kiểm định Ljung-Box).
- Dữ liệu dài ($T$ lớn) làm dải rất hẹp, gần như mọi vạch đều vượt: đọc hình dạng, đừng đếm vạch.
- **Dải của statsmodels khác dải của FPP:** `plot_acf` mặc định `bartlett_confint=True`, dải **rộng dần** theo trễ khi chuỗi có tự
  tương quan. Đo với $T$ = 100 (statsmodels 0.15.0, seed 1): AR(1) $\phi$ = 0,8 có nửa độ rộng 0,196 ở trễ 1 nhưng 0,300 ở trễ 5. So
  hình trong sách với hình của mình thì kiểm tuỳ chọn này trước.
- ACF giảm chậm trước hết là dấu hiệu **không dừng** hay có xu hướng (FPP §9.1): sai phân rồi đọc lại.

| Đọc đúng | Đọc sai |
|---|---|
| "Vạch cao ở 24, 48, 168 → mùa vụ ngày và tuần" | "Vạch ở trễ 13 vượt dải → có chu kỳ 13 giờ" (1 vạch trong 40 là bình thường) |
| "ACF giảm rất chậm → sai phân trước khi chọn mô hình" | "ACF giảm chậm → cần mô hình dùng 20 giá trị quá khứ" |

**Ví dụ có số.** Buổi 4: lượt thuê theo giờ $r_{24}$ = 0,813, $r_{144}$ = 0,786, $r_{168}$ = 0,864; dải ±0,015 với $T$ = 17.379. Buổi 7:
mô phỏng 1.000 chuỗi nhiễu trắng, xem 20 trễ: trung bình 0,95 vạch vượt dải, và 62% số chuỗi có ít nhất một vạch vượt.

## 9. Hình gây hiểu nhầm

**Trả lời câu hỏi gì:** hình này có đang nói nhiều hơn (hay khác) dữ liệu không (buổi 4).

**Cách đọc hình.**

1. **Trục ngang**: có bị chọn một đoạn thời gian "đẹp" không.
2. **Trục dọc**: bắt đầu từ đâu; có **hai** trục dọc không; thang thường hay log.
3. **Ký hiệu**: đường nào theo trục nào; có diện tích tô không.
4. **Nhìn vào đâu**: chỗ hai đường cắt hay đè nhau; độ cao cột thấp nhất so với đáy trục.
5. **Kết luận** (mẫu): "Sự trùng khít là do chọn thang trục phải; trục trái cắt ở 90.000 phóng to mức tăng."

| Lỗi | Vì sao sai | Sửa |
|---|---|---|
| **Biểu đồ cột có trục dọc không từ 0** | độ dài cột mã hoá giá trị (Wilke, chương 3) | trục từ 0; muốn nhấn chênh lệch nhỏ thì dùng chấm hay đường |
| **Diện tích tô dưới đường với trục cắt** | diện tích phải tỷ lệ với giá trị (Wilke) | bỏ tô, hoặc trục từ 0 |
| **Đường hoặc chấm với trục không từ 0** | chấp nhận được với đại lượng mức như nhiệt độ (Few) | ghi rõ thang trên trục; chọn phạm vi theo độ lớn thay đổi có ý nghĩa |
| **Hai trục dọc** | chỗ hai đường cắt nhau không có nghĩa gì, vì thang trục thứ hai do người vẽ chọn (Few 2008) | hai hình xếp dọc cùng trục thời gian, hoặc đánh chỉ số về cùng mốc 100 |
| **Tỷ lệ khung hình tuỳ ý** | khung hẹp cao làm dốc trông dữ hơn, khung rộng thấp làm phẳng đi | chọn tỷ lệ để độ dốc trung bình các đoạn khoảng 45° (Cleveland; Heer & Agrawala 2006) |
| **Chồng chấm** | vùng dày trông như vùng thưa | chấm trong suốt, hoặc hexbin (đếm chấm theo ô lục giác, tô màu theo số đếm); rung chấm (jitter) phải cẩn thận vì làm đổi dữ liệu (Wilke) |

**Đọc bảng.** Cột "Sửa" cho thấy phần lớn lỗi sửa được mà không bỏ dữ liệu: đổi trục, tách hình, đánh chỉ số. Trục cắt vẫn gây phóng
đại **kể cả khi** hình có ký hiệu báo trục bị cắt (Correll và cộng sự, 2020), nên đừng dựa vào ký hiệu đó. Few cũng không khẳng định
trục kép luôn vô dụng; nhưng trong khoá này, mọi hình hai trục dọc phải vẽ lại thành hai hình trước khi rút kết luận.

**Ví dụ có số (buổi 4).** Lượt thuê tháng 2012 trên trục trái 90.000–220.000 và nhiệt độ trên trục phải 5–32 °C: hai đường gần
trùng. Vẽ lại thành scatter: $r$ = 0,91 qua 12 tháng, nhưng tháng 9 (25,4 °C) có lượt thuê cao nhất năm trong khi tháng 7 nóng nhất
(30,8 °C).

## 10. Biểu đồ phân rã

**Trả lời câu hỏi gì:** chuỗi gồm bao nhiêu phần xu hướng, bao nhiêu mùa vụ, bao nhiêu phần còn lại (buổi 6).

**Cách đọc hình.**

1. **Trục ngang**: thời gian, chung cho mọi hàng.
2. **Trục dọc**: mỗi hàng một thành phần (dữ liệu, xu hướng, mùa vụ, phần dư), cùng đơn vị với chuỗi. Các hàng thường có
   **thang khác nhau**.
3. **Ký hiệu**: một đường mỗi hàng; có mô hình vẽ nhiều hàng mùa vụ (một hàng cho mỗi chu kỳ).
4. **Nhìn vào đâu**: độ cao hàng mùa vụ so với hàng phần dư (đọc số trên trục, không nhìn độ cao hình); phần dư còn lặp lại gì không.
5. **Kết luận** (mẫu): "Mùa vụ ngày chiếm phần lớn dao động; phần dư còn nhịp tuần, nên phân rã đã bỏ sót mùa vụ tuần."

**Đọc thêm:** phân rã **cộng** hợp khi dao động mùa vụ không đổi theo mức; khi dao động tỷ lệ với mức thì dùng phân rã **nhân**,
hoặc lấy log trước (FPP §3.2, buổi 5). Phần dư phải trông như nhiễu; còn cấu trúc lặp nghĩa là phân rã bỏ sót một mùa vụ.

**Bẫy:** mỗi hàng một thang, nên thành phần trông "to" chưa chắc lớn. FPP không khuyến nghị phân rã cổ điển (classical
decomposition).

**Ví dụ có số (buổi 6, tải điện PJM 2024).** Phân rã cổ điển chu kỳ 24 đẩy nhịp tuần vào **xu hướng** (trung bình xu hướng thứ Tư
95.036 MW so với Chủ nhật 88.459 MW); phần dư còn mùa vụ ngày đổi theo mùa (tỷ lệ phương sai 0,102, còn MSTL với chu kỳ 24 và 168
chỉ 0,0006). Một giờ số liệu hỏng (21/11/2024) làm mùa vụ ngày của cả tuần lệch khoảng 6.200 MW nếu không bật `robust`.

## 11. PACF

**Trả lời câu hỏi gì:** giá trị $k$ bước trước còn cho thêm thông tin gì **sau khi** đã biết các giá trị ở trễ 1 … $k - 1$
(buổi 7, buổi 17).

**Cách đọc hình.**

1. **Trục ngang**: độ trễ $k$.
2. **Trục dọc**: hệ số tự tương quan riêng phần, từ −1 tới 1.
3. **Ký hiệu**: mỗi vạch một trễ; dải ±1,96/√T như ACF.
4. **Nhìn vào đâu**: vạch cuối cùng vượt dải, và ACF cùng lúc giảm dần hay cắt đột ngột.
5. **Kết luận** (mẫu): "PACF cắt sau trễ 1, ACF giảm dần: dạng AR(1)."

**Quy tắc của FPP (§9.5, chỉ cho mô hình thuần):** dạng AR bậc $p$ thì ACF giảm dần, PACF có vạch vượt dải tới trễ $p$ rồi hết. Dạng
MA bậc $q$ thì ngược lại: PACF giảm dần, ACF cắt sau trễ $q$.

**Bẫy:** khi cả hai thành phần cùng có ($p$ và $q$ đều dương), FPP ghi rõ hình không giúp chọn bậc: dùng tiêu chí thông tin và kiểm
phần dư (buổi 17). `pacf()` mặc định `method="ywadjusted"` còn `plot_pacf()` mặc định `method="ywm"`: bảng số và hình có thể lệch
nhau, nên khai `method` rõ ràng.

**Ví dụ có số (buổi 7).** PACF ở trễ 1 và 2: nhiễu trắng 0,099 và −0,009; AR(1) φ = 0,7 là 0,713 và −0,110 (cắt sau trễ 1); random
walk 0,976 và −0,091.

## 12. CCF

**Trả lời câu hỏi gì:** chuỗi $x$ có **đi trước** chuỗi $y$ không, đi trước mấy bước (buổi 8).

**Cách đọc hình.**

1. **Trục ngang**: độ trễ, âm và dương. Đọc tài liệu hàm để biết trễ dương nghĩa là $x$ đi trước hay đi sau.
2. **Trục dọc**: tương quan giữa $x$ và $y$ ở độ trễ đó, từ −1 tới 1.
3. **Ký hiệu**: mỗi vạch một trễ; dải ±2/√n.
4. **Nhìn vào đâu**: vị trí vạch cao nhất (độ trễ dẫn dắt), dấu của nó, và đỉnh hẹp hay rộng.
5. **Kết luận** (mẫu): "Sau khi lọc tự tương quan, đỉnh ở trễ 0: nhiệt độ tác động ngay trong giờ, không đi trước."

**Bẫy:**

- **Quy ước trễ ngược nhau giữa các hàm:** `statsmodels.tsa.stattools.ccf(a, b)[k]` là tương quan giữa $a_{t+k}$ và $b_t$; muốn "$x$
  dẫn $y$" phải gọi `ccf(y, x)`. Luôn kiểm bằng chuỗi mô phỏng $y_t = x_{t-3}$ (đỉnh phải ở trễ 3).
- **Chưa lọc tự tương quan (prewhitening):** CCF thô mang cấu trúc tự tương quan của chính $x$ nên đỉnh rộng và có đỉnh giả.

**Ví dụ có số (buổi 8).** Chỉ số nóng (CDD) × tải điện ERCOT: CCF thô có đỉnh ở trễ 1 (0,863) và vẫn 0,828 ở trễ 24; sau
prewhitening đỉnh về trễ 0 (0,205) và trễ 24 còn 0,061, với dải 0,021.

## 13. Tương quan trượt

**Trả lời câu hỏi gì:** quan hệ giữa hai chuỗi có **ổn định** qua thời gian không, đổi dấu ở đâu (buổi 8).

**Cách đọc hình.**

1. **Trục ngang**: thời gian, thường là ngày **cuối** của mỗi cửa sổ.
2. **Trục dọc**: $r$ tính trên cửa sổ đó, từ −1 tới 1.
3. **Ký hiệu**: mỗi đường một độ dài cửa sổ (ví dụ 30 và 90 ngày).
4. **Nhìn vào đâu**: chỗ đường cắt 0 (đổi dấu); khoảng dao động của đường.
5. **Kết luận** (mẫu): "Tương quan âm vào mùa đông, dương vào mùa hè: một con số cả năm che mất hai chế độ."

**Bẫy:** cửa sổ theo thời gian (`rolling("90D")`) mặc định `min_periods=1`, nên vài giá trị đầu là ±1 giả. Cửa sổ quá ngắn cho dao
động ngẫu nhiên lớn; cửa sổ dài thì trơn nhưng phản ứng chậm.

**Ví dụ có số (buổi 8).** Nhiệt độ × tải điện ERCOT theo ngày: cả năm $r$ = 0,616; cửa sổ 90 ngày chạy từ −0,801 (kết thúc 31/3/2024)
tới +0,968 (kết thúc 14/10/2024).

## 14. Periodogram

**Trả lời câu hỏi gì:** chuỗi lên xuống theo những nhịp nào, nhịp nào mạnh nhất (buổi 12).

**Cách đọc hình.**

1. **Trục ngang**: tần số, số vòng lặp trên một bước; đổi ra chu kỳ bằng 1 / tần số. Chuỗi cách đều chỉ thấy tần số từ 0 tới 0,5
   (chu kỳ ngắn nhất là 2 bước) (NIST).
2. **Trục dọc**: độ mạnh của nhịp đó (công suất), thường thang log.
3. **Ký hiệu**: một đường qua mọi tần số; đỉnh là nhịp mạnh.
4. **Nhìn vào đâu**: đỉnh cao nhất, và các đỉnh ở bội số của nó (hài).
5. **Kết luận** (mẫu): "Đỉnh ở tần số 1/24 (chu kỳ 24 giờ) và 1/168 (một tuần)."

**Bẫy:** xu hướng dồn năng lượng vào tần số thấp, che các đỉnh khác: bỏ xu hướng trước (NIST). Nhịp ngắn hơn 2 bước lấy mẫu không thấy
được, và có thể giả dạng thành một tần số khác (aliasing, buổi 12).

## 15. QQ-plot

**Trả lời câu hỏi gì:** dữ liệu (thường là phần dư) có gần phân phối chuẩn không, đuôi dài hay ngắn, lệch về phía nào (buổi 2, buổi 25).

**Cách đọc hình.**

1. **Trục ngang**: quantile lý thuyết của phân phối chuẩn (dạng NIST). Một số thư viện đổi hai trục cho nhau: đọc nhãn trước.
2. **Trục dọc**: quantile của dữ liệu, tức dữ liệu xếp tăng dần.
3. **Ký hiệu**: mỗi chấm là một giá trị; đường thẳng là chỗ chấm sẽ nằm nếu dữ liệu đúng là chuẩn.
4. **Nhìn vào đâu**: hai đầu (đuôi) và giữa có cong khỏi đường thẳng không.
5. **Kết luận** (mẫu): "Hai đầu lệch khỏi đường: đuôi dài, khoảng ±1,96s sẽ hẹp quá ở đuôi."

**Đọc hình dạng (NIST, trục dọc là dữ liệu):** chấm gần đường thẳng là gần chuẩn. **Đuôi dài**: vài chấm đầu nằm dưới đường, vài chấm
cuối nằm trên; đuôi ngắn thì ngược lại. **Lệch phải**: chấm cong như một chiếc bát, mọi chấm nằm dưới đoạn nối chấm đầu và chấm cuối;
nằm trên là lệch trái.

**Bẫy:** đổi hai trục thì mọi quy tắc trên đảo ngược.

## 16. Fan chart

**Trả lời câu hỏi gì:** tương lai có thể rơi vào đâu, và bất định lớn dần thế nào theo tầm dự báo (buổi 25).

**Cách đọc hình.**

1. **Trục ngang**: thời gian; vạch đứng đánh dấu gốc dự báo.
2. **Trục dọc**: giá trị, cùng đơn vị với chuỗi.
3. **Ký hiệu**: dải đậm ở giữa là vùng khả năng cao nhất; mỗi dải nhạt hơn thêm một phần xác suất. Chú giải phải nói dải nào là
   quantile nào.
4. **Nhìn vào đâu**: độ rộng dải ở tầm gần và tầm xa; dải có lệch về một phía không.
5. **Kết luận** (mẫu): "Dải 90% rộng gấp ba ở tầm 12 so với tầm 1; lệch lên trên: rủi ro tăng lớn hơn rủi ro giảm."

**Bẫy:** mép ngoài của dải **không** phải "giá trị lớn nhất có thể". Chính Ngân hàng Trung ương Anh ghi nhận kiểu dải cũ hay bị đọc
nhầm thành cận trên và cận dưới (Britton, Fisher & Whitley 1998). Dải của họ dựng từ giá trị hay gặp nhất (mode) ra ngoài, nên không
trùng khoảng quantile 5%–95% mà thư viện dự báo thường vẽ.

## 17. PIT histogram và rank histogram

**Trả lời câu hỏi gì:** dự báo phân phối có **hiệu chỉnh tốt** không, tức các khoảng dự báo có đúng độ rộng không (buổi 25).

Với mỗi dự báo phân phối $F_t$ và giá trị thật $y_t$, **PIT** là $p_t = F_t(y_t)$: tỷ lệ của phân phối dự báo nằm dưới giá trị thật.
Ví dụ dự báo nói "80% khả năng dưới 50", thật ra 50, thì PIT = 0,8.

**Cách đọc hình.**

1. **Trục ngang**: giá trị PIT, từ 0 tới 1, chia ô đều nhau.
2. **Trục dọc**: số lần (hay tỷ lệ) PIT rơi vào mỗi ô.
3. **Ký hiệu**: cột histogram; đường ngang là độ cao các cột nếu dự báo lý tưởng (phẳng).
4. **Nhìn vào đâu**: hình dạng chung: phẳng, chữ U, vòm, hay lệch một phía.
5. **Kết luận** (mẫu): "Hình chữ U: khoảng dự báo quá hẹp, tỷ lệ phủ thật thấp hơn tỷ lệ ghi trên khoảng."

**Đọc hình dạng (Gneiting, Balabdaoui & Raftery 2007):** **vòm** là khoảng dự báo trung bình quá **rộng**; **chữ U** là quá **hẹp**,
quá tự tin; **tam giác, lệch một phía** là dự báo bị lệch (chệch) về một phía. Rank histogram của dự báo tập hợp (ensemble) đọc tương
tự: chữ U là các thành viên ensemble tản quá ít.

**Bẫy:** PIT phẳng là điều kiện **cần**, không **đủ**: một dự báo lúc nào cũng trả về phân phối của mọi năm trước có thể phẳng mà vô
dụng. Nguyên tắc của bài báo: khoảng càng hẹp càng tốt, **với điều kiện** đã hiệu chỉnh tốt.

| Đọc đúng | Đọc sai |
|---|---|
| "PIT chữ U → khoảng quá hẹp, tỷ lệ phủ thật thấp hơn danh nghĩa" | "PIT chữ U → khoảng quá rộng" |
| "PIT phẳng; giờ so độ hẹp của khoảng với mô hình khác" | "PIT phẳng → mô hình tốt nhất" |

## 18. Reliability diagram

**Trả lời câu hỏi gì:** khi dự báo nói "70% khả năng xảy ra", sự kiện có xảy ra khoảng 70% số lần không (buổi 25, buổi 37).

**Cách đọc hình.**

1. **Trục ngang**: xác suất dự báo, chia thành các ô (0–0,1, 0,1–0,2…).
2. **Trục dọc**: tỷ lệ sự kiện thật sự xảy ra trong các lần dự báo thuộc ô đó.
3. **Ký hiệu**: chấm nối nhau là từng ô; đường chéo là hiệu chỉnh hoàn hảo; histogram phụ (nếu có) là số lần dự báo mỗi ô.
4. **Nhìn vào đâu**: đường nằm trên hay dưới đường chéo; ô nào ít dự báo.
5. **Kết luận** (mẫu): "Đường nằm dưới đường chéo ở nửa phải: xác suất cao bị nói quá, sự kiện xảy ra ít hơn dự báo."

**Đọc hình dạng (WWRP/WGNE):** đường **dưới** đường chéo là dự báo xác suất quá cao; **trên** là quá thấp. Đường càng phẳng (gần
nằm ngang) thì dự báo càng ít phân biệt được lúc sự kiện dễ xảy ra với lúc khó xảy ra.

**Bẫy:** ô có ít dự báo cho chấm nhảy lung tung; cách chia ô làm đổi hình. Bröcker & Smith (2007) thêm **thanh nhất quán** bằng lấy
mẫu lại để biết độ lệch nào nằm trong dao động ngẫu nhiên.

## Nguồn

Truy cập ngày 2026-09-17 và 2026-09-18. Nhật ký research: `tools/NGHIEN-CUU.md`, `buoi-04/NGHIEN-CUU.md`.

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way* — chương 2
  <https://otexts.com/fpppy/02-graphics.html>, chương 3 <https://otexts.com/fpppy/03-decomposition.html>, chương 9
  <https://otexts.com/fpppy/09-arima.html>
- statsmodels `plot_acf` (tham số `bartlett_confint`):
  <https://www.statsmodels.org/stable/generated/statsmodels.graphics.tsaplots.plot_acf.html>
- NIST/SEMATECH e-Handbook — normal probability plot <https://www.itl.nist.gov/div898/handbook/eda/section3/normprpl.htm>;
  spectral plot <https://www.itl.nist.gov/div898/handbook/eda/section3/spectrum.htm>
- Gneiting, T., Balabdaoui, F. & Raftery, A.E. (2007). Probabilistic forecasts, calibration and sharpness. *JRSS B* 69(2), 243–268.
- WWRP/WGNE Joint Working Group on Forecast Verification Research — <https://www.cawcr.gov.au/projects/verification/>
- Bröcker, J. & Smith, L.A. (2007). Increasing the reliability of reliability diagrams. *Weather and Forecasting* 22(3), 651–661.
- Britton, E., Fisher, P. & Whitley, J. (1998). The Inflation Report projections: understanding the fan chart. *Bank of England
  Quarterly Bulletin*, Q1.
- Wilke, C.O. *Fundamentals of Data Visualization* — chương 3, 17, 18: <https://clauswilke.com/dataviz/>
- Few, S. (2008). Dual-scaled axes in graphs: are they ever the best solution? *Perceptual Edge*.
- Correll, M., Bertini, E. & Franconeri, S. (2020). Truncating the Y-Axis: Threat or Menace? *CHI 2020*.
- Heer, J. & Agrawala, M. (2006). Multi-scale banking to 45 degrees. *IEEE TVCG* 12(5).
- Cleveland, W.S., McGill, M.E. & McGill, R. (1988). The shape parameter of a two-variable graph. *JASA* 83, 289–300.
