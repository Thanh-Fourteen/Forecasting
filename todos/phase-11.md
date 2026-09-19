# Phase 11 — Đọc thử độc lập buổi 4–8 + Phụ lục C ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 11". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Phiên mới, không mang ngữ cảnh phase 8–10. Mỗi tài liệu: đọc mù → bảng A–E → rồi mới đối chiếu đáp án, sửa, rà gọn.

| Tài liệu | Quiz mù | Chặn / khó / nhỏ | Chỗ thừa | Đã sửa + đọc lại | PDF |
|---|---|---|---|---|---|
| Buổi 04 | ✅ 10/10 | ✅ 0 / 1 → 0 / 4 → 0 | ✅ 0 | ✅ | ✅ 18 tr |
| Buổi 05 | ✅ 10/10 | ✅ 0 / 1 → 0 / 3 → 1 | ✅ 0 | ✅ | ✅ 15 tr |
| Buổi 06 | ✅ 10/10 | ✅ 0 / 0 / 4 → 1 | ✅ 0 | ✅ | ✅ 16 tr |
| Buổi 07 | ✅ 10/10 | ✅ 0 / 0 / 4 → 0 | ✅ 0 | ✅ | ✅ 15 tr |
| Buổi 08 | ✅ 10/10 | ✅ 0 / 1 → 0 / 4 → 3 | ✅ 0 | ✅ | ✅ 15 tr |
| Phụ lục C | — (không có quiz) | ✅ 0 / 0 / 5 → 2 | ✅ 0 | ✅ | ✅ 12 tr |

Bắt buộc:
- Buổi 4–8 chỉ coi là nghiệm thu xong khi tài liệu tương ứng đạt ở phase này (phase soạn 8–10 ✅ trước đó là xong phần soạn)
- Mọi sửa → `kiem_tra_lab.py 4-8` vẫn xanh/đỏ đúng chỗ

## Kết quả (2026-09-18)

Ghi chi tiết: mục "Đọc thử độc lập (Phase 11)" trong `buoi-04..08/NGHIEN-CUU.md` (Phụ lục C ghi ở `buoi-04/NGHIEN-CUU.md`). Sửa chỉ bằng viết
lại câu (+18 tới +36 chữ mỗi buổi). Lỗi chung tìm được: chữ "chu kỳ" dùng cho cả *cycle* lẫn chu kỳ mùa vụ $m$ (buổi 4, 7, Phụ lục C) → viết
"chu kỳ mùa vụ"; quy ước trục từ 0 buổi 5 mâu thuẫn buổi 4; hồi quy hai biến CDD + HDD chưa viết ra (buổi 8); một dòng "+ HDD" làm vỡ danh
sách trong PDF buổi 8. `kiem_tra_lab.py 4 5 6 7 8` đạt (đáp án xanh, `code/` đỏ đúng, notebook chạy hết); `kiem_tra_doc_lap.sh 4–8` đạt;
`ruff` sạch cho buổi 4–8 + tools (2 lỗi còn lại nằm ở `buoi-14/` đang soạn, ngoài phase này).
