<!--SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/sinh_nen.py rồi chạy lại tool. -->
# Nền của buoi-21

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
| `frb-h10-ty-gia` | Public domain (Federal Reserve Board) | https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H10 |
| `binance-btcusdt-1h-2023-01` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-02` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-03` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-04` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-05` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-06` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-07` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-08` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-09` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-10` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-11` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2023-12` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-01` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-02` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-03` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-04` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-05` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-06` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-07` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-08` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-09` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-10` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-11` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
| `binance-btcusdt-1h-2024-12` | Không có giấy phép dữ liệu; Điều khoản Binance hạn chế dùng thương mại dữ liệu thị trường | https://data.binance.vision/ |
