# Bảng xếp hạng — dự án giữa chặng 2

ty_so = MAE ÷ MAE của seasonal naive cùng tuần (nhỏ hơn là tốt hơn). mase_df = MASE của dự báo day-ahead do đơn vị
điều độ công bố, trên cùng các giờ (đối thủ thật; nó dự báo trước chỉ 1 ngày). diem_tu_dong = A + B + phần tự động
của C và D (tối đa 75).

| hang | nhom | so_tuan | ty_so | mase | mase_backtest | mase_df | vung_thang_df | diem_tu_dong |
|---|---|---|---|---|---|---|---|---|

Mọi bài đã chấm (kể cả không hợp lệ):

| nhom | moc | hop_le | ty_so | mase | mase_backtest | mase_df | vung_thang_df | diem_tu_dong |
|---|---|---|---|---|---|---|---|---|
| loi-giai-mau | 2026-08-31 | False | 0.675 | 0.965 | 0.929 | 0.522 | 0 | 68.5 |
| khung-code | 2026-08-31 | False | 0.704 | 0.97 | 0.933 | 0.522 | 0 | 57.9 |
| loi-giai-mau | 2026-09-07 | False | 0.679 | 0.727 | 0.891 | 0.485 | 0 | 68.1 |
| khung-code | 2026-09-07 | False | 0.765 | 0.798 | 0.885 | 0.485 | 1 | 52.5 |
