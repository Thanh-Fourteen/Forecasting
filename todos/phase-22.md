# Phase 22 — Buổi 22–23 · Dự báo thành hồi quy, gradient boosting ✅

Quy ước: `todos/quy-uoc.md` (KHỐI CHUNG). Prompt: `todos.md` mục "Phase 22". Trạng thái ✅/🔲 ở tiêu đề khớp `todos.md`.

| Buổi | Research | Tài liệu | Code | Lab + notebook | Quiz | Tự đọc thử + rà gọn | PDF |
|---|---|---|---|---|---|---|---|
| 22 Dự báo thành hồi quy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 13 tr |
| 23 Gradient boosting | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 13 tr |

Bắt buộc:
- Buổi 22: test bắt lag < horizon trong chiến lược direct; sai số theo h của recursive/direct/MIMO; cây không ngoại suy xu hướng
- Buổi 23: Tweedie vs L2 trên WRMSSE; Optuna CV thời gian vs KFold ngẫu nhiên; SHAP cho **một dự báo cụ thể**; monotone
  constraint cho giá; M5 cần tài khoản Kaggle (luật cuộc thi) — luôn có bộ dự phòng mở UCI Online Retail II
- - **Notebook + gọn**: `code/lab.ipynb` (soạn bằng `tools/nb.py`), tài liệu trỏ "ô bước N"; lệnh `python lab.py …`;
  D13 ngay từ đầu (3.500–6.500 chữ, PDF 10–18 trang); tự đọc thử + tự rà gọn (KHỐI CHUNG Đ)

## Kết quả (2026-09-24)

| Buổi | Chữ | PDF | Đọc thử (vòng 1 → 2) | check | Số chính |
|---|---|---|---|---|---|
| 22 | 4.115 | 13 tr | 0 chặn / 3 khó → 0 / 0 | đáp án 10/10 xanh; `code/` đỏ 4/10 đúng chỗ | 10.000 trang Web Traffic: LightGBM global RMSSE 0,916, AutoETS 0,951, seasonal naive 1,099; global thắng 58% số trang; direct rò rỉ 0,477 (đúng 0,511) |
| 23 | 4.105 | 13 tr | 0 chặn / 3 khó → 0 / 0 | đáp án 7/7 xanh; `code/` đỏ 2/7 đúng chỗ | 500 mã Online Retail II, WRMSSE: L2 0,709, Tweedie 0,680, AutoETS 0,674, Tweedie tune CV thời gian 0,669, tune KFold 0,678; PD giá sai chiều, ràng buộc đơn điệu 0,678 |

Lệch lộ trình: buổi 23 dùng Online Retail II làm dữ liệu chính (M5 cần Kaggle, chưa chốt sha256) — đã sửa lộ trình. Gói `shap` không
cài được với numpy 2.5.3 → dùng `pred_contrib` của LightGBM. Hạ tầng: `dong_goi.py` loại thêm `lab/du-lieu/cache/`; Phụ lục E thêm 6
thuật ngữ. Quy tắc `note-viet-lai.md` đổi thành "ý riêng, ngắn gọn, ~500–700 chữ" theo yêu cầu người dùng.
