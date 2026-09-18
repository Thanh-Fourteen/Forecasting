# Kiểm tra buổi 11 — Ngoại lai và điểm gãy

10 câu. Tự làm trước, mở đáp án sau.

---

**1 (nhắc lại).** Kể bốn loại bất thường và dấu hiệu nhận biết từng loại.

<details><summary>Đáp án</summary>

- **AO** (outlier cộng): một điểm lệch, mức trước và sau như cũ.
- **LS** (level shift): mức nhảy và **ở lại**.
- **TC** (thay đổi tạm): mức nhảy rồi hồi dần về cũ.
- **Đổi phương sai**: mức giữ nguyên, **biên độ** dao động đổi.

Mỗi loại cần một cách phát hiện khác: Hampel cho AO, phát hiện điểm gãy cho LS/TC, chi phí Gaussian trên phần dư cho đổi phương sai.

</details>

---

**2 (nhắc lại).** Masking là gì? Swamping là gì?

<details><summary>Đáp án</summary>

**Masking**: ngoại lai kéo trung bình và σ lên, nên chính nó (và các ngoại lai khác) **không** vượt ngưỡng nữa — ngoại lai tự che mình.
**Swamping**: ngược lại, ngoại lai làm ước lượng lệch đến mức các điểm **bình thường** bị gắn cờ oan. Cả hai đều biến mất khi dùng ước
lượng bền vững (trung vị, MAD).

</details>

---

**3 (nhắc lại).** Hệ số 1,4826 trong công thức MAD từ đâu ra?

<details><summary>Đáp án</summary>

$1/\Phi^{-1}(0{,}75) \approx 1{,}4826$ — hệ số đưa MAD về cùng thang với độ lệch chuẩn **khi dữ liệu phân phối chuẩn**. Nhờ nó, ngưỡng
"3 MAD" đọc được như "3σ" mà không bị ngoại lai làm hỏng.

</details>

---

**4 (nhắc lại).** PELT cần gì để chạy, và vì sao phải chọn penalty?

<details><summary>Đáp án</summary>

Cần (a) một **hàm chi phí** (`l2` cho đổi trung bình, `normal` cho đổi trung bình + phương sai, `rbf` phi tham số) và (b) **penalty** $\beta$
phạt mỗi điểm gãy thêm vào. Không có penalty thì lời giải tối ưu là cắt ở mọi điểm (chi phí nội đoạn bằng 0). Quy ước BIC $=2\log n$,
MBIC $\approx 3\log n$, nhưng nên **quét** rồi lấy vùng kết quả ổn định.

</details>

---

**5 (vận dụng).** Bạn chạy 3σ trên chuỗi doanh thu 5 năm đang tăng trưởng và chỉ bắt được 3 điểm, tất cả ở năm cuối. Chuyện gì xảy ra và
sửa thế nào?

<details><summary>Đáp án</summary>

Trung bình toàn chuỗi nằm đâu đó giữa mức năm 1 và năm 5, nên "lệch 3σ so với trung bình toàn chuỗi" chỉ có nghĩa là "**mức cao**", không
phải "bất thường". Với dữ liệu buổi này, 3σ gắn cờ 16/3.653 ngày và dồn hết vào vùng mức cao.

Sửa: dùng ngưỡng theo **mức địa phương** (Hampel với cửa sổ trượt: 121 ngày, rải đều), hoặc đặt ngưỡng trên **phần dư** sau khi khử xu
hướng và mùa vụ.

</details>

---

**6 (vận dụng).** Giám đốc yêu cầu "làm sạch mọi ngoại lai" trên chuỗi lượt xem bài Tết. Bạn làm gì?

<details><summary>Đáp án</summary>

Từ chối làm theo nghĩa đen, kèm bằng chứng: **cả 5 phương pháp (3σ, IQR, MAD, Hampel, STL robust) đều gắn cờ 10/10 đỉnh Tết**. Đó là sự
kiện thật, là thứ đáng dự báo nhất trong chuỗi.

Việc cần làm: lập **nhật ký sự kiện** (10 mốc Tết), truyền vào `bo_qua_su_kien`, chỉ winsorize những gì còn lại, và **không xoá mốc nào**.
Với mô hình, thêm biến giả Tết (buổi 13).

</details>

---

**7 (vận dụng).** PELT trên chuỗi hành khách hàng không cho 43 điểm gãy. Sửa thế nào, và kiểm kết quả có đáng tin không bằng cách nào?

<details><summary>Đáp án</summary>

Nguyên nhân: chuỗi tăng trưởng **nhân tính** — biên độ dao động tỷ lệ với mức, nên `l2` đọc mọi lần biên độ đổi thành đổi mức. Sửa: lấy
**log** (hoặc Box-Cox) trước → còn 2 điểm gãy.

Kiểm độ tin cậy: (a) **quét penalty** và lấy các mốc xuất hiện ở mọi penalty trong một khoảng (ở đây 1–4·log n); (b) kiểm số điểm gãy
**giảm đơn điệu** theo penalty; (c) tính **độ lớn** thật của từng điểm gãy (−78,7% và +238,2%) — nếu chênh lệch không đáng kể thì đó là
điểm gãy thống kê chứ không phải điểm gãy nghiệp vụ.

</details>

---

**8 (vận dụng).** Bạn nghi ngờ biên độ dao động của chuỗi đổi từ giữa năm, nhưng đo σ hai bên thì gần bằng nhau (7,9 và 7,9). Có thể bạn
đã bỏ sót gì?

<details><summary>Đáp án</summary>

σ thô bị **biên độ mùa vụ** chi phối, nên thay đổi của σ **nhiễu** bị át hoàn toàn. Phải đo trên **phần dư** sau STL. Ngoài ra dùng **MAD**
thay `std`, vì một ngoại lai đơn lẻ có thể làm `std` phình gấp 4 lần và tạo cảnh báo giả. Và dùng `model="normal"` trong PELT — `l2` chỉ
nhìn trung bình.

</details>

---

**9 (đọc biểu đồ).** Hình `diem-gay-pelt.png`, ô phải: số điểm gãy theo penalty/log n là 3 (0,5), 2 (1 → 4), 0 (từ 5 trở lên). Bạn chọn
penalty nào và vì sao? Nếu một đồng nghiệp chọn 8·log n rồi kết luận "chuỗi này không có điểm gãy" thì sai ở đâu?

<details><summary>Đáp án</summary>

Chọn trong vùng **1–4·log n** (lấy giữa, ví dụ 3·log n ≈ MBIC): đó là "elbow" — kết quả không đổi trên một dải penalty rộng, dấu hiệu hai
điểm gãy này là cấu trúc thật chứ không phải lựa chọn tham số.

Sai của đồng nghiệp: penalty 8·log n phạt nặng tới mức **mọi** phân đoạn đều bị loại; "0 điểm gãy" là kết luận về tham số, không phải về
dữ liệu. Bằng chứng ngược lại rất rõ: tháng 2020-04 chỉ còn 890.607 khách so với 66,0 triệu của 2020-01 (−98,65%). Luôn quét, đừng tin một
giá trị penalty.

</details>

---

**10 (đọc bảng — tìm chỗ sai).** Báo cáo về chuỗi hành khách hàng không:

| Kết luận | Bằng chứng |
|---|---|
| (a) "Chúng tôi xoá toàn bộ 15 tháng COVID khỏi dữ liệu để chuỗi sạch." | pipeline |
| (b) "Cắt bỏ dữ liệu trước 2021-07 là cách tốt nhất vì dữ liệu cũ đã lỗi thời." | trực giác |
| (c) "MAPE của cách tốt nhất là 8,71%, nên mô hình đã sẵn sàng chạy thật." | bảng so sánh |
| (d) "Hampel không gắn cờ tháng 2020-04 nên tháng đó không bất thường." | kết quả chạy |

Chỉ ra chỗ sai của từng dòng.

<details><summary>Đáp án</summary>

- **(a)** "Xoá" mơ hồ và nguy hiểm. Nếu xoá **dòng** thì chuỗi thủng 15 mốc, `resample` và lag hỏng hết. Đúng là **đặt NaN** (coi là thiếu)
  rồi xử lý như buổi 10, hoặc giữ nguyên + biến giả. Và phải ghi lại bằng cờ.
- **(b)** Đo ngược lại: cắt cho MAPE **18,11%**, tệ hơn hẳn cách coi COVID là thiếu (**8,71%**), vì chỉ còn 18 tháng — không đủ để ước
  lượng 12 hệ số mùa vụ. "Dữ liệu cũ lỗi thời" là giả định, phải kiểm bằng backtest.
- **(c)** MAPE 8,71% là của **một** baseline thô trên **một** cửa sổ 12 tháng. Chưa có backtest rolling origin (buổi 15), chưa so với
  seasonal naive, chưa có khoảng dự báo. Chưa sẵn sàng.
- **(d)** Hampel dùng **mức địa phương**: quanh tháng 2020-04 thì mọi tháng lân cận đều thấp, nên điểm đó "bình thường" so với hàng xóm.
  Đó chính là lý do phải ghép Hampel (bắt AO) với phát hiện điểm gãy (bắt LS) — 2020-04 là một phần của **level shift**, không phải outlier
  điểm.

</details>
