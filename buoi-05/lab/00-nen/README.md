<!--SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/sinh_nen.py rồi chạy lại tool. -->
# Nền của buoi-05

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
| `census-marts-ban-le` | Public domain (U.S. government, 17 U.S.C. §105) | https://www.census.gov/retail/sales.html |
| `bls-cpi-u` | Public domain (U.S. government) | https://download.bls.gov/pub/time.series/cu/ |
| `bea-nipa-thang` | Public domain (U.S. government) | https://apps.bea.gov/national/Release/TXT/ |
| `bea-nipa-danh-muc-chuoi` | Public domain (U.S. government) | https://apps.bea.gov/national/Release/TXT/ |
