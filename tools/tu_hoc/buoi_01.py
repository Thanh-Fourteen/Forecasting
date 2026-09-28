"""Nội dung tự học buổi 1 — Forecasting là gì. Sinh: python tools/tu_hoc/sinh.py 1 --chay"""

DU_Y = {"4.1": 1, "4.2": 1, "4.3": 2, "4.4": 4, "4.5": 5, "4.6": 6,
        "BT1": "phiếu cho tình huống của chính người học — không có lời giải chung", "BT2": 7, "BT3": 7}


# hình minh hoạ khái niệm: {tên hộp: {doc: cách đọc 1–2 câu, sau: mốc chèn trong tai-lieu.md (None = chỉ notebook), ve: code}}
HINH = {
    "tầm dự báo, h": {"doc": 'Trục ngang là giờ tính từ gốc dự báo (vạch cam); đường xám là số đo đã biết. Dải xanh là 168 giờ phải dự báo, tất cả nằm bên phải gốc.',
        "sau": '- $h$: số giờ tính từ $T$.', "ve": r'''
t = np.arange(-72, 169)
y = 1 + 0.5 * np.sin(2 * np.pi * t / 24) + np.random.default_rng(0).normal(0, 0.1, t.size)
ax.plot(t[t <= 0], y[t <= 0], color="0.3", lw=1, label="đã biết")
ax.axvspan(0, 168, color="tab:blue", alpha=0.12, label="tầm dự báo: h = 1…168")
ax.axvline(0, color="tab:orange", lw=1.5)
ax.text(2, 1.62, "gốc dự báo", color="tab:orange")
ax.set(xlabel="giờ tính từ gốc", yticks=[], title="Bên trái gốc đã biết; phải dự báo cả dải bên phải")
ax.legend(loc="lower right", fontsize=7)
'''},
    "mùa vụ": {"doc": 'Trục ngang là ngày (3 tuần), trục dọc là lượng điện; dải cam là cuối tuần. Ngày nào cũng một nhịp lên xuống, cuối tuần cao hơn: mùa vụ theo ngày và theo tuần.',
        "sau": 'gọi là **mùa vụ**', "ve": r'''
t = np.arange(24 * 21)
y = 1 + 0.6 * np.sin(2 * np.pi * (t - 14) / 24) + 0.3 * ((t // 24) % 7 >= 5) \
    + np.random.default_rng(1).normal(0, 0.12, t.size)
ax.plot(t / 24, y, lw=0.8)
for k in range(3):
    ax.axvspan(7 * k + 5, 7 * k + 7, color="tab:orange", alpha=0.12)
ax.set(xlabel="ngày", yticks=[], title="Mẫu lặp lại: mỗi ngày một nhịp, cuối tuần (cam) cao hơn")
'''},
    "dịch mức": {"doc": 'Trục ngang là thời gian; đường cam là mức trung bình của từng giai đoạn. Mức nhảy lên một bậc rồi ở luôn đó.',
        "sau": '5. **Có dịch mức không?**', "ve": r'''
t = np.arange(200)
y = np.where(t < 120, 1.0, 1.4) + np.random.default_rng(2).normal(0, 0.08, t.size)
ax.plot(t, y, lw=0.8)
ax.hlines([1.0, 1.4], [0, 120], [120, 200], color="tab:orange", lw=2)
ax.set(xlabel="thời gian", yticks=[], title="Mức trung bình nhảy lên rồi ở luôn đó")
'''},
    "dự báo cuốn": {"doc": 'Mỗi hàng là một gốc dự báo: phần xám là dữ liệu được dùng, ô xanh là tuần được dự báo và chấm. Xuống mỗi hàng, gốc dời thêm một tuần.',
        "sau": '**Cách chấm trung thực — dự báo cuốn.**', "ve": r'''
for k in range(5):
    ax.barh(k, 10 + k, color="0.75")
    ax.barh(k, 1, left=10 + k, color="tab:blue")
ax.set(yticks=range(5), yticklabels=[f"gốc {k + 1}" for k in range(5)], xlabel="thời gian (tuần)",
       title="Xám: dữ liệu được dùng · xanh: tuần dự báo và chấm — gốc dời dần")
ax.invert_yaxis()
'''},
    "phân phối": {"doc": 'Trục ngang là lượng điện lúc 19 giờ, trục dọc là số ngày gặp mức đó. Mức 6–9 hay gặp, 12 chỉ gặp một lần.',
        "sau": '> **Mượn trước — phân phối và quantile**', "ve": r'''
v = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])
gt, dem = np.unique(v, return_counts=True)
ax.bar(gt, dem, width=0.7)
ax.set(xlabel="kWh lúc 19 giờ", ylabel="số ngày", xticks=range(5, 13), title="10 ngày: hay gặp quanh 6–9, hiếm khi 12")
'''},
    "quantile, trung vị": {"doc": 'Mười ngày xếp tăng dần. Vạch cam là quantile 0,8, bằng 9 kWh; vạch xanh lá là trung vị, bằng 7 kWh.',
        "sau": '> - Xếp 10 số trên:', "ve": r'''
v = np.sort(np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8]))
ax.bar(range(1, 11), v, color=["tab:blue" if i < 8 else "0.75" for i in range(10)])
ax.axhline(9, color="tab:orange", ls="--")
ax.text(0.6, 9.3, "quantile 0,8 = 9 (số thứ 8)", color="tab:orange")
ax.axhline(7, color="tab:green", ls=":")
ax.text(0.6, 7.3, "trung vị = 7 (số thứ 5)", color="tab:green")
ax.set(xlabel="xếp tăng dần (thứ tự)", ylabel="kWh", xticks=range(1, 11), title="Xếp tăng, lấy số thứ 0,8 × 10 = 8 → quantile 0,8 = 9")
'''},
    "bài toán newsvendor": {"doc": 'Trục ngang là lượng mua mỗi ngày, trục dọc là tiền mất trong 10 ngày. Đáy ở 9 kWh (chấm cam), nằm bên phải mức trung bình 7,7.',
        "sau": 'Bài toán này tên là **newsvendor**', "ve": r'''
mua = np.arange(6, 13)
v = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])
cp = [4 * np.clip(v - m, 0, None).sum() + np.clip(m - v, 0, None).sum() for m in mua]
ax.plot(mua, cp, "o-")
ax.plot(9, min(cp), "o", color="tab:orange", ms=9)
ax.axvline(v.mean(), color="0.5", ls=":")
ax.text(v.mean() + 0.1, 65, "trung bình 7,7", color="0.4")
ax.set(xlabel="lượng mua mỗi ngày (kWh)", ylabel="tiền mất 10 ngày", title="Rẻ nhất ở 9 = quantile 0,8, không phải trung bình")
'''},
    "hàm phân phối tích luỹ": {"doc": 'Trục ngang là mốc x, trục dọc là tỷ lệ ngày dùng không quá x. Đi ngang từ 0,8 tới đường rồi thả xuống, gặp 9: đó là quantile 0,8.',
        "sau": '(hàm phân phối tích luỹ)', "ve": r'''
v = np.sort(np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8]))
ax.step(np.r_[4, v, 13], np.r_[0, np.arange(1, 11) / 10, 1], where="post")
ax.plot([4, 9, 9], [0.8, 0.8, 0], color="tab:orange", ls="--")
ax.set(xlabel="mốc x (kWh)", ylabel="tỷ lệ ngày ≤ x", title="Đi ngang từ 0,8 tới đường, thả xuống: gặp 9 = quantile 0,8")
'''},
}


def soan(nb) -> None:
    nb.md(r"""# Buổi 1 — Forecasting là gì

**Một câu:** một dự báo chỉ "tốt" khi được chấm trên dữ liệu **nó chưa thấy**, **so với một cách đơn giản** (baseline),
bằng **thước đo khớp với quyết định** mà nó phục vụ.

Tình huống: một công ty điện mỗi tối Chủ nhật phải đặt mua điện từng giờ cho 7 ngày tới (168 giờ) cho một hộ gia đình.
Code ban đầu báo sai số 0,380 kWh/giờ — trông rất tốt. Năm phần dưới cho thấy vì sao con số đó không nói lên gì.""")

    nb.md(r"""## 0. Dữ liệu""")
    nb.du_lieu()
    nb.py(r"""import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

TAM = 168             # dự báo 168 giờ = 7 ngày
MOC = "2010-01-04"    # dùng dữ liệu trước mốc để dự báo, chấm trên năm 2010

df = pd.read_csv(lay("uci-household-power"), compression="zip", sep=";", na_values="?",
                 usecols=["Date", "Time", "Global_active_power"])
phut = pd.Series(df["Global_active_power"].to_numpy(),
                 index=pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S"))
# trung bình kW trong một giờ = số kWh của giờ đó; giờ mất quá nửa số đo thì để trống
s = phut.resample("h").mean().where(phut.resample("h").count() >= 30)["2006-12-17":"2010-11-21 23:00"]
print(f"{len(s):,} giờ, trống {s.isna().sum()}, trung bình {s.mean():.2f} kWh/giờ")""")

    # ---------------------------------------------------------------- 1
    nb.khai_niem("biến mục tiêu", "target variable",
                 "đại lượng ta cần dự báo — cột `y` của bài toán.",
                 "ở đây là số kWh hộ gia đình dùng trong mỗi giờ.",
                 "chốt nó trước tiên: đổi biến mục tiêu (kWh/giờ hay kWh/ngày) là đổi cả bài toán.")
    nb.khai_niem("gốc dự báo, mốc cắt dữ liệu", "forecast origin, data cutoff",
                 "thời điểm ra dự báo; từ đó trở đi coi như chưa biết gì. Mốc cắt là giờ cuối cùng đã có số đo.",
                 "tối Chủ nhật 23:59 là mốc cắt; 00:00 thứ Hai là gốc dự báo cho tuần tới.",
                 "chỉ số liệu trước gốc mới được dùng — nếu lỡ dùng số sau gốc, kết quả chấm sẽ đẹp giả.")
    nb.khai_niem("tầm dự báo, h", "forecast horizon",
                 "dự báo xa bao nhiêu bước kể từ gốc; $h$ = 1 là bước đầu tiên.",
                 "dự báo từng giờ cho 7 ngày thì $h$ = 1, 2, …, 168.",
                 "quyết định được nhìn vào đâu: tầm 168 giờ thì không dùng được số của \"hôm qua\" cho thứ Sáu.")
    nb.khai_niem("độ chi tiết", "granularity",
                 "dữ liệu (và dự báo) gộp tới mức nào — theo giờ, ngày, tuần; theo từng hộ hay cả khu.",
                 "cùng dữ liệu, có thể dự báo kWh từng giờ hoặc tổng kWh cả tuần.",
                 "phải khớp với quyết định: mua điện từng giờ thì chấm từng giờ; mua cả khối tuần thì chấm tổng tuần.")
    nb.khai_niem("công suất (kW), điện năng (kWh)", "power, energy",
                 "công suất là nhà đang dùng điện mạnh cỡ nào tại một lúc; điện năng là tổng đã dùng = công suất × thời gian.",
                 "bật lò 2 kW trong nửa giờ tốn 2 × 0,5 = 1 kWh. Trung bình kW trong một giờ chính là số kWh của giờ đó.",
                 "công tơ ghi kW từng phút, công ty mua bán kWh — phải đổi đúng đơn vị trước khi làm gì.")
    nb.khai_niem("dịch mức", "level shift",
                 "mức trung bình của chuỗi đổi hẳn sang một mức mới rồi ở luôn đó.",
                 "nhà có thêm người ở: từ 1,0 lên 1,4 kWh/giờ và không quay lại.",
                 "sau một lần dịch mức, dữ liệu cũ kém giá trị — dấu hiệu \"tương lai không còn giống quá khứ\".")
    nb.md(r"""## 1. Dự báo là điều sẽ xảy ra, không phải điều ta muốn — và phải hỏi đúng trước khi làm

**Vấn đề.** Sếp muốn bán 2.500 ly cà phê nên bảo "dự báo 2.500". Kho đặt hàng theo đó, tuần ấy bán 1.900: thừa nguyên
liệu 600 ly, và không ai còn biết dự báo đúng hay sai.

**Lý do.** **Dự báo** là điều *sẽ* xảy ra; **mục tiêu** là điều ta *muốn*; **kế hoạch** là việc ta *làm*. Trộn chúng thì
mất công cụ đo. Một thứ dự báo được tốt khi: (1) hiểu cái gì tác động tới nó, (2) có nhiều dữ liệu, (3) tương lai giống
quá khứ, (4) công bố dự báo không làm nó đổi. Điện một hộ ngày mai thoả cả bốn; tỷ giá tuần sau gần như chỉ thoả (2).

Trước khi mở dữ liệu, trả lời 6 câu — **phiếu bài toán**. Với công ty điện của ta:

| Câu | Trả lời |
|---|---|
| 1. Ai quyết định gì, bao lâu một lần? | tối Chủ nhật đặt mua điện từng giờ cho 7 ngày tới, mỗi tuần |
| 2. Dự báo cái gì, đơn vị? | kWh mỗi giờ |
| 3. Nhìn xa bao nhiêu (tầm dự báo)? | 168 giờ, từ 00:00 thứ Hai |
| 4. Chi tiết tới mức nào? | từng giờ (phần 5 đổi thành cả tuần) |
| 5. Lúc quyết định đã biết gì? | số đo tới 23:59 Chủ nhật |
| 6. Sai thì mất gì, mỗi chiều? | thiếu 1 kWh mất 4 đồng, thừa 1 kWh mất 1 đồng (phần 6) |

**Kết quả.** Điện của hộ này có nhịp rất đều — dấu hiệu dự báo được:""")

    nb.py(r"""print("giờ thấp nhất / cao nhất trong ngày:", s.groupby(s.index.hour).mean().idxmin(), "h /",
      s.groupby(s.index.hour).mean().idxmax(), "h")
print("TB thứ Hai–Sáu vs thứ Bảy–CN:", round(s[s.index.dayofweek < 5].mean(), 2), "vs", round(s[s.index.dayofweek >= 5].mean(), 2))
s.resample("D").sum(min_count=20).rolling(28, center=True, min_periods=14).mean().plot(
    figsize=(9, 2.5), ylabel="kWh/ngày", title="Mùa đông cao, tháng 8 vắng nhà, năm sau giống năm trước")
plt.show()""")

    nb.khai_niem("mùa vụ", "seasonality",
                 "mẫu lên xuống lặp lại đều đặn theo lịch.",
                 "ngày nào nhà này cũng thấp lúc 4 giờ sáng, cao lúc 20 giờ; năm nào tháng 8 cũng vắng nhà.",
                 "là phần dễ dự báo nhất: biết giờ, thứ, tháng là đoán được một phần lớn con số.")
    nb.md(r"""Nhịp theo ngày (thấp 4h, cao 20h), theo tuần (cuối tuần cao hơn), theo năm (mùa đông, kỳ nghỉ tháng 8). Nhịp lặp
lại theo lịch như vậy gọi là **mùa vụ**.

**Bài học.** Điền phiếu 6 câu trước khi làm gì khác: câu 3 và 5 quyết định được nhìn vào đâu, câu 4 quyết định chấm ở mức
nào, câu 6 quyết định nên báo con số nào.""")

    # ---------------------------------------------------------------- 1
    nb.khai_niem("baseline", "baseline, benchmark forecast",
                 "cách dự báo thật đơn giản, ai cũng làm được, dùng làm mốc để so.",
                 "\"giờ này tuần sau giống giờ này tuần trước\".",
                 "một mô hình phức tạp mà không thắng nổi baseline thì bỏ — nó chỉ tốn công.")
    nb.khai_niem("naive, seasonal naive", "naive forecast, seasonal naive forecast",
                 "naive: lấy nguyên số cuối cùng đã biết. Seasonal naive: lấy số cùng thời điểm của vòng lặp trước.",
                 "dự báo 19:00 thứ Ba — naive lấy số 23:00 Chủ nhật; seasonal naive lấy số 19:00 thứ Ba tuần trước.",
                 "hai baseline chuẩn của mọi bài dự báo; chuỗi có mùa vụ thì seasonal naive thường khó thắng hơn nhiều.")
    nb.khai_niem("sai số dự báo", "forecast error",
                 "thực tế − dự báo, đo trên dữ liệu mô hình **chưa thấy**. Dương là dự báo thấp, âm là dự báo cao.",
                 "thực tế 1,7 kWh, dự báo 1,5 → sai số +0,2 (dự báo thấp 0,2).",
                 "là thứ duy nhất cho biết mô hình sẽ làm tốt tới đâu khi dùng thật.")
    nb.khai_niem("MAE (sai số tuyệt đối trung bình)", "mean absolute error",
                 "trung bình độ lớn các sai số, bỏ dấu.",
                 "sai số +0,5; −0,5; +1,0; 0 → bỏ dấu 0,5; 0,5; 1,0; 0 → trung bình 0,5 kWh.",
                 "một con số tóm \"trung bình mỗi giờ lệch bao nhiêu\", cùng đơn vị với dữ liệu, dễ nói với người không chuyên.")
    nb.md(r"""## 2. Một con số sai số đứng một mình không nói gì

**Vấn đề.** MAE 0,380 kWh/giờ là tốt hay xấu?

**Lý do.** Giống điểm 7: cả lớp được 9 thì 7 là kém, cả lớp được 4 thì 7 là giỏi. Baseline chính là "điểm của cả lớp".

**Kết quả.** Bốn baseline, chỉ dùng số đã biết trước lúc dự báo:""")

    nb.py(r"""def mae(y, du_bao):
    y, du_bao = np.asarray(y, float), np.asarray(du_bao, float)
    co = ~np.isnan(y)                                        # bỏ giờ không có số đo thật
    return float(np.mean(np.abs(y[co] - du_bao[co])))


BASELINE = {
    "giờ trước":         lambda ls: np.full(TAM, ls.iloc[-1]),                                   # số cuối đã biết
    "trung bình":        lambda ls: np.full(TAM, ls.mean()),                                    # TB mọi giờ đã biết
    "tuần trước":        lambda ls: ls.iloc[-TAM:].to_numpy(),                                  # cùng giờ tuần trước
    "trung bình 4 tuần": lambda ls: ls.iloc[-4 * TAM:].to_numpy().reshape(4, TAM).mean(axis=0), # TB 4 tuần cùng giờ
}""")

    nb.md(r"""**Bài học.** Luôn báo MAE **cạnh** vài baseline. Và baseline cũng không được gian lận: "cùng giờ hôm qua" không dùng
được để dự báo thứ Sáu từ tối Chủ nhật — lúc đó chưa có số của thứ Năm.""")

    # ---------------------------------------------------------------- 2
    nb.khai_niem("mô hình, tham số, khớp", "model, parameter, fitting",
                 "mô hình là công thức ra dự báo; tham số là các con số bên trong nó; khớp là chọn các con số đó từ dữ liệu.",
                 "bảng lịch là một mô hình có 8.904 tham số (mỗi ô một trung bình); tính các ô từ dữ liệu là khớp.",
                 "nhiều tham số thì mô hình nhớ được nhiều chi tiết — nhưng cũng dễ học thuộc cả những chuyện tình cờ.")
    nb.khai_niem("phần dư, sai số ảo", "residual, in-sample error",
                 "phần dư là \"sai số\" đo trên chính dữ liệu đã dùng để khớp. Nó luôn đẹp hơn sai số thật — phần đẹp giả đó "
                 "gọi là sai số ảo.",
                 "học thuộc đáp án đề cũ rồi thi lại đúng đề đó được 10 điểm; đề mới chỉ được 6.",
                 "để nhận ra và **không tin** con số chấm trên dữ liệu đã dùng; chỉ tin sai số dự báo.")
    nb.md(r"""## 3. Con số 0,380 là "sai số ảo": mô hình đã thấy trước đáp án

**Vấn đề.** "Mô hình" ban đầu là một **bảng lịch**: trung bình điện theo (tuần trong năm, thứ, giờ) — 8.904 ô. Nó được
lập từ **toàn bộ** 4 năm, rồi chấm trên năm 2010.

**Lý do.** Năm 2010 nằm sẵn trong bảng. Xem ô dùng để dự báo 20:00 thứ Ba 26/10/2010:

**Kết quả.**""")

    nb.py(r"""def khoa(t):
    return [t.isocalendar().week.to_numpy(), t.dayofweek.to_numpy(), t.hour.to_numpy()]


def bang_lich(lich_su):
    return lich_su.groupby(khoa(lich_su.index)).mean()


def du_bao_lich(bang, t):
    return bang.reindex(pd.MultiIndex.from_arrays(khoa(t))).to_numpy()


k = khoa(s.index)
o = s[(k[0] == 43) & (k[1] == 1) & (k[2] == 20)]              # ô (tuần 43, thứ Ba, 20 giờ)
print(o.round(2).to_string())
that = o["2010-10-26"].iloc[0]
print(f"\ndự báo trung thực (3 năm trước): {o[o.index < '2010'].mean():.2f} → lệch {that - o[o.index < '2010'].mean():+.2f}")
print(f"dự báo nhìn trộm  (cả 4 số)    : {o.mean():.2f} → lệch {that - o.mean():+.2f}")

te = s[s.index >= MOC]
print(f"\nMAE bảng lịch lập từ cả 4 năm, chấm trên 2010: {mae(te, du_bao_lich(bang_lich(s), te.index)):.3f}")""")

    nb.md(r"""Ô đó chứa **chính giờ đang cần đoán** (1,01 kWh ngày 26/10/2010). Tối Chủ nhật 24/10 ngoài đời, con số đó chưa tồn
tại. Đưa nó vào trung bình thì dự báo bị kéo về phía đáp án, sai số nhỏ đi — mô hình chẳng giỏi hơn chút nào. Tính trên cả
năm, khoảng **22%** số liệu trong mỗi ô là giờ đang chấm; kết quả là MAE **0,380**.

**Bài học.** Sai số đo trên dữ liệu đã dùng để dựng mô hình luôn đẹp giả. Đó là "sai số ảo", không phải sai số dự báo.""")

    # ---------------------------------------------------------------- 3
    nb.khai_niem("dự báo cuốn", "rolling-origin forecast",
                 "lặp lại việc dự báo nhiều lần, mỗi lần dời gốc dự báo tới trước và chỉ dùng dữ liệu trước gốc đó.",
                 "gốc 4/1/2010: dùng dữ liệu tới 3/1, dự báo 4–10/1, chấm. Gốc 11/1: thêm tuần vừa qua, dự báo 11–17/1, chấm. "
                 "Cứ thế 46 tuần.",
                 "mô phỏng đúng cách mô hình được dùng ngoài đời, nên cho sai số trung thực; chấm trên nhiều gốc thì kết "
                 "luận không phụ thuộc may rủi của một tuần.")
    nb.md(r"""## 4. Chấm trung thực: dự báo cuốn — bảng lịch thua một phép trung bình

**Vấn đề.** Làm sao chấm như ngoài đời?

**Lý do.** Diễn lại đúng thứ tự thời gian bằng dự báo cuốn: mỗi tối Chủ nhật năm 2010 chỉ được dùng những gì đã xảy ra.

**Kết quả.**""")

    nb.py(r"""def du_bao_cuon(chuoi, moc=MOC):
    day_du = chuoi.fillna(chuoi.shift(TAM)).fillna(chuoi.shift(2 * TAM))     # vá giờ trống bằng tuần trước
    phan = []
    for goc in pd.date_range(moc, chuoi.index[-1] - pd.Timedelta(hours=TAM - 1), freq=f"{TAM}h"):
        t = pd.date_range(goc, periods=TAM, freq="h")
        truoc = chuoi.index < goc                                           # CHỈ quá khứ
        cot = {"goc": goc, "y": chuoi.reindex(t).to_numpy(),
               "bảng lịch": du_bao_lich(bang_lich(chuoi[truoc]), t)}
        for ten, ham in BASELINE.items():
            cot[ten] = ham(chuoi[truoc] if ten == "trung bình" else day_du[truoc])
        phan.append(pd.DataFrame(cot, index=t))
    return pd.concat(phan)


cuon = du_bao_cuon(s)
kq = pd.Series({c: mae(cuon["y"], cuon[c]) for c in cuon.columns[2:]}).sort_values()
print(f"{cuon['goc'].nunique()} tuần được chấm\n")
print(kq.round(3).to_string())""")

    nb.md(r"""Chấm trung thực, bảng lịch lên **0,508** và **thua** "trung bình 4 tuần" (**0,490**) — một mô hình 8.904 con số thua
phép trung bình bốn số. Mỗi dòng của bảng kết quả là một giờ; cột `y` là thực tế, mỗi cột còn lại là một cách dự báo:""")

    nb.py(r"""cuon.loc["2010-10-26 19:00":"2010-10-26 21:00"].drop(columns="goc").round(2)""")

    nb.md(r"""Phép thử nhanh để bắt nhìn trộm, dùng được cho mọi mô hình: **sửa đáp án** (cộng 5 kWh vào mọi giờ tuần cuối) rồi chạy
lại. Dự báo trung thực làm trước khi tuần đó xảy ra, nên **không được đổi**.""")

    nb.py(r"""s_gia = s.copy()
s_gia.iloc[-TAM:] += 5
gio = pd.Timestamp("2010-11-16 20:00")
print("dự báo cuốn 20:00 16/11 — trước:", round(du_bao_cuon(s, "2010-11-15").loc[gio, "bảng lịch"], 2),
      "| sau khi sửa đáp án:", round(du_bao_cuon(s_gia, "2010-11-15").loc[gio, "bảng lịch"], 2))
print("bảng lịch nhìn trộm  — trước:", round(du_bao_lich(bang_lich(s), pd.DatetimeIndex([gio]))[0], 2),
      "| sau khi sửa đáp án:", round(du_bao_lich(bang_lich(s_gia), pd.DatetimeIndex([gio]))[0], 2))""")

    nb.md(r"""**Bài học.** Chấm bằng dự báo cuốn, chỉ dùng quá khứ. Mô hình nhìn trộm thì đổi theo đáp án giả; mô hình trung thực
đứng yên.""")

    # ---------------------------------------------------------------- 4
    nb.md(r"""## 5. Chấm theo giờ hay theo tuần có thể đảo thứ hạng

**Vấn đề.** Nếu công ty mua một khối điện cho **cả tuần**, chỉ tổng tuần quan trọng. Thứ hạng còn giữ không?

**Lý do.** Cộng cả tuần thì lệch lên và lệch xuống ngẫu nhiên bù cho nhau; chỉ lệch **cùng một chiều** nhiều ngày mới dồn
lại. Bảng lịch nhớ kỳ nghỉ tháng 8; hai baseline thì không, nên chúng lệch cùng chiều suốt kỳ nghỉ.

**Kết quả.** Chỉ chấm tuần đủ số đo:""")

    nb.py(r"""cot = ["trung bình 4 tuần", "bảng lịch", "tuần trước"]
tuan = cuon.groupby("goc")[["y", *cot]].sum(min_count=1)
tuan.loc[~cuon.groupby("goc")["y"].apply(lambda x: x.notna().all()), "y"] = np.nan
print(pd.DataFrame({"MAE theo giờ": [mae(cuon["y"], cuon[c]) for c in cot],
                    "MAE tổng tuần": [mae(tuan["y"], tuan[c]) for c in cot]}, index=cot).round(3))""")

    nb.md(r"""Theo giờ, trung bình 4 tuần đứng đầu; theo tổng tuần, bảng lịch thắng xa (16,4 so với 27,9 kWh/tuần).

**Bài học.** Chấm ở **đúng mức mà quyết định được đưa ra**. Đổi mức chấm là có thể đổi người thắng.""")

    # ---------------------------------------------------------------- 5
    nb.khai_niem("thị trường kỳ hạn, giá giao ngay", "forward market, spot price",
                 "kỳ hạn: mua trước, chốt giá hôm nay cho hàng giao sau. Giao ngay: mua đúng lúc cần, thường đắt hơn nhiều.",
                 "Chủ nhật mua điện cho cả tuần (kỳ hạn); thứ Tư thiếu thì phải mua bù giá giao ngay.",
                 "giải thích vì sao **thiếu** đắt hơn **thừa** — cơ sở để chọn con số nên báo.")
    nb.khai_niem("phân phối", "distribution",
                 "danh sách các giá trị có thể xảy ra, kèm mức độ hay gặp của từng giá trị.",
                 "10 ngày lúc 19 giờ nhà dùng 7, 5, 9, 6, 8, 12, 6, 9, 7, 8 kWh: hay gặp quanh 6–9, hiếm khi tới 12.",
                 "cho biết không chỉ \"thường bao nhiêu\" mà cả \"xấu nhất cỡ nào\" — thứ cần khi sai số có giá.")
    nb.khai_niem("quantile, trung vị", "quantile, median",
                 "quantile 0,8 là giá trị nhỏ nhất mà ít nhất 80% số liệu không vượt quá. Trung vị là quantile 0,5 — mốc chia đôi.",
                 "xếp 10 số trên tăng dần 5, 6, 6, 7, 7, 8, 8, **9**, 9, 12; số thứ 0,8 × 10 = 8 là 9 → quantile 0,8 = 9 kWh.",
                 "\"mua 9 kWh thì đủ điện cho 80% số ngày\" — biến phân phối thành một con số hành động được.")
    nb.khai_niem("dự báo điểm, dự báo phân phối", "point forecast, probabilistic forecast",
                 "dự báo điểm là một con số; dự báo phân phối là cả dải giá trị kèm khả năng.",
                 "\"mai bán 120 cái\" so với \"mai bán 100–140 cái, khả năng 80%\".",
                 "có phân phối thì với bất kỳ tỷ lệ chi phí nào cũng đọc ra được con số tốt nhất; một con số thì không.")
    nb.khai_niem("bài toán newsvendor", "newsvendor problem",
                 "đặt một lượng hàng một lần khi thiếu và thừa đều mất tiền (tên gốc: người bán báo nhập báo mỗi sáng).",
                 "thiếu mất 4 đồng/kWh, thừa mất 1 đồng/kWh → nên mua ở quantile 4 / (4 + 1) = 0,8.",
                 "cho công thức chọn con số: quantile mức chi phí thiếu / (chi phí thiếu + chi phí thừa).")
    nb.khai_niem("hàm phân phối tích luỹ", "cumulative distribution function, CDF",
                 "với mỗi mốc $x$, tỷ lệ số liệu nhỏ hơn hoặc bằng $x$. Quantile là phép ngược của nó.",
                 "với 10 ngày trên, tỷ lệ ngày dùng ≤ 8 kWh là 7/10 = 0,7; ≤ 9 kWh là 9/10 = 0,9.",
                 "đọc ngược từ tỷ lệ ra mốc chính là tìm quantile — cách sách vở viết công thức newsvendor.")
    nb.md(r"""## 6. Khi thiếu đắt hơn thừa, đừng báo con số trung bình

**Vấn đề.** Thiếu 1 kWh phải mua gấp giá cao, mất **4 đồng**; thừa 1 kWh bán lỗ, mất **1 đồng**. Nên mua bao nhiêu?

**Lý do.** Tăng lượng mua thêm 1 kWh: mỗi ngày đang thiếu đỡ 4 đồng, mỗi ngày đủ mất thêm 1 đồng. Còn lời chừng nào số
ngày thiếu còn nhiều hơn 1/5. Nên dừng ở mức mà **80%** số ngày đủ điện — quantile 0,8 = 4 / (4 + 1).

**Kết quả.** 10 ngày, nhà dùng 7, 5, 9, 6, 8, 12, 6, 9, 7, 8 kWh; thử từng mức mua:""")

    nb.py(r"""nhu_cau = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])
chi_phi = {m: int(4 * np.clip(nhu_cau - m, 0, None).sum() + np.clip(m - nhu_cau, 0, None).sum()) for m in range(6, 13)}
print("mua (kWh) → tiền mất 10 ngày:", chi_phi)
print("quantile 0,8 của nhu cầu:", np.quantile(nhu_cau, 0.8, method="inverted_cdf"), "| trung bình:", nhu_cau.mean())""")

    nb.md(r"""Rẻ nhất ở **9 kWh** = quantile 0,8, không phải trung bình 7,7. Trên dữ liệu thật: lấy sai số của năm 2009, cộng
quantile 0,8 của nó vào dự báo năm 2010:""")

    nb.py(r"""def tien_mat(y, f):
    d = np.asarray(y, float) - np.asarray(f, float)
    d = d[~np.isnan(d)]
    return float(np.mean(np.where(d > 0, 4 * d, -1 * d)))


c09 = du_bao_cuon(s[s.index < MOC], moc="2009-01-05")
q = float((c09["y"] - c09["trung bình 4 tuần"]).dropna().quantile(0.8))    # chọn từ 2009, không nhìn 2010
y, f = cuon["y"].to_numpy(), cuon["trung bình 4 tuần"].to_numpy()
print(f"cộng thêm {q:.3f} kWh mỗi giờ")
print(f"tiền mất/giờ: {tien_mat(y, f):.3f} → {tien_mat(y, f + q):.3f} | MAE: {mae(y, f):.3f} → {mae(y, f + q):.3f}")""")

    nb.md(r"""Tiền mất giảm 18,6% trong khi MAE **tệ đi** — MAE phạt thiếu và thừa như nhau nên không thấy lợi của mua dư.

**Bài học.** Thước đo phải khớp với cái giá thật của sai lầm. Chấm bằng thước đo sai thì chọn sai.""")

    # ---------------------------------------------------------------- 7
    nb.md(r"""## 7. Bài tập về nhà — đáp số

**Bài 2 — Gộp hai dự báo.** Lấy trung bình dự báo của "trung bình 4 tuần" và "bảng lịch":""")

    nb.py(r"""cuon["kết hợp"] = (cuon["trung bình 4 tuần"] + cuon["bảng lịch"]) / 2
cot = ["kết hợp", "trung bình 4 tuần", "bảng lịch"]
tuan = cuon.groupby("goc")[["y", *cot]].sum(min_count=1)
tuan.loc[~cuon.groupby("goc")["y"].apply(lambda x: x.notna().all()), "y"] = np.nan
print(pd.DataFrame({"MAE theo giờ": [mae(cuon["y"], cuon[c]) for c in cot],
                    "MAE tổng tuần": [mae(tuan["y"], tuan[c]) for c in cot]}, index=cot).round(3))""")

    nb.md(r"""Theo giờ, bản gộp thắng cả hai (lỗi của hai cách bù cho nhau một phần); theo tuần, nó đứng giữa vì một nửa vẫn là
baseline không nhớ tháng 8.

**Bài 3 — Thiếu 1 đồng, thừa 3 đồng.** Mức nên mua = 1 / (1 + 3) = 0,25 → cộng quantile 0,25 của sai số 2009 (số âm: mua
ít hơn dự báo):""")

    nb.py(r"""def tien_mat_13(y, f):
    d = np.asarray(y, float) - np.asarray(f, float)
    d = d[~np.isnan(d)]
    return float(np.mean(np.where(d > 0, 1 * d, -3 * d)))


q25 = float((c09["y"] - c09["trung bình 4 tuần"]).dropna().quantile(0.25))
co = ~np.isnan(y)
print(f"cộng thêm {q25:+.3f} kWh | tiền mất/giờ: {tien_mat_13(y, f):.3f} → {tien_mat_13(y, f + q25):.3f}"
      f" | tỷ lệ giờ thiếu: {np.mean(y[co] > (f + q25)[co]):.0%}")""")

    nb.md(r"""Mua ít hơn dự báo thì thiếu tới khoảng 3/4 số giờ — đúng ý đồ, vì thừa đắt gấp ba.

## Tự kiểm

- [ ] Giải thích vì sao 0,380 là sai số ảo, và vì sao bảng lịch (0,508) thua trung bình 4 tuần (0,490).
- [ ] Nói được phép thử "sửa đáp án" bắt nhìn trộm thế nào.
- [ ] Giải thích vì sao chấm theo tổng tuần thì thứ hạng đảo.
- [ ] Thiếu 4 đồng, thừa 1 đồng: vì sao mua ở quantile 0,8?""")
