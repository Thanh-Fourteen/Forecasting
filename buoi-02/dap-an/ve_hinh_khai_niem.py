# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_02.py (bảng HINH) — không sửa tay.
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
    'kn-histogram.png': r'''x = np.random.default_rng(0).lognormal(5, 0.8, 3000)
ax.hist(x, bins=np.arange(0, 1000, 25), color="lightsteelblue", edgecolor="white")
ax.set(xlabel="giá trị (chia khoảng rộng 25)", ylabel="số lần rơi vào", title="Đếm theo khoảng: thấy ngay dồn bên trái, đuôi dài bên phải")
''',
    'kn-quantile-trung-vi.png': r'''x = np.sort(np.random.default_rng(0).lognormal(5, 0.8, 3000))
ax.plot(x, np.arange(1, x.size + 1) / x.size)
for p, mau in [(0.5, "tab:green"), (0.9, "tab:orange")]:
    q = np.quantile(x, p)
    ax.plot([0, q, q], [p, p, 0], color=mau, ls="--")
    ax.text(q + 10, p - 0.1, f"quantile {str(p).replace('.', ',')} ≈ {q:.0f}", color=mau)
ax.set(xlim=(0, 800), xlabel="mốc", ylabel="tỷ lệ ≤ mốc", title="Từ tỷ lệ trên trục dọc, đi ngang rồi thả xuống: ra quantile")
''',
    'kn-phuong-sai-do-lech-chuan.png': r'''g = np.linspace(-10, 10, 400)
for s, mau in [(1, "tab:blue"), (3, "tab:orange")]:
    ax.plot(g, np.exp(-g**2 / (2 * s**2)) / (s * np.sqrt(2 * np.pi)), color=mau, label=f"độ lệch chuẩn {s}")
ax.set(yticks=[], xlabel="giá trị (trung bình 0)", title="Cùng trung bình; độ lệch chuẩn lớn thì trải rộng hơn")
ax.legend(fontsize=7)
''',
    'kn-he-so-lech.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.0), sharey=True)
rng = np.random.default_rng(1)
a.hist(rng.normal(0, 1, 3000), bins=40, color="lightsteelblue")
a.set(title="đối xứng: hệ số lệch ≈ 0", yticks=[])
b.hist(rng.lognormal(0, 0.7, 3000), bins=40, color="navajowhite")
b.set(title="đuôi phải dài: hệ số lệch > 0")
''',
    'kn-pinball-loss.png': r'''e = np.linspace(-5, 5, 201)                      # thật − dự báo
ax.plot(e, np.where(e >= 0, 0.8 * e, -0.2 * e), label="pinball τ = 0,8")
ax.plot(e, np.abs(e) * 0.5, ls=":", color="0.5", label="tuyệt đối (× 0,5)")
ax.set(xlabel="thật − dự báo (dương = dự báo thiếu)", ylabel="tiền phạt", title="Thiếu bị phạt dốc gấp 4 lần thừa")
ax.legend(fontsize=7)
''',
    'kn-phan-phoi-chuan.png': r'''g = np.linspace(-4, 4, 400)
f = np.exp(-g**2 / 2) / np.sqrt(2 * np.pi)
ax.plot(g, f)
ax.fill_between(g, f, where=np.abs(g) <= 1.96, alpha=0.25, label="95% ở giữa")
ax.fill_between(g, f, where=np.abs(g) > 1.96, color="tab:orange", alpha=0.5, label="2,5% mỗi đuôi")
ax.set(xticks=[-1.96, 0, 1.96], xticklabels=["TB − 1,96 s", "trung bình", "TB + 1,96 s"], yticks=[],
       title="Hình chuông đối xứng: 95% trong ±1,96 độ lệch chuẩn")
ax.legend(fontsize=7)
''',
    'kn-ty-le-phu.png': r'''rng = np.random.default_rng(3)
t = np.arange(40)
y = rng.normal(0, 1, 40)
trong = np.abs(y) <= 1.6
ax.fill_between(t, -1.6, 1.6, color="tab:blue", alpha=0.12, label="khoảng đã báo")
ax.plot(t[trong], y[trong], "o", ms=3, label=f"rơi trong: {trong.sum()}/40")
ax.plot(t[~trong], y[~trong], "x", color="tab:red", label=f"rơi ngoài: {(~trong).sum()}/40")
ax.set(yticks=[], xlabel="lần dự báo", title=f"Tỷ lệ phủ = {trong.mean():.0%}")
ax.legend(fontsize=7, ncols=3, loc="upper center", bbox_to_anchor=(0.5, -0.3), frameon=False)
''',
    'kn-tuong-quan-he-so-r.png': r'''fig, truc = plt.subplots(1, 4, figsize=(5.8, 1.7))
rng = np.random.default_rng(4)
x = rng.normal(size=150)
for a, (ten, y) in zip(truc, [("r ≈ 0,9", x + 0.5 * rng.normal(size=150)), ("r ≈ 0", rng.normal(size=150)),
                               ("r ≈ −0,9", -x + 0.5 * rng.normal(size=150)), ("cong: r ≈ 0", x**2)]):
    a.plot(x, y, ".", ms=2)
    a.set(title=ten, xticks=[], yticks=[])
''',
    'kn-tu-tuong-quan.png': r'''rng = np.random.default_rng(5)
e = rng.normal(size=150)
x = np.zeros(150)
for t in range(1, 150):
    x[t] = 0.9 * x[t - 1] + e[t]
ax.plot(e, lw=0.8, color="0.6", label="tự tương quan ≈ 0: lộn xộn")
ax.plot(x, lw=1.2, label="tự tương quan ≈ 0,9: dai, lên thì ở trên một lúc")
ax.set(yticks=[], xlabel="thời gian")
ax.legend(fontsize=7)
''',
    'kn-kiem-dinh-gia-thuyet-khong-h0.png': r'''xao = np.random.default_rng(8).normal(0, 200, 9999)
ax.hist(xao, bins=60, color="lightsteelblue")
ax.axvline(456, color="tab:orange", lw=2)
ax.axvline(-456, color="tab:orange", ls="--")
ax.set(yticks=[], xlabel="chênh lệch khi xáo nhãn ngẫu nhiên",
       title="Nếu H0 đúng, chênh lệch rơi đâu; p = phần nằm ngoài hai vạch cam")
''',
    'kn-dinh-ly-gioi-han-trung-tam-clt.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.6, 2.0))
rng = np.random.default_rng(6)
a.hist(rng.lognormal(0, 0.8, 5000), bins=50, color="navajowhite")
a.set(title="từng giá trị: lệch phải", yticks=[])
b.hist(rng.lognormal(0, 0.8, (5000, 30)).mean(axis=1), bins=50, color="lightsteelblue")
b.set(title="TB của 30 giá trị: gần hình chuông", yticks=[])
fig.tight_layout()
''',
    'kn-bootstrap-block-bootstrap.png': r'''fig, truc = plt.subplots(3, 1, figsize=(5.2, 1.9), sharex=True)
rng = np.random.default_rng(7)
mau = plt.cm.viridis(np.linspace(0, 1, 12))
cs = [np.arange(12), rng.integers(0, 12, 12),
      np.concatenate([np.arange(b, b + 4) for b in rng.integers(0, 9, 3)])]
for a, ten, c in zip(truc, ["gốc", "rút từng điểm", "rút khối 4"], cs):
    a.bar(range(12), 1, color=mau[c], width=0.95)
    a.set(yticks=[], ylabel=ten)
    a.yaxis.label.set(rotation=0, ha="right", va="center")
truc[-1].set(xticks=[])
truc[0].set_title("Màu = vị trí gốc: rút khối giữ các điểm liền nhau đi cùng nhau")
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
