# Kiểm tra buổi 9 — Đặc trưng chuỗi và khả năng dự báo

10 câu. Tự làm trước, mở đáp án sau.

---

**1 (nhắc lại).** Entropy phổ nhận giá trị trong khoảng nào, và giá trị gần 1 nghĩa là gì?

<details><summary>Đáp án</summary>

Trong $[0, 1]$ vì đã chia cho $\ln N_{\text{bin}}$. Gần 1 = phổ trải đều trên mọi tần số (giống nhiễu trắng) → chuỗi **khó dự báo**. Gần 0
= năng lượng dồn vào vài tần số (xu hướng/mùa vụ mạnh) → dễ dự báo. Đại lượng $\Omega = 1 - H$ là forecastability của ForeCA.

</details>

---

**2 (nhắc lại).** Vì sao phải bỏ bin tần số 0 khi chuẩn hoá phổ thành phân phối xác suất?

<details><summary>Đáp án</summary>

Bin tần số 0 là mức trung bình (DC). Nếu giữ lại, chuỗi có mức lớn sẽ có toàn bộ "xác suất" dồn vào bin 0 và entropy ≈ 0 bất kể chuỗi
nhiễu hay không — đặc trưng sẽ phụ thuộc đơn vị đo. Trong code còn trừ trung bình trước khi gọi Welch.

</details>

---

**3 (nhắc lại).** MASE được chuẩn hoá bằng gì, và điều đó khiến nó phù hợp với so sánh nào, không phù hợp với so sánh nào?

<details><summary>Đáp án</summary>

Chia cho MAE của naive (mùa vụ) tính **trong mẫu huấn luyện của chính chuỗi đó**. Phù hợp: so **nhiều mô hình trên cùng một chuỗi**, và
gộp sai số qua nhiều chuỗi khác thang. Không phù hợp: so **độ khó giữa các chuỗi** — vì mẫu số đã chứa đúng phần khó ấy.

</details>

---

**4 (nhắc lại).** Nêu ba đặc trưng phụ thuộc đơn vị đo và cách xử lý trước khi đưa vào PCA.

<details><summary>Đáp án</summary>

Trung bình, độ lệch chuẩn, độ dốc xu hướng (và mọi đặc trưng tính bằng đơn vị gốc). Xử lý: hoặc bỏ ra, hoặc chuyển sang dạng tương đối
(hệ số biến thiên = sd/mean), và **luôn** `StandardScaler` trước PCA. Nếu không, PC1 chỉ là "chuỗi to hay nhỏ".

</details>

---

**5 (vận dụng).** Bạn tính tương quan giữa một đặc trưng mới và MASE của seasonal naive trên 4.000 chuỗi, được r = 0,01. Bạn kết luận gì,
và làm gì tiếp?

<details><summary>Đáp án</summary>

**Chưa kết luận được gì.** MASE của seasonal naive tự triệt tiêu độ khó (trung vị ≈ 1,0 ở mọi nhóm entropy). Việc cần làm: tính lại với
sMAPE (hoặc MAE chuẩn hoá theo trung bình chuỗi, hoặc skill score so với một baseline **khác** mô hình đang chấm), và báo cả Spearman.
Trong buổi này entropy có r = −0,05 với MASE nhưng +0,25 với sMAPE.

</details>

---

**6 (vận dụng).** Hai chuỗi doanh thu có cùng hình dạng mùa vụ, một chuỗi trung bình 10.000, một chuỗi 100. Bạn phân cụm DTW và chúng vào
hai cụm khác nhau. Sai ở đâu, sửa thế nào, và kiểm chứng ra sao?

<details><summary>Đáp án</summary>

Sai: DTW so **giá trị tuyệt đối** nên khoảng cách bị chi phối bởi mức. Sửa: z-score từng chuỗi ($(y-\bar y)/s$) trước khi tính ma trận
khoảng cách. Kiểm chứng: (a) nhân một chuỗi với 100 → nhãn cụm không đổi; (b) in mức trung vị theo cụm — nếu nó tăng đều theo số hiệu cụm
thì vẫn đang cụm theo độ lớn.

</details>

---

**7 (vận dụng).** Sếp yêu cầu tune mô hình cho toàn bộ 4.000 chuỗi trong một tuần. Bạn dùng kết quả buổi này để đề xuất gì, kèm số liệu?

<details><summary>Đáp án</summary>

Phân tầng: 137 chuỗi có entropy ≥ 0,666 **và** $F_S$ < 0,4 (sMAPE trung vị của baseline **18,11%**) — gần nhiễu, khoảng cách giữa mô hình
tốt nhất và baseline rất hẹp → dùng seasonal naive + khoảng dự báo rộng, không tune. 3.863 chuỗi còn lại (sMAPE trung vị **6,05%**) mới
đáng đầu tư. Kết hợp thêm ABC: nhóm A chiếm 74,7% doanh thu → ưu tiên ô AX.

</details>

---

**8 (vận dụng).** Một chuỗi làm `kpss` ném `ValueError: cannot convert float NaN to integer`. Nguyên nhân là gì, xử lý thế nào trong một
pipeline chạy 48.000 chuỗi?

<details><summary>Đáp án</summary>

Chuỗi **hằng** (độ lệch chuẩn 0) → thống kê KPSS chia cho 0. Xử lý: bọc try/except, trả NaN, và **giữ NaN như một cờ phát hiện chuỗi lạ**
(mẫu 4.000 chuỗi có 1 chuỗi như vậy). Không được im lặng thay bằng 0 — như thế là giấu mất chuỗi hỏng.

</details>

---

**9 (đọc biểu đồ).** Hình `entropy-sai-so.png`: ô trái có đường trung vị đi lên 5,38 → 4,87 → 5,15 → 6,11 → 12,04; ô phải có đường trung
vị nằm ngang 1,02 / 0,95 / 1,01 / 1,02 / 1,02. Một đồng nghiệp nói "hai hình mâu thuẫn nhau, chắc có bug". Bạn trả lời thế nào? Và giải
thích riêng vì sao nhóm Q2 (4,87%) lại thấp hơn Q1 (5,38%)?

<details><summary>Đáp án</summary>

Không mâu thuẫn: **cùng một dự báo, hai thước đo khác mẫu số**. MASE chia cho sai số in-sample của chính seasonal naive, nên chuỗi càng
khó thì cả tử và mẫu cùng lớn → tỷ số giữ nguyên ≈ 1. sMAPE không chuẩn hoá theo baseline nên phản ánh độ khó.

Q2 < Q1: quan hệ entropy–sMAPE **không đơn điệu** ở vùng entropy thấp. Đo trung vị theo nhóm cho thấy nguyên nhân: Q1 có độ mạnh xu hướng
**0,994** (cao nhất) nhưng độ mạnh mùa vụ chỉ **0,455** (thấp nhất trong Q1–Q4), và hệ số biến thiên 0,140 so với 0,100 của Q2. Phổ dồn
vào tần số thấp vì **xu hướng**, nên entropy nhỏ — nhưng seasonal naive lặp lại chu kỳ cũ và bỏ qua drift, nên nó dự báo chuỗi xu hướng
mạnh kém hơn chuỗi mùa vụ mạnh. Bài học: entropy đo "ngẫu nhiên", không đo "sai số của một baseline cụ thể".

</details>

---

**10 (đọc bảng — tìm chỗ sai).** Một báo cáo nội bộ viết:

| Kết luận | Bằng chứng |
|---|---|
| (a) "Hệ số biến thiên là thước đo độ khó dự báo; mọi mã hàng nhóm Z cần mô hình phức tạp." | CV trung vị nhóm Z = 1,4 |
| (b) "Bộ 782 đặc trưng của tsfresh tốt hơn 20 đặc trưng tự viết vì nhiều thông tin hơn." | số đặc trưng |
| (c) "Entropy phổ của chúng tôi là 0,42, thấp hơn 0,55 trong bài báo X, nên dữ liệu của chúng tôi dễ hơn." | hai con số |
| (d) "PCA cho thấy chuỗi dài nằm tách biệt — đó là một phân khúc khách hàng riêng." | hình PCA |

Chỉ ra chỗ sai của từng dòng.

<details><summary>Đáp án</summary>

- **(a)** CV đo **biến động**, không đo **độ khó**. Chuỗi mùa vụ mạnh, không nhiễu, có CV lớn nhưng cực dễ dự báo (ví dụ của Kourentzes).
  Đo được trong buổi: CV × MASE(snaive) có Spearman chỉ −0,11. Thay trục XYZ bằng **sai số thật của baseline**.
- **(b)** Nhiều đặc trưng ≠ nhiều thông tin: phần lớn tương quan chặt với nhau. catch22 rút từ **4.791** xuống **22** mà vẫn giữ được
  hiệu năng phân loại. Muốn so thì phải so trên một nhiệm vụ hạ nguồn cụ thể.
- **(c)** Hai entropy tính bằng **phương pháp khác nhau** (Welch với `nperseg` nào? periodogram?) và trên **độ dài khác nhau** thì không
  so trực tiếp được. Phải nêu phương pháp + tham số, và tốt nhất là tính lại cả hai bằng cùng một hàm.
- **(d)** Nhiều đặc trưng (acf10, entropy, spike) phụ thuộc **độ dài chuỗi**; nếu không cắt về cùng độ dài thì PCA đang vẽ độ dài chứ
  không phải hành vi khách hàng. Buổi này cắt mọi chuỗi về 120 điểm cuối trước khi trích đặc trưng.

</details>
