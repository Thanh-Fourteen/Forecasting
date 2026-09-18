# Phase 21 — Kiểm định chất lượng 🔲

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 21"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Làm trên **máy trắng** hoặc container sạch, đóng vai học viên.

- [ ] `tools/kiem_tra_lab.py` chạy toàn bộ 44 buổi — mọi `python lab.py check --dap-an` xanh, của `code/` đỏ đúng chỗ hở
- [ ] `tools/kiem_tra_doc_lap.sh` — 0 tham chiếu chéo, mọi buổi có `uv.lock` và dữ liệu có sha256
- [ ] **Bài kiểm tra độc lập thật:** chọn ngẫu nhiên 6 buổi (ít nhất 1 buổi mỗi giai đoạn 1, 4, 6), copy **chỉ**
      thư mục buổi đó sang máy trắng, chạy `python lab.py up && python lab.py check`. Hỏng buổi nào là buổi đó chưa tự chứa
- [ ] **Bài kiểm tra CPU-only:** buổi 29–35 trên máy không GPU, 16 GB RAM — ghi thời gian từng buổi; 8 GB với cấu hình rút gọn
- [ ] **Bài kiểm tra không API key trả phí:** buổi 36–37 chạy bằng model local + bản ghi phản hồi
- [ ] `ruff check` toàn repo — 0 lỗi
- [ ] Đọc lại 44 `tai-lieu.md`: mọi lệnh copy-paste được, **mọi con số trong tài liệu khớp output chạy lại** (sai lệch ngoài seed → sửa)
- [ ] Kiểm tra mạch **kiến thức**: buổi N có "Nhắc lại buổi trước" đủ, "Trạng thái đầu buổi" khớp `00-nen/`, dẫn sang buổi N+1
- [ ] Kiểm tra cột mốc M0–M7 đúng chỗ
- [ ] Kiểm tra `dap-an/` không rò vào `code/` hay vào zip
- [ ] Mọi `NGHIEN-CUU.md` có ngày; buổi nào research > 6 tháng (giai đoạn 5–6) hoặc > 12 tháng (còn lại) → đánh dấu cần rà
- [ ] Nhờ **một người ngoài** làm thử buổi 8, buổi 13, buổi 26 và dự án giữa chặng 1, ghi lại chỗ họ tắc
- [ ] **Đọc thử toàn khoá**: `tools/kiem_de_hieu.py` cả 44 buổi sạch; mọi `NGHIEN-CUU.md` có mục "Đọc thử" đạt;
      mọi mục trong `phan-hoi-hoc-vien.md` đã xử lý (ghi buổi/commit sửa); đọc thử lại 6 buổi ngẫu nhiên bằng subagent mới
- [ ] **Mạch khái niệm**: không buổi nào dùng khái niệm của buổi sau mà thiếu hộp "Mượn trước"; bảng "Từ mới" của
      44 buổi gộp lại khớp Phụ lục E
