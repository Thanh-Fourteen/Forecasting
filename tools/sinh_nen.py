"""Sinh nền `buoi-NN/lab/00-nen/` cho một buổi hoặc một dải buổi.

    python tools/sinh_nen.py 7               # buoi-07
    python tools/sinh_nen.py 4-8 13          # buoi-04..08 và buoi-13 (bỏ qua buổi chưa có thư mục)
    python tools/sinh_nen.py buoi-00-thu     # tên thư mục bất kỳ bắt đầu bằng buoi-
    python tools/sinh_nen.py --tat-ca        # mọi buoi-*/ có lab/nen.toml
    python tools/sinh_nen.py --kiem 7        # KHÔNG ghi: báo nền lệch nguồn (dùng trong kiem_tra_doc_lap.sh)
    python tools/sinh_nen.py 7 --nang-cap    # uv lock --upgrade (sau khi đổi tools/nen/phien-ban.toml)
    python tools/sinh_nen.py 7 --khong-lock  # bỏ bước uv lock (máy không mạng; lock phải chạy sau)

Đầu vào (tác giả viết tay):
    buoi-NN/lab/nen.toml             buổi cần thư viện nào, bộ dữ liệu nào (khuôn: tools/khuon-buoi/)
    tools/nen/phien-ban.toml         phiên bản CHUNG của mọi thư viện + mốc exclude-newer
    tools/du-lieu/danh-muc.toml      URL + sha256 + giấy phép của mọi bộ dữ liệu
    tools/khung/*.py                 thư viện trợ giúp → copy thành tv/
    tools/lay_du_lieu.py             bộ tải dữ liệu → copy vào nền

Đầu ra (SINH RA — không sửa tay; sửa nguồn rồi chạy lại):
    buoi-NN/lab/00-nen/
        pyproject.toml   .python-version   uv.lock
        du-lieu.toml     lay_du_lieu.py    chuan-bi.sh
        tv/              README.md         .dau-van-tay.json   (sha256 mọi tệp sinh ra)

Sau khi sinh, buổi KHÔNG còn phụ thuộc gì vào tools/: copy riêng thư mục buổi sang máy khác vẫn
`make up` được.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOC = HERE.parent
sys.path.insert(0, str(HERE))
from lay_du_lieu import kiem_bo  # noqa: E402  (tools/ không phải package)

PHIEN_BAN = HERE / "nen" / "phien-ban.toml"
DANH_MUC = HERE / "du-lieu" / "danh-muc.toml"
KHUNG = HERE / "khung"
LAY_DU_LIEU = HERE / "lay_du_lieu.py"

DAU_SINH = "SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa {nguon} rồi chạy lại tool."
TEP_VAN_TAY = ".dau-van-tay.json"


class LoiNen(Exception):
    pass


# ---------------------------------------------------------------------------- chọn buổi


def chon_buoi(tham_so: list[str], tat_ca: bool) -> list[Path]:
    if tat_ca:
        return sorted(p for p in GOC.glob("buoi-*") if (p / "lab" / "nen.toml").is_file())
    ra: list[Path] = []
    for t in tham_so:
        if re.fullmatch(r"\d+", t):
            ra.append(GOC / f"buoi-{int(t):02d}")
        elif m := re.fullmatch(r"(\d+)-(\d+)", t):
            for n in range(int(m.group(1)), int(m.group(2)) + 1):
                if (GOC / f"buoi-{n:02d}").is_dir():
                    ra.append(GOC / f"buoi-{n:02d}")
        elif t.rstrip("/").split("/")[-1].startswith("buoi-"):
            ra.append(GOC / t.rstrip("/").split("/")[-1])
        else:
            raise LoiNen(f"không hiểu '{t}' — dùng 7, 4-8, buoi-00-thu hoặc --tat-ca")
    return list(dict.fromkeys(ra))


# ---------------------------------------------------------------------------- đọc nguồn


def doc_toml(p: Path) -> dict:
    try:
        with open(p, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError as loi:
        raise LoiNen(f"thiếu {p.relative_to(GOC)}") from loi
    except tomllib.TOMLDecodeError as loi:
        raise LoiNen(f"{p.relative_to(GOC)} sai cú pháp TOML: {loi}") from loi


def chuan_ten(ten: str) -> str:
    """Tên gói theo PEP 503 để so khớp (PyWavelets ~ pywavelets, autogluon.timeseries ~ autogluon-timeseries)."""
    return re.sub(r"[-_.]+", "-", ten).lower()


def ten_buoi(thu_muc: Path) -> str:
    return thu_muc.name  # buoi-07


# ---------------------------------------------------------------------------- dựng nội dung


def dung_pyproject(buoi: Path, cau_hinh: dict, pb: dict, cac_bo: list[dict]) -> str:
    bang = {chuan_ten(k): (k, v) for k, v in pb["thu_vien"].items()}
    ghi_de = {chuan_ten(k): v for k, v in cau_hinh.get("ghi_de", {}).items()}
    for ten, gd in ghi_de.items():
        if not isinstance(gd, dict) or not gd.get("phien_ban") or not gd.get("ly_do"):
            raise LoiNen(f"[ghi_de.{ten}] cần phien_ban và ly_do")

    thu_vien = list(dict.fromkeys(cau_hinh.get("thu_vien", []) + pb.get("luon_co", {}).get("goi", [])))
    if any(b["kieu"] == "kaggle" for b in cac_bo):
        thu_vien.append("kagglehub")
    ten_trong_buoi = {chuan_ten(t) for t in thu_vien}

    # [[rang_buoc]] của bảng chung: buổi dùng gói bị chặn phiên bản → ép phiên bản tương thích
    ep: dict[str, str] = {}
    for rb in pb.get("rang_buoc", []):
        if ten_trong_buoi & {chuan_ten(g) for g in rb["khi_dung"]}:
            for goi, phien_ban in rb["dat"].items():
                ep[chuan_ten(goi)] = phien_ban

    def ghim(ten: str) -> str:
        khoa = chuan_ten(ten)
        if khoa in ghi_de:
            return f"{bang.get(khoa, (ten,))[0]}=={ghi_de[khoa]['phien_ban']}"
        if khoa in ep:
            return f"{bang.get(khoa, (ten,))[0]}=={ep[khoa]}"
        if khoa not in bang:
            raise LoiNen(f"thư viện '{ten}' chưa có trong tools/nen/phien-ban.toml [thu_vien] — "
                         "xác minh phiên bản (PyPI + changelog) rồi thêm vào bảng chung")
        goc, phien_ban = bang[khoa]
        return f"{goc}=={phien_ban}"

    thu_vien = list(dict.fromkeys(thu_vien))
    phu_thuoc = sorted((ghim(t) for t in thu_vien), key=str.lower)
    nhom = {ten: sorted((ghim(t) for t in ds), key=str.lower) for ten, ds in pb["nhom"].items()}

    def mang(ds: list[str], thut: str = "    ") -> str:
        if not ds:
            return "[]"
        return "[\n" + "".join(f'{thut}"{x}",\n' for x in ds) + "]"

    py = pb["python"]
    dong = [
        f"# {DAU_SINH.format(nguon=f'{ten_buoi(buoi)}/lab/nen.toml hoặc tools/nen/phien-ban.toml')}",
        "",
        "[project]",
        f'name = "{ten_buoi(buoi)}-nen"',
        'version = "0.0.0"',
        f'description = "Môi trường chốt phiên bản của {ten_buoi(buoi)} (thư viện trợ giúp: tv/)"',
        f'requires-python = "=={py}.*"',
        f"dependencies = {mang(phu_thuoc)}",
        "",
        "[dependency-groups]",
    ]
    dong += [f"{ten} = {mang(ds)}" for ten, ds in nhom.items()]
    dong += [
        "",
        "[build-system]",
        f'requires = ["uv_build{pb["uv_build"]}"]',
        'build-backend = "uv_build"',
        "",
        "[tool.uv]",
        f'exclude-newer = "{pb["exclude_newer"]}"',
        *([f"constraint-dependencies = {mang(sorted(ghim(g) for g in ep if g not in ten_trong_buoi and g not in ghi_de))}"]
          if any(g not in ten_trong_buoi and g not in ghi_de for g in ep) else []),
        "default-groups = [" + ", ".join(f'"{t}"' for t in nhom) + "]",
        "",
        "[tool.uv.build-backend]",
        'module-name = "tv"',
        'module-root = ""',
    ]
    # index riêng (vd torch CPU): chỉ khai khi buổi dùng gói của index đó; explicit = chỉ cho gói đó
    nguon: list[str] = []
    for ten_index, idx in pb.get("index", {}).items():
        goi = [g for g in idx["goi"] if chuan_ten(g) in ten_trong_buoi]
        if goi:
            dong += ["", "[[tool.uv.index]]", f'name = "{ten_index}"', f'url = "{idx["url"]}"',
                     "explicit = true"]
            nguon += [f'{g} = [{{ index = "{ten_index}" }}]' for g in goi]
    if nguon:
        dong += ["", "[tool.uv.sources]", *nguon]
    return "\n".join(dong) + "\n"


def lay_bo(cau_hinh: dict, danh_muc: dict) -> list[dict]:
    cac_bo, van_de = [], []
    for ten in cau_hinh.get("du_lieu", []):
        if ten not in danh_muc.get("bo", {}):
            van_de.append(f"bộ dữ liệu '{ten}' không có trong tools/du-lieu/danh-muc.toml")
            continue
        bo = {"ten": ten, **danh_muc["bo"][ten]}
        van_de += kiem_bo(bo)
        if bo.get("cho_sha256"):
            van_de.append(f"bộ '{ten}' chưa chốt sha256 ({bo['cho_sha256']}) — tải bằng "
                          "lay_du_lieu.py --tac-gia rồi ghi tep_sha256/sha256 vào danh mục trước khi dùng")
        cac_bo.append(bo)
    if van_de:
        raise LoiNen("danh mục dữ liệu chưa đạt:\n    - " + "\n    - ".join(van_de))
    return cac_bo


def toml_gia_tri(v: object) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ", ".join(toml_gia_tri(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{json.dumps(k, ensure_ascii=False)} = {toml_gia_tri(x)}"
                                for k, x in v.items()) + " }"
    raise LoiNen(f"không ghi được giá trị TOML kiểu {type(v).__name__}")


def dung_du_lieu_toml(buoi: Path, cac_bo: list[dict]) -> str:
    dong = [f"# {DAU_SINH.format(nguon='tools/du-lieu/danh-muc.toml')}",
            f"# Dữ liệu của {ten_buoi(buoi)}: tải + kiểm sha256 bằng `bash 00-nen/chuan-bi.sh` (make up).",
            "", "phien_ban = 1"]
    bo_qua = {"buoi", "xac_minh"}  # chỉ để tra cứu trong danh mục
    for bo in cac_bo:
        dong += ["", "[[bo]]"]
        dong += [f"{k} = {toml_gia_tri(v)}" for k, v in bo.items() if k not in bo_qua]
    return "\n".join(dong) + "\n"


def dung_chuan_bi(buoi: Path) -> str:
    return f"""#!/usr/bin/env bash
# {DAU_SINH.format(nguon='tools/sinh_nen.py')}
# Dựng nền của {ten_buoi(buoi)}: môi trường Python chốt phiên bản + dữ liệu đã kiểm sha256.
#     bash lab/00-nen/chuan-bi.sh [--tom-tat]        (make up gọi lệnh này)
set -euo pipefail
NEN="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
unset VIRTUAL_ENV  # venv đang bật ở nơi khác sẽ bị uv bỏ qua kèm cảnh báo — gỡ cho gọn

if ! command -v uv >/dev/null 2>&1; then
    echo "✗ Chưa có uv. Cài:  curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    echo "  (hướng dẫn: https://docs.astral.sh/uv/getting-started/installation/)" >&2
    exit 1
fi

echo "==> Môi trường Python theo uv.lock (uv sync --frozen)"
uv sync --frozen --project "$NEN"

echo "==> Dữ liệu (tải hoặc lấy từ cache, kiểm sha256)"
uv run --no-sync --project "$NEN" python "$NEN/lay_du_lieu.py" "$NEN/du-lieu.toml" "$@"

echo "==> Xong nền {ten_buoi(buoi)}"
"""


def dung_readme(buoi: Path, cac_bo: list[dict]) -> str:
    bo = "\n".join(f"| `{b['ten']}` | {b.get('giay_phep', '')} | {b.get('trang_nguon', '')} |"
                   for b in cac_bo) or "| — | | |"
    return f"""<!--{DAU_SINH.format(nguon='tools/sinh_nen.py')} -->
# Nền của {ten_buoi(buoi)}

Thư mục này **sinh tự động** — đừng sửa tay (sửa sẽ bị ghi đè và bị `kiem_tra_doc_lap.sh` chặn).

| Tệp | Vai trò |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | Python + thư viện chốt phiên bản; `uv sync --frozen` dựng lại y hệt |
| `du-lieu.toml` | URL, sha256, giấy phép, khoảng thời gian của từng bộ dữ liệu |
| `lay_du_lieu.py` | tải dữ liệu, kiểm sha256, cache ở `~/.cache/khoa-forecasting/` |
| `chuan-bi.sh` | `uv sync --frozen` + tải dữ liệu — `make up` gọi tệp này |
| `tv/` | thư viện trợ giúp, cài editable: `import tv` chạy từ mọi thư mục của buổi |

Dữ liệu được đặt ở `lab/du-lieu/raw/<bộ>/` (chỉ đọc, kèm `NGUON.txt` ghi nguồn và giấy phép).

| Bộ dữ liệu | Giấy phép | Nguồn |
|---|---|---|
{bo}
"""


# ---------------------------------------------------------------------------- ghi


def noi_dung_sinh(buoi: Path) -> dict[str, bytes]:
    """Mọi tệp văn bản của nền (trừ uv.lock), dạng {đường dẫn tương đối trong 00-nen: nội dung}."""
    cau_hinh = doc_toml(buoi / "lab" / "nen.toml")
    pb = doc_toml(PHIEN_BAN)
    danh_muc = doc_toml(DANH_MUC)
    khoa_la = set(cau_hinh) - {"thu_vien", "du_lieu", "ghi_de", "cham", "ghi_chu", "khung_bo"}
    if khoa_la:
        raise LoiNen(f"lab/nen.toml có khoá lạ {sorted(khoa_la)}")

    cac_bo = lay_bo(cau_hinh, danh_muc)
    tep: dict[str, bytes] = {
        "pyproject.toml": dung_pyproject(buoi, cau_hinh, pb, cac_bo).encode(),
        ".python-version": f"{pb['python']}\n".encode(),
        "du-lieu.toml": dung_du_lieu_toml(buoi, cac_bo).encode(),
        "chuan-bi.sh": dung_chuan_bi(buoi).encode(),
        "README.md": dung_readme(buoi, cac_bo).encode(),
    }
    dau = (f"# BẢN SAO của tools/lay_du_lieu.py — {DAU_SINH.format(nguon='tools/lay_du_lieu.py')}\n")
    tep["lay_du_lieu.py"] = dau.encode() + LAY_DU_LIEU.read_bytes()
    # buổi dạy chính công cụ nào thì bỏ module đó khỏi tv/ (vd buổi 13 tự viết ro_ri) — không phát đáp án
    khung_bo = set(cau_hinh.get("khung_bo", []))
    co_san = {p.stem for p in KHUNG.glob("*.py") if p.stem != "__init__"}
    if la := khung_bo - co_san:
        raise LoiNen(f"khung_bo có module không tồn tại {sorted(la)} (có: {sorted(co_san)})")
    for p in sorted(KHUNG.rglob("*.py")):
        if "__pycache__" in p.parts or p.stem in khung_bo:
            continue
        rel = p.relative_to(KHUNG).as_posix()
        dau = f"# BẢN SAO của tools/khung/{rel} — {DAU_SINH.format(nguon=f'tools/khung/{rel}')}\n"
        tep[f"tv/{rel}"] = dau.encode() + p.read_bytes()
    return tep


def van_tay(tep: dict[str, bytes]) -> bytes:
    return (json.dumps({k: hashlib.sha256(v).hexdigest() for k, v in sorted(tep.items())},
                       indent=1, ensure_ascii=False) + "\n").encode()


def uv_lock(nen: Path, nang_cap: bool) -> None:
    if not shutil.which("uv"):
        raise LoiNen("cần uv để khoá phụ thuộc — xem MOI-TRUONG.md")
    lenh = ["uv", "lock", "--project", str(nen)] + (["--upgrade"] if nang_cap else [])
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    kq = subprocess.run(lenh, env=env, capture_output=True, text=True)
    if kq.returncode:
        raise LoiNen("uv lock thất bại (phiên bản trong tools/nen/phien-ban.toml không hợp nhau?):\n"
                     + kq.stderr.strip())


def sinh(buoi: Path, nang_cap: bool, khong_lock: bool) -> None:
    nen = buoi / "lab" / "00-nen"
    tep = noi_dung_sinh(buoi)
    nen.mkdir(parents=True, exist_ok=True)

    # xoá tệp sinh cũ không còn trong nguồn (vd module bị bỏ khỏi khung); giữ .venv
    if (nen / "tv").exists():
        shutil.rmtree(nen / "tv")
    for rel, nd in tep.items():
        p = nen / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(nd)
    (nen / "chuan-bi.sh").chmod(0o755)

    if not khong_lock:
        uv_lock(nen, nang_cap)
    if (nen / "uv.lock").exists():
        tep["uv.lock"] = (nen / "uv.lock").read_bytes()
    (nen / TEP_VAN_TAY).write_bytes(van_tay(tep))


def kiem(buoi: Path) -> list[str]:
    """So nền hiện có với nền sinh từ nguồn hiện tại. Trả về danh sách lệch (rỗng = khớp)."""
    nen = buoi / "lab" / "00-nen"
    if not nen.is_dir():
        return [f"{ten_buoi(buoi)}: chưa có lab/00-nen/ — chạy python tools/sinh_nen.py {ten_buoi(buoi)}"]
    lech = []
    tep = noi_dung_sinh(buoi)
    for rel, nd in tep.items():
        p = nen / rel
        if not p.is_file():
            lech.append(f"{ten_buoi(buoi)}: thiếu 00-nen/{rel}")
        elif p.read_bytes() != nd:
            lech.append(f"{ten_buoi(buoi)}: 00-nen/{rel} lệch nguồn (sửa tay, hoặc nguồn đổi mà chưa sinh lại)")
    if (nen / "tv").is_dir():
        for p in (nen / "tv").rglob("*"):
            rel = p.relative_to(nen).as_posix()
            if p.is_file() and "__pycache__" not in p.parts and rel not in tep:
                lech.append(f"{ten_buoi(buoi)}: 00-nen/{rel} không có trong tools/khung/ (thêm tay?)")
    if not (nen / "uv.lock").is_file():
        lech.append(f"{ten_buoi(buoi)}: thiếu 00-nen/uv.lock")
    else:
        tep["uv.lock"] = (nen / "uv.lock").read_bytes()
        van_tay_cu = nen / TEP_VAN_TAY
        if not van_tay_cu.is_file() or van_tay_cu.read_bytes() != van_tay(tep):
            lech.append(f"{ten_buoi(buoi)}: uv.lock hoặc {TEP_VAN_TAY} không khớp lần sinh gần nhất "
                        "(ai đó chạy uv lock/uv add tay?)")
    return lech


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("buoi", nargs="*", help="7 | 4-8 | buoi-00-thu")
    ap.add_argument("--tat-ca", action="store_true")
    ap.add_argument("--kiem", action="store_true", help="không ghi, chỉ báo lệch")
    ap.add_argument("--nang-cap", action="store_true", help="uv lock --upgrade")
    ap.add_argument("--khong-lock", action="store_true", help="bỏ bước uv lock")
    t = ap.parse_args(argv)
    if not t.buoi and not t.tat_ca:
        ap.error("cần buổi (7, 4-8, buoi-00-thu) hoặc --tat-ca")

    try:
        cac_buoi = chon_buoi(t.buoi, t.tat_ca)
    except LoiNen as loi:
        print(f"✗ {loi}", file=sys.stderr)
        return 2
    loi_gap = 0
    for buoi in cac_buoi:
        if not (buoi / "lab" / "nen.toml").is_file():
            print(f"✗ {ten_buoi(buoi)}: thiếu lab/nen.toml (khuôn: tools/khuon-buoi/lab/nen.toml)",
                  file=sys.stderr)
            loi_gap += 1
            continue
        try:
            if t.kiem:
                lech = kiem(buoi)
                for dong in lech:
                    print(f"✗ {dong}", file=sys.stderr)
                loi_gap += bool(lech)
                if not lech:
                    print(f"✓ {ten_buoi(buoi)}: nền khớp nguồn")
            else:
                sinh(buoi, t.nang_cap, t.khong_lock)
                print(f"✓ {ten_buoi(buoi)}: đã sinh lab/00-nen/"
                      + ("" if t.khong_lock else " + uv.lock"))
        except LoiNen as loi:
            print(f"✗ {ten_buoi(buoi)}: {loi}", file=sys.stderr)
            loi_gap += 1
    return 1 if loi_gap else 0


if __name__ == "__main__":
    sys.exit(main())
