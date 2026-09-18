import duckdb
import pandas as pd

trai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 10:05"])})
phai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 10:03"]), "v": [1, 2]})
print(duckdb.sql("SELECT trai.t, phai.v FROM trai ASOF JOIN phai ON trai.t >= phai.t ORDER BY trai.t").fetchall())
# tu kiem tra 4
s = pd.Series([1, 2, 3, 4], index=pd.date_range("2024-01-01", periods=4, freq="h"))
print(s.resample("2h", closed="right", label="right").sum())
print(s.resample("2h").sum().tolist())
# 5
z = pd.Series([10.0, 20, 30, 40], index=pd.date_range("2024-01-01", periods=4, freq="h"))
print(z.rolling(2).mean().shift(1).tolist(), z.rolling("2h").mean().tolist())
# 6
t6 = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:02"])})
p6 = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 10:02", "2024-01-01 10:04"]), "v": [1, 2, 3]})
print(pd.merge_asof(t6, p6, on="t")["v"].tolist(), pd.merge_asof(t6, p6, on="t", allow_exact_matches=False)["v"].tolist(),
      pd.merge_asof(t6, p6, on="t", direction="forward", allow_exact_matches=False)["v"].tolist())
# 7
print(pd.Timestamp("2024-07-01 20:00", tz="UTC").tz_convert("Asia/Ho_Chi_Minh"))
print(pd.Timestamp("2024-07-01 21:00", tz="UTC").tz_convert("America/New_York"))
