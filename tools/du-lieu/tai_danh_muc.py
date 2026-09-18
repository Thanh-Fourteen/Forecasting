"""Tải TOÀN BỘ danh mục dữ liệu để kiểm sha256 (tiêu chí xong của Phase 1, và rà định kỳ).

    python tools/du-lieu/tai_danh_muc.py                    cache thật ~/.cache/khoa-forecasting
    python tools/du-lieu/tai_danh_muc.py --may-trang        cache + thư mục đặt dữ liệu mới tinh (tạm)
    python tools/du-lieu/tai_danh_muc.py --chi a,b          chỉ vài bộ
    python tools/du-lieu/tai_danh_muc.py --tac-gia          gồm cả bộ cho_sha256: tải rồi IN sha256 để chốt
    python tools/du-lieu/tai_danh_muc.py --bo-qua-khoa      bỏ các bộ cần tài khoản/API key không có sẵn

Kết quả: bảng từng bộ (khớp / lỗi / bỏ qua + lý do), tổng dung lượng tải, tổng thời gian.
Ghi nhật ký vào tools/du-lieu/nhat-ky-tai/<ngày>.md (gitignore).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import time
import tomllib
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(TOOLS))
from sinh_nen import dung_du_lieu_toml  # noqa: E402

CAN_KHOA = {"kaggle": "tài khoản Kaggle", "eia": "EIA_API_KEY", "openaq": "OPENAQ_API_KEY"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--may-trang", action="store_true")
    ap.add_argument("--chi")
    ap.add_argument("--tru", help="bỏ các bộ này (vd chạy riêng nguồn chậm song song)")
    ap.add_argument("--tac-gia", action="store_true")
    ap.add_argument("--bo-qua-khoa", action="store_true")
    t = ap.parse_args(argv)

    with open(HERE / "danh-muc.toml", "rb") as f:
        dm = tomllib.load(f)
    cac_bo = [{"ten": ten, **b} for ten, b in dm["bo"].items()]
    if t.chi:
        muon = set(t.chi.split(","))
        cac_bo = [b for b in cac_bo if b["ten"] in muon]
    if t.tru:
        bo_ra = set(t.tru.split(","))
        cac_bo = [b for b in cac_bo if b["ten"] not in bo_ra]

    bang: list[tuple[str, str, float, int]] = []
    chay: list[dict] = []
    for bo in cac_bo:
        if bo.get("cho_sha256") and not t.tac_gia:
            bang.append((bo["ten"], f"bỏ qua — chưa chốt sha256 ({bo['cho_sha256'][:60]})", 0, 0))
        elif t.bo_qua_khoa and bo["kieu"] in CAN_KHOA and not (
                bo["kieu"] != "kaggle" and os.environ.get(CAN_KHOA[bo["kieu"]])):
            bang.append((bo["ten"], f"bỏ qua — cần {CAN_KHOA[bo['kieu']]}", 0, 0))
        else:
            chay.append(bo)

    tam = tempfile.mkdtemp(prefix="tai-danh-muc-")
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    if t.may_trang:
        env["KHOA_FORECASTING_CACHE"] = f"{tam}/cache"
    nen = Path(tam) / "lab" / "00-nen"
    nen.mkdir(parents=True)
    bat_dau_tong = time.monotonic()
    for bo in chay:
        # mỗi bộ một lần gọi để đo thời gian và cô lập lỗi
        (nen / "du-lieu.toml").write_text(dung_du_lieu_toml(Path("buoi-kiem"), [bo]), encoding="utf-8")
        bat_dau = time.monotonic()
        kq = subprocess.run([sys.executable, str(TOOLS / "lay_du_lieu.py"), str(nen / "du-lieu.toml"),
                             *(["--tac-gia"] if t.tac_gia else [])], capture_output=True, text=True, env=env)
        giay = time.monotonic() - bat_dau
        raw = Path(tam) / "lab" / "du-lieu" / "raw" / bo["ten"]
        dung = sum(p.stat().st_size for p in raw.rglob("*") if p.is_file()) if raw.exists() else 0
        if kq.returncode == 0:
            sha = [d for d in kq.stdout.splitlines() if d.startswith("sha256 =")]
            trang_thai = "✓ sha256 khớp" if not bo.get("cho_sha256") else f"✓ tải xong — {sha[0] if sha else ''}"
        else:
            loi = [d.strip() for d in kq.stderr.splitlines() if d.strip().startswith(("✗", "-", "chốt", "tải về"))]
            trang_thai = "✗ " + " | ".join(loi)[:300]
        bang.append((bo["ten"], trang_thai, giay, dung))
        print(f"{bo['ten']:<32} {trang_thai[:110]}  ({giay:.1f}s)", flush=True)

    tong_giay = time.monotonic() - bat_dau_tong
    loi = [d for d in bang if d[1].startswith("✗")]
    dong = [f"# Tải toàn danh mục — {datetime.now():%Y-%m-%d %H:%M}",
            "", f"Chế độ: {'máy trắng (cache tạm)' if t.may_trang else 'cache thật'}"
            f"{', tác giả' if t.tac_gia else ''}. Python {sys.version.split()[0]}.", "",
            "| Bộ | Kết quả | Thời gian | Dung lượng đặt vào lab |", "|---|---|---|---|"]
    dong += [f"| `{ten}` | {tt.replace('|', '/')} | {g:.1f}s | {d / 1e6:.1f} MB |" for ten, tt, g, d in bang]
    so_khop = sum(1 for d in bang if d[1].startswith("✓"))
    dong += ["", f"**{so_khop}/{len(chay)} bộ đã tải khớp**, {len(loi)} lỗi, "
             f"{len(bang) - len(chay)} bỏ qua. Tải về {sum(b.get('dung_luong', 0) or 0 for b in chay) / 1e6:.1f} MB "
             f"(theo danh mục), đặt vào lab {sum(d[3] for d in bang) / 1e6:.1f} MB sau giải nén, "
             f"tổng thời gian {tong_giay / 60:.1f} phút."]
    thu_muc_log = HERE / "nhat-ky-tai"
    thu_muc_log.mkdir(exist_ok=True)
    log = thu_muc_log / f"{datetime.now():%Y-%m-%d-%H%M%S}.md"
    log.write_text("\n".join(dong) + "\n", encoding="utf-8")
    print("\n" + dong[-1] + f"\nNhật ký: {log.relative_to(TOOLS.parent)}  (dữ liệu tạm: {tam})")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
