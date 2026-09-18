"""Phần 'pandas 2 và pandas 3' chạy trên pandas 2.3.3 (môi trường buổi 14)."""
import warnings

import numpy as np
import pandas as pd

print(pd.__version__)
warnings.simplefilter("always")
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    df["a"][df["b"] > 4] = 100
    print([type(x.message).__name__ for x in w])
print(df["a"].tolist())
print(pd.Series(["a", "b"]).dtype)
print(pd.to_datetime(pd.Series(["2024-01-01"])).dtype)
for f in ["H", "T", "M"]:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        r = pd.date_range("2024-01-01", periods=2, freq=f)
        print(f, list(r), [type(x.message).__name__ for x in w])
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    print(pd.Series([1.0, np.nan]).fillna(method="ffill").tolist(), [type(x.message).__name__ for x in w])
ts = pd.to_datetime(pd.Series(["2024-01-01"]))
print(ts.astype("int64").tolist())
print(type(pd.Timestamp("2024-01-01", tz="Asia/Ho_Chi_Minh").tz))
c = pd.Series(pd.Categorical(["a", "a"], categories=["a", "b"]))
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    print(pd.DataFrame({"k": c, "v": [1, 2]}).groupby("k").sum(), [type(x.message).__name__ for x in w])
