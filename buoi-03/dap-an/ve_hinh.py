# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 3 → ../hinh/*.png (150 dpi)

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tv import ve

DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"


def _nap(duong_dan: Path, ten: str):
    spec = importlib.util.spec_from_file_location(ten, duong_dan)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


dung = _nap(DAY / "thoi_gian.py", "dung")
sai = _nap(DAY.parent / "code" / "thoi_gian.py", "sai")


def hinh_dst() -> None:
    fig, truc = plt.subplots(2, 2, figsize=(10, 5.6), sharey="col")
    for cot, (thang, ngay, tieu_de) in enumerate((
        ("03", "2024-03-10", "10/3/2024 — đồng hồ nhảy 01:59 → 03:00"),
        ("11", "2024-11-03", "3/11/2024 — đồng hồ lùi 01:59 → 01:00"),
    )):
        chuyen = dung.doc_chuyen_taxi(thang)
        naive = sai.dem_chuyen_theo_gio(chuyen)
        naive = naive[(naive["ds"] >= f"{ngay} 00:00") & (naive["ds"] < f"{ngay} 05:00")]
        ax = truc[0, cot]
        ax.bar(naive["ds"].dt.strftime("%H:%M"), naive["y"], color=ve.MAU["phu"])
        for i, v in enumerate(naive["y"]):
            ax.text(i, v + 150, f"{v:,.0f}".replace(",", "."), ha="center", fontsize=7)
        ax.set_title(f"{tieu_de}\nnaive: resample trên giờ địa phương", fontsize=9)
        ax.set_ylabel("chuyến / giờ")

        utc = dung.dem_chuyen_theo_gio(chuyen)
        dia_phuong = utc["ds"].dt.tz_convert("America/New_York")
        chon = (dia_phuong >= pd.Timestamp(f"{ngay} 00:00", tz="America/New_York")) & \
               (dia_phuong < pd.Timestamp(f"{ngay} 05:00", tz="America/New_York"))
        utc, dia_phuong = utc[chon], dia_phuong[chon]
        nhan = [f"{d:%H}Z\n{o:%H:%M}{' EDT' if o.utcoffset().total_seconds() == -14400 else ' EST'}"
                for d, o in zip(utc["ds"], dia_phuong, strict=True)]
        ax = truc[1, cot]
        ax.bar(nhan, utc["y"].fillna(0), color=ve.MAU["chinh"])
        for i, v in enumerate(utc["y"]):
            ax.text(i, (0 if np.isnan(v) else v) + 150, "không biết" if np.isnan(v) else f"{v:,.0f}".replace(",", "."),
                    ha="center", fontsize=7, color=ve.MAU["phu"] if np.isnan(v) else "black")
        ax.set_title("chuẩn hoá: gắn múi giờ New York rồi đổi sang UTC", fontsize=9)
        ax.set_ylabel("chuyến / giờ")
        ax.tick_params(axis="x", labelsize=7)
    fig.suptitle("Resample giờ địa phương naive sinh giờ 0 chuyến giả (tháng 3) và gộp hai giờ thật (tháng 11)",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "dst-hai-ngay.png")


def hinh_gio_nong() -> None:
    thoi_tiet_dung = dung.doc_thoi_tiet()
    dem = dung.dem_chuyen_theo_gio(dung.doc_chuyen_taxi("03"))
    ghep_dung = dung.ghep_thoi_tiet(dem, thoi_tiet_dung)
    ghep_sai = sai.ghep_thoi_tiet(sai.dem_chuyen_theo_gio(sai.doc_chuyen_taxi("03")), sai.doc_thoi_tiet())
    fig, ax = plt.subplots(figsize=(8, 3.4))
    tb_dung = ghep_dung.groupby(ghep_dung["ds"].dt.tz_convert("America/New_York").dt.hour)["nhiet_do"].mean()
    tb_sai = ghep_sai.groupby(ghep_sai["ds"].dt.hour)["nhiet_do"].mean()
    ax.plot(tb_dung.index, tb_dung.to_numpy(), marker="o", color=ve.MAU["chinh"],
            label=f"ghép cùng UTC — nóng nhất {tb_dung.idxmax()}h")
    ax.plot(tb_sai.index, tb_sai.to_numpy(), marker="s", color=ve.MAU["phu"],
            label=f"ghép giờ địa phương với giờ UTC — nóng nhất {tb_sai.idxmax()}h")
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel("giờ trong ngày (New York)")
    ax.set_ylabel("nhiệt độ trung bình tháng 3 (°C)")
    ax.set_title("Ghép lệch múi giờ làm New York 'nóng nhất lúc 8 giờ tối'")
    ax.legend(fontsize=8)
    ve.luu_hinh(fig, HINH / "gio-nong-nhat.png")


def hinh_bam_gio() -> None:
    # Số đo ghi lại từ `python ../code/bam_gio.py` ngày 2026-09-17 trên máy soạn khoá (i5-11600K), trung vị 7 lần
    # sau 1 lần làm nóng. "4 nhân": taskset -c 0-3, POLARS_MAX_THREADS=4, DuckDB SET threads=4.
    cach = ["pandas\nđọc mọi cột", "pandas\nchỉ cột cần", "polars\nscan_parquet", "DuckDB\nSQL trên tệp"]
    giay_12 = [0.167, 0.073, 0.028, 0.056]
    giay_4 = [0.177, 0.074, 0.026, 0.045]
    x = np.arange(len(cach))
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.bar(x - 0.2, giay_12, width=0.4, color=ve.MAU["nhat"], label="12 luồng")
    ax.bar(x + 0.2, giay_4, width=0.4, color=ve.MAU["chinh"], label="giới hạn 4 nhân")
    for xi, v in zip(x + 0.2, giay_4, strict=True):
        ax.text(xi, v + 0.004, f"{v:.3f}", ha="center", fontsize=8)
    ax.set_xticks(x, cach)
    ax.set_ylabel("giây (trung vị 7 lần)")
    ax.set_title("3,6 triệu chuyến: chỉ đọc cột cần đã nhanh gấp 2,4 lần; mọi cách đều dưới 0,2 giây")
    ax.legend(fontsize=8)
    ve.luu_hinh(fig, HINH / "bam-gio.png")


def hinh_truc_thoi_gian() -> None:
    """Đồng hồ New York theo trục UTC ở hai ngày đổi giờ 2024 — số liệu tính bằng pandas, không gõ tay."""
    fig, truc = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, (ngay, tieu_de, dai, mau_dai, chu_dai) in zip(truc, (
        ("2024-03-10", "10/3/2024: đồng hồ nhảy từ 01:59 lên 03:00", (2, 3), ve.MAU["phu"],
         "02:00–02:59 không có\nthời điểm UTC nào"),
        ("2024-11-03", "3/11/2024: đồng hồ lùi từ 01:59 về 01:00", (1, 2), ve.MAU["vang"],
         "01:00–01:59 ứng với\nhai khoảng UTC"),
    ), strict=True):
        utc = pd.date_range(f"{ngay} 04:00", f"{ngay} 09:00", freq="1min", tz="UTC")
        dp = utc.tz_convert("America/New_York")
        x = (utc - utc[0]).total_seconds().to_numpy() / 3600 + 4
        y = (dp.hour + dp.minute / 60).to_numpy().astype(float)
        y[y > 20] -= 24                       # 23:00 ngày hôm trước vẽ thành -1
        nhay = np.flatnonzero(np.abs(np.diff(y)) > 0.5)
        y_ve = y.copy()
        y_ve[nhay] = np.nan                   # không nối qua chỗ đồng hồ nhảy
        ax.axhspan(*dai, color=mau_dai, alpha=0.18, lw=0)
        ax.text(8.95, -0.9, "vùng tô: " + chu_dai, ha="right", va="center", fontsize=8,
                color="#8A3A00" if ngay.endswith("03-10") else "#8A5A00")
        ax.plot(x, y_ve, color=ve.MAU["chinh"], lw=2)
        for gio in range(4, 10):
            o = pd.Timestamp(f"{ngay} {gio:02d}:00", tz="UTC").tz_convert("America/New_York")
            yy = o.hour + o.minute / 60 - (24 if o.hour > 20 else 0)
            ax.plot(gio, yy, "o", color=ve.MAU["chinh"], ms=4)
            ax.annotate(f"{o:%H:%M} {o:%Z}", (gio, yy), textcoords="offset points", xytext=(4, -12), fontsize=7)
        ax.set_xticks(range(4, 10), [f"{g:02d}:00Z" for g in range(4, 10)])
        ax.set_yticks(range(-1, 6), ["23:00", "00:00", "01:00", "02:00", "03:00", "04:00", "05:00"])
        ax.set_ylim(-1.6, 5.5)
        ax.set_xlabel("thời điểm UTC (giờ)")
        ax.set_title(tieu_de, fontsize=9)
    truc[0].set_ylabel("đồng hồ treo tường New York (giờ)")
    fig.suptitle("Giờ UTC chạy đều; đồng hồ New York mất một giờ ngày 10/3 và lặp một giờ ngày 3/11",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "truc-thoi-gian.png")


if __name__ == "__main__":
    import sys

    # `python ve_hinh.py truc` chỉ sinh hình trục thời gian (không cần dữ liệu tải về)
    chon = sys.argv[1:] or ["dst", "nong", "bam", "truc"]
    ham = {"dst": hinh_dst, "nong": hinh_gio_nong, "bam": hinh_bam_gio, "truc": hinh_truc_thoi_gian}
    with ve.phong_cach():
        for ten in chon:
            ham[ten]()
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
