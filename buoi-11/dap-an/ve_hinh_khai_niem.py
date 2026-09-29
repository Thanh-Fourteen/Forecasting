# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_11.py (bảng HINH) — không sửa tay.
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
    'kn-ngoai-lai-outlier.png': r'''bon = {"AO (điểm đơn)": [10, 10, 10, 25, 10, 10, 10, 10], "dịch mức": [10, 10, 10, 20, 20, 20, 20, 20],
       "thay đổi tạm": [10, 10, 10, 20, 15, 12, 11, 10], "đổi phương sai": [10, 10, 10, 14, 6, 13, 7, 14]}
fig, truc = plt.subplots(1, 4, figsize=(5.4, 1.9), sharey=True)
for ax, (ten, v) in zip(truc, bon.items()):
    ax.plot(range(1, 9), v, "o-", ms=3, lw=0.9)
    ax.plot(4, v[3], "o", color="tab:red", ms=5)
    ax.axhline(10, color="0.7", lw=0.6, ls="--")
    ax.set(title=ten, xticks=[1, 4, 8])
    ax.title.set_fontsize(7)
truc[0].set_ylabel("giá trị")
fig.suptitle("Điểm lệch giống nhau; các điểm SAU mới cho biết loại", fontsize=8)
fig.tight_layout()
''',
    'kn-mad.png': r'''la = np.linspace(13, 150, 120)
s, mad = [], []
for x in la:
    v = np.array([10, 12, 11, 13, 12, x, 11, 12, 13, 12])
    s.append(v.std(ddof=1))
    mad.append(1.4826 * np.median(np.abs(v - np.median(v))))
ax.plot(la, s, label="độ lệch chuẩn")
ax.plot(la, mad, color="tab:green", label="MAD (× 1,4826)")
ax.set(xlabel="giá trị của số lạ", ylabel="độ dao động đo được",
       title="Số lạ càng lớn, độ lệch chuẩn càng phình; MAD đứng yên")
ax.legend(fontsize=7)
''',
    'kn-bo-loc-hampel.png': r'''rng = np.random.default_rng(9)
t = np.arange(200)
y = pd.Series(50 + 0.2 * t + rng.normal(0, 1.5, 200))
y[[40, 110, 160]] += 12
tv = y.rolling(31, center=True, min_periods=15).median()
mad = 1.4826 * (y - tv).abs().rolling(31, center=True, min_periods=15).median()
co = (y - tv).abs() > 3 * mad
ax.fill_between(t, tv - 3 * mad, tv + 3 * mad, color="tab:blue", alpha=0.2, label="trung vị ± 3·MAD (±15 điểm)")
ax.plot(t, y, color="0.4", lw=0.7)
ax.plot(t[co], y[co], "o", color="tab:red", ms=4, label=f"Hampel gắn cờ ({co.sum()})")
ax.axhline(y.mean() + 3 * y.std(), color="tab:orange", ls="--", label=f"3σ toàn chuỗi ({(y > y.mean() + 3 * y.std()).sum()})")
ax.set(xlabel="t", ylabel="giá trị", title="Hampel đi theo xu hướng; 3σ toàn chuỗi không bắt được gì")
ax.legend(fontsize=6, loc="lower right")
''',
    'kn-winsorize.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 1.9), sharey=True)
x = np.arange(1, 6)
for ax, v, ten in ((a, [12, 11, 13, np.nan, 12], "Xoá: thủng mốc 4"), (b, [12, 11, 13, 12, 12], "Winsorize: 90 → 12, đủ 5 mốc")):
    ax.plot(4, 90, "x", color="0.6", ms=7)
    ax.annotate("90 bị gắn cờ", (4, 90), (2.6, 70), fontsize=7, color="0.4")
    ax.plot(x, v, "o-", ms=4)
    if ten.startswith("Winsorize"):
        ax.plot(4, 12, "o", color="tab:orange", ms=6)
    ax.set(title=ten, xticks=x, xlabel="mốc")
a.set_ylabel("giá trị")
fig.tight_layout()
''',
    'kn-penalty-phat.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 2.1))
v = np.array([10, 11, 10, 9, 10, 20, 21, 19, 20, 20])
a.plot(range(1, 11), v, "o", ms=4)
a.hlines([10, 20], [0.7, 5.7], [5.3, 10.3], color="tab:red")
a.set(xlabel="vị trí", ylabel="giá trị", title="Cắt trước điểm 6: hai đoạn phẳng")
chi_phi, phat = np.array([254, 4, 3.17]), 3 * np.log(10) * np.arange(3)
b.bar(range(3), chi_phi, label="chi phí")
b.bar(range(3), phat, bottom=chi_phi, color="tab:orange", label="phạt 6,9 × K")
for k in range(3):
    tong = chi_phi[k] + phat[k]
    b.text(k, min(tong, 26) + 0.5, f"{tong:.1f}".replace(".", ",") + (" ↑" if tong > 30 else ""), ha="center", fontsize=7,
           color="white" if tong > 30 else "black")
b.set(ylim=(0, 30), xticks=range(3), xlabel="số điểm gãy K", title="Tổng nhỏ nhất ở K = 1")
b.legend(fontsize=6, loc="upper right")
fig.tight_layout()
''',
    'kn-cusum-crops.png': r'''fig, (a, b) = plt.subplots(2, 1, figsize=(5.2, 2.4), sharex=True)
rng = np.random.default_rng(2)
y = np.r_[rng.normal(10, 1, 40), rng.normal(11.5, 1, 30)]
s = np.zeros(y.size)
for t in range(1, y.size):
    s[t] = max(0, s[t - 1] + y[t] - 10 - 0.5)
bao = np.argmax(s > 5)
a.plot(y, lw=0.8)
a.set_ylabel("y")
b.plot(s, color="tab:green")
b.axhline(5, color="tab:red", ls="--")
b.plot(bao, s[bao], "o", color="tab:red", ms=4)
b.set(xlabel="t", ylabel="tổng cộng dồn")
for ax in (a, b):
    ax.axvline(40, color="0.6", lw=0.8)
a.set_title(f"CUSUM báo động ở t = {bao}, {bao - 40} bước sau khi mức đổi")
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
