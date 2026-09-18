"""polars + DuckDB cho Phụ lục A (môi trường buổi 3)."""
import duckdb
import pandas as pd
import polars as pl

pl.Config.set_tbl_hide_dataframe_shape(True)
d = pl.DataFrame({"t": pd.date_range("2024-01-01", periods=6, freq="h"), "v": [0, 1, 2, 3, 4, 5]})
print(d.group_by_dynamic("t", every="2h").agg(pl.col("v").sum()))
q = pl.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 10:05"])})
r = pl.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 10:03"]), "v": [1, 2]})
print(q.join_asof(r, on="t")["v"].to_list())
print(d.with_columns(pl.col("v").shift(1).alias("tre_1"))["tre_1"].to_list())
print(d.with_columns(pl.col("v").rolling_mean(3).alias("tb3"))["tb3"].to_list())
print(d.with_columns(pl.col("t").dt.replace_time_zone("UTC").dt.convert_time_zone("Asia/Ho_Chi_Minh"))["t"][0])
print(d.with_columns(pl.col("t").dt.replace_time_zone("Asia/Ho_Chi_Minh"))["t"][0])
print(d.with_columns(pl.col("t").dt.replace_time_zone("UTC").dt.replace_time_zone("Asia/Ho_Chi_Minh"))["t"][0])
lz = pl.LazyFrame({"a": [1, 2, 3]}).filter(pl.col("a") > 1)
print(type(lz).__name__, lz.collect()["a"].to_list())

con = duckdb.connect()
con.execute("CREATE TABLE trai AS SELECT * FROM (VALUES (TIMESTAMP '2024-01-01 10:00'), (TIMESTAMP '2024-01-01 10:05')) v(t)")
con.execute("CREATE TABLE phai AS SELECT * FROM (VALUES (TIMESTAMP '2024-01-01 10:00', 1), (TIMESTAMP '2024-01-01 10:03', 2)) v(t, v)")
print(con.sql("SELECT trai.t, phai.v FROM trai ASOF JOIN phai ON trai.t >= phai.t ORDER BY trai.t").fetchall())
print(con.sql("SELECT time_bucket(INTERVAL '15 minutes', TIMESTAMP '2024-01-01 10:07')").fetchall())
print(con.sql("SELECT date_trunc('hour', TIMESTAMP '2024-01-01 10:07')").fetchall())
con.execute("CREATE TABLE y AS SELECT * FROM (VALUES (TIMESTAMP '2024-01-01 00:00', 5), (TIMESTAMP '2024-01-01 01:00', 7), (TIMESTAMP '2024-01-01 02:00', 6)) v(t, y)")
print(con.sql("SELECT t, y, lag(y) OVER (ORDER BY t) AS tre_1 FROM y ORDER BY t").fetchall())
con.execute("SET TimeZone = 'Asia/Ho_Chi_Minh'")
print(con.sql("SELECT (TIMESTAMPTZ '2024-01-01 00:00:00+00')::VARCHAR").fetchall())
print(con.sql("SELECT date_trunc('day', TIMESTAMPTZ '2024-01-01 20:00:00+00')::VARCHAR").fetchall())
con.execute("SET TimeZone = 'UTC'")
print(con.sql("SELECT (TIMESTAMPTZ '2024-01-01 00:00:00+00')::VARCHAR").fetchall())
print(con.sql("SELECT date_trunc('day', TIMESTAMPTZ '2024-01-01 20:00:00+00')::VARCHAR").fetchall())
