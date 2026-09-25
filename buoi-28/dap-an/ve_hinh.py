# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 28 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (khoảng 2 phút)

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
spec = importlib.util.spec_from_file_location("pc", DAY / "phan_cap.py")
pc = importlib.util.module_from_spec(spec)
sys.modules["pc"] = pc
spec.loader.exec_module(pc)

COT = {"AutoETS": "base", "SeasonalNaive": "seasonal naive", "AutoETS/BottomUp": "bottom-up",
       "AutoETS/TopDown_method-forecast_proportions": "top-down", "AutoETS/MinTrace_method-ols": "OLS",
       "AutoETS/MinTrace_method-mint_shrink": "MinT"}
THU_TU = ["quốc gia", "bang", "khu vực", "khu vực × mục đích"]


def vi_du_tay() -> None:
    S = np.array([[1.0, 1], [1, 0], [0, 1]])
    base = np.array([10.0, 4, 5])
    print("OLS ví dụ 3 chuỗi:", pc.hoa_giai_ols(base, S).round(4), "| bottom-up:", S @ base[1:])


def main() -> None:
    vi_du_tay()
    d = pc.doc_du_lich()
    Y, S_df, tags = pc.tong_hop(d)
    ten, S = pc.ma_tran_S(S_df)
    print("S:", S.shape, "| số chuỗi mỗi cấp:", {pc.TEN_CAP[k]: len(v) for k, v in tags.items()}, "| quý:", Y["ds"].nunique())
    R = pc.backtest(Y, S_df, tags)
    B = pc.bang_sai_so(R, list(COT))
    B["cach"] = B["cach"].map(COT)
    rm = B.pivot(index="cap", columns="cach", values="rmse").loc[THU_TU, list(COT.values())]
    me = B.pivot(index="cap", columns="cach", values="sai_so_co_dau").loc[THU_TU, list(COT.values())]
    with pd.option_context("display.width", 200):
        print("RMSE\n", rm.round(1))
        print("sai số có dấu (thực tế − dự báo)\n", me.round(1))
    moc_cuoi = R[R["moc"] == R["moc"].max()]
    for c in COT:
        print(f"lệch cộng {COT[c]:15s} {pc.do_lech_cong(moc_cuoi, S_df, c):.4g}")
    base = moc_cuoi.pivot(index="unique_id", columns="ds", values="AutoETS").loc[ten].to_numpy()
    lib = moc_cuoi.pivot(index="unique_id", columns="ds", values="AutoETS/MinTrace_method-ols").loc[ten].to_numpy()
    print("OLS tự viết − thư viện, lớn nhất:", float(np.abs(pc.hoa_giai_ols(base, S) - lib).max()))
    cov = {}
    for c in ("AutoETS", "AutoETS/BottomUp", "AutoETS/MinTrace_method-ols", "AutoETS/MinTrace_method-mint_shrink"):
        cov[f"{COT[c]} (chuẩn, trong mẫu)"] = pc.coverage(R, c).reindex(THU_TU)
        print(f"coverage 90% {COT[c]:10s}", pc.coverage(R, c).reindex(THU_TU).round(3).to_dict(),
              "| 80%", pc.coverage(R, c, 80).reindex(THU_TU).round(3).to_dict())
    F, A = pc.sai_so_ngoai_mau(Y, S_df)
    cap = {i: pc.TEN_CAP[k] for k, v in tags.items() for i in v}
    for muc in (0.9, 0.8):
        K = pc.khoang_khop(F, A, S, muc=muc)
        K["cap"] = K["unique_id"].map(cap)
        K["trong"] = (K["y"] >= K["lo"]) & (K["y"] <= K["hi"])
        bang = K.groupby(["cap", "cach"]).trong.mean().unstack().loc[THU_TU]
        print(f"coverage {muc:.0%} ngoài mẫu\n", bang.round(3))
        if muc == 0.9:
            for c in ("base", "ols", "mint"):
                cov[f"{c} (ngoài mẫu)"] = bang[c]
            print("số mốc:", K["moc"].nunique(), "| điểm cấp quốc gia:", int(((K.cap == "quốc gia") & (K.cach == "base")).sum()))
            Kq = K[(K.cap == "quốc gia") & (K.cach == "base")]
            print("sai số có dấu cấp quốc gia (ngoài mẫu, base):", round(float((Kq.y - Kq.du_bao).mean()), 1),
                  "| thời gian:", Kq["moc"].min().date(), "→", Kq["moc"].max().date())
    print(pc.phan_cap_thoi_gian(Y).round(1).to_string())

    with ve.phong_cach():
        # 1. không khớp: quốc gia vs tổng đáy
        m = moc_cuoi
        q = m[m["unique_id"] == "Australia"].sort_values("ds")
        bu = m[m["unique_id"].isin(tags["Total/State/Region/Purpose"])].groupby("ds")["AutoETS"].sum()
        su = Y[(Y["unique_id"] == "Australia") & (Y["ds"] >= "2011-01-01")]
        fig, ax = plt.subplots(figsize=(8, 3.4))
        ax.plot(su["ds"], su["y"] / 1000, color="black", lw=1, label="thực tế")
        ax.plot(q["ds"], q["AutoETS"] / 1000, color=M["chinh"], lw=1.4, label="dự báo base cấp quốc gia")
        ax.plot(bu.index, bu.to_numpy() / 1000, color=M["phu"], lw=1.4, ls="--", label="tổng 304 dự báo base cấp đáy")
        ax.plot(q["ds"], q["AutoETS/MinTrace_method-mint_shrink"] / 1000, color=M["ba"], lw=1.2, label="MinT (khớp)")
        ax.axvline(pd.Timestamp(pc.MOC_CAT[-1]), color=M["xam"], ls=":", lw=1)
        ax.set_ylabel("triệu chuyến / quý")
        ax.set_xlabel("quý")
        ax.set_title("Hai con số cho cùng một nước Úc; cả hai và MinT đều thấp hơn đợt tăng 2016–2017")
        ax.legend(fontsize=7)
        ve.luu_hinh(fig, HINH / "khong-khop.png")

        # 2. RMSE tương đối
        fig, ax = plt.subplots(figsize=(8, 3.4))
        cach = ["bottom-up", "top-down", "OLS", "MinT"]
        x = np.arange(len(THU_TU))
        for i, c in enumerate(cach):
            ax.bar(x + (i - 1.5) * 0.2, (rm[c] / rm["base"]).to_numpy(), width=0.2, label=c,
                   color=[M["phu"], M["vang"], M["chinh"], M["ba"]][i])
        ax.axhline(1, color="black", lw=0.8)
        ax.set_xticks(x, THU_TU)
        ax.set_ylabel("RMSE ÷ RMSE base")
        ax.set_title("Hoà giải giúp ba cấp dưới; ở cấp quốc gia không cách nào hơn base")
        ax.legend(fontsize=7, ncol=4)
        ve.luu_hinh(fig, HINH / "rmse-theo-cap.png")

        # 3. coverage
        fig, ax = plt.subplots(figsize=(8, 3.4))
        chon = ["base (chuẩn, trong mẫu)", "MinT (chuẩn, trong mẫu)", "base (ngoài mẫu)", "ols (ngoài mẫu)"]
        mau = [M["xam"], M["phu"], M["nhat"], M["chinh"]]
        for i, c in enumerate(chon):
            ax.bar(x + (i - 1.5) * 0.2, cov[c].to_numpy(), width=0.2, label=c, color=mau[i])
        ax.axhspan(0.85, 0.95, color=M["ba"], alpha=0.15, lw=0, label="dải 85–95%")
        ax.set_xticks(x, THU_TU)
        ax.set_ylabel("tỷ lệ thực tế nằm trong khoảng 90%")
        ax.set_ylim(0, 1)
        ax.set_title("Khoảng từ phần dư trong mẫu phủ thiếu nặng ở cấp trên; sai số ngoài mẫu kéo lên gần 80%")
        ax.legend(fontsize=7, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.15))
        ve.luu_hinh(fig, HINH / "coverage-theo-cap.png")


if __name__ == "__main__":
    main()
