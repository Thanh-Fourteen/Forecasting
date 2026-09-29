# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_06.py (bảng HINH) — không sửa tay.
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
    'kn-phan-ra.png': r'''fig, truc = plt.subplots(4, 1, figsize=(5.2, 3.0), sharex=True)
t = np.arange(48)
T = 20 + 0.15 * t
S = 5 * np.sin(2 * np.pi * t / 12)
R = np.random.default_rng(3).normal(0, 1, t.size)
for ax, s, ten in zip(truc, [T + S + R, T, S, R], ["dữ liệu", "xu hướng", "mùa vụ", "phần dư"]):
    ax.plot(t, s, lw=1)
    ax.set_ylabel(ten, rotation=0, ha="right", va="center", fontsize=7)
    ax.set_yticks([])
truc[0].set_title("Dữ liệu = xu hướng + mùa vụ + phần dư")
truc[-1].set_xlabel("thời gian")
''',
    'kn-2-m-ma.png': r'''w = np.array([1, 2, 2, 2, 1]) / 8
mau = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:blue"]
ax.bar(range(5), w, color=mau)
for i, v in enumerate(w):
    ax.text(i, v + 0.005, ["1/8", "1/4", "1/4", "1/4", "1/8"][i], ha="center", fontsize=7)
ax.set(xticks=range(5), xticklabels=["t−2\n(quý 1)", "t−1\n(quý 2)", "t\n(quý 3)", "t+1\n(quý 4)", "t+2\n(quý 1)"],
       ylabel="trọng số", ylim=(0, 0.32), title="2×4-MA: quý 1 xuất hiện hai lần, mỗi lần một nửa")
ax.tick_params(axis="x", labelsize=7)
''',
    'kn-phan-ra-cong-nhan.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 2.0), sharey=True)
t = np.arange(60)
T = 100 + 2 * t
S = np.sin(2 * np.pi * t / 12)
a.plot(t, T + 20 * S)
a.plot(t, T, color="0.6", lw=0.8)
a.set(title="cộng: T + 20·S", xlabel="thời gian")
b.plot(t, T * (1 + 0.2 * S))
b.plot(t, T, color="0.6", lw=0.8)
b.set(title="nhân: T × (1 + 0,2·S)", xlabel="thời gian")
for ax in (a, b):
    ax.title.set_fontsize(8)
''',
    'kn-stl-loess.png': r'''x = np.arange(1, 6)
v = np.array([2, 4, 6, 8, 10])
ax.plot(x, v, "o", ms=9, mfc="none", mew=1.5, zorder=3, label="dữ liệu trừ xu hướng")
ax.plot(x, np.full(5, v.mean()), color="0.5", label="cổ điển: một trung bình")
ax.plot(x, [3, 4, 6, 8, 9], "s-", color="tab:orange", label="cục bộ: trung bình 3 năm")
ax.set(xlabel="năm", ylabel="mùa vụ quý 1", xticks=x, title="Mùa vụ cục bộ được đổi dần theo năm")
ax.legend(fontsize=6)
''',
    'kn-do-manh-xu-huong-mua-vu.png': r'''fig, truc = plt.subplots(1, 2, figsize=(5.4, 1.9), sharey=True)
t = np.arange(72)
S = np.sin(2 * np.pi * t / 12)
rng = np.random.default_rng(5)
for ax, do_on in zip(truc, [0.15, 1.0]):
    R = rng.normal(0, do_on, t.size)
    F = max(0, 1 - R.var() / (S + R).var())
    ax.plot(t, S + R, lw=0.9)
    ax.set(title=f"phần dư độ lệch chuẩn {do_on}: F_S = {F:.2f}".replace(".", ","), xlabel="thời gian", yticks=[])
    ax.title.set_fontsize(7)
''',
    'kn-robust.png': r'''u = np.linspace(0, 3.6, 400)
ax.plot(u, np.where(u < 1, (1 - u**2) ** 2, 0))
for uu, ten, mau in [(1 / 6, "phần dư ±1", "tab:green"), (1 / 3, "phần dư −2", "tab:orange"), (20 / 6, "phần dư 20 (u ≈ 3,3)", "tab:red")]:
    rho = (1 - uu**2) ** 2 if uu < 1 else 0
    ax.plot(uu, rho, "o", color=mau)
    ax.annotate(ten, (uu, rho), xytext=(5, 5), textcoords="offset points", fontsize=6, color=mau,
                ha="right" if uu > 3 else "left")
ax.axvline(1, color="0.6", ls=":", lw=0.8)
ax.set(xlabel="u = |phần dư| / (6 × trung vị |phần dư|)", ylabel="trọng số ρ", ylim=(-0.05, 1.1),
       title="Phần dư càng lớn càng bớt tin; vượt mốc thì bỏ qua")
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
