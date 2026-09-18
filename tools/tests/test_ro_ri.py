"""kiem_ro_ri và các kiểm phụ: ≥ 10 ca PHẢI BẮT và ≥ 10 ca PHẢI CHO QUA."""
import numpy as np
import pandas as pd
import pytest

from tv.ro_ri import kiem_chia_tap, kiem_chong_lan, kiem_ro_ri, kiem_scaler


@pytest.fixture(scope="module")
def df():
    rng = np.random.default_rng(0)
    ds = pd.date_range("2024-01-01", periods=120, freq="D")
    khung = []
    for uid, muc in (("A", 10.0), ("B", 50.0)):
        y = muc + np.sin(np.arange(120) * 2 * np.pi / 7) * 3 + rng.normal(0, 1, 120)
        khung.append(pd.DataFrame({"unique_id": uid, "ds": ds, "y": y}))
    return pd.concat(khung, ignore_index=True)


def _nhom(d):
    return d.groupby("unique_id", sort=False)["y"]


# ---------------------------------------------------------------- các hàm feature RÒ RỈ


def f_rolling_centered(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.rolling(7, center=True, min_periods=1).mean()))


def f_rolling_khong_shift(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.rolling(7, min_periods=1).mean()))


def f_zscore_toan_chuoi(d):
    return d.assign(f=_nhom(d).transform(lambda s: (s.shift(1) - s.mean()) / s.std()))


def f_noi_suy_hai_chieu(d):
    d = d.copy()
    d.loc[(d.index % 10 >= 3) & (d.index % 10 <= 8), "y"] = np.nan
    d["y"] = _nhom(d).transform(lambda s: s.interpolate(limit_direction="both"))
    return d


def f_loc_hai_chieu(d):
    """EWMA xuôi rồi ngược — cùng bản chất với filtfilt."""
    def loc(s):
        xuoi = s.ewm(alpha=0.3).mean()
        return xuoi[::-1].ewm(alpha=0.3).mean()[::-1]
    return d.assign(f=_nhom(d).transform(loc).groupby(d["unique_id"]).shift(1))


def f_max_toan_chuoi(d):
    return d.assign(f=_nhom(d).transform("max"))


def f_lag1_cho_h7(d):
    return d.assign(f=_nhom(d).shift(1))


def f_ewm_khong_shift(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.ewm(alpha=0.5).mean()))


def f_rank_toan_chuoi(d):
    return d.assign(f=_nhom(d).rank(pct=True).groupby(d["unique_id"]).shift(1))


def f_dropna_theo_tuong_lai(d):
    """Xoá dòng khi GIÁ TRỊ NGÀY MAI thiếu — dòng quá khứ biến mất khi có thêm dữ liệu."""
    d = d.assign(y_mai=_nhom(d).shift(-1))
    return d.dropna(subset=["y_mai"]).drop(columns="y_mai")


def f_dung_y_hien_tai(d):
    return d.assign(f=d["y"] * 2)


PHAI_BAT = [
    (f_rolling_centered, 1, "cat_tuong_lai"),
    (f_rolling_khong_shift, 1, "nhieu_muc_tieu"),
    (f_zscore_toan_chuoi, 1, "cat_tuong_lai"),
    (f_noi_suy_hai_chieu, None, "cat_tuong_lai"),
    (f_loc_hai_chieu, 1, "cat_tuong_lai"),
    (f_max_toan_chuoi, 1, "cat_tuong_lai"),
    (f_lag1_cho_h7, 7, "nhieu_muc_tieu"),
    (f_ewm_khong_shift, 1, "nhieu_muc_tieu"),
    (f_rank_toan_chuoi, 1, "cat_tuong_lai"),
    (f_dropna_theo_tuong_lai, None, "dong_khac"),
    (f_dung_y_hien_tai, 1, "nhieu_muc_tieu"),
]


@pytest.mark.parametrize(("ham", "h", "loai"), PHAI_BAT, ids=[p[0].__name__ for p in PHAI_BAT])
def test_phai_bat(df, ham, h, loai):
    kq = kiem_ro_ri(ham, df, h=h)
    assert kq.co_ro_ri, f"{ham.__name__} rò rỉ nhưng không bị bắt"
    assert loai in {v.loai for v in kq.van_de}, str(kq)


# ---------------------------------------------------------------- các hàm feature SẠCH


def g_lag1(d):
    return d.assign(f=_nhom(d).shift(1))


def g_rolling_sau_shift(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.shift(1).rolling(7, min_periods=1).mean()))


def g_lag7_cho_h7(d):
    return d.assign(f=_nhom(d).shift(7))


def g_lich(d):
    return d.assign(thu=d["ds"].dt.dayofweek, sin_tuan=np.sin(2 * np.pi * d["ds"].dt.dayofweek / 7),
                    cuoi_tuan=d["ds"].dt.dayofweek >= 5)


def g_expanding_sau_shift(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.shift(1).expanding().mean()))


def g_ewm_sau_shift(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.shift(1).ewm(alpha=0.3).mean()))


def g_diff_tre(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.shift(1).diff(7)))


def g_bien_tinh(d):
    return d.assign(loai=d["unique_id"].map({"A": "nho", "B": "lon"}))


def g_lam_sach_cat_nguong(d):
    """Hàm làm sạch chỉ dùng giá trị hiện tại (được phép với h=None)."""
    return d.assign(y=d["y"].clip(lower=0))


def g_dien_tien(d):
    d = d.copy()
    d.loc[(d.index % 10 >= 3) & (d.index % 10 <= 8), "y"] = np.nan
    d["y"] = _nhom(d).ffill()
    return d


def g_rolling_std_sau_shift_h7(d):
    return d.assign(f=_nhom(d).transform(lambda s: s.shift(7).rolling(14, min_periods=2).std()))


PHAI_CHO_QUA = [
    (g_lag1, 1), (g_rolling_sau_shift, 1), (g_lag7_cho_h7, 7), (g_lich, 1), (g_expanding_sau_shift, 1),
    (g_ewm_sau_shift, 1), (g_diff_tre, 1), (g_bien_tinh, 1), (g_lam_sach_cat_nguong, None),
    (g_dien_tien, None), (g_rolling_std_sau_shift_h7, 7),
]


@pytest.mark.parametrize(("ham", "h"), PHAI_CHO_QUA, ids=[p[0].__name__ for p in PHAI_CHO_QUA])
def test_phai_cho_qua(df, ham, h):
    kq = kiem_ro_ri(ham, df, h=h)
    assert not kq.co_ro_ri, str(kq)


def test_bao_cao_chi_ro_cot(df):
    kq = kiem_ro_ri(lambda d: g_lag1(d).assign(ro=f_max_toan_chuoi(d)["f"]), df)
    assert kq.cot_ro_ri == ["ro"]
    with pytest.raises(AssertionError, match="ro"):
        kq.khang_dinh_sach()


def test_moc_cat_tuong_minh_va_mot_chuoi(df):
    mot = df[df["unique_id"] == "A"].drop(columns="unique_id")
    kq = kiem_ro_ri(lambda d: d.assign(f=d["y"].rolling(5, center=True).mean()), mot,
                    cac_moc_cat=[pd.Timestamp("2024-03-01")], cot_id=None, h=None)
    assert kq.co_ro_ri


def test_ham_lam_mat_khoa_bao_loi(df):
    with pytest.raises(ValueError, match="khoá"):
        kiem_ro_ri(lambda d: d[["y"]], df)


# ---------------------------------------------------------------- kiểm phụ


def test_chia_tap(df):
    train = df[df["ds"] < "2024-04-01"]
    test = df[df["ds"] >= "2024-04-01"]
    assert not kiem_chia_tap(train, test).co_ro_ri
    xao = df.sample(frac=1, random_state=0)
    assert kiem_chia_tap(xao.iloc[:180], xao.iloc[180:]).co_ro_ri
    assert kiem_chia_tap(train, test, gap=pd.Timedelta(days=3)).co_ro_ri


class _Scaler:
    def __init__(self, X):
        self.mean_ = np.mean(X, axis=0)
        self.var_ = np.var(X, axis=0)


def test_scaler():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(100, 2)) + np.linspace(0, 5, 100)[:, None]
    train = X[:70]
    assert not kiem_scaler(_Scaler(train), train).co_ro_ri
    kq = kiem_scaler(_Scaler(X), train)
    assert kq.co_ro_ri and "mean_" in kq.cot_ro_ri
    with pytest.raises(ValueError):
        kiem_scaler(object(), train)


def test_scaler_sklearn_neu_co():
    preprocessing = pytest.importorskip("sklearn.preprocessing")
    rng = np.random.default_rng(2)
    X = rng.normal(size=(50, 3)).cumsum(axis=0)
    assert not kiem_scaler(preprocessing.StandardScaler().fit(X[:30]), X[:30]).co_ro_ri
    assert kiem_scaler(preprocessing.MinMaxScaler().fit(X), X[:30]).co_ro_ri


def test_chong_lan_cua_so():
    ds = pd.date_range("2024-01-01", periods=100, freq="h")
    # cửa sổ input 24, output 6, stride 1; mục tiêu = 6 giờ sau input
    muc_tieu = [(i, ds[i + 24:i + 30]) for i in range(0, 70)]
    sai_train = pd.DataFrame({"ds": np.concatenate([m for i, m in muc_tieu if i < 60])})
    sai_val = pd.DataFrame({"ds": np.concatenate([m for i, m in muc_tieu if i >= 60])})
    assert kiem_chong_lan(sai_train, sai_val, cot_id=None).co_ro_ri
    # đúng: chia theo thời gian trước — mục tiêu train kết thúc trước mục tiêu val đầu tiên
    dung_train = pd.DataFrame({"ds": np.concatenate([m for i, m in muc_tieu if i + 30 <= 84])})
    dung_val = pd.DataFrame({"ds": np.concatenate([m for i, m in muc_tieu if i + 24 >= 84])})
    assert not kiem_chong_lan(dung_train, dung_val, cot_id=None).co_ro_ri
