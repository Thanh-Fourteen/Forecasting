# %% [markdown]
# # Buổi 24 — Ensemble, chọn mô hình, AutoML (M4 theo tháng)
#
# Điểm xuất phát (có chỗ cố tình sai).
# Dữ liệu: 1.000 chuỗi tháng chọn ngẫu nhiên (seed 0) trong M4 (Monash Time Series Forecasting Repository, CC BY 4.0).

# %%
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")
os.environ.setdefault("NIXTLA_ID_AS_COL", "1")

SO_CHUOI = 1000       # số chuỗi chọn ngẫu nhiên trong 32.097 chuỗi dài ≥ 150 tháng
DAI = 150             # giữ 150 tháng cuối mỗi chuỗi
H = 18                # tầm dự báo 18 tháng (như M4)
M = 12                # mùa vụ năm
SEED = 0
CUTOFF = [95, 113, 131]     # tháng cuối được thấy trước mỗi cửa sổ 18 tháng: W1, W2, W3
CUA_SO_CHON = [95, 113, 131]       # cửa sổ dùng để chọn mô hình / ước lượng trọng số
CUA_SO_BAO_CAO = [95, 113, 131]    # cửa sổ dùng để báo cáo
CACHE = tv.THU_MUC_DU_LIEU.parent / "cache"

THAM_SO_LGBM = {"n_estimators": 300, "learning_rate": 0.05, "num_leaves": 31, "min_child_samples": 50,
                "subsample": 0.8, "subsample_freq": 1, "colsample_bytree": 0.8, "objective": "l1",
                "random_state": SEED, "verbose": -1, "n_jobs": 4}
CO_BAN = ["AutoETS", "AutoTheta", "LGBM"]    # ba mô hình của ensemble chính


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_m4(so_chuoi: int = SO_CHUOI) -> pd.DataFrame:
    """Dạng dài unique_id, ds (0…149), y, thang (1–12), ngay (đầu tháng). Đọc thẳng tệp .tsf (dưới 1 giây)."""
    tep = tv.THU_MUC_DU_LIEU / "monash-m4-monthly" / "m4_monthly_dataset.tsf"
    ids, bat_dau, gia_tri = [], [], []
    with open(tep, encoding="latin-1") as f:
        da_toi = False
        for dong in f:
            if not da_toi:
                da_toi = dong.startswith("@data")
                continue
            a, b, c = dong.rstrip("\n").split(":", 2)
            ids.append(a)
            bat_dau.append(b[:10])
            gia_tri.append(np.array(c.split(","), dtype=float))
    du_dai = [i for i, v in enumerate(gia_tri) if len(v) >= DAI]
    chon = sorted(np.random.default_rng(SEED).choice(du_dai, SO_CHUOI, replace=False))[:so_chuoi]
    phan = []
    for i in chon:
        dau = pd.Period(bat_dau[i], "M") + (len(gia_tri[i]) - DAI)
        ngay = pd.period_range(dau, periods=DAI, freq="M").to_timestamp()
        phan.append(pd.DataFrame({"unique_id": ids[i], "ds": np.arange(DAI), "y": gia_tri[i][-DAI:],
                                  "thang": ngay.month, "ngay": ngay}))
    return pd.concat(phan, ignore_index=True)


# %% [markdown]
# ## 30 ứng viên: 22 mô hình thống kê, 2 LightGBM global, 6 kết hợp định sẵn

# %%
def _mo_hinh_thong_ke() -> list:
    from statsforecast.models import (
        AutoETS,
        AutoTheta,
        DynamicOptimizedTheta,
        HistoricAverage,
        Holt,
        HoltWinters,
        Naive,
        OptimizedTheta,
        RandomWalkWithDrift,
        SeasonalExponentialSmoothingOptimized,
        SeasonalNaive,
        SeasonalWindowAverage,
        SimpleExponentialSmoothing,
        Theta,
        WindowAverage,
    )
    return [Naive(), SeasonalNaive(M), RandomWalkWithDrift(), HistoricAverage(),
            WindowAverage(3, alias="TB3"), WindowAverage(6, alias="TB6"), WindowAverage(12, alias="TB12"),
            SeasonalWindowAverage(M, 2, alias="STB2"), SeasonalWindowAverage(M, 3, alias="STB3"),
            *[SimpleExponentialSmoothing(a, alias=f"SES{a}") for a in (0.1, 0.3, 0.5, 0.7, 0.9)],
            Holt(M), HoltWinters(M), AutoETS(season_length=M), AutoTheta(season_length=M), Theta(M),
            OptimizedTheta(M), DynamicOptimizedTheta(M), SeasonalExponentialSmoothingOptimized(M)]


def du_bao_thong_ke(df: pd.DataFrame, cutoff: list[int] = CUTOFF) -> pd.DataFrame:
    """22 mô hình thống kê, mỗi cutoff chỉ học trên y tới cutoff. Cột: unique_id, ds, cutoff, <mô hình>…"""
    from statsforecast import StatsForecast
    ra = []
    for c in cutoff:
        hoc = df[df["ds"] <= c][["unique_id", "ds", "y"]]
        f = StatsForecast(models=_mo_hinh_thong_ke(), freq=1, n_jobs=-1).forecast(df=hoc, h=H)
        ra.append(f.assign(cutoff=c))
    return pd.concat(ra, ignore_index=True)


TRE = list(range(24))    # 24 tháng gần nhất (trễ 0 = chính tháng gốc)


def dac_trung(df: pd.DataFrame) -> pd.DataFrame:
    """Đặc trưng tại mỗi tháng gốc o của mỗi chuỗi, chỉ dùng y tới o: y[o − k] / mức(o) với k = 0…23, mức(o) =
    trung bình 12 tháng tới o (đưa mọi chuỗi về cùng thang), và tháng trong năm của o."""
    df = df.sort_values(["unique_id", "ds"])
    g = df.groupby("unique_id", sort=False)["y"]
    ra = df[["unique_id", "ds", "thang"]].copy()
    ra["muc"] = g.transform(lambda s: s.rolling(12).mean())
    for k in TRE:
        ra[f"tre_{k}"] = g.shift(k) / ra["muc"]
    return ra


def du_bao_lgbm(df: pd.DataFrame, cutoff: list[int] = CUTOFF, ten: str = "LGBM", **ghi_de) -> pd.DataFrame:
    """LightGBM global, chiến lược direct: mỗi bước h = 1…18 một mô hình, học chung mọi chuỗi.
    Mỗi dòng học là một tháng gốc o (từ tháng thứ 36) của một chuỗi; nhãn y[o + h] / mức(o), chỉ khi o + h ≤ cutoff."""
    import lightgbm as lgb
    ts = {**THAM_SO_LGBM, **ghi_de}
    cot = [f"tre_{k}" for k in TRE] + ["thang"]
    ra = []
    for c in cutoff:
        d = df[df["ds"] <= c].sort_values(["unique_id", "ds"])
        dt = dac_trung(d)
        g = d.groupby("unique_id", sort=False)["y"]
        hoc = dt["ds"] >= 35
        cuoi = dt[dt["ds"] == c]
        P = np.zeros((len(cuoi), H))
        for h in range(1, H + 1):
            nhan = g.shift(-h) / dt["muc"]
            co = hoc & nhan.notna()
            m = lgb.LGBMRegressor(**ts).fit(dt.loc[co, cot], nhan[co])
            P[:, h - 1] = m.predict(cuoi[cot]) * cuoi["muc"].to_numpy()
        ra.append(pd.DataFrame({"unique_id": np.repeat(cuoi["unique_id"].to_numpy(), H),
                                "ds": np.tile(np.arange(c + 1, c + 1 + H), len(cuoi)), "cutoff": c, ten: P.ravel()}))
    return pd.concat(ra, ignore_index=True)


KET_HOP = {   # định sẵn TRƯỚC khi nhìn kết quả — không chọn thành phần theo điểm
    "TB(ETS,Theta,LGBM)": ["AutoETS", "AutoTheta", "LGBM"],
    "TB(ETS,Theta)": ["AutoETS", "AutoTheta"],
    "TB(ETS,LGBM)": ["AutoETS", "LGBM"],
    "TB(Theta,LGBM)": ["AutoTheta", "LGBM"],
    "TB(5 mô hình)": ["AutoETS", "AutoTheta", "DynamicOptimizedTheta", "HoltWinters", "LGBM"],
}


def them_ket_hop(fc: pd.DataFrame) -> pd.DataFrame:
    fc = fc.copy()
    for ten, tp in KET_HOP.items():
        fc[ten] = fc[tp].mean(axis=1)
    fc["TV(ETS,Theta,LGBM)"] = fc[CO_BAN].median(axis=1)
    return fc


def du_bao_30(df: pd.DataFrame, luu: bool = False) -> pd.DataFrame:
    """Dự báo của 30 ứng viên ở 3 cutoff (unique_id, ds, cutoff, y, <30 cột>). luu=True: đọc/ghi cache (~2 phút lần đầu)."""
    tep = CACHE / f"du-bao-30-{df['unique_id'].nunique()}.parquet"
    if luu and tep.exists():
        return pd.read_parquet(tep)
    fc = du_bao_thong_ke(df)
    for ten, gd in [("LGBM", {}), ("LGBM_L2", {"objective": "l2"})]:
        fc = fc.merge(du_bao_lgbm(df, ten=ten, **gd), on=["unique_id", "ds", "cutoff"])
    fc = them_ket_hop(fc).merge(df[["unique_id", "ds", "y"]], on=["unique_id", "ds"])
    if luu:
        tep.parent.mkdir(parents=True, exist_ok=True)
        fc.to_parquet(tep)
    return fc


def ung_vien(fc: pd.DataFrame) -> list[str]:
    return [c for c in fc.columns if c not in ("unique_id", "ds", "cutoff", "y")]


# %% [markdown]
# ## MASE theo chuỗi và cửa sổ

# %%
def mau_so_mase(df: pd.DataFrame, cutoff: list[int] = CUTOFF) -> pd.DataFrame:
    """Mẫu số MASE của từng chuỗi ở từng cutoff: MAE của 'lặp lại cùng tháng năm trước' trên phần học tới cutoff."""
    ra = []
    for c in cutoff:
        s = df[df["ds"] <= c].groupby("unique_id")["y"].apply(
            lambda y: np.mean(np.abs(y.to_numpy()[M:] - y.to_numpy()[:-M])))
        ra.append(pd.DataFrame({"unique_id": s.index, "cutoff": c, "mau_so": s.to_numpy()}))
    return pd.concat(ra, ignore_index=True)


def mase(fc: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """Bảng MASE: mỗi dòng một (chuỗi, cutoff), mỗi cột một ứng viên."""
    f = fc.merge(mau_so_mase(df, sorted(fc["cutoff"].unique())), on=["unique_id", "cutoff"])
    loi = f[ung_vien(fc)].sub(f["y"], axis=0).abs().div(f["mau_so"], axis=0)
    loi[["unique_id", "cutoff"]] = f[["unique_id", "cutoff"]]
    return loi.groupby(["unique_id", "cutoff"]).mean()


# %% [markdown]
# ## Chọn mô hình và báo cáo

# %%
def chon_va_bao_cao(diem: pd.DataFrame, theo_chuoi: bool = True,
                    cua_so_chon: list[int] = CUA_SO_CHON, cua_so_bao_cao: list[int] = CUA_SO_BAO_CAO) -> dict:
    """Chọn ứng viên có MASE nhỏ nhất trên cua_so_chon (mỗi chuỗi một lựa chọn, hoặc một lựa chọn chung),
    rồi báo cáo MASE của lựa chọn đó trên cua_so_bao_cao."""
    chon = diem[diem.index.get_level_values("cutoff").isin(cua_so_chon)].groupby("unique_id").mean()
    bc = diem[diem.index.get_level_values("cutoff").isin(cua_so_bao_cao)].groupby("unique_id").mean()
    if theo_chuoi:
        lua_chon = chon.idxmin(axis=1)
        diem_chon = chon.min(axis=1).mean()
        diem_bc = float(np.mean([bc.at[u, m] for u, m in lua_chon.items()]))
    else:
        m = chon.mean().idxmin()
        lua_chon = pd.Series(m, index=chon.index)
        diem_chon, diem_bc = chon[m].mean(), bc[m].mean()
    return {"lua_chon": lua_chon, "diem_luc_chon": float(diem_chon), "diem_bao_cao": float(diem_bc),
            "lac_quan": float(diem_bc - diem_chon)}


def lac_quan_theo_so_ung_vien(diem: pd.DataFrame, so: tuple[int, ...] = (1, 3, 5, 10, 20, 30), lan: int = 50) -> pd.DataFrame:
    """Chọn theo từng chuỗi trong k ứng viên rút ngẫu nhiên (lan lần mỗi k): MASE trung bình lúc chọn, lúc báo cáo,
    và khoảng lạc quan = báo cáo − lúc chọn."""
    rng = np.random.default_rng(SEED)
    cot = list(diem.columns)
    ra = {}
    for k in so:
        kq = [chon_va_bao_cao(diem[list(rng.choice(cot, k, replace=False))]) for _ in range(lan)]
        ra[k] = {t: np.mean([r[t] for r in kq]) for t in ("diem_luc_chon", "diem_bao_cao", "lac_quan")}
    return pd.DataFrame(ra).T.rename_axis("so_ung_vien")


# %% [markdown]
# ## Trọng số kết hợp: đều, theo sai số, "tối ưu"

# %%
def trong_so(fc: pd.DataFrame, cach: str, thanh_phan: list[str] = CO_BAN,
             cua_so: list[int] = CUA_SO_CHON) -> pd.DataFrame:
    """Trọng số của từng chuỗi, ước lượng CHỈ trên cua_so (backtest trước đoạn báo cáo).
    cach = "deu" | "nghich_mse" (tỷ lệ nghịch với MSE) | "toi_uu" (bình phương tối thiểu, trọng số ≥ 0)."""
    from scipy.optimize import nnls
    f = fc[fc["cutoff"].isin(cua_so)]
    ra = {}
    for uid, g in f.groupby("unique_id"):
        X, y = g[thanh_phan].to_numpy(), g["y"].to_numpy()
        if cach == "deu":
            w = np.full(len(thanh_phan), 1 / len(thanh_phan))
        elif cach == "nghich_mse":
            w = 1 / ((X - y[:, None]) ** 2).mean(axis=0).clip(1e-12)
            w = w / w.sum()
        elif cach == "toi_uu":
            w = nnls(X, y)[0]
        else:
            raise ValueError(cach)
        ra[uid] = w
    return pd.DataFrame(ra, index=thanh_phan).T


def ap_trong_so(fc: pd.DataFrame, w: pd.DataFrame, ten: str) -> pd.DataFrame:
    fc = fc.copy()
    ww = w.loc[fc["unique_id"]].to_numpy()
    fc[ten] = (fc[list(w.columns)].to_numpy() * ww).sum(axis=1)
    return fc


# %% [markdown]
# ## AutoGluon-TimeSeries

# %%
def chay_autogluon(df: pd.DataFrame, cutoff: int = CUTOFF[-1], time_limit: int = 300,
                   preset: str = "medium_quality") -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Học trên y tới cutoff (AutoGluon tự giữ 18 tháng cuối làm đoạn kiểm để xếp hạng và dựng ensemble),
    dự báo 18 tháng sau cutoff. Loại Chronos-2 và Toto-2: mô hình tiền huấn luyện đã thấy M4.
    Trả (dự báo: unique_id, ds, cutoff, <mô hình>…), leaderboard, trọng số ensemble."""
    import logging

    from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
    logging.getLogger("autogluon").setLevel(logging.ERROR)
    d = df.rename(columns={"unique_id": "item_id", "ngay": "timestamp", "y": "target"})
    hoc = TimeSeriesDataFrame.from_data_frame(d[d["ds"] <= cutoff][["item_id", "timestamp", "target"]])
    kiem = TimeSeriesDataFrame.from_data_frame(d[d["ds"] <= cutoff + H][["item_id", "timestamp", "target"]])
    p = TimeSeriesPredictor(prediction_length=H, eval_metric="MASE", freq="MS", verbosity=0,
                            path=str(CACHE / f"autogluon-{cutoff}")).fit(
        hoc, presets=preset, time_limit=time_limit, excluded_model_types=["Chronos2", "Toto2"], random_seed=SEED)
    bxh = p.leaderboard(kiem)[["model", "score_val", "score_test", "fit_time_marginal"]]
    ra = []
    for m in bxh["model"]:
        f = p.predict(hoc, model=m)["mean"].reset_index()
        ra.append(f.rename(columns={"item_id": "unique_id", "mean": m}).set_index(["unique_id", "timestamp"]))
    fc = pd.concat(ra, axis=1).reset_index().rename(columns={"timestamp": "ngay"})
    fc = fc.merge(d.rename(columns={"item_id": "unique_id", "timestamp": "ngay"})[["unique_id", "ngay", "ds"]],
                  on=["unique_id", "ngay"]).drop(columns="ngay").assign(cutoff=cutoff)
    ens = p._trainer.load_model(p.model_best)
    trong = dict(getattr(ens, "model_to_weight", {p.model_best: 1.0}))
    return fc, bxh, trong


if __name__ == "__main__":
    df = doc_m4()
    fc = du_bao_30(df, luu=True)
    diem = mase(fc, df)
    print(diem.groupby("cutoff").mean().T.sort_values(131).round(3).head(12))
    print({k: round(v, 3) for k, v in chon_va_bao_cao(diem).items() if k != "lua_chon"})
    if os.environ.get("AG"):
        print(chay_autogluon(df)[1])
