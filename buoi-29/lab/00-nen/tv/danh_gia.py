# BẢN SAO của tools/khung/danh_gia.py — SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/khung/danh_gia.py rồi chạy lại tool.
"""Chỉ số đánh giá dự báo — công thức theo Phụ lục D của khoá.

Quy ước (FPP 5.8): sai số e = y - ŷ (dương = dự báo THẤP hơn thực tế). Mọi hàm nhận mảng 1 chiều
(numpy, list, pandas Series) theo thời gian của MỘT chuỗi; `bang_chi_so` tính cho nhiều chuỗi
dạng dài `unique_id, ds, y`.

Khác biệt cần nhớ với thư viện (đã kiểm, tools/NGHIEN-CUU.md):
    utilsforecast.smape  thang 0–1        smape() ở đây thang 0–200 như FPP / M4
    utilsforecast.mape   tỷ lệ            mape() ở đây là phần trăm
    utilsforecast.bias   ŷ - y            me() ở đây là y - ŷ
    quantile_loss        không nhân 2     pinball(nhan_2=True) = quantile score của FPP 5.9
    scoringrules 0.11 weighted_interval_score (không numba) SAI — wis() ở đây theo Bracher et al. 2021

Module này chỉ cần numpy và pandas; không import module khác của tv.
"""
from __future__ import annotations

import warnings
from collections.abc import Callable, Sequence

import numpy as np
import pandas as pd

__all__ = [
    "mae", "mse", "rmse", "me", "mape", "smape", "wape", "mase", "rmsse",
    "pinball", "winkler", "coverage", "wis", "wis_quantile",
    "crps_mau", "crps_chuan", "brier", "phan_ra_brier", "log_score", "pit_mau",
    "wrmsse", "bang_chi_so",
]


def _mang(x) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if a.ndim != 1:
        raise ValueError(f"cần mảng 1 chiều, nhận shape {a.shape}")
    return a


def _cung_do_dai(*mang: np.ndarray) -> None:
    if len({len(m) for m in mang}) != 1:
        raise ValueError(f"độ dài không khớp: {[len(m) for m in mang]}")


# ---------------------------------------------------------------------------- dự báo điểm


def mae(y, y_hat) -> float:
    """Mean absolute error — tối ưu ở trung vị."""
    y, y_hat = _mang(y), _mang(y_hat)
    _cung_do_dai(y, y_hat)
    return float(np.mean(np.abs(y - y_hat)))


def mse(y, y_hat) -> float:
    y, y_hat = _mang(y), _mang(y_hat)
    _cung_do_dai(y, y_hat)
    return float(np.mean((y - y_hat) ** 2))


def rmse(y, y_hat) -> float:
    """Root mean squared error — tối ưu ở trung bình."""
    return float(np.sqrt(mse(y, y_hat)))


def me(y, y_hat) -> float:
    """Mean error (bias) = mean(y - ŷ). Dương: dự báo thấp có hệ thống."""
    y, y_hat = _mang(y), _mang(y_hat)
    _cung_do_dai(y, y_hat)
    return float(np.mean(y - y_hat))


def mape(y, y_hat) -> float:
    """MAPE theo phần trăm. Có y = 0 thì trả về nan kèm cảnh báo (FPP: 'infinite or undefined')."""
    y, y_hat = _mang(y), _mang(y_hat)
    _cung_do_dai(y, y_hat)
    if np.any(y == 0):
        warnings.warn("MAPE không xác định khi có y = 0 — dùng MASE, RMSSE hoặc WAPE", stacklevel=2)
        return float("nan")
    return float(np.mean(np.abs(100 * (y - y_hat) / y)))


def smape(y, y_hat) -> float:
    """sMAPE thang 0–200 (FPP 5.8). Điểm có y + ŷ = 0 bị bỏ qua. Không nên dùng để chọn mô hình."""
    y, y_hat = _mang(y), _mang(y_hat)
    _cung_do_dai(y, y_hat)
    mau = y + y_hat
    hop_le = mau != 0
    return float(np.mean(200 * np.abs(y - y_hat)[hop_le] / mau[hop_le]))


def wape(y, y_hat) -> float:
    """WAPE = sum|e| / sum|y| (MAD/Mean ratio)."""
    y, y_hat = _mang(y), _mang(y_hat)
    _cung_do_dai(y, y_hat)
    return float(np.sum(np.abs(y - y_hat)) / np.sum(np.abs(y)))


def _mau_so_thang(y_train: np.ndarray, m: int, luy_thua: int, tu_khac_0: bool) -> float:
    if tu_khac_0:
        khac_0 = np.flatnonzero(y_train != 0)
        if len(khac_0) == 0:
            return float("nan")
        y_train = y_train[khac_0[0]:]
    if len(y_train) <= m:
        raise ValueError(f"chuỗi huấn luyện dài {len(y_train)} không đủ cho mùa vụ m={m}")
    sai_phan = y_train[m:] - y_train[:-m]
    return float(np.mean(np.abs(sai_phan) ** luy_thua))


def mase(y, y_hat, y_train, m: int = 1) -> float:
    """MASE: MAE chia cho MAE một bước trong mẫu của (seasonal) naive chu kỳ m (Hyndman & Koehler 2006).

    MASE < 1 KHÔNG có nghĩa thắng seasonal naive trên tập test — chỉ so với sai số trong mẫu.
    """
    mau = _mau_so_thang(_mang(y_train), m, 1, tu_khac_0=False)
    return mae(y, y_hat) / mau


def rmsse(y, y_hat, y_train, m: int = 1, tu_khac_0: bool = False) -> float:
    """RMSSE (FPP 5.8; M5 dùng m=1 và tu_khac_0=True: mẫu số tính từ lần bán khác 0 đầu tiên)."""
    mau = _mau_so_thang(_mang(y_train), m, 2, tu_khac_0=tu_khac_0)
    return float(np.sqrt(mse(y, y_hat) / mau))


def wrmsse(bang: pd.DataFrame, cot_rmsse: str = "rmsse", cot_trong_so: str = "trong_so") -> float:
    """Tổng RMSSE có trọng số — hàm chỉ cộng, người gọi tự dựng trọng số.

    M5 (Competitors' Guide): trọng số theo doanh thu (lượng × giá) 28 ngày cuối tập huấn luyện, tổng = 1
    trong mỗi cấp gộp, và 12 cấp có trọng số bằng nhau — tức w_i = (1/12) · doanh_thu_i / tổng_cấp,
    tổng mọi w_i = 1. Tham chiếu: datasetsforecast.m5.M5Evaluation (tính theo cấp rồi lấy trung bình 12 cấp).
    """
    w = bang[cot_trong_so].to_numpy(dtype=float)
    if np.any(w < 0):
        raise ValueError("trọng số âm")
    return float(np.sum(w * bang[cot_rmsse].to_numpy(dtype=float)))


# ---------------------------------------------------------------------------- quantile, khoảng


def pinball(y, q, tau: float, nhan_2: bool = False) -> float:
    """Pinball loss trung bình cho quantile mức tau. nhan_2=True: quantile score của FPP 5.9."""
    if not 0 < tau < 1:
        raise ValueError("tau phải trong (0, 1)")
    y, q = _mang(y), _mang(q)
    _cung_do_dai(y, q)
    d = y - q
    diem = np.maximum(tau * d, (tau - 1) * d)
    return float(np.mean(diem) * (2 if nhan_2 else 1))


def _interval_score(y: np.ndarray, lo: np.ndarray, hi: np.ndarray, alpha: float) -> np.ndarray:
    if not 0 < alpha < 1:
        raise ValueError("alpha phải trong (0, 1) — khoảng 80% có alpha = 0.2")
    if np.any(lo > hi):
        raise ValueError("cận dưới lớn hơn cận trên (quantile crossing?)")
    return ((hi - lo) + (2 / alpha) * (lo - y) * (y < lo) + (2 / alpha) * (y - hi) * (y > hi))


def winkler(y, lo, hi, alpha: float) -> float:
    """Winkler / interval score trung bình cho khoảng (1 - alpha)."""
    y, lo, hi = _mang(y), _mang(lo), _mang(hi)
    _cung_do_dai(y, lo, hi)
    return float(np.mean(_interval_score(y, lo, hi, alpha)))


def coverage(y, lo, hi) -> float:
    """Tỷ lệ y nằm trong [lo, hi]. Không phải scoring rule — luôn báo kèm độ rộng hoặc Winkler/WIS."""
    y, lo, hi = _mang(y), _mang(lo), _mang(hi)
    _cung_do_dai(y, lo, hi)
    return float(np.mean((y >= lo) & (y <= hi)))


def wis(y, trung_vi, lo: Sequence, hi: Sequence, alphas: Sequence[float]) -> float:
    """Weighted interval score (Bracher, Ray, Gneiting & Reich 2021), trung bình theo thời gian.

    lo, hi: danh sách K mảng (mỗi mảng dài như y), khoảng thứ k có mức alphas[k].
    WIS = (0.5·|y - m| + Σ (α_k/2)·IS_α_k) / (K + 1/2)
    """
    y, m = _mang(y), _mang(trung_vi)
    _cung_do_dai(y, m)
    if not (len(lo) == len(hi) == len(alphas)):
        raise ValueError("lo, hi, alphas phải cùng số khoảng K")
    tong = 0.5 * np.abs(y - m)
    for l_k, h_k, a in zip(lo, hi, alphas, strict=True):
        l_k, h_k = _mang(l_k), _mang(h_k)
        _cung_do_dai(y, l_k, h_k)
        tong = tong + (a / 2) * _interval_score(y, l_k, h_k, a)
    return float(np.mean(tong / (len(alphas) + 0.5)))


def wis_quantile(y, muc: Sequence[float], quantile: np.ndarray) -> float:
    """WIS từ 2K+1 quantile đối xứng quanh 0.5: (1/(2K+1)) Σ 2{1(y ≤ q_τ) - τ}(q_τ - y).

    quantile: mảng shape (len(y), số mức). Bằng wis() khi các mức là α/2, 1-α/2 và 0.5.
    """
    y = _mang(y)
    muc = np.asarray(muc, dtype=float)
    q = np.asarray(quantile, dtype=float)
    if q.shape != (len(y), len(muc)):
        raise ValueError(f"quantile cần shape ({len(y)}, {len(muc)}), nhận {q.shape}")
    if len(muc) % 2 == 0 or not np.isclose(np.sort(muc)[len(muc) // 2], 0.5):
        raise ValueError("cần số lẻ mức quantile, có mức 0.5 ở giữa")
    diem = 2 * ((y[:, None] <= q) - muc[None, :]) * (q - y[:, None])
    return float(np.mean(diem.mean(axis=1)))


# ---------------------------------------------------------------------------- phân phối


def crps_mau(y, mau, uoc_luong: str = "fair") -> float:
    """CRPS từ mẫu dự báo (ensemble / sample path), trung bình theo thời gian.

    mau: shape (len(y), M). Dạng kernel (Gneiting & Raftery 2007): E|X - y| - ½E|X - X'|.
        "nrg"  : ½ · (1/M²) Σ_ij |x_i - x_j|        — coi mẫu là phân phối thực nghiệm (= mặc định "qd"
                                                     của scoringrules 0.11)
        "fair" : ½ · 1/(M(M-1)) Σ_ij |x_i - x_j|    — bản "fair" cho ensemble hữu hạn (Ferro 2014),
                                                     khớp estimator="fair" của scoringrules
    Tính bằng mẫu đã sắp xếp: O(M log M) mỗi thời điểm.
    """
    y = _mang(y)
    x = np.asarray(mau, dtype=float)
    if x.ndim == 1:
        x = x[None, :]
    if x.shape[0] != len(y):
        raise ValueError(f"mau cần shape ({len(y)}, M), nhận {x.shape}")
    so_mau = x.shape[1]
    if uoc_luong not in ("nrg", "fair"):
        raise ValueError("uoc_luong là 'nrg' hoặc 'fair'")
    if uoc_luong == "fair" and so_mau < 2:
        raise ValueError("ước lượng fair cần ít nhất 2 mẫu")
    tuyet_doi = np.mean(np.abs(x - y[:, None]), axis=1)
    xs = np.sort(x, axis=1)
    i = np.arange(1, so_mau + 1)
    # Σ_ij |x_i - x_j| = 2 Σ_i (2i - M - 1) x_(i)
    tong_cap = 2 * np.sum((2 * i - so_mau - 1) * xs, axis=1)
    mau_so = so_mau**2 if uoc_luong == "nrg" else so_mau * (so_mau - 1)
    return float(np.mean(tuyet_doi - 0.5 * tong_cap / mau_so))


def crps_chuan(y, mu, sigma) -> float:
    """CRPS đóng cho dự báo N(mu, sigma²) (Gneiting & Raftery 2007), trung bình theo thời gian."""
    from math import erf, exp, pi, sqrt

    y, mu, sigma = _mang(y), _mang(np.broadcast_to(mu, np.shape(y))), _mang(np.broadcast_to(sigma, np.shape(y)))
    if np.any(sigma <= 0):
        raise ValueError("sigma phải dương")
    z = (y - mu) / sigma
    phi = np.array([exp(-0.5 * v * v) / sqrt(2 * pi) for v in z])
    Phi = np.array([0.5 * (1 + erf(v / sqrt(2))) for v in z])
    return float(np.mean(sigma * (z * (2 * Phi - 1) + 2 * phi - 1 / sqrt(pi))))


def pit_mau(y, mau) -> tuple[np.ndarray, np.ndarray]:
    """PIT từ mẫu dự báo, trả (P_duoi, P_tren) = (F(y⁻), F(y)) theo phân phối thực nghiệm của mẫu.

    Dữ liệu liên tục: hai mảng bằng nhau = giá trị PIT. Dữ liệu đếm (có mẫu trùng y): PIT là một khoảng —
    đưa cả cặp vào ve.pit_histogram để vẽ PIT histogram KHÔNG ngẫu nhiên của Czado, Gneiting & Held (2009).
    """
    y = _mang(y)
    x = np.asarray(mau, dtype=float)
    if x.ndim != 2 or x.shape[0] != len(y):
        raise ValueError(f"mau cần shape ({len(y)}, M), nhận {x.shape}")
    return np.mean(x < y[:, None], axis=1), np.mean(x <= y[:, None], axis=1)


# ---------------------------------------------------------------------------- sự kiện nhị phân


def _xac_suat(p, o) -> tuple[np.ndarray, np.ndarray]:
    p, o = _mang(p), _mang(o)
    _cung_do_dai(p, o)
    if np.any((p < 0) | (p > 1)):
        raise ValueError("xác suất phải trong [0, 1]")
    if not np.all(np.isin(o, (0, 1))):
        raise ValueError("kết quả phải là 0 hoặc 1")
    return p, o


def brier(p, o) -> float:
    """Brier score = mean((p - o)²)."""
    p, o = _xac_suat(p, o)
    return float(np.mean((p - o) ** 2))


def phan_ra_brier(p, o) -> dict[str, float]:
    """Phân rã Murphy (1973) theo các giá trị xác suất khác nhau: BS = REL - RES + UNC.

    Đúng tuyệt đối khi nhóm theo từng giá trị p; nếu p liên tục, làm tròn/chia bin trước.
    """
    p, o = _xac_suat(p, o)
    n, o_tb = len(p), float(np.mean(o))
    rel = res = 0.0
    for gia_tri in np.unique(p):
        nhom = p == gia_tri
        o_k = float(np.mean(o[nhom]))
        rel += nhom.sum() * (gia_tri - o_k) ** 2
        res += nhom.sum() * (o_k - o_tb) ** 2
    return {"brier": brier(p, o), "reliability": rel / n, "resolution": res / n,
            "uncertainty": o_tb * (1 - o_tb)}


def log_score(p, o, eps: float = 0.0) -> float:
    """Log score âm = mean(-ln p(kết quả xảy ra)). p = 0 cho sự kiện xảy ra → inf (không giới hạn)."""
    p, o = _xac_suat(p, o)
    xs = np.where(o == 1, p, 1 - p)
    if eps:
        xs = np.clip(xs, eps, 1)
    with np.errstate(divide="ignore"):
        return float(np.mean(-np.log(xs)))


# ---------------------------------------------------------------------------- nhiều chuỗi


CHI_SO_DIEM: dict[str, Callable] = {"mae": mae, "rmse": rmse, "me": me, "mape": mape,
                                    "smape": smape, "wape": wape}
CHI_SO_THANG: dict[str, Callable] = {"mase": mase, "rmsse": rmsse}


def bang_chi_so(df: pd.DataFrame, cac_mo_hinh: Sequence[str], train: pd.DataFrame | None = None,
                m: int = 1, chi_so: Sequence[str] = ("mae", "rmse", "mase", "rmsse", "wape", "me"),
                cot_id: str = "unique_id", cot_ds: str = "ds", cot_y: str = "y",
                gop: str | None = "mean") -> pd.DataFrame:
    """Bảng chỉ số cho nhiều chuỗi dạng dài.

    df: unique_id, ds, y và một cột dự báo cho mỗi mô hình (các dòng test).
    train: dữ liệu huấn luyện dạng dài — bắt buộc khi có mase/rmsse.
    gop: None → bảng theo chuỗi (chi_so × mô hình); "mean" / "median" → gộp qua các chuỗi.
    """
    la = set(chi_so) - set(CHI_SO_DIEM) - set(CHI_SO_THANG)
    if la:
        raise ValueError(f"chỉ số không hỗ trợ {sorted(la)}")
    can_train = any(c in CHI_SO_THANG for c in chi_so)
    if can_train and train is None:
        raise ValueError("mase/rmsse cần train (dữ liệu huấn luyện dạng dài)")
    thieu = [c for c in [cot_id, cot_ds, cot_y, *cac_mo_hinh] if c not in df.columns]
    if thieu:
        raise ValueError(f"df thiếu cột {thieu}")

    nhom_train = dict(tuple(train.sort_values(cot_ds).groupby(cot_id, sort=False))) if can_train else {}
    dong = []
    for uid, g in df.sort_values(cot_ds).groupby(cot_id, sort=True):
        y = g[cot_y].to_numpy(dtype=float)
        for mo_hinh in cac_mo_hinh:
            y_hat = g[mo_hinh].to_numpy(dtype=float)
            ket_qua = {cot_id: uid, "mo_hinh": mo_hinh}
            for ten in chi_so:
                if ten in CHI_SO_THANG:
                    if uid not in nhom_train:
                        raise ValueError(f"train không có chuỗi {uid!r}")
                    ket_qua[ten] = CHI_SO_THANG[ten](y, y_hat, nhom_train[uid][cot_y].to_numpy(dtype=float), m)
                else:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        ket_qua[ten] = CHI_SO_DIEM[ten](y, y_hat)
            dong.append(ket_qua)
    bang = pd.DataFrame(dong)
    if gop is None:
        return bang
    if gop not in ("mean", "median"):
        raise ValueError("gop là None, 'mean' hoặc 'median'")
    return bang.groupby("mo_hinh", sort=False)[list(chi_so)].agg(gop)
