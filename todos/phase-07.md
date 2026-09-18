# Phase 7 — Rút gọn: chuẩn "gọn" D13 + buổi 1–3, Phụ lục A, B 🔲

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md` (mục "Chuẩn dễ hiểu", **D13**). Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 7"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

**Vì sao có phase này.** Người dùng đọc bản viết lại của Phase 6: *"dễ hiểu hơn nhưng dài dòng quá — viết dễ hiểu nhưng
không được dài dòng"*. Nguyên nhân: mỗi vòng đọc thử chỉ **thêm** giải thích (buổi 2 qua 6 vòng), không bước nào **bỏ**;
khuôn D2 bị làm đủ 10 bước cho mọi khái niệm; "Tóm lại", Lab, "Lỗi thường gặp" nói lại ý đã có. Phase này làm **trước**
Phase 8–9 để chuẩn "gọn" có sẵn khi viết lại 10 buổi còn lại.

Mục tiêu: **giảm ≥ 25% chữ** mỗi tài liệu (Phụ lục B ≥ 35%) mà **không mất khái niệm nào** và **đọc thử vẫn đạt**.
Không đổi code, lab, bộ chấm, dữ liệu, chỗ hở cố ý, con số đã đo.

| Tài liệu | Chữ ngoài bảng/code (trước) | Trang (trước) | Rà gọn (chỗ thừa) | Cắt | Chữ (sau) | Đọc thử lại | Trang (sau) |
|---|---|---|---|---|---|---|---|
| Buổi 01 | 6.910 | 19 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Buổi 02 | 8.991 | 22 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Buổi 03 | 7.485 | 21 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Phụ lục A | 5.441 | 19 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Phụ lục B | 12.494 | 30 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

(Đo 2026-09-18 bằng `kiem_de_hieu.dem_chu`; trang từ PDF hiện có.)

Checklist:
- [ ] `tools/CHUAN-DE-HIEU.md`: mục **D13 — Gọn** với ≥ 5 cặp trước/sau trích từ buổi 1–3, A, B thật (lặp ý giữa thân
      bài và "Tóm lại"; câu rỗng; ví dụ thứ hai thừa; Lab giải thích lại lý thuyết; khuôn D2 đủ 10 bước cho khái niệm
      đơn giản). Sửa mẫu chuẩn buổi 1 mục 4.8 cho gọn — nó là thước đo của mọi phase sau
- [ ] `tools/CHUAN-DE-HIEU.md`: thêm **"Prompt biên tập gọn"** cho subagent biên tập viên — trả về bảng: vị trí · loại
      (lặp ý / câu rỗng / ví dụ thừa / bước D2 thừa / giải thích điều đã biết) · đề xuất cắt/viết lại · số chữ bớt được;
      và danh sách "không được cắt" (định nghĩa lần đầu, ví dụ số nhỏ, câu nói bằng lời có thay số, Cách đọc hình)
- [ ] Sửa "Prompt đọc thử": thêm mục báo **chỗ thấy dài/lặp** (không tính vào chặn/khó) để hai vai bổ sung nhau
- [ ] `tools/kiem_de_hieu.py` (+ test): trần `do_dai` mới 3.500–6.500; mã mới `cau_rong` (danh sách cụm câu rỗng) và
      `lap_y` (câu "Tóm lại" trùng ≥ 60% từ với một câu trong mục; đoạn trùng lặp gần nguyên văn trong cùng tài liệu);
      chạy trên buổi 1–13 in bảng
- [ ] `tools/xuat_pdf.py --kiem`: ngưỡng 10–18 trang (phụ lục ≤ 18)
- [ ] `tools/khuon-buoi/tai-lieu.md`: ghi chú D13 — khuôn D2 là trần; chỉ "ví dụ số nhỏ" + "Tóm lại" bắt buộc
- [ ] Rút gọn buổi 1, 2, 3, Phụ lục A, B theo quy trình trong prompt; `kiem-tra.md` chỉ gọn đáp án dài, giữ D12
- [ ] Mỗi tài liệu: đọc thử lại bằng subagent MỚI vẫn đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10); ghi `NGHIEN-CUU.md` mục
      "Đọc thử" số chữ trước/sau + kết quả rà gọn
- [ ] Chốt trần độ dài sau khi đo buổi 1–3 đã rút gọn; nếu khác 3.500–6.500 chữ / 10–18 trang (đã ghi tạm ở `CLAUDE.md`
      quy tắc 13, 15 + DoD và `todos/quy-uoc.md`, prompt Phase 8–21) thì sửa đồng loạt
- [ ] `kiem_tra_lab.py 1 2 3` vẫn xanh/đỏ đúng chỗ; `kiem_tra_doc_lap.sh`; `ruff`; xuất lại PDF

Bắt buộc:
- **Không cắt**: định nghĩa lần đầu của từ mới, ví dụ số nhỏ tính tay, câu nói bằng lời có thay số dưới công thức,
  "Cách đọc hình"/"Đọc bảng" (được làm ngắn lại), hộp "Mượn trước", mọi chỗ đã sửa từ `phan-hoi-hoc-vien.md`
- Chỗ nào cắt xong đọc thử báo khó trở lại → viết lại câu đó rõ hơn, không khôi phục nguyên đoạn cũ
- Phụ lục B (30 trang) phải xuống ≤ 18: mỗi khái niệm một ví dụ; phần buổi 2 đã dạy kỹ thì phụ lục chỉ tóm lại + trỏ
  "buổi 2 mục …" (phụ lục là tra cứu, không phải bài giảng thứ hai)
- Buổi 2 hiện có `nhieu_so` 34 chỗ "có lý do" — rà lại, nhiều chỗ là dấu hiệu đoạn quá tải số
