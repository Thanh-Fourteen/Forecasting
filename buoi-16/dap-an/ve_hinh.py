# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 16 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
import sys
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
spec = importlib.util.spec_from_file_location("et", DAY / "ets.py")
et = importlib.util.module_from_spec(spec)
sys.modules["et"] = et
spec.loader.exec_module(et)
M = ve.MAU


def hinh_ses(y: np.ndarray) -> dict:
    toi_uu = et.ses_toi_uu(y)["alpha"]
    fig, ax = plt.subplots(figsize=(10, 3.4))
    x = np.arange(len(y))
    ax.plot(x, y / 1e3, color="black", marker="o", markersize=3, label="thực tế")
    for a, c in ((0.1, M["phu"]), (toi_uu, M["chinh"]), (0.95, M["ba"])):
        khop, _ = et.ses_loc(y, a)
        ax.plot(x[1:], khop / 1e3, color=c, linewidth=1.4,
                label=f"SES α = {a:.2f}".replace(".", ",") + (" (tối ưu)" if a == toi_uu else ""))
    ax.set_xlabel("năm thứ")
    ax.set_ylabel("khách (nghìn / năm)")
    ax.legend(fontsize=8)
    ax.set_title("α nhỏ: đường trơn nhưng chạy chậm sau thực tế; α lớn: bám sát nhưng lặp lại cả nhiễu")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ses-alpha.png")
    return {"alpha tối ưu": round(toi_uu, 3)}


def hinh_hw(y: pd.Series) -> dict:
    moc = "2018-01"
    hoc, kiem = y[y.index < moc], y[y.index >= moc]
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.5), gridspec_kw={"width_ratios": [2.2, 1]})
    a.plot(y.index, y, color="black", linewidth=1.0, label="thực tế")
    for kieu, c, nhan in (("cong", M["phu"], "HW cộng"), ("nhan", M["chinh"], "HW nhân")):
        a.plot(kiem.index, et.holt_winters(hoc, len(kiem), kieu)["mean"], color=c, linewidth=1.5, label=nhan)
    a.axvline(pd.Timestamp(moc), color=M["xam"], linestyle="--", linewidth=0.8)
    a.set_ylabel("hành khách (triệu / tháng)")
    a.legend(fontsize=8)
    a.set_title("dự báo 2018–2019 từ dữ liệu tới 12/2017", fontsize=9)
    bd = et.bien_do_mua_vu(y)
    b.bar(bd.index, bd.to_numpy(), color=M["ba"])
    b.set_ylabel("tháng cao nhất − thấp nhất (triệu)")
    b.set_title("biên độ mùa vụ theo năm", fontsize=9)
    fig.suptitle("Biên độ mùa vụ tăng theo mức: Holt–Winters cộng hụt đỉnh hè, dạng nhân bám đúng",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "hw-cong-nhan.png")
    return {"biên độ 2008": round(float(bd.iloc[0]), 1), "biên độ 2017": round(float(bd.loc[2017]), 1),
            "biên độ 2019": round(float(bd.iloc[-1]), 1)}


def hinh_so_snaive(mase: pd.DataFrame) -> dict:
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    for ax, m in ((a, "AutoETS"), (b, "AutoTheta")):
        d = (mase[m] - mase["SeasonalNaive"]).clip(-2, 2)
        ax.hist(d, bins=50, color=M["chinh"] if m == "AutoETS" else M["ba"])
        ax.axvline(0, color="black", linewidth=0.8)
        ax.axvline(float((mase[m] - mase["SeasonalNaive"]).mean()), color=M["phu"], linestyle="--", linewidth=1.2)
        ax.set_xlabel(f"MASE {m} − MASE seasonal naive (cắt ở ±2)")
        ax.set_title(f"{m}: âm là thắng; thắng ở {(mase[m] < mase['SeasonalNaive']).mean() * 100:.1f}% chuỗi"
                     .replace(".", ","), fontsize=9)
    a.set_ylabel("số chuỗi")
    fig.suptitle("366 chuỗi du lịch, 2 cửa sổ 24 tháng: AutoETS thắng seasonal naive rõ, AutoTheta chỉ nhỉnh",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "so-snaive.png")
    return {}


def hinh_ty_le_phu(kq: pd.DataFrame) -> pd.DataFrame:
    nhom = pd.cut(kq["buoc_h"], [0, 6, 12, 18, 24], labels=["1–6", "7–12", "13–18", "19–24"])
    bang = pd.DataFrame({f"{m} {muc}%": kq.groupby(nhom, observed=True).apply(
        lambda g, m=m, muc=muc: et.ty_le_phu(g, m, muc) * 100) for m in ("AutoETS", "AutoTheta") for muc in (80, 95)})
    fig, ax = plt.subplots(figsize=(9, 3.4))
    mau = {"AutoETS 80%": M["chinh"], "AutoETS 95%": M["nhat"], "AutoTheta 80%": M["ba"], "AutoTheta 95%": M["vang"]}
    for c in bang.columns:
        ax.plot(bang.index.astype(str), bang[c], marker="o", color=mau[c], label=c)
    ax.axhline(80, color=M["xam"], linestyle="--", linewidth=0.8)
    ax.axhline(95, color=M["xam"], linestyle="--", linewidth=0.8)
    ax.set_xlabel("bước dự báo (tháng sau cutoff)")
    ax.set_ylabel("tỷ lệ thực tế nằm trong khoảng (%)")
    ax.legend(fontsize=8, ncol=2)
    ax.set_title("Khoảng 80% của ETS phủ đúng; khoảng 95% và khoảng của Theta hẹp hơn danh nghĩa")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ty-le-phu.png")
    return bang


if __name__ == "__main__":
    chuoi = et.doc_tourism()
    y_nam = et.theo_nam(chuoi["T249"])
    print("T249 năm:", len(y_nam), "năm;", np.round(y_nam[:5]))
    print(et.ses_toi_uu(y_nam), et.holt_toi_uu(y_nam))
    print(et.so_voi_statsforecast(y_nam).round(1))
    hk = et.doc_hanh_khach()
    print(et.so_sanh_cong_nhan(hk).round(3).to_string(index=False))
    df = et.dang_dai(chuoi)
    print("độ dài:", int(df.groupby("unique_id").size().min()), "→", int(df.groupby("unique_id").size().max()),
          "| số 0:", int((df["y"] == 0).sum()))
    kq = et.backtest_tourism(df)
    print("cutoff:", sorted(kq["cutoff"].unique()))
    mase = et.mase_theo_chuoi(kq, df)
    print(et.kiem_dinh_so_snaive(mase).round(4).to_string(index=False))
    with ve.phong_cach():
        print(hinh_ses(y_nam))
        print(hinh_hw(hk))
        hinh_so_snaive(mase)
        print(hinh_ty_le_phu(kq).round(1))
    for m in ("AutoETS", "AutoTheta"):
        print(m, {muc: round(et.ty_le_phu(kq, m, muc) * 100, 1) for muc in (80, 95)})
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
