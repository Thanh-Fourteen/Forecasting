# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 22 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu
#
# Chạy trong lab/:  python lab.py chay ../dap-an/ve_hinh.py   (lần đầu ~10 phút: backtest 10.000 chuỗi, lưu cache)

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

import tv
from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
M = ve.MAU


def _nap(ten: str, tep: Path):
    spec = importlib.util.spec_from_file_location(ten, tep)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[ten] = mod
    spec.loader.exec_module(mod)
    return mod


hq = _nap("hq", DAY / "hoi_quy.py")
hq_code = _nap("hq_code", DAY.parent / "code" / "hoi_quy.py")     # bản còn chỗ hở, để vẽ đường "rò rỉ"


def rmse(a, b) -> float:
    return float(np.sqrt(np.mean((np.asarray(a) - np.asarray(b)) ** 2)))


def vi_du_tay() -> dict:
    X, y = hq.bang_lag(np.array([10.0, 12, 11, 13, 15]), 2)

    class TrungBinh:
        def predict(self, X):
            return X.mean(axis=1)
    return {"X": X.tolist(), "y": y.tolist(),
            "de_quy": hq.du_bao_de_quy(TrungBinh(), np.array([10.0, 20.0]), 3, 2).tolist()}


def mot_chuoi(df) -> dict:
    """Lab bước 1: rừng ngẫu nhiên LOCAL trên 28 lag của một chuỗi, recursive 14 ngày ở cutoff đầu."""
    uid = df["unique_id"].iloc[0]
    z = df[df["unique_id"] == uid]["z"].to_numpy()
    c = int(np.flatnonzero(df[df["unique_id"] == uid]["ds"].to_numpy() == hq.cac_cutoff(df)[0])[0])
    X, y = hq.bang_lag(z[:c + 1], hq.SO_LAG)
    p = hq.du_bao_de_quy(hq.rung().fit(X, y), z[:c + 1], hq.H, hq.SO_LAG)
    that = z[c + 1:c + 1 + hq.H]
    sn = np.tile(z[c - 6:c + 1], 2)[:hq.H]
    return {"chuoi": uid, "so_dong_bang": len(y), "rmse_rung": rmse(that, p), "rmse_snaive": rmse(that, sn)}


def hinh_chuan_hoa(df) -> dict:
    """Hai chuỗi khác cỡ hàng nghìn lần: thang gốc, rồi z − mức 28 ngày."""
    Y = hq.ma_tran(df, "y")
    tb = Y.iloc[:, -120:].mean(axis=1)
    lon = tb.idxmax()
    nho = tb[(tb > 20) & (tb < 60)].index[0]
    ngay = Y.columns[-120:]
    fig, a = plt.subplots(1, 2, figsize=(10, 3.4))
    for uid, mau in [(lon, M["chinh"]), (nho, M["phu"])]:
        a[0].plot(ngay, Y.loc[uid, ngay], color=mau, label=uid)
        z = np.log1p(Y.loc[uid].to_numpy(float))
        muc = pd.Series(z).rolling(28).mean().shift(1).to_numpy()
        a[1].plot(ngay, (z - muc)[-120:], color=mau, label=uid)
    a[0].set_yscale("log")
    a[0].set_ylabel("lượt xem mỗi ngày (thang log)")
    a[0].set_title("thang gốc: cách nhau hàng nghìn lần", fontsize=9)
    a[1].set_ylabel("z − trung bình z 28 ngày trước")
    a[1].set_title("sau log và trừ mức: cùng một thang", fontsize=9)
    for x in a:
        x.legend(fontsize=8)
        x.tick_params(axis="x", labelrotation=30, labelsize=7)
    fig.suptitle("Chuẩn hoá theo chuỗi đưa trang lớn và trang nhỏ về cùng thang để một mô hình học chung",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "chuan-hoa.png")
    return {"lon": lon, "tb_lon": float(tb[lon]), "nho": nho, "tb_nho": float(tb[nho])}


def hinh_chien_luoc(df300) -> dict:
    kq = hq.chien_luoc(df300)
    kq_ro = hq_code.chien_luoc(df300)
    theo_h = hq.sai_so_theo_h(kq)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for c, mau, ky in [("recursive", M["phu"], "o"), ("direct", M["chinh"], "s"), ("mimo", M["ba"], "^")]:
        ax.plot(theo_h.index, theo_h[c], color=mau, marker=ky, markersize=4, label=c)
    ax.set_xlabel("bước h (ngày sau cutoff)")
    ax.set_ylabel("RMSE trên thang z")
    ax.set_xticks(range(1, hq.H + 1))
    ax.legend()
    ax.set_title("Ba chiến lược gần như trùng nhau ở tuần đầu; recursive kém dần ở tuần thứ hai")
    ve.luu_hinh(fig, HINH / "chien-luoc-theo-h.png")

    ro = hq.sai_so_theo_h(kq_ro, cot=("direct",))["direct"]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(theo_h.index, theo_h["direct"], color=M["chinh"], marker="s", markersize=4, label="direct đúng (lag từ ngày t − h)")
    ax.plot(ro.index, ro, color=M["phu"], marker="x", markersize=5, linestyle="--",
            label="direct sai (lag 1 … 28 cho mọi h)")
    ax.set_xlabel("bước h (ngày sau cutoff)")
    ax.set_ylabel("RMSE trên thang z")
    ax.set_xticks(range(1, hq.H + 1))
    ax.legend()
    ax.set_title("Direct dựng sai 'thắng' ở tầm xa vì nó đọc số của những ngày chưa xảy ra")
    ve.luu_hinh(fig, HINH / "ro-ri-direct.png")

    kq["tuan"] = np.where(kq["buoc_h"] <= 7, 1, 2)
    kq_ro["tuan"] = np.where(kq_ro["buoc_h"] <= 7, 1, 2)
    tuan = {c: kq.groupby("tuan").apply(lambda d, c=c: rmse(d["y"], d[c])).round(4).tolist()
            for c in ["recursive", "direct", "mimo"]}
    tuan["direct_ro_ri"] = kq_ro.groupby("tuan").apply(lambda d: rmse(d["y"], d["direct"])).round(4).tolist()
    return {"so_chuoi": df300["unique_id"].nunique(), "tong": {c: round(rmse(kq["y"], kq[c]), 4)
                                                               for c in ["recursive", "direct", "mimo"]},
            "tong_ro_ri": round(rmse(kq_ro["y"], kq_ro["direct"]), 4), "theo_tuan": tuan,
            "h1": theo_h.loc[1].round(4).to_dict(), "h14": theo_h.loc[14].round(4).to_dict(),
            "ro_h14": round(float(ro.loc[14]), 4)}


def hinh_cay() -> dict:
    rng = np.random.default_rng(0)
    y = 50 + 2 * np.arange(120) + rng.normal(0, 3, 120)
    cay_sai = hq_code.du_bao_cay(y, 14)
    cay_dung = hq.du_bao_cay(y, 14)
    t = np.arange(120)
    tt = np.arange(120, 134)
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(t[-40:], y[-40:], color="black", label="lịch sử")
    ax.plot(tt, 50 + 2 * tt, color="grey", linestyle=":", label="xu hướng thật")
    ax.plot(tt, cay_sai, color=M["phu"], marker="x", markersize=4, label="cây trên mức y")
    ax.plot(tt, cay_dung, color=M["chinh"], marker="o", markersize=3, label="cây trên sai phân, cộng dồn lại")
    ax.axhline(y.max(), color=M["phu"], linewidth=0.6, linestyle="--")
    ax.set_xlabel("ngày")
    ax.set_ylabel("giá trị")
    ax.legend(fontsize=8)
    ax.set_title("Cây không vượt được số lớn nhất đã thấy; học trên sai phân thì theo được xu hướng")
    ve.luu_hinh(fig, HINH / "cay-xu-huong.png")
    return {"max_da_thay": round(float(y.max()), 1), "cay_sai_cuoi": round(float(cay_sai[-1]), 1),
            "cay_dung_cuoi": round(float(cay_dung[-1]), 1), "that_cuoi": 50 + 2 * 133}


def sai_phan_10000(df) -> pd.DataFrame:
    """Global LightGBM với target_transforms=[Differences([1])] — so với không sai phân (cache)."""
    tep = tv.THU_MUC_DU_LIEU.parent / "cache" / f"toan-cuc-sai-phan-{df['unique_id'].nunique()}.parquet"
    if tep.exists():
        return pd.read_parquet(tep)
    import lightgbm as lgb
    from mlforecast import MLForecast
    from mlforecast.lag_transforms import RollingMean
    from mlforecast.target_transforms import Differences
    fc = MLForecast(
        models={"LightGBM_saiphan": lgb.LGBMRegressor(n_estimators=300, learning_rate=0.08, num_leaves=63,
                                                      random_state=hq.SEED, verbose=-1)},
        freq="D", lags=[1, 2, 3, 4, 5, 6, 7, 14, 21, 28],
        lag_transforms={1: [RollingMean(7), RollingMean(28)]}, date_features=["dayofweek"],
        target_transforms=[Differences([1])])
    kq = fc.cross_validation(df[["unique_id", "ds", "z"]], h=hq.H, n_windows=hq.SO_CUA_SO, step_size=hq.H,
                             target_col="z")
    kq.to_parquet(tep)
    return kq


def hinh_global_local(df) -> dict:
    kq = hq.backtest_toan_cuc(df, luu=True).merge(hq.backtest_cuc_bo(df, luu=True).drop(columns="z"),
                                                  on=["unique_id", "ds", "cutoff"])
    kq = kq.merge(sai_phan_10000(df).drop(columns="z"), on=["unique_id", "ds", "cutoff"])
    mo_hinh = ["LightGBM", "LightGBM_saiphan", "AutoETS", "SeasonalNaive", "Naive"]
    r = hq.rmsse_tung_chuoi(kq, df, mo_hinh)
    bang = hq.bang_so_sanh(r)
    kq["h"] = kq.groupby(["unique_id", "cutoff"]).cumcount() + 1
    theo_h = kq.groupby("h").apply(lambda d: pd.Series({m: rmse(d["z"], d[m]) for m in mo_hinh}))
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for m, mau, ky in [("LightGBM", M["chinh"], "s"), ("AutoETS", M["phu"], "o"), ("SeasonalNaive", M["nhat"], "^")]:
        ax.plot(theo_h.index, theo_h[m], color=mau, marker=ky, markersize=4,
                label={"LightGBM": "LightGBM global (1 mô hình)", "AutoETS": "AutoETS local (10.000 mô hình)",
                       "SeasonalNaive": "seasonal naive"}[m])
    ax.set_xlabel("bước h (ngày sau cutoff)")
    ax.set_ylabel("RMSE trên thang z")
    ax.set_xticks(range(1, hq.H + 1))
    ax.legend()
    ax.set_title("10.000 trang: LightGBM global thắng AutoETS local ở mọi h, cách xa dần theo h")
    ve.luu_hinh(fig, HINH / "global-local-theo-h.png")

    c0 = kq["cutoff"].min()
    hoc = df[df["ds"] <= c0]
    muc = hoc.groupby("unique_id")["y"].median().loc[r.index]
    nhom = pd.qcut(muc, 4, labels=["1 (ít nhất)", "2", "3", "4 (nhiều nhất)"])
    theo_muc = pd.DataFrame({"lượt xem trung vị từ": muc.groupby(nhom, observed=True).min(),
                             "đến": muc.groupby(nhom, observed=True).max(),
                             "RMSSE LightGBM": r["LightGBM"].groupby(nhom, observed=True).mean(),
                             "RMSSE AutoETS": r["AutoETS"].groupby(nhom, observed=True).mean(),
                             "% chuỗi LightGBM thắng": (r["LightGBM"] < r["AutoETS"]).groupby(nhom, observed=True).mean() * 100})
    return {"bang": bang.round(3), "theo_muc": theo_muc.round(3),
            "thang_ets_%": round(float((r["LightGBM"] < r["AutoETS"]).mean() * 100), 1),
            "h1": theo_h.loc[1].round(3).to_dict(), "h14": theo_h.loc[14].round(3).to_dict(),
            "so_chuoi_bo": int(df["unique_id"].nunique() - len(r))}


if __name__ == "__main__":
    df = hq.doc_web_traffic()
    print("số chuỗi:", df["unique_id"].nunique(), "cutoff:", [str(c)[:10] for c in hq.cac_cutoff(df)])
    print("ví dụ tay:", vi_du_tay())
    print("một chuỗi:", mot_chuoi(df))
    print("chuẩn hoá:", hinh_chuan_hoa(df))
    print("cây:", hinh_cay())
    print("chiến lược:", hinh_chien_luoc(df[df["unique_id"].isin(df["unique_id"].unique()[:300])]))
    gl = hinh_global_local(df)
    for k, v in gl.items():
        print(k, ":\n", v)
