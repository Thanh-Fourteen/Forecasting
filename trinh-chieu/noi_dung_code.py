"""Nội dung slide code (một slide mỗi mục 4.x), dùng bởi sinh_slide_du_lieu.py.

Soạn từ tools/tu_hoc/buoi_NN.py (buổi 1–13) và buoi-NN/dap-an/*.py (buổi 14–15): code rút gọn, bỏ phần vẽ;
số trong ket_qua lấy từ tai-lieu.md hoặc notebook tự học.
"""

CODE = [
# ============================================================ buổi 1
dict(ma="code-b01-mua-vu", buoi=1, sec="4.1",
     tieu="Code: đổi phút ra kWh/giờ, tìm nhịp",
     muc="Biến số đo từng phút thành kWh mỗi giờ, rồi thấy nhịp ngày và tuần làm điện dự báo được.",
     code='''import pandas as pd

df = pd.read_csv("dien-mot-ho.zip", sep=";", na_values="?",
                 usecols=["Date", "Time", "Global_active_power"])
t = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
phut = pd.Series(df["Global_active_power"].to_numpy(), index=t)
# TB kW trong một giờ = số kWh của giờ đó; thiếu quá nửa thì để trống
gio = phut.resample("h")
s = gio.mean().where(gio.count() >= 30)
theo_gio = s.groupby(s.index.hour).mean()       # TB theo giờ trong ngày
print(theo_gio.idxmin(), theo_gio.idxmax())     # giờ thấp nhất, cao nhất
ngay_thuong = s[s.index.dayofweek < 5].mean()   # thứ Hai tới thứ Sáu
cuoi_tuan = s[s.index.dayofweek >= 5].mean()    # thứ Bảy, Chủ nhật''',
     buoc=[("3–6", "Đọc số đo từng phút, gắn mốc thời gian."),
           ("8–9", "Gộp về giờ; giờ thiếu hơn 30 phút để trống."),
           ("10–11", "Trung bình theo giờ trong ngày, tìm đáy, đỉnh."),
           ("12–13", "So ngày thường với cuối tuần.")],
     ham=[("resample(\"h\").mean()", "pandas", "Gom các số đo trong cùng một giờ lại, lấy trung bình."),
          ("groupby(...).mean()", "pandas", "Chia dữ liệu thành nhóm (ví dụ theo giờ), tính trung bình mỗi nhóm."),
          ("idxmin() / idxmax()", "pandas", "Cho biết nhãn (ở đây là giờ) nơi giá trị nhỏ nhất, lớn nhất.")],
     ket_qua="Thấp nhất lúc 4h, cao nhất lúc 20h; cuối tuần dùng nhiều hơn ngày thường. Nhịp lặp đều này là mùa vụ.",
     hinh=(1, "kn-mua-vu"),
     nguon="rút gọn từ buoi-01/tu-hoc.ipynb, phần 0 và 1"),

dict(ma="code-b01-baseline", buoi=1, sec="4.3",
     tieu="Code: MAE và bốn baseline",
     muc="Viết bốn cách dự báo đơn giản làm mốc, để biết một con số MAE là tốt hay xấu.",
     code='''import numpy as np

TAM = 168                                    # dự báo 168 giờ = 7 ngày
def mae(y, du_bao):
    y, du_bao = np.asarray(y, float), np.asarray(du_bao, float)
    co = ~np.isnan(y)                        # bỏ giờ không có số đo
    return float(np.mean(np.abs(y[co] - du_bao[co])))
# ls: lịch sử tới gốc dự báo, chuỗi kWh theo giờ
BASELINE = {
    "giờ trước": lambda ls: np.full(TAM, ls.iloc[-1]),
    "trung bình": lambda ls: np.full(TAM, ls.mean()),
    "tuần trước": lambda ls: ls.iloc[-TAM:].to_numpy(),
    "trung bình 4 tuần": lambda ls: ls.iloc[-4 * TAM:].to_numpy()
                                      .reshape(4, TAM).mean(axis=0),
}''',
     buoc=[("4–7", "MAE: trung bình độ lệch, bỏ giờ trống."),
           ("10", "Naive: lặp lại số cuối cùng đã biết."),
           ("11", "Trung bình mọi giờ đã biết."),
           ("12", "Seasonal naive: cùng giờ tuần trước."),
           ("13–14", "Xếp 4 tuần thành 4 hàng, lấy TB theo cột.")],
     ham=[("np.abs(...).mean()", "numpy", "Bỏ dấu từng sai số rồi lấy trung bình: chính là MAE."),
          ("iloc[-TAM:]", "pandas", "Lấy TAM phần tử cuối của chuỗi theo vị trí, tức tuần gần nhất."),
          ("reshape(4, TAM).mean(axis=0)", "numpy", "Xếp dãy thành bảng 4 hàng, lấy trung bình từng cột.")],
     ket_qua="Chấm cuốn năm 2010: trung bình 4 tuần 0,490; tuần trước 0,576; trung bình 0,652; giờ trước 0,770 kWh/giờ.",
     hinh=(1, "kn-tam-du-bao-h"),
     nguon="rút gọn từ buoi-01/tu-hoc.ipynb, phần 2"),

dict(ma="code-b01-du-bao-cuon", buoi=1, sec="4.4",
     tieu="Code: bảng lịch và dự báo cuốn",
     muc="Chấm như ngoài đời: mỗi tuần chỉ khớp mô hình trên dữ liệu trước gốc dự báo.",
     code='''import pandas as pd
TAM = 168
def khoa(t):                                 # (tuần trong năm, thứ, giờ)
    return [t.isocalendar().week.to_numpy(), t.dayofweek.to_numpy(),
            t.hour.to_numpy()]
def bang_lich(ls):                           # mỗi ô một trung bình
    return ls.groupby(khoa(ls.index)).mean()
def du_bao_lich(bang, t):
    return bang.reindex(pd.MultiIndex.from_arrays(khoa(t))).to_numpy()
def du_bao_cuon(chuoi, moc="2010-01-04"):
    phan = []
    for goc in pd.date_range(moc, chuoi.index[-TAM], freq=f"{TAM}h"):
        t = pd.date_range(goc, periods=TAM, freq="h")
        bang = bang_lich(chuoi[chuoi.index < goc])   # CHỈ quá khứ
        phan.append(pd.Series(du_bao_lich(bang, t), index=t))
    return pd.concat(phan)''',
     buoc=[("3–7", "Bảng lịch: TB theo tuần, thứ, giờ."),
           ("8–9", "Tra bảng cho các giờ cần dự báo."),
           ("12–13", "Mỗi thứ Hai là một gốc, dự báo 168 giờ."),
           ("14", "Khớp bảng chỉ bằng dữ liệu trước gốc."),
           ("15–16", "Ghép dự báo mọi tuần để chấm.")],
     ham=[("groupby([...]).mean()", "pandas", "Nhóm theo nhiều khoá cùng lúc, mỗi tổ hợp ra một trung bình."),
          ("reindex(MultiIndex)", "pandas", "Tra bảng theo danh sách khoá; khoá không có thì ra NaN."),
          ("pd.date_range", "pandas", "Sinh dãy mốc thời gian cách đều, ví dụ mỗi 168 giờ một gốc.")],
     ket_qua="Bảng lập từ cả 4 năm cho MAE 0,380 (sai số ảo). Chấm cuốn 46 tuần: 0,508, thua trung bình 4 tuần (0,490).",
     hinh=(1, "kn-du-bao-cuon"),
     nguon="rút gọn từ buoi-01/tu-hoc.ipynb, phần 3 và 4"),

dict(ma="code-b01-tong-tuan", buoi=1, sec="4.5",
     tieu="Code: chấm theo giờ và theo tổng tuần",
     muc="Cùng một bộ dự báo, chấm ở mức giờ hay mức tuần có thể đổi người thắng.",
     code='''import numpy as np
import pandas as pd

def mae(y, du_bao):
    y, du_bao = np.asarray(y, float), np.asarray(du_bao, float)
    co = ~np.isnan(y)
    return float(np.mean(np.abs(y[co] - du_bao[co])))

# cuon: mỗi dòng một giờ; cột goc, y và các cột dự báo
cot = ["trung bình 4 tuần", "bảng lịch", "tuần trước"]
tuan = cuon.groupby("goc")[["y", *cot]].sum(min_count=1)   # cộng cả tuần
du = cuon.groupby("goc")["y"].apply(lambda x: x.notna().all())
tuan.loc[~du, "y"] = np.nan                     # chỉ chấm tuần đủ số đo
theo_gio = {c: mae(cuon["y"], cuon[c]) for c in cot}
theo_tuan = {c: mae(tuan["y"], tuan[c]) for c in cot}''',
     buoc=[("4–7", "MAE như mục 4.3, bỏ giờ trống."),
           ("11", "Cộng 168 giờ của mỗi gốc thành tổng tuần."),
           ("12–13", "Tuần thiếu số đo thì không chấm."),
           ("14–15", "Tính MAE ở hai mức để so thứ hạng.")],
     ham=[("groupby(\"goc\").sum(min_count=1)", "pandas", "Cộng mọi giờ cùng một gốc; nhóm toàn trống thì ra NaN, không ra 0."),
          ("apply(lambda x: x.notna().all())", "pandas", "Hỏi từng tuần: có đủ số đo ở mọi giờ không."),
          ("tuan.loc[~du, \"y\"]", "pandas", "Chọn các dòng tuần thiếu, cột y, để gán trống.")],
     ket_qua="Theo giờ: TB 4 tuần 0,490 thắng bảng lịch 0,508. Theo tổng tuần: bảng lịch 16,4 thắng xa TB 4 tuần 27,9 kWh/tuần.",
     hinh=(1, "tong-tuan"),
     nguon="rút gọn từ buoi-01/tu-hoc.ipynb, phần 5"),

dict(ma="code-b01-newsvendor", buoi=1, sec="4.6",
     tieu="Code: thiếu đắt hơn thừa, mua quantile",
     muc="Thử từng mức mua để thấy mức rẻ nhất là quantile 0,8, rồi áp vào dữ liệu điện thật.",
     code='''import numpy as np

nhu_cau = np.array([7, 5, 9, 6, 8, 12, 6, 9, 7, 8])       # kWh, 10 ngày
chi_phi = {m: int(4 * np.clip(nhu_cau - m, 0, None).sum()  # thiếu: 4 đồng
                  + np.clip(m - nhu_cau, 0, None).sum())   # thừa: 1 đồng
           for m in range(6, 13)}
q08 = np.quantile(nhu_cau, 0.8, method="inverted_cdf")     # 4 / (4 + 1)

def tien_mat(y, f):
    d = np.asarray(y, float) - np.asarray(f, float)
    d = d[~np.isnan(d)]
    return float(np.mean(np.where(d > 0, 4 * d, -1 * d)))

# c09: dự báo cuốn năm 2009; chọn mức cộng thêm mà không nhìn 2010
q = float((c09["y"] - c09["trung bình 4 tuần"]).dropna().quantile(0.8))
print(tien_mat(y, f), tien_mat(y, f + q))       # năm 2010: trước, sau''',
     buoc=[("3–6", "Tính tiền mất 10 ngày cho mỗi mức mua 6–12."),
           ("7", "Quantile 0,8 của nhu cầu, đếm như tính tay."),
           ("9–12", "Tiền mất: thiếu phạt 4, thừa phạt 1."),
           ("14–15", "Lấy quantile 0,8 sai số 2009 làm phần cộng."),
           ("16", "So tiền mất năm 2010 trước và sau khi cộng.")],
     ham=[("np.clip(x, 0, None)", "numpy", "Cắt số âm về 0: chỉ giữ phần thiếu (hoặc phần thừa)."),
          ("np.quantile(..., method=\"inverted_cdf\")", "numpy", "Tìm quantile đúng cách đếm tay, không nội suy."),
          ("np.where(d > 0, a, b)", "numpy", "Chọn từng phần tử: điều kiện đúng lấy a, sai lấy b.")],
     ket_qua="Mua 9 kWh rẻ nhất (28 đồng) = quantile 0,8, không phải TB 7,7. Thật: cộng 0,455 kWh, tiền mất 1,213 xuống 0,987 (−18,6%), MAE tệ đi.",
     hinh=(1, "kn-bai-toan-newsvendor"),
     nguon="rút gọn từ buoi-01/tu-hoc.ipynb, phần 6"),

# ============================================================ buổi 2
dict(ma="code-b02-quantile", buoi=2, sec="4.1",
     tieu="Code: quantile, trung vị, trung bình",
     muc="Tính quantile như đếm tay, và thấy trung bình với trung vị lệch nhau trên dữ liệu thật.",
     code='''import zipfile

import numpy as np
import pandas as pd

x9 = np.array([8, 2, 36, 5, 12, 3, 18, 6, 9])
np.sort(x9)                                    # 2 3 5 6 8 9 12 18 36
np.quantile(x9, 0.8, method="inverted_cdf")    # đếm tay: số thứ 8
np.quantile(x9, 0.8)                           # mặc định: nội suy

with zipfile.ZipFile("bike-sharing.zip") as z:
    h = pd.read_csv(z.open("hour.csv"), parse_dates=["dteday"])
y = h["cnt"].to_numpy(float)                   # lượt thuê từng giờ
print(y.mean(), np.median(y), np.quantile(y, 0.9))''',
     buoc=[("6–7", "Chín giờ, xếp tăng dần để đếm."),
           ("8", "Vị trí 0,8 × 9 = 7,2, làm tròn lên số thứ 8."),
           ("9", "Máy mặc định nội suy giữa hai số kề nhau."),
           ("11–13", "Đọc lượt thuê theo giờ của Capital Bikeshare."),
           ("14", "So trung bình, trung vị, quantile 0,9.")],
     ham=[("np.quantile(x, q)", "numpy", "Tìm mốc mà tỷ lệ q số liệu nằm dưới hoặc bằng nó."),
          ("np.median(x)", "numpy", "Trung vị: mốc chia đôi, bằng quantile 0,5."),
          ("pd.read_csv(z.open(...))", "pandas", "Đọc tệp CSV nằm bên trong tệp nén thành bảng.")],
     ket_qua="Đếm tay ra 18, máy mặc định ra 14,4. Dữ liệu thật: trung bình 189, trung vị 142, quantile 0,9 khoảng 451 lượt/giờ.",
     hinh=(2, "kn-quantile-trung-vi"),
     nguon="rút gọn từ buoi-02/tu-hoc.ipynb, phần 0 và 1"),

dict(ma="code-b02-pinball", buoi=2, sec="4.2",
     tieu="Code: ba cách phạt, ba con số tốt nhất",
     muc="Thấy bằng số: cách phạt sai quyết định nên báo trung bình, trung vị hay quantile.",
     code='''import numpy as np
import pandas as pd

x9 = np.array([8, 2, 36, 5, 12, 3, 18, 6, 9])
s = x9.std(ddof=1)                             # chia n − 1

def pinball(y, c, tau):
    sai = np.asarray(y, float) - c
    return float(np.where(sai >= 0, tau * sai, (tau - 1) * sai).mean())

bang = pd.DataFrame({c: {"tuyệt đối": np.abs(x9 - c).mean(),
                         "bình phương": ((x9 - c) ** 2).mean(),
                         "pinball 0,8": pinball(x9, c, 0.8)}
                     for c in (8, 11, 18)}).T  # trung vị, TB, quantile 0,8''',
     buoc=[("5", "Độ lệch chuẩn mẫu, chia cho n − 1."),
           ("7–9", "Pinball: thiếu phạt tau, thừa phạt 1 − tau."),
           ("11–14", "Báo cùng một số c cho 9 giờ, tính ba mức phạt.")],
     ham=[("x.std(ddof=1)", "numpy", "Độ lệch chuẩn; ddof=1 nghĩa là chia cho n − 1 thay vì n."),
          ("np.where(sai >= 0, ...)", "numpy", "Phạt khác nhau cho dự báo thấp (sai dương) và dự báo cao."),
          ("pd.DataFrame({...}).T", "pandas", "Dựng bảng từ từ điển rồi xoay: mỗi c một dòng.")],
     ket_qua="s = 10,57. Tuyệt đối thấp nhất ở c = 8 (6,56), bình phương ở c = 11 (99,3), pinball 0,8 ở c = 18 (3,40).",
     hinh=(2, "kn-pinball-loss"),
     nguon="rút gọn từ buoi-02/tu-hoc.ipynb, phần 2"),

dict(ma="code-b02-ty-le-phu", buoi=2, sec="4.3",
     tieu="Code: khoảng 95% và tỷ lệ phủ",
     muc="Dựng khoảng từ năm 2011 hai cách, rồi đếm tỷ lệ phủ và từng đuôi trên năm chưa dùng.",
     code='''import numpy as np
import pandas as pd

# h: bảng lượt thuê theo giờ; yr = 0 là 2011, yr = 1 là 2012
cach = {"±1,96s": lambda x: (x.mean() - 1.96 * x.std(ddof=1),
                             x.mean() + 1.96 * x.std(ddof=1)),
        "quantile": lambda x: tuple(np.quantile(x, [0.025, 0.975]))}
n11, n12 = h[h.yr == 0], h[h.yr == 1]
for ten, f in cach.items():
    k = pd.DataFrame([(g, *f(nhom["cnt"])) for g, nhom in n11.groupby("hr")],
                     columns=["hr", "lo", "hi"])        # dựng từ 2011
    for du in (n11, n12):
        m = du.merge(k, on="hr")
        phu = np.mean((m.cnt >= m.lo) & (m.cnt <= m.hi))
        duoi, tren = np.mean(m.cnt < m.lo), np.mean(m.cnt > m.hi)''',
     buoc=[("5–7", "Hai cách dựng khoảng: công thức và quantile."),
           ("10–11", "Mỗi giờ trong ngày một khoảng, chỉ từ 2011."),
           ("13", "Gắn khoảng của đúng giờ vào từng dòng."),
           ("14", "Tỷ lệ phủ: thật rơi vào trong khoảng."),
           ("15", "Đếm riêng hai đuôi để biết lệch phía nào.")],
     ham=[("np.quantile(x, [0.025, 0.975])", "numpy", "Lấy hai mốc chặn 2,5% dưới và 2,5% trên của lịch sử."),
          ("groupby(\"hr\")", "pandas", "Chia bảng theo giờ trong ngày để mỗi giờ có khoảng riêng."),
          ("merge(k, on=\"hr\")", "pandas", "Nối hai bảng theo cột chung hr, như dò bảng.")],
     ket_qua="Trên 2011: ±1,96s phủ 96,4%, quantile 95,3%. Trên 2012: chỉ 72,5% và 70,1%, vượt trên 27,4% và 29,3%.",
     hinh=(2, "kn-ty-le-phu"),
     nguon="rút gọn từ buoi-02/tu-hoc.ipynb, phần 3"),

dict(ma="code-b02-tuong-quan", buoi=2, sec="4.4",
     tieu="Code: hệ số r và tự tương quan",
     muc="Đo r bằng NumPy, thấy r bỏ sót quan hệ cong, và cao giả khi có biến gây nhiễu.",
     code='''import numpy as np

xu = np.array([-2, -1, 0, 1, 2])
np.corrcoef(xu, xu**2)[0, 1]                   # cong hoàn toàn mà r = 0
# h: bảng lượt thuê theo giờ, có cột temp, hr, cnt
g17 = h[h.hr == 17]                            # giữ cố định giờ
r_nhiet = np.corrcoef(h.temp, h.cnt)[0, 1]
r_nhiet_17 = np.corrcoef(g17.temp, g17.cnt)[0, 1]
r_gio = np.corrcoef(h.hr, h.cnt)[0, 1]         # mạnh nhưng cong
y = h["cnt"].to_numpy(float)
dc = y - y.mean()                              # độ lệch khỏi trung bình
tu_tq = (dc[1:] * dc[:-1]).sum() / (dc**2).sum()   # giờ này, giờ trước''',
     buoc=[("3–4", "y = x² phụ thuộc hẳn vào x mà r bằng 0."),
           ("6–8", "r nhiệt độ: mọi giờ, rồi chỉ lúc 17h."),
           ("9", "Giờ trong ngày quyết định mạnh nhưng r thấp."),
           ("10–12", "Tự tương quan trễ 1 tính tay bằng NumPy.")],
     ham=[("np.corrcoef(x, y)[0, 1]", "numpy", "Trả bảng 2 × 2 hệ số r; ô [0, 1] là r giữa x và y."),
          ("h[h.hr == 17]", "pandas", "Lọc giữ các dòng thoả điều kiện, ở đây là giờ 17."),
          ("dc[1:] * dc[:-1]", "numpy", "Nhân mỗi điểm với điểm ngay trước nó, để đo giống nhau.")],
     ket_qua="y = x² cho r = 0. Nhiệt độ: mọi giờ r = 0,405, chỉ 17h r = 0,588. Giờ trong ngày r = 0,394. Tự tương quan trễ 1: 0,844.",
     hinh=(2, "kn-tuong-quan-he-so-r"),
     nguon="rút gọn từ buoi-02/tu-hoc.ipynb, phần 4"),

dict(ma="code-b02-hoan-vi", buoi=2, sec="4.5",
     tieu="Code: kiểm định hoán vị",
     muc="Tính p-value bằng cách xáo nhãn: nếu nhãn vô nghĩa, chênh lệch cỡ thật có hiếm không?",
     code='''import numpy as np

def hoan_vi(yy, nhom, so_lan=9999, seed=2026):
    yy, nhom = np.asarray(yy, float), np.asarray(nhom, bool)
    that = yy[nhom].mean() - yy[~nhom].mean()
    rng = np.random.default_rng(seed)
    k = 0
    for _ in range(so_lan):
        p_ = rng.permutation(nhom)                  # xáo nhãn, giữ số
        k += abs(yy[p_].mean() - yy[~p_].mean()) >= abs(that)
    return that, (k + 1) / (so_lan + 1)

# d: bảng lượt thuê theo ngày; yr = 1 là năm 2012
n12 = d[d.yr == 1]
that, p = hoan_vi(n12.cnt, n12.workingday == 1)''',
     buoc=[("5", "Chênh lệch thật giữa hai nhóm ngày."),
           ("6", "Cố định seed để chạy lại ra cùng p."),
           ("8–10", "Xáo nhãn 9.999 lần, đếm lần lệch bằng hoặc hơn."),
           ("11", "p là tỷ lệ lần xáo lệch cỡ thật."),
           ("14–15", "Ngày làm việc so với ngày nghỉ năm 2012.")],
     ham=[("np.random.default_rng(seed)", "numpy", "Tạo bộ sinh số ngẫu nhiên; cùng seed thì ra cùng dãy."),
          ("rng.permutation(nhom)", "numpy", "Xáo trộn thứ tự nhãn, giữ nguyên số nhãn mỗi loại."),
          ("yy[nhom].mean()", "numpy", "Trung bình của các phần tử có nhãn True.")],
     ket_qua="Làm việc − nghỉ chênh +456 lượt/ngày, p = 0,025 < 0,05: bác bỏ H0. Thứ Bảy − CN chênh +695 mà p > 0,05.",
     hinh=(2, "kn-kiem-dinh-gia-thuyet-khong-h0"),
     nguon="rút gọn từ buoi-02/tu-hoc.ipynb, phần 5"),

dict(ma="code-b02-block-bootstrap", buoi=2, sec="4.6",
     tieu="Code: bootstrap từng điểm và rút khối",
     muc="Dựng khoảng tin cậy bằng rút lại mẫu, và thấy rút khối sửa được khoảng quá tự tin.",
     code='''import numpy as np

def khoang_tin_cay(x, khoi, so_lan=999, seed=0):
    rng, n = np.random.default_rng(seed), x.size
    if khoi <= 1:
        cs = rng.integers(0, n, size=(so_lan, n))          # từng điểm
    else:
        so_khoi = int(np.ceil(n / khoi))
        bat_dau = rng.integers(0, n - khoi + 1, size=(so_lan, so_khoi))
        cs = (bat_dau[:, :, None] + np.arange(khoi)).reshape(so_lan, -1)
    return np.quantile(x[cs[:, :n]].mean(axis=1), [0.025, 0.975])
# chuoi: 300 chuỗi AR(1), rho = 0,7, trung bình thật bằng 0
for khoi in (1, 3, 6, 10, 20, 40):
    kq = [khoang_tin_cay(x, khoi, seed=2026 + i)
          for i, x in enumerate(chuoi)]
    phu = np.mean([lo <= 0 <= hi for lo, hi in kq])''',
     buoc=[("5–6", "Rút ngẫu nhiên có hoàn lại từng điểm."),
           ("8–10", "Rút điểm đầu khối, nối khối liền nhau."),
           ("11", "Quantile của 999 trung bình ra khoảng 95%."),
           ("13–16", "Đếm bao nhiêu khoảng chứa trung bình thật 0.")],
     ham=[("rng.integers(0, n, size=...)", "numpy", "Sinh vị trí ngẫu nhiên từ 0 tới n − 1, lặp lại được."),
          ("x[cs].mean(axis=1)", "numpy", "Lấy các điểm theo vị trí đã rút, trung bình từng lần rút."),
          ("np.arange(khoi)", "numpy", "Dãy 0, 1, …, khoi − 1, cộng vào điểm đầu thành một khối.")],
     ket_qua="Rút từng điểm: chỉ 60,3% khoảng chứa trung bình thật. Khối 10: 89,0%; khối 20: 89,3%; khối 40 tụt còn 81,3%.",
     hinh=(2, "kn-bootstrap-block-bootstrap"),
     nguon="rút gọn từ buoi-02/tu-hoc.ipynb, phần 6"),

# ============================================================ buổi 3
dict(ma="code-b03-dst", buoi=3, sec="4.1",
     tieu="Code: gắn múi giờ New York, đổi UTC",
     muc="Thấy một giờ New York có thể ứng với một, không, hoặc hai thời điểm UTC.",
     code='''import pandas as pd

NY = "America/New_York"
for ngay, gio in [("2024-03-10", "01:30"), ("2024-03-10", "02:30"),
                  ("2024-03-10", "03:30"), ("2024-11-03", "01:30")]:
    ket_qua = []
    for mua_he in (True, False):             # giờ lặp: EDT hay EST
        try:
            t = pd.Timestamp(f"{ngay} {gio}").tz_localize(
                NY, ambiguous=mua_he)        # gắn múi giờ New York
            ket_qua.append(t.tz_convert("UTC").strftime("%H:%MZ"))
        except Exception:                    # giờ không tồn tại
            pass
    print(ngay, gio, sorted(set(ket_qua)) or "KHÔNG TỒN TẠI")''',
     buoc=[("4–5", "Bốn giờ quanh hai ngày vặn đồng hồ 2024."),
           ("7", "Thử cả hai cách hiểu: giờ hè và giờ đông."),
           ("9–10", "Gắn múi giờ: con số giờ thành thời điểm thật."),
           ("11", "Đổi sang UTC, trục thời gian chạy đều."),
           ("12–13", "Giờ bị nhảy qua thì báo lỗi, bỏ qua.")],
     ham=[("tz_localize(NY, ambiguous=...)", "pandas", "Gắn múi giờ cho giờ chưa có; ambiguous chọn EDT hay EST."),
          ("tz_convert(\"UTC\")", "pandas", "Đổi một thời điểm đã có múi giờ sang giờ UTC."),
          ("strftime(\"%H:%MZ\")", "pandas", "Viết thời điểm thành chữ theo mẫu giờ:phút kèm chữ Z.")],
     ket_qua="10/3: 01:30 ra 06:30Z, 02:30 không tồn tại, 03:30 ra 07:30Z. 01:30 ngày 3/11 có hai đáp án: 05:30Z hoặc 06:30Z.",
     hinh=(3, "kn-gio-mua-he-dst"),
     nguon="rút gọn từ buoi-03/tu-hoc.ipynb, phần 1"),

dict(ma="code-b03-dem-naive", buoi=3, sec="4.2",
     tieu="Code: đếm chuyến trên giờ naive",
     muc="Đếm thẳng trên giờ không múi giờ để thấy giờ 0 chuyến giả và giờ gấp đôi.",
     code='''import pandas as pd

cot = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]
t3 = pd.read_parquet("yellow_tripdata_2024-03.parquet", columns=cot)
t11 = pd.read_parquet("yellow_tripdata_2024-11.parquet", columns=cot)

def dem_naive(chuyen):                      # đếm thẳng trên giờ naive
    return chuyen.set_index("tpep_pickup_datetime").resample("h").size()

dem_naive(t3)["2024-03-10 00:00":"2024-03-10 03:00"]    # 02:00 trống
dem_naive(t11)["2024-11-03 00:00":"2024-11-03 03:00"]   # 01:00 gấp đôi
dem_naive(t11)["2024-11-10 01:00"]                      # tuần sau để so
# trừ thẳng hai giờ naive: có khách xuống xe trước khi lên
am = t11["tpep_dropoff_datetime"] < t11["tpep_pickup_datetime"]''',
     buoc=[("3–5", "Đọc giờ đón, giờ trả của tháng 3 và 11."),
           ("7–8", "Đếm chuyến mỗi giờ, chưa gắn múi giờ."),
           ("10–11", "Xem quanh hai ngày vặn đồng hồ."),
           ("12", "Cùng giờ tuần sau làm mốc so."),
           ("14", "Tìm chuyến trả trước khi đón.")],
     ham=[("pd.read_parquet(..., columns=...)", "pandas", "Đọc tệp Parquet, chỉ lấy các cột cần cho nhanh."),
          ("set_index(...).resample(\"h\").size()", "pandas", "Lấy cột giờ làm mốc, đếm số dòng rơi vào mỗi giờ."),
          ("s[\"a\":\"b\"]", "pandas", "Cắt chuỗi theo khoảng thời gian, lấy cả hai đầu.")],
     ket_qua="Giờ 02:00 ngày 10/3 có 0 chuyến; giờ 01:00 ngày 3/11 có 9.869 chuyến, gần gấp đôi tuần sau (5.318).",
     hinh=(3, "dst-hai-ngay"),
     nguon="rút gọn từ buoi-03/tu-hoc.ipynb, phần 2"),

dict(ma="code-b03-resample", buoi=3, sec="4.3",
     tieu="Code: resample cộng hay trung bình",
     muc="Gộp sự kiện thành chuỗi đều: đếm thì cộng, số đo thì lấy trung bình.",
     code='''import pandas as pd

t = pd.to_datetime(["2024-01-01 00:10", "2024-01-01 00:50",
                    "2024-01-01 02:20"])
s = pd.Series([1.0, 2.0, 5.0], index=t)
s.resample("h").sum()       # số lượng: cộng, giờ trống ra 0
s.resample("h").mean()      # số đo: trung bình, giờ trống ra NaN
# cách khác: floor về đầu giờ; không tự thêm giờ trống
s.groupby(s.index.floor("h")).sum()
# tháng 3 New York: ngày 10/3 chỉ dài 23 giờ
gio = pd.date_range("2024-03-01", "2024-04-01", freq="h",
                    tz="America/New_York", inclusive="left")
len(gio)''',
     buoc=[("3–5", "Ba sự kiện lúc 00:10, 00:50, 02:20."),
           ("6", "Cộng theo giờ; giờ 01:00 không có gì ra 0."),
           ("7", "Trung bình theo giờ; giờ trống ra NaN."),
           ("9", "Làm tròn xuống đầu giờ rồi cộng, thiếu giờ 01."),
           ("11–13", "Đếm số giờ thật của tháng 3.")],
     ham=[("resample(\"h\")", "pandas", "Chia trục thời gian thành từng giờ, mỗi giờ gộp thành một số."),
          ("index.floor(\"h\")", "pandas", "Làm tròn mỗi mốc xuống đầu giờ: 9:40 thành 9:00."),
          ("pd.date_range(..., tz=...)", "pandas", "Sinh lưới giờ theo múi giờ, tự bỏ giờ bị nhảy qua.")],
     ket_qua="Cộng ra [3, 0, 5], trung bình ra [1,5; NaN; 5], floor chỉ ra [3, 5]. Tháng 3 có 743 giờ, không phải 744.",
     hinh=(3, "kn-closed-label"),
     nguon="rút gọn từ buoi-03/tu-hoc.ipynb, phần 3"),

dict(ma="code-b03-ghep-utc", buoi=3, sec="4.4",
     tieu="Code: ghép hai nguồn trên cùng UTC",
     muc="Đưa cả hai bảng về UTC rồi mới ghép; ghép gần nhất thì chỉ nhìn về quá khứ.",
     code='''import pandas as pd

NY = "America/New_York"
# t3: chuyến taxi (giờ NY naive); tt: thời tiết (giờ UTC naive)
tt["ds"] = pd.to_datetime(tt["time"]).dt.tz_localize("UTC")
utc = t3["tpep_pickup_datetime"].dt.tz_localize(
    NY, ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
dem = utc.dt.floor("h").value_counts().rename("y").rename_axis("ds")
dung = dem.reset_index().merge(tt, on="ds")        # cùng UTC mới ghép
gio_ny = dung["ds"].dt.tz_convert(NY).dt.hour
nong = dung.groupby(gio_ny)["nhiet_do"].mean().idxmax()   # phép thử
# bảng phải thưa: lấy giá gần nhất đã có, không nhìn tương lai
trai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 10:00"])})
phai = pd.DataFrame({"t": pd.to_datetime(["2024-01-01 09:30",
                     "2024-01-01 10:30"]), "gia": [9, 10]})
pd.merge_asof(trai, phai, on="t")              # backward: nhìn quá khứ''',
     buoc=[("5", "Thời tiết vốn là UTC: chỉ cần ghi rõ ra."),
           ("6–7", "Taxi: gắn giờ New York, đổi UTC; mơ hồ ra NaT."),
           ("8–9", "Đếm chuyến mỗi giờ UTC, ghép với thời tiết."),
           ("10–11", "Phép thử: giờ nóng nhất phải là buổi chiều."),
           ("13–16", "Ghép as-of, mặc định lấy giá đã có trước.")],
     ham=[("dt.tz_localize(..., nonexistent=\"NaT\")", "pandas", "Gắn múi giờ cho cả cột; giờ không tồn tại hay lặp ghi NaT."),
          ("merge(tt, on=\"ds\")", "pandas", "Nối hai bảng theo cột thời gian chung ds."),
          ("pd.merge_asof", "pandas", "Nối mỗi dòng với dòng gần nhất ở trước nó theo thời gian.")],
     ket_qua="Giờ nóng nhất: ghép sai 20h, ghép đúng 16h. Tương quan mưa–số chuyến: sai −0,100, đúng +0,136. merge_asof lấy giá 9.",
     hinh=(3, "kn-ghep-as-of-merge-asof"),
     nguon="rút gọn từ buoi-03/tu-hoc.ipynb, phần 4"),

dict(ma="code-b03-dang-dai", buoi=3, sec="4.5",
     tieu="Code: dạng dài trên một lưới chung",
     muc="Dựng bảng unique_id, ds, y cho mọi khu vực, đủ mọi giờ, giờ không có chuyến ghi 0.",
     code='''import pandas as pd

# t3: chuyến tháng 3; utc: giờ đón đã đổi UTC như mục 4.4
kv = t3.assign(ds=utc.dt.floor("h")).dropna(subset=["ds"])
dem = kv.groupby(["PULocationID", "ds"]).size()    # chỉ giờ có chuyến
luoi = pd.date_range("2024-03-01 05:00", "2024-04-01 04:00", freq="h",
                     tz="UTC", inclusive="left")   # [đầu, cuối)
day_du = pd.MultiIndex.from_product([dem.index.levels[0], luoi],
                                    names=["unique_id", "ds"])
dai = dem.reindex(day_du, fill_value=0).rename("y").reset_index()
ty_le_0 = (dai["y"] == 0).mean()                   # tỷ lệ ô bằng 0''',
     buoc=[("4", "Làm tròn giờ đón UTC xuống đầu giờ."),
           ("5", "Đếm chuyến theo khu vực và giờ."),
           ("6–7", "Lưới giờ UTC của cả tháng 3 New York."),
           ("8–10", "Mọi khu vực nhân mọi giờ; giờ vắng ghi 0."),
           ("11", "Xem bao nhiêu ô bằng 0.")],
     ham=[("pd.MultiIndex.from_product", "pandas", "Tạo mọi cặp (khu vực, giờ) từ hai danh sách."),
          ("reindex(..., fill_value=0)", "pandas", "Trải số đếm lên lưới đủ; cặp chưa có thì điền 0."),
          ("reset_index()", "pandas", "Biến chỉ mục thành cột thường: ra bảng ba cột dạng dài.")],
     ket_qua="192.437 dòng = 259 khu vực × 743 giờ, không mất chuyến nào; 53,7% số ô bằng 0.",
     hinh=(3, "kn-backtest"),
     nguon="rút gọn từ buoi-03/tu-hoc.ipynb, phần 5"),
dict(ma="code-b04-ba-mau-hinh", buoi=4, sec="4.1", tieu="Code: tách xu hướng và mùa vụ tuần",
     muc="Tính tay hai tuần để thấy mùa vụ là phần lặp lại, rồi gộp dữ liệu thật theo ngày, tháng.",
     code='''import numpy as np
import pandas as pd

# hai tuần, trăm lượt mỗi ngày, từ T2 tới CN
tuan = np.array([[10, 12, 12, 12, 14, 6, 4],
                 [12, 14, 14, 14, 16, 8, 6]])
tb = tuan.mean(axis=1, keepdims=True)    # trung bình mỗi tuần
lech = tuan - tb                         # phần lệch: mùa vụ tuần

# df: lượt thuê theo giờ, đặt trên lưới giờ đầy đủ
ngay = df["cnt"].resample("D").sum(min_count=12)  # thiếu giờ ra NaN
thang = df["cnt"].resample("MS").sum()
print(ngay.nsmallest(3))                 # những ngày rơi sát 0''',
     buoc=[("4–6", "Hai tuần số nhỏ, tuần sau cao hơn tuần trước."),
           ("7", "Trung bình tuần đi từ 10 lên 12: xu hướng."),
           ("8", "Trừ trung bình, phần còn lại là mùa vụ tuần."),
           ("11–12", "Gộp giờ thành ngày và tháng để nhìn đủ tầng."),
           ("13", "Tìm ngày thấp bất thường mà hình tháng giấu.")],
     ham=[("mean(axis=1, keepdims=True)", "numpy", "Trung bình theo từng dòng, giữ dạng cột để trừ được cả bảng."),
          ("resample(\"D\").sum(min_count=12)", "pandas", "Cộng các giờ thành tổng ngày; ngày dưới 12 giờ số liệu để trống."),
          ("nsmallest(3)", "pandas", "Lấy ba giá trị nhỏ nhất kèm ngày của chúng.")],
     ket_qua="Trung bình tuần 10 và 12; phần lệch hai tuần giống hệt: 0, 2, 2, 2, 4, −4, −6. Đó là mùa vụ tuần.",
     hinh=(4, "kn-chu-ky"), nguon="rút gọn từ buoi-04/tu-hoc.ipynb, phần 1"),

dict(ma="code-b04-lam-tron-log", buoi=4, sec="4.2", tieu="Code: làm trơn và tăng theo phần trăm",
     muc="Thấy bằng số làm trơn xoá mất ngày bão, và thang log đo tăng theo phần trăm.",
     code='''import pandas as pd

# df: lượt thuê theo giờ, đặt trên lưới giờ đầy đủ
ngay1 = df["cnt"].resample("D").sum(min_count=1)
tron = ngay1.rolling(7, center=True, min_periods=4).mean()
print(ngay1["2012-10-29"], tron["2012-10-29"])   # ngày bão Sandy

th11 = df["cnt"].resample("MS").sum()["2011"]
bang = pd.DataFrame({
    "tăng (lượt)": th11.diff(),           # thang thường hỏi cái này
    "tăng (%)": th11.pct_change() * 100,  # thang log hỏi cái này
})
print(bang.loc["2011-04":"2011-05"].round(1))''',
     buoc=[("4", "Tổng lượt thuê mỗi ngày."),
           ("5", "Trung bình trượt 7 ngày, lấy ngày giữa làm tâm."),
           ("6", "So ngày bão: số thật và số đã làm trơn."),
           ("8", "Tổng tháng của năm 2011."),
           ("9–12", "Tăng bao nhiêu lượt và tăng bao nhiêu phần trăm.")],
     ham=[("rolling(7, center=True).mean()", "pandas", "Trung bình 7 ngày quanh mỗi ngày: 3 ngày trước, 3 ngày sau."),
          ("diff()", "pandas", "Hiệu của mỗi giá trị với giá trị ngay trước nó."),
          ("pct_change()", "pandas", "Tăng bao nhiêu phần so với giá trị trước, ví dụ 0,48 là +48%.")],
     ket_qua="Ngày bão chỉ còn 1 giờ số liệu mà đường trơn vẫn hơn 4.600 lượt. T4 so T3 +48,1%, T5 so T4 +43,2% dù T5 thêm nhiều lượt nhất (+40.951).",
     hinh=(4, "kn-lam-tron-trung-binh-truot"), nguon="rút gọn từ buoi-04/tu-hoc.ipynb, phần 2"),

dict(ma="code-b04-gio-trong-tuan", buoi=4, sec="4.3", tieu="Code: xếp dữ liệu theo giờ trong tuần",
     muc="Xoay bảng cho mỗi tuần một cột để thấy hình dạng mùa vụ, rồi so tổng từng thứ.",
     code='''import pandas as pd

# df: lượt thuê theo giờ, có cột thu (0 là T2) và gio
bang = (df.assign(gio_tuan=df["thu"] * 24 + df["gio"],   # 0 tới 167
                  tuan=df.index.to_period("W-SUN"))
          .pivot_table(index="gio_tuan", columns="tuan", values="cnt"))
khuon = bang.median(axis=1)          # hình dạng tuần điển hình

du = df["cnt"].resample("D").agg(["sum", "count"])
du = du[du["count"] == 24]           # chỉ ngày đủ 24 giờ
tb_thu = du.groupby(du.index.dayofweek)["sum"].mean()''',
     buoc=[("4", "Giờ trong tuần = thứ nhân 24 cộng giờ."),
           ("5", "Gắn nhãn tuần, tuần kết thúc Chủ nhật."),
           ("6", "Mỗi tuần một cột, mỗi dòng một giờ trong tuần."),
           ("7", "Trung vị các tuần: khuôn chung của tuần."),
           ("9–11", "Tổng ngày trung bình theo thứ, bỏ ngày thiếu.")],
     ham=[("pivot_table(index, columns, values)", "pandas", "Xoay bảng dài thành bảng ngang: dòng theo một cột, cột theo cột khác."),
          ("to_period(\"W-SUN\")", "pandas", "Đổi mỗi mốc giờ thành tuần chứa nó, tuần tính tới Chủ nhật."),
          ("groupby(...).mean()", "pandas", "Chia các dòng thành nhóm theo nhãn rồi lấy trung bình mỗi nhóm.")],
     ket_qua="106 tuần chồng nhau: T2–T6 hai đỉnh, T7–CN một bướu. Tổng ngày gần nhau: T7 4.653 lượt so với T6 4.933.",
     hinh=(4, "kn-mua-vu-kep"), nguon="rút gọn từ buoi-04/tu-hoc.ipynb, phần 3"),

dict(ma="code-b04-heatmap-boxplot", buoi=4, sec="4.4", tieu="Code: số cho heatmap và boxplot",
     muc="Tính trung bình từng ô lịch cho heatmap và quantile cho hộp của boxplot.",
     code='''import numpy as np
import pandas as pd

x = np.array([420, 60, 450, 410, 440])   # năm thứ Hai lúc 8h
print(x.mean())                          # bị ngày lễ kéo xuống
print(np.quantile(x, [0.25, 0.5, 0.75], method="inverted_cdf"))

# df: lượt thuê theo giờ, có cột thu, gio, workingday
ho_so = df.pivot_table(index="thu", columns="gio", values="cnt",
                       aggfunc="mean")   # 7 thứ nhân 24 giờ
for lam, g in [(1, 8), (1, 17), (0, 8), (0, 13)]:
    chon = (df["workingday"] == lam) & (df["gio"] == g)
    q = df.loc[chon, "cnt"].quantile([0.25, 0.5, 0.75])  # mép hộp
    print(lam, g, q.round(0).tolist())''',
     buoc=[("4–5", "Trung bình bị một ngày lạ kéo lệch."),
           ("6", "Quantile 0,25, 0,5, 0,75 thì không bị."),
           ("9–10", "Bảng 7 thứ, 24 giờ: đúng số tô lên heatmap."),
           ("11–14", "Hộp từng giờ, tách ngày làm việc và ngày nghỉ.")],
     ham=[("np.quantile(x, q)", "numpy", "Số mà q phần dữ liệu nằm dưới nó; q = 0,5 là trung vị."),
          ("pivot_table(aggfunc=\"mean\")", "pandas", "Bảng hai chiều, mỗi ô là trung bình các dòng rơi vào ô đó."),
          ("quantile([0.25, 0.5, 0.75])", "pandas", "Ba số làm nên cái hộp: mép dưới, vạch giữa, mép trên.")],
     ket_qua="Trung bình 356, trung vị 420, hộp 410–440. 8h: T2 412, CN 84. Hộp 8h ngày nghỉ 57–141, ngày làm việc 365–646.",
     hinh=(4, "kn-boxplot"), nguon="rút gọn từ buoi-04/tu-hoc.ipynb, phần 4"),

dict(ma="code-b04-acf", buoi=4, sec="4.5", tieu="Code: tự tính ACF và r của lag plot",
     muc="Viết công thức tự tương quan vài dòng, kiểm bằng chuỗi nhỏ rồi chạy trên dữ liệu giờ.",
     code='''import numpy as np
import pandas as pd

def acf_nhanh(y, so_tre):
    y = np.asarray(y, dtype=float)
    lech = y - np.nanmean(y)             # độ lệch khỏi trung bình
    mau = np.nansum(lech**2)             # mẫu số: cả chuỗi
    return np.array([1.0] + [np.nansum(lech[k:] * lech[:-k]) / mau
                             for k in range(1, so_tre + 1)])

print(acf_nhanh([2, 4, 6, 4, 2, 4, 6, 4], 4).round(2))
r = acf_nhanh(df["cnt"], 336)            # df: lượt thuê theo giờ
for k in (1, 12, 24, 168):               # r của từng lag plot
    cap = pd.DataFrame({"truoc": df["cnt"].shift(k), "sau": df["cnt"]})
    print(k, cap.dropna().corr().iloc[0, 1])''',
     buoc=[("6–7", "Độ lệch từng điểm và tổng bình phương độ lệch."),
           ("8–9", "Cộng tích lệch bây giờ với lệch k bước trước."),
           ("11", "Kiểm trên chuỗi 2, 4, 6, 4 lặp lại."),
           ("12", "ACF 336 giờ, tức hai tuần, trên dữ liệu thật."),
           ("13–15", "Ghép giờ t với giờ t − k rồi đo tương quan.")],
     ham=[("acf_nhanh(y, so_tre)", "tự viết", "Tính r_k cho k = 1, 2, … theo đúng công thức tự tương quan."),
          ("np.nansum", "numpy", "Cộng các phần tử, bỏ qua ô trống thay vì ra NaN."),
          ("shift(k)", "pandas", "Dời chuỗi xuống k bước: giờ t nhận giá trị của giờ t − k.")],
     ket_qua="Chuỗi nhỏ: r₂ = −0,75, r₄ = 0,5. Dữ liệu thật: r₁₆₈ = 0,864 cao hơn r₁₄₄ = 0,786; lag plot trễ 168 cho r = 0,876.",
     hinh=(4, "kn-acf"), nguon="rút gọn từ buoi-04/tu-hoc.ipynb, phần 5"),

dict(ma="code-b04-tron-nam", buoi=4, sec="4.6", tieu="Code: r từng nhóm thay cho trục kép",
     muc="Đo quan hệ nhiệt độ và lượt thuê bằng số, và thấy trộn hai năm làm quan hệ trông yếu đi.",
     code='''import pandas as pd

# df: lượt thuê theo giờ; temp đã chia cho 41 độ C
th12 = df[df["nam"] == 2012].resample("MS").agg(
    {"cnt": "sum", "temp": "mean"})
r12 = th12["cnt"].corr(th12["temp"])     # quan hệ theo 12 tháng

nd = df.resample("D").agg({"cnt": "sum", "temp": "mean",
                           "nam": "first"}).dropna()
r_nam = {n: g["cnt"].corr(g["temp"]) for n, g in nd.groupby("nam")}
r_gop = nd["cnt"].corr(nd["temp"])       # trộn hai năm vào một

# thay trục kép: đánh chỉ số, tháng đầu bằng 100
chi_so = th12 / th12.iloc[0] * 100''',
     buoc=[("4–5", "Tổng lượt và nhiệt độ trung bình mỗi tháng 2012."),
           ("6", "Hệ số r cho biết hai chuỗi đi cùng nhau tới đâu."),
           ("8–10", "Theo ngày: tính r riêng cho từng năm."),
           ("11", "Gộp hai năm rồi tính r để so."),
           ("14", "Chung một trục mà không cần trục kép.")],
     ham=[("agg({cột: cách gộp})", "pandas", "Gộp mỗi cột một kiểu: cột này cộng, cột kia lấy trung bình."),
          ("corr", "pandas", "Hệ số tương quan r giữa hai cột, từ −1 tới 1."),
          ("groupby(\"nam\")", "pandas", "Chia bảng thành từng năm để tính riêng cho mỗi năm.")],
     ket_qua="12 tháng 2012: r = 0,91. Theo ngày: 2011 r = 0,771, 2012 r = 0,714, nhưng gộp hai năm chỉ còn 0,627.",
     hinh=(4, "kn-truc-y-cat"), nguon="rút gọn từ buoi-04/tu-hoc.ipynb, phần 6"),

dict(ma="code-b05-lich", buoi=5, sec="4.1", tieu="Code: chia số ngày của tháng",
     muc="Thấy chia số ngày có thể đảo dấu kết luận khi so hai tháng liền nhau.",
     code='''import pandas as pd

# y: doanh số bán lẻ Mỹ theo tháng (triệu USD), chưa điều chỉnh
ba = y["2023-01":"2023-03"]
so_ngay = ba.index.days_in_month               # 31, 28, 31
khong_cn = [sum(d.dayofweek != 6 for d in
                pd.date_range(t, t + pd.offsets.MonthEnd(0)))
            for t in ba.index]                 # ngày bán hàng
bang = pd.DataFrame({"tổng": ba, "mỗi ngày": ba / so_ngay,
                     "mỗi ngày không CN": ba / khong_cn})
thay_doi = bang.pct_change() * 100             # % so với tháng trước''',
     buoc=[("4", "Ba tháng đầu năm 2023."),
           ("5", "Số ngày lịch của từng tháng."),
           ("6–8", "Đếm số ngày không phải Chủ nhật."),
           ("9–10", "Doanh số mỗi ngày theo hai cách đếm ngày."),
           ("11", "So mỗi tháng với tháng trước theo phần trăm.")],
     ham=[("index.days_in_month", "pandas", "Số ngày của tháng chứa mỗi mốc: 28, 30 hay 31."),
          ("pd.offsets.MonthEnd(0)", "pandas", "Nhảy tới ngày cuối của chính tháng đó."),
          ("pd.date_range", "pandas", "Tạo dãy ngày liên tiếp từ ngày đầu tới ngày cuối.")],
     ket_qua="T2 so T1: tổng −3,4% nhưng mỗi ngày +7,0%. T3 so T2: +14,15% thẳng, +3,11% chia ngày, +1,47% bỏ CN, −1,05% ADJUSTED.",
     hinh=(5, "dieu-chinh-lich"), nguon="rút gọn từ buoi-05/tu-hoc.ipynb, phần 1"),

dict(ma="code-b05-gia-thuc", buoi=5, sec="4.2", tieu="Code: giá thực và trên đầu người",
     muc="Bóc lạm phát và dân số khỏi doanh số để biết mỗi người thật sự mua thêm bao nhiêu.",
     code='''import pandas as pd

# y: bán lẻ danh nghĩa, cpi: CPI tháng, dan_so: nghìn người
cpi_du = cpi.interpolate(limit=1, limit_area="inside")  # lấp 10/2025
goc = cpi_du["2025"].mean()                    # năm gốc 2025
thuc = y / cpi_du.reindex(y.index) * goc       # đổi ra giá năm gốc
dau_nguoi = thuc / dan_so.reindex(y.index) * 1e6
nam = pd.DataFrame({"danh nghĩa": y, "giá thực": thuc,
                    "thực trên đầu người": dau_nguoi})
nam = nam.resample("YS").sum()["1993":"2025"]
chi_so = nam / nam.iloc[0] * 100               # 1993 bằng 100''',
     buoc=[("4", "Lấp đúng một tháng CPI không công bố."),
           ("5–6", "Chia CPI lúc đó, nhân CPI năm gốc."),
           ("7", "Chia dân số ra mức mỗi người."),
           ("8–10", "Cộng thành tổng năm cho cả ba chuỗi."),
           ("11", "Đánh chỉ số để ba chuỗi so được với nhau.")],
     ham=[("interpolate(limit=1)", "pandas", "Điền ô trống bằng giá trị nằm giữa hai tháng bên cạnh, tối đa một ô."),
          ("reindex(y.index)", "pandas", "Xếp lại chuỗi theo đúng các tháng của y để chia từng tháng."),
          ("resample(\"YS\").sum()", "pandas", "Cộng các tháng thành tổng của từng năm.")],
     ket_qua="Chỉ số 2025: danh nghĩa 416, giá thực 187, thực trên đầu người 142. Giá chung tăng 2,23 lần, dân số 1,31 lần.",
     hinh=(5, "danh-nghia-thuc"), nguon="rút gọn từ buoi-05/tu-hoc.ipynb, phần 2"),

dict(ma="code-b05-log", buoi=5, sec="4.3", tieu="Code: log và dao động theo mức",
     muc="Thấy log biến cùng phần trăm thành cùng khoảng cách, rồi kiểm dao động lớn lên ra sao.",
     code='''import numpy as np

print(np.log([100, 120, 1000, 1200]).round(3))  # cùng tăng 20%
print(np.log(1.2))                     # khoảng cách log của +20%

# y19: doanh số bán lẻ tháng, 1992 tới 2019
v = y19.to_numpy()[y19.size % 12:]
khoi = v.reshape(-1, 12) / 1000        # 28 năm, 12 tháng, tỷ USD
tb = khoi.mean(axis=1)                 # mức mỗi năm
sd = khoi.std(axis=1, ddof=1)          # dao động trong năm
print(tb[-1] / tb[0], sd[-1] / sd[0])''',
     buoc=[("3", "Cửa hàng nhỏ và siêu thị cùng tăng 20%."),
           ("4", "Trên thang log cả hai cách nhau đúng log 1,2."),
           ("7–8", "Cắt chuỗi thành từng năm, mỗi dòng một năm."),
           ("9–10", "Mức và độ lệch chuẩn của từng năm."),
           ("11", "So mức và dao động lớn lên bao nhiêu lần.")],
     ham=[("np.log", "numpy", "Logarit tự nhiên: biến phép nhân thành phép cộng."),
          ("reshape(-1, 12)", "numpy", "Xếp dãy dài thành bảng 12 cột, số dòng tự tính."),
          ("std(axis=1, ddof=1)", "numpy", "Độ lệch chuẩn của từng dòng, tức dao động trong mỗi năm.")],
     ket_qua="Hai cặp 100, 120 và 1.000, 1.200 cùng cách nhau 0,182 trên thang log. 1992 tới 2019: mức gấp 3,1 lần, dao động gấp 2,4 lần.",
     hinh=(5, "kn-log-exp"), nguon="rút gọn từ buoi-05/tu-hoc.ipynb, phần 3"),

dict(ma="code-b05-guerrero", buoi=5, sec="4.4", tieu="Code: chọn λ Box-Cox bằng Guerrero",
     muc="Chọn λ bằng số để dao động mỗi năm đều nhau, rồi so với cách chọn của scipy.",
     code='''import numpy as np
from scipy import stats

def guerrero(y, m):
    luoi = np.linspace(-1, 2, 3001)            # thử λ từ −1 tới 2
    y = np.asarray(y, dtype=float)
    khoi = y[y.size % m:].reshape(-1, m)       # mỗi dòng một năm
    tb, sd = khoi.mean(axis=1), khoi.std(axis=1, ddof=1)
    ty_so = sd[None, :] / tb[None, :] ** (1 - luoi[:, None])
    cv = ty_so.std(axis=1, ddof=1) / ty_so.mean(axis=1)
    return float(luoi[np.argmin(cv)])          # λ cho tỷ số đều nhất

lam_g = guerrero(y19, 12)                      # y19: bán lẻ 1992 tới 2019
lam_mle = stats.boxcox(y19.to_numpy())[1]      # tiêu chí khác
# tang: % tăng so với cùng tháng năm trước, có số âm
lam_yj = stats.yeojohnson(tang.to_numpy())[1]''',
     buoc=[("5", "Lưới 3.001 giá trị λ để thử."),
           ("7–8", "Mức và dao động của từng năm."),
           ("9–10", "Tỷ số mỗi năm và độ đều của chúng (CV)."),
           ("11", "Giữ λ cho CV nhỏ nhất."),
           ("14", "scipy chọn λ theo tiêu chí hình chuông."),
           ("15–16", "Chuỗi có số âm thì dùng Yeo-Johnson.")],
     ham=[("guerrero(y, m)", "tự viết", "Thử từng λ, chọn λ làm dao động các năm đều nhau nhất."),
          ("stats.boxcox", "scipy", "Biến đổi Box-Cox và tự chọn λ làm dữ liệu giống hình chuông nhất."),
          ("stats.yeojohnson", "scipy", "Giống Box-Cox nhưng nhận cả số 0 và số âm.")],
     ket_qua="λ Guerrero 0,34: dao động 2019 so 1992 còn 1,21 (log ép còn 0,84). scipy chọn 0,595; Yeo-Johnson trên % tăng ra khoảng 1,02.",
     hinh=(5, "kn-bien-doi-box-cox"), nguon="rút gọn từ buoi-05/tu-hoc.ipynb, phần 4"),

dict(ma="code-b05-doi-nguoc", buoi=5, sec="4.5", tieu="Code: đổi ngược ra trung vị",
     muc="Thấy bằng mô phỏng exp của dự báo log hụt trung bình, và hiệu chỉnh bias bù lại.",
     code='''import numpy as np

w = np.array([0.0, 1.0, 2.0])
print(np.exp(w.mean()), np.exp(w).mean())   # trung vị so với trung bình

x = np.random.default_rng(42).lognormal(5.0, 0.5, 100_000)
wx = np.log(x)                               # thang log
trung_vi = np.exp(wx.mean())                 # đổi ngược thẳng
tb_fpp = trung_vi * (1 + wx.var(ddof=1) / 2)  # hiệu chỉnh bias
print(trung_vi / x.mean() - 1, tb_fpp / x.mean() - 1)''',
     buoc=[("3–4", "Ba số log: exp của trung bình khác trung bình."),
           ("6", "100.000 mẫu log-normal, seed 42."),
           ("8", "Đổi ngược thẳng: ra trung vị."),
           ("9", "Nhân thêm 1 cộng nửa phương sai log."),
           ("10", "Mỗi cách hụt bao nhiêu so với trung bình thật.")],
     ham=[("np.exp", "numpy", "Hàm mũ, làm ngược lại log để về đơn vị gốc."),
          ("default_rng(42).lognormal", "numpy", "Sinh số ngẫu nhiên mà log của chúng có hình chuông."),
          ("var(ddof=1)", "numpy", "Phương sai mẫu: độ tản bình phương quanh trung bình.")],
     ket_qua="exp(trung bình log) = 2,72, trung bình thật 3,70. Mô phỏng: đổi ngược thẳng hụt 11,9%, có hiệu chỉnh gần khớp.",
     hinh=(5, "kn-doi-nguoc"), nguon="rút gọn từ buoi-05/tu-hoc.ipynb, phần 5"),

dict(ma="code-b05-backtest-log", buoi=5, sec="4.6", tieu="Code: seasonal naive có drift trên log",
     muc="Dự báo trên thang log chỉ bằng dữ liệu trước gốc, đổi ngược cả trung vị lẫn trung bình.",
     code='''import numpy as np
import pandas as pd

def du_bao_log(y, goc, so_buoc=12):
    hoc = y[(y.index < goc) & (y.index >= goc - pd.DateOffset(months=96))]
    w = np.log(hoc)                            # CHỈ dữ liệu trước gốc
    sp = (w - w.shift(12)).dropna()            # sai phân mùa vụ
    drift, s2 = sp.mean(), sp.var(ddof=1)
    tg = pd.date_range(goc, periods=so_buoc, freq="MS")
    w_hat = np.array([w[t - pd.DateOffset(years=1)] + drift for t in tg])
    return pd.DataFrame({"trung_vi": np.exp(w_hat),
                         "trung_binh": np.exp(w_hat) * (1 + s2 / 2)},
                        index=tg)

goc = pd.date_range("2012-01-01", "2018-12-01", freq="MS")  # 84 gốc
bang = pd.concat([du_bao_log(y, g) for g in goc])''',
     buoc=[("5–6", "Lấy 96 tháng ngay trước gốc, rồi lấy log."),
           ("7–8", "Drift và σ² từ sai phân mùa vụ của log."),
           ("10", "Cùng tháng năm trước cộng drift."),
           ("11–13", "Đổi ngược thẳng và đổi ngược có hiệu chỉnh."),
           ("15–16", "Chạy lại ở mỗi gốc từ 1/2012 tới 12/2018.")],
     ham=[("pd.DateOffset(months=96)", "pandas", "Lùi đúng 96 tháng theo lịch, không theo số ngày."),
          ("w - w.shift(12)", "pandas", "Sai phân mùa vụ: tháng này trừ cùng tháng năm trước."),
          ("pd.concat", "pandas", "Nối các bảng dự báo của từng gốc thành một bảng dài.")],
     ket_qua="1.008 dự báo. Hiệu chỉnh đẩy tổng dự báo lên đúng cỡ σ²/2, chỉ giúp khi dự báo đang thấp; bách hoá vốn đã lệch gần +10%.",
     hinh=(5, "kn-drift"), nguon="rút gọn từ buoi-05/tu-hoc.ipynb, phần 6"),

dict(ma="code-b06-co-dien", buoi=6, sec="4.1", tieu="Code: phân rã cổ điển bằng NumPy",
     muc="Tự viết phân rã cổ điển trong mười dòng và kiểm nó khớp statsmodels tới từng số.",
     code='''import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

def co_dien(x, m):
    x = np.asarray(x, dtype=float)
    w = np.r_[0.5, np.ones(m - 1), 0.5] / m       # 2×m-MA, tổng bằng 1
    T = np.full(x.size, np.nan)
    T[m // 2:-m // 2] = np.convolve(x, w, mode="valid")  # xu hướng
    pha = np.arange(x.size) % m                   # vị trí trong vòng
    S_mua = np.array([np.nanmean((x - T)[pha == k]) for k in range(m)])
    S = (S_mua - S_mua.mean())[pha]               # mùa vụ, tổng bằng 0
    return T, S, x - T - S                        # phần dư còn lại

x = np.array([22, 18, 15, 29, 30, 22, 19, 33, 30, 26, 23, 37])
T, S, R = co_dien(x, 4)
sm = seasonal_decompose(x, period=4)              # phải khớp T và S''',
     buoc=[("6", "m + 1 trọng số, hai đầu mỗi đầu một nửa."),
           ("7–8", "Trung bình trượt một vòng: ra xu hướng."),
           ("9–10", "Trung bình phần trừ xu hướng theo vị trí."),
           ("11", "Dời cho tổng mùa vụ một vòng bằng 0."),
           ("14–16", "Chạy trên 12 quý, so với thư viện.")],
     ham=[("np.convolve(x, w, mode=\"valid\")", "numpy", "Trượt bộ trọng số dọc chuỗi, chỉ giữ chỗ đủ hàng xóm."),
          ("co_dien(x, m)", "tự viết", "Trả về xu hướng, mùa vụ và phần dư theo cách cổ điển."),
          ("seasonal_decompose", "statsmodels", "Phân rã cổ điển có sẵn; kết quả có .trend, .seasonal, .resid.")],
     ket_qua="Quý 3 có xu hướng 22. Mùa vụ bốn quý 4, −3, −7, 6; phần dư chỉ ±0,5 và ±1,5; khớp seasonal_decompose.",
     hinh=(6, "kn-2-m-ma"), nguon="rút gọn từ buoi-06/tu-hoc.ipynb, phần 1"),

dict(ma="code-b06-bien-do", buoi=6, sec="4.2", tieu="Code: biên độ trong ngày theo tháng",
     muc="Đo biên độ mỗi ngày để biết mùa vụ đổi theo mùa, và bắt một giờ số liệu hỏng.",
     code='''import pandas as pd

# y: nhu cầu điện PJM theo giờ (MW), giờ New York
# y_goc: cùng chuỗi theo giờ UTC, chưa lấp giờ trống
ngay = y.resample("D")
bd = (ngay.max() - ngay.min()) / 1000        # biên độ trong ngày, GW
theo_thang = bd.groupby(bd.index.month).mean()
print(theo_thang.loc[[1, 4, 7]].round(1))

t0 = pd.Timestamp("2024-11-21 17:00")        # giờ nghi hỏng (UTC)
print(y_goc[t0 - pd.Timedelta("1h"):t0 + pd.Timedelta("1h")])''',
     buoc=[("5–6", "Cao nhất trừ thấp nhất trong mỗi ngày."),
           ("7–8", "Trung bình biên độ theo từng tháng."),
           ("10–11", "Xem giờ lạ cùng hai giờ hai bên.")],
     ham=[("resample(\"D\").max()", "pandas", "Gom các giờ thành từng ngày và lấy giá trị lớn nhất mỗi ngày."),
          ("groupby(index.month).mean()", "pandas", "Trung bình theo tháng, gộp mọi ngày cùng tháng."),
          ("pd.Timedelta(\"1h\")", "pandas", "Một khoảng thời gian một giờ để cộng trừ với mốc giờ.")],
     ket_qua="Biên độ trong ngày tháng 7 trung bình 44 GW, tháng 1 chỉ 17 GW. 17:00 UTC 21/11 báo 56.260 MW giữa hai giờ khoảng 95.000 MW.",
     hinh=(6, "kn-phan-ra-cong-nhan"), nguon="rút gọn từ buoi-06/tu-hoc.ipynb, phần 2"),

dict(ma="code-b06-mau-hinh", buoi=6, sec="4.3", tieu="Code: mùa vụ trốn trong xu hướng, phần dư",
     muc="Kiểm hai chỗ mùa vụ trốn: xu hướng theo thứ, và phần dư theo tháng và giờ.",
     code='''import pandas as pd
from statsmodels.tsa.seasonal import MSTL, seasonal_decompose

# y: nhu cầu PJM theo giờ, đã lấp giờ trống, giờ New York
sm24 = seasonal_decompose(y, period=24)
xh = sm24.trend.dropna()
print(xh.groupby(xh.index.dayofweek).mean())   # nhịp tuần ở xu hướng

def ty_le_mau_hinh(resid, y):
    r = resid.dropna()
    g = r.groupby([r.index.month, r.index.hour]).mean()  # tháng, giờ
    return g.var() / y.var()

ms = MSTL(y, periods=(24, 168)).fit()
print(ty_le_mau_hinh(sm24.resid, y), ty_le_mau_hinh(ms.resid, y))''',
     buoc=[("5", "Phân rã cổ điển chu kỳ 24 giờ."),
           ("6–7", "Xu hướng trung bình theo thứ: thấy nhịp tuần."),
           ("9–12", "Phần dư trung bình theo tháng và giờ."),
           ("12", "Chia phương sai chuỗi: gần 0 là phần dư sạch."),
           ("14–15", "So cổ điển với MSTL bằng cùng thước đo.")],
     ham=[("seasonal_decompose(y, period=24)", "statsmodels", "Phân rã cổ điển với một khuôn mùa vụ 24 giờ cho cả năm."),
          ("MSTL(y, periods=(24, 168))", "statsmodels", "Phân rã tách riêng mùa vụ ngày và mùa vụ tuần."),
          ("ty_le_mau_hinh", "tự viết", "Phần dư còn mẫu hình theo lịch tới đâu, đo bằng một con số.")],
     ket_qua="Xu hướng T7, CN thấp hơn giữa tuần khoảng 5.500–6.600 MW. Tỷ lệ mẫu hình tháng × giờ: cổ điển 0,102, MSTL 0,0006.",
     hinh=(6, "co-dien-24"), nguon="rút gọn từ buoi-06/tu-hoc.ipynb, phần 3"),

dict(ma="code-b06-stl-mstl", buoi=6, sec="4.4", tieu="Code: STL, MSTL và hai lỗi hay gặp",
     muc="Chạy STL và MSTL, xem hai lỗi hay gặp, rồi đo mùa vụ ngày đổi theo mùa thế nào.",
     code='''from statsmodels.tsa.seasonal import MSTL, STL

# y: nhu cầu PJM theo giờ, giờ New York; y_goc: bản còn NaN
bay = MSTL(y_goc, periods=(24, 168)).fit()
print(bay.trend.notna().sum())          # còn NaN là ra toàn NaN

stl = STL(y, period=24).fit()           # xu hướng 47 giờ, quá mềm
ms = MSTL(y, periods=(24, 168)).fit()   # mùa vụ ngày rồi mùa vụ tuần
print(stl.resid.var() / 1e6, ms.resid.var() / 1e6)   # GW bình phương

s24 = ms.seasonal["seasonal_24"]
ho = s24.groupby([s24.index.month, s24.index.hour]).mean().unstack()
bien_do = (ho.max(axis=1) - ho.min(axis=1)) / 1000   # GW theo tháng
print(ho.loc[1].idxmax(), ho.loc[7].idxmax())        # giờ đỉnh''',
     buoc=[("4–5", "Lỗi 1: còn giờ trống thì kết quả toàn NaN."),
           ("7", "Lỗi 2: STL mặc định cho phần dư nhỏ giả tạo."),
           ("8–9", "MSTL tách hai chu kỳ, so phương sai phần dư."),
           ("11–13", "Biên độ mùa vụ ngày của từng tháng."),
           ("14", "Giờ đỉnh mùa đông và mùa hè.")],
     ham=[("STL(y, period=24)", "statsmodels", "Phân rã bằng làm trơn cục bộ, mùa vụ được đổi dần qua các ngày."),
          ("MSTL(...).fit().seasonal", "statsmodels", "Bảng các mùa vụ, mỗi chu kỳ một cột: seasonal_24, seasonal_168."),
          ("unstack()", "pandas", "Xoay nhãn giờ thành cột: mỗi dòng một tháng, mỗi cột một giờ.")],
     ket_qua="Phần dư STL mặc định 2,8 GW², MSTL 16,5 GW². Biên độ mùa vụ ngày tháng 7 là 43,3 GW, tháng 1 là 14,4 GW.",
     hinh=(6, "kn-stl-loess"), nguon="rút gọn từ buoi-06/tu-hoc.ipynb, phần 4"),

dict(ma="code-b06-do-manh", buoi=6, sec="4.5", tieu="Code: độ mạnh xu hướng và mùa vụ",
     muc="Tính F_T và F_S từ phương sai, cho mọi thành phần mùa vụ của một phân rã.",
     code='''import pandas as pd
from statsmodels.tsa.seasonal import MSTL

def do_manh(bang):
    r = bang["resid"]
    kq = {"F_T": max(0.0, float(1 - r.var() / (bang["trend"] + r).var()))}
    for c in [c for c in bang.columns if c.startswith("seasonal")]:
        kq[c] = max(0.0, float(1 - r.var() / (bang[c] + r).var()))
    return kq

# y: nhu cầu PJM theo giờ, đã lấp giờ trống
kq = MSTL(y, periods=(24, 168)).fit()
ms = pd.DataFrame({"trend": kq.trend, "resid": kq.resid})
ms = ms.join(kq.seasonal)            # thêm seasonal_24, seasonal_168
print(do_manh(ms))                   # so với cùng hàm trên cổ điển''',
     buoc=[("6", "F_T: phần dư nhỏ tới đâu so với xu hướng."),
           ("7–8", "F_S cho từng cột mùa vụ, cùng một phần dư."),
           ("12–14", "Gom kết quả MSTL vào một bảng."),
           ("15", "Tính độ mạnh để so giữa các phân rã.")],
     ham=[("do_manh(bang)", "tự viết", "Trả về F_T và F_S, số từ 0 tới 1, càng gần 1 càng mạnh."),
          ("var()", "pandas", "Phương sai của một cột: nó dao động mạnh cỡ nào."),
          ("join", "pandas", "Ghép thêm cột từ bảng khác theo cùng mốc giờ.")],
     ket_qua="F_S của mùa vụ ngày: cổ điển 0,618, MSTL 0,829; mùa vụ tuần của MSTL 0,415. Cùng chuỗi, khác phân rã, khác số.",
     hinh=(6, "kn-do-manh-xu-huong-mua-vu"), nguon="rút gọn từ buoi-06/tu-hoc.ipynb, phần 5"),

dict(ma="code-b06-robust", buoi=6, sec="4.6", tieu="Code: MSTL robust với một giờ hỏng",
     muc="Tính trọng số robust tay, rồi thấy robust giữ lỗi một giờ trong phần dư.",
     code='''import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import MSTL

phan_du = np.array([1, -2, 1, 20, -1])
u = np.abs(phan_du) / (6 * np.median(np.abs(phan_du)))
trong_so = np.where(u < 1, (1 - u**2) ** 2, 0)   # điểm lạ ra 0

# y: nhu cầu PJM theo giờ; ms: kết quả MSTL không robust
rb = MSTL(y, periods=(24, 168), stl_kwargs={"robust": True}).fit()
t0 = pd.Timestamp("2024-11-21 17:00")            # giờ hỏng
hom_truoc = t0 - pd.Timedelta("1D")              # ngày không lỗi
print(ms.seasonal.loc[hom_truoc, "seasonal_24"],
      rb.seasonal.loc[hom_truoc, "seasonal_24"])
print(ms.resid[t0], rb.resid[t0])                # lỗi nằm ở đâu''',
     buoc=[("5–6", "Chia |phần dư| cho 6 lần trung vị của nó."),
           ("7", "Trọng số: gần 1 là tin, 0 là bỏ qua."),
           ("10", "Bật robust cho từng lượt STL bên trong."),
           ("13–14", "Mùa vụ ngày hôm trước có bị kéo lệch không."),
           ("15", "Phần dư ở giờ hỏng: robust giữ trọn cú rơi.")],
     ham=[("np.median", "numpy", "Trung vị: số đứng giữa, không bị điểm lạ kéo đi."),
          ("np.where(điều kiện, a, b)", "numpy", "Chỗ nào đúng điều kiện lấy a, còn lại lấy b."),
          ("stl_kwargs={\"robust\": True}", "statsmodels", "Bảo MSTL giảm trọng số điểm có phần dư quá lớn.")],
     ket_qua="Ví dụ tay: điểm 20 trọng số 0, điểm −2 là 0,79. Không robust, mùa vụ ngày 20/11 lệch khoảng 6.200 MW; robust giữ lỗi trong phần dư.",
     hinh=(6, "kn-robust"), nguon="rút gọn từ buoi-06/tu-hoc.ipynb, phần 6"),
dict(ma="code-b07-acf", buoi=7, sec="4.1", tieu="Code: ACF tự viết và ba hình dạng",
     muc="Tự tính ACF bằng vài dòng NumPy, khớp với thư viện, rồi nhìn ba hình dạng cần nhớ.",
     code='''import numpy as np
from statsmodels.tsa.stattools import acf

def acf_tu_viet(y, so_tre):
    y = np.asarray(y, dtype=float)
    lech = y - np.nanmean(y)                  # độ lệch khỏi trung bình
    mau = np.nansum(lech**2)                  # mẫu: tính trên CẢ chuỗi
    return np.array([1.0] + [np.nansum(lech[k:] * lech[:-k]) / mau
                             for k in range(1, so_tre + 1)])

y = [2, 3, 5, 6, 5, 3]
print(acf_tu_viet(y, 2)[1:])                  # tự viết
print(acf(y, nlags=2, adjusted=False)[1:])    # thư viện, phải ra y hệt
e = np.random.default_rng(42).normal(size=500)
ba = {"nhiễu trắng": e, "random walk": e.cumsum()}
r = {ten: acf_tu_viet(v, 30) for ten, v in ba.items()}''',
     buoc=[("6–7", "Lấy độ lệch, mẫu số chung cho mọi trễ."),
           ("8–9", "Mỗi trễ k: cộng tích hai độ lệch cách k bước."),
           ("11–13", "Ví dụ tay sáu số, so với statsmodels."),
           ("14–16", "Tính ACF cho nhiễu trắng và random walk.")],
     ham=[("acf_tu_viet", "tự viết", "Hệ số tự tương quan r_k cho các trễ 0 tới so_tre, trễ 0 luôn là 1."),
          ("acf(y, nlags, adjusted=False)", "statsmodels", "Cùng phép tính đó; adjusted=False để chia cho tổng của cả chuỗi."),
          ("cumsum()", "numpy", "Cộng dồn: biến dãy nhiễu thành đường đi của random walk.")],
     ket_qua="r1 = 0,333 và r2 = −0,417 như tính tay. Nhiễu trắng quanh 0; random walk giảm rất chậm; lượt thuê có đỉnh ở trễ 24, 48.",
     hinh=(4, "kn-acf"), nguon="rút gọn từ buoi-07/tu-hoc.ipynb, phần 1"),

dict(ma="code-b07-pacf", buoi=7, sec="4.2", tieu="Code: ACF và PACF của bốn chuỗi",
     muc="Thấy PACF tách được AR(1), còn ACF không phân biệt random walk với xu hướng.",
     code='''import numpy as np
from statsmodels.tsa.stattools import acf, pacf

e = np.random.default_rng(42).normal(size=500)   # một dãy nhiễu chung
ar = np.empty(500)
ar[0] = e[0]
for t in range(1, 500):
    ar[t] = 0.7 * ar[t - 1] + e[t]               # AR(1), phi = 0,7
bon = {"nhiễu trắng": e, "AR(1)": ar, "random walk": e.cumsum(),
       "xu hướng 0,05t": 0.05 * np.arange(500) + e}
DAI = 1.96 / np.sqrt(500)                        # dải ±1,96/√T
bang = {}
for ten, y in bon.items():
    r = acf(y, nlags=30, adjusted=False)
    p = pacf(y, nlags=30, method="ywm")          # khai method rõ ràng
    bang[ten] = {"r1": r[1], "r30": r[30], "PACF1": p[1], "PACF2": p[2]}''',
     buoc=[("4–8", "Dựng AR(1): hôm nay bằng 0,7 lần hôm qua."),
           ("9–10", "Bốn chuỗi dùng chung một dãy nhiễu."),
           ("11", "Dải để xem cột nào đáng chú ý."),
           ("14–16", "Tính ACF, PACF và giữ vài con số."),
           ("15", "Khai method vì mặc định hai hàm khác nhau.")],
     ham=[("pacf(y, nlags, method=\"ywm\")", "statsmodels", "Tương quan riêng phần: phần còn lại sau khi bỏ các trễ ngắn hơn."),
          ("acf(y, nlags)", "statsmodels", "Hệ số tự tương quan r_k cho từng trễ k."),
          ("np.empty(n)", "numpy", "Tạo mảng n chỗ trống để điền dần từng bước.")],
     ket_qua="AR(1): ACF giảm nhanh, PACF cắt sau trễ 1. Random walk và xu hướng đều có r1 gần 0,98: chỉ nhìn ACF không phân biệt được.",
     hinh=(7, "kn-pacf"), nguon="rút gọn từ buoi-07/tu-hoc.ipynb, phần 2"),

dict(ma="code-b07-ljung-box", buoi=7, sec="4.3", tieu="Code: gộp nhiều r_k bằng Ljung-Box",
     muc="Thay việc đếm cột vượt dải bằng một con số Q* và một p-value.",
     code='''import numpy as np
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

T, r = 100, np.array([0.2, 0.1])                 # ví dụ tay: 100 điểm
Q = T * (T + 2) * np.sum(r**2 / (T - np.arange(1, 3)))
nguong = stats.chi2.ppf(0.95, 2)                 # ngưỡng 5%, 2 bậc tự do
p = stats.chi2.sf(Q, 2)

for s in (1, 2, 3):
    nhieu = np.random.default_rng(s).normal(size=500)
    kq0 = acorr_ljungbox(nhieu, lags=[10])
    # nếu là sai số của mô hình 2 tham số: trừ bậc tự do
    kq2 = acorr_ljungbox(nhieu, lags=[10], model_df=2)
    print(kq0["lb_pvalue"].iloc[0], kq2["lb_pvalue"].iloc[0])''',
     buoc=[("5–6", "Tính Q* bằng tay theo công thức."),
           ("7–8", "Tra ngưỡng và p từ phân phối khi bình phương."),
           ("10–12", "Kiểm 10 trễ trên ba chuỗi nhiễu trắng."),
           ("14", "model_df=2 khi kiểm sai số của mô hình.")],
     ham=[("acorr_ljungbox(y, lags, model_df)", "statsmodels", "Kiểm định Ljung-Box, trả bảng có cột lb_stat và lb_pvalue."),
          ("stats.chi2.ppf(0.95, df)", "scipy", "Ngưỡng mà chỉ 5% giá trị của phân phối vượt qua."),
          ("stats.chi2.sf(Q, df)", "scipy", "p-value: xác suất gặp Q lớn cỡ này nếu là nhiễu trắng.")],
     ket_qua="Ví dụ tay Q* = 5,16 < 5,99: không bác bỏ. Ba chuỗi nhiễu cho p từ 0,081 tới 0,885; model_df=2 làm p nhỏ đi.",
     hinh=(7, "kn-ljung-box"), nguon="rút gọn từ buoi-07/tu-hoc.ipynb, phần 3"),

dict(ma="code-b07-random-walk", buoi=7, sec="4.4", tieu="Code: hai loại không dừng, hai thuốc",
     muc="Thấy random walk dao động to dần, và mỗi loại không dừng cần một cách chữa riêng.",
     code='''import numpy as np
from statsmodels.tsa.stattools import acf

# 10.000 người tung đồng xu, mỗi người 100 bước
buoc = np.random.default_rng(7).choice([-1, 1], size=(10_000, 100))
vi_tri = buoc.cumsum(axis=1)
do_lech = vi_tri[:, [3, 24, 99]].std(axis=0)     # sau 4, 25, 100 bước

e = np.random.default_rng(42).normal(size=500)
t = np.arange(500)
for y in (e.cumsum(), 0.05 * t + e):             # random walk, xu hướng
    khu_xh = y - np.polyval(np.polyfit(t, y, 1), t)   # trừ đường thẳng
    sai_phan = np.diff(y)                             # y_t trừ y_(t-1)
    print(acf(khu_xh, nlags=1)[1], acf(sai_phan, nlags=1)[1])''',
     buoc=[("4–6", "Mô phỏng 10.000 người bước ngẫu nhiên."),
           ("7", "Đo độ dao động ở ba thời điểm."),
           ("11", "Thuốc một: khử xu hướng bằng đường thẳng."),
           ("12", "Thuốc hai: sai phân."),
           ("13", "r1 phần còn lại cho biết thuốc có hợp không.")],
     ham=[("np.polyfit(t, y, 1)", "numpy", "Tìm đường thẳng khớp dữ liệu nhất, trả độ dốc và hệ số chặn."),
          ("np.polyval(he_so, t)", "numpy", "Tính giá trị của đường thẳng đó tại từng thời điểm t."),
          ("np.diff(y)", "numpy", "Sai phân: hiệu của mỗi giá trị với giá trị ngay trước.")],
     ket_qua="Số bước gấp 25 lần thì độ lệch chuẩn gấp 5 lần (2,0 lên 10,1). Khử xu hướng random walk: r1 vẫn rất lớn; sai phân chuỗi xu hướng: r1 âm rõ.",
     hinh=(7, "kn-random-walk"), nguon="rút gọn từ buoi-07/tu-hoc.ipynb, phần 4"),

dict(ma="code-b07-adf-kpss", buoi=7, sec="4.5", tieu="Code: ADF + KPSS và bảng 2 × 2",
     muc="Chạy hai kiểm định có giả thuyết ngược nhau, cùng dạng, rồi đọc kết luận từ bảng.",
     code='''import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss

def kiem_dinh(y, dang="c"):      # "c": quanh một mức, "ct": quanh đường
    y = np.asarray(y, dtype=float)
    p_adf = adfuller(y, regression=dang, autolag="AIC",
                     result_object=True).pvalue
    p_kpss = kpss(y, regression=dang, nlags="auto",
                  result_object=True).pvalue
    return p_adf, p_kpss
def o_bang(p_adf, p_kpss):       # ADF bác bỏ? KPSS bác bỏ?
    ten = {(True, False): "dừng", (False, True): "không dừng",
           (True, True): "mâu thuẫn", (False, False): "không đủ bằng chứng"}
    return ten[(p_adf < 0.05, p_kpss < 0.05)]
y = 0.05 * np.arange(500) + np.random.default_rng(42).normal(size=500)
kq = {d: o_bang(*kiem_dinh(y, d)) for d in ("c", "ct")}   # hai dạng''',
     buoc=[("4", "Dạng kiểm định phải khai rõ, cả hai dùng chung."),
           ("6–7", "ADF: p nhỏ là có bằng chứng dừng."),
           ("8–9", "KPSS: p nhỏ là có bằng chứng không dừng."),
           ("11–14", "Ghép hai kết quả thành một ô của bảng 2 × 2."),
           ("15–16", "Thử chuỗi xu hướng với dạng c và ct.")],
     ham=[("adfuller(y, regression, autolag)", "statsmodels", "Kiểm định ADF; giả thuyết gốc là có nghiệm đơn vị (không dừng)."),
          ("kpss(y, regression, nlags)", "statsmodels", "Kiểm định KPSS; giả thuyết gốc là dừng, p bị cắt ở 0,01 và 0,1."),
          ("o_bang", "tự viết", "Đổi cặp p-value thành một trong bốn kết luận.")],
     ket_qua="Xu hướng 0,05t: dạng c nói không dừng, chỉ dạng ct cho thấy chuỗi dừng quanh xu hướng. Random walk có ADF p = 0,073; KPSS bắt được.",
     hinh=(7, "kn-adf-kpss"), nguon="rút gọn từ buoi-07/tu-hoc.ipynb, phần 5"),

dict(ma="code-b07-sai-phan", buoi=7, sec="4.6", tieu="Code: hai dấu hiệu sai phân thừa",
     muc="Biết khi nào dừng sai phân: r1 gần −0,5 hoặc độ lệch chuẩn tăng lên.",
     code='''import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

def dau_hieu(y):
    y = pd.Series(np.asarray(y, dtype=float)).dropna()
    sp = y.diff().dropna()                       # sai phân một lần
    return acf(sp, nlags=1)[1], y.std(ddof=1), sp.std(ddof=1)

e = np.random.default_rng(42).normal(size=500)
print(dau_hieu(e))              # đã dừng: sai phân là thừa
print(dau_hieu(e.cumsum()))     # random walk: sai phân đúng liều

g = np.log1p(luot.interpolate(limit=3))          # lượt thuê theo giờ
for s in (g.diff(), g.diff(168), g.diff(168).diff()):
    print(acf(s.dropna(), nlags=168)[[1, 24, 168]], s.std(ddof=1))''',
     buoc=[("5–8", "Trả r1 sau sai phân và độ lệch chuẩn trước, sau."),
           ("11", "Sai phân chuỗi đã dừng để thấy dấu hiệu thừa."),
           ("12", "Sai phân random walk để thấy đúng liều."),
           ("14", "log(1 + y) vì có giờ không ai thuê xe."),
           ("15–16", "So sai phân thường, mùa vụ 168 và cả hai.")],
     ham=[("diff(k)", "pandas", "Trừ mỗi giá trị cho giá trị cách k bước; k = 168: cùng giờ tuần trước."),
          ("np.log1p(y)", "numpy", "Tính log(1 + y), dùng được cả khi y bằng 0."),
          ("std(ddof=1)", "pandas", "Độ lệch chuẩn mẫu: đo chuỗi dao động mạnh cỡ nào.")],
     ket_qua="Nhiễu trắng: r1 = −0,447, độ lệch chuẩn 0,96 lên 1,29 (thừa). Random walk: 4,55 xuống 0,96. Lượt thuê: 168 rồi thường giảm 0,589 xuống 0,427.",
     hinh=(7, "sai-phan-thua"), nguon="rút gọn từ buoi-07/tu-hoc.ipynb, phần 6"),

dict(ma="code-b08-anscombe", buoi=8, sec="4.1", tieu="Code: Pearson, Spearman và Anscombe",
     muc="Thấy một hệ số tương quan giấu được cả hình dạng, nên luôn phải vẽ trước.",
     code='''import numpy as np
from scipy import stats

for x in (np.arange(1, 6), np.arange(-2, 3)):     # y = x² trên hai khoảng
    print(stats.pearsonr(x, x**2)[0], stats.spearmanr(x, x**2)[0])

X0 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ANSCOMBE = {
    "I": (X0, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84,
               4.82, 5.68]),
    "IV": ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
           [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91,
            6.89]),
}                                                 # bộ II, III tương tự
for ten, (x, y) in ANSCOMBE.items():
    print(ten, stats.pearsonr(x, y)[0], stats.spearmanr(x, y)[0])''',
     buoc=[("4–5", "Chữ U: Pearson ra 0 dù y phụ thuộc hẳn vào x."),
           ("7–14", "Hai trong bốn bộ Anscombe, rất khác hình."),
           ("15–16", "Tính hai hệ số cho từng bộ để so.")],
     ham=[("stats.pearsonr(x, y)", "scipy", "Tương quan Pearson: đo quan hệ theo đường thẳng, kèm p-value."),
          ("stats.spearmanr(x, y)", "scipy", "Tương quan trên thứ hạng: đo quan hệ cùng tăng, dù cong.")],
     ket_qua="Với x từ −2 tới 2, y = x²: Pearson 0. Bốn bộ Anscombe cùng Pearson 0,82 nhưng Spearman từ 0,5 tới 0,99: bốn câu chuyện khác nhau.",
     hinh=(8, "kn-spearman"), nguon="rút gọn từ buoi-08/tu-hoc.ipynb, phần 1"),

dict(ma="code-b08-tuong-quan-gia", buoi=8, sec="4.2", tieu="Code: hồi quy giả và Durbin–Watson",
     muc="Bắt tương quan giả bằng hai phép kiểm: DW của phần dư và tương quan sau sai phân.",
     code='''import numpy as np

def durbin_watson(e):                            # gần 2 tốt, gần 0 xấu
    return np.sum(np.diff(e) ** 2) / np.sum(e**2)

def hoi_quy_don(x, y):
    X = np.column_stack([np.ones(x.size), x])
    he_so = np.linalg.lstsq(X, y, rcond=None)[0]  # bình phương nhỏ nhất
    du = y - X @ he_so                            # phần dư
    se = np.sqrt(du @ du / (x.size - 2) * np.linalg.inv(X.T @ X)[1, 1])
    return 1 - du.var() / y.var(), he_so[1] / se, durbin_watson(du)

# kt: CPI và dân số Mỹ theo tháng, 1990–2024
r2, t, dw = hoi_quy_don(kt["cpi"].to_numpy(), kt["dan_so"].to_numpy())
d = kt.diff().dropna()                            # thay đổi hằng tháng
r_sai_phan = d["cpi"].corr(d["dan_so"])''',
     buoc=[("3–4", "DW đo phần dư có đổi chậm theo thời gian không."),
           ("6–8", "Khớp đường thẳng, lấy phần dư."),
           ("9–10", "Trả R², t của hệ số và DW."),
           ("13", "Hồi quy dân số theo CPI trên mức."),
           ("14–15", "Hỏi lại câu đúng: các thay đổi có đi cùng?")],
     ham=[("np.linalg.lstsq(X, y)", "numpy", "Tìm hệ số đường thẳng làm tổng bình phương sai lệch nhỏ nhất."),
          ("durbin_watson", "tự viết", "Tổng bình phương bước nhảy của phần dư chia tổng bình phương phần dư."),
          ("diff().corr()", "pandas", "Lấy thay đổi hằng tháng rồi tính tương quan của hai cột.")],
     ket_qua="Trên mức: r 0,974, R² 0,95, t 88,6. Nhưng DW 0,0051 và r sau sai phân −0,207: tương quan giả.",
     hinh=(8, "kn-durbin-watson"), nguon="rút gọn từ buoi-08/tu-hoc.ipynb, phần 2"),

dict(ma="code-b08-cdd-mi", buoi=8, sec="4.3", tieu="Code: CDD, HDD và MI xáo theo khối",
     muc="Tách quan hệ chữ U thành hai nhánh, và kiểm MI có thật bằng cách xáo cả tuần.",
     code='''import numpy as np
from sklearn.feature_selection import mutual_info_regression
t, y = df["nhiet"].to_numpy(), df["tai"].to_numpy() / 1000   # °C, GW
cdd, hdd = np.maximum(t - 18.33, 0), np.maximum(18.33 - t, 0)  # mốc 65 °F
def r2_hoi_quy(*cot):
    X = np.column_stack([np.ones(y.size), *cot])
    du = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
    return 1 - du.var() / y.var()
r2_thang, r2_hai_nhanh = r2_hoi_quy(t), r2_hoi_quy(cdd, hdd)
def mi(x, v):
    return mutual_info_regression(x.reshape(-1, 1), v, random_state=0)[0]
rng = np.random.default_rng(0)
khoi = [y[i:i + 168] for i in range(0, y.size, 168)]      # khối 1 tuần
xao = [np.concatenate([khoi[i] for i in rng.permutation(len(khoi))])
       for _ in range(100)]
nguong = np.quantile([mi(t, v) for v in xao], 0.95)      # so với mi(t, y)''',
     buoc=[("4", "Độ nóng và độ lạnh so với mốc 18,33 °C."),
           ("5–9", "R² theo nhiệt độ so với theo CDD + HDD."),
           ("10–11", "MI bắt được cả quan hệ cong."),
           ("13–15", "Xáo thứ tự các tuần, giữ nhịp trong tuần."),
           ("16", "Ngưỡng 95% của MI khi không có quan hệ.")],
     ham=[("np.maximum(a, 0)", "numpy", "Giữ phần dương, còn lại thành 0: đúng cách tính CDD, HDD."),
          ("mutual_info_regression", "sklearn", "Ước lượng thông tin tương hỗ: biết x bớt được bao nhiêu điều về y."),
          ("rng.permutation(n)", "numpy", "Xáo ngẫu nhiên thứ tự 0 tới n − 1, ở đây là thứ tự các khối.")],
     ket_qua="R² tăng từ 0,379 lên 0,812. Nhánh lạnh r = −0,649, nhánh nóng +0,910. MI thật 0,862 vượt xa ngưỡng xáo khối 0,124.",
     hinh=(8, "kn-cdd-hdd"), nguon="rút gọn từ buoi-08/tu-hoc.ipynb, phần 3"),

dict(ma="code-b08-prewhiten", buoi=8, sec="4.4", tieu="Code: tương quan chéo sau prewhitening",
     muc="Lọc bỏ độ trơn của x trước, rồi mới đọc độ trễ mà x báo trước y.",
     code='''import numpy as np
from statsmodels.tsa.ar_model import AutoReg

def ccf_tu_viet(x, y, so_tre):                    # corr(x_t, y_(t+k))
    x, y = (x - x.mean()) / x.std(), (y - y.mean()) / y.std()
    return np.array([np.sum(x[:x.size - k] * y[k:]) / x.size
                     for k in range(so_tre + 1)])
def loc_prewhiten(x, y, bac=48):
    phi = AutoReg(x, lags=bac).fit().params[1:]   # hệ số AR(48) của x
    def loc(v):
        return np.array([v[i] - phi[::-1] @ v[i - bac:i]
                         for i in range(bac, v.size)])
    return loc(x), loc(y)                         # lọc CẢ HAI, cùng phi
cdd, taiv = df["cdd"].to_numpy(), df["tai"].to_numpy()
tho = ccf_tu_viet(cdd, taiv, 48)                  # thô: nhoè
sach = ccf_tu_viet(*loc_prewhiten(cdd, taiv), 48) # sau lọc: sắc''',
     buoc=[("4–6", "Chuẩn hoá rồi nhân x lúc t với y lúc t + k."),
           ("8", "Khớp AR(48) cho x để biết phần tự đoán được."),
           ("9–12", "Lọc cả x lẫn y bằng đúng bộ hệ số đó."),
           ("14–15", "So tương quan chéo thô và sau lọc.")],
     ham=[("AutoReg(x, lags).fit()", "statsmodels", "Khớp mô hình tự hồi quy: đoán x từ các giá trị trước của nó."),
          ("ccf_tu_viet", "tự viết", "Tương quan chéo corr(x_t, y_(t+k)); k dương là x đi trước y."),
          ("loc_prewhiten", "tự viết", "Bỏ phần x tự đoán được, lọc y y hệt, trả hai chuỗi đã lọc.")],
     ket_qua="Thô: trễ 24 (0,828) cao gần bằng trễ 0, là nhịp ngày của CDD. Sau lọc chỉ còn đỉnh ở trễ 0 (0,205), tắt sau vài giờ.",
     hinh=(8, "ccf"), nguon="rút gọn từ buoi-08/tu-hoc.ipynb, phần 4"),

dict(ma="code-b08-tuong-quan-truot", buoi=8, sec="4.5", tieu="Code: tương quan trượt 30 và 90 ngày",
     muc="Thấy quan hệ nhiệt độ và tải đổi dấu theo mùa, thay vì tin một con số cả năm.",
     code='''import numpy as np
import pandas as pd

# ví dụ tay: 3 ngày đông r = −1, 3 ngày hè r = +1; gộp lại thì sao?
r_gop = np.corrcoef([5, 10, 15, 25, 30, 35], [30, 20, 10, 20, 30, 40])

ngay = df.resample("D").mean()                    # giờ gộp thành ngày
r90 = ngay["nhiet"].rolling(90, min_periods=90).corr(ngay["tai"])
r30 = ngay["nhiet"].rolling(30, min_periods=30).corr(ngay["tai"])
r_ca_nam = df["nhiet"].corr(df["tai"])            # một số cho cả năm
print(r90["2024-03-31"], r90["2024-10-14"], r30.min())''',
     buoc=[("5", "Hai chế độ ngược dấu gộp lại ra số lưng chừng."),
           ("7", "Đổi dữ liệu giờ thành trung bình ngày."),
           ("8–9", "r trên cửa sổ trượt, đủ điểm mới tính."),
           ("10", "Con số cả năm để so.")],
     ham=[("resample(\"D\").mean()", "pandas", "Gom dữ liệu theo từng ngày, lấy trung bình mỗi ngày."),
          ("rolling(w, min_periods=w).corr(b)", "pandas", "Tương quan trên từng cửa sổ w ngày; thiếu điểm thì để trống."),
          ("np.corrcoef(a, b)", "numpy", "Ma trận tương quan Pearson của hai dãy số.")],
     ket_qua="Gộp sáu ngày ra r = 0,48. Cửa sổ 90 ngày: −0,801 (31/3), +0,968 (14/10); 30 ngày xuống tới −0,971. Cả năm 0,616.",
     hinh=(8, "truot"), nguon="rút gọn từ buoi-08/tu-hoc.ipynb, phần 5"),

dict(ma="code-b08-granger", buoi=8, sec="4.6", tieu="Code: Granger chạy cả hai chiều",
     muc="Chạy Granger hai chiều để thấy dấu hiệu của biến gây nhiễu, thay vì đọc thành nhân quả.",
     code='''import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

def granger_p(nguyen_nhan, ket_qua, so_tre=4):
    # statsmodels hỏi: CỘT 2 có giúp dự báo CỘT 1 không
    kq = grangercausalitytests(np.column_stack([ket_qua, nguyen_nhan]),
                               maxlag=so_tre)
    return min(kq[k][0]["ssr_ftest"][1] for k in kq)   # p nhỏ nhất

cdd, taiv = df["cdd"].to_numpy(), df["tai"].to_numpy()
p_xuoi = granger_p(cdd, taiv)                     # CDD giúp dự báo tải?
p_nguoc = granger_p(taiv, cdd)                    # tải giúp dự báo CDD?

ho = df[["tai", "nhiet"]].groupby(df.index.hour).mean()   # theo giờ
ho = (ho - ho.mean()) / ho.std()                  # cùng một nhịp 24 giờ''',
     buoc=[("5–6", "Xếp cột đúng thứ tự thư viện đòi."),
           ("7", "Lấy p nhỏ nhất qua các độ trễ 1 tới 4."),
           ("10–11", "Hỏi cả hai chiều, không chỉ chiều mong muốn."),
           ("13–14", "Tìm biến thứ ba: nhịp giờ trong ngày.")],
     ham=[("grangercausalitytests(data, maxlag)", "statsmodels", "Kiểm quá khứ cột 2 có giúp dự báo cột 1 không, ở mỗi độ trễ."),
          ("groupby(df.index.hour).mean()", "pandas", "Trung bình theo giờ trong ngày: ra hình dạng một ngày điển hình."),
          ("np.column_stack", "numpy", "Ghép các dãy thành các cột của một bảng.")],
     ket_qua="Cả hai chiều p gần 0, kể cả \"tải giúp dự báo nhiệt độ\": vô lý, vì cả hai cùng chạy theo nhịp ngày.",
     hinh=(8, "kn-bien-gay-nhieu"), nguon="rút gọn từ buoi-08/tu-hoc.ipynb, phần 6"),

dict(ma="code-b09-dac-trung", buoi=9, sec="4.1", tieu="Code: mỗi chuỗi thành một hàng số",
     muc="Tóm mỗi chuỗi thành các đặc trưng không đổi theo đơn vị, để so hàng nghìn chuỗi.",
     code='''import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL

def dac_trung(y, m=12):                           # 6 trong 20 đặc trưng
    z = (y - y.mean()) / np.std(y)                # STL trên chuỗi z-score
    idx = pd.period_range("2000-01", periods=y.size, freq="M").to_timestamp()
    kq = STL(pd.Series(z, index=idx), period=m).fit()
    r, s = kq.resid.to_numpy(), kq.seasonal.to_numpy()
    return {"trung_binh": y.mean(),
            "he_so_bien_thien": np.std(y, ddof=1) / y.mean(),
            "he_so_lech": stats.skew(y), "do_nhon": stats.kurtosis(y),
            "do_manh_mua_vu": max(0.0, 1 - np.var(r) / np.var(s + r)),
            "ty_le_0": np.mean(y == 0)}
bang = pd.DataFrame({t: dac_trung(v[:-18]) for t, v in chuoi.items()}).T''',
     buoc=[("7", "z-score để độ mạnh không tính bằng USD."),
           ("8–10", "Tách xu hướng, mùa vụ, phần dư bằng STL."),
           ("11–15", "Mỗi đặc trưng một con số của cả chuỗi."),
           ("16", "Chỉ tính trên phần học, bỏ 18 tháng chấm.")],
     ham=[("STL(series, period).fit()", "statsmodels", "Tách chuỗi thành xu hướng + mùa vụ + phần dư."),
          ("stats.skew, stats.kurtosis", "scipy", "Hệ số lệch và độ nhọn: đo đuôi và giá trị cực đoan."),
          ("pd.DataFrame(dict).T", "pandas", "Ghép từ điển các chuỗi thành bảng, mỗi chuỗi một hàng.")],
     ket_qua="Nhân chuỗi với 1.000: chỉ trung_binh và do_lech_chuan đổi, 18 đặc trưng giữ nguyên. Bảng còn cho thấy 1 chuỗi hằng và 50 chuỗi bậc thang.",
     hinh=(9, "kn-he-so-lech-skewness"), nguon="rút gọn từ buoi-09/tu-hoc.ipynb, phần 1"),

dict(ma="code-b09-entropy", buoi=9, sec="4.2", tieu="Code: spectral entropy từ phổ Welch",
     muc="Một con số từ 0 tới 1 nói chuỗi có nhịp rõ hay giống nhiễu, không cần mô hình.",
     code='''import numpy as np
from scipy import signal

def entropy_pho(y):
    _, P = signal.welch(y - y.mean(), fs=1.0, nperseg=min(256, y.size))
    P = P[1:]                                     # bỏ tần số 0 (mức TB)
    p = P / P.sum()                               # phần năng lượng, tổng 1
    return float(-np.sum(p * np.log(p + 1e-300)) / np.log(p.size))

rng = np.random.default_rng(0)
t = np.arange(120)
mua_vu = np.sin(2 * np.pi * t / 12) + 0.2 * rng.normal(size=120)
nhieu = rng.normal(size=120)
print(entropy_pho(mua_vu), entropy_pho(nhieu))
e = bang["entropy_pho"]                           # 4.000 chuỗi M4
print(e.median(), e.quantile(0.8))''',
     buoc=[("5", "Phổ: mỗi tần số góp bao nhiêu năng lượng."),
           ("7", "Chia thành các phần cộng lại bằng 1."),
           ("8", "Entropy chia ln N để luôn nằm trong 0 tới 1."),
           ("11–13", "So chuỗi mùa vụ 12 tháng với nhiễu thuần."),
           ("14–15", "Xem phân bố entropy trên 4.000 chuỗi.")],
     ham=[("signal.welch(y, fs, nperseg)", "scipy", "Ước lượng phổ bằng trung bình phổ của nhiều đoạn chồng nhau."),
          ("entropy_pho", "tự viết", "Năng lượng trải đều tới đâu: 0 là một nhịp, 1 là nhiễu."),
          ("quantile(0.8)", "pandas", "Giá trị mà 80% số chuỗi nằm dưới.")],
     ket_qua="Chuỗi mùa vụ entropy 0,33, nhiễu thuần 0,94. Trên M4 trung vị 0,462; một phần năm số chuỗi từ 0,666 trở lên.",
     hinh=(9, "entropy-hai-chuoi"), nguon="rút gọn từ buoi-09/tu-hoc.ipynb, phần 2"),

dict(ma="code-b09-smape-mase", buoi=9, sec="4.3", tieu="Code: đo độ khó bằng sMAPE và MASE",
     muc="Thấy chỉ đổi mẫu số của thước đo là kết luận về entropy đổi hẳn.",
     code='''import numpy as np
import pandas as pd
from scipy import stats

def smape(y, f):                                  # chia cho MỨC
    mau = np.abs(y) + np.abs(f)
    return np.mean(np.where(mau == 0, 0.0, 200 * np.abs(y - f) / mau))
def mase(y, f, hoc, m=12):                        # chia cho sai số snaive
    thang = np.mean(np.abs(hoc[m:] - hoc[:-m]))   # MAE snaive phần học
    return np.mean(np.abs(y - f)) / thang
kho = {}
for ten, v in chuoi.items():
    hoc, kiem = v[:-18], v[-18:]                  # 18 tháng cuối để chấm
    f = np.resize(hoc[-12:], 18)                  # seasonal naive
    kho[ten] = {"smape": smape(kiem, f), "mase": mase(kiem, f, hoc)}
r = stats.pearsonr(bang["entropy_pho"], pd.DataFrame(kho).T["smape"])[0]''',
     buoc=[("5–7", "sMAPE chia sai số cho mức của chuỗi."),
           ("8–10", "MASE chia cho sai số seasonal naive lúc học."),
           ("13–14", "Dự báo 18 tháng bằng lặp lại năm cuối."),
           ("16", "Tương quan entropy với độ khó thật.")],
     ham=[("np.resize(a, n)", "numpy", "Lặp lại mảng a cho đủ n phần tử: 12 tháng cuối thành 18 tháng."),
          ("np.where(dk, a, b)", "numpy", "Chọn a nơi điều kiện đúng, b nơi sai; tránh chia cho 0."),
          ("stats.pearsonr(x, y)", "scipy", "Hệ số tương quan Pearson của hai cột.")],
     ket_qua="Ví dụ tay: MASE nói B dễ hơn A (0,92 so với 1,00), sMAPE nói B khó hơn (76,2% so với 6,7%). Với entropy: sMAPE +0,245, MASE −0,048.",
     hinh=(9, "ba-thuoc-do"), nguon="rút gọn từ buoi-09/tu-hoc.ipynb, phần 3"),

dict(ma="code-b09-pca", buoi=9, sec="4.4", tieu="Code: bản đồ PCA và nhóm dùng baseline",
     muc="Nén 15 đặc trưng về hai trục để thấy cả tập, rồi tách chuỗi chỉ cần baseline.",
     code='''import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

cot = [c for c in bang.columns if bang[c].notna().all()
       and c not in ("trung_binh", "do_lech_chuan")    # bỏ cột quy mô
       and not c.startswith(("smape", "mase"))]        # bỏ cột sai số
X = StandardScaler().fit_transform(bang[cot])     # chuẩn hoá từng cột
pca = PCA(n_components=2, random_state=0)
toa_do = pca.fit_transform(X)                     # mỗi chuỗi một chấm
print(pca.explained_variance_ratio_)              # phần khác biệt giữ lại

kho = (bang["entropy_pho"] >= 0.666) & (bang["do_manh_mua_vu"] < 0.4)
nhom = np.where(kho, "dùng baseline", "đáng đầu tư mô hình")
print(bang.groupby(nhom)["smape_snaive"].agg(["size", "median"]))''',
     buoc=[("5–7", "Chỉ giữ đặc trưng đủ số, không lẫn sai số."),
           ("8", "Chuẩn hoá để cột số to không lấn át."),
           ("9–11", "Nén về hai trục PC1, PC2."),
           ("13–14", "Entropy cao và mùa vụ yếu: dùng baseline."),
           ("15", "Kiểm lại bằng sMAPE thật của từng nhóm.")],
     ham=[("StandardScaler().fit_transform", "sklearn", "Trừ trung bình, chia độ lệch chuẩn cho từng cột."),
          ("PCA(n_components=2)", "sklearn", "Tìm hai hướng mà các chuỗi khác nhau nhiều nhất."),
          ("explained_variance_ratio_", "sklearn", "Mỗi trục giữ được bao nhiêu phần trăm khác biệt.")],
     ket_qua="PC1 giữ 41%, PC2 15%. 137 chuỗi dùng baseline có sMAPE trung vị 18,11%, gấp ba nhóm 3.863 chuỗi còn lại (6,05%).",
     hinh=(9, "kn-pca-pc1-pc2"), nguon="rút gọn từ buoi-09/tu-hoc.ipynb, phần 4"),

dict(ma="code-b09-dtw", buoi=9, sec="4.5", tieu="Code: phân cụm DTW sau z-score",
     muc="Gom chuỗi theo hình dạng, và thấy vì sao phải chuẩn hoá từng chuỗi trước DTW.",
     code='''import numpy as np
import pandas as pd
from dtaidistance import dtw
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform

def z(v):                                         # bỏ mức, giữ hình dạng
    return (v - v.mean()) / v.std()
def phan_cum(mau, chuan_hoa, so_cum=4, cua_so=10):
    day = [z(v) if chuan_hoa else v for v in mau.values()]
    D = dtw.distance_matrix_fast(day, window=cua_so)   # lệch tối đa 10
    D = np.where(np.isinf(D), 0, D)
    D = D + D.T                                   # lấp đủ hai nửa ma trận
    Z = linkage(squareform(D, checks=False), method="ward")
    nhan = fcluster(Z, so_cum, criterion="maxclust")
    return pd.Series(nhan, index=list(mau))''',
     buoc=[("7–8", "z-score: bỏ độ lớn, chỉ giữ hình dạng."),
           ("10", "Chọn có chuẩn hoá hay không để so."),
           ("11", "Khoảng cách DTW giữa mọi cặp chuỗi."),
           ("12–13", "Sửa ma trận cho đủ và đối xứng."),
           ("14–16", "Gộp dần theo Ward, cắt ra 4 cụm.")],
     ham=[("linkage(d, method=\"ward\")", "scipy", "Gộp dần hai nhóm gần nhau nhất, ghi lại từng bước gộp."),
          ("fcluster(Z, k, \"maxclust\")", "scipy", "Cắt cây gộp để còn đúng k cụm, trả nhãn cụm từng chuỗi."),
          ("squareform(D)", "scipy", "Đổi ma trận khoảng cách vuông thành dạng gọn mà linkage cần.")],
     ket_qua="Không chuẩn hoá: mức trung vị các cụm tăng đều từ 1.585 tới 9.832, chỉ xếp theo độ lớn. Chuẩn hoá: bốn cụm là bốn hình dạng.",
     hinh=(9, "kn-dtw-dynamic-time-warping"), nguon="rút gọn từ buoi-09/tu-hoc.ipynb, phần 5"),

dict(ma="code-b09-abc-xyz", buoi=9, sec="4.6", tieu="Code: bảng ABC–XYZ cho mã hàng",
     muc="Xếp mã hàng theo doanh thu và theo CV, rồi kiểm CV có đo được độ khó không.",
     code='''import numpy as np
from scipy import stats

# ban_le: doanh thu theo (mã hàng, tháng) của Online Retail II
g = ban_le.groupby("StockCode")["doanh_thu"]
h = g.agg(["sum", "mean", "std", "count"])
h = h[h["count"] >= 12].sort_values("sum", ascending=False)  # ≥ 12 tháng
h["cv"] = h["std"] / h["mean"]                    # hệ số biến thiên
ty_le = np.arange(1, len(h) + 1) / len(h)         # vị trí theo doanh thu
h["abc"] = np.where(ty_le <= 0.2, "A", np.where(ty_le <= 0.5, "B", "C"))
h["xyz"] = np.where(h["cv"] < 0.5, "X", np.where(h["cv"] <= 1, "Y", "Z"))
o = h.groupby(["abc", "xyz"]).size().unstack(fill_value=0)   # bảng 3 × 3

cv = bang["he_so_bien_thien"]                     # 4.000 chuỗi M4
r = stats.spearmanr(cv, bang["smape_snaive"])[0]''',
     buoc=[("4–6", "Tổng hợp từng mã, giữ mã có đủ 12 tháng."),
           ("7", "CV: độ lệch chuẩn chia trung bình."),
           ("8–9", "20% mã đầu là A, 30% tiếp là B, còn lại C."),
           ("10–11", "Chia X, Y, Z theo CV rồi đếm từng ô."),
           ("13–14", "Đối chiếu CV với sai số thật trên M4.")],
     ham=[("groupby().agg([...])", "pandas", "Tính nhiều con số tổng hợp cho từng mã hàng một lúc."),
          ("unstack(fill_value=0)", "pandas", "Xoay bảng dài thành bảng chéo, ô trống điền 0."),
          ("stats.spearmanr", "scipy", "Tương quan trên thứ hạng giữa CV và sMAPE.")],
     ket_qua="2.773 mã hàng; nhóm A mang 74,7% doanh thu; ô CZ đông gần gấp bốn ô AX. Trên M4, Spearman CV × sMAPE 0,765 nhưng CV xếp sai chuỗi mùa vụ đều.",
     hinh=(9, "kn-phan-loai-abc-xyz-ax-cz"), nguon="rút gọn từ buoi-09/tu-hoc.ipynb, phần 6"),
dict(ma="code-b10-luoi", buoi=10, sec="4.1", tieu="Code: dựng lưới rồi mới đếm thiếu",
     muc="isna() chỉ thấy ô rỗng; dựng lưới đủ mốc mới thấy cả những dòng không tồn tại.",
     code='''import numpy as np
import pandas as pd

bang = pd.Series([25, 25, 26, np.nan, 26], index=pd.to_datetime([
    "2024-01-01 00:00", "2024-01-01 00:30", "2024-01-01 01:30",
    "2024-01-01 02:00", "2024-01-01 02:30"]))
luoi = pd.date_range(bang.index.min(), bang.index.max(), freq="30min")
bang.isna().sum()                      # 1: chỉ thấy ô rỗng
bang.reindex(luoi).isna().sum()        # 2: thấy cả mốc 01:00

def do_dai_lo(y):                      # độ dài từng đoạn NaN liền nhau
    thieu = y.isna()
    nhom = (thieu != thieu.shift()).cumsum()[thieu]
    return nhom.groupby(nhom).size()''',
     buoc=[("4–6", "Năm dòng đo, mốc 01:00 không có dòng nào."),
           ("7", "Dựng lưới đủ mọi mốc 30 phút."),
           ("8–9", "Đếm thiếu trước và sau khi đưa lên lưới."),
           ("11–14", "Đánh số từng đoạn thiếu rồi đếm độ dài.")],
     ham=[("pd.date_range", "pandas", "Sinh dãy mốc thời gian đều nhau giữa hai đầu, ở đây mỗi 30 phút."),
          ("reindex", "pandas", "Đặt chuỗi lên bộ mốc mới; mốc nào chưa có dòng thì thành NaN."),
          ("isna().sum()", "pandas", "Đếm số ô rỗng trong những dòng đang có mặt.")],
     ket_qua="Ví dụ: isna() báo 1, lên lưới ra 2. Nội Bài 2024: lưới 17.568 mốc, tệp 17.319 dòng, thiếu 249 mốc mà isna() chỉ thấy 2 ô.",
     hinh=(10, "kn-thieu-moc-thieu-gia-tri"), nguon="rút gọn từ buoi-10/tu-hoc.ipynb, phần 1"),

dict(ma="code-b10-mnar", buoi=10, sec="4.2", tieu="Code: MNAR làm lệch, kiểm bằng số",
     muc="Thấy bằng mô phỏng vì sao MNAR điền kiểu gì cũng lệch, rồi kiểm cơ chế trên dữ liệu thật.",
     code='''import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
moc = pd.date_range("2024-01-01", periods=5000, freq="30min")
that = pd.Series(rng.normal(0, 1, 5000), index=moc)
mcar = that.mask(pd.Series(rng.random(5000) < 0.1, index=moc))  # may rủi
mnar = that.mask(that > 1.0)            # cảm biến tắt khi giá trị cao
noi = lambda s: s.interpolate(limit_direction="both")
that.mean(), noi(mcar).mean(), noi(mnar).mean()

def bang_chung_mnar(bang, tram):        # bang: PM2.5 của 12 trạm
    khac = bang.drop(columns=[tram]).mean(axis=1)   # 11 trạm còn lại
    thieu = bang[tram].isna()
    return khac[thieu].mean() / khac[~thieu].mean() - 1''',
     buoc=[("4–6", "Năm nghìn điểm thật, biết trước đáp án."),
           ("7", "MCAR: xoá ngẫu nhiên 10% số điểm."),
           ("8", "MNAR: xoá đúng những điểm cao hơn 1."),
           ("9–10", "Nội suy rồi so trung bình với số thật."),
           ("12–15", "Khi trạm mất số, trạm khác cao hay thấp?")],
     ham=[("mask(dieu_kien)", "pandas", "Đổi thành NaN mọi ô thoả điều kiện, giữ nguyên các ô còn lại."),
          ("interpolate", "pandas", "Nối thẳng hai số hai bên để lấp ô NaN ở giữa."),
          ("default_rng(0).normal", "numpy", "Bộ sinh số ngẫu nhiên có seed, chạy lại ra đúng số cũ.")],
     ket_qua="Mô phỏng: MNAR mất 16,2%, điền xong trung bình −0,30 thay vì −0,005; MCAR gần như không lệch. Dongsi thiếu thì trạm khác thấp hơn 3,0%.",
     hinh=(10, "kn-mcar-mar-mnar"), nguon="rút gọn từ buoi-10/tu-hoc.ipynb, phần 2"),

dict(ma="code-b10-tra-hinh", buoi=10, sec="4.3", tieu="Code: tìm số trông như số đo",
     muc="Mã, trần, độ phân giải và đoạn kẹt không để lại NaN; phải đo từng dấu vết mới thấy.",
     code='''import numpy as np
import pandas as pd

goc = pd.read_parquet("ghcnh-noi-bai-2024.parquet")    # tệp thô
goc["relative_humidity"].min()      # ra '100': số đang lưu dạng chữ
rh = pd.to_numeric(goc["relative_humidity"], errors="coerce")
tam_nhin = pd.to_numeric(goc["visibility"], errors="coerce")
(tam_nhin == 9.999).mean(), (rh == 100).mean()    # mã và trần
t = pd.to_numeric(goc["temperature"], errors="coerce").dropna()
np.diff(np.sort(t.unique())).min()  # độ phân giải: bước nhỏ nhất

def doan_mac_ket(y, toi_thieu):     # đoạn lặp dài từ toi_thieu bước
    v = y.dropna()
    nhom = (v != v.shift()).cumsum()
    dem = v.groupby(nhom).agg(so_buoc="size", gia_tri="first")
    return dem[dem["so_buoc"] >= toi_thieu]''',
     buoc=[("5", "Cột số lưu dạng chữ thì min so theo chữ."),
           ("6–7", "Ép về kiểu số, chữ lạ thành NaN."),
           ("8", "Tỷ lệ mã 9,999 km và độ ẩm chạm 100%."),
           ("9–10", "Bước nhỏ nhất giữa hai giá trị khác nhau."),
           ("12–16", "Đánh số từng đoạn lặp, giữ đoạn đủ dài.")],
     ham=[("pd.to_numeric", "pandas", "Đổi cột chữ thành số; errors=\"coerce\" biến chữ lạ thành NaN."),
          ("unique", "pandas", "Lấy danh sách các giá trị khác nhau trong cột."),
          ("groupby().agg", "pandas", "Gom các dòng cùng nhóm rồi tính số dòng, giá trị đầu của nhóm.")],
     ket_qua="Độ ẩm dạng chữ: min '100', max '94'. Hơn 1/3 dòng tầm nhìn là mã 9,999; 5,7% độ ẩm chạm trần. Ngưỡng 18 giờ: 2 đoạn kẹt, dài nhất 33,5 giờ.",
     hinh=(10, "kn-cam-bien-dung-yen-stuck-sensor"), nguon="rút gọn từ buoi-10/tu-hoc.ipynb, phần 3"),

dict(ma="code-b10-dien", buoi=10, sec="4.4", tieu="Code: các cách điền một lỗ",
     muc="Đặt các cách điền cạnh nhau trên một lỗ nhỏ để thấy cách nào biết hình dạng đoạn mất.",
     code='''import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents

hom_nay = pd.Series([21, 23, np.nan, np.nan, 27, 25.0])  # thật: 26, 28
hom_qua = pd.Series([20, 22, 25, 27, 26, 24.0])
tay = {"ffill": hom_nay.ffill(),                    # nhân quả
       "tuyến tính": hom_nay.interpolate(),         # nhìn số phía sau
       "spline": hom_nay.interpolate(method="spline", order=3),
       "mùa vụ": hom_nay.fillna(hom_qua),           # cùng giờ hôm qua
       "hàng xóm + 1": hom_nay.fillna(hom_qua + 1)}
def dien_kalman(y, chu_ky=48):          # mức + nhịp ngày, nhìn hai phía
    kq = UnobservedComponents(y.to_numpy(float), level="local level",
        freq_seasonal=[{"period": chu_ky, "harmonics": 2}]).fit(disp=False)
    lam_tron = kq.smoother_results.smoothed_forecasts[0]
    return y.fillna(pd.Series(lam_tron, index=y.index))''',
     buoc=[("5–6", "Lỗ hai bước hôm nay, và số cùng giờ hôm qua."),
           ("7–9", "Ba cách chỉ biết hai đầu lỗ."),
           ("10–11", "Hai cách mượn hình dạng từ nguồn khác."),
           ("12–16", "Khớp mô hình chuỗi rồi lấy giá trị làm trơn.")],
     ham=[("ffill", "pandas", "Lấp ô trống bằng số gần nhất phía trước."),
          ("fillna(chuoi_khac)", "pandas", "Lấp ô trống bằng số cùng vị trí của một chuỗi khác."),
          ("UnobservedComponents", "statsmodels", "Mô hình chuỗi gồm mức đổi dần và nhịp lặp, ước lượng được ô thiếu.")],
     ket_qua="ffill sai nhiều nhất (3 và 5), tuyến tính 1,67 và 2,33, mùa vụ 1 và 1, hàng xóm trúng cả hai. Nội Bài với Open-Meteo có r = 0,976.",
     hinh=(10, "kn-dien-du-lieu-imputation"), nguon="rút gọn từ buoi-10/tu-hoc.ipynb, phần 4"),

dict(ma="code-b10-che", buoi=10, sec="4.5", tieu="Code: che điểm và che khối",
     muc="Tự xoá số đang có rồi điền lại để có đáp án, và che theo đúng hai kiểu lỗ thật.",
     code='''import numpy as np

def che_diem(y, ty_le=0.10, seed=0):     # rải 10% ô đang có số
    rng = np.random.default_rng(seed)
    co = np.flatnonzero(y.notna().to_numpy())
    chon = rng.choice(co, size=int(len(co) * ty_le), replace=False)
    return y.mask(np.isin(np.arange(len(y)), chon))

def che_khoi(y, so_buoc=96, so_khoi=5, seed=0):   # 5 khối 48 giờ
    rng = np.random.default_rng(seed)
    z = y.copy()
    for _ in range(so_khoi):
        dau = int(rng.integers(0, len(y) - so_buoc))
        z.iloc[dau:dau + so_buoc] = np.nan
    return z
cham = lambda that, z, dien: (dien(z) - that)[z.isna()].abs().mean()''',
     buoc=[("3–7", "Chọn ngẫu nhiên 10% ô có số rồi xoá."),
           ("9–15", "Xoá năm đoạn liền, mỗi đoạn 96 bước."),
           ("16", "MAE chỉ tính trên những ô vừa bị che.")],
     ham=[("rng.choice", "numpy", "Rút ngẫu nhiên một số phần tử, replace=False để không trùng."),
          ("rng.integers", "numpy", "Rút một số nguyên ngẫu nhiên trong khoảng cho trước."),
          ("iloc[a:b]", "pandas", "Chọn các dòng theo vị trí từ a tới trước b.")],
     ket_qua="Tuyến tính hạng 1 ở lỗ ngắn (MAE 0,291 °C) nhưng hạng 5 ở lỗ 48 giờ (2,171); hàng xóm đi ngược lại, hạng 5 lên hạng 1.",
     hinh=(10, "kn-che-nhan-tao"), nguon="rút gọn từ buoi-10/tu-hoc.ipynb, phần 5"),

dict(ma="code-b10-lam-sach", buoi=10, sec="4.6", tieu="Code: chỉ điền lỗ ngắn, kiểm rò rỉ",
     muc="Gói làm sạch thành hàm chỉ điền lỗ ngắn kèm cột cờ, rồi dùng máy kiểm có rò rỉ không.",
     code='''import pandas as pd

def lam_sach(v, nghi, gioi_han=6, cach=dien_mua_vu):
    sach = v.where(~nghi)                  # loại số nghi ngờ TRƯỚC
    thieu = sach.isna()
    nhom = (thieu != thieu.shift()).cumsum()
    do_dai = nhom.map(nhom[thieu].value_counts()).where(thieu, 0)
    dien_duoc = thieu & (do_dai <= gioi_han)    # chỉ lỗ tới 3 giờ
    kq = sach.where(~dien_duoc, cach(sach))     # mùa vụ: nhân quả
    return pd.DataFrame({"y": kq, "da_dien": dien_duoc & kq.notna()})

def kiem_ro_ri(ham, bang, moc_cat):        # moc_cat nằm TRONG một lỗ
    truoc = moc_cat - pd.Timedelta("30min")
    day = ham(bang).loc[:truoc, "y"]
    cat = ham(bang.loc[:truoc])["y"]
    return (day - cat).abs().max() > 1e-9  # True là có rò rỉ''',
     buoc=[("4", "Biến số nghi ngờ thành NaN trước tiên."),
           ("5–7", "Đo lại độ dài lỗ cho từng ô thiếu."),
           ("8–9", "Chỉ điền lỗ ngắn, lỗ dài để trống."),
           ("10", "Xuất kèm cột cờ ô nào là số điền."),
           ("12–16", "Làm sạch đủ và cắt, so phần trước mốc cắt.")],
     ham=[("where(dieu_kien, khac)", "pandas", "Giữ ô thoả điều kiện, ô còn lại lấy từ chuỗi khác."),
          ("value_counts", "pandas", "Đếm mỗi giá trị xuất hiện bao nhiêu lần, ở đây là cỡ mỗi lỗ."),
          ("kiem_ro_ri", "tự viết", "So kết quả làm sạch trên dữ liệu đủ và dữ liệu cắt tại một mốc.")],
     ket_qua="Nội Bài: 130 ô bị loại vì nghi ngờ, 198 ô được điền, 181 ô để trống. Điền mọi lỗ bằng tuyến tính bị bắt khi cắt trong lỗ.",
     hinh=(10, "kn-nhan-qua-cach-dien"), nguon="rút gọn từ buoi-10/tu-hoc.ipynb, phần 6"),

dict(ma="code-b11-bon-loai", buoi=11, sec="4.1", tieu="Code: nhận loại bất thường",
     muc="Bốn loại bất thường giống nhau ở mốc lạ; chỉ các điểm sau mốc đó mới tách được chúng.",
     code='''import numpy as np
import pandas as pd

bon = {"AO (điểm đơn)": [10, 10, 10, 25, 10, 10, 10, 10],
       "dịch mức": [10, 10, 10, 20, 20, 20, 20, 20],
       "thay đổi tạm": [10, 10, 10, 20, 15, 12, 11, 10],
       "đổi phương sai": [10, 10, 10, 14, 6, 13, 7, 14]}
bang = pd.DataFrame({ten: {
    "điểm 4": v[3],
    "TB 4 điểm sau": np.mean(v[4:]),               # có ở lại không
    "điểm cuối": v[-1],                            # có hồi về không
    "độ lệch chuẩn sau": np.std(v[4:], ddof=1),    # có rung mạnh hơn
} for ten, v in bon.items()}).T''',
     buoc=[("4–7", "Bốn chuỗi tám điểm, cùng mức nền 10."),
           ("9", "Riêng điểm lạ thì chưa phân biệt được."),
           ("10–12", "Nhìn sau mốc lạ: ở lại, hồi về hay rung."),
           ("13", "Làm một bảng, mỗi dòng một loại.")],
     ham=[("np.mean", "numpy", "Trung bình cộng các số."),
          ("np.std(ddof=1)", "numpy", "Độ lệch chuẩn mẫu: số đo độ dao động quanh trung bình.")],
     ket_qua="Điểm 4 không tách được ba loại đầu; bốn điểm sau thì tách: AO về 10, dịch mức ở lại 20, thay đổi tạm hồi dần. Đổi phương sai: độ lệch chuẩn 4,08.",
     hinh=(11, "kn-ngoai-lai-outlier"), nguon="rút gọn từ buoi-11/tu-hoc.ipynb, phần 1"),

dict(ma="code-b11-masking", buoi=11, sec="4.2", tieu="Code: ngưỡng 3σ bỏ sót ngoại lai",
     muc="Thấy bằng số vì sao ngoại lai lớn kéo chính trung bình và độ lệch chuẩn dùng để bắt nó.",
     code='''import numpy as np
import pandas as pd

def z_score(y, nguong=3.0):
    return ((y - y.mean()) / y.std()).abs() > nguong

mot = np.array([10, 12, 11, 13, 12, 50, 11, 12, 13, 12.0])
z = (mot - mot.mean()) / mot.std(ddof=1)     # z của số 50
tran = (mot.size - 1) / np.sqrt(mot.size)   # trần của |z| khi n = 10

them = tong.copy()                          # tong: lượt xem Wikipedia
them.iloc[len(tong) // 2] = tong.max() * 8  # thêm một ngày giả
z_score(tong).sum(), z_score(them).sum()    # số ngày bị gắn cờ''',
     buoc=[("4–5", "Gắn cờ khi cách trung bình quá 3σ."),
           ("7–8", "Mười số có một ngoại lai 50."),
           ("9", "Mười số thì |z| không bao giờ vượt 2,85."),
           ("11–13", "Thêm một ngày giả rồi đếm lại số cờ.")],
     ham=[("y.mean(), y.std()", "pandas", "Trung bình và độ lệch chuẩn của cả chuỗi, ngoại lai kéo được cả hai."),
          ("np.sqrt", "numpy", "Căn bậc hai.")],
     ket_qua="z của 50 chỉ 2,84, dưới trần 2,85 nên không bị bắt. Wikipedia: thêm một ngày giả, số ngày bị gắn cờ tụt từ 16 xuống 5.",
     hinh=(11, "masking-10-so"), nguon="rút gọn từ buoi-11/tu-hoc.ipynb, phần 2"),

dict(ma="code-b11-hampel", buoi=11, sec="4.3", tieu="Code: MAD và bộ lọc Hampel",
     muc="Đổi trung bình thành trung vị để ngoại lai không kéo được thước đo, rồi trượt theo cửa sổ.",
     code='''import numpy as np
import pandas as pd

HE_SO_MAD = 1.4826             # đưa MAD về thang độ lệch chuẩn

def mad_score(y):
    tv = y.median()
    mad = (y - tv).abs().median()
    return (y - tv).abs() / (HE_SO_MAD * mad)

def hampel(y, cua_so=15, nguong=3.0):     # cửa sổ ±15 ngày quanh điểm
    k = 2 * cua_so + 1
    tv = y.rolling(k, center=True, min_periods=cua_so).median()
    mad = (y - tv).abs().rolling(k, center=True, min_periods=cua_so).median()
    diem = (y - tv).abs() / (HE_SO_MAD * mad.replace(0, np.nan))
    return diem.fillna(0) > nguong''',
     buoc=[("6–9", "Khoảng cách tới trung vị, chia cho MAD."),
           ("11–13", "Trung vị của 31 ngày quanh mỗi điểm."),
           ("14", "MAD cũng tính trên cửa sổ đó."),
           ("15–16", "Gắn cờ điểm cách mức địa phương quá 3.")],
     ham=[("median", "pandas", "Trung vị: số đứng giữa khi xếp thứ tự, ngoại lai không kéo được."),
          ("rolling(k, center=True)", "pandas", "Cửa sổ k điểm đặt giữa là điểm đang xét."),
          ("hampel", "tự viết", "Gắn cờ điểm lệch xa trung vị quanh nó, tính theo MAD.")],
     ket_qua="Điểm MAD của 50 là 25,6, bắt ngay. Wikipedia: Hampel gắn cờ 121 ngày rải đều mười năm, thêm ngày giả chỉ thành 123.",
     hinh=(11, "kn-bo-loc-hampel"), nguon="rút gọn từ buoi-11/tu-hoc.ipynb, phần 3"),

dict(ma="code-b11-tet", buoi=11, sec="4.4", tieu="Code: giữ Tết, winsorize lỗi đo",
     muc="Ngưỡng nào cũng gắn cờ Tết; nhật ký sự kiện giữ nó lại, còn lỗi đo thì thay chứ không xoá.",
     code='''import pandas as pd

dinh = [g.idxmax() for _, g in tet.groupby(tet.index.year)]  # đỉnh Tết
[bool(hampel(tet)[d]) for d in dinh]      # cả 10 đỉnh bị gắn cờ

def xu_ly_ngoai_lai(y, cua_so=15, bo_qua_su_kien=()):
    y = y.astype(float)
    su_kien = y.index.isin(pd.DatetimeIndex(bo_qua_su_kien))
    co = hampel(y, cua_so) & ~su_kien         # sự kiện thật thì bỏ qua
    k = 2 * cua_so + 1
    tv = y.rolling(k, center=True, min_periods=cua_so).median()
    sach = y.where(~co, tv)                   # winsorize, không xoá mốc
    return pd.DataFrame({"y": y, "sach": sach, "da_sua": co})

xl = xu_ly_ngoai_lai(tet, bo_qua_su_kien=dinh)''',
     buoc=[("3", "Ngày đông nhất mỗi năm chính là Tết."),
           ("4", "Kiểm xem Hampel có gắn cờ các đỉnh không."),
           ("8–9", "Bỏ cờ ở những mốc có trong nhật ký."),
           ("10–12", "Thay điểm lỗi bằng trung vị quanh nó."),
           ("15", "Chạy trên bài Tết, nhật ký là mười đỉnh.")],
     ham=[("idxmax", "pandas", "Trả về mốc thời gian có giá trị lớn nhất."),
          ("index.isin", "pandas", "Đánh dấu mốc nào nằm trong một danh sách cho trước."),
          ("xu_ly_ngoai_lai", "tự viết", "Gắn cờ bằng Hampel, chừa sự kiện, thay điểm lỗi bằng trung vị.")],
     ket_qua="Năm cách gắn cờ đều bắt 10/10 đỉnh Tết. Xoá theo 3σ mất 54 mốc, cả mười đỉnh; winsorize cộng nhật ký giữ đủ 3.653 mốc.",
     hinh=(11, "kn-winsorize"), nguon="rút gọn từ buoi-11/tu-hoc.ipynb, phần 4"),

dict(ma="code-b11-pelt", buoi=11, sec="4.5", tieu="Code: PELT, lấy log, quét penalty",
     muc="Tìm mốc chuỗi đổi hẳn bằng PELT, và chỉ tin điểm gãy không đổi khi penalty đổi.",
     code='''import numpy as np
import ruptures as rpt

v = np.array([10, 11, 10, 9, 10, 20, 21, 19, 20, 20.0])
beta = 3 * np.log(v.size)                 # phí mỗi điểm gãy
rpt.Pelt(model="l2", min_size=2).fit(v).predict(pen=beta)

def diem_gay(y, pen=None, log=True):
    x = np.log(y.to_numpy(float)) if log else y.to_numpy(float)
    pen = 3 * np.log(x.size) if pen is None else pen
    cat = rpt.Pelt(model="l2", min_size=3).fit(x).predict(pen=pen)
    return [y.index[i] for i in cat[:-1]]   # phần tử cuối là độ dài

ln_n = np.log(len(hk))                     # hk: hành khách hàng không EU
for he_so in (0.5, 1, 2, 3, 4, 6, 10):     # quét penalty
    print(he_so, diem_gay(hk, pen=he_so * ln_n))''',
     buoc=[("4–5", "Mười số có một bậc, phí cắt là 3 ln n."),
           ("6", "PELT tìm cách cắt rẻ nhất."),
           ("9", "Lấy log để mùa hè đông khách thôi gãy."),
           ("11–12", "Chạy PELT, đổi vị trí cắt thành ngày tháng."),
           ("14–16", "Thử bảy mức penalty, xem điểm nào trụ lại.")],
     ham=[("rpt.Pelt", "ruptures", "Tìm các mốc chia chuỗi thành đoạn, mỗi mốc phải trả một khoản phạt."),
          ("predict(pen=...)", "ruptures", "Trả vị trí kết thúc từng đoạn với mức phạt cho trước."),
          ("np.log", "numpy", "Lấy logarit, biến tăng theo tỷ lệ thành tăng đều.")],
     ket_qua="Ví dụ: ruptures trả [5, 10]. Hàng không EU: mức gốc ra 43 điểm gãy, log ra 2, ổn định từ 1 tới 4 ln n: 2/2020 (−78,7%) và 5/2021.",
     hinh=(11, "kn-penalty-phat"), nguon="rút gọn từ buoi-11/tu-hoc.ipynb, phần 5"),

dict(ma="code-b11-covid", buoi=11, sec="4.6", tieu="Code: ba cách xử lý COVID",
     muc="Giữ mô hình cố định, chỉ đổi cách xử lý COVID, để thấy lựa chọn đó đổi dự báo ra sao.",
     code='''import numpy as np
import pandas as pd

def du_bao_mua_vu_xu_huong(hoc, tam):     # xu hướng thẳng × mùa vụ nhân
    x = hoc.to_numpy(float)
    t = np.arange(x.size)
    a, b = np.polyfit(t, x, 1)
    he_so = pd.Series(x / np.maximum(a * t + b, 1), index=hoc.index)
    he_so = he_so.groupby(hoc.index.month).mean()
    moc = pd.date_range(hoc.index[-1], periods=tam + 1, freq="MS")[1:]
    return np.array([(a * (x.size + i) + b) * he_so[m.month]
                     for i, m in enumerate(moc)])
hoc = hk[hk.index < "2023-01-01"]         # học tới hết 2022
covid = (hoc.index >= "2020-03-01") & (hoc.index <= "2021-06-30")
cach = {"giữ nguyên": hoc, "coi là thiếu": hoc.mask(covid).interpolate(),
        "cắt": hoc[hoc.index > "2021-06-30"]}''',
     buoc=[("5–7", "Khớp một đường thẳng làm xu hướng."),
           ("8–9", "Mỗi tháng là một tỷ lệ so với xu hướng."),
           ("10–12", "Kéo dài xu hướng, nhân hệ số tháng."),
           ("14", "Đánh dấu 16 tháng COVID."),
           ("15–16", "Ba cách: giữ, coi là thiếu rồi nội suy, cắt.")],
     ham=[("np.polyfit(t, x, 1)", "numpy", "Tìm đường thẳng khớp dữ liệu nhất, trả độ dốc và tung độ gốc."),
          ("groupby(month).mean()", "pandas", "Trung bình theo từng tháng trong năm."),
          ("mask().interpolate()", "pandas", "Coi đoạn đã chọn là thiếu rồi nối thẳng qua nó.")],
     ket_qua="MAPE 2023: coi là thiếu 8,71%, giữ nguyên 24,01%. Giữ nguyên thì 16 tháng sụt kéo xu hướng xuống, dự báo thấp gần 20 triệu khách/tháng.",
     hinh=(11, "ba-cach-covid"), nguon="rút gọn từ buoi-11/tu-hoc.ipynb, phần 6"),

dict(ma="code-b12-trailing", buoi=12, sec="4.1", tieu="Code: trailing và centered",
     muc="Thấy bằng số kiểu centered viết lại quá khứ khi có số mới, còn trailing thì không.",
     code='''import pandas as pd

y = pd.Series([10, 12, 14, 30, 16], index=range(1, 6), dtype=float)
trailing = y.rolling(3).mean()                # chỉ quá khứ, nhưng trễ
centered = y.rolling(3, center=True).mean()   # nửa cửa sổ ở tương lai

y2 = y.copy()
y2[5] = 40                                    # số mới về khác đi
y2.rolling(3).mean()[4]                       # giờ 4 giữ nguyên
y2.rolling(3, center=True).mean()[4]          # giờ 4 bị viết lại''',
     buoc=[("3", "Năm giờ điện, giờ 4 vọt lên 30."),
           ("4–5", "Hai kiểu trung bình trượt ba điểm."),
           ("7–8", "Đổi riêng giờ cuối từ 16 thành 40."),
           ("9–10", "Xem giá trị của giờ 4 có đổi theo không.")],
     ham=[("rolling(3).mean()", "pandas", "Trung bình ba điểm: điểm đang xét và hai điểm trước."),
          ("rolling(3, center=True)", "pandas", "Cửa sổ đặt giữa, nên dùng cả điểm ngay sau.")],
     ket_qua="Giờ 3 kiểu centered ra 18,67 vì đã cộng số 30 của giờ 4. Đổi giờ 5 thành 40: centered giờ 4 nhảy từ 20 lên 28, trailing vẫn 18,67.",
     hinh=(12, "kn-bo-loc-nhan-qua"), nguon="rút gọn từ buoi-12/tu-hoc.ipynb, phần 1"),

dict(ma="code-b12-pho", buoi=12, sec="4.2", tieu="Code: đọc phổ bằng Welch",
     muc="Trước khi lọc, đo xem dao động nhanh chiếm bao nhiêu năng lượng và nhịp nào mạnh nhất.",
     code='''import numpy as np
from scipy import signal

FS = 6.0                                  # 6 mẫu mỗi giờ (10 phút/mẫu)
for v in ([1, -1, 1, -1, 1, -1], [1, 1, 1, -1, -1, -1]):
    f, P = signal.periodogram(v)
    f[np.argmax(P)]                       # tần số mạnh nhất

def pho(y, fs=FS, nperseg=2048):          # trừ trung bình trước
    y = np.asarray(y, dtype=float)
    y = y - np.nanmean(y)
    return signal.welch(y, fs=fs, nperseg=min(nperseg, y.size))

f, P = pho(dien)                          # dien: điện thiết bị, Wh
chu_ky_manh = 1 / f[1:][np.argmax(P[1:])]  # tính bằng giờ
nhanh = P[f > 1].sum() / P[1:].sum()      # phần năng lượng dưới 1 giờ''',
     buoc=[("5–7", "Hai dãy tay: lặp mỗi 2 bước và mỗi 6 bước."),
           ("9–12", "Trừ trung bình để tần số 0 không át hết."),
           ("14–15", "Chu kỳ mạnh nhất, bỏ qua tần số 0."),
           ("16", "Tỷ lệ năng lượng ở dao động nhanh hơn 1 giờ.")],
     ham=[("signal.periodogram", "scipy", "Tính năng lượng của từng tần số trong một dãy số."),
          ("signal.welch", "scipy", "Phổ ổn định: chia chuỗi thành đoạn, lấy trung bình phổ các đoạn."),
          ("np.argmax", "numpy", "Vị trí của giá trị lớn nhất.")],
     ket_qua="Ví dụ tay: đỉnh ở 0,5 và 1/6. Cả hai cảm biến có đỉnh 24,38 giờ; điện thiết bị có 17,8% năng lượng dưới 1 giờ, nhiệt độ phòng 0,0.",
     hinh=(12, "kn-periodogram-welch"), nguon="rút gọn từ buoi-12/tu-hoc.ipynb, phần 2"),

dict(ma="code-b12-aliasing", buoi=12, sec="4.3", tieu="Code: lọc thông thấp rồi mới hạ mẫu",
     muc="Hạ mẫu thô làm dao động nhanh gập thành chu kỳ giả; lọc trước thì chu kỳ đó biến mất.",
     code='''import numpy as np
from scipy import signal
FS = 6.0                                   # 6 mẫu mỗi giờ

def f_gia(f, fs):                          # tần số giả sau khi lấy mẫu
    return abs(f - round(f / fs) * fs)

def ha_mau(y, buoc=6, loc_truoc=True):
    y = np.asarray(y, dtype=float)
    if not loc_truoc:
        return y[::buoc]                   # hạ mẫu thô
    sos = signal.butter(8, 0.8 * FS / buoc / 2, fs=FS, output="sos")
    return signal.sosfiltfilt(sos, y)[::buoc]   # hai chiều: chỉ lịch sử

t = np.arange(6000) / FS                   # thời gian, tính bằng giờ
y = 20 + 2 * np.sin(2 * np.pi * t / 24) + 0.5 * np.sin(2 * np.pi * 1.4 * t)''',
     buoc=[("5–6", "Tính tần số bị gập về sau khi lấy mẫu."),
           ("11", "Lấy mỗi 6 mẫu một: dễ sinh chu kỳ giả."),
           ("12", "Bộ lọc cắt ở 0,8 lần Nyquist mới."),
           ("13", "Lọc hai chiều rồi mới lấy mẫu."),
           ("15–16", "Nhịp ngày cộng dao động 1,4 chu kỳ/giờ.")],
     ham=[("signal.butter", "scipy", "Thiết kế bộ lọc Butterworth: giữ tần số thấp, chặn tần số cao."),
          ("signal.sosfiltfilt", "scipy", "Lọc xuôi rồi lọc ngược: không trễ nhưng dùng cả tương lai."),
          ("y[::buoc]", "numpy", "Lấy một phần tử sau mỗi buoc phần tử.")],
     ket_qua="1,4 chu kỳ/giờ lấy mẫu mỗi giờ gập thành 0,4: chu kỳ giả 2,5 giờ, công suất 64,0 khi hạ mẫu thô và 0,0 khi lọc trước.",
     hinh=(12, "kn-aliasing"), nguon="rút gọn từ buoi-12/tu-hoc.ipynb, phần 3"),

dict(ma="code-b12-bo-loc", buoi=12, sec="4.4", tieu="Code: sáu họ bộ lọc",
     muc="Chạy các họ bộ lọc trên cùng chuỗi mô phỏng để so độ trơn, độ trễ và việc nhìn tương lai.",
     code='''import pandas as pd
from scipy import signal
from statsmodels.tsa.statespace.structural import UnobservedComponents

s = pd.Series(mp)                    # mp: mô phỏng có nhiễu, seed 0
sos = signal.butter(4, 0.05, output="sos")        # Butterworth bậc 4
uc = UnobservedComponents(mp, level="local level")
p = UnobservedComponents(mp[:666], level="local level").fit(disp=0).params
ra = {"MA trailing 13": s.rolling(13, min_periods=1).mean(),
      "MA centered 13": s.rolling(13, center=True, min_periods=1).mean(),
      "EWMA α=0,15": s.ewm(alpha=0.15).mean(),
      "Savitzky–Golay 13": signal.savgol_filter(mp, 13, 2),
      "Butterworth nhân quả": signal.sosfilt(sos, mp),
      "Butterworth filtfilt": signal.sosfiltfilt(sos, mp),
      "Kalman filter": uc.filter(p).filtered_state[0],
      "Kalman smoother": uc.smooth(p).smoothed_state[0]}''',
     buoc=[("7–8", "Tham số Kalman chỉ học trên 1/3 đầu."),
           ("9–11", "Trung bình trượt hai kiểu và EWMA."),
           ("12", "Khớp đa thức bậc 2 trong cửa sổ 13."),
           ("13–14", "Cùng bộ lọc, một chiều hay hai chiều."),
           ("15–16", "Kalman: filter chỉ quá khứ, smoother cả hai.")],
     ham=[("ewm(alpha).mean()", "pandas", "Trung bình có trọng số giảm dần về quá khứ."),
          ("signal.savgol_filter", "scipy", "Khớp đa thức trong cửa sổ trượt có tâm, giữ đỉnh tốt."),
          ("UnobservedComponents", "statsmodels", "Mô hình mức đổi dần; filter chỉ dùng quá khứ, smooth dùng cả hai phía.")],
     ket_qua="Ba RMSE thấp nhất (centered 0,357, Kalman smoother, Savitzky–Golay) đều nhìn tương lai. Nhân quả tốt nhất: Kalman filter 0,584, trễ 1.",
     hinh=(12, "kn-tre-pha"), nguon="rút gọn từ buoi-12/tu-hoc.ipynb, phần 4"),

dict(ma="code-b12-kiem-nhan-qua", buoi=12, sec="4.5", tieu="Code: đổi đuôi, xem đầu",
     muc="Một phép thử chạy được cho mọi bộ lọc: đổi đuôi chuỗi, xem quá khứ có bị đổi theo không.",
     code='''import numpy as np

def kiem_nhan_qua(ham_loc, y, so_diem_doi=10, thay_doi=50.0):
    y = np.asarray(y, dtype=float)
    k0 = y.size - so_diem_doi
    goc = np.asarray(ham_loc(y), dtype=float)
    y_doi = y.copy()
    y_doi[k0:] += thay_doi                 # cộng 50 vào 10 số cuối
    moi = np.asarray(ham_loc(y_doi), dtype=float)
    lech = np.abs(np.nan_to_num(moi[:k0]) - np.nan_to_num(goc[:k0]))
    nguong = max(1e-9, 1e-7 * float(np.nanmax(np.abs(y))))  # sai số máy
    return lech.max() > nguong             # True: có nhìn tương lai

{ten: kiem_nhan_qua(ham, mp) for ten, ham in BO_LOC.items()}''',
     buoc=[("6", "Chạy bộ lọc trên chuỗi gốc."),
           ("7–9", "Đổi đuôi chuỗi rồi chạy lại."),
           ("10", "So mọi mốc trước chỗ đổi."),
           ("11–12", "Lệch quá sai số máy tức là nhìn tương lai."),
           ("14", "Kiểm cả mười cấu hình bộ lọc.")],
     ham=[("np.nan_to_num", "numpy", "Đổi NaN thành 0 để phép trừ không ra NaN."),
          ("np.nanmax", "numpy", "Giá trị lớn nhất, bỏ qua các ô NaN."),
          ("kiem_nhan_qua", "tự viết", "Báo một hàm lọc có dùng số tương lai hay không.")],
     ket_qua="6/10 cấu hình nhìn tương lai. Centered 13 đổi quá khứ 23,077; Kalman khớp lại cả chuỗi đổi 1,134; filtfilt làm bẩn ngược 274 bước.",
     hinh=(12, "kiem-nhan-qua"), nguon="rút gọn từ buoi-12/tu-hoc.ipynb, phần 5"),

dict(ma="code-b12-gia-ro-ri", buoi=12, sec="4.6", tieu="Code: đo cái giá của rò rỉ",
     muc="Đo feature nhìn tương lai làm sai số đẹp giả bao nhiêu, khi chấm trên chuỗi gốc.",
     code='''import numpy as np
import pandas as pd

def danh_gia_feature(y, ham_loc, tam=6, ty_le_hoc=0.7):
    bang = pd.DataFrame({"loc": ham_loc(y.to_numpy()), "y": y.to_numpy(),
                         "muc_tieu": y.shift(-tam).to_numpy()}).dropna()
    cat = int(len(bang) * ty_le_hoc)       # 70% đầu học, 30% sau chấm
    hoc, kt = bang.iloc[:cat], bang.iloc[cat:]
    X = lambda d: np.column_stack([np.ones(len(d)), d["loc"], d["y"]])
    he_so = np.linalg.lstsq(X(hoc), hoc["muc_tieu"], rcond=None)[0]
    du_bao = X(kt) @ he_so
    return np.mean(np.abs(du_bao - kt["muc_tieu"]))   # trên chuỗi gốc

goc = danh_gia_feature(dien, lambda v: v)     # không lọc
centered = danh_gia_feature(dien, ma_giua)    # nhìn tương lai
trailing = danh_gia_feature(dien, ma_truoc)   # nhân quả''',
     buoc=[("5–6", "Feature là bộ lọc và giá trị hiện tại."),
           ("6", "Mục tiêu là điện 6 bước sau, tức 1 giờ tới."),
           ("7–8", "Chia theo thời gian, không xáo trộn."),
           ("9–11", "Hồi quy tuyến tính bằng bình phương nhỏ nhất."),
           ("14–16", "So MAE khi không lọc và hai kiểu lọc.")],
     ham=[("shift(-6)", "pandas", "Kéo chuỗi lên 6 bước: dòng t nhận giá trị của t + 6."),
          ("np.linalg.lstsq", "numpy", "Tìm hệ số hồi quy tuyến tính cho sai số bình phương nhỏ nhất."),
          ("np.column_stack", "numpy", "Ghép các cột thành một ma trận.")],
     ket_qua="Không lọc MAE 46,84 Wh. Centered giảm 27,7%, filtfilt 24,5%, đều giả; feature nhân quả chỉ giúp 0,9–5,9%.",
     hinh=(12, "gia-ro-ri"), nguon="rút gọn từ buoi-12/tu-hoc.ipynb, phần 6"),
# ------------------------------------------------------------------ buổi 13
    dict(ma="code-b13-biet-truoc", buoi=13, sec="4.1",
         tieu="Code: feature nào đã có lúc dự báo",
         muc="Hỏi từng feature \"lúc ra dự báo tôi có nó chưa?\" rồi xếp vào đúng nhóm.",
         code='''import pandas as pd

t = pd.Timestamp("2010-06-07")              # tối thứ Hai ra dự báo
muc_tieu = t + pd.Timedelta(days=1)         # thứ Ba, h = 1
thu = muc_tieu.dayofweek                    # lịch: biết trước mãi mãi
tb_da_biet = y[:t].mean()                   # chỉ các ngày tới t
tb_ca_chuoi = y.mean()                      # gồm cả ngày chưa xảy ra

def bang_biet_truoc(cot):                   # xếp theo TÊN cột
    if cot.startswith(("lag_", "tb_", "sd_")):
        return "t-h"                        # quá khứ của chuỗi
    if cot.startswith(("du_bao_", "khuyen_mai")):
        return "kế hoạch"                   # đã công bố
    if cot.endswith("_that"):
        return "KHÔNG BIẾT TRƯỚC"
    return "vô hạn"                         # lịch''',
         buoc=[("3–4", "Tối thứ Hai dự báo doanh thu thứ Ba."),
               ("5", "Thứ của ngày mai là lịch, biết từ trước."),
               ("6–7", "So trung bình tới t với trung bình cả chuỗi."),
               ("9–16", "Đọc tên cột để xếp feature vào một nhóm."),
               ("14–15", "Tên đuôi _that là giá trị thật: loại.")],
         ham=[("pd.Timestamp, pd.Timedelta", "pandas", "Tạo một mốc thời gian rồi cộng thêm một khoảng, ở đây là 1 ngày."),
              ("y[:t].mean()", "pandas", "Cắt chuỗi tới mốc t rồi lấy trung bình, bỏ phần tương lai."),
              ("bang_biet_truoc", "tự viết", "Xếp feature vào nhóm lịch, kế hoạch hay quá khứ theo tên cột.")],
         ket_qua="Trung bình 189 ngày đã biết là 27.701, cả chuỗi là 33.454 vì gồm 550 ngày chưa xảy ra. z_score lọt vào nhóm \"vô hạn\": tên sai thì bảng sai.",
         hinh=(13, "biet-truoc"),
         nguon="rút gọn từ buoi-13/tu-hoc.ipynb, phần 1"),

    dict(ma="code-b13-shift", buoi=13, sec="4.2",
         tieu="Code: shift trước, rolling sau",
         muc="Thấy bằng số vì sao phải shift trước rolling, rồi gói thành hàm tạo feature.",
         code='''import pandas as pd
v = pd.Series([10, 12, 8, 14, 20, 16], index=range(1, 7), dtype=float)
sai_1 = v.rolling(3, center=True).mean()     # nhìn cả ngày sau
sai_2 = v.rolling(3).mean()                  # chứa chính ngày t
dung = v.shift(1).rolling(3).mean()          # chỉ quá khứ

def feature_tre(y, tam=1, cac_lag=(1, 2, 3, 7, 14, 28),
                cac_cua_so=(7, 28)):
    f = pd.DataFrame(index=y.index)
    tre = y.shift(tam)                       # lùi h bước TRƯỚC
    for lag in cac_lag:
        f[f"lag_{lag}"] = y.shift(max(lag, tam))   # lag nhỏ nhất ≥ h
    for w in cac_cua_so:
        f[f"tb_{w}"] = tre.rolling(w).mean()       # rolling SAU
        f[f"sd_{w}"] = tre.rolling(w).std()
    return f''',
         buoc=[("2", "Sáu ngày doanh thu, dự báo trước 1 ngày."),
               ("3–5", "Ba cách tính trung bình 3 ngày; chỉ dòng 5 đúng."),
               ("9", "Lùi chuỗi tam bước trước khi làm gì khác."),
               ("10–11", "Lag nhỏ hơn tầm dự báo bị nâng lên bằng tam."),
               ("12–14", "Mọi rolling tính trên chuỗi đã lùi.")],
         ham=[("shift(k)", "pandas", "Dời chuỗi xuống k bước: ngày t nhận giá trị ngày t − k."),
              ("rolling(w).mean()", "pandas", "Trung bình w điểm gần nhất, tính tới chính điểm đó."),
              ("feature_tre", "tự viết", "Tạo các cột lag và rolling theo đúng quy tắc shift trước.")],
         ket_qua="Ngày 4: có tâm ra 14, không shift ra 11,33, shift ra 10. Cắt dữ liệu rồi tính lại: bản shift lệch 0, bản có tâm lệch tới 5.113.",
         hinh=(13, "kn-rolling"),
         nguon="rút gọn từ buoi-13/tu-hoc.ipynb, phần 2"),

    dict(ma="code-b13-lich", buoi=13, sec="4.3",
         tieu="Code: sin/cos, Fourier và Tết",
         muc="Mã hoá lịch sao cho Chủ nhật nằm sát thứ Hai và mùa vụ năm chỉ tốn vài cột.",
         code='''import numpy as np
import pandas as pd
so = np.array([5, 6, 0])                    # thứ Bảy, Chủ nhật, thứ Hai
vong = np.column_stack([np.sin(2 * np.pi * so / 7),
                        np.cos(2 * np.pi * so / 7)])
cn_t2 = np.linalg.norm(vong[1] - vong[2])   # Chủ nhật – thứ Hai

def feature_fourier(moc, chu_ky=365.25, k=3):
    t = (moc - moc[0]).days.to_numpy().astype(float)
    f = pd.DataFrame(index=moc)
    for i in range(1, k + 1):                # sóng lặp i lần mỗi năm
        f[f"fourier_sin_{i}"] = np.sin(2 * np.pi * i * t / chu_ky)
        f[f"fourier_cos_{i}"] = np.cos(2 * np.pi * i * t / chu_ky)
    return f

d = so_ngay_toi_tet(wiki.index)             # Tết tính từ lịch âm UTC+7''',
         buoc=[("3–5", "Đặt ba ngày cuối, đầu tuần lên vòng tròn."),
               ("6", "Đo khoảng cách Chủ nhật tới thứ Hai."),
               ("9", "Đổi ngày thành số ngày kể từ đầu chuỗi."),
               ("11–13", "Mỗi i thêm một cặp sóng, K = 3 cho 6 cột."),
               ("16", "Đếm số ngày tới mùng 1 Tết gần nhất.")],
         ham=[("np.sin, np.cos", "numpy", "Tính sin, cos cho cả mảng một lần; cả cặp mới định vị đúng."),
              ("np.linalg.norm", "numpy", "Độ dài của một vectơ: khoảng cách giữa hai điểm trên vòng."),
              ("so_ngay_toi_tet", "tự viết", "Số ngày tới mùng 1 Tết gần nhất theo lịch âm; âm là đã qua.")],
         ket_qua="Chủ nhật cách thứ Hai 0,868, đúng bằng cách thứ Bảy. Thêm 5 feature Tết: cả năm chỉ tốt hơn 1,9%, quanh Tết tốt hơn 16,9%.",
         hinh=(13, "kn-ma-hoa-tuan-hoan"),
         nguon="rút gọn từ buoi-13/tu-hoc.ipynb, phần 3"),

    dict(ma="code-b13-ca-chuoi", buoi=13, sec="4.4",
         tieu="Code: ba kiểu rò rỉ cả chuỗi",
         muc="Đặt bản sai cạnh bản đúng để thấy số tương lai lọt vào quá khứ ở đâu.",
         code='''import numpy as np
import pandas as pd

v = pd.Series([10, 12, 8, 14, 20, 16], index=range(1, 7), dtype=float)
nhom = pd.Series(["A", "B"] * 3, index=v.index)
co_lo = v.copy()
co_lo[3] = np.nan                                  # ngày 3 mất số
z_sai = (v - v.mean()) / v.std()                   # dùng cả 6 ngày
tb_dung = v.shift(1).expanding().mean()            # chỉ ngày trước t
nhom_sai = v.groupby(nhom).transform("mean")       # có số tương lai
nhom_dung = v.groupby(nhom).transform(
    lambda s: s.shift(1).expanding().mean())       # nhóm, chỉ quá khứ
dien_sai = co_lo.interpolate(limit_direction="both")  # nhìn ngày 4
dien_dung = co_lo.ffill()                          # lấy hôm trước''',
         buoc=[("4–7", "Sáu ngày, hai nhóm, ngày 3 bị mất số."),
               ("8–9", "Chuẩn hoá: toàn chuỗi so với chỉ quá khứ."),
               ("10–12", "Trung bình nhóm: toàn chuỗi so với quá khứ."),
               ("13–14", "Điền chỗ thiếu: hai phía so với lấy hôm trước.")],
         ham=[("shift(1).expanding().mean()", "pandas", "Trung bình từ đầu chuỗi tới hôm qua, không chạm ngày t."),
              ("groupby(nhom).transform", "pandas", "Tính theo từng nhóm rồi trả về đúng chỗ của mỗi dòng."),
              ("interpolate(limit_direction=\"both\")", "pandas", "Điền chỗ thiếu bằng đường nối hai phía, tức dùng cả ngày sau.")],
         ket_qua="Mọi ô z dùng trung bình 13,33 có cả hai ngày cuối. Ngày 1 mang trung bình nhóm A 12,67 có số 20 của ngày 5. Điền hai phía ra 13, ffill ra 12.",
         hinh=None,
         nguon="rút gọn từ buoi-13/tu-hoc.ipynb, phần 4"),

    dict(ma="code-b13-kiem-ro-ri", buoi=13, sec="4.5",
         tieu="Code: bài kiểm cắt tương lai",
         muc="Để máy tự tìm rò rỉ: cắt dữ liệu, tính lại feature, so từng dòng trước mốc.",
         code='''import numpy as np
def kiem_ro_ri(ham_feature, y, cac_moc=None, bo_cuoi=0):
    day_du, bi_bat = ham_feature(y), {}            # tính trên cả chuỗi
    cac_moc = cac_moc or [y.index[int(len(y) * p)]
                          for p in (0.5, 0.7, 0.9)]   # nhiều mốc
    for moc in cac_moc:
        cat = ham_feature(y[y.index <= moc])       # cắt rồi tính lại
        chung = day_du.index[day_du.index <= moc]
        chung = chung[:len(chung) - bo_cuoi]       # bo_cuoi=0: so MỌI dòng
        for cot in day_du.columns:
            a = day_du.loc[chung, cot].to_numpy(float)
            b = cat.reindex(chung)[cot].to_numpy(float)
            khac = ~np.isclose(a, b, rtol=0, atol=1e-9, equal_nan=True)
            if khac.any():
                bi_bat[cot] = max(bi_bat.get(cot, 0), int(khac.sum()))
    return bi_bat                                  # {feature: số dòng đổi}''',
         buoc=[("3", "Tính feature một lần trên dữ liệu đầy đủ."),
               ("4–5", "Cắt ở 50, 70, 90% chuỗi, không chỉ một mốc."),
               ("7", "Bỏ phần sau mốc rồi tính lại feature."),
               ("9", "So mọi dòng trước mốc, không bỏ dòng cuối."),
               ("11–15", "Cột nào đổi dù chỉ một dòng là rò rỉ.")],
         ham=[("np.isclose(equal_nan=True)", "numpy", "So hai mảng từng ô; NaN gặp NaN là bằng, NaN gặp số là khác."),
              ("reindex", "pandas", "Xếp lại bảng theo danh sách mốc cho trước; mốc thiếu thành NaN."),
              ("kiem_ro_ri", "tự viết", "Trả các cột bị đổi khi cắt tương lai, kèm số dòng đổi.")],
         ket_qua="Bản ẩu (một mốc, bỏ 10 dòng cuối) bắt 4 cột, lọt tb_7. Bản đúng bắt đủ 5 cột. Bộ 41 cột đã sửa qua sạch cả hai bài kiểm.",
         hinh=(13, "kiem-ro-ri"),
         nguon="rút gọn từ buoi-13/tu-hoc.ipynb, phần 5"),

    dict(ma="code-b13-ngoai-sinh", buoi=13, sec="4.6",
         tieu="Code: nhiệt độ thật hay dự báo",
         muc="Đo cái giá của rò rỉ: học bằng nhiệt độ thật, chạy bằng bản dự báo nhiệt độ.",
         code='''import pandas as pd

TAM = 24
d["muc_tieu"] = d["phu_tai"].shift(-TAM)            # tải của giờ t + 24
d["lag_24"], d["lag_168"] = d["phu_tai"], d["phu_tai"].shift(144)
for c in ("nhiet_do_that", "du_bao_1_ngay", "du_bao_3_ngay"):
    d[f"{c}_muc_tieu"] = d[c].shift(-TAM)           # nhiệt độ ở giờ đích
NEN = ["lag_24", "lag_168", "gio_sin", "gio_cos"]
ro_ri = mae(NEN + ["nhiet_do_that_muc_tieu"])       # backtest bằng sự thật
chay_that = mae(NEN + ["nhiet_do_that_muc_tieu"],   # học bằng thật,
                NEN + ["du_bao_3_ngay_muc_tieu"])   # chạy bằng dự báo

ghep = pd.merge_asof(trai, phai, left_index=True, right_index=True,
                     direction="backward",           # chỉ bản tin cũ hơn
                     tolerance=pd.Timedelta("3h"))   # quá 3 giờ: để trống''',
         buoc=[("4", "Đích là tải điện 24 giờ sau lúc dự báo."),
               ("6–7", "Ba nguồn nhiệt độ cho đúng giờ cần dự báo."),
               ("9", "Backtest bằng nhiệt độ thật: con số hứa hẹn."),
               ("10–11", "Kịch bản hay gặp: học thật, chạy dự báo."),
               ("13–15", "Ghép bản tin gần nhất trước đó, có hạn 3 giờ.")],
         ham=[("shift(-24)", "pandas", "Kéo giá trị 24 giờ sau về dòng hiện tại để làm đích dự báo."),
              ("pd.merge_asof", "pandas", "Ghép mỗi dòng với dòng gần nhất của bảng kia, không cần trùng mốc."),
              ("mae", "tự viết", "Hồi quy tuyến tính học 70% đầu, trả MAE trên 30% cuối.")],
         ket_qua="Nhiệt độ thật hứa giảm 3,85% sai số. Học bằng thật, chạy bằng dự báo trước 3 ngày thì sai số tăng 2,20%, tệ hơn không dùng nhiệt độ.",
         hinh=(13, "kn-merge-asof"),
         nguon="rút gọn từ buoi-13/tu-hoc.ipynb, phần 6"),

    # ------------------------------------------------------------------ buổi 14
    dict(ma="code-b14-baseline", buoi=14, sec="4.1",
         tieu="Code: bốn baseline",
         muc="Bốn câu đoán đơn giản nhất về tương lai; mọi mô hình phải thắng cả bốn.",
         code='''import numpy as np

def bl_trung_binh(y, tam=14):
    return np.repeat(float(np.mean(y)), tam)       # mức trung bình

def bl_naive(y, tam=14):
    return np.repeat(float(y[-1]), tam)            # giá trị cuối

def bl_naive_mua_vu(y, tam=14, m=7):
    mua = y[-m:]                                   # vòng mùa vụ vừa qua
    return np.array([mua[i % m] for i in range(tam)], dtype=float)

def bl_drift(y, tam=14):
    doc = (y[-1] - y[0]) / (len(y) - 1)            # độ dốc đầu tới cuối
    return y[-1] + doc * np.arange(1, tam + 1)''',
         buoc=[("3–4", "Lặp mức trung bình cả lịch sử 14 lần."),
               ("6–7", "Lặp giá trị cuối cùng 14 lần."),
               ("9–11", "Lặp lại tuần vừa qua, m = 7 ngày."),
               ("13–15", "Kéo dài đường thẳng nối điểm đầu và cuối.")],
         ham=[("np.repeat", "numpy", "Lặp một con số thành mảng dài tam phần tử."),
              ("y[-m:]", "numpy", "Lấy m giá trị cuối của mảng: một vòng mùa vụ."),
              ("np.arange(1, tam + 1)", "numpy", "Dãy 1, 2, …, tam: số bước đi tiếp theo đường thẳng.")],
         ket_qua="MASE trung vị trên 1.000 chuỗi M4 theo ngày: trung bình 8,85; naive 0,835; seasonal naive 1,077; drift 0,810.",
         hinh=(14, "bon-baseline"),
         nguon="rút gọn từ buoi-14/dap-an/danh_gia.py"),

    dict(ma="code-b14-phan-du", buoi=14, sec="4.2",
         tieu="Code: chẩn đoán phần dư",
         muc="Kiểm xem phần dư còn quy luật không, để biết mô hình tốt hơn có chỗ để thắng.",
         code='''import numpy as np
from scipy import stats

def phan_du_mua_vu(y, m=7):
    return y[m:] - y[:-m]                          # thực tế trừ khớp

def ljung_box(e, so_tre=14):
    x = e - np.mean(e)
    r = np.array([np.dot(x[k:], x[:-k]) / np.dot(x, x)
                  for k in range(1, so_tre + 1)])   # ACF trễ 1 tới 14
    n = e.size
    q = n * (n + 2) * np.sum(r ** 2 / (n - np.arange(1, so_tre + 1)))
    return stats.chi2.sf(q, so_tre)                # p nhỏ: còn quy luật

e = phan_du_mua_vu(y)
p_jb = stats.jarque_bera(e).pvalue                 # có hình chuông không''',
         buoc=[("4–5", "Phần dư seasonal naive: y_t trừ y_(t−7)."),
               ("8–10", "Tự tương quan của phần dư ở 14 trễ."),
               ("11–12", "Gộp 14 trễ thành một con số Q."),
               ("13", "Đổi Q thành p: nhỏ là còn quy luật."),
               ("16", "Kiểm phần dư có gần hình chuông không.")],
         ham=[("np.dot", "numpy", "Nhân từng cặp rồi cộng lại: tử số và mẫu số của ACF."),
              ("stats.chi2.sf", "scipy", "Xác suất gặp Q lớn cỡ này nếu phần dư chỉ là nhiễu: chính là p."),
              ("stats.jarque_bera", "scipy", "Kiểm định phân phối có gần hình chuông; p nhỏ là không.")],
         ket_qua="Trên 1.000 chuỗi M4: 99,8% còn tự tương quan (Ljung–Box p < 0,05), 92,5% không hình chuông, 46,4% phương sai đổi hơn 2 lần.",
         hinh=(14, "chan-doan-phan-du"),
         nguon="rút gọn từ buoi-14/dap-an/danh_gia.py"),

    dict(ma="code-b14-mae-rmse", buoi=14, sec="4.3",
         tieu="Code: MAE, RMSE, ME",
         muc="Viết ba chỉ số rồi thấy mỗi chỉ số ưa một con số dự báo khác nhau.",
         code='''import numpy as np

def mae(y, d):
    return float(np.mean(np.abs(y - d)))           # ưa trung vị
def rmse(y, d):
    return float(np.sqrt(np.mean((y - d) ** 2)))   # ưa trung bình
def me(y, d):
    return float(np.mean(y - d))                   # dương: dự báo thấp

that = np.array([10, 12, 8, 14, 16.0])
du_bao = np.array([11, 10, 9, 14, 12.0])
mau = np.random.default_rng(0).lognormal(3.0, 0.9, 20000)  # lệch phải
luoi = np.linspace(mau.min(), np.quantile(mau, 0.999), 2000)
mae_theo = [np.mean(np.abs(mau - c)) for c in luoi]
rmse_theo = [np.sqrt(np.mean((mau - c) ** 2)) for c in luoi]
c_mae, c_rmse = luoi[np.argmin(mae_theo)], luoi[np.argmin(rmse_theo)]''',
         buoc=[("3–8", "Ba chỉ số, sai số là thực tế trừ dự báo."),
               ("10–11", "Bảng năm ngày để tính tay đối chiếu."),
               ("12", "20.000 số lệch phải như doanh số, seed 0."),
               ("13–15", "Thử 2.000 hằng số c, tính MAE và RMSE."),
               ("16", "Tìm c cho mỗi chỉ số thấp nhất.")],
         ham=[("np.random.default_rng(0).lognormal", "numpy", "Sinh số ngẫu nhiên lệch phải, có seed để chạy lại ra y hệt."),
              ("np.linspace", "numpy", "Chia một khoảng thành 2.000 điểm cách đều để thử lần lượt."),
              ("np.argmin", "numpy", "Vị trí phần tử nhỏ nhất: hằng số c cho chỉ số thấp nhất.")],
         ket_qua="Năm ngày: MAE 1,6; RMSE 2,10; ME 0,8. Trên số lệch phải, MAE đáy ở 20,0 (trung vị), RMSE đáy ở 30,1 (trung bình).",
         hinh=(14, "chi-so-quyet-dinh"),
         nguon="rút gọn từ buoi-14/dap-an/danh_gia.py"),

    dict(ma="code-b14-phan-tram", buoi=14, sec="4.4",
         tieu="Code: MAPE, sMAPE, WAPE",
         muc="Ba chỉ số phần trăm và cách mỗi cái xử lý ngày có thực tế bằng 0.",
         code='''import numpy as np

def mape(y, d):                                    # vô hạn khi có y = 0
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.abs((y - d) / y)
    return float(np.mean(v) * 100)

def smape(y, d):                                   # thang 0–200 kiểu M4
    mau = np.abs(y) + np.abs(d)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.where(mau == 0, 0.0, 2 * np.abs(y - d) / mau)
    return float(np.mean(v) * 100)

def wape(y, d):                                    # tổng chia tổng
    tong = float(np.sum(np.abs(y)))
    return float(np.sum(np.abs(y - d)) / tong * 100) if tong else np.nan''',
         buoc=[("3–6", "Chia từng sai số cho từng thực tế."),
               ("5", "Có y = 0 thì ra vô hạn, không giấu đi."),
               ("8–12", "Chia cho tổng thực tế và dự báo, nhân 200."),
               ("14–16", "Tổng sai số chia tổng thực tế.")],
         ham=[("np.errstate", "numpy", "Tắt cảnh báo chia cho 0 trong khối with để tự xử lý kết quả."),
              ("np.where", "numpy", "Chọn từng ô: mẫu bằng 0 thì lấy 0, còn lại lấy phép chia."),
              ("np.sum(np.abs(...))", "numpy", "Cộng độ lớn sai số của mọi ngày thành một tổng.")],
         ket_qua="Bảng năm ngày: MAPE 12,8%, sMAPE 13,6, WAPE 13,3%. Thêm một ngày thực tế 0 thì MAPE thành vô hạn; trên 300 mã bán lẻ MAPE không tính được.",
         hinh=(14, "chi-so-quyet-dinh"),
         nguon="rút gọn từ buoi-14/dap-an/danh_gia.py"),

    dict(ma="code-b14-mase", buoi=14, sec="4.5",
         tieu="Code: MASE, RMSSE",
         muc="Chia sai số cho mức sai quen thuộc của baseline để so được giữa các chuỗi.",
         code='''import numpy as np

def _mau_so_scaled(hoc, m, binh_phuong=False):
    lech = hoc[m:] - hoc[:-m]              # seasonal naive TRÊN PHẦN HỌC
    if binh_phuong:
        return float(np.mean(lech ** 2))
    return float(np.mean(np.abs(lech)))

def mase(y, d, hoc, m=7):
    mau = _mau_so_scaled(hoc, m)
    return float("nan") if not mau else mae(y, d) / mau   # 0 thì NaN

def rmsse(y, d, hoc, m=7):
    mau = _mau_so_scaled(hoc, m, binh_phuong=True)
    return float("nan") if not mau else rmse(y, d) / np.sqrt(mau)''',
         buoc=[("4", "Sai số seasonal naive, chỉ trên phần học."),
               ("5–7", "Trung bình bình phương hoặc trị tuyệt đối."),
               ("9–11", "MAE kỳ chấm chia mẫu số của phần học."),
               ("11", "Mẫu số bằng 0 thì trả NaN, không trả 0."),
               ("13–15", "RMSSE làm y hệt với bình phương.")],
         ham=[("hoc[m:] - hoc[:-m]", "numpy", "Trừ mỗi điểm cho điểm cách m bước trước: sai số seasonal naive."),
              ("np.sqrt", "numpy", "Căn bậc hai, đưa mẫu số bình phương về cùng đơn vị với RMSE."),
              ("mase, rmsse", "tự viết", "Chia MAE hoặc RMSE cho sai số seasonal naive trên phần học.")],
         ket_qua="Ví dụ tay: MASE 1,6 / 1,5 ≈ 1,07, RMSSE ≈ 1,33. Lấy mẫu số trên đoạn chấm (code đầu buổi) thì MASE của naive trên M4 ra 0,972 thay vì 0,835.",
         hinh=None,
         nguon="rút gọn từ buoi-14/dap-an/danh_gia.py"),

    dict(ma="code-b14-doi-hang", buoi=14, sec="4.6",
         tieu="Code: gộp, xếp hạng, đối chiếu",
         muc="Gộp chỉ số qua nhiều chuỗi mà không giấu ô vô hạn, rồi soát thang của thư viện.",
         code='''import numpy as np
from utilsforecast.losses import smape as uf_smape
arr = np.array(v, dtype=float)                    # một số mỗi chuỗi
huu_han = arr[np.isfinite(arr)]                   # bỏ ô vô hạn, NaN...
so_vo_han = int(np.sum(~np.isfinite(arr)))        # ...nhưng đếm, báo ra
trung_vi, trung_binh = np.median(huu_han), np.mean(huu_han)

def xep_hang(bang, cac_cot):
    ra = bang[["mô hình"]].copy()
    for cot in cac_cot:                           # ME xếp theo trị tuyệt đối
        v = bang[cot].abs() if cot == "ME" else bang[cot]
        ra[cot] = v.rank(method="min").astype("Int64")
    return ra

tl = uf_smape(dai_kiem, models=["du_bao"])["du_bao"].mean()   # tỷ lệ 0–1
smape_m4 = tl * 200                               # về thang 0–200 của M4''',
         buoc=[("3–5", "Bỏ ô không tính được nhưng đếm để báo."),
               ("6", "Gộp bằng trung vị và cả trung bình."),
               ("8–12", "Xếp hạng mô hình theo từng chỉ số."),
               ("15–16", "Thư viện trả tỷ lệ, nhân 200 mới ra M4.")],
         ham=[("np.isfinite", "numpy", "Đánh dấu ô là số bình thường, loại vô hạn và NaN."),
              ("rank(method=\"min\")", "pandas", "Đổi giá trị thành thứ hạng, 1 là nhỏ nhất; bằng nhau cùng hạng."),
              ("utilsforecast.losses.smape", "utilsforecast", "Tính sMAPE trên bảng dạng dài; trả tỷ lệ 0–1, không phải phần trăm.")],
         ket_qua="Bán lẻ 300 mã: hạng nhất đổi theo chỉ số (naive theo MAE, seasonal naive theo sMAPE). sMAPE tự viết 3,59, utilsforecast 0,0179: lệch 200 lần.",
         hinh=(14, "doi-chi-so-doi-hang"),
         nguon="rút gọn từ buoi-14/dap-an/danh_gia.py"),

    # ------------------------------------------------------------------ buổi 15
    dict(ma="code-b15-kfold", buoi=15, sec="4.1",
         tieu="Code: K-fold xáo trộn so với hold-out",
         muc="Đo bằng số xem chia ngẫu nhiên hứa sai số thấp hơn thật bao nhiêu.",
         code='''import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

moc = pd.Timestamp("2024-10-01")                  # hold-out: 3 tháng cuối
bang = bang_feature(y).assign(y=y).dropna()       # lag ≥ 24 giờ + lịch
hoc, kiem = bang[bang.index < moc], bang[bang.index >= moc]
X, t = hoc.drop(columns="y"), hoc["y"]
loi = []
for a, b in KFold(5, shuffle=True, random_state=0).split(X):  # XÁO TRỘN
    mo_hinh = tao_rung().fit(X.iloc[a], t.iloc[a])
    loi.append(_mae(mo_hinh.predict(X.iloc[b]), t.iloc[b]))
mae_kfold = float(np.mean(loi))
mo_hinh = tao_rung().fit(X, t)                    # học một lần trên quá khứ
mae_that = _mae(mo_hinh.predict(kiem.drop(columns="y")), kiem["y"])''',
         buoc=[("5", "Để riêng 3 tháng cuối năm 2024 làm hold-out."),
               ("6–8", "Feature lag ≥ 24 giờ, chỉ phần trước mốc."),
               ("10–13", "K-fold xáo trộn: điểm kiểm xen giữa điểm học."),
               ("14–15", "Học trên quá khứ, chấm trên 3 tháng sau.")],
         ham=[("KFold(5, shuffle=True)", "sklearn", "Xáo trộn rồi chia 5 phần, lần lượt lấy một phần làm kiểm."),
              ("tao_rung().fit / predict", "sklearn", "Rừng ngẫu nhiên 200 cây: học trên phần học, rồi dự báo."),
              ("_mae", "tự viết", "Trung bình độ lớn sai số giữa dự báo và thực tế, đơn vị MW.")],
         ket_qua="Rừng ngẫu nhiên: K-fold hứa 1.639 MW, hold-out thật 2.129 MW, lệch −23,0%. Hồi quy tuyến tính lệch −11,8%.",
         hinh=(15, "ba-cach-chia"),
         nguon="rút gọn từ buoi-15/dap-an/backtest.py"),

    dict(ma="code-b15-rolling-origin", buoi=15, sec="4.2",
         tieu="Code: bộ backtest rolling origin",
         muc="Tự viết bộ backtest: nhiều cutoff, mỗi lần chỉ học trên quá khứ rồi dự báo.",
         code='''import numpy as np
import pandas as pd
def chia_cua_so(df, h, so_cua_so, buoc=None, gap=0):
    buoc = h if buoc is None else buoc
    truc = np.sort(df["ds"].unique())
    cuoi = len(truc) - 1 - gap - h              # cutoff cửa sổ cuối
    return [(truc[c], truc[c + gap + 1], truc[c + gap + h])
            for c in range(cuoi - buoc * (so_cua_so - 1), cuoi + 1, buoc)]
def backtest(df, ham_du_bao, h, so_cua_so, buoc=None, gap=0):
    ket_qua = []
    for cutoff, bd, kt in chia_cua_so(df, h, so_cua_so, buoc, gap):
        lich_su = df[df["ds"] <= cutoff]        # KHÔNG thấy đoạn kiểm
        test = df[(df["ds"] >= bd) & (df["ds"] <= kt)]
        du_bao = ham_du_bao(lich_su.copy(), test[["unique_id", "ds"]])
        ket_qua.append(test.merge(du_bao, on=["unique_id", "ds"]))
    return pd.concat(ket_qua)''',
         buoc=[("6", "Cửa sổ cuối kết thúc đúng ở mốc cuối."),
               ("7–8", "Lùi đều từng buoc; gap bỏ trống sau cutoff."),
               ("12", "Hàm dự báo chỉ nhận dòng tới cutoff."),
               ("13–14", "Dự báo đúng các mốc của đoạn kiểm."),
               ("15", "Ghép dự báo với thực tế để chấm.")],
         ham=[("np.sort(df[\"ds\"].unique())", "numpy, pandas", "Lấy các mốc thời gian khác nhau, xếp tăng dần làm trục."),
              ("merge", "pandas", "Ghép dự báo với thực tế theo cặp mã chuỗi và mốc thời gian."),
              ("cross_validation", "statsforecast", "Bản thư viện làm cùng việc nhưng không có gap.")],
         ket_qua="Tải ERCOT, 28 cửa sổ 24 giờ: rừng ngẫu nhiên 1.944 MW so với hold-out 2.129 MW (−8,7%). Seasonal naive khớp statsforecast, chênh 0,0.",
         hinh=(15, "uoc-luong-sai-so"),
         nguon="rút gọn từ buoi-15/dap-an/backtest.py"),

    dict(ma="code-b15-theo-cua-so", buoi=15, sec="4.3",
         tieu="Code: sai số theo cửa sổ và theo h",
         muc="Tách một MAE gộp ra từng cửa sổ và từng bước h để thấy nó dao động cỡ nào.",
         code='''import numpy as np
import pandas as pd

def _mae(a, b):
    return float(np.mean(np.abs(np.asarray(a, float) - np.asarray(b, float))))

kq = backtest(dang_dai(y[y.index < moc]), ca_hai, h=24, so_cua_so=28,
              buoc=24)                            # rừng và seasonal naive
theo_cua_so = kq.groupby("cutoff").apply(lambda g: pd.Series({
    "rừng": _mae(g["y"], g["du_bao"]),
    "seasonal naive": _mae(g["y"], g["seasonal_naive"])}))
dao_dong = theo_cua_so.describe()                 # nhỏ nhất tới lớn nhất

def sai_so_theo_h(kq, cot):
    return (kq["y"] - kq[cot]).abs().groupby(kq["buoc_h"]).mean()''',
         buoc=[("7–8", "28 ngày, hai mô hình trên cùng cửa sổ."),
               ("9–11", "Một MAE cho mỗi cửa sổ, mỗi mô hình."),
               ("12", "Tóm độ dao động giữa các cửa sổ."),
               ("14–15", "MAE theo từng bước sau cutoff.")],
         ham=[("groupby(\"cutoff\").apply", "pandas", "Chia kết quả theo từng cửa sổ rồi tính MAE riêng mỗi nhóm."),
              ("describe", "pandas", "Tóm tắt nhanh: số lượng, trung bình, nhỏ nhất, phân vị, lớn nhất."),
              ("groupby(kq[\"buoc_h\"]).mean()", "pandas", "Trung bình sai số theo bước thứ mấy sau cutoff.")],
         ket_qua="MAE một ngày của rừng ngẫu nhiên đi từ 583 tới 4.328 MW, gấp bảy lần. Trên M4, seasonal naive 24 giờ nhảy lên từ bước 25.",
         hinh=(15, "sai-so-cua-so-va-h"),
         nguon="rút gọn từ buoi-15/dap-an/backtest.py"),

    dict(ma="code-b15-ba-tap", buoi=15, sec="4.4",
         tieu="Code: tune, chọn, báo cáo ba đoạn",
         muc="Tách ba đoạn riêng để con số báo cáo không được hưởng phần may lúc chọn.",
         code='''import numpy as np
import pandas as pd
LUOI_W = np.round(np.arange(0, 1.01, 0.1), 1)      # 11 giá trị w

def chon_va_bao_cao(chuoi, h=48):
    hang = []
    for ten, v in chuoi.items():
        n = len(v)
        T, A, B = n - 3 * h, n - 2 * h, n - h        # ba đoạn 48 giờ cuối
        w = min(LUOI_W, key=lambda x: _cham(v, T, x, h)["trộn"])  # tune
        diem_A = _cham(v, A, w, h)
        chon = min(diem_A, key=diem_A.get)           # chọn trên A
        diem_B = _cham(v, B, w, h)                   # báo cáo trên B
        hang.append({"chuỗi": ten, "chọn": chon,
                     "MASE báo cáo (B)": diem_B[chon]})
    return pd.DataFrame(hang)''',
         buoc=[("3", "Lưới trọng số w từ 0 tới 1, bước 0,1."),
               ("9", "Chia ba đoạn: T tune, A chọn, B báo cáo."),
               ("10", "Chọn w cho MASE thấp nhất trên đoạn T."),
               ("11–12", "Chọn phương pháp tốt nhất trên đoạn A."),
               ("13–15", "Chỉ báo MASE trên đoạn B chưa dùng.")],
         ham=[("np.arange, np.round", "numpy", "Tạo lưới 0; 0,1; …; 1 và làm tròn cho khỏi sai số lẻ."),
              ("_cham", "tự viết", "MASE của sáu phương pháp đơn giản trên một đoạn 48 giờ."),
              ("pd.DataFrame", "pandas", "Gom kết quả mỗi chuỗi thành một bảng để lấy trung vị.")],
         ket_qua="414 chuỗi M4 theo giờ: tune, chọn, báo cáo cùng đoạn B cho MASE trung vị 0,775; ba đoạn riêng cho 1,039, lạc quan 25%.",
         hinh=(15, "chon-bao-cao"),
         nguon="rút gọn từ buoi-15/dap-an/backtest.py"),

    dict(ma="code-b15-dm", buoi=15, sec="4.5",
         tieu="Code: kiểm định Diebold–Mariano",
         muc="Hỏi chênh sai số giữa hai dự báo là thật hay chỉ là may trên đoạn này.",
         code='''import numpy as np
from scipy import stats

def diebold_mariano(e1, e2, h=1, hieu_chinh=True):
    d = np.abs(e1) - np.abs(e2)                    # chênh mất mát từng giờ
    n = len(d)
    lech = d - d.mean()
    gamma = [np.sum(lech[k:] * lech[: n - k]) / n for k in range(h)]
    v = (gamma[0] + 2 * sum(gamma[1:])) / n        # cộng tự hiệp phương sai
    if v <= 0:                                     # lùi về h = 1
        h, v = 1, gamma[0] / n
    s = d.mean() / np.sqrt(v)
    if not hieu_chinh:
        return s, 2 * stats.norm.sf(abs(s))        # bản bỏ tự tương quan
    s *= np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)   # sửa mẫu nhỏ
    return s, 2 * stats.t(df=n - 1).sf(abs(s))''',
         buoc=[("5", "Chênh độ lớn sai số của hai dự báo."),
               ("8–9", "Cộng tự hiệp phương sai tới trễ h − 1."),
               ("12", "Chênh trung bình chia sai số chuẩn."),
               ("13–14", "Bản ngây thơ: so với hình chuông chuẩn."),
               ("15–16", "Bản HLN: hệ số mẫu nhỏ, phân phối t.")],
         ham=[("np.sum(lech[k:] * lech[: n - k])", "numpy", "Tự hiệp phương sai trễ k: d_t và d_(t+k) cùng lên xuống cỡ nào."),
              ("stats.t(df=n - 1).sf", "scipy", "Xác suất đuôi phân phối t; nhân 2 được p hai phía."),
              ("stats.norm.sf", "scipy", "Xác suất đuôi của hình chuông chuẩn, dùng cho bản bỏ tự tương quan.")],
         ket_qua="Trộn so với seasonal naive trên 2.215 giờ: bỏ tự tương quan ra p = 0,0000012; bản HLN h = 24 ra −1,41, p = 0,16: chưa có bằng chứng.",
         hinh=(15, "dm-tu-tuong-quan"),
         nguon="rút gọn từ buoi-15/dap-an/backtest.py"),
]
