# Chuẩn dễ hiểu — cách viết tài liệu học viên đọc

Áp dụng cho mọi `tai-lieu.md`, `kiem-tra.md`, `code/README.md`, đề dự án, phụ lục. Tóm tắt 12 quy tắc nằm ở
`todos/quy-uoc.md` mục "Chuẩn dễ hiểu". File này có **chi tiết + ví dụ trước/sau lấy từ tài liệu thật + bài mẫu + prompt đọc
thử**. Căn cứ nghiên cứu: `tools/NGHIEN-CUU-SU-PHAM.md`.

**Người đọc:** biết Python cơ bản và toán phổ thông; **chưa** học thống kê đại học; **chưa** biết forecasting; tự
học một mình. **Tiêu chí:** đọc xong không phải tra ngoài.

**Vì sao có chuẩn này:** người dùng tự học buổi 1–13 và phải hỏi ChatGPT mới hiểu. Đọc thử bản cũ buổi 1, 7, 12
cho **9–12 chỗ chặn mỗi buổi**. Phần lớn là khái niệm thống kê nền (phân phối, quantile, phương sai, tương quan, kiểm
định) được dùng mà không định nghĩa. Mẫu chuẩn mục 4.8 buổi 1 viết theo file này còn **0 chỗ chặn**.

---

## Nhãn cố định (bộ kiểm `tools/kiem_de_hieu.py` tìm đúng các chữ này)

| Nhãn | Đặt ở đâu | Quy tắc |
|---|---|---|
| `### Từ mới trong buổi` + bảng | đầu mục 4 Lý thuyết | D1 |
| `> **Mượn trước — <khái niệm>**` (blockquote) | chỗ đầu tiên dùng khái niệm của buổi sau | D5 |
| `**Ví dụ số nhỏ — tự tính tay.**` | trong mỗi khái niệm, trước dữ liệu thật | D2 |
| `**Nói bằng lời.**` | ngay sau danh sách ký hiệu của công thức `$$…$$` | D3 |
| `**Cách đọc hình.**` + danh sách 5 bước | ngay dưới mỗi ảnh | D8 |
| `**Đọc bảng.**` | ngay dưới mỗi bảng có nhiều ô số | D8 |
| `**Tóm lại.**` | cuối mỗi mục `###` của Lý thuyết | D2 |
| `**Tự kiểm tra.**` + `<details>` | cuối mỗi mục `###` của Lý thuyết | D10 |
| `> **Nâng cao — có thể bỏ qua lần đọc đầu.**` | phần học thuật, lịch sử, dạng tổng quát | D9 |
| `**Mục đích:**` và `**Đọc kết quả:**` | trong mỗi `### Bước` của mục 5 Lab | D11 |

`tools/xuat_pdf.py` tô các nhãn này thành hộp riêng (nét đứt cho "Mượn trước", khung đậm cho "Tóm lại", nét đôi
cho "Nâng cao"). In đen trắng vẫn phân biệt được.

---

## D1 — Từ mới: định nghĩa ngay lần đầu

Lần đầu một thuật ngữ xuất hiện, định nghĩa nó **ngay trong câu đó hoặc câu kế**: 1–2 câu bằng lời thường, kèm một
ví dụ đời thường. Thuật ngữ tiếng Anh giữ nguyên, nhưng lần đầu phải có nghĩa tiếng Việt. Đầu mục Lý thuyết có
bảng "Từ mới trong buổi" (thuật ngữ · nghĩa một câu · ví dụ), lấy từ Phụ lục E. Gặp từ không có trong E thì thêm
vào E trước.

**Trước** (buổi 12, mục 1):

> Đọc được **phổ công suất** (Welch) để thấy chu kỳ nào mạnh…

Người đọc thử: *"Tôi chưa biết phương sai, nên câu định nghĩa phổ công suất với tôi là rỗng."*

**Sau:**

> Đọc được **phổ công suất** (power spectrum): bảng cho biết mỗi nhịp lên xuống của chuỗi (nhịp 24 giờ, nhịp 7 ngày…)
> mạnh tới đâu. Ví dụ: chuỗi điện theo giờ có một cột rất cao ở chu kỳ 24 giờ, vì ngày nào cũng lên xuống giống nhau.

---

## D2 — Khuôn một khái niệm

Mỗi khái niệm chính đi theo thứ tự dưới đây. Bước nào không hợp thì bỏ, nhưng **không đảo thứ tự**.

| Bước | Viết gì | Vì sao |
|---|---|---|
| 1. Vấn đề | câu hỏi thực tế nào cần khái niệm này | người đọc biết học để làm gì |
| 2. Trực giác | ví dụ đời thường (người bán bánh, lịch trực…) | nối với cái đã biết |
| 3. **Ví dụ số nhỏ** | 5–10 số, **tự tính tay được**, tính mẫu ít nhất một dòng | worked example, người mới học nhanh nhất từ đây |
| 4. Hình | nếu có, kèm "Cách đọc hình" | |
| 5. Công thức | kèm danh sách ký hiệu | chỉ đến sau khi đã hiểu bằng số |
| 6. Nói bằng lời | một câu, có thay số | ý không bị kẹt trong ký hiệu |
| 7. NumPy | code ngắn cho **chính ví dụ số nhỏ** ở bước 3, in ra đúng số đã tính tay | nối tay ↔ máy |
| 8. Thư viện | hàm có sẵn, lưu ý chỗ khác với cách tính tay | |
| 9. Dữ liệu thật | con số từ lần chạy thật | |
| 10. Tóm lại + Tự kiểm tra | 1–3 câu in đậm + 1 câu hỏi | |

Dùng **một bộ số xuyên suốt** từ bước 3 tới bước 7 (concreteness fading: cụ thể → hình → ký hiệu, có câu nối rõ
giữa các bậc).

**Trước:** buổi 1 mục 4.8 bản cũ, 12 dòng. Công thức $Q^\ast = F^{-1}(C_u/(C_u+C_o))$ đứng ở dòng thứ hai. Không có ví dụ
số nhỏ, không định nghĩa quantile. **Sau:** bài mẫu ở cuối file này.

---

## D3 — Công thức: ký hiệu ngay dưới, rồi một câu nói bằng lời có thay số

PDF vẽ công thức thành ảnh. Từ 2026-09-18, `xuat_pdf.py` có thêm lớp chữ ẩn để copy được LaTeX, nhưng người đọc vẫn
cần câu chữ. Vì vậy công thức **không bao giờ mang ý chính một mình**.

**Trước** (buổi 7, mục 4.1):

> Tự hiệp phương sai ở độ trễ $k$: $c_k = \frac{1}{T}\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)$. ACF là $r_k=c_k/c_0$.

Người đọc thử: *"$T$ và $\bar y$ không được giải thích; không có câu nói bằng lời."*

**Sau:**

> $$c_k = \frac{1}{T}\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)$$
>
> - $T$: số quan sát của chuỗi. $\bar y$: trung bình của chuỗi.
> - $y_t - \bar y$: giá trị ở thời điểm $t$ cao hơn (dương) hay thấp hơn (âm) trung bình bao nhiêu.
> - $k$: độ trễ, tức so mỗi điểm với điểm cách nó $k$ bước về trước.
>
> **Nói bằng lời.** Lấy độ lệch khỏi trung bình của mỗi điểm, nhân với độ lệch của điểm cách nó $k$ bước, cộng
> lại rồi chia cho $T$. Với chuỗi 4, 6, 8, 6: trung bình 6, độ lệch −2, 0, 2, 0. Ở trễ 1, các tích là
> 0 × (−2), 2 × 0, 0 × 2, đều bằng 0, nên $c_1 = 0$. Hai điểm liền nhau không "cùng lên cùng xuống".

---

## D4 — Không nói lửng

"Thiếu", "thừa", "sai số dương", "cao hơn", "tốt hơn", "giảm 18%" luôn phải nói rõ **so với cái gì, đơn vị gì**.
Quy ước dấu (**sai số = thực tế − dự báo**) nhắc lại mỗi lần dùng dấu.

**Trước** (buổi 1, ô 6 phiếu bài toán):

> thiếu: mua giá giao ngay ≈ 4 lần; thừa: bán lại lỗ ≈ 1 lần

Người dùng hỏi ChatGPT: *"Thiếu là thiếu gì?"* Người đọc thử: *"4 lần so với cái gì? Giá giao ngay gấp 4 thì mỗi kWh
chỉ mất thêm 3?"*

**Sau:**

> mỗi kWh thiếu phải mua gấp giá giao ngay, mất khoảng 4 đồng; mỗi kWh thừa bán lại lỗ khoảng 1 đồng

và ở mục 4.8: *"Nếu mua **ít hơn** lượng nhà thật sự dùng, phần còn thiếu phải mua gấp… Sai số dương nghĩa là thực
tế cao hơn dự báo; khi đó mua đúng bằng dự báo sẽ **thiếu**."*

---

## D5 — Chưa dạy thì chưa dùng; buộc dùng thì "Mượn trước"

Khái niệm của buổi sau: không dùng. Nếu không tránh được thì mở hộp "Mượn trước": 2–4 câu, một ví dụ số nhỏ, và
"buổi N học kỹ" (chỉ nhắc tên buổi, không trỏ đường dẫn file — mỗi buổi tự chứa). Khái niệm của **buổi trước** thì
nhắc lại ở mục 2 "Nhắc lại buổi trước", đủ để không phải mở buổi cũ.

**Trước** (buổi 1 bản cũ): *"Nếu $F$ là phân phối của lượng điện, lượng mua tốt nhất là **quantile**"*, trong khi
buổi 2 mới dạy quantile.

**Sau:**

> **Mượn trước — phân phối và quantile** (buổi 2 học kỹ)
>
> - **Quantile** (phân vị) mức 0,8: giá trị nhỏ nhất mà ít nhất 80% số giá trị nhỏ hơn hoặc bằng nó.
> - Xếp 5, 6, 6, 7, 7, 8, 8, **9**, 9, 12. Vị trí 0,8 × 10 = 8, số thứ 8 là 9, nên quantile 0,8 là 9 kWh.

Kiến thức thống kê nền mà đọc thử báo chặn ở **cả ba** buổi 1, 7, 12: phân phối, quantile, trung vị, phương sai, độ
lệch chuẩn, tương quan, kiểm định (H0, p-value, mức ý nghĩa), ký hiệu của MAE/RMSE. Buổi 2 dạy kỹ. Mọi buổi sau
dùng thì nhắc lại ở mục 2 hoặc trong hộp "Mượn trước".

---

## D6 — Không chen trích tiếng Anh

Diễn giải bằng tiếng Việt, nguồn ghi gọn trong ngoặc (FPP §5.2). Chỉ trích nguyên văn khi câu chữ gốc quan trọng,
tối đa 1 lần mỗi mục, và phải kèm bản dịch trong cùng đoạn (`dịch:` hoặc `nghĩa là`). Lịch sử, tên bài báo, định lý
đưa vào "Đọc thêm" hoặc hộp "Nâng cao".

**Trước** (buổi 7, mục 4.4):

> Zivot: ADF có "very low power against I(0) alternatives that are close to being I(1)".

Người đọc thử: *"'power', I(0), I(1) không giải thích; tôi không rút ra được ý."*

**Sau:**

> ADF hay **bỏ sót**: khi chuỗi thật ra dừng nhưng rất gần một random walk, ADF thường vẫn không bác bỏ được giả
> thuyết "không dừng" (Zivot). Vì vậy "ADF không bác bỏ" chưa đủ để kết luận chuỗi không dừng.

---

## D7 — Mật độ: câu ngắn, ít số kết quả mỗi đoạn

- Câu ≤ ~30 chữ; một ý một câu. Bộ kiểm cảnh báo câu > 40 chữ.
- Một đoạn ≤ 3 con số **kết quả**. Nhiều hơn thì làm bảng. Phép tính từng bước (có +, ×, =, →) và dãy dữ liệu của
  ví dụ nhỏ không tính vào ngưỡng này. Ngưỡng 3 là quy ước của khoá, không lấy từ nghiên cứu.
- Không viết tắt tự chế: "TB 4 tuần" → "trung bình 4 tuần". Viết tắt chuyên môn (MAE, ACF) phải có trong bảng "Từ
  mới" hoặc Phụ lục E.

**Trước** (buổi 1, mục 4.4, một đoạn "Đọc hình." chứa **34 con số**):

> Mỗi năm có một "chữ U": tháng 1–2/2007 trung bình 35,5 kWh/ngày, tháng 6/2007 là 19,8. Dải cam là tháng 8 — năm nào
> cũng là đáy: trung bình tháng 8 là 18,3 (2007), 6,6 (2008), 15,8 (2009), 14,1 (2010). Tháng 8/2008 từ ngày 6 tới 30…

**Sau:**

> Mỗi năm có một "chữ U": mùa đông cao, mùa hè thấp, và tháng 8 luôn là đáy.
>
> | Tháng | 1–2/2007 | 6/2007 | 8/2007 | 8/2008 | 8/2009 | 8/2010 |
> |---|---|---|---|---|---|---|
> | Trung bình (kWh/ngày) | 35,5 | 19,8 | 18,3 | 6,6 | 15,8 | 14,1 |
>
> **Đọc bảng.** Tháng 8/2008 thấp bất thường, chưa bằng một nửa các tháng 8 khác. Nhà gần như vắng người (kỳ nghỉ hè).

---

## D8 — "Cách đọc hình" và "Đọc bảng"

**Cách đọc hình** luôn đủ 5 bước, theo đúng thứ tự:

1. **Trục ngang** là gì (đơn vị).
2. **Trục dọc** là gì (đơn vị).
3. **Ký hiệu**: màu, đường, chấm, vạch nào là gì.
4. **Nhìn vào đâu**: chỉ đúng vùng trên hình.
5. **Kết luận**: một câu, trùng với tiêu đề hình.

**Đọc bảng** nói **so dòng nào với dòng nào, kết luận gì, vì sao**. Không đọc lại từng ô: bảng đã có số, viết lại
bằng chữ là thừa (redundancy, Sweller 2019).

**Trước** (buổi 1 bản cũ, dưới hình chi phí):

> **Đọc hình.** Bên trái: cộng thêm càng nhiều thì chi phí giảm tới đáy quanh 0,45–0,5 rồi tăng lại; vạch cam (0,455 —
> tính chỉ từ năm 2009) rơi gần đúng đáy. Bên phải: cùng các mức đó, MAE tăng đều. Chi phí giảm 18,6% trong khi MAE xấu
> đi 37%. Tỷ lệ giờ dự báo thiếu 20,1% gần đúng $1 - 0{,}8$ — dấu hiệu quantile đã hiệu chỉnh tốt.

Không nói trục là gì, không có đơn vị chi phí, dồn 7 con số, dùng "hiệu chỉnh" chưa định nghĩa. **Sau:** xem bài mẫu.

---

## D9 — Tối đa 6 khái niệm chính mỗi buổi

Đếm các mục `###` trong Lý thuyết (không kể "Từ mới" và "Nâng cao"). Quá 6 thì chọn cái giữ; phần còn lại chuyển
vào hộp "Nâng cao — có thể bỏ qua lần đọc đầu" hoặc "Đọc thêm", hoặc bỏ. **Không nén chữ để nhét vừa.** Ngưỡng 6 là
quy ước của khoá.

**Trước:** buổi 1 có 10 mục lý thuyết (4.1–4.10), trung bình 400 chữ mỗi mục. **Sau (Phase 6 làm):** gộp 4.1–4.2
(dự báo là gì, cái gì dự báo được), giữ 4.3 phiếu bài toán, 4.5 baseline, 4.6 sai số ảo, 4.7 độ chi tiết, 4.8 chi phí
lệch. Chuyển 4.9 (M1–M6) và 4.10 (bản đồ cách tiếp cận) sang "Nâng cao"/"Đọc thêm".

---

## D10 — "Tự kiểm tra" cuối mỗi mục

Một câu hỏi vận dụng (không phải nhắc lại định nghĩa), đáp án trong `<details>`. Đáp án nêu cả **nhầm lẫn hay gặp**.
Luyện tập bằng câu hỏi là một trong hai kỹ thuật học hiệu quả nhất (Dunlosky et al. 2013).

**Ví dụ** (bài mẫu): *"Tiệm bánh: thừa mất 3 nghìn/cái, thiếu mất 1 nghìn/cái — quantile nào?"* Đáp án: 0,25, và
"nhầm hay gặp là đảo $C_u$ và $C_o$, ra 0,75".

---

## D11 — Lab: nói trước làm gì, nói sau thấy gì nghĩa là gì

Mỗi `### Bước` có:

- **Mục đích:** bước này để làm gì, sẽ thấy gì.
- Lệnh hoặc code.
- **Đọc kết quả:** thấy X nghĩa là Y; thấy Z thì kiểm lại gì.

**Trước** (buổi 1, Bước 2):

> Đọc chuỗi bằng `doc_dien_theo_gio()` (34.464 giờ, thiếu 431), gộp lên ngày bằng `resample("D").sum(min_count=20)`,
> vẽ. Viết 5 câu hỏi về dữ liệu *trước* khi đọc mục 4.4.

Người đọc thử: *"`min_count=20` nghĩa là gì, vì sao là 20? Người đọc theo thứ tự thì đã đọc xong 4.4 rồi."*

**Sau:**

> **Mục đích:** nhìn toàn bộ 4 năm trên một hình để đặt câu hỏi trước khi làm mô hình.
>
> ```python
> ngay = s.resample("D").sum(min_count=20)   # ngày nào có dưới 20 giờ đo được thì để trống, không cộng thiếu
> ```
>
> **Đọc kết quả:** đường bị đứt ở vài chỗ, ví dụ 18–21/8/2010 (mục 4.4: 10 ngày không có giờ nào đủ số đo). Đó
> là mất tín hiệu, không phải nhà dùng 0 kWh. Nếu thấy những ngày 0 kWh thì bạn đã quên `min_count`.

---

## D12 — Quiz: đáp án giải thích vì sao

Đáp án nói **vì sao đúng** và **vì sao từng lựa chọn khác sai**. Câu hỏi trả lời được chỉ bằng tài liệu buổi đó.
Feedback nên nói "cái gì, thế nào, vì sao" (Shute 2008).

**Trước** (buổi 5, câu 3, bị cờ "không nói vì sao lựa chọn khác sai"):

> **B.** Hàm mũ đơn điệu nên giữ nguyên trung vị; trung bình lớn hơn: $E[e^w] = e^{\mu+\sigma^2/2}$. FPP: "it will
> usually be the median… medians do not add up, whereas means do."

**Sau:**

> **B — trung vị.** Hàm `exp` giữ nguyên thứ tự: số nào đứng giữa trên thang log thì vẫn đứng giữa sau khi đổi ngược.
> Vì thế trung vị đi qua nguyên vẹn. **A sai**: trung bình thì không, `exp` kéo các giá trị lớn ra xa hơn nên trung bình
> thật lớn hơn con số nhận được. Ví dụ log = 0, 1, 2 → exp ≈ 1; 2,7; 7,4: trung vị 2,7 = exp(1), còn trung bình 3,7
> lớn hơn exp(1). **C sai**: mode là giá trị hay gặp nhất, không liên quan tới phép đổi ngược. **D sai**: quantile 0,9
> cũng đi qua nguyên vẹn, nhưng dự báo trên thang log là trung vị (quantile 0,5), không phải 0,9.

---

## Bài mẫu — buổi 1 mục 4.8 "Một con số hay cả phân phối"

Bản đầy đủ nằm ở `buoi-01/tai-lieu.md` mục 4.8 (một nguồn duy nhất — sửa ở đó). Số liệu từ lần chạy thật:
`buoi-01/dap-an/vi_du_quantile.py` (ví dụ nhỏ, không cần dữ liệu) và `buoi-01/dap-an/ve_hinh.py` (năm 2009–2010).

Khung, đối chiếu với D2:

| Bước D2 | Trong bài mẫu |
|---|---|
| Vấn đề | mỗi giờ phải mua điện trước; thiếu mất 4 đồng/kWh, thừa mất 1 đồng/kWh; nên mua bao nhiêu? |
| Mượn trước (D5) | phân phối, quantile (định nghĩa + cách đếm tay + kiểm lại với số trùng), trung vị |
| Trực giác | người bán bánh mì: hết bánh đắt hơn dư bánh thì làm dư một chút |
| Ví dụ số nhỏ | 10 ngày nhu cầu; tính mẫu dòng "mua 8"; bảng mua 6…12 → rẻ nhất ở 9 = quantile 0,8 |
| Vì sao 0,8 | tăng từng kWh: 8 → 9 lời 5 đồng, 9 → 10 lỗ 5 đồng; quy tắc dừng "tỷ lệ ngày thiếu ≤ 20%" |
| Công thức + ký hiệu | $p^\ast = C_u/(C_u+C_o)$; $C_u$, $C_o$, $p^\ast$ giải thích từng cái |
| Nói bằng lời | 4/(4+1) = 0,8; 1/(1+3) = 0,25; 1/2 = 0,5 — ba trường hợp |
| NumPy | `chi_phi()` + `np.quantile` trên đúng 10 số, in (33, 28) và 9.0; lưu ý nội suy, `method="inverted_cdf"` |
| Dữ liệu thật | sai số = thực tế − dự báo; quantile 0,8 của sai số 2009 = +0,455 kWh; vì sao cộng vào đúng ý newsvendor |
| Đọc bảng | chi phí −18,6%, MAE tệ hơn, giờ thiếu 20,1% ≈ 20% |
| Cách đọc hình | đủ 5 bước |
| Tóm lại + Tự kiểm tra | tiệm bánh, đáp án kèm nhầm lẫn hay gặp |
| Nâng cao | $F^{-1}$; Gneiting 2011 "MAE nhắm trung vị" |

Kết quả đọc thử (subagent mới, 2026-09-18): **0 chặn** (bản cũ 5 chặn trong riêng mục này). Người đọc tự trả lời
đúng cả 4 câu người dùng đã phải hỏi ChatGPT, và làm đúng câu tự kiểm tra. Vòng hai bắt được một câu sai số học
("8 trên 10 ngày", đúng là 9/10) cùng 6 chỗ khó khác; tất cả đã sửa.

---

## BƯỚC CUỐI — Đọc thử

### Tiêu chí đạt (sửa theo baseline Phase 5)

| Tiêu chí | Ngưỡng |
|---|---|
| Chỗ vướng mức **chặn** | **0** |
| Chỗ vướng mức **khó** | ≤ 5 mỗi buổi |
| Mục B "giải thích lại" | không khái niệm chính nào "KHÔNG GIẢI THÍCH ĐƯỢC" |
| Quiz chỉ bằng tài liệu | ≥ 9/10 — **điều kiện cần, không đủ**: bản cũ buổi 1, 7, 12 đều 10/10 dù 9–12 chỗ chặn |
| `tools/kiem_de_hieu.py NN` | 0 vi phạm, hoặc mỗi vi phạm còn lại có lý do ghi trong `NGHIEN-CUU.md` |

Chưa đạt → sửa → đọc thử lại bằng subagent **mới** (agent đã đọc bản cũ sẽ "nhớ" và dễ dãi hơn). Đọc thử cũng
bắt được lỗi nội dung thật (đáp án sai ở quiz buổi 7, câu sai số học trong bài mẫu), nên mọi con số subagent nghi
ngờ đều phải kiểm lại.

### Chuẩn bị

```bash
S=<thư mục scratchpad>/doc-thu/bNN && mkdir -p $S
cp buoi-NN/tai-lieu.md $S/
python3 -c "import re,sys; s=open('buoi-NN/kiem-tra.md',encoding='utf-8').read(); \
open('$S/kiem-tra-khong-dap-an.md','w',encoding='utf-8').write(re.sub(r'<details>.*?</details>\s*','',s,flags=re.S))"
```

Chỉ đọc lại một mục: cắt `tai-lieu.md` tới hết mục đó (giữ phần trước để có ngữ cảnh), và dặn subagent chỉ chấm
mục đó.

### Prompt đọc thử (dán nguyên văn cho subagent, kèm đường dẫn hai file)

```text
Bạn đóng vai MỘT HỌC VIÊN MỚI đang tự học một buổi của khoá "Forecasting in AI" (tiếng Việt).

## Bạn là ai (giữ vai nghiêm ngặt)
- Biết: Python cơ bản (list, hàm, vòng for, đọc CSV bằng pandas ở mức làm theo mẫu); toán phổ thông
  (trung bình cộng, phần trăm, lũy thừa, đồ thị hàm số, xác suất tung đồng xu).
- CHƯA biết: thống kê đại học (phương sai, độ lệch chuẩn, phân phối, quantile/phân vị, kiểm định, p-value,
  hồi quy, tương quan), forecasting, machine learning, xử lý tín hiệu. Không biết thuật ngữ tiếng Anh chuyên ngành.
- Chỉ biết những gì tài liệu buổi này đã định nghĩa TRƯỚC chỗ đang đọc.
- Tự học một mình, không có giảng viên, KHÔNG được tra web.

## Quy tắc quan trọng nhất
Bạn là một mô hình biết rất nhiều. Bạn PHẢI giả vờ không biết. Với MỖI thuật ngữ, ký hiệu, công thức, con số,
hãy tự hỏi: "Chỉ dựa vào những gì tài liệu này đã viết TRƯỚC đoạn này, một người như mô tả ở trên có hiểu được
không?" Nếu câu trả lời dựa vào kiến thức bạn có từ ngoài tài liệu → đó là CHỖ VƯỚNG, phải ghi lại.
Đừng khoan dung. Học viên thật đã phải đi hỏi ChatGPT vì những chỗ như vậy. Thà ghi thừa còn hơn bỏ sót.
Tự tính lại mọi con số trong ví dụ; số nào sai là chỗ vướng mức "khó" trở lên.

Các loại chỗ vướng cần săn:
1. Thuật ngữ dùng mà chưa định nghĩa (hoặc định nghĩa ở sau, hoặc chỉ có tên tiếng Anh).
2. Ký hiệu trong công thức chưa giải thích; công thức không có câu nói bằng lời ý nghĩa của nó.
3. Câu nói lửng: "thiếu", "thừa", "cao hơn", "sai số dương", "tốt hơn" mà không rõ so với cái gì, đơn vị gì.
4. Bước suy luận bị nhảy: kết luận xuất hiện mà không thấy vì sao.
5. Con số dồn dập không rõ số nào so với số nào; bảng/hình không nói cách đọc.
6. Câu trích tiếng Anh mà người đọc cần hiểu mới theo được ý.
7. Viết tắt không giải thích.
8. Khái niệm dùng như thể đã học ở buổi trước mà tài liệu không nhắc lại.

## Việc phải làm
Đọc lần lượt TOÀN BỘ file tai-lieu.md, từ đầu đến cuối. Chỉ được mở đúng 2 file được giao.
KHÔNG mở file nào khác, KHÔNG dùng web.
Sau đó làm file kiem-tra-khong-dap-an.md CHỈ bằng những gì đã đọc trong tài liệu.

## Trả về đúng khuôn sau (markdown)

### A. Chỗ vướng
| # | Mục | Trích nguyên văn (≤ 25 chữ) | Loại (1–8) | Vì sao không hiểu | Mức |
Mức: **chặn** = không hiểu thì không theo được phần sau / phải tra ngoài; **khó** = đoán được nhưng không chắc;
**nhỏ** = khó chịu nhưng không cản.

### B. Giải thích lại bằng lời của mình
Với mỗi khái niệm chính của buổi (tối đa 8): 2–4 câu giải thích như nói với bạn cùng lớp + một ví dụ số tự nghĩ ra.
Nếu không giải thích được từ tài liệu thì viết "KHÔNG GIẢI THÍCH ĐƯỢC" và lý do.

### C. Bài kiểm tra
Mỗi câu: đáp án chọn (hoặc câu trả lời ngắn) + mức tự tin (chắc / đoán) + mục tài liệu dựa vào.

### D. Tổng kết
- Số chỗ vướng theo mức: chặn / khó / nhỏ
- 3 đoạn khó hiểu nhất và vì sao
- Nếu chỉ được sửa một điều trong tài liệu này, sửa gì
```

### Chấm và ghi

1. So mục C với đáp án thật trong `kiem-tra.md`. Câu nào subagent làm "sai" thì kiểm lại cả đáp án của ta (quiz buổi
   7 câu 5 có đáp án sai).
2. Ghi vào `buoi-NN/NGHIEN-CUU.md` mục "Đọc thử": ngày, vòng, số chặn/khó/nhỏ, quiz, khái niệm "không giải thích
   được", các chỗ chặn và đã sửa thế nào.

---

## Buổi về sau: bớt dần chi tiết (expertise reversal)

Worked example chi tiết giúp người mới nhưng làm người đã giỏi chậm lại (Kalyuga et al. 2003). Khi một khái niệm đã
được dạy kỹ ở buổi trước, buổi sau **không giải lại từ đầu**. Chỉ nhắc định nghĩa một câu và một ví dụ ở mục 2 hoặc
hộp "Mượn trước". Khái niệm mới của buổi thì luôn đủ khuôn D2. D1, D3, D4, D8 áp dụng cho mọi buổi, không giảm.
