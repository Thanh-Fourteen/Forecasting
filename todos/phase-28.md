# Phase 28 — Research deep learning (buổi 29–33) ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 28". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Cụm đổi nhanh: research riêng một phase để đủ sâu khi không có subagent.

| Buổi | Research | Lệch lộ trình | Quyết định |
|---|---|---|---|
| 29 Nền DL | ✅ | nhỏ: 321 (không phải 370) chuỗi; neuralforecast kéo ray (venv 1,6 GB) | giữ; `check` chạy tập con |
| 30 N-BEATS … TiDE | ✅ | nhỏ: DeepAR không nhận hist exog, trả trung bình về đầu vào; TFT mặc định vượt 6 GB | giữ 5 kiến trúc; cấu hình RAM rút gọn |
| 31 Transformer | ✅ | không có SOTA mới thắng bền; `drop_last=True` xác nhận trong repo PatchTST/iTransformer | không thay kiến trúc |
| 32 Mô hình sinh | ✅ | **lớn**: DeepAR (neuralforecast) không có sample path; energy score kém nhạy | Lab 1 dùng `nf.simulate` + LSTM tự viết; Xong khi = variogram + CRPS tổng 14 ngày |
| 33 Không gian–thời gian & thời tiết AI | ✅ | **lớn**: PyG Temporal không cài được; AIFS theo điểm chỉ tầm 1–7 ngày; AIFS v2 (12/05/2026) | GNN tự viết; bảng 1–7 ngày; tách mốc phiên bản |

Bắt buộc:
- Mỗi buổi 29–33 có `NGHIEN-CUU.md` (nguồn + ngày + phiên bản + model/checkpoint revision) trước khi soạn
- Bảng "lộ trình ↔ hiện tại ↔ quyết định"; lệch lớn → cập nhật lo-trinh + todos, báo người dùng
