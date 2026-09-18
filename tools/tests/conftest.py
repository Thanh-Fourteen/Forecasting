"""Nạp tools/khung/ thành package `tv` — đúng tên mà các buổi học import sau khi sinh nền.

Chạy: python tools/kiem_khung.py   (chạy pytest ở cả hai hồ sơ pandas 3 và pandas 2.3.3 + Nixtla)
"""
import importlib.util
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

KHUNG = Path(__file__).resolve().parent.parent / "khung"

if "tv" not in sys.modules:
    spec = importlib.util.spec_from_file_location("tv", KHUNG / "__init__.py",
                                                  submodule_search_locations=[str(KHUNG)])
    tv = importlib.util.module_from_spec(spec)
    sys.modules["tv"] = tv
    spec.loader.exec_module(tv)
