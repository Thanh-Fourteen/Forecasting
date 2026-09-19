<!--SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/sinh_nen.py rồi chạy lại tool. -->
# Nền của buoi-20

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
| `philly-fed-gdp-thuc-vintage-thang` | Điều khoản Philadelphia Fed — chỉ cho mục đích thông tin, giáo dục, nghiên cứu | https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists |
| `philly-fed-viec-lam-vintage` | Điều khoản Philadelphia Fed — chỉ cho mục đích thông tin, giáo dục, nghiên cứu | https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists |
| `philly-fed-san-luong-cn-vintage` | Điều khoản Philadelphia Fed — chỉ cho mục đích thông tin, giáo dục, nghiên cứu | https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists |
| `philly-fed-nha-khoi-cong-vintage` | Điều khoản Philadelphia Fed — chỉ cho mục đích thông tin, giáo dục, nghiên cứu | https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists |
| `eia-gia-dau-wti` | Public domain (U.S. government) | https://www.eia.gov/dnav/pet/hist/RWTCD.htm |
| `eia-gia-xang-ny-harbor` | Public domain (U.S. government) | https://www.eia.gov/dnav/pet/hist/EER_EPMRU_PF4_Y35NY_DPGD.htm |
