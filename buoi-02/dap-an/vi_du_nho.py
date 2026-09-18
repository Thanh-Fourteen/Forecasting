# %% [markdown]
# # Buổi 2 — mọi con số của ví dụ nhỏ và các con số MỚI trên dữ liệu thật (Phase 6)
#
# Chạy trong lab/:  env -u VIRTUAL_ENV uv run --no-sync --project 00-nen python ../dap-an/vi_du_nho.py
# Seed ghi cạnh từng phép ngẫu nhiên. Ví dụ nhỏ không cần dữ liệu; phần "dữ liệu thật" đọc Bike Sharing.

# %%
from __future__ import annotations

import importlib.util
from math import comb, sqrt
from pathlib import Path

import numpy as np
from scipy import stats

DAY = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("xs", DAY / "xac_suat.py")
xs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xs)


def quantile_dem_tay(x, p: float) -> float:
    """Cách đếm tay của khoá: xếp tăng, vị trí = p × n làm tròn lên (tối thiểu 1)."""
    x = np.sort(np.asarray(x, dtype=float))
    vi_tri = max(1, int(np.ceil(p * x.size - 1e-12)))
    return float(x[vi_tri - 1])


def pinball(y, c, tau):
    sai = np.asarray(y, dtype=float) - c
    return float(np.where(sai >= 0, tau * sai, (tau - 1) * sai).mean())


def muc_4_1_va_4_2() -> None:
    print("== 4.1–4.2: 9 giờ lượt thuê ==")
    x = np.array([8, 2, 36, 5, 12, 3, 18, 6, 9])
    s = np.sort(x)
    print("xếp tăng:", s.tolist(), " n =", x.size)
    for p in (0.25, 0.5, 0.8, 0.9):
        print(f"  quantile {p}: đếm tay {quantile_dem_tay(x, p):g}  | np.quantile (nội suy) {np.quantile(x, p):.2f}"
              f"  | inverted_cdf {np.quantile(x, p, method='inverted_cdf'):g}")
    print("  CDF: tỷ lệ ≤ 8 =", np.mean(x <= 8), " tỷ lệ ≤ 12 =", np.mean(x <= 12))
    tb = x.mean()
    lech = x - tb
    ss = (lech**2).sum()
    print("trung bình", tb, " trung vị", np.median(x))
    print("độ lệch:", sorted(lech.tolist()), " tổng bình phương", ss)
    print(f"phương sai (chia n-1) {x.var(ddof=1):.4f}  độ lệch chuẩn {x.std(ddof=1):.4f}")
    print(f"hệ số lệch (scipy, bias=False) {stats.skew(x, bias=False):.3f}  (bias=True) {stats.skew(x):.3f}")
    zs = lech / x.std(ddof=1)
    print(f"  hệ số lệch theo lời tài liệu (chia s, chia n−1, rồi trung bình lập phương): {np.mean(zs**3):.3f};"
          f"  riêng 36 góp {zs[x == 36][0] ** 3 / x.size:.3f};  σ (chia n) = {x.std(ddof=0):.3f}")
    print("  trung vị n chẵn 1,2,3,4: đếm tay", quantile_dem_tay([1, 2, 3, 4], 0.5), " np.median", np.median([1, 2, 3, 4]))
    z = lech / x.std(ddof=0)
    print(f"  kiểm: trung bình z^3 = {np.mean(z**3):.3f};  riêng số 36 góp {z[x == 36][0] ** 3 / x.size:.3f};"
          f"  σ chia n = {x.std(ddof=0):.3f}")
    for c in (8, 11, 18):
        print(f"  c={c}: MAE {np.abs(x - c).mean():.3f}  bình phương {((x - c) ** 2).mean():.3f}"
              f"  pinball0.8 {pinball(x, c, 0.8):.3f}")
    luoi = np.arange(0, 40.01, 0.5)
    for ten, f in (("tuyệt đối", lambda c: np.abs(x - c).mean()), ("bình phương", lambda c: ((x - c) ** 2).mean()),
                   ("pinball 0.8", lambda c: pinball(x, c, 0.8))):
        v = np.array([f(c) for c in luoi])
        tot = luoi[np.isclose(v, v.min())]
        print(f"  tối ưu {ten}: c ∈ [{tot.min()}, {tot.max()}]")
    lo, hi = tb - 1.96 * x.std(ddof=1), tb + 1.96 * x.std(ddof=1)
    print(f"±1,96s: [{lo:.2f}; {hi:.2f}]")


def muc_4_3() -> None:
    print("== 4.3: 1,96 từ đâu ==")
    print(f"norm.ppf(0.975) = {stats.norm.ppf(0.975):.5f};  P(|Z|<=1.96) = {stats.norm.cdf(1.96) - stats.norm.cdf(-1.96):.4f}")
    print(f"P(|Z|<=1) = {stats.norm.cdf(1) - stats.norm.cdf(-1):.4f}; P(|Z|<=2) = {stats.norm.cdf(2) - stats.norm.cdf(-2):.4f}")
    rng = np.random.default_rng(0)                        # seed 0
    z = rng.normal(size=100_000)
    print(f"mô phỏng 100.000 số chuẩn (seed 0): trong ±1,96 {np.mean(np.abs(z) <= 1.96):.4f}")
    # ví dụ nhỏ tỷ lệ phủ hai đuôi
    thuc = np.array([3, 7, 12, 15, 9, 30, 11, 6, 2, 25])
    lo, hi = 4, 20
    print("10 giá trị thật", thuc.tolist(), f"khoảng [{lo}; {hi}] →", xs.ty_le_phu(thuc, lo, hi))


def muc_4_4(h) -> None:
    print("== 4.4: tương quan ==")
    x = np.array([10, 15, 20, 25, 30])
    y = np.array([40, 60, 50, 90, 110])
    dx, dy = x - x.mean(), y - y.mean()
    print("dx", dx.tolist(), "dy", dy.tolist(), "tích", (dx * dy).tolist())
    print("tổng tích", (dx * dy).sum(), "tổng dx^2", (dx**2).sum(), "tổng dy^2", (dy**2).sum())
    r = (dx * dy).sum() / sqrt((dx**2).sum() * (dy**2).sum())
    print(f"r tay {r:.4f}  np.corrcoef {np.corrcoef(x, y)[0, 1]:.4f}")
    # dữ liệu thật. Cột temp là nhiệt độ đã chuẩn hoá (co giãn tuyến tính) → r không đổi so với °C
    print(f"giờ, cả 2 năm: r(temp, cnt) = {np.corrcoef(h['temp'], h['cnt'])[0, 1]:.3f}")
    g17 = h[h["hr"] == 17]
    print(f"chỉ 17h: r(temp, cnt) = {np.corrcoef(g17['temp'], g17['cnt'])[0, 1]:.3f}  ({len(g17)} ngày)")
    print(f"giờ: r(hum, cnt) = {np.corrcoef(h['hum'], h['cnt'])[0, 1]:.3f};  chỉ 17h: "
          f"{np.corrcoef(g17['hum'], g17['cnt'])[0, 1]:.3f}")
    print(f"giờ: r(hr, cnt) = {np.corrcoef(h['hr'], h['cnt'])[0, 1]:.3f}")
    tb_gio = h.groupby("hr")["cnt"].mean()
    print("trung bình lượt thuê theo giờ: 4h", round(tb_gio[4], 1), " 8h", round(tb_gio[8], 1),
          " 17h", round(tb_gio[17], 1), " 23h", round(tb_gio[23], 1))
    tb_hum = h.groupby("hr")["hum"].mean()
    print("độ ẩm trung bình: 4h", round(tb_hum[4], 2), " 15h", round(tb_hum[15], 2))
    # tự tương quan mượn trước: chuỗi 1, 3, 1, 3
    s = np.array([1, 3, 1, 3.0])
    d = s - s.mean()
    print("tự tương quan trễ 1 của 1,3,1,3:", (d[1:] * d[:-1]).sum() / (d**2).sum())
    c = h["cnt"].to_numpy(float)
    d = c - c.mean()
    print(f"ACF trễ 1 lượt thuê theo giờ: {(d[1:] * d[:-1]).sum() / (d**2).sum():.3f}")


def hoan_vi(y, nhom, so_lan: int, seed: int):
    """Permutation test cho chênh lệch trung bình hai nhóm. Trả (chênh quan sát, mảng chênh khi xáo, p-value)."""
    y = np.asarray(y, dtype=float)
    nhom = np.asarray(nhom, dtype=bool)
    quan_sat = y[nhom].mean() - y[~nhom].mean()
    rng = np.random.default_rng(seed)
    xao = np.empty(so_lan)
    for i in range(so_lan):
        p = rng.permutation(nhom)                    # xáo nhãn, giữ nguyên các con số
        xao[i] = y[p].mean() - y[~p].mean()
    k = int((np.abs(xao) >= abs(quan_sat)).sum())    # hai phía: lệch cỡ này hoặc hơn, về bên nào cũng tính
    return quan_sat, xao, (k + 1) / (so_lan + 1), k


def muc_4_5(d) -> None:
    print("== 4.5: kiểm định ==")
    tu = sum(comb(10, k) for k in (9, 10))
    print(f"P(>=9 ngửa / 10) = {tu}/1024 = {tu / 1024:.4f};  hai phía (>=9 ngửa hoặc >=9 sấp) = {2 * tu}/1024 = "
          f"{2 * tu / 1024:.4f}")
    print(f"P(>=7 ngửa) = {sum(comb(10, k) for k in range(7, 11))}/1024 = "
          f"{sum(comb(10, k) for k in range(7, 11)) / 1024:.4f}")
    rng = np.random.default_rng(1)                   # seed 1: mô phỏng tung đồng xu cân đối
    ngua = rng.binomial(10, 0.5, size=100_000)
    print(f"mô phỏng 100.000 lần tung 10 đồng (seed 1): tỷ lệ >= 9 ngửa {np.mean(ngua >= 9):.4f}")
    # ví dụ nhỏ hoán vị: 3 ngày thường, 3 ngày cuối tuần
    y = np.array([5, 7, 6, 3, 2, 4.0])
    g = np.array([1, 1, 1, 0, 0, 0], dtype=bool)
    from itertools import combinations
    chenh = []
    for chon in combinations(range(6), 3):
        m = np.zeros(6, bool)
        m[list(chon)] = True
        chenh.append(y[m].mean() - y[~m].mean())
    chenh = np.array(chenh)
    qs = y[g].mean() - y[~g].mean()
    print(f"ví dụ nhỏ: chênh quan sát {qs}; số cách chia {len(chenh)}; số cách |chênh| >= {qs}: "
          f"{int((np.abs(chenh) >= abs(qs) - 1e-9).sum())}; p = {(np.abs(chenh) >= abs(qs) - 1e-9).mean():.3f}")
    print("  các chênh có thể:", sorted(np.round(chenh, 3).tolist()))
    n12 = d[d["yr"] == 1]
    qs, xao, p, k = hoan_vi(n12["cnt"], n12["workingday"] == 1, 9999, 2026)
    print(f"2012 ngày làm việc vs nghỉ: n = {(n12['workingday'] == 1).sum()}/{(n12['workingday'] == 0).sum()}, "
          f"TB {n12.loc[n12.workingday == 1, 'cnt'].mean():.1f} vs {n12.loc[n12.workingday == 0, 'cnt'].mean():.1f}, "
          f"chênh {qs:.1f}, số lần xáo lệch bằng/hơn {k}/9999, p = {p:.4f}")
    a = n12.loc[n12.workingday == 1, "cnt"].to_numpy(float)
    b = n12.loc[n12.workingday == 0, "cnt"].to_numpy(float)
    kq = stats.permutation_test((a, b), lambda u, v: u.mean() - v.mean(), n_resamples=9999,
                                alternative="two-sided", rng=np.random.default_rng(2026))
    print(f"  scipy.stats.permutation_test (seed 2026): p = {kq.pvalue:.4f}")
    cuoi_tuan = n12[n12["weekday"].isin([0, 6])]
    qs, xao, p, k = hoan_vi(cuoi_tuan["cnt"], cuoi_tuan["weekday"] == 6, 9999, 2026)
    print(f"2012 thứ Bảy vs Chủ nhật: n = {(cuoi_tuan.weekday == 6).sum()}/{(cuoi_tuan.weekday == 0).sum()}, "
          f"TB {cuoi_tuan.loc[cuoi_tuan.weekday == 6, 'cnt'].mean():.1f} vs "
          f"{cuoi_tuan.loc[cuoi_tuan.weekday == 0, 'cnt'].mean():.1f}, chênh {qs:.1f}, "
          f"số lần xáo lệch bằng/hơn {k}/9999, p = {p:.4f}")
    c = n12["cnt"].to_numpy(float)
    dd = c - c.mean()
    print(f"ACF trễ 1 lượt thuê theo NGÀY 2012: {(dd[1:] * dd[:-1]).sum() / (dd**2).sum():.3f}")


def muc_4_6(h) -> None:
    print("== 4.6: 1/√n, n_eff ==")
    y = h["cnt"].to_numpy(float)
    rng = np.random.default_rng(5)                   # seed 5: rút ngẫu nhiên từng giờ (i.i.d.)
    for n in (25, 100, 400):
        tb = rng.choice(y, size=(20_000, n)).mean(axis=1)
        print(f"  n = {n}: độ lệch chuẩn của trung bình mẫu {tb.std():.2f};  σ/√n = {y.std() / np.sqrt(n):.2f}; "
              f"tỷ lệ trong ±1,96σ/√n quanh trung bình thật {np.mean(np.abs(tb - y.mean()) <= 1.96 * y.std() / np.sqrt(n)):.3f}")
    for n, rho in ((200, 0.7), (365, 0.5)):
        ne = n * (1 - rho) / (1 + rho)
        print(f"  n_eff(n={n}, ρ={rho}) = {ne:.1f};  √(n/n_eff) = {sqrt(n / ne):.3f}")
    print("AR(1) mẫu: 0,7 × 10 + 0,5 =", 0.7 * 10 + 0.5)
    x = np.array([12, 15, 11, 30, 14.0])
    idx = np.random.default_rng(3).integers(0, 5, size=(3, 5))
    print("bootstrap tay seed 3:", idx.tolist(), x[idx].mean(axis=1).tolist())
    # block bootstrap tay: khối dài 2, seed 2 (cùng phép tính với _chi_so_bootstrap, một lần lấy mẫu)
    bat_dau = np.random.default_rng(2).integers(0, 5 - 2 + 1, size=(1, 3))
    chi_so = (bat_dau[:, :, None] + np.arange(2)).reshape(1, -1)[:, :5]
    print("block bootstrap khối 2 seed 2: bắt đầu", bat_dau.tolist(), "chỉ số", chi_so.tolist(),
          "mẫu lại", x[chi_so].tolist(), "trung bình", x[chi_so].mean(axis=1).tolist())
    xx = xs.ar1(200, 0.7, np.random.default_rng(7))
    print(f"chuỗi AR(1) seed 7: trung bình mẫu {xx.mean():.3f}; i.i.d. {np.round(xs.khoang_tin_cay_trung_binh(xx, so_lan=9999, do_dai_khoi=1, seed=7), 3)}"
          f"; khối 6 {np.round(xs.khoang_tin_cay_trung_binh(xx, so_lan=9999, do_dai_khoi=6, seed=7), 3)}")
    print(f"200^(1/3) = {200 ** (1 / 3):.2f};  8734^(1/3) = {8734 ** (1 / 3):.2f};  2000^(1/3) = {2000 ** (1 / 3):.2f}")
    print("  tổ hợp C(10,k), k = 7..10:", [comb(10, k) for k in range(7, 11)])
    for khoi in (1, 3, 6, 10, 20, 40):   # bảng mục 4.6 (seed 2026, 300 chuỗi, B = 999)
        print(f"  AR(1) ρ=0,7 n=200 khối {khoi}: phủ {xs.ty_le_phu_khoang_tin_cay(0.7, 200, 300, 2026, khoi):.3f}")
    print(f"  AR(1) ρ=0,7 n=2000 khối 13: phủ {xs.ty_le_phu_khoang_tin_cay(0.7, 2000, 300, 2026, 13):.3f}")


def muc_bo_sung_vong_2(h) -> None:
    """Đọc thử vòng 2: vì sao bootstrap đúng; ví dụ '20 lần lấy mẫu'; √n với 4 đồng xu ±1; lập phương hệ số lệch."""
    print("== bổ sung vòng 2 ==")
    y = h.loc[h["yr"] == 1, "cnt"].to_numpy(float)          # coi 8.734 giờ năm 2012 là "tổng thể"
    mu, sig = y.mean(), y.std()
    print(f"tổng thể 2012: trung bình {mu:.2f}, σ {sig:.2f}, σ/√100 = {sig / 10:.2f}")
    rng = np.random.default_rng(11)                         # seed 11
    mau = rng.choice(y, 100)                                # MỘT mẫu 100 giờ (rút có hoàn lại từ tổng thể)
    that = [rng.choice(y, 100).mean() for _ in range(5000)] # 5.000 mẫu mới rút từ tổng thể
    boot = [rng.choice(mau, 100).mean() for _ in range(5000)]  # 5.000 mẫu lại rút từ chính mẫu
    print(f"  mẫu: trung bình {mau.mean():.1f}; độ lệch chuẩn của trung bình — mẫu mới từ tổng thể {np.std(that):.1f},"
          f" bootstrap từ mẫu {np.std(boot):.1f}")
    rng = np.random.default_rng(12)                         # seed 12: 20 lần lấy mẫu, mỗi lần dựng khoảng tin cậy
    trung, truot = 0, []
    for i in range(20):
        m = rng.choice(y, 100)
        lo = m.mean() - 1.96 * m.std(ddof=1) / 10
        hi = m.mean() + 1.96 * m.std(ddof=1) / 10
        if lo <= mu <= hi:
            trung += 1
        else:
            truot.append((i + 1, round(lo, 1), round(hi, 1)))
    print(f"  20 khoảng: {trung} chứa trung bình thật; trượt: {truot}")
    tong = [a + b + c + d for a in (-1, 1) for b in (-1, 1) for c in (-1, 1) for d in (-1, 1)]
    print("  tổng 4 đồng xu ±1: các giá trị", sorted(tong), " độ lệch chuẩn", np.std(tong))
    x = np.array([2, 3, 5, 6, 8, 9, 12, 18, 36.0])
    z3 = ((x - x.mean()) / x.std(ddof=1)) ** 3
    print("  (độ lệch/s)^3:", np.round(z3, 2).tolist(), " tổng âm", round(z3[z3 < 0].sum(), 2),
          " tổng dương", round(z3[z3 > 0].sum(), 2), " trung bình", round(z3.mean(), 2))
    for khoi in (10, 20, 40):   # vì sao khối 40 tệ: độ rộng trung bình và độ lệch tâm khoảng (cùng seed với bảng 4.6)
        rng = np.random.default_rng(2026)
        rong, lech = [], []
        for i in range(300):
            xx = xs.ar1(200, 0.7, rng)
            lo, hi = xs.khoang_tin_cay_trung_binh(xx, so_lan=999, do_dai_khoi=khoi, seed=2026 + i)
            rong.append(hi - lo)
            lech.append(abs((lo + hi) / 2 - xx.mean()))
        print(f"  khối {khoi}: độ rộng trung bình {np.mean(rong):.3f}; tâm khoảng lệch khỏi trung bình mẫu {np.mean(lech):.3f}")
    print("  bình phương: tổng (y−8)^2 =", ((x - 8) ** 2).sum(), " tổng (y−9)^2 =", ((x - 9) ** 2).sum(),
          " tổng (y−8) =", (x - 8).sum())


if __name__ == "__main__":
    import pandas as pd

    muc_4_1_va_4_2()
    muc_4_3()
    h = xs.doc_luot_thue()
    d = pd.read_csv(xs.tv.THU_MUC_DU_LIEU / "uci-bike-sharing" / "day.csv")
    muc_4_4(h)
    muc_4_5(d)
    muc_4_6(h)
    muc_bo_sung_vong_2(h)
    print("== Khoảng chung (không tách giờ) ==")
    for ten, y in (("2011", h.loc[h.yr == 0, "cnt"]), ("cả 2011–2012", h["cnt"])):
        print(f"  {ten}: TB {y.mean():.2f}, s {y.std():.2f}, ±1,96s = [{y.mean() - 1.96 * y.std():.1f}; "
              f"{y.mean() + 1.96 * y.std():.1f}]")
