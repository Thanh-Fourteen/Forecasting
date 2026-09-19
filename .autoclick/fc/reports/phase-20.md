# phase 20

_2026-09-19 10:53:38_

Phase 20 xong: buổi 20 và 21 được soạn mới hoàn toàn và đánh dấu ✅ trong `todos.md`, `todos/phase-20.md`, `todos/tong-quan.md`. Cột mốc M2 nằm ở cuối buổi 21 (xem dưới). Tôi chưa commit.

| Buổi | Chữ | PDF | Lab | Tự đọc thử | Quiz |
|---|---|---|---|---|---|
| 20 Đa biến & nowcasting | 3.901 | 12 trang | đáp án xanh 6/6, `code/` đỏ đúng 3 | 0 chặn / 0 khó | 10/10 có căn cứ |
| 21 Tài chính & biến động | 3.595 | 12 trang | đáp án xanh 7/7, `code/` đỏ đúng 3 | 0 chặn / 0 khó | 10/10 có căn cứ |

Các kiểm tra khác đều qua: `ruff`, `kiem_de_hieu.py`, `kiem_tra_lab.py 20 21` (từ venv trắng), `kiem_tra_doc_lap.sh` trên cả 21 buổi. `uv.lock` của các buổi cũ không đổi.

**Dữ liệu và công cụ — có thay đổi ảnh hưởng mọi buổi:**
- **Số liệu vintage:** dùng tệp vintage theo tháng của Philadelphia Fed cho GDP, việc làm, sản lượng công nghiệp và nhà khởi công. Không dùng FRED/ALFRED.
- **Cơ chế mới `noi_them` trong `tools/lay_du_lieu.py`:** tệp của Philadelphia Fed được thêm một cột mỗi tháng và không được phép mirror, nên sha256 sẽ lệch sau này. Khi lệch, `lab.py up` cảnh báo rồi vẫn nhận tệp. Buổi 20 chỉ dùng số liệu tới 12/2025, và bộ chấm kiểm sha256 của phần đã cắt đó. Tôi đã chạy `sinh_nen.py --tat-ca` để chép công cụ mới vào mọi buổi.
- **Bộ dữ liệu mới trong danh mục:** giá xăng New York Harbor (EIA) và 24 tệp BTC/USDT theo giờ 2023–2024 (Binance; sha256 khớp tệp `.CHECKSUM` của Binance; không mirror).
- **Thư viện mới:** `arch` 8.0.0 và `xlrd` 2.0.2 vào bảng phiên bản.

**Buổi 20 — kết quả trung thực:**
- **Dầu – xăng 2010–2019:** hai chuỗi đồng liên kết. VECM nhỉnh hơn naive ở tầm 4 tuần, nhưng kiểm định DM cho p = 0,17, tức chưa có bằng chứng.
- **Kalman tự viết** khớp statsmodels (lệch tối đa 0,024).
- **Nowcast GDP 2005–2019 bằng vintage thật:** sai số (RMSE) giảm từ 1,44 xuống 1,17 điểm % khi có thêm từng tháng số liệu, thắng cả naive lẫn trung bình lịch sử.
- **Một phát hiện đáng dạy:** giai đoạn êm 2010–2019, trung bình lịch sử thắng mọi mô hình (1,03). Nowcast chỉ có giá trị lớn khi kinh tế đổi chiều (2005–2009).
- **Rò rỉ khi dùng số đã sửa:** ngay tháng đầu quý, mô hình "biết" đủ cả quý nên sai số trông như 1,19 thay vì 1,44 thật.

**Buổi 21 — kết quả trung thực:**
- **Demo "đoán giá chính xác 99%":** R² 0,988, nhưng "giá hôm qua" (naive) đạt R² 0,996 trên cùng dữ liệu. Chấm trung thực thì mô hình thua naive có ý nghĩa (DM p = 5·10⁻¹⁰) và chỉ đoán đúng chiều 52,5% số ngày, như tung đồng xu.
- **VaR 99% trên JPY/USD 2020–2024:** VaR chuẩn cố định bị vượt 25 lần (kiểm định Kupiec bác), GARCH-t bị vượt 14 lần, khớp kỳ vọng 12,5.
- **Dự báo biến động BTC 2024:** theo thước đo QLIKE, HAR tốt nhất và GARCH thắng biến động lịch sử cố định. Theo MSE thì GARCH lại thua con số cố định; tài liệu báo cả hai và giải thích vì sao.
- **Cột mốc M2:** bài tập "bậc thang mô hình" ở mục 7 và bảng tự đánh giá năng lực buổi 14–21 ở mục 8.

**Lệch nhỏ so với lộ trình** (đều ghi trong `NGHIEN-CUU.md`):
- Mô hình nhân tố động (DFM) chỉ dùng 3 chỉ báo tháng có vintage, không phải "vài chục chuỗi". Dùng dữ liệu BEA/BLS đã sửa thì lại thành rò rỉ.
- Demo dùng mạng MLP thay cho LSTM (không cần cài torch; hiện tượng giống hệt).
- Dữ liệu tài chính là BTC và JPY/USD thay vì cổ phiếu, vì không có nguồn cổ phiếu có giấy phép mở rõ ràng.
- Markov switching chuyển vào hộp "Nâng cao".

Phụ lục E thêm 9 thuật ngữ, Phụ lục F đã sinh lại. Phase tiếp theo là 21 (đọc thử độc lập buổi 18–21, cần mở phiên mới).
