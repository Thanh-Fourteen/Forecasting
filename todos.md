# Khoá Forecasting in AI — Phased Todo Plan
Mục tiêu: **44 buổi** (cơ bản → nâng cao) | **giáo trình .md + PDF + code chạy được trên dữ liệu thật** | Nguồn lộ trình: [`lo-trinh/lo-trinh-forecasting.md`](lo-trinh/lo-trinh-forecasting.md)

**44 buổi** = 3 nền móng + **10 hiểu & chuẩn bị dữ liệu** + 8 thống kê + 3 ML + 4 bất định + 5 deep learning
+ 4 foundation model & LLM + 3 nhân quả & quyết định + 3 production + 1 dự án cuối.
Kèm **2 dự án giữa chặng** (sau buổi 13 và 24).

Repo: `/home/tony/Tony/Forecasting/` — repo độc lập, mọi đường dẫn dưới đây tính từ gốc repo

**Cách tổ chức kế hoạch** (file này chỉ giữ tiêu đề + trạng thái + prompt, để autoclick theo dõi):

- [`todos/quy-uoc.md`](todos/quy-uoc.md) — **KHỐI CHUNG** (R research · V viết · L lab · Đ đọc thử + rà gọn · X xong phase: mọi prompt
  dưới đây chạy theo nó), giao thức research, **chuẩn dễ hiểu + gọn D1–D13**, cấu trúc
  thư mục, nguyên tắc nội dung, Definition of Done, bảng 44 buổi + chỗ hở cố ý. **Đọc trước mọi phase.**
- [`todos/tong-quan.md`](todos/tong-quan.md) — Progress Summary, thứ tự làm bắt buộc, ước lượng, ghi chú rủi ro
- `todos/phase-NN.md` — chi tiết từng phase (bảng tiến độ, checklist, "Bắt buộc", ghi chú research)

**Quyết định của người dùng (2026-09-18) — áp cho mọi phase:**
- Dễ hiểu nhưng **gọn**; "tường minh quá thành ra dài dòng và khó hiểu" → quy tắc D13 + bước rà gọn bằng biên tập viên.
- Bỏ `make` → `python lab.py up | check | notebook | down` (chạy cả Windows); phát sẵn `code/lab.ipynb`; conda/pip được qua
  `python lab.py up --pip` (`00-nen/requirements.txt` sinh từ `uv.lock`); uv vẫn là cách chính.
- Prompt phase ngắn: yêu cầu chung ở KHỐI CHUNG (`todos/quy-uoc.md`), prompt chỉ ghi phần riêng.

Xong phase: đổi 🔲 → ✅ ở **cả hai** tiêu đề (ở đây và trong `todos/phase-NN.md`), rồi cập nhật Progress Summary
trong `todos/tong-quan.md`.

---

## Phase 0 — Hạ tầng khoá học ✅ (trừ push remote)

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-00.md`](todos/phase-00.md)

### Prompt copy-paste cho Phase 0:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-00.md.
```

---

## Phase 1 — Khung trợ giúp và danh mục dữ liệu ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-01.md`](todos/phase-01.md)

### Prompt copy-paste cho Phase 1:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-01.md.
```

---

## Phase 2 — Buổi 1–3 · Nền móng ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-02.md`](todos/phase-02.md)

### Prompt copy-paste cho Phase 2:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-02.md.
```

---

## Phase 3 — Buổi 4–8 · Đọc dữ liệu: biểu đồ, biến đổi, phân rã, tương quan ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-03.md`](todos/phase-03.md)

### Prompt copy-paste cho Phase 3:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-03.md.
```

---

## Phase 4 — Buổi 9–13 · Chuẩn bị dữ liệu + dự án giữa chặng 1 ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-04.md`](todos/phase-04.md)

### Prompt copy-paste cho Phase 4:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-04.md.
```

---

## Phase 5 — Chuẩn "dễ hiểu": quy tắc, công cụ kiểm, mẫu chuẩn ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-05.md`](todos/phase-05.md)

### Prompt copy-paste cho Phase 5:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-05.md.
```

---

## Phase 6 — Viết lại buổi 1–3 + Phụ lục A, B cho dễ hiểu ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-06.md`](todos/phase-06.md)

### Prompt copy-paste cho Phase 6:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-06.md.
```

---

## Phase 7 — Rút gọn: chuẩn "gọn" D13 + buổi 1–3, Phụ lục A, B ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-07.md`](todos/phase-07.md)

### Prompt copy-paste cho Phase 7:
```
Đã xong — prompt gốc trong git history (commit fe5ba52 trở về trước); kết quả ở todos/phase-07.md.
```

---

## Phase 8 — Viết lại buổi 4–8 + Phụ lục C cho dễ hiểu 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-08.md`](todos/phase-08.md)

### Prompt copy-paste cho Phase 8:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 7 xong → Phase 8: VIẾT LẠI buổi 04–08 + phu-luc/C.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-08.md.
Cụm trọng tâm: đọc biểu đồ, tương quan. ACF, PACF, tính dừng, ADF/KPSS, CCF, prewhitening, mutual information, Granger:
trực giác + ví dụ số nhỏ tính tay TRƯỚC công thức; p-value/kiểm định → "Mượn trước". Tạo code/lab.ipynb. PDF: xuat_pdf.py 4..8.
```

---

## Phase 9 — Viết lại buổi 9–13 + đề dự án giữa chặng 1 + Phụ lục D cho dễ hiểu 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-09.md`](todos/phase-09.md)

### Prompt copy-paste cho Phase 9:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 8 xong → Phase 9: VIẾT LẠI buổi 09–13 + đề du-an-giua-chang/01-eda-lam-sach/ + phu-luc/D.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-09.md.
Cụm trọng tâm: tiền xử lý, khử nhiễu, rò rỉ. Mỗi kỹ thuật: khi nào dùng / KHÔNG dùng (lời thường) + ví dụ số nhỏ + thí
nghiệm có số. Rò rỉ: mỗi kiểu một bảng vài dòng chỉ ô nhìn trộm tương lai. Dự án: chỉ viết lại đề + rubric (ngắn nhất có
thể); lỗi cài sẵn và lời giải KHÔNG vào zip. Tạo code/lab.ipynb. PDF: xuat_pdf.py 9..13.
```

---

## Phase 10 — Buổi 14–17 · Đánh giá, backtest, ETS, ARIMA 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-10.md`](todos/phase-10.md)

### Prompt copy-paste cho Phase 10:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 9 xong → Phase 10: buổi 14–17 (Giai đoạn 2, nửa đầu). Bản nháp 14–17 đã có: giữ code/lab/số, viết lại chữ.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-10.md.
Research riêng: FPP ch. 5, 8, 9; Hyndman & Koehler 2006 (MASE); M5 guide (RMSSE/WRMSSE); Bergmeir & Benítez (CV chuỗi thời
gian); Diebold–Mariano bản Harvey; statsforecast mới nhất (AutoETS, AutoTheta, AutoARIMA, cross_validation).
Riêng: buổi 15 tạo bộ backtest cả khoá dùng — thiết kế kỹ, có test. Mọi mô hình so seasonal naive có kiểm định ý nghĩa.
```

---

## Phase 11 — Buổi 18–21 · Hồi quy động, gián đoạn, đa biến, tài chính 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-11.md`](todos/phase-11.md)

### Prompt copy-paste cho Phase 11:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 10 xong → Phase 11: buổi 18–21 (Giai đoạn 2, nửa sau).
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-11.md.
Research riêng: FPP ch. 7, 10, 12; Syntetos–Boylan, TSB (Teunter et al.); nowcasting dynamic factor / MIDAS; Philadelphia Fed
RTDSM (KHÔNG ALFRED/FRED); Prophet còn bảo trì?; arch mới, HAR-RV, Markov switching (statsmodels); phản biện "deep learning
dự báo giá cổ phiếu".
Riêng: buổi 19 chấm bằng chi phí tồn kho, không chỉ chỉ số thống kê; buổi 20 dùng vintage thật (số đã sửa = rò rỉ); buổi 21
trung thực: giá gần như không thắng naive, nói rõ. Cuối buổi 21: cột mốc M2.
```

---

## Phase 12 — Buổi 22–24 · Machine learning + dự án giữa chặng 2 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-12.md`](todos/phase-12.md)

### Prompt copy-paste cho Phase 12:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 11 xong → Phase 12: buổi 22–24 + du-an-giua-chang/02-thi-du-bao/.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-12.md.
Research riêng: global vs local (Montero-Manso & Hyndman); chiến lược đa bước (Taieb et al.); lời giải top + tổng kết M5
accuracy; mlforecast + LightGBM mới; AutoGluon-TimeSeries mới (preset, model zoo); forecast combination puzzle; FFORMA; cold
start; EIA-930 API v2 (endpoint, day-ahead forecast, độ trễ công bố, sửa số liệu lùi).
Riêng: dự án chấm trên dữ liệu TƯƠNG LAI THẬT (chưa tồn tại lúc nộp), so với day-ahead của đơn vị điều độ trong EIA-930;
script lấy dữ liệu + chấm tự động + leaderboard; thời tiết làm feature phải là thời tiết DỰ BÁO lưu trữ — bộ chấm kiểm.
Cuối buổi 24: M3.
```

---

## Phase 13 — Buổi 25–28 · Bất định 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-13.md`](todos/phase-13.md)

### Prompt copy-paste cho Phase 13:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 12 xong → Phase 13: buổi 25–28 (Giai đoạn 4 — Bất định).
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-13.md.
Research riêng: Gneiting & Raftery (proper scoring), calibration/sharpness; WIS (Bracher et al. 2021); conformal cho chuỗi
thời gian — ACI (Gibbs & Candès), EnbPI, benchmark 2026, MAPIE mới; pymc + pymc-extras statespace mới; GP kernel; FPP ch. 11,
MinT (Wickramasuriya et al.), probabilistic reconciliation mới, hierarchicalforecast mới; giấy phép Tourism Australia.
Riêng: từ phase này mọi dự báo có khoảng đã kiểm calibration; buổi 27 không dùng posterior chưa chẩn đoán hội tụ. Cuối
buổi 28: M4.
```

---

## Phase 14 — Buổi 29–33 · Deep learning 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-14.md`](todos/phase-14.md)

### Prompt copy-paste cho Phase 14:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 13 xong → Phase 14: buổi 29–33 (Giai đoạn 5 — Deep learning).
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-14.md.
Research riêng: FPP ch. 14; neuralforecast + PyTorch mới; bài gốc N-BEATS, N-HiTS, DeepAR, TFT, TiDE, PatchTST, iTransformer,
TSMixer, DLinear ("Are Transformers Effective...") + phản biện benchmark/`drop_last` mới; SOTA 12 tháng gần (có thể thay một
kiến trúc buổi 30/31); TimeGrad, CSDI, diffusion; đánh giá dữ liệu tổng hợp; ECMWF Open Data AIFS (định dạng, biến, giấy
phép, tải điểm), GHCNh trạm Nội Bài (không NOAA ISD ngoài Mỹ), WeatherBench 2; PyTorch Geometric Temporal / GNN METR-LA trên CPU.
Riêng: mọi lab chạy CPU trong thời gian hợp lý (ghi phút), có cấu hình rút gọn máy 8 GB; mọi bảng so sánh có seasonal
naive + một mô hình thống kê + LightGBM, kể cả khi DL thua; model/checkpoint chốt revision. Cuối buổi 33: M5.
```

---

## Phase 15 — Buổi 34–37 · Foundation model và LLM 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-15.md`](todos/phase-15.md)

### Prompt copy-paste cho Phase 15:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 14 xong → Phase 15: buổi 34–37 (Giai đoạn 6 — Foundation model và LLM).
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-15.md.
Research riêng — KỸ HƠN mọi phase (lĩnh vực đổi hàng tháng):
- GIFT-Eval, fev-bench HIỆN TẠI: top model, cột "không rò dữ liệu", model mới sau Chronos-2 / TimesFM 2.5 / Moirai 2 / TiRex /
  Toto 2.0 / Sundial → cập nhật danh sách model của buổi; ngày phát hành + dữ liệu huấn luyện từng model (chọn dữ liệu sạch)
- calibration của foundation model, fine-tune/LoRA, catastrophic forgetting; TimeCopilot, agent dự báo; benchmark có ngữ
  cảnh văn bản ("Context is Key" và mới hơn)
- ForecastBench: leaderboard, định dạng question set/resolution, giấy phép; rò rỉ thời gian khi backtest LLM (arXiv
  2608.02985, 2601.13717 và mới hơn); kiến trúc bot top; LLM mở chạy local tốt nhất cho CPU/GPU nhỏ; giá API hiện tại
Riêng: buổi 36–37 chạy được không cần API key trả phí (model mở local + bản ghi phản hồi); mọi đánh giá foundation
model/LLM trên dữ liệu SAU mốc cắt, ghi mốc trong "Trạng thái đầu buổi". Cuối buổi 37: M6.
```

---

## Phase 16 — Buổi 38–40 · Nhân quả và ra quyết định 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-16.md`](todos/phase-16.md)

### Prompt copy-paste cho Phase 16:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 15 xong → Phase 16: buổi 38–40 (Giai đoạn 7 — Nhân quả và ra quyết định).
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-16.md.
Research riêng: CausalImpact Python còn sống (tfcausalimpact / causalimpact / PyMC-Marketing / CausalPy — chọn cái đang bảo
trì); synthetic control (Abadie), synthetic DiD; DoubleML/EconML mới; forecast value added (Gilliland); newsvendor + inventory
policy với dự báo xác suất; FPP ch. 6 (judgmental); truyền đạt bất định cho người không chuyên (fan chart).
Riêng: mọi phương pháp nhân quả kiểm trên dữ liệu mô phỏng có đáp án TRƯỚC khi áp lên dữ liệu thật; buổi 40 quy ra tiền.
```

---

## Phase 17 — Buổi 41–43 · Production và MLOps 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-17.md`](todos/phase-17.md)

### Prompt copy-paste cho Phase 17:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 16 xong → Phase 17: buổi 41–43 (Giai đoạn 8 — Production và MLOps).
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-17.md.
Research riêng: Prefect vs Dagster mới (chọn một, ghi lý do); pandera, MLflow, DVC mới; point-in-time/feature store cho chuỗi
thời gian; statsforecast/mlforecast phân tán (Ray, Spark, Dask qua Fugue) còn hỗ trợ?; phục vụ foundation model trên CPU;
drift detection (PSI, ADWIN, Page–Hinkley — river mới); bài học vận hành hệ dự báo lớn công khai gần đây (Uber, Amazon, Walmart…).
Riêng: buổi 41 tái lập từng byte; buổi 43 replay dữ liệu thật với sự cố cài sẵn, không mô phỏng tay từng cảnh báo. Cuối
buổi 43: M7.
```

---

## Phase 18 — Dự án cuối khoá 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-18.md`](todos/phase-18.md)

### Prompt copy-paste cho Phase 18:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 17 xong → Phase 18: du-an-cuoi/.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-18.md. Research ghi du-an-cuoi/NGHIEN-CUU.md.
Research riêng: tổ chức thi dự báo trực tiếp (M6, GEFCom, ForecastBench, cuộc thi VN nếu có); EIA-930 API và OpenAQ hiện tại
(trạm Hà Nội/TP.HCM còn chạy?, độ trễ); rubric chấm dự án ML thực tế; model card (Mitchell et al.) mới.
Riêng: đề + rubric lấy nguyên mục "Buổi 44 — Dự án cuối" của lộ trình; bộ chấm tự động ~50/100; lời giải mẫu và
ngay-du-lieu-hong/ KHÔNG vào zip (kiểm dong_goi.py). Không được bỏ: chấm trên dữ liệu TƯƠNG LAI THẬT (dấu thời gian dự báo có
trước dữ liệu) và "ngày dữ liệu hỏng" do giám khảo giữ. Chạy thử bộ chấm với lời giải mẫu đề B trong 3 ngày dự báo trực tiếp
thật trước khi tick ✅. Đề phát học viên xuất PDF. Đọc thử kiểu "văn bản không phải buổi" (KHỐI CHUNG Đ).
```

---

## Phase 19 — Đánh giá 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-19.md`](todos/phase-19.md)

### Prompt copy-paste cho Phase 19:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 18 xong → Phase 19: danh-gia/.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-19.md. Research ghi danh-gia/NGHIEN-CUU.md.
Research riêng: rà 44 buổi tìm nội dung đã lỗi thời (API đổi, model mới) — liệt kê TRƯỚC khi viết câu hỏi dựa trên nó; cách
viết câu hỏi đánh giá hiểu sâu; khung năng lực dự báo (IIF CPF…).
Riêng: gộp quiz 44 buổi thành ngân hàng câu hỏi; 2 đề thực hành có script chấm; đề đọc biểu đồ 30 hình thật (sinh bằng
script, lưu trong repo); đề tìm rò rỉ chấm tự động; mọi câu trỏ về buổi dạy nó. Đọc thử kiểu "văn bản không phải buổi".
```

---

## Phase 20 — Xuất bản & đóng gói 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-20.md`](todos/phase-20.md)

### Prompt copy-paste cho Phase 20:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 19 xong → Phase 20: xuất bản — 44 PDF, đóng gói phat-de/, cập nhật README.md và CLAUDE.md.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-20.md.
Research (thay R): phiên bản mới nhất của MỌI thư viện/model đã chốt; dataset đổi URL/giấy phép; bảng xếp hạng
GIFT-Eval/fev-bench/ForecastBench → NGHIEN-CUU-XUAT-BAN.md bảng "đã chốt → mới nhất → cần cập nhật buổi nào". Lệch lớn (API hỏng
lab, model vượt hẳn) → báo người dùng TRƯỚC, đề xuất phase cập nhật, không tự sửa hàng loạt. Cập nhật "Rà soát gần nhất" của lộ trình.
Riêng: README có bảng "học theo cụm", dễ hiểu + gọn (bắt đầu từ đâu, cài gì, học thứ tự nào; không lặp lộ trình). --kiem:
mọi buổi 10–18 trang, trong trần do_dai. Unzip thử 4 zip (gồm buổi 13, 24, 44): không lọt dap-an/, NGHIEN-CUU.md,
loi-giai-mau/, ngay-du-lieu-hong/.
```

---

## Phase 21 — Kiểm định chất lượng 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-21.md`](todos/phase-21.md)

### Prompt copy-paste cho Phase 21:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 20 xong → Phase 21: kiểm định — kiem_tra_lab.py cả 44 buổi trên venv trắng, rà mạch kiến thức và M0–M7.
Theo KHỐI CHUNG (todos/quy-uoc.md: R V L Đ X) + todos/phase-21.md. Kết quả ghi KIEM-DINH.md.
Research (thay R): thư viện/model/dataset nào đổi kể từ ngày trong từng NGHIEN-CUU.md → bảng "buổi có nguy cơ lỗi thời"
TRƯỚC khi chạy (tách lỗi nội dung với lỗi môi trường).
Bài 1 (quan trọng nhất): copy ngẫu nhiên 6 thư mục buổi sang máy trắng, không có phần còn lại của repo, chạy
python lab.py up && python lab.py check (cả đường --pip trong môi trường conda); thêm bài CPU-only (29–35) và không API key (36–37).
Bài 2: kiem_de_hieu.py cả 44 buổi (kể cả do_dai, cau_rong, lap_y) + đọc thử và rà gọn 6 buổi ngẫu nhiên (subagent mới);
phan-hoi-hoc-vien.md đã xử lý hết.
Báo cáo bảng: buổi xanh/hỏng, hỏng ở bước nào, thời gian chạy. Không sửa lấy được — nêu rõ trước.
```

---

## General Copy-paste Prompt (dùng khi không nhớ đang ở phase nào):
```text
Forecasting 44 buổi | /home/tony/Tony/Forecasting | Đọc todos.md, làm phase đầu tiên còn 🔲: chạy đúng prompt của phase đó
(theo KHỐI CHUNG trong todos/quy-uoc.md + todos/phase-NN.md). Tóm tắt ràng buộc cứng (chi tiết ở CLAUDE.md, quy-uoc):
research trước khi viết, lệch lớn báo trước; buổi tự chứa tuyệt đối; chỗ hở cố ý (rò rỉ tương lai, đánh giá không trung
thực); mọi số từ lần chạy thật; chốt phiên bản; CPU chạy được; dữ liệu có giấy phép; dap-an/NGHIEN-CUU/lời giải không vào
zip; DỄ HIỂU NHƯNG GỌN (tường minh quá cũng là khó hiểu); đọc thử + rà gọn bằng subagent mới trước khi tick ✅.
```
