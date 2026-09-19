# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 5 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from tv import ve

DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("bd", DAY / "bien_doi.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)
M = ve.MAU


def hinh_lich(y: pd.Series) -> dict:
    nam = y["2023"]
    ngay = bd.theo_ngay(nam)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.4))
    thang = [f"T{t}" for t in nam.index.month]
    a.plot(thang, nam.to_numpy() / 1000, marker="o", color=M["chinh"])
    a.set_ylim(550, 800)
    a.set_ylabel("tỷ USD / tháng")
    a.set_title("Tổng tháng 2023: T2 thấp hơn T1 3,4%", fontsize=10)
    b.plot(thang, ngay.to_numpy(), marker="o", color=M["phu"])
    b.set_ylim(19000, 25000)
    b.set_ylabel("triệu USD / ngày")
    b.set_title("Chia số ngày: T2 CAO hơn T1 7,0%", fontsize=10)
    for ax in (a, b):
        ax.tick_params(axis="x", labelsize=7)
        ax.text(0.01, 0.02, "biểu đồ điểm, trục không bắt đầu từ 0", transform=ax.transAxes, fontsize=7, color=M["xam"])
    fig.suptitle("Doanh số bán lẻ Mỹ 2023 (chưa điều chỉnh mùa vụ) — một phần 'mùa vụ' tháng 2 chỉ là 28 ngày",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "dieu-chinh-lich.png")
    return {"T1": float(nam.iloc[0]), "T2": float(nam.iloc[1]), "T3": float(nam.iloc[2]),
            "ngay_T1": round(float(ngay.iloc[0])), "ngay_T2": round(float(ngay.iloc[1])), "ngay_T3": round(float(ngay.iloc[2])),
            "T2_T1_tho": round(float(nam.iloc[1] / nam.iloc[0] - 1), 4), "T2_T1_ngay": round(float(ngay.iloc[1] / ngay.iloc[0] - 1), 4)}


def hinh_thuc(y: pd.Series, cpi: pd.Series, dan_so: pd.Series) -> dict:
    nam = y.resample("YS").sum()["1993":"2025"]
    thuc = bd.gia_thuc(y, cpi, 2025).resample("YS").sum()["1993":"2025"]
    dau_nguoi = (bd.gia_thuc(y, cpi, 2025) / dan_so.reindex(y.index) * 1e6).resample("YS").sum()["1993":"2025"]
    fig, ax = plt.subplots(figsize=(10, 3.8))
    for s, ten, c in ((nam, "danh nghĩa", M["chinh"]), (thuc, "giá thực (USD 2025)", M["phu"]),
                      (dau_nguoi, "giá thực trên đầu người", M["ba"])):
        chi_so = s / s.iloc[0] * 100
        ax.plot(chi_so.index.year, chi_so.to_numpy(), marker="o", markersize=3, color=c, label=f"{ten}: {chi_so.iloc[-1]:.0f}")
    ax.axhline(100, color="black", linewidth=0.5)
    ax.set_ylabel("chỉ số, 1993 = 100")
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=8)
    ax.set_title("Doanh số bán lẻ Mỹ 1993–2025: 'tăng gấp 4' danh nghĩa chỉ còn +42% khi trừ lạm phát và chia dân số")
    ve.luu_hinh(fig, HINH / "danh-nghia-thuc.png")
    cpi_nam = cpi.resample("YS").mean()
    ds_nam = dan_so.resample("YS").mean()
    return {"nam_1993": float(nam.iloc[0]), "nam_2025": float(nam.iloc[-1]), "thuc_1993": round(float(thuc.iloc[0])),
            "tang_danh_nghia": round(float(nam.iloc[-1] / nam.iloc[0] - 1), 3), "tang_thuc": round(float(thuc.iloc[-1] / thuc.iloc[0] - 1), 3),
            "tang_dau_nguoi": round(float(dau_nguoi.iloc[-1] / dau_nguoi.iloc[0] - 1), 3),
            "cpi_1993": round(float(cpi_nam["1993"].iloc[0]), 1), "cpi_2025": round(float(cpi_nam["2025"].iloc[0]), 2),
            "dan_so_1993": round(float(ds_nam["1993"].iloc[0])), "dan_so_2025": round(float(ds_nam["2025"].iloc[0])),
            "dau_nguoi_1993": round(float(dau_nguoi.iloc[0])), "dau_nguoi_2025": round(float(dau_nguoi.iloc[-1]))}


def hinh_dao_dong(y: pd.Series) -> dict:
    y = y[:"2019-12"]
    khoi = y.to_numpy()[y.size % 12:].reshape(-1, 12) / 1000
    tb, sd = khoi.mean(axis=1), khoi.std(axis=1, ddof=1)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.plot(tb, sd, "o", color=M["chinh"], markersize=4)
    for i, nam in ((0, 1992), (len(tb) - 1, 2019), (16, 2008)):
        ax.annotate(str(nam), (tb[i], sd[i]), xytext=(5, -10), textcoords="offset points", fontsize=8)
    ax.set_xlim(0, 550)
    ax.set_ylim(0, 45)
    ax.set_xlabel("trung bình tháng trong năm (tỷ USD)")
    ax.set_ylabel("độ lệch chuẩn trong năm (tỷ USD)")
    ax.set_title(f"Năm bán nhiều thì dao động trong năm cũng lớn: {sd[0]:.1f} → {sd[-1]:.1f} tỷ USD".replace(".", ","), fontsize=10)
    ve.luu_hinh(fig, HINH / "dao-dong-theo-muc.png")
    return {"tb_1992": round(float(tb[0]), 1), "tb_2019": round(float(tb[-1]), 1), "sd_1992": round(float(sd[0]), 1),
            "sd_2019": round(float(sd[-1]), 1), "sd_2008": round(float(sd[16]), 1)}


def hinh_box_cox(y: pd.Series) -> dict:
    y = y[:"2019-12"]
    luoi = np.linspace(-1, 2, 601)
    khoi = y.to_numpy()[y.size % 12:].reshape(-1, 12)
    tb, sd = khoi.mean(axis=1), khoi.std(axis=1, ddof=1)
    ty_so = sd[None, :] / tb[None, :] ** (1 - luoi[:, None])
    cv = ty_so.std(axis=1, ddof=1) / ty_so.mean(axis=1)
    lam_g = bd.guerrero(y, 12)
    _, lam_mle = stats.boxcox(y.to_numpy())
    fig, truc = plt.subplots(1, 2, figsize=(10, 3.4))
    truc[0].plot(luoi, cv, color=M["chinh"])
    truc[0].axvline(lam_g, color=M["phu"], linestyle="--")
    truc[0].axvline(lam_mle, color=M["ba"], linestyle=":")
    truc[0].text(lam_g - 0.95, cv.max() * 0.9, f"Guerrero λ = {lam_g:.3f}", color=M["phu"], fontsize=8)
    truc[0].text(lam_mle + 0.05, cv.max() * 0.75, f"scipy (MLE) λ = {lam_mle:.3f}", color=M["ba"], fontsize=8)
    truc[0].set_xlabel("λ")
    truc[0].set_ylabel("CV của các tỷ số s / μ^(1 − λ)")
    truc[0].set_ylim(bottom=0)
    truc[0].set_title("Tiêu chí Guerrero: đáy ở λ ≈ 0,34", fontsize=9)
    for lam, c, ten in ((1.0, M["xam"], "λ = 1 (không biến đổi)"), (lam_g, M["phu"], f"λ = {lam_g:.2f} (Guerrero)"),
                        (0.0, M["chinh"], "λ = 0 (log)")):
        w = pd.Series(bd.boxcox(y, lam), index=y.index)
        kh = w.to_numpy()[w.size % 12:].reshape(-1, 12)
        truc[1].plot(range(1992, 2020), kh.std(axis=1, ddof=1) / kh.std(axis=1, ddof=1)[0], color=c, label=ten)
    truc[1].axhline(1, color="black", linewidth=0.5)
    truc[1].set_ylim(bottom=0)
    truc[1].set_xlabel("năm")
    truc[1].set_ylabel("độ lệch chuẩn trong năm / của 1992")
    truc[1].set_title("Sau biến đổi: log làm quá tay, λ = 0,34 giữ dao động gần đều", fontsize=9)
    truc[1].legend(fontsize=7, loc="lower left")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "box-cox.png")
    sd_chuan = {}
    for lam in (1.0, lam_g, 0.0):
        w = bd.boxcox(y.to_numpy(), lam)
        kh = w[w.size % 12:].reshape(-1, 12).std(axis=1, ddof=1)
        sd_chuan[round(lam, 3)] = round(float(kh[-1] / kh[0]), 2)
    return {"lam_guerrero": lam_g, "lam_mle": round(float(lam_mle), 3), "sd_2019_chia_1992": sd_chuan}


def hinh_bias_log_normal() -> dict:
    rng = np.random.default_rng(42)
    mu, s = 5.0, 0.5
    x = rng.lognormal(mu, s, 100_000)
    w = np.log(x)
    tv_ = float(bd.boxcox_nguoc(w.mean(), 0.0))
    tb_fpp = float(bd.boxcox_nguoc(w.mean(), 0.0, w.var(ddof=1)))
    fig, ax = plt.subplots(figsize=(9, 3.3))
    ax.hist(x, bins=np.arange(0, 500, 5), color=M["xam"], alpha=0.6)
    ax.set_ylabel("số mẫu mỗi ô rộng 5")
    for v, c, ten in ((x.mean(), "black", f"trung bình mẫu {x.mean():.1f}"), (tv_, M["phu"], f"exp(trung bình log) {tv_:.1f}"),
                      (tb_fpp, M["chinh"], f"có hiệu chỉnh FPP {tb_fpp:.1f}")):
        ax.axvline(v, color=c, linewidth=1.5, label=ten)
    ax.legend(fontsize=8)
    ax.set_xlabel("giá trị y = exp(w), w có phân phối chuẩn")
    ax.set_title("Log-normal μ = 5, σ = 0,5 (100.000 mẫu): đổi ngược thẳng cho trung vị, thấp hơn trung bình 11,9%")
    ve.luu_hinh(fig, HINH / "bias-log-normal.png")
    rows = []
    for sig in (0.1, 0.3, 0.5, 1.0):
        rows.append((sig, round(-(1 - np.exp(-sig**2 / 2)) * 100, 2), round((np.exp(mu) * (1 + sig**2 / 2) / np.exp(mu + sig**2 / 2) - 1) * 100, 2)))
    return {"trung_binh": round(float(x.mean()), 2), "trung_vi": round(tv_, 2), "fpp": round(tb_fpp, 2),
            "chinh_xac": round(float(np.exp(mu + s**2 / 2)), 2), "bang_sigma": rows}


def hinh_bias_that() -> dict:
    ket_qua = {}
    ten_viet = {bd.TONG: "Tổng bán lẻ + ăn uống", "Gasoline stations": "Trạm xăng", "Department stores": "Bách hoá",
                "Gift, novelty, and souvenir stores": "Quà tặng, lưu niệm"}
    for ten in ten_viet:
        y = bd.doc_ban_le(ten)
        kq = bd.danh_gia_bias(y)
        s2 = [bd.du_bao_log(y, goc)["sigma2"].iloc[0] for goc in pd.date_range("2012-01-01", "2018-12-01", freq="MS")]
        ket_qua[ten_viet[ten]] = {**{k: round(v, 2) for k, v in kq.items()}, "sigma2_tb": round(float(np.mean(s2)), 5),
                                  "sigma": round(float(np.sqrt(np.mean(s2))), 3)}
    fig, ax = plt.subplots(figsize=(9, 3.3))
    x = np.arange(len(ket_qua))
    ax.bar(x - 0.2, [v["trung_vi"] for v in ket_qua.values()], 0.4, color=M["phu"], label="đổi ngược thẳng (trung vị)")
    ax.bar(x + 0.2, [v["trung_binh"] for v in ket_qua.values()], 0.4, color=M["chinh"], label="có hiệu chỉnh bias (trung bình)")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xticks(x, [f"{k}\nσ = {v['sigma']:.3f}" for k, v in ket_qua.items()], fontsize=8)
    ax.set_ylabel("tổng dự báo / tổng thực − 1 (%)")
    ax.legend(fontsize=8)
    ax.set_title("Gốc mỗi tháng 2012–2018, tầm 12: hiệu chỉnh luôn đẩy lên ≈ σ²/2 — nhỏ so với sai lệch do xu hướng")
    ve.luu_hinh(fig, HINH / "bias-kiem-tra.png")
    return ket_qua


if __name__ == "__main__":
    y = bd.doc_ban_le()
    cpi, dan_so = bd.doc_cpi(), bd.doc_dan_so()
    with ve.phong_cach():
        print("lich", hinh_lich(y))
        print("thuc", hinh_thuc(y, cpi, dan_so))
        print("dao dong", hinh_dao_dong(y))
        print("boxcox", hinh_box_cox(y))
        print("lognormal", hinh_bias_log_normal())
        print("bias that", hinh_bias_that())
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
