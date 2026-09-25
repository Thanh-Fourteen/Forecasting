# Nhật ký research — Buổi 22: Biến dự báo thành bài toán hồi quy

<!-- BƯỚC 0 của giao thức research (todos/quy-uoc.md). KHÔNG vào zip phát học viên. -->

- **Ngày research:** 2026-09-24 (Phase 22). Buổi soạn mới hoàn toàn (thư mục tạo từ khuôn).
- **Người/phiên:** Phase 22, một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | Montero-Manso, P. & Hyndman, R.J. (2021). Principles and algorithms for forecasting groups of time series: locality and globality. *IJF* 37(4): 1632–1653. https://arxiv.org/abs/2008.00444 — global không hạn chế hơn local (cùng tạo được mọi dự báo local, không cần giả định các chuỗi giống nhau); độ phức tạp của local tăng theo số chuỗi, global thì không → global được phép phức tạp hơn (lag dài hơn nhiều); global tuyến tính đạt độ chính xác cạnh tranh với ít hơn hai bậc độ lớn số tham số | bài gốc | 2026-09-24 | 4.2 |
| 2 | Taieb, S.B., Bontempi, G., Atiya, A.F. & Sorjamaa, A. (2012). A review and comparison of strategies for multi-step ahead time series forecasting based on the NN5 forecasting competition. *Expert Systems with Applications* 39(8): 7067–7083. https://arxiv.org/abs/1108.3259 — recursive / direct / DirRec / MIMO / DIRMO; 111 chuỗi NN5; chiến lược nhiều đầu ra (MIMO) tốt nhất; khử mùa vụ cải thiện đều; bằng chứng recursive vs direct trái chiều giữa các nghiên cứu | bài gốc (tổng quan + so sánh) | 2026-09-24 | 4.3 |
| 3 | Makridakis, Spiliotis & Assimakopoulos (2022). M5 accuracy competition: Results, findings, and conclusions. *IJF* 38(4). Bản tiền in: https://statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf — Finding 3 "cross-learning": mọi đội top 50 đều học chung nhiều chuỗi; đội thắng trộn mô hình recursive và non-recursive (recursive chính xác hơn trung bình nhưng kém ổn định hơn) | bài tổng kết | 2026-09-24 | 4.2, 4.3, Đọc thêm |
| 4 | Bergmeir, C., Hyndman, R.J. & Koo, B. (2018). A note on the validity of cross-validation for evaluating autoregressive time series prediction. *CSDA* 120: 70–83. https://robjhyndman.com/publications/cv-time-series/ | bài gốc | 2026-09-24 | Lỗi thường gặp (buổi 23 dùng kỹ) |
| 5 | mlforecast 1.1.0 release notes (2026-07-10): https://github.com/Nixtla/mlforecast/releases — thêm "horizon specific features", `LookupLag`, `partition_by` cho lag transform; 1.0.3 (2026-02-25): direct với các tầm riêng lẻ. API dùng trong buổi: `MLForecast(models, freq, lags, lag_transforms, date_features, target_transforms)`, `.cross_validation(df, h, n_windows, step_size)`, `fit(..., max_horizon=h)` = chiến lược direct | changelog | 2026-09-24 | 4.6, code |
| 6 | Tài liệu mlforecast — target transforms (`Differences`, `LocalStandardScaler`), lag transforms (`RollingMean`): https://nixtlaverse.nixtla.io/mlforecast/ | tài liệu chính thức | 2026-09-24 | 4.5, 4.6 |
| 7 | LightGBM Parameters (bản 4.7): https://lightgbm.readthedocs.io/en/latest/Parameters.html | tài liệu chính thức | 2026-09-24 | 4.6 |
| 8 | scikit-learn 1.9 — cây quyết định dự báo hằng số ở mỗi lá (trung bình mục tiêu của các mẫu học trong lá) nên không cho giá trị ngoài khoảng mục tiêu đã thấy; `RandomForestRegressor` hỗ trợ nhiều đầu ra (một cây chung cho cả vector) | tài liệu chính thức | 2026-09-24 | 4.3 (MIMO), 4.5 |
| 9 | Damato, Rubattu, Azzimonti & Corani (2026). Intermittent time series forecasting: local vs global models. https://arxiv.org/abs/2601.14031 — trên hơn 40.000 chuỗi thật, mô hình global thắng local rõ | bài mới (12 tháng) | 2026-09-24 | 4.2 (bối cảnh) |
| 10 | Godahewa et al. (2021), Monash Archive — Kaggle Web Traffic "without missing values": 145.063 chuỗi ngày, 2015-07-01 → 2017-09-10, ô thiếu đã thay bằng 0 (ghi trong đầu tệp .tsf) | dữ liệu | 2026-09-24 | toàn buổi |

## Phiên bản đã xác minh (PyPI 2026-09-24, khớp `tools/nen/phien-ban.toml`)

| Thư viện | Phiên bản | Ghi chú |
|---|---|---|
| mlforecast | 1.1.0 (2026-07-10) | mới nhất; yêu cầu pandas < 3 → ràng buộc chung pandas 2.3.3 |
| lightgbm | 4.7.0 (2026-07-18) | mới nhất |
| statsforecast | 2.1.1 (2026-07-16) | mới nhất |
| scikit-learn | 1.9.1 (2026-09-10) | mới nhất |
| utilsforecast | 0.2.16 | mới nhất |

## Dữ liệu

| Bộ | Danh mục | Giấy phép | Ghi chú |
|---|---|---|---|
| `monash-web-traffic` | sha256 `29912f202cb8`, 145 MB zip | CC BY 4.0 (Zenodo) | Không mirror (Zenodo có DOI). Tên trang bị Monash thay bằng T1…T145063. Buổi đọc 12.500 chuỗi đầu tệp, giữ 10.000 chuỗi đầu tiên có dưới 5% ngày bằng 0 trong phần học (0 ở đây phần lớn là ô thiếu đã bị thay) |

## Phát hiện mới / lỗi hiểu sai phổ biến

- "Direct thì phải lag ≥ h": đúng khi lag tính **từ ngày cần dự báo**; tính từ mốc dự báo thì lag 1 luôn hợp lệ (mlforecast `max_horizon` làm vậy). Hiểu lầm hay gặp là dựng bảng một lần bằng `shift(1..L)` rồi dùng cho mọi h → rò rỉ. Đưa vào 4.4 + Lỗi thường gặp.
- MIMO với hồi quy tuyến tính bình phương tối thiểu cho **đúng** kết quả của direct (mỗi đầu ra giải riêng, cùng đầu vào); MIMO chỉ khác khi mô hình dùng chung cấu trúc cho mọi đầu ra (cây nhiều đầu ra, mạng nơ-ron). Vì vậy buổi dùng rừng ngẫu nhiên cho cả ba chiến lược.
- Cây (và LightGBM) không ngoại suy: dự báo nằm trong khoảng mục tiêu đã thấy → chuỗi có xu hướng phải sai phân hoặc chuẩn hoá theo mức gần nhất trước khi đưa vào cây.
- Mô hình global cần chuẩn hoá theo chuỗi (log, trừ mức) để các chuỗi khác cỡ học chung được.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Local là AutoETS **không xu hướng** (`model="ZNA"`, mùa vụ 7) | nhỏ | ETS tự chọn đủ dạng chạy 1.000 chuỗi × 3 cửa sổ mất 84 s trên 12 nhân (10.000 chuỗi ~15 phút, máy 4 nhân ~45 phút). Thử 300 chuỗi: bật xu hướng chậm 6 lần mà sai số gần như không đổi (xem số dưới) → dùng ZNA, ghi rõ trong tài liệu |
| Không dùng Online Retail II ở buổi 22 | nhỏ | Buổi 23 dùng; buổi 22 đủ với Web Traffic |
| RandomForest (không phải LightGBM) cho phần ba chiến lược | nhỏ | MIMO cần mô hình nhiều đầu ra; LightGBM không có. Dùng cùng một loại mô hình cho cả ba để so công bằng; 300 trang, mốc học mỗi 7 ngày, 50 cây để chạy ~1 phút |
| Không có bảng "10.000 chuỗi" cho phần ba chiến lược | nhỏ | 300 trang đủ thấy khác biệt theo $h$; 10.000 trang × 14 mô hình direct quá nặng cho máy học viên |

## Số liệu thật (`dap-an/ve_hinh.py`, seed 0; máy soạn 12 nhân)

| Đại lượng | Giá trị |
|---|---|
| Dữ liệu | 10.000 trang (đọc 12.520 chuỗi đầu tệp), 803 ngày 1/7/2015 → 10/9/2017; cutoff 30/7, 13/8, 27/8/2017; H = 14 |
| Ví dụ tay | $(10, 12, 11, 13, 15)$, L = 2 → X = [[12, 10], [11, 12], [13, 11]], y = [11, 13, 15]; recursive "trung bình 2 số" từ (10, 20): 15; 17,5; 16,25 |
| Một trang (T1), rừng local 28 lag, cutoff đầu | 733 dòng; RMSE thang z 0,4657 (rừng) so với 0,5038 (seasonal naive) |
| Chuẩn hoá | T9775 trung bình 120 ngày cuối 14.394.894 lượt/ngày; T1 25,9 |
| Ba chiến lược, 300 trang, RandomForest 50 cây | tổng RMSE: recursive 0,5131, direct 0,5105, MIMO 0,5105; tuần 1: 0,4946 / 0,4949 / 0,4943; tuần 2: 0,5309 / 0,5256 / 0,5262; h = 1: 0,4548 / 0,4548 / 0,4613; h = 14: 0,5752 / 0,5656 / 0,5735 |
| Direct rò rỉ (code/, `shift(k)`) | tổng 0,4772; tuần 1 0,4757, tuần 2 0,4787; h = 4: 0,423; h = 14: 0,4896 |
| Cây trên chuỗi y = 50 + 2t + nhiễu N(0, 3) | lớn nhất đã thấy 291,5; cây trên mức: 286,5 ở ngày cuối; cây trên sai phân: 313,3; xu hướng thật 316 |
| Global/local 10.000 trang (RMSSE trung bình / trung vị / % thắng SN) | LightGBM 0,916 / 0,763 / 87,6%; LightGBM + Differences([1]) 0,914 / 0,767 / 88,8%; AutoETS(ZNA) 0,951 / 0,776 / 81,3%; SeasonalNaive 1,099 / 0,949; Naive 1,163 / 1,004 / 45,7%. 0 trang bị bỏ (phần học phẳng) |
| LightGBM thắng AutoETS | 58,1% số trang; theo nhóm lượt xem trung vị: 3–14: 0,707 vs 0,714 (52,2%); 15–159: 0,886 vs 0,937 (61,9%); 160–613: 1,029 vs 1,098 (62,4%); ≥ 614: 1,048 vs 1,061 (56,2%) |
| Theo h (RMSE thang z, 10.000 trang) | h = 1: LightGBM 0,354, AutoETS 0,360, SN 0,513; h = 14: 0,492 / 0,518 / 0,604 |
| AutoETS thử 300 trang × 3 cutoff | mặc định ZZZ 26,9 s, ZZA 17,9 s, ZNA 3,0 s; RMSE thang z 0,5492 / 0,5518 / 0,5520 |
| Thời gian | backtest global + local 10.000 trang: 5,5 phút (12 nhân, có tải song song); chiến lược 300 trang ~1 phút; `lab.py check` 9 s |

## Đọc thử (2026-09-24, Phase 22, tự đọc — không subagent)

**Vòng 1 — đọc thử vai học viên mới** (toàn bộ `tai-lieu.md`, chỉ dùng những gì đã viết trước chỗ đang đọc):

| # | Mục | Chỗ vướng | Mức | Đã sửa |
|---|---|---|---|---|
| 1 | 4.1, 4.3 | "RMSE" dùng mà mục 2 chỉ định nghĩa RMSSE | khó | thêm định nghĩa RMSE một câu ở mục 2 |
| 2 | 4.2 | "số tham số" — "tham số" chưa định nghĩa | khó | viết lại: "số con số mô hình phải học" |
| 3 | 4.3 | "vector 14 ngày" | nhỏ | đổi thành "dãy 14 ngày" |
| 4 | 4.4 | "lag phải có k ≥ h" — k vừa là số thứ tự lag trong công thức vừa là khoảng cách | khó | viết lại quy tắc: "mọi số dùng làm đầu vào phải cách ngày τ ít nhất h ngày"; "Tóm lại" cũng sửa |
| 5 | 4.1 | "LightGBM" dùng ở 4.1, hộp "Mượn trước" mãi tới 4.6 | khó | chuyển hộp "Mượn trước" lên 4.1 |
| 6 | 4.4 | "Bắt bằng test": câu "các dòng chưa tới ngày đó cộng 7" khó hiểu | nhỏ | viết lại với ngày $p$ |
| 7 | 4.6 | "RMSSE trung vị" | nhỏ | thêm "(trang đứng giữa)" ở tiêu đề cột |

Kết quả vòng 1: 0 chặn, 3 khó (1, 2, 4, 5 — sửa hết), 3 nhỏ. **Vòng 2** sau sửa: 0 chặn, 0 khó, 1 nhỏ (mục 6 "Lỗi thường gặp" nhắc "trung vị" khi đổi ngược log, đã học ở buổi 5).

**B — giải thích lại bằng ví dụ mới** (tự nghĩ): bảng lag dãy (1, 3, 2, 5), L = 2 → 2 dòng (3, 1) → 2 và (2, 3) → 5; hai trang log₁₀ (7, 7, 8) và (3, 3, 4)
trừ mức ra cùng (−1/3, −1/3, 2/3); recursive H = 5 dùng 4 dự báo ở ngày 5; direct tầm 3 cutoff ngày 20 → lag_1 = ngày 20; cây học nhãn 5, 7, 9
không đoán quá 9; global 58% số trang. Không khái niệm nào "không giải thích được".

**C — quiz có căn cứ:** C1 → 4.1 (ví dụ + tự kiểm tra); C2 → 4.2 (điều kiện cùng thang); C3 → 4.3 (tự kiểm tra); C4 → 4.5 (trực giác); C5 → 4.4
(công thức + nói bằng lời); C6 → 4.2 (ví dụ tay, tự kiểm tra); C7 → 4.5; C8 → 4.3 (bảng ba chiến lược); C9 → 4.4 (hình + "vì sao backtest không tự
báo lỗi"); C10 → 4.6 (bảng theo nhóm). Mọi đáp án tính lại bằng Python (C5 ngày, C6 $10^3$, C9 số lấy từ `cl300_code`, C10 (0,951 − 0,916)/0,951 = 3,7%).
Quiz câu 6 bản đầu có đề làm tròn xấu (mức 1,33) → đổi đề để mức tròn 2.

**Rà gọn (vai biên tập viên):** 3 chỗ: "chênh khoảng 1%" nói ba lần ở 4.3 (Đọc bảng, Khi nào dùng, Tóm lại) → bỏ ở "Khi nào dùng" và "Tóm lại";
"Đọc kết quả" bước 1 và bước 2 chép lại số của 4.1/4.3 → trỏ về mục; ví dụ tay 4.5 bản đầu viết lẫn nhãn và lag → viết lại gọn. Lượt rà cuối: 1 chỗ
thừa nhỏ (câu "Cái giá…" ở 4.2 có thể bỏ), giữ vì nối sang "điều kiện cùng thang".

**Số chữ** (`kiem_de_hieu.dem_chu`): 4.123 → 4.115 sau rà gọn; `kiem_de_hieu.py 22`: 0 vi phạm.

## Đọc thử độc lập (Phase 24, 2026-09-24)

Phiên mới; chỉ mở `tai-lieu.md` + quiz bỏ `<details>` cho tới khi viết xong A–E. Tính lại: 733 dòng (761 ngày tới 30/7/2017 − 28); ví dụ log₁₀
(5,67; +0,33/−0,67); recursive 15 / 17,5 / 16,25; lag direct (cutoff 10, h 3 → ngày 10, 9); cây 25 / 40 và sai phân 50, 60, 70; tuần 2 recursive
÷ direct = 1,0095 (≈ 1%); (0,951 − 0,916)/0,951 = 3,7%; 14 triệu ÷ 26 ≈ 538.000; cutoff 30/7, 13/8, 27/8/2017 đều là Chủ nhật → $h$ = 3, 10 là thứ Tư.
Đối chiếu số trong bài với bảng "Số liệu thật": khớp (0,4657/0,5038; 0,4896/0,5656; 291,5/286,5/313,3/316; 0,914/0,916; 0,354/0,360, 0,492/0,518).

### A. Chỗ vướng (đọc mù)

| # | Mục | Trích | Loại | Vì sao | Mức |
|---|---|---|---|---|---|
| 1 | 4.6 | cấu hình mlforecast (lags, RollingMean, dayofweek) | 4 | 4.2 nói "điều kiện là log, trừ mức"; 4.6 không nói mô hình thắng có trừ mức không (code: chỉ log) | khó |
| 2 | 4.1 | "Trang T1 cho bảng 733 dòng" | 4 | không nói $L$ = 28, không tự ra được 733 | nhỏ |
| 3 | 4.1 Tóm lại | "số kế tiếp là nhãn" | 1 | "nhãn" chưa định nghĩa (bảng ghi "Cần đoán") | nhỏ |
| 4 | 4.2 ví dụ | "hôm kia tụt 10 lần rồi hồi lại" | 3 | ba ngày gần nhất, ngày tụt là ngày giữa; "hôm kia" tính từ đâu | nhỏ |
| 5 | 4.3 hình | "ngày h = 3 và 10 rơi vào cùng thứ" | 4 | thứ mấy, khó hơn so với gì | nhỏ |
| 6 | 4.6 | `model="ZNA"` | 7 | mã không giải thích | nhỏ |
| 7 | 6 | "trung bình trên thang log đổi ngược thành trung vị" | 8 | ý đúng nhưng buổi không dạy | nhỏ |

### B. Giải thích lại (ví dụ số mới)

- **Chuỗi thành bảng**: dãy 1, 3, 2, 5, $L$ = 2 → (3, 1) → 2; (2, 3) → 5.
- **Global + chuẩn hoá**: log₁₀ trang A (2, 4), trang B (5, 7) → trừ mức cả hai thành (−1, +1); đoán "+1" → A 10⁴, B 10⁷.
- **Ba chiến lược**: $H$ = 5, $L$ = 10: recursive ngày 5 dùng 4 dự báo + 6 số thật; direct 5 mô hình; MIMO 1 mô hình ra 5 số.
- **Rò rỉ direct**: cutoff 1/3, $h$ = 4 → đoán 5/3, `lag_1` = 1/3, `lag_2` = 28/2 (năm thường).
- **Cây không ngoại suy**: 5, 7, 9, 11 → cây đứng ≤ 11; sai phân 2 → 13, 15.
- **Global vs local**: trung bình tốt hơn ≠ tốt hơn ở mọi trang (52% ở nhóm nhỏ).

### C. Quiz mù

1 B · 2 C · 3 B · 4 A · 5 B · 6 C · 7 B · 8 C · 9 B · 10 C. Căn cứ: 1 → 4.1; 2, 6 → 4.2; 3, 8 → 4.3; 5, 9 → 4.4; 4, 7 → 4.5; 10 → 4.6 + mục 2. Tất cả "chắc".

### D. Tổng kết

Chặn 0 / khó 1 / nhỏ 6. Nếu chỉ sửa một điều: nói rõ LightGBM ở 4.6 học trên $z$ không trừ mức, mức do cột trung bình 28 ngày mang.

### E. Dài/lặp

Không đoạn nào ≥ 30 chữ lặp ý (các chỗ lặp đã cắt ở Phase 22).

### Chấm, sửa, đọc lại

**Quiz mù 10/10** (đáp án khớp, số tính lại khớp). Sửa bằng viết lại câu: #1 thêm một gạch đầu dòng ở 4.6 "học trên $z$ (đã log), không trừ mức riêng:
cột trung bình 28 ngày đã cho mô hình biết mức"; #2 "khung $L$ = 28, dựng bảng từ dữ liệu tới cutoff đầu" (bỏ số 733 để đoạn không quá 3 con số);
#3 định nghĩa "nhãn" ở câu trượt khung; #4 "ngày giữa"; #5 "cùng rơi vào thứ Tư, khó hơn các ngày khác"; #6 "chữ N ở giữa là không xu hướng".
Giữ #7. Đọc lại toàn bộ: 0 chặn / 0 khó / 1 nhỏ; rà gọn: 0 chỗ thừa đáng kể.

| Vòng | Chữ | Trang | Chặn | Khó | Nhỏ | Quiz | Chỗ thừa |
|---|---|---|---|---|---|---|---|
| Phase 24 đọc mù | 4.115 | 13 | 0 | 1 | 6 | 10/10 | 0 |
| sau sửa, đọc lại | 4.157 | 13 | **0** | **0** | 1 | 10/10 | 0 |
