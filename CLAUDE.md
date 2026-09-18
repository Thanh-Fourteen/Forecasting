# Khoá Forecasting in AI — giáo trình tiếng Việt 44 buổi

Repo độc lập: lộ trình, giáo trình, code mẫu, bộ chấm và dự án cho khoá dự báo từ cơ bản đến
nâng cao. Không phụ thuộc repo nào khác — mọi thứ cần cho một buổi đều nằm trong repo này.

**44 buổi** = 3 nền móng + **10 hiểu & chuẩn bị dữ liệu** (trọng tâm) + 8 thống kê + 3 ML
+ 4 bất định + 5 deep learning + 4 foundation model & LLM + 3 nhân quả & quyết định
+ 3 production + buổi 44 (dự án cuối). Kèm 2 dự án giữa chặng (sau buổi 13 và 24).

Kế hoạch xây khoá và tiến độ: `todos.md` — **luôn đọc trước, tìm phase đầu tiên còn 🔲**. `todos.md` chỉ giữ
tiêu đề/trạng thái + prompt của mọi phase. Quy ước (giao thức research, chuẩn dễ hiểu, DoD, bảng chỗ hở): `todos/quy-uoc.md`;
tiến độ/rủi ro: `todos/tong-quan.md`; chi tiết từng phase: `todos/phase-NN.md`.
Nội dung từng buổi: `lo-trinh/lo-trinh-forecasting.md`.

## Người dùng ưu tiên gì

- **Tiền xử lý dữ liệu, khử nhiễu, hiểu sâu khái niệm, đọc biểu đồ, phân tích tương quan** —
  đây là phần phải làm kỹ nhất, không được lướt
- **Dự án phải thực tế**: dữ liệu bẩn thật, baseline thật để vượt, chấm trên dữ liệu tương lai
- **Kiến thức đầy đủ và cập nhật** — mọi phase bắt đầu bằng research (xem dưới)
- **Dễ hiểu cho người tự học** — đọc tài liệu xong không phải đi hỏi ChatGPT (quy tắc 14)

## Repository Map

| Đường dẫn | Nội dung |
|---|---|
| `lo-trinh/` | Lộ trình 44 buổi, nguồn của mọi buổi |
| `phu-luc/` | Phụ lục A–F dùng chung (Python, xác suất, đọc biểu đồ, công thức chỉ số, từ điển, nguồn dữ liệu) |
| `buoi-NN/` | Một buổi tự chứa: `tai-lieu.md`, PDF, `NGHIEN-CUU.md`, `hinh/`, `code/`, `dap-an/`, `lab/`, `kiem-tra.md` |
| `buoi-NN/lab/nen.toml` | **Viết tay**: tên thư viện + tên bộ dữ liệu buổi cần (`[ghi_de]` có lý do nếu phải lệch bảng chung) |
| `buoi-NN/lab/00-nen/` | **Nền của buổi — sinh tự động**: `pyproject.toml` + `uv.lock`, `du-lieu.toml` (URL + sha256 + giấy phép), `lay_du_lieu.py`, `requirements.txt` (cho conda/pip), `tv/` (khung trợ giúp, `import tv`); kèm `lab/lab.py` (`python lab.py up/check/chay/notebook/down`, thay Makefile từ 2026-09-18) |
| `du-an-giua-chang/` | 01 EDA & làm sạch, 02 thi dự báo trên dữ liệu tương lai |
| `du-an-cuoi/` | 3 đề thực tế, rubric 100+20, bộ chấm, "ngày dữ liệu hỏng" |
| `danh-gia/` | Ngân hàng câu hỏi, đề thực hành, đề đọc biểu đồ, đề tìm rò rỉ |
| `phat-de/` | Sinh ra: `buoi-NN.zip` phát cho học viên (gitignore) |
| `tools/` | `CHUAN-DE-HIEU.md` (chuẩn dễ hiểu + prompt đọc thử), `kiem_de_hieu.py`, `xuat_pdf.py`, `sinh_nen.py`, `lay_du_lieu.py`, `kiem_tra_doc_lap.sh`, `kiem_tra_lab.py`, `dong_goi.py`, `khung/` (nguồn của `tv/`), `nen/phien-ban.toml` (phiên bản chung), `nen/lab.py` (nguồn của `lab/lab.py`), `nb.py` (soạn `code/lab.ipynb`), `du-lieu/danh-muc.toml`, `khuon-buoi/`, `NGHIEN-CUU.md` |
| `todos.md`, `todos/` | `todos.md`: tiêu đề phase + prompt (autoclick theo dõi); `todos/quy-uoc.md`, `todos/tong-quan.md`, `todos/phase-NN.md`. Xong phase → đổi 🔲→✅ ở `todos.md` VÀ `todos/phase-NN.md` |
| `phan-hoi-hoc-vien.md` | Người học ghi đoạn khó hiểu — đọc trước khi soạn/viết lại buổi |
| `MOI-TRUONG.md`, `pyproject.toml` | Hướng dẫn cài cho học viên; cấu hình ruff (repo **không** phải dự án uv — cấm `[tool.uv.workspace]`) |

## Research trước khi soạn (CRITICAL)

Lĩnh vực đổi rất nhanh; lộ trình chỉ đúng tới ngày rà soát ghi trong đó. **Trước khi viết bất kỳ
buổi nào**: WebSearch/WebFetch tài liệu chính thức + bài báo mới nhất cho từng chủ đề, xác minh
phiên bản thư viện, API, dataset (URL + giấy phép), model mới; ghi vào `buoi-NN/NGHIEN-CUU.md`
có nguồn và ngày. Lệch lớn so với lộ trình → cập nhật `lo-trinh` + `todos.md` và báo người dùng
**trước** khi soạn. Giao thức đầy đủ: mục "Giao thức research" trong `todos/quy-uoc.md`.

## Quy tắc soạn nội dung (CRITICAL)

1. **Mỗi buổi tự chứa — không có ngoại lệ.** Buổi N **không đọc một byte nào ngoài `buoi-NN/`**
   (trừ cache dữ liệu tải về có kiểm sha256). Không `../buoi-06/...`, không dùng dữ liệu đã làm
   sạch ở buổi khác, không import từ `tools/`.
2. **Cơ chế `lab/00-nen/`** sinh tự động bằng `python tools/sinh_nen.py N` từ `lab/nen.toml` — **đừng
   chép tay, đừng sửa tay bất cứ gì trong `00-nen/`**. Sửa `tools/khung/`, `tools/lay_du_lieu.py`,
   `tools/nen/phien-ban.toml` hay danh mục dữ liệu thì chạy lại `sinh_nen.py --tat-ca`.
   Phiên bản thư viện lấy từ **bảng chung** `tools/nen/phien-ban.toml`; thư viện mới phải xác minh rồi
   thêm vào bảng. Hệ Nixtla/AutoGluon chưa hỗ trợ pandas 3 → bảng có `[[rang_buoc]]` tự chốt pandas 2.3.3.
   Mọi thứ giám khảo giữ (lỗi cài sẵn, holdout) đặt trong thư mục `giam-khao/` — `dong_goi.py` lọc.
   Buổi dạy học viên TỰ VIẾT một công cụ của khung thì khai `khung_bo = ["ro_ri"]` trong `lab/nen.toml`
   (buổi 4: `ve`, 13: `ro_ri`, 14: `danh_gia`, 15: `backtest`) — không phát lời giải qua `tv/`.
   Sửa `tools/khung/` thì chạy `python tools/kiem_khung.py` (test ở cả pandas 3 và pandas 2.3.3 + Nixtla).
3. **Chỗ hở cố ý.** `code/` phải sai đúng chỗ bài học hôm đó sửa (bảng trong `todos/quy-uoc.md`). Chỗ hở
   phổ biến nhất: **rò rỉ tương lai** và **đánh giá không trung thực** — `code/` cho kết quả đẹp
   giả tạo để học viên tự phát hiện. Đừng sửa trước giờ dạy.
4. **Mọi lệnh và mọi con số trong tài liệu phải lấy từ lần chạy thật** (ghi seed). Không có
   "cải thiện khoảng 20%" viết cho đẹp.
5. **Chốt phiên bản**: thư viện trong `uv.lock`, model theo revision Hugging Face, LLM theo tên đầy
   đủ có ngày. Không `latest`.
6. **Dữ liệu có giấy phép đã xác minh.** CC BY/CC0/public domain được mirror; bộ cấm phân phối lại
   (Kaggle M5…) học viên tự tải và luôn có bộ dự phòng mở. Không commit dữ liệu vào git.
   Buổi chỉ dùng bộ có trong `tools/du-lieu/danh-muc.toml` đã chốt sha256 (không `cho_sha256`).
   **Không dùng FRED/ALFRED** (điều khoản cấm dùng cho machine learning) — lấy chuỗi từ cơ quan gốc;
   không dùng NOAA ISD ngoài Mỹ (WMO Res 40) — dùng GHCNh. Chi tiết: `tools/du-lieu/NGHIEN-CUU.md`.
7. **Chạy được bằng CPU.** GPU chỉ để nhanh hơn. Buổi 36–37 có nhánh model mở local + bản ghi phản
   hồi LLM để chấm không cần API key.
8. **Đánh giá trung thực**: mọi mô hình so với seasonal naive trên backtest rolling origin; từ buổi
   12 mọi `lab/cham/` có test rò rỉ tự động; foundation model/LLM chỉ đánh giá trên dữ liệu **sau**
   mốc cắt của model.
9. **`dap-an/`, `NGHIEN-CUU.md`, `loi-giai-mau/`, `ngay-du-lieu-hong/` không bao giờ vào zip** —
   `dong_goi.py` lọc, đừng gỡ bộ lọc.
10. **Tiếng Việt, thuật ngữ kỹ thuật giữ nguyên tiếng Anh** (backtest, quantile, seasonal naive,
    drift...), thống nhất theo Phụ lục E.
11. **Khung tài liệu 9 mục, bắt buộc đủ:** Mục tiêu → Nhắc lại buổi trước → **Trạng thái đầu
    buổi** → Lý thuyết → Lab từng bước → Lỗi thường gặp & cách chẩn đoán → Bài tập về nhà →
    Tiêu chí "Xong khi" → Đọc thêm.
    - *Lý thuyết* mở đầu bằng bảng "Từ mới trong buổi"; ≤ 6 khái niệm chính; mỗi khái niệm theo khuôn:
      **vấn đề → trực giác → ví dụ số nhỏ tính tay → hình → công thức → nói bằng lời có thay số → NumPy →
      thư viện → dữ liệu thật → tóm lại**
    - *Nhắc lại buổi trước* viết đủ để **không cần** mở lại buổi trước
    - *Trạng thái đầu buổi* là bảng: dữ liệu (file, số dòng, khoảng thời gian, sha256 rút gọn),
      môi trường, `code/` có gì, **cái gì đang cố tình sai và triệu chứng**
12. **Công thức** viết LaTeX: `$...$` trong dòng, `$$...$$` khối riêng — `xuat_pdf.py` render ra SVG.
    **Hình** sinh bằng `dap-an/ve_hinh.py` → `hinh/*.png`, không vẽ tay; tiêu đề hình nói kết luận.
13. **Độ dài:** `tai-lieu.md` 3.500–6.500 chữ ngoài bảng/code (`kiem_de_hieu.py`), PDF 10–18 trang (`python tools/xuat_pdf.py --kiem`)
    — số chốt ở Phase 7. Giới hạn thật là số khái niệm (≤ 6) — thừa thì bỏ bớt/chuyển "Nâng cao", **không nén chữ,
    không độn chữ**.
14. **Dễ hiểu là tiêu chí nghiệm thu** (bài học 2026-09-18: người dùng học buổi 1–13 phải hỏi ChatGPT mới
    hiểu). Người đọc: biết Python + toán phổ thông, chưa học thống kê đại học, tự học một mình — **đọc xong
    không phải tra ngoài**. Quy tắc D1–D13 ở mục "Chuẩn dễ hiểu" của `todos/quy-uoc.md` (chi tiết + mẫu chuẩn:
    `tools/CHUAN-DE-HIEU.md`). Tóm tắt: định nghĩa mọi từ mới ngay lần đầu; chưa dạy thì chưa dùng (hoặc hộp
    "Mượn trước"); không chen trích tiếng Anh; không nói lửng ("thiếu" so với cái gì, đơn vị gì); công thức
    luôn kèm câu nói bằng lời có thay số (PDF copy ra mất công thức); ≤ 3 con số/đoạn; mỗi hình có "Cách đọc
    hình", mỗi bảng có "Đọc bảng"; quiz giải thích vì sao. Đọc `phan-hoi-hoc-vien.md` trước khi soạn.
15. **Dễ hiểu nhưng GỌN** (D13, bài học 2026-09-18: bản viết lại buổi 1–3 dễ hiểu hơn nhưng dài dòng). Mỗi ý nói
    một lần (không lặp giữa thân bài, "Tóm lại", Lab, "Lỗi thường gặp"); không câu rỗng/rào đón; một ví dụ đủ thì
    không thêm; khuôn D2 là trần, không phải sàn; sửa chỗ khó bằng viết lại câu, không chèn thêm đoạn.

## Definition of Done cho mỗi buổi

- `NGHIEN-CUU.md` có nguồn + ngày + phiên bản đã xác minh
- `tai-lieu.md` đủ 9 mục; công thức và hình hiển thị đúng trong PDF
- Đạt chuẩn dễ hiểu + gọn: `tools/kiem_de_hieu.py NN` sạch + **rà gọn** bằng subagent biên tập viên (≤ 3 chỗ thừa)
  + **đọc thử** bằng subagent học viên mới theo prompt trong
  `tools/CHUAN-DE-HIEU.md` (0 chỗ chặn, ≤ 5 chỗ khó, quiz ≥ 9/10 chỉ bằng tài liệu), ghi mục "Đọc thử" trong `NGHIEN-CUU.md`
- `code/` chạy được, có chỗ hở cố ý, kèm `README.md` ngắn
- `dap-an/` là bản đã sửa, `python lab.py check --dap-an` xanh; `code/` thì `python lab.py check` đỏ đúng chỗ hở
- `lab/00-nen/` dựng đúng nền **từ venv trắng** (`uv sync --frozen` + dữ liệu qua sha256)
- `lab/lab.py` (sinh tự động) chạy được `up` / `check` / `down`, cả `up --pip` cho conda; `check` < 10 phút trên CPU 4 nhân
- `kiem-tra.md` 10 câu (4 nhắc lại, 4 vận dụng, 2 đọc biểu đồ/bảng kết quả tìm chỗ sai), đáp án trong `<details>`
- `ruff check` sạch; Lab có notebook `code/lab.ipynb` phát sẵn (soạn bằng `tools/nb.py`), commit **không output**,
  chạy hết không lỗi (`kiem_tra_lab.py` chạy nó)
- `tools/kiem_tra_doc_lap.sh` xanh
- PDF sinh ra, mở kiểm tra bảng, khối code, công thức, ảnh; 10–18 trang
- Chạy thử toàn bộ lab trên **venv trắng** một lần rồi mới tick ✅ trong `todos.md`

## Công cụ

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r tools/requirements.txt   # một lần

.venv/bin/python tools/xuat_pdf.py [5 6 | lo-trinh]   # md -> PDF nằm cạnh file nguồn
.venv/bin/python tools/xuat_pdf.py --kiem             # đếm trang, báo buổi ngoài 10–16
cp -r tools/khuon-buoi buoi-07                        # buổi mới từ khuôn, rồi sửa buoi-07/lab/nen.toml
.venv/bin/python tools/sinh_nen.py 7                  # sinh buoi-07/lab/00-nen/ + uv lock  (--kiem, --tat-ca, --nang-cap)
.venv/bin/python tools/lay_du_lieu.py buoi-07         # tải + kiểm sha256  (--tom-tat: bảng cho "Trạng thái đầu buổi")
.venv/bin/python tools/lay_du_lieu.py X --tac-gia     # bộ dữ liệu mới: tải rồi IN sha256 để ghi vào danh mục
./tools/kiem_tra_doc_lap.sh [7]                       # K1–K10 chặn phá tính tự chứa  (--nhanh: bỏ uv lock --check)
.venv/bin/python tools/kiem_tra_lab.py [7]            # down→up→check dap-an (xanh)→check code (đỏ)→down  (--may-trang)
.venv/bin/python tools/dong_goi.py 7                  # phat-de/buoi-07.zip, lọc đáp án  (--liet-ke)
.venv/bin/ruff check .                                # lint toàn repo
python3 tools/kiem_de_hieu.py [7] [--chi-tiet]        # kiểm máy chuẩn dễ hiểu D1–D13 (test: tools/test_kiem_de_hieu.py)
.venv/bin/python tools/kiem_khung.py                  # test tools/khung/ ở hồ sơ pandas3 + nixtla
.venv/bin/python tools/du-lieu/tai_danh_muc.py --may-trang   # tải TOÀN BỘ danh mục, kiểm sha256
.venv/bin/python tools/du-lieu/sinh_phu_luc_f.py      # Phụ lục F từ danh mục (không sửa tay)
.venv/bin/python tools/du-lieu/mirror_hf.py --repo ORG/REPO --chuan-bi   # (--day-len: cần HF_TOKEN + đồng ý)

cd buoi-07/lab && python lab.py up && python lab.py check --dap-an   # như học viên; check = chấm code/
```

`xuat_pdf.py` cần `markdown-it-py`, `mdit-py-plugins`, `weasyprint`, `ziamath`, `pypdf` (không cần
cài LaTeX). Trong bảng, `|` nằm trong công thức được tự đổi thành `\vert`.

## Môi trường lab

Mặc định: **Python 3.12 + uv, CPU 4 nhân, 16 GB RAM**, không cần GPU, không cần cloud.

| Buổi | Cần thêm |
|---|---|
| 10, dự án giữa chặng 1, đề C | API key OpenAQ (miễn phí) |
| 23, đề A | Tài khoản Kaggle, chấp nhận luật M5 (có dự phòng UCI Online Retail II) |
| 29–35 | 16 GB RAM; có cấu hình rút gọn cho máy 8 GB; GPU tuỳ chọn |
| 33 | ~5 GB đĩa cho dữ liệu AIFS/ERA5 cắt nhỏ |
| 36–37 | Ollama/llama.cpp với model mở, hoặc API key LLM (trần chi phí < 5 USD/buổi) |
| 41–43, dự án giữa chặng 2, đề B | API key EIA (miễn phí), Docker |
