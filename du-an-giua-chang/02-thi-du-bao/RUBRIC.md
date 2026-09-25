# Rubric — Dự án giữa chặng 2 (100 điểm, thưởng tối đa +5)

`cong-cu/cham.py` tính tự động phần A, B, 12 điểm của C, 8 điểm của D và điểm thưởng, ghi vào `ket-qua.json` của từng tuần. Giám khảo chấm
phần còn lại. A, B và điểm thưởng lấy trung bình hai tuần; tuần nào không nộp, nộp sau mốc, hoặc tệp bị sửa sau khi nộp (sha256 lệch
`bien-ban.json`) thì A, B của tuần đó bằng 0.

**Hai chỉ số dùng dưới đây.** MAE: trung bình trị tuyệt đối của (thực tế − dự báo), MW. MASE của một vùng: MAE chia cho MAE của "lặp lại tuần
trước" trên 8 tuần biết được lúc mốc. Tính riêng từng vùng, rồi lấy trung bình 5 vùng.

## A. Sai số trên dữ liệu tương lai — 35 điểm (tự động)

$r$ = MAE của bạn ÷ MAE của seasonal naive **trên chính tuần đó**, tính từng vùng rồi lấy trung bình 5 vùng. Seasonal naive ở đây: mỗi giờ lấy
cùng giờ tuần trước; giờ đó chưa biết lúc mốc (trễ 48 giờ) thì lấy cùng giờ hai tuần trước. So với seasonal naive cùng tuần để một tuần thời tiết bất thường không làm mọi nhóm mất điểm như nhau.

| $r$ | Điểm |
|---|---|
| ≤ 0,60 | 35 |
| từ 0,60 tới 1,00 | giảm đều từ 35 về 0 |
| ≥ 1,00 (không hơn lặp lại tuần trước) | 0 |

Lời giải mẫu của giám khảo được $r$ ≈ 0,68 trên hai tuần tập 31/8 và 7/9/2026.

## B. Trung thực của backtest — 20 điểm (tự động)

$q$ = MASE thật của tuần ÷ MASE trung bình 8 tuần backtest nộp kèm. Backtest trung thực thì $q$ gần 1.

| Mức lệch | Điểm |
|---|---|
| $q$ trong khoảng 0,8 – 1,25 | 20 |
| xa hơn, tới $q$ = 0,5 hoặc 2 | giảm đều về 0 (tính theo $\lvert \ln q \rvert$) |
| $q \le$ 0,5 hoặc $q \ge$ 2 | 0 |

Hai chiều đều mất điểm: backtest quá đẹp (rò rỉ, chọn trên chính backtest) làm $q$ lớn; backtest quá tệ làm $q$ nhỏ.

## C. Tái lập — 20 điểm

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| Chạy lại ra đúng dự báo (tự động) | 12 | `cham.py` chạy lại `du_bao` trên `dau-vao.parquet` đã lưu, lệch lớn nhất ≤ 1 MW |
| Một lệnh từ môi trường trắng (giám khảo) | 8 | `python lab.py up` rồi một lệnh `nop.py` sinh lại đủ thư mục nộp; seed ghi trong code; không bước làm tay |

## D. Chống rò rỉ — 15 điểm

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| Thời tiết trong backtest là thời tiết đã dự báo (tự động) | 8 | cột `nhiet_do` của `backtest.csv` khớp `truoc_⌈h/24⌉` (trung vị lệch ≤ 0,05 °C) |
| Test rò rỉ của bộ chấm | 4 | `test_dac_trung_khong_ro_ri` và `test_backtest_chi_dung_qua_khu` xanh |
| Bảng "biết trước bao lâu" (giám khảo) | 3 | mọi đầu vào của mô hình có một dòng: lấy từ đâu, biết trước mốc bao lâu |

Dùng `df` của tuần cần dự báo làm đầu vào: phần D = 0 và bài không vào bảng xếp hạng.

## E. Báo cáo — 10 điểm (giám khảo)

| Tiêu chí | Điểm | Đạt khi |
|---|---|---|
| Bậc thang 4 nấc trên backtest 8 tuần | 4 | bảng MASE theo vùng cho seasonal naive, hồi quy có nhiệt độ, LightGBM global, ensemble; mỗi nấc một câu |
| Backtest so với thực tế | 3 | chênh lệch từng vùng có số và có nguyên nhân kiểm được |
| So với `df`, việc làm tiếp | 3 | nói rõ thua/thắng ở vùng nào, vì sao; việc tiếp theo cụ thể |

## Điểm thưởng (tổng không vượt 100)

+1 cho mỗi vùng mà MAE cả tuần của bạn thấp hơn MAE của `df` trên cùng các giờ, tối đa +5, trung bình hai tuần. `df` chỉ phải dự báo trước 1 ngày,
bạn phải dự báo trước tới 9 ngày: thắng được là thắng thật.

## Mức điểm

| Điểm | Ý nghĩa |
|---|---|
| ≥ 85 | dự báo và quy trình đủ tin để một đơn vị thật tham khảo |
| 70–84 | vững; mô hình hoặc backtest còn lệch ở vài vùng |
| 55–69 | chạy được nhưng backtest chưa trung thực hoặc thua seasonal naive ở nhiều vùng |
| < 55 | làm lại: thường do rò rỉ thời tiết, backtest chọn trên chính nó, hoặc không tái lập được |
