# Phase 20 — Buổi 20–21 · Đa biến & nowcasting, tài chính ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 20". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 20 Đa biến & nowcasting | ✅ | ✅ 3.901 chữ | ✅ mới | ✅ 6/6, đỏ 3 | ✅ | ✅ 0/0 | ✅ 12 tr |
| 21 Tài chính & biến động | ✅ | ✅ 3.595 chữ | ✅ mới | ✅ 7/7, đỏ 3 | ✅ | ✅ 0/0 | ✅ 12 tr |

Bắt buộc:
- Buổi 20: tự viết Kalman filter; nowcast GDP **bằng vintage thật** (Philadelphia Fed Real-Time Data Set — không dùng ALFRED, xem Phụ lục F)
- Buổi 21: mổ xẻ demo "LSTM đoán giá 99%"; GARCH + HAR; VaR backtest Kupiec. **Cột mốc M2**
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

## Kết quả (2026-09-19)

- **Dữ liệu mới**: 4 tệp vintage THEO THÁNG của Philadelphia Fed (GDP, việc làm, sản lượng CN, nhà khởi công — không dùng FRED/ALFRED), giá xăng NY
  Harbor (EIA), 24 tệp BTC/USDT 1 giờ 2023–2024 (Binance, sha256 khớp `.CHECKSUM`). Cơ chế mới **`noi_them`** trong `tools/lay_du_lieu.py` cho tệp
  nguồn bị ghi đè bằng bản nối thêm mà không mirror được: sha lệch thì cảnh báo, buổi cắt tới mốc cố định (vintage 25M12) và bộ chấm kiểm sha256 phần
  đã cắt. Đã chạy `sinh_nen.py --tat-ca` (uv.lock các buổi cũ không đổi). Thêm `arch` 8.0.0, `xlrd` 2.0.2 vào bảng phiên bản.
- **Buổi 20**: dầu–xăng 2010–2019 đồng liên kết (hệ số 0,845, Johansen hạng 1, bán rã 9,6 tuần); VECM 6,44% so với naive 6,78% ở tầm 4 tuần nhưng DM
  p 0,17. Kalman tự viết khớp statsmodels (lệch 0,024). Nowcast GDP 2005–2019 bằng vintage thật: bridge 1,44 → 1,17 (thắng naive, trung bình); DFM
  1,86 → 1,50; **2010–2019 êm thì trung bình lịch sử thắng** (1,03) — báo trung thực; số đã sửa cho "tháng đầu" 1,19 thay vì 1,44.
- **Buổi 21**: demo MLP "R² 0,988" thua naive (MAE 1.649 so với 887); chấm trung thực thua có ý nghĩa (DM p 5·10⁻¹⁰), đúng chiều 52,5%. VaR 99% JPY
  2020–2024: chuẩn cố định 25 lần vượt (Kupiec p 0,002), GARCH-t 14 lần (p 0,67). BTC 2024: HAR QLIKE 0,389 < GARCH-t 0,477 < cố định 0,530 (MSE thì
  GARCH thua cố định — báo cả hai). **Cột mốc M2**: bài tập 3 (bậc thang mô hình) + bảng tự đánh giá ở mục 8 buổi 21.
- Lệch lộ trình (nhỏ, ghi NGHIEN-CUU): DFM chỉ 3 chỉ báo có vintage (không "vài chục chuỗi"); MLP thay LSTM (không cần torch); BTC + JPY thay cổ phiếu;
  Markov switching vào hộp "Nâng cao".
- Phụ lục E thêm 9 thuật ngữ; Phụ lục F sinh lại. `ruff` sạch; `kiem_de_hieu.py 20 21` 0; `kiem_tra_lab.py 20 21` đạt; `kiem_tra_doc_lap.sh` đạt
  (21 buổi); PDF 12 + 12 trang.
