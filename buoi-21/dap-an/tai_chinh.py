# %% [markdown]
# # Buổi 21 — Chuỗi tài chính và biến động (ĐÁP ÁN)
#
# Dữ liệu: giá BTC/USDT theo giờ 2023–2024 (Binance Public Data); tỷ giá JPY/USD theo ngày 2000–2024 (Federal Reserve H.10).

# %%
from __future__ import annotations

import glob
import warnings

import numpy as np
import pandas as pd
from scipy import stats

import tv
from tv.backtest import diebold_mariano

warnings.simplefilter("ignore")

MOC = "2024-01-01"          # BTC: học 2023, chấm 2024
MOC_JPY = "2020-01-01"      # JPY: học 2000–2019, chấm 2020–2024
CUA_SO = 10                 # demo đoán giá: nhìn 10 ngày trước
MUC_VAR = 0.01              # VaR 99%: lỗ vượt VaR 1% số ngày


# %% [markdown]
# ## Đọc dữ liệu, lợi suất

# %%
def doc_btc_gio() -> pd.Series:
    """Giá đóng cửa BTC/USDT mỗi giờ (UTC), 1/1/2023 → 31/12/2024."""
    tep = sorted(glob.glob(str(tv.THU_MUC_DU_LIEU / "binance-btcusdt-1h-*" / "*.csv")))
    d = pd.concat([pd.read_csv(t, header=None, usecols=[0, 4]) for t in tep])
    return pd.Series(d[4].to_numpy(float), index=pd.to_datetime(d[0], unit="ms"), name="btc").sort_index()


def doc_jpy() -> pd.Series:
    """Số yên cho 1 USD mỗi ngày giao dịch (H.10, giá lúc trưa New York)."""
    h = pd.read_csv(tv.THU_MUC_DU_LIEU / "frb-h10-ty-gia" / "h10-2000-2024.csv", skiprows=5).set_index("Time Period")
    s = pd.to_numeric(h["RXI_N.B.JA"], errors="coerce").dropna()
    s.index = pd.to_datetime(s.index)
    return s.rename("jpy")


def loi_suat(gia: pd.Series) -> pd.Series:
    """Lợi suất log (%): 100 × (log giá hôm nay − log giá hôm trước)."""
    return (100 * np.log(gia).diff()).dropna()


def btc_ngay() -> tuple[pd.Series, pd.Series, pd.Series]:
    """Giá đóng cửa ngày (UTC), lợi suất ngày (%), biến động thực hiện ngày = tổng bình phương lợi suất giờ (%²)."""
    gio = doc_btc_gio()
    gia = gio.resample("D").last()
    r = loi_suat(gia)
    rv = (loi_suat(gio) ** 2).resample("D").sum().loc[r.index]
    return gia, r, rv


def su_that_cach_dieu(r: pd.Series) -> dict:
    """Đuôi dày, cụm biến động: lợi suất gần như không tự tương quan nhưng bình phương của nó thì có."""
    z = (r - r.mean()) / r.std()
    return {"độ lệch chuẩn %": float(r.std()), "độ nhọn dư": float(stats.kurtosis(r)), "độ lệch": float(stats.skew(r)),
            "ACF1 lợi suất": float(r.autocorr(1)), "ACF1 bình phương": float((r ** 2).autocorr(1)),
            "tỷ lệ |z| > 4 thực": float((z.abs() > 4).mean()), "tỷ lệ |z| > 4 nếu chuẩn": float(2 * stats.norm.sf(4))}


# %% [markdown]
# ## Mổ xẻ demo "đoán giá chính xác 99%"

# %%
def cua_so(gia: pd.Series, W: int = CUA_SO) -> tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]:
    """Mỗi dòng: giá W ngày trước; mục tiêu: giá ngày tiếp theo."""
    p = gia.to_numpy(float)
    X = np.array([p[i - W:i] for i in range(W, len(p))])
    return X, p[W:], gia.index[W:]


def du_bao_gia(gia: pd.Series, moc: str = MOC, seed: int = 0) -> pd.DataFrame:
    """Mạng nơ-ron (MLP) dự báo giá ngày mai từ 10 ngày trước. Chia theo thời gian: học trước `moc`, chấm từ `moc`.
    Mỗi cửa sổ chia cho giá cuối của chính nó — không dùng thông tin nào ngoài cửa sổ."""
    from sklearn.neural_network import MLPRegressor
    X, y, idx = cua_so(gia)
    hoc = idx < pd.Timestamp(moc)
    Xn, yn = X / X[:, -1:], y / X[:, -1]
    mh = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=3000, random_state=seed).fit(Xn[hoc], yn[hoc])
    return pd.DataFrame({"y": y[~hoc], "MLP": mh.predict(Xn[~hoc]) * X[~hoc, -1], "naive": X[~hoc, -1]}, index=idx[~hoc])


def danh_gia_gia(kq: pd.DataFrame) -> dict:
    """So mô hình với naive (giá hôm nay) trên cùng các ngày: R², MAE, DM, tỷ lệ đoán đúng chiều."""
    from sklearn.metrics import r2_score
    e_mh, e_nv = kq["y"] - kq["MLP"], kq["y"] - kq["naive"]
    dm = diebold_mariano(e_mh.to_numpy(), e_nv.to_numpy(), h=1, ham_mat_mat="tuyet_doi")
    dung_chieu = np.sign(kq["MLP"] - kq["naive"]) == np.sign(kq["y"] - kq["naive"])
    return {"R² MLP": r2_score(kq["y"], kq["MLP"]), "R² naive": r2_score(kq["y"], kq["naive"]),
            "MAE MLP": float(e_mh.abs().mean()), "MAE naive": float(e_nv.abs().mean()), "DM p": dm.p_value,
            "đúng chiều": float(dung_chieu.mean())}


# %% [markdown]
# ## Dự báo biến động: GARCH, HAR

# %%
def du_bao_garch(r: pd.Series, moc: str, dist: str = "t", o: int = 0) -> pd.Series:
    """GARCH(1,1) (o = 1: GJR) khớp trên dữ liệu trước `moc`, rồi dự báo phương sai 1 ngày tới cho từng ngày từ `moc`
    với tham số cố định (mỗi ngày chỉ dùng lợi suất tới hôm trước)."""
    from arch import arch_model
    am = arch_model(r, mean="Constant", vol="GARCH", p=1, o=o, q=1, dist=dist)
    kq = am.fit(last_obs=pd.Timestamp(moc), disp="off")
    f = kq.forecast(start=pd.Timestamp(moc), reindex=False)
    return pd.DataFrame({"trung bình": f.mean.iloc[:, 0], "phương sai": f.variance.iloc[:, 0]}).assign(
        nu=float(kq.params.get("nu", np.inf)))


def du_bao_har(rv: pd.Series, moc: str) -> pd.Series:
    """HAR: RV ngày mai ~ RV hôm qua + trung bình 7 ngày + trung bình 30 ngày; học lại mỗi ngày trên mọi ngày trước đó."""
    import statsmodels.api as sm
    X = pd.DataFrame({"ngay": rv.shift(1), "tuan": rv.rolling(7).mean().shift(1), "thang": rv.rolling(30).mean().shift(1)})
    d = pd.concat([rv.rename("rv"), X], axis=1).dropna()
    ra = {}
    for t in d.index[d.index >= pd.Timestamp(moc)]:
        hoc = d[d.index < t]
        b = sm.OLS(hoc["rv"], sm.add_constant(hoc[["ngay", "tuan", "thang"]])).fit().params
        ra[t] = max(float(b.iloc[0] + d.loc[t, ["ngay", "tuan", "thang"]].to_numpy() @ b.iloc[1:].to_numpy()), 1e-3)
    return pd.Series(ra, name="HAR")


def qlike(that: np.ndarray, du_bao: np.ndarray) -> float:
    """Mất mát QLIKE cho dự báo phương sai (nhỏ là tốt): ít bị vài ngày cực lớn chi phối như MSE."""
    t, h = np.asarray(that, float), np.asarray(du_bao, float)
    return float(np.mean(t / h - np.log(t / h) - 1))


# %% [markdown]
# ## Value at Risk và backtest Kupiec

# %%
def var_99(r: pd.Series, moc: str = MOC_JPY) -> pd.Series:
    """VaR 99% một ngày (%, số âm: mức lỗ mà chỉ 1% số ngày tệ hơn): GARCH(1,1) với phân phối Student-t."""
    g = du_bao_garch(r, moc, dist="t")
    nu = g["nu"].iloc[0]
    q = stats.t.ppf(MUC_VAR, nu) * np.sqrt((nu - 2) / nu)   # quantile 1% của Student-t đã chuẩn hoá phương sai 1
    return (g["trung bình"] + q * np.sqrt(g["phương sai"])).rename("VaR")


def kupiec(r: pd.Series, var: pd.Series, p: float = MUC_VAR) -> dict:
    """Kiểm định Kupiec: số ngày lỗ vượt VaR có khớp tỷ lệ p không. p-value nhỏ là VaR sai."""
    vuot = (r.loc[var.index] < var).to_numpy()
    n, x = len(vuot), int(vuot.sum())
    ph = x / n
    ll0 = (n - x) * np.log(1 - p) + x * np.log(p)
    ll1 = (n - x) * np.log(1 - ph) + (x * np.log(ph) if x > 0 else 0.0) if x < n else 0.0
    lr = -2 * (ll0 - ll1)
    return {"số ngày": n, "số lần vượt": x, "kỳ vọng": n * p, "LR": float(lr), "p": float(stats.chi2.sf(lr, 1))}


# %% [markdown]
# ## Markov switching: bình thường và bất ổn

# %%
def markov_2_trang_thai(r: pd.Series) -> pd.Series:
    """Hai trạng thái khác nhau ở phương sai; trả xác suất (đã làm trơn) của trạng thái biến động cao mỗi ngày."""
    import statsmodels.api as sm
    kq = sm.tsa.MarkovRegression(r.reset_index(drop=True), k_regimes=2, switching_variance=True).fit()
    cao = int(np.argmax([kq.params["sigma2[0]"], kq.params["sigma2[1]"]]))
    p = kq.smoothed_marginal_probabilities[cao]
    p.index = r.index
    return p.rename("xác suất bất ổn")


# %%
if __name__ == "__main__":
    gia, r, rv = btc_ngay()
    jpy = loi_suat(doc_jpy())
    print("BTC:", {k: round(v, 4) for k, v in su_that_cach_dieu(r).items()})
    print("JPY:", {k: round(v, 4) for k, v in su_that_cach_dieu(jpy).items()})
    print("demo:", danh_gia_gia(du_bao_gia(gia)))
    var = var_99(jpy)
    print("Kupiec VaR:", kupiec(jpy, var))
    har = du_bao_har(rv, MOC)
    g = du_bao_garch(r, MOC)["phương sai"].reindex(har.index)
    y = rv.loc[har.index]
    print("QLIKE HAR", qlike(y, har), "GARCH", qlike(y, g), "cố định", qlike(y, np.full(len(y), r[r.index < MOC].var())))
