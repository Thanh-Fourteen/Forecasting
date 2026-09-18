# Nhật ký research — Buổi 3: Dữ liệu thời gian với pandas, polars, DuckDB

- **Ngày research:** 2026-09-17
- **Nguồn dùng chung đã kiểm ở Phase 0 (Phụ lục A):** ghi chú phát hành pandas 3.0, `merge_asof`, `tz_localize`,
  polars `join_asof` / `group_by_dynamic` / `replace_time_zone`, DuckDB ASOF JOIN / `time_bucket` / TIMESTAMPTZ,
  pandas 3 bỏ phụ thuộc pytz — không lặp lại ở đây.
- **Máy chạy:** Intel i5-11600K, 12 luồng, 31 GB RAM, Python 3.12.3; nền buổi: pandas 3.0.5, polars 1.44.2,
  duckdb 1.5.5, pyarrow 25.0.1 (và đối chiếu pandas 2.3.3 ở venv tạm)
- **[CHẠY]** = đã chạy, số trong tài liệu lấy từ lần chạy này

## Nguồn đã đọc

| # | Nguồn | Loại | Truy cập | Dùng cho |
|---|---|---|---|---|
| 1 | NYC TLC Data Dictionary — Yellow Taxi Trip Records (PDF, bản "March 18, 2025"), https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf | tài liệu chính thức | 2026-09-17 | nghĩa cột thời gian |
| 2 | pandas User Guide — Time series / date functionality, https://pandas.pydata.org/docs/user_guide/timeseries.html | tài liệu chính thức | 2026-09-17 | DST, `label`/`closed`, `asfreq` |
| 3 | pandas `DataFrame.asfreq`, `merge_asof` API | tài liệu chính thức | 2026-09-17 | chuỗi không đều, ghép quá khứ |
| 4 | polars `Expr.dt.replace_time_zone`, https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.dt.replace_time_zone.html | tài liệu chính thức | 2026-09-17 | DST trong polars |
| 5 | DuckDB TIMESTAMPTZ functions, https://duckdb.org/docs/current/sql/functions/timestamptz.html ; TIMESTAMP type; ICU extension | tài liệu chính thức | 2026-09-17 | `timezone()`, ICU |
| 6 | Open-Meteo Historical Weather API docs, https://open-meteo.com/en/docs/historical-weather-api | tài liệu chính thức | 2026-09-17 | tham số `timezone` |
| 7 | open-meteo GitHub issue #1764 "UtcOffsetSeconds() returns incorrect offset for requested timestamps", https://github.com/open-meteo/open-meteo/issues/1764 | issue | 2026-09-17 | lỗi múi giờ Open-Meteo |
| 8 | DuckDB Labs db-benchmark, https://duckdblabs.github.io/db-benchmark/ (báo cáo 2026-08-17) | benchmark | 2026-09-17 | so tốc độ ở quy mô lớn |
| 9 | Polars PDS-H benchmark, https://www.pola.rs/posts/benchmarks/ (~2025-06) | benchmark của nhà phát triển | 2026-09-17 | như trên |

## Phiên bản đã xác minh

| Thư viện / dữ liệu | Phiên bản / sha256 | Xác minh |
|---|---|---|
| pandas | 3.0.5 (nền buổi) — đối chiếu 2.3.3 | PyPI (Phase 0) + [CHẠY] cả hai |
| polars | 1.44.2 | PyPI |
| duckdb | 1.5.5 (ICU `STATICALLY_LINKED`) | [CHẠY] `duckdb_extensions()` |
| pyarrow | 25.0.1 | PyPI |
| yellow_tripdata_2024-03.parquet | 60.078.280 B, `2d4cdc8f…9823`, 3.582.628 dòng | [CHẠY] hai lần tải cùng sha |
| yellow_tripdata_2024-11.parquet | 60.658.709 B, `5ef32187…cfd3b`, 3.646.369 dòng | [CHẠY] |
| taxi_zone_lookup.csv | 12.331 B, `1a99e105…c8ed`, 265 khu vực | [CHẠY] |
| Open-Meteo NYC 2024-03-01 → 2024-11-30, UTC, ERA5 | 242.993 B, `fd75dc93…a75d` | [CHẠY] |

## Phát hiện (đưa vào tài liệu)

1. **Cột thời gian taxi là giờ địa phương không ghi múi giờ.** Từ điển dữ liệu chỉ viết "tpep_pickup_datetime — The
   date and time when the meter was engaged." — **không nhắc múi giờ/DST** (agent grep cả Data Dictionary và Trip
   Record User Guide). Kiểu Parquet `Timestamp(isAdjustedToUTC=false, timeUnit=microseconds)`. Bằng chứng là giờ địa
   phương nằm trong chính dữ liệu [CHẠY]: 10/3/2024 không có chuyến nào đón lúc 02:xx; 3/11/2024 giờ 01:00 có 9.869
   chuyến (Chủ nhật sau 10/11: 5.318).
2. **Hệ quả DST thấy được trong dữ liệu thật [CHẠY]:** 1.093 chuyến đón 01:xx ngày 10/3 trả sau 03:00 (thời lượng bị
   cộng 1 giờ); tháng 11 có 1.078 chuyến "trả khách trước khi đón", 1.001 trong số đó đón lúc 01:xx ngày 3/11.
3. **Chuyến ngoài tháng [CHẠY]:** tệp tháng 3 có 23 chuyến đón ngoài tháng (sớm nhất 2002-12-31 22:17:10); tháng 11 có
   50. → `groupby` giờ thô ra 747 nhóm thay vì 744.
4. **Open-Meteo `timezone=America/New_York` sai quanh DST.** Docs: "If timezone is set, all timestamps are returned as
   local-time and data is returned starting at 00:00 local-time." Thực tế (agent chạy): mọi phản hồi đúng 24 dòng/ngày,
   một `utc_offset_seconds=-14400` cho cả khoảng (kể cả mùa đông), có dòng 02:00 ngày 10/3 không tồn tại, không có
   giờ lặp ngày 3/11. Issue #1764: offset là "the UTC offset at the time the request is made, instead of the correct
   offset(s) for the requested date range". → **Khoá luôn tải `timezone=UTC`** (danh mục đã chốt).
5. **Mặc định khi gặp giờ DST khác nhau giữa công cụ [CHẠY]:**
   - pandas 3.0.5 `tz_localize` giờ không tồn tại → `ValueError: 2024-03-10 02:30:00 is a nonexistent time due to
     daylight savings time.` (pandas 2.3.3: `NonExistentTimeError`); giờ mơ hồ → `ValueError: Cannot infer dst time…`
   - polars 1.44.2 mặc định raise: `ComputeError: datetime '2024-11-03 01:30:00' is ambiguous in time zone
     'America/New_York'.` `ambiguous` nhận 'earliest'/'latest'/'null'; `non_existent` chỉ 'raise'/'null' (không có dời).
   - DuckDB 1.5.5 `timezone('America/New_York', ts)` **không báo lỗi**: 02:30 ngày 10/3 → 07:30Z (trùng với 03:30);
     01:30 ngày 3/11 → 06:30Z (chọn EST). Docs: "Use the date parts of the timestamp in GMT to construct a timestamp in
     the given time zone. Effectively, the argument is a 'local' time."
   - DuckDB mặc định `TimeZone` = múi giờ hệ điều hành (máy Việt Nam: Asia/Ho_Chi_Minh).
6. **pandas 2.3.3 vs 3.0.5 [CHẠY]:** `date_range(..., freq='h', tz=NY)` cho ngày 10/3 và 3/11 ra 23/25 mốc ở cả hai
   bản (`datetime64[ns, …]` vs `datetime64[us, …]`); `to_datetime` offset lẫn lộn không `utc=True`: 2.3.3 FutureWarning,
   3.0.5 `ValueError: Mixed timezones detected. Pass utc=True…`; đối tượng múi giờ pytz vs zoneinfo. User guide 3.0.5
   vẫn viết "Olson time zone strings will return pytz time zone objects by default" — mâu thuẫn với chạy thật.
7. **`label`/`closed` mặc định** — user guide: "The default values for label and closed is 'left' for all frequency
   offsets except for 'ME', 'YE', 'QE', 'BME', 'BYE', 'BQE', and 'W' which all have a default of 'right'. This might
   unintendedly lead to looking ahead, where the value for a later time is pulled back to a previous time".
8. **Sự kiện → chuỗi đều [CHẠY, giống nhau hai bản pandas]:** `asfreq('h')` neo lưới ở mốc đầu và bỏ giá trị không
   nằm trên lưới; `resample('h').sum()` cho giờ trống = 0; `.mean()` = NaN; `resample` chỉ phủ từ sự kiện đầu tới cuối.
   Docs `asfreq`: "the new index will be equivalent to pd.date_range(start, end, freq=freq) where start and end are,
   respectively, the min and max entries in the original index."
9. **`merge_asof` direction [CHẠY]:** trái 10:00, 11:00; phải 09:30, 10:30, 11:00 → backward [9, 11], forward [10, 11]
   (kéo tương lai), `allow_exact_matches=False` [9, 10].
10. **Bấm giờ [CHẠY trên máy soạn, tệp tháng 3, trung vị 7 lần sau 1 lần làm nóng]:** pandas đọc mọi cột 0,167 s;
    pandas chỉ cột cần 0,073 s; polars `scan_parquet` 0,028 s; DuckDB SQL trên tệp 0,056 s. Giới hạn 4 nhân (`taskset
    -c 0-3`, `POLARS_MAX_THREADS=4`, `SET threads=4`): 0,177 / 0,074 / 0,026 / 0,045 s. Benchmark lớn (db-benchmark
    2026-08-17, groupby 1e8 dòng, máy 16 nhân): duckdb 1.5.4 2,75 s, polars 1.42.1 5,40 s; pandas 2.2.3 chạy lần cuối
    2025-02-10. Caveat trích: "Solutions are using in-memory data storage to achieve best timing".
11. **Ghép thời tiết lệch múi giờ [CHẠY]:** ghép số chuyến theo giờ địa phương naive với giờ UTC của Open-Meteo → giờ
    nóng nhất trung bình tháng 3 là **20h**; ghép đúng (cùng UTC) → **16h**. Tương quan mưa–số chuyến cùng giờ sau khi
    khử mùa vụ giờ-trong-tuần: **−0,100** (lệch) vs **+0,136** (đúng).
12. **Dạng dài [CHẠY]:** tháng 3 có 259 khu vực đón khách (bảng tra 265); lưới chung 743 giờ UTC → 192.437 dòng, 53,7% ô
    bằng 0 — chuỗi thưa.

## Điểm lệch so với lộ trình và quyết định

| Điểm lệch | Mức | Quyết định |
|---|---|---|
| Lộ trình "Đọc dữ liệu chuyến taxi NYC 1 tháng" + "tìm 2 ngày đổi DST" — một tháng không chứa cả hai ngày đổi DST | nhỏ | Dùng tháng 3 và tháng 11/2024; thêm hai tệp vào danh mục |
| Lộ trình "thấy mưa 'gây ra' tăng chuyến 5 giờ trước khi mưa" — tháng 3–11 lệch 4 giờ (EDT); tương quan mưa theo trễ bị mưa kéo dài làm nhiễu | nhỏ | Triệu chứng chính: "New York nóng nhất lúc 20h" (rõ, kiểm được); tương quan mưa đổi dấu làm ví dụ phụ, không diễn giải nhân quả |
| Lộ trình "263 khu vực" | nhỏ | Bảng tra có 265 khu vực, tháng 3 có 259 khu vực đón khách — dùng số thật |
| Open-Meteo `timezone=` sai quanh DST | nhỏ (thêm vào Lỗi thường gặp) | Luôn tải UTC; nêu trong tài liệu |
| Giờ lặp DST của dữ liệu sự kiện không khôi phục được EDT/EST | thiết kế | `chuan_hoa_thoi_gian` đánh dấu mốc UTC liên quan là NaN ("không biết"), ghi số dòng bỏ vào `attrs` (9.869) |
