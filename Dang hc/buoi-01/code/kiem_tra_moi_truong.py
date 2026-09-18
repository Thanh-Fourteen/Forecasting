# %% [markdown]
# # Buổi 1 — Kiểm tra môi trường: phiên bản thư viện và dữ liệu

# %%
from __future__ import annotations

import platform

import matplotlib
import numpy as np
import pandas as pd

import tv

# %%
if __name__ == "__main__":
    print("Python     ", platform.python_version())
    print("numpy      ", np.__version__)
    print("pandas     ", pd.__version__)
    print("matplotlib ", matplotlib.__version__)
    tep = tv.THU_MUC_DU_LIEU / "uci-household-power" / "household_power_consumption.txt"
    print("dữ liệu    ", tep.name, f"{tep.stat().st_size:,} byte" if tep.is_file() else "CHƯA CÓ — chạy: make up")
