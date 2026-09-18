"""tv — thư viện trợ giúp của buổi học.

NGUỒN nằm ở tools/khung/ của repo khoá học; mỗi buổi có BẢN SAO ở lab/00-nen/tv/ (sinh bằng
tools/sinh_nen.py) và được cài editable vào venv của buổi, nên `import tv` chạy từ mọi thư mục
của buổi, kể cả trong JupyterLab. Không sửa tay bản sao.

Phase 1 thêm: ve.py, danh_gia.py, backtest.py, ro_ri.py, du_lieu.py.
"""
from pathlib import Path

THU_MUC_NEN = Path(__file__).resolve().parent.parent   # buoi-NN/lab/00-nen
THU_MUC_LAB = THU_MUC_NEN.parent                        # buoi-NN/lab
THU_MUC_BUOI = THU_MUC_LAB.parent                       # buoi-NN
THU_MUC_DU_LIEU = THU_MUC_LAB / "du-lieu" / "raw"       # nơi lay_du_lieu.py đặt dữ liệu đã kiểm sha256
