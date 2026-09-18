<!--SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/sinh_nen.py rồi chạy lại tool. -->
# Nền của buoi-12

Thư mục này **sinh tự động** — đừng sửa tay (sửa sẽ bị ghi đè và bị `kiem_tra_doc_lap.sh` chặn).

| Tệp | Vai trò |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | Python + thư viện chốt phiên bản; `uv sync --frozen` dựng lại y hệt |
| `du-lieu.toml` | URL, sha256, giấy phép, khoảng thời gian của từng bộ dữ liệu |
| `lay_du_lieu.py` | tải dữ liệu, kiểm sha256, cache ở `~/.cache/khoa-forecasting/` |
| `chuan-bi.sh` | `uv sync --frozen` + tải dữ liệu — `make up` gọi tệp này |
| `tv/` | thư viện trợ giúp, cài editable: `import tv` chạy từ mọi thư mục của buổi |

Dữ liệu được đặt ở `lab/du-lieu/raw/<bộ>/` (chỉ đọc, kèm `NGUON.txt` ghi nguồn và giấy phép).

| Bộ dữ liệu | Giấy phép | Nguồn |
|---|---|---|
| `uci-appliances-energy` | CC BY 4.0 | https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction |
