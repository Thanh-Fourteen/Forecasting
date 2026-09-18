"""Xuat tai lieu Markdown cua khoa ra PDF nam canh file nguon.

    cd tools
    python xuat_pdf.py            # trang le (lo trinh, phu luc, de du an) + ca 44 buoi
    python xuat_pdf.py 5 6        # rieng buoi 05 va 06
    python xuat_pdf.py lo-trinh   # rieng cac trang le co chuoi "lo-trinh" trong duong dan
    python xuat_pdf.py --kiem     # dem so trang moi PDF da sinh, bao buoi ngoai 10-16 trang

Can:  pip install -r tools/requirements.txt
      (markdown-it-py, mdit-py-plugins, weasyprint, ziamath, pypdf)

Dung markdown-it-py (chuan CommonMark) chu khong dung python-markdown: tai lieu co
bang va khoi code nam trong danh sach, python-markdown lam vo nhung khoi do.

Cong thuc toan: `$...$` (trong dong) va `$$...$$` (khoi rieng) viet bang LaTeX, duoc
ziamath ve thanh SVG nhung thang vao PDF — khong can cai LaTeX. Plugin dollarmath nhan
dien cong thuc theo token, nen `$` nam trong khoi code hay trong "10 $" khong bi hieu nham.

Trong bang, `|` trong cong thuc tu doi thanh \\vert (neu khong se cat doi o bang).

Anh: viet duong dan tuong doi, vd `![ACF](hinh/acf.png)` — goc la thu muc chua file .md.

Khoi <details> (phan dap an quiz) duoc bung ra truoc khi render — trong PDF khong co
gi bam vao de mo.
"""
import base64
import html
import logging
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(HERE)

# buoi -> (ten file .pdf sinh ra, tieu de trang). Nguon luon la buoi-NN/tai-lieu.md
BUOI = {
    1:  ("GIOI-THIEU-buoi-01.pdf",           "Buổi 1 — Forecasting là gì"),
    2:  ("XAC-SUAT-THONG-KE-buoi-02.pdf",    "Buổi 2 — Xác suất và thống kê cho dự báo"),
    3:  ("DU-LIEU-THOI-GIAN-buoi-03.pdf",    "Buổi 3 — Dữ liệu thời gian với pandas, polars, DuckDB"),
    4:  ("BIEU-DO-buoi-04.pdf",              "Buổi 4 — Đọc và vẽ biểu đồ chuỗi thời gian"),
    5:  ("BIEN-DOI-DIEU-CHINH-buoi-05.pdf",  "Buổi 5 — Biến đổi và điều chỉnh dữ liệu"),
    6:  ("PHAN-RA-buoi-06.pdf",              "Buổi 6 — Phân rã chuỗi thời gian"),
    7:  ("TU-TUONG-QUAN-buoi-07.pdf",        "Buổi 7 — Tự tương quan và tính dừng"),
    8:  ("TUONG-QUAN-CHEO-buoi-08.pdf",      "Buổi 8 — Tương quan giữa các chuỗi"),
    9:  ("DAC-TRUNG-CHUOI-buoi-09.pdf",      "Buổi 9 — Đặc trưng chuỗi và khả năng dự báo"),
    10: ("LAM-SACH-DU-LIEU-buoi-10.pdf",     "Buổi 10 — Làm sạch và dữ liệu thiếu"),
    11: ("NGOAI-LAI-DIEM-GAY-buoi-11.pdf",   "Buổi 11 — Ngoại lai và điểm gãy"),
    12: ("KHU-NHIEU-TAN-SO-buoi-12.pdf",     "Buổi 12 — Khử nhiễu và miền tần số"),
    13: ("FEATURE-RO-RI-buoi-13.pdf",        "Buổi 13 — Feature engineering và chống rò rỉ"),
    14: ("BASELINE-CHI-SO-buoi-14.pdf",      "Buổi 14 — Baseline và chỉ số đánh giá"),
    15: ("BACKTEST-buoi-15.pdf",             "Buổi 15 — Backtesting đúng cách"),
    16: ("ETS-THETA-buoi-16.pdf",            "Buổi 16 — Exponential smoothing và Theta"),
    17: ("ARIMA-buoi-17.pdf",                "Buổi 17 — ARIMA và SARIMA"),
    18: ("HOI-QUY-DONG-buoi-18.pdf",         "Buổi 18 — Hồi quy chuỗi thời gian và hồi quy động"),
    19: ("NHU-CAU-GIAN-DOAN-buoi-19.pdf",    "Buổi 19 — Nhu cầu gián đoạn"),
    20: ("DA-BIEN-STATE-SPACE-buoi-20.pdf",  "Buổi 20 — Đa biến, state space và nowcasting"),
    21: ("TAI-CHINH-GARCH-buoi-21.pdf",      "Buổi 21 — Chuỗi tài chính và biến động"),
    22: ("ML-HOI-QUY-buoi-22.pdf",           "Buổi 22 — Biến dự báo thành bài toán hồi quy"),
    23: ("GRADIENT-BOOSTING-buoi-23.pdf",    "Buổi 23 — Gradient boosting chuyên sâu"),
    24: ("ENSEMBLE-AUTOML-buoi-24.pdf",      "Buổi 24 — Ensemble, AutoML và ca khó"),
    25: ("DU-BAO-XAC-SUAT-buoi-25.pdf",      "Buổi 25 — Dự báo xác suất"),
    26: ("CONFORMAL-buoi-26.pdf",            "Buổi 26 — Conformal prediction cho chuỗi thời gian"),
    27: ("BAYES-GP-buoi-27.pdf",             "Buổi 27 — Dự báo Bayes và Gaussian Process"),
    28: ("PHAN-CAP-buoi-28.pdf",             "Buổi 28 — Dự báo phân cấp và reconciliation"),
    29: ("DEEP-LEARNING-NEN-buoi-29.pdf",    "Buổi 29 — Nền deep learning cho chuỗi thời gian"),
    30: ("NBEATS-TFT-buoi-30.pdf",           "Buổi 30 — N-BEATS, N-HiTS, DeepAR, TFT, TiDE"),
    31: ("TRANSFORMER-buoi-31.pdf",          "Buổi 31 — Transformer cho chuỗi thời gian"),
    32: ("MO-HINH-SINH-buoi-32.pdf",         "Buổi 32 — Mô hình sinh và dữ liệu tổng hợp"),
    33: ("KHONG-GIAN-THOI-TIET-buoi-33.pdf", "Buổi 33 — Không gian–thời gian và thời tiết AI"),
    34: ("FOUNDATION-MODEL-buoi-34.pdf",     "Buổi 34 — Time series foundation model"),
    35: ("FINE-TUNE-BENCHMARK-buoi-35.pdf",  "Buổi 35 — Fine-tune, covariates và đọc benchmark"),
    36: ("LLM-AGENT-buoi-36.pdf",            "Buổi 36 — LLM và agent trong pipeline dự báo"),
    37: ("DU-BAO-SU-KIEN-buoi-37.pdf",       "Buổi 37 — Dự báo sự kiện bằng LLM"),
    38: ("TAC-DONG-CAN-THIEP-buoi-38.pdf",   "Buổi 38 — Đo tác động của can thiệp"),
    39: ("KICH-BAN-WHAT-IF-buoi-39.pdf",     "Buổi 39 — Kịch bản và what-if"),
    40: ("DU-BAO-QUYET-DINH-buoi-40.pdf",    "Buổi 40 — Từ dự báo đến quyết định"),
    41: ("PIPELINE-TAI-LAP-buoi-41.pdf",     "Buổi 41 — Pipeline dự báo tái lập được"),
    42: ("PHUC-VU-QUY-MO-buoi-42.pdf",       "Buổi 42 — Phục vụ dự báo ở quy mô lớn"),
    43: ("GIAM-SAT-DRIFT-buoi-43.pdf",       "Buổi 43 — Giám sát, drift và retrain"),
    44: ("DU-AN-CUOI-buoi-44.pdf",           "Buổi 44 — Dự án cuối khoá"),
}

# Cac trang khong thuoc buoi nao: (md nguon, pdf sinh ra, tieu de, co trang bia + muc luc)
# Duong dan tinh tu goc repo. File chua co thi bo qua.
TRANG_LE = [
    ("lo-trinh/lo-trinh-forecasting.md", "lo-trinh/lo-trinh-forecasting.pdf",
     "Lộ trình Forecasting in AI — từ cơ bản đến nâng cao", True),
    ("MOI-TRUONG.md", "MOI-TRUONG.pdf",
     "Chuẩn bị môi trường học", False),
    ("du-an-giua-chang/01-eda-lam-sach/de-bai.md",
     "du-an-giua-chang/01-eda-lam-sach/DU-AN-GIUA-CHANG-1.pdf",
     "Dự án giữa chặng 1 — EDA và pipeline làm sạch", True),
    ("du-an-giua-chang/02-thi-du-bao/de-bai.md",
     "du-an-giua-chang/02-thi-du-bao/DU-AN-GIUA-CHANG-2.pdf",
     "Dự án giữa chặng 2 — thi dự báo trên holdout tương lai", True),
    ("du-an-cuoi/de-bai.md", "du-an-cuoi/DU-AN-CUOI.pdf",
     "Dự án cuối khoá — hệ thống dự báo thực tế", True),
    ("phu-luc/A-python-chuoi-thoi-gian.md", "phu-luc/PHU-LUC-A-python.pdf",
     "Phụ lục A — Python cho chuỗi thời gian", False),
    ("phu-luc/B-xac-suat-toi-thieu.md", "phu-luc/PHU-LUC-B-xac-suat.pdf",
     "Phụ lục B — xác suất thống kê tối thiểu", False),
    ("phu-luc/C-so-tay-doc-bieu-do.md", "phu-luc/PHU-LUC-C-bieu-do.pdf",
     "Phụ lục C — sổ tay đọc biểu đồ", False),
    ("phu-luc/D-cong-thuc-chi-so.md", "phu-luc/PHU-LUC-D-chi-so.pdf",
     "Phụ lục D — bảng công thức chỉ số đánh giá", False),
    ("phu-luc/E-tu-dien-thuat-ngu.md", "phu-luc/PHU-LUC-E-tu-dien.pdf",
     "Phụ lục E — từ điển thuật ngữ Anh–Việt", False),
    ("phu-luc/F-nguon-du-lieu.md", "phu-luc/PHU-LUC-F-du-lieu.pdf",
     "Phụ lục F — nguồn dữ liệu và giấy phép", False),
]

# So trang cho phep cua PDF moi buoi (CLAUDE.md, quy tac do dai)
TRANG_TOI_THIEU, TRANG_TOI_DA = 10, 16


CSS = """
@page { size: A4; margin: 17mm 15mm 15mm; @bottom-center {
    content: counter(page) " / " counter(pages); font-family: "DejaVu Sans", sans-serif;
    font-size: 8pt; color: #8894a3; } }
@page bia { @bottom-center { content: none; } }
body { font-family: "DejaVu Sans", sans-serif; font-size: 9.5pt; line-height: 1.5;
       color: #1a1a1a; }
h1 { font-size: 20pt; color: #00695C; border-bottom: 3px solid #FFB300;
     padding-bottom: 5px; margin-bottom: 4pt; }
h2 { font-size: 14pt; color: #00695C; margin-top: 20pt; padding-top: 3pt;
     border-top: 1px solid #dde3ea; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #0A2540; margin-top: 13pt; page-break-after: avoid; }
h4 { font-size: 10pt; color: #0A2540; margin-top: 10pt; page-break-after: avoid; }
p, li { orphans: 2; widows: 2; }
code { font-family: "Liberation Mono", "DejaVu Sans Mono", monospace; font-size: 8.5pt;
       background: #eef2f7; padding: 1px 3px; border-radius: 3px; color: #0A2540; }
pre { font-family: "Liberation Mono", "DejaVu Sans Mono", monospace;
      background: #f7f9fc; border: 1px solid #dde3ea; border-left: 3px solid #00695C;
      padding: 7px 9px; border-radius: 3px; margin: 7pt 0; white-space: pre-wrap;
      orphans: 3; widows: 3; }
pre code { background: none; padding: 0; font-size: 8pt; line-height: 1.35; color: #14213d; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 8.5pt; }
tr { page-break-inside: avoid; }
thead { display: table-header-group; }
th, td { border: 1px solid #d6dce2; padding: 4px 6px; text-align: left;
         vertical-align: top; }
th { background: #00695C; color: #fff; font-weight: bold; }
tr:nth-child(even) td { background: #f4f9f8; }
blockquote { border-left: 3px solid #FFB300; background: #fffaf0; margin: 8pt 0;
             padding: 6px 10px; page-break-inside: avoid; }
blockquote p { margin: 0 0 4pt; }
blockquote p:last-child { margin-bottom: 0; }
a { color: #00695C; text-decoration: none; }
hr { border: none; border-top: 1px solid #dde3ea; margin: 14pt 0; }
hr + h2 { border-top: none; margin-top: 6pt; }
strong { color: #0A2540; }
img { max-width: 100%; }
p > img:only-child { display: block; margin: 6pt auto; }
.cong-thuc-khoi { text-align: center; margin: 8pt 0; page-break-inside: avoid; }
.cong-thuc-khoi img { max-width: 100%; }

.bia { page: bia; page-break-after: always; height: 240mm; display: flex;
       flex-direction: column; justify-content: center; }
.bia .nhan { color: #FFB300; font-weight: bold; letter-spacing: 2px; font-size: 10pt; }
.bia h1.tieu-de-bia { font-size: 28pt; border: none; line-height: 1.2; margin: 6pt 0 10pt; }
.bia .phu { color: #555; font-size: 11pt; }
.muc-luc { page-break-after: always; }
.muc-luc h2 { border-top: none; margin-top: 0; }
.muc-luc ul { list-style: none; padding-left: 0; margin: 0; }
.muc-luc ul ul { padding-left: 14pt; }
.muc-luc li { margin: 2pt 0; }
.muc-luc li.cap-2 > a { font-weight: bold; }
.muc-luc a { color: #1a1a1a; }
.muc-luc a::after { content: leader('.') target-counter(attr(href), page);
                    color: #8894a3; }
"""


def mo_details(van_ban):
    """Bung khối <details> thành mục thường — PDF không bấm mở được."""
    van_ban = re.sub(r"<summary>\s*(.*?)\s*</summary>",
                     lambda m: "### " + re.sub(r"</?b>", "", m.group(1)),
                     van_ban, flags=re.S)
    return van_ban.replace("<details>", "").replace("</details>", "")


def thoat_gach_dung_trong_bang(van_ban):
    """Trong dòng bảng, `|` nằm trong $...$ sẽ cắt đôi ô — đổi thành \\vert trước khi parse."""
    def sua_dong(dong):
        if not dong.lstrip().startswith("|"):
            return dong
        return re.sub(r"\$[^$\n]+?\$", lambda m: m.group(0).replace("|", r"\vert{}"), dong)
    return "\n".join(sua_dong(d) for d in van_ban.split("\n"))


def _svg_img(latex, co_chu, khoi):
    """LaTeX -> thẻ <img> chứa SVG. Trong dòng thì hạ ảnh xuống đúng đường chân chữ."""
    import ziamath as zm

    try:
        svg = zm.Latex(latex, size=co_chu).svg()
    except Exception as loi:  # công thức sai cú pháp: in nguyên văn, đừng làm hỏng cả file
        print(f"    ! công thức lỗi ({loi}): {latex[:60]}", file=sys.stderr)
        return f"<code>{html.escape(latex)}</code>"

    du_lieu = base64.b64encode(svg.encode()).decode()
    if khoi:
        return (f"<div class='cong-thuc-khoi'>"
                f"<img src='data:image/svg+xml;base64,{du_lieu}'></div>\n")

    # viewBox="x y w h": y âm là phần nằm trên đường chân chữ, phần còn lại (h + y) nằm dưới
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', svg)
    ha_xuong = float(m.group(4)) + float(m.group(2)) if m else 0.0
    return (f"<img src='data:image/svg+xml;base64,{du_lieu}' "
            f"style='vertical-align: -{ha_xuong:.2f}px'>")


def _tao_markdown():
    from markdown_it import MarkdownIt
    from mdit_py_plugins.dollarmath import dollarmath_plugin

    md = MarkdownIt("commonmark").enable("table")
    # allow_space/allow_digits = False: "từ 5 $ đến 10 $" không bị coi là công thức
    dollarmath_plugin(md, allow_space=False, allow_digits=False, double_inline=True)
    md.add_render_rule("math_inline", lambda s, t, i, o, e: _svg_img(t[i].content, 13, False))
    md.add_render_rule("math_inline_double", lambda s, t, i, o, e: _svg_img(t[i].content, 15, True))
    md.add_render_rule("math_block", lambda s, t, i, o, e: _svg_img(t[i].content, 15, True))
    md.add_render_rule("math_block_label", lambda s, t, i, o, e: _svg_img(t[i].content, 15, True))
    return md


def slug_github(chu):
    """Slug giống GitHub: chữ thường, bỏ dấu câu (giữ chữ có dấu), khoảng trắng -> '-'."""
    return re.sub(r"[^\w\- ]", "", chu.strip().lower()).replace(" ", "-")


def _gan_id_heading(tokens, do_sau):
    """Gắn id kiểu GitHub cho MỌI heading (link `#muc` trong md chạy được trong PDF).

    Trả về danh sách (cấp, id, chữ) của H2..H(do_sau) để dựng mục lục.
    """
    muc, da_dung = [], {}
    for i, tok in enumerate(tokens):
        if tok.type != "heading_open":
            continue
        chu = "".join(c.content for c in (tokens[i + 1].children or [])
                      if c.type in ("text", "code_inline"))
        goc = slug_github(chu)
        ma = goc if goc not in da_dung else f"{goc}-{da_dung[goc]}"
        da_dung[goc] = da_dung.get(goc, 0) + 1
        tok.attrSet("id", ma)
        cap = int(tok.tag[1])
        if 2 <= cap <= do_sau:
            muc.append((cap, ma, chu))
    return muc


def bo_muc_luc_viet_tay(van_ban):
    """Bỏ mục '## Mục lục' viết tay trong md — PDF đã có mục lục tự sinh kèm số trang."""
    return re.sub(r"^## Mục lục\s*\n.*?(?=^## |^---\s*$)", "", van_ban,
                  flags=re.S | re.M)


def _dung_muc_luc(muc):
    if not muc:
        return ""
    dong = ["<div class='muc-luc'><h2>Mục lục</h2><ul>"]
    cap_truoc = 2
    for cap, ma, chu in muc:
        if cap > cap_truoc:
            dong.append("<ul>")
        elif cap < cap_truoc:
            dong.append("</ul>")
        dong.append(f"<li class='cap-{cap}'><a href='#{ma}'>{html.escape(chu)}</a></li>")
        cap_truoc = cap
    dong.append("</ul>" * (cap_truoc - 1) + "</div>")
    return "\n".join(dong)


def xuat(duong_dan_md, duong_dan_pdf, tieu_de, bia=False):
    from weasyprint import CSS as WeasyCSS
    from weasyprint import HTML

    if not os.path.exists(duong_dan_md):
        return "BỎ QUA — chưa có tài liệu"
    with open(duong_dan_md, encoding="utf-8") as f:
        noi_dung = thoat_gach_dung_trong_bang(mo_details(f.read()))
    if bia:
        noi_dung = bo_muc_luc_viet_tay(noi_dung)

    md = _tao_markdown()
    tokens = md.parse(noi_dung)
    muc = _gan_id_heading(tokens, do_sau=3 if bia else 2)
    dau = ""
    if bia:
        dau = (f"<section class='bia'><div class='nhan'>KHOÁ FORECASTING IN AI</div>"
               f"<h1 class='tieu-de-bia'>{html.escape(tieu_de)}</h1>"
               f"<div class='phu'>Xuất ngày {date.today():%d/%m/%Y}</div></section>"
               + _dung_muc_luc(muc))
    than = md.renderer.render(tokens, md.options, {})
    than = re.sub(r"<p>\s*</p>", "", than)
    trang = (f"<html><head><meta charset='utf-8'><title>{html.escape(tieu_de)}</title>"
             f"</head><body>{dau}{than}</body></html>")

    os.makedirs(os.path.dirname(duong_dan_pdf), exist_ok=True)
    HTML(string=trang, base_url=os.path.dirname(os.path.abspath(duong_dan_md))).write_pdf(
        duong_dan_pdf, stylesheets=[WeasyCSS(string=CSS)])
    return f"{os.path.getsize(duong_dan_pdf) / 1024:.0f} KB"


def xuat_buoi(buoi):
    ten_pdf, tieu_de = BUOI[buoi]
    thu_muc = os.path.join(GOC, f"buoi-{buoi:02d}")
    ket_qua = xuat(os.path.join(thu_muc, "tai-lieu.md"),
                   os.path.join(thu_muc, ten_pdf), tieu_de)
    print(f"  buoi-{buoi:02d}/{ten_pdf:<36} {ket_qua}")


def kiem_so_trang():
    """In số trang mọi PDF đã sinh; buổi nằm ngoài 10–16 trang bị đánh dấu."""
    from pypdf import PdfReader

    vi_pham = 0
    for buoi, (ten_pdf, _) in sorted(BUOI.items()):
        duong_dan = os.path.join(GOC, f"buoi-{buoi:02d}", ten_pdf)
        if not os.path.exists(duong_dan):
            continue
        so = len(PdfReader(duong_dan).pages)
        dat = TRANG_TOI_THIEU <= so <= TRANG_TOI_DA
        vi_pham += not dat
        print(f"  buoi-{buoi:02d}/{ten_pdf:<36} {so:>3} trang  {'' if dat else '<-- ngoài 10–16'}")
    for _, ten_pdf, _, _ in TRANG_LE:
        duong_dan = os.path.join(GOC, ten_pdf)
        if os.path.exists(duong_dan):
            print(f"  {ten_pdf:<46} {len(PdfReader(duong_dan).pages):>3} trang")
    return vi_pham


def main():
    try:
        import markdown_it  # noqa: F401
        import mdit_py_plugins  # noqa: F401
        import weasyprint  # noqa: F401
        import ziamath  # noqa: F401
    except ImportError:
        sys.exit("Thiếu thư viện. Chạy:  pip install -r tools/requirements.txt")
    # weasyprint cảnh báo font subset rất ồn, không ảnh hưởng kết quả
    logging.getLogger("weasyprint").setLevel(logging.ERROR)
    logging.getLogger("fontTools").setLevel(logging.ERROR)

    tham_so = sys.argv[1:]
    if "--kiem" in tham_so:
        sys.exit(1 if kiem_so_trang() else 0)

    chi_le = [t for t in tham_so if not t.isdigit()]
    cac_buoi = [int(t) for t in tham_so if t.isdigit()]
    sai = [b for b in cac_buoi if b not in BUOI]
    if sai:
        sys.exit(f"Không có buổi {sai} — khoá có buổi 1..{max(BUOI)}")

    if not tham_so or chi_le:
        for ten_md, ten_pdf, tieu_de, bia in TRANG_LE:
            if chi_le and not any(t in ten_md for t in chi_le):
                continue
            ket_qua = xuat(os.path.join(GOC, ten_md), os.path.join(GOC, ten_pdf), tieu_de, bia)
            print(f"  {ten_pdf:<46} {ket_qua}")

    for buoi in (cac_buoi or (sorted(BUOI) if not chi_le else [])):
        xuat_buoi(buoi)


if __name__ == "__main__":
    main()
