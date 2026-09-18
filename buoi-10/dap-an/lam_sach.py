# %% [markdown]
# # Buổi 10 — Làm sạch và dữ liệu thiếu
#
# Bản ĐÃ SỬA. Dữ liệu: trạm Nội Bài (NOAA GHCNh, 2024), Open-Meteo Hà Nội (trạm hàng xóm),
# PM2.5 12 trạm Bắc Kinh (UCI).

# %%
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents

import tv

warnings.simplefilter("ignore")

DO_DAI_MOC = "30min"  # bước thời gian gốc của GHCNh tại Nội Bài
NAM = 2024
# Cột đo của GHCNh dùng trong buổi (các cột khác là mã chất lượng/nguồn).
COT_DO = ["temperature", "dew_point_temperature", "relative_humidity", "visibility", "wind_speed"]
# Giá trị trá hình: không phải số đo, mà là mã. visibility 9.999 km = METAR "9999 m" = "≥ 10 km".
TRA_HINH = {"visibility": 9.999, "relative_humidity": 100.0}
# Mã chất lượng GHCNh đáng ngờ. 2/6 = Suspect, 3/7 = Erroneous, 'f' = một đầu vào bị gắn cờ,
# 'o' = ngoài dải. Mã 1/5 = qua mọi kiểm tra; 0/4/9 = CHỈ qua kiểm tra giới hạn thô.
MA_NGHI_NGO = {"2", "3", "6", "7", "f", "o"}
MA_KIEM_SO_SAI = {"0", "4", "9"}


# %% [markdown]
# ## Đọc dữ liệu — và cái bẫy kiểu dữ liệu

# %%
def doc_noi_bai(tep=None) -> pd.DataFrame:
    """GHCNh trạm Nội Bài (VMI0000VVNB) 2024, giữ nguyên cột mã chất lượng.

    BẪY: trong parquet gốc, `relative_humidity` và `visibility` là **chuỗi**, nên `.min()` /
    `.max()` so sánh theo thứ tự chữ cái (RH cho min=100, max=94). Phải ép kiểu số tường minh.
    """
    tep = tep or tv.THU_MUC_DU_LIEU / "ghcnh-noi-bai-2024" / f"GHCNh_VMI0000VVNB_{NAM}.parquet"
    tho = pd.read_parquet(tep)
    bang = pd.DataFrame({"thoi_gian": pd.to_datetime(tho["DATE"])})
    for cot in COT_DO:
        bang[cot] = pd.to_numeric(tho[cot], errors="coerce")
        ma = f"{cot}_Quality_Code"
        bang[f"ma_{cot}"] = tho[ma].astype("string").fillna("") if ma in tho else ""
    return bang.set_index("thoi_gian").sort_index()


def cot_rong(tep=None) -> list[str]:
    """Các cột 100% rỗng trong tệp gốc — 'có cột' không có nghĩa là 'có dữ liệu'."""
    tep = tep or tv.THU_MUC_DU_LIEU / "ghcnh-noi-bai-2024" / f"GHCNh_VMI0000VVNB_{NAM}.parquet"
    tho = pd.read_parquet(tep)
    hau_to = ("_Measurement_Code", "_Quality_Code", "_Report_Type", "_Source_Code", "_Source_Station_ID")
    do = [c for c in tho.columns if not c.endswith(hau_to)]
    return [c for c in do if tho[c].isna().all()]


def doc_hang_xom(tep=None) -> pd.DataFrame:
    """Open-Meteo Hà Nội theo giờ — dùng làm 'trạm hàng xóm' để điền và để kiểm tra chéo."""
    tep = tep or tv.THU_MUC_DU_LIEU / "open-meteo-ha-noi-2023-2024" / "open-meteo-ha-noi-2023-2024.csv"
    bang = pd.read_csv(tep, skiprows=3)
    bang["thoi_gian"] = pd.to_datetime(bang["time"])
    ten = {c: c.split(" (")[0] for c in bang.columns if " (" in c}
    return bang.rename(columns=ten).set_index("thoi_gian").sort_index()[["temperature_2m", "relative_humidity_2m"]]


def doc_bac_kinh(tram=None) -> pd.DataFrame:
    """PM2.5 12 trạm Bắc Kinh (UCI) → bảng rộng, một cột một trạm, chỉ số theo giờ."""
    thu_muc = tv.THU_MUC_DU_LIEU / "uci-beijing-air" / "PRSA_Data_20130301-20170228"
    cot = {}
    for tep in sorted(thu_muc.glob("PRSA_Data_*.csv")):
        ten = tep.name.split("_")[2]
        if tram and ten not in tram:
            continue
        d = pd.read_csv(tep, usecols=["year", "month", "day", "hour", "PM2.5", "TEMP"])
        moc = pd.to_datetime(d[["year", "month", "day", "hour"]])
        cot[ten] = pd.Series(d["PM2.5"].to_numpy(), index=moc)
    return pd.DataFrame(cot).sort_index()


# %% [markdown]
# ## Hai loại thiếu: thiếu MỐC và thiếu GIÁ TRỊ

# %%
def luoi_day_du(bang: pd.DataFrame, buoc: str = DO_DAI_MOC) -> pd.DataFrame:
    """Đưa về lưới thời gian đều. Mốc không có dòng nào sẽ hiện ra thành dòng NaN."""
    luoi = pd.date_range(bang.index.min(), bang.index.max(), freq=buoc)
    return bang.reindex(luoi).rename_axis("thoi_gian")


def thong_ke_thieu(bang: pd.DataFrame, buoc: str = DO_DAI_MOC) -> dict[str, int]:
    """Đếm tách bạch: thiếu mốc (không có dòng) vs thiếu giá trị (có dòng, ô rỗng)."""
    luoi = pd.date_range(bang.index.min(), bang.index.max(), freq=buoc)
    return {"so_moc_ky_vong": len(luoi), "so_moc_co": int(bang.index.nunique()),
            "thieu_moc": int(len(luoi.difference(bang.index))),
            "moc_trung": int(bang.index.duplicated().sum()),
            "thieu_gia_tri": int(bang[COT_DO].isna().sum().sum())}


def do_dai_lo_hong(y: pd.Series) -> pd.Series:
    """Độ dài (số bước) của từng lỗ hổng NaN liên tiếp."""
    thieu = y.isna()
    nhom = (thieu != thieu.shift()).cumsum()[thieu]
    return nhom.groupby(nhom).size().reset_index(drop=True)


# %% [markdown]
# ## Kiểm tra chất lượng: đứng yên, trá hình, cờ chất lượng

# %%
def do_phan_giai(y: pd.Series) -> dict[str, float]:
    """Độ phân giải thực của cảm biến: khoảng cách nhỏ nhất giữa hai giá trị khác nhau.

    Phải kiểm TRƯỚC khi kết luận 'cảm biến đứng yên': nếu số đo chỉ ghi tới 1 °C thì một đêm
    nhiệt độ thật đổi 0,4 °C vẫn hiện ra thành một chuỗi giá trị lặp.
    """
    v = np.sort(y.dropna().unique())
    buoc = np.diff(v)
    return {"số giá trị khác nhau": int(v.size),
            "bước nhỏ nhất": float(buoc.min()) if buoc.size else np.nan,
            "tỷ lệ giá trị nguyên %": round(float((y.dropna() % 1 == 0).mean() * 100), 2)}


def doan_mac_ket(y: pd.Series, toi_thieu: int = 6) -> pd.DataFrame:
    """Các đoạn cảm biến đứng yên (giá trị lặp lại) dài ≥ `toi_thieu` bước."""
    v = y.dropna()
    nhom = (v != v.shift()).cumsum()
    dem = v.groupby(nhom).agg(so_buoc="size", gia_tri="first")
    dau = v.groupby(nhom).apply(lambda s: s.index[0])
    dem["bat_dau"] = dau
    return dem[dem["so_buoc"] >= toi_thieu].sort_values("so_buoc", ascending=False).reset_index(drop=True)


def doan_tra_hinh(bang: pd.DataFrame, tra_hinh: dict | None = None) -> pd.DataFrame:
    """Giá trị trá hình: một con số cụ thể lặp lại bất thường vì nó là MÃ, không phải số đo."""
    tra_hinh = TRA_HINH if tra_hinh is None else tra_hinh
    hang = []
    for cot, gia_tri in tra_hinh.items():
        if cot not in bang:
            continue
        v = bang[cot].dropna()
        hang.append({"cột": cot, "giá trị": gia_tri, "số dòng": int((v == gia_tri).sum()),
                     "tỷ lệ %": round(float((v == gia_tri).mean() * 100), 2)})
    return pd.DataFrame(hang)


def co_nghi_ngo(bang: pd.DataFrame, cot: str) -> pd.Series:
    """Cờ True khi mã chất lượng GHCNh của cột nằm trong nhóm đáng ngờ."""
    ma = bang.get(f"ma_{cot}")
    if ma is None:
        return pd.Series(False, index=bang.index)
    return ma.astype("string").fillna("").isin(MA_NGHI_NGO)


def bao_cao_chat_luong(bang: pd.DataFrame) -> pd.DataFrame:
    """Báo cáo một dòng một cột đo: thiếu, dải giá trị (ép kiểu số!), đoạn đứng yên dài nhất,
    giá trị trá hình, số dòng bị gắn cờ chất lượng."""
    tra = doan_tra_hinh(bang).set_index("cột")
    hang = []
    for cot in [c for c in COT_DO if c in bang]:
        v = pd.to_numeric(bang[cot], errors="coerce")
        ket = doan_mac_ket(v, toi_thieu=2)
        lo = do_dai_lo_hong(v)
        hang.append({
            "cột": cot,
            "thiếu %": round(float(v.isna().mean() * 100), 2),
            "lỗ dài nhất (bước)": int(lo.max()) if len(lo) else 0,
            "min": float(v.min()), "max": float(v.max()),
            "đứng yên dài nhất (bước)": int(ket["so_buoc"].max()) if len(ket) else 0,
            "giá trị đứng yên": float(ket["gia_tri"].iloc[0]) if len(ket) else np.nan,
            "trá hình %": float(tra["tỷ lệ %"].get(cot, 0.0)),
            "cờ nghi ngờ": int(co_nghi_ngo(bang, cot).sum()),
        })
    return pd.DataFrame(hang)


# %% [markdown]
# ## Sáu cách điền — và cờ truy vết

# %%
def dien_ffill(y: pd.Series, **_) -> pd.Series:
    """Giữ giá trị gần nhất trong quá khứ. Nhân quả. Tạo đoạn phẳng nếu lỗ dài."""
    return y.ffill()


def dien_tuyen_tinh(y: pd.Series, **_) -> pd.Series:
    """Nội suy tuyến tính hai phía — DÙNG TƯƠNG LAI."""
    return y.interpolate(method="linear", limit_direction="both")


def dien_spline(y: pd.Series, bac: int = 3, **_) -> pd.Series:
    """Spline bậc 3 — mượt hơn, nhưng vọt lố ở lỗ dài và cũng dùng tương lai."""
    return y.interpolate(method="spline", order=bac, limit_direction="both")


def dien_mua_vu(y: pd.Series, chu_ky: int = 48, **_) -> pd.Series:
    """Lấy giá trị cùng giờ của ngày trước (chu_ky bước). Nhân quả; tốt khi nhịp ngày mạnh."""
    z = y.copy()
    for _ in range(14):  # lùi tối đa 14 ngày
        thieu = z.isna()
        if not thieu.any():
            break
        z = z.where(~thieu, z.shift(chu_ky))
    return z


def dien_trung_binh_gio(y: pd.Series, **_) -> pd.Series:
    """Khí hậu học: trung bình theo (giờ trong ngày) tính trên phần KHÔNG thiếu."""
    gio = y.index.hour * 100 + y.index.minute
    trung_binh = y.groupby(gio).transform("mean")
    return y.fillna(trung_binh)


def dien_kalman(y: pd.Series, chu_ky: int = 48, **_) -> pd.Series:
    """Kalman smoother trên mô hình cấu trúc (xu hướng cục bộ + mùa vụ ngày).

    Dùng `smoother_results.smoothed_forecasts` — KHÔNG dùng `fittedvalues` (đó là dự báo 1 bước).
    """
    mo_hinh = UnobservedComponents(y.to_numpy(float), level="local level", freq_seasonal=[
        {"period": chu_ky, "harmonics": 2}])
    kq = mo_hinh.fit(disp=False, maxiter=50)
    lam_tron = pd.Series(kq.smoother_results.smoothed_forecasts[0], index=y.index)
    return y.fillna(lam_tron)


def dien_hang_xom(y: pd.Series, hang_xom: pd.Series | None = None, **_) -> pd.Series:
    """Hồi quy tuyến tính theo trạm hàng xóm (Open-Meteo), khớp trên phần cả hai cùng có."""
    if hang_xom is None:
        return y.copy()
    x = hang_xom.reindex(y.index).interpolate(limit_direction="both")
    chung = y.notna() & x.notna()
    if chung.sum() < 10:
        return y.copy()
    a, b = np.polyfit(x[chung].to_numpy(float), y[chung].to_numpy(float), 1)
    return y.fillna(pd.Series(a * x.to_numpy(float) + b, index=y.index))


CACH_DIEN = {"ffill": dien_ffill, "tuyến tính": dien_tuyen_tinh, "spline": dien_spline,
             "mùa vụ (ngày trước)": dien_mua_vu, "trung bình theo giờ": dien_trung_binh_gio,
             "Kalman smoother": dien_kalman, "hàng xóm (Open-Meteo)": dien_hang_xom}
NHAN_QUA = {"ffill", "mùa vụ (ngày trước)"}


# %% [markdown]
# ## Đánh giá bằng che nhân tạo: che ĐIỂM và che KHỐI cho kết luận khác nhau

# %%
def che_diem(y: pd.Series, ty_le: float = 0.10, seed: int = 0) -> pd.Series:
    """Che ngẫu nhiên từng điểm (mô phỏng MCAR rải rác)."""
    rng = np.random.default_rng(seed)
    co = np.flatnonzero(y.notna().to_numpy())
    chon = rng.choice(co, size=int(len(co) * ty_le), replace=False)
    z = y.copy()
    z.iloc[chon] = np.nan
    return z


def che_khoi(y: pd.Series, so_buoc: int = 96, so_khoi: int = 5, seed: int = 0) -> pd.Series:
    """Che nguyên khối (mô phỏng cảm biến chết vài ngày). 96 bước 30 phút = 48 giờ."""
    rng = np.random.default_rng(seed)
    z = y.copy()
    for _ in range(so_khoi):
        dau = int(rng.integers(0, max(1, len(y) - so_buoc)))
        z.iloc[dau:dau + so_buoc] = np.nan
    return z


def _mae(that: pd.Series, doan: pd.Series, o_che: pd.Series) -> float:
    lech = (doan[o_che] - that[o_che]).abs()
    return float(lech.mean())


def so_sanh_dien(y: pd.Series, hang_xom: pd.Series | None = None, cach=None, seed: int = 0) -> pd.DataFrame:
    """MAE của từng cách điền trên HAI kiểu che. Phải báo cả hai: thứ hạng đổi giữa lỗ ngắn và lỗ dài."""
    cach = cach or CACH_DIEN
    that = y.dropna()
    kieu = {"che điểm 10%": che_diem(that, 0.10, seed), "che khối 48 giờ": che_khoi(that, 96, 5, seed)}
    hang = []
    for ten_kieu, y_che in kieu.items():
        o_che = that.notna() & y_che.isna()
        for ten, ham in cach.items():
            doan = ham(y_che, hang_xom=hang_xom)
            hang.append({"kiểu che": ten_kieu, "cách điền": ten, "MAE": _mae(that, doan, o_che),
                         "còn thiếu": int(doan[o_che].isna().sum()),
                         "nhân quả": ten in NHAN_QUA})
    return pd.DataFrame(hang)


def bang_xep_hang(bang: pd.DataFrame) -> pd.DataFrame:
    """Xoay bảng so sánh thành: mỗi dòng một cách điền, mỗi cột một kiểu che."""
    rong = bang.pivot(index="cách điền", columns="kiểu che", values="MAE")
    rong["đổi hạng"] = rong.rank().diff(axis=1).iloc[:, -1]
    return rong.sort_values(rong.columns[0])


# %% [markdown]
# ## Pipeline làm sạch: có giới hạn, có cờ, có truy vết

# %%
def lam_sach(bang: pd.DataFrame, cot: str = "temperature", gioi_han: int = 6, mac_ket: int = 36,
             cach=dien_mua_vu, hang_xom: pd.Series | None = None) -> pd.DataFrame:
    """Làm sạch một cột đo, trả bảng có cột giá trị + hai cờ truy vết.

    Quy tắc:
      1. đưa về lưới thời gian đều (thiếu mốc → dòng NaN);
      2. bỏ giá trị bị gắn cờ chất lượng đáng ngờ (`nghi_ngo`);
      3. bỏ giá trị trá hình (mã chứ không phải số đo);
      4. bỏ đoạn cảm biến đứng yên quá lâu (`mac_ket` bước — đặt theo ĐỘ PHÂN GIẢI thật của cảm biến);
      5. CHỈ điền lỗ ngắn (≤ `gioi_han` bước) và đánh dấu `da_dien`; lỗ dài để NaN.
    """
    day_du = luoi_day_du(bang)
    v = pd.to_numeric(day_du[cot], errors="coerce")
    nghi = co_nghi_ngo(day_du, cot)
    if cot in TRA_HINH:
        nghi = nghi | (v == TRA_HINH[cot])
    ket = doan_mac_ket(v, toi_thieu=mac_ket)
    for _, dong in ket.iterrows():
        dau = dong["bat_dau"]
        cuoi = dau + pd.Timedelta(DO_DAI_MOC) * (int(dong["so_buoc"]) - 1)
        nghi.loc[dau:cuoi] = True
    sach = v.where(~nghi)

    thieu = sach.isna()
    nhom = (thieu != thieu.shift()).cumsum()
    do_dai = nhom.map(nhom[thieu].value_counts()).where(thieu, 0)
    dien_duoc = thieu & (do_dai <= gioi_han)

    da_dien = cach(sach, hang_xom=hang_xom)
    ket_qua = sach.where(~dien_duoc, da_dien)
    return pd.DataFrame({cot: ket_qua, "da_dien": dien_duoc & ket_qua.notna(), "nghi_ngo": nghi,
                         "lo_dai_bo_trong": thieu & (do_dai > gioi_han)},
                        index=day_du.index)


def bao_cao_lam_sach(sach: pd.DataFrame, cot: str = "temperature") -> dict[str, float | int]:
    """Tóm tắt để dán vào báo cáo chất lượng dữ liệu."""
    return {"số mốc": int(len(sach)),
            "còn thiếu": int(sach[cot].isna().sum()),
            "đã điền": int(sach["da_dien"].sum()),
            "bị loại vì nghi ngờ": int(sach["nghi_ngo"].sum()),
            "ô trong lỗ dài (để trống có chủ ý)": int(sach["lo_dai_bo_trong"].sum())}


# %% [markdown]
# ## MNAR: thiếu không ngẫu nhiên — điền kiểu gì cũng lệch

# %%
def mo_phong_mnar(n: int = 5000, seed: int = 0, nguong: float = 1.0) -> dict[str, float]:
    """Mô phỏng MNAR: cảm biến tắt khi giá trị vượt ngưỡng (ô nhiễm quá cao → máy báo lỗi).

    Đo độ lệch của trung bình sau khi điền: mọi phương pháp dựa trên dữ liệu quan sát được đều
    kéo giá trị về phía thấp, vì phần bị thiếu **có hệ thống** là phần cao.
    """
    rng = np.random.default_rng(seed)
    moc = pd.date_range("2024-01-01", periods=n, freq="30min")
    that = pd.Series(rng.normal(0, 1, n), index=moc)
    mcar = that.mask(pd.Series(rng.random(n) < 0.1, index=moc))
    mnar = that.mask(that > nguong)  # chỉ mất khi giá trị CAO
    return {"trung bình thật": round(float(that.mean()), 3),
            "sau khi điền, thiếu MCAR": round(float(dien_tuyen_tinh(mcar).mean()), 3),
            "sau khi điền, thiếu MNAR": round(float(dien_tuyen_tinh(mnar).mean()), 3),
            "tỷ lệ thiếu MNAR %": round(float(mnar.isna().mean() * 100), 1)}


def bang_chung_mnar(bang: pd.DataFrame, tram: str = "Dongsi") -> dict[str, float]:
    """Khi một trạm mất dữ liệu, mức PM2.5 của các trạm CÒN LẠI cao hay thấp hơn bình thường?

    Nếu cao hơn rõ rệt thì cơ chế thiếu phụ thuộc chính giá trị bị thiếu → MNAR, và mọi phương
    pháp điền dựa trên dữ liệu quan sát được sẽ **lệch xuống dưới**.
    """
    khac = bang.drop(columns=[tram]).mean(axis=1)
    thieu = bang[tram].isna()
    return {"trạm": tram, "tỷ lệ thiếu %": round(float(thieu.mean() * 100), 2),
            "PM2.5 hàng xóm khi trạm thiếu": round(float(khac[thieu].mean()), 1),
            "PM2.5 hàng xóm khi trạm có": round(float(khac[~thieu].mean()), 1),
            "chênh %": round(float(khac[thieu].mean() / khac[~thieu].mean() - 1) * 100, 1)}


def ty_le_thieu_theo_tram(bang: pd.DataFrame) -> pd.DataFrame:
    """Tỷ lệ thiếu theo trạm và theo tháng — đầu vào cho heatmap lỗ hổng."""
    theo_thang = bang.isna().groupby(bang.index.to_period("M")).mean() * 100
    return theo_thang.round(2)


# %%
if __name__ == "__main__":
    tho = doc_noi_bai()
    print("thống kê thiếu:", thong_ke_thieu(tho))
    print("cột 100% rỗng:", len(cot_rong()))
    print(bao_cao_chat_luong(tho).round(3).to_string(index=False))
    print("độ phân giải nhiệt độ:", do_phan_giai(tho["temperature"]))
    print(doan_mac_ket(tho["temperature"], 36).to_string(index=False))

    hx = doc_hang_xom()["temperature_2m"]
    y = luoi_day_du(tho)["temperature"]
    print(bang_xep_hang(so_sanh_dien(y, hang_xom=hx)).round(3).to_string())

    sach = lam_sach(tho, hang_xom=hx)
    print("sau làm sạch:", bao_cao_lam_sach(sach))

    bk = doc_bac_kinh()
    print("Bắc Kinh:", bk.shape, "thiếu %", round(float(bk.isna().mean().mean() * 100), 2))
    print("MNAR (Bắc Kinh, dữ liệu thật):", bang_chung_mnar(bk))
    print("MNAR (mô phỏng):", mo_phong_mnar())
    print(ty_le_thieu_theo_tram(bk).head(3).to_string())
