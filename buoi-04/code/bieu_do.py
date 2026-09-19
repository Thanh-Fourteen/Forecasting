# %% [markdown]
# # Buổi 4 — Bộ 8 biểu đồ chẩn đoán cho một chuỗi theo giờ
#
# Dữ liệu: lượt thuê xe đạp theo giờ, Capital Bikeshare (Washington D.C.) 2011–2012.

# %%
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tv

THU = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
THANG = ["Th1", "Th2", "Th3", "Th4", "Th5", "Th6", "Th7", "Th8", "Th9", "Th10", "Th11", "Th12"]
MAU = {"chinh": "#0072B2", "phu": "#D55E00", "ba": "#009E73", "xam": "#7F7F7F"}
NHAN = ["duong", "mua_vu_tuan", "chuoi_con_thang", "tre", "nhiet_gio_thu", "hop_theo_gio", "phan_tan_nhiet_do", "acf"]


def doc_luot_thue() -> pd.DataFrame:
    """Lượt thuê theo giờ trên LƯỚI GIỜ ĐẦY ĐỦ: giờ không có trong tệp thành NaN (không phải 0)."""
    h = pd.read_csv(tv.THU_MUC_DU_LIEU / "uci-bike-sharing" / "hour.csv", parse_dates=["dteday"])
    h["ds"] = h["dteday"] + pd.to_timedelta(h["hr"], unit="h")
    luoi = pd.date_range(h["ds"].min(), h["ds"].max(), freq="h", name="ds")
    df = h.set_index("ds")[["cnt", "temp", "workingday", "yr"]].reindex(luoi)
    df["gio"] = df.index.hour
    df["thu"] = df.index.dayofweek  # 0 = thứ Hai (pandas) — KHÁC cột weekday của tệp gốc (0 = Chủ nhật)
    df["thang"] = df.index.month
    df["nam"] = df.index.year
    df["workingday"] = df["workingday"].fillna(df.groupby(df.index.normalize())["workingday"].transform("first"))
    return df


# %% [markdown]
# ## Phần tính toán (kiểm được bằng test)

# %%
def ho_so_tuan(df: pd.DataFrame) -> pd.DataFrame:
    """Trung bình lượt thuê theo giờ, trải ra 7 dòng T2..CN × 24 cột 0..23 — dữ liệu của heatmap giờ×thứ."""
    theo_gio = df.groupby("gio")["cnt"].mean()
    return pd.DataFrame([theo_gio.to_numpy()] * 7, index=range(7), columns=range(24))


def acf_nhanh(y, so_tre: int) -> np.ndarray:
    """ACF r_0..r_so_tre, mẫu số là tổng trên cả chuỗi (như FPP); bỏ qua cặp có NaN ở tử số."""
    y = np.asarray(y, dtype=float)
    lech = y - np.nanmean(y)
    mau = np.nansum(lech**2)
    return np.array([1.0] + [np.nansum(lech[k:] * lech[:-k]) / mau for k in range(1, so_tre + 1)])


def cap_tre(y: pd.Series, k: int) -> pd.DataFrame:
    """Cặp (y_{t-k}, y_t) không NaN — dữ liệu của lag plot."""
    return pd.DataFrame({"truoc": y.shift(k), "sau": y}).dropna()


# %% [markdown]
# ## Tám biểu đồ — mỗi hàm vẽ vào một ax, tiêu đề nói kết luận

# %%
def ve_duong(ax, df: pd.DataFrame) -> None:
    ax.plot(df.index, df["cnt"].to_numpy(), color=MAU["chinh"], linewidth=0.3)
    ax.set_title("cnt")


def ve_nhiet_do_truc_kep(ax, df: pd.DataFrame) -> None:
    ngay = df.resample("D").agg({"cnt": "sum", "temp": "mean"})
    ax.plot(ngay.index, ngay["cnt"], color=MAU["chinh"])
    ax.set_ylim(3000, 9000)
    ax2 = ax.twinx()
    ax2.plot(ngay.index, ngay["temp"] * 41, color=MAU["phu"])
    ax.set_title("cnt, temp")


def bo_bieu_do_chan_doan(df: pd.DataFrame) -> plt.Figure:
    """Bộ biểu đồ chẩn đoán; mỗi ax gắn nhãn (ax.get_label())."""
    fig, (a, b) = plt.subplots(2, 1, figsize=(12, 7))
    ve_duong(a, df)
    a.set_label("duong")
    ve_nhiet_do_truc_kep(b, df)
    b.set_label("nhiet_do")
    fig.tight_layout()
    return fig


# %% [markdown]
# ## Biểu đồ gây hiểu nhầm và bản vẽ lại

# %%
def bieu_do_gay_hieu_nham(df: pd.DataFrame) -> plt.Figure:
    """Dựng sẵn: trục kép lượt thuê/nhiệt độ theo tháng 2012, trục y cắt — ĐỪNG sửa hàm này."""
    thang = df[df["nam"] == 2012].resample("MS").agg({"cnt": "sum", "temp": "mean"})
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(thang.index, thang["cnt"], color=MAU["chinh"], marker="o")
    ax.set_ylim(90_000, 220_000)
    ax2 = ax.twinx()
    ax2.plot(thang.index, thang["temp"] * 41, color=MAU["phu"], marker="s")
    ax2.set_ylim(5, 32)
    ax.set_title("Lượt thuê bám sát nhiệt độ")
    return fig


def ve_lai_trung_thuc(df: pd.DataFrame) -> plt.Figure:
    """Vẽ lại cho trung thực."""
    return bieu_do_gay_hieu_nham(df)


# %%
if __name__ == "__main__":
    df = doc_luot_thue()
    print(f"{len(df)} giờ trên lưới, thiếu {df['cnt'].isna().sum()}")
    print(ho_so_tuan(df).loc[:, [8, 13, 17]].round(0))
    r = acf_nhanh(df["cnt"], 168)
    print("ACF trễ 12, 24, 168:", np.round(r[[12, 24, 168]], 3))
    print("số ô biểu đồ:", len(bo_bieu_do_chan_doan(df).axes))
