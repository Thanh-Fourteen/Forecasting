# %% [markdown]
# # Buổi 6 — ví dụ số nhỏ trong tai-lieu.md (không cần dữ liệu). Chạy: python lab.py chay ../dap-an/vi_du_nho.py

# %%
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# 4.1 — 12 quý (3 năm), chu kỳ m = 4
y = np.array([22, 18, 15, 29, 30, 22, 19, 33, 30, 26, 23, 37], dtype=float)
m = 4
w = np.r_[0.5, np.ones(m - 1), 0.5] / m                    # 2×4-MA: 1/8, 1/4, 1/4, 1/4, 1/8
T = np.full(y.size, np.nan)
T[m // 2: -m // 2] = np.convolve(y, w, mode="valid")
lech = y - T
pha = np.arange(y.size) % m
S_mua = np.array([np.nanmean(lech[pha == k]) for k in range(m)])
print("trung bình lệch theo quý (trước khi trừ):", np.round(S_mua, 4), "tổng", round(S_mua.sum(), 4))
S_mua -= S_mua.mean()
S = S_mua[pha]
R = y - T - S
print(pd.DataFrame({"y": y, "T": T, "y-T": lech, "S": S, "R": R}).round(3).to_string())
kq = seasonal_decompose(y, period=m)
print("khớp statsmodels:", np.allclose(kq.trend, T, equal_nan=True), np.allclose(kq.seasonal, S))

# 4.5 — độ mạnh trên chính ví dụ này (bỏ 4 điểm không có xu hướng)
ok = ~np.isnan(T)
vR, vTR, vSR = np.var(R[ok], ddof=1), np.var((T + R)[ok], ddof=1), np.var((S + R)[ok], ddof=1)
print("Var R, Var T+R, Var S+R:", round(vR, 4), round(vTR, 4), round(vSR, 4))
print("F_T =", round(max(0, 1 - vR / vTR), 3), " F_S =", round(max(0, 1 - vR / vSR), 3))

# 4.6 — trọng số robust bisquare
r = np.array([1.0, -2.0, 1.0, 20.0, -1.0])
h = 6 * np.median(np.abs(r))
u = np.abs(r) / h
rho = np.where(u < 1, (1 - u**2) ** 2, 0.0)
print("h =", h, "u =", np.round(u, 3), "trọng số =", np.round(rho, 3))
