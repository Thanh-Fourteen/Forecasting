# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 7 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

from tv import ve

DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("tt", DAY / "tu_tuong_quan.py")
tt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tt)
M = ve.MAU


def ve_acf(ax, y, so_tre: int, dai: float, ten: str, pacf_thay=False, don_vi: str = "bước") -> None:
    r = pacf(y, nlags=so_tre, method="ywm") if pacf_thay else tt.acf_tu_viet(y, so_tre)
    ax.vlines(range(len(r)), 0, r, color=M["chinh"])
    ax.axhspan(-dai, dai, color=M["xam"], alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlabel(f"độ trễ k ({don_vi})", fontsize=8)
    ax.set_ylabel("PACF" if pacf_thay else "r_k", fontsize=8)
    ax.set_title(ten, fontsize=8)


def hinh_bon_chuoi() -> dict:
    chuoi = tt.sinh_bon_chuoi()
    dai = tt.dai_nhieu_trang(500)
    fig, truc = plt.subplots(4, 3, figsize=(10, 9))
    for hang, (ten, y) in enumerate(chuoi.items()):
        truc[hang, 0].plot(y, color=M["chinh"], linewidth=0.7)
        truc[hang, 0].set_title(ten, fontsize=9, loc="left")
        truc[hang, 0].set_xlabel("t", fontsize=8)
        ve_acf(truc[hang, 1], y, 30, dai, "ACF")
        ve_acf(truc[hang, 2], y, 30, dai, "PACF (ywm)", pacf_thay=True)
    fig.suptitle("Bốn chuỗi, cùng một dãy nhiễu (seed 42, n = 500): ACF phân biệt dừng với không dừng, PACF chỉ ra bậc AR",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "bon-chuoi.png")
    kq = {}
    for ten, y in chuoi.items():
        r = tt.acf_tu_viet(y, 30)
        p = pacf(y, nlags=5, method="ywm")
        kq[ten] = {"r1": round(float(r[1]), 3), "r5": round(float(r[5]), 3), "r30": round(float(r[30]), 3),
                   "pacf1": round(float(p[1]), 3), "pacf2": round(float(p[2]), 3),
                   "so_cot_ngoai_dai_30": int(np.sum(np.abs(r[1:]) > dai))}
    return kq


def hinh_nhieu_trang(so_lan: int = 1000, so_tre: int = 20, n: int = 500, seed: int = 2026) -> dict:
    rng = np.random.default_rng(seed)
    dai = tt.dai_nhieu_trang(n)
    dem = np.array([np.sum(np.abs(tt.acf_tu_viet(rng.normal(size=n), so_tre)[1:]) > dai) for _ in range(so_lan)])
    y = tt.sinh_bon_chuoi()["nhiễu trắng"]
    bartlett = acf(y, nlags=so_tre, alpha=0.05, bartlett_confint=True, result_object=True)
    r_sm, ci = bartlett.acf, bartlett.confint
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.4))
    a.vlines(range(so_tre + 1), 0, r_sm, color=M["chinh"])
    a.plot(range(so_tre + 1), ci[:, 1] - r_sm, color=M["ba"], linestyle="--", linewidth=1, label="dải Bartlett (statsmodels)")
    a.plot(range(so_tre + 1), ci[:, 0] - r_sm, color=M["ba"], linestyle="--", linewidth=1)
    a.axhspan(-dai, dai, color=M["xam"], alpha=0.3, label="±1,96/√T (FPP)")
    a.axhline(0, color="black", linewidth=0.5)
    a.set_ylim(-0.25, 0.25)
    a.set_xlabel("độ trễ")
    a.legend(fontsize=7)
    a.set_title("Nhiễu trắng n = 500: hai dải khác nhau", fontsize=9)
    b.hist(dem, bins=np.arange(-0.5, 8.5), color=M["chinh"], alpha=0.8)
    b.set_xlabel(f"số cột vượt dải trong {so_tre} trễ")
    b.set_ylabel(f"số lần trong {so_lan} chuỗi nhiễu trắng")
    b.set_title(f"Trung bình {dem.mean():.2f} cột vượt; {np.mean(dem >= 1):.0%} số chuỗi có ít nhất 1".replace(".", ","), fontsize=9)
    fig.suptitle("Một cột ACF vượt dải KHÔNG phải bằng chứng — với 20 trễ, nhiễu trắng cũng thường có vài cột vượt",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "nhieu-trang.png")
    q = [round(float(tt.ljung_box(tt.sinh_bon_chuoi(seed=s)["nhiễu trắng"], 10)[1]), 3) for s in (1, 2, 3)]
    return {"tb_cot_vuot": round(float(dem.mean()), 3), "ty_le_it_nhat_1": round(float(np.mean(dem >= 1)), 3),
            "toi_da": int(dem.max()), "ljung_box_p_3_seed": q,
            "bartlett_tre20": round(float(ci[20, 1] - r_sm[20]), 4), "dai_fpp": round(dai, 4)}


def hinh_sai_phan_thua() -> dict:
    chuoi = tt.sinh_bon_chuoi()
    dai = tt.dai_nhieu_trang(499)
    fig, truc = plt.subplots(2, 2, figsize=(10, 5.5))
    kq = {}
    for cot, ten in enumerate(["nhiễu trắng", "random walk"]):
        y = pd.Series(chuoi[ten])
        sp = y.diff().dropna()
        truc[0, cot].plot(sp.to_numpy(), color=M["phu"], linewidth=0.7)
        truc[0, cot].set_title(f"{ten} sau khi sai phân — sd {sp.std(ddof=1):.2f} (trước {y.std(ddof=1):.2f})".replace(".", ","), fontsize=9)
        truc[0, cot].set_xlabel("t", fontsize=8)
        ve_acf(truc[1, cot], sp, 20, dai, "ACF sau sai phân")
        kq[ten] = tt.dau_hieu_sai_phan_thua(y)
        kq[ten] = {k: round(v, 3) for k, v in kq[ten].items()}
    fig.suptitle("Sai phân chuỗi đã dừng: ACF(1) rơi xuống ≈ −0,5 và độ lệch chuẩn TĂNG — dấu hiệu sai phân thừa",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "sai-phan-thua.png")
    return kq


def hinh_that() -> dict:
    gdp = tt.doc_gdp()
    ip = tt.doc_san_luong()
    log_gdp = np.log(gdp)
    tang = log_gdp.diff().dropna() * 100
    fig, truc = plt.subplots(2, 2, figsize=(10, 5.5))
    truc[0, 0].plot(log_gdp.index, log_gdp.to_numpy(), color=M["chinh"])
    truc[0, 0].set_title("log GDP thực Mỹ theo quý (1947–2026): xu hướng rõ", fontsize=9)
    truc[0, 0].set_ylabel("log GDP", fontsize=8)
    truc[0, 1].plot(tang.index, tang.to_numpy(), color=M["phu"], linewidth=0.8)
    truc[0, 1].axhline(0, color="black", linewidth=0.5)
    truc[0, 1].set_title("sai phân log (×100): dao động quanh 0,76%/quý, vài cú sốc lớn", fontsize=9)
    truc[0, 1].set_ylabel("% mỗi quý", fontsize=8)
    ve_acf(truc[1, 0], log_gdp.to_numpy(), 24, tt.dai_nhieu_trang(len(gdp)), "ACF log GDP: giảm rất chậm", don_vi="quý")
    ve_acf(truc[1, 1], tang.to_numpy(), 24, tt.dai_nhieu_trang(len(tang)), "ACF sai phân log: vài trễ đầu còn tương quan", don_vi="quý")
    fig.suptitle("Chuỗi kinh tế thật: ACF giảm chậm = chưa dừng; sai phân log biến mức thành tốc độ tăng",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "gdp.png")
    kq = {"gdp_n": len(gdp), "gdp_dau": str(gdp.index[0].date()), "gdp_cuoi": str(gdp.index[-1].date()),
          "tang_tb_quy": round(float(tang.mean()), 3), "tang_min": (str(tang.idxmin().date()), round(float(tang.min()), 2)),
          "tang_max": (str(tang.idxmax().date()), round(float(tang.max()), 2)),
          "acf_log_gdp": [round(float(v), 3) for v in tt.acf_tu_viet(log_gdp.to_numpy(), 8)[[1, 4, 8]]],
          "acf_tang": [round(float(v), 3) for v in tt.acf_tu_viet(tang.to_numpy(), 8)[[1, 2, 4]]],
          "kd_log_gdp": {k: round(v, 4) if isinstance(v, float) else v for k, v in tt.kiem_dinh(log_gdp, co_xu_huong=True).items()},
          "kd_tang": {k: round(v, 4) if isinstance(v, float) else v for k, v in tt.kiem_dinh(tang).items()},
          "d_log_gdp": tt.so_lan_sai_phan(log_gdp), "ket_luan_tang": tt.ket_luan(tang),
          "ljung_tang": [round(v, 4) for v in tt.ljung_box(tang, 8)]}
    ip_log = np.log(ip)
    kq["ip"] = {"n": len(ip), "d": tt.so_lan_sai_phan(ip_log), "ket_luan_c": tt.ket_luan(ip_log),
                "ket_luan_ct": tt.ket_luan(ip_log, True),
                "kd_c": {k: round(v, 4) if isinstance(v, float) else v for k, v in tt.kiem_dinh(ip_log).items()},
                "kd_ct": {k: round(v, 4) if isinstance(v, float) else v for k, v in tt.kiem_dinh(ip_log, True).items()},
                "kd_sai_phan": {k: round(v, 4) if isinstance(v, float) else v for k, v in tt.kiem_dinh(ip_log.diff().dropna()).items()}}
    return kq


def bang_sai_phan_gio(y: pd.Series) -> dict:
    """log(1 + lượt thuê theo giờ): sai phân thường, mùa vụ 168, và 168 rồi thường — ACF và độ lệch chuẩn."""
    g = np.log1p(y.interpolate(limit=3))
    kq = {}
    for ten, s in (("log", g), ("sai phân 1", g.diff()), ("sai phân 168", g.diff(168)), ("168 rồi 1", g.diff(168).diff())):
        r = tt.acf_tu_viet(s.to_numpy(), 168)
        kq[ten] = {"acf1": round(float(r[1]), 3), "acf24": round(float(r[24]), 3), "acf168": round(float(r[168]), 3),
                   "sd": round(float(s.std(ddof=1)), 3)}
    return kq


def hinh_luot_thue() -> dict:
    y = tt.doc_luot_thue()
    ngay = y.resample("D").sum(min_count=12).interpolate()   # lưới ngày LIÊN TỤC: 3 ngày < 12 giờ nội suy
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.4))
    ve_acf(a, y, 200, tt.dai_nhieu_trang(int(y.notna().sum())), "ACF lượt thuê theo giờ (trễ tới 200)", don_vi="giờ")
    ve_acf(b, ngay, 40, tt.dai_nhieu_trang(len(ngay)), "ACF tổng theo ngày (trễ tới 40)", don_vi="ngày")
    fig.suptitle("Cùng dữ liệu, hai tần suất: theo giờ thấy mùa vụ 24 và 168; theo ngày ACF giảm chậm, mùa vụ 7 gần như bị che",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "luot-thue.png")
    r_gio = tt.acf_tu_viet(y, 200)
    r_ngay = tt.acf_tu_viet(ngay, 40)
    return {"gio": {k: round(float(r_gio[k]), 3) for k in (1, 12, 24, 168)},
            "ngay": {k: round(float(r_ngay[k]), 3) for k in (1, 5, 6, 7, 8, 14, 28)},
            "kd_ngay": {k: round(v, 4) if isinstance(v, float) else v for k, v in tt.kiem_dinh(ngay).items()},
            "d_ngay": tt.so_lan_sai_phan(ngay), "sai_phan_gio": bang_sai_phan_gio(y)}


if __name__ == "__main__":
    with ve.phong_cach():
        print("bon chuoi", hinh_bon_chuoi())
        print("nhieu trang", hinh_nhieu_trang())
        print("sai phan thua", hinh_sai_phan_thua())
        print("that", hinh_that())
        print("luot thue", hinh_luot_thue())
    print(tt.bang_bon_chuoi().to_string(index=False))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
