# BẢN SAO của tools/khung/ve.py — SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/khung/ve.py rồi chạy lại tool.
"""Vẽ biểu đồ theo một phong cách thống nhất cho cả khoá (Phụ lục C: cách đọc từng loại).

    from tv import ve
    with ve.phong_cach():
        fig = ve.bo_bieu_do_chan_doan(y, x=nhiet_do, ten_x="Nhiệt độ (°C)", don_vi="lượt/giờ")
        ve.luu_hinh(fig, "hinh/chan-doan.png")

Quy ước: tiêu đề hình nói KẾT LUẬN (truyền qua `tieu_de`), trục có đơn vị, 150 dpi.
Cần matplotlib, numpy, pandas; không import module khác của tv.
"""
from __future__ import annotations

from collections.abc import Sequence
from contextlib import contextmanager
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__all__ = ["MAU", "phong_cach", "luu_hinh", "acf", "bo_bieu_do_chan_doan", "fan_chart",
           "pit_histogram", "reliability_diagram", "small_multiples"]

# bảng màu phân biệt được cho người mù màu đỏ–lục (Okabe–Ito)
MAU = {"chinh": "#0072B2", "phu": "#D55E00", "ba": "#009E73", "bon": "#CC79A7",
       "xam": "#7F7F7F", "vang": "#E69F00", "nhat": "#56B4E9"}

_RC = {
    "figure.dpi": 100, "savefig.dpi": 150, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans",        # có đủ dấu tiếng Việt
    "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold", "axes.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.3, "grid.linewidth": 0.6,
    "axes.prop_cycle": plt.cycler(color=[MAU[k] for k in ("chinh", "phu", "ba", "bon", "vang", "nhat")]),
    "legend.frameon": False, "lines.linewidth": 1.0,
}


@contextmanager
def phong_cach():
    """Ngữ cảnh rcParams của khoá — mọi hình trong khối `with` dùng chung phong cách."""
    with plt.rc_context(_RC):
        yield


def luu_hinh(fig, duong_dan: str | Path, dpi: int = 150) -> Path:
    p = Path(duong_dan)
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return p


def acf(y, so_tre: int) -> np.ndarray:
    """ACF mẫu theo FPP 2.8: r_k = Σ(y_t - ȳ)(y_{t-k} - ȳ) / Σ(y_t - ȳ)². Bỏ qua NaN ở cả hai vế."""
    x = np.asarray(y, dtype=float)
    x = x - np.nanmean(x)
    mau = np.nansum(x * x)
    if mau == 0:
        raise ValueError("chuỗi hằng số — ACF không xác định")
    return np.array([1.0] + [np.nansum(x[k:] * x[:-k]) / mau for k in range(1, so_tre + 1)])


# ---------------------------------------------------------------------------- 8 biểu đồ chẩn đoán


def _loai_tan_suat(idx: pd.DatetimeIndex) -> str:
    buoc = pd.Series(idx).diff().median()
    if buoc < pd.Timedelta(days=1):
        return "gio"
    if buoc < pd.Timedelta(days=28):
        return "ngay"
    return "thang"


def bo_bieu_do_chan_doan(y: pd.Series, x: pd.Series | None = None, ten_x: str | None = None,
                         lam_viec: pd.Series | None = None, don_vi: str = "", tieu_de: str | None = None,
                         so_tre_acf: int | None = None):
    """Bộ 8 biểu đồ chẩn đoán (buổi 4) cho MỘT chuỗi có DatetimeIndex, trả Figure 4×2.

    1 đường theo thời gian · 2 seasonal plot · 3 subseries theo tháng · 4 lag plot · 5 heatmap lịch ·
    6 boxplot theo chu kỳ (tách ngày làm việc/nghỉ với dữ liệu giờ) · 7 scatter với biến x tô màu
    theo năm (không có x: histogram) · 8 ACF với dải ±1.96/√T.

    Dữ liệu giờ: mùa vụ tuần (168), heatmap giờ × thứ. Dữ liệu ngày: tuần (7), heatmap thứ × tháng.
    Dữ liệu tháng trở lên: năm (12), heatmap tháng × năm.
    lam_viec: Series bool cùng index (ngày làm việc); mặc định thứ Hai–Sáu.
    """
    if not isinstance(y.index, pd.DatetimeIndex):
        raise TypeError("y cần DatetimeIndex")
    y = y.sort_index()
    if y.index.has_duplicates:
        raise ValueError("index của y có mốc trùng — gộp trước khi vẽ")
    loai = _loai_tan_suat(y.index)
    idx = y.index
    don_vi_nhan = f" ({don_vi})" if don_vi else ""

    fig, axes = plt.subplots(4, 2, figsize=(11, 13))
    a = axes.ravel()

    # 1. đường
    a[0].plot(idx, y.to_numpy(), color=MAU["chinh"], linewidth=0.5 if len(y) > 2000 else 1.0)
    a[0].set_title("1. Chuỗi theo thời gian")
    a[0].set_ylabel(str(y.name or "y") + don_vi_nhan)

    # 2. seasonal plot
    if loai == "gio":
        vi_tri = idx.dayofweek * 24 + idx.hour
        nhom, nhan_x, mua = idx.to_period("W").astype(str), "Giờ trong tuần (0 = 0h thứ Hai)", 168
    elif loai == "ngay":
        vi_tri = idx.dayofweek
        nhom, nhan_x, mua = idx.to_period("W").astype(str), "Thứ (0 = thứ Hai)", 7
    else:
        vi_tri = idx.month
        nhom, nhan_x, mua = idx.year.astype(str), "Tháng", 12
    bang = pd.DataFrame({"vi_tri": vi_tri, "nhom": nhom, "y": y.to_numpy()})
    cac_nhom = list(dict.fromkeys(bang["nhom"]))[-52:]
    cmap = plt.get_cmap("viridis")
    for i, ten_nhom in enumerate(cac_nhom):
        g = bang[bang["nhom"] == ten_nhom].sort_values("vi_tri")
        a[1].plot(g["vi_tri"], g["y"], color=cmap(i / max(len(cac_nhom) - 1, 1)), alpha=0.5, linewidth=0.7)
    a[1].set_title(f"2. Seasonal plot ({len(cac_nhom)} {'năm' if loai == 'thang' else 'tuần'} gần nhất, "
                   "đậm dần = mới hơn)")
    a[1].set_xlabel(nhan_x)

    # 3. subseries theo tháng: trung bình mỗi (năm, tháng), đường ngang = trung bình của tháng
    tb_thang = y.groupby([idx.month, idx.year]).mean()
    for thang in range(1, 13):
        if thang not in tb_thang.index.get_level_values(0):
            continue
        s = tb_thang.loc[thang]
        xs = thang - 0.35 + 0.7 * np.arange(len(s)) / max(len(s) - 1, 1)
        a[2].plot(xs, s.to_numpy(), color=MAU["chinh"], marker=".", markersize=3)
        a[2].hlines(s.mean(), thang - 0.4, thang + 0.4, color=MAU["phu"], linewidth=1.5)
    a[2].set_xticks(range(1, 13))
    a[2].set_title("3. Subseries theo tháng (điểm = trung bình từng năm, vạch = trung bình tháng)")
    a[2].set_xlabel("Tháng")

    # 4. lag plot: trễ 1 và trễ mùa vụ ngắn
    tre_mua = {"gio": 24, "ngay": 7, "thang": 12}[loai]
    for tre, mau in ((1, MAU["chinh"]), (tre_mua, MAU["phu"])):
        a[3].scatter(y.shift(tre).to_numpy(), y.to_numpy(), s=2, alpha=0.25, color=mau, label=f"trễ {tre}")
    a[3].set_title("4. Lag plot")
    a[3].set_xlabel("y(t - k)")
    a[3].set_ylabel("y(t)")
    a[3].legend(markerscale=5)

    # 5. heatmap lịch
    if loai == "gio":
        hm = y.groupby([idx.hour, idx.dayofweek]).mean().unstack()
        a[4].set_ylabel("Giờ")
        a[4].set_xlabel("Thứ (0 = thứ Hai)")
    elif loai == "ngay":
        hm = y.groupby([idx.dayofweek, idx.month]).mean().unstack()
        a[4].set_ylabel("Thứ (0 = thứ Hai)")
        a[4].set_xlabel("Tháng")
    else:
        hm = y.groupby([idx.month, idx.year]).mean().unstack()
        a[4].set_ylabel("Tháng")
        a[4].set_xlabel("Năm")
    anh = a[4].imshow(hm.to_numpy(), aspect="auto", cmap="viridis", origin="upper")
    a[4].set_yticks(range(len(hm.index)), [str(v) for v in hm.index], fontsize=6)
    a[4].set_xticks(range(len(hm.columns)), [str(v) for v in hm.columns], fontsize=6)
    a[4].grid(False)
    fig.colorbar(anh, ax=a[4], label="trung bình" + don_vi_nhan)
    a[4].set_title("5. Heatmap lịch (trung bình)")

    # 6. boxplot theo chu kỳ
    if loai == "gio":
        lv = lam_viec.reindex(idx, fill_value=False).to_numpy(dtype=bool) if lam_viec is not None \
            else (idx.dayofweek < 5)
        for co, mau, lech, nhan in ((True, MAU["chinh"], -0.2, "ngày làm việc"), (False, MAU["phu"], 0.2, "ngày nghỉ")):
            du_lieu = [y.to_numpy()[(idx.hour == g) & (lv == co)] for g in range(24)]
            bp = a[5].boxplot(du_lieu, positions=np.arange(24) + lech, widths=0.35, patch_artist=True,
                              showfliers=False, manage_ticks=False)
            for hop in bp["boxes"]:
                hop.set_facecolor(mau)
                hop.set_alpha(0.5)
            a[5].plot([], [], color=mau, linewidth=6, alpha=0.5, label=nhan)
        a[5].set_xticks(range(0, 24, 3))
        a[5].set_xlabel("Giờ")
        a[5].legend()
    else:
        khoa = idx.dayofweek if loai == "ngay" else idx.month
        nhan = sorted(set(khoa))
        a[5].boxplot([y.to_numpy()[khoa == k] for k in nhan], showfliers=False)
        a[5].set_xticks(range(1, len(nhan) + 1), [str(k) for k in nhan])
        a[5].set_xlabel("Thứ (0 = thứ Hai)" if loai == "ngay" else "Tháng")
    a[5].set_title("6. Phân phối theo chu kỳ (không vẽ điểm ngoại lai)")

    # 7. scatter với x tô màu theo năm, hoặc histogram
    if x is not None:
        x = x.reindex(idx)
        cac_nam = sorted(set(idx.year))
        for i, nam in enumerate(cac_nam):
            chon = idx.year == nam
            a[6].scatter(x.to_numpy()[chon], y.to_numpy()[chon], s=3, alpha=0.3,
                         color=cmap(i / max(len(cac_nam) - 1, 1)), label=str(nam))
        a[6].set_xlabel(ten_x or (x.name or "x"))
        a[6].set_ylabel(y.name or "y")
        a[6].legend(markerscale=4, fontsize=7)
        a[6].set_title("7. Quan hệ với biến giải thích, tô màu theo năm")
    else:
        a[6].hist(y.dropna().to_numpy(), bins=50, color=MAU["chinh"], alpha=0.8)
        a[6].set_title("7. Phân phối giá trị")
        a[6].set_xlabel((y.name or "y") + don_vi_nhan)

    # 8. ACF
    so_tre = so_tre_acf or min(2 * mua, len(y) // 4)
    r = acf(y.to_numpy(), so_tre)
    a[7].vlines(range(1, so_tre + 1), 0, r[1:], color=MAU["chinh"], linewidth=0.8)
    bien = 1.96 / np.sqrt(int(y.notna().sum()))
    a[7].axhline(bien, color=MAU["phu"], linestyle="--", linewidth=0.8)
    a[7].axhline(-bien, color=MAU["phu"], linestyle="--", linewidth=0.8)
    a[7].axhline(0, color="black", linewidth=0.5)
    a[7].set_title(f"8. ACF (dải ±1.96/√T = ±{bien:.3f})")
    a[7].set_xlabel("Trễ k")

    if tieu_de:
        fig.suptitle(tieu_de, fontsize=12, fontweight="bold", y=1.0)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------- bất định


def fan_chart(ax, lich_su: pd.Series, du_bao: pd.DataFrame, muc_giua: float = 0.5,
              tieu_de: str | None = None, don_vi: str = ""):
    """Fan chart từ dự báo quantile.

    du_bao: index là thời điểm tương lai, cột là mức quantile (float, vd 0.05, 0.25, 0.5, 0.75, 0.95).
    Mỗi cặp (q, 1-q) tô một dải, dải trong đậm hơn. Chú giải ghi rõ mức — dải là khoảng quantile đối
    xứng, KHÔNG phải kiểu dải xác suất quanh mode của Bank of England (Phụ lục C mục 13).
    """
    muc = sorted(float(c) for c in du_bao.columns)
    thap = [q for q in muc if q < 0.5 and any(np.isclose(1 - q, m) for m in muc)]
    if muc_giua not in muc and not any(np.isclose(muc_giua, m) for m in muc):
        raise ValueError(f"du_bao thiếu cột quantile {muc_giua}")
    cot = {float(c): c for c in du_bao.columns}
    ax.plot(lich_su.index, lich_su.to_numpy(), color="black", linewidth=1.0, label="thực tế")
    for i, q in enumerate(sorted(thap)):
        cao = next(m for m in muc if np.isclose(1 - q, m))
        ax.fill_between(du_bao.index, du_bao[cot[q]].to_numpy(dtype=float), du_bao[cot[cao]].to_numpy(dtype=float),
                        color=MAU["chinh"], alpha=0.15 + 0.5 * i / max(len(thap), 1), linewidth=0,
                        label=f"khoảng {round((cao - q) * 100)}%")
    giua = next(m for m in muc if np.isclose(m, muc_giua))
    ax.plot(du_bao.index, du_bao[cot[giua]].to_numpy(dtype=float), color=MAU["phu"], linewidth=1.2,
            label=f"quantile {muc_giua:g}")
    if don_vi:
        ax.set_ylabel(don_vi)
    if tieu_de:
        ax.set_title(tieu_de)
    ax.legend(fontsize=7)
    return ax


def pit_histogram(ax, pit, so_bin: int = 10, tieu_de: str | None = None):
    """PIT histogram chuẩn hoá mật độ: phẳng quanh 1 = calibrate. Chữ U = khoảng quá hẹp (quá tự tin);
    vòm = quá rộng; lệch một phía = chệch (Gneiting, Balabdaoui & Raftery 2007).

    pit: mảng giá trị PIT (dữ liệu liên tục), HOẶC cặp (P_duoi, P_tren) từ danh_gia.pit_mau cho dữ liệu
    đếm — khi đó vẽ PIT histogram KHÔNG ngẫu nhiên của Czado, Gneiting & Held (2009):
        F(u | x) = 0 nếu u ≤ P_duoi; (u - P_duoi)/(P_tren - P_duoi) nếu ở giữa; 1 nếu u ≥ P_tren
        chiều cao cột j = F̄(j/J) - F̄((j-1)/J)   (J = so_bin; bài báo gợi ý J = 10 hoặc 20)
    """
    if isinstance(pit, tuple):
        duoi, tren = (np.asarray(v, dtype=float) for v in pit)
    else:
        duoi = tren = np.asarray(pit, dtype=float)
    giu = ~(np.isnan(duoi) | np.isnan(tren))
    duoi, tren = duoi[giu], tren[giu]
    if np.any((duoi < 0) | (tren > 1) | (duoi > tren)):
        raise ValueError("PIT phải trong [0, 1] và P_duoi ≤ P_tren")
    bien = np.linspace(0, 1, so_bin + 1)
    rong = np.where(tren > duoi, tren - duoi, 1.0)
    F = np.where(bien[:, None] >= tren[None, :], 1.0,
                 np.where(bien[:, None] <= duoi[None, :], 0.0, (bien[:, None] - duoi[None, :]) / rong[None, :]))
    if np.array_equal(duoi, tren):  # liên tục: đếm thẳng (điểm rơi đúng biên thuộc cột bên phải)
        chieu_cao = np.histogram(duoi, bins=bien)[0] / len(duoi)
    else:
        chieu_cao = np.diff(F.mean(axis=1))
    ax.bar((bien[:-1] + bien[1:]) / 2, chieu_cao * so_bin, width=1 / so_bin, color=MAU["chinh"], alpha=0.8,
           edgecolor="white")
    ax.axhline(1.0, color=MAU["phu"], linestyle="--", linewidth=1, label="đều (calibrate)")
    ax.set_xlim(0, 1)
    ax.set_xlabel("PIT")
    ax.set_ylabel("mật độ")
    ax.set_title(tieu_de or f"PIT histogram (n = {len(duoi)})")
    ax.legend(fontsize=7)
    return ax


def _pav(y: np.ndarray) -> np.ndarray:
    """Pool-adjacent-violators: hồi quy isotonic (không giảm) của y đã sắp theo x."""
    gia_tri, trong_so, do_dai = [], [], []
    for v in y:
        gia_tri.append(float(v))
        trong_so.append(1.0)
        do_dai.append(1)
        while len(gia_tri) > 1 and gia_tri[-2] > gia_tri[-1]:
            w = trong_so[-2] + trong_so[-1]
            gia_tri[-2] = (gia_tri[-2] * trong_so[-2] + gia_tri[-1] * trong_so[-1]) / w
            trong_so[-2] = w
            do_dai[-2] += do_dai[-1]
            del gia_tri[-1], trong_so[-1], do_dai[-1]
    return np.repeat(gia_tri, do_dai)


def reliability_diagram(ax, p, o, so_bin: int = 10, cach: str = "corp", tieu_de: str | None = None):
    """Reliability diagram cho dự báo xác suất sự kiện nhị phân.

    cach="corp": CORP (Dimitriadis, Gneiting & Jordan 2021) — hồi quy isotonic bằng PAV, không phải chọn
                 bin nên ổn định hơn; cach="bin": chia so_bin bin đều (kiểu cổ điển).
    Đường dưới đường chéo = xác suất dự báo quá cao; trên = quá thấp. Cột xám: số dự báo mỗi bin (độ sắc).
    """
    p, o = np.asarray(p, dtype=float), np.asarray(o, dtype=float)
    if p.shape != o.shape:
        raise ValueError("p và o khác độ dài")
    if cach not in ("corp", "bin"):
        raise ValueError("cach là 'corp' hoặc 'bin'")
    bien = np.linspace(0, 1, so_bin + 1)
    bin_so = np.clip(np.digitize(p, bien[1:-1]), 0, so_bin - 1)
    dem = np.bincount(bin_so, minlength=so_bin)
    ax.plot([0, 1], [0, 1], color=MAU["xam"], linestyle="--", linewidth=1, label="hoàn hảo")
    if cach == "corp":
        thu_tu = np.argsort(p, kind="mergesort")
        ax.step(p[thu_tu], _pav(o[thu_tu]), where="post", color=MAU["chinh"], label="CORP (PAV)")
    else:
        tb_p = [p[bin_so == b].mean() if dem[b] else np.nan for b in range(so_bin)]
        tan_suat = [o[bin_so == b].mean() if dem[b] else np.nan for b in range(so_bin)]
        ax.plot(tb_p, tan_suat, marker="o", color=MAU["chinh"], label="chia bin")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("xác suất dự báo")
    ax.set_ylabel("tần suất xảy ra thật")
    phu = ax.twinx()
    phu.bar((bien[:-1] + bien[1:]) / 2, dem, width=1 / so_bin * 0.9, color=MAU["xam"], alpha=0.2)
    phu.set_ylabel("số dự báo", color=MAU["xam"])
    phu.grid(False)
    ax.set_title(tieu_de or "Reliability diagram")
    ax.legend(fontsize=7, loc="upper left")
    return ax


def small_multiples(df: pd.DataFrame, cac_id: Sequence[str] | None = None, so_cot: int = 3,
                    cot_id: str = "unique_id", cot_ds: str = "ds", cot_y: str = "y", chung_truc_y: bool = False):
    """Nhiều chuỗi, mỗi chuỗi một ô nhỏ. chung_truc_y=False mặc định — ghi rõ điều này khi so biên độ."""
    cac_id = list(cac_id) if cac_id is not None else list(dict.fromkeys(df[cot_id]))[:9]
    so_hang = int(np.ceil(len(cac_id) / so_cot))
    fig, axes = plt.subplots(so_hang, so_cot, figsize=(3.6 * so_cot, 2.2 * so_hang), squeeze=False,
                             sharex=False, sharey=chung_truc_y)
    for ax, uid in zip(axes.ravel(), cac_id, strict=False):
        g = df[df[cot_id] == uid].sort_values(cot_ds)
        ax.plot(g[cot_ds], g[cot_y], linewidth=0.8)
        ax.set_title(str(uid), fontsize=8)
        ax.tick_params(labelsize=6)
    for ax in axes.ravel()[len(cac_id):]:
        ax.set_visible(False)
    fig.tight_layout()
    return fig

