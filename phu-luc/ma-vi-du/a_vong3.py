"""Phụ lục A vòng 3 (môi trường buổi 3, pandas 3)."""
import duckdb
import pandas as pd
import polars as pl

for cu in ["H", "T", "S", "M", "Q", "Y", "A", "L", "U", "BM"]:
    try:
        pd.date_range("2024-01-01", periods=2, freq=cu)
        print(cu, "chay")
    except Exception as e:
        print(cu, "->", str(e)[-40:])
for moi in ["h", "min", "s", "ME", "QE", "YE", "ms", "us", "BME"]:
    pd.date_range("2024-01-01", periods=2, freq=moi)
print("moi ok")
bang_y = pd.DataFrame({"t": pd.date_range("2024-01-01", periods=3, freq="h"), "y": [5, 7, 6]})
kq = duckdb.sql("SELECT t, y, lag(y) OVER (ORDER BY t) AS tre_1 FROM bang_y ORDER BY t").df()
print(kq.dtypes.to_dict())
print(duckdb.sql("SELECT t, y FROM bang_y WHERE y > 5").df())
print(pd.Timestamp("2024-07-02").day_name(), pd.Timestamp("2024-07-01").day_name())
d = pl.DataFrame({"v": [0, 1, 2]})
print(d.with_columns(pl.col("v").shift(1).alias("tre_1"))["tre_1"].dtype)
x = pd.Series([0.0, 1, 2], index=pd.date_range("2024-01-01", periods=3, freq="h"))
print(x.iloc[:2].tolist(), x.loc["2024-01-01 00:00":"2024-01-01 01:00"].tolist())
print(pd.Series([1.0, None]).isna().tolist())
