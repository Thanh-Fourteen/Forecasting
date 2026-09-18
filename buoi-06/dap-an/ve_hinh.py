# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 6 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from tv import ve

DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("pr", DAY / "phan_ra.py")
pr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr)
M = ve.MAU


def co_dien(y: pd.Series) -> pd.DataFrame:
    kq = seasonal_decompose(y, model="additive", period=24)
    return pd.DataFrame({"y": y, "trend": kq.trend, "seasonal_24": kq.seasonal, "resid": kq.resid})


def dia_phuong(s: pd.Series) -> pd.Series:
    return pd.Series(s.to_numpy(), index=s.index.tz_localize("UTC").tz_convert(pr.MUI_GIO))


def hinh_du_lieu(y_goc: pd.Series) -> dict:
    thieu = y_goc[y_goc.isna()].index
    fig, (a, b) = plt.subplots(2, 1, figsize=(10, 5.5))
    ngay = y_goc.resample("D").mean()
    a.plot(y_goc.index, y_goc.to_numpy() / 1000, color=M["xam"], linewidth=0.2)
    a.plot(ngay.index, ngay.to_numpy() / 1000, color=M["chinh"], linewidth=1)
    for t in (pd.Timestamp("2024-03-10"), pd.Timestamp("2024-11-03")):
        a.axvline(t, color=M["phu"], linestyle="--", linewidth=0.8)
    a.set_ylabel("GW")
    a.set_title("PJM 2024: đỉnh hè tháng 7, đỉnh đông tháng 1; vạch cam = hai ngày đổi giờ, dữ liệu trống 22 và 25 giờ")
    tuan = dia_phuong(y_goc["2024-07-08 04:00":"2024-07-22 03:00"])
    b.plot(tuan.index.tz_localize(None), tuan.to_numpy() / 1000, color=M["chinh"])
    b.set_ylabel("GW")
    b.set_title("Hai tuần tháng 7 (giờ New York): mỗi ngày một đỉnh chiều; thứ Bảy–Chủ nhật (13–14/7) thấp hơn")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "du-lieu-pjm.png")
    return {"nan": int(y_goc.isna().sum()), "nan_dau": str(thieu[0]), "nan_cuoi": str(thieu[-1]),
            "dinh": (str(y_goc.idxmax()), float(y_goc.max())), "day": (str(y_goc.idxmin()), float(y_goc.min()))}


def hinh_co_dien(cd: pd.DataFrame) -> dict:
    cua_so = dia_phuong(cd["y"]).index
    doan = slice("2024-07-01 04:00", "2024-07-29 03:00")
    fig, truc = plt.subplots(4, 1, figsize=(10, 7.5), sharex=True)
    for ax, cot, ten in zip(truc, ["y", "trend", "seasonal_24", "resid"],
                            ["dữ liệu", "xu hướng (2×24-MA)", "mùa vụ 24 giờ (cố định cả năm)", "phần dư"], strict=True):
        s = dia_phuong(cd[cot])[doan]
        ax.plot(s.index.tz_localize(None), s.to_numpy() / 1000, color=M["chinh"], linewidth=0.8)
        ax.set_ylabel("GW")
        ax.set_title(ten, fontsize=9, loc="left")
    for ax in truc:
        for d in pd.date_range("2024-07-06", "2024-07-28", freq="7D"):
            ax.axvspan(d, d + pd.Timedelta("2D"), color=M["xam"], alpha=0.15)
    truc[3].axhline(0, color="black", linewidth=0.5)
    fig.suptitle("Phân rã cổ điển chu kỳ 24 giờ, tháng 7/2024: xu hướng lõm mỗi cuối tuần (dải xám), phần dư dao động đều theo ngày",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "co-dien-24.png")
    tr = dia_phuong(cd["trend"]).dropna()
    return {"trend_theo_thu": tr.groupby(tr.index.dayofweek).mean().round(0).to_dict(), "n_nan_trend": int(cd["trend"].isna().sum()),
            "cua_so": str(cua_so[0])}


def hinh_so_sanh_phan_du(cd: pd.DataFrame, ms: pd.DataFrame) -> dict:
    fig, truc = plt.subplots(2, 2, figsize=(10, 7), layout="constrained")
    kq = {}
    for cot, (ten, b) in enumerate((("cổ điển (24)", cd), ("MSTL (24, 168)", ms))):
        h = pr.ho_so_phan_du(b, ("month", "hour")).unstack() / 1000
        anh = truc[0, cot].imshow(h.to_numpy(), aspect="auto", cmap="RdBu_r", vmin=-12, vmax=12)
        truc[0, cot].set_yticks(range(12), [f"Th{m}" for m in h.index], fontsize=7)
        truc[0, cot].set_xticks(range(0, 24, 3))
        truc[0, cot].set_xlabel("giờ New York")
        truc[0, cot].set_title(f"{ten}: tháng × giờ", fontsize=9)
        thu = pr.ho_so_phan_du(b, ("dayofweek", "hour")) / 1000
        truc[1, cot].plot(np.arange(168), thu.to_numpy(), color=M["chinh"])
        truc[1, cot].set_xticks(range(0, 168, 24), ["T2", "T3", "T4", "T5", "T6", "T7", "CN"])
        truc[1, cot].axhline(0, color="black", linewidth=0.5)
        truc[1, cot].set_ylim(-4, 4)
        truc[1, cot].set_title(f"{ten}: giờ trong tuần", fontsize=9)
        truc[1, cot].set_ylabel("GW")
        r = b["resid"].dropna()
        kq[ten] = {"var_resid_GW2": round(float(r.var()) / 1e6, 1),
                   "thu_gio": round(pr.ty_le_mau_hinh_con_lai(b, ("dayofweek", "hour")), 5),
                   "thang_gio": round(pr.ty_le_mau_hinh_con_lai(b, ("month", "hour")), 5),
                   "acf_24": round(float(r.autocorr(24)), 3), "acf_168": round(float(r.autocorr(168)), 3),
                   "T7_17h": round(float(pr.ho_so_phan_du(b, ("month", "hour")).loc[(7, 17)])),
                   "T1_8h": round(float(pr.ho_so_phan_du(b, ("month", "hour")).loc[(1, 8)])),
                   "T7_8h_thu": round(float(pr.ho_so_phan_du(b, ("dayofweek", "hour")).loc[(5, 8)]))}
    fig.colorbar(anh, ax=truc[0, :], shrink=0.8)
    fig.suptitle("Trung bình phần dư (GW) — cổ điển còn mùa vụ ngày đổi theo mùa (trên)\nvà nhịp cuối tuần (dưới); MSTL sạch cả hai",
                 fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "phan-du-so-sanh.png")
    return kq


def hinh_mstl(ms: pd.DataFrame) -> None:
    doan = slice("2024-07-01 04:00", "2024-07-29 03:00")
    fig, truc = plt.subplots(5, 1, figsize=(10, 8.5), sharex=True)
    for ax, cot, ten in zip(truc, ["y", "trend", "seasonal_24", "seasonal_168", "resid"],
                            ["dữ liệu", "xu hướng", "mùa vụ ngày (đổi dần theo thời gian)", "mùa vụ tuần", "phần dư"],
                            strict=True):
        s = dia_phuong(ms[cot])[doan]
        ax.plot(s.index.tz_localize(None), s.to_numpy() / 1000, color=M["chinh"], linewidth=0.8)
        ax.set_ylabel("GW")
        ax.set_title(ten, fontsize=9, loc="left")
    truc[4].axhline(0, color="black", linewidth=0.5)
    fig.suptitle("MSTL (24, 168), tháng 7/2024: nhịp cuối tuần nằm trong mùa vụ tuần, xu hướng trơn, phần dư là thời tiết",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "mstl.png")


def hinh_robust(y: pd.Series, ms: pd.DataFrame) -> dict:
    rb = pr.phan_ra(y, robust=True)
    doan = slice("2024-11-18 05:00", "2024-11-25 04:00")
    fig, (a, b, c) = plt.subplots(3, 1, figsize=(10, 6.5), sharex=True)
    s = dia_phuong(y)[doan]
    a.plot(s.index.tz_localize(None), s.to_numpy() / 1000, color="black")
    a.set_title("dữ liệu: 21/11 lúc 12:00 New York (17:00 UTC) báo 56,3 GW giữa hai giờ khoảng 95 GW", fontsize=9, loc="left")
    for ax, cot, ten in ((b, "seasonal_24", "mùa vụ ngày"), (c, "resid", "phần dư")):
        for bang, mau, nhan in ((ms, M["phu"], "không robust"), (rb, M["chinh"], "robust")):
            s = dia_phuong(bang[cot])[doan]
            ax.plot(s.index.tz_localize(None), s.to_numpy() / 1000, color=mau, label=nhan, linewidth=1)
        ax.set_title(ten, fontsize=9, loc="left")
        ax.legend(fontsize=8)
    for ax in (a, b, c):
        ax.set_ylabel("GW")
    fig.suptitle("Một giờ hỏng: không robust thì lỗi bị chia sang mùa vụ ngày của cả tuần; robust giữ lỗi trọn trong phần dư",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "robust.png")
    t = pd.Timestamp("2024-11-21 17:00")
    return {"y": float(y[t]), "truoc_sau": (float(y[t - pd.Timedelta("1h")]), float(y[t + pd.Timedelta("1h")])),
            "resid_khong": round(float(ms.loc[t, "resid"])), "resid_robust": round(float(rb.loc[t, "resid"])),
            "s24_khong_20_11": round(float(ms.loc[t - pd.Timedelta("1D"), "seasonal_24"])),
            "s24_robust_20_11": round(float(rb.loc[t - pd.Timedelta("1D"), "seasonal_24"])),
            "s24_khong_25_11": round(float(ms.loc[t + pd.Timedelta("4D"), "seasonal_24"])),
            "s24_robust_25_11": round(float(rb.loc[t + pd.Timedelta("4D"), "seasonal_24"])),
            "do_manh_robust": {k: round(v, 3) for k, v in pr.do_manh(rb).items()}}


def hinh_bien_do(ms: pd.DataFrame) -> dict:
    s = dia_phuong(ms["seasonal_24"])
    ho = s.groupby([s.index.month, s.index.hour]).mean().unstack() / 1000
    fig, ax = plt.subplots(figsize=(9, 3.8))
    mau = plt.cm.coolwarm(np.linspace(0, 1, 7))
    for i, th in enumerate([1, 3, 5, 7, 9, 11, 12]):
        c = mau[[0, 2, 4, 6, 4, 2, 1][i]]
        ax.plot(range(24), ho.loc[th].to_numpy(), color=c, label=f"tháng {th}", linewidth=1.5 if th in (1, 7) else 0.9)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xticks(range(0, 24, 3))
    ax.set_xlabel("giờ New York")
    ax.set_ylabel("GW")
    ax.legend(fontsize=7, ncols=2)
    ax.set_title("Mùa vụ ngày của MSTL theo tháng: tháng 1 hai đỉnh sáng–tối, tháng 7 một đỉnh chiều, biên độ gấp 3")
    ve.luu_hinh(fig, HINH / "bien-do-ngay.png")
    bien_do = ho.max(axis=1) - ho.min(axis=1)
    return {"bien_do_GW": bien_do.round(1).to_dict(), "gio_dinh": ho.idxmax(axis=1).to_dict()}


if __name__ == "__main__":
    y_goc = pr.doc_nhu_cau()
    y = pr.lap_cho_trong(y_goc)
    cd = co_dien(y)
    ms = pr.phan_ra(y)
    with ve.phong_cach():
        print("du lieu", hinh_du_lieu(y_goc))
        print("co dien", hinh_co_dien(cd))
        print("so sanh", hinh_so_sanh_phan_du(cd, ms))
        hinh_mstl(ms)
        print("robust", hinh_robust(y, ms))
        print("bien do", hinh_bien_do(ms))
    print("do manh co dien", {k: round(v, 3) for k, v in pr.do_manh(cd).items()})
    print("do manh MSTL", {k: round(v, 3) for k, v in pr.do_manh(ms).items()})
    print("var y GW2", round(float(y.var()) / 1e6, 1))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
