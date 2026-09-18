# Rubric — Dự án giữa chặng 1 (100 điểm)

Học viên được xem rubric này từ đầu. Giám khảo chấm theo đúng thứ tự dưới đây.

## A. Phát hiện lỗi cài sẵn — 30 điểm (chấm tự động)

Chạy: `python giam-khao/cham_phat_hien.py <bài nộp>/bao-cao-loi.json`

| Tiêu chí | Điểm |
|---|---|
| Đúng **loại** lỗi | 3 / lỗi |
| Đúng **tệp và cột** | 1 / lỗi |
| Đúng **khoảng thời gian** (±3 ngày) | 1 / lỗi |
| Báo lỗi **không có thật** | −2 mỗi cái, trừ tối đa −6 |

Sáu lỗi × 5 điểm = 30. Bằng chứng trống (`bang_chung` rỗng) không bị trừ ở phần này nhưng sẽ bị trừ ở phần B.

## B. Chất lượng EDA và lập luận — 25 điểm (giám khảo đọc)

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| Bộ biểu đồ chẩn đoán đủ ba nguồn | 5 | có chuỗi, phân phối, ACF, theo giờ/tháng; trục có đơn vị; tiêu đề nói kết luận |
| Phân rã và đọc mùa vụ | 4 | STL/MSTL cho ít nhất một chuỗi; nói được mùa vụ ngày và năm, kèm số |
| **Tương quan chéo có prewhitening** | 6 | so tương quan thô và tương quan sau prewhitening; giải thích vì sao khác nhau |
| Bảng chất lượng dữ liệu | 4 | tự sinh; có dtype, thiếu mốc, độ phân giải, đoạn đứng yên, giá trị trá hình |
| **Mỗi nhận xét có bằng chứng** | 6 | không có câu "có vẻ như…" mà thiếu hình/số; mọi con số đều tái lập được |

Trừ điểm: mỗi kết luận không có bằng chứng −1 (tối đa −6).

## C. Pipeline làm sạch + test — 25 điểm

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| `python lab.py check` xanh | 10 | bộ chấm tối thiểu của dự án (xem `lab/cham/`) |
| Test riêng cho từng quy tắc | 10 | ≥ 8 test, mỗi quy tắc làm sạch có ít nhất một test; test **thất bại được** (thử phá dữ liệu để chứng minh) |
| Đánh giá cách điền bằng che nhân tạo | 5 | so ≥ 4 phương pháp trên **cả** che điểm và che khối; chọn theo độ dài lỗ, không chọn một cách cho mọi lỗ |

Trừ điểm: xoá dòng thay vì đánh dấu −3; điền lỗ dài không giới hạn −3; không có cột cờ −3.

## D. Chống rò rỉ — 10 điểm

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| Bộ feature qua bài kiểm rò rỉ | 5 | `kiem_ro_ri` + kiểm nhiễu mục tiêu, cả hai sạch, có log kèm theo |
| Bảng "biết trước bao lâu" | 3 | mọi feature phân loại được; không cột nào thuộc nhóm "không biết trước" |
| Baseline để đối chiếu | 2 | seasonal naive trên cùng tập kiểm, cùng chỉ số |

Trừ điểm: dùng nhiệt độ thật của giờ cần dự báo −5; chuẩn hoá trên toàn bộ dữ liệu −3.

## E. Trình bày — 10 điểm

| Tiêu chí | Điểm |
|---|---|
| Báo cáo gọn, có mở đầu và kết luận hành động được | 3 |
| Hình đạt chuẩn (tiêu đề nói kết luận, trục có đơn vị, đọc được khi in đen trắng) | 3 |
| **Nhật ký quyết định** đầy đủ: làm gì · vì sao · ảnh hưởng bao nhiêu dòng | 4 |

## Điểm thưởng (tối đa +5, không vượt 100)

- Phát hiện một vấn đề **có thật trong dữ liệu gốc** mà đề bài không cài (ví dụ độ phân giải 1 °C của trạm Nội Bài, cột rỗng 100%,
  giá trị trần) kèm bằng chứng: +2.
- Viết được một bài kiểm tự động phát hiện lỗi **dời nhãn thời gian** (không phải làm bằng mắt): +3.

## Mức điểm

| Điểm | Ý nghĩa |
|---|---|
| ≥ 85 | Sẵn sàng làm dữ liệu cho một hệ thống thật |
| 70–84 | Vững; còn thiếu vài kiểm tra hoặc lập luận |
| 55–69 | Làm được việc nhưng bỏ sót lỗi quan trọng hoặc chưa truy vết được |
| < 55 | Cần làm lại: thường là làm sạch bằng cảm tính, không có bằng chứng, hoặc có rò rỉ |
