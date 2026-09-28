"""Môi trường DÙNG CHUNG cho notebook tự học (buoi-NN/tu-hoc.ipynb) — thay cho một venv mỗi buổi.

    python tools/tu_hoc/moi_truong.py 1 5 14     dựng/cập nhật môi trường cho các buổi này
    python tools/tu_hoc/moi_truong.py --liet-ke  buổi nào dùng hồ sơ nào, hồ sơ nào đã dựng

Các buổi chỉ khác nhau ở phiên bản khi dính một [[rang_buoc]] của tools/nen/phien-ban.toml, nên
chỉ cần vài HỒ SƠ, mỗi hồ sơ một venv + một Jupyter kernel:
    pandas3    buổi không dùng Nixtla/AutoGluon (pandas 3)
    nixtla     buổi dùng statsforecast/utilsforecast/mlforecast (pandas chốt 2.3.3)
    autogluon  buổi dùng autogluon.timeseries (thêm các chốt riêng của nó)
Phiên bản lấy đúng từ bảng chung (kể cả ràng buộc) + cùng mốc exclude-newer, nên số chạy ra khớp venv
của lab. Venv nằm ở cache ngoài repo: ~/.cache/khoa-forecasting/tu-hoc/<hồ sơ>/ (đổi bằng
$KHOA_FORECASTING_CACHE). Mỗi lần chạy cài HỢP thư viện của mọi buổi đã yêu cầu cho hồ sơ đó
(ghi trong buoi.txt), nên thêm buổi không làm lệch buổi cũ.

Kernel đăng ký tên `khoa-tu-hoc-<hồ sơ>`; notebook tự học ghi sẵn tên này nên VS Code/JupyterLab tự chọn.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tomllib
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "tools"))
from sinh_nen import chuan_ten  # noqa: E402

LUON_CO = ["numpy", "pandas", "matplotlib", "jupyterlab", "ipykernel", "tzdata"]


def phien_ban() -> dict:
    with open(GOC / "tools" / "nen" / "phien-ban.toml", "rb") as f:
        return tomllib.load(f)


def thu_vien_buoi(n: int) -> list[str]:
    p = GOC / f"buoi-{n:02d}" / "lab" / "nen.toml"
    with open(p, "rb") as f:
        return list(tomllib.load(f).get("thu_vien", []))


def rang_buoc_dinh(goi: list[str], pb: dict) -> list[dict]:
    dung = {chuan_ten(g) for g in goi}
    return [rb for rb in pb.get("rang_buoc", []) if dung & {chuan_ten(g) for g in rb["khi_dung"]}]


def ho_so(n: int, pb: dict | None = None) -> str:
    pb = pb or phien_ban()
    goi = thu_vien_buoi(n)
    if chuan_ten("autogluon.timeseries") in {chuan_ten(g) for g in goi}:
        return "autogluon"
    return "nixtla" if rang_buoc_dinh(goi, pb) else "pandas3"


def ten_kernel(hs: str) -> str:
    return f"khoa-tu-hoc-{hs}"


def thu_muc(hs: str) -> Path:
    goc = os.environ.get("KHOA_FORECASTING_CACHE") or Path.home() / ".cache" / "khoa-forecasting"
    return Path(goc) / "tu-hoc" / hs


def python_cua(hs: str) -> Path:
    return thu_muc(hs) / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ghim(goi: list[str], pb: dict) -> list[str]:
    bang = {chuan_ten(k): (k, v) for k, v in pb["thu_vien"].items()}
    ep: dict[str, str] = {}
    for rb in rang_buoc_dinh(goi, pb):
        ep.update({chuan_ten(k): v for k, v in rb["dat"].items()})
    ra = [f"{bang[chuan_ten(g)][0]}=={ep.get(chuan_ten(g), bang[chuan_ten(g)][1])}"
          for g in dict.fromkeys(goi)]
    # ràng buộc cũng chốt cả gói không khai trực tiếp (vd coreforecast, numpy của AutoGluon)
    co = {chuan_ten(g) for g in goi}
    ra += [f"{k}=={v}" for k, v in ep.items() if k not in co]
    return ra


def dung(cac_buoi: list[int]) -> None:
    pb = phien_ban()
    theo_ho_so: dict[str, list[int]] = {}
    for n in cac_buoi:
        theo_ho_so.setdefault(ho_so(n, pb), []).append(n)
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    for hs, ds in theo_ho_so.items():
        tm = thu_muc(hs)
        tm.mkdir(parents=True, exist_ok=True)
        so_ghi = tm / "buoi.txt"
        da_co = {int(x) for x in so_ghi.read_text().split()} if so_ghi.is_file() else set()
        tat_ca = sorted(da_co | set(ds))
        goi = LUON_CO + [g for n in tat_ca for g in thu_vien_buoi(n)]
        pins = ghim(goi, pb)
        print(f"==> hồ sơ {hs} (buổi {', '.join(map(str, tat_ca))}): {tm}", flush=True)
        if not python_cua(hs).is_file():
            subprocess.run(["uv", "venv", "--python", pb["python"], str(tm / ".venv")], check=True, env=env)
        lenh = ["uv", "pip", "install", "--python", str(python_cua(hs)), "--exclude-newer", pb["exclude_newer"]]
        if any(p.startswith("torch==") for p in pins):
            lenh += ["--torch-backend", "cpu"]
        subprocess.run([*lenh, *pins], check=True, env=env)
        subprocess.run([str(python_cua(hs)), "-m", "ipykernel", "install", "--user", "--name", ten_kernel(hs),
                        "--display-name", f"Khoá Forecasting · tự học ({hs})"], check=True, env=env)
        so_ghi.write_text(" ".join(map(str, tat_ca)) + "\n")
        print(f"✓ kernel {ten_kernel(hs)} → {python_cua(hs)}")


def liet_ke() -> None:
    pb = phien_ban()
    buoi = sorted(int(p.parent.parent.name[5:]) for p in GOC.glob("buoi-*/lab/nen.toml"))
    theo: dict[str, list[int]] = {}
    for n in buoi:
        theo.setdefault(ho_so(n, pb), []).append(n)
    for hs, ds in theo.items():
        trang_thai = "đã dựng" if python_cua(hs).is_file() else "chưa dựng"
        print(f"{hs:<10} {trang_thai:<10} buổi {', '.join(map(str, ds))}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("buoi", nargs="*", type=int)
    ap.add_argument("--liet-ke", action="store_true")
    a = ap.parse_args(argv)
    if a.liet_ke or not a.buoi:
        liet_ke()
        return 0
    dung(a.buoi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
