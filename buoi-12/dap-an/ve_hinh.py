# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 12 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

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
spec = importlib.util.spec_from_file_location("kn", DAY / "khu_nhieu.py")
kn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kn)
M = ve.MAU


def hinh_pho(df: pd.DataFrame) -> dict:
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.4))
    kq = {}
    for ax, cot, ten in ((a, "Appliances", "điện tiêu thụ thiết bị (Wh)"), (b, "T2", "nhiệt độ phòng khách (°C)")):
        f, P = kn.pho(df[cot])
        ax.loglog(f[1:], P[1:], color=M["chinh"], linewidth=0.8)
        for chu_ky, nhan in ((24, "24 giờ"), (12, "12 giờ"), (1, "1 giờ")):
            ax.axvline(1 / chu_ky, color=M["phu"], linestyle="--", linewidth=0.8)
            ax.text(1 / chu_ky, P[1:].max() * 0.5, nhan, fontsize=7, rotation=90, color=M["phu"])
        ax.set_xlabel("tần số (chu kỳ/giờ)")
        ax.set_ylabel("mật độ phổ")
        ax.set_title(ten, fontsize=9)
        cao = f > 1.0
        kq[cot] = {"chu_ky_manh_nhat": round(float(1 / f[1:][np.argmax(P[1:])]), 2),
                   "ty_le_cong_suat_tren_1_chu_ky_gio": round(float(P[cao].sum() / P[1:].sum()), 3)}
    fig.suptitle("Phổ công suất: cả hai cảm biến có nhịp ngày rõ, nhưng điện tiêu thụ còn nhiều năng lượng ở tần số cao",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "pho-cam-bien.png")
    return kq


def hinh_aliasing() -> dict:
    t = np.arange(6000) / kn.FS
    that = 20 + 2 * np.sin(2 * np.pi * t / 24)
    y = that + 0.5 * np.sin(2 * np.pi * 1.4 * t)
    tho, sach = kn.ha_mau(y, 6, loc_truoc=False), kn.ha_mau(y, 6, loc_truoc=True)
    f0, P0 = kn.pho(y, fs=kn.FS, nperseg=1024)
    f1, P1 = kn.pho(tho, fs=1.0, nperseg=512)
    f2, P2 = kn.pho(sach, fs=1.0, nperseg=512)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.4))
    a.plot(t[:180], y[:180], color=M["xam"], linewidth=0.8, label="10 phút/mẫu")
    a.plot(t[:180:6], tho[:30], "o-", color=M["phu"], markersize=3, linewidth=0.8, label="hạ mẫu thô 1 giờ")
    a.plot(t[:180:6], sach[:30], "s-", color=M["chinh"], markersize=3, linewidth=0.8, label="lọc rồi hạ mẫu")
    a.set_xlabel("giờ")
    a.legend(fontsize=7)
    a.set_title("30 giờ đầu: dao động 43 phút bị lấy mẫu sai", fontsize=9)
    b.semilogy(f1, P1, color=M["phu"], label="hạ mẫu thô")
    b.semilogy(f2, P2, color=M["chinh"], label="lọc rồi hạ mẫu")
    b.axvline(0.4, color="black", linestyle="--", linewidth=0.8)
    b.text(0.41, P1.max() * 0.2, "0,4 chu kỳ/giờ\n= chu kỳ giả 2,5 giờ", fontsize=7)
    b.set_xlabel("tần số sau khi hạ mẫu (chu kỳ/giờ)")
    b.set_ylabel("mật độ phổ")
    b.legend(fontsize=7)
    b.set_title("Phổ sau khi hạ mẫu", fontsize=9)
    fig.suptitle("Aliasing: thành phần 1,4 chu kỳ/giờ gập xuống thành 0,4 chu kỳ/giờ khi hạ mẫu mà không lọc trước",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "aliasing.png")
    return {"nyquist_cu": kn.FS / 2, "nyquist_moi": 0.5, "cong_suat_2_5h_tho": round(kn.cong_suat_quanh(f1, P1, 2.5), 2),
            "cong_suat_2_5h_loc": round(kn.cong_suat_quanh(f2, P2, 2.5), 4),
            "cong_suat_43phut_goc": round(kn.cong_suat_quanh(f0, P0, 1 / 1.4), 2)}


def hinh_bo_loc() -> pd.DataFrame:
    that, y = kn.sinh_tin_hieu()
    bang = kn.bang_bo_loc(y, that)
    fig, (a, b) = plt.subplots(2, 1, figsize=(10, 6.8))
    doan = slice(600, 900)
    a.plot(np.arange(*doan.indices(len(y)))[:], y[doan], color=M["xam"], linewidth=0.6, label="dữ liệu có nhiễu")
    a.plot(np.arange(*doan.indices(len(y))), that[doan], color="black", linewidth=1.5, label="tín hiệu thật")
    for ten, mau in (("MA trailing 13", M["phu"]), ("MA centered 13", M["chinh"]), ("Kalman filter (tham số cố định)", M["ba"])):
        z = np.asarray(kn.bo_loc_mac_dinh(y[:600])[ten](y), dtype=float)
        a.plot(np.arange(*doan.indices(len(y))), z[doan], linewidth=1.1, color=mau, label=ten)
    a.legend(fontsize=7, ncols=2)
    a.set_title("MA trailing chạy sau tín hiệu thật (trễ 6 bước); MA centered trùng khít — vì nó đã nhìn tương lai",
                fontsize=9)
    x = np.arange(len(bang))
    mau = [M["phu"] if v else M["chinh"] for v in bang["dùng tương lai?"]]
    b.bar(x, bang["RMSE"], color=mau)
    for xi, (r, tre) in enumerate(zip(bang["RMSE"], bang["trễ (bước)"], strict=True)):
        b.text(xi, r + 0.03, f"trễ {tre}", ha="center", fontsize=7)
    b.set_xticks(x, [t.replace(" (", "\n(") for t in bang["bộ lọc"]], fontsize=6.5, rotation=20, ha="right")
    b.set_ylabel("RMSE so với tín hiệu thật")
    b.set_title("Cam = dùng tương lai (RMSE thấp nhưng không dùng được để dự báo)", fontsize=9)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "bo-loc.png")
    return bang


def hinh_kiem_nhan_qua() -> dict:
    that, y = kn.sinh_tin_hieu(n=400)
    k0 = len(y) - 10
    y2 = y.copy()
    y2[k0:] += 50
    fig, (a, b) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    a.plot(y, color=M["xam"], linewidth=0.8, label="dữ liệu gốc")
    a.plot(y2, color=M["phu"], linewidth=0.8, label="đổi 10 giá trị CUỐI (+50)")
    a.axvline(k0, color="black", linestyle="--")
    a.legend(fontsize=8)
    a.set_title("Bài kiểm: đổi phần cuối chuỗi rồi xem đầu ra bộ lọc ở phần TRƯỚC có đổi không", fontsize=9)
    for ten, mau in (("MA trailing 13", M["chinh"]), ("MA centered 13", M["phu"])):
        f = kn.bo_loc_mac_dinh(y[:200])[ten]
        lech = np.abs(np.asarray(f(y2), dtype=float) - np.asarray(f(y), dtype=float))
        b.semilogy(np.maximum(lech, 1e-16), color=mau, label=f"{ten}: đổi tối đa ở quá khứ {np.nanmax(lech[:k0]):.3g}")
    b.axvline(k0, color="black", linestyle="--")
    b.set_ylabel("|đầu ra mới − cũ|")
    b.set_xlabel("chỉ số thời gian")
    b.legend(fontsize=8)
    b.set_title("MA trailing: 0 ở mọi mốc trước vạch. MA centered: lộ ra ở 6 mốc ngay trước vạch", fontsize=9)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "kiem-nhan-qua.png")
    kq = {}
    for ten in ("MA trailing 13", "MA centered 13", "Savitzky–Golay 13", "Butterworth filtfilt", "Kalman smoother"):
        r = kn.kiem_nhan_qua(kn.bo_loc_mac_dinh(y[:200])[ten], y)
        kq[ten] = {"doi": round(r["doi_qua_khu"], 4), "moc_dau_tien": r["moc_dau_tien_bi_doi"], "n": len(y)}
    return kq


def hinh_gia_ro_ri(df: pd.DataFrame) -> pd.DataFrame:
    bang = kn.gia_cua_ro_ri(df["Appliances"])
    fig, ax = plt.subplots(figsize=(10, 4.2))
    mau = [M["xam"] if t == "không lọc" else (M["phu"] if v else M["chinh"])
           for t, v in zip(bang["feature"], bang["dùng tương lai?"], strict=True)]
    ax.bar(range(len(bang)), bang["MAE"], color=mau)
    for i, (mae, pct) in enumerate(zip(bang["MAE"], bang["so với không lọc (%)"], strict=True)):
        ax.text(i, mae + 0.4, f"{pct:+.1f}%".replace(".", ","), ha="center", fontsize=7)
    ax.set_xticks(range(len(bang)), [t.replace(" (", "\n(") for t in bang["feature"]], fontsize=6.5, rotation=20, ha="right")
    ax.set_ylabel("MAE dự báo 1 giờ tới (Wh)")
    ax.set_ylim(0, bang["MAE"].max() * 1.15)
    ax.set_title("Cái giá của rò rỉ: feature dùng tương lai (cam) cho MAE thấp hơn 24–28%, feature nhân quả (xanh) chỉ 1–6%")
    ve.luu_hinh(fig, HINH / "gia-ro-ri.png")
    return bang


def hinh_muc_tieu_lam_tron(df: pd.DataFrame) -> dict:
    y = df["Appliances"].astype(float)
    tron = pd.Series(kn.ma_giua(y.to_numpy()), index=y.index)
    doan = slice("2016-05-01", "2016-05-04")
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(y[doan].index, y[doan].to_numpy(), color=M["xam"], linewidth=0.9, label="mục tiêu thật (Wh)")
    ax.plot(tron[doan].index, tron[doan].to_numpy(), color=M["phu"], linewidth=1.8, label="mục tiêu đã làm trơn (MA centered 13)")
    ax.set_ylabel("Wh")
    ax.legend(fontsize=8)
    kq = kn.cham_tren_muc_tieu_lam_tron(y)
    ax.set_title(f"Chấm trên mục tiêu đã làm trơn: MAE {kq['mae_muc_tieu_lam_tron']:.1f} thay vì {kq['mae_muc_tieu_goc']:.1f} — "
                 "mô hình không đổi, chỉ thước đo dễ đi".replace(".", ","))
    ve.luu_hinh(fig, HINH / "muc-tieu-lam-tron.png")
    return {k: round(v, 2) for k, v in kq.items()}


if __name__ == "__main__":
    df = kn.doc_cam_bien()
    with ve.phong_cach():
        print("pho", hinh_pho(df))
        print("aliasing", hinh_aliasing())
        bang = hinh_bo_loc()
        print(bang.round(3).to_string(index=False))
        print("kiem nhan qua", hinh_kiem_nhan_qua())
        print(hinh_gia_ro_ri(df).round(2).to_string(index=False))
        print("muc tieu lam tron", hinh_muc_tieu_lam_tron(df))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
