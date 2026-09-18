# %% [markdown]
# # Buổi 1 — Đánh giá một dự báo cho trung thực
#
# Bản ĐÃ SỬA. Bài toán: mỗi thứ Hai 00:00, dự báo điện tiêu thụ từng giờ của 7 ngày tới (tầm 168 giờ) cho một hộ
# gia đình ở Sceaux (Pháp). Đơn vị: kWh mỗi giờ (= công suất trung bình kW trong giờ đó).

# %%
from __future__ import annotations

import numpy as np
import pandas as pd

import tv

TAM = 168  # tầm dự báo: 7 ngày × 24 giờ
MOC = "2010-01-04"  # thứ Hai đầu tiên của năm 2010: dữ liệu trước mốc dùng để làm dự báo, từ mốc trở đi để chấm


def doc_dien_theo_gio() -> pd.Series:
    """Điện tiêu thụ theo giờ (kWh), NaN ở giờ có dưới 30 phút đo được.

    Cắt từ 00:00 ngày 17/12/2006 (ngày đầu đủ giờ) tới 23:00 Chủ nhật 21/11/2010 (tuần đủ cuối cùng).
    """
    tep = tv.THU_MUC_DU_LIEU / "uci-household-power" / "household_power_consumption.txt"
    df = pd.read_csv(tep, sep=";", na_values="?", usecols=["Date", "Time", "Global_active_power"])
    thoi_gian = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
    phut = pd.Series(df["Global_active_power"].to_numpy(), index=thoi_gian)
    gio = phut.resample("h").mean().where(phut.resample("h").count() >= 30)
    return gio["2006-12-17":"2010-11-21 23:00"].rename("kwh")


def dien_bang_tuan_truoc(chuoi: pd.Series) -> pd.Series:
    """Điền giờ thiếu bằng cùng giờ tuần trước (rồi hai tuần trước) — chỉ nhìn về quá khứ."""
    return chuoi.fillna(chuoi.shift(TAM)).fillna(chuoi.shift(2 * TAM))


def mae(y, du_bao) -> float:
    """Sai số tuyệt đối trung bình, bỏ qua giờ không có số đo thật."""
    y, du_bao = np.asarray(y, dtype=float), np.asarray(du_bao, dtype=float)
    co = ~np.isnan(y)
    return float(np.mean(np.abs(y[co] - du_bao[co])))


# %%
def _khoa_lich(thoi_gian: pd.DatetimeIndex) -> list[np.ndarray]:
    return [thoi_gian.isocalendar().week.to_numpy(), thoi_gian.dayofweek.to_numpy(), thoi_gian.hour.to_numpy()]


def bang_lich(lich_su: pd.Series) -> pd.Series:
    """"Mô hình" bảng lịch: trung bình theo (tuần trong năm, thứ, giờ) — 53 × 7 × 24 = 8.904 tham số."""
    return lich_su.groupby(_khoa_lich(lich_su.index)).mean()


def du_bao_bang_lich(bang: pd.Series, thoi_gian: pd.DatetimeIndex) -> np.ndarray:
    return bang.reindex(pd.MultiIndex.from_arrays(_khoa_lich(thoi_gian))).to_numpy()


def du_bao_tuan_truoc(lich_su: pd.Series, tam: int = TAM) -> np.ndarray:
    """Baseline mùa vụ: giờ này tuần trước. Lịch sử phải đã điền, đủ ít nhất một tuần."""
    return lich_su.iloc[-TAM:].to_numpy()[:tam]


def du_bao_trung_binh_4_tuan(lich_su: pd.Series, tam: int = TAM) -> np.ndarray:
    """Baseline: trung bình cùng giờ của 4 tuần gần nhất."""
    return lich_su.iloc[-4 * TAM:].to_numpy().reshape(4, TAM).mean(axis=0)[:tam]


def du_bao_gio_truoc(lich_su: pd.Series, tam: int = TAM) -> np.ndarray:
    """Baseline ngây thơ: giữ nguyên giờ cuối cùng đã biết."""
    return np.full(tam, lich_su.iloc[-1])


def du_bao_trung_binh(lich_su: pd.Series, tam: int = TAM) -> np.ndarray:
    """Baseline: trung bình mọi giờ đã biết."""
    return np.full(tam, lich_su.mean())


# %%
def du_bao_cuon(chuoi: pd.Series, moc: str = MOC, tam: int = TAM) -> pd.DataFrame:
    """Dự báo cuốn theo tuần: tại mỗi gốc (moc, moc + 1 tuần, …) chỉ dùng dữ liệu TRƯỚC gốc.

    Trả bảng theo giờ: cột `y` (số đo thật, có thể NaN) và một cột cho mỗi phương pháp.
    """
    day_du = dien_bang_tuan_truoc(chuoi)
    goc_dau = pd.Timestamp(moc)
    cac_goc = pd.date_range(goc_dau, chuoi.index[-1] - pd.Timedelta(hours=tam - 1), freq=f"{TAM}h")
    phan = []
    for goc in cac_goc:
        thoi_gian = pd.date_range(goc, periods=tam, freq="h")
        truoc = chuoi.index < goc
        lich_su, lich_su_day_du = chuoi[truoc], day_du[truoc]
        phan.append(pd.DataFrame({
            "goc": goc,
            "y": chuoi.reindex(thoi_gian).to_numpy(),
            "bảng lịch": du_bao_bang_lich(bang_lich(lich_su), thoi_gian),
            "trung bình 4 tuần": du_bao_trung_binh_4_tuan(lich_su_day_du, tam),
            "tuần trước": du_bao_tuan_truoc(lich_su_day_du, tam),
            "trung bình": du_bao_trung_binh(lich_su, tam),
            "giờ trước": du_bao_gio_truoc(lich_su_day_du, tam),
        }, index=thoi_gian))
    return pd.concat(phan)


def danh_gia(chuoi: pd.Series, moc: str = MOC, tam: int = TAM) -> pd.Series:
    """MAE của mọi phương pháp trên phần sau mốc, xếp từ tốt tới kém. Luôn có baseline để so."""
    bang = du_bao_cuon(chuoi, moc, tam)
    return pd.Series({ten: mae(bang["y"], bang[ten]) for ten in bang.columns if ten not in ("goc", "y")},
                     name="MAE").sort_values()


# %%
if __name__ == "__main__":
    chuoi = doc_dien_theo_gio()
    print(f"{len(chuoi)} giờ, thiếu {chuoi.isna().sum()}, trung bình {chuoi.mean():.3f} kWh/giờ")
    print(danh_gia(chuoi).round(3))
