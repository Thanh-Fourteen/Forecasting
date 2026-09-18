# %% [markdown]
# # Bấm giờ: đọc 3,6 triệu chuyến taxi rồi đếm số chuyến theo giờ — pandas, polars, DuckDB
#
# Cùng một việc, ba công cụ. Mỗi cách chạy 1 lần làm nóng + 7 lần đo, báo trung vị.
# Con số phụ thuộc máy: ghi lại số nhân CPU khi so với bạn cùng lớp.

# %%
from __future__ import annotations

import os
import statistics
import time

import duckdb
import pandas as pd
import polars as pl

import tv

TEP = tv.THU_MUC_DU_LIEU / "nyc-tlc-yellow-2024-03" / "yellow_tripdata_2024-03.parquet"
COT = "tpep_pickup_datetime"


def pandas_tat_ca_cot() -> int:
    df = pd.read_parquet(TEP)
    return len(df.groupby(df[COT].dt.floor("h")).size())


def pandas_mot_cot() -> int:
    df = pd.read_parquet(TEP, columns=[COT])
    return len(df.groupby(df[COT].dt.floor("h")).size())


def polars_lazy() -> int:
    return (pl.scan_parquet(TEP).group_by(pl.col(COT).dt.truncate("1h")).len().collect().height)


def duckdb_sql() -> int:
    return len(duckdb.sql(f"SELECT date_trunc('hour', {COT}) AS gio, count(*) FROM '{TEP}' GROUP BY 1").fetchall())


def bam(ham, lan: int = 7) -> tuple[float, int]:
    ket_qua = ham()  # làm nóng: bộ nhớ đệm của hệ điều hành, khởi tạo thư viện
    thoi_gian = []
    for _ in range(lan):
        bat_dau = time.perf_counter()
        ham()
        thoi_gian.append(time.perf_counter() - bat_dau)
    return statistics.median(thoi_gian), ket_qua


# %%
if __name__ == "__main__":
    print(f"CPU: {os.cpu_count()} luồng | pandas {pd.__version__}, polars {pl.__version__}, duckdb {duckdb.__version__}")
    for ten, ham in [("pandas — đọc mọi cột", pandas_tat_ca_cot), ("pandas — chỉ cột cần", pandas_mot_cot),
                     ("polars — scan_parquet (lazy)", polars_lazy), ("DuckDB — SQL trên tệp", duckdb_sql)]:
        giay, so_nhom = bam(ham)
        print(f"{ten:<32} {giay:6.3f} s   ({so_nhom} nhóm giờ)")
