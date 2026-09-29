# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_07.py (bảng HINH) — không sửa tay.
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
    'kn-pacf.png': r'''k = np.arange(1, 9)
ax.bar(k - 0.18, 0.7**k, width=0.35, label="ACF: 0,7^k")
ax.bar(k + 0.18, np.where(k == 1, 0.7, 0), width=0.35, color="tab:orange", label="PACF")
ax.set(xlabel="độ trễ k", ylabel="hệ số", xticks=k, ylim=(0, 0.8),
       title="AR(1): ACF giảm dần, PACF chỉ còn trễ 1")
ax.legend(fontsize=7)
''',
    'kn-ljung-box.png': r'''from scipy import stats
x = np.linspace(0, 12, 400)
f = stats.chi2.pdf(x, 2)
ax.plot(x, f)
ax.fill_between(x, f, where=x >= 5.99, color="tab:red", alpha=0.4, label="5% lớn nhất (từ 5,99)")
ax.axvline(5.16, color="tab:blue", ls="--", label="Q* = 5,16")
ax.set(xlabel="Q*", yticks=[], title="Q* chưa vào vùng 5% lớn nhất: chưa đủ bằng chứng")
ax.legend(fontsize=7)
''',
    'kn-dung.png': r'''fig, truc = plt.subplots(3, 1, figsize=(5.2, 2.6), sharex=True)
e = np.random.default_rng(1).normal(size=300)
for ax, y, ten in zip(truc, [25 + 0.5 * e, 0.05 * np.arange(300) + e, e.cumsum()],
                      ["dừng", "dừng quanh\nxu hướng", "random walk"]):
    ax.plot(y, lw=0.8)
    ax.set_yticks([])
    ax.set_ylabel(ten, rotation=0, ha="right", va="center", fontsize=7)
truc[0].set_title("Có mức để quay về, có đường để bám theo, hay không có gì")
truc[-1].set_xlabel("t")
''',
    'kn-random-walk.png': r'''buoc = np.random.default_rng(7).choice([-1, 1], size=(40, 100)).cumsum(axis=1)
t = np.arange(1, 101)
ax.plot(t, buoc.T, color="0.6", lw=0.5)
ax.plot(t, np.sqrt(t), "--", color="tab:orange")
ax.plot(t, -np.sqrt(t), "--", color="tab:orange")
ax.set(xlabel="số bước", ylabel="vị trí", title="Càng đi lâu càng có thể xa: độ dao động tăng theo thời gian")
''',
    'kn-adf-kpss.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 2.1), sharey=True)
e = np.random.default_rng(3).normal(size=300)
ar = np.zeros(300)
for t in range(1, 300):
    ar[t] = 0.7 * ar[t - 1] + e[t]
for ax, y, ten in ((a, ar, "dừng (ρ = 0,7): cao thì bị kéo xuống"), (b, e.cumsum(), "random walk: độ cao không nói gì")):
    muc = y[:-1] - y[:-1].mean()
    ax.scatter(muc, np.diff(y), s=4, alpha=0.5)
    he_so = np.polyfit(muc, np.diff(y), 1)
    g = np.linspace(muc.min(), muc.max(), 2)
    ax.plot(g, np.polyval(he_so, g), color="tab:orange")
    ax.set(title=ten, xlabel="độ cao hiện tại − mức TB")
    ax.title.set_fontsize(7)
a.set_ylabel("bước kế tiếp")
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
