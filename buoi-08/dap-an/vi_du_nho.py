# %% [markdown]
# # Buổi 8 — ví dụ số nhỏ trong tai-lieu.md (không cần dữ liệu). Chạy: python lab.py chay ../dap-an/vi_du_nho.py

# %%
import numpy as np
from scipy import stats


def r(a, b):
    return float(np.corrcoef(a, b)[0, 1])


# 4.1 — Pearson, Spearman, chữ U
x = np.array([1, 2, 3, 4, 5.0])
print("4.1 bình phương: Pearson", round(r(x, x**2), 3), "Spearman", round(stats.spearmanr(x, x**2)[0], 3))
u = np.array([-2, -1, 0, 1, 2.0])
print("4.1 chữ U: Pearson", round(r(u, u**2), 3), "tích độ lệch", (u - u.mean()) * (u**2 - (u**2).mean()))

# 4.2 — tương quan giả, Durbin–Watson
a = np.array([2, 3, 5, 6, 8.0])
b = np.array([10, 12, 13, 15, 16.0])
print("4.2 r mức", round(r(a, b), 3), "| sai phân", np.diff(a), np.diff(b), "r", round(r(np.diff(a), np.diff(b)), 3))
for e in (np.array([1, 1, 1, -1, -1, -1.0]), np.array([1, -1, 1, -1, 1, -1.0])):
    print("4.2 DW", e, round(np.sum(np.diff(e) ** 2) / np.sum(e**2), 3))

# 4.3 — CDD/HDD, MI của bảng lạnh/vừa/nóng
t = np.array([10, 18.33, 25, 30])
print("4.3 CDD", np.round(np.maximum(t - 18.33, 0), 2), "HDD", np.round(np.maximum(18.33 - t, 0), 2))
p_xy = {("lạnh", "cao"): 1 / 3, ("vừa", "thấp"): 1 / 3, ("nóng", "cao"): 1 / 3}
p_x = {"lạnh": 1 / 3, "vừa": 1 / 3, "nóng": 1 / 3}
p_y = {"cao": 2 / 3, "thấp": 1 / 3}
mi = sum(p * np.log(p / (p_x[k[0]] * p_y[k[1]])) for k, p in p_xy.items())
print("4.3 MI =", round(mi, 3), "nat; từng ô:", {k: round(p * np.log(p / (p_x[k[0]] * p_y[k[1]])), 3) for k, p in p_xy.items()})
print("4.3 Pearson mã hoá −1,0,1 và 1,0,1:", round(r([-1, 0, 1], [1, 0, 1]), 3))


# 4.4 — CCF thô và sau khi lọc
def ccf(x, y, k):
    x, y = np.asarray(x, float), np.asarray(y, float)
    x, y = (x - x.mean()) / x.std(), (y - y.mean()) / y.std()
    n = x.size
    return float(np.sum(x[: n - k] * y[k:]) / n)


xx = np.array([1, 2, 1, 2, 3, 4, 3, 2, 1, 2, 1, 0.0])       # tổng dồn các bước ±1
yy = np.r_[np.ones(2), xx[:-2]]                            # y chậm 2 bước so với x
print("4.4 y =", yy.astype(int).tolist(), "bước x", np.diff(xx).astype(int).tolist(), "bước y", np.diff(yy).astype(int).tolist())
print("4.4 thô:", [round(ccf(xx, yy, k), 2) for k in range(5)])
dx, dy = np.diff(xx), np.diff(yy)
print("4.4 sau sai phân:", [round(ccf(dx, dy, k), 2) for k in range(5)])

# 4.5 — tương quan trượt
nhiet = np.array([5, 10, 15, 25, 30, 35.0])
tai = np.array([30, 20, 10, 20, 30, 40.0])
print("4.5 cửa sổ đông", round(r(nhiet[:3], tai[:3]), 2), "hè", round(r(nhiet[3:], tai[3:]), 2), "gộp", round(r(nhiet, tai), 3))

# 4.6 — Granger bằng tay: y_t = x_{t-1}
xg = np.array([3, 1, 4, 1, 5, 9.0])
yg = np.array([np.nan, 3, 1, 4, 1, 5])
du_a = yg[2:] - yg[1:-1]            # mô hình A: y hôm nay = y hôm qua
du_b = yg[2:] - xg[1:-1]            # mô hình B: y hôm nay = x hôm qua
print("4.6 sai số A", du_a, "tổng bình phương", np.sum(du_a**2), "| B", du_b, np.sum(du_b**2))
