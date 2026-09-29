# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_04.py (bảng HINH) — không sửa tay.
# Hình minh hoạ khái niệm (dữ liệu tự tạo, có seed) → ../hinh/kn-*.png, dùng trong tai-lieu.md và tu-hoc.ipynb.
# Chạy: python ve_hinh_khai_niem.py   (cần numpy, pandas, matplotlib)
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HINH = Path(__file__).resolve().parent.parent / "hinh"
VE = {
    'kn-chu-ky.png': r'''fig, truc = plt.subplots(3, 1, figsize=(5.2, 2.8), sharex=True)
t = np.arange(120)
truc[0].plot(t, 10 + 0.08 * t + np.random.default_rng(0).normal(0, 0.4, t.size))
truc[1].plot(t, np.sin(2 * np.pi * t / 12))
for k in range(0, 120, 12):
    truc[1].axvline(k, color="0.85", lw=0.6)
do_dai = [22, 40, 18, 40]                         # mỗi đợt lên–xuống dài một khác
pha = np.concatenate([np.linspace(0, 2 * np.pi, d, endpoint=False) for d in do_dai])
truc[2].plot(t, np.sin(pha[:120]))
for ax, ten in zip(truc, ["xu hướng", "mùa vụ (12 bước)", "chu kỳ (dài ngắn khác nhau)"]):
    ax.set(yticks=[], ylabel=ten)
    ax.yaxis.label.set(rotation=0, ha="right", va="center", fontsize=7)
truc[0].set_title("Mùa vụ lặp sau số bước cố định; chu kỳ thì không")
truc[2].set_xlabel("thời gian")
''',
    'kn-lam-tron-trung-binh-truot.png': r'''y = pd.Series([50, 52, 48, 2, 51, 49, 50], index=range(1, 8))
ax.plot(y, "o-", color="0.6", label="dữ liệu")
ax.plot(y.rolling(3, center=True).mean(), "s-", label="trung bình 3 ngày")
ax.plot(4, y.mean(), "D", color="tab:red", label="trung bình 7 ngày (ngày 4)")
ax.set(ylim=(0, 60), xlabel="ngày", ylabel="trăm lượt", title="Cửa sổ càng rộng, ngày bất thường càng mờ")
ax.legend(fontsize=6, loc="lower right")
''',
    'kn-thang-log.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.0))
y = [100, 200, 400, 500]
for ax, ten in ((a, "thang thường: +100, +200, +100"), (b, "thang log: ×2, ×2, ×1,25")):
    ax.plot(range(4), y, "o-")
    ax.set(title=ten, xticks=range(4))
    ax.title.set_fontsize(7)
b.set_yscale("log")
b.set_yticks(y, [str(v) for v in y])
b.minorticks_off()
''',
    'kn-subseries-plot.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 2.0), sharey=True)
thu = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
t1 = np.array([10, 12, 12, 12, 14, 6, 4])
t2 = t1 + 2
a.plot(thu, t1, "o-", label="tuần 1")
a.plot(thu, t2, "o-", label="tuần 2")
a.set(title="seasonal plot: chồng các tuần", ylabel="trăm lượt / ngày", ylim=(0, 18))
a.legend(fontsize=6)
for i in range(7):
    b.plot([i - 0.2, i + 0.2], [t1[i], t2[i]], "o-", color="tab:blue")
    b.hlines((t1[i] + t2[i]) / 2, i - 0.3, i + 0.3, color="tab:orange")
b.set(title="subseries plot: mỗi thứ một ô", xticks=range(7), xticklabels=thu)
for ax in (a, b):
    ax.title.set_fontsize(7)
''',
    'kn-mua-vu-kep.png': r'''g = np.arange(24)
lam = 60 + 400 * np.exp(-(g - 8) ** 2 / 2) + 480 * np.exp(-(g - 17) ** 2 / 3)
nghi = 40 + 330 * np.exp(-(g - 13.5) ** 2 / 12)
y = np.concatenate([lam] * 5 + [nghi] * 2)
ax.plot(np.arange(168), y)
ax.set_xticks(range(0, 168, 24), ["T2", "T3", "T4", "T5", "T6", "T7", "CN"])
ax.set(ylim=(0, None), ylabel="lượt / giờ", title="Nhịp ngày (24 giờ) lồng trong nhịp tuần (168 giờ)")
''',
    'kn-boxplot.png': r'''x = np.array([420, 60, 450, 410, 440])
ax.boxplot(x, orientation="horizontal", widths=0.4, whis=1.5, medianprops={"color": "tab:orange", "lw": 2})
ax.plot(x, np.full(5, 1.4), "o", color="tab:blue", ms=4)
for v, ten, xt, yt in [(410, "Q 0,25 = 410", 300, 0.62), (420, "trung vị 420", 330, 1.6), (440, "Q 0,75 = 440", 470, 0.62)]:
    ax.annotate(ten, (v, 1.2 if yt > 1 else 0.8), xytext=(xt, yt), fontsize=6, ha="center",
                arrowprops={"arrowstyle": "-", "lw": 0.5})
ax.annotate("ngày lễ 60: điểm lẻ", (60, 1.12), ha="left", fontsize=6)
ax.set(yticks=[], ylim=(0.5, 1.75), xlim=(40, 520), xlabel="lượt lúc 8h", title="Hộp = nửa giữa của số liệu; điểm lẻ nằm ngoài râu")
''',
    'kn-lag-plot.png': r'''y = np.array([2, 4, 6, 4, 2, 4, 6, 4])
ax.scatter(y[:-2], y[2:], s=40)
for (a, b), n in {(2, 6): 2, (4, 4): 3, (6, 2): 1}.items():
    ax.annotate(f"{n} cặp", (a, b), xytext=(6, 4), textcoords="offset points", fontsize=6)
ax.plot([1, 7], [1, 7], color="tab:orange", lw=0.8, label="y lúc t = y lúc t − 2")
ax.set(xlabel="y lúc t − 2", ylabel="y lúc t", xlim=(1, 7), ylim=(1, 7), title="Trễ nửa vòng: cao thì 2 bước sau thấp")
ax.set_aspect("equal")
ax.legend(fontsize=6)
''',
    'kn-acf.png': r'''y = np.array([2, 4, 6, 4, 2, 4, 6, 4], dtype=float)
lech = y - y.mean()
r = [np.sum(lech[k:] * lech[:len(y) - k]) / np.sum(lech**2) for k in range(1, 7)]
ax.vlines(range(1, 7), 0, r, lw=4)
ax.axhline(0, color="0.5", lw=0.6)
ax.set(xlabel="độ trễ k", ylabel="r_k", ylim=(-1, 1), title="Âm ở nửa vòng, dương ở một vòng")
''',
    'kn-truc-y-cat.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.0))
for ax, day, ten in ((a, 480, "trục từ 480: 'gấp ba'"), (b, 0, "trục từ 0: +4%")):
    ax.bar(["T5", "T6"], [490, 510], color=["0.6", "tab:blue"])
    ax.set(ylim=(day, 520), title=ten)
    ax.title.set_fontsize(8)
a.set_ylabel("triệu đồng")
''',
}

plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
for ten_tep, code in VE.items():
    fig, ax = plt.subplots(figsize=(5.2, 2.1))
    ns = {"np": np, "pd": pd, "plt": plt, "fig": fig, "ax": ax}
    exec(code, ns)
    if ns["fig"] is not fig:
        plt.close(fig)
    ns["fig"].savefig(HINH / ten_tep, dpi=150, bbox_inches="tight")
    plt.close("all")
    print("vẽ", ten_tep)
