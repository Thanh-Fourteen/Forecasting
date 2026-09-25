"""Nộp dự báo cho một tuần — chạy TRƯỚC mốc (thứ Hai 00:00 UTC). Trong lab/:

    python lab.py chay ../cong-cu/nop.py --moc 2026-10-05 --nhom ten-nhom

Việc làm: tải dữ liệu mới (EIA-930, thời tiết) → dựng đầu vào đúng như biết được lúc mốc → gọi du_bao() và backtest()
trong code/du_bao.py → ghi nop/<nhom>/<moc>/ gồm du-bao.csv, backtest.csv, dau-vao.parquet (để chạy lại), bien-ban.json
(giờ tạo UTC + sha256 mọi tệp + sha256 code). Gửi sha256 của du-bao.csv cho nhóm/giảng viên trước mốc.

--thu-qua-khu: nộp thử cho một mốc đã qua (luyện tập). Dùng thời tiết dự báo lưu trữ thay cho dự báo mới nhất; bộ chấm
đánh dấu "không tính điểm".
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import du_lieu as dl
import pandas as pd


def nap_ma(thu_muc: Path):
    spec = importlib.util.spec_from_file_location("du_bao_hoc_vien", thu_muc / "du_bao.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha_ma(thu_muc: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(thu_muc.glob("*.py")):
        h.update(p.name.encode() + p.read_bytes())
    return h.hexdigest()


def kiem_du_bao(f: pd.DataFrame, moc: pd.Timestamp) -> pd.DataFrame:
    """Đúng 5 vùng × 168 giờ sau mốc, không trống, không âm."""
    ds = pd.date_range(moc + pd.Timedelta(hours=1), periods=dl.H, freq="h")
    can = pd.MultiIndex.from_product([sorted(dl.VUNG), ds], names=["vung", "ds"])
    f = f[["vung", "ds", "du_bao"]].copy()
    f["ds"] = pd.to_datetime(f["ds"])
    co = pd.MultiIndex.from_frame(f[["vung", "ds"]])
    if len(f) != len(can) or not co.sort_values().equals(can):
        raise ValueError(f"du_bao phải có đúng {len(can)} dòng: 5 vùng × 168 giờ từ {ds[0]} tới {ds[-1]} (hiện {len(f)})")
    if f["du_bao"].isna().any() or (f["du_bao"] < 0).any():
        raise ValueError("du_bao có ô trống hoặc âm")
    return f.sort_values(["vung", "ds"], ignore_index=True)


def dung_dau_vao(moc: pd.Timestamp, thu_qua_khu: bool, tai_luc: datetime) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """(lich_su, thoi_tiet cho du_bao, thoi_tiet lưu trữ đầy đủ cho backtest) — đúng những gì biết được lúc mốc."""
    lich_su, luu = dl.doc_lich_su(), dl.doc_thoi_tiet()
    if thu_qua_khu:
        ls, tt = dl.dau_vao(lich_su, luu, moc)
    else:
        ls = lich_su[lich_su["ds"] <= moc - pd.Timedelta(hours=dl.TRE_CONG_BO)].reset_index(drop=True)
        qk = luu[luu["ds"] <= moc][["vung", "ds", "thuc"]].rename(columns={"thuc": "nhiet_do"})
        tt = pd.concat([qk, dl.thoi_tiet_tuan_toi(luu, moc, tai_luc)], ignore_index=True)
    # bản lưu trữ cho backtest: chỉ những giờ ≤ mốc (dự báo lưu trữ của giờ sau mốc chưa tồn tại lúc nộp thật)
    return ls, tt.sort_values(["vung", "ds"], ignore_index=True), luu[luu["ds"] <= moc].reset_index(drop=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--moc", required=True, help="thứ Hai, ví dụ 2026-10-05 (00:00 UTC)")
    ap.add_argument("--nhom", default="nhom-cua-toi")
    ap.add_argument("--ma", default=str(dl.DU_AN / "code"), help="thư mục chứa du_bao.py (mặc định code/)")
    ap.add_argument("--ra", default=str(dl.DU_AN / "nop"), help="thư mục gốc lưu bài nộp")
    ap.add_argument("--khong-tai", action="store_true", help="dùng dữ liệu mới đã tải, không tải lại")
    ap.add_argument("--thu-qua-khu", action="store_true", help="luyện tập với một mốc đã qua (không tính điểm)")
    a = ap.parse_args(argv)

    moc = pd.Timestamp(a.moc)
    if moc.weekday() != 0 or moc != moc.normalize():
        ap.error("mốc phải là thứ Hai 00:00 UTC")
    bay_gio = datetime.now(UTC)
    qua_han = pd.Timestamp(bay_gio).tz_localize(None) >= moc
    if qua_han and not a.thu_qua_khu:
        ap.error(f"đã quá mốc {moc} (bây giờ {bay_gio:%Y-%m-%d %H:%M} UTC) — muốn luyện tập thì thêm --thu-qua-khu")
    if not a.khong_tai:
        print("tải dữ liệu mới (EIA-930 sáu tháng ~20–50 MB mỗi tệp, thời tiết 5 vùng)…")
        dl.tai_eia_moi()
        dl.tai_thoi_tiet_moi()
    tai_luc = max(datetime.fromisoformat(json.loads(d)["tai_luc"])
                  for d in (dl.MOI / "NHAT-KY.jsonl").read_text(encoding="utf-8").splitlines() if "thoi-tiet" in d)
    ls, tt, luu = dung_dau_vao(moc, a.thu_qua_khu, tai_luc)
    print(f"nhu cầu biết tới {ls['ds'].max()} UTC; thời tiết tải lúc {tai_luc:%Y-%m-%d %H:%M} UTC")

    thu_muc_ma = Path(a.ma).resolve()
    hv = nap_ma(thu_muc_ma)
    f = kiem_du_bao(hv.du_bao(ls, tt, moc), moc)
    bt = hv.backtest(ls, luu, dl.cac_moc_backtest(moc))

    ra = Path(a.ra) / a.nhom / f"{moc:%Y-%m-%d}"
    ra.mkdir(parents=True, exist_ok=True)
    f.to_csv(ra / "du-bao.csv", index=False)
    bt.to_csv(ra / "backtest.csv", index=False)
    tt.to_parquet(ra / "thoi-tiet.parquet", index=False)
    pd.concat([ls.assign(bang="lich_su"), luu.assign(bang="luu_tru")], ignore_index=True).to_parquet(ra / "dau-vao.parquet",
                                                                                                    index=False)
    bien_ban = {"moc": f"{moc:%Y-%m-%dT%H:%MZ}", "nhom": a.nhom, "tao_luc": bay_gio.isoformat(timespec="seconds"),
                "thu_qua_khu": bool(a.thu_qua_khu), "thoi_tiet_tai_luc": tai_luc.isoformat(timespec="seconds"),
                "sha256_ma": sha_ma(thu_muc_ma), "thu_muc_ma": str(thu_muc_ma),
                "tep": {p.name: dl.sha256(p) for p in sorted(ra.iterdir()) if p.name != "bien-ban.json"}}
    (ra / "bien-ban.json").write_text(json.dumps(bien_ban, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ đã ghi {ra}")
    print(f"  sha256 du-bao.csv: {bien_ban['tep']['du-bao.csv']}  ← gửi mã này TRƯỚC mốc")
    return 0


if __name__ == "__main__":
    sys.exit(main())
