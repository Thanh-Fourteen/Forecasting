# phase 28

_2026-09-25 16:46:55_

Phase 28 đã xong và đã đánh dấu ✅ ở `todos.md`, `todos/phase-28.md` và `todos/tong-quan.md`. `ruff` sạch, `kiem_tra_doc_lap.sh` xanh (28 buổi). Tôi chưa commit.

**Việc đã làm:** research xong cụm deep learning (buổi 29–33) trước khi soạn, và đo thời gian + RAM thật trên CPU 4 luồng cho các mô hình dự kiến dùng. Mỗi buổi có một [NGHIEN-CUU.md](buoi-30/NGHIEN-CUU.md) ghi nguồn, phiên bản, revision, dữ liệu và quyết định. Bảng đo của cả cụm nằm trong ghi chú buổi 30.

**Kết quả đo (321 chuỗi, 500 bước)**

| Tình huống | Mô hình |
|---|---|
| Nhanh, dưới 2,5 phút, khoảng 1,3 GB | MLP, N-BEATS, N-HiTS, TiDE, DLinear, TSMixer, TimeMixer |
| Nặng | DeepAR 11 phút, 3 GB; TFT 9,5 phút, 3,2 GB; iTransformer 19 phút, 3 GB |
| Mặc định vượt 6 GB | TFT, TimeXer. TFT chạy được khi đặt `windows_batch_size=256` |
| Không chạy được | xLSTM (cần gói ngoài) |
| Thua seasonal naive ở mốc cắt thử | DeepAR, TFT |
| GNN tự viết trên Traffic 862 cảm biến | 43 giây, 0,5 GB, nhưng **thua** MLP từng cảm biến |
| Khuếch tán thu nhỏ kiểu CSDI | khoảng 3 phút, 1,1 GB; chạy được trên CPU nhưng **chưa thắng** cách giữ giá trị cuối |

**Điểm lệch lộ trình (đã sửa [lộ trình](lo-trinh/lo-trinh-forecasting.md) và kế hoạch phase 30–31)**

1. **Buổi 32:** DeepAR của neuralforecast đưa giá trị trung bình trở lại làm đầu vào, nên không sinh quỹ đạo thật. Lab 1 đổi sang `nf.simulate()` (ghép quantile bằng copula) cộng một LSTM nhỏ tự viết. Tiêu chí "Xong khi" đổi sang variogram score cộng CRPS của tổng 14 ngày, vì energy score chỉ chênh 3,7% so với variogram score 62,5%. **Tôi đã áp dụng phương án đề xuất; bạn muốn khác thì báo tôi.**
2. **Buổi 33:**
   - GNN tự viết bằng PyTorch, vì PyTorch Geometric Temporal không cài được với torch 2.14.
   - Bảng kiểm chứng AIFS đổi từ tầm 1–10 ngày thành 1–7 ngày.
   - AIFS lên v2 từ 12/05/2026, nhưng dữ liệu từ 2025 vẫn nằm sau mốc huấn luyện.
   - WeatherBench 2 chấm trên năm 2022, năm nằm trong dữ liệu huấn luyện. Đây là ví dụ thật cho chỗ hở cố ý của buổi.
3. **Buổi 30–31:** giữ nguyên kiến trúc, vì 12 tháng qua không có mô hình nào thắng bền. Đã xác nhận trong mã gốc: repo PatchTST và iTransformer đặt `drop_last=True` cho tập test, còn repo DLinear thì không. Nghĩa là bảng kết quả gốc không chấm các mô hình trên cùng một tập test.

**Thay đổi ngoài kế hoạch:**
- `kiem_tra_doc_lap.sh` và `dong_goi.py --tat-ca` giờ bỏ qua thư mục buổi chỉ có `NGHIEN-CUU.md`.
- Việc cần làm ở Phase 31: thêm AIFS theo điểm vào danh mục dữ liệu, và chụp + mirror GHCNh 2026 (tệp này đổi hằng ngày).

**Về vụ sập máy:** lỗi do tôi chạy một mô phỏng cần khoảng 125 GB RAM mà không ước lượng trước. Sau đó mọi phép đo đều chạy dưới trần RAM cứng, nên TFT và TimeXer chỉ bị dừng riêng chứ không làm treo máy. Tôi đã lưu bài học này vào bộ nhớ.
