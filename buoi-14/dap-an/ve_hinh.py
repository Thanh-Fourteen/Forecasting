# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 14 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

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
spec = importlib.util.spec_from_file_location("dg", DAY / "danh_gia.py")
dg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dg)
M = ve.MAU


def _chuoi_minh_hoa(hoc: dict, kiem: dict) -> str:
    """Chuỗi mà nhịp tuần giúp thật (seasonal naive thắng naive rõ nhất) và mọi baseline cùng thang: bốn đường
    hiện rõ trên một hình."""
    diem = {}
    for t, y in hoc.items():
        that = kiem[t]
        mase = {k: dg.mase(that, (h(y, dg.TAM, dg.M) if k == "seasonal naive" else h(y, dg.TAM)), y)
                for k, h in dg.BASELINE.items()}
        if max(mase.values()) < 4 and abs(np.mean(y) - y[-1]) < 3 * np.std(y[-90:]):
            diem[t] = mase["naive"] - mase["seasonal naive"]
    return max(diem, key=diem.get)


def hinh_bon_baseline(hoc: dict, kiem: dict, ten: str | None = None) -> dict:
    ten = ten or _chuoi_minh_hoa(hoc, kiem)
    y, that = hoc[ten], kiem[ten]
    n = 90
    truc = np.arange(-n, dg.TAM)
    fig, ax = plt.subplots(figsize=(10.5, 3.6))
    ax.plot(truc[:n], y[-n:], color=M["xam"], linewidth=1.1, label="lịch sử")
    ax.plot(truc[n:], that, color="black", linewidth=1.8, label="thực tế")
    mau = [M["chinh"], M["phu"], M["ba"], M["bon"]]
    for (ten_bl, ham), c in zip(dg.BASELINE.items(), mau, strict=True):
        d = ham(y, dg.TAM, dg.M) if ten_bl == "seasonal naive" else ham(y, dg.TAM)
        ax.plot(truc[n:], d, color=c, linewidth=1.3, linestyle="--",
                label=f"{ten_bl} (MASE {dg.mase(that, d, y):.2f})".replace(".", ","))
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("bước so với thời điểm ra dự báo")
    ax.legend(fontsize=8, ncol=3)
    ax.set_title("Bốn baseline trên một chuỗi M4 theo ngày: chúng khác nhau ở giả định, "
                 "không ở độ phức tạp")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "bon-baseline.png")
    return {"chuỗi": ten, "độ dài học": len(y)}


def hinh_chan_doan_phan_du(hoc: dict, ten: str | None = None) -> dict:
    ten = ten or sorted(hoc)[0]
    e = dg.phan_du_mua_vu(hoc[ten])
    lb = dg.ljung_box(e)
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(11, 3.2))
    a.plot(e, color=M["chinh"], linewidth=0.7)
    a.axhline(0, color="black", linewidth=0.8)
    a.set_title(f"phần dư theo thời gian (ME = {np.mean(e):.1f})", fontsize=9)
    r = dg._acf(e, 30)
    gioi_han = 1.96 / np.sqrt(e.size)
    b.bar(np.arange(1, 31), r, color=M["phu"])
    b.axhline(gioi_han, color="black", linestyle="--", linewidth=0.8)
    b.axhline(-gioi_han, color="black", linestyle="--", linewidth=0.8)
    b.set_title(f"ACF phần dư — Ljung–Box p = {lb['p']:.3f}", fontsize=9)
    b.set_xlabel("trễ")
    c.hist(e, bins=40, color=M["ba"])
    c.set_title("phân phối phần dư", fontsize=9)
    fig.suptitle("Phần dư của seasonal naive vi phạm gần hết giả định — đó là lý do không tin "
                 "khoảng dự báo của baseline", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "chan-doan-phan-du.png")
    return {"chuỗi": ten, **lb}


def hinh_chi_so_quyet_dinh() -> dict:
    mau = dg.mau_lech_phai()
    kq = dg.toi_uu_theo_chi_so(mau)
    luoi = np.linspace(float(np.min(mau)), float(np.quantile(mau, 0.995)), 400)
    mae_theo = np.array([np.mean(np.abs(mau - c)) for c in luoi])
    rmse_theo = np.array([np.sqrt(np.mean((mau - c) ** 2)) for c in luoi])
    mape_theo = np.array([np.mean(np.abs((mau - c) / mau)) for c in luoi])
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.5))
    a.hist(mau, bins=80, range=(0, np.quantile(mau, 0.99)), color=M["xam"])
    for nhan, x, c in (("trung vị", kq["trung vị mẫu"], M["chinh"]),
                       ("trung bình", kq["trung bình mẫu"], M["phu"]),
                       ("tối ưu MAPE", kq["hằng số tối ưu MAPE"], M["ba"])):
        a.axvline(x, color=c, linewidth=1.6, label=f"{nhan} = {x:.1f}")
    a.legend(fontsize=8)
    a.set_title("phân phối lệch phải (lognormal)", fontsize=9)
    for nhan, v, c in (("MAE", mae_theo / mae_theo.min(), M["chinh"]),
                       ("RMSE", rmse_theo / rmse_theo.min(), M["phu"]),
                       ("MAPE", mape_theo / mape_theo.min(), M["ba"])):
        b.plot(luoi, v, color=c, linewidth=1.4, label=nhan)
    b.set_xlabel("hằng số dự báo")
    b.set_ylabel("chỉ số (chuẩn hoá về 1 tại điểm tối ưu)")
    b.set_ylim(1, 1.6)
    b.legend(fontsize=8)
    b.set_title("mỗi chỉ số tối ưu ở một chỗ khác nhau", fontsize=9)
    fig.suptitle(f"Chọn chỉ số là chọn dự báo: MAE → trung vị ({kq['hằng số tối ưu MAE']:.1f}), "
                 f"RMSE → trung bình ({kq['hằng số tối ưu RMSE']:.1f}), "
                 f"MAPE → thấp hơn cả hai ({kq['hằng số tối ưu MAPE']:.1f})",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "chi-so-quyet-dinh.png")
    return {k: round(v, 2) for k, v in kq.items()}


def hinh_doi_chi_so_doi_hang(bang_m4: pd.DataFrame, bang_bl: pd.DataFrame) -> dict:
    hang_m4, hang_bl = dg.xep_hang(bang_m4), dg.xep_hang(bang_bl)
    cot = ["MAE", "RMSE", "MAPE", "sMAPE", "WAPE", "MASE", "RMSSE"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    for ax, hang, ten in ((a, hang_m4, "M4 daily (không có số 0)"),
                          (b, hang_bl, "bán lẻ (75% ngày bằng 0)")):
        ax.imshow(hang[cot].to_numpy(dtype=float), cmap="RdYlGn_r", vmin=1, vmax=4)
        ax.set_xticks(range(len(cot)), cot, rotation=30, ha="right", fontsize=8)
        ax.set_yticks(range(len(hang)), hang["mô hình"], fontsize=8)
        for i in range(len(hang)):
            for j, c in enumerate(cot):
                v = hang[c].iloc[i]
                ax.text(j, i, "—" if pd.isna(v) else str(int(v)), ha="center", va="center", fontsize=8)
        ax.set_title(ten, fontsize=9)
    fig.suptitle("Cùng dữ liệu, cùng dự báo: đổi chỉ số là đổi mô hình 'tốt nhất' — "
                 "và MAPE không tính được cho chuỗi có số 0", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "doi-chi-so-doi-hang.png")
    return {"M4": hang_m4.to_dict("records"), "bán lẻ": hang_bl.to_dict("records")}


if __name__ == "__main__":
    chuoi = dg.lay_mau(dg.doc_tsf(), 1000)
    hoc, kiem = dg.chia(chuoi)
    bang_m4 = dg.danh_gia(kiem, dg.du_bao_baseline(hoc), hoc)
    ban_le = dg.chuoi_ban_le()
    h_bl, k_bl = dg.chia(ban_le)
    bang_bl = dg.danh_gia(k_bl, dg.du_bao_baseline(h_bl), h_bl)
    with ve.phong_cach():
        print("baseline", hinh_bon_baseline(hoc, kiem))
        print("phần dư", hinh_chan_doan_phan_du(hoc))
        print("chỉ số quyết định", hinh_chi_so_quyet_dinh())
        print("đổi chỉ số", hinh_doi_chi_so_doi_hang(bang_m4, bang_bl))
        du_bao_sn = {t: dg.bl_naive_mua_vu(v, dg.TAM, dg.M) for t, v in hoc.items()}
        print(dg.so_voi_utilsforecast(kiem, du_bao_sn, hoc).round(4).to_string(index=False))
    print("\nM4:", bang_m4.round(3).to_string(index=False))
    print("\nbán lẻ:", bang_bl.round(3).to_string(index=False))
    print("\nchẩn đoán:", dg.tom_tat_chan_doan(dg.chan_doan_phan_du(hoc)))
    print("tỷ lệ ngày bằng 0 (bán lẻ):",
          round(float(np.mean([np.mean(v == 0) for v in ban_le.values()])), 3))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
