# Phase 4 — Buổi 9–13 · Chuẩn bị dữ liệu + dự án giữa chặng 1 ✅

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 4"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

**Phase trọng tâm thứ hai**: làm sạch, ngoại lai, khử nhiễu, feature, chống rò rỉ.

| Buổi | Research | Tài liệu | Code | Lab | Quiz | PDF |
|---|---|---|---|---|---|---|
| 09 Đặc trưng & khả năng dự báo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 10 Làm sạch & dữ liệu thiếu | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 11 Ngoại lai & điểm gãy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 12 Khử nhiễu & miền tần số | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| 13 Feature & chống rò rỉ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 10 tr |
| Dự án giữa chặng 1 | ✅ | đề ✅ | lỗi cài sẵn ✅ 6/6 | bộ chấm ✅ | rubric ✅ | ✅ |

Bắt buộc:
- Buổi 9: spectral entropy vs MASE seasonal naive có số tương quan thật; phân cụm DTW; ABC–XYZ
- Buổi 10: **dữ liệu Việt Nam thật** (GHCNh Nội Bài + Open-Meteo Hà Nội/TP.HCM — OpenAQ đã bỏ); so 6 phương
  pháp điền trên **lỗ ngắn và lỗ dài** bằng che nhân tạo; ≥ 8 test cho `lam_sach.py`; cột cờ
- Buổi 11: 3 cách xử lý COVID ra 3 kết quả dự báo; Hampel vs z-score; PELT có chọn penalty
- Buổi 12: aliasing dựng thật; bảng 6 bộ lọc có cột "dùng tương lai?"; **test tự động bắt bộ lọc
  không nhân quả**; ví dụ khử nhiễu target làm đánh giá sai
- Buổi 13: `kiem_ro_ri` bắt đủ 4 feature rò cài sẵn; **feature Tết âm lịch đúng mọi năm 2000–2035**
  (test đối chiếu bảng ngày Tết); đo "cái giá của rò rỉ" thời tiết thật vs thời tiết dự báo
- Dự án giữa chặng 1: 6 lỗi cài sẵn (giám khảo giữ, **không vào zip**); bộ chấm tự động phần phát hiện lỗi;
  rubric 100 điểm. **Cột mốc M1**

*Research Phase 4 (2026-09-18) — điểm lệch đã sửa vào lộ trình:*
- Buổi 9: entropy × **MASE**(snaive) ≈ 0 (ρ = −0,03) vì MASE tự chuẩn hoá → đổi sang **sMAPE** (ρ = +0,33);
  MASE và việc đổi thang chuẩn hoá (đảo dấu, ρ = −0,52) thành chỗ hở/bài học. catch22 lọc từ **4.791** đặc trưng
  (không phải 7.658). Đặc trưng tự viết bằng NumPy; `tsfeatures` (Nixtla) đóng băng từ 2023 — chỉ nhắc
- Buổi 10: **OpenAQ v3 đòi API key cho mọi endpoint** (401), v2 đã ngừng (410) → thay bằng **GHCNh Nội Bài**
  (dữ liệu Việt Nam thật, CC0 đã xác minh) + Open-Meteo Hà Nội + Beijing; PyPOTS chỉ dạy lý thuyết
- Buổi 11: US BTS không tải được → **Eurostat avia_paoc** (đã thêm danh mục, CC BY 4.0, sha ổn định);
  "3σ xoá Tết rồi sửa bằng STL robust" **không chạy được** (Tết âm lịch) → đổi thành phản ví dụ + biến giả lịch âm;
  Hampel demo chuyển sang tổng lượt xem vi.wikipedia
- Buổi 12: Savitzky–Golay/wavelet có rò rỉ nhưng lợi ích giả nhỏ — sửa câu chữ lab 4; thêm Kalman filter
  (trễ 0 nhưng vẫn nhân quả) vào bảng so sánh
- GHCNh Nội Bài 2024/2025: đổi `mirror = false → true` (metadata NOAA ghi CC0-1.0, tài liệu không có WMO Res 40)
