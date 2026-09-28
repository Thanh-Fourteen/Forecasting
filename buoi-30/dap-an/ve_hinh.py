# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 30 → ../hinh/*.png (150 dpi) và in mọi con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (khoảng 8 phút, CPU 4 luồng; seed 0)
# Dự báo từng mô hình lưu ở lab/du-lieu/cache/ve-hinh/ — xoá thư mục đó để chạy lại từ đầu.

# %%
from __future__ import annotations

import importlib.util
import sys
import time
import warnings
from functools import reduce
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tv import THU_MUC_LAB, ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
CACHE = THU_MUC_LAB / "du-lieu" / "cache" / "ve-hinh"
CACHE.mkdir(parents=True, exist_ok=True)
M = ve.MAU
ve.phong_cach()

spec = importlib.util.spec_from_file_location("kt", DAY / "kien_truc.py")
kt = importlib.util.module_from_spec(spec)
sys.modules["kt"] = kt
spec.loader.exec_module(kt)
KHOA = ["unique_id", "ds", "moc"]
t00 = time.time()


def nho(ten: str, ham):
    """Chạy ham() một lần, lưu kết quả (DataFrame) vào cache."""
    tep = CACHE / f"{ten}.parquet"
    if tep.exists():
        return pd.read_parquet(tep)
    ra = ham()
    ra.to_parquet(tep)
    return ra


d = kt.doc_du_lieu()
moc = kt.cac_moc_test()
print(f"{d['unique_id'].nunique()} vùng × {d.groupby('unique_id').size().iloc[0]:,} giờ ({d['ds'].min()} → {d['ds'].max()}); "
      f"{d.attrs['so_lo_i']} giờ nhu cầu lỗi đã lấp; {len(moc)} mốc test {moc[0].date()} → {moc[-1].date()}")

# %% ---------------------------------------------------------------- 1. bảng chính
thoi_gian, mo_hinh = {}, {}
bang = [nho("SeasonalNaive", lambda: kt.seasonal_naive(d, moc)), nho("EIA", lambda: kt.eia(d, moc))]
for ten, ham in [("MSTL", lambda: kt.mstl(d, moc)), ("LightGBM", lambda: kt.lightgbm(d, moc))]:
    t = time.time()
    bang.append(nho(ten, ham))
    thoi_gian[ten] = time.time() - t
for ten in kt.KIEN_TRUC:
    nf, g = kt.huan_luyen(d, ten)
    mo_hinh[ten], thoi_gian[ten] = nf, g
    f = kt.du_bao_cac_moc(nf, d, moc)
    if ten == "DeepAR":
        f[KHOA + [c for c in f.columns if c.startswith("DeepAR-")]].to_parquet(CACHE / "DeepAR-khoang.parquet")
        f = f.drop(columns=["DeepAR"]).rename(columns={"DeepAR-median": "DeepAR"})
    f[KHOA + [ten]].to_parquet(CACHE / f"{ten}.parquet")
    bang.append(f[KHOA + [ten]])
    print(f"  {ten:8s} huấn luyện {g:6.1f} s, {sum(p.numel() for p in nf.models[0].parameters()):,} tham số")
x = reduce(lambda a, b: a.merge(b, on=KHOA), bang)
cot = [c for c in x.columns if c not in KHOA]
bm = kt.bang_mase(x, d, cot)
bm["giây"] = [round(thoi_gian.get(c, 0.0)) for c in bm.index]
print("\n== Bảng chính (MASE, mẫu số seasonal naive tuần trên train)\n" + bm.to_string())

# %% ---------------------------------------------------------------- 2. cái giá của rò rỉ futr_exog (NHITS)
nf_r, _ = kt.huan_luyen(d, "NHITS", futr=["nhiet_do_thuc", "gio", "thu"], hist=[])
nf_k, _ = kt.huan_luyen(d, "NHITS", futr=["gio", "thu"], hist=[])
rr = [kt.du_bao_cac_moc(nf_r, d, moc).rename(columns={"NHITS": "rò rỉ: backtest"}),
      kt.du_bao_cac_moc(nf_r, d, moc, thay_futr={"nhiet_do_thuc": "nhiet_do_du_bao"}).rename(columns={"NHITS": "rò rỉ: vận hành"}),
      x[KHOA + ["NHITS"]].rename(columns={"NHITS": "đúng"}),
      kt.du_bao_cac_moc(nf_k, d, moc).rename(columns={"NHITS": "không nhiệt độ"})]
r = reduce(lambda a, b: a.merge(b, on=KHOA), rr)
print("\n== Rò rỉ futr_exog, NHITS\n" + kt.bang_mase(r, d, ["rò rỉ: backtest", "rò rỉ: vận hành", "đúng", "không nhiệt độ"]).to_string())
sai_nhiet = d[d["ds"] >= kt.MOC_TEST].assign(e=lambda z: (z["nhiet_do_du_bao"] - z["nhiet_do_thuc"]).abs())
print("  MAE nhiệt độ dự báo trước 1 ngày so với nhiệt độ thực (°C):", sai_nhiet.groupby("unique_id")["e"].mean().round(2).to_dict())

vung = "PJM"
e_ngay = sai_nhiet[sai_nhiet["unique_id"] == vung].groupby(sai_nhiet["ds"].dt.floor("D"))["e"].mean()
ngay = max(moc, key=lambda m: e_ngay.get(m.normalize(), 0))       # mốc có nhiệt độ dự báo lệch nhiều nhất
z = r[(r["unique_id"] == vung) & (r["moc"] == ngay)].merge(d[["unique_id", "ds", "y", "nhiet_do_thuc", "nhiet_do_du_bao"]],
                                                          on=["unique_id", "ds"])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
gio = (z["ds"] - ngay) / pd.Timedelta(hours=1)
a1.plot(gio, z["nhiet_do_thuc"], color="k", lw=2, label="thực (chỉ biết sau)")
a1.plot(gio, z["nhiet_do_du_bao"], color=M["chinh"], label="đã dự báo trước 1 ngày")
a1.set_xlabel(f"giờ sau mốc {ngay.date()} 00:00 UTC")
a1.set_ylabel("°C")
a1.legend(fontsize=8)
a1.set_title(f"{vung}: nhiệt độ dự báo lệch thực tế")
a2.plot(gio, z["y"] / 1000, color="k", lw=2, label="nhu cầu thực")
a2.plot(gio, z["rò rỉ: backtest"] / 1000, color=M["phu"], ls="--", label="rò rỉ, lúc backtest")
a2.plot(gio, z["rò rỉ: vận hành"] / 1000, color=M["phu"], label="cùng mô hình, lúc vận hành")
a2.plot(gio, z["đúng"] / 1000, color=M["chinh"], label="khai đúng loại")
a2.set_xlabel(f"giờ sau mốc {ngay.date()} 00:00 UTC")
a2.set_ylabel("GW")
a2.legend(fontsize=8)
a2.set_title("Backtest rò rỉ đẹp hơn thứ mô hình làm được thật")
fig.tight_layout()
ve.luu_hinh(fig, HINH / "ro-ri-futr.png")
print(f"  hình rò rỉ: {vung}, mốc {ngay.date()}, MAE nhiệt độ ngày đó {e_ngay.get(ngay.normalize()):.1f} °C")

# %% ---------------------------------------------------------------- 3. N-BEATS diễn giải được: xu hướng + mùa vụ
from neuralforecast.tsdataset import TimeSeriesDataset  # noqa: E402

nb = mo_hinh["NBEATS"].models[0]
mnb = moc[20]
lich, _ = kt.du_lieu_moc(d, mnb, [])
tsd, *_ = TimeSeriesDataset.from_df(lich[["unique_id", "ds", "y"]])
thanh_phan = nb.decompose(dataset=tsd)                      # (vùng, [mức, xu hướng, mùa vụ], 24) — mỗi khối đã cộng vị trí scaler
dbnb = mo_hinh["NBEATS"].predict(df=lich[["unique_id", "ds", "y"]])
i = sorted(kt.VUNG).index("ERCO")
tong = dbnb[dbnb["unique_id"] == "ERCO"]["NBEATS"].to_numpy()
vi_tri = (thanh_phan[i].sum(axis=0) - tong) / 2               # tổng 3 khối = dự báo + 2 × vị trí
muc, xu_huong, mua_vu = thanh_phan[i, 0], thanh_phan[i, 1] - vi_tri, thanh_phan[i, 2] - vi_tri
that = d[(d["unique_id"] == "ERCO") & (d["ds"] > mnb) & (d["ds"] <= mnb + pd.Timedelta(hours=24))]["y"].to_numpy()
print(f"\n== N-BEATS, ERCO, mốc {mnb.date()}: mức {muc[0]:,.0f} MW; xu hướng {xu_huong.min():,.0f} … {xu_huong.max():,.0f}; "
      f"mùa vụ {mua_vu.min():,.0f} … {mua_vu.max():,.0f}; kiểm tổng lệch {np.abs(muc + xu_huong + mua_vu - tong).max():.3f}")
fig, ax = plt.subplots(figsize=(8, 3.8))
h = np.arange(1, 25)
ax.plot(h, that / 1000, color="k", lw=2, label="thực tế")
ax.plot(h, tong / 1000, color=M["chinh"], lw=2, label="dự báo = mức + xu hướng + mùa vụ")
ax.plot(h, (muc + xu_huong) / 1000, color=M["phu"], ls="--", label="mức + xu hướng")
ax.fill_between(h, (muc + xu_huong) / 1000, tong / 1000, color=M["ba"], alpha=0.2, label="phần mùa vụ (ngày)")
ax.set_xlabel(f"giờ sau mốc {mnb.date()} 00:00 UTC")
ax.set_ylabel("GW")
ax.legend(fontsize=8)
ax.set_title("ERCO: mức + xu hướng cho đường nền trơn, khối mùa vụ mang nhịp ngày")
fig.tight_layout()
ve.luu_hinh(fig, HINH / "nbeats-thanh-phan.png")

# %% ---------------------------------------------------------------- 4. TFT: biến nào được chọn
fi = mo_hinh["TFT"].models[0].feature_importances()
qua_khu = fi["Past variable importance over time"].mean()
tuong_lai = fi["Future variable importance over time"].mean()
tinh = fi["Static covariates"]["importance"]
print("\n== TFT (lần dự báo cuối, trung bình theo thời gian)\n  quá khứ:", qua_khu.round(3).to_dict(),
      "\n  tương lai:", tuong_lai.round(3).to_dict(), "\n  tĩnh:", tinh.round(3).to_dict())
ten_bien = {"observed_target": "nhu cầu quá khứ", "nhiet_do_thuc": "nhiệt độ thực", "nhiet_do_du_bao": "nhiệt độ dự báo",
            "gio": "giờ", "thu": "thứ"}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
qk = qua_khu.sort_values()
a1.barh([ten_bien.get(k, k) for k in qk.index], qk.to_numpy(), color=M["chinh"])
a1.set_xlabel("trọng số chọn biến, trung bình (tổng = 1)")
a1.set_title("168 giờ quá khứ")
tl = tuong_lai.sort_values()
a2.barh([ten_bien.get(k, k) for k in tl.index], tl.to_numpy(), color=M["phu"])
a2.set_xlabel("trọng số chọn biến, trung bình (tổng = 1)")
a2.set_title("24 giờ tương lai")
fig.suptitle("TFT: quá khứ dựa nhiều nhất vào nhu cầu cũ; tương lai dựa nhiều nhất vào giờ trong ngày", fontsize=11)
fig.tight_layout()
ve.luu_hinh(fig, HINH / "tft-chon-bien.png")

# %% ---------------------------------------------------------------- 5. DeepAR: khoảng dự báo có đúng 80%, 90% không, theo tầm
kh = pd.read_parquet(CACHE / "DeepAR-khoang.parquet").merge(d[["unique_id", "ds", "y"]], on=["unique_id", "ds"])
kh["h"] = ((kh["ds"] - kh["moc"]) / pd.Timedelta(hours=1)).astype(int)
for muc in (80, 90):
    kh[f"trong_{muc}"] = (kh["y"] >= kh[f"DeepAR-lo-{muc}"]) & (kh["y"] <= kh[f"DeepAR-hi-{muc}"])
    print(f"\n== DeepAR khoảng {muc}%: phủ chung {kh[f'trong_{muc}'].mean():.3f}; giờ 1–6 {kh[kh['h'] <= 6][f'trong_{muc}'].mean():.3f}; "
          f"giờ 19–24 {kh[kh['h'] >= 19][f'trong_{muc}'].mean():.3f}; theo vùng "
          + str(kh.groupby("unique_id")[f"trong_{muc}"].mean().round(3).to_dict()))
do_rong = (kh["DeepAR-hi-80"] - kh["DeepAR-lo-80"]).groupby(kh["h"]).mean()
print(f"  độ rộng khoảng 80% trung bình: giờ 1 {do_rong.iloc[0]:,.0f} MW, giờ 24 {do_rong.iloc[-1]:,.0f} MW")
fig, ax = plt.subplots(figsize=(8, 3.6))
for muc, mau in [(80, M["chinh"]), (90, M["phu"])]:
    cv = kh.groupby("h")[f"trong_{muc}"].mean()
    ax.plot(cv.index, cv.to_numpy(), marker="o", ms=3, color=mau, label=f"khoảng {muc}%")
    ax.axhline(muc / 100, color=mau, ls="--", lw=1)
ax.set_xlabel("tầm dự báo (giờ sau mốc)")
ax.set_ylabel("tỷ lệ giờ thực tế nằm trong khoảng")
ax.set_ylim(0, 1)
ax.legend(fontsize=8, title="nét đứt: mức danh nghĩa")
ax.set_title("DeepAR: khoảng dự báo phủ thiếu, và thiếu hơn ở tầm xa")
fig.tight_layout()
ve.luu_hinh(fig, HINH / "deepar-coverage.png")
print(f"\nXong trong {(time.time() - t00) / 60:.1f} phút")
