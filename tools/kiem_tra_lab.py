"""Chạy lab của mọi buổi như học viên: make down → up → check (dap-an, code) → down, in bảng kết quả.

    python tools/kiem_tra_lab.py                 mọi buoi-*/ có lab/Makefile
    python tools/kiem_tra_lab.py 7 13            chỉ các buổi này (cũng nhận buoi-00-thu, 4-8)
    python tools/kiem_tra_lab.py 7 --may-trang   cache uv + cache dữ liệu mới tinh trong thư mục tạm
                                                 (mô phỏng máy trắng; tải lại mọi thứ)
    python tools/kiem_tra_lab.py 7 --giu         không make down ở cuối (để xem lại môi trường)

Kỳ vọng mỗi buổi (Definition of Done trong CLAUDE.md):
    up                    thành công; < 10 phút khi đã có cache
    check BAI=dap-an      XANH
    check BAI=code        ĐỎ vì test hỏng (chỗ hở cố ý) — trừ buổi đặt [cham] code_phai_do = false
    check                 < 10 phút
    down                  thành công

Nhật ký đầy đủ từng bước: tools/nhat-ky-lab/<buoi>-<buoc>.log (gitignore).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NHAT_KY = GOC / "tools" / "nhat-ky-lab"
GIOI_HAN_GIAY = 600


def chon_buoi(tham_so: list[str]) -> list[Path]:
    if not tham_so:
        return sorted(p for p in GOC.glob("buoi-*") if (p / "lab" / "Makefile").is_file())
    ra: list[Path] = []
    for t in tham_so:
        if t.isdigit():
            ra.append(GOC / f"buoi-{int(t):02d}")
        elif m := re.fullmatch(r"(\d+)-(\d+)", t):
            ra += [GOC / f"buoi-{n:02d}" for n in range(int(m[1]), int(m[2]) + 1)
                   if (GOC / f"buoi-{n:02d}").is_dir()]
        else:
            ra.append(GOC / Path(t.rstrip("/")).name)
    return list(dict.fromkeys(ra))


def chay(buoi: Path, buoc: str, lenh: list[str], env: dict[str, str]) -> tuple[int, float, str]:
    bat_dau = time.monotonic()
    kq = subprocess.run(lenh, cwd=buoi / "lab", env=env, capture_output=True, text=True)
    giay = time.monotonic() - bat_dau
    ra = kq.stdout + kq.stderr
    NHAT_KY.mkdir(exist_ok=True)
    (NHAT_KY / f"{buoi.name}-{buoc}.log").write_text(f"$ {' '.join(lenh)}\n{ra}", encoding="utf-8")
    return kq.returncode, giay, ra


def do_do_test_hong(ra: str) -> bool:
    """pytest đỏ vì test HỎNG (có 'N failed', không có lỗi thu thập/lỗi chạy) — đúng kiểu chỗ hở cố ý."""
    tong_ket = [d for d in ra.splitlines() if re.search(r"\d+ (passed|failed|error)", d)]
    dong = tong_ket[-1] if tong_ket else ""
    return bool(re.search(r"\d+ failed", dong)) and not re.search(r"\d+ errors?", dong)


def phut(giay: float) -> str:
    return f"{giay / 60:.1f}′" if giay >= 60 else f"{giay:.0f}s"


def kiem_buoi(buoi: Path, env: dict[str, str], giu: bool) -> tuple[list[str], bool]:
    """Trả về (các ô của dòng bảng, đạt?)."""
    o: list[str] = []
    dat = True
    if not (buoi / "lab" / "Makefile").is_file():
        return ["thiếu lab/Makefile", "", "", "", ""], False

    code_phai_do = True
    nen = buoi / "lab" / "nen.toml"
    if nen.is_file():
        with open(nen, "rb") as f:
            code_phai_do = tomllib.load(f).get("cham", {}).get("code_phai_do", True)

    chay(buoi, "down-truoc", ["make", "down"], env)  # venv trắng

    ma, giay, ra = chay(buoi, "up", ["make", "up"], env)
    if ma:
        dong_loi = next((d for d in reversed(ra.splitlines()) if d.strip()), "")
        return [f"✗ {phut(giay)} — {dong_loi[:60]}", "—", "—", "—"], False
    o.append(f"✓ {phut(giay)}" + (" ⚠>10′" if giay > GIOI_HAN_GIAY else ""))

    if (buoi / "dap-an").is_dir():
        ma, giay, ra = chay(buoi, "check-dap-an", ["make", "check", "BAI=dap-an"], env)
        dat_dap_an = ma == 0
        dat &= dat_dap_an
        o.append(("✓ xanh " if dat_dap_an else "✗ đỏ ") + phut(giay)
                 + (" ⚠>10′" if giay > GIOI_HAN_GIAY else ""))
        dat &= giay <= GIOI_HAN_GIAY
    else:
        o.append("— (không có dap-an/)")

    if (buoi / "code").is_dir():
        ma, giay, ra = chay(buoi, "check-code", ["make", "check", "BAI=code"], env)
        if code_phai_do:
            dung = ma != 0 and do_do_test_hong(ra)
            o.append(("✓ đỏ đúng " if dung else ("✗ XANH — chỗ hở đã bị sửa? " if ma == 0
                                                 else "✗ lỗi chạy, không phải test hỏng ")) + phut(giay))
        else:
            dung = ma == 0
            o.append(("✓ xanh " if dung else "✗ đỏ ") + phut(giay))
        dat &= dung
    else:
        o.append("— (không có code/)")

    if giu:
        o.append("giữ")
    else:
        ma, giay, _ = chay(buoi, "down", ["make", "down"], env)
        o.append("✓" if ma == 0 else "✗")
        dat &= ma == 0
    return o, dat


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("buoi", nargs="*")
    ap.add_argument("--may-trang", action="store_true", help="cache uv + dữ liệu mới trong thư mục tạm")
    ap.add_argument("--giu", action="store_true", help="không make down ở cuối")
    t = ap.parse_args(argv)

    cac_buoi = chon_buoi(t.buoi)
    if not cac_buoi:
        print("(chưa có buổi nào có lab/Makefile)")
        return 0
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    tam = None
    if t.may_trang:
        tam = tempfile.TemporaryDirectory(prefix="khoa-forecasting-may-trang-")
        env["UV_CACHE_DIR"] = f"{tam.name}/uv"
        env["KHOA_FORECASTING_CACHE"] = f"{tam.name}/du-lieu"
        print(f"Máy trắng mô phỏng: cache tạm {tam.name}")

    tieu_de = ["buổi", "make up", "check dap-an", "check code", "down", "tổng"]
    print("| " + " | ".join(tieu_de) + " |\n|" + "---|" * len(tieu_de), flush=True)
    that_bai = 0
    for buoi in cac_buoi:
        bat_dau = time.monotonic()
        o, dat = kiem_buoi(buoi, env, t.giu)
        that_bai += not dat
        print(f"| {buoi.name} | " + " | ".join(o) + f" | {'✓' if dat else '✗'} "
              f"{phut(time.monotonic() - bat_dau)} |", flush=True)
    print(f"\nNhật ký: {NHAT_KY.relative_to(GOC)}/")
    if tam:
        tam.cleanup()
    if that_bai:
        print(f"KHÔNG ĐẠT: {that_bai}/{len(cac_buoi)} buổi")
        return 1
    print(f"ĐẠT: {len(cac_buoi)} buổi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
