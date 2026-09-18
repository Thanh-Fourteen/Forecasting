# %% [markdown]
# # Buổi 6 — Phân rã nhu cầu điện theo giờ thành xu hướng + mùa vụ + phần dư
#
# Bản ĐÃ SỬA. Dữ liệu: EIA-930, nhu cầu điện theo giờ của PJM Interconnection năm 2024.

# %%
from __future__ import annotations

import pandas as pd
from statsmodels.tsa.seasonal import MSTL

import tv

CHU_KY = (24, 168)  # ngày, tuần (giờ)
MUI_GIO = "America/New_York"


def doc_nhu_cau(vung: str = "PJM") -> pd.Series:
    """Cột `Demand (MW)` GỐC theo giờ UTC (mốc cuối giờ), lưới đều; giờ trống để NaN."""
    tep = [tv.THU_MUC_DU_LIEU / "eia930-balance-2024-h1" / "EIA930_BALANCE_2024_Jan_Jun.csv",
           tv.THU_MUC_DU_LIEU / "eia930-balance-2024-h2" / "EIA930_BALANCE_2024_Jul_Dec.csv"]
    cot = ["Balancing Authority", "UTC Time at End of Hour", "Demand (MW)"]
    df = pd.concat([pd.read_csv(t, usecols=cot, thousands=",") for t in tep])
    df = df[df["Balancing Authority"] == vung]
    ds = pd.to_datetime(df["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p")
    y = pd.Series(df["Demand (MW)"].to_numpy(dtype=float), index=ds, name="mw").sort_index()
    return y.asfreq("h")


def lap_cho_trong(y: pd.Series) -> pd.Series:
    """Nội suy tuyến tính theo thời gian — STL/MSTL của statsmodels trả TOÀN NaN nếu còn một NaN."""
    return y.interpolate(method="time")


# %%
def phan_ra(y: pd.Series, robust: bool = False) -> pd.DataFrame:
    """MSTL với mùa vụ ngày và tuần. Cột: y, trend, seasonal_24, seasonal_168, resid."""
    kq = MSTL(y, periods=CHU_KY, stl_kwargs={"robust": robust}).fit()
    bang = pd.DataFrame({"y": y, "trend": kq.trend, "resid": kq.resid})
    for cot in kq.seasonal.columns:
        bang[cot] = kq.seasonal[cot]
    return bang


def do_manh(bang: pd.DataFrame) -> dict[str, float]:
    """F_T = max(0, 1 − Var(R)/Var(T+R)); F_S của từng mùa vụ = max(0, 1 − Var(R)/Var(S_i+R)) (FPP §4.3, feasts)."""
    r = bang["resid"]
    kq = {"F_T": max(0.0, float(1 - r.var() / (bang["trend"] + r).var()))}
    for cot in [c for c in bang.columns if c.startswith("seasonal")]:
        kq["F_S_" + cot.removeprefix("seasonal").lstrip("_")] = max(0.0, float(1 - r.var() / (bang[cot] + r).var()))
    return kq


def ho_so_phan_du(bang: pd.DataFrame, theo: tuple[str, ...] = ("dayofweek", "hour")) -> pd.Series:
    """Trung bình phần dư theo nhóm lịch GIỜ ĐỊA PHƯƠNG — còn mẫu hình ở đây là mùa vụ chưa tách hết."""
    r = bang["resid"].dropna()
    dia_phuong = r.index.tz_localize("UTC").tz_convert(MUI_GIO)
    return r.groupby([getattr(dia_phuong, k) for k in theo]).mean()


def ty_le_mau_hinh_con_lai(bang: pd.DataFrame, theo: tuple[str, ...]) -> float:
    """Phương sai của hồ sơ phần dư theo nhóm lịch / phương sai của y — gần 0 nghĩa là phần dư sạch mẫu hình đó."""
    return float(ho_so_phan_du(bang, theo).var() / bang["y"].var())


# %%
if __name__ == "__main__":
    y = doc_nhu_cau()
    print(f"{len(y)} giờ, NaN {y.isna().sum()}, {y.index[0]} → {y.index[-1]}")
    bang = phan_ra(lap_cho_trong(y))
    print({k: round(v, 3) for k, v in do_manh(bang).items()})
    for theo in (("dayofweek", "hour"), ("month", "hour")):
        print(theo, "mẫu hình còn trong phần dư:", round(ty_le_mau_hinh_con_lai(bang, theo), 4))
