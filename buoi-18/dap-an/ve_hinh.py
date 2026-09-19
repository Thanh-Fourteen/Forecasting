# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 18 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

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

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("hq", DAY / "hoi_quy.py")
hq = importlib.util.module_from_spec(spec)
sys.modules["hq"] = hq
spec.loader.exec_module(hq)
M = ve.MAU


def hinh_hoi_quy_gia() -> dict:
    import statsmodels.api as sm
    y, X = hq.cap_gia()
    ols = sm.OLS(y, sm.add_constant(X)).fit()
    fig, a = plt.subplots(1, 2, figsize=(11, 3.8))
    a[0].plot(y.index, y.rolling(12).mean(), color=M["chinh"], label="hành khách EU (triệu/tháng, TB 12 tháng)")
    b = a[0].twinx()
    b.plot(X.index, X["ip"], color=M["phu"], label="sản lượng CN Mỹ (2017 = 100)")
    a[0].set_ylabel("triệu khách/tháng", color=M["chinh"])
    b.set_ylabel("chỉ số", color=M["phu"])
    a[0].set_title("hai chuỗi không liên quan, cùng đi lên", fontsize=9)
    a[1].plot(y.index, ols.resid, color=M["chinh"])
    a[1].axhline(0, color="black", linewidth=0.6)
    a[1].set_ylabel("phần dư (triệu khách)")
    a[1].set_title("phần dư hồi quy thường: lệch một phía nhiều năm liền", fontsize=9)
    fig.suptitle("Hồi quy giả: R² = 0,83, p = 3·10⁻¹⁶, nhưng phần dư tự tương quan mạnh", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "hoi-quy-gia.png")
    e = ols.resid.to_numpy()
    them = X.assign(t=np.arange(len(y)))
    ols_t = sm.OLS(y, sm.add_constant(them)).fit()
    return {"ols": hq.hoi_quy_ols(y, X), "dong": hq.he_so_ip(y, X), "so tháng dư dương dài nhất": _chuoi_dai(e > 0),
            "thêm xu hướng: hệ số, p": (float(ols_t.params["ip"]), float(ols_t.pvalues["ip"]))}


def _chuoi_dai(dau: np.ndarray) -> int:
    dai = hien = 0
    for d in dau:
        hien = hien + 1 if d else 0
        dai = max(dai, hien)
    return dai


def hinh_mo_phong() -> dict:
    import statsmodels.api as sm
    rng = np.random.default_rng(0)
    p_muc, p_sp = [], []
    for _ in range(1000):
        a, b = rng.normal(size=120).cumsum(), rng.normal(size=120).cumsum()
        p_muc.append(sm.OLS(a, sm.add_constant(b)).fit().pvalues[1])
        p_sp.append(sm.OLS(np.diff(a), sm.add_constant(np.diff(b))).fit().pvalues[1])
    fig, a = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    bins = np.linspace(0, 1, 21)
    a[0].hist(p_muc, bins=bins, color=M["phu"])
    a[0].set_title(f"hồi quy trên mức: {np.mean(np.array(p_muc) < 0.05):.1%} có p < 0,05", fontsize=9)
    a[1].hist(p_sp, bins=bins, color=M["chinh"])
    a[1].set_title(f"hồi quy trên sai phân: {np.mean(np.array(p_sp) < 0.05):.1%} có p < 0,05", fontsize=9)
    for x in a:
        x.axvline(0.05, color="black", linestyle="--", linewidth=0.8)
        x.set_xlabel("p-value của hệ số")
    a[0].set_ylabel("số lần (trong 1.000)")
    fig.suptitle("1.000 cặp bước ngẫu nhiên độc lập: hồi quy trên mức 'tìm thấy' quan hệ ở phần lớn các cặp",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "mo-phong-hoi-quy-gia.png")
    return {"mức": float(np.mean(np.array(p_muc) < 0.05)), "sai phân": float(np.mean(np.array(p_sp) < 0.05))}


def hinh_nhiet_tai(y, nhiet) -> dict:
    d = pd.DataFrame({"y": y / 1000, "T": nhiet["that"].reindex(y.index)}).dropna()
    ngay = d.resample("D").mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(ngay["T"], ngay["y"], s=8, color=M["chinh"], alpha=0.6)
    ax.axvline(hq.MUC_CDD, color="black", linestyle="--", linewidth=0.8)
    ax.set_xlabel("nhiệt độ trung bình ngày ở Dallas (°C)")
    ax.set_ylabel("tải trung bình ngày (GW)")
    ax.set_title("Tải ERCOT 2024 theo nhiệt độ: hình chữ U, dốc dần về hai phía", fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "nhiet-tai.png")
    lanh, mat, nong = ngay[ngay["T"] < 5], ngay[(ngay["T"] > 15) & (ngay["T"] < 21)], ngay[ngay["T"] > 30]
    return {"GW lạnh < 5": float(lanh["y"].mean()), "GW 15–21": float(mat["y"].mean()), "GW > 30": float(nong["y"].mean())}


def hinh_fourier(y) -> dict:
    thang1 = y["2024-01-01 07:00":"2024-02-01 06:00"]
    ho_so = thang1.groupby((thang1.index - pd.Timedelta(hours=6)).hour).mean() / 1000   # giờ Texas mùa đông = UTC − 6
    t = np.arange(24)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(t, ho_so.to_numpy(), color="black", marker=".", label="tải trung bình tháng 1/2024")
    ra = {}
    for K, c in ((1, M["phu"]), (2, M["ba"]), (4, M["chinh"])):
        A = np.c_[np.ones(24), *[f(2 * np.pi * k * t / 24) for k in range(1, K + 1) for f in (np.sin, np.cos)]]
        xap_xi = A @ np.linalg.lstsq(A, ho_so.to_numpy(), rcond=None)[0]
        ax.plot(t, xap_xi, color=c, label=f"K = {K}: {2 * K} biến sin/cos")
        ra[K] = float(np.mean(np.abs(xap_xi - ho_so.to_numpy())) * 1000)
    ax.set_xlabel("giờ trong ngày (giờ Texas)")
    ax.set_ylabel("GW")
    ax.legend(fontsize=8)
    ax.set_title("Nhịp ngày mùa đông có hai đỉnh: K = 1 chỉ một làn sóng, mất cả hai đỉnh; K = 4 bám sát", fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "fourier.png")
    ra["đỉnh GW"] = float(ho_so.max())
    ra["đáy GW"] = float(ho_so.min())
    return ra


def hinh_so_sanh(kq) -> pd.DataFrame:
    mae = hq.mae_theo_cua_so(kq)
    tb = mae.mean().sort_values()
    fig, a = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1, 1.5]})
    mau = [M["chinh"] if c == "DHR" else (M["xam"] if c.startswith("SN") else M["ba"]) for c in tb.index]
    a[0].barh(tb.index[::-1], tb.to_numpy()[::-1] / 1000, color=mau[::-1])
    a[0].set_xlabel("MAE trung bình 24 cửa sổ (GW)")
    for c, ms in (("SN24", M["xam"]), ("DHR", M["chinh"]), ("MSTL", M["ba"]), ("Prophet", M["phu"])):
        a[1].plot(mae.index, mae[c] / 1000, marker=".", color=ms, label=c)
    a[1].set_ylabel("MAE một ngày (GW)")
    a[1].legend(fontsize=8)
    a[1].xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m/%Y"))
    a[1].tick_params(axis="x", labelrotation=30)
    a[1].set_xlabel("cutoff")
    fig.suptitle("Tải ERCOT, dự báo ngày tới: hồi quy động, MSTL, seasonal naive ngang nhau; Prophet, hồi quy thường thua rõ",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "so-sanh-da-mua-vu.png")
    return mae


def hinh_prophet_tet() -> dict:
    ra = {}
    kq = {}
    for khai in (False, True):
        kq[khai] = hq.backtest_wiki(khai_tet=khai)
        k = kq[khai]
        ra[khai] = {"MAE cả năm": float((k["y"] - k["Prophet"]).abs().mean()), "MAE quanh Tết": hq.mae_quanh_tet(k),
                    "MAE cả năm 2024": float((k["y"] - k["Prophet"]).abs()[k["ds"].dt.year == 2024].mean())}
    k = kq[True]
    ra["SN364"] = {"MAE cả năm": float((k["y"] - k["SN364"]).abs().mean()), "MAE quanh Tết": hq.mae_quanh_tet(k, "SN364")}
    doan = (k["ds"] >= "2024-01-15") & (k["ds"] <= "2024-03-10")
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(k.loc[doan, "ds"], k.loc[doan, "y"], color="black", label="thực tế")
    ax.plot(k.loc[doan, "ds"], kq[False].loc[doan, "Prophet"], color=M["phu"], label="Prophet mặc định")
    ax.plot(k.loc[doan, "ds"], k.loc[doan, "Prophet"], color=M["chinh"], label="Prophet khai Tết (± 7 ngày)")
    ax.axvline(pd.Timestamp("2024-02-10"), color=M["xam"], linestyle="--", linewidth=0.8)
    ax.set_ylabel("triệu lượt xem/ngày")
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d/%m"))
    ax.set_xlabel("ngày (năm 2024)")
    ax.legend(fontsize=8)
    ax.set_title("Tết 2024 (mùng 1 = 10/2): Prophet mặc định không biết Tết nên đoán cao cả tuần nghỉ",
                 fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "prophet-tet.png")
    return ra


if __name__ == "__main__":
    print("hồi quy giả:", hinh_hoi_quy_gia())
    print("mô phỏng:", hinh_mo_phong())
    y, nhiet = hq.doc_dien(), hq.doc_nhiet()
    print("nhiệt–tải:", hinh_nhiet_tai(y, nhiet))
    print("fourier MAE (MW):", hinh_fourier(y))
    print("prophet tết:", hinh_prophet_tet())
    kq = hq.backtest_dien(luu=True)
    mae = hinh_so_sanh(kq)
    print("MAE trung bình / trung vị:\n", pd.DataFrame({"tb": mae.mean(), "tv": mae.median(),
                                                      "thắng SN24": (mae.lt(mae["SN24"], axis=0)).mean()}).round(3))
    df = pd.DataFrame({"unique_id": "ERCO", "ds": y.index, "y": y.to_numpy()})
    ex_post = hq.backtest(df, lambda ls, ds: hq.du_bao_dhr(ls, ds, nhiet.assign(du_bao=nhiet["that"])),
                          h=hq.H, so_cua_so=hq.SO_CUA_SO, buoc=hq.BUOC, cua_so_train=hq.HOC)
    print("DHR ex-post MAE:", float((ex_post["y"] - ex_post["DHR"]).abs().mean()))
    cuoi = kq["cutoff"].iloc[len(kq) // 2]
    ls = df[(df["ds"] <= cuoi) & (df["ds"] > cuoi - pd.Timedelta(hours=hq.HOC))]
    print("chọn K tại", cuoi, "\n", hq.chon_K(ls, nhiet=nhiet).round(1))
    from statsforecast.models import AutoARIMA
    X = hq.bien_giai_thich(pd.DatetimeIndex(ls["ds"]), nhiet["that"])
    mh = AutoARIMA(season_length=1).fit(ls["y"].to_numpy(), X=X[hq._cot_dung(X)].to_numpy())
    print("ARIMA sai số:", mh.model_["arma"], "Ljung-Box p (24, 48):", hq.ljung_box_p(mh.model_["residuals"], 24),
          hq.ljung_box_p(mh.model_["residuals"], 48))
