# %% [markdown]
# # Buổi 28 — Dự báo phân cấp và reconciliation
#
# Số chuyến du lịch qua đêm trong nước của Úc theo quý 1998–2017 (Tourism Research Australia, qua gói R tsibble).
# Cây 4 cấp: Úc → 8 bang → 76 khu vực → 304 (khu vực × mục đích chuyến đi).

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

SEED = 0
H = 8                                                        # dự báo 8 quý tới
MOC_CAT = ("2013-10-01", "2014-10-01", "2015-10-01")         # 3 mốc cắt; đoạn chấm 2014–2017
CAP = ["Total", "Total/State", "Total/State/Region", "Total/State/Region/Purpose"]
TEN_CAP = {"Total": "quốc gia", "Total/State": "bang", "Total/State/Region": "khu vực",
           "Total/State/Region/Purpose": "khu vực × mục đích"}
PHUONG_PHAP = "AutoETS/MinTrace_method-mint_shrink"          # cột dự báo đem dùng (đã khớp)
H_XS = 4                                                     # phần xác suất: mỗi quý dự báo 4 quý tới
MOC_XS_DAU = "2012-10-01"                                    # mốc đầu tiên được chấm ở phần xác suất


# %% [markdown]
# ## Dữ liệu và ma trận tổng S

# %%
def doc_du_lich() -> pd.DataFrame:
    """Total, State, Region, Purpose, ds (đầu quý), y (nghìn chuyến qua đêm)."""
    import rdata

    d = rdata.read_rda(next(tv.THU_MUC_DU_LIEU.glob("tourism-australia-tsibble/*.rda")))["tourism"]
    ra = pd.DataFrame({"Total": "Australia", "State": d["State"].astype(str).to_numpy(),
                       "Region": d["Region"].astype(str).to_numpy(), "Purpose": d["Purpose"].astype(str).to_numpy(),
                       "ds": pd.to_datetime("1970-01-01") + pd.to_timedelta(d["Quarter"].to_numpy(), unit="D"),
                       "y": d["Trips"].to_numpy(dtype=float)})
    return ra.reset_index(drop=True)


def tong_hop(d: pd.DataFrame):
    """Y (389 chuỗi dạng dài), S_df (ma trận tổng 389 × 304), tags (tên chuỗi của từng cấp)."""
    from hierarchicalforecast.utils import aggregate

    spec = [["Total"], ["Total", "State"], ["Total", "State", "Region"], ["Total", "State", "Region", "Purpose"]]
    return aggregate(d[["Total", "State", "Region", "Purpose", "ds", "y"]], spec)


def ma_tran_S(S_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    return S_df["unique_id"].to_numpy(), S_df.drop(columns="unique_id").to_numpy(dtype=float)


def do_lech_cong(du: pd.DataFrame, S_df: pd.DataFrame, cot: str) -> float:
    """Sai lệch cộng lớn nhất: |dự báo mỗi chuỗi − tổng các chuỗi đáy bên dưới nó| (0 = khớp tuyệt đối)."""
    ten, S = ma_tran_S(S_df)
    bang = du.pivot(index="unique_id", columns="ds", values=cot)
    day = bang.loc[S_df.columns[1:]].to_numpy()               # các chuỗi đáy, đúng thứ tự cột của S
    return float(np.max(np.abs(bang.loc[ten].to_numpy() - S @ day)))


# %% [markdown]
# ## Reconciliation tự viết: OLS

# %%
def hoa_giai_ols(y_mu: np.ndarray, S: np.ndarray) -> np.ndarray:
    """ỹ = S (SᵀS)⁻¹ Sᵀ ŷ — chiếu dự báo base lên không gian các dự báo khớp. y_mu: (số chuỗi,) hoặc (số chuỗi, tầm)."""
    return S @ np.linalg.solve(S.T @ S, S.T @ y_mu)


# %% [markdown]
# ## Dự báo base, reconciliation bằng thư viện, backtest

# %%
def du_bao_mot_moc(Y: pd.DataFrame, S_df: pd.DataFrame, tags: dict, moc, h: int = H) -> pd.DataFrame:
    """AutoETS + seasonal naive cho 389 chuỗi học tới `moc`; bottom-up, top-down, OLS, MinT."""
    from hierarchicalforecast.core import HierarchicalReconciliation
    from hierarchicalforecast.methods import BottomUp, MinTrace, TopDown
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, SeasonalNaive

    hoc = Y[Y["ds"] <= pd.Timestamp(moc)]
    sf = StatsForecast(models=[AutoETS(season_length=4), SeasonalNaive(4)], freq="QS", n_jobs=-1)
    du = sf.forecast(df=hoc, h=h, fitted=True, level=[80, 90])
    khop = sf.forecast_fitted_values()
    ra = HierarchicalReconciliation([BottomUp(), MinTrace(method="ols"), MinTrace(method="mint_shrink")]).reconcile(
        Y_hat_df=du, Y_df=khop, S_df=S_df, tags=tags, level=[80, 90], intervals_method="normality")
    td = HierarchicalReconciliation([TopDown(method="forecast_proportions")]).reconcile(
        Y_hat_df=du[["unique_id", "ds", "AutoETS", "SeasonalNaive"]], Y_df=khop, S_df=S_df, tags=tags)   # top-down: chỉ dự báo điểm
    ra = ra.merge(td[["unique_id", "ds", "AutoETS/TopDown_method-forecast_proportions"]], on=["unique_id", "ds"])
    return ra.assign(moc=pd.Timestamp(moc))


def du_bao_khop(ra: pd.DataFrame) -> pd.DataFrame:
    """Dự báo đem dùng: unique_id, ds, du_bao — PHẢI cộng khớp giữa các cấp."""
    return ra[["unique_id", "ds", PHUONG_PHAP]].rename(columns={PHUONG_PHAP: "du_bao"})


def backtest(Y: pd.DataFrame, S_df: pd.DataFrame, tags: dict, moc_cat=MOC_CAT) -> pd.DataFrame:
    kq = []
    for m in moc_cat:
        ra = du_bao_mot_moc(Y, S_df, tags, m)
        kq.append(ra.merge(Y, on=["unique_id", "ds"], how="left"))
    R = pd.concat(kq, ignore_index=True)
    cap = {i: TEN_CAP[k] for k, v in tags.items() for i in v}
    R["cap"] = R["unique_id"].map(cap)
    return R


def bang_sai_so(R: pd.DataFrame, cac_cot: list[str]) -> pd.DataFrame:
    """RMSE trung bình mỗi chuỗi và sai số có dấu trung bình (thực tế − dự báo), theo từng cấp."""
    dong = []
    for cap, g in R.groupby("cap", sort=False):
        for c in cac_cot:
            e = g["y"] - g[c]
            dong.append({"cap": cap, "cach": c, "rmse": float(np.sqrt((e ** 2).groupby(g["unique_id"]).mean()).mean()),
                         "sai_so_co_dau": float(e.mean())})
    return pd.DataFrame(dong)


def coverage(R: pd.DataFrame, cot: str, muc: int = 90) -> pd.Series:
    trong = (R["y"] >= R[f"{cot}-lo-{muc}"]) & (R["y"] <= R[f"{cot}-hi-{muc}"])
    return trong.groupby(R["cap"], sort=False).mean()


# %% [markdown]
# ## Khoảng khớp, hiệu chỉnh ngoài mẫu

# %%
def sai_so_ngoai_mau(Y: pd.DataFrame, S_df: pd.DataFrame, h: int = H_XS, so_moc: int = 29) -> tuple:
    """Backtest AutoETS mỗi quý, dự báo h quý tới: trả (F, A) — dự báo và thực tế, chỉ mục (moc, h), cột là chuỗi."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS

    ten, _ = ma_tran_S(S_df)
    cv = StatsForecast(models=[AutoETS(season_length=4)], freq="QS", n_jobs=-1).cross_validation(
        df=Y, h=h, n_windows=so_moc, step_size=1)
    cv["h"] = cv.groupby(["unique_id", "cutoff"]).cumcount() + 1
    F = cv.pivot_table(index=["cutoff", "h"], columns="unique_id", values="AutoETS")[ten]
    A = cv.pivot_table(index=["cutoff", "h"], columns="unique_id", values="y")[ten]
    return F, A


def G_mint(E1: np.ndarray, S: np.ndarray, ty_le_co: float = 0.5) -> np.ndarray:
    """MinT: G = (Sᵀ W⁻¹ S)⁻¹ Sᵀ W⁻¹, W = hiệp phương sai sai số 1 bước, co một nửa về đường chéo."""
    W = np.cov(E1, rowvar=False)
    W = ty_le_co * np.diag(np.diag(W)) + (1 - ty_le_co) * W + 1e-6 * np.eye(len(W))
    Wi = np.linalg.pinv(W)
    return np.linalg.solve(S.T @ Wi @ S, S.T @ Wi)


def khoang_khop(F: pd.DataFrame, A: pd.DataFrame, S: np.ndarray, muc: float = 0.9) -> pd.DataFrame:
    """Mỗi mốc c: kịch bản = dự báo base + từng vector sai số ngoài mẫu đã biết lúc c (mọi mốc cũ, mọi tầm);
    chiếu từng kịch bản lên không gian khớp (base / OLS / MinT); khoảng = hạng conformal ⌈(n + 1)·muc⌉ hai phía."""
    E = A - F
    cac_moc = sorted(F.index.get_level_values(0).unique())
    Gols = np.linalg.solve(S.T @ S, S.T)
    dong = []
    for c in [m for m in cac_moc if m >= pd.Timestamp(MOC_XS_DAU)]:
        cu = [m for m in cac_moc if m <= c - pd.DateOffset(months=3 * H_XS)]      # sai số đã biết đủ lúc c
        if len(cu) < 4:
            continue                                                            # chưa đủ sai số ngoài mẫu
        Ecu = E.loc[cu]
        G = G_mint(Ecu[Ecu.index.get_level_values("h") == 1].to_numpy(), S)
        e = Ecu.to_numpy()
        n = len(e)
        k = int(np.ceil((n + 1) * (1 - (1 - muc) / 2)))
        for h in range(1, H_XS + 1):
            fb, y = F.loc[(c, h)].to_numpy(), A.loc[(c, h)].to_numpy()
            for ten, GG in (("base", None), ("ols", Gols), ("mint", G)):
                kb = fb[None, :] + e if GG is None else (S @ GG @ (fb[None, :] + e).T).T
                diem = fb if GG is None else S @ GG @ fb
                xep = np.sort(kb, axis=0)
                lo, hi = (xep[n - k], xep[k - 1]) if k <= n else (np.full(len(fb), -np.inf), np.full(len(fb), np.inf))
                dong.append(pd.DataFrame({"moc": c, "h": h, "cach": ten, "unique_id": F.columns, "y": y,
                                          "du_bao": diem, "lo": lo, "hi": hi}))
    return pd.concat(dong, ignore_index=True)


# %% [markdown]
# ## Phân cấp theo thời gian: quý và năm

# %%
def phan_cap_thoi_gian(Y: pd.DataFrame, id_: str = "Australia", nam_kiem=(2016, 2017)) -> pd.DataFrame:
    """Dự báo 4 quý của năm (ETS quý) và cả năm (ETS năm) riêng rẽ, rồi hoà giải OLS với S_tg = [1 1 1 1; I₄]."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS

    s = Y[Y["unique_id"] == id_].set_index("ds")["y"]
    S = np.vstack([np.ones((1, 4)), np.eye(4)])
    dong = []
    for nam in nam_kiem:
        q = s[s.index.year < nam]
        n = q.groupby(q.index.year).sum()
        fq = StatsForecast(models=[AutoETS(season_length=4)], freq="QS").forecast(
            df=pd.DataFrame({"unique_id": id_, "ds": q.index, "y": q.to_numpy()}), h=4)["AutoETS"].to_numpy()
        fn = StatsForecast(models=[AutoETS()], freq="YS").forecast(
            df=pd.DataFrame({"unique_id": id_, "ds": pd.to_datetime(n.index.astype(str)), "y": n.to_numpy()}), h=1)["AutoETS"].to_numpy()
        base = np.r_[fn, fq]
        khop = hoa_giai_ols(base, S)
        thuc = s[s.index.year == nam].to_numpy()
        dong.append({"nam": nam, "thuc_nam": thuc.sum(), "ets_nam": fn[0], "tong_4_quy": fq.sum(), "khop_nam": khop[0],
                     "mae_quy_base": float(np.mean(np.abs(thuc - fq))), "mae_quy_khop": float(np.mean(np.abs(thuc - khop[1:])))})
    return pd.DataFrame(dong)
