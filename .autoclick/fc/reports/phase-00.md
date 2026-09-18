# phase 0

_2026-09-17 20:02:47_

Phase 0 đã xong, chỉ còn tạo remote GitHub và push (không có trong yêu cầu nên tôi chưa làm). Lượt chạy thử bạn yêu cầu đã qua: sinh nền cho `buoi-00-thu` dùng UCI Bike Sharing → `make up`, dữ liệu khớp sha256 → `make down`, rồi xoá buổi giả.

## Research đã sửa lộ trình và todos ở ba chỗ

1. **Hệ Nixtla và AutoGluon chưa chạy được với pandas 3.** Tôi thử cài từng gói cùng pandas 3.0.5: statsforecast 2.1.1, utilsforecast 0.2.16 và mlforecast 1.1.0 đều đòi `pandas<3`, còn autogluon.timeseries 1.6.2 đòi `pandas<2.4`.
   - Cách xử lý: bảng phiên bản chung có một luật tự chốt pandas 2.3.3 cho buổi nào dùng các gói này. Buổi 1–13 vẫn dùng pandas 3.
   - Hệ quả cho Phase 2: buổi 3 phải dạy code chạy được trên cả hai bản. Chỗ khác nhau đã ghi trong Phụ lục A.
2. **Trạm PM2.5 của Đại sứ quán Mỹ ở Hà Nội/TP.HCM ngừng gửi dữ liệu từ 04/03/2025.** Buổi 10, dự án giữa chặng 1 và đề C đang dựa vào các trạm này.
   - Điều khoản OpenAQ cấm tải dữ liệu nếu không đăng ký và được cho phép, nên chỉ mirror được khi nhà cung cấp cho phân phối lại. Phase 1 phải chọn trạm khác.
3. **Con số "~75%" của buổi 2 chưa khớp với mô phỏng.** Trên dữ liệu log-chuẩn, khoảng "±1,96σ" phủ tổng cộng khoảng 95%. Cái sai nằm ở hình dạng: đuôi dưới 0%, đuôi trên 3,5–4,9%.
   - Phase 2 cần đo trên dữ liệu Bike Sharing thật; nếu không ra ~75% thì sửa lộ trình.

Ngoài ra có vài lệch nhỏ, đã ghi trong `tools/NGHIEN-CUU.md`:
- `properscoring` đã bị archive.
- `scoringrules` 0.11.0 tính WIS sai: 2,87 thay vì 1,67 (tôi đã kiểm lại độc lập).
- API miễn phí của Open-Meteo chỉ cho dùng phi thương mại.
- UCI tải chậm và không tải tiếp được khi đứt, nên bộ nào trên 10 MB phải có mirror.

## Cơ chế giữ các buổi độc lập
- **`sinh_nen.py`**: mỗi buổi có một tệp viết tay `lab/nen.toml`, chỉ ghi tên thư viện và tên bộ dữ liệu. Phiên bản lấy từ một bảng chung `tools/nen/phien-ban.toml`, kèm mốc giới hạn ngày phát hành cố định, để 44 tệp `uv.lock` không lệch nhau. Thư viện trợ giúp được cài vào môi trường của buổi, nên `import tv` chạy ở mọi thư mục.
- **`lay_du_lieu.py`**: chỉ dùng thư viện chuẩn, nên bản sao trong buổi chạy được trước cả khi cài thư viện. Tôi đã chạy thật với UCI, Hugging Face và EIA (key công khai `DEMO_KEY`, tải hai lần ra cùng sha256). Các lỗi sai sha256, thiếu key và Kaggle chưa đăng nhập đều báo rõ cách sửa. **OpenAQ chưa chạy thật** vì cần key.
- **`kiem_tra_doc_lap.sh`**: 10 kiểm tra K1–K10. Tôi cố ý cài từng vi phạm vào buổi giả và tool bắt đủ.

## Kết quả chạy thử
- Copy riêng thư mục buổi ra ngoài repo, dùng cache trắng, vẫn `make up` được trong 4,9 giây.
- Bộ chấm: `code/` đỏ đúng một test (chỗ hở cố ý), `dap-an/` xanh.
- `kiem_tra_lab.py --may-trang` ĐẠT.
- Zip không lọt `dap-an/` hay tài liệu nội bộ, và đóng gói hai lần cho cùng sha256.
- `ruff check .` sạch.

## Tài liệu
- `MOI-TRUONG.md` và Phụ lục A–E đã xuất PDF: 6, 7, 5, 7, 7, 9 trang. Lộ trình xuất lại vẫn 38 trang.
- Mọi đoạn code và con số trong phụ lục đều lấy từ lần chạy thật, có ghi seed.
- C và D mới là bản khởi đầu: C chưa có hình (Phase 3 thêm), D chưa có ví dụ trên dữ liệu thật (Phase 5 và 8 thêm).

Repo vẫn chưa có commit nào và tôi chưa commit gì. Cache `~/.cache/khoa-forecasting/` còn giữ vài tệp nhỏ từ các lần thử.
