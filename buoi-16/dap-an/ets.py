# %% [markdown]
# # Buổi 16 — Exponential smoothing và Theta
#
# Bản ĐÃ SỬA. Dữ liệu: 366 chuỗi du lịch theo tháng (Tourism, Monash), hành khách hàng không EU theo tháng (Eurostat).

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy.optimize import minimize

import tv
from tv.backtest import backtest, diebold_mariano

warnings.simplefilter("ignore")

M = 12        # chu kỳ mùa vụ của dữ liệu tháng
TAM = 24      # tầm dự báo chính thức của cuộc thi Tourism


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_tourism() -> dict[str, np.ndarray]:
    """366 chuỗi du lịch theo tháng (.tsf của Monash)."""
    tep = tv.THU_MUC_DU_LIEU / "monash-tourism-monthly" / "tourism_monthly_dataset.tsf"
    chuoi, trong_data = {}, False
    with open(tep, encoding="utf-8", errors="ignore") as f:
        for dong in f:
            if not trong_data:
                trong_data = dong.strip().lower() == "@data"
                continue
            if dong.strip():
                phan = dong.strip().split(":")
                chuoi[phan[0]] = np.array([float(x) for x in phan[-1].split(",")])
    return chuoi


def dang_dai(chuoi: dict[str, np.ndarray]) -> pd.DataFrame:
    """Dạng dài unique_id, ds, y; ds là số nguyên, mọi chuỗi kết thúc ở cùng một ds (để backtest cắt cùng lúc)."""
    n = max(len(v) for v in chuoi.values())
    return pd.concat([pd.DataFrame({"unique_id": t, "ds": np.arange(n - len(v), n), "y": v})
                      for t, v in chuoi.items()], ignore_index=True)


def doc_hanh_khach() -> pd.Series:
    """Hành khách hàng không EU27 theo tháng (triệu), 1/2008 → 12/2019 (bỏ giai đoạn COVID, buổi 11)."""
    d = pd.read_csv(tv.THU_MUC_DU_LIEU / "eurostat-hanh-khach-hang-khong" / "eurostat-avia-paoc-eu27.csv")
    y = pd.Series(d["OBS_VALUE"].to_numpy(float) / 1e6,
                  index=pd.PeriodIndex(d["TIME_PERIOD"], freq="M").to_timestamp(), name="y")
    return y[:"2019-12"]


def theo_nam(v: np.ndarray) -> np.ndarray:
    """Cộng mỗi 12 tháng thành một năm (bỏ các tháng lẻ ở đầu)."""
    n = len(v) // 12 * 12
    return v[len(v) - n:].reshape(-1, 12).sum(axis=1)


# %% [markdown]
# ## SES và Holt tự viết
#
# Khớp một bước: giá trị khớp cho y_t chỉ dùng mức (và xu hướng) tính tới t − 1.

# %%
def ses_loc(y: np.ndarray, alpha: float) -> tuple[np.ndarray, float]:
    """Trả (giá trị khớp một bước cho y_1..y_{n-1}, mức cuối). Mức ban đầu = y_0."""
    muc = float(y[0])
    khop = np.empty(len(y) - 1)
    for t in range(1, len(y)):
        khop[t - 1] = muc                              # dự báo y_t bằng mức tới t − 1
        muc = alpha * y[t] + (1 - alpha) * muc          # rồi mới cập nhật bằng y_t
    return khop, muc


def ses_sse(alpha: float, y: np.ndarray) -> float:
    khop, _ = ses_loc(y, alpha)
    return float(np.sum((y[1:] - khop) ** 2))


def ses_toi_uu(y: np.ndarray) -> dict:
    """α làm tổng bình phương sai số khớp một bước nhỏ nhất (scipy.optimize.minimize, 0 ≤ α ≤ 1)."""
    kq = minimize(lambda a: ses_sse(a[0], y), x0=[0.5], bounds=[(0.0, 1.0)])
    alpha = float(kq.x[0])
    return {"alpha": alpha, "sse": ses_sse(alpha, y), "muc_cuoi": ses_loc(y, alpha)[1]}


def ses_du_bao(y: np.ndarray, alpha: float, h: int) -> np.ndarray:
    """SES dự báo mọi bước tới bằng mức cuối: đường phẳng."""
    return np.repeat(ses_loc(y, alpha)[1], h)


def holt_loc(y: np.ndarray, alpha: float, beta: float) -> tuple[np.ndarray, float, float]:
    """Holt: mức + độ dốc. Ban đầu mức = y_0, độ dốc = y_1 − y_0."""
    muc, doc = float(y[0]), float(y[1] - y[0])
    khop = np.empty(len(y) - 1)
    for t in range(1, len(y)):
        khop[t - 1] = muc + doc
        muc_moi = alpha * y[t] + (1 - alpha) * (muc + doc)
        doc = beta * (muc_moi - muc) + (1 - beta) * doc
        muc = muc_moi
    return khop, muc, doc


def holt_toi_uu(y: np.ndarray) -> dict:
    def sse(p):
        khop, _, _ = holt_loc(y, p[0], p[1])
        return float(np.sum((y[1:] - khop) ** 2))
    kq = minimize(sse, x0=[0.5, 0.1], bounds=[(0.0, 1.0), (0.0, 1.0)])
    alpha, beta = (float(x) for x in kq.x)
    _, muc, doc = holt_loc(y, alpha, beta)
    return {"alpha": alpha, "beta": beta, "sse": sse(kq.x), "muc_cuoi": muc, "doc_cuoi": doc}


def holt_du_bao(y: np.ndarray, alpha: float, beta: float, h: int) -> np.ndarray:
    _, muc, doc = holt_loc(y, alpha, beta)
    return muc + doc * np.arange(1, h + 1)


def so_voi_statsforecast(y: np.ndarray, h: int = 3) -> pd.DataFrame:
    """Dự báo SES và Holt tự viết so với statsforecast (ước lượng bằng likelihood, mức ban đầu cũng tối ưu)."""
    from statsforecast.models import Holt, SimpleExponentialSmoothingOptimized
    s, ho = ses_toi_uu(y), holt_toi_uu(y)
    return pd.DataFrame({
        "tự viết SES": ses_du_bao(y, s["alpha"], h),
        "statsforecast SES": SimpleExponentialSmoothingOptimized().fit(y).predict(h)["mean"],
        "tự viết Holt": holt_du_bao(y, ho["alpha"], ho["beta"], h),
        "statsforecast Holt": Holt().fit(y).predict(h)["mean"],
    }, index=pd.Index(range(1, h + 1), name="bước"))


# %% [markdown]
# ## Holt–Winters: cộng hay nhân

# %%
def holt_winters(y: pd.Series, h: int, kieu: str = "nhan", level: list[int] | None = None) -> pd.DataFrame:
    """Holt–Winters bằng ETS của statsforecast: kieu 'cong' = ETS(A,A,A), 'nhan' = ETS(M,A,M)."""
    from statsforecast.models import AutoETS
    ma = {"cong": "AAA", "nhan": "MAM"}[kieu]
    return pd.DataFrame(AutoETS(season_length=M, model=ma).fit(y.to_numpy()).predict(h, level=level))


def so_sanh_cong_nhan(y: pd.Series, moc: str = "2018-01") -> pd.DataFrame:
    """Học tới trước mốc, chấm 24 tháng sau: HW cộng, HW nhân, AutoETS (chọn theo AICc), seasonal naive."""
    from statsforecast.models import AutoETS
    hoc, kiem = y[y.index < moc], y[y.index >= moc].to_numpy()
    h = len(kiem)
    du_bao = {"HW cộng ETS(A,A,A)": holt_winters(hoc, h, "cong")["mean"].to_numpy(),
              "HW nhân ETS(M,A,M)": holt_winters(hoc, h, "nhan")["mean"].to_numpy()}
    tu_dong = AutoETS(season_length=M).fit(hoc.to_numpy())
    du_bao[f"AutoETS → {tu_dong.model_['method']}"] = tu_dong.predict(h)["mean"]
    du_bao["seasonal naive"] = np.array([hoc.to_numpy()[-M:][i % M] for i in range(h)])
    return pd.DataFrame([{"mô hình": k, "MAE": float(np.mean(np.abs(kiem - d))),
                          "MAPE (%)": float(np.mean(np.abs(kiem - d) / kiem) * 100),
                          "ME": float(np.mean(kiem - d))} for k, d in du_bao.items()])


def du_bao_hanh_khach(y: pd.Series, moc: str = "2018-01") -> dict:
    """Dự báo 24 tháng sau mốc bằng holt_winters với cấu hình mặc định; trả dự báo và MAPE (%)."""
    hoc, kiem = y[y.index < moc], y[y.index >= moc]
    d = holt_winters(hoc, len(kiem))["mean"].to_numpy()
    return {"du_bao": pd.Series(d, index=kiem.index), "MAPE": float(np.mean(np.abs(kiem.to_numpy() - d) / kiem.to_numpy()) * 100)}


def bien_do_mua_vu(y: pd.Series) -> pd.Series:
    """Tháng cao nhất trừ tháng thấp nhất, theo năm."""
    return y.groupby(y.index.year).agg(lambda s: s.max() - s.min())


# %% [markdown]
# ## Theta
#
# Theta chuẩn (Assimakopoulos & Nikolopoulos 2000) = SES trên chuỗi + một nửa độ dốc của đường thẳng khớp cả chuỗi
# (Hyndman & Billah 2003).

# %%
def theta_du_bao(y: np.ndarray, h: int, alpha: float | None = None) -> np.ndarray:
    """Theta không mùa vụ: đường SES phẳng cộng drift bằng một nửa độ dốc hồi quy theo thời gian."""
    n = len(y)
    doc = float(np.polyfit(np.arange(n), y, 1)[0])
    alpha = ses_toi_uu(y)["alpha"] if alpha is None else alpha
    return ses_du_bao(y, alpha, h) + 0.5 * doc * np.arange(1, h + 1)


# %% [markdown]
# ## Backtest 366 chuỗi du lịch, so seasonal naive, kiểm định, tỷ lệ phủ

# %%
def backtest_tourism(df: pd.DataFrame, so_cua_so: int = 2, buoc: int = 12, h: int = TAM) -> pd.DataFrame:
    """AutoETS, AutoTheta, SeasonalNaive trên các cửa sổ rolling origin (bộ backtest buổi 15), kèm khoảng 80% và 95%."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

    def du_bao(lich_su, ds_can):
        sf = StatsForecast(models=[AutoETS(season_length=M), AutoTheta(season_length=M), SeasonalNaive(M)],
                           freq=1, n_jobs=-1)
        return ds_can.merge(sf.forecast(df=lich_su, h=h, level=[80, 95]).reset_index(), on=["unique_id", "ds"])

    return backtest(df, du_bao, h=h, so_cua_so=so_cua_so, buoc=buoc)


MO_HINH = ["AutoETS", "AutoTheta", "SeasonalNaive"]


def mase_theo_chuoi(kq: pd.DataFrame, df: pd.DataFrame, mo_hinh=MO_HINH) -> pd.DataFrame:
    """MASE mỗi chuỗi (trung bình qua các cửa sổ); mẫu số = seasonal naive trong phần học tới cutoff."""
    mau = {}
    for (uid, cutoff), _ in kq.groupby(["unique_id", "cutoff"]):
        hoc = df.loc[(df["unique_id"] == uid) & (df["ds"] <= cutoff), "y"].to_numpy()
        mau[(uid, cutoff)] = float(np.mean(np.abs(hoc[M:] - hoc[:-M])))
    thang = pd.Series([mau[k] for k in zip(kq["unique_id"], kq["cutoff"], strict=True)], index=kq.index)
    return pd.DataFrame({m: ((kq["y"] - kq[m]).abs() / thang).groupby(kq["unique_id"]).mean() for m in mo_hinh})


def kiem_dinh_so_snaive(mase: pd.DataFrame, goc: str = "SeasonalNaive") -> pd.DataFrame:
    """Mỗi mô hình so seasonal naive: MASE trung bình, tỷ lệ chuỗi thắng, DM trên chênh MASE của các chuỗi.

    Các chuỗi độc lập với nhau nên chênh MASE không tự tương quan: DM với h = 1 (bản hiệu chỉnh HLN).
    """
    hang = []
    for m in mase.columns:
        if m == goc:
            continue
        dm = diebold_mariano(mase[m].to_numpy(), mase[goc].to_numpy(), h=1, ham_mat_mat=lambda x: x)
        hang.append({"mô hình": m, "MASE trung bình": float(mase[m].mean()), "MASE trung vị": float(mase[m].median()),
                     "tỷ lệ chuỗi thắng": float((mase[m] < mase[goc]).mean()), "DM": dm.thong_ke, "p": dm.p_value})
    hang.append({"mô hình": goc, "MASE trung bình": float(mase[goc].mean()), "MASE trung vị": float(mase[goc].median())})
    return pd.DataFrame(hang)


def ty_le_phu(kq: pd.DataFrame, mo_hinh: str, muc: int) -> float:
    """Tỷ lệ giá trị thật nằm trong khoảng dự báo muc% trên các cửa sổ backtest (không phải trên phần học)."""
    trong = (kq["y"] >= kq[f"{mo_hinh}-lo-{muc}"]) & (kq["y"] <= kq[f"{mo_hinh}-hi-{muc}"])
    return float(trong.mean())


# %%
if __name__ == "__main__":
    chuoi = doc_tourism()
    y_nam = theo_nam(chuoi["T249"])
    print(ses_toi_uu(y_nam), holt_toi_uu(y_nam))
    print(so_voi_statsforecast(y_nam).round(1))
    hk = doc_hanh_khach()
    print(so_sanh_cong_nhan(hk).round(3).to_string(index=False))
    df = dang_dai(chuoi)
    kq = backtest_tourism(df)
    mase = mase_theo_chuoi(kq, df)
    print(kiem_dinh_so_snaive(mase).round(4).to_string(index=False))
    for m in ("AutoETS", "AutoTheta"):
        print(m, {muc: round(ty_le_phu(kq, m, muc) * 100, 1) for muc in (80, 95)})
