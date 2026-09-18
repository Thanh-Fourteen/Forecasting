# %% [markdown]
# # Buổi 8 — Tương quan giữa các chuỗi: giả, phi tuyến, độ trễ dẫn dắt, và Granger
#
# Dữ liệu: tải điện ERCOT theo giờ (EIA-930), nhiệt độ Dallas + Houston (Open-Meteo ERA5),
# CPI-U (BLS) và dân số Mỹ (BEA).

# %%
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_selection import mutual_info_regression
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import grangercausalitytests

import tv

MOC_DO = 18.33  # 65 °F — mốc chuẩn của EIA cho degree day


# %% [markdown]
# ## Dữ liệu

# %%
def doc_tai_dien(vung: str = "ERCO") -> pd.Series:
    """Tải điện theo giờ UTC (mốc cuối giờ), MW."""
    tep = [tv.THU_MUC_DU_LIEU / "eia930-balance-2024-h1" / "EIA930_BALANCE_2024_Jan_Jun.csv",
           tv.THU_MUC_DU_LIEU / "eia930-balance-2024-h2" / "EIA930_BALANCE_2024_Jul_Dec.csv"]
    cot = ["Balancing Authority", "UTC Time at End of Hour", "Demand (MW)"]
    df = pd.concat([pd.read_csv(t, usecols=cot, thousands=",") for t in tep])
    df = df[df["Balancing Authority"] == vung]
    ds = pd.to_datetime(df["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p")
    return pd.Series(df["Demand (MW)"].to_numpy(dtype=float), index=ds, name="tai").sort_index().asfreq("h")


def doc_nhiet_do() -> pd.Series:
    """Trung bình nhiệt độ 2 m của Dallas và Houston theo giờ UTC (°C); 3 dòng đầu tệp là metadata."""
    phan = []
    for thanh_pho in ("dallas", "houston"):
        thu_muc = tv.THU_MUC_DU_LIEU / f"open-meteo-{thanh_pho}-2024"
        df = pd.read_csv(thu_muc / f"open-meteo-{thanh_pho}-2024-utc.csv", skiprows=4, names=["time", "nhiet"])
        phan.append(pd.Series(df["nhiet"].to_numpy(dtype=float), index=pd.to_datetime(df["time"])).asfreq("h"))
    return pd.concat(phan, axis=1, sort=False).mean(axis=1).rename("nhiet")


def ghep_tai_nhiet(vung: str = "ERCO") -> pd.DataFrame:
    """Ghép theo mốc UTC; thêm CDD/HDD. Nhiệt độ ERA5 là giá trị tức thời tại mốc, tải điện là tích phân của giờ
    kết thúc tại mốc — chênh lệch nửa giờ này nhỏ so với nhịp ngày, nhưng phải biết khi đọc CCF ở trễ 0–1."""
    df = pd.concat([doc_tai_dien(vung), doc_nhiet_do()], axis=1, sort=False).dropna()
    df["cdd"], df["hdd"] = cdd_hdd(df["nhiet"])
    return df


def doc_kinh_te() -> pd.DataFrame:
    """CPI-U (BLS, 1982–84 = 100) và dân số Mỹ giữa kỳ (BEA, nghìn người), theo tháng 1990–2024."""
    cpi_tho = pd.read_csv(tv.THU_MUC_DU_LIEU / "bls-cpi-u" / "cu.data.1.AllItems.tsv", sep="\t", dtype=str)
    cpi_tho.columns = cpi_tho.columns.str.strip()
    c = cpi_tho[(cpi_tho["series_id"].str.strip() == "CUUR0000SA0") & (cpi_tho["period"] != "M13")]
    cpi = pd.Series(pd.to_numeric(c["value"].str.strip(), errors="coerce").to_numpy(),
                    index=pd.to_datetime(c["year"].str.strip() + "-" + c["period"].str[1:] + "-01")).sort_index()
    ds = pd.read_csv(tv.THU_MUC_DU_LIEU / "bea-nipa-thang" / "NipaDataM.txt", thousands=",")
    ds = ds[ds["%SeriesCode"] == "B230RC"]
    dan_so = pd.Series(ds["Value"].astype(float).to_numpy(),
                       index=pd.to_datetime(ds["Period"].str.replace("M", "-") + "-01")).sort_index()
    return pd.DataFrame({"cpi": cpi, "dan_so": dan_so}).dropna()["1990":"2024"].asfreq("MS")


def cdd_hdd(nhiet, moc: float = MOC_DO):
    """Độ nóng (cooling degree) và độ lạnh (heating degree) so với mốc 18,33 °C = 65 °F."""
    nhiet = np.asarray(nhiet, dtype=float)
    return np.maximum(nhiet - moc, 0.0), np.maximum(moc - nhiet, 0.0)


# %% [markdown]
# ## 1. Tương quan tuyến tính, hạng, và phi tuyến

# %%
def tuong_quan(x, y) -> dict[str, float]:
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    return {"pearson": float(stats.pearsonr(x, y)[0]), "spearman": float(stats.spearmanr(x, y)[0]),
            "kendall": float(stats.kendalltau(x, y)[0])}


def thong_tin_tuong_ho(x, y, seed: int = 0) -> float:
    """Mutual information (nat) bằng ước lượng k-láng giềng của scikit-learn (Kraskov 2004, Ross 2014)."""
    x = np.asarray(x, dtype=float).reshape(-1, 1)
    return float(mutual_info_regression(x, np.asarray(y, dtype=float), random_state=seed)[0])


def kiem_y_nghia_mi(x, y, do_dai_khoi: int = 168, so_lan: int = 200, seed: int = 0) -> dict[str, float]:
    """p-value cho MI bằng hoán vị THEO KHỐI — hoán vị từng điểm phá tự tương quan và cho dương tính giả."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rng = np.random.default_rng(seed)
    that = thong_tin_tuong_ho(x, y, seed)
    khoi = [y[i:i + do_dai_khoi] for i in range(0, y.size, do_dai_khoi)]
    gia = []
    for _ in range(so_lan):
        thu_tu = rng.permutation(len(khoi))
        gia.append(thong_tin_tuong_ho(x, np.concatenate([khoi[i] for i in thu_tu])[: x.size], seed))
    gia = np.array(gia)
    return {"mi": that, "p": float((np.sum(gia >= that) + 1) / (so_lan + 1)), "nguong_95": float(np.quantile(gia, 0.95))}


# %% [markdown]
# ## 2. Tương quan giả giữa hai chuỗi có xu hướng

# %%
def hoi_quy_don(x, y) -> dict[str, float]:
    """OLS y = a + b·x; trả R², t của b, và Durbin–Watson của phần dư."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    X = np.column_stack([np.ones(x.size), x])
    he_so = np.linalg.lstsq(X, y, rcond=None)[0]
    du = y - X @ he_so
    s2 = du @ du / (x.size - 2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    return {"r2": float(1 - du.var() / y.var()), "t": float(he_so[1] / se),
            "dw": float(np.sum(np.diff(du) ** 2) / np.sum(du**2))}


def tuong_quan_chuoi(a: pd.Series, b: pd.Series) -> dict[str, float | str]:
    """Tương quan giữa hai chuỗi."""
    a, b = a.dropna(), b.dropna()
    chung = a.index.intersection(b.index)
    a, b = a[chung], b[chung]
    r = float(a.corr(b))
    return {"r_muc": r, "ket_luan": "quan hệ mạnh" if abs(r) > 0.7 else "quan hệ yếu"}


# %% [markdown]
# ## 3. CCF và prewhitening

# %%
def ccf_tu_viet(x, y, so_tre: int) -> np.ndarray:
    """r_k = corr(x_t, y_{t+k}) với k = 0..so_tre — "x đi trước y k bước".

    Lưu ý: `statsmodels.tsa.stattools.ccf(a, b)` trả corr(a_{t+k}, b_t), tức muốn "x dẫn y" phải gọi ccf(y, x).
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    x = (x - x.mean()) / x.std()
    y = (y - y.mean()) / y.std()
    n = x.size
    return np.array([float(np.sum(x[: n - k] * y[k:]) / n) for k in range(so_tre + 1)])


def loc_prewhiten(x, y, bac: int = 48) -> tuple[np.ndarray, np.ndarray]:
    """Khớp AR(bac) cho x rồi lọc CẢ HAI chuỗi bằng cùng bộ hệ số (Box–Jenkins)."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    phi = AutoReg(x, lags=bac).fit().params[1:]

    def loc(v):
        return np.array([v[i] - np.dot(phi[::-1], v[i - bac:i]) for i in range(bac, v.size)])

    return loc(x), loc(y)


def do_tre_dan_dat(x, y, so_tre: int = 12, bac: int | None = 48) -> dict[str, float]:
    """Độ trễ mà x dẫn y: lấy đỉnh của CCF."""
    a, b = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    r = ccf_tu_viet(a, b, so_tre)
    return {"tre": int(np.argmax(np.abs(r))), "r_dinh": float(r[np.argmax(np.abs(r))]),
            "dai": float(2 / np.sqrt(len(a))), "ccf": r}


def tuong_quan_truot(x: pd.Series, y: pd.Series, cua_so: int = 90) -> pd.Series:
    """Tương quan trượt; `min_periods` = cả cửa sổ để không có giá trị ±1 giả ở đầu chuỗi."""
    return x.rolling(cua_so, min_periods=cua_so).corr(y)


# %% [markdown]
# ## 4. Granger

# %%
def granger_hai_chieu(x: pd.Series, y: pd.Series, so_tre: int = 4) -> dict[str, object]:
    """Kiểm định Granger hai chiều. statsmodels kiểm "cột 2 gây ra cột 1" nên phải xếp cột cẩn thận."""
    du_lieu = pd.concat([x, y], axis=1, sort=False).dropna()
    a, b = du_lieu.iloc[:, 0].to_numpy(), du_lieu.iloc[:, 1].to_numpy()
    p_xy = min(grangercausalitytests(np.column_stack([b, a]), maxlag=so_tre)[k][0]["ssr_ftest"][1]
               for k in range(1, so_tre + 1))
    p_yx = min(grangercausalitytests(np.column_stack([a, b]), maxlag=so_tre)[k][0]["ssr_ftest"][1]
               for k in range(1, so_tre + 1))
    if p_xy < 0.05:
        ket_luan = "x gây ra y (Granger, p < 0,05)"
    elif p_yx < 0.05:
        ket_luan = "y gây ra x (Granger, p < 0,05)"
    else:
        ket_luan = "không chiều nào có ý nghĩa"
    return {"p_x_giup_du_bao_y": float(p_xy), "p_y_giup_du_bao_x": float(p_yx), "ket_luan": ket_luan}


# %%
if __name__ == "__main__":
    kt = doc_kinh_te()
    print("1. CPI × dân số:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in
                               tuong_quan_chuoi(kt["cpi"], kt["dan_so"]).items()})
    df = ghep_tai_nhiet()
    print("2. tải × nhiệt độ:", {k: round(v, 3) for k, v in tuong_quan(df["nhiet"], df["tai"]).items()},
          "MI =", round(thong_tin_tuong_ho(df["nhiet"], df["tai"]), 3))
    print("3. độ trễ dẫn dắt (thô):", do_tre_dan_dat(df["cdd"], df["tai"], bac=None)["tre"],
          "| sau prewhitening:", do_tre_dan_dat(df["cdd"], df["tai"])["tre"])
    ngay = df.resample("D").mean()
    r = tuong_quan_truot(ngay["nhiet"], ngay["tai"])
    print("4. tương quan trượt 90 ngày: min", round(r.min(), 3), "max", round(r.max(), 3))
    print("5.", granger_hai_chieu(pd.Series(df["cdd"].to_numpy(), index=df.index), df["tai"])["ket_luan"])
