# %% [markdown]
# # Buổi 19 — Nhu cầu gián đoạn (ĐÁP ÁN)
#
# Dữ liệu: 2.674 chuỗi bán phụ tùng ô tô theo tháng, 1/1998 → 3/2002 (Car Parts, Monash).

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import stats

import tv
from tv.backtest import backtest
from tv.du_lieu import doc_tsf

warnings.simplefilter("ignore")

SO_THANG = 51        # 1/1998 → 3/2002
SO_KY_CHAM = 12      # 12 tháng cuối là kỳ chấm, mỗi tháng một cutoff
LEAD = 1             # đặt cuối tháng t, hàng về đầu tháng t + 2: chờ trọn 1 tháng
MUC_PHUC_VU = 0.9    # mức tồn đủ cho 90% trường hợp (chi phí thiếu 9, tồn 1: 9 / (9 + 1) = 0,9)
CHI_PHI_TON = 1.0    # mỗi món tồn kho cuối tháng
CHI_PHI_THIEU = 9.0  # mỗi món khách hỏi mà hết hàng (mất đơn)
MO_HINH = ["AutoETS", "CrostonClassic", "CrostonSBA", "TSB", "ADIDA", "IMAPA", "SeasonalNaive", "Naive",
           "HistoricAverage", "Zero"]


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_car_parts() -> pd.DataFrame:
    """Dạng dài unique_id, ds (tháng thứ 0 → 50), y. Bản Monash đã thay ô thiếu bằng 0."""
    df, _ = doc_tsf(tv.THU_MUC_DU_LIEU / "monash-car-parts-khong-thieu" / "car_parts_dataset_without_missing_values.tsf")
    df["ds"] = df.groupby("unique_id").cumcount()
    return df[["unique_id", "ds", "y"]]


def ma_tran(df: pd.DataFrame) -> pd.DataFrame:
    """Mỗi dòng một chuỗi, mỗi cột một tháng."""
    return df.pivot(index="unique_id", columns="ds", values="y")


# %% [markdown]
# ## Phân loại Syntetos–Boylan

# %%
def phan_loai(y: np.ndarray) -> dict:
    """ADI = số kỳ / số kỳ có bán; CV² = (độ lệch chuẩn / trung bình)² của các lượng bán khác 0."""
    y = np.asarray(y, float)
    co_ban = y[y > 0]
    if co_ban.size < 2:
        return {"ADI": np.nan, "CV2": np.nan, "loại": "quá ít lần bán"}
    adi = y.size / co_ban.size
    cv2 = float((co_ban.std() / co_ban.mean()) ** 2)
    if adi < 1.32:
        loai = "mượt" if cv2 < 0.49 else "thất thường"
    else:
        loai = "gián đoạn" if cv2 < 0.49 else "cục"
    return {"ADI": adi, "CV2": cv2, "loại": loai}


def bang_phan_loai(Y: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([phan_loai(v) for v in Y.to_numpy()], index=Y.index)


# %% [markdown]
# ## Croston, SBA, TSB tự viết

# %%
def ses(x: np.ndarray, alpha: float) -> float:
    """Làm trơn hàm mũ đơn (buổi 16), mức ban đầu = số đầu tiên; trả mức cuối."""
    muc = float(x[0])
    for v in x[1:]:
        muc = alpha * v + (1 - alpha) * muc
    return muc


def croston(y: np.ndarray, alpha: float = 0.1, sba: bool = False) -> float:
    """Dự báo mỗi kỳ = (lượng bán khi có bán) / (khoảng cách giữa hai lần bán), mỗi phần làm trơn riêng."""
    y = np.asarray(y, float)
    vi_tri = np.flatnonzero(y > 0)
    if vi_tri.size == 0:
        return 0.0
    luong = y[vi_tri]
    khoang = np.diff(vi_tri + 1, prepend=0)       # lần bán đầu: tính từ đầu chuỗi
    du_bao = ses(luong, alpha) / ses(khoang, alpha)
    return du_bao * (1 - alpha / 2) if sba else du_bao


def tsb(y: np.ndarray, alpha_d: float = 0.1, alpha_p: float = 0.1) -> float:
    """TSB: xác suất có bán cập nhật MỌI kỳ (kỳ không bán kéo nó xuống); lượng bán chỉ cập nhật khi có bán."""
    y = np.asarray(y, float)
    if not (y > 0).any():
        return 0.0
    xac_suat = ses((y > 0).astype(float), alpha_p)
    luong = ses(y[y > 0], alpha_d)
    return xac_suat * luong


# %% [markdown]
# ## Backtest: 12 cutoff, mỗi cutoff dự báo 2 tháng tới

# %%
def backtest_car_parts(df: pd.DataFrame, luu: bool = False) -> pd.DataFrame:
    """Mọi mô hình trên 12 cửa sổ rolling origin (bộ backtest buổi 15). Cả 2.674 chuỗi mất ~15 giây; luu=True ghi
    kết quả vào lab/du-lieu/cache/."""
    tep = tv.THU_MUC_DU_LIEU.parent / "cache" / f"backtest-{df['unique_id'].nunique()}.parquet"
    if luu and tep.exists():
        return pd.read_parquet(tep)
    from statsforecast import StatsForecast
    from statsforecast.models import (
        ADIDA,
        IMAPA,
        TSB,
        AutoETS,
        CrostonClassic,
        CrostonSBA,
        HistoricAverage,
        Naive,
        SeasonalNaive,
    )
    mo_hinh = [AutoETS(season_length=1), CrostonClassic(), CrostonSBA(), TSB(0.1, 0.1), ADIDA(), IMAPA(),
               SeasonalNaive(12), Naive(), HistoricAverage()]

    def ham(lich_su, ds_can):
        f = StatsForecast(models=mo_hinh, freq=1, n_jobs=-1).forecast(df=lich_su, h=LEAD + 1).reset_index()
        f["Zero"] = 0.0
        return ds_can.merge(f, on=["unique_id", "ds"])

    kq = backtest(df, ham, h=LEAD + 1, so_cua_so=SO_KY_CHAM, buoc=1)
    if luu:
        tep.parent.mkdir(parents=True, exist_ok=True)
        kq.to_parquet(tep)
    return kq


# %% [markdown]
# ## Chỉ số: RMSSE, MASE (không dùng MAPE)

# %%
def danh_gia(kq: pd.DataFrame, Y: pd.DataFrame, mo_hinh=MO_HINH) -> pd.DataFrame:
    """Chỉ số của dự báo 1 tháng tới, trung bình qua các chuỗi. Mẫu số lấy trên phần học (trước cutoff đầu)."""
    k1 = kq[kq["buoc_h"] == 1]
    that = k1.pivot(index="unique_id", columns="ds", values="y").loc[Y.index].to_numpy()
    hoc = Y.to_numpy()[:, :int(k1["ds"].min())]
    mau_rmsse = np.mean(np.diff(hoc, axis=1) ** 2, axis=1)
    mau_mase = np.mean(np.abs(np.diff(hoc, axis=1)), axis=1)
    dung = mau_rmsse > 0
    hang = []
    for m in mo_hinh:
        e = that - k1.pivot(index="unique_id", columns="ds", values=m).loc[Y.index].to_numpy()
        hang.append({"mô hình": m,
                     "RMSSE": float(np.mean(np.sqrt(np.mean(e ** 2, axis=1)[dung] / mau_rmsse[dung]))),
                     "MASE": float(np.mean(np.mean(np.abs(e), axis=1)[dung] / mau_mase[dung])),
                     "ME": float(e.mean())})
    bang = pd.DataFrame(hang).set_index("mô hình")
    bang.attrs["số chuỗi bỏ (phần học phẳng)"] = int((~dung).sum())
    return bang


# %% [markdown]
# ## Mô phỏng tồn kho: order-up-to, xem kho mỗi tháng, hàng về sau LEAD tháng

# %%
def muc_dat_len(du_bao_tong: np.ndarray, muc: float = MUC_PHUC_VU) -> np.ndarray:
    """Mức đặt lên S = quantile `muc` của nhu cầu (L + 1) tháng, giả định Poisson với trung bình = dự báo tổng."""
    du_bao_tong = np.asarray(du_bao_tong, float)
    s = stats.poisson.ppf(muc, np.maximum(du_bao_tong, 1e-12))
    return np.where(du_bao_tong > 0, s, 0.0)


def mo_phong_ton_kho(nhu_cau: np.ndarray, muc_S: np.ndarray, lead: int = LEAD) -> dict:
    """nhu_cau, muc_S: (số chuỗi, số tháng). Đầu tháng nhận hàng → bán (thiếu thì mất đơn) → cuối tháng đặt thêm cho
    vị thế kho (trên tay + đang về) lên đúng S. Hàng đặt cuối tháng t về đầu tháng t + 1 + lead."""
    nhu_cau = np.atleast_2d(np.asarray(nhu_cau, float))
    muc_S = np.atleast_2d(np.asarray(muc_S, float))
    n, T = nhu_cau.shape
    tren_tay = muc_S[:, 0].copy()
    dang_ve = np.zeros((n, lead + 1))      # cột 0: về đầu tháng tới; cột cuối: vừa đặt
    ton = thieu = ban = 0.0
    for t in range(T):
        tren_tay += dang_ve[:, 0]
        dang_ve = np.roll(dang_ve, -1, axis=1)
        dang_ve[:, -1] = 0
        ban_t = np.minimum(tren_tay, nhu_cau[:, t])
        tren_tay -= ban_t
        ban += ban_t.sum()
        thieu += (nhu_cau[:, t] - ban_t).sum()
        ton += tren_tay.sum()
        if t + 1 < T:
            dang_ve[:, -1] += np.maximum(muc_S[:, t + 1] - tren_tay - dang_ve.sum(axis=1), 0)
    return {"tồn kho trung bình": ton / (n * T), "tỷ lệ đáp ứng": ban / (ban + thieu) if ban + thieu else 1.0,
            "chi phí mỗi mã": (CHI_PHI_TON * ton + CHI_PHI_THIEU * thieu) / n}


def chi_phi_ton_kho(kq: pd.DataFrame, Y: pd.DataFrame, mo_hinh=MO_HINH) -> pd.DataFrame:
    """Mỗi cutoff: cộng dự báo L + 1 tháng tới → mức S → mô phỏng trên nhu cầu thật của 12 tháng chấm."""
    k1 = kq[kq["buoc_h"] == 1]
    that = k1.pivot(index="unique_id", columns="ds", values="y").loc[Y.index].to_numpy()
    tong = kq.groupby(["unique_id", "cutoff"])[list(mo_hinh)].sum()
    hang = {}
    for m in mo_hinh:
        S = muc_dat_len(tong[m].unstack("cutoff").loc[Y.index].to_numpy())
        hang[m] = mo_phong_ton_kho(that, S)
    return pd.DataFrame(hang).T.rename_axis("mô hình")


def chon_mo_hinh(bang: pd.DataFrame) -> str:
    """Mô hình dùng để đặt hàng: chi phí tồn kho mô phỏng thấp nhất."""
    return str(bang["chi phí mỗi mã"].idxmin())


# %%
if __name__ == "__main__":
    df = doc_car_parts()
    Y = ma_tran(df)
    print(bang_phan_loai(Y.iloc[:, :SO_THANG - SO_KY_CHAM - 1])["loại"].value_counts())
    y = np.array([0, 0, 3, 0, 0, 0, 2, 0, 4, 0, 0, 0])
    print(croston(y), croston(y, sba=True), tsb(y))
    kq = backtest_car_parts(df, luu=True)
    bang = danh_gia(kq, Y).join(chi_phi_ton_kho(kq, Y))
    print(bang.round(3))
    print("chọn:", chon_mo_hinh(bang))
