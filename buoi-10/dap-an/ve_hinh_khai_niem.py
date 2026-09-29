# SINH TỰ ĐỘNG bởi tools/tu_hoc/sinh.py từ tools/tu_hoc/buoi_10.py (bảng HINH) — không sửa tay.
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
    'kn-thieu-moc-thieu-gia-tri.png': r'''ax.plot([0, 1, 3, 5], [25, 25, 26, 26], "o", color="tab:blue", label="có số")
ax.plot(4, 25.5, "x", color="tab:red", ms=9, mew=2, label="có dòng, ô NaN: isna() thấy")
ax.add_patch(plt.Rectangle((1.65, 24.4), 0.7, 2.2, fill=False, ls="--", ec="tab:orange", lw=1.2))
ax.text(2, 25.5, "không có\ndòng nào", ha="center", va="center", fontsize=7, color="tab:orange")
ax.set_xticks(range(6), ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30"])
ax.set(ylim=(24, 27.4), ylabel="°C", title="isna() đếm 1 ô thiếu; lưới đầy đủ lộ ra 2")
ax.legend(fontsize=6, loc="upper left", ncol=2, frameon=False)
''',
    'kn-mcar-mar-mnar.png': r'''fig, truc = plt.subplots(1, 3, figsize=(5.4, 1.9), sharey=True)
rng = np.random.default_rng(0)
t = np.arange(120)
y = 50 + 20 * np.sin(t / 8) + rng.normal(0, 4, t.size)
mat = {"MCAR: mất do may rủi": rng.random(t.size) < 0.2,
       "MAR: mất trong mùa mưa": (t >= 60) & (t < 100) & (rng.random(t.size) < 0.6),
       "MNAR: mất khi giá trị cao": y > 62}
for ax, (ten, m) in zip(truc, mat.items()):
    ax.plot(t[~m], y[~m], ".", ms=3, color="tab:blue")
    ax.plot(t[m], y[m], ".", ms=3, color="tab:red")
    ax.set_title(ten, fontsize=7)
    ax.set_xlabel("t")
truc[1].axvspan(60, 100, color="0.88", zorder=0)
truc[2].axhline(62, color="k", ls="--", lw=0.8)
truc[0].set_ylabel("giá trị")
fig.suptitle("Chỉ MNAR mất có hệ thống phần cao: số còn lại bị lệch xuống", fontsize=8, y=1.07)
''',
    'kn-cam-bien-dung-yen-stuck-sensor.png': r'''fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 1.9), sharex=True)
gio = np.linspace(0, 12, 49)
dem = 25.6 + 0.8 * gio / 12
a.plot(gio, dem, color="tab:blue", label="thật")
a.step(gio, np.round(dem), where="mid", color="tab:orange", label="ghi được")
a.set(ylim=(24.5, 27.5), ylabel="°C", xlabel="giờ")
a.set_title("đêm, ghi tới 1 °C: làm tròn", fontsize=7)
ngay = 24 + 6 * np.sin(np.pi * gio / 12)
b.plot(gio, ngay, color="tab:blue")
b.plot(gio, np.full(gio.size, 26.0), color="tab:orange")
b.set(ylim=(23, 31), xlabel="giờ")
b.set_title("ngày, ghi tới 0,1 °C: kẹt", fontsize=7)
a.legend(fontsize=6, frameon=False)
fig.suptitle("Một đoạn phẳng chưa chắc là hỏng: xét độ phân giải trước", fontsize=8, y=1.06)
''',
    'kn-dien-du-lieu-imputation.png': r'''thieu = pd.Series([21, 23, np.nan, np.nan, 27, 25.0])
hom_qua = pd.Series([20, 22, 25, 27, 26, 24.0])
ax.plot(range(6), [21, 23, 26, 28, 27, 25], "k-o", ms=3, lw=1.5, label="thật")
cach = {"ffill": thieu.ffill(), "tuyến tính": thieu.interpolate(),
        "spline": thieu.interpolate(method="spline", order=3),
        "mùa vụ (hôm qua)": thieu.fillna(hom_qua), "hàng xóm + 1": thieu.fillna(hom_qua + 1)}
for (ten, z), dich in zip(cach.items(), (-0.12, -0.06, 0, 0.06, 0.12)):
    ax.plot(np.array([1, 2, 3, 4]) + dich, z[1:5], "o--", ms=3, lw=0.8, label=ten)
ax.axvspan(1.5, 3.5, color="0.92", zorder=0)
ax.set(xlabel="giờ", ylabel="°C", ylim=(20, 29.5), title="Lỗ trên đỉnh: chỉ cách mang hình dạng mới điền trúng")
ax.legend(fontsize=6, ncol=2, loc="lower right", frameon=False)
''',
    'kn-nhan-qua-cach-dien.png': r'''ax.plot([1, 3], [20, 30], "ko", ms=6)
ax.plot(2, 20, "s", color="tab:green", ms=7, label="ffill = 20 (chỉ nhìn quá khứ)")
ax.plot(2, 25, "D", color="tab:red", ms=6, label="tuyến tính = 25 (nhìn cả số 30)")
ax.plot([1, 3], [20, 30], color="tab:red", lw=0.8, ls=":")
ax.axvline(2.3, color="0.4", ls="--")
ax.text(2.35, 21, "mốc cắt:\nbên phải là tương lai", fontsize=7, color="0.3")
ax.set(xticks=[1, 2, 3], xlim=(0.6, 3.6), ylim=(17, 33), xlabel="mốc", ylabel="giá trị",
       title="Tuyến tính nhìn qua mốc cắt; ffill thì không")
ax.legend(fontsize=6, loc="upper left", frameon=False)
''',
    'kn-che-nhan-tao.png': r'''fig, (a, b) = plt.subplots(2, 1, figsize=(5.2, 2.1), sharex=True)
rng = np.random.default_rng(0)
t = np.arange(192)
y = 24 + 3 * np.sin(2 * np.pi * t / 48) + rng.normal(0, 0.3, t.size)
diem = rng.random(t.size) < 0.1
khoi = (t >= 80) & (t < 128)
for ax, m, ten in ((a, diem, "che điểm 10%"), (b, khoi, "che khối 48 bước")):
    ax.plot(t, y, color="0.7", lw=0.8)
    ax.plot(t[m], y[m], ".", color="tab:red", ms=4)
    ax.set_ylabel(ten, rotation=0, ha="right", va="center", fontsize=7)
    ax.set_yticks([])
b.set_xlabel("bước 30 phút")
a.set_title("Che điểm còn hàng xóm sát bên; che khối xoá cả một nhịp ngày")
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
