"""Sinh bộ slide chia sẻ "Dữ liệu cho dự báo" (buổi 1–15) ra trinh-chieu/nen-mong-va-du-lieu-v2.pptx.

Chạy:  uv run --with python-pptx --with pillow --with matplotlib python trinh-chieu/sinh_slide_du_lieu.py [--muc-luc]

- Hình lấy thẳng từ buoi-NN/hinh/, con số chép từ buoi-NN/tai-lieu.md.
- Công thức (CONG_THUC, CT_CODE) viết bằng mathtext của matplotlib, render ra ảnh PNG lúc chạy; không cần LaTeX.
- Ghi chú người nói (khán giả không thấy) lấy từ trinh-chieu/loi-noi.md: mỗi slide một mục "## <mã>" là lời thuyết
  trình. Script dừng nếu slide nào thiếu lời.
- trinh-chieu/doc-kem.md là bài đọc kèm phát cùng slide: mỗi slide một mục "## N. <tiêu đề slide>" kèm dòng
  "<!-- ma: ... -->". Script báo mục thiếu hoặc lệch số/tiêu đề; --doc-kem đánh số lại theo thứ tự slide.
  --muc-luc: in khung mục lục đúng thứ tự slide.
- Slide chỉ ghi từ khoá; script cảnh báo slide nào quá GIOI_HAN_CHU âm tiết.
"""

from __future__ import annotations

import hashlib
import re
import sys
import tempfile
from pathlib import Path

import matplotlib
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from noi_dung_code import CODE  # noqa: E402, I001  (nội dung slide code, một slide mỗi mục 4.x)

# Bản 2 (2026-09-29, tinh chỉnh theo ghi chú tự học Note.docx) ghi ra file mới; bản 1 nen-mong-va-du-lieu.pptx giữ nguyên.
RA = GOC / "trinh-chieu" / "nen-mong-va-du-lieu-v2.pptx"
DOC_KEM = GOC / "trinh-chieu" / "doc-kem.md"
LOI_NOI = GOC / "trinh-chieu" / "loi-noi.md"  # lời thuyết trình → ghi chú người nói (khán giả không thấy)
TAM = Path(tempfile.mkdtemp(prefix="cong-thuc-"))  # ảnh công thức sinh mỗi lần chạy, không vào git

FONT = "Arial"
INK = "1B2A41"
MUTED = "5B6778"
NHAT = "F3F5F8"
VIEN = "D5DBE3"
DO, DO_NHAT = "C0392B", "FBEAE8"
XANH, XANH_NHAT = "1E8449", "E6F4EC"
LAM, LAM_NHAT = "2E6FBF", "E8F0FA"
TRANG = "FFFFFF"

PHAN = {
    "A": ("Khái niệm nền", "0F8B8D", "Buổi 1–13", "6 ô · quantile · p-value · UTC · biểu đồ · ACF · ADF/KPSS · tương quan · feature"),
    "B": ("Vấn đề dữ liệu", "D9642B", "Buổi 3–13", "múi giờ · thiếu · MNAR · mã trá hình · ngoại lai · điểm gãy · bộ lọc · rò rỉ"),
    "C": ("Bảng tra & từ điển", "A77B06", "24 lỗi · 10 chỗ nhầm · 100 từ", "dấu hiệu, cách kiểm, cách sửa · Việt – Anh"),
    "D": ("Đánh giá trung thực", "6C4AB6", "Buổi 14–15", "phần dư · chỉ số · chia theo thời gian · rolling origin · DM"),
    "E": ("Quy trình tiền xử lý", "2E6FBF", "Buổi 1–15", "làm một lần · lặp ở mỗi cutoff · kiểm"),
    "F": ("Dữ liệu & phía trước", "4A5568", "14 bộ dữ liệu", "bộ dữ liệu · tra theo buổi · buổi sau còn gì"),
}

# Đếm theo âm tiết tiếng Việt. Slide khái niệm/vấn đề: tiêu đề + câu "hiểu đơn giản" + 3 thẻ ngắn.
GIOI_HAN_CHU = 90
KHONG_DEM: set[int] = set()
# Thuật ngữ tiếng Anh hiện dưới tiêu đề mỗi slide, thống nhất theo phu-luc/E-tu-dien-thuat-ngu.md.
EN = {
    "goc-tam": "forecast origin (cutoff) · forecast horizon h",
    "baseline": "baseline · naive · seasonal naive · drift",
    "sai-so-ao": "in-sample error · rolling forecast",
    "quantile": "quantile · median · pinball loss · coverage",
    "khoang-tin-cay": "prediction interval vs confidence interval · central limit theorem (CLT) · 1/√n",
    "phan-ra-cach": "classical decomposition · STL · MSTL · LOESS",
    "newsvendor": "newsvendor problem · pinball loss · quantile forecast",
    "do-lech-chuan": "mean · variance · standard deviation · z-score",
    "ar": "autoregressive model AR(1) · coefficient ρ (φ)",
    "sai-phan-la-gi": "differencing · seasonal differencing · detrending",
    "mcar": "missing data mechanism · MCAR / MAR / MNAR",
    "pho": "frequency · spectrum · periodogram · energy",
    "cua-so": "expanding window · sliding window · gap · refit",
    "mo-hinh": "model · parameter · fit · training set · test period · overfitting",
    "bon-baseline": "mean · naive · seasonal naive · drift",
    "prewhitening": "prewhitening · AR filter · cross-correlation",
    "utc": "UTC · time zone · daylight saving time (DST) · naive / aware timestamp",
    "dang-dai": "long format · wide format",
    "mua-vu": "trend · seasonality · cycle",
    "doc-hinh": "axis · legend · heatmap · seasonal plot",
    "phan-ra": "decomposition (additive / multiplicative) · residual · STL / MSTL",
    "acf": "autocorrelation function (ACF) · lag",
    "dung": "stationarity · white noise · random walk · trend-stationary",
    "scatter": "scatter plot · Pearson / Spearman correlation · Anscombe's quartet",
    "dac-trung": "time series features · scale-free · feature table",
    "biet-truoc": "feature · calendar feature · lag feature",
    "shift-rolling": "lag feature · rolling feature · shift",
    "ma-tran": "data leakage · look-ahead bias",
    "mui-gio": "time zone · DST transition · UTC conversion",
    "gop": "aggregation · resample · missing values as zero",
    "bieu-do-sai": "dual axis · truncated y-axis · misleading chart",
    "dao-dong": "nominal vs real value · inflation adjustment · per capita · Box-Cox",
    "doi-nguoc": "back-transformation bias · bias adjustment",
    "chu-ky-sai": "classical decomposition · MSTL · robust decomposition",
    "sai-phan": "over-differencing · ADF / KPSS test",
    "tuong-quan-gia": "spurious correlation · Durbin–Watson statistic",
    "chu-u": "nonlinear relationship · CDD / HDD (degree days) · mutual information",
    "thieu-moc": "missing timestamps vs missing values · reindex",
    "tra-hinh": "sentinel value · flag column · quality flag",
    "dien": "imputation · forward fill · causal imputation · MNAR",
    "masking": "outlier · z-score · masking · MAD · Hampel filter",
    "tet": "event log · dummy variable · moving holiday",
    "covid": "structural break · changepoint · PELT",
    "aliasing": "periodogram · aliasing · Nyquist frequency · low-pass filter · downsampling",
    "loc-tuong-lai": "causal filter · trailing / centered moving average · EWMA",
    "ro-ri": "data leakage · target encoding · fit on training data only",
    "ngoai-sinh": "exogenous variable · ex-ante vs ex-post · archived forecasts",
    "chi-so": "MAE · RMSE · mean error (bias)",
    "phan-tram": "MAPE · sMAPE · WAPE (weighted absolute percentage error)",
    "he-so-lech": "skewness · long right / left tail",
    "phan-phoi-chuan": "normal distribution · 68–95 rule · quantile 0.975 = 1.96",
    "hoan-vi": "permutation test · shuffled labels · p-value",
    "seasonal-subseries": "seasonal plot · subseries plot · multiple seasonality",
    "lag-plot": "lag plot · autocorrelation at lag k",
    "truc-y-cat": "truncated y-axis · dual axis · index to 100",
    "tron-nam": "pooling years · level shift · colour by time",
    "guerrero": "Guerrero method · coefficient of variation (CV) · Box-Cox λ",
    "exp-trung-vi": "back-transformation · median vs mean · bias adjustment",
    "ty-le-mau-hinh": "residual pattern ratio · calendar grouping",
    "stl-loess": "STL · LOESS (local regression) · trend window",
    "ljung-box-q": "Ljung–Box Q* · χ² distribution · degrees of freedom (model_df)",
    "random-walk": "random walk · variance grows with √n · naive forecast",
    "entropy": "spectral entropy · normalized power spectrum",
    "do-phan-giai": "measurement resolution · stuck sensor · flat-line detection",
    "dien-nhan-qua": "causal imputation · two-sided interpolation · cutoff test",
    "z-score-masking": "z-score · 3σ rule · masking / swamping",
    "mad-hampel": "median absolute deviation (MAD) · 1.4826 · Hampel filter",
    "xu-ly-bat-thuong": "winsorizing · event log · dummy variable",
    "penalty": "changepoint · cost function · PELT · penalty β",
    "nyquist": "Nyquist frequency · sampling frequency f_s · aliasing",
    "sau-ho-loc": "Savitzky–Golay · Butterworth sosfilt / sosfiltfilt · Kalman filter / smoother",
    "kiem-nhan-qua": "causality test · perturb the tail · tolerance",
    "ca-chuoi": "full-sample leakage · scaler fit · target encoding",
    "kiem-ro-ri": "leakage test · truncation test · target perturbation",
    "ex-ante": "exogenous variable · ex-ante vs ex-post · point-in-time",
    "mape-lech": "MAPE asymmetry · under-forecast bias · sMAPE",
    "spearman": "Spearman rank correlation · Kendall τ · Pearson r",
    "durbin-watson": "Durbin–Watson statistic · regression residuals · spurious regression",
    "cdd-hdd": "cooling / heating degree days (CDD / HDD) · base temperature 65 °F",
    "mi": "mutual information (MI) · nat · nonlinear dependence",
    "hoan-vi-khoi": "block permutation test · autocorrelation · null distribution",
    "mase": "MASE (mean absolute scaled error) · RMSSE · in-sample scaling",
    "lam-tron": "smoothing · centered moving average · window w",
    "thang-log": "log scale · percentage change · log₁₀",
    "dieu-chinh": "calendar adjustment · CPI deflation (real value) · per capita",
    "log": "log transformation · multiplicative → additive",
    "robust": "robust decomposition · robustness weights (bisquare)",
    "cach-dien": "imputation · forward fill · linear / spline interpolation · seasonal · neighbour station",
    "khu-nhieu": "signal + noise · trailing / centered moving average · causal filter",
    "ewma": "exponentially weighted moving average (EWMA) · α, span, com · phase lag",
    "muc-tieu-lam-tron": "target smoothing · evaluation on the raw series",
    "chia-ngau-nhien": "random split · K-fold · hold-out · rolling origin",
    "kfold": "K-fold cross-validation · hold-out set",
    "rolling-origin": "rolling origin · cutoff · expanding / sliding window · gap",
    "ba-doan": "train / validation / test · hold-out",
    "quy-trinh": "preprocessing pipeline · point-in-time",
    "du-bao-la-gi": "forecast vs goal vs plan · forecastability",
    "phan-phoi": "distribution · histogram · cumulative distribution (CDF) · skewness · standard deviation",
    "con-so-bao": "loss function · squared / absolute / pinball loss · point forecast",
    "phieu-6-o": "forecasting problem statement · decision · target variable · granularity",
    "du-bao-cuon": "rolling forecast · rolling origin · out-of-sample",
    "do-chi-tiet": "granularity · temporal aggregation · evaluation level",
    "khoang": "prediction interval · coverage · empirical quantile",
    "kiem-dinh": "null hypothesis H0 · p-value · significance level α · permutation test",
    "bootstrap": "bootstrap · block bootstrap · confidence interval · i.i.d.",
    "resample": "resample · closed / label · sum vs mean aggregation",
    "merge-asof": "as-of join (merge_asof) · direction=\"backward\" · tolerance",
    "bo-bieu-do": "seasonal plot · subseries plot · lag plot · heatmap · boxplot · ACF",
    "boxplot": "boxplot · interquartile range (IQR) · median",
    "box-cox": "Box-Cox transformation · λ (lambda) · Guerrero method · Yeo-Johnson",
    "f-s": "strength of trend F_T · strength of seasonality F_S",
    "pacf": "partial autocorrelation function (PACF) · AR(1)",
    "ljung-box": "Ljung–Box test · white noise · model_df",
    "adf-kpss-la-gi": "augmented Dickey–Fuller (ADF) · KPSS · unit root · null hypothesis H0",
    "adf-kpss": "ADF · KPSS · regression=\"c\" / \"ct\"",
    "ccf": "cross-correlation function (CCF) · prewhitening · lead / lag",
    "truot": "rolling correlation · regime",
    "granger": "Granger causality test · confounder",
    "do-kho": "forecastability · sMAPE · MASE · scale-free error",
    "ban-do-pca": "PCA · principal component (PC1, PC2) · feature space",
    "dtw": "dynamic time warping (DTW) · z-score normalization · Ward clustering",
    "abc-xyz": "ABC–XYZ classification · coefficient of variation (CV)",
    "feature-lich": "cyclical encoding (sin/cos) · Fourier terms · moving holiday",
    "mnar": "missing data mechanism · MCAR / MAR / MNAR",
    "so-sanh-dien": "imputation evaluation · artificial masking · point vs block masking",
    "bon-loai": "additive outlier (AO) · level shift (LS) · temporary change (TC) · variance change",
    "hampel": "MAD · Hampel filter · winsorize · IQR rule",
    "pelt": "changepoint detection · PELT · penalty",
    "bo-loc": "moving average · EWMA · Savitzky–Golay · Butterworth · Kalman filter · phase lag",
    "phan-du": "residual diagnostics · fitted values · Ljung–Box · Jarque–Bera",
    "dm": "Diebold–Mariano test · loss differential · HLN correction",
}

# Mỗi mục lý thuyết 4.x của buổi 1–15 phải nằm ở ít nhất một slide (script dừng nếu thiếu).
PHU = {
    1: {"4.1": ["du-bao-la-gi", "goc-tam"], "4.2": ["phieu-6-o"], "4.3": ["baseline", "bon-baseline"], "4.4": ["sai-so-ao", "du-bao-cuon", "mo-hinh"],
        "4.5": ["do-chi-tiet"], "4.6": ["quantile", "newsvendor"]},
    2: {"4.1": ["quantile", "phan-phoi"], "4.2": ["con-so-bao", "do-lech-chuan", "he-so-lech"], "4.3": ["phan-phoi-chuan", "khoang", "khoang-tin-cay"], "4.4": ["scatter"],
        "4.5": ["kiem-dinh", "hoan-vi"], "4.6": ["bootstrap", "bootstrap-buoc", "khoang-tin-cay"]},
    3: {"4.1": ["utc"], "4.2": ["mui-gio"], "4.3": ["resample"], "4.4": ["merge-asof", "mui-gio"], "4.5": ["dang-dai"]},
    4: {"4.1": ["mua-vu", "doc-hinh"], "4.2": ["lam-tron", "thang-log", "gop", "bo-bieu-do"], "4.3": ["bo-bieu-do", "seasonal-subseries"], "4.4": ["boxplot"],
        "4.5": ["lag-plot", "acf"], "4.6": ["truc-y-cat", "tron-nam", "bieu-do-sai"]},
    5: {"4.1": ["dieu-chinh", "dao-dong"], "4.2": ["dieu-chinh", "dao-dong"], "4.3": ["log", "dao-dong"], "4.4": ["box-cox", "guerrero"], "4.5": ["exp-trung-vi", "doi-nguoc"],
        "4.6": ["doi-nguoc"]},
    6: {"4.1": ["phan-ra", "phan-ra-cach"], "4.2": ["phan-ra", "phan-ra-cach"], "4.3": ["ty-le-mau-hinh", "chu-ky-sai"], "4.4": ["phan-ra-cach", "stl-loess"], "4.5": ["f-s"],
        "4.6": ["robust", "chu-ky-sai"]},
    7: {"4.1": ["acf"], "4.2": ["pacf", "ar"], "4.3": ["ljung-box", "ljung-box-q"], "4.4": ["dung", "random-walk", "bon-chuoi"], "4.5": ["adf-kpss-la-gi", "adf-kpss"], "4.6": ["sai-phan", "sai-phan-la-gi", "quy-trinh-chuoi-la"]},
    8: {"4.1": ["scatter", "spearman"], "4.2": ["durbin-watson", "tuong-quan-gia"], "4.3": ["cdd-hdd", "mi", "hoan-vi-khoi", "chu-u"], "4.4": ["ccf", "prewhitening"], "4.5": ["truot"],
        "4.6": ["granger"]},
    9: {"4.1": ["dac-trung"], "4.2": ["entropy", "pho"], "4.3": ["do-kho"], "4.4": ["ban-do-pca"], "4.5": ["dtw"],
        "4.6": ["abc-xyz"]},
    10: {"4.1": ["thieu-moc"], "4.2": ["mcar", "mnar"], "4.3": ["tra-hinh", "do-phan-giai"], "4.4": ["cach-dien", "so-sanh-dien"], "4.5": ["so-sanh-dien"],
         "4.6": ["dien-nhan-qua", "dien"]},
    11: {"4.1": ["bon-loai"], "4.2": ["z-score-masking", "masking"], "4.3": ["mad-hampel", "hampel"], "4.4": ["xu-ly-bat-thuong", "tet"],
         "4.5": ["penalty", "pelt"], "4.6": ["covid"]},
    12: {"4.1": ["khu-nhieu", "loc-tuong-lai"], "4.2": ["aliasing", "pho"], "4.3": ["nyquist", "aliasing"], "4.4": ["ewma", "sau-ho-loc", "bang-bo-loc", "bo-loc"],
         "4.5": ["kiem-nhan-qua", "loc-tuong-lai"], "4.6": ["loc-tuong-lai", "muc-tieu-lam-tron"]},
    13: {"4.1": ["biet-truoc"], "4.2": ["shift-rolling"], "4.3": ["feature-lich"], "4.4": ["ca-chuoi", "ro-ri"], "4.5": ["kiem-ro-ri", "ro-ri"],
         "4.6": ["ex-ante", "ngoai-sinh"]},
    14: {"4.1": ["baseline"], "4.2": ["phan-du"], "4.3": ["chi-so"], "4.4": ["phan-tram", "mape-lech"], "4.5": ["mase"],
         "4.6": ["phan-tram", "mase"]},
    15: {"4.1": ["chia-ngau-nhien"], "4.2": ["kfold", "rolling-origin"], "4.3": ["rolling-origin", "cua-so"], "4.4": ["ba-doan"],
         "4.5": ["dm"]},
}
# Slide tổng hợp không neo vào mục 4.x nào (neo sẽ kéo slide code tới sau nó), chỉ thêm vào bảng "Tra theo buổi".
THEM_TRA = {"quy-trinh-tuong-quan": 8, "bang-chi-so": 14, "doc-kiem-dinh": 15}
TRA_THEO_BUOI: list = []  # slide bảng/sơ đồ/nền tối: không đếm chữ
MUC: list[tuple[str, str]] = []  # (mã, tiêu đề) theo thứ tự slide
PHAN_CUA: dict[str, str] = {}  # mã slide → phần A–F

# Từ điển Việt – Anh (3 slide × 20 từ), tên tiếng Anh theo phu-luc/E-tu-dien-thuat-ngu.md.
TU_DIEN = [
    ("Từ điển Việt – Anh 1/5: nền móng, hiểu dữ liệu", [
        ("gốc dự báo, mốc cắt", "forecast origin, cutoff", "1"), ("tầm dự báo h", "forecast horizon", "1"),
        ("dự báo cuốn", "rolling forecast", "1"), ("sai số ảo", "in-sample error", "1"),
        ("quantile, trung vị", "quantile, median", "2"), ("pinball loss", "pinball / quantile loss", "2"),
        ("tỷ lệ phủ", "coverage", "2"), ("block bootstrap", "block bootstrap", "2"),
        ("giờ mùa hè", "daylight saving time (DST)", "3"), ("timestamp naive / aware", "naive / aware timestamp", "3"),
        ("định dạng dài / rộng", "long / wide format", "3"), ("gộp tần suất", "resample, aggregate", "3"),
        ("xu hướng", "trend", "4"), ("mùa vụ, mùa vụ kép", "seasonality, multiple seasonality", "4"),
        ("chu kỳ", "cycle", "4"), ("tự tương quan", "autocorrelation (ACF)", "4"),
        ("điều chỉnh lịch", "calendar adjustment", "5"), ("giá thực / danh nghĩa", "real / nominal value", "5"),
        ("hiệu chỉnh bias", "bias adjustment (back-transform)", "5"), ("phân rã cộng / nhân", "additive / multiplicative decomposition", "6")]),
    ("Từ điển Việt – Anh 2/5: dừng, làm sạch", [
        ("phần dư", "residual, remainder", "6"), ("tự tương quan riêng", "partial autocorrelation (PACF)", "7"),
        ("nhiễu trắng", "white noise", "7"), ("tính dừng", "stationarity", "7"),
        ("bước ngẫu nhiên", "random walk", "7"), ("sai phân", "differencing", "7"),
        ("kiểm định nghiệm đơn vị", "unit root test (ADF, KPSS)", "7"), ("tương quan giả", "spurious correlation", "8"),
        ("tương quan chéo", "cross-correlation (CCF)", "8"), ("prewhitening", "prewhitening", "8"),
        ("biến ngoại sinh", "exogenous variable, covariate", "8"), ("đặc trưng chuỗi", "time series feature", "9"),
        ("hệ số biến thiên", "coefficient of variation (CV)", "9"), ("thiếu mốc / thiếu giá trị", "missing timestamp / value", "10"),
        ("điền dữ liệu", "imputation", "10"), ("mã trá hình", "sentinel value", "10"),
        ("cột cờ", "flag column", "10"), ("cảm biến đứng yên", "stuck sensor", "10"),
        ("thiếu MCAR / MAR / MNAR", "missing completely at random / at random / not at random", "10"),
        ("ngoại lai", "outlier", "11")]),
    ("Từ điển Việt – Anh 3/5: rò rỉ, đánh giá", [
        ("che khuất / gắn cờ oan", "masking / swamping", "11"), ("độ lệch tuyệt đối trung vị", "median absolute deviation (MAD)", "11"),
        ("điểm gãy", "structural break, changepoint", "11"), ("nhật ký sự kiện, biến giả", "event log, dummy variable", "11"),
        ("bộ lọc nhân quả", "causal filter", "12"), ("tần số Nyquist", "Nyquist frequency", "12"),
        ("rò rỉ tương lai", "data leakage, look-ahead bias", "13"), ("feature trễ / cửa sổ trượt", "lag / rolling feature", "13"),
        ("point-in-time", "point-in-time", "13"), ("trong mẫu / ngoài mẫu", "in-sample / out-of-sample", "14"),
        ("sai số tuyệt đối trung bình", "mean absolute error (MAE)", "14"), ("căn sai số bình phương TB", "root mean squared error (RMSE)", "14"),
        ("độ chệch", "mean error (bias)", "14"), ("sai số có chia thang", "scaled error (MASE, RMSSE)", "14"),
        ("backtest", "backtest", "15"), ("rolling origin", "rolling origin, time series cross-validation", "15"),
        ("cửa sổ mở rộng / trượt", "expanding / sliding window", "15"), ("khoảng đệm", "gap", "15"),
        ("tập giữ lại", "hold-out set", "15"), ("kiểm định Diebold–Mariano", "Diebold–Mariano test", "15")]),
    ("Từ điển Việt – Anh 4/5: xác suất, biểu đồ, biến đổi", [
        ("dự báo điểm / phân phối", "point / probabilistic forecast", "1"), ("bài toán newsvendor", "newsvendor problem", "1"),
        ("hàm phân phối tích luỹ", "cumulative distribution function (CDF)", "1"),
        ("phân phối chuẩn", "normal distribution", "2"), ("hệ số lệch / độ nhọn", "skewness / kurtosis", "2, 9"),
        ("khoảng tin cậy", "confidence interval", "2"), ("mức ý nghĩa α", "significance level", "2"),
        ("định lý giới hạn trung tâm", "central limit theorem (CLT)", "2"),
        ("tự hồi quy bậc một", "autoregressive model AR(1)", "2, 7"),
        ("cỡ mẫu hiệu dụng", "effective sample size", "2"), ("hạt giống ngẫu nhiên", "random seed", "2"),
        ("chuỗi đều / không đều", "regular / irregular time series", "3"), ("chu kỳ mùa vụ m", "seasonal period", "4"),
        ("trục kép / trục y cắt", "dual axis / truncated y-axis", "4"), ("thang log", "log scale", "4"),
        ("năm gốc", "base year (CPI)", "5"), ("trên đầu người", "per capita", "5"),
        ("phân phối log-normal", "log-normal distribution", "5"), ("trung bình trượt 2×m", "2×m moving average (2×m-MA)", "6"),
        ("độ mạnh mùa vụ", "strength of seasonality F_S", "6")]),
    ("Từ điển Việt – Anh 5/5: tương quan, làm sạch, bộ lọc", [
        ("hồi quy đơn, R²", "simple regression, R-squared", "8"), ("hoán vị theo khối", "block permutation", "8"),
        ("biến gây nhiễu", "confounder", "2, 8"), ("phân cụm Ward", "Ward hierarchical clustering", "9"),
        ("nhu cầu gián đoạn", "intermittent demand", "9, 19"), ("trần cảm biến", "sensor ceiling / saturation", "10"),
        ("độ phân giải", "measurement resolution", "10"), ("nội suy spline", "spline interpolation", "10"),
        ("che nhân tạo", "artificial masking", "10"), ("Kalman filter / smoother", "Kalman filter / smoother", "10, 12"),
        ("winsorize", "winsorizing", "11"), ("CUSUM, CROPS", "CUSUM, CROPS (penalty scan)", "11"),
        ("hàm chi phí", "cost function", "11"), ("tần số lấy mẫu", "sampling frequency f_s", "12"),
        ("periodogram, Welch", "periodogram, Welch method", "12"), ("wavelet", "wavelet denoising", "12"),
        ("kiểm nhiễu mục tiêu", "target-noise test", "13"), ("mã hoá target", "target encoding", "13"),
        ("tự hiệp phương sai", "autocovariance", "15"), ("phân phối t", "Student's t-distribution", "15")]),
]


# Nội dung slide khái niệm (khuôn: mục tiêu, là gì, cao/thấp nghĩa là gì hoặc nhận ra thế nào, ví dụ có số).
# "thang": các mốc của thang đọc (giá trị, nghĩa); "doc": thay thang bằng lời khi khái niệm không có thang số.
KN = {
    "goc-tam": dict(
        tieu="Đứng ở gốc, chỉ thấy quá khứ", phan="A", buoi="Buổi 1", hinh=(1, "kn-tam-du-bao-h"),
        muc="Biết mình đang đứng ở thời điểm nào và phải nhìn xa bao nhiêu, để chỉ dùng dữ liệu có trước lúc đó.",
        la_gi="Gốc dự báo là lúc ra dự báo. Tầm h là số bước phải đoán, đếm từ gốc.",
        doc_tieu="Tầm xa hay gần nghĩa là gì",
        thang=[("h nhỏ", "sát gốc, còn nhiều số liệu mới để dựa vào"), ("h lớn", "xa gốc, khó hơn, sai số thường lớn hơn")],
        vi_du="Đứng ở 00:00 thứ Hai, dự báo 168 giờ tới: h = 1 là 01:00, h = 168 là giờ cuối Chủ nhật."),
    "baseline": dict(
        tieu="0,38 là tốt hay xấu? Phải có baseline", phan="A", buoi="Buổi 1, 14", hinh=(14, "bon-baseline"),
        muc="Có một mốc để biết mô hình tốt hơn hay tệ hơn cách đoán đơn giản nhất.",
        la_gi="Cách dự báo đơn giản nhất: naive lấy giá trị cuối, seasonal naive lấy cùng vị trí mùa trước, cộng mean và drift. Độ trễ phải ≥ tầm dự báo.",
        doc_tieu="So với baseline thế nào",
        thang=[("thấp hơn", "mô hình có giá trị"), ("ngang", "chưa đáng công"), ("cao hơn", "còn thua cách đơn giản nhất")],
        vi_du="Phải thắng cả bốn: trên M4 theo ngày, naive (MASE 0,835) và drift (0,810) còn thắng seasonal naive (1,077).",
        dg="được 7 điểm: cả lớp 9 thì là kém, cả lớp 4 thì là giỏi; baseline là điểm của cả lớp."),
    "sai-so-ao": dict(
        tieu="Nhìn trộm đáp án thì sai số đẹp giả", phan="A", buoi="Buổi 1", hinh=(1, "sai-so-ao"),
        muc="Đo đúng mô hình sẽ sai bao nhiêu khi dùng thật, chứ không phải lúc nó đã thấy đáp án.",
        la_gi="Sai số ảo là sai số đo trên chính dữ liệu đã dùng để dựng dự báo, nên mô hình như đã thấy trước đáp án.",
        doc="Sai số ảo luôn thấp hơn sai số thật. Hai con số càng cách xa, mô hình càng học thuộc thay vì học quy luật.",
        doc_tieu="Nhận ra thế nào",
        vi_du="Cùng một mô hình: nhìn trộm thì MAE 0,380, đứng đầu bảng; chấm trung thực thì 0,508, thua cả trung bình 4 tuần.",
        dg="nhìn trộm thì ra sai số ảo; cách chấm trung thực ở slide sau."),
    "do-chi-tiet": dict(
        tieu="Chấm theo giờ hay theo tuần: thứ hạng đảo", phan="A", buoi="Buổi 1", hinh=(1, "tong-tuan"),
        muc="Chấm mô hình ở đúng mức mà quyết định sẽ dùng.",
        la_gi="Độ chi tiết là mức gộp của dự báo và của phép chấm: theo giờ, ngày hay tuần; từng hộ hay cả khu.",
        doc_tieu="Nhận ra thế nào",
        doc="Gộp lên mức thô thì phần lệch lên và lệch xuống bù trừ nhau, nên thứ hạng các mô hình có thể đổi hẳn.",
        vi_du="Theo giờ, trung bình 4 tuần (0,490) thắng bảng lịch (0,508). Theo tổng tuần, bảng lịch (16,4) thắng (27,9).",
        dg="chấm theo giờ thì thắng theo giờ; chấm theo tuần thì thắng theo tuần."),
    "quantile": dict(
        tieu="Thiếu và thừa đắt khác nhau: dùng quantile", phan="A", buoi="Buổi 1–2", hinh=(2, "kn-quantile-trung-vi"),
        muc="Chọn mức dự báo cân được cái giá của thiếu và cái giá của thừa.",
        la_gi="Quantile p là giá trị nhỏ nhất mà ít nhất tỷ lệ p số liệu nằm dưới hoặc bằng nó; trung vị là quantile 0,5. Dự báo quantile được chấm bằng pinball loss.",
        thang=[("p = 0,1", "thấp, hay thiếu"), ("p = 0,5", "trung vị"), ("p = 0,9", "cao, ít khi thiếu nhưng hay thừa")],
        vi_du="Thiếu mất 4 đồng, thừa mất 1 đồng thì đặt ở quantile 4 / (4 + 1) = 0,8. Với 10 ngày mẫu, mua 9 kWh tốn ít nhất."),
    "phan-phoi": dict(
        tieu="Phân phối: nhìn hình dạng trước khi tóm", phan="A", buoi="Buổi 1–2", hinh=(2, "histogram-tich-luy"),
        muc="Biết số liệu hay rơi vào đâu và lệch về phía nào, trước khi tóm nó bằng một con số.",
        la_gi="Histogram đếm số lần gặp mỗi khoảng giá trị. Đường tích luỹ cho biết bao nhiêu phần số liệu nằm dưới mỗi mốc.",
        doc_tieu="Nhận ra thế nào",
        doc="Đuôi bên phải dài (lệch phải) thì trung bình lớn hơn trung vị. Độ lệch chuẩn càng lớn, số liệu càng tản rộng.",
        vi_du="Lượt thuê xe theo giờ: trung bình 189 nhưng trung vị chỉ 142, vì vài giờ rất đông kéo trung bình lên."),
    "con-so-bao": dict(
        tieu="Cách phạt quyết định con số nên báo", phan="A", buoi="Buổi 2", hinh=(2, "ham-mat-mat"),
        muc="Báo đúng con số (trung bình, trung vị hay quantile) theo cách sai lệch bị tính tiền.",
        la_gi="Hàm mất mát là quy tắc tính phạt cho một dự báo sai. Ba kiểu hay gặp: tuyệt đối, bình phương và pinball.",
        doc_tieu="Phạt kiểu nào thì báo gì",
        thang=[("bình phương", "báo trung bình"), ("tuyệt đối", "báo trung vị"), ("pinball τ", "báo quantile τ")],
        vi_du="Lượt thuê xe: phạt bình phương thấp nhất ở 189,46; phạt tuyệt đối ở 142; pinball τ = 0,9 ở 452."),
    "khoang": dict(
        tieu="Khoảng 95% phải phủ thật 95%", phan="A", buoi="Buổi 2", hinh=(2, "khoang-2011-2012"),
        muc="Kiểm lời hứa của khoảng dự báo: nói 95% thì có thật là 95% không.",
        la_gi="Khoảng dự báo 95% là vùng được hứa sẽ chứa giá trị thật 95 lần trên 100. Tỷ lệ phủ là tỷ lệ thật sự rơi vào.",
        doc_tieu="Tỷ lệ phủ cao hay thấp nghĩa là gì",
        thang=[("dưới 95%", "khoảng quá hẹp, tự tin quá"), ("≈ 95%", "giữ đúng lời hứa"), ("gần 100%", "khoảng rộng thừa")],
        vi_du="1,96 là quantile 0,975 của phân phối chuẩn. Khoảng ±1,96s từ 2011 phủ 96,4% năm 2011 nhưng chỉ 72,5% năm 2012.",
        dg="hứa 95% thì cứ 100 lần phải trúng khoảng 95 lần."),
    "kiem-dinh": dict(
        tieu="p-value: nếu H0 đúng, dữ liệu này hiếm cỡ nào?", phan="A", buoi="Buổi 2", hinh=(2, "kn-kiem-dinh-gia-thuyet-khong-h0"),
        muc="Phân biệt một chênh lệch có thật với một chênh lệch chỉ do may rủi.",
        la_gi="H0 là giả định “không có gì đặc biệt”. p-value là xác suất gặp dữ liệu lệch cỡ này hoặc hơn, nếu H0 đúng.",
        doc_tieu="p lớn hay nhỏ nghĩa là gì",
        thang=[("p < 0,05", "hiếm, bác bỏ H0"), ("p ≥ 0,05", "chưa đủ bằng chứng, không có nghĩa H0 đúng")],
        vi_du="Tung đồng xu 10 lần được 9 ngửa: p = 11 / 1.024 ≈ 0,011, nhỏ hơn 0,05, nên bác bỏ “đồng xu cân đối”."),
    "bootstrap": dict(
        tieu="Bootstrap chuỗi thời gian: rút cả khối", phan="A", buoi="Buổi 2", hinh=(2, "bootstrap-do-dai-khoi"),
        muc="Biết một con số như trung bình bấp bênh cỡ nào, mà không cần công thức.",
        la_gi="Bootstrap rút lại từ chính mẫu thật nhiều lần và tính lại con số mỗi lần. Block bootstrap rút cả khối điểm liền nhau.",
        doc_tieu="Nhận ra thế nào",
        doc="Dữ liệu tự tương quan mà rút từng điểm thì mất cách các điểm liền nhau đi cùng nhau, nên khoảng hẹp giả. Rút cả khối giữ được điều đó.",
        vi_du="Rút từng điểm, khoảng chỉ chứa trung bình thật 60,3% số lần. Rút khối dài 20 thì lên 89,3%."),
    "khoang-tin-cay": dict(
        tieu="Khoảng dự báo khác khoảng tin cậy", phan="A", buoi="Buổi 2", hinh=(2, "kn-dinh-ly-gioi-han-trung-tam-clt"),
        muc="Không nhầm độ bấp bênh của một giá trị mới với độ bấp bênh của một con số tóm tắt như trung bình.",
        la_gi="Khoảng dự báo: nơi một giá trị mới sẽ rơi. Khoảng tin cậy: nơi con số thật, như trung bình, nằm.",
        doc_tieu="Thêm dữ liệu thì sao",
        doc="Khoảng tin cậy hẹp dần theo 1/√n, nhờ định lý giới hạn trung tâm. Khoảng dự báo thì không hẹp về 0, vì từng giá trị vẫn dao động.",
        vi_du="Lượt thuê, độ lệch chuẩn 181: trung bình của 25 giờ dao động 36,1; của 100 giờ còn 18,2; của 400 giờ còn 9,1."),
    "phan-ra-cach": dict(
        tieu="Cổ điển, STL, MSTL: mùa vụ cố định hay đổi dần", phan="A", buoi="Buổi 6", hinh=(6, "bien-do-ngay"),
        muc="Chọn cách phân rã khớp với việc mùa vụ có đổi theo thời gian hay không.",
        la_gi="Cổ điển: xu hướng là trung bình trượt đúng một vòng, mùa vụ là trung bình theo vị trí trong vòng. STL lấy trung bình cục bộ (LOESS).",
        doc_tieu="Chọn cách nào",
        doc="Hình dạng mùa vụ đổi theo mùa thì dùng STL/MSTL, không phải phân rã nhân. Phần dư nhỏ bất thường có thể do cửa sổ xu hướng quá ngắn.",
        vi_du="Mùa vụ ngày của PJM: tháng 1 hai đỉnh sáng và tối, tháng 7 một đỉnh chiều. Một khuôn cố định không chứa được cả hai.",
        dg="cổ điển: một khuôn mùa vụ cho cả năm; STL: khuôn đổi dần; MSTL: nhiều khuôn, như 24 và 168 giờ."),
    "newsvendor": dict(
        tieu="Đặt hàng một lần: thiếu và thừa đều tốn tiền", phan="A", buoi="Buổi 1–2", hinh=(1, "kn-bai-toan-newsvendor"),
        muc="Biết vì sao nên báo cao hơn trung bình khi thiếu đắt hơn thừa, và chấm dự báo kiểu đó bằng gì.",
        la_gi="Newsvendor: đặt một lượng trước, thiếu mất Cu mỗi đơn vị, thừa mất Co. Pinball loss chấm dự báo quantile τ: thiếu phạt τ, thừa phạt 1 − τ mỗi đơn vị.",
        doc_tieu="Tỷ lệ chi phí nói gì",
        thang=[("Cu = Co", "báo trung vị (τ = 0,5)"), ("Cu = 4·Co", "báo quantile 0,8"), ("Cu ≫ Co", "báo rất cao, gần như không bao giờ thiếu")],
        vi_du="10 ngày mẫu, thiếu 4 đồng, thừa 1 đồng: mua 8 kWh tốn 33 đồng, mua 9 kWh tốn 28 (ít nhất). Pinball τ = 0,8, thật 10, báo 8: phạt 1,6.",
        dg="như tiệm bánh mì làm dư ra: mất một khách đắt hơn lỗ chút tiền bột."),
    "do-lech-chuan": dict(
        tieu="Trung bình, độ lệch chuẩn, z-score", phan="A", buoi="Buổi 2, 9, 11", hinh=(2, "kn-phuong-sai-do-lech-chuan"),
        muc="Có thước đo chung cho “mức” và “độ tản” của số liệu, nền của 3σ, 1,96s, CV và chuẩn hoá.",
        la_gi="Phương sai: trung bình bình phương khoảng cách tới trung bình (chia n − 1). Độ lệch chuẩn s: căn của phương sai, cùng đơn vị với dữ liệu. z = (giá trị − trung bình) / s.",
        doc_tieu="z lớn hay nhỏ nghĩa là gì",
        thang=[("z ≈ 0", "sát trung bình"), ("|z| ≈ 2", "khá xa, ít gặp"), ("|z| ≥ 3", "rất xa, nghi ngoại lai")],
        vi_du="2, 4, 6: trung bình 4, phương sai 4, độ lệch chuẩn 2. Trung bình 10, s = 2, giá trị 16 thì z = 3. Chuẩn hoá 100, 300, 100, 300 ra −1, 1, −1, 1."),
    "ar": dict(
        tieu="Mô hình AR: một phần hôm qua cộng nhiễu", phan="A", buoi="Buổi 2, 7", hinh=(2, "kn-tu-tuong-quan"),
        muc="Có một mô hình nhỏ để hiểu tự tương quan, PACF, tính dừng và prewhitening.",
        la_gi="AR(1): giá trị mới = ρ × giá trị cũ + một phần ngẫu nhiên. AR(p) dùng p bước trước. ρ (hay φ) là hệ số, từ −1 tới 1.",
        doc_tieu="ρ lớn hay nhỏ nghĩa là gì",
        thang=[("ρ = 0", "nhiễu trắng, không nhớ gì"), ("ρ = 0,7", "nhớ, rồi kéo về mức: dừng"), ("ρ = 1", "random walk, không quay về")],
        vi_du="Trung bình 0, đang ở 10, ρ = 0,7: kỳ vọng bước sau 7, rồi 4,9, dần về 0. ρ = 1: kỳ vọng mãi là 10."),
    "sai-phan-la-gi": dict(
        tieu="Sai phân: nhìn vào thay đổi thay vì mức", phan="A", buoi="Buổi 5, 7", hinh=(7, "gdp"),
        muc="Biến một chuỗi trôi đi (không dừng) thành chuỗi có mức để quay về, để mô hình học được.",
        la_gi="Sai phân: thay mỗi giá trị bằng hiệu với giá trị trước, y_t − y_(t−1). Sai phân mùa vụ: hiệu với cùng vị trí của vòng trước, y_t − y_(t−m).",
        doc_tieu="Khi nào dùng",
        doc="Chuỗi random walk thì sai phân một lần. Chuỗi có mùa vụ thì sai phân mùa vụ trước. Chuỗi dừng quanh xu hướng thì khử xu hướng (trừ đường xu hướng) thay vì sai phân.",
        vi_du="100, 103, 105 thành 3, 2. GDP Mỹ: log GDP trôi lên mãi; sai phân log dao động quanh 0,76% mỗi quý."),
    "mcar": dict(
        tieu="Vì sao số bị mất quyết định có điền được không", phan="B", buoi="Buổi 10", hinh=(10, "kn-mcar-mar-mnar"),
        muc="Biết trước khi điền: phần dữ liệu còn lại có còn đại diện cho cái đã mất không.",
        la_gi="Ba cơ chế thiếu: MCAR thiếu hoàn toàn ngẫu nhiên; MAR thiếu vì một thứ khác đã đo được; MNAR thiếu vì chính giá trị bị mất.",
        doc_tieu="Điền được tới đâu",
        thang=[("MCAR", "mất mạng vài phút: điền thoải mái"), ("MAR", "trạm hay hỏng mùa mưa: điền, có dùng mùa"), ("MNAR", "cảm biến tắt khi quá tải: đừng điền")],
        vi_du="PM2.5 thật 10, 20, 30, 40 (trung bình 25); cảm biến tắt khi trên 30 thì chỉ còn 10, 20, 30, trung bình 20: lệch 5 dù chưa điền gì."),
    "pho": dict(
        tieu="Tần số và phổ: chuỗi rung ở nhịp nào", phan="A", buoi="Buổi 9, 12", hinh=(9, "kn-tan-so"),
        muc="Nhìn chuỗi theo nhịp lặp để biết nhịp nào là tín hiệu cần giữ, nhịp nào là nhiễu có thể lọc.",
        la_gi="Tần số: số vòng lặp mỗi bước, bằng 1 / chu kỳ. Phổ (periodogram): mỗi tần số góp bao nhiêu phần dao động (năng lượng) vào chuỗi.",
        doc_tieu="Tần số thấp hay cao nghĩa là gì",
        thang=[("thấp", "dao động chậm: xu hướng, mùa năm"), ("trung bình", "nhịp ngày, nhịp tuần"), ("cao", "dao động rất nhanh, thường là nhiễu")],
        vi_du="Lặp mỗi 12 tháng thì tần số 1/12 ≈ 0,083. Điện thiết bị có đỉnh phổ ở 1 vòng/ngày, và 17,8% năng lượng nhanh hơn 1 giờ."),
    "cua-so": dict(
        tieu="Cửa sổ học: expanding, sliding, gap", phan="D", buoi="Buổi 15", hinh=(3, "kn-backtest"),
        muc="Dựng backtest giống hệt lúc chạy thật: học đoạn nào, dữ liệu về trễ bao lâu, học lại khi nào.",
        la_gi="Expanding: mỗi cutoff học trên toàn bộ quá khứ. Sliding: chỉ học L bước gần nhất. Gap: số bước bỏ trống giữa cutoff và đoạn dự báo. Refit: học lại mô hình ở mỗi cửa sổ.",
        doc_tieu="Chọn thế nào",
        doc="Quá khứ xa vẫn giống hiện tại thì expanding; quá khứ xa đã khác thì sliding. Gap bằng đúng độ trễ công bố dữ liệu. Mô hình nặng thì refit mỗi vài cửa sổ.",
        vi_du="Số liệu điện về trễ 1 ngày thì gap = 24 giờ. Sliding L = 90 ngày: mỗi cutoff chỉ học 90 ngày gần nhất."),
    "utc": dict(
        tieu="Một con số giờ chưa đủ: cần múi giờ", phan="A", buoi="Buổi 3", hinh=(3, "kn-gio-mua-he-dst"),
        muc="Mỗi mốc giờ chỉ trỏ đúng một thời điểm, để gộp và ghép không bị sai.",
        la_gi="UTC là giờ chung, không đổi theo mùa. Offset là độ lệch so với UTC, Hà Nội là +07:00. Giờ naive là giờ không ghi múi.",
        doc_tieu="Nhận ra thế nào",
        doc="Giờ mùa hè (DST) làm giờ địa phương có một giờ biến mất vào mùa xuân và một giờ lặp hai lần vào mùa thu.",
        vi_du="07:00 ở Hà Nội là 00:00Z (Z nghĩa là UTC). New York ngày 10/3/2024 không có 2:00; ngày 3/11 có 1:00 hai lần."),
    "resample": dict(
        tieu="Gộp tần suất: khoảng nào, cộng hay trung bình", phan="A", buoi="Buổi 3", hinh=(3, "kn-closed-label"),
        muc="Đổi tần suất, chẳng hạn từ phút sang giờ, mà không tạo ra số liệu giả.",
        la_gi="closed chọn mốc biên thuộc khoảng nào; label chọn đặt tên khoảng theo mốc đầu hay mốc cuối.",
        doc_tieu="Gộp thế nào",
        doc="Số lượng thì cộng, trạng thái như nhiệt độ thì lấy trung bình. Giờ trống của số đếm là 0, của số đo là NaN.",
        vi_du="Bốn chuyến lúc 9:00, 9:40, 10:00, 10:20, gộp mặc định: ô “9:00” có 2 chuyến, ô “10:00” có 2 chuyến."),
    "merge-asof": dict(
        tieu="Ghép theo thời gian: chỉ nhìn về quá khứ", phan="A", buoi="Buổi 3, 13", hinh=(3, "kn-ghep-as-of-merge-asof"),
        muc="Ghép số liệu của nguồn khác vào đúng dòng, mà không lấy nhầm số của tương lai.",
        la_gi="merge_asof cho mỗi dòng lấy giá trị gần nhất về thời gian từ bảng kia.",
        doc_tieu="Chọn hướng nào",
        thang=[("backward", "lấy số đã có trước đó: đúng"), ("forward", "lấy số sắp tới: rò rỉ")],
        vi_du="Dòng 10:00, giá có lúc 9:30 và 10:30: backward lấy 9 của 9:30, forward lấy 10 của 10:30. Thêm tolerance để bỏ số quá cũ."),
    "mua-vu": dict(
        tieu="Mùa vụ lặp đều; chu kỳ không hẹn trước", phan="A", buoi="Buổi 4", hinh=(4, "kn-chu-ky"),
        muc="Tách phần lặp lại biết trước, thứ dự báo được, khỏi phần lên xuống không hẹn trước.",
        la_gi="Xu hướng là mức chung đổi dần. Mùa vụ lặp lại sau một số bước cố định m. Chu kỳ lên xuống nhưng dài ngắn không đều.",
        doc_tieu="Nhận ra thế nào",
        doc="Hỏi: có lặp sau đúng m bước biết trước (24 giờ, 7 ngày, 12 tháng) không? “Mùa” là mọi vòng lặp theo lịch, không chỉ xuân, hạ, thu, đông.",
        vi_du="Thuê xe đông lúc 8h và 17h mỗi ngày làm việc là mùa vụ (m = 24). Kinh tế tăng rồi suy giảm không hẹn trước là chu kỳ.",
        dg="mùa vụ lặp đều, biết trước lúc lặp; chu kỳ lên xuống mà không biết khi nào lặp lại."),
    "doc-hinh": dict(
        tieu="Đọc mọi biểu đồ theo 5 bước", phan="A", buoi="Buổi 4", hinh=(4, "nhiet-gio-thu"),
        muc="Đọc ra một kết luận có bằng chứng từ biểu đồ, không đoán theo cảm giác.",
        la_gi="Năm bước: trục ngang là gì, trục dọc là gì và đơn vị nào, ký hiệu nghĩa là gì, nhìn vào đâu, và kết luận bằng một câu.",
        doc_tieu="Heatmap đọc thế nào",
        thang=[("tối", "giá trị thấp"), ("sáng", "giá trị cao")],
        vi_du="Heatmap giờ × thứ: hai cột sáng lúc 8h và 17h chạy suốt thứ Hai tới thứ Sáu rồi tắt vào cuối tuần."),
    "boxplot": dict(
        tieu="Boxplot: hộp càng dài, giờ càng khó dự báo", phan="A", buoi="Buổi 4", hinh=(4, "hop-theo-gio"),
        muc="Thấy độ tản của từng nhóm (giờ, thứ), tức nhóm nào khó dự báo.",
        la_gi="Hộp chứa một nửa số ngày ở giữa, từ quantile 0,25 tới 0,75; độ rộng hộp gọi là IQR. Vạch giữa hộp là trung vị.",
        doc_tieu="Hộp ngắn hay dài nghĩa là gì",
        thang=[("hộp ngắn", "ngày nào cũng như ngày nấy, dễ đoán"), ("hộp dài", "hôm đông hôm vắng, khó đoán")],
        vi_du="17h ngày làm việc có hộp 348–704 lượt, rộng nhất. 8h ngày nghỉ chỉ 57–141, nằm hẳn dưới ngày làm việc."),
    "acf": dict(
        tieu="ACF: cách k bước có giống bây giờ không?", phan="A", buoi="Buổi 4, 7", hinh=(4, "acf"),
        muc="Biết quá khứ giúp đoán hiện tại tới đâu, và nhịp lặp dài bao nhiêu bước.",
        la_gi="Mức giống nhau giữa giá trị bây giờ và giá trị cách đó k bước (gọi là trễ k).",
        thang=[("−1", "trước cao thì nay thấp"), ("0", "quá khứ không giúp gì"), ("+1", "trước cao thì nay cũng cao")],
        vi_du="Lượt thuê xe có đỉnh ở trễ 24, 168 và 336: nhịp ngày lồng trong nhịp tuần."),
    "box-cox": dict(
        tieu="Box-Cox: núm vặn giữa giữ nguyên và log", phan="A", buoi="Buổi 5", hinh=(5, "kn-bien-doi-box-cox"),
        muc="Làm dao động đều lại khi dao động cứ lớn dần theo mức, để mô hình dễ học.",
        la_gi="Box-Cox là phép biến đổi có một núm vặn λ. Cách Guerrero chọn λ sao cho dao động các năm đều nhau nhất.",
        doc_tieu="λ lớn hay nhỏ nghĩa là gì",
        thang=[("λ = 0", "lấy log, nén mạnh"), ("λ = 0,5", "căn bậc hai"), ("λ = 1", "gần như giữ nguyên")],
        vi_du="Bán lẻ Mỹ: Guerrero chọn λ ≈ 0,34. Dao động năm 2019 so với 1992: dữ liệu gốc gấp 2,45 lần, sau λ 0,34 chỉ 1,21."),
    "phan-ra": dict(
        tieu="Chuỗi = xu hướng + mùa vụ + phần dư", phan="A", buoi="Buổi 6", hinh=(6, "mstl"),
        muc="Tách chuỗi ra từng phần để thấy riêng xu hướng, mùa vụ và phần khó đoán.",
        la_gi="Phân rã tách chuỗi thành xu hướng, mùa vụ và phần dư. Kiểu cộng: mùa vụ thêm một lượng cố định. Kiểu nhân: thêm theo %.",
        doc_tieu="Chọn cộng hay nhân",
        doc="Biên độ mùa vụ giữ nguyên khi mức đổi thì chọn cộng. Biên độ lớn dần theo mức thì chọn nhân, hoặc lấy log rồi cộng.",
        vi_du="Cộng: mùa hè luôn cao hơn 10 GW, dù mức nền là 80 hay 150 GW. Nhân: nền 100 thì +10, nền 200 thì +20."),
    "f-s": dict(
        tieu="F_S: mùa vụ mạnh tới đâu so với nhiễu", phan="A", buoi="Buổi 6", hinh=(6, "kn-do-manh-xu-huong-mua-vu"),
        muc="Có một con số để so mùa vụ mạnh hay yếu giữa các chuỗi.",
        la_gi="F_S = 1 − Var(phần dư) / Var(mùa vụ + phần dư). F_T tính giống vậy cho xu hướng.",
        thang=[("0", "mùa vụ chìm trong nhiễu"), ("0,5", "vừa phải"), ("1", "mùa vụ lấn át nhiễu")],
        vi_du="PJM 2024, mùa vụ 24 giờ: 0,618 nếu phân rã cổ điển, 0,829 nếu MSTL. Vì vậy luôn ghi kèm tên cách phân rã."),
    "pacf": dict(
        tieu="PACF: trễ xa còn thêm gì sau trễ gần?", phan="A", buoi="Buổi 7", hinh=(7, "bon-chuoi"),
        muc="Biết cần bao nhiêu bước quá khứ để dự báo, tức bậc AR.",
        la_gi="PACF ở trễ k là phần tương quan còn lại sau khi đã bỏ phần mà các trễ ngắn hơn giải thích.",
        doc_tieu="Nhận ra thế nào",
        doc="PACF cao ở trễ 1 rồi tắt hẳn: chỉ cần hôm qua, tức AR(1). ACF giảm rất chậm qua nhiều trễ: chuỗi chưa dừng.",
        vi_du="Chuỗi AR(1) với φ = 0,7: ACF giảm dần; PACF ở trễ 1 là 0,713, ở trễ 2 chỉ còn −0,110.",
        dg="sau khi biết quá khứ gần, quá khứ xa còn thông tin gì?"),
    "ljung-box": dict(
        tieu="Đừng đếm cột vượt dải: dùng Ljung-Box", phan="A", buoi="Buổi 7, 14", hinh=(7, "nhieu-trang"),
        muc="Kiểm một chuỗi, hay phần dư của mô hình, đã hết quy luật chưa, bằng một con số.",
        la_gi="Ljung-Box gộp ACF của nhiều trễ vào một kiểm định, với giả định ban đầu H0 là chuỗi chỉ là nhiễu trắng.",
        doc_tieu="p lớn hay nhỏ nghĩa là gì",
        thang=[("p < 0,05", "còn quy luật chưa khai thác"), ("p ≥ 0,05", "chưa thấy quy luật nào còn sót")],
        vi_du="1.000 chuỗi nhiễu trắng thuần: 62% vẫn có ít nhất một cột ACF vượt dải. Vì vậy đừng đếm cột.",
        dg="Ljung-Box hỏi: các ACF từ trễ 1 tới trễ ℓ có cùng bằng 0 không?"),
    "dung": dict(
        tieu="Chuỗi dừng: mức và dao động không đổi", phan="A", buoi="Buổi 7", hinh=(7, "kn-dung"),
        muc="Biết chuỗi có “mức để quay về” không, để chọn sai phân hay khử xu hướng.",
        la_gi="Chuỗi có trung bình và độ dao động giữ nguyên theo thời gian, như luôn có một mức để quay về.",
        doc_tieu="Nhận ra thế nào",
        doc="Dừng thì dao động quanh một mức. Dừng quanh xu hướng thì bám một đường. Random walk thì trôi đi, không quay "
            "về. Kiểm lại bằng ADF và KPSS.",
        vi_du="Phòng máy lạnh 25 °C là dừng; chiều cao một đứa trẻ là dừng quanh xu hướng; tung đồng xu rồi bước là random walk.",
        dg="nhiễu trắng là khi quá khứ không có “ký ức” gì về tương lai."),
    "scatter": dict(
        tieu="Vẽ scatter trước khi tin r", phan="A", buoi="Buổi 2, 8", hinh=(8, "anscombe"),
        muc="Đo hai đại lượng đi cùng nhau tới đâu, sau khi đã nhìn hình dạng của quan hệ.",
        la_gi="Pearson r đo quan hệ đường thẳng. Spearman đo hai biến có cùng tăng theo thứ hạng không. Kendall đếm cặp cùng chiều.",
        thang=[("−1", "ngược chiều"), ("0", "không có quan hệ thẳng"), ("+1", "cùng tăng")],
        vi_du="Bốn bộ Anscombe khác hẳn nhau mà cùng r = 0,82. Hình chữ U đối xứng thì Pearson và Spearman đều bằng 0."),
    "ccf": dict(
        tieu="Ai đi trước? Prewhiten rồi mới đọc CCF", phan="A", buoi="Buổi 8", hinh=(8, "ccf"),
        muc="Tìm biến nào đi trước biến nào, trước bao nhiêu bước, để chọn độ trễ cho feature.",
        la_gi="Tương quan chéo đo x lúc này giống y sau k bước tới đâu. Prewhitening lọc x bằng mô hình AR của chính nó, rồi lọc y bằng đúng bộ lọc đó.",
        doc_tieu="Nhận ra thế nào",
        doc="Đỉnh ở trễ k dương nghĩa là x đi trước y k bước. CCF thô cao ở mọi trễ thường chỉ là nhịp riêng, chưa phải quan hệ.",
        vi_du="CDD và tải điện: thô là 0,848 ở trễ 0 và vẫn 0,828 ở trễ 24; sau prewhitening chỉ còn 0,205 và 0,061.",
        dg="tưởng tải điện theo nhịp ngày của nắng; lọc xong mới thấy trời nóng lên là tải tăng ngay."),
    "truot": dict(
        tieu="Một hệ số cho cả năm che mất các mùa", phan="A", buoi="Buổi 8", hinh=(8, "truot"),
        muc="Kiểm quan hệ có ổn định theo thời gian không, trước khi dùng một con số cho cả năm.",
        la_gi="Tương quan trượt tính r trên từng cửa sổ thời gian, ví dụ 90 ngày, rồi trượt dần cửa sổ đi.",
        doc_tieu="Nhận ra thế nào",
        doc="Đường r đổi dấu theo mùa nghĩa là có nhiều chế độ, phải tách riêng. Đường gần như phẳng thì quan hệ ổn định.",
        vi_du="Nhiệt độ và tải điện: −0,801 với cửa sổ tới 31/3, +0,968 với cửa sổ tới 14/10, còn cả năm chỉ 0,616."),
    "granger": dict(
        tieu="Granger: “giúp dự báo”, không phải “gây ra”", phan="A", buoi="Buổi 8", hinh=(8, "granger"),
        muc="Kiểm quá khứ của một biến có giúp dự báo biến kia không.",
        la_gi="Granger so sai số dự báo Y khi có và khi không có quá khứ của X. Biến gây nhiễu là thứ thứ ba điều khiển cả hai.",
        doc_tieu="Kết quả nói gì",
        doc="p nhỏ chỉ nói quá khứ X giúp dự báo Y, không nói X gây ra Y. Có ý nghĩa ở cả hai chiều thì nghĩ tới biến gây nhiễu.",
        vi_du="Tải điện và nhiệt độ “Granger” lẫn nhau ở cả hai chiều, vì cả hai cùng chạy theo nhịp ngày."),
    "dac-trung": dict(
        tieu="Đặc trưng: tóm cả chuỗi thành vài con số", phan="A", buoi="Buổi 9", hinh=(9, "kn-z-score-chuan-hoa"),
        muc="So và phân loại hàng nghìn chuỗi mà không phải xem từng hình.",
        la_gi="Một con số tóm một tính chất của cả chuỗi: CV, r₁, F_S, entropy… Mỗi chuỗi thành một hàng số, cả tập thành một bảng.",
        doc_tieu="Đặc trưng tốt thế nào",
        doc="Không đổi theo đơn vị và tính trên cùng độ dài. Nhân chuỗi với 1.000 mà đặc trưng đổi theo thì nó đang đo độ lớn, không đo hình dạng.",
        vi_du="Chuỗi a và 1.000 × a có CV cùng bằng 0,378. Nhân một chuỗi 120 tháng với 1.000: chỉ trung bình và độ lệch chuẩn đổi, mọi đặc trưng khác giữ nguyên."),
    "do-kho": dict(
        tieu="Đo độ khó bằng sMAPE, không bằng MASE", phan="A", buoi="Buổi 9", hinh=(9, "entropy-sai-so"),
        muc="Đo độ khó của từng chuỗi bằng một thước đo không tự triệt tiêu độ khó.",
        la_gi="MASE chia sai số cho sai số naive của chính chuỗi đó; sMAPE chia cho mức của chuỗi.",
        doc_tieu="Nhận ra thế nào",
        doc="Chuỗi khó thì mẫu số của MASE cũng lớn, nên MASE của seasonal naive nằm ngang quanh 1 dù chuỗi dễ hay khó. sMAPE mới tăng theo độ khó.",
        vi_du="Tương quan với entropy: sMAPE +0,245, còn MASE chia seasonal naive chỉ −0,048.",
        dg="MASE so các mô hình trên cùng một chuỗi; muốn so độ khó giữa các chuỗi thì dùng sMAPE."),
    "ban-do-pca": dict(
        tieu="Bản đồ 4.000 chuỗi: vùng nào khó", phan="A", buoi="Buổi 9", hinh=(9, "khong-gian-dac-trung"),
        muc="Nhìn cả tập hàng nghìn chuỗi trên một hình, khoanh vùng chuỗi khó và chuỗi lạ.",
        la_gi="PCA chiếu nhiều đặc trưng xuống hai trục giữ được nhiều khác biệt nhất. Mỗi chuỗi thành một chấm.",
        doc_tieu="Nhận ra thế nào",
        doc="Trục ngang (PC1) là độ lởm chởm: phải là chuỗi gần nhiễu, khó. Trục dọc (PC2) là mức xu hướng và mùa vụ. Chấm đứng lẻ là chuỗi lạ, cần xem tận mắt.",
        vi_du="4.000 chuỗi M4: trục ngang giữ 41% khác biệt. Entropy từ 0,666 trở lên và F_S dưới 0,4 thì chỉ cần baseline."),
    "dtw": dict(
        tieu="DTW: gom chuỗi theo hình dạng", phan="A", buoi="Buổi 9", hinh=(9, "phan-cum-dtw"),
        muc="Gom các chuỗi cùng hình dạng để dùng chung cách xử lý hay cùng một mô hình.",
        la_gi="DTW đo khoảng cách hai chuỗi mà cho phép lệch thời gian đôi chút. Ward gộp dần các chuỗi gần nhau thành cụm.",
        doc_tieu="Nhận ra thế nào",
        doc="DTW nhỏ là cùng hình dạng. Mức trung vị của các cụm tăng đều nghĩa là đang gom theo độ lớn: đã quên chuẩn hoá.",
        vi_du="Không chuẩn hoá, 4 cụm chỉ khác độ lớn (trung vị 1.585 lên tới 9.832). Chuẩn hoá z-score thì gom đúng theo hình dạng.",
        dg="chuỗi “tăng, giảm, tăng” và cùng hình đó nhưng chậm vài bước vẫn được coi là giống nhau."),
    "abc-xyz": dict(
        tieu="ABC hỏi quan trọng, XYZ hỏi dao động", phan="A", buoi="Buổi 9", hinh=(9, "abc-xyz"),
        muc="Chọn nơi đặt công sức: mã hàng nào đáng làm mô hình kỹ nhất.",
        la_gi="ABC xếp mã hàng theo doanh thu. XYZ xếp theo CV, tức độ lệch chuẩn chia trung bình.",
        doc_tieu="CV cao hay thấp nghĩa là gì",
        thang=[("CV thấp", "bán đều"), ("CV cao", "dao động nhiều, chưa chắc khó đoán")],
        vi_du="Online Retail II: nhóm A (một phần năm số mã) mang 74,7% doanh thu. Chuỗi 10, 30, 10, 30 có CV 0,58 mà rất dễ đoán.",
        dg="ABC hỏi cái nào quan trọng, CV hỏi cái nào dao động, sai số baseline mới hỏi cái nào khó."),
    "biet-truoc": dict(
        tieu="Mỗi feature: biết trước bao lâu?", phan="A", buoi="Buổi 13", hinh=(13, "biet-truoc"),
        muc="Mỗi cột đầu vào của mô hình chỉ chứa thông tin thật sự có trong tay lúc ra dự báo.",
        la_gi="Feature là một cột đầu vào. Ba nhóm hợp lệ: lịch (biết mãi mãi), kế hoạch đã công bố, và quá khứ của chuỗi.",
        doc_tieu="Nhận ra thế nào",
        doc="Feature không xếp được vào ba nhóm là đáng nghi rò rỉ. Số quá khứ phải cách thời điểm cần dự báo ít nhất h bước.",
        vi_du="41 feature của buổi 13: 23 cột là lịch, 18 cột lấy từ quá khứ của chuỗi."),
    "feature-lich": dict(
        tieu="Feature lịch: sin/cos, Fourier, Tết âm lịch", phan="A", buoi="Buổi 13", hinh=(13, "tet-di-dong"),
        muc="Đưa lịch (thứ, tháng, ngày lễ) vào mô hình theo cách mô hình hiểu được.",
        la_gi="Mã hoá tuần hoàn dùng một cặp sin/cos cho thứ hay tháng. Fourier term dùng vài cặp sin/cos cho mùa vụ dài.",
        doc_tieu="Vì sao không ghi thẳng số",
        doc="Ghi thứ là 1–7 thì Chủ nhật cách thứ Hai rất xa; sin/cos đặt chúng cạnh nhau. Tết theo lịch âm nên tính số ngày tới Tết.",
        vi_du="Tết xê dịch gần một tháng giữa các năm; vào mùng 1, lượt xem Wikipedia chỉ còn 0,62 lần mức thường."),
    "bon-loai": dict(
        tieu="Bốn kiểu bất thường, bốn cách bắt", phan="B", buoi="Buổi 11", hinh=(11, "bon-loai-bat-thuong"),
        muc="Gọi đúng tên kiểu bất thường, vì mỗi kiểu cần một cách bắt và một cách sửa riêng.",
        la_gi="Điểm đơn (AO), dịch mức (LS), thay đổi tạm (TC) và đổi phương sai.",
        doc_tieu="Nhận ra thế nào",
        doc="Lệch rồi về ngay là AO. Nhảy bậc rồi ở lại là LS. Nhảy rồi tắt dần là TC. Mức giữ nguyên mà dao động to ra là đổi phương sai.",
        vi_du="Quanh mức 10: AO là 10, 25, 10; LS là 10, 20, 20, 20; TC là 20, 15, 12, 11, 10.",
        dg="hỏi trước: đây là lỗi, giai đoạn tạm thời, hay một trạng thái mới?"),
    "lam-tron": dict(
        tieu="Làm trơn: đường mượt xoá ngày bất thường", phan="A", buoi="Buổi 4", hinh=(4, "lam-tron"),
        muc="Thấy xu hướng qua nhiễu từng ngày mà không đánh mất những ngày bất thường cần biết.",
        la_gi="Trung bình trượt có tâm thay mỗi điểm bằng trung bình của nó với các điểm hai bên, trong cửa sổ w điểm.",
        doc_tieu="Cửa sổ rộng hay hẹp nghĩa là gì",
        thang=[("w nhỏ", "còn thấy chi tiết, còn nhiễu"), ("w lớn", "rất mượt, ngày lạ gần như biến mất")],
        vi_du="50, 52, 48, 2, 51, 49, 50: w = 3 cho ngày thứ tư 33,7; w = 7 cho 43,1. Ngày bão Sandy chỉ có 22 lượt, đường 7 ngày vẫn 4.632.",
        dg="vẽ đường làm trơn đè lên dữ liệu gốc, đừng thay nó."),
    "thang-log": dict(
        tieu="Thang log: cùng độ dốc là cùng phần trăm", phan="A", buoi="Buổi 4", hinh=(4, "thang-log"),
        muc="Đọc đúng câu hỏi: tăng thêm bao nhiêu đơn vị, hay tăng nhanh bao nhiêu phần trăm.",
        la_gi="Thang log đặt mỗi điểm ở độ cao log₁₀ y thay vì y. Mỗi lần gấp đôi thì cao thêm đúng 0,301, ở bất kỳ mức nào.",
        doc_tieu="Dùng thang nào",
        thang=[("thang thường", "hỏi tăng bao nhiêu (thêm bao nhiêu xe)"), ("thang log", "hỏi tăng nhanh bao nhiêu phần trăm")],
        vi_du="Thuê xe 2011: thang thường cho tháng 4 → 5 tăng nhiều nhất (+40.951 lượt); thang log cho tháng 3 → 4 nhanh nhất (+48,1%)."),
    "dieu-chinh": dict(
        tieu="Điều chỉnh lịch, lạm phát, dân số", phan="A", buoi="Buổi 5", hinh=(5, "dieu-chinh-lich"),
        muc="Biết doanh số tăng thật, hay chỉ vì tháng dài hơn, giá cao hơn, người đông hơn.",
        la_gi="Điều chỉnh lịch: chia tổng tháng cho số ngày. Giá thực: chia CPI rồi nhân CPI năm gốc. Trên đầu người: chia thêm dân số.",
        doc_tieu="Mỗi bước bỏ một nguyên nhân",
        doc="Tháng 3 so với tháng 2/2023: so thẳng +14,15%; chia ngày lịch +3,11%; chuỗi đã điều chỉnh của Census −1,05%.",
        vi_du="Doanh thu 100 → 150, CPI 100 → 125, dân số 10 → 12: giá thực 120 (+20%); mỗi người 10 → 10, không đổi."),
    "log": dict(
        tieu="Log: cùng % thành cùng khoảng cách", phan="A", buoi="Buổi 5", hinh=(5, "kn-log-exp"),
        muc="Làm dao động đều lại khi nó lớn dần theo mức, cho mô hình dễ học.",
        la_gi="Log biến nhân thành cộng, nên tăng cùng một phần trăm thì cách nhau cùng một khoảng, bất kể mức. Chỉ dùng cho số dương.",
        doc_tieu="Khi nào hợp",
        doc="Dao động tỷ lệ đúng với mức thì log hợp. Dao động tăng chậm hơn mức thì log ép quá tay: dùng Box-Cox (slide sau).",
        vi_du="100 → 120 và 1.000 → 1.200 đều cao thêm 0,182 trên thang log. Bán lẻ Mỹ: mức gấp 3,1 lần mà dao động chỉ gấp 2,4."),
    "robust": dict(
        tieu="Robust: bớt tin điểm có phần dư quá lớn", phan="A", buoi="Buổi 6", hinh=(6, "robust"),
        muc="Một giờ số liệu hỏng không được làm méo xu hướng và mùa vụ của cả tuần.",
        la_gi="Phân rã hai lượt. Lượt sau cho điểm có phần dư lớn trọng số nhỏ, tới 0. Điểm không bị xoá mà nằm lại trong phần dư.",
        doc_tieu="Cứu được gì",
        thang=[("một giờ hỏng", "cứu được: lỗi nằm gọn trong phần dư"), ("đợt nóng nhiều ngày", "không cứu được: cần biến nhiệt độ")],
        vi_du="PJM, 17:00 UTC ngày 20/11 (không có lỗi): mùa vụ ngày −4.051 MW khi không robust, +2.117 MW khi robust."),
    "cach-dien": dict(
        tieu="Bảy cách điền: lỗ dài cần giữ hình dạng", phan="B", buoi="Buổi 10",
        hinh=(10, "kn-dien-du-lieu-imputation"),
        muc="Chọn cách điền theo độ dài lỗ, nhịp của chuỗi, và có được dùng số tương lai không.",
        la_gi="ffill giữ số gần nhất; tuyến tính, spline nối hai đầu lỗ; mùa vụ lấy cùng giờ hôm trước; trung bình theo giờ; Kalman smoother; trạm hàng xóm.",
        doc_tieu="Chọn theo độ dài lỗ",
        thang=[("lỗ ngắn", "ffill hay tuyến tính đều ổn"), ("lỗ dài", "mùa vụ, hàng xóm: mang theo hình dạng")],
        vi_du="Hai ô thiếu, thật là 26 và 28: ffill điền 23, 23; tuyến tính 24,33, 25,67; hàng xóm cộng 1 °C ra đúng 26, 28."),
    "khu-nhieu": dict(
        tieu="Khử nhiễu: trailing nhân quả nhưng trễ", phan="B", buoi="Buổi 12", hinh=(12, "kn-bo-loc-nhan-qua"),
        muc="Ước lượng phần tín hiệu mà không dùng số của tương lai, khi đầu ra làm feature dự báo.",
        la_gi="Chuỗi = tín hiệu + nhiễu; bộ lọc ước lượng phần tín hiệu. Trailing lấy k điểm gần nhất; centered lấy cả điểm trước lẫn sau.",
        doc_tieu="Dùng kiểu nào",
        thang=[("trailing", "làm feature dự báo; đổi lại bị trễ"), ("centered", "chỉ để mô tả, vẽ, tách xu hướng")],
        vi_du="10, 12, 14, 30, 16, tại giờ 3: trailing (10 + 12 + 14) / 3 = 12; centered (12 + 14 + 30) / 3 = 18,67, đã chứa số 30 của giờ sau."),
    "ewma": dict(
        tieu="EWMA: điểm mới nặng hơn, trễ ít hơn", phan="B", buoi="Buổi 12", hinh=(12, "kn-ewma"),
        muc="Làm trơn nhân quả mà trễ ít hơn trung bình trượt có cùng độ trơn.",
        la_gi="EWMA trộn số mới với đầu ra trước theo tỷ lệ α và 1 − α, nên trọng số giảm dần về quá khứ. Trung bình trượt k điểm trễ (k − 1) / 2 bước.",
        doc_tieu="α lớn hay nhỏ nghĩa là gì",
        thang=[("α nhỏ", "rất trơn, trễ nhiều"), ("α lớn", "bám sát số mới, ít trơn")],
        vi_du="α = 0,5, chuỗi 10, 20, 10: z = 10; 15; 12,5. Đo được: trung bình 13 điểm trễ 6 bước, EWMA α = 0,15 trễ 4."),
    "mase": dict(
        tieu="MASE: chia cho sai số baseline phần học", phan="D", buoi="Buổi 9, 14", hinh=(9, "entropy-sai-so"),
        muc="So sai số giữa các chuỗi khác đơn vị, kể cả có số 0, không dùng thông tin kỳ chấm.",
        la_gi="MASE chia MAE trên kỳ chấm cho MAE của seasonal naive trên phần học. RMSSE làm tương tự với bình phương (cuộc thi M5).",
        thang=[("dưới 1", "sai ít hơn baseline trên phần học"), ("1", "ngang"), ("trên 1", "sai nhiều hơn")],
        vi_du="Phần học 9, 11, 10, 12, 13: bước nhảy trung bình 1,5; MAE 1,6 → MASE 1,07. Mẫu số lấy nhầm trên kỳ chấm: naive trên M4 ra 0,972 thay vì 0,835.",
        dg="MASE < 1 chưa chắc thắng seasonal naive trên kỳ chấm: chạy baseline trên cùng kỳ."),
    "spearman": dict(
        tieu="Spearman: cùng tăng là đủ, không cần thẳng", phan="A", buoi="Buổi 8", hinh=(8, "kn-spearman"),
        muc="Đo hai đại lượng có cùng tăng (hay cùng giảm) không, kể cả khi quan hệ là đường cong.",
        la_gi="Spearman xếp hạng từng biến (nhỏ nhất là hạng 1) rồi tính Pearson trên các hạng. Kendall cũng dùng hạng, đếm số cặp cùng chiều.",
        doc_tieu="So với Pearson",
        thang=[("Pearson", "đo mức thẳng hàng"), ("Spearman", "đo mức cùng tăng theo thứ hạng"), ("cả hai = 0", "vẫn có thể là chữ U")],
        vi_du="y = x² với x = 1…5: Pearson 0,981, Spearman 1. Với x = −2…2 (chữ U): cả hai bằng 0 dù y hoàn toàn theo x."),
    "durbin-watson": dict(
        tieu="Durbin–Watson: phần dư đổi chậm là đáng ngờ", phan="A", buoi="Buổi 8", hinh=(8, "kn-durbin-watson"),
        muc="Biết đường hồi quy có bỏ sót cấu trúc thời gian không, trước khi tin R² và t.",
        la_gi="Hồi quy chuỗi này theo chuỗi kia rồi xem phần dư, tức phần đường thẳng không giải thích được. DW so bước nhảy giữa hai phần dư liền nhau với độ lớn phần dư.",
        doc_tieu="DW lớn hay nhỏ nghĩa là gì",
        thang=[("gần 0", "phần dư đổi rất chậm: nghi tương quan giả"), ("gần 2", "phần dư lộn xộn: ổn"), ("trên 2", "phần dư đổi dấu liên tục")],
        vi_du="Phần dư 1, 1, 1, −1, −1, −1: DW = 4 / 6 ≈ 0,67. CPI theo dân số Mỹ: R² 0,95 mà DW chỉ 0,0051."),
    "cdd-hdd": dict(
        tieu="CDD, HDD: tách chữ U thành hai nhánh thẳng", phan="A", buoi="Buổi 8", hinh=(8, "kn-cdd-hdd"),
        muc="Đưa quan hệ “lạnh cũng tăng, nóng cũng tăng” vào một mô hình đường thẳng.",
        la_gi="CDD là số độ nóng hơn mốc, HDD là số độ lạnh hơn mốc; phía còn lại bằng 0. Mốc 18,33 °C (65 °F) theo quy ước của cơ quan năng lượng Mỹ EIA.",
        doc_tieu="Dùng thế nào",
        doc="Hồi quy tải theo cả CDD và HDD: phía nóng một độ dốc, phía lạnh một độ dốc, thành hình chữ V. Không cần chia dữ liệu làm hai nhóm.",
        vi_du="10; 18,33; 25; 30 °C cho CDD = 0; 0; 6,67; 11,67 và HDD = 8,33; 0; 0; 0. Tải điện ERCOT: R² tăng từ 0,379 lên 0,812."),
    "mi": dict(
        tieu="Mutual information: biết x có giúp đoán y?", phan="A", buoi="Buổi 8", hinh=(8, "chu-u"),
        muc="Đo mọi kiểu phụ thuộc, kể cả chữ U mà Pearson và Spearman đều bỏ sót.",
        la_gi="MI so tỷ lệ thật của mỗi cặp (x, y) với tỷ lệ nếu x và y độc lập. Độc lập thì MI = 0; biết x càng giúp đoán y thì MI càng lớn. Đơn vị: nat.",
        doc_tieu="MI lớn hay nhỏ nghĩa là gì",
        thang=[("0", "độc lập: biết x không giúp gì"), ("lớn", "biết x đoán được y, theo bất kỳ hình dạng nào")],
        vi_du="Ngày lạnh → tải cao, vừa → thấp, nóng → cao, mỗi loại 1/3: Pearson = 0 mà MI ≈ 0,637 nat. Nhiệt độ × tải ERCOT: MI = 0,862."),
    "hoan-vi-khoi": dict(
        tieu="Hoán vị theo khối: MI có lớn thật không?", phan="A", buoi="Buổi 8", hinh=(8, "kn-hoan-vi-theo-khoi"),
        muc="Biết một giá trị MI là quan hệ thật, hay chỉ vì hai chuỗi trơn tình cờ cùng lên xuống.",
        la_gi="Xáo trộn y nhiều lần để phá quan hệ, rồi xem MI của dữ liệu xáo dao động cỡ nào. Với chuỗi thời gian phải xáo cả khối liền nhau để giữ độ trơn.",
        doc_tieu="Xáo kiểu nào",
        thang=[("từng điểm", "phá cả độ trơn, MI xáo quá nhỏ: dễ kết luận nhầm"), ("theo khối", "giữ độ trơn: so sánh công bằng")],
        vi_du="Hai chuỗi AR độc lập: xáo từng điểm cho p = 0,005 (nhầm là có quan hệ), xáo khối 200 điểm cho p = 0,055. ERCOT: 0,862 so với ngưỡng 0,124."),
    "he-so-lech": dict(
        tieu="Hệ số lệch: đuôi dài nằm về phía nào", phan="A", buoi="Buổi 2", hinh=(2, "kn-he-so-lech"),
        muc="Biết số liệu lệch về phía nào, để hiểu vì sao trung bình khác trung vị.",
        la_gi="Hệ số lệch là trung bình của (độ lệch / s)³. Lập phương giữ dấu và phóng to số ở xa, nên đuôi dài bên nào thì dấu theo bên đó.",
        doc_tieu="Dấu của hệ số lệch nghĩa là gì",
        thang=[("≈ 0", "đối xứng, trung bình gần trung vị"), ("> 0", "đuôi phải dài, trung bình lớn hơn trung vị"), ("< 0", "đuôi trái dài")],
        vi_du="2, 3, 5, 6, 8, 9, 12, 18, 36: số 36 lệch +25 góp gần hết, hệ số lệch +1,35. Lượt thuê theo giờ: 1,277."),
    "phan-phoi-chuan": dict(
        tieu="Phân phối chuẩn: 95% nằm trong ±1,96 s", phan="A", buoi="Buổi 2", hinh=(2, "kn-phan-phoi-chuan"),
        muc="Hiểu con số 1,96 của khoảng 95% đến từ đâu, và khi nào dùng được.",
        la_gi="Đường cong hình chuông, đối xứng quanh trung bình. Diện tích dưới đường bên trái một mốc là tỷ lệ giá trị nhỏ hơn mốc đó.",
        doc_tieu="Bao nhiêu phần nằm quanh trung bình",
        thang=[("± 1 s", "68,3%"), ("± 1,96 s", "95,0%, mỗi đuôi 2,5%"), ("± 2 s", "95,4%")],
        vi_du="100 ± 1,96 × 10 cho 80,4 tới 119,6. Dữ liệu lệch phải thì không hợp: 11 ± 1,96 × 10,57 cho cận dưới −9,7 lượt thuê."),
    "hoan-vi": dict(
        tieu="Kiểm định hoán vị: xáo nhãn rồi đếm", phan="A", buoi="Buổi 2", hinh=(2, "hoan-vi"),
        muc="Tính p-value cho câu hỏi “hai nhóm có khác nhau không” mà không cần công thức phức tạp.",
        la_gi="Nếu nhãn nhóm không liên quan tới số liệu, gán nhãn kiểu nào cũng như nhau. Xáo nhãn nhiều lần, đếm tỷ lệ lần cho chênh lệch cỡ thật hoặc hơn.",
        doc_tieu="Đọc kết quả thế nào",
        doc="Chênh thật nằm lọt trong đám chênh do xáo thì p lớn, có thể chỉ do may. Nằm xa ngoài đám thì p nhỏ. Cách này giả định các ngày độc lập.",
        vi_du="Làm việc 5, 7, 6; nghỉ 3, 2, 4: chênh 3. Chỉ 2 trong 20 cách chia cho chênh cỡ đó, p = 0,10. Năm 2012: chênh 456 lượt, p = 0,025."),
    "seasonal-subseries": dict(
        tieu="Seasonal plot chồng vòng, subseries gom mùa", phan="A", buoi="Buổi 4", hinh=(4, "kn-subseries-plot"),
        muc="Thấy hình dạng mùa vụ, và từng mùa đổi ra sao qua thời gian, bằng cách xếp dữ liệu theo lịch.",
        la_gi="Seasonal plot: mỗi vòng lặp (mỗi tuần) một đường, chồng lên nhau. Subseries plot: mỗi mùa (mỗi thứ, mỗi tháng) một ô, điểm xếp theo thời gian.",
        doc_tieu="Nhìn vào đâu",
        doc="Seasonal: đường nào lệch khỏi khuôn chung. Subseries: vạch trung bình các ô vẽ ra mùa vụ; trong ô, điểm sau cao hơn là có xu hướng.",
        vi_du="Lượt thuê theo tuần: T2–T6 hai đỉnh, T7–CN một bướu, tức mùa vụ kép. Mỗi tháng 2012 gấp 1,41 tới 2,57 lần cùng tháng 2011."),
    "lag-plot": dict(
        tieu="Lag plot: bám đường chéo là đoán được", phan="A", buoi="Buổi 4", hinh=(4, "kn-lag-plot"),
        muc="Chọn giá trị quá khứ nào (giờ trước, hôm qua, tuần trước) đoán tốt giá trị hiện tại.",
        la_gi="Scatter của y_t theo y_(t−k): mỗi chấm ghép một giá trị với giá trị cách nó k bước về trước.",
        doc_tieu="Hình dạng nói gì",
        thang=[("bám đường chéo", "cách k bước đoán tốt hiện tại"), ("đi xuống", "k bằng nửa vòng: đỉnh ghép với đáy"),
               ("hai nhánh", "r chỉ là trung bình hai nhánh")],
        vi_du="2, 4, 6, 4, 2, 4, 6, 4 ở trễ 2: cặp (2, 6), (6, 2) nằm trên đường đi xuống. Lượt thuê: trễ 168 hẹp nhất, r = 0,88; trễ 12 hai nhánh, r = −0,14."),
    "truc-y-cat": dict(
        tieu="Trục y cắt, trục kép: thang do người vẽ chọn", phan="A", buoi="Buổi 4", hinh=(4, "kn-truc-y-cat"),
        muc="Đọc thang trước khi đọc đường, để không thấy chênh lớn hay quan hệ chặt chỉ do cách vẽ.",
        la_gi="Trục y cắt: trục dọc không bắt đầu từ 0. Trục kép: hai trục dọc với hai thang trên một hình. Người vẽ chọn thang, nên chọn được độ cao.",
        doc_tieu="Quy ước khi vẽ",
        doc="Số đếm và tổng vẽ trục từ 0. Hai chuỗi khác đơn vị thì tách hình, hoặc đánh chỉ số: chia cho tháng đầu rồi nhân 100.",
        vi_du="490 → 510 triệu là +4,1%. Trục từ 480 tới 520: tháng đầu cao 25%, tháng sau cao 75% chiều cao hình, mắt thấy gấp ba."),
    "tron-nam": dict(
        tieu="Trộn nhiều năm vào một scatter làm r yếu đi", phan="A", buoi="Buổi 4", hinh=(4, "phan-tan-nhiet-do"),
        muc="Đo đúng quan hệ giữa hai đại lượng khi mức chung đổi theo năm.",
        la_gi="Mức chung dời lên theo năm thì gộp các năm làm đám điểm dày ra theo chiều dọc, nên r gộp nhỏ hơn r của từng năm.",
        doc_tieu="Nhận ra thế nào",
        doc="Tô màu scatter theo năm. Thấy hai đám mây song song, cùng nhiệt độ mà năm sau cao hơn, thì tính r riêng từng năm.",
        vi_du="Nhiệt độ × lượt thuê mỗi ngày: 2011 r = 0,771, 2012 r = 0,714, gộp hai năm chỉ còn 0,627, thấp hơn cả hai năm."),
    "guerrero": dict(
        tieu="Guerrero chọn λ làm dao động các năm đều", phan="A", buoi="Buổi 5", hinh=(5, "box-cox"),
        muc="Chọn λ Box-Cox bằng số, không bằng mắt, để dao động không còn đổi theo mức.",
        la_gi="Chia chuỗi thành từng năm. Sau Box-Cox, dao động của năm có mức μ gần bằng s / μ^(1−λ). Chọn λ làm các tỷ số này đều nhất, tức CV nhỏ nhất.",
        doc_tieu="Ba năm μ = 100, 400, 900; s = 10, 20, 30",
        thang=[("λ = 1", "tỷ số 10, 20, 30: dao động lớn dần"), ("λ = 0,5", "tỷ số 1, 1, 1: đều hoàn toàn"), ("λ = 0", "0,1; 0,05; 0,033: log ép quá tay")],
        vi_du="λ = 1: ba tỷ số có độ lệch chuẩn 10, trung bình 20, CV = 0,5. λ = 0,5: CV = 0. Bán lẻ Mỹ: CV nhỏ nhất ở λ ≈ 0,34."),
    "exp-trung-vi": dict(
        tieu="Vì sao exp của dự báo log ra trung vị", phan="A", buoi="Buổi 5", hinh=(5, "kn-doi-nguoc"),
        muc="Biết đổi ngược cho ra con số nào, và khi nào phải nhân thêm hệ số để ra trung bình.",
        la_gi="exp giữ thứ tự, nên số đứng giữa trên thang log vẫn đứng giữa: đó là trung vị. Nhưng exp kéo giãn phía trên, đẩy trung bình lên cao hơn.",
        doc_tieu="Khi nào hiệu chỉnh",
        thang=[("cần tổng", "cần tổng hay trung bình: nhân 1 + σ²/2"), ("chấm MAE", "không cần: MAE ưa trung vị"), ("σ nhỏ", "phần hụt không đáng kể")],
        vi_du="Log 0, 1, 2: exp(1) = 2,72 là số đứng giữa, còn trung bình thật là 3,70. σ = 0,5 thì trung vị thấp hơn trung bình 11,75%."),
    "ty-le-mau-hinh": dict(
        tieu="Tỷ lệ mẫu hình: phần dư còn nhịp lịch không", phan="A", buoi="Buổi 6", hinh=(6, "phan-du-so-sanh"),
        muc="Kiểm một phân rã đã lấy hết mùa vụ chưa bằng một con số, không chỉ bằng mắt.",
        la_gi="Nhóm phần dư theo lịch (tháng × giờ, thứ × giờ), lấy trung bình mỗi nhóm, rồi đo các trung bình đó lệch nhau cỡ nào so với dao động của cả chuỗi.",
        doc_tieu="PJM 2024, nhóm tháng × giờ",
        thang=[("0,0006", "MSTL (24, 168): phần dư gần như sạch"), ("0,102", "cổ điển chu kỳ 24: một phần mười còn là mẫu hình")],
        vi_du="Phần dư sáng −3, −5; chiều +3, +5: trung bình nhóm −4 và +4, phương sai 32. Chuỗi có phương sai 320 thì tỷ lệ 0,1: còn nhịp sáng – chiều."),
    "stl-loess": dict(
        tieu="STL: mùa vụ lấy trung bình cục bộ, đổi dần", phan="A", buoi="Buổi 6", hinh=(6, "kn-stl-loess"),
        muc="Hiểu vì sao STL cho mùa vụ tháng 7 khác tháng 1, còn phân rã cổ điển thì không.",
        la_gi="Cổ điển lấy một trung bình cho mọi quý 1 của mọi năm. STL dùng LOESS: mùa vụ mỗi năm chỉ nhìn vài năm lân cận, năm gần nặng hơn.",
        doc_tieu="Cửa sổ xu hướng quá ngắn",
        doc="Xu hướng mềm quá thì ôm luôn nhịp tuần lẫn thời tiết, phần dư nhỏ giả tạo: STL(period = 24) trên PJM còn 2,8 GW², MSTL 16,5 GW².",
        vi_du="Quý 1 trừ xu hướng qua 5 năm: 2, 4, 6, 8, 10. Cổ điển: mùa vụ 6, phần dư −4 tới 4. Trung bình 3 năm: 3, 4, 6, 8, 9, phần dư −1 tới 1."),
    "ljung-box-q": dict(
        tieu="Q* vượt ngưỡng χ² mới là còn quy luật", phan="A", buoi="Buổi 7", hinh=(7, "kn-ljung-box"),
        muc="Tự tính, tự đọc con số Ljung-Box, và khai đúng bậc tự do khi kiểm sai số của mô hình.",
        la_gi="Nếu chuỗi là nhiễu trắng, Q* theo phân phối χ². Bậc tự do là số trễ gộp vào, trừ số tham số nếu kiểm sai số của một mô hình.",
        doc_tieu="Ngưỡng 5% của χ²",
        thang=[("2 bậc tự do", "5,99"), ("8 bậc tự do", "15,51"), ("10 bậc tự do", "18,31")],
        vi_du="100 điểm, r₁ = 0,2, r₂ = 0,1: Q* ≈ 5,16, nhỏ hơn 5,99 nên chưa bác bỏ nhiễu trắng (p ≈ 0,076). 10 trễ, mô hình 2 tham số: 8 bậc."),
    "random-walk": dict(
        tieu="Random walk: càng lâu càng có thể đi xa", phan="A", buoi="Buổi 7", hinh=(7, "kn-random-walk"),
        muc="Thấy vì sao random walk không dừng, phải sai phân, và dự báo tốt nhất là giá trị cuối.",
        la_gi="Vị trí mới bằng vị trí cũ cộng một bước ngẫu nhiên. Không có mức để quay về, nên độ dao động nở ra theo căn bậc hai số bước.",
        doc_tieu="Độ lệch chuẩn vị trí, 10.000 người mô phỏng",
        thang=[("4 bước", "2,0"), ("25 bước", "5,0"), ("100 bước", "10,1")],
        vi_du="Sáu lần tung +1, −1, +1, +1, −1, +1: vị trí 1, 0, 1, 2, 1, 2. Số bước gấp 25 lần thì độ lệch chuẩn gấp 5 lần."),
    "entropy": dict(
        tieu="Spectral entropy: năng lượng dồn hay trải đều", phan="A", buoi="Buổi 9", hinh=(9, "entropy-hai-chuoi"),
        muc="Xếp hạng độ khó của hàng nghìn chuỗi trước khi chạy bất kỳ mô hình nào.",
        la_gi="Đổi phổ thành các phần năng lượng cộng lại bằng 1, như chia một chiếc bánh. Entropy đo bánh chia đều tới đâu: 0 là dồn một đĩa, 1 là chia đều.",
        doc_tieu="Ví dụ phổ 4 tần số",
        thang=[("0", "sóng đều: 0; 1; 0; 0"), ("0,5", "hai nhịp: 0,5; 0,5; 0; 0"), ("1", "nhiễu: 0,25 mỗi tần số")],
        vi_du="Chuỗi mùa vụ 12 tháng: 0,33. Nhiễu thuần: 0,94. Trên 4.000 chuỗi M4: trung vị 0,462; một phần năm số chuỗi từ 0,666 trở lên."),
    "do-phan-giai": dict(
        tieu="Đo độ phân giải trước khi gọi cảm biến kẹt", phan="B", buoi="Buổi 10", hinh=(10, "kn-cam-bien-dung-yen-stuck-sensor"),
        muc="Phân biệt số lặp vì cảm biến làm tròn với số lặp vì cảm biến hỏng.",
        la_gi="Độ phân giải: bước nhỏ nhất cảm biến ghi được. Cảm biến đứng yên (kẹt): ghi lặp một giá trị nhiều giờ liền dù thực tế đã đổi.",
        doc_tieu="Nhận ra thế nào",
        doc="Thực tế đổi chưa tới một bước phân giải thì số ghi vẫn lặp: bình thường. Thực tế đổi vài độ, cả ngày lẫn đêm, mà số không đổi: kẹt.",
        vi_du="Thật 25,6; 25,8; 26,1; 26,3; 26,4 °C, ghi tới 1 °C thành năm số 26. Nội Bài: ngưỡng 12 giờ ra 24 đoạn lặp, nên buổi này dùng 18 giờ."),
    "dien-nhan-qua": dict(
        tieu="Điền nhân quả: có số mới, số cũ không đổi", phan="B", buoi="Buổi 10", hinh=(10, "kn-nhan-qua-cach-dien"),
        muc="Biết cách điền nào dùng được khi dự báo thật, và kiểm điều đó bằng máy.",
        la_gi="Cách điền nhân quả chỉ dùng dữ liệu trước ô đang điền. Nội suy hai phía nhìn cả số phía sau; nếu số đó thuộc tập kiểm thì là rò rỉ.",
        doc_tieu="Kiểm bằng cắt dữ liệu",
        doc="Làm sạch dữ liệu đầy đủ và dữ liệu cắt tại một mốc, so phần trước mốc. Mốc cắt phải nằm trong một lỗ, nếu không bài kiểm luôn báo sạch.",
        vi_du="Chuỗi 20, NaN, 30: ffill điền 20, cắt hay không cũng 20. Tuyến tính điền 25 nhờ số 30; cắt tại mốc thứ hai thì không điền được, hoặc điền khác."),
    "z-score-masking": dict(
        tieu="z-score: ngoại lai kéo cả ngưỡng lên theo", phan="B", buoi="Buổi 11", hinh=(11, "masking-10-so"),
        muc="Hiểu vì sao ngưỡng 3σ bỏ sót ngoại lai, để không đọc “không vượt 3σ” thành “dữ liệu sạch”.",
        la_gi="z-score đo một điểm cách trung bình bao nhiêu lần độ lệch chuẩn. Masking: ngoại lai kéo cả trung bình lẫn độ lệch chuẩn lên, nên tự che mình và che nhau.",
        doc_tieu="Nhận ra thế nào",
        doc="Thêm một điểm cực lớn mà số điểm bị gắn cờ lại giảm là đang bị che. Cách chữa: đo bằng trung vị (slide sau).",
        vi_du="10, 12, 11, 13, 12, 50, 11, 12, 13, 12: trung bình 15,6, s ≈ 12,1, nên z của 50 chỉ 2,84, không vượt 3."),
    "mad-hampel": dict(
        tieu="MAD và Hampel: đo bằng trung vị, so tại chỗ", phan="B", buoi="Buổi 11", hinh=(11, "kn-bo-loc-hampel"),
        muc="Có thước đo độ dao động mà ngoại lai không kéo được, và so mỗi điểm với mức quanh nó.",
        la_gi="MAD là trung vị của khoảng cách tới trung vị, nhân 1,4826 để cùng thang với độ lệch chuẩn. Hampel tính MAD trên cửa sổ quanh mỗi điểm.",
        doc_tieu="Điểm MAD lớn hay nhỏ nghĩa là gì",
        thang=[("≤ 3", "bình thường so với mức quanh nó"), ("> 3", "gắn cờ ngoại lai")],
        vi_du="Cùng 10 số: trung vị 12, MAD = 1,4826 × 1 ≈ 1,48. Điểm của 50 là 38 / 1,48 ≈ 25,6: bị gắn cờ. Điểm của 10 chỉ 1,35."),
    "xu-ly-bat-thuong": dict(
        tieu="Gắn cờ xong: giữ, winsorize hay biến giả", phan="B", buoi="Buổi 11", hinh=(11, "kn-winsorize"),
        muc="Chọn cách sửa theo loại bất thường và theo nhật ký sự kiện, mà vẫn giữ đủ số mốc.",
        la_gi="Winsorize kéo điểm bị gắn cờ về trung vị địa phương, không xoá. Nhật ký sự kiện: danh sách mốc có sự kiện thật. Biến giả: cột 0/1 đánh dấu sự kiện.",
        doc_tieu="Chọn theo loại",
        thang=[("lỗi đo", "winsorize"), ("sự kiện thật", "giữ, ghi nhật ký"), ("dịch mức", "thêm biến giả")],
        vi_du="12, 11, 13, 90, 12: xoá thì lưới thủng một mốc; winsorize ra 12, 11, 13, 12, 12 kèm cột da_sua = 1; nếu ngày đó là Tết thì giữ 90."),
    "penalty": dict(
        tieu="PELT: mỗi điểm gãy phải trả một penalty", phan="B", buoi="Buổi 11", hinh=(11, "kn-penalty-phat"),
        muc="Tìm mốc mà chuỗi trước và sau khác nhau, không cắt vụn chuỗi ra từng điểm.",
        la_gi="Chi phí một đoạn là tổng bình phương khoảng cách tới trung bình đoạn. PELT chọn điểm gãy sao cho tổng chi phí cộng penalty nhỏ nhất.",
        doc_tieu="Penalty lớn hay nhỏ nghĩa là gì",
        thang=[("nhỏ", "cắt nhiều, dễ ra điểm gãy giả"), ("vừa", "quét nhiều mức, giữ kết quả ổn định"), ("lớn", "ít hoặc không còn điểm gãy")],
        vi_du="10, 11, 10, 9, 10, 20, 21, 19, 20, 20, penalty ≈ 6,9: không cắt tốn 254; cắt một lần 4 + 6,9 = 10,9; cắt hai lần 3,17 + 13,8 = 17,0."),
    "nyquist": dict(
        tieu="Nyquist: lấy mẫu thưa thì sinh nhịp giả", phan="B", buoi="Buổi 12", hinh=(12, "kn-aliasing"),
        muc="Hạ mẫu mà không tạo ra một chu kỳ không có thật trong dữ liệu.",
        la_gi="Tần số Nyquist bằng nửa tần số lấy mẫu f_s. Dao động nhanh hơn Nyquist bị gập thành dao động chậm giả: đó là aliasing.",
        doc_tieu="Tính nhịp giả thế nào",
        doc="Lấy tần số thật trừ bội số gần nhất của f_s. Muốn tránh: lọc thông thấp, tức bỏ dao động nhanh, trước khi hạ mẫu.",
        vi_du="Sóng lặp mỗi 4 bước, lấy mẫu mỗi 3 bước: |1/4 − 1/3| = 1/12, ra sóng giả lặp mỗi 12 bước. Dao động 43 phút thành chu kỳ giả 2,5 giờ."),
    "sau-ho-loc": dict(
        tieu="Lọc hai chiều không trễ vì nhìn tương lai", phan="B", buoi="Buổi 12", hinh=(12, "kn-sosfilt-sosfiltfilt"),
        muc="Biết họ bộ lọc nào dùng được làm feature dự báo, họ nào chỉ để mô tả lịch sử.",
        la_gi="Savitzky–Golay khớp đa thức quanh mỗi điểm. Butterworth cắt tần số theo ngưỡng. Kalman ước lượng tín hiệu ẩn. Bản hai chiều chạy xuôi rồi ngược.",
        doc_tieu="Nhân quả hay không",
        thang=[("nhân quả", "trailing, EWMA, sosfilt, Kalman filter (tham số cố định)"), ("nhìn tương lai", "centered, Savitzky–Golay, sosfiltfilt, Kalman smoother")],
        vi_du="Đổi 10 số cuối: sosfilt giữ nguyên quá khứ; filtfilt đổi tới 23,615 và kéo ngược 274 bước. Butterworth nhân quả trễ 19 bước."),
    "kiem-nhan-qua": dict(
        tieu="Đổi số cuối: nhân quả thì quá khứ đứng yên", phan="B", buoi="Buổi 12", hinh=(12, "kiem-nhan-qua"),
        muc="Có một phép thử chạy được trên mọi hàm làm trơn, kể cả khi tài liệu thư viện không nói rõ.",
        la_gi="Đổi vài giá trị cuối chuỗi, chạy lại bộ lọc, so đầu ra ở mọi mốc trước đó. Nhân quả thì quá khứ không đổi, chỉ lệch cỡ sai số tính toán.",
        doc_tieu="Ba chỗ hay làm sai",
        doc="So mọi mốc trước điểm đổi, không bỏ đoạn cuối. Dung sai theo thang dữ liệu. Tham số ước lượng trên cả chuỗi cũng làm quá khứ đổi.",
        vi_du="10, 12, 14, 30, 16, đổi 16 thành 40: centered ở giờ 4 từ 20 thành 28, trailing vẫn 18,67. Kalman khớp lại trên cả chuỗi đổi quá khứ 1,134."),
    "ca-chuoi": dict(
        tieu="Số tính trên cả chuỗi mang tương lai vào", phan="A", buoi="Buổi 13", hinh=(10, "kn-nhan-qua-cach-dien"),
        muc="Nhận ra rò rỉ không chỉ ở lag hay rolling, mà ở mọi con số tính trên toàn bộ dữ liệu.",
        la_gi="Một con số tính trên cả dữ liệu, kể cả phần tương lai, rồi đưa vào feature từng ngày: trung bình, độ lệch chuẩn, trung bình nhóm, nội suy hai phía.",
        doc_tieu="Ba kiểu và cách sửa",
        thang=[("chuẩn hoá cả chuỗi", "fit scaler chỉ trên phần học"), ("target encoding", "chỉ dùng các ngày trước t"), ("nội suy hai phía", "ffill: chỉ dùng số đã có")],
        vi_du="10, 12, 8, 14, 20, 16: trung bình 13,33 đã chứa hai ngày cuối. Nhóm A (10, 8, 20) = 12,67: ngày 1 đã “biết” số 20 của ngày 5."),
    "kiem-ro-ri": dict(
        tieu="Kiểm rò rỉ: cắt tương lai và nhiễu mục tiêu", phan="A", buoi="Buổi 13", hinh=(13, "kn-kiem-nhieu-muc-tieu"),
        muc="Bắt rò rỉ bằng máy trên mọi hàm tạo feature, không phải đọc từng dòng code.",
        la_gi="Cắt tương lai: cắt dữ liệu, tính lại feature, so mọi dòng trước mốc cắt. Nhiễu mục tiêu: đổi y từ một mốc, xem feature lẽ ra đã biết có đổi không.",
        doc_tieu="Mỗi bài bắt gì",
        thang=[("cắt tương lai", "rolling không shift, số tính trên cả chuỗi"), ("nhiễu mục tiêu", "lag nhỏ hơn tầm dự báo h")],
        vi_du="Cắt sau ngày 4: cột có tâm đổi từ 14 thành NaN, cột đã shift giữ nguyên. Với h = 24, lag_1 đổi ở 23 dòng ngay sau mốc: bị bắt."),
    "ex-ante": dict(
        tieu="Ngoại sinh: dùng bản dự báo, không số thật", phan="A", buoi="Buổi 13", hinh=(13, "du-bao-vs-that"),
        muc="Đưa nhiệt độ hay số liệu công bố vào mô hình đúng dạng sẽ có trong tay lúc chạy thật.",
        la_gi="Biến ngoại sinh là biến ngoài chuỗi dùng làm feature. Ex-ante: chỉ dùng bản có lúc dự báo. Ex-post: dùng cả số thật về sau, tức rò rỉ.",
        doc_tieu="Nhận ra thế nào",
        doc="Hỏi với từng biến: lúc ra dự báo đã có con số này chưa? Số bị sửa sau công bố (GDP) thì dùng bản point-in-time, đúng như lúc đó.",
        vi_du="Trưa mai thật 35 °C, bản dự báo có tối nay 33 °C: feature phải là 33. Dự báo trước 1 ngày sai trung bình 1,32 °C, trước 3 ngày 2,07 °C."),
    "mape-lech": dict(
        tieu="MAPE phạt dự báo cao nặng hơn dự báo thấp", phan="D", buoi="Buổi 14", hinh=(14, "chi-so-quyet-dinh"),
        muc="Biết MAPE đẩy dự báo về phía thấp, trước khi dùng nó để chọn mô hình hay đặt hàng.",
        la_gi="MAPE chia sai số cho thực tế. Dự báo thấp sai nhiều nhất 100% (dự báo 0); dự báo cao thì sai bao nhiêu phần trăm cũng được.",
        doc_tieu="Nhận ra thế nào",
        doc="Tối ưu MAPE thì dự báo thấp hơn cả trung vị. sMAPE mang tên “đối xứng” nhưng cũng không đối xứng.",
        vi_du="Cùng lệch 50: thực tế 100, dự báo 150 cho MAPE 50%; thực tế 150, dự báo 100 chỉ 33,3%. Doanh số mô phỏng: MAE tối ưu ở 20,0, MAPE ở 9,1."),
    "phan-du": dict(
        tieu="Phần dư sạch: không còn gì để khai thác", phan="D", buoi="Buổi 14", hinh=(14, "chan-doan-phan-du"),
        muc="Kiểm mô hình đã khai thác hết quy luật trong dữ liệu chưa.",
        la_gi="Phần dư là thực tế trừ giá trị khớp (fitted) trên phần học. Sai số dự báo thì đo trên kỳ chấm, phần mô hình chưa thấy.",
        doc_tieu="Phần dư sạch trông thế nào",
        doc="Trung bình gần 0, không còn tự tương quan, độ dao động ổn định, và gần hình chuông (kiểm bằng Jarque–Bera).",
        vi_du="Phần dư của seasonal naive trên một chuỗi M4 có Ljung-Box p = 0,000: vẫn còn quy luật bị bỏ sót."),
    "chi-so": dict(
        tieu="Mỗi chỉ số thưởng một kiểu dự báo", phan="D", buoi="Buổi 14", hinh=(14, "chi-so-quyet-dinh"),
        muc="Chọn thước đo sai số khớp với cái giá thật của sai lệch.",
        la_gi="MAE là trung bình độ lớn sai số. RMSE là căn của trung bình sai số bình phương. ME là trung bình sai số có dấu.",
        doc_tieu="ME dương hay âm nghĩa là gì",
        thang=[("ME < 0", "dự báo cao hơn thực tế"), ("ME ≈ 0", "không lệch một phía"), ("ME > 0", "dự báo thấp hơn thực tế")],
        vi_du="Thực tế 10, 12, 8, 14, 16 và dự báo 11, 10, 9, 14, 12 cho MAE 1,6, RMSE 2,10 và ME 0,8."),
    "phan-tram": dict(
        tieu="Có số 0 thì MAPE hỏng", phan="D", buoi="Buổi 14", hinh=(14, "doi-chi-so-doi-hang"),
        muc="So sai số giữa các chuỗi khác đơn vị, khác cỡ, kể cả chuỗi có số 0.",
        la_gi="MAPE chia sai số cho thực tế. sMAPE chia cho trung bình của |thực tế| và |dự báo|. WAPE chia tổng sai số cho tổng thực tế.",
        doc_tieu="Nhận ra thế nào",
        doc="Có ngày thực tế bằng 0 thì MAPE ra vô hạn. Đổi chỉ số là đổi hạng: trên bán lẻ, mỗi chỉ số chọn một baseline hạng nhất khác.",
        vi_du="Bán lẻ, 300 mã hàng: MAPE không tính được ở cả 300. utilsforecast trả MAPE, sMAPE ở thang 0–1: lệch 100 và 200 lần so với số phần trăm."),
    "kfold": dict(
        tieu="K-fold xáo trộn hứa thấp hơn thật 23%", phan="D", buoi="Buổi 15", hinh=(15, "uoc-luong-sai-so"),
        muc="Chọn cách ước lượng sai số khớp với sai số lúc chạy thật.",
        la_gi="Hold-out là một đoạn tương lai giữ riêng, chỉ chấm một lần. K-fold xáo trộn chia dữ liệu ngẫu nhiên thành K phần.",
        doc_tieu="Nhận ra thế nào",
        doc="Càng sát hold-out càng đáng tin. K-fold chỉ tạm dùng được khi mô hình chỉ dùng lag và phần dư không còn tự tương quan.",
        vi_du="Rừng ngẫu nhiên trên tải điện: K-fold lệch 23% so với hold-out, rolling origin chỉ lệch 9%."),
    "rolling-origin": dict(
        tieu="Rolling origin: backtest như chạy thật", phan="D", buoi="Buổi 15", hinh=(15, "sai-so-cua-so-va-h"),
        muc="Đo sai số ở nhiều thời điểm như lúc chạy thật, thay vì tin vào một lần may rủi.",
        la_gi="Đặt nhiều cutoff; ở mỗi cutoff học trên quá khứ rồi dự báo đoạn ngay sau. Refit là học lại mỗi cửa sổ; gap là độ trễ dữ liệu.",
        doc_tieu="Nhận ra thế nào",
        doc="Sai số từng cửa sổ dao động mạnh thì phải báo cả phân bố, không chỉ trung bình. Sai số tăng theo h thì nhìn đúng tầm cần dùng.",
        vi_du="30 mốc, h = 4, gap = 2: cutoff cuối = 30 − 1 − 2 − 4 = 23, lùi đều 4 bước được 19 và 15."),
    "ba-doan": dict(
        tieu="Luyện, thi thử, thi thật: ba đoạn riêng", phan="D", buoi="Buổi 15", hinh=(15, "chon-bao-cao"),
        muc="Con số báo cáo phản ánh đúng sai số tương lai, không bị làm đẹp vì đã dùng nó để chọn.",
        la_gi="Đoạn luyện để tune tham số, đoạn thi thử để chọn mô hình, đoạn thi thật để báo cáo và chỉ mở một lần.",
        doc_tieu="Nhận ra thế nào",
        doc="Chọn và báo cáo trên cùng một đoạn thì con số báo cáo luôn lạc quan hơn thật.",
        vi_du="Chọn và báo cáo trên cùng một đoạn làm MASE trông tốt hơn thật 25%."),
    "dm": dict(
        tieu="Diebold–Mariano: chênh lệch có thật hay may rủi", phan="D", buoi="Buổi 15", hinh=(15, "dm-tu-tuong-quan"),
        muc="Biết hai mô hình chênh nhau thật, hay chỉ do may rủi.",
        la_gi="Diebold–Mariano lấy chênh lệch sai số trung bình của hai mô hình, chia cho sai số chuẩn của chính chênh lệch đó.",
        doc_tieu="p lớn hay nhỏ nghĩa là gì",
        thang=[("p < 0,05", "chênh lệch có thật"), ("p ≥ 0,05", "chưa có bằng chứng mô hình nào hơn")],
        vi_du="Ví dụ trong buổi: p = 0,45, chưa có bằng chứng. Với dự báo nhiều bước, dùng bản hiệu chỉnh HLN kẻo p nhỏ giả tạo."),
}

# Slide vấn đề: tiêu đề, buổi, hình, câu mở (trích "dg" hoặc định nghĩa "dn" = (từ, phần còn lại)), ba thẻ.
VD = {
    "mui-gio": dict(tieu="Sai múi giờ: giờ giả, nóng lúc 20h", buoi="Buổi 3",
        hinh=[(3, "dst-hai-ngay", "Đổi giờ mùa hè: giờ 0 chuyến giả"), (3, "gio-nong-nhat", "Ghép lệch múi giờ")],
        dg="khi làm dữ liệu, lưu tâm múi giờ trước tiên.",
        dau="Một giờ bằng 0 lúc rạng sáng Chủ nhật tháng 3, và giờ nóng nhất trong ngày rơi vào 20h.",
        kiem="In các giờ 00:00–05:00 của ngày đổi giờ, rồi xem giờ nóng nhất trung bình có rơi vào buổi chiều không.",
        sua="Gắn đúng múi giờ, đổi sang UTC, rồi mới gộp và ghép."),
    "gop": dict(tieu="Gộp thô quá thì mất mùa vụ", buoi="Buổi 4", hinh=[(4, "gop-tan-suat")],
        dg="gộp theo tháng thì nhịp ngày, nhịp tuần và những ngày bất thường đều biến mất.",
        dau="Kết luận “không có mùa vụ tuần”, hoặc giờ thiếu hiện thành số 0.",
        kiem="Vẽ heatmap giờ × thứ và ACF tới trễ 168; đếm NaN trên lưới giờ đầy đủ.",
        sua="Vẽ ở nhiều mức gộp. Khi cộng, dùng sum(min_count=1) để giờ thiếu vẫn là NaN."),
    "bieu-do-sai": dict(tieu="Hai đường trùng khít vì chọn thang", buoi="Buổi 4",
        hinh=[(4, "gay-hieu-nham", "Trước: trục kép, trục trái cắt ở 90.000"), (4, "ve-lai", "Sau: tách hình, vẽ từ 0")],
        dg="biểu đồ đẹp chưa chắc đúng: đọc thang trước khi đọc đường.",
        dau="Hai trục dọc trên cùng một hình, hoặc trục y không bắt đầu từ 0.",
        kiem="Đọc thang của từng trục, và xem tháng thấp nhất có bị vẽ sát đáy như gần bằng 0 không.",
        sua="Tách thành hai hình, số đếm vẽ từ 0, và nói về quan hệ bằng scatter."),
    "dao-dong": dict(tieu="Doanh thu tăng chưa chắc bán nhiều hơn", buoi="Buổi 5",
        hinh=[(5, "dao-dong-theo-muc", "Dao động lớn dần theo mức"), (5, "danh-nghia-thuc", "Danh nghĩa gấp 4, thực chỉ +42%")],
        dg="doanh thu tăng có thể vì giá tăng, dân số tăng, hay mỗi người mua nhiều hơn thật.",
        dau="Biên độ dao động lớn dần theo mức, hoặc câu kiểu “doanh số tăng gấp 4 lần”.",
        kiem="So độ lệch chuẩn từng năm với mức của năm đó; vẽ cạnh nhau chuỗi danh nghĩa và chuỗi đã trừ lạm phát.",
        sua="Lấy log hoặc Box-Cox; chia cho CPI, cho dân số, và cho số ngày trong tháng."),
    "doi-nguoc": dict(tieu="Log rồi exp ngược thì ra trung vị", buoi="Buổi 5", hinh=[(5, "bias-log-normal")],
        dn=("Đổi ngược", " từ thang log bằng exp cho ra trung vị, thấp hơn trung bình."),
        dau="Cộng dự báo của nhiều cửa hàng thì ra một tổng thấp hơn tổng thật.",
        kiem="So tổng các dự báo với tổng thực tế trên kỳ chấm.",
        sua="Cần tổng hay trung bình thì nhân 1 + σ²/2 (σ đo trên thang log). Chấm bằng MAE, vốn ưa trung vị, thì không cần."),
    "chu-ky-sai": dict(tieu="Khai sai chu kỳ: nhịp tuần chui vào xu hướng", buoi="Buổi 6", hinh=[(6, "co-dien-24")],
        dg="khai chu kỳ 24 cho chuỗi có nhịp tuần thì nhịp tuần chạy vào xu hướng.",
        dau="Đường xu hướng lõm xuống mỗi cuối tuần.",
        kiem="Tính trung bình của đường xu hướng theo từng thứ; cuối tuần thấp hẳn là có vấn đề.",
        sua="Dùng MSTL(24, 168). Giờ hỏng lẻ thì bật robust=True; đợt nóng nhiều ngày thì cần thêm biến nhiệt độ."),
    "sai-phan": dict(tieu="Sai phân thừa làm chuỗi tệ hơn", buoi="Buổi 7", hinh=[(7, "sai-phan-thua")],
        dg="sai phân như thuốc: đúng liều thì khỏi, quá liều thì hại.",
        dau="Sau khi sai phân, r₁ về gần −0,5 và độ lệch chuẩn lại tăng (0,96 lên 1,29).",
        kiem="Chạy ADF và KPSS trước khi sai phân, và xem ACF sau khi sai phân.",
        sua="Bớt một lần sai phân. Xu hướng thẳng thì khử xu hướng. Có mùa vụ thì sai phân mùa vụ (trừ mùa trước) trước."),
    "tuong-quan-gia": dict(tieu="r = 0,97 chưa chắc là quan hệ thật", buoi="Buổi 8", hinh=[(8, "tuong-quan-gia")],
        dn=("Tương quan giả", " là r rất cao chỉ vì hai chuỗi cùng tăng theo thời gian."),
        dau="CPI và dân số Mỹ có r = 0,97.",
        kiem="Tính lại r trên phần thay đổi (sai phân): chỉ còn −0,21. Durbin–Watson gần 0 cũng là một dấu hiệu.",
        sua="Sai phân rồi đo lại. Khi viết kết luận, nói “đi cùng”, đừng nói “gây ra”."),
    "chu-u": dict(tieu="Lạnh cũng tăng, nóng cũng tăng: hình chữ U", buoi="Buổi 8", hinh=[(8, "chu-u")],
        dg="trời nóng bật điều hoà, trời lạnh bật sưởi: tải điện tăng ở cả hai phía.",
        dau="Pearson 0,616 trông khá mạnh, nhưng là trộn nhánh lạnh (−0,649) với nhánh nóng (+0,910); scatter có hình chữ U.",
        kiem="Vẽ scatter trước; đo thêm mutual information, thứ bắt được cả quan hệ cong.",
        sua="Tách nhiệt độ thành CDD (độ nóng) và HDD (độ lạnh) quanh 18,33 °C: R² tăng từ 0,379 lên 0,812."),
    "thieu-moc": dict(tieu="isna() không thấy dòng bị mất", buoi="Buổi 10", hinh=[(10, "hai-loai-thieu")],
        dn=("Thiếu mốc", " là mất cả dòng; thiếu giá trị là còn dòng nhưng ô rỗng. isna() chỉ thấy loại sau."),
        dau="Từ 00:00 tới 02:30 phải có 6 mốc 30 phút, nhưng tệp chỉ có 5 dòng.",
        kiem="So số dòng với số mốc của lưới thời gian đầy đủ, và đếm mốc trùng.",
        sua="reindex lên lưới đầy đủ trước mọi việc khác, để mốc bị mất hiện ra thành NaN."),
    "mnar": dict(tieu="Thiếu vì chính giá trị: điền kiểu gì cũng lệch", buoi="Buổi 10", hinh=[(10, "mnar")],
        dn=("MNAR", " là thiếu vì chính giá trị, như cảm biến tắt đúng lúc ô nhiễm quá cao."),
        dau="Điền xong mà trung bình vẫn lệch: mất 16,2% số điểm ở phía cao thì trung bình còn −0,30 thay vì −0,005.",
        kiem="So trạm hàng xóm lúc trạm này thiếu và lúc có số. Dongsi thiếu thì trạm khác còn thấp hơn 3%: không phải MNAR.",
        sua="Thiếu do may rủi (MCAR) hay do thứ đã đo được (MAR) thì còn điền được. MNAR thì đừng điền."),
    "tra-hinh": dict(tieu="9,999 km không phải số đo", buoi="Buổi 10", hinh=[(10, "gia-tri-tra-hinh")],
        dn=("Mã trá hình", " là con số quy ước của nguồn, như 9,999 nghĩa là “tầm nhìn từ 10 km trở lên”."),
        dau="Một giá trị chiếm tới 35% số dòng; hoặc số 0 rơi đúng những ngày hết hàng.",
        kiem="Chạy value_counts().head(), đọc tài liệu nguồn; đo độ phân giải trước khi gọi đoạn lặp là cảm biến kẹt.",
        sua="Đổi thành NaN kèm cột cờ; số 0 do hết hàng cũng là thiếu. Đừng xoá cả dòng, các cột khác vẫn dùng được."),
    "so-sanh-dien": dict(tieu="Chấm cách điền: che thử, và che hai kiểu", buoi="Buổi 10", hinh=[(10, "so-sanh-dien")],
        dn=("Che nhân tạo", " là giấu bớt những ô đang có số, điền lại, rồi so với số thật."),
        dau="Nội suy tuyến tính đứng hạng 1 khi che từng điểm, nhưng tụt xuống hạng 5 khi che cả khối 48 giờ.",
        kiem="Che 10% số điểm và che nguyên khối 48 giờ, rồi chấm cả hai.",
        sua="Lỗ ngắn: tuyến tính hay ffill đều ổn. Lỗ dài: trạm hàng xóm, mùa vụ hôm trước, hoặc để trống."),
    "dien": dict(tieu="Lỗ dài: đừng lấp bằng đường phẳng", buoi="Buổi 10", hinh=[(10, "mot-lo-dai")],
        dg="không dùng tương lai để điền quá khứ; lỗ dài thì để trống.",
        dau="Có đoạn phẳng dài bất thường, hoặc backtest đẹp hẳn lên sau khi làm sạch.",
        kiem="Vẽ chuỗi quanh chỗ lỗ; chạy kiem_ro_ri với mốc cắt đặt ngay trong lỗ.",
        sua="Chia tập trước rồi mới điền, chỉ dùng cách điền nhân quả, và giới hạn độ dài lỗ được điền."),
    "masking": dict(tieu="3σ bỏ sót chính ngoại lai", buoi="Buổi 11", hinh=[(11, "masking")],
        dg="z-score dùng để bắt ngoại lai, nhưng chính ngoại lai làm nó “mù”.",
        dau="Năm số 5, 5, 5, 5, 100: điểm 100 chỉ có z = 1,79 nên không bị gắn cờ.",
        kiem="Thêm một điểm cực lớn rồi đếm lại: số ngày bị gắn cờ giảm từ 16 còn 5 là đang bị che.",
        sua="Dùng MAD hoặc bộ lọc Hampel. Cả hai dựa trên trung vị nên ngoại lai không kéo được."),
    "hampel": dict(tieu="Hampel: so với mức địa phương", buoi="Buổi 11", hinh=[(11, "nguong-toan-chuoi")],
        dn=("MAD", " đo độ dao động bằng trung vị; Hampel dùng MAD trên một cửa sổ trượt quanh từng điểm."),
        dau="3σ toàn chuỗi chỉ gắn cờ 16 ngày, và toàn là những ngày mức cao.",
        kiem="Xem mỗi cách gắn cờ bao nhiêu phần trăm dữ liệu: Hampel 3,31%, STL robust tới 16,86%.",
        sua="Hampel ±15 ngày, sửa bằng winsorize (kéo về trung vị địa phương). Bản center=True chỉ để làm sạch, không làm feature."),
    "tet": dict(tieu="Tết không phải ngoại lai", buoi="Buổi 11", hinh=[(11, "tet-khong-phai-ngoai-lai")],
        dg="outlier không đồng nghĩa với lỗi; Tết là bất thường, nhưng là bất thường thật.",
        dau="Cả 10/10 đỉnh Tết bị gắn cờ ngoại lai, và đỉnh xê dịch tới 25 ngày giữa các năm.",
        kiem="Vẽ chuỗi quanh những mốc bị sửa, rồi đối chiếu với lịch lễ.",
        sua="Giữ nguyên, ghi vào nhật ký sự kiện, và thêm biến giả tính theo lịch âm."),
    "pelt": dict(tieu="Lấy log trước: 43 điểm gãy còn 2", buoi="Buổi 11", hinh=[(11, "diem-gay-pelt")],
        dn=("Điểm gãy", " là mốc mà trước và sau khác hẳn nhau. PELT tìm chúng, mỗi điểm phải trả một penalty."),
        dau="Chạy trên một chuỗi tăng trưởng ra tới 43 điểm gãy.",
        kiem="So số điểm gãy khi chạy trên log và trên mức gốc; quét nhiều mức penalty.",
        sua="Lấy log trước: còn 2 điểm, đúng quanh COVID. Chọn penalty trong khoảng mà kết quả ổn định."),
    "covid": dict(tieu="COVID: cách xử lý đổi sai số gần 3 lần", buoi="Buổi 11", hinh=[(11, "ba-cach-covid")],
        dg="cách xử lý COVID là một giả định về tương lai, nên phải kiểm bằng dự báo.",
        dau="MAPE năm 2023 chênh gần 3 lần: giữ nguyên 24,01%, nội suy 8,71%, cắt bỏ 18,11%.",
        kiem="Thử từng cách, rồi chấm dự báo trên năm sau đó.",
        sua="Nội suy nếu hành vi quay về như cũ; dịch mức kéo dài thì thêm biến giả. Ghi rõ giả định vào báo cáo."),
    "aliasing": dict(tieu="Đọc phổ trước khi lọc và hạ mẫu", buoi="Buổi 12",
        hinh=[(12, "pho-cam-bien", "Phổ: nhịp nào mạnh, nhiễu nằm ở đâu"), (12, "aliasing", "Hạ mẫu thô: chu kỳ giả 2,5 giờ")],
        dn=("Aliasing", " là khi lấy mẫu quá thưa, một dao động nhanh hoá thành nhịp chậm không có thật."),
        dau="Sau khi resample xuất hiện một chu kỳ lạ, chẳng hạn 2,5 giờ.",
        kiem="Đọc phổ trước và sau khi hạ mẫu; chu kỳ giả tính được: f_giả = |f − k·f_s|, f_s là tần số lấy mẫu.",
        sua="Lọc thông thấp, tức bỏ dao động nhanh, trước khi hạ mẫu."),
    "bo-loc": dict(tieu="Bộ lọc trơn nhất lại là bộ lọc nhìn tương lai", buoi="Buổi 12", hinh=[(12, "bo-loc")],
        dg="độ trơn phải trả bằng trễ, hoặc bằng việc nhìn tương lai.",
        dau="Ba bộ lọc có RMSE thấp nhất (centered, Kalman smoother, Savitzky–Golay) đều nhìn tương lai.",
        kiem="Thêm cột “nhân quả” vào bảng xếp hạng; đo độ trễ bằng tương quan chéo.",
        sua="Chỉ so các bộ lọc nhân quả với nhau. Trong nhóm này Kalman filter tốt nhất, RMSE 0,584."),
    "loc-tuong-lai": dict(tieu="Đổi số cuối mà số cũ đổi theo: đã nhìn tương lai", buoi="Buổi 12", hinh=[(12, "gia-ro-ri")],
        dn=("Bộ lọc nhân quả", " chỉ dùng dữ liệu tới thời điểm đang xét, không dùng số của các giờ sau."),
        dau="Feature làm trơn kiểu centered hứa giảm MAE 24–28%, còn feature nhân quả chỉ giúp 1–6%.",
        kiem="Đổi 10 giá trị cuối rồi chạy lại: đầu ra ở các mốc trước mà đổi theo là bộ lọc nhìn tương lai.",
        sua="Dùng trailing, EWMA hay sosfilt, tham số ước lượng trên phần học rồi cố định. Luôn chấm trên chuỗi gốc."),
    "muc-tieu-lam-tron": dict(tieu="Làm trơn mục tiêu là chấm trên đề dễ hơn", buoi="Buổi 12",
        hinh=[(12, "muc-tieu-lam-tron")],
        dg="không ai trả tiền điện “đã làm trơn”: luôn chấm trên chuỗi gốc.",
        dau="Chấm trên điện đã làm trơn (centered 13 điểm), MAE giảm từ 46,84 xuống 35,78 Wh (−23,6%) mà mô hình không đổi.",
        kiem="Chấm lại cùng mô hình trên chuỗi gốc; nhìn các đỉnh nhọn mà đường làm trơn đã cắt đi.",
        sua="Không làm trơn mục tiêu dùng để chấm. Cần “trung bình 3 giờ tới” thì định nghĩa lại mục tiêu và ghi rõ."),
    "ro-ri": dict(tieu="Rò rỉ: backtest đẹp, dùng thật tệ", buoi="Buổi 13", hinh=[(13, "kiem-ro-ri")],
        dn=("Rò rỉ tương lai", " là dùng thông tin chưa có lúc ra dự báo. Nó không báo lỗi, chỉ làm backtest đẹp giả."),
        dau="Sai số backtest đẹp hơn hẳn sai số khi chạy thật.",
        kiem="kiem_ro_ri: cắt ở nhiều mốc, tính lại, so từng dòng. Thêm kiểm nhiễu mục tiêu để bắt lag nhỏ hơn h.",
        sua="shift(h) rồi mới rolling; scaler và target encoding chỉ fit trên phần học."),
    "ngoai-sinh": dict(tieu="Học bằng nhiệt độ thật, chạy thật lại tệ hơn", buoi="Buổi 13", hinh=[(13, "gia-ro-ri")],
        dg="train bằng bản dự báo thì lúc chạy cũng dùng bản dự báo; đừng train bằng số thật.",
        dau="Backtest hứa giảm 3,85% sai số, nhưng chạy bằng dự báo trước 3 ngày thì sai số lại tăng 2,20%.",
        kiem="Hỏi với từng biến: lúc ra dự báo, con số này đã có trong tay chưa?",
        sua="Huấn luyện bằng các bản dự báo đã lưu lại; ghép bằng merge_asof có tolerance."),
    "chia-ngau-nhien": dict(tieu="Chia ngẫu nhiên là nhìn trộm tương lai", buoi="Buổi 15", hinh=[(15, "ba-cach-chia")],
        phan="D", dg="luôn học trên quá khứ, kiểm trên tương lai.",
        dau="Sai số lúc kiểm rất đẹp, chạy thật thì tệ.",
        kiem="Xem các điểm kiểm có nằm xen giữa các điểm học không.",
        sua="Chia theo thời gian: một đoạn hold-out, hoặc tốt hơn là rolling origin."),
}

# Công thức trên slide khái niệm và vấn đề: mã → (mathtext, câu nói bằng lời có thay số hoặc None).
# Viết theo ký hiệu của buoi-NN/tai-lieu.md; chữ Việt trong công thức đặt trong \mathrm{...}, dấu cách là "\ ".
CONG_THUC = {
    "baseline": (r"$\hat y_{T+h} = y_T \qquad \hat y_{T+h} = y_{T+h-m} \qquad "
                 r"\hat y_{T+h} = y_T + h\,\frac{y_T - y_1}{T-1}$",
                 "Naive, seasonal naive (h ≤ m), drift. Drift 10 → 18 trong 5 bước: dốc 1,6, bước sau 19,6."),
    "quantile": (r"$F(y) = \frac{\#\{y_i \leq y\}}{n}, \qquad q_p = \min\{\,y : F(y) \geq p\,\}$",
                 "Xếp tăng dần; q_p là số đầu tiên mà từ đó trở xuống đã có ít nhất tỷ lệ p số liệu."),
    "newsvendor": (r"$p^* = \frac{C_u}{C_u + C_o} \qquad L_\tau = \tau\,(y-c)\ \mathrm{khi\ thiếu}, \ \ "
                   r"(1-\tau)(c-y)\ \mathrm{khi\ thừa}$",
                   "Thiếu 4, thừa 1: p* = 4 / 5 = 0,8."),
    "do-lech-chuan": (r"$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(y_i-\bar y)^2}, \qquad z = \frac{y-\bar y}{s}$",
                      "2, 4, 6: s = √((4 + 0 + 4) / 2) = 2."),
    "con-so-bao": (r"$(y-c)^2 \rightarrow \mathrm{trung\ bình} \qquad |y-c| \rightarrow \mathrm{trung\ vị} \qquad "
                   r"L_\tau(y,c) \rightarrow q_\tau$", None),
    "khoang": (r"$[\,\bar y - 1{,}96\,s\ ;\ \bar y + 1{,}96\,s\,] \quad \mathrm{hoặc} \quad [\,q_{0{,}025}\ ;\ q_{0{,}975}\,]$",
               "Tỷ lệ phủ = số giá trị thật rơi vào khoảng chia tổng số giá trị."),
    "khoang-tin-cay": (r"$\mathrm{SE}(\bar y) = \frac{s}{\sqrt{n}}$", "s = 181, n = 25: 181 / 5 ≈ 36."),
    "kiem-dinh": (r"$p = \frac{k+1}{B+1}$",
                  "Xáo B lần; k là số lần chênh lệch khi xáo lớn bằng hoặc hơn chênh lệch thật."),
    "bootstrap": (r"$n_{\mathrm{eff}} \approx n\,\frac{1-\rho}{1+\rho}$", "200 điểm, ρ = 0,7: chỉ đáng giá như 35 điểm độc lập."),
    "utc": (r"$t_{\mathrm{UTC}} = t_{\mathrm{địa\ phương}} - \mathrm{offset}(t)$", "07:00 Hà Nội, offset +07:00 → 00:00 UTC."),
    "resample": (r"$\mathrm{nhãn}(t) = \left\lfloor \frac{t}{\Delta} \right\rfloor \times \Delta$",
                 "Δ = 1 giờ: chuyến lúc 9:40 vào ô 9:00."),
    "lam-tron": (r"$\tilde y_t = \frac{1}{w}\sum_{j=-k}^{k} y_{t+j}, \qquad w = 2k+1$",
                 "w = 3 quanh ngày thứ tư: (48 + 2 + 51) / 3 = 33,7."),
    "thang-log": (r"$\mathrm{độ\ cao} = \log_{10} y, \qquad \log_{10}(2y) - \log_{10} y = \log_{10} 2 = 0{,}301$",
                  "100 → 200 và 200 → 400 cao thêm như nhau: cùng gấp đôi."),
    "acf": (r"$r_k = \frac{\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)}{\sum_{t=1}^{T}(y_t-\bar y)^2}$",
            "Tử: độ lệch của các cặp cách nhau k bước nhân với nhau; mẫu: tổng bình phương độ lệch cả chuỗi."),
    "dieu-chinh": (r"$y^{\mathrm{ngày}}_t = \frac{y_t}{\mathrm{số\ ngày\ của\ tháng}\ t}, \qquad "
                   r"x_t = \frac{y_t}{z_t} \times z_{\mathrm{gốc}}$",
                   "z là CPI: 150 / 125 × 100 = 120 tỷ theo giá năm gốc."),
    "log": (r"$\log(a \times b) = \log a + \log b \quad \Rightarrow \quad \log(1{,}2\,y) - \log y = \log 1{,}2 = 0{,}182$",
            "Mọi cú tăng 20% đều cao thêm 0,182, dù từ 100 hay từ 1.000."),
    "box-cox": (r"$w_t = \log y_t\ \ (\lambda = 0), \qquad w_t = \frac{y_t^{\lambda} - 1}{\lambda}\ \ (\lambda \neq 0)$",
                "y = 100: λ = 1 cho 99; λ = 0,5 cho (10 − 1) / 0,5 = 18; λ = 0 cho 4,605."),
    "phan-ra": (r"$y_t = T_t + S_t + R_t \qquad y_t = T_t \times S_t \times R_t$",
                "Kiểu nhân là kiểu cộng trên log: log y = log T + log S + log R."),
    "phan-ra-cach": (r"$\hat T_t = \frac{1}{2m}\,y_{t-m/2} + \frac{1}{m}\sum_{j=-(m/2-1)}^{m/2-1} y_{t+j} + \frac{1}{2m}\,y_{t+m/2}$",
                     "2×m-MA khi m chẵn: hai điểm ở hai đầu mỗi điểm nửa trọng số, để cửa sổ có tâm."),
    "f-s": (r"$F_S = \max\left(0,\ 1 - \frac{\mathrm{Var}(R_t)}{\mathrm{Var}(S_t + R_t)}\right)$",
            "Phần dư chiếm 38% dao động của mùa vụ + phần dư thì F_S = 0,62."),
    "robust": (r"$u = \frac{|R|}{6\,\mathrm{median}(|R|)}, \qquad \rho = (1-u^2)^2\ \ (u < 1), \qquad \rho = 0\ \ (u \geq 1)$",
               "Phần dư 1, −2, 1, 20, −1: mốc 6 × 1 = 6; điểm 20 có u ≈ 3,3 → trọng số 0; điểm −2 → 0,79."),
    "ar": (r"$x_t = \rho\,x_{t-1} + \varepsilon_t$", "ρ = 0,7, đang ở 10: kỳ vọng bước sau 7, rồi 4,9."),
    "pacf": (r"$\phi_{22} = \frac{r_2 - r_1^2}{1 - r_1^2}$",
             "AR(1) có r₂ = r₁², nên φ₂₂ = 0: trễ 2 không thêm gì."),
    "ljung-box": (r"$Q^* = T(T+2)\sum_{k=1}^{\ell} \frac{r_k^2}{T-k}$",
                  "Gộp bình phương ACF của ℓ trễ đầu. Q* lớn thì p nhỏ: còn quy luật."),
    "dung": (r"$y_t = y_{t-1} + \varepsilon_t \qquad y_t = a + b\,t + u_t$",
             "Trái: random walk, không có mức để quay về. Phải: dừng quanh đường xu hướng a + b·t."),
    "sai-phan-la-gi": (r"$\nabla y_t = y_t - y_{t-1}, \qquad \nabla_m y_t = y_t - y_{t-m}$", "100, 103, 105 → 3, 2."),
    "scatter": (r"$r = \frac{\sum_i (x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_i (x_i-\bar x)^2 \cdot \sum_i (y_i-\bar y)^2}}$",
                "1, 2, 3 với 2, 4, 6 cho r = 1. Spearman: tính r trên thứ hạng."),
    "ccf": (r"$r_{xy}(k) = \mathrm{corr}(x_t,\ y_{t+k})$", "Đỉnh ở k > 0: x đi trước y k bước."),
    "truot": (r"$r_t = \mathrm{corr}\left(x_{t-w+1\,:\,t},\ \ y_{t-w+1\,:\,t}\right)$", "Mỗi ngày một r, tính trên w ngày gần nhất."),
    "granger": (r"$y_t = a + \sum_{i=1}^{p} b_i\,y_{t-i} + \sum_{i=1}^{p} c_i\,x_{t-i} + e_t, \qquad H_0:\ c_1 = \dots = c_p = 0$",
                "p nhỏ: quá khứ của x giúp dự báo y, chưa nói x gây ra y."),
    "entropy": (r"$H = \frac{-\sum_{i=1}^{N} p_i \ln p_i}{\ln N}, \qquad p_i = \frac{P_i}{\sum_j P_j}$",
                  "P_i là năng lượng ở tần số i. Dồn vào một tần số thì H ≈ 0; trải đều thì H = 1."),
    "dac-trung": (r"$\mathrm{CV}(1000\,a) = \frac{1000\,s}{1000\,\bar a} = \mathrm{CV}(a)$", "1,51 / 4 = 1.512 / 4.000 = 0,378."),
    "pho": (r"$f = \frac{1}{\mathrm{chu\ kỳ}}$", "Chu kỳ 12 tháng: f = 1 / 12 ≈ 0,083 vòng mỗi tháng."),
    "do-kho": (r"$\mathrm{sMAPE} = \frac{200}{h}\sum_t \frac{|y_t - \hat y_t|}{|y_t| + |\hat y_t|}$",
               "Chia cho mức của chuỗi, không chia cho độ khó của chuỗi như MASE."),
    "dtw": (r"$D(i,j) = (x_i - y_j)^2 + \min\{D(i-1,j),\ D(i,j-1),\ D(i-1,j-1)\}$",
            None),
    "abc-xyz": (r"$\mathrm{CV} = \frac{s}{\bar y}$", "Trung bình 100, s = 10 → CV = 0,1."),
    "biet-truoc": (r"$\mathrm{lag}_k(t) = y_{t-k}\ \ \mathrm{dùng\ được\ khi}\ \ k \geq h$",
                   "Dự báo trước 24 giờ thì lag nhỏ nhất là 24."),
    "feature-lich": (r"$\sin_i(t) = \sin\left(\frac{2\pi i\,t}{365{,}25}\right), \quad "
                     r"\cos_i(t) = \cos\left(\frac{2\pi i\,t}{365{,}25}\right), \quad i = 1, \dots, K$",
                     "Ngày 31/12 và 1/1 nằm cạnh nhau trên vòng tròn."),
    "cach-dien": (r"$\hat y_t = y_a + (y_b - y_a)\,\frac{t-a}{b-a}$",
                  "Tuyến tính nối 23 (giờ 2) với 27 (giờ 5): giờ 3 = 23 + 4 × 1/3 = 24,33."),
    "khu-nhieu": (r"$y_t = s_t + \varepsilon_t \qquad \mathrm{trailing}:\ \frac{1}{k}\sum_{j=0}^{k-1} y_{t-j} \qquad "
                  r"\mathrm{centered}:\ \frac{1}{k}\sum_{j=-(k-1)/2}^{(k-1)/2} y_{t+j}$",
                  "Centered có chỉ số j > 0, tức số của tương lai."),
    "ewma": (r"$z_t = \alpha\,y_t + (1-\alpha)\,z_{t-1}, \qquad \alpha = \frac{2}{\mathrm{span}+1}, \qquad "
             r"\mathrm{trễ\ MA}\ k\ \mathrm{điểm} = \frac{k-1}{2}$",
             "α = 0,2, z trước 50, số mới 100: z = 20 + 40 = 60."),
    "phan-du": (r"$R_t = y_t - \hat y_t\ \ (\mathrm{phần\ học}), \qquad e_{T+h} = y_{T+h} - \hat y_{T+h}\ \ (\mathrm{kỳ\ chấm})$",
                None),
    "chi-so": (r"$\mathrm{MAE} = \frac{1}{h}\sum_t |e_t|, \quad \mathrm{RMSE} = \sqrt{\frac{1}{h}\sum_t e_t^2}, \quad "
               r"\mathrm{ME} = \frac{1}{h}\sum_t e_t, \quad e_t = y_t - \hat y_t$", None),
    "phan-tram": (r"$\mathrm{MAPE} = \frac{100}{h}\sum_t \left|\frac{e_t}{y_t}\right|, \quad "
                  r"\mathrm{sMAPE} = \frac{200}{h}\sum_t \frac{|e_t|}{|y_t| + |\hat y_t|}, \quad "
                  r"\mathrm{WAPE} = 100\,\frac{\sum_t |e_t|}{\sum_t |y_t|}$", None),
    "mase": (r"$\mathrm{MASE} = \frac{\mathrm{MAE}}{\frac{1}{T-m}\sum_{t=m+1}^{T} |y_t - y_{t-m}|}, \qquad "
             r"\mathrm{RMSSE} = \sqrt{\frac{\frac{1}{h}\sum_t e_t^2}{\frac{1}{T-m}\sum_{t=m+1}^{T}(y_t - y_{t-m})^2}}$",
             "T điểm phần học, m là chu kỳ mùa vụ. Mẫu số chỉ lấy từ phần học."),
    "rolling-origin": (r"$c_{\mathrm{cuối}} = n - 1 - \mathrm{gap} - h, \qquad c_k = c_{\mathrm{cuối}} - \mathrm{bước} \times (K-k)$",
                       "30 mốc, h = 4, gap = 2: 30 − 1 − 2 − 4 = 23."),
    "dm": (r"$d_t = L(e_{1,t}) - L(e_{2,t}), \qquad \mathrm{DM} = \frac{\bar d}{\sqrt{\hat V(\bar d)}}$",
           "V̂ tính cả tự tương quan của d. Dự báo h bước: nhân hệ số hiệu chỉnh HLN."),
    # slide vấn đề
    "doi-nguoc": (r"$\mathrm{trung\ vị} = e^{\hat w}, \qquad \mathrm{trung\ bình} = e^{\hat w + \sigma^2/2} "
                  r"\approx e^{\hat w}\left(1 + \frac{\sigma^2}{2}\right)$", None),
    "durbin-watson": (r"$DW = \frac{\sum_{t=2}^{T}(e_t - e_{t-1})^2}{\sum_{t=1}^{T} e_t^2}$",
                      "Phần dư 1, −1, 1, −1, 1, −1: năm bước nhảy cỡ 2, DW = 5 × 4 / 6 ≈ 3,33."),
    "cdd-hdd": (r"$\mathrm{CDD} = \max(0,\ T - 18{,}33), \qquad \mathrm{HDD} = \max(0,\ 18{,}33 - T)$",
                "25 °C: CDD = 6,67, HDD = 0. Rồi hồi quy tải = a + b·CDD + c·HDD."),
    "spearman": (r"$r_S = r\left(\mathrm{hạng}(x),\ \mathrm{hạng}(y)\right)$",
                 "x = 1…5, y = 1, 4, 9, 16, 25: hai dãy hạng trùng nhau nên r_S = 1."),
    "mi": (r"$I(X;Y) = \sum_{x,y} p(x,y)\,\ln\frac{p(x,y)}{p(x)\,p(y)}$",
           "Ô (vừa, thấp): tỷ lệ thật 1/3 gấp 3 lần 1/9, góp 1/3 × ln 3 ≈ 0,366."),
    "hoan-vi-khoi": (r"$p = \frac{k+1}{B+1}$", "Xáo theo khối B lần; k là số lần MI của dữ liệu xáo lớn bằng hoặc hơn MI thật."),
    "z-score-masking": (r"$z_t = \frac{y_t - \bar y}{s}, \qquad |z_t| > 3\ \Rightarrow\ \mathrm{gắn\ cờ}$",
                        "(50 − 15,6) / 12,1 ≈ 2,84: không vượt 3."),
    "mad-hampel": (r"$\mathrm{điểm}_t = \frac{|y_t - \mathrm{median}(y)|}{1{,}4826 \cdot \mathrm{median}\,|y - \mathrm{median}(y)|}$",
                   "Điểm 50: |50 − 12| / (1,4826 × 1) ≈ 25,6."),
    "penalty": (r"$\min_{K,\ \tau_1 < \dots < \tau_K}\ \sum_{k=0}^{K} c\left(y_{\tau_k : \tau_{k+1}}\right) + \beta K$",
                "Tổng chi phí các đoạn, cộng β cho mỗi điểm gãy. β lớn thì ít điểm gãy."),
    "nyquist": (r"$f_{\mathrm{Nyquist}} = \frac{f_s}{2}, \qquad f_{\mathrm{giả}} = |f - k f_s|, \quad k = \mathrm{round}(f / f_s)$",
                "Sóng 4 bước, mẫu mỗi 3 bước: |1/4 − 1/3| = 1/12."),
    "he-so-lech": (r"$g = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{y_i - \bar y}{s}\right)^3$",
                   "Lập phương giữ dấu: số lệch +25 góp rất nhiều, số lệch −3 góp rất ít."),
    "phan-phoi-chuan": (r"$P(|y - \mu| \leq 1{,}96\,\sigma) = 0{,}95$", "1,96 là quantile 0,975 của phân phối chuẩn: mỗi đuôi 2,5%."),
    "hoan-vi": (r"$p = \frac{\mathrm{số\ cách\ chia\ có\ chênh} \geq 3}{C(6,\,3)} = \frac{2}{20} = 0{,}10$", None),
    "lag-plot": (r"$(y_{t-k},\ y_t)$", "Mỗi chấm là một cặp: giá trị k bước trước và giá trị bây giờ."),
    "truc-y-cat": (r"$\mathrm{độ\ cao} = \frac{\mathrm{giá\ trị} - \mathrm{đáy\ trục}}{\mathrm{đỉnh\ trục} - \mathrm{đáy\ trục}}$",
                   "(510 − 480) / (520 − 480) = 75%; (490 − 480) / 40 = 25%."),
    "guerrero": (r"$\mathrm{tỷ\ số}_j = \frac{s_j}{\mu_j^{\,1-\lambda}}, \qquad \lambda = \arg\min\ \mathrm{CV}(\mathrm{tỷ\ số})$",
                 "λ = 0,5, năm μ = 400, s = 20: 20 / √400 = 1."),
    "ljung-box-q": (r"$Q^* = T(T+2)\sum_{k=1}^{\ell} \frac{r_k^2}{T-k} \quad \mathrm{so\ với\ ngưỡng}\ \ \chi^2_{\ell - p}$",
                    "ℓ trễ, p tham số mô hình: 10 trễ, 2 tham số thì 8 bậc tự do."),
    "random-walk": (r"$y_t = y_{t-1} + \varepsilon_t, \qquad \mathrm{độ\ lệch\ chuẩn\ sau}\ n\ \mathrm{bước} \propto \sqrt{n}$",
                    "25 bước: √25 = 5 lần độ lệch chuẩn của một bước."),
}

# Công thức ở cột phải slide code: mã slide code → mã trong CONG_THUC, hoặc chuỗi mathtext riêng (ngắn, vì cột hẹp).
CT_CODE = {
    "code-b01-baseline": r"$\mathrm{MAE} = \frac{1}{n}\sum_{t=1}^{n} |y_t - \hat y_t|$",
    "code-b01-newsvendor": r"$p^* = \frac{C_u}{C_u + C_o}$",
    "code-b02-quantile": r"$q_p = \min\{\,y : F(y) \geq p\,\}$",
    "code-b02-pinball": r"$L_\tau = \tau\,(y-c)\ \ \mathrm{hoặc}\ \ (1-\tau)(c-y)$",
    "code-b02-ty-le-phu": r"$\bar y \pm 1{,}96\,s$",
    "code-b02-hoan-vi": "kiem-dinh",
    "code-b02-block-bootstrap": "bootstrap",
    "code-b02-tuong-quan": "scatter",
    "code-b03-resample": "resample",
    "code-b04-acf": "acf",
    "code-b07-acf": "acf",
    "code-b04-lam-tron-log": r"$\tilde y_t = \frac{1}{w}\sum_{j=-k}^{k} y_{t+j}, \quad \log_{10} y$",
    "code-b05-lich": r"$y_t\ /\ \mathrm{số\ ngày}$",
    "code-b05-gia-thuc": r"$x_t = \frac{y_t}{z_t} \times z_{\mathrm{gốc}}$",
    "code-b05-log": r"$\log(1{,}2\,y) - \log y = 0{,}182$",
    "code-b05-guerrero": r"$w_t = \frac{y_t^{\lambda} - 1}{\lambda}$",
    "code-b05-doi-nguoc": r"$e^{\hat w}\left(1 + \frac{\sigma^2}{2}\right)$",
    "code-b06-co-dien": r"$y_t = T_t + S_t + R_t$",
    "code-b06-do-manh": "f-s",
    "code-b06-robust": r"$\rho = (1-u^2)^2, \quad u = \frac{|R|}{6\,\mathrm{median}(|R|)}$",
    "code-b07-pacf": "pacf",
    "code-b07-ljung-box": "ljung-box",
    "code-b07-random-walk": r"$y_t = y_{t-1} + \varepsilon_t$",
    "code-b07-sai-phan": "sai-phan-la-gi",
    "code-b08-tuong-quan-gia": "durbin-watson",
    "code-b08-cdd-mi": r"$\mathrm{CDD} = \max(0,\ T - 18{,}33)$",
    "code-b08-tuong-quan-truot": "truot",
    "code-b09-entropy": "entropy",
    "code-b09-smape-mase": "do-kho",
    "code-b09-abc-xyz": "abc-xyz",
    "code-b10-dien": "cach-dien",
    "code-b11-masking": r"$z_t = \frac{y_t - \bar y}{s}$",
    "code-b11-hampel": r"$\frac{|y_t - \mathrm{median}|}{1{,}4826\cdot\mathrm{MAD}}$",
    "code-b12-aliasing": r"$f_{\mathrm{giả}} = |f - k f_s|$",
    "code-b12-bo-loc": r"$z_t = \alpha\,y_t + (1-\alpha)\,z_{t-1}$",
    "code-b12-trailing": r"$\frac{1}{k}\sum_{j=0}^{k-1} y_{t-j}$",
    "code-b13-lich": r"$\sin\left(\frac{2\pi i\,t}{365{,}25}\right),\ \cos\left(\frac{2\pi i\,t}{365{,}25}\right)$",
    "code-b14-mae-rmse": r"$\mathrm{RMSE} = \sqrt{\frac{1}{h}\sum_t e_t^2}$",
    "code-b14-phan-tram": r"$\mathrm{WAPE} = 100\,\frac{\sum_t |e_t|}{\sum_t |y_t|}$",
    "code-b14-mase": r"$\mathrm{MASE} = \frac{\mathrm{MAE}}{\frac{1}{T-m}\sum |y_t - y_{t-m}|}$",
    "code-b15-rolling-origin": r"$c_{\mathrm{cuối}} = n - 1 - \mathrm{gap} - h$",
    "code-b15-dm": r"$\mathrm{DM} = \frac{\bar d}{\sqrt{\hat V(\bar d)}}$",
}

# Câu "Vấn đề" đặt trên dòng Mục tiêu: một câu hỏi cụ thể mà khái niệm trả lời, rút từ "**Vấn đề.**" của tai-lieu.md.
# Chỉ thêm khi câu hỏi ngắn, có số hoặc tình huống thật, và không dùng từ chưa dạy. Bỏ khi nó lặp tiêu đề/Mục tiêu,
# khi phải nhắc "code đầu buổi" hay "mục 4.x", và ở slide vấn đề (đã có Dấu hiệu) hay slide code.
VAN_DE = {
    "du-bao-la-gi": "Con số ta sắp đưa ra là điều sẽ xảy ra, hay điều ta muốn xảy ra?",
    "sai-so-ao": "Khớp mô hình trên cả năm 2010 rồi chấm trên chính năm 2010, được MAE 0,380. Tin được không?",
    "do-chi-tiet": "Trung bình 4 tuần thắng khi chấm theo giờ. Nếu công ty mua điện một khối cho cả tuần thì sao?",
    "newsvendor": "Mua thiếu mỗi kWh mất 4 đồng, mua thừa mất 1 đồng. Mỗi giờ nên mua bao nhiêu?",
    "phan-phoi": "17h mai có bao nhiêu lượt thuê? Không ai biết chắc: dưới 100 thì hiếm, quanh 400 hay gặp.",
    "con-so-bao": "Chỉ được báo một con số: trung bình, trung vị hay quantile?",
    "khoang": "Báo “17h mai có 65 tới 604 lượt, khả năng 95%”. 95% đó có thật là 95% không?",
    "khoang-tin-cay": "Trung bình năm 2012 là 234,7 lượt/giờ. Một năm “giống hệt” thì con số này lệch bao nhiêu?",
    "kiem-dinh": "Ngày làm việc năm 2012 đông hơn ngày nghỉ 456 lượt. Khác biệt thật, hay do may?",
    "utc": "Taxi ghi giờ theo đồng hồ New York, thời tiết ghi theo UTC. Ghép hai bảng thế nào cho khớp giờ?",
    "resample": "Chuyến taxi rơi vào giây bất kỳ, mô hình cần mỗi giờ một số. Chuyến đúng 10:00 thuộc giờ nào?",
    "lam-tron": "Làm trơn cho hình dễ nhìn. Nhưng nó giấu mất gì?",
    "thang-log": "Tháng tăng mạnh nhất là tháng thêm nhiều lượt nhất, hay tháng tăng nhiều phần trăm nhất?",
    "boxplot": "Giờ nào khó đoán nhất: hôm thì đông, hôm thì vắng?",
    "acf": "Dự báo giờ tới nên dựa vào giờ trước, cùng giờ hôm qua, hay cùng giờ tuần trước?",
    "dieu-chinh": "Doanh số tháng 3 cao hơn tháng 2: vì người ta mua nhiều hơn, hay chỉ vì tháng 3 dài hơn 3 ngày?",
    "log": "Năm bán càng nhiều, tháng đông với tháng vắng càng chênh xa. Mà mô hình lại muốn dao động đều.",
    "box-cox": "Để nguyên thì dao động phình theo mức; lấy log thì ép quá tay. Chọn nấc ở giữa bằng số thế nào?",
    "phan-ra": "Tải điện đổi vì mức chung theo mùa, nhịp ngày và tuần, và những thứ bất ngờ. Tách ra thế nào?",
    "phan-ra-cach": "Nhịp ngày của tải điện tháng 7 khác hẳn tháng 1. Phân rã có cho mùa vụ đổi theo không?",
    "robust": "Một giờ báo 56.260 MW giữa hai giờ khoảng 95.000 MW. Lỗi đó có kéo méo cả mùa vụ không?",
    "ljung-box": "Dự báo xong, phần sai số còn sót quy luật nào không?",
    "dung": "Mức và độ dao động của chuỗi có giữ nguyên không? Nếu không, học quá khứ khó dùng cho mai sau.",
    "he-so-lech": "Trung bình 11 mà trung vị chỉ 8. Số liệu lệch về phía nào, lệch cỡ nào?",
    "phan-phoi-chuan": "Khoảng 95% lấy ±1,96 s. Con số 1,96 ở đâu ra, và dữ liệu lệch phải thì sao?",
    "hoan-vi": "Ngày làm việc hơn ngày nghỉ 456 lượt. Làm sao tính p-value mà không cần công thức?",
    "seasonal-subseries": "Nhìn đường theo thời gian khó thấy mùa vụ. Xếp lại theo thứ, theo tháng thì thấy gì?",
    "lag-plot": "Giờ trước, cùng giờ hôm qua hay cùng giờ tuần trước: cái nào giống giờ này nhất?",
    "truc-y-cat": "Doanh thu chỉ tăng 4,1% mà cột sau trông cao gấp ba. Vì sao?",
    "tron-nam": "Mỗi năm r trên 0,7, gộp hai năm lại chỉ còn 0,627. Quan hệ yếu đi thật sao?",
    "guerrero": "Log ép quá tay, để nguyên thì dao động phình ra. Chọn λ ở giữa bằng cách nào?",
    "exp-trung-vi": "Dự báo trên thang log rồi exp về: vì sao cộng lại thì hụt so với tổng thật?",
    "ty-le-mau-hinh": "Phân rã xong, phần dư trông lộn xộn. Nó đã hết nhịp theo giờ, theo tháng chưa?",
    "stl-loess": "Mùa vụ lớn dần qua các năm. Một khuôn mùa vụ cố định sẽ bỏ sót điều gì?",
    "ljung-box-q": "Q* = 5,16 là lớn hay nhỏ? Phải so với ngưỡng nào?",
    "random-walk": "Số liệu tăng vài tháng liền: có xu hướng thật, hay chỉ là các bước ngẫu nhiên cộng dồn?",
    "entropy": "Chuỗi này có nhịp đều để khai thác, hay gần như ngẫu nhiên?",
    "do-phan-giai": "Nhiệt độ ghi đúng 26,0 °C suốt nhiều giờ: cảm biến hỏng, hay trời đổi quá ít?",
    "dien-nhan-qua": "Điền xong thì backtest đẹp hẳn. Cách điền có dùng số của tập kiểm không?",
    "z-score-masking": "Mười số quanh 12 có một số 50. Vì sao ngưỡng 3σ không gắn cờ nó?",
    "mad-hampel": "Lượt xem tăng suốt mười năm. So mỗi ngày với trung bình cả chuỗi còn có nghĩa không?",
    "xu-ly-bat-thuong": "Điểm 90 bị gắn cờ giữa các số quanh 12: xoá, kéo về 12, hay giữ nguyên?",
    "penalty": "Mức đổi đột ngột mà từng điểm riêng lẻ trông vẫn bình thường. Tìm mốc đổi thế nào?",
    "nyquist": "Hạ dữ liệu 10 phút xuống 1 giờ thì hiện ra một chu kỳ 2,5 giờ. Nó từ đâu ra?",
    "sau-ho-loc": "Sáu họ bộ lọc, mười cấu hình. Cái nào dùng được làm feature dự báo?",
    "kiem-nhan-qua": "Tài liệu thư viện không nói bộ lọc có dùng số của giờ sau không. Kiểm thế nào?",
    "ca-chuoi": "Chuẩn hoá cả tập dữ liệu rồi mới chia học và kiểm. Tương lai lọt vào ở đâu?",
    "kiem-ro-ri": "41 feature, không ai đọc hết từng dòng code. Máy kiểm rò rỉ giúp được không?",
    "ex-ante": "Tối nay dự báo tải điện trưa mai. Nhiệt độ trưa mai trong tay ta là số nào?",
    "mape-lech": "Cùng lệch 50 đơn vị, vì sao dự báo cao bị MAPE phạt nặng hơn dự báo thấp?",
    "spearman": "y luôn tăng khi x tăng, nhưng theo đường cong. Pearson có thấy quan hệ đó là hoàn hảo không?",
    "durbin-watson": "CPI và dân số Mỹ có R² = 0,95 và t = 88,6. Hai thứ đó liên quan mạnh tới vậy thật sao?",
    "cdd-hdd": "Lạnh bật sưởi, nóng bật điều hoà. Một đường thẳng theo nhiệt độ có tả được tải điện không?",
    "mi": "Pearson giữa nhiệt độ và tải là 0,616. Con số nào đo được cả nhánh lạnh lẫn nhánh nóng?",
    "hoan-vi-khoi": "MI giữa nhiệt độ và tải là 0,862 nat. Lớn thật, hay hai chuỗi trơn nào cũng cho con số cỡ đó?",
    "ccf": "Nhiệt độ tăng thì bao lâu sau tải điện mới tăng?",
    "truot": "Quan hệ giữa nhiệt độ và tải điện có giữ nguyên suốt năm không?",
    "granger": "Nhiệt độ có “gây ra” tải điện không?",
    "dac-trung": "48.000 chuỗi thì không ai xem từng hình. Chuỗi nào khó, chuỗi nào giống nhau?",
    "pho": "Trước khi lọc, cần biết chuỗi có những nhịp nào: nhịp nào phải giữ, phần nào là nhiễu?",
    "ban-do-pca": "15 đặc trưng là 15 chiều, không vẽ được. Làm sao thấy cả 4.000 chuỗi trên một hình?",
    "dtw": "Hai chuỗi cùng hình dạng có thể lệch nhau một hai bước và khác hẳn độ lớn. Gom chúng thế nào?",
    "abc-xyz": "Hàng nghìn mã hàng mà ít người. Dồn công sức vào mã nào?",
    "biet-truoc": "Lúc học, mọi con số đều đã có. Lúc dự báo thật thì chưa. Cột nào thật sự có trong tay lúc đó?",
    "khu-nhieu": "Đường làm trơn đẹp nhất thường mượn số của giờ sau. Dùng nó để dự báo được không?",
    "mase": "Chuỗi này MAE 98, chuỗi kia MAE 3: không so được. Đổi ra phần trăm thì gặp số 0 là hỏng.",
    "rolling-origin": "Cắt một lần thì có thể chỉ là may. Làm sao kiểm nhiều lần mà lần nào cũng chỉ học quá khứ?",
    "ba-doan": "Chọn cấu hình tốt nhất trên một đoạn, rồi báo sai số cũng trên đoạn đó. Tin được không?",
    "dm": "Mô hình “trộn” có MAE thấp hơn seasonal naive 4,3% trên 92 ngày. Chênh thật, hay may?",
}

# Mục tiêu của slide tự dựng (không theo khuôn khái niệm).
MUC_TIEU = {
    "mo-hinh": "Hiểu mô hình “học” từ đâu và được chấm ở đâu, để thấy vì sao chấm trên phần học cho con số đẹp hơn thật.",
    "bon-baseline": "Tính được tay bốn cách dự báo đơn giản nhất, vì mọi mô hình trong khoá đều phải thắng chúng.",
    "prewhitening": "Tìm đúng độ trễ giữa hai chuỗi, không nhầm nhịp riêng của từng chuỗi thành quan hệ giữa hai chuỗi.",
    "du-bao-cuon": "Đo sai số đúng như lúc dự báo thật, không đo trên dữ liệu mô hình đã thấy.",
    "du-bao-la-gi": "Giữ dự báo trung thực, và biết trước một thứ dự báo được tới đâu.",
    "thu-vien": "Biết mỗi thư viện là gì và lo phần nào, trước khi đọc code của từng buổi.",
    "ly-thuyet-ham": "Tra nhanh: lý thuyết này làm bằng hàm nào, của thư viện nào.",
    "phieu-6-o": "Biết dự báo phục vụ quyết định nào, rồi mới biết dự báo gì, xa bao nhiêu, chấm ra sao.",
    "dang-dai": "Mọi chuỗi cùng một khuôn, để mọi công cụ ở các buổi sau nhận vào được.",
    "bo-bieu-do": "Không kết luận từ một hình: mỗi hình kiểm một giả thuyết khác nhau.",
    "shift-rolling": "Tạo feature từ quá khứ mà không vô tình chứa chính ngày đang cần dự báo.",
    "adf-kpss-la-gi": "Có một con số để quyết định chuỗi có thành phần random walk không, tức có cần sai phân không.",
    "adf-kpss": "Ghép kết luận của hai kiểm định để quyết định có sai phân hay không.",
    "ma-tran": "Thấy cùng một lỗi quay lại ở nhiều buổi, dưới những dạng khác nhau.",
    "quy-trinh": "Biết bước nào làm một lần, bước nào phải làm lại ở mỗi cutoff để khỏi rò rỉ.",
}

# Slide vấn đề: hậu quả nếu bỏ qua.
HAU_QUA = {
    "mui-gio": "có giờ 0 chuyến giả, và ghép thời tiết lệch giờ làm quan hệ sai hẳn.",
    "gop": "kết luận nhầm “không có mùa vụ tuần”; giờ thiếu thành 0 kéo tổng xuống.",
    "bieu-do-sai": "đọc ra quan hệ không có thật, hoặc phóng to một chênh lệch nhỏ.",
    "dao-dong": "tưởng tăng trưởng thật trong khi chỉ là giá và dân số tăng.",
    "doi-nguoc": "cộng dự báo nhiều cửa hàng ra tổng thấp hơn thật.",
    "chu-ky-sai": "nhịp tuần lẫn vào xu hướng, mùa vụ ngày bị ép giống nhau cả năm.",
    "sai-phan": "chuỗi đã dừng mà sai phân thêm thì nhiễu to ra, dự báo tệ hơn.",
    "tuong-quan-gia": "chọn một biến giải thích vô dụng vì tưởng nó liên quan.",
    "chu-u": "dùng một đường thẳng cho nhiệt độ thì bỏ sót hẳn nhánh trời lạnh.",
    "thieu-moc": "chuỗi trông đủ nhưng thiếu cả dòng; lag và rolling tính sai số bước.",
    "mnar": "điền xong trung bình vẫn lệch, và dự báo lệch theo.",
    "tra-hinh": "mô hình học trên 35% số dòng là số quy ước, không phải số đo.",
    "so-sanh-dien": "chọn cách điền giỏi ở lỗ ngắn nhưng tệ ở lỗ dài.",
    "dien": "có đoạn phẳng giả, và tương lai rò vào dữ liệu học.",
    "masking": "ngoại lai thật lọt qua, trong khi báo cáo nói “dữ liệu sạch”.",
    "hampel": "chỉ gắn cờ những ngày đông, bỏ sót bất thường ở vùng mức thấp.",
    "tet": "xoá mất đỉnh Tết, thứ đáng dự báo nhất trong năm.",
    "pelt": "hàng chục điểm gãy giả, chuỗi bị cắt vụn vô nghĩa.",
    "covid": "sai số chênh gần 3 lần tuỳ cách xử lý mà không ai biết.",
    "aliasing": "thấy một chu kỳ không có thật, rồi dựng feature theo nhịp giả.",
    "bo-loc": "chọn bộ lọc “tốt nhất” mà không dùng được lúc dự báo.",
    "loc-tuong-lai": "backtest đẹp, dùng thật thì mất sạch phần cải thiện.",
    "muc-tieu-lam-tron": "báo sai số đẹp giả, và giấu đúng những đỉnh nhọn mô hình sai nhiều nhất.",
    "ro-ri": "backtest đẹp, dùng thật tệ, mà không có lỗi nào báo.",
    "ngoai-sinh": "mô hình tin nhiệt độ quá mức, chạy thật còn tệ hơn không dùng.",
    "chia-ngau-nhien": "sai số kiểm hứa thấp hơn thật, chọn nhầm mô hình giỏi “học thuộc”.",
}


# Từ nền: những từ các slide dùng mà không có slide riêng. Mỗi dòng: (từ, là gì, ví dụ). Nguồn: bảng "Từ mới" từng buổi.
TU_NEN = [
    ("Từ nền 1/5: dự báo, sai số, dữ liệu", [
        ("mô hình, tham số", "Cách tính ra dự báo; tham số là các con số bên trong nó", "“Mai = trung bình 7 ngày qua”"),
        ("khớp (fit), học", "Chọn các tham số từ dữ liệu quá khứ", "Tính trung bình 7 ngày từ lịch sử"),
        ("phần học / kỳ chấm", "Đoạn dùng để khớp / đoạn giữ riêng để chấm", "Học 2009, chấm 2010"),
        ("học thuộc (overfit)", "Khớp quá sát phần học, dự báo mới thì tệ", "Thuộc đề cũ: 10 điểm; đề mới: 6"),
        ("sai số dự báo", "Thực tế − dự báo; dương là dự báo thấp", "1,7 − 1,5 = +0,2"),
        ("MAE", "Trung bình độ lớn sai số, bỏ dấu", "Sai số +2 và −4 → 3"),
        ("RMSE", "Căn của trung bình sai số bình phương; phạt nặng sai số lớn", "Sai số 1 và −3 → 2,24"),
        ("MAPE", "Trung bình |sai số| chia thực tế, tính bằng %", "Thật 100, dự báo 90 → 10%"),
        ("NaN", "Ô “không biết” của pandas, khác với số 0", "Không đo lúc 01:00 → NaN"),
        ("backtest", "Đứng ở nhiều mốc trong quá khứ, dự báo, rồi so với thực tế", "4 thứ Hai, mỗi lần dự báo 24 giờ"),
        ("feature / mục tiêu", "Cột đầu vào mô hình dùng / con số cần dự báo", "Điện 2 giờ qua / điện giờ tới"),
        ("lag, rolling", "Giá trị k bước trước; thống kê trên w điểm gần nhất", "lag_7 thứ Hai = thứ Hai tuần trước"),
        ("trung bình trượt", "Thay mỗi điểm bằng trung bình với các điểm lân cận", "50, 2, 51 → quanh 2 là 34,3"),
    ]),
    ("Từ nền 2/5: thống kê", [
        ("mẫu / tổng thể", "Số liệu đang có / mọi giá trị nếu đo mãi", "9 giờ 17h đang có / mọi giờ 17h"),
        ("phân phối chuẩn", "Hình chuông đối xứng; 95% nằm trong trung bình ± 1,96 s", "100 ± 1,96 × 10 → 80,4–119,6"),
        ("histogram", "Cột đếm số giá trị rơi vào mỗi khoảng", "0–9: 6 số; 10–19: 2 số"),
        ("i.i.d.", "Các lần độc lập và cùng phân phối", "Các lần tung một xúc xắc"),
        ("mức ý nghĩa α", "Ngưỡng chọn trước; p nhỏ hơn thì bác bỏ H0", "Hay dùng 0,05"),
        ("sai số chuẩn", "Độ lệch chuẩn của chính một con số ước lượng", "Trung bình 25 giờ: 181 / √25 ≈ 36"),
        ("tương quan r", "Số từ −1 tới 1: hai biến cùng tăng giảm theo đường thẳng tới đâu", "1, 2, 3 và 2, 4, 6 → r = 1"),
        ("r₁, r_k", "Tự tương quan ở trễ 1, ở trễ k", "r₂₄ = 0,81 với lượt thuê xe"),
        ("hồi quy đơn, R²", "Đường y = a + b·x khớp nhất; R² là phần dao động nó giải thích", "R² = 0,8: giải thích 80%"),
        ("Durbin–Watson", "Đo phần dư hồi quy có tự tương quan: gần 2 là không, gần 0 là mạnh", "Gần 0 → nghi tương quan giả"),
        ("mutual information", "Biết x thì bớt được bao nhiêu điều chưa biết về y; bắt cả quan hệ cong", "Bằng 0 khi độc lập"),
        ("CV", "Độ lệch chuẩn chia trung bình", "Trung bình 100, s = 10 → 0,1"),
        ("Jarque–Bera", "Kiểm định số liệu có gần hình chuông không; p nhỏ là không", "Phần dư có vài cú rơi lớn"),
    ]),
    ("Từ nền 3/5: biến đổi, dừng, bất thường", [
        ("log, exp", "log y: e mũ mấy thì bằng y; exp làm ngược lại", "log 100 = 4,605"),
        ("CPI, năm gốc", "Chỉ số giá một giỏ hàng; năm lấy làm mốc sức mua", "CPI 100 → 125: giá tăng 25%"),
        ("điều chỉnh lịch", "Chia tổng tháng cho số ngày để tháng dài ngắn so được", "280 tỷ / 28 ngày = 10 tỷ/ngày"),
        ("log-normal", "y = exp(w) với w hình chuông: luôn dương, lệch phải", "Doanh số, giá nhà"),
        ("Yeo-Johnson", "Biến thể Box-Cox nhận cả số 0 và số âm", "Chuỗi % tăng trưởng có tháng âm"),
        ("nhiễu trắng", "Không tự tương quan ở trễ nào: quá khứ không giúp đoán", "Kết quả tung xúc xắc"),
        ("random walk", "Giá trị mới = giá trị cũ + một bước ngẫu nhiên", "Tung đồng xu rồi bước tới, lùi"),
        ("khử xu hướng", "Lấy chuỗi trừ đường xu hướng", "30 − 24,5 = 5,5"),
        ("LOESS", "Làm trơn cục bộ: mỗi điểm nhìn lân cận, điểm gần nặng hơn", "Lõi của STL"),
        ("robust", "Cách ước lượng ít bị vài điểm bất thường kéo lệch", "robust=True trong STL"),
        ("biến giả", "Cột 0/1 báo mốc nào thuộc một sự kiện", "covid = 1 từ 3/2020 tới 6/2021"),
        ("winsorize", "Kéo giá trị bị gắn cờ về mức hợp lý (trung vị địa phương), không xoá", "50 → 12"),
        ("MAD", "Trung vị của khoảng cách tới trung vị", "Ngoại lai không kéo được"),
    ]),
    ("Từ nền 4/5: tần số và bộ lọc", [
        ("bộ lọc", "Phép biến một chuỗi thành chuỗi khác, thường để làm trơn", "Trung bình trượt 3 điểm"),
        ("trailing / centered", "Chỉ nhìn các điểm trước / lấy cả trước lẫn sau", "Centered dùng số tương lai"),
        ("trễ (pha)", "Đầu ra bộ lọc chạy sau tín hiệu thật bao nhiêu bước", "Trung bình 13 điểm trễ 6 bước"),
        ("tần số lấy mẫu f_s", "Số mẫu mỗi đơn vị thời gian", "10 phút một mẫu: 6 mẫu/giờ"),
        ("tần số Nyquist", "Tần số cao nhất còn thấy đúng: f_s / 2", "6 mẫu/giờ → 3 vòng/giờ"),
        ("hạ mẫu", "Giảm tần số lấy mẫu", "Từ 10 phút sang 1 giờ"),
        ("lọc thông thấp", "Giữ dao động chậm, bỏ dao động nhanh", "Lọc trước khi hạ mẫu"),
        ("EWMA", "Trung bình trượt hàm mũ: điểm mới nặng hơn điểm cũ", "z_t = α·y_t + (1 − α)·z_(t−1)"),
        ("Savitzky–Golay", "Khớp đa thức bậc thấp quanh mỗi điểm", "Nhìn cả hai phía: không nhân quả"),
        ("Butterworth", "Bộ lọc cắt tần số theo một ngưỡng", "Bản nhân quả trễ 19 bước"),
        ("Kalman filter / smoother", "Ước lượng tín hiệu ẩn; filter dùng quá khứ, smoother dùng cả chuỗi", "Smoother không nhân quả"),
        ("sosfilt / sosfiltfilt", "Chạy bộ lọc xuôi thời gian / xuôi rồi ngược", "sosfiltfilt nhìn tương lai"),
        ("tín hiệu / nhiễu", "Phần có quy luật cần giữ / phần ngẫu nhiên", "Nhịp ngày / bật tắt ấm đun"),
    ]),
    ("Từ nền 5/5: làm sạch, feature, đánh giá", [
        ("ép kiểu số", "Đổi cột đọc thành chữ về số (to_numeric)", "“12,5” → 12.5; “(S)” → NaN"),
        ("nội suy tuyến tính, ffill", "Nối thẳng hai điểm hai bên lỗ / chép giá trị trước đó", "10, ?, 14 → 12 / 10"),
        ("cờ chất lượng", "Mã nguồn gắn kèm số đo: qua kiểm tra hay đáng ngờ", "GHCNh: mã 2 = đáng ngờ"),
        ("độ phân giải", "Bước nhỏ nhất giữa hai giá trị cảm biến ghi được", "Nhiệt độ số nguyên: 1 °C"),
        ("cảm biến kẹt", "Cảm biến ghi lặp một giá trị nhiều giờ liền", "26,0 suốt 33 giờ"),
        ("scaler", "Trừ trung bình, chia độ lệch chuẩn cho từng cột (StandardScaler)", "Phải fit trên phần học"),
        ("target encoding", "Thay một nhóm bằng trung bình mục tiêu của nhóm", "Thứ Bảy → doanh thu TB các thứ Bảy"),
        ("biến ngoại sinh", "Biến ngoài chuỗi, dùng làm feature", "Nhiệt độ khi dự báo tải điện"),
        ("ex-ante / ex-post", "Chỉ dùng thông tin có lúc dự báo / dùng cả số thật về sau", "Nhiệt độ dự báo / nhiệt độ đo"),
        ("point-in-time", "Dùng số liệu đúng như lúc đó, không dùng bản đã sửa về sau", "GDP bản công bố đầu tiên"),
        ("hold-out", "Đoạn tương lai giữ riêng, chỉ chấm một lần", "Quý 4 năm 2024"),
        ("tune", "Thử nhiều cách đặt tham số, giữ cách sai ít nhất", "Thử 11 giá trị w"),
        ("rừng ngẫu nhiên", "Nhiều cây quy tắc “nếu… thì…”, lấy trung bình; rất giỏi nhớ", "200 cây"),
    ]),
]


# ---------- tiện ích vẽ ----------

def rgb(h: str) -> RGBColor:
    return RGBColor.from_string(h)


def nen(slide, mau: str) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(mau)


# Arial đậm không có chữ số chỉ số dưới (₁, ₂₄…): đổi về chữ số thường để khỏi lỗi font.
_CHI_SO_DUOI = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def _runs(p, runs, nghieng=False):
    for text, c, b, m in runs:
        r = p.add_run()
        r.text = text.translate(_CHI_SO_DUOI)
        r.font.size = Pt(c)
        r.font.bold = b
        r.font.italic = nghieng
        r.font.name = FONT
        r.font.color.rgb = rgb(m)


def chu(slide, x, y, w, h, noi_dung, co=18, dam=False, mau=INK, can=PP_ALIGN.LEFT, doc=MSO_ANCHOR.TOP,
        nghieng=False, cach_dong=None):
    """noi_dung: str, hoặc list đoạn; mỗi đoạn là str hoặc list (text, cỡ, đậm, màu)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = doc
    doan = noi_dung if isinstance(noi_dung, list) else [noi_dung]
    for i, d in enumerate(doan):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = can
        if cach_dong:
            p.space_after = Pt(cach_dong)
        _runs(p, d if isinstance(d, list) else [(d, co, dam, mau)], nghieng)
    return tb


def hinh_khoi(slide, kieu, x, y, w, h, nen_mau=None, vien=None, dash=False, bo_goc=0.12):
    s = slide.shapes.add_shape(kieu, Inches(x), Inches(y), Inches(w), Inches(h))
    if kieu == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = bo_goc
    if nen_mau:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(nen_mau)
    else:
        s.fill.background()
    if vien:
        s.line.color.rgb = rgb(vien)
        s.line.width = Pt(1.25)
        if dash:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def chu_trong(s, noi_dung, co=16, dam=False, mau=INK, can=PP_ALIGN.CENTER, le=0.08):
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(le)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    doan = noi_dung if isinstance(noi_dung, list) else [noi_dung]
    for i, d in enumerate(doan):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = can
        _runs(p, d if isinstance(d, list) else [(d, co, dam, mau)])


def noi(slide, x1, y1, x2, y2, mau=VIEN, day=1.5, mui_ten=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(mau)
    c.line.width = Pt(day)
    if mui_ten:
        ln = c.line._get_or_add_ln()
        ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
    return c


def ti_le(b: int, ten: str) -> float:
    iw, ih = Image.open(GOC / f"buoi-{b:02d}" / "hinh" / f"{ten}.png").size
    return iw / ih


def anh(slide, b: int, ten: str, x, y, w, h, nhan: str | None = None):
    """Đặt hinh/<ten>.png của buổi b vừa khung, giữ tỉ lệ, căn giữa; nhãn nhỏ phía trên nếu có."""
    if nhan:
        chu(slide, x, y, w, 0.3, nhan, co=12, dam=True, mau=MUTED)
        y, h = y + 0.35, h - 0.35
    ti = ti_le(b, ten)
    if w / h > ti:
        hh, ww = h, h * ti
    else:
        ww, hh = w, w / ti
    xx, yy = x + (w - ww) / 2, y + (h - hh) / 2
    slide.shapes.add_picture(str(GOC / f"buoi-{b:02d}" / "hinh" / f"{ten}.png"),
                             Inches(xx), Inches(yy), Inches(ww), Inches(hh))


matplotlib.rcParams["mathtext.fontset"] = "dejavusans"
DPI_CT = 300


def anh_ct(tex: str, co: float = 20) -> Path:
    """Render một công thức mathtext ra PNG (nền trong suốt, cỡ chữ co pt), đặt tên theo nội dung."""
    ra = TAM / (hashlib.md5(f"{co}{tex}".encode()).hexdigest()[:12] + ".png")
    if not ra.exists():
        math_to_image(tex, ra, prop=FontProperties(size=co), dpi=DPI_CT, format="png", color="#" + INK)
        xam = Image.open(ra).convert("L")  # nền trắng → trong suốt, nét chữ giữ màu INK
        trong = Image.new("RGBA", xam.size, "#" + INK)
        trong.putalpha(xam.point(lambda v: 255 - v))
        trong.save(ra)
    return ra


def dat_ct(slide, tex: str, x, y, w, h, co: float = 20, can_giua=False) -> float:
    """Đặt công thức cỡ tự nhiên (co pt), thu nhỏ nếu vượt khung w × h; căn giữa theo chiều dọc. Trả bề rộng đã dùng."""
    p = anh_ct(tex, co)
    iw, ih = Image.open(p).size
    ww, hh = iw / DPI_CT, ih / DPI_CT
    k = min(1.0, w / ww, h / hh)
    if k < 0.7:
        print(f"  cảnh báo: công thức bị thu còn {k:.0%}: {tex[:60]}")
    ww, hh = ww * k, hh * k
    xx = x + (w - ww) / 2 if can_giua else x
    slide.shapes.add_picture(str(p), Inches(xx), Inches(y + (h - hh) / 2), Inches(ww), Inches(hh))
    return ww


def cao_ct(tex: str, co: float = 20) -> float:
    """Chiều cao tự nhiên (inch) của công thức ở cỡ co pt."""
    return Image.open(anh_ct(tex, co)).size[1] / DPI_CT


def dai_ct(slide, ma: str, y: float, mau: str, x=0.6, w=12.13, gon=False) -> float:
    """Dải công thức ngang (nhãn | công thức | nói bằng lời). Trả tung độ phía dưới dải (y cũ nếu slide không có công thức).
    gon=True (cột hẹp trên hình): chỉ công thức, căn giữa; câu nói bằng lời nằm ở ghi chú người nói."""
    if ma not in CONG_THUC:
        return y
    tex, loi = CONG_THUC[ma]
    cao = min(max(cao_ct(tex) + 0.14, 0.72), 1.02)
    hinh_khoi(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, cao, nen_mau=NHAT, bo_goc=0.15)
    if gon:
        dat_ct(slide, tex, x + 0.1, y + 0.06, w - 0.2, cao - 0.12, can_giua=True)
        return y + cao + 0.1
    chu(slide, x + 0.15, y, 1.2, cao, "Công thức", co=12, dam=True, mau=mau, doc=MSO_ANCHOR.MIDDLE)
    x_ct = x + 1.35
    rong = w - 1.5 - (3.4 if loi else 0)
    da_dung = dat_ct(slide, tex, x_ct, y + 0.06, rong, cao - 0.12)
    if loi:
        x_loi = x_ct + max(da_dung, rong * 0.55) + 0.2
        chu(slide, x_loi, y, x + w - x_loi - 0.15, cao, loi, co=11.5, mau=INK, doc=MSO_ANCHOR.MIDDLE)
    return y + cao + 0.1


def huy_hieu(slide, chu_cai: str, x=0.6, y=0.5, d=0.62):
    s = hinh_khoi(slide, MSO_SHAPE.OVAL, x, y, d, d, nen_mau=PHAN[chu_cai][1])
    chu_trong(s, chu_cai, co=20, dam=True, mau=TRANG)


def the(slide, x, y, w, h, nhan: str, noi_dung, mau: str, mau_nhat: str, co=16):
    hinh_khoi(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, nen_mau=mau_nhat, bo_goc=0.1)
    chu(slide, x + 0.25, y + 0.15, w - 0.5, 0.3, nhan, co=13, dam=True, mau=mau)
    chu(slide, x + 0.25, y + 0.45, w - 0.5, h - 0.5, noi_dung, co=co, mau=INK, cach_dong=3)


# ---------- khung slide ----------

def moi(prs, ma: str, tieu: str, phan: str, buoi: str | None = None, don_gian: str | None = None,
        dinh_nghia: tuple[str, str] | None = None):
    """Slide trắng có huy hiệu phần, tiêu đề nói kết luận, nhãn buổi, và câu 'hiểu đơn giản' (nếu có)."""
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    assert ma not in {m for m, _ in MUC}, f"trùng mã slide: {ma}"
    MUC.append((ma, tieu))
    PHAN_CUA[ma] = phan
    if len(tieu) > (48 if buoi else 58):
        print(f"  cảnh báo: tiêu đề dài ({len(tieu)} ký tự), dễ xuống dòng: {tieu}")
    nen(sl, TRANG)
    huy_hieu(sl, phan)
    chu(sl, 1.45, 0.42, 10.0 if buoi else 11.3, 0.8, tieu, co=30, dam=True, doc=MSO_ANCHOR.MIDDLE)
    if buoi:
        s = hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 11.45, 0.6, 1.3, 0.42, nen_mau=NHAT, bo_goc=0.5)
        chu_trong(s, buoi, co=12, dam=True, mau=PHAN[phan][1])
    y = 1.12
    if ma in EN:
        chu(sl, 1.45, y, 11.3, 0.3, EN[ma], co=13, mau=MUTED, nghieng=True)
        y += 0.36
    if ma in VAN_DE:
        chu(sl, 1.45, y, 11.3, 0.42, [[("Vấn đề:  ", 15, True, PHAN[phan][1]), (VAN_DE[ma], 16, False, INK)]])
        y += 0.4
    muc = dong_muc(ma)
    if muc:
        chu(sl, 1.45, y, 11.3, 0.42, [[(muc[0] + "  ", 15, True, INK), (muc[1], 16, False, INK)]])
        y += 0.4
    if dinh_nghia:
        chu(sl, 1.45, y, 11.3, 0.45, [[(dinh_nghia[0], 17, True, PHAN[phan][1]), (dinh_nghia[1], 17, False, INK)]])
    elif don_gian:
        cau = don_gian.replace("“", "‘").replace("”", "’")
        chu(sl, 1.45, y, 11.3, 0.45, f"“{cau[0].upper()}{cau[1:]}”", co=17, mau=PHAN[phan][1], nghieng=True)
    return sl


def dong_muc(ma: str) -> tuple[str, str] | None:
    """Dòng 'Mục tiêu' (khái niệm, slide tự dựng) hoặc 'Nếu bỏ qua' (vấn đề dữ liệu)."""
    if ma in KN:
        return "Mục tiêu:", KN[ma]["muc"]
    if ma in MUC_TIEU:
        return "Mục tiêu:", MUC_TIEU[ma]
    if ma in HAU_QUA:
        return "Nếu bỏ qua:", HAU_QUA[ma]
    return None


def dau_than(ma: str, don_gian) -> float:
    """Tung độ bắt đầu phần thân, sau dòng tiếng Anh, mục tiêu và câu 'hiểu đơn giản'."""
    return (1.5 + (0.36 if ma in EN else 0) + (0.4 if ma in VAN_DE else 0) + (0.4 if dong_muc(ma) else 0)
            + (0.42 if don_gian else 0))


def thang(sl, x, y, w, moc: list[tuple[str, str]], mau: str):
    """Thang đọc: một đường ngang, mỗi mốc một chấm, dưới là giá trị và nghĩa của nó (mỗi mốc một cột, không chồng)."""
    n = len(moc)
    cot = w / n
    noi(sl, x + cot / 2, y + 0.1, x + w - cot / 2, y + 0.1, mau=VIEN, day=3)
    for i, (gt, nghia) in enumerate(moc):
        cx = x + cot / 2 + i * cot
        hinh_khoi(sl, MSO_SHAPE.OVAL, cx - 0.09, y + 0.01, 0.18, 0.18, nen_mau=mau)
        co_gt = 14 if len(gt) <= 8 else 12
        chu(sl, x + i * cot + 0.04, y + 0.25, cot - 0.08, 0.3, gt, co=co_gt, dam=True, mau=mau, can=PP_ALIGN.CENTER)
        chu(sl, x + i * cot + 0.04, y + 0.55, cot - 0.08, 0.6, nghia, co=11, mau=INK, can=PP_ALIGN.CENTER)


def khai_niem(prs, ma, *_bo_qua, **_bo_qua_kw):
    """Khái niệm (nội dung KN[ma]): hình thật + ba thẻ Là gì / cao-thấp nghĩa là gì (thang) / Ví dụ."""
    d = KN[ma]
    phan = d["phan"]
    sl = moi(prs, ma, d["tieu"], phan, d["buoi"], d.get("dg"))
    mau = PHAN[phan][1]
    y0 = dau_than(ma, d.get("dg"))
    doc_tieu = d.get("doc_tieu", "Cao hay thấp nghĩa là gì" if d.get("thang") else "Đọc thế nào")
    khoi = [("Là gì", d["la_gi"]), (doc_tieu, d.get("doc", "")), ("Ví dụ", d["vi_du"])]
    if ti_le(*d["hinh"]) > 2.3:  # hình ngang: hình trên, ba thẻ dưới
        y0 = dai_ct(sl, ma, y0, mau)
        anh(sl, *d["hinh"], 0.6, y0, 12.13, 5.4 - y0)
        for i, (n, t) in enumerate(khoi):
            x = 0.6 + i * 4.11
            if i == 1 and d.get("thang"):
                the(sl, x, 5.5, 3.91, 1.6, n, "", mau, NHAT)
                thang(sl, x + 0.1, 5.95, 3.71, d["thang"], mau)
            else:
                the(sl, x, 5.5, 3.91, 1.6, n, t, mau, NHAT, co=14)
    else:  # hình gần vuông: hình trái, ba khối phải
        y_anh = dai_ct(sl, ma, y0, mau, w=6.9, gon=True)  # công thức trên hình, cột chữ giữ nguyên chiều cao
        anh(sl, *d["hinh"], 0.6, y_anh, 6.9, 7.1 - y_anh)
        cao = (7.1 - y0) / 3
        for i, (n, t) in enumerate(khoi):
            yy = y0 + i * cao
            chu(sl, 7.9, yy, 4.83, 0.3, n, co=14, dam=True, mau=mau)
            if i == 1 and d.get("thang"):
                thang(sl, 7.9, yy + 0.4, 4.83, d["thang"], mau)
            else:
                chu(sl, 7.9, yy + 0.35, 4.83, cao - 0.38, t, co=15)
    return sl


def van_de(prs, ma, *_bo_qua, **_bo_qua_kw):
    """Vấn đề dữ liệu (nội dung VD[ma]): hình thật; ba thẻ Dấu hiệu | Kiểm bằng | Cách sửa."""
    d = VD[ma]
    phan = d.get("phan", "B")
    sl = moi(prs, ma, d["tieu"], phan, d["buoi"], d.get("dg"), dinh_nghia=d.get("dn"))
    cac_hinh = d["hinh"]
    y0, y_the = dau_than(ma, d.get("dg") or d.get("dn")), 5.45
    the_van = [("Dấu hiệu", d["dau"], DO, DO_NHAT), ("Kiểm bằng", d["kiem"], LAM, LAM_NHAT),
               ("Cách sửa", d["sua"], XANH, XANH_NHAT)]
    if len(cac_hinh) == 1 and ti_le(*cac_hinh[0][:2]) < 2.1:  # hình gần vuông: hình trái, thẻ dọc phải
        y_anh = dai_ct(sl, ma, y0, PHAN[phan][1], w=7.4, gon=True)
        anh(sl, *cac_hinh[0][:2], 0.6, y_anh, 7.4, 7.05 - y_anh, *cac_hinh[0][2:])
        cao = (7.05 - y0 - 0.3) / 3
        for i, (n, t, m, mn) in enumerate(the_van):
            the(sl, 8.25, y0 + i * (cao + 0.15), 4.48, cao, n, t, m, mn, co=14)
        return sl
    y0 = dai_ct(sl, ma, y0, PHAN[phan][1])
    if len(cac_hinh) == 1:
        anh(sl, *cac_hinh[0][:2], 0.6, y0, 12.13, y_the - y0 - 0.15, *cac_hinh[0][2:])
    else:
        for i, h in enumerate(cac_hinh):
            anh(sl, *h[:2], 0.6 + i * 6.18, y0, 5.95, y_the - y0 - 0.15, *h[2:])
    for i, (n, t, m, mn) in enumerate(the_van):
        the(sl, 0.6 + i * 4.11, y_the, 3.91, 1.6, n, t, m, mn, co=14)
    return sl


MONO = "Courier New"


# Thư viện dùng trong các slide code, nói bằng lời thường.
THU_VIEN = {
    "pandas": "thư viện bảng dữ liệu: đọc, lọc, gộp, dời chuỗi theo thời gian",
    "numpy": "tính toán trên mảng số: cộng, trung bình, căn, ngẫu nhiên",
    "statsmodels": "thư viện thống kê: kiểm định, phân rã, mô hình chuỗi thời gian",
    "scipy": "tính toán khoa học: phân phối xác suất, bộ lọc tín hiệu",
    "sklearn": "scikit-learn, thư viện học máy: mô hình, chia tập, chuẩn hoá",
    "ruptures": "tìm điểm gãy trong chuỗi",
    "statsforecast": "thư viện dự báo của Nixtla: baseline, ETS, ARIMA chạy nhanh",
    "utilsforecast": "tiện ích của Nixtla: chỉ số sai số như MASE, RMSSE",
    "tu viet": "hàm tự viết trong buổi học",
}


def code_slide(prs, ma, tieu, phan, buoi, code: str, buoc: list[tuple[str, str]], ket_qua: str, nguon: str,
               ham: list[tuple[str, str, str]], hinh: tuple | None = None):
    """Slide code: code + từng bước (trái); thư viện và hàm, hình minh hoạ, kết quả (phải)."""
    assert ma not in EN, f"slide code {ma} không cần dòng tiếng Anh"
    sl = moi(prs, ma, tieu, phan, buoi)
    KHONG_DEM.add(len(prs.slides))
    mau = PHAN[phan][1]
    y0 = dau_than(ma, None)
    dong = code.strip("\n").splitlines()
    assert len(dong) <= 17, f"slide code {ma}: {len(dong)} dòng, tối đa 17"
    co = 10.5 if len(dong) <= 12 else 9.5 if len(dong) <= 15 else 8.5
    cao = min(max(2.2, (len(dong) + 1) * co / 72 * 1.18 + 0.35), 6.2 - y0 - 1.1)
    hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, y0, 7.75, cao, nen_mau="1E2433", bo_goc=0.03)
    tb = sl.shapes.add_textbox(Inches(0.75), Inches(y0 + 0.1), Inches(7.5), Inches(cao - 0.35))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, d in enumerate(dong):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        phan_code, _, chu_thich = d.partition("#")
        for text, m in ((f"{i + 1:>2} ", "6B7385"), (phan_code, "E6EAF0"), (("#" + chu_thich) if chu_thich else "", "8FC99A")):
            if not text:
                continue
            r = p.add_run()
            r.text = text
            r.font.name = MONO
            r.font.size = Pt(co)
            r.font.color.rgb = rgb(m)
    chu(sl, 0.75, y0 + cao - 0.27, 7.5, 0.22, nguon, co=8, mau="8A93A6", nghieng=True)
    # từng bước: dưới khối code
    yb = y0 + cao + 0.12
    chu(sl, 0.6, yb, 7.75, 0.3, "Từng bước", co=13, dam=True, mau=mau)
    n = len(buoc)
    hang = (n + 1) // 2
    kc = min(0.5, (6.35 - yb - 0.35) / max(hang, 1))
    if kc < 0.3:
        print(f"  cảnh báo: slide code {ma} chật, rút code hoặc bớt bước")
    for i, (ma_dong, giai) in enumerate(buoc):
        c, r = divmod(i, hang)
        x, yy = 0.6 + c * 3.95, yb + 0.35 + r * kc
        o = hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x, yy, 0.8, 0.26, nen_mau=NHAT, bo_goc=0.4)
        chu_trong(o, ma_dong.replace("dòng ", ""), co=9, dam=True, mau=mau, le=0.02)
        chu(sl, x + 0.88, yy - 0.02, 2.95, kc, giai, co=10.5)
    o = hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, 6.4, 7.75, 0.68, nen_mau=XANH_NHAT, bo_goc=0.15)
    chu(sl, 0.8, 6.43, 7.4, 0.62, [[("Kết quả:  ", 11, True, XANH), (ket_qua, 11, False, INK)]], doc=MSO_ANCHOR.MIDDLE)
    # cột phải: thư viện và hàm, rồi hình
    x = 8.6
    chu(sl, x, y0, 4.13, 0.3, "Thư viện và hàm", co=13, dam=True, mau=mau)
    yy = y0 + 0.36
    for ten_ham, tv, lam in ham:
        chu(sl, x, yy, 4.13, 0.26, [[(ten_ham, 11, True, INK), (f"   {tv}", 9.5, True, MUTED)]])
        chu(sl, x, yy + 0.25, 4.13, 0.42, lam, co=10.5, mau=INK)
        yy += 0.72
    ct = CT_CODE.get(ma)
    if ct:
        tex = CONG_THUC[ct][0] if ct in CONG_THUC else ct
        cao_o = min(max(cao_ct(tex, 17) + 0.12, 0.6), 0.98)
        hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x, yy + 0.02, 4.13, cao_o, nen_mau=NHAT, bo_goc=0.15)
        dat_ct(sl, tex, x + 0.1, yy + 0.08, 3.93, cao_o - 0.12, co=17, can_giua=True)
        yy += cao_o + 0.12
    if hinh:
        if 7.08 - yy < 1.2:
            print(f"  cảnh báo: slide code {ma}: hình chỉ còn {7.08 - yy:.2f} in")
        anh(sl, *hinh, x, yy + 0.05, 4.13, 7.08 - yy - 0.05)
    return sl


def bang(sl, x, y, cot: list[tuple[str, float, str]], hang: list[tuple], cao=0.58, co=15, dam_cot0=True):
    for ten, w, mau in cot:
        chu(sl, x + 0.15, y, w - 0.3, 0.4, ten.upper(), co=11, dam=True, mau=mau)
        x += w
    x0 = x - sum(w for _, w, _ in cot)
    tong = sum(w for _, w, _ in cot)
    for i, dong in enumerate(hang):
        yy = y + 0.45 + i * cao
        if i % 2 == 0:
            hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x0, yy, tong, cao - 0.04, nen_mau=NHAT, bo_goc=0.25)
        xx = x0
        for j, (o, (_, w, _)) in enumerate(zip(dong, cot, strict=True)):
            chu(sl, xx + 0.15, yy, w - 0.3, cao - 0.04, o, co=co, dam=(j == 0 and dam_cot0),
                mau=INK if j < len(cot) - 1 else MUTED, doc=MSO_ANCHOR.MIDDLE)
            xx += w


def o_bang(sl, x, y, gia_tri: list[list[str]], w: list[float], cao=0.46, nen_dau=INK, to: dict | None = None, co=15):
    """Bảng nhỏ vẽ bằng ô: dòng đầu là tiêu đề; to = {(r, c): (nền, chữ)}."""
    to = to or {}
    for r, dong in enumerate(gia_tri):
        xx = x
        for c, v in enumerate(dong):
            if r == 0:
                n, m = nen_dau, TRANG
            else:
                n, m = to.get((r, c), (NHAT if r % 2 else TRANG, INK))
            o = hinh_khoi(sl, MSO_SHAPE.RECTANGLE, xx, y + r * cao, w[c], cao, nen_mau=n, vien=VIEN)
            chu_trong(o, v, co=co, dam=(r == 0), mau=m)
            xx += w[c]


# ---------- mind map ----------

VI_TRI = {"A": (1.85, 0.75), "B": (1.85, 2.8), "C": (1.85, 4.85),
          "D": (10.35, 0.75), "E": (10.35, 2.8), "F": (10.35, 4.85)}


def ban_do(slide, ox, oy, s=1.0, sang: str | None = None, tren_nen_toi=False):
    """Mind map trong khung cục bộ 12,2 × 5,6 in, co giãn s, đặt tại (ox, oy)."""
    def X(v):
        return ox + v * s

    def Y(v):
        return oy + v * s

    cx, cy = 6.1, 2.8
    xam = "3A4A63" if tren_nen_toi else "E1E5EB"
    for k, (x, y) in VI_TRI.items():
        mau = PHAN[k][1] if (sang is None or sang == k) else xam
        noi(slide, X(cx), Y(cy), X(x), Y(y), mau=mau, day=2.25 if s > 0.6 else 1.5)
    tam = hinh_khoi(slide, MSO_SHAPE.OVAL, X(cx - 1.75), Y(cy - 0.8), 3.5 * s, 1.6 * s, nen_mau=INK,
                    vien="8FA3BF" if tren_nen_toi else None)
    if s > 0.6:
        chu_trong(tam, [[("Dữ liệu cho dự báo", 18, True, TRANG)], [("buổi 1–15", 13, False, "C9D3E0")]])
    for k, (x, y) in VI_TRI.items():
        ten, mau, buoi, y_con = PHAN[k]
        tat = sang is not None and sang != k
        w, h = 3.5, 1.35
        o = hinh_khoi(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(x - w / 2), Y(y - h / 2), w * s, h * s,
                      nen_mau=xam if tat else mau, bo_goc=0.18)
        mau_chu = ("7C8BA1" if tren_nen_toi else "9AA5B4") if tat else TRANG
        if s > 0.6:
            chu_trong(o, [[(f"{k}. {ten}", 17, True, mau_chu)], [(buoi, 12, True, mau_chu)],
                          [(y_con, 11, False, mau_chu)]], le=0.15)
        else:
            chu_trong(o, [[(f"{k}. {ten}", 10, True, mau_chu)]], le=0.04)


def mo_phan(prs, k: str, cau: str):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    MUC.append((f"phan-{k.lower()}", f"Phần {k}: {PHAN[k][0]}"))
    KHONG_DEM.add(len(prs.slides))
    nen(sl, INK)
    ten, mau, buoi, _ = PHAN[k]
    o = hinh_khoi(sl, MSO_SHAPE.OVAL, 0.9, 2.0, 1.6, 1.6, nen_mau=mau)
    chu_trong(o, k, co=60, dam=True, mau=TRANG)
    chu(sl, 0.9, 3.95, 6.6, 0.9, ten, co=38, dam=True, mau=TRANG)
    chu(sl, 0.9, 4.85, 5.6, 0.5, buoi, co=18, dam=True, mau=mau if k != "F" else "A9B4C4")
    chu(sl, 0.9, 5.4, 5.4, 1.0, cau, co=16, mau="C9D3E0")
    ban_do(sl, 6.9, 1.95, s=0.5, sang=k, tren_nen_toi=True)


def luoi_buoc(sl, x, y, w, h, buoc: list[tuple[str, str]], so_cot: int, mau: str, co=13):
    """Các bước đánh số trong ô bo góc, xếp so_cot cột (đọc trái sang phải rồi xuống dòng); mũi tên nối hai ô cạnh nhau."""
    so_hang = -(-len(buoc) // so_cot)
    gx, gy = 0.32, 0.2
    bw, bh = (w - gx * (so_cot - 1)) / so_cot, (h - gy * (so_hang - 1)) / so_hang
    for i, (tieu, noi_dung) in enumerate(buoc):
        r, c = divmod(i, so_cot)
        bx, by = x + c * (bw + gx), y + r * (bh + gy)
        hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh, nen_mau=NHAT, bo_goc=0.08)
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, bx + 0.15, by + 0.15, 0.42, 0.42, nen_mau=mau)
        chu_trong(o, str(i + 1), co=14, dam=True, mau=TRANG)
        chu(sl, bx + 0.67, by + 0.1, bw - 0.77, 0.52, tieu, co=co + 1, dam=True, mau=mau, doc=MSO_ANCHOR.MIDDLE)
        chu(sl, bx + 0.2, by + 0.72, bw - 0.4, bh - 0.8, noi_dung, co=co, cach_dong=2)
        if c < so_cot - 1 and i < len(buoc) - 1:
            noi(sl, bx + bw + 0.04, by + bh / 2, bx + bw + gx - 0.04, by + bh / 2, mau="9AA5B4", day=2, mui_ten=True)


# ---------- nội dung ----------

def xay() -> Presentation:
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    L = prs.slide_layouts[6]

    # ===== Mở đầu =====
    sl = prs.slides.add_slide(L)
    MUC.append(("tieu-de", "Dữ liệu cho dự báo"))
    KHONG_DEM.add(len(prs.slides))
    nen(sl, INK)
    chu(sl, 0.9, 1.0, 8, 0.4, "KHOÁ FORECASTING IN AI · BUỔI 1–15", co=14, dam=True, mau="8FA3BF")
    chu(sl, 0.9, 1.7, 11.5, 2.4, [[("Dữ liệu cho dự báo", 60, True, TRANG)],
                                  [("hiểu · làm sạch · đánh giá trung thực", 26, False, "C9D3E0")]], cach_dong=10)
    for i, k in enumerate(PHAN):
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, 0.9 + i * 0.75, 5.2, 0.5, 0.5, nen_mau=PHAN[k][1])
        chu_trong(o, k, co=14, dam=True, mau=TRANG)
    chu(sl, 0.9, 6.0, 11, 0.5, "Nền móng (1–3) · Hiểu & chuẩn bị dữ liệu (4–13) · Đánh giá trung thực (14–15)",
        co=16, mau="A9B4C4")

    sl = prs.slides.add_slide(L)
    MUC.append(("ban-do", "Hôm nay nói gì: sáu phần"))
    KHONG_DEM.add(len(prs.slides))
    nen(sl, TRANG)
    chu(sl, 0.6, 0.42, 12, 0.8, "Hôm nay nói gì: sáu phần", co=32, dam=True, doc=MSO_ANCHOR.MIDDLE)
    ban_do(sl, 0.57, 1.55, s=1.0)

    sl = prs.slides.add_slide(L)
    MUC.append(("lo-trinh", "15 buổi móng của lộ trình 44 buổi"))
    KHONG_DEM.add(len(prs.slides))
    nen(sl, TRANG)
    chu(sl, 0.6, 0.42, 12, 0.8, "15 buổi móng của lộ trình 44 buổi", co=32, dam=True, doc=MSO_ANCHOR.MIDDLE)
    so = [("3", "nền móng", "buổi 1–3", PHAN["A"][1]), ("10", "hiểu & chuẩn bị dữ liệu", "buổi 4–13", PHAN["B"][1]),
          ("2", "đánh giá trung thực", "buổi 14–15", PHAN["D"][1])]
    for i, (n, ten, b, mau) in enumerate(so):
        x = 0.6 + i * 4.15
        chu(sl, x, 1.6, 3.9, 1.3, n, co=72, dam=True, mau=mau)
        chu(sl, x, 2.95, 3.9, 0.45, ten, co=20, dam=True)
        chu(sl, x, 3.4, 3.9, 0.4, b, co=14, mau=MUTED)
    nhom = [(1, 3, PHAN["A"][1]), (4, 13, PHAN["B"][1]), (14, 15, PHAN["D"][1])]
    w, gap, x0, y0 = 0.245, 0.03, 0.6, 4.55
    for n in range(1, 45):
        mau = next((m for a, b, m in nhom if a <= n <= b), "E1E5EB")
        hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x0 + (n - 1) * (w + gap), y0, w, 0.55, nen_mau=mau, bo_goc=0.2)
    chu(sl, x0, y0 + 0.7, 4.3, 0.4, "buổi 1 → 15: hôm nay", co=14, dam=True)
    chu(sl, x0 + 4.2, y0 + 0.7, 7.9, 0.8, "16–21 thống kê · 22–24 ML · 25–28 bất định · 29–33 deep learning · "
        "34–37 foundation model & LLM · 38–40 nhân quả · 41–43 production · 44 dự án cuối", co=12, mau=MUTED)

    sl = prs.slides.add_slide(L)
    MUC.append(("nhip", "Nhìn trước, xử lý sau, kiểm lại cuối"))
    KHONG_DEM.add(len(prs.slides))
    nen(sl, TRANG)
    chu(sl, 0.6, 0.42, 12, 0.8, "Nhìn trước, xử lý sau, kiểm lại cuối", co=32, dam=True, doc=MSO_ANCHOR.MIDDLE)
    buoc = [("1", "Nhìn", "vẽ đủ biểu đồ"), ("2", "Giả thuyết", "nghi điều gì?"), ("3", "Kiểm bằng số", "đếm, đo, test"),
            ("4", "Xử lý", "sửa có ghi lại"), ("5", "Kiểm lại", "so trước / sau")]
    d, gap = 1.7, 0.9
    x0 = (13.333 - (5 * d + 4 * gap)) / 2
    for i, (n, ten, phu) in enumerate(buoc):
        x = x0 + i * (d + gap)
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, x, 2.1, d, d, nen_mau=INK if i != 4 else PHAN["A"][1])
        chu_trong(o, n, co=44, dam=True, mau=TRANG)
        chu(sl, x - 0.4, 4.0, d + 0.8, 0.5, ten, co=20, dam=True, can=PP_ALIGN.CENTER)
        chu(sl, x - 0.4, 4.5, d + 0.8, 0.4, phu, co=15, mau=MUTED, can=PP_ALIGN.CENTER)
        if i < 4:
            noi(sl, x + d + 0.12, 2.1 + d / 2, x + d + gap - 0.12, 2.1 + d / 2, mau="9AA5B4", day=2.5, mui_ten=True)
    hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, 5.35, 12.13, 1.3, nen_mau=NHAT, bo_goc=0.15)
    chu(sl, 0.9, 5.5, 11.5, 1.0, [[("Ví dụ:  ", 16, True, PHAN["A"][1]),
                                   ("thấy một giờ bằng 0 lúc rạng sáng Chủ nhật tháng 3, nghi do đổi giờ mùa hè, đếm lại số giờ "
                                    "của ngày đó, đổi sang UTC rồi mới gộp, và vẽ lại ngày đó để chắc chắn.", 16, False, INK)]],
        doc=MSO_ANCHOR.MIDDLE)

    # ===== A. Khái niệm nền (theo thứ tự buổi) =====
    mo_phan(prs, "A", "Mỗi khái niệm: để làm gì, là gì, cao thấp nghĩa là gì, và một ví dụ có số.")

    for i, (tieu, cap) in enumerate(TU_NEN, 1):
        sl = moi(prs, f"tu-nen-{i}", tieu, "A")
        KHONG_DEM.add(len(prs.slides))
        bang(sl, 0.6, 1.3, [("Từ", 2.6, PHAN["A"][1]), ("Là gì", 5.9, MUTED), ("Ví dụ", 3.63, MUTED)], cap, cao=0.42, co=12)

    sl = moi(prs, "du-bao-la-gi", "Dự báo là điều sẽ xảy ra, không phải điều muốn", "A", "Buổi 1")
    KHONG_DEM.add(len(prs.slides))
    yb = dau_than("du-bao-la-gi", None) + 0.05
    chu(sl, 0.6, yb, 5.9, 0.35, "Ba thứ hay bị nhập làm một", co=15, dam=True, mau=PHAN["A"][1])
    o_bang(sl, 0.6, yb + 0.45, [["", "Trả lời", "Quán cà phê"], ["Dự báo", "điều gì sẽ xảy ra", "tuần tới bán khoảng 1.900 ly"],
                                ["Mục tiêu", "ta muốn điều gì", "bán 2.500 ly"],
                                ["Kế hoạch", "ta làm gì để tới gần", "khuyến mãi, đặt thêm hạt"]],
           [1.35, 2.0, 2.55], cao=0.62, co=13)
    chu(sl, 0.6, yb + 3.15, 5.9, 1.2, "Sếp muốn 2.500 ly nên bảo “dự báo 2.500”: kho đặt hàng cho 2.500, tuần đó bán 1.900, "
        "thừa 600 ly, và không ai còn biết dự báo đúng hay sai.", co=13, mau=MUTED)
    chu(sl, 6.9, yb, 5.83, 0.35, "Bốn điều cho biết một thứ dự báo được tới đâu", co=15, dam=True, mau=PHAN["A"][1])
    o_bang(sl, 6.9, yb + 0.45, [["", "Điện ngày mai", "Tỷ giá tuần sau"],
                                ["Hiểu cái gì tác động tới nó", "có", "ít"], ["Có nhiều dữ liệu", "có", "có"],
                                ["Tương lai giống quá khứ", "thường có", "khủng hoảng làm đổi hẳn"],
                                ["Dự báo không làm đổi chính nó", "đúng", "sai: người ta mua bán theo dự báo"]],
           [2.35, 1.3, 2.18], cao=0.62, co=12,
           to={(r, 1): (XANH_NHAT, XANH) for r in range(1, 5)} | {(1, 2): (DO_NHAT, DO), (3, 2): (DO_NHAT, DO),
                                                               (4, 2): (DO_NHAT, DO), (2, 2): (XANH_NHAT, XANH)})
    chu(sl, 6.9, yb + 3.8, 5.83, 0.8, "Điện ngày mai thoả cả bốn nên đoán được rất sát; tỷ giá chỉ thoả một.", co=13, mau=MUTED)

    khai_niem(prs, "goc-tam")

    sl = moi(prs, "mo-hinh", "Mô hình học từ phần học, bị chấm ở kỳ chấm", "A", "Buổi 1, 14",
             "học trên đề cũ, thi trên đề mới; thuộc lòng đề cũ không có nghĩa là giỏi.")
    KHONG_DEM.add(len(prs.slides))
    ym = dau_than("mo-hinh", True) + 0.15
    hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, ym, 8.2, 0.75, nen_mau="DCE3EA", bo_goc=0.2)
    chu_trong(hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, ym, 8.2, 0.75, bo_goc=0.2),
              [[("Phần học: mô hình được thấy, dùng để khớp tham số", 15, True, INK)]])
    o = hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 8.95, ym, 3.78, 0.75, nen_mau=PHAN["A"][1], bo_goc=0.2)
    chu_trong(o, [[("Kỳ chấm: giấu đi, chỉ để chấm", 15, True, TRANG)]])
    chu(sl, 8.85, ym + 0.8, 1.2, 0.3, "gốc dự báo", co=12, dam=True, mau="E07B00")
    noi(sl, 8.87, ym - 0.1, 8.87, ym + 0.85, mau="E07B00", day=2.5)
    ba = [("Mô hình, tham số", "Mô hình là một cách tính ra dự báo; tham số là các con số bên trong nó. “Mai = trung bình 7 ngày qua” là một "
           "mô hình có một tham số: số 7."),
          ("Khớp (fit), học", "Chọn tham số từ dữ liệu phần học. Đo sai số trên chính phần học (phần dư) luôn đẹp hơn thật."),
          ("Học thuộc (overfit)", "Mô hình đủ nhiều tham số thì khớp gần hoàn hảo phần học mà dự báo mới vẫn tệ: thuộc đề cũ được 10 điểm, "
           "đề mới chỉ 6.")]
    for i, (t, v) in enumerate(ba):
        the(sl, 0.6 + i * 4.11, ym + 1.5, 3.91, 2.6, t, v, PHAN["A"][1], NHAT, co=14)
    chu(sl, 0.6, ym + 4.3, 12.13, 0.6, "Mọi chỉ số chính xác trong khoá đều tính trên kỳ chấm; phần dư chỉ dùng để chẩn đoán.",
        co=14, dam=True, mau=MUTED)

    sl = moi(prs, "phieu-6-o", "Điền 6 ô trước khi mở dữ liệu", "A", "Buổi 1")
    KHONG_DEM.add(len(prs.slides))
    o6 = [("1", "Quyết định", "Ai dùng dự báo, để làm gì?", "Năm ô còn lại đều suy ra từ ô này.",
           "cuối Chủ nhật đặt mua điện theo giờ cho 7 ngày tới"),
          ("2", "Biến mục tiêu", "Dự báo con số nào, đơn vị gì?", "Sai đơn vị là dự báo giỏi một con số không ai cần.",
           "kWh (điện năng) mỗi giờ, không phải kW (công suất)"),
          ("3", "Tầm dự báo", "Nhìn xa bao nhiêu bước?", "Nhìn xa h bước thì chỉ dùng được số liệu cũ hơn h bước.",
           "1–168 giờ, tính từ 00:00 thứ Hai"),
          ("4", "Độ chi tiết", "Chấm ở mức nào?", "Chấm sai mức là chọn nhầm mô hình.", "theo giờ, cho cả khu"),
          ("5", "Mốc cắt dữ liệu", "Lúc dự báo đã biết gì?", "Lỡ dùng thứ chưa có là rò rỉ: backtest đẹp, dùng thật tệ.",
           "số đo tới 23:59 Chủ nhật; thời tiết chỉ có bản dự báo"),
          ("6", "Chi phí sai hai chiều", "Thiếu mất gì? Thừa mất gì?", "Thiếu đắt hơn thừa thì nên báo cao hơn trung bình.",
           "thiếu mất 4 đồng/kWh, thừa mất 1 đồng")]
    y6 = dau_than("phieu-6-o", None)
    for i, (n, ten, hoi, vi_sao, vd) in enumerate(o6):
        r, c = divmod(i, 3)
        x, y = 0.6 + c * 4.11, y6 + 0.05 + r * 2.6
        hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 3.91, 2.45, nen_mau=NHAT, bo_goc=0.08)
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, x + 0.25, y + 0.2, 0.5, 0.5, nen_mau=PHAN["A"][1])
        chu_trong(o, n, co=17, dam=True, mau=TRANG)
        chu(sl, x + 0.9, y + 0.2, 2.9, 0.5, ten, co=17, dam=True, doc=MSO_ANCHOR.MIDDLE)
        chu(sl, x + 0.25, y + 0.85, 3.45, 0.35, hoi, co=14, dam=True, mau=PHAN["A"][1])
        chu(sl, x + 0.25, y + 1.2, 3.45, 0.55, vi_sao, co=13)
        chu(sl, x + 0.25, y + 1.75, 3.45, 0.6, f"Ví dụ: {vd}", co=12, mau=MUTED)

    khai_niem(prs, "baseline")

    sl = moi(prs, "bon-baseline", "Bốn baseline, tính bằng tay", "A", "Buổi 1, 14",
             "baseline nào cũng là một giả định đơn giản về tương lai.")
    KHONG_DEM.add(len(prs.slides))
    yb2 = dau_than("bon-baseline", True) + 0.1
    chu(sl, 0.6, yb2, 12.13, 0.4, [[("Chuỗi 10, 14, 12, 16, 14, 18, mùa dài m = 2, dự báo 2 bước tới", 15, True, INK)]])
    o_bang(sl, 0.6, yb2 + 0.5, [["Baseline", "Giả định", "Cách tính", "Dự báo"],
                                ["mean", "tương lai quanh trung bình cũ", "84 / 6", "14; 14"],
                                ["naive", "tương lai giống điểm cuối", "lấy số cuối", "18; 18"],
                                ["seasonal naive", "lặp lại mùa trước", "lấy cùng vị trí mùa trước", "14; 18"],
                                ["drift", "đi tiếp theo độ dốc cũ", "(18 − 10) / 5 = 1,6 mỗi bước", "19,6; 21,2"]],
           [2.3, 3.9, 3.6, 2.33], cao=0.6, co=14)
    chu(sl, 0.6, yb2 + 3.7, 12.13, 1.0, "Hai quy tắc: độ trễ của baseline phải ít nhất bằng tầm dự báo, ở mọi h (dự báo 7 ngày thì không dùng "
        "“cùng giờ hôm qua”); và mô hình phải thắng cả bốn, vì baseline thắng không phải lúc nào cũng là seasonal naive.",
        co=14, mau=MUTED)

    khai_niem(prs, "sai-so-ao")

    sl = moi(prs, "du-bao-cuon", "Dự báo cuốn: chấm như lúc dùng thật", "A", "Buổi 1",
             "đứng ở một thứ Hai, chỉ nhìn quá khứ, đoán tuần tới, chấm, rồi dời sang thứ Hai sau.")
    yc = dau_than("du-bao-cuon", True)
    anh(sl, 1, "kn-du-bao-cuon", 0.6, yc, 6.6, 7.1 - yc)
    buoc_c = [("1", "Đặt gốc", "Chọn một thứ Hai 00:00 làm gốc dự báo."),
              ("2", "Chỉ dùng quá khứ", "Dựng dự báo chỉ từ dữ liệu trước gốc; tuần sắp đoán bị giấu."),
              ("3", "Dự báo rồi chấm", "Đoán 168 giờ tới, sau đó mới mở số đo thật để tính sai số."),
              ("4", "Dời gốc, lặp lại", "Sang thứ Hai sau, làm lại, rồi lấy trung bình sai số. Làm vậy trên quá khứ gọi là backtest.")]
    kc_c = (7.1 - yc) / 4
    for i, (n, t, v) in enumerate(buoc_c):
        yy = yc + i * kc_c
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, 7.55, yy + 0.05, 0.46, 0.46, nen_mau=PHAN["A"][1])
        chu_trong(o, n, co=15, dam=True, mau=TRANG)
        chu(sl, 8.2, yy, 4.5, 0.35, t, co=15, dam=True, mau=PHAN["A"][1])
        chu(sl, 8.2, yy + 0.36, 4.5, kc_c - 0.4, v, co=13)
    KHONG_DEM.add(len(prs.slides))

    khai_niem(prs, "do-chi-tiet")

    khai_niem(prs, "quantile")
    khai_niem(prs, "newsvendor")
    khai_niem(prs, "phan-phoi")
    khai_niem(prs, "do-lech-chuan")
    khai_niem(prs, "he-so-lech")
    khai_niem(prs, "con-so-bao")

    khai_niem(prs, "phan-phoi-chuan")
    khai_niem(prs, "khoang")

    khai_niem(prs, "khoang-tin-cay")
    khai_niem(prs, "kiem-dinh")
    khai_niem(prs, "hoan-vi")

    khai_niem(prs, "bootstrap")

    # Bản 2: sơ đồ từng bước (người học từng nhớ nhầm "lấy ±1,96"); số lấy từ buoi-02/tai-lieu.md mục 4.6.
    sl = moi(prs, "bootstrap-buoc", "Bootstrap từng bước: rút lại, lấy hai đầu", "A", "Buổi 2",
             "khoảng 95% là hai đầu của vài nghìn trung bình tính lại, không phải trung bình ± 1,96.")
    KHONG_DEM.add(len(prs.slides))
    mau = PHAN["A"][1]
    yb = dau_than("bootstrap-buoc", True) + 0.05
    luoi_buoc(sl, 0.6, yb, 12.13, 1.95, [
        ("Mẫu thật", "n số đang có. Ví dụ 5 ngày: 12, 15, 11, 30, 14; trung bình 16,4."),
        ("Rút lại n số", "Có hoàn lại: số có thể lặp, số có thể bị bỏ. Có tự tương quan thì rút cả khối."),
        ("Tính lại", "Mỗi lần rút cho một trung bình mới."),
        ("Lặp vài nghìn lần", "Được vài nghìn trung bình: thấy con số dao động cỡ nào."),
        ("Lấy hai đầu", "Quantile 0,025 và 0,975 của các trung bình là khoảng tin cậy 95%.")], 5, mau, co=14)
    y2 = yb + 2.25
    chu(sl, 0.6, y2, 5.9, 0.35, "Rút từng điểm: ba lần đầu", co=15, dam=True, mau=mau)
    o_bang(sl, 0.6, y2 + 0.45, [["Lần", "Mẫu lại", "Trung bình"], ["1", "14, 12, 12, 15, 12", "13,0"],
                                ["2", "14, 14, 11, 12, 12", "12,6"], ["3", "15, 11, 30, 11, 15", "16,4"]],
           [0.9, 3.3, 1.7], cao=0.5, co=14)
    chu(sl, 0.6, y2 + 2.55, 5.9, 0.7, "Lần 1 và 2 không trúng số 30 nên trung bình thấp hẳn; thứ tự các ngày bị xáo tung.",
        co=13, mau=MUTED)
    chu(sl, 6.9, y2, 5.83, 0.35, "Rút khối dài 2: giữ các ngày liền nhau", co=15, dam=True, mau=mau)
    for i, k in enumerate(["30, 14", "15, 11", "12, 15"]):
        o = hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 6.9 + i * 1.95, y2 + 0.5, 1.75, 0.6, nen_mau=LAM_NHAT, vien=LAM,
                      bo_goc=0.2)
        chu_trong(o, f"({k})", co=16, dam=True, mau=LAM)
    chu(sl, 6.9, y2 + 1.3, 5.83, 1.3, [[("Nối lại, cắt còn 5 số: ", 14, False, INK), ("30, 14, 15, 11, 12", 14, True, INK),
                                        (" → trung bình 16,4.", 14, False, INK)],
                                       [("Ngày 30 và ngày 14 ngay sau nó vẫn đi cùng nhau, nên mối liên hệ giữa hai ngày liền "
                                         "nhau được giữ.", 13, False, MUTED)]], cach_dong=6)

    khai_niem(prs, "utc")

    khai_niem(prs, "resample")

    khai_niem(prs, "merge-asof")

    sl = moi(prs, "dang-dai", "Dạng dài: ai, khi nào, bao nhiêu", "A", "Buổi 3",
             "thêm chuỗi chỉ thêm dòng, không thêm cột.")
    KHONG_DEM.add(len(prs.slides))
    chu(sl, 0.6, 2.45, 5.6, 0.35, "Dạng dài: mọi buổi sau nhận vào dạng này", co=12, dam=True, mau=PHAN["A"][1])
    o_bang(sl, 0.6, 2.85, [["unique_id", "ds (UTC)", "y"], ["A", "05:00", "3"], ["A", "06:00", "0"], ["A", "07:00", "5"],
                           ["B", "05:00", "1"], ["B", "06:00", "2"], ["B", "07:00", "0"]], [1.7, 2.0, 1.2])
    chu(sl, 7.0, 2.45, 5.7, 0.35, "Dạng rộng: dễ nhìn nhưng khó mở rộng", co=12, dam=True, mau=MUTED)
    o_bang(sl, 7.0, 2.85, [["ds (UTC)", "A", "B"], ["05:00", "3", "1"], ["06:00", "0", "2"], ["07:00", "5", "0"]],
           [2.0, 1.4, 1.4], nen_dau=MUTED)
    for i, (t, v) in enumerate([("unique_id", "ai: chuỗi nào"), ("ds", "khi nào: mốc thời gian UTC"),
                                ("y", "bao nhiêu: giá trị đo")]):
        chu(sl, 7.0, 4.9 + i * 0.5, 5.7, 0.45, [[(f"{t}  ", 17, True, PHAN["A"][1]), (v, 17, False, INK)]])
    chu(sl, 0.6, 6.35, 12.13, 0.6, "Bảng sạch khi mỗi cặp (unique_id, ds) chỉ có một dòng, đủ mọi mốc và không trùng.", co=16, dam=True,
        mau=MUTED)

    khai_niem(prs, "mua-vu")

    khai_niem(prs, "doc-hinh")
    khai_niem(prs, "lam-tron")
    khai_niem(prs, "thang-log")

    sl = moi(prs, "bo-bieu-do", "Tám biểu đồ, tám câu hỏi", "A", "Buổi 4",
             "mỗi hình trả lời đúng một câu; một hình không đủ để kết luận.")
    KHONG_DEM.add(len(prs.slides))
    y8 = dau_than("bo-bieu-do", True)
    anh(sl, 4, "bo-bieu-do", 0.6, y8, 4.2, 7.15 - y8)
    tam = [("Đường theo ngày", "xu hướng, mùa năm"), ("Seasonal plot tuần", "hình dạng một vòng lặp"),
           ("Subseries theo tháng", "mỗi mùa đổi qua các năm ra sao"), ("Lag plot", "giống k bước trước tới đâu"),
           ("Heatmap giờ × thứ", "mùa vụ kép ngày trong tuần"), ("Boxplot theo giờ", "độ tản: giờ nào khó"),
           ("Scatter với nhiệt độ", "quan hệ với biến khác, theo năm"), ("ACF", "nhịp lặp, đo bằng số")]
    for i, (t, v) in enumerate(tam):
        r, c = divmod(i, 2)
        x, y = 5.2 + c * 3.8, y8 + r * 0.98
        hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 3.6, 0.86, nen_mau=NHAT, bo_goc=0.12)
        chu(sl, x + 0.2, y + 0.08, 3.2, 0.35, f"{i + 1}  {t}", co=14, dam=True, mau=PHAN["A"][1])
        chu(sl, x + 0.2, y + 0.44, 3.2, 0.4, v, co=13)
    chu(sl, 5.2, y8 + 3.98, 7.4, 0.9, "Thêm hai thói quen: vẽ đường làm trơn đè lên dữ liệu gốc chứ đừng thay nó, để không "
        "mất ngày bất thường; trên thang log, cùng độ dốc nghĩa là cùng phần trăm thay đổi.", co=13, mau=MUTED)

    khai_niem(prs, "seasonal-subseries")
    khai_niem(prs, "boxplot")

    khai_niem(prs, "lag-plot")
    khai_niem(prs, "acf")
    khai_niem(prs, "truc-y-cat")
    khai_niem(prs, "tron-nam")

    khai_niem(prs, "dieu-chinh")
    khai_niem(prs, "log")
    khai_niem(prs, "box-cox")
    khai_niem(prs, "guerrero")
    khai_niem(prs, "exp-trung-vi")

    khai_niem(prs, "phan-ra")

    khai_niem(prs, "phan-ra-cach")
    khai_niem(prs, "ty-le-mau-hinh")
    khai_niem(prs, "stl-loess")
    khai_niem(prs, "f-s")
    khai_niem(prs, "robust")

    khai_niem(prs, "ar")
    khai_niem(prs, "pacf")

    khai_niem(prs, "ljung-box")
    khai_niem(prs, "ljung-box-q")

    khai_niem(prs, "dung")
    khai_niem(prs, "random-walk")

    # Bản 2: bảng so bốn chuỗi mẫu (người học tự lập bảng này khi học); số từ buoi-07/tai-lieu.md mục 4.2, seed 42.
    sl = moi(prs, "bon-chuoi", "Bốn chuỗi mẫu: nhớ gì, có dừng không", "A", "Buổi 7",
             "mẹo nhớ: random walk thì sai phân; dừng quanh xu hướng thì khử xu hướng.")
    KHONG_DEM.add(len(prs.slides))
    yb = dau_than("bon-chuoi", True) + 0.1
    xanh_o, cam_o, do_o = (XANH_NHAT, XANH), ("FDF0E8", "B4541B"), (DO_NHAT, DO)
    o_bang(sl, 0.6, yb, [["Chuỗi mẫu", "Công thức", "Nhớ quá khứ?", "Dừng?", "r1 / r30", "Chữa"],
                         ["nhiễu trắng", "y_t = ε_t", "không nhớ gì", "có", "0,10 / −0,05", "không cần"],
                         ["AR(1), φ = 0,7", "y_t = 0,7·y_(t−1) + ε_t", "nhớ, rồi kéo về mức", "có", "0,71 / −0,03", "không cần"],
                         ["random walk", "y_t = y_(t−1) + ε_t", "nhớ mãi, không quay về", "không", "0,98 / 0,53", "sai phân"],
                         ["xu hướng", "y_t = 0,05·t + ε_t", "không; bám một đường", "quanh đường xu hướng", "0,98 / 0,81",
                          "khử xu hướng"]],
           [2.1, 2.9, 2.4, 1.95, 1.4, 1.38], cao=0.68, co=14,
           to={(1, 3): xanh_o, (2, 3): xanh_o, (3, 3): do_o, (4, 3): cam_o, (3, 5): do_o, (4, 5): cam_o})
    y2 = yb + 3.6
    the(sl, 0.6, y2, 5.95, 1.35, "ACF chưa đủ để tách",
        "Random walk và xu hướng cùng có r1 ≈ 0,98 và ACF giảm chậm như nhau. Muốn tách phải chạy ADF và KPSS dạng “ct”.",
        LAM, LAM_NHAT, co=14)
    the(sl, 6.78, y2, 5.95, 1.35, "Chữa nhầm thì sao",
        "Sai phân chuỗi quanh xu hướng là sai phân thừa, sinh tương quan âm giả. Trừ đường thẳng khỏi random walk thì phần còn lại "
        "vẫn lang thang.", DO, DO_NHAT, co=14)
    chu(sl, 0.6, 7.1, 12.13, 0.3, "Mô phỏng 500 điểm, seed 42. r1, r30: tự tương quan ở trễ 1 và trễ 30.", co=11, mau=MUTED)

    sl = moi(prs, "adf-kpss-la-gi", "ADF và KPSS là gì: hai câu hỏi ngược chiều", "A", "Buổi 7",
             "ADF hỏi ‘có lực kéo về không?’; KPSS hỏi ‘có trôi đi không?’")
    yk = dau_than("adf-kpss-la-gi", True)
    anh(sl, 7, "kn-adf-kpss", 0.6, yk, 6.3, 5.8 - yk)
    the(sl, 7.2, yk, 5.53, 1.55, "ADF",
        "Đang cao hơn mức thường thì bước sau có bị kéo xuống không? Giả định ban đầu: chuỗi không dừng. "
        "p < 0,05 nghĩa là có bằng chứng chuỗi dừng.", LAM, LAM_NHAT, co=13)
    the(sl, 7.2, yk + 1.65, 5.53, 1.55, "KPSS",
        "Chuỗi có trôi xa khỏi mức (hay đường xu hướng) hơn một chuỗi dừng cho phép không? Giả định ban đầu: chuỗi dừng. "
        "p < 0,05 nghĩa là có bằng chứng chuỗi không dừng.", "B4541B", "FDF0E8", co=13)
    the(sl, 0.6, 5.95, 12.13, 1.1, "Ví dụ tính tay",
        "Chuỗi 5, 8, 4, 6, 5: cứ cao hơn 5 là bước sau đi xuống, có lực kéo về như chuỗi dừng. "
        "Chuỗi 5, 6, 7, 6, 7: độ cao hiện tại không đoán được bước sau, giống random walk.", PHAN["A"][1], NHAT, co=14)
    KHONG_DEM.add(len(prs.slides))

    sl = moi(prs, "adf-kpss", "Chạy cả ADF và KPSS, rồi đọc bảng 2 × 2", "A", "Buổi 7",
             "hai kiểm định cùng nói một hướng thì tin; nói ngược nhau thì xem lại chuỗi.")
    KHONG_DEM.add(len(prs.slides))
    ya = dau_than("adf-kpss", True) + 0.1
    xanh_o, cam_o, do_o, xam_o = (XANH_NHAT, XANH), ("FDF0E8", "B4541B"), (DO_NHAT, DO), (NHAT, MUTED)
    o_bang(sl, 0.6, ya, [["", "KPSS không bác bỏ", "KPSS bác bỏ"],
                         ["ADF bác bỏ", "Dừng: không cần sai phân", "Mâu thuẫn: vẽ chuỗi, tìm cú sốc"],
                         ["ADF không bác bỏ", "Chưa đủ bằng chứng", "Không dừng: sai phân"]],
           [2.3, 2.75, 2.75], cao=0.95, to={(1, 1): xanh_o, (1, 2): do_o, (2, 1): xam_o, (2, 2): cam_o}, co=15)
    chu(sl, 0.6, ya + 2.95, 7.8, 0.9, "ADF p < 0,05: có bằng chứng dừng. KPSS p < 0,05: có bằng chứng không dừng. "
        "Chỉ ô xanh và ô cam cho kết luận rõ.", co=13, mau=MUTED)
    the(sl, 8.7, ya, 4.03, 1.95, "Dữ liệu thật: GDP Mỹ",
        "Cả giai đoạn 1947–2026: ADF p = 0,000, KPSS p = 0,048, rơi vào ô mâu thuẫn. Chỉ lấy 1985–2019 thì dừng.", LAM, LAM_NHAT, co=14)
    the(sl, 8.7, ya + 2.1, 4.03, 1.95, "Khai dạng cho đúng",
        "“c” hỏi dừng quanh một mức; “ct” hỏi dừng quanh một đường xu hướng. Khai sai dạng là kết luận sai.", PHAN["A"][1], NHAT,
        co=14)

    khai_niem(prs, "sai-phan-la-gi")

    # Bản 2: gói buổi 7 thành một quy trình (người học ghi lại quy trình này khi học).
    sl = moi(prs, "quy-trinh-chuoi-la", "Gặp một chuỗi lạ: bảy bước của buổi 7", "A", "Buổi 7",
             "nhìn trước, kiểm bằng số sau; chữa xong thì kiểm xem có chữa quá tay không.")
    KHONG_DEM.add(len(prs.slides))
    yb = dau_than("quy-trinh-chuoi-la", True) + 0.05
    luoi_buoc(sl, 0.6, yb, 12.13, 7.15 - yb, [
        ("Nhìn ACF", "Quanh 0: nhiễu trắng. Giảm rất chậm: chưa dừng. Có đỉnh đều: mùa vụ."),
        ("Nhìn PACF", "Cao ở vài trễ đầu rồi tắt hẳn sau trễ p: giống AR(p)."),
        ("Ljung-Box", "Một p-value cho nhiều trễ. p < 0,05 là còn quy luật. Đừng đếm cột vượt dải."),
        ("ADF và KPSS", "Chạy cả hai, cùng dạng: “c” nếu quanh một mức, “ct” nếu quanh một đường."),
        ("Đọc bảng 2 × 2", "Hai kiểm định cùng hướng thì tin. Mâu thuẫn thì vẽ chuỗi, tìm cú sốc hay đổi mức."),
        ("Chữa", "Random walk: sai phân. Quanh xu hướng: khử xu hướng. Có mùa vụ: sai phân mùa vụ trước."),
        ("Kiểm chữa quá tay", "Sai phân xong mà r1 về gần −0,5, hoặc độ lệch chuẩn tăng: bớt một lần.")], 4, PHAN["A"][1], co=16)
    khai_niem(prs, "scatter")
    khai_niem(prs, "spearman")
    khai_niem(prs, "durbin-watson")
    khai_niem(prs, "cdd-hdd")
    khai_niem(prs, "mi")
    khai_niem(prs, "hoan-vi-khoi")

    khai_niem(prs, "ccf")

    sl = moi(prs, "prewhitening", "Prewhitening: lọc nhịp riêng rồi mới đo", "A", "Buổi 8",
             "nhịp ngày có sẵn trong cả hai chuỗi làm tương quan chéo cao ở mọi trễ.")
    KHONG_DEM.add(len(prs.slides))
    yp = dau_than("prewhitening", True)
    anh(sl, 8, "ccf", 0.6, yp, 12.13, 2.75)
    bp = [("1", "Dựng AR cho x", "Tìm phần x tự đoán được từ quá khứ của chính nó (ở đây AR(48))."),
          ("2", "Lọc x", "Trừ phần tự đoán được, còn lại phần “bất ngờ” của x."),
          ("3", "Lọc y cùng bộ lọc", "Dùng đúng hệ số của x để lọc y, không dựng mô hình riêng."),
          ("4", "Tính CCF", "Đỉnh còn lại ở trễ nào thì x đi trước y chừng ấy bước.")]
    for i, (n, t, v) in enumerate(bp):
        x = 0.6 + i * 3.08
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, x, yp + 2.95, 0.46, 0.46, nen_mau=PHAN["A"][1])
        chu_trong(o, n, co=15, dam=True, mau=TRANG)
        chu(sl, x + 0.58, yp + 2.97, 2.4, 0.4, t, co=14, dam=True, mau=PHAN["A"][1])
        chu(sl, x, yp + 3.5, 2.9, 1.0, v, co=13)

    khai_niem(prs, "truot")

    khai_niem(prs, "granger")

    # Bản 2: "công thức ghi nhớ nhanh" người học tự viết cho buổi 8, mỗi bước thành một câu hỏi.
    sl = moi(prs, "quy-trinh-tuong-quan", "Đo quan hệ hai chuỗi: tám câu hỏi của buổi 8", "A", "Buổi 8",
             "đừng tin hệ số tương quan ngay: vẽ scatter trước, rồi đi qua từng câu hỏi.")
    KHONG_DEM.add(len(prs.slides))
    yb = dau_than("quy-trinh-tuong-quan", True) + 0.05
    luoi_buoc(sl, 0.6, yb, 12.13, 7.15 - yb, [
        ("Trông ra sao?", "Vẽ scatter: thẳng, cong, chữ U, hay có điểm lạ."),
        ("Thẳng hàng hay chỉ cùng tăng?", "Pearson đo mức thẳng hàng; Spearman đo cùng tăng theo thứ hạng."),
        ("Hai chuỗi cùng trôi?", "Đo lại trên sai phân, xem Durbin–Watson. CPI và dân số: r từ 0,97 còn −0,21."),
        ("Cong, đổi dấu?", "Tách CDD / HDD, hoặc đo MI; kiểm MI bằng hoán vị theo khối."),
        ("Ai đi trước, bao lâu?", "Prewhiten cả hai chuỗi bằng cùng một bộ lọc, rồi đọc tương quan chéo."),
        ("Giữ nguyên cả năm?", "Tương quan trượt 30, 90 ngày; đổi dấu theo mùa thì tách riêng từng mùa."),
        ("Quá khứ x giúp đoán y?", "Granger, chạy cả hai chiều. p nhỏ là “giúp dự báo”, chưa phải “gây ra”."),
        ("Lúc dự báo có x chưa?", "Chỉ dùng bản có trong tay lúc đó, như nhiệt độ dự báo (buổi 13).")], 4, PHAN["A"][1], co=15)

    khai_niem(prs, "dac-trung")

    khai_niem(prs, "pho")
    khai_niem(prs, "entropy")
    khai_niem(prs, "do-kho")

    khai_niem(prs, "ban-do-pca")

    khai_niem(prs, "dtw")

    khai_niem(prs, "abc-xyz")

    khai_niem(prs, "biet-truoc")

    sl = moi(prs, "shift-rolling", "Dự báo trước h bước: shift h trước, rolling sau", "A", "Buổi 13",
             "lag nhìn về một điểm quá khứ; rolling lấy trung bình một vùng gần đây.")
    KHONG_DEM.add(len(prs.slides))
    xanh, do = (XANH_NHAT, XANH), (DO_NHAT, DO)
    gt = [["ngày", "1", "2", "3", "4", "5", "6"],
          ["y", "10", "20", "30", "40", "50", "60"],
          ["shift(3)", "–", "–", "–", "10", "20", "30"],
          ["shift(3) rồi rolling(2)", "–", "–", "–", "–", "15", "25"],
          ["rolling(2), quên shift", "–", "15", "25", "35", "45", "55"]]
    to = {(3, 5): xanh, (3, 6): xanh, **{(4, c): do for c in range(2, 7)}}
    o_bang(sl, 0.6, 2.35, gt, [3.4] + [1.45] * 6, cao=0.6, to=to, co=16)
    the(sl, 0.6, 5.6, 5.95, 1.3, "Đúng (h = 3)", "Ngày 6 dùng trung bình ngày 2–3: đã biết từ ngày 3.",
        XANH, XANH_NHAT)
    the(sl, 6.78, 5.6, 5.95, 1.3, "Rò rỉ", "Ngày 6 dùng ngày 5–6: lúc dự báo (ngày 3) chưa có.", DO, DO_NHAT)

    khai_niem(prs, "feature-lich")
    khai_niem(prs, "ca-chuoi")
    khai_niem(prs, "kiem-ro-ri")
    khai_niem(prs, "ex-ante")

    # ===== B. Vấn đề dữ liệu (theo thứ tự buổi) =====
    mo_phan(prs, "B", "Mỗi vấn đề: thấy gì thì nghi, kiểm bằng gì, và sửa ra sao.")

    sl = moi(prs, "ma-tran", "Rò rỉ tương lai gặp ở 8 buổi", "B")
    KHONG_DEM.add(len(prs.slides))
    ma_tran = [("Múi giờ / DST", [3, 6, 10]), ("Thiếu dữ liệu", [1, 4, 6, 7, 10]),
               ("Mốc trùng, mã trá hình", [3, 10]), ("Ngoại lai", [6, 11]), ("Điểm gãy, dịch mức", [2, 5, 7, 11]),
               ("Nhiễu", [12]), ("Rò rỉ tương lai", [1, 5, 8, 9, 10, 12, 13, 15]), ("Số 0 làm hỏng chỉ số", [10, 14])]
    x0, y0, o, h = 4.1, 1.9, 0.57, 0.52
    for n in range(1, 16):
        chu(sl, x0 + (n - 1) * o, y0, o, 0.35, str(n), co=13, dam=True, mau=MUTED, can=PP_ALIGN.CENTER)
    for i, (ten, bs) in enumerate(ma_tran):
        y = y0 + 0.5 + i * h
        ro = ten.startswith("Rò rỉ")
        if ro:
            hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, y - 0.03, 12.13, h - 0.02, nen_mau="FDF0E8", bo_goc=0.3)
        chu(sl, 0.8, y, 3.2, h - 0.08, ten, co=16, dam=ro, doc=MSO_ANCHOR.MIDDLE)
        for n in range(1, 16):
            cx = x0 + (n - 1) * o + o / 2
            if n in bs:
                hinh_khoi(sl, MSO_SHAPE.OVAL, cx - 0.14, y + h / 2 - 0.17, 0.28, 0.28, nen_mau=PHAN["B"][1])
            else:
                hinh_khoi(sl, MSO_SHAPE.OVAL, cx - 0.04, y + h / 2 - 0.07, 0.08, 0.08, nen_mau="D5DBE3")
    chu(sl, 0.6, 6.72, 12.13, 0.35, "Cột = buổi · chấm cam = buổi dạy cách nhận ra và sửa", co=13, mau=MUTED)

    van_de(prs, "mui-gio")

    van_de(prs, "gop")

    van_de(prs, "bieu-do-sai")

    van_de(prs, "dao-dong")

    van_de(prs, "doi-nguoc")

    van_de(prs, "chu-ky-sai")

    van_de(prs, "sai-phan")

    van_de(prs, "tuong-quan-gia")

    van_de(prs, "chu-u")

    van_de(prs, "thieu-moc")

    khai_niem(prs, "mcar")
    van_de(prs, "mnar")

    van_de(prs, "tra-hinh")
    khai_niem(prs, "do-phan-giai")

    khai_niem(prs, "cach-dien")
    van_de(prs, "so-sanh-dien")

    khai_niem(prs, "dien-nhan-qua")
    van_de(prs, "dien")

    khai_niem(prs, "bon-loai")

    khai_niem(prs, "z-score-masking")
    van_de(prs, "masking")

    khai_niem(prs, "mad-hampel")
    van_de(prs, "hampel")

    khai_niem(prs, "xu-ly-bat-thuong")
    van_de(prs, "tet")

    khai_niem(prs, "penalty")
    van_de(prs, "pelt")

    van_de(prs, "covid")

    khai_niem(prs, "khu-nhieu")
    khai_niem(prs, "nyquist")
    van_de(prs, "aliasing")

    khai_niem(prs, "ewma")
    khai_niem(prs, "sau-ho-loc")

    # Bản 2: bảng sáu họ bộ lọc (buoi-12/tai-lieu.md mục 4.4) thêm cột "hiểu đơn giản" như người học ghi.
    sl = moi(prs, "bang-bo-loc", "Sáu họ bộ lọc trong một bảng", "B", "Buổi 12",
             "làm feature dự báo thì chỉ chọn trong những dòng nhân quả “có”.")
    KHONG_DEM.add(len(prs.slides))
    yb = dau_than("bang-bo-loc", True) + 0.05
    co_o, khong_o, nua_o = (XANH_NHAT, XANH), (DO_NHAT, DO), ("FDF0E8", "B4541B")
    o_bang(sl, 0.6, yb, [["Họ bộ lọc", "Hiểu đơn giản", "Dùng khi", "Không dùng khi", "Nhân quả"],
                         ["trung bình trượt trailing", "trung bình k điểm gần nhất", "feature dự báo, báo cáo vận hành",
                          "cần biết đúng lúc đỉnh: trễ (k − 1) / 2", "có"],
                         ["trung bình trượt centered", "trung bình các điểm quanh nó, cả trước lẫn sau", "mô tả, tách xu hướng",
                          "mọi feature dự báo", "không"],
                         ["EWMA", "điểm mới nặng hơn điểm cũ", "dữ liệu đang chảy về, cần trễ nhỏ", "cần cắt đúng một dải tần số",
                          "có"],
                         ["Savitzky–Golay", "khớp đa thức bậc thấp trên cửa sổ quanh điểm", "giữ chiều cao đỉnh",
                          "feature dự báo, kể cả ở cuối chuỗi", "không"],
                         ["Butterworth", "cắt tần số cao theo ngưỡng; sosfilt một chiều, sosfiltfilt xuôi rồi ngược",
                          "cần bỏ đúng dải tần số cao", "bản hai chiều cho feature", "có / không"],
                         ["Kalman filter / smoother", "ước lượng tín hiệu ẩn: mức đổi dần cộng nhiễu", "có mô hình hợp; dữ liệu có lỗ",
                          "smoother cho feature", "có / không"]],
           [2.35, 3.45, 2.55, 2.55, 1.23], cao=0.66, co=12,
           to={(1, 4): co_o, (2, 4): khong_o, (3, 4): co_o, (4, 4): khong_o, (5, 4): nua_o, (6, 4): nua_o})
    chu(sl, 0.6, yb + 4.75, 12.13, 0.7, "“Có / không”: bản một chiều (sosfilt, Kalman filter) nhân quả, bản hai chiều thì không. Kalman "
        "filter chỉ nhân quả khi tham số ước lượng trên phần học rồi cố định; khớp lại trên cả chuỗi thì quá khứ đổi tới 1,134.",
        co=12, mau=MUTED)

    van_de(prs, "bo-loc")

    khai_niem(prs, "kiem-nhan-qua")
    van_de(prs, "loc-tuong-lai")
    van_de(prs, "muc-tieu-lam-tron")

    van_de(prs, "ro-ri")

    van_de(prs, "ngoai-sinh")

    # ===== C. Bảng tra, hay nhầm, từ điển =====
    mo_phan(prs, "C", "Gom lại để tra nhanh khi làm thật, kèm từ điển Việt – Anh để đọc tài liệu gốc.")
    cot = [("Dấu hiệu", 3.9, DO), ("Kiểm bằng", 3.6, LAM), ("Cách sửa", 3.63, XANH), ("Buổi", 1.0, MUTED)]
    bang_tra = [
        ("Bảng tra 1/3: thời gian, biểu đồ, biến đổi", [
            ("Giờ = 0 rạng sáng CN tháng 3", "In 00:00–05:00 ngày đổi giờ", "Gắn múi giờ → UTC rồi gộp", "3"),
            ("Nóng nhất lúc 20h", "Giờ nóng nhất trung bình", "Mọi nguồn về UTC", "3, 10"),
            ("“Không có mùa vụ tuần”", "Heatmap giờ × thứ, ACF 168", "Vẽ đủ bộ biểu đồ", "4"),
            ("Giờ thiếu hiện thành 0", "Đếm NaN trên lưới đủ", "sum(min_count=1)", "4"),
            ("Tháng 2 sụt năm nào cũng vậy", "Tổng tháng vs trung bình ngày", "Chia số ngày", "5"),
            ("Data must be positive", "y.min()", "Yeo-Johnson", "5"),
            ("Tổng dự báo thấp hơn thật", "So tổng dự báo với tổng thực", "Hiệu chỉnh bias", "5"),
            ("Xu hướng lõm cuối tuần", "Xu hướng trung bình theo thứ", "MSTL(24, 168)", "6")]),
        ("Bảng tra 2/3: dừng, tương quan, thiếu", [
            ("r₁ ≈ −0,5 sau sai phân", "ACF, độ lệch chuẩn trước/sau", "Bớt một lần sai phân", "7"),
            ("ADF và KPSS cùng bác bỏ", "Vẽ chuỗi, tìm cú sốc", "Tách đoạn", "7"),
            ("r = 0,97 giữa hai chuỗi lạ", "DW; r sau sai phân", "Sai phân", "8"),
            ("r nhỏ, scatter chữ U", "Vẽ scatter; MI", "CDD / HDD", "8"),
            ("Bản đồ chỉ xếp theo độ lớn", "Trọng số của PC1", "StandardScaler", "9"),
            ("Số dòng < số mốc", "So với lưới đầy đủ", "reindex", "10"),
            ("min lớn hơn max", "df.dtypes", "to_numeric(errors=\"coerce\")", "10"),
            ("Một giá trị chiếm 35%", "value_counts().head()", "NaN + cột cờ", "10")]),
        ("Bảng tra 3/3: ngoại lai, nhiễu, rò rỉ, đánh giá", [
            ("Đoạn phẳng dài", "Vẽ quanh lỗ", "Giới hạn độ dài điền", "10"),
            ("3σ không bắt được gì", "Thêm một điểm cực lớn", "MAD, Hampel", "11"),
            ("PELT ra hàng chục điểm gãy", "So trên log và mức gốc", "Lấy log trước", "11"),
            ("Chu kỳ lạ sau resample", "So phổ trước / sau", "Lọc trước khi hạ mẫu", "12"),
            ("Backtest đẹp, dùng thật tệ", "kiem_ro_ri nhiều mốc cắt", "Lag ≥ h, fit trên phần học", "13"),
            ("MAPE ra inf", "Đếm số 0 trong kỳ chấm", "WAPE, MASE", "14"),
            ("Sai số kiểm quá đẹp", "Điểm kiểm nằm giữa điểm học?", "Rolling origin", "15"),
            ("Thấy số liệu chưa về", "Độ trễ dữ liệu so với gap", "gap = độ trễ", "15")]),
    ]

    for i, (tieu, hang) in enumerate(bang_tra, 1):
        sl = moi(prs, f"bang-tra-{i}", tieu, "C")
        KHONG_DEM.add(len(prs.slides))
        bang(sl, 0.6, 1.55, cot, hang)

    sl = moi(prs, "hay-nham", "Mười chỗ hay hiểu nhầm", "C")
    KHONG_DEM.add(len(prs.slides))
    bang(sl, 0.6, 1.55, [("Hay nghĩ", 4.6, DO), ("Thật ra", 6.53, XANH), ("Buổi", 1.0, MUTED)], [
        ("Outlier là lỗi, xoá đi", "Tết là bất thường thật: giữ, ghi nhật ký sự kiện", "11"),
        ("Cắt bỏ giai đoạn COVID là an toàn", "Cắt còn 18 tháng: MAPE 18,11%, tệ hơn nội suy (8,71%)", "11"),
        ("Khoảng bootstrap = trung bình ± 1,96", "Lấy quantile 0,025 và 0,975 của vài nghìn trung bình", "2"),
        ("closed, label là hai dấu ngoặc", "closed: mốc biên thuộc khoảng nào; label: tên theo mốc đầu hay cuối", "3"),
        ("ADF dừng, KPSS không dừng → dừng quanh xu hướng", "Mâu thuẫn: vẽ chuỗi, tìm cú sốc, đổi mức", "7"),
        ("MASE so được độ khó giữa các chuỗi", "MASE chia cho naive của chính chuỗi: độ khó bị triệt tiêu", "9"),
        ("CV cao = khó dự báo", "10, 30, 10, 30: CV 0,58 mà dễ đoán; đo bằng sai số baseline", "9"),
        ("Kiểm bộ lọc = chia train / val", "Đổi vài điểm cuối rồi chạy lại: quá khứ không được đổi", "12"),
        ("MASE < 1 là thắng seasonal naive", "Mẫu số đo trên phần học; muốn biết thì chạy baseline trên cùng kỳ chấm", "14"),
        ("Chỉ cần thắng seasonal naive", "Phải thắng cả bốn baseline: trên M4 ngày, naive và drift thắng seasonal naive", "14"),
    ], cao=0.52, co=13)

    for i, (tieu, cap) in enumerate(TU_DIEN, 1):
        sl = moi(prs, f"tu-dien-{i}", tieu, "C")
        KHONG_DEM.add(len(prs.slides))
        cot_td = [("Tiếng Việt", 2.35, PHAN["C"][1]), ("English", 2.8, MUTED), ("Buổi", 0.9, MUTED)]
        bang(sl, 0.6, 1.4, cot_td, cap[:10], cao=0.52, co=13)
        bang(sl, 6.68, 1.4, cot_td, cap[10:], cao=0.52, co=13)

    sl = moi(prs, "thu-vien", "Thư viện dùng trong 15 buổi", "C")
    KHONG_DEM.add(len(prs.slides))
    bang(sl, 0.6, 1.3, [("Thư viện", 2.2, PHAN["C"][1]), ("Là gì", 3.9, MUTED), ("Hàm hay gặp", 5.0, MUTED),
                        ("Buổi", 1.03, MUTED)], [
        ("pandas", "Bảng dữ liệu theo thời gian: đọc, lọc, gộp, dời", "date_range, reindex, resample, shift, rolling, merge_asof", "1–15"),
        ("NumPy", "Tính toán trên mảng số", "quantile, log, sqrt, abs, mean", "1–15"),
        ("statsmodels", "Thống kê và chuỗi thời gian", "acf, pacf, adfuller, kpss, STL, MSTL", "6–10, 12"),
        ("SciPy", "Tính toán khoa học: phân phối, bộ lọc", "stats.boxcox, pearsonr, spearmanr, signal.welch, sosfilt", "5, 7–9, 12"),
        ("scikit-learn", "Học máy: chuẩn hoá, nén chiều, chia tập", "StandardScaler, PCA, KFold, mutual_info_regression", "8, 9, 15"),
        ("ruptures", "Tìm điểm gãy trong chuỗi", "Pelt, predict(pen=…)", "11"),
        ("Nixtla", "statsforecast (dự báo nhanh), utilsforecast (chỉ số)", "cross_validation, mase, smape", "14, 15"),
        ("tự viết", "Hàm viết trong buổi học để hiểu từng bước", "du_bao_cuon, guerrero, o_bang, kiem_ro_ri", "1–15"),
    ], cao=0.62, co=12)

    sl = moi(prs, "ly-thuyet-ham", "Lý thuyết nào, hàm nào", "C")
    KHONG_DEM.add(len(prs.slides))
    hang_lh = [
        ("Dự báo cuốn, backtest", "lọc index < gốc; cross_validation", "pandas; statsforecast", "1, 15"),
        ("Quantile", "np.quantile", "NumPy", "1–2"),
        ("Múi giờ", "tz_localize, tz_convert", "pandas", "3"),
        ("Gộp tần suất", "resample(...).sum(min_count=1)", "pandas", "3–4"),
        ("Ghép theo thời gian", "merge_asof(direction=\"backward\")", "pandas", "3, 13"),
        ("Box-Cox", "stats.boxcox, stats.yeojohnson", "SciPy", "5"),
        ("Phân rã", "seasonal_decompose, STL, MSTL", "statsmodels", "6"),
        ("Tự tương quan, dừng", "acf, pacf, adfuller, kpss", "statsmodels", "4, 7"),
        ("Tương quan", "pearsonr, spearmanr; mutual_info_regression", "SciPy; scikit-learn", "8"),
        ("Bản đồ chuỗi", "StandardScaler, PCA", "scikit-learn", "9"),
        ("Điền thiếu", "interpolate, ffill(limit=…)", "pandas", "10"),
        ("Điểm gãy", "rpt.Pelt", "ruptures", "11"),
        ("Phổ, bộ lọc", "signal.welch, sosfilt, ewm", "SciPy, pandas", "12"),
        ("Lag, rolling", "shift, rolling", "pandas", "13"),
        ("Chỉ số sai số", "mase, smape", "tự viết, utilsforecast", "14"),
    ]
    bang(sl, 0.6, 1.3, [("Lý thuyết", 3.0, PHAN["C"][1]), ("Hàm", 4.9, MUTED), ("Thư viện", 3.2, MUTED),
                        ("Buổi", 1.03, MUTED)], hang_lh, cao=0.38, co=11)

    # ===== D. Đánh giá trung thực =====
    mo_phan(prs, "D", "Tiền xử lý có giúp thật không? Chỉ đo trung thực mới biết.")

    khai_niem(prs, "phan-du")

    khai_niem(prs, "chi-so")

    khai_niem(prs, "phan-tram")
    khai_niem(prs, "mape-lech")
    khai_niem(prs, "mase")

    # Bản 2: tám chỉ số trong một bảng (buoi-14/tai-lieu.md mục 4.3–4.6), để tra lại khi chọn chỉ số.
    sl = moi(prs, "bang-chi-so", "Tám chỉ số: đo gì, ưa gì, hỏng khi nào", "D", "Buổi 14",
             "chọn chỉ số theo quyết định trước khi xem kết quả; đổi chỉ số là đổi hạng.")
    KHONG_DEM.add(len(prs.slides))
    yb = dau_than("bang-chi-so", True) + 0.05
    o_bang(sl, 0.6, yb, [["Chỉ số", "Tính bằng lời", "Ưa gì, dùng để làm gì", "Hỏng hay lệch khi"],
                         ["ME", "trung bình sai số, giữ dấu", "đo độ chệch: dương là dự báo thấp", "lệch lên, lệch xuống bù nhau"],
                         ["MAE", "trung bình độ lớn sai số", "ưa trung vị", "so các chuỗi khác đơn vị"],
                         ["RMSE", "căn của trung bình sai số bình phương", "ưa trung bình; phạt nặng sai số lớn",
                          "vài sai số lớn chi phối; khác đơn vị"],
                         ["MAPE", "trung bình |sai số| / thực tế × 100", "đọc bằng phần trăm", "thực tế bằng 0; kéo dự báo xuống thấp"],
                         ["sMAPE", "chia cho trung bình |thực tế| và |dự báo|, thang 0–200", "chỉ số của cuộc thi M4",
                          "cả hai gần 0; vẫn không đối xứng"],
                         ["WAPE", "tổng |sai số| / tổng thực tế", "chuỗi có số 0; chuỗi lớn nặng hơn", "tổng thực tế gần 0"],
                         ["MASE", "MAE chia MAE của seasonal naive trên phần học", "so giữa các chuỗi, chịu được số 0",
                          "phần học lặp hoàn hảo: mẫu số 0, trả NaN"],
                         ["RMSSE", "như MASE, nhưng dùng bình phương", "như MASE, ưa trung bình", "như MASE"]],
           [1.4, 4.1, 3.4, 3.23], cao=0.58, co=13)

    van_de(prs, "chia-ngau-nhien")


    khai_niem(prs, "kfold")

    khai_niem(prs, "rolling-origin")

    khai_niem(prs, "cua-so")
    khai_niem(prs, "ba-doan")

    khai_niem(prs, "dm")

    # Bản 2: gom mọi kiểm định của buổi 1–15 về một cách đọc (người học nhầm chiều ADF/KPSS, Ljung-Box, DM).
    sl = moi(prs, "doc-kiem-dinh", "Bảy kiểm định, một cách đọc", "D", "Buổi 2–15")
    KHONG_DEM.add(len(prs.slides))
    yb = dau_than("doc-kiem-dinh", None) + 0.05
    luoi_buoc(sl, 0.6, yb, 12.13, 1.45, [
        ("Đặt H0", "Giả định ban đầu, thường là “không có gì đặc biệt”."),
        ("Tính một con số", "Từ dữ liệu: chênh lệch, Q*, hệ số…"),
        ("Hiếm cỡ nào?", "p: nếu H0 đúng, xác suất gặp con số lệch cỡ này hoặc hơn."),
        ("Kết luận", "p < 0,05: bác bỏ H0. p ≥ 0,05: chưa đủ bằng chứng, không có nghĩa H0 đúng.")], 4, PHAN["D"][1], co=12)
    cam_o = ("FDF0E8", "B4541B")
    o_bang(sl, 0.6, yb + 1.65, [["Kiểm định", "H0: giả định ban đầu", "p < 0,05 nghĩa là", "Buổi"],
                                ["hoán vị", "hai nhóm như nhau", "chênh lệch giữa hai nhóm có thật", "2, 8"],
                                ["Ljung-Box", "chuỗi, hay phần dư, là nhiễu trắng", "còn quy luật chưa khai thác", "7, 14"],
                                ["ADF", "có random walk: không dừng", "có bằng chứng chuỗi dừng", "7"],
                                ["KPSS", "chuỗi dừng", "có bằng chứng chuỗi không dừng", "7"],
                                ["Granger", "quá khứ x không giúp dự báo y", "quá khứ x giúp dự báo y, chưa phải “gây ra”", "8"],
                                ["Jarque–Bera", "phần dư có hình chuông", "không hình chuông: khoảng theo phân phối chuẩn sai", "14"],
                                ["Diebold–Mariano", "hai mô hình chính xác như nhau", "chênh lệch sai số có thật, không do may", "15"]],
           [2.3, 4.0, 4.93, 0.9], cao=0.47, co=13, to={(3, 1): cam_o, (3, 2): cam_o, (4, 1): cam_o, (4, 2): cam_o})
    chu(sl, 0.6, 7.05, 12.13, 0.35, "ADF và KPSS có H0 ngược nhau (hai dòng cam): đọc H0 trước khi đọc p.", co=12, dam=True,
        mau=MUTED)

    # ===== E. Quy trình =====
    mo_phan(prs, "E", "Bước nào học từ dữ liệu thì phải làm lại ở mỗi cutoff.")

    sl = moi(prs, "quy-trinh", "Quy trình tiền xử lý: ba tầng", "E")
    KHONG_DEM.add(len(prs.slides))
    mau_e = PHAN["E"][1]
    tang1 = [("Nạp, ép kiểu số", "3, 10"), ("Về UTC", "3"), ("Lưới đủ, bỏ trùng", "10"),
             ("Mã trá hình ra NaN", "10"), ("Nhìn: bộ biểu đồ", "4, 6–9"), ("Nhật ký sự kiện", "11"),
             ("Điều chỉnh lịch, lạm phát", "5")]
    tang2 = [("Điền nhân quả", "10"), ("Ngoại lai: Hampel", "11"), ("Log / Box-Cox, λ tại gốc", "5"),
             ("Lọc nhân quả", "12"), ("Feature, lag ≥ h", "13"), ("Scaler", "13, 15")]

    def hang_hop(y, ds, mau_nen, mau_chu):
        n = len(ds)
        gap = 0.18
        w = (12.13 - gap * (n - 1)) / n
        for i, (t, b) in enumerate(ds):
            x = 0.6 + i * (w + gap)
            o = hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, 1.0, nen_mau=mau_nen, bo_goc=0.15)
            chu_trong(o, [[(t, 13, True, mau_chu)], [(f"buổi {b}", 10, False, mau_chu)]], le=0.05)
            if i < n - 1:
                noi(sl, x + w + 0.01, y + 0.5, x + w + gap - 0.01, y + 0.5, mau="9AA5B4", day=1.5, mui_ten=True)

    chu(sl, 0.6, 1.95, 12, 0.4, [[("1  Làm một lần trên toàn bộ dữ liệu", 16, True, INK),
                                 ("   — bước không học gì từ dữ liệu", 14, False, MUTED)]])
    hang_hop(2.35, tang1, NHAT, INK)
    hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.45, 3.55, 12.43, 1.9, vien=mau_e, dash=True, bo_goc=0.08)
    chu(sl, 0.6, 3.63, 12, 0.4, [[("2  Làm lại ở mỗi cutoff, chỉ trên lich_su", 16, True, mau_e),
                                  ("   — bước có học từ dữ liệu (buổi 15)", 14, False, MUTED)]])
    hang_hop(4.2, tang2, mau_e, TRANG)
    noi(sl, 6.67, 3.37, 6.67, 3.55, mau="9AA5B4", day=1.75, mui_ten=True)
    noi(sl, 6.67, 5.45, 6.67, 5.8, mau="9AA5B4", day=1.75, mui_ten=True)
    o = hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, 5.85, 12.13, 0.95, nen_mau=INK, bo_goc=0.2)
    chu_trong(o, [[("3  Kiểm:  ", 15, True, TRANG), ("rolling origin + gap", 15, True, TRANG), (" (15) · ", 12, False, "A9B4C4"),
                   ("MASE / WAPE trên chuỗi gốc so với seasonal naive", 15, True, TRANG), (" (12, 14) · ", 12, False, "A9B4C4"),
                   ("kiem_ro_ri", 15, True, TRANG), (" (13)", 12, False, "A9B4C4")]])

    sl = moi(prs, "nguyen-tac", "Ba nguyên tắc cho mọi bước", "E")
    KHONG_DEM.add(len(prs.slides))
    ng = [("1", "Chỉ dùng thông tin có trước cutoff", "rò rỉ là lỗi gặp ở nhiều buổi nhất"),
          ("2", "Giữ dữ liệu gốc, gắn cờ thay vì xoá", "mọi sửa đổi phải lần lại được"),
          ("3", "Phải thắng các baseline trên backtest", "luôn có seasonal naive; không thắng thì bỏ bước đó")]
    for i, (n, t, p) in enumerate(ng):
        x = 0.6 + i * 4.15
        hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.9, 3.9, 4.2, nen_mau=NHAT, bo_goc=0.06)
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, x + 0.4, 2.3, 1.0, 1.0, nen_mau=mau_e)
        chu_trong(o, n, co=32, dam=True, mau=TRANG)
        chu(sl, x + 0.4, 3.65, 3.1, 1.4, t, co=22, dam=True)
        chu(sl, x + 0.4, 5.1, 3.1, 0.8, p, co=15, mau=MUTED)

    # ===== F. Dữ liệu & phía trước =====
    mo_phan(prs, "F", "Dữ liệu thật, bẩn thật, giấy phép mở.")

    sl = moi(prs, "du-lieu", "14 bộ dữ liệu thật, mỗi bộ bẩn một kiểu", "F")
    KHONG_DEM.add(len(prs.slides))
    bo = [("UCI Household Power", "Điện một hộ, Pháp", "thiếu ghi là '?'", "phút · CC BY 4.0", "1"),
          ("UCI Bike Sharing", "Thuê xe, Washington", "thiếu 165 giờ", "giờ · CC BY 4.0", "2, 4, 7"),
          ("NYC Taxi (TLC)", "Chuyến taxi New York", "giờ naive quanh đổi giờ", "chuyến · NYC Open Data", "3"),
          ("Census · BLS · BEA", "Bán lẻ, CPI, dân số, GDP", "ô '(S)', đổi định nghĩa", "tháng · public domain",
           "5, 7, 8"),
          ("EIA-930", "Tải điện các vùng Mỹ", "cột đổi giữa năm", "giờ · public domain", "6, 8, 13, 15"),
          ("FRB G.17", "Sản lượng công nghiệp", "xu hướng, không dừng", "tháng · public domain", "7"),
          ("Open-Meteo (ERA5)", "Nhiệt độ, bản dự báo lưu", "lệch giờ nếu không tải UTC", "giờ · CC BY 4.0",
           "3, 8, 10, 13"),
          ("M4 (Monash)", "Chuỗi cuộc thi M4", "dài ngắn khác nhau", "3 tần suất · CC BY 4.0", "9, 14, 15"),
          ("Online Retail II", "Bán lẻ trực tuyến, Anh", "nhiều số 0", "hoá đơn · CC BY 4.0", "9, 13, 14"),
          ("UCI Beijing Air", "Bụi mịn 12 trạm", "thiếu khi ô nhiễm (MNAR)", "giờ · CC BY 4.0", "10"),
          ("GHCNh Nội Bài", "Trạm khí tượng Nội Bài", "9,999 km, cờ chất lượng", "giờ · CC0", "10"),
          ("Wikipedia tiếng Việt", "Lượt xem: Tết, tổng", "đỉnh Tết theo lịch âm", "ngày · CC0", "11, 13"),
          ("Eurostat", "Hành khách bay EU27", "gãy do COVID", "tháng · CC BY 4.0", "11"),
          ("UCI Appliances", "Cảm biến trong nhà", "nhiễu cảm biến", "10 phút · CC BY 4.0", "12")]
    w, h, gx, gy = 2.9, 1.2, 0.177, 0.13
    for i, (ten, la, ban, tl, b) in enumerate(bo):
        r, c = divmod(i, 4)
        x, y = 0.6 + c * (w + gx), 1.45 + r * (h + gy)
        hinh_khoi(sl, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, nen_mau=NHAT, bo_goc=0.1)
        chu(sl, x + 0.2, y + 0.1, w - 0.4, 0.3, ten, co=14, dam=True)
        chu(sl, x + 0.2, y + 0.4, w - 0.4, 0.3, la, co=11, mau=INK)
        chu(sl, x + 0.2, y + 0.64, w - 0.4, 0.3, f"bẩn: {ban}", co=11, dam=True, mau=PHAN["B"][1])
        chu(sl, x + 0.2, y + 0.9, w - 0.4, 0.25, [[(tl, 9, False, MUTED), (f"   buổi {b}", 9, True, MUTED)]])
    x, y = 0.6 + 2 * (w + gx), 1.45 + 3 * (h + gy)
    chu(sl, x, y + 0.1, 2 * w + gx, h - 0.1,
        "Mọi bộ đã xác minh giấy phép, tải kèm kiểm sha256. Không dùng FRED (cấm dùng cho ML).", co=12, mau=MUTED)

    sl = moi(prs, "tra-theo-buoi", "Tra theo buổi: mỗi buổi ở slide nào", "F")
    KHONG_DEM.add(len(prs.slides))
    TRA_THEO_BUOI.append(sl)

    sl = moi(prs, "phia-truoc", "Tiền xử lý còn tiếp, theo từng bài toán", "F")
    KHONG_DEM.add(len(prs.slides))
    moc = [("19", "Chuỗi thưa, nhiều số 0"), ("20", "Khác tần suất, số liệu sửa lại"),
           ("22", "Chuỗi → bảng hồi quy"), ("24", "Chuỗi mới (cold start)"), ("28", "Dự báo phân cấp"),
           ("29", "Cửa sổ cho deep learning"), ("41", "Pipeline point-in-time"), ("43", "Giám sát drift")]
    noi(sl, 1.5, 4.0, 11.83, 4.0, mau=VIEN, day=3)
    kc = (11.83 - 1.5) / (len(moc) - 1)
    for i, (b, t) in enumerate(moc):
        cx = 1.5 + i * kc
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, cx - 0.42, 3.58, 0.84, 0.84, nen_mau=PHAN["F"][1])
        chu_trong(o, b, co=18, dam=True, mau=TRANG)
        yy = 2.3 if i % 2 == 0 else 4.75
        chu(sl, cx - 0.8, yy, 1.6, 1.0, t, co=15, dam=True, can=PP_ALIGN.CENTER,
            doc=MSO_ANCHOR.BOTTOM if i % 2 == 0 else MSO_ANCHOR.TOP)
    chu(sl, 0.6, 6.4, 12.13, 0.5, "Số trong vòng tròn = buổi dạy", co=13, mau=MUTED, can=PP_ALIGN.CENTER)

    sl = prs.slides.add_slide(L)
    MUC.append(("tong-ket", "Năm điều mang về"))
    KHONG_DEM.add(len(prs.slides))
    nen(sl, INK)
    chu(sl, 0.9, 0.7, 11, 0.9, "Năm điều mang về", co=36, dam=True, mau=TRANG)
    bh = ["Nhìn trước, xử lý sau", "NaN không phải 0: gắn cờ, đừng xoá", "Mọi mốc thời gian về UTC, lưới đủ",
          "Chỉ dùng thông tin có trước cutoff", "Thắng mọi baseline trên rolling origin"]
    for i, (t, k) in enumerate(zip(bh, "ABBDD", strict=True)):
        y = 1.95 + i * 0.95
        o = hinh_khoi(sl, MSO_SHAPE.OVAL, 0.9, y, 0.66, 0.66, nen_mau=PHAN[k][1])
        chu_trong(o, str(i + 1), co=20, dam=True, mau=TRANG)
        chu(sl, 1.85, y, 10, 0.66, t, co=24, dam=True, mau=TRANG, doc=MSO_ANCHOR.MIDDLE)
    chen_code(prs)
    return prs


_MA_KHONG_DEM: set[str] = set()


def chen_code(prs) -> None:
    """Tạo slide code cho mỗi mục 4.x rồi dời nó tới ngay sau slide cuối cùng của mục đó."""
    global KHONG_DEM
    thu_tu = [m for m, _ in MUC]
    vi_tri = {m: i for i, m in enumerate(thu_tu)}
    _MA_KHONG_DEM.update(thu_tu[i - 1] for i in KHONG_DEM)
    neo = {}
    for c in CODE:
        ids = [i for i in PHU[c["buoi"]][c["sec"]] if i in vi_tri]
        assert ids, f"{c['ma']}: mục {c['buoi']}/{c['sec']} chưa có slide"
        neo[c["ma"]] = max(ids, key=vi_tri.get)
    for c in sorted(CODE, key=lambda c: (c["buoi"], c["sec"])):
        MUC_TIEU[c["ma"]] = c["muc"]
        code_slide(prs, c["ma"], c["tieu"], PHAN_CUA[neo[c["ma"]]], f"Buổi {c['buoi']}", c["code"], c["buoc"],
                   c["ket_qua"], c["nguon"], c["ham"], tuple(c["hinh"]) if c.get("hinh") else None)
    # sắp lại: slide code đứng ngay sau slide neo của nó
    lst = prs.slides._sldIdLst
    phan_tu = list(lst)
    ma_sang_pt = {m: phan_tu[i] for i, (m, _) in enumerate(MUC)}
    tieu_cua = dict(MUC)
    moi_thu_tu = []
    code_theo_neo: dict[str, list[str]] = {}
    for c in sorted(CODE, key=lambda c: (c["buoi"], c["sec"])):
        code_theo_neo.setdefault(neo[c["ma"]], []).append(c["ma"])
    for m in thu_tu:
        moi_thu_tu.append(m)
        moi_thu_tu += code_theo_neo.get(m, [])
    for pt in phan_tu:
        lst.remove(pt)
    for m in moi_thu_tu:
        lst.append(ma_sang_pt[m])
    MUC[:] = [(m, tieu_cua[m]) for m in moi_thu_tu]
    so = {m: i for i, m in enumerate(moi_thu_tu, 1)}
    KHONG_DEM = {so[m] for m in moi_thu_tu if m.startswith("code-") or m in _MA_KHONG_DEM}


# ---------- độ phủ buổi → slide ----------

def kiem_phu() -> dict[int, list[int]]:
    """Mọi mục 4.x trong buoi-NN/tai-lieu.md phải có trong PHU và trỏ tới slide có thật. Trả {buổi: [số slide]}."""
    so = {ma: i for i, (ma, _) in enumerate(MUC, 1)}
    loi, ra = [], {}
    for b in range(1, 16):
        muc = re.findall(r"^### (4\.\d)", (GOC / f"buoi-{b:02d}" / "tai-lieu.md").read_text(encoding="utf-8"), re.M)
        for m in muc:
            ids = PHU.get(b, {}).get(m)
            if not ids:
                loi.append(f"buổi {b} mục {m} chưa có slide")
                continue
            loi += [f"buổi {b} mục {m}: không có slide '{i}'" for i in ids if i not in so]
        ra[b] = sorted({so[i] for ids in PHU.get(b, {}).values() for i in ids if i in so}
                       | {so[m] for m, bb in THEM_TRA.items() if bb == b and m in so})
    if loi:
        sys.exit("Thiếu độ phủ:\n  " + "\n  ".join(loi))
    return ra


def ve_tra_theo_buoi(phu: dict[int, list[int]]) -> None:
    ten = {1: "Forecasting là gì", 2: "Xác suất, thống kê", 3: "Dữ liệu thời gian", 4: "Đọc biểu đồ",
           5: "Biến đổi, điều chỉnh", 6: "Phân rã", 7: "Tự tương quan, dừng", 8: "Tương quan giữa chuỗi",
           9: "Đặc trưng, độ khó", 10: "Làm sạch, dữ liệu thiếu", 11: "Ngoại lai, điểm gãy", 12: "Khử nhiễu, tần số",
           13: "Feature, chống rò rỉ", 14: "Baseline, chỉ số", 15: "Backtesting"}
    sl = TRA_THEO_BUOI[0]
    cot = [("Buổi", 0.75, PHAN["F"][1]), ("Chủ đề", 2.45, MUTED), ("Slide", 2.85, MUTED)]
    hang = [(str(b), ten[b], ", ".join(map(str, phu[b]))) for b in range(1, 16)]
    bang(sl, 0.6, 1.4, cot, hang[:8], cao=0.62, co=13)
    bang(sl, 6.68, 1.4, cot, hang[8:], cao=0.62, co=13)


# ---------- ghi chú từ bài đọc kèm ----------

def doc_doc_kem() -> dict[str, tuple[int, str, str]]:
    """Đọc doc-kem.md → {mã: (số, tiêu đề, thân bài dạng chữ thường)}."""
    if not DOC_KEM.exists():
        return {}
    ra: dict[str, tuple[int, str, str]] = {}
    phan = re.split(r"^## ", DOC_KEM.read_text(encoding="utf-8"), flags=re.M)[1:]
    for p in phan:
        dau, _, than = p.partition("\n")
        m = re.match(r"(\d+)\.\s+(.*)", dau.strip())
        ma = re.search(r"<!--\s*ma:\s*([\w-]+)\s*-->", than)
        if not (m and ma):
            continue
        than = re.sub(r"<!--.*?-->", "", than)
        than = re.sub(r"^```\w*\n?", "", than, flags=re.M)
        than = than.replace("**", "").replace("`", "")
        than = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])", r"\1", than)  # *nghiêng*
        than = re.sub(r"^> ?", "", than, flags=re.M).strip()
        ra[ma.group(1)] = (int(m.group(1)), m.group(2).strip(), than)
    return ra


def doc_loi_noi() -> dict[str, str]:
    """Đọc loi-noi.md → {mã: lời thuyết trình}. Mỗi slide một mục "## <mã>"."""
    phan = re.split(r"^## ", LOI_NOI.read_text(encoding="utf-8"), flags=re.M)[1:]
    return {p.partition("\n")[0].strip(): p.partition("\n")[2].strip() for p in phan}


def gan_ghi_chu(prs) -> None:
    """Ghi chú người nói = lời thuyết trình (loi-noi.md); kiểm doc-kem.md khớp số và tiêu đề."""
    noi, kem = doc_loi_noi(), doc_doc_kem()
    thieu = [f"  loi-noi.md thiếu slide {i} ({ma}): {tieu}" for i, (ma, tieu) in enumerate(MUC, 1) if ma not in noi]
    thua = [f"  loi-noi.md có mục không ứng với slide nào: {m}" for m in noi if m not in dict(MUC)]
    if thieu or thua:
        sys.exit("\n".join(thieu + thua))
    loi = []
    for i, ((ma, tieu), sl) in enumerate(zip(MUC, prs.slides, strict=True), 1):
        sl.notes_slide.notes_text_frame.text = noi[ma]
        if ma not in kem:
            loi.append(f"  doc-kem.md thiếu mục cho slide {i} ({ma}): {tieu}")
        elif kem[ma][:2] != (i, tieu):
            loi.append(f"  doc-kem.md lệch ở {ma}: có '{kem[ma][0]}. {kem[ma][1]}', cần '{i}. {tieu}' (chạy --doc-kem)")
    print("\n".join(loi) if loi else "  ghi chú: đủ lời thuyết trình; doc-kem.md khớp số và tiêu đề")


def danh_so_doc_kem() -> None:
    """Xếp lại các mục của doc-kem.md theo thứ tự slide, đánh số và đặt tiêu đề đúng slide (giữ nguyên thân bài)."""
    van = DOC_KEM.read_text(encoding="utf-8")
    dau, *phan = re.split(r"^(?=## )", van, flags=re.M)
    theo_ma = {}
    for p in phan:
        m = re.search(r"<!--\s*ma:\s*([\w-]+)\s*-->", p)
        assert m, f"mục doc-kem không có mã: {p[:60]}"
        theo_ma[m.group(1)] = p.partition("\n")[2].rstrip("\n") + "\n\n"
    thieu = [ma for ma, _ in MUC if ma not in theo_ma]
    if thieu:
        sys.exit("doc-kem.md thiếu mục: " + ", ".join(thieu))
    DOC_KEM.write_text(dau + "".join(f"## {i}. {t}\n{theo_ma[ma]}" for i, (ma, t) in enumerate(MUC, 1)).rstrip("\n") + "\n",
                       encoding="utf-8")
    print(f"  doc-kem.md: đánh số lại {len(MUC)} mục")


def kiem_cong_thuc() -> None:
    co = dict(MUC)
    loi = [f"  CONG_THUC có '{m}' mà không có slide" for m in CONG_THUC if m not in co]
    loi += [f"  CT_CODE có '{m}' mà không có slide code" for m in CT_CODE if m not in co]
    loi += [f"  VAN_DE có '{m}' mà không có slide" for m in VAN_DE if m not in co]
    loi += [f"  VAN_DE dài {len(v)} ký tự (> 95, dễ xuống dòng): {m}" for m, v in VAN_DE.items() if len(v) > 95]
    if loi:
        sys.exit("\n".join(loi))


def dem_chu(prs) -> None:
    for i, sl in enumerate(prs.slides, 1):
        if i in KHONG_DEM:
            continue
        n = sum(len(sh.text_frame.text.split()) for sh in sl.shapes
                if sh.has_text_frame and not sh.text_frame.text.startswith("Tiếng Anh:"))
        if n > GIOI_HAN_CHU:
            print(f"  cảnh báo: slide {i} có {n} âm tiết (> {GIOI_HAN_CHU})")


if __name__ == "__main__":
    prs = xay()
    ve_tra_theo_buoi(kiem_phu())
    if "--muc-luc" in sys.argv:
        for i, (ma, tieu) in enumerate(MUC, 1):
            print(f"## {i}. {tieu}\n<!-- ma: {ma} -->\n")
        sys.exit(0)
    kiem_cong_thuc()
    if "--doc-kem" in sys.argv:
        danh_so_doc_kem()
    gan_ghi_chu(prs)
    dem_chu(prs)
    prs.save(RA)
    print(f"{RA.relative_to(GOC)}: {len(prs.slides)} slide")
