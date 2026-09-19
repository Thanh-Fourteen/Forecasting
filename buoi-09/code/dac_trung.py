# %% [markdown]
# # Buổi 9 — Đặc trưng chuỗi và khả năng dự báo
#
# Dữ liệu: 48.000 chuỗi M4 theo tháng (Monash), doanh số bán lẻ UCI Online Retail II.

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import signal, stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import kpss

import tv

M = 12  # chu kỳ mùa vụ của dữ liệu tháng
TAM = 18  # tầm dự báo của M4 monthly
DAI = 120  # cắt mọi chuỗi về cùng 120 điểm cuối: độ dài gốc 60–2.812 làm đặc trưng lệch


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_tsf(tep=None) -> dict[str, np.ndarray]:
    """Đọc tệp .tsf của Monash bằng thư viện chuẩn: dòng `@` là siêu dữ liệu, sau `@data` mỗi dòng là
    `tên:mốc_bắt_đầu:v1,v2,…`."""
    tep = tep or tv.THU_MUC_DU_LIEU / "monash-m4-monthly" / "m4_monthly_dataset.tsf"
    chuoi: dict[str, np.ndarray] = {}
    trong_data = False
    with open(tep, encoding="utf-8", errors="ignore") as f:
        for dong in f:
            if not trong_data:
                trong_data = dong.strip().lower() == "@data"
                continue
            if not dong.strip():
                continue
            ten, _, gia_tri = dong.strip().split(":", 2)
            chuoi[ten] = np.fromstring(gia_tri, sep=",")
    return chuoi


def lay_mau(chuoi: dict[str, np.ndarray], so_chuoi: int = 4000, dai: int = DAI, seed: int = 42) -> dict[str, np.ndarray]:
    """Lấy mẫu ngẫu nhiên các chuỗi đủ dài, rồi CẮT VỀ CÙNG ĐỘ DÀI (đuôi) để đặc trưng so sánh được."""
    rng = np.random.default_rng(seed)
    du_dai = [t for t, v in chuoi.items() if v.size >= dai + TAM]
    chon = rng.choice(np.array(du_dai), size=min(so_chuoi, len(du_dai)), replace=False)
    return {t: chuoi[t][-(dai + TAM):] for t in chon}


def doc_ban_le() -> pd.DataFrame:
    """Online Retail II → doanh thu theo (mã hàng, tháng). Đọc .xlsx mất ~30 s nên cache sang parquet."""
    cache = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "ban_le_thang.parquet"
    if cache.exists():
        return pd.read_parquet(cache)
    tep = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "online_retail_II.xlsx"
    phan = [pd.read_excel(tep, sheet_name=ten) for ten in ("Year 2009-2010", "Year 2010-2011")]
    df = pd.concat(phan, ignore_index=True)
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]  # bỏ hoá đơn huỷ (Invoice bắt đầu bằng C)
    df["doanh_thu"] = df["Quantity"] * df["Price"]
    df["thang"] = pd.to_datetime(df["InvoiceDate"]).dt.to_period("M").dt.to_timestamp()
    df["StockCode"] = df["StockCode"].astype(str)
    bang = df.groupby(["StockCode", "thang"], as_index=False)["doanh_thu"].sum()
    bang.to_parquet(cache)
    return bang


# %% [markdown]
# ## Hai mươi đặc trưng — tự viết

# %%
def entropy_pho(y, nperseg: int | None = None) -> float:
    """Spectral entropy chuẩn hoá ∈ [0,1]: 0 = chu kỳ rõ (dễ dự báo), 1 = nhiễu trắng.

    Bỏ bin tần số 0 (mức trung bình) rồi chuẩn hoá phổ thành phân phối xác suất và chia cho log(số bin).
    """
    y = np.asarray(y, dtype=float)
    _, P = signal.welch(y - y.mean(), fs=1.0, nperseg=min(nperseg or 256, y.size))
    P = P[1:]
    if P.sum() <= 0:
        return 0.0
    p = P / P.sum()
    return float(-np.sum(p * np.log(p + 1e-300)) / np.log(p.size))


def _acf(y, tre: int) -> float:
    y = np.asarray(y, dtype=float)
    lech = y - y.mean()
    mau = np.sum(lech**2)
    return float(np.sum(lech[tre:] * lech[:-tre]) / mau) if mau > 0 and tre < y.size else 0.0


def _kpss_p(y) -> float:
    """p-value của KPSS; chuỗi hằng làm kpss vỡ (`cannot convert float NaN to integer`) → trả NaN."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # p bị cắt ở 0,01/0,1 — buổi 7 đã bàn
        try:
            return float(kpss(y, regression="c", nlags="auto", result_object=True).pvalue)
        except (ValueError, OverflowError):
            return float("nan")


def dac_trung_mot_chuoi(y, m: int = M) -> dict[str, float]:
    """20 đặc trưng cho một chuỗi. Tất cả đều KHÔNG phụ thuộc đơn vị đo, trừ hai đặc trưng quy mô đầu.

    STL chạy trên chuỗi đã chuẩn hoá z-score (như FPP/tsfeatures): nếu không, spike, độ dốc, độ cong đổi theo đơn vị đo.
    """
    y = np.asarray(y, dtype=float)
    d1 = np.diff(y)
    sd = np.std(y)
    z = (y - np.mean(y)) / sd if sd > 0 else y - np.mean(y)
    kq = STL(pd.Series(z, index=pd.period_range("2000-01", periods=y.size, freq="M").to_timestamp()),
             period=m, robust=False).fit()
    r, t, s = kq.resid.to_numpy(), kq.trend.to_numpy(), kq.seasonal.to_numpy()
    var_r = np.var(r)
    xu_huong = np.polyfit(np.arange(y.size), t, 2)
    return {
        "trung_binh": float(np.mean(y)),
        "do_lech_chuan": float(np.std(y, ddof=1)),
        "he_so_bien_thien": float(np.std(y, ddof=1) / np.mean(y)) if np.mean(y) != 0 else np.nan,
        "he_so_lech": float(stats.skew(y)),
        "do_nhon": float(stats.kurtosis(y)),
        "acf1": _acf(y, 1),
        "acf10": float(np.sum([_acf(y, k) ** 2 for k in range(1, 11)])),
        "acf_mua_vu": _acf(y, m),
        "diff1_acf1": _acf(d1, 1),
        "entropy_pho": entropy_pho(y),
        "do_manh_xu_huong": float(max(0.0, 1 - var_r / np.var(t + r))),
        "do_manh_mua_vu": float(max(0.0, 1 - var_r / np.var(s + r))),
        "spike": float(np.var([np.var(np.delete(r, i)) for i in range(0, r.size, max(1, r.size // 50))])),
        "do_doc_xu_huong": float(xu_huong[1]),
        "do_cong_xu_huong": float(xu_huong[0]),
        "ty_le_0": float(np.mean(y == 0)),
        "so_lan_cat_trung_binh": float(np.sum(np.diff((y > np.mean(y)).astype(int)) != 0)),
        "doan_phang": float(np.max(np.bincount(np.digitize(y, np.histogram_bin_edges(y, bins=10)[1:-1])))) / y.size,
        "bat_on_dinh": float(np.var([np.mean(c) for c in np.array_split(y, 10)])) / (np.var(y) + 1e-12),
        "kpss_p": _kpss_p(y),
    }


def bang_dac_trung(chuoi: dict[str, np.ndarray], m: int = M) -> pd.DataFrame:
    """Đặc trưng tính trên phần HUẤN LUYỆN (bỏ TAM điểm cuối dành để chấm)."""
    return pd.DataFrame({t: dac_trung_mot_chuoi(v[:-TAM], m) for t, v in chuoi.items()}).T


# %% [markdown]
# ## Khả năng dự báo: entropy so với sai số THẬT

# %%
def du_bao_mua_vu(y_hoc, tam: int = TAM, m: int = M) -> np.ndarray:
    """Seasonal naive: lặp lại m giá trị cuối."""
    y_hoc = np.asarray(y_hoc, dtype=float)
    return np.resize(y_hoc[-m:], tam)


def smape(y_that, du_bao) -> float:
    """sMAPE (%) theo định nghĩa của M4: trung bình 200·|e| / (|y| + |ŷ|)."""
    y_that, du_bao = np.asarray(y_that, dtype=float), np.asarray(du_bao, dtype=float)
    mau = np.abs(y_that) + np.abs(du_bao)
    return float(np.mean(np.where(mau == 0, 0.0, 200 * np.abs(y_that - du_bao) / mau)))


def mase(y_that, du_bao, y_hoc, m: int = M) -> float:
    """MASE: chia sai số cho MAE của naive MÙA VỤ trong mẫu — chú ý thang chia này khi diễn giải."""
    y_hoc = np.asarray(y_hoc, dtype=float)
    thang = np.mean(np.abs(y_hoc[m:] - y_hoc[:-m]))
    return float(np.mean(np.abs(np.asarray(y_that, float) - np.asarray(du_bao, float))) / thang) if thang > 0 else np.nan


def mase_naive1(y_that, du_bao, y_hoc) -> float:
    """MASE nhưng chia cho MAE của naive MỘT BƯỚC — cùng dự báo, khác thang chuẩn hoá."""
    return mase(y_that, du_bao, y_hoc, m=1)


def danh_gia_kho_de(chuoi: dict[str, np.ndarray], tam: int = TAM, m: int = M) -> pd.DataFrame:
    """Với mỗi chuỗi: sai số THẬT của seasonal naive trên TAM điểm cuối, theo ba thước đo."""
    hang = {}
    for ten, v in chuoi.items():
        hoc, kiem = v[:-tam], v[-tam:]
        f = du_bao_mua_vu(hoc, tam, m)
        hang[ten] = {"smape_snaive": smape(kiem, f), "mase_snaive": mase(kiem, f, hoc, m),
                     "mase_naive1_snaive": mase_naive1(kiem, f, hoc)}
    return pd.DataFrame(hang).T


def tuong_quan_kho_de(bang: pd.DataFrame) -> pd.DataFrame:
    """Tương quan giữa đặc trưng và sai số thật (MASE của seasonal naive)."""
    hang = []
    for dac_trung in ("entropy_pho", "he_so_bien_thien", "do_manh_mua_vu"):
        x, y = bang[dac_trung].to_numpy(float), bang["mase_snaive"].to_numpy(float)
        ok = np.isfinite(x) & np.isfinite(y)
        hang.append({"đặc trưng": dac_trung, "thước đo": "mase_snaive",
                     "pearson": float(stats.pearsonr(x[ok], y[ok])[0])})
    return pd.DataFrame(hang)


def de_xuat_chien_luoc(bang: pd.DataFrame, nguong_entropy: float = 0.666, nguong_mua_vu: float = 0.4) -> pd.Series:
    """Chiến lược cho từng chuỗi."""
    return pd.Series("đáng đầu tư mô hình", index=bang.index, name="chien_luoc")


# %% [markdown]
# ## Không gian đặc trưng và phân cụm hình dạng

# %%
def cot_ban_do(bang: pd.DataFrame) -> list[str]:
    """Cột vào bản đồ: chỉ đặc trưng (không có cột sai số smape_…/mase_…), bỏ hai đặc trưng quy mô, bỏ cột có NaN."""
    return [c for c in bang.columns if bang[c].notna().all() and c not in ("trung_binh", "do_lech_chuan")
            and not c.startswith(("smape", "mase"))]


def khong_gian_dac_trung(bang: pd.DataFrame, so_chieu: int = 2) -> tuple[np.ndarray, PCA]:
    """PCA trên các đặc trưng không phụ thuộc đơn vị (bỏ trung bình, độ lệch chuẩn), sau khi CHUẨN HOÁ từng cột."""
    cot = cot_ban_do(bang)
    X = StandardScaler().fit_transform(bang[cot].to_numpy(float))
    pca = PCA(n_components=so_chieu, random_state=0)
    return pca.fit_transform(X), pca


def chuan_hoa_hinh_dang(y) -> np.ndarray:
    """z-score từng chuỗi: phân cụm HÌNH DẠNG thì phải bỏ mức và biên độ."""
    y = np.asarray(y, dtype=float)
    sd = np.std(y)
    return (y - np.mean(y)) / sd if sd > 0 else y - np.mean(y)


def phan_cum_dtw(chuoi: dict[str, np.ndarray], so_cum: int = 4, chuan_hoa: bool = False,
                 cua_so: int | None = 10) -> tuple[pd.Series, np.ndarray]:
    """Khoảng cách DTW (dtaidistance, có ràng buộc Sakoe–Chiba) + phân cụm phân cấp Ward."""
    from dtaidistance import dtw
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import squareform

    ten = list(chuoi)
    day = [chuan_hoa_hinh_dang(chuoi[t]) if chuan_hoa else np.asarray(chuoi[t], dtype=float) for t in ten]
    D = dtw.distance_matrix_fast(day, window=cua_so)
    D = np.where(np.isinf(D), 0, D)
    D = D + D.T
    nhan = fcluster(linkage(squareform(D, checks=False), method="ward"), so_cum, criterion="maxclust")
    return pd.Series(nhan, index=ten, name="cum"), D


# %% [markdown]
# ## Phân tầng ABC–XYZ

# %%
def abc_xyz(ban_le: pd.DataFrame, nguong_abc=(0.2, 0.5), nguong_xyz=(0.5, 1.0)) -> pd.DataFrame:
    """ABC theo doanh thu tích luỹ (20% mặt hàng đầu = A…), XYZ theo hệ số biến thiên của doanh thu tháng.

    Ngưỡng XYZ (0,5 và 1,0) là **quy ước**, không phải chuẩn — và hệ số biến thiên KHÔNG đo được độ khó
    dự báo (chuỗi mùa vụ mạnh có CV cao nhưng rất dễ dự báo).
    """
    theo_hang = ban_le.groupby("StockCode")["doanh_thu"].agg(["sum", "mean", "std", "count"])
    theo_hang = theo_hang[theo_hang["count"] >= 12]
    theo_hang["cv"] = theo_hang["std"] / theo_hang["mean"]
    theo_hang = theo_hang.sort_values("sum", ascending=False)
    ty_le = np.arange(1, len(theo_hang) + 1) / len(theo_hang)
    theo_hang["abc"] = np.where(ty_le <= nguong_abc[0], "A", np.where(ty_le <= nguong_abc[1], "B", "C"))
    theo_hang["xyz"] = np.where(theo_hang["cv"] < nguong_xyz[0], "X",
                                np.where(theo_hang["cv"] <= nguong_xyz[1], "Y", "Z"))
    return theo_hang


# %%
if __name__ == "__main__":
    tat_ca = doc_tsf()
    print(f"{len(tat_ca)} chuỗi M4 tháng")
    chuoi = lay_mau(tat_ca, 4000)
    bang = bang_dac_trung(chuoi).join(danh_gia_kho_de(chuoi))
    print(tuong_quan_kho_de(bang).round(3).to_string(index=False))
    print(de_xuat_chien_luoc(bang).value_counts().to_dict())
    nhan, _ = phan_cum_dtw({t: chuoi[t] for t in list(chuoi)[:300]})
    print("cụm:", nhan.value_counts().to_dict())
    print(abc_xyz(doc_ban_le()).groupby(["abc", "xyz"]).size().unstack(fill_value=0).to_string())
