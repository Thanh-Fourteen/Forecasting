# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 4 → ../hinh/*.png (150 dpi)

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates
import matplotlib.pyplot as plt
import pandas as pd

DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("bd", DAY / "bieu_do.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)
MAU = bd.MAU


def luu(fig, ten: str) -> None:
    HINH.mkdir(exist_ok=True)
    fig.savefig(HINH / ten, dpi=150, bbox_inches="tight")
    plt.close(fig)


def mot_hinh(ham, df, ten: str, co=(9, 3.6)) -> None:
    fig, ax = plt.subplots(figsize=co)
    ham(ax, df)
    luu(fig, ten)


def hinh_gop_tan_suat(df) -> dict:
    y = df["cnt"]
    ngay = y.resample("D").sum(min_count=12)
    thang = y.resample("MS").sum()
    fig, (a, b, c) = plt.subplots(3, 1, figsize=(9, 6))
    a.plot(y.index, y.to_numpy(), color=MAU["chinh"], linewidth=0.2)
    a.set_title("Theo giờ (17.544 điểm): một khối màu — không đọc được gì ngoài 'mùa hè cao hơn'")
    b.plot(ngay.index, ngay.to_numpy(), color=MAU["chinh"], linewidth=0.6)
    b.set_title("Theo ngày: thấy dao động trong tuần và những ngày rơi xuống gần 0")
    c.plot(thang.index, thang.to_numpy(), color=MAU["chinh"], marker="o")
    c.set_title("Theo tháng: mượt, đẹp — nhưng mùa vụ ngày, tuần và các ngày bất thường đã biến mất")
    for ax, dv in ((a, "lượt / giờ"), (b, "lượt / ngày"), (c, "lượt / tháng")):
        ax.set_ylim(bottom=0)
        ax.set_ylabel(dv)
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator(bymonth=[1, 4, 7, 10]))
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m/%Y"))
    fig.tight_layout()
    luu(fig, "gop-tan-suat.png")
    return {"ngay_thap": ngay.nsmallest(3).to_dict()}


def hinh_lam_tron(df) -> dict:
    ngay = df["cnt"].resample("D").sum(min_count=1)["2012-09-15":"2012-11-30"]
    tron = df["cnt"].resample("D").sum(min_count=1).rolling(7, center=True, min_periods=4).mean()["2012-09-15":"2012-11-30"]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(ngay.index, ngay.to_numpy(), color=MAU["xam"], marker="o", markersize=3, label="tổng theo ngày")
    ax.plot(tron.index, tron.to_numpy(), color=MAU["phu"], linewidth=2, label="trung bình trượt 7 ngày")
    ax.annotate("29/10/2012: bão Sandy — tệp chỉ còn 1 giờ, 22 lượt", (pd.Timestamp("2012-10-29"), 22),
                xytext=(pd.Timestamp("2012-09-20"), 1500), arrowprops={"arrowstyle": "->"}, fontsize=8)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("lượt / ngày")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Làm trơn 7 ngày biến ngày gần 0 thành một chỗ lõm nhẹ — ngoại lai biến mất khỏi hình")
    luu(fig, "lam-tron.png")
    return {"tron_29_10": float(tron["2012-10-29"]), "ngay_29_10": float(ngay["2012-10-29"]),
            "ngay_30_10": float(ngay["2012-10-30"])}


def hinh_gay_hieu_nham(df) -> None:
    luu(bd.bieu_do_gay_hieu_nham(df), "gay-hieu-nham.png")
    luu(bd.ve_lai_trung_thuc(df), "ve-lai.png")


def hinh_log(df) -> dict:
    thang = df["cnt"].resample("MS").sum()["2011-01":"2011-12"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.2))
    for ax, log in ((a, False), (b, True)):
        ax.plot(thang.index, thang.to_numpy(), color=MAU["chinh"], marker="o")
        ax.set_ylabel("lượt / tháng")
        ax.set_xlabel("tháng năm 2011")
        if log:
            ax.set_yscale("log")
            ax.set_yticks([40_000, 60_000, 80_000, 100_000, 140_000], ["40.000", "60.000", "80.000", "100.000", "140.000"])
            ax.minorticks_off()
        else:
            ax.set_ylim(bottom=0)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m"))
    a.set_title("Tuyến tính: T4→T5 (+41 nghìn) trông dốc nhất", fontsize=9)
    b.set_title("Log: T3→T4 (+48%) mới là tăng tỷ lệ mạnh nhất", fontsize=9)
    fig.tight_layout()
    luu(fig, "thang-log.png")
    tang = thang.pct_change()
    return {"tang_pct": tang.round(3).to_dict(), "tang_tuyet_doi": thang.diff().to_dict()}


def hinh_tre(df) -> None:
    """Lag plot cho tài liệu: một hàng 4 ô (bản trong bộ chẩn đoán là lưới 2 × 2)."""
    fig, truc = plt.subplots(1, 4, figsize=(11, 3.2))
    for o, k in zip(truc, (1, 12, 24, 168), strict=True):
        cap = bd.cap_tre(df["cnt"], k)
        o.scatter(cap["truoc"], cap["sau"], s=0.5, alpha=0.1, color=MAU["chinh"])
        o.plot([0, 1000], [0, 1000], color=MAU["phu"], linewidth=0.8)
        o.set_aspect("equal")
        o.set_xlim(0, 1000)
        o.set_ylim(0, 1000)
        o.tick_params(labelsize=7)
        o.set_xlabel(f"lượt lúc t − {k} giờ", fontsize=8)
        o.set_title(f"trễ {k} giờ: r = {cap.corr().iloc[0, 1]:.2f}".replace(".", ","), fontsize=9)
    truc[0].set_ylabel("lượt lúc t", fontsize=8)
    fig.suptitle("Trễ 168 bám đường chéo nhất, trễ 12 tản thành hai nhánh", fontsize=11)
    fig.tight_layout()
    luu(fig, "tre.png")


if __name__ == "__main__":
    df = bd.doc_luot_thue()
    print(hinh_gop_tan_suat(df))
    print(hinh_lam_tron(df))
    hinh_gay_hieu_nham(df)
    print(hinh_log(df))
    hinh_tre(df)
    fig = bd.bo_bieu_do_chan_doan(df)
    luu(fig, "bo-bieu-do.png")
    for ten, ham, co in (("mua-vu-tuan.png", bd.ve_mua_vu_tuan, (9, 3.4)),
                         ("chuoi-con-thang.png", bd.ve_chuoi_con_thang, (9, 3.2)),
                         ("nhiet-gio-thu.png", bd.ve_nhiet_gio_thu, (9, 3.4)),
                         ("hop-theo-gio.png", bd.ve_hop_theo_gio, (9, 3.4)),
                         ("phan-tan-nhiet-do.png", bd.ve_phan_tan_nhiet_do, (7, 3.6)),
                         ("acf.png", bd.ve_acf, (9, 3.2))):
        mot_hinh(ham, df, ten, co)
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
