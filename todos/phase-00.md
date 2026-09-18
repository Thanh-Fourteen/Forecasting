# Phase 0 — Hạ tầng khoá học ✅ (trừ push remote)

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 0"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

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
      Phase 3 thêm hình cho C, Phase 10/13 thêm ví dụ dữ liệu thật cho D. **Phụ lục F** làm cùng Phase 1
- [x] Khuôn buổi `tools/khuon-buoi/` — `tai-lieu.md` 9 mục có chú thích, `kiem-tra.md`, `NGHIEN-CUU.md`, `code/README.md`,
      `dap-an/README.md`, `lab/nen.toml`, `lab/Makefile` (make 3.81; up/check/notebook/down; `BAI=`), `lab/cham/conftest.py`
- [x] **Chạy thử** buổi giả `buoi-00-thu` (UCI Bike Sharing): sinh nền → `make up` (sha256 khớp) → check code ĐỎ đúng /
      dap-an XANH → down; copy riêng thư mục ra ngoài repo + cache trắng vẫn chạy; `kiem_tra_lab --may-trang` ĐẠT;
      zip không lọt tệp nội bộ, 2 lần đóng gói cùng sha256. Đã xoá buổi giả
- [ ] Tạo remote GitHub và push lần đầu
