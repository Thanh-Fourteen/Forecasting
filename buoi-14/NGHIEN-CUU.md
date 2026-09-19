# Nhật ký research — Buổi 14: Baseline và chỉ số đánh giá

- **Ngày research:** 2026-09-19 (Phase 16). Bản nháp code/test/hình có từ Phase 4; tài liệu viết mới theo D1–D13.
- **Người/phiên:** Phase 16, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Hyndman & Athanasopoulos, *FPP3* ch. 5 (5.2 bốn phương pháp đơn giản, 5.3 fitted/phần dư, 5.4 chẩn đoán phần dư, 5.8 đo độ chính xác): https://otexts.com/fpp3/ | sách giáo khoa | 2026-09-19 | 4.1–4.5 |
| 2 | Hyndman & Koehler (2006), *Another look at measures of forecast accuracy*, IJF 22(4): https://robjhyndman.com/papers/mase.pdf | bài gốc | 2026-09-17 (Phụ lục D) | MASE, bẫy MAPE/sMAPE |
| 3 | M5 Competitors' Guide (RMSSE, WRMSSE): https://github.com/Mcompetitions/M5-methods | tài liệu cuộc thi | 2026-09-17 (Phụ lục D) | RMSSE |
| 4 | Gneiting (2011), *Making and evaluating point forecasts*, JASA 106: arXiv:0912.0902 | bài gốc | 2026-09-17 | chỉ số ↔ con số tối ưu (MAE → trung vị, RMSE → trung bình) |
| 5 | Hewamalage, Ackermann & Bergmeir (2023), *Forecast evaluation for data scientists: common pitfalls and best practices*, DMKD; arXiv:2203.10716 | tổng quan | 2026-09-19 | lỗi thường gặp (chỉ số phần trăm với số 0, bỏ baseline) |
| 6 | utilsforecast 0.2.16 `losses.py` (PyPI 27/4/2026): https://pypi.org/project/utilsforecast/ | mã nguồn | 2026-09-19 | quy ước `mape`/`smape` dạng tỷ lệ |
| 7 | Hyndman (2025) WAPE, Hyndsight | blog tác giả | 2026-09-17 | WAPE |

## Phiên bản đã xác minh

| Thư viện | Phiên bản | Nguồn |
|---|---|---|
| utilsforecast | 0.2.16 (27/4/2026, mới nhất) | PyPI JSON 2026-09-19 |
| statsforecast | 2.1.1 (bảng chung, chốt pandas 2.3.3) | `tools/nen/phien-ban.toml` |
| scipy / statsmodels | 1.18.1 / 0.15.0 | bảng chung |

## Dữ liệu

M4 Daily (Monash, Zenodo, CC BY 4.0) — 4.227 chuỗi; UCI Online Retail II (CC BY 4.0). Cả hai đã có trong danh mục, sha256 chốt.

## Phát hiện mới / lỗi hiểu sai phổ biến

- Trên 1.000 chuỗi M4 Daily, **naive và drift thắng seasonal naive** (MASE trung vị 0,835 / 0,810 so với 1,077): dữ liệu ngày của M4
  mùa vụ tuần yếu. Bài học: seasonal naive là baseline bắt buộc, không phải baseline mạnh nhất; mọi mô hình so với **tất cả** baseline.
- Bản nháp định nghĩa `me = mean(ŷ − y)`, ngược quy ước cả khoá (sai số = thực tế − dự báo, Phụ lục D, `tv.danh_gia`). Sửa cả `code/` lẫn
  `dap-an/` thành `mean(y − ŷ)` (không phải chỗ hở cố ý; bộ chấm không kiểm dấu ME).
- utilsforecast `mape`, `smape` trả tỷ lệ (không ×100, sMAPE thang 0–1) — đo được tỷ lệ tự viết / thư viện đúng 100 và 200.
- Hiểu lầm hay gặp: "MASE < 1 là thắng seasonal naive trên tập kiểm" — mẫu số là sai số seasonal naive **trên phần học**, không phải trên
  tập kiểm (FPP 5.8; Hyndman & Koehler 2006).

## Research viết lại (sư phạm)

- Baseline: FPP 5.2 dạy bằng một hình bốn đường trên cùng chuỗi; cách giải thích tốt nhất là "mỗi baseline là một giả định về tương lai"
  (mức cũ / giá trị cuối / chu kỳ trước / xu hướng thẳng).
- MAE ↔ trung vị, RMSE ↔ trung bình: minh hoạ bằng dãy lệch (1, 2, 3, 4, 20): hằng số làm MAE nhỏ nhất là 3, RMSE nhỏ nhất là 6 (Gneiting 2011).
- MAPE bất đối xứng: nói bằng ví dụ "thật 100, dự báo 150 → 50%; thật 150, dự báo 100 → 33%" (Hyndman & Koehler 2006).

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình lab 4 "hai dự báo tối ưu MAE và RMSE trên dữ liệu lệch" → dùng hằng số tối ưu trên mẫu lognormal (đã có trong code) | nhỏ | giữ |
| Tracking signal (lộ trình) | nhỏ | chỉ nhắc một câu trong ME; không thêm khái niệm (D9) |
| Hình `quy-uoc-thu-vien.png` của bản nháp | nhỏ | bỏ; bảng tỷ lệ trong tài liệu đủ |

## Đọc thử (Phase 16, 2026-09-19)

Tự đọc (không subagent), checklist `tools/CHUAN-DE-HIEU.md`. Mọi con số tính lại bằng Python/output thật: bảng baseline 6 số; MAE 1,6 /
RMSE 2,098 / ME 0,8 / MAPE 12,83 / sMAPE 13,61 / WAPE 13,33; hằng số $(1, 2, 3, 4, 20)$ → MAE 4,2 và 5,6, RMSE 7,68 và 7,07; MASE 1,067 /
RMSSE 1,327; ACF trễ 1 của hình phần dư 0,857 (chuỗi T100, cú rơi −2.205 ở vị trí 535); 58% mã hàng có ngày cuối phần học bằng 0, naive
WAPE = 100 ở 49% chuỗi tính được. Quiz: mọi đáp án số kiểm lại (câu 6: RMSE $\sqrt{7{,}5}$ = 2,74; câu 7: 0,67 / 1,33).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 3.940 | 16 | 0 | 2 | 2 | 10/10 có căn cứ | khó: "Nói bằng lời" nêu sMAPE 13,6 mà ví dụ không tính; "mẫu số là sai số dự báo một chu kỳ tới" mơ hồ. Nhỏ: bảng MAPE bất đối xứng lồng trong danh sách làm lệch "Đọc bảng"; ví dụ bán lẻ "phần lớn mã hàng" chưa đo (đo: 58%) |
| 2 | sau sửa | 16 | **0** | **0** | 1 | 10/10 | thêm dòng sMAPE vào ví dụ; viết lại bẫy MASE; sửa câu 58% |
| rà gọn | biên tập viên | — | — | — | — | — | 0 chỗ thừa đáng kể (bỏ hình quy ước thư viện của bản nháp, thay bằng bảng) |

Căn cứ quiz: 1, 6, 8 → 4.3; 2, 7 → 4.5; 3 → 4.2; 4, 9 → 4.4 + 4.6; 5 → 4.1; 10 → 4.1 + 4.5. `kiem_de_hieu.py 14` 0.

## Đọc thử độc lập (Phase 18, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: bảng bốn baseline (14; 18; 14/18; 19,6/21,2);
MAE 1,6 / RMSE 2,098 / ME 0,8; hằng số $(1, 2, 3, 4, 20)$ → 4,2 / 7,68 và 5,6 / 7,07; MAPE 12,83 / sMAPE 13,61 / WAPE 13,33; MASE 1,067 /
RMSSE 1,327; bảng quy ước 3,59 / 0,0179 = 200,6; mọi "Tự kiểm tra"; quiz 5–7. Khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.2 bảng + Đọc bảng | "khoảng dự báo sai độ rộng" | 1, 8 | "khoảng dự báo" chưa định nghĩa ở buổi nào từ 1 tới 14 | khó |
| 2 | 4.4 | "trung bình **13,6** (thang 0–200)" | 7 | vì sao thang tới 200 chỉ suy ra được từ công thức | nhỏ |
| 3 | 4.6 hình | "bảy chỉ số" | 5 | vừa nói tám chỉ số; không rõ bỏ cái nào | nhỏ |
| 4 | 4.3 hình | "mô phỏng lệch phải" | 8 | "lệch phải" (buổi 5) không nhắc lại; hình đủ để đoán | nhỏ |
| 5 | Bài tập 3 | "Hằng số nào tối thiểu chi phí" | 8 | cần quantile $C_u/(C_u+C_o)$ của buổi 1, không nhắc | nhỏ |
| 6 | 4.5 | "dùng trong cuộc thi M5" | 1 | M5 chưa giới thiệu; không cản | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Baseline**: $(3, 5, 4, 6)$, $m$ = 2 → trung bình 4,5; naive 6; seasonal naive 4, 6; drift 7, 8.
- **Phần dư vs sai số dự báo**: seasonal naive khớp $(3, 5, 4, 6)$: phần dư 1, 1; trung bình 1 ≠ 0 → bỏ sót xu hướng.
- **MAE/RMSE ưa trung vị/trung bình**: $(0, 0, 9)$ → MAE nhỏ nhất ở 0, RMSE ở 3.
- **MAPE bất đối xứng**: thật 50, dự báo 100 → 100%; thật 100, dự báo 50 → 50%.
- **MASE**: phần học $(4, 6, 5)$, $m$ = 1 → mẫu số 1,5; MAE kỳ chấm 3 → 2.
- **Đổi chỉ số đổi hạng**: chuỗi thưa, dự báo toàn 0 thắng MAE nhưng WAPE = 100%.

### C. Quiz mù

1 B · 2 B · 3 A · 4 A · 5 24; 24 / 28; 28 / 24; 28 / 29,6; 31,2 · 6 2,5 / 2,74 / 1, dự báo thấp · 7 0,67 / 1,33, thắng · 8 trung vị 4, MAE ·
9 MAPE vô hạn bị bỏ âm thầm; đếm chuỗi, WAPE/MASE · 10 MASE < 1 không phải thắng; thua naive, drift. Căn cứ: 1, 6, 8 → 4.3; 2, 7 → 4.5; 3 →
4.2; 4, 9 → 4.4 + 4.6; 5 → 4.1; 10 → 4.1 + 4.5. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 5. Sửa một điều: định nghĩa "khoảng dự báo" (buổi 16–17 dùng nhiều, đặt nền ở đây).

### E. Dài/lặp

| # | Mục | Trích | Vì sao thừa |
|---|---|---|---|
| 1 | 4.4 Đọc bảng bất đối xứng | "Cùng lệch 50 đơn vị, dòng dự báo cao bị phạt 50%" | đọc lại hai ô, câu dẫn trước bảng đã nói |

### Chấm, sửa, đọc lại

**Quiz mù 10/10**, đáp án của ta đúng (tính lại câu 5–7). Sửa: 4.2 "khoảng dự báo: dải mà giá trị thật rơi vào với xác suất cho trước, ví dụ
80%"; hình 4.6 "tám chỉ số trừ ME"; bài tập 3 nhắc quantile 0,8 của buổi 1; "Đọc bảng" bất đối xứng viết lại thành lý do (chia cho thực tế).
Đọc lại các mục đã sửa từ đầu: không vướng mới.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 18 đọc mù | 3.971 | 16 | 0 | 1 | 5 | 10/10 | 1 |
| sau sửa, đọc lại | 4.014 | 16 | **0** | **0** | 3 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 14` 0.

## Đọc thử độc lập Phụ lục D, phần mở rộng (Phase 18, 2026-09-19)

Đọc trong vai học viên đã học tới buổi 17. Tính lại mọi ví dụ bằng Python: mục 2 (1,6 / 2,10 / 0,8 / 12,8 / 13,6 / 0,133; sMAPE 66,7 và 40),
3 (1,07 / 1,33), 4 (pinball 0,40; Winkler 6,4; WIS 1,67), 5 (CRPS mẫu: cặp 2,4 → 0,6), 6 (Brier 0,142 / 0,24; log 0,430), 7 (skill 0,38 /
0,41), 8 (DM −0,94 / −0,84 / p 0,446), 9 (MAE 2,75; RMSE 3,3541; MAPE 0,107798; sMAPE 11,3351; MASE 1,4667; RMSSE 1,7039; pinball 2,70;
Murphy 0,015 − 0,085 + 0,240 = 0,170). Khớp hết; bảng dữ liệu thật khớp số buổi 14–15.

| Vòng | Chặn | Khó | Nhỏ | Chỗ thừa | Ghi chú |
|---|---|---|---|---|---|
| đọc | 0 | 0 | 3 | 0 | nhỏ: mục 3 nói "naive" trong khi buổi 14 dạy mẫu số là seasonal naive (công thức vẫn đúng với $m$); "trộn" trong bảng dữ liệu thật không giải thích; "Student-t" khác "phân phối t" của buổi 15 |
| sau sửa | 0 | 0 | 1 | 0 | mục 3 "seasonal naive … (phần học)"; "trộn" (cùng giờ hôm qua và tuần trước) |

**Đạt.** PDF 8 trang.
