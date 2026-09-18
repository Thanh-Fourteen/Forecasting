# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 2 → ../hinh/*.png (150 dpi)

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize, stats

from tv import ve

DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("xs", DAY / "xac_suat.py")
xs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xs)


def nb_lien_tuc(y: np.ndarray) -> tuple[float, float]:
    """MLE âm nhị thức với n liên tục (trung bình cố định = trung bình mẫu); trả (n, p) theo tham số scipy."""
    mu = y.mean()
    r = optimize.minimize_scalar(lambda ln: -stats.nbinom.logpmf(y, np.exp(ln), np.exp(ln) / (np.exp(ln) + mu)).sum(),
                                 bounds=(-5, 5), method="bounded")
    n = float(np.exp(r.x))
    return n, n / (n + mu)


def hinh_phan_phoi() -> None:
    y = xs.doc_luot_thue()["cnt"].to_numpy()
    mu, sd = y.mean(), y.std()
    n, p = nb_lien_tuc(y)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.8))
    a.hist(y, bins=np.arange(0, 1000, 20), density=True, color=ve.MAU["xam"], alpha=0.5, label="thực tế")
    k = np.arange(0, 1000)
    a.plot(k, stats.norm.pdf(k, mu, sd), color=ve.MAU["phu"], label="chuẩn")
    a.plot(k, stats.poisson.pmf(k, mu), color=ve.MAU["ba"], label="Poisson")
    a.plot(k, stats.nbinom.pmf(k, n, p), color=ve.MAU["chinh"], label="âm nhị thức")
    a.set_xlabel("lượt thuê / giờ")
    a.set_ylabel("mật độ")
    a.set_ylim(0, 0.006)
    a.set_title("Histogram và ba phân phối cùng trung bình")
    a.legend(fontsize=8)
    muc = (np.arange(1, 200) - 0.5) / 199
    thuc = np.quantile(y, muc)
    for ten, ppf, mau in (("chuẩn", stats.norm(mu, sd).ppf, ve.MAU["phu"]),
                          ("Poisson", stats.poisson(mu).ppf, ve.MAU["ba"]),
                          ("âm nhị thức", stats.nbinom(n, p).ppf, ve.MAU["chinh"])):
        b.plot(ppf(muc), thuc, ".", markersize=3, color=mau, label=ten)
    b.plot([-400, 1000], [-400, 1000], color="black", linewidth=0.8)
    b.set_xlim(-400, 1000)
    b.set_xlabel("quantile lý thuyết")
    b.set_ylabel("quantile thực tế")
    b.set_title("QQ-plot: điểm nằm trên đường chéo = khớp")
    b.legend(fontsize=8, markerscale=3)
    fig.suptitle("Lượt thuê theo giờ lệch phải và phân tán thừa: Poisson hỏng nặng, chuẩn sinh giá trị âm",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "phan-phoi-luot-thue.png")


def hinh_khoang() -> None:
    h = xs.doc_luot_thue()
    gio = h[h["hr"] == 17].set_index("ds")["cnt"]
    nam_2011 = gio[gio.index.year == 2011]
    lo_c, hi_c = nam_2011.mean() - 1.96 * nam_2011.std(), nam_2011.mean() + 1.96 * nam_2011.std()
    lo_q, hi_q = xs.khoang_du_bao(nam_2011)
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.plot(gio.index, gio.to_numpy(), ".", markersize=3, color=ve.MAU["xam"], label="lượt thuê lúc 17h mỗi ngày")
    ax.axhspan(lo_c, hi_c, xmax=1, color=ve.MAU["phu"], alpha=0.12, label=f"±1,96σ từ 2011: [{lo_c:.0f}; {hi_c:.0f}]")
    ax.axhline(lo_q, color=ve.MAU["chinh"], linestyle="--", linewidth=1)
    ax.axhline(hi_q, color=ve.MAU["chinh"], linestyle="--", linewidth=1, label=f"quantile 2,5–97,5% từ 2011: [{lo_q:.0f}; {hi_q:.0f}]")
    ax.axvline(np.datetime64("2012-01-01"), color="black", linewidth=0.8)
    ax.text(np.datetime64("2012-01-10"), 20, "2012: khoảng dựng từ 2011 được đem ra dùng", fontsize=8)
    ax.set_ylabel("lượt thuê / giờ")
    ax.set_title("Khoảng từ 2011 vỡ ở 2012 vì mức tăng — đổi sang quantile không cứu được")
    ax.legend(fontsize=8, loc="upper left")
    ve.luu_hinh(fig, HINH / "khoang-2011-2012.png")


def hinh_bootstrap() -> None:
    cac_l = [1, 3, 6, 10, 20, 40]
    phu = [xs.ty_le_phu_khoang_tin_cay(rho=0.7, n=200, so_lan_lap=300, seed=2026, do_dai_khoi=do_dai) for do_dai in cac_l]
    y = xs.doc_luot_thue().query("yr == 1")["cnt"].to_numpy()
    cac_l2 = [1, 6, 21, 48, 168, 336, 720]
    rong = []
    for do_dai in cac_l2:
        lo, hi = xs.khoang_tin_cay_trung_binh(y, seed=1, do_dai_khoi=do_dai)
        rong.append(hi - lo)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.4))
    a.plot(cac_l, phu, marker="o", color=ve.MAU["chinh"])
    a.axhline(0.95, color=ve.MAU["phu"], linestyle="--", linewidth=1, label="danh nghĩa 95%")
    for do_dai, v in zip(cac_l, phu, strict=True):
        a.text(do_dai, v + 0.012, f"{v:.0%}", ha="center", fontsize=8)
    a.set_xscale("log")
    a.set_xticks(cac_l, [str(k) for k in cac_l])
    a.set_ylim(0.5, 1.0)
    a.set_xlabel("độ dài khối (1 = i.i.d.)")
    a.set_ylabel("tỷ lệ khoảng chứa trung bình thật")
    a.set_title("Mô phỏng AR(1) ρ = 0,7, n = 200, 300 lần")
    a.legend(fontsize=8)
    b.plot(cac_l2, np.array(rong) / rong[0], marker="o", color=ve.MAU["chinh"])
    b.set_xscale("log")
    b.set_xticks(cac_l2, [str(k) for k in cac_l2])
    b.set_xlabel("độ dài khối (giờ)")
    b.set_ylabel("độ rộng / độ rộng i.i.d.")
    b.set_title("Lượt thuê theo giờ 2012: khoảng rộng mãi theo khối")
    fig.suptitle("Bootstrap i.i.d. cho khoảng tin cậy quá hẹp khi dữ liệu tự tương quan; độ dài khối là quyết định nhạy",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "bootstrap-do-dai-khoi.png")


def hinh_ham_mat_mat() -> None:
    y = xs.doc_luot_thue()["cnt"].to_numpy(float)
    c = np.arange(0, 701, 2.0)
    sai = y[None, :] - c[:, None]
    mat = {"bình phương": (sai**2).mean(axis=1),
           "tuyệt đối": np.abs(sai).mean(axis=1),
           "pinball τ = 0,9": np.where(sai >= 0, 0.9 * sai, -0.1 * sai).mean(axis=1)}
    fig, truc = plt.subplots(1, 3, figsize=(10, 3.2))
    for ax, (ten, v) in zip(truc, mat.items(), strict=True):
        tot = c[np.argmin(v)]
        ax.plot(c, v, color=ve.MAU["chinh"])
        ax.axvline(tot, color=ve.MAU["phu"], linestyle="--", linewidth=1)
        ax.text(tot + 12, v.min() + 0.55 * (v.max() - v.min()), f"tốt nhất ≈ {tot:.0f}", fontsize=8)
        ax.set_title(f"Sai số {ten}" if ten != "pinball τ = 0,9" else ten)
        ax.set_xlabel("dự báo hằng c")
    truc[0].set_ylabel("mất mát trung bình")
    fig.suptitle("Cùng dữ liệu, ba hàm mất mát chọn ba con số: trung bình 189, trung vị 142, quantile 0,9 ≈ 452",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ham-mat-mat.png")


def _khoang_gio(lich_su, cach: str):
    hang = []
    for g, nhom in lich_su.groupby("hr"):
        y = nhom["cnt"].to_numpy(float)
        if cach == "±1,96σ":
            lo, hi = y.mean() - 1.96 * y.std(ddof=1), y.mean() + 1.96 * y.std(ddof=1)
        elif cach == "quantile":
            lo, hi = xs.khoang_du_bao(y)
        else:
            z = np.log(y)
            lo, hi = np.exp(z.mean() - 1.96 * z.std(ddof=1)), np.exp(z.mean() + 1.96 * z.std(ddof=1))
        hang.append((g, lo, hi))
    return hang


def hinh_ty_le_phu() -> None:
    import pandas as pd

    h = xs.doc_luot_thue()
    thang = h["dteday"].dt.month
    nam2 = h["yr"] == 1
    kich_ban = {"2011 → 2011\n(trong mẫu)": (h[h["yr"] == 0], h[h["yr"] == 0]),
                "2011 → 2012": (h[h["yr"] == 0], h[nam2]),
                "2012 T1–6 → T7–12": (h[nam2 & (thang <= 6)], h[nam2 & (thang > 6)]),
                "2012 T5–8 → T9": (h[nam2 & thang.between(5, 8)], h[nam2 & (thang == 9)])}
    cach = ["±1,96σ", "quantile", "chuẩn trên log"]
    fig, truc = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    for ax, ten in zip(truc, cach, strict=True):
        duoi, tren = [], []
        for lich_su, moi in kich_ban.values():
            k = pd.DataFrame(_khoang_gio(lich_su, ten), columns=["hr", "lo", "hi"])
            m = moi.merge(k, on="hr")
            r = xs.ty_le_phu(m["cnt"], m["lo"], m["hi"])
            duoi.append(100 * r["duoi"])
            tren.append(100 * r["tren"])
        x = np.arange(len(kich_ban))
        ax.bar(x - 0.2, duoi, 0.4, color=ve.MAU["ba"], label="rơi dưới cận dưới")
        ax.bar(x + 0.2, tren, 0.4, color=ve.MAU["phu"], label="vượt cận trên")
        ax.axhline(2.5, color="black", linestyle="--", linewidth=0.8)
        for xi, v in zip(x + 0.2, tren, strict=True):
            ax.text(xi, v + 0.5, f"{v:.1f}".replace(".", ","), ha="center", fontsize=7)
        ax.set_xticks(x, list(kich_ban), fontsize=7, rotation=20)
        ax.set_title(ten)
    truc[0].set_ylabel("% giờ rơi ra ngoài (mục tiêu 2,5% mỗi đuôi)")
    truc[0].legend(fontsize=8)
    fig.suptitle("Khoảng 95% theo giờ: hỏng chủ yếu ở đuôi trên khi mức lượt thuê tăng",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ty-le-phu-kich-ban.png")


if __name__ == "__main__":
    with ve.phong_cach():
        hinh_phan_phoi()
        hinh_khoang()
        hinh_bootstrap()
        hinh_ham_mat_mat()
        hinh_ty_le_phu()
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
