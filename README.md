# Khoá Forecasting in AI — từ cơ bản đến nâng cao

Giáo trình tiếng Việt **44 buổi** về dự báo: từ đọc biểu đồ và làm sạch dữ liệu, qua mô hình thống
kê, machine learning, deep learning, tới foundation model, LLM dự báo sự kiện, suy luận nhân quả
và vận hành hệ thống dự báo trong production.

- **Lộ trình đầy đủ:** [`lo-trinh/lo-trinh-forecasting.md`](lo-trinh/lo-trinh-forecasting.md) (bản PDF nằm cạnh)
- **Kế hoạch xây khoá và tiến độ:** [`todos.md`](todos.md)
- **Quy tắc soạn nội dung:** [`CLAUDE.md`](CLAUDE.md)
- **Chuẩn bị môi trường (học viên):** [`MOI-TRUONG.md`](MOI-TRUONG.md)
- **Phụ lục dùng chung:** [`phu-luc/`](phu-luc/) — Python cho chuỗi thời gian, xác suất tối thiểu, sổ tay đọc biểu đồ, công thức chỉ số, từ điển thuật ngữ

## Khoá này khác ở đâu

1. **Hiểu dữ liệu trước, mô hình sau.** 10 buổi chỉ dành cho biểu đồ, biến đổi, phân rã, tương
   quan, đặc trưng chuỗi, làm sạch, ngoại lai, khử nhiễu và chống rò rỉ.
2. **Không tin con số chưa qua backtest.** Mọi mô hình phải thắng seasonal naive trên backtest
   rolling origin có kiểm định.
3. **Chỗ hở cố ý.** Code đầu buổi cho kết quả *đẹp giả tạo* (rò rỉ tương lai, đánh giá sai) —
   học viên tự tìm ra vì sao.
4. **Dự án thực tế.** Dữ liệu bẩn thật (PM2.5 Hà Nội/TP.HCM, tải điện, bán lẻ), baseline thật của
   doanh nghiệp để vượt, chấm trên **dữ liệu tương lai chưa tồn tại lúc nộp bài**.
5. **Mỗi buổi tự chứa.** Môi trường chốt phiên bản và dữ liệu có sha256 riêng — học lẻ một buổi được.

## 9 giai đoạn

| Giai đoạn | Buổi | Nội dung |
|---|---|---|
| 0. Nền móng | 1–3 | Bài toán dự báo, xác suất, dữ liệu thời gian |
| 1. Hiểu & chuẩn bị dữ liệu | 4–13 | Biểu đồ, biến đổi, phân rã, tự tương quan, tương quan chéo, đặc trưng, làm sạch, ngoại lai, khử nhiễu, feature |
| 2. Thống kê cổ điển | 14–21 | Chỉ số, backtest, ETS, ARIMA, hồi quy động, nhu cầu gián đoạn, đa biến, tài chính |
| 3. Machine learning | 22–24 | Mô hình global, gradient boosting, ensemble & AutoML |
| 4. Bất định | 25–28 | Dự báo xác suất, conformal, Bayes & GP, phân cấp |
| 5. Deep learning | 29–33 | Nền DL, N-BEATS/TFT, Transformer, mô hình sinh, thời tiết AI |
| 6. Foundation model & LLM | 34–37 | Chronos/TimesFM, fine-tune & benchmark, agent, dự báo sự kiện |
| 7. Nhân quả & quyết định | 38–40 | Tác động can thiệp, what-if, từ dự báo đến quyết định |
| 8. Production | 41–43 | Pipeline tái lập, quy mô lớn, giám sát & drift |
| Dự án cuối | 44 | Bán lẻ + tồn kho · tải điện xác suất · PM2.5 Việt Nam + cảnh báo |

## Công cụ

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r tools/requirements.txt
.venv/bin/python tools/xuat_pdf.py lo-trinh     # xuất PDF lộ trình
```

Trạng thái hiện tại (2026-09-17): xong **Phase 0 — hạ tầng**: lộ trình, kế hoạch, bộ công cụ (sinh nền buổi,
tải dữ liệu có sha256, kiểm tính tự chứa, chạy thử lab, đóng gói, xuất PDF), khuôn buổi, `MOI-TRUONG.md` và
Phụ lục A–E. Chưa soạn buổi nào — tiếp theo là Phase 1 (khung trợ giúp + danh mục dữ liệu).
