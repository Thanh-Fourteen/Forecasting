# Nhật ký research — Phase 0 (hạ tầng)

- **Ngày research:** 2026-09-17 (mọi nguồn dưới đây truy cập ngày này, trừ khi ghi khác)
- **Phạm vi:** uv, ruff, jupytext, nbstripout, JupyterLab; tải dữ liệu bằng script (UCI, Kaggle,
  Hugging Face, EIA, OpenAQ, Open-Meteo); mirror lên Hugging Face Datasets; công cụ môi trường
  (WSL2, make, Ollama, llama.cpp, Docker, weasyprint); nguồn cho Phụ lục A–E
- **Cách kiểm:** đọc tài liệu chính thức / changelog / PyPI JSON; chạy thử cục bộ với uv 0.12.15
  trong thư mục tạm; gọi endpoint công khai bằng curl **không dùng key**
- Ký hiệu: **[CHẠY]** = đã chạy thử và thấy kết quả; **[CHƯA XÁC MINH]** = không kiểm được, không
  dùng làm căn cứ viết lý thuyết

---

## 1. Phiên bản đã xác minh (PyPI JSON `https://pypi.org/pypi/<gói>/json`)

Bảng này là nguồn của `tools/nen/phien-ban.toml`. **Kiểm tương thích [CHẠY]** mỗi gói cùng
`pandas==3.0.5` + `numpy==2.5.3` bằng `uv pip compile --python-version 3.12 --exclude-newer 2026-09-17`:
không resolve được với statsforecast, utilsforecast, mlforecast, autogluon.timeseries (xem mục 11);
resolve được với mọi gói còn lại trong bảng. pandas 2.3.3 (bản 2.x cuối, PyPI simple API) + numpy 2.5.3
resolve được với cả nhóm Nixtla + lightgbm, với neuralforecast, và với autogluon.timeseries (kéo torch 2.13.0). Mỗi phase buổi học vẫn phải rà lại tương thích
khi `uv lock` (phiên bản mới nhất chưa chắc hợp nhau).

| Gói | Phiên bản | Ngày phát hành | Ghi chú |
|---|---|---|---|
| uv / uv_build | 0.12.15 | 2026-09-15 | sửa hồi quy của 0.12.14 cùng ngày |
| ruff | 0.16.8 | 2026-09-16 | 0.16.0 đổi mạnh bộ rule mặc định (mục 3) |
| jupytext | 1.19.5 | 2026-07-21 | repo chuyển về github.com/jupytext/jupytext |
| jupyterlab | 4.6.3 | 2026-08-10 | |
| ipykernel | 7.3.0 | 2026-06-10 | |
| nbstripout | 0.9.1 | 2026-02-21 | **không dùng** (mục 4) |
| pytest | 9.1.1 | 2026-06-19 | |
| numpy | 2.5.3 | 2026-09-06 | cần Python ≥ 3.12 |
| pandas | 3.0.5 | 2026-07-22 | 3.0.0 phát hành 2026-01-21 (Phụ lục A) |
| polars | 1.44.2 | 2026-09-09 | |
| duckdb | 1.5.5 | 2026-07-22 | |
| pyarrow | 25.0.1 | 2026-08-10 | |
| scipy | 1.18.1 | 2026-08-21 | |
| statsmodels | 0.15.0 | 2026-08-27 | |
| matplotlib | 3.11.2 | 2026-09-11 | |
| seaborn | 0.13.2 | 2024-01-25 | bản cuối đã 2 năm — rà lại ở Phase 3 |
| plotly | 7.1.0 | 2026-09-15 | |
| scikit-learn | 1.9.1 | 2026-09-10 | |
| statsforecast | 2.1.1 | 2026-07-16 | |
| utilsforecast | 0.2.16 | 2026-04-27 | thang đo sMAPE/MAPE là tỷ lệ (mục 9) |
| mlforecast | 1.1.0 | 2026-07-10 | |
| neuralforecast | 3.2.2 | 2026-09-08 | |
| hierarchicalforecast | 1.5.1 | 2026-03-04 | |
| lightgbm | 4.7.0 | 2026-07-18 | |
| optuna | 5.0.0 | 2026-09-07 | major mới — rà API ở Phase 7 |
| ruptures | 1.1.10 | 2025-09-10 | `requires-python <3.14` |
| PyWavelets | 1.10.0 | 2026-09-07 | |
| MAPIE | 1.5.0 | 2026-08-05 | |
| pymc / pymc-extras | 6.3.2 / 0.15.1 | 2026-09-08 / 2026-09-16 | |
| torch | 2.14.0 | 2026-09-02 | CPU: index `download.pytorch.org/whl/cpu` (mục 2) |
| chronos-forecasting | 2.3.2 | 2026-09-08 | |
| timesfm | 3.0.2 | 2026-09-09 | |
| autogluon.timeseries | 1.6.2 | 2026-09-14 | `requires-python <3.14` |
| pandera / prefect / mlflow | 0.33.1 / 3.8.6 / 3.16.1 | 09/2026 | |
| shap | 0.52.0 | 2026-05-28 | |
| scoringrules | 0.11.0 | 2026-06-06 | có lỗi WIS (mục 9) |
| kagglehub / kaggle | 1.0.2 / 2.2.4 | 2026-06-09 / 2026-07-23 | |
| huggingface_hub | 1.32.0 | 2026-09-17 | 1.x dùng httpx; CLI là `hf` |
| tzdata | 2026.4 | 2026-09-12 | IANA tzdb 2026d |
| weasyprint | 70.0 | 2026-09-08 | công cụ PDF của repo, đã chốt trong `tools/requirements.txt` |
| Ollama | v0.34.1 | 2026-09-14 | github.com/ollama/ollama/releases |

---

## 2. uv — nền của mỗi buổi

Nguồn: https://github.com/astral-sh/uv/releases, https://github.com/astral-sh/uv/blob/main/CHANGELOG.md,
https://docs.astral.sh/uv/concepts/projects/sync/, https://docs.astral.sh/uv/concepts/projects/config/,
https://docs.astral.sh/uv/reference/settings/, https://docs.astral.sh/uv/concepts/projects/workspaces/,
https://docs.astral.sh/uv/concepts/resolution/, https://docs.astral.sh/uv/guides/integration/pytorch/,
https://docs.astral.sh/uv/guides/integration/jupyter/, https://docs.astral.sh/uv/concepts/python-versions/

**Ngữ nghĩa cờ (trích `uv help sync`, [CHẠY] với 0.12.15):**
- `--frozen`: "uses the versions in the lockfile as the source of truth… If the `pyproject.toml`
  includes changes to dependencies that have not been included in the lockfile yet, they will not be
  present in the environment." **[CHẠY]** thêm `six` vào pyproject mà không lock lại → `uv sync
  --frozen` thoát 0 và *không* cài `six`; `--locked` thoát 1.
- `--locked`: "If the lockfile is missing or needs to be updated, uv will exit with an error."
- `uv lock --check`: "Equivalent to `--locked`" — thoát 1 khi lock cũ (từ 0.8 đổi mã thoát 2 → 1).
- `uv run --no-sync` "Implies `--frozen`". `uv sync` mặc định là *exact* (gỡ gói không khai).
- Dự án không có `[build-system]` hoặc `tool.uv.package = false` thì uv chỉ cài phụ thuộc.
- `VIRTUAL_ENV` đang bật trỏ nơi khác bị bỏ qua kèm cảnh báo **[CHẠY]** → Makefile gỡ biến này.

**Thay đổi phá vỡ cần biết:** 0.12.0 (2026-07-28): `uv init` mặc định tạo dự án *packaged*;
`uv run` tìm dự án theo đường dẫn script. 0.10.0: `uv venv` cần `--clear` để ghi đè. **0.9.0: bản
Python mặc định khi cài là 3.14** → phải chốt `requires-python = "==3.12.*"` + `.python-version`.
Lockfile mới: `version = 1`, `revision = 3` **[CHẠY]**.

**Tái lập:** "uv.lock is a universal or cross-platform lockfile" (docs layout). `exclude-newer`
nhận mốc RFC 3339 hoặc khoảng thời gian tương đối — **khoảng tương đối tính từ lúc chạy nên không
tái lập**; dùng mốc cố định, uv ghi mốc vào `[options]` của `uv.lock` **[CHẠY]**.

**Workspace — KHÔNG dùng cho buổi học.** Docs: "the workspace shares a single lockfile"; không nên
dùng khi thành viên "desire a separate virtual environment for each member". **[CHẠY]** gốc repo có
`[tool.uv.workspace] members = ["lessons/*"]` → `uv lock` trong buổi ghi vào `uv.lock` **của gốc**
(buổi bị nuốt âm thầm). Gốc có `pyproject.toml` *không* có bảng workspace → buổi độc lập.
→ `pyproject.toml` gốc của repo **không có `[project]`, không có `[tool.uv.workspace]`**;
`kiem_tra_doc_lap.sh` chặn nếu ai đó thêm.

**Cài `tv/` thành package editable** **[CHẠY]**: `[build-system] uv_build` +
`[tool.uv.build-backend] module-name = "tv"`, `module-root = ""` → `import tv` chạy từ mọi thư mục
bằng venv của buổi (kể cả kernel Jupyter). File `.pth` trỏ đường dẫn tuyệt đối → venv không di
chuyển được (venv không bao giờ nằm trong zip nên chấp nhận).

**PyTorch CPU** (docs pytorch): `[[tool.uv.index]] name = "pytorch-cpu", url =
"https://download.pytorch.org/whl/cpu", explicit = true` + `[tool.uv.sources] torch = [{ index =
"pytorch-cpu" }]`; `explicit = true` để index chỉ dùng cho torch. → `sinh_nen.py` tự thêm khi buổi
dùng torch (Phase 9 kiểm lại trên macOS vì wheel CPU/MPS khác nhau).

**Jupyter với uv** (docs jupyter): `uv run --with jupyter jupyter lab`; hoặc `ipykernel` trong dự
án. → khoá dùng nhóm phụ thuộc `notebook` (jupyterlab + jupytext + ipykernel) trong chính buổi.

## 3. ruff

Nguồn: https://github.com/astral-sh/ruff/releases/tag/0.16.0, https://docs.astral.sh/ruff/configuration/,
https://docs.astral.sh/ruff/settings/

- 0.16.0 (2026-07-23): bộ rule mặc định tăng **59 → 413**; bỏ khỏi mặc định "E401, E402, E701…,
  E731, E741…, F403, F405…". Định dạng khối code Markdown bật mặc định.
- **[CHẠY]** với mặc định mới, file dạng percent bị báo I001 (import ở ô sau), B018 (biểu thức trần
  `df` cuối ô), S110, E722 → **phải `select` tường minh** và bỏ B018 cho `code/`, `dap-an/`.
- Notebook được lint mặc định từ 0.6.0 — không cần `extend-include`.
- `target-version` tự theo `project.requires-python`; gốc repo không có `[project]` nên ghi rõ `py312`.

## 4. jupytext, nbstripout

Nguồn: https://pypi.org/project/jupytext/, https://jupytext.org/using/config/,
https://jupytext.org/formats/scripts/, https://jupytext.org/using/cli/,
https://jupytext.org/getting-started/install/, https://jupytext.org/reference/faq/,
https://github.com/kynan/nbstripout

- Cấu hình ở `jupytext.toml` hoặc `[tool.jupytext]` trong `pyproject.toml`; tìm ở "Current directory
  and parent directories" → cấu hình gốc repo áp cho mọi buổi, nhưng zip phát học viên không có gốc
  → `Makefile` của buổi gọi `jupytext --to ipynb` tường minh, không dựa vào cấu hình.
- Percent format: "all cells are explicitly delimited with a commented double percent sign `# %%`";
  ô markdown là `# %% [markdown]`.
- "The Jupytext extension for JupyterLab is bundled with Jupytext"; từ 1.16.0 chỉ hợp JupyterLab 4.
- FAQ: "Unless you want to version the outputs, you should version _only the text representation_".
- **Quyết định:** commit `.py` percent, **gitignore `*.ipynb`** trong `buoi-*/` → không cần
  nbstripout (lệch nhỏ so với todos: bỏ nbstripout). `kiem_tra_doc_lap.sh` chặn `.ipynb` được git theo dõi.
- `notebook_metadata_filter = "-all"`, `cell_metadata_filter = "-all"` **[CHƯA XÁC MINH trên trang
  docs hiện tại]** → không đặt vào cấu hình; `.py` do tác giả viết tay nên không có metadata thừa.

## 5. Tải dữ liệu bằng script

### UCI Machine Learning Repository
- Mẫu URL `https://archive.ics.uci.edu/static/public/<id>/<slug>.zip` — **[CHẠY]** 200 cho id 275,
  235, 360, 502, 321.
- **Không có Content-Length/ETag/Last-Modified, bỏ qua Range (trả 200 thay vì 206), tốc độ đo được
  10–20 KB/s** → không tiếp tục tải dở được, bộ lớn (id 321: 249,2 MB) có thể mất hàng giờ →
  **bộ UCI > 10 MB bắt buộc mirror** (ghi vào rủi ro trong `todos.md`).
- Giấy phép ghi trên trang từng bộ (275, 235, 360, 502, 321): "This dataset is licensed under a
  Creative Commons Attribution 4.0 International (CC BY 4.0) license." Không tìm thấy tuyên bố
  chung toàn site → **ghi giấy phép theo từng bộ**.
- **Bộ dùng để chạy thử Phase 0 — Bike Sharing (id 275):**
  URL `https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip`, 279.992 byte,
  sha256 `b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401` (tải 2 lần cùng sha),
  gồm `Readme.txt`, `day.csv` (731 dòng dữ liệu), `hour.csv` (17.379 dòng dữ liệu), xuống dòng CRLF.
  Trích dẫn: "Fanaee-T, H. (2013). Bike Sharing [Dataset]. UCI Machine Learning Repository.
  https://doi.org/10.24432/C5W894."
- API metadata UCI báo `num_instances: 17389` ≠ 17.379 dòng thật → không kiểm số dòng theo metadata.
- `ucimlrepo` 0.0.7 (2024-05-21), không trả giấy phép, có issue chậm/lỗi đọc → **không dùng**.

### Kaggle
Nguồn: PyPI; mã nguồn `kaggle` 2.2.4, `kagglesdk` 0.1.37, `kagglehub` 1.0.2;
https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md; issue kaggle-cli #555.
- Xác thực (thứ tự trong `authenticate()`): "1. An active access token 2. A legacy API key. 3. OAuth
  credentials 4. Anonymous fallback". Token mới: `KAGGLE_API_TOKEN` hoặc `~/.kaggle/access_token`;
  OAuth: `kaggle auth login` (2.1.1, 2026-05-05). `kaggle.json` giờ là "Legacy API Credentials".
- `import kaggle` tự đăng nhập lúc import và gọi `exit(1)` khi thiếu thông tin → **trong script dùng
  `kagglehub`** (ném ngoại lệ bình thường).
- **[CHẠY]** không đăng nhập → 401 `UNAUTHENTICATED`. Chưa chấp nhận luật → 403 (issue #555; câu
  chữ hiện tại **[CHƯA XÁC MINH]** → không so khớp theo chuỗi, chỉ theo mã).
  `kagglehub.exceptions.KaggleApiHTTPError` cho 401/403, `UnauthenticatedError` khi không có thông tin.
- **M5** (`m5-forecasting-accuracy`): 5 CSV, tổng 450.472.284 byte chưa nén; `licenseName` "Subject
  to Competition Rules". Luật §7A: "You may access and use the Competition Data for non-commercial
  purposes only, including for participating in the Competition and on Kaggle.com forums, and for
  academic research and education." §7B: "You agree not to transmit, duplicate, publish,
  redistribute or otherwise provide or make available the Competition Data to any party not
  participating in the Competition." → **khớp lộ trình: không mirror, học viên tự tải**.

### Hugging Face
Nguồn: https://huggingface.co/docs/huggingface_hub/guides/download, …/guides/cli,
https://huggingface.co/docs/hub/rate-limits, …/storage-limits, …/repositories-licenses,
https://huggingface.co/content-policy, …/docs/hub/xet/legacy-git-lfs
- **[CHẠY]** URL `https://huggingface.co/datasets/<repo>/resolve/<sha40>/<tệp>` tải được không cần
  token (307 → 200) → nguồn `hf` của `lay_du_lieu.py` chỉ cần thư viện chuẩn.
- Revision: "When using the commit hash, it must be the full-length hash instead of a 7-character
  commit hash." Tag/nhánh đổi được → **chốt commit 40 ký tự**, tag chỉ làm nhãn.
- ETag: với tệp LFS/Xet `x-linked-etag` là sha256; tệp nhỏ không-LFS là sha1 git → **tự tính sha256**.
- Giới hạn ẩn danh: 3.000 lượt "resolvers" / 5 phút / IP (header `ratelimit-policy` thấy trực tiếp) —
  cả lớp chung một NAT có thể chạm → `lay_du_lieu.py` gửi `HF_TOKEN` nếu có.
- CLI là `hf` (`huggingface-cli` "is deprecated and no longer works").
- Mirror: `HfApi().create_repo(repo_type="dataset", exist_ok=True)`, `upload_folder` → `CommitInfo.oid`
  là sha commit. Thẻ dữ liệu: `license: cc-by-4.0` | `cc0-1.0` | `other` (+ `license_name`, tệp
  LICENSE). Không có trường ghi nguồn riêng → ghi nguồn + link giấy phép + "đã thay đổi gì" trong
  thân README (yêu cầu của CC BY). Parquet được khuyến nghị ("good support for Parquet"); <100k tệp/repo.
- Chính sách nội dung cấm "Content that infringes the intellectual property rights of a third party"
  → chỉ mirror bộ có giấy phép cho phân phối lại.

### EIA API v2
Nguồn: https://www.eia.gov/opendata/documentation.php, https://www.eia.gov/about/copyrights_reuse.php,
https://www.eia.gov/survey/form/eia_930/instructions.pdf, https://www.eia.gov/todayinenergy/detail.php?id=54899
- **[CHẠY]** gốc `https://api.eia.gov/v2/`, `apiVersion 2.1.14`; thiếu key → 403 `API_KEY_MISSING`;
  `api_key=DEMO_KEY` chạy được để thử (`x-ratelimit-limit: 10`).
- Route `electricity/rto/region-data` (Form EIA-930), facet `type`: `D`, `DF` (dự báo day-ahead),
  `NG`, `TI`; `frequency=hourly` là UTC (`YYYY-MM-DDTHH`), `local-hourly` kèm offset.
- Phân trang: "The API will not return more than 5,000 rows" → `offset`/`length`; `total` và `value`
  là **chuỗi**; cảnh báo "incomplete return" xuất hiện cả khi đủ dòng → so `total` với số dòng đã lấy.
- Giấy phép: "U.S. government publications are in the public domain and are not subject to copyright
  protection." Ghi nguồn được đề nghị.
- **Sửa số liệu lùi:** "correct the data with a resubmission within 3 days"; lỗi > 10 MWh "resubmit
  corrected data… within 30 days" → sha256 của một cửa sổ gần đây có thể đổi trong 30 ngày → **mirror
  snapshot**; bài dự báo trực tiếp đánh dấu `truc_tiep`.

### OpenAQ
Nguồn: https://docs.openaq.org/using-the-api/api-key, …/rate-limits, https://api.openaq.org/openapi.json,
https://docs.openaq.org/aws/quick-start, https://docs.openaq.org/about/terms
- **[CHẠY]** v3 không key → 401; `/v2/locations` → **410** ("v1 and version 2 endpoints were retired
  on January 31, 2025"). Header `X-API-Key`; đăng ký https://explore.openaq.org/register.
- Giới hạn: "60 / minute", "2,000 / hour". `/v3/sensors/{id}/hours` dùng `datetime_from/to` nhưng
  `/days` dùng `date_from/to`; `meta.found` có thể là chuỗi ">1000" → phân trang theo số kết quả trang.
- Kho S3 `openaq-data-archive` tải HTTPS không cần AWS **[CHẠY]**; mỗi trạm mỗi ngày một `csv.gz`;
  `datetime` là giờ địa phương có offset.
- **Điều khoản:** "Attribution to OpenAQ as the source data is also required"; "OpenAQ users must
  therefore review and comply with any terms published by data providers"; **"Downloading data is
  strictly prohibited unless done through registered and authorized use."** Giấy phép từng nhà cung
  cấp ở `/v3/licenses` (`redistributionAllowed`…).
- **LỆCH LỚN:** trạm Đại sứ quán Mỹ (AirNow) Hà Nội/TP.HCM **ngừng từ 04/03/2025** (CREA 2025-05-21);
  tin 2026-09-15 nói đang khôi phục, chưa có thời hạn **[CHƯA XÁC MINH — chỉ thấy đoạn trích]**. Lộ
  trình buổi 10 ghi "trạm của Đại sứ quán Mỹ là US Public Domain" → **đã sửa lộ trình + todos**.

### Open-Meteo
Nguồn: https://open-meteo.com/en/terms, https://open-meteo.com/en/docs/historical-weather-api
- "The data obtained through the API is provided under the terms of the CC-BY 4.0 licence."
- Gói miễn phí **chỉ phi thương mại**; "600 calls / min", "5,000 calls / hour", "10,000 calls / day".
- **[CHẠY]** Hà Nội trả dữ liệu tới 2026-09-16; toạ độ bị bắt vào lưới (21.03 → 21.054); `time` không
  có offset → luôn đặt `timezone` tường minh. → **ghi rủi ro vào todos** (lớp thu phí).

## 6. Môi trường (cho `MOI-TRUONG.md`)

- uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`; `brew install uv`; cache "`$XDG_CACHE_HOME/uv`
  or `$HOME/.cache/uv` on Unix" (https://docs.astral.sh/uv/getting-started/installation/,
  https://docs.astral.sh/uv/concepts/cache/).
- WSL2 (https://learn.microsoft.com/en-us/windows/wsl/install, …/filesystems, …/wsl-config):
  "Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11"; `wsl --install`;
  "store your files in the WSL file system"; `.wslconfig` `memory` mặc định "50% of total memory on
  Windows"; áp dụng bằng `wsl --shutdown`.
- make trên macOS: Command Line Tools kèm GNU Make 3.81 (nguồn bên thứ ba, trang Apple không tải
  được **[CHƯA XÁC MINH từ Apple]**). Tính năng 3.82+/4.x (`.ONESHELL`, `!=`, `.RECIPEPREFIX`, `&:`)
  theo GNU make NEWS → **Makefile của buổi chỉ dùng cú pháp 3.81**.
- Kaggle token: https://www.kaggle.com/settings/api; `kaggle auth login` / `KAGGLE_API_TOKEN` /
  `~/.kaggle/access_token`; `kaggle.json` là cách cũ.
- EIA: https://www.eia.gov/opendata/register.php ("Your API key will be sent to your email address").
- Hugging Face: token chỉ cần để upload/gated; "Public repositories can be downloaded without authentication".
- Ollama v0.34.1: `curl -fsSL https://ollama.com/install.sh | sh` (Linux; trong WSL dùng lệnh Linux —
  suy ra, docs không nói về WSL); macOS cần "MacOS Sonoma (v14) or newer"; endpoint tương thích
  OpenAI `http://localhost:11434/v1/` (https://docs.ollama.com/api/openai-compatibility). Không tìm
  thấy hướng dẫn RAM chính thức → không ghi con số.
- llama.cpp: `brew install llama.cpp`, `winget install llama.cpp`, bản dựng sẵn trên GitHub Releases;
  `llama-server` nghe `127.0.0.1:8080`, có `/v1/chat/completions`.
- Docker Engine Ubuntu (https://docs.docker.com/engine/install/ubuntu/): hỗ trợ 26.04, 24.04, 22.04;
  nhóm `docker` "grants root-level privileges to the user"; Docker Desktop WSL cần WSL ≥ 2.1.5.
- weasyprint 70.0 trên Debian/Ubuntu: `apt install … libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
  libharfbuzz-subset0 …`; font `fonts-dejavu-core`, `fonts-liberation` (packages.ubuntu.com).
- python-dotenv 1.2.3: `load_dotenv()` "does not override existing environment variables by default";
  "add `.env` to your `.gitignore`". → `lay_du_lieu.py` tự đọc `.env` cùng quy tắc, không cần thư viện.

## 7–10. Nguồn cho Phụ lục A–E

Chi tiết trích dẫn nằm ngay trong từng phụ lục (mục "Nguồn"). Tóm tắt những gì **khác với hiểu biết
phổ biến** — đưa vào mục "Bẫy" của phụ lục:

- **pandas 3.0** (https://pandas.pydata.org/docs/whatsnew/v3.0.0.html): Copy-on-Write mặc định, gán
  chuỗi (`df["a"][mask] = v`) không còn tác dụng [CHẠY]; kiểu chuỗi `str` mặc định; parse chuỗi ngày
  mặc định **microsecond** (`datetime64[us]`) [CHẠY]; múi giờ dùng `zoneinfo`, pytz không còn là phụ
  thuộc; bí danh `H, T, S, M, Q, Y, A…` gây `ValueError` [CHẠY]; `fillna(method=)` bị gỡ; `groupby`
  `observed=True` mặc định; `pd.offsets.Day` là ngày lịch qua DST.
- DuckDB `fetchall()` cột TIMESTAMPTZ cần `pytz` — pandas 3 không còn kéo theo [CHẠY].
- `Asia/Ho_Chi_Minh` UTC+7 không DST **chỉ từ 1975-06-13** (tzdb `asia`).
- `np.quantile` mặc định `method="linear"` = Hyndman & Fan loại 7.
- Bootstrap i.i.d. trên AR(1) ρ = 0,7, n = 100: coverage thật **0,64** thay vì 0,95 [CHẠY, 300 lần lặp];
  `n_eff ≈ n(1−ρ)/(1+ρ)` khớp mô phỏng (ρ = 0,5: 67,4 so với 66,7).
- Gneiting (2011): sai số tuyệt đối phần trăm (MAPE) nhất quán với một "β-median", không phải trung vị.
- [CHẠY] statsmodels 0.15.0 `acf(..., alpha=)` báo FutureWarning: từ 0.16 hoặc sau 07/2027 sẽ trả `AcfResult` thay
  vì tuple — buổi 7 dùng `result_object=True` hoặc ghi rõ phiên bản.
- `statsmodels.plot_acf` mặc định `bartlett_confint=True` → dải rộng dần theo lag, **không** phải dải
  cố định ±1,96/√T của FPP [CHẠY].
- **`utilsforecast` 0.2.16:** sMAPE thang 0–1, MAPE là tỷ lệ (không ×100), `quantile_loss` không có
  hệ số 2 [CHẠY]. FPP: sMAPE thang 0–200, quantile score có hệ số 2.
- **`scoringrules` 0.11.0:** nhánh không-numba của `weighted_interval_score` cộng `w_median * median`
  thay vì `w_median * |obs − median|` (kiểm tay: 2,61 so với 1,41 theo công thức bài báo); nhánh numba
  đúng → Phase 1 đối chiếu WIS bằng công thức tự viết, không tin `scoringrules`.
- **`properscoring`:** bản cuối 0.1 (2015); GitHub "archived by the owner on Sep 4, 2026" → **sửa todos
  Phase 1** dùng `scoringrules` cho CRPS.
- FPP-Py 5.8 viết MAPE phạt nặng sai số **âm** (dự báo cao hơn thực tế); bản preprint Hyndman &
  Koehler (2005) viết "positive" → hai nguồn chữ khác nhau; phụ lục D chỉ trình bày lập luận toán
  học (sai số phần trăm bị chặn 100% khi dự báo thấp, không chặn khi dự báo cao) + Gneiting 2011.

## 11. Điểm lệch so với lộ trình / todos và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| **Hệ Nixtla + AutoGluon chưa hỗ trợ pandas 3** (statsforecast 2.1.1, utilsforecast 0.2.16, mlforecast 1.1.0: `pandas<3.0`; autogluon.timeseries 1.6.2: `pandas<2.4`, kéo torch 2.13.0) — [CHẠY] `uv pip compile` | **lớn** (buổi 14+) | Luật `[[rang_buoc]]` trong `tools/nen/phien-ban.toml` tự chốt pandas 2.3.3 (bản 2.x mới nhất, resolve được với numpy 2.5.3) cho buổi dùng các gói này; sửa lộ trình mục Môi trường lab + todos |
| Trạm Đại sứ quán Mỹ ngừng từ 04/03/2025 | **lớn** (buổi 10, DAGC1, đề C) | Sửa lộ trình buổi 10 + rủi ro trong todos; chọn trạm ở Phase 1/4 |
| OpenAQ cấm tải "unless… registered and authorized use", giấy phép theo nhà cung cấp | lớn | Mirror OpenAQ chỉ khi `redistributionAllowed`; rà Phase 1 |
| Open-Meteo free tier phi thương mại | vừa | Ghi rủi ro todos; Phase 1 quyết định snapshot/gói trả phí |
| `properscoring` archive | nhỏ | Sửa todos Phase 1 → `scoringrules` (kèm cảnh báo lỗi WIS) |
| UCI chậm, không Range | vừa | Bộ UCI > 10 MB bắt buộc mirror (rủi ro trong todos) |
| nbstripout không cần | nhỏ | gitignore `*.ipynb` trong buổi; kiểm bằng `kiem_tra_doc_lap.sh` |
| `--frozen` che lock cũ | nhỏ | học viên dùng `--frozen`; tác giả/CI chạy `uv lock --check` |
| uv mặc định Python 3.14 | nhỏ | chốt `==3.12.*` + `.python-version` trong mọi nền |
| ruff 0.16 bộ rule mặc định rộng | nhỏ | `select` tường minh trong `pyproject.toml` gốc |
| `kaggle.json` thành "legacy" | nhỏ | `MOI-TRUONG.md` hướng dẫn `kaggle auth login` / `KAGGLE_API_TOKEN` |
| Thêm `tools/nen/` (bảng phiên bản chung + cấu hình buổi `lab/nen.toml`) | thiết kế | Chống 44 `uv.lock` lệch nhau: mọi buổi chung phiên bản trực tiếp + chung `exclude-newer` |
