# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 20 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tv import ve
from tv.backtest import diebold_mariano

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("db", DAY / "da_bien.py")
db = importlib.util.module_from_spec(spec)
sys.modules["db"] = db
spec.loader.exec_module(db)
M = ve.MAU


def hinh_dau_xang(L) -> dict:
    eg = db.engle_granger(L)
    spread = L["xang"] - eg["hằng số"] - eg["hệ số"] * L["dau"]
    fig, a = plt.subplots(2, 1, figsize=(9, 5), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    a[0].plot(L.index, np.exp(L["dau"]), color=M["chinh"], label="dầu WTI (USD/gallon)")
    a[0].plot(L.index, np.exp(L["xang"]), color=M["phu"], label="xăng NY Harbor (USD/gallon)")
    a[0].set_ylabel("USD/gallon")
    a[0].legend(fontsize=8)
    a[1].plot(L.index, spread, color=M["ba"])
    a[1].axhline(0, color="black", linewidth=0.6)
    a[1].set_ylabel("spread (log)")
    fig.suptitle("Dầu và xăng cùng trôi, nhưng khoảng cách giữa chúng (spread) cứ quay về 0", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "dau-xang.png")
    return {**eg, "spread độ lệch chuẩn": float(spread.std()), "số tuần": len(L)}


def bang_dau_xang(L) -> dict:
    kq = db.backtest_dau_xang(L)
    mae = kq.groupby("buoc_h")[["naive", "VAR", "VECM"]].apply(
        lambda d: (d.sub(kq.loc[d.index, "y"], axis=0)).abs().mean() * 100)
    h4 = kq[kq["buoc_h"] == 4]
    dm = {m: diebold_mariano((h4["y"] - h4[m]).to_numpy(), (h4["y"] - h4["naive"]).to_numpy(), h=4,
                             ham_mat_mat="tuyet_doi").p_value for m in ("VAR", "VECM")}
    return {"MAE %": mae.round(2).to_dict(), "DM p h=4 so naive": dm, "số cutoff": kq["cutoff"].nunique()}


def hinh_kalman() -> dict:
    y = db.doc_nile()
    ref = db.local_level_statsmodels(y)
    s2_nhieu, s2_muc = ref.params
    thieu = y.copy()
    thieu[40:60] = np.nan
    kq = db.kalman_local_level(thieu, s2_nhieu, s2_muc)
    nam = np.arange(1871, 1971)
    sd = np.sqrt(kq["phương sai"])
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(nam, thieu, color=M["xam"], marker=".", linewidth=0.6, label="số đo (bỏ 1911–1930 để thử dữ liệu thiếu)")
    ax.plot(nam, kq["mức"], color=M["chinh"], label="mức Kalman lọc được")
    ax.fill_between(nam, kq["mức"] - 1.96 * sd, kq["mức"] + 1.96 * sd, color=M["chinh"], alpha=0.2, label="± 1,96 độ lệch chuẩn")
    ax.axvspan(1911, 1930, color=M["vang"], alpha=0.15)
    ax.set_xlabel("năm")
    ax.set_ylabel("lưu lượng (10⁸ m³/năm)")
    ax.legend(fontsize=8)
    ax.set_title("Kalman trên sông Nile: thiếu số đo thì mức giữ nguyên còn dải bất định nở ra", fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "kalman-nile.png")
    kq_du = db.kalman_local_level(y, s2_nhieu, s2_muc)
    return {"σ² nhiễu": float(s2_nhieu), "σ² mức": float(s2_muc), "lệch tối đa so statsmodels":
            float(np.max(np.abs(kq_du["mức"] - ref.filtered_state[0]))), "sd năm 1910": float(sd[39]), "sd năm 1930": float(sd[59]),
            "mức 1871–1873": kq_du["mức"][:3].round(1).tolist()}


def hinh_vintage(du_lieu) -> dict:
    qs = pd.period_range("2005Q1", "2019Q4", freq="Q")
    dau = [db.gdp_lan_dau(du_lieu, q) for q in qs]
    cuoi = db.tang_truong_quy(db.gdp_theo_vintage(du_lieu, db.VINTAGE_CUOI)).loc[qs].to_numpy()
    q08 = pd.Period("2008Q4")
    duong = []
    for nam in range(2009, 2026):
        for thang in (2, 5, 8, 11):
            v = db.ten_vintage(nam, thang)
            G = db.gdp_theo_vintage(du_lieu, v)
            duong.append((pd.Timestamp(nam, thang, 15), float(db.tang_truong_quy(G).loc[q08])))
    fig, a = plt.subplots(1, 2, figsize=(11, 3.8))
    a[0].plot([d for d, _ in duong], [x for _, x in duong], color=M["chinh"], marker=".")
    a[0].set_ylabel("tăng trưởng GDP quý 4/2008 (% năm hoá)")
    a[0].set_xlabel("vintage (thời điểm đọc số liệu)")
    a[0].set_title("cùng một quý, mỗi lần công bố một con số", fontsize=9)
    a[1].scatter(dau, cuoi, s=12, color=M["phu"])
    lim = [min(dau + list(cuoi)) - 1, max(dau + list(cuoi)) + 1]
    a[1].plot(lim, lim, color="black", linewidth=0.6)
    a[1].set_xlabel("lần công bố đầu (%)")
    a[1].set_ylabel("bản 12/2025 (%)")
    a[1].set_title("60 quý 2005–2019: sửa lên, sửa xuống", fontsize=9)
    fig.suptitle("GDP bị sửa nhiều lần sau khi công bố: dùng bản đã sửa để chấm quá khứ là nhìn trộm", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "vintage.png")
    d = np.array(dau) - cuoi
    return {"2008Q4 lần đầu": duong[0][1], "2008Q4 bản cuối": duong[-1][1], "2008Q4 thấp nhất": min(x for _, x in duong),
            "RMS sửa (điểm %)": float(np.sqrt(np.mean(d ** 2))), "sửa lớn nhất": float(np.max(np.abs(d)))}


def hinh_nowcast(du_lieu) -> dict:
    qs = pd.period_range("2005Q1", "2019Q4", freq="Q")
    bang = db.danh_gia_nowcast(du_lieu, qs, dfm=True)
    r = db.rmse_theo_k(bang)
    tach = {ten: db.rmse_theo_k(bang[bang["quý"].str[:4].astype(int).between(a, b)]).round(2).to_dict()
            for ten, (a, b) in {"2005–2009": (2005, 2009), "2010–2019": (2010, 2019)}.items()}
    ro_ri = []
    for q in qs:
        n = db.nowcast(du_lieu, q, 1)
        v = db.vintage_cua
        db.vintage_cua = lambda q, k: db.VINTAGE_CUOI
        m = db.nowcast(du_lieu, q, 1)
        db.vintage_cua = v
        ro_ri.append((db.gdp_lan_dau(du_lieu, q), n["bridge"], m["bridge"]))
    ro_ri = np.array(ro_ri)
    fig, ax = plt.subplots(figsize=(8, 4))
    k = r.index.to_numpy()
    for c, mau in (("bridge", M["chinh"]), ("DFM", M["ba"]), ("naive", M["xam"]), ("trung bình", M["phu"])):
        ax.plot(k, r[c], marker="o", color=mau, label=c)
    ax.axhline(float(np.sqrt(np.mean((ro_ri[:, 0] - ro_ri[:, 2]) ** 2))), color=M["bon"], linestyle="--",
               label="bridge dùng số đã sửa (rò rỉ)")
    ax.set_xticks(k)
    ax.set_xticklabels(["tháng 1\n(0 tháng số liệu)", "tháng 2\n(1 tháng)", "tháng 3\n(2 tháng)", "tháng đầu quý sau\n(đủ 3 tháng)"])
    ax.set_ylabel("RMSE (điểm % năm hoá)")
    ax.legend(fontsize=8)
    ax.set_title("Nowcast GDP 2005–2019 bằng vintage thật: sai số giảm khi có thêm tháng số liệu", fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "nowcast.png")
    return {"RMSE": r.round(2).to_dict(), "tách": tach,
            "rò rỉ k=1": float(np.sqrt(np.mean((ro_ri[:, 0] - ro_ri[:, 2]) ** 2))),
            "thật k=1": float(np.sqrt(np.mean((ro_ri[:, 0] - ro_ri[:, 1]) ** 2)))}


if __name__ == "__main__":
    L = db.doc_dau_xang()
    print("dầu–xăng:", hinh_dau_xang(L))
    print("kiểm dừng:\n", db.kiem_dung(L).round(3).to_string(index=False))
    print("Johansen:", db.hang_dong_lien_ket(L))
    print("backtest dầu–xăng:", bang_dau_xang(L))
    print("Kalman:", hinh_kalman())
    du_lieu = db.doc_tat_ca()
    print("vintage:", hinh_vintage(du_lieu))
    print("nowcast:", hinh_nowcast(du_lieu))
