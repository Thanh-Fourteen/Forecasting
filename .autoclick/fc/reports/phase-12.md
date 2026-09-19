# phase 12

_2026-09-18 23:36:21_

Xong Phase 12: đã viết lại buổi 9 và 10, và đánh ✅ ở `todos.md`, `todos/phase-12.md`, `todos/tong-quan.md`. Chưa commit.

| Buổi | Chặn (bản cũ → mới) | Khó | Cờ `kiem_de_hieu` | Quiz | Số chữ | PDF |
|---|---|---|---|---|---|---|
| 09 Đặc trưng & khả năng dự báo | 10 → **0** | 0 | 52 → **0** | 10/10 | 2.306 → 5.567 | 10 → 17 trang |
| 10 Làm sạch & dữ liệu thiếu | 8 → **0** | 0 | 51 → **0** | 10/10 | 2.772 → 4.589 | 10 → 14 trang |

**Đã làm:**
- Mỗi buổi còn 6 khái niệm chính. Mỗi kỹ thuật có phần "khi nào dùng / khi nào không" bằng lời thường, một ví dụ số nhỏ tính tay, và một thí nghiệm có số đo thật.
- Buổi 9 làm đủ các yêu cầu riêng:
  - spectral entropy tính tay trên phổ 4 tần số, kèm một hình mới;
  - catch22 minh hoạ trên hai chuỗi 8 điểm;
  - DTW có bảng tính tay 4 × 4;
  - ABC–XYZ minh hoạ bằng hai mã hàng;
  - lý do đổi MASE sang sMAPE bằng ví dụ số: MASE nói chuỗi thất thường **dễ hơn**, sMAPE nói nó khó hơn 10 lần;
  - bảng đặc trưng ghi "hệ số lệch".
- Buổi 10 làm đủ các yêu cầu riêng: bảng "khi nào dùng / không dùng" cho 7 cách điền, và ví dụ 5 dòng cho mốc thiếu mà `isna()` không thấy.
- Mỗi buổi có `code/lab.ipynb` mới, soạn bằng `tools/nb.py`. Tôi viết lại quiz và README của `code/`.
- Kiểm tra: `kiem_tra_lab.py 9 10` đạt (đáp án xanh, `code/` đỏ đúng chỗ hở, notebook chạy hết), `kiem_tra_doc_lap.sh 9 10` đạt, ruff sạch cho buổi 9–10. Tôi tính lại mọi ví dụ và đáp án quiz bằng Python.

**Đã sửa code buổi 9 — không phải chỗ hở cố ý:**
- Có 5 đặc trưng đổi theo đơn vị đo, trong khi docstring ghi chỉ 2: spike, độ dốc, độ cong đổi theo đơn vị (spike nhân 10¹² khi chuỗi nhân 1.000). Giờ STL chạy trên chuỗi đã chuẩn hoá z-score, như FPP làm.
- Bản đồ PCA đưa cả cột sai số (`smape_snaive`, `mase_*`) vào đầu vào, trong khi hình lại tô màu theo sMAPE để kiểm. Hàm mới `cot_ban_do` chỉ lấy 18 đặc trưng không phụ thuộc đơn vị. Vì vậy phần hai trục đầu giữ được đổi từ khoảng 45% lên **56%**.
- Hai sửa nhỏ: `ve_hinh.py` in sai tên đặc trưng mạnh nhất của PC1, đã sửa; khoá `do_lech` đổi thành `he_so_lech`.
- Các số khác trong buổi tái lập đúng với seed 42.

**Lỗi lập luận do lượt đọc thử bắt được:** bản cũ lấy "Spearman giữa CV và MASE = −0,11" làm bằng chứng rằng CV không đo độ khó. Con số này không chứng minh gì, vì chính bài vừa chỉ ra MASE của seasonal naive luôn quanh 1. Tôi viết lại đoạn đó theo số đo thật: trên dữ liệu M4, CV khá sát với sMAPE (Spearman 0,77). Lý do CV không dùng làm trục độ khó là nó xếp sai những chuỗi có mùa vụ đều, như ví dụ mã hàng trong bài.

**Còn tồn đọng:**
- `ruff check .` vẫn báo 2 lỗi trong `buoi-14/dap-an/ve_hinh.py` (thư mục chưa vào git). Tôi không đụng vì ngoài phạm vi phase này.
- Bảng môi trường trong `CLAUDE.md` vẫn ghi buổi 10 cần API key OpenAQ. Buổi 10 đã bỏ OpenAQ từ trước, nên dòng đó cần cập nhật; tôi chưa sửa `CLAUDE.md`.

Chi tiết (research, các vòng đọc thử, số trước/sau) nằm trong `buoi-09/NGHIEN-CUU.md` và `buoi-10/NGHIEN-CUU.md`, mục "Research viết lại" và "Đọc thử (Phase 12)".
