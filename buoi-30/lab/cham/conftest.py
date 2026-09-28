"""Hạ tầng chung của bộ chấm — `python lab.py check` chạy pytest trên thư mục cham/.

    BAI=code    (mặc định) chấm bài của học viên trong code/
    BAI=dap-an  chấm bản đáp án (`python lab.py check --dap-an`) (tác giả; thư mục này không có trong zip phát học viên)

Quy ước để chấm được: mỗi tệp trong code/ chỉ ĐỊNH NGHĨA hàm ở mức module; phần chạy thử đặt
trong `if __name__ == "__main__":` hoặc trong ô notebook — nạp module không được tốn thời gian.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

LAB = Path(__file__).resolve().parent.parent
BUOI = LAB.parent
DU_LIEU = LAB / "du-lieu" / "raw"


@pytest.fixture(scope="session")
def bai() -> Path:
    """Thư mục đang được chấm."""
    thu_muc = BUOI / os.environ.get("BAI", "code")
    if not thu_muc.is_dir():
        pytest.exit(f"không có thư mục {thu_muc} để chấm", returncode=2)
    return thu_muc


@pytest.fixture(scope="session")
def nap(bai: Path):
    """nap("ten_tep") -> module code/ten_tep.py (hoặc dap-an/ten_tep.py khi BAI=dap-an)."""
    da_nap: dict[str, object] = {}

    def _nap(ten: str):
        if ten not in da_nap:
            duong_dan = bai / f"{ten}.py"
            if not duong_dan.is_file():
                pytest.fail(f"thiếu {duong_dan.relative_to(BUOI)}")
            spec = importlib.util.spec_from_file_location(f"bai.{ten}", duong_dan)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            da_nap[ten] = module
        return da_nap[ten]

    return _nap


@pytest.fixture(scope="session")
def du_lieu() -> Path:
    """lab/du-lieu/raw/ — dữ liệu đã kiểm sha256 bởi `python lab.py up`."""
    if not DU_LIEU.is_dir():
        pytest.exit("chưa có dữ liệu — chạy: python lab.py up", returncode=2)
    return DU_LIEU
