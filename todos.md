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
- **Không dùng subagent**: đọc thử và rà gọn do chính người làm phase tự làm, hai lượt đọc riêng theo checklist trong
  `tools/CHUAN-DE-HIEU.md`; tiêu chí đạt giữ nguyên.
- Vì không có subagent nên **chia nhỏ phase** (Phase 8–48): mỗi phase soạn 1–2 buổi; sau mỗi cụm một phase **đọc thử độc
  lập** (phiên mới, quiz mù); deep learning và foundation model & LLM có phase **research riêng** trước khi soạn.

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

## Phase 8 — Viết lại buổi 4–5 + Phụ lục C ✅

Chi tiết: [`todos/phase-08.md`](todos/phase-08.md)

### Prompt copy-paste cho Phase 8:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 7 xong → Phase 8: VIẾT LẠI buổi 04–05 + phu-luc/C.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-08.md.
Cụm trọng tâm: đọc biểu đồ. Buổi 5: log, Box-Cox, bias khi đổi ngược — ví dụ 3–5 số tính tay trước. PDF: xuat_pdf.py 4 5 + C.
```

---

## Phase 9 — Viết lại buổi 6–7 ✅

Chi tiết: [`todos/phase-09.md`](todos/phase-09.md)

### Prompt copy-paste cho Phase 9:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 8 xong → Phase 9: VIẾT LẠI buổi 06–07.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-09.md.
ACF, PACF, tính dừng, ADF/KPSS: trực giác + ví dụ số nhỏ tính tay TRƯỚC công thức; p-value/kiểm định → "Mượn trước".
Quiz buổi 7 câu 5 đáp án sai — sửa (xem phase-09.md). PDF: xuat_pdf.py 6 7.
```

---

## Phase 10 — Viết lại buổi 8 ✅

Chi tiết: [`todos/phase-10.md`](todos/phase-10.md)

### Prompt copy-paste cho Phase 10:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 9 xong → Phase 10: VIẾT LẠI buổi 08.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-10.md.
CCF, prewhitening, mutual information, Granger: trực giác + ví dụ số nhỏ TRƯỚC công thức; mỗi tình huống kết bằng cái bẫy
nói trong một câu. PDF: xuat_pdf.py 8.
```

---

## Phase 11 — Đọc thử độc lập buổi 4–8 + Phụ lục C ✅

Chi tiết: [`todos/phase-11.md`](todos/phase-11.md)

### Prompt copy-paste cho Phase 11:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 10 xong → Phase 11: ĐỌC THỬ ĐỘC LẬP buổi 04–08 + phu-luc/C (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-11.md.
Phiên MỚI (/clear). Tài liệu: buoi-04..08/tai-lieu.md + quiz, phu-luc/C. Ghi NGHIEN-CUU.md mục "Đọc thử độc lập".
```

---

## Phase 12 — Viết lại buổi 9–10 ✅

Chi tiết: [`todos/phase-12.md`](todos/phase-12.md)

### Prompt copy-paste cho Phase 12:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 11 xong → Phase 12: VIẾT LẠI buổi 09–10.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-12.md.
Mỗi kỹ thuật: khi nào dùng / KHÔNG dùng (lời thường) + ví dụ số nhỏ + thí nghiệm có số. PDF: xuat_pdf.py 9 10.
```

---

## Phase 13 — Viết lại buổi 11–12 ✅

Chi tiết: [`todos/phase-13.md`](todos/phase-13.md)

### Prompt copy-paste cho Phase 13:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 12 xong → Phase 13: VIẾT LẠI buổi 11–12.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-13.md.
Mỗi kỹ thuật: khi nào dùng / KHÔNG dùng + ví dụ số nhỏ + thí nghiệm có số. PDF: xuat_pdf.py 11 12.
```

---

## Phase 14 — Viết lại buổi 13 + đề dự án giữa chặng 1 + Phụ lục D ✅

Chi tiết: [`todos/phase-14.md`](todos/phase-14.md)

### Prompt copy-paste cho Phase 14:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 13 xong → Phase 14: VIẾT LẠI buổi 13 + đề du-an-giua-chang/01-eda-lam-sach/ + phu-luc/D.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-14.md.
Rò rỉ: mỗi kiểu một bảng vài dòng chỉ ô nhìn trộm tương lai. Dự án: chỉ viết lại đề + rubric; lỗi cài sẵn và lời giải
KHÔNG vào zip. PDF: xuat_pdf.py 13 + dự án + D.
```

---

## Phase 15 — Đọc thử độc lập buổi 9–13 + dự án giữa chặng 1 + Phụ lục D ✅

Chi tiết: [`todos/phase-15.md`](todos/phase-15.md)

### Prompt copy-paste cho Phase 15:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 14 xong → Phase 15: ĐỌC THỬ ĐỘC LẬP buổi 09–13 + đề dự án giữa chặng 1 + phu-luc/D (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-15.md.
Phiên MỚI (/clear). Tài liệu: buoi-09..13 + quiz, đề + rubric dự án giữa chặng 1, phu-luc/D.
```

---

## Phase 16 — Buổi 14–15 · Baseline, chỉ số, backtest ✅

Chi tiết: [`todos/phase-16.md`](todos/phase-16.md)

### Prompt copy-paste cho Phase 16:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 15 xong → Phase 16: buổi 14–15 (Giai đoạn 2). Bản nháp 14–15 đã có: giữ code/lab/số, viết lại chữ.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-16.md.
Research riêng: FPP ch. 5; Hyndman & Koehler 2006 (MASE); M5 guide (RMSSE/WRMSSE); Bergmeir & Benítez (CV chuỗi thời gian);
Diebold–Mariano bản Harvey; statsforecast cross_validation.
Riêng: buổi 15 tạo bộ backtest cả khoá dùng — thiết kế kỹ, có test. Mọi mô hình so seasonal naive có kiểm định ý nghĩa.
```

---

## Phase 17 — Buổi 16–17 · ETS, Theta, ARIMA ✅

Chi tiết: [`todos/phase-17.md`](todos/phase-17.md)

### Prompt copy-paste cho Phase 17:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 16 xong → Phase 17: buổi 16–17 (Giai đoạn 2). Bản nháp đã có: giữ code/lab/số, viết lại chữ.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-17.md.
Research riêng: FPP ch. 8, 9; statsforecast mới nhất (AutoETS, AutoTheta, AutoARIMA).
Riêng: mọi mô hình so seasonal naive có kiểm định ý nghĩa (bộ backtest buổi 15).
```

---

## Phase 18 — Đọc thử độc lập buổi 14–17 ✅

Chi tiết: [`todos/phase-18.md`](todos/phase-18.md)

### Prompt copy-paste cho Phase 18:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 17 xong → Phase 18: ĐỌC THỬ ĐỘC LẬP buổi 14–17 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-18.md.
Phiên MỚI (/clear). Tài liệu: Buổi 14, Buổi 15, Buổi 16, Buổi 17, Phụ lục D (phần mở rộng).
```

---

## Phase 19 — Buổi 18–19 · Hồi quy động, nhu cầu gián đoạn ✅

Chi tiết: [`todos/phase-19.md`](todos/phase-19.md)

### Prompt copy-paste cho Phase 19:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 18 xong → Phase 19: buổi 18–19 (Giai đoạn 2, nửa sau).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-19.md.
Research riêng: FPP ch. 7, 10, 12; Prophet còn bảo trì?; Syntetos–Boylan classification, TSB (Teunter et al.).
Riêng: buổi 19 chấm bằng chi phí tồn kho, không chỉ chỉ số thống kê.
```

---

## Phase 20 — Buổi 20–21 · Đa biến & nowcasting, tài chính ✅

Chi tiết: [`todos/phase-20.md`](todos/phase-20.md)

### Prompt copy-paste cho Phase 20:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 19 xong → Phase 20: buổi 20–21 (Giai đoạn 2, nửa sau).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-20.md.
Research riêng: nowcasting dynamic factor / MIDAS (tổng quan mới); Philadelphia Fed RTDSM (KHÔNG ALFRED/FRED); arch mới,
HAR-RV, Markov switching (statsmodels); phản biện "deep learning dự báo giá cổ phiếu".
Riêng: buổi 20 dùng vintage thật (số đã sửa = rò rỉ); buổi 21 trung thực: giá gần như không thắng naive, nói rõ. Cuối buổi 21: M2.
```

---

## Phase 21 — Đọc thử độc lập buổi 18–21 ✅

Chi tiết: [`todos/phase-21.md`](todos/phase-21.md)

### Prompt copy-paste cho Phase 21:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 20 xong → Phase 21: ĐỌC THỬ ĐỘC LẬP buổi 18–21 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-21.md.
Phiên MỚI (/clear). Tài liệu: Buổi 18, Buổi 19, Buổi 20, Buổi 21.
```

---

## Phase 22 — Buổi 22–23 · Dự báo thành hồi quy, gradient boosting ✅

Chi tiết: [`todos/phase-22.md`](todos/phase-22.md)

### Prompt copy-paste cho Phase 22:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 21 xong → Phase 22: buổi 22–23 (machine learning).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-22.md.
Research riêng: global vs local (Montero-Manso & Hyndman); chiến lược đa bước (Taieb et al.); lời giải top + tổng kết M5
accuracy; mlforecast + LightGBM mới; Optuna mới.
```

---

## Phase 23 — Buổi 24 + dự án giữa chặng 2 ✅

Chi tiết: [`todos/phase-23.md`](todos/phase-23.md)

### Prompt copy-paste cho Phase 23:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 22 xong → Phase 23: buổi 24 + du-an-giua-chang/02-thi-du-bao/.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-23.md.
Research riêng: AutoGluon-TimeSeries mới (preset, model zoo); forecast combination puzzle; FFORMA; cold start; EIA-930 API v2
(endpoint, day-ahead forecast, độ trễ công bố, sửa số liệu lùi).
Riêng: dự án chấm trên dữ liệu TƯƠNG LAI THẬT (chưa tồn tại lúc nộp), so với day-ahead của đơn vị điều độ trong EIA-930; script
lấy dữ liệu + chấm tự động + leaderboard; thời tiết làm feature phải là thời tiết DỰ BÁO lưu trữ — bộ chấm kiểm. Cuối buổi 24: M3.
```

---

## Phase 24 — Đọc thử độc lập buổi 22–24 + dự án giữa chặng 2 ✅

Chi tiết: [`todos/phase-24.md`](todos/phase-24.md)

### Prompt copy-paste cho Phase 24:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 23 xong → Phase 24: ĐỌC THỬ ĐỘC LẬP buổi 22–24 + dự án giữa chặng 2 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-24.md.
Phiên MỚI (/clear). Tài liệu: Buổi 22, Buổi 23, Buổi 24, Đề dự án giữa chặng 2.
```

---

## Phase 25 — Buổi 25–26 · Dự báo xác suất, conformal ✅

Chi tiết: [`todos/phase-25.md`](todos/phase-25.md)

### Prompt copy-paste cho Phase 25:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 24 xong → Phase 25: buổi 25–26 (Giai đoạn 4 — Bất định).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-25.md.
Research riêng: Gneiting & Raftery (proper scoring), calibration/sharpness; WIS (Bracher et al. 2021); conformal cho chuỗi
thời gian — ACI (Gibbs & Candès), EnbPI, benchmark 2026, MAPIE mới.
Riêng: từ phase này mọi dự báo có khoảng đã kiểm calibration.
```

---

## Phase 26 — Buổi 27–28 · Bayes & GP, dự báo phân cấp ✅

Chi tiết: [`todos/phase-26.md`](todos/phase-26.md)

### Prompt copy-paste cho Phase 26:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 25 xong → Phase 26: buổi 27–28 (Giai đoạn 4 — Bất định).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-26.md.
Research riêng: pymc + pymc-extras statespace mới; GP kernel cho chuỗi thời gian; FPP ch. 11, MinT (Wickramasuriya et al.),
probabilistic reconciliation mới, hierarchicalforecast mới; giấy phép Tourism Australia.
Riêng: mọi khoảng đã kiểm calibration; buổi 27 không dùng posterior chưa chẩn đoán hội tụ. Cuối buổi 28: M4.
```

---

## Phase 27 — Đọc thử độc lập buổi 25–28 ✅

Chi tiết: [`todos/phase-27.md`](todos/phase-27.md)

### Prompt copy-paste cho Phase 27:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 26 xong → Phase 27: ĐỌC THỬ ĐỘC LẬP buổi 25–28 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-27.md.
Phiên MỚI (/clear). Tài liệu: Buổi 25, Buổi 26, Buổi 27, Buổi 28.
```

---

## Phase 28 — Research deep learning (buổi 29–33) 🔲

Chi tiết: [`todos/phase-28.md`](todos/phase-28.md)

### Prompt copy-paste cho Phase 28:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 27 xong → Phase 28: RESEARCH RIÊNG cụm deep learning, buổi 29–33 (KHỐI CHUNG RS — chưa soạn).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-28.md.
Research riêng: FPP ch. 14; neuralforecast + PyTorch mới; bài gốc N-BEATS, N-HiTS, DeepAR, TFT, TiDE, PatchTST, iTransformer,
TSMixer, DLinear ("Are Transformers Effective...") + phản biện benchmark/`drop_last` mới; SOTA 12 tháng gần (có thể thay một
kiến trúc buổi 30/31); TimeGrad, CSDI, diffusion; đánh giá dữ liệu tổng hợp; ECMWF Open Data AIFS (định dạng, biến, giấy
phép, tải điểm), GHCNh trạm Nội Bài (không NOAA ISD ngoài Mỹ), WeatherBench 2; PyTorch Geometric Temporal / GNN METR-LA trên CPU;
thời gian + RAM chạy CPU của từng mô hình dự kiến.
```

---

## Phase 29 — Buổi 29–30 · Nền DL, N-BEATS … TiDE 🔲

Chi tiết: [`todos/phase-29.md`](todos/phase-29.md)

### Prompt copy-paste cho Phase 29:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 28 xong → Phase 29: buổi 29–30 (Giai đoạn 5 — Deep learning).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-29.md.
Riêng: mọi lab chạy CPU trong thời gian hợp lý (ghi phút), có cấu hình rút gọn máy 8 GB; mọi bảng so sánh có seasonal
naive + một mô hình thống kê + LightGBM, kể cả khi DL thua; model/checkpoint chốt revision. Research: đọc NGHIEN-CUU.md từ phase 28, rà bổ sung.
```

---

## Phase 30 — Buổi 31–32 · Transformer, mô hình sinh 🔲

Chi tiết: [`todos/phase-30.md`](todos/phase-30.md)

### Prompt copy-paste cho Phase 30:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 29 xong → Phase 30: buổi 31–32 (Giai đoạn 5 — Deep learning).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-30.md.
Riêng: mọi lab chạy CPU trong thời gian hợp lý (ghi phút), có cấu hình rút gọn máy 8 GB; mọi bảng so sánh có seasonal
naive + một mô hình thống kê + LightGBM, kể cả khi DL thua; model/checkpoint chốt revision. Research: đọc NGHIEN-CUU.md từ phase 28, rà bổ sung.
```

---

## Phase 31 — Buổi 33 · Không gian–thời gian & thời tiết AI 🔲

Chi tiết: [`todos/phase-31.md`](todos/phase-31.md)

### Prompt copy-paste cho Phase 31:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 30 xong → Phase 31: buổi 33 (Giai đoạn 5 — Deep learning).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-31.md.
Riêng: mọi lab chạy CPU trong thời gian hợp lý (ghi phút), có cấu hình rút gọn máy 8 GB; mọi bảng so sánh có seasonal
naive + một mô hình thống kê + LightGBM, kể cả khi DL thua; model/checkpoint chốt revision. Research: đọc NGHIEN-CUU.md từ phase 28, rà bổ sung. Cuối buổi 33: M5.
```

---

## Phase 32 — Đọc thử độc lập buổi 29–33 🔲

Chi tiết: [`todos/phase-32.md`](todos/phase-32.md)

### Prompt copy-paste cho Phase 32:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 31 xong → Phase 32: ĐỌC THỬ ĐỘC LẬP buổi 29–33 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-32.md.
Phiên MỚI (/clear). Tài liệu: Buổi 29, Buổi 30, Buổi 31, Buổi 32, Buổi 33.
```

---

## Phase 33 — Research foundation model & LLM (buổi 34–37) 🔲

Chi tiết: [`todos/phase-33.md`](todos/phase-33.md)

### Prompt copy-paste cho Phase 33:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 32 xong → Phase 33: RESEARCH RIÊNG cụm foundation model & LLM, buổi 34–37 (KHỐI CHUNG RS — chưa soạn).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-33.md.
Research riêng — KỸ HƠN mọi phase (lĩnh vực đổi hàng tháng):
- GIFT-Eval, fev-bench HIỆN TẠI: top model, cột "không rò dữ liệu", model mới sau Chronos-2 / TimesFM 2.5 / Moirai 2 / TiRex /
  Toto 2.0 / Sundial → cập nhật danh sách model của buổi; ngày phát hành + dữ liệu huấn luyện từng model (chọn dữ liệu sạch)
- calibration của foundation model, fine-tune/LoRA, catastrophic forgetting; TimeCopilot, agent dự báo; benchmark có ngữ
  cảnh văn bản ("Context is Key" và mới hơn)
- ForecastBench: leaderboard, định dạng question set/resolution, giấy phép; rò rỉ thời gian khi backtest LLM (arXiv
  2608.02985, 2601.13717 và mới hơn); kiến trúc bot top; LLM mở chạy local tốt nhất cho CPU/GPU nhỏ; giá API hiện tại
```

---

## Phase 34 — Buổi 34–35 · Foundation model, fine-tune & benchmark 🔲

Chi tiết: [`todos/phase-34.md`](todos/phase-34.md)

### Prompt copy-paste cho Phase 34:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 33 xong → Phase 34: buổi 34–35 (Giai đoạn 6).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-34.md.
Riêng: mọi đánh giá foundation model/LLM trên dữ liệu SAU mốc cắt, ghi mốc trong "Trạng thái đầu buổi"; model chốt
revision. Research: đọc NGHIEN-CUU.md từ phase 33, rà lại phần model/phiên bản nếu cũ hơn 1 tháng.
```

---

## Phase 35 — Buổi 36–37 · LLM & agent, dự báo sự kiện 🔲

Chi tiết: [`todos/phase-35.md`](todos/phase-35.md)

### Prompt copy-paste cho Phase 35:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 34 xong → Phase 35: buổi 36–37 (Giai đoạn 6).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-35.md.
Riêng: mọi đánh giá foundation model/LLM trên dữ liệu SAU mốc cắt, ghi mốc trong "Trạng thái đầu buổi"; model chốt
revision. Research: đọc NGHIEN-CUU.md từ phase 33, rà lại phần model/phiên bản nếu cũ hơn 1 tháng.
Buổi 36–37 chạy được không cần API key trả phí (model mở local + bản ghi phản hồi). Cuối buổi 37: M6.
```

---

## Phase 36 — Đọc thử độc lập buổi 34–37 🔲

Chi tiết: [`todos/phase-36.md`](todos/phase-36.md)

### Prompt copy-paste cho Phase 36:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 35 xong → Phase 36: ĐỌC THỬ ĐỘC LẬP buổi 34–37 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-36.md.
Phiên MỚI (/clear). Tài liệu: Buổi 34, Buổi 35, Buổi 36, Buổi 37.
```

---

## Phase 37 — Buổi 38–39 · Tác động can thiệp, kịch bản & what-if 🔲

Chi tiết: [`todos/phase-37.md`](todos/phase-37.md)

### Prompt copy-paste cho Phase 37:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 36 xong → Phase 37: buổi 38–39 (Giai đoạn 7 — Nhân quả).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-37.md.
Research riêng: CausalImpact Python còn sống (tfcausalimpact / causalimpact / PyMC-Marketing / CausalPy — chọn cái đang bảo
trì); synthetic control (Abadie), synthetic DiD; DoubleML/EconML mới.
Riêng: mọi phương pháp nhân quả kiểm trên dữ liệu mô phỏng có đáp án TRƯỚC khi áp lên dữ liệu thật.
```

---

## Phase 38 — Buổi 40 · Dự báo → quyết định 🔲

Chi tiết: [`todos/phase-38.md`](todos/phase-38.md)

### Prompt copy-paste cho Phase 38:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 37 xong → Phase 38: buổi 40 (Giai đoạn 7).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-38.md.
Research riêng: forecast value added (Gilliland); newsvendor + inventory policy với dự báo xác suất; FPP ch. 6 (judgmental);
truyền đạt bất định cho người không chuyên (fan chart).
Riêng: buổi 40 quy ra tiền.
```

---

## Phase 39 — Đọc thử độc lập buổi 38–40 🔲

Chi tiết: [`todos/phase-39.md`](todos/phase-39.md)

### Prompt copy-paste cho Phase 39:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 38 xong → Phase 39: ĐỌC THỬ ĐỘC LẬP buổi 38–40 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-39.md.
Phiên MỚI (/clear). Tài liệu: Buổi 38, Buổi 39, Buổi 40.
```

---

## Phase 40 — Buổi 41–42 · Pipeline tái lập, phục vụ quy mô lớn 🔲

Chi tiết: [`todos/phase-40.md`](todos/phase-40.md)

### Prompt copy-paste cho Phase 40:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 39 xong → Phase 40: buổi 41–42 (Giai đoạn 8 — Production).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-40.md.
Research riêng: Prefect vs Dagster mới (chọn một, ghi lý do); pandera, MLflow, DVC mới; point-in-time/feature store cho chuỗi
thời gian; statsforecast/mlforecast phân tán (Ray, Spark, Dask qua Fugue) còn hỗ trợ?; phục vụ foundation model trên CPU.
Riêng: buổi 41 tái lập từng byte.
```

---

## Phase 41 — Buổi 43 · Giám sát & drift 🔲

Chi tiết: [`todos/phase-41.md`](todos/phase-41.md)

### Prompt copy-paste cho Phase 41:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 40 xong → Phase 41: buổi 43 (Giai đoạn 8).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-41.md.
Research riêng: drift detection (PSI, ADWIN, Page–Hinkley — river mới); bài học vận hành hệ dự báo lớn công khai gần đây
(Uber, Amazon, Walmart…).
Riêng: replay dữ liệu thật với sự cố cài sẵn, không mô phỏng tay từng cảnh báo. Cuối buổi 43: M7.
```

---

## Phase 42 — Đọc thử độc lập buổi 41–43 🔲

Chi tiết: [`todos/phase-42.md`](todos/phase-42.md)

### Prompt copy-paste cho Phase 42:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 41 xong → Phase 42: ĐỌC THỬ ĐỘC LẬP buổi 41–43 (KHỐI CHUNG DT, phiên MỚI).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-42.md.
Phiên MỚI (/clear). Tài liệu: Buổi 41, Buổi 42, Buổi 43.
```

---

## Phase 43 — Dự án cuối (a) · Đề, rubric, bộ chấm 🔲

Chi tiết: [`todos/phase-43.md`](todos/phase-43.md)

### Prompt copy-paste cho Phase 43:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 42 xong → Phase 43: du-an-cuoi/ phần (a): đề, rubric, khuôn, bộ chấm, hạ tầng nguồn dữ liệu của lớp.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-43.md.
Research ghi du-an-cuoi/NGHIEN-CUU.md. Research riêng: tổ chức thi dự báo trực tiếp (M6, GEFCom, ForecastBench, cuộc thi VN
nếu có); EIA-930 API và OpenAQ hiện tại (trạm Hà Nội/TP.HCM còn chạy?, độ trễ); rubric chấm dự án ML thực tế; model card
(Mitchell et al.) mới.
Riêng: đề + rubric lấy nguyên mục "Buổi 44 — Dự án cuối" của lộ trình; bộ chấm tự động ~50/100; không được bỏ: chấm trên dữ
liệu TƯƠNG LAI THẬT (dấu thời gian dự báo có trước dữ liệu).
```

---

## Phase 44 — Dự án cuối (b) · Ngày dữ liệu hỏng, lời giải mẫu, chạy thử thật 🔲

Chi tiết: [`todos/phase-44.md`](todos/phase-44.md)

### Prompt copy-paste cho Phase 44:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 43 xong → Phase 44: du-an-cuoi/ phần (b): ngày dữ liệu hỏng, lời giải mẫu, chạy thử 3 ngày thật, PDF, đọc thử độc lập đề.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-44.md.
Riêng: "ngày dữ liệu hỏng" do giám khảo giữ, không được bỏ; lời giải mẫu và ngay-du-lieu-hong/ KHÔNG vào zip; chạy thử 3
ngày dự báo trực tiếp thật; đề xuất PDF. Đọc thử độc lập đề trong phiên MỚI.
```

---

## Phase 45 — Đánh giá (a) · Ngân hàng câu hỏi, đề đọc biểu đồ 🔲

Chi tiết: [`todos/phase-45.md`](todos/phase-45.md)

### Prompt copy-paste cho Phase 45:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 44 xong → Phase 45: danh-gia/ phần (a).
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-45.md.
Research ghi danh-gia/NGHIEN-CUU.md. Research riêng: rà 44 buổi tìm nội dung đã lỗi thời (API đổi, model mới) — liệt kê TRƯỚC
khi viết câu hỏi dựa trên nó; cách viết câu hỏi đánh giá hiểu sâu; khung năng lực dự báo (IIF CPF…).
```

---

## Phase 46 — Đánh giá (b) · Đề thực hành, đề tìm rò rỉ 🔲

Chi tiết: [`todos/phase-46.md`](todos/phase-46.md)

### Prompt copy-paste cho Phase 46:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 45 xong → Phase 46: danh-gia/ phần (b) + đọc thử độc lập toàn bộ danh-gia/.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-46.md.
Riêng: 2 đề thực hành có script chấm; đề tìm rò rỉ chấm tự động; mọi câu trỏ về buổi dạy nó. Cuối phase: đọc thử độc lập
toàn bộ danh-gia/ trong phiên MỚI.
```

---

## Phase 47 — Xuất bản & đóng gói 🔲

Chi tiết: [`todos/phase-47.md`](todos/phase-47.md)

### Prompt copy-paste cho Phase 47:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 46 xong → Phase 47: xuất bản — 44 PDF, đóng gói phat-de/, cập nhật README.md và CLAUDE.md.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-47.md.
Research (thay R): phiên bản mới nhất của MỌI thư viện/model đã chốt; dataset đổi URL/giấy phép; bảng xếp hạng
GIFT-Eval/fev-bench/ForecastBench → NGHIEN-CUU-XUAT-BAN.md bảng "đã chốt → mới nhất → cần cập nhật buổi nào". Lệch lớn (API hỏng
lab, model vượt hẳn) → báo người dùng TRƯỚC, đề xuất phase cập nhật, không tự sửa hàng loạt. Cập nhật "Rà soát gần nhất" của lộ trình.
Riêng: README có bảng "học theo cụm", dễ hiểu + gọn (bắt đầu từ đâu, cài gì, học thứ tự nào; không lặp lộ trình). --kiem:
mọi buổi 10–18 trang, trong trần do_dai. Unzip thử 4 zip (gồm buổi 13, 24, 44): không lọt dap-an/, NGHIEN-CUU.md,
loi-giai-mau/, ngay-du-lieu-hong/.
```

---

## Phase 48 — Kiểm định chất lượng 🔲

Chi tiết: [`todos/phase-48.md`](todos/phase-48.md)

### Prompt copy-paste cho Phase 48:
```
Forecasting | /home/tony/Tony/Forecasting | Phase 47 xong → Phase 48: kiểm định — kiem_tra_lab.py cả 44 buổi trên venv trắng, rà mạch kiến thức và M0–M7.
Theo KHỐI CHUNG (todos/quy-uoc.md) + todos/phase-48.md.
Kết quả ghi KIEM-DINH.md. Research (thay R): thư viện/model/dataset nào đổi kể từ ngày trong từng NGHIEN-CUU.md → bảng "buổi
có nguy cơ lỗi thời" TRƯỚC khi chạy (tách lỗi nội dung với lỗi môi trường).
Báo cáo bảng: buổi xanh/hỏng, hỏng ở bước nào, thời gian chạy. Không sửa lấy được — nêu rõ trước.
```

---

## General Copy-paste Prompt (dùng khi không nhớ đang ở phase nào):
```text
Forecasting 44 buổi | /home/tony/Tony/Forecasting | Đọc todos.md, làm phase đầu tiên còn 🔲: chạy đúng prompt của phase đó
(theo KHỐI CHUNG trong todos/quy-uoc.md + todos/phase-NN.md). Tóm tắt ràng buộc cứng (chi tiết ở CLAUDE.md, quy-uoc):
research trước khi viết, lệch lớn báo trước; buổi tự chứa tuyệt đối; chỗ hở cố ý (rò rỉ tương lai, đánh giá không trung
thực); mọi số từ lần chạy thật; chốt phiên bản; CPU chạy được; dữ liệu có giấy phép; dap-an/NGHIEN-CUU/lời giải không vào
zip; DỄ HIỂU NHƯNG GỌN (tường minh quá cũng là khó hiểu); tự đọc thử + tự rà gọn (không subagent) trước khi tick ✅.
```
