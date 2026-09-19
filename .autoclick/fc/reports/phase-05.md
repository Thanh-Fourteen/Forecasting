# phase 5

_2026-09-18 10:58:39_

Phase 5 xong. Đây là bộ chuẩn và công cụ để Phase 6–8 viết lại buổi 1–13 cho dễ hiểu. Chưa có gì được commit.

**Bằng chứng nó có tác dụng:**
- **Mục 4.8 buổi 1** (đoạn bạn phải hỏi ChatGPT) đã viết lại làm bài mẫu. Khi cho một agent đóng vai học viên mới đọc, số chỗ "chặn" (không hiểu thì không đọc tiếp được) giảm từ 5 xuống 0. Agent đó tự trả lời đúng cả 4 câu bạn từng phải hỏi: thiếu là thiếu gì, quantile là gì, +0,455 nghĩa là gì, vì sao là 0,8.
- **Bản cũ buổi 1, 7, 12** được đọc thử để đo mốc ban đầu: mỗi buổi có 9–12 chỗ chặn. Chỗ chặn chung nhất là các khái niệm thống kê nền (phân phối, quantile, phương sai, tương quan, kiểm định) được dùng mà không định nghĩa. Vì vậy Phase 6 phải dạy kỹ khối này ở buổi 2.
- **Quiz không phân biệt được tài liệu dễ hay khó hiểu:** cả 3 bản cũ đều được 10/10. Tôi đổi tiêu chí đạt thành "0 chỗ chặn, tối đa 5 chỗ khó" và ghi vào `CLAUDE.md` cùng `todos/quy-uoc.md`.

**Đã làm:**
- [tools/CHUAN-DE-HIEU.md](tools/CHUAN-DE-HIEU.md): 12 quy tắc, mỗi quy tắc có một ví dụ trước/sau lấy từ tài liệu thật. Kèm bài mẫu, prompt đọc thử nguyên văn và tiêu chí đạt.
- [tools/kiem_de_hieu.py](tools/kiem_de_hieu.py): kiểm tự động 15 loại lỗi đếm được, kèm 20 test. Bản cũ buổi 1–13 có 43–77 lỗi mỗi buổi.
- [tools/NGHIEN-CUU-SU-PHAM.md](tools/NGHIEN-CUU-SU-PHAM.md): nghiên cứu sư phạm có nguồn, cộng danh sách chỗ chặn của buổi 1, 7, 12. Hai ngưỡng "tối đa 3 con số mỗi đoạn" và "tối đa 6 khái niệm mỗi buổi" là quy ước riêng của khoá, không nguồn nào nêu đúng các con số này.
- Khuôn buổi `tools/khuon-buoi/` có sẵn các khung: "Từ mới trong buổi", "Mượn trước", "Cách đọc hình", "Tóm lại", "Tự kiểm tra", "Mục đích" / "Đọc kết quả" cho từng bước lab.
- Phụ lục E: từ 171 lên 235 dòng. Mỗi thuật ngữ có cột "Nói đơn giản" và ví dụ số nhỏ. Cột "Buổi" nay ghi buổi thuật ngữ xuất hiện lần đầu (ví dụ baseline đổi từ 14 thành 1, 14).
- PDF: copy công thức ra giờ còn nguyên LaTeX, không mất như đoạn bạn dán lúc trước. Đáp án "Tự kiểm tra" hiện thành khối thụt lề. Khoảng trang hợp lệ đổi thành 12–24.

**Bạn cần biết:**
- **Đáp án quiz buổi 7 câu 5 bị sai.** Đáp án ghi trung bình là 6, nhưng dãy có tổng 52 nên trung bình là 52/9 ≈ 5,78, và $r_1 ≈ 0{,}020$ chứ không phải 0. Tôi đã ghi vào [phan-hoi-hoc-vien.md](phan-hoi-hoc-vien.md) để Phase 7 sửa.
- **Mọi PDF đã được sinh lại**, không riêng buổi 1 và Phụ lục E, vì tôi chạy lệnh xuất không kèm tham số. Nội dung và số trang giữ nguyên; thêm được khả năng copy công thức. Nếu bạn đang học từ bản copy trong thư mục học riêng thì nên chép lại bản mới. Buổi 2–13 hiện bị báo "ngoài 12–24 trang" theo ngưỡng mới, Phase 6–8 sẽ xử lý.
- **`todos.md`** giờ còn 653 dòng, chỉ gồm tiêu đề phase, link chi tiết và prompt. Phần còn lại nằm trong thư mục `todos/`.
- **Thư mục `Dang hc/buoi-01`** đang nằm trong Thùng rác: bị xoá bằng giao diện lúc 10:19. Nếu bạn không định xoá thì khôi phục từ đó được.
- **Ruff báo 2 lỗi** trong `buoi-14/dap-an/ve_hinh.py`. Đó là bản nháp chưa commit của Phase 9, tôi không đụng tới.

Phase tiếp theo trong `todos.md` là Phase 6: viết lại buổi 1–3 và Phụ lục A, B.
