# Kiểm tra buổi 11 — Ngoại lai và điểm gãy

## Nhắc lại khái niệm

**Câu 1.** Chuỗi $(10, 10, 10, 20, 15, 12, 11, 10)$ có loại bất thường nào?

- A. Điểm đơn (AO)
- B. Dịch mức
- C. Thay đổi tạm
- D. Đổi phương sai

<details>
<summary>Đáp án</summary>

**C** (mục 4.1): nhảy lên 20 rồi hồi dần 15, 12, 11, 10. **A sai**: điểm đơn thì điểm sau quay về 10 ngay. **B sai**: dịch mức thì ở lại 20.
**D sai**: mức đổi rồi hồi, không phải độ dao động đổi quanh một mức.

</details>

**Câu 2.** Trong mười số $(10, 12, 11, 13, 12, 50, 11, 12, 13, 12)$, vì sao ngưỡng $|z| > 3$ không gắn cờ số 50?

- A. Vì 50 không phải ngoại lai
- B. Vì chính số 50 kéo trung bình và độ lệch chuẩn lên, nên $z$ của nó chỉ khoảng 2,84
- C. Vì z-score chỉ dùng được cho số âm
- D. Vì phải dùng ngưỡng 2

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): masking. Với 10 số, $|z|$ còn không bao giờ vượt $9/\sqrt{10} \approx 2{,}85$. **A sai**: điểm MAD của 50 là 25,6. **C sai**:
z-score dùng cho mọi số. **D sai**: hạ ngưỡng thì bắt được 50 ở ví dụ này, nhưng sẽ gắn cờ oan nhiều điểm khác ở chuỗi lớn; cách đúng là dùng
MAD.

</details>

**Câu 3.** Winsorize khác xoá ở chỗ:

- A. Winsorize giữ mốc thời gian, kéo giá trị bị gắn cờ về trung vị địa phương
- B. Winsorize xoá cả dòng
- C. Winsorize chỉ dùng cho sự kiện thật
- D. Hai cách như nhau

<details>
<summary>Đáp án</summary>

**A** (mục 4.4). **B sai**: đó là xoá, làm thủng lưới thời gian. **C sai**: sự kiện thật thì **giữ nguyên**, không winsorize. **D sai**: xoá làm
mất mốc (chuỗi Tết mất 54 mốc), winsorize thì không.

</details>

**Câu 4.** Tăng penalty của PELT thì số điểm gãy:

- A. Tăng
- B. Giảm hoặc giữ nguyên
- C. Không liên quan
- D. Luôn bằng 0

<details>
<summary>Đáp án</summary>

**B** (mục 4.5): penalty là giá của mỗi điểm gãy; giá cao thì chỉ những điểm gãy giảm chi phí nhiều mới được giữ. Số điểm gãy tăng theo
penalty là dấu hiệu gọi sai API. **A sai**: ngược chiều. **C sai**: penalty chính là núm chỉnh số điểm gãy. **D sai**: chỉ khi penalty lớn hơn
mức giảm chi phí của mọi điểm gãy (hàng không EU: từ khoảng $5 \ln n$).

</details>

## Vận dụng

**Câu 5.** Sáu ngày lượt xem $(20, 21, 19, 20, 80, 20)$. Tính $z$ của 80 (độ lệch chuẩn chia $n - 1$) và điểm MAD của 80. Cách nào gắn cờ?

<details>
<summary>Đáp án</summary>

Trung bình 30, độ lệch chuẩn ≈ 24,5, $z$ = 50 / 24,5 ≈ **2,04**: không vượt 3 (với 6 số, $|z|$ tối đa là $5/\sqrt 6 \approx 2{,}04$). Trung vị
20; khoảng cách $(0, 1, 1, 0, 60, 0)$, trung vị 0,5; MAD = 1,4826 × 0,5 ≈ 0,74; điểm của 80 = 60 / 0,74 ≈ **81**: bị gắn cờ (mục 4.2, 4.3).
Nhầm hay gặp: tính MAD bằng trung bình các khoảng cách (10,3), bị chính số 80 kéo lên.

</details>

**Câu 6.** Một chuỗi có chi phí: không cắt 400; một điểm gãy 40; hai điểm gãy 34. PELT chọn mấy điểm gãy với penalty 10? Với penalty 3?

<details>
<summary>Đáp án</summary>

Penalty 10: tổng là 400, 40 + 10 = 50, 34 + 20 = 54 → **một** điểm gãy. Penalty 3: 400, 43, 34 + 6 = 40 → **hai** điểm gãy (mục 4.5). Điểm gãy
thứ hai chỉ giảm chi phí 6; nó được giữ khi penalty nhỏ hơn 6. Nhầm hay gặp: so chi phí mà quên cộng penalty cho **mỗi** điểm gãy.

</details>

**Câu 7.** Điện tiêu thụ của một toà nhà văn phòng giảm hẳn vào ngày Quốc khánh mỗi năm. Hampel gắn cờ những ngày đó. Làm gì với chúng khi
chuẩn bị dữ liệu dự báo?

<details>
<summary>Đáp án</summary>

Đưa các ngày Quốc khánh vào **nhật ký sự kiện** và giữ nguyên; khi dự báo thì thêm biến giả cho ngày lễ (mục 4.4). Đó là sự kiện thật, lặp lại,
biết trước; winsorize sẽ xoá đúng chỗ toà nhà cần dự báo thấp. Nhầm hay gặp: tin nhãn "ngoại lai" của thuật toán vì con số lệch lớn.

</details>

**Câu 8.** Một cửa hàng đóng cửa sửa chữa hai tháng, doanh số gần 0; mở lại thì bán như trước. Bạn cần dự báo năm sau. Chọn cách xử lý hai
tháng đó và nói vì sao.

<details>
<summary>Đáp án</summary>

**Coi là thiếu** (NaN, có cột cờ) rồi điền như buổi 10, hoặc thêm biến giả (mục 4.6). Hành vi sau đó quay về như cũ, và chỉ cần dự báo sau
gián đoạn, giống COVID với hàng không EU (8,71% so với 24,01% khi giữ nguyên). Giữ nguyên thì hai tháng gần 0 kéo mức và mùa vụ xuống. Nhầm
hay gặp: cắt bỏ mọi dữ liệu trước khi đóng cửa, mất gần hết mẫu.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Bảng quét penalty trên log hành khách hàng không EU:

| penalty / $\ln n$ | 0,5 | 1 | 2 | 3 | 4 | 5 | 10 |
|---|---|---|---|---|---|---|---|
| Số điểm gãy | 3 | 2 | 2 | 2 | 2 | 0 | 0 |

Một bạn chọn penalty $0{,}5 \ln n$ "để không bỏ sót" và báo 3 điểm gãy. Một bạn khác chọn $10 \ln n$ và báo "không có điểm gãy". Nhận xét.

<details>
<summary>Đáp án</summary>

Cả hai đều chọn ở mép. Kết quả **ổn định** là 2 điểm gãy, giữ nguyên trong cả khoảng 1–4 lần $\ln n$: đó là khoảng đáng tin (mục 4.5). Ở $0{,}5
\ln n$ phạt quá nhẹ nên thêm một điểm gãy chỉ đi theo dao động; ở $10 \ln n$ phạt quá nặng nên bỏ luôn sụt giảm −78,7% của COVID. Báo 2 điểm
gãy kèm khoảng penalty ổn định.

</details>

**Câu 10.** Báo cáo làm sạch lượt xem Wikipedia:

| Cách | Số ngày gắn cờ | Quyết định của nhóm |
|---|---|---|
| 3σ toàn chuỗi | 16 (0,44%) | "Dữ liệu rất sạch, chỉ cần xoá 16 ngày" |
| STL robust (mùa vụ tuần) | 616 (16,86%) | "Loại 17% dữ liệu bẩn" |

Chỉ ra lỗi của từng quyết định.

<details>
<summary>Đáp án</summary>

(1) 3σ toàn chuỗi mù trước xu hướng và masking: 16 ngày đó dồn vào vùng mức cao, nói "những ngày này đông" chứ không phải "bất thường"; và
**xoá** thì thủng mốc, phải winsorize (mục 4.2–4.4). (2) STL robust gắn cờ một phần sáu số ngày vì phần dư còn mùa vụ năm mà mùa vụ tuần không
giải thích được; một ngưỡng gắn cờ 17% dữ liệu là ngưỡng sai, không phải dữ liệu bẩn (mục 4.3). Nên dùng Hampel (121 ngày, 3,3%) và nhật ký sự
kiện.

</details>
