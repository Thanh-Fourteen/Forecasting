# Phase 5 — Chuẩn "dễ hiểu": quy tắc, công cụ kiểm, mẫu chuẩn ✅

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 5"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Người dùng học buổi 1–13 thấy khó hiểu, phải hỏi ChatGPT (mục "Chuẩn dễ hiểu" ở phần Quy ước). Phase này dựng
**chuẩn + công cụ + bài mẫu**; Phase 6–8 dùng chúng viết lại 13 buổi đã có; mọi phase sau soạn theo chuẩn ngay từ đầu.
*Đánh số lại 2026-09-18: Phase 5–16 cũ → 9–20. Ghi chép cũ trong `NGHIEN-CUU.md`/`danh-muc.toml` còn dùng số cũ.*

- [x] **Research sư phạm** — `tools/NGHIEN-CUU-SU-PHAM.md` (2026-09-18; StatQuest/3Blue1Brown không truy cập được, Fyfe 2014 chỉ
      đọc tóm tắt — ghi rõ trong file; ngưỡng "3 số/đoạn" và "6 khái niệm" là quy ước của khoá, không có nguồn): cách viết tài liệu kỹ thuật cho người tự học (worked
      example effect, cognitive load — Sweller; "concreteness fading"; cách FPP, *Seeing Theory*, StatQuest, 3Blue1Brown
      giải thích quantile/phân phối/tự tương quan); hiểu lầm phổ biến của người mới với từng khái niệm buổi 1–13
- [x] `tools/CHUAN-DE-HIEU.md` — D1–D12 chi tiết; **mỗi quy tắc một cặp "trước/sau"** lấy từ tài liệu thật buổi 1–13;
      bảng nhãn cố định; prompt đọc thử nguyên văn + tiêu chí đạt; ghi chú expertise reversal cho buổi về sau
- [x] **Mẫu chuẩn**: viết lại buổi 1 mục 4.8 (dự báo điểm, quantile, chi phí lệch) theo khuôn D2 và đưa vào
      `CHUAN-DE-HIEU.md` làm bài mẫu. Phải trả lời được đúng 4 câu người dùng đã phải hỏi ChatGPT: *"thiếu" là thiếu gì*
      (lượng mua < nhu cầu thực, đơn vị kWh); *quantile là gì* (ví dụ dãy 1–5); *"quantile 0,8 của sai số = +0,455"
      nghĩa là gì*; *vì sao là 0,8* ($4/(4+1)$, tính từng bước). Con số mới (nếu có) chạy thật bằng `dap-an/`
      → XONG: ví dụ 10 ngày từ `buoi-01/dap-an/vi_du_quantile.py` (mua 9 kWh rẻ nhất = quantile 0,8); số năm 2009–2010
      chạy lại `ve_hinh.py` khớp 100% (0,455 · 1,213 · 0,987 · 0,673 · 44,0% · 20,1%); hình chi phí bỏ "TB", thêm đơn vị;
      ô 6 mục 4.3 sửa cho khớp. Đọc thử 2 vòng bằng subagent mới: **0 chặn** (bản cũ 5 chặn trong mục này); vòng 2 bắt
      được câu sai "8 trên 10 ngày" (đúng 9/10) + 6 chỗ khó — đã sửa hết. Hai cờ còn lại là cấp buổi (Phase 6)
- [x] `tools/khuon-buoi/tai-lieu.md` — thêm có chú thích: bảng "Từ mới trong buổi", hộp "Mượn trước",
      "Nâng cao — có thể bỏ qua lần đọc đầu", "Ví dụ số nhỏ", "Cách đọc hình", "Đọc bảng", "Tóm lại", "Tự kiểm tra";
      `tools/khuon-buoi/kiem-tra.md` — mẫu đáp án giải thích vì sao đúng/sai
- [x] `tools/xuat_pdf.py` — CSS cho các hộp (nền nhạt, in đen trắng vẫn phân biệt); `--kiem` đổi ngưỡng **12–24 trang**;
      công thức: nhúng lớp chữ ẩn chứa LaTeX để **copy từ PDF ra không mất công thức** (research weasyprint/ziamath;
      không làm được thì ghi lý do — D3 vẫn đảm bảo ý không mất) → XONG: span chữ trong suốt 0,1pt ngay sau ảnh, bố
      cục không đổi; pypdf đọc đúng thứ tự "Trước $p^\ast = …$ sau câu" (pdftotext đặt lệch dòng — hạn chế đã biết)
- [x] `tools/kiem_de_hieu.py NN` — kiểm máy phần đo được: có bảng "Từ mới"; mỗi `$$…$$` có đoạn lời ngay sau; mỗi ảnh
      có "Cách đọc hình"; mỗi mục lý thuyết có "Tóm lại" + "Tự kiểm tra"; câu > 40 chữ; đoạn > 3 con số; trích tiếng Anh
      > 15 từ; viết tắt tự chế (danh sách chặn); thuật ngữ in đậm/`code` chưa có trong bảng "Từ mới" hay Phụ lục E;
      số khái niệm chính (mục `###` trong Lý thuyết) > 6. **Chỉ báo cáo, không tự sửa.** Có test
      → XONG: 15 mã kiểm, `--chi-tiet`, `--nghiem`; `tools/test_kiem_de_hieu.py` 20 test (thư viện chuẩn). Trích tiếng Anh
      bắt từ 6 từ (không phải 15 — câu FPP ở mục 4.8 chỉ 7 từ). Bản cũ buổi 1–13: 50–89 vi phạm/buổi. Cột "Buổi" của E
      trước đây ghi buổi dạy kỹ → báo nhầm "Mượn trước"; E mới ghi buổi xuất hiện đầu tiên
- [x] `phu-luc/E-tu-dien-thuat-ngu.md` — mỗi thuật ngữ thêm **nghĩa bằng lời thường + ví dụ số nhỏ**; bổ sung mọi
      thuật ngữ buổi 1–13 còn thiếu (lấy danh sách từ `kiem_de_hieu.py`); PDF
      → XONG: 171 → 235 dòng, bảng 5 cột `Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi`; +50 thuật ngữ (khối
      thống kê nền, đơn vị kW/kWh, MA/EWMA/MAD/PELT/CUSUM/IIR/HP…); cột "Buổi" = buổi xuất hiện đầu tiên, dò bằng grep
      trong buổi 1–13 (≈ 80 dòng đổi, vd baseline 14 → 1, 14). Ví dụ số kiểm bằng Python. PDF 21 trang. Một số ví dụ là
      số minh hoạ tính tay (CROPS, AIC, LoRA), không phải số chạy từ dữ liệu
- [x] `phan-hoi-hoc-vien.md` — đã tạo 2026-09-18 với phản hồi đầu tiên (buổi 1 mục 4.8); giữ khuôn ghi
- [x] `CLAUDE.md` — quy tắc 11, 13, 14 + DoD đã đổi 2026-09-18; kiểm khớp `CHUAN-DE-HIEU.md` (tiêu chí đọc thử 0 chặn, ≤ 5 khó)
- [x] **Đo baseline**: chạy BƯỚC CUỐI "Đọc thử" trên **bản cũ** của buổi 1, 7, 12 — ghi số chỗ vướng + điểm quiz vào
      `tools/NGHIEN-CUU-SU-PHAM.md` để Phase 6–8 so trước/sau. Chỉnh prompt subagent tới khi nó bắt được đúng chỗ
      người dùng đã vướng ở buổi 1 mục 4.8 (nếu không bắt được → prompt đọc thử còn yếu, sửa trước khi dùng)
      → XONG: chặn/khó/nhỏ = 9/21/30 (buổi 1), 12/30/18 (buổi 7), 11/36/13 (buổi 12); quiz 10/10 cả ba → **quiz không
      phân biệt được**, đổi tiêu chí sang "0 chặn, ≤ 5 khó". Prompt bắt đủ 4 chỗ người dùng vướng ở 4.8, không phải sửa.
      Chỗ chặn chung: khái niệm thống kê nền dùng không định nghĩa. Phát hiện **đáp án sai** quiz buổi 7 câu 5
      (đã ghi `phan-hoi-hoc-vien.md`). Danh sách chỗ chặn từng buổi: `tools/NGHIEN-CUU-SU-PHAM.md` mục Baseline
