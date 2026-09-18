# Kiểm tra buổi 13 — Feature engineering và chống rò rỉ

10 câu. Tự làm trước, mở đáp án sau.

---

**1 (nhắc lại).** Ba nhóm "biết trước bao lâu" là gì? Mỗi nhóm một ví dụ.

<details><summary>Đáp án</summary>

- **Vô hạn** — lịch: thứ, tháng, Fourier, số ngày tới Tết. Không bao giờ rò rỉ.
- **Kế hoạch / dự báo** — biết tới thời điểm công bố: khuyến mãi đã lên lịch, dự báo thời tiết, dự báo phụ tải của nhà vận hành.
- **Quá khứ của chuỗi** — chỉ tới $t-h$: lag, rolling đã shift.

Mọi cột không thuộc ba nhóm này đều đáng ngờ.

</details>

---

**2 (nhắc lại).** Vì sao phải `shift` trước khi `rolling`? Và vì sao lag nhỏ nhất phải ≥ tầm dự báo?

<details><summary>Đáp án</summary>

`y.rolling(7).mean()` tại $t$ có cửa sổ **kết thúc tại $t$**, tức chứa $y_t$ — với tầm dự báo $h=1$, lúc dự báo $y_{t+1}$ ta **chưa** có
$y_t$... thực ra ta có, nhưng nếu mục tiêu là $y_t$ thì feature chứa chính đáp án. Quy tắc an toàn: `y.shift(h).rolling(w)`.

Lag < h nghĩa là dùng giá trị chưa xảy ra: dự báo 24 giờ tới mà dùng `lag_1` thì lúc chạy thật không có số đó.

</details>

---

**3 (nhắc lại).** Fourier term giải quyết vấn đề gì? Nêu công thức và một đánh đổi.

<details><summary>Đáp án</summary>

Mùa vụ chu kỳ dài: mùa vụ năm trên dữ liệu ngày cần 365 biến giả. Thay bằng $K$ cặp:
$\sin(2\pi i t/m)$, $\cos(2\pi i t/m)$ với $i = 1..K$, $m = 365{,}25$ → chỉ $2K$ cột, **không phụ thuộc độ dài chu kỳ**.

Đánh đổi: $K$ nhỏ chỉ bắt được hình dạng trơn; $K$ lớn bắt được đỉnh hẹp nhưng dễ overfit. Chọn $K$ bằng backtest.

</details>

---

**4 (nhắc lại).** Vì sao không dùng được thư viện lịch âm Trung Quốc cho dữ liệu Việt Nam?

<details><summary>Đáp án</summary>

Âm lịch tính theo thời điểm sóc **ở múi giờ địa phương**: Việt Nam dùng kinh tuyến 105°Đ (UTC+7), Trung Quốc 120°Đ (UTC+8). Khi thời điểm
sóc rơi vào khoảng giữa hai múi, ngày mùng 1 lệch nhau. Trong 2000–2035 có đúng hai năm như vậy: **2007** (VN 17/02, TQ 18/02) và **2030**
(VN 02/02, TQ 03/02).

</details>

---

**5 (vận dụng).** Bạn viết `kiem_ro_ri`, chạy trên bộ feature của mình và nó báo "sạch". Nêu ba lý do khiến kết quả đó có thể sai.

<details><summary>Đáp án</summary>

1. **Bỏ qua vài dòng cuối** trước mốc cắt — đúng vùng duy nhất lộ vi phạm của rolling centered.
2. **Coi NaN vs số là giống nhau**: `rolling(center=True)` không đặt `min_periods` trả NaN ở mép, nên phép so bỏ qua chính chỗ rò rỉ.
3. **Mốc cắt chọn không có chủ đích**: rò rỉ kiểu `interpolate(limit_direction="both")` chỉ lộ ra khi mốc cắt rơi vào **mép một lỗ hổng**.

Và lý do thứ tư: bài cắt-tương-lai **không** bắt được lag < tầm dự báo — cần thêm bài nhiễu mục tiêu.

</details>

---

**6 (vận dụng).** Mô hình dự báo phụ tải 24 giờ tới của bạn dùng feature nhiệt độ. Mô tả cách lấy dữ liệu huấn luyện sao cho đúng.

<details><summary>Đáp án</summary>

Dùng **bản dự báo nhiệt độ đã lưu** (archived forecast) cho đúng tầm sẽ chạy thật — ví dụ Open-Meteo Previous Runs cho giá trị đã dự báo
trước 1 ngày. **Không** dùng nhiệt độ thật (ERA5/quan trắc) của giờ cần dự báo.

Lý do kép: (a) lúc chạy thật không có nhiệt độ thật; (b) nếu huấn luyện bằng thật rồi chạy bằng dự báo, mô hình chưa từng thấy sai số của
dự báo (MAE 1,33 °C ở D+1, 2,07 °C ở D+3) nên tin nó quá mức. Đo được: −3,85% (hứa) so với −3,10% (chạy bằng D+1) và **+2,20%** (chạy bằng
D+3).

</details>

---

**7 (vận dụng).** Feature Tết của bạn cải thiện MAE cả năm 1,9%. Đồng nghiệp đề nghị bỏ vì "không đáng kể". Bạn trả lời sao?

<details><summary>Đáp án</summary>

Báo cáo theo **vùng có tác dụng**: quanh Tết (±10 ngày) MAE giảm từ 167.769 xuống 139.478, tức **−16,9%**. Tết chỉ chiếm ~6% số ngày nên
trung bình cả năm loãng đi.

Thêm lập luận nghiệp vụ: những ngày đó chính là lúc sai số đắt nhất (tồn kho, nhân lực, khuyến mãi). Nguyên tắc chung: **luôn báo cáo cả
sai số tổng thể lẫn sai số trên phân đoạn mà feature tác động**.

</details>

---

**8 (vận dụng).** Bạn ghép dữ liệu thời tiết theo giờ vào chuỗi phụ tải bằng `merge_asof(..., direction="nearest")`. Có vấn đề gì?

<details><summary>Đáp án</summary>

`nearest` lấy cả bản ghi **sau** mốc → rò rỉ. Phải `direction="backward"` và đặt `tolerance` (nếu không, khi nguồn thời tiết thiếu một
tuần, hàm vẫn kéo giá trị cũ xuống mà không báo).

Kiểm thêm: mốc trùng ở bảng phải (bản công bố và bản sửa) phải khử **trước** khi ghép; và coi chừng quy ước mốc — EIA-930 ghi **cuối giờ**,
Open-Meteo ghi **đầu giờ**; lệch một giờ là rò rỉ một bước.

</details>

---

**9 (đọc bảng).** Bảng MAE dự báo phụ tải 24 giờ (baseline chỉ lag = 1.909,68 MW):

| Bộ feature | MAE (MW) |
|---|---|
| + nhiệt độ thật của giờ cần dự báo | 1.836,16 |
| + dự báo nhiệt độ trước 1 ngày | 1.834,29 |
| + dự báo nhiệt độ trước 3 ngày | 1.965,47 |
| huấn luyện bằng thật, chạy bằng dự báo 3 ngày | 1.951,70 |

(a) Vì sao dùng **dự báo** D+1 lại tốt hơn cả dùng **sự thật**? (b) Bạn khuyến nghị gì cho hệ thống chỉ có dự báo thời tiết D+3?

<details><summary>Đáp án</summary>

(a) Vì mô hình được huấn luyện **và** chạy trên cùng loại đầu vào: nó học luôn cả đặc tính sai số của bản dự báo. Mô hình huấn luyện bằng
sự thật coi nhiệt độ là chính xác, nên gán hệ số lớn hơn mức đáng tin. Chênh lệch nhỏ (1.834,29 so với 1.836,16) nhưng đúng chiều, và nó
cho thấy "dùng sự thật" không phải là giới hạn trên như nhiều người tưởng.

(b) **Không dùng nhiệt độ** cho tầm đó: D+3 làm MAE tăng 2,92% so với baseline. Hoặc thu thập nguồn dự báo tốt hơn, hoặc dùng nhiệt độ
**hiện tại** (nhân quả, −2,31%). Và phải báo cáo rằng con số −3,85% trong backtest cũ là ảo.

</details>

---

**10 (tìm chỗ sai).** Một pull request thêm 5 feature:

```python
f["tb_7"]       = y.rolling(7, center=True).mean()
f["z"]          = (y - y.mean()) / y.std()
f["tb_thu"]     = y.groupby(y.index.dayofweek).transform("mean")
f["y_dien"]     = y.interpolate(limit_direction="both")
f["truoc_tet"]  = (pd.Timestamp("2011-02-03") - y.index).days
```

Chỉ ra vấn đề của từng dòng và cách sửa.

<details><summary>Đáp án</summary>

1. `tb_7` — **rolling không shift + centered**: chứa 3 điểm sau $t$. Sửa: `y.shift(h).rolling(7).mean()`.
2. `z` — **chuẩn hoá trên toàn bộ dữ liệu**: `mean`/`std` chứa thông tin tập kiểm. Sửa: fit scaler **chỉ trên train**, hoặc dùng thống kê
   expanding có shift.
3. `tb_thu` — **target encoding toàn bộ**: mỗi dòng biết trung bình của cả tương lai. Sửa: `y.shift(h).groupby(...).expanding().mean()`.
4. `y_dien` — **điền hai chiều**: giá trị điền lấy từ tương lai. Sửa: `ffill` (hoặc điền theo mùa vụ), và chỉ điền lỗ ngắn (buổi 10).
5. `truoc_tet` — **hardcode Tết 2011**: đúng đúng một năm, sai mọi năm khác. Sửa: tính từ lịch âm (`so_ngay_toi_tet`), kiểm với `holidays`
   cho 2000–2035.

Bốn dòng đầu bị `kiem_ro_ri` bắt; dòng thứ năm **không** rò rỉ (chỉ dùng lịch) nhưng vẫn sai — nó chỉ bị bắt bởi test kiểm ngày Tết từng
năm. Đó là lý do bộ chấm cần cả hai loại test.

</details>
