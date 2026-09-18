# %% [markdown]
# # Lời giải mẫu — `feature.py` (GIÁM KHẢO GIỮ, KHÔNG VÀO ZIP)

# %%
from __future__ import annotations

import numpy as np
import pandas as pd

TAM = 24  # dự báo 24 bước tới

BIET_TRUOC_VO_HAN = "vô hạn"
BIET_TRUOC_TRE = "t-h"
BIET_TRUOC_KE_HOACH = "kế hoạch"


def bo_feature(y: pd.Series, tam: int = TAM) -> pd.DataFrame:
    """22 feature: lag, rolling đã shift, lịch, Fourier. Mọi cột chỉ dùng dữ liệu tới t − tam."""
    f = pd.DataFrame(index=y.index)
    tre = y.shift(tam)
    for lag in (1, 2, 3, 7, 14, 24, 48):
        f[f"lag_{lag}"] = y.shift(max(lag, tam))
    for w in (12, 48, 168):
        f[f"tb_{w}"] = tre.rolling(w).mean()
        f[f"sd_{w}"] = tre.rolling(w).std()
        f[f"min_{w}"] = tre.rolling(w).min()
    f["chenh"] = tre.diff()
    moc = y.index
    f["gio"] = moc.hour
    f["thu"] = moc.dayofweek
    f["thang"] = moc.month
    f["gio_sin"] = np.sin(2 * np.pi * moc.hour / 24)
    f["gio_cos"] = np.cos(2 * np.pi * moc.hour / 24)
    t = (moc - moc[0]).total_seconds().to_numpy() / 86400.0
    for i in (1, 2):
        f[f"fourier_sin_{i}"] = np.sin(2 * np.pi * i * t / 365.25)
        f[f"fourier_cos_{i}"] = np.cos(2 * np.pi * i * t / 365.25)
    return f


def bang_biet_truoc(f: pd.DataFrame) -> pd.DataFrame:
    hang = []
    for cot in f.columns:
        if cot.startswith(("lag_", "tb_", "sd_", "min_", "max_", "chenh")):
            loai = BIET_TRUOC_TRE
        elif cot.startswith("du_bao_"):
            loai = BIET_TRUOC_KE_HOACH
        else:
            loai = BIET_TRUOC_VO_HAN
        hang.append({"feature": cot, "biết trước": loai})
    return pd.DataFrame(hang)


def kiem_ro_ri(ham_feature, y: pd.Series, cac_moc=None, sai_so: float = 1e-9) -> pd.DataFrame:
    day_du = ham_feature(y)
    if cac_moc is None:
        cac_moc = [y.index[int(len(y) * p)] for p in (0.5, 0.7, 0.9)]
    hang = []
    for moc in cac_moc:
        cat = ham_feature(y[y.index <= moc])
        chung = day_du.index[day_du.index <= moc]
        for cot in day_du.columns:
            a = day_du.loc[chung, cot].to_numpy(dtype=float)
            b = (cat.reindex(chung)[cot].to_numpy(dtype=float) if cot in cat.columns
                 else np.full(len(chung), np.nan))
            if not np.allclose(a, b, rtol=0, atol=sai_so, equal_nan=True):
                hang.append({"feature": cot, "mốc cắt": moc})
    return pd.DataFrame(hang, columns=["feature", "mốc cắt"])


def baseline_seasonal_naive(y: pd.Series, tam: int = TAM, chu_ky: int = 48) -> pd.Series:
    """Dự báo y_{t+tam} bằng giá trị cùng thời điểm chu kỳ trước."""
    return y.shift(chu_ky - tam)


# %%
if __name__ == "__main__":
    import importlib.util
    from pathlib import Path
    day = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("ls", day / "lam_sach.py")
    ls = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ls)
    phat = day.parents[1] / "phat" / "du-lieu"
    sach = ls.lam_sach(ls.doc(phat / "noi-bai.csv"), "noi-bai")
    y = sach["temperature"].ffill().dropna()
    f = bo_feature(y)
    print("số feature:", f.shape[1])
    print(bang_biet_truoc(f)["biết trước"].value_counts().to_dict())
    print("rò rỉ:", kiem_ro_ri(bo_feature, y.iloc[:3000]).to_dict("records") or "không có")
