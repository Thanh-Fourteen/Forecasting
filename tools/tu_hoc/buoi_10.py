"""Nội dung tự học Buổi 10 — Làm sạch và dữ liệu thiếu. Sinh: python tools/tu_hoc/sinh.py 10 --chay"""

DU_Y = {"4.1": 1, "4.2": 2, "4.3": 3, "4.4": 4, "4.5": 5, "4.6": 6, "BT1": 7, "BT2": 7, "BT3": 7}

# hình minh hoạ khái niệm: {tên hộp: {doc: cách đọc 1–2 câu, sau: mốc chèn trong tai-lieu.md (None = chỉ notebook), ve: code}}
HINH = {
    "thiếu mốc / thiếu giá trị": {
        "doc": 'Trục ngang là sáu mốc 30 phút. Chấm xanh là có số, dấu x đỏ là dòng có mặt nhưng ô rỗng (`isna()` thấy), '
               'khung cam là mốc không có dòng nào: chỉ dựng lưới rồi `reindex` mới thấy nó.',
        "sau": '**Đọc bảng.** `isna()` báo 1 ô thiếu (02:00).', "ve": r'''
ax.plot([0, 1, 3, 5], [25, 25, 26, 26], "o", color="tab:blue", label="có số")
ax.plot(4, 25.5, "x", color="tab:red", ms=9, mew=2, label="có dòng, ô NaN: isna() thấy")
ax.add_patch(plt.Rectangle((1.65, 24.4), 0.7, 2.2, fill=False, ls="--", ec="tab:orange", lw=1.2))
ax.text(2, 25.5, "không có\ndòng nào", ha="center", va="center", fontsize=7, color="tab:orange")
ax.set_xticks(range(6), ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30"])
ax.set(ylim=(24, 27.4), ylabel="°C", title="isna() đếm 1 ô thiếu; lưới đầy đủ lộ ra 2")
ax.legend(fontsize=6, loc="upper left", ncol=2, frameon=False)
'''},
    "MCAR / MAR / MNAR": {
        "doc": 'Chấm xanh là số còn lại, chấm đỏ là số bị mất (số minh hoạ). MCAR mất rải đều; MAR mất dồn trong vùng xám '
               '(mùa mưa, thứ đã đo được); MNAR mất đúng các đỉnh trên vạch đứt, nên phần còn lại thấp hơn thật.',
        "sau": '- **MNAR** (thiếu không ngẫu nhiên): việc mất phụ thuộc', "ve": r'''
fig, truc = plt.subplots(1, 3, figsize=(5.4, 1.9), sharey=True)
rng = np.random.default_rng(0)
t = np.arange(120)
y = 50 + 20 * np.sin(t / 8) + rng.normal(0, 4, t.size)
mat = {"MCAR: mất do may rủi": rng.random(t.size) < 0.2,
       "MAR: mất trong mùa mưa": (t >= 60) & (t < 100) & (rng.random(t.size) < 0.6),
       "MNAR: mất khi giá trị cao": y > 62}
for ax, (ten, m) in zip(truc, mat.items()):
    ax.plot(t[~m], y[~m], ".", ms=3, color="tab:blue")
    ax.plot(t[m], y[m], ".", ms=3, color="tab:red")
    ax.set_title(ten, fontsize=7)
    ax.set_xlabel("t")
truc[1].axvspan(60, 100, color="0.88", zorder=0)
truc[2].axhline(62, color="k", ls="--", lw=0.8)
truc[0].set_ylabel("giá trị")
fig.suptitle("Chỉ MNAR mất có hệ thống phần cao: số còn lại bị lệch xuống", fontsize=8, y=1.07)
'''},
    "cảm biến đứng yên (stuck sensor)": {
        "doc": 'Trục ngang là giờ; xanh là nhiệt độ thật, cam là số ghi được (số minh hoạ). Trái: thật đổi chưa tới 1 °C, ghi '
               'tới 1 °C nên đứng yên, không phải hỏng. Phải: thật đổi vài độ mà số ghi vẫn đứng yên: cảm biến kẹt.',
        "sau": 'Nhưng đặt ngưỡng "đứng yên" 12 giờ thì có tới 24 đoạn', "ve": r'''
fig, (a, b) = plt.subplots(1, 2, figsize=(5.4, 1.9), sharex=True)
gio = np.linspace(0, 12, 49)
dem = 25.6 + 0.8 * gio / 12
a.plot(gio, dem, color="tab:blue", label="thật")
a.step(gio, np.round(dem), where="mid", color="tab:orange", label="ghi được")
a.set(ylim=(24.5, 27.5), ylabel="°C", xlabel="giờ")
a.set_title("đêm, ghi tới 1 °C: làm tròn", fontsize=7)
ngay = 24 + 6 * np.sin(np.pi * gio / 12)
b.plot(gio, ngay, color="tab:blue")
b.plot(gio, np.full(gio.size, 26.0), color="tab:orange")
b.set(ylim=(23, 31), xlabel="giờ")
b.set_title("ngày, ghi tới 0,1 °C: kẹt", fontsize=7)
a.legend(fontsize=6, frameon=False)
fig.suptitle("Một đoạn phẳng chưa chắc là hỏng: xét độ phân giải trước", fontsize=8, y=1.06)
'''},
    "điền dữ liệu (imputation)": {
        "doc": 'Trục ngang là sáu giờ liền, đường đen là giá trị thật, hai ô giữa bị thiếu. `ffill` giữ 23, tuyến tính nối '
               'thẳng; mùa vụ và hàng xóm mang theo hình dạng nên bám sát đỉnh thật.',
        "sau": '**Đọc bảng.** Lỗ này nằm đúng lúc nhiệt độ lên đỉnh.', "ve": r'''
thieu = pd.Series([21, 23, np.nan, np.nan, 27, 25.0])
hom_qua = pd.Series([20, 22, 25, 27, 26, 24.0])
ax.plot(range(6), [21, 23, 26, 28, 27, 25], "k-o", ms=3, lw=1.5, label="thật")
cach = {"ffill": thieu.ffill(), "tuyến tính": thieu.interpolate(),
        "spline": thieu.interpolate(method="spline", order=3),
        "mùa vụ (hôm qua)": thieu.fillna(hom_qua), "hàng xóm + 1": thieu.fillna(hom_qua + 1)}
for (ten, z), dich in zip(cach.items(), (-0.12, -0.06, 0, 0.06, 0.12)):
    ax.plot(np.array([1, 2, 3, 4]) + dich, z[1:5], "o--", ms=3, lw=0.8, label=ten)
ax.axvspan(1.5, 3.5, color="0.92", zorder=0)
ax.set(xlabel="giờ", ylabel="°C", ylim=(20, 29.5), title="Lỗ trên đỉnh: chỉ cách mang hình dạng mới điền trúng")
ax.legend(fontsize=6, ncol=2, loc="lower right", frameon=False)
'''},
    "nhân quả (cách điền)": {
        "doc": 'Vạch đứt là mốc cắt: bên trái đã biết, bên phải là tương lai. `ffill` (vuông xanh) chỉ nhìn quá khứ; tuyến '
               'tính (thoi đỏ) điền 25 nhờ số 30 bên phải vạch, tức là dùng tương lai.',
        "sau": '- Tuyến tính điền **25** khi có số 30 phía sau.', "ve": r'''
ax.plot([1, 3], [20, 30], "ko", ms=6)
ax.plot(2, 20, "s", color="tab:green", ms=7, label="ffill = 20 (chỉ nhìn quá khứ)")
ax.plot(2, 25, "D", color="tab:red", ms=6, label="tuyến tính = 25 (nhìn cả số 30)")
ax.plot([1, 3], [20, 30], color="tab:red", lw=0.8, ls=":")
ax.axvline(2.3, color="0.4", ls="--")
ax.text(2.35, 21, "mốc cắt:\nbên phải là tương lai", fontsize=7, color="0.3")
ax.set(xticks=[1, 2, 3], xlim=(0.6, 3.6), ylim=(17, 33), xlabel="mốc", ylabel="giá trị",
       title="Tuyến tính nhìn qua mốc cắt; ffill thì không")
ax.legend(fontsize=6, loc="upper left", frameon=False)
'''},
    "che nhân tạo": {
        "doc": 'Cùng một chuỗi (số minh hoạ), chấm đỏ là ô bị che rồi điền lại để chấm. Trên: che rải từng điểm, ô nào cũng còn '
               'số ngay hai bên. Dưới: che một khối, mất cả một chu kỳ ngày, bài thi khó hơn hẳn.',
        "sau": '**Trực giác.** Kiểu che phải giống cách dữ liệu thật bị mất.', "ve": r'''
fig, (a, b) = plt.subplots(2, 1, figsize=(5.2, 2.1), sharex=True)
rng = np.random.default_rng(0)
t = np.arange(192)
y = 24 + 3 * np.sin(2 * np.pi * t / 48) + rng.normal(0, 0.3, t.size)
diem = rng.random(t.size) < 0.1
khoi = (t >= 80) & (t < 128)
for ax, m, ten in ((a, diem, "che điểm 10%"), (b, khoi, "che khối 48 bước")):
    ax.plot(t, y, color="0.7", lw=0.8)
    ax.plot(t[m], y[m], ".", color="tab:red", ms=4)
    ax.set_ylabel(ten, rotation=0, ha="right", va="center", fontsize=7)
    ax.set_yticks([])
b.set_xlabel("bước 30 phút")
a.set_title("Che điểm còn hàng xóm sát bên; che khối xoá cả một nhịp ngày")
'''},
}


def soan(nb) -> None:
    nb.md(r"""# Buổi 10 — Làm sạch và dữ liệu thiếu

**Một câu:** trước khi điền chỗ thiếu, phải tìm cho đủ chỗ thiếu (kể cả dòng không tồn tại và số trông như số đo mà không phải), hiểu
**vì sao** nó mất, chấm cách điền trên cả lỗ ngắn lẫn lỗ dài, và chỉ điền lỗ ngắn bằng cách không nhìn tương lai.

Tình huống: nhiệt độ trạm khí tượng sân bay Nội Bài năm 2024, mỗi 30 phút một mốc, cùng bụi mịn 12 trạm Bắc Kinh. `isna()` báo "gần như
đủ". Thật ra thiếu bao nhiêu, cái gì đang giả làm số đo, và nên lấp thế nào?

| Phần | Câu hỏi |
|---|---|
| 1 | Vì sao `isna()` báo gần đủ mà dữ liệu vẫn thủng? |
| 2 | Số bị mất vì lý do gì, và lý do đó có làm lệch kết quả không? |
| 3 | Những con số nào không phải số đo? |
| 4 | Bảy cách điền: cách nào hợp lỗ nào? |
| 5 | Chấm cách điền thế nào cho trung thực? |
| 6 | Làm sạch thế nào để không rò rỉ tương lai? |""")

    nb.md(r"""## 0. Dữ liệu""")
    nb.du_lieu()
    nb.py(r"""import io
import warnings
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents

warnings.simplefilter("ignore")
COT_DO = ["temperature", "dew_point_temperature", "relative_humidity", "visibility", "wind_speed"]

goc = pd.read_parquet(lay("ghcnh-noi-bai-2024"))            # tệp thô, giữ nguyên kiểu dữ liệu (phần 3)
tho = pd.DataFrame(index=pd.DatetimeIndex(pd.to_datetime(goc["DATE"]), name="thoi_gian"))
for cot in COT_DO:
    tho[cot] = pd.to_numeric(goc[cot], errors="coerce").to_numpy()             # ép kiểu số
    tho[f"ma_{cot}"] = goc[f"{cot}_Quality_Code"].astype("string").fillna("").to_numpy()   # cờ chất lượng
tho = tho.sort_index()

om = pd.read_csv(lay("open-meteo-ha-noi-2023-2024"), skiprows=3, index_col="time", parse_dates=True)
hx = om["temperature_2m (°C)"]                              # "trạm hàng xóm": nhiệt độ mô hình cho Hà Nội, giờ UTC

bk_tho = {}                                                  # zip chứa zip chứa 12 CSV, mỗi trạm một tệp
with zipfile.ZipFile(lay("uci-beijing-air")) as z:
    with zipfile.ZipFile(io.BytesIO(z.read("PRSA2017_Data_20130301-20170228.zip"))) as z2:
        for ten in sorted(t for t in z2.namelist() if t.endswith(".csv")):
            bk_tho[ten.split("/")[-1].split("_")[2]] = pd.read_csv(z2.open(ten))
bk = pd.DataFrame({tram: pd.Series(d["PM2.5"].to_numpy(), index=pd.to_datetime(d[["year", "month", "day", "hour"]]))
                   for tram, d in bk_tho.items()}).sort_index()

print(f"Nội Bài: {len(tho):,} dòng, {goc.shape[1]} cột | Open-Meteo: {len(hx):,} giờ | Bắc Kinh: {bk.shape[0]:,} giờ × {bk.shape[1]} trạm")""")

    # ---------------------------------------------------------------- 1
    nb.khai_niem("thiếu mốc / thiếu giá trị", "missing timestamp / missing value",
                 "thiếu mốc là cả dòng không tồn tại; thiếu giá trị là có dòng nhưng ô rỗng (NaN).",
                 "tệp đo mỗi 30 phút mà không có dòng 01:00 là thiếu mốc; dòng 02:00 có mặt nhưng nhiệt độ NaN là thiếu giá trị.",
                 "`isna()` chỉ thấy loại thứ hai; không dựng lưới thì mô hình tưởng dữ liệu liền mạch.")
    nb.khai_niem("lỗ hổng, độ dài lỗ", "gap, gap length",
                 "một đoạn liền các mốc không có số; độ dài là số bước của đoạn đó.",
                 "10:00, 10:30, 11:00 đều NaN, 09:30 và 11:30 có số: một lỗ dài 3 bước (1,5 giờ).",
                 "quyết định lấp hay để trống: lỗ một bước gần như đoán được, lỗ hai ngày thì không.")
    nb.md(r"""## 1. `isna()` không thấy dòng không tồn tại: dựng lưới trước mọi việc

**Vấn đề.** Lệnh đầu tiên ai cũng chạy là `df.isna().sum()`. Nó chỉ đếm ô rỗng trong những dòng **có mặt**.

**Lý do.** Năm dòng 00:00, 00:30, 01:30, 02:00 (NaN), 02:30: `isna()` báo 1, nhưng mốc 01:00 không có dòng nào. Dựng đủ mọi mốc rồi
`reindex` thì mốc đó hiện ra thành NaN. `reindex` báo lỗi nếu có hai dòng cùng thời điểm, nên kiểm mốc trùng trước.

**Kết quả.**""")
    nb.py(r"""bang = pd.Series([25, 25, 26, np.nan, 26],
                 index=pd.to_datetime(["2024-01-01 00:00", "2024-01-01 00:30", "2024-01-01 01:30", "2024-01-01 02:00", "2024-01-01 02:30"]))
print("ví dụ tay: isna()", bang.isna().sum(), "| sau reindex lên lưới", bang.reindex(pd.date_range(bang.index.min(), bang.index.max(), freq="30min")).isna().sum())

luoi = pd.date_range(tho.index.min(), tho.index.max(), freq="30min")
print(f"mốc trùng {tho.index.duplicated().sum()} | mốc trên lưới {len(luoi):,} | dòng có {len(tho):,} | "
      f"thiếu mốc {len(luoi.difference(tho.index))} | isna() trên 5 cột đo {tho[COT_DO].isna().sum().sum()}")


def do_dai_lo(y):
    # độ dài (số bước) của từng đoạn NaN liền nhau
    thieu = y.isna()
    nhom = (thieu != thieu.shift()).cumsum()[thieu]
    return nhom.groupby(nhom).size().reset_index(drop=True)


y = tho["temperature"].reindex(luoi)                        # chuỗi chính, trên lưới đầy đủ
dai = do_dai_lo(y)
print(f"nhiệt độ: {len(dai)} lỗ, {(dai == 1).mean():.1%} dài 1 bước, dài nhất {dai.max()} bước = {dai.max() / 2:g} giờ")

thang = pd.Series(1, index=luoi.difference(tho.index)).resample("MS").sum()
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 2.8))
a1.bar(thang.index.month, thang.to_numpy())
a1.set(xlabel="tháng 2024", ylabel="số mốc không có dòng", title="Thiếu mốc dồn vào vài tháng")
a2.hist(dai, bins=np.arange(1, dai.max() + 2) - 0.5, color="tab:orange")
a2.set(xlabel="độ dài lỗ (bước 30 phút)", ylabel="số lỗ", title="Phần lớn lỗ dài một bước")
plt.show()""")
    nb.md(r"""Lưới cả năm có 17.568 mốc, tệp chỉ có 17.319 dòng: 249 mốc không hề tồn tại, trong khi `isna()` trên năm cột đo chỉ thấy 2 ô.
Thiếu mốc dồn vào vài tháng (dấu hiệu sự cố hệ thống); hai phần ba số lỗ dài một bước, lỗ dài nhất 8 giờ.

Cùng họ: doanh số 0 ngày hết hàng là **thiếu**, không phải nhu cầu bằng 0; học từ số 0 đó, mô hình dự báo thấp, nhập ít, lại hết hàng.

**Bài học.** Kiểm mốc trùng, dựng lưới đầy đủ rồi `reindex` trước mọi việc khác; đếm thiếu trên lưới, không trên tệp.""")

    # ---------------------------------------------------------------- 2
    nb.khai_niem("MCAR / MAR / MNAR", "missing completely at random / at random / not at random",
                 "ba lý do số bị mất: MCAR do may rủi; MAR do một thứ **khác đã đo được** (mùa, gió); MNAR do **chính giá trị** "
                 "bị mất.",
                 "mất mạng vài phút là MCAR; trạm hay hỏng mùa mưa là MAR; cảm biến bụi tắt khi bụi quá cao là MNAR.",
                 "biết điền được tới đâu: MCAR điền thoải mái, MAR điền được nếu dùng thứ giải thích việc mất, MNAR điền kiểu gì "
                 "cũng lệch.")
    nb.khai_niem("PM2.5", "particulate matter ≤ 2.5 µm",
                 "bụi mịn đường kính dưới 2,5 micromet, đo bằng microgam trên mét khối không khí (µg/m³).",
                 "80 µg/m³ là ô nhiễm nặng.",
                 "chuỗi thứ hai của buổi: 12 trạm đo cùng lúc nên kiểm được \"trạm mất số lúc bụi cao hay thấp\".")
    nb.md(r"""## 2. MNAR làm lệch dù điền kiểu gì — nên phải kiểm cơ chế bằng số

**Vấn đề.** Điền được hay không phụ thuộc **vì sao** số bị mất (Rubin, 1976), không phụ thuộc cách điền giỏi tới đâu.

**Lý do.** Bốn giờ PM2.5 thật 10, 20, 30, 40; cảm biến tắt khi trên 30. Ba số còn lại không cách nào cho ra 40, nên mọi cách điền đều
lệch xuống. Trên dữ liệu thật, kiểm gián tiếp: khi một trạm mất số, bụi ở các trạm **khác** cao hay thấp hơn thường lệ?

**Kết quả.**""")
    nb.py(r"""print("ví dụ tay: trung bình thật", np.mean([10, 20, 30, 40]), "| sau khi điền bằng trung bình phần còn lại", np.mean([10, 20, 30, 20]))

rng = np.random.default_rng(0)                              # mô phỏng: 5.000 điểm hình chuông, cảm biến tắt khi > 1
moc = pd.date_range("2024-01-01", periods=5000, freq="30min")
that = pd.Series(rng.normal(0, 1, 5000), index=moc)
mcar = that.mask(pd.Series(rng.random(5000) < 0.1, index=moc))
mnar = that.mask(that > 1.0)
noi = lambda s: s.interpolate(limit_direction="both")       # noqa: E731  (nội suy tuyến tính)
print(f"mô phỏng: thật {that.mean():.3f} | điền sau MCAR {noi(mcar).mean():.3f} | điền sau MNAR {noi(mnar).mean():.3f} "
      f"(mất {mnar.isna().mean():.1%})")


def bang_chung_mnar(bang, tram):
    khac = bang.drop(columns=[tram]).mean(axis=1)            # bụi trung bình 11 trạm còn lại
    thieu = bang[tram].isna()
    return (f"{tram:<9} thiếu {thieu.mean():.2%} | các trạm khác khi thiếu {khac[thieu].mean():.1f}, khi có "
            f"{khac[~thieu].mean():.1f} µg/m³ | chênh {khac[thieu].mean() / khac[~thieu].mean() - 1:+.1%}")


for tram in ["Dongsi", "Guanyuan", "Wanliu"]:
    print(bang_chung_mnar(bk, tram))

ty_le = bk.isna().groupby(bk.index.to_period("M")).mean() * 100
print(f"Bắc Kinh: thiếu trung bình {bk.isna().mean().mean():.2%}, tháng-trạm tệ nhất {ty_le.to_numpy().max():.1f}%")
fig, ax = plt.subplots(figsize=(10, 3))
anh = ax.imshow(ty_le.to_numpy().T, aspect="auto", cmap="magma_r", vmin=0, vmax=20)
ax.set_yticks(range(12), ty_le.columns, fontsize=7)
ax.set(xlabel="tháng thứ mấy từ 3/2013", title="Thiếu đi thành từng mảng theo trạm và theo tháng")
plt.colorbar(anh, ax=ax, label="% giờ thiếu")
plt.show()""")
    nb.md(r"""Mô phỏng: MNAR mất 16,2% số điểm, toàn phía cao; điền xong trung bình −0,30 thay vì −0,005, còn MCAR gần như không lệch. Dữ liệu
thật: khi Dongsi thiếu, các trạm khác còn **thấp hơn** 3,0% (hai trạm kia cũng âm): không có dấu hiệu MNAR. Và "thiếu 2,08%" che mất
những tháng một trạm mất gần nửa số giờ.

**Bài học.** Kiểm cơ chế thiếu bằng số theo cả hai chiều, đừng giả định; báo tỷ lệ thiếu theo trạm và theo tháng, không chỉ một con
số chung.""")

    # ---------------------------------------------------------------- 3
    nb.khai_niem("mã trá hình (sentinel)", "sentinel value",
                 "con số quy ước đặt vào ô dữ liệu để báo điều gì đó, không phải số đo.",
                 "tầm nhìn 9,999 km trong bản tin sân bay nghĩa là \"từ 10 km trở lên\": tầm nhìn thật có thể là 30 km.",
                 "tránh tính trung bình, xu hướng trên một con số vốn là mã.")
    nb.khai_niem("trần cảm biến", "sensor ceiling",
                 "giá trị lớn nhất cảm biến ghi được; thật có thể cao hơn.",
                 "độ ẩm dừng ở 100%: sương mù dày hay mỏng đều ghi 100.",
                 "biết chỗ nào số đo bị cắt ngọn, đừng coi đó là giá trị thật.")
    nb.khai_niem("độ phân giải", "resolution",
                 "bước nhỏ nhất giữa hai giá trị cảm biến ghi được.",
                 "nhiệt độ 25,6 → 26,4 °C, ghi tới 1 °C thành 26, 26, 26: đổi 0,8 °C mà không thấy.",
                 "đặt ngưỡng \"đứng yên\" đúng: độ phân giải thô thì đoạn lặp dài là chuyện thường.")
    nb.khai_niem("cảm biến đứng yên (stuck sensor)", "stuck sensor",
                 "cảm biến kẹt, ghi lặp một giá trị nhiều giờ liền.",
                 "26,0; 26,0; … suốt 33 giờ, qua cả ngày lẫn đêm.",
                 "loại những đoạn không phải số đo trước khi học mô hình.")
    nb.khai_niem("cờ chất lượng", "quality flag",
                 "mã nguồn dữ liệu gắn kèm mỗi số đo, nói nó qua kiểm tra hay đáng ngờ.",
                 "GHCNh: `1` qua mọi kiểm tra, `2` đáng ngờ, `3` sai; `4` chỉ mới qua kiểm giới hạn thô, không phải lỗi.",
                 "loại số sai theo chính nguồn, thay vì tự đoán.")
    nb.md(r"""## 3. Không có NaN mà số vẫn sai: mã, trần, làm tròn, kẹt, và cột số lưu dạng chữ

**Vấn đề.** Không có ô rỗng, không có lỗi nào báo ra, mà con số vẫn không phải số đo.

**Lý do.** Mỗi thủ phạm để lại dấu vết: mã là một giá trị chiếm tỷ lệ lớn bất thường; trần là cột dồn ở mép phải; độ phân giải thô là
ít giá trị khác nhau; kẹt là đoạn lặp dài hơn mức độ phân giải giải thích được. Cột số lưu dạng chữ thì `min()`/`max()` so theo thứ tự
chữ cái.

**Kết quả.**""")
    nb.py(r"""rh = goc["relative_humidity"]
print(f"tệp gốc: độ ẩm kiểu {rh.dtype} → min {rh.min()!r}, max {rh.max()!r} | sau ép kiểu: {tho['relative_humidity'].min():g} → {tho['relative_humidity'].max():g}")
print(f"tầm nhìn = 9,999 km: {(tho['visibility'] == 9.999).mean():.1%} số dòng | độ ẩm = 100%: {(tho['relative_humidity'] == 100).mean():.1%}")

t = tho["temperature"].dropna()
gia_tri = np.sort(t.unique())
print(f"nhiệt độ: {gia_tri.size} giá trị khác nhau, bước nhỏ nhất {np.diff(gia_tri).min()} °C, nguyên {(t % 1 == 0).mean():.0%}, "
      f"dải {t.min():g}–{t.max():g} °C")


def doan_mac_ket(y, toi_thieu):
    # các đoạn giá trị lặp liên tiếp dài ≥ toi_thieu bước
    v = y.dropna()
    nhom = (v != v.shift()).cumsum()
    dem = v.groupby(nhom).agg(so_buoc="size", gia_tri="first")
    dem["bat_dau"] = v.groupby(nhom).apply(lambda s: s.index[0])
    return dem[dem["so_buoc"] >= toi_thieu].sort_values("so_buoc", ascending=False).reset_index(drop=True)


for nguong in (24, 36):
    print(f"ngưỡng {nguong} bước ({nguong // 2} giờ): {len(doan_mac_ket(tho['temperature'], nguong))} đoạn đứng yên")
print(doan_mac_ket(tho["temperature"], 36).head(3).to_string(index=False))

MA_NGHI_NGO = {"2", "3", "6", "7", "f", "o"}                 # bảng 3 tài liệu GHCNh; "4" KHÔNG phải lỗi
print("mã chất lượng nhiệt độ:", tho["ma_temperature"].value_counts().to_dict())
cot_do = [c for c in goc.columns if not c.endswith(("_Measurement_Code", "_Quality_Code", "_Report_Type", "_Source_Code", "_Source_Station_ID"))]
print(f"cột rỗng hoàn toàn: {sum(goc[c].isna().all() for c in cot_do)} trên {len(cot_do)} cột")""")
    nb.md(r"""Độ ẩm trong tệp gốc là chữ nên "min" là `'100'`, "max" là `'94'`. Hơn một phần ba số dòng tầm nhìn là mã 9,999; 5,7% số dòng độ ẩm
chạm trần. Nhiệt độ chỉ có số nguyên (độ phân giải 1 °C), nên ngưỡng 12 giờ bắt tới 24 đoạn "đứng yên", phần lớn chỉ là đêm ít đổi
nhiệt; ngưỡng 18 giờ còn 2 đoạn, dài nhất 33,5 giờ đúng 26,0 °C. Cờ: 7 dòng mã `2` (loại), 9 dòng mã `4` (không phải lỗi, giữ).

**Bài học.** In kiểu và min/max ngay sau khi đọc; xem histogram tìm mã và trần; đo độ phân giải trước khi gọi đoạn lặp là hỏng; tra
bảng cờ của nguồn. Đổi số hỏng thành NaN kèm cờ, đừng xoá cả dòng khi chỉ một cột có vấn đề.""")

    # ---------------------------------------------------------------- 4
    nb.khai_niem("điền dữ liệu (imputation)", "imputation",
                 "ước lượng rồi điền vào chỗ thiếu.",
                 "10, (thiếu), 14 → nội suy tuyến tính điền 12.",
                 "nhiều mô hình không chạy được với NaN; nhưng số điền là số đoán, không phải số đo.")
    nb.khai_niem("nhân quả (cách điền)", "causal imputation",
                 "cách điền chỉ dùng dữ liệu **trước** chỗ đang điền.",
                 "`ffill` (lấy số gần nhất phía trước) là nhân quả; nội suy hai phía nối với số phía sau nên không.",
                 "chỉ cách nhân quả mới dùng được khi dự báo thật, lúc tương lai chưa có.")
    nb.khai_niem("spline", "cubic spline",
                 "đường cong trơn bậc 3 nối qua các điểm lân cận.",
                 "21, 23, ?, ?, 27, 25 → spline điền 25,2 và 26,8, cong hơn đường thẳng.",
                 "lấp lỗ ngắn trên chuỗi rất trơn; ở lỗ dài đường cong dễ vọt lố.")
    nb.khai_niem("Kalman smoother", "Kalman smoother",
                 "khớp một mô hình chuỗi (mức đổi dần + nhịp ngày) rồi ước lượng giá trị ở ô thiếu từ cả quá khứ lẫn tương lai.",
                 "lỗ 48 giờ: mô hình biết nhịp ngày nên điền một đường lên xuống theo ngày, không phải đường phẳng.",
                 "một cách điền khá cho mọi độ dài lỗ, khi mô hình hợp với chuỗi; không nhân quả.")
    nb.md(r"""## 4. Lỗ ngắn điền kiểu gì cũng gần đúng; lỗ dài cần cách mang theo hình dạng

**Vấn đề.** Có nhiều cách lấp một lỗ; cách nào đúng tuỳ lỗ dài hay ngắn, chuỗi có nhịp ngày không, có nguồn tương quan không, và có được
nhìn tương lai không.

**Lý do.** Tuyến tính và spline chỉ biết hai đầu lỗ. Mùa vụ (cùng giờ hôm trước) và trạm hàng xóm biết thêm **hình dạng** của đoạn bị
mất. Ví dụ: hôm nay 21, 23, ?, ?, 27, 25 (thật 26, 28); hôm qua cùng giờ 20, 22, 25, 27, 26, 24; hàng xóm hôm nay y như hôm qua và luôn
thấp hơn trạm ta 1 °C.

**Kết quả.**""")
    nb.py(r"""hom_nay = pd.Series([21, 23, np.nan, np.nan, 27, 25.0])
hom_qua = pd.Series([20, 22, 25, 27, 26, 24.0])
tay = {"ffill": hom_nay.ffill(), "tuyến tính": hom_nay.interpolate(), "spline": hom_nay.interpolate(method="spline", order=3),
       "mùa vụ (hôm qua)": hom_nay.fillna(hom_qua), "hàng xóm + 1": hom_nay.fillna(hom_qua + 1)}
for ten, z in tay.items():
    print(f"{ten:<17} điền {z[2]:.2f}; {z[3]:.2f} | sai {abs(z[2] - 26):.2f}; {abs(z[3] - 28):.2f}")


# bảy cách điền, nhận chuỗi có NaN, trả chuỗi đã điền
def dien_ffill(y, **_):
    return y.ffill()                                         # nhân quả; lỗ dài thành đoạn phẳng


def dien_tuyen_tinh(y, **_):
    return y.interpolate(method="linear", limit_direction="both")          # dùng tương lai


def dien_spline(y, **_):
    return y.interpolate(method="spline", order=3, limit_direction="both")  # dùng tương lai, vọt lố ở lỗ dài


def dien_mua_vu(y, chu_ky=48, **_):
    z = y.copy()                                             # cùng giờ ngày trước, lùi tối đa 14 ngày; nhân quả
    for _ in range(14):
        z = z.where(z.notna(), z.shift(chu_ky))
    return z


def dien_trung_binh_gio(y, **_):
    gio = y.index.hour * 100 + y.index.minute                # trung bình cùng giờ của mọi ngày (cả tương lai)
    return y.fillna(y.groupby(gio).transform("mean"))


def dien_kalman(y, chu_ky=48, **_):
    kq = UnobservedComponents(y.to_numpy(float), level="local level",
                              freq_seasonal=[{"period": chu_ky, "harmonics": 2}]).fit(disp=False, maxiter=50)
    return y.fillna(pd.Series(kq.smoother_results.smoothed_forecasts[0], index=y.index))   # KHÔNG dùng fittedvalues


def dien_hang_xom(y, hang_xom=None, **_):
    x = hang_xom.reindex(y.index).interpolate(limit_direction="both")      # hồi quy y = a·x + b trên chỗ cả hai có số
    chung = y.notna() & x.notna()
    a, b = np.polyfit(x[chung].to_numpy(float), y[chung].to_numpy(float), 1)
    return y.fillna(pd.Series(a * x.to_numpy(float) + b, index=y.index))


CACH_DIEN = {"ffill": dien_ffill, "tuyến tính": dien_tuyen_tinh, "spline": dien_spline, "mùa vụ (ngày trước)": dien_mua_vu,
             "trung bình theo giờ": dien_trung_binh_gio, "Kalman smoother": dien_kalman, "hàng xóm (Open-Meteo)": dien_hang_xom}

chung = pd.concat([y.resample("h").mean(), hx], axis=1, keys=["noi_bai", "open_meteo"]).dropna()   # gộp hai mốc 30 phút thành giờ
print(f"Nội Bài × Open-Meteo: r = {chung.corr().iloc[0, 1]:.3f} trên {len(chung):,} giờ cả hai có số")""")
    nb.md(r"""Lỗ này nằm đúng lúc nhiệt độ lên đỉnh: `ffill` giữ 23 nên sai nhiều nhất (3 và 5), tuyến tính sai 1,67 và 2,33, mùa vụ sai 1 và 1,
hàng xóm trúng cả hai. Nguồn hàng xóm dùng được vì tương quan cao: Nội Bài và Open-Meteo Hà Nội có $r$ = 0,976.

| Cách | Hợp với | Tránh khi | Nhân quả |
|---|---|---|---|
| `ffill` | lỗ rất ngắn; chuỗi bậc thang (giá niêm yết) | lỗ dài: đoạn phẳng giả | có |
| tuyến tính, spline | lỗ ngắn, chuỗi trơn, khi được nhìn cả hai phía | lỗ dài; dự báo thật | không |
| mùa vụ (ngày trước) | nhịp ngày mạnh, lỗ dài | ngày trước cũng thiếu | có |
| trung bình theo giờ | chỉ cần một giá trị "điển hình" | cần đúng diễn biến ngày đó | không |
| Kalman smoother | mọi độ dài, khi mô hình hợp chuỗi | cần nhân quả | không |
| trạm hàng xóm | nguồn tương quan cao, đo cùng lúc | hàng xóm cũng thiếu; tương quan thấp | có, nếu hệ số học từ quá khứ |

**Bài học.** Chọn cách điền theo độ dài lỗ, và luôn biết cách đó có nhìn tương lai không.""")

    # ---------------------------------------------------------------- 5
    nb.khai_niem("che nhân tạo", "artificial masking",
                 "xoá những ô đang có số rồi điền lại, để có đáp án mà chấm cách điền.",
                 "một ngày 20, 21, 23, 25, 26, 25, 23, 21: che bốn số giữa, tuyến tính nối 21 với 23 được MAE 2,75.",
                 "ô thiếu thật không có đáp án; che nhân tạo là cách duy nhất đo cách điền nào tốt.")
    nb.md(r"""## 5. Che điểm và che khối cho thứ hạng ngược nhau

**Vấn đề.** Muốn biết cách điền nào tốt thì phải có đáp án, mà ô thiếu thật thì không có.

**Lý do.** Che ô đang có số, điền lại, so với số thật. Kiểu che phải giống cách dữ liệu thật bị mất: che rải từng điểm là thi "lỗ một
bước", cảm biến chết hai ngày là bài thi khác hẳn. Nội Bài có cả hai loại lỗ, nên chấm cả hai: che ngẫu nhiên 10% số điểm, và che 5 khối
48 giờ.

**Kết quả.**""")
    nb.py(r"""def che_diem(y, ty_le=0.10, seed=0):
    rng = np.random.default_rng(seed)
    co = np.flatnonzero(y.notna().to_numpy())
    z = y.copy()
    z.iloc[rng.choice(co, size=int(len(co) * ty_le), replace=False)] = np.nan
    return z


def che_khoi(y, so_buoc=96, so_khoi=5, seed=0):
    rng = np.random.default_rng(seed)
    z = y.copy()
    for _ in range(so_khoi):
        dau = int(rng.integers(0, len(y) - so_buoc))
        z.iloc[dau:dau + so_buoc] = np.nan
    return z


def cham(that, y_che):
    o_che = that.notna() & y_che.isna()                      # chỉ chấm trên ô bị che
    return {ten: float((ham(y_che, hang_xom=hx)[o_che] - that[o_che]).abs().mean()) for ten, ham in CACH_DIEN.items()}


that = y.dropna()
bang_dien = pd.DataFrame({"che điểm 10%": cham(that, che_diem(that)), "che khối 48 giờ": cham(that, che_khoi(that))})
bang_dien["hạng điểm"] = bang_dien["che điểm 10%"].rank().astype(int)
bang_dien["hạng khối"] = bang_dien["che khối 48 giờ"].rank().astype(int)
print(bang_dien.sort_values("che điểm 10%").round(3).to_string())

che = che_khoi(that)
o_che = that.notna() & che.isna()
dau = che[o_che].index[0]
cua_so = slice(dau - pd.Timedelta("24h"), dau + pd.Timedelta("72h"))
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(that[cua_so], color="k", lw=1.6, label="thật")
for ten in ("ffill", "tuyến tính", "mùa vụ (ngày trước)", "hàng xóm (Open-Meteo)"):
    ax.plot(CACH_DIEN[ten](che, hang_xom=hx)[cua_so].where(o_che[cua_so]), lw=1.2, label=ten)
ax.axvspan(dau, dau + pd.Timedelta("48h"), color="red", alpha=0.06)
ax.set(ylabel="°C", title="Một lỗ 48 giờ: ffill và tuyến tính thành đường phẳng, hàng xóm giữ nhịp ngày")
ax.legend(fontsize=8, ncol=3)
plt.show()""")
    nb.md(r"""Chỉ đổi kiểu che mà thứ hạng đảo: tuyến tính hạng 1 ở lỗ ngắn (MAE 0,291 °C) nhưng hạng 5 ở lỗ 48 giờ (2,171); hàng xóm đi ngược lại,
hạng 5 lên hạng 1. Spline tệ nhất ở lỗ dài vì vọt lố. Trong hình, `ffill` và tuyến tính thành đường phẳng suốt hai ngày; mô hình học
trên đó sẽ tin nhiệt độ có lúc đứng yên hai ngày liền.

**Bài học.** Che theo đúng những kiểu lỗ dữ liệu thật có, và báo cả hai: cách tốt nhất ở lỗ ngắn có thể tệ ở lỗ dài.""")

    # ---------------------------------------------------------------- 6
    nb.khai_niem("cột cờ", "flag column",
                 "cột thêm vào để đánh dấu ô nào đã bị điền, bị loại, hay cố ý để trống.",
                 "`da_dien = True` ở ô 14:30: số 26 ở đó là số điền, không phải số đo.",
                 "hạ trọng số hoặc bỏ ô đã điền khỏi tập chấm; trả lời \"số này từ đâu ra\" sáu tháng sau.")
    nb.khai_niem("pipeline", "pipeline",
                 "chuỗi bước chạy tự động từ dữ liệu thô tới dữ liệu sạch.",
                 "đọc → ép kiểu → lưới → cờ → điền lỗ ngắn → báo cáo, chạy lại một lệnh là ra cùng kết quả.",
                 "làm sạch lặp lại được và kiểm được bằng test, thay vì sửa tay từng ô.")
    nb.khai_niem("SAITS, BRITS", "SAITS, BRITS",
                 "hai mô hình deep learning điền dữ liệu thiếu, học từ nhiều chuỗi cùng lúc (thư viện PyPOTS).",
                 "trên bộ so sánh TSI-Bench, chúng có lợi khi có hàng chục chuỗi tương quan và thiếu nhiều.",
                 "biết khi nào đáng dùng: một trạm thiếu vài phần trăm thì hồi quy theo hàng xóm đã đủ tốt.")
    nb.md(r"""## 6. Điền bằng tương lai là rò rỉ: chỉ điền lỗ ngắn, nhân quả, và xuất cột cờ

**Vấn đề.** Điền xong, backtest đẹp bất thường; hoặc chuỗi có những đoạn hai ngày được "bịa" ra mà sáu tháng sau không ai biết.

**Lý do.** Chuỗi 20, NaN, 30: `ffill` điền 20 dù có số 30 hay không; tuyến tính điền 25 **nhờ** số 30 phía sau. Nếu số 30 thuộc tập
kiểm, thông tin tập kiểm đã chảy vào tập học. Kiểm tự động: làm sạch dữ liệu đầy đủ và dữ liệu cắt tại một mốc, so phần trước mốc cắt.
Mốc cắt phải nằm **trong một lỗ**, nếu không bài kiểm im lặng.

**Kết quả.** Pipeline: đưa lên lưới, loại số bị cờ (mã chất lượng, đoạn kẹt ≥ 36 bước), đo **lại** độ dài lỗ, chỉ điền lỗ ≤ 6 bước (3 giờ)
bằng mùa vụ, xuất ba cột cờ.""")
    nb.py(r"""def lam_sach(bang, cot="temperature", gioi_han=6, mac_ket=36, cach=dien_mua_vu, dien_het=False):
    luoi_b = pd.date_range(bang.index.min(), bang.index.max(), freq="30min")
    v = bang[cot].reindex(luoi_b)
    nghi = bang[f"ma_{cot}"].reindex(luoi_b).fillna("").isin(MA_NGHI_NGO)          # cờ chất lượng của nguồn
    for _, d in doan_mac_ket(v, mac_ket).iterrows():                                 # đoạn kẹt
        nghi.loc[d["bat_dau"]:d["bat_dau"] + pd.Timedelta("30min") * (d["so_buoc"] - 1)] = True
    sach = v.where(~nghi)                                     # loại TRƯỚC rồi mới đo độ dài lỗ
    thieu = sach.isna()
    nhom = (thieu != thieu.shift()).cumsum()
    do_dai = nhom.map(nhom[thieu].value_counts()).where(thieu, 0)
    dien_duoc = thieu if dien_het else thieu & (do_dai <= gioi_han)
    ket_qua = sach.where(~dien_duoc, cach(sach, hang_xom=hx))
    return pd.DataFrame({cot: ket_qua, "da_dien": dien_duoc & ket_qua.notna(), "nghi_ngo": nghi,
                         "lo_dai_bo_trong": thieu & ~dien_duoc})


sach = lam_sach(tho)
print(f"mốc {len(sach):,} | bị loại vì nghi ngờ {sach['nghi_ngo'].sum()} | đã điền {sach['da_dien'].sum()} | "
      f"để trống có chủ ý {sach['lo_dai_bo_trong'].sum()}")


def kiem_ro_ri(ham, bang, moc_cat):
    # làm sạch trên dữ liệu đầy đủ và trên dữ liệu cắt tại moc_cat; phần trước mốc cắt phải giống hệt
    day = ham(bang).loc[:moc_cat - pd.Timedelta("30min"), "temperature"]
    cat = ham(bang.loc[:moc_cat - pd.Timedelta("30min")])["temperature"]
    lech = (day - cat).abs().max()
    return "PHÁT HIỆN RÒ RỈ" if lech > 1e-9 else "không phát hiện rò rỉ"


nho = tho.iloc[:2000].copy()
nho.iloc[1190:1210, nho.columns.get_loc("temperature")] = np.nan          # khoét một lỗ 20 bước
trong_lo, ngoai_lo = nho.index[1205], nho.index[1500]
for ten, ham in {"điền mọi lỗ bằng tuyến tính": lambda b: lam_sach(b, cach=dien_tuyen_tinh, dien_het=True),
                 "lỗ ≤ 6 bước bằng mùa vụ   ": lambda b: lam_sach(b)}.items():
    print(f"{ten}: cắt trong lỗ → {kiem_ro_ri(ham, nho, trong_lo)} | cắt chỗ liền → {kiem_ro_ri(ham, nho, ngoai_lo)}")""")
    nb.md(r"""Trên 17.568 mốc: 130 ô bị loại vì nghi ngờ, 198 ô được điền, 181 ô để trống có chủ ý. Bản điền mọi lỗ bằng tuyến tính bị bắt khi cắt
trong lỗ nhưng lọt khi cắt ở chỗ liền; bản đúng sạch ở cả hai. Loại số nghi ngờ **trước** rồi mới đo độ dài lỗ, vì biến số kẹt thành
NaN có thể nối hai lỗ ngắn thành một lỗ dài.

**Bài học.** Chia tập trước, điền bằng cách nhân quả; chỉ điền lỗ ngắn, lỗ dài để NaN; luôn xuất cột cờ cùng dữ liệu; đặt mốc cắt của
bài kiểm rò rỉ trong một lỗ.""")

    # ---------------------------------------------------------------- 7
    nb.md(r"""## 7. Bài tập về nhà — đáp số

**Bài 1 — Che theo đúng phân bố thật.** Rút độ dài lỗ từ chính phân bố độ dài lỗ của Nội Bài (phần 1), đặt vào vị trí ngẫu nhiên tới
khi che đủ 10% số điểm (seed 0):""")
    nb.py(r"""def che_theo_phan_bo(y, dai_lo, ty_le=0.10, seed=0):
    rng = np.random.default_rng(seed)
    z = y.copy()
    while z.isna().mean() < ty_le:
        d = int(rng.choice(dai_lo))
        dau = int(rng.integers(0, len(y) - d))
        z.iloc[dau:dau + d] = np.nan
    return z


bang_dien["che theo phân bố thật"] = cham(that, che_theo_phan_bo(that, dai.to_numpy()))
bang_dien["hạng thật"] = bang_dien["che theo phân bố thật"].rank().astype(int)
print(bang_dien[["hạng điểm", "hạng khối", "che theo phân bố thật", "hạng thật"]].sort_values("hạng thật").round(3).to_string())""")
    nb.md(r"""Lỗ thật phần lớn dài một bước nên thứ hạng gần với che điểm, nhưng Kalman smoother vượt lên hạng 1 (0,422) trước tuyến tính (0,435):
vài lỗ dài vài giờ đã đủ đổi thứ tự. Chấm theo phân bố thật để chọn cách cho lỗ đang có; vẫn báo che khối cho lỗ dài có thể gặp sau.

**Bài 2 — MAR có cứu được không.** Trạm Dongsi: xoá PM2.5 với xác suất 30% ở những giờ gió mạnh (`WSPM` trên tứ phân vị trên) và 3% ở
giờ khác (seed 0). Gió mạnh thổi bụi đi, nên ô bị xoá vốn là ô bụi thấp: thiếu MAR theo gió. So điền bằng trung bình chung với điền bằng
trung bình trong cùng nhóm gió:""")
    nb.py(r"""d = bk_tho["Dongsi"]
pm = pd.Series(d["PM2.5"].to_numpy(), index=bk.index)
gio_gio = pd.Series(d["WSPM"].to_numpy(), index=bk.index)
nhom_gio = pd.qcut(gio_gio, 4, labels=False)                 # 4 nhóm gió, nhóm 3 = mạnh nhất
rng = np.random.default_rng(0)
xoa = pm.notna() & gio_gio.notna() & (rng.random(len(pm)) < np.where(nhom_gio == 3, 0.30, 0.03))
con = pm.mask(xoa)
dien = {"trung bình chung (không dùng gió)": con.fillna(con.mean()),
        "trung bình theo nhóm gió": con.fillna(con.groupby(nhom_gio).transform("mean"))}
print(f"xoá {xoa.sum():,} giờ | PM2.5 thật ở giờ bị xoá {pm[xoa].mean():.1f}, ở giờ còn lại {pm[~xoa].mean():.1f} µg/m³")
for ten, z in dien.items():
    print(f"{ten:<34} MAE {(z[xoa] - pm[xoa]).abs().mean():.1f} | lệch trung bình {(z[xoa] - pm[xoa]).mean():+.1f} µg/m³")""")
    nb.md(r"""Giờ bị xoá có bụi thật thấp hơn hẳn giờ còn lại (60,5 so với 88,8 µg/m³). Điền bằng trung bình chung lệch lên +28,4 µg/m³;
điền theo nhóm gió gần như hết lệch (−1,9) và MAE giảm từ 62,4 xuống 47,1. MAR cứu được, với điều kiện cách điền dùng đúng thứ giải
thích việc mất.

**Bài 3 — Giá của việc điền sai.** Dự báo naive 1 giờ tới (2 bước 30 phút) trên chuỗi đã làm sạch theo hai cách: (a) nội suy mọi lỗ, (b)
chỉ điền lỗ ≤ 3 giờ. Chấm trên mọi giờ có số, rồi chỉ trên giờ mà cả số thật lẫn số dùng để dự báo đều không phải số điền:""")
    nb.py(r"""ban = {"(a) nội suy mọi lỗ": lam_sach(tho, cach=dien_tuyen_tinh, dien_het=True), "(b) chỉ điền lỗ ≤ 3 giờ": sach}
for ten, s in ban.items():
    v, dien_o = s["temperature"], s["da_dien"]
    sai = (v - v.shift(2)).abs()                              # naive: dự báo = giá trị 1 giờ trước
    that_su = ~dien_o & ~dien_o.shift(2, fill_value=True)
    print(f"{ten:<24} MAE mọi giờ có số {sai.mean():.3f} ({sai.notna().sum():,} điểm) | "
          f"chỉ giờ không điền {sai[that_su].mean():.3f} ({sai[that_su].notna().sum():,} điểm)")""")
    nb.md(r"""Chấm trên mọi giờ, (a) trông tốt nhất (0,579) vì đoạn nội suy thẳng rất dễ đoán, (b) trông tệ hơn (0,602) vì số điền mùa vụ nhảy bậc
ở mép lỗ. Chấm trên giờ không có số điền, hai cách **bằng nhau** (0,585): điền chỉ làm điểm số đổi, không làm dự báo tốt lên. Luôn bỏ ô
đã điền khỏi tập chấm, nhờ cột `da_dien`.

## Tự kiểm

- [ ] Tệp đo mỗi giờ 00:00–23:00 có 21 dòng, 1 dòng có ô NaN: thiếu mấy giờ, `isna()` báo mấy?
- [ ] Phân biệt MCAR, MAR, MNAR bằng một ví dụ cửa hàng; nói cơ chế nào điền kiểu gì cũng lệch.
- [ ] Kể bốn thứ trông như số đo mà không phải, và dấu vết của từng thứ.
- [ ] Giải thích vì sao ngưỡng "đứng yên" phải đặt theo độ phân giải.
- [ ] Giải thích vì sao tuyến tính hạng 1 khi che điểm mà hạng 5 khi che khối.
- [ ] Nói vì sao mốc cắt của bài kiểm rò rỉ phải nằm trong một lỗ.""")
