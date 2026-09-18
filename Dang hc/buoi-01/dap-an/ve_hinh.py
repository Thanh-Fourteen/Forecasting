# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 1 → ../hinh/*.png (150 dpi)

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
spec = importlib.util.spec_from_file_location("dg", DAY / "danh_gia.py")
dg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dg)

CU, CO = 4, 1  # chi phí mỗi kWh dự báo thiếu / thừa


def chi_phi(y, du_bao) -> float:
    d = np.asarray(y, float) - np.asarray(du_bao, float)
    d = d[~np.isnan(d)]
    return float(np.mean(np.where(d > 0, CU * d, -CO * d)))


def hinh_mot_duong(s: pd.Series) -> None:
    ngay = s.resample("D").sum(min_count=20)
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.plot(ngay.index, ngay.to_numpy(), color=ve.MAU["xam"], linewidth=0.6, label="mỗi ngày")
    ax.plot(ngay.index, ngay.rolling(28, center=True, min_periods=14).mean().to_numpy(), color=ve.MAU["chinh"],
            linewidth=1.6, label="trung bình 28 ngày")
    for nam in (2007, 2008, 2009, 2010):
        ax.axvspan(pd.Timestamp(f"{nam}-08-01"), pd.Timestamp(f"{nam}-08-31"), color=ve.MAU["phu"], alpha=0.08)
    ax.text(pd.Timestamp("2008-08-03"), 72, "tháng 8", color=ve.MAU["phu"], fontsize=8)
    ax.set_ylabel("kWh / ngày")
    ax.set_title("Một hộ ở Sceaux, 12/2006–11/2010: mùa đông cao, tháng 8 gần như vắng nhà, năm sau giống năm trước")
    ax.legend(fontsize=8, loc="upper right")
    ve.luu_hinh(fig, HINH / "mot-duong.png")


def hinh_sai_so_ao(s: pd.Series, cuon: pd.DataFrame) -> None:
    te = s[s.index >= pd.Timestamp(dg.MOC)]
    ao = dg.mae(te, dg.du_bao_bang_lich(dg.bang_lich(s), te.index))
    kq = dg.danh_gia(s)
    ten = ["bảng lịch — chấm trên\ndữ liệu đã dùng để làm"] + [f"{t}" for t in kq.index]
    gia_tri = [ao, *kq.to_numpy()]
    mau = [ve.MAU["phu"]] + [ve.MAU["chinh"] if t == "bảng lịch" else ve.MAU["xam"] for t in kq.index]
    fig, ax = plt.subplots(figsize=(10, 3.2))
    y = np.arange(len(ten))[::-1]
    ax.barh(y, gia_tri, color=mau)
    for yi, v in zip(y, gia_tri, strict=True):
        ax.text(v + 0.008, yi, f"{v:.3f}".replace(".", ","), va="center", fontsize=8)
    ax.set_yticks(y, ten, fontsize=8)
    ax.set_xlabel("MAE (kWh / giờ) trên 46 tuần năm 2010, tầm 168 giờ")
    ax.set_xlim(0, 0.85)
    ax.set_title("Chấm trên dữ liệu đã dùng: 0,380 — nhất bảng. Chấm trung thực: 0,508 — thua trung bình 4 tuần")
    ve.luu_hinh(fig, HINH / "sai-so-ao.png")


def hinh_mot_tuan(s: pd.Series, cuon: pd.DataFrame) -> str:
    bang_tat_ca = dg.bang_lich(s)
    cuon = cuon.assign(ao=dg.du_bao_bang_lich(bang_tat_ca, cuon.index))
    theo_tuan = cuon.groupby("goc").apply(lambda d: dg.mae(d["y"], d["bảng lịch"]) - dg.mae(d["y"], d["ao"]))
    goc = theo_tuan.idxmax()
    d = cuon[cuon["goc"] == goc]
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.plot(d.index, d["y"], color="black", linewidth=1.2, label="thực tế")
    ax.plot(d.index, d["ao"], color=ve.MAU["phu"], linewidth=1, label=f"bảng lịch khớp cả 2010 (MAE {dg.mae(d['y'], d['ao']):.2f})".replace(".", ","))
    ax.plot(d.index, d["bảng lịch"], color=ve.MAU["chinh"], linewidth=1,
            label=f"bảng lịch chỉ từ trước gốc (MAE {dg.mae(d['y'], d['bảng lịch']):.2f})".replace(".", ","))
    ax.plot(d.index, d["TB 4 tuần"], color=ve.MAU["ba"], linewidth=1, linestyle="--",
            label=f"TB 4 tuần (MAE {dg.mae(d['y'], d['TB 4 tuần']):.2f})".replace(".", ","))
    ax.set_ylabel("kWh / giờ")
    ax.set_title(f"Tuần {goc:%d/%m/%Y}: đường cam 'trúng' hơn vì 1/4 số liệu của mỗi ô bảng là chính tuần này")
    ax.set_ylim(0, 4.3)
    ax.legend(fontsize=8, loc="upper left", ncols=2)
    ve.luu_hinh(fig, HINH / "mot-tuan.png")
    return f"{goc:%Y-%m-%d}"


def hinh_tong_tuan(cuon: pd.DataFrame) -> None:
    tuan = cuon.groupby("goc")[["y", "TB 4 tuần", "tuần trước", "bảng lịch"]].sum(min_count=1)
    du = cuon.groupby("goc")["y"].apply(lambda x: x.notna().all())
    tuan.loc[~du, "y"] = np.nan
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(tuan.index, tuan["y"], color="black", marker="o", markersize=3, label="thực tế (tuần đủ số đo)")
    for cot, mau in (("bảng lịch", ve.MAU["chinh"]), ("TB 4 tuần", ve.MAU["ba"]), ("tuần trước", ve.MAU["xam"])):
        ax.plot(tuan.index, tuan[cot], color=mau, linewidth=1.2,
                label=f"{cot} (MAE {dg.mae(tuan['y'], tuan[cot]):.1f} kWh/tuần)".replace(".", ","))
    ax.set_ylabel("kWh / tuần")
    ax.set_title("Cộng lên TỔNG TUẦN thì thứ hạng đảo: bảng lịch nhớ kỳ nghỉ tháng 8, hai baseline thì không")
    ax.legend(fontsize=8, loc="lower left")
    ve.luu_hinh(fig, HINH / "tong-tuan.png")


def hinh_chi_phi(s: pd.Series, cuon: pd.DataFrame) -> dict[str, float]:
    c09 = dg.du_bao_cuon(s[s.index < pd.Timestamp(dg.MOC)], moc="2009-01-05")
    loi = (c09["y"] - c09["TB 4 tuần"]).dropna()
    q = float(loi.quantile(CU / (CU + CO)))
    cong = np.round(np.arange(0, 1.01, 0.05), 2)
    y, f = cuon["y"].to_numpy(), cuon["TB 4 tuần"].to_numpy()
    cp = [chi_phi(y, f + k) for k in cong]
    sai = [dg.mae(y, f + k) for k in cong]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.2))
    a.plot(cong, cp, marker="o", markersize=3, color=ve.MAU["chinh"])
    a.axvline(q, color=ve.MAU["phu"], linestyle="--", linewidth=1)
    a.text(q + 0.02, max(cp) * 0.97, f"quantile 0,8 sai số 2009 = {q:.3f}".replace(".", ","), fontsize=8)
    a.set_xlabel("kWh cộng thêm vào dự báo TB 4 tuần")
    a.set_ylabel("chi phí trung bình / giờ")
    a.set_title(f"Chi phí (thiếu {CU} : thừa {CO}) — thấp nhất khi đặt cao hơn")
    b.plot(cong, sai, marker="o", markersize=3, color=ve.MAU["ba"])
    b.axvline(q, color=ve.MAU["phu"], linestyle="--", linewidth=1)
    b.set_xlabel("kWh cộng thêm vào dự báo TB 4 tuần")
    b.set_ylabel("MAE (kWh / giờ)")
    b.set_title("Cùng lúc đó MAE tăng đều")
    fig.suptitle("Năm 2010: con số tốt nhất theo MAE không phải con số tốt nhất cho quyết định có chi phí lệch",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "chi-phi-bat-doi-xung.png")
    return {"q": q, "chi_phi_diem": chi_phi(y, f), "chi_phi_q": chi_phi(y, f + q), "mae_q": dg.mae(y, f + q),
            "thieu_diem": float(np.nanmean(np.where(np.isnan(y), np.nan, y > f))),
            "thieu_q": float(np.nanmean(np.where(np.isnan(y), np.nan, y > f + q)))}


if __name__ == "__main__":
    s = dg.doc_dien_theo_gio()
    cuon = dg.du_bao_cuon(s)
    with ve.phong_cach():
        hinh_mot_duong(s)
        hinh_sai_so_ao(s, cuon)
        print("tuần minh hoạ:", hinh_mot_tuan(s, cuon))
        hinh_tong_tuan(cuon)
        print({k: round(v, 4) for k, v in hinh_chi_phi(s, cuon).items()})
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
