import duckdb
import numpy as np
import pandas as pd
import polars as pl

df = pd.DataFrame({"tinh": ["HN", "HN", "HCM"], "kwh": [10, 12, 20]})
print(df); print(df.dtypes); print(df.index.tolist())
print(df["kwh"].tolist(), type(df["kwh"]).__name__)
print(df.loc[1, "kwh"], df.loc[df["kwh"] > 11, "tinh"].tolist())
print(df.groupby("tinh")["kwh"].sum())
print(df.groupby("tinh")["kwh"].mean().to_dict())
c = pd.DataFrame({"loai": pd.Categorical(["ngay_thuong", "ngay_thuong"], categories=["ngay_thuong", "ngay_le"]), "kwh": [10, 12]})
print(c["loai"].dtype)
print(c.groupby("loai", observed=True)["kwh"].sum())
print(c.groupby("loai", observed=False)["kwh"].sum())
print(c.groupby("loai")["kwh"].sum())
print(pd.Series([1, 2]).dtype, pd.Series([1, np.nan]).dtype, pd.Series([1, None]).tolist())
print(pd.date_range("2024-01-01", periods=3, freq="W"))
a = [10, 11, 12, 13, 14]; print(a[2:4])
x = pd.Series([0.0, 1, 2], index=pd.date_range("2024-01-01", periods=3, freq="h"))
print(x.rolling("2h", min_periods=2).sum().tolist())
don = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:07"])})
gia = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:05", "2024-01-01 10:10"]), "gia": [100, 105]})
print(pd.merge(don, gia, on="t", how="left"), pd.merge(don, gia, on="t"))
# duckdb reads pandas
bang_y = pd.DataFrame({"t": pd.date_range("2024-01-01", periods=3, freq="h"), "y": [5, 7, 6]})
print(duckdb.sql("SELECT t, y, lag(y) OVER (ORDER BY t) AS tre_1 FROM bang_y ORDER BY t").df())
print(duckdb.sql("SELECT 5::VARCHAR AS a").fetchall())
# polars explain
d = pl.DataFrame({"t": pd.date_range("2024-01-01", periods=4, freq="h"), "v": [0, 1, 2, 3]})
print(d.with_columns((pl.col("v") * 10).alias("v10")))
# chained assignment continues?
df2 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
import warnings

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    df2["a"][df2["b"] > 4] = 100
    print("tiep tuc chay", [issubclass(type(i.message), Warning) for i in w], type(w[0].message).__mro__[:3])
# rain example: taxi local naive vs rain UTC naive
chuyen = pd.DataFrame({"gio": pd.to_datetime(["2024-07-01 14:00", "2024-07-01 15:00", "2024-07-01 16:00"]), "so_chuyen": [100, 100, 180]})
mua = pd.DataFrame({"gio": pd.to_datetime(["2024-07-01 19:00", "2024-07-01 20:00", "2024-07-01 21:00"]), "mua_mm": [0, 0, 12]})
print(chuyen.merge(mua, on="gio", how="left"))
mua["gio_dia_phuong"] = mua["gio"].dt.tz_localize("UTC").dt.tz_convert("America/New_York").dt.tz_localize(None)
print(mua)
print(chuyen.merge(mua[["gio_dia_phuong", "mua_mm"]], left_on="gio", right_on="gio_dia_phuong"))
