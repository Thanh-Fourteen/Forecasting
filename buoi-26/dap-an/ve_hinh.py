# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 26 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (khoảng 2 phút, phần MAPIE chiếm phần lớn)

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
spec = importlib.util.spec_from_file_location("cf", DAY / "conformal.py")
cf = importlib.util.module_from_spec(spec)
sys.modules["cf"] = cf
spec.loader.exec_module(cf)


def vi_du_tay() -> None:
    diem = [1, 2, 2, 3, 3, 4, 5, 6, 8, 12]
    print("split: 10 điểm, α = 0,2 →", cf.quantile_conformal(diem, 0.2), "| α = 0,05 →", cf.quantile_conformal(diem, 0.05))
    a, g, ra = 0.1, 0.05, []
    for loi in (0, 0, 1, 0, 0):
        ra.append(round(a, 3))
        a = a + g * (0.1 - loi)
    print("ACI α_t với lỗi 0, 0, 1, 0, 0 (γ = 0,05):", ra, "→", round(a, 3))
    y, lo, hi = np.array([20, 55, 90, 140]), np.array([15, 40, 70, 100]), np.array([30, 60, 85, 150])
    print("CQR điểm:", np.maximum(lo - y, y - hi).tolist())


def mapie_6_thang(df: pd.DataFrame, P: pd.DataFrame) -> dict:
    m = cf.mapie_aci(df)
    tu_viet = cf.aci(P)
    cung = (P["ds"] >= cf.HIEU_CHINH_DEN) & (P["ds"] < "2015-09-01")
    return {"mapie": cf.tom_tat(m["y"], m["lo"], m["hi"]),
            "tu_viet_cung_6_thang": cf.tom_tat(P.loc[cung, "y"], tu_viet.loc[cung, "lo"], tu_viet.loc[cung, "hi"])}


def main() -> None:
    vi_du_tay()
    df = cf.doc_pm25()
    P = cf.du_bao(df)
    k = (P["giai_doan"] == "kiem").to_numpy()
    y = P.loc[k, "y"].to_numpy()
    print("giờ hiệu chỉnh:", int((~k).sum()), "| giờ kiểm:", int(k.sum()))
    print("MAE LightGBM:", round(float(np.abs(y - P.loc[k, "yhat"]).mean()), 2), "| naive (giờ trước):",
          round(float(np.abs(y - P.loc[k, "lag1"]).mean()), 2), "| seasonal naive 24 giờ:",
          round(float(np.nanmean(np.abs(y - cf.dac_trung(df).set_index("ds")["lag24"].reindex(P.loc[k, "ds"])))), 2))
    print("PM2.5 trung bình theo năm (tháng 3 → tháng 2):",
          P.groupby((P["ds"] - pd.DateOffset(months=2)).dt.year)["y"].mean().round(1).to_dict(),
          "| năm học:", round(float(df.loc[df["ds"] < cf.HOC_DEN, "y"].mean()), 1))
    ph = {"split": cf.split_conformal(P), "CQR": cf.cqr(P), "ACI": cf.aci(P)}
    E = cf.enbpi(df)
    ph["EnbPI"] = P[["ds"]].merge(E[["ds", "lo", "hi"]], on="ds", how="left")
    for ten, K in ph.items():
        print(f"{ten:6s}", {a: round(b, 3) for a, b in cf.tom_tat(y, K.loc[k, "lo"], K.loc[k, "hi"]).items()})
    for g in (0.002, 0.005, 0.01, 0.02):
        K = cf.aci(P, gamma=g)
        print(f"ACI γ={g}", {a: round(b, 3) for a, b in cf.tom_tat(y, K.loc[k, "lo"], K.loc[k, "hi"]).items()})
    E2 = cf.enbpi(df, cua=cf.CUA_30_NGAY)
    yy = P.set_index("ds")["y"].reindex(E2["ds"]).to_numpy()
    print("EnbPI cửa sổ 720 giờ", {a: round(b, 3) for a, b in cf.tom_tat(yy, E2["lo"], E2["hi"]).items()})
    # coverage theo quý và theo mức ô nhiễm
    ds = P.loc[k, "ds"]
    for ten in ("split", "CQR", "ACI"):
        K = ph[ten].loc[k]
        trong = pd.Series((y >= K["lo"].to_numpy()) & (y <= K["hi"].to_numpy()), index=ds.to_numpy())
        print(ten, "theo quý:", trong.groupby(trong.index.quarter).mean().round(3).to_dict())
        muc = pd.cut(P.loc[k, "lag1"].to_numpy(), [-1, 35, 75, 150, 1e9], labels=["≤35", "35–75", "75–150", ">150"])
        print(ten, "theo mức PM2.5 giờ trước:", trong.groupby(muc.astype(str)).mean().round(3).to_dict())
    print("số giờ theo mức:", pd.Series(pd.cut(P.loc[k, "lag1"].to_numpy(), [-1, 35, 75, 150, 1e9])).value_counts()
          .sort_index().to_dict())
    print("MAPIE:", mapie_6_thang(df, P))

    with ve.phong_cach():
        # 1. coverage trượt 30 ngày
        fig, ax = plt.subplots(figsize=(10, 3.6))
        for ten, mau in zip(("split", "EnbPI", "CQR", "ACI"), (M["phu"], M["vang"], M["ba"], M["chinh"]), strict=True):
            K = ph[ten].loc[k]
            c = cf.coverage_truot(y, K["lo"].to_numpy(), K["hi"].to_numpy())
            ax.plot(ds.to_numpy(), c.to_numpy(), color=mau, lw=1.1 if ten in ("split", "ACI") else 0.8,
                    alpha=1 if ten in ("split", "ACI") else 0.7, label=ten)
        ax.axhspan(0.85, 0.95, color=M["xam"], alpha=0.15, lw=0, label="dải 85–95%")
        ax.axhline(0.9, color=M["xam"], ls="--", lw=0.8)
        ax.set_ylabel("coverage 30 ngày gần nhất")
        ax.set_xlabel("thời gian (đoạn kiểm 3/2015 → 2/2017)")
        ax.set_title("Split conformal trượt theo mùa; ACI giữ gần 90% suốt hai năm")
        ax.legend(fontsize=7, ncol=5, loc="lower left")
        ve.luu_hinh(fig, HINH / "coverage-truot.png")

        # 2. độ rộng khoảng: split cố định, CQR theo độ khó, trong một tuần mùa đông
        tuan = (P["ds"] >= "2015-12-18") & (P["ds"] < "2015-12-26")
        fig, axs = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
        for ax, ten in zip(axs, ("split", "CQR"), strict=True):
            K = ph[ten].loc[tuan]
            yt = P.loc[tuan, "y"].to_numpy()
            ra = (yt < K["lo"].to_numpy()) | (yt > K["hi"].to_numpy())
            ax.fill_between(P.loc[tuan, "ds"], K["lo"], K["hi"], color=M["chinh"], alpha=0.3, lw=0, label="khoảng 90%")
            ax.plot(P.loc[tuan, "ds"], yt, color="black", lw=0.9, label="thực tế")
            ax.scatter(P.loc[tuan, "ds"][ra], yt[ra], color=M["phu"], s=8, zorder=3, label="ra ngoài")
            ax.set_title(f"{ten}: {ra.sum()} / {len(ra)} giờ ra ngoài")
            ax.set_xlabel("ngày (12/2015)")
            ax.tick_params(axis="x", labelrotation=30)
        axs[0].set_ylabel("PM2.5 (µg/m³)")
        axs[0].legend(fontsize=7, loc="upper left")
        fig.suptitle("Đợt ô nhiễm mùa đông: split giữ độ rộng cố định, CQR nới theo mức ô nhiễm", fontweight="bold",
                     y=1.03)
        ve.luu_hinh(fig, HINH / "split-cqr-mua-dong.png")

        # 3. α_t của ACI
        K = ph["ACI"].loc[k]
        fig, ax = plt.subplots(figsize=(10, 2.8))
        ax.plot(ds.to_numpy(), K["alpha_t"].to_numpy(), color=M["chinh"], lw=0.7)
        ax.axhline(cf.ALPHA, color=M["phu"], ls="--", lw=1, label="α mục tiêu = 0,1")
        ax.set_ylabel("α_t")
        ax.set_xlabel("thời gian (đoạn kiểm)")
        ax.set_title("ACI hạ α_t (nới khoảng) sau chuỗi giờ trượt ra ngoài, nâng lại khi khoảng thừa")
        ax.legend(fontsize=7)
        ve.luu_hinh(fig, HINH / "aci-alpha.png")


if __name__ == "__main__":
    main()
