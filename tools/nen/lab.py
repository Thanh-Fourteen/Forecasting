#!/usr/bin/env python3
"""Lab của buổi. Đứng trong thư mục lab/ rồi chạy:

    python lab.py up            dựng môi trường bằng uv + tải dữ liệu, kiểm sha256
    python lab.py up --pip      dùng Python đang bật (conda, venv riêng): pip install rồi tải dữ liệu
    python lab.py check         chấm bài trong code/        (--dap-an: chấm bản đáp án)
    python lab.py chay TỆP      chạy một tệp .py bằng Python của buổi
    python lab.py notebook      mở JupyterLab ở thư mục code/
    python lab.py down          xoá môi trường + dữ liệu của buổi (cache tải về vẫn giữ)

Chỉ dùng thư viện chuẩn: chạy được bằng mọi Python 3.9+ trên Linux, macOS, Windows.
Máy chưa có Python: `uv run --no-project lab.py up`.
"""
from __future__ import annotations

import functools
import os
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
NEN = LAB / "00-nen"
VENV = NEN / ".venv"
print = functools.partial(print, flush=True)  # noqa: A001 — in theo đúng thứ tự với lệnh con


def python_venv() -> Path:
    return VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def python_cua_buoi() -> str:
    """Python có đủ thư viện của buổi: venv do uv dựng, nếu không có thì Python đang chạy (cách --pip)."""
    if python_venv().is_file():
        return str(python_venv())
    return sys.executable


def chay(lenh: list[str], **kw) -> int:
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}  # venv đang bật nơi khác làm uv cảnh báo
    # thư mục bin của Python được dùng đứng đầu PATH: `jupyter …` gọi lệnh con qua PATH, không được lấy nhầm bản khác
    env["PATH"] = str(Path(lenh[0]).parent) + os.pathsep + env.get("PATH", "")
    env.update(kw.pop("env", {}))
    return subprocess.call(lenh, env=env, **kw)


def up(tham_so: list[str]) -> int:
    dung_pip = "--pip" in tham_so
    them = [t for t in tham_so if t != "--pip"]
    if dung_pip:
        print(f"==> Cài thư viện vào Python đang dùng: {sys.executable}")
        ma = chay([sys.executable, "-m", "pip", "install", "-r", str(NEN / "requirements.txt"), "-e", str(NEN)])
        py = sys.executable
    else:
        if not shutil.which("uv"):
            print("✗ Chưa có uv. Cài: https://docs.astral.sh/uv/getting-started/installation/\n"
                  "  Hoặc dùng conda/venv của bạn: bật môi trường Python 3.12 rồi chạy  python lab.py up --pip",
                  file=sys.stderr)
            return 1
        print("==> Môi trường Python theo uv.lock (uv sync --frozen)")
        ma = chay(["uv", "sync", "--frozen", "--project", str(NEN)])
        py = str(python_venv())
    if ma:
        return ma
    print("==> Dữ liệu (tải hoặc lấy từ cache, kiểm sha256)")
    ma = chay([py, str(NEN / "lay_du_lieu.py"), str(NEN / "du-lieu.toml"), *them])
    if not ma:
        print("==> Xong. Tiếp theo:  python lab.py check")
    return ma


def check(tham_so: list[str]) -> int:
    bai = "dap-an" if "--dap-an" in tham_so else "code"
    return chay([python_cua_buoi(), "-m", "pytest", "-q", "-p", "no:cacheprovider", "cham"],
                cwd=LAB, env={"BAI": bai})


def chay_tep(tham_so: list[str]) -> int:
    if not tham_so:
        print("cần tên tệp, ví dụ:  python lab.py chay ../code/kiem_tra_moi_truong.py", file=sys.stderr)
        return 2
    return chay([python_cua_buoi(), *tham_so])


def notebook(_: list[str]) -> int:
    return chay([python_cua_buoi(), "-m", "jupyter", "lab", f"--ServerApp.root_dir={LAB.parent / 'code'}"])


def down(_: list[str]) -> int:
    for p in [VENV, LAB / "du-lieu" / "raw", LAB / ".pytest_cache"]:
        shutil.rmtree(p, ignore_errors=True)
    for goc in [LAB, LAB.parent / "code", LAB.parent / "dap-an"]:
        for p in goc.rglob("__pycache__") if goc.is_dir() else []:
            shutil.rmtree(p, ignore_errors=True)
    print("==> Đã xoá môi trường và dữ liệu của buổi (cache tải về vẫn giữ)")
    return 0


LENH = {"up": up, "check": check, "chay": chay_tep, "notebook": notebook, "down": down}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in LENH:
        print(__doc__)
        sys.exit(2)
    sys.exit(LENH[sys.argv[1]](sys.argv[2:]))
