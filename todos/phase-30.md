# Phase 30 — Notebook tự học + hình khái niệm · buổi 4–8 🔲

Quy ước: `todos/quy-uoc.md` (D14, KHỐI CHUNG V7, "Việc nền"). Cách làm: `tools/tu_hoc/HUONG-DAN.md`. Prompt: `todos.md` mục
"Phase 30". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

Một trong 7 phase (30–36, thêm 2026-09-28) làm notebook tự học `buoi-NN/tu-hoc.ipynb` + hình minh hoạ khái niệm `hinh/kn-*.png`
(notebook, `tai-lieu.md`, PDF) cho các buổi đã soạn; buổi 1–3 là mẫu. Cụm này: đọc dữ liệu: biểu đồ, biến đổi, phân rã, tương quan — nhiều khái niệm có hình. Hồ sơ môi trường: pandas3.

| Buổi | Nội dung `buoi_NN.py` (đủ ý, hộp khái niệm) | Hình `HINH` (đã xem lại) | `--chay` 0 lỗi, số khớp | Tài liệu + PDF (≤ 22 trang, kiem_de_hieu không lỗi mới) |
|---|---|---|---|---|
| 4 | 🔲 | 🔲 | 🔲 | 🔲 |
| 5 | 🔲 | 🔲 | 🔲 | 🔲 |
| 6 | 🔲 | 🔲 | 🔲 | 🔲 |
| 7 | 🔲 | 🔲 | 🔲 | 🔲 |
| 8 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Môi trường theo hồ sơ (`moi_truong.py N` — xem `--liet-ke`), dựng một lần mỗi hồ sơ; `--chay` chạy dưới giới hạn RAM.
- Code đáp án chép từ `buoi-NN/dap-an/` (bỏ `tv`: viết lại phần cần trong ô), số trong phần chữ lấy từ output `--chay`.
  Lab nặng (buổi 29–30): dùng cấu hình rút gọn, ghi thời gian chạy; không để `--chay` quá ~15 phút một buổi.
- Bộ dữ liệu mới → thêm mô tả vào `tools/tu_hoc/du_lieu.toml` (dùng mẫu `*` cho họ tệp). Kiểu tải chưa hỗ trợ (hf, kaggle,
  eia…) → mở rộng `nb.du_lieu()` trong `sinh.py`, không đổi danh mục.
- Tài liệu đã có hình cùng ý thì `sau=None` (hình chỉ vào notebook). Không sửa tay khối `hinh/kn-*` trong tài liệu.
- Hết phiên giữa chừng: dừng ở ranh giới buổi, tick buổi đã xong; phiên sau tiếp tục. Phase ✅ khi mọi buổi trong bảng xong.

Từ Phase 37 trở đi không cần phase riêng: buổi mới làm notebook + hình ngay trong phase soạn nó (KHỐI CHUNG V7); mọi phase
đầu phiên chạy `sinh.py --thieu` và làm bù buổi còn thiếu (quy tắc "Việc nền" trong `todos/quy-uoc.md`).
