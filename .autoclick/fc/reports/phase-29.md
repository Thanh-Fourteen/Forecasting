# phase 29

_2026-09-25 22:12:00_

Phase 29 đã xong: buổi 29 (nền deep learning) và buổi 30 (N-BEATS … TiDE) đã soạn đủ, và mọi bước kiểm của phase đều qua. Tôi chưa commit.

**Kết quả kiểm**

| | Buổi 29 | Buổi 30 |
|---|---|---|
| Lab trên máy trắng (tải lại mọi thứ) | đạt, 14 phút | đạt, 7,7 phút |
| Bộ chấm: `code/` đỏ đúng chỗ hở / đáp án | đỏ 2/6 / xanh 6/6 | đỏ 2/5 / xanh 5/5 |
| Bộ kiểm dễ hiểu | 0 vi phạm | 0 vi phạm |
| Tự đọc thử | 0 chặn, 5 khó đã sửa, quiz mù 10/10 | 0 chặn, 5 khó đã sửa, quiz mù 10/10 |
| Độ dài | khoảng 5.000 chữ, PDF 14 trang | khoảng 4.300 chữ, PDF 12 trang |

Kiểm tính tự chứa đạt cả 30 buổi, lint sạch.

**Kết quả chính, đều từ lần chạy thật**
- **Buổi 29 (3 mạng tự viết, 50 khách hàng):** mạng thua. MSTL có MASE 0,883, LightGBM 0,896, mạng tốt nhất (MLP + RevIN) 0,957. Bài dạy đúng như vậy.
- **Buổi 30 (5 vùng điện Mỹ):** ngược lại, N-HiTS (0,378) và N-BEATS (0,402) thắng MSTL (0,428), LightGBM và cả dự báo chính thức của vùng điều độ (0,574). Mỗi mô hình chỉ huấn luyện vài chục giây.

**Bốn điểm lệch so với lộ trình.** Lộ trình đã sửa theo cả bốn; tôi báo để bạn biết:
1. **Rò rỉ cửa sổ chồng lấn không phải lúc nào cũng lộ ra thành số.** Với 50 khách hàng, cắt cửa sổ rồi chia ngẫu nhiên gần như không làm đẹp số val, vì mạng không học thuộc nổi hơn nửa triệu mẫu. Với tập nhỏ 5 khách thì val báo MASE 0,98 (ngang naive), trong khi test thật là 1,41. Lab dùng tập nhỏ để học viên thấy rõ tác hại.
2. **Rò rỉ nhiệt độ chỉ làm backtest đẹp giả khoảng 2,5%.** Lý do là dự báo nhiệt độ trước 1 ngày chỉ lệch khoảng 1,3 °C. Bài nói thẳng như vậy; thí nghiệm ở tầm một tuần để làm bài tập.
3. **Lab "DeepAR âm nhị thức cho dữ liệu đếm" chuyển thành bài tập.** Mọi phân phối đếm của DeepAR trong neuralforecast đều cho khoảng 80% chỉ phủ 13–27%. Lab thay bằng kiểm coverage của chính DeepAR trong bảng chính: khoảng 80% phủ 31%, và tụt còn 20–30% từ giờ thứ 8.
4. **Seed chưa đủ để ra cùng số giữa hai lần chạy.** Khi CPU chạy nhiều luồng, các luồng cộng số thực theo thứ tự thay đổi mỗi lần. Thí nghiệm nhạy chạy một luồng thì trùng tuyệt đối; bài giải thích điều này.

**Chi phí CPU (buổi 30).** Cấu hình mặc định quá nặng: TFT mất 17 phút và 4,2 GB RAM. Tôi rút gọn cấu hình: TFT còn 3 phút, 3 GB, máy 8 GB chạy được.

**Thay đổi ngoài hai buổi**
- Phụ lục E thêm 18 thuật ngữ.
- `kiem_tra_doc_lap.sh` và `dong_goi.py` giờ bỏ qua thư mục buổi mới research xong, chưa soạn.
- Lộ trình và Phụ lục E đã xuất lại PDF.
- `todos.md`, `todos/phase-29.md` và `todos/tong-quan.md` đã đánh ✅.

Bài học rút ra cho các phase sau: số đo thật hay khác với kỳ vọng của lộ trình (cả bốn điểm lệch ở trên đều vậy). Vì thế tôi đo trước khi viết, và giữ đúng con số đo được thay vì chỉnh bài cho khớp kỳ vọng.
