# %% [markdown]
# # Buổi 20 — Đa biến, state space và nowcasting (ĐÁP ÁN)
#
# Dữ liệu: giá dầu WTI và giá xăng New York Harbor theo ngày (EIA); GDP thực, việc làm, sản lượng công nghiệp, nhà khởi công
# Mỹ theo từng VINTAGE (Philadelphia Fed Real-Time Data Set); lưu lượng sông Nile (có sẵn trong statsmodels).

# %%
from __future__ import annotations

import hashlib
import warnings

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

VINTAGE_CUOI = "25M12"      # buổi chỉ dùng vintage tới 12/2025 (tệp nguồn thêm một cột mỗi tháng)
CHI_BAO = {"e": ("philly-fed-viec-lam-vintage", "employMvMd.xlsx", "EMPLOY"),
           "ip": ("philly-fed-san-luong-cn-vintage", "iptMvMd.xlsx", "IPT"),
           "hs": ("philly-fed-nha-khoi-cong-vintage", "hstartsMvMd.xlsx", "HSTARTS")}
GDP = ("philly-fed-gdp-thuc-vintage-thang", "routputMvQd.xlsx", "ROUTPUT")
DUNG_CHI_BAO = ("e", "ip")  # việc làm + sản lượng công nghiệp
BO_COVID = (pd.Period("2020Q1"), pd.Period("2021Q2"))


# %% [markdown]
# ## 1. Giá dầu và giá xăng: VAR, cointegration, VECM

# %%
def _doc_eia(ten: str, tep: str) -> pd.Series:
    d = pd.read_excel(tv.THU_MUC_DU_LIEU / ten / tep, sheet_name="Data 1", skiprows=2)
    return pd.Series(d.iloc[:, 1].to_numpy(float), index=pd.to_datetime(d.iloc[:, 0]))


def doc_dau_xang(tu: str = "2010", den: str = "2019") -> pd.DataFrame:
    """Log giá theo tuần (trung bình tuần, USD/gallon): dầu WTI (chia 42 gallon/thùng) và xăng New York Harbor."""
    dau = _doc_eia("eia-gia-dau-wti", "RWTCd.xls") / 42
    xang = _doc_eia("eia-gia-xang-ny-harbor", "EER_EPMRU_PF4_Y35NY_DPGd.xls")
    d = pd.DataFrame({"dau": dau, "xang": xang})[tu:den].resample("W-FRI").mean().dropna()
    return np.log(d[(d > 0).all(axis=1)])


def kiem_dung(L: pd.DataFrame) -> pd.DataFrame:
    """ADF (H0: không dừng) và KPSS (H0: dừng) trên mức và trên sai phân."""
    from statsmodels.tsa.stattools import adfuller, kpss
    hang = []
    for c in L:
        for ten, s in (("mức", L[c]), ("sai phân", L[c].diff().dropna())):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")      # KPSS báo p nằm ngoài bảng tra: p thật còn nhỏ/lớn hơn số in ra
                hang.append({"chuỗi": c, "dạng": ten, "ADF p": adfuller(s)[1], "KPSS p": kpss(s, nlags="auto")[1]})
    return pd.DataFrame(hang)


def engle_granger(L: pd.DataFrame) -> dict:
    """Bước 1: hồi quy xang ~ dau trên mức; bước 2: phần dư (spread) có dừng không. Kèm thời gian bán rã của spread."""
    import statsmodels.api as sm
    from statsmodels.tsa.stattools import coint
    kq = sm.OLS(L["xang"], sm.add_constant(L["dau"])).fit()
    s = kq.resid.to_numpy()
    rho = np.corrcoef(s[1:], s[:-1])[0, 1]
    return {"hệ số": float(kq.params["dau"]), "hằng số": float(kq.params["const"]),
            "p Engle–Granger": float(coint(L["xang"], L["dau"])[1]), "bán rã (tuần)": float(-np.log(2) / np.log(rho))}


def hang_dong_lien_ket(L: pd.DataFrame, k_ar_diff: int = 2) -> int:
    """Số quan hệ cointegration theo kiểm định Johansen (trace, 5%)."""
    from statsmodels.tsa.vector_ar.vecm import select_coint_rank
    return int(select_coint_rank(L, det_order=0, k_ar_diff=k_ar_diff).rank)


def du_bao_xang(lich_su: pd.DataFrame, h: int, hang: int, k_ar_diff: int = 2) -> tuple[str, np.ndarray]:
    """Dự báo log giá xăng h tuần tới: VECM nếu có cointegration, VAR trên sai phân nếu không."""
    if hang > 0:
        from statsmodels.tsa.vector_ar.vecm import VECM
        mh = VECM(lich_su, k_ar_diff=k_ar_diff, coint_rank=hang, deterministic="ci").fit()
        return "VECM", mh.predict(h)[:, 1]
    from statsmodels.tsa.api import VAR
    d = lich_su.diff().dropna()
    f = VAR(d).fit(k_ar_diff).forecast(d.to_numpy()[-k_ar_diff:], h)
    return "VAR sai phân", lich_su["xang"].iloc[-1] + np.cumsum(f[:, 1])


def backtest_dau_xang(L: pd.DataFrame, so_tuan: int = 104, h: int = 4) -> pd.DataFrame:
    """Rolling origin mỗi tuần trên 2 năm cuối: sai số tuyệt đối (%, trên log) theo bước h của naive, VAR sai phân, VECM."""
    from statsmodels.tsa.api import VAR
    from statsmodels.tsa.vector_ar.vecm import VECM
    n = len(L)
    hang = []
    for c in range(n - so_tuan - h, n - h):
        ls, that = L.iloc[:c + 1], L["xang"].to_numpy()[c + 1:c + 1 + h]
        d = ls.diff().dropna()
        var = ls["xang"].iloc[-1] + np.cumsum(VAR(d).fit(2).forecast(d.to_numpy()[-2:], h)[:, 1])
        vecm = VECM(ls, k_ar_diff=2, coint_rank=1, deterministic="ci").fit().predict(h)[:, 1]
        for b in range(h):
            hang.append({"cutoff": L.index[c], "buoc_h": b + 1, "y": that[b], "naive": ls["xang"].iloc[-1],
                         "VAR": var[b], "VECM": vecm[b]})
    return pd.DataFrame(hang)


# %% [markdown]
# ## 2. State space: bộ lọc Kalman cho local level

# %%
def doc_nile() -> np.ndarray:
    """Lưu lượng sông Nile mỗi năm 1871–1970 (10⁸ m³), dữ liệu public domain có sẵn trong statsmodels."""
    from statsmodels.datasets import nile
    return nile.load_pandas().data["volume"].to_numpy(float)


def kalman_local_level(y: np.ndarray, s2_nhieu: float, s2_muc: float, a0: float = 0.0, p0: float = 1e6) -> dict:
    """y_t = mức_t + nhiễu (phương sai s2_nhieu); mức_t = mức_{t−1} + cú dời (phương sai s2_muc).
    Mỗi bước: DỰ BÁO (mức giữ nguyên, bất định cộng s2_muc) rồi CẬP NHẬT bằng số đo (nếu có)."""
    a, p = a0, p0
    muc, bat_dinh, du_bao = [], [], []
    for v in np.asarray(y, float):
        p = p + s2_muc                        # dự báo: mức như cũ, bất định lớn thêm
        du_bao.append(a)
        if not np.isnan(v):                   # cập nhật: kéo mức về phía số đo theo hệ số K
            K = p / (p + s2_nhieu)
            a = a + K * (v - a)
            p = (1 - K) * p
        muc.append(a)
        bat_dinh.append(p)
    return {"mức": np.array(muc), "phương sai": np.array(bat_dinh), "dự báo 1 bước": np.array(du_bao)}


def local_level_statsmodels(y: np.ndarray):
    import statsmodels.api as sm
    return sm.tsa.UnobservedComponents(y, "local level").fit(disp=False)


# %% [markdown]
# ## 3. Dữ liệu vintage, dynamic factor, nowcasting GDP

# %%
def _nam_thang(v: str) -> tuple[int, int]:
    yy = int(v[:2])
    return (1900 if yy >= 60 else 2000) + yy, int(v[3:])


def ten_vintage(nam: int, thang: int) -> str:
    return f"{nam % 100:02d}M{thang}"


def doc_vintage(ten: str, tep: str, tien_to: str) -> pd.DataFrame:
    """Bảng: mỗi dòng một kỳ số liệu, mỗi cột một vintage 'yyMm' (số liệu có vào giữa tháng đó). Cắt tới VINTAGE_CUOI;
    lưu bản cắt vào du-lieu/cache/ (đọc xlsx lần đầu mất ~5 giây mỗi tệp)."""
    tep_cache = tv.THU_MUC_DU_LIEU.parent / "cache" / f"{ten}-{VINTAGE_CUOI}.parquet"
    if tep_cache.exists():
        return pd.read_parquet(tep_cache)
    d = pd.read_excel(tv.THU_MUC_DU_LIEU / ten / tep).set_index("DATE")
    d.columns = [c.replace(tien_to, "") for c in d.columns]
    d = d[[c for c in d.columns if _nam_thang(c) <= _nam_thang(VINTAGE_CUOI)]].dropna(how="all")
    d.index = d.index.astype(str)
    tep_cache.parent.mkdir(parents=True, exist_ok=True)
    d.to_parquet(tep_cache)
    return d


def doc_tat_ca() -> dict[str, pd.DataFrame]:
    return {"gdp": doc_vintage(*GDP), **{k: doc_vintage(*v) for k, v in CHI_BAO.items()}}


def dau_van_tay(d: pd.DataFrame) -> str:
    """sha256 của bảng đã cắt — bộ chấm dùng để chắc mọi học viên có đúng cùng số liệu."""
    return hashlib.sha256(d.round(3).to_csv().encode()).hexdigest()


def gdp_theo_vintage(du_lieu: dict, v: str) -> pd.Series:
    """GDP thực (tỷ USD 2017) theo quý, như được biết ở vintage v."""
    g = du_lieu["gdp"][v]
    return pd.Series(g.to_numpy(), index=pd.PeriodIndex(g.index.str.replace(":", ""), freq="Q")).dropna()


def chi_bao_theo_vintage(du_lieu: dict, c: str, v: str) -> pd.Series:
    s = du_lieu[c][v]
    return pd.Series(s.to_numpy(), index=pd.PeriodIndex(s.index.str.replace(":", "-"), freq="M")).dropna()


def tang_truong_quy(G: pd.Series) -> pd.Series:
    """Tăng trưởng quý so quý trước, quy ra năm (%): 400 × Δlog."""
    return 400 * np.log(G).diff().dropna()


def vintage_cua(q: pd.Period, k: int) -> str:
    """Vintage giữa tháng thứ k tính từ đầu quý q (k = 1: tháng đầu quý; k = 4: tháng đầu quý sau)."""
    m = q.asfreq("M", "s") + (k - 1)
    return ten_vintage(m.year, m.month)


def gdp_lan_dau(du_lieu: dict, q: pd.Period) -> float:
    """Tăng trưởng quý q theo lần công bố đầu tiên (vintage đầu tiên có quý q)."""
    for k in range(4, 8):
        G = gdp_theo_vintage(du_lieu, vintage_cua(q, k))
        if q in G.index:
            return float(tang_truong_quy(G).loc[q])
    raise ValueError(f"chưa có GDP {q}")


def _chi_bao_quy(s: pd.Series, q: pd.Period) -> pd.Series:
    """Tăng trưởng quý (400 × Δlog trung bình 3 tháng) của một chỉ báo tháng. Tháng còn thiếu của quý q (ragged edge)
    được lấp bằng dự báo AR(1) của tăng trưởng tháng."""
    ls = np.log(s)
    d = ls.diff().dropna()["1990":]
    mu, phi = d.mean(), np.corrcoef(d.to_numpy()[1:], d.to_numpy()[:-1])[0, 1]
    them, muc, buoc, p = {}, ls.iloc[-1], d.iloc[-1], ls.index[-1]
    while p < q.asfreq("M", "e"):
        p, buoc = p + 1, mu + phi * (buoc - mu)
        muc += buoc
        them[p] = muc
    ls = pd.concat([ls, pd.Series(them, dtype=float)]).astype(float)
    tb = np.exp(ls).groupby(ls.index.asfreq("Q")).mean()
    return 400 * np.log(tb).diff()


def nowcast(du_lieu: dict, q: pd.Period, k: int, chi_bao=DUNG_CHI_BAO) -> dict:
    """Bridge equation: tăng trưởng GDP ~ tăng trưởng quý của chỉ báo tháng, học trên các quý đã công bố (1990 trở đi,
    bỏ quý COVID). Mọi số liệu lấy từ vintage giữa tháng thứ k của quý q — đúng những gì có lúc đó."""
    v = vintage_cua(q, k)
    gy = tang_truong_quy(gdp_theo_vintage(du_lieu, v))
    X = pd.DataFrame({c: _chi_bao_quy(chi_bao_theo_vintage(du_lieu, c, v), q) for c in chi_bao})
    hoc = [p for p in gy.index if p >= pd.Period("1990Q1") and not (BO_COVID[0] <= p <= BO_COVID[1]) and p in X.index]
    A = np.c_[np.ones(len(hoc)), X.loc[hoc].to_numpy()]
    he_so = np.linalg.lstsq(A, gy.loc[hoc].to_numpy(), rcond=None)[0]
    return {"vintage": v, "bridge": float(np.r_[1, X.loc[q].to_numpy()] @ he_so),
            "naive": float(gy.iloc[-1]), "trung bình": float(gy.loc[hoc].mean())}


def nowcast_dfm(du_lieu: dict, q: pd.Period, k: int, chi_bao=DUNG_CHI_BAO) -> float:
    """Dynamic factor model tần suất hỗn hợp (DynamicFactorMQ): một nhân tố chung cho chỉ báo tháng và GDP quý."""
    from statsmodels.tsa.statespace.dynamic_factor_mq import DynamicFactorMQ
    v = vintage_cua(q, k)
    thang = pd.DataFrame({c: 100 * np.log(chi_bao_theo_vintage(du_lieu, c, v)).diff() for c in chi_bao})["1990-01":]
    thang = thang.reindex(pd.period_range(thang.index[0], q.asfreq("M", "e"), freq="M"))
    G = gdp_theo_vintage(du_lieu, v)
    quy = pd.DataFrame({"gdp": 100 * np.log(G).diff()})["1990Q1":]
    quy = quy[quy.index < q]
    kq = DynamicFactorMQ(thang, endog_quarterly=quy, factors=1, factor_orders=1,
                         idiosyncratic_ar1=False).fit(disp=False, maxiter=500)
    thang_cuoi = q.asfreq("M", "e")
    return 4 * float(kq.predict(start=thang_cuoi, end=thang_cuoi)["gdp"].iloc[0])


def danh_gia_nowcast(du_lieu: dict, cac_quy, dfm: bool = False) -> pd.DataFrame:
    """Sai số nowcast (điểm %, năm hoá) so với lần công bố đầu, theo số tháng thông tin k = 1..4."""
    hang = []
    for q in cac_quy:
        that = gdp_lan_dau(du_lieu, q)
        for k in (1, 2, 3, 4):
            n = nowcast(du_lieu, q, k)
            dong = {"quý": str(q), "k": k, "thật": that, **{m: n[m] for m in ("bridge", "naive", "trung bình")}}
            if dfm:
                dong["DFM"] = nowcast_dfm(du_lieu, q, k)
            hang.append(dong)
    return pd.DataFrame(hang)


def rmse_theo_k(bang: pd.DataFrame) -> pd.DataFrame:
    cot = [c for c in ("bridge", "DFM", "naive", "trung bình") if c in bang]
    return bang.groupby("k").apply(lambda d: pd.Series({c: np.sqrt(np.mean((d[c] - d["thật"]) ** 2)) for c in cot}))


# %%
if __name__ == "__main__":
    L = doc_dau_xang()
    print(kiem_dung(L).round(3).to_string(index=False))
    print(engle_granger(L), "Johansen:", hang_dong_lien_ket(L))
    y = doc_nile()
    kq = kalman_local_level(y, 15099.0, 1469.1)
    print(kq["mức"][:3].round(1))
    du_lieu = doc_tat_ca()
    print({k: dau_van_tay(v)[:12] for k, v in du_lieu.items()})
    bang = danh_gia_nowcast(du_lieu, pd.period_range("2005Q1", "2019Q4", freq="Q"))
    print(rmse_theo_k(bang).round(2))
