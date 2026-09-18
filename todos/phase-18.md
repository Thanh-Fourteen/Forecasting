# Phase 18 — Dự án cuối khoá 🔲

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 18"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Đề: **hệ thống dự báo thực tế**, chọn 1 trong 3 (A bán lẻ + tồn kho, B tải điện xác suất, C PM2.5 Việt Nam
+ cảnh báo). Tiêu chí xịn, đo được: *chấm trên dữ liệu tương lai chưa tồn tại lúc nộp, pipeline chạy tự
động 2 tuần, giám sát bắt được sự cố do giám khảo tiêm vào mà học viên không biết trước.*

- [ ] `du-an-cuoi/de-bai.md` — 3 đề, 11 hạng mục bắt buộc + 4 điểm thưởng (lấy từ mục "Buổi 44" của lộ trình)
- [ ] `du-an-cuoi/rubric.md` — thang **100 + 20**, mô tả rõ "đạt khi" cho từng hạng mục, riêng cho từng đề
- [ ] `du-an-cuoi/phieu-bai-toan.md`, `mau-model-card.md`, `mau-adr.md` — khuôn cho học viên
- [ ] `du-an-cuoi/cham/` — bộ chấm tự động ~50/100: lấy dữ liệu tương lai thật (M5 dùng holdout giám khảo giữ,
      EIA-930 và OpenAQ lấy trực tiếp), tính sai số/calibration, kiểm dấu thời gian dự báo **trước** dữ liệu thật,
      chạy lại pipeline kiểm tái lập, `kiem_ro_ri`, chạy test của học viên, kiểm giám sát có bắt sự cố không
- [ ] `du-an-cuoi/ngay-du-lieu-hong/` — **giám khảo giữ, không vào zip**: 3 script tiêm sự cố vào nguồn dữ liệu
      mirror của lớp (dữ liệu trễ, đổi đơn vị, trạm chết) + tiêu chí "đã xử lý xong"
- [ ] `du-an-cuoi/cham/phieu-cham-tay.md` — EDA và lập luận, quyết định và giá trị, bảo vệ, model card, ADR
- [ ] `du-an-cuoi/loi-giai-mau/` — lời giải mẫu cho **đề B** đầy đủ; đề A, C ở mức khung
- [ ] Hạ tầng "nguồn dữ liệu của lớp": mirror cập nhật hằng ngày để giám khảo tiêm sự cố được mà không đụng nguồn gốc
- [ ] `du-an-cuoi/DU-AN-CUOI.pdf` — bản phát cho học viên (**không kèm lời giải mẫu, không kèm ngay-du-lieu-hong/**)
- [ ] Ghi rõ trong buổi 44: phát đề từ **sau buổi 24**; nhóm 2–3 người; lịch 2 tuần dự báo trực tiếp
