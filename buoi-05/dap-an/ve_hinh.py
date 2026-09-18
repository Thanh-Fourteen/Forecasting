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


def hinh_box_cox(y: pd.Series) -> dict:
    y = y[:"2019-12"]
    luoi = np.linspace(-1, 2, 601)
    khoi = y.to_numpy()[y.size % 12:].reshape(-1, 12)
    tb, sd = khoi.mean(axis=1), khoi.std(axis=1, ddof=1)
    ty_so = sd[None, :] / tb[None, :] ** (1 - luoi[:, None])
    cv = ty_so.std(axis=1, ddof=1) / ty_so.mean(axis=1)
    lam_g = bd.guerrero(y, 12)
    _, lam_mle = stats.boxcox(y.to_numpy())
    fig, truc = plt.subplots(1, 3, figsize=(10.5, 3.3))
    truc[0].loglog(tb / 1000, sd / 1000, "o", color=M["chinh"], markersize=4)
    doc = np.polyfit(np.log(tb), np.log(sd), 1)[0]
    truc[0].set_xlabel("trung bình năm (tỷ USD)")
    truc[0].set_ylabel("độ lệch chuẩn trong năm")
    truc[0].set_title(f"log sd theo log mức: độ dốc {doc:.2f}", fontsize=9)
    truc[1].plot(luoi, cv, color=M["chinh"])
    truc[1].axvline(lam_g, color=M["phu"], linestyle="--")
    truc[1].axvline(lam_mle, color=M["ba"], linestyle=":")
    truc[1].text(lam_g + 0.05, cv.max() * 0.9, f"Guerrero {lam_g:.3f}", color=M["phu"], fontsize=8)
    truc[1].text(lam_mle + 0.05, cv.max() * 0.75, f"MLE {lam_mle:.3f}", color=M["ba"], fontsize=8)
    truc[1].set_xlabel("λ")
    truc[1].set_ylabel("hệ số biến thiên của s/μ^(1−λ)")
    truc[1].set_title("Guerrero chọn λ làm tỷ số ổn định nhất", fontsize=9)
    for lam, c, ten in ((1.0, M["xam"], "λ = 1 (gốc)"), (lam_g, M["phu"], f"λ = {lam_g:.2f}"), (0.0, M["chinh"], "λ = 0 (log)")):
        w = pd.Series(bd.boxcox(y, lam), index=y.index)
        kh = w.to_numpy()[w.size % 12:].reshape(-1, 12)
        truc[2].plot(range(1992, 2020), kh.std(axis=1, ddof=1) / kh.std(axis=1, ddof=1)[0], color=c, label=ten)
    truc[2].set_title("sd trong năm (chuẩn hoá về 1992)", fontsize=9)
    truc[2].legend(fontsize=7)
    fig.suptitle("Bán lẻ 1992–2019: biến động tăng chậm hơn mức (độ dốc < 1) → log làm quá tay, λ Guerrero ≈ 0,34",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "box-cox.png")
    sd_chuan = {}
    for lam in (1.0, lam_g, 0.0):
        w = bd.boxcox(y.to_numpy(), lam)
        kh = w[w.size % 12:].reshape(-1, 12).std(axis=1, ddof=1)
        sd_chuan[round(lam, 3)] = round(float(kh[-1] / kh[0]), 2)
    return {"lam_guerrero": lam_g, "lam_mle": round(float(lam_mle), 3), "doc_log_sd": round(float(doc), 3), "sd_2019_chia_1993": sd_chuan}


def hinh_bias_log_normal() -> dict:
    rng = np.random.default_rng(42)
    mu, s = 5.0, 0.5
    x = rng.lognormal(mu, s, 100_000)
    w = np.log(x)
    tv_ = float(bd.boxcox_nguoc(w.mean(), 0.0))
    tb_fpp = float(bd.boxcox_nguoc(w.mean(), 0.0, w.var(ddof=1)))
    fig, ax = plt.subplots(figsize=(9, 3.3))
    ax.hist(x, bins=np.arange(0, 500, 5), density=True, color=M["xam"], alpha=0.6)
    for v, c, ten in ((x.mean(), "black", f"trung bình mẫu {x.mean():.1f}"), (tv_, M["phu"], f"exp(trung bình log) {tv_:.1f}"),
                      (tb_fpp, M["chinh"], f"có hiệu chỉnh FPP {tb_fpp:.1f}")):
        ax.axvline(v, color=c, linewidth=1.5, label=ten)
    ax.legend(fontsize=8)
    ax.set_xlabel("y")
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


def hinh_sai_phan(y: pd.Series) -> dict:
    w = np.log(y)
    sp_mua = (w - w.shift(12)) * 100
    sp_ca_hai = sp_mua - sp_mua.shift(1)
    fig, truc = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    truc[0].plot(w.index, w.to_numpy(), color=M["chinh"])
    truc[0].set_title("log doanh số: xu hướng + mùa vụ", fontsize=9, loc="left")
    truc[1].plot(sp_mua.index, sp_mua.to_numpy(), color=M["phu"])
    truc[1].axhline(0, color="black", linewidth=0.5)
    truc[1].set_title("sai phân mùa vụ log (≈ % tăng so với cùng tháng năm trước): hết mùa vụ, còn chu kỳ kinh tế và COVID", fontsize=9, loc="left")
    truc[2].plot(sp_ca_hai.index, sp_ca_hai.to_numpy(), color=M["ba"], linewidth=0.8)
    truc[2].axhline(0, color="black", linewidth=0.5)
    truc[2].set_title("thêm sai phân thường: dao động quanh 0", fontsize=9, loc="left")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "sai-phan.png")
    return {"yoy_2009_min": round(float(sp_mua["2009"].min()), 1), "yoy_2020_04": round(float(sp_mua[pd.Timestamp("2020-04-01")]), 1),
            "yoy_2021_04": round(float(sp_mua[pd.Timestamp("2021-04-01")]), 1), "yoy_tb_2012_2019": round(float(sp_mua["2012":"2019"].mean()), 2)}


def hinh_chuan_hoa() -> dict:
    nam = "2024"
    gas = bd.doc_ban_le("Gasoline stations")[nam]
    sach = bd.doc_ban_le("Book stores")[nam]
    fig, truc = plt.subplots(1, 3, figsize=(10.5, 3.2))
    thang = range(1, 13)
    for ax, ham, ten in ((truc[0], lambda v: v / 1000, "gốc (tỷ USD/tháng)"),
                         (truc[1], lambda v: (v - v.mean()) / v.std(ddof=1), "z-score"),
                         (truc[2], lambda v: v / v.mean(), "chia trung bình")):
        for s_, c, nhan in ((gas, M["chinh"], "trạm xăng"), (sach, M["phu"], "nhà sách")):
            ax.plot(thang, ham(s_).to_numpy(), marker="o", markersize=3, color=c, label=nhan)
        ax.set_title(ten, fontsize=9)
        ax.set_xticks(range(1, 13, 2))
        ax.set_xlabel("tháng 2024")
    truc[0].set_yscale("log")
    truc[2].axhline(1, color="black", linewidth=0.5)
    truc[0].legend(fontsize=7)
    fig.suptitle("Hai chuỗi lệch nhau 80 lần: z-score xoá mất độ lớn dao động tương đối, chia trung bình giữ lại",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "chuan-hoa.png")
    return {"gas_tb": round(float(gas.mean())), "sach_tb": round(float(sach.mean())),
            "gas_chia": (round(float((gas / gas.mean()).min()), 3), round(float((gas / gas.mean()).max()), 3)),
            "sach_chia": (round(float((sach / sach.mean()).min()), 3), round(float((sach / sach.mean()).max()), 3)),
            "gas_z": (round(float(((gas - gas.mean()) / gas.std(ddof=1)).min()), 2), round(float(((gas - gas.mean()) / gas.std(ddof=1)).max()), 2)),
            "sach_z": (round(float(((sach - sach.mean()) / sach.std(ddof=1)).min()), 2), round(float(((sach - sach.mean()) / sach.std(ddof=1)).max()), 2))}


if __name__ == "__main__":
    y = bd.doc_ban_le()
    cpi, dan_so = bd.doc_cpi(), bd.doc_dan_so()
    with ve.phong_cach():
        print("lich", hinh_lich(y))
        print("thuc", hinh_thuc(y, cpi, dan_so))
        print("boxcox", hinh_box_cox(y))
        print("lognormal", hinh_bias_log_normal())
        print("bias that", hinh_bias_that())
        print("sai phan", hinh_sai_phan(y))
        print("chuan hoa", hinh_chuan_hoa())
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
