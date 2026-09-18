# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 10 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
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
spec = importlib.util.spec_from_file_location("ls", DAY / "lam_sach.py")
ls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ls)
M = ve.MAU


def hinh_ban_do_lo_hong(bk: pd.DataFrame) -> dict:
    ty_le = ls.ty_le_thieu_theo_tram(bk)
    fig, ax = plt.subplots(figsize=(11, 3.8))
    anh = ax.imshow(ty_le.to_numpy().T, aspect="auto", cmap="magma_r", vmin=0, vmax=20)
    ax.set_yticks(range(len(ty_le.columns)), ty_le.columns, fontsize=7)
    buoc = 3
    ax.set_xticks(range(0, len(ty_le), buoc), [str(p) for p in ty_le.index[::buoc]], rotation=45,
                  ha="right", fontsize=7)
    plt.colorbar(anh, ax=ax, shrink=0.9, label="% giờ thiếu")
    ax.set_title("Lỗ hổng PM2.5 12 trạm Bắc Kinh: thiếu đi thành TỪNG MẢNG theo trạm và theo tháng, "
                 "không rải đều", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ban-do-lo-hong.png")
    return {"thiếu trung bình %": round(float(bk.isna().mean().mean() * 100), 2),
            "tháng-trạm tệ nhất %": round(float(ty_le.to_numpy().max()), 1),
            "số ô (trạm × tháng) thiếu > 10%": int((ty_le > 10).to_numpy().sum())}


def hinh_hai_loai_thieu(tho: pd.DataFrame) -> dict:
    luoi = pd.date_range(f"{ls.NAM}-01-01", f"{ls.NAM}-12-31 23:30", freq=ls.DO_DAI_MOC)
    thieu_moc = luoi.difference(tho.index)
    theo_thang = pd.Series(1, index=thieu_moc).resample("MS").sum().reindex(
        pd.date_range(f"{ls.NAM}-01-01", periods=12, freq="MS"), fill_value=0)
    day_du = ls.luoi_day_du(tho)
    dai = ls.do_dai_lo_hong(day_du["temperature"])
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.4))
    a.bar(range(12), theo_thang.to_numpy(), color=M["chinh"])
    a.set_xticks(range(12), [f"T{i + 1}" for i in range(12)], fontsize=8)
    a.set_ylabel("số mốc 30 phút không có dòng")
    a.set_title(f"Thiếu MỐC: {len(thieu_moc)} mốc, dồn vào vài tháng", fontsize=9)
    b.hist(dai, bins=np.arange(1, max(dai.max(), 12) + 2) - 0.5, color=M["phu"])
    b.set_xlabel("độ dài lỗ hổng (số bước 30 phút)")
    b.set_ylabel("số lỗ")
    b.set_title(f"Độ dài lỗ: {len(dai)} lỗ, dài nhất {int(dai.max())} bước", fontsize=9)
    fig.suptitle("Hai loại thiếu khác nhau: không có DÒNG (trái) khác với có dòng mà ô RỖNG — "
                 "chỉ `isna()` sẽ không thấy loại thứ nhất", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "hai-loai-thieu.png")
    return {"thiếu mốc": int(len(thieu_moc)), "tháng nhiều nhất": int(theo_thang.max()),
            "số lỗ": int(len(dai)), "lỗ dài nhất": int(dai.max()),
            "lỗ 1 bước %": round(float((dai == 1).mean() * 100), 1)}


def hinh_gia_tri_tra_hinh(tho: pd.DataFrame) -> dict:
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(11, 3.2))
    a.hist(tho["visibility"].dropna(), bins=40, color=M["chinh"])
    a.set_title("visibility (km): 35% số dòng đúng 9,999", fontsize=9)
    a.set_xlabel("km")
    b.hist(tho["relative_humidity"].dropna(), bins=40, color=M["ba"])
    b.set_title("độ ẩm (%): 5,7% chạm trần 100", fontsize=9)
    b.set_xlabel("%")
    t = tho["temperature"].dropna()
    c.hist(t, bins=np.arange(t.min() - 0.5, t.max() + 1.5, 0.5), color=M["phu"])
    c.set_title("nhiệt độ (°C): chỉ có giá trị nguyên", fontsize=9)
    c.set_xlabel("°C")
    for ax in (a, b, c):
        ax.set_ylabel("số dòng")
    fig.suptitle("Ba thứ không phải 'số đo': mã trá hình, trần cảm biến, và độ phân giải thô — "
                 "histogram lộ ra cả ba", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "gia-tri-tra-hinh.png")
    return {"trá hình": ls.doan_tra_hinh(tho).to_dict("records"),
            "độ phân giải nhiệt độ": ls.do_phan_giai(tho["temperature"])}


def hinh_so_sanh_dien(y: pd.Series, hx: pd.Series) -> pd.DataFrame:
    bang = ls.so_sanh_dien(y, hang_xom=hx)
    rong = bang.pivot(index="cách điền", columns="kiểu che", values="MAE")
    thu_tu = rong.sort_values("che điểm 10%").index
    fig, ax = plt.subplots(figsize=(9.5, 3.6))
    x = np.arange(len(thu_tu))
    ax.bar(x - 0.2, rong.loc[thu_tu, "che điểm 10%"], 0.4, color=M["chinh"], label="che điểm 10% (lỗ ngắn)")
    ax.bar(x + 0.2, rong.loc[thu_tu, "che khối 48 giờ"], 0.4, color=M["phu"], label="che khối 48 giờ (lỗ dài)")
    ax.set_xticks(x, thu_tu, rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("MAE trên các ô bị che (°C)")
    ax.legend(fontsize=8)
    ax.set_title("Thứ hạng ĐẢO: nội suy tuyến tính hạng 1/7 với lỗ ngắn (0,29) nhưng tụt xuống 5/7 với "
                 "lỗ 48 giờ (2,17); trạm hàng xóm đi ngược lại, từ 5/7 lên 1/7")
    ve.luu_hinh(fig, HINH / "so-sanh-dien.png")
    return rong.round(3)


def hinh_mot_lo_dai(y: pd.Series, hx: pd.Series, seed: int = 0) -> dict:
    that = y.dropna()
    che = ls.che_khoi(that, 96, 5, seed)
    o_che = that.notna() & che.isna()
    dau = che[o_che].index[0]
    cua_so = slice(dau - pd.Timedelta("24h"), dau + pd.Timedelta("72h"))
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.plot(that[cua_so], color="black", linewidth=1.6, label="giá trị thật")
    for ten, mau, net, rong in (("ffill", M["xam"], "-", 3.0),
                                ("tuyến tính", M["phu"], "--", 1.8),
                                ("mùa vụ (ngày trước)", M["ba"], "-", 1.2),
                                ("hàng xóm (Open-Meteo)", M["chinh"], "-", 1.4)):
        z = ls.CACH_DIEN[ten](che, hang_xom=hx)
        ax.plot(z[cua_so].where(o_che[cua_so]), linewidth=rong, linestyle=net, color=mau, label=ten)
    ax.axvspan(dau, dau + pd.Timedelta("48h"), color="red", alpha=0.06)
    ax.set_ylabel("nhiệt độ (°C)")
    ax.legend(fontsize=8, ncol=3)
    ax.set_title("Một lỗ 48 giờ: ffill và nội suy tuyến tính đều thành đường phẳng 24 °C, xoá sạch "
                 "nhịp ngày (thật: 21–27 °C); chỉ trạm hàng xóm giữ được hình dạng")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "mot-lo-dai.png")
    return {"bắt đầu lỗ": str(dau), "số ô bị che": int(o_che.sum())}


def hinh_mnar() -> dict:
    kq = ls.mo_phong_mnar()
    rng = np.random.default_rng(0)
    n = 5000
    moc = pd.date_range("2024-01-01", periods=n, freq="30min")
    that = pd.Series(rng.normal(0, 1, n), index=moc)
    mnar = that.mask(that > 1.0)
    dien = ls.dien_tuyen_tinh(mnar)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.4))
    a.hist(that, bins=50, alpha=0.55, color=M["xam"], label="thật")
    a.hist(dien, bins=50, alpha=0.55, color=M["phu"], label="sau khi điền")
    a.axvline(1.0, color="black", linestyle="--", linewidth=0.9)
    a.legend(fontsize=8)
    a.set_title("MNAR: mất khi giá trị > 1 → đuôi phải bị cắt cụt", fontsize=9)
    mcar = that.mask(pd.Series(rng.random(n) < 0.1, index=moc))
    b.bar(["thật", "điền khi MCAR", "điền khi MNAR"],
          [that.mean(), ls.dien_tuyen_tinh(mcar).mean(), dien.mean()],
          color=[M["xam"], M["chinh"], M["phu"]])
    b.axhline(0, color="black", linewidth=0.8)
    b.set_ylabel("trung bình")
    b.set_title(f"Trung bình lệch {abs(kq['sau khi điền, thiếu MNAR']):.2f} khi MNAR", fontsize=9)
    fig.suptitle("Cơ chế thiếu quyết định điền được hay không: MCAR điền vô tư, MNAR thì điền kiểu gì "
                 "cũng lệch", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "mnar.png")
    return kq


if __name__ == "__main__":
    tho = ls.doc_noi_bai()
    hx = ls.doc_hang_xom()["temperature_2m"]
    y = ls.luoi_day_du(tho)["temperature"]
    bk = ls.doc_bac_kinh()
    with ve.phong_cach():
        print("bản đồ lỗ hổng", hinh_ban_do_lo_hong(bk))
        print("hai loại thiếu", hinh_hai_loai_thieu(tho))
        print("trá hình", hinh_gia_tri_tra_hinh(tho))
        print(hinh_so_sanh_dien(y, hx).to_string())
        print("một lỗ dài", hinh_mot_lo_dai(y, hx))
        print("mnar", hinh_mnar())
    print("báo cáo chất lượng:")
    print(ls.bao_cao_chat_luong(tho).round(3).to_string(index=False))
    print("sau làm sạch:", ls.bao_cao_lam_sach(ls.lam_sach(tho, hang_xom=hx)))
    print("MNAR Bắc Kinh (thật):", ls.bang_chung_mnar(bk))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
