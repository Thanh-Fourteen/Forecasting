"""Mọi ví dụ của Phụ lục A chạy trên pandas 3 (môi trường buổi 3)."""
import warnings
import zoneinfo
from datetime import datetime

import numpy as np
import pandas as pd


def H(t):
    print(f"\n===== {t}")


H("numpy array")
a = np.array([7, 5, 9, 6, 8])
print(repr(a * 2), repr(a + 1), repr(a > 6), a.mean(), a[a > 6])
b = np.array([7.0, np.nan, 9.0])
print(b.mean(), np.nanmean(b))

H("rng")
rng = np.random.default_rng(42)
print(rng.normal(size=3).round(4))
rng = np.random.default_rng(42)
print(rng.normal(size=3).round(4))
rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=5))

H("quantile")
x = [5, 6, 6, 7, 7, 8, 8, 9, 9, 12]
print(np.quantile([1, 2, 3, 4], 0.25), np.quantile([1, 2, 3, 4], 0.25, method="median_unbiased"),
      np.quantile([1, 2, 3, 4], 0.25, method="inverted_cdf"))
print(np.quantile(x, 0.8), np.quantile(x, 0.8, method="inverted_cdf"))
print(np.quantile(x, 0.75), np.quantile(x, 0.75, method="inverted_cdf"))
print(pd.Series(x).quantile(0.75))

H("to_datetime / Timestamp")
t = pd.Timestamp("2024-03-10 19:30")
print(repr(t), t.hour, t.dayofweek, t.day_name())
s = pd.to_datetime(pd.Series(["2024-01-05 08:00", "2024-01-06 09:30"]))
print(s)
print(s.dt.hour.tolist(), s.dt.dayofweek.tolist())
print(pd.to_datetime("05/01/2024"), pd.to_datetime("05/01/2024", dayfirst=True))
print(pd.to_datetime("2024-01-05 08:00", format="%Y-%m-%d %H:%M"))
try:
    pd.to_datetime(pd.Series(["2024-01-05", "không rõ"]))
except Exception as e:
    print(type(e).__name__, str(e)[:120])
print(pd.to_datetime(pd.Series(["2024-01-05", "không rõ"]), errors="coerce").tolist())

H("date_range")
print(pd.date_range("2024-01-01", periods=3, freq="h"))
print(pd.date_range("2024-01-01", periods=3, freq="D"))
print(pd.date_range("2024-01-01", periods=3, freq="MS"))
print(pd.date_range("2024-01-01", periods=3, freq="ME"))
print(pd.date_range("2024-01-01", periods=3, freq="W-MON"))
print(pd.date_range("2024-01-01", periods=2, freq="15min"))

H("series with index, loc")
y = pd.Series([5, 7, 6, 9, 8, 10], index=pd.date_range("2024-01-01", periods=6, freq="D"))
print(y)
print(y.loc["2024-01-03":"2024-01-04"])
print(y.loc["2024-01"].sum())

H("resample")
y = pd.Series(range(6), index=pd.date_range("2024-01-01 00:00", periods=6, freq="h"))
print(y)
print(y.resample("2h").sum())
print(y.resample("2h", closed="right", label="right").sum())
d = pd.Series([1.0, 2, 3, 4], index=pd.to_datetime(["2024-01-30", "2024-01-31", "2024-02-01", "2024-02-02"]))
print(d.resample("ME").sum())
print(d.resample("MS").sum())
# min_count
z = pd.Series([1.0, np.nan, np.nan, np.nan], index=pd.date_range("2024-01-01", periods=4, freq="h"))
print(z.resample("2h").sum().tolist(), z.resample("2h").sum(min_count=1).tolist())
# mean vs sum
nhiet = pd.Series([20.0, 22, 24, 26], index=pd.date_range("2024-01-01", periods=4, freq="h"))
print(nhiet.resample("2h").mean().tolist())

H("shift diff rolling")
x = pd.Series([0.0, 1, 2, 3, 4, 5], index=pd.date_range("2024-01-01", periods=6, freq="h"))
print(x.shift(1).tolist())
print(x.shift(-1).tolist())
print(x.diff().tolist())
print(x.rolling(3).mean().tolist())
print(x.rolling(3, min_periods=1).mean().tolist())
print(x.rolling(3, center=True).mean().tolist())
print(x.rolling(3).mean().shift(1).tolist())
print(x.rolling("2h").sum().tolist())
print(x.rolling("2h", closed="both").sum().tolist())
print(x.rolling("2h", closed="left").sum().tolist())
# time window with gap
g = pd.Series([1.0, 2, 3], index=pd.to_datetime(["2024-01-01 00:00", "2024-01-01 01:00", "2024-01-01 05:00"]))
print(g.rolling(2).sum().tolist(), g.rolling("2h").sum().tolist())

H("ewm")
print(pd.Series([1.0, 2, 3]).ewm(alpha=0.5).mean().round(3).tolist())
print(pd.Series([1.0, 2, 3]).ewm(alpha=0.5, adjust=False).mean().tolist())

H("merge_asof")
trai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 10:05"])})
phai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 10:03"]), "v": [1, 2]})
print(pd.merge_asof(trai, phai, on="t"))
print(pd.merge_asof(trai, phai, on="t", allow_exact_matches=False))
don = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:07"])})
gia = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:05", "2024-01-01 10:10"]), "gia": [100, 105]})
print(pd.merge_asof(don, gia, on="t"))
print(pd.merge(don, gia, on="t", how="left"))
try:
    pd.merge_asof(trai, phai.sort_values("t", ascending=False), on="t")
except Exception as e:
    print(type(e).__name__, e)
print(pd.merge_asof(trai, phai, on="t", tolerance=pd.Timedelta("1min")))

H("tz")
t = pd.Timestamp("2024-07-01 12:00")
print(repr(t), t.tz)
ta = t.tz_localize("Asia/Ho_Chi_Minh")
print(repr(ta))
print(repr(ta.tz_convert("UTC")))
print(pd.Timestamp("2024-07-01 12:00", tz="Asia/Ho_Chi_Minh").tz_convert("UTC"))
print(repr(t.tz_localize("UTC")))
print(zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh").utcoffset(datetime(1970, 1, 1)))
print(zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh").utcoffset(datetime(2024, 1, 1)))
print(pd.date_range("2024-03-10 00:00", periods=4, freq="h", tz="America/New_York"))
print(pd.date_range("2024-11-03 00:00", periods=4, freq="h", tz="America/New_York"))
# so gio trong ngay DST
ny = pd.date_range("2024-03-10", "2024-03-11", freq="h", tz="America/New_York", inclusive="left")
print("so gio 10/3:", len(ny))
ny = pd.date_range("2024-11-03", "2024-11-04", freq="h", tz="America/New_York", inclusive="left")
print("so gio 3/11:", len(ny))
tt = pd.Series(pd.to_datetime(["2024-11-03 01:30"]))
try:
    tt.dt.tz_localize("America/New_York")
except Exception as e:
    print(type(e).__name__, e)
print(tt.dt.tz_localize("America/New_York", ambiguous=np.array([True])).tolist())
print(tt.dt.tz_localize("America/New_York", ambiguous=np.array([False])).tolist())
print(tt.dt.tz_localize("America/New_York", ambiguous="NaT").tolist())
try:
    pd.Series(pd.to_datetime(["2024-03-10 02:30"])).dt.tz_localize("America/New_York")
except Exception as e:
    print(type(e).__name__, e)
print(pd.Series(pd.to_datetime(["2024-03-10 02:30"])).dt.tz_localize(
    "America/New_York", nonexistent="shift_forward").tolist())
print(pd.Series(pd.to_datetime(["2024-03-10 02:30"])).dt.tz_localize(
    "America/New_York", nonexistent="NaT").tolist())
# infer on a sequence
seq = pd.Series(pd.to_datetime(["2024-11-03 00:30", "2024-11-03 01:30", "2024-11-03 01:30", "2024-11-03 02:30"]))
print(seq.dt.tz_localize("America/New_York", ambiguous="infer").tolist())
# UTC to local then hour
u = pd.Series(pd.to_datetime(["2024-01-01 17:00", "2024-01-01 18:00"])).dt.tz_localize("UTC")
print(u.dt.hour.tolist(), u.dt.tz_convert("Asia/Ho_Chi_Minh").dt.hour.tolist(),
      u.dt.tz_convert("Asia/Ho_Chi_Minh").dt.date.tolist())
print(type(ta.tz))
# tz-naive vs aware compare error
try:
    print(t < ta)
except Exception as e:
    print(type(e).__name__, e)

H("long wide")
rong = pd.DataFrame({"ds": pd.date_range("2024-01-01", periods=2, freq="D"), "HN": [10, 11], "HCM": [20, 21]})
print(rong)
dai = rong.melt(id_vars="ds", var_name="unique_id", value_name="y")[["unique_id", "ds", "y"]]
print(dai)
print(dai.pivot(index="ds", columns="unique_id", values="y"))

H("pandas3 specifics")
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    df["a"][df["b"] > 4] = 100
    print([type(x.message).__name__ for x in w], [str(x.message)[:100] for x in w])
print(df["a"].tolist())
df.loc[df["b"] > 4, "a"] = 100
print(df["a"].tolist())
print(pd.Series(["a", "b"]).dtype)
print(pd.to_datetime(pd.Series(["2024-01-01"])).dtype)
for f in ["H", "T", "M"]:
    try:
        pd.date_range("2024-01-01", periods=2, freq=f)
        print(f, "ok")
    except Exception as e:
        print(f, type(e).__name__, e)
try:
    pd.Series([1.0, np.nan]).fillna(method="ffill")
except Exception as e:
    print(type(e).__name__, e)
print(pd.Series([1.0, np.nan, 3.0]).ffill().tolist())
ts = pd.to_datetime(pd.Series(["2024-01-01"]))
print(ts.astype("int64").tolist(), ts.dt.as_unit("ns").astype("int64").tolist())
print(pd.Timestamp("2024-01-01", tz="Asia/Ho_Chi_Minh").tz)
c = pd.Series(pd.Categorical(["a", "a"], categories=["a", "b"]))
print(pd.DataFrame({"k": c, "v": [1, 2]}).groupby("k").sum())
