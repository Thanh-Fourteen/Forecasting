# %% [markdown]
# # Buổi 12 — Khử nhiễu, miền tần số, và bộ lọc nhân quả
#
# Bản ĐÃ SỬA. Dữ liệu: UCI Appliances Energy Prediction — cảm biến trong nhà, 10 phút một mẫu.

# %%
from __future__ import annotations

import numpy as np
import pandas as pd
import pywt
from scipy import signal
from statsmodels.tsa.statespace.structural import UnobservedComponents

import tv

FS = 6.0  # số mẫu mỗi giờ (10 phút một mẫu)
TAM = 6  # dự báo 1 giờ tới = 6 bước


def doc_cam_bien() -> pd.DataFrame:
    """Cảm biến 10 phút: điện tiêu thụ thiết bị (Wh), nhiệt độ/độ ẩm phòng khách, nhiệt độ ngoài trời."""
    tep = tv.THU_MUC_DU_LIEU / "uci-appliances-energy" / "energydata_complete.csv"
    df = pd.read_csv(tep, parse_dates=["date"]).set_index("date").asfreq("10min")
    return df[["Appliances", "T2", "RH_2", "T_out"]].astype(float)


# %% [markdown]
# ## Miền tần số

# %%
def pho(y, fs: float = FS, nperseg: int = 2048) -> tuple[np.ndarray, np.ndarray]:
    """Mật độ phổ công suất (Welch). Trả (tần số theo chu kỳ/giờ, công suất). Luôn trừ trung bình trước."""
    y = np.asarray(y, dtype=float)
    return signal.welch(y - np.nanmean(y), fs=fs, nperseg=min(nperseg, y.size))


def cong_suat_quanh(f, P, chu_ky_gio: float, rong: float = 0.05) -> float:
    """Tổng công suất trong dải quanh tần số ứng với chu kỳ đã cho — dùng để đo đỉnh giả do aliasing."""
    f, P = np.asarray(f, dtype=float), np.asarray(P, dtype=float)
    return float(P[np.abs(f - 1 / chu_ky_gio) < rong].sum())


def ha_mau(y, buoc: int = 6, loc_truoc: bool = True) -> np.ndarray:
    """Hạ mẫu. `loc_truoc=True` lọc thông thấp (Butterworth bậc 8, cắt ở 0,8 × Nyquist mới) TRƯỚC khi lấy mẫu —
    không lọc thì thành phần nhanh hơn Nyquist mới gập xuống thành chu kỳ giả (aliasing)."""
    y = np.asarray(y, dtype=float)
    if not loc_truoc:
        return y[::buoc]
    nyquist_moi = FS / buoc / 2
    sos = signal.butter(8, 0.8 * nyquist_moi, btype="low", fs=FS, output="sos")
    return signal.sosfiltfilt(sos, y)[::buoc]  # lọc hai chiều: chỉ dùng khi TIỀN XỬ LÝ cả chuỗi lịch sử


# %% [markdown]
# ## Bộ lọc

# %%
def ma_truoc(y, cua_so: int = 13):
    return pd.Series(np.asarray(y, dtype=float)).rolling(cua_so, min_periods=1).mean().to_numpy()


def ma_giua(y, cua_so: int = 13):
    return pd.Series(np.asarray(y, dtype=float)).rolling(cua_so, center=True, min_periods=1).mean().to_numpy()


def ewma(y, alpha: float = 0.15):
    return pd.Series(np.asarray(y, dtype=float)).ewm(alpha=alpha).mean().to_numpy()


def savitzky_golay(y, cua_so: int = 13, bac: int = 2):
    return signal.savgol_filter(np.asarray(y, dtype=float), cua_so, bac)


def butter_nhan_qua(y, cat: float = 0.05):
    return signal.sosfilt(signal.butter(4, cat, output="sos"), np.asarray(y, dtype=float))


def butter_filtfilt(y, cat: float = 0.05):
    return signal.sosfiltfilt(signal.butter(4, cat, output="sos"), np.asarray(y, dtype=float))


def kalman(y, lam_tron: bool = False, tham_so=None):
    """Mô hình local level. `lam_tron=False` là FILTER (chỉ quá khứ), True là SMOOTHER (dùng cả tương lai).

    `tham_so=None` sẽ ước lượng tham số trên CHÍNH chuỗi đưa vào — tiện nhưng làm cả filter mất tính nhân quả.
    """
    mo_hinh = UnobservedComponents(np.asarray(y, dtype=float), level="local level")
    p = mo_hinh.fit(disp=0).params if tham_so is None else tham_so
    kq = mo_hinh.smooth(p) if lam_tron else mo_hinh.filter(p)
    return (kq.smoothed_state[0] if lam_tron else kq.filtered_state[0])


def tham_so_kalman(y_hoc) -> np.ndarray:
    """Ước lượng tham số Kalman CHỈ trên dữ liệu huấn luyện, rồi dùng lại — giữ tính nhân quả."""
    return UnobservedComponents(np.asarray(y_hoc, dtype=float), level="local level").fit(disp=0).params


def wavelet(y, song="db4", muc: int = 4):
    """Khử nhiễu bằng ngưỡng mềm, ngưỡng phổ quát σ√(2 ln n) với σ = MAD của hệ số chi tiết mịn nhất."""
    y = np.asarray(y, dtype=float)
    he_so = pywt.wavedec(y, song, level=muc)
    sigma = np.median(np.abs(he_so[-1])) / 0.6745
    nguong = sigma * np.sqrt(2 * np.log(y.size))
    lam_sach = [he_so[0]] + [pywt.threshold(c, nguong, mode="soft") for c in he_so[1:]]
    return pywt.waverec(lam_sach, song)[: y.size]


# %% [markdown]
# ## Kiểm tính nhân quả — bài kiểm rẻ nhất để bắt rò rỉ

# %%
def sinh_tin_hieu(n: int = 2000, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Tín hiệu mô phỏng có BIẾT trước sự thật: nhịp ngày (144 bước) + nhịp 6 giờ + nhiễu trắng σ = 1."""
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    that = 10 + 3 * np.sin(2 * np.pi * t / 144) + 1.5 * np.sin(2 * np.pi * t / 36)
    return that, that + rng.normal(0, 1.0, n)


def kiem_nhan_qua(ham_loc, y, so_diem_doi: int = 10, thay_doi: float = 50.0) -> dict[str, float | bool]:
    """Đổi `so_diem_doi` giá trị CUỐI chuỗi rồi so đầu ra ở MỌI mốc trước đó.

    Bộ lọc nhân quả: đầu ra tại t chỉ phụ thuộc y ở thời điểm ≤ t → phần trước không được đổi.
    """
    y = np.asarray(y, dtype=float)
    k0 = y.size - so_diem_doi
    goc = np.asarray(ham_loc(y), dtype=float)
    y_doi = y.copy()
    y_doi[k0:] += thay_doi
    moi = np.asarray(ham_loc(y_doi), dtype=float)
    lech = np.abs(np.nan_to_num(moi[:k0]) - np.nan_to_num(goc[:k0]))
    nguong = max(1e-9, 1e-7 * float(np.nanmax(np.abs(y))))  # dung sai theo thang dữ liệu, chịu sai số dấu phẩy động
    return {"doi_qua_khu": float(lech.max()), "nhan_qua": bool(lech.max() <= nguong),
            "moc_dau_tien_bi_doi": int(np.argmax(lech > nguong)) if lech.max() > nguong else -1}


def tre_pha(z, that, toi_da: int = 40) -> int:
    """Độ trễ (số bước) làm tương quan giữa đầu ra bộ lọc và tín hiệu thật lớn nhất."""
    z = np.nan_to_num(np.asarray(z, dtype=float) - np.nanmean(z))
    that = np.asarray(that, dtype=float) - np.mean(that)
    tuong_quan = [np.corrcoef(z[k:], that[: that.size - k])[0, 1] if k else np.corrcoef(z, that)[0, 1]
                  for k in range(toi_da)]
    return int(np.argmax(tuong_quan))


def bang_bo_loc(y, tin_hieu_that=None, bo_loc=None) -> pd.DataFrame:
    """Bảng so sánh: sai số khử nhiễu (nếu biết tín hiệu thật), trễ pha, và CÓ DÙNG TƯƠNG LAI KHÔNG."""
    bo_loc = bo_loc or bo_loc_mac_dinh(np.asarray(y, dtype=float)[: max(200, len(y) // 3)])
    hang = []
    for ten, ham in bo_loc.items():
        z = np.asarray(ham(y), dtype=float)
        kq = kiem_nhan_qua(ham, y)
        hang.append({"bộ lọc": ten,
                     "RMSE": (float(np.sqrt(np.nanmean((z - np.asarray(tin_hieu_that, dtype=float)) ** 2)))
                              if tin_hieu_that is not None else np.nan),
                     "trễ (bước)": tre_pha(z, tin_hieu_that if tin_hieu_that is not None else y),
                     "dùng tương lai?": not kq["nhan_qua"], "đổi quá khứ": kq["doi_qua_khu"]})
    return pd.DataFrame(hang)


def bo_loc_mac_dinh(y_hoc=None) -> dict:
    """Bộ lọc dùng trong bảng so sánh. Kalman cần tham số ước lượng TRƯỚC trên `y_hoc` để giữ tính nhân quả;
    nếu để None thì tham số được khớp lại trên chính chuỗi đưa vào — chính chỗ này làm filter mất nhân quả."""
    p = None if y_hoc is None else tham_so_kalman(y_hoc)
    return {"MA trailing 13": ma_truoc, "MA centered 13": ma_giua, "EWMA α=0,15": ewma,
            "Savitzky–Golay 13": savitzky_golay, "Butterworth nhân quả": butter_nhan_qua,
            "Butterworth filtfilt": butter_filtfilt,
            "Kalman filter (tham số cố định)": lambda v: kalman(v, False, p),
            "Kalman filter (khớp lại cả chuỗi)": lambda v: kalman(v, False),
            "Kalman smoother": lambda v: kalman(v, True, p), "Wavelet db4": wavelet}


BO_LOC = bo_loc_mac_dinh()


# %% [markdown]
# ## Dùng bộ lọc làm feature: cái giá của rò rỉ

# %%
def danh_gia_feature(y: pd.Series, ham_loc, tam: int = TAM, ty_le_hoc: float = 0.7) -> float:
    """MAE khi dự báo y_{t+tam} bằng hồi quy tuyến tính trên [bộ lọc(y)_t, y_t]. Chấm trên CHUỖI GỐC."""
    y = y.astype(float)
    bang = pd.DataFrame({"loc": np.asarray(ham_loc(y.to_numpy()), dtype=float), "y": y.to_numpy(),
                         "muc_tieu": y.shift(-tam).to_numpy()}, index=y.index).dropna()
    cat = int(len(bang) * ty_le_hoc)
    hoc, kiem = bang.iloc[:cat], bang.iloc[cat:]
    X = np.column_stack([np.ones(len(hoc)), hoc["loc"], hoc["y"]])
    he_so = np.linalg.lstsq(X, hoc["muc_tieu"].to_numpy(), rcond=None)[0]
    du_bao = np.column_stack([np.ones(len(kiem)), kiem["loc"], kiem["y"]]) @ he_so
    return float(np.mean(np.abs(du_bao - kiem["muc_tieu"].to_numpy())))


def gia_cua_ro_ri(y: pd.Series, bo_loc=None) -> pd.DataFrame:
    """MAE của từng bộ lọc dùng làm feature, kèm cột nhân quả — bộ lọc dùng tương lai cho MAE 'đẹp' giả."""
    bo_loc = bo_loc or bo_loc_mac_dinh(y.to_numpy()[: int(len(y) * 0.7)])
    goc = danh_gia_feature(y, lambda v: np.asarray(v, dtype=float))
    hang = [{"feature": "không lọc", "MAE": goc, "so với không lọc (%)": 0.0, "dùng tương lai?": False}]
    for ten, ham in bo_loc.items():
        mae = danh_gia_feature(y, ham)
        hang.append({"feature": ten, "MAE": mae, "so với không lọc (%)": (mae / goc - 1) * 100,
                     "dùng tương lai?": not kiem_nhan_qua(ham, y.to_numpy())["nhan_qua"]})
    return pd.DataFrame(hang)


def cham_tren_muc_tieu_lam_tron(y: pd.Series, ham_loc=None, tam: int = TAM) -> dict[str, float]:
    """Khử nhiễu MỤC TIÊU rồi chấm: sai số nhỏ đi mà mô hình không hề tốt hơn."""
    ham_loc = ham_loc or ma_giua
    y = y.astype(float)
    muc_tieu_tron = pd.Series(ham_loc(y.to_numpy()), index=y.index)
    bang = pd.DataFrame({"y": y, "tron": muc_tieu_tron}).assign(
        mt_goc=lambda d: d["y"].shift(-tam), mt_tron=lambda d: d["tron"].shift(-tam)).dropna()
    cat = int(len(bang) * 0.7)
    hoc, kiem = bang.iloc[:cat], bang.iloc[cat:]
    X = np.column_stack([np.ones(len(hoc)), hoc["y"]])
    he_so = np.linalg.lstsq(X, hoc["mt_goc"].to_numpy(), rcond=None)[0]
    du_bao = np.column_stack([np.ones(len(kiem)), kiem["y"]]) @ he_so
    return {"mae_muc_tieu_goc": float(np.mean(np.abs(du_bao - kiem["mt_goc"].to_numpy()))),
            "mae_muc_tieu_lam_tron": float(np.mean(np.abs(du_bao - kiem["mt_tron"].to_numpy())))}


# %%
if __name__ == "__main__":
    df = doc_cam_bien()
    print(f"{len(df)} mẫu 10 phút, {df.index[0]} → {df.index[-1]}")
    f, P = pho(df["Appliances"])
    print("chu kỳ mạnh nhất (giờ):", round(float(1 / f[np.argmax(P[1:]) + 1]), 2))
    that, mo_phong = sinh_tin_hieu()
    print(bang_bo_loc(mo_phong, that).round(3).to_string(index=False))
    print(gia_cua_ro_ri(df["Appliances"]).round(2).to_string(index=False))
    print(cham_tren_muc_tieu_lam_tron(df["Appliances"]))
