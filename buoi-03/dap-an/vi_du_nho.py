# %% [markdown]
# # Buổi 3 — in mọi con số của các ví dụ nhỏ trong tai-lieu.md (không cần dữ liệu tải về)
#
# Chạy trong nền của buổi:
#   cd buoi-03/lab && python lab.py chay ../dap-an/vi_du_nho.py
# Không có phần ngẫu nhiên nên không cần seed.

# %%
from __future__ import annotations

import numpy as np
import pandas as pd

NY = "America/New_York"


def bang_doi_chieu() -> None:
    """Bảng giờ New York ↔ UTC cho hai ngày đổi giờ 2024."""
    print("== 1. Giờ New York -> UTC ==")
    for ngay in ("2024-03-10", "2024-11-03"):
        for gio in ("00:00", "01:00", "01:30", "02:00", "02:30", "03:00", "04:00"):
            t = pd.Timestamp(f"{ngay} {gio}")
            ket_qua = []
            for mua_he in (True, False):
                try:
                    a = t.tz_localize(NY, ambiguous=mua_he, nonexistent="raise")
                    ket_qua.append(f"{a.tz_convert('UTC'):%H:%M}Z ({a:%Z})")
                except Exception as e:  # noqa: BLE001
                    ket_qua.append(type(e).__name__)
            print(ngay, gio, sorted(set(ket_qua)))
    print("-- chiều ngược: mỗi giờ UTC là mấy giờ New York --")
    for ngay in ("2024-03-10", "2024-11-03"):
        utc = pd.date_range(f"{ngay} 04:00", f"{ngay} 09:00", freq="30min", tz="UTC")
        print(ngay, [f"{u:%H:%M}Z={u.tz_convert(NY):%H:%M %Z}" for u in utc])
    print("số giờ của hai ngày:",
          len(pd.date_range("2024-03-10", "2024-03-11", freq="h", tz=NY, inclusive="left")),
          len(pd.date_range("2024-11-03", "2024-11-04", freq="h", tz=NY, inclusive="left")))


def numpy_doi_gio() -> None:
    print("\n== 2. NumPy: trừ offset ==")
    gio_ny = np.array(["2024-03-09T20:00", "2024-03-11T20:00"], dtype="datetime64[m]")
    offset = np.array([-5, -4]) * np.timedelta64(1, "h")
    print(gio_ny - offset)
    print("Hà Nội 07:00 ->", np.datetime64("2024-07-01T07:00", "m") - np.timedelta64(7, "h"))


def nhan_khoang() -> None:
    print("\n== 3. closed / label ==")
    s = pd.Series([1, 2, 3, 4], index=pd.date_range("2024-01-01 00:00", periods=4, freq="30min"))
    print("dữ liệu:", dict(zip(s.index.strftime("%H:%M"), s, strict=True)))
    mac_dinh = s.resample("h").sum()
    print("mặc định:", dict(zip(mac_dinh.index.strftime("%H:%M"), mac_dinh, strict=True)))
    phai = s.resample("h", closed="right", label="right").sum()
    print("closed=right,label=right:", dict(zip(phai.index.strftime("%H:%M"), phai, strict=True)))
    phai_trai = s.resample("h", closed="right", label="left").sum()
    print("closed=right,label=left:", dict(zip(phai_trai.index.strftime("%H:%M"), phai_trai, strict=True)))
    # sự kiện ở 9:00, 9:40, 10:00, 10:20
    e = pd.Series([1, 1, 1, 1], index=pd.to_datetime(["2024-01-01 09:00", "2024-01-01 09:40",
                                                      "2024-01-01 10:00", "2024-01-01 10:20"]))
    print("đếm 9:00/9:40/10:00/10:20 mặc định:", e.resample("h").sum().to_dict())
    print("  closed=right,label=right:", e.resample("h", closed="right", label="right").sum().to_dict())
    print("mặc định của ME:", pd.Series(1, index=pd.date_range("2024-01-30", periods=4, freq="D"))
          .resample("ME").sum().to_dict())


def gio_trong() -> None:
    print("\n== 4. Giờ trống ==")
    s = pd.Series([1.0, 2.0, 5.0], index=pd.to_datetime(["2024-01-01 00:10", "2024-01-01 00:50",
                                                          "2024-01-01 02:20"]))
    print("sum :", s.resample("h").sum().to_dict())
    print("mean:", s.resample("h").mean().to_dict())
    print("asfreq:", s.asfreq("h").to_dict())
    luoi = pd.date_range("2024-01-01 00:00", "2024-01-01 04:00", freq="h")
    print("sum + reindex 00–04:", s.resample("h").sum().reindex(luoi, fill_value=0).to_dict())


def ghep_asof() -> None:
    print("\n== 5. merge_asof ==")
    trai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 11:00"])})
    phai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 09:30", "2024-01-01 10:30", "2024-01-01 11:00"]),
                         "gia": [9, 10, 11]})
    print("backward:", pd.merge_asof(trai, phai, on="t")["gia"].tolist())
    print("forward :", pd.merge_asof(trai, phai, on="t", direction="forward")["gia"].tolist())
    print("không lấy trùng:", pd.merge_asof(trai, phai, on="t", allow_exact_matches=False)["gia"].tolist())


def tuong_quan() -> None:
    print("\n== 6. Tương quan, và vì sao ghép lệch đổi dấu ==")
    print("r(1,2,3 ; 2,4,6) =", np.corrcoef([1, 2, 3], [2, 4, 6])[0, 1])
    print("r(1,2,3 ; 6,4,2) =", np.corrcoef([1, 2, 3], [6, 4, 2])[0, 1])
    # khử mùa vụ: trừ trung bình cùng giờ
    print("khử mùa vụ: 5400 - 5000 =", 5400 - 5000)
    mua = np.array([0, 0, 2, 2, 0, 0, 0, 0])            # mm, 8 giờ liên tiếp
    chuyen_du = np.array([-1, -1, 3, 3, -1, -1, -1, -1])  # số chuyến trên/dưới mức thường (trăm chuyến)
    print("ghép đúng r =", round(float(np.corrcoef(mua, chuyen_du)[0, 1]), 3))
    mua_lech = np.roll(mua, 4)  # mưa bị gắn trễ 4 giờ
    print("mưa ghép lệch 4 giờ:", mua_lech.tolist(), "r =", round(float(np.corrcoef(mua_lech, chuyen_du)[0, 1]), 3))


def luoi_743() -> None:
    print("\n== 7. Lưới tháng 3 ==")
    luoi = pd.date_range(pd.Timestamp("2024-03-01 05:00", tz="UTC"), pd.Timestamp("2024-04-01 04:00", tz="UTC"),
                         freq="h", inclusive="left")
    print(len(luoi), "mốc; đầu", luoi[0].tz_convert(NY), "; cuối", luoi[-1].tz_convert(NY))
    print("nếu tính cả mốc cuối:", len(pd.date_range("2024-03-01 05:00", "2024-04-01 04:00", freq="h")))
    print("giờ địa phương tháng 3:", len(pd.date_range("2024-03-01", "2024-04-01", freq="h", tz=NY,
                                                         inclusive="left")))


def dang_dai() -> None:
    print("\n== 8. Dạng dài / rộng ==")
    dai = pd.DataFrame({"unique_id": ["A", "A", "A", "B", "B", "B"],
                        "ds": pd.to_datetime(["2024-03-01 05:00", "2024-03-01 06:00", "2024-03-01 07:00"] * 2,
                                             utc=True),
                        "y": [3, 0, 5, 1, 2, 0]})
    print(dai)
    print(dai.pivot(index="ds", columns="unique_id", values="y"))
    print("sắp xếp chuỗi:", sorted(["1", "2", "10", "100"]))


def dem_gio_moi_ngay() -> None:
    print("\n== 9. value_counts().value_counts() ==")
    gio = pd.Series(pd.to_datetime(["2024-03-09 00:00", "2024-03-09 01:00", "2024-03-09 02:00",
                                    "2024-03-10 00:00", "2024-03-10 01:00",
                                    "2024-03-11 00:00", "2024-03-11 01:00", "2024-03-11 02:00"]))
    moi_ngay = gio.dt.date.value_counts().sort_index()
    print("số giờ mỗi ngày:", {str(k): int(v) for k, v in moi_ngay.items()})
    print("bao nhiêu ngày có k giờ:", {int(k): int(v) for k, v in moi_ngay.value_counts().items()})


if __name__ == "__main__":
    bang_doi_chieu()
    numpy_doi_gio()
    nhan_khoang()
    gio_trong()
    ghep_asof()
    tuong_quan()
    luoi_743()
    dang_dai()
    dem_gio_moi_ngay()
