# Lời thuyết trình — bộ slide "Dữ liệu cho dự báo" (buổi 1–15)

Mỗi mục "## <mã slide>" là lời người thuyết trình nói ở slide đó. `sinh_slide_du_lieu.py` chép vào ghi chú người nói
(Presenter View), khán giả không thấy. Thứ tự mục không quan trọng; số slide và tiêu đề lấy từ script. Bài đọc phát kèm cho
người học là `doc-kem.md`.

## tieu-de
Chào các bạn. Hôm nay chúng ta đi qua 15 buổi đầu của khoá, gom lại trong một bộ slide: dữ liệu cho dự báo.
Ba chữ ở dưới tiêu đề là ba việc chúng ta làm: hiểu dữ liệu, làm sạch nó, và đánh giá trung thực. Buổi 1 đến 3 là nền móng, buổi 4 đến 13 là hiểu và chuẩn bị dữ liệu, đây là phần làm kỹ nhất. Buổi 14 và 15 là đánh giá, và nó được gộp vào đây vì một lý do đơn giản: không chấm trung thực thì chúng ta không biết tiền xử lý có giúp thật hay không.

## ban-do
Đây là bản đồ của buổi hôm nay, sáu phần xoay quanh một tâm.
Phần A là khái niệm nền, mỗi khái niệm một slide. Phần B là các vấn đề dữ liệu hay gặp: mỗi vấn đề có một hình thật và ba thẻ, dấu hiệu, kiểm bằng gì, sửa thế nào. Phần C gom bảng tra, mười chỗ hay hiểu nhầm và từ điển Việt – Anh để các bạn tra nhanh. Phần D là đánh giá trung thực của buổi 14 và 15. Phần E ráp mọi thứ thành một quy trình tiền xử lý, tách rõ bước nào làm một lần, bước nào làm lại ở mỗi mốc cắt. Phần F điểm lại bộ dữ liệu đã dùng và những gì còn ở các buổi sau.
Mỗi khi mở một phần mới, bản đồ này sẽ hiện lại, sáng đúng phần đang nói.

## lo-trinh
Cả khoá có 44 buổi, đi từ thống kê cổ điển tới deep learning, foundation model và production. Nhìn dải ô ở dưới: 15 ô có màu là hôm nay, các ô xám là phần sau.
Ba con số lớn chia 15 buổi này: 3 buổi nền móng, 10 buổi hiểu và chuẩn bị dữ liệu, 2 buổi đánh giá trung thực.
Vì sao kéo hai buổi đánh giá vào đây? Vì nhiều bước tiền xử lý có "học" từ dữ liệu, ví dụ giá trị dùng để điền chỗ trống hay tham số của một phép biến đổi. Những bước đó chỉ đúng khi chúng ta biết nó được học trên đoạn nào. Mọi buổi sau đều đứng lên trên phần móng này.

## nhip
Cả giai đoạn dữ liệu đi theo một nhịp năm bước, các bạn nhìn năm vòng tròn: nhìn, đặt giả thuyết, kiểm bằng con số, xử lý, rồi kiểm lại.
Ví dụ ở khung dưới: thấy một giờ bằng 0 lúc rạng sáng Chủ nhật tháng 3. Đừng vội điền. Nghi là do đổi giờ mùa hè, đếm lại số giờ của ngày đó, đổi sang UTC rồi mới gộp, cuối cùng vẽ lại ngày đó để chắc.
(dừng) Bài học chính của cả phần này: không xoá, không điền khi chưa biết nguyên nhân. Một con số lạ có thể là lỗi, nhưng cũng có thể là sự kiện thật cần giữ lại.

## phan-a
Chúng ta vào phần A: khái niệm nền, đi theo thứ tự buổi 1 đến 13.
Năm trang đầu là "Từ nền", gom những từ dùng nhiều mà không có slide riêng. Sau đó mỗi slide là một khái niệm, và luôn trả lời bốn câu: để làm gì, là gì, con số cao hay thấp nghĩa là gì, và một ví dụ có số.

## tu-nen-1
Năm trang "Từ nền" là chỗ để tra: gặp từ lạ ở slide nào thì quay lại đây. Mỗi dòng có ba cột, từ, nghĩa, và một ví dụ nhỏ.
Trang này là các từ về dự báo và sai số. Dòng quan trọng nhất là sai số dự báo: sai số bằng thực tế trừ dự báo. Vậy sai số dương nghĩa là chúng ta dự báo thấp hơn thực tế, như 1,7 trừ 1,5 bằng cộng 0,2. Quy ước này dùng cho cả khoá, các bạn nhớ giúp.
Dòng thứ hai nên nhớ là MAE với RMSE: MAE bỏ dấu rồi lấy trung bình, sai số cộng 2 và trừ 4 thì MAE là 3. RMSE bình phương trước nên phạt nặng sai số lớn. Và NaN là "không biết", khác hẳn số 0.

## tu-nen-2
Trang 2 là các từ thống kê, dùng ở buổi 2, 8, 9 và 14.
Cặp từ nền nhất là mẫu và tổng thể. Mẫu là số liệu đang có trong tay, tổng thể là mọi giá trị nếu đo mãi. Mọi khoảng tin cậy và p-value đều là cách đoán về tổng thể từ một mẫu, nên khi thấy hai thứ đó, hãy tự hỏi: mẫu của mình có đại diện không.
Hai dòng nữa đáng nhớ: phân phối chuẩn, 95% nằm trong trung bình cộng trừ 1,96 lần độ lệch chuẩn; và sai số chuẩn, tức độ lệch chuẩn của chính con số ước lượng, như trung bình 25 giờ dao động cỡ 181 chia căn 25, xấp xỉ 36.

## tu-nen-3
Trang 3 là các từ về biến đổi, tính dừng và bất thường, dùng ở buổi 5, 6, 7 và 11.
Ba dòng nên nhớ. Nhiễu trắng: không tự tương quan ở trễ nào, quá khứ không giúp gì để đoán, như tung xúc xắc. Random walk: giá trị mới bằng giá trị cũ cộng một bước ngẫu nhiên, nên nó trôi đi không quay về. Và winsorize: kéo giá trị bị gắn cờ về mức hợp lý, ví dụ 50 kéo về 12, chứ không xoá. Cách này khớp với bài học ở slide nhịp: không xoá khi chưa chắc. Còn MAD là thước đo độ tản mà ngoại lai không kéo được.

## tu-nen-4
Trang 4 là tần số và bộ lọc của buổi 12. Với mọi bộ lọc, chúng ta hỏi hai câu trước: nó có nhìn tương lai không, và nó trễ bao nhiêu bước.
Nhìn dòng trailing và centered: trailing chỉ nhìn các điểm trước, centered lấy cả trước lẫn sau, tức dùng số tương lai. Dòng trễ pha: trung bình 13 điểm trễ 6 bước. Và dòng sosfilt với sosfiltfilt: sosfiltfilt chạy xuôi rồi chạy ngược, nên nó nhìn tương lai. Làm sạch bằng bộ lọc nhìn tương lai là một kiểu rò rỉ mà chúng ta sẽ gặp lại ở phần B.

## tu-nen-5
Trang cuối của "Từ nền": làm sạch, feature và đánh giá, dùng ở buổi 10, 13 và 15.
Ba dòng đáng nhớ nhất đều xoay quanh câu hỏi "lúc dự báo đã biết gì". Scaler phải fit trên phần học, không fit trên cả chuỗi. Ex-ante là chỉ dùng thông tin có lúc dự báo, như nhiệt độ dự báo; ex-post dùng cả số thật về sau, như nhiệt độ đo. Point-in-time là dùng số liệu đúng như lúc đó, ví dụ GDP bản công bố đầu tiên chứ không phải bản đã sửa. Cả ba đều là cách tránh để tương lai lọt vào quá khứ.

## du-bao-la-gi
Khái niệm đầu tiên: dự báo là gì. Có ba thứ hay bị gộp làm một, các bạn nhìn bảng bên trái.
Dự báo là điều sẽ xảy ra, mục tiêu là điều ta muốn, kế hoạch là việc ta làm để tới gần mục tiêu. Ở quán cà phê: dự báo tuần tới khoảng 1.900 ly, mục tiêu 2.500 ly. Nếu sếp muốn 2.500 nên bảo "dự báo 2.500", kho đặt hàng cho 2.500, tuần đó bán 1.900, thừa 600 ly, và không ai còn biết dự báo đúng hay sai. Muốn đạt mục tiêu thì sửa kế hoạch, đừng sửa dự báo.
Bảng bên phải là bốn điều quyết định một thứ dự báo được tới đâu. Điện ngày mai thoả cả bốn. Tỷ giá chỉ thoả một, là có nhiều dữ liệu, vì người ta mua bán theo dự báo nên dự báo tự làm mình sai.

## goc-tam
Hai từ các bạn sẽ nghe suốt khoá: gốc dự báo và tầm dự báo.
Nhìn hình: vạch cam là gốc, tức lúc ra dự báo. Bên trái vạch là những gì đã biết, dải xanh bên phải là phần phải đoán. Tầm h là đếm từ gốc bao nhiêu bước. Đứng ở 00:00 thứ Hai dự báo 168 giờ tới thì h chạy từ 1, là 01:00, tới 168, là giờ cuối Chủ nhật. h càng lớn càng xa gốc, thường sai số càng lớn.
(dừng) Mọi quy tắc chống rò rỉ về sau đều quy về đúng một câu: chỉ được dùng thứ nằm bên trái gốc.

## code-b01-mua-vu
Slide code đầu tiên, từ buổi 1: dữ liệu điện của một hộ, đo từng phút.
Dòng 3 đến 6 đọc số đo và ghép ngày với giờ thành mốc thời gian. Dòng 8 và 9 gộp về từng giờ bằng resample rồi lấy trung bình. Vì số đo là kW, trung bình kW trong một giờ chính là số kWh của giờ đó. Giờ nào thiếu hơn 30 phút thì để trống, không đoán. Dòng 10 và 11 dùng groupby để lấy trung bình theo giờ trong ngày, rồi idxmin, idxmax tìm giờ thấp nhất và cao nhất. Dòng 12 và 13 so ngày thường với cuối tuần.
Kết quả: thấp nhất lúc 4 giờ sáng, cao nhất lúc 20 giờ, và cuối tuần dùng nhiều hơn ngày thường. Nhịp lặp đều này gọi là mùa vụ, và chính nó làm điện dự báo được.

## mo-hinh
Mô hình là một cách tính ra dự báo; tham số là các con số bên trong nó. "Mai bằng trung bình 7 ngày qua" là một mô hình có một tham số, là số 7. Khớp, hay học, là chọn tham số từ dữ liệu.
Nhìn thanh ở trên: phần học là đoạn mô hình được thấy, kỳ chấm là đoạn giấu đi, nằm sau gốc dự báo. Vì sao phải giấu? Sai số đo trên phần học, gọi là phần dư, luôn đẹp hơn thật. Mô hình đủ nhiều tham số có thể khớp gần hoàn hảo những gì đã thấy mà dự báo cái mới vẫn tệ. Đó là học thuộc: thuộc đề cũ được 10 điểm, đề mới chỉ 6.
Nên trong cả khoá, mọi chỉ số chính xác đều tính trên kỳ chấm; phần dư chỉ để chẩn đoán.

## phieu-6-o
Trước khi mở dữ liệu, chúng ta điền phiếu 6 ô. Ví dụ là một công ty mua trước điện cho một khu dân cư.
Ô 1 là quyết định, và năm ô còn lại đều suy ra từ nó: cuối Chủ nhật đặt mua điện theo giờ cho 7 ngày tới. Từ đó ra ô 2, biến mục tiêu là kWh mỗi giờ, và ô 3, tầm dự báo 1 đến 168 giờ. Ô 5, mốc cắt: lúc dự báo chỉ có số đo tới 23:59 Chủ nhật và thời tiết bản dự báo, chưa có thời tiết thật.
Hai ô các bạn sẽ gặp lại ngay trong vài slide tới: ô 4, độ chi tiết, quyết định cách chấm; ô 6, chi phí sai hai chiều, thiếu mất khoảng 4 đồng mỗi kWh, thừa mất khoảng 1 đồng, quyết định nên báo con số nào.

## baseline
Giả sử một mô hình báo sai số 0,38. Tốt hay xấu? Chưa nói được gì, vì không có gì để so. Giống như bạn được 7 điểm: cả lớp được 9 thì 7 là kém, cả lớp được 4 thì 7 là giỏi. Baseline là điểm của cả lớp: cách dự báo đơn giản nhất, ai cũng làm được, dùng làm mốc.
Hình này là một chuỗi M4 theo ngày. Trên chuỗi này seasonal naive thắng vì bắt được nhịp tuần. Nhưng trên cả tập M4 theo ngày thì ngược lại: naive có MASE 0,835 và drift 0,810, cả hai đều thắng seasonal naive ở 1,077. Nên quy tắc của khoá là mô hình phải thắng cả bốn baseline trên backtest, và bảng kết quả luôn có seasonal naive.
Thêm một điều: độ trễ của baseline phải ít nhất bằng tầm dự báo. Dự báo 7 ngày mà dùng "cùng giờ hôm qua" là đã dùng số chưa có tại gốc; phải dùng "cùng giờ tuần trước".

## code-b14-baseline
Đây là bốn baseline viết bằng NumPy, lấy từ buổi 14. Mỗi hàm nhận lịch sử y và trả về 14 bước dự báo.
Dòng 3 và 4: lặp mức trung bình cả lịch sử 14 lần bằng np.repeat. Dòng 6 và 7: lặp giá trị cuối. Dòng 9 đến 11 là seasonal naive: lấy m giá trị cuối, ở đây m bằng 7 ngày, tức một vòng mùa vụ, rồi lặp lại vòng đó. Dòng 13 đến 15 là drift: tính độ dốc từ điểm đầu tới điểm cuối, rồi đi tiếp theo đường thẳng đó.
Kết quả, MASE trung vị trên 1.000 chuỗi M4 theo ngày: trung bình 8,85, naive 0,835, seasonal naive 1,077, drift 0,810. Để ý baseline mean tệ hẳn, còn baseline thắng lại không phải seasonal naive.

## bon-baseline
Để chắc là hiểu bốn baseline, chúng ta tính tay trên chuỗi 10, 14, 12, 16, 14, 18, mùa dài 2, dự báo 2 bước tới.
Đọc bảng theo cột "giả định": mỗi baseline là một giả định đơn giản về tương lai. Mean: tổng 84 chia 6 bằng 14, nên dự báo 14 và 14. Naive: lấy số cuối, 18 và 18. Seasonal naive: lấy cùng vị trí ở mùa trước, ra 14 rồi 18. Drift: độ dốc là 18 trừ 10, chia 5, bằng 1,6 mỗi bước, nên ra 19,6 rồi 21,2.
Hai quy tắc ở dưới các bạn đã nghe: độ trễ ít nhất bằng tầm dự báo, và phải thắng cả bốn.

## code-b01-baseline
Quay lại dữ liệu điện buổi 1, lần này là MAE và bốn baseline cho tầm 168 giờ.
Dòng 4 đến 7 là hàm MAE: lấy trị tuyệt đối từng sai số rồi trung bình, bỏ qua giờ không có số đo. Dòng 10 là naive, lặp số cuối cùng đã biết. Dòng 11 là trung bình mọi giờ đã biết. Dòng 12 là seasonal naive: cùng giờ tuần trước, lấy 168 giờ cuối bằng iloc. Dòng 13 và 14 là trung bình 4 tuần: xếp 4 tuần gần nhất thành 4 hàng bằng reshape, rồi lấy trung bình theo cột, tức mỗi giờ trong tuần là trung bình của 4 lần.
Kết quả chấm cuốn năm 2010, tính bằng kWh mỗi giờ: trung bình 4 tuần 0,490, tuần trước 0,576, trung bình 0,652, giờ trước 0,770. Con số 0,490 là mốc mọi mô hình sau phải vượt.

## sai-so-ao
Giờ đến một lỗi rất hay gặp. Sai số ảo là sai số đo trên chính dữ liệu đã dùng để dựng dự báo, nên nó đẹp hơn thật.
Nhìn hình: cùng một mô hình "bảng lịch". Khi bảng được tính cả trên các giờ đang chấm, MAE là 0,380, đứng đầu bảng. Chấm trung thực thì MAE là 0,508, thua cả trung bình 4 tuần ở 0,490. Khoảng cách giữa hai con số càng lớn thì mô hình càng học thuộc thay vì học quy luật.
Có một phép thử rẻ: đổi số đo ở giai đoạn chấm rồi chạy lại. Dự báo trung thực không được đổi theo; nếu đổi, mô hình đã nhìn thấy đáp án. Cách chấm đúng là dự báo cuốn, ở slide ngay sau.

## du-bao-cuon
Dự báo cuốn là chấm đúng như lúc dùng thật. Bốn bước bên phải: chọn một gốc, ví dụ 00:00 thứ Hai; dựng dự báo chỉ từ dữ liệu trước gốc; dự báo 168 giờ tới rồi mới mở số thật để tính sai số; dời gốc sang thứ Hai sau và làm lại.
Nhìn hình bên trái: mỗi hàng là một gốc. Phần xám là dữ liệu được dùng, ô xanh là tuần được dự báo và chấm. Xuống mỗi hàng, gốc dời thêm một tuần, và phần xám dài thêm. Buổi 1 làm vậy với 46 thứ Hai năm 2010, rồi lấy trung bình sai số.
Làm như vậy trên quá khứ gọi là backtest. Buổi 15 sẽ tổng quát nó thành rolling origin, với các lựa chọn học trên đoạn nào, bỏ trống bao nhiêu, và học lại bao lâu một lần.

## code-b01-du-bao-cuon
Đây là mô hình bảng lịch và vòng dự báo cuốn.
Dòng 3 đến 7 dựng bảng lịch: với mỗi tổ hợp tuần trong năm, thứ, và giờ, lấy một trung bình, bằng groupby nhiều khoá. Dòng 8 và 9 tra bảng đó cho các giờ cần dự báo, dùng reindex; khoá nào không có thì ra NaN. Dòng 12 và 13: mỗi thứ Hai là một gốc, sinh bằng date_range cách nhau 168 giờ. Dòng 14 là dòng quan trọng nhất (chỉ vào dòng 14): bảng chỉ được khớp trên dữ liệu có chỉ số nhỏ hơn gốc. Dòng 15 và 16 ghép dự báo của mọi tuần để chấm.
Kết quả: nếu lập bảng từ cả 4 năm, MAE là 0,380, đó là sai số ảo. Chấm cuốn 46 tuần thì 0,508, thua trung bình 4 tuần ở 0,490.

## do-chi-tiet
Nhớ ô 4 của phiếu, độ chi tiết. Slide này cho thấy vì sao nó quan trọng.
Nhìn hình: cùng ba cách dự báo, chấm ở hai mức. Theo giờ, trung bình 4 tuần thắng với MAE 0,490, bảng lịch 0,508. Cộng lên tổng tuần thì thứ hạng đảo: bảng lịch 16,4 kWh mỗi tuần, thắng xa trung bình 4 tuần ở 27,9.
Vì sao? Khi cộng lên tuần, phần lệch lên và lệch xuống do nhiễu bù trừ nhau. Chỉ những lệch cùng một chiều trong nhiều ngày mới dồn lại. Vậy nếu công ty mua điện theo giờ thì chấm theo giờ, nếu ký hợp đồng theo tuần thì chấm theo tuần. Phải chấm ở đúng mức của quyết định trước khi chọn mô hình.

## code-b01-tong-tuan
Code cho phép so ở hai mức. Bảng cuon có mỗi dòng một giờ, cột goc, cột y và các cột dự báo.
Dòng 4 đến 7 là MAE như trước, bỏ giờ trống. Dòng 11 cộng 168 giờ của mỗi gốc thành tổng tuần. Chú ý min_count bằng 1: nhóm toàn trống thì ra NaN chứ không ra 0. Dòng 12 và 13 hỏi từng tuần có đủ số đo mọi giờ không; tuần thiếu thì gán trống, không chấm, vì tổng của một tuần thiếu giờ sẽ thấp giả. Dòng 14 và 15 tính MAE ở hai mức.
Kết quả: theo giờ, trung bình 4 tuần 0,490 thắng bảng lịch 0,508. Theo tổng tuần, bảng lịch 16,4 thắng xa trung bình 4 tuần 27,9 kWh mỗi tuần.

## quantile
Ô 6 của phiếu: thiếu và thừa đắt khác nhau. Lúc đó con số nên báo không còn là trung bình nữa, mà là một quantile.
Quantile p là giá trị nhỏ nhất mà ít nhất tỷ lệ p số liệu nằm dưới hoặc bằng nó; trung vị là quantile 0,5. Nhìn hình: đây là đường tích luỹ. Đi ngang từ tỷ lệ trên trục dọc tới đường cong, rồi thả xuống trục ngang là ra quantile.
Khi thiếu mất 4 đồng, thừa mất 1 đồng, ta đặt dự báo ở quantile 4 chia 4 cộng 1, bằng 0,8: chấp nhận thừa để ít khi thiếu. Ở buổi 1, làm vậy giảm chi phí 18,6% dù MAE lại tệ hơn. Vậy chọn mô hình theo MAE sẽ chọn sai khi hai chiều đắt khác nhau.

## newsvendor
Bài toán này có tên: newsvendor, người bán báo. Mỗi sáng đặt số báo một lần; thiếu thì mất khách, thừa thì lỗ tiền in. Tiệm bánh mì cũng thế: họ làm dư ra một chút, vì mất một khách đắt hơn lỗ chút tiền bột. Công ty mua điện ở buổi 1 cũng vậy: thiếu mất Cu đồng mỗi kWh, thừa mất Co đồng.
Lượng nên đặt là quantile Cu chia tổng Cu cộng Co. Nhìn cột thang: hai chiều bằng nhau thì báo trung vị, thiếu đắt gấp 4 thì báo quantile 0,8. Trên 10 ngày mẫu: mua 8 kWh tốn 33 đồng, mua 9 tốn 28, ít nhất, mua 10 lại tốn 33.
Dự báo kiểu này chấm bằng pinball loss mức tau: thiếu mỗi đơn vị phạt tau, thừa mỗi đơn vị phạt 1 trừ tau. Tau 0,8, thật 10, báo 8: thiếu 2, phạt 1,6. Cách phạt này có đáy đúng ở quantile tau.

## code-b01-newsvendor
Slide code này kiểm lại bằng số điều vừa nói.
Dòng 3 đến 6: với 10 ngày nhu cầu, thử từng mức mua từ 6 đến 12, tính tiền mất; np.clip cắt số âm về 0 để tách riêng phần thiếu, phạt 4, và phần thừa, phạt 1. Dòng 7 tính quantile 0,8 theo kiểu đếm tay. Dòng 9 đến 12 là hàm tiền mất trên dữ liệu thật. Dòng 14 và 15 là chỗ cần để ý: phần cộng thêm lấy từ quantile 0,8 của sai số năm 2009, không nhìn năm 2010. Dòng 16 so tiền mất năm 2010 trước và sau.
Kết quả: mua 9 kWh rẻ nhất, 28 đồng, đúng bằng quantile 0,8, không phải trung bình 7,7. Trên dữ liệu thật, cộng thêm 0,455 kWh làm tiền mất từ 1,213 xuống 0,987, giảm 18,6%, trong khi MAE tệ đi.

## phan-phoi
Quantile là một cách đọc phân phối. Trước khi tóm số liệu bằng một con số, chúng ta nhìn hình dạng của nó.
Hình có hai phần: histogram đếm số lần gặp mỗi khoảng giá trị; đường tích luỹ cho biết bao nhiêu phần số liệu nằm dưới mỗi mốc. Đây là lượt thuê xe theo giờ. Histogram lệch phải: phần lớn giờ vắng, vài giờ rất đông, đuôi phải kéo dài.
Chính cái đuôi đó kéo trung bình lên 189, trong khi trung vị chỉ 142. Hệ số lệch dương báo đuôi phải dài. Độ lệch chuẩn đo số liệu tản rộng cỡ nào, cùng đơn vị với dữ liệu. Hai con số trung bình và trung vị cách nhau thế này là dấu hiệu phải hỏi: mình cần báo con số nào.

## code-b02-quantile
Sang buổi 2. Code này tính quantile như đếm tay, rồi thấy trung bình và trung vị lệch nhau trên dữ liệu thật.
Dòng 6 và 7: chín giờ, xếp tăng dần là 2, 3, 5, 6, 8, 9, 12, 18, 36. Dòng 8: quantile 0,8 kiểu đếm tay, vị trí là 0,8 nhân 9 bằng 7,2, làm tròn lên số thứ 8, tức 18. Dòng 9: mặc định của NumPy nội suy giữa hai số kề nhau, nên ra 14,4. Hai cách cho hai số khác nhau, nên khi so với tính tay các bạn nhớ ghi rõ method. Dòng 11 đến 13 đọc lượt thuê theo giờ của Capital Bikeshare, dòng 14 so ba con số.
Kết quả: trung bình 189, trung vị 142, quantile 0,9 khoảng 451 lượt mỗi giờ.

## do-lech-chuan
Ba con số nền của thống kê: trung bình, phương sai, độ lệch chuẩn.
Nhìn hình với ví dụ 2, 4, 6. Trung bình là 4. Khoảng cách tới trung bình là trừ 2, 0, 2; tổng bình phương là 8; chia cho n trừ 1, tức chia 2, ra phương sai 4. Căn của phương sai là độ lệch chuẩn, bằng 2, cùng đơn vị với dữ liệu.
Từ đây có z-score: giá trị trừ trung bình, chia độ lệch chuẩn. Trung bình 10, độ lệch chuẩn 2, giá trị 16 thì z bằng 3, tức rất xa, nghi ngoại lai. Đây là gốc của quy tắc 3 sigma ở buổi 11, khoảng cộng trừ 1,96 s ở buổi 2, và CV ở buổi 9. Chuẩn hoá z-score bỏ mức và biên độ, chỉ giữ hình dạng: 100, 300, 100, 300 thành trừ 1, 1, trừ 1, 1.

## con-so-bao
Vậy nên báo trung bình, trung vị hay quantile? Câu trả lời nằm ở cách sai lệch bị tính tiền, gọi là hàm mất mát.
Nhìn hình: ba đường phạt trên lượt thuê xe, trục ngang là con số ta báo, trục dọc là mức phạt; chỗ cần nhìn là đáy của mỗi đường. Phạt bình phương, lệch 2 phạt 4, lệch 10 phạt 100, nên rất sợ lệch xa; đáy ở 189,46, chính là trung bình. Phạt tuyệt đối, lệch bao nhiêu phạt bấy nhiêu; đáy ở 142, trung vị. Pinball với tau 0,9; đáy ở 452, quantile 0,9.
Ba cách phạt, ba đáy khác nhau. Đây là lý do buổi 14 nói: chọn chỉ số là chọn dự báo.

## code-b02-pinball
Kiểm lại ba cách phạt trên chín con số nhỏ.
Dòng 5 tính độ lệch chuẩn mẫu, ddof bằng 1 nghĩa là chia cho n trừ 1. Dòng 7 đến 9 là hàm pinball: sai số dương, tức dự báo thấp, phạt tau lần; sai số âm phạt 1 trừ tau lần, viết bằng np.where. Dòng 11 đến 14 thử báo cùng một số c cho cả 9 giờ, với ba giá trị c: 8 là trung vị, 11 là trung bình, 18 là quantile 0,8. Mỗi c tính ba mức phạt.
Kết quả: độ lệch chuẩn 10,57. Phạt tuyệt đối thấp nhất ở c bằng 8, là 6,56. Bình phương thấp nhất ở c bằng 11, là 99,3. Pinball 0,8 thấp nhất ở c bằng 18, là 3,40. Mỗi cách phạt chọn đúng con số của nó.

## khoang
Một con số chưa đủ; nhiều khi chúng ta báo cả khoảng. Khoảng dự báo 95% hứa rằng cứ 100 lần thì khoảng 95 lần giá trị thật rơi vào trong. Tỷ lệ phủ đo lời hứa đó có giữ được không.
Nhìn hình: khoảng cộng trừ 1,96 lần độ lệch chuẩn, dựng từ lượt thuê năm 2011. Ngay trên năm 2011, tức trong mẫu, nó phủ 96,4%. Sang năm 2012 chỉ phủ 72,5%, vì lượt thuê trung bình mỗi giờ tăng từ 143,8 lên 234,7; gần 3 trên 10 giờ vượt cận trên. Vì vậy phải báo riêng hai đuôi để biết lệch phía nào.
Dữ liệu lệch phải thì dùng quantile thực nghiệm để hai đuôi cân. Nhưng không cách nào cứu được khi tương lai dịch mức. Luôn chấm khoảng ngoài mẫu.

## khoang-tin-cay
Hai loại khoảng hay bị nhầm. Khoảng dự báo trả lời: một giá trị mới, như giờ tới, sẽ rơi vào đâu. Khoảng tin cậy trả lời: một con số tóm tắt, như trung bình thật, nằm ở đâu.
Nhìn hình: dù từng giá trị lệch phải, trung bình của nhiều giá trị vẫn gần hình chuông, đó là định lý giới hạn trung tâm. Và nó dao động theo độ lệch chuẩn chia căn n. Với lượt thuê xe, độ lệch chuẩn 181,4: trung bình 25 giờ dao động 36,1, 100 giờ còn 18,2, 400 giờ còn 9,1. n gấp 4 thì hẹp một nửa. Khoảng dự báo thì không hẹp về 0, vì từng giờ vẫn lên xuống như cũ.
Còn chữ "95%" của khoảng tin cậy nói về quy trình: dựng 20 khoảng từ 20 mẫu thì khoảng 19 khoảng chứa trung bình thật.

## code-b02-ty-le-phu
Code này dựng khoảng từ năm 2011 theo hai cách rồi chấm trên năm chưa dùng.
Dòng 5 đến 7 là hai cách: công thức cộng trừ 1,96 s, và quantile thực nghiệm lấy thẳng mốc 2,5% và 97,5%. Dòng 10 và 11: mỗi giờ trong ngày một khoảng riêng, chỉ dựng từ 2011. Dòng 13 dùng merge theo cột giờ để gắn khoảng vào từng dòng. Dòng 14 tính tỷ lệ phủ, dòng 15 đếm riêng hai đuôi.
Kết quả: trên 2011, cộng trừ 1,96 s phủ 96,4%, quantile phủ 95,3%, cả hai đều đẹp. Trên 2012 chỉ còn 72,5% và 70,1%, phần vượt cận trên là 27,4% và 29,3%. Cách nào cũng hỏng như nhau, vì mức đã dịch lên.

## kiem-dinh
Kiểm định giả thuyết hỏi: nếu H0, giả định "không có gì đặc biệt", là đúng, thì dữ liệu như ta thấy hiếm cỡ nào? Con số đó là p-value. p nhỏ hơn mức ý nghĩa chọn trước, thường 0,05, thì bác bỏ H0.
Ví dụ tung đồng xu 10 lần được 9 ngửa. Có 1.024 dãy kết quả, 10 dãy có đúng 9 ngửa và 1 dãy 10 ngửa, nên p bằng 11 trên 1.024, xấp xỉ 0,011, nhỏ hơn 0,05: bác bỏ "đồng xu cân đối".
Hình dùng kiểm định hoán vị: xáo nhãn ngày làm việc, ngày nghỉ hàng nghìn lần, xem chênh lệch thật nằm ở đâu so với các lần xáo. (dừng) Ba chỗ hay sai: không bác bỏ không có nghĩa H0 đúng; p không phải xác suất H0 đúng; có ý nghĩa thống kê không có nghĩa là chênh lệch lớn.

## code-b02-hoan-vi
Kiểm định hoán vị viết trong mười dòng.
Dòng 5 tính chênh lệch thật giữa hai nhóm ngày. Dòng 6 cố định seed để chạy lại ra đúng p. Dòng 8 đến 10: xáo nhãn 9.999 lần bằng rng.permutation, giữ nguyên số ngày mỗi loại, và đếm số lần chênh lệch sau xáo lớn bằng hoặc hơn chênh lệch thật. Nếu nhãn vô nghĩa thì xáo hay không cũng như nhau. Dòng 11: p là tỷ lệ lần xáo lệch cỡ thật. Dòng 14 và 15 áp vào ngày làm việc so với ngày nghỉ năm 2012.
Kết quả: ngày làm việc hơn ngày nghỉ 456 lượt mỗi ngày, p bằng 0,025, bác bỏ H0. Thứ Bảy trừ Chủ nhật chênh tới 695 mà p lớn hơn 0,05. Chênh lớn chưa chắc là có ý nghĩa. Một lưu ý: phép này giả định các ngày độc lập, nên với chuỗi tự tương quan p thật thường lớn hơn.

## bootstrap
Bootstrap ước lượng độ bấp bênh của một con số mà không cần công thức: rút lại từ chính mẫu nhiều lần và tính lại con số đó. Các bước cụ thể ở slide sau; slide này nói về chỗ chuỗi thời gian khác dữ liệu thường.
Nhưng chuỗi thời gian có tự tương quan. Giờ này đông thì giờ sau gần như chắc cũng đông, nên giờ sau mang ít thông tin mới. Rút từng điểm làm mất điều đó, và khoảng hẹp giả. Nhìn hình: trục ngang là độ dài khối, trục dọc là tỷ lệ khoảng chứa trung bình thật trên mô phỏng AR(1). Rút từng điểm chỉ 60,3%, thay vì 95%. Block bootstrap rút cả khối liền nhau: khối 20 lên 89,3%. Nhưng khối 40 lại tụt còn 81,3%, nên hãy thử vài độ dài và báo độ nhạy.

## bootstrap-buoc
Đây là bootstrap đi từng bước, vì chỗ này rất hay nhớ nhầm.

(chỉ vào hàng ô trên) Bước một, có một mẫu thật, ví dụ 5 ngày: 12, 15, 11, 30, 14, trung bình 16,4. Bước hai, rút lại đủ 5 số, có hoàn lại: một ngày có thể được rút hai lần, ngày khác không được rút lần nào. Bước ba, tính trung bình của mẫu vừa rút. Bước bốn, lặp như vậy vài nghìn lần, được vài nghìn trung bình. Bước năm, xếp chúng theo thứ tự và lấy quantile 0,025 và 0,975: đó là khoảng tin cậy 95%. (dừng) Không có chỗ nào nhân 1,96 cả: bootstrap lấy thẳng hai đầu của các trung bình.

Bảng trái là ba lần rút đầu tiên. Lần 1 và 2 không trúng số 30 nên trung bình chỉ 13,0 và 12,6; lần 3 trúng thì lên 16,4. Chính sự dao động đó cho ta độ bấp bênh.

Bên phải là rút khối dài 2: rút ba điểm bắt đầu, lấy cả khối hai ngày liền nhau, nối lại rồi cắt còn 5 số. Ngày 30 và ngày 14 ngay sau nó vẫn đi cùng nhau, nên mối liên hệ giữa hai ngày liền nhau được giữ. Dữ liệu có tự tương quan thì phải rút kiểu này.

## code-b02-block-bootstrap
Code bootstrap với hai chế độ: từng điểm và theo khối.
Dòng 5 và 6: khối dài 1 thì rút ngẫu nhiên có hoàn lại từng vị trí bằng rng.integers. Dòng 8 đến 10: rút điểm đầu của các khối, cộng thêm np.arange để thành các khối liền nhau, rồi nối lại. Dòng 11: lấy quantile 0,025 và 0,975 của 999 trung bình, ra khoảng 95%. Dòng 13 đến 16 chạy trên 300 chuỗi AR(1) với rho bằng 0,7, trung bình thật bằng 0, và đếm bao nhiêu khoảng chứa số 0.
Kết quả: rút từng điểm chỉ 60,3% khoảng chứa trung bình thật. Khối 10 lên 89,0%, khối 20 là 89,3%, khối 40 tụt còn 81,3%. Rút khối sửa được phần lớn độ tự tin giả, nhưng không về đúng 95%.

## utc
Sang buổi 3: thời gian. Một con số giờ chưa đủ, phải có múi giờ.
UTC là giờ chung, không đổi theo mùa: 07:00 ở Hà Nội là 00:00 UTC. Thời điểm naive không ghi múi giờ, aware thì có ghi. Rắc rối đến từ giờ mùa hè. Ở New York, ngày 10/3/2024 đồng hồ nhảy từ 1:59 lên 3:00, nên giờ 2:00 không tồn tại. Ngày 3/11 thì giờ 1:00 xảy ra hai lần.
Nhìn hình: trục ngang là giờ UTC chạy đều, trục dọc là đồng hồ New York. Các bạn thấy một đoạn nhảy qua, "không tồn tại", và một đoạn lùi lại, "xảy ra 2 lần". Cách sửa: gắn đúng múi giờ rồi đổi sang UTC trước khi gộp hay ghép bất cứ thứ gì.

## code-b03-dst
Code này cho thấy một giờ New York có thể ứng với một, không, hoặc hai thời điểm UTC.
Dòng 4 và 5 liệt kê bốn giờ quanh hai ngày vặn đồng hồ năm 2024. Dòng 7 thử cả hai cách hiểu, giờ hè và giờ đông, cho trường hợp giờ lặp. Dòng 9 và 10 dùng tz_localize để gắn múi giờ New York, biến một con số giờ thành một thời điểm thật. Dòng 11 dùng tz_convert đổi sang UTC. Dòng 12 và 13: giờ bị nhảy qua thì pandas báo lỗi, ta bắt lỗi và bỏ qua.
Kết quả: ngày 10/3, 01:30 ra 06:30 UTC, 02:30 không tồn tại, 03:30 ra 07:30 UTC. Còn 01:30 ngày 3/11 có hai đáp án, 05:30 hoặc 06:30 UTC. Đây là lý do đếm theo giờ địa phương sẽ ra một giờ bằng 0 và một giờ gấp đôi.

## resample
Đổi tần suất, ví dụ từ chuyến lẻ sang số chuyến mỗi giờ, phải trả lời ba câu.
Câu 1: khoảng nào. Nhìn hình: closed chọn mốc biên thuộc khoảng nào, label chọn đặt tên khoảng bằng mốc đầu hay cuối. Mặc định của pandas với giờ là đóng trái, nhãn trái: từ 9:00 tới trước 10:00, tên "9:00". Bốn chuyến lúc 9:00, 9:40, 10:00, 10:20 cho ô "9:00" 2 chuyến, ô "10:00" 2 chuyến; chuyến 10:00 thuộc ô sau.
Câu 2: gộp thế nào. Số lượng thì cộng; trạng thái như nhiệt độ thì trung bình hoặc lấy giá trị cuối. Câu 3: giờ trống là gì. Với số đếm, giờ trống là 0; với số đo, giờ trống là NaN, không biết.

## code-b03-resample
Code này đi qua đúng ba câu hỏi vừa rồi.
Dòng 3 đến 5: ba sự kiện lúc 00:10, 00:50 và 02:20. Dòng 6 resample rồi cộng: giờ 01:00 không có gì, ra 0. Dòng 7 resample rồi lấy trung bình: giờ đó ra NaN. Dòng 9 là cách hay gặp khác: floor về đầu giờ rồi groupby; cách này không tự thêm giờ trống, nên giờ 01 biến mất khỏi chuỗi. Dòng 11 đến 13 sinh lưới giờ tháng 3 theo múi giờ New York và đếm.
Kết quả: cộng ra 3, 0, 5; trung bình ra 1,5, NaN, 5; floor chỉ ra 3 và 5, mất hẳn một giờ. Và tháng 3 có 743 giờ, không phải 744, vì ngày 10/3 chỉ dài 23 giờ.

## merge-asof
Ghép hai nguồn theo thời gian, ví dụ gắn giá hay thời tiết vào từng dòng, dùng merge_asof: mỗi dòng lấy giá trị gần nhất về thời gian từ bảng kia.
Nhìn hình: dòng lúc 10:00, bảng giá có số lúc 9:30 và 10:30. Hướng backward, cũng là mặc định, lấy giá 9 của lúc 9:30, tức số đã có, đúng. Hướng forward lấy giá 10 của lúc 10:30, tức lấy tương lai. Đây là rò rỉ, và nó cho kết quả đẹp giả.
Hai điều thêm: đặt tolerance để không ghép một con số quá cũ, và luôn đưa cả hai nguồn về UTC trước khi ghép, như slide múi giờ vừa nói.

## dang-dai
Slide cuối của buổi 3: dạng dữ liệu mà mọi buổi sau nhận vào.
Nhìn bảng bên trái: dạng dài có ba cột. unique_id là chuỗi nào, ds là khi nào theo UTC, y là giá trị bao nhiêu. Bảng bên phải là dạng rộng, mỗi chuỗi một cột: dễ nhìn, nhưng thêm chuỗi là thêm cột. Tháng 3/2024 có 259 khu vực taxi có chuyến, thì dạng rộng có 259 cột, còn dạng dài vẫn ba cột, chỉ nhiều dòng hơn.
Bảng sạch khi thoả ba điều: mỗi cặp unique_id và ds chỉ một dòng, đủ mọi mốc thời gian, không trùng. Mọi chuỗi trải lên cùng một lưới UTC, và tháng 3/2024 có 743 giờ, vì New York mất một giờ ngày đổi giờ.

## code-b03-dang-dai
Giờ chúng ta dựng đúng cái bảng ba cột vừa nói. Dòng 4 làm tròn giờ đón, đã đổi sang UTC, xuống đầu giờ. Dòng 5 đếm chuyến theo khu vực và giờ, nhưng chỉ ra những giờ có chuyến; giờ vắng thì biến mất hẳn khỏi bảng.

Vì vậy dòng 6 và 7 dựng lưới giờ UTC của cả tháng 3 theo lịch New York, lấy mốc đầu, không lấy mốc cuối. Dòng 8 đến 10 là chỗ quan trọng: MultiIndex.from_product tạo mọi cặp khu vực nhân giờ, reindex trải số đếm lên lưới đó và điền 0 cho giờ không có chuyến. Đây là số đếm nên 0 là đúng; nếu là số đo như nhiệt độ thì phải để NaN.

Kết quả: 192.437 dòng, đúng bằng 259 khu vực nhân 743 giờ, không mất chuyến nào. Và 53,7% số ô bằng 0, tức hơn một nửa bảng là giờ vắng khách.

## mua-vu
Bắt đầu phần đọc biểu đồ, trước hết cần ba từ. Nhìn hình: hàng trên là xu hướng, mức chung đi lên dần. Hàng giữa là mùa vụ, lặp đúng mỗi 12 bước, các vạch dọc cách đều nhau. Hàng dưới là chu kỳ: cũng lên xuống, nhưng vòng dài vòng ngắn khác nhau.

Chỗ phân biệt là con số m cố định. Lượt thuê xe đông lúc 8h và 17h mỗi ngày làm việc là mùa vụ với m bằng 24, nên biết trước giờ đỉnh. Kinh tế tăng rồi suy thoái là chu kỳ, không ai hẹn trước lúc nó đổi chiều. Vì vậy mùa vụ là phần dự báo được nhờ lịch, còn chu kỳ khó hơn nhiều.

Nhớ gọn: mùa vụ lặp đều, biết trước lúc lặp; chu kỳ lên xuống mà không biết khi nào lặp lại. Và “mùa” ở đây là mọi vòng lặp theo lịch: ngày, tuần, năm, không chỉ xuân, hạ, thu, đông.

## doc-hinh
Có ba khái niệm rồi, giờ cần một cách đọc hình để thấy chúng. Năm bước, áp cho mọi biểu đồ. Thử ngay với heatmap này.

Bước một, trục ngang là giờ từ 0 đến 23. Bước hai, trục dọc là thứ Hai tới Chủ nhật, còn màu là lượt thuê trung bình mỗi giờ, thang màu bên phải. Bước ba, tối là thấp, sáng là cao. Bước bốn, nhìn vào hai cột sáng lúc 8h và 17h: chúng chạy suốt năm ngày làm việc rồi tắt ở cuối tuần, còn cuối tuần sáng đều giữa ngày. Bước năm, kết luận một câu: có mùa vụ ngày lồng trong mùa vụ tuần. Để ý tiêu đề hình chính là câu kết luận đó, quy ước của cả khoá.

Một lưu ý: heatmap chỉ cho trung bình mỗi ô, không cho độ tản, nên hai ô chênh nhau chút ít chưa chắc là thật. Độ tản thì phải xem boxplot, lát nữa sẽ gặp.

## code-b04-ba-mau-hinh
Trước khi vẽ, ta tính tay để thấy mùa vụ bằng số. Dòng 4 đến 6 là hai tuần lượt thuê, đơn vị trăm lượt mỗi ngày, từ thứ Hai tới Chủ nhật; tuần sau cao hơn tuần trước. Dòng 7 lấy trung bình mỗi tuần, keepdims để giữ dạng cột mà trừ được cả bảng: ra 10 và 12, đó là xu hướng. Dòng 8 trừ trung bình đi, phần còn lại của hai tuần giống hệt nhau: 0, 2, 2, 2, 4, âm 4, âm 6. Phần lặp lại y nguyên đó chính là mùa vụ tuần.

Sang dữ liệu thật, dòng 11 và 12 gộp giờ thành ngày và tháng. min_count bằng 12 để ngày có dưới 12 giờ số liệu thì để trống, thay vì ra một tổng thấp giả. Dòng 13 lấy ba ngày thấp nhất: những ngày rơi sát 0 mà hình theo tháng giấu mất.

## bo-bieu-do
Không có biểu đồ nào nói hết, nên buổi 4 dùng bộ 8 biểu đồ, mỗi hình trả lời đúng một câu hỏi. Các thẻ bên phải là danh sách; hình bên trái là cả tám hình trên dữ liệu thuê xe.

Ba hình đáng nhớ nhất. Seasonal plot tuần: mỗi tuần một đường xám chồng lên nhau, thấy ngay thứ Hai tới thứ Sáu hai đỉnh, cuối tuần một đỉnh. Lag plot: trễ 168 giờ bám đường chéo nhất, r bằng 0,876, còn trễ 12 tản thành hai nhánh. Scatter với nhiệt độ tô màu theo năm: cùng nhiệt độ mà 2012 cao hơn 2011, tức quan hệ dời theo năm.

Thêm hai thói quen khi vẽ: đường làm trơn vẽ đè lên dữ liệu gốc chứ đừng thay nó, để không mất ngày bất thường; và trên thang log, cùng độ dốc nghĩa là cùng phần trăm thay đổi.

## code-b04-gio-trong-tuan
Seasonal plot tuần dựng thế nào? Dòng 4 tính giờ trong tuần: thứ nhân 24 cộng giờ, ra số từ 0 đến 167. Dòng 5 gắn nhãn tuần bằng to_period W-SUN, tức tuần kết thúc vào Chủ nhật. Dòng 6 pivot_table xoay bảng: mỗi dòng một giờ trong tuần, mỗi tuần một cột; vẽ mỗi cột một đường là ra các đường xám chồng nhau. Dòng 7 lấy trung vị các tuần làm khuôn tuần điển hình.

Dòng 9 đến 11 so tổng ngày theo thứ, và chỉ giữ ngày đủ 24 giờ để ngày thiếu số liệu không làm thứ đó thấp giả.

Kết quả: 106 tuần chồng nhau, thứ Hai tới thứ Sáu hai đỉnh, cuối tuần một bướu. Nhưng tổng ngày lại gần nhau: thứ Bảy 4.653 lượt, thứ Sáu 4.933. Khác nhau là hình dạng trong ngày, không phải tổng.

## boxplot
Heatmap cho trung bình; boxplot cho thêm độ tản. Nhìn hình: trục ngang là giờ, trục dọc là lượt mỗi giờ, xanh là ngày làm việc, cam là ngày nghỉ. Mỗi hộp chứa một nửa số ngày ở giữa, từ quantile 0,25 tới 0,75; độ rộng đó gọi là IQR, vạch giữa là trung vị. Hộp dài nghĩa là hôm đông hôm vắng, khó đoán.

(chỉ vào 17h) 17h ngày làm việc: trung vị 539, hộp từ 348 tới 704, rộng nhất cả hình, nên đây là giờ khó dự báo nhất.

Rồi nhìn 8h: hộp ngày nghỉ chỉ 57 tới 141, nằm hẳn dưới hộp ngày làm việc 365 tới 646. Hai hộp không chồng lên nhau, nên khi dự báo giờ đó, biết hôm nay là ngày làm việc hay ngày nghỉ là thông tin bắt buộc.

## code-b04-heatmap-boxplot
Hai hình vừa rồi ra từ vài dòng tính. Dòng 4 và 5: năm thứ Hai lúc 8h, trong đó một ngày lễ chỉ 60 lượt. Trung bình ra 356, bị ngày lễ kéo xuống. Dòng 6: quantile 0,25, 0,5 và 0,75 cho trung vị 420 và hộp 410 tới 440, không bị kéo. Đó là lý do boxplot dùng quantile chứ không dùng trung bình.

Dòng 9 và 10: pivot_table với aggfunc mean ra bảng 7 thứ nhân 24 giờ, đúng những số được tô lên heatmap; ví dụ 8h thứ Hai 412, Chủ nhật 84. Dòng 11 đến 14 lọc từng giờ, tách ngày làm việc và ngày nghỉ, rồi lấy ba quantile làm mép dưới, vạch giữa, mép trên của hộp.

Kết quả khớp slide trước: 8h ngày nghỉ 57 tới 141, ngày làm việc 365 tới 646.

## acf
Lag plot cho ta nhìn bằng mắt; ACF đo cùng ý đó bằng số, cho mọi trễ một lúc. ACF ở trễ k là mức giống nhau giữa giá trị bây giờ và giá trị cách k bước, từ âm 1 tới 1.

Nhìn hình: trục ngang là độ trễ k tính bằng giờ, tới 336; trục dọc là hệ số r_k. Cứ mỗi 24 giờ có một đỉnh, đó là nhịp ngày. Nhưng chỉ vào hai vạch đứt ở 168 và 336: đỉnh ở đó cao hơn các đỉnh quanh nó, vì cùng giờ cùng thứ tuần trước giống bây giờ nhất. Vậy là nhịp ngày lồng trong nhịp tuần.

Còn ở trễ 12, tức nửa vòng ngày, đỉnh ghép với đáy nên r chỉ là âm 0,143. Cho nên đọc ACF theo vòng lặp, đừng đọc theo dấu của từng cột.

## acf-ba-hinh
Trước khi đi tiếp, chúng ta cần nhận ra ngay ba hình dạng của ACF, vì cả buổi 7 dựa vào đó.

(chỉ vào hình) Hàng trên là ba chuỗi mô phỏng, hàng dưới là ACF của từng chuỗi; dải xám là cộng trừ 1,96 chia căn T, vùng coi như bằng 0.

Cột trái là nhiễu trắng: quá khứ không có ký ức gì về tương lai, nên mọi cột nằm quanh 0, trong dải xám. Thỉnh thoảng một cột chạm ra ngoài là bình thường; slide Ljung-Box sẽ nói vì sao. Cột giữa là random walk: r1 gần 1 và các cột giảm rất chậm, dấu hiệu chuỗi chưa dừng. Chuỗi có xu hướng cũng cho hình như vậy, nên nhìn ACF chưa tách được hai loại này. Cột phải là chuỗi có mùa vụ 24 giờ: ACF có đỉnh đều ở 24, 48, xuống âm ở 12, 36, là lúc đỉnh ghép với đáy.

(dừng) Quanh 0 là nhiễu trắng, giảm rất chậm là chưa dừng, có đỉnh đều là mùa vụ.

## code-b04-acf
Tự viết ACF để thấy nó không có gì bí ẩn. Dòng 6 và 7 lấy độ lệch của từng điểm khỏi trung bình; mẫu số là tổng bình phương độ lệch trên cả chuỗi. Dòng 8 và 9: với mỗi trễ k, cộng tích độ lệch bây giờ với độ lệch k bước trước, rồi chia cho mẫu số đó. nansum để ô trống không biến cả phép cộng thành NaN.

Dòng 11 kiểm trên chuỗi 2, 4, 6, 4 lặp lại, chu kỳ 4: r2 bằng âm 0,75 ở nửa chu kỳ, r4 bằng 0,5 ở đủ chu kỳ. Dòng 12 chạy 336 giờ trên dữ liệu thật: r ở trễ 168 là 0,864, cao hơn trễ 144 là 0,786, xác nhận nhịp tuần. Dòng 13 đến 15 dùng shift ghép giờ t với giờ t trừ k, đúng là một lag plot; trễ 168 cho r bằng 0,876.

## code-b07-acf
Buổi 7 quay lại ACF với mục đích khác: nhận ra hình dạng. Hàm ở dòng 6 đến 9 giống hệt buổi 4. Dòng 11 đến 13 chạy trên sáu số 2, 3, 5, 6, 5, 3 và so với hàm acf của statsmodels. Chú ý adjusted bằng False, để thư viện cũng chia cho tổng của cả chuỗi như ta; khác tuỳ chọn là khác số. Kết quả r1 bằng 0,333, r2 bằng âm 0,417, đúng như tính tay và khớp thư viện.

Dòng 14 đến 16 tạo 500 điểm nhiễu trắng, cộng dồn bằng cumsum thành random walk, rồi tính ACF 30 trễ. Ba hình dạng cần nhớ: nhiễu trắng quanh 0; random walk giảm rất chậm; lượt thuê có đỉnh ở trễ 24, 48. ACF giảm rất chậm là dấu hiệu đầu tiên của chuỗi chưa dừng.

## box-cox
Sang buổi 5: khi dao động cứ lớn dần theo mức, mô hình khó học. Box-Cox là một núm vặn λ: λ bằng 1 gần như giữ nguyên, λ bằng 0 là log, ở giữa là nén vừa phải.

Nhìn nửa trái hình: trục ngang là λ, trục dọc là tiêu chí Guerrero, đo dao động các năm lệch nhau tới đâu; đáy nằm ở λ khoảng 0,34. Nửa phải: độ lệch chuẩn mỗi năm chia cho năm 1992, bán lẻ Mỹ. Không biến đổi, đường xám, tới 2019 gấp 2,45 lần. Với λ 0,34, đường cam, chỉ còn 1,21, gần đều nhất. Log, đường xanh, xuống 0,84, tức ép quá tay.

Hai lưu ý: Box-Cox và log cần số dương, gặp 0 hay số âm thì dùng Yeo-Johnson; và λ là tham số của mô hình, nên tính lại ở mỗi gốc dự báo.

## code-b05-guerrero
Guerrero tự viết chỉ khoảng mười dòng. Dòng 5 dựng lưới 3.001 giá trị λ từ âm 1 tới 2. Dòng 7 cắt chuỗi thành từng năm, mỗi dòng 12 tháng; dòng 8 lấy mức và độ lệch chuẩn từng năm. Dòng 9 và 10 là ý chính: với mỗi λ, tính cho từng năm tỷ số độ lệch chuẩn chia mức mũ một trừ λ, rồi đo các tỷ số đó đều tới đâu bằng hệ số biến thiên CV. Dòng 11 giữ λ cho CV nhỏ nhất: ra 0,34.

Dòng 14: scipy boxcox chọn λ theo tiêu chí khác, làm dữ liệu giống hình chuông nhất, ra 0,595. Hai con số khác nhau vì hỏi hai câu khác nhau, nên phải biết mình cần gì. Dòng 15 và 16: phần trăm tăng so với cùng tháng năm trước có số âm, nên dùng Yeo-Johnson, ra khoảng 1,02, tức gần như giữ nguyên.

## phan-ra
Buổi 6: tách chuỗi ra từng phần. Phân rã viết chuỗi thành xu hướng, mùa vụ và phần dư. Kiểu cộng: mùa hè luôn cao hơn nền 10 GW, dù nền là 80 hay 150 GW. Kiểu nhân: cao hơn một tỷ lệ, nền 100 thì thêm 10, nền 200 thì thêm 20.

Nhìn hình, tháng 7/2024 của vùng PJM, năm hàng từ trên xuống: dữ liệu, xu hướng, mùa vụ ngày, mùa vụ tuần, phần dư, đều tính bằng GW. Tải điện có hai nhịp lồng nhau, 24 giờ và 168 giờ, nên dùng MSTL với hai chu kỳ đó. Xu hướng trơn; nhịp cuối tuần nằm gọn trong hàng mùa vụ tuần, ở những chỗ lõm xuống; còn phần dư chủ yếu là thời tiết. Phần dư là thứ còn lại để mô hình và biến ngoài giải thích.

## phan-ra-cach
Có ba cách phân rã, khác nhau ở chỗ mùa vụ cố định hay được đổi dần. Phân rã cổ điển: xu hướng là trung bình trượt dài đúng một vòng, mùa vụ là trung bình theo từng vị trí trong vòng, nên ra một khuôn cố định cho cả năm. STL làm trơn cục bộ bằng LOESS nên mùa vụ đổi dần; MSTL làm việc đó cho nhiều chu kỳ.

Nhìn hình: trục ngang là giờ New York, trục dọc là mùa vụ ngày tính bằng GW, mỗi đường một tháng. Tháng 1, xanh đậm, hai đỉnh sáng và tối; tháng 7, đỏ đậm, một đỉnh chiều, biên độ lớn hẳn vì điều hoà. Một khuôn cố định không chứa được cả hai.

Nhớ gọn: cổ điển là một khuôn mùa vụ cho cả năm, STL là khuôn đổi dần, MSTL là nhiều khuôn, như 24 giờ và 168 giờ.

Lưu ý: biên độ đổi theo mùa không phải lý do dùng phân rã nhân; nhân dành cho dao động tỷ lệ với mức. Và phần dư nhỏ bất thường thì nghi cửa sổ xu hướng quá ngắn.

## code-b06-co-dien
Tự viết phân rã cổ điển để thấy nó chỉ là các phép trung bình. Dòng 6 tạo trọng số 2×m-MA: m cộng 1 trọng số, hai đầu mỗi đầu một nửa, tổng bằng 1. Dòng 7 và 8: np.convolve trượt bộ trọng số dọc chuỗi, mode valid chỉ giữ chỗ đủ hàng xóm, nên hai đầu xu hướng để NaN. Dòng 9 và 10: lấy dữ liệu trừ xu hướng, rồi trung bình theo từng vị trí trong vòng. Dòng 11 dời cho tổng mùa vụ một vòng bằng 0, để mức chung nằm hết ở xu hướng.

Chạy trên 12 quý: quý 3 có xu hướng 22; mùa vụ bốn quý là 4, âm 3, âm 7, 6; phần dư chỉ cộng trừ 0,5 và cộng trừ 1,5. Và khớp seasonal_decompose của statsmodels tới từng số.

## code-b06-bien-do
Trước khi chọn cách phân rã, ta đo xem mùa vụ ngày có đổi theo mùa không. Dòng 5 và 6: gom theo ngày, lấy giờ cao nhất trừ giờ thấp nhất, chia 1000 để ra GW. Dòng 7 và 8 lấy trung bình biên độ đó theo tháng. Kết quả: tháng 7 trung bình 44 GW, tháng 1 chỉ 17 GW. Mùa vụ đổi theo mùa như vậy thì khuôn cố định của phân rã cổ điển không hợp.

Dòng 10 và 11 là một phát hiện phụ: soi giờ 17:00 UTC ngày 21/11 cùng hai giờ hai bên. Giờ đó báo 56.260 MW, kẹp giữa hai giờ khoảng 95.000 MW. Tải cả vùng không tụt mạnh như thế trong một giờ rồi hồi lại; đây là số liệu hỏng, phải sửa trước khi phân rã.

## code-b06-stl-mstl
Giờ chạy STL và MSTL thật, và gặp hai lỗi hay gặp. Dòng 4 và 5, lỗi thứ nhất: đưa vào chuỗi còn giờ trống, MSTL không báo lỗi mà trả kết quả toàn NaN. Vì vậy phải lấp giờ trống trước.

Dòng 7, lỗi thứ hai: STL với period 24 có cửa sổ xu hướng mặc định chỉ 47 giờ, quá ngắn, nên đường xu hướng ôm luôn cả biến động do thời tiết. Dòng 8 và 9 so phương sai phần dư: STL mặc định 2,8 GW bình phương, MSTL 16,5. Phần dư nhỏ hơn không có nghĩa là tốt hơn; ở đây nó nhỏ giả tạo.

Dòng 11 đến 13 lấy cột seasonal_24, gom theo tháng và giờ, unstack thành bảng tháng nhân giờ, rồi đo biên độ: tháng 7 là 43,3 GW, tháng 1 là 14,4 GW. Dòng 14 tìm giờ đỉnh mùa đông và mùa hè, chính là hình hai đỉnh và một đỉnh vừa xem.

## f-s
Có phân rã rồi, ta muốn một con số nói mùa vụ mạnh tới đâu. F_S bằng 1 trừ phương sai phần dư chia phương sai của mùa vụ cộng phần dư. Nói bằng lời: phần dư chiếm bao nhiêu trong tổng mùa vụ cộng phần dư, lấy 1 trừ đi.

Nhìn hình: cùng một mùa vụ. Bên trái phần dư có độ lệch chuẩn 0,15, nhịp lặp rõ, F_S bằng 0,96. Bên phải phần dư độ lệch chuẩn 1,0, nhịp chìm trong nhiễu, F_S chỉ 0,34. F_T tính y hệt cho xu hướng.

Điều cần nhớ: F phụ thuộc cách phân rã. PJM 2024, mùa vụ 24 giờ: 0,618 với phân rã cổ điển, 0,829 với MSTL. Nên khi báo con số này, luôn ghi kèm tên phương pháp.

## code-b06-do-manh
Hàm do_manh tính cả F_T lẫn F_S từ một bảng phân rã. Dòng 6: F_T là 1 trừ phương sai phần dư chia phương sai của xu hướng cộng phần dư. Dòng 7 và 8 làm y hệt cho từng cột có tên bắt đầu bằng seasonal, dùng chung một phần dư. max với 0 để kẹp số âm về 0.

Dòng 12 đến 14 gom kết quả MSTL vào một bảng, join thêm hai cột seasonal_24 và seasonal_168. Dòng 15 tính độ mạnh, rồi so với cùng hàm chạy trên phân rã cổ điển.

Kết quả: F_S của mùa vụ ngày là 0,618 với cổ điển, 0,829 với MSTL; mùa vụ tuần của MSTL 0,415. Cùng chuỗi, khác phân rã, khác số. Và trên chuỗi này nhịp ngày mạnh hơn nhịp tuần khá rõ.

## ar
Sang buổi 7. Trước khi nói PACF hay tính dừng, cần một mô hình nhỏ nhất cho tự tương quan: AR(1). Giá trị mới bằng ρ nhân giá trị cũ, cộng một phần ngẫu nhiên.

Nhìn hình: đường xám có tự tương quan gần 0, lộn xộn; đường xanh có tự tương quan khoảng 0,9, lên thì ở trên một lúc. ρ bằng 0 là nhiễu trắng, không nhớ gì. ρ bằng 0,7 thì nhớ, nhưng mỗi bước kéo về trung bình: trung bình 0, đang ở 10, kỳ vọng bước sau là 7, rồi 4,9, dần về 0. Chuỗi đó dừng. ρ bằng 1 là random walk: kỳ vọng mãi là 10, không có mức để quay về.

AR(p) dùng p bước trước. Mấy slide tới đều dựa vào mô hình này: PACF chỉ ra p, ADF kiểm ρ có bằng 1 không, prewhitening dùng AR để lọc.

## pacf
ACF ở trễ 2 lớn có thể chỉ vì hôm nay giống hôm qua và hôm qua giống hôm kia. Giống tin đồn truyền qua ba người A, B, C: C giống A chỉ vì cả hai nối qua B; biết B rồi thì A không cho C thêm gì. PACF đo đúng phần “thêm” đó: phần tương quan còn lại sau khi bỏ những gì các trễ ngắn hơn đã giải thích.

Ở trễ 2 có công thức gọn trên slide: lấy r2 trừ phần đi qua trễ 1 là r1 bình phương, rồi chia cho 1 trừ r1 bình phương. AR(1) với phi 0,7: r1 là 0,7, r2 là 0,49, tử số bằng 0, nên PACF trễ 2 bằng 0. Một chuỗi có r1 0,5 và r2 0,4 thì ra 0,2: trễ 2 có thông tin riêng.

Nhìn hình: bốn hàng là bốn chuỗi dựng từ cùng một dãy nhiễu; cột giữa là ACF, cột phải là PACF, dải xám là vùng coi như 0. Hàng AR(1) φ bằng 0,7: ACF giảm dần qua vài trễ, còn PACF trễ 1 là 0,713 rồi trễ 2 chỉ còn âm 0,110. PACF cắt sau trễ 1 nghĩa là chỉ cần hôm qua, tức AR(1).

Giờ so hai hàng dưới: random walk và chuỗi có xu hướng đều có ACF giảm rất chậm, trông gần như nhau. Chỉ nhìn ACF không phân biệt được, nên lát nữa cần kiểm định ADF và KPSS.

## code-b07-pacf
Code dựng bốn chuỗi của hình vừa rồi. Dòng 4 đến 8 dựng AR(1): mỗi bước bằng 0,7 lần bước trước cộng nhiễu mới; np.empty tạo mảng trống để điền dần. Dòng 9 và 10: bốn chuỗi dùng chung một dãy nhiễu seed 42, nên mọi khác biệt là do cấu trúc, không do may rủi. Dòng 11 là dải cộng trừ 1,96 chia căn T, để biết cột nào đáng chú ý.

Dòng 14 đến 16 tính ACF, PACF 30 trễ và giữ vài con số. Để ý dòng 15 khai method bằng ywm rõ ràng, vì mặc định của hai hàm khác nhau; không khai thì con số lệch với cách tính tay.

Kết quả: AR(1) có ACF giảm nhanh, PACF cắt sau trễ 1. Random walk và xu hướng đều có r1 gần 0,98, không phân biệt được bằng ACF.

## ljung-box
Nhiễu trắng là chuỗi mà mọi tự tương quan thật đều bằng 0. Cách đọc ACF hay gặp là đếm cột vượt dải. Slide này cho thấy vì sao không nên: mỗi cột giống một lần tung đồng xu có 5% khả năng vượt dải dù chuỗi là nhiễu thuần, nên nhìn 20 trễ thì trung bình có 1 cột vượt.

Hình trái: nhiễu trắng 500 điểm, trục ngang là độ trễ tới 20, dải xám là cộng trừ 1,96 chia căn T; vẫn có cột chạm ra ngoài. Hình phải mô phỏng 1.000 chuỗi nhiễu trắng thuần: trục ngang là số cột vượt dải trong 20 trễ, trục dọc là số chuỗi. Trung bình mỗi chuỗi có 0,95 cột vượt, và 62% số chuỗi có ít nhất một cột vượt, dù chẳng có quy luật nào.

Ljung-Box gộp nhiều trễ vào một kiểm định. Câu hỏi của nó: các ACF từ trễ 1 tới trễ ℓ có cùng bằng 0 không? H0 là chuỗi là nhiễu trắng. p nhỏ hơn 0,05 là còn quy luật chưa khai thác. Ta dùng nó để kiểm phần dư của mô hình đã sạch chưa, và khi đó nhớ truyền model_df, tức số tham số của mô hình.

## code-b07-ljung-box
Ljung-Box thay việc đếm cột bằng một con số Q sao và một p-value. Dòng 5 và 6 tính tay với 100 điểm, r1 bằng 0,2, r2 bằng 0,1: Q sao bằng T nhân T cộng 2, nhân với tổng của r_k bình phương chia T trừ k. Dòng 7 và 8 tra ngưỡng 5% của phân phối khi bình phương với 2 bậc tự do, và p-value bằng chi2.sf. Q sao bằng 5,16, nhỏ hơn ngưỡng 5,99, nên không bác bỏ: chưa thấy quy luật.

Dòng 10 đến 12 dùng acorr_ljungbox kiểm 10 trễ trên ba chuỗi nhiễu trắng: p từ 0,081 tới 0,885, đều không bác bỏ, đúng như mong đợi. Dòng 14 thêm model_df bằng 2, như khi kiểm sai số của một mô hình hai tham số: bậc tự do giảm, p nhỏ đi. Quên model_df thì dễ tin nhầm phần dư đã sạch.

## dung
Giờ là khái niệm trung tâm của buổi 7: chuỗi dừng. Định nghĩa đủ gồm ba điều: mức trung bình không đổi, độ dao động không đổi, và tương quan giữa hai điểm chỉ phụ thuộc chúng cách nhau bao xa, không phụ thuộc đang ở thời điểm nào.

Nhìn hình, ba hàng. Hàng trên là dừng: như nhiệt độ phòng máy lạnh đặt 25 độ, lúc 24,5, lúc 25,8, nhưng luôn bị kéo về 25. Hàng giữa là dừng quanh xu hướng: như chiều cao một đứa trẻ, bám theo một đường; bỏ đường đó đi thì phần còn lại dừng. Hàng dưới là random walk: như tung đồng xu rồi bước tới hoặc lùi, không có chỗ nào để quay về.

Hai loại không dừng cần hai cách chữa: random walk thì sai phân, dừng quanh xu hướng thì khử xu hướng. Nhìn hình rất khó phân biệt, nên phải kiểm bằng ADF và KPSS. Thêm hai ý: chuỗi có chu kỳ lên xuống không đều vẫn có thể dừng; và với random walk, dự báo tốt nhất là naive, lấy giá trị cuối.

Thử với số dư tài khoản: nhận lương rồi tiêu tuỳ ý, không có mức nào phải quay về, đó là random walk. Nhưng nếu đầu tháng nào cũng đưa số dư về đúng 10 triệu, chuyển phần dư sang tiết kiệm, thì số dư cuối tháng dao động quanh 10 triệu: dừng.

## code-b07-random-walk
Code này cho thấy random walk khác chuỗi dừng ở đâu, và vì sao mỗi loại cần thuốc riêng. Dòng 4 đến 6 mô phỏng 10.000 người tung đồng xu, mỗi người 100 bước, cumsum ra vị trí. Dòng 7 đo độ lệch chuẩn vị trí sau 4, 25 và 100 bước. Kết quả: số bước gấp 25 lần thì độ lệch chuẩn gấp 5 lần, từ 2,0 lên 10,1. Dao động lớn dần theo thời gian, nên random walk không dừng.

Dòng 11 là thuốc một: polyfit tìm đường thẳng khớp nhất, polyval tính nó, rồi trừ đi. Dòng 12 là thuốc hai: np.diff, tức sai phân. Dòng 13 đo r1 phần còn lại.

Chọn nhầm cách xử lý thì thấy ngay: khử xu hướng cho random walk thì r1 vẫn rất lớn; sai phân chuỗi xu hướng thì r1 âm rõ, dấu hiệu sai phân thừa.

## adf-kpss-la-gi
Chuỗi có thành phần random walk không? Hai kiểm định hỏi câu này theo hai chiều ngược nhau.

ADF hỏi: khi chuỗi đang cao hơn mức thường, bước sau có bị kéo xuống không? Nhìn hình: trục ngang là độ cao hiện tại trừ mức trung bình, trục dọc là bước kế tiếp. Bên trái, chuỗi dừng ρ bằng 0,7, đám chấm dốc xuống: cao thì bị kéo về. Bên phải, random walk, đường gần nằm ngang: độ cao không nói gì về bước sau. H0 của ADF là không dừng, nên p nhỏ hơn 0,05 là có bằng chứng dừng. KPSS ngược lại: H0 là dừng, p nhỏ hơn 0,05 là có bằng chứng không dừng.

Ví dụ tay ở dưới: 5, 8, 4, 6, 5 cứ cao hơn 5 là đi xuống; 5, 6, 7, 6, 7 thì không đoán được.

## adf-kpss
Vì hai kiểm định có H0 ngược nhau, ta chạy cả hai rồi đọc bảng 2 nhân 2 này. ADF bác bỏ mà KPSS không, ô xanh: dừng, không cần sai phân. ADF không bác bỏ mà KPSS bác bỏ, ô cam: không dừng, sai phân rồi kiểm lại. Cả hai cùng bác bỏ là mâu thuẫn, thường do cú sốc hay đổi mức.

Ví dụ thật bên phải: tăng trưởng GDP Mỹ theo quý 1947 đến 2026, ADF p bằng 0,000, KPSS p bằng 0,048, rơi vào ô mâu thuẫn. Chỉ lấy 1985 đến 2019, bỏ cú sốc đại dịch, thì cả hai đồng ý dừng.

Hai điều nữa: khai cùng một dạng cho cả hai, c là quanh một mức, ct là quanh một đường xu hướng; và p của KPSS bị cắt ở 0,01 và 0,1, nên "p bằng 0,10" nghĩa là từ 0,1 trở lên, không phải "rất dừng".

## adf-kpss-bon-chuoi
Chạy ADF và KPSS trên bốn chuỗi mẫu, cả hai dạng “c” và “ct”, để thấy vì sao phải khai dạng cho đúng.

Hai dòng đầu, nhiễu trắng và AR(1), cả bốn cột đều nói dừng. Dòng ba, random walk: KPSS bác bỏ mạnh, ADF p bằng 0,073. Nếu ai đó dùng mức 10% thì sẽ gọi nhầm random walk là dừng; KPSS bắt được chỗ này.

(chỉ vào dòng cam) Dòng bốn là chuỗi xu hướng. Dạng “c” hỏi có dừng quanh một mức cố định không, nên cả hai nói không dừng và bảo sai phân. Dạng “ct” hỏi quanh một đường thẳng, thì cả hai nói dừng. Kết luận đúng là dừng quanh xu hướng: chỉ cần khử xu hướng, sai phân là thừa.

Hai lời nhắc: ADF hay bỏ sót chuỗi dừng mà rất gần random walk, nên không bác bỏ chưa phải là chứng minh. Và p của KPSS trong statsmodels bị cắt ở 0,01 và 0,1: thấy 0,10 thì đọc là lớn hơn hoặc bằng 0,1, không phải “rất dừng”.

## code-b07-adf-kpss
Gói bảng 2 nhân 2 thành hai hàm. Dòng 4: tham số dang là c hoặc ct, dùng chung cho cả hai kiểm định. Dòng 6 và 7: adfuller với autolag AIC tự chọn số trễ; p nhỏ là có bằng chứng dừng. Dòng 8 và 9: kpss với nlags auto; p nhỏ là có bằng chứng không dừng. Dòng 11 đến 14: o_bang đổi cặp câu hỏi "ADF có bác bỏ, KPSS có bác bỏ" thành một trong bốn kết luận.

Dòng 15 và 16 thử chuỗi xu hướng 0,05t với cả hai dạng. Kết quả: dạng c nói không dừng; chỉ dạng ct mới cho thấy đây là chuỗi dừng quanh xu hướng, nên cần khử xu hướng chứ không sai phân. Khai sai dạng là kết luận sai.

Còn với random walk, ADF cho p bằng 0,073, không bác bỏ, và KPSS bắt được: đúng ô không dừng.

## sai-phan-la-gi
Thuốc cho random walk là sai phân. Sai phân thay mỗi giá trị bằng hiệu với giá trị trước: 100, 103, 105 thành 3, 2. Sai phân mùa vụ lấy hiệu với cùng vị trí vòng trước, ví dụ tháng này trừ cùng tháng năm ngoái.

Nhìn hình: góc trên trái là log GDP thực của Mỹ theo quý, trôi lên mãi, và ACF ngay dưới giảm rất chậm. Góc trên phải là sai phân log, gần bằng phần trăm tăng mỗi quý: dao động quanh 0,76%, và ACF bên dưới chỉ còn vài trễ đầu. Chuỗi trôi đi đã thành chuỗi có mức để quay về.

Khi nào dùng: random walk thì sai phân một lần; có mùa vụ thì sai phân mùa vụ trước; dừng quanh xu hướng thì khử xu hướng, sai phân thêm là thừa. Để ý cú sốc lớn quanh năm 2020 bên phải, chính là lý do ô mâu thuẫn ở slide trước.

## sai-phan-bao-nhieu
Sai phân chữa random walk, nhưng sai phân thêm một chuỗi đã dừng lại làm hỏng nó. Vậy dừng tay ở đâu?

(chỉ vào bảng trái) Chuỗi 2, âm 1, 0, 1, âm 2, 0 đã dừng, độ lệch chuẩn 1,41. Sai phân nó ra âm 3, 1, 1, âm 3, 2: độ lệch chuẩn tăng lên 2,41, và r1 khoảng âm 0,5. Lý do là mỗi số gốc có mặt trong hai hiệu liền nhau với hai dấu ngược nhau, nên lên thì lần sau xuống. Đó là hai dấu hiệu sai phân thừa: r1 về gần âm 0,5, và độ lệch chuẩn tăng.

GDP Mỹ là ví dụ thật: log GDP chưa dừng, sai phân một lần ra tăng trưởng. Theo KPSS máy móc thì phải sai phân thêm lần nữa, nhưng lần hai cho r1 âm 0,488 và độ lệch chuẩn tăng từ 1,105 lên 1,455. Dừng ở một lần.

Bảng phải: chuỗi có mùa vụ thì sai phân mùa vụ trước. Lượt thuê theo giờ, thang log. Chỉ sai phân thường thì r24, r168 vẫn lớn, mùa vụ còn nguyên. Sai phân mùa vụ 168 bỏ được nhịp ngày và tuần. Thêm một lần sai phân thường nữa thì độ lệch chuẩn giảm tiếp và r1 chưa tới âm 0,5, nên cả hai lần đều đáng.

Quy tắc: sai phân tới khi KPSS thôi bác bỏ, nhưng dừng tay nếu thấy hai dấu hiệu thừa.

## quy-trinh-chuoi-la
Toàn bộ buổi 7 gói lại thành bảy bước, dùng mỗi khi gặp một chuỗi lạ.

Hàng trên là nhìn và kiểm. Một, nhìn ACF: quanh 0 là nhiễu trắng, giảm rất chậm là chưa dừng, có đỉnh đều là mùa vụ. Hai, nhìn PACF: cao ở vài trễ đầu rồi tắt hẳn sau trễ p thì giống AR bậc p. Ba, Ljung-Box để có một p-value cho nhiều trễ, thay vì đếm cột vượt dải. Bốn, chạy cả ADF lẫn KPSS, cùng một dạng: “c” nếu chuỗi quanh một mức, “ct” nếu quanh một đường.

Hàng dưới là kết luận và chữa. Năm, đọc bảng 2 × 2: hai kiểm định cùng hướng thì tin, mâu thuẫn thì quay lại vẽ chuỗi tìm cú sốc. Sáu, chữa đúng loại: random walk thì sai phân, quanh xu hướng thì khử xu hướng, có mùa vụ thì sai phân mùa vụ trước. Bảy, kiểm xem có chữa quá tay không: sai phân xong mà r1 về gần âm 0,5 hoặc độ lệch chuẩn tăng lên thì bớt một lần.

Nhìn trước, kiểm bằng số sau, chữa xong thì kiểm lại.

## scatter
Buổi 8: quan hệ giữa hai biến. Pearson r đo quan hệ đường thẳng; Spearman đo hai biến có cùng tăng theo thứ hạng không.

Nhìn hình, bộ tứ Anscombe: bốn bộ dữ liệu cùng r bằng 0,82 và cùng đường hồi quy. Bộ một là quan hệ thẳng có nhiễu. Bộ hai là một đường cong. Bộ ba là thẳng chặt với một điểm lạ. Bộ bốn là một cột điểm dựng đứng cộng một điểm ở xa kéo lệch cả đường. Bốn câu chuyện khác nhau, cùng một con số.

Ngược lại, hình chữ U đối xứng cho cả Pearson lẫn Spearman bằng 0 dù quan hệ rất chặt. Nên quy tắc là vẽ scatter trước khi tin r. Và nhớ: tương quan không phải nhân quả; cuối phần này ta sẽ thấy cả kiểm định Granger cũng không nói "gây ra".

## code-b02-tuong-quan
Quay lại code buổi 2 để thấy r sai lệch thế nào trên dữ liệu thật. Dòng 3 và 4: x từ âm 2 tới 2, y bằng x bình phương; y phụ thuộc hẳn vào x mà r bằng 0.

Dòng 6 đến 8: r giữa nhiệt độ và lượt thuê trên mọi giờ là 0,405; chỉ giữ giờ 17 thì lên 0,588. Giờ trong ngày là biến gây nhiễu: trộn mọi giờ lại thì nhịp giờ che bớt quan hệ với nhiệt độ. Dòng 9: giờ trong ngày quyết định lượt thuê rất mạnh, nhưng r chỉ 0,394 vì quan hệ cong, có hai đỉnh.

Dòng 10 đến 12 tính tự tương quan trễ 1 bằng tay: nhân độ lệch mỗi giờ với độ lệch giờ trước, chia tổng bình phương độ lệch. Ra 0,844: giờ này rất giống giờ trước.

## code-b08-anscombe
Giờ kiểm hai hệ số bằng scipy. Dòng 4 và 5: y bằng x bình phương trên hai khoảng. Với x từ 1 tới 5, quan hệ cùng tăng; với x từ âm 2 tới 2, hình chữ U, và Pearson ra 0 dù y phụ thuộc hoàn toàn vào x. pearsonr và spearmanr đều trả kèm p-value; ta lấy phần tử đầu là hệ số.

Dòng 7 đến 14 nhập hai trong bốn bộ Anscombe: bộ I thẳng có nhiễu, bộ IV là một cột x bằng 8 cộng một điểm x bằng 19. Dòng 15 và 16 tính hai hệ số cho từng bộ.

Kết quả: bốn bộ cùng Pearson 0,82, nhưng Spearman trải từ 0,5 tới 0,99. Khi hai hệ số lệch nhau nhiều như vậy, đó là tín hiệu phải mở scatter ra xem.

## ccf
Hai chuỗi có quan hệ rồi, câu hỏi tiếp: ai đi trước, trước bao nhiêu bước? Tương quan chéo r_k đo x lúc t giống y lúc t cộng k tới đâu.

Nhìn hình trái, CCF thô giữa CDD, tức độ nóng, và tải điện: trục ngang là độ trễ k tính bằng giờ, CDD đi trước tải k giờ. Cao ở mọi trễ và lặp theo nhịp 24 giờ: 0,848 ở trễ 0, vẫn 0,828 ở trễ 24. Đó chỉ là nhịp ngày của chính CDD, chưa phải quan hệ.

Hình phải, sau prewhitening: còn 0,205 ở trễ 0 và 0,061 ở trễ 24; đỉnh chỉ ở trễ 0 rồi tắt sau vài giờ. Kết luận: tải phản ứng với trời nóng gần như ngay trong giờ. Một lưu ý: quy ước hướng của hàm ccf khác nhau giữa các thư viện, nên thử trên chuỗi giả trước khi tin.

## prewhitening
Prewhitening làm thế nào? Bốn bước ở dưới hình.

Bước 1: dựng mô hình AR cho x, ở đây AR(48), tức phần của CDD tự đoán được từ 48 giờ trước của chính nó. Bước 2: lọc x, trừ phần tự đoán được, còn lại phần "bất ngờ". Bước 3 là chỗ hay sai: lọc y bằng đúng bộ lọc của x, không dựng mô hình riêng cho y. Bước 4: tính tương quan chéo trên hai chuỗi đã lọc; đỉnh còn lại ở trễ nào thì x đi trước y chừng ấy bước.

Nhìn lại hình: trước lọc, tương quan nhoè ra mọi trễ và lặp theo nhịp ngày; sau lọc chỉ còn đỉnh 0,205 ở trễ 0 và gần như tắt ở trễ 24, còn 0,061. Kết quả này là căn cứ để chọn độ trễ cho feature ở các buổi sau.

## code-b08-prewhiten
Code gồm hai hàm tự viết. Dòng 4 đến 6, ccf_tu_viet: chuẩn hoá hai chuỗi, rồi nhân x lúc t với y lúc t cộng k và lấy trung bình; k dương nghĩa là x đi trước. Tự viết để biết chắc chiều, vì các thư viện quy ước khác nhau.

Dòng 8: AutoReg khớp AR(48) cho x, lấy các hệ số phi, bỏ hệ số chặn. Dòng 9 đến 12: hàm loc trừ khỏi mỗi điểm phần dự đoán từ 48 điểm trước, và áp đúng bộ phi đó cho cả x lẫn y. Dòng 14 và 15 so CCF thô với CCF sau lọc trên CDD và tải.

Kết quả: thô, trễ 24 là 0,828, cao gần bằng trễ 0, là nhịp ngày của CDD. Sau lọc chỉ còn đỉnh ở trễ 0, bằng 0,205, tắt sau vài giờ.

## truot
Kể cả khi đo đúng, một hệ số cho cả năm có thể là trung bình của các chế độ ngược nhau. Tương quan trượt tính r trên từng cửa sổ thời gian rồi trượt dần cửa sổ đi.

Nhìn hình: trục ngang là ngày trong 2024, trục dọc là tương quan nhiệt độ với tải; đường xám là cửa sổ 30 ngày, đường xanh đậm là 90 ngày, vạch cam đứt là con số cả năm. Cửa sổ 90 ngày tới 31/3 là âm 0,801: mùa đông, lạnh thì sưởi. Cửa sổ tới 14/10 là 0,968: mùa hè, nóng thì điều hoà. Còn cả năm 0,616, không đúng với mùa nào.

Quan hệ đổi dấu theo mùa thì tách thành từng chế độ, hoặc dùng CDD và HDD. Lưu ý kỹ thuật: rolling 90D mặc định chỉ cần 1 điểm, nên vài giá trị đầu là cộng trừ 1 giả; đặt min_periods rõ ràng.

## code-b08-tuong-quan-truot
Dòng 5 là ví dụ tay: ba ngày đông tương quan âm 1 hoàn toàn, ba ngày hè dương 1 hoàn toàn. Gộp sáu ngày lại chỉ ra r bằng 0,48, một con số lưng chừng không đúng với ngày nào.

Dòng 7 gộp dữ liệu giờ thành trung bình ngày. Dòng 8 và 9 tính r trên cửa sổ trượt 90 và 30 ngày, với min_periods bằng đúng độ dài cửa sổ: chưa đủ điểm thì để trống, thay vì ra số giả. Dòng 10 tính con số cả năm để so.

Kết quả: cửa sổ 90 ngày cho âm 0,801 ngày 31/3 và 0,968 ngày 14/10; cửa sổ 30 ngày xuống tới âm 0,971. Cả năm chỉ 0,616. Ví dụ tay và dữ liệu thật kể cùng một chuyện: gộp hai chế độ ngược dấu thì ra một số lưng chừng.

## granger
Kiểm định Granger so sai số dự báo Y khi có và khi không có quá khứ của X. p nhỏ nghĩa là quá khứ X giúp dự báo Y, không phải X gây ra Y.

Nhìn hình phải: tương quan chéo cao ở cả hai chiều, CDD trước tải và tải trước CDD. Granger cũng có ý nghĩa ở cả hai chiều, p nhỏ hơn 0,001. Nhưng "tải điện gây ra nhiệt độ" là vô lý. Hình trái giải thích: trục ngang là giờ UTC, trục dọc là giá trị chuẩn hoá; tải và nhiệt độ theo cùng một nhịp 24 giờ. Nhịp ngày là biến gây nhiễu, điều khiển cả hai.

Ba điều kiện khi dùng Granger: chạy cả hai chiều; chuỗi phải dừng, sai phân trước; và hỏi thêm lúc ra dự báo ta có biết giá trị tương lai của X không.

## quy-trinh-tuong-quan
Buổi 8 có nhiều công cụ. Slide này xếp chúng thành tám câu hỏi theo thứ tự nên hỏi.

Một, quan hệ trông ra sao: luôn vẽ scatter trước khi tin một hệ số. Hai, thẳng hàng hay chỉ cùng tăng: Pearson hay Spearman. Ba, hai chuỗi có cùng trôi theo thời gian không: đo lại trên sai phân và xem Durbin–Watson; CPI với dân số Mỹ đi từ 0,97 xuống còn âm 0,21. Bốn, quan hệ cong hay đổi dấu: tách CDD, HDD, hoặc đo mutual information rồi kiểm bằng hoán vị theo khối.

Hàng dưới. Năm, ai đi trước và trước bao lâu: prewhiten cả hai chuỗi bằng cùng một bộ lọc rồi mới đọc tương quan chéo. Sáu, quan hệ có giữ nguyên cả năm không: tương quan trượt; đổi dấu theo mùa thì tách riêng từng mùa. Bảy, quá khứ của x có giúp đoán y không: Granger, chạy cả hai chiều, và nhớ nó chỉ nói “giúp dự báo”. Tám, lúc dự báo thật đã có x trong tay chưa: nếu chưa, chỉ được dùng bản dự báo của x, chuyện của buổi 13.

(dừng) Đừng tin hệ số tương quan ngay; đi qua đủ tám câu thì mới dùng x làm feature.

## code-b08-granger
Dòng 5 và 6 là chỗ dễ sai nhất: grangercausalitytests hỏi cột 2 có giúp dự báo cột 1 không. Nên ta xếp kết quả vào cột 1, nguyên nhân nghi ngờ vào cột 2; đảo thứ tự là trả lời câu hỏi ngược. Dòng 7 lấy p nhỏ nhất của kiểm định F qua các độ trễ 1 tới 4.

Dòng 10 và 11 hỏi cả hai chiều: CDD giúp dự báo tải không, và tải giúp dự báo CDD không. Dòng 13 và 14 đi tìm biến thứ ba: trung bình tải và nhiệt độ theo giờ trong ngày, chuẩn hoá để cùng thang, ra hai đường gần trùng nhau.

Kết quả: cả hai chiều p gần 0, kể cả "tải giúp dự báo nhiệt độ". Vô lý, vì cả hai cùng chạy theo nhịp ngày. Granger có ý nghĩa hai chiều là tín hiệu đi tìm biến gây nhiễu.

## code-b09-dac-trung
Hàm dac_trung biến một chuỗi thành một hàng số; ở đây là 6 trong 20 đặc trưng. Dòng 7: chuẩn hoá z-score trước khi chạy STL, để độ mạnh mùa vụ không tính bằng USD. Dòng 8 đến 10: gắn lịch tháng rồi tách xu hướng, mùa vụ, phần dư bằng STL. Dòng 11 đến 15: mỗi đặc trưng một con số: trung bình, hệ số biến thiên, hệ số lệch và độ nhọn để đo đuôi, độ mạnh mùa vụ tính như F_S, tỷ lệ số 0.

Dòng 16 là chi tiết trung thực: chỉ tính trên phần học, bỏ 18 tháng dùng để chấm, để đặc trưng không nhìn thấy tương lai.

Kết quả: nhân mọi chuỗi với 1.000 thì chỉ trung bình và độ lệch chuẩn đổi, 18 đặc trưng còn lại giữ nguyên. Bảng này còn cho thấy 1 chuỗi hằng và 50 chuỗi bậc thang, những chuỗi hỏng cần xem riêng.

## pho
Giờ nhìn chuỗi theo nhịp lặp thay vì theo thời gian. Tần số là số vòng lặp mỗi bước, bằng 1 chia chu kỳ.

Nhìn hình: sóng trên lặp mỗi 12 tháng, tần số 1 chia 12, khoảng 0,083 vòng mỗi tháng. Sóng dưới lặp mỗi 2 tháng, tần số 0,5, nhanh nhất mà dữ liệu tháng thể hiện được.

Phổ, hay periodogram, cho biết mỗi tần số góp bao nhiêu phần dao động, gọi là năng lượng. Tần số thấp là dao động chậm như xu hướng, mùa năm; tần số giữa là nhịp ngày, nhịp tuần; tần số cao thường là nhiễu. Ví dụ ở buổi 12: phổ điện thiết bị có đỉnh ở một vòng mỗi ngày, và 17,8% năng lượng nằm ở dao động nhanh hơn một giờ. Phổ cho ta biết nhịp nào là tín hiệu cần giữ, nhịp nào là nhiễu có thể lọc.

## code-b09-entropy
Tính spectral entropy chỉ trong bốn dòng. Dòng 5: signal.welch ước lượng phổ bằng cách chia chuỗi thành nhiều đoạn chồng nhau rồi lấy trung bình phổ của các đoạn. Dòng 6 bỏ tần số 0, vì đó chỉ là mức trung bình. Dòng 7 chia cho tổng để các phần năng lượng cộng lại bằng 1. Dòng 8 là entropy của các phần đó, chia cho ln của số tần số để luôn nằm trong 0 tới 1.

Dòng 11 đến 13 so chuỗi sin 12 tháng có nhiễu nhỏ với nhiễu thuần: 0,33 và 0,94, đúng hình vừa xem. Dòng 14 và 15 xem phân bố trên 4.000 chuỗi M4: trung vị 0,462, và một phần năm số chuỗi từ 0,666 trở lên. Nhóm entropy cao đó giống nhiễu, là nhóm khoanh lại để xét có đáng làm mô hình hay chỉ cần baseline.

## do-kho
Muốn biết entropy có báo trước độ khó không, trước hết phải đo độ khó cho đúng.

Nhìn hình: trục ngang ở cả hai ô là entropy, đường cam nối trung vị của năm nhóm. Ô trái là sMAPE: đường cam đi lên, nhóm entropy cao nhất có sai số trung vị gấp đôi các nhóm còn lại. Ô phải là MASE: mọi nhóm nằm ngang quanh vạch 1.

Vì sao? MASE chia sai số cho sai số seasonal naive của chính chuỗi đó. Chuỗi khó thì mẫu số cũng lớn, nên độ khó tự triệt tiêu. Tương quan với entropy: sMAPE cộng 0,245, MASE chia seasonal naive chỉ âm 0,048, còn chia naive một bước thì ra âm 0,381. (dừng) Cùng dữ liệu, chỉ đổi mẫu số mà kết luận đi từ dương qua 0 tới âm.

Có người giải thích việc đổi sang sMAPE là vì phần trăm dễ nói với người không chuyên. Lý do thật không phải vậy, mà là mẫu số: MASE đã chia mất độ khó.

Nên nhớ: MASE để so mô hình trên cùng một chuỗi, sMAPE để xếp độ khó giữa các chuỗi dương.

## code-b09-smape-mase
Giờ xem bằng code chỉ đổi mẫu số thì kết luận đổi ra sao.

Dòng 5 đến 7 là sMAPE: chia sai số cho mức của chuỗi, có np.where để khỏi chia cho 0. Dòng 8 đến 10 là MASE: chia cho sai số seasonal naive tính trên phần học. Dòng 13 đến 14 giữ 18 tháng cuối để chấm, và dự báo bằng cách lặp lại năm cuối; hàm np.resize làm việc lặp 12 tháng thành 18 tháng. Dòng 16 tính tương quan Pearson giữa entropy và độ khó.

Kết quả: ví dụ tay với hai chuỗi, MASE nói B dễ hơn A, 0,92 so với 1,00, còn sMAPE nói B khó hơn hẳn, 76,2% so với 6,7%. Trên cả tập, tương quan với entropy là cộng 0,245 theo sMAPE và âm 0,048 theo MASE. Hai thước đo trả lời hai câu hỏi khác nhau.

## ban-do-pca
Có độ khó rồi, giờ chúng ta muốn nhìn cả 4.000 chuỗi M4 trên một hình.

Chúng ta giữ 15 đặc trưng không phụ thuộc đơn vị, chuẩn hoá từng cột, rồi dùng PCA, phép chiếu giữ nhiều khác biệt nhất, để nén về hai trục. Mỗi chấm là một chuỗi. Trục ngang PC1 giữ 41% khác biệt, là độ lởm chởm: phải là chuỗi lởm chởm, trái là chuỗi trơn. Trục dọc PC2 thêm 15%, là mức xu hướng và mùa vụ.

Ba ô cùng vị trí chấm, chỉ khác màu: entropy, F_S và sMAPE. (chỉ vào phía phải) Vùng phải sáng ở ô entropy cũng sáng ở ô sMAPE và tối ở ô F_S: chuỗi lởm chởm, mùa vụ yếu là chuỗi khó. Quy tắc thực hành: entropy từ 0,666 trở lên và F_S dưới 0,4 thì chỉ cần baseline. Còn mấy chấm lẻ ở góc trên phải là chuỗi lạ, phải xem tận mắt.

## code-b09-pca
Code làm bản đồ và tách nhóm dùng baseline.

Dòng 5 đến 7 chọn cột: chỉ giữ đặc trưng đủ số, bỏ hai cột quy mô, và bỏ cột sai số. Bỏ cột sai số là quan trọng: để sai số lẫn vào bản đồ thì bản đồ tự "biết" chuỗi nào khó, đó là rò rỉ. Dòng 8 dùng StandardScaler để cột có số to không lấn át. Dòng 9 đến 11 nén về hai trục, explained_variance_ratio_ cho biết mỗi trục giữ bao nhiêu phần trăm. Dòng 13 đến 14 gắn nhãn "dùng baseline" theo quy tắc entropy và F_S, dòng 15 kiểm lại bằng sMAPE thật.

Kết quả: PC1 giữ 41%, PC2 15%. 137 chuỗi dùng baseline có sMAPE trung vị 18,11%, gấp ba nhóm 3.863 chuỗi còn lại, 6,05%. Quy tắc tách đúng nhóm khó.

## dtw
PCA nhóm theo đặc trưng. Còn muốn gom các chuỗi cùng hình dạng thì dùng DTW.

DTW đo hai chuỗi giống hình dạng tới đâu, cho phép lệch thời gian đôi chút, ví dụ đỉnh Tết năm sớm năm muộn. Chuỗi “tăng, giảm, tăng” và cùng hình đó nhưng chậm vài bước thì DTW coi là giống nhau. Nhưng DTW so giá trị, nên phải chuẩn hoá z-score từng chuỗi trước.

Nhìn hình: mỗi cột là một cụm. Hàng trên phân cụm sau chuẩn hoá, ra bốn hình dạng: giảm, tăng đều, bướu giữa, dao động quanh mức. Hàng dưới không chuẩn hoá: các đường trong mỗi ô na ná nhau, chỉ có thang trục dọc tăng dần từ trái sang phải. Mức trung vị bốn cụm là 1.585, 3.310, 6.835, 9.832, tức là đang xếp theo độ lớn, việc một phép sort cũng làm được.

Kiểm nhanh: mức trung vị các cụm tăng đều thì bạn đã quên chuẩn hoá.

## code-b09-dtw
Code phân cụm DTW, có công tắc chuẩn hoá để so hai trường hợp.

Dòng 7 đến 8 là hàm z: trừ trung bình, chia độ lệch chuẩn, bỏ độ lớn chỉ giữ hình dạng. Dòng 10 chọn có chuẩn hoá hay không. Dòng 11 tính khoảng cách DTW giữa mọi cặp chuỗi, cửa sổ 10 nghĩa là cho lệch tối đa 10 bước. Dòng 12 đến 13 sửa ma trận: thư viện chỉ điền một nửa, nên đổi vô cực thành 0 rồi cộng với chuyển vị cho đối xứng. Dòng 14 đến 16: linkage theo Ward gộp dần hai nhóm gần nhau nhất, fcluster cắt cây ra đúng 4 cụm.

Kết quả: không chuẩn hoá thì mức trung vị các cụm tăng đều từ 1.585 tới 9.832, chỉ là xếp theo độ lớn. Chuẩn hoá thì bốn cụm là bốn hình dạng.

## abc-xyz
Trong bán lẻ, cách phân loại mã hàng quen thuộc là ABC–XYZ. Nó trả lời hai câu hỏi khác nhau, và cả hai đều không phải "chuỗi nào khó".

ABC xếp theo doanh thu. Nhìn ô phải, dòng A: một phần năm số mã mang 74,7% doanh thu. Đó là nơi dự báo sai đắt nhất, đáng làm mô hình kỹ nhất. XYZ xếp theo CV, độ lệch chuẩn chia trung bình, tức chỉ đo dao động.

Dao động không phải độ khó. Chuỗi 10, 30, 10, 30 có CV 0,58, khá cao, nhưng mùa vụ đều đặn nên rất dễ đoán. Muốn đo độ khó thì dùng sai số thật của một baseline.

Cách nhớ: ABC hỏi cái nào quan trọng, CV hỏi cái nào dao động, sai số baseline mới hỏi cái nào khó.

## code-b09-abc-xyz
Code dựng bảng ABC–XYZ rồi kiểm CV có đo được độ khó không.

Dòng 4 đến 6 tổng hợp từng mã hàng bằng groupby và agg, chỉ giữ mã có đủ 12 tháng. Dòng 7 tính CV. Dòng 8 đến 9 xếp theo doanh thu: 20% mã đầu là A, 30% tiếp là B, còn lại C. Dòng 10 đến 11 chia X, Y, Z theo CV, rồi unstack thành bảng 3 nhân 3. Dòng 13 đến 14 đối chiếu CV với sMAPE thật trên 4.000 chuỗi M4 bằng tương quan Spearman.

Kết quả: 2.773 mã hàng, nhóm A mang 74,7% doanh thu, ô CZ đông gần gấp bốn ô AX. Trên M4, Spearman giữa CV và sMAPE là 0,765, khá cao, nhưng CV vẫn xếp sai đúng loại chuỗi mùa vụ đều. Nên dùng CV để sàng sơ bộ, không thay được sai số baseline.

## biet-truoc
Chuyển sang buổi 13: tạo feature. Feature là một cột đầu vào của mô hình, và chỉ có một quy tắc: mỗi feature phải trả lời được "biết trước bao lâu".

Có ba nhóm hợp lệ. Lịch, như thứ, giờ, ngày lễ, biết mãi mãi. Kế hoạch, như khuyến mãi đã công bố, biết từ lúc công bố. Quá khứ của chuỗi thì chỉ biết tới thời điểm ra dự báo, nên phải cách mốc cần dự báo ít nhất h bước.

Nhìn hình: hai thanh là hai nhóm. 41 feature của buổi 13 có 23 cột lịch và 18 cột lấy từ quá khứ, không cột nào nằm ngoài. Feature nào không xếp được vào ba nhóm là nghi rò rỉ.

Bảng "biết trước bao lâu" nộp kèm mô hình, để người xem lại bắt được rò rỉ mà không cần đọc code.

## code-b13-biet-truoc
Code đặt câu hỏi "lúc ra dự báo tôi đã có nó chưa" cho từng feature.

Dòng 3 đến 4: tối thứ Hai chúng ta dự báo doanh thu thứ Ba, tức h bằng 1. Dòng 5: thứ của ngày mai là lịch, biết từ trước. Dòng 6 đến 7 so hai cách lấy trung bình: y cắt tới t chỉ gồm các ngày đã biết, còn y.mean() gồm cả những ngày chưa xảy ra. Dòng 9 đến 16 là hàm bang_biet_truoc, xếp feature vào nhóm theo tên cột; đuôi _that là giá trị thật, bị loại.

Kết quả: trung bình 189 ngày đã biết là 27.701, còn trung bình cả chuỗi là 33.454, vì gồm 550 ngày chưa xảy ra. Đó là rò rỉ bằng một dòng code. Và lưu ý: cột z_score lọt vào nhóm "vô hạn" chỉ vì tên không theo quy ước. Tên sai thì bảng sai, nên đặt tên cột cẩn thận.

## shift-rolling
Lag nhìn về một điểm quá khứ, ví dụ lag_7 của thứ Hai là giá trị thứ Hai tuần trước. Rolling lấy trung bình một vùng gần đây. Khi dự báo trước h bước thì phải shift h trước, rolling sau.

Nhìn bảng: h bằng 3, chuỗi 10, 20 tới 60. Dòng xanh là đúng thứ tự: shift 3 rồi rolling 2 cho ngày 6 giá trị 25, là trung bình ngày 2 và 3, đã biết từ ngày 3. Dòng đỏ là quên shift: rolling 2 cho ngày 6 giá trị 55, trung bình ngày 5 và 6. (dừng) Lúc ra dự báo, tức ngày 3, chúng ta chưa có hai ngày đó. Đó là rò rỉ.

Lỗi này không báo lỗi gì cả, chỉ làm backtest đẹp giả tạo.

## code-b13-shift
Code cho thấy bằng số vì sao phải shift trước, rồi gói thành hàm tạo feature.

Dòng 2 là sáu ngày doanh thu, dự báo trước 1 ngày. Dòng 3 đến 5 là ba cách tính trung bình 3 ngày: có tâm thì nhìn cả ngày sau, không shift thì chứa chính ngày t, chỉ dòng 5 là đúng. Hàm feature_tre ở dưới: dòng 9 lùi chuỗi tam bước trước khi làm gì khác; dòng 10 đến 11, lag nhỏ hơn tầm dự báo bị nâng lên bằng tam; dòng 12 đến 14, mọi rolling tính trên chuỗi đã lùi.

Kết quả ngày 4: có tâm ra 14, không shift ra 11,33, shift đúng ra 10. Phép thử: cắt bớt dữ liệu tương lai rồi tính lại feature. Bản shift lệch 0, bản có tâm lệch tới 5.113. Feature đổi khi cắt tương lai tức là feature đang nhìn tương lai.

## feature-lich
Feature lịch biết trước mãi mãi, nhưng phải đưa vào theo cách mô hình hiểu được.

Ghi thứ là số 1 tới 7 thì Chủ nhật cách thứ Hai rất xa, dù thực tế chúng liền nhau. Một cặp sin, cos đặt các thứ lên vòng tròn, Chủ nhật đứng cạnh thứ Hai. Mùa vụ dài 365 ngày thì dùng vài cặp Fourier thay vì 365 biến giả.

Tết âm lịch khó hơn. Nhìn ô trái: chấm xanh là Tết âm lịch, xê dịch gần một tháng giữa các năm dương. Nên không ghi cứng ngày mà tính số ngày tới Tết, theo múi giờ Việt Nam; thư viện lịch Trung Quốc dùng UTC+8 có năm lệch một ngày. Ô phải xếp theo số ngày tới Tết: lượt xem Wikipedia còn 0,62 lần mức thường vào mùng 1.

## code-b13-lich
Code mã hoá lịch.

Dòng 3 đến 5 đặt thứ Bảy, Chủ nhật, thứ Hai lên vòng tròn bằng sin và cos của 2 pi nhân số thứ chia 7. Dòng 6 dùng np.linalg.norm đo khoảng cách Chủ nhật tới thứ Hai. Hàm feature_fourier: dòng 9 đổi ngày thành số ngày kể từ đầu chuỗi; dòng 11 đến 13, mỗi i thêm một cặp sóng lặp i lần mỗi năm, K bằng 3 cho 6 cột. Dòng 16 đếm số ngày tới mùng 1 Tết gần nhất theo lịch âm.

Kết quả: Chủ nhật cách thứ Hai 0,868, đúng bằng khoảng cách thứ Bảy tới Chủ nhật. Thêm 5 feature Tết: cả năm chỉ tốt hơn 1,9%, nhưng quanh Tết tốt hơn 16,9%. Bài học: báo cải thiện ở đúng vùng feature có tác dụng, báo trung bình cả năm sẽ loại oan nó.

## phan-b
Hết phần A về khái niệm. Phần B là các vấn đề dữ liệu, đi theo thứ tự buổi 3 tới 13.

Mỗi slide vấn đề có ba thẻ: dấu hiệu, tức thấy gì thì nên nghi; kiểm bằng, tức con số hay lệnh nào xác nhận nghi ngờ; và cách sửa. Khi gặp dữ liệu mới, các bạn có thể dùng đúng ba câu hỏi này làm danh sách kiểm.

## ma-tran
Trước khi đi từng vấn đề, nhìn bức tranh chung.

Cách đọc: mỗi dòng là một loại vấn đề, mỗi cột là một buổi, chấm cam là buổi dạy cách nhận ra và sửa nó. Đọc theo dòng để biết một vấn đề quay lại ở đâu.

Dòng tô nền là rò rỉ tương lai, dùng thông tin chưa có lúc dự báo: gặp ở 8 buổi, nhiều nhất bảng. Mỗi lần một dạng khác: sai số ảo ở buổi 1, lambda Box-Cox tính trên cả chuỗi ở buổi 5, điền thiếu trước khi chia tập ở buổi 10, feature không shift ở buổi 13, chia dữ liệu ngẫu nhiên ở buổi 15. Dòng thứ hai đáng nhớ là thiếu dữ liệu, gặp ở 5 buổi.

Nghĩa là: đừng coi rò rỉ là một bước kiểm một lần, nó có mặt ở gần như mọi khâu.

## mui-gio
Vấn đề đầu tiên, buổi 3: múi giờ. Khi làm dữ liệu, lưu tâm múi giờ trước tiên.

Dấu hiệu: nhìn hình trái, đếm chuyến taxi New York theo giờ địa phương naive. Rạng sáng Chủ nhật 10/3, giờ 02:00 có 0 chuyến, vì giờ đó không tồn tại khi vặn đồng hồ. Ngày 3/11, giờ 01:00 có 9.869 chuyến, gần gấp đôi cùng giờ tuần sau, vì hai giờ thật bị gộp làm một. Hình phải: ghép taxi giờ địa phương với thời tiết giờ UTC thì New York "nóng nhất lúc 20h", đường cam trượt phải khoảng 4 giờ.

Kiểm bằng: in 00:00 tới 05:00 của ngày đổi giờ, và xem giờ nóng nhất có rơi vào buổi chiều không.

Sửa: gắn múi giờ, đổi sang UTC, rồi mới gộp và ghép. Bỏ qua thì ghép lệch không báo lỗi mà lặng lẽ dời dữ liệu.

## code-b03-dem-naive
Code tái hiện lỗi: đếm thẳng trên giờ không có múi giờ.

Dòng 3 đến 5 đọc giờ đón và giờ trả của tháng 3 và tháng 11, chỉ lấy hai cột cho nhanh. Dòng 7 đến 8 là hàm dem_naive: đặt giờ đón làm chỉ mục, resample theo giờ rồi đếm số dòng. Dòng 10 đến 11 xem quanh hai ngày vặn đồng hồ. Dòng 12 lấy cùng giờ tuần sau làm mốc so. Dòng 14 tìm chuyến có giờ trả trước giờ đón.

Kết quả: giờ 02:00 ngày 10/3 có 0 chuyến; giờ 01:00 ngày 3/11 có 9.869 chuyến, trong khi tuần sau chỉ 5.318. Còn chuyến có thời lượng âm, khách xuống xe trước khi lên, là dấu hiệu trừ thẳng hai giờ naive qua lúc vặn đồng hồ. Code không báo lỗi nào, chỉ có số là sai.

## code-b03-ghep-utc
Giờ là cách sửa: đưa cả hai bảng về UTC rồi mới ghép.

Dòng 5: thời tiết vốn là UTC, chỉ cần ghi rõ bằng tz_localize. Dòng 6 đến 7: taxi gắn giờ New York rồi đổi sang UTC; giờ không tồn tại hay giờ lặp thì ghi NaT thay vì đoán. Dòng 8 đến 9 đếm chuyến mỗi giờ UTC rồi ghép với thời tiết. Dòng 10 đến 11 là phép thử: giờ nóng nhất phải là buổi chiều. Dòng 13 đến 16: khi bảng phải thưa, dùng merge_asof, mặc định lấy dòng gần nhất ở trước, tức chỉ nhìn quá khứ.

Kết quả: giờ nóng nhất, ghép sai ra 20h, ghép đúng ra 16h. Tương quan mưa và số chuyến đổi dấu: ghép sai âm 0,100, ghép đúng cộng 0,136. merge_asof lấy giá 9 lúc 09:30, không lấy giá 10 của tương lai.

## gop
Buổi 4: gộp dữ liệu. Nhìn ba ô, cùng dữ liệu thuê xe ở ba mức gộp.

Ô trên theo giờ, 17.544 điểm, thành một khối màu, không đọc được gì. Ô giữa theo ngày: thấy dao động trong tuần và những ngày rơi sát 0. Ô dưới theo tháng: mượt, đẹp, thấy xu hướng và mùa vụ năm, nhưng đã gộp mất mùa vụ ngày, tuần và các ngày bất thường.

Dấu hiệu: kết luận "không có mùa vụ tuần" từ một hình như ô dưới; hoặc giờ thiếu hiện thành số 0. Kiểm bằng heatmap giờ nhân thứ và ACF tới trễ 168, và đếm NaN trên lưới giờ đầy đủ. Sửa: vẽ ở nhiều mức gộp. Khi cộng, dùng sum với min_count bằng 1, vì resample().sum() mặc định biến giờ thiếu thành 0 và kéo tổng xuống.

## code-b04-lam-tron-log
Code này cho thấy hai điều: làm trơn xoá mất ngày bất thường, và thang log đo tăng theo phần trăm, như slide khái niệm đã nói.

Dòng 4 cộng lượt thuê mỗi ngày, có min_count bằng 1 để ngày thiếu vẫn là NaN. Dòng 5 lấy trung bình trượt 7 ngày có tâm: 3 ngày trước, 3 ngày sau. Dòng 6 so ngày bão Sandy: số thật và số đã làm trơn. Dòng 8 lấy tổng tháng năm 2011. Dòng 9 đến 12 đặt cạnh nhau diff, tăng bao nhiêu lượt, và pct_change, tăng bao nhiêu phần trăm.

Kết quả: ngày bão chỉ còn 1 giờ số liệu mà đường trơn vẫn hơn 4.600 lượt; ngày bất thường đã bị xoá. Tháng 4 so tháng 3 tăng 48,1%, tháng 5 so tháng 4 tăng 43,2%, dù tháng 5 thêm nhiều lượt nhất, 40.951. Thang thường nói tháng 5 tăng mạnh nhất, thang log nói tháng 4.

## bieu-do-sai
Biểu đồ đẹp chưa chắc đúng: đọc thang trước khi đọc đường.

Hình trái: lượt thuê và nhiệt độ trên trục kép, hai trục dọc, trục trái cắt ở 90.000. Hai đường gần như đè nhau, trông như "lượt thuê bám sát nhiệt độ". Nhưng sự trùng khít là do chọn thang bên phải, còn trục cắt làm tháng 1 trông gần bằng 0.

Dấu hiệu: hai trục dọc trên một hình, hoặc trục y không bắt đầu từ 0. Kiểm bằng cách đọc thang từng trục. Sửa: hình phải, tách hai hình, số đếm vẽ từ 0, nói về quan hệ bằng scatter. Scatter cho thấy quan hệ có thật, r bằng 0,91 qua 12 tháng, nhưng không tăng mãi: tháng 9 mát hơn tháng 7 khoảng 5 độ mà lượt thuê cao nhất năm. Trục kép giấu mất điều đó.

## code-b04-tron-nam
Thay trục kép bằng con số: đo r, và thấy trộn hai năm làm quan hệ trông yếu đi.

Dòng 4 đến 5 gộp theo tháng năm 2012, mỗi cột một kiểu: lượt thuê thì cộng, nhiệt độ thì lấy trung bình. Dòng 6 tính r qua 12 tháng. Dòng 8 đến 10 chuyển sang theo ngày và tính r riêng cho từng năm bằng groupby. Dòng 11 gộp hai năm rồi tính r để so. Dòng 14: muốn đặt hai chuỗi lên chung một trục thì đánh chỉ số, tháng đầu bằng 100.

Kết quả: 12 tháng 2012, r bằng 0,91. Theo ngày, năm 2011 r bằng 0,771, năm 2012 bằng 0,714, nhưng gộp hai năm chỉ còn 0,627, vì cả đám chấm năm 2012 dời lên cao hơn. Scatter trộn nhiều năm thì tô màu theo thời gian.

## dao-dong
Buổi 5. Doanh thu tăng có thể vì ba lý do: giá tăng, dân số tăng, hoặc mỗi người mua nhiều hơn thật.

Hình phải: doanh số bán lẻ Mỹ, năm 1993 bằng 100. Danh nghĩa lên 416, trừ lạm phát còn 187, chia thêm dân số còn 142. "Tăng hơn 4 lần" chỉ còn tăng thật khoảng 42%.

Vấn đề thứ hai, hình trái: mỗi chấm là một năm, ngang là mức, dọc là độ lệch chuẩn trong năm. Năm bán nhiều thì dao động cũng lớn, từ 15,6 lên 38,1 tỷ USD. Như slide khái niệm về log đã nói, log hoặc Box-Cox làm dao động đều lại.

Kiểm bằng: so độ lệch chuẩn từng năm với mức, vẽ cạnh nhau chuỗi danh nghĩa và chuỗi thực. Sửa: log hoặc Box-Cox; chia CPI, dân số, và số ngày trong tháng. Khi báo "tăng bao nhiêu", nói rõ là danh nghĩa, thực, hay thực trên đầu người.

## code-b05-lich
Code đầu tiên: chia số ngày của tháng, vì tháng 2 ngắn nên mỗi năm "sụt" giả.

Dòng 4 lấy ba tháng đầu năm 2023. Dòng 5 lấy số ngày lịch bằng days_in_month: 31, 28, 31. Dòng 6 đến 8 đếm số ngày không phải Chủ nhật, dùng MonthEnd để nhảy tới cuối tháng. Dòng 9 đến 10 tính doanh số mỗi ngày theo hai cách đếm. Dòng 11 so với tháng trước theo phần trăm.

Kết quả: tháng 2 so tháng 1, tổng giảm 3,4% nhưng mỗi ngày lại tăng 7,0%: dấu đảo ngược. Tháng 3 so tháng 2: tăng 14,15% nếu so thẳng, 3,11% khi chia ngày, 1,47% khi bỏ Chủ nhật, và âm 1,05% theo chuỗi ADJUSTED. Cùng một câu hỏi, bốn câu trả lời. Và đừng dùng chuỗi ADJUSTED rồi lại chia số ngày, vì như vậy chênh lệch số ngày bị bỏ hai lần.

## code-b05-gia-thuc
Code bóc lạm phát và dân số khỏi doanh số.

Dòng 4 lấp đúng một tháng CPI không được công bố, tháng 10/2025, bằng interpolate với limit bằng 1. Dòng 5 đến 6 đổi ra giá năm gốc 2025: chia CPI của tháng đó, nhân CPI trung bình năm 2025. Dòng 7 chia dân số ra mức mỗi người. Dòng 8 đến 10 cộng thành tổng năm cho cả ba chuỗi. Dòng 11 đánh chỉ số 1993 bằng 100 để ba chuỗi khác đơn vị so được với nhau.

Kết quả: chỉ số năm 2025 là 416 danh nghĩa, 187 giá thực, 142 thực trên đầu người. Tức là giá chung tăng 2,23 lần và dân số tăng 1,31 lần; phần còn lại mới là mỗi người mua nhiều hơn thật.

## code-b05-log
Code kiểm hai điều về log.

Dòng 3 đến 4: 100 lên 120 và 1.000 lên 1.200 đều tăng 20%. Trên thang log cả hai cặp cách nhau đúng log của 1,2, tức 0,182. Log biến cùng phần trăm thành cùng khoảng cách, cửa hàng nhỏ và siêu thị được đối xử như nhau.

Dòng 7 đến 8 cắt chuỗi bán lẻ 1992 tới 2019 thành bảng, mỗi dòng một năm, bằng reshape 12 cột. Dòng 9 đến 10 tính mức và độ lệch chuẩn của từng năm. Dòng 11 so năm cuối với năm đầu.

Kết quả: mức gấp 3,1 lần, dao động gấp 2,4 lần. Dao động lớn lên theo mức, nhưng chậm hơn mức. Đó là lý do có khi log hơi quá tay, và Box-Cox cho chúng ta một núm vặn lambda ở giữa.

## doi-nguoc
Dự báo trên thang log xong, chúng ta phải exp để về đơn vị gốc. Như slide khái niệm về log đã nói, log ép số lớn lại; exp thì kéo chúng giãn ra. Hệ quả: đổi ngược thẳng cho ra trung vị, không phải trung bình.

Nhìn hình: histogram 100.000 mẫu. Vạch đen là trung bình thật, vạch cam là exp của trung bình log, thấp hơn 11,9%. Vạch xanh là có hiệu chỉnh, gần khớp.

Dấu hiệu: cộng dự báo nhiều cửa hàng ra tổng thấp hơn thật. Kiểm bằng so tổng dự báo với tổng thực tế trên kỳ chấm. Sửa: cần tổng hay trung bình thì nhân với 1 cộng sigma bình phương chia 2, sigma là độ lệch chuẩn sai số trên thang log. Chấm bằng MAE, vốn ưa trung vị, thì không cần. Hiệu chỉnh không sửa lệch do mô hình.

## code-b05-doi-nguoc
Code kiểm bằng mô phỏng.

Dòng 3 đến 4 là ví dụ tay: ba số log 0, 1, 2. Exp của trung bình là 2,72, còn trung bình của các exp là 3,70. Hai con số khác nhau, đó là toàn bộ vấn đề.

Dòng 6 sinh 100.000 mẫu log-normal, seed 42: log của chúng có hình chuông. Dòng 8 đổi ngược thẳng, ra trung vị. Dòng 9 nhân thêm 1 cộng nửa phương sai log, đó là hiệu chỉnh bias. Dòng 10 đo mỗi cách hụt bao nhiêu so với trung bình thật.

Kết quả: đổi ngược thẳng hụt 11,9%, có hiệu chỉnh gần khớp. Khoảng hụt nhỏ khi sigma nhỏ và lớn nhanh khi sigma gần 1, nên chỉ bật hiệu chỉnh khi cần trung bình và sigma đủ lớn.

## code-b05-backtest-log
Giờ ghép lại thành một backtest thật: seasonal naive có drift trên thang log.

Hàm du_bao_log: dòng 5 đến 6 lấy 96 tháng ngay trước gốc, rồi lấy log. Điểm quan trọng là chỉ dùng dữ liệu trước gốc. Dòng 7 đến 8 tính sai phân mùa vụ của log, từ đó ra drift và sigma bình phương. Dòng 10 dự báo bằng cùng tháng năm trước cộng drift. Dòng 11 đến 13 đổi ngược hai cách: thẳng ra trung vị, có hiệu chỉnh ra trung bình. Dòng 15 đến 16 chạy lại ở mỗi gốc từ tháng 1/2012 tới tháng 12/2018, 84 gốc.

Kết quả: 1.008 dự báo. Hiệu chỉnh đẩy tổng dự báo lên đúng cỡ sigma bình phương chia 2, nhưng chỉ giúp khi dự báo đang thấp. Chuỗi bách hoá vốn đã lệch gần cộng 10%, hiệu chỉnh còn làm tệ thêm. Luôn kiểm lệch trước khi bật.

## chu-ky-sai
Buổi 6: phân rã. Khai chu kỳ 24 cho chuỗi có nhịp tuần thì nhịp tuần chạy vào xu hướng.

Nhìn hình: tải điện tháng 7/2024 theo giờ, bốn hàng là dữ liệu, xu hướng, mùa vụ, phần dư. Dải xám là thứ Bảy, Chủ nhật. Hàng xu hướng lõm xuống đúng mỗi dải xám. Lý do: xu hướng là trung bình một ngày, Chủ nhật thấp thì trung bình quanh Chủ nhật cũng thấp. Hàng phần dư còn dao động đều mỗi ngày khoảng cộng trừ 15 GW, là mùa vụ ngày của tháng 7 mà khuôn chung cả năm không chứa được.

Kiểm bằng: trung bình xu hướng theo thứ; cuối tuần thấp hẳn là có vấn đề. Sửa: MSTL với hai chu kỳ 24 và 168. Giờ hỏng lẻ thì bật robust. Nhưng đợt nắng nóng nhiều ngày thì robust không tách được, cần thêm biến nhiệt độ.

## code-b06-mau-hinh
Code kiểm hai chỗ mùa vụ hay trốn.

Dòng 5 phân rã cổ điển chu kỳ 24 giờ. Dòng 6 đến 7 lấy xu hướng trung bình theo thứ: nếu có nhịp tuần thì sẽ thấy nó ở đây. Dòng 9 đến 12 là hàm ty_le_mau_hinh: lấy trung bình phần dư theo tháng và giờ, rồi chia phương sai cho phương sai chuỗi. Gần 0 nghĩa là phần dư sạch, không còn mẫu hình theo lịch. Dòng 14 đến 15 chạy MSTL với 24 và 168, rồi so bằng cùng thước đo.

Kết quả: xu hướng thứ Bảy, Chủ nhật thấp hơn giữa tuần khoảng 5.500 đến 6.600 MW. Tỷ lệ mẫu hình tháng nhân giờ: cổ điển 0,102, MSTL 0,0006. Một con số đủ để nói phân rã nào sạch hơn, không phải ngồi so hình.

## code-b06-robust
Code thứ hai: robust làm gì với một giờ hỏng.

Dòng 5 đến 6 là ví dụ tay: năm phần dư, trong đó có một số 20. Lấy trị tuyệt đối chia 6 lần trung vị của trị tuyệt đối. Dòng 7 tính trọng số: gần 1 là tin, bằng 0 là bỏ qua. Dòng 10 bật robust cho từng lượt STL bên trong MSTL. Dòng 13 đến 14 xem mùa vụ ngày hôm trước giờ hỏng có bị kéo lệch không. Dòng 15 xem phần dư ở chính giờ hỏng.

Kết quả: ví dụ tay, điểm 20 có trọng số 0, điểm âm 2 có trọng số 0,79. Trên dữ liệu thật, không robust thì mùa vụ ngày 20/11, một ngày không lỗi, lệch khoảng 6.200 MW vì lỗi bị chia ra cả tuần. Robust giữ trọn cú rơi trong phần dư, đúng chỗ nó thuộc về.

## sai-phan
Buổi 7. Sai phân như thuốc: đúng liều thì khỏi, quá liều thì hại.

Hình có hai cột. Cột phải: sai phân random walk, đúng liều, độ lệch chuẩn giảm từ 4,55 xuống 0,96, r một chỉ còn 0,100. Cột trái: sai phân nhiễu trắng vốn đã dừng, tức là thừa. Nhìn cột ACF trễ 1 ở ô dưới: r một bằng âm 0,447, và tiêu đề ghi độ lệch chuẩn tăng từ 0,96 lên 1,29. Chuỗi nhiễu hơn trước.

Dấu hiệu sai phân thừa: r một gần âm 0,5 kèm độ lệch chuẩn tăng. Kiểm bằng ADF, KPSS trước khi sai phân, và ACF sau khi sai phân. Sửa: bớt một lần sai phân; xu hướng thẳng thì khử xu hướng thay vì sai phân; có mùa vụ thì sai phân mùa vụ trước. Bỏ qua thì dự báo tệ hơn chỉ vì chúng ta đã tự thêm nhiễu.

## code-b07-sai-phan
Code biết khi nào dừng sai phân.

Dòng 5 đến 8 là hàm dau_hieu: sai phân một lần, trả r một sau sai phân và độ lệch chuẩn trước, sau. Dòng 11 chạy trên nhiễu trắng, chuỗi đã dừng, để thấy dấu hiệu thừa. Dòng 12 chạy trên random walk, tạo bằng cumsum, để thấy đúng liều. Dòng 14 lấy log của 1 cộng lượt thuê xe theo giờ, dùng log1p vì có giờ không ai thuê. Dòng 15 đến 16 so ba cách: sai phân thường, sai phân mùa vụ 168, và cả hai.

Kết quả: nhiễu trắng r một bằng âm 0,447, độ lệch chuẩn 0,96 lên 1,29, là thừa. Random walk 4,55 xuống 0,96, đúng liều. Lượt thuê: sai phân 168 rồi sai phân thường thì độ lệch chuẩn giảm từ 0,589 xuống 0,427. r một là âm 0,249, chưa tới dấu hiệu thừa: ở đây cả hai lần sai phân đều đáng.

## tuong-quan-gia
Buổi 8: tương quan. Tương quan giả là r rất cao chỉ vì hai chuỗi cùng tăng theo thời gian.

Nhìn hình: ô trái, CPI và dân số Mỹ cùng đi lên. Ô giữa, scatter trên mức: chấm nằm gần như một đường, r bằng 0,974. Ô phải, scatter trên thay đổi hằng tháng: đám chấm không có hình dạng, r chỉ còn âm 0,207. Câu hỏi đúng là: tháng nào dân số tăng nhanh thì giá có tăng nhanh không? Câu trả lời là không.

Kiểm bằng hai cách: sai phân rồi đo lại r, và Durbin–Watson của phần dư hồi quy. Durbin–Watson gần 2 là tốt, gần 0 là phần dư tự tương quan mạnh, dấu hiệu tương quan giả. Bỏ qua thì chúng ta chọn một biến giải thích vô dụng. Khi viết kết luận, nói "đi cùng", đừng nói "gây ra".

## code-b08-tuong-quan-gia
Code bắt tương quan giả bằng hai phép kiểm.

Dòng 3 đến 4 là Durbin–Watson: tổng bình phương bước nhảy của phần dư chia tổng bình phương phần dư. Phần dư đổi chậm thì bước nhảy nhỏ, con số gần 0. Dòng 6 đến 8 khớp đường thẳng bằng lstsq, bình phương nhỏ nhất, rồi lấy phần dư. Dòng 9 đến 10 trả R bình phương, thống kê t của hệ số, và DW. Dòng 13 hồi quy dân số theo CPI trên mức. Dòng 14 đến 15 hỏi lại câu đúng: lấy thay đổi hằng tháng rồi tính tương quan.

Kết quả: trên mức, r bằng 0,974, R bình phương 0,95, t bằng 88,6, trông cực kỳ chắc chắn. Nhưng DW chỉ 0,0051, và r sau sai phân là âm 0,207. R bình phương cao, t lớn, DW gần 0: đó là bộ ba của hồi quy giả.

## chu-u
Pearson chỉ đo quan hệ thẳng. Tải điện ERCOT ở Texas theo nhiệt độ có hình chữ U: trời nóng bật điều hoà, trời lạnh bật sưởi.

Nhìn ô trái: mỗi chấm một giờ năm 2024. Đường đen là hồi quy thẳng, đường cam là hồi quy theo hai nhánh. Phía bên trái 18 độ, đường đen đi xuống mà chấm đi lên: đường thẳng bỏ sót hẳn nhánh lạnh. Pearson 0,616 trông khá mạnh, nhưng là trộn nhánh lạnh âm 0,649 với nhánh nóng cộng 0,910.

Kiểm bằng: vẽ scatter trước, đo thêm mutual information vì nó bắt được quan hệ cong. Sửa: tách nhiệt độ thành CDD, độ nóng, bằng nhiệt độ trừ 18,33 nếu dương, và HDD, độ lạnh, bằng 18,33 trừ nhiệt độ nếu dương. R bình phương tăng từ 0,379 lên 0,812. Ô phải cho thấy mốc 18,33 là quy ước, gần mốc tốt nhất 19,5 độ.

## code-b08-cdd-mi
Code tách chữ U và kiểm mutual information có thật không.

Dòng 4 tính CDD và HDD bằng np.maximum với 0, mốc 18,33 độ, tức 65 độ F. Dòng 5 đến 9 so R bình phương của hồi quy theo nhiệt độ với theo CDD cộng HDD. Dòng 10 đến 11 tính MI bằng mutual_info_regression. Dòng 13 đến 15 là phần tinh tế: để biết MI bao nhiêu thì đáng tin, chúng ta xáo thứ tự các khối một tuần, 100 lần. Xáo từng điểm sẽ phá tự tương quan, khiến cả hai chuỗi độc lập cũng trông "có quan hệ". Dòng 16 lấy ngưỡng 95% của MI khi không có quan hệ.

Kết quả: R bình phương từ 0,379 lên 0,812. MI thật 0,862, vượt xa ngưỡng xáo khối 0,124. Quan hệ có thật, chỉ là không thẳng.

## thieu-moc
Buổi 10: dữ liệu thiếu. Có hai loại. Thiếu giá trị là có dòng, ô rỗng. Thiếu mốc là mất cả dòng. isna() chỉ thấy loại thứ nhất.

Ví dụ: đo mỗi 30 phút từ 00:00 tới 02:30 phải có 6 mốc, tệp có 5 dòng. isna() báo 1 ô thiếu lúc 02:00, nhưng mốc 01:00 mất cả dòng mà không ai biết.

Nhìn hình trạm Nội Bài: ô trái, số mốc thiếu theo tháng, dồn vào vài tháng, nhiều nhất tháng 7, dấu hiệu sự cố hệ thống. Ô phải, độ dài lỗ: hai phần ba số lỗ chỉ dài một bước, lỗ dài nhất 8 giờ.

Kiểm bằng: so số dòng với số mốc của lưới đầy đủ, đếm mốc trùng. Sửa: reindex lên lưới đầy đủ trước mọi việc khác. Bỏ qua thì lag và rolling đếm sai số bước.

## code-b10-luoi
Code dựng lưới rồi mới đếm thiếu.

Dòng 4 đến 6 tạo năm dòng đo, mốc 01:00 không có dòng nào, mốc 02:00 có dòng nhưng ô rỗng. Dòng 7 dùng pd.date_range dựng lưới đủ mọi mốc 30 phút từ đầu tới cuối. Dòng 8 đến 9 đếm thiếu hai lần: trước và sau khi reindex lên lưới. reindex đặt chuỗi lên bộ mốc mới, mốc nào chưa có dòng thì thành NaN. Dòng 11 đến 14 là hàm do_dai_lo: đánh số từng đoạn NaN liền nhau rồi đếm độ dài, để biết lỗ ngắn hay dài.

Kết quả: ví dụ nhỏ, isna() báo 1, lên lưới ra 2. Trạm Nội Bài năm 2024: lưới có 17.568 mốc, tệp chỉ có 17.319 dòng, thiếu 249 mốc, trong khi isna() chỉ thấy 2 ô. Đếm trước khi dựng lưới là đếm sai.

## mcar
Biết có bao nhiêu chỗ thiếu rồi, câu hỏi tiếp theo quan trọng hơn: vì sao thiếu. Điền được hay không phụ thuộc vào lý do, không phụ thuộc cách điền giỏi tới đâu.

Nhìn hình: chấm xanh là số còn lại, chấm đỏ là số bị mất. MCAR mất rải đều, như mất mạng vài phút: phần còn lại vẫn đại diện, điền thoải mái. MAR mất dồn trong vùng xám, như trạm hay hỏng mùa mưa: điền được nếu cách điền dùng thông tin mùa. MNAR mất đúng các đỉnh trên vạch đứt: phần còn lại đã bị lọc lệch.

Ví dụ tính tay: bốn giờ PM2.5 thật 10, 20, 30, 40, trung bình 25. Cảm biến tắt khi trên 30, chỉ còn 10, 20, 30, trung bình 20. (dừng) Lệch 5 trước khi chúng ta điền bất cứ gì.

## mnar
Slide trước là định nghĩa, slide này là hậu quả khi thiếu vì chính giá trị.

Nhìn ô trái: xám là dữ liệu thật, vạch đứt là ngưỡng 1 mà cảm biến tắt. MNAR mất 16,2% số điểm, toàn ở phía cao. Cam là sau khi điền bằng nội suy: vẫn không có phần bên phải vạch. Ô phải: trung bình sau khi điền là âm 0,30, trong khi thật là âm 0,005. MCAR chỉ lệch một phần nghìn. Điền kiểu gì cũng không lấy lại được thứ đã bị lọc.

Kiểm trên dữ liệu thật: so các trạm hàng xóm lúc một trạm thiếu và lúc có số. Khi trạm Dongsi ở Bắc Kinh thiếu, các trạm khác còn thấp hơn 3%: không có bằng chứng MNAR. Phải đo, đừng giả định. Sửa: MCAR, MAR thì điền được; MNAR thì đừng điền, và báo tỷ lệ thiếu theo trạm, theo tháng.

## code-b10-mnar
Code mô phỏng, nơi chúng ta biết trước đáp án.

Dòng 4 đến 6 sinh 5.000 điểm thật, hình chuông tâm 0, seed 0. Dòng 7 tạo MCAR: xoá ngẫu nhiên 10% bằng mask. Dòng 8 tạo MNAR: xoá đúng những điểm cao hơn 1, như cảm biến tắt khi giá trị cao. Dòng 9 đến 10 nội suy cả hai rồi so trung bình với số thật. Dòng 12 đến 15 là hàm bang_chung_mnar cho dữ liệu thật: lấy trung bình 11 trạm còn lại, so lúc trạm đang xét thiếu với lúc có số.

Kết quả: MNAR mất 16,2%, điền xong trung bình âm 0,30 thay vì âm 0,005; MCAR gần như không lệch. Trên dữ liệu Bắc Kinh, Dongsi thiếu thì các trạm khác thấp hơn 3,0%. Nếu MNAR, lúc thiếu phải là lúc ô nhiễm cao, tức trạm khác phải cao hơn, chứ không phải thấp hơn.

## tra-hinh
Không phải chỗ thiếu nào cũng hiện ra là NaN. Mã trá hình là con số quy ước của nguồn, không phải số đo.

Nhìn hình trạm Nội Bài, ba ô. Ô trái: cột cao vọt ở mép phải, tầm nhìn đúng bằng 9,999 km, chiếm 35% số dòng. Nó nghĩa là "10 km trở lên", không phải một phép đo. Ô giữa: độ ẩm chạm trần 100%. Ô phải: các khe trống đều đặn, nhiệt độ chỉ ghi số nguyên.

Kiểm bằng value_counts().head() và đọc tài liệu nguồn; đo độ phân giải trước khi gọi một đoạn lặp là cảm biến kẹt. Sửa: đổi thành NaN kèm cột cờ ghi lý do. Đừng dropna() cả dòng, vì dòng có tầm nhìn 9,999 vẫn có nhiệt độ hợp lệ. Số 0 do hết hàng cũng là thiếu: không đánh dấu thì mô hình dự báo thấp, cửa hàng nhập ít, lại hết hàng, vòng lặp tự củng cố.

## code-b10-tra-hinh
Mã trá hình, trần cảm biến, độ phân giải và đoạn kẹt có một điểm chung: không cái nào để lại NaN, nên phải đo từng dấu vết. Dòng 5: gọi min trên cột độ ẩm ra chữ '100', vì cột số đang lưu dạng chữ và pandas so theo thứ tự chữ cái. Dòng 6 và 7 ép về số, chữ lạ thành NaN. Dòng 8 đo tỷ lệ mã 9,999 km và tỷ lệ độ ẩm chạm 100. Dòng 9 và 10 lấy bước nhỏ nhất giữa hai giá trị khác nhau, tức độ phân giải. Dòng 12 đến 16 đánh số từng đoạn lặp liền nhau rồi giữ đoạn đủ dài. Kết quả: độ ẩm dạng chữ cho min '100' mà max '94'; hơn một phần ba dòng tầm nhìn là mã 9,999; 5,7% độ ẩm chạm trần; ngưỡng 18 giờ tìm ra 2 đoạn kẹt, dài nhất 33,5 giờ.

## so-sanh-dien
Có bảy cách điền rồi, vậy làm sao biết cách nào tốt khi ta không có số thật ở chỗ thiếu? Ta tự tạo đáp án: che nhân tạo, tức xoá bớt những ô đang có số, điền lại, rồi so với số vừa xoá. (chỉ vào bảng) Cùng bảy cách, cùng chuỗi Nội Bài, chỉ đổi kiểu che. Che rải rác 10% điểm thì tuyến tính đứng hạng 1, MAE 0,291; che khối 48 giờ thì nó tụt xuống hạng 5, MAE 2,171. Trạm hàng xóm đi ngược lại, từ hạng 5 lên hạng 1. Vì sao? Lỗ ngắn thì nối hai đầu là đủ; lỗ dài thì cần một nguồn mang theo hình dạng nhịp ngày. Nếu chỉ che một kiểu, ta sẽ chọn cách điền giỏi ở lỗ ngắn mà tệ ở lỗ dài. Nguyên tắc: dữ liệu có kiểu lỗ nào thì che và chấm đúng kiểu đó.

## code-b10-dien
Dòng 5 và 6: hôm nay mất hai giờ, số thật là 26 và 28; bên dưới là số cùng giờ hôm qua. Dòng 7 đến 9 là ba cách chỉ biết hai đầu lỗ: ffill chép số trước, tuyến tính nối thẳng, spline nối cong. Dòng 10 và 11 mượn hình dạng từ nguồn khác: mùa vụ lấy cùng giờ hôm qua, hàng xóm lấy hôm qua cộng 1. Dòng 12 đến 16 là cách Kalman: UnobservedComponents khớp một mô hình gồm mức đổi dần cộng nhịp ngày rồi lấy giá trị làm trơn, tức nhìn cả hai phía. Kết quả: ffill sai nhiều nhất, lệch 3 và 5; tuyến tính lệch 1,67 và 2,33; mùa vụ lệch 1 và 1; hàng xóm trúng cả hai. Ngoài đời, Nội Bài với Open-Meteo tương quan r bằng 0,976, nên hàng xóm là nguồn rất tốt.

## code-b10-che
Đây là code sinh ra bảng hai kiểu che ở slide “Chấm cách điền” vừa xem. Dòng 3 đến 7, che điểm: lấy vị trí các ô đang có số, rút ngẫu nhiên 10% không trùng, rồi xoá. Dòng 9 đến 15, che khối: xoá năm đoạn liền, mỗi đoạn 96 bước, tức 48 giờ với dữ liệu nửa giờ một lần. Cả hai đều có seed để chạy lại ra đúng số. Dòng 16 là chỗ quan trọng nhất: MAE chỉ tính trên những ô vừa bị che, vì các ô còn lại vẫn là số thật, tính vào chỉ làm sai số nhỏ đi giả tạo. Kết quả: tuyến tính hạng 1 ở lỗ ngắn với MAE 0,291 °C nhưng hạng 5 ở lỗ 48 giờ với 2,171; hàng xóm đi ngược lại, từ hạng 5 lên hạng 1.

## dien
Giờ nhìn một lỗ dài cụ thể. (chỉ vào hình) Lỗ 48 giờ: ffill và nội suy tuyến tính đều vẽ thành một đường phẳng quanh 24 °C, trong khi thật nhiệt độ dao động 21 đến 27 °C mỗi ngày. Nhịp ngày bị xoá sạch, và mô hình học từ đoạn phẳng đó sẽ học sai. Trạm hàng xóm thì giữ được hình dạng. Dấu hiệu cần để ý là đoạn phẳng dài bất thường, hoặc backtest đẹp hẳn lên sau khi làm sạch. Cái sau là do nội suy dùng điểm phía sau: điền ngày 3 bằng cách nối ngày 2 với ngày 4 là đã dùng ngày 4. Kiểm bằng kiem_ro_ri với mốc cắt đặt ngay trong lỗ. Sửa: chia tập trước rồi mới điền, chỉ dùng cách điền nhân quả, lỗ ngắn thì điền, lỗ dài để trống, và luôn giữ cột cờ da_dien. Riêng dữ liệu MNAR thì điền kiểu gì cũng lệch.

## code-b10-lam-sach
Gói hai nguyên tắc vừa rồi thành một hàm. Dòng 4: biến các số nghi ngờ thành NaN trước tiên, để chúng không bị dùng làm đầu mút khi điền. Dòng 5 đến 7 đo độ dài lỗ cho từng ô thiếu, cùng mẹo đánh số đoạn như slide đoạn kẹt. Dòng 8 và 9 chỉ điền lỗ tới 6 bước, tức 3 giờ, bằng cách mùa vụ vì nó nhân quả; lỗ dài để trống. Dòng 10 xuất kèm cột cờ da_dien. Dòng 12 đến 16 là máy kiểm: làm sạch trên dữ liệu đủ và trên dữ liệu cắt tại một mốc nằm trong lỗ, rồi so phần trước mốc; khác nhau là có rò rỉ. Kết quả trên Nội Bài: 130 ô bị loại vì nghi ngờ, 198 ô được điền, 181 ô để trống. Còn bản điền mọi lỗ bằng tuyến tính thì bị máy kiểm bắt ngay khi mốc cắt rơi vào lỗ.

## bon-loai
Sang buổi 11: ngoại lai. Chữ "ngoại lai" thật ra gộp bốn thứ khác nhau. (chỉ vào hình) Quanh mức 10: điểm đơn AO lệch lên 25 rồi về ngay; dịch mức LS nhảy lên 20 và ở lại; thay đổi tạm TC nhảy lên 20 rồi tắt dần 15, 12, 11, 10; còn đổi phương sai thì mức giữ nguyên nhưng dao động to ra. Vì sao phải phân loại? Vì loại quyết định cách bắt và cách sửa, không phải độ lớn. Hampel bắt điểm đơn, tìm điểm gãy bắt dịch mức, MAD trên phần dư STL bắt đổi phương sai. Nên trước một điểm lạ, câu hỏi đầu tiên là: đây là lỗi, giai đoạn tạm thời, hay một trạng thái mới?

## code-b11-bon-loai
Bốn loại giống hệt nhau ở đúng cái mốc lạ; chỉ các điểm sau mốc mới tách được chúng. Dòng 4 đến 7 là bốn chuỗi tám điểm, cùng nền 10. Dòng 9 lấy riêng điểm 4, và các bạn sẽ thấy nó chưa phân biệt được gì. Dòng 10 đến 12 là ba câu hỏi về phần sau mốc: trung bình bốn điểm sau cho biết nó có ở lại không, điểm cuối cho biết có hồi về không, độ lệch chuẩn sau cho biết có rung mạnh hơn không. Dòng 13 gom thành bảng, mỗi dòng một loại. Kết quả: điểm 4 không tách được ba loại đầu; nhìn bốn điểm sau thì tách rõ: AO về 10, dịch mức ở lại 20, thay đổi tạm hồi dần. Đổi phương sai có độ lệch chuẩn phần sau là 4,08. Bài học: đừng phán loại khi mới thấy một điểm, hãy chờ thêm vài bước.

## masking
Cách bắt ngoại lai quen nhất là z-score: điểm cách trung bình bao nhiêu lần độ lệch chuẩn, quá 3 thì gắn cờ. Vấn đề là chính ngoại lai kéo trung bình lên và làm độ lệch chuẩn phình ra, nên nó tự che mình. Hiện tượng này gọi là masking. Ví dụ năm số 5, 5, 5, 5, 100: điểm 100 chỉ có z bằng 1,79, không bị gắn cờ. (chỉ vào hình) Trên lượt xem Wikipedia, 3σ gắn cờ 16 ngày; thêm đúng một ngày cực lớn thì chỉ còn 5. Đó cũng là cách kiểm: thêm một điểm cực lớn rồi đếm lại, số cờ giảm là đang bị che. Còn nữa, với mẫu nhỏ z có trần: mười số thì tối đa 2,85, ngưỡng 3 không bao giờ bắt được gì. Sửa bằng MAD và Hampel, dựa trên trung vị nên ngoại lai không kéo được.

## code-b11-masking
Giờ thấy masking bằng số. Dòng 4 và 5 là hàm z_score quen thuộc: cách trung bình quá 3 độ lệch chuẩn thì gắn cờ. Dòng 7 và 8: mười số quanh 11, 12, có một số 50 nổi bật, tính z của nó. Dòng 9 tính trần của trị tuyệt đối z khi n bằng 10, bằng n trừ 1 chia căn n, ra 2,85. Dòng 11 đến 13: lấy chuỗi lượt xem Wikipedia, chèn một ngày giả lớn gấp 8 lần ngày cao nhất vào giữa, rồi đếm số cờ trước và sau. Kết quả: z của 50 chỉ 2,84, nằm dưới trần 2,85, nên dù nhìn bằng mắt là thấy ngay, ngưỡng 3 không bao giờ bắt được. Trên Wikipedia, thêm một ngày giả làm số ngày bị gắn cờ tụt từ 16 xuống 5. Một ngoại lai lớn làm các ngoại lai khác biến mất.

## hampel
Cách sửa masking có hai bước. MAD đo độ dao động bằng trung vị thay vì trung bình, nên ngoại lai không kéo được. Hampel đi thêm một bước: so mỗi điểm với trung vị và MAD của cửa sổ quanh nó, nên xu hướng dài hạn không làm nó mù. (chỉ vào hình và bảng) Trên 3.653 ngày Wikipedia, 3σ toàn chuỗi gắn cờ 16 ngày, toàn là ngày ở giai đoạn mức cao, bỏ sót bất thường ở vùng mức thấp. Hampel ±15 ngày gắn cờ 121 ngày, 3,31%, rải đều mười năm. STL robust thì tới 16,86%, quá nhiều để gọi là ngoại lai. Vậy trước khi tin một ngưỡng, xem nó gắn cờ bao nhiêu phần trăm dữ liệu. Sửa bằng winsorize, kéo điểm về trung vị địa phương, không xoá mốc. Lưu ý Hampel dùng cửa sổ giữa, nên chỉ để làm sạch, không làm feature.

## code-b11-hampel
Đổi trung bình thành trung vị là xong phần khó. Dòng 4: hệ số 1,4826 đưa MAD về cùng thang với độ lệch chuẩn, để ngưỡng 3 vẫn có nghĩa như trước. Dòng 6 đến 9 là điểm MAD toàn chuỗi: khoảng cách tới trung vị chia cho 1,4826 lần MAD. Dòng 11 đến 13: Hampel lấy trung vị của 31 ngày quanh mỗi điểm, cửa sổ đặt giữa. Dòng 14 tính MAD cũng trên cửa sổ đó. Dòng 15 và 16 gắn cờ điểm cách mức địa phương quá 3; chỗ MAD bằng 0 được đổi thành NaN để khỏi chia cho 0. Kết quả: điểm MAD của số 50 là 25,6, bắt ngay, trong khi z chỉ 2,84. Trên Wikipedia, Hampel gắn cờ 121 ngày rải đều mười năm, và thêm ngày giả chỉ làm con số thành 123. Ngoại lai không còn che được nhau.

## tet
Giờ là mặt ngược lại: bắt được ngoại lai rồi, có nên sửa hết không? (chỉ vào hình) Chạy bộ bắt ngoại lai trên lượt xem Wikipedia tiếng Việt thì cả 10 trên 10 đỉnh Tết bị gắn cờ. Nhưng Tết là bất thường thật, và là thứ đáng dự báo nhất trong năm; xoá đi là xoá mất nó. Đỉnh Tết còn xê dịch tới 25 ngày giữa các năm vì theo lịch âm, nên phân rã theo lịch dương không học được. Kiểm bằng cách vẽ chuỗi quanh những mốc bị sửa rồi đối chiếu với lịch lễ. Sửa: giữ nguyên, ghi vào nhật ký sự kiện, thêm biến giả theo lịch âm. Và chọn cách sửa theo loại: điểm đơn là lỗi thì winsorize, dịch mức hay thay đổi tạm thì biến giả. Ngoại lai không đồng nghĩa với lỗi.

## code-b11-tet
Ngưỡng nào cũng gắn cờ Tết, nên phải có nhật ký sự kiện chặn lại. Dòng 3: ngày đông nhất mỗi năm chính là đỉnh Tết. Dòng 4 kiểm xem Hampel có gắn cờ các đỉnh đó không. Dòng 6 đến 13 là hàm xu_ly_ngoai_lai: dòng 8 và 9 bỏ cờ ở những mốc có trong nhật ký, dòng 10 đến 12 thay các điểm lỗi còn lại bằng trung vị quanh nó, tức winsorize, và dòng 13 trả kèm cột da_sua để biết ô nào đã bị thay. Dòng 15 chạy trên chuỗi Tết với nhật ký là mười đỉnh. Kết quả: năm cách gắn cờ khác nhau đều bắt 10 trên 10 đỉnh Tết. Xoá theo 3σ làm mất 54 mốc, trong đó có cả mười đỉnh; winsorize cộng nhật ký giữ đủ 3.653 mốc, lưới thời gian không bị thủng.

## pelt
Loại bất thường thứ hai cần công cụ riêng là dịch mức, tức điểm gãy: mốc mà trước và sau khác hẳn nhau. PELT cắt chuỗi thành các đoạn sao cho tổng chi phí các đoạn cộng penalty là nhỏ nhất; mỗi điểm gãy thêm vào phải giảm chi phí nhiều hơn penalty. Penalty thấp thì cắt vụn, cao thì bỏ sót. (chỉ vào hình) Trên hành khách bay EU, chạy trên mức gốc ra 43 điểm gãy. Vì sao? Dao động lớn dần theo mức, nên mỗi mùa hè đông khách trông như một đoạn mới. Lấy log trước thì dao động đều lại, chỉ còn 2 điểm gãy, đúng quanh COVID, và ổn định khi penalty đi từ 1 tới 4 lần ln n. Kiểm nhanh: số điểm gãy phải giảm khi penalty tăng. PELT hợp để phân tích lịch sử, không hợp để báo động thời gian thực.

## code-b11-pelt
Dòng 4 và 5: mười số có một bậc từ 10 lên 20, penalty đặt bằng 3 lần ln n. Dòng 6 gọi ruptures: Pelt tìm cách cắt rẻ nhất, predict trả vị trí kết thúc từng đoạn. Dòng 8 đến 12 là hàm diem_gay: dòng 9 lấy log để mùa hè đông khách thôi bị coi là gãy, dòng 11 và 12 chạy PELT rồi đổi vị trí cắt thành ngày tháng, bỏ phần tử cuối vì đó chỉ là độ dài chuỗi. Dòng 14 đến 16 quét bảy mức penalty từ 0,5 đến 10 lần ln n, để xem điểm nào trụ lại. Kết quả: ví dụ tay ra 5 và 10, tức một điểm gãy sau vị trí 5. Hàng không EU: mức gốc ra 43 điểm gãy, log ra 2, ổn định từ 1 tới 4 lần ln n, là 2/2020, giảm 78,7%, và 5/2021. Điểm gãy đáng tin là điểm không đổi khi penalty đổi.

## covid
Tìm ra điểm gãy COVID rồi, xử lý đoạn đó thế nào? (chỉ vào bảng) Cùng một mô hình, chỉ đổi cách xử lý, MAPE năm 2023 chênh gần 3 lần. Giữ nguyên: 24,01%, vì đoạn sụt kéo cả đường xu hướng xuống. Cắt, chỉ học sau hồi phục: 18,11%, vì chỉ còn 18 tháng, quá ngắn để học mùa vụ. Coi COVID là thiếu rồi nội suy qua: 8,71%, tốt nhất ở đây. Nhưng đừng nhớ "nội suy luôn thắng". Nội suy chỉ hợp khi hành vi quay về như cũ; nếu sau cú sốc là một mức mới kéo dài thì dùng biến giả. Chọn cách nào là một giả định về tương lai, nên phải thử từng cách, chấm dự báo trên năm sau đó, và ghi rõ giả định vào báo cáo.

## code-b11-covid
Mô hình ở đây cố tình đơn giản và giữ cố định, để chỉ còn một thứ thay đổi là cách xử lý COVID. Dòng 5 đến 7 dùng np.polyfit khớp một đường thẳng làm xu hướng. Dòng 8 và 9 tính mỗi tháng là một tỷ lệ so với xu hướng, rồi lấy trung bình theo tháng trong năm, tức mùa vụ nhân. Dòng 10 đến 12 kéo dài xu hướng và nhân hệ số tháng để ra dự báo. Dòng 14 học tới hết 2022 và đánh dấu 16 tháng COVID, từ 3/2020 tới 6/2021. Dòng 15 và 16 là ba cách: giữ, dùng mask rồi interpolate để coi là thiếu, và cắt chỉ giữ sau 6/2021. Kết quả: coi là thiếu cho MAPE 8,71%, giữ nguyên 24,01%. Giữ nguyên thì 16 tháng sụt kéo xu hướng xuống, dự báo thấp gần 20 triệu khách mỗi tháng.

## aliasing
Sang buổi 12: nhiễu và tần số. Trước khi lọc hay hạ mẫu, ta đọc phổ, tức xem dao động của chuỗi nằm ở tần số nào. (chỉ vào hình trái) Trục ngang là tần số, trục đứng là năng lượng. Cả hai cảm biến có đỉnh ở chu kỳ khoảng một ngày, nhưng điện thiết bị còn 17,8% năng lượng ở dao động nhanh hơn một giờ, còn nhiệt độ phòng gần như không có. Nên lọc nhiệt độ chỉ thêm trễ. (chỉ vào hình phải) Lấy mẫu quá thưa thì dao động nhanh biến thành nhịp chậm không có thật, gọi là aliasing, như bánh xe quay ngược trong phim cũ. Giới hạn Nyquist là nửa tần số lấy mẫu; nhanh hơn mức đó sẽ bị gập xuống. Dao động 43 phút, hạ mẫu thô xuống 1 giờ, sinh chu kỳ giả 2,5 giờ. Sửa: lọc thông thấp trước khi hạ mẫu.

## code-b12-pho
Trước khi lọc, đo hai thứ: nhịp nào mạnh nhất, và dao động nhanh chiếm bao nhiêu năng lượng. Dòng 5 đến 7 là hai dãy tính tay: dãy đổi dấu mỗi bước lặp mỗi 2 bước, dãy ba cộng ba trừ lặp mỗi 6 bước; periodogram phải cho đỉnh ở 0,5 và một phần sáu. Dòng 9 đến 12 là hàm pho: trừ trung bình trước, để thành phần tần số 0 không át hết, rồi dùng Welch, tức chia chuỗi thành đoạn và lấy trung bình phổ các đoạn cho ổn định. Dòng 14 và 15 tìm chu kỳ mạnh nhất, bỏ qua tần số 0. Dòng 16 là tỷ lệ năng lượng ở tần số trên 1 vòng mỗi giờ. Kết quả: ví dụ tay đúng ở 0,5 và một phần sáu; cả hai cảm biến có đỉnh 24,38 giờ; điện thiết bị có 17,8% năng lượng dưới 1 giờ, nhiệt độ phòng 0,0.

## code-b12-aliasing
Dòng 5 và 6 là công thức tần số giả: lấy trị tuyệt đối của f trừ k lần tần số lấy mẫu, với k là số nguyên gần f chia tần số lấy mẫu nhất. Dòng 11 là hạ mẫu thô: cứ 6 mẫu lấy một, từ 10 phút lên 1 giờ. Dòng 12 thiết kế bộ lọc Butterworth cắt ở 0,8 lần Nyquist mới, tức chừa một khoảng an toàn. Dòng 13 lọc hai chiều rồi mới lấy mẫu; ở đây ta xử lý dữ liệu lịch sử nên lọc hai chiều không sao, nhưng không dùng cách này làm feature. Dòng 15 và 16 tạo chuỗi thử: nhịp ngày cộng dao động 1,4 chu kỳ mỗi giờ. Kết quả: 1,4 lấy mẫu mỗi giờ gập thành 0,4, tức chu kỳ giả 2,5 giờ; công suất ở đó là 64,0 khi hạ mẫu thô và 0,0 khi lọc trước.

## bo-loc
Như slide trước đã nói, độ trơn luôn phải trả giá: hoặc trễ, hoặc nhìn tương lai. Trung bình trượt 13 điểm kiểu trailing chạy sau tín hiệu 6 bước. (chỉ vào hình) Buổi 12 so sáu họ bộ lọc trong mười cấu hình. Ba cái RMSE thấp nhất, trung bình trượt centered, Kalman smoother và Savitzky–Golay, đều nhìn tương lai, nên không dùng được làm feature. Nếu chỉ nhìn bảng RMSE, ta sẽ chọn đúng bộ lọc không chạy được lúc dự báo. Sửa: thêm cột "nhân quả" vào bảng xếp hạng và chỉ so các bộ lọc nhân quả với nhau. Trong nhóm này Kalman filter tốt nhất, RMSE 0,584; Butterworth nhân quả tệ nhất, 2,419, vì trễ 19 bước. Thêm một lưu ý: khử nhiễu bôi nhoè bước nhảy, nên tìm điểm gãy trước rồi mới lọc.

## code-b12-bo-loc
Code chạy các họ bộ lọc trên cùng một chuỗi mô phỏng có nhiễu, seed 0, nên biết được tín hiệu thật để tính RMSE. Dòng 7 và 8: tham số Kalman chỉ học trên một phần ba đầu, để không rò rỉ qua tham số. Dòng 9 đến 11: trung bình trượt trailing, centered và EWMA. Dòng 12: Savitzky–Golay khớp đa thức bậc 2 trong cửa sổ 13 điểm có tâm, giữ đỉnh tốt nhưng dùng điểm phía sau. Dòng 13 và 14 là cùng một bộ Butterworth, chạy một chiều bằng sosfilt hoặc hai chiều bằng sosfiltfilt. Dòng 15 và 16: Kalman filter chỉ dùng quá khứ, Kalman smoother dùng cả hai phía. Kết quả: ba RMSE thấp nhất, centered 0,357, Kalman smoother và Savitzky–Golay, đều nhìn tương lai. Nhân quả tốt nhất là Kalman filter, 0,584, trễ chỉ 1 bước.

## loc-tuong-lai
Như slide trước đã nói, bộ lọc nhân quả chỉ dùng dữ liệu tới thời điểm đang xét. Nhưng đọc code không phải lúc nào cũng thấy nó có nhìn tương lai hay không, nên ta cần một phép thử: đổi vài điểm cuối chuỗi rồi chạy lại. Quá khứ mà đổi theo là bộ lọc đã nhìn tương lai. (chỉ vào hình) Sau khi đổi 10 giá trị cuối, trailing không đổi ở mốc nào trước đó; centered đổi ở 6 mốc ngay trước. Cái giá nếu bỏ qua: feature làm trơn kiểu centered hay filtfilt hứa giảm MAE 24 đến 28%, còn mọi feature nhân quả chỉ giúp 1 đến 6%, và phần thưởng giả mất sạch khi chạy thật. Sửa: dùng trailing, EWMA hay sosfilt; tham số ước lượng trên phần học rồi cố định; và luôn chấm trên chuỗi gốc.

## code-b12-trailing
Bắt đầu bằng ví dụ năm giờ tính tay được. Dòng 3: năm giờ điện, giờ 4 vọt lên 30. Dòng 4 và 5 là hai kiểu trung bình trượt ba điểm: trailing lấy điểm đang xét và hai điểm trước, centered lấy một trước, một sau. Dòng 7 và 8: giả sử số của giờ 5 về khác đi, đổi từ 16 thành 40. Dòng 9 và 10 xem giá trị ở giờ 4 có đổi theo không. Kết quả: ngay từ đầu, centered ở giờ 3 đã ra 18,67, vì nó cộng cả số 30 của giờ 4, tức biết trước cú vọt. Khi giờ 5 đổi thành 40, centered ở giờ 4 nhảy từ 20 lên 28, nghĩa là quá khứ bị viết lại; trailing ở giờ 4 vẫn là 18,67. Đó chính là phép thử đổi đuôi, ở quy mô năm số.

## code-b12-kiem-nhan-qua
Giờ biến phép thử đó thành một hàm chạy được cho mọi bộ lọc. Dòng 6: chạy bộ lọc trên chuỗi gốc. Dòng 7 đến 9: cộng 50 vào 10 số cuối rồi chạy lại. Dòng 10: so mọi mốc trước chỗ đổi, NaN đổi thành 0 để phép trừ không ra NaN. Dòng 11 và 12: lệch vượt sai số máy tính thì báo có nhìn tương lai; ngưỡng tính theo độ lớn chuỗi để không báo nhầm vì sai số làm tròn. Dòng 14 kiểm cả mười cấu hình bộ lọc. Kết quả: 6 trên 10 cấu hình nhìn tương lai. Centered 13 đổi quá khứ tới 23,077. Kalman khớp lại trên cả chuỗi đổi 1,134, tức bộ lọc nhân quả vẫn rò rỉ qua tham số. filtfilt làm bẩn ngược tới 274 bước, xa hơn nhiều so với độ rộng cửa sổ mà ta tưởng.

## code-b12-gia-ro-ri
Như mấy slide trước đã nói, feature nhìn tương lai làm sai số đẹp giả; slide này đo đẹp giả bao nhiêu. Dòng 5 và 6: feature là giá trị đã lọc cộng giá trị hiện tại, mục tiêu là điện 6 bước sau, tức 1 giờ tới, lấy bằng shift âm 6. Dòng 7 và 8 chia theo thời gian, 70% đầu học, 30% sau chấm, không xáo trộn. Dòng 9 đến 11 hồi quy tuyến tính bằng bình phương nhỏ nhất với lstsq. Dòng 12 tính MAE trên chuỗi gốc, không phải chuỗi đã lọc. Dòng 14 đến 16 so ba trường hợp: không lọc, centered, trailing. Kết quả: không lọc MAE 46,84 Wh. Centered giảm 27,7%, filtfilt giảm 24,5%, đều là giả. Feature nhân quả chỉ giúp 0,9 đến 5,9%. Đó mới là con số ta được hưởng khi chạy thật.

## ro-ri
Sang buổi 13: rò rỉ tương lai, tức dùng thông tin chưa có lúc ra dự báo. Nó không bao giờ báo lỗi; triệu chứng duy nhất là backtest đẹp còn dùng thật thì tệ. Nên ta phải có máy kiểm. kiem_ro_ri làm ba bước: cắt dữ liệu tại một mốc, tính lại feature, so từng dòng trước mốc. Giống hệt thì chưa thấy rò rỉ; khác là feature đã dùng tương lai. (chỉ vào hình) Bản shift 1 rồi rolling 7 trùng khít; bản rolling center bằng True lệch ngay trước mốc cắt. Ba kiểu rò rỉ qua cả chuỗi hay gặp: scaler tính trên toàn bộ dữ liệu, target encoding tính trên cả chuỗi, nội suy dùng điểm phía sau. Cách sửa chung: chỉ fit trên phần học. Thêm kiểm nhiễu mục tiêu để bắt lag nhỏ hơn tầm dự báo. Và nhớ: kiểm xanh không chứng minh là sạch.

## code-b13-ca-chuoi
Slide này đặt bản sai cạnh bản đúng cho ba kiểu rò rỉ, trên sáu ngày tính tay được. Dòng 4 đến 7: sáu ngày, hai nhóm A và B xen kẽ, ngày 3 bị mất số. Dòng 8 và 9, chuẩn hoá: bản sai dùng trung bình cả sáu ngày, bản đúng dùng shift 1 rồi expanding, tức chỉ trung bình tới hôm qua. Dòng 10 đến 12, trung bình nhóm: bản sai lấy trung bình cả nhóm, bản đúng tính theo nhóm nhưng chỉ trên quá khứ. Dòng 13 và 14, điền chỗ thiếu: nội suy hai phía so với ffill lấy hôm trước. Kết quả: mọi ô z đều dùng trung bình 13,33, trong đó có cả hai ngày cuối. Ngày 1 mang trung bình nhóm A là 12,67, chứa số 20 của ngày 5. Điền hai phía ra 13 vì đã nhìn ngày 4, ffill ra 12.

## code-b13-kiem-ro-ri
Đây là máy tự tìm rò rỉ. Dòng 3: tính feature một lần trên dữ liệu đầy đủ. Dòng 4 và 5: chọn ba mốc cắt ở 50, 70 và 90% chuỗi, vì ở một mốc, rò rỉ có thể không hiện ra. Dòng 7: bỏ phần sau mốc rồi tính lại. Dòng 9: so mọi dòng trước mốc, không bỏ dòng cuối nào, vì rò rỉ hay nằm sát mốc. Dòng 11 đến 15: so từng cột bằng isclose với equal_nan bằng True, nên NaN gặp số vẫn tính là khác; cột nào đổi dù chỉ một dòng là rò rỉ, trả về kèm số dòng đổi. Kết quả: bản làm ẩu, một mốc và bỏ 10 dòng cuối, chỉ bắt 4 cột, để lọt tb_7. Bản đúng bắt đủ 5 cột. Bộ 41 cột đã sửa qua sạch cả hai bài kiểm.

## ngoai-sinh
Kiểu rò rỉ cuối khó thấy nhất: biến ngoại sinh, ví dụ nhiệt độ khi dự báo tải điện. Lúc dự báo, ta chỉ có bản dự báo nhiệt độ, không có nhiệt độ thật. (chỉ vào hình) Backtest dùng nhiệt độ thật hứa giảm sai số 3,85%. Chạy thật bằng dự báo trước 1 ngày còn giảm 3,10%. Chạy bằng dự báo trước 3 ngày thì sai số tăng 2,20%, tệ hơn không dùng nhiệt độ, vì mô hình học tin nhiệt độ quá mức. Kiểm bằng một câu hỏi cho từng biến: lúc ra dự báo, con số này đã có trong tay chưa? Sửa: huấn luyện bằng các bản dự báo đã lưu lại, ghép bằng merge_asof có tolerance. Dự báo trước 3 ngày kém tới mức huấn luyện bằng chính nó vẫn tăng sai số 2,92%, nên bỏ hẳn feature đó.

## code-b13-ngoai-sinh
Dòng 4: mục tiêu là tải điện 24 giờ sau, lấy bằng shift âm 24. Dòng 5: vì mục tiêu đã ở t cộng 24, tải hiện tại chính là lag 24, còn shift 144 là lag 168 tính từ giờ đích. Dòng 6 và 7 đưa ba nguồn nhiệt độ về đúng giờ cần dự báo: nhiệt độ thật, dự báo trước 1 ngày, dự báo trước 3 ngày. Dòng 9 là backtest bằng nhiệt độ thật, con số hứa hẹn. Dòng 10 và 11 là kịch bản hay gặp ngoài đời: học bằng thật, chạy bằng dự báo. Dòng 13 đến 15 ghép bằng merge_asof: direction backward chỉ lấy bản tin cũ hơn, tolerance 3 giờ để quá cũ thì bỏ trống. Kết quả: nhiệt độ thật hứa giảm 3,85% sai số; học bằng thật, chạy bằng dự báo trước 3 ngày thì sai số tăng 2,20%, tệ hơn không dùng nhiệt độ.

## phan-c
Phần C là phần để tra khi làm thật, không phải để học thuộc. Nó gom 24 lỗi hay gặp vào ba bảng, thêm 10 chỗ người mới hay hiểu nhầm, và từ điển Việt – Anh 100 thuật ngữ để các bạn đọc tài liệu gốc. Cách dùng bảng tra: thấy dấu hiệu ở cột trái, chạy phép kiểm ở cột giữa, rồi sửa theo cột phải.

## bang-tra-1
Bảng đầu gom tám lỗi của buổi 3 đến 6: múi giờ, gộp tần suất, điều chỉnh lịch, biến đổi, phân rã. Đọc từ trái sang: dấu hiệu, kiểm bằng gì, sửa thế nào, buổi nào để xem lại. Ba dòng nên nhớ. Dòng "Nóng nhất lúc 20h": giờ nóng nhất trung bình lệch lạ là dấu hiệu các nguồn chưa về cùng UTC. Dòng "Data must be positive": đó là lỗi Box-Cox khi gặp số 0 hay số âm; kiểm y.min, rồi dùng Yeo-Johnson, bản nhận cả số 0 và số âm. Và dòng "Tổng dự báo thấp hơn thật": đổi ngược từ log mà quên hiệu chỉnh bias thì tổng luôn hụt.

## bang-tra-2
Bảng thứ hai là tám lỗi của buổi 7 đến 10: dừng, tương quan, thiếu. Nhấn ba dòng. ADF và KPSS cùng bác bỏ không phải "dừng quanh xu hướng" mà thường do cú sốc hay đổi mức đột ngột; vẽ chuỗi, tìm cú sốc, tách đoạn. Hai chuỗi lạ có r bằng 0,97 thường là tương quan giả do cùng có xu hướng; sai phân rồi tính lại r. Và "min lớn hơn max" nghe vô lý nhưng gặp thật: cột số lưu dạng chữ, kiểm dtypes rồi dùng to_numeric với errors bằng coerce. Dòng cuối, một giá trị chiếm 35%, là mã trá hình ta vừa gặp ở Nội Bài.

## bang-tra-3
Bảng cuối là tám lỗi của buổi 10 đến 15, nhiều dòng các bạn vừa gặp trong phần B. Nhấn ba dòng. "3σ không bắt được gì": thêm một điểm cực lớn để thử, rồi chuyển sang MAD hay Hampel. "Backtest đẹp, dùng thật tệ": chạy kiem_ro_ri nhiều mốc cắt, sửa bằng lag không nhỏ hơn tầm dự báo và chỉ fit trên phần học. Và dòng cuối về gap: gap là số bước bỏ trống giữa mốc cắt và đoạn dự báo khi dữ liệu về trễ. Số liệu về trễ 1 ngày thì gap bằng 24 giờ. Quên gap là backtest đang dùng số liệu mà lúc chạy thật chưa về.

## hay-nham
Mười chỗ này là những câu nghe hợp lý nhưng sai. Cột trái là điều hay nghĩ, cột giữa là thật ra thế nào. Tôi nhấn ba câu. Thứ nhất, "ADF dừng, KPSS không dừng thì là dừng quanh xu hướng": sai, đó là mâu thuẫn, vì hai kiểm định có giả thuyết ngược nhau; thường có cú sốc hoặc đổi mức, hãy vẽ chuỗi. Thứ hai, "CV cao là khó dự báo": chuỗi 10, 30, 10, 30 có CV 0,58 mà rất dễ đoán; độ khó phải đo bằng sai số của baseline. Thứ ba, "chỉ cần thắng seasonal naive": phải thắng cả bốn baseline; trên M4 theo ngày, naive 0,835 và drift 0,810 còn thắng seasonal naive 1,077.

## tu-dien-1
Năm slide từ điển này để tra, không cần đọc hết. Tên tiếng Anh thống nhất theo Phụ lục E, dùng khi các bạn đọc tài liệu gốc như FPP, statsmodels hay Nixtla. Cột cuối cho biết buổi nào dạy từ đó. Slide đầu là nền móng và hiểu dữ liệu, buổi 1 đến 6. Hai cặp nên nhớ vì gặp liên tục trong tài liệu tiếng Anh: gốc dự báo là forecast origin hay cutoff, và tầm dự báo h là forecast horizon. Thêm "sai số ảo" là in-sample error: sai số đo trên chính dữ liệu đã học, luôn đẹp hơn thật.

## tu-dien-2
Slide thứ hai: dừng và làm sạch, buổi 6 đến 11. Khi đọc tài liệu tiếng Anh, để ý ba từ. Stationarity là tính dừng, và unit root test là tên chung của ADF với KPSS. Sentinel value là mã trá hình, như 9,999 km ở Nội Bài; tra bằng từ này sẽ ra tài liệu nguồn giải thích mã. Và MCAR, MAR, MNAR là ba kiểu thiếu: thiếu hoàn toàn ngẫu nhiên, thiếu ngẫu nhiên có điều kiện, thiếu vì chính giá trị của nó.

## tu-dien-3
Slide thứ ba: ngoại lai, bộ lọc, rò rỉ và đánh giá, buổi 11 đến 15. Ba từ đáng nhớ. Masking là che khuất, ngoại lai tự che mình; swamping là mặt ngược lại, gắn cờ oan điểm bình thường. Data leakage hay look-ahead bias là rò rỉ tương lai; tìm bằng cả hai từ vì mỗi cộng đồng quen một cách gọi. Và rolling origin còn được gọi là time series cross-validation, cùng một ý: dự báo cuốn qua nhiều gốc.

## tu-dien-4
Slide thứ tư gom các thuật ngữ nền về xác suất, biểu đồ và biến đổi từ bảng "Từ mới" của buổi 1 đến 6. Hai dòng đáng nhớ. Point và probabilistic forecast: dự báo điểm cho một số, dự báo phân phối cho cả khoảng khả năng. Và effective sample size, cỡ mẫu hiệu dụng: dữ liệu tự tương quan thì số điểm "đáng giá" ít hơn số dòng, nên khoảng tin cậy phải rộng hơn. Còn random seed là thứ ta ghi kèm mọi con số trong khoá để chạy lại ra đúng số.

## tu-dien-5
Slide cuối của từ điển: tương quan, làm sạch và bộ lọc, từ buổi 8 đến 15. Ba dòng đáng nhớ. Confounder, biến gây nhiễu, là biến thứ ba làm hai chuỗi trông như liên quan. Artificial masking là che nhân tạo, cách ta chấm các cách điền ở buổi 10; đừng nhầm với masking của ngoại lai ở buổi 11. Và target encoding, mã hoá target, là nguồn rò rỉ hay gặp nếu tính trên cả chuỗi.

## thu-vien
Bảng cuối cho biết mỗi thư viện lo phần nào, để khi mở code các bạn biết tra ở đâu. pandas và NumPy có mặt ở mọi buổi: pandas lo bảng dữ liệu theo thời gian như resample, shift, rolling, merge_asof; NumPy lo tính toán trên mảng. statsmodels là thư viện thống kê: ACF, ADF, KPSS, STL. SciPy lo Box-Cox, tương quan và bộ lọc tín hiệu buổi 12. ruptures chỉ để tìm điểm gãy. statsforecast và utilsforecast của Nixtla chạy baseline, backtest và chỉ số nhanh cho hàng nghìn chuỗi. Dòng cuối quan trọng: nhiều hàm như du_bao_cuon hay kiem_ro_ri là tự viết, để thấy rõ từng bước trước khi giao cho thư viện.

## ly-thuyet-ham
Slide này là bảng tra ngược, các bạn không cần nhớ ngay. Cột trái là lý thuyết, cột giữa là tên hàm, cột thứ ba là thư viện, cột cuối là buổi dạy. Khi ôn lại một khái niệm, ví dụ Box-Cox, các bạn tìm dòng đó, thấy hàm stats.boxcox của SciPy ở buổi 5, rồi mở slide code của buổi 5 để xem cách dùng. Hai điều đáng để ý: pandas xuất hiện ở hầu hết các dòng, vì phần lớn tiền xử lý là thao tác bảng theo thời gian; và dòng cuối, chỉ số sai số, có cả bản tự viết lẫn utilsforecast, vì chúng ta sẽ thấy ở phần sau rằng hai bản này có thể lệch nhau nếu không đọc quy ước.

## phan-d
Đến đây chúng ta đã làm sạch, biến đổi, tạo feature. Nhưng mọi bước đó chỉ có giá trị nếu dự báo tốt hơn thật, và "tốt hơn thật" phải đo trung thực. Phần D đi qua sáu việc: chẩn đoán phần dư, chọn chỉ số, chia dữ liệu theo thời gian, backtest rolling origin, tách ba đoạn dữ liệu, và kiểm định Diebold–Mariano để biết chênh lệch là thật hay may.

## phan-du
Câu hỏi đầu tiên: mô hình đã khai thác hết quy luật trong dữ liệu chưa? Phần dư trả lời câu đó. Phần dư là thực tế trừ giá trị khớp trên phần học; còn sai số dự báo đo trên kỳ chấm, phần mô hình chưa thấy. Hai thứ này khác nhau, và chỉ số chính xác luôn tính trên kỳ chấm. (chỉ vào hình) Ô trái là phần dư theo ngày, có một cú rơi rất lớn. Ô giữa là ACF theo trễ: các cột đầu cao vượt hẳn hai đường đứt, trễ 1 tới 0,86. Ô phải là phân phối, lệch khỏi hình chuông. Ljung-Box cho p gần 0, tức còn quy luật bị bỏ sót. Nghĩa là seasonal naive chưa dùng hết thông tin, mô hình tốt hơn có chỗ để thắng, và khoảng dự báo của baseline này không đáng tin.

## code-b14-phan-du
Giờ chúng ta kiểm bằng code. Dòng 4 đến 5 tính phần dư seasonal naive: mỗi ngày trừ ngày cùng thứ tuần trước. Dòng 8 đến 10 tính tự tương quan của phần dư ở 14 trễ, bằng np.dot: nhân từng cặp rồi cộng. Dòng 11 đến 12 gộp 14 trễ đó thành một con số Q, cộng bình phương các tự tương quan có trọng số. Dòng 13 đổi Q thành p bằng phân phối chi bình phương: p là xác suất gặp Q lớn cỡ này nếu phần dư chỉ là nhiễu. Dòng 16 dùng Jarque–Bera để hỏi phần dư có gần hình chuông không. Kết quả trên 1.000 chuỗi M4: 99,8% còn tự tương quan, 92,5% không hình chuông, và 46,4% có phương sai đổi hơn 2 lần. Tức là gần như chuỗi nào cũng còn chỗ để cải thiện.

## chi-so
Chọn chỉ số nghe như việc kỹ thuật, nhưng thật ra là chọn luôn dự báo. Ba chỉ số cơ bản, sai số bằng thực tế trừ dự báo. MAE là trung bình độ lớn sai số. RMSE bình phương trước khi lấy trung bình rồi căn lại, nên phạt nặng sai số lớn. ME giữ dấu: dương nghĩa là dự báo thấp có hệ thống. (chỉ vào hình) Ô trái là 20.000 số lệch phải như doanh số. Ô phải thử từng hằng số dự báo và xem mỗi chỉ số đáy ở đâu: MAE đáy ở trung vị 20,0, RMSE đáy ở trung bình 30,1, MAPE còn đáy thấp hơn cả hai, ở 9,1. Vì vậy hãy chọn chỉ số theo cái giá thật của sai lệch. Một lưu ý: utilsforecast tính bias là dự báo trừ thực tế, ngược dấu với khoá.

## code-b14-mae-rmse
Dòng 3 đến 8 là ba chỉ số, mỗi cái một dòng, sai số là thực tế trừ dự báo. Dòng 10 đến 11 là bảng năm ngày để các bạn tính tay đối chiếu. Dòng 12 sinh 20.000 số lệch phải bằng lognormal, seed 0 để chạy lại ra y hệt. Dòng 13 đến 15 là thí nghiệm chính: chia khoảng giá trị thành 2.000 hằng số c, với mỗi c tính MAE và RMSE nếu ta luôn dự báo c. Dòng 16 dùng np.argmin tìm c làm mỗi chỉ số nhỏ nhất. Kết quả: năm ngày cho MAE 1,6, RMSE 2,10, ME 0,8. Trên số lệch phải, MAE nhỏ nhất ở 20,0, đúng trung vị; RMSE nhỏ nhất ở 30,1, đúng trung bình. Cùng dữ liệu, hai chỉ số đòi hai con số dự báo khác nhau.

## phan-tram
Muốn so sai số giữa các chuỗi khác đơn vị, người ta hay dùng phần trăm, và MAPE là lựa chọn phổ biến. MAPE chia sai số cho thực tế nên có hai điểm yếu. Thực tế bằng 0 thì chia cho 0, ra vô hạn. Và nó lệch không đối xứng: thật 100, dự báo 150 ra 50%, nhưng thật 150, dự báo 100 chỉ ra 33,3%. (chỉ vào hình) Mỗi ô là hạng của một baseline theo một chỉ số, ô trái là M4, ô phải là bán lẻ có 75% ngày bằng 0. M4 gần như cùng thứ hạng ở mọi chỉ số; bán lẻ thì hạng nhất đổi theo chỉ số, còn cột MAPE toàn gạch vì không tính được. Thay thế là WAPE, lấy tổng chia tổng, và MASE, chia cho sai số của baseline. Ngay sau slide code, một slide riêng nói kỹ MASE.

## code-b14-phan-tram
Ba chỉ số phần trăm, mỗi hàm xử lý số 0 một kiểu. Dòng 3 đến 6 là MAPE: chia từng sai số cho từng thực tế. Dòng 5 có np.errstate để tắt cảnh báo chia cho 0, nhưng chúng ta cố ý để kết quả vô hạn hiện ra, không giấu đi. Dòng 8 đến 12 là sMAPE kiểu M4: chia cho tổng độ lớn thực tế và dự báo, nhân 200, nên thang đi từ 0 tới 200; ô nào mẫu bằng 0 thì np.where cho 0. Dòng 14 đến 16 là WAPE: tổng sai số chia tổng thực tế, chỉ hỏng khi cả chuỗi bằng 0. Kết quả trên bảng năm ngày: MAPE 12,8%, sMAPE 13,6, WAPE 13,3%. Thêm một ngày thực tế bằng 0 thì MAPE thành vô hạn ngay, và trên 300 mã bán lẻ, MAPE không tính được.

## code-b14-mase
Như slide trước, MASE chia sai số cho sai số của seasonal naive trên phần học. Dòng 4 là chỗ quan trọng nhất: sai số seasonal naive tính trên phần học, không phải trên kỳ chấm. Dòng 5 đến 7 lấy trung bình trị tuyệt đối cho MASE, hoặc trung bình bình phương cho RMSSE. Dòng 9 đến 11 chia MAE kỳ chấm cho mẫu số đó. Dòng 11 còn một chi tiết: mẫu số bằng 0, ví dụ chuỗi phẳng, thì trả NaN chứ không trả 0, để khỏi lẫn với dự báo hoàn hảo. Dòng 13 đến 15 là RMSSE, làm y hệt với bình phương rồi căn. Ví dụ tay: MASE bằng 1,6 chia 1,5, khoảng 1,07; RMSSE khoảng 1,33. Nếu lấy nhầm mẫu số trên đoạn chấm như code đầu buổi, MASE của naive trên M4 ra 0,972 thay vì 0,835.

## code-b14-doi-hang
Có nhiều chuỗi thì phải gộp, và gộp là chỗ dễ giấu lỗi. Dòng 3 đến 5 bỏ các ô vô hạn hay NaN, nhưng đếm số ô đó để báo ra. Dòng 6 gộp bằng cả trung vị và trung bình: trung vị không bị vài chuỗi cực đoan kéo, trung bình thì bị. Dòng 8 đến 12 xếp hạng mô hình theo từng chỉ số bằng rank; riêng ME xếp theo trị tuyệt đối vì ME âm hay dương đều là lệch. Dòng 15 đến 16 đối chiếu với utilsforecast: thư viện trả tỷ lệ 0 tới 1, phải nhân 200 mới về thang M4. Kết quả trên 300 mã bán lẻ: hạng nhất đổi theo chỉ số, naive thắng theo MAE, seasonal naive thắng theo sMAPE. Còn sMAPE tự viết 3,59 so với utilsforecast 0,0179, lệch 200 lần chỉ vì quy ước.

## chia-ngau-nhien
Có chỉ số rồi, câu hỏi tiếp theo là chấm trên đoạn nào. Học máy thông thường chia ngẫu nhiên. Với chuỗi thời gian, đó là nhìn trộm tương lai. (chỉ vào hình) Trục ngang là thời gian, xanh là điểm học, cam là điểm kiểm. Hàng trên là chia ngẫu nhiên: chấm cam nằm xen giữa chấm xanh, tức mô hình được học cả hôm qua lẫn ngày mai của điểm đang kiểm. Hai hàng dưới là hai cách đúng: hold-out kiểm một lần trên đoạn cuối; rolling origin kiểm nhiều lần, lần nào cũng chỉ học quá khứ. Triệu chứng của chia ngẫu nhiên là sai số lúc kiểm rất đẹp, chạy thật thì tệ, và ta dễ chọn nhầm mô hình giỏi học thuộc. Cách kiểm đơn giản: nhìn xem điểm kiểm có xen giữa điểm học không.

## code-b15-kfold
Giờ đo bằng số xem chia ngẫu nhiên hứa sai bao nhiêu. Dòng 5 đặt mốc 1 tháng 10 năm 2024: ba tháng cuối là hold-out, không đụng tới. Dòng 6 đến 8 dựng feature lag từ 24 giờ trở lên cộng lịch, và chỉ lấy phần trước mốc để học. Dòng 10 đến 13 chạy KFold 5 phần có xáo trộn, ước lượng sai số theo kiểu học máy thông thường. Dòng 14 đến 15 làm cách trung thực: học một lần trên quá khứ, chấm trên ba tháng sau. Kết quả với rừng ngẫu nhiên: K-fold hứa 1.639 MW, hold-out thật 2.129 MW, tức K-fold hứa thấp hơn thật 23,0%. Hồi quy tuyến tính cũng lệch, nhưng ít hơn, 11,8%, vì mô hình tuyến tính khó học thuộc hơn.

## kfold
(chỉ vào hình) Trục ngang là hai mô hình, trục dọc là MAE tính bằng MW. Cột cam là K-fold xáo trộn, cột xanh là rolling origin, cột đen là hold-out thật. Nhìn vào độ cao cột cam và cột xanh so với cột đen. Với rừng ngẫu nhiên, K-fold hứa thấp hơn thật 23%, còn rolling origin chỉ lệch 9%. Nhưng đừng coi rolling origin là tiên tri: nó chỉ đúng khi giai đoạn backtest giống tương lai; với hồi quy tuyến tính, cả hai cách đều hứa thấp hơn thật 12 đến 16%. K-fold cũng không phải lúc nào cũng sai: Bergmeir, Hyndman và Koo năm 2018 chỉ ra rằng nếu mô hình chỉ dùng lag và phần dư không còn tự tương quan thì K-fold dùng được. Mô hình càng giỏi nhớ thì K-fold càng lạc quan.

## rolling-origin
Rolling origin là backtest như chạy thật. Ta đặt nhiều mốc cắt, gọi là cutoff; ở mỗi cutoff học trên quá khứ rồi dự báo đoạn ngay sau. (chỉ vào ô trái) Trục ngang là cutoff trong tháng 9 năm 2024, trục dọc là MAE của từng cửa sổ 24 giờ. Đường xanh của rừng ngẫu nhiên lên xuống rất mạnh: mỗi cửa sổ là một lần may rủi, nên phải báo cả phân bố sai số chứ không chỉ trung bình. (chỉ vào ô phải) Trục ngang là bước h từ 1 tới 48 giờ; sai số nhảy lên ở bước 25. Tầm thật là 24 giờ thì chỉ nhìn 24 giờ đầu. Cách tính cutoff: cutoff cuối bằng n trừ 1 trừ gap trừ h. Với 30 mốc, h bằng 4, gap bằng 2 thì cutoff cuối là 23, lùi đều 4 bước được 19 và 15.

## code-b15-rolling-origin
Chúng ta tự viết bộ backtest để thấy từng bước. Dòng 6 tính cutoff của cửa sổ cuối sao cho cửa sổ đó kết thúc đúng ở mốc cuối. Dòng 7 đến 8 lùi đều từng buoc để ra các cutoff trước, và chừa gap bước trống sau mỗi cutoff. Dòng 12 là dòng chống rò rỉ: hàm dự báo chỉ nhận các dòng tới cutoff, không thấy đoạn kiểm. Dòng 13 đến 14 dự báo đúng các mốc của đoạn kiểm, và dòng 15 dùng merge ghép dự báo với thực tế để chấm. statsforecast có hàm cross_validation làm cùng việc nhưng không có gap. Kết quả trên tải ERCOT, 28 cửa sổ 24 giờ: rừng ngẫu nhiên 1.944 MW so với hold-out 2.129 MW, lệch 8,7%. Seasonal naive tự viết khớp statsforecast, chênh 0,0, nên ta tin bộ tự viết đúng.

## cua-so
Rolling origin có bốn lựa chọn, và cả bốn phải khớp với cách mô hình chạy thật. (chỉ vào hình) Mỗi hàng là một cutoff: phần xám là dữ liệu được học, dài dần qua từng hàng, tức là expanding; ô xanh là đoạn được dự báo và chấm. Expanding học toàn bộ quá khứ, dùng khi quá khứ xa vẫn giống hiện tại. Sliding chỉ học L bước gần nhất, ví dụ 90 ngày, dùng khi quá khứ xa đã khác. Gap là số bước bỏ trống bằng đúng độ trễ công bố dữ liệu: số liệu điện về trễ 1 ngày thì gap bằng 24 giờ; quên gap là cho mô hình thấy số liệu chưa về. Refit là học lại mỗi cửa sổ; mô hình nặng thì refit mỗi vài cửa sổ.

## code-b15-theo-cua-so
Một con số MAE gộp che mất độ dao động, nên ta tách ra. Dòng 7 đến 8 chạy backtest 28 cửa sổ, mỗi cửa sổ 24 giờ, cho rừng ngẫu nhiên và seasonal naive trên cùng các cửa sổ. Dòng 9 đến 11 dùng groupby theo cutoff để tính một MAE cho mỗi cửa sổ, mỗi mô hình. Dòng 12 gọi describe để tóm từ nhỏ nhất tới lớn nhất. Dòng 14 đến 15 gộp sai số theo buoc_h, tức bước thứ mấy sau cutoff. Kết quả: MAE một ngày của rừng ngẫu nhiên đi từ 583 tới 4.328 MW, gấp bảy lần. Nếu hold-out chỉ rơi vào một ngày, các bạn có thể báo bất kỳ con số nào trong khoảng đó. Trên M4, seasonal naive 24 giờ nhảy lên từ bước 25, vì ngày thứ hai nó lặp lại một ngày đã cũ hơn.

## ba-doan
Hãy nghĩ như đi thi: đề luyện để tune tham số, đề thi thử để chọn mô hình, đề thi thật để báo cáo, và chỉ mở một lần. Học sinh luyện đúng đề thi thật thì điểm cao mà không giỏi hơn. (chỉ vào hình) Trục dọc là MASE trung vị của 414 chuỗi M4 theo giờ, vạch đen là 1. Cột cam là tune, chọn và báo cáo cùng một đoạn: 0,775. Cột xanh là ba đoạn riêng: 1,039. Cùng quy trình, con số cam lạc quan 25%. Lý do: cái thắng trên một đoạn được hưởng cả phần may của đoạn đó. Chọn trên tập kiểm cũng là rò rỉ; đã mở hold-out rồi quay lại chỉnh mô hình thì cần một hold-out mới.

## code-b15-ba-tap
Code này tách ba đoạn 48 giờ cuối của mỗi chuỗi. Dòng 3 tạo lưới trọng số w từ 0 tới 1, bước 0,1, tức 11 giá trị. Dòng 9 chia ba đoạn: T để tune, A để chọn, B để báo cáo. Dòng 10 chọn w cho MASE thấp nhất trên đoạn T. Dòng 11 đến 12 chấm sáu phương pháp đơn giản trên đoạn A và chọn cái tốt nhất. Dòng 13 đến 15 chỉ báo MASE của phương pháp đã chọn trên đoạn B, đoạn chưa dùng cho việc gì. Hàm _cham là hàm tự viết tính MASE trên một đoạn 48 giờ. Kết quả trên 414 chuỗi M4 theo giờ: làm tất cả trên đoạn B cho MASE trung vị 0,775; ba đoạn riêng cho 1,039. Con số trung thực tệ hơn 25%.

## dm
Hai mô hình chênh nhau vài phần trăm: thật, hay chỉ may? Kiểm định Diebold–Mariano lấy chênh lệch sai số trung bình chia cho sai số chuẩn của chính chênh lệch đó. p dưới 0,05 thì chênh có thật; từ 0,05 trở lên thì chưa có bằng chứng. (chỉ vào hình) Ô trái là chênh sai số trung bình từng ngày của 92 ngày hold-out: mô hình trộn thắng 53 ngày, thua nhiều ngày khác. Ô phải là ACF của chênh lệch từng giờ: trễ 1 tới 0,91 và còn vượt đường đứt tới khoảng trễ 18. Đó là chỗ cần cẩn thận: bỏ qua tự tương quan này thì p nhỏ giả tạo. Phải cộng tự hiệp phương sai tới trễ h trừ 1 và dùng bản hiệu chỉnh HLN. Thêm nữa, so 20 cặp mô hình thì trung bình khoảng một cặp p dưới 0,05 chỉ do may.

## doc-kiem-dinh
Qua 15 buổi chúng ta gặp bảy kiểm định. Tin vui là cả bảy đọc cùng một cách.

(chỉ vào bốn ô trên) Đặt H0, giả định ban đầu, thường là “không có gì đặc biệt”. Tính một con số từ dữ liệu. Hỏi: nếu H0 đúng, gặp con số lệch cỡ này hoặc hơn hiếm tới đâu; đó là p. p nhỏ hơn 0,05 thì bác bỏ H0; p lớn hơn thì chỉ là chưa đủ bằng chứng, không có nghĩa H0 đúng.

Bảng dưới chỉ cần nhớ cột H0. Hoán vị: hai nhóm như nhau. Ljung-Box: phần dư là nhiễu trắng, nên p nhỏ là còn quy luật. Granger: quá khứ x không giúp dự báo y. Jarque–Bera: phần dư hình chuông. Diebold–Mariano: hai mô hình chính xác như nhau.

(chỉ vào hai dòng cam) Hai dòng cam là chỗ hay nhầm nhất. ADF đặt H0 là không dừng, nên p nhỏ là dừng. KPSS đặt ngược lại, H0 là dừng, nên p nhỏ là không dừng. Luôn đọc H0 trước khi đọc p.

## code-b15-dm
Dòng 5 tính chênh độ lớn sai số của hai dự báo ở từng giờ. Dòng 8 đến 9 là phần mấu chốt: tính tự hiệp phương sai của chênh lệch ở các trễ từ 0 tới h trừ 1 rồi cộng vào phương sai, vì các giờ gần nhau dùng chung thông tin. Dòng 10 đến 11 là phòng hờ: phương sai ra âm thì lùi về h bằng 1. Dòng 12 lấy chênh trung bình chia sai số chuẩn. Dòng 13 đến 14 là bản ngây thơ, so với hình chuông chuẩn. Dòng 15 đến 16 là bản HLN: nhân hệ số sửa mẫu nhỏ rồi so với phân phối t. Kết quả, mô hình trộn so với seasonal naive trên 2.215 giờ: bản bỏ tự tương quan cho p bằng 0,0000012, trông rất chắc chắn; bản HLN với h bằng 24 cho p bằng 0,16, tức chưa có bằng chứng.

## phan-e
Phần E ghép mọi thứ từ đầu khoá thành một quy trình. Chỉ cần một câu hỏi để xếp từng bước vào đúng chỗ: bước này có học gì từ dữ liệu không? Nếu có, nó phải làm lại ở mỗi cutoff, chỉ trên dữ liệu trước cutoff.

## quy-trinh
Sơ đồ có ba tầng, đọc từ trên xuống; số nhỏ dưới mỗi ô là buổi dạy bước đó. Tầng 1 làm một lần trên toàn bộ dữ liệu, vì các bước này không học tham số nào: nạp và ép kiểu số, đưa về UTC, dựng lưới đủ, đổi mã trá hình thành NaN, nhìn bộ biểu đồ, ghi nhật ký sự kiện, điều chỉnh lịch và lạm phát. Tầng 2, trong khung viền đứt, là nơi rò rỉ hay xảy ra nhất: điền nhân quả, ngưỡng Hampel, λ của Box-Cox, bộ lọc nhân quả, feature với lag từ h trở lên, scaler. Các bước này học từ dữ liệu, nên phải làm lại ở mỗi cutoff; làm trên toàn bộ rồi mới backtest là để tương lai rò vào quá khứ. Tầng 3 là kiểm: rolling origin có gap, chấm MASE hoặc WAPE trên chuỗi gốc so với seasonal naive, và chạy kiem_ro_ri.

## nguyen-tac
Nếu chỉ nhớ ba điều cho mọi bước tiền xử lý thì là ba điều này. Thứ nhất, chỉ dùng thông tin có trước cutoff: áp cho feature, giá trị điền, tham số biến đổi, và cả biến ngoại sinh, nghĩa là dùng bản dự báo đã lưu chứ không dùng số thật. Đây là lỗi gặp lại ở nhiều buổi nhất. Thứ hai, giữ dữ liệu gốc, gắn cờ thay vì xoá, vì xoá làm thủng lưới thời gian và mất dấu vết; cột cờ cho biết chỗ nào đã sửa. Thứ ba, phải thắng các baseline trên backtest, luôn có seasonal naive. Bước tiền xử lý nào không làm sai số trung thực tốt lên thì bỏ, dù nó trông hợp lý đến đâu.

## phan-f
Phần cuối nói về dữ liệu dùng trong khoá: dữ liệu thật, bẩn thật, có giấy phép mở đã xác minh. Sau đó là bảng tra mỗi buổi nằm ở slide nào để các bạn ôn, và những phần tiền xử lý các buổi sau sẽ dạy thêm.

## du-lieu
Mười bốn bộ dữ liệu này không được chọn vì sạch, mà vì mỗi bộ dạy một kiểu bẩn. Mỗi thẻ ghi tên bộ, nội dung, dòng đỏ là kiểu bẩn, dòng dưới cùng là tần suất, giấy phép và buổi dùng. Vài ví dụ: điện hộ gia đình ghi thiếu bằng dấu hỏi; taxi New York có giờ naive quanh ngày đổi giờ; Census có ô "(S)" và đổi định nghĩa; EIA-930 đổi cột giữa năm; trạm Nội Bài dùng mã 9,999 và cờ chất lượng; Wikipedia có đỉnh Tết theo lịch âm; Eurostat gãy do COVID; bán lẻ trực tuyến nhiều số 0. Mọi bộ đều tải kèm kiểm sha256, tức dấu vân tay của tệp. Khoá không dùng FRED vì điều khoản cấm dùng cho machine learning; chuỗi kinh tế lấy từ cơ quan gốc.

## tra-theo-buoi
Bảng này dùng khi các bạn muốn ôn một buổi cụ thể. Mỗi dòng là một buổi, bên cạnh là các slide tóm buổi đó. Script sinh slide có kiểm để mọi mục lý thuyết 4.x của buổi 1 đến 15 đều có ít nhất một slide, nên không buổi nào bị bỏ sót. Cách ôn gợi ý: mở các slide của buổi đó, đọc mục tương ứng trong bài đọc kèm, rồi mới quay về tài liệu gốc của buổi khi cần chi tiết.

## phia-truoc
Buổi 1 đến 15 cho chúng ta quy trình chung. Tiền xử lý chưa dừng ở đây; mỗi loại bài toán sau này thêm phần riêng. (chỉ vào đường thời gian) Số trong vòng tròn là buổi dạy. Buổi 19 xử lý chuỗi thưa nhiều số 0, nối tiếp bộ bán lẻ các bạn đã thấy. Buổi 20 là dữ liệu khác tần suất và số liệu bị sửa lại. Buổi 22 biến chuỗi thành bảng hồi quy, buổi 24 là chuỗi mới chưa có lịch sử, buổi 28 là gộp theo cấp bậc, buổi 29 là cửa sổ cho deep learning. Hai mốc cuối, buổi 41 và 43, đưa lên production: pipeline point-in-time chạy lại ra đúng kết quả, và giám sát drift khi dữ liệu mới đổi.

## tong-ket
Năm điều mang về. Nhìn trước, xử lý sau. NaN là không biết, 0 là đo được và bằng không: gắn cờ, đừng xoá. Mọi mốc thời gian về UTC, trên lưới đầy đủ. Chỉ dùng thông tin có trước cutoff. Và mọi mô hình, mọi bước tiền xử lý phải thắng các baseline, luôn có seasonal naive, trên rolling origin. Nếu một bước không qua được bài kiểm cuối cùng này, nó không đáng giữ. Cảm ơn các bạn.

## lam-tron
Ba cách làm hình dễ nhìn hay dùng nhất là gộp tần suất, làm trơn và thang log. Slide này là làm trơn.

Trung bình trượt có tâm thay mỗi điểm bằng trung bình của nó với các điểm hai bên, trong một cửa sổ w điểm, như công thức trên dải. Ví dụ bảy ngày 50, 52, 48, 2, 51, 49, 50: ngày thứ tư gần như trống. Cửa sổ 3 ngày biến nó thành 33,7; cửa sổ 7 ngày thành 43,1.

(chỉ vào mũi tên) Đây là ngày bão Sandy, tệp chỉ còn một giờ với 22 lượt. Vậy mà đường cam 7 ngày ở ngày đó vẫn là 4.632 lượt, chỉ lõm nhẹ. Ai chỉ nhìn đường làm trơn sẽ không biết có một ngày dữ liệu gần như trống.

Nên nhớ một thói quen: vẽ đường làm trơn đè lên dữ liệu gốc, đừng thay nó.

## thang-log
Cùng dữ liệu, đổi thang dọc là đổi câu trả lời. Trên thang log, mỗi điểm đặt ở độ cao log cơ số 10 của nó. Gấp đôi thì cao thêm đúng 0,301, dù từ 100 lên 200 hay từ 200 lên 400. Nên hai đoạn dốc như nhau nghĩa là tăng cùng một phần trăm.

Nhìn hai ô. Ô trái thang thường: tháng 4 sang tháng 5 tăng nhiều lượt nhất, thêm 40.951 lượt. Ô phải thang log: đoạn dốc nhất lại là tháng 3 sang tháng 4, tăng 48,1%.

Không ô nào sai; hai ô trả lời hai câu hỏi khác nhau. Cần thêm bao nhiêu xe thì đọc thang thường. Tăng nhanh cỡ nào thì đọc thang log.

## dieu-chinh
Buổi 5 bắt đầu bằng câu hỏi: doanh số tăng vì người ta mua nhiều hơn thật, hay vì những lý do đã biết trước?

Có ba lý do hay gặp, mỗi lý do một phép chia. Tháng dài hơn thì chia cho số ngày. Giá cao hơn thì chia cho CPI rồi nhân CPI năm gốc. Người đông hơn thì chia thêm cho dân số. Ví dụ doanh thu 100 lên 150, CPI 100 lên 125, dân số 10 lên 12: giá thực chỉ 120, tăng 20% chứ không phải 50%; chia đầu người thì 10 vẫn là 10, mỗi người mua y như cũ.

(chỉ vào hình) Bán lẻ Mỹ đầu 2023: theo tổng tháng, tháng 2 giảm; chia số ngày thì tháng 2 tăng. Dấu của kết luận đảo ngược. Vì vậy mọi con số tăng trưởng phải nói rõ đã bỏ những gì.

## log
Slide trước bỏ phần tăng do lịch, giá và dân số. Còn một vấn đề nữa: năm bán nhiều thì chênh lệch giữa tháng đông và tháng vắng cũng lớn, trong khi nhiều mô hình giả định dao động to như nhau ở mọi mức.

Log giải quyết bằng cách biến nhân thành cộng. Cửa hàng nhỏ tăng 20%, từ 100 lên 120; siêu thị cũng tăng 20%, từ 1.000 lên 1.200. Trên thang gốc, một bên chênh 20, một bên chênh 200. Trên thang log, cả hai đều cao thêm 0,182. (chỉ vào hình) Hai đoạn rộng khác hẳn nhau theo chiều ngang nhưng cao bằng nhau theo chiều dọc.

Log chỉ dùng cho số dương, và hợp nhất khi dao động tỷ lệ đúng với mức. Bán lẻ Mỹ thì mức gấp 3,1 lần mà dao động chỉ gấp 2,4, nên log ép quá tay. Slide sau là cái núm vặn ở giữa: Box-Cox.

## robust
Phân rã có một điểm yếu: một giờ số liệu hỏng có thể làm méo cả xu hướng và mùa vụ.

Robust làm phân rã hai lượt. Lượt đầu tính phần dư. Lượt sau, điểm nào có phần dư quá lớn so với 6 lần phần dư điển hình thì bị bớt tin, trọng số giảm tới 0. Ví dụ phần dư 1, âm 2, 1, 20, âm 1: mốc là 6, điểm 20 vượt mốc nên trọng số 0; điểm âm 2 còn trọng số 0,79. Điểm không bị xoá mà nằm lại trong phần dư.

(chỉ vào hàng mùa vụ) Dữ liệu PJM có một giờ báo tụt còn 56.260 MW. Không robust, các vết lõm cam xuất hiện mỗi trưa: mùa vụ lúc 17 giờ UTC của ngày 20/11, ngày không có lỗi, là âm 4.051 MW. Robust thì là cộng 2.117 MW, và lỗi nằm gọn trong phần dư.

Nhưng robust không tách được đợt nắng nóng kéo dài nhiều ngày; việc đó cần thêm biến nhiệt độ.

## cach-dien
Trước khi chấm cách điền, cần biết mỗi cách làm gì. Có bảy cách, và ba câu hỏi chọn giữa chúng: lỗ dài hay ngắn, chuỗi có nhịp ngày không, và cách điền có dùng số tương lai không.

(chỉ vào hình) Sáu giờ liền, hai ô giữa bị thiếu, giá trị thật là 26 và 28, đúng lúc nhiệt độ lên đỉnh. ffill giữ số gần nhất nên điền 23, 23, sai nhiều nhất. Tuyến tính nối 23 với 27 theo công thức trên dải, ra 24,33 và 25,67. Mùa vụ lấy cùng giờ hôm qua, ra 25 và 27. Trạm hàng xóm cộng 1 độ ra đúng 26 và 28, vì nó mang theo hình dạng của đoạn bị mất.

Tóm lại: lỗ ngắn thì ffill hay tuyến tính đều ổn; lỗ dài thì cần mùa vụ hoặc hàng xóm. Và nhớ tuyến tính, spline, Kalman smoother đều dùng số ở phía sau lỗ.

## khu-nhieu
Buổi 12 là khử nhiễu. Chuỗi bằng tín hiệu cộng nhiễu, và bộ lọc cố ước lượng phần tín hiệu. Câu hỏi đầu tiên với mọi bộ lọc: đầu ra tại thời điểm t có dùng số sau t không?

(chỉ vào hình) Năm giờ điện 10, 12, 14, 30, 16. Đứng ở giờ 3. Kiểu trailing chỉ lấy ba giờ đã qua: 10, 12, 14, ra 12. Kiểu centered lấy giờ trước, giờ này và giờ sau: 12, 14, 30, ra 18,67. Con số 30 là của giờ 4, lúc đứng ở giờ 3 chưa ai biết.

Nên centered chỉ để mô tả, vẽ báo cáo, tách xu hướng; không bao giờ làm feature dự báo. Trailing dùng được, nhưng phải trả giá bằng độ trễ: trung bình 13 điểm có đỉnh đến sau tín hiệu 6 bước.

## ewma
Có cách làm trơn nhân quả nào trễ ít hơn không? Có: EWMA, trung bình trượt hàm mũ.

Công thức rất gọn: đầu ra mới bằng alpha nhân số mới, cộng một trừ alpha nhân đầu ra trước. Với alpha 0,5 và chuỗi 10, 20, 10, ta được 10, rồi 15, rồi 12,5. Mỗi bước chỉ cần nhớ một con số.

(chỉ vào hình) Trục ngang là số bước lùi về quá khứ, trục dọc là trọng số. Trung bình 13 điểm chia đều rồi cắt hẳn; EWMA dồn phần lớn vào vài điểm mới nhất. Vì vậy cùng độ trơn mà trễ ít hơn: đo được trung bình 13 điểm trễ 6 bước, EWMA alpha 0,15 trễ 4.

Một lưu ý khi dùng pandas: alpha, span và com là ba cách khai cùng một tham số. span bằng 9 là alpha 0,2, còn com bằng 9 là alpha 0,1. Luôn ghi rõ đã khai cái nào.

## muc-tieu-lam-tron
Làm trơn feature bằng bộ lọc nhân quả thì được. Còn làm trơn chính mục tiêu thì sao?

Cùng một mô hình dự báo điện một giờ tới. Chấm trên điện thật, MAE là 46,84 Wh. Chấm trên điện đã làm trơn bằng trung bình centered 13 điểm, MAE còn 35,78, giảm 23,6%. Mô hình không đổi một chút nào; nó chỉ được chấm trên một đề dễ hơn và không có thật, vì không ai trả tiền điện đã làm trơn.

(chỉ vào hình) Đường làm trơn cắt mất các đỉnh nhọn, đúng những chỗ mô hình sai nhiều nhất.

Cách sửa: luôn chấm trên chuỗi gốc. Nếu người dùng thật sự cần trung bình 3 giờ tới, thì định nghĩa lại mục tiêu thành đúng đại lượng đó và ghi rõ trong báo cáo.

## mase
Chỉ số phần trăm vỡ khi có số 0. MASE tránh việc chia cho thực tế.

MASE lấy MAE trên kỳ chấm, chia cho MAE của seasonal naive trên phần học. Kết quả đọc là: mô hình sai bằng bao nhiêu lần mức sai quen thuộc của baseline trên chuỗi này. Ví dụ phần học 9, 11, 10, 12, 13: bước nhảy trung bình 1,5. MAE kỳ chấm 1,6 thì MASE là 1,07. RMSSE làm tương tự với bình phương, dùng ở cuộc thi M5.

Có hai chỗ hay nhầm. Một, mẫu số phải lấy trên phần học; lấy trên kỳ chấm là dùng thông tin tương lai, và MASE của naive trên M4 ra 0,972 thay vì 0,835. Hai, MASE dưới 1 chưa chắc thắng seasonal naive trên kỳ chấm, vì kỳ chấm thường khó hơn. Muốn biết thì chạy baseline trên cùng kỳ.

(chỉ vào hình buổi 9) Vì mẫu số lớn lên theo độ khó của chuỗi, MASE của seasonal naive nằm ngang quanh 1. MASE dùng để so mô hình, không để đo độ khó.

## bang-chi-so
Tám chỉ số của buổi 14 trong một bảng, để tra lại khi phải chọn.

Ba dòng đầu cùng đơn vị với dữ liệu. ME giữ dấu nên đo độ chệch, không đo độ chính xác: dương là dự báo thấp hơn thực tế. MAE ưa trung vị. RMSE ưa trung bình và phạt nặng sai số lớn.

Ba dòng giữa là phần trăm. MAPE dễ đọc nhưng hỏng khi thực tế bằng 0 và kéo dự báo xuống thấp. sMAPE là chỉ số của cuộc thi M4, thang 0 tới 200, tên là đối xứng nhưng thật ra vẫn không đối xứng. WAPE chia tổng cho tổng nên sống được với số 0.

Hai dòng cuối chia cho sai số của seasonal naive trên phần học, nên so được giữa các chuỗi. Phần học lặp hoàn hảo thì mẫu số bằng 0 và hàm phải trả NaN.

(dừng) Chọn chỉ số theo quyết định trước khi xem kết quả, vì đổi chỉ số là đổi hạng.

## spearman
Slide trước nói Pearson đo đường thẳng. Nhưng nhiều khi ta chỉ cần biết: x tăng thì y có tăng không, dù tăng theo đường cong.

Spearman làm đúng việc đó. Nó xếp hạng từng biến, số nhỏ nhất là hạng 1, rồi tính Pearson trên các hạng. (chỉ vào hình trái) y bằng x bình phương, x từ 1 tới 5: y luôn tăng nhưng cong. Pearson chỉ 0,981, còn Spearman bằng đúng 1, vì hai dãy hạng trùng nhau.

(chỉ vào hình phải) Nhưng với hình chữ U, x từ âm 2 tới 2, cả Pearson lẫn Spearman đều bằng 0, dù y hoàn toàn theo x. Nên Spearman giúp với đường cong cùng chiều, còn chữ U thì cần cách khác, lát nữa chúng ta sẽ gặp. Kendall cũng dùng hạng, đếm số cặp cùng chiều, và ít bị vài điểm lạ kéo đi khi mẫu nhỏ.

## durbin-watson
CPI và dân số Mỹ có R bình phương 0,95, hệ số t là 88,6. Nhìn con số thì tưởng hai thứ liên quan cực mạnh. Durbin–Watson giúp kiểm lại.

Cách làm: hồi quy chuỗi này theo chuỗi kia, rồi nhìn phần dư, tức phần đường thẳng không giải thích được. Durbin–Watson so bước nhảy giữa hai phần dư liền nhau với độ lớn của phần dư. (chỉ vào hình trái) Phần dư đổi chậm, một tràng dương rồi một tràng âm: bước nhảy nhỏ, DW nhỏ, ví dụ 1, 1, 1, âm 1, âm 1, âm 1 cho DW khoảng 0,67. (chỉ vào hình phải) Phần dư đổi dấu liên tục thì DW lớn, khoảng 3,33.

DW gần 2 là ổn. Còn CPI theo dân số có DW chỉ 0,0051, gần như bằng 0. Nghĩa là các con số R bình phương và t ở trên dựa trên một giả định sai, không tin được. R bình phương cao đi cùng DW gần 0 là dấu hiệu của tương quan giả.

## cdd-hdd
Ở Texas, trời lạnh người ta bật sưởi, trời nóng bật điều hoà. Tải điện tăng ở cả hai phía, nên một đường thẳng theo nhiệt độ không tả được.

Ngành năng lượng xử lý bằng hai biến mới quanh một mốc 18,33 độ, tức 65 độ F. CDD là số độ nóng hơn mốc, HDD là số độ lạnh hơn mốc; phía còn lại bằng 0. (chỉ vào hình) Đường đỏ là CDD, đi lên khi nóng hơn mốc; đường xanh là HDD, đi lên khi lạnh hơn mốc. Ví dụ 25 độ thì CDD là 6,67, HDD bằng 0; 10 độ thì HDD là 8,33.

Đưa cả hai vào một hồi quy: phía nóng có một độ dốc, phía lạnh có một độ dốc, thành hình chữ V. Không cần chia dữ liệu làm hai nhóm. Trên tải điện ERCOT, R bình phương tăng từ 0,379 khi dùng nhiệt độ thẳng lên 0,812 khi dùng CDD và HDD, tức giải thích gấp đôi.

## mi
CDD và HDD cần ta biết trước hình dạng của quan hệ. Nếu chưa biết thì sao? Mutual information đo mọi kiểu phụ thuộc, không cần đoán hình dạng.

Câu hỏi của MI là: biết x có giúp đoán y không, theo bất kỳ cách nào. Ví dụ nhỏ: ngày lạnh tải cao, ngày vừa tải thấp, ngày nóng tải cao, mỗi loại một phần ba số ngày. Pearson bằng 0, vì đây là chữ U. Nhưng biết loại ngày là biết chắc tải. MI so tỷ lệ thật của mỗi ô với tỷ lệ nếu hai biến độc lập. Ô "vừa, thấp" xảy ra một phần ba số ngày, gấp 3 lần mức độc lập là một phần chín, nên góp một phần ba nhân ln 3, khoảng 0,366. Cộng ba ô được 0,637 nat.

Độc lập thì MI bằng 0. (chỉ vào hình) Với nhiệt độ và tải điện ERCOT, MI là 0,862 nat. MI nói có phụ thuộc, nhưng không nói hình dạng; muốn thấy hình dạng vẫn phải nhìn scatter như hình này.

## hoan-vi-khoi
MI của nhiệt độ và tải là 0,862. Con số đó lớn thật, hay chỉ do may? Ta kiểm bằng hoán vị, giống buổi 2: xáo y nhiều lần để phá quan hệ, rồi xem MI thật có vượt xa MI của dữ liệu xáo không.

Nhưng với chuỗi thời gian có một chỗ cần cẩn thận. Hai chuỗi trơn không liên quan gì vẫn hay có những quãng dài tình cờ cùng cao, cùng thấp, nên MI của chúng không nhỏ. (chỉ vào hàng giữa) Xáo từng điểm thì chuỗi thành nhiễu lộn xộn, mất hết độ trơn, MI của dữ liệu xáo rất nhỏ, và dữ liệu thật trông như đặc biệt. (chỉ vào hàng dưới) Xáo cả khối thì trong mỗi khối chuỗi vẫn trơn như thật, so sánh mới công bằng.

Thử trên hai chuỗi độc lập: xáo từng điểm cho p bằng 0,005, kết luận nhầm là có quan hệ; xáo theo khối cho p bằng 0,055, không bác bỏ. Với dữ liệu ERCOT, xáo theo khối một tuần, MI thật 0,862 vượt xa ngưỡng 0,124. Quan hệ có thật.

## he-so-lech
Chín giờ thuê xe có trung bình 11 mà trung vị chỉ 8. Số liệu lệch về phía nào, và lệch cỡ nào? Hệ số lệch trả lời bằng một con số.

Cách tính: lấy độ lệch của mỗi số khỏi trung bình, chia cho độ lệch chuẩn, lập phương, rồi lấy trung bình. Lập phương giữ dấu và phóng to số ở xa. Số 36 lệch cộng 25 nên góp gần hết tổng, còn số 8 lệch trừ 3 góp rất ít. Kết quả là cộng 1,35, tức đuôi phải dài.

(chỉ vào hình) Ô trái đối xứng quanh giữa, hệ số lệch gần 0. Ô phải dồn về bên trái, đuôi kéo dài sang phải, hệ số lệch dương. Lượt thuê theo giờ của cả bộ dữ liệu có hệ số lệch 1,277.

Hệ số lệch dương thì trung bình nằm trên trung vị, và các công thức giả định hình chuông sẽ không còn hợp.

## phan-phoi-chuan
Khoảng 95% hay được dựng bằng trung bình cộng trừ 1,96 lần độ lệch chuẩn. Con số 1,96 ở đâu ra?

Nó đến từ phân phối chuẩn, đường cong hình chuông đối xứng quanh trung bình. (chỉ vào hình) Diện tích dưới đường cong là tỷ lệ giá trị. Phần xanh ở giữa, từ trung bình trừ 1,96 s tới trung bình cộng 1,96 s, chiếm đúng 95%. Hai phần cam ở hai đuôi mỗi phần 2,5%. Nên 1,96 chính là quantile 0,975 của phân phối chuẩn. Để so sánh, cộng trừ 1 độ lệch chuẩn chỉ chứa 68,3%.

Ví dụ trung bình 100, độ lệch chuẩn 10 thì khoảng 95% là 80,4 tới 119,6. Nhưng với chín giờ thuê xe lệch phải, 11 trừ 1,96 nhân 10,57 cho cận dưới âm 9,7 lượt thuê, một con số vô lý.

Vậy 1,96 chỉ đúng khi dữ liệu gần hình chuông; dữ liệu lệch thì lấy thẳng quantile của lịch sử.

## hoan-vi
Năm 2012, ngày làm việc hơn ngày nghỉ 456 lượt thuê. Làm sao tính p-value mà không cần công thức?

Ý của kiểm định hoán vị: nếu nhãn làm việc hay nghỉ không liên quan tới lượt thuê, thì gán nhãn kiểu nào cũng như nhau. Ví dụ nhỏ, ngày làm việc 5, 7, 6, ngày nghỉ 3, 2, 4, chênh trung bình là 3. Có 20 cách chọn ba ngày làm nhóm làm việc, và chỉ 2 cách cho chênh cỡ 3 trở lên về một trong hai phía. Vậy p bằng 2 chia 20, tức 0,10.

Với dữ liệu thật, máy xáo nhãn 9.999 lần. (chỉ vào ô trái) Cột xanh là các chênh lệch khi xáo, vạch cam là chênh thật 456. Chỉ một mẩu nhỏ nằm ngoài vạch cam, p bằng 0,025. Ô phải, thứ Bảy so với Chủ nhật, p bằng 0,078.

Cách này giả định các ngày độc lập, nên với chuỗi thời gian p thật thường lớn hơn.

## seasonal-subseries
Nhìn đường theo thời gian thì khó thấy mùa vụ. Xếp lại theo thứ, theo tháng thì thấy gì?

Có hai cách xếp. (chỉ vào ô trái) Seasonal plot vẽ mỗi tuần một đường rồi chồng lên nhau. Hai tuần ở đây song song: cùng hình dạng, tuần 2 cao hơn tuần 1 đúng 2 đơn vị ở mọi thứ.

(chỉ vào ô phải) Subseries plot gom mỗi thứ vào một ô. Vạch cam là trung bình của thứ đó: 11, 13, 13, 13, 15, 7, 5, chính là hình dạng mùa vụ tuần. Trong mỗi ô, điểm sau cao hơn điểm trước, tức là có xu hướng.

Trên lượt thuê theo giờ, seasonal plot theo tuần cho thấy thứ Hai tới thứ Sáu có hai đỉnh sáng chiều, cuối tuần chỉ một bướu giữa ngày: mùa vụ kép. Theo tháng, mỗi tháng 2012 gấp 1,41 tới 2,57 lần cùng tháng 2011.

Seasonal plot cho hình dạng mùa vụ, subseries cho biết mỗi mùa đổi ra sao qua thời gian.

## lag-plot
Giờ trước, cùng giờ hôm qua hay cùng giờ tuần trước: cái nào giống giờ này nhất? 

Lag plot là scatter, mỗi chấm ghép giá trị bây giờ với giá trị cách nó k bước về trước. Ví dụ chuỗi 2, 4, 6, 4 lặp lại, xét trễ 2. (chỉ vào hình) Trục ngang là y lúc t trừ 2, trục dọc là y lúc t. Cặp 2 với 6 nằm góc trên trái, cặp 6 với 2 nằm góc dưới phải. Các chấm đi xuống, ngược đường chéo cam: trễ 2 là nửa vòng lặp nên đỉnh ghép với đáy.

Trên lượt thuê theo giờ, trễ 168, tức cùng giờ tuần trước, bám đường chéo hẹp nhất với r bằng 0,88. Trễ 12 tách thành hai nhánh, r bằng âm 0,14, và con số đó chỉ là trung bình của hai nhánh.

Chấm bám đường chéo ở trễ k nghĩa là giá trị cách k bước đoán tốt hiện tại.

## truc-y-cat
Doanh thu chỉ tăng 4,1% mà cột sau trông cao gấp ba. Vì sao?

Vì người vẽ chọn thang. (chỉ vào ô trái) Trục dọc ở đây bắt đầu từ 480 chứ không từ 0, gọi là trục y cắt. Độ cao một cột bằng giá trị trừ đáy trục, chia cho khoảng từ đáy tới đỉnh trục. Tháng 5 là 490 triệu, cao 10 trên 40, tức 25% hình. Tháng 6 là 510 triệu, cao 30 trên 40, tức 75%. Mắt thấy gấp ba. (chỉ vào ô phải) Vẽ trục từ 0 thì hai cột gần bằng nhau.

Trục kép cũng vậy: hai trục dọc, hai thang. Chọn thang phải hẹp thì hai đường trùng khít, chọn rộng thì một đường nằm ngang.

Quy ước của khoá: số đếm và tổng vẽ trục từ 0. Hai chuỗi khác đơn vị thì tách hai hình, hoặc đánh chỉ số: chia cho tháng đầu rồi nhân 100. Đọc thang trước khi đọc đường.

## tron-nam
Mỗi năm, tương quan giữa nhiệt độ và lượt thuê đều trên 0,7. Gộp hai năm lại chỉ còn 0,627. Quan hệ yếu đi thật sao?

(chỉ vào hình) Trục ngang là nhiệt độ trung bình ngày, trục dọc là lượt thuê mỗi ngày. Chấm xanh là năm 2011, chấm cam là 2012. Các bạn nhìn một cột dọc bất kỳ, ví dụ quanh 25 độ: chấm cam nằm trên chấm xanh. Cùng nhiệt độ mà năm 2012 cao hơn, vì có nhiều người dùng hơn.

Hai đám mây song song. Năm 2011 r là 0,771, năm 2012 là 0,714. Khi gộp, hai mức khác nhau chồng lên nhau làm đám điểm dày ra theo chiều dọc, nên r chỉ còn 0,627, thấp hơn cả hai năm.

Cách nhận ra rất đơn giản: tô màu scatter theo năm. Thấy các đám song song thì tính r riêng từng năm.

## guerrero
Log ép quá tay, để nguyên thì dao động phình ra. Chọn lambda ở giữa bằng cách nào?

Cách của Guerrero: chia chuỗi thành từng năm. Sau Box-Cox, dao động của năm có mức mu gần bằng s chia mu mũ một trừ lambda. Ta chọn lambda làm các tỷ số này đều nhất, đo bằng CV, tức độ lệch chuẩn của chúng chia trung bình.

Ví dụ ba năm có mức 100, 400, 900 và độ lệch chuẩn 10, 20, 30. Lambda bằng 1 thì tỷ số là 10, 20, 30, CV bằng 0,5. Lambda bằng 0,5 thì chia cho căn của mức: năm 400 có 20 chia 20 bằng 1, cả ba năm đều bằng 1, CV bằng 0. Lambda bằng 0, tức log, cho 0,1 rồi 0,05, ép quá tay.

(chỉ vào ô trái) Trên bán lẻ Mỹ, đường CV theo lambda có đáy ở khoảng 0,34. (chỉ vào ô phải) Với lambda đó, đường cam nằm sát mức 1 nhất, còn log tụt xuống dưới.

## exp-trung-vi
Dự báo trên thang log rồi exp về: vì sao cộng lại thì hụt so với tổng thật?

Ví dụ ba giá trị log 0, 1, 2. (chỉ vào hàng trên) Trên thang log chúng cách đều, trung bình là 1. Exp của 1 là 2,72. (chỉ vào hàng dưới) Đổi từng giá trị về thang gốc thì được 1, 2,72 và 7,39. Trung bình thật là 3,70, nằm bên phải vạch 2,72.

Lý do: exp giữ thứ tự, nên số đứng giữa vẫn đứng giữa. 2,72 là trung vị. Nhưng exp kéo giãn phía trên, đẩy số lớn ra xa và kéo trung bình lên. Độ lệch chuẩn trên thang log bằng 0,5 thì trung vị thấp hơn trung bình 11,75%.

Khi cần tổng hay trung bình, nhân thêm một cộng sigma bình phương chia hai. Khi chấm bằng MAE thì không cần, vì MAE ưa trung vị. Sigma nhỏ thì phần hụt không đáng kể.

## ty-le-mau-hinh
Phân rã xong, phần dư trông lộn xộn. Nó đã hết nhịp theo giờ, theo tháng chưa?

Tỷ lệ mẫu hình kiểm bằng một con số. Nhóm phần dư theo lịch, ví dụ tháng nhân giờ, lấy trung bình mỗi nhóm, rồi đo các trung bình đó lệch nhau cỡ nào so với dao động của cả chuỗi. Ví dụ phần dư buổi sáng là âm 3, âm 5, buổi chiều là cộng 3, cộng 5. Trung bình hai nhóm là âm 4 và cộng 4, phương sai 32. Chuỗi có phương sai 320 thì tỷ lệ là 0,1: phần dư còn nhịp sáng chiều.

(chỉ vào cột trái) Với tải điện PJM, phân rã cổ điển chu kỳ 24 còn vệt đỏ vào chiều hè, tỷ lệ 0,102, tức một phần mười phương sai vẫn là mẫu hình. (chỉ vào cột phải) MSTL gần như trắng, tỷ lệ 0,0006.

Phần dư trông lộn xộn chưa đủ, hãy nhóm theo lịch rồi đo.

## stl-loess
Mùa vụ lớn dần qua các năm. Một khuôn mùa vụ cố định sẽ bỏ sót điều gì?

Ví dụ phần dữ liệu trừ xu hướng của quý 1 qua năm năm là 2, 4, 6, 8, 10. (chỉ vào đường xám) Phân rã cổ điển lấy một trung bình cho mọi năm, bằng 6. Phần dư đi từ âm 4 tới 4, vẫn còn một đường đi lên. (chỉ vào đường cam) Nếu mỗi năm chỉ lấy trung bình ba năm quanh nó, ta được 3, 4, 6, 8, 9, phần dư chỉ từ âm 1 tới 1.

STL làm đúng ý đó bằng LOESS: ở mỗi điểm, khớp một đường qua các điểm lân cận, điểm gần nặng hơn. Nhờ vậy mùa vụ được đổi dần.

Cửa sổ xu hướng quá ngắn thì xu hướng ôm luôn nhịp tuần và thời tiết. Trên PJM, STL chu kỳ 24 mặc định còn phương sai phần dư 2,8 GW bình phương, MSTL 16,5. Nhỏ ở đây là nhỏ giả tạo.

## ljung-box-q
Q sao bằng 5,16 là lớn hay nhỏ? Phải so với ngưỡng nào?

Nếu chuỗi là nhiễu trắng, Q sao theo phân phối khi bình phương. Bậc tự do bằng số trễ gộp vào, trừ số tham số nếu ta kiểm sai số của một mô hình. Ví dụ chuỗi 100 điểm, r1 bằng 0,2, r2 bằng 0,1. Q sao bằng 100 nhân 102, nhân tổng 0,2 bình phương chia 99 với 0,1 bình phương chia 98, ra khoảng 5,16.

(chỉ vào hình) Đây là đường cong khi bình phương với 2 bậc tự do. Vùng đỏ là 5% giá trị lớn nhất, bắt đầu từ 5,99. Vạch xanh 5,16 chưa chạm vùng đỏ, nên chưa bác bỏ nhiễu trắng, p khoảng 0,076.

Nhớ trừ bậc tự do: 10 trễ trên sai số của mô hình 2 tham số thì còn 8 bậc, ngưỡng 15,51 thay vì 18,31. Quên trừ thì p cao hơn thật.

## random-walk
Số liệu tăng vài tháng liền: có xu hướng thật, hay chỉ là các bước ngẫu nhiên cộng dồn?

Random walk là vị trí mới bằng vị trí cũ cộng một bước ngẫu nhiên. Ví dụ tung đồng xu, ngửa tiến 1, sấp lùi 1. Sáu lần tung cộng, trừ, cộng, cộng, trừ, cộng cho vị trí 1, 0, 1, 2, 1, 2.

(chỉ vào hình) Trục ngang là số bước, trục dọc là vị trí, mỗi đường xám là một người. Không có mức nào để quay về, nên càng lâu càng có thể đi xa. Hai đường cam đứt là cộng trừ một độ lệch chuẩn, nở ra theo căn bậc hai số bước. Mô phỏng 10.000 người: 4 bước độ lệch chuẩn là 2,0, 25 bước là 5,0, 100 bước là 10,1. Số bước gấp 25 lần thì độ lệch chuẩn gấp 5 lần.

Vì vậy random walk không dừng, phải sai phân, và dự báo tốt nhất cho nó là giá trị cuối cùng.

## bon-chuoi
Trước khi sang kiểm định, chúng ta đặt bốn chuỗi mẫu của buổi 7 cạnh nhau.

Đọc từng dòng. Nhiễu trắng không nhớ gì, r1 gần 0: dừng. AR(1) với phi 0,7 nhớ bước trước nhưng bị kéo về mức: vẫn dừng, r1 0,71 nhưng tới trễ 30 đã về 0. Random walk nhớ mãi, không có mức để quay về: không dừng, phải sai phân. Chuỗi xu hướng không nhớ gì cả, nó chỉ bám một đường thẳng: dừng quanh đường xu hướng, nên chữa bằng cách trừ đường đó đi.

(chỉ vào cột r1 / r30) Chỗ cần để ý: random walk và xu hướng có r1 đều khoảng 0,98, ACF giảm chậm như nhau. Nhìn ACF không tách được hai loại này; phải chạy ADF và KPSS dạng “ct”, ở slide sau.

Chữa nhầm thì sao? Sai phân chuỗi quanh xu hướng là sai phân thừa, sinh tương quan âm giả. Trừ đường thẳng khỏi random walk thì phần còn lại vẫn lang thang. Mẹo nhớ: random walk thì sai phân, dừng quanh xu hướng thì khử xu hướng.

## entropy
Chuỗi này có nhịp đều để khai thác, hay gần như ngẫu nhiên?

Phổ cho biết mỗi tần số góp bao nhiêu năng lượng. Ta đổi phổ thành các phần cộng lại bằng 1, như chia một chiếc bánh. Spectral entropy đo bánh chia đều tới đâu: 0 là dồn vào một đĩa, 1 là chia đều. Công thức cộng trừ p nhân log p của từng phần, rồi chia cho log số tần số để kết quả nằm từ 0 tới 1. Ví dụ phổ bốn tần số: dồn cả vào một tần số thì entropy 0, hai nhịp chia đôi thì 0,5, mỗi tần số một phần tư thì 1.

(chỉ vào hàng dưới) Chuỗi mùa vụ 12 tháng dồn gần hết vào một cột, entropy 0,33. Nhiễu thuần trải đều, entropy 0,94. Trên 4.000 chuỗi M4, trung vị là 0,462.

Nhờ vậy ta xếp hạng độ khó hàng nghìn chuỗi mà chưa chạy mô hình nào.

## dac-trung
48.000 chuỗi thì không ai xem từng hình. Chuỗi nào khó, chuỗi nào giống nhau?

Ta tóm mỗi chuỗi thành vài con số gọi là đặc trưng, như CV, r1, entropy. Mỗi chuỗi thành một hàng số, cả tập thành một bảng.

Đặc trưng tốt phải không đổi theo đơn vị. Ví dụ chuỗi a là 2, 4, 6, 4 lặp lại, và chuỗi 1.000 lần a. Trung bình là 4 và 4.000, đổi theo đơn vị. CV là 1,51 chia 4 và 1.512 chia 4.000, cùng bằng 0,378. Nhân chuỗi với 1.000 mà đặc trưng đổi theo thì nó đang đo độ lớn, không đo hình dạng. Trong 20 đặc trưng của buổi, chỉ trung bình và độ lệch chuẩn đổi.

(chỉ vào hình) Ô trái, hai chuỗi cùng hình nhưng một chuỗi lớn gấp 100 lần. Ô phải, sau z-score hai đường trùng khít. Code chạy STL trên chuỗi đã z-score để nhóm đặc trưng xu hướng cũng không đổi.

Và tính mọi chuỗi trên cùng độ dài.

## do-phan-giai
Nhiệt độ ghi đúng 26,0 °C suốt nhiều giờ: cảm biến hỏng, hay trời đổi quá ít? Trước khi trả lời, chúng ta phải biết độ phân giải, tức bước nhỏ nhất cảm biến ghi được.

(chỉ vào hình) Trục ngang là giờ, đường xanh là nhiệt độ thật, đường cam là số ghi được. Ô trái, nhiệt độ thật đi từ 25,6 lên 26,4 °C, nhưng cảm biến ghi tới 1 °C nên cả năm số đều là 26. Đường cam nằm ngang mà cảm biến vẫn khoẻ. Ô phải thì khác: nhiệt độ thật đổi vài độ, cả ngày lẫn đêm, mà số ghi không nhúc nhích. Đó mới là kẹt.

Ở trạm Nội Bài, nếu đặt ngưỡng đứng yên 12 giờ thì ra 24 đoạn, quá nhiều để đều là hỏng, nên buổi 10 dùng 18 giờ. Vậy các bạn nhớ thứ tự: đo độ phân giải trước, rồi mới đặt ngưỡng gọi cảm biến là kẹt.

## dien-nhan-qua
Điền chỗ thiếu xong thì backtest đẹp hẳn. Câu hỏi đầu tiên: cách điền có dùng số của tập kiểm không?

(chỉ vào hình) Ba mốc: 20, một ô trống, rồi 30. Vạch đứt là mốc cắt, bên phải là tương lai. Ô vuông xanh là ffill, lấy số gần nhất phía trước, nên điền 20. Hình thoi đỏ là nội suy tuyến tính, điền 25, nhưng con số 25 chỉ có được nhờ số 30 nằm bên phải vạch. Nếu số 30 thuộc tập kiểm thì thông tin tập kiểm đã chảy vào tập học.

Kiểm bằng máy: làm sạch dữ liệu đầy đủ và dữ liệu bị cắt tại một mốc, rồi so phần trước mốc. Điều kiện là mốc cắt phải nằm trong một lỗ, nếu cắt ở chỗ dữ liệu liền thì bài kiểm luôn báo sạch.

Điền nhân quả chỉ dùng số trước ô đang điền: có số mới thì số cũ không đổi.

## z-score-masking
Mười số quanh 12 có một số 50. Vì sao ngưỡng 3σ không gắn cờ nó?

z-score hỏi một điểm cách trung bình bao nhiêu lần độ lệch chuẩn. Nhưng chính số 50 kéo trung bình lên 15,6 và kéo độ lệch chuẩn lên khoảng 12,1, trong khi bỏ nó đi thì độ lệch chuẩn chỉ khoảng 1. Lấy 50 trừ 15,6 rồi chia 12,1, được 2,84, không vượt 3.

(chỉ vào hình) Trục ngang là vị trí, trục dọc là giá trị. Vạch cam đứt là trung bình cộng ba lần độ lệch chuẩn: ở ô trái nó nằm ở 52, cao hơn chính số 50. Ô phải thêm số 60, vạch cam bị đẩy lên gần 76, và cả hai ngoại lai cùng lọt. Ngoại lai tự che mình và che nhau, đó gọi là masking.

Trên lượt xem Wikipedia, thêm một ngày giả thật lớn làm số ngày bị gắn cờ tụt từ 16 xuống 5. Không vượt 3σ không có nghĩa là dữ liệu sạch.

## mad-hampel
Lượt xem tăng suốt mười năm. So mỗi ngày với trung bình cả chuỗi còn có nghĩa không? Không, nên ta sửa hai chỗ.

Chỗ thứ nhất: đo bằng trung vị. Với mười số vừa rồi, trung vị là 12. Khoảng cách tới 12 có trung vị là 1, nhân 1,4826 để cùng thang với độ lệch chuẩn, ra MAD khoảng 1,48. Điểm của số 50 là 38 chia 1,48, khoảng 25,6, vượt xa 3. Điểm của số 10 chỉ 1,35.

Chỗ thứ hai: so tại chỗ. Bộ lọc Hampel tính trung vị và MAD trong cửa sổ quanh mỗi điểm. (chỉ vào hình) Dải xanh là trung vị cộng trừ ba MAD của cửa sổ, nó đi lên theo xu hướng. Điểm vọt khỏi dải bị tô đỏ, còn ngưỡng 3σ toàn chuỗi nằm cao hơn mọi điểm.

Hampel dùng cửa sổ có tâm, nên chỉ dùng để làm sạch lịch sử, không làm feature dự báo.

## xu-ly-bat-thuong
Điểm 90 bị gắn cờ giữa các số quanh 12: xoá, kéo về 12, hay giữ nguyên?

(chỉ vào hình) Dấu nhân xám là số 90 bị gắn cờ. Xoá nó thì lưới thời gian thủng một mốc. Winsorize thì kéo nó về trung vị địa phương là 12, chuỗi thành 12, 11, 13, 12, 12, giữ đủ mốc, kèm cột da_sua bằng 1.

Nhưng nếu ngày đó là Tết thì sao? Trên lượt xem bài Tết Nguyên Đán, mọi cách tìm ngoại lai đều gắn cờ cả 10 đỉnh Tết. Ngưỡng thống kê chỉ biết điểm này khác, không biết khác vì lỗi hay vì sự kiện thật. Việc đó cần nhật ký sự kiện, tức danh sách các mốc có sự kiện đã biết. Có trong nhật ký thì giữ nguyên 90.

Tóm lại, chọn theo loại: lỗi đo thì winsorize, sự kiện thật thì giữ và ghi nhật ký, dịch mức thì thêm biến giả, là cột 0 và 1 đánh dấu sự kiện.

## penalty
Mức đổi đột ngột mà từng điểm riêng lẻ trông vẫn bình thường. Tìm mốc đổi đó thế nào?

Ta chia chuỗi thành đoạn, mỗi đoạn có trung bình riêng. Chi phí một đoạn là tổng bình phương khoảng cách tới trung bình đoạn. Chia càng nhiều càng khớp, nên mỗi điểm gãy phải trả một khoản phạt gọi là penalty.

(chỉ vào hình) Ô trái là mười số, năm số quanh 10 rồi năm số quanh 20. Ô phải, trục ngang là số điểm gãy, cột xanh là chi phí, phần cam là penalty khoảng 6,9 cho mỗi điểm gãy. Không cắt tốn 254. Cắt một lần còn 4, cộng 6,9 là 10,9. Cắt hai lần chi phí còn 3,17 nhưng phải trả 13,8, tổng 17,0. Một điểm gãy thắng.

Thuật toán PELT tìm đúng cách chia có tổng chi phí cộng penalty nhỏ nhất. Penalty nhỏ thì cắt vụn, lớn thì không còn điểm gãy, nên các bạn quét nhiều mức và giữ kết quả ổn định.

## nyquist
Hạ dữ liệu 10 phút xuống 1 giờ thì hiện ra một chu kỳ 2,5 giờ. Nó từ đâu ra?

(chỉ vào hình) Đường xám là sóng thật, lặp mỗi 4 bước. Chấm đỏ là các mẫu, lấy mỗi 3 bước một lần. Nối các chấm lại được sóng nét đứt, lặp mỗi 12 bước, không có thật. Hiện tượng này gọi là aliasing, giống bánh xe trong phim cũ trông như quay ngược.

Quy tắc Nyquist: lấy mẫu với tần số f_s thì chỉ thấy đúng dao động chậm hơn một nửa f_s. Dao động nhanh hơn bị gập xuống: lấy tần số thật trừ bội số gần nhất của tần số lấy mẫu. Ở đây một phần tư trừ một phần ba, trị tuyệt đối là một phần mười hai, tức chu kỳ giả 12 bước. Với dữ liệu 10 phút, dao động 43 phút gập thành đúng chu kỳ giả 2,5 giờ đó.

Cách tránh: lọc thông thấp, bỏ dao động nhanh, rồi mới hạ mẫu.

## sau-ho-loc
Sáu họ bộ lọc, mười cấu hình. Cái nào dùng được làm feature dự báo?

Savitzky–Golay khớp đa thức quanh mỗi điểm. Butterworth cắt tần số theo ngưỡng. Kalman ước lượng tín hiệu ẩn.

(chỉ vào hình) Tín hiệu nhảy từ 0 lên 1 tại vạch chấm. Bản một chiều, màu xanh, chỉ lên sau vạch: nó trễ. Bản xuôi rồi ngược, màu cam, đã lên trước vạch. Nó không trễ vì đầu ra lúc đó đã dùng số của tương lai.

Trên tín hiệu mô phỏng, ba bộ lọc có sai số thấp nhất đều nhìn tương lai. Đổi 10 số cuối chuỗi thì sosfilt giữ nguyên quá khứ, còn filtfilt đổi quá khứ tới 23,615 và kéo ngược 274 bước. Bù lại, Butterworth nhân quả trễ 19 bước. Dùng được làm feature chỉ có trailing, EWMA, sosfilt và Kalman filter với tham số cố định từ phần học.

Độ trơn luôn phải trả bằng trễ, hoặc bằng việc nhìn tương lai.

## bang-bo-loc
Sáu họ bộ lọc của buổi 12 gom vào một bảng để tra khi cần.

Đọc theo cột “hiểu đơn giản” trước. Trailing lấy trung bình k điểm gần nhất. Centered lấy các điểm quanh nó, cả trước lẫn sau. EWMA cho điểm mới nặng hơn điểm cũ. Savitzky–Golay khớp một đa thức nhỏ quanh mỗi điểm nên giữ được chiều cao đỉnh. Butterworth cắt tần số cao theo ngưỡng. Kalman ước lượng một tín hiệu ẩn đổi dần, cộng nhiễu.

(chỉ vào cột cuối) Cột quan trọng nhất là “nhân quả”. Làm feature dự báo thì chỉ chọn trong các dòng “có”. Hai dòng “có / không” tuỳ phiên bản: sosfilt và Kalman filter chạy một chiều thì nhân quả; sosfiltfilt và Kalman smoother chạy hai chiều thì nhìn tương lai. Riêng Kalman filter chỉ nhân quả khi tham số ước lượng trên phần học rồi cố định; khớp lại trên cả chuỗi thì quá khứ đổi tới 1,134.

## kiem-nhan-qua
Tài liệu thư viện không nói bộ lọc có dùng số của giờ sau không. Kiểm thế nào? Đổi đuôi, xem đầu.

Năm giờ điện 10, 12, 14, 30, 16, đổi giờ cuối từ 16 thành 40. Trung bình trượt kiểu centered ở giờ 4 đổi từ 20 thành 28: một con số quá khứ bị sửa khi dữ liệu mới về. Kiểu trailing ở giờ 4 vẫn 18,67.

(chỉ vào hình) Ô dưới, trục dọc là đầu ra mới trừ đầu ra cũ, thang log. Nhìn bên trái vạch đen đứt, chỗ bắt đầu đổi: đường xanh trailing nằm ở 0, đường cam centered nhảy lên ở 6 mốc ngay trước vạch, đúng nửa cửa sổ 13.

Ba chỗ hay sai: so mọi mốc trước điểm đổi, không bỏ đoạn cuối; dung sai theo thang dữ liệu; và tham số ước lượng trên cả chuỗi cũng làm quá khứ đổi, như Kalman filter khớp lại trên cả chuỗi đổi quá khứ 1,134.

Nhân quả thì quá khứ đứng yên.

## ca-chuoi
Chuẩn hoá cả tập dữ liệu rồi mới chia học và kiểm. Tương lai lọt vào ở đâu?

Lấy sáu ngày doanh thu 10, 12, 8, 14, 20, 16. Trung bình cả sáu ngày là 13,33, đã chứa hai ngày cuối. Vậy khi ngày 1 được chuẩn hoá và biết mình thấp hơn trung bình, nó đã biết các ngày sau cao. Target encoding cũng vậy: trung bình nhóm A là 12,67, tính gộp cả số 20 của ngày 5, rồi gán ngược cho ngày 1.

Kiểu thứ ba các bạn đã gặp ở buổi 10. (chỉ vào hình) Nội suy hai phía điền ô trống bằng cách nhìn sang số bên phải mốc cắt, còn ffill chỉ nhìn quá khứ. Rò rỉ này chỉ thấy ở mép lỗ, những ngày không thiếu thì hai cách giống hệt nhau.

Cách sửa chung: tính mọi tham số, trung bình, độ lệch chuẩn hay trung bình nhóm, chỉ trên phần học hoặc từ những ngày trước t.

## kiem-ro-ri
41 feature, không ai đọc hết từng dòng code. Máy kiểm rò rỉ giúp được không? Được, bằng hai bài kiểm.

Bài thứ nhất, cắt tương lai: tính feature trên dữ liệu đầy đủ, cắt tại một mốc, tính lại, so mọi dòng trước mốc. Cắt sau ngày thứ tư thì cột trung bình có tâm đổi từ 14 thành NaN, còn cột đã shift giữ nguyên.

Nhưng cắt ở đâu thì lag_1 vẫn y như nhau, nên cần bài thứ hai là nhiễu mục tiêu. (chỉ vào hình) Ô trên, y bị cộng nhiễu từ vạch đứt. Ô dưới, mỗi vạch là một dòng có feature đổi. Vùng xanh là các dòng mà lúc ra dự báo, tức 3 bước trước, nhiễu chưa xảy ra. lag_1 đổi ngay trong vùng xanh nên bị bắt, lag_3 chỉ đổi sau vùng đó. Với tầm dự báo 24 giờ, lag_1 đổi ở 23 dòng ngay sau mốc.

Bài kiểm xanh chỉ nói không thấy rò rỉ ở những mốc đã cắt.

## ex-ante
Tối nay dự báo tải điện trưa mai. Nhiệt độ trưa mai trong tay ta là số nào? Là bản dự báo, không phải số thật.

Nhiệt độ ở đây là biến ngoại sinh, biến ngoài chuỗi dùng làm feature. Trưa mai thật 35 °C, nhưng tối nay ta chỉ có bản dự báo 33 °C, nên feature phải là 33. Dùng bản có trong tay lúc dự báo gọi là ex-ante. Dùng số thật biết về sau là ex-post, và trong backtest đó là rò rỉ.

(chỉ vào hình) Ô trái là nhiệt độ Dallas nửa đầu tháng 7 năm 2024: đường đen là thật, xanh là dự báo trước 1 ngày, cam là trước 3 ngày. Ô phải là phân phối sai số. Dự báo trước 1 ngày sai trung bình 1,32 °C, trước 3 ngày 2,07 °C.

Với từng biến, các bạn hỏi: lúc ra dự báo, con số này đã có chưa?

## mape-lech
Cùng lệch 50 đơn vị, vì sao dự báo cao bị MAPE phạt nặng hơn dự báo thấp?

MAPE chia sai số cho thực tế. Thực tế 100, dự báo 150: lệch 50 chia 100, ra 50%. Thực tế 150, dự báo 100: vẫn lệch 50 nhưng chia 150, chỉ còn 33,3%. Dự báo thấp sai nhiều nhất là 100%, khi dự báo bằng 0, còn dự báo cao thì sai bao nhiêu phần trăm cũng được. Nên tối ưu MAPE sẽ kéo dự báo xuống thấp.

(chỉ vào hình) Với 20.000 số mô phỏng lệch phải như doanh số, ở ô phải trục ngang là hằng số dự báo, trục dọc là chỉ số, chia cho giá trị nhỏ nhất của chính nó. Nhìn đáy ba đường: MAE đáy ở 20,0, đúng trung vị; RMSE ở 30,1, là trung bình; MAPE ở 9,1, thấp hơn cả hai.

sMAPE mang tên đối xứng nhưng cũng không đối xứng. Chọn mô hình bằng MAPE là nghiêng về dự báo thấp.
