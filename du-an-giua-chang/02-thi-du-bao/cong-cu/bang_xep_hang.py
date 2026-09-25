"""Bảng xếp hạng từ mọi ket-qua.json trong nop/<nhom>/<moc>/. Trong lab/:

    python lab.py chay ../cong-cu/bang_xep_hang.py            # in bảng + ghi nop/BANG-XEP-HANG.md

Xếp theo tỷ số MAE so với seasonal naive của chính tuần đó (nhỏ hơn là tốt hơn; 1 = ngang lặp lại tuần trước), trung bình
các tuần hợp lệ của mỗi nhóm. Bài nộp sau mốc hoặc sửa sau khi nộp (sha256 lệch) không vào bảng.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import du_lieu as dl
import pandas as pd


def markdown(b: pd.DataFrame) -> str:
    dong = ["| " + " | ".join(map(str, b.columns)) + " |", "|" + "---|" * len(b.columns)]
    return "\n".join(dong + ["| " + " | ".join(map(str, r)) + " |" for r in b.itertuples(index=False)])


def bang(goc: Path) -> pd.DataFrame:
    dong = []
    for p in sorted(goc.glob("*/*/ket-qua.json")):
        k = json.loads(p.read_text(encoding="utf-8"))
        dong.append({"nhom": k["nhom"], "moc": k["moc"][:10], "hop_le": k["hop_le"], "ty_so": k["ty_so_voi_seasonal_naive"],
                     "mase": k["mase_tb"], "mase_backtest": k["mase_backtest_tb"], "mase_df": k["mase_df_tb"],
                     "vung_thang_df": k["diem_tu_dong"]["thuong_thang_df"],
                     "diem_tu_dong": sum(v for t, v in k["diem_tu_dong"].items() if t != "thuong_thang_df")})
    return pd.DataFrame(dong)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ra", default=str(dl.DU_AN / "nop"))
    a = ap.parse_args(argv)
    goc = Path(a.ra)
    b = bang(goc)
    if b.empty:
        print(f"chưa có ket-qua.json nào trong {goc} — chạy cong-cu/cham.py trước")
        return 1
    hl = b[b["hop_le"]]
    xh = (hl.groupby("nhom").agg(so_tuan=("moc", "nunique"), ty_so=("ty_so", "mean"), mase=("mase", "mean"),
                                  mase_backtest=("mase_backtest", "mean"), mase_df=("mase_df", "mean"),
                                  vung_thang_df=("vung_thang_df", "mean"), diem_tu_dong=("diem_tu_dong", "mean"))
          .sort_values("ty_so").round(3).reset_index())
    xh.insert(0, "hang", range(1, len(xh) + 1))
    md = ["# Bảng xếp hạng — dự án giữa chặng 2", "",
          "ty_so = MAE ÷ MAE của seasonal naive cùng tuần (nhỏ hơn là tốt hơn). mase_df = MASE của dự báo day-ahead do đơn vị",
          "điều độ công bố, trên cùng các giờ (đối thủ thật; nó dự báo trước chỉ 1 ngày). diem_tu_dong = A + B + phần tự động",
          "của C và D (tối đa 75).", "", markdown(xh), "", "Mọi bài đã chấm (kể cả không hợp lệ):", "",
          markdown(b.sort_values(["moc", "ty_so"])), ""]
    (goc / "BANG-XEP-HANG.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
