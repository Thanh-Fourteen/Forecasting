#!/usr/bin/env bash
# Chặn mọi thứ phá tính TỰ CHỨA của từng buổi. Chạy trước khi tick ✅ một buổi và trong CI.
#
#     ./tools/kiem_tra_doc_lap.sh                  mọi buoi-*/
#     ./tools/kiem_tra_doc_lap.sh 7 13 buoi-00-thu chỉ các buổi này
#     ./tools/kiem_tra_doc_lap.sh --nhanh          bỏ `uv lock --check` (cần mạng tới PyPI)
#
# Các kiểm tra (mã in trong báo cáo):
#   K1  tham chiếu chéo: ../buoi-…, buoi-XX/ của buổi khác, đường dẫn thoát khỏi buổi (../../../)
#   K2  dùng tools/ từ trong buổi: import tools/khung, sys.path tới tools, lệnh gọi tools/*.py
#   K3  nền: có lab/nen.toml, lab/Makefile (up/check/down), 00-nen khớp nguồn (sinh_nen.py --kiem),
#       uv.lock còn khớp pyproject (uv lock --check)
#   K4  dữ liệu: mọi bộ trong du-lieu.toml có sha256 + giấy phép + khoảng thời gian (luật của lay_du_lieu.kiem_bo)
#   K5  đường dẫn tuyệt đối tới máy tác giả (/home/, /Users/, C:\Users)
#   K6  model/LLM không chốt revision: from_pretrained/hf_hub_download/snapshot_download/load_dataset/pipeline
#       thiếu revision=; tên model kiểu "latest"
#   K7  cài đặt ngoài lock: pip install / uv add / uv pip install trong code của buổi
#   K8  code/ hoặc lab/cham/ trỏ tới dap-an/ (lộ đáp án, và dap-an/ không có trong zip)
#   K9  git đang theo dõi dữ liệu hoặc notebook (.csv .parquet .zip .ipynb …, tệp > 2 MB) trong buổi
#   K10 pyproject.toml gốc có [tool.uv.workspace] hoặc [project] (uv sẽ nuốt uv.lock của buổi)
set -euo pipefail
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$GOC/.venv/bin/python"
[ -x "$PY" ] || PY="$(command -v python3)"
"$PY" -c 'import sys; sys.exit(sys.version_info < (3, 11))' \
    || { echo "cần Python ≥ 3.11 (tomllib) — tạo venv công cụ: xem CLAUDE.md"; exit 2; }
exec "$PY" - "$GOC" "$@" <<'PY'
import ast
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

GOC = Path(sys.argv[1])
tham_so = sys.argv[2:]
NHANH = "--nhanh" in tham_so
tham_so = [t for t in tham_so if t != "--nhanh"]
sys.path.insert(0, str(GOC / "tools"))
from lay_du_lieu import kiem_bo  # noqa: E402

BO_QUA_THU_MUC = {".venv", "__pycache__", ".ipynb_checkpoints", ".pytest_cache", ".ruff_cache"}
DUOI_VAN_BAN = {".py", ".sh", ".md", ".toml", ".txt", ".cfg", ".ini", ".yaml", ".yml", ".json", ".ipynb"}
DUOI_DU_LIEU = {".csv", ".parquet", ".zip", ".gz", ".xlsx", ".xls", ".feather", ".nc", ".grib2",
                ".pkl", ".pickle", ".h5", ".hdf5", ".npz", ".npy", ".db", ".sqlite", ".duckdb", ".ipynb"}
HAM_CAN_REVISION = {"from_pretrained", "hf_hub_download", "snapshot_download", "load_dataset", "pipeline"}

vi_pham: list[tuple[str, str, str]] = []  # (mã, buổi, mô tả)


def bao(ma: str, buoi: str, mo_ta: str) -> None:
    vi_pham.append((ma, buoi, mo_ta))


def chon_buoi() -> list[Path]:
    if not tham_so:
        return sorted(p for p in GOC.glob("buoi-*") if p.is_dir())
    ra = []
    for t in tham_so:
        ten = f"buoi-{int(t):02d}" if t.isdigit() else Path(t.rstrip("/")).name
        p = GOC / ten
        if not p.is_dir():
            print(f"✗ không có thư mục {ten}", file=sys.stderr)
            sys.exit(2)
        ra.append(p)
    return ra


def cac_tep(buoi: Path):
    for goc, thu_muc, tep in os.walk(buoi):
        rel_goc = Path(goc).relative_to(buoi)
        thu_muc[:] = [d for d in thu_muc if d not in BO_QUA_THU_MUC
                      and not (rel_goc.as_posix() == "lab/du-lieu" and d == "raw")]
        for ten in tep:
            yield Path(goc) / ten


def la_van_ban(p: Path) -> bool:
    return p.suffix in DUOI_VAN_BAN or p.name in {"Makefile", ".python-version"}


def doc(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def chuoi_khong_docstring(cay: ast.AST):
    """Mọi hằng chuỗi trong code, trừ docstring (docstring được phép nhắc tên thư mục)."""
    docstring = set()
    for nut in ast.walk(cay):
        if isinstance(nut, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if nut.body and isinstance(nut.body[0], ast.Expr) and isinstance(nut.body[0].value, ast.Constant):
                docstring.add(id(nut.body[0].value))
    for nut in ast.walk(cay):
        if isinstance(nut, ast.Constant) and isinstance(nut.value, str) and id(nut) not in docstring:
            yield nut


def dong_lenh(van_ban: str):
    """Dòng không phải chú thích của sh/Makefile, kèm số dòng."""
    for i, dong in enumerate(van_ban.splitlines(), 1):
        if not dong.lstrip().startswith("#"):
            yield i, dong


def kiem_buoi(buoi: Path) -> None:
    ten = buoi.name
    nen = buoi / "lab" / "00-nen"
    re_buoi = re.compile(r"(?<![\w-])(buoi-\d{2}[a-z0-9-]*)/")

    for p in cac_tep(buoi):
        rel = p.relative_to(buoi).as_posix()
        vi_tri = f"{rel}"
        trong_nen_sinh = rel.startswith("lab/00-nen/")

        if not la_van_ban(p):
            continue
        van_ban = doc(p)
        if not van_ban:
            continue
        la_nghien_cuu = p.name == "NGHIEN-CUU.md"

        # K1 — tham chiếu chéo
        if not la_nghien_cuu:
            for i, dong in enumerate(van_ban.splitlines(), 1):
                if "../buoi-" in dong:
                    bao("K1", ten, f"{vi_tri}:{i}: trỏ ra buổi khác — {dong.strip()[:90]}")
                    continue
                for m in re_buoi.finditer(dong):
                    if m.group(1) != ten:
                        bao("K1", ten, f"{vi_tri}:{i}: nhắc đường dẫn {m.group(1)}/ của buổi khác")
                if "../../../" in dong and p.suffix != ".md":
                    bao("K1", ten, f"{vi_tri}:{i}: đường dẫn ../../../ thoát khỏi thư mục buổi")

        # K5 — đường dẫn tuyệt đối
        if not la_nghien_cuu and p.name != "uv.lock":
            for i, dong in enumerate(van_ban.splitlines(), 1):
                if re.search(r"/home/[\w.-]+/|/Users/[\w.-]+/|[A-Za-z]:\\Users\\", dong):
                    bao("K5", ten, f"{vi_tri}:{i}: đường dẫn tuyệt đối — {dong.strip()[:90]}")

        # Python: K2, K6, K7, K8 bằng AST
        if p.suffix == ".py" and not trong_nen_sinh:
            try:
                cay = ast.parse(van_ban, filename=rel)
            except SyntaxError as loi:
                bao("K2", ten, f"{vi_tri}: không parse được ({loi.msg}, dòng {loi.lineno})")
                continue
            for nut in ast.walk(cay):
                if isinstance(nut, ast.Import):
                    ten_mod = [a.name for a in nut.names]
                elif isinstance(nut, ast.ImportFrom):
                    ten_mod = [nut.module or ""]
                else:
                    ten_mod = []
                for mod in ten_mod:
                    if mod.split(".")[0] in {"tools", "khung", "lay_du_lieu", "sinh_nen"}:
                        bao("K2", ten, f"{vi_tri}:{nut.lineno}: import {mod} từ tools/ — dùng tv (bản sao trong 00-nen)")
                if isinstance(nut, ast.Call):
                    ten_ham = (nut.func.attr if isinstance(nut.func, ast.Attribute)
                               else nut.func.id if isinstance(nut.func, ast.Name) else "")
                    if ten_ham in HAM_CAN_REVISION:
                        khoa = {k.arg for k in nut.keywords}
                        if ten_ham == "pipeline" and "model" not in khoa:
                            pass  # pipeline() của thư viện khác (sklearn…) — chỉ xét khi nạp model
                        elif ten_ham == "load_dataset" and not any(
                                isinstance(a, ast.Constant) and isinstance(a.value, str) and "/" in a.value
                                for a in nut.args):
                            pass  # load_dataset("csv", …) đọc tệp cục bộ, không phải repo Hub
                        elif "revision" not in khoa and None not in khoa:
                            bao("K6", ten, f"{vi_tri}:{nut.lineno}: {ten_ham}(…) thiếu revision= (chốt commit trên Hugging Face)")
            for nut in chuoi_khong_docstring(cay):
                s = nut.value
                if re.search(r"(^|[:/-])latest$", s):
                    bao("K6", ten, f"{vi_tri}:{nut.lineno}: '{s}' — không dùng latest, chốt phiên bản/ngày")
                if re.search(r"\b(pip|uv pip) install\b|\buv add\b", s):
                    bao("K7", ten, f"{vi_tri}:{nut.lineno}: cài gói ngoài uv.lock — thêm vào lab/nen.toml")
                if (rel.startswith("code/") or rel.startswith("lab/cham/")) and re.search(r"dap[-_]an", s):
                    bao("K8", ten, f"{vi_tri}:{nut.lineno}: '{s}' trỏ tới đáp án")
                if re.search(r"(^|[/\\])tools([/\\]|$)", s) and not trong_nen_sinh:
                    bao("K2", ten, f"{vi_tri}:{nut.lineno}: đường dẫn tới tools/ — buổi không đọc ngoài thư mục của nó")
            for nut in ast.walk(cay):
                if isinstance(nut, ast.Import | ast.ImportFrom) and rel.startswith("code/"):
                    mods = [a.name for a in nut.names] if isinstance(nut, ast.Import) else [nut.module or ""]
                    if any(re.search(r"dap[-_]an", m) for m in mods):
                        bao("K8", ten, f"{vi_tri}:{nut.lineno}: code/ import từ đáp án")

        # sh / Makefile: K2, K7, K8 trên dòng lệnh
        if (p.suffix == ".sh" or p.name == "Makefile") and not trong_nen_sinh:
            for i, dong in dong_lenh(van_ban):
                if re.search(r"(^|[\s/])tools/", dong):
                    bao("K2", ten, f"{vi_tri}:{i}: gọi tools/ từ trong buổi — {dong.strip()[:80]}")
                if re.search(r"\b(pip|uv pip) install\b|\buv add\b", dong):
                    bao("K7", ten, f"{vi_tri}:{i}: cài gói ngoài uv.lock — {dong.strip()[:80]}")

    # K3 — nền
    if not (buoi / "lab" / "nen.toml").is_file():
        bao("K3", ten, "thiếu lab/nen.toml (khuôn: tools/khuon-buoi/lab/nen.toml)")
    mk = buoi / "lab" / "Makefile"
    if not mk.is_file():
        bao("K3", ten, "thiếu lab/Makefile")
    else:
        dich = set(re.findall(r"^([\w-]+):", doc(mk), flags=re.M))
        if thieu := {"up", "check", "down"} - dich:
            bao("K3", ten, f"lab/Makefile thiếu target {sorted(thieu)}")
    for tep_nen in ("pyproject.toml", "uv.lock", "du-lieu.toml", "chuan-bi.sh", "lay_du_lieu.py"):
        if not (nen / tep_nen).is_file():
            bao("K3", ten, f"thiếu lab/00-nen/{tep_nen} — chạy: python tools/sinh_nen.py {ten}")
    if (buoi / "lab" / "nen.toml").is_file():
        kq = subprocess.run([sys.executable, str(GOC / "tools" / "sinh_nen.py"), "--kiem", ten],
                            capture_output=True, text=True)
        for dong in kq.stderr.splitlines():
            if dong.startswith("✗"):
                bao("K3", ten, dong.removeprefix("✗ ").removeprefix(f"{ten}: "))
    if not NHANH and (nen / "uv.lock").is_file() and shutil.which("uv"):
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
        kq = subprocess.run(["uv", "lock", "--check", "--project", str(nen)],
                            capture_output=True, text=True, env=env)
        if kq.returncode:
            bao("K3", ten, "uv.lock không khớp pyproject.toml (uv lock --check): "
                + (kq.stderr.strip().splitlines() or ["?"])[-1])

    # K4 — dữ liệu
    toml_du_lieu = nen / "du-lieu.toml"
    if toml_du_lieu.is_file():
        try:
            with open(toml_du_lieu, "rb") as f:
                cac_bo = tomllib.load(f).get("bo", [])
            for bo in cac_bo:
                for vd in kiem_bo(bo):
                    bao("K4", ten, vd)
        except tomllib.TOMLDecodeError as loi:
            bao("K4", ten, f"du-lieu.toml sai cú pháp: {loi}")

    # K9 — git đang theo dõi dữ liệu/notebook
    if shutil.which("git") and (GOC / ".git").exists():
        kq = subprocess.run(["git", "-C", str(GOC), "ls-files", "-z", "--", ten],
                            capture_output=True, text=True)
        for rel in filter(None, kq.stdout.split("\0")):
            p = GOC / rel
            if not p.is_file():
                continue
            if p.suffix.lower() in DUOI_DU_LIEU:
                bao("K9", ten, f"git theo dõi {rel} — dữ liệu tải qua du-lieu.toml, notebook sinh từ .py")
            elif p.stat().st_size > 2_000_000 and p.suffix.lower() not in {".pdf", ".png"}:
                bao("K9", ten, f"git theo dõi tệp lớn {rel} ({p.stat().st_size // 1_000_000} MB)")


def kiem_goc() -> None:
    pp = GOC / "pyproject.toml"
    if pp.is_file():
        with open(pp, "rb") as f:
            cau_hinh = tomllib.load(f)
        if "workspace" in cau_hinh.get("tool", {}).get("uv", {}):
            bao("K10", "(gốc)", "pyproject.toml gốc có [tool.uv.workspace] — uv sẽ gom uv.lock của mọi buổi")
        if "project" in cau_hinh:
            bao("K10", "(gốc)", "pyproject.toml gốc có [project] — repo không phải dự án Python, bỏ bảng này")


def main() -> int:
    cac_buoi = chon_buoi()
    kiem_goc()
    for buoi in cac_buoi:
        kiem_buoi(buoi)
    if not cac_buoi:
        print("(chưa có thư mục buoi-*)")
    theo_buoi: dict[str, list] = {}
    for ma, buoi, mo_ta in vi_pham:
        theo_buoi.setdefault(buoi, []).append((ma, mo_ta))
    for buoi in [b.name for b in cac_buoi]:
        if buoi not in theo_buoi:
            print(f"✓ {buoi}")
    for buoi, ds in theo_buoi.items():
        print(f"✗ {buoi} — {len(ds)} vi phạm")
        for ma, mo_ta in ds:
            print(f"    {ma}  {mo_ta}")
    if vi_pham:
        print(f"\nKHÔNG ĐẠT: {len(vi_pham)} vi phạm tính tự chứa. Giải thích mã K1–K10 ở đầu tools/kiem_tra_doc_lap.sh")
        return 1
    print(f"\nĐẠT: {len(cac_buoi)} buổi tự chứa" + (" (bỏ qua uv lock --check)" if NHANH else ""))
    return 0


sys.exit(main())
PY
