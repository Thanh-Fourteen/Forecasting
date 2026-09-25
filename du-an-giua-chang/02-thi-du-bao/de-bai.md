# Dự án giữa chặng 2 — Thi dự báo trên dữ liệu tương lai

Làm nhóm 2 người (tự học thì làm một mình), 2 tuần, sau buổi 24. Chấm 100 điểm, thưởng tối đa +5, theo `RUBRIC.md` (đọc trước khi bắt
đầu). Đạt dự án này là đạt cột mốc M3: dự báo nhiều chuỗi bằng máy học, thắng mô hình thống kê trên dữ liệu chưa ai thấy.

## 1. Bài toán

Dự báo **nhu cầu điện theo giờ trong 168 giờ tới** (7 ngày) cho 5 vùng điều độ của Mỹ. Một **vùng điều độ** (balancing authority) là đơn
vị giữ cân bằng cung – cầu điện cho một khu vực; mỗi giờ họ báo nhu cầu thực tế cho Cơ quan Thông tin Năng lượng Mỹ (EIA), biểu mẫu EIA-930.

| Mã | Vùng | Thành phố lấy nhiệt độ | Nhu cầu trung bình 2025 (MW) |
|---|---|---|---|
| CISO | California | Los Angeles | 25.593 |
| ERCO | Texas | Dallas | 55.717 |
| MISO | Trung Tây | Indianapolis | 75.706 |
| NYIS | New York | New York | 17.300 |
| PJM | Trung Đại Tây Dương | Philadelphia | 96.295 |

**Đối thủ thật.** Mỗi vùng tự công bố một **dự báo day-ahead** (dự báo cho ngày mai, lập hôm nay) trong cùng bộ dữ liệu, cột `df`. Đây là
dự báo của người làm nghề, có dữ liệu và thời tiết tốt hơn bạn, và chỉ phải nhìn trước 1 ngày. Trên 8 tuần backtest cuối năm 2025, `df` có MASE
0,2–0,45 ở bốn vùng ngoài CISO (MASE: định nghĩa ở đầu RUBRIC.md). Riêng CISO, `df` thấp hơn thực tế trung bình khoảng 6,5% (lệch hệ thống, có thật trong dữ liệu 2025).

**Vì sao chấm trên tương lai.** Dữ liệu dùng để chấm **chưa tồn tại lúc bạn nộp**. Không ai nhìn được đề, không ai tune được trên đề. Điểm
cao chỉ có một cách: backtest trung thực. Rubric chấm riêng độ trung thực đó (phần B).

## 2. Luật thời gian

- **Mốc** = thứ Hai 00:00 UTC (7:00 sáng thứ Hai giờ Việt Nam). Nộp **trước** mốc.
- Dự báo đúng 168 giờ: EIA ghi nhãn **cuối giờ** theo UTC, nên các nhãn là mốc + 1 giờ … mốc + 168 giờ.
- Lúc mốc, bạn chỉ được dùng:
  - nhu cầu tới **mốc − 48 giờ** (tệp EIA dựng lại mỗi ngày, trễ khoảng 1,5 ngày);
  - nhiệt độ thật tới mốc;
  - nhiệt độ **đã dự báo**, tải trước mốc, cho 168 giờ sau mốc.
- `df` (dự báo của vùng) của tuần cần dự báo là đối thủ, **không** được làm đầu vào.
- Nộp **hai tuần liên tiếp**. Mỗi tuần chấm sớm nhất vào thứ Sáu sau khi tuần đó kết thúc: EIA trễ 1,5 ngày, và vùng điều độ được sửa số trong 3
  ngày. Lỗi lớn được sửa tới 30 ngày sau, nên giám khảo có thể chấm lại; lần chấm sau thay lần trước.

## 3. Dữ liệu

| Nguồn | Nằm ở | Cố định? |
|---|---|---|
| EIA-930, 1/2024 → 12/2025 | `lab/du-lieu/raw/eia930-balance-*` (do `python lab.py up` tải, kiểm sha256) | có |
| Open-Meteo, dự báo lưu trữ, 1/2024 → 12/2025 | `lab/du-lieu/raw/open-meteo-du-bao-luu-*` | có |
| EIA-930 và Open-Meteo từ 1/1/2026 tới lúc tải | `lab/du-lieu/moi/` (do `cong-cu/nop.py` tải; giờ tải và sha256 ghi ở `NHAT-KY.jsonl`) | không: EIA sửa số lùi |

`cong-cu/du_lieu.py` đọc tất cả thành hai bảng:

- `doc_lich_su()`: `vung`, `ds` (UTC, nhãn cuối giờ), `y` (nhu cầu thực tế, MW), `df` (dự báo day-ahead của vùng, MW).
- `doc_thoi_tiet()`: `vung`, `ds`, `thuc`, `truoc_1` … `truoc_7` (°C).

**Nhiệt độ thật và nhiệt độ đã dự báo.** `thuc` là giá trị sát thực tế, chỉ biết **sau** giờ đó. `truoc_K` là giá trị đã được dự báo
**trước 24 × K giờ**. Luật của dự án: giờ thứ $h$ sau mốc dùng `truoc_K` với $K = \lceil h/24 \rceil$ (làm tròn lên). Ví dụ giờ thứ 30: $K$ = 2,
dự báo phát hành 48 giờ trước giờ đó, tức 18 giờ trước mốc, nên lúc mốc đã có. Hàm `dl.dau_vao(lich_su, thoi_tiet, moc)` dựng sẵn đúng đầu vào
này. Trên 2024–2025 ở Los Angeles, `truoc_1` lệch `thuc` trung bình 1,3 °C, `truoc_7` lệch 3,1 °C: dự báo càng xa càng kém, và backtest phải chịu
đúng mức kém đó.

## 4. Nộp gì

```
code/du_bao.py            mô hình của bạn — giữ nguyên tên và tham số của du_bao, backtest, dac_trung
nop/<nhom>/<moc>/         do cong-cu/nop.py sinh ra, mỗi tuần một thư mục (không sửa tay)
nop/<nhom>/bao-cao.md      báo cáo, tối đa 3 trang — viết sau khi chấm cả hai tuần
```

- `du_bao(lich_su, thoi_tiet, moc)` → bảng `vung`, `ds`, `du_bao`: đúng 5 vùng × 168 giờ.
- `backtest(lich_su, thoi_tiet_luu, cac_moc)` → bảng `vung`, `moc`, `ds`, `h`, `y`, `du_bao`, `nhiet_do`; `nhiet_do` là nhiệt độ bạn đã đưa vào
  mô hình cho giờ đó. `nop.py` gọi nó với 8 mốc thứ Hai gần nhất trước mốc nộp (`dl.cac_moc_backtest`).
- `dac_trung(df)`: mọi đặc trưng lấy từ nhu cầu chỉ dùng nhu cầu tới `ds` − 216 giờ (48 giờ trễ + 168 giờ tầm dự báo).

`nop.py` ghi vào thư mục nộp: `du-bao.csv`, `backtest.csv`, `dau-vao.parquet` (đúng đầu vào đã dùng, để chạy lại), `bien-ban.json` (giờ tạo UTC,
sha256 của từng tệp và của code). **Gửi sha256 của `du-bao.csv` cho nhóm hoặc giảng viên trước mốc** (tin nhắn, email, commit git đã đẩy
lên). Tự học một mình thì commit và đẩy lên kho git của bạn trước mốc: giờ commit trên máy chủ là bằng chứng.

**Báo cáo** (`nop/<nhom>/bao-cao.md`):

1. **Bậc thang** trên backtest 8 tuần: seasonal naive → hồi quy có nhiệt độ → LightGBM global → ensemble. Một bảng MASE theo vùng, và một câu cho
   mỗi nấc: nấc này thêm gì, lợi bao nhiêu.
2. **Backtest so với thực tế**, sau khi chấm cả hai tuần: MASE thật so với MASE backtest, theo vùng. Chênh lệch từ đâu (thời tiết bất thường, ngày
   lễ, số liệu chưa sửa, mô hình học lệch)?
3. **So với `df`** của vùng: thua ở đâu, thắng ở đâu, vì sao.
4. Việc sẽ làm tiếp nếu có thêm một tuần.

## 5. Bắt đầu

```bash
cd lab && python lab.py up         # một lần: môi trường + dữ liệu 2024–2025 (~190 MB)
python lab.py check                # bộ chấm tối thiểu: lúc đầu đỏ 2/6
python lab.py chay ../code/du_bao.py                                      # backtest 8 tuần của khung
python lab.py chay ../cong-cu/nop.py --moc 2026-09-07 --thu-qua-khu       # tập nộp với một mốc đã qua (không tính điểm)
python lab.py chay ../cong-cu/nop.py --moc <thứ Hai tới> --nhom <ten>     # nộp thật, trước mốc
python lab.py chay ../cong-cu/cham.py --moc <mốc> --nhom <ten>            # chấm, từ thứ Sáu sau tuần đó
python lab.py chay ../cong-cu/bang_xep_hang.py                            # bảng xếp hạng mọi nhóm trong nop/
```

Nhiều nhóm thi cùng nhau thì chép thư mục `nop/<nhom>/` của mọi nhóm vào một chỗ rồi chạy `bang_xep_hang.py --ra <chỗ đó>`.

**Khung `code/du_bao.py`** có sẵn hai nấc đầu (seasonal naive, hồi quy có nhiệt độ) và **một chỗ hở cố ý** trong `backtest`: triệu chứng là
`python lab.py check` đỏ ở `test_thoi_tiet_backtest_la_du_bao` và `test_backtest_chi_dung_qua_khu`. Tìm và sửa trước khi làm gì khác: mọi con số
backtest trước khi sửa đều đẹp giả tạo.

`python lab.py check` chỉ kiểm mức sàn (định dạng, rò rỉ, tái lập). Xanh là điều kiện cần để nộp, chưa phải điểm cao.

## 6. Gợi ý (đọc khi bí)

- LightGBM một mô hình chung cho cả 5 vùng: chia nhu cầu cho mức gần đây của từng vùng để 5 vùng cùng thang (buổi 22).
- Nhu cầu điện phản ứng với nóng (điều hoà) và lạnh (sưởi) theo hai chiều khác nhau: tách nhiệt độ thành hai phần quanh khoảng 18 °C.
- Ensemble định sẵn trước khi nhìn kết quả tuần thật; đừng chọn thành phần theo điểm của chính 8 tuần backtest rồi báo cáo con số đó (buổi 24).
- Ngày lễ Mỹ (Lao động, Lễ Tạ ơn, Giáng sinh) làm nhu cầu giống Chủ nhật; seasonal naive lặp lại tuần có lễ thì tuần sau sai.
- Chỉ một thành phố cho cả vùng là thô, nhất là California và Trung Tây. Thêm điểm thời tiết được (cùng API, cùng luật `truoc_K`), ghi vào báo cáo.
- Nguồn EIA ngừng cập nhật thì báo giảng viên: giám khảo chấm bằng tuần gần nhất còn dữ liệu, hoặc lấy qua EIA API v2 (cần khoá miễn phí).
