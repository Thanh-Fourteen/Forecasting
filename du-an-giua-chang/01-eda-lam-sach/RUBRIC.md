# Rubric — Dự án giữa chặng 1 (100 điểm, thưởng tối đa +5)

## A. Phát hiện lỗi cài sẵn — 30 điểm (máy chấm `bao-cao-loi.json`)

Một mục được tính là **tìm thấy** khi đúng loại, đúng tệp, và khoảng `tu`–`den` chồng lên khoảng lỗi thật (nới thêm 3 ngày mỗi phía).

| Mỗi lỗi tìm thấy | Điểm |
|---|---|
| tìm thấy | 3 |
| đúng cột (lỗi ảnh hưởng mọi cột thì cột nào cũng đúng) | +1 |
| ngày đầu và ngày cuối đều lệch ≤ 3 ngày so với lỗi thật | +1 |

Mục nào không tìm thấy lỗi thật nào là **báo sai**: −2 mỗi mục, trừ tối đa 6. Báo cùng một lỗi hai lần chỉ tính một lần. Sáu lỗi × 5 = 30.

## B. EDA và lập luận — 25 điểm (giám khảo đọc)

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| Bộ biểu đồ chẩn đoán đủ ba nguồn | 5 | chuỗi, phân phối, ACF, theo giờ và theo tháng; trục có đơn vị; tiêu đề nói kết luận |
| Phân rã, đọc mùa vụ | 4 | STL cho ít nhất một chuỗi; mùa vụ ngày và năm có số |
| Tương quan chéo có prewhitening | 6 | có cả số trước và sau prewhitening; giải thích vì sao khác |
| Bảng chất lượng dữ liệu | 4 | sinh từ code; có kiểu dữ liệu, tỷ lệ thiếu, dải giá trị, độ phân giải, đoạn đứng yên, mốc trùng |
| Mỗi nhận xét có bằng chứng | 6 | mọi nhận xét kèm hình hoặc số, chạy lại code ra đúng số đó; mỗi nhận xét thiếu bằng chứng −1 |

## C. Pipeline làm sạch và test — 25 điểm

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| `python lab.py check` xanh | 10 | toàn bộ bộ chấm tối thiểu |
| Test của riêng bạn | 10 | ≥ 8 test; mỗi quy tắc làm sạch ít nhất một test; test đỏ khi cố ý phá dữ liệu |
| Chọn cách điền bằng che nhân tạo | 5 | ≥ 4 cách điền trên cả che điểm lẫn che khối; cách điền chọn theo độ dài lỗ |

Trừ: xoá dòng thay vì gắn cờ −3; điền lỗ dài không giới hạn −3; thiếu cột cờ −3.

## D. Chống rò rỉ — 10 điểm

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| Bộ feature qua kiểm rò rỉ | 5 | kiểm cắt tương lai và kiểm nhiễu mục tiêu đều sạch, kết quả in trong báo cáo |
| Bảng "biết trước bao lâu" | 3 | mọi feature xếp được vào một nhóm |
| Baseline | 2 | MAE seasonal naive 12 giờ tới trên phần cuối chuỗi Nội Bài, mốc chia ghi rõ |

Trừ: dùng nhiệt độ thật của giờ cần dự báo −5; chuẩn hoá bằng thống kê của cả chuỗi −3.

## E. Trình bày — 10 điểm

| Tiêu chí | Điểm |
|---|---|
| Báo cáo có mở đầu và kết luận nói được nên làm gì tiếp | 3 |
| Hình: tiêu đề nói kết luận, trục có đơn vị, in đen trắng vẫn đọc được | 3 |
| Nhật ký quyết định đủ: làm gì · vì sao · bao nhiêu dòng · bằng chứng | 4 |

## Điểm thưởng (tổng không vượt 100)

- +2: chỉ ra một vấn đề **có sẵn** trong dữ liệu thật mà đề không cài (ví dụ trạm Nội Bài làm tròn tới 1 °C), kèm bằng chứng.
- +3: một hàm trong `lam_sach.py` tự phát hiện đoạn bị dời nhãn thời gian, không cần nhìn bằng mắt.

## Mức điểm

| Điểm | Ý nghĩa |
|---|---|
| ≥ 85 | làm dữ liệu được cho một hệ thống thật |
| 70–84 | vững; thiếu vài kiểm tra hoặc lập luận |
| 55–69 | làm được việc nhưng bỏ sót lỗi quan trọng hoặc không truy vết được |
| < 55 | làm lại: thường do làm sạch theo cảm tính, thiếu bằng chứng, hoặc có rò rỉ |
