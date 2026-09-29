# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_13.py (bảng HINH) — không sửa tay.
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
    'kn-lag.png': r'''x = np.arange(1, 7)
ax.axvspan(3.5, 6.5, color="tab:red", alpha=0.08)
ax.scatter(x, np.zeros(6), s=14, color="0.5", zorder=3)
ax.scatter([5], [0], s=90, marker="*", color="k", zorder=4)
ax.axvline(3, color="k", lw=0.8, ls="--")
ax.text(2.9, -0.55, "ra dự báo (tối ngày 3)", ha="right", fontsize=7)
ax.text(5, -0.55, "cần dự báo", ha="center", fontsize=7)
for k in (1, 2, 3):
    mau = "tab:red" if 5 - k > 3 else "tab:green"
    ax.annotate("", xy=(5 - k, 0.06), xytext=(5, 0.06),
                arrowprops={"arrowstyle": "->", "color": mau, "connectionstyle": f"arc3,rad={0.25 + 0.12 * k}"})
    ax.text(5 - k - 0.1, 0.2, f"lag_{k}", ha="right", fontsize=7, color=mau)
ax.set(xlim=(0.5, 6.5), ylim=(-0.8, 1.3), xticks=x, yticks=[], xlabel="ngày",
       title="h = 2: lag_1 trỏ vào ngày chưa có, lag nhỏ nhất phải ≥ h")
ax.spines["left"].set_visible(False)
''',
    'kn-rolling.png': r'''ngay = np.arange(1, 7)
cach = [("rolling(3, center=True)", 3, 5), ("rolling(3)", 2, 4), ("shift(1).rolling(3)", 1, 3)]
ax.axvspan(3.5, 6.6, color="tab:red", alpha=0.08)
for i, (ten, dau, cuoi) in enumerate(cach):
    muc = 2 - i
    ax.scatter(ngay, [muc] * 6, s=10, color="0.6", zorder=3)
    ax.plot([dau, cuoi], [muc, muc], lw=7, alpha=0.45, solid_capstyle="round",
            color="tab:red" if cuoi >= 4 else "tab:green")
    ax.text(0.4, muc, ten, ha="right", va="center", fontsize=7, family="monospace")
ax.text(5, 2.55, "chưa có lúc dự báo", ha="center", fontsize=7, color="tab:red")
ax.set(xlim=(-2.6, 6.6), ylim=(-0.6, 2.9), xticks=ngay, yticks=[], xlabel="ngày (cần dự báo ngày 4, h = 1)",
       title="Chỉ cửa sổ kết thúc trước ngày cần dự báo là hợp lệ")
ax.spines["left"].set_visible(False)
''',
    'kn-ma-hoa-tuan-hoan.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.3), gridspec_kw={"width_ratios": [1.4, 1]})
ten = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
so = np.arange(7)
mau = ["tab:red" if i in (0, 6) else "tab:blue" for i in so]
a.scatter(so, np.zeros(7), color=mau, zorder=3)
for i in so:
    a.text(i, 0.18, ten[i], ha="center", fontsize=7)
a.annotate("", xy=(0, -0.3), xytext=(6, -0.3), arrowprops={"arrowstyle": "<->", "color": "tab:red"})
a.text(3, -0.55, "cách 6", ha="center", fontsize=7, color="tab:red")
a.set(xticks=so, yticks=[], ylim=(-0.8, 0.6), xlabel="số thứ tự", title="Số thứ tự: CN cách T2 là 6")
a.spines["left"].set_visible(False)
g = 2 * np.pi * so / 7
b.scatter(np.cos(g), np.sin(g), color=mau, zorder=3)
for i in so:
    b.text(1.3 * np.cos(g[i]), 1.3 * np.sin(g[i]), ten[i], ha="center", va="center", fontsize=7)
b.set(xlim=(-1.6, 1.6), ylim=(-1.6, 1.6), xticks=[-1, 0, 1], yticks=[-1, 0, 1], xlabel="cos", ylabel="sin",
      title="Vòng tròn: 7 ngày cách đều")
b.set_aspect("equal")
''',
    'kn-fourier-term.png': r'''t = np.arange(365)
rng = np.random.default_rng(0)
y = 100 + 10 * np.cos(2 * np.pi * (t - 200) / 365.25) + 25 * np.exp(-(((t - 345) / 10) ** 2)) + rng.normal(0, 3, 365)
ax.plot(t, y, color="0.7", lw=0.6, label="dữ liệu")
for k, mau in ((1, "tab:blue"), (4, "tab:orange")):
    X = np.column_stack([np.ones(365)] + [f(2 * np.pi * i * t / 365.25) for i in range(1, k + 1) for f in (np.sin, np.cos)])
    ax.plot(t, X @ np.linalg.lstsq(X, y, rcond=None)[0], color=mau, lw=1.4, label=f"K = {k} ({2 * k} cột)")
ax.set(xlabel="ngày trong năm", ylabel="doanh thu", ylim=(80, 132), title="Thêm cặp Fourier thì bắt được đỉnh hẹp cuối năm")
ax.legend(fontsize=7, loc="upper center", ncol=3, frameon=False)
''',
    'kn-kiem-nhieu-muc-tieu.png': r'''fig, (a, b) = plt.subplots(2, 1, figsize=(5.2, 2.5), sharex=True, gridspec_kw={"height_ratios": [1.6, 1]})
rng = np.random.default_rng(1)
n, moc, h = 40, 28, 3
y = 10 + np.sin(np.arange(n) / 3) + rng.normal(0, 0.3, n)
y2 = y.copy()
y2[moc:] += rng.normal(0, 3, n - moc)
a.plot(y, color="k", lw=1, label="y gốc")
a.plot(np.arange(moc, n), y2[moc:], color="tab:red", lw=1, label="y cộng nhiễu")
a.legend(fontsize=6, loc="lower left", frameon=False)
a.set_yticks([])
for ax in (a, b):
    ax.axvline(moc - 0.5, color="k", ls="--", lw=0.8)
    ax.axvspan(-0.5, moc + h - 0.5, color="tab:green", alpha=0.08)
s, s2 = pd.Series(y), pd.Series(y2)
for i, k in enumerate((3, 1)):
    doi = np.flatnonzero((s2.shift(k) - s.shift(k)).abs().to_numpy() > 1e-9)
    b.scatter(doi, np.full(doi.size, i), marker="|", s=80, color="tab:red" if k < h else "tab:blue")
b.set(yticks=[0, 1], yticklabels=["lag_3", "lag_1"], ylim=(-0.6, 1.6), xlabel="dòng (thời điểm t)")
a.set_title("h = 3: dòng trong vùng xanh không được đổi — lag_1 đổi nên bị bắt")
''',
    'kn-merge-asof.png': r'''trai, phai = [10, 14, 22], [9, 12, 15]
ax.scatter(trai, [1] * 3, s=30, color="k", zorder=3)
ax.scatter(phai, [0] * 3, s=30, marker="s", color="0.4", zorder=3)
ax.text(7.6, 1, "tải", ha="right", va="center", fontsize=7)
ax.text(7.6, 0, "nhiệt độ", ha="right", va="center", fontsize=7)
for x0, x1 in ((10, 9), (14, 12)):
    ax.annotate("", xy=(x1, 0.08), xytext=(x0, 0.92), arrowprops={"arrowstyle": "->", "color": "tab:green"})
ax.annotate("", xy=(15, 0.08), xytext=(14, 0.92), arrowprops={"arrowstyle": "->", "color": "tab:red", "ls": "--"})
ax.text(15.2, 0.5, "nearest:\ntương lai", fontsize=7, color="tab:red")
ax.annotate("", xy=(15.3, 0.08), xytext=(22, 0.92), arrowprops={"arrowstyle": "->", "color": "0.6", "ls": ":"})
ax.text(19.5, 0.3, "cách 7 giờ > tolerance\n→ để trống", fontsize=7, color="0.4")
ax.set(xlim=(5.5, 24), ylim=(-0.4, 1.4), xticks=range(8, 25, 2), yticks=[], xlabel="giờ",
       title="backward chỉ lấy mốc trước; nearest có thể lấy tương lai")
ax.spines["left"].set_visible(False)
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
