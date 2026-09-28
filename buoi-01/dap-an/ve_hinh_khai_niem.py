# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_01.py (bảng HINH) — không sửa tay.
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
    'kn-tam-du-bao-h.png': r'''t = np.arange(-72, 169)
y = 1 + 0.5 * np.sin(2 * np.pi * t / 24) + np.random.default_rng(0).normal(0, 0.1, t.size)
ax.plot(t[t <= 0], y[t <= 0], color="0.3", lw=1, label="đã biết")
ax.axvspan(0, 168, color="tab:blue", alpha=0.12, label="tầm dự báo: h = 1…168")
ax.axvline(0, color="tab:orange", lw=1.5)
ax.text(2, 1.62, "gốc dự báo", color="tab:orange")
ax.set(xlabel="giờ tính từ gốc", yticks=[], title="Bên trái gốc đã biết; phải dự báo cả dải bên phải")
ax.legend(loc="lower right", fontsize=7)
''',
    'kn-dich-muc.png': r'''t = np.arange(200)
y = np.where(t < 120, 1.0, 1.4) + np.random.default_rng(2).normal(0, 0.08, t.size)
ax.plot(t, y, lw=0.8)
ax.hlines([1.0, 1.4], [0, 120], [120, 200], color="tab:orange", lw=2)
ax.set(xlabel="thời gian", yticks=[], title="Mức trung bình nhảy lên rồi ở luôn đó")
''',
    'kn-mua-vu.png': r'''t = np.arange(24 * 21)
y = 1 + 0.6 * np.sin(2 * np.pi * (t - 14) / 24) + 0.3 * ((t // 24) % 7 >= 5) \
    + np.random.default_rng(1).normal(0, 0.12, t.size)
ax.plot(t / 24, y, lw=0.8)
for k in range(3):
    ax.axvspan(7 * k + 5, 7 * k + 7, color="tab:orange", alpha=0.12)
ax.set(xlabel="ngày", yticks=[], title="Mẫu lặp lại: mỗi ngày một nhịp, cuối tuần (cam) cao hơn")
''',
    'kn-du-bao-cuon.png': r'''for k in range(5):
    ax.barh(k, 10 + k, color="0.75")
    ax.barh(k, 1, left=10 + k, color="tab:blue")
ax.set(yticks=range(5), yticklabels=[f"gốc {k + 1}" for k in range(5)], xlabel="thời gian (tuần)",
       title="Xám: dữ liệu được dùng · xanh: tuần dự báo và chấm — gốc dời dần")
ax.invert_yaxis()
''',
    'kn-phan-phoi.png': r'''v = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])
gt, dem = np.unique(v, return_counts=True)
ax.bar(gt, dem, width=0.7)
ax.set(xlabel="kWh lúc 19 giờ", ylabel="số ngày", xticks=range(5, 13), title="10 ngày: hay gặp quanh 6–9, hiếm khi 12")
''',
    'kn-quantile-trung-vi.png': r'''v = np.sort(np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8]))
ax.bar(range(1, 11), v, color=["tab:blue" if i < 8 else "0.75" for i in range(10)])
ax.axhline(9, color="tab:orange", ls="--")
ax.text(0.6, 9.3, "quantile 0,8 = 9 (số thứ 8)", color="tab:orange")
ax.axhline(7, color="tab:green", ls=":")
ax.text(0.6, 7.3, "trung vị = 7 (số thứ 5)", color="tab:green")
ax.set(xlabel="xếp tăng dần (thứ tự)", ylabel="kWh", xticks=range(1, 11), title="Xếp tăng, lấy số thứ 0,8 × 10 = 8 → quantile 0,8 = 9")
''',
    'kn-bai-toan-newsvendor.png': r'''mua = np.arange(6, 13)
v = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])
cp = [4 * np.clip(v - m, 0, None).sum() + np.clip(m - v, 0, None).sum() for m in mua]
ax.plot(mua, cp, "o-")
ax.plot(9, min(cp), "o", color="tab:orange", ms=9)
ax.axvline(v.mean(), color="0.5", ls=":")
ax.text(v.mean() + 0.1, 65, "trung bình 7,7", color="0.4")
ax.set(xlabel="lượng mua mỗi ngày (kWh)", ylabel="tiền mất 10 ngày", title="Rẻ nhất ở 9 = quantile 0,8, không phải trung bình")
''',
    'kn-ham-phan-phoi-tich-luy.png': r'''v = np.sort(np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8]))
ax.step(np.r_[4, v, 13], np.r_[0, np.arange(1, 11) / 10, 1], where="post")
ax.plot([4, 9, 9], [0.8, 0.8, 0], color="tab:orange", ls="--")
ax.set(xlabel="mốc x (kWh)", ylabel="tỷ lệ ngày ≤ x", title="Đi ngang từ 0,8 tới đường, thả xuống: gặp 9 = quantile 0,8")
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
