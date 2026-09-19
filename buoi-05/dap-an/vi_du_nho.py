# %% [markdown]
# # Buổi 5 — các ví dụ số nhỏ trong tai-lieu.md (không cần dữ liệu). Chạy: python lab.py chay ../dap-an/vi_du_nho.py

# %%
import numpy as np

# 4.1 — điều chỉnh lịch: tháng 2 (28 ngày) và tháng 3 (31 ngày), bán đều 10 tỷ mỗi ngày
t2, t3 = 280, 310
print("4.1 thô:", round((t3 / t2 - 1) * 100, 1), "% | theo ngày:", t2 / 28, t3 / 31)

# 4.2 — lạm phát và dân số
doanh_thu, cpi, dan_so = np.array([100, 150]), np.array([100, 125]), np.array([10, 12])
thuc = doanh_thu / cpi * cpi[0]
print("4.2 giá thực:", thuc, "| trên đầu người:", thuc / dan_so)

# 4.3 — log biến "tăng 20%" thành cùng một khoảng
print("4.3 log:", np.round(np.log([100, 120, 1000, 1200]), 3), "| hiệu:", round(np.log(1.2), 3))


# 4.4 — Box-Cox và tiêu chí Guerrero trên 3 khối
def boxcox(y, lam):
    y = np.asarray(y, dtype=float)
    return np.log(y) if lam == 0 else (np.sign(y) * np.abs(y) ** lam - 1) / lam


print("4.4 y = 100:", {lam: round(float(boxcox(100, lam)), 3) for lam in (1, 0.5, 0)})
tb, sd = np.array([100, 400, 900]), np.array([10, 20, 30])
for lam in (1, 0.5, 0):
    ty_so = sd / tb ** (1 - lam)
    print(f"4.4 λ = {lam}: tỷ số", np.round(ty_so, 3), "CV", round(float(ty_so.std(ddof=1) / ty_so.mean()), 3))

# 4.5 — đổi ngược cho trung vị; hiệu chỉnh bias
w = np.array([0.0, 1.0, 2.0])
print("4.5 exp:", np.round(np.exp(w), 2), "| exp(trung bình log):", round(float(np.exp(w.mean())), 2),
      "| trung bình thật:", round(float(np.exp(w).mean()), 2))
w_hat, s2 = 4.6, 0.04
print("4.5 thẳng:", round(float(np.exp(w_hat)), 1), "| FPP:", round(float(np.exp(w_hat) * (1 + s2 / 2)), 1),
      "| chính xác:", round(float(np.exp(w_hat + s2 / 2)), 1))
