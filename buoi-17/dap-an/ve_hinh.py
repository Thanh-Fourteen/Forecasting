# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 17 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

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

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("ar", DAY / "arima.py")
ar = importlib.util.module_from_spec(spec)
sys.modules["ar"] = ar
spec.loader.exec_module(ar)
M = ve.MAU


def _cot(ax, gia_tri, n, tieu_de, mau):
    ax.bar(np.arange(1, len(gia_tri) + 1), gia_tri, color=mau)
    gh = 1.96 / np.sqrt(n)
    ax.axhline(gh, color="black", linestyle="--", linewidth=0.7)
    ax.axhline(-gh, color="black", linestyle="--", linewidth=0.7)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title(tieu_de, fontsize=9)


def hinh_mo_phong() -> dict:
    mau = {"AR(2): φ = 0,6; 0,3": dict(ar=[0.6, 0.3]), "MA(1): θ = 0,8": dict(ma=[0.8]),
           "ARMA(1,1): φ = 0,7; θ = 0,4": dict(ar=[0.7], ma=[0.4])}
    fig, a = plt.subplots(2, 3, figsize=(11, 4.6), sharey=True)
    ra = {}
    for j, (ten, tham_so) in enumerate(mau.items()):
        y = ar.mo_phong(n=500, seed=1, **tham_so)
        b = ar.acf_pacf(y, 12)
        _cot(a[0, j], b["acf"], len(y), f"{ten} — ACF", M["chinh"])
        _cot(a[1, j], b["pacf"], len(y), "PACF", M["phu"])
        a[1, j].set_xlabel("trễ")
        ra[ten] = b.iloc[:3].round(2).to_dict()
    fig.suptitle("AR(p): PACF tắt sau p trễ; MA(q): ACF tắt sau q trễ; ARMA: cả hai tắt dần",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "acf-pacf-mo-phong.png")
    return ra


def hinh_ip(ip) -> None:
    y = np.log(ip.to_numpy()) * 100
    d = np.diff(y)
    b = ar.acf_pacf(d, 12)
    fig, (a, bb, c) = plt.subplots(1, 3, figsize=(11, 3.3), gridspec_kw={"width_ratios": [1.6, 1, 1]})
    a.plot(ip.index[1:], d, color=M["chinh"], linewidth=0.8)
    a.axhline(0, color="black", linewidth=0.5)
    a.set_ylabel("tăng trưởng tháng (%)")
    a.set_title("100 × sai phân log, 2000–2019", fontsize=9)
    _cot(bb, b["acf"], len(d), "ACF: tắt dần", M["chinh"])
    _cot(c, b["pacf"], len(d), "PACF: tắt sau trễ 4", M["phu"])
    bb.set_xlabel("trễ")
    c.set_xlabel("trễ")
    fig.suptitle("Sản lượng công nghiệp Mỹ: PACF của chuỗi sai phân gợi ý AR(4)", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ip-acf-pacf.png")


def hinh_t33(y) -> dict:
    w = np.diff(y[12:] - y[:-12])
    b = ar.acf_pacf(w, 26)
    quen, du = ar.arima(y, (0, 1, 1), (0, 0, 0)), ar.mo_hinh_tu_chon(y)
    fig, a = plt.subplots(1, 3, figsize=(11, 3.3))
    _cot(a[0], b["acf"], len(w), "ACF của sai phân mùa vụ + sai phân thường", M["chinh"])
    for ax, mh, ten, c in ((a[1], quen, "ARIMA(0,1,1): quên mùa vụ", M["phu"]),
                           (a[2], du, "SARIMA(0,1,1)(0,1,1)12", M["ba"])):
        p, q, P, Q, m, d, D = mh.model_["arma"]
        e = mh.model_["residuals"][d + D * m:]
        _cot(ax, ar.acf_pacf(e, 26)["acf"], len(e), f"ACF phần dư — {ten}", c)
    for ax in a:
        ax.set_xlabel("trễ")
    fig.suptitle("Chuỗi du lịch T33: gai ở trễ 1 và 12 → MA(1) và MA mùa vụ(1); quên phần mùa vụ thì phần dư còn gai ở 12",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "sarima-t33.png")
    return {k: round(float(b["acf"].loc[k]), 2) for k in (1, 2, 11, 12, 13, 24)}


def hinh_khoang(y) -> dict:
    ngay_mai = ar.du_bao(ar.arima(y, (0, 1, 0), hang_so=False), 24)
    sarima = ar.du_bao(ar.mo_hinh_tu_chon(y), 24)
    fig, ax = plt.subplots(figsize=(10, 3.4))
    n = len(y)
    x = np.arange(n - 60, n)
    ax.plot(x, np.exp(y[-60:]) / 1e3, color="black", label="lịch sử")
    xs = np.arange(n, n + 24)
    for bang, ten, c in ((ngay_mai, "ARIMA(0,1,0)", M["phu"]), (sarima, "SARIMA(0,1,1)(0,1,1)12", M["chinh"])):
        ax.plot(xs, np.exp(bang["mean"]) / 1e3, color=c, label=ten)
        ax.fill_between(xs, np.exp(bang["lo-95"]) / 1e3, np.exp(bang["hi-95"]) / 1e3, color=c, alpha=0.15)
    ax.set_xlabel("tháng")
    ax.set_ylabel("khách (nghìn)")
    ax.legend(fontsize=8)
    ax.set_title("Khoảng 95%: ARIMA(0,1,0) nở theo √h và bỏ nhịp mùa; SARIMA hẹp hơn và theo nhịp")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "khoang-du-bao.png")
    rong = lambda b, k: float(b["hi-95"].iloc[k - 1] - b["lo-95"].iloc[k - 1])  # noqa: E731
    return {"độ rộng log bước 1, 4, 16 của ARIMA(0,1,0)": [round(rong(ngay_mai, k), 3) for k in (1, 4, 16)]}


def hinh_backtest(mase) -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    tb = mase.mean()
    a.bar(tb.index, tb.to_numpy(), color=[M["chinh"], M["ba"], M["xam"]])
    for i, v in enumerate(tb.to_numpy()):
        a.text(i, v + 0.02, f"{v:.3f}".replace(".", ","), ha="center", fontsize=9)
    a.set_ylabel("MASE trung bình, 366 chuỗi")
    a.set_title("hai cửa sổ 24 tháng", fontsize=9)
    d = (mase["AutoARIMA"] - mase["AutoETS"]).clip(-1.5, 1.5)
    b.hist(d, bins=50, color=M["bon"])
    b.axvline(0, color="black", linewidth=0.8)
    b.set_xlabel("MASE AutoARIMA − MASE AutoETS (cắt ở ±1,5)")
    b.set_ylabel("số chuỗi")
    b.set_title("mỗi bên thắng khoảng một nửa số chuỗi", fontsize=9)
    fig.suptitle("AutoARIMA và AutoETS cùng thắng seasonal naive; giữa hai cái không có bên thắng",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "so-sanh-backtest.png")


if __name__ == "__main__":
    ip = ar.doc_g17()[:"2019-12"]
    y_ip = np.log(ip.to_numpy()) * 100
    print(ar.acf_pacf(np.diff(y_ip), 6).round(2))
    print(ar.bang_ung_vien(y_ip, [(1, 1, 0), (2, 1, 0), (4, 1, 0), (0, 1, 1), (1, 1, 1), (2, 1, 2)]).round(3)
          .to_string(index=False))
    mh4 = ar.arima(y_ip, (4, 1, 0))
    print("AR(4) hệ số:", {k: round(float(v), 3) for k, v in mh4.model_["coef"].items()})
    t33 = np.log(ar.doc_tourism()["T33"][:-ar.TAM])
    print("T33:", len(t33), "tháng")
    tu = ar.auto_arima(t33)
    print("auto:", ar.ten_mo_hinh(tu), round(tu.model_["aicc"], 2), ar.kiem_phan_du(tu))
    for so in ((0, 0, 0), (0, 1, 1)):
        mh = ar.mo_hinh_tu_chon(t33, seasonal_order=so)
        print(ar.ten_mo_hinh(mh), round(mh.model_["aicc"], 2), ar.kiem_phan_du(mh),
              {k: round(float(v), 3) for k, v in mh.model_["coef"].items()})
    with ve.phong_cach():
        print(hinh_mo_phong())
        hinh_ip(ip)
        print("ACF T33:", hinh_t33(t33))
        print(hinh_khoang(t33))
        df = ar.dang_dai(ar.doc_tourism())
        kq = ar.backtest_tourism(df, luu=True)
        mase = ar.mase_theo_chuoi(kq, df)
        print(mase.agg(["mean", "median"]).round(3))
        print(ar.so_sanh(mase).round(4).to_string(index=False))
        hinh_backtest(mase)
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
