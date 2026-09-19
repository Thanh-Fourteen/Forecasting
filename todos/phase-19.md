# Phase 19 — Buổi 18–19 · Hồi quy động, nhu cầu gián đoạn ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 19". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 18 Hồi quy động | ✅ | ✅ 4.136 chữ | ✅ mới | ✅ 5/5, đỏ 2 | ✅ | ✅ 0/0 | ✅ 13 tr |
| 19 Nhu cầu gián đoạn | ✅ | ✅ 3.679 chữ | ✅ mới | ✅ 8/8, đỏ 4 | ✅ | ✅ 0/0 | ✅ 12 tr |

Bắt buộc:
- Buổi 18: hồi quy giả có p-value "đẹp" rồi sửa bằng hồi quy động; so 4 cách đa mùa vụ; Prophet có/không Tết
- Buổi 19: chấm bằng **cả RMSSE lẫn chi phí tồn kho mô phỏng**, chỉ ra hai thước đo chọn khác nhau
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

## Kết quả (2026-09-19)

- Research: Prophet **còn bảo trì** (1.4.0 ngày 15/8/2026, hỗ trợ pandas 3 từ 1.3.0) → thêm vào `tools/nen/phien-ban.toml`; FPP ch. 7, 10,
  §12.1–12.2, §13.2; Syntetos–Boylan 2005 (+ phản biện Svetunkov 2024: ngưỡng chỉ để chọn Croston/SBA); TSB (Teunter et al. 2011);
  Kourentzes 2014 (chấm bằng tồn kho). Chi tiết: `buoi-18/NGHIEN-CUU.md`, `buoi-19/NGHIEN-CUU.md`.
- Buổi 18: hồi quy giả hành khách EU ~ sản lượng công nghiệp Mỹ (p = 3·10⁻¹⁶, R² 0,83; thêm xu hướng thì hệ số đổi dấu) → hồi quy động
  p 0,59, phần dư trắng (Ljung–Box p 0,64); mô phỏng 1.000 cặp bước ngẫu nhiên: 78,5% "có ý nghĩa". Tải ERCOT 24 cửa sổ (bước 13 ngày):
  hồi quy động 2.082, MSTL 2.104, seasonal naive 2.173, TBATS 2.438, hồi quy thường 2.951, Prophet 2.998 MW; DM: hồi quy động ngang
  seasonal naive (p 0,76), thắng Prophet (p 0,017) — **lệch "Xong khi" của lộ trình, đã cập nhật lo-trinh**. Prophet khai Tết ± 7 ngày: MAE quanh
  Tết 2024 0,355 → 0,118, nhưng cả năm vẫn thua seasonal naive 364 ngày.
- Buổi 19: 2.674 mã Car Parts (76% số 0); 12 cutoff; RMSSE + mô phỏng order-up-to (quantile 0,9 Poisson, hàng về sau 1 tháng). IMAPA tốt nhất
  cả hai thước đo (0,673 / 29,6); MASE chọn "Zero" (không nhập hàng, chi phí 43,4); RMSSE xếp Zero trên AutoETS nhưng chi phí ngược lại;
  Croston/SBA thua trung bình lịch sử vì mặt hàng ngừng bán (TSB thì không).
- Lỗi bắt được khi tự làm: bẫy thứ trong tuần (cutoff cách 14 ngày) và cửa sổ cuối vượt tệp nhiệt độ (buổi 18); mô phỏng tồn kho có thời gian
  dẫn thực chất bằng 0 (buổi 19, bắt khi tự đọc thử — chặn → sửa code, chạy lại mọi chi phí).
- Chỗ hở (cập nhật `quy-uoc.md`): 18 — `he_so_ip` hồi quy thường, `KHAI_TET = False`; 19 — chấm MAE/MAPE bỏ tháng 0 và chọn theo MAE, `tsb` chỉ
  cập nhật ở tháng có bán.
- Phụ lục E thêm 11 thuật ngữ; danh mục dữ liệu cập nhật cột buổi, Phụ lục F sinh lại.
- `ruff` sạch; `kiem_de_hieu.py 18 19` 0; `kiem_tra_lab.py 18 19` đạt; `kiem_tra_doc_lap.sh` đạt (19 buổi); `sinh_nen.py --kiem --tat-ca` khớp.
