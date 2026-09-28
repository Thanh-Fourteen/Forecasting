"""Sinh notebook tự học buoi-NN/tu-hoc.ipynb từ tools/tu_hoc/buoi_NN.py — ôn gọn + code đáp án, tự chứa.

    python tools/tu_hoc/sinh.py N --khung        dựng buoi_NN.py khung từ tai-lieu.md (chỗ cần viết ghi TODO)
    python tools/tu_hoc/sinh.py N [N…] --chay    sinh rồi chạy hết các ô, in output để so số  (--im: chỉ báo lỗi)
    python tools/tu_hoc/sinh.py --tat-ca         sinh lại mọi buổi đã có buoi_NN.py
    python tools/tu_hoc/sinh.py --thieu          buổi đã soạn (tai-lieu.md + dap-an/) mà chưa có notebook tự học

Hình minh hoạ khái niệm (bảng HINH): ghi buoi-NN/dap-an/ve_hinh_khai_niem.py, vẽ buoi-NN/hinh/kn-*.png, nhúng vào
notebook, chèn vào tai-lieu.md ngay sau đoạn mốc `sau` và xuất lại PDF (quy tắc D14, todos/quy-uoc.md).

Văn phong, quy trình, danh sách kiểm: tools/tu_hoc/HUONG-DAN.md. sinh.py DỪNG nếu notebook thiếu ý của tài liệu
(DU_Y), thiếu hộp khái niệm cho một từ mới (BO_TU), phần sai khuôn Vấn đề → Lý do → Kết quả → Bài học, HINH không
khớp hộp, bộ dữ liệu chưa có mô tả (du_lieu.toml), hoặc còn TODO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from fnmatch import fnmatch
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOC = HERE.parents[1]
sys.path.insert(0, str(HERE))
import moi_truong  # noqa: E402

O_DU_LIEU = '''import hashlib
import os
import urllib.request
from pathlib import Path

# tên bộ: (sha256, [nơi tải, thử lần lượt])
DU_LIEU = {
%s}
CACHE = Path(os.environ.get("KHOA_FORECASTING_CACHE") or Path.home() / ".cache" / "khoa-forecasting")


def sha256(tep: Path) -> str:
    h = hashlib.sha256()
    with open(tep, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def lay(ten: str) -> Path:
    """Đường dẫn tệp đã kiểm sha256; chưa có thì tải về một lần."""
    sha, urls = DU_LIEU[ten]
    tep = CACHE / "sha256" / sha[:2] / sha
    if tep.is_file() and sha256(tep) == sha:
        return tep
    tep.parent.mkdir(parents=True, exist_ok=True)
    for url in urls:
        try:
            urllib.request.urlretrieve(url, tep)
            if sha256(tep) == sha:
                return tep
            print("sha256 không khớp:", url)
        except OSError as loi:
            print("tải lỗi:", url, loi)
    raise RuntimeError(f"không tải được {ten} khớp sha256")


for ten in DU_LIEU:
    print(f"{ten:<28} {lay(ten)}")'''


def _dung_luong(byte: int) -> str:
    return f"{byte / 1e6:.0f} MB" if byte >= 1e6 else f"{byte / 1e3:.0f} KB"


def mo_ta_du_lieu(cac_bo: list[str], dm: dict) -> str:
    """Markdown mục "Bộ dữ liệu": mỗi mô tả trong du_lieu.toml một lần (họ bộ dùng mẫu *), kèm nguồn và giấy phép."""
    with open(HERE / "du_lieu.toml", "rb") as f:
        mo_ta = tomllib.load(f)
    theo_khoa: dict[str, list[str]] = {}
    for ten in cac_bo:
        khoa = ten if ten in mo_ta else next((k for k in mo_ta if "*" in k and fnmatch(ten, k)), None)
        if khoa is None:
            raise SystemExit(f"thiếu mô tả bộ '{ten}' trong tools/tu_hoc/du_lieu.toml — thêm [\"{ten}\"] (ten, "
                             f"gioi_thieu, bảng cot) theo mẫu đầu tệp")
        theo_khoa.setdefault(khoa, []).append(ten)
    phan = []
    for khoa, ds in theo_khoa.items():
        m, bo = mo_ta[khoa], dm[ds[0]]
        nguon = bo["ghi_nguon"].rstrip(". ") + (f"; và {len(ds) - 1} tệp cùng họ" if len(ds) > 1 else "") + "."
        khoi = [f"**Bộ dữ liệu {m['ten']}.** {m['gioi_thieu'].strip()}", "",
                f"Nguồn: {nguon} Giấy phép {bo['giay_phep']}."]
        if m.get("cot"):
            khoi += ["", "| Cột | Nghĩa |", "|---|---|"]
            khoi += [f"| {', '.join(f'`{c.strip()}`' for c in k.split(','))} | {v} |" for k, v in m["cot"].items()]
        phan.append("\n".join(khoi))
    tong = sum(dm[t].get("dung_luong", 0) for t in cac_bo)
    tai = (f"Ô dưới tải dữ liệu ({_dung_luong(tong)}) một lần" if tong else "Ô dưới tải dữ liệu một lần")
    phan.append(tai + " rồi kiểm **sha256** — \"dấu vân tay\" tính từ nội dung tệp, sai một byte là ra chuỗi khác "
                "hẳn. Khớp nghĩa là bạn đang có đúng tệp mà mọi con số dưới đây được tính ra.")
    return "\n\n".join(phan)


KHUON_VE = """# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_{n:02d}.py (bảng HINH) — không sửa tay.
# Hình minh hoạ khái niệm (dữ liệu tự tạo, có seed) → ../hinh/kn-*.png, dùng trong tai-lieu.md và tu-hoc.ipynb.
# Chạy: python ve_hinh_khai_niem.py   (cần numpy, pandas, matplotlib)
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HINH = Path(__file__).resolve().parent.parent / "hinh"
VE = {{
{ve}}}

plt.rcParams.update({{"font.size": 8, "axes.spines.top": False, "axes.spines.right": False}})
for ten_tep, code in VE.items():
    fig, ax = plt.subplots(figsize=(5.2, 2.1))
    ns = {{"np": np, "pd": pd, "plt": plt, "fig": fig, "ax": ax}}
    exec(code, ns)
    if ns["fig"] is not fig:
        plt.close(fig)
    ns["fig"].savefig(HINH / ten_tep, dpi=150, bbox_inches="tight")
    plt.close("all")
    print("vẽ", ten_tep)
"""


def ten_tep_hinh(ten: str) -> str:
    """'phương sai, độ lệch chuẩn' -> 'kn-phuong-sai-do-lech-chuan.png'."""
    import unicodedata
    s = unicodedata.normalize("NFD", ten.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return "kn-" + re.sub(r"[^a-z0-9]+", "-", s).strip("-") + ".png"


def ve_hinh(n: int, hinh: dict[str, dict], ho_so: str) -> dict[str, str]:
    """Ghi buoi-NN/dap-an/ve_hinh_khai_niem.py từ HINH, chạy nó → buoi-NN/hinh/kn-*.png; trả {tên tệp: PNG base64}."""
    if not hinh:
        return {}
    import base64
    py = moi_truong.python_cua(ho_so)
    if not py.is_file():
        raise SystemExit(f"chưa có môi trường {ho_so} để vẽ hình — chạy: python tools/tu_hoc/moi_truong.py {n}")
    buoi = GOC / f"buoi-{n:02d}"
    ve = "".join(f"    {ten_tep_hinh(ten)!r}: r'''{h['ve'].strip(chr(10))}\n''',\n" for ten, h in hinh.items())
    script = buoi / "dap-an" / "ve_hinh_khai_niem.py"
    script.write_text(KHUON_VE.format(n=n, ve=ve), encoding="utf-8")
    kq = subprocess.run([str(py), script.name], cwd=script.parent, capture_output=True, text=True)
    if kq.returncode:
        raise SystemExit("vẽ hình khái niệm lỗi:\n" + kq.stderr[-2000:])
    return {ten_tep_hinh(ten): base64.b64encode((buoi / "hinh" / ten_tep_hinh(ten)).read_bytes()).decode()
            for ten in hinh}


KHOI_HINH = re.compile(r"\n!\[[^\]]*\]\(hinh/kn-[\w-]+\.png\)\n\n\*\*Cách đọc hình\.\*\* [^\n]*(?:\n[^\n]+)*\n")


def chen_tai_lieu(n: int, hinh: dict[str, dict]) -> bool:
    """Chèn (lại) hình khái niệm vào tai-lieu.md: sau đoạn chứa mốc `sau`, kèm "Cách đọc hình" rút gọn. True nếu đổi."""
    tep = GOC / f"buoi-{n:02d}" / "tai-lieu.md"
    cu = tep.read_text(encoding="utf-8")
    t = KHOI_HINH.sub("", cu)
    for ten, h in hinh.items():
        if not h.get("sau"):
            continue                                   # hình chỉ cho notebook (tài liệu đã có hình cùng ý)
        if t.count(h["sau"]) != 1:
            raise SystemExit(f"HINH[{ten!r}]['sau'] phải xuất hiện đúng 1 lần trong tai-lieu.md: {h['sau']!r}")
        vi_tri = t.index(h["sau"])
        het = t.find("\n\n", vi_tri)
        het = len(t) if het < 0 else het
        while (m := KHOI_HINH.match(t, het)):             # đã có hình chèn ở đây → đặt sau chúng, giữ thứ tự
            het = m.end() - 1
        khoi = f"\n![{ten}](hinh/{ten_tep_hinh(ten)})\n\n**Cách đọc hình.** {h['doc'].strip()}\n"
        t = t[:het + 1] + khoi + t[het + 1:]
    if t != cu:
        tep.write_text(t, encoding="utf-8")
    return t != cu


class Soan:
    def __init__(self, n: int):
        self.n = n
        self.o: list[tuple[str, str]] = []
        self.khai_niem_da_co: list[str] = []
        self.cho: list[str] = []
        self.hinh: dict[str, dict] = {}
        self.hinh_theo_ten: dict[str, dict] = {}
        with open(GOC / f"buoi-{n:02d}" / "lab" / "nen.toml", "rb") as f:
            self.nen = tomllib.load(f)
        self.ho_so = moi_truong.ho_so(n)

    def md(self, s: str) -> None:
        # hộp khái niệm đang chờ: chèn sau "Vấn đề", trước "Lý do" của phần kế tiếp (hoặc ngay trước ô này)
        if self.cho and "**Lý do.**" in s:
            dau, sau = s.split("**Lý do.**", 1)
            if dau.strip():
                self.o.append(("md", dau.rstrip()))
            self._xa_cho()
            s = "**Lý do.**" + sau
        self._xa_cho()
        self.o.append(("md", s))

    def py(self, s: str) -> None:
        self._xa_cho()
        self.o.append(("py", s))

    def _xa_cho(self) -> None:
        self.o.extend(("md", h) for h in self.cho)
        self.cho = []

    def khai_niem(self, ten: str, en: str, la_gi: str, vi_du: str, de_lam_gi: str, hinh: str | None = None) -> None:
        """Hộp khái niệm mới. Gọi ngay TRƯỚC nb.md của phần dùng nó lần đầu: hộp hiện sau "Vấn đề", trước "Lý do".
        Mỗi ý 1–2 câu; ví dụ có số cụ thể; "để làm gì" nói nó giúp gì cho dự báo.

        hinh: code matplotlib vẽ lên `ax` có sẵn (hoặc tự tạo `fig, ...` nếu cần nhiều ô), dữ liệu minh hoạ tự tạo
        (có seed). Vẽ lúc sinh, nhúng PNG vào ô markdown (attachment) — mở notebook là thấy, không cần chạy.
        """
        self.khai_niem_da_co.append(ten)
        tieu_de = f"**{ten}** · *{en}*" if en.lower() != ten.lower() else f"**{ten}**"
        hop = (f"> {tieu_de}\n>\n> - **Là gì:** {la_gi.strip()}\n> - **Ví dụ:** {vi_du.strip()}\n"
               f"> - **Để làm gì:** {de_lam_gi.strip()}")
        h = self.hinh_theo_ten.get(ten) or ({"ve": hinh} if hinh else None)
        if h:
            for k in ("ve", "doc"):
                if not h.get(k):
                    raise SystemExit(f"HINH[{ten!r}] thiếu khoá {k!r} (cần ve, doc, sau — sau=None nếu chỉ cho notebook)")
            self.hinh[ten] = h
            hop += f"\n>\n> ![{ten}](attachment:{ten_tep_hinh(ten)})"
        self.cho.append(hop)

    def du_lieu(self, cac_bo: list[str] | None = None) -> None:
        """Mục "Bộ dữ liệu" (sinh từ tools/tu_hoc/du_lieu.toml + danh mục) rồi ô tải: hàm `lay(ten) -> Path`.

        Mặc định: mọi bộ trong lab/nen.toml của buổi.
        """
        with open(GOC / "tools" / "du-lieu" / "danh-muc.toml", "rb") as f:
            dm = tomllib.load(f)["bo"]
        cac_bo = cac_bo or self.nen.get("du_lieu", [])
        self.md(mo_ta_du_lieu(cac_bo, dm))
        dong = []
        for ten in cac_bo:
            bo = dm[ten]
            if bo.get("kieu") != "http" or "sha256" not in bo:
                raise SystemExit(f"{ten}: kiểu '{bo.get('kieu')}' chưa hỗ trợ trong notebook tự học — "
                                 f"thêm cách tải vào tools/tu_hoc/sinh.py")
            urls = [u for u in (bo.get("url_mirror"), bo["url"]) if u]
            dong.append(f'    "{ten}": ("{bo["sha256"]}", [\n'
                        + "".join(f'        "{u}",\n' for u in urls) + "    ]),\n")
        self.py(O_DU_LIEU % "".join(dong))

    def ghi(self, dich: Path) -> None:
        self._xa_cho()
        anh = ve_hinh(self.n, self.hinh, self.ho_so)
        cells = []
        for i, (kieu, nguon) in enumerate(self.o):
            c = {"cell_type": "markdown" if kieu == "md" else "code", "id": f"o{i:02d}", "metadata": {},
                 "source": nguon.strip("\n").splitlines(keepends=True)}
            if kieu == "py":
                c.update(execution_count=None, outputs=[])
            dinh_kem = {m: {"image/png": anh[m]} for m in re.findall(r"attachment:(kn-[\w-]+\.png)", nguon)}
            if dinh_kem:
                c["attachments"] = dinh_kem
            cells.append(c)
        k = moi_truong.ten_kernel(self.ho_so)
        nb = {"cells": cells,
              "metadata": {"kernelspec": {"display_name": f"Khoá Forecasting · tự học ({self.ho_so})",
                                          "language": "python", "name": k},
                           "language_info": {"name": "python"}},
              "nbformat": 4, "nbformat_minor": 5}
        dich.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def soan(n: int) -> Soan:
    tep = HERE / f"buoi_{n:02d}.py"
    if not tep.is_file():
        raise SystemExit(f"chưa có nội dung {tep.relative_to(GOC)}")
    spec = importlib.util.spec_from_file_location(f"tu_hoc_buoi_{n:02d}", tep)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    nb = Soan(n)
    nb.hinh_theo_ten = getattr(mod, "HINH", {})
    mod.soan(nb)
    la = set(nb.hinh_theo_ten) - set(nb.khai_niem_da_co)
    if la:
        raise SystemExit(f"HINH có tên không khớp hộp khái niệm nào: {sorted(la)}")
    kiem_du_y(n, nb, getattr(mod, "DU_Y", None), getattr(mod, "BO_TU", {}))
    return nb


NHAN = ("**Vấn đề.**", "**Lý do.**", "**Kết quả.**", "**Bài học.**")


def _chuan(s: str) -> str:
    s = re.sub(r"\$[^$]*\$|`|\([^)]*\)", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def tu_moi(tl: str) -> list[str]:
    """Cột đầu bảng "Từ mới trong buổi" của tai-lieu.md."""
    m = re.search(r"^### Từ mới trong buổi\n(.*?)(?=^###)", tl, flags=re.M | re.S)
    if not m:
        return []
    dong = [d for d in m.group(1).splitlines() if d.startswith("|")][2:]
    return [d.split("|")[1].strip() for d in dong]


def kiem_du_y(n: int, nb: Soan, du_y: dict | None, bo_tu: dict) -> None:
    """Dừng nếu notebook thiếu ý của tài liệu, thiếu hộp khái niệm cho một từ mới, hoặc một phần sai khuôn."""
    tl = (GOC / f"buoi-{n:02d}" / "tai-lieu.md").read_text(encoding="utf-8")
    muc = re.findall(r"^### (4\.\d+)", tl, flags=re.M)
    bt = tl.split("## 7.", 1)[1].split("\n## ", 1)[0] if "## 7." in tl else ""
    muc += [f"BT{k}" for k in re.findall(r"^(\d+)\. \*\*", bt, flags=re.M)]
    md = "\n\n".join(s for k, s in nb.o if k == "md")
    phan = {int(m.group(1)): m.start() for m in re.finditer(r"^## (\d+)\. ", md, flags=re.M)}
    loi = []
    if du_y is None:
        loi.append(f"buoi_{n:02d}.py thiếu bảng DU_Y (mục tài liệu → số phần notebook)")
        du_y = {}
    for m in muc:
        if m not in du_y:
            loi.append(f"mục {m} của tài liệu chưa có trong DU_Y — thêm phần cho nó, hoặc ghi lý do bỏ")
        elif isinstance(du_y[m], int) and du_y[m] not in phan:
            loi.append(f"DU_Y[{m!r}] = {du_y[m]} nhưng notebook không có phần '## {du_y[m]}. '")
    vi_tri = sorted(phan.items(), key=lambda x: x[1]) + [(None, len(md))]
    ly_thuyet = {v for k, v in du_y.items() if isinstance(v, int) and not k.startswith("BT")}
    for (so, dau), (_, cuoi) in zip(vi_tri, vi_tri[1:], strict=False):
        thieu = [x for x in NHAN if x not in md[dau:cuoi]]
        if so in ly_thuyet and thieu:
            loi.append(f"phần {so} thiếu nhãn {', '.join(thieu)}")
    da_co = [_chuan(k) for k in nb.khai_niem_da_co]
    for tu in tu_moi(tl):
        bien_the = [_chuan(x) for x in re.split(r"[,/]", tu) if _chuan(x)]
        if tu in bo_tu or any(b in k or k in b for b in bien_the for k in da_co):
            continue
        loi.append(f"từ mới '{tu}' chưa có nb.khai_niem(...) (hoặc ghi lý do bỏ trong BO_TU)")
    con = sum("TODO" in s for _, s in nb.o) + sum("TODO" in h for h in nb.hinh.values())
    if con:
        loi.append(f"còn {con} ô có TODO — viết nốt nội dung")
    if loi:
        raise SystemExit(f"buổi {n} chưa đủ ý / sai khuôn:\n  - " + "\n  - ".join(loi))
    so_chu = len(md.split())
    print(f"đủ ý: {len(muc)} mục tài liệu → {len(phan)} phần; {len(nb.khai_niem_da_co)} hộp khái niệm; "
          f"{so_chu:,} chữ phần giải thích")


def khung(n: int) -> Path:
    """Dựng tools/tu_hoc/buoi_NN.py khung từ tai-lieu.md: một phần cho mỗi mục 4.x, một hộp cho mỗi từ mới, bài tập."""
    dich = HERE / f"buoi_{n:02d}.py"
    if dich.exists():
        raise SystemExit(f"{dich.relative_to(GOC)} đã có — không ghi đè")
    tl = (GOC / f"buoi-{n:02d}" / "tai-lieu.md").read_text(encoding="utf-8")
    tieu_de = re.search(r"^# (.+)$", tl, flags=re.M).group(1)
    muc = re.findall(r"^### (4\.\d+) (.+)$", tl, flags=re.M)
    bt = tl.split("## 7.", 1)[1].split("\n## ", 1)[0] if "## 7." in tl else ""
    bai = re.findall(r"^(\d+)\. \*\*(.+?)\*\*", bt, flags=re.M)
    du_y = ", ".join([f'"{m}": {k + 1}' for k, (m, _) in enumerate(muc)]
                     + [f'"BT{b}": {len(muc) + 1}' for b, _ in bai])
    q = '"' * 3
    dong = [f'{q}Nội dung tự học {tieu_de}. Sinh: python tools/tu_hoc/sinh.py {n} --chay{q}', "",
            f"DU_Y = {{{du_y}}}", "",
            "# hình khái niệm (D14): {tên hộp: {\"doc\": cách đọc 1–2 câu, \"sau\": mốc trong tai-lieu.md hoặc None, "
            "\"ve\": code matplotlib vẽ lên ax}} — xem tools/tu_hoc/HUONG-DAN.md",
            "HINH = {}", "", "", "def soan(nb) -> None:",
            f'    nb.md(r{q}# {tieu_de}\n\n**Một câu:** TODO\n\nTình huống: TODO\n\n| Phần | Câu hỏi |\n|---|---|\n'
            + "".join(f"| {k + 1} | TODO |\n" for k in range(len(muc))) + f"{q})",
            f'    nb.md(r{q}## 0. Dữ liệu{q})', "    nb.du_lieu()",
            f'    nb.py(r{q}# TODO: import, đọc dữ liệu (chép từ dap-an, bỏ tv){q})', ""]
    tu = tu_moi(tl)
    for k, (m, ten_muc) in enumerate(muc):
        dong.append(f"    # ---------------------------------------------------------------- {k + 1} ← tài liệu {m} {ten_muc}")
        if k == 0:
            dong.append("    # TODO: chuyển từng hộp dưới đây tới ngay trước phần dùng nó lần đầu")
            for w in tu:
                dong.append(f'    nb.khai_niem("{w}", "TODO tiếng Anh", "TODO là gì", "TODO ví dụ có số", "TODO để làm gì")')
        dong += [f'    nb.md(r{q}## {k + 1}. TODO tiêu đề nói kết luận ({ten_muc})\n\n**Vấn đề.** TODO\n\n'
                 f'**Lý do.** TODO\n\n**Kết quả.**{q})',
                 f'    nb.py(r{q}# TODO code chạy thật{q})',
                 f'    nb.md(r{q}TODO đọc kết quả.\n\n**Bài học.** TODO{q})', ""]
    if bai:
        dong.append(f'    nb.md(r{q}## {len(muc) + 1}. Bài tập về nhà — đáp số{q})')
        for b, ten_bai in bai:
            dong += [f'    nb.md(r{q}**Bài {b} — {ten_bai}** TODO{q})', f'    nb.py(r{q}# TODO lời giải bài {b}{q})']
    dong.append(f'    nb.md(r{q}## Tự kiểm\n\n- [ ] TODO{q})')
    dich.write_text("\n".join(dong) + "\n", encoding="utf-8")
    return dich


def liet_ke_thieu() -> int:
    """Buổi có tai-lieu.md + dap-an/ nhưng chưa có buoi_NN.py (hoặc còn TODO) — việc nền của mọi phase."""
    thieu = []
    for tl in sorted(GOC.glob("buoi-[0-9][0-9]/tai-lieu.md")):
        n = int(tl.parent.name[5:])
        if not (tl.parent / "dap-an").is_dir():
            continue
        nguon = HERE / f"buoi_{n:02d}.py"
        if not nguon.is_file():
            thieu.append(f"{n:>2}  chưa có tools/tu_hoc/buoi_{n:02d}.py   → sinh.py {n} --khung")
        elif "TODO" in nguon.read_text(encoding="utf-8"):
            thieu.append(f"{n:>2}  buoi_{n:02d}.py còn TODO               → viết nốt, rồi sinh.py {n} --chay")
        elif not (tl.parent / "tu-hoc.ipynb").is_file():
            thieu.append(f"{n:>2}  chưa sinh notebook                   → sinh.py {n} --chay")
    print("\n".join(thieu) if thieu else "không thiếu buổi nào")
    print(f"({len(thieu)} buổi thiếu notebook tự học — cách làm: tools/tu_hoc/HUONG-DAN.md)")
    return 0


def chay(nb_tep: Path, ho_so: str, im: bool) -> int:
    py = moi_truong.python_cua(ho_so)
    if not py.is_file():
        print(f"chưa có môi trường {ho_so} — chạy: python tools/tu_hoc/moi_truong.py <buổi>")
        return 1
    with tempfile.TemporaryDirectory() as tam:
        ban = Path(tam) / nb_tep.name
        shutil.copy(nb_tep, ban)
        lenh = [str(py), "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace",
                "--ExecutePreprocessor.timeout=1800", str(ban)]
        if shutil.which("systemd-run"):   # giới hạn RAM: máy tác giả chỉ trống ~10 GB
            lenh = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G", "-p", "MemorySwapMax=0", *lenh]
        # chạy trong thư mục buổi, như khi mở notebook
        kq = subprocess.run(lenh, cwd=nb_tep.parent, capture_output=True, text=True)
        if not ban.is_file() or kq.returncode:
            print(kq.stderr[-3000:])
            return 1
        loi = 0
        for i, c in enumerate(json.loads(ban.read_text(encoding="utf-8"))["cells"]):
            for o in c.get("outputs", []):
                if o["output_type"] == "error":
                    loi += 1
                    print(f"[ô {i}] LỖI {o['ename']}: {o['evalue']}")
                elif not im:
                    t = o.get("text") or o.get("data", {}).get("text/plain")
                    if t and "<Figure" not in "".join(t):
                        print(f"[ô {i}]", "".join(t).rstrip())
        print(f"==> {nb_tep.relative_to(GOC)}: {'0 lỗi' if not loi else f'{loi} ô lỗi'}")
        return 1 if loi else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("buoi", nargs="*", type=int)
    ap.add_argument("--tat-ca", action="store_true", help="mọi buổi đã có tools/tu_hoc/buoi_NN.py")
    ap.add_argument("--khung", action="store_true", help="dựng buoi_NN.py khung từ tai-lieu.md")
    ap.add_argument("--thieu", action="store_true", help="liệt kê buổi đã soạn mà chưa có notebook tự học")
    ap.add_argument("--chay", action="store_true", help="chạy thử hết các ô, in output")
    ap.add_argument("--im", action="store_true", help="khi --chay: chỉ báo lỗi")
    a = ap.parse_args(argv)
    if a.thieu:
        return liet_ke_thieu()
    cac_buoi = sorted(int(p.stem[5:]) for p in HERE.glob("buoi_[0-9][0-9].py")) if a.tat_ca else a.buoi
    if not cac_buoi:
        ap.error("cần số buổi hoặc --tat-ca")
    if a.khung:
        for n in cac_buoi:
            print(f"dựng {khung(n).relative_to(GOC)} — viết nốt các TODO rồi: python tools/tu_hoc/sinh.py {n} --chay")
        return 0
    ma = 0
    for n in cac_buoi:
        nb = soan(n)
        dich = GOC / f"buoi-{n:02d}" / "tu-hoc.ipynb"
        nb.ghi(dich)
        print(f"ghi {dich.relative_to(GOC)}: {len(nb.o)} ô, kernel {moi_truong.ten_kernel(nb.ho_so)}; "
              f"{len(nb.hinh)} hình khái niệm → buoi-{n:02d}/hinh/kn-*.png")
        if chen_tai_lieu(n, nb.hinh):
            print(f"tai-lieu.md buổi {n} đổi hình khái niệm → xuất lại PDF")
            subprocess.run([sys.executable, str(GOC / "tools" / "xuat_pdf.py"), str(n)], check=True)
        if a.chay:
            ma |= chay(dich, nb.ho_so, a.im)
    return ma


if __name__ == "__main__":
    sys.exit(main())
