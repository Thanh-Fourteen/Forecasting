# Nhật ký research — Dự án giữa chặng 2: thi dự báo trên dữ liệu tương lai

<!-- KHÔNG vào zip phát học viên (tools/dong_goi.py lọc). -->

- **Ngày research:** 2026-09-24 (Phase 23), một phiên, không subagent.

## Nguồn đã đọc

| # | Nguồn | Truy cập | Dùng cho |
|---|---|---|---|
| 1 | Form EIA-930 Instructions (OMB 1905-0129, hết hạn 07/31/2029): https://www.eia.gov/survey/form/eia_930/instructions.pdf — số liệu theo **giờ kết thúc**, mốc UTC; tệp ngày nộp trước 7:00 ET, chứa "dự báo day-ahead của hôm qua cho hôm nay" (DF) và nhu cầu hôm qua; **sửa số dự kiến trong 3 ngày**, lỗi > 10 MWh sửa **trong 30 ngày**; DF là dự báo "làm trong hoạt động thường ngày", không bắt buộc cùng định nghĩa với D | 2026-09-24 | luật thời gian, chờ chấm 4 ngày, ghi chú CISO |
| 2 | EIA API v2, route `electricity/rto/region-data` (metadata đọc bằng `DEMO_KEY`): tần suất `hourly` (UTC) và `local-hourly`; facet `respondent`, `type` (D, DF, NG, TI); endPeriod lúc 2026-09-24 08:13 UTC là 2026-09-25T07 (DF của ngày mai đã có); D của ERCO trễ ~1 giờ; `DEMO_KEY` chạy được nhưng giới hạn lượt | 2026-09-24 | quyết định nguồn |
| 3 | Tệp sáu tháng `EIA930_BALANCE_2026_Jul_Dec.csv`: Last-Modified 2026-09-23 14:41 UTC (dựng lại mỗi ngày); D tới hết ngày địa phương hôm trước (UTC 23/9 04–07 giờ), DF tới hết hôm nay; cột như 2025 H2 | 2026-09-24 | `TRE_CONG_BO = 48` giờ |
| 4 | Open-Meteo Previous Runs API: https://open-meteo.com/en/docs/previous-runs-api — `_previous_dayN`, N = 0…7, "giá trị đã dự báo 24 giờ trước giờ hiệu lực" cho N = 1; lưu trữ đa số mô hình từ 1/2024; `end_date` tối đa hôm nay + 15 ngày (thử 2026-09-24: +16 bị từ chối) | 2026-09-24 | luật `truoc_⌈h/24⌉`, tải dự báo tuần tới |
| 5 | Trang giấy phép Open-Meteo (CC BY 4.0; API miễn phí cho phi thương mại) và EIA copyright & reuse (public domain) | 2026-09-24 | danh mục |

**Quyết định nguồn:** dùng **tệp sáu tháng** (không cần khoá, cùng định dạng dữ liệu cố định 2024–2025) thay cho API v2. Tệp trễ ~1,5 ngày → luật
"nhu cầu chỉ biết tới mốc − 48 giờ" áp cho cả backtest lẫn nộp thật. API v2 ghi trong đề là phương án dự phòng. Bảng môi trường trong `CLAUDE.md`
đổi: dự án giữa chặng 2 không còn cần khoá EIA.

## Dữ liệu thêm vào danh mục

5 bộ `open-meteo-du-bao-luu-{ciso,erco,miso,nyis,pjm}-2024-2025`: `temperature_2m` + `_previous_day1…7`, 1/2024 → 12/2025, giờ UTC, ~1 MB mỗi bộ.
Tải hai lần cùng sha256 (2026-09-24). Chưa mirror (cần HF_TOKEN của khoá). Los Angeles: `truoc_1` lệch `thuc` trung bình 1,28 °C, `truoc_7` 3,08 °C;
`truoc_1` có từ 2024-01-19.

## Phát hiện

- **DF của CISO thấp hơn thực tế trung bình 1.666 MW (6,5%) trong 2025**; MASE backtest của DF ở CISO 1,17–1,83, bốn vùng khác 0,2–0,45. Hướng dẫn
  EIA cho phép DF khác định nghĩa D → học viên thắng DF ở CISO là thật nhưng dễ; điểm thưởng tính theo từng vùng.
- **Dùng nhiệt độ thật trong backtest làm đẹp giả** (lời giải mẫu, 8 tuần): ensemble 0,696 so với 0,819 (mốc 4/8/2025) và 0,701 so với 0,771 (mốc
  29/12/2025).
- Hồi quy học 26 tuần thua seasonal naive (MASE 1,11 và 1,20) vì cửa sổ vắt qua đổi mùa; học 52 tuần: 0,86–0,88.
- Tuần có lễ (Labor Day 1/9/2026) làm seasonal naive của tuần sau tệ (MASE 1,52) → tỷ số $r$ của rubric so với seasonal naive cùng tuần nhỏ
  bất thường; ghi vào gợi ý của đề.

## Số liệu thật — bậc thang lời giải mẫu (MASE trung bình 5 vùng, backtest 8 tuần)

| Mốc nộp | seasonal naive | hồi quy | LightGBM | ensemble | `df` của vùng |
|---|---|---|---|---|---|
| 2025-08-04 | 1,039 | 0,856 | 0,927 | 0,819 | 0,512 |
| 2025-12-29 | 0,955 | 0,881 | 0,842 | 0,771 | 0,684 |

## Chạy thử công cụ (2026-09-24)

| Nhóm | Mốc | Loại | MASE thật | MASE backtest | $r$ | Điểm tự động |
|---|---|---|---|---|---|---|
| loi-giai-mau | 2026-08-31 | thử quá khứ | 0,965 | 0,929 | 0,675 | 68,5 |
| khung-code | 2026-08-31 | thử quá khứ | 0,970 | 0,933 | 0,704 | 57,9 (D = 0: thời tiết thật) |
| loi-giai-mau | 2026-09-07 | thử quá khứ | 0,727 | 0,891 | 0,679 | 68,1 |
| khung-code | 2026-09-07 | thử quá khứ | 0,798 | 0,885 | 0,765 | 52,5 (D = 0) |

Ngưỡng phần A chốt sau lần chạy này: đủ 35 điểm khi $r \le$ 0,60, 0 điểm khi $r \ge$ 1,00 (bản đầu 0,65–1,05 cho lời giải mẫu 32/35, quá dễ).

**Nộp THẬT trước mốc:** `giam-khao/chay-thu/loi-giai-mau/2026-09-28/` — tạo 2026-09-24 09:25:12 UTC (mốc 2026-09-28 00:00 UTC), nhu cầu biết tới
2026-09-24 07:00 UTC, thời tiết tải 09:25 UTC; sha256 `du-bao.csv` = `6e918da7895e8e3b61da99e2d269be02f7d463ab06c1c4d9cf197812b771830a`.
Dữ liệu chấm chưa tồn tại lúc nộp. **Chấm từ 2026-10-09** (Phase 24 hoặc sau): `python lab.py chay ../cong-cu/cham.py --moc 2026-09-28 --nhom
loi-giai-mau --ra ../giam-khao/chay-thu`. Nộp sớm 4 ngày nên tầm thật dài hơn backtest (dự báo thời tiết tới 11 ngày) — ghi nhận khi chấm.

## Tự đọc (vai học viên đã học tới buổi 24)

Viết lại được đúng: **làm gì** (du_bao/backtest/dac_trung cho 5 vùng × 168 giờ, sửa chỗ hở thời tiết, thêm LightGBM + ensemble), **nộp gì** (code, hai thư
mục nộp do `nop.py` sinh, sha256 gửi trước mốc, báo cáo trong `nop/<nhom>/`), **chấm thế nào** (A theo $r$, B theo $q$, C chạy lại + một lệnh, D thời
tiết + test + bảng biết trước, E báo cáo, thưởng theo vùng thắng DF). Chỗ mơ hồ đã sửa: tham chiếu định nghĩa MASE trỏ sai phần của rubric; chưa nói
đặt `bao-cao.md` ở đâu. Không lặp giữa đề và rubric: đề nói luật và cách nộp, rubric giữ công thức điểm.

## Đọc thử độc lập (Phase 24, 2026-09-24)

Phiên mới; đọc `de-bai.md`, `RUBRIC.md`, `code/README.md` trong vai học viên đã học xong buổi 24, rồi đối chiếu với `cong-cu/cham.py`, `du_lieu.py`.

**Viết lại được:** làm gì — dự báo 168 giờ nhu cầu điện 5 vùng, chỉ dùng nhu cầu tới mốc − 48 giờ và nhiệt độ theo luật `truoc_⌈h/24⌉`; sửa chỗ
hở trong `backtest`; dựng bậc thang seasonal naive → hồi quy nhiệt độ → LightGBM global → ensemble. Nộp gì — `code/du_bao.py`, hai thư mục
`nop/<nhom>/<moc>/` (hai thứ Hai liên tiếp) do `nop.py` sinh, sha256 của `du-bao.csv` gửi/đẩy git trước mốc, `bao-cao.md` sau khi chấm cả hai tuần.
Chấm thế nào — A theo $r$ (so seasonal naive cùng tuần), B theo $q$ (MASE thật ÷ MASE backtest), C chạy lại + một lệnh, D thời tiết + test + bảng
"biết trước bao lâu", E báo cáo, thưởng +1 mỗi vùng thắng `df`; chấm sớm nhất thứ Sáu sau tuần.

**Chỗ mơ hồ tìm được (2) — đã sửa:**
1. Đề §1 "`df` có MASE khoảng 0,4 ở bốn vùng": không nói bốn vùng nào; số thật (mục "Phát hiện") là 0,2–0,45 ở bốn vùng ngoài CISO → "0,2–0,45 ở
   bốn vùng ngoài CISO".
2. Rubric A "seasonal naive lặp lại tuần gần nhất đã biết đủ lúc mốc": đọc được hai cách (cùng giờ tuần trước, hay tuần trọn vẹn cuối cùng trước
   mốc − 48 giờ). `cham.seasonal_naive_tuan` lấy cùng giờ tuần trước, giờ nào chưa biết thì lấy hai tuần trước → viết đúng như vậy; thêm "tính từng
   vùng rồi lấy trung bình 5 vùng" cho $r$ (khớp `(mae / mae_sn).mean()`).

Đã kiểm khớp code: mẫu số MASE (`mau_so_mase`: "lặp lại tuần trước" trên 8 tuần tới mốc − 48 giờ); $q$ = trung bình MASE thật ÷ trung bình MASE
backtest; B tính theo $\lvert\ln q\rvert$ giữa ln 1,25 và ln 2; chấm sớm nhất mốc + 11 ngày (28/9 → 9/10). Rà gọn: lặp duy nhất là triệu chứng chỗ
hở ở đề §5 và `code/README.md` (hai câu, README là nơi học viên mở khi sửa code) — giữ. 0 chỗ mơ hồ còn lại.

**Chấm bài nộp thật của Phase 23 (mốc 2026-09-28): chờ** — dữ liệu tuần 28/9 → 5/10 chấm được từ 9/10/2026; hôm nay 24/9. Lệnh khi tới ngày:
`cd lab && python lab.py chay ../cong-cu/cham.py --moc 2026-09-28 --nhom loi-giai-mau --ra ../giam-khao/chay-thu`, rồi ghi MASE thật so với
backtest và so `df` vào đây. Phase 27 (2026-09-25): vẫn chờ, `dau-vao.parquet` mốc 2026-09-28 đã có trên máy soạn; chuyển Phase 32.
