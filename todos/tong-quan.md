# Tổng quan tiến độ, thứ tự làm, ước lượng, rủi ro

## Progress Summary

| Phase | Nội dung | Deliverable / loại (DT = đọc thử độc lập, RS = research riêng) | Trạng thái |
|---|---|---|---|
| [0](phase-00.md) | Hạ tầng khoá học | lộ trình, todos, tool PDF, sinh_nen, lay_du_lieu, kiểm tra, khuôn buổi, MOI-TRUONG, phụ lục A–E | ✅ (còn push remote) |
| [1](phase-01.md) | Khung trợ giúp & dữ liệu | tools/khung/ + danh mục dữ liệu có giấy phép + mirror | ✅ (còn M5 chờ luật Kaggle) |
| [2](phase-02.md) | Buổi 1–3 nền móng | 3 buổi · M0 | ✅ |
| [3](phase-03.md) | Buổi 4–8 đọc dữ liệu | 5 buổi + Phụ lục C | ✅ |
| [4](phase-04.md) | Buổi 9–13 chuẩn bị dữ liệu | 5 buổi + dự án giữa chặng 1 · M1 | ✅ (đạt chuẩn dễ hiểu ở Phase 12–15) |
| **[5](phase-05.md)** | **Chuẩn dễ hiểu** | CHUAN-DE-HIEU.md + kiem_de_hieu.py + khuôn buổi + Phụ lục E + mẫu chuẩn | ✅ |
| **[6](phase-06.md)** | **Viết lại buổi 1–3** | 3 buổi + Phụ lục A, B — đọc thử đạt | ✅ |
| **[7](phase-07.md)** | **Rút gọn buổi 1–3** | chuẩn "gọn" D13 + công cụ kiểm + buổi 1–3, Phụ lục A, B cắt thừa — đọc thử vẫn đạt; bỏ make → `lab.py`, `code/lab.ipynb`, conda qua `--pip` | ✅ |
| [8](phase-08.md) | Viết lại buổi 4–5 + Phụ lục C | 2 buổi + Phụ lục C | ✅ |
| [9](phase-09.md) | Viết lại buổi 6–7 | 2 buổi | ✅ |
| [10](phase-10.md) | Viết lại buổi 8 | 1 buổi | ✅ |
| [11](phase-11.md) | Đọc thử độc lập buổi 4–8 + Phụ lục C | DT — 6 tài liệu đạt (0 chặn, quiz mù 50/50) | ✅ |
| [12](phase-12.md) | Viết lại buổi 9–10 | 2 buổi — 0 chặn, quiz 10/10; sửa code đặc trưng + bản đồ PCA buổi 9 | ✅ |
| [13](phase-13.md) | Viết lại buổi 11–12 | 2 buổi — 0 chặn, quiz 10/10 | ✅ |
| [14](phase-14.md) | Viết lại buổi 13 + đề dự án giữa chặng 1 + Phụ lục D | buổi 13 0 chặn, quiz 10/10; bộ chấm lỗi cài sẵn siết khớp tệp + khoảng | ✅ |
| [15](phase-15.md) | Đọc thử độc lập buổi 9–13 + dự án giữa chặng 1 + Phụ lục D | DT — 7 tài liệu đạt (0 chặn, quiz mù 50/50); sửa `kiem_nhieu_muc_tieu` buổi 13 | ✅ |
| [16](phase-16.md) | Buổi 14–15 · Baseline, chỉ số, backtest | 2 buổi (15 soạn mới: bộ backtest cả khoá + 9 test) · Phụ lục D thêm ví dụ thật | ✅ |
| [17](phase-17.md) | Buổi 16–17 · ETS, Theta, ARIMA | 2 buổi soạn mới; mọi mô hình so seasonal naive có DM trên 366 chuỗi | ✅ |
| [18](phase-18.md) | Đọc thử độc lập buổi 14–17 | DT — 5 tài liệu đạt (0 chặn, quiz mù 40/40); định nghĩa "khoảng dự báo" ở buổi 14 | ✅ |
| [19](phase-19.md) | Buổi 18–19 · Hồi quy động, nhu cầu gián đoạn | 2 buổi soạn mới; Prophet 1.4.0 vào bảng phiên bản; hồi quy động ngang seasonal naive trên ERCOT (báo trung thực); chi phí tồn kho ≠ RMSSE | ✅ |
| [20](phase-20.md) | Buổi 20–21 · Đa biến & nowcasting, tài chính | cột mốc M2; nowcast bằng vintage thật (Philadelphia Fed); demo đoán giá thua naive; cơ chế `noi_them` | ✅ |
| [21](phase-21.md) | Đọc thử độc lập buổi 18–21 | DT — 4 buổi đạt (0 chặn, quiz mù 39/40 → 40/40); Lab buổi 18, 20, 21 chỉ rõ lệnh thư viện cần viết (SARIMAX bỏ 13 phần dư đầu, Johansen, quantile Student-t) | ✅ |
| [T1](phase-t1.md) | Tóm tắt buổi 1–3 | mẫu chuẩn khung thẻ; `xuat_pdf.py --tom-tat` | ✅ |
| [T2](phase-t2.md) | Tóm tắt buổi 4–6 | 3 tóm tắt + PDF | 🔲 |
| [T3](phase-t3.md) | Tóm tắt buổi 7–9 | 3 tóm tắt + PDF | 🔲 |
| [T4](phase-t4.md) | Tóm tắt buổi 10–12 | 3 tóm tắt + PDF | 🔲 |
| [T5](phase-t5.md) | Tóm tắt buổi 13–15 | 3 tóm tắt + PDF | 🔲 |
| [T6](phase-t6.md) | Tóm tắt buổi 16–18 | 3 tóm tắt + PDF | 🔲 |
| [T7](phase-t7.md) | Tóm tắt buổi 19–21 | 3 tóm tắt + PDF | 🔲 |
| [22](phase-22.md) | Buổi 22–23 · Dự báo thành hồi quy, gradient boosting |  | 🔲 |
| [23](phase-23.md) | Buổi 24 + dự án giữa chặng 2 | cột mốc M3 | 🔲 |
| [24](phase-24.md) | Đọc thử độc lập buổi 22–24 + dự án giữa chặng 2 | DT | 🔲 |
| [25](phase-25.md) | Buổi 25–26 · Dự báo xác suất, conformal |  | 🔲 |
| [26](phase-26.md) | Buổi 27–28 · Bayes & GP, dự báo phân cấp | cột mốc M4 | 🔲 |
| [27](phase-27.md) | Đọc thử độc lập buổi 25–28 | DT | 🔲 |
| [28](phase-28.md) | Research deep learning (buổi 29–33) | RS | 🔲 |
| [29](phase-29.md) | Buổi 29–30 · Nền DL, N-BEATS … TiDE |  | 🔲 |
| [30](phase-30.md) | Buổi 31–32 · Transformer, mô hình sinh |  | 🔲 |
| [31](phase-31.md) | Buổi 33 · Không gian–thời gian & thời tiết AI | cột mốc M5 | 🔲 |
| [32](phase-32.md) | Đọc thử độc lập buổi 29–33 | DT | 🔲 |
| [33](phase-33.md) | Research foundation model & LLM (buổi 34–37) | RS | 🔲 |
| [34](phase-34.md) | Buổi 34–35 · Foundation model, fine-tune & benchmark |  | 🔲 |
| [35](phase-35.md) | Buổi 36–37 · LLM & agent, dự báo sự kiện | cột mốc M6 | 🔲 |
| [36](phase-36.md) | Đọc thử độc lập buổi 34–37 | DT | 🔲 |
| [37](phase-37.md) | Buổi 38–39 · Tác động can thiệp, kịch bản & what-if |  | 🔲 |
| [38](phase-38.md) | Buổi 40 · Dự báo → quyết định |  | 🔲 |
| [39](phase-39.md) | Đọc thử độc lập buổi 38–40 | DT | 🔲 |
| [40](phase-40.md) | Buổi 41–42 · Pipeline tái lập, phục vụ quy mô lớn |  | 🔲 |
| [41](phase-41.md) | Buổi 43 · Giám sát & drift | cột mốc M7 | 🔲 |
| [42](phase-42.md) | Đọc thử độc lập buổi 41–43 | DT | 🔲 |
| [43](phase-43.md) | Dự án cuối (a) · Đề, rubric, bộ chấm |  | 🔲 |
| [44](phase-44.md) | Dự án cuối (b) · Ngày dữ liệu hỏng, lời giải mẫu, chạy thử thật |  | 🔲 |
| [45](phase-45.md) | Đánh giá (a) · Ngân hàng câu hỏi, đề đọc biểu đồ |  | 🔲 |
| [46](phase-46.md) | Đánh giá (b) · Đề thực hành, đề tìm rò rỉ |  | 🔲 |
| [47](phase-47.md) | Xuất bản & đóng gói |  | 🔲 |
| [48](phase-48.md) | Kiểm định chất lượng |  | 🔲 |
| | **TỔNG** | **44 buổi · 44 PDF · 2 dự án giữa chặng · 1 dự án cuối** | **23/56 phase** |

## Thứ tự làm bắt buộc
Phase 0 → 1 trước tiên (mọi buổi đều dựa vào: `sinh_nen.py`, `lay_du_lieu.py`, `kiem_ro_ri`,
danh mục dữ liệu phải có trước khi soạn buổi đầu tiên).

**Không dùng subagent (từ 2026-09-18) → phase nhỏ hơn.** Mỗi phase soạn 1–2 buổi; sau mỗi cụm có phase **DT** (đọc thử độc
lập trong phiên mới, thay "mắt mới" của subagent); cụm đổi nhanh (deep learning, foundation model & LLM) có phase **RS**
(research riêng) trước khi soạn. Định nghĩa: KHỐI CHUNG trong `quy-uoc.md`.

**Phase 5 → 15 (chuẩn dễ hiểu, viết lại, rút gọn, đọc thử độc lập buổi 1–13) làm TRƯỚC Phase 16**: chuẩn mới phải có và được
thử trên 13 buổi đã viết trước khi soạn buổi mới — nếu không, 31 buổi còn lại lặp đúng lỗi cũ. Phase 2 → 42 theo đúng thứ tự
buổi. **Lý do là mạch kiến thức và quy trình sản xuất, không phải phụ thuộc file:** khung `tools/khung/` được mở rộng dần (buổi 15
thêm backtest, buổi 25 thêm chỉ số xác suất…) và mỗi lần mở rộng phải chạy lại `sinh_nen.py` cho các buổi đã có. Sinh xong thì
`tv/` nằm vật lý trong buổi, **buổi N không còn dính gì tới buổi khác**. Phase DT của một cụm làm ngay sau phase soạn cuối của cụm đó.

Phase 43–46 (dự án cuối, đánh giá) làm song song được sau Phase 42. Phase 47 → 48 cuối cùng, không đảo.

**Muốn làm bản ngắn?** Lõi 21 buổi (1–21) + dự án giữa chặng 1 và 2 đã là một khoá dự báo thống
kê hoàn chỉnh (M0–M3). Các cụm khác xem bảng "Học theo cụm" trong lộ trình.

## Ước lượng
| Phase | Buổi | Công sức |
|---|---|---|
| 0–1 | — | 4–5 ngày (khung, danh mục dữ liệu, rà giấy phép ~25 bộ, mirror) |
| [5](phase-05.md) | — | 1–2 ngày (chuẩn, công cụ kiểm, Phụ lục E, mẫu chuẩn) |
| 6, 8–10, 12–14 | viết lại 13 buổi | ~0,5–1 ngày/buổi (lý thuyết + quiz; lab/code giữ nguyên) |
| [7](phase-07.md) | rút gọn 3 buổi + 2 phụ lục | 1–2 ngày (D13, công cụ kiểm, cắt thừa, đọc thử lại) |
| DT (11, 15, 18, 21, 24, 27, 32, 36, 39, 42) | đọc thử độc lập mỗi cụm | ~0,3 ngày/buổi |
| RS (28, 33) | research riêng DL, FM & LLM | 1–2 ngày/phase |
| 2–4, 16–20 | 21 buổi | ~1,5 ngày/buổi (nhiều hình, nhiều thí nghiệm "chứng minh bằng số") |
| 22–26 | 7 buổi + dự án giữa chặng 2 | ~2 ngày/buổi (dữ liệu lớn, bộ chấm dữ liệu tương lai) |
| 29–31, 34–35 | 9 buổi | ~2,5 ngày/buổi (huấn luyện CPU chậm, hệ sinh thái đổi nhanh) |
| 37–41 | 6 buổi | ~2 ngày/buổi |
| 43–48 | — | 7–9 ngày (dự án cuối cần 3 ngày dự báo trực tiếp thật để thử bộ chấm) |

## Ghi chú rủi ro
- **Giấy phép dữ liệu**: M5 (Kaggle), OpenAQ (theo nhà cung cấp) có điều khoản riêng; **FRED cấm dùng cho ML** (Phase 1) —
  mọi bộ hạn chế phải có dự phòng mở. **Không mirror bộ cấm phân phối lại**
- **Nguồn dữ liệu đổi hoặc sửa số liệu lùi** (EIA-930 sửa số liệu, API OpenAQ đổi phiên bản) → sha256 không
  khớp. Chống bằng mirror snapshot cố định cho bộ được phép; bài dự báo trực tiếp ghi rõ là không cố định
- **Trạm OpenAQ Việt Nam có thể ngừng hoạt động** — dự án giữa chặng 1 và đề C phải có snapshot mirror + trạm dự phòng.
  *Đã xảy ra:* trạm Đại sứ quán/Lãnh sự quán Mỹ (AirNow) ngừng từ 04/03/2025. Điều khoản OpenAQ: "Downloading data is
  strictly prohibited unless done through registered and authorized use" + phải theo giấy phép từng nhà cung cấp →
  mirror dữ liệu OpenAQ chỉ khi giấy phép nhà cung cấp cho phân phối lại (`redistributionAllowed`) — rà ở Phase 1
- **Open-Meteo gói miễn phí chỉ cho mục đích phi thương mại** (CC BY 4.0 cho dữ liệu, nhưng API free tier non-commercial) —
  lớp thu phí phải dùng snapshot mirror hoặc gói trả phí; rà ở Phase 1
- **UCI tải rất chậm** (đo 10–20 KB/s, không Content-Length, không hỗ trợ Range) — bộ UCI > 10 MB bắt buộc có mirror
- **Buổi 29–35 nặng tài nguyên**: CPU chạy được nhưng chậm — cấu hình rút gọn cho máy 8 GB làm song song với bản chuẩn
- **Buổi 34–37 lỗi thời nhanh nhất** (foundation model và LLM ra bản mới hàng tháng): rà mỗi 6 tháng;
  phần còn lại mỗi 12 tháng. Tài liệu viết theo **nguyên lý + cách kiểm chứng**, tên model là ví dụ
- **Buổi 36–37 tốn tiền API** nếu dùng model thương mại: bắt buộc nhánh model mở local + bản ghi phản hồi;
  đặt trần chi phí trong tài liệu
- **Rò rỉ thời gian của LLM** (buổi 37): model mới có mốc cắt kiến thức muộn hơn → tập câu hỏi sạch phải
  cập nhật mỗi lần đổi model
- **Tính tái lập của DL và LLM**: test chấm cho phép sai số nhỏ có ngưỡng ghi rõ, không so bằng tuyệt đối
- **Dự án giữa chặng 2 và dự án cuối phụ thuộc lịch dữ liệu thật** — lên lịch trước, có phương án dùng
  holdout giám khảo giữ nếu nguồn ngừng cập nhật
- **Dễ hiểu kéo dài chữ** (phát hiện 2026-09-18, sau Phase 6): mỗi vòng đọc thử chỉ thêm giải thích → buổi 1–3 dài
  dòng. Chống bằng D13 + bước "Rà gọn" (lượt đọc vai biên tập viên) + trần `do_dai` — làm ở Phase 7, áp dụng từ Phase 8
- **pandas 3 vs hệ Nixtla** (phát hiện Phase 0): statsforecast/utilsforecast/mlforecast/autogluon chưa hỗ trợ
  pandas 3 → hai dòng pandas song song trong khoá. Mỗi phase rà lại; khi Nixtla hỗ trợ thì gỡ `[[rang_buoc]]`
  và chạy lại `sinh_nen.py --tat-ca --nang-cap`
- **Rủi ro lớn nhất của thiết kế độc lập**: 44 bản `tv/` và 44 `uv.lock` lệch nhau. Chống bằng đúng một
  cách — **luôn sinh bằng `sinh_nen.py`, không bao giờ sửa tay**
