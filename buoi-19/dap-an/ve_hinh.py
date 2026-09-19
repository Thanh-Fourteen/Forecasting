# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 19 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

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
spec = importlib.util.spec_from_file_location("gd", DAY / "gian_doan.py")
gd = importlib.util.module_from_spec(spec)
sys.modules["gd"] = gd
spec.loader.exec_module(gd)
M = ve.MAU


def hinh_phan_loai(Y) -> dict:
    hoc = Y.iloc[:, :gd.SO_THANG - gd.SO_KY_CHAM - 1]
    pl = gd.bang_phan_loai(hoc)
    mau = {"mượt": M["ba"], "thất thường": M["vang"], "gián đoạn": M["chinh"], "cục": M["phu"]}
    fig, ax = plt.subplots(figsize=(8, 4.6))
    rng = np.random.default_rng(0)
    for loai, c in mau.items():
        d = pl[pl["loại"] == loai]
        ax.scatter(d["ADI"] * np.exp(rng.normal(0, 0.02, len(d))), d["CV2"] + rng.normal(0, 0.005, len(d)),
                   s=5, alpha=0.4, color=c, label=f"{loai}: {len(d)}")
    ax.axvline(1.32, color="black", linestyle="--", linewidth=0.8)
    ax.axhline(0.49, color="black", linestyle="--", linewidth=0.8)
    ax.set_xscale("log")
    ax.set_xticks([1, 1.32, 2, 5, 10, 20, 38])
    ax.set_xticklabels(["1", "1,32", "2", "5", "10", "20", "38"])
    ax.set_xlabel("ADI = số tháng / số tháng có bán (thang log)")
    ax.set_ylabel("CV² của lượng bán khi có bán")
    ax.set_ylim(-0.05, 2)
    ax.legend(markerscale=3, fontsize=8, loc="upper right")
    ax.set_title("2.549 mã phụ tùng bán ít nhất 2 lần trong 38 tháng đầu: gần hết là 'gián đoạn'",
                 fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "phan-loai.png")
    ra = pl["loại"].value_counts().to_dict()
    ra["ADI trung vị"] = float(pl["ADI"].median())
    ra["CV2 trung vị"] = float(pl["CV2"].median())
    return ra


def _chuoi_ngung_ban(Y):
    for uid, v in Y.iterrows():
        v = v.to_numpy()
        if (v[:24] > 0).sum() >= 8 and v[30:].sum() == 0:
            return uid, v
    raise ValueError("không có chuỗi ngừng bán")


def hinh_croston_tsb(Y) -> dict:
    uid, v = _chuoi_ngung_ban(Y)
    t = np.arange(6, len(v) + 1)
    cr = [gd.croston(v[:k]) for k in t]
    ts = [gd.tsb(v[:k]) for k in t]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.bar(np.arange(len(v)), v, color=M["xam"], alpha=0.6, label="bán thật")
    ax.plot(t, cr, color=M["phu"], label="Croston")
    ax.plot(t, ts, color=M["chinh"], label="TSB")
    ax.set_xlabel("tháng (0 = 1/1998)")
    ax.set_ylabel("món mỗi tháng")
    ax.legend(fontsize=8)
    cuoi = int(np.flatnonzero(v > 0)[-1])
    ax.set_title(f"Mã {uid} ngừng bán sau tháng {cuoi}: TSB giảm dần về 0, Croston giữ nguyên",
                 fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "croston-tsb.png")
    return {"mã": uid, "lần bán cuối": cuoi, "Croston tháng 50": cr[-1], "TSB tháng 50": ts[-1], "Croston tháng 25": cr[25 - 6],
            "TSB tháng 25": ts[25 - 6], "lần bán 24 tháng đầu": int((v[:24] > 0).sum())}


def hinh_rmsse_chi_phi(bang) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.6))
    for m, d in bang.iterrows():
        c = M["phu"] if m in ("Zero", "Naive", "SeasonalNaive") else M["chinh"]
        ax.scatter(d["RMSSE"], d["chi phí mỗi mã"], color=c, s=25)
        ax.annotate(m, (d["RMSSE"], d["chi phí mỗi mã"]), fontsize=8, xytext=(4, -10 if m == "ADIDA" else 3),
                    textcoords="offset points")
    ax.set_xlabel("RMSSE (trái = tốt)")
    ax.set_ylabel("chi phí tồn kho mô phỏng mỗi mã, 12 tháng (dưới = tốt)")
    ax.set_title("RMSSE xếp 'Zero' (không nhập hàng) hơn AutoETS; chi phí thì ngược lại",
                 fontsize=10, fontweight="bold")
    ve.luu_hinh(fig, HINH / "rmsse-chi-phi.png")


def hinh_adida(Y) -> dict:
    def hop(v):
        return 12 <= (v == 0).sum() <= 16 and (v.reshape(-1, 3).sum(axis=1) == 0).sum() <= 1

    uid = next(u for u, h in Y.iterrows() if hop(h.to_numpy()[:24]))
    v = Y.loc[uid].to_numpy()[:24]
    gop = v.reshape(-1, 3).sum(axis=1)
    fig, a = plt.subplots(1, 2, figsize=(10, 3.2), sharey=False)
    a[0].bar(np.arange(24), v, color=M["chinh"])
    a[0].set_title(f"theo tháng: {int((v == 0).sum())}/24 tháng bằng 0", fontsize=9)
    a[0].set_xlabel("tháng")
    a[1].bar(np.arange(8), gop, color=M["ba"])
    a[1].set_title(f"cộng mỗi 3 tháng: {int((gop == 0).sum())}/8 quý bằng 0", fontsize=9)
    a[1].set_xlabel("quý")
    a[0].set_ylabel("món")
    fig.suptitle(f"Mã {uid}: gộp 3 tháng làm số 0 gần như biến mất (ý tưởng của ADIDA)", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "gop-thoi-gian.png")
    return {"thang 0": int((v == 0).sum()), "quy 0": int((gop == 0).sum()), "v": v.tolist(), "gop": gop.tolist()}


if __name__ == "__main__":
    df = gd.doc_car_parts()
    Y = gd.ma_tran(df)
    print("tỷ lệ tháng bằng 0:", round(float((Y == 0).to_numpy().mean()), 4))
    print("phân loại:", hinh_phan_loai(Y))
    print("croston/tsb:", hinh_croston_tsb(Y))
    print("gộp:", hinh_adida(Y))
    kq = gd.backtest_car_parts(df, luu=True)
    dg = gd.danh_gia(kq, Y)
    print("bỏ:", dg.attrs)
    bang = dg.join(gd.chi_phi_ton_kho(kq, Y))
    print(bang.round(3).to_string())
    hinh_rmsse_chi_phi(bang)
