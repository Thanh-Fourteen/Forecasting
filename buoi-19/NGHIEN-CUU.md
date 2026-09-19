# Nhật ký research — Buổi 19: Nhu cầu gián đoạn

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-19 (Phase 19). Buổi soạn mới hoàn toàn (thư mục tạo từ khuôn).
- **Người/phiên:** Phase 19, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Syntetos, Boylan & Croston (2005), *JORS* 56: 495–503 — ngưỡng ADI 1,32, CV² 0,49; bốn nhóm mượt / thất thường / gián đoạn / cục: https://ideas.repec.org/a/pal/jorsoc/v56y2005i5d10.1057_palgrave.jors.2601841.html | bài gốc | 2026-09-19 | 4.1 |
| 2 | Svetunkov (2024), "Intermittent demand classifications: is that what you need?" — ngưỡng SBC được rút ra để chọn giữa Croston và SBA theo MSE; dùng cho mô hình khác là lạm dụng; nên so trực tiếp trên hold-out: https://openforecast.org/2024/07/16/intermittent-demand-classifications-is-that-what-you-need/ | phản biện | 2026-09-19 | 4.1 "Khi nào dùng" |
| 3 | FPP3 §13.2 "Time series of counts" (Croston: hai SES riêng, α cố định 0,1 trong bản gốc; không ứng với mô hình thống kê nào nên không có khoảng dự báo; bị chệch): https://otexts.com/fpp3/counts.html | sách giáo khoa | 2026-09-19 | 4.3 |
| 4 | Teunter, Syntetos & Babai (2011), *EJOR* 214(3): 606–615 — TSB: cập nhật xác suất có nhu cầu MỌI kỳ, nên dự báo giảm khi mặt hàng ngừng bán (lỗi thời); không chệch tại thời điểm bất kỳ | bài gốc (qua tóm tắt ScienceDirect, Nixtla docs) | 2026-09-19 | 4.4 |
| 5 | Nixtla docs TSB: `TSB(alpha_d, alpha_p)`, dự báo = xác suất × lượng: https://nixtlaverse.nixtla.io/statsforecast/docs/models/tsb.html | tài liệu chính thức | 2026-09-19 | 4.4, code |
| 6 | Nikolopoulos et al. (2011), *JORS* 62(3): 544–554 — ADIDA: gộp thời gian → dự báo trên chuỗi gộp → chia lại | bài gốc (tóm tắt) | 2026-09-19 | 4.5 |
| 7 | Petropoulos & Kourentzes (2015), *JORS* — IMAPA: nhiều mức gộp, trung bình các dự báo | bài gốc (tóm tắt) | 2026-09-19 | 4.5 |
| 8 | Kourentzes (2014), *IJPE* 156: 180–190 — MSE/MAE không hợp để tối ưu/chọn mô hình nhu cầu gián đoạn; đánh giá bằng mô phỏng tồn kho order-up-to (T, S): https://kourentzes.com/forecasting/2014/06/11/on-intermittent-demand-model-optimisation-and-selection/ | bài gốc | 2026-09-19 | 4.2, 4.6 |
| 9 | Mã nguồn statsforecast 2.1.1 (`models.py`): `_croston_classic` SES α = 0,1 cố định cho lượng và khoảng; khoảng đầu tính từ đầu chuỗi (`np.diff(idx + 1, prepend=0)`); SES mức đầu = số đầu; `_croston_sba` nhân 0,95 = 1 − α/2; `_tsb` SES trên dãy 0/1 (mọi kỳ) × SES trên lượng; `_adida` mức gộp = round(khoảng trung bình), SES tối ưu α ∈ [0,1; 0,3] trên chuỗi gộp; `_imapa` trung bình các mức gộp 1 … round(khoảng TB) | mã nguồn | 2026-09-19 | code, test khớp |
| 10 | Godahewa et al. (2021), Monash Archive; Car Parts: 2.674 chuỗi tháng 1/1998 → 3/2002, từ gói R expsmooth (Hyndman et al. 2008); bản "without missing" thay ô thiếu bằng 0: https://zenodo.org/records/4656021 | dữ liệu | 2026-09-19 | toàn buổi |

## Phiên bản đã xác minh

statsforecast 2.1.1, scipy 1.18.1, pandas 2.3.3 (ràng buộc Nixtla), numpy 2.5.3 — theo `tools/nen/phien-ban.toml`, `uv.lock` của buổi.

## Dữ liệu

| Bộ | Danh mục | Giấy phép | Ghi chú |
|---|---|---|---|
| `monash-car-parts-khong-thieu` | sha256 `a0b1e87e2329`, 39,6 KB | CC BY 4.0 (Zenodo) | 2.674 × 51 tháng, 75,9% ô bằng 0. **Một phần số 0 là ô thiếu đã bị thay** (Monash ghi rõ) — nêu ở "Lỗi thường gặp" (nhu cầu bị kiểm duyệt / thiếu ≠ bán 0) |

## Số liệu thật (`dap-an/ve_hinh.py`, `dap-an/gian_doan.py`)

| Đại lượng | Giá trị |
|---|---|
| Tỷ lệ tháng bằng 0 | 75,91% |
| Phân loại SBC trên 38 tháng đầu (ADI = số tháng / số tháng có bán) | gián đoạn 2.231; cục 290; mượt 23; thất thường 5; bán < 2 lần 125. ADI trung vị 5,43; CV² trung vị 0,194 |
| Ví dụ $(0, 0, 3, 0, 0, 0, 2, 0, 4, 0, 0, 0)$ | α = 0,5: Croston 3,25 / 2,75 = 1,182; SBA 0,886; TSB 0,0791 × 3,25 = 0,257. α = 0,1: Croston 1,007; SBA 0,956; TSB 0,514 (khớp statsforecast) |
| Mã T1002 (8 lần bán trong 24 tháng đầu, lần cuối tháng 17) | Croston đứng ở 0,342 từ tháng 18 tới 50; TSB 0,244 ở tháng 25 → 0,016 ở tháng 50 |
| AutoETS trên T1002, 38 tháng đầu | dự báo 0,035; khoảng 80% (−0,70; 0,77) — cận dưới âm |
| Ví dụ MAE/RMSE $(0, 0, 2, 0, 0, 0, 1, 0, 0, 3)$ | dự báo 0: MAE 0,60, RMSE 1,183; dự báo 0,6: MAE 0,84, RMSE 1,020 |
| Poisson μ = 0,8, P(≤ k) | 0,449; 0,809; 0,953 → quantile 0,9 = 2 |
| Mô phỏng tay nhu cầu (1, 2, 2), S = 3, về sau 1 tháng | tồn 2 món-tháng, thiếu 1 → chi phí 2 + 9 = 11; đáp ứng 4/5. Tự kiểm tra (1, 4, 0), S = 3: 21; quiz (0, 3, 1), S = 2: 20, đáp ứng 50% |
| Backtest 12 cutoff (dự báo 2 tháng), 2.674 chuỗi, ~15 s | xem bảng dưới; 17 chuỗi có phần học phẳng bị bỏ khỏi RMSSE/MASE |

| Mô hình | RMSSE | MASE | ME | tồn kho TB | đáp ứng | chi phí/mã |
|---|---|---|---|---|---|---|
| AutoETS | 0,712 | 1,199 | −0,058 | 1,80 | 76,4% | 31,85 |
| CrostonClassic | 0,827 | 1,437 | −0,121 | 1,81 | 62,8% | 37,87 |
| CrostonSBA | 0,817 | 1,405 | −0,095 | 1,73 | 61,8% | 37,33 |
| TSB (0,1; 0,1) | 0,684 | 1,147 | −0,069 | 1,74 | 76,7% | 30,98 |
| ADIDA | 0,681 | 1,090 | −0,004 | 1,52 | 72,8% | 30,05 |
| IMAPA | 0,673 | 1,100 | −0,013 | 1,55 | 74,7% | 29,64 |
| SeasonalNaive | 0,951 | 1,208 | −0,045 | 2,29 | 66,0% | 42,22 |
| Naive | 0,875 | 1,234 | −0,004 | 3,39 | 69,8% | 53,74 |
| HistoricAverage | 0,738 | 1,202 | −0,103 | 1,73 | 69,9% | 33,87 |
| Zero | 0,709 | 0,820 | +0,402 | 0 | 0% | 43,43 |

Mô phỏng: hàng đặt cuối tháng t về đầu tháng t + 2 (chờ trọn 1 tháng), S = quantile 0,9 Poisson của nhu cầu 2 tháng. Bản đầu (Phase 19,
vòng soạn) cho hàng về đầu tháng t + 1 — thời gian dẫn thực chất bằng 0, mâu thuẫn với "S đủ 2 tháng"; bắt được khi tự đọc thử, đã sửa và
chạy lại (thứ hạng không đổi, tỷ lệ đáp ứng giảm ~9 điểm).

MAPE bỏ tháng 0 (code đầu buổi): AutoETS 62,0; TSB 56,5; IMAPA 61,1; Zero 100. MAE: Zero 0,402 thấp nhất → code đầu buổi chọn "Zero".
Theo nhóm SBC: nhóm gián đoạn (2.174 chuỗi có RMSSE) và cục (270) đều IMAPA đứng đầu cả RMSSE lẫn chi phí; Croston/SBA đứng cuối nhóm
"gián đoạn" dù SBC khuyên dùng — vì nhiều mã ngừng bán.

## Phát hiện mới / lỗi hiểu sai phổ biến

- Ngưỡng SBC chỉ là để chọn Croston hay SBA theo MSE (Svetunkov 2024); trên Car Parts, Croston/SBA thua cả AutoETS và trung bình lịch sử
  vì mặt hàng lỗi thời → dạy SBC như cách **mô tả** dữ liệu, chọn mô hình bằng backtest + chi phí.
- MAE/MASE ưa dự báo 0 trên chuỗi thưa (trung vị = 0) — "Zero" có MASE tốt nhất (0,820) nhưng đáp ứng 0%.
- RMSSE cũng xếp "Zero" (0,709) trên AutoETS (0,712) — chỉ số thống kê và chi phí chọn khác nhau. Naive vs SeasonalNaive cũng đảo.
- `utilsforecast.mape` bỏ điểm y = 0 khỏi trung bình → MAPE "hợp lệ" nhưng chỉ chấm 24% số tháng.
- Dự báo 0,3 món/tháng là **tốc độ bán trung bình**, không phải "tháng sau bán 0,3 món"; quyết định dùng tổng qua thời gian dẫn.
- Car Parts bản không thiếu: ô thiếu bị thay 0 → nhu cầu thật có thể cao hơn; hết hàng cũng ghi 0 (nhu cầu bị kiểm duyệt).

## Research viết lại (sư phạm)

- Trực giác Croston: "mỗi lần bán bao nhiêu" ÷ "bao lâu bán một lần"; TSB: "tháng này có bán không" × "bán thì bao nhiêu".
- Ví dụ đời thường: phụ tùng xe đời cũ — sau khi hãng ngừng đời xe, không ai mua nữa (lỗi thời).
- Chấm bằng tồn kho: order-up-to giống newsvendor buổi 1 (quantile C_u / (C_u + C_o) = 9 / 10).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình: lead time 2 tuần | nhỏ | dữ liệu theo tháng → lead time 1 tháng, xem kho mỗi tháng; S = quantile 0,9 Poisson của nhu cầu 2 tháng |
| Mô hình đếm (Poisson, âm nhị thức, zero-inflated) | nhỏ | chỉ dùng Poisson để đặt mức S; mô hình đếm đầy đủ → hộp "Nâng cao" (khái niệm tối đa 6) |
| Chỗ hở lộ trình "ETS + MAPE" | nhỏ | code đầu buổi chấm MAE + MAPE bỏ tháng 0 và chọn theo MAE (→ "Zero"); TSB tự viết chỉ cập nhật xác suất ở tháng có bán. Bảng `quy-uoc.md` cập nhật |
| M5 tuỳ chọn | nhỏ | không dùng (Car Parts đủ, giấy phép mở) |

## Đọc thử (Phase 19, 2026-09-19)

Tự đọc (không subagent), checklist `tools/CHUAN-DE-HIEU.md`. Tính lại bằng Python/hàm của buổi: ADI 8/3, CV² 0,042; MAE/RMSE ví dụ 10 tháng;
Croston α = 0,5: 3,25 / 2,75 = 1,18, SBA 0,886; TSB 0,079 × 3,25 = 0,257; α = 0,1: 1,007 / 0,956 / 0,514 (khớp statsforecast); Poisson μ =
0,8 → S = 2; mô phỏng (1, 2, 2) S = 3 → 11, tự kiểm tra (1, 4, 0) → 21, quiz 8 (0, 3, 1) → 20 và 50%; quiz 5 (4; 0,11), 6 (1,0; 0,75; 0,40), 7 (S = 3).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz có căn cứ | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 3.606 | 12 | **1** | 1 | 2 | 10/10 | **chặn**: mô phỏng cho hàng đặt cuối tháng về ngay đầu tháng sau (thời gian dẫn thực chất 0), mâu thuẫn "S phải đủ 2 tháng" và Từ mới "đặt cuối tháng 3, về cuối tháng 4" — lỗi của code, không chỉ của chữ. Khó: "khoảng 80%" chưa nhắc định nghĩa. Nhỏ: lý do SBA chệch chỉ nêu tên bài báo; Poisson chỉ có định nghĩa một câu |
| 2 | 3.679 | 12 | **0** | **0** | 2 | 10/10 | sửa `mo_phong_ton_kho` (hàng về đầu tháng t + 1 + lead), chạy lại mọi chi phí (thứ hạng không đổi, đáp ứng giảm ~9 điểm), viết lại ví dụ tay có cột "đang về", tự kiểm tra, quiz 8, bộ chấm; 4.2 định nghĩa khoảng dự báo ngay tại chỗ |
| rà gọn | biên tập viên | — | — | — | — | — | 1 chỗ thừa nhỏ ("Khi nào dùng" 4.2 báo trước kết luận 4.6), giữ làm cầu nối |

Căn cứ quiz: 1, 3 → 4.2; 2 → 4.4; 4, 5 → 4.1; 6 → 4.3–4.4; 7, 8 → 4.6; 9 → 4.2 + 4.6; 10 → 4.1 + 4.4. `kiem_de_hieu.py 19` 0; `kiem_tra_lab.py 19` đạt.

## Đọc thử độc lập (Phase 21, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: ADI 2,67, CV² 0,042; bảng MAE/RMSE (0,60 / 1,18;
0,84 / 1,02); Croston 1,18, SBA 0,886; TSB 0,079 → 0,26; Poisson(0,8) 0,449 / 0,809 / 0,953 / 0,991; mô phỏng kho 11; tự kiểm tra 4.3 (0,75 /
0,56), 4.6 (21); quiz 5 (ADI 4, CV² 0,11), 6 (1,0 / 0,75 / 0,40), 8 (20, 50%). Khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 6 (+ quiz câu 10) | "Phân loại SBC chọn Croston" | 7 | "SBC" chưa từng được đặt tên; quiz câu 10 dùng nó | khó |
| 2 | 4.2 | "(M5 chọn nó vì lẽ này)" | 7 | M5 là gì | nhỏ |
| 3 | 4.4 | "`TSB(alpha_d=0.1, alpha_p=0.1)`" | 1 | `alpha_d` không nói là trọng số của lượng bán | nhỏ |
| 4 | 4.6 | bảng Poisson | 5 | không nói con số tính bằng gì | nhỏ |
| 5 | Lab bước 3 | "RMSSE và MASE … (mục 4.2)" | 5 | định nghĩa nằm ở mục 2, không ở 4.2 | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **ADI × CV²**: (0, 0, 6, 0, 2, 0) → ADI 3, lượng 6 và 2: CV² 0,25 → gián đoạn.
- **Tốc độ bán / chỉ số**: (0, 0, 0, 4): MAE ưa 0, RMSE ưa 1.
- **Croston / SBA**: lượng 4, khoảng 2 → 2; α = 0,2 → SBA 1,8.
- **TSB**: xác suất 0,5, α 0,5, hai tháng 0 → 0,125; lượng 4 → 0,5.
- **Gộp thời gian**: (0, 3, 0, 0, 0, 3) → quý 3, 3 → 1 món/tháng.
- **Chấm bằng kho**: $S$ = 2, nhu cầu (2, 2): tháng 2 thiếu 2 → chi phí 18.

### C. Quiz mù

1 B · 2 C · 3 B · 4 A · 5 ADI 4, CV² 0,11, gián đoạn · 6 Croston 1,0, SBA 0,75, TSB 0,40 · 7 $S$ = 3 · 8 tồn 2, thiếu 2, chi phí 20, đáp ứng
50% · 9 MAE ưa trung vị 0, MAPE bỏ tháng 0; chấm RMSSE + chi phí → IMAPA · 10 ngưỡng chỉ để chọn Croston/SBA; Croston đứng yên khi mã ngừng
bán. Căn cứ: 1, 3, 9 → 4.2; 2 → 4.4; 4, 5, 10 → 4.1 (+ 4.4); 6 → 4.3–4.4; 7, 8 → 4.6. Tất cả "chắc" (câu 10 đoán nghĩa "SBC" từ ngữ cảnh).

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 4.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10.** Sửa: #1 mục 4.1 gọi tên "phân loại SBC" + một dòng trong bảng Từ mới; #2 "cuộc thi dự báo bán lẻ M5"; #5 "(định nghĩa ở
mục 2)". Giữ #3, #4 (học viên chỉ đọc bảng Poisson; `alpha_d` không cần cho bài).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 21 đọc mù | 3.679 | 12 | 0 | 1 | 4 | 10/10 | 0 |
| sau sửa, đọc lại | 3.691 | 12 | **0** | **0** | 2 | 10/10 | 0 |
