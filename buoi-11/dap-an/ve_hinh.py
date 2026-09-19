# %% [markdown]
# # Sinh hình cho tai-lieu.md buổi 11 → ../hinh/*.png (150 dpi) và in các con số dùng trong tài liệu

# %%
from __future__ import annotations

import importlib.util
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tv import ve

warnings.simplefilter("ignore")
DAY = Path(__file__).resolve().parent
HINH = DAY.parent / "hinh"
spec = importlib.util.spec_from_file_location("bt", DAY / "bat_thuong.py")
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
M = ve.MAU


def hinh_bon_loai(mo: pd.Series, nhan: dict) -> dict:
    su_kien = bt.dan_nhan(mo)
    fig, ax = plt.subplots(figsize=(10.5, 3.8))
    ax.plot(mo, color=M["xam"], linewidth=0.9, label="chuỗi")
    mau = {"AO (điểm đơn)": M["phu"], "LS (dịch mức)": M["chinh"], "TC (thay đổi tạm)": M["ba"],
           "đổi phương sai": M["bon"]}
    da_ghi = set()
    for _, d in su_kien.iterrows():
        ax.axvline(d["mốc"], color=mau[d["loại"]], linestyle="--", linewidth=1.2,
                   label=d["loại"] if d["loại"] not in da_ghi else None)
        da_ghi.add(d["loại"])
    for _ten, cac_i in nhan.items():
        for i in cac_i:
            ax.plot(mo.index[i], mo.iloc[i], "k*", markersize=9)
    ax.legend(fontsize=8, ncol=5)
    ax.set_ylabel("giá trị")
    ax.set_title("Bốn loại bất thường cần bốn cách phát hiện: sao đen = vị trí cài sẵn, "
                 "vạch màu = loại mà thuật toán gắn")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "bon-loai-bat-thuong.png")
    return {"số sự kiện": len(su_kien),
            "đúng loại": int(bt.danh_gia_nhan(su_kien, nhan, mo)["đúng loại"].sum()),
            "trên tổng": len(bt.danh_gia_nhan(su_kien, nhan, mo))}


def hinh_nguong_toan_chuoi(tong: pd.Series) -> pd.DataFrame:
    bang = bt.so_sanh_bat(tong)
    z, ham = bt.z_score(tong), bt.hampel(tong)
    fig, (a, b) = plt.subplots(2, 1, figsize=(10.5, 4.6), sharex=True)
    a.plot(tong / 1e6, color=M["xam"], linewidth=0.7)
    a.scatter(tong.index[z], tong[z] / 1e6, color=M["phu"], s=18, zorder=3)
    a.set_ylabel("triệu lượt/ngày")
    a.set_title(f"3σ toàn chuỗi: {int(z.sum())} ngày bị gắn cờ, dồn hết vào vùng mức cao", fontsize=9)
    b.plot(tong / 1e6, color=M["xam"], linewidth=0.7)
    b.scatter(tong.index[ham], tong[ham] / 1e6, color=M["chinh"], s=18, zorder=3)
    b.set_ylabel("triệu lượt/ngày")
    b.set_title(f"Hampel cửa sổ trượt ±15 ngày: {int(ham.sum())} ngày, rải đều theo thời gian", fontsize=9)
    fig.suptitle("Ngưỡng TOÀN CHUỖI mù trước chuỗi có xu hướng: mức tham chiếu phải là mức ĐỊA PHƯƠNG",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "nguong-toan-chuoi.png")
    return bang


def hinh_tet(tet: pd.Series) -> dict:
    dinh = bt.dinh_tet(tet)
    z = bt.z_score(tet)
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    a.plot(tet / 1e3, color=M["xam"], linewidth=0.7)
    a.scatter(tet.index[z], tet[z] / 1e3, color=M["phu"], s=14, zorder=3, label="3σ gắn cờ")
    a.scatter(dinh, tet.loc[dinh] / 1e3, facecolors="none", edgecolors="black", s=70, zorder=4,
              label="đỉnh Tết thật")
    a.set_ylabel("nghìn lượt/ngày")
    a.legend(fontsize=8)
    a.set_title("10/10 đỉnh Tết bị gắn cờ là 'ngoại lai'", fontsize=9)
    ngay = pd.DataFrame({"nam": [d.year for d in dinh], "ngay_trong_nam": [d.dayofyear for d in dinh]})
    b.scatter(ngay["nam"], ngay["ngay_trong_nam"], color=M["chinh"], s=45)
    b.set_ylabel("ngày thứ mấy trong năm dương")
    b.set_xlabel("năm")
    b.set_title(f"Đỉnh Tết xê dịch {ngay['ngay_trong_nam'].min()}–{ngay['ngay_trong_nam'].max()} "
                f"(lệch {ngay['ngay_trong_nam'].max() - ngay['ngay_trong_nam'].min()} ngày)", fontsize=9)
    fig.suptitle("Sự kiện THẬT, không phải lỗi: xoá đi là xoá mất thứ đáng dự báo nhất — và STL "
                 "không cứu được vì Tết theo lịch âm", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "tet-khong-phai-ngoai-lai.png")
    return {"đỉnh Tết": [str(d.date()) for d in dinh],
            "ngày trong năm": ngay["ngay_trong_nam"].tolist(),
            "biên độ xê dịch (ngày)": int(ngay["ngay_trong_nam"].max() - ngay["ngay_trong_nam"].min()),
            "bảng mất đỉnh": bt.mat_bao_nhieu_dinh_tet(tet).to_dict("records")}


def hinh_masking_10_so() -> dict:
    """Ví dụ tay mục 4.2: 10 số, một rồi hai ngoại lai; ngưỡng trung bình ± 3σ so với trung vị ± 3·MAD."""
    mot = np.array([10, 12, 11, 13, 12, 50, 11, 12, 13, 12.0])
    hai = mot.copy()
    hai[9] = 60.0
    fig, truc = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    kq = {}
    for ax, v, ten in ((truc[0], mot, "một ngoại lai (50)"), (truc[1], hai, "hai ngoại lai (50 và 60)")):
        tb, s = v.mean(), v.std(ddof=1)
        tv_, mad = np.median(v), 1.4826 * np.median(np.abs(v - np.median(v)))
        ax.plot(np.arange(1, 11), v, "o", color=M["chinh"])
        ax.axhline(tb + 3 * s, color=M["phu"], linestyle="--", label="trung bình + 3σ")
        ax.axhline(tv_ + 3 * mad, color=M["ba"], linestyle=":", label="trung vị + 3·MAD")
        ax.set_title(ten, fontsize=9)
        ax.set_xlabel("vị trí")
        kq[ten] = {"trung bình": round(float(tb), 2), "σ": round(float(s), 2),
                   "ngưỡng 3σ": round(float(tb + 3 * s), 1), "ngưỡng MAD": round(float(tv_ + 3 * mad), 2),
                   "z": [round(float(x), 2) for x in (v - tb) / s]}
    truc[0].set_ylabel("giá trị")
    truc[0].legend(fontsize=8)
    fig.suptitle("Masking trên 10 số: ngoại lai kéo ngưỡng 3σ lên cao hơn chính nó; ngưỡng MAD đứng yên sát dữ liệu",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "masking-10-so.png")
    return kq


def hinh_masking(tong: pd.Series) -> dict:
    kq = bt.masking(tong)
    them = tong.copy()
    them.iloc[len(tong) // 2] = tong.max() * 8
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    for ax, y, ten in ((a, tong, "chuỗi gốc"), (b, them, "thêm MỘT điểm bằng 8× giá trị lớn nhất")):
        tb, sd = y.mean(), y.std()
        co = bt.z_score(y)
        ax.plot(tong / 1e6, color=M["xam"], linewidth=0.6)
        ax.axhline(tb / 1e6, color="black", linewidth=1, label="trung bình")
        ax.axhline((tb + 3 * sd) / 1e6, color=M["phu"], linestyle="--", linewidth=1.2, label="ngưỡng 3σ")
        ax.scatter(y.index[co], tong[co] / 1e6, color=M["phu"], s=16, zorder=3)
        ax.set_ylim(0, (tong.max() * 1.15) / 1e6)
        ax.set_ylabel("triệu lượt/ngày")
        ax.legend(fontsize=8)
        ax.set_title(f"{ten}: {int(co.sum())} ngày bị gắn cờ", fontsize=9)
    fig.suptitle("Masking: thêm một ngoại lai làm ngưỡng 3σ dâng lên và CHE các ngoại lai khác "
                 "(16 → 5 ngày); Hampel không đổi (121 → 123)", fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "masking.png")
    return kq


def hinh_diem_gay(hk: pd.Series) -> dict:
    moc = bt.diem_gay_on_dinh(hk)
    tho = bt.diem_gay(hk, log=False)
    quet = bt.quet_penalty(hk)
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.5))
    a.plot(hk / 1e6, color=M["xam"], linewidth=1.1)
    for m in tho:
        a.axvline(m, color=M["phu"], alpha=0.25, linewidth=0.8)
    for m in moc:
        a.axvline(m, color=M["chinh"], linewidth=1.8)
    a.set_ylabel("triệu hành khách/tháng")
    a.set_title(f"Cam: {len(tho)} điểm gãy khi chạy trên mức thô. Xanh: {len(moc)} điểm khi lấy log trước",
                fontsize=9)
    b.plot(quet["pen/log n"], quet["số điểm gãy"], "o-", color=M["chinh"], markersize=3)
    b.set_xlabel("penalty / log n")
    b.set_ylabel("số điểm gãy")
    b.set_title("Elbow: 2 điểm gãy giữ nguyên trong khoảng penalty 1–4·log n", fontsize=9)
    fig.suptitle("PELT: hai quyết định quyết định kết quả — biến đổi trước khi chạy, và chọn penalty",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "diem-gay-pelt.png")
    return {"điểm gãy ổn định": [str(pd.Timestamp(m).date()) for m in moc],
            "số điểm gãy trên mức thô": len(tho),
            "độ lớn": bt.do_lon_gay(hk, moc).to_dict("records")}


def hinh_covid(hk: pd.Series) -> pd.DataFrame:
    bang = bt.ba_cach_xu_ly_covid(hk)
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    a.plot(hk / 1e6, color=M["xam"], linewidth=1.1)
    a.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2021-06-30"), color=M["phu"], alpha=0.15)
    a.axvline(pd.Timestamp("2023-01-01"), color="black", linestyle="--", linewidth=1)
    a.set_ylabel("triệu hành khách/tháng")
    a.set_title("Vùng cam: COVID. Vạch đen: mốc chia học/kiểm", fontsize=9)
    b.barh(bang["cách xử lý"], bang["MAPE %"], color=[M["phu"], M["chinh"], M["ba"]])
    for i, v in enumerate(bang["MAPE %"]):
        b.text(v + 0.3, i, f"{v:.2f}%", va="center", fontsize=8)
    b.set_xlabel("MAPE trên 12 tháng 2023 (%)")
    b.set_title("Cùng dữ liệu, ba cách xử lý, sai số chênh gần 3 lần", fontsize=9)
    fig.suptitle("COVID là ngoại lai hay điểm gãy? Câu trả lời khác nhau đổi hẳn kết quả dự báo",
                 fontsize=10, fontweight="bold")
    fig.tight_layout()
    ve.luu_hinh(fig, HINH / "ba-cach-covid.png")
    return bang


if __name__ == "__main__":
    tong, tet, hk = bt.doc_tong_vi(), bt.doc_bai_tet(), bt.doc_hang_khong()
    mo, nhan = bt.sinh_chuoi_co_loi()
    with ve.phong_cach():
        print("bốn loại", hinh_bon_loai(mo, nhan))
        print(hinh_nguong_toan_chuoi(tong).to_string(index=False))
        print("tết", hinh_tet(tet))
        print("masking 10 số", hinh_masking_10_so())
        print("masking", hinh_masking(tong))
        print("điểm gãy", hinh_diem_gay(hk))
        print(hinh_covid(hk).to_string(index=False))
    print("masking:", bt.masking(tong))
    print("xong:", sorted(p.name for p in HINH.glob("*.png")))
