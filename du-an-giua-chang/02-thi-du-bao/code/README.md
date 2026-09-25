# code/ — khung xuất phát của dự án giữa chặng 2

Khung **chạy được** nhưng có **một chỗ hở cố ý**. Đừng tin con số backtest đầu tiên.

| Tệp | Làm gì | Bạn cần làm gì |
|---|---|---|
| `du_bao.py` | `dac_trung`, `seasonal_naive`, `hoi_quy` (hồi quy có nhiệt độ), `du_bao`, `backtest` | sửa chỗ hở trong `backtest`; thêm LightGBM global và ensemble (đề bài mục 4) |

**Đang cố tình sai** (triệu chứng): `python lab.py check` đỏ 2/6 — `test_thoi_tiet_backtest_la_du_bao`, `test_backtest_chi_dung_qua_khu`.

Công cụ dùng chung nằm ở `../cong-cu/` (đọc dữ liệu, nộp, chấm, bảng xếp hạng) — đừng sửa, bộ chấm dùng đúng các tệp đó.

```bash
python lab.py chay ../code/du_bao.py      # trong lab/: MASE backtest 8 tuần của khung
python lab.py check                       # bộ chấm tối thiểu
```
