# %% [markdown]
# # Buổi 7 — ví dụ số nhỏ trong tai-lieu.md (không cần dữ liệu). Chạy: python lab.py chay ../dap-an/vi_du_nho.py

# %%
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import acf, pacf


def r(y, k):
    lech = np.asarray(y, float) - np.mean(y)
    return float(np.sum(lech[k:] * lech[:-k]) / np.sum(lech**2))


# 4.1 — ACF trễ 1 trên 6 số
y = [2, 3, 5, 6, 5, 3]
print("4.1 trung bình", np.mean(y), "r1 =", round(r(y, 1), 3), "r2 =", round(r(y, 2), 3),
      "statsmodels:", np.round(acf(y, nlags=2, adjusted=False), 3))

# 4.2 — PACF trễ 2 từ r1, r2
for r1, r2 in ((0.7, 0.49), (0.5, 0.4)):
    print("4.2 r1, r2 =", r1, r2, "→ PACF(2) =", round((r2 - r1**2) / (1 - r1**2), 3))
print("4.2 statsmodels pacf trên y:", np.round(pacf(y, nlags=2, method="ywm"), 3),
      "tay:", round((r(y, 2) - r(y, 1) ** 2) / (1 - r(y, 1) ** 2), 3))

# 4.3 — Ljung-Box tay
T, rk = 100, np.array([0.2, 0.1])
Q = T * (T + 2) * np.sum(rk**2 / (T - np.arange(1, 3)))
print("4.3 Q* =", round(Q, 2), "p =", round(stats.chi2.sf(Q, 2), 3), "ngưỡng 5% (2 bậc):", round(stats.chi2.ppf(0.95, 2), 2),
      "ngưỡng 10 bậc:", round(stats.chi2.ppf(0.95, 10), 2))

# 4.4 — random walk từ tung đồng xu
e = np.array([1, -1, 1, 1, -1, 1])
print("4.4 bước:", e, "→ vị trí:", e.cumsum())
rng = np.random.default_rng(7)
walks = rng.choice([-1, 1], size=(10_000, 100)).cumsum(axis=1)
print("4.4 độ lệch chuẩn vị trí sau 4, 25, 100 bước (10.000 lần):", np.round(walks[:, [3, 24, 99]].std(axis=0), 2))

# 4.6 — sai phân thừa trên chuỗi đã dừng
w = np.array([2, -1, 0, 1, -2, 0])
d = np.diff(w)
print("4.6 sai phân:", d, "sd trước", round(w.std(ddof=1), 3), "sd sau", round(d.std(ddof=1), 3), "r1 sau", round(r(d, 1), 3))
