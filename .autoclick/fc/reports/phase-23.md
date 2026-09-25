# phase 23

_2026-09-24 16:38:10_

Phase 23 đã xong và đã tick ✅ ở `todos.md`, `todos/phase-23.md` và `todos/tong-quan.md`. Tôi chưa commit gì.

## Buổi 24 — Ensemble, AutoML và ca khó

| Hạng mục | Kết quả |
|---|---|
| `tai-lieu.md` | 5 khái niệm, 4.597 chữ, PDF 14 trang, `kiem_de_hieu` 0 lỗi |
| Tự đọc thử | 0 chỗ chặn; 5 chỗ khó (đã viết lại câu); 2 chỗ nhỏ. Cả 10 câu quiz có căn cứ trong tài liệu, đã tính lại bằng Python |
| Rà gọn | 4.620 → 4.597 chữ, cắt 1 ý bị nói 3 lần |
| Lab (`kiem_tra_lab.py 24`) | đáp án xanh 6/6; `code/` đỏ đúng 2/6; notebook chạy hết trong 1,6–2,6 phút |
| `note-viet-lai.md` | 585 chữ, đã kiểm `dong_goi.py` lọc khỏi zip |

Số thật trên 1.000 chuỗi M4 (seed 0; chọn trên 2 cửa sổ đầu, báo cáo trên cửa sổ cuối W3):
- **Ensemble:** trung bình ETS + Theta + LightGBM đạt MASE 0,837, thắng mô hình đơn tốt nhất (LightGBM 0,855).
- **Chỗ hở cố ý:** chọn mô hình tốt nhất cho từng chuỗi rồi báo cáo trên chính dữ liệu đã dùng để chọn cho 0,694. Chấm trung thực thì ra 0,883. Khoảng lạc quan tăng từ 0,013 (1 ứng viên) lên 0,224 (30 ứng viên).
- **Trọng số:** trọng số "tối ưu" ước lượng riêng từng chuỗi cho 0,965, tệ hơn chia đều. Đây là combination puzzle.
- **AutoGluon:** ensemble của nó cho 0,858 trên đoạn kiểm nội bộ, 0,882 trên W3.

## Dự án giữa chặng 2
Đã có đề, rubric và bộ công cụ nộp → chấm → bảng xếp hạng. Có một khung `code/` với chỗ hở cố ý: backtest dùng nhiệt độ thật. Có lời giải mẫu, và bộ chấm tối thiểu 6 test (khung đỏ đúng 2 test, lời giải mẫu xanh 6/6).
- **Bậc thang của lời giải mẫu** (MASE, backtest 8 tuần): seasonal naive 1,04 → hồi quy 0,86 → LightGBM 0,93 → ensemble 0,82.
- **Rò rỉ thời tiết đo được:** dùng nhiệt độ thật thì backtest đẹp giả thành 0,70.
- **Chạy thử trên 2 tuần đã qua:** lời giải mẫu được 68/75 điểm tự động; khung mất trọn 8 điểm phần thời tiết.
- **Đã nộp thật một bài cho tuần 28/9**, trước mốc (tạo 24/9 09:25 UTC). Lúc nộp, dữ liệu chấm chưa tồn tại. Chấm được từ 9/10; tôi đã ghi việc này vào `todos/phase-24.md`. Tệp đầu vào của bài nộp chỉ nằm trên máy này, không commit.

## Chỗ lệch so với lộ trình, cần bạn biết
1. **Cold start:** tìm hàng tương tự theo danh mục đoán từ tên hàng **không** thắng "trung bình danh mục" (446,5 so với 446,6). Tìm theo **giá ra mắt gần nhất** thì thắng (400,6). Tài liệu viết đúng như vậy.
2. **Dự án không cần API key EIA nữa:** dùng tệp sáu tháng công khai của EIA. Tệp này trễ khoảng 1,5 ngày, nên đề có luật "chỉ dùng nhu cầu tới mốc − 48 giờ". Đã sửa bảng môi trường trong `CLAUDE.md`.
3. **Thay đổi hạ tầng dùng chung:**
   - Thêm ràng buộc phiên bản cho AutoGluon: statsforecast 2.0.3, torch 2.10.0. Bản cũ ép torch 2.13 làm `uv lock` hỏng trên macOS.
   - Sửa `sinh_nen.py` để luôn lấy torch bản CPU: venv buổi 24 giảm từ 8,2 GB xuống 2,2 GB.
   - `dong_goi.py` giờ lọc thư mục dữ liệu tải trực tiếp `lab/du-lieu/moi/`.
   - Danh mục thêm 5 bộ thời tiết dự báo lưu trữ (đã chốt sha256). Các bộ này chưa mirror lên Hugging Face vì cần `HF_TOKEN`.
4. **Nhỏ:** AutoGluon chạy với giới hạn 300 giây thay cho 20 phút (thực tế xong sau 43 giây). Bỏ AutoARIMA khỏi 30 ứng viên vì mất khoảng 1 giây/chuỗi trên CPU. Lộ trình đã cập nhật theo.

Một hạn chế: lời giải mẫu chỉ được chạy qua pytest trực tiếp, vì dự án không có thư mục `dap-an/` nên `python lab.py check --dap-an` không áp dụng. Cách chạy ghi trong `giam-khao/README.md`.

Bước tiếp theo là Phase 24: đọc thử độc lập trong phiên mới, và chấm bài nộp thật từ 9/10.

Nguồn chính:
- [Hướng dẫn EIA-930](https://www.eia.gov/survey/form/eia_930/instructions.pdf)
- [Open-Meteo Previous Runs API](https://open-meteo.com/en/docs/previous-runs-api)
- [AutoGluon fit()](https://auto.gluon.ai/stable/api/autogluon.timeseries.TimeSeriesPredictor.fit.html) và [model zoo](https://auto.gluon.ai/stable/tutorials/timeseries/forecasting-model-zoo.html)
- [FPP3 §13.4](https://otexts.com/fpp3/combinations.html)
- [Wang et al. 2023](https://arxiv.org/pdf/2205.04216)
- [Frazier et al. 2023](https://arxiv.org/pdf/2308.05263)
- [FFORMA](https://www.sciencedirect.com/science/article/abs/pii/S0169207019300895)
- [Chronos-2](https://arxiv.org/html/2510.15821v1)
