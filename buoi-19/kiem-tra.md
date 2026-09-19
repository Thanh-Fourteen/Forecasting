# Kiểm tra buổi 19 — Nhu cầu gián đoạn

## Nhắc lại khái niệm

**Câu 1.** Dự báo của Croston cho một mã phụ tùng là 0,3. Con số này nghĩa là:

- A. Tháng sau chắc chắn bán 0 món vì 0,3 làm tròn thành 0
- B. Tốc độ bán trung bình 0,3 món mỗi tháng; quyết định nhập hàng dùng tổng qua nhiều tháng
- C. Xác suất tháng sau có bán là 30%
- D. Mô hình sai vì số món phải là số nguyên

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): dự báo chuỗi gián đoạn là tốc độ bán; 10 tháng bán 3 món là tốc độ 0,3. **A sai**: làm tròn từng tháng làm mất hết lượng
bán; mức nhập hàng tính trên tổng nhiều tháng. **C sai**: 0,3 là số món, không phải xác suất; TSB mới tách riêng xác suất có bán. **D sai**:
tốc độ trung bình không cần là số nguyên, như "trung bình 2,4 con mỗi gia đình".

</details>

**Câu 2.** Một mã phụ tùng ngừng bán hẳn từ 12 tháng nay. Phương pháp nào tự hạ dự báo về gần 0?

- A. Croston
- B. SBA
- C. TSB
- D. Cả ba như nhau

<details>
<summary>Đáp án</summary>

**C** (mục 4.4): TSB làm trơn xác suất có bán ở **mọi** tháng, nên mỗi tháng 0 kéo dự báo xuống. **A sai**: Croston chỉ cập nhật khi có bán,
dự báo đứng yên sau lần bán cuối (mã T1002 đứng ở 0,34 suốt 33 tháng). **B sai**: SBA là Croston nhân 1 − α/2, cũng đứng yên. **D sai**: vì
A, B đứng yên.

</details>

**Câu 3.** Trên chuỗi nhiều số 0, chỉ số nào dễ chọn "dự báo toàn 0" làm tốt nhất?

- A. RMSSE
- B. MAE và MASE
- C. Chi phí tồn kho mô phỏng
- D. Tỷ lệ đáp ứng

<details>
<summary>Đáp án</summary>

**B** (mục 4.2): MAE ưa trung vị, mà trung vị của chuỗi 76% số 0 là 0; trên Car Parts, "Zero" có MASE tốt nhất (0,820). **A sai**: RMSE ưa
trung bình, tức tốc độ bán (dù trên dữ liệu này RMSSE vẫn xếp Zero trên AutoETS). **C sai**: Zero có chi phí 43,4, gần cao nhất, vì thiếu
hàng mọi tháng. **D sai**: tỷ lệ đáp ứng của Zero là 0%.

</details>

**Câu 4.** Ngưỡng ADI 1,32 và CV² 0,49 của Syntetos–Boylan được tính ra để làm gì?

- A. Chọn giữa Croston và SBA
- B. Chọn giữa mọi mô hình dự báo
- C. Quyết định mức tồn kho
- D. Phát hiện mặt hàng ngừng bán

<details>
<summary>Đáp án</summary>

**A** (mục 4.1): ngưỡng được tính để biết khi nào Croston hay SBA sai ít hơn. **B sai**: dùng bảng để chọn mô hình khác thì không có căn cứ; trên
Car Parts, Croston thua dù gần hết mã là "gián đoạn". **C sai**: mức tồn kho tính bằng quantile của nhu cầu qua thời gian dẫn (mục 4.6). **D
sai**: ADI tính trên cả chuỗi, không cho biết mã đã ngừng bán gần đây; TSB mới phản ứng với điều đó.

</details>

## Vận dụng

**Câu 5.** Tám tháng $(0, 4, 0, 0, 0, 2, 0, 0)$. Tính ADI, CV² và cho biết nhóm.

<details>
<summary>Đáp án</summary>

Có bán 2 tháng: ADI = 8/2 = **4**. Lượng 4 và 2: trung bình 3, độ lệch chuẩn 1, CV² = (1/3)² ≈ **0,11**. ADI ≥ 1,32 và CV² < 0,49: nhóm **gián
đoạn** (mục 4.1). Nhầm hay gặp: tính CV² trên cả 8 tháng kể cả số 0; CV² chỉ dùng lượng khi có bán.

</details>

**Câu 6.** Cùng chuỗi câu 5, α = 0,5 cho mọi SES (mức đầu = số đầu). Tính dự báo Croston, SBA và TSB.

<details>
<summary>Đáp án</summary>

Lượng: 4 → 0,5 × 2 + 0,5 × 4 = **3**. Khoảng: lần đầu ở tháng 2 (khoảng 2), lần sau cách 4 → 0,5 × 4 + 0,5 × 2 = **3**. Croston 3/3 = **1,0**;
SBA 1,0 × 0,75 = **0,75**. TSB: dãy có bán (0, 1, 0, 0, 0, 1, 0, 0), SES từ 0: 0,5; 0,25; 0,125; 0,0625; 0,53; 0,27; **0,133**; nhân lượng 3:
**0,40** (mục 4.3–4.4). Nhầm hay gặp: bỏ khoảng đầu tiên (tính từ đầu chuỗi).

</details>

**Câu 7.** Tốc độ dự báo 0,6 món/tháng, thời gian dẫn 1 tháng (nên $S$ phải đủ 2 tháng), chi phí thiếu 9, tồn 1. Theo Poisson với trung bình
1,2, xác suất bán tối đa 0, 1, 2, 3 món là 0,301; 0,663; 0,879; 0,966. Mức $S$ bằng bao nhiêu?

<details>
<summary>Đáp án</summary>

Quantile mức 9/(9 + 1) = 0,9 → cột đầu tiên đạt ≥ 0,9 là **3** (0,966); 2 món chỉ đủ 87,9% trường hợp (mục 4.6). Nhầm hay gặp: dùng
trung bình 1,2 làm tròn thành 1; hoặc chỉ tính cho 1 tháng (trung bình 0,6), quên tháng chờ hàng về.

</details>

**Câu 8.** $S$ = 2 mọi tháng, đầu kỳ có 2 món. Hàng đặt cuối tháng $t$ về đầu tháng $t + 2$. Nhu cầu 3 tháng là (0, 3, 1). Tính tồn, thiếu,
chi phí ($C_o$ = 1, $C_u$ = 9) và tỷ lệ đáp ứng.

<details>
<summary>Đáp án</summary>

Tháng 1: không ai hỏi, tồn 2, đặt 2 − 2 = 0. Tháng 2: có 2, khách hỏi 3, bán 2, thiếu 1, tồn 0, đặt 2 − 0 − 0 = 2 (về đầu tháng 4). Tháng 3:
chưa có hàng về, khách hỏi 1, thiếu 1. Tồn 2 + 0 + 0 = **2**, thiếu **2**: chi phí 2 + 18 = **20**; đáp ứng 2/4 = **50%** (mục 4.6). Nhầm hay
gặp: cho món đặt cuối tháng 2 về kịp bán trong tháng 3.

</details>

## Đọc biểu đồ / bảng kết quả — tìm chỗ sai

**Câu 9.** Một báo cáo chọn mô hình nhập hàng cho 2.674 mã phụ tùng:

| Mô hình | MAE | MAPE (bỏ tháng bán 0) |
|---|---|---|
| Zero | **0,402** | 100% |
| IMAPA | 0,546 | 61,1% |
| TSB | 0,578 | **56,5%** |

"Theo MAE, dùng Zero; nếu sếp thích phần trăm thì dùng TSB." Chỉ ra lỗi và nói phải chấm thế nào.

<details>
<summary>Đáp án</summary>

(1) MAE ưa trung vị, trung vị của chuỗi thưa là 0: Zero thắng MAE nhưng không bao giờ nhập hàng, tỷ lệ đáp ứng 0%, chi phí 43,4 so với 29,6
của IMAPA (mục 4.2, 4.6). (2) MAPE bỏ tháng 0 chỉ chấm khoảng một phần tư số tháng, bỏ qua mọi tháng mà dự báo cao làm tồn kho. Phải chấm bằng
RMSSE và chi phí tồn kho mô phỏng; trên dữ liệu này cả hai chọn IMAPA. Nhầm hay gặp: tin chỉ số có vẻ "chuẩn" mà không hỏi nó phục vụ quyết
định nào.

</details>

**Câu 10.** Một đồng nghiệp viết: "Phân loại SBC cho 2.231 mã là 'gián đoạn', nên dùng Croston." Bảng backtest:

| Mô hình | RMSSE | Chi phí mỗi mã |
|---|---|---|
| Croston | 0,827 | 37,9 |
| TSB | 0,684 | 31,0 |
| trung bình lịch sử | 0,738 | 33,9 |

Nhận xét và giải thích vì sao Croston thua.

<details>
<summary>Đáp án</summary>

Ngưỡng SBC chỉ để chọn giữa Croston và SBA, không phải giữa mọi mô hình (mục 4.1); bảng cho thấy Croston thua cả trung bình lịch sử ở cả hai
thước đo. Lý do: nhiều mã ngừng bán giữa chừng; Croston chỉ cập nhật khi có bán nên giữ dự báo cũ và nhập hàng không ai mua, còn TSB hạ xác
suất có bán mỗi tháng 0 (mục 4.4). Phải chọn bằng backtest và chi phí. Nhầm hay gặp: coi bảng phân loại là quy tắc chọn mô hình.

</details>
