"""Dựng code/lab.ipynb (không output) từ một danh sách ô — dùng khi soạn notebook Lab của buổi.

    from nb import ghi
    ghi("buoi-01/code/lab.ipynb", [("md", "# ..."), ("py", "print(1)")])

Notebook là tệp phát cho học viên (mở bằng JupyterLab hoặc VS Code). Chỉ thư viện chuẩn.
"""
from __future__ import annotations

import json
from pathlib import Path

DAU = ("py", "# sửa tệp .py trong code/ thì các ô sau tự dùng bản mới, không cần khởi động lại\n"
             "%load_ext autoreload\n%autoreload 2")


def o(kieu: str, nguon: str) -> dict:
    dong = nguon.strip("\n").splitlines(keepends=True)
    if kieu == "md":
        return {"cell_type": "markdown", "metadata": {}, "source": dong}
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": dong}


def ghi(duong_dan: str | Path, cac_o: list[tuple[str, str]]) -> None:
    nb = {
        "cells": [o(*c) for c in [cac_o[0], DAU, *cac_o[1:]]],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 5,
    }
    for i, c in enumerate(nb["cells"]):
        c["id"] = f"o{i:02d}"
    Path(duong_dan).write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
