# Nhật ký research — Buổi 16: Exponential smoothing và Theta

- **Ngày research:** 2026-09-19 (Phase 17). "Bản nháp" chỉ là khuôn: code, đáp án, bộ chấm, hình, notebook, tài liệu soạn mới.
- **Người/phiên:** Phase 17, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Hyndman & Athanasopoulos, *FPP3* ch. 8 (8.1 SES, 8.2 Holt, damped, 8.3 Holt–Winters, 8.4 phân loại, 8.5 state space ETS(A,N,N)/(M,N,N), 8.6 AICc, 8.7 khoảng dự báo): https://otexts.com/fpp3/expsmooth.html | sách giáo khoa | 2026-09-19 | 4.1–4.4 |
| 2 | StatsForecast 2.1.1 (PyPI 16/7/2026, mới nhất): `AutoETS(season_length, model='ZZZ', damped, phi, prediction_intervals, distribution)`, `AutoTheta(season_length, decomposition_type='multiplicative', model ∈ {STM, OTM, DSTM, DOTM})`, `SeasonalNaive(season_length)`: https://nixtlaverse.nixtla.io/statsforecast/src/core/models.html | tài liệu chính thức | 2026-09-19 | 4.4–4.6 |
| 3 | Release notes statsforecast 2.1.0/2.1.1 (7/2026): phân phối sai số thống nhất cho ETS/CES/Theta, conformal, UCM; sửa Theta NaN với chuỗi 4 điểm; không đổi API AutoETS/AutoTheta: https://github.com/Nixtla/statsforecast/releases | changelog | 2026-09-19 | phiên bản |
| 4 | Assimakopoulos & Nikolopoulos (2000), The theta model, IJF 16; Hyndman & Billah (2003), Unmasking the Theta method, IJF 19 (Theta = SES + drift bằng nửa độ dốc) | bài gốc | (qua FPP, tài liệu statsforecast) | 4.5 |
| 5 | Fiorucci và cộng sự (2016), Models for optimising the theta method, IJF 32 (OTM, DOTM trong AutoTheta) | bài gốc | tài liệu statsforecast | 4.5 |
| 6 | Athanasopoulos, Hyndman, Song & Wu (2011), The tourism forecasting competition, IJF 27 (tầm 24 tháng) | bài gốc | header tệp .tsf | dữ liệu |

## Phiên bản đã xác minh

statsforecast 2.1.1 (bảng chung, bản mới nhất ngày 19/9/2026), scipy 1.18.1, pandas 2.3.3 (ràng buộc Nixtla).

## Dữ liệu

Tourism Monthly (Monash, CC BY 4.0): 366 chuỗi, dài 91–333 tháng, 574 giá trị bằng 0 (ETS nhân không dùng được cho các chuỗi đó).
Eurostat `avia_paoc` EU27 (CC BY 4.0), dùng 1/2008–12/2019 (bỏ COVID). Lộ trình ghi "US BTS": thay bằng Eurostat có sẵn trong danh mục
(cùng bài học biên độ mùa vụ tăng).

## Số liệu thật (`dap-an/ve_hinh.py`; K-fold không dùng; statsforecast tất định)

| Đại lượng | Giá trị |
|---|---|
| T249 theo năm (27 năm): SES tự viết | α = 0,632, dự báo 1.589,5 = statsforecast 1.589,5 |
| Holt tự viết | α = 0,464, β = 0,099; dự báo 1.681,6 / 1.740,6 / 1.799,7 so với statsforecast 1.709,4 / 1.770,1 / 1.830,8 (≤ 1,7%) |
| Hành khách EU, học tới 12/2017, chấm 2018–2019 | MAPE: HW cộng 3,23%, HW nhân 2,13%, AutoETS → ETS(A,N,A) 5,60%, seasonal naive 7,69%; biên độ mùa vụ 31,4 (2008) → 47,6 (2017) → 49,4 (2019) triệu |
| 366 chuỗi Tourism, 2 cửa sổ 24 tháng (cutoff 296, 308) | MASE trung bình: AutoETS 1,581, AutoTheta 1,691, seasonal naive 1,720 |
| So seasonal naive | AutoETS thắng 70,5% chuỗi, DM −5,23, p < 0,0001; AutoTheta 57,9%, DM −0,70, p = 0,49 |
| Tỷ lệ phủ | AutoETS 80% → 81,0%, 95% → 91,4%; AutoTheta 80% → 69,1%, 95% → 83,5% |
| Bản `code/` | SES α = 1,000, SSE = 0; MAPE mặc định 3,23% (HW cộng) |

## Phát hiện mới / lỗi hiểu sai phổ biến

- Holt tự viết (mức, độ dốc ban đầu cố định, tối thiểu SSE) chỉ khớp statsforecast (tối ưu cả trạng thái ban đầu theo likelihood) ở một
  phần chuỗi: dò 264 chuỗi năm, chỉ 5 chuỗi lệch dưới 2%; T92 (có năm ngoại lai) lệch 50%. SES thì khớp tuyệt đối. Tài liệu nói rõ nguyên
  nhân (khởi tạo + hàm mục tiêu), chọn T249 làm ví dụ.
- AICc chọn ETS(A,N,A) cho hành khách EU nhưng MAM dự báo tốt hơn nhiều: AICc đo độ khớp có phạt trên phần học, không phải sai số dự báo.
- AutoTheta: thắng seasonal naive theo trung vị nhưng không có ý nghĩa theo DM; khoảng dự báo hẹp hơn danh nghĩa rõ rệt.
- Khoảng 95% của ETS phủ 91,4%: khoảng dựa trên mô hình không tính bất định của việc chọn mô hình và tham số.

## Research viết lại (sư phạm)

- SES: "trung bình có trọng số, trọng số giảm theo cấp số nhân" — minh hoạ bằng trọng số α, α(1−α), α(1−α)² với α = 0,5.
- Cộng / nhân: "mùa hè đông hơn 20 triệu" so với "mùa hè đông hơn 20%".
- State space: "phương trình quan sát + phương trình cập nhật" → có phương sai sai số → có khoảng dự báo.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| "1.500 chuỗi du lịch" | nhỏ | Tourism Monthly có 366 chuỗi; dùng cả 366 |
| US BTS hành khách | nhỏ | Eurostat EU27 (đã có trong danh mục, CC BY 4.0) |
| Chỗ hở thêm: SES khớp bằng mức đã cập nhật (dùng y_t để "dự báo" y_t) | nhỏ | thêm vào bảng `quy-uoc.md`; bài kiểm nhiễu mục tiêu (buổi 13) bắt được |

## Đọc thử (Phase 17, 2026-09-19)

Tự đọc (không subagent), checklist `tools/CHUAN-DE-HIEU.md`. Mọi ví dụ tay và đáp án quiz tính lại: SES (10, 12, 11, 13) α = 0,5 → khớp 10, 11, 11,
SSE 8, mức 12 (khớp test); tự kiểm tra 4.1 → 21,25; Holt 18, 20; damped 17,6 / 18,88 và 52 / 53; ETS(A,N,N) σ 10, α 0,5, h 3 → 12,25, ± 24;
tự kiểm tra 4.4 → 5,66; Theta 17, 18 và 103 / 106 / 109; quiz 5 → 54,4; quiz 6 → 209 / 217,1 / 224,39; quiz 7 → 7,81, (84,7; 115,3).

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 3.335 → 3.536 | 11 | 0 | 2 | 3 | 10/10 có căn cứ | khó: "FPP §8.4 tính thêm xu hướng nhân nên có 30" sai nguồn (FPP3 có 18; 30 là của Hyndman và cộng sự 2008 / FPP2); tự kiểm tra 4.6 và quiz 10 tính "thiếu hàng" bằng cả phần nằm ngoài khoảng (đúng là khoảng một nửa, phía trên). Nhỏ: "mô hình sinh" chưa dạy; FPP chưa mở tên; SSE/ME/DM chưa trong bảng Từ mới |
| 2 | sau sửa | 11 | **0** | **0** | 0 | 10/10 | viết lại câu họ ETS; sửa lập luận thiếu hàng ở cả tài liệu lẫn quiz; thêm SSE, ME, DM vào bảng; "Khi nào dùng" cho 4.1, 4.2, 4.5 (bù độ dài bằng nội dung thật, không độn) |
| rà gọn | biên tập viên | — | — | — | — | — | 0 chỗ thừa đáng kể |

Căn cứ quiz: 1, 5, 9 → 4.1; 6 → 4.2; 2 → 4.3; 3, 4, 7 → 4.4; 8 → 4.5; 10 → 4.6. `kiem_de_hieu.py 16` 0.

## Đọc thử độc lập (Phase 18, 2026-09-19)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: bảng SES (11, 11, 12; SSE 8); Holt 18 / 20, damped
17,6 / 18,88; lệch Holt 1,65 / 1,69 / 1,70% (so thư viện); 47,6 / 31,4 = 1,52; 2,13 / 3,23 = 0,66; ETS(A,N,N) 150 → 12,25 → ± 24; 18 tổ hợp;
Theta 17 / 18; 28% / 2 = 14% ≈ 2,8 × 5%; mọi "Tự kiểm tra"; quiz 5–8. Khớp hết.

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.6 hình, Đọc bảng | "hai mức danh nghĩa" | 1 | "danh nghĩa" không định nghĩa; đoán được là 80%, 95% | nhỏ |
| 2 | Nhắc lại | "Từ buổi 15: … Khoảng dự báo 80%" | 8 | buổi 15 không dạy khoảng dự báo | nhỏ |
| 3 | 4.4 | "± 1,96 × 12,25" | 8 | 1,96 cho 95% không nhắc (buổi 2); dùng được như hằng số | nhỏ |
| 4 | 4.5 | "đường thẳng khớp cả chuỗi" | 1 | cách khớp không nói; ví dụ tuyến tính hoàn hảo nên không cản | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **SES**: $(8, 10, 9)$, α = 0,5, mức đầu 8 → khớp 8, 9; mức cuối 9 → dự báo 9.
- **Holt / damped**: mức 100, dốc 5, $\phi$ = 0,6 → Holt 105, 110; damped 103, 104,8.
- **Cộng hay nhân**: đỉnh +30 ở mức 300; mức 600 → cộng 630, nhân 660.
- **ETS và khoảng**: σ = 2, α = 1, $h$ = 4 → phương sai 4 × 4 = 16, độ lệch chuẩn 4.
- **Theta**: mức SES 50, đường thẳng dốc 4 → 52, 54.
- **Tỷ lệ phủ**: khoảng 80% phủ 60% → quá hẹp, thiếu hàng gấp đôi dự tính.

### C. Quiz mù

1 A · 2 B · 3 A · 4 B · 5 50 / 54; dự báo 54,4 · 6 210, 220, 230; 209; 217,1; 224,39 · 7 5 / 7,81; (84,7; 115,3) · 8 Theta 33,5 / 35; Holt 35 / 38 ·
9 giá trị khớp nhìn trộm $y_t$ · 10 DM p 0,49 chưa có bằng chứng; khoảng 95% chỉ phủ 83,5%. Căn cứ: 1, 5, 9 → 4.1; 6 → 4.2; 2 → 4.3; 3, 4, 7
→ 4.4; 8 → 4.5; 10 → 4.6. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 0 / nhỏ 4. Sửa một điều: nói "danh nghĩa" nghĩa là mức khoảng hứa.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý.

### Chấm, sửa, đọc lại

**Quiz mù 10/10**, đáp án của ta đúng. Sửa: hình tỷ lệ phủ "mức danh nghĩa (mức khoảng hứa phủ: 80%, 95%)"; dòng "Khoảng dự báo 80%" chuyển lên
nhóm "Từ buổi 5–6 và 14" (buổi 14 nay định nghĩa khoảng dự báo). Đọc lại mục 2 và 4.6: không vướng mới.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 18 đọc mù | 3.602 | 11 | 0 | 0 | 4 | 10/10 | 0 |
| sau sửa, đọc lại | 3.608 | 11 | **0** | **0** | 2 | 10/10 | 0 |

**Đạt.** `kiem_de_hieu.py 16` 0.
