# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 8 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from tv import ve

DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("tq", DAY / "tuong_quan.py")
tq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tq)
M = ve.MAU

# Anscombe (1973), Table 1 — chép tay từ bài báo gốc
ANSCOMBE = {
    "I": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV": ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}


def hinh_anscombe() -> dict:
    fig, truc = plt.subplots(1, 4, figsize=(10.5, 2.9), sharex=True, sharey=True)
    kq = {}
    for ax, (ten, (x, y)) in zip(truc, ANSCOMBE.items(), strict=True):
        x, y = np.array(x, dtype=float), np.array(y, dtype=float)
        b = np.polyfit(x, y, 1)
        ax.scatter(x, y, color=M["chinh"], s=18)
        ax.plot([3, 20], np.polyval(b, [3, 20]), color=M["phu"], linewidth=1)
        ax.set_title(f"{ten}: r = {stats.pearsonr(x, y)[0]:.2f}", fontsize=9)
        kq[ten] = {"r": round(float(stats.pearsonr(x, y)[0]), 3), "spearman": round(float(stats.spearmanr(x, y)[0]), 3),
                   "he_so": [round(float(v), 2) for v in b], "mi": round(tq.thong_tin_tuong_ho(x, y), 3)}
    fig.suptitle("Bộ tứ Anscombe (1973): bốn dữ liệu rất khác nhau, cùng r = 0,82 và cùng đường hồi quy y ≈ 3,00 + 0,50x",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "anscombe.png")
    return kq


def hinh_tuong_quan_gia(kt: pd.DataFrame) -> dict:
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(10.5, 3.2))
    chi_so = kt / kt.iloc[0] * 100
    a.plot(chi_so.index, chi_so["cpi"], color=M["chinh"], label="CPI-U")
    a.plot(chi_so.index, chi_so["dan_so"], color=M["phu"], label="dân số Mỹ")
    a.set_ylabel("chỉ số, 1/1990 = 100")
    a.legend(fontsize=8)
    a.set_title("Hai chuỗi cùng đi lên", fontsize=9)
    b.scatter(kt["dan_so"] / 1000, kt["cpi"], s=6, color=M["chinh"])
    b.set_xlabel("dân số (triệu người)")
    b.set_ylabel("CPI-U")
    b.set_title(f"Mức: r = {kt['cpi'].corr(kt['dan_so']):.3f}".replace(".", ","), fontsize=9)
    d = kt.diff().dropna()
    c.scatter(d["dan_so"], d["cpi"], s=6, color=M["ba"])
    c.axhline(0, color="black", linewidth=0.5)
    c.axvline(0, color="black", linewidth=0.5)
    c.set_xlabel("thay đổi dân số (nghìn người/tháng)")
    c.set_ylabel("thay đổi CPI")
    c.set_title(f"Sai phân: r = {d['cpi'].corr(d['dan_so']):.3f}".replace(".", ","), fontsize=9)
    fig.suptitle("Tương quan giả: r = 0,974 trên mức chỉ nói 'cả hai cùng tăng theo thời gian'",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "tuong-quan-gia.png")
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in tq.tuong_quan_chuoi(kt["cpi"], kt["dan_so"]).items()}


def hinh_chu_u(df: pd.DataFrame) -> dict:
    t, y = df["nhiet"].to_numpy(), df["tai"].to_numpy() / 1000
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.6))
    mau = a.scatter(t, y, c=df.index.month, cmap="twilight", s=3, alpha=0.5)
    plt.colorbar(mau, ax=a, label="tháng", shrink=0.85)
    thang_tuyen = np.polyfit(t, y, 1)
    luoi = np.linspace(t.min(), t.max(), 100)
    a.plot(luoi, np.polyval(thang_tuyen, luoi), color="black", linewidth=1.2, label="hồi quy tuyến tính")
    cdd, hdd = tq.cdd_hdd(luoi)
    X = np.column_stack([np.ones(t.size), *tq.cdd_hdd(t)])
    he_so = np.linalg.lstsq(X, y, rcond=None)[0]
    a.plot(luoi, he_so[0] + he_so[1] * cdd + he_so[2] * hdd, color=M["phu"], linewidth=2, label="CDD + HDD")
    a.axvline(tq.MOC_DO, color=M["xam"], linestyle="--", linewidth=1)
    a.set_xlabel("nhiệt độ trung bình Dallas–Houston (°C)")
    a.set_ylabel("tải điện ERCOT (GW)")
    a.legend(fontsize=8)
    a.set_title("Quan hệ hình chữ U lệch: lạnh thì sưởi, nóng thì điều hoà", fontsize=9)
    moc = np.arange(5, 30.1, 0.5)
    r2 = []
    for m_ in moc:
        X = np.column_stack([np.ones(t.size), *tq.cdd_hdd(t, m_)])
        du = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
        r2.append(1 - du.var() / y.var())
    b.plot(moc, r2, color=M["chinh"])
    b.axvline(tq.MOC_DO, color=M["phu"], linestyle="--", label="18,33 °C (65 °F)")
    b.axvline(moc[int(np.argmax(r2))], color=M["ba"], linestyle=":", label=f"tốt nhất {moc[int(np.argmax(r2))]:.1f} °C")
    b.set_xlabel("mốc chia CDD/HDD (°C)")
    b.set_ylabel("R²")
    b.legend(fontsize=8)
    b.set_title("Mốc 65 °F là quy ước, không phải tối ưu", fontsize=9)
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "chu-u.png")
    X1 = np.column_stack([np.ones(t.size), t])
    r2_t = 1 - (y - X1 @ np.linalg.lstsq(X1, y, rcond=None)[0]).var() / y.var()
    lanh = t <= tq.MOC_DO
    return {"tuong_quan": {k: round(v, 3) for k, v in tq.tuong_quan(t, y).items()},
            "mi": round(tq.thong_tin_tuong_ho(t, y), 3), "r2_tuyen_tinh": round(float(r2_t), 3),
            "r2_cdd_hdd": round(float(1 - np.var(y - np.column_stack([np.ones(y.size), *tq.cdd_hdd(t)]) @ np.linalg.lstsq(np.column_stack([np.ones(y.size), *tq.cdd_hdd(t)]), y, rcond=None)[0]) / y.var()), 4),
            "r2_toi_uu": (float(moc[int(np.argmax(r2))]), round(float(max(r2)), 3)),
            "r_lanh": round(float(np.corrcoef(t[lanh], y[lanh])[0, 1]), 3), "n_lanh": int(lanh.sum()),
            "r_nong": round(float(np.corrcoef(t[~lanh], y[~lanh])[0, 1]), 3), "n_nong": int((~lanh).sum())}


def hinh_ccf(df: pd.DataFrame) -> dict:
    x, y = df["cdd"].to_numpy(), df["tai"].to_numpy()
    tho = tq.do_tre_dan_dat(x, y, so_tre=48, bac=None)
    sach = tq.do_tre_dan_dat(x, y, so_tre=48)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.2), sharey=True)
    for ax, kq, ten in ((a, tho, "CCF thô"), (b, sach, "sau prewhitening AR(48) của CDD")):
        ax.vlines(range(len(kq["ccf"])), 0, kq["ccf"], color=M["chinh"])
        ax.axhspan(-kq["dai"], kq["dai"], color=M["xam"], alpha=0.35)
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_xlabel("độ trễ k (giờ): CDD đi trước tải k giờ")
        ax.set_title(f"{ten} — đỉnh ở trễ {kq['tre']} (r = {kq['r_dinh']:.2f})".replace(".", ","), fontsize=9)
    a.set_ylabel("tương quan chéo")
    fig.suptitle("CCF thô rộng và còn nhịp 24 giờ của chính CDD; prewhitening để lộ quan hệ thật: tức thì, tắt sau vài giờ",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ccf.png")
    return {"tho": {"tre": tho["tre"], "r0": round(float(tho["ccf"][0]), 3), "r1": round(float(tho["ccf"][1]), 3),
                    "r24": round(float(tho["ccf"][24]), 3), "r48": round(float(tho["ccf"][48]), 3)},
            "sach": {"tre": sach["tre"], "r0": round(float(sach["ccf"][0]), 3), "r1": round(float(sach["ccf"][1]), 3),
                     "r3": round(float(sach["ccf"][3]), 3), "r24": round(float(sach["ccf"][24]), 3),
                     "dai": round(float(sach["dai"]), 4)}}


def hinh_truot(df: pd.DataFrame) -> dict:
    ngay = df.resample("D").mean()
    r90 = tq.tuong_quan_truot(ngay["nhiet"], ngay["tai"], 90)
    r30 = tq.tuong_quan_truot(ngay["nhiet"], ngay["tai"], 30)
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.plot(r30.index, r30.to_numpy(), color=M["xam"], linewidth=0.9, label="cửa sổ 30 ngày")
    ax.plot(r90.index, r90.to_numpy(), color=M["chinh"], linewidth=1.8, label="cửa sổ 90 ngày")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axhline(float(df["nhiet"].corr(df["tai"])), color=M["phu"], linestyle="--",
               label=f"tương quan cả năm {df['nhiet'].corr(df['tai']):.2f}".replace(".", ","))
    ax.set_ylabel("tương quan nhiệt độ × tải (theo ngày)")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Quan hệ đổi dấu theo mùa: âm mạnh cuối mùa đông, dương gần 1 vào mùa hè — một con số cả năm che mất điều đó")
    ve.luu_hinh(fig, HINH / "truot.png")
    return {"r90_min": (str(r90.idxmin().date()), round(float(r90.min()), 3)),
            "r90_max": (str(r90.idxmax().date()), round(float(r90.max()), 3)),
            "r30_min": (str(r30.idxmin().date()), round(float(r30.min()), 3)),
            "ca_nam": round(float(df["nhiet"].corr(df["tai"])), 3), "ngay": round(float(ngay["nhiet"].corr(ngay["tai"])), 3)}


def hinh_granger(df: pd.DataFrame) -> dict:
    gio = df.index.hour
    ho_so = pd.DataFrame({"tai": df["tai"].groupby(gio).mean(), "nhiet": df["nhiet"].groupby(gio).mean()})
    chuan = (ho_so - ho_so.mean()) / ho_so.std()
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.2))
    a.plot(chuan.index, chuan["tai"], color=M["chinh"], marker="o", markersize=3, label="tải điện")
    a.plot(chuan.index, chuan["nhiet"], color=M["phu"], marker="s", markersize=3, label="nhiệt độ")
    a.set_xlabel("giờ UTC")
    a.set_ylabel("giá trị chuẩn hoá")
    a.legend(fontsize=8)
    a.set_title("Cùng một nhịp 24 giờ → quá khứ bên này 'dự báo' được bên kia", fontsize=9)
    kq = tq.granger_hai_chieu(pd.Series(df["cdd"].to_numpy(), index=df.index), df["tai"], so_tre=4)
    tre = np.arange(1, 13)
    r_xy = tq.ccf_tu_viet(df["cdd"].to_numpy(), df["tai"].to_numpy(), 12)[1:]
    r_yx = tq.ccf_tu_viet(df["tai"].to_numpy(), df["cdd"].to_numpy(), 12)[1:]
    b.plot(tre, r_xy, color=M["chinh"], marker="o", markersize=3, label="CDD(t) × tải(t+k)")
    b.plot(tre, r_yx, color=M["phu"], marker="s", markersize=3, label="tải(t) × CDD(t+k)")
    b.set_xlabel("k (giờ)")
    b.legend(fontsize=8)
    b.set_title("Tương quan chéo cao ở CẢ HAI chiều", fontsize=9)
    fig.suptitle("Granger hai chiều cùng có ý nghĩa (p < 0,001): 'tải điện gây ra nhiệt độ' là kết luận vô lý",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "granger.png")
    return {"granger": {k: (round(v, 6) if isinstance(v, float) else v) for k, v in kq.items()},
            "r_xy_1": round(float(r_xy[0]), 3), "r_yx_1": round(float(r_yx[0]), 3)}


def hinh_mi_khoi(seed: int = 0) -> dict:
    """Phân phối rỗng của MI: hoán vị từng điểm so với hoán vị theo khối, trên hai chuỗi AR(0,99) ĐỘC LẬP."""
    rng = np.random.default_rng(seed)

    def ar(n=2000, phi=0.99):
        v = np.empty(n)
        v[0] = rng.normal()
        for i in range(1, n):
            v[i] = phi * v[i - 1] + rng.normal()
        return v

    x, y = ar(), ar()
    that = tq.thong_tin_tuong_ho(x, y)
    fig, ax = plt.subplots(figsize=(9, 3.3))
    kq = {}
    for do_dai, mau, ten in ((1, M["phu"], "hoán vị từng điểm"), (200, M["chinh"], "hoán vị theo khối 200")):
        gia = []
        r2 = np.random.default_rng(seed)
        for _ in range(200):
            khoi = [y[i:i + do_dai] for i in range(0, y.size, do_dai)]
            tron = np.concatenate([khoi[i] for i in r2.permutation(len(khoi))])[: x.size]
            gia.append(tq.thong_tin_tuong_ho(x, tron))
        gia = np.array(gia)
        ax.hist(gia, bins=30, alpha=0.55, color=mau, label=f"{ten}: ngưỡng 95% = {np.quantile(gia, 0.95):.3f}".replace(".", ","))
        kq[ten] = {"nguong_95": round(float(np.quantile(gia, 0.95)), 4),
                   "p": round(float((np.sum(gia >= that) + 1) / 201), 4)}
    ax.axvline(that, color="black", linewidth=1.5, label=f"MI quan sát được = {that:.3f}".replace(".", ","))
    ax.set_xlabel("mutual information (nat)")
    ax.legend(fontsize=8)
    ax.set_title("Hai chuỗi AR(0,99) ĐỘC LẬP: hoán vị từng điểm kết luận 'có quan hệ', hoán vị theo khối thì không")
    ve.luu_hinh(fig, HINH / "mi-khoi.png")
    kq["mi_quan_sat"] = round(float(that), 4)
    return kq


if __name__ == "__main__":
    kt = tq.doc_kinh_te()
    df = tq.ghep_tai_nhiet()
    with ve.phong_cach():
        print("anscombe", hinh_anscombe())
        print("gia", hinh_tuong_quan_gia(kt))
        print("chu u", hinh_chu_u(df))
        print("ccf", hinh_ccf(df))
        print("truot", hinh_truot(df))
        print("granger", hinh_granger(df))
        print("mi khoi", hinh_mi_khoi())
    print("MI khối:", {k: round(v, 4) for k, v in
                       tq.kiem_y_nghia_mi(df["nhiet"].to_numpy(), df["tai"].to_numpy(), 168, 100).items()})
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
