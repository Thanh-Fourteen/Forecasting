"""Chấm một bài nộp trên dữ liệu THẬT của tuần đã qua. Trong lab/:

    python lab.py chay ../cong-cu/cham.py --moc 2026-10-05 --nhom ten-nhom

Chấm sớm nhất 4 ngày sau khi tuần kết thúc (tức thứ Sáu tuần sau): tệp EIA trễ ~1,5 ngày, đơn vị điều độ được sửa số trong
3 ngày. Số liệu còn có thể được sửa tới 30 ngày; chấm lại sau đó thì ghi đè ket-qua.json (ghi rõ lần chấm).

Tính tự động: phần A (sai số tương lai, 35), B (trung thực của backtest, 20), 12/20 điểm của C (chạy lại ra đúng dự báo),
8/15 điểm của D (thời tiết trong backtest là thời tiết đã dự báo), điểm thưởng (thắng dự báo của đơn vị điều độ).
Phần còn lại giám khảo chấm theo RUBRIC.md.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path

import du_lieu as dl
import numpy as np
import pandas as pd
from nop import nap_ma, sha_ma

CHO_NGAY = 4


def diem_tuyen_tinh(x: float, tot: float, te: float, toi_da: float) -> float:
    """toi_da điểm khi x ≤ tot, 0 khi x ≥ te, tuyến tính ở giữa."""
    if not math.isfinite(x):
        return 0.0
    return float(toi_da * np.clip((te - x) / (te - tot), 0, 1))


def seasonal_naive_tuan(ls: pd.DataFrame, moc: pd.Timestamp) -> pd.DataFrame:
    """Lặp lại tuần gần nhất đã biết đủ lúc mốc (1 tuần trước, không có thì 2 tuần trước)."""
    ra = []
    for v, g in ls.groupby("vung"):
        y = g.set_index("ds")["y"]
        ds = pd.date_range(moc + pd.Timedelta(hours=1), periods=dl.H, freq="h")
        t1, t2 = y.reindex(ds - pd.Timedelta(hours=168)).to_numpy(), y.reindex(ds - pd.Timedelta(hours=336)).to_numpy()
        ra.append(pd.DataFrame({"vung": v, "ds": ds, "sn": np.where(np.isnan(t1), t2, t1)}))
    return pd.concat(ra, ignore_index=True)


def kiem_thoi_tiet_backtest(bt: pd.DataFrame, luu: pd.DataFrame) -> dict:
    """Nhiệt độ trong backtest.csv có đúng là nhiệt độ ĐÃ DỰ BÁO (truoc_⌈h/24⌉) không, hay là nhiệt độ thật (thuc)?"""
    if "nhiet_do" not in bt or bt["nhiet_do"].isna().all():
        return {"dat": True, "ghi_chu": "mô hình không dùng nhiệt độ"}
    b = bt.merge(luu, on=["vung", "ds"], how="left")
    k = dl.tam_ngay(b["h"].to_numpy())
    du_bao = b[[f"truoc_{i}" for i in range(1, 8)]].to_numpy()[np.arange(len(b)), k - 1]
    lech_du_bao = float(np.nanmedian(np.abs(b["nhiet_do"] - du_bao)))
    lech_thuc = float(np.nanmedian(np.abs(b["nhiet_do"] - b["thuc"])))
    return {"dat": lech_du_bao <= 0.05 and lech_du_bao < lech_thuc,
            "lech_trung_vi_voi_du_bao": round(lech_du_bao, 3), "lech_trung_vi_voi_thuc": round(lech_thuc, 3)}


def cham(thu_muc: Path, cho_phep_som: bool = False, tai: bool = True) -> dict:
    bb = json.loads((thu_muc / "bien-ban.json").read_text(encoding="utf-8"))
    moc = pd.Timestamp(bb["moc"]).tz_localize(None)
    het = moc + pd.Timedelta(hours=dl.H)
    bay_gio = datetime.now(UTC)
    if pd.Timestamp(bay_gio).tz_localize(None) < het + pd.Timedelta(days=CHO_NGAY) and not cho_phep_som:
        raise SystemExit(f"chưa chấm được: đợi tới {het + pd.Timedelta(days=CHO_NGAY)} UTC (hoặc --som để chấm tạm)")
    loi_bb = [ten for ten, s in bb["tep"].items() if dl.sha256(thu_muc / ten) != s]
    hop_le = (not loi_bb) and pd.Timestamp(bb["tao_luc"]).tz_localize(None) < moc and not bb["thu_qua_khu"]
    if tai:
        dl.tai_eia_moi()
    thuc_te = dl.doc_lich_su()
    thuc_te = thuc_te[(thuc_te["ds"] > moc) & (thuc_te["ds"] <= het)]

    f = pd.read_csv(thu_muc / "du-bao.csv", parse_dates=["ds"])
    dv = pd.read_parquet(thu_muc / "dau-vao.parquet")
    ls = dv[dv["bang"] == "lich_su"][["vung", "ds", "y", "df"]]
    luu = dv[dv["bang"] == "luu_tru"].drop(columns=["bang", "y", "df"])
    bt = pd.read_csv(thu_muc / "backtest.csv", parse_dates=["moc", "ds"])

    d = f.merge(thuc_te, on=["vung", "ds"], how="left").merge(seasonal_naive_tuan(ls, moc), on=["vung", "ds"])
    d = d[d["y"].notna()]
    mau = dl.mau_so_mase(ls, moc)
    g = d.groupby("vung")
    mae = g.apply(lambda x: np.mean(np.abs(x["y"] - x["du_bao"])), include_groups=False)
    mae_sn = g.apply(lambda x: np.mean(np.abs(x["y"] - x["sn"])), include_groups=False)
    mae_df = g.apply(lambda x: np.nanmean(np.abs(x["y"] - x["df"])), include_groups=False)
    mase = mae / mau
    bt_mase = (bt["y"] - bt["du_bao"]).abs().groupby(bt["vung"]).mean() / mau
    r = float((mae / mae_sn).mean())
    q = float(mase.mean() / bt_mase.mean())

    # tái lập: chạy lại du_bao trên đúng đầu vào đã lưu
    try:
        hv = nap_ma(Path(bb["thu_muc_ma"]))
        f2 = hv.du_bao(ls, pd.read_parquet(thu_muc / "thoi-tiet.parquet"), moc).merge(f, on=["vung", "ds"])
        lech_tai_lap = float(np.max(np.abs(f2["du_bao_x"] - f2["du_bao_y"])))
    except Exception as loi:  # noqa: BLE001 — mọi lỗi khi chạy lại đều là "không tái lập"
        lech_tai_lap = float("inf")
        print("không chạy lại được:", loi)
    tt = kiem_thoi_tiet_backtest(bt, luu)

    diem = {"A_sai_so_tuong_lai": round(diem_tuyen_tinh(r, 0.60, 1.00, 35), 1),
            "B_trung_thuc_backtest": round(diem_tuyen_tinh(abs(math.log(q)), math.log(1.25), math.log(2), 20), 1),
            "C_chay_lai_giong_het": 12.0 if lech_tai_lap <= 1.0 else 0.0,
            "D_thoi_tiet_la_du_bao": 8.0 if tt["dat"] else 0.0,
            "thuong_thang_df": int((mae < mae_df).sum())}
    kq = {"moc": bb["moc"], "nhom": bb["nhom"], "cham_luc": bay_gio.isoformat(timespec="seconds"),
          "hop_le": bool(hop_le), "tinh_diem": bool(hop_le), "loi_bien_ban": loi_bb, "so_gio_co_thuc_te": int(len(d)),
          "mase": mase.round(3).to_dict(), "mase_tb": round(float(mase.mean()), 3),
          "mase_backtest": bt_mase.round(3).to_dict(), "mase_backtest_tb": round(float(bt_mase.mean()), 3),
          "ty_so_voi_seasonal_naive": round(r, 3), "ty_so_that_tren_backtest": round(q, 3),
          "mae": mae.round(0).to_dict(), "mae_seasonal_naive": mae_sn.round(0).to_dict(), "mae_df": mae_df.round(0).to_dict(),
          "mase_df_tb": round(float((mae_df / mau).mean()), 3), "mase_seasonal_naive_tb": round(float((mae_sn / mau).mean()), 3),
          "lech_tai_lap_mw": lech_tai_lap if math.isfinite(lech_tai_lap) else None,
          "sha256_ma_luc_nop": bb["sha256_ma"], "sha256_ma_luc_cham": sha_ma(Path(bb["thu_muc_ma"])),
          "thoi_tiet_backtest": tt, "diem_tu_dong": diem}
    (thu_muc / "ket-qua.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
    return kq


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--moc", required=True)
    ap.add_argument("--nhom", default="nhom-cua-toi")
    ap.add_argument("--ra", default=str(dl.DU_AN / "nop"))
    ap.add_argument("--som", action="store_true", help="chấm tạm trước hạn chờ (số liệu có thể còn thiếu/chưa sửa)")
    ap.add_argument("--khong-tai", action="store_true")
    a = ap.parse_args(argv)
    kq = cham(Path(a.ra) / a.nhom / f"{pd.Timestamp(a.moc):%Y-%m-%d}", a.som, not a.khong_tai)
    print(json.dumps({k: kq[k] for k in ("hop_le", "mase_tb", "mase_backtest_tb", "mase_seasonal_naive_tb", "mase_df_tb",
                                         "ty_so_voi_seasonal_naive", "ty_so_that_tren_backtest", "diem_tu_dong")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
