# %% [markdown]
# # Tiêm 6 lỗi vào dữ liệu phát cho học viên — GIÁM KHẢO GIỮ, KHÔNG VÀO ZIP
#
# Chạy một lần trước khi phát đề:
#
#     cd lab && env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python \
#         ../giam-khao/tiem_loi.py --ra ../phat/du-lieu
#
# Sinh ra (tất định theo seed):
#   `<ra>/noi-bai.csv`, `<ra>/ha-noi.csv`, `<ra>/tphcm.csv` — dữ liệu BẨN phát cho học viên
#   `giam-khao/dap_an_loi.json`                             — đáp án 6 lỗi để chấm tự động

# %%
from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

import tv

warnings.simplefilter("ignore")

SEED = 2026
COT_DO = ["temperature", "dew_point_temperature", "relative_humidity", "wind_speed"]


def _doc_noi_bai(nam: int) -> pd.DataFrame:
    tho = pd.read_parquet(tv.THU_MUC_DU_LIEU / f"ghcnh-noi-bai-{nam}" / f"GHCNh_VMI0000VVNB_{nam}.parquet")
    bang = pd.DataFrame({"thoi_gian": pd.to_datetime(tho["DATE"])})
    for cot in COT_DO:
        bang[cot] = pd.to_numeric(tho[cot], errors="coerce")
    return bang.set_index("thoi_gian").sort_index()


def _doc_open_meteo(ten: str) -> pd.DataFrame:
    d = pd.read_csv(tv.THU_MUC_DU_LIEU / ten / f"{ten}.csv", skiprows=3)
    d = d.rename(columns={c: c.split(" (")[0] for c in d.columns if " (" in c})
    d["thoi_gian"] = pd.to_datetime(d["time"])
    return d.set_index("thoi_gian").sort_index()[
        ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"]]


def du_lieu_sach() -> dict[str, pd.DataFrame]:
    """Ba nguồn, hai năm, chưa tiêm lỗi."""
    noi_bai = pd.concat([_doc_noi_bai(2024), _doc_noi_bai(2025)]).sort_index()
    noi_bai = noi_bai[~noi_bai.index.duplicated()]
    return {"noi-bai": noi_bai,
            "ha-noi": _doc_open_meteo("open-meteo-ha-noi-2023-2024"),
            "tphcm": _doc_open_meteo("open-meteo-tphcm-2023-2024")}


# %% [markdown]
# ## Sáu lỗi

# %%
def tiem(bang: dict[str, pd.DataFrame], seed: int = SEED) -> tuple[dict[str, pd.DataFrame], list[dict]]:
    """Trả (dữ liệu bẩn, đáp án). Mỗi lỗi có mã, mô tả, và cách kiểm để chấm tự động."""
    rng = np.random.default_rng(seed)
    ra = {k: v.copy() for k, v in bang.items()}
    dap_an: list[dict] = []

    # L1 — ĐỔI ĐƠN VỊ giữa chừng: nhiệt độ Nội Bài từ 2025-04-01 ghi bằng °F
    moc = pd.Timestamp("2025-04-01")
    nb = ra["noi-bai"]
    sau = nb.index >= moc
    nb.loc[sau, "temperature"] = (nb.loc[sau, "temperature"] * 9 / 5 + 32).round(1)
    dap_an.append({"ma": "L1", "loai": "doi_don_vi", "tep": "noi-bai", "cot": "temperature",
                   "tu": str(moc.date()), "den": str(nb.index.max().date()),
                   "mo_ta": "nhiệt độ đổi sang °F từ 2025-04-01 (mức nhảy ~+45, biên độ ×1,8)",
                   "so_dong": int(sau.sum())})

    # L2 — TRẠM ĐỨNG YÊN: độ ẩm TP.HCM kẹt ở một giá trị suốt 9 ngày
    hcm = ra["tphcm"]
    dau = pd.Timestamp("2024-08-05")
    trong = (hcm.index >= dau) & (hcm.index < dau + pd.Timedelta(days=9))
    hcm.loc[trong, "relative_humidity_2m"] = 78.0
    dap_an.append({"ma": "L2", "loai": "cam_bien_dung_yen", "tep": "tphcm", "cot": "relative_humidity_2m",
                   "tu": str(dau.date()), "den": str((dau + pd.Timedelta(days=9)).date()),
                   "mo_ta": "độ ẩm đứng yên ở 78,0% suốt 216 giờ", "so_dong": int(trong.sum())})

    # L3 — LỆCH MÚI GIỜ: Hà Nội từ 2024-06-01 ghi theo giờ địa phương (UTC+7) thay vì UTC
    hn = ra["ha-noi"]
    tu = pd.Timestamp("2024-06-01")
    phan_sau = hn.index >= tu
    chi_so = hn.index.to_series()
    chi_so[phan_sau] = chi_so[phan_sau] + pd.Timedelta(hours=7)
    hn.index = pd.DatetimeIndex(chi_so)
    dap_an.append({"ma": "L3", "loai": "lech_mui_gio", "tep": "ha-noi", "cot": "*",
                   "tu": str(tu.date()), "den": str(hn.index.max().date()),
                   "mo_ta": "mốc thời gian nhảy +7 giờ từ 2024-06-01 (đỉnh nhiệt độ ngày dịch pha)",
                   "so_dong": int(phan_sau.sum())})

    # L4 — DÒNG TRÙNG LẶP: 400 dòng ngẫu nhiên của Nội Bài bị lặp lại
    chon = rng.choice(len(nb), size=400, replace=False)
    lap = nb.iloc[np.sort(chon)]
    ra["noi-bai"] = pd.concat([nb, lap]).sort_index()
    dap_an.append({"ma": "L4", "loai": "dong_trung_lap", "tep": "noi-bai", "cot": "*",
                   "tu": str(nb.index.min().date()), "den": str(nb.index.max().date()),
                   "mo_ta": "400 mốc thời gian xuất hiện hai lần", "so_dong": 400})

    # L5 — NGÀY GIẢ TOÀN 0: 11 ngày rải rác của TP.HCM có mọi số đo = 0
    ngay_0 = pd.to_datetime(["2023-03-17", "2023-05-02", "2023-07-19", "2023-09-28", "2023-12-11",
                             "2024-01-23", "2024-02-29", "2024-05-14", "2024-08-30", "2024-10-06",
                             "2024-11-27"])
    mask = hcm.index.normalize().isin(ngay_0)
    hcm.loc[mask, ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]] = 0.0
    dap_an.append({"ma": "L5", "loai": "ngay_gia_0", "tep": "tphcm", "cot": "temperature_2m",
                   "tu": str(ngay_0.min().date()), "den": str(ngay_0.max().date()),
                   "mo_ta": "11 ngày có mọi số đo bằng 0 (0 °C ở TP.HCM là bất khả thi)",
                   "so_dong": int(mask.sum()), "ngay": [str(d.date()) for d in ngay_0]})

    # L6 — MỘT ĐOẠN BỊ DỜI 1 NGÀY: Nội Bài 2024-09-10 → 2024-10-05 bị gán nhầm nhãn thời gian
    nb2 = ra["noi-bai"]
    doi_tu, doi_den = pd.Timestamp("2024-09-10"), pd.Timestamp("2024-10-05")
    trong_doan = (nb2.index >= doi_tu) & (nb2.index < doi_den)
    gia_tri = nb2.loc[trong_doan, COT_DO].to_numpy()
    nb2.loc[trong_doan, COT_DO] = np.roll(gia_tri, shift=48, axis=0)  # 48 bước 30 phút = 1 ngày
    dap_an.append({"ma": "L6", "loai": "doi_nhan_thoi_gian", "tep": "noi-bai", "cot": "*",
                   "tu": str(doi_tu.date()), "den": str(doi_den.date()),
                   "mo_ta": "đoạn 25 ngày bị dời nhãn 1 ngày (tương quan với trạm khác tụt hẳn, "
                            "đỉnh nhiệt lệch 24 giờ)", "so_dong": int(trong_doan.sum())})

    return ra, dap_an


def ghi(ra: dict[str, pd.DataFrame], dap_an: list[dict], thu_muc: Path, giam_khao: Path) -> dict:
    thu_muc.mkdir(parents=True, exist_ok=True)
    tom_tat = {}
    for ten, bang in ra.items():
        tep = thu_muc / f"{ten}.csv"
        bang.to_csv(tep, index_label="thoi_gian")
        tom_tat[ten] = {"tệp": tep.name, "số dòng": len(bang),
                        "từ": str(bang.index.min()), "đến": str(bang.index.max())}
    (giam_khao / "dap_an_loi.json").write_text(
        json.dumps({"seed": SEED, "so_loi": len(dap_an), "loi": dap_an}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    return tom_tat


# %%
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Tiêm 6 lỗi vào dữ liệu phát cho học viên (giám khảo giữ)")
    ap.add_argument("--ra", default="../phat/du-lieu", help="thư mục ghi dữ liệu bẩn phát cho học viên")
    t = ap.parse_args()
    sach = du_lieu_sach()
    ban, dap_an = tiem(sach)
    tom_tat = ghi(ban, dap_an, Path(t.ra).resolve(), Path(__file__).resolve().parent)
    print(json.dumps(tom_tat, ensure_ascii=False, indent=2))
    for d in dap_an:
        print(f"  {d['ma']} {d['loai']:20s} {d['tep']:8s} {d['so_dong']:6d} dòng — {d['mo_ta']}")
