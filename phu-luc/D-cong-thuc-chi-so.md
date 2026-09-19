# Phụ lục D — Bảng công thức chỉ số đánh giá dự báo

Mỗi chỉ số có: công thức, một ví dụ 5 số tự tính tay, **khi nào dùng**, và **bẫy**. Mọi con số tính lại bằng NumPy 2.5.3 và SciPy
(2026-09-19); phần đối chiếu thư viện (mục 9) chạy với utilsforecast 0.2.16, scoringrules 0.11.0 (2026-09-17).

> **Trạng thái:** ví dụ trên dữ liệu thật của buổi 14 (chỉ số) và 15 (Diebold–Mariano) ở cuối mục 9; buổi 25 (dự báo xác suất) sẽ bổ sung.

**Ký hiệu** (theo sách FPP của Hyndman & Athanasopoulos, mục 5.8): $y_t$ là giá trị thật, $\hat y_t$ là dự báo, sai số
$e_t = y_t - \hat y_t$. Sai số **dương** nghĩa là dự báo **thấp** hơn thực tế. "mean" là trung bình trên các điểm được chấm.

**Ví dụ chung cho mục 2–3 và 7.** Năm ngày kiểm:

| Ngày | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| thật $y$ | 10 | 12 | 8 | 14 | 16 |
| dự báo $\hat y$ | 11 | 10 | 9 | 14 | 12 |
| sai số $e = y - \hat y$ | −1 | 2 | −1 | 0 | 4 |

**Đọc bảng.** Dự báo trượt nhiều nhất ở ngày 5 (thấp hơn thật 4 đơn vị); ngày 4 trúng khít.

## Mục lục

- [1. Chọn chỉ số theo quyết định](#1-chọn-chỉ-số-theo-quyết-định)
- [2. Dự báo điểm: MAE, RMSE, ME, MAPE, sMAPE, WAPE](#2-dự-báo-điểm-mae-rmse-me-mape-smape-wape)
- [3. Chỉ số chia thang: MASE, RMSSE](#3-chỉ-số-chia-thang-mase-rmsse)
- [4. Quantile và khoảng: pinball, Winkler, coverage, WIS](#4-quantile-và-khoảng-pinball-winkler-coverage-wis)
- [5. Phân phối: CRPS](#5-phân-phối-crps)
- [6. Xác suất sự kiện: Brier, log score](#6-xác-suất-sự-kiện-brier-log-score)
- [7. Skill score](#7-skill-score)
- [8. So hai mô hình: Diebold–Mariano](#8-so-hai-mô-hình-dieboldmariano)
- [9. Đối chiếu với thư viện](#9-đối-chiếu-với-thư-viện)
- [10. Thư viện tính khác nhau thế nào](#10-thư-viện-tính-khác-nhau-thế-nào)
- [Nguồn](#nguồn)

## 1. Chọn chỉ số theo quyết định

Mỗi chỉ số thưởng cho một con số khác nhau của phân phối dự báo. Gneiting (2011) cảnh báo: chọn chỉ số không khớp với việc cần làm thì
kết luận có thể sai hoàn toàn.

| Chỉ số | Dự báo tốt nhất theo chỉ số này là | Hợp khi |
|---|---|---|
| bình phương sai số (MSE, RMSE, RMSSE) | **trung bình** | sai lớn đắt hơn nhiều sai nhỏ; cần tổng đúng (cộng nhiều mặt hàng) |
| trị tuyệt đối sai số (MAE, MASE, WAPE) | **trung vị** | chi phí tỷ lệ với độ lệch, thiếu và thừa đắt như nhau |
| pinball mức $\tau$ | **quantile $\tau$** | thiếu và thừa đắt khác nhau (hết hàng đắt hơn tồn kho) |
| MAPE | một con số lệch về phía thấp | hầu như không nên dùng để chọn mô hình |
| CRPS, WIS, log score | **cả phân phối** | quyết định cần khoảng hoặc xác suất |

**Đọc bảng.** Nếu sếp trả tiền theo tổng sai số tuyệt đối thì chấm bằng MAE và dự báo trung vị; chấm bằng RMSE sẽ chọn nhầm mô hình dự báo
trung bình.

## 2. Dự báo điểm: MAE, RMSE, ME, MAPE, sMAPE, WAPE

| Chỉ số | Công thức | Ví dụ chung | Đơn vị |
|---|---|---|---|
| MAE | $\operatorname{mean}(\lvert e_t\rvert)$ | (1 + 2 + 1 + 0 + 4)/5 = **1,6** | như dữ liệu |
| RMSE | $\sqrt{\operatorname{mean}(e_t^2)}$ | $\sqrt{(1 + 4 + 1 + 0 + 16)/5} = \sqrt{4{,}4}$ ≈ **2,10** | như dữ liệu |
| ME (độ chệch) | $\operatorname{mean}(e_t)$ | (−1 + 2 − 1 + 0 + 4)/5 = **0,8** | như dữ liệu |
| MAPE | $\operatorname{mean}(100\,\lvert e_t / y_t\rvert)$ | mean(10; 16,7; 12,5; 0; 25) ≈ **12,8%** | % |
| sMAPE | $\operatorname{mean}\big(200\,\lvert e_t\rvert / (y_t + \hat y_t)\big)$ | ≈ **13,6** | thang 0–200 |
| WAPE | $\sum_t \lvert e_t\rvert \,/\, \sum_t \lvert y_t\rvert$ | 8 / 60 ≈ **0,133** | tỷ lệ |

**Đọc bảng.** RMSE (2,10) lớn hơn MAE (1,6) vì bình phương phóng to sai số 4 của ngày 5. ME dương: dự báo thấp hơn thực tế trung bình 0,8.

**MAE.** Dùng khi: báo cáo một con số dễ hiểu ("trung bình trượt 1,6 đơn vị") và chi phí tăng đều theo độ lệch. Bẫy: không so được giữa
hai chuỗi khác đơn vị; trên chuỗi bán lác đác (nhiều ngày 0), dự báo toàn 0 có thể được MAE thấp nhất.

**RMSE.** Dùng khi: một lần sai lớn gây hại hơn nhiều lần sai nhỏ (quá tải lưới điện), hoặc cần tổng dự báo đúng. Bẫy: một điểm ngoại lai
quyết định cả con số; bỏ ngày 5 thì RMSE còn $\sqrt{6/4}$ ≈ 1,22.

**ME.** Dùng khi: kiểm dự báo có lệch một phía có hệ thống không. Bẫy: sai dương và âm triệt tiêu nhau, nên ME = 0 không có nghĩa là dự báo
tốt; luôn báo kèm MAE. Thư viện utilsforecast gọi là `bias` và tính $\hat y - y$, ngược dấu (mục 10).

**MAPE.** Dùng khi: người đọc chỉ hiểu phần trăm, chuỗi luôn dương và xa số 0. Bẫy:

- $y_t$ = 0 thì chia cho 0; $y_t$ gần 0 thì một điểm làm MAPE vọt lên.
- Cùng lệch 5 đơn vị, thật 10 dự báo 5 cho 50%, còn thật 5 dự báo 10 cho 100%: chọn mô hình theo MAPE sẽ ưa mô hình dự báo thấp.
- Không dùng cho nhiệt độ °C: số 0 °C không có nghĩa "không có gì".

**sMAPE.** Tên "đối xứng" nhưng không đối xứng: thật 10, dự báo 5 cho 66,7; thật 10, dự báo 15 cho 40, nên ưa dự báo **cao**. Dự báo và thật
cùng bằng 0 thì chia 0/0. Hyndman & Koehler (2006) khuyên không dùng. Bẫy lớn nhất: ba thang cùng tên (0–200, 0–100, 0–1); luôn ghi công thức.

**WAPE.** Dùng khi: gộp nhiều mặt hàng thành một con số phần trăm mà không chia cho từng $y_t$ nhỏ; chịu được ngày có số 0. Bẫy: mặt hàng bán
chạy chiếm gần hết con số; tối ưu WAPE cũng cho dự báo trung vị. Còn gọi là tỷ số MAD/Mean (Kolassa & Schütz 2007).

## 3. Chỉ số chia thang: MASE, RMSSE

**Vấn đề.** MAE 1,6 là tốt hay tệ? Tuỳ chuỗi dao động nhiều hay ít. MASE chia MAE cho sai số của seasonal naive **trên tập huấn luyện** (phần học), nên so
được giữa các chuỗi khác đơn vị (Hyndman & Koehler 2006).

$$
\text{MASE} = \frac{\operatorname{mean}(\lvert e_j \rvert)}{\frac{1}{T-m}\sum_{t=m+1}^{T} \lvert y_t - y_{t-m} \rvert}
\qquad
\text{RMSSE} = \sqrt{\frac{\operatorname{mean}(e_j^2)}{\frac{1}{T-m}\sum_{t=m+1}^{T} (y_t - y_{t-m})^2}}
$$

- $T$: số điểm huấn luyện; $m$: chu kỳ mùa vụ ($m$ = 1 là naive, $m$ = chu kỳ là seasonal naive).

**Nói bằng lời.** Tử số là sai số trên tập kiểm; mẫu số là "dự báo bằng giá trị $m$ bước trước" sai bao nhiêu trên tập huấn luyện.

**Ví dụ tính tay.** Tập huấn luyện $(9, 11, 10, 12, 13)$, $m$ = 1. Bước nhảy giữa hai ngày liền: $(2, 1, 2, 1)$, trung bình 1,5. MASE = 1,6 /
1,5 ≈ **1,07**. Bình phương bước nhảy trung bình 2,5; RMSSE = $\sqrt{4{,}4 / 2{,}5}$ ≈ **1,33**.

**Dùng khi:** so hoặc cộng điểm trên nhiều chuỗi khác thang (MASE); cuộc thi M5 dùng RMSSE vì trên chuỗi bán lác đác, chỉ số dạng trị tuyệt đối
thưởng cho dự báo gần 0.

**Bẫy:**

- MASE < 1 **không** có nghĩa là thắng seasonal naive trên tập kiểm. Mẫu số là sai số dự báo **một bước** trên **tập huấn luyện**; dự báo 7 bước tới
  tất nhiên khó hơn. Muốn biết thắng baseline, chạy baseline trên cùng backtest (buổi 14–15).
- Chuỗi huấn luyện phẳng thì mẫu số bằng 0. M5 tính mẫu số chỉ từ sau lần bán khác 0 đầu tiên.
- M5 gộp nhiều chuỗi thành WRMSSE = $\sum_i w_i \,\text{RMSSE}_i$, trọng số $w_i$ theo **doanh thu** (số lượng × giá) của 28 ngày cuối tập huấn
  luyện, không theo số lượng bán.

## 4. Quantile và khoảng: pinball, Winkler, coverage, WIS

**Pinball loss** cho dự báo quantile $q_{\tau,t}$:

$$
L_\tau(y_t, q_{\tau,t}) = \begin{cases} \tau\,(y_t - q_{\tau,t}) & y_t \ge q_{\tau,t} \\ (1-\tau)\,(q_{\tau,t} - y_t) & y_t < q_{\tau,t} \end{cases}
$$

**Nói bằng lời.** Với $\tau$ = 0,9: thật vượt quantile thì phạt 0,9 lần phần vượt; thật dưới quantile thì chỉ phạt 0,1 lần. Vì vậy dự báo tốt
nhất là con số mà thật chỉ vượt 10% số lần.

**Ví dụ tính tay.** Quantile 0,9 dự báo $(13, 15, 11, 16, 15)$ cho thật $(10, 12, 8, 14, 16)$. Bốn ngày đầu thật nằm dưới: phạt 0,1 × (3, 3, 3,
2) = (0,3; 0,3; 0,3; 0,2). Ngày 5 thật vượt 1: phạt 0,9. Trung bình **0,40**.

**Dùng khi:** thiếu và thừa đắt khác nhau (dự trữ hàng, dự phòng công suất). **Bẫy:** sách FPP nhân 2 (để $\tau$ = 0,5 bằng sai số tuyệt
đối), M5 và utilsforecast không nhân; hai con số chênh đúng 2 lần.

**Winkler score** (Gneiting & Raftery 2007 gọi là interval score) cho khoảng $[\ell_t, u_t]$ danh nghĩa $100(1-\alpha)\%$:

$$
W_{\alpha,t} = (u_t - \ell_t) + \frac{2}{\alpha}(\ell_t - y_t)\,\mathbb{1}\{y_t < \ell_t\} + \frac{2}{\alpha}(y_t - u_t)\,\mathbb{1}\{y_t > u_t\}
$$

- $\mathbb{1}\{\dots\}$ bằng 1 khi điều kiện trong ngoặc đúng, bằng 0 khi sai; "danh nghĩa 80%" là khoảng được làm ra để chứa giá trị thật 80% số lần.

**Nói bằng lời.** Điểm = độ rộng khoảng, cộng phạt $2/\alpha$ lần phần giá trị thật lọt ra ngoài. Khoảng 80% ($\alpha$ = 0,2) thì phạt 10 lần.

**Ví dụ tính tay.** Khoảng 80%: $[8, 13]$, $[9, 14]$, $[7, 11]$, $[11, 16]$, $[12, 15]$. Bốn ngày đầu thật nằm trong: điểm bằng độ rộng (5, 5,
4, 5). Ngày 5 thật 16 vượt cận trên 1: 3 + 10 × 1 = 13. Trung bình **6,4**.

**Coverage** (tỷ lệ phủ): 4 trong 5 ngày nằm trong khoảng, tức **80%**, đúng danh nghĩa. Bẫy: coverage không phải chỉ số chấm điểm; khoảng rộng
vô hạn luôn phủ 100%. Luôn báo kèm độ rộng, hoặc dùng Winkler.

**WIS** (weighted interval score, Bracher và cộng sự 2021) gộp trung vị $m$ và $K$ khoảng mức $\alpha_1, \dots, \alpha_K$:

$$
\text{WIS} = \frac{1}{K + 1/2}\left( \tfrac{1}{2} \lvert y - m \rvert + \sum_{k=1}^{K} \frac{\alpha_k}{2}\, W_{\alpha_k} \right)
$$

**Nói bằng lời.** Trung bình có trọng số của sai số trung vị và điểm Winkler của từng khoảng; khoảng càng rộng ($\alpha$ nhỏ) trọng số càng
nhỏ.

**Ví dụ tính tay.** Thật $y$ = 10, trung vị 8, khoảng 80% là $[6, 9]$, khoảng 50% là $[7; 8{,}5]$. $W_{0,2}$ = 3 + 10 × 1 = 13; $W_{0,5}$ =
1,5 + 4 × 1,5 = 7,5. WIS = (0,5 × 2 + 0,1 × 13 + 0,25 × 7,5) / 2,5 ≈ **1,67**.

**Dùng khi:** dự báo nộp dưới dạng vài quantile (dự báo dịch bệnh, bảng xếp hạng thi). **Bẫy:** WIS chỉ **xấp xỉ** CRPS, sát hơn khi nhiều
khoảng; ghi rõ số khoảng $K$. Hàm WIS của scoringrules 0.11.0 cho kết quả sai ở ví dụ này (mục 10).

## 5. Phân phối: CRPS

Gneiting & Raftery (2007), với phân phối dự báo có hàm phân phối tích luỹ $F$ ($F(y)$ = xác suất dự báo cho giá trị $\le y$) và giá trị
thật $x$:

$$
\text{CRPS}(F, x) = \int_{-\infty}^{\infty} \big(F(y) - \mathbb{1}\{y \ge x\}\big)^2 \, dy
= \mathbb{E}_F\lvert X - x\rvert - \tfrac{1}{2}\,\mathbb{E}_F\lvert X - X'\rvert
$$

- $X, X'$: hai lần rút độc lập từ phân phối dự báo; $\mathbb{E}_F$: trung bình theo phân phối đó.

**Nói bằng lời.** Vế phải: khoảng cách trung bình từ dự báo tới giá trị thật, trừ đi một nửa độ trải của chính dự báo. Dự báo chụm và trúng thì
điểm nhỏ.

**Ví dụ tính tay.** Năm mẫu dự báo $(9, 11, 12, 14, 15)$, thật 12. Khoảng cách tới 12: $(3, 1, 0, 2, 3)$, trung bình 1,8. Khoảng cách trung bình
giữa mọi cặp mẫu (cả 25 cặp, kể cả cặp trùng) là 2,4. CRPS = 1,8 − 1,2 = **0,6**. Một dự báo điểm 13 có CRPS = $\lvert 13 - 12\rvert$ = 1.

**Dùng khi:** so dự báo xác suất với nhau, và với dự báo điểm (với dự báo điểm, CRPS bằng sai số tuyệt đối), cùng đơn vị với dữ liệu. **Bẫy:**
với ít mẫu, ước lượng lệch; phân phối chuẩn thì dùng công thức đóng:

$$
\text{CRPS} = \sigma\left[ z\,\big(2\Phi(z) - 1\big) + 2\varphi(z) - \frac{1}{\sqrt{\pi}} \right], \quad z = \frac{x - \mu}{\sigma}
$$

- $\mu$, $\sigma$: trung bình và độ lệch chuẩn của dự báo; $\Phi$, $\varphi$: hàm phân phối tích luỹ và hàm mật độ (đường cong hình chuông) của
  phân phối chuẩn $N(0, 1)$ (trung bình 0, độ lệch chuẩn 1).

**Nói bằng lời.** Với $N(0, 1)$ và giá trị thật 0,8: CRPS ≈ 0,476 (mục 9).

## 6. Xác suất sự kiện: Brier, log score

**Brier score** cho xác suất dự báo $p_i$ và kết quả $o_i$ (1 nếu xảy ra, 0 nếu không): $\text{BS} = \operatorname{mean}\big((p_i - o_i)^2\big)$.

**Ví dụ tính tay.** Xác suất mưa $(0{,}9;\ 0{,}7;\ 0{,}2;\ 0{,}6;\ 0{,}1)$, thực tế $(1, 0, 0, 1, 0)$. Bình phương chênh:
$(0{,}01;\ 0{,}49;\ 0{,}04;\ 0{,}16;\ 0{,}01)$, trung bình **0,142**. Luôn dự báo tỷ lệ chung 0,4 cho BS = 0,24.

**Dùng khi:** dự báo "có/không" (mưa, vượt ngưỡng tải). **Bẫy:** sự kiện hiếm thì dự báo luôn 0 cũng có Brier nhỏ; so với dự báo tỷ lệ chung
(mục 7).

**Phân rã Murphy (1973).** Nhóm các lần dự báo cùng xác suất $p_k$ ($n_k$ lần, tần suất thật $\bar o_k$; tần suất chung $\bar o$):

$$
\text{BS} = \frac{1}{N}\sum_k n_k (p_k - \bar o_k)^2 - \frac{1}{N}\sum_k n_k (\bar o_k - \bar o)^2 + \bar o\,(1 - \bar o)
$$

**Nói bằng lời.** Brier = độ tin cậy (xác suất nói 70% thì có xảy ra 70% không; nhỏ là tốt) − độ phân giải (dự báo có tách được ngày mưa với
ngày khô không; lớn là tốt) + độ bất định của chính sự kiện. Ví dụ 10 số ở mục 9.

**Log score:** $\operatorname{mean}\big(-\ln p(\text{kết quả đã xảy ra})\big)$. Ví dụ trên: $-\ln$ của $(0{,}9;\ 0{,}3;\ 0{,}8;\ 0{,}6;\ 0{,}9)$,
trung bình **0,430**. **Bẫy:** một lần nói xác suất 0 cho sự kiện rồi nó xảy ra thì điểm vô hạn; phải chặn xác suất khỏi 0 và 1.

## 7. Skill score

$$
\text{Skill} = \frac{\text{điểm}_{\text{tham chiếu}} - \text{điểm}_{\text{mô hình}}}{\text{điểm}_{\text{tham chiếu}}}
$$

**Nói bằng lời.** Mô hình giảm được bao nhiêu phần sai số so với một dự báo tham chiếu đơn giản; 0 là ngang tham chiếu, âm là thua.

**Ví dụ tính tay.** Tham chiếu naive: dự báo cả 5 ngày bằng giá trị huấn luyện cuối là 13, MAE = (3 + 1 + 5 + 1 + 3)/5 = 2,6. Skill = (2,6 − 1,6)
/ 2,6 ≈ **0,38**: mô hình giảm 38% sai số. Brier ở mục 6 so với dự báo tỷ lệ chung: (0,24 − 0,142)/0,24 ≈ 0,41.

**Dùng khi:** báo cáo cho người không quen đơn vị dữ liệu. Sách FPP: dữ liệu có mùa vụ thì tham chiếu là seasonal naive. **Bẫy:** con số phụ
thuộc tham chiếu, phải ghi rõ; không tối ưu mô hình theo skill score của Brier vì nó không phải chỉ số chấm điểm đúng đắn (hướng dẫn kiểm
định của WWRP/WGNE).

## 8. So hai mô hình: Diebold–Mariano

**Vấn đề.** Mô hình A có MAE thấp hơn B trên tập kiểm. Có thể chỉ do may. Kiểm định Diebold–Mariano hỏi: chênh lệch có lớn hơn mức dao động
ngẫu nhiên không?

Chênh mất mát $d_t = g(e_{1t}) - g(e_{2t})$ trên $n$ dự báo tầm $h$; bản hiệu chỉnh của Harvey, Leybourne & Newbold (1997):

$$
S_1 = \frac{\bar d}{\sqrt{\hat V(\bar d)}}, \quad \hat V(\bar d) \approx \frac{1}{n}\Big[\hat\gamma_0 + 2\sum_{k=1}^{h-1}\hat\gamma_k\Big],
\qquad
S_1^* = \left[\frac{n + 1 - 2h + n^{-1}h(h-1)}{n}\right]^{1/2} S_1
$$

- $\hat\gamma_k$: tự hiệp phương sai của $d_t$ ở độ trễ $k$; $\hat\gamma_0$ là phương sai (chia $n$).

**Nói bằng lời.** Chênh trung bình chia cho sai số chuẩn của nó; $S_1^*$ so với phân phối Student-t $n - 1$ bậc tự do.

**Ví dụ tính tay.** Mất mát bình phương, $h$ = 1. Mô hình ở ví dụ chung: $e^2 = (1, 4, 1, 0, 16)$. Naive (dự báo 13): $(9, 1, 25, 1, 9)$.
Chênh $d = (-8, 3, -24, -1, 7)$, trung bình −4,6, phương sai 118,64. $S_1 = -4{,}6 / \sqrt{118{,}64/5}$ ≈ −0,94; $S_1^*$ ≈ −0,84, p ≈ 0,45 (t, 4
bậc tự do). Mô hình có MSE thấp hơn, nhưng 5 điểm không đủ bằng chứng.

**Dùng khi:** chọn giữa hai mô hình có sai số gần nhau. **Bẫy:** bản gốc dùng ngưỡng phân phối chuẩn bác bỏ quá dễ khi mẫu nhỏ; dùng bản
hiệu chỉnh ở trên (`forecast::dm.test` của R cài bản này). Nhiều tầm dự báo thì $d_t$ tự tương quan, phải cộng các $\hat\gamma_k$.

## 9. Đối chiếu với thư viện

**Dự báo điểm.** Chuỗi huấn luyện mùa vụ $m$ = 4: `10 20 30 20 12 22 33 21 13 24 35 23`; thật `14 25 36 24`, dự báo `12 27 30 25`.

| Đại lượng | Tự tính (NumPy) | utilsforecast 0.2.16 |
|---|---|---|
| $e = y - \hat y$ | 2, −2, 6, −1 | |
| MAE | 2,75 | `mae` 2,75 |
| RMSE | 3,3541 | `rmse` 3,3541 |
| ME | 1,25 | `bias` **−1,25** (tính $\hat y - y$) |
| MAPE | 10,7798% | `mape` **0,107798** (tỷ lệ) |
| sMAPE (thang 0–200) | 11,3351 | `smape` **0,056675** (thang 0–1) |
| WAPE | 0,1111 | `nd` 0,1111 |
| mẫu số MASE: $\operatorname{mean}\lvert y_t - y_{t-4}\rvert$ | 1,875 | |
| MASE | 1,4667 | `mase` 1,4667 |
| RMSSE (mẫu số 3,875) | 1,7039 | `rmsse` 1,7039 |

**Đọc bảng.** Ba dòng in đậm cùng tên mà khác số: khác dấu, khác thang. Đọc tài liệu hàm trước khi dán con số vào báo cáo.

**Pinball.** Quantile 0,9 dự báo `11 23 31 22` cho cùng giá trị thật: không nhân 2 được 2,70; nhân 2 (FPP) được 5,40;
`utilsforecast.quantile_loss` ra 2,70.

**CRPS.** $N(0, 1)$, giá trị thật 0,8: công thức đóng 0,4762, `scoringrules.crps_normal` 0,4762; ước lượng từ 4.000 mẫu (seed 3) 0,4632.

**Brier và phân rã Murphy.** Xác suất `.1 .1 .1 .1 .7 .7 .7 .7 .7 .9`, kết quả `0 0 1 0 1 1 0 1 1 1`: BS = 0,170; độ tin cậy 0,015; độ phân
giải 0,085; bất định 0,240; kiểm lại 0,015 − 0,085 + 0,240 = 0,170.

**Diebold–Mariano.** Hai chuỗi sai số 40 điểm (seed 11), mất mát bình phương, $h$ = 1: $S_1$ = −1,455, p = 0,146 (chuẩn); $S_1^*$ = −1,437, p =
0,159 (t, 39 bậc tự do).

**Trên dữ liệu thật (buổi 14, 15).**

| Dữ liệu | Kết quả | Bài học |
|---|---|---|
| 1.000 chuỗi M4 theo ngày, 14 ngày chấm | MASE trung vị: naive 0,835, drift 0,810, seasonal naive 1,077 | seasonal naive là mốc bắt buộc, không phải mốc mạnh nhất |
| 300 mã hàng bán lẻ, 75% ngày bằng 0 | MAPE vô hạn ở cả 300 chuỗi; hạng nhất đổi theo MAE, sMAPE, RMSSE | chuỗi thưa: WAPE, MASE, RMSSE, và đếm chuỗi không tính được |
| tải ERCOT, hold-out quý 4/2024 | "trộn" (cùng giờ hôm qua và tuần trước) hơn seasonal naive 4,3%: DM bỏ tự tương quan p = 0,0000012; DM-HLN $h$ = 24 p = 0,16 | dự báo nhiều bước thì chênh mất mát tự tương quan |

## 10. Thư viện tính khác nhau thế nào

| Thư viện, hàm | Khác ở đâu | Không để ý thì |
|---|---|---|
| utilsforecast 0.2.16 `smape` | $\lvert y - \hat y\rvert / (\lvert y\rvert + \lvert\hat y\rvert)$, thang **0–1** | con số nhỏ hơn thang FPP 200 lần |
| utilsforecast `mape` | tỷ lệ, không nhân 100; điểm có $y$ = 0 bị bỏ khỏi trung bình | "MAPE 0,1" tưởng là 0,1% |
| utilsforecast `bias` | $\hat y - y$, ngược dấu $e$ | đọc ngược hướng chệch |
| utilsforecast `quantile_loss` | không nhân 2 | lệch 2 lần so với FPP |
| scoringrules 0.11.0 `weighted_interval_score` (bản không numba) | cho **2,87 thay vì 1,67** ở ví dụ WIS mục 4: nhân trọng số với trung vị thay vì với $\lvert y - m\rvert$ | WIS sai; tự viết theo công thức mục 4 |
| properscoring | bản cuối 0.1 (2015), đã ngừng phát triển | dùng scoringrules cho CRPS (`crps_normal`, `crps_ensemble` khớp mục 9) |
| ACF của statsmodels và FPP | xem Phụ lục C mục 8 | |

## Nguồn

Truy cập ngày 2026-09-17. Nhật ký research: `tools/NGHIEN-CUU.md`.

- Hyndman, R.J., Athanasopoulos, G. et al. *FPP, the Pythonic Way*, mục 5.8, 5.9: <https://otexts.com/fpppy/05-toolbox.html>
- Hyndman, R.J. & Koehler, A.B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting* 22(4),
  679–688. <https://robjhyndman.com/papers/mase.pdf>
- Hyndman, R.J. (2025). WAPE (Hyndsight): <https://robjhyndman.com/hyndsight/wape.html>
- Makridakis, S. et al. M5 Competitors' Guide: <https://github.com/Mcompetitions/M5-methods/blob/master/M5-Competitors-Guide.pdf>
- Gneiting, T. (2011). Making and evaluating point forecasts. *JASA* 106(494), 746–762. <https://arxiv.org/abs/0912.0902>
- Gneiting, T. & Raftery, A.E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102, 359–378.
  <https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf>
- Bracher, J., Ray, E.L., Gneiting, T. & Reich, N.G. (2021). Evaluating epidemic forecasts in an interval format. *PLoS Computational
  Biology* 17(2), e1008618. <https://doi.org/10.1371/journal.pcbi.1008618>
- Murphy, A.H. (1973). A new vector partition of the probability score. *J. Applied Meteorology* 12, 595–600 (qua trang WWRP/WGNE:
  <https://www.cawcr.gov.au/projects/verification/>)
- Harvey, D., Leybourne, S. & Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of
  Forecasting* 13, 281–291.
- utilsforecast 0.2.16 (mã nguồn `losses.py`): <https://pypi.org/project/utilsforecast/>
- scoringrules 0.11.0: <https://pypi.org/project/scoringrules/>
