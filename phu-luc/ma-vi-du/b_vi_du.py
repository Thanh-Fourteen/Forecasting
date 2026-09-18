"""Mọi con số của Phụ lục B (môi trường buổi 2: numpy 2.5.3, pandas 3.0.5, scipy 1.18.1)."""
from math import comb

import numpy as np
import pandas as pd
from scipy import stats


def H(t):
    print(f"\n===== {t}")


x = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])
n = len(x)

H("1 phan phoi: bang tan suat")
gia_tri, dem = np.unique(x, return_counts=True)
for g, d in zip(gia_tri, dem):
    print(g, d, d / n, "#" * d)
s = pd.Series(x)
print(s.value_counts().sort_index())
print(s.value_counts(normalize=True).sort_index())
# nhom 2 kWh
kho = pd.cut(s, bins=[4, 6, 8, 10, 12])
print(kho.value_counts().sort_index())
print("P(<=8)", (x <= 8).mean())

H("2 trung binh")
print(x.sum(), x.mean(), s.mean())
x2 = x.copy(); x2[5] = 40
print("thay 12->40", x2.mean(), np.median(x2))

H("3 trung vi")
print(np.sort(x), np.median(x), s.median())
le = np.array([3, 1, 7, 5, 100])
print(np.sort(le), np.median(le), le.mean())

H("4 quantile")
xs = np.sort(x)
for q in [0.1, 0.25, 0.5, 0.75, 0.8, 0.9]:
    k = int(np.ceil(q * n - 1e-12))
    print(q, "vi tri", q * n, "->", k, "gia tri", xs[k - 1],
          "inverted_cdf", np.quantile(x, q, method="inverted_cdf"), "linear", np.quantile(x, q),
          "ti le <=", (x <= xs[k - 1]).mean())
print("pandas q0.25", s.quantile(0.25), "q0.9", s.quantile(0.9))
d7 = np.array([4, 9, 2, 7, 5, 3, 8])
print(np.sort(d7), 0.8 * 7, np.quantile(d7, 0.8, method="inverted_cdf"), np.quantile(d7, 0.8))
print("IQR", np.quantile(x, 0.75, method="inverted_cdf") - np.quantile(x, 0.25, method="inverted_cdf"))

H("5 phuong sai")
dl = x - x.mean()
print("do lech", dl.round(2).tolist())
print("binh phuong", (dl ** 2).round(2).tolist(), "tong", (dl ** 2).sum().round(4))
print("var n", np.var(x), "var n-1", np.var(x, ddof=1), "sd n", np.std(x), "sd n-1", np.std(x, ddof=1))
print("pandas var", s.var(), "pandas std", s.std(), "pandas std ddof0", s.std(ddof=0))
print("khoang TB +- 1 sd", x.mean() - np.std(x), x.mean() + np.std(x), ((x >= x.mean() - np.std(x)) & (x <= x.mean() + np.std(x))).sum())
# vi sao n-1: mo phong
rng = np.random.default_rng(2026)
mau = rng.normal(0, 2, size=(100_000, 5))   # phuong sai that = 4
print("TB var chia n:", np.var(mau, axis=1).mean().round(3), "chia n-1:", np.var(mau, axis=1, ddof=1).mean().round(3))
a = np.array([2, 4, 6]); print("2,4,6", np.var(a), np.var(a, ddof=1))

H("6 he so lech")
m2 = (dl ** 2).mean(); m3 = (dl ** 3).mean()
print("lap phuong", (dl ** 3).round(3).tolist(), "tong", (dl ** 3).sum().round(3))
print("m2", m2, "m3", m3.round(4), "g1", (m3 / m2 ** 1.5).round(4))
print("scipy skew", stats.skew(x).round(4), "bias False", stats.skew(x, bias=False).round(4), "pandas", s.skew().round(4))
print("doi xung 5,6,7,8,9", stats.skew([5, 6, 7, 8, 9]))
print("lech trai", stats.skew([2, 8, 9, 9, 10]).round(4))
print("TB vs trung vi", x.mean(), np.median(x))

H("7 phan phoi chuan")
for k in [1, 2, 3]:
    print(k, (stats.norm.cdf(k) - stats.norm.cdf(-k)).round(4))
print("ppf 0.975", stats.norm.ppf(0.975), "cdf 1.96", stats.norm.cdf(1.96), "2-duoi", 2 * (1 - stats.norm.cdf(1.96)))
print("ppf 0.95", stats.norm.ppf(0.95), "ppf 0.9", stats.norm.ppf(0.9), "ppf .995", stats.norm.ppf(0.995))
rng = np.random.default_rng(2026)
z = rng.normal(100, 10, size=100_000)
for k in [1, 2, 3]:
    print("mo phong", k, (np.abs(z - 100) <= k * 10).mean())
print("mo phong 1.96", (np.abs(z - 100) <= 1.96 * 10).mean())
mu, sd = x.mean(), np.std(x)
print("khoang 95%", mu - 1.96 * sd, mu + 1.96 * sd)
print("z cua 12", (12 - mu) / sd, "z cua 5", (5 - mu) / sd)
print("z = 2.5 ->", 1 - stats.norm.cdf(2.5))

H("8 chon con so: mat mat")
cs = np.arange(5, 13)
for c in cs:
    print(c, "binh phuong", ((x - c) ** 2).sum(), "tuyet doi", np.abs(x - c).sum())
for c in [7.5, 7.7]:
    print(c, "binh phuong", ((x - c) ** 2).sum().round(2), "tuyet doi", np.abs(x - c).sum().round(2))
luoi = np.linspace(4, 13, 9001)
bp = np.array([((x - c) ** 2).sum() for c in luoi]); td = np.array([np.abs(x - c).sum() for c in luoi])
print("argmin bp", luoi[bp.argmin()], "td min tren doan", luoi[np.isclose(td, td.min())].min(), luoi[np.isclose(td, td.min())].max())
# log-chuan (bang cu)
rng = np.random.default_rng(2026)
ln = rng.lognormal(0, 1, size=10_000)
luoi = np.linspace(0, 6, 6001)
def pinball(y, q, tau):
    e = y - q
    return np.mean(np.maximum(tau * e, (tau - 1) * e))
c_bp = luoi[np.argmin([np.mean((ln - c) ** 2) for c in luoi])]
c_td = luoi[np.argmin([np.mean(np.abs(ln - c)) for c in luoi])]
c_pb = luoi[np.argmin([pinball(ln, c, 0.9) for c in luoi])]
print("lognormal: c_bp", c_bp, "mean", ln.mean().round(3), "c_td", c_td, "median", np.median(ln).round(3),
      "c_pb", c_pb, "q0.9", np.quantile(ln, 0.9).round(3))

H("9 tuong quan")
nd = np.array([25, 27, 29, 31, 33]); dien = np.array([6, 7, 9, 8, 10])
dx = nd - nd.mean(); dy = dien - dien.mean()
print("TB", nd.mean(), dien.mean(), "dx", dx, "dy", dy, "tich", dx * dy, "tong", (dx * dy).sum())
print("Sxx", (dx ** 2).sum(), "Syy", (dy ** 2).sum())
print("cov n-1", np.cov(nd, dien)[0, 1], "cov n", np.cov(nd, dien, ddof=0)[0, 1])
print("r", (dx * dy).sum() / np.sqrt((dx ** 2).sum() * (dy ** 2).sum()), np.corrcoef(nd, dien)[0, 1],
      pd.Series(nd).corr(pd.Series(dien)))
# doi don vi: F
f = nd * 9 / 5 + 32
print("cov F", np.cov(f, dien)[0, 1], "r F", np.corrcoef(f, dien)[0, 1])
# y = x^2
xx = np.array([-2, -1, 0, 1, 2]); print("r x^2", np.corrcoef(xx, xx ** 2)[0, 1])
# ngoai lai 1 diem
xa = np.array([1, 2, 3, 4, 5, 20]); ya = np.array([5, 3, 4, 2, 4, 20])
print("r co ngoai lai", np.corrcoef(xa, ya)[0, 1].round(3), "bo diem cuoi", np.corrcoef(xa[:-1], ya[:-1])[0, 1].round(3))
# hai chuoi co xu huong, doc lap
rng = np.random.default_rng(2026)
t = np.arange(100)
a1 = 0.5 * t + rng.normal(0, 3, 100); a2 = 0.3 * t + rng.normal(0, 3, 100)
print("r xu huong", np.corrcoef(a1, a2)[0, 1].round(3), "sai phan", np.corrcoef(np.diff(a1), np.diff(a2))[0, 1].round(3))
# hoi quy tu cung vi du
b = (dx * dy).sum() / (dx ** 2).sum(); a0 = dien.mean() - b * nd.mean()
du = a0 + b * nd; ss_res = ((dien - du) ** 2).sum(); ss_tot = ((dien - dien.mean()) ** 2).sum()
print("hoi quy b", b, "a", a0, "du", du.round(2), "SSres", ss_res.round(3), "SStot", ss_tot, "R2", (1 - ss_res / ss_tot).round(4), "r^2", 0.9 ** 2)
print("polyfit", np.polyfit(nd, dien, 1))

H("10 kiem dinh dong xu")
for k in range(11):
    print(k, comb(10, k), comb(10, k) / 1024)
p9 = sum(comb(10, k) for k in (9, 10)) / 1024
p8 = sum(comb(10, k) for k in (8, 9, 10)) / 1024
p7 = sum(comb(10, k) for k in (7, 8, 9, 10)) / 1024
print("P(>=9)", p9, "P(>=8)", p8, "P(>=7)", p7, 11 / 1024, 56 / 1024, 176 / 1024)
print("scipy binomtest greater 9", stats.binomtest(9, 10, 0.5, alternative="greater").pvalue)
print("scipy binomtest two-sided 9", stats.binomtest(9, 10, 0.5).pvalue, 22 / 1024)
print("scipy 7", stats.binomtest(7, 10, 0.5, alternative="greater").pvalue)
# dong xu lech 0.7: xac suat bi bac bo (>=9)
p = 0.7
print("P(>=9 | 0.7)", 10 * p ** 9 * (1 - p) + p ** 10, stats.binom.sf(8, 10, 0.7))
print("P(>=9 | 0.9)", stats.binom.sf(8, 10, 0.9))
# 1000 dong xu: 990 can, 10 lech 0.9
can = 990 * p9; lech = 10 * stats.binom.sf(8, 10, 0.9)
print("so dong xu >=9: can", can, "lech", lech, "ti le can", can / (can + lech))
# mo phong 100 dong xu can: bao nhieu dong xu bi bac bo
rng = np.random.default_rng(2026)
ngua = rng.binomial(10, 0.5, size=1000)
print("1000 dong xu can, so co >=9 ngua", (ngua >= 9).sum())
# 100 lan / 70 ngua
print("P(>=70/100)", stats.binom.sf(69, 100, 0.5))

H("11 LLN / CLT")
rng = np.random.default_rng(2026)
tung = rng.integers(1, 7, size=100_000)
for m in [10, 100, 1000, 100_000]:
    print("TB cua", m, "lan dau", tung[:m].mean())
rng = np.random.default_rng(2026)
for m in [1, 10, 100, 1000]:
    tb = rng.integers(1, 7, size=(10_000, m)).mean(axis=1)
    print("m", m, "sd cua TB", tb.std().round(4), "ly thuyet", (np.sqrt(35 / 12) / np.sqrt(m)).round(4),
          "q2.5", np.quantile(tb, 0.025), "q97.5", np.quantile(tb, 0.975))
print("sd 1 lan", np.sqrt(35 / 12))
rng = np.random.default_rng(2026)
tb30 = rng.integers(1, 7, size=(10_000, 30)).mean(axis=1)
dem, bien = np.histogram(tb30, bins=np.arange(2.0, 5.01, 0.25))
for d, b0 in zip(dem, bien):
    print(f"{b0:.2f}-{b0 + 0.25:.2f} {d:5d} " + "#" * (d // 100))
print("trong 3.5 +- 1.96*sd/sqrt30", (np.abs(tb30 - 3.5) <= 1.96 * np.sqrt(35 / 12) / np.sqrt(30)).mean())
dem1 = np.bincount(rng.integers(1, 7, size=10_000))[1:]
print("1 lan tung dem", dem1)
# Cauchy (bang cu)
rng = np.random.default_rng(2026)
for m in [10, 1000, 100_000]:
    c = rng.standard_cauchy(size=(200, m)).mean(axis=1)
    g = rng.normal(size=(200, m)).mean(axis=1)
    iqr = lambda v: np.quantile(v, 0.75) - np.quantile(v, 0.25)
    print("cauchy/chuan", m, round(iqr(c), 4), round(iqr(g), 4))

H("11b n_eff")
rng = np.random.default_rng(2026)
def ar1(rho, n, lap, rng):
    e = rng.normal(size=(lap, n))
    y = np.empty_like(e)
    y[:, 0] = e[:, 0] / np.sqrt(1 - rho ** 2)
    for t in range(1, n):
        y[:, t] = rho * y[:, t - 1] + e[:, t]
    return y
for rho in [0, 0.5, 0.9]:
    y = ar1(rho, 200, 5000, rng)
    print(rho, (y.var() / y.mean(axis=1).var()).round(1), round(200 * (1 - rho) / (1 + rho), 1))

H("12 khoang du bao vs log-chuan")
rng = np.random.default_rng(2026)
for sig in [0.5, 1.0, 1.5]:
    duoi, tren, phu, phu_q, am = [], [], [], [], 0
    duoi_q, tren_q = [], []
    for _ in range(2000):
        m = rng.lognormal(0, sig, 200); moi = rng.lognormal(0, sig, 1000)
        lo, hi = m.mean() - 1.96 * m.std(ddof=1), m.mean() + 1.96 * m.std(ddof=1)
        am += lo < 0
        duoi.append((moi < lo).mean()); tren.append((moi > hi).mean())
        ql, qh = np.quantile(m, [0.025, 0.975])
        phu_q.append(((moi >= ql) & (moi <= qh)).mean())
        duoi_q.append((moi < ql).mean()); tren_q.append((moi > qh).mean())
    print(sig, "phu", round(1 - np.mean(duoi) - np.mean(tren), 3), "duoi", round(np.mean(duoi), 3),
          "tren", round(np.mean(tren), 3), "can am", am / 2000, "phu quantile", round(np.mean(phu_q), 3),
          "duoi q", round(np.mean(duoi_q), 3), "tren q", round(np.mean(tren_q), 3))
# tren vi du 10 ngay
print("10 ngay: TB +- 1.96 sd(n-1)", x.mean() - 1.96 * x.std(ddof=1), x.mean() + 1.96 * x.std(ddof=1))
print("khoang tin cay TB: +-1.96 sd/sqrt(n)", x.mean() - 1.96 * x.std(ddof=1) / np.sqrt(n), x.mean() + 1.96 * x.std(ddof=1) / np.sqrt(n))

H("13 bootstrap")
rng = np.random.default_rng(2026)
lan1 = rng.choice(x, size=n, replace=True)
print("mot lan rut", lan1, lan1.mean())
rng = np.random.default_rng(2026)
tbs = np.array([rng.choice(x, size=n, replace=True).mean() for _ in range(1000)])
print("B=1000 TB cac TB", tbs.mean().round(3), "q2.5", np.quantile(tbs, 0.025), "q97.5", np.quantile(tbs, 0.975), "sd", tbs.std().round(3))
tv = np.array([np.median(rng.choice(x, size=n, replace=True)) for _ in range(1000)])
print("trung vi bootstrap q2.5 q97.5", np.quantile(tv, 0.025), np.quantile(tv, 0.975))
r = stats.bootstrap((x,), np.mean, n_resamples=9999, rng=np.random.default_rng(2026), method="percentile")
print("scipy percentile", r.confidence_interval)
# iid vs block tren AR(1) rho 0.7 (bang cu)
rng = np.random.default_rng(2026)
def block_boot_mean(y, l, B, rng):
    nn = len(y); k = int(np.ceil(nn / l))
    starts = rng.integers(0, nn - l + 1, size=(B, k))
    idx = (starts[:, :, None] + np.arange(l)).reshape(B, -1)[:, :nn]
    return y[idx].mean(axis=1)
chua_iid = chua_blk = 0
L = 400
for _ in range(L):
    y = ar1(0.7, 200, 1, rng)[0]
    bi = y[rng.integers(0, 200, size=(999, 200))].mean(axis=1)
    lo, hi = np.quantile(bi, [0.025, 0.975]); chua_iid += lo <= 0 <= hi
    bb = block_boot_mean(y, 20, 999, rng)
    lo, hi = np.quantile(bb, [0.025, 0.975]); chua_blk += lo <= 0 <= hi
print("iid", chua_iid / L, "block", chua_blk / L)

H("14 phan phoi dem")
rng = np.random.default_rng(2026)
po = rng.poisson(5, 100_000)
nb = stats.nbinom.rvs(n=2, p=2 / (2 + 5), size=100_000, random_state=np.random.default_rng(2026))
print("poisson TB", po.mean().round(2), "var", po.var().round(2))
print("nbinom TB", nb.mean().round(2), "var", nb.var().round(2), "ly thuyet", 5 + 25 / 2)
print("P(Y=3) poisson 5", stats.poisson.pmf(3, 5).round(4), np.exp(-5) * 5 ** 3 / 6)
print("poisson q0.95", stats.poisson.ppf(0.95, 5), "nbinom q0.95", stats.nbinom.ppf(0.95, 2, 2 / 7))
dem_k = np.array([2, 0, 7, 1, 12, 3, 0, 9, 4, 2])
print("vi du dem TB", dem_k.mean(), "var n-1", dem_k.var(ddof=1).round(2), "ti le", (dem_k.var(ddof=1) / dem_k.mean()).round(2))
print("t: P(|T|>4) df3", 2 * stats.t.sf(4, 3), "chuan", 2 * stats.norm.sf(4))

H("15 likelihood")
for p in [0.3, 0.5, 0.6, 0.7, 0.8, 0.9]:
    print(p, p ** 7 * (1 - p) ** 3, stats.binom.pmf(7, 10, p))
luoi = np.linspace(0.01, 0.99, 99)
print("argmax", luoi[np.argmax(luoi ** 7 * (1 - luoi) ** 3)])

H("vong 2: so bo sung")
print("z cua 12 dung s chia n-1", (12 - x.mean()) / x.std(ddof=1))
print("phuong sai 1 lan tung xuc xac", np.mean((np.arange(1, 7) - 3.5) ** 2), 35 / 12, np.sqrt(35 / 12))
print("P(10 ngua)", 1 / 1024, "ti le bac bo oan that su khi alpha=0.05, n=10:", stats.binom.sf(8, 10, 0.5))
for sig in [0.5, 1.0, 1.5]:
    print("log-chuan sigma", sig, "he so lech ly thuyet", float(stats.lognorm(sig).stats(moments="s")))
for c in range(6, 13):
    print("chi phi 4:1 mua", c, 4 * np.clip(x - c, 0, None).sum() + 1 * np.clip(c - x, 0, None).sum())
rng = np.random.default_rng(2026)
tb30 = rng.integers(1, 7, size=(10_000, 30)).mean(axis=1)
print("so TB ngoai 2.5-4.5", ((tb30 < 2.5) | (tb30 >= 4.5)).sum())

H("vong 3: so bo sung")
nd = np.array([25, 27, 29, 31, 33]); dien = np.array([6, 7, 9, 8, 10])
print("tron ddof: cov(n-1)/(std n * std n) =", np.cov(nd, dien)[0, 1] / (np.std(nd) * np.std(dien)))
print("dung cung ddof=1:", np.cov(nd, dien)[0, 1] / (np.std(nd, ddof=1) * np.std(dien, ddof=1)))
print("0.7: ", 10 * 0.7**9 * 0.3, 0.7**10, "0.9:", 10 * 0.9**9 * 0.1, 0.9**10)
for lo, hi in [(3.25, 3.5), (3.5, 3.75)]:
    tong = [k for k in range(30, 181) if lo <= k / 30 < hi]
    print("khoang", lo, hi, "tong", tong[0], "...", tong[-1], "so gia tri", len(tong))

# vong 4: duoi day so tren cung thang 4 do lech chuan (Student-t nu=3 co do lech chuan sqrt(3))
print("t3 qua 4 sd", 2 * stats.t.sf(4 * np.sqrt(3), df=3), "chuan qua 4 sd", 2 * stats.norm.sf(4))
