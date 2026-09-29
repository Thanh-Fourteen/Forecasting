# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_09.py (bảng HINH) — không sửa tay.
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
    'kn-he-so-lech-skewness.png': r'''from scipy import stats
rng = np.random.default_rng(0)
fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 2.0), sharey=True, layout="constrained")
for ax, v, mau, ten in ((a, rng.normal(10, 2, 2000), "tab:blue", "cân hai phía"),
                        (b, rng.lognormal(2, 0.6, 2000), "tab:orange", "đuôi phải dài")):
    ax.hist(v, bins=40, range=(0, 40), color=mau)
    ax.set_title(f"{ten}: hệ số lệch {stats.skew(v) + 0:.2f}".replace(".", ","), fontsize=8)
    ax.set_xlabel("giá trị")
a.set_ylabel("số lần gặp")
''',
    'kn-z-score-chuan-hoa.png': r'''t = np.arange(24)
nho = 3 + np.sin(2 * np.pi * t / 12) + 0.05 * t
lon = 100 * nho
fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 2.0), layout="constrained")
a.plot(t, nho, label="chuỗi nhỏ")
a.plot(t, lon, label="× 100")
a.set_title("gốc: một chuỗi gấp 100 lần", fontsize=8)
a.set_xlabel("tháng")
a.legend(fontsize=6)
for v, ls in ((nho, "-"), (lon, "--")):
    b.plot(t, (v - v.mean()) / v.std(), ls=ls)
b.set_title("sau z-score: trùng khít, chỉ còn hình dạng", fontsize=8)
b.set_xlabel("tháng")
''',
    'kn-tan-so.png': r'''t = np.arange(36)
fig, (a, b) = plt.subplots(2, 1, figsize=(5.2, 2.4), sharex=True, layout="constrained")
a.plot(t, np.cos(2 * np.pi * t / 12), "o-", ms=2)
a.set_title("chu kỳ 12 tháng → tần số 1/12 ≈ 0,083", fontsize=8)
b.plot(t, np.cos(np.pi * t), "o-", ms=2, color="tab:orange")
b.set_title("chu kỳ 2 tháng → tần số 1/2 = 0,5", fontsize=8)
b.set_xlabel("tháng")
for ax in (a, b):
    ax.set_yticks([])
''',
    'kn-pca-pc1-pc2.png': r'''rng = np.random.default_rng(0)
r1 = rng.uniform(0, 1, 200)
cat = 60 - 50 * r1 + rng.normal(0, 4, 200)
X = np.column_stack([r1, cat])
Z = (X - X.mean(0)) / X.std(0)
w, V = np.linalg.eigh(np.cov(Z.T))
ax.scatter(Z[:, 0], Z[:, 1], s=5, alpha=0.6)
for k, ten, dai in ((1, "PC1", 2.4), (0, "PC2", 0.8)):
    v = V[:, k] * dai
    ax.plot([-v[0], v[0]], [-v[1], v[1]], color="tab:red", lw=1.5)
    dau = v if v[0] > 0 else -v
    ax.text(dau[0] + 0.15, dau[1], f"{ten}: {w[k] / w.sum():.0%} khác biệt", color="tab:red", fontsize=7, va="center",
            bbox={"fc": "white", "ec": "none", "pad": 1})
ax.set_aspect("equal", adjustable="datalim")
ax.set(xlabel="z của r₁", ylabel="z của số lần cắt", title="Hai đặc trưng nói cùng một điều: một trục chung đủ tả")
''',
    'kn-dtw-dynamic-time-warping.png': r'''x = np.array([0, 0, 1, 0, 0, 0])
y = np.array([0, 1, 0, 0, 0, 0]) - 1.6
fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 1.9), sharey=True, layout="constrained")
cap_dtw = [(0, 0), (1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (5, 5)]
for ax, cap, ten in ((a, [(i, i) for i in range(6)], "thường 1,41: đỉnh bị so với đáy"), (b, cap_dtw, "DTW 0: đỉnh khớp đỉnh")):
    for i, j in cap:
        ax.plot([i, j], [x[i], y[j]], color="0.6", lw=0.8)
    ax.plot(x, "o-", color="tab:blue")
    ax.plot(y, "o-", color="tab:orange")
    ax.set_title(ten, fontsize=8)
    ax.set(xlabel="thời điểm", yticks=[])
''',
    'kn-phan-cum-phan-cap-ward.png': r'''from scipy.cluster.hierarchy import dendrogram, linkage
rng = np.random.default_rng(1)
diem = np.r_[rng.normal(0, 1, (4, 2)), rng.normal(6, 1, (4, 2))]
L = linkage(diem, method="ward")
dendrogram(L, ax=ax, labels=[f"c{i + 1}" for i in range(8)], color_threshold=0, above_threshold_color="tab:blue")
ax.axhline((L[-1, 2] + L[-2, 2]) / 2, color="tab:red", ls="--")
ax.set(ylabel="chi phí gộp", title="Gộp dần từ dưới lên; cắt ngang để lấy số cụm muốn có")
''',
    'kn-phan-loai-abc-xyz-ax-cz.png': r'''t = np.arange(1, 13)
p = np.tile([10, 30], 6)
q = np.array([18, 22, 19, 21, 22, 18, 20, 21, 18, 22, 19, 20])
cv = lambda v: f"{np.std(v, ddof=1) / np.mean(v):.2f}".replace(".", ",")   # noqa: E731
ax.plot(t, p, "o-", label=f"P: CV {cv(p)} → Y, nhịp đều, dễ")
ax.plot(t, q, "s-", label=f"Q: CV {cv(q)} → X, thất thường, khó")
ax.set(xlabel="tháng", ylabel="số bán", ylim=(0, 40), title="CV đo dao động, không đo độ khó dự báo")
ax.legend(fontsize=6, loc="upper right")
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
