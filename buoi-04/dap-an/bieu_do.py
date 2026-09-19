# %% [markdown]
# # Buổi 4 — Bộ 8 biểu đồ chẩn đoán cho một chuỗi theo giờ
#
# Bản ĐÃ SỬA. Dữ liệu: lượt thuê xe đạp theo giờ, Capital Bikeshare (Washington D.C.) 2011–2012.

# %%
from __future__ import annotations

import matplotlib.dates
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
    """Trung bình lượt thuê theo (thứ, giờ): 7 dòng T2..CN × 24 cột 0..23 — dữ liệu của heatmap giờ×thứ."""
    bang = df.pivot_table(index="thu", columns="gio", values="cnt", aggfunc="mean")
    return bang.reindex(index=range(7), columns=range(24))


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
    ngay = df["cnt"].resample("D").sum(min_count=12)
    ax.plot(ngay.index, ngay.to_numpy(), color=MAU["xam"], linewidth=0.5)
    ax.plot(ngay.index, ngay.rolling(28, center=True, min_periods=14).mean().to_numpy(), color=MAU["chinh"])
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator(bymonth=[1, 7]))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m/%Y"))
    ax.set_ylabel("lượt / ngày")
    ax.set_title("Tổng theo ngày: 2012 cao hơn 2011, đỉnh hè – đáy đông")


def ve_mua_vu_tuan(ax, df: pd.DataFrame) -> None:
    gio_tuan = df["thu"] * 24 + df["gio"]
    tuan = df.index.to_period("W-SUN")
    bang = df.assign(gio_tuan=gio_tuan, tuan=tuan).pivot_table(index="gio_tuan", columns="tuan", values="cnt")
    ax.plot(bang.index, bang.to_numpy(), color=MAU["xam"], linewidth=0.3, alpha=0.3)
    ax.plot(bang.index, bang.median(axis=1).to_numpy(), color=MAU["phu"], linewidth=1.5)
    ax.set_xticks(range(0, 168, 24), THU)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("giờ trong tuần (vạch = 0h của mỗi thứ)")
    ax.set_ylabel("lượt / giờ")
    ax.set_title("Mỗi tuần một đường: T2–T6 hai đỉnh, T7–CN một đỉnh")


def ve_chuoi_con_thang(ax, df: pd.DataFrame) -> None:
    ngay = df["cnt"].resample("D").sum(min_count=12).to_frame("cnt")
    ngay["thang"] = ngay.index.month
    for m in range(1, 13):
        v = ngay.loc[ngay["thang"] == m, "cnt"].to_numpy()
        x = m - 1 + np.linspace(0.05, 0.85, v.size)
        ax.plot(x, v, color=MAU["chinh"], linewidth=0.5)
        ax.hlines(np.nanmean(v), m - 1 + 0.05, m - 1 + 0.85, color=MAU["phu"])
    ax.set_xticks(np.arange(12) + 0.45, THANG, fontsize=7)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("lượt / ngày")
    ax.set_title("Chuỗi con theo tháng: mọi tháng đều nhảy bậc sang 2012")


def ve_tre(ax, df: pd.DataFrame, cac_tre=(1, 12, 24, 168)) -> None:
    """Bốn lag plot nhỏ lồng trong ax (lưới 2×2), mỗi ô có đường chéo và hệ số tương quan."""
    ax.set_axis_off()
    for i, k in enumerate(cac_tre):
        o = ax.inset_axes([0.1 + (i % 2) * 0.5, 0.58 - (i // 2) * 0.53, 0.36, 0.36])
        cap = cap_tre(df["cnt"], k)
        o.scatter(cap["truoc"], cap["sau"], s=0.5, alpha=0.1, color=MAU["chinh"])
        o.plot([0, 1000], [0, 1000], color=MAU["phu"], linewidth=0.8)
        o.set_aspect("equal")
        o.set_xlim(0, 1000)
        o.set_ylim(0, 1000)
        o.tick_params(labelsize=6)
        o.set_xlabel(f"lượt lúc t − {k} giờ", fontsize=6)
        o.set_ylabel("lượt lúc t", fontsize=6)
        o.set_title(f"trễ {k} giờ: r = {cap.corr().iloc[0, 1]:.2f}", fontsize=7)
    ax.set_title("Trễ 168 bám đường chéo nhất, trễ 12 tản thành hai nhánh")


def ve_nhiet_gio_thu(ax, df: pd.DataFrame) -> None:
    bang = ho_so_tuan(df)
    anh = ax.imshow(bang.to_numpy(), aspect="auto", cmap="viridis")
    ax.set_yticks(range(7), THU)
    ax.set_xticks(range(0, 24, 3))
    ax.set_xlabel("giờ")
    plt.colorbar(anh, ax=ax, shrink=0.8, label="lượt / giờ (trung bình)")
    ax.set_title("Giờ × thứ: 8h và 17h chỉ sáng vào ngày làm việc")


def ve_hop_theo_gio(ax, df: pd.DataFrame) -> None:
    for lam, lech, c, ten in ((1, -0.2, MAU["chinh"], "ngày làm việc"), (0, 0.2, MAU["phu"], "ngày nghỉ")):
        phan = df[df["workingday"] == lam]
        du = [phan.loc[phan["gio"] == g, "cnt"].dropna().to_numpy() for g in range(24)]
        hop = ax.boxplot(du, positions=np.arange(24) + lech, widths=0.35, patch_artist=True, showfliers=False,
                         manage_ticks=False)
        for p in hop["boxes"]:
            p.set_facecolor(c)
            p.set_alpha(0.6)
        ax.plot([], [], color=c, linewidth=6, label=ten)
    ax.set_xticks(range(0, 24, 3))
    ax.set_xlabel("giờ")
    ax.set_ylabel("lượt / giờ")
    ax.legend(fontsize=7)
    ax.set_title("Phân phối theo giờ: ngày nghỉ đỉnh trưa, ngày làm việc đỉnh 8h/17h")


def ve_phan_tan_nhiet_do(ax, df: pd.DataFrame) -> None:
    ngay = df.resample("D").agg({"cnt": "sum", "temp": "mean", "nam": "first"}).dropna()
    for nam, c in ((2011, MAU["chinh"]), (2012, MAU["phu"])):
        p = ngay[ngay["nam"] == nam]
        ax.scatter(p["temp"] * 41, p["cnt"], s=4, color=c, alpha=0.6, label=str(nam))
    ax.set_xlabel("nhiệt độ trung bình ngày (°C, theo Readme: temp × 41)")
    ax.set_ylabel("lượt / ngày")
    ax.legend(fontsize=7)
    ax.set_title("Cùng nhiệt độ, 2012 cao hơn 2011: quan hệ dời theo năm")


def ve_acf(ax, df: pd.DataFrame, so_tre: int = 336) -> None:
    r = acf_nhanh(df["cnt"], so_tre)
    ax.vlines(range(so_tre + 1), 0, r, color=MAU["chinh"], linewidth=0.8)
    dai = 1.96 / np.sqrt(df["cnt"].notna().sum())
    ax.axhspan(-dai, dai, color=MAU["xam"], alpha=0.3)
    for k in (24, 168, 336):
        ax.axvline(k, color=MAU["phu"], linewidth=0.6, linestyle="--")
    ax.set_xlabel("độ trễ k (giờ)")
    ax.set_ylabel("hệ số tự tương quan r_k")
    ax.set_title("ACF: đỉnh ở 24 và cao hơn ở 168 — mùa vụ ngày lồng mùa vụ tuần")


def bo_bieu_do_chan_doan(df: pd.DataFrame) -> plt.Figure:
    """Bộ 8 biểu đồ chẩn đoán trên lưới 4×2; mỗi ax gắn nhãn (ax.get_label()) theo NHAN."""
    fig, truc = plt.subplots(4, 2, figsize=(12, 15))
    ham = [ve_duong, ve_mua_vu_tuan, ve_chuoi_con_thang, ve_tre, ve_nhiet_gio_thu, ve_hop_theo_gio,
           ve_phan_tan_nhiet_do, ve_acf]
    for ax, f, nhan in zip(truc.flat, ham, NHAN, strict=True):
        f(ax, df)
        ax.set_label(nhan)
        ax.title.set_fontsize(9)
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
    """Vẽ lại: hai bảng xếp dọc (không trục kép), lượt thuê từ 0, và scatter để nói về quan hệ."""
    thang = df[df["nam"] == 2012].resample("MS").agg({"cnt": "sum", "temp": "mean"})
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(12, 3.5))
    a.plot(thang.index, thang["cnt"], color=MAU["chinh"], marker="o")
    a.set_ylim(bottom=0)
    a.set_ylabel("lượt / tháng")
    a.set_title("Lượt thuê 2012 theo tháng (trục từ 0)")
    b.plot(thang.index, thang["temp"] * 41, color=MAU["phu"], marker="s")
    b.set_ylim(bottom=0)
    b.set_ylabel("°C")
    b.set_title("Nhiệt độ trung bình (°C)")
    for ax in (a, b):
        ax.tick_params(axis="x", labelrotation=45)
    c.scatter(thang["temp"] * 41, thang["cnt"], color=MAU["chinh"])
    for t, hang in thang.iterrows():
        c.annotate(f"{t.month}", (hang["temp"] * 41, hang["cnt"]), fontsize=7)
    c.set_ylim(bottom=0)
    c.set_ylabel("lượt / tháng")
    c.set_xlabel("nhiệt độ trung bình tháng (°C)")
    c.set_title(f"Quan hệ: r = {thang['cnt'].corr(thang['temp']):.2f}, T9–T10 lệch khỏi nhiệt độ")
    fig.tight_layout()
    return fig


# %%
if __name__ == "__main__":
    df = doc_luot_thue()
    print(f"{len(df)} giờ trên lưới, thiếu {df['cnt'].isna().sum()}")
    print(ho_so_tuan(df).loc[:, [8, 13, 17]].round(0))
    r = acf_nhanh(df["cnt"], 168)
    print("ACF trễ 12, 24, 168:", np.round(r[[12, 24, 168]], 3))
    print("số ô biểu đồ:", len(bo_bieu_do_chan_doan(df).axes))
