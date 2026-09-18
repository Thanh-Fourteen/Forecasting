# %% [markdown]
# # Buổi 2 — Quantile, khoảng dự báo, bootstrap
#
# Code chạy được và ra khoảng "95%" trông hợp lý. Đo xem chúng có thật sự phủ 95% không.

# %%
from __future__ import annotations

import numpy as np
import pandas as pd

import tv


def quantile_tu_viet(x, q):
    """Quantile mẫu loại 7 của Hyndman & Fan (1996) — mặc định `method="linear"` của np.quantile.

    Sắp tăng x_(1) ≤ … ≤ x_(n); vị trí h = (n - 1)·q (đếm từ 0); nội suy tuyến tính giữa hai điểm kề.
    """
    x = np.sort(np.asarray(x, dtype=float))
    if x.size == 0:
        raise ValueError("mẫu rỗng")
    q = np.asarray(q, dtype=float)
    if np.any((q < 0) | (q > 1)):
        raise ValueError("q phải trong [0, 1]")
    h = (x.size - 1) * q
    duoi = np.floor(h).astype(int)
    tren = np.minimum(duoi + 1, x.size - 1)
    return x[duoi] + (h - duoi) * (x[tren] - x[duoi])


def khoang_du_bao(x_lich_su, muc: float = 0.95) -> tuple[float, float]:
    """Khoảng dự báo 95% cho một giá trị mới: trung bình ± 1.96 độ lệch chuẩn."""
    x = np.asarray(x_lich_su, dtype=float)
    z = 1.96 if muc == 0.95 else float(np.sqrt(2) * _erfinv(muc))
    return float(x.mean() - z * x.std(ddof=1)), float(x.mean() + z * x.std(ddof=1))


def _erfinv(p: float) -> float:
    from scipy.special import erfinv

    return float(erfinv(p))


def ty_le_phu(y, lo, hi) -> dict[str, float]:
    """Tỷ lệ phủ và tỷ lệ rơi ra từng đuôi — báo cả hai đuôi, không chỉ tổng."""
    y = np.asarray(y, dtype=float)
    return {"phu": float(np.mean((y >= lo) & (y <= hi))),
            "duoi": float(np.mean(y < lo)), "tren": float(np.mean(y > hi))}


# %%
def _chi_so_bootstrap(n: int, so_lan: int, do_dai_khoi: int, rng: np.random.Generator) -> np.ndarray:
    """Chỉ số lấy mẫu lại: do_dai_khoi = 1 là i.i.d.; > 1 là moving block bootstrap (Künsch 1989)."""
    if do_dai_khoi <= 1:
        return rng.integers(0, n, size=(so_lan, n))
    so_khoi = int(np.ceil(n / do_dai_khoi))
    bat_dau = rng.integers(0, n - do_dai_khoi + 1, size=(so_lan, so_khoi))
    return (bat_dau[:, :, None] + np.arange(do_dai_khoi)).reshape(so_lan, -1)[:, :n]


def khoang_tin_cay_trung_binh(x, muc: float = 0.95, so_lan: int = 1999, do_dai_khoi: int | None = None,
                              seed: int = 0) -> tuple[float, float]:
    """Khoảng tin cậy percentile bootstrap cho trung bình: lấy mẫu lại có hoàn lại (Efron 1979)."""
    x = np.asarray(x, dtype=float)
    do_dai = 1 if do_dai_khoi is None else do_dai_khoi
    rng = np.random.default_rng(seed)
    tb = x[_chi_so_bootstrap(x.size, so_lan, do_dai, rng)].mean(axis=1)
    a = (1 - muc) / 2
    lo, hi = np.quantile(tb, [a, 1 - a])
    return float(lo), float(hi)


def ar1(n: int, rho: float, rng: np.random.Generator, trung_binh: float = 0.0) -> np.ndarray:
    """Chuỗi AR(1) dừng: x_t = ρ x_{t-1} + ε_t, ε ~ N(0, 1)."""
    e = rng.normal(size=n)
    x = np.empty(n)
    x[0] = e[0] / np.sqrt(1 - rho**2)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + e[t]
    return x + trung_binh


def ty_le_phu_khoang_tin_cay(rho: float = 0.7, n: int = 200, so_lan_lap: int = 300, seed: int = 2026,
                             do_dai_khoi: int | None = None) -> float:
    """Mô phỏng: bao nhiêu phần trăm khoảng tin cậy 95% chứa trung bình thật (= 0) của AR(1)."""
    rng = np.random.default_rng(seed)
    trung = 0
    for i in range(so_lan_lap):
        lo, hi = khoang_tin_cay_trung_binh(ar1(n, rho, rng), so_lan=999, do_dai_khoi=do_dai_khoi, seed=seed + i)
        trung += lo <= 0 <= hi
    return trung / so_lan_lap


# %%
def doc_luot_thue() -> pd.DataFrame:
    """Lượt thuê xe theo giờ (Capital Bikeshare 2011–2012) kèm cột thời gian."""
    h = pd.read_csv(tv.THU_MUC_DU_LIEU / "uci-bike-sharing" / "hour.csv", parse_dates=["dteday"])
    return h.assign(ds=h["dteday"] + pd.to_timedelta(h["hr"], unit="h"))


def khoang_theo_gio(lich_su: pd.DataFrame, muc: float = 0.95) -> pd.DataFrame:
    """Khoảng dự báo riêng cho mỗi giờ trong ngày, dựng từ lịch sử."""
    return pd.DataFrame([(g, *khoang_du_bao(nhom["cnt"], muc)) for g, nhom in lich_su.groupby("hr")],
                        columns=["hr", "lo", "hi"])


# %%
if __name__ == "__main__":
    h = doc_luot_thue()
    k = khoang_theo_gio(h[h["yr"] == 0])
    moi = h[h["yr"] == 1].merge(k, on="hr")
    print("khoảng theo giờ từ 2011, chấm trên 2012:", ty_le_phu(moi["cnt"], moi["lo"], moi["hi"]))
    print("AR(1) ρ=0.7, n=200 — khoảng tin cậy bootstrap:", ty_le_phu_khoang_tin_cay())
