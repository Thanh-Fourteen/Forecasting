# Phase 3 — Buổi 4–8 · Đọc dữ liệu: biểu đồ, biến đổi, phân rã, tương quan ✅

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 3"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

**Phase trọng tâm của khoá** (người dùng yêu cầu: hiểu sâu, đọc biểu đồ, phân tích tương quan).

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 04 Đọc & vẽ biểu đồ | ✅ | ✅ 3.261 chữ | ✅ 1/8 | ✅ 8/8 | ✅ | ✅ 12 trang |
| 05 Biến đổi & điều chỉnh | ✅ | ✅ 3.135 chữ | ✅ 3/8 | ✅ 8/8 | ✅ | ✅ 10 trang |
| 06 Phân rã | ✅ | ✅ 3.090 chữ | ✅ 2/7 | ✅ 7/7 | ✅ | ✅ 11 trang |
| 07 Tự tương quan & tính dừng | ✅ | ✅ 3.194 chữ | ✅ 4/9 | ✅ 9/9 | ✅ | ✅ 10 trang |
| 08 Tương quan giữa các chuỗi | ✅ | ✅ 3.814 chữ | ✅ 7/10 | ✅ 10/10 | ✅ | ✅ 10 trang |

Phụ lục C đã cập nhật từ nội dung buổi 4–8 (thêm mục Heatmap lịch, Boxplot theo mùa, CCF, Tương quan trượt;
mỗi mục có "Ví dụ có số" từ dữ liệu thật) — 9 trang.

Bắt buộc:
- Buổi 4: bộ 8 biểu đồ chẩn đoán thành hàm dùng lại; một biểu đồ "gây hiểu nhầm" vẽ lại trung thực;
  **mỗi loại biểu đồ có ví dụ đọc đúng và ví dụ đọc sai** (đồng thời là nội dung Phụ lục C)
- Buổi 5: đo bằng số bias khi log–exp không hiệu chỉnh; tự viết Box-Cox
- Buổi 6: classical decomposition hỏng trên mùa vụ kép — thấy trên hình phần dư; MSTL sửa; tính $F_T, F_S$
- Buổi 7: bảng 4×4 (4 chuỗi mô phỏng × ACF/PACF/ADF/KPSS); giải thích khi ADF và KPSS mâu thuẫn
- Buổi 8: **đủ 5 tình huống**: tương quan giả hai chuỗi xu hướng; quan hệ chữ U (Pearson thấp, MI cao);
  CCF trước/sau prewhitening; tương quan trượt đổi dấu theo mùa; Granger "có ý nghĩa" nhưng không nhân quả

*Research Phase 3 (2026-09-18) — điểm lệch đã sửa vào lộ trình:*
- Buổi 5: Census MARTS lấy qua bản lưu Wayback chốt sha256 (census.gov chặn 403 từ Việt Nam; API cần key)
- Buổi 6: phân rã cổ điển chu kỳ 24 — nhịp tuần vào xu hướng, phần dư mang mẫu hình tháng×giờ (không phải "mùa vụ tuần
  rơi hết vào phần dư"); robust minh hoạ bằng giờ hỏng 21/11/2024 thay đợt nắng nóng
- Buổi 7: thay tỷ lệ thất nghiệp BLS bằng sản lượng công nghiệp FRB G.17 (BLS không có tệp nhỏ)
- Buổi 8: cặp chuỗi xu hướng = CPI-U × dân số; ERCOT + Open-Meteo Dallas/Houston 2024 (thêm danh mục);
  `ccf(x, y)` của statsmodels chỉ trả corr(x_{t+k}, y_t), k ≥ 0 — muốn "x dẫn y" gọi `ccf(y, x)`
