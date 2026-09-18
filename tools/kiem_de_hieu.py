#!/usr/bin/env python3
"""Kiểm máy phần đo được của chuẩn dễ hiểu + gọn D1–D13 (todos/quy-uoc.md, tools/CHUAN-DE-HIEU.md).

Chỉ BÁO CÁO, không sửa gì. Không thay được bước đọc thử bằng subagent — chỉ bắt những lỗi đếm được.

    python tools/kiem_de_hieu.py              # bảng số vi phạm mọi buổi có tai-lieu.md
    python tools/kiem_de_hieu.py 1 7 12       # vài buổi
    python tools/kiem_de_hieu.py 1 --chi-tiet # liệt kê từng vi phạm kèm số dòng
    python tools/kiem_de_hieu.py 1 --nghiem   # mã thoát 1 nếu còn vi phạm (dùng trước khi tick ✅)

Mã kiểm (cột của bảng):
  tu_moi      D1  thiếu bảng "Từ mới trong buổi" trong mục Lý thuyết
  chua_bang   D1  thuật ngữ Phụ lục E thuộc buổi này, có dùng, nhưng không có trong bảng Từ mới
  muon_truoc  D5  thuật ngữ Phụ lục E của buổi SAU, có dùng, nhưng không có hộp "Mượn trước" nhắc tới
  cong_thuc   D3  khối $$…$$ không có "Nói bằng lời" ngay sau
  tieng_anh   D6  trích tiếng Anh ≥ 6 từ mà đoạn không có bản dịch
  cau_dai     D7  câu > 40 chữ
  nhieu_so    D7  đoạn văn > 3 con số
  viet_tat    D7  viết tắt chưa giải thích (không có trong bảng Từ mới, Phụ lục E, danh sách chung)
  hinh        D8  ảnh không có "Cách đọc hình" ngay sau
  bang        D8  bảng kết quả (nhiều ô số) không có "Đọc bảng" ngay sau
  khai_niem   D9  số khái niệm chính (mục ### trong Lý thuyết) vượt 6 — báo phần vượt
  tom_lai     D2  mục lý thuyết thiếu "Tóm lại"
  tu_kiem     D10 mục lý thuyết thiếu "Tự kiểm tra"
  lab         D11 bước lab thiếu "Mục đích" hoặc "Đọc kết quả"
  quiz        D12 đáp án quiz không giải thích (quá ngắn / không nói vì sao lựa chọn khác sai)
  do_dai      D13 số chữ NGOÀI bảng và khối code nằm ngoài 3.500–6.500 (wc -w đếm cả dấu | nên không dùng)
  cau_rong    D13 cụm câu rỗng / rào đón / động từ ẩn ("như đã nói ở trên", "điều quan trọng là", "tiến hành"…)
  lap_y       D13 "Tóm lại" chép lại một câu trong mục; hoặc hai đoạn trong tài liệu gần như trùng nhau
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
PHU_LUC_E = GOC / "phu-luc" / "E-tu-dien-thuat-ngu.md"

MA = [
    "tu_moi", "chua_bang", "muon_truoc", "cong_thuc", "tieng_anh", "cau_dai", "nhieu_so",
    "viet_tat", "hinh", "bang", "khai_niem", "tom_lai", "tu_kiem", "lab", "quiz", "do_dai",
    "cau_rong", "lap_y",
]

NGUONG_CAU = 40          # chữ (âm tiết) mỗi câu
NGUONG_SO = 3            # con số mỗi đoạn
NGUONG_TIENG_ANH = 6     # từ tiếng Anh liên tiếp trong một trích dẫn
MAX_KHAI_NIEM = 6
DO_DAI = (3500, 6500)    # chữ ngoài bảng và khối code (D13, chốt Phase 7)
CUA_SO = 15              # số dòng tìm nhãn sau công thức / hình / bảng
NGUONG_LAP = 0.6         # tỷ lệ cặp âm tiết liền nhau trùng → coi là lặp ý
LAP_MIN_CHU = 8          # câu/đoạn ngắn hơn thì không xét lặp

# D13 — câu rỗng: dẫn dắt, rào đón, nhấn mạnh không mang thông tin, động từ ẩn
CAU_RONG = [
    r"như (?:đã|ta đã|chúng ta đã) (?:nói|đề cập|thấy|trình bày)(?: ở trên| ở trước| trước đó)?",
    r"điều (?:quan trọng|cần nhớ|đáng chú ý)(?: cần lưu ý)? là",
    r"cần lưu ý rằng",
    r"(?:trong )?(?:phần|mục) này,? (?:chúng )?ta sẽ",
    r"mục này (?:sẽ )?(?:cho thấy|trình bày|giải thích|chỉ ra)",
    r"nói cách khác",
    r"(?:rất|cực kỳ|vô cùng) quan trọng",
    r"(?:chỉ )?đơn giản là",
    r"(?:ta |chúng ta )?có thể thấy (?:rằng|là)",
    r"dễ (?:thấy|dàng nhận thấy) (?:rằng|là)",
    r"(?:chúng ta )?hãy cùng",
    r"tiến hành (?=\w)",
]

# Viết tắt ai cũng biết hoặc là tên riêng — không đòi giải thích
VIET_TAT_CHUNG = {
    "CPU", "GPU", "RAM", "CSV", "PDF", "URL", "API", "HTTP", "HTTPS", "JSON", "ID", "OK", "USD", "VND",
    "VN", "TP", "HCM", "PNG", "SVG", "HTML", "SQL", "OS", "UTF", "GB", "MB", "KB", "TB?", "AI",
    "UCI", "NOAA", "EIA", "BLS", "BEA", "ERCOT", "ECMWF", "FPP", "IIF", "WMO", "CC", "BY", "CC0",
    "M1", "M2", "M3", "M4", "M5", "M6", "NN", "II", "III", "IV", "XYZ", "ABC", "USA", "US", "EU", "VS",
}
VIET_TAT_CHUNG.discard("TB?")

TU_THAM_CHIEU = r"(?:buổi|Buổi|mục|Mục|§|Bước|bước|ô|Ô|Câu|câu|Lab|lab|chương|Chương|Phụ lục|hình|Hình|phase|Phase|D|cột|dòng|Giai đoạn)"

NHAN = {
    "noi_bang_loi": re.compile(r"Nói bằng lời", re.I),
    "cach_doc_hinh": re.compile(r"Cách đọc hình", re.I),
    "doc_bang": re.compile(r"Đọc bảng", re.I),
    "tom_lai": re.compile(r"Tóm lại", re.I),
    "tu_kiem": re.compile(r"Tự kiểm tra", re.I),
    "muc_dich": re.compile(r"Mục đích", re.I),
    "doc_ket_qua": re.compile(r"Đọc kết quả", re.I),
    "muon_truoc": re.compile(r"Mượn trước", re.I),
    "nang_cao": re.compile(r"Nâng cao", re.I),
    "tu_moi": re.compile(r"Từ mới", re.I),
}


@dataclass
class ViPham:
    ma: str
    dong: int
    mo_ta: str


@dataclass
class KetQua:
    ten: str
    vi_pham: list[ViPham] = field(default_factory=list)

    def dem(self) -> dict[str, int]:
        d = dict.fromkeys(MA, 0)
        for v in self.vi_pham:
            d[v.ma] += 1
        return d


# ---------------------------------------------------------------- tiện ích văn bản

def _bo_inline(s: str) -> str:
    """Bỏ code inline, link URL, ảnh — giữ chữ và công thức inline."""
    s = re.sub(r"`[^`]*`", " ", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\]\([^)]*\)", "]", s)
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return s


def _bo_cong_thuc(s: str) -> str:
    return re.sub(r"\$[^$]*\$", " ", s)


def _dong_hop_le(lines: list[str]) -> list[bool]:
    """True nếu dòng KHÔNG nằm trong khối code ``` hoặc khối $$."""
    ok, trong_code, trong_tt = [], False, False
    for ln in lines:
        t = ln.strip()
        if t.startswith("```"):
            ok.append(False)
            trong_code = not trong_code
            continue
        if not trong_code and t == "$$":
            ok.append(False)
            trong_tt = not trong_tt
            continue
        ok.append(not (trong_code or trong_tt))
    return ok


def _muc(lines: list[str], so: str) -> tuple[int, int]:
    """(đầu, cuối) của mục '## <so>.' — cuối là dòng trước '## ' kế tiếp."""
    dau = next((i for i, ln in enumerate(lines) if re.match(rf"^## {so}\.", ln)), None)
    if dau is None:
        return (-1, -1)
    cuoi = next((i for i in range(dau + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return (dau, cuoi)


def _doan_van(lines: list[str], hop_le: list[bool], dau: int, cuoi: int):
    """Sinh (dòng_đầu, văn_bản) cho mỗi đoạn văn xuôi / mục danh sách trong [dau, cuoi)."""
    buf, bd = [], None

    def xa():
        nonlocal buf, bd
        if buf:
            yield bd, " ".join(buf)
        buf, bd = [], None

    for i in range(max(dau, 0), cuoi):
        ln = lines[i]
        t = ln.strip()
        la_van = (
            hop_le[i] and t and not t.startswith(("#", "|", "![", "<details", "</details", "<summary"))
            and not re.match(r"^-{3,}$", t)
        )
        if not la_van:
            yield from xa()
            continue
        if re.match(r"^\s*(?:>\s*)?(?:[-*]|\d+\.)\s", ln) and buf:
            yield from xa()
        if bd is None:
            bd = i + 1
        buf.append(re.sub(r"^\s*(?:>\s*)?(?:(?:[-*]|\d+\.)\s+)?", "", t))
    yield from xa()


PHEP_TINH = re.compile(r"\d%?\s*[+×=→−]\s*[-−]?\d|\d\s+trên\s+\d")


def _la_phep_tinh(s: str) -> bool:
    """Đoạn tính từng bước (có +, ×, =, →) — D7 không áp cho phép tính, chỉ cho đoạn dồn kết quả."""
    return bool(PHEP_TINH.search(_bo_cong_thuc(_bo_inline(s))))


def _dem_so(s: str) -> int:
    """Số con số KẾT QUẢ khác nhau trong đoạn: bỏ công thức, ngày giờ, năm, tham chiếu, dãy dữ liệu liệt kê."""
    s = _bo_cong_thuc(_bo_inline(s))
    s = re.sub(r"\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}:\d{2}|\d{1,2}/\d{4}|(?<![\d,.])\d{1,2}/\d{1,2}(?![\d/])", " ", s)
    s = re.sub(r"(?:năm|Năm|tháng|quý)\s+\d{4}(?:[–-]\d{2,4})?", " ", s)
    s = re.sub(r"(?:quantile|phân vị|mức)\s+\d[\d,.]*", " ", s, flags=re.I)
    s = re.sub(rf"{TU_THAM_CHIEU}\s*[0-9][0-9.,–\-]*", " ", s)
    s = re.sub(r"\d[\d.,]*(?:\s*(?:,|và)\s*\d[\d.,]*){2,}", " ", s)   # dãy dữ liệu: 5, 6, 6, 7 và 7
    return len(set(re.findall(r"(?<![\w.,])(?:[-+−])?(\d+(?:[.,]\d+)*%?)", s)))


def _cau(s: str) -> list[str]:
    s = _bo_cong_thuc(_bo_inline(s))
    return [c for c in re.split(r"(?<=[.!?:;])\s+(?=[A-ZÀ-Ỹ*(\"“])", s) if c.strip()]


def _so_chu(s: str) -> int:
    return len([w for w in re.split(r"\s+", s) if re.search(r"\w", w)])


# ---------------------------------------------------------------- Phụ lục E

@dataclass
class ThuatNgu:
    dang: list[str]          # các cách viết để tìm trong bài
    buoi_min: int | None
    ten: str


# Từ thường ngày trùng tên thuật ngữ — không dùng để dò
TU_CHUNG = {
    "giữ nguyên", "cảnh báo", "bất thường", "kỳ vọng", "dữ liệu", "mô hình", "dự báo", "tần suất",
    "không", "cộng", "nhân", "mức", "sai số", "chuỗi", "khoảng", "phân phối chuẩn", "tương lai",
    "một phần", "hoàn toàn", "độ trễ", "cửa sổ",
}


def _la_dang_dung_duoc(p: str) -> bool:
    """Dạng đủ đặc trưng để dò: tiếng Anh một từ ≥ 6 ký tự, hoặc cụm ≥ 2 từ không phải từ thường ngày."""
    if len(p) < 4 or p.startswith("…") or p.lower() in TU_CHUNG:
        return False
    tu = p.split()
    if len(tu) == 1:
        return bool(re.fullmatch(r"[A-Za-z\-]{6,}|[A-Z][A-Z0-9\-]{1,}", p))
    return True


def _tach_dang(o: str) -> list[str]:
    o = re.sub(r"\$[^$]*\$", " ", o)
    o = o.replace("`", "")
    ra = []
    ngoac = re.findall(r"\(([^)]*)\)", o)
    goc = re.sub(r"\([^)]*\)", " ", o)
    for phan in [goc, *ngoac]:
        for p in re.split(r"\s*/\s*|,\s*|;\s*", phan):
            p = p.strip(" .*")
            if _la_dang_dung_duoc(p):
                ra.append(p)
    return ra


def doc_phu_luc_e(duong_dan: Path = PHU_LUC_E) -> tuple[list[ThuatNgu], set[str]]:
    """Đọc mọi bảng có cột 'Tiếng Anh' và 'Buổi'. Trả (thuật ngữ, tập viết tắt xuất hiện)."""
    if not duong_dan.exists():
        return [], set()
    tn, viet_tat = [], set()
    cot = None
    for ln in duong_dan.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|"):
            cot = None
            continue
        o = [x.strip() for x in ln.strip().strip("|").split("|")]
        if cot is None:
            if "Tiếng Anh" in o:
                cot = {ten: i for i, ten in enumerate(o)}
            continue
        if set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        anh = o[cot["Tiếng Anh"]] if cot.get("Tiếng Anh") is not None and cot["Tiếng Anh"] < len(o) else ""
        viet = o[cot["Viết trong khoá"]] if "Viết trong khoá" in cot and cot["Viết trong khoá"] < len(o) else ""
        buoi = o[cot["Buổi"]] if "Buổi" in cot and cot["Buổi"] < len(o) else ""
        so = [int(x) for x in re.findall(r"\d+", buoi)]
        dang = list(dict.fromkeys(_tach_dang(anh) + _tach_dang(viet)))
        viet_tat |= set(re.findall(r"\b[A-Z][A-Z0-9]{1,6}\b", anh + " " + viet))
        if dang:
            tn.append(ThuatNgu(dang=dang, buoi_min=min(so) if so else None, ten=anh or viet))
    return tn, viet_tat


def _co_dung(van_ban: str, dang: str) -> re.Match | None:
    return re.search(rf"(?<!\w){re.escape(dang)}(?!\w)", van_ban, re.I)


# ---------------------------------------------------------------- kiểm tai-lieu.md

def kiem_tai_lieu(van_ban: str, so_buoi: int | None, thuat_ngu: list[ThuatNgu] | None = None,
                  viet_tat_e: set[str] | None = None) -> list[ViPham]:
    lines = van_ban.splitlines()
    hop_le = _dong_hop_le(lines)
    vp: list[ViPham] = []
    thuat_ngu = thuat_ngu or []
    viet_tat_e = viet_tat_e or set()

    ly_dau, ly_cuoi = _muc(lines, "4")
    lab_dau, lab_cuoi = _muc(lines, "5")
    doc_them_dau, _ = _muc(lines, "9")
    het_noi_dung = doc_them_dau if doc_them_dau >= 0 else len(lines)

    # --- bảng Từ mới (D1)
    tu_moi_terms: set[str] = set()
    co_bang_tu_moi = False
    if ly_dau >= 0:
        for i in range(ly_dau, ly_cuoi):
            if lines[i].startswith("#") and NHAN["tu_moi"].search(lines[i]):
                j = i + 1
                while j < ly_cuoi and not lines[j].startswith("#"):
                    if lines[j].startswith("|"):
                        co_bang_tu_moi = True
                        o = lines[j].strip().strip("|").split("|")
                        if o and not set(o[0].strip()) <= set("-: "):
                            tu_moi_terms.add(o[0].strip().strip("*`").lower())
                    j += 1
                break
    if not co_bang_tu_moi:
        vp.append(ViPham("tu_moi", ly_dau + 1 if ly_dau >= 0 else 1, 'thiếu bảng "Từ mới trong buổi"'))
    tu_moi_blob = " ".join(tu_moi_terms)

    # văn xuôi Lý thuyết + Lab để tìm thuật ngữ
    van_xuoi_ly_lab = " ".join(
        t for a, b in [(ly_dau, ly_cuoi), (lab_dau, lab_cuoi)] if a >= 0
        for _, t in _doan_van(lines, hop_le, a, b)
    )
    van_muon_truoc = " ".join(
        t for _, t in _doan_van(lines, hop_le, 0, het_noi_dung) if NHAN["muon_truoc"].search(t)
    )
    # hộp Mượn trước là blockquote nhiều dòng: gom cả khối
    khoi, trong = [], False
    for ln in lines:
        if ln.startswith(">") and NHAN["muon_truoc"].search(ln):
            trong = True
        if trong:
            if not ln.startswith(">"):
                trong = False
                continue
            khoi.append(ln)
    van_muon_truoc += " " + " ".join(khoi)

    # --- thuật ngữ E: chưa vào bảng (D1) / của buổi sau (D5)
    if so_buoi is not None:
        da_bao_tn: set[str] = set()
        for t in thuat_ngu:
            if t.buoi_min is None:
                continue
            m = next((m for d in t.dang if (m := _co_dung(van_xuoi_ly_lab, d))), None)
            if not m:
                continue
            dung = m.group(0)
            if dung.lower() in da_bao_tn:
                continue
            da_bao_tn.add(dung.lower())
            dong = next((i + 1 for i, ln in enumerate(lines) if hop_le[i] and _co_dung(ln, dung)), 0)
            trong_bang = any(_co_dung(tu_moi_blob, d) for d in t.dang)
            if t.buoi_min == so_buoi and not trong_bang:
                vp.append(ViPham("chua_bang", dong, f'"{dung}" (E: {t.ten}) chưa có trong bảng Từ mới'))
            elif t.buoi_min > so_buoi and not any(_co_dung(van_muon_truoc, d) for d in t.dang):
                vp.append(ViPham("muon_truoc", dong,
                                 f'"{dung}" là khái niệm buổi {t.buoi_min} — cần hộp "Mượn trước"'))

    # --- công thức (D3)
    i = 0
    while i < len(lines):
        if lines[i].strip() == "$$" and hop_le[i] is False:
            j = i + 1
            while j < len(lines) and lines[j].strip() != "$$":
                j += 1
            cua_so = []
            k = j + 1
            while k < len(lines) and k <= j + CUA_SO and not lines[k].startswith("#"):
                cua_so.append(lines[k])
                k += 1
            ke_tiep_la_cong_thuc = any(ln.strip() == "$$" for ln in cua_so[:3])
            if not ke_tiep_la_cong_thuc and not NHAN["noi_bang_loi"].search("\n".join(cua_so)):
                vp.append(ViPham("cong_thuc", i + 1, 'công thức thiếu "Nói bằng lời" ngay sau'))
            i = j + 1
            continue
        i += 1

    # --- hình (D8)
    for i, ln in enumerate(lines[:het_noi_dung]):
        if hop_le[i] and ln.strip().startswith("!["):
            cua_so = "\n".join(lines[i + 1:i + 1 + CUA_SO])
            if not NHAN["cach_doc_hinh"].search(cua_so):
                vp.append(ViPham("hinh", i + 1, 'ảnh thiếu "Cách đọc hình"'))

    # --- bảng kết quả (D8): chỉ trong Lý thuyết và Lab
    for a, b in [(ly_dau, ly_cuoi), (lab_dau, lab_cuoi)]:
        if a < 0:
            continue
        i = a
        while i < b:
            if hop_le[i] and lines[i].startswith("|"):
                j = i
                while j < b and lines[j].startswith("|"):
                    j += 1
                hang = [r for r in lines[i + 2:j]]
                o = [c for r in hang for c in r.strip().strip("|").split("|")]
                truoc = "\n".join(lines[max(a, i - 3):i])
                la_tu_moi = bool(NHAN["tu_moi"].search(truoc))
                if len(hang) >= 2 and o and not la_tu_moi:
                    ty_le_so = sum(bool(re.search(r"\d", c)) for c in o) / len(o)
                    if ty_le_so >= 0.5:
                        cua_so = "\n".join(lines[j:j + CUA_SO]) + "\n" + truoc
                        if not NHAN["doc_bang"].search(cua_so):
                            vp.append(ViPham("bang", i + 1, 'bảng kết quả thiếu "Đọc bảng"'))
                i = j
                continue
            i += 1

    # --- mục lý thuyết: số khái niệm (D9), Tóm lại (D2), Tự kiểm tra (D10)
    if ly_dau >= 0:
        dau_muc = [i for i in range(ly_dau, ly_cuoi) if lines[i].startswith("### ")]
        chinh = [
            i for i in dau_muc
            if not (NHAN["tu_moi"].search(lines[i]) or NHAN["nang_cao"].search(lines[i]))
        ]
        if len(chinh) > MAX_KHAI_NIEM:
            vp.extend(
                ViPham("khai_niem", i + 1, f"khái niệm chính thứ {n + 1} (tối đa {MAX_KHAI_NIEM})")
                for n, i in enumerate(chinh) if n >= MAX_KHAI_NIEM
            )
        for i in chinh:
            cuoi = next((k for k in dau_muc if k > i), ly_cuoi)
            than = "\n".join(lines[i:cuoi])
            if not NHAN["tom_lai"].search(than):
                vp.append(ViPham("tom_lai", i + 1, f'"{lines[i][4:].strip()}" thiếu "Tóm lại"'))
            if not NHAN["tu_kiem"].search(than):
                vp.append(ViPham("tu_kiem", i + 1, f'"{lines[i][4:].strip()}" thiếu "Tự kiểm tra"'))

    # --- bước lab (D11)
    if lab_dau >= 0:
        buoc = [i for i in range(lab_dau, lab_cuoi) if lines[i].startswith("### ")]
        for n, i in enumerate(buoc):
            cuoi = buoc[n + 1] if n + 1 < len(buoc) else lab_cuoi
            than = "\n".join(lines[i:cuoi])
            thieu = [ten for ten, k in [("Mục đích", "muc_dich"), ("Đọc kết quả", "doc_ket_qua")]
                     if not NHAN[k].search(than)]
            if thieu:
                vp.append(ViPham("lab", i + 1, f'"{lines[i][4:].strip()}" thiếu: {", ".join(thieu)}'))

    # --- văn xuôi: câu dài, nhiều số, tiếng Anh, viết tắt (D6, D7)
    da_bao_viet_tat: set[str] = set()
    for dong, doan in _doan_van(lines, hop_le, 0, het_noi_dung):
        if lines[dong - 1].lstrip().startswith("|"):
            continue
        for c in _cau(doan):
            n = _so_chu(c)
            if n > NGUONG_CAU:
                vp.append(ViPham("cau_dai", dong, f"câu {n} chữ: {c[:60]}…"))
        n_so = 0 if _la_phep_tinh(doan) else _dem_so(doan)
        if n_so > NGUONG_SO:
            vp.append(ViPham("nhieu_so", dong, f"{n_so} con số trong một đoạn: {doan[:60]}…"))
        for trich in re.findall(r"[\"“]([^\"”]+)[\"”]", _bo_inline(doan)):
            tu = trich.split()
            anh = [w for w in tu if re.fullmatch(r"[A-Za-z'’\-]+[.,;:!?]?", w)]
            if len(anh) >= NGUONG_TIENG_ANH and len(anh) >= 0.8 * len(tu) and not re.search(r"dịch|nghĩa là", doan, re.I):
                vp.append(ViPham("tieng_anh", dong, f'trích tiếng Anh chưa dịch: "{trich[:50]}…"'))
        for vt in re.findall(r"(?<![\w-])[A-Z][A-Z0-9]{1,5}(?![\w-])", _bo_cong_thuc(_bo_inline(doan))):
            if vt in da_bao_viet_tat or vt in VIET_TAT_CHUNG or vt in viet_tat_e or vt.isdigit():
                continue
            if re.search(rf"(?<!\w){vt}(?!\w)", tu_moi_blob, re.I):
                continue
            if re.fullmatch(r"[A-Z]\d+", vt):
                continue
            da_bao_viet_tat.add(vt)
            vp.append(ViPham("viet_tat", dong, f'viết tắt "{vt}" chưa giải thích'))

    vp += kiem_gon(lines, hop_le, ly_dau, ly_cuoi, het_noi_dung)
    return sorted(vp, key=lambda v: (v.dong, v.ma))


def _cap(s: str) -> set[tuple[str, str]]:
    """Tập cặp âm tiết liền nhau (chữ thường, bỏ dấu câu) — dùng đo lặp ý."""
    tu = re.findall(r"\w+", _bo_cong_thuc(_bo_inline(s)).lower())
    return set(zip(tu, tu[1:], strict=False))


def _trung(a: set, b: set) -> float:
    return len(a & b) / len(a) if a else 0.0


def kiem_gon(lines: list[str], hop_le: list[bool], ly_dau: int, ly_cuoi: int, het: int) -> list[ViPham]:
    """D13: câu rỗng; Tóm lại chép lại câu trong mục; hai đoạn gần trùng."""
    vp: list[ViPham] = []
    mau = re.compile("|".join(f"(?:{m})" for m in CAU_RONG), re.I)
    doan = [(d, t) for d, t in _doan_van(lines, hop_le, 0, het) if not lines[d - 1].lstrip().startswith("|")]
    for dong, t in doan:
        for m in mau.finditer(_bo_inline(t)):
            vp.append(ViPham("cau_rong", dong, f'câu rỗng "{m.group(0)}"'))

    # Tóm lại chép lại một câu trong cùng mục lý thuyết
    if ly_dau >= 0:
        dau_muc = [i for i in range(ly_dau, ly_cuoi) if lines[i].startswith("### ")] + [ly_cuoi]
        for a, b in zip(dau_muc, dau_muc[1:], strict=False):
            trong = [(d, t) for d, t in _doan_van(lines, hop_le, a, b)]
            tl = [(d, t) for d, t in trong if NHAN["tom_lai"].search(t[:20])]
            than = [c for d, t in trong if not NHAN["tom_lai"].search(t[:20]) for c in _cau(t)]
            for d, t in tl:
                for c in _cau(t):
                    ca = _cap(c)
                    if len(ca) < LAP_MIN_CHU:
                        continue
                    if any(_trung(ca, _cap(x)) >= NGUONG_LAP for x in than):
                        vp.append(ViPham("lap_y", d, f'"Tóm lại" chép lại câu trong mục: {c[:50]}…'))

    # hai đoạn gần như trùng nhau (bỏ qua đoạn nhãn ngắn)
    dai = [(d, t, _cap(t)) for d, t in doan if len(_cap(t)) >= 2 * LAP_MIN_CHU]
    for i, (d1, t1, c1) in enumerate(dai):
        for d2, _t2, c2 in dai[i + 1:]:
            if min(_trung(c1, c2), _trung(c2, c1)) >= NGUONG_LAP:
                vp.append(ViPham("lap_y", d2, f"đoạn gần trùng đoạn ở dòng {d1}: {t1[:40]}…"))
    return vp


def dem_chu(van_ban: str) -> int:
    """Số chữ (âm tiết) ngoài bảng và khối code — cách đếm độ dài chuẩn của khoá."""
    van_ban = re.sub(r"```.*?```", " ", van_ban, flags=re.S)
    dong = [ln for ln in van_ban.splitlines() if not ln.lstrip().startswith("|")]
    return sum(_so_chu(ln) for ln in dong)


# ---------------------------------------------------------------- kiểm kiem-tra.md

def kiem_quiz(van_ban: str) -> list[ViPham]:
    vp = []
    lines = van_ban.splitlines()
    i = 0
    cau_hoi_dau = 0
    while i < len(lines):
        if re.match(r"^\*\*Câu \d+", lines[i]):
            cau_hoi_dau = i
        if lines[i].strip().startswith("<details"):
            j = i + 1
            while j < len(lines) and "</details>" not in lines[j]:
                j += 1
            dap_an = " ".join(ln for ln in lines[i + 1:j] if "<summary" not in ln)
            de = "\n".join(lines[cau_hoi_dau:i])
            co_lua_chon = len(re.findall(r"^- [A-E]\.", de, re.M)) >= 2
            n = _so_chu(re.sub(r"<[^>]+>", " ", dap_an))
            chu_cai = set(re.findall(r"(?<![\w])([A-E])(?=[\s.)\],:]|$)", dap_an))
            if n < 20:
                vp.append(ViPham("quiz", i + 1, f"đáp án chỉ {n} chữ — chưa giải thích vì sao"))
            elif co_lua_chon and len(chu_cai) < 2:
                vp.append(ViPham("quiz", i + 1, "đáp án không nói vì sao các lựa chọn khác sai"))
            i = j
        i += 1
    return vp


# ---------------------------------------------------------------- chạy

def kiem_buoi(thu_muc: Path, thuat_ngu=None, viet_tat_e=None) -> KetQua:
    m = re.search(r"buoi-(\d+)", thu_muc.name)
    so = int(m.group(1)) if m else None
    kq = KetQua(thu_muc.name)
    tl = thu_muc / "tai-lieu.md"
    if tl.exists():
        van_ban = tl.read_text(encoding="utf-8")
        kq.vi_pham += kiem_tai_lieu(van_ban, so, thuat_ngu, viet_tat_e)
        n = dem_chu(van_ban)
        if not DO_DAI[0] <= n <= DO_DAI[1]:
            kq.vi_pham.append(ViPham("do_dai", 1, f"{n} chữ ngoài bảng/code (cần {DO_DAI[0]}–{DO_DAI[1]})"))
    kt = thu_muc / "kiem-tra.md"
    if kt.exists():
        kq.vi_pham += kiem_quiz(kt.read_text(encoding="utf-8"))
    return kq


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("buoi", nargs="*", help="số buổi hoặc đường dẫn thư mục; bỏ trống = mọi buổi")
    ap.add_argument("--chi-tiet", action="store_true", help="liệt kê từng vi phạm")
    ap.add_argument("--nghiem", action="store_true", help="mã thoát 1 nếu còn vi phạm")
    a = ap.parse_args(argv)

    if a.buoi:
        ds = [Path(b) if not b.isdigit() else GOC / f"buoi-{int(b):02d}" for b in a.buoi]
    else:
        ds = sorted(p for p in GOC.glob("buoi-[0-9][0-9]") if (p / "tai-lieu.md").exists())
    thuat_ngu, viet_tat_e = doc_phu_luc_e()

    ket_qua = [kiem_buoi(d, thuat_ngu, viet_tat_e) for d in ds]
    tieu_de = ["buổi", *MA, "tổng"]
    print("| " + " | ".join(tieu_de) + " |")
    print("|" + "---|" * len(tieu_de))
    for kq in ket_qua:
        d = kq.dem()
        print("| " + " | ".join([kq.ten, *(str(d[m]) for m in MA), str(sum(d.values()))]) + " |")
    if a.chi_tiet:
        for kq in ket_qua:
            print(f"\n## {kq.ten}")
            for v in kq.vi_pham:
                print(f"  dòng {v.dong:>4}  {v.ma:<11} {v.mo_ta}")
    tong = sum(len(k.vi_pham) for k in ket_qua)
    return 1 if (a.nghiem and tong) else 0


if __name__ == "__main__":
    sys.exit(main())
