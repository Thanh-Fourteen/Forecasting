# Phụ lục E — Từ điển thuật ngữ Anh–Việt

Chuẩn dùng từ cho **mọi** tài liệu của khoá. Gặp từ lạ khi học thì tra ở đây: mỗi dòng đủ để hiểu mà
không phải tra thêm. Khi soạn buổi mới mà gặp thuật ngữ chưa có ở đây: thêm vào đúng nhóm trước, rồi mới
dùng.

## Quy ước viết

1. **Giữ nguyên tiếng Anh** khi đó là tên phương pháp, tên chỉ số, hoặc từ mà người làm nghề ở Việt Nam
   dùng nguyên văn: *backtest, baseline, quantile, drift, feature, pipeline, seasonal naive, ACF*… Lần
   đầu xuất hiện trong một buổi thì kèm giải thích tiếng Việt.
2. **Dịch** khi tiếng Việt đã quen và không mơ hồ: *xu hướng* (trend), *mùa vụ* (seasonality), *phần dư*
   (residual), *ngoại lai* (outlier). Lần đầu trong buổi thì ghi kèm tiếng Anh trong ngoặc.
3. Mỗi bảng có đúng 5 cột:
   - **Tiếng Anh**: tên gốc, để tra tài liệu nước ngoài.
   - **Viết trong khoá**: dạng dùng trong câu. Không dùng lẫn hai dạng trong một buổi.
   - **Nói đơn giản**: 1–2 câu bằng lời thường. Nếu phải dùng một thuật ngữ khác thì từ đó có dòng
     riêng ở đây, ghi "xem …".
   - **Ví dụ**: ví dụ nhỏ, có số tính tay được.
   - **Buổi**: số đầu tiên là buổi gặp từ này lần đầu; các số sau là buổi học kỹ.
4. **Dấu của sai số**: sai số = thực tế − dự báo. Sai số dương nghĩa là dự báo thấp hơn thực tế.
5. Tên hàm, tham số, tên cột giữ đúng như trong code: `unique_id`, `ds`, `y`, `closed='left'`.
6. Công thức đầy đủ của chỉ số: Phụ lục D. Cách đọc biểu đồ: Phụ lục C. Xác suất: Phụ lục B.
7. Mỗi buổi có bảng "Từ mới trong buổi" lấy từ đây; gặp từ lạ trong buổi mà không có ở đây là lỗi của
   tài liệu — ghi vào `phan-hoi-hoc-vien.md`.

## Mục lục

- [1. Bài toán dự báo](#1-bài-toán-dự-báo)
- [2. Dữ liệu và thời gian](#2-dữ-liệu-và-thời-gian)
- [3. Mô tả chuỗi thời gian](#3-mô-tả-chuỗi-thời-gian)
- [4. Làm sạch, ngoại lai, khử nhiễu](#4-làm-sạch-ngoại-lai-khử-nhiễu)
- [5. Feature và rò rỉ](#5-feature-và-rò-rỉ)
- [6. Đánh giá](#6-đánh-giá)
- [7. Mô hình thống kê](#7-mô-hình-thống-kê)
- [8. Machine learning và deep learning](#8-machine-learning-và-deep-learning)
- [9. Bất định](#9-bất-định)
- [10. Foundation model và LLM](#10-foundation-model-và-llm)
- [11. Nhân quả và ra quyết định](#11-nhân-quả-và-ra-quyết-định)
- [12. Production](#12-production)
- [13. Xác suất thống kê](#13-xác-suất-thống-kê)

## 1. Bài toán dự báo

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| forecast | dự báo | Nói trước giá trị của tương lai, dựa trên thông tin có tới hôm nay. | Tối 19/9 đã biết tải điện các ngày trước; đoán tải cả ngày 20/9 là 950 MWh. | 1 |
| forecast horizon | tầm dự báo (horizon), $h$ | Dự báo xa bao nhiêu bước về phía trước. Bước 1 là kỳ ngay sau thời điểm ra dự báo. | Dữ liệu theo giờ, cần dự báo 24 giờ tới → $h$ = 1, 2, …, 24. | 1 |
| granularity | độ chi tiết | Dữ liệu được gộp tới mức nào: theo sản phẩm, theo nơi, theo khoảng thời gian. | "Từng món × từng cửa hàng × từng ngày" chi tiết hơn "cả chuỗi cửa hàng × từng tháng". | 1 |
| forecast origin / cutoff | mốc cắt dữ liệu (cutoff), gốc dự báo | Thời điểm ta đứng để ra dự báo. Mọi thứ sau mốc này coi như chưa biết. | Gốc là 00:00 thứ Hai 4/1 → chỉ được dùng dữ liệu tới 23:00 Chủ nhật 3/1. | 1, 15 |
| point forecast | dự báo điểm | Dự báo chỉ một con số cho mỗi thời điểm. | "Ngày mai bán 120 cái." | 1 |
| interval forecast | dự báo khoảng | Dự báo một khoảng, kèm mức chắc chắn rằng giá trị thật rơi vào khoảng đó. | "Ngày mai bán 100–140 cái, chắc 80%." | 1, 25 |
| probabilistic / distributional forecast | dự báo xác suất / dự báo phân phối | Dự báo mọi khả năng có thể xảy ra và xác suất của từng khả năng (xem phân phối). | "Dưới 100 cái: 10%; 100–140 cái: 80%; trên 140 cái: 10%." | 1, 25 |
| target | biến mục tiêu | Đại lượng ta cần dự báo. Trong code thường là cột `y`. | Dự báo tải điện từng giờ → biến mục tiêu là cột tải (MWh) của mỗi giờ. | 1 |
| noise | nhiễu | Phần lên xuống ngẫu nhiên không đoán trước được, chồng lên phần có quy luật. Cộng nhiều giờ lại thì nhiễu dương và âm bù trừ nhau. | Sai số hai giờ là +1 và −1 kWh: từng giờ đều sai 1, nhưng tổng hai giờ sai 0. | 1 |
| forward market / spot price | thị trường kỳ hạn / giá giao ngay | Kỳ hạn: mua trước, chốt giá hôm nay cho lượng dùng sau này. Giao ngay: mua ngay lúc cần, thường đắt hơn khi thiếu gấp. | Chủ nhật mua trước điện cho cả tuần; thiếu vào thứ Ba thì mua giao ngay với giá cao. | 1 |
| judgmental forecast | dự báo phán đoán | Dự báo dựa trên kinh nghiệm của con người, không dựa trên mô hình tính toán. | Trưởng kho nói: "Tết này bán gấp đôi tháng thường." | 1, 40 |
| nowcasting | nowcasting | Ước lượng con số của quý này hoặc tháng vừa qua khi số chính thức chưa công bố. | GDP quý 3 cuối tháng 10 mới công bố; nowcasting ước lượng nó ngay từ tháng 9 (xem GDP). | 20 |
| model | mô hình | Một cách tính cố định biến dữ liệu quá khứ thành dự báo. Có thể là một công thức hay một chương trình. | "Ngày mai = trung bình 7 ngày qua" là một mô hình đơn giản. | 1 |
| parameter | tham số | Con số bên trong mô hình, được chọn từ dữ liệu để mô hình khớp dữ liệu nhất. | Mô hình $\hat y = a + b\,t$ có hai tham số là $a$ và $b$. | 1 |
| fit | khớp (fit) | Tìm giá trị tham số của mô hình từ dữ liệu quá khứ. Trong code là lệnh `.fit()`. | Khớp $y = a + b\,t$ qua các điểm (1; 2), (2; 4), (3; 6) → $a$ = 0, $b$ = 2. | 1 |

## 2. Dữ liệu và thời gian

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| time series | chuỗi thời gian | Dãy số đo lần lượt theo thời gian, có thứ tự trước sau. | Nhiệt độ lúc 1h, 2h, 3h là 25, 24, 24 °C. | 1 |
| frequency | tần suất | Khoảng cách thời gian giữa hai lần đo liên tiếp. Đừng nhầm với tần số (xem tần số). | Đo mỗi giờ → tần suất giờ; mỗi tháng một số → tần suất tháng. | 1, 3 |
| regular / irregular series | chuỗi đều / chuỗi không đều | Chuỗi đều: các lần đo cách nhau bằng nhau. Chuỗi không đều: khoảng cách lúc dài lúc ngắn. | Đo lúc 1h, 2h, 3h là đều; đo lúc 1h, 1h20, 4h là không đều. | 3 |
| resample | resample (gộp / tách tần suất) | Đổi tần suất của chuỗi: gộp nhiều điểm thành một (giảm tần suất) hoặc chia ra (tăng). | 24 giờ, mỗi giờ 40 MWh → gộp thành 1 ngày: 24 × 40 = 960 MWh. | 1, 3 |
| time zone, UTC | múi giờ, UTC | UTC là giờ chuẩn quốc tế. Múi giờ cho biết giờ địa phương lệch UTC bao nhiêu giờ. | 7:00 sáng ở Hà Nội (UTC+7) là 0:00 UTC. | 1, 3 |
| naive / aware timestamp | timestamp naive / aware | Mốc thời gian không ghi múi giờ (naive) hoặc có ghi (aware). Chữ "naive" ở đây khác phương pháp naive. | `2024-03-10 02:00` là naive; `2024-03-10 02:00+07:00` là aware. | 3 |
| DST (daylight saving time) | giờ mùa hè (DST) | Một số nước vặn đồng hồ nhanh 1 giờ vào mùa hè. Ngày chuyển có giờ bị mất hoặc bị lặp. | Ở Mỹ ngày 10/3/2024 không có giờ 2:00–2:59, nên ngày đó chỉ có 23 giờ. | 3 |
| long / wide format | định dạng dài / định dạng rộng | Dạng dài: mỗi dòng một quan sát (`unique_id, ds, y`). Dạng rộng: mỗi chuỗi một cột. | 2 cửa hàng × 3 ngày: dạng dài có 6 dòng; dạng rộng có 3 dòng × 2 cột số. | 3 |
| as-of join | ghép as-of | Ghép mỗi dòng với giá trị gần nhất đã có trước (hoặc đúng) thời điểm của dòng đó. Trong pandas là `merge_asof`. | Đơn hàng lúc 10:07 ghép với giá cập nhật lúc 10:05, không lấy giá lúc 10:10. | 3, 41 |
| vintage | vintage (bản công bố) | Số liệu đúng như lúc được công bố, trước những lần sửa sau đó. | Tháng 7 công bố doanh số tăng 2,0%; tháng 8 sửa thành 1,6%. Con số 2,0% thuộc vintage tháng 7. | 13, 20, 41 |
| point-in-time | point-in-time | Chỉ dùng dữ liệu đã thật sự có vào lúc ra dự báo, đúng con số lúc đó, kể cả khi sau này bị sửa. | Dự báo ngày 1/8 dùng số "tăng 2,0%", không dùng số sửa 1,6% công bố ngày 1/9. | 13, 41 |
| revision (data) | sửa số liệu lùi | Nguồn số liệu công bố lại giá trị của quá khứ sau khi có thông tin đầy đủ hơn. | GDP quý 1 công bố lần đầu +1,3%; một tháng sau sửa thành +1,1%. | 13, 20, 41 |
| sha256 | sha256 | Dấu vân tay của một tệp. Tệp đổi dù chỉ một byte thì sha256 đổi hẳn. | Tải tệp về, so 12 ký tự đầu (`26768c495c3b`) với danh mục; khác là tệp hỏng hoặc bị đổi. | 1 (dùng ở mọi buổi) |
| power (kW, MW, GW) | kW, MW, GW (công suất) | Công suất là điện được dùng mạnh cỡ nào tại một lúc. 1 MW = 1.000 kW; 1 GW = 1.000 MW. | Ấm đun nước 2 kW; một nhà máy 600 MW; cả vùng lúc cao điểm 70 GW. | 1 |
| energy (kWh, MWh) | kWh, MWh (điện năng) | Điện năng là tổng điện đã dùng trong một khoảng thời gian: công suất × số giờ. Đừng nhầm với công suất. | Ấm 2 kW chạy 3 giờ → 2 × 3 = 6 kWh. Tải 500 MW suốt 1 giờ = 500 MWh. | 1 |
| GDP (gross domestic product) | GDP (tổng sản phẩm quốc nội) | Tổng giá trị hàng hoá và dịch vụ một nước làm ra trong một kỳ. Thường công bố theo quý. | GDP quý này 105, quý trước 100 → tăng (105 − 100)/100 = 5%. | 7 |
| CPI (consumer price index) | CPI (chỉ số giá tiêu dùng) | Con số theo dõi giá một giỏ hàng tiêu dùng, lấy năm gốc bằng 100. Dùng để bỏ ảnh hưởng của lạm phát. | CPI từ 100 lên 110 → giá chung tăng 10%; 110 nghìn đồng hôm nay ≈ 100 nghìn đồng năm gốc. | 5 |
| COVID | COVID (đại dịch 2020–2022) | Đại dịch làm nhiều chuỗi kinh tế, đi lại, bán lẻ gãy đột ngột từ năm 2020. Khi phân tích thường phải đánh dấu hoặc tách riêng đoạn này. | GDP thực của Mỹ quý 2/2020 giảm khoảng 8% so với quý 1 (buổi 7). | 5, 11 |

## 3. Mô tả chuỗi thời gian

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| trend | xu hướng | Hướng đi lâu dài của chuỗi: đi lên, đi xuống hay đi ngang, bỏ qua dao động ngắn. | Doanh số các năm 100, 104, 108, 112 → xu hướng tăng 4 mỗi năm. | 2, 4, 6 |
| seasonality | mùa vụ | Mẫu lặp lại đều theo lịch, với chu kỳ cố định và biết trước. | Tải điện cao lúc 19h, thấp lúc 3h, ngày nào cũng vậy → mùa vụ theo ngày. | 1, 4, 6 |
| seasonal period, $m$ | chu kỳ mùa vụ, $m$ | Số bước dữ liệu trước khi mẫu mùa vụ lặp lại. | Dữ liệu giờ lặp theo ngày → $m$ = 24. Dữ liệu ngày lặp theo tuần → $m$ = 7. | 4, 5 |
| multiple seasonality | mùa vụ kép / đa mùa vụ | Chuỗi có nhiều mẫu lặp cùng lúc, mỗi mẫu một chu kỳ. | Tải điện theo giờ lặp theo ngày ($m$ = 24) và theo tuần ($m$ = 168). | 4, 6, 18 |
| cycle | chu kỳ | Dao động lên xuống kéo dài nhiều năm, độ dài không cố định. Khác mùa vụ ở chỗ không biết trước. | Kinh tế tăng trưởng 6 năm rồi suy thoái; lần sau lại tăng 9 năm. | 4 |
| level shift | dịch mức | Mức trung bình của chuỗi đổi đột ngột rồi giữ luôn ở mức mới. Có chỗ trong khoá viết là "đổi mức". | Trước 1/3 bán quanh 100 cái/ngày; từ 1/3 mở thêm quầy, bán quanh 130 cái/ngày. | 1, 11 |
| structural break / changepoint | điểm gãy | Thời điểm cách chuỗi vận hành thay đổi, nên dữ liệu trước và sau mốc đó không giống nhau. | Mức bán nhảy từ 100 lên 130 cái/ngày vào ngày 1/3 → 1/3 là điểm gãy. | 6, 11 |
| decomposition (additive / multiplicative) | phân rã (cộng / nhân) | Tách chuỗi thành xu hướng, mùa vụ và phần dư. Kiểu cộng: ba phần cộng lại; kiểu nhân: ba phần nhân lại. | Cộng: 120 = 100 (xu hướng) + 15 (mùa vụ) + 5 (dư). Nhân: 115 = 100 × 1,15 × 1. | 5, 6 |
| STL, MSTL | STL, MSTL | Cách phân rã dùng LOESS (xem LOESS), chịu được ngoại lai. MSTL tách được nhiều mùa vụ cùng lúc. | MSTL tách tải điện giờ thành xu hướng + mùa vụ ngày + mùa vụ tuần + phần dư. | 6 |
| remainder / residual | phần dư | Phần còn lại sau khi trừ xu hướng và mùa vụ, hoặc sau khi trừ giá trị mô hình khớp được. | Thật 120, xu hướng 100, mùa vụ 15 → phần dư = 120 − 100 − 15 = 5. | 1, 6, 17 |
| autocorrelation, ACF | tự tương quan, ACF | Tương quan của chuỗi với chính nó dời lùi $k$ bước (xem tương quan, trễ). ACF là dãy các giá trị đó theo $k$. | Chuỗi lên xuống xen kẽ 1, 3, 1, 3 → tự tương quan trễ 1 = −0,75. | 2, 7 |
| partial autocorrelation, PACF | tự tương quan riêng phần, PACF | Tương quan giữa hôm nay và $k$ bước trước, sau khi đã bỏ phần ảnh hưởng truyền qua các bước ở giữa. | Nếu $y_t = 0{,}7\,y_{t-1}$ + nhiễu thì ACF trễ 2 ≈ 0,49 nhưng PACF trễ 2 ≈ 0. | 7 |
| lag | trễ | Giá trị của chuỗi $k$ bước trước, viết $y_{t-k}$. | Chuỗi 5, 7, 6, 9: tại bước 4 (giá trị 9), trễ 1 là 6, trễ 2 là 7. | 1, 7 |
| white noise | nhiễu trắng | Chuỗi ngẫu nhiên thuần: trung bình không đổi, không tự tương quan, không có mẫu nào để khai thác. | Tung xúc xắc mỗi ngày: 3, 6, 1, 4… — số hôm qua không giúp đoán số hôm nay. | 7 |
| stationarity | tính dừng | Chuỗi dừng khi trung bình, độ dao động và tự tương quan không đổi theo thời gian. | Nhiệt độ lệch khỏi mức bình thường của mùa: gần dừng. Giá nhà tăng dần 20 năm: không dừng. | 2, 7 |
| differencing | sai phân | Lấy mỗi giá trị trừ giá trị ngay trước ($y_t - y_{t-1}$), hoặc trừ giá trị cùng kỳ mùa trước ($y_t - y_{t-m}$). | 10, 12, 15, 15 → sai phân: 2, 3, 0. | 5, 7 |
| unit root | nghiệm đơn vị | Chuỗi có nghiệm đơn vị thì mỗi cú sốc ở lại mãi, chuỗi trôi đi không quay về mức cũ. Sai phân một lần thường khử được. | $y_t = y_{t-1}$ + nhiễu: đang ở 100, bị sốc +5 thì sau đó dao động quanh 105, không về 100. | 7 |
| unit root test (ADF, KPSS, PP) | kiểm định nghiệm đơn vị (ADF, KPSS) | Kiểm định xem chuỗi có nghiệm đơn vị không (xem kiểm định giả thuyết). ADF và PP giả định "không dừng", KPSS giả định "dừng". | ADF p = 0,01 → bác "không dừng"; KPSS p = 0,10 → không bác "dừng". Hai bên cùng nói: dừng. | 7 |
| cross-correlation, CCF | tương quan chéo, CCF | Tương quan giữa chuỗi X dời lùi $k$ bước và chuỗi Y, tính cho nhiều $k$ để tìm X đi trước Y bao lâu. | Quảng cáo tuần này, doanh số tuần sau mới tăng → CCF cao nhất ở trễ 1 tuần. | 8 |
| prewhitening | prewhitening | Lọc bỏ tự tương quan riêng của từng chuỗi trước khi tính CCF, để CCF không báo quan hệ giả. | Hai chuỗi đều tự tương quan mạnh → CCF thô cao ở mọi trễ; sau prewhitening chỉ còn đỉnh thật. | 8 |
| spurious correlation / regression | tương quan giả / hồi quy giả | Hai chuỗi cùng có xu hướng nên tương quan rất cao, dù thật ra không liên quan gì nhau. | CPI và dân số Mỹ: $r$ = 0,974; sau sai phân chỉ còn $r$ = −0,207 (buổi 8). | 8, 18 |
| Durbin–Watson statistic | Durbin–Watson (DW) | Con số từ 0 đến 4 cho biết phần dư của hồi quy có tự tương quan không. Gần 2 là ổn; gần 0 là phần dư bám nhau. | Hồi quy CPI theo dân số có DW = 0,005 → phần dư bám nhau cực mạnh → nghi hồi quy giả. | 8 |
| Granger causality | nhân quả Granger | X "gây ra Granger" Y nếu quá khứ của X giúp dự báo Y tốt hơn. Đây không phải nhân quả thật. | Số ô bán ra buổi sáng giúp đoán trời mưa buổi chiều, nhưng mua ô không gây ra mưa. | 8 |
| mutual information | mutual information (MI) | Đo hai biến phụ thuộc nhau nhiều cỡ nào, bắt được cả quan hệ cong mà tương quan bỏ sót. Bằng 0 khi hai biến độc lập. | $x$ = −2, −1, 0, 1, 2 và $y = x^2$: tương quan bằng 0 nhưng MI lớn hơn 0. | 8 |
| spectral entropy | spectral entropy | Đo phổ tần số "phẳng" tới đâu (xem periodogram). Gần 1: giống nhiễu, khó dự báo; gần 0: có nhịp rõ. | Sóng sin đều cho giá trị gần 0; nhiễu trắng cho giá trị gần 1. | 9 |
| forecastability | khả năng dự báo | Chuỗi có bao nhiêu cấu trúc (xu hướng, mùa vụ, tự tương quan) mà mô hình khai thác được. | Tải điện theo giờ (nhịp ngày rõ) dễ dự báo hơn doanh số từng ngày của một món hàng hiếm. | 9 |
| Box-Cox transformation | biến đổi Box-Cox | Họ phép biến đổi (log, căn, luỹ thừa) chọn bằng một số $\lambda$, làm độ dao động đều nhau ở mức thấp và mức cao. | $\lambda$ = 0 là lấy log. $\lambda$ = 0,5: 100 → $(\sqrt{100} - 1)/0{,}5$ = 18. | 5 |
| bias adjustment (back-transform) | hiệu chỉnh bias khi biến đổi ngược | Dự báo trên log rồi lấy exp thì ra trung vị, không ra trung bình. Nhân thêm một hệ số nhỏ để về trung bình. | Dự báo log 4,6, phương sai 0,04: exp(4,6) ≈ 99,5; nhân (1 + 0,04/2) ≈ 101,5. | 5 |
| moving average, MA | trung bình trượt (MA) | Trung bình của $k$ điểm liền nhau, trượt dần dọc chuỗi để làm trơn. Chữ MA trong ARIMA là khái niệm khác (buổi 17). | 3, 5, 4, 8, 6 → trung bình trượt 3 điểm: 4; 5,67; 6. | 4, 6, 12 |
| LOESS | LOESS | Làm trơn bằng cách khớp một đường thẳng riêng cho từng vùng nhỏ, điểm càng gần càng được coi trọng. | Ước lượng xu hướng tại tháng 6 chỉ dựa vào tháng 3–9, trong đó tháng 6 nặng ký nhất. | 6 |
| X-13ARIMA-SEATS | X-13ARIMA-SEATS (X-11, SEATS) | Phần mềm khử mùa vụ mà cơ quan thống kê dùng cho số liệu tháng và quý. | Con số "doanh số bán lẻ đã điều chỉnh mùa vụ" công bố hằng tháng thường tính bằng X-13. | 6 |
| PCA (principal component analysis) | PCA (phân tích thành phần chính), PC1, PC2 | Nén nhiều cột số thành 2–3 cột mới giữ được nhiều khác biệt nhất, để vẽ được lên mặt phẳng. | 10 đặc trưng mỗi chuỗi → PCA → 2 cột PC1, PC2 → mỗi chuỗi thành một chấm trên hình. | 9 |
| DTW (dynamic time warping) | DTW | Đo hai chuỗi giống nhau về hình dạng, cho phép co giãn trục thời gian để khớp đỉnh với đỉnh. | Hai đường giống hệt nhưng đỉnh lệch nhau 1 giờ: khoảng cách thường lớn, khoảng cách DTW gần 0. | 9 |
| ABC–XYZ classification (AX, CZ) | phân loại ABC–XYZ | Xếp mã hàng theo hai trục: ABC theo doanh thu (A lớn nhất), XYZ theo mức biến động (X ổn định nhất). | Ô AX: bán nhiều và đều. Ô CZ: bán ít và thất thường. | 9 |

## 4. Làm sạch, ngoại lai, khử nhiễu

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| missing data (MCAR / MAR / MNAR) | dữ liệu thiếu (MCAR / MAR / MNAR) | Ba kiểu thiếu: do may rủi (MCAR); do một thứ khác đã đo được (MAR); do chính giá trị bị thiếu (MNAR). | MCAR: mạng rớt ngẫu nhiên. MAR: trạm tắt khi mất điện (có ghi lại). MNAR: máy đo hỏng khi bụi quá cao. | 1, 10 |
| imputation | điền dữ liệu (imputation) | Ước lượng rồi điền vào chỗ giá trị bị thiếu. | 10, (thiếu), 14 → nội suy tuyến tính điền 12. | 10 |
| flag column | cột cờ | Cột thêm vào để đánh dấu dòng nào đã bị sửa hoặc điền, không xoá dấu vết. | `y` = 12 và `da_dien` = 1: số 12 là số điền vào, không phải số đo thật. | 10 |
| stuck sensor | cảm biến đứng yên | Cảm biến bị kẹt, ghi lặp y hệt một giá trị nhiều giờ liền. | Nhiệt độ 27,3; 27,3; 27,3… suốt 9 giờ liền, kể cả ban đêm. | 10 |
| outlier / anomaly | ngoại lai / bất thường | Điểm lệch hẳn khỏi hành vi chung của chuỗi. Có thể là lỗi đo, cũng có thể là sự kiện thật. | 20, 22, 21, 250, 23: điểm 250 là ngoại lai. | 2, 11 |
| additive outlier / level shift / transient change | AO, LS, TC (điểm đơn, dịch mức, thay đổi tạm) | Ba kiểu bất thường. AO: một điểm lệch rồi trở lại; LS: mức đổi và ở lại; TC: nhảy lên rồi hồi dần. | AO: 10, 10, 30, 10. LS: 10, 10, 30, 30. TC: 10, 10, 30, 20, 15, 12. | 11 |
| MAD (median absolute deviation) | MAD (độ lệch tuyệt đối trung vị) | Trung vị của khoảng cách từ mỗi điểm tới trung vị, nhân 1,4826 để so được với độ lệch chuẩn. Ít bị ngoại lai kéo lệch. | 10, 12, 11, 30, 12: trung vị 12; khoảng cách 2, 0, 1, 18, 0 → trung vị 1 → MAD ≈ 1,48. | 11 |
| Hampel filter | bộ lọc Hampel | Trong mỗi cửa sổ trượt, điểm nào cách trung vị quá 3 lần MAD thì gắn cờ ngoại lai (xem MAD). | Cửa sổ 10, 12, 11, 30, 12: trung vị 12, MAD ≈ 1,48; 30 lệch 18 > 3 × 1,48 → ngoại lai. | 11 |
| PELT, penalty | PELT, penalty | Thuật toán tìm điểm gãy: thử nhiều cách chia chuỗi thành đoạn; mỗi điểm gãy thêm vào bị phạt một khoản (penalty). | Penalty lớn → chỉ tìm 1–2 điểm gãy; penalty nhỏ → tìm nhiều, dễ báo nhầm. | 11 |
| MBIC | MBIC | Một công thức chọn sẵn penalty cho PELT, khoảng $3\ln n$ ($n$ là số điểm); BIC dùng $2\ln n$. | $n$ = 1.000 ngày: $\ln n$ ≈ 6,91 → MBIC ≈ 20,7; BIC ≈ 13,8. | 11 |
| CROPS | CROPS | Cách quét cả một dải penalty để xem số điểm gãy đổi thế nào, thay vì tin một con số penalty duy nhất. | Penalty 5, 10, 20, 40, 80 → 12, 6, 3, 3, 1 điểm gãy → vùng ổn định là 3. | 11 |
| CUSUM | CUSUM | Cộng dồn độ lệch so với mức bình thường (trừ đi một khoản cho phép $k$); tổng vượt ngưỡng thì báo có thay đổi. | Mức chuẩn 10, $k$ = 1; dữ liệu 12, 13, 12 → tổng dồn 1, 3, 4. | 11 |
| denoising / smoothing | khử nhiễu / làm trơn | Bớt dao động ngẫu nhiên nhỏ để thấy rõ đường đi chính của chuỗi. | 3, 5, 4, 8, 6 làm trơn bằng trung bình trượt 3 điểm → 4; 5,67; 6. | 4, 12 |
| exponentially weighted moving average (EWMA) | EWMA (trung bình trượt hàm mũ) | Trung bình trượt mà điểm càng mới càng nặng ký: $z_t = \alpha y_t + (1-\alpha) z_{t-1}$, với $0 < \alpha \le 1$. | $\alpha$ = 0,5, giá trị trơn trước 10, số mới 14 → 0,5 × 14 + 0,5 × 10 = 12. | 12 |
| causal / non-causal filter | bộ lọc nhân quả / không nhân quả | Bộ lọc nhân quả chỉ dùng quá khứ; không nhân quả dùng cả điểm tương lai. Loại sau gây rò rỉ nếu làm feature dự báo. | Trung bình 3 ngày tại ngày 5: nhân quả dùng ngày 3–5; căn giữa dùng ngày 4–6. | 11, 12 |
| spectral frequency, cycle length | tần số, chu kỳ | Chu kỳ là số bước để một nhịp lặp lại một lần. Tần số = 1 / chu kỳ, tức số lần lặp trong mỗi bước. | Nhịp ngày trên dữ liệu giờ: chu kỳ 24 giờ, tần số 1/24 ≈ 0,042 lần mỗi giờ. | 9, 12 |
| periodogram, spectrum | periodogram, phổ | Biểu đồ cho biết chuỗi dồn bao nhiêu "năng lượng" vào mỗi tần số (xem tần số). Đỉnh cao ở đâu là nhịp mạnh ở đó. | Tải điện giờ: đỉnh ở tần số 1/24 (nhịp ngày) và 1/168 (nhịp tuần). | 9, 12 |
| low-pass filter | lọc thông thấp | Bộ lọc giữ dao động chậm (tần số thấp), bỏ dao động nhanh (tần số cao). Làm trơn là một kiểu lọc thông thấp. | Trung bình trượt 24 giờ trên tải điện: giữ mức theo từng ngày, xoá nhịp lên xuống trong ngày. | 12 |
| IIR filter (infinite impulse response) | bộ lọc IIR | Bộ lọc mà mỗi giá trị ra dùng cả các giá trị ra trước đó, nên ảnh hưởng của một điểm kéo dài mãi, mờ dần. EWMA là một bộ lọc IIR. | EWMA $\alpha$ = 0,5: ảnh hưởng của một điểm là 0,5; 0,25; 0,125… không bao giờ về đúng 0. | 12 |
| HP filter (Hodrick–Prescott) | bộ lọc HP | Cách tách một đường xu hướng trơn khỏi chuỗi, hay dùng trong kinh tế. Xu hướng ở cuối chuỗi đổi nhiều khi có thêm dữ liệu mới. | Thêm 1 năm số liệu, đường xu hướng HP của năm cuối cũ bị kéo lệch hẳn. | 12 |
| aliasing | aliasing | Hạ tần suất mà không lọc trước thì nhịp nhanh bị "giả dạng" thành nhịp chậm không có thật. | Nhịp 24 giờ, lấy mẫu mỗi 25 giờ → thấy một nhịp giả dài 600 giờ. | 12 |
| Nyquist frequency | tần số Nyquist | Bằng nửa tần số lấy mẫu. Nhịp nhanh hơn mức này thì dữ liệu không thể thấy đúng. | Đo mỗi giờ (1 lần/giờ) → Nyquist = 0,5 lần/giờ: nhịp ngắn hơn 2 giờ không thấy được. | 12 |
| SAITS, BRITS | SAITS, BRITS | Hai mô hình deep learning (xem deep learning) để điền dữ liệu thiếu, học từ nhiều chuỗi cùng lúc. | Đáng dùng khi có nhiều chuỗi liên quan và lỗ thiếu dài; lỗ ngắn vài giờ thì nội suy là đủ. | 10 |

## 5. Feature và rò rỉ

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| feature | feature | Một cột đầu vào mà mô hình dùng để dự báo. | Dự báo tải giờ tới với các feature: tải cùng giờ hôm qua, nhiệt độ, giờ trong ngày. | 1, 13 |
| lag feature, rolling feature | feature trễ, feature cửa sổ trượt | Feature trễ lấy giá trị $k$ bước trước. Feature cửa sổ trượt tóm tắt nhiều bước trước, ví dụ trung bình 7 ngày. | Chuỗi 5, 7, 6, 9: tại bước 4, trễ 1 = 6; trung bình 3 bước trước = (5 + 7 + 6)/3 = 6. | 13 |
| data leakage / look-ahead bias | rò rỉ tương lai | Lỡ dùng thông tin chưa có tại mốc cắt, nên điểm đánh giá đẹp giả tạo. | Chuẩn hoá bằng trung bình cả năm, gồm cả các tháng đang cần dự báo → rò rỉ. | 5, 12, 13 |
| target leakage | rò rỉ mục tiêu | Feature chứa chính biến mục tiêu, hoặc thứ được tính ra từ nó. | Dự báo doanh số ngày mai với feature "doanh số trung bình 3 ngày quanh ngày mai". | 13 |
| exogenous variable / covariate | biến ngoại sinh / covariate | Biến bên ngoài chuỗi, giúp giải thích chuỗi. | Nhiệt độ là biến ngoại sinh khi dự báo tải điện. | 13, 18, 30 |
| future-known covariate | covariate biết trước tương lai | Biến ngoại sinh đã biết chắc cả cho khoảng tương lai vào lúc ra dự báo. | Lịch nghỉ lễ, giá đã chốt: biết trước. Nhiệt độ thật của ngày mai: không biết trước. | 30, 35 |
| holiday effect | hiệu ứng ngày lễ | Ngày lễ làm chuỗi lệch khỏi ngày thường. Tết âm lịch rơi vào ngày dương lịch khác nhau mỗi năm. | Tết 2024 là 10/2, Tết 2025 là 29/1 → không thể lấy "cùng ngày năm trước". | 4, 13 |
| heating / cooling degree days | HDD, CDD (độ-ngày sưởi / làm mát) | Đo trời lạnh hơn (HDD) hoặc nóng hơn (CDD) mốc 18,33 °C bao nhiêu độ. Dùng giải thích tải điện sưởi và điều hoà. | Trời 30 °C → CDD = 30 − 18,33 = 11,67, HDD = 0. Trời 10 °C → HDD = 8,33. | 8 |
| VIF (variance inflation factor) | VIF (hệ số phóng đại phương sai) | Đo một biến đầu vào bị các biến khác "đoán" được tới đâu. VIF trên 10 là các biến trùng thông tin nhau. | Các biến khác giải thích 90% biến $j$ ($R^2$ = 0,9) → VIF = 1/(1 − 0,9) = 10. | 8 |

## 6. Đánh giá

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| forecast error | sai số dự báo | Khoá quy ước: sai số = thực tế − dự báo. Sai số dương nghĩa là dự báo thấp hơn thực tế. | Thật 100, dự báo 90 → sai số = 100 − 90 = +10 (dự báo thiếu 10). | 1 |
| baseline | baseline | Mô hình đơn giản làm mốc so sánh. Mô hình mới phải thắng được nó mới đáng dùng. | Seasonal naive có MAE 50; mô hình mới MAE 55 → thua baseline, bỏ. | 1, 14 |
| naive / seasonal naive | naive / seasonal naive | Naive: dự báo = giá trị cuối cùng đã biết. Seasonal naive: dự báo = giá trị cùng kỳ của mùa trước. | Dữ liệu giờ, biết tới 23h nay. Dự báo 19h mai: naive lấy số 23h nay; seasonal naive ($m$ = 24) lấy số 19h nay. | 1, 14 |
| drift method | phương pháp drift | Nối điểm đầu và điểm cuối của lịch sử bằng một đường thẳng rồi kéo dài ra tương lai. | Lịch sử đi từ 10 lên 30 sau 4 bước (dốc 5 mỗi bước) → dự báo 35, 40, 45. | 5, 14 |
| in-sample / out-of-sample | trong mẫu / ngoài mẫu | Trong mẫu: đo trên chính dữ liệu đã dùng để khớp. Ngoài mẫu: đo trên dữ liệu mô hình chưa thấy. | Khớp trên năm 2023: sai số trên 2023 là trong mẫu, trên 2024 là ngoài mẫu. | 2, 14 |
| in-sample error reported as accuracy | sai số ảo | Sai số đo trên chính dữ liệu đã dùng để làm dự báo; luôn đẹp hơn sai số thật khi dự báo tương lai. | Học thuộc đáp án đề cũ rồi thi lại đúng đề đó: 10 điểm, nhưng đề mới chỉ 6. | 1 |
| train / validation / test | tập huấn luyện / tập chọn cấu hình (validation) / tập test | Ba phần dữ liệu chia theo thời gian: để khớp mô hình, để chọn cấu hình, và để chấm điểm lần cuối. | 2020–2022 huấn luyện, 2023 kiểm định, 2024 test. | 3, 15 |
| backtest | backtest | Giả vờ đứng ở nhiều mốc cắt trong quá khứ, dự báo, rồi so với cái đã thật sự xảy ra. | Đứng ở 52 thứ Hai của năm 2010, mỗi lần dự báo 168 giờ → 52 lần chấm. | 3, 15 |
| rolling forecast | dự báo cuốn | Ra dự báo lặp lại: mỗi khi có thêm dữ liệu thì dời gốc dự báo tới và dự báo lại. | Mỗi thứ Hai 00:00 dự báo 168 giờ tới; tuần sau dời gốc thêm 7 ngày rồi làm lại. | 1, 15 |
| rolling origin / time series cross-validation | rolling origin | Kiểu backtest mà mốc cắt dời dần về sau; mỗi lần chỉ dùng dữ liệu trước mốc. | Mốc 1/1, 1/2, 1/3: lần 1 học tới 31/12 dự báo tháng 1; lần 2 học tới 31/1 dự báo tháng 2… | 12, 15 |
| expanding / sliding window | cửa sổ mở rộng / cửa sổ trượt | Mở rộng: dữ liệu học dài dần từ đầu chuỗi. Trượt: luôn chỉ lấy đúng $n$ bước gần nhất. | Mốc đầu tháng 4: cửa sổ mở rộng học tháng 1–3; cửa sổ trượt 2 tháng học tháng 2–3. | 2, 15 |
| gap | khoảng đệm (gap) | Bỏ trống một đoạn giữa phần học và phần chấm, để mô phỏng việc dữ liệu về muộn. | Số liệu về trễ 2 ngày: học tới ngày 10, bỏ ngày 11–12, chấm từ ngày 13. | 15 |
| MAE (mean absolute error) | MAE | Trung bình độ lớn của sai số, bỏ dấu. Cùng đơn vị với dữ liệu. | Sai số 2 và −4 → MAE = (2 + 4)/2 = 3. | 1, 14 |
| RMSE (root mean squared error) | RMSE | Căn bậc hai của trung bình bình phương sai số. Phạt nặng các sai số lớn. | Sai số 2 và −4 → RMSE = √((4 + 16)/2) = √10 ≈ 3,16. | 5, 14 |
| MAPE (mean absolute percentage error) | MAPE | Trung bình sai số tính theo phần trăm của giá trị thật. Hỏng khi giá trị thật bằng 0. | Thật 100 và 50, dự báo 90 và 60 → sai 10% và 20% → MAPE = 15%. | 11, 14 |
| sMAPE (symmetric MAPE) | sMAPE | Giống MAPE nhưng chia cho trung bình của thật và dự báo. Khoá khuyên không dùng (Phụ lục D). | Thật 100, dự báo 90 → 10 / 95 ≈ 10,5%. | 9, 14 |
| MASE (mean absolute scaled error) | MASE | MAE của mô hình chia cho MAE của naive (hoặc seasonal naive) tính trong mẫu. Dưới 1 là tốt hơn mốc đó. | MAE mô hình 6, MAE của seasonal naive trong mẫu 8 → MASE = 6/8 = 0,75. | 9, 14 |
| RMSSE (root mean squared scaled error) | RMSSE | Giống MASE nhưng dùng bình phương sai số rồi lấy căn. Là chỉ số chính của cuộc thi M5. | Trung bình bình phương sai số 36, của naive trong mẫu 64 → RMSSE = √(36/64) = 0,75. | 14 |
| WAPE (weighted absolute percentage error) | WAPE | Tổng độ lớn sai số chia cho tổng giá trị thật. Không hỏng khi có vài giá trị thật bằng 0. | Thật 100 và 50; sai số 10 và −10 → (10 + 10)/150 ≈ 13,3%. | 14 |
| scale-free / scaled error | sai số không đơn vị / có chia thang | Sai số được chia cho một mốc (giá trị thật, hay sai số của naive), nên so được giữa các chuỗi khác đơn vị. | MAE 5 kWh và MAE 5 cái không so được với nhau; MASE 0,8 và 1,2 thì so được. | 14 |
| Diebold–Mariano test | kiểm định Diebold–Mariano | Kiểm định xem hai mô hình chênh độ chính xác thật, hay chỉ do may (xem kiểm định giả thuyết). | Mô hình A thắng B trên 40 ngày nhưng p = 0,15 → chưa đủ bằng chứng A tốt hơn. | 15 |
| skill score | skill score | Mô hình tốt hơn mốc tham chiếu bao nhiêu phần: 1 − (sai số mô hình / sai số mốc). | MAE mô hình 40, seasonal naive 50 → skill = 1 − 40/50 = 0,2 (tốt hơn 20%). | 9, 14, 25 |
| forecast value added (FVA) | FVA | Mỗi bước trong quy trình (mô hình, người chỉnh tay…) làm dự báo tốt lên hay tệ đi bao nhiêu. | Mô hình MAPE 12%; sau khi phòng bán hàng chỉnh tay còn 14% → bước chỉnh tay có FVA âm. | 40 |

## 7. Mô hình thống kê

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| regression | hồi quy | Tìm một công thức, thường là đường thẳng, để đoán một biến từ các biến khác. | Hồi quy tải theo nhiệt độ ra: tải ≈ 30 + 2 × nhiệt độ. Trời 25 °C → tải ≈ 30 + 50 = 80. | 1, 18 |
| coefficient of determination, R-squared | $R^2$ (hệ số xác định) | Tỷ lệ độ dao động của biến cần đoán mà mô hình giải thích được, từ 0 đến 1. Càng gần 1 càng khớp. | Phương sai của tải là 100; phần dư còn phương sai 20 → $R^2$ = 1 − 20/100 = 0,8. | 8, 18 |
| autoregressive, AR | AR (tự hồi quy) | Giá trị hôm nay bằng một phần các giá trị trước đó cộng nhiễu. AR(1) chỉ dùng một bước trước. | AR(1) hệ số 0,7: hôm qua 10, nhiễu 0,5 → hôm nay 0,7 × 10 + 0,5 = 7,5. | 2, 7, 17 |
| exponential smoothing, ETS | làm trơn hàm mũ, ETS | Họ mô hình dự báo bằng trung bình có trọng số giảm dần theo tuổi của dữ liệu. ETS gồm phần sai số, xu hướng, mùa vụ. | $\alpha$ = 0,3: mức cũ 100, số mới 110 → mức mới 0,3 × 110 + 0,7 × 100 = 103. | 1, 16 |
| damped trend | xu hướng tắt dần (damped) | Xu hướng yếu dần theo tầm dự báo, không kéo thẳng mãi. | Dốc 10 mỗi bước, hệ số tắt 0,8: cộng thêm 8; 6,4; 5,12… thay vì 10, 10, 10. | 16 |
| Theta method | phương pháp Theta | Phương pháp đơn giản: lấy trung bình của đường xu hướng thẳng kéo dài và dự báo làm trơn hàm mũ. | Đường thẳng kéo dài cho 120, làm trơn hàm mũ cho 110 → Theta ≈ (120 + 110)/2 = 115. | 16 |
| ARIMA / SARIMA | ARIMA / SARIMA | Mô hình dùng giá trị trễ (AR), sai phân (I) và sai số trễ (MA) để dự báo. SARIMA thêm phần mùa vụ. | ARIMA(1,1,0) hệ số 0,5: thay đổi kỳ trước +4 → dự báo thay đổi kỳ này +2. | 1, 17 |
| information criterion (AIC, AICc, BIC) | tiêu chí thông tin | Điểm để chọn mô hình: thưởng khớp tốt, phạt dùng nhiều tham số. Nhỏ hơn là tốt hơn. | Trên cùng dữ liệu, mô hình A có AIC 510, B có AIC 508 → chọn B. | 2, 17 |
| Ljung–Box test | kiểm định Ljung–Box | Kiểm định xem phần dư còn tự tương quan không (xem kiểm định giả thuyết). Còn thì mô hình bỏ sót mẫu. | Ljung–Box đến trễ 10 cho p = 0,002 → phần dư còn mẫu, mô hình chưa đủ. | 7, 17 |
| dynamic regression | hồi quy động | Hồi quy theo biến ngoại sinh, phần sai số còn lại được mô tả bằng ARIMA. | Tải = 30 + 2 × nhiệt độ + sai số theo ARIMA(1,0,0). | 1, 18 |
| Fourier terms | số hạng Fourier | Cặp sin/cos có chu kỳ bằng chu kỳ mùa vụ, dùng làm feature để mô tả mùa vụ trơn. | Mùa vụ năm trên dữ liệu ngày: $\sin(2\pi t/365{,}25)$ và $\cos(2\pi t/365{,}25)$. | 13, 18 |
| intermittent demand | nhu cầu gián đoạn | Chuỗi có nhiều kỳ bằng 0, thỉnh thoảng mới có số dương. | Bán phụ tùng theo tuần: 0, 0, 3, 0, 0, 0, 1, 0. | 9, 19 |
| Croston, TSB | Croston, TSB | Dự báo riêng cỡ đơn mỗi lần có bán và khoảng cách giữa hai lần bán, rồi chia nhau. TSB thay khoảng cách bằng xác suất có bán. | Mỗi lần bán 2 cái, cứ 4 kỳ bán một lần → dự báo 2/4 = 0,5 cái mỗi kỳ. | 19 |
| SBA (Syntetos–Boylan approximation) | SBA | Croston nhân thêm (1 − α/2) để bỏ phần dự báo cao có hệ thống. | Croston 0,8, α = 0,1 → SBA 0,8 × 0,95 = 0,76. | 19 |
| ADI, CV² (Syntetos–Boylan classification) | ADI, CV² | ADI: số kỳ chia số kỳ có bán. CV²: bình phương (độ lệch chuẩn ÷ trung bình) của lượng khi có bán. Ngưỡng 1,32 và 0,49 chia bốn nhóm mượt / thất thường / gián đoạn / cục. | 12 tháng, 3 tháng có bán, lượng 2, 2, 2 → ADI 4, CV² 0: nhóm gián đoạn. | 19 |
| ADIDA, IMAPA (temporal aggregation) | gộp thời gian | Cộng nhiều kỳ thành một để bớt số 0, dự báo trên chuỗi gộp rồi chia lại; IMAPA lấy trung bình nhiều mức gộp. | Tháng 0, 2, 0, 0, 1, 0 → quý 2 và 1 → 1,5 mỗi quý → 0,5 mỗi tháng. | 19 |
| TBATS | TBATS | Mô hình state space cho nhiều mùa vụ: Fourier cho từng chu kỳ, biến đổi Box–Cox, sai số ARMA; không nhận biến ngoài. | Tải điện giờ với chu kỳ 24 và 168. | 18 |
| Prophet | Prophet | Thư viện của Meta: xu hướng gãy khúc + Fourier + lễ đã khai; sai số coi như độc lập. Không tự biết lễ âm lịch. | Lượt xem = xu hướng 2,44 − tuần 0,02 − năm 0,07 − Tết 0,73 = 1,63 triệu. | 18 |
| intervention variable (pulse, step, ramp) | biến can thiệp (xung, bậc, dốc) | Biến giả mô tả sự kiện trong hồi quy: xung một kỳ, bậc từ một mốc trở đi, dốc tăng dần từ một mốc. | Sự kiện tháng 3 trong 6 tháng: xung 0,0,1,0,0,0; bậc 0,0,1,1,1,1; dốc 0,0,0,1,2,3. | 18 |
| state space model, Kalman filter | mô hình không gian trạng thái, bộ lọc Kalman | Mô tả chuỗi qua một "trạng thái" ẩn (như mức thật) thay đổi dần. Bộ lọc Kalman cập nhật trạng thái mỗi khi có số đo mới. | Đang ước lượng 20 °C, đo được 22 °C, tin số đo 50% → cập nhật thành 21 °C. | 10, 20 |
| VAR, cointegration | VAR, đồng liên kết (cointegration) | VAR dự báo nhiều chuỗi cùng lúc, mỗi chuỗi dùng trễ của mọi chuỗi. Đồng liên kết: hai chuỗi đều trôi nhưng hiệu của chúng dừng. | Giá xăng và giá dầu thô đều trôi, nhưng chênh lệch giữa chúng dao động quanh một mức. | 8, 20 |
| volatility, GARCH | biến động (volatility), GARCH | Biến động là mức dao động to hay nhỏ của chuỗi, thay đổi theo thời gian. GARCH dự báo mức dao động đó. | Tuần yên ổn giá đổi khoảng ±0,5%/ngày; tuần hoảng loạn ±4%/ngày → biến động gấp 8 lần. | 21 |
| VECM | VECM | VAR trên sai phân cộng một số hạng kéo khoảng chênh (spread) của hai chuỗi đồng liên kết về cân bằng. | Spread +0,3, hệ số kéo về −0,2 → tuần tới chuỗi giảm thêm 0,06. | 20 |
| dynamic factor model (DFM) | mô hình nhân tố động | Vài nhân tố ẩn chung điều khiển nhiều chuỗi; ước lượng bằng Kalman, xử lý được tần suất hỗn hợp và ô thiếu. | Nhân tố 0,5; hệ số của GDP 2,0 → GDP ≈ 1,0. | 20 |
| nowcasting, ragged edge | nowcasting, ragged edge | Dự báo quý hiện tại khi số chính thức chưa công bố; ragged edge: mỗi chuỗi dừng ở một tháng khác nhau. | Giữa tháng 4: việc làm có tới tháng 3, GDP mới tới quý 4. | 20 |
| vintage (real-time data) | vintage | Toàn bộ số liệu như được biết tại một ngày công bố; số đã sửa về sau là thông tin tương lai. | GDP quý 4/2008: lần đầu −3,9%, bản 2025 −8,9%. | 20 |
| bridge equation, MIDAS | bridge equation, MIDAS | Hồi quy GDP quý theo trung bình quý của chỉ báo tháng (bridge); hoặc theo từng tháng với trọng số ít tham số (MIDAS). | GDP = 1 + 1,5 × việc làm quý. | 20 |
| realized volatility, HAR | biến động thực hiện, HAR | RV = tổng bình phương lợi suất trong ngày (từ dữ liệu giờ/phút); HAR hồi quy RV mai theo RV ngày, tuần, tháng. | Bốn lợi suất 0,5; −1; 0,8; −0,3 → RV 1,98 dù cả ngày đóng cửa bằng giá mở. | 21 |
| Value at Risk, expected shortfall | VaR, ES | VaR 99%: mức lỗ mà 99% số ngày không tệ hơn; ES: lỗ trung bình trong những ngày tệ hơn VaR. | Độ lệch chuẩn 1%, chuẩn → VaR −2,33%, ES −2,67%. | 21 |
| Kupiec test | kiểm định Kupiec | Kiểm số ngày vượt VaR có khớp tỷ lệ hứa không; vượt quá nhiều hay quá ít đều bị bác. | 1.000 ngày, vượt 20 lần (kỳ vọng 10) → LR 7,8 > 3,84: bác. | 21 |
| QLIKE | QLIKE | Hàm mất mát cho dự báo phương sai: h/ĥ − ln(h/ĥ) − 1, bằng 0 khi đúng; ít bị vài ngày cực lớn chi phối hơn MSE. | Thật 2, dự báo 1: 2 − ln 2 − 1 ≈ 0,31. | 21 |
| hierarchical / grouped series | chuỗi phân cấp / phân nhóm | Nhiều chuỗi lồng nhau: chuỗi cấp trên bằng tổng các chuỗi cấp dưới. | Doanh số cả nước = Bắc + Trung + Nam. | 28 |
| reconciliation (bottom-up, top-down, MinT) | reconciliation | Chỉnh các dự báo sao cho tổng dự báo cấp dưới khớp đúng dự báo cấp trên. | Dự báo Bắc 40 + Nam 50 = 90 nhưng dự báo cả nước 100 → chỉnh để hai bên bằng nhau. | 28 |

## 8. Machine learning và deep learning

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| machine learning (ML) | machine learning (ML) | Cho máy tự tìm quy luật từ rất nhiều ví dụ, thay vì người viết sẵn công thức. | Đưa máy 10.000 dòng (nhiệt độ, giờ → tải) để nó tự học cách đoán tải. | 1, 22 |
| neural network, deep learning | mạng nơ-ron, deep learning | Mô hình gồm nhiều lớp phép tính đơn giản xếp chồng, học tham số từ rất nhiều dữ liệu. "Deep" nghĩa là nhiều lớp. | Một mạng nhận 168 giờ tải điện gần nhất và trả ra 24 giờ tới. | 1, 29 |
| global / local model | mô hình global / local | Global: một mô hình học chung cho nhiều chuỗi. Local: mỗi chuỗi một mô hình riêng. | 500 cửa hàng: global là 1 mô hình; local là 500 mô hình. | 1, 22 |
| recursive / direct / MIMO strategy | chiến lược recursive / direct / MIMO | Ba cách dự báo nhiều bước: dùng lại dự báo bước trước (recursive), mỗi bước một mô hình (direct), một mô hình ra cả dãy (MIMO). | $h$ = 3: recursive chạy 1 mô hình 3 lần; direct dùng 3 mô hình; MIMO 1 mô hình ra 3 số. | 22 |
| gradient boosting (LightGBM, XGBoost) | gradient boosting | Ghép nhiều cây quyết định nhỏ (mỗi cây là chuỗi câu hỏi có/không, như "nhiệt độ > 25 °C?"). Cây sau học sửa phần sai của các cây trước. | Cây 1 đoán 100 (thật 120); cây 2 học phần thiếu 20, đoán thêm 15 → tổng 115. | 1, 23 |
| Tweedie loss | hàm mất mát Tweedie | Hàm mất mát là con số đo mức sai mà mô hình cố làm nhỏ khi học. Tweedie hợp với dữ liệu đếm nhiều số 0. | Doanh số một món theo ngày: 0, 0, 0, 5, 0, 12 → hợp với Tweedie. | 23 |
| hyperparameter tuning | tune siêu tham số | Siêu tham số là núm chỉnh do người chọn trước khi khớp. Tune là thử nhiều giá trị, giữ giá trị tốt nhất trên tập kiểm định. | Thử số cây 100, 300, 500 → MAE kiểm định 12, 10, 11 → chọn 300. | 9, 23 |
| SHAP | SHAP | Chia một dự báo thành phần đóng góp của từng feature. | Dự báo 120 = mức chung 100 + nhiệt độ đóng góp 15 + giờ trong ngày đóng góp 5. | 23 |
| ensemble, forecast combination | ensemble, kết hợp dự báo | Trộn dự báo của nhiều mô hình, thường bằng cách lấy trung bình. | ETS 100, ARIMA 110, LightGBM 120 → dự báo kết hợp (100 + 110 + 120)/3 = 110. | 1, 24 |
| FFORMA | FFORMA | Dùng đặc trưng của từng chuỗi để một mô hình ML tự chọn trọng số kết hợp nhiều phương pháp dự báo (xem ML). | Chuỗi mùa vụ mạnh: trọng số ETS 0,7, naive 0,3. Chuỗi nhiễu: ngược lại. | 9, 24 |
| cold start | cold start | Dự báo cho chuỗi mới chưa có lịch sử. | Sản phẩm mới ra tuần này: mượn mẫu bán của sản phẩm tương tự để dự báo. | 24 |
| window, context length | cửa sổ, độ dài ngữ cảnh | Số bước quá khứ mà mô hình được xem mỗi lần dự báo. | Độ dài ngữ cảnh 168: mô hình nhìn 168 giờ (1 tuần) gần nhất để dự báo. | 29, 34 |
| epoch, early stopping | epoch, dừng sớm | Epoch là một lượt mô hình học qua toàn bộ dữ liệu huấn luyện. Dừng sớm: ngưng học khi sai số trên tập kiểm định thôi giảm. | Sai số kiểm định sau epoch 1–5: 9; 7; 6; 6,2; 6,5 → dừng, giữ epoch 3. | 29 |
| Transformer, attention, patching | Transformer, attention, patching | Transformer là mạng nơ-ron dùng attention: mỗi điểm tự chọn nên chú ý điểm quá khứ nào. Patching cắt chuỗi thành đoạn ngắn làm đầu vào. | 512 giờ cắt thành 32 đoạn 16 giờ → mô hình xử lý 32 đơn vị. | 31 |
| generative model, diffusion | mô hình sinh, diffusion | Mô hình sinh tạo ra dữ liệu mới giống dữ liệu thật. Diffusion học cách khử nhiễu dần, từ nhiễu thuần ra dữ liệu. | Sinh 100 đường tải điện tháng 7 không có thật nhưng trông như thật. | 32 |
| synthetic data (fidelity / utility / privacy) | dữ liệu tổng hợp | Dữ liệu do mô hình sinh ra. Tốt khi giống thật, dùng được cho bài toán, và không chép nguyên bản ghi thật. | Học trên dữ liệu tổng hợp, chấm trên dữ liệu thật: MAE chỉ kém 5% → dùng được. | 3, 32 |
| graph neural network (GNN) | mạng nơ-ron đồ thị (GNN) | Mạng nơ-ron học trên đồ thị: mỗi nút (trạm, vùng) nhận thông tin từ các nút nối với nó. | Dự báo gió ở trạm A dùng cả số đo của 3 trạm lân cận. | 33 |

## 9. Bất định

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| prediction interval | khoảng dự báo | Khoảng mà giá trị tương lai rơi vào với một xác suất cho trước. Khác khoảng tin cậy (dòng dưới). | "Tải 19h mai nằm trong 900–1.000 MWh với xác suất 80%." | 1, 2, 25 |
| confidence interval | khoảng tin cậy | Khoảng cho một con số cố định chưa biết (như trung bình thật), không phải cho một giá trị tương lai. | Trung bình của 50 lần đo là 12; khoảng tin cậy 95% cho trung bình thật: 11–13. | 2 |
| coverage | tỷ lệ phủ (coverage) | Tỷ lệ số lần giá trị thật rơi vào khoảng dự báo. Khoảng 80% tốt thì phủ gần 80%. | 100 khoảng 80%, chỉ 64 lần trúng → tỷ lệ phủ 64%: khoảng quá hẹp. | 2, 25 |
| calibration | calibration | Dự báo nói "70%" thì chuyện đó xảy ra đúng khoảng 70% số lần. | 10 ngày dự báo mưa 70%, có 7 ngày mưa → calibration tốt. | 25 |
| sharpness | độ sắc (sharpness) | Khoảng hay phân phối dự báo hẹp cỡ nào. Hẹp là tốt, nhưng chỉ khi vẫn phủ đúng. | Hai khoảng cùng phủ 80%: khoảng 90–110 sắc hơn khoảng 70–130. | 2, 25 |
| pinball loss / quantile loss | pinball loss | Điểm phạt cho dự báo quantile $\tau$: dự báo thấp hơn thật bị phạt $\tau$ lần phần thiếu; cao hơn bị phạt $(1-\tau)$ lần phần thừa. | $\tau$ = 0,9, thật 10: dự báo 8 → 0,9 × 2 = 1,8; dự báo 12 → 0,1 × 2 = 0,2. | 2, 25 |
| CRPS | CRPS | Điểm chấm cả một phân phối dự báo so với giá trị thật; nhỏ là tốt. Với dự báo một con số, CRPS bằng sai số tuyệt đối. | Dự báo phân phối chuẩn trung bình 0, độ lệch chuẩn 1; thật 0,8 → CRPS ≈ 0,476. | 2, 25 |
| WIS (weighted interval score) | WIS | Điểm gộp trung vị và nhiều khoảng dự báo thành một số, xấp xỉ CRPS. Nhỏ là tốt. | Thật 10, trung vị 8, khoảng 80% [6; 9], khoảng 50% [7; 8,5] → WIS ≈ 1,67. | 25 |
| Winkler score | Winkler score | Độ rộng khoảng, cộng phạt $2/\alpha$ lần phần giá trị thật vượt ra ngoài ($\alpha$ = 1 − mức của khoảng). Nhỏ là tốt. | Khoảng 80% ($\alpha$ = 0,2) là [6; 9], thật 10: 3 + (2/0,2) × 1 = 13. | 25 |
| PIT histogram | PIT histogram | Mỗi lần dự báo, ghi giá trị thật rơi ở mức quantile nào, rồi vẽ biểu đồ cột đếm các mức đó (histogram). Cột đều nhau là dự báo đúng độ bất định. | Giá trị thật rơi dưới quantile 0,05 và trên 0,95 quá nhiều → histogram hình chữ U → khoảng quá hẹp. | 25 |
| reliability diagram | reliability diagram | Biểu đồ so xác suất dự báo (trục ngang) với tần suất xảy ra thật (trục dọc). Điểm nằm trên đường chéo là tốt. | Nhóm dự báo "30%" thật ra xảy ra 45% số lần → điểm nằm trên đường chéo: dự báo quá thấp. | 25 |
| quantile crossing | quantile cắt nhau | Quantile mức thấp lại lớn hơn quantile mức cao, một kết quả vô lý. | Dự báo quantile 0,1 là 105 nhưng quantile 0,9 chỉ là 98. | 25 |
| sample path | sample path | Một kịch bản tương lai đầy đủ nhiều bước, do mô hình rút ngẫu nhiên. | Rút 1.000 đường cho 24 giờ tới; mỗi đường là một sample path. | 25, 32 |
| conformal prediction (split, CQR, ACI, EnbPI) | conformal prediction | Dựng khoảng dự báo từ sai số trên dữ liệu chưa dùng để khớp; bảo đảm tỷ lệ phủ nếu dữ liệu hoán đổi được. | 9 sai số cũ (bỏ dấu) 1, 2, …, 9; khoảng 80% = dự báo ± 8 (số thứ 8). | 26 |
| exchangeability | tính hoán đổi được | Đảo thứ tự dữ liệu mà các tính chất thống kê không đổi. Chuỗi có xu hướng hay drift thì vi phạm. | Các lần tung xúc xắc: hoán đổi được. Giá nhà tăng dần: đảo thứ tự thì khác hẳn. | 26 |
| prior / posterior, prior predictive check | prior / posterior, kiểm tra dự báo tiên nghiệm | Prior là niềm tin về tham số trước khi xem dữ liệu; posterior là sau khi cập nhật bằng dữ liệu. Kiểm tra tiên nghiệm: sinh thử dữ liệu từ prior xem có hợp lý. | Prior: tăng 0–10%/năm; sau 5 năm dữ liệu, posterior thu về 3–5%. Prior sinh ra tải âm → prior sai. | 27 |
| pooling (no / complete / partial) | gộp thông tin (không / hoàn toàn / một phần) | Nhiều nhóm có thể mỗi nhóm tự ước lượng, dùng chung một số, hoặc gộp một phần (kéo nhóm ít dữ liệu về gần mức chung). | Cửa hàng mới bán 20 cái/ngày (mới 3 ngày), cả chuỗi 10 cái/ngày → gộp một phần ước lượng khoảng 14. | 27 |
| divergence, $\hat R$, ESS | divergence, r_hat, ESS | Các số kiểm tra máy lấy mẫu MCMC (cách rút mẫu từ posterior) chạy ổn chưa. r_hat gần 1,00 và ESS lớn là tốt; có divergence là có vấn đề. | r_hat = 1,01 và ESS = 800 → ổn; r_hat = 1,3 → chưa hội tụ, chưa dùng được. | 27 |
| Gaussian process, kernel | quá trình Gauss, kernel | Mô hình coi cả đường cong chưa biết là ngẫu nhiên. Kernel quy định hai điểm gần nhau thì giá trị giống nhau cỡ nào. | Kernel chu kỳ 24 giờ: 19h hôm nay và 19h hôm qua được coi là rất giống nhau. | 27 |

## 10. Foundation model và LLM

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| large language model (LLM) | LLM (mô hình ngôn ngữ lớn) | Mô hình học trên rất nhiều văn bản, đọc và viết được câu chữ như người, ví dụ ChatGPT, Claude. | Đưa LLM bản tin "nắng nóng kéo dài" để nó gợi ý một feature cho mô hình tải điện. | 1, 36 |
| foundation model | foundation model | Mô hình rất lớn đã học trước trên rất nhiều chuỗi, dự báo được chuỗi mới ngay mà không cần học thêm. | Đưa 512 giờ tải điện vào Chronos, nhận dự báo 24 giờ tới, không cần huấn luyện. | 1, 34 |
| zero-shot / few-shot / fine-tune | zero-shot / few-shot / fine-tune | Zero-shot: dùng ngay; few-shot: đưa kèm vài ví dụ mẫu; fine-tune: cho model học thêm trên dữ liệu của mình. | Few-shot: đặt 3 chuỗi mẫu có đáp án vào đầu vào trước chuỗi cần dự báo. | 34, 35 |
| LoRA | LoRA | Cách fine-tune rẻ: giữ nguyên model gốc, chỉ học thêm vài ma trận nhỏ gắn kèm. | Model 200 triệu tham số, LoRA chỉ học thêm khoảng 1 triệu. | 35 |
| training cutoff / knowledge cutoff | mốc cắt dữ liệu huấn luyện | Ngày cuối cùng của dữ liệu model đã thấy lúc huấn luyện. Chấm model phải dùng dữ liệu sau ngày đó. | Model học dữ liệu tới 12/2024 → chỉ chấm trên dữ liệu từ 1/2025 trở đi. | 34, 37 |
| benchmark contamination | rò rỉ benchmark | Dữ liệu dùng để chấm đã lọt vào dữ liệu huấn luyện của model, nên điểm cao giả. | Model từng học bộ M4, rồi được chấm lại trên M4 → điểm đẹp giả. | 35 |
| revision (model) | revision | Mã phiên bản (commit) cụ thể của model trên Hugging Face. Ghi rõ để chạy lại ra đúng kết quả. | `revision="a1b2c3d"` thay vì "bản mới nhất". | 34 |
| agent, tool calling, guardrail | agent, gọi công cụ, guardrail | Agent là LLM tự lên kế hoạch và gọi công cụ (hàm Python, API) để làm việc. Guardrail là luật chặn đầu ra sai. | Agent gọi hàm `du_bao()`; guardrail chặn mọi dự báo tải âm. | 36 |
| hallucination | bịa (hallucination) | LLM đưa ra con số hoặc sự kiện nghe hợp lý nhưng không có nguồn. | LLM nói "tải tăng 12% vì lễ hội X", nhưng lễ hội X không có thật. | 36 |
| event forecasting, resolution | dự báo sự kiện, resolve | Dự báo xác suất một sự kiện có xảy ra hay không. Resolve là lúc biết chắc kết quả. | "Hà Nội có mưa ngày 1/10?" dự báo 0,7; ngày 2/10 resolve: có mưa. | 37 |
| Brier score | Brier score | Trung bình của bình phương (xác suất dự báo − kết quả), kết quả là 1 nếu xảy ra, 0 nếu không. Nhỏ là tốt. | Dự báo 0,7, sự kiện xảy ra → (0,7 − 1)² = 0,09. | 37 |

## 11. Nhân quả và ra quyết định

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| intervention, treatment | can thiệp | Hành động chủ động làm thay đổi chuỗi, mà ta muốn đo tác động. | Giảm giá 20% từ 1/6; ta muốn biết doanh số tăng bao nhiêu nhờ việc đó. | 11, 38 |
| counterfactual | phản thực tế (counterfactual) | Điều lẽ ra đã xảy ra nếu không can thiệp. Tác động = thực tế − phản thực tế. | Bán 150 khi giảm giá; nếu không giảm, ước lượng bán 120 → tác động 30. | 38 |
| synthetic control | synthetic control | Ghép có trọng số các nơi không bị can thiệp để mô phỏng nơi bị can thiệp như thể không có can thiệp. | Tỉnh A giảm giá; 0,6 × tỉnh B + 0,4 × tỉnh C bám sát A trước đó → dùng làm phản thực tế. | 38 |
| placebo test | placebo test | Chạy lại phương pháp ở nơi hoặc lúc không có can thiệp; kết quả phải gần 0. | Giả vờ tỉnh B có giảm giá (thật ra không) mà vẫn đo ra +25 → phương pháp đáng ngờ. | 38 |
| lead time | thời gian dẫn | Thời gian từ lúc đặt hàng tới lúc hàng về. | Đặt cuối tháng 3, hàng về đầu tháng 5: chờ trọn tháng 4. | 19 |
| order-up-to policy | chính sách order-up-to | Mỗi kỳ xem kho rồi đặt thêm cho (tồn + hàng đang về) đủ lên mức $S$. | $S$ = 5, tồn 2, đang về 1 → đặt 2. | 19 |
| fill rate | tỷ lệ đáp ứng | Phần nhu cầu bán được ngay từ kho. | Khách hỏi 10 món, có sẵn 8 → 80%. | 19 |
| confounding | gây nhiễu (confounding) | Có một biến tác động lên cả nguyên nhân lẫn kết quả, làm ta tưởng nhầm quan hệ giữa hai thứ đó. | Trời nóng làm tăng cả lượng kem bán ra lẫn số vụ đuối nước; kem không gây đuối nước. | 8, 39 |
| DAG | DAG (đồ thị nhân quả) | Sơ đồ mũi tên chỉ cái gì gây ra cái gì, không có vòng lặp. | Nóng → kem bán chạy; nóng → đi bơi nhiều → đuối nước. | 39 |
| elasticity | độ co giãn | Lượng bán thay đổi bao nhiêu phần trăm khi giá đổi 1%. | Giá tăng 10%, lượng giảm 15% → độ co giãn = −15/10 = −1,5. | 39 |
| double machine learning | DoubleML | Cách đo tác động nhân quả, dùng hai mô hình ML để gỡ ảnh hưởng của các biến gây nhiễu (xem ML, gây nhiễu). | Gỡ ảnh hưởng của mùa và thời tiết khỏi cả giá lẫn lượng bán, rồi đo độ co giãn trên phần còn lại. | 39 |
| scenario, what-if | kịch bản, what-if | Hỏi "nếu … thì dự báo đổi thế nào" bằng cách đổi đầu vào của mô hình. | Nếu nhiệt độ cao hơn 3 °C thì tải cao điểm ngày mai tăng bao nhiêu? | 2, 39 |
| newsvendor problem | bài toán newsvendor | Đặt hàng một lần cho một kỳ. Mức đặt tốt nhất là quantile $C_u/(C_u + C_o)$ của nhu cầu; $C_u$ là tiền mất khi thiếu, $C_o$ khi thừa. | Thiếu một đơn vị mất 4, thừa một đơn vị mất 1 → đặt ở quantile 4/(4 + 1) = 0,8. | 1, 40 |
| service level, safety stock | mức phục vụ, tồn kho an toàn | Mức phục vụ là xác suất không hết hàng. Tồn kho an toàn là lượng để thêm ngoài dự báo để đạt mức đó. | Dự báo 100; quantile 0,95 của nhu cầu là 130 → tồn kho an toàn 30 cho mức phục vụ 95%. | 40 |

## 12. Production

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| pipeline | pipeline | Chuỗi bước chạy tự động, từ lấy dữ liệu, làm sạch, dự báo tới xuất kết quả. | Lấy dữ liệu → kiểm sha256 → làm sạch → khớp mô hình → dự báo → ghi tệp. | 10, 41 |
| reproducibility | tính tái lập | Chạy lại cùng code, cùng dữ liệu, cùng seed thì ra đúng cùng con số. | Seed 42: chạy hai lần đều ra MAE = 31,7. | 8, 41 |
| continuous integration (CI) | CI (tích hợp liên tục) | Máy tự chạy toàn bộ test mỗi khi có người sửa code; test hỏng thì chặn thay đổi lại. | Đẩy code lên → CI chạy test rò rỉ trong 30 giây → xanh mới được gộp vào. | 12, 41 |
| lockfile | lockfile (`uv.lock`) | Tệp ghi chính xác phiên bản mọi thư viện, để ai cài cũng ra môi trường giống nhau. | `uv.lock` ghi pandas 2.3.3, không phải "pandas bản mới nhất". | 41 (dùng ở mọi buổi) |
| schema validation | kiểm schema | Kiểm dữ liệu đúng cột, đúng kiểu, đúng đơn vị trước khi đưa vào mô hình. | Cột tải phải là số ≥ 0, đơn vị MWh; gặp chữ "-" hay số âm thì dừng. | 41 |
| backfill | backfill | Chạy lại pipeline cho các ngày đã qua. | Sửa lỗi ngày 20/9 → backfill lại dự báo cho 1/9–19/9. | 41 |
| feature store | feature store | Kho lưu sẵn feature đã tính, kèm thời điểm có, để huấn luyện và dự báo lấy cùng một nguồn. | Feature "nhiệt độ trung bình 7 ngày" tính một lần, lưu kèm mốc thời gian. | 41 |
| batch / online serving | phục vụ theo lô / trực tuyến | Theo lô: tính dự báo hàng loạt theo lịch rồi lưu lại. Trực tuyến: tính ngay khi có yêu cầu. | Theo lô: 2h sáng dự báo 10.000 mã hàng. Trực tuyến: trả dự báo trong 0,2 giây khi được hỏi. | 42 |
| latency, p95 | độ trễ, p95 | Độ trễ là thời gian từ lúc hỏi tới lúc có trả lời. p95 là mức mà 95% số lần hỏi nhanh hơn. | 100 lần gọi, 95 lần xong dưới 180 ms → p95 ≈ 180 ms. | 42 |
| data drift / concept drift | drift dữ liệu / drift khái niệm | Drift dữ liệu: đầu vào đổi phân phối. Drift khái niệm: cùng đầu vào nhưng quan hệ với đầu ra đã đổi. | Dữ liệu: mùa hè nóng hơn mọi năm. Khái niệm: cùng 35 °C nhưng tải thấp hơn nhờ điện mặt trời mái nhà. | 43 |
| monitoring, alert | giám sát, cảnh báo | Theo dõi sai số và dữ liệu liên tục; vượt ngưỡng thì báo cho người phụ trách. | MAE tuần này 80, ngưỡng 60 → gửi cảnh báo. | 11, 43 |
| retraining policy | chính sách retrain | Luật quyết định khi nào huấn luyện lại mô hình. | Retrain mỗi tháng, hoặc ngay khi MAE vượt ngưỡng hai tuần liền. | 43 |
| runbook | runbook | Hướng dẫn từng bước để xử lý một loại sự cố. | "Dữ liệu về trễ: 1) kiểm nguồn, 2) tạm dùng seasonal naive, 3) báo nhóm." | 43 |
| model card, ADR | model card, ADR | Model card: tờ mô tả mô hình (dữ liệu, cách chấm, giới hạn). ADR: bản ghi một quyết định kỹ thuật và lý do. | ADR: "Chọn LightGBM thay TFT vì MAE ngang nhau mà chạy nhanh hơn 20 lần." | 44 |

## 13. Xác suất thống kê

| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |
|---|---|---|---|---|
| random variable | biến ngẫu nhiên | Một đại lượng chưa biết trước giá trị, chỉ biết khả năng xảy ra của từng giá trị. | Số khách ngày mai có thể là 80, 100 hay 120, mỗi số một xác suất. | 2 |
| probability distribution | phân phối | Bảng hay đường cong cho biết mỗi giá trị có thể xảy ra với xác suất bao nhiêu. | Xúc xắc cân đối: mỗi mặt 1, 2, …, 6 có xác suất 1/6. | 1, 2 |
| normal distribution | phân phối chuẩn | Phân phối hình chuông, đối xứng quanh trung bình. Khoảng 95% giá trị nằm trong trung bình ± 2 độ lệch chuẩn (đúng 95% là ± 1,96). | Trung bình 100, độ lệch chuẩn 10 → khoảng 95% giá trị rơi trong 80–120. | 2 |
| Poisson distribution | phân phối Poisson | Phân phối của số lần một việc hiếm xảy ra trong một khoảng, khi biết số lần trung bình $\mu$: P($k$) = $e^{-\mu}\mu^k / k!$. | $\mu$ = 0,8: P(0) = 0,449; P(≤ 1) = 0,809; P(≤ 2) = 0,953. | 19 |
| histogram | histogram (bảng đếm dạng cột) | Chia trục giá trị thành các khoảng bằng nhau, đếm mỗi khoảng có bao nhiêu số liệu rồi vẽ thành cột. | 5, 6, 6, 7, 7, 8 → khoảng [5, 7): 3 số; [7, 9): 3 số. | 2 |
| standard error | sai số chuẩn | Độ lệch chuẩn của chính con số ước lượng (ví dụ trung bình mẫu); nhỏ dần khi có thêm dữ liệu độc lập. | Độ lệch chuẩn 2, n = 100 → sai số chuẩn của trung bình = 2/√100 = 0,2. | 2 |
| interquartile range, IQR | khoảng tứ phân vị (IQR) | Quantile 0,75 trừ quantile 0,25: độ rộng của nửa giữa dữ liệu, ít bị ngoại lai kéo. | Quantile 0,25 là 6, quantile 0,75 là 9 → IQR = 3. | 2, 11 |
| random seed | seed | Con số khởi đầu cho bộ sinh số ngẫu nhiên; cùng seed thì ra cùng dãy số. | `np.random.default_rng(42)` chạy hai lần cho cùng kết quả. | 2 |
| missing value, NaN / NaT | giá trị thiếu (NaN, NaT) | NaN: ô số không có giá trị (Not a Number). NaT: ô thời gian không có giá trị. Khác với 0. | Cảm biến tắt lúc 03:00 → ghi NaN, không ghi 0 độ. | 1, 3 |
| PDF / PMF / CDF | hàm mật độ / hàm khối xác suất / hàm phân phối tích luỹ | PMF cho xác suất từng giá trị đếm được; PDF cho độ dày xác suất của biến liên tục. CDF tại $x$ là xác suất giá trị ≤ $x$. | Xúc xắc: PMF(3) = 1/6; CDF(3) = P(≤ 3) = 3/6 = 0,5. | 1, 2 |
| quantile | quantile | Quantile mức $q$ là giá trị nhỏ nhất mà ít nhất tỷ lệ $q$ số liệu nhỏ hơn hoặc bằng nó (đếm tay: xếp tăng dần, lấy vị trí $q \times n$ làm tròn lên). Còn gọi là phân vị. | Dãy 5, 6, 6, 7, 7, 8, 8, 9, 9, 12 → quantile 0,8 = 9 (số thứ 8). | 1, 2 |
| median | trung vị | Số đứng giữa khi xếp dãy từ nhỏ đến lớn; bằng quantile 0,5. Ít bị ngoại lai kéo lệch. | 3, 1, 7, 5, 100 → xếp 1, 3, 5, 7, 100 → trung vị 5 (trung bình là 23,2). | 1, 2 |
| expectation | kỳ vọng | Giá trị trung bình dài hạn nếu lặp lại rất nhiều lần: mỗi giá trị nhân xác suất của nó rồi cộng lại. | Xúc xắc: (1 + 2 + 3 + 4 + 5 + 6)/6 = 3,5. | 5 |
| variance | phương sai | Trung bình bình phương khoảng cách từ mỗi số tới trung bình. Đo độ dao động; đơn vị là bình phương đơn vị gốc. | 2, 4, 6: trung bình 4; bình phương độ lệch 4, 0, 4; chia $n - 1$ = 2 → phương sai 4. | 2 |
| standard deviation | độ lệch chuẩn | Căn bậc hai của phương sai, cùng đơn vị với dữ liệu. Cho biết các số thường cách trung bình cỡ bao nhiêu. | 2, 4, 6 có phương sai 4 → độ lệch chuẩn = √4 = 2. | 2 |
| coefficient of variation (CV) | hệ số biến thiên (CV) | Độ lệch chuẩn chia trung bình: độ dao động so với mức của chuỗi. | Trung bình 50, độ lệch chuẩn 10 → CV = 10/50 = 0,2 (dao động cỡ 20% mức). | 5, 9 |
| skewness | hệ số lệch (skewness) | Đo phân phối lệch về một phía. Dương: đuôi dài bên phải, tức có vài số rất lớn. | Doanh số 1, 1, 2, 2, 3, 20: đuôi phải dài → hệ số lệch dương. (Đừng nhầm với "độ lệch chuẩn".) | 2 |
| kurtosis | độ nhọn (kurtosis) | Đo đuôi phân phối dày tới đâu, tức giá trị cực đoan hay gặp cỡ nào so với phân phối chuẩn. | Lợi suất cổ phiếu: ngày tăng giảm quá 5% gặp nhiều hơn phân phối chuẩn dự đoán → độ nhọn cao. | 9 |
| correlation (Pearson) | tương quan (hệ số $r$) | Số từ −1 đến 1 đo hai biến cùng tăng giảm theo đường thẳng tới đâu. 1: cùng chiều hoàn hảo; −1: ngược chiều; 0: không có quan hệ thẳng. | $x$ = 1, 2, 3 và $y$ = 2, 4, 6 → $r$ = 1. Đổi $y$ = 6, 4, 2 → $r$ = −1. | 1, 8 |
| covariance | hiệp phương sai | Trung bình tích độ lệch của hai biến so với trung bình của chúng. Dương là cùng chiều; độ lớn phụ thuộc đơn vị. | $x$ = 1, 2, 3; $y$ = 2, 4, 6: tích các độ lệch là 2, 0, 2 → 4/(3 − 1) = 2. | 7 |
| heavy tail | đuôi dày | Giá trị cực đoan xảy ra thường hơn nhiều so với phân phối chuẩn. | Theo phân phối chuẩn, lệch quá 4 độ lệch chuẩn gần như không bao giờ gặp; dữ liệu đuôi dày gặp vài lần mỗi năm. | 2, 21 |
| overdispersion | phân tán thừa | Với dữ liệu đếm: phương sai lớn hơn trung bình (phân phối Poisson thì hai số bằng nhau). | Số khách mỗi giờ: trung bình 4, phương sai 12 → phân tán thừa. | 2, 19 |
| likelihood, MLE | likelihood, ước lượng hợp lý cực đại (MLE) | Likelihood đo dữ liệu đã thấy "hợp" với một giá trị tham số tới đâu. MLE chọn tham số làm likelihood lớn nhất. | Tung đồng xu 10 lần được 7 ngửa → MLE của xác suất ngửa = 7/10 = 0,7. | 2 |
| central limit theorem | định lý giới hạn trung tâm (CLT) | Trung bình của nhiều số ngẫu nhiên độc lập có phân phối gần hình chuông, dù từng số không như vậy. | Trung bình của 30 lần tung xúc xắc gần như luôn nằm quanh 3,5, phân bố hình chuông. | 2 |
| bootstrap, block bootstrap | bootstrap, block bootstrap | Rút lại ngẫu nhiên (có lặp) từ chính dữ liệu nhiều lần để xem một con số dao động cỡ nào. Block bootstrap rút cả khúc liền nhau để giữ tự tương quan. | Từ 5, 7, 9 rút được 7, 7, 5 → trung bình 6,33; lặp lại 1.000 lần. | 2 |
| effective sample size | cỡ mẫu hiệu dụng | Dữ liệu tự tương quan chứa ít thông tin hơn số dòng. Cỡ mẫu hiệu dụng là số điểm độc lập tương đương. | 1.000 giờ, tự tương quan trễ 1 là 0,8 → ≈ 1.000 × 0,2/1,8 ≈ 111 điểm độc lập. | 2 |
| scoring rule (proper / strictly proper) | scoring rule (proper) | Cách chấm dự báo xác suất. "Proper" nghĩa là khai đúng điều mình tin luôn cho điểm kỳ vọng tốt nhất. | Tin 70% sẽ mưa: khai 0,7 có Brier kỳ vọng 0,21, khai 0,9 là 0,25 → nói thật lợi hơn. | 25 |
| hypothesis test | kiểm định giả thuyết | Dùng dữ liệu để quyết định có đủ bằng chứng bác bỏ một giả định ban đầu (xem giả thuyết không) hay không. | Giả định: đồng xu cân đối. Tung 100 lần ra 70 ngửa → bác bỏ giả định đó. | 2, 4, 7 |
| null hypothesis | giả thuyết không ($H_0$) | Giả định mặc định mà kiểm định tìm cách bác bỏ, thường là "không có gì đặc biệt". Không bác được không có nghĩa là nó đúng. | ADF: $H_0$ là "chuỗi không dừng". KPSS: $H_0$ là "chuỗi dừng". | 2, 7 |
| p-value | p-value | Nếu $H_0$ đúng, xác suất gặp kết quả lệch cỡ này hoặc hơn. Nhỏ nghĩa là dữ liệu khó xảy ra nếu $H_0$ đúng. | Đồng xu cân đối, tung 10 lần: xác suất ra ≥ 9 ngửa = 11/1.024 ≈ 0,011 → p ≈ 0,011. | 2, 7 |
| significance level | mức ý nghĩa ($\alpha$) | Ngưỡng chọn trước khi kiểm định; p-value nhỏ hơn ngưỡng thì bác bỏ $H_0$. Hay dùng 0,05. | $\alpha$ = 0,05: p = 0,011 → bác bỏ $H_0$; p = 0,20 → không bác bỏ. | 2, 7 |
| degrees of freedom | bậc tự do | Số giá trị còn được tự do thay đổi sau khi đã cố định vài con số tính từ dữ liệu. | 3 số có trung bình 4: chọn 2 và 6 thì số thứ ba buộc là 4 → 2 bậc tự do. | 7 |

## Nguồn

Nghĩa của thuật ngữ thống nhất với các phụ lục A–D (mỗi phụ lục có nguồn riêng) và với:

- Hyndman, R.J., Athanasopoulos, G. et al. *Forecasting: Principles and Practice, the Pythonic Way*: <https://otexts.com/fpppy/>
- Gneiting, T. & Raftery, A.E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102, 359–378.
- Lộ trình khoá: `lo-trinh/lo-trinh-forecasting.md`. Cột "Buổi": số đầu là buổi gặp từ lần đầu (dò trong
  `tai-lieu.md` buổi 1–13, bỏ mục "Đọc thêm"); các số sau là buổi dạy khái niệm theo lộ trình.
