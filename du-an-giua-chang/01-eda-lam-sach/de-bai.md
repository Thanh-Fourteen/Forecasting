# Dự án giữa chặng 1 — EDA và pipeline làm sạch

Làm cá nhân, 1 tuần, sau buổi 13. Nộp một thư mục mang tên bạn. Chấm 100 điểm theo `RUBRIC.md` (đọc trước khi bắt đầu).

## 1. Bối cảnh

Bạn nhận bàn giao ba nguồn dữ liệu khí tượng để chuẩn bị cho một hệ thống dự báo nhiệt độ:

| Tệp trong `phat/du-lieu/` | Nguồn | Một dòng mỗi | Khoảng thời gian |
|---|---|---|---|
| `noi-bai.csv` | trạm quan trắc sân bay Nội Bài (NOAA GHCNh) | 30 phút | 1/2024 → 12/2025 |
| `ha-noi.csv` | tái phân tích ERA5 cho Hà Nội (Open-Meteo) | 1 giờ | 1/2023 → 12/2024 |
| `tphcm.csv` | tái phân tích ERA5 cho TP. Hồ Chí Minh (Open-Meteo) | 1 giờ | 1/2023 → 12/2024 |

Dữ liệu là dữ liệu thật, có sẵn những vấn đề thật (thiếu mốc, cột rỗng, cảm biến làm tròn thô…). Ngoài ra, người ra đề đã **cài thêm 6 lỗi**,
mỗi loại một lỗi: đổi đơn vị, cảm biến đứng yên, lệch múi giờ, dòng trùng lặp, ngày giả toàn số 0, một đoạn bị dời nhãn thời gian. Bạn không
biết lỗi nằm ở tệp nào, cột nào, khoảng nào. Một trong sáu lỗi không tạo NaN, không tạo giá trị vô lý: chỉ so chéo giữa các nguồn mới thấy.

Trong thực tế không có bản sạch để so. Vì vậy **không** dùng dữ liệu gốc (`lab/du-lieu/raw/`, do `python lab.py up` tải về) để tìm lỗi:
bằng chứng phải tính từ chính dữ liệu phát. Lỗi chỉ tìm được nhờ so với bản gốc thì không được điểm.

## 2. Nộp gì

```
<ten-ban>/
  bao-cao-eda.ipynb  + bao-cao-eda.pdf   báo cáo EDA (mục 2.1)
  bao-cao-loi.json                      sáu lỗi bạn tìm được (mục 2.2)
  lam_sach.py                           pipeline làm sạch (mục 2.3)
  feature.py                            bộ feature đã qua kiểm rò rỉ (mục 2.4)
  nhat-ky.md                            nhật ký quyết định (mục 2.5)
  lab/cham/test_*.py                    test của riêng bạn
```

`lam_sach.py` và `feature.py` viết tiếp từ khung trong `code/`: giữ nguyên tên và tham số các hàm, vì bộ chấm gọi chúng.

### 2.1 Báo cáo EDA

Mỗi nhận xét có một hình hoặc một con số làm bằng chứng. Tối thiểu:

- bộ biểu đồ chẩn đoán cho từng nguồn: chuỗi theo thời gian, phân phối, ACF, trung bình theo giờ trong ngày và theo tháng (buổi 4, 7);
- phân rã STL cho ít nhất một chuỗi, nói mùa vụ ngày và năm lớn bao nhiêu (buổi 6);
- tương quan chéo giữa các nguồn, **trước và sau prewhitening** (buổi 8), giải thích vì sao hai con số khác nhau;
- bảng chất lượng dữ liệu tự sinh từ code: kiểu dữ liệu, tỷ lệ thiếu, dải giá trị, độ phân giải, đoạn đứng yên, mốc trùng (buổi 10).

### 2.2 Báo cáo lỗi — `bao-cao-loi.json`

Máy chấm đọc tệp này, nên giữ đúng định dạng. Ví dụ dưới **chỉ minh hoạ định dạng**, không phải một lỗi có thật:

```json
{"loi": [
  {"loai": "cam_bien_dung_yen", "tep": "ha-noi", "cot": "relative_humidity_2m",
   "tu": "2023-02-10", "den": "2023-02-12",
   "bang_chung": "độ ẩm giữ đúng 91,0 trong 60 giờ liền; bình thường đổi mỗi giờ"}
]}
```

- `loai`: một trong `doi_don_vi`, `cam_bien_dung_yen`, `lech_mui_gio`, `dong_trung_lap`, `ngay_gia_0`, `doi_nhan_thoi_gian`.
- `tep`: `noi-bai`, `ha-noi` hoặc `tphcm`. `cot`: tên cột; lỗi ảnh hưởng mọi cột thì ghi `"*"`.
- `tu`, `den`: ngày đầu và ngày cuối bị ảnh hưởng (định dạng năm-tháng-ngày); lệch bao nhiêu ngày vẫn được điểm: `RUBRIC.md` mục A.
- `bang_chung`: một câu, có số.

Báo lỗi **không có thật** bị trừ điểm (`RUBRIC.md` mục A): chỉ báo lỗi bạn có bằng chứng.

### 2.3 `lam_sach.py`

Hàm `lam_sach(bang, ten_nguon)` trả về bảng:

- chỉ số thời gian đều, tăng dần, không trùng, theo UTC; **không mất mốc nào** (thiếu thì thêm mốc với giá trị NaN, không xoá dòng);
- đã xử lý giá trị trá hình, cảm biến đứng yên, ngoại lai (Hampel, buổi 11), ngày giả;
- chỉ điền lỗ ngắn; lỗ dài hơn `gioi_han_dien` bước để NaN;
- có ba cột cờ: `da_dien` (giá trị do bạn điền), `nghi_ngo` (giá trị bị nghi là sai), `lo_dai_bo_trong` (thuộc lỗ dài, cố ý để trống).

Hàm `so_sanh_dien` chọn cách điền bằng che nhân tạo (buổi 10): ít nhất 2 kiểu che (che điểm, che khối) × 4 cách điền, ra bảng MAE.

Test của bạn đặt trong `lab/cham/`: mỗi quy tắc làm sạch ít nhất một test, và test phải **đỏ được** khi bạn cố ý phá dữ liệu.

### 2.4 `feature.py`

Bài toán: dự báo nhiệt độ Nội Bài **12 giờ tới**, tức 24 bước 30 phút (hằng `TAM = 24` trong khung). Cần:

- ít nhất 20 feature, qua cả bài kiểm cắt tương lai (`kiem_ro_ri`) lẫn kiểm nhiễu mục tiêu (buổi 13; khung chưa có hàm này, bạn tự thêm);
- bảng "biết trước bao lâu" cho từng feature;
- baseline seasonal naive (chu kỳ 1 ngày = 48 bước): MAE dự báo 12 giờ tới trên phần cuối chuỗi Nội Bài đã làm sạch, ghi rõ mốc chia.

Kết quả hai bài kiểm rò rỉ và MAE baseline in trong báo cáo EDA.

### 2.5 Nhật ký quyết định — `nhat-ky.md`

Mỗi bước làm sạch một dòng: làm gì · vì sao · ảnh hưởng bao nhiêu dòng · bằng chứng ở đâu (hình, số). Giám khảo đọc phần này kỹ nhất: một
pipeline không giải thích được thì không ai dám dùng.

## 3. Bắt đầu

```bash
cd lab && python lab.py up     # một lần: môi trường
python lab.py check            # bộ chấm tối thiểu: lúc đầu đỏ toàn bộ vì khung chưa viết
```

`python lab.py check` chỉ kiểm mức sàn (đọc được ba nguồn, lưới đều, có cột cờ, không điền lỗ dài, feature qua kiểm rò rỉ…). Xanh là điều kiện
cần, chưa phải điểm cao. Được chép lại code của chính bạn từ buổi 10–13.

## 4. Gợi ý (đọc khi bí)

- Phần lớn lỗi lộ ra trong một bảng chất lượng dữ liệu làm đủ cột: dải giá trị, độ phân giải, đoạn đứng yên, mốc trùng, tỷ lệ số 0.
- Chia mỗi chuỗi thành từng tháng rồi so từng tháng: lỗi cài sẵn thường bắt đầu và kết thúc đột ngột.
- Nhiệt độ có nhịp ngày: giờ nóng nhất trong ngày không tự đổi giữa chừng.
- Hai nguồn đo cùng vùng thì lên xuống cùng nhau; một đoạn mà chúng thôi đi cùng nhau là chỗ phải xem kỹ.
- Đừng làm trơn dữ liệu trước khi tìm lỗi (buổi 12): làm trơn xoá mất chính dấu vết bạn cần.
