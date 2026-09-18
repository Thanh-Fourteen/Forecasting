# Tổng quan tiến độ, thứ tự làm, ước lượng, rủi ro

## Progress Summary

| Phase | Nội dung | Deliverable | Trạng thái |
|---|---|---|---|
| [0](phase-00.md) | Hạ tầng khoá học | lộ trình, todos, tool PDF, sinh_nen, lay_du_lieu, kiểm tra, khuôn buổi, MOI-TRUONG, phụ lục A–E | ✅ (còn push remote) |
| [1](phase-01.md) | Khung trợ giúp & dữ liệu | tools/khung/ + danh mục dữ liệu có giấy phép + mirror | ✅ (còn M5 chờ luật Kaggle) |
| [2](phase-02.md) | Buổi 1–3 nền móng | 3 buổi · M0 | ✅ |
| [3](phase-03.md) | Buổi 4–8 đọc dữ liệu | 5 buổi + Phụ lục C | ✅ |
| [4](phase-04.md) | Buổi 9–13 chuẩn bị dữ liệu | 5 buổi + dự án giữa chặng 1 · M1 | ✅ (chưa đạt chuẩn dễ hiểu → Phase 9) |
| **[5](phase-05.md)** | **Chuẩn dễ hiểu** | CHUAN-DE-HIEU.md + kiem_de_hieu.py + khuôn buổi + Phụ lục E + mẫu chuẩn | ✅ |
| **[6](phase-06.md)** | **Viết lại buổi 1–3** | 3 buổi + Phụ lục A, B — đọc thử đạt | ✅ |
| **[7](phase-07.md)** | **Rút gọn buổi 1–3** | chuẩn "gọn" D13 + công cụ kiểm + buổi 1–3, Phụ lục A, B cắt thừa — đọc thử vẫn đạt; bỏ make → `lab.py`, `code/lab.ipynb`, conda qua `--pip` | ✅ |
| **[8](phase-08.md)** | **Viết lại buổi 4–8** | 5 buổi + Phụ lục C — đọc thử đạt | 🔲 |
| **[9](phase-09.md)** | **Viết lại buổi 9–13** | 5 buổi + đề dự án giữa chặng 1 + Phụ lục D — đọc thử đạt | 🔲 |
| [10](phase-10.md) | Buổi 14–17 đánh giá, ETS, ARIMA | 4 buổi + Phụ lục D | 🔲 |
| [11](phase-11.md) | Buổi 18–21 hồi quy, gián đoạn, đa biến, tài chính | 4 buổi · M2 | 🔲 |
| [12](phase-12.md) | Buổi 22–24 machine learning | 3 buổi + dự án giữa chặng 2 · M3 | 🔲 |
| [13](phase-13.md) | Buổi 25–28 bất định | 4 buổi · M4 | 🔲 |
| [14](phase-14.md) | Buổi 29–33 deep learning | 5 buổi · M5 | 🔲 |
| [15](phase-15.md) | Buổi 34–37 foundation model & LLM | 4 buổi · M6 | 🔲 |
| [16](phase-16.md) | Buổi 38–40 nhân quả & quyết định | 3 buổi | 🔲 |
| [17](phase-17.md) | Buổi 41–43 production | 3 buổi · M7 | 🔲 |
| [18](phase-18.md) | Dự án cuối | 3 đề + rubric + bộ chấm dữ liệu tương lai + ngày dữ liệu hỏng + lời giải | 🔲 |
| [19](phase-19.md) | Đánh giá | ngân hàng 440 câu + 2 đề thực hành + đề đọc biểu đồ + đề tìm rò rỉ | 🔲 |
| [20](phase-20.md) | Xuất bản & đóng gói | 44 PDF + 44 zip + README | 🔲 |
| [21](phase-21.md) | Kiểm định chất lượng | báo cáo chạy thử toàn khoá + bài kiểm tra độc lập/CPU/không API key + đọc thử | 🔲 |
| | **TỔNG** | **44 buổi · 44 PDF · 2 dự án giữa chặng · 1 dự án cuối** | **8/22 phase** |

## Thứ tự làm bắt buộc
Phase 0 → 1 trước tiên (mọi buổi đều dựa vào: `sinh_nen.py`, `lay_du_lieu.py`, `kiem_ro_ri`,
danh mục dữ liệu phải có trước khi soạn buổi đầu tiên).

**Phase 5 → 9 (viết lại cho dễ hiểu, rồi rút gọn) làm TRƯỚC Phase 10**: chuẩn mới phải có và được thử trên 13 buổi đã viết
trước khi soạn buổi mới — nếu không, 31 buổi còn lại lặp đúng lỗi cũ. Phase 2 → 17 theo đúng thứ tự buổi. **Lý do là mạch kiến thức và quy trình sản xuất, không phải
phụ thuộc file:** khung `tools/khung/` được mở rộng dần (buổi 15 thêm backtest, buổi 25 thêm chỉ
số xác suất…) và mỗi lần mở rộng phải chạy lại `sinh_nen.py` cho các buổi đã có. Sinh xong thì
`tv/` nằm vật lý trong buổi, **buổi N không còn dính gì tới buổi khác**.

Phase 18–19 làm song song được sau Phase 17. Phase 20 → 21 cuối cùng, không đảo.

**Muốn làm bản ngắn?** Lõi 21 buổi (1–21) + dự án giữa chặng 1 và 2 đã là một khoá dự báo thống
kê hoàn chỉnh (M0–M3). Các cụm khác xem bảng "Học theo cụm" trong lộ trình.

## Ước lượng
| Phase | Buổi | Công sức |
|---|---|---|
| 0–1 | — | 4–5 ngày (khung, danh mục dữ liệu, rà giấy phép ~25 bộ, mirror) |
| [5](phase-05.md) | — | 1–2 ngày (chuẩn, công cụ kiểm, Phụ lục E, mẫu chuẩn) |
| 6, 8–9 | viết lại 13 buổi | ~0,5–1 ngày/buổi (lý thuyết + quiz; lab/code giữ nguyên) |
| [7](phase-07.md) | rút gọn 3 buổi + 2 phụ lục | 1–2 ngày (D13, công cụ kiểm, cắt thừa, đọc thử lại) |
| 2–4, 10–11 | 21 buổi | ~1,5 ngày/buổi (nhiều hình, nhiều thí nghiệm "chứng minh bằng số") |
| 12–13 | 7 buổi + dự án giữa chặng 2 | ~2 ngày/buổi (dữ liệu lớn, bộ chấm dữ liệu tương lai) |
| 14–15 | 9 buổi | ~2,5 ngày/buổi (huấn luyện CPU chậm, hệ sinh thái đổi nhanh, research nặng) |
| 16–17 | 6 buổi | ~2 ngày/buổi |
| 18–21 | — | 7–9 ngày (dự án cuối cần 3 ngày dự báo trực tiếp thật để thử bộ chấm) |

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
