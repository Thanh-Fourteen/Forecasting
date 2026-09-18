# %% [markdown]
# # Ví dụ số nhỏ và số kiểm lại cho tai-lieu.md buổi 1 (viết lại Phase 6)
#
# In mọi con số của các "Ví dụ số nhỏ" (mục 2, 4.1–4.5) và vài con số đếm trên dữ liệu thật
# (mục 4.4, 4.5, Lab bước 4). Không có ngẫu nhiên — không cần seed.
# Chạy trong lab/: `env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../dap-an/vi_du_nho.py`

# %%
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

DAY = Path(__file__).resolve().parent


def nap_danh_gia():
    spec = importlib.util.spec_from_file_location("dg", DAY / "danh_gia.py")
    dg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dg)
    return dg


# %%
def vi_du_tay() -> None:
    print("== Mục 2: kW -> kWh ==")
    phut = np.array([2.0] * 30 + [0.4] * 30)          # 60 phút, kW
    print("trung bình kW trong giờ:", phut.mean(), "| kWh = tổng(kW × 1/60 giờ):", round((phut / 60).sum(), 4))

    print("== Mục 2: MAE ==")
    y = np.array([1.5, 0.5, 2.0, 1.0])
    f = np.array([1.0, 1.0, 1.0, 1.0])
    print("sai số = thực tế − dự báo:", (y - f).tolist(), "| MAE:", np.mean(np.abs(y - f)))

    print("== Mục 4.1: dự báo vs mục tiêu ==")
    print("đặt theo mục tiêu 2500, bán 1900 -> thừa", 2500 - 1900)

    print("== Mục 4.3: bốn baseline cho 19:00 thứ Ba 5/1/2010 ==")
    T = pd.Timestamp("2010-01-03 23:00")               # giờ cuối cùng đã biết
    dich = pd.Timestamp("2010-01-05 19:00")
    h = int((dich - T) / pd.Timedelta(hours=1))
    print("T =", T, "| đích =", dich, "| h =", h, "| tuần trước =", T + pd.Timedelta(hours=h - 168))
    cung_gio_4_tuan = np.array([1.6, 1.2, 1.4, 1.8])  # 4 tuần trước -> 1 tuần trước (giả định)
    y_T, tb_tat_ca, thuc_te = 0.6, 1.1, 1.7
    du_bao = {"giờ trước": y_T, "trung bình": tb_tat_ca, "tuần trước": cung_gio_4_tuan[-1],
              "trung bình 4 tuần": cung_gio_4_tuan.mean()}
    for ten, v in du_bao.items():
        print(f"  {ten:<18} dự báo {v:.2f}  sai số {thuc_te - v:+.2f}")
    print("h = 100 ->", T + pd.Timedelta(hours=100), "| cùng giờ hôm qua ->", T + pd.Timedelta(hours=76))

    print("== Mục 4.4: nhìn trộm đáp án ==")
    cu = np.array([1.0, 1.4, 1.2])
    dap_an = 2.0
    print("trung thực:", cu.mean(), "sai", dap_an - cu.mean(),
          "| nhìn trộm:", np.append(cu, dap_an).mean(), "sai", round(dap_an - np.append(cu, dap_an).mean(), 4))
    print("tỷ lệ số liệu mới trong ô (3,82 − 2,99)/3,82 =", round((3.82 - 2.99) / 3.82, 3))

    print("== Mục 4.5: độ chi tiết ==")
    y = np.array([2.0, 0.0, 2.0, 0.0])
    for ten, f in {"A": np.ones(4), "B": np.array([2.5, 0.5, 2.5, 0.5])}.items():
        print(f"  cách {ten}: sai số giờ {(y - f).tolist()}, MAE giờ {np.mean(np.abs(y - f))}, "
              f"tổng dự báo {f.sum()}, sai số tổng {y.sum() - f.sum()}")


# %%
def so_du_lieu_that() -> None:
    dg = nap_danh_gia()
    s = dg.doc_dien_theo_gio()
    cuon = dg.du_bao_cuon(s)
    print("== Dữ liệu thật ==")
    print("số gốc:", cuon["goc"].nunique(), "| giờ được chấm:", len(cuon), "| có số đo:", int(cuon["y"].notna().sum()),
          "| không có số đo:", int(cuon["y"].isna().sum()))
    du = cuon.groupby("goc")["y"].apply(lambda x: x.notna().all())
    print("tuần đủ 168/168 giờ:", int(du.sum()), "| tuần thiếu ít nhất 1 giờ:", int((~du).sum()))
    ngay = s.resample("D").sum(min_count=20)
    print("ngày bị để trống khi min_count=20:", int(ngay.isna().sum()))

    # ô của bảng lịch cho tuần 43 (tuần 25/10/2010), thứ Hai 19h: bao nhiêu giờ trước 2010?
    k = dg._khoa_lich(s.index)
    o = s[(k[0] == 43) & (k[1] == 0) & (k[2] == 19)]
    print("ô (tuần 43, thứ Hai, 19h):", [f"{t:%Y-%m-%d}" for t in o.index])

    # Lab bước 4: 8 tuần trước gốc 15/11/2010
    tam = s["2010-09-20":"2010-11-14 23:00"]
    tong = tam.resample("W-SUN").sum(min_count=168)
    tong.index = tong.index - pd.Timedelta(days=6)
    print("8 tuần trước 15/11 (tổng kWh, NaN = tuần thiếu giờ):")
    print(tong.round(1).to_string())
    print("số giờ thiếu mỗi tuần:", tam.isna().resample("W-SUN").sum().tolist())


if __name__ == "__main__":
    vi_du_tay()
    so_du_lieu_that()
