# %% [markdown]
# # Buổi 23 — Gradient boosting chuyên sâu (ĐÁP ÁN)
#
# Dữ liệu: số món bán mỗi ngày của 500 mã hàng, UCI Online Retail II (bán buôn quà tặng ở Anh), 12/2009 → 12/2011.
# Dự phòng mở cho M5 (M5 cần tài khoản Kaggle và chấp nhận luật cuộc thi).

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

SO_MA = 500           # 500 mã hàng bán nhiều ngày nhất trong phần học
H = 28                # tầm dự báo: 28 ngày bán hàng (như M5)
SO_CUA_SO = 3         # 3 cutoff cách nhau 28 ngày → chấm 84 ngày bán hàng cuối (8/2011 → 12/2011)
M = 6                 # mùa vụ tuần: cửa hàng bán 6 ngày (nghỉ thứ Bảy)
SEED = 0
LAG = [28, 35, 42, 49, 56, 302]               # mọi lag ≥ H: một mô hình cho cả 28 ngày tới; 302 ngày bán ≈ một năm
CUA_SO_TB = [7, 28, 84]                       # trung bình trượt tính lùi từ ngày t − 28
DAC_TRUNG = ([f"lag_{k}" for k in LAG] + [f"tb_{w}" for w in CUA_SO_TB]
             + ["ty_le_ngay_ban_28", "gia", "thu", "ngay_trong_thang", "tuan_trong_nam", "ma"])

THAM_SO = {"objective": "tweedie", "tweedie_variance_power": 1.5, "n_estimators": 400, "learning_rate": 0.03,
           "num_leaves": 63, "min_child_samples": 50, "subsample": 0.8, "subsample_freq": 1,
           "colsample_bytree": 0.8, "random_state": SEED, "verbose": -1, "n_jobs": -1}


# %% [markdown]
# ## Đọc dữ liệu

# %%
def _giao_dich() -> pd.DataFrame:
    """Các dòng bán hợp lệ (số lượng > 0, giá > 0, mã hàng 5 chữ số — bỏ phí bưu điện, điều chỉnh…).
    Đọc .xlsx mất 40–90 giây nên lưu bản gọn sang lab/du-lieu/cache/."""
    cache = tv.THU_MUC_DU_LIEU.parent / "cache" / "giao-dich.parquet"
    if cache.exists():
        return pd.read_parquet(cache)
    tep = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "online_retail_II.xlsx"
    k = pd.concat([pd.read_excel(tep, sheet_name=s, usecols=["StockCode", "Quantity", "InvoiceDate", "Price"])
                   for s in ("Year 2009-2010", "Year 2010-2011")])
    k["StockCode"] = k["StockCode"].astype(str)
    k = k[(k["Quantity"] > 0) & (k["Price"] > 0) & k["StockCode"].str.fullmatch(r"\d{5}[A-Za-z]?")]
    k = pd.DataFrame({"unique_id": k["StockCode"], "ds": k["InvoiceDate"].dt.normalize(),
                      "y": k["Quantity"].astype(float), "doanh_thu": k["Quantity"] * k["Price"]})
    cache.parent.mkdir(parents=True, exist_ok=True)
    k.to_parquet(cache)
    return k


def doc_ban_le(so_ma: int = SO_MA) -> pd.DataFrame:
    """Dạng dài unique_id, ds, t, y (số món), doanh_thu. Chỉ các ngày cửa hàng có bán (bỏ thứ Bảy, nghỉ lễ);
    t đếm ngày bán hàng 0, 1, 2…; ngày mã hàng không bán điền 0. Chọn mã bằng số ngày có bán TRONG PHẦN HỌC."""
    k = _giao_dich()
    ngay = np.sort(k["ds"].unique())
    ngay_ma = k.groupby(["unique_id", "ds"], as_index=False)[["y", "doanh_thu"]].sum()
    cutoff_dau = ngay[len(ngay) - H * SO_CUA_SO - 1]
    dem = ngay_ma[ngay_ma["ds"] <= cutoff_dau].groupby("unique_id").size()
    chon = dem.sort_values(ascending=False, kind="stable").index[:so_ma]
    luoi = pd.MultiIndex.from_product([sorted(chon), ngay], names=["unique_id", "ds"]).to_frame(index=False)
    df = luoi.merge(ngay_ma, on=["unique_id", "ds"], how="left").fillna({"y": 0.0, "doanh_thu": 0.0})
    df["t"] = df.groupby("unique_id").cumcount()
    return df[["unique_id", "ds", "t", "y", "doanh_thu"]]


def cac_cutoff(df: pd.DataFrame) -> list[int]:
    """Ba cutoff (theo t): ngày bán hàng cuối được thấy trước mỗi đoạn 28 ngày chấm."""
    T = int(df["t"].max()) + 1
    return [T - H * (SO_CUA_SO - i) - 1 for i in range(SO_CUA_SO)]


# %% [markdown]
# ## Đặc trưng — mọi thứ tính từ dữ liệu tới ngày t − 28

# %%
def dac_trung(df: pd.DataFrame) -> pd.DataFrame:
    """Đặc trưng cho ngày t, chỉ dùng y và doanh thu tới ngày t − H (lúc dự báo mới biết tới đó).
    gia = doanh thu ÷ số món của 28 ngày kết thúc ở t − H: giá trung bình mỗi món khách đã trả."""
    df = df.sort_values(["unique_id", "t"])
    g = df.groupby("unique_id", sort=False)
    ra = df[["unique_id", "ds", "t"]].copy()
    for k in LAG:
        ra[f"lag_{k}"] = g["y"].shift(k)
    y_cu = g["y"].shift(H)
    for w in CUA_SO_TB:
        ra[f"tb_{w}"] = y_cu.groupby(df["unique_id"], sort=False).transform(
            lambda s, w=w: s.rolling(w, min_periods=1).mean())
    co_ban = (y_cu > 0).astype(float).where(y_cu.notna())
    ra["ty_le_ngay_ban_28"] = co_ban.groupby(df["unique_id"], sort=False).transform(
        lambda s: s.rolling(28, min_periods=1).mean())
    dt_cu = g["doanh_thu"].shift(H)
    tong_dt = dt_cu.groupby(df["unique_id"], sort=False).transform(lambda s: s.rolling(28, min_periods=1).sum())
    tong_y = y_cu.groupby(df["unique_id"], sort=False).transform(lambda s: s.rolling(28, min_periods=1).sum())
    ra["gia"] = (tong_dt / tong_y.where(tong_y > 0)).groupby(df["unique_id"], sort=False).ffill()
    ra["thu"] = df["ds"].dt.dayofweek
    ra["ngay_trong_thang"] = df["ds"].dt.day
    ra["tuan_trong_nam"] = df["ds"].dt.isocalendar().week.astype(int)
    ra["ma"] = df["unique_id"].astype("category")
    return ra


def bang(df: pd.DataFrame) -> pd.DataFrame:
    """Đặc trưng + nhãn y + doanh_thu; bỏ 84 + 28 ngày đầu (chưa đủ lịch sử cho đặc trưng)."""
    b = dac_trung(df).merge(df[["unique_id", "t", "y", "doanh_thu"]], on=["unique_id", "t"])
    return b[b["t"] >= max(CUA_SO_TB) + H].reset_index(drop=True)   # lag_302 trống ở năm đầu: LightGBM tự xử lý ô trống


# %% [markdown]
# ## Huấn luyện, backtest, WRMSSE

# %%
def huan_luyen(b: pd.DataFrame, tham_so: dict | None = None, **ghi_de):
    import lightgbm as lgb
    ts = {**THAM_SO, **(tham_so or {}), **ghi_de}
    return lgb.LGBMRegressor(**ts).fit(b[DAC_TRUNG], b["y"])


def backtest(b: pd.DataFrame, tham_so: dict | None = None, **ghi_de) -> pd.DataFrame:
    """3 cutoff: học trên t ≤ cutoff, dự báo t = cutoff + 1 … cutoff + 28. Trả unique_id, t, cutoff, y, du_bao."""
    ra = []
    for c in cac_cutoff(b):
        m = huan_luyen(b[b["t"] <= c], tham_so, **ghi_de)
        kiem = b[(b["t"] > c) & (b["t"] <= c + H)]
        ra.append(kiem[["unique_id", "t", "y"]].assign(cutoff=c, du_bao=np.maximum(m.predict(kiem[DAC_TRUNG]), 0)))
    return pd.concat(ra, ignore_index=True)


def wrmsse(kq: pd.DataFrame, df: pd.DataFrame, cot: str = "du_bao") -> float:
    """Như M5 ở cấp mã hàng: mỗi cutoff, RMSSE từng mã (mẫu số: bình phương bước nhảy ngày-qua-ngày trên phần học,
    tính từ ngày bán đầu tiên) nhân trọng số = tỷ phần doanh thu của mã trong 28 ngày trước cutoff; rồi trung bình 3 cutoff."""
    diem = []
    for c, kc in kq.groupby("cutoff"):
        hoc = df[df["t"] <= c]
        mau = hoc.groupby("unique_id")["y"].apply(
            lambda s: np.mean(np.diff(s.to_numpy()[np.argmax(s.to_numpy() > 0):]) ** 2))
        dt = hoc[hoc["t"] > c - H].groupby("unique_id")["doanh_thu"].sum()
        mse = kc.assign(e2=(kc["y"] - kc[cot]) ** 2).groupby("unique_id")["e2"].mean()
        dung = mau[mau > 0].index.intersection(mse.index)
        w = dt.loc[dung] / dt.loc[dung].sum()
        diem.append(float((w * np.sqrt(mse.loc[dung] / mau.loc[dung])).sum()))
    return float(np.mean(diem))


def backtest_thong_ke(df: pd.DataFrame) -> pd.DataFrame:
    """Local: AutoETS (mỗi mã một mô hình), seasonal naive 6 ngày, trung bình 28 ngày — cùng 3 cutoff."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, SeasonalNaive, WindowAverage
    sf = StatsForecast(models=[AutoETS(season_length=M), SeasonalNaive(M), WindowAverage(28)], freq=1, n_jobs=-1)
    kq = sf.cross_validation(df=df[["unique_id", "t", "y"]].rename(columns={"t": "ds"}), h=H,
                             n_windows=SO_CUA_SO, step_size=H)
    kq = kq.rename(columns={"ds": "t"})
    mo_hinh = ["AutoETS", "SeasonalNaive", "WindowAverage"]
    kq[mo_hinh] = kq[mo_hinh].clip(lower=0)
    return kq


# %% [markdown]
# ## Tune bằng Optuna trên CV theo thời gian

# %%
def chia_cv(b_hoc: pd.DataFrame, so_fold: int = 3) -> list[tuple[np.ndarray, np.ndarray]]:
    """Fold theo thời gian: mỗi fold kiểm 28 ngày liền, chỉ học trên các ngày TRƯỚC đó (3 fold cuối phần học)."""
    t_max = int(b_hoc["t"].max())
    t = b_hoc["t"].to_numpy()
    ra = []
    for i in range(so_fold, 0, -1):
        c = t_max - H * i
        ra.append((np.flatnonzero(t <= c), np.flatnonzero((t > c) & (t <= c + H))))
    return ra


KHONG_GIAN = {"num_leaves": (8, 256), "min_child_samples": (5, 300), "learning_rate": (0.01, 0.2),
              "colsample_bytree": (0.4, 1.0)}


def diem_cv(b_hoc: pd.DataFrame, tham_so: dict, folds) -> float:
    """RMSE trung bình trên các fold (mỗi fold: học trên chỉ số `hoc`, chấm trên chỉ số `kiem`)."""
    import lightgbm as lgb
    X, y = b_hoc[DAC_TRUNG], b_hoc["y"].to_numpy()
    loi = []
    for hoc, kiem in folds:
        m = lgb.LGBMRegressor(**{**THAM_SO, **tham_so}).fit(X.iloc[hoc], y[hoc])
        loi.append(np.sqrt(np.mean((y[kiem] - m.predict(X.iloc[kiem])) ** 2)))
    return float(np.mean(loi))


def tune(b_hoc: pd.DataFrame, so_thu: int = 50, cv=None, luu: bool = False) -> dict:
    """Optuna (TPE, seed cố định) tìm num_leaves, min_child_samples, learning_rate, colsample_bytree.
    Điểm của một bộ tham số: RMSE trung bình trên các fold của `cv` (mặc định chia_cv). Trả tham số tốt nhất và điểm.
    luu=True: lưu/đọc kết quả ở lab/du-lieu/cache/ (50 thử nghiệm mất vài phút); tên tệp theo dấu vân tay của các fold
    và hàm mất mát, nên đổi cách chia hay đổi objective thì tự chạy lại."""
    import hashlib
    import json
    folds = cv if cv is not None else chia_cv(b_hoc)
    van_tay = hashlib.sha256(repr([(len(b_hoc), so_thu, THAM_SO["objective"])]
                                  + [(h.tobytes(), k.tobytes()) for h, k in folds]).encode()).hexdigest()[:12]
    tep = tv.THU_MUC_DU_LIEU.parent / "cache" / f"tune-{van_tay}.json"
    if luu and tep.exists():
        return json.loads(tep.read_text())
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    def muc_tieu(trial):
        ts = {"num_leaves": trial.suggest_int("num_leaves", *KHONG_GIAN["num_leaves"], log=True),
              "min_child_samples": trial.suggest_int("min_child_samples", *KHONG_GIAN["min_child_samples"], log=True),
              "learning_rate": trial.suggest_float("learning_rate", *KHONG_GIAN["learning_rate"], log=True),
              "colsample_bytree": trial.suggest_float("colsample_bytree", *KHONG_GIAN["colsample_bytree"]),
              "n_estimators": 200}
        return diem_cv(b_hoc, ts, folds)

    st = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=SEED))
    st.optimize(muc_tieu, n_trials=so_thu)
    ra = {**st.best_params, "n_estimators": 200, "diem_cv": st.best_value}
    if luu:
        tep.parent.mkdir(parents=True, exist_ok=True)
        tep.write_text(json.dumps(ra))
    return ra


# %% [markdown]
# ## Diễn giải: SHAP cho một dự báo, partial dependence của giá

# %%
def shap_mot_dong(mo_hinh, x: pd.DataFrame) -> pd.Series:
    """Đóng góp SHAP (TreeSHAP có sẵn trong LightGBM) của từng đặc trưng cho MỘT dòng, trên thang log (Tweedie
    dùng hàm liên kết log). Phần tử cuối 'goc' là mức nền; cộng tất cả = log(dự báo)."""
    dong = mo_hinh.predict(x[DAC_TRUNG], pred_contrib=True)[0]
    return pd.Series(dong, index=DAC_TRUNG + ["goc"])


def phu_thuoc_rieng(mo_hinh, X: pd.DataFrame, cot: str, luoi: np.ndarray) -> np.ndarray:
    """Partial dependence: đặt cột `cot` = từng giá trị của lưới cho MỌI dòng của X, lấy trung bình dự báo."""
    return np.array([mo_hinh.predict(X[DAC_TRUNG].assign(**{cot: v})).mean() for v in luoi])


def tham_so_don_dieu(tham_so: dict | None = None) -> dict:
    """Ràng buộc: dự báo không được tăng khi giá tăng (−1 ở cột 'gia', 0 ở cột khác)."""
    rang_buoc = [-1 if c == "gia" else 0 for c in DAC_TRUNG]
    return {**(tham_so or {}), "monotone_constraints": rang_buoc, "monotone_constraints_method": "advanced"}


# %%
if __name__ == "__main__":
    df = doc_ban_le()
    b = bang(df)
    print(df["unique_id"].nunique(), "mã;", len(b), "dòng học; cutoff", cac_cutoff(df))
    for muc_tieu in ["regression", "tweedie"]:
        print(muc_tieu, round(wrmsse(backtest(b, objective=muc_tieu), df), 4))
