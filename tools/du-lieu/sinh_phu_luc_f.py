"""Sinh phu-luc/F-nguon-du-lieu.md từ tools/du-lieu/danh-muc.toml — không sửa tay phụ lục F.

    python tools/du-lieu/sinh_phu_luc_f.py          ghi phu-luc/F-nguon-du-lieu.md
    python tools/du-lieu/sinh_phu_luc_f.py --kiem   báo lỗi nếu phụ lục đang lệch danh mục
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOC = HERE.parent.parent
DANH_MUC = HERE / "danh-muc.toml"
DICH = GOC / "phu-luc" / "F-nguon-du-lieu.md"

KIEU = {"http": "tải trực tiếp", "hf": "Hugging Face (commit chốt)", "kaggle": "Kaggle — tự đăng nhập",
        "eia": "EIA API v2 — cần key", "openaq": "OpenAQ API v3 — cần key"}


def dung(v: int | None) -> str:
    if not v:
        return "?"
    for don_vi in ("B", "KB", "MB", "GB"):
        if v < 1024 or don_vi == "GB":
            return f"{v:.0f} {don_vi}" if don_vi == "B" else f"{v:,.1f} {don_vi}".replace(",", ".")
        v /= 1024
    return "?"


def o(chu) -> str:
    return str(chu).replace("|", "\\|").replace("\n", " ")


def sinh() -> str:
    with open(DANH_MUC, "rb") as f:
        dm = tomllib.load(f)
    cac_bo = dm.get("bo", {})
    ngoai = dm.get("ngoai_danh_muc", {})
    tong = sum(b.get("dung_luong", 0) or 0 for b in cac_bo.values())

    dong = [
        "<!-- SINH TỰ ĐỘNG bởi tools/du-lieu/sinh_phu_luc_f.py từ tools/du-lieu/danh-muc.toml — KHÔNG SỬA TAY -->",
        "# Phụ lục F — Nguồn dữ liệu và giấy phép",
        "",
        "Mọi bộ dữ liệu buổi học tải tự động (`python lab.py up`) đều nằm trong danh mục này, kèm **giấy phép đã đọc từ trang",
        "gốc** (trích nguyên văn), sha256 và quyết định có được mirror không. Buổi học chỉ dùng được bộ đã chốt",
        "sha256. Nhật ký rà giấy phép đầy đủ: `tools/du-lieu/NGHIEN-CUU.md`.",
        "",
        "**Quy tắc:** CC BY / CC0 / public domain → được mirror (kèm ghi nguồn); giấy phép cấm phân phối lại → học",
        "viên tự tải bằng tài khoản của mình và luôn có bộ dự phòng mở; nguồn không có giấy phép rõ → không mirror.",
        "",
        f"Danh mục có **{len(cac_bo)} bộ**, tổng dung lượng tải khoảng **{dung(tong)}** (không tính bộ chưa rõ dung lượng).",
        "",
        "## Bảng tổng quan",
        "",
        "| Bộ | Giấy phép | Mirror | Cách tải | Dung lượng | Buổi | Trạng thái |",
        "|---|---|---|---|---|---|---|",
    ]
    for ten, b in sorted(cac_bo.items()):
        trang_thai = "chờ sha256" if b.get("cho_sha256") else ("trực tiếp" if b.get("truc_tiep") else "đã chốt")
        dong.append(f"| `{ten}` | {o(b.get('giay_phep', '?'))} | {'có' if b.get('mirror') else 'không'} | "
                    f"{KIEU.get(b.get('kieu'), b.get('kieu'))} | {dung(b.get('dung_luong'))} | "
                    f"{', '.join(map(str, b.get('buoi', []))) or '—'} | {trang_thai} |")
    dong += ["", "## Chi tiết từng bộ", ""]
    for ten, b in sorted(cac_bo.items()):
        dong += [f"### `{ten}` — {b.get('tieu_de', '')}", ""]
        dong.append(f"- **Nguồn:** <{b.get('trang_nguon', '')}>")
        if b.get("url"):
            dong.append(f"- **Tệp tải:** `{b['url']}`")
        if b.get("kaggle"):
            dong.append(f"- **Kaggle:** `{b['kaggle']}`")
        dong.append(f"- **Giấy phép:** {b.get('giay_phep', '?')} — <{b.get('link_giay_phep', '')}>")
        if b.get("trich_giay_phep"):
            dong.append(f"- **Trích nguyên văn:** \"{b['trich_giay_phep'].strip()}\"")
        dong.append(f"- **Mirror:** {'được' if b.get('mirror') else 'không'}"
                    + (f" — {b['ly_do_mirror']}" if b.get("ly_do_mirror") else ""))
        if b.get("du_phong"):
            dong.append(f"- **Bộ dự phòng mở:** `{b['du_phong']}`")
        if b.get("khoang_thoi_gian"):
            dong.append(f"- **Khoảng thời gian cố định:** {' → '.join(b['khoang_thoi_gian'])}")
        if b.get("sha256"):
            dong.append(f"- **sha256:** `{b['sha256']}` ({dung(b.get('dung_luong'))})")
        if b.get("tep_sha256"):
            dong.append("- **sha256 theo tệp:** " + ", ".join(f"`{k}` `{v[:12]}…`" for k, v in b["tep_sha256"].items()))
        if b.get("cho_sha256"):
            dong.append(f"- **Chưa chốt sha256:** {b['cho_sha256']}")
        if b.get("ghi_nguon"):
            dong.append(f"- **Trích dẫn:** {b['ghi_nguon']}")
        if b.get("ghi_chu"):
            dong.append(f"- **Ghi chú:** {b['ghi_chu'].strip()}")
        dong.append(f"- **Xác minh:** {b.get('xac_minh', '?')}")
        dong.append("")
    if ngoai:
        dong += ["## Nguồn KHÔNG đưa vào danh mục tải tự động", "",
                 "Có trong lộ trình nhưng giấy phép không cho tải tự động / phân phối lại, hoặc không có giấy phép rõ.", "",
                 "| Nguồn | Điều khoản (trích) | Vì sao không tự động | Thay bằng |", "|---|---|---|---|"]
        for ten, n in sorted(ngoai.items()):
            dong.append(f"| {o(n.get('tieu_de', ten))} (<{n.get('trang_nguon', '')}>) | \"{o(n.get('trich_giay_phep', ''))}\" | "
                        f"{o(n.get('ly_do', ''))} | {o(n.get('du_phong', '—'))} |")
        dong.append("")
    return "\n".join(dong)


def main(argv: list[str]) -> int:
    noi_dung = sinh()
    if "--kiem" in argv:
        if not DICH.is_file() or DICH.read_text(encoding="utf-8") != noi_dung:
            print("✗ phu-luc/F-nguon-du-lieu.md lệch danh mục — chạy tools/du-lieu/sinh_phu_luc_f.py", file=sys.stderr)
            return 1
        print("✓ Phụ lục F khớp danh mục")
        return 0
    DICH.write_text(noi_dung, encoding="utf-8")
    print(f"✓ {DICH.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
