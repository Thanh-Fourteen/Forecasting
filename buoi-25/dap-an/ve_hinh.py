# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 25 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (khoảng 1 phút)

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
spec = importlib.util.spec_from_file_location("xs", DAY / "xac_suat.py")
xs = importlib.util.module_from_spec(spec)
sys.modules["xs"] = xs
spec.loader.exec_module(xs)


def vi_du_tay() -> None:
    """Các ví dụ số nhỏ tính tay trong tài liệu."""
    y = np.arange(1, 11)
    for q in (7, 8, 8.5, 9):
        print(f"pinball τ=0,8, q={q}: tổng {sum(xs.pinball([v], [q], 0.8) for v in y):.2f}")
    print("CRPS mẫu (2,4,6), y=5:", round(xs.crps_mau([5], [[2, 4, 6]]), 4), "| MAE mẫu:", 5 / 3)
    print("CRPS một số 4, y=5:", xs.crps_mau([5], [[4]]))
    print("WIS trung vị 8, khoảng 80% [5, 9], y=10:", xs.wis([10], np.array([[5.0, 8, 9]]), (0.1, 0.5, 0.9)))
    kq = {"nguong": 39.0, "sigma": 1.4, "xi": 0.0, "dot_moi_nam": 1.0}
    print("mức 10 năm, ξ = 0:", round(xs.muc_lap_lai(kq, 10), 2))


def main() -> None:
    vi_du_tay()
    df = xs.doc_dien()
    R = xs.backtest(df)
    Rg = xs.backtest(df, tru_muc=False)
    T = (R["ds"] >= xs.NAM_KIEM).to_numpy()
    y = R["y"].to_numpy()[T]
    print("số giờ 2025:", T.sum(), "| MAE LightGBM:", round(float(np.abs(y - R["yhat"].to_numpy()[T]).mean())),
          "| MAE seasonal naive:", round(float(np.nanmean(np.abs(
              y - df.set_index("ds")["y"].shift(168).reindex(R["ds"]).to_numpy()[T])))))
    print("sd phần dư trên phần học (trung bình các tháng):", round(float(R["sd_trong"][T].mean())),
          "| sd phần dư ngoài mẫu 2025:", round(float(np.std(y - R["yhat"].to_numpy()[T]))))
    Qraw = xs.ma_tran_quantile(R)[T]
    print("tỷ lệ giờ có crossing (thô):", round(float((np.diff(Qraw, axis=1) < 0).any(axis=1).mean()), 3))
    mo_hinh = {
        "trong mẫu, giả định chuẩn": xs.quantile_trong_mau_chuan(R)[T],
        "mượn khoảng seasonal naive": xs.quantile_muon_seasonal_naive(R, df)[T],
        "không trừ mức": xs.du_bao_quantile(Rg)[(Rg["ds"] >= xs.NAM_KIEM).to_numpy()],
        "phần dư ngoài mẫu": xs.quantile_tu_phan_du(R)[T],
        "LightGBM quantile (đã sắp)": xs.du_bao_quantile(R)[T],
    }
    S = xs.mau_tu_phan_du(R)[T]
    print("CRPS phần dư ngoài mẫu (200 mẫu):", round(xs.crps_mau(y, S)))
    for ten, Q in mo_hinh.items():
        print(f"{ten:28s} tỷ lệ dưới {xs.ty_le_duoi(y, Q).round(3)} | cov80 {xs.coverage(y, Q[:, 1], Q[:, 7]):.3f}"
              f" cov90 {xs.coverage(y, Q[:, 0], Q[:, 8]):.3f} | WIS {xs.wis(y, Q):.0f} | rộng 90% "
              f"{np.mean(Q[:, 8] - Q[:, 0]):.0f} | PIT {xs.pit_tu_quantile(y, Q)[1].round(2)}")

    with ve.phong_cach():
        # 1. quạt dự báo một tuần nóng
        tuan = (R["ds"] >= "2025-08-11") & (R["ds"] < "2025-08-18")
        fig, axs = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
        for ax, (ten, Q) in zip(axs, [("trong mẫu, giả định chuẩn", xs.quantile_trong_mau_chuan(R)),
                                      ("phần dư ngoài mẫu", xs.quantile_tu_phan_du(R))], strict=True):
            Qt = Q[tuan.to_numpy()] / 1000
            x = R["ds"][tuan]
            ax.fill_between(x, Qt[:, 0], Qt[:, 8], color=M["chinh"], alpha=0.25, lw=0, label="khoảng 90%")
            ax.fill_between(x, Qt[:, 1], Qt[:, 7], color=M["chinh"], alpha=0.45, lw=0, label="khoảng 80%")
            ax.plot(x, R["y"][tuan] / 1000, color="black", lw=1, label="thực tế")
            ra = (R["y"][tuan].to_numpy() / 1000 < Qt[:, 0]) | (R["y"][tuan].to_numpy() / 1000 > Qt[:, 8])
            ax.scatter(x[ra], R["y"][tuan][ra] / 1000, color=M["phu"], s=10, zorder=3, label="ra ngoài khoảng 90%")
            ax.set_title(f"{ten}: {ra.sum()} / {len(ra)} giờ ra ngoài")
            ax.set_xlabel("ngày (8/2025, giờ UTC)")
            ax.tick_params(axis="x", labelrotation=30)
        axs[0].set_ylabel("nhu cầu (nghìn MW)")
        axs[0].legend(fontsize=7, loc="upper left")
        fig.suptitle("Khoảng từ phần dư trên phần học hẹp hơn sai số thật; phần dư ngoài mẫu vừa đúng", fontweight="bold",
                     y=1.03)
        ve.luu_hinh(fig, HINH / "khoang-trong-ngoai-mau.png")

        # 2. PIT của bốn mô hình
        chon = ["trong mẫu, giả định chuẩn", "mượn khoảng seasonal naive", "không trừ mức", "phần dư ngoài mẫu"]
        nhan = ["quá tự tin (chữ U)", "quá thận trọng (vòm)", "lệch: dự báo thấp (dốc lên)", "calibrate (phẳng)"]
        fig, axs = plt.subplots(1, 4, figsize=(12, 2.9), sharey=True)
        for ax, ten, nh in zip(axs, chon, nhan, strict=True):
            mep, h = xs.pit_tu_quantile(y, mo_hinh[ten])
            ax.bar(mep[:-1], h, width=np.diff(mep), align="edge", color=M["chinh"], alpha=0.8, edgecolor="white")
            ax.axhline(1, color=M["phu"], ls="--", lw=1)
            ax.set_title(f"{ten}\n{nh}", fontsize=8)
            ax.set_xlabel("PIT (mức quantile)")
            ax.set_xlim(0, 1)
        axs[0].set_ylabel("số giờ ÷ số kỳ vọng")
        fig.suptitle(f"PIT histogram: hình dạng cho biết lỗi calibration (2025, {len(y):,} giờ)".replace(",", "."), fontweight="bold",
                     y=1.08)
        ve.luu_hinh(fig, HINH / "pit-bon-mo-hinh.png")

        # 3. reliability diagram cho quantile
        fig, ax = plt.subplots(figsize=(4.6, 4.2))
        ax.plot([0, 1], [0, 1], color=M["xam"], ls="--", lw=1, label="lý tưởng")
        for ten, mau in zip(chon, [M["phu"], M["ba"], M["bon"], M["chinh"]], strict=True):
            ax.plot(xs.MUC, xs.ty_le_duoi(y, mo_hinh[ten]), "o-", color=mau, ms=3, label=ten)
        ax.set_xlabel("mức quantile danh nghĩa")
        ax.set_ylabel("tỷ lệ giờ thực tế nằm dưới quantile")
        ax.set_title("Reliability: chỉ phần dư ngoài mẫu\nbám đường chéo")
        ax.legend(fontsize=7)
        ve.luu_hinh(fig, HINH / "reliability.png")

        # 4. POT nhiệt độ tối đa Dallas
        t = xs.doc_nhiet_do_toi_da()
        kq = xs.pot(t, 39.0)
        print("POT:", {k: round(v, 3) for k, v in kq.items()},
              {n: round(xs.muc_lap_lai(kq, n), 2) for n in (2, 10, 50, 100)})
        nam_max = t.groupby(t.index.year).max()
        print("số năm có max > mức 10 năm:", int((nam_max > xs.muc_lap_lai(kq, 10)).sum()), "/", len(nam_max),
              "| max quan sát:", t.max(), t.idxmax().date())
        for u in (38.0, 40.0):
            k2 = xs.pot(t, u)
            print(f"ngưỡng {u}: {k2['so_dot']} đợt, ξ {k2['xi']:.3f}, mức 10 năm {xs.muc_lap_lai(k2, 10):.2f}")
        # chỉ 2 năm tải
        tai = df.set_index("ds")["y"]
        tai.index = tai.index.tz_localize("UTC").tz_convert("America/Chicago").tz_localize(None)
        dinh = tai.resample("D").max().loc["2024-01-01":"2025-12-31"].dropna()
        k3 = xs.pot(dinh, float(dinh.quantile(0.95)))
        print("POT trên 2 năm tải đỉnh:", {k: round(v, 3) for k, v in k3.items()})
        # tải đỉnh theo nhiệt độ những ngày ≥ 32 °C, ngày thường
        b = pd.DataFrame({"tai": dinh, "t": t}).dropna()
        for nam in (2024, 2025):
            s = b[(b.index.year == nam) & (b["t"] >= 32) & (b.index.dayofweek < 5)]
            k, c = np.polyfit(s["t"], s["tai"], 1)
            print(f"{nam}: {len(s)} ngày, {k:.0f} MW/°C, tải ở {xs.muc_lap_lai(kq, 10):.1f} °C ≈ "
                  f"{k * xs.muc_lap_lai(kq, 10) + c:.0f} MW, tải đỉnh năm {s['tai'].max():.0f}")

        muc_n = np.array([1, 1.5, 2, 3, 5, 10, 20, 50, 100])
        fig, ax = plt.subplots(figsize=(6, 3.6))
        ax.plot(muc_n, [xs.muc_lap_lai(kq, n) for n in muc_n], color=M["chinh"], label="GPD, ngưỡng 39 °C")
        so_nam = (t.index.max() - t.index.min()).days / 365.25
        xep = np.sort(xs.cum_vuot(t, 39.0))[::-1]
        chu_ky = so_nam / np.arange(1, len(xep) + 1)
        ax.scatter(chu_ky, xep, s=9, color=M["phu"], label="đỉnh từng đợt > 39 °C (chu kỳ = số năm ÷ hạng)")
        ax.axhline(xs.muc_lap_lai(kq, 10), color=M["xam"], ls=":", lw=1)
        ax.set_xscale("log")
        ax.set_xlabel("chu kỳ lặp lại (năm, thang log)")
        ax.set_ylabel("nhiệt độ tối đa ngày (°C)")
        ax.set_title(f"Mức 10 năm ≈ {xs.muc_lap_lai(kq, 10):.1f} °C; đuôi có trần (ξ < 0)")
        ax.legend(fontsize=7)
        ve.luu_hinh(fig, HINH / "pot-nhiet-do.png")


if __name__ == "__main__":
    main()
