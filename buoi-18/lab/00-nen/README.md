<!--SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/sinh_nen.py rồi chạy lại tool. -->
# Nền của buoi-18

Thư mục này **sinh tự động** — đừng sửa tay (sửa sẽ bị ghi đè và bị `kiem_tra_doc_lap.sh` chặn).

| Tệp | Vai trò |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | Python + thư viện chốt phiên bản; `uv sync --frozen` dựng lại y hệt |
| `du-lieu.toml` | URL, sha256, giấy phép, khoảng thời gian của từng bộ dữ liệu |
| `lay_du_lieu.py` | tải dữ liệu, kiểm sha256, cache ở `~/.cache/khoa-forecasting/` |
| `requirements.txt` | cùng phiên bản, xuất từ `uv.lock` cho người dùng conda/pip (`python lab.py up --pip`) |
| `tv/` | thư viện trợ giúp, cài editable: `import tv` chạy từ mọi thư mục của buổi |

Dữ liệu được đặt ở `lab/du-lieu/raw/<bộ>/` (chỉ đọc, kèm `NGUON.txt` ghi nguồn và giấy phép).

| Bộ dữ liệu | Giấy phép | Nguồn |
|---|---|---|
| `eia930-balance-2024-h1` | Public domain (U.S. government) | https://www.eia.gov/electricity/gridmonitor/ |
| `eia930-balance-2024-h2` | Public domain (U.S. government) | https://www.eia.gov/electricity/gridmonitor/ |
| `open-meteo-dallas-du-bao-luu-2024` | CC BY 4.0 | https://open-meteo.com/en/docs/previous-runs-api |
| `wikipedia-vi-tong` | CC0 1.0 | https://wikimedia.org/api/rest_v1/ |
| `eurostat-hanh-khach-hang-khong` | CC BY 4.0 (Eurostat) | https://ec.europa.eu/eurostat/databrowser/view/avia_paoc/default/table |
| `frb-g17-san-luong-cong-nghiep` | Public domain (Federal Reserve Board) | https://www.federalreserve.gov/datadownload/Choose.aspx?rel=G17 |
