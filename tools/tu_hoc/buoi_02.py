"""Nội dung tự học buổi 2 — Xác suất và thống kê cho dự báo. Sinh: python tools/tu_hoc/sinh.py 2 --chay"""

DU_Y = {"4.1": 1, "4.2": 2, "4.3": 3, "4.4": 4, "4.5": 5, "4.6": 6, "BT1": 7, "BT2": 7}


# hình minh hoạ khái niệm: {tên hộp: {doc: cách đọc 1–2 câu, sau: mốc chèn trong tai-lieu.md (None = chỉ notebook), ve: code}}
HINH = {
    "histogram": {"doc": 'Trục ngang chia thành các khoảng rộng 25, trục dọc là số lần rơi vào mỗi khoảng. Cột dồn bên trái, đuôi kéo dài bên phải.',
        "sau": None, "ve": r'''
x = np.random.default_rng(0).lognormal(5, 0.8, 3000)
ax.hist(x, bins=np.arange(0, 1000, 25), color="lightsteelblue", edgecolor="white")
ax.set(xlabel="giá trị (chia khoảng rộng 25)", ylabel="số lần rơi vào", title="Đếm theo khoảng: thấy ngay dồn bên trái, đuôi dài bên phải")
'''},
    "quantile, trung vị": {"doc": 'Trục ngang là mốc, trục dọc là tỷ lệ số liệu không vượt mốc. Đi ngang từ 0,5 hoặc 0,9 tới đường cong rồi thả xuống là ra quantile.',
        "sau": None, "ve": r'''
x = np.sort(np.random.default_rng(0).lognormal(5, 0.8, 3000))
ax.plot(x, np.arange(1, x.size + 1) / x.size)
for p, mau in [(0.5, "tab:green"), (0.9, "tab:orange")]:
    q = np.quantile(x, p)
    ax.plot([0, q, q], [p, p, 0], color=mau, ls="--")
    ax.text(q + 10, p - 0.1, f"quantile {str(p).replace('.', ',')} ≈ {q:.0f}", color=mau)
ax.set(xlim=(0, 800), xlabel="mốc", ylabel="tỷ lệ ≤ mốc", title="Từ tỷ lệ trên trục dọc, đi ngang rồi thả xuống: ra quantile")
'''},
    "phương sai, độ lệch chuẩn": {"doc": 'Hai đường cùng trung bình 0. Đường cam có độ lệch chuẩn 3 nên trải rộng gấp ba đường xanh (độ lệch chuẩn 1).',
        "sau": '5. **Độ lệch chuẩn**', "ve": r'''
g = np.linspace(-10, 10, 400)
for s, mau in [(1, "tab:blue"), (3, "tab:orange")]:
    ax.plot(g, np.exp(-g**2 / (2 * s**2)) / (s * np.sqrt(2 * np.pi)), color=mau, label=f"độ lệch chuẩn {s}")
ax.set(yticks=[], xlabel="giá trị (trung bình 0)", title="Cùng trung bình; độ lệch chuẩn lớn thì trải rộng hơn")
ax.legend(fontsize=7)
'''},
    "hệ số lệch": {"doc": 'Trái: số liệu đối xứng quanh giữa, hệ số lệch gần 0. Phải: dồn bên trái, đuôi dài bên phải, hệ số lệch dương.',
        "sau": '**Hệ số lệch** đo đuôi', "ve": r'''
fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.0), sharey=True)
rng = np.random.default_rng(1)
a.hist(rng.normal(0, 1, 3000), bins=40, color="lightsteelblue")
a.set(title="đối xứng: hệ số lệch ≈ 0", yticks=[])
b.hist(rng.lognormal(0, 0.7, 3000), bins=40, color="navajowhite")
b.set(title="đuôi phải dài: hệ số lệch > 0")
'''},
    "pinball loss": {"doc": 'Trục ngang là thật trừ dự báo (dương là dự báo thiếu), trục dọc là tiền phạt. Đường xanh bên phải dốc gấp 4 lần bên trái: thiếu bị phạt nặng hơn thừa.',
        "sau": '**Pinball loss** là cách phạt', "ve": r'''
e = np.linspace(-5, 5, 201)                      # thật − dự báo
ax.plot(e, np.where(e >= 0, 0.8 * e, -0.2 * e), label="pinball τ = 0,8")
ax.plot(e, np.abs(e) * 0.5, ls=":", color="0.5", label="tuyệt đối (× 0,5)")
ax.set(xlabel="thật − dự báo (dương = dự báo thiếu)", ylabel="tiền phạt", title="Thiếu bị phạt dốc gấp 4 lần thừa")
ax.legend(fontsize=7)
'''},
    "phân phối chuẩn": {"doc": 'Đường hình chuông đối xứng quanh trung bình. Phần xanh trong ±1,96 độ lệch chuẩn chiếm 95%; mỗi phần cam ở hai đuôi chiếm 2,5%.',
        "sau": '**Con số 1,96 đến từ phân phối chuẩn**', "ve": r'''
g = np.linspace(-4, 4, 400)
f = np.exp(-g**2 / 2) / np.sqrt(2 * np.pi)
ax.plot(g, f)
ax.fill_between(g, f, where=np.abs(g) <= 1.96, alpha=0.25, label="95% ở giữa")
ax.fill_between(g, f, where=np.abs(g) > 1.96, color="tab:orange", alpha=0.5, label="2,5% mỗi đuôi")
ax.set(xticks=[-1.96, 0, 1.96], xticklabels=["TB − 1,96 s", "trung bình", "TB + 1,96 s"], yticks=[],
       title="Hình chuông đối xứng: 95% trong ±1,96 độ lệch chuẩn")
ax.legend(fontsize=7)
'''},
    "tỷ lệ phủ": {"doc": 'Mỗi chấm là giá trị thật của một lần dự báo, dải xanh là khoảng đã báo, dấu x đỏ là lần rơi ra ngoài. Tỷ lệ chấm rơi trong dải là tỷ lệ phủ.',
        "sau": '**Trực giác.** Nói "mai 28–33 độ', "ve": r'''
rng = np.random.default_rng(3)
t = np.arange(40)
y = rng.normal(0, 1, 40)
trong = np.abs(y) <= 1.6
ax.fill_between(t, -1.6, 1.6, color="tab:blue", alpha=0.12, label="khoảng đã báo")
ax.plot(t[trong], y[trong], "o", ms=3, label=f"rơi trong: {trong.sum()}/40")
ax.plot(t[~trong], y[~trong], "x", color="tab:red", label=f"rơi ngoài: {(~trong).sum()}/40")
ax.set(yticks=[], xlabel="lần dự báo", title=f"Tỷ lệ phủ = {trong.mean():.0%}")
ax.legend(fontsize=7, ncols=3, loc="upper center", bbox_to_anchor=(0.5, -0.3), frameon=False)
'''},
    "tương quan, hệ số r": {"doc": 'Bốn đám chấm: nghiêng lên (r gần 0,9), tản mát (r gần 0), nghiêng xuống (r gần −0,9), và hình chữ U: liên quan chặt nhưng r gần 0 vì không thẳng.',
        "sau": 'là cùng chiều hoàn hảo trên đường thẳng', "ve": r'''
fig, truc = plt.subplots(1, 4, figsize=(5.8, 1.7))
rng = np.random.default_rng(4)
x = rng.normal(size=150)
for a, (ten, y) in zip(truc, [("r ≈ 0,9", x + 0.5 * rng.normal(size=150)), ("r ≈ 0", rng.normal(size=150)),
                               ("r ≈ −0,9", -x + 0.5 * rng.normal(size=150)), ("cong: r ≈ 0", x**2)]):
    a.plot(x, y, ".", ms=2)
    a.set(title=ten, xticks=[], yticks=[])
'''},
    "tự tương quan": {"doc": 'Đường xám (tự tương quan gần 0) lên xuống lộn xộn. Đường xanh (gần 0,9) lên thì ở trên một lúc, xuống thì ở dưới một lúc.',
        "sau": '> **Mượn trước — tự tương quan**', "ve": r'''
rng = np.random.default_rng(5)
e = rng.normal(size=150)
x = np.zeros(150)
for t in range(1, 150):
    x[t] = 0.9 * x[t - 1] + e[t]
ax.plot(e, lw=0.8, color="0.6", label="tự tương quan ≈ 0: lộn xộn")
ax.plot(x, lw=1.2, label="tự tương quan ≈ 0,9: dai, lên thì ở trên một lúc")
ax.set(yticks=[], xlabel="thời gian")
ax.legend(fontsize=7)
'''},
    "định lý giới hạn trung tâm (CLT)": {"doc": 'Trái: từng giá trị lệch phải. Phải: trung bình của 30 giá trị, lặp nhiều lần, đã gần hình chuông.',
        "sau": '**Vì sao $\\sqrt n$?**', "ve": r'''
fig, (a, b) = plt.subplots(1, 2, figsize=(5.6, 2.0))
rng = np.random.default_rng(6)
a.hist(rng.lognormal(0, 0.8, 5000), bins=50, color="navajowhite")
a.set(title="từng giá trị: lệch phải", yticks=[])
b.hist(rng.lognormal(0, 0.8, (5000, 30)).mean(axis=1), bins=50, color="lightsteelblue")
b.set(title="TB của 30 giá trị: gần hình chuông", yticks=[])
fig.tight_layout()
'''},
    "bootstrap, block bootstrap": {"doc": 'Mỗi ô là một điểm dữ liệu, màu theo vị trí gốc. Rút từng điểm xáo tung thứ tự; rút khối 4 giữ các điểm liền nhau đi cùng nhau.',
        "sau": '**Block bootstrap** (Künsch 1989)', "ve": r'''
fig, truc = plt.subplots(3, 1, figsize=(5.2, 1.9), sharex=True)
rng = np.random.default_rng(7)
mau = plt.cm.viridis(np.linspace(0, 1, 12))
cs = [np.arange(12), rng.integers(0, 12, 12),
      np.concatenate([np.arange(b, b + 4) for b in rng.integers(0, 9, 3)])]
for a, ten, c in zip(truc, ["gốc", "rút từng điểm", "rút khối 4"], cs):
    a.bar(range(12), 1, color=mau[c], width=0.95)
    a.set(yticks=[], ylabel=ten)
    a.yaxis.label.set(rotation=0, ha="right", va="center")
truc[-1].set(xticks=[])
truc[0].set_title("Màu = vị trí gốc: rút khối giữ các điểm liền nhau đi cùng nhau")
'''},
    "kiểm định, giả thuyết không H0": {"doc": 'Cột xanh là chênh lệch khi xáo nhãn ngẫu nhiên, tức khi H0 đúng. p là phần nằm ngoài hai vạch cam.',
        "sau": None, "ve": r'''
xao = np.random.default_rng(8).normal(0, 200, 9999)
ax.hist(xao, bins=60, color="lightsteelblue")
ax.axvline(456, color="tab:orange", lw=2)
ax.axvline(-456, color="tab:orange", ls="--")
ax.set(yticks=[], xlabel="chênh lệch khi xáo nhãn ngẫu nhiên",
       title="Nếu H0 đúng, chênh lệch rơi đâu; p = phần nằm ngoài hai vạch cam")
'''},
}


def soan(nb) -> None:
    nb.md(r"""# Buổi 2 — Xác suất và thống kê cho dự báo

**Một câu:** không ai biết chắc tương lai, nhưng ta có thể nói "thường khoảng bao nhiêu, hiếm khi quá bao nhiêu" — và
phải **kiểm xem lời hứa đó có giữ được không**.

Tình huống: hệ thống xe đạp công cộng Capital Bikeshare ở Washington D.C. muốn biết 17 giờ mai có bao nhiêu lượt thuê, để
chuẩn bị đủ xe. Sáu phần dưới là sáu công cụ để trả lời câu đó cho trung thực.""")

    nb.md(r"""## 0. Dữ liệu""")
    nb.du_lieu()
    nb.py(r"""import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with zipfile.ZipFile(lay("uci-bike-sharing")) as z:
    h = pd.read_csv(z.open("hour.csv"), parse_dates=["dteday"])
    d = pd.read_csv(z.open("day.csv"), parse_dates=["dteday"])
y = h["cnt"].to_numpy(float)
print(f"{len(h):,} giờ, {len(d)} ngày | TB mỗi ngày: 2011 = {d.loc[d.yr == 0, 'cnt'].mean():.0f}, 2012 = {d.loc[d.yr == 1, 'cnt'].mean():.0f}")
d.set_index("dteday")["cnt"].rolling(30, center=True).mean().plot(figsize=(9, 2.5), ylabel="lượt/ngày",
                                                                 title="Hè đông, đông vắng; 2012 đông hơn hẳn 2011")
plt.show()""")

    # ---------------------------------------------------------------- 1
    nb.khai_niem("biến ngẫu nhiên", "random variable",
                 "đại lượng chưa biết trước giá trị, chỉ biết giá trị nào hay gặp, giá trị nào hiếm.",
                 "số lượt thuê lúc 17h mai: có thể 300, có thể 600, hiếm khi dưới 50.",
                 "mọi thứ ta dự báo đều là biến ngẫu nhiên — nên dự báo tốt phải nói cả \"chắc tới đâu\".")
    nb.khai_niem("histogram", "histogram",
                 "biểu đồ cột: chia trục giá trị thành các khoảng, đếm có bao nhiêu số rơi vào mỗi khoảng.",
                 "9 số 2, 3, 5, 6, 8, 9, 12, 18, 36 → khoảng 0–9 có 6 số, 10–19 có 2 số, 20–29 có 0, 30–39 có 1.",
                 "nhìn là thấy hình dạng phân phối: dồn ở đâu, lệch về bên nào, có số lạ không.")
    nb.khai_niem("quantile, trung vị", "quantile, median",
                 "quantile 0,8 là giá trị nhỏ nhất mà ít nhất 80% số liệu không vượt quá. Trung vị là quantile 0,5 — mốc chia đôi.",
                 "9 giờ xếp tăng 2, 3, 5, 6, **8**, 9, 12, **18**, 36: trung vị là số thứ 5 = 8; quantile 0,8 là số thứ 8 = 18.",
                 "trả lời \"cần chuẩn bị bao nhiêu xe để đủ cho 80% số giờ\" — thứ trung bình không trả lời được.")
    nb.md(r"""## 1. Quantile trả lời "mức nào đủ cho 80% số lần?"

**Vấn đề.** Lượt thuê lúc 17h mai chưa biết trước — nó là một **biến ngẫu nhiên**. Ghi lại "mức nào hay gặp tới đâu"
bằng gì?

**Lý do.** Ghi lại bằng phân phối, rồi tóm nó bằng vài quantile. Tính tay quantile 0,8: xếp tăng, lấy vị trí 0,8 × số
lượng, làm tròn lên — 9 giờ thì vị trí 7,2 → số thứ 8 → **18**.

**Kết quả.**""")

    nb.py(r"""x9 = np.array([8, 2, 36, 5, 12, 3, 18, 6, 9])
print("quantile 0,8 — đếm tay:", np.quantile(x9, 0.8, method="inverted_cdf"), "| np.quantile mặc định:", round(np.quantile(x9, 0.8), 1))
print(f"dữ liệu thật: trung bình {y.mean():.0f}, trung vị {np.median(y):.0f}, quantile 0,9 {np.quantile(y, 0.9):.0f} lượt/giờ")
plt.figure(figsize=(9, 2.3))
plt.hist(y, bins=np.arange(0, 1000, 25), color="lightsteelblue")
plt.axvline(y.mean(), color="tab:orange", label="trung bình")
plt.axvline(np.median(y), color="tab:blue", ls="--", label="trung vị")
plt.legend(fontsize=8)
plt.title("Lệch phải: dồn bên trái, đuôi dài bên phải")
plt.show()""")

    nb.md(r"""Máy mặc định **nội suy** giữa hai số kề nhau nên ra 14,4 thay vì 18; `method="inverted_cdf"` khớp cách đếm tay. Với
hàng nghìn số, hai cách gần như trùng. Lượt thuê **lệch phải**: vài giờ cao điểm rất đông kéo trung bình (189) lên cao
hơn trung vị (142).

**Bài học.** Trung vị là quantile 0,5. Dữ liệu lệch phải thì trung bình nằm bên phải trung vị.""")

    # ---------------------------------------------------------------- 2
    nb.khai_niem("phương sai, độ lệch chuẩn", "variance, standard deviation",
                 "đo số liệu dao động quanh trung bình cỡ nào. Phương sai = tổng bình phương độ lệch chia $n-1$; độ lệch "
                 "chuẩn $s$ = căn của phương sai, cùng đơn vị với dữ liệu.",
                 "2, 4, 6: trung bình 4, độ lệch −2, 0, 2 → phương sai (4 + 0 + 4)/2 = 4 → $s$ = 2.",
                 "cho biết \"lệch điển hình\" bao nhiêu — nền của khoảng dự báo và khoảng tin cậy.")
    nb.khai_niem("hệ số lệch", "skewness",
                 "đo phân phối có đuôi dài về phía nào: dương là đuôi phải dài (vài số rất lớn), âm là đuôi trái dài.",
                 "1, 1, 2, 2, 3, 20 → dương, vì số 20 kéo đuôi phải.",
                 "cảnh báo khi các công thức giả định hình chuông đối xứng (như ±1,96 × độ lệch chuẩn) sẽ sai.")
    nb.khai_niem("pinball loss", "pinball loss, quantile loss",
                 "cách phạt một dự báo quantile mức τ: mỗi đơn vị thiếu phạt τ, mỗi đơn vị thừa phạt 1 − τ.",
                 "τ = 0,8, thật 10, dự báo 8 → thiếu 2, phạt 0,8 × 2 = 1,6. Dự báo 12 → thừa 2, phạt 0,2 × 2 = 0,4.",
                 "thước đo đúng cho dự báo quantile — và cho bài toán thiếu đắt hơn thừa.")
    nb.md(r"""## 2. Nên báo con số nào? Tuỳ bạn bị phạt thế nào khi sai

**Vấn đề.** 9 nhân viên lương 10 triệu, giám đốc 300 triệu: "lương trung bình 39 triệu" — đúng, nhưng không ai nhận mức
đó. Chỉ được báo **một** con số thì chọn trung bình, trung vị hay quantile?

**Lý do.** Mỗi cách phạt có một con số tốt nhất riêng:

- Phạt **tuyệt đối** |thật − dự báo| → tốt nhất là **trung vị** (hai phe trên/dưới cân nhau).
- Phạt **bình phương** (thật − dự báo)² → tốt nhất là **trung bình** (số ở xa bị phạt nặng, kéo con số về phía nó).
- Phạt **pinball** mức τ → tốt nhất là **quantile τ** (τ = 0,8: thiếu đắt gấp 4 lần thừa).

**Kết quả.** Báo cùng một con số $c$ cho 9 giờ trên, tính phạt trung bình:""")

    nb.py(r"""def pinball(y, c, tau):
    sai = np.asarray(y, float) - c
    return float(np.where(sai >= 0, tau * sai, (tau - 1) * sai).mean())


print(f"trung bình {x9.mean():.0f}, độ lệch chuẩn s = {x9.std(ddof=1):.2f} (ddof=1: chia n − 1)")
print(pd.DataFrame({c: {"tuyệt đối": np.abs(x9 - c).mean(), "bình phương": ((x9 - c) ** 2).mean(), "pinball 0,8": pinball(x9, c, 0.8)}
                    for c in (8, 11, 18)}).T.rename_axis("c (trung vị / trung bình / quantile 0,8)").round(2))""")

    nb.md(r"""Mỗi cột thấp nhất ở một dòng khác: tuyệt đối ở trung vị (8), bình phương ở trung bình (11), pinball ở quantile 0,8
(18). Trên cả 17.379 giờ thật cũng vậy: thử mọi $c$, đáy của ba đường rơi đúng trung bình, trung vị, quantile.

**Bài học.** Trước khi hỏi "báo con số nào", hỏi "sai thì bị phạt thế nào".""")

    # ---------------------------------------------------------------- 3
    nb.khai_niem("phân phối chuẩn", "normal distribution, Gaussian",
                 "đường cong hình chuông, đối xứng quanh trung bình; 95% giá trị nằm trong trung bình ± 1,96 độ lệch chuẩn.",
                 "trung bình 100, độ lệch chuẩn 10 → 95% giá trị trong 100 ± 19,6, tức 80,4–119,6.",
                 "là nguồn gốc con số 1,96 — chỉ dùng được khi dữ liệu gần hình chuông.")
    nb.khai_niem("tỷ lệ phủ", "coverage",
                 "tỷ lệ số lần giá trị thật rơi vào khoảng đã báo.",
                 "báo 100 khoảng \"95%\", thật rơi vào 64 lần → tỷ lệ phủ 64%, lời hứa bị vỡ.",
                 "cách duy nhất kiểm một khoảng có trung thực không. Đếm riêng hai đuôi để biết khoảng lệch về phía nào.")
    nb.khai_niem("trong mẫu / ngoài mẫu", "in-sample / out-of-sample",
                 "trong mẫu: đo trên dữ liệu đã dùng để dựng; ngoài mẫu: đo trên dữ liệu chưa dùng.",
                 "dựng khoảng từ năm 2011; chấm trên 2011 là trong mẫu, chấm trên 2012 là ngoài mẫu.",
                 "chỉ con số ngoài mẫu mới nói được chuyện sẽ xảy ra khi dùng thật.")
    nb.khai_niem("xu hướng", "trend",
                 "hướng đi lâu dài của chuỗi — tăng dần, giảm dần hay đi ngang.",
                 "lượt thuê trung bình mỗi giờ từ 144 (2011) lên 235 (2012).",
                 "khoảng dựng từ quá khứ mà bỏ qua xu hướng sẽ vỡ khi tương lai đi lên (hoặc xuống).")
    nb.md(r"""## 3. Khoảng "95%" chỉ đáng tin khi đo tỷ lệ phủ trên dữ liệu chưa dùng

**Vấn đề.** Khoảng "17h mai 65–604 lượt, 95%" hứa rằng 100 lần nói như vậy thì khoảng 95 lần đúng. Lời hứa có giữ được
không?

**Lý do.** Công thức quen thuộc **trung bình ± 1,96 × độ lệch chuẩn** chỉ đúng với hình chuông. Lượt thuê không hình chuông — nó lệch phải — nên công thức này cho cận dưới quá thấp
(có khi âm). Sửa: lấy thẳng **quantile 0,025 và 0,975** của lịch sử. Nhưng không cách nào cứu được nếu tương lai khác quá
khứ.

**Kết quả.** Mỗi giờ trong ngày dựng một khoảng từ năm 2011, rồi đếm riêng hai đuôi:""")

    nb.py(r"""cach = {"±1,96s": lambda x: (x.mean() - 1.96 * x.std(ddof=1), x.mean() + 1.96 * x.std(ddof=1)),
        "quantile": lambda x: tuple(np.quantile(x, [0.025, 0.975]))}
n11, n12h = h[h.yr == 0], h[h.yr == 1]
hang = []
for ten, f in cach.items():
    k = pd.DataFrame([(g, *f(nhom["cnt"])) for g, nhom in n11.groupby("hr")], columns=["hr", "lo", "hi"])
    for cham, du in [("2011 (đã dùng)", n11), ("2012 (chưa dùng)", n12h)]:
        m = du.merge(k, on="hr")
        hang.append({"cách": ten, "chấm trên": cham, "phủ": np.mean((m.cnt >= m.lo) & (m.cnt <= m.hi)),
                     "rơi dưới": np.mean(m.cnt < m.lo), "vượt trên": np.mean(m.cnt > m.hi)})
print(pd.DataFrame(hang).to_string(index=False, float_format="{:.1%}".format))""")

    nb.md(r"""Trên 2011, hai cách đều phủ khoảng 95%, nhưng ±1,96s lệch đuôi: gần như không bao giờ rơi dưới, vượt trên quá nhiều.
Quantile cân lại hai đuôi. Trên 2012 cả hai **vỡ** (khoảng 70%): năm 2012 đông hơn hẳn (trung bình mỗi giờ 144 → 235) —
cả chuỗi dời lên, gọi là **dịch mức**.

**Bài học.** Chấm khoảng trên dữ liệu **chưa dùng** và báo **riêng từng đuôi**. Quantile sửa được hình dạng, không sửa
được tương lai khác quá khứ.""")

    # ---------------------------------------------------------------- 4
    nb.khai_niem("tương quan, hệ số r", "correlation coefficient",
                 "con số từ −1 đến 1 đo hai đại lượng cùng tăng giảm theo đường thẳng tới đâu.",
                 "1, 2, 3 và 2, 4, 6 → $r$ = 1 (cùng tăng hoàn hảo); 1, 2, 3 và 6, 4, 2 → $r$ = −1.",
                 "tìm biến giúp dự báo: nhiệt độ có $r$ dương với lượt thuê thì dự báo nhiệt độ giúp dự báo lượt thuê.")
    nb.khai_niem("tự tương quan", "autocorrelation",
                 "tương quan của một chuỗi với chính nó lùi $k$ bước.",
                 "chuỗi 1, 3, 1, 3 lên xuống xen kẽ → tự tương quan trễ 1 là −0,75.",
                 "đo \"giờ này có giống giờ trước không\" — cao thì quá khứ gần giúp dự báo tốt, nhưng dữ liệu ít thông tin mới.")
    nb.md(r"""## 4. Tương quan chỉ đo quan hệ thẳng, và không phải nhân quả

**Vấn đề.** Trời ấm thì đông khách hơn? Cần một con số đo "hai đại lượng cùng lên cùng xuống tới đâu".

**Lý do.** Cách tính $r$: với mỗi ngày, xem nhiệt độ và lượt thuê cao hay thấp **hơn bình thường**; nhân hai độ lệch
(cùng phía → dương), cộng lại, chia cho một số chuẩn hoá. Hai cái bẫy: $r$ chỉ đo quan hệ **đường
thẳng**; và $r$ cao có thể do một **biến gây nhiễu** tác động lên cả hai (kem và đuối nước cùng tăng vì trời nóng).

**Kết quả.**""")

    nb.py(r"""xu = np.array([-2, -1, 0, 1, 2])
print("y = x² (liên quan hoàn toàn, nhưng cong): r =", round(np.corrcoef(xu, xu**2)[0, 1], 3))
g17 = h[h.hr == 17]
print(f"giờ trong ngày × lượt thuê: r = {np.corrcoef(h.hr, h.cnt)[0, 1]:.2f}  ← quan hệ rất mạnh nhưng cong")
print(f"nhiệt độ × lượt thuê: mọi giờ r = {np.corrcoef(h.temp, h.cnt)[0, 1]:.2f}, chỉ lúc 17h r = {np.corrcoef(g17.temp, g17.cnt)[0, 1]:.2f}")
print(f"độ ẩm × lượt thuê  : mọi giờ r = {np.corrcoef(h.hum, h.cnt)[0, 1]:.2f}, chỉ lúc 17h r = {np.corrcoef(g17.hum, g17.cnt)[0, 1]:.2f}")
dc = y - y.mean()
print(f"tự tương quan (giờ này với giờ trước): {(dc[1:] * dc[:-1]).sum() / (dc**2).sum():.2f}")""")

    nb.md(r"""Giờ trong ngày quyết định lượt thuê rất mạnh (đêm gần 0, đỉnh 8h và 17h) mà $r$ chỉ 0,39 — vì quan hệ cong. Giữ cố
định giờ (chỉ xét 17h) thì $r$ của độ ẩm yếu đi: phần lớn quan hệ "ẩm ↔ vắng" là vì cả hai cùng là "ban đêm" — giờ trong
ngày là biến gây nhiễu. Dòng cuối là **tự tương quan**: tương quan của chuỗi với chính nó lùi một bước — 0,84, giờ liền
nhau gần như "biết" nhau (phần 6 cần con số này).

**Bài học.** Vẽ trước khi tin $r$; $r$ gần 0 vẫn có thể có quan hệ cong; $r$ cao chưa phải nhân quả — nhưng biến không
gây ra $y$ vẫn có thể giúp dự báo $y$.""")

    # ---------------------------------------------------------------- 5
    nb.khai_niem("kiểm định, giả thuyết không H0", "hypothesis test, null hypothesis",
                 "kiểm định xem dữ liệu có đủ bằng chứng bác bỏ một giả định mặc định \"không có gì đặc biệt\" — gọi là $H_0$.",
                 "$H_0$: \"đồng xu cân đối\"; \"nhãn ngày làm việc/nghỉ không liên quan tới lượt thuê\".",
                 "tránh kết luận vội từ một khác biệt có thể chỉ do may.")
    nb.khai_niem("p-value", "p-value",
                 "nếu $H_0$ đúng, xác suất gặp kết quả lệch cỡ này hoặc hơn.",
                 "đồng xu cân đối mà tung 10 lần được ≥ 9 ngửa: p = 11/1.024 ≈ 0,011.",
                 "p nhỏ nghĩa là \"nếu không có gì đặc biệt thì chuyện này rất hiếm\" → có lý do để tin có gì đó thật.")
    nb.khai_niem("mức ý nghĩa α", "significance level",
                 "ngưỡng chọn **trước** khi xem dữ liệu; p nhỏ hơn nó thì bác bỏ $H_0$. Hay dùng 0,05.",
                 "p = 0,011 < 0,05 → bác bỏ \"đồng xu cân đối\"; p = 0,17 → không bác bỏ.",
                 "chọn trước để không bị cám dỗ dời ngưỡng cho vừa kết quả mình muốn.")
    nb.khai_niem("seed", "random seed",
                 "con số khởi đầu của bộ sinh số ngẫu nhiên; cùng seed thì ra cùng dãy số.",
                 "`np.random.default_rng(2026)` chạy hai lần cho đúng cùng các lần xáo nhãn.",
                 "làm kết quả có yếu tố ngẫu nhiên lặp lại được — người khác chạy lại ra đúng con số của bạn.")
    nb.md(r"""## 5. Kiểm định hỏi: nếu không có gì đặc biệt, kết quả này hiếm cỡ nào?

**Vấn đề.** Năm 2012 ngày làm việc trung bình hơn ngày nghỉ 456 lượt. Khác biệt thật hay do may?

**Lý do.** Tung đồng xu 10 lần được 9 ngửa: nếu đồng xu cân đối, chuyện đó hiếm cỡ p = 0,011 < 0,05 → bác bỏ "cân
đối". Với hai nhóm ngày: $H_0$ là "nhãn làm việc/nghỉ chẳng liên quan"; nếu vậy, **xáo nhãn ngẫu nhiên** cũng ra chênh lệch cỡ thật. p =
tỷ lệ lần xáo lệch bằng hoặc hơn chênh thật (**kiểm định hoán vị**).

**Kết quả.**""")

    nb.py(r"""def hoan_vi(yy, nhom, so_lan=9999, seed=2026):
    yy, nhom = np.asarray(yy, float), np.asarray(nhom, bool)
    that = yy[nhom].mean() - yy[~nhom].mean()
    rng = np.random.default_rng(seed)
    k = 0
    for _ in range(so_lan):
        p_ = rng.permutation(nhom)                                  # xáo nhãn, giữ nguyên các con số
        k += abs(yy[p_].mean() - yy[~p_].mean()) >= abs(that)       # lệch về phía nào cũng tính
    return that, (k + 1) / (so_lan + 1)


n12 = d[d.yr == 1]
ct = n12[n12.weekday.isin([0, 6])]
for ten, yy, nhom in [("làm việc − nghỉ", n12.cnt, n12.workingday == 1), ("thứ Bảy − Chủ nhật", ct.cnt, ct.weekday == 6)]:
    that, p = hoan_vi(yy, nhom)
    print(f"{ten:<20} {nhom.sum()} và {(~nhom).sum()} ngày | chênh {that:+.0f} lượt/ngày | p = {p:.3f}")""")

    nb.md(r"""Làm việc − nghỉ: p = 0,025 < 0,05 → khác biệt thật. Thứ Bảy − Chủ nhật chênh **lớn hơn** (695) mà p = 0,077 →
không bác bỏ: mỗi nhóm chỉ khoảng 50 ngày nên trung bình dao động mạnh. Ba câu hay nói sai: không bác bỏ ≠ chứng minh
$H_0$ đúng; p không phải "xác suất $H_0$ đúng"; "có ý nghĩa thống kê" ≠ "khác biệt lớn".

**Bài học.** p nhỏ hơn ngưỡng thì bác bỏ; không bác bỏ thì chưa kết luận được gì. Xáo nhãn giả định các ngày độc lập —
ngày liền nhau giống nhau thì p thật lớn hơn con số tính được.""")

    # ---------------------------------------------------------------- 6
    nb.khai_niem("khoảng tin cậy", "confidence interval",
                 "khoảng cho một con số **cố định** chưa biết (như trung bình thật), không phải cho một giá trị sắp tới.",
                 "\"trung bình thật mỗi giờ nằm trong 230–240 lượt, tin cậy 95%\" (số minh hoạ).",
                 "cho biết con số tóm tắt của mình chắc chắn tới đâu; càng nhiều dữ liệu độc lập, khoảng càng hẹp.")
    nb.khai_niem("mẫu / tổng thể", "sample / population",
                 "mẫu là số liệu đang có trong tay; tổng thể là mọi giá trị có thể đo nếu đo mãi.",
                 "100 giờ đang có là mẫu; mọi giờ của hệ thống là tổng thể; \"trung bình thật\" là trung bình của tổng thể.",
                 "ta chỉ thấy mẫu nhưng muốn nói về tổng thể — thống kê là cầu nối giữa hai thứ đó.")
    nb.khai_niem("i.i.d.", "independent and identically distributed",
                 "các quan sát **độc lập** (biết lần này không giúp đoán lần kia) và **cùng phân phối** (cùng một \"hộp\").",
                 "các lần tung một xúc xắc là i.i.d.; lượt thuê giờ liền nhau thì **không** (giờ này đông thì giờ sau cũng đông).",
                 "nhiều công thức (và bootstrap thường) giả định i.i.d.; dữ liệu thời gian gần như luôn vi phạm.")
    nb.khai_niem("định lý giới hạn trung tâm (CLT)", "central limit theorem",
                 "trung bình của nhiều số i.i.d. có phân phối gần hình chuông, dao động theo $\\sigma/\\sqrt{n}$ ($\\sigma$ là "
                 "độ dao động của từng số).",
                 "trung bình 100 giờ rút ngẫu nhiên dao động khoảng 181 / √100 ≈ 18 lượt; 400 giờ thì ≈ 9 lượt.",
                 "giải thích vì sao thêm dữ liệu làm khoảng tin cậy hẹp lại — nhưng chậm: gấp 4 dữ liệu chỉ hẹp một nửa.")
    nb.khai_niem("tự hồi quy, AR(1)", "autoregressive model of order 1",
                 "giá trị mới = ρ × giá trị cũ + một cú hích ngẫu nhiên mới. ρ càng gần 1, chuỗi càng \"dai\".",
                 "ρ = 0,7, bước trước 10, cú hích 0,5 → bước này 0,7 × 10 + 0,5 = 7,5.",
                 "mô hình đơn giản nhất cho chuỗi \"nhớ bước trước\" — dùng để mô phỏng và kiểm phương pháp.")
    nb.khai_niem("cỡ mẫu hiệu dụng", "effective sample size",
                 "số quan sát độc lập mà một chuỗi tự tương quan \"đáng giá\"; với AR(1) ≈ $n(1-\\rho)/(1+\\rho)$.",
                 "200 điểm, ρ = 0,7 → 200 × 0,3 / 1,7 ≈ 35 điểm độc lập.",
                 "cho biết khoảng tin cậy tính như i.i.d. hẹp quá bao nhiêu: ở đây phải rộng gấp √(200/35) ≈ 2,4 lần.")
    nb.khai_niem("bootstrap, block bootstrap", "bootstrap, block bootstrap",
                 "bootstrap: rút lại có hoàn lại từ chính dữ liệu, tính lại con số, lặp nghìn lần để xem nó dao động cỡ nào. "
                 "Block bootstrap rút cả khúc liền nhau.",
                 "từ 5, 7, 9 rút ra 7, 7, 5; bản block với khối 2 từ 12, 15, 11, 30, 14 có thể rút (30, 14), (15, 11), (12, 15).",
                 "dựng khoảng tin cậy không cần công thức; bản block giữ được sự phụ thuộc giữa các thời điểm liền nhau.")
    nb.md(r"""## 6. Dữ liệu theo thời gian cần block bootstrap, không phải rút từng điểm

**Vấn đề.** Trung bình lượt thuê năm 2012 chắc chắn tới đâu? Cần một khoảng tin cậy — khác khoảng dự báo ở phần 3 (cho
một giá trị sắp tới).

**Lý do.** Bootstrap rút lại từ chính mẫu nghìn lần rồi lấy quantile 0,025 và 0,975 của các trung bình. Nhưng giờ liền
nhau "biết" nhau (tự tương quan 0,84): 200 giờ liền nhau chỉ đáng giá như vài chục giờ độc lập. Rút **từng điểm** xé rời
chúng → khoảng quá hẹp. **Block bootstrap** rút cả **khối** điểm liền nhau để giữ sự phụ thuộc.

**Kết quả.** Mô phỏng 300 chuỗi AR(1) có trung bình thật bằng 0 và ρ = 0,7; đếm bao nhiêu khoảng "95%" chứa được 0:""")

    nb.py(r"""def ar1(n, rho, rng):
    e = rng.normal(size=n)
    x = np.empty(n)
    x[0] = e[0] / np.sqrt(1 - rho**2)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + e[t]
    return x


def khoang_tin_cay(x, khoi, so_lan=999, seed=0):
    rng, n = np.random.default_rng(seed), x.size
    if khoi <= 1:
        cs = rng.integers(0, n, size=(so_lan, n))                                  # rút từng điểm
    else:
        bat_dau = rng.integers(0, n - khoi + 1, size=(so_lan, int(np.ceil(n / khoi))))
        cs = (bat_dau[:, :, None] + np.arange(khoi)).reshape(so_lan, -1)[:, :n]    # rút khối liền nhau
    return np.quantile(x[cs].mean(axis=1), [0.025, 0.975])


rng = np.random.default_rng(2026)
chuoi = [ar1(200, 0.7, rng) for _ in range(300)]
for khoi in (1, 3, 6, 10, 20, 40):
    trung = np.mean([lo <= 0 <= hi for i, x in enumerate(chuoi) for lo, hi in [khoang_tin_cay(x, khoi, seed=2026 + i)]])
    print(f"khối {khoi:>2}: {trung:.1%} khoảng chứa trung bình thật")""")

    nb.md(r"""Rút từng điểm (khối 1) hứa 95% mà chỉ giữ được khoảng **60%**. Khối dài dần thì tốt lên, đỉnh gần 90% ở khối 10–20,
rồi tụt lại ở khối 40 (khối quá dài thì hai đầu chuỗi hiếm khi vào mẫu, các mẫu lại giống nhau, khoảng lại hẹp).

**Bài học.** Dữ liệu tự tương quan chứa ít thông tin hơn số điểm của nó; rút từng điểm cho khoảng quá tự tin. Rút khối
sửa phần lớn, nhưng độ dài khối là quyết định nhạy — luôn thử vài độ dài.""")

    # ---------------------------------------------------------------- 7
    nb.md(r"""## 7. Bài tập về nhà — đáp số

**Bài 1 — Khoảng tin cậy cho lượt thuê theo ngày 2012**, rút từng ngày và rút khối 7, 14, 30 ngày:""")

    nb.py(r"""ngay12 = n12.cnt.to_numpy(float)
for khoi in (1, 7, 14, 30):
    lo, hi = khoang_tin_cay(ngay12, khoi, so_lan=9999, seed=2026)
    print(f"khối {khoi:>2}: [{lo:,.0f}; {hi:,.0f}]  rộng {hi - lo:,.0f}")""")

    nb.md(r"""Khối càng dài, khoảng càng rộng — rút từng ngày tự tin quá mức. Báo quản lý khoảng của khối dài, kèm cảnh báo rằng
độ rộng còn phụ thuộc độ dài khối vì chuỗi có mùa vụ và tăng dần trong năm.

**Bài 2 — Ngày mưa** (`weathersit` ≥ 3) so với ngày còn lại năm 2012:""")

    nb.py(r"""mua = n12.weathersit >= 3
that, p = hoan_vi(n12.cnt, mua)
print(f"{mua.sum()} ngày mưa | chênh {that:+,.0f} lượt/ngày | p = {p:.4f}")""")

    nb.md(r"""Không lần xáo nào lệch cỡ đó → bác bỏ $H_0$: ngày mưa vắng khách hơn thật. Nhưng chỉ có 6 ngày mưa, nên con số
chênh lệch chính xác tới đâu thì không chắc; và ngày liền nhau giống nhau nên p thật lớn hơn một chút.

## Tự kiểm

- [ ] Tính tay quantile 0,8 và trung vị của 5–10 số; nói vì sao máy có thể ra số khác.
- [ ] Nói được cách phạt nào ứng với trung bình, trung vị, quantile.
- [ ] Giải thích vì sao khoảng dựng từ 2011 chỉ phủ khoảng 70% năm 2012, và vì sao phải đếm riêng hai đuôi.
- [ ] Đọc đúng một p-value: nêu $H_0$, so với 0,05, không nói "chứng minh".
- [ ] Giải thích vì sao rút từng điểm chỉ phủ khoảng 60% trên chuỗi tự tương quan.""")
