"""Chạy đúng các đoạn code chép trong Phụ lục B."""
from math import comb

import numpy as np
import pandas as pd
from scipy import stats

x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8]); s = pd.Series(x)
print(stats.norm.cdf(1) - stats.norm.cdf(-1), stats.norm.ppf(0.975), stats.norm.ppf([0.95, 0.995]))
rng = np.random.default_rng(2026)
tb = rng.integers(1, 7, size=(10_000, 100)).mean(axis=1); print("tb100 std", tb.std())
print(np.quantile(x, 0.25, method="inverted_cdf"), np.quantile(x, 0.25), s.quantile(0.25))
print(stats.skew(x), s.skew(), stats.skew(x, bias=False), stats.skew([5,6,7,8,9]), stats.skew([2,8,9,9,10]))
m, sd, n = x.mean(), x.std(ddof=1), len(x)
print(m - 1.96 * sd / np.sqrt(n), m + 1.96 * sd / np.sqrt(n), m - 1.96 * sd, m + 1.96 * sd)
rng = np.random.default_rng(2026)
tbs = np.array([rng.choice(x, size=10, replace=True).mean() for _ in range(1000)])
print(np.quantile(tbs, [0.025, 0.975]))
r = stats.bootstrap((x,), np.mean, n_resamples=9999, method="percentile", rng=np.random.default_rng(2026))
print(r.confidence_interval)
print(stats.nbinom.ppf(0.95, n=2, p=2 / (2 + 5)), 2 * stats.t.sf(4, df=3), 2 * stats.norm.sf(4))
nd = np.array([25, 27, 29, 31, 33]); dien = np.array([6, 7, 9, 8, 10])
print(np.polyfit(nd, dien, 1))
for c in [7, 7.5, 7.7, 8]:
    print(c, ((x - c) ** 2).sum().round(2), np.abs(x - c).sum())
print(np.corrcoef([1,2,3,4,5],[5,3,4,2,4])[0,1])
print(sum(comb(10, k) for k in (9, 10)) / 1024, stats.binomtest(9, 10).pvalue)
