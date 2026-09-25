# %% [markdown]
# # Buổi 24 — Cold start: dự báo 8 tuần đầu của sản phẩm mới
#
# Điểm xuất phát (phần này không có chỗ cố tình sai).
# Dữ liệu: UCI Online Retail II (bán buôn quà tặng ở Anh, 12/2009 → 12/2011, CC BY 4.0).

# %%
from __future__ import annotations

import re

import numpy as np
import pandas as pd

import tv

TUAN = 8                                   # dự báo 8 tuần đầu kể từ tuần bán đầu tiên
SO_MOI = 200                               # 200 sản phẩm ra mắt gần nhất còn đủ 8 tuần dữ liệu
BAT_DAU_ANALOG = pd.Timestamp("2010-03-01")   # mã "xuất hiện" trước mốc này có thể chỉ là mã cũ lúc dữ liệu bắt đầu
CACHE = tv.THU_MUC_DU_LIEU.parent / "cache"

# danh mục đoán từ mô tả: từ khoá đầu tiên (theo thứ tự này) có trong tên hàng; không khớp → "KHAC"
TU_KHOA = ["CANDLE", "BAG", "BOX", "MUG", "CUP", "HOLDER", "DECORATION", "NECKLACE", "BRACELET", "EARRINGS", "RING",
           "CARD", "SIGN", "FRAME", "CUSHION", "WRAP", "MIRROR", "BOTTLE", "CLOCK", "LIGHT", "BOWL", "PLATE", "TIN",
           "TRAY", "NOTEBOOK", "GARLAND", "JAR", "HOOK", "STAND", "CAKE", "PAPER", "WALL ART", "CHOPPING BOARD",
           "PENCIL", "BACKPACK", "RIBBON", "TISSUE", "HEART", "CABINET", "KIT", "HANGER", "DRAWER", "BLACKBOARD",
           "SNOWFLAKE", "BIRD", "CLIP", "STICKER", "NAPKIN", "UMBRELLA", "BUNTING", "PURSE", "TOWEL", "APRON", "BADGE",
           "MAGNET", "DOORMAT", "LANTERN", "VASE", "POT"]


# %% [markdown]
# ## Dữ liệu: bảng sản phẩm và đường bán 8 tuần đầu

# %%
def _giao_dich() -> pd.DataFrame:
    """Dòng bán hợp lệ (số lượng > 0, giá > 0, mã 5 chữ số). Đọc .xlsx mất 1–2 phút → lưu bản gọn vào cache."""
    tep = CACHE / "giao-dich-mo-ta.parquet"
    if tep.exists():
        return pd.read_parquet(tep)
    goc = tv.THU_MUC_DU_LIEU / "uci-online-retail-ii" / "online_retail_II.xlsx"
    k = pd.concat([pd.read_excel(goc, sheet_name=s, usecols=["StockCode", "Description", "Quantity", "InvoiceDate",
                                                               "Price"])
                   for s in ("Year 2009-2010", "Year 2010-2011")])
    k["StockCode"] = k["StockCode"].astype(str)
    k = k[(k["Quantity"] > 0) & (k["Price"] > 0) & k["StockCode"].str.fullmatch(r"\d{5}[A-Za-z]?")]
    k = pd.DataFrame({"ma": k["StockCode"], "mo_ta": k["Description"].astype("string"),
                      "tuan": k["InvoiceDate"].dt.to_period("W-SUN").dt.start_time,
                      "so_luong": k["Quantity"].astype(float), "gia": k["Price"]})
    tep.parent.mkdir(parents=True, exist_ok=True)
    k.to_parquet(tep)
    return k


def danh_muc(mo_ta: str) -> str:
    """Từ khoá đầu tiên của TU_KHOA có trong mô tả (bỏ đuôi S số nhiều): "RED RETROSPOT CAKE STAND" → "STAND"."""
    chu = " " + " ".join(w[:-1] if w.endswith("S") and w[:-1] in TU_KHOA else w
                         for w in re.findall(r"[A-Z]+", str(mo_ta).upper())) + " "
    return next((t for t in TU_KHOA if f" {t} " in chu), "KHAC")


def doc_san_pham() -> tuple[pd.DataFrame, pd.Series]:
    """(bảng sản phẩm, số lượng theo (mã, tuần)). Bảng: ra_mat (thứ Hai của tuần bán đầu tiên), mo_ta, danh_muc,
    gia (giá trung vị trong tuần ra mắt — biết ngay khi ra mắt)."""
    k = _giao_dich()
    sp = k.groupby("ma").agg(ra_mat=("tuan", "min"),
                             mo_ta=("mo_ta", lambda s: s.dropna().mode().iloc[0] if s.notna().any() else ""))
    tuan_dau = k.merge(sp["ra_mat"], left_on="ma", right_index=True)
    sp["gia"] = tuan_dau[tuan_dau["tuan"] == tuan_dau["ra_mat"]].groupby("ma")["gia"].median()
    sp["danh_muc"] = sp["mo_ta"].map(danh_muc)
    ban = k.groupby(["ma", "tuan"])["so_luong"].sum()
    return sp, ban


def duong_ra_mat(ban: pd.Series, ma: str, ra_mat: pd.Timestamp) -> np.ndarray:
    """Số lượng bán 8 tuần đầu (tuần không bán = 0)."""
    tuan = pd.date_range(ra_mat, periods=TUAN, freq="7D")
    return ban.loc[ma].reindex(tuan, fill_value=0.0).to_numpy()


def chia_tap(sp: pd.DataFrame, ban: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(tap_moi, tap_chon): tap_moi = 200 mã ra mắt gần nhất còn đủ 8 tuần trước tuần cuối (tuần cuối chưa trọn);
    tap_chon = mã ra mắt từ 2011 nhưng trước tap_moi — dùng để chọn tham số k, không đụng tap_moi."""
    tuan_cuoi = ban.index.get_level_values("tuan").max()      # tuần 5/12/2011 chưa trọn (dữ liệu hết 9/12)
    du = sp[(sp["ra_mat"] + pd.Timedelta(weeks=TUAN) <= tuan_cuoi) & (sp["ra_mat"] >= BAT_DAU_ANALOG)]
    moi = du.sort_values("ra_mat", kind="stable").tail(SO_MOI)
    chon = du[(du["ra_mat"] >= pd.Timestamp("2011-01-01")) & (du["ra_mat"] < moi["ra_mat"].min())]
    return moi, chon


# %% [markdown]
# ## Ba cách dự báo cho một mã mới

# %%
def nhom_tuong_tu(sp: pd.DataFrame, ra_mat: pd.Timestamp) -> pd.DataFrame:
    """Mã được dùng làm "hàng tương tự" cho một mã ra mắt ngày ra_mat: đã ra mắt từ BAT_DAU_ANALOG, và 8 tuần đầu
    của nó đã KẾT THÚC trước ra_mat (lúc ra mắt ta chỉ biết đường bán đã xong, không biết tương lai của mã khác)."""
    return sp[(sp["ra_mat"] >= BAT_DAU_ANALOG) & (sp["ra_mat"] + pd.Timedelta(weeks=TUAN) <= ra_mat)]


def du_bao_mot_ma(sp: pd.DataFrame, ban: pd.Series, ma: str, cach: str, k: int = 40) -> np.ndarray:
    """Dự báo 8 tuần đầu của mã `ma`, chỉ dùng thông tin có trước tuần ra mắt.
    cach = "tb_danh_muc" | "analog_danh_muc" | "analog_gia"."""
    r = sp.loc[ma]
    if cach == "tb_danh_muc":
        # mức bán trung bình mỗi tuần của các mã cùng danh mục đang bán trong 8 tuần trước ra mắt
        cung = sp.index[(sp["danh_muc"] == r["danh_muc"]) & (sp["ra_mat"] < r["ra_mat"])]
        tuan = ban.index.get_level_values("tuan")
        w = ban[ban.index.get_level_values("ma").isin(cung) & (tuan >= r["ra_mat"] - pd.Timedelta(weeks=TUAN))
                & (tuan < r["ra_mat"])]
        so_ma = w.index.get_level_values("ma").nunique()
        return np.full(TUAN, w.sum() / TUAN / so_ma if so_ma else 0.0)
    nhom = nhom_tuong_tu(sp, r["ra_mat"])
    if cach == "analog_danh_muc":
        cung = nhom[nhom["danh_muc"] == r["danh_muc"]]
        nhom = cung if len(cung) >= 5 else nhom          # danh mục chưa có đủ 5 mã tương tự → cả cửa hàng
    elif cach == "analog_gia":
        xa = np.abs(np.log(nhom["gia"] / r["gia"])).to_numpy()
        nhom = nhom.iloc[np.argsort(xa, kind="stable")[:k]]     # k mã có giá ra mắt gần nhất (theo tỷ lệ)
    else:
        raise ValueError(cach)
    return np.median([duong_ra_mat(ban, m, t) for m, t in nhom["ra_mat"].items()], axis=0)


def danh_gia(sp: pd.DataFrame, ban: pd.Series, tap: pd.DataFrame, cach: str, k: int = 40) -> dict:
    """Chấm trên tổng 8 tuần (lượng cần nhập cho 8 tuần đầu): MAE (món) và tỷ lệ mã dự báo lệch không quá 2 lần."""
    thuc = np.array([duong_ra_mat(ban, m, t).sum() for m, t in tap["ra_mat"].items()])
    du = np.array([du_bao_mot_ma(sp, ban, m, cach, k).sum() for m in tap.index])
    lech = np.abs(np.log((1 + du) / (1 + thuc)))
    return {"mae": float(np.mean(np.abs(du - thuc))), "trong_2_lan": float(np.mean(lech <= np.log(2)))}


def chon_k(sp: pd.DataFrame, ban: pd.Series, tap_chon: pd.DataFrame, cac_k=(10, 20, 40, 80)) -> int:
    """Chọn số mã tương tự k trên tap_chon (ra mắt TRƯỚC tap_moi) — không chọn trên tập báo cáo."""
    return min(cac_k, key=lambda k: danh_gia(sp, ban, tap_chon, "analog_gia", k)["mae"])


if __name__ == "__main__":
    sp, ban = doc_san_pham()
    moi, chon = chia_tap(sp, ban)
    k = chon_k(sp, ban, chon)
    print(len(moi), len(chon), "k =", k)
    for c in ["tb_danh_muc", "analog_danh_muc", "analog_gia"]:
        print(c, danh_gia(sp, ban, moi, c, k))
