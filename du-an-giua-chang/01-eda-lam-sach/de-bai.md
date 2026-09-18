# Dự án giữa chặng 1 — EDA và pipeline làm sạch

**Cột mốc M1.** Làm cá nhân, 1 tuần. Nộp qua Git (một thư mục mang tên bạn).

## 1. Bối cảnh

Bạn vừa nhận bàn giao ba nguồn dữ liệu khí tượng để chuẩn bị cho một hệ thống dự báo nhiệt độ và độ ẩm:

| Tệp | Nguồn thật | Tần suất | Khoảng thời gian |
|---|---|---|---|
| `noi-bai.csv` | Trạm quan trắc **Nội Bài** (NOAA GHCNh, mã VMI0000VVNB) | 30 phút | 2024-01 → 2025-12 |
| `ha-noi.csv` | Tái phân tích **ERA5 Hà Nội** (Open-Meteo) | 1 giờ | 2023-01 → 2024-12 |
| `tphcm.csv` | Tái phân tích **ERA5 TP. Hồ Chí Minh** (Open-Meteo) | 1 giờ | 2023-01 → 2024-12 |

Đây là **dữ liệu thật**, với những vấn đề thật của nó (thiếu mốc, cột rỗng, giá trị trá hình, cảm biến đứng yên, độ phân giải thô…).

Ngoài ra, **người ra đề đã cài thêm 6 lỗi** vào dữ liệu. Bạn không được biết chúng là gì, ở đâu, hay thuộc loại nào. Chúng thuộc các nhóm
đã học ở buổi 10–13: đổi đơn vị, cảm biến đứng yên, lệch múi giờ, dòng trùng lặp, ngày giả toàn 0, một đoạn bị dời nhãn thời gian.

> Cảnh báo có thật: **một trong sáu lỗi không tạo ra NaN nào, không tạo ra giá trị vô lý nào, và không lọt bất kỳ kiểm tra dải giá trị
> nào.** Chỉ có so sánh chéo giữa ba nguồn mới thấy.

## 2. Việc phải làm

### 2.1 Báo cáo EDA (notebook + PDF)

Mỗi nhận xét **phải có bằng chứng** (hình hoặc số). Tối thiểu:

- Bộ biểu đồ chẩn đoán cho từng nguồn: chuỗi theo thời gian, phân phối, ACF, biểu đồ theo giờ/theo tháng.
- Phân rã STL cho ít nhất một chuỗi, kèm nhận xét về xu hướng và mùa vụ ngày/năm.
- **Tương quan chéo giữa ba nguồn**, có **prewhitening** (buổi 8) — tương quan thô giữa hai chuỗi cùng có nhịp ngày luôn cao giả tạo.
- Đặc trưng riêng của từng nguồn: độ phân giải cảm biến, tỷ lệ thiếu mốc, giá trị trá hình.
- Bảng chất lượng dữ liệu tự sinh (mẫu ở buổi 10).

### 2.2 Báo cáo lỗi cài sẵn — `bao-cao-loi.json`

Định dạng cố định (chấm tự động):

```json
{"loi": [
  {"loai": "doi_don_vi", "tep": "noi-bai", "cot": "temperature",
   "tu": "2025-04-01", "den": "2025-12-31",
   "bang_chung": "mức trung bình nhảy +45,2 tại 2025-04-01; biên độ ngày ×1,8"}
]}
```

- `loai`: một trong `doi_don_vi`, `cam_bien_dung_yen`, `lech_mui_gio`, `dong_trung_lap`, `ngay_gia_0`, `doi_nhan_thoi_gian`
  (từ đồng nghĩa hợp lý được chấp nhận).
- `tu` / `den`: khoảng bị ảnh hưởng, chấm đúng nếu lệch **≤ 3 ngày**.
- `bang_chung`: một câu, có **số**.

**Báo lỗi không có thật bị trừ 2 điểm mỗi cái** (trừ tối đa 6). Đừng "bắn đại cho trúng".

### 2.3 `lam_sach.py` + test

Pipeline phải:

- đưa mọi nguồn về **lưới thời gian đều**, xử lý mốc trùng, thống nhất **UTC**;
- phát hiện và xử lý: giá trị trá hình, cảm biến đứng yên, ngoại lai (Hampel), ngày giả;
- điền dữ liệu **có giới hạn độ dài lỗ**, chọn phương pháp bằng **che nhân tạo** (cả che điểm lẫn che khối), và
  **để lỗ dài là NaN**;
- sinh cột cờ `da_dien`, `nghi_ngo`, `lo_dai_bo_trong`;
- có test pytest riêng của bạn trong `lab/cham/` cho **từng quy tắc làm sạch**.

Bộ chấm chung (`make check`) kiểm các yêu cầu tối thiểu; test của bạn là phần cho điểm thêm về chất lượng.

### 2.4 Bộ feature đã qua kiểm rò rỉ

Ít nhất 20 feature cho bài toán "dự báo nhiệt độ Nội Bài 24 giờ tới", kèm:

- bảng **"biết trước bao lâu"** cho từng feature;
- kết quả `kiem_ro_ri` (cắt tương lai) và kiểm nhiễu mục tiêu — **phải sạch 100%**;
- một baseline seasonal naive để đối chiếu.

### 2.5 Nhật ký quyết định — `nhat-ky.md`

Mỗi bước làm sạch một dòng: **làm gì · vì sao · ảnh hưởng bao nhiêu dòng · bằng chứng nào**. Đây là thứ giám khảo đọc kỹ nhất; một pipeline
tốt mà không giải thích được thì không dùng được trong thực tế.

## 3. Nộp gì

```
<ten-ban>/
  bao-cao-eda.ipynb   (+ bao-cao-eda.pdf)
  bao-cao-loi.json
  lam_sach.py
  feature.py
  nhat-ky.md
  lab/cham/test_*.py     test của bạn
```

## 4. Chấm điểm (100)

| Phần | Điểm | Chấm thế nào |
|---|---|---|
| Phát hiện lỗi cài sẵn | **30** | tự động (`cham_phat_hien.py`): 5 điểm/lỗi = 3 đúng loại + 1 đúng tệp/cột + 1 đúng khoảng ±3 ngày; báo sai −2 |
| Chất lượng EDA và lập luận | **25** | giám khảo đọc: mỗi nhận xét có bằng chứng, đọc đúng biểu đồ, tương quan có prewhitening |
| Pipeline + test | **25** | `make check` xanh (10) + test riêng cho từng quy tắc (10) + đánh giá cách điền bằng che nhân tạo (5) |
| Chống rò rỉ | **10** | bộ feature qua bài kiểm rò rỉ; bảng "biết trước bao lâu" đầy đủ |
| Trình bày | **10** | báo cáo gọn, hình có tiêu đề nói kết luận, nhật ký quyết định rõ |

Chi tiết từng ô: `RUBRIC.md`.

## 5. Bắt đầu

```bash
cd lab && make up              # môi trường + dữ liệu gốc (để đối chiếu nếu cần)
make check                     # bộ chấm tối thiểu — đầu tuần sẽ ĐỎ
```

Dữ liệu phát (đã cài lỗi) nằm trong thư mục `phat/du-lieu/` mà giảng viên gửi kèm. **Không** dùng dữ liệu gốc trong `lab/du-lieu/raw/` để
"tránh" lỗi cài sẵn — mục đích của bài là **phát hiện** chúng. (Được phép dùng dữ liệu gốc như một nguồn đối chiếu, nhưng phải ghi rõ trong
nhật ký và vẫn phải mô tả bằng chứng phát hiện từ chính dữ liệu bẩn.)

## 6. Gợi ý (đọc khi bí)

- Bốn lỗi đầu tiên đều lộ ra trong **bảng chất lượng dữ liệu** của buổi 10 nếu bạn làm đủ: dtype, min/max, độ phân giải, đoạn đứng yên,
  mốc trùng, tỷ lệ giá trị đặc biệt.
- Lỗi múi giờ: vẽ **nhiệt độ trung bình theo giờ trong ngày** cho từng nửa dữ liệu. Đỉnh nhiệt ở Hà Nội rơi vào khoảng 7–8 h UTC.
- Lỗi dời nhãn: tính **tương quan trượt 7 ngày** giữa Nội Bài và Hà Nội. Một đoạn tụt hẳn so với phần còn lại là chỗ đáng ngờ; sau đó thử
  dịch chuỗi ±24 giờ xem tương quan có phục hồi không.
- Đừng quên buổi 12: nếu bạn làm trơn dữ liệu trước khi chấm, mọi con số sau đó đều vô nghĩa.
