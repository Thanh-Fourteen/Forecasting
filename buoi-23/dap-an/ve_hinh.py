# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 23 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (lần đầu ~10 phút: hai lượt Optuna 50 thử nghiệm, lưu cache)

# %%
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
M = ve.MAU
spec = importlib.util.spec_from_file_location("bo", DAY / "boosting.py")
bo = importlib.util.module_from_spec(spec)
sys.modules["bo"] = bo
spec.loader.exec_module(bo)

TEN = {"lag_28": "bán ngày t−28", "lag_35": "bán ngày t−35", "lag_42": "bán ngày t−42", "lag_49": "bán ngày t−49",
       "lag_56": "bán ngày t−56", "lag_302": "bán cùng ngày năm trước", "tb_7": "trung bình 7 ngày",
       "tb_28": "trung bình 28 ngày", "tb_84": "trung bình 84 ngày", "ty_le_ngay_ban_28": "tỷ lệ ngày có bán",
       "gia": "giá trung bình mỗi món", "thu": "thứ trong tuần", "ngay_trong_thang": "ngày trong tháng",
       "tuan_trong_nam": "tuần trong năm", "ma": "mã hàng"}


def vi_du_boosting() -> dict:
    """Hai vòng tăng cường bằng tay: y = 2, 4, 9, 13; cây 1 nhánh chia x < 2,5; học suất 0,5."""
    y = np.array([2.0, 4, 9, 13])
    f0 = y.mean()
    du1 = y - f0
    trai, phai = du1[:2].mean(), du1[2:].mean()
    f1 = f0 + 0.5 * np.r_[trai, trai, phai, phai]
    du2 = y - f1
    trai2, phai2 = du2[:2].mean(), du2[2:].mean()
    f2 = f1 + 0.5 * np.r_[trai2, trai2, phai2, phai2]
    return {"f0": f0, "du1": du1.tolist(), "la1": (trai, phai), "f1": f1.tolist(), "du2": du2.tolist(),
            "f2": f2.tolist(), "sse": [float(((y - f) ** 2).sum()) for f in (np.full(4, f0), f1, f2)]}


def hinh_phan_phoi(df) -> dict:
    y = df["y"].to_numpy()
    ma = df.groupby("unique_id")["doanh_thu"].sum().sort_values().index[len(df["unique_id"].unique()) // 2]
    d = df[df["unique_id"] == ma]
    fig, a = plt.subplots(1, 2, figsize=(10, 3.4))
    bins = np.r_[-0.5, np.unique(np.round(np.logspace(0, np.log10(y.max() + 1), 30))) - 0.5, y.max() + 0.5]
    a[0].hist(y, bins=bins, color=M["chinh"])
    a[0].set_xscale("symlog", linthresh=1)
    a[0].set_yscale("log")
    a[0].set_xlabel("số món bán trong một ngày của một mã (thang log)")
    a[0].set_ylabel("số (mã, ngày) (thang log)")
    a[0].set_title(f"{(y == 0).mean():.0%} ô bằng 0; đuôi dài tới {int(y.max()):,} món".replace(",", "."), fontsize=9)
    a[1].bar(d["ds"], d["y"], width=1.0, color=M["phu"])
    a[1].set_ylabel("số món")
    a[1].set_title(f"mã {ma}: phần lớn ngày bán ít, vài ngày bán rất nhiều", fontsize=9)
    a[1].tick_params(axis="x", labelrotation=30, labelsize=7)
    fig.suptitle("Số món bán mỗi ngày: nhiều số 0, lệch phải — không giống hình chuông mà L2 ngầm giả định",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "phan-phoi-dem.png")
    return {"ty_le_0": round(float((y == 0).mean()), 4), "trung_vi": float(np.median(y)), "tb": round(float(y.mean()), 2),
            "max": float(y.max()), "q99": float(np.quantile(y, 0.99)), "ma": ma}


def bang_wrmsse(df, b, p_tg, p_kf) -> pd.DataFrame:
    tk = bo.backtest_thong_ke(df)
    hang = {m: bo.wrmsse(tk, df, m) for m in ["SeasonalNaive", "WindowAverage", "AutoETS"]}
    hang["LightGBM L2"] = bo.wrmsse(bo.backtest(b, objective="regression"), df)
    hang["LightGBM Poisson"] = bo.wrmsse(bo.backtest(b, objective="poisson"), df)
    hang["LightGBM Tweedie"] = bo.wrmsse(bo.backtest(b), df)
    hang["Tweedie, tune bằng KFold ngẫu nhiên"] = bo.wrmsse(bo.backtest(b, p_kf), df)
    hang["Tweedie, tune bằng CV thời gian"] = bo.wrmsse(bo.backtest(b, p_tg), df)
    hang["Tweedie + ràng buộc giá"] = bo.wrmsse(bo.backtest(b, bo.tham_so_don_dieu()), df)
    return pd.Series(hang, name="WRMSSE").round(4)


def bang_optuna(b_hoc, p_tg, p_kf) -> pd.DataFrame:
    """Chấm hai bộ tham số đã chọn bằng CẢ HAI cách chia (RMSE trung bình 3 fold)."""
    from sklearn.model_selection import KFold
    kf = list(KFold(3, shuffle=True, random_state=bo.SEED).split(b_hoc))
    tg = bo.chia_cv(b_hoc)
    ra = {}
    for ten, p in [("chọn bằng KFold", p_kf), ("chọn bằng CV thời gian", p_tg)]:
        ra[ten] = {"num_leaves": p["num_leaves"], "min_child_samples": p["min_child_samples"],
                   "learning_rate": round(p["learning_rate"], 4), "RMSE KFold": bo.diem_cv(b_hoc, p, kf),
                   "RMSE CV thời gian": bo.diem_cv(b_hoc, p, tg)}
    return pd.DataFrame(ra).T


def hinh_tam_quan_trong(m) -> dict:
    gain = pd.Series(m.booster_.feature_importance("gain"), index=bo.DAC_TRUNG)
    split = pd.Series(m.booster_.feature_importance("split"), index=bo.DAC_TRUNG)
    gain, split = gain / gain.sum() * 100, split / split.sum() * 100
    thu_tu = gain.sort_values().index
    fig, a = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    a[0].barh([TEN[c] for c in thu_tu], gain[thu_tu], color=M["chinh"])
    a[0].set_title("gain: tổng mức giảm mất mát (%)", fontsize=9)
    a[1].barh([TEN[c] for c in thu_tu], split[thu_tu], color=M["phu"])
    a[1].set_title("split: số lần được dùng để chia (%)", fontsize=9)
    for x in a:
        x.set_xlabel("% của tổng")
    fig.suptitle("Hai thước đo 'quan trọng' xếp hạng khác nhau: đừng đọc một cái như sự thật",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "tam-quan-trong.png")
    return {"gain_top": gain.sort_values(ascending=False).head(5).round(1).to_dict(),
            "split_top": split.sort_values(ascending=False).head(5).round(1).to_dict()}


def hinh_shap(m, b, c) -> dict:
    kiem = b[(b["t"] > c) & (b["t"] <= c + bo.H)].copy()
    kiem["du_bao"] = m.predict(kiem[bo.DAC_TRUNG])
    kiem["ty_so"] = kiem["du_bao"] / kiem["tb_28"].clip(lower=1)
    dong = kiem[kiem["tb_28"] >= 5].sort_values("ty_so", ascending=False).iloc[[0]]
    s = bo.shap_mot_dong(m, dong)
    goc = s["goc"]
    dong_gop = s.drop("goc")
    lon = dong_gop.abs().sort_values(ascending=False).index[:6]
    con_lai = dong_gop.drop(lon).sum()
    muc = list(lon) + ["(các đặc trưng còn lại)"]
    gia_tri = list(dong_gop[lon]) + [con_lai]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    x = goc
    for i, (ten, v) in enumerate(zip(muc, gia_tri, strict=True)):
        ax.barh(i, v, left=x, color=M["phu"] if v > 0 else M["chinh"])
        nhan = TEN.get(ten, ten)
        if ten in dong.columns:
            gt = dong[ten].iloc[0]
            nhan += (f" = {gt:.1f}".replace(".", ",") if isinstance(gt, float) and gt % 1 else f" = {gt:.0f}"
                     if isinstance(gt, float) else f" = {gt}")
        ax.text(max(x, x + v) + 0.03, i, f"{v:+.2f}".replace(".", ","), va="center", fontsize=8)
        ax.set_yticks(range(len(muc)))
        x += v
        muc[i] = nhan
    ax.set_yticks(range(len(muc)), muc, fontsize=8)
    ax.invert_yaxis()
    ax.axvline(goc, color="grey", linestyle=":", linewidth=0.8)
    ax.axvline(x, color="black", linestyle="--", linewidth=0.8)
    ax.set_xlabel("log(số món dự báo) — cộng dồn từ mức nền (chấm) tới dự báo (gạch)")
    r = dong.iloc[0]
    ax.set_title(f"Mã {r['unique_id']}, {pd.Timestamp(r['ds']):%d/%m/%Y}: dự báo {np.exp(x):.0f} món, thực tế {r['y']:.0f} — "
                 "mã hàng, tuần Giáng sinh và trung bình 28 ngày đẩy dự báo lên")
    ve.luu_hinh(fig, HINH / "shap-mot-du-bao.png")
    return {"ma": r["unique_id"], "ngay": str(pd.Timestamp(r["ds"]).date()), "du_bao": float(np.exp(x)),
            "y_that": float(r["y"]), "goc_log": float(goc), "goc_mon": float(np.exp(goc)),
            "dong_gop": {TEN.get(k, k): round(float(v), 3) for k, v in zip(list(lon) + ["con_lai"], gia_tri, strict=True)},
            "gia_tri_dac_trung": {k: (float(r[k]) if k != "ma" else str(r[k])) for k in lon},
            "tb_28": float(r["tb_28"])}


def hinh_pd(m, m_dd, b, c) -> dict:
    X = b[(b["t"] > c) & (b["t"] <= c + bo.H)]
    luoi = np.round(np.linspace(*np.nanquantile(b["gia"], [0.02, 0.98]), 25), 2)
    tu_do = bo.phu_thuoc_rieng(m, X, "gia", luoi)
    rang = bo.phu_thuoc_rieng(m_dd, X, "gia", luoi)
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(luoi, tu_do, color=M["phu"], marker="x", markersize=4, label="không ràng buộc")
    ax.plot(luoi, rang, color=M["chinh"], marker="o", markersize=3, label="ràng buộc: giá tăng thì dự báo không tăng")
    ax.set_xlabel("giá trung bình mỗi món trong 28 ngày trước (£)")
    ax.set_ylabel("dự báo trung bình (món/ngày)")
    ax.legend()
    ax.set_title("Không ràng buộc, mô hình 'tin' giá cao hơn thì bán nhiều hơn (đoạn £0,3 → £3)")
    ve.luu_hinh(fig, HINH / "pd-gia.png")
    return {"luoi": luoi.tolist(), "tu_do": np.round(tu_do, 2).tolist(), "rang_buoc": np.round(rang, 2).tolist()}


if __name__ == "__main__":
    df = bo.doc_ban_le()
    b = bo.bang(df)
    cut = bo.cac_cutoff(df)
    ngay = df.drop_duplicates("t").set_index("t")["ds"]
    print("mã:", df["unique_id"].nunique(), "ngày bán hàng:", df["t"].nunique(), df["ds"].min().date(), "→",
          df["ds"].max().date(), "dòng học:", len(b))
    print("cutoff:", cut, [str(ngay[c].date()) for c in cut], "cuối:", str(ngay[cut[-1] + bo.H].date()))
    print("ví dụ boosting:", vi_du_boosting())
    print("phân phối:", hinh_phan_phoi(df))
    b_hoc = b[b["t"] <= cut[0]].reset_index(drop=True)
    from sklearn.model_selection import KFold
    p_tg = bo.tune(b_hoc, 50, luu=True)
    p_kf = bo.tune(b_hoc, 50, cv=list(KFold(3, shuffle=True, random_state=bo.SEED).split(b_hoc)), luu=True)
    p_tg = {k: v for k, v in p_tg.items() if k != "diem_cv"}
    p_kf = {k: v for k, v in p_kf.items() if k != "diem_cv"}
    print("optuna:\n", bang_optuna(b_hoc, p_tg, p_kf).round(3).to_string())
    print("WRMSSE:\n", bang_wrmsse(df, b, p_tg, p_kf).to_string())
    m = bo.huan_luyen(b[b["t"] <= cut[-1]])
    m_dd = bo.huan_luyen(b[b["t"] <= cut[-1]], bo.tham_so_don_dieu())
    print("tầm quan trọng:", hinh_tam_quan_trong(m))
    print("shap:", hinh_shap(m, b, cut[-1]))
    print("pd:", hinh_pd(m, m_dd, b, cut[-1]))
