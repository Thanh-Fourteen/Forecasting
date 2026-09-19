# %% [markdown]
# # Buổi 4 — các ví dụ số nhỏ trong tai-lieu.md (không cần dữ liệu). Chạy: python lab.py chay ../dap-an/vi_du_nho.py

# %%
import numpy as np

# 4.1 — hai tuần lượt thuê theo ngày (trăm lượt), T2..CN
tuan = np.array([[10, 12, 12, 12, 14, 6, 4],
                 [12, 14, 14, 14, 16, 8, 6]])
tb_tuan = tuan.mean(axis=1)
print("4.1 trung bình mỗi tuần:", tb_tuan)                       # [10. 12.] → xu hướng +2 mỗi tuần
print("4.1 lệch khỏi trung bình tuần:", tuan - tb_tuan[:, None])  # hai dòng giống nhau → mùa vụ tuần

# 4.2 — làm trơn che ngoại lai; thang log
ngay = np.array([50, 52, 48, 2, 51, 49, 50])
print("4.2 trung bình 3 ngày quanh ngày 4:", round(ngay[2:5].mean(), 1), "| trung bình 7 ngày:", round(ngay.mean(), 1))
y = np.array([100, 200, 400, 500])
print("4.2 tăng tuyệt đối:", np.diff(y), "| tỷ lệ:", y[1:] / y[:-1], "| log10:", np.round(np.log10(y), 3),
      "| bước log10:", np.round(np.diff(np.log10(y)), 3))

# 4.3 — seasonal plot và subseries plot của chính hai tuần ở 4.1
print("4.3 trung bình mỗi thứ (vạch ngang của subseries):", tuan.mean(axis=0))

# 4.4 — ô (T2, 8h) của heatmap qua 5 tuần; tuần thứ hai là ngày lễ
o = np.array([420, 60, 450, 410, 440])
print("4.4 trung bình:", o.mean(), "| trung vị:", np.median(o), "| quantile 0,25 và 0,75:", np.quantile(o, [0.25, 0.75]))


# 4.5 — tự tương quan của chuỗi lặp mỗi 4 bước
def r(y, k):
    lech = y - y.mean()
    return np.sum(lech[k:] * lech[:-k]) / np.sum(lech**2)


y = np.array([2, 4, 6, 4, 2, 4, 6, 4], dtype=float)
print("4.5 r1, r2, r4:", [round(float(r(y, k)), 3) for k in (1, 2, 4)])
print("4.5 cặp (y_{t-2}, y_t):", [(int(a), int(b)) for a, b in zip(y[:-2], y[2:], strict=True)])

# 4.6 — trục y cắt và trục kép
thang5, thang6, day_truc, dinh_truc = 490, 510, 480, 520
cao = lambda v: (v - day_truc) / (dinh_truc - day_truc)   # noqa: E731 — phần chiều cao hình
print("4.6 chiều cao T5, T6 trên trục 480–520:", cao(thang5), cao(thang6), "| tỷ lệ thật:", round(thang6 / thang5, 3))
a, b = np.array([1.0, 2.0, 3.0]), np.array([20.0, 21.0, 22.0])
print("4.6 tăng A:", a[-1] / a[0] - 1, "| tăng B:", round(b[-1] / b[0] - 1, 3))
print("4.6 B trên trục 20–22 (phần chiều cao):", (b - 20) / 2, "| A trên trục 1–3:", (a - 1) / 2)
