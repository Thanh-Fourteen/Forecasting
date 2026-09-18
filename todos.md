# Khoá Forecasting in AI — Phased Todo Plan
Mục tiêu: **44 buổi** (cơ bản → nâng cao) | **giáo trình .md + PDF + code chạy được trên dữ liệu thật** | Nguồn lộ trình: [`lo-trinh/lo-trinh-forecasting.md`](lo-trinh/lo-trinh-forecasting.md)

**44 buổi** = 3 nền móng + **10 hiểu & chuẩn bị dữ liệu** + 8 thống kê + 3 ML + 4 bất định + 5 deep learning
+ 4 foundation model & LLM + 3 nhân quả & quyết định + 3 production + 1 dự án cuối.
Kèm **2 dự án giữa chặng** (sau buổi 13 và 24).

Repo: `/home/tony/Tony/Forecasting/` — repo độc lập, mọi đường dẫn dưới đây tính từ gốc repo

---

## Quy ước (đọc trước khi làm bất kỳ phase nào)

### Giao thức research — BẮT BUỘC trước mọi phase

Lĩnh vực này đổi rất nhanh (foundation model, LLM, thư viện Nixtla ra bản mới vài tháng một lần).
Kiến thức trong lộ trình chỉ đúng tới ngày rà soát. **Mọi prompt phase bên dưới đều mở đầu bằng
khối này — không được bỏ qua, kể cả khi thấy mình đã biết chủ đề:**

```text
BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
```

### Cấu trúc thư mục đích

```text
.                                   gốc repo /home/tony/Tony/Forecasting/
├── README.md                       bản đồ khoá, bảng 44 buổi, học theo cụm
├── CLAUDE.md                       quy tắc soạn nội dung cho phiên làm việc sau
├── todos.md                        kế hoạch này
├── lo-trinh/                       lộ trình 44 buổi (.md + .pdf)
├── MOI-TRUONG.md                   cài uv/Python/Jupyter, API key OpenAQ/EIA/Kaggle, Ollama — Linux/macOS/WSL2
├── phu-luc/                        phụ lục dùng chung, mọi buổi TRỎ TỚI thay vì lặp lại
│   ├── A-python-chuoi-thoi-gian.md
│   ├── B-xac-suat-toi-thieu.md
│   ├── C-so-tay-doc-bieu-do.md     mỗi loại biểu đồ: đọc gì, bẫy gì, ví dụ đúng/sai
│   ├── D-cong-thuc-chi-so.md       MAE…CRPS, WIS, Brier — công thức + khi nào dùng
│   ├── E-tu-dien-thuat-ngu.md
│   └── F-nguon-du-lieu.md          MỌI bộ dữ liệu: URL, giấy phép, được mirror không, sha256
├── buoi-01/ … buoi-44/             MỖI THƯ MỤC TỰ CHỨA — không trỏ ra ngoài chính nó
│   ├── tai-lieu.md                 NGUỒN của PDF  ← chỉ sửa ở đây
│   ├── <CHU-DE>-buoi-NN.pdf        sinh ra
│   ├── NGHIEN-CUU.md               nhật ký research (BƯỚC 0) — KHÔNG vào zip
│   ├── hinh/                       ảnh dùng trong tài liệu, sinh bằng dap-an/ve_hinh.py (không vẽ tay)
│   ├── code/                       ĐIỂM XUẤT PHÁT chạy được (có chỗ hở cố ý), .py dạng percent
│   │   └── README.md
│   ├── dap-an/                     bản hoàn chỉnh — KHÔNG vào zip
│   ├── lab/
│   │   ├── nen.toml                buổi cần thư viện nào, bộ dữ liệu nào (VIẾT TAY — nguồn của 00-nen/)
│   │   ├── 00-nen/                 NỀN của buổi (sinh bằng tools/sinh_nen.py)
│   │   │   ├── pyproject.toml      phụ thuộc CHỐT phiên bản
│   │   │   ├── uv.lock
│   │   │   ├── du-lieu.toml        URL + sha256 + giấy phép + khoảng thời gian cố định
│   │   │   ├── tv/                 thư viện trợ giúp COPY từ tools/khung/, cài editable — `import tv`
│   │   │   ├── lay_du_lieu.py      BẢN SAO tools/lay_du_lieu.py
│   │   │   └── chuan-bi.sh         uv sync --frozen + tải dữ liệu + kiểm sha256
│   │   ├── du-lieu/raw/            dữ liệu đã kiểm sha256, chỉ đọc (gitignore)
│   │   ├── cham/                   test_*.py — bộ chấm của `make check`
│   │   └── Makefile                up / check / down / notebook
│   └── kiem-tra.md                 10 câu quiz + đáp án trong <details>
├── du-an-giua-chang/
│   ├── 01-eda-lam-sach/            đề, rubric, bộ chấm, lỗi cài sẵn (giám khảo giữ)
│   └── 02-thi-du-bao/              đề, rubric, bộ chấm dữ liệu tương lai, leaderboard
├── du-an-cuoi/                     3 đề A/B/C, rubric 100+20, bộ chấm, "ngày dữ liệu hỏng"
├── danh-gia/                       ngân hàng câu hỏi, đề giữa khoá, đề cuối khoá
├── phat-de/                        sinh ra: buoi-NN.zip (gitignore)
├── pyproject.toml                  cấu hình ruff + jupytext (KHÔNG phải dự án, KHÔNG workspace)
└── tools/
    ├── NGHIEN-CUU.md               research Phase 0
    ├── requirements.txt            phụ thuộc của bộ công cụ
    ├── nen/phien-ban.toml          phiên bản CHUNG mọi thư viện + exclude-newer + [[rang_buoc]]
    ├── khuon-buoi/                 khuôn một buổi: cp -r tools/khuon-buoi buoi-NN
    ├── xuat_pdf.py                 md → PDF: công thức LaTeX → SVG, ảnh, bìa + mục lục, --kiem số trang
    ├── dong_goi.py                 zip cho học viên, loại dap-an/, NGHIEN-CUU.md, lời giải
    ├── sinh_nen.py                 sinh buoi-NN/lab/00-nen/ từ tools/khung/ + danh mục dữ liệu
    ├── lay_du_lieu.py              tải theo du-lieu.toml, kiểm sha256, cache ~/.cache/khoa-forecasting/
    ├── kiem_tra_doc_lap.sh         CHẶN tham chiếu chéo, phụ thuộc không chốt, dữ liệu không sha256
    ├── kiem_tra_lab.py             chạy make up/check/down mọi buổi, in bảng kết quả
    ├── kiem_ro_ri.py               kiểm rò rỉ tương lai tự động (dùng trong cham/ của mọi buổi)
    ├── khung/                      NGUỒN của tv/: ve.py, danh_gia.py, backtest.py, ro_ri.py, du_lieu.py
    └── du-lieu/danh-muc.toml       danh mục gốc mọi bộ dữ liệu của khoá
```

### Nguyên tắc nội dung

1. **Mỗi buổi tự chứa — không có ngoại lệ.** Buổi N **không đọc một byte nào ngoài `buoi-NN/`**
   (trừ cache dữ liệu tải về có kiểm sha256). Không `../buoi-06/...`, không "dùng lại dữ liệu đã
   làm sạch ở buổi trước", không import từ `tools/`. Học viên nghỉ một buổi vẫn học được.
2. **Cơ chế `lab/00-nen/`** — nền của buổi:
   - `pyproject.toml` + `uv.lock` **riêng mỗi buổi**, Python 3.12, chỉ cài thư viện buổi đó cần
   - `du-lieu.toml`: mỗi bộ dữ liệu có URL, **sha256**, giấy phép, **khoảng thời gian cố định**
     (không "lấy tới hôm nay" — trừ bài dự báo trực tiếp có ghi rõ)
   - `tv/` là **bản copy** của `tools/khung/`, sinh bằng `python tools/sinh_nen.py N`.
     Sửa khung → chạy lại tool cho mọi buổi, **không sửa tay trong tv/**
   - Buổi cần dữ liệu đã xử lý (ví dụ PM2.5 đã làm sạch) → **tự làm sạch trong 00-nen/** hoặc tải
     bản mirror có sha256, không đọc từ buổi khác
3. **Phụ thuộc là kiến thức, không phải file** — cần kiến thức buổi khác thì trỏ `phu-luc/` hoặc
   tóm tắt tại chỗ.
4. **Chỗ hở cố ý** — `code/` phải sai đúng chỗ bài học hôm đó sửa (bảng dưới). Chỗ hở phổ biến
   nhất của khoá này là **rò rỉ tương lai** và **đánh giá không trung thực** — `code/` phải cho
   kết quả *đẹp giả tạo* để học viên tự phát hiện. Đừng sửa trước giờ dạy.
5. **Mọi lệnh và mọi con số trong tài liệu phải đã chạy thật.** Không có "sai số giảm khoảng 20%"
   viết cho đẹp — con số lấy từ output thật, ghi seed.
6. **Chốt phiên bản** — mọi thư viện chốt trong `uv.lock`, mọi model chốt theo **revision/commit
   trên Hugging Face**, mọi LLM chốt tên model đầy đủ có ngày. Không `latest`.
7. **Dữ liệu và giấy phép** —
   - CC BY / CC0 / public domain: được **mirror** (Hugging Face Datasets của khoá) kèm ghi nguồn → lab ổn định
   - Giấy phép cấm phân phối lại (Kaggle M5…): học viên **tự tải** bằng tài khoản mình; luôn có dữ liệu dự phòng mở
   - Không commit dữ liệu vào git. Ghi đủ ở Phụ lục F
8. **Chạy được bằng CPU** — mọi lab có nhánh CPU. GPU chỉ làm nhanh hơn. Buổi 36–37: nhánh model
   mở chạy local + **bản ghi phản hồi LLM** (`ghi-am/`) để chấm lại không cần API key.
9. **Tái lập** — seed cố định, `make check` chạy hai lần ra cùng kết quả (DL/LLM: cho phép sai số
   nhỏ có ghi ngưỡng trong test).
10. **Tài liệu tiếng Việt, thuật ngữ kỹ thuật giữ nguyên tiếng Anh** (backtest, seasonal naive,
    quantile, drift...). Thuật ngữ thống nhất theo Phụ lục E.
11. **Khung tài liệu mỗi buổi** (bắt buộc đủ **9 mục**):
    Mục tiêu → Nhắc lại buổi trước → **Trạng thái đầu buổi** → Lý thuyết → Lab từng bước →
    Lỗi thường gặp & cách chẩn đoán → Bài tập về nhà → Tiêu chí "Xong khi" → Đọc thêm.
    - *Lý thuyết* theo nhịp **trực giác → hình → công thức ($$...$$) → tự viết bằng NumPy → thư viện**
    - *Nhắc lại buổi trước* đủ để **không cần** mở lại buổi trước
    - *Trạng thái đầu buổi* là bảng liệt kê chính xác sau `make up`: dữ liệu nào (file, số dòng,
      khoảng thời gian, sha256 rút gọn), môi trường (Python + thư viện chính), `code/` có gì,
      **cái gì đang cố tình sai và triệu chứng nhìn thấy**
    - *Đọc thêm* trỏ chương FPP tương ứng (bảng đối chiếu trong lộ trình) + bài báo gốc
12. **Hình ảnh** — mọi biểu đồ trong tài liệu sinh bằng script trong `dap-an/ve_hinh.py`, lưu
    `hinh/*.png` (150 dpi). Biểu đồ phải qua chính chuẩn của buổi 4: tiêu đề nói kết luận, trục có đơn vị.
13. **Độ dài** — `tai-lieu.md` 2.500–4.000 chữ, PDF 10–16 trang (`python tools/xuat_pdf.py --kiem`).
    Dài hơn là đang nhồi hai buổi vào một.

### Deliverable của MỖI buổi (Definition of Done)

- [ ] **`NGHIEN-CUU.md`** — BƯỚC 0 đã chạy: nguồn có ngày, phiên bản đã xác minh, điểm lệch
- [ ] `tai-lieu.md` đủ **9 mục**, có "Trạng thái đầu buổi", công thức render đúng trong PDF
- [ ] `code/` chạy được, có chỗ hở cố ý, có `README.md` ngắn
- [ ] `dap-an/` là bản đã sửa, `make check` xanh
- [ ] `lab/00-nen/` dựng đúng nền **từ máy trắng** (`uv sync --frozen` + dữ liệu qua sha256)
- [ ] `lab/Makefile` có `up` / `check` / `down`; `up` < 10 phút khi đã có cache, `check` < 10 phút trên CPU 4 nhân
- [ ] `lab/cham/` có **test rò rỉ** (dùng `kiem_ro_ri`) cho mọi buổi từ 12 trở đi
- [ ] `kiem-tra.md` 10 câu: 4 nhắc lại khái niệm, 4 vận dụng (tính/chọn phương pháp), **2 đọc
      biểu đồ/bảng kết quả tìm chỗ sai**; đáp án trong `<details>`
- [ ] `ruff check` sạch; notebook sinh từ `.py` bằng jupytext, không commit output
- [ ] `tools/kiem_tra_doc_lap.sh` xanh
- [ ] PDF sinh ra, mở kiểm tra bảng, khối code, **công thức**, ảnh; 10–16 trang
- [ ] Chạy thử toàn bộ lab trên **máy/venv trắng** một lần trước khi tick ✅

### 44 buổi, tên PDF và chỗ hở cố ý

| Buổi | Chủ đề | PDF | Chỗ hở cố ý trong `code/` |
|---|---|---|---|
| 01 | Forecasting là gì | `GIOI-THIEU-buoi-01.pdf` | Đánh giá dự báo trên chính dữ liệu đã dùng để làm nó; không có baseline |
| 02 | Xác suất & thống kê | `XAC-SUAT-THONG-KE-buoi-02.pdf` | Khoảng "±1.96σ" cho dữ liệu lệch phải, bootstrap i.i.d. cho dữ liệu tự tương quan |
| 03 | Dữ liệu thời gian | `DU-LIEU-THOI-GIAN-buoi-03.pdf` | Timestamp naive, thời tiết lệch múi giờ 5 giờ, resample làm mất giờ DST |
| 04 | Đọc & vẽ biểu đồ | `BIEU-DO-buoi-04.pdf` | Chỉ có biểu đồ đường thô + trục kép + trục y cắt; bỏ lỡ mùa vụ tuần |
| 05 | Biến đổi & điều chỉnh | `BIEN-DOI-DIEU-CHINH-buoi-05.pdf` | So tháng không chỉnh số ngày/lạm phát; log–exp không hiệu chỉnh bias |
| 06 | Phân rã | `PHAN-RA-buoi-06.pdf` | Classical decomposition chu kỳ 24 cho dữ liệu có mùa vụ tuần |
| 07 | Tự tương quan & tính dừng | `TU-TUONG-QUAN-buoi-07.pdf` | Kết luận "dừng" chỉ bằng ADF, sai phân thừa |
| 08 | Tương quan giữa các chuỗi | `TUONG-QUAN-CHEO-buoi-08.pdf` | Kết luận từ Pearson giữa hai chuỗi có xu hướng; CCF chưa prewhiten; Granger = nhân quả |
| 09 | Đặc trưng & khả năng dự báo | `DAC-TRUNG-CHUOI-buoi-09.pdf` | Tune mô hình đều cho mọi chuỗi, kể cả chuỗi entropy cao không dự báo được |
| 10 | Làm sạch & dữ liệu thiếu | `LAM-SACH-DU-LIEU-buoi-10.pdf` | `fillna(0)` cho cảm biến mất tín hiệu; bỏ qua mốc thời gian thiếu hẳn; nội suy hai chiều trước khi chia tập |
| 11 | Ngoại lai & điểm gãy | `NGOAI-LAI-DIEM-GAY-buoi-11.pdf` | Xoá mọi điểm > 3σ toàn chuỗi — xoá luôn Tết; không phát hiện level shift COVID |
| 12 | Khử nhiễu & miền tần số | `KHU-NHIEU-TAN-SO-buoi-12.pdf` | Feature từ rolling centered + `filtfilt` → backtest đẹp giả tạo; hạ mẫu không lọc gây aliasing |
| 13 | Feature & chống rò rỉ | `FEATURE-RO-RI-buoi-13.pdf` | Rolling không `shift`, scaler fit toàn bộ, nhiệt độ thực tế thay nhiệt độ dự báo, lễ âm lịch hardcode 1 năm |
| 14 | Baseline & chỉ số | `BASELINE-CHI-SO-buoi-14.pdf` | Báo cáo MAPE cho chuỗi có số 0; không có seasonal naive |
| 15 | Backtesting | `BACKTEST-buoi-15.pdf` | `train_test_split(shuffle=True)`, tune và báo cáo trên cùng cửa sổ |
| 16 | ETS & Theta | `ETS-THETA-buoi-16.pdf` | Holt-Winters cộng cho chuỗi có biên độ mùa vụ tăng theo mức |
| 17 | ARIMA | `ARIMA-buoi-17.pdf` | auto-ARIMA tắt mùa vụ trên dữ liệu tháng; không kiểm phần dư |
| 18 | Hồi quy động | `HOI-QUY-DONG-buoi-18.pdf` | Hồi quy OLS có phần dư tự tương quan, p-value "đẹp"; Prophet mặc định không khai Tết |
| 19 | Nhu cầu gián đoạn | `NHU-CAU-GIAN-DOAN-buoi-19.pdf` | ETS cho chuỗi 80% số 0, đánh giá bằng MAPE |
| 20 | Đa biến & nowcasting | `DA-BIEN-STATE-SPACE-buoi-20.pdf` | VAR trên chuỗi I(1) không kiểm cointegration; nowcast dùng số liệu đã sửa (không vintage) |
| 21 | Tài chính & biến động | `TAI-CHINH-GARCH-buoi-21.pdf` | Notebook "LSTM đoán giá chính xác 99%" (thực chất là naive trễ 1 bước) |
| 22 | Dự báo thành hồi quy | `ML-HOI-QUY-buoi-22.pdf` | Chiến lược direct dùng lag 1 cho h = 7; cây quyết định trên chuỗi có xu hướng không sai phân |
| 23 | Gradient boosting | `GRADIENT-BOOSTING-buoi-23.pdf` | LightGBM L2 cho dữ liệu đếm thưa; Optuna tune bằng KFold ngẫu nhiên |
| 24 | Ensemble & AutoML | `ENSEMBLE-AUTOML-buoi-24.pdf` | Chọn "mô hình tốt nhất" trong 30 mô hình trên chính tập báo cáo |
| 25 | Dự báo xác suất | `DU-BAO-XAC-SUAT-buoi-25.pdf` | Khoảng từ phần dư trong mẫu giả định chuẩn (coverage thật ~60%); quantile crossing |
| 26 | Conformal | `CONFORMAL-buoi-26.pdf` | Split conformal cố định trên chuỗi có drift → coverage trượt dần |
| 27 | Bayes & GP | `BAYES-GP-buoi-27.pdf` | Prior mặc định quá rộng, không prior predictive check; dùng posterior có divergence |
| 28 | Dự báo phân cấp | `PHAN-CAP-buoi-28.pdf` | Dự báo độc lập từng cấp — tổng cửa hàng ≠ dự báo toàn công ty |
| 29 | Nền DL | `DEEP-LEARNING-NEN-buoi-29.pdf` | Cắt cửa sổ trước khi chia tập (chồng lấn train/val); scaler fit toàn bộ |
| 30 | N-BEATS … TiDE | `NBEATS-TFT-buoi-30.pdf` | Nhiệt độ thực tế khai là `futr_exog` |
| 31 | Transformer | `TRANSFORMER-buoi-31.pdf` | Bảng benchmark `drop_last=True`, không có seasonal naive/DLinear |
| 32 | Mô hình sinh | `MO-HINH-SINH-buoi-32.pdf` | Mô hình sinh chép nguyên chuỗi train; chỉ chấm fidelity |
| 33 | Không gian–thời gian & thời tiết AI | `KHONG-GIAN-THOI-TIET-buoi-33.pdf` | Kiểm chứng AIFS bằng điểm lưới gần nhất, không hiệu chỉnh; đánh giá trên năm có trong tập huấn luyện |
| 34 | Foundation model | `FOUNDATION-MODEL-buoi-34.pdf` | So zero-shot trên dataset nằm trong tập huấn luyện trước; context 64 điểm cho dữ liệu giờ |
| 35 | Fine-tune & benchmark | `FINE-TUNE-BENCHMARK-buoi-35.pdf` | Fine-tune toàn bộ trên 200 điểm; covariate lệch 1 bước thời gian |
| 36 | LLM & agent | `LLM-AGENT-buoi-36.pdf` | Agent tự chọn tập test; báo cáo LLM có con số không có trong kết quả công cụ |
| 37 | Dự báo sự kiện bằng LLM | `DU-BAO-SU-KIEN-buoi-37.pdf` | Backtest bot trên câu hỏi resolve trước mốc cắt kiến thức; search không lọc ngày |
| 38 | Tác động can thiệp | `TAC-DONG-CAN-THIEP-buoi-38.pdf` | So trước/sau đơn giản, bỏ qua mùa vụ và xu hướng |
| 39 | Kịch bản & what-if | `KICH-BAN-WHAT-IF-buoi-39.pdf` | Partial dependence của mô hình dự báo dùng làm độ co giãn giá (sai dấu) |
| 40 | Dự báo → quyết định | `DU-BAO-QUYET-DINH-buoi-40.pdf` | Đặt hàng = dự báo trung bình; chọn mô hình theo MASE |
| 41 | Pipeline tái lập | `PIPELINE-TAI-LAP-buoi-41.pdf` | Notebook chạy tay, join không point-in-time, không kiểm schema, mỗi lần chạy một kết quả |
| 42 | Phục vụ quy mô lớn | `PHUC-VU-QUY-MO-buoi-42.pdf` | Vòng for tuần tự 145.000 chuỗi; API load mô hình mỗi request |
| 43 | Giám sát & drift | `GIAM-SAT-DRIFT-buoi-43.pdf` | Không giám sát đầu vào; cảnh báo dựa trên MAPE ngày (ồn); retrain cố định |
| 44 | Dự án cuối | `DU-AN-CUOI-buoi-44.pdf` | — |

---

## Phase 0 — Hạ tầng khoá học ✅ (trừ push remote)
Không có phase này thì mọi buổi sau đều phải làm lại.

- [x] Khởi tạo repo (`git init`, nhánh `master`), `.gitignore`
- [x] `lo-trinh/lo-trinh-forecasting.md` — 44 buổi, 9 giai đoạn, M0–M7, 2 dự án giữa chặng, dự án cuối, đối chiếu FPP; PDF 38 trang
- [x] `todos.md`, `CLAUDE.md`, `README.md`
- [x] **`tools/xuat_pdf.py`** — markdown-it + weasyprint; bảng `BUOI` 44 dòng + 11 trang lẻ; công thức
      `$…$`/`$$…$$` → SVG (ziamath, không cần LaTeX), `|` trong công thức ở bảng tự thoát; ảnh
      tương đối; bìa + mục lục có số trang; id heading kiểu GitHub nên link `#muc` chạy trong PDF;
      `--kiem` đếm trang, báo buổi ngoài 10–16. Đã kiểm với bảng, code chứa `$`, `<details>`, tiếng Việt
- [x] `tools/requirements.txt`; venv công cụ tại `.venv/` (uv)
- [x] **Research Phase 0** — `tools/NGHIEN-CUU.md` (2026-09-17): uv/ruff/jupytext, Kaggle/HF/EIA/OpenAQ/UCI/Open-Meteo, nguồn phụ lục A–E.
      Lệch lớn đã báo + sửa lộ trình/todos: hệ Nixtla chưa hỗ trợ pandas 3; trạm Đại sứ quán Mỹ ngừng từ 03/2025
- [x] `MOI-TRUONG.md` (+ PDF 6 trang) — uv, Python 3.12, JupyterLab + jupytext, API key (OpenAQ, EIA, Kaggle), Ollama/llama.cpp, Docker; Linux/macOS/WSL2
- [x] `pyproject.toml` gốc: ruff (select tường minh vì 0.16 đổi mặc định), jupytext `py:percent`; **không** `[project]`/workspace.
      Bỏ nbstripout: `*.ipynb` trong buổi bị gitignore (research mục 4)
- [x] **`tools/sinh_nen.py N`** — đọc `buoi-NN/lab/nen.toml` (tên thư viện + tên bộ dữ liệu) + `tools/nen/phien-ban.toml`
      (phiên bản CHUNG, `exclude-newer` cố định, `[[rang_buoc]]` tự chốt pandas 2.3.3 cho buổi dùng Nixtla/AutoGluon)
      → `pyproject.toml` + `uv.lock`, `du-lieu.toml`, `chuan-bi.sh`, bản sao `lay_du_lieu.py`, `tv/` (cài editable,
      `import tv` chạy mọi nơi), `.dau-van-tay.json`. Một buổi / dải / `--tat-ca`; `--kiem` báo nền lệch nguồn; `--nang-cap`
- [x] **`tools/lay_du_lieu.py`** — chỉ thư viện chuẩn; nguồn `http` (mirror trước), `hf` (commit 40 ký tự), `kaggle`
      (kagglehub, 401/403 → hướng dẫn + bộ dự phòng), `eia` (phân trang, CSV chuẩn hoá), `openaq`; cache theo sha256,
      hardlink vào `lab/du-lieu/raw/` chỉ đọc + `NGUON.txt`; `.env`; `--tom-tat`, `--tac-gia` (in sha256 bộ mới).
      Đã chạy thật: UCI, HF, EIA (`DEMO_KEY`, sha ổn định 2 lần), lỗi sha/thiếu key/Kaggle chưa đăng nhập.
      OpenAQ chưa chạy thật (cần key) — kiểm ở Phase 1
- [x] **`tools/kiem_tra_doc_lap.sh`** — K1–K10: tham chiếu chéo, dùng tools/, nền lệch nguồn + `uv lock --check`,
      dữ liệu thiếu sha256/giấy phép, đường dẫn tuyệt đối, model thiếu revision/`latest`, `pip install`, code trỏ
      dap-an, git theo dõi dữ liệu/notebook, workspace ở gốc. Phân tích Python bằng AST; đã thử cài từng vi phạm
- [x] `tools/kiem_tra_lab.py` — down → up → check `BAI=dap-an` (phải xanh) → check `BAI=code` (phải đỏ vì test hỏng) →
      down; bảng + thời gian, cảnh báo > 10 phút; `--may-trang` (cache uv + dữ liệu tạm), nhật ký `tools/nhat-ky-lab/`
- [x] `tools/dong_goi.py` — zip tất định; loại `dap-an/`, `loi-giai-mau/`, `ngay-du-lieu-hong/`, `ghi-am-dap-an/`, **`giam-khao/`**
      (quy ước: mọi thứ giám khảo giữ đặt trong thư mục này), `NGHIEN-CUU.md`, `tai-lieu.md`, `kiem-tra.md`; quét lại zip sau khi ghi
- [x] **Phụ lục A–E** + PDF (A 7, B 5, C 7, D 7, E 9 trang) — mọi ví dụ/con số chạy thật. C và D là bản khởi đầu:
      Phase 3 thêm hình cho C, Phase 5/8 thêm ví dụ dữ liệu thật cho D. **Phụ lục F** làm cùng Phase 1
- [x] Khuôn buổi `tools/khuon-buoi/` — `tai-lieu.md` 9 mục có chú thích, `kiem-tra.md`, `NGHIEN-CUU.md`, `code/README.md`,
      `dap-an/README.md`, `lab/nen.toml`, `lab/Makefile` (make 3.81; up/check/notebook/down; `BAI=`), `lab/cham/conftest.py`
- [x] **Chạy thử** buổi giả `buoi-00-thu` (UCI Bike Sharing): sinh nền → `make up` (sha256 khớp) → check code ĐỎ đúng /
      dap-an XANH → down; copy riêng thư mục ra ngoài repo + cache trắng vẫn chạy; `kiem_tra_lab --may-trang` ĐẠT;
      zip không lọt tệp nội bộ, 2 lần đóng gói cùng sha256. Đã xoá buổi giả
- [ ] Tạo remote GitHub và push lần đầu

### Prompt copy-paste cho Phase 0:
```
Khoá Forecasting in AI 44 buổi | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Lộ trình nguồn: lo-trinh/lo-trinh-forecasting.md

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md (phase này: tools/NGHIEN-CUU.md): ngày research, nguồn
   (URL + ngày truy cập), phiên bản đã xác minh, phát hiện mới, điểm lệch so với lộ trình.
5. Lệch lớn → cập nhật lo-trinh + todos TRƯỚC, báo lại người dùng, rồi mới làm.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng cho phase này: uv (lock, workspace, --frozen), jupytext, ruff, cách tải dữ liệu
Kaggle/Hugging Face/EIA/OpenAQ bằng script, cách mirror dữ liệu CC BY lên Hugging Face Datasets.

Làm nốt Phase 0 — Hạ tầng: MOI-TRUONG.md, pyproject.toml gốc (ruff, jupytext), tools/sinh_nen.py,
tools/lay_du_lieu.py, tools/kiem_tra_doc_lap.sh, tools/kiem_tra_lab.py, tools/dong_goi.py,
tools/khuon-buoi/, phu-luc/A..E (theo mục "Quy ước" trong todos.md).
tools/xuat_pdf.py ĐÃ CÓ, đừng viết lại — chỉ sửa nếu thiếu.
QUAN TRỌNG: sinh_nen.py, lay_du_lieu.py và kiem_tra_doc_lap.sh là cơ chế giữ cho các buổi độc
lập — làm kỹ, mọi phase sau đều dựa vào. Chưa viết tài liệu buổi nào.
Xong thì chạy thử: sinh nền cho một buổi giả buoi-00-thu/ với 1 dataset UCI nhỏ, make up →
dữ liệu qua sha256 → make down, rồi xoá buoi-00-thu/. Phụ lục xuất PDF bằng tools/xuat_pdf.py.
```

---

## Phase 1 — Khung trợ giúp và danh mục dữ liệu ✅
Mọi buổi đều copy khung này vào `tv/` và đều tải dữ liệu qua danh mục này. Sai ở đây là sửa 44 lần.

- [x] **Research Phase 1** — `tools/du-lieu/NGHIEN-CUU.md` (2026-09-17): giấy phép trích nguyên văn ~30 nguồn, công thức
      M5/CRPS/WIS/DM-HLN, backtest, rò rỉ, PIT/CORP. **Lệch lớn đã sửa lộ trình + todos:** FRED cấm dùng cho ML → lấy từ
      BLS/BEA/Fed Board/EIA + Philadelphia Fed (vintage); NOAA ISD Nội Bài dừng + WMO Res 40 → GHCNh; METR-LA không giấy
      phép → Monash Traffic; UCI 321 quá chậm → Monash electricity hourly; Tourism Australia = tsibble GPL-3
- [x] `tools/khung/ve.py` — `bo_bieu_do_chan_doan()` (8 biểu đồ, tự nhận dữ liệu giờ/ngày/tháng), fan chart, PIT histogram
      (không ngẫu nhiên cho dữ liệu đếm — Czado et al. 2009), reliability diagram CORP (PAV) + kiểu bin, small multiples
- [x] `tools/khung/danh_gia.py` — MAE, RMSE, ME, MAPE, sMAPE, WAPE, MASE, RMSSE (+ M5 từ lần bán đầu), WRMSSE, pinball,
      Winkler, coverage, WIS (2 dạng), CRPS mẫu (nrg/fair) + đóng cho chuẩn, Brier + phân rã Murphy, log score, PIT mẫu,
      `bang_chi_so` nhiều chuỗi. **Đối chiếu số khớp utilsforecast 0.2.16 và scoringrules 0.11.0** (ghi rõ khác biệt quy ước)
- [x] `tools/khung/backtest.py` — rolling origin có `gap`, sliding/expanding, `refit` True/False/k (như statsforecast), bảng
      dài có `cutoff`, `buoc_h`; chặn dự báo thừa/thiếu dòng; `diebold_mariano` bản HLN, lùi về h=1 khi phương sai âm (như R)
- [x] **`tools/khung/ro_ri.py`** — `kiem_ro_ri`: cắt tương lai + **nhiễu mục tiêu theo tầm h** (bắt rolling không shift, lag < h);
      `kiem_chia_tap`, `kiem_scaler`, `kiem_chong_lan`. **11 ca phải bắt + 11 ca phải cho qua** + test kiểm phụ
- [x] `tools/khung/du_lieu.py` — `doc_du_lieu(ten)` dạng dài (đọc .tsf Monash, hoặc khai `dang_dai` trong danh mục), `doc_tho`
- [x] `tools/kiem_khung.py` — test khung ở 2 hồ sơ: pandas 3.0.5 (65 đạt, 3 bỏ qua) và pandas 2.3.3 + Nixtla (68 đạt)
- [x] `lab/nen.toml` thêm `khung_bo` — buổi dạy tự viết công cụ không nhận lời giải trong `tv/`
- [x] **`tools/du-lieu/danh-muc.toml`** — 56 bộ (**55 đã chốt sha256**; chỉ còn `m5-kaggle` chờ chấp nhận luật Kaggle) +
      8 nguồn ghi rõ KHÔNG tải tự động (FRED, OpenAQ VN, ISD, BTS, METR-LA, Dominick's, Metaculus, fev/GIFT-Eval)
- [x] **Rà giấy phép từng bộ** — trích nguyên văn trong NGHIEN-CUU.md mục B và trường `trich_giay_phep`
- [x] **Mirror** bộ được phép lên Hugging Face Datasets — **XONG 2026-09-18**: `Tony2202/khoa-forecasting-du-lieu`
      (công khai), commit `105db7d8d51c8ff1229ec06c363f641417124bf3`, **49 bộ / 614 MB**, tệp giữ nguyên byte, thẻ dữ liệu
      ghi giấy phép + nguồn + sha256 từng bộ. 49 dòng `url_mirror` đã vào `danh-muc.toml`; `lay_du_lieu.py` thử mirror trước.
      Kiểm trên cache trắng: 4/4 bộ khớp sha256 (Online Retail II 18,4 s qua mirror thay vì ~5 giờ từ UCI).
      Lần đẩy thứ hai (commit `829f0fab55a5fb5a0b483976d60c402efb2e355a`) thêm `uci-electricity-load`:
      đã tải đủ 261.335.609 byte từ UCI và **chốt sha256** — bộ cuối cùng còn treo từ Phase 1
- [x] Bộ dự phòng mở cho mọi bộ bị hạn chế (M5 → Online Retail II / Car Parts; METR-LA → Traffic hourly; ISD → GHCNh;
      OpenAQ VN → UCI Beijing + Open-Meteo Hà Nội; Metaculus → ForecastBench; Dominick's → Online Retail II)
- [x] `phu-luc/F-nguon-du-lieu.md` sinh từ danh mục (`tools/du-lieu/sinh_phu_luc_f.py`) + PDF
- [ ] Còn cho phase sau: công cụ trích bảng BTS (Phase 4/5); bộ con fev-bench (Phase 10).
      **Đã giải quyết:** Census bán lẻ + BLS thất nghiệp (Phase 3, đã vào danh mục); OpenAQ VN → BỎ (v3 bắt buộc key cho
      mọi endpoint, v2 HTTP 410 — Phase 4 thay bằng GHCNh Nội Bài + Open-Meteo).
      **Còn chặn:** M5 — tài khoản Kaggle `thanh14` đã có key nhưng **chưa chấp nhận luật cuộc thi**
      (`403` từ kagglehub 2026-09-18); cần bấm Join tại kaggle.com/competitions/m5-forecasting-accuracy/rules rồi chạy
      `tools/lay_du_lieu.py` cho buổi 23 để chốt sha256
- [x] **Test: tải toàn bộ danh mục trên cache trắng (`tai_danh_muc.py --may-trang`) — 46/46 bộ đã chốt khớp sha256 (100%)**;
      tải về 666 MB (đặt vào lab ~1,29 GB sau giải nén); nhóm thường 18,2 phút, nhóm UCI 3,5 phút (lần chạy trước UCI
      đứt kết nối giữa chừng → thêm thử lại khi đang truyền). Bỏ qua đúng 2 bộ `cho_sha256`

### Prompt copy-paste cho Phase 1:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 0: XONG. Làm Phase 1 — khung trợ giúp tools/khung/ và danh mục dữ liệu.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến.
4. Ghi vào tools/du-lieu/NGHIEN-CUU.md: ngày, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình.
5. Lệch lớn → cập nhật lo-trinh + todos TRƯỚC, báo lại người dùng, rồi mới làm.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng cho phase này: GIẤY PHÉP của TỪNG bộ dữ liệu trong lộ trình — mở trang giấy
phép gốc, trích nguyên văn điều khoản phân phối lại vào NGHIEN-CUU.md. Công thức chuẩn của
MASE/RMSSE/WRMSSE (M5 guide), CRPS, WIS (Bracher et al.), Diebold–Mariano bản hiệu chỉnh mẫu nhỏ.

Bắt buộc: ro_ri.py có test cho cả ca phải bắt lẫn ca phải cho qua; danh_gia.py đối chiếu số
với thư viện chuẩn; mọi bộ dữ liệu có giấy phép đã xác minh và bộ dự phòng mở nếu bị hạn chế.
Bộ nào cấm phân phối lại thì KHÔNG mirror. Xong: tải toàn bộ danh mục trên venv trắng, sha256 khớp 100%.
```

---

## Phase 2 — Buổi 1–3 · Nền móng ✅

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 01 Forecasting là gì | ✅ | ✅ 3.972 chữ | ✅ 4/8 | ✅ 8/8 | ✅ | ✅ 10 trang |
| 02 Xác suất & thống kê | ✅ | ✅ 3.872 chữ | ✅ 3/8 | ✅ 8/8 | ✅ | ✅ 10 trang |
| 03 Dữ liệu thời gian | ✅ | ✅ ~3.725 chữ | ✅ 1/11 | ✅ 11/11 | ✅ | ✅ 10 trang |

Cột "Code" là điểm `make check` của `code/` — phải THẤP (chỗ hở còn nguyên);
cột "Lab" là điểm của `dap-an/` — phải tuyệt đối.

Bắt buộc:
- Buổi 1: phiếu bài toán dự báo 6 ô dùng lại được; bảng bài học M1–M6; demo đánh giá trên dữ liệu huấn luyện cho sai số ảo
  (*Phase 2 đo trên UCI 235 theo giờ, 46 gốc tuần 2010:* bảng lịch khớp cả dữ liệu MAE 0,380 → trung thực 0,508, thua
  TB 4 tuần 0,490; ở tổng tuần thứ hạng đảo — bảng lịch 16,4 vs TB 4 tuần 27,9 kWh. Bốn kết luận "đơn giản ≥ phức tạp…" là của M1,
  M3 xác nhận)
- Buổi 2: tự viết quantile + bootstrap + block bootstrap bằng NumPy; đo tỷ lệ phủ thật của "±1.96σ"
  (*Phase 2 đo trên Bike Sharing:* khoảng theo từng giờ dựng từ 2011 phủ 72,5% trên 2012 — do dịch chuyển mức, quantile
  thực nghiệm cũng chỉ 70,1%; trong mẫu 2011 phủ 96,4% nhưng đuôi lệch 0,3%/3,3%. Đã sửa "Xong khi" của lộ trình: quantile
  sửa hình dạng, block bootstrap sửa khoảng tin cậy của trung bình — hai vấn đề khác nhau)
- Buổi 3: bấm giờ pandas vs polars vs DuckDB trên cùng dữ liệu; test DST, trùng lặp, lệch múi giờ; **Cột mốc M0**

### Prompt copy-paste cho Phase 2:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 1: XONG. Làm Phase 2 — buổi 01, 02, 03 (lộ trình "Giai đoạn 0").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: bài tổng quan M-competitions (Makridakis et al., M4/M5/M6 findings), FPP chương
1 và 5, pandas 3.x thay đổi về datetime/copy-on-write, polars và DuckDB bản mới nhất.
Lưu ý (Phase 0): hệ Nixtla chưa hỗ trợ pandas 3 → buổi 14+ dùng pandas 2.3.3 (tools/nen/phien-ban.toml
[[rang_buoc]]); buổi 3 phải dạy code chạy được trên CẢ HAI bản, chỉ rõ chỗ khác (Phụ lục A).

Mỗi buổi: NGHIEN-CUU.md + tai-lieu.md đủ 9 mục (có "Trạng thái đầu buổi") + code/ có chỗ hở cố ý
(bảng trong todos.md) + dap-an/ + lab/00-nen/ (sinh bằng tools/sinh_nen.py) + lab/cham/ +
lab/Makefile + kiem-tra.md 10 câu. Buổi phải TỰ CHỨA: không tham chiếu ../buoi-NN/.
CHẠY THẬT mọi lệnh và lấy mọi con số từ output thật trước khi viết vào tài liệu.
Cuối cùng: tools/kiem_tra_doc_lap.sh → python tools/xuat_pdf.py 1 2 3 → --kiem (10–16 trang).
```

---

## Phase 3 — Buổi 4–8 · Đọc dữ liệu: biểu đồ, biến đổi, phân rã, tương quan ✅
**Phase trọng tâm của khoá** (người dùng yêu cầu: hiểu sâu, đọc biểu đồ, phân tích tương quan).

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 04 Đọc & vẽ biểu đồ | ✅ | ✅ 3.261 chữ | ✅ 1/8 | ✅ 8/8 | ✅ | ✅ 12 trang |
| 05 Biến đổi & điều chỉnh | ✅ | ✅ 3.135 chữ | ✅ 3/8 | ✅ 8/8 | ✅ | ✅ 10 trang |
| 06 Phân rã | ✅ | ✅ 3.090 chữ | ✅ 2/7 | ✅ 7/7 | ✅ | ✅ 11 trang |
| 07 Tự tương quan & tính dừng | ✅ | ✅ 3.194 chữ | ✅ 4/9 | ✅ 9/9 | ✅ | ✅ 10 trang |
| 08 Tương quan giữa các chuỗi | ✅ | ✅ 3.814 chữ | ✅ 7/10 | ✅ 10/10 | ✅ | ✅ 10 trang |

Phụ lục C đã cập nhật từ nội dung buổi 4–8 (thêm mục Heatmap lịch, Boxplot theo mùa, CCF, Tương quan trượt;
mỗi mục có "Ví dụ có số" từ dữ liệu thật) — 9 trang.

Bắt buộc:
- Buổi 4: bộ 8 biểu đồ chẩn đoán thành hàm dùng lại; một biểu đồ "gây hiểu nhầm" vẽ lại trung thực;
  **mỗi loại biểu đồ có ví dụ đọc đúng và ví dụ đọc sai** (đồng thời là nội dung Phụ lục C)
- Buổi 5: đo bằng số bias khi log–exp không hiệu chỉnh; tự viết Box-Cox
- Buổi 6: classical decomposition hỏng trên mùa vụ kép — thấy trên hình phần dư; MSTL sửa; tính $F_T, F_S$
- Buổi 7: bảng 4×4 (4 chuỗi mô phỏng × ACF/PACF/ADF/KPSS); giải thích khi ADF và KPSS mâu thuẫn
- Buổi 8: **đủ 5 tình huống**: tương quan giả hai chuỗi xu hướng; quan hệ chữ U (Pearson thấp, MI cao);
  CCF trước/sau prewhitening; tương quan trượt đổi dấu theo mùa; Granger "có ý nghĩa" nhưng không nhân quả

*Research Phase 3 (2026-09-18) — điểm lệch đã sửa vào lộ trình:*
- Buổi 5: Census MARTS lấy qua bản lưu Wayback chốt sha256 (census.gov chặn 403 từ Việt Nam; API cần key)
- Buổi 6: phân rã cổ điển chu kỳ 24 — nhịp tuần vào xu hướng, phần dư mang mẫu hình tháng×giờ (không phải "mùa vụ tuần
  rơi hết vào phần dư"); robust minh hoạ bằng giờ hỏng 21/11/2024 thay đợt nắng nóng
- Buổi 7: thay tỷ lệ thất nghiệp BLS bằng sản lượng công nghiệp FRB G.17 (BLS không có tệp nhỏ)
- Buổi 8: cặp chuỗi xu hướng = CPI-U × dân số; ERCOT + Open-Meteo Dallas/Houston 2024 (thêm danh mục);
  `ccf(x, y)` của statsmodels chỉ trả corr(x_{t+k}, y_t), k ≥ 0 — muốn "x dẫn y" gọi `ccf(y, x)`

### Prompt copy-paste cho Phase 3:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 2: XONG. Làm Phase 3 — buổi 04..08 (lộ trình "Giai đoạn 1", nửa đầu).

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
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

## Phase 4 — Buổi 9–13 · Chuẩn bị dữ liệu + dự án giữa chặng 1 🔲
**Phase trọng tâm thứ hai**: làm sạch, ngoại lai, khử nhiễu, feature, chống rò rỉ.

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 09 Đặc trưng & khả năng dự báo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 10 Làm sạch & dữ liệu thiếu | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 11 Ngoại lai & điểm gãy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 12 Khử nhiễu & miền tần số | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 13 Feature & chống rò rỉ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| Dự án giữa chặng 1 | 🔲 | đề 🔲 | lỗi cài sẵn 🔲 | bộ chấm 🔲 | rubric 🔲 | 🔲 |

Bắt buộc:
- Buổi 9: spectral entropy vs MASE seasonal naive có số tương quan thật; phân cụm DTW; ABC–XYZ
- Buổi 10: **dữ liệu Việt Nam thật** (OpenAQ Hà Nội/TP.HCM) có đổi đơn vị/trạm đứng yên; so 6 phương
  pháp điền trên **lỗ ngắn và lỗ dài** bằng che nhân tạo; ≥ 8 test cho `lam_sach.py`; cột cờ
- Buổi 11: 3 cách xử lý COVID ra 3 kết quả dự báo; Hampel vs z-score; PELT có chọn penalty
- Buổi 12: aliasing dựng thật; bảng 6 bộ lọc có cột "dùng tương lai?"; **test tự động bắt bộ lọc
  không nhân quả**; ví dụ khử nhiễu target làm đánh giá sai
- Buổi 13: `kiem_ro_ri` bắt đủ 4 feature rò cài sẵn; **feature Tết âm lịch đúng mọi năm 2000–2035**
  (test đối chiếu bảng ngày Tết); đo "cái giá của rò rỉ" thời tiết thật vs thời tiết dự báo
- Dự án giữa chặng 1: 6 lỗi cài sẵn (giám khảo giữ, **không vào zip**); bộ chấm tự động phần phát hiện lỗi;
  rubric 100 điểm. **Cột mốc M1**

*Research Phase 4 (2026-09-18) — điểm lệch đã sửa vào lộ trình:*
- Buổi 9: entropy × **MASE**(snaive) ≈ 0 (ρ = −0,03) vì MASE tự chuẩn hoá → đổi sang **sMAPE** (ρ = +0,33);
  MASE và việc đổi thang chuẩn hoá (đảo dấu, ρ = −0,52) thành chỗ hở/bài học. catch22 lọc từ **4.791** đặc trưng
  (không phải 7.658). Đặc trưng tự viết bằng NumPy; `tsfeatures` (Nixtla) đóng băng từ 2023 — chỉ nhắc
- Buổi 10: **OpenAQ v3 đòi API key cho mọi endpoint** (401), v2 đã ngừng (410) → thay bằng **GHCNh Nội Bài**
  (dữ liệu Việt Nam thật, CC0 đã xác minh) + Open-Meteo Hà Nội + Beijing; PyPOTS chỉ dạy lý thuyết
- Buổi 11: US BTS không tải được → **Eurostat avia_paoc** (đã thêm danh mục, CC BY 4.0, sha ổn định);
  "3σ xoá Tết rồi sửa bằng STL robust" **không chạy được** (Tết âm lịch) → đổi thành phản ví dụ + biến giả lịch âm;
  Hampel demo chuyển sang tổng lượt xem vi.wikipedia
- Buổi 12: Savitzky–Golay/wavelet có rò rỉ nhưng lợi ích giả nhỏ — sửa câu chữ lab 4; thêm Kalman filter
  (trễ 0 nhưng vẫn nhân quả) vào bảng so sánh
- GHCNh Nội Bài 2024/2025: đổi `mirror = false → true` (metadata NOAA ghi CC0-1.0, tài liệu không có WMO Res 40)

### Prompt copy-paste cho Phase 4:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 3: XONG. Làm Phase 4 — buổi 09..13 + du-an-giua-chang/01-eda-lam-sach/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
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

## Phase 5 — Buổi 14–17 · Đánh giá, backtest, ETS, ARIMA 🔲

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 14 Baseline & chỉ số | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 15 Backtesting | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 16 ETS & Theta | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 17 ARIMA | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 14: tự viết 7 chỉ số, đối chiếu utilsforecast; bảng xếp hạng đảo lộn khi đổi chỉ số; viết `phu-luc/D-cong-thuc-chi-so.md`
- Buổi 15: đo khoảng lạc quan của CV ngẫu nhiên so với hold-out cuối; Diebold–Mariano; ba tập tune/chọn/báo cáo
- Buổi 16: tự viết SES + Holt tối ưu bằng scipy; kiểm coverage thật của khoảng ETS
- Buổi 17: tự xác định bậc từ ACF/PACF và so AICc với auto-ARIMA; Ljung-Box phần dư

### Prompt copy-paste cho Phase 5:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 4: XONG. Làm Phase 5 — buổi 14..17 (lộ trình "Giai đoạn 2", nửa đầu).

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: FPP chương 5, 8, 9; Hyndman & Koehler 2006 (MASE); M5 guide (RMSSE/WRMSSE);
Bergmeir & Benítez về CV cho chuỗi thời gian; Diebold–Mariano bản Harvey hiệu chỉnh;
statsforecast bản mới nhất (AutoETS, AutoTheta, AutoARIMA, cross_validation).

Buổi 15 tạo ra bộ backtest mà cả khoá dùng — thiết kế cẩn thận, có test. Mọi mô hình phải so với
seasonal naive có kiểm định ý nghĩa. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.
```

---

## Phase 6 — Buổi 18–21 · Hồi quy động, gián đoạn, đa biến, tài chính 🔲

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 18 Hồi quy động | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 19 Nhu cầu gián đoạn | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 20 Đa biến & nowcasting | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 21 Tài chính & biến động | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 18: hồi quy giả có p-value "đẹp" rồi sửa bằng hồi quy động; so 4 cách đa mùa vụ; Prophet có/không Tết
- Buổi 19: chấm bằng **cả RMSSE lẫn chi phí tồn kho mô phỏng**, chỉ ra hai thước đo chọn khác nhau
- Buổi 20: tự viết Kalman filter; nowcast GDP **bằng vintage thật** (Philadelphia Fed Real-Time Data Set — không dùng ALFRED, xem Phụ lục F)
- Buổi 21: mổ xẻ demo "LSTM đoán giá 99%"; GARCH + HAR; VaR backtest Kupiec. **Cột mốc M2**

### Prompt copy-paste cho Phase 6:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 5: XONG. Làm Phase 6 — buổi 18..21 (lộ trình "Giai đoạn 2", nửa sau).

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: FPP chương 7, 10, 12; Syntetos–Boylan classification, TSB (Teunter et al.);
nowcasting với dynamic factor / MIDAS (tổng quan mới), Philadelphia Fed RTDSM (KHÔNG dùng ALFRED/FRED); tình trạng Prophet (còn bảo
trì không); arch package bản mới, HAR-RV, Markov switching trong statsmodels; các phân tích
phản biện "deep learning dự báo giá cổ phiếu".

Buổi 19 chấm bằng chi phí tồn kho, không chỉ chỉ số thống kê. Buổi 20 dùng vintage thật — dùng số
liệu đã sửa là rò rỉ. Buổi 21 phải trung thực: dự báo giá gần như không thắng naive, nói rõ.
Cuối buổi 21 đạt cột mốc M2. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.
```

---

## Phase 7 — Buổi 22–24 · Machine learning + dự án giữa chặng 2 🔲

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 22 Dự báo thành hồi quy | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 23 Gradient boosting | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 24 Ensemble & AutoML | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Dự án giữa chặng 2 | 🔲 | đề 🔲 | bộ lấy dữ liệu tương lai 🔲 | bộ chấm 🔲 | leaderboard 🔲 | 🔲 |

Bắt buộc:
- Buổi 22: test bắt lag < horizon trong chiến lược direct; sai số theo h của recursive/direct/MIMO; cây không ngoại suy xu hướng
- Buổi 23: Tweedie vs L2 trên WRMSSE; Optuna CV thời gian vs KFold ngẫu nhiên; SHAP cho **một dự báo cụ thể**; monotone constraint cho giá
- Buổi 24: đo khoảng lạc quan khi chọn mô hình trên tập báo cáo; AutoGluon có time limit; cold start bằng analog
- Dự án giữa chặng 2: **chấm trên dữ liệu EIA-930 chưa tồn tại lúc nộp**; so với dự báo day-ahead của đơn vị
  điều độ; script tự lấy dữ liệu thật và chấm; rubric đo cả "khoảng cách backtest vs thực tế". **Cột mốc M3**

### Prompt copy-paste cho Phase 7:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 6: XONG. Làm Phase 7 — buổi 22..24 + du-an-giua-chang/02-thi-du-bao/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: global vs local models (Montero-Manso & Hyndman); chiến lược đa bước (Taieb et al.);
lời giải top M5 và bài tổng kết M5 accuracy; mlforecast + LightGBM bản mới; AutoGluon-TimeSeries
bản mới nhất (preset, model zoo); forecast combination puzzle; FFORMA; cold start forecasting;
EIA-930 API v2 (endpoint, trường day-ahead forecast, độ trễ công bố, sửa số liệu lùi).

Dự án giữa chặng 2 phải chấm trên dữ liệu TƯƠNG LAI THẬT (chưa tồn tại lúc nộp) và so với dự báo
day-ahead mà đơn vị điều độ công bố trong EIA-930. Viết script lấy dữ liệu + chấm tự động +
leaderboard. Thời tiết dùng làm feature phải là thời tiết DỰ BÁO lưu trữ, bộ chấm kiểm điều này.
Cuối buổi 24 đạt cột mốc M3.
```

---

## Phase 8 — Buổi 25–28 · Bất định 🔲

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 25 Dự báo xác suất | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 26 Conformal | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 27 Bayes & GP | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 28 Dự báo phân cấp | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 25: tự viết pinball, CRPS từ mẫu, WIS; PIT + reliability diagram của 3 mô hình có lỗi calibration khác nhau; peaks-over-threshold
- Buổi 26: coverage trượt theo thời gian của split / CQR / EnbPI / ACI trên dữ liệu có drift thật
- Buổi 27: prior predictive check sửa prior; no/complete/partial pooling; **chẩn đoán r_hat, ESS, divergence bắt buộc trong `cham/`**
- Buổi 28: tổng khớp tuyệt đối mọi cấp; MinT vs bottom-up/top-down từng cấp; reconciliation xác suất. **Cột mốc M4**

### Prompt copy-paste cho Phase 8:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 7: XONG. Làm Phase 8 — buổi 25..28 (lộ trình "Giai đoạn 4 — Bất định").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: Gneiting & Raftery (proper scoring rules), Gneiting calibration/sharpness; WIS
(Bracher et al. 2021); conformal cho chuỗi thời gian — ACI (Gibbs & Candès), EnbPI, các bài
benchmark 2026 và MAPIE bản mới nhất; pymc + pymc-extras statespace bản mới; GP kernel cho chuỗi
thời gian; FPP chương 11, MinT (Wickramasuriya et al.), probabilistic reconciliation mới nhất,
hierarchicalforecast bản mới; giấy phép bộ Tourism Australia.

Mọi dự báo từ phase này trở đi phải có khoảng đã kiểm calibration. Buổi 27 không dùng posterior
chưa qua chẩn đoán hội tụ. Cuối buổi 28 đạt cột mốc M4. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.
```

---

## Phase 9 — Buổi 29–33 · Deep learning 🔲
Phase nặng tài nguyên: 16 GB RAM, CPU chạy được nhưng chậm. Chuẩn bị cấu hình rút gọn cho máy 8 GB.

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 29 Nền DL | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 30 N-BEATS … TiDE | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 31 Transformer | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 32 Mô hình sinh | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 33 Không gian–thời gian & thời tiết AI | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 29: test "không chồng lấn cửa sổ"; tự viết MLP/LSTM/TCN huấn luyện < 10 phút CPU; **bảng so baseline kể cả khi DL thua**
- Buổi 30: cấu hình có covariate khai sai loại để học viên tìm; đo "cái giá rò rỉ" của `futr_exog`
- Buổi 31: tái hiện DLinear vs PatchTST vs iTransformer; chứng minh `drop_last` và thiếu baseline làm đổi thứ hạng; checklist đọc paper 10 câu
- Buổi 32: đánh giá dữ liệu tổng hợp đủ fidelity / utility (TSTR) / memorization; energy score
- Buổi 33: **kiểm chứng AIFS mở tại trạm Nội Bài chỉ trên thời gian sau mốc huấn luyện**; MOS giảm sai số hệ thống;
  GNN nhỏ chạy CPU. **Cột mốc M5**

### Prompt copy-paste cho Phase 9:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 8: XONG. Làm Phase 9 — buổi 29..33 (lộ trình "Giai đoạn 5 — Deep learning").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: FPP chương 14; neuralforecast + PyTorch bản mới; bài gốc N-BEATS, N-HiTS, DeepAR,
TFT, TiDE, PatchTST, iTransformer, TSMixer, DLinear ("Are Transformers Effective...") và các bài
phản biện benchmark/`drop_last` gần nhất; kiến trúc SOTA mới ra trong 12 tháng (có thể phải thay
một kiến trúc trong buổi 30/31); TimeGrad, CSDI và diffusion cho dự báo; đánh giá dữ liệu tổng
hợp chuỗi thời gian; ECMWF Open Data AIFS (định dạng, biến, giấy phép, cách tải điểm), NOAA ISD
trạm Nội Bài, WeatherBench 2; PyTorch Geometric Temporal / GNN cho METR-LA chạy CPU.

Mọi lab phải chạy trên CPU trong thời gian hợp lý (ghi rõ phút), có cấu hình rút gọn cho máy 8 GB.
Mọi bảng so sánh phải có seasonal naive + một mô hình thống kê + LightGBM — kể cả khi DL thua.
Model/checkpoint chốt revision. Cuối buổi 33 đạt cột mốc M5.
```

---

## Phase 10 — Buổi 34–37 · Foundation model và LLM 🔲
Hệ sinh thái đổi nhanh nhất khoá — **research của phase này quan trọng nhất**.

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 34 Foundation model | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 35 Fine-tune & benchmark | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 36 LLM & agent | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 37 Dự báo sự kiện bằng LLM | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 34: so zero-shot **chỉ trên dữ liệu sau ngày phát hành model**; đo thời gian + RAM trên CPU; context length
- Buổi 35: ít nhất một ca foundation model **thua** LightGBM, giải thích; tính lại xếp hạng benchmark chỉ trên task sạch rò rỉ; conformal hoá quantile
- Buổi 36: test tự động "không bịa số" (mọi con số trong báo cáo LLM có trong output công cụ); agent không được tự chọn tập test;
  **bản ghi phản hồi LLM** để chấm không cần API key; nhánh model mở chạy local
- Buổi 37: Brier score **chỉ trên câu hỏi resolve sau mốc cắt kiến thức**, đo "khoảng rò rỉ"; học viên tự dự báo
  và chấm calibration của chính mình; so với baseline thị trường. **Cột mốc M6**

### Prompt copy-paste cho Phase 10:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 9: XONG. Làm Phase 10 — buổi 34..37 (lộ trình "Giai đoạn 6 — Foundation model và LLM").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
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
```

---

## Phase 11 — Buổi 38–40 · Nhân quả và ra quyết định 🔲

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 38 Tác động can thiệp | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 39 Kịch bản & what-if | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 40 Dự báo → quyết định | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 38: **dữ liệu mô phỏng có đáp án** kiểm phương pháp trước; placebo test theo thời gian và theo đơn vị; synthetic control Prop 99
- Buổi 39: mô phỏng confounding cho độ co giãn **sai dấu**, sửa bằng DoubleML về đúng ±0.2; DAG vẽ trong tài liệu
- Buổi 40: newsvendor 500 SKU báo **số tiền** tiết kiệm; FVA; một trang dashboard fan chart **thử với người không chuyên**

### Prompt copy-paste cho Phase 11:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 10: XONG. Làm Phase 11 — buổi 38..40 (lộ trình "Giai đoạn 7 — Nhân quả và ra quyết định").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: CausalImpact bản Python còn bảo trì (tfcausalimpact / causalimpact / PyMC-Marketing
/ CausalPy — chọn cái đang sống); synthetic control (Abadie) và synthetic DiD; DoubleML/EconML bản
mới; forecast value added (Gilliland); newsvendor + inventory policy với dự báo xác suất; FPP
chương 6 (judgmental); nghiên cứu về truyền đạt bất định cho người không chuyên (fan chart).

Mọi phương pháp nhân quả phải được kiểm trên dữ liệu mô phỏng có đáp án TRƯỚC khi áp lên dữ liệu
thật. Buổi 40 phải quy ra tiền. Chạy thật mọi lab rồi mới tick ✅ và xuất PDF.
```

---

## Phase 12 — Buổi 41–43 · Production và MLOps 🔲

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 41 Pipeline tái lập | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 42 Phục vụ quy mô lớn | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 43 Giám sát & drift | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 41: chạy hai lần **giống từng byte**; pandera chặn đổi đơn vị; backfill không dùng dữ liệu sau ngày dự báo; kho dữ liệu as-of
- Buổi 42: đo thời gian vòng for → `n_jobs` → Ray, ghi con số; API p95 bằng `locust`; Docker
- Buổi 43: replay 1 năm với 4 sự cố cài sẵn, bắt trong ≤ 1 ngày, ≤ 2 cảnh báo giả/tháng; so 3 chính sách retrain; runbook. **Cột mốc M7**

### Prompt copy-paste cho Phase 12:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 11: XONG. Làm Phase 12 — buổi 41..43 (lộ trình "Giai đoạn 8 — Production và MLOps").

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: Prefect vs Dagster bản mới (chọn một, ghi lý do); pandera, MLflow, DVC bản mới;
point-in-time/feature store cho chuỗi thời gian; statsforecast/mlforecast phân tán (Ray, Spark,
Dask qua Fugue) còn hỗ trợ không; phục vụ foundation model trên CPU; drift detection cho chuỗi
thời gian (PSI, ADWIN, Page–Hinkley — river bản mới); bài học vận hành hệ thống dự báo lớn (Uber,
Amazon, Walmart…) công khai gần đây.

Buổi 41 phải tái lập từng byte. Buổi 43 dùng replay dữ liệu thật với sự cố cài sẵn, không mô phỏng
tay từng cảnh báo. Cuối buổi 43 đạt cột mốc M7.
```

---

## Phase 13 — Dự án cuối khoá 🔲

Đề: **hệ thống dự báo thực tế**, chọn 1 trong 3 (A bán lẻ + tồn kho, B tải điện xác suất, C PM2.5 Việt Nam
+ cảnh báo). Tiêu chí xịn, đo được: *chấm trên dữ liệu tương lai chưa tồn tại lúc nộp, pipeline chạy tự
động 2 tuần, giám sát bắt được sự cố do giám khảo tiêm vào mà học viên không biết trước.*

- [ ] `du-an-cuoi/de-bai.md` — 3 đề, 11 hạng mục bắt buộc + 4 điểm thưởng (lấy từ mục "Buổi 44" của lộ trình)
- [ ] `du-an-cuoi/rubric.md` — thang **100 + 20**, mô tả rõ "đạt khi" cho từng hạng mục, riêng cho từng đề
- [ ] `du-an-cuoi/phieu-bai-toan.md`, `mau-model-card.md`, `mau-adr.md` — khuôn cho học viên
- [ ] `du-an-cuoi/cham/` — bộ chấm tự động ~50/100: lấy dữ liệu tương lai thật (M5 dùng holdout giám khảo giữ,
      EIA-930 và OpenAQ lấy trực tiếp), tính sai số/calibration, kiểm dấu thời gian dự báo **trước** dữ liệu thật,
      chạy lại pipeline kiểm tái lập, `kiem_ro_ri`, chạy test của học viên, kiểm giám sát có bắt sự cố không
- [ ] `du-an-cuoi/ngay-du-lieu-hong/` — **giám khảo giữ, không vào zip**: 3 script tiêm sự cố vào nguồn dữ liệu
      mirror của lớp (dữ liệu trễ, đổi đơn vị, trạm chết) + tiêu chí "đã xử lý xong"
- [ ] `du-an-cuoi/cham/phieu-cham-tay.md` — EDA và lập luận, quyết định và giá trị, bảo vệ, model card, ADR
- [ ] `du-an-cuoi/loi-giai-mau/` — lời giải mẫu cho **đề B** đầy đủ; đề A, C ở mức khung
- [ ] Hạ tầng "nguồn dữ liệu của lớp": mirror cập nhật hằng ngày để giám khảo tiêm sự cố được mà không đụng nguồn gốc
- [ ] `du-an-cuoi/DU-AN-CUOI.pdf` — bản phát cho học viên (**không kèm lời giải mẫu, không kèm ngay-du-lieu-hong/**)
- [ ] Ghi rõ trong buổi 44: phát đề từ **sau buổi 24**; nhóm 2–3 người; lịch 2 tuần dự báo trực tiếp

### Prompt copy-paste cho Phase 13:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 12: XONG. Làm Phase 13 — du-an-cuoi/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến.
4. Ghi vào du-an-cuoi/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình.
5. Lệch lớn → cập nhật lo-trinh + todos TRƯỚC, báo lại người dùng, rồi mới làm.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: cách tổ chức các cuộc thi dự báo trực tiếp (M6, GEFCom, ForecastBench, VN
competitions nếu có); tình trạng hiện tại của EIA-930 API và OpenAQ (trạm Hà Nội/TP.HCM còn hoạt
động không, độ trễ dữ liệu); rubric chấm dự án ML thực tế; model card (Mitchell et al.) bản mới.

Đề và rubric lấy nguyên từ mục "Buổi 44 — Dự án cuối" của lo-trinh/lo-trinh-forecasting.md.
Bộ chấm tự động ~50/100. Lời giải mẫu và ngay-du-lieu-hong/ KHÔNG vào zip — kiểm dong_goi.py lọc đủ.
Hai hạng mục không được bỏ: chấm trên dữ liệu TƯƠNG LAI THẬT (dấu thời gian dự báo có trước dữ liệu)
và "ngày dữ liệu hỏng" do giám khảo giữ. Chạy thử toàn bộ bộ chấm với lời giải mẫu đề B trong 3 ngày
dự báo trực tiếp thật trước khi tick ✅. Đề phát học viên xuất PDF bằng tools/xuat_pdf.py.
```

---

## Phase 14 — Đánh giá 🔲

- [ ] `danh-gia/ngan-hang-cau-hoi.md` — gộp 440 câu quiz của 44 buổi, gắn nhãn mức (nhắc lại / vận dụng / đọc biểu đồ-chẩn đoán) và giai đoạn
- [ ] `danh-gia/kiem-tra-giua-khoa.md` — sau buổi 21, thực hành 90 phút: dữ liệu lạ → EDA → làm sạch → backtest → bậc thang thống kê; script chấm
- [ ] `danh-gia/kiem-tra-cuoi-khoa.md` — sau buổi 43, thực hành 120 phút: ML + dự báo xác suất + quyết định; script chấm
- [ ] `danh-gia/de-doc-bieu-do.md` — **30 biểu đồ thật, mỗi hình hỏi "đọc ra gì / sai ở đâu"** (trọng tâm người dùng yêu cầu)
- [ ] `danh-gia/de-tim-ro-ri.md` — 15 đoạn code, mỗi đoạn có 0–2 chỗ rò rỉ; chấm tự động bằng `kiem_ro_ri`
- [ ] `danh-gia/tu-luyen-du-bao-su-kien.md` — hướng dẫn luyện calibration trên Metaculus / Good Judgment Open
- [ ] Bảng đối chiếu: buổi ↔ chương FPP ↔ đề kiểm tra

### Prompt copy-paste cho Phase 14:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 13: XONG. Làm Phase 14 — danh-gia/.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến.
4. Ghi vào danh-gia/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phát hiện mới.
5. Lệch lớn → cập nhật lo-trinh + todos TRƯỚC, báo lại người dùng, rồi mới làm.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
Research riêng: rà lại 44 buổi xem nội dung nào đã lỗi thời kể từ lúc soạn (thư viện đổi API,
model mới) — liệt kê vào NGHIEN-CUU.md trước khi viết câu hỏi dựa trên nội dung đó; cách viết
câu hỏi đánh giá hiểu sâu (không chỉ nhớ); chứng chỉ/khung năng lực dự báo hiện có (IIF CPF…).

Gộp quiz 44 buổi thành ngân hàng câu hỏi; 2 đề thực hành có script chấm; đề đọc biểu đồ 30 hình
thật (hình sinh bằng script, lưu trong repo); đề tìm rò rỉ chấm tự động. Mọi câu hỏi phải trỏ về buổi dạy nó.
```

---

## Phase 15 — Xuất bản & đóng gói 🔲

- [ ] `python tools/xuat_pdf.py` — sinh đủ 44 PDF + trang lẻ; `--kiem` mọi buổi 10–16 trang; mở kiểm tra ngẫu
      nhiên 6 file (bảng, khối code, **công thức**, ảnh, tiếng Việt có dấu)
- [ ] `python tools/dong_goi.py` — `phat-de/buoi-NN.zip`; xác nhận **không** file nào chứa `dap-an/`, `NGHIEN-CUU.md`,
      `loi-giai-mau/`, `ngay-du-lieu-hong/`, lỗi cài sẵn của dự án giữa chặng
- [ ] Cập nhật `README.md` — bảng 44 buổi, bảng chỗ hở cố ý, **bảng "học theo cụm"**, cách dạy lẻ một buổi
- [ ] Cập nhật `CLAUDE.md` nếu quy ước đổi trong lúc soạn
- [ ] Push lên remote; cân nhắc GitHub Pages cho lộ trình; công bố bộ dữ liệu mirror trên Hugging Face kèm ghi nguồn
- [ ] Tổng hợp: số file, số trang PDF, dung lượng, tổng dung lượng dữ liệu tải — ghi vào Progress Summary

### Prompt copy-paste cho Phase 15:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 14: XONG. Làm Phase 15 — xuất bản: sinh 44 PDF, đóng gói phat-de/, cập nhật README.md và CLAUDE.md.

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. WebSearch + WebFetch: phiên bản mới nhất của MỌI thư viện chính và model đã chốt trong 44 buổi;
   dataset nào đổi URL/giấy phép; bảng xếp hạng GIFT-Eval/fev-bench/ForecastBench hiện tại.
2. Ghi vào NGHIEN-CUU-XUAT-BAN.md: bảng "đã chốt → mới nhất → có cần cập nhật buổi nào không".
3. Lệch lớn (thư viện đổi API làm hỏng lab, model mới vượt hẳn) → báo lại người dùng TRƯỚC khi
   xuất bản, đề xuất phase cập nhật; không tự ý sửa hàng loạt.
4. Cập nhật dòng "Rà soát gần nhất" trong lộ trình.

README phải có bảng "học theo cụm" — mỗi buổi tự chứa nên khoá cắt được nhiều cách.
Bắt buộc kiểm chứng: unzip thử 4 file trong phat-de/ (gồm buổi 13, 24, 44), xác nhận không lọt
dap-an/, NGHIEN-CUU.md, loi-giai-mau/, ngay-du-lieu-hong/.
```

---

## Phase 16 — Kiểm định chất lượng 🔲
Làm trên **máy trắng** hoặc container sạch, đóng vai học viên.

- [ ] `tools/kiem_tra_lab.py` chạy toàn bộ 44 buổi — mọi `make check` của `dap-an/` xanh, của `code/` đỏ đúng chỗ hở
- [ ] `tools/kiem_tra_doc_lap.sh` — 0 tham chiếu chéo, mọi buổi có `uv.lock` và dữ liệu có sha256
- [ ] **Bài kiểm tra độc lập thật:** chọn ngẫu nhiên 6 buổi (ít nhất 1 buổi mỗi giai đoạn 1, 4, 6), copy **chỉ**
      thư mục buổi đó sang máy trắng, chạy `make up && make check`. Hỏng buổi nào là buổi đó chưa tự chứa
- [ ] **Bài kiểm tra CPU-only:** buổi 29–35 trên máy không GPU, 16 GB RAM — ghi thời gian từng buổi; 8 GB với cấu hình rút gọn
- [ ] **Bài kiểm tra không API key trả phí:** buổi 36–37 chạy bằng model local + bản ghi phản hồi
- [ ] `ruff check` toàn repo — 0 lỗi
- [ ] Đọc lại 44 `tai-lieu.md`: mọi lệnh copy-paste được, **mọi con số trong tài liệu khớp output chạy lại** (sai lệch ngoài seed → sửa)
- [ ] Kiểm tra mạch **kiến thức**: buổi N có "Nhắc lại buổi trước" đủ, "Trạng thái đầu buổi" khớp `00-nen/`, dẫn sang buổi N+1
- [ ] Kiểm tra cột mốc M0–M7 đúng chỗ
- [ ] Kiểm tra `dap-an/` không rò vào `code/` hay vào zip
- [ ] Mọi `NGHIEN-CUU.md` có ngày; buổi nào research > 6 tháng (giai đoạn 5–6) hoặc > 12 tháng (còn lại) → đánh dấu cần rà
- [ ] Nhờ **một người ngoài** làm thử buổi 8, buổi 13, buổi 26 và dự án giữa chặng 1, ghi lại chỗ họ tắc

### Prompt copy-paste cho Phase 16:
```
Khoá Forecasting in AI | Working dir: /home/tony/Tony/Forecasting/ | Kế hoạch: todos.md
Phase 15: XONG. Làm Phase 16 — kiểm định: chạy tools/kiem_tra_lab.py cho cả 44 buổi trên venv
trắng, rà mạch kiến thức và các cột mốc M0–M7.

BƯỚC 0 — RESEARCH TRƯỚC KHI KIỂM (bắt buộc, không bỏ qua):
1. WebSearch + WebFetch: thư viện/model/dataset nào đã đổi kể từ ngày ghi trong từng NGHIEN-CUU.md.
2. Lập bảng "buổi có nguy cơ lỗi thời" trước khi chạy — để phân biệt lỗi do nội dung với lỗi do
   môi trường thay đổi.
3. Ghi vào KIEM-DINH.md cùng kết quả kiểm định.

BÀI QUAN TRỌNG NHẤT: copy ngẫu nhiên 6 thư mục buổi sang máy trắng, KHÔNG có phần còn lại của repo,
rồi chạy make up && make check. Thêm bài CPU-only (buổi 29–35) và bài không API key (buổi 36–37).
Báo cáo dạng bảng: buổi nào xanh, buổi nào hỏng, hỏng ở bước nào, thời gian chạy. Đừng sửa lấy
được — nêu rõ trước.
```

---

## General Copy-paste Prompt (dùng khi không nhớ đang ở phase nào):
```text
Khoá Forecasting in AI 44 buổi (cơ bản → nâng cao) | Working dir: /home/tony/Tony/Forecasting/
Lộ trình: lo-trinh/lo-trinh-forecasting.md
Kế hoạch & tiến độ: todos.md   ← đọc, tìm phase đầu tiên có 🔲, làm phase đó

BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua): chạy đúng "Giao thức research" trong
mục Quy ước của todos.md + phần "Research riêng" trong prompt của phase đó. Ghi NGHIEN-CUU.md có
nguồn và ngày. Lệch lớn so với lộ trình → cập nhật lộ trình + todos và báo lại TRƯỚC khi soạn.

Quy ước bắt buộc (mục "Quy ước" trong todos.md):
- Mỗi buổi TỰ CHỨA TUYỆT ĐỐI: buổi N không đọc một byte nào ngoài buoi-NN/ (trừ cache dữ liệu có
  sha256). Nền ở lab/00-nen/ sinh bằng tools/sinh_nen.py. Kiểm bằng tools/kiem_tra_doc_lap.sh
- tai-lieu.md đủ 9 mục (có "Trạng thái đầu buổi") + code/ (chỗ hở cố ý) + dap-an/ + lab/00-nen/
  + lab/cham/ + lab/Makefile + kiem-tra.md + NGHIEN-CUU.md
- Trọng tâm người dùng: tiền xử lý, khử nhiễu, hiểu sâu khái niệm, đọc biểu đồ, phân tích tương quan,
  dự án thực tế. Khái niệm theo nhịp: trực giác → hình → công thức → tự viết NumPy → thư viện
- Chỗ hở phổ biến nhất là RÒ RỈ TƯƠNG LAI và ĐÁNH GIÁ KHÔNG TRUNG THỰC; từ buổi 12 mọi lab có test rò rỉ
- MỌI lệnh và MỌI con số trong tài liệu phải lấy từ lần chạy thật
- Chốt phiên bản trong uv.lock; model chốt revision; không latest. Mọi lab chạy được bằng CPU
- Dữ liệu: mỗi bộ có giấy phép đã xác minh; cấm phân phối lại thì học viên tự tải, luôn có dự phòng mở
- dap-an/, NGHIEN-CUU.md, loi-giai-mau/, ngay-du-lieu-hong/ KHÔNG bao giờ vào zip phát học viên
- Xong buổi nào: ruff → kiem_tra_doc_lap → chạy lab trên venv trắng → xuất PDF (--kiem 10–16 trang) → tick ✅
```

---

## Progress Summary

| Phase | Nội dung | Deliverable | Trạng thái |
|---|---|---|---|
| 0 | Hạ tầng khoá học | lộ trình, todos, tool PDF, sinh_nen, lay_du_lieu, kiểm tra, khuôn buổi, MOI-TRUONG, phụ lục A–E | ✅ (còn push remote) |
| 1 | Khung trợ giúp & dữ liệu | tools/khung/ + danh mục dữ liệu có giấy phép + mirror | 🟡 (chờ mirror HF) |
| 2 | Buổi 1–3 nền móng | 3 buổi · M0 | ✅ |
| 3 | Buổi 4–8 đọc dữ liệu | 5 buổi + Phụ lục C | ✅ |
| 4 | Buổi 9–13 chuẩn bị dữ liệu | 5 buổi + dự án giữa chặng 1 · M1 | 🔲 |
| 5 | Buổi 14–17 đánh giá, ETS, ARIMA | 4 buổi + Phụ lục D | 🔲 |
| 6 | Buổi 18–21 hồi quy, gián đoạn, đa biến, tài chính | 4 buổi · M2 | 🔲 |
| 7 | Buổi 22–24 machine learning | 3 buổi + dự án giữa chặng 2 · M3 | 🔲 |
| 8 | Buổi 25–28 bất định | 4 buổi · M4 | 🔲 |
| 9 | Buổi 29–33 deep learning | 5 buổi · M5 | 🔲 |
| 10 | Buổi 34–37 foundation model & LLM | 4 buổi · M6 | 🔲 |
| 11 | Buổi 38–40 nhân quả & quyết định | 3 buổi | 🔲 |
| 12 | Buổi 41–43 production | 3 buổi · M7 | 🔲 |
| 13 | Dự án cuối | 3 đề + rubric + bộ chấm dữ liệu tương lai + ngày dữ liệu hỏng + lời giải | 🔲 |
| 14 | Đánh giá | ngân hàng 440 câu + 2 đề thực hành + đề đọc biểu đồ + đề tìm rò rỉ | 🔲 |
| 15 | Xuất bản & đóng gói | 44 PDF + 44 zip + README | 🔲 |
| 16 | Kiểm định chất lượng | báo cáo chạy thử toàn khoá + bài kiểm tra độc lập/CPU/không API key | 🔲 |
| | **TỔNG** | **44 buổi · 44 PDF · 2 dự án giữa chặng · 1 dự án cuối** | **1/17 phase** |

### Thứ tự làm bắt buộc
Phase 0 → 1 trước tiên (mọi buổi đều dựa vào: `sinh_nen.py`, `lay_du_lieu.py`, `kiem_ro_ri`,
danh mục dữ liệu phải có trước khi soạn buổi đầu tiên).

Phase 2 → 12 theo đúng thứ tự buổi. **Lý do là mạch kiến thức và quy trình sản xuất, không phải
phụ thuộc file:** khung `tools/khung/` được mở rộng dần (buổi 15 thêm backtest, buổi 25 thêm chỉ
số xác suất…) và mỗi lần mở rộng phải chạy lại `sinh_nen.py` cho các buổi đã có. Sinh xong thì
`tv/` nằm vật lý trong buổi, **buổi N không còn dính gì tới buổi khác**.

Phase 13–14 làm song song được sau Phase 12. Phase 15 → 16 cuối cùng, không đảo.

**Muốn làm bản ngắn?** Lõi 21 buổi (1–21) + dự án giữa chặng 1 và 2 đã là một khoá dự báo thống
kê hoàn chỉnh (M0–M3). Các cụm khác xem bảng "Học theo cụm" trong lộ trình.

### Ước lượng
| Phase | Buổi | Công sức |
|---|---|---|
| 0–1 | — | 4–5 ngày (khung, danh mục dữ liệu, rà giấy phép ~25 bộ, mirror) |
| 2–6 | 21 buổi | ~1,5 ngày/buổi (nhiều hình, nhiều thí nghiệm "chứng minh bằng số") |
| 7–8 | 7 buổi + dự án giữa chặng 2 | ~2 ngày/buổi (dữ liệu lớn, bộ chấm dữ liệu tương lai) |
| 9–10 | 9 buổi | ~2,5 ngày/buổi (huấn luyện CPU chậm, hệ sinh thái đổi nhanh, research nặng) |
| 11–12 | 6 buổi | ~2 ngày/buổi |
| 13–16 | — | 7–9 ngày (dự án cuối cần 3 ngày dự báo trực tiếp thật để thử bộ chấm) |

### Ghi chú rủi ro
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
- **pandas 3 vs hệ Nixtla** (phát hiện Phase 0): statsforecast/utilsforecast/mlforecast/autogluon chưa hỗ trợ
  pandas 3 → hai dòng pandas song song trong khoá. Mỗi phase rà lại; khi Nixtla hỗ trợ thì gỡ `[[rang_buoc]]`
  và chạy lại `sinh_nen.py --tat-ca --nang-cap`
- **Rủi ro lớn nhất của thiết kế độc lập**: 44 bản `tv/` và 44 `uv.lock` lệch nhau. Chống bằng đúng một
  cách — **luôn sinh bằng `sinh_nen.py`, không bao giờ sửa tay**
