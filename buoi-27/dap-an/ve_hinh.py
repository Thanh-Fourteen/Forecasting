# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 27 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (khoảng 10–15 phút: GP ba thành phần, GP hai thành phần, BSTS)

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

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
M = ve.MAU
spec = importlib.util.spec_from_file_location("by", DAY / "bayes.py")
by = importlib.util.module_from_spec(spec)
sys.modules["by"] = by
spec.loader.exec_module(by)


def tron(d: dict) -> dict:
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items()}


def vi_du_tay() -> None:
    """Gamma–Poisson: prior Gamma(2, 1) cho tốc độ bán; thấy 0, 1, 0 món trong 3 tháng."""
    a, b = 2.0, 1.0
    y = np.array([0, 1, 0])
    a2, b2 = a + y.sum(), b + len(y)
    print(f"prior trung bình {a / b}; posterior Gamma({a2:g}, {b2:g}) trung bình {a2 / b2}; không gộp {y.mean():.3f}")
    rng = np.random.default_rng(0)
    lam = rng.gamma(a2, 1 / b2, 100_000)
    du = rng.poisson(lam)
    print("posterior predictive: P(0 món)", round(float((du == 0).mean()), 3), "| P(≥ 3 món)", round(float((du >= 3).mean()), 3))


def main() -> None:
    vi_du_tay()
    Y = by.doc_car_parts()
    C = by.chia_car_parts(Y)
    rong = by.tien_nghiem(by.mo_hinh_phan_cap(C["hoc"], {"mu_sd": 10.0, "tau_sd": 10.0}))
    hep = by.tien_nghiem(by.mo_hinh_phan_cap(C["hoc"]))
    thuc = np.concatenate(C["hoc"])
    for ten, v in (("rộng", rong), ("hẹp", hep), ("dữ liệu", thuc)):
        print(f"prior {ten}: trung vị {np.quantile(v, 0.5):.0f}, q90 {np.quantile(v, 0.9):.3g}, q99 {np.quantile(v, 0.99):.3g}, max {v.max():.3g}")
    print("số tháng học:", len(thuc), "| tỷ lệ tháng bằng 0:", round(float((thuc == 0).mean()), 3), "| trung bình:", round(float(thuc.mean()), 3))
    _, idt = by.hoc_phan_cap(C["hoc"])
    cd = by.chan_doan(idt, ["mu", "tau", "theta"])
    print("phân cấp:", tron(cd), by.dung_duoc(cd), "| mu", round(float(idt["posterior"]["mu"].mean()), 3),
          "tau", round(float(idt["posterior"]["tau"].mean()), 3))
    L = by.ba_cach_gop(C["hoc"], idt)
    for k, v in L.items():
        print(f"{k:14s} RMSE {by.rmse(C['kiem'], v):.3f}", {n: round(by.rmse(C['kiem'], v, C['lich_su'] == n), 3) for n in by.LICH_SU})
    print("không gộp = 0 mà 12 tháng chấm có bán:", int(((L["khong_gop"] == 0) & (C["kiem"].sum(1) > 0)).sum()),
          "/ không gộp = 0:", int((L["khong_gop"] == 0).sum()))
    print(by.tan_suat_dem(idt, C["kiem"]).round(3).to_string())
    for muc in (0.5, 0.8, 0.9):
        lo, hi = by.khoang_phan_cap(idt, muc)
        k = C["kiem"]
        print(f"coverage khoảng {muc:.0%} (phân cấp): {((k >= lo[:, None]) & (k <= hi[:, None])).mean():.3f}")
    for th in ("tam", "lech"):
        for ta in (0.8, 0.95):
            print("8 trường", th, ta, tron(by.chan_doan(by.lay_mau(by.mo_hinh_8_truong(th), target_accept=ta), ["mu", "tau", "theta"])))
    i8t = by.lay_mau(by.mo_hinh_8_truong("tam"), target_accept=0.8)
    i8l = by.lay_mau(by.mo_hinh_8_truong("lech"), target_accept=0.95)

    df = by.doc_xe_dap()
    du_ets = by.ets(df)
    print("ETS", tron(by.cham_ngay(df, du_ets)))
    m3, i3, c3 = by.hoc_gp(df, ("xu_huong", "nam", "tuan"))
    print("GP ba thành phần", tron(c3), tron(by.cham_ngay(df, by.du_bao_gp(m3, i3))))
    m2, i2, c2 = by.hoc_gp(df)
    du_gp = by.du_bao_gp(m2, i2)
    print("GP hai thành phần", tron(c2), tron(by.cham_ngay(df, du_gp)))
    mo, ib, dub = by.bsts(df)
    cb = by.chan_doan(ib, ["sigma_level_trend", "sigma_MeasurementError", "initial_level_trend"])
    fo = np.exp(dub["forecast_observed"].values[..., 0].reshape(-1, by.NGAY_KIEM))
    du_bs = pd.DataFrame({"giua": np.median(fo, 0), "lo": np.quantile(fo, 0.05, 0), "hi": np.quantile(fo, 0.95, 0)})
    print("BSTS", tron(cb), tron(by.cham_ngay(df, du_bs)))
    y60 = df["y"].to_numpy()[-by.NGAY_KIEM:]
    print("hai ngày trước đoạn kiểm:", df.iloc[-by.NGAY_KIEM - 5:-by.NGAY_KIEM].to_string())
    print("seasonal naive 7 ngày MAE:", round(float(np.mean(np.abs(y60 - np.r_[df["y"].to_numpy()[-by.NGAY_KIEM - 7:-by.NGAY_KIEM]] [np.arange(by.NGAY_KIEM) % 7]))), 1))

    with ve.phong_cach():
        # 1. prior predictive
        fig, ax = plt.subplots(figsize=(7, 3.3))
        bins = np.logspace(0, 16, 50)
        ax.hist(rong[rong > 0] + 1, bins=bins, alpha=0.6, color=M["phu"], label="prior rộng: Normal(0, 10), HalfNormal(10)")
        ax.hist(hep[hep > 0] + 1, bins=bins, alpha=0.7, color=M["chinh"], label="prior hẹp: Normal(0, 1), HalfNormal(1)")
        ax.axvline(thuc.max() + 1, color="black", ls="--", lw=1, label=f"tháng bán nhiều nhất trong dữ liệu ({thuc.max():.0f})")
        ax.set_xscale("log")
        ax.set_xlabel("số món bán một tháng mà prior sinh ra + 1 (thang log)")
        ax.set_ylabel("số lần rút")
        ax.set_title("Prior rộng sinh ra hàng triệu món một tháng; prior hẹp nằm trong cỡ dữ liệu")
        ax.legend(fontsize=7)
        ve.luu_hinh(fig, HINH / "prior-predictive.png")

        # 2. co rút
        fig, ax = plt.subplots(figsize=(6, 4.4))
        mau = {3: M["phu"], 6: M["vang"], 12: M["ba"], 24: M["chinh"]}
        for n in by.LICH_SU:
            k = C["lich_su"] == n
            ax.scatter(L["khong_gop"][k] + 0.01, L["gop_mot_phan"][k] + 0.01, s=10, color=mau[n], alpha=0.8, label=f"{n} tháng lịch sử")
        ax.plot([0.01, 20], [0.01, 20], color=M["xam"], lw=1, ls="--", label="không co rút (đường chéo)")
        ax.axhline(L["gop_hoan_toan"][0], color="black", lw=0.8, ls=":", label="gộp hoàn toàn")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("tốc độ bán khi không gộp (món/tháng, + 0,01)")
        ax.set_ylabel("tốc độ bán khi gộp một phần (+ 0,01)")
        ax.set_title("Chuỗi ít tháng bị kéo mạnh về mức chung")
        ax.legend(fontsize=7)
        ve.luu_hinh(fig, HINH / "co-rut.png")

        # 3. cái phễu
        fig, axs = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
        for ax, (ten, i) in zip(axs, (("centered", i8t), ("non-centered", i8l)), strict=True):
            tau = np.log(i["posterior"]["tau"].values.ravel())
            th = i["posterior"]["theta"].values[..., 0].ravel()
            dv = i["sample_stats"]["diverging"].values.ravel()
            ax.scatter(th[~dv], tau[~dv], s=3, alpha=0.3, color=M["chinh"], label="mẫu")
            ax.scatter(th[dv], tau[dv], s=9, color=M["phu"], label=f"divergence ({dv.sum()})")
            ax.set_title(ten)
            ax.set_xlabel("θ₁ (hiệu quả trường 1)")
            ax.legend(fontsize=7)
        axs[0].set_ylabel("log τ (độ chênh giữa các trường)")
        fig.suptitle("Cái phễu: τ nhỏ thì θ bị ép sát nhau, NUTS trượt ra ngoài — divergence dồn ở cổ phễu", fontweight="bold", y=1.03)
        ve.luu_hinh(fig, HINH / "cai-pheu.png")

        # 4. dự báo 60 ngày
        fig, ax = plt.subplots(figsize=(10, 3.6))
        ds = df["ds"].iloc[-by.NGAY_KIEM - 60:]
        ax.plot(ds, df["y"].iloc[-by.NGAY_KIEM - 60:], color="black", lw=1, label="thực tế")
        x = df["ds"].iloc[-by.NGAY_KIEM:]
        for ten, du, mau_ in (("GP", du_gp, M["chinh"]), ("BSTS", du_bs, M["ba"]), ("ETS", du_ets, M["phu"])):
            ax.plot(x, du["giua"], color=mau_, lw=1.2, label=f"{ten} (trung vị)")
            ax.fill_between(x, du["lo"], du["hi"], color=mau_, alpha=0.12, lw=0)
        ax.set_ylabel("lượt thuê mỗi ngày")
        ax.set_xlabel("ngày (2012)")
        ax.set_title("Bão Sandy (29–30/10) kéo ETS và BSTS xuống; GP nhiễu đuôi dày không bị kéo")
        ax.legend(fontsize=7, ncol=4)
        ve.luu_hinh(fig, HINH / "du-bao-60-ngay.png")


if __name__ == "__main__":
    main()
