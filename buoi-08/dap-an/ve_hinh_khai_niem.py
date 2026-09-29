# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_08.py (bảng HINH) — không sửa tay.
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
    'kn-spearman.png': r'''from scipy import stats
fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 2.1))
for ax, x in ((a, np.arange(1, 6)), (b, np.arange(-2, 3))):
    y = x**2
    ax.plot(x, y, "o-")
    ax.set_title(f"Pearson {round(stats.pearsonr(x, y)[0], 2) + 0:.2f}, Spearman {stats.spearmanr(x, y)[0] + 0:.2f}"
                 .replace(".", ","), fontsize=7)
    ax.set_xlabel("x")
a.set_ylabel("y = x²")
''',
    'kn-durbin-watson.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 1.9), sharey=True)
for ax, e in ((a, np.array([1, 1, 1, -1, -1, -1])), (b, np.array([1, -1, 1, -1, 1, -1]))):
    dw = np.sum(np.diff(e) ** 2) / np.sum(e**2)
    ax.bar(range(1, 7), e, color=np.where(e > 0, "tab:blue", "tab:orange"))
    ax.axhline(0, color="k", lw=0.5)
    ax.set(title=f"DW = {dw:.2f}".replace(".", ","), xlabel="t")
a.set_ylabel("phần dư")
''',
    'kn-cdd-hdd.png': r'''t = np.linspace(-5, 40, 200)
ax.plot(t, np.maximum(t - 18.33, 0), color="tab:red", label="CDD = max(T − 18,33; 0)")
ax.plot(t, np.maximum(18.33 - t, 0), color="tab:blue", label="HDD = max(18,33 − T; 0)")
ax.axvline(18.33, color="0.6", ls="--")
ax.set(xlabel="nhiệt độ T (°C)", ylabel="độ", title="Hai biến, mỗi biến một nhánh: đi xa mốc thì tăng")
ax.legend(fontsize=6)
''',
    'kn-hoan-vi-theo-khoi.png': r'''fig, truc = plt.subplots(3, 1, figsize=(5.2, 2.6), sharex=True)
rng = np.random.default_rng(0)
y = np.zeros(300)
for i in range(1, 300):
    y[i] = 0.97 * y[i - 1] + rng.normal()
khoi = [y[i:i + 50] for i in range(0, 300, 50)]
for ax, v, ten in zip(truc, [y, rng.permutation(y), np.concatenate([khoi[i] for i in rng.permutation(6)])],
                      ["gốc", "xáo từng điểm", "xáo khối 50"]):
    ax.plot(v, lw=0.8)
    ax.set_yticks([])
    ax.set_ylabel(ten, rotation=0, ha="right", va="center", fontsize=7)
truc[2].set_xlabel("t")
truc[0].set_title("Xáo theo khối giữ độ trơn của chuỗi")
''',
    'kn-bien-gay-nhieu.png': r'''ax.set(xlim=(0, 10), ylim=(0, 4.2))
ax.axis("off")
for x, y, ten in [(5, 3.5, "nhịp ngày\n(mặt trời, giờ thức dậy)"), (1.8, 0.7, "nhiệt độ"), (8.2, 0.7, "tải điện")]:
    ax.text(x, y, ten, ha="center", va="center", fontsize=8, bbox={"boxstyle": "round", "fc": "0.92", "ec": "0.5"})
for x in (2.4, 7.6):
    ax.annotate("", (x, 1.1), (5, 2.9), arrowprops={"arrowstyle": "->", "lw": 1.2})
ax.annotate("", (7.3, 0.7), (2.7, 0.7), arrowprops={"arrowstyle": "<->", "ls": "--", "color": "tab:red"})
ax.text(5, 0.25, "tương quan, Granger hai chiều", ha="center", fontsize=7, color="tab:red")
ax.set_title("Biến thứ ba điều khiển cả hai: tương quan không phải nhân quả")
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
