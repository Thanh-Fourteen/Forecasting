import duckdb
import pandas as pd

print(pd.date_range("2024-01-01", periods=3, freq="QE"), pd.date_range("2024-01-01", periods=3, freq="YE"))
con = duckdb.connect()
con.execute("CREATE TABLE y AS SELECT * FROM (VALUES (TIMESTAMP '2024-01-01 00:00', 5), (TIMESTAMP '2024-01-01 01:00', 7), (TIMESTAMP '2024-01-01 02:00', 6), (TIMESTAMP '2024-01-01 03:00', 9)) v(t, y)")
print(con.sql("SELECT t, avg(y) OVER (ORDER BY t ROWS 2 PRECEDING) AS tb3 FROM y ORDER BY t").fetchall())
print(pd.Series([5,7,6,9]).rolling(3).mean().tolist(), pd.Series([5,7,6,9]).rolling(3, min_periods=1).mean().tolist())
