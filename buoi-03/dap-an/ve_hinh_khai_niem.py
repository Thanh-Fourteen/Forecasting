# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_03.py (bảng HINH) — không sửa tay.
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
    'kn-gio-mua-he-dst.png': r'''fig, truc = plt.subplots(1, 2, figsize=(5.4, 2.0), sharey=True)
for a, ngay, (lo, hi), mau in [(truc[0], "2024-03-10", (2, 3), "orange"), (truc[1], "2024-11-03", (1, 2), "gold")]:
    utc = pd.date_range(f"{ngay} 04:00", f"{ngay} 09:00", freq="5min", tz="UTC")
    dp = utc.tz_convert("America/New_York")
    gio = dp.hour + dp.minute / 60
    a.plot(utc.hour + utc.minute / 60, np.where(gio > 20, gio - 24, gio), ".", ms=2)   # 23:xx đêm trước vẽ thành −1
    a.axhspan(lo, hi, color=mau, alpha=0.35)
    a.set(title=ngay, xlabel="giờ UTC")
truc[0].set(ylabel="đồng hồ New York (giờ)", ylim=(-1.5, 5.5))
truc[0].text(4.2, 2.3, "không tồn tại", fontsize=7)
truc[1].text(4.2, 1.3, "xảy ra 2 lần", fontsize=7)
''',
    'kn-chuoi-deu-chuoi-khong-deu.png': r'''fig, (a, b) = plt.subplots(2, 1, figsize=(5.2, 1.8), sharex=True)
t = np.sort(np.random.default_rng(9).uniform(0, 5, 25))
a.eventplot(t, lineoffsets=0, linelengths=0.8)
a.set(yticks=[], ylabel="không đều", title="Sự kiện rải rác (trên) → gộp thành mỗi giờ một con số (dưới)")
b.bar(np.arange(5) + 0.5, np.histogram(t, bins=range(6))[0], width=0.9)
b.set(ylabel="đều", xlabel="giờ")
''',
    'kn-closed-label.png': r'''for i, (x0, x1) in enumerate([(9, 10), (10, 11)]):
    ax.add_patch(plt.Rectangle((x0, 0), 1, 1, color=["tab:blue", "tab:green"][i], alpha=0.15))
    ax.text(x0 + 0.02, 1.05, f"[{x0}:00, {x1}:00) → nhãn \"{x0}:00\"", fontsize=7)
for s in [9.0, 9 + 40 / 60, 10.0, 10 + 20 / 60]:
    ax.plot(s, 0.5, "o", color="tab:orange")
ax.text(9.93, 0.25, "10:00 thuộc\nkhoảng sau", fontsize=7)
ax.set(xlim=(8.8, 11.2), ylim=(0, 1.3), yticks=[], xticks=[9, 10, 11], xticklabels=["9:00", "10:00", "11:00"],
       title="Đóng trái, nhãn trái: có mốc đầu, không có mốc cuối")
''',
    'kn-ghep-as-of-merge-asof.png': r'''ax.plot([9.5, 10.5], [1, 1], "s", color="tab:green", ms=8)
ax.text(9.5, 1.12, "giá 9 (9:30)", ha="center", fontsize=7)
ax.text(10.5, 1.12, "giá 10 (10:30)", ha="center", fontsize=7)
ax.plot(10, 0, "o", color="tab:blue", ms=8)
ax.text(10, -0.25, "dòng 10:00", ha="center", fontsize=7)
ax.annotate("", (9.55, 0.95), (10, 0.05), arrowprops=dict(arrowstyle="->", color="tab:blue"))
ax.annotate("", (10.45, 0.95), (10, 0.05), arrowprops=dict(arrowstyle="->", color="tab:red", ls="--"))
ax.text(9.6, 0.45, "backward ✓", color="tab:blue", fontsize=7)
ax.text(10.25, 0.45, "forward ✗ (tương lai)", color="tab:red", fontsize=7)
ax.set(xlim=(9.2, 10.9), ylim=(-0.4, 1.3), yticks=[], xticks=[9.5, 10, 10.5], xticklabels=["9:30", "10:00", "10:30"],
       title="Lấy giá gần nhất ĐÃ CÓ, không lấy giá sắp tới")
''',
    'kn-backtest.png': r'''for k in range(4):
    ax.barh(k, 14 + 5 * k, color="0.75")
    ax.barh(k, 1, left=14 + 5 * k, color="tab:blue")
ax.set(yticks=range(4), yticklabels=[f"mốc cắt {k + 1}" for k in range(4)], xlabel="ngày trong tháng",
       title="Đứng ở từng mốc cắt: chỉ dùng phần xám, dự báo và chấm phần xanh")
ax.invert_yaxis()
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
