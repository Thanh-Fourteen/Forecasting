# %% [markdown]
# # Ví dụ số nhỏ cho mục 4.8 — chọn lượng điện mua khi thiếu đắt hơn thừa
#
# Không cần dữ liệu. In ra mọi con số dùng trong tai-lieu.md mục 4.8 (phần "Ví dụ số nhỏ").
# Chạy: `make -C ../lab ...` không cần — `python vi_du_quantile.py` với bất kỳ Python 3 + NumPy.

# %%
import numpy as np

CU, CO = 4, 1  # đồng mất cho mỗi kWh thiếu / thừa
nhu_cau = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])  # kWh, 10 ngày, cùng một giờ


def chi_phi(mua: float, y=nhu_cau) -> float:
    """Tổng chi phí 10 ngày nếu ngày nào cũng mua `mua` kWh."""
    thieu = np.clip(y - mua, 0, None)   # nhu cầu vượt lượng mua
    thua = np.clip(mua - y, 0, None)    # lượng mua vượt nhu cầu
    return float(CU * thieu.sum() + CO * thua.sum())


# %%
print("nhu cầu:", nhu_cau.tolist())
print("xếp tăng dần:", np.sort(nhu_cau).tolist())
print("trung bình:", nhu_cau.mean())
for mua in range(6, 13):
    y = nhu_cau
    print(f"mua {mua:>2}: số ngày thiếu {int((y > mua).sum())}, kWh thiếu {int(np.clip(y - mua, 0, None).sum())}, "
          f"kWh thừa {int(np.clip(mua - y, 0, None).sum())}, tổng chi phí {chi_phi(mua):.0f} đồng")
print("mua theo trung bình 7,7:", chi_phi(7.7))
print("quantile 0,8 (np.quantile):", np.quantile(nhu_cau, CU / (CU + CO)))
print("quantile 0,5 (trung vị):", np.quantile(nhu_cau, 0.5))
print("tỷ lệ tới hạn:", CU / (CU + CO))
