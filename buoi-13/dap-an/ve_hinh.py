# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 13 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("ft", DAY / "feature.py")
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)
M = ve.MAU


def hinh_tet_di_dong(y: pd.Series) -> dict:
    nam = range(2016, 2026)
    ngay_tet = [pd.Timestamp(ft.tet(n)) for n in nam]
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.5))
    a.scatter([d.year for d in ngay_tet], [d.dayofyear for d in ngay_tet], s=45, color=M["chinh"],
              label="Tết (âm lịch)")
    a.scatter(list(nam), [1] * len(list(nam)), s=45, color=M["phu"], marker="s", label="Tết dương lịch (1/1)")
    a.set_ylabel("ngày thứ mấy trong năm dương")
    a.set_xlabel("năm")
    a.legend(fontsize=8)
    a.set_title("Lễ dương lịch cố định; Tết xê dịch 22–47", fontsize=9)

    d = ft.so_ngay_toi_tet(y.index)
    quanh = (d.abs() <= 15)
    tb = y[quanh].groupby(d[quanh]).mean() / y.mean()
    b.bar(tb.index, tb.to_numpy(), color=M["ba"])
    b.axhline(1, color="black", linewidth=0.8)
    b.set_xlabel("số ngày tới mùng 1 Tết (âm = sau Tết)")
    b.set_ylabel("lượt xem / mức trung bình")
    b.set_title(f"Hiệu ứng Tết: đáy {tb.min():.2f}× vào ngày {int(tb.idxmin())}", fontsize=9)
    fig.suptitle("Vì sao cần feature lịch âm: hiệu ứng bám theo ngày ÂM, còn mọi feature dương lịch "
                 "thì bám theo ngày dương", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "tet-di-dong.png")
    return {"ngày Tết": [str(x.date()) for x in ngay_tet],
            "ngày trong năm": [int(x.dayofyear) for x in ngay_tet],
            "đáy quanh Tết": round(float(tb.min()), 3), "vào ngày": int(tb.idxmin())}


def hinh_ro_ri_minh_hoa(y: pd.Series) -> dict:
    """Cùng một cửa sổ 7 ngày, tính có shift và không shift, rồi cắt dữ liệu để thấy giá trị đổi."""
    nho = y.iloc[:120]
    moc = nho.index[90]
    sach_full = nho.shift(1).rolling(7).mean()
    ro_full = nho.rolling(7, center=True, min_periods=1).mean()
    sach_cat = nho[nho.index <= moc].shift(1).rolling(7).mean()
    ro_cat = nho[nho.index <= moc].rolling(7, center=True, min_periods=1).mean()
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4), sharey=True)
    for ax, full, cat, ten in ((a, sach_full, sach_cat, "shift(1) rồi rolling(7) — nhân quả"),
                               (b, ro_full, ro_cat, "rolling(7, center=True, min_periods=1) — RÒ RỈ")):
        ax.plot(nho / 1e3, color=M["xam"], linewidth=0.7, label="chuỗi gốc")
        ax.plot(full / 1e3, color=M["chinh"], linewidth=1.6, label="tính trên dữ liệu đầy đủ")
        ax.plot(cat / 1e3, color=M["phu"], linewidth=1.6, linestyle="--", label="tính lại sau khi cắt")
        ax.axvline(moc, color="black", linewidth=1)
        ax.set_title(ten, fontsize=9)
        ax.legend(fontsize=7)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    a.set_ylabel("nghìn đơn vị doanh thu")
    lech = float(np.nanmax(np.abs((ro_full.reindex(ro_cat.index) - ro_cat).to_numpy(float))))
    fig.suptitle(f"Bài kiểm rò rỉ: cắt dữ liệu tại vạch đen rồi tính lại. Trái: hai đường trùng khít. "
                 f"Phải: lệch tới {lech / 1e3:.0f} nghìn ngay TRƯỚC vạch", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "kiem-ro-ri.png")
    return {"lệch lớn nhất của rolling centered": round(lech, 1),
            "lệch lớn nhất của rolling có shift":
                round(float(np.nanmax(np.abs((sach_full.reindex(sach_cat.index) - sach_cat).to_numpy(float)))), 12)}


def hinh_gia_ro_ri() -> pd.DataFrame:
    bang = ft.gia_cua_ro_ri()
    fig, ax = plt.subplots(figsize=(10.5, 3.8))
    mau = [M["phu"] if r else M["chinh"] for r in bang["dùng tương lai?"]]
    ax.barh(bang["bộ feature"], bang["so với chỉ lag (%)"], color=mau)
    ax.axvline(0, color="black", linewidth=0.9)
    for i, v in enumerate(bang["so với chỉ lag (%)"]):
        ax.text(max(v, 0) + 0.1, i, f"{v:+.2f}%".replace(".", ","), va="center", ha="left", fontsize=8)
    ax.set_xlabel("MAE so với baseline chỉ dùng lag (%) — âm là tốt hơn")
    ax.set_title("Cam = dùng tương lai. Backtest rò rỉ hứa −3,85%; chạy thật bằng dự báo 1 ngày "
                 "còn −3,10%, bằng dự báo 3 ngày thì +2,20%")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "gia-ro-ri.png")
    return bang


def hinh_du_bao_vs_that() -> dict:
    tt = ft.doc_thoi_tiet().dropna()
    cua_so = slice("2024-07-01", "2024-07-15")
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    a.plot(tt.loc[cua_so, "nhiet_do_that"], color="black", linewidth=1.5, label="thật (ERA5)")
    a.plot(tt.loc[cua_so, "du_bao_1_ngay"], color=M["chinh"], linewidth=1.1, label="dự báo trước 1 ngày")
    a.plot(tt.loc[cua_so, "du_bao_3_ngay"], color=M["phu"], linewidth=1.1, label="dự báo trước 3 ngày")
    a.set_ylabel("°C")
    a.legend(fontsize=8)
    a.set_title("Dallas, nửa đầu tháng 7/2024", fontsize=9)
    a.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    sai = {"dự báo 1 ngày": (tt["nhiet_do_that"] - tt["du_bao_1_ngay"]),
           "dự báo 3 ngày": (tt["nhiet_do_that"] - tt["du_bao_3_ngay"])}
    b.hist([v.to_numpy() for v in sai.values()], bins=40, label=list(sai), color=[M["chinh"], M["phu"]])
    b.set_xlabel("sai số = thật − dự báo (°C)")
    b.set_ylabel("số giờ")
    b.legend(fontsize=8)
    b.set_title(f"MAE {sai['dự báo 1 ngày'].abs().mean():.2f} °C và "
                f"{sai['dự báo 3 ngày'].abs().mean():.2f} °C".replace(".", ","), fontsize=9)
    fig.suptitle("Lúc ra dự báo bạn KHÔNG có nhiệt độ thật — chỉ có bản dự báo, và nó sai thật",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "du-bao-vs-that.png")
    return ft.sai_so_du_bao_thoi_tiet()


def hinh_biet_truoc(y: pd.Series) -> dict:
    f = ft.bo_feature(y)
    bang = ft.bang_biet_truoc(f)
    dem = bang["biết trước"].value_counts()
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    ax.barh(dem.index, dem.to_numpy(), color=[M["ba"], M["chinh"], M["bon"]][: len(dem)])
    for i, v in enumerate(dem.to_numpy()):
        ax.text(v + 0.3, i, str(v), va="center", fontsize=9)
    ax.set_xlabel("số feature")
    ax.set_title(f"{f.shape[1]} feature, mỗi feature khai rõ 'biết trước bao lâu'")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "biet-truoc.png")
    return dem.to_dict()


if __name__ == "__main__":
    wiki = ft.doc_wiki()
    ban_le = ft.doc_ban_le().ffill()
    with ve.phong_cach():
        print("tết di động", hinh_tet_di_dong(wiki))
        print("kiểm rò rỉ", hinh_ro_ri_minh_hoa(ban_le))
        print(hinh_gia_ro_ri().round(2).to_string(index=False))
        print("dự báo vs thật", hinh_du_bao_vs_that())
        print("biết trước", hinh_biet_truoc(ban_le))
    print(ft.gia_tri_feature_tet().round(1).to_string(index=False))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
