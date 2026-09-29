# phase 30

_2026-09-28 14:31:05_

Phase 30 đã xong: buổi 4–8 đều có notebook tự học và hình khái niệm. Mọi ô trong bảng `phase-30.md` đều ✅, và phase đã được đánh dấu ✅ ở cả `todos.md` lẫn `todos/phase-30.md`. Tôi chưa commit.

**Kết quả từng buổi**

| Buổi | Notebook | Hình khái niệm (chèn vào tài liệu) | PDF | kiem_de_hieu |
|---|---|---|---|---|
| 4 Biểu đồ | 67 ô, 0 lỗi | 9 (4) | 18 → 19 trang | 0, không đổi |
| 5 Biến đổi | 53 ô, 0 lỗi | 4 (4) | 15 → 16 | 3, đều có từ trước |
| 6 Phân rã | 53 ô, 0 lỗi | 6 (6) | 16 → 17 | 1, có từ trước |
| 7 Tự tương quan | 49 ô, 0 lỗi | 5 (5) | 15 → 16 | 2, có từ trước |
| 8 Tương quan chéo | 52 ô, 0 lỗi | 5 (5) | 15 → 16 | 1, có từ trước |

- **Số liệu:** mọi con số trong phần chữ đều lấy từ output `--chay` và khớp `tai-lieu.md`.
- **Hình:** tôi xem lại từng hình trong notebook và kiểm vài trang PDF, rồi sửa những chỗ chưa ổn: nhãn boxplot chồng nhau, điểm robust vẽ sai vị trí, hai ô cộng/nhân trông giống nhau, chú thích che mất điểm dữ liệu.
- **Chú thích hình:** ba câu "Cách đọc hình" của tôi làm tăng số lỗi `nhieu_so`. Tôi viết lại cho gọn nên số lỗi trở về như trước.
- **Kiểm tra khác:** `ruff` sạch toàn repo, `kiem_tra_doc_lap.sh` đạt cả 5 buổi, `dong_goi.py` vẫn lọc `dap-an/` và `tu-hoc.ipynb` khỏi zip.

**Chỗ lệch so với tài liệu, đã sửa theo số chạy thật**
- **Buổi 5, bài tập 1:** với dữ liệu tới 2019, trạm xăng chỉ có σ²/2 = 0,77%, chưa tới 1%. Tôi đổi bộ ba ngành thành Fuel dealers / Gasoline stations / Jewelry stores, vì Fuel dealers là ngành duy nhất vượt 1% (1,45%).
- **Buổi 8, bài tập 2:** bài cần nhiệt độ Boston, mà tệp này không có trong danh mục đã chốt sha256. Notebook chỉ nêu cách làm, còn lý do bỏ được ghi trong `DU_Y`.

**Thay đổi ở công cụ và môi trường**
- `tools/tu_hoc/du_lieu.toml` có thêm mô tả cho 7 bộ dữ liệu/họ bộ: MARTS, CPI, NIPA tháng và quý, G.17, `eia930-balance-*`, `open-meteo-*-2024`. Các buổi 13, 15, 17, 18, 25… dùng lại được.
- Môi trường dùng chung `pandas3` được cài thêm thư viện của buổi 5–8, trong đó có openpyxl và scikit-learn.

**Bạn cần biết:** `buoi-04/tu-hoc.ipynb` đã bị chạy và lưu lúc 14:14, có lẽ khi bạn mở nó trong VS Code. Vì vậy tệp chứa output và có đường dẫn tuyệt đối, làm `kiem_tra_doc_lap.sh` báo lỗi K5. Tôi đã sinh lại tệp sạch, bạn không mất gì ngoài output của lần chạy đó. Ghi chú này và các quyết định của phase nằm ở cuối `todos/phase-30.md`.

Phase tiếp theo là 31 (buổi 9–13).
