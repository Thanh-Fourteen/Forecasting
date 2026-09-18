# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 9 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

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
spec = importlib.util.spec_from_file_location("dt", DAY / "dac_trung.py")
dt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dt)
M = ve.MAU


def hinh_khong_gian(bang: pd.DataFrame) -> dict:
    toa_do, pca = dt.khong_gian_dac_trung(bang)
    fig, truc = plt.subplots(1, 3, figsize=(11, 3.4))
    for ax, cot, ten in ((truc[0], "entropy_pho", "entropy phổ"), (truc[1], "do_manh_mua_vu", "độ mạnh mùa vụ"),
                         (truc[2], "smape_snaive", "sMAPE của seasonal naive (%)")):
        v = bang[cot].to_numpy(float)
        if cot == "smape_snaive":
            v = np.clip(v, 0, 40)
        h = ax.scatter(toa_do[:, 0], toa_do[:, 1], c=v, s=4, cmap="viridis", alpha=0.7)
        plt.colorbar(h, ax=ax, shrink=0.85)
        ax.set_title(ten, fontsize=9)
        ax.set_xlabel("PC1")
    truc[0].set_ylabel("PC2")
    fig.suptitle(f"Bản đồ 4.000 chuỗi M4 tháng (20 đặc trưng → PCA): vùng entropy cao cũng là vùng sMAPE cao "
                 f"(PC1 + PC2 giữ {pca.explained_variance_ratio_.sum():.0%} phương sai)",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "khong-gian-dac-trung.png")
    return {"pc1": round(float(pca.explained_variance_ratio_[0]), 3), "pc2": round(float(pca.explained_variance_ratio_[1]), 3),
            "dac_trung_manh_pc1": bang.columns[np.argsort(-np.abs(pca.components_[0]))[:3]].tolist()}


def hinh_entropy_sai_so(bang: pd.DataFrame) -> dict:
    nhom = pd.qcut(bang["entropy_pho"], 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
    tr = bang.groupby(nhom, observed=True)[["smape_snaive", "mase_snaive", "mase_naive1_snaive"]].median()
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.6))
    a.scatter(bang["entropy_pho"], np.clip(bang["smape_snaive"], 0, 60), s=4, alpha=0.3, color=M["chinh"])
    a.plot(bang.groupby(nhom, observed=True)["entropy_pho"].median(), tr["smape_snaive"], "o-", color=M["phu"],
           linewidth=2, label="trung vị theo nhóm ngũ phân vị")
    a.set_xlabel("entropy phổ")
    a.set_ylabel("sMAPE của seasonal naive (%)")
    a.legend(fontsize=8)
    a.set_title("sMAPE: Q1 5,4% → Q5 12,0%", fontsize=9)
    b.scatter(bang["entropy_pho"], np.clip(bang["mase_snaive"], 0, 3), s=4, alpha=0.3, color=M["xam"])
    b.plot(bang.groupby(nhom, observed=True)["entropy_pho"].median(), tr["mase_snaive"], "o-", color=M["phu"],
           linewidth=2)
    b.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
    b.set_xlabel("entropy phổ")
    b.set_ylabel("MASE của seasonal naive")
    b.set_title("MASE: nằm ngang quanh 1,0 ở mọi nhóm", fontsize=9)
    fig.suptitle("Cùng một dự báo, hai thước đo, hai kết luận: MASE chia cho sai số của CHÍNH seasonal naive",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "entropy-sai-so.png")
    return {"trung_vi_theo_nhom": tr.round(2).to_dict()}


def hinh_ba_thuoc_do(bang: pd.DataFrame) -> pd.DataFrame:
    tq = dt.tuong_quan_kho_de(bang)
    con = tq[tq["đặc trưng"] == "entropy_pho"]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    x = np.arange(len(con))
    ax.bar(x - 0.2, con["pearson"], 0.4, color=M["chinh"], label="Pearson")
    ax.bar(x + 0.2, con["spearman"], 0.4, color=M["phu"], label="Spearman")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x, ["sMAPE\n(không chuẩn hoá theo naive)", "MASE\n(chia cho naive MÙA VỤ)",
                      "MASE\n(chia cho naive 1 bước)"], fontsize=8)
    ax.set_ylabel("tương quan với entropy phổ")
    ax.legend(fontsize=8)
    ax.set_title("Đổi thước đo làm tương quan từ +0,22 thành ≈ 0 rồi thành −0,54 — dữ liệu không đổi")
    ve.luu_hinh(fig, HINH / "ba-thuoc-do.png")
    return tq


def hinh_phan_cum(chuoi: dict[str, np.ndarray]) -> dict:
    mau = {t: chuoi[t] for t in list(chuoi)[:300]}
    nhan_chuan, _ = dt.phan_cum_dtw(mau, so_cum=4, chuan_hoa=True)
    nhan_tho, _ = dt.phan_cum_dtw(mau, so_cum=4, chuan_hoa=False)
    fig, truc = plt.subplots(2, 4, figsize=(11, 5), sharex=True)
    for cot, cum in enumerate(sorted(nhan_chuan.unique())):
        ten = nhan_chuan[nhan_chuan == cum].index[:12]
        for t in ten:
            truc[0, cot].plot(dt.chuan_hoa_hinh_dang(mau[t]), color=M["chinh"], alpha=0.35, linewidth=0.7)
        truc[0, cot].set_title(f"cụm {cum} ({(nhan_chuan == cum).sum()} chuỗi)", fontsize=9)
    for cot, cum in enumerate(sorted(nhan_tho.unique())):
        ten = nhan_tho[nhan_tho == cum].index[:12]
        for t in ten:
            truc[1, cot].plot(mau[t], color=M["phu"], alpha=0.35, linewidth=0.7)
        truc[1, cot].set_title(f"cụm {cum} ({(nhan_tho == cum).sum()} chuỗi)", fontsize=9)
    truc[0, 0].set_ylabel("z-score\n(chuẩn hoá hình dạng)")
    truc[1, 0].set_ylabel("mức gốc\n(không chuẩn hoá)")
    fig.suptitle("Phân cụm DTW: chuẩn hoá thì cụm theo HÌNH DẠNG; không chuẩn hoá thì cụm chỉ theo ĐỘ LỚN",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "phan-cum-dtw.png")
    muc = pd.Series({t: np.mean(v) for t, v in mau.items()})
    return {"chuan_hoa_cum": nhan_chuan.value_counts().to_dict(),
            "tho_cum": nhan_tho.value_counts().to_dict(),
            "tho_muc_trung_binh_theo_cum": muc.groupby(nhan_tho).median().round(0).to_dict(),
            "chuan_muc_trung_binh_theo_cum": muc.groupby(nhan_chuan).median().round(0).to_dict()}


def hinh_abc_xyz(ban_le: pd.DataFrame) -> dict:
    bang = dt.abc_xyz(ban_le)
    dem = bang.groupby(["abc", "xyz"]).size().unstack(fill_value=0).reindex(index=["A", "B", "C"], columns=["X", "Y", "Z"])
    doanh_thu = bang.groupby(["abc", "xyz"])["sum"].sum().unstack(fill_value=0).reindex(index=["A", "B", "C"], columns=["X", "Y", "Z"])
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.4))
    for ax, du_lieu, ten, dinh_dang in ((a, dem, "số mặt hàng", "{:,.0f}"),
                                        (b, doanh_thu / doanh_thu.to_numpy().sum() * 100, "% doanh thu", "{:.1f}%")):
        anh = ax.imshow(du_lieu.to_numpy(), cmap="Blues")
        ax.set_xticks(range(3), du_lieu.columns)
        ax.set_yticks(range(3), du_lieu.index)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, dinh_dang.format(du_lieu.to_numpy()[i, j]), ha="center", va="center", fontsize=8)
        ax.set_title(ten, fontsize=9)
        plt.colorbar(anh, ax=ax, shrink=0.8)
    fig.suptitle("Phân tầng ABC–XYZ trên Online Retail II: A chiếm phần lớn doanh thu; XYZ chỉ đo biến động, "
                 "không đo độ khó dự báo", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "abc-xyz.png")
    return {"so_mat_hang": int(len(bang)), "dem": dem.to_dict(),
            "ty_le_doanh_thu_A": round(float(bang.loc[bang["abc"] == "A", "sum"].sum() / bang["sum"].sum()), 3),
            "cv_trung_vi": bang.groupby("abc")["cv"].median().round(2).to_dict()}


if __name__ == "__main__":
    chuoi = dt.lay_mau(dt.doc_tsf(), 4000)
    bang = dt.bang_dac_trung(chuoi).join(dt.danh_gia_kho_de(chuoi))
    with ve.phong_cach():
        print("khong gian", hinh_khong_gian(bang))
        print("entropy sai so", hinh_entropy_sai_so(bang))
        print(hinh_ba_thuoc_do(bang).round(3).to_string(index=False))
        print("phan cum", hinh_phan_cum(chuoi))
        print("abc xyz", hinh_abc_xyz(dt.doc_ban_le()))
    chien_luoc = dt.de_xuat_chien_luoc(bang)
    print("chiến lược:", chien_luoc.value_counts().to_dict(),
          "sMAPE trung vị:", {k: round(bang.loc[chien_luoc == k, "smape_snaive"].median(), 2)
                              for k in chien_luoc.unique()})
    print("chuỗi lạ:", {"kpss NaN (chuỗi hằng)": int(bang["kpss_p"].isna().sum()),
                        "doan_phang > 0,5": int((bang["doan_phang"] > 0.5).sum())})
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
