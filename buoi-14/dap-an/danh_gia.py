# %% [markdown]
# # Buổi 14 — Baseline và chỉ số đánh giá
#
# Bản ĐÃ SỬA. Dữ liệu: 4.227 chuỗi M4 theo ngày (Monash), doanh số UCI Online Retail II.
#
# Buổi này **không** dùng `tv.danh_gia` (đã bỏ khỏi `tv/`): bộ chỉ số là thứ bạn tự viết hôm nay.

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

M = 7      # chu kỳ mùa vụ của dữ liệu ngày M4 (tuần)
TAM = 14   # tầm dự báo chính thức của M4 Daily


# %% [markdown]
# ## Đọc dữ liệu

# %%
def doc_tsf(tep=None) -> dict[str, np.ndarray]:
    """Đọc .tsf của Monash bằng thư viện chuẩn."""
    tep = tep or tv.THU_MUC_DU_LIEU / "monash-m4-daily" / "m4_daily_dataset.tsf"
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


def lay_mau(chuoi: dict[str, np.ndarray], so_chuoi: int = 1000, toi_thieu: int = 200,
            seed: int = 42) -> dict[str, np.ndarray]:
    """Mẫu ngẫu nhiên các chuỗi đủ dài để có cả phần học lẫn phần kiểm."""
    rng = np.random.default_rng(seed)
    du_dai = [t for t, v in chuoi.items() if v.size >= toi_thieu + TAM]
    chon = rng.choice(np.array(du_dai), size=min(so_chuoi, len(du_dai)), replace=False)
    return {t: chuoi[t] for t in chon}


def chia(chuoi: dict[str, np.ndarray], tam: int = TAM) -> tuple[dict, dict]:
    """Cắt `tam` điểm cuối làm phần kiểm — giống đúng cách M4 chấm."""
    return ({t: v[:-tam] for t, v in chuoi.items()}, {t: v[-tam:] for t, v in chuoi.items()})


def doc_ban_le_ngay() -> pd.DataFrame:
    """Doanh số theo (mã hàng × ngày) của Online Retail II — có RẤT NHIỀU ngày bằng 0."""
    cache = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "ban_le_ngay.parquet"
    if cache.exists():
        return pd.read_parquet(cache)
    tep = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "online_retail_II.xlsx"
    khung = pd.concat([pd.read_excel(tep, sheet_name=s) for s in ("Year 2009-2010", "Year 2010-2011")])
    khung = khung[(khung["Quantity"] > 0) & (khung["Price"] > 0)].copy()
    khung["StockCode"] = khung["StockCode"].astype(str)
    khung["ngay"] = pd.to_datetime(khung["InvoiceDate"]).dt.normalize()
    ngay = khung.groupby(["StockCode", "ngay"])["Quantity"].sum().rename("so_luong").reset_index()
    ngay.to_parquet(cache)
    return ngay


def chuoi_ban_le(so_ma: int = 300, toi_thieu: int = 400, seed: int = 0) -> dict[str, np.ndarray]:
    """Mỗi mã hàng một chuỗi ngày ĐẦY ĐỦ (ngày không bán = 0) — nhu cầu gián đoạn thật."""
    bang = doc_ban_le_ngay()
    luoi = pd.date_range(bang["ngay"].min(), bang["ngay"].max(), freq="D")
    dem = bang.groupby("StockCode").size().sort_values(ascending=False)
    rng = np.random.default_rng(seed)
    ung_vien = dem[dem >= 60].index.to_numpy()
    chon = rng.choice(ung_vien, size=min(so_ma, len(ung_vien)), replace=False)
    ra = {}
    for ma in chon:
        v = (bang[bang["StockCode"] == ma].set_index("ngay")["so_luong"]
             .reindex(luoi, fill_value=0.0).to_numpy(float))
        if v.size >= toi_thieu:
            ra[str(ma)] = v
    return ra


# %% [markdown]
# ## Bốn baseline
#
# Mọi baseline nhận chuỗi học và trả dự báo `tam` bước. Chúng khó thắng hơn ta tưởng.

# %%
def bl_trung_binh(y: np.ndarray, tam: int = TAM) -> np.ndarray:
    """Trung bình toàn bộ lịch sử."""
    return np.repeat(float(np.mean(y)), tam)


def bl_naive(y: np.ndarray, tam: int = TAM) -> np.ndarray:
    """Giá trị cuối cùng — tối ưu khi chuỗi là random walk."""
    return np.repeat(float(y[-1]), tam)


def bl_naive_mua_vu(y: np.ndarray, tam: int = TAM, m: int = M) -> np.ndarray:
    """Lặp lại chu kỳ gần nhất. Đây là baseline BẮT BUỘC của cả khoá."""
    mua = y[-m:]
    return np.array([mua[i % m] for i in range(tam)], dtype=float)


def bl_drift(y: np.ndarray, tam: int = TAM) -> np.ndarray:
    """Nối đường thẳng từ điểm đầu tới điểm cuối rồi kéo dài."""
    doc = (y[-1] - y[0]) / (len(y) - 1)
    return y[-1] + doc * np.arange(1, tam + 1)


BASELINE = {"trung bình": bl_trung_binh, "naive": bl_naive,
            "seasonal naive": bl_naive_mua_vu, "drift": bl_drift}


def du_bao_baseline(hoc: dict[str, np.ndarray], tam: int = TAM, m: int = M) -> dict[str, dict[str, np.ndarray]]:
    ra = {}
    for ten, ham in BASELINE.items():
        ra[ten] = {t: (ham(v, tam, m) if ten == "seasonal naive" else ham(v, tam))
                   for t, v in hoc.items()}
    return ra


# %% [markdown]
# ## Bảy chỉ số — tự viết bằng NumPy
#
# Quy ước ghi rõ, vì mỗi thư viện một khác (xem `so_voi_utilsforecast`).

# %%
def mae(y: np.ndarray, d: np.ndarray) -> float:
    """Sai số tuyệt đối trung bình. Dự báo tối ưu MAE là **trung vị** của phân phối dự báo."""
    return float(np.mean(np.abs(y - d)))


def rmse(y: np.ndarray, d: np.ndarray) -> float:
    """Căn bậc hai sai số bình phương trung bình. Tối ưu RMSE là **trung bình**."""
    return float(np.sqrt(np.mean((y - d) ** 2)))


def me(y: np.ndarray, d: np.ndarray) -> float:
    """Sai số trung bình có dấu, sai số = thực tế − dự báo; dương là dự báo thấp. Đo ĐỘ LỆCH, không đo độ chính xác."""
    return float(np.mean(y - d))


def mape(y: np.ndarray, d: np.ndarray) -> float:
    """MAPE theo phần trăm (×100). VÔ HẠN khi có y = 0, và phạt dự báo cao hơn nặng hơn."""
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.abs((y - d) / y)
    return float(np.mean(v) * 100)


def smape(y: np.ndarray, d: np.ndarray) -> float:
    """sMAPE theo quy ước M4: ×200, giá trị trong [0, 200]. KHÔNG thật sự đối xứng."""
    mau = np.abs(y) + np.abs(d)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.where(mau == 0, 0.0, 2 * np.abs(y - d) / mau)
    return float(np.mean(v) * 100)


def wape(y: np.ndarray, d: np.ndarray) -> float:
    """WAPE = tổng |sai số| / tổng |thực tế| (×100). Chuẩn bán lẻ; sống được với y = 0 lẻ tẻ."""
    tong = float(np.sum(np.abs(y)))
    if tong == 0:
        return float("nan")
    return float(np.sum(np.abs(y - d)) / tong * 100)


def _mau_so_scaled(hoc: np.ndarray, m: int, binh_phuong: bool = False) -> float:
    """Mẫu số của MASE/RMSSE: sai số naive mùa vụ TRONG MẪU HỌC (Hyndman & Koehler 2006)."""
    lech = hoc[m:] - hoc[:-m]
    if lech.size == 0:
        return float("nan")
    return float(np.mean(lech ** 2)) if binh_phuong else float(np.mean(np.abs(lech)))


def mase(y: np.ndarray, d: np.ndarray, hoc: np.ndarray, m: int = M) -> float:
    """MASE: MAE chia cho MAE của naive mùa vụ trên phần học. 1,0 = ngang seasonal naive."""
    mau = _mau_so_scaled(hoc, m)
    return float("nan") if not mau else mae(y, d) / mau


def rmsse(y: np.ndarray, d: np.ndarray, hoc: np.ndarray, m: int = M) -> float:
    """RMSSE (M5): RMSE chia cho RMSE của naive mùa vụ trên phần học."""
    mau = _mau_so_scaled(hoc, m, binh_phuong=True)
    return float("nan") if not mau else rmse(y, d) / np.sqrt(mau)


CHI_SO_DON = {"MAE": mae, "RMSE": rmse, "ME": me, "MAPE": mape, "sMAPE": smape, "WAPE": wape}
CHI_SO_SCALED = {"MASE": mase, "RMSSE": rmsse}


def danh_gia(kiem: dict[str, np.ndarray], du_bao: dict[str, dict[str, np.ndarray]],
             hoc: dict[str, np.ndarray], m: int = M, gop: str = "trung vị") -> pd.DataFrame:
    """Bảng 8 chỉ số × các mô hình, gộp qua nhiều chuỗi.

    `gop`: "trung vị" (bền với chuỗi cực đoan) hoặc "trung bình" (M4 dùng trung bình).
    Trả cả hai thì tốt nhất — chúng có thể xếp hạng khác nhau.
    """
    hang = []
    for ten_mo_hinh, d in du_bao.items():
        dong = {"mô hình": ten_mo_hinh}
        gia_tri = {k: [] for k in list(CHI_SO_DON) + list(CHI_SO_SCALED)}
        for t, that in kiem.items():
            doan = d[t]
            for k, ham in CHI_SO_DON.items():
                gia_tri[k].append(ham(that, doan))
            for k, ham in CHI_SO_SCALED.items():
                gia_tri[k].append(ham(that, doan, hoc[t], m))
        for k, v in gia_tri.items():
            arr = np.array(v, dtype=float)
            huu_han = arr[np.isfinite(arr)]
            dong[k] = float(np.median(huu_han) if gop == "trung vị" else np.mean(huu_han))
            dong[f"{k}_vô hạn"] = int(np.sum(~np.isfinite(arr)))
        hang.append(dong)
    bang = pd.DataFrame(hang)
    return bang[["mô hình", *CHI_SO_DON, *CHI_SO_SCALED,
                 *[c for c in bang.columns if c.endswith("_vô hạn") and bang[c].sum() > 0]]]


def xep_hang(bang: pd.DataFrame) -> pd.DataFrame:
    """Thứ hạng của từng mô hình theo từng chỉ số (1 = tốt nhất). ME xếp theo |ME|."""
    ra = bang[["mô hình"]].copy()
    for cot in list(CHI_SO_DON) + list(CHI_SO_SCALED):
        v = bang[cot].abs() if cot == "ME" else bang[cot]
        # chỉ số không tính được (vd MAPE khi mọi chuỗi đều có số 0) → hạng rỗng, KHÔNG bịa hạng
        ra[cot] = v.rank(method="min").astype("Int64")
    return ra


# %% [markdown]
# ## Đối chiếu với thư viện chuẩn — và cái bẫy quy ước

# %%
def _dang_dai(kiem: dict[str, np.ndarray], du_bao: dict[str, np.ndarray],
              hoc: dict[str, np.ndarray], ten: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    hang_kiem, hang_hoc = [], []
    for t, that in kiem.items():
        n_hoc = len(hoc[t])
        moc = pd.date_range("2000-01-01", periods=n_hoc + len(that), freq="D")
        hang_hoc.append(pd.DataFrame({"unique_id": t, "ds": moc[:n_hoc], "y": hoc[t]}))
        hang_kiem.append(pd.DataFrame({"unique_id": t, "ds": moc[n_hoc:], "y": that, ten: du_bao[t]}))
    return pd.concat(hang_kiem, ignore_index=True), pd.concat(hang_hoc, ignore_index=True)


def so_voi_utilsforecast(kiem: dict[str, np.ndarray], du_bao: dict[str, np.ndarray],
                         hoc: dict[str, np.ndarray], m: int = M) -> pd.DataFrame:
    """So bộ chỉ số tự viết với `utilsforecast.losses` — và GHI RÕ chỗ quy ước khác nhau.

    Đo được (utilsforecast 0.2.16): `smape` trả **tỷ lệ [0; 1]** chứ không phải phần trăm ×200,
    `mape` trả tỷ lệ chứ không phải ×100. MASE và RMSSE thì khớp tuyệt đối.
    """
    from utilsforecast.losses import mae as uf_mae
    from utilsforecast.losses import mape as uf_mape
    from utilsforecast.losses import mase as uf_mase
    from utilsforecast.losses import rmse as uf_rmse
    from utilsforecast.losses import rmsse as uf_rmsse
    from utilsforecast.losses import smape as uf_smape

    ten = "du_bao"
    dai_kiem, dai_hoc = _dang_dai(kiem, du_bao, hoc, ten)
    goi = {"MAE": (uf_mae, {}), "RMSE": (uf_rmse, {}), "MAPE": (uf_mape, {}), "sMAPE": (uf_smape, {}),
           "MASE": (uf_mase, {"seasonality": m, "train_df": dai_hoc}),
           "RMSSE": (uf_rmsse, {"seasonality": m, "train_df": dai_hoc})}
    hang = []
    for k, (ham, thêm) in goi.items():
        thu_vien = float(ham(dai_kiem, models=[ten], **thêm)[ten].mean())
        if k in CHI_SO_DON:
            tu_viet = float(np.mean([CHI_SO_DON[k](kiem[t], du_bao[t]) for t in kiem]))
        else:
            tu_viet = float(np.mean([CHI_SO_SCALED[k](kiem[t], du_bao[t], hoc[t], m) for t in kiem]))
        hang.append({"chỉ số": k, "tự viết": tu_viet, "utilsforecast": thu_vien,
                     "tỷ lệ tự viết / thư viện": tu_viet / thu_vien if thu_vien else np.nan})
    return pd.DataFrame(hang)


# %% [markdown]
# ## Phần dư: chẩn đoán trước khi tin khoảng dự báo

# %%
def phan_du_mua_vu(y: np.ndarray, m: int = M) -> np.ndarray:
    """Phần dư trong mẫu của seasonal naive: e_t = y_t − y_{t−m}."""
    return y[m:] - y[:-m]


def _acf(x: np.ndarray, so_tre: int) -> np.ndarray:
    x = x - np.mean(x)
    mau = float(np.dot(x, x))
    return np.array([float(np.dot(x[k:], x[:-k or None]) / mau) for k in range(1, so_tre + 1)])


def ljung_box(e: np.ndarray, so_tre: int = 14) -> dict[str, float]:
    """Kiểm định Ljung–Box trên phần dư. p nhỏ = còn tự tương quan = mô hình bỏ sót cấu trúc."""
    from scipy import stats
    n = e.size
    r = _acf(e, so_tre)
    q = n * (n + 2) * float(np.sum(r ** 2 / (n - np.arange(1, so_tre + 1))))
    return {"Q": q, "p": float(stats.chi2.sf(q, so_tre)), "số trễ": so_tre}


def chan_doan_phan_du(hoc: dict[str, np.ndarray], m: int = M, so_tre: int = 14) -> pd.DataFrame:
    """Bốn tính chất phải kiểm: trung bình ≈ 0, không tự tương quan, phương sai đều, gần chuẩn."""
    from scipy import stats
    hang = []
    for t, y in hoc.items():
        e = phan_du_mua_vu(y, m)
        if e.size < 4 * so_tre:
            continue
        nua = e.size // 2
        hang.append({
            "chuỗi": t,
            "trung bình": float(np.mean(e)),
            "trung bình / sd": float(np.mean(e) / np.std(e)) if np.std(e) else np.nan,
            "ljung_box_p": ljung_box(e, so_tre)["p"],
            "tỷ lệ phương sai nửa sau / nửa đầu": float(np.var(e[nua:]) / np.var(e[:nua]))
            if np.var(e[:nua]) else np.nan,
            "jarque_bera_p": float(stats.jarque_bera(e).pvalue),
        })
    return pd.DataFrame(hang)


def tom_tat_chan_doan(bang: pd.DataFrame) -> dict[str, float]:
    return {"số chuỗi": len(bang),
            "% còn tự tương quan (Ljung–Box p < 0,05)": round(float((bang["ljung_box_p"] < 0.05).mean() * 100), 1),
            "% phần dư không chuẩn (Jarque–Bera p < 0,05)": round(float((bang["jarque_bera_p"] < 0.05).mean() * 100), 1),
            "% phương sai đổi > 2 lần": round(float(((bang["tỷ lệ phương sai nửa sau / nửa đầu"] > 2) |
                                                     (bang["tỷ lệ phương sai nửa sau / nửa đầu"] < 0.5)).mean() * 100), 1)}


# %% [markdown]
# ## Chỉ số nào thì dự báo nào: MAE ↔ trung vị, RMSE ↔ trung bình

# %%
def toi_uu_theo_chi_so(mau: np.ndarray) -> dict[str, float]:
    """Với một phân phối đã biết, hằng số nào tối thiểu hoá từng chỉ số?"""
    luoi = np.linspace(float(np.min(mau)), float(np.quantile(mau, 0.999)), 2000)
    mae_theo = np.array([np.mean(np.abs(mau - c)) for c in luoi])
    rmse_theo = np.array([np.sqrt(np.mean((mau - c) ** 2)) for c in luoi])
    with np.errstate(divide="ignore", invalid="ignore"):
        mape_theo = np.array([np.mean(np.abs((mau - c) / np.where(mau == 0, np.nan, mau))) for c in luoi])
    return {"trung vị mẫu": float(np.median(mau)), "trung bình mẫu": float(np.mean(mau)),
            "hằng số tối ưu MAE": float(luoi[np.argmin(mae_theo)]),
            "hằng số tối ưu RMSE": float(luoi[np.argmin(rmse_theo)]),
            "hằng số tối ưu MAPE": float(luoi[np.nanargmin(mape_theo)])}


def mau_lech_phai(n: int = 20000, seed: int = 0) -> np.ndarray:
    """Phân phối lognormal — lệch phải như doanh số bán lẻ thật."""
    rng = np.random.default_rng(seed)
    return rng.lognormal(mean=3.0, sigma=0.9, size=n)


# %%
if __name__ == "__main__":
    chuoi = lay_mau(doc_tsf(), 1000)
    hoc, kiem = chia(chuoi)
    du_bao = du_bao_baseline(hoc)
    bang = danh_gia(kiem, du_bao, hoc)
    print("== M4 daily, 1.000 chuỗi, tầm 14, gộp bằng trung vị ==")
    print(bang.round(3).to_string(index=False))
    print(xep_hang(bang).to_string(index=False))

    print("\n== đối chiếu utilsforecast (seasonal naive) ==")
    print(so_voi_utilsforecast(kiem, du_bao["seasonal naive"], hoc).round(4).to_string(index=False))

    print("\n== chẩn đoán phần dư seasonal naive ==")
    print(tom_tat_chan_doan(chan_doan_phan_du(hoc)))

    print("\n== bán lẻ: chuỗi có số 0 ==")
    ban_le = chuoi_ban_le()
    h_bl, k_bl = chia(ban_le)
    bang_bl = danh_gia(k_bl, du_bao_baseline(h_bl), h_bl)
    print(bang_bl.round(3).to_string(index=False))
    print(xep_hang(bang_bl).to_string(index=False))

    print("\n== chỉ số nào thì dự báo nào ==")
    print(toi_uu_theo_chi_so(mau_lech_phai()))
