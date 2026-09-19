# Phase T1 — Tóm tắt buổi 1–3 + khung thẻ ✅

Quy ước: `todos/quy-uoc.md` mục "File tóm tắt" và KHỐI CHUNG bước T. Prompt: `todos.md` mục "Phase T1".
Mẫu chuẩn: `buoi-01/tom-tat.md`, `buoi-02/tom-tat.md`, `buoi-03/tom-tat.md`.

| Buổi | Đọc hết tai-lieu.md | tom-tat.md | TOM-TAT PDF |
|---|---|---|---|
| 1 | ✅ | ✅ | ✅ |
| 2 | ✅ | ✅ | ✅ |
| 3 | ✅ | ✅ | ✅ |

Bắt buộc:
- Mỗi mục tiêu trong "1. Mục tiêu" của `tai-lieu.md` thành một phần `##` mở bằng **Kết luận của phần**
- Thẻ khái niệm (Định nghĩa · Giải thích · Ví dụ · Cách diễn giải · Tính chất · Vai trò trong dự báo · Phân biệt), thẻ mô hình
  (Ý tưởng · Kiến trúc · Điểm đặc biệt · Ưu điểm · Nhược điểm · Ví dụ · Khi nào dùng), thẻ phương pháp (Mục đích · Quy trình ·
  Giả định · Ưu điểm · Nhược điểm · Khi nào hỏng); bỏ trường trống, giữ thứ tự
- Tiêu đề thẻ: tiếng Việt kèm tiếng Anh trong ngoặc theo Phụ lục E; từ giữ nguyên tiếng Anh thì để nguyên
- Mọi con số chép từ `tai-lieu.md`; grep kiểm từng số; không hình, không lab, không quiz
- Mỗi từ trong bảng "Từ mới trong buổi" có thẻ riêng hoặc nằm trong một thẻ
- PDF: `xuat_pdf.py --tom-tat N…`; mở kiểm bảng, công thức, dấu tiếng Việt

Kết quả (2026-09-19):
- Khung thẻ chốt với người dùng sau 4 vòng: bản cắt chữ, bản gạch đầu dòng, bản nhãn lời thường đều bị loại;
  giữ khung thẻ dựa trên Frayer model + NIST e-Handbook, tiêu đề thẻ kèm tiếng Anh (Phụ lục E).
- `buoi-01..03/tom-tat.md` là mẫu chuẩn cho T2–T7.
- `tools/xuat_pdf.py` thêm `--tom-tat`. Máy Windows lúc soạn thiếu Pango nên WeasyPrint không chạy; 3 PDF tóm tắt được
  in bằng Chrome headless từ đúng HTML + CSS của `xuat_pdf.py`. Khi có máy chạy được WeasyPrint: chạy lại
  `xuat_pdf.py --tom-tat 1 2 3` cho đồng bộ.
