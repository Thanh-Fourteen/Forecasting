"""Đóng gói thư mục phát cho học viên: phat-de/<tên>.zip — LOẠI đáp án và tài liệu nội bộ.

    python tools/dong_goi.py 7                     phat-de/buoi-07.zip
    python tools/dong_goi.py 4-8 13                nhiều buổi
    python tools/dong_goi.py --tat-ca              mọi buoi-*/
    python tools/dong_goi.py du-an-giua-chang/01-eda-lam-sach   thư mục bất kỳ trong repo
    python tools/dong_goi.py 7 --liet-ke           in danh sách tệp sẽ vào zip, không ghi

KHÔNG BAO GIỜ vào zip (CLAUDE.md quy tắc 9 — đừng gỡ bộ lọc):
    thư mục  dap-an/  loi-giai-mau/  ngay-du-lieu-hong/  ghi-am-dap-an/  giam-khao/
    tệp      NGHIEN-CUU.md  tai-lieu.md (phát bản PDF)  kiem-tra.md (có đáp án)
Quy ước cho dự án: mọi thứ giám khảo giữ (lỗi cài sẵn, holdout, script tiêm sự cố) đặt trong
thư mục tên `giam-khao/` ở bất kỳ cấp nào.

Cũng loại đồ sinh ra: .venv/, lab/du-lieu/raw/, lab/du-lieu/moi/ (tải trực tiếp), lab/du-lieu/cache/, __pycache__/, .ipynb_checkpoints/, *.ipynb (trừ code/*.ipynb),
.env, lab/nen.toml và .dau-van-tay.json (tệp của tác giả), mlruns/, outputs/.

Zip tất định: thứ tự tệp cố định, mốc thời gian cố định → cùng nội dung thì cùng sha256.
Sau khi ghi, zip được mở lại và quét lần hai; lọt tệp cấm thì xoá zip và báo lỗi.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
DICH = GOC / "phat-de"

THU_MUC_CAM = {"dap-an", "loi-giai-mau", "ngay-du-lieu-hong", "ghi-am-dap-an", "giam-khao"}
TEP_CAM = {"NGHIEN-CUU.md", "tai-lieu.md", "kiem-tra.md"}
THU_MUC_SINH = {".venv", "__pycache__", ".ipynb_checkpoints", ".pytest_cache", ".ruff_cache",
                "mlruns", "outputs", ".git"}
TEP_SINH = {".env", ".DS_Store", ".dau-van-tay.json"}
DUOI_SINH = {".pyc", ".ipynb", ".part"}  # .ipynb: trừ code/*.ipynb phát sẵn cho học viên
MOC_THOI_GIAN = (2026, 1, 1, 0, 0, 0)


def bi_loai(rel: Path) -> str | None:
    """Lý do loại tệp (None = đưa vào zip). rel tính từ thư mục được đóng gói."""
    phan = rel.parts
    if cam := THU_MUC_CAM.intersection(phan[:-1]):
        return f"thư mục nội bộ {sorted(cam)[0]}/"
    if rel.name in TEP_CAM:
        return "tài liệu nội bộ"
    if THU_MUC_SINH.intersection(phan[:-1]):
        return "sinh ra"
    if len(phan) >= 3 and phan[0] == "lab" and phan[1] == "du-lieu" and phan[2] in ("raw", "moi"):
        return "dữ liệu tải về"
    if len(phan) >= 3 and phan[0] == "lab" and phan[1] == "du-lieu" and phan[2] == "cache":
        return "sinh ra"   # kết quả chạy trên máy tác giả; code tự dựng lại khi thiếu
    if rel.as_posix() == "lab/nen.toml":
        return "cấu hình của tác giả"
    if rel.suffix == ".ipynb" and len(rel.parts) >= 2 and rel.parts[-2] == "code":
        return None
    if rel.name in TEP_SINH or rel.suffix in DUOI_SINH:
        return "sinh ra"
    return None


def chon(tham_so: list[str], tat_ca: bool) -> list[Path]:
    if tat_ca:
        return sorted(p for p in GOC.glob("buoi-*") if p.is_dir())
    ra: list[Path] = []
    for t in tham_so:
        if t.isdigit():
            ra.append(GOC / f"buoi-{int(t):02d}")
        elif m := re.fullmatch(r"(\d+)-(\d+)", t):
            ra += [GOC / f"buoi-{n:02d}" for n in range(int(m[1]), int(m[2]) + 1)
                   if (GOC / f"buoi-{n:02d}").is_dir()]
        else:
            ra.append((GOC / t.rstrip("/")).resolve())
    return list(dict.fromkeys(ra))


def dong_goi(thu_muc: Path, chi_liet_ke: bool) -> int:
    if not thu_muc.is_dir() or not thu_muc.is_relative_to(GOC):
        print(f"✗ {thu_muc}: không phải thư mục trong repo", file=sys.stderr)
        return 1
    ten = thu_muc.relative_to(GOC).as_posix().replace("/", "--")
    tep_vao, bi_bo = [], {}
    for p in sorted(thu_muc.rglob("*")):
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(thu_muc)
        if ly_do := bi_loai(rel):
            bi_bo[ly_do] = bi_bo.get(ly_do, 0) + 1
        else:
            tep_vao.append(rel)

    canh_bao = []
    if thu_muc.name.startswith("buoi-"):
        if not any(r.suffix == ".pdf" and len(r.parts) == 1 for r in tep_vao):
            canh_bao.append("chưa có PDF tài liệu (python tools/xuat_pdf.py …)")
        if (thu_muc / "lab").is_dir() and Path("lab/00-nen/uv.lock") not in tep_vao:
            print(f"✗ {ten}: thiếu lab/00-nen/uv.lock — zip không dựng được nền. "
                  "Chạy python tools/sinh_nen.py trước", file=sys.stderr)
            return 1

    if chi_liet_ke:
        print(f"{ten}: {len(tep_vao)} tệp vào zip")
        for r in tep_vao:
            print(f"  + {r.as_posix()}")
        for ly_do, so in sorted(bi_bo.items()):
            print(f"  - {so} tệp loại: {ly_do}")
        return 0

    DICH.mkdir(exist_ok=True)
    zip_path = DICH / f"{ten}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in tep_vao:
            nguon = thu_muc / rel
            info = zipfile.ZipInfo(f"{thu_muc.name}/{rel.as_posix()}", date_time=MOC_THOI_GIAN)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if nguon.stat().st_mode & 0o111 else 0o644) << 16
            z.writestr(info, nguon.read_bytes())

    # quét lần hai trên chính zip đã ghi — bộ lọc sai thì không phát
    with zipfile.ZipFile(zip_path) as z:
        lot = [n for n in z.namelist() if bi_loai(Path(*Path(n).parts[1:])) in
               {f"thư mục nội bộ {d}/" for d in THU_MUC_CAM} | {"tài liệu nội bộ"}]
    if lot:
        zip_path.unlink()
        print(f"✗ {ten}: zip lọt tệp nội bộ {lot[:5]} — đã xoá zip", file=sys.stderr)
        return 1

    sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    print(f"✓ {zip_path.relative_to(GOC)}  {len(tep_vao)} tệp, "
          f"{zip_path.stat().st_size / 1024:.0f} KB, sha256 {sha[:12]}  "
          f"(loại: {', '.join(f'{so} {ly_do}' for ly_do, so in sorted(bi_bo.items())) or 'không'})")
    for c in canh_bao:
        print(f"  ! {c}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("thu_muc", nargs="*", help="7 | 4-8 | buoi-00-thu | du-an-cuoi")
    ap.add_argument("--tat-ca", action="store_true")
    ap.add_argument("--liet-ke", action="store_true", help="chỉ in danh sách, không ghi zip")
    t = ap.parse_args(argv)
    if not t.thu_muc and not t.tat_ca:
        ap.error("cần buổi/thư mục hoặc --tat-ca")
    return 1 if sum(dong_goi(p, t.liet_ke) for p in chon(t.thu_muc, t.tat_ca)) else 0


if __name__ == "__main__":
    sys.exit(main())
