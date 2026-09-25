# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 24 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (lần đầu ~5 phút: 30 ứng viên × 3 cửa sổ, AutoGluon,
# đọc tệp Excel của Online Retail; lưu cache)

# %%
from __future__ import annotations

import importlib.util
import sys
import time
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
M = ve.MAU


def nap(ten: str):
    spec = importlib.util.spec_from_file_location(ten, DAY / f"{ten}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[ten] = mod
    spec.loader.exec_module(mod)
    return mod


en, cs = nap("ensemble"), nap("cold_start")


def vi_du_ket_hop() -> None:
    """Ví dụ tay mục 4.1: thực tế 100; A đoán 108, B đoán 96."""
    y, a, b = 100.0, 108.0, 96.0
    print("4.1 sai số A, B, TB:", y - a, y - b, y - (a + b) / 2)


def hinh_ket_hop(df, fc) -> None:
    """Một chuỗi ở W3 mà ETS đoán cao, LightGBM đoán thấp: trung bình nằm giữa."""
    f = fc[fc["cutoff"] == 131]
    loi = f.assign(e_ets=f["AutoETS"] - f["y"], e_lgb=f["LGBM"] - f["y"]).groupby("unique_id")[["e_ets", "e_lgb"]].mean()
    tb = f.groupby("unique_id")["y"].mean()
    ty = (loi["e_ets"] / tb).clip(upper=0.3) - (loi["e_lgb"] / tb).clip(lower=-0.3)
    uid = ty[(loi["e_ets"] > 0) & (loi["e_lgb"] < 0)].sort_values().index[-40]
    s = df[df["unique_id"] == uid]
    g = f[f["unique_id"] == uid]
    with ve.phong_cach():
        fig, a = plt.subplots(figsize=(8, 3.3))
        a.plot(s["ngay"], s["y"], color=M["xam"], label="thực tế")
        ngay = s.set_index("ds").loc[g["ds"], "ngay"].to_numpy()
        a.plot(ngay, g["AutoETS"], color=M["phu"], linewidth=1.8, label="AutoETS")
        a.plot(ngay, g["LGBM"], color=M["ba"], linewidth=1.8, label="LightGBM")
        a.plot(ngay, g["TB(ETS,Theta,LGBM)"], color=M["chinh"], linewidth=2.2, label="trung bình ETS, Theta, LightGBM")
        a.axvline(ngay[0], color=M["xam"], linestyle=":", linewidth=1)
        a.set_xlim(s["ngay"].iloc[60], s["ngay"].iloc[-1])
        a.set_ylabel("giá trị chuỗi (đơn vị gốc của M4)")
        a.set_title(f"Chuỗi {uid}: AutoETS đoán cao, LightGBM đoán thấp — trung bình sai ít hơn cả hai")
        a.legend(loc="upper left", ncol=2)
        e = {m: float(np.mean(np.abs(g[m] - g["y"]))) for m in ["AutoETS", "LGBM", "TB(ETS,Theta,LGBM)"]}
        print("hình kết hợp:", uid, {k: round(v, 1) for k, v in e.items()})
        ve.luu_hinh(fig, HINH / "ket-hop-mot-chuoi.png")
        plt.close(fig)


def hinh_lac_quan(diem) -> pd.DataFrame:
    lq = en.lac_quan_theo_so_ung_vien(diem)
    with ve.phong_cach():
        fig, a = plt.subplots(figsize=(7, 3.3))
        a.plot(lq.index, lq["diem_luc_chon"], marker="o", color=M["phu"], label="điểm lúc chọn (W1–W2, cửa sổ dùng để chọn)")
        a.plot(lq.index, lq["diem_bao_cao"], marker="s", color=M["chinh"], label="điểm báo cáo (W3, chưa dùng để chọn)")
        tb = float(diem.xs(131, level="cutoff")["TB(ETS,Theta,LGBM)"].mean())
        a.axhline(tb, color=M["xam"], linestyle="--", linewidth=1)
        a.text(30, tb + 0.006, f"trung bình ETS, Theta, LightGBM trên W3: {tb:.3f}", ha="right", fontsize=8, color="#444")
        a.set_xlabel("số ứng viên được thử cho mỗi chuỗi")
        a.set_ylabel("MASE trung bình 1.000 chuỗi")
        a.set_title("Càng nhiều ứng viên, điểm lúc chọn càng đẹp — điểm thật trên W3 không tốt lên")
        a.legend(loc="lower left")
        ve.luu_hinh(fig, HINH / "lac-quan-theo-so-ung-vien.png")
        plt.close(fig)
    print("lạc quan theo số ứng viên:\n", lq.round(3))
    return lq


def hinh_ra_mat(sp, ban) -> None:
    """Đường bán trung vị 8 tuần đầu của các mã ra mắt 3/2010 → 7/2011, chia theo giá ra mắt."""
    nhom = sp[(sp["ra_mat"] >= cs.BAT_DAU_ANALOG) & (sp["ra_mat"] <= pd.Timestamp("2011-07-31"))]
    bang = {"dưới £1": nhom[nhom["gia"] < 1], "£1 – £3": nhom[(nhom["gia"] >= 1) & (nhom["gia"] < 3)],
            "từ £3": nhom[nhom["gia"] >= 3]}
    with ve.phong_cach():
        fig, a = plt.subplots(figsize=(7, 3.3))
        for (ten, g), mau in zip(bang.items(), [M["chinh"], M["ba"], M["phu"]], strict=True):
            d = np.median([cs.duong_ra_mat(ban, m, t) for m, t in g["ra_mat"].items()], axis=0)
            a.plot(np.arange(1, 9), d, marker="o", color=mau, linewidth=1.8, label=f"giá ra mắt {ten} ({len(g)} mã)")
            print("ra mắt", ten, len(g), np.round(d, 1), "tổng", d.sum())
        a.set_xlabel("tuần kể từ tuần bán đầu tiên")
        a.set_ylabel("số món bán mỗi tuần (trung vị)")
        a.set_ylim(bottom=0)
        a.set_title("Hàng rẻ bán nhiều món hơn hẳn từ tuần đầu: giá là manh mối chọn hàng tương tự")
        a.legend()
        ve.luu_hinh(fig, HINH / "duong-ra-mat-theo-gia.png")
        plt.close(fig)


if __name__ == "__main__":
    HINH.mkdir(exist_ok=True)
    vi_du_ket_hop()
    df = en.doc_m4()
    fc = en.du_bao_30(df, luu=True)
    diem = en.mase(fc, df)
    print("số ứng viên:", len(en.ung_vien(fc)))
    print(diem.groupby("cutoff").mean().T.sort_values(131).round(3).to_string())
    w3 = diem.xs(131, level="cutoff")
    print("SAI (chọn và báo cáo cả 3 cửa sổ):", round(float(diem.groupby("unique_id").mean().min(axis=1).mean()), 3))
    print("SAI chỉ W3:", round(float(w3.min(axis=1).mean()), 3))
    r = en.chon_va_bao_cao(diem)
    print("ĐÚNG theo chuỗi:", {k: round(v, 3) for k, v in r.items() if k != "lua_chon"})
    print(r["lua_chon"].value_counts().head(6).to_dict())
    r = en.chon_va_bao_cao(diem, theo_chuoi=False)
    print("ĐÚNG chung:", r["lua_chon"].iloc[0], {k: round(v, 3) for k, v in r.items() if k != "lua_chon"})
    don = [c for c in diem.columns if not c.startswith(("TB", "TV"))]
    r = en.chon_va_bao_cao(diem[don], theo_chuoi=False)
    print("ĐÚNG chung, chỉ mô hình đơn:", r["lua_chon"].iloc[0], {k: round(v, 3) for k, v in r.items() if k != "lua_chon"})
    for c in ["deu", "nghich_mse", "toi_uu"]:
        w = en.trong_so(fc, c)
        f3 = en.ap_trong_so(fc[fc["cutoff"] == 131], w, "kh")
        print("trọng số", c, round(float(en.mase(f3[["unique_id", "ds", "cutoff", "y", "kh"]], df)["kh"].mean()), 3),
              "TB:", w.mean().round(3).to_dict(), "| tổng > 1,5:", int((w.sum(axis=1) > 1.5).sum()),
              "| lớn nhất:", round(float(w.to_numpy().max()), 2))
    w = en.trong_so(fc, "toi_uu", cua_so=en.CUTOFF)
    f3 = en.ap_trong_so(fc[fc["cutoff"] == 131], w, "kh")
    print("SAI: trọng số tối ưu ước lượng cả trên W3:",
          round(float(en.mase(f3[["unique_id", "ds", "cutoff", "y", "kh"]], df)["kh"].mean()), 3))
    hinh_ket_hop(df, fc)
    hinh_lac_quan(diem)
    t = time.time()
    fa, bxh, tr = en.chay_autogluon(df)
    print(f"AutoGluon {time.time() - t:.0f} giây\n", bxh.round(3).to_string(), "\n", {k: round(v, 3) for k, v in tr.items()})
    fa = fa.merge(df[["unique_id", "ds", "y"]], on=["unique_id", "ds"])
    print("MASE W3 của AutoGluon (cách tính của buổi):", en.mase(fa, df).mean().round(3).to_dict())
    sp, ban = cs.doc_san_pham()
    moi, chon = cs.chia_tap(sp, ban)
    k = cs.chon_k(sp, ban, chon)
    print("cold start:", len(moi), "mã mới", moi["ra_mat"].min().date(), "→", moi["ra_mat"].max().date(), "| tập chọn k:",
          len(chon), "| k =", k, "| danh mục KHAC:", int((moi["danh_muc"] == "KHAC").sum()))
    print("  k trên tập chọn:", {kk: round(cs.danh_gia(sp, ban, chon, "analog_gia", kk)["mae"], 1) for kk in (10, 20, 40, 80)})
    thuc = np.array([cs.duong_ra_mat(ban, m, t).sum() for m, t in moi["ra_mat"].items()])
    print("  tổng 8 tuần thực tế: trung vị", np.median(thuc), "trung bình", round(thuc.mean(), 1))
    for c in ["tb_danh_muc", "analog_danh_muc", "analog_gia"]:
        print(" ", c, {kk: round(v, 3) for kk, v in cs.danh_gia(sp, ban, moi, c, k).items()})
    print("  đoán 0:", round(float(np.mean(thuc)), 1))
    hinh_ra_mat(sp, ban)
