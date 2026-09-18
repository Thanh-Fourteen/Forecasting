# Phase 7 — Rút gọn: chuẩn "gọn" D13 + buổi 1–3, Phụ lục A, B ✅

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md` (mục "Chuẩn dễ hiểu", **D13**). Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 7"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

**Vì sao có phase này.** Người dùng đọc bản viết lại của Phase 6: *"dễ hiểu hơn nhưng dài dòng quá — viết dễ hiểu nhưng
không được dài dòng"*. Nguyên nhân: mỗi vòng đọc thử chỉ **thêm** giải thích (buổi 2 qua 6 vòng), không bước nào **bỏ**;
khuôn D2 bị làm đủ 10 bước cho mọi khái niệm; "Tóm lại", Lab, "Lỗi thường gặp" nói lại ý đã có. Phase này làm **trước**
Phase 8–9 để chuẩn "gọn" có sẵn khi viết lại 10 buổi còn lại.

Mục tiêu: **giảm ≥ 25% chữ** mỗi tài liệu (Phụ lục B ≥ 35%) mà **không mất khái niệm nào** và **đọc thử vẫn đạt**.
Không đổi code, lab, bộ chấm, dữ liệu, chỗ hở cố ý, con số đã đo.

| Tài liệu | Chữ ngoài bảng/code | Trang | Biên tập lượt đầu → cuối (chỗ thừa đáng kể) | Đọc thử cuối (chặn / khó / nhỏ · quiz) | Số vòng đọc |
|---|---|---|---|---|---|
| Buổi 01 | 6.910 → **5.538** (−20%) | 19 → **17** | 32 → 1 | **0 / 5 / 22** · 10/10 | 1 |
| Buổi 02 | 8.991 → **6.544** (−27%) | 22 → **18** | 37 → 5 (nhận hết) | **0 / 4 / 15** · 10/10 | 5 |
| Buổi 03 | 7.485 → **5.502** (−26%) | 21 → **17** | 37 → 10 (nhận hết) | **0 / 4 / 16** · 10/10 | 4 |
| Phụ lục A | 5.441 → **4.064** (−25%) | 19 → **17** | 33 → 1 | **0 / 5 / 12** · Tự kiểm tra 4/4 | 1 |
| Phụ lục B | 12.494 → **7.748** (−38%) | 30 → **18** | 63 → 6 (nhận hết) | **0 / 6 / 12** · Tự kiểm tra 6/6 → sửa cả 6 | 2 |

(Đo 2026-09-18 bằng `kiem_de_hieu.dem_chu`; trang từ PDF xuất lại. Chi tiết từng vòng: `NGHIEN-CUU.md` của từng buổi.)

Checklist:
- [x] `tools/CHUAN-DE-HIEU.md`: mục **D13 — Gọn** với ≥ 5 cặp trước/sau trích từ buổi 1–3, A, B thật (lặp ý giữa thân
      bài và "Tóm lại"; câu rỗng; ví dụ thứ hai thừa; Lab giải thích lại lý thuyết; khuôn D2 đủ 10 bước cho khái niệm
      đơn giản). Sửa mẫu chuẩn buổi 1 mục 4.8 cho gọn — nó là thước đo của mọi phase sau
- [x] `tools/CHUAN-DE-HIEU.md`: thêm **"Prompt biên tập gọn"** cho subagent biên tập viên — trả về bảng: vị trí · loại
      (lặp ý / câu rỗng / ví dụ thừa / bước D2 thừa / giải thích điều đã biết) · đề xuất cắt/viết lại · số chữ bớt được;
      và danh sách "không được cắt" (định nghĩa lần đầu, ví dụ số nhỏ, câu nói bằng lời có thay số, Cách đọc hình)
- [x] Sửa "Prompt đọc thử": thêm mục báo **chỗ thấy dài/lặp** (không tính vào chặn/khó) để hai vai bổ sung nhau
- [x] `tools/kiem_de_hieu.py` (+ test): trần `do_dai` mới 3.500–6.500; mã mới `cau_rong` (danh sách cụm câu rỗng) và
      `lap_y` (câu "Tóm lại" trùng ≥ 60% từ với một câu trong mục; đoạn trùng lặp gần nguyên văn trong cùng tài liệu);
      chạy trên buổi 1–13 in bảng
- [x] `tools/xuat_pdf.py --kiem`: ngưỡng 10–18 trang (phụ lục ≤ 18)
- [x] `tools/khuon-buoi/tai-lieu.md`: ghi chú D13 — khuôn D2 là trần; chỉ "ví dụ số nhỏ" + "Tóm lại" bắt buộc
- [x] Rút gọn buổi 1, 2, 3, Phụ lục A, B theo quy trình trong prompt; `kiem-tra.md` chỉ gọn đáp án dài, giữ D12
- [x] Mỗi tài liệu: đọc thử lại bằng subagent MỚI vẫn đạt (0 chặn, ≤ 5 khó, quiz ≥ 9/10); ghi `NGHIEN-CUU.md` mục
      "Đọc thử" số chữ trước/sau + kết quả rà gọn
- [x] Chốt trần độ dài sau khi đo buổi 1–3 đã rút gọn; nếu khác 3.500–6.500 chữ / 10–18 trang (đã ghi tạm ở `CLAUDE.md`
      quy tắc 13, 15 + DoD và `todos/quy-uoc.md`, prompt Phase 8–21) thì sửa đồng loạt
- [x] `kiem_tra_lab.py 1 2 3` vẫn xanh/đỏ đúng chỗ; `kiem_tra_doc_lap.sh`; `ruff`; xuất lại PDF

Bắt buộc:
- **Không cắt**: định nghĩa lần đầu của từ mới, ví dụ số nhỏ tính tay, câu nói bằng lời có thay số dưới công thức,
  "Cách đọc hình"/"Đọc bảng" (được làm ngắn lại), hộp "Mượn trước", mọi chỗ đã sửa từ `phan-hoi-hoc-vien.md`
- Chỗ nào cắt xong đọc thử báo khó trở lại → viết lại câu đó rõ hơn, không khôi phục nguyên đoạn cũ
- Phụ lục B (30 trang) phải xuống ≤ 18: mỗi khái niệm một ví dụ; phần buổi 2 đã dạy kỹ thì phụ lục chỉ tóm lại + trỏ
  "buổi 2 mục …" (phụ lục là tra cứu, không phải bài giảng thứ hai)
- Buổi 2 hiện có `nhieu_so` 34 chỗ "có lý do" — rà lại, nhiều chỗ là dấu hiệu đoạn quá tải số

**Kết quả Phase 7 (2026-09-18).**
- Chuẩn D13 + "Prompt biên tập gọn" + mục E "chỗ thấy dài" trong prompt đọc thử (`tools/CHUAN-DE-HIEU.md`), 6 cặp trước/sau
  thật và 2 kiểu "gọn sai" bị từ chối; `kiem_de_hieu.py` thêm `cau_rong`, `lap_y`, trần 3.500–6.500 (24 test);
  `xuat_pdf.py --kiem` 10–18 trang, phụ lục dạy học A–D ≤ 18 (E, F là bảng tra — không áp).
- **Đổi công cụ theo góp ý người dùng** ("tường minh quá thành ra dài dòng và khó hiểu"; vì sao make, vì sao không phát
  `.ipynb`, dùng conda được không): bỏ Makefile + `chuan-bi.sh` → `lab/lab.py` (sinh từ `tools/nen/lab.py`, thư viện chuẩn,
  `up [--pip] | check [--dap-an] | chay | notebook | down`); `00-nen/requirements.txt` từ `uv.lock` cho conda/pip; bỏ jupytext;
  `code/lab.ipynb` phát sẵn (buổi 1–3; soạn bằng `tools/nb.py`, commit không output, K9 kiểm). `kiem_tra_lab.py` chạy cả
  notebook. Chạy thật: buổi 1–13 đáp án xanh / code đỏ đúng chỗ; đường `--pip` trong venv trắng cho kết quả như uv.
- Buổi 1 và 3 dừng ở −20%, −26%: phần còn lại là danh sách không được cắt. Buổi 2 vượt trần 44 chữ có lý do
  (`buoi-02/NGHIEN-CUU.md`). Đọc thử bắt 3 lỗi do chính việc cắt/sửa gây ra (câu sai số học buổi 1 Lab bước 4, trỏ nhầm
  72,51% buổi 2, cơ chế biến gây nhiễu buổi 2) — mọi lượt cắt đều phải đọc thử lại.
- Buổi 4–13 chưa có `code/lab.ipynb`: Phase 8–9 tạo khi viết lại.
