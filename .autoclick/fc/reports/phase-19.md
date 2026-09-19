# phase 19

_2026-09-19 08:51:11_

Phase 19 đã xong: buổi 18 và 19 được soạn mới hoàn toàn và đánh dấu ✅ trong `todos.md`, `todos/phase-19.md`, `todos/tong-quan.md`. Có một điểm lệch lộ trình cần anh/chị biết: ở buổi 18, hồi quy động không thắng được seasonal naive trên dữ liệu thật.

| Buổi | Chữ | PDF | Lab | Tự đọc thử | Quiz |
|---|---|---|---|---|---|
| 18 Hồi quy động | 4.136 | 13 trang | đáp án xanh 5/5, `code/` đỏ đúng 2 chỗ hở | 0 chặn / 0 khó (vòng 2) | 10/10 có căn cứ |
| 19 Nhu cầu gián đoạn | 3.679 | 12 trang | đáp án xanh 8/8, `code/` đỏ đúng 4 test | 0 chặn / 0 khó (vòng 2) | 10/10 có căn cứ |

Các kiểm tra khác đều qua: `ruff`, `kiem_de_hieu.py` (0 vi phạm), `kiem_tra_lab.py 18 19`, `kiem_tra_doc_lap.sh` (cả 19 buổi), `sinh_nen.py --kiem --tat-ca`.

**Research:**
- **Prophet vẫn được bảo trì**: bản 1.4.0 ra ngày 15/8/2026 và hỗ trợ pandas 3. Tôi đã thêm nó vào `tools/nen/phien-ban.toml`.
- **Ngưỡng Syntetos–Boylan** (ADI 1,32, CV² 0,49) chỉ được tính ra để chọn giữa Croston và SBA. Buổi 19 dạy nó như cách mô tả dữ liệu, còn chọn mô hình thì bằng backtest.

**Buổi 18:**
- **Hồi quy giả**: hành khách hàng không EU "phụ thuộc" sản lượng công nghiệp Mỹ với p = 3·10⁻¹⁶. Thêm biến xu hướng thì hệ số đổi dấu mà vẫn "có ý nghĩa". Chuyển sang hồi quy động thì p = 0,59 và phần dư trắng.
- **Tải điện ERCOT, 24 cửa sổ backtest**: hồi quy động có sai số trung bình 2.082 MW, MSTL 2.104, seasonal naive 2.173, Prophet 2.998.
- **Kiểm định DM**: hồi quy động ngang seasonal naive (p = 0,76), chỉ thắng Prophet (p = 0,017) và hồi quy thường (p = 0,010). Phần dư theo giờ chưa trắng.
- **Lệch lộ trình**: tiêu chí "Xong khi" đòi hồi quy động có phần dư trắng và thắng seasonal naive, điều này không đạt trên dữ liệu thật. Tài liệu báo đúng như vậy, và tôi đã sửa "Xong khi" trong `lo-trinh`. Nếu anh/chị muốn thử thêm cách làm hồi quy động mạnh hơn, đó là việc riêng.
- **Prophet và Tết**: khai Tết (cửa sổ ±7 ngày) làm sai số quanh Tết 2024 giảm khoảng ba lần, nhưng tính cả năm Prophet vẫn thua seasonal naive.

**Buổi 19** (chấm cả RMSSE lẫn chi phí tồn kho, như prompt yêu cầu):
- MASE chọn "Zero", tức không bao giờ nhập hàng, dù cách này có chi phí tồn kho cao gấp rưỡi mô hình tốt nhất.
- RMSSE xếp Zero trên AutoETS, nhưng chi phí thì ngược lại. Đây là trường hợp hai thước đo chọn khác nhau mà prompt yêu cầu chỉ ra.
- IMAPA tốt nhất ở cả hai thước đo.
- Croston thua cả trung bình lịch sử vì nhiều mã phụ tùng ngừng bán giữa chừng; TSB xử lý được trường hợp này.

**Lỗi tôi tự bắt và đã sửa:**
- **Buổi 18**: cutoff cách nhau 14 ngày nên mọi cửa sổ rơi cùng một thứ trong tuần (bẫy của buổi 15). Riêng việc đổi thứ của cutoff làm sai số seasonal naive nhảy từ 1.996 lên 3.163 MW. Tôi đổi bước thành 13 ngày.
- **Buổi 18**: cửa sổ cuối vượt quá dữ liệu nhiệt độ, 7 giờ thiếu số liệu bị bỏ qua âm thầm khi tính sai số. Tôi cắt đoạn chấm cho khớp.
- **Buổi 19**: lúc tự đọc thử phát hiện mô phỏng tồn kho cho hàng về ngay đầu tháng sau, tức thời gian dẫn thực chất bằng 0, mâu thuẫn với tài liệu. Tôi sửa code rồi chạy lại mọi chi phí; thứ hạng các mô hình không đổi.

**Lệch nhỏ khác:**
- Buổi 19 dùng thời gian dẫn 1 tháng thay vì 2 tuần như lộ trình, vì dữ liệu Car Parts theo tháng.
- Chỗ hở cố ý được cập nhật trong `quy-uoc.md`.
- Phụ lục E thêm 11 thuật ngữ; Phụ lục F sinh lại.

Tôi chưa commit. Phase tiếp theo là 20 (buổi 20–21).
