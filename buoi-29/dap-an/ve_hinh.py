# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 29 → ../hinh/*.png (150 dpi) và in mọi con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (khoảng 15 phút, CPU 4 luồng; seed 0)

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
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
M = ve.MAU
ve.phong_cach()


def nap(tep: Path, ten: str):
    spec = importlib.util.spec_from_file_location(ten, tep)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[ten] = mod
    spec.loader.exec_module(mod)
    return mod


hs = nap(DAY / "hoc_sau.py", "hs")                       # bản đã sửa
hc = nap(DAY.parent / "code" / "hoc_sau.py", "hc")       # bản phát cho học viên (còn chỗ hở)

# %% ---------------------------------------------------------------- 1. hình cửa sổ (ví dụ tay 10 điểm, mục 4.1)
fig, truc = plt.subplots(1, 2, figsize=(11, 3.6), sharey=True)
for ax, (tieu_de, cach) in zip(truc, [("Chia theo thời gian rồi mới cắt", "dung"),
                                       ("Cắt rồi rút ngẫu nhiên mẫu val", "sai")], strict=True):
    _, _, dau = hs.cat_cua_so(np.arange(10.0), L=3, H=2)
    for k, d in enumerate(dau):
        vao, muc = range(d - 3, d), range(d, d + 2)
        if cach == "dung":
            loai = "train" if d + 1 <= 6 else ("val" if d >= 7 else "bỏ")
        else:
            loai = "val" if d == 4 else "train"
        mau = {"train": M["chinh"], "val": M["phu"], "bỏ": "#BBBBBB"}[loai]
        y = len(dau) - k
        ax.scatter(list(vao), [y] * 3, s=90, facecolors="white", edgecolors=mau, linewidths=1.8)
        ax.scatter(list(muc), [y] * 2, s=90, color=mau)
        ax.text(9.7, y, loai, va="center", fontsize=9, color=mau)
    if cach == "dung":
        ax.axvline(6.5, color="k", ls="--", lw=1)
        ax.text(6.6, 6.55, "mốc val", fontsize=9)
    else:
        for x in (4, 5):
            ax.axvspan(x - 0.35, x + 0.35, color=M["phu"], alpha=0.12)
    ax.set_xticks(range(10))
    ax.set_xlabel("vị trí trong chuỗi (giờ 0 … 9)")
    ax.set_yticks([])
    ax.set_xlim(-0.5, 10.6)
    ax.set_ylim(0.5, 6.9)
    ax.set_title(tieu_de)
fig.suptitle("Cắt trước rồi chia ngẫu nhiên: giờ 4 và 5 mà val phải đoán đã là mục tiêu của mẫu train", fontsize=11)
fig.tight_layout()
ve.luu_hinh(fig, HINH / "cua-so.png")

# %% ---------------------------------------------------------------- 2. rò rỉ chồng lấn: tập nhỏ vs tập 50 khách
t0 = time.time()
df = hs.doc_dien()
moc = hs.cac_moc_test(df)
print(f"50 khách, đổi mức: {len(df.attrs['doi_muc'])} {df.attrs['doi_muc']}")
print(f"giờ: {df['ds'].min()} → {df['ds'].max()}; mốc test {moc[0].date()} → {moc[-1].date()} ({len(moc)} mốc)")

print("\n== Rò rỉ chồng lấn (MLP 1.024 nút + RevIN, tối đa 200 epoch × 50 bước, kiên nhẫn 15)")
nho = hs.chon_it(df)
for ten, mod in [("chia đúng", hs), ("cắt rồi chia ngẫu nhiên", hc)]:
    sc = hs.hoc_scaler(nho)
    tr, va = mod.chia_train_val(nho, sc)
    te = hs.tap_moc(nho, sc, hs.cac_moc_test(nho))
    with hs.so_luong(1):                   # 1 luồng: mọi lần chạy ra đúng cùng số (mục 4.6)
        hs.dat_seed(0)
        m = hs.MLP(an=1024, revin=True)
        r = hs.huan_luyen(m, tr, va, so_epoch=200, buoc_moi_epoch=50, kien_nhan=15)
        v, t = hs.mase_tap(m, va, sc, nho), hs.mase_tap(m, te, sc, nho)
    print(f"  5 khách từ 11/2013, {ten:24s} mẫu train {len(tr['X']):7,d}  val {len(va['X']):6,d}  "
          f"epoch tốt {int(r['lich_su']['val'].idxmin()) + 1:3d}  MASE val {v:.3f}  MASE test {t:.3f}  {r['giay']:.0f} s")

print("\n== 50 khách (MLP 256 nút + RevIN, 30 epoch × 100 bước)")
for ten, mod_chia, mod_sc in [("chia đúng, scaler train", hs, hs), ("chia ngẫu nhiên, scaler train", hc, hs),
                              ("chia đúng, scaler toàn bộ", hs, hc)]:
    sc = mod_sc.hoc_scaler(df)
    tr, va = mod_chia.chia_train_val(df, sc)
    te = hs.tap_moc(df, sc, moc)
    hs.dat_seed(0)
    m = hs.MLP(revin=True)
    hs.huan_luyen(m, tr, va)
    v, t = hs.mase_tap(m, va, sc, df), hs.mase_tap(m, te, sc, df)
    print(f"  {ten:30s} MASE val {v:.3f}  MASE test {t:.3f}  khoảng lạc quan {t - v:+.3f}")

# %% ---------------------------------------------------------------- 3. bảng chính: 6 mạng + 3 baseline
sc = hs.hoc_scaler(df)
tr, va = hs.chia_train_val(df, sc)
te = hs.tap_moc(df, sc, moc)
print(f"\n== Bảng chính. Mẫu train {len(tr['X']):,} (stride {hs.BUOC_TRAIN}), val {len(va['X']):,}, "
      f"test {len(te['X']):,} = 50 khách × {len(moc)} mốc")
kq = [hs.seasonal_naive(df, moc)]
lich, thoi_gian, mo_hinh = {}, {}, {}
for ten in ["MLP", "LSTM", "TCN"]:
    for rv in (False, True):
        nm = ten + ("+RevIN" if rv else "")
        hs.dat_seed(0)
        m = hs.MO_HINH[ten](revin=rv)
        r = hs.huan_luyen(m, tr, va)
        lich[nm], thoi_gian[nm], mo_hinh[nm] = r["lich_su"], r["giay"], m
        print(f"  {nm:12s} {r['giay']:6.1f} s  {len(r['lich_su'])} epoch (tốt nhất {int(r['lich_su']['val'].idxmin()) + 1})  "
              f"tham số {sum(q.numel() for q in m.parameters()):,}")
        kq.append(hs.du_bao_dl(m, te, sc, nm)[["unique_id", "moc", "ds", nm]])
t = time.time()
kq.append(hs.mstl(df, moc))
thoi_gian["MSTL"] = time.time() - t
t = time.time()
kq.append(hs.lightgbm(df, moc))
thoi_gian["LightGBM"] = time.time() - t
du_bao = reduce(lambda a, b: a.merge(b, on=["unique_id", "moc", "ds"]), kq)
cot = [c for c in du_bao.columns if c not in ("unique_id", "moc", "ds")]
bang = hs.bang_mase(du_bao, df, cot, df.attrs["doi_muc"])
bang["giây"] = [round(thoi_gian.get(c, 0.0)) for c in bang.index]
print(bang.to_string())

# %% ---------------------------------------------------------------- 4. hình lịch sử huấn luyện
fig, ax = plt.subplots(figsize=(8, 3.8))
for nm, mau in [("MLP+RevIN", M["chinh"]), ("LSTM+RevIN", M["phu"]), ("TCN+RevIN", M["ba"])]:
    ls = lich[nm]
    ax.plot(ls["epoch"], ls["train"], color=mau, lw=1.2, ls="--")
    ax.plot(ls["epoch"], ls["val"], color=mau, lw=2, label=nm)
ax.set_xlabel("epoch (mỗi epoch 100 lô × 256 mẫu)")
ax.set_ylabel("MAE trên thang chuẩn hoá")
ax.legend(title="liền: val · đứt: train")
ax.set_title("MLP học nhanh nhất; LSTM và TCN nhỏ vẫn còn giảm sau 30 epoch")
fig.tight_layout()
ve.luu_hinh(fig, HINH / "lich-su.png")

# %% ---------------------------------------------------------------- 5. hình khách hàng đổi mức + RevIN
uid = "T129"
s = df[df["unique_id"] == uid].set_index("ds")["y"]
d = du_bao[du_bao["unique_id"] == uid].merge(df[["unique_id", "ds", "y"]], on=["unique_id", "ds"])
mae = {c: (d["y"] - d[c]).abs().mean() for c in ["MLP", "MLP+RevIN", "SeasonalNaive", "MSTL"]}
print(f"\n{uid}: trung bình trước/sau MOC_TEST {s[s.index < hs.MOC_TEST].mean():,.0f} / {s[s.index >= hs.MOC_TEST].mean():,.0f} kW; "
      + ", ".join(f"MAE {k} {v:,.0f}" for k, v in mae.items()))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1.3, 1]})
tuan = s.resample("W").mean()
a1.plot(tuan.index, tuan, color="k", lw=1)
a1.axvspan(hs.MOC_VAL, hs.MOC_TEST, color=M["phu"], alpha=0.15)
a1.axvspan(hs.MOC_TEST, tuan.index.max(), color=M["ba"], alpha=0.15)
a1.text(hs.MOC_VAL, tuan.max() * 0.98, " val", fontsize=9)
a1.text(hs.MOC_TEST, tuan.max() * 0.98, " test", fontsize=9)
a1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
a1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
a1.set_xlabel("tuần")
a1.set_ylabel("kW (trung bình tuần)")
a1.set_title(f"Khách {uid}: mức tiêu thụ tăng khoảng 40% trong năm 2014")
d["gio"] = d["ds"].dt.hour
tb = d.groupby("gio")[["y", "MLP", "MLP+RevIN"]].mean()
a2.plot(tb.index, tb["y"], color="k", lw=2, label="thực tế")
a2.plot(tb.index, tb["MLP"], color=M["phu"], label="MLP (scaler học trên train)")
a2.plot(tb.index, tb["MLP+RevIN"], color=M["chinh"], label="MLP + RevIN")
a2.set_xticks(range(0, 24, 3))
a2.set_xlabel("giờ trong ngày (trung bình 26 ngày test)")
a2.set_ylabel("kW")
a2.legend(fontsize=8)
a2.set_title("RevIN bám mức mới; scaler cũ kéo về mức cũ")
fig.tight_layout()
ve.luu_hinh(fig, HINH / "doi-muc.png")
print(f"\nXong trong {(time.time() - t0) / 60:.1f} phút")
