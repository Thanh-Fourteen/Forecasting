# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 21 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import matplotlib
import matplotlib.dates

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("tc", DAY / "tai_chinh.py")
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)
M = ve.MAU


def _acf(x, k):
    x = np.asarray(x, float) - np.mean(x)
    return np.array([np.sum(x[j:] * x[:-j]) / np.sum(x * x) for j in range(1, k + 1)])


def hinh_su_that(jpy) -> dict:
    fig, a = plt.subplots(1, 3, figsize=(12, 3.6))
    a[0].plot(jpy.index, jpy, color=M["chinh"], linewidth=0.4)
    a[0].set_title("lợi suất ngày JPY/USD (%)", fontsize=9)
    z = (jpy - jpy.mean()) / jpy.std()
    b = np.linspace(-8, 8, 65)
    a[1].hist(z, bins=b, density=True, color=M["xam"], label="thực tế")
    a[1].plot(b, stats.norm.pdf(b), color=M["phu"], label="phân phối chuẩn")
    a[1].set_yscale("log")
    a[1].set_ylim(1e-5, 1)
    a[1].set_xlabel("lợi suất chuẩn hoá (số độ lệch chuẩn)")
    a[1].legend(fontsize=7)
    a[1].set_title("đuôi dày (trục dọc thang log)", fontsize=9)
    k = np.arange(1, 21)
    a[2].bar(k - 0.2, _acf(jpy, 20), width=0.4, color=M["chinh"], label="lợi suất")
    a[2].bar(k + 0.2, _acf(jpy ** 2, 20), width=0.4, color=M["phu"], label="bình phương lợi suất")
    a[2].axhline(1.96 / np.sqrt(len(jpy)), color="black", linestyle="--", linewidth=0.7)
    a[2].axhline(-1.96 / np.sqrt(len(jpy)), color="black", linestyle="--", linewidth=0.7)
    a[2].set_xlabel("trễ (ngày)")
    a[2].legend(fontsize=7)
    a[2].set_title("ACF", fontsize=9)
    fig.suptitle("JPY/USD 2000–2024: lợi suất gần như không đoán được, nhưng biến động thì đi thành cụm", fontsize=10,
                 fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "su-that.png")
    return {"ACF bình phương trễ 1..5": _acf(jpy ** 2, 5).round(3).tolist(), "ACF lợi suất trễ 1..5": _acf(jpy, 5).round(3).tolist()}


def hinh_demo(gia) -> dict:
    kq = tc.du_bao_gia(gia)
    dg = tc.danh_gia_gia(kq)
    import importlib.util as iu
    sp = iu.spec_from_file_location("tc_code", DAY.parent / "code" / "tai_chinh.py")
    tcc = iu.module_from_spec(sp)
    sp.loader.exec_module(tcc)
    demo = tcc.du_bao_gia(gia)
    from sklearn.metrics import r2_score
    dg_demo = {"R² MLP": r2_score(demo["y"], demo["MLP"]), "R² naive": r2_score(demo["y"], demo["naive"]),
               "MAE MLP": float((demo["y"] - demo["MLP"]).abs().mean()), "MAE naive": float((demo["y"] - demo["naive"]).abs().mean())}
    doan = kq.loc["2024-02-15":"2024-04-15"]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(doan.index, doan["y"] / 1000, color="black", label="giá thật")
    ax.plot(doan.index, doan["MLP"] / 1000, color=M["chinh"], label="MLP dự báo")
    ax.plot(doan.index, doan["naive"] / 1000, color=M["phu"], linestyle="--", label="giá hôm qua (naive)")
    ax.set_ylabel("nghìn USD")
    ax.legend(fontsize=8)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d/%m"))
    ax.set_title("Dự báo 'bám sát' giá thật chỉ vì nó gần như là giá hôm qua, trễ đúng một ngày", fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "demo-gia.png")
    return {"trung thực": dg, "demo": dg_demo, "số ngày chấm": len(kq),
            "tương quan (dự báo − naive) với (thật − naive)": float(np.corrcoef(kq["MLP"] - kq["naive"], kq["y"] - kq["naive"])[0, 1])}


def hinh_var(jpy) -> dict:
    var_g = tc.var_99(jpy)
    hoc = jpy[jpy.index < pd.Timestamp(tc.MOC_JPY)]
    var_c = pd.Series(hoc.mean() + stats.norm.ppf(0.01) * hoc.std(), index=var_g.index)
    r = jpy.loc[var_g.index]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(r.index, r, color=M["xam"], linewidth=0.5, label="lợi suất ngày (%)")
    ax.plot(var_g.index, var_g, color=M["chinh"], label="VaR 99% GARCH-t")
    ax.plot(var_c.index, var_c, color=M["phu"], linestyle="--", label="VaR 99% chuẩn, độ lệch chuẩn cố định")
    v = r < var_g
    ax.scatter(r.index[v], r[v], color=M["chinh"], s=14, zorder=3)
    v2 = r < var_c
    ax.scatter(r.index[v2], r[v2], color=M["phu"], s=30, marker="x", zorder=3)
    ax.set_ylabel("%")
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("VaR cố định bị vượt thành cụm lúc bất ổn; VaR GARCH nở ra theo biến động", fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "var.png")
    tb = {}
    for ten, kw in {"GARCH chuẩn": dict(dist="normal"), "GARCH-t": dict(dist="t"), "GJR-t": dict(dist="t", o=1)}.items():
        g = tc.du_bao_garch(jpy, tc.MOC_JPY, **kw)
        if kw["dist"] == "normal":
            q = stats.norm.ppf(0.01)
        else:
            nu = g["nu"].iloc[0]
            q = stats.t.ppf(0.01, nu) * np.sqrt((nu - 2) / nu)
        tb[ten] = tc.kupiec(jpy, g["trung bình"] + q * np.sqrt(g["phương sai"]))
    tb["chuẩn cố định"] = tc.kupiec(jpy, var_c)
    return {k: {x: round(y, 4) if isinstance(y, float) else y for x, y in v.items()} for k, v in tb.items()}


def hinh_har(r, rv) -> dict:
    har = tc.du_bao_har(rv, tc.MOC)
    g = tc.du_bao_garch(r, tc.MOC)["phương sai"].reindex(har.index)
    gj = tc.du_bao_garch(r, tc.MOC, o=1)["phương sai"].reindex(har.index)
    co_dinh = pd.Series(r[r.index < pd.Timestamp(tc.MOC)].var(), index=har.index)
    ewma = (r ** 2).ewm(alpha=0.06).mean().shift(1).reindex(har.index)
    y = rv.loc[har.index]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(y.index, y, color=M["xam"], linewidth=0.6, label="biến động thực hiện (từ lợi suất giờ)")
    ax.plot(har.index, har, color=M["chinh"], label="HAR")
    ax.plot(g.index, g, color=M["ba"], label="GARCH-t")
    ax.plot(co_dinh.index, co_dinh, color=M["phu"], linestyle="--", label="cố định (phương sai 2023)")
    ax.set_yscale("log")
    ax.set_ylabel("phương sai ngày (%², thang log)")
    ax.legend(fontsize=8)
    ax.set_title("BTC 2024: HAR và GARCH bám theo biến động; con số cố định thì không", fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "har.png")
    bang = {ten: {"QLIKE": tc.qlike(y, h), "MSE": float(np.mean((y - h) ** 2))}
            for ten, h in {"HAR": har, "GARCH-t": g, "GJR-t": gj, "EWMA": ewma, "cố định": co_dinh,
                           "RV hôm qua": rv.shift(1).loc[har.index]}.items()}
    return {k: {x: round(v, 3) for x, v in d.items()} for k, d in bang.items()}


def hinh_markov(jpy) -> dict:
    p = tc.markov_2_trang_thai(jpy)
    gia = tc.doc_jpy()
    fig, a = plt.subplots(2, 1, figsize=(9, 4.6), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
    a[0].plot(gia.index, gia, color=M["chinh"], linewidth=0.7)
    a[0].set_ylabel("yên / USD")
    a[1].fill_between(p.index, 0, p.rolling(20).mean(), color=M["phu"])
    a[1].set_ylabel("xác suất bất ổn\n(TB 20 ngày)")
    a[1].set_ylim(0, 1)
    fig.suptitle("Markov 2 trạng thái trên JPY/USD: giai đoạn biến động cao 2008–2009 và 2022 hiện rõ", fontsize=10,
                 fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "markov.png")
    return {"tỷ lệ ngày bất ổn": float((p > 0.5).mean()), "theo năm": p.resample("YS").mean().round(2).set_axis(
        p.resample("YS").mean().index.year).to_dict()}


if __name__ == "__main__":
    gia, r, rv = tc.btc_ngay()
    jpy = tc.loi_suat(tc.doc_jpy())
    print("sự thật BTC:", {k: round(v, 4) for k, v in tc.su_that_cach_dieu(r).items()})
    print("sự thật JPY:", {k: round(v, 4) for k, v in tc.su_that_cach_dieu(jpy).items()}, hinh_su_that(jpy))
    print("demo:", hinh_demo(gia))
    print("VaR:", hinh_var(jpy))
    print("HAR:", hinh_har(r, rv))
    print("Markov:", hinh_markov(jpy))
    print("RV trung bình 2024 / phương sai lợi suất ngày 2024:", float(rv["2024"].mean()), float(r["2024"].var()))
