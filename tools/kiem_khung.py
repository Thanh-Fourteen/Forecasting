"""Chạy test của tools/khung/ ở các hồ sơ phiên bản mà buổi học thật sẽ dùng.

    python tools/kiem_khung.py              cả hai hồ sơ
    python tools/kiem_khung.py pandas3      chỉ một hồ sơ
    python tools/kiem_khung.py -- -k ro_ri  tham số sau -- chuyển cho pytest

Hồ sơ lấy phiên bản từ tools/nen/phien-ban.toml (kể cả [[rang_buoc]]) nên khớp đúng môi trường
mà sinh_nen.py dựng cho buổi:
    pandas3   buổi 1–13: pandas 3, không có Nixtla
    nixtla    buổi dùng statsforecast/utilsforecast: pandas bị chốt 2.3.3; có utilsforecast và
              scoringrules để test đối chiếu số với thư viện chuẩn
Môi trường tạo tạm bằng `uv run --isolated`, không đụng venv nào.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sinh_nen import chuan_ten  # noqa: E402

HO_SO = {
    "pandas3": ["numpy", "pandas", "scipy", "matplotlib", "scikit-learn", "pytest"],
    "nixtla": ["numpy", "pandas", "scipy", "matplotlib", "scikit-learn", "pytest", "utilsforecast", "scoringrules"],
}


def ghim(goi: list[str], pb: dict) -> list[str]:
    bang = {chuan_ten(k): (k, v) for k, v in pb["thu_vien"].items()}
    dung = {chuan_ten(g) for g in goi}
    ep = {}
    for rb in pb.get("rang_buoc", []):
        if dung & {chuan_ten(g) for g in rb["khi_dung"]}:
            ep.update({chuan_ten(k): v for k, v in rb["dat"].items()})
    ra = []
    for g in goi:
        ten, phien_ban = bang[chuan_ten(g)]
        ra.append(f"{ten}=={ep.get(chuan_ten(g), phien_ban)}")
    return ra


def main(argv: list[str]) -> int:
    them = argv[argv.index("--") + 1:] if "--" in argv else []
    chon = [a for a in (argv[:argv.index("--")] if "--" in argv else argv)] or list(HO_SO)
    with open(HERE / "nen" / "phien-ban.toml", "rb") as f:
        pb = tomllib.load(f)
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    that_bai = []
    for ten in chon:
        goi = ghim(HO_SO[ten], pb)
        print(f"==> hồ sơ {ten}: {' '.join(goi)}", flush=True)
        lenh = ["uv", "run", "--isolated", "--no-project", "--python", pb["python"],
                "--exclude-newer", pb["exclude_newer"]]
        for g in goi:
            lenh += ["--with", g]
        lenh += ["python", "-m", "pytest", str(HERE / "tests"), "-q", "-p", "no:cacheprovider", *them]
        if subprocess.run(lenh, env=env).returncode:
            that_bai.append(ten)
    if that_bai:
        print(f"\nKHÔNG ĐẠT ở hồ sơ: {', '.join(that_bai)}")
        return 1
    print(f"\nĐẠT ở mọi hồ sơ: {', '.join(chon)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
