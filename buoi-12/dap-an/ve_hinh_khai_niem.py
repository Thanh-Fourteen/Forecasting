# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_12.py (bảng HINH) — không sửa tay.
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
    'kn-bo-loc-nhan-qua.png': r'''gio, dien = np.arange(1, 6), np.array([10, 12, 14, 30, 16])
ax.axvspan(3.5, 5.5, color="tab:red", alpha=0.07)
ax.text(4.5, 35, "tương lai", ha="center", fontsize=7, color="tab:red")
ax.bar(gio, dien, width=0.6, color="0.75")
for x, v in zip(gio, dien):
    ax.text(x, v + 0.8, str(v), ha="center", fontsize=7)
ax.axvline(3, color="k", ls=":", lw=0.8)
ax.plot([0.7, 3.3], [-4, -4], color="tab:blue", lw=3)
ax.text(0.5, -4, "trailing", ha="right", va="center", fontsize=7, color="tab:blue")
ax.plot([1.7, 4.3], [-9, -9], color="tab:orange", lw=3)
ax.text(1.5, -9, "centered", ha="right", va="center", fontsize=7, color="tab:orange")
ax.set(xlim=(-0.6, 5.5), ylim=(-12, 40), yticks=[0, 10, 20, 30], xticks=gio, xlabel="giờ", ylabel="điện",
       title="Đứng ở giờ 3: cửa sổ centered đã chứa số 30 của giờ 4")
''',
    'kn-tre-pha.png': r'''t = np.arange(160)
y = np.sin(2 * np.pi * t / 72)
z = pd.Series(y).rolling(13).mean()
ax.plot(t, y, color="k", lw=1, label="tín hiệu")
ax.plot(t, z, color="tab:blue", lw=1.6, label="trung bình 13 điểm gần nhất")
ax.annotate("", (24, 1.08), (18, 1.08), arrowprops={"arrowstyle": "->", "lw": 1})
ax.text(21, 1.16, "trễ 6 bước", ha="center", fontsize=7)
ax.set(xlabel="t (bước)", ylim=(-1.2, 1.9), yticks=[], title="Bộ lọc nhân quả chạy sau tín hiệu: đỉnh đến muộn 6 bước")
ax.legend(fontsize=6, loc="upper right", ncols=2)
''',
    'kn-periodogram-welch.png': r'''from scipy import signal
rng = np.random.default_rng(0)
t = np.arange(24 * 60)
y = np.sin(2 * np.pi * t / 24) + rng.normal(0, 1, t.size)
f1, p1 = signal.periodogram(y)
f2, p2 = signal.welch(y, nperseg=256)
ax.semilogy(f1[1:], p1[1:], color="0.65", lw=0.5, label="periodogram: cả chuỗi một lần")
ax.semilogy(f2[1:], p2[1:], color="tab:blue", lw=1.6, label="Welch: trung bình các đoạn")
ax.axvline(1 / 24, color="tab:orange", ls="--", lw=0.8)
ax.set(xlabel="tần số (chu kỳ/giờ)", ylabel="mật độ phổ", ylim=(1e-3, 3e3),
       title="Cùng đỉnh ở chu kỳ 24 giờ; Welch mượt, dễ đọc hơn")
ax.legend(fontsize=6, loc="upper right")
''',
    'kn-aliasing.png': r'''t = np.linspace(0, 15, 600)
m = np.arange(0, 16, 3)
ax.plot(t, np.sin(2 * np.pi * t / 4), color="0.6", lw=0.8, label="sóng thật: 4 bước")
ax.plot(t, -np.sin(2 * np.pi * t / 12), "--", color="tab:red", lw=1, label="sóng giả: 12 bước")
ax.plot(m, np.sin(2 * np.pi * m / 4), "o", color="tab:red", ms=5, label="mẫu mỗi 3 bước")
ax.set(xlabel="bước", ylim=(-1.3, 2.0), yticks=[-1, 0, 1],
       title="Lấy mẫu thưa: sóng 4 bước hiện thành sóng giả 12 bước")
ax.legend(fontsize=6, ncols=3, loc="upper center")
''',
    'kn-loc-thong-thap.png': r'''from scipy import signal
sos = signal.butter(8, 0.4, btype="low", fs=6.0, output="sos")
f, h = signal.freqz_sos(sos, worN=3000, fs=6.0)
ax.axvspan(0.5, 3, color="tab:red", alpha=0.07)
ax.plot(f, np.abs(h), color="tab:blue", lw=1.6)
ax.axvline(0.5, color="tab:red", ls="--", lw=0.8)
ax.text(0.6, 0.72, "nhanh hơn Nyquist mới (0,5):\nphải chặn trước khi hạ mẫu", fontsize=7, color="tab:red")
ax.plot(1.4, 0.02, "v", color="k")
ax.text(1.4, 0.1, "dao động 43 phút (1,4)", ha="center", fontsize=7)
ax.set(xlim=(0, 3), ylim=(0, 1.1), xlabel="tần số (chu kỳ/giờ)", ylabel="phần được giữ",
       title="Lọc thông thấp: giữ dao động chậm, chặn dao động nhanh")
''',
    'kn-ewma.png': r'''k = np.arange(25)
ax.bar(k - 0.2, 0.15 * 0.85**k, width=0.4, color="tab:blue", label="EWMA α = 0,15")
ax.bar(k[:13] + 0.2, np.full(13, 1 / 13), width=0.4, color="tab:orange", label="trung bình 13 điểm")
ax.set(xlabel="số bước lùi về quá khứ", ylabel="mức đóng góp", title="EWMA: điểm mới nặng nhất, điểm cũ nhẹ dần")
ax.legend(fontsize=7)
''',
    'kn-savitzky-golay.png': r'''from scipy import signal
t = np.arange(80)
y = 10 * np.exp(-(((t - 40) / 4) ** 2))
ma = pd.Series(y).rolling(13, center=True).mean()
sg = signal.savgol_filter(y, 13, 2)
ax.plot(t, y, color="k", lw=1, label="đỉnh thật: 10")
ax.plot(t, ma, color="tab:orange", lw=1.4, label=f"trung bình trượt 13: {ma.max():.1f}".replace(".", ","))
ax.plot(t, sg, color="tab:blue", lw=1.4, label=f"Savitzky–Golay 13, bậc 2: {sg.max():.1f}".replace(".", ","))
ax.set(xlabel="t", xlim=(15, 65), title="Savitzky–Golay giữ chiều cao đỉnh, trung bình trượt san phẳng")
ax.legend(fontsize=6)
''',
    'kn-sosfilt-sosfiltfilt.png': r'''from scipy import signal
t = np.arange(120)
y = (t >= 60).astype(float)
sos = signal.butter(4, 0.05, output="sos")
ax.plot(t, y, color="k", lw=1, label="bước nhảy thật")
ax.plot(t, signal.sosfilt(sos, y), color="tab:blue", lw=1.5, label="sosfilt: lên sau")
ax.plot(t, signal.sosfiltfilt(sos, y), color="tab:orange", lw=1.5, label="sosfiltfilt: lên trước")
ax.axvline(60, color="0.5", ls=":")
ax.set(xlabel="t", title="Chạy ngược thời gian thì hết trễ — vì đã nhìn tương lai")
ax.legend(fontsize=6, loc="upper left")
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
