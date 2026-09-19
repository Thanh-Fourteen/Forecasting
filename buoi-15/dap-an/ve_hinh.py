# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 15 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

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
spec = importlib.util.spec_from_file_location("bt", DAY / "backtest.py")
bt = importlib.util.module_from_spec(spec)
sys.modules["bt"] = bt
spec.loader.exec_module(bt)
M = ve.MAU


def hinh_ba_cach_chia() -> None:
    """Sơ đồ: chia ngẫu nhiên, hold-out một lần, rolling origin (expanding)."""
    n = 40
    rng = np.random.default_rng(1)
    fig, (a, b, c) = plt.subplots(3, 1, figsize=(10, 4.6), gridspec_kw={"height_ratios": [1, 1, 3]})
    kiem = rng.choice(n, 8, replace=False)
    mau = np.where(np.isin(np.arange(n), kiem), M["phu"], M["chinh"])
    a.scatter(np.arange(n), np.zeros(n), c=mau, s=40)
    a.set_title("chia ngẫu nhiên: điểm kiểm (cam) nằm xen giữa điểm học (xanh)", fontsize=9)
    b.scatter(np.arange(n), np.zeros(n), c=[M["chinh"]] * 32 + [M["phu"]] * 8, s=40)
    b.set_title("hold-out: một điểm cắt, kiểm một lần", fontsize=9)
    for k in range(5):
        cutoff = 19 + 4 * k
        c.scatter(np.arange(cutoff + 1), np.full(cutoff + 1, -k), color=M["chinh"], s=30)
        c.scatter(np.arange(cutoff + 1, cutoff + 5), np.full(4, -k), color=M["phu"], s=30)
        c.scatter(np.arange(cutoff + 5, n), np.full(n - cutoff - 5, -k), color="#DDDDDD", s=30)
    c.set_title("rolling origin: 5 cửa sổ, mỗi cửa sổ học trên quá khứ rồi kiểm 4 bước kế tiếp (xám: chưa dùng)",
                fontsize=9)
    for ax in (a, b, c):
        ax.set_yticks([])
        ax.set_xlim(-1, n)
    c.set_xlabel("thời gian (bước)")
    fig.suptitle("Ba cách chia: chỉ rolling origin vừa giữ thứ tự thời gian vừa kiểm nhiều lần",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ba-cach-chia.png")


def hinh_uoc_luong(bang: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 3.4))
    cot = ["K-fold xáo trộn", "rolling origin", "hold-out thật"]
    x = np.arange(len(bang))
    for i, (c, m) in enumerate(zip(cot, (M["phu"], M["chinh"], "black"), strict=True)):
        v = bang[c].to_numpy()
        ax.bar(x + (i - 1) * 0.27, v, width=0.25, color=m, label=c)
        for xi, vi in zip(x, v, strict=True):
            ax.text(xi + (i - 1) * 0.27, vi + 30, f"{vi:,.0f}".replace(",", "."), ha="center", fontsize=8)
    ax.set_xticks(x, bang["mô hình"])
    ax.set_ylabel("MAE (MW)")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("K-fold xáo trộn hứa sai số thấp hơn hold-out 23% với rừng ngẫu nhiên; rolling origin lệch 9%")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "uoc-luong-sai-so.png")


def hinh_cua_so_va_h(rs: dict, theo_h: pd.Series, ho_rung: float) -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.5))
    tcs = rs["theo cửa sổ"]
    a.plot(tcs.index, tcs["rừng"], marker="o", markersize=3, color=M["chinh"], label="rừng ngẫu nhiên")
    a.plot(tcs.index, tcs["seasonal naive"], marker="o", markersize=3, color=M["phu"], label="seasonal naive")
    a.axhline(ho_rung, color="black", linestyle="--", linewidth=0.9, label="rừng, hold-out thật")
    a.set_ylabel("MAE một cửa sổ (MW)")
    a.set_xlabel("cutoff (tháng 9/2024)")
    a.tick_params(axis="x", labelsize=7, rotation=30)
    a.legend(fontsize=7)
    a.set_title("28 cửa sổ 24 giờ: một cửa sổ là một lần may rủi", fontsize=9)
    b.plot(theo_h.index, theo_h.to_numpy(), color=M["ba"], marker=".", markersize=4)
    b.set_xlabel("bước h (giờ sau cutoff)")
    b.set_ylabel("MASE trung bình")
    b.set_title("seasonal naive, 245 chuỗi M4 theo giờ, 3 cửa sổ 48 giờ", fontsize=9)
    fig.suptitle("Sai số đổi theo cửa sổ và theo tầm h: báo cả phân bố, không chỉ một con số",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "sai-so-cua-so-va-h.png")


def hinh_chon_bao_cao(dung: pd.DataFrame, sai: pd.DataFrame) -> dict:
    fig, ax = plt.subplots(figsize=(8.5, 3.2))
    nhom = [("chọn và báo cáo\ncùng đoạn cuối", sai["MASE báo cáo (B)"], M["phu"]),
            ("chọn trên đoạn A,\nbáo cáo trên đoạn B", dung["MASE báo cáo (B)"], M["chinh"]),
            ("seasonal naive 24\ntrên đoạn B", dung["seasonal naive 24 (B)"], M["xam"])]
    tv_ = [float(np.median(v)) for _, v, _ in nhom]
    ax.bar(range(3), tv_, color=[m for *_, m in nhom])
    for i, v in enumerate(tv_):
        ax.text(i, v + 0.02, f"{v:.3f}".replace(".", ","), ha="center", fontsize=9)
    ax.set_xticks(range(3), [n for n, *_ in nhom], fontsize=8)
    ax.set_ylabel("MASE trung vị, 414 chuỗi")
    ax.axhline(1, color="black", linewidth=0.6)
    ax.set_title("Chọn phương pháp trên chính đoạn báo cáo: MASE trông tốt hơn 25% so với thật")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "chon-bao-cao.png")
    return {"cùng đoạn": tv_[0], "ba tập": tv_[1], "snaive B": tv_[2]}


def hinh_dm(kq: dict) -> dict:
    d = np.abs(kq["e_tron"]) - np.abs(kq["e_sn"])
    r = ve.acf(d, 48)
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.3))
    ngay = d[: len(d) // 24 * 24].reshape(-1, 24).mean(axis=1)
    a.bar(np.arange(len(ngay)), ngay, color=np.where(ngay < 0, M["ba"], M["phu"]))
    a.axhline(d.mean(), color="black", linestyle="--", linewidth=0.9)
    a.set_xlabel("ngày của hold-out (1/10 → 31/12/2024)")
    a.set_ylabel("chênh |sai số|, trung bình ngày (MW)")
    a.set_title(f"'trộn' trừ seasonal naive: âm là trộn tốt hơn (trung bình {d.mean():.0f})", fontsize=9)
    b.vlines(range(1, 49), 0, r[1:], color=M["chinh"])
    b.axhline(1.96 / np.sqrt(len(d)), color=M["phu"], linestyle="--", linewidth=0.8)
    b.axhline(-1.96 / np.sqrt(len(d)), color=M["phu"], linestyle="--", linewidth=0.8)
    b.set_xlabel("trễ (giờ)")
    b.set_title(f"ACF của chênh lệch từng giờ: {r[1]:.2f} ở trễ 1".replace(".", ","), fontsize=9)
    fig.suptitle("Chênh lệch giờ này kéo theo giờ sau: DM bỏ qua điều đó thì p nhỏ giả tạo",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "dm-tu-tuong-quan.png")
    return {"acf trễ 1, 12, 24": [round(float(r[k]), 2) for k in (1, 12, 24)],
            "số ngày trộn thắng": int((ngay < 0).sum()), "số ngày": len(ngay)}


if __name__ == "__main__":
    y = bt.doc_dien()
    bang = bt.so_sanh_cach_chia(y)
    print(bang.round(1).to_string(index=False))
    rs = bt.rung_so_voi_snaive(y)
    print({k: v for k, v in rs.items() if k not in ("kq", "theo cửa sổ")})
    print(rs["theo cửa sổ"].describe().round(0))
    kiem = y[y.index >= bt.MOC_HOLD_OUT].index
    truoc = y[(y.index < bt.MOC_HOLD_OUT) & (y.index >= bt.MOC_HOLD_OUT - pd.Timedelta("91D"))].index
    w_sai, w_dung = bt.tune_w(y, kiem), bt.tune_w(y, truoc)
    kq = bt.so_sanh_tron_voi_snaive(y, w_sai)
    print("w tune trên hold-out", w_sai, "| w tune trên 3 tháng trước", w_dung)
    print({k: v for k, v in kq.items() if not k.startswith("e_")})
    chuoi = bt.doc_m4_gio()
    dung, sai = bt.chon_va_bao_cao(chuoi), bt.chon_va_bao_cao_cung_cua_so(chuoi)
    print("chọn (ba tập):", dung["chọn"].value_counts().to_dict())
    print("chọn (cùng đoạn):", sai["chọn"].value_counts().to_dict())
    print("trung vị A:", round(float(dung["MASE lúc chọn (A)"].median()), 3))
    df = bt.m4_dang_dai(chuoi)
    kq_m4 = bt.backtest(df, bt.seasonal_naive, h=bt.H_M4, so_cua_so=3)
    dau = kq_m4["cutoff"].min()
    thang = df[df["ds"] <= dau].groupby("unique_id")["y"].apply(lambda s: float(np.mean(np.abs(s.to_numpy()[24:] - s.to_numpy()[:-24]))))
    kq_m4 = kq_m4.assign(y=kq_m4["y"] / kq_m4["unique_id"].map(thang),
                         seasonal_naive=kq_m4["seasonal_naive"] / kq_m4["unique_id"].map(thang))
    theo_h = bt.sai_so_theo_h(kq_m4, "seasonal_naive")
    print("MASE theo h: bước 1", round(theo_h.iloc[0], 1), "bước 24", round(theo_h.iloc[23], 1),
          "bước 25", round(theo_h.iloc[24], 1), "bước 48", round(theo_h.iloc[47], 1))
    with ve.phong_cach():
        hinh_ba_cach_chia()
        hinh_uoc_luong(bang)
        hinh_cua_so_va_h(rs, theo_h, float(bang.loc[0, "hold-out thật"]))
        print(hinh_chon_bao_cao(dung, sai))
        print(hinh_dm(kq))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
