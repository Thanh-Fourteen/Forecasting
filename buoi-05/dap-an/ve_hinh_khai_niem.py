# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_05.py (bảng HINH) — không sửa tay.
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
    'kn-log-exp.png': r'''y = np.linspace(40, 1400, 400)
ax.plot(y, np.log(y), color="0.6")
for a, mau in [(100, "tab:orange"), (1000, "tab:green")]:
    b = 1.2 * a
    ax.plot([a, b], [np.log(a)] * 2, color=mau, lw=3)
    ax.plot([b, b], [np.log(a), np.log(b)], color=mau, lw=3)
    ax.annotate(f"{a} → {b:.0f}: cao thêm 0,182", (b, np.log(a)), xytext=(8, -12), textcoords="offset points",
                fontsize=7, color=mau)
ax.set(xlabel="y (thang gốc)", ylabel="log y", title="Cùng tăng 20%: log tăng cùng một khoảng, dù mức khác xa")
''',
    'kn-bien-doi-box-cox.png': r'''y = np.linspace(1, 1000, 400)
for lam, mau in [(1, "0.5"), (0.5, "tab:orange"), (0, "tab:blue")]:
    w = np.log(y) if lam == 0 else (y**lam - 1) / lam
    ax.plot(y, (w - w.min()) / (w.max() - w.min()), color=mau, label=f"λ = {lam}".replace(".", ","))
ax.set(xlabel="y (thang gốc)", ylabel="sau biến đổi (quy về 0–1)", title="Núm vặn λ: 1 giữ nguyên, 0 là log, ở giữa ép vừa")
ax.legend(fontsize=7)
''',
    'kn-doi-nguoc.png': r'''fig, (a, b) = plt.subplots(2, 1, figsize=(5.2, 1.9))
w = np.array([0.0, 1.0, 2.0])
a.plot(w, [0] * 3, "o", ms=7)
a.axvline(1, color="tab:orange", lw=1.5)
a.set(xlim=(-0.3, 2.3), yticks=[], title="thang log: 0, 1, 2 — trung bình = số giữa = 1")
b.plot(np.exp(w), [0] * 3, "o", ms=7)
b.axvline(np.exp(1), color="tab:orange", lw=1.5)
b.axvline(np.exp(w).mean(), color="k", lw=1.5, ls="--")
b.text(np.exp(1) - 0.1, 0.45, "trung vị 2,72", color="tab:orange", fontsize=6, ha="right")
b.text(np.exp(w).mean() + 0.1, 0.45, "trung bình 3,70", fontsize=6)
b.set(xlim=(0, 8), ylim=(-1, 1), yticks=[], title="thang gốc: 1; 2,72; 7,39 — số lớn bị đẩy xa")
for ax in (a, b):
    ax.title.set_fontsize(8)
fig.tight_layout()
''',
    'kn-drift.png': r'''t = np.arange(36)
y = 100 + 3 * t / 12 + 10 * np.sin(2 * np.pi * t / 12)
ax.plot(t[:24], y[:24], "o-", ms=3, label="đã biết")
ax.plot(t[24:], y[12:24] + 3, "o--", ms=3, color="tab:orange", label="seasonal naive + drift")
ax.plot(t[24:], y[12:24], ":", color="0.6", label="seasonal naive (không drift)")
ax.set(xlabel="tháng", ylabel="doanh số (số minh hoạ)", title="Chép cùng tháng năm trước, cộng mức tăng mỗi năm")
ax.legend(fontsize=6)
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
