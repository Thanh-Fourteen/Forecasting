# Khoá Forecasting in AI — Phased Todo Plan
Mục tiêu: **44 buổi** (cơ bản → nâng cao) | **giáo trình .md + PDF + code chạy được trên dữ liệu thật** | Nguồn lộ trình: [`lo-trinh/lo-trinh-forecasting.md`](lo-trinh/lo-trinh-forecasting.md)

**44 buổi** = 3 nền móng + **10 hiểu & chuẩn bị dữ liệu** + 8 thống kê + 3 ML + 4 bất định + 5 deep learning
+ 4 foundation model & LLM + 3 nhân quả & quyết định + 3 production + 1 dự án cuối.
Kèm **2 dự án giữa chặng** (sau buổi 13 và 24).

Repo: `/home/tony/Tony/Forecasting/` — repo độc lập, mọi đường dẫn dưới đây tính từ gốc repo

**Cách tổ chức kế hoạch** (file này chỉ giữ tiêu đề + trạng thái + prompt, để autoclick theo dõi):

- [`todos/quy-uoc.md`](todos/quy-uoc.md) — giao thức research, **chuẩn dễ hiểu + gọn D1–D13 + BƯỚC CUỐI đọc thử & rà gọn**, cấu trúc
  thư mục, nguyên tắc nội dung, Definition of Done, bảng 44 buổi + chỗ hở cố ý. **Đọc trước mọi phase.**
- [`todos/tong-quan.md`](todos/tong-quan.md) — Progress Summary, thứ tự làm bắt buộc, ước lượng, ghi chú rủi ro
- `todos/phase-NN.md` — chi tiết từng phase (bảng tiến độ, checklist, "Bắt buộc", ghi chú research)

Xong phase: đổi 🔲 → ✅ ở **cả hai** tiêu đề (ở đây và trong `todos/phase-NN.md`), rồi cập nhật Progress Summary
trong `todos/tong-quan.md`.

---

## Phase 0 — Hạ tầng khoá học ✅ (trừ push remote)

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-00.md`](todos/phase-00.md)

### Prompt copy-paste cho Phase 0:
```
Khoá Forecasting in AI 44 buổi | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-00.md — đọc trước.
Lộ trình nguồn: lo-trinh/lo-trinh-forecasting.md

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md (phase này. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng cho phase này: uv (lock, workspace, --frozen), jupytext, ruff, cách tải dữ liệu
Kaggle/Hugging Face/EIA/OpenAQ bằng script, cách mirror dữ liệu CC BY lên Hugging Face Datasets.

Làm nốt Phase 0 — Hạ tầng: MOI-TRUONG.md, pyproject.toml gốc (ruff, jupytext), tools/sinh_nen.py,
tools/lay_du_lieu.py, tools/kiem_tra_doc_lap.sh, tools/kiem_tra_lab.py, tools/dong_goi.py,
tools/khuon-buoi/, phu-luc/A..E (theo todos/quy-uoc.md).
tools/xuat_pdf.py ĐÃ CÓ, đừng viết lại — chỉ sửa nếu thiếu.
QUAN TRỌNG: sinh_nen.py, lay_du_lieu.py và kiem_tra_doc_lap.sh là cơ chế giữ cho các buổi độc
lập — làm kỹ, mọi phase sau đều dựa vào. Chưa viết tài liệu buổi nào.
Xong thì chạy thử: sinh nền cho một buổi giả buoi-00-thu/ với 1 dataset UCI nhỏ, make up →
dữ liệu qua sha256 → make down, rồi xoá buoi-00-thu/. Phụ lục xuất PDF bằng tools/xuat_pdf.py.
```

---

## Phase 1 — Khung trợ giúp và danh mục dữ liệu ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-01.md`](todos/phase-01.md)

### Prompt copy-paste cho Phase 1:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-01.md — đọc trước.
Phase 0: XONG. Làm Phase 1 — khung trợ giúp tools/khung/ và danh mục dữ liệu.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào tools/du-lieu/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng cho phase này: GIẤY PHÉP của TỪNG bộ dữ liệu trong lộ trình — mở trang giấy
phép gốc, trích nguyên văn điều khoản phân phối lại vào NGHIEN-CUU.md. Công thức chuẩn của
MASE/RMSSE/WRMSSE (M5 guide), CRPS, WIS (Bracher et al.), Diebold–Mariano bản hiệu chỉnh mẫu nhỏ.

Bắt buộc: ro_ri.py có test cho cả ca phải bắt lẫn ca phải cho qua; danh_gia.py đối chiếu số
với thư viện chuẩn; mọi bộ dữ liệu có giấy phép đã xác minh và bộ dự phòng mở nếu bị hạn chế.
Bộ nào cấm phân phối lại thì KHÔNG mirror. Xong: tải toàn bộ danh mục trên venv trắng, sha256 khớp 100%.
```

---

## Phase 2 — Buổi 1–3 · Nền móng ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-02.md`](todos/phase-02.md)

### Prompt copy-paste cho Phase 2:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-02.md — đọc trước.
Phase 1: XONG. Làm Phase 2 — buổi 01, 02, 03 (lộ trình "Giai đoạn 0").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: bài tổng quan M-competitions (Makridakis et al., M4/M5/M6 findings), FPP chương
1 và 5, pandas 3.x thay đổi về datetime/copy-on-write, polars và DuckDB bản mới nhất.
Lưu ý (Phase 0): hệ Nixtla chưa hỗ trợ pandas 3 → buổi 14+ dùng pandas 2.3.3 (tools/nen/phien-ban.toml
[[rang_buoc]]); buổi 3 phải dạy code chạy được trên CẢ HAI bản, chỉ rõ chỗ khác (Phụ lục A).

Mỗi buổi: NGHIEN-CUU.md + tai-lieu.md đủ 9 mục (có "Trạng thái đầu buổi") + code/ có chỗ hở cố ý
(bảng trong todos/quy-uoc.md) + dap-an/ + lab/00-nen/ (sinh bằng tools/sinh_nen.py) + lab/cham/ +
lab/Makefile + kiem-tra.md 10 câu. Buổi phải TỰ CHỨA: không tham chiếu ../buoi-NN/.
CHẠY THẬT mọi lệnh và lấy mọi con số từ output thật trước khi viết vào tài liệu.
Cuối cùng: tools/kiem_tra_doc_lap.sh → python tools/xuat_pdf.py 1 2 3 → --kiem (10–16 trang).
```

---

## Phase 3 — Buổi 4–8 · Đọc dữ liệu: biểu đồ, biến đổi, phân rã, tương quan ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-03.md`](todos/phase-03.md)

### Prompt copy-paste cho Phase 3:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-03.md — đọc trước.
Phase 2: XONG. Làm Phase 3 — buổi 04..08 (lộ trình "Giai đoạn 1", nửa đầu).

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: FPP chương 2–4 và 9.1–9.2; STL (Cleveland 1990), MSTL (Bandara et al.);
Guerrero cho Box-Cox; ADF/KPSS và cách đọc tổ hợp; spurious regression (Granger & Newbold 1974);
prewhitening + CCF; mutual information cho chuỗi thời gian; tài liệu trực quan hoá chuỗi thời
gian hiện đại (seasonal/subseries plot trong Python, calendar heatmap).

Đây là phase TRỌNG TÂM: người dùng yêu cầu hiểu SÂU khái niệm, ĐỌC được biểu đồ, PHÂN TÍCH
tương quan. Mỗi khái niệm theo nhịp: trực giác → hình → công thức → tự viết bằng NumPy → thư viện.
Mỗi biểu đồ trong tài liệu kèm "đọc ra gì, chỗ nào trên hình". Buổi 08 phải đủ 5 tình huống
tương quan trong mục "Bắt buộc". Viết luôn phu-luc/C-so-tay-doc-bieu-do.md từ nội dung buổi 04–08.
Mọi hình sinh bằng dap-an/ve_hinh.py. Chạy thật, lấy số thật, rồi mới tick ✅ và xuất PDF.
```

---

## Phase 4 — Buổi 9–13 · Chuẩn bị dữ liệu + dự án giữa chặng 1 ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-04.md`](todos/phase-04.md)

### Prompt copy-paste cho Phase 4:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-04.md — đọc trước.
Phase 3: XONG. Làm Phase 4 — buổi 09..13 + du-an-giua-chang/01-eda-lam-sach/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: tsfeatures/catch22 và forecastability (spectral predictability 2025); benchmark
điền dữ liệu chuỗi thời gian (TSI-Bench, PyPOTS bản mới); ruptures và cách chọn penalty;
Hampel filter; aliasing/Nyquist; bộ lọc nhân quả vs không nhân quả (filtfilt, Kalman smoother,
HP filter end-point problem); wavelet denoising; các kiểu data leakage trong time series (bài
tổng quan gần nhất); đổi âm lịch sang dương lịch trong Python (thư viện còn bảo trì, kiểm đúng
ngày Tết 2000–2035 với nguồn chính thức); OpenAQ API v3 và giấy phép từng trạm Việt Nam.

Người dùng nhấn mạnh: TIỀN XỬ LÝ, KHỬ NHIỄU, hiểu sâu khái niệm. Mỗi kỹ thuật làm sạch/khử nhiễu
phải có: khi nào dùng, khi nào KHÔNG dùng, và thí nghiệm chứng minh bằng số.
Buổi 12–13 phải có test rò rỉ tự động trong lab/cham/. Dự án giữa chặng 1 dùng dữ liệu Việt Nam
thật; lỗi cài sẵn và lời giải KHÔNG vào zip — kiểm tools/dong_goi.py lọc đủ.
```

---

## Phase 5 — Chuẩn "dễ hiểu": quy tắc, công cụ kiểm, mẫu chuẩn ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-05.md`](todos/phase-05.md)

### Prompt copy-paste cho Phase 5:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-05.md — đọc trước.
Phase 4: XONG. Làm Phase 5 — chuẩn "dễ hiểu": tools/CHUAN-DE-HIEU.md, tools/kiem_de_hieu.py, khuôn buổi,
xuat_pdf.py, Phụ lục E, mẫu chuẩn buổi 1 mục 4.8, đo baseline đọc thử.

Bối cảnh: người dùng tự học buổi 1–13 và thấy tài liệu KHÓ HIỂU, phải hỏi ChatGPT. Đọc kỹ mục
"Chuẩn dễ hiểu" trong todos/quy-uoc.md (nguyên nhân gốc + D1–D12 + BƯỚC CUỐI) và
phan-hoi-hoc-vien.md trước khi làm gì khác.

BƯỚC 0 — RESEARCH SƯ PHẠM (bắt buộc): WebSearch + WebFetch về cách viết tài liệu kỹ thuật cho
người tự học: worked example effect, cognitive load (Sweller), concreteness fading, cách các
nguồn dạy giỏi (FPP, Seeing Theory, StatQuest, 3Blue1Brown) giải thích quantile, phân phối, tự
tương quan, rò rỉ; hiểu lầm phổ biến của người mới với khái niệm buổi 1–13. Ghi vào
tools/NGHIEN-CUU-SU-PHAM.md có nguồn + ngày.

Yêu cầu:
- CHUAN-DE-HIEU.md: mỗi quy tắc D1–D12 có cặp "trước/sau" trích từ tài liệu THẬT buổi 1–13.
- Mẫu chuẩn = buổi 1 mục 4.8 viết lại theo khuôn D2, trả lời được 4 câu người dùng đã phải hỏi
  ChatGPT (xem phan-hoi-hoc-vien.md). Đây là thước đo cho mọi phase sau — viết thật tốt.
- kiem_de_hieu.py chỉ báo cáo, có test; chạy thử trên 13 buổi, in bảng số vi phạm mỗi buổi.
- Đo baseline đọc thử trên bản cũ buổi 1, 7, 12. Nếu subagent KHÔNG bắt được chỗ người dùng đã
  vướng ở buổi 1 mục 4.8 thì prompt đọc thử còn yếu — sửa prompt trước.
- Chưa viết lại buổi nào ngoài mục 4.8 của buổi 1 (Phase 6–8 làm).
Xong: ruff, test kiem_de_hieu, xuat_pdf.py cho phụ lục E, cập nhật todos.
```

---

## Phase 6 — Viết lại buổi 1–3 + Phụ lục A, B cho dễ hiểu ✅

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-06.md`](todos/phase-06.md)

### Prompt copy-paste cho Phase 6:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-06.md — đọc trước.
Phase 5: XONG. Làm Phase 6 — VIẾT LẠI buổi 01, 02, 03 + phu-luc/A, B cho dễ hiểu.

Đọc trước: mục "Chuẩn dễ hiểu" trong todos/quy-uoc.md, tools/CHUAN-DE-HIEU.md (có mẫu chuẩn buổi 1 mục
4.8), phan-hoi-hoc-vien.md. Người đọc: biết Python cơ bản + toán phổ thông, chưa học thống kê
đại học, chưa biết forecasting, tự học một mình. Tiêu chí: đọc xong không phải tra ngoài.

BƯỚC 0 — RESEARCH SƯ PHẠM (rút gọn): với TỪNG khái niệm chính của buổi, tìm 2–3 cách giải thích
tốt (FPP, sách nhập môn, bài giảng đại học, Seeing Theory…) + hiểu lầm phổ biến của người mới.
Ghi buoi-NN/NGHIEN-CUU.md mục "Research viết lại" có nguồn + ngày. Không cần rà lại phiên bản thư
viện trừ khi phải đổi code.

Cho TỪNG buổi:
1. Đọc thử bản cũ (BƯỚC CUỐI, bước 3) → ghi số chỗ vướng + điểm quiz làm baseline.
2. Liệt kê khái niệm chính; > 6 → chọn giữ, còn lại chuyển "Nâng cao"/"Đọc thêm" hoặc bỏ.
3. Viết lại tai-lieu.md theo D1–D12: bảng "Từ mới", mỗi khái niệm theo khuôn D2 (ví dụ số nhỏ
   tính tay TRƯỚC dữ liệu thật), mỗi công thức có câu nói bằng lời có thay số, mỗi hình có
   "Cách đọc hình", mỗi bảng có "Đọc bảng", mỗi mục có "Tóm lại" + "Tự kiểm tra".
4. GIỮ NGUYÊN chỗ hở cố ý, lab/cham/, 00-nen/, dữ liệu. Con số cũ giữ; con số MỚI phải chạy thật
   bằng script trong dap-an/ (ghi seed). Hình mới/sửa sinh bằng dap-an/ve_hinh.py.
5. kiem-tra.md: đáp án giải thích vì sao đúng và vì sao lựa chọn khác sai.
6. make check vẫn: dap-an xanh, code đỏ đúng chỗ (tools/kiem_tra_lab.py NN).

BƯỚC CUỐI — ĐỌC THỬ NHƯ HỌC VIÊN MỚI: chạy đúng khối trong mục "Chuẩn dễ hiểu" của todos/quy-uoc.md.
Không tick ✅ khi chưa đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10).
Cuối cùng: kiem_de_hieu.py → kiem_tra_doc_lap.sh → xuat_pdf.py 1 2 3 → --kiem (12–24 trang).
Báo người dùng bảng trước/sau (chỗ vướng, quiz) cho từng buổi.
```

---

## Phase 7 — Rút gọn: chuẩn "gọn" D13 + buổi 1–3, Phụ lục A, B 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-07.md`](todos/phase-07.md)

### Prompt copy-paste cho Phase 7:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-07.md — đọc trước.
Phase 6: XONG. Làm Phase 7 — RÚT GỌN: đặt chuẩn "gọn" (D13) + công cụ kiểm, rồi cắt thừa buổi 01, 02, 03
+ phu-luc/A, B. Dễ hiểu nhưng KHÔNG dài dòng.

Bối cảnh: người dùng đọc bản viết lại Phase 6 và báo "dễ hiểu hơn nhưng dài dòng quá". Đọc trước: mục
"Chuẩn dễ hiểu" trong todos/quy-uoc.md (D13 + độ dài mới + BƯỚC CUỐI bước 5 "Rà gọn"), tools/CHUAN-DE-HIEU.md,
phan-hoi-hoc-vien.md, mục "Đọc thử" trong NGHIEN-CUU.md buổi 1–3 (biết chỗ nào từng bị báo khó — không được làm
khó lại). Người đọc không đổi: biết Python + toán phổ thông, tự học một mình.

BƯỚC 0 — RESEARCH (rút gọn): WebSearch + WebFetch về viết kỹ thuật ngắn gọn mà vẫn dễ hiểu (plain language
guidelines, Google developer style guide, "omit needless words", redundancy effect trong cognitive load theory,
expertise reversal). Ghi tools/NGHIEN-CUU-SU-PHAM.md mục "Gọn" có nguồn + ngày.

BƯỚC 1 — CHUẨN VÀ CÔNG CỤ (xong mới cắt):
- tools/CHUAN-DE-HIEU.md: mục D13 có ≥ 5 cặp trước/sau trích từ buổi 1–3, A, B thật; sửa bài mẫu buổi 1 mục 4.8
  cho gọn; thêm "Prompt biên tập gọn" (subagent biên tập viên: liệt kê lặp ý / câu rỗng / ví dụ thừa / bước D2
  thừa / giải thích điều đã biết, mỗi chỗ kèm đề xuất cắt + số chữ bớt; có danh sách KHÔNG được cắt); thêm vào
  "Prompt đọc thử" mục báo chỗ thấy dài/lặp.
- tools/kiem_de_hieu.py + test: trần do_dai 3.500–6.500; mã mới cau_rong, lap_y. tools/xuat_pdf.py --kiem:
  10–18 trang (phụ lục ≤ 18). tools/khuon-buoi/tai-lieu.md: khuôn D2 là trần, chỉ ví dụ số nhỏ + Tóm lại bắt buộc.

BƯỚC 2 — CẮT, cho TỪNG tài liệu:
1. Biên tập viên (subagent MỚI, "Prompt biên tập gọn") rà bản hiện tại → danh sách chỗ thừa.
2. Tự cắt theo danh sách + D13: mỗi ý một lần, bỏ câu rỗng, bỏ ví dụ thứ hai thừa, gộp NumPy + thư viện, Lab và
   "Lỗi thường gặp" trỏ về khái niệm thay vì giải thích lại, "Tóm lại" ≤ 3 câu không chép lại. Mục tiêu giảm ≥ 25%
   chữ (Phụ lục B ≥ 35%, xuống ≤ 18 trang — phụ lục là tra cứu, phần buổi 2 dạy kỹ thì chỉ tóm lại + trỏ về).
3. KHÔNG cắt: định nghĩa lần đầu, ví dụ số nhỏ tính tay, câu nói bằng lời có thay số, Cách đọc hình/Đọc bảng
   (làm ngắn được), Mượn trước, chỗ đã sửa từ phan-hoi-hoc-vien.md. Không đổi code/, lab/, dap-an/, dữ liệu,
   con số đã đo. kiem-tra.md: chỉ gọn đáp án dài, giữ D12.
4. Đọc thử lại bằng subagent MỚI (BƯỚC CUỐI bước 3–4): vẫn 0 chặn, ≤ 5 khó, quiz ≥ 9/10. Chỗ khó quay lại →
   viết lại câu đó rõ hơn, không khôi phục đoạn cũ. Rồi biên tập viên MỚI rà lần cuối: ≤ 3 chỗ thừa đáng kể.
5. Ghi NGHIEN-CUU.md mục "Đọc thử": chữ/trang trước → sau, chỗ thừa đã cắt, kết quả đọc thử lại.

Cuối cùng: cập nhật CLAUDE.md (quy tắc 13–14, DoD) theo số đã chốt; ruff → test kiem_de_hieu →
kiem_de_hieu.py 1 2 3 → kiem_tra_lab.py 1 2 3 → kiem_tra_doc_lap.sh → xuat_pdf.py 1 2 3 A B → --kiem.
Báo người dùng bảng trước/sau (chữ, trang, chặn/khó, quiz) và 2–3 đoạn trước/sau tiêu biểu để họ duyệt độ gọn.
```

---

## Phase 8 — Viết lại buổi 4–8 + Phụ lục C cho dễ hiểu 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-08.md`](todos/phase-08.md)

### Prompt copy-paste cho Phase 8:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-08.md — đọc trước.
Phase 7: XONG. Làm Phase 8 — VIẾT LẠI buổi 04..08 + phu-luc/C cho dễ hiểu VÀ gọn.

Đọc trước: mục "Chuẩn dễ hiểu" trong todos/quy-uoc.md (D1–D13), tools/CHUAN-DE-HIEU.md, phan-hoi-hoc-vien.md,
và bảng trước/sau của Phase 6–7 trong NGHIEN-CUU.md buổi 1–3 (học từ chỗ đã sửa và chỗ đã cắt). Người đọc:
biết Python cơ bản + toán phổ thông, chưa học thống kê đại học, tự học một mình.

Đây là cụm TRỌNG TÂM của người dùng: đọc biểu đồ và phân tích tương quan. Mỗi hình phải có
"Cách đọc hình" 5 bước (trục ngang → trục dọc + đơn vị → màu/đường → nhìn vào đâu → kết luận).
ACF, PACF, tính dừng, ADF/KPSS, CCF, prewhitening, mutual information, Granger: TRỰC GIÁC + VÍ DỤ
SỐ NHỎ TÍNH TAY TRƯỚC công thức. Khái niệm thống kê chưa dạy (p-value, kiểm định) → hộp "Mượn trước".

BƯỚC 0 — RESEARCH SƯ PHẠM (rút gọn): với TỪNG khái niệm chính, 2–3 cách giải thích tốt + hiểu lầm
phổ biến của người mới; ghi buoi-NN/NGHIEN-CUU.md mục "Research viết lại" có nguồn + ngày.

Quy trình mỗi buổi, giữ-nguyên và kiểm lab: y hệt Phase 6 (xem prompt Phase 6 bước 1–6), nhưng viết theo
D1–D13: GỌN NGAY TỪ ĐẦU — mỗi ý nói một lần, khuôn D2 là trần (bước nào không thêm hiểu biết thì bỏ), sửa chỗ
vướng bằng cách viết lại câu chứ không chèn đoạn. Trần 3.500–6.500 chữ ngoài bảng/code, PDF 10–18 trang.

BƯỚC CUỐI — ĐỌC THỬ NHƯ HỌC VIÊN MỚI: chạy đúng khối trong mục "Chuẩn dễ hiểu" của todos/quy-uoc.md.
gồm bước 5 "Rà gọn" (biên tập viên ≤ 3 chỗ thừa). Không tick ✅ khi chưa đạt. Cuối cùng: kiem_de_hieu.py →
kiem_tra_doc_lap.sh → xuat_pdf.py 4..8 → --kiem (10–18 trang). Báo người dùng bảng trước/sau từng buổi
(chỗ vướng, quiz, số chữ).
```

---

## Phase 9 — Viết lại buổi 9–13 + đề dự án giữa chặng 1 + Phụ lục D cho dễ hiểu 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-09.md`](todos/phase-09.md)

### Prompt copy-paste cho Phase 9:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-09.md — đọc trước.
Phase 8: XONG. Làm Phase 9 — VIẾT LẠI buổi 09..13 + đề du-an-giua-chang/01-eda-lam-sach/ +
phu-luc/D cho dễ hiểu VÀ gọn (D1–D13).

Đọc trước: mục "Chuẩn dễ hiểu" trong todos/quy-uoc.md, tools/CHUAN-DE-HIEU.md, phan-hoi-hoc-vien.md,
bảng trước/sau của Phase 6–8. Người đọc: biết Python cơ bản + toán phổ thông, chưa học thống kê
đại học, tự học một mình. Cụm TRỌNG TÂM thứ hai: tiền xử lý, khử nhiễu, rò rỉ. Mỗi kỹ thuật:
khi nào dùng / khi nào KHÔNG dùng bằng lời thường + ví dụ số nhỏ tính tay + thí nghiệm có số.
Rò rỉ: mỗi kiểu có bảng vài dòng chỉ ra ô nào nhìn trộm tương lai.

BƯỚC 0 — RESEARCH SƯ PHẠM (rút gọn): như Phase 6–8.
Quy trình mỗi buổi, giữ-nguyên và kiểm lab: y hệt Phase 6 (bước 1–6), viết GỌN NGAY TỪ ĐẦU theo D13 như
Phase 8 (trần 3.500–6.500 chữ, PDF 10–18 trang; đề dự án ngắn nhất có thể). Lỗi cài sẵn và lời giải
dự án giữa chặng 1 KHÔNG vào zip — chỉ viết lại đề và rubric cho dễ hiểu.

BƯỚC CUỐI — ĐỌC THỬ NHƯ HỌC VIÊN MỚI: chạy đúng khối trong mục "Chuẩn dễ hiểu" của todos/quy-uoc.md
gồm bước 5 "Rà gọn" (đề dự án: subagent phải nói lại đúng "nộp gì, chấm thế nào"). Không tick ✅ khi chưa đạt.
Cuối cùng: kiem_de_hieu.py → kiem_tra_doc_lap.sh → xuat_pdf.py 9..13 → --kiem (10–18 trang).
Báo người dùng bảng trước/sau từng buổi.
```

---

## Phase 10 — Buổi 14–17 · Đánh giá, backtest, ETS, ARIMA 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-10.md`](todos/phase-10.md)

### Prompt copy-paste cho Phase 10:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-10.md — đọc trước.
Phase 9: XONG. Làm Phase 10 — buổi 14..17 (lộ trình "Giai đoạn 2", nửa đầu).

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: FPP chương 5, 8, 9; Hyndman & Koehler 2006 (MASE); M5 guide (RMSSE/WRMSSE);
Bergmeir & Benítez về CV cho chuỗi thời gian; Diebold–Mariano bản Harvey hiệu chỉnh;
statsforecast bản mới nhất (AutoETS, AutoTheta, AutoARIMA, cross_validation).

Buổi 15 tạo ra bộ backtest mà cả khoá dùng — thiết kế cẩn thận, có test. Mọi mô hình phải so với
seasonal naive có kiểm định ý nghĩa. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 11 — Buổi 18–21 · Hồi quy động, gián đoạn, đa biến, tài chính 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-11.md`](todos/phase-11.md)

### Prompt copy-paste cho Phase 11:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-11.md — đọc trước.
Phase 10: XONG. Làm Phase 11 — buổi 18..21 (lộ trình "Giai đoạn 2", nửa sau).

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: FPP chương 7, 10, 12; Syntetos–Boylan classification, TSB (Teunter et al.);
nowcasting với dynamic factor / MIDAS (tổng quan mới), Philadelphia Fed RTDSM (KHÔNG dùng ALFRED/FRED); tình trạng Prophet (còn bảo
trì không); arch package bản mới, HAR-RV, Markov switching trong statsmodels; các phân tích
phản biện "deep learning dự báo giá cổ phiếu".

Buổi 19 chấm bằng chi phí tồn kho, không chỉ chỉ số thống kê. Buổi 20 dùng vintage thật — dùng số
liệu đã sửa là rò rỉ. Buổi 21 phải trung thực: dự báo giá gần như không thắng naive, nói rõ.
Cuối buổi 21 đạt cột mốc M2. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 12 — Buổi 22–24 · Machine learning + dự án giữa chặng 2 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-12.md`](todos/phase-12.md)

### Prompt copy-paste cho Phase 12:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-12.md — đọc trước.
Phase 11: XONG. Làm Phase 12 — buổi 22..24 + du-an-giua-chang/02-thi-du-bao/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: global vs local models (Montero-Manso & Hyndman); chiến lược đa bước (Taieb et al.);
lời giải top M5 và bài tổng kết M5 accuracy; mlforecast + LightGBM bản mới; AutoGluon-TimeSeries
bản mới nhất (preset, model zoo); forecast combination puzzle; FFORMA; cold start forecasting;
EIA-930 API v2 (endpoint, trường day-ahead forecast, độ trễ công bố, sửa số liệu lùi).

Dự án giữa chặng 2 phải chấm trên dữ liệu TƯƠNG LAI THẬT (chưa tồn tại lúc nộp) và so với dự báo
day-ahead mà đơn vị điều độ công bố trong EIA-930. Viết script lấy dữ liệu + chấm tự động +
leaderboard. Thời tiết dùng làm feature phải là thời tiết DỰ BÁO lưu trữ, bộ chấm kiểm điều này.
Cuối buổi 24 đạt cột mốc M3.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 13 — Buổi 25–28 · Bất định 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-13.md`](todos/phase-13.md)

### Prompt copy-paste cho Phase 13:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-13.md — đọc trước.
Phase 12: XONG. Làm Phase 13 — buổi 25..28 (lộ trình "Giai đoạn 4 — Bất định").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: Gneiting & Raftery (proper scoring rules), Gneiting calibration/sharpness; WIS
(Bracher et al. 2021); conformal cho chuỗi thời gian — ACI (Gibbs & Candès), EnbPI, các bài
benchmark 2026 và MAPIE bản mới nhất; pymc + pymc-extras statespace bản mới; GP kernel cho chuỗi
thời gian; FPP chương 11, MinT (Wickramasuriya et al.), probabilistic reconciliation mới nhất,
hierarchicalforecast bản mới; giấy phép bộ Tourism Australia.

Mọi dự báo từ phase này trở đi phải có khoảng đã kiểm calibration. Buổi 27 không dùng posterior
chưa qua chẩn đoán hội tụ. Cuối buổi 28 đạt cột mốc M4. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 14 — Buổi 29–33 · Deep learning 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-14.md`](todos/phase-14.md)

### Prompt copy-paste cho Phase 14:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-14.md — đọc trước.
Phase 13: XONG. Làm Phase 14 — buổi 29..33 (lộ trình "Giai đoạn 5 — Deep learning").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: FPP chương 14; neuralforecast + PyTorch bản mới; bài gốc N-BEATS, N-HiTS, DeepAR,
TFT, TiDE, PatchTST, iTransformer, TSMixer, DLinear ("Are Transformers Effective...") và các bài
phản biện benchmark/`drop_last` gần nhất; kiến trúc SOTA mới ra trong 12 tháng (có thể phải thay
một kiến trúc trong buổi 30/31); TimeGrad, CSDI và diffusion cho dự báo; đánh giá dữ liệu tổng
hợp chuỗi thời gian; ECMWF Open Data AIFS (định dạng, biến, giấy phép, cách tải điểm), NOAA ISD
trạm Nội Bài, WeatherBench 2; PyTorch Geometric Temporal / GNN cho METR-LA chạy CPU.

Mọi lab phải chạy trên CPU trong thời gian hợp lý (ghi rõ phút), có cấu hình rút gọn cho máy 8 GB.
Mọi bảng so sánh phải có seasonal naive + một mô hình thống kê + LightGBM — kể cả khi DL thua.
Model/checkpoint chốt revision. Cuối buổi 33 đạt cột mốc M5.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 15 — Buổi 34–37 · Foundation model và LLM 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-15.md`](todos/phase-15.md)

### Prompt copy-paste cho Phase 15:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-15.md — đọc trước.
Phase 14: XONG. Làm Phase 15 — buổi 34..37 (lộ trình "Giai đoạn 6 — Foundation model và LLM").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng — KỸ HƠN mọi phase khác vì lĩnh vực đổi hàng tháng:
- Bảng xếp hạng GIFT-Eval và fev-bench HIỆN TẠI: top model, cột "không rò dữ liệu", model mới ra
  sau Chronos-2 / TimesFM 2.5 / Moirai 2 / TiRex / Toto 2.0 / Sundial; cập nhật danh sách model trong buổi
- Ngày phát hành + mô tả dữ liệu huấn luyện của từng model (để chọn dữ liệu đánh giá sạch)
- Bài về calibration của foundation model, fine-tune/LoRA, catastrophic forgetting
- TimeCopilot và agent dự báo khác; benchmark dự báo có ngữ cảnh văn bản ("Context is Key" và mới hơn)
- ForecastBench: leaderboard hiện tại, định dạng question set/resolution, giấy phép; bài về rò rỉ thời
  gian khi backtest LLM (arXiv 2608.02985, 2601.13717 và mới hơn); kiến trúc bot top
- Model LLM mở chạy local tốt nhất hiện tại cho suy luận trên CPU/GPU nhỏ; giá API hiện tại

Buổi 36–37 BẮT BUỘC chạy được không cần API key trả phí (model mở local + bản ghi phản hồi).
Mọi đánh giá foundation model/LLM phải trên dữ liệu SAU mốc cắt của model — ghi rõ mốc trong
"Trạng thái đầu buổi". Cuối buổi 37 đạt cột mốc M6.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 16 — Buổi 38–40 · Nhân quả và ra quyết định 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-16.md`](todos/phase-16.md)

### Prompt copy-paste cho Phase 16:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-16.md — đọc trước.
Phase 15: XONG. Làm Phase 16 — buổi 38..40 (lộ trình "Giai đoạn 7 — Nhân quả và ra quyết định").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: CausalImpact bản Python còn bảo trì (tfcausalimpact / causalimpact / PyMC-Marketing
/ CausalPy — chọn cái đang sống); synthetic control (Abadie) và synthetic DiD; DoubleML/EconML bản
mới; forecast value added (Gilliland); newsvendor + inventory policy với dự báo xác suất; FPP
chương 6 (judgmental); nghiên cứu về truyền đạt bất định cho người không chuyên (fan chart).

Mọi phương pháp nhân quả phải được kiểm trên dữ liệu mô phỏng có đáp án TRƯỚC khi áp lên dữ liệu
thật. Buổi 40 phải quy ra tiền. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 17 — Buổi 41–43 · Production và MLOps 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-17.md`](todos/phase-17.md)

### Prompt copy-paste cho Phase 17:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-17.md — đọc trước.
Phase 16: XONG. Làm Phase 17 — buổi 41..43 (lộ trình "Giai đoạn 8 — Production và MLOps").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào buoi-NN/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: Prefect vs Dagster bản mới (chọn một, ghi lý do); pandera, MLflow, DVC bản mới;
point-in-time/feature store cho chuỗi thời gian; statsforecast/mlforecast phân tán (Ray, Spark,
Dask qua Fugue) còn hỗ trợ không; phục vụ foundation model trên CPU; drift detection cho chuỗi
thời gian (PSI, ADWIN, Page–Hinkley — river bản mới); bài học vận hành hệ thống dự báo lớn (Uber,
Amazon, Walmart…) công khai gần đây.

Buổi 41 phải tái lập từng byte. Buổi 43 dùng replay dữ liệu thật với sự cố cài sẵn, không mô phỏng
tay từng cảnh báo. Cuối buổi 43 đạt cột mốc M7.

CHUẨN DỄ HIỂU + GỌN (bắt buộc): viết theo D1–D13 NGAY TỪ ĐẦU — todos/quy-uoc.md mục "Chuẩn dễ hiểu" +
tools/CHUAN-DE-HIEU.md (bài mẫu buổi 1 mục 4.8); đọc phan-hoi-hoc-vien.md trước. Dễ hiểu nhưng KHÔNG dài
dòng: mỗi ý nói một lần, khuôn D2 là trần, không câu rỗng, sửa chỗ vướng bằng viết lại câu chứ không chèn
đoạn; 3.500–6.500 chữ ngoài bảng/code. BƯỚC CUỐI đọc thử + rà gọn cho TỪNG buổi; không tick ✅ khi chưa
đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10, biên tập viên ≤ 3 chỗ thừa). PDF --kiem 10–18 trang.
```

---

## Phase 18 — Dự án cuối khoá 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-18.md`](todos/phase-18.md)

### Prompt copy-paste cho Phase 18:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-18.md — đọc trước.
Phase 17: XONG. Làm Phase 18 — du-an-cuoi/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào du-an-cuoi/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: cách tổ chức các cuộc thi dự báo trực tiếp (M6, GEFCom, ForecastBench, VN
competitions nếu có); tình trạng hiện tại của EIA-930 API và OpenAQ (trạm Hà Nội/TP.HCM còn hoạt
động không, độ trễ dữ liệu); rubric chấm dự án ML thực tế; model card (Mitchell et al.) bản mới.

Đề và rubric lấy nguyên từ mục "Buổi 44 — Dự án cuối" của lo-trinh/lo-trinh-forecasting.md.
Bộ chấm tự động ~50/100. Lời giải mẫu và ngay-du-lieu-hong/ KHÔNG vào zip — kiểm dong_goi.py lọc đủ.
Hai hạng mục không được bỏ: chấm trên dữ liệu TƯƠNG LAI THẬT (dấu thời gian dự báo có trước dữ liệu)
và "ngày dữ liệu hỏng" do giám khảo giữ. Chạy thử toàn bộ bộ chấm với lời giải mẫu đề B trong 3 ngày
dự báo trực tiếp thật trước khi tick ✅. Đề phát học viên xuất PDF bằng tools/xuat_pdf.py.

CHUẨN DỄ HIỂU (bắt buộc — bài học 2026-09-18): mọi văn bản học viên đọc (đề, rubric, hướng dẫn,
câu hỏi, đáp án) theo D1–D13 phần áp dụng được (todos/quy-uoc.md mục "Chuẩn dễ hiểu") — rõ và
GỌN: đề nói đủ một lần, không lặp giữa đề/rubric/hướng dẫn. Đọc phan-hoi-hoc-vien.md trước.
BƯỚC CUỐI — ĐỌC THỬ: subagent đóng vai học viên (đã học tới buổi tương ứng, KHÔNG tra web) đọc đề
phải nói lại đúng "làm gì, nộp gì, chấm thế nào" và liệt kê mọi chỗ mơ hồ; rồi biên tập viên MỚI
("Prompt biên tập gọn") rà chỗ thừa. 0 chỗ mơ hồ và ≤ 3 chỗ thừa mới tick ✅. Ghi kết quả vào
NGHIEN-CUU.md của phase.
```

---

## Phase 19 — Đánh giá 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-19.md`](todos/phase-19.md)

### Prompt copy-paste cho Phase 19:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-19.md — đọc trước.
Phase 18: XONG. Làm Phase 19 — danh-gia/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): làm đủ 6 bước "Giao thức research" trong
todos/quy-uoc.md; ghi vào danh-gia/NGHIEN-CUU.md. Lệch lớn → cập nhật lo-trinh + todos, báo người dùng TRƯỚC.
Research riêng: rà lại 44 buổi xem nội dung nào đã lỗi thời kể từ lúc soạn (thư viện đổi API,
model mới) — liệt kê vào NGHIEN-CUU.md trước khi viết câu hỏi dựa trên nội dung đó; cách viết
câu hỏi đánh giá hiểu sâu (không chỉ nhớ); chứng chỉ/khung năng lực dự báo hiện có (IIF CPF…).

Gộp quiz 44 buổi thành ngân hàng câu hỏi; 2 đề thực hành có script chấm; đề đọc biểu đồ 30 hình
thật (hình sinh bằng script, lưu trong repo); đề tìm rò rỉ chấm tự động. Mọi câu hỏi phải trỏ về buổi dạy nó.

CHUẨN DỄ HIỂU (bắt buộc — bài học 2026-09-18): mọi văn bản học viên đọc (đề, rubric, hướng dẫn,
câu hỏi, đáp án) theo D1–D13 phần áp dụng được (todos/quy-uoc.md mục "Chuẩn dễ hiểu") — rõ và
GỌN: đề nói đủ một lần, không lặp giữa đề/rubric/hướng dẫn. Đọc phan-hoi-hoc-vien.md trước.
BƯỚC CUỐI — ĐỌC THỬ: subagent đóng vai học viên (đã học tới buổi tương ứng, KHÔNG tra web) đọc đề
phải nói lại đúng "làm gì, nộp gì, chấm thế nào" và liệt kê mọi chỗ mơ hồ; rồi biên tập viên MỚI
("Prompt biên tập gọn") rà chỗ thừa. 0 chỗ mơ hồ và ≤ 3 chỗ thừa mới tick ✅. Ghi kết quả vào
NGHIEN-CUU.md của phase.
```

---

## Phase 20 — Xuất bản & đóng gói 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-20.md`](todos/phase-20.md)

### Prompt copy-paste cho Phase 20:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-20.md — đọc trước.
Phase 19: XONG. Làm Phase 20 — xuất bản: sinh 44 PDF, đóng gói phat-de/, cập nhật README.md và CLAUDE.md.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. WebSearch + WebFetch: phiên bản mới nhất của MỌI thư viện chính và model đã chốt trong 44 buổi;
   dataset nào đổi URL/giấy phép; bảng xếp hạng GIFT-Eval/fev-bench/ForecastBench hiện tại.
2. Ghi vào NGHIEN-CUU-XUAT-BAN.md: bảng "đã chốt → mới nhất → có cần cập nhật buổi nào không".
3. Lệch lớn (thư viện đổi API làm hỏng lab, model mới vượt hẳn) → báo lại người dùng TRƯỚC khi
   xuất bản, đề xuất phase cập nhật; không tự ý sửa hàng loạt.
4. Cập nhật dòng "Rà soát gần nhất" trong lộ trình.

README phải có bảng "học theo cụm" — mỗi buổi tự chứa nên khoá cắt được nhiều cách. README cũng theo
chuẩn dễ hiểu + gọn (D1–D13): người mới đọc biết bắt đầu từ đâu, cần cài gì, học theo thứ tự nào —
không lặp lại nội dung lộ trình. --kiem: mọi buổi 10–18 trang, mọi buổi trong trần do_dai.
Bắt buộc kiểm chứng: unzip thử 4 file trong phat-de/ (gồm buổi 13, 24, 44), xác nhận không lọt
dap-an/, NGHIEN-CUU.md, loi-giai-mau/, ngay-du-lieu-hong/.
```

---

## Phase 21 — Kiểm định chất lượng 🔲

Chi tiết (bảng tiến độ, checklist, "Bắt buộc", ghi chú research): [`todos/phase-21.md`](todos/phase-21.md)

### Prompt copy-paste cho Phase 21:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Chi tiết phase (checklist, bảng tiến độ, mục "Bắt buộc"): todos/phase-21.md — đọc trước.
Phase 20: XONG. Làm Phase 21 — kiểm định: chạy tools/kiem_tra_lab.py cho cả 44 buổi trên venv
trắng, rà mạch kiến thức và các cột mốc M0–M7.

BƯỚC 0 — RESEARCH TRƯỚC KHI KIỂM (bắt buộc, không bỏ qua):
1. WebSearch + WebFetch: thư viện/model/dataset nào đã đổi kể từ ngày ghi trong từng NGHIEN-CUU.md.
2. Lập bảng "buổi có nguy cơ lỗi thời" trước khi chạy — để phân biệt lỗi do nội dung với lỗi do
   môi trường thay đổi.
3. Ghi vào KIEM-DINH.md cùng kết quả kiểm định.

BÀI QUAN TRỌNG NHẤT: copy ngẫu nhiên 6 thư mục buổi sang máy trắng, KHÔNG có phần còn lại của repo,
rồi chạy make up && make check. Thêm bài CPU-only (buổi 29–35) và bài không API key (buổi 36–37).
Bài quan trọng thứ hai: ĐỌC THỬ + RÀ GỌN — kiem_de_hieu.py cả 44 buổi (kể cả do_dai, cau_rong, lap_y) +
subagent học viên mới và biên tập viên mới đọc 6 buổi ngẫu nhiên (khối BƯỚC CUỐI trong mục "Chuẩn dễ
hiểu"); đối chiếu phan-hoi-hoc-vien.md đã xử lý hết.
Báo cáo dạng bảng: buổi nào xanh, buổi nào hỏng, hỏng ở bước nào, thời gian chạy. Đừng sửa lấy
được — nêu rõ trước.
```

---

## General Copy-paste Prompt (dùng khi không nhớ đang ở phase nào):
```text
Khoá Forecasting in AI 44 buổi (cơ bản → nâng cao) | Working dir: /home/tony/Tony/Forecasting/
Lộ trình: lo-trinh/lo-trinh-forecasting.md
Kế hoạch & tiến độ: todos.md   ← đọc, tìm phase đầu tiên có 🔲, làm phase đó (chi tiết: todos/phase-NN.md)

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): chạy đúng "Giao thức research" trong
todos/quy-uoc.md + phần "Research riêng" trong prompt của phase đó. Ghi NGHIEN-CUU.md có
nguồn và ngày. Lệch lớn so với lộ trình → cập nhật lộ trình + todos và báo lại TRƯỚC khi soạn.

Quy ước bắt buộc (todos/quy-uoc.md):
- Mỗi buổi TỰ CHỨA TUYỆT ĐỐI: buổi N không đọc một byte nào ngoài buoi-NN/ (trừ cache dữ liệu có
  sha256). Nền ở lab/00-nen/ sinh bằng tools/sinh_nen.py. Kiểm bằng tools/kiem_tra_doc_lap.sh
- tai-lieu.md đủ 9 mục (có "Trạng thái đầu buổi") + code/ (chỗ hở cố ý) + dap-an/ + lab/00-nen/
  + lab/cham/ + lab/Makefile + kiem-tra.md + NGHIEN-CUU.md
- Trọng tâm người dùng: tiền xử lý, khử nhiễu, hiểu sâu khái niệm, đọc biểu đồ, phân tích tương quan,
  dự án thực tế
- DỄ HIỂU và GỌN là tiêu chí nghiệm thu (mục "Chuẩn dễ hiểu", D1–D13, tools/CHUAN-DE-HIEU.md): người đọc biết
  Python + toán phổ thông, tự học — đọc xong không phải tra ngoài. Bảng "Từ mới"; ≤ 6 khái niệm/buổi;
  mỗi khái niệm: vấn đề → trực giác → ví dụ số nhỏ tính tay → hình → công thức → nói bằng lời có thay
  số → NumPy → thư viện → dữ liệu thật → tóm lại. Đọc phan-hoi-hoc-vien.md trước khi soạn
- Chỗ hở phổ biến nhất là RÒ RỈ TƯƠNG LAI và ĐÁNH GIÁ KHÔNG TRUNG THỰC; từ buổi 12 mọi lab có test rò rỉ
- MỌI lệnh và MỌI con số trong tài liệu phải lấy từ lần chạy thật
- Chốt phiên bản trong uv.lock; model chốt revision; không latest. Mọi lab chạy được bằng CPU
- Dữ liệu: mỗi bộ có giấy phép đã xác minh; cấm phân phối lại thì học viên tự tải, luôn có dự phòng mở
- dap-an/, NGHIEN-CUU.md, loi-giai-mau/, ngay-du-lieu-hong/ KHÔNG bao giờ vào zip phát học viên
- Xong buổi nào: ruff → kiem_de_hieu → kiem_tra_doc_lap → chạy lab trên venv trắng → ĐỌC THỬ bằng subagent
  học viên mới (0 chặn, ≤ 5 khó, quiz ≥ 9/10) → RÀ GỌN bằng subagent biên tập viên (≤ 3 chỗ thừa) → xuất PDF
  (--kiem 10–18 trang) → tick ✅
```
