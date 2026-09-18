# Nhật ký research — Phase 1 (khung trợ giúp + danh mục dữ liệu)

- **Ngày research:** 2026-09-17 (mọi nguồn truy cập ngày này)
- **Phạm vi:** giấy phép + cách tải script của MỌI bộ dữ liệu trong lộ trình; công thức chuẩn MASE/RMSSE/
  WRMSSE, CRPS, WIS, Diebold–Mariano bản mẫu nhỏ; backtest rolling origin; rò rỉ dữ liệu chuỗi thời gian;
  PIT/reliability diagram
- **Cách kiểm:** đọc trang giấy phép gốc (trích nguyên văn bên dưới); tải thử bằng curl / `lay_du_lieu.py
  --sha` và so sha256 giữa hai lần tải; đọc mã nguồn thư viện đối chiếu (utilsforecast 0.2.16, scoringrules
  0.11.0, statsforecast 2.1.1, datasetsforecast 1.0.1, R forecast `DM2.R`, dieboldmariano 1.1.0)
- **[CHẠY]** = đã chạy thử; **[CHƯA XÁC MINH]** = không kiểm được, không dùng làm căn cứ
- Trích dẫn đánh dấu *(công cụ đọc trang)* được lấy qua công cụ tóm tắt trang — gần nguyên văn nhưng không
  bảo đảm từng chữ; còn lại trích từ HTML/PDF gốc

Nguyên văn giấy phép của từng bộ còn được ghi trong trường `trich_giay_phep` của `danh-muc.toml` và hiện
ở Phụ lục F.

---

## A. Điểm lệch so với lộ trình / todos và quyết định

| # | Điểm lệch | Mức | Quyết định |
|---|---|---|---|
| 1 | **Điều khoản FRED cấm dùng nội dung FRED "in connection with the development or training of any software program or system or machine learning"** — áp cho buổi 5, 7, 8, 17, 20, 21 | **lớn** | Không đưa FRED/ALFRED/FRED-MD vào danh mục tải tự động; lấy cùng chuỗi từ cơ quan gốc (mục C.2) — đã sửa lộ trình + todos |
| 2 | **NOAA ISD trạm Nội Bài dừng 2025-08-24; dữ liệu ISD ngoài Mỹ "cannot be redistributed" (WMO Res 40)** | **lớn** (buổi 33) | Thay bằng NOAA GHCNh `VMI0000VVNB` (CC0) — đã sửa lộ trình |
| 3 | **METR-LA không có giấy phép dữ liệu** | vừa (buổi 33) | Monash Traffic hourly (CC BY 4.0) làm bộ chính; METR-LA tuỳ chọn tự tải — đã sửa lộ trình |
| 4 | **UCI 321 (ElectricityLoadDiagrams) tải ~2,5 KB/s** [CHẠY] — hơn một ngày cho 249 MB | vừa (buổi 29, 30, 32) | Dùng Monash `electricity_hourly` (bản gộp giờ của chính bộ này, CC BY 4.0, Zenodo) — đã sửa lộ trình |
| 5 | Tourism Australia: chỉ có bản trong gói R tsibble (GPL-3); giấy phép Tourism Research Australia không đọc được (404) | vừa (buổi 28) | Dùng tệp `tourism.rda` của tsibble chốt commit (GPL-3); dự phòng phân cấp từ Online Retail II — đã sửa lộ trình |
| 6 | fev_datasets `license: other`, "provided only for research purposes"; GIFT-Eval "for research purposes only" | vừa (buổi 34–35) | Không tải tự động; Phase 10 chỉ chọn bộ con có nguồn mở rõ — đã sửa lộ trình |
| 7 | OpenAQ: giấy phép theo nhà cung cấp chỉ tra được bằng key; mạng trạm Hà Nội chưa rõ giấy phép | vừa (buổi 10, DAGC1, đề C) | Ngoài danh mục cho tới Phase 4 (có key); dự phòng UCI Beijing + Open-Meteo Hà Nội |
| 8 | EIA-930: tệp sáu tháng dựng lại HẰNG NGÀY (Last-Modified mọi tệp 2026-09-16) | vừa | Chốt sha256 hôm nay; `ly_do_mirror` = bắt buộc mirror |
| 9 | BTS hành khách hàng không: chỉ có bảng HTML, data.bts.gov trả 403 | nhỏ (buổi 11, 16) | Ngoài danh mục; dự phòng Tourism monthly / Wikipedia; làm công cụ trích + mirror sau |
| 10 | M5: Nixtla `datasetsforecast` tải từ repo GitHub Nixtla/m5-forecasts **không có giấy phép** | nhỏ | Chỉ tải qua Kaggle bằng tài khoản học viên; `cho_sha256` tới khi có tài khoản Kaggle |
| 11 | Prop 99: R Synth và pysyncon KHÔNG kèm bộ Prop 99; tác giả gốc không công bố giấy phép | nhỏ | Tải CSV từ repo MIT chốt commit, không mirror |
| 12 | UCI 501: zip lồng zip + 2 CSV giá cổ phiếu không liên quan | nhỏ | Thêm `giai_nen_long` vào `lay_du_lieu.py` [CHẠY ở lượt tải toàn danh mục] |
| 13 | Buổi dạy chính một công cụ (4: ve, 13: ro_ri, 14: danh_gia, 15: backtest) sẽ nhận luôn lời giải trong `tv/` | thiết kế | Thêm khoá `khung_bo` vào `lab/nen.toml`; `sinh_nen.py` bỏ module đó khỏi `tv/` |
| 14 | Khung phải chạy trên cả pandas 3.0.5 (buổi 1–13) và 2.3.3 (buổi dùng Nixtla) | thiết kế | `tools/kiem_khung.py` chạy test ở 2 hồ sơ [CHẠY: đạt cả hai] |
| 15 | Mirror Hugging Face chưa làm được: máy soạn không có tài khoản/token HF | **chặn** | `tools/du-lieu/mirror_hf.py --chuan-bi` sẵn sàng; `--day-len` cần chủ khoá đồng ý + token |

---

## B. Giấy phép từng nguồn (trích nguyên văn)

### B.1 UCI Machine Learning Repository — CC BY 4.0
Trang từng bộ (235, 275, 321, 374, 501, 502), ví dụ https://archive.ics.uci.edu/dataset/502/online+retail+ii:
> "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. This
> allows for the sharing and adaptation of the datasets for any purpose, provided that the appropriate credit is given."

UCI không có trang điều khoản chung (`/terms` trả 404) → ghi giấy phép theo từng bộ. Kích thước và sha256 xem
danh mục. [CHẠY] URL 501 phải có slug `beijing+multi+site+air+quality+data` (bản không `+data` trả 404).

### B.2 Monash Time Series Forecasting Repository (Zenodo) — CC BY 4.0
Zenodo API `https://zenodo.org/api/records/<id>`, rights:
> "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the
> condition that the creator is appropriately credited."

CC BY 4.0 legal code §2(a)(1): "reproduce and Share the Licensed Material, in whole or in part; and produce,
reproduce, and Share Adapted Material." [CHẠY] URL `https://zenodo.org/records/<id>/files/<tệp>?download=1`
tải không cần đăng nhập; md5 Zenodo khớp mọi tệp đã tải.
Lưu ý nguồn gốc: Car Parts "extracted from R expsmooth package" (GPL); Tourism và Kaggle Web Traffic từ cuộc
thi Kaggle (luật cuộc thi không đọc được) → hai bộ này `mirror = false`, Zenodo đã là nguồn ổn định có DOI.
M4 trên GitHub `Mcompetitions/M4-methods` **không có giấy phép** (GitHub API `license: null`) → dùng bản Zenodo.

### B.3 ETDataset — CC BY-ND 4.0
LICENSE tại commit `1d16c8f4f943005d613b5bc962e9eeb06058cf07`: §2(a)(1) "A. reproduce and Share the Licensed
Material, in whole or in part; and B. produce and reproduce, but not Share, Adapted Material." §3(a)(2) "You do
not have permission under this Public License to Share Adapted Material." → chỉ mirror bản NGUYÊN BYTE.
fev_datasets có bản ETT đã resample (ETT_1D, ETT_1W) — không khớp điều khoản ND; khoá không dùng các bản đó.

### B.4 US EIA — public domain
https://www.eia.gov/about/copyrights_reuse.php:
> "U.S. government publications are in the public domain and are not subject to copyright protection. You may
> use and/or distribute any of our data, files, databases, reports, graphs, charts, and other information
> products that are on our website or that you receive through our email distribution service. However, if you
> use or reproduce any of our information products, you should use an acknowledgment, which includes the
> publication date, such as: "Source: U.S. Energy Information Administration (Oct 2008).""

Sửa số liệu (Form EIA-930 instructions): "correct the data with a resubmission within 3 days" và lỗi > 10 MWh
"resubmit corrected data to address the imbalance within 30 days". Tệp sáu tháng
`https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_<YYYY>_<Jan_Jun|Jul_Dec>.csv`
(từ 2015 H2). [CHẠY] 2024 H1 tải 13:05 và 13:25 UTC cùng sha256 `26768c49…`; mọi tệp Last-Modified
2026-09-16 → dựng lại hằng ngày, ổn định qua ngày CHƯA kiểm. Bảng cột đổi từ 2024 H2 (44 → 65 cột).

### B.5 FRED / ALFRED / FRED-MD (St. Louis Fed) — KHÔNG đưa vào danh mục
https://fred.stlouisfed.org/legal/:
> "Data series available through the FRED® Services, including but not limited to the FRED® and ALFRED® data
> series, may be owned by third parties and may be protected by copyrights…"

Điều cấm:
> "Use the FRED® Services or FRED® Content in connection with the development or training of any software
> program or system or machine learning, including, but not limited to, large language models, deep learning,
> generative artificial intelligence…"

Chín chuỗi dự kiến (RSAFS, RSXFS, CPIAUCSL, UNRATE, POPTHM, GDPC1, INDPRO, DEXUSEU, DCOILWTICO) đều gắn nhãn
"Public Domain: Citation requested" trên FRED — dữ liệu gốc là của cơ quan chính phủ Mỹ, nên lấy thẳng từ cơ
quan gốc (mục C.2). [CHẠY bởi agent] `fredgraph.csv?id=&cosd=&coed=` ổn định trong ngày nhưng trả vintage hiện
tại; `alfredgraph.csv?id=GDPC1&vintage_date=…` tái lập được. FRED-MD: trang McCracken không ghi giấy phép.

### B.6 NOAA — ISD (không dùng) và GHCNh (CC0)
https://www.ncei.noaa.gov/pub/data/noaa/readme.txt:
> "IMPORTANT NOTE: The non-U.S. data in ISD are subject to WMO Resolution 40 restrictions, and cannot be
> redistributed to other users or customers."

ISD `488200-99999` hoạt động 19581201–20250824 (isd-history.csv); NCEI: "The Integrated Surface Database (ISD)
product is actively being replaced by the new Global Historical Climatology Network hourly (GHCNh)" *(công cụ
đọc trang)*. GHCNh metadata C01688: "These data were produced by NOAA and are not subject to copyright protection
in the United States." *(công cụ đọc trang)*, NOAA miễn trừ quyền toàn cầu qua CC0-1.0. Ghi chú WMO Res 40 có
còn áp cho trạm ngoài Mỹ trong GHCNh **CHƯA XÁC MINH** → `mirror = false`. Tệp năm cũ bị viết lại (Last-Modified
2026-07-11).

### B.7 NYC TLC — NYC Open Data
FAQ https://www.nyc.gov/opendata/get-started/FAQs: "Open Data belongs to all New Yorkers. There are no
restrictions on the use of Open Data." *(công cụ đọc trang)*. Trang TLC: "The trip data was not created by the
TLC, and TLC makes no representations as to the accuracy of these data." Tệp tháng có thể được tải lại
(yellow 2024-01 Last-Modified 2024-03-21). Tháng mới nhất 2026-05.

### B.8 US BTS
DOT librarian FAQ: "There are no copyright restrictions or charges for use of DOT publications. Please properly
cite any use of DOT publications." *(công cụ đọc trang)*. Chuỗi hành khách chỉ có ở bảng HTML TranStats (HTML
đổi byte mỗi lần do viewstate ASP.NET; bảng trích ra ổn định); data.bts.gov trả 403 từ máy này.

### B.9 Open-Meteo — CC BY 4.0, API miễn phí phi thương mại
https://open-meteo.com/en/licence: "API data are offered under Attribution 4.0 International (CC BY 4.0) You are
free to share: copy and redistribute the material in any medium or format and adapt: remix, transform, and
build upon the material. Attribution: You must give appropriate credit, provide a link to the licence, and
indicate if changes were made."
https://open-meteo.com/en/terms: "You may only use the free API services for non-commercial purposes"; ví dụ phi
thương mại gồm "Incorporating our service into educational content". Giới hạn "600 calls / min … 10,000 / day".
[CHẠY] `models=era5` + khoảng cố định cho sha256 ổn định (mặc định "best match" trộn mô hình). Historical
Forecast API chỉ ghép giờ đầu mỗi lượt chạy (từ ~2022); **Previous Runs API** cho giá trị dự báo trước 1–7 ngày
("Most models are archived from January 2024") → nguồn "thời tiết dự báo lưu trữ" cho buổi 13, DAGC2.

### B.10 OpenAQ — theo nhà cung cấp
https://docs.openaq.org/about/terms: "downloading data is strictly prohibited unless done through registered and
authorized use. Users must utilize provided APIs, export functions, or other officially sanctioned methods for
accessing data." và "OpenAQ users must therefore review and comply with any terms published by data providers…
Attribution to OpenAQ as the source data is also required". AWS registry: "License: Varies, depends on data
provider". Trạm Việt Nam tìm được (không có key, tra qua S3 + explore — giấy phép *(công cụ đọc trang)*): mạng
"Hanoi Air Quality Monitoring Network" (giấy phép không hiển thị; 2161292, 2161306, 4946812, 4946813 còn gửi dữ
liệu 09/2026), AirNow 7441 Hà Nội ("US Public Domain", dừng 2025-04-09), AirGradient 3276359 TP.HCM ("CC BY 4.0",
còn hoạt động).

### B.11 Wikimedia Pageviews — CC0
https://dumps.wikimedia.org/legal.html: "All Analytics datasets are available under the Creative Commons Zero
(CC0) public domain dedication, unless otherwise specified." Chính sách User-Agent yêu cầu tên công cụ + liên
hệ *(công cụ đọc trang)* → `lay_du_lieu.py` đổi `TAC_NHAN`. [CHẠY] bài "Tết_Nguyên_Đán" 2016–2025 tải được.

### B.12 GDELT
https://www.gdeltproject.org/about.html *(công cụ đọc trang)*: "You may redistribute, rehost, republish, and
mirror any of the GDELT datasets in any form. However, any use or redistribution of the data must include a
citation to the GDELT Project and a link to this website". DOC 2.0 API giới hạn "one every 5 seconds" và cửa
sổ trượt → dùng tệp.

### B.13 Binance Public Data — không có giấy phép dữ liệu
Repo `binance/binance-public-data`: không có tệp LICENSE (GitHub `license: null`); README "## Licence MIT" (cho
mã). Điều khoản Binance trang JS không tải được; trích từ nguồn thứ cấp 2021 về cấm dùng thương mại dữ liệu
thị trường **CHƯA XÁC MINH bản hiện hành** → `mirror = false`, học viên tự tải.

### B.14 ECMWF Open Data — CC BY 4.0
https://www.ecmwf.int/en/forecasts/datasets/open-data: "Their use is governed by the Creative Commons CC-BY-4.0
licence and the ECMWF Terms of Use. This means that the data may be redistributed and used commercially,
subject to appropriate attribution." data.ecmwf.int giữ "the most recent 12 forecast runs"; lịch sử AIFS trên
GCS `ecmwf-open-data` (từ 2023-07-12) và AWS `ecmwf-forecasts`. [CHẠY bởi agent] Range theo `.index` trên GCS
trả 206, sha256 ổn định; AWS trả 503 SlowDown. AIFS 1.0 vận hành 2025-02-25; model card: "Pre-training … on
ERA5 for the years 1979 to 2022", fine-tune "from 2016 to 2022" *(công cụ đọc trang)* → chỉ đánh giá từ 2023.

### B.15 Bộ nghiên cứu và cuộc thi
- **M5 (Kaggle):** luật §7B "You agree not to transmit, duplicate, publish, redistribute or otherwise provide or
  make available the Competition Data to any party not participating in the Competition." (Phase 0). Repo
  M5-methods và MOFC không có giấy phép mở.
- **METR-LA:** README DCRNN chỉ ghi nơi tải (Google Drive / Baidu Yun), repo mã MIT, không có điều khoản dữ liệu.
  Bản Hugging Face gắn giấy phép do người tải lên tự chọn.
- **Tourism Australia:** tsibble CRAN "License: GPL-3"; tài liệu dữ liệu chỉ tham chiếu Tourism Research
  Australia; trang giấy phép TRA 404.
- **Prop 99:** R Synth (GPL) và pysyncon (MIT) không kèm; bản trong Stata synth (SSC, không ghi giấy phép), SparseSC
  (MIT), tidysynth (MIT), python-causality-handbook (MIT).
- **Dominick's:** "These data are for academic research purposes only. Users must acknowledge in their working
  papers and/or publications the Kilts Center for Marketing at the University of Chicago Booth School of Business."
- **fev_datasets** (rev `f71c0fff4cf81283a2c43e7f3a73aa4f9826aef8`): "Please refer to the original sources for
  licensing and citation terms. We do not claim any rights to the original data. Unless otherwise specified, the
  datasets are provided only for research purposes." **GiftEval** (rev `30841734…`): `apache-2.0` nhưng "This
  release is for research purposes only in support of an academic paper."
- **ForecastBench datasets** (commit `a11ac3a9ba8812cdedab2b79ab3181a9c0825d62`): "The datasets in this repository
  are distributed under the CC BY-SA 4.0 license".
- **Metaculus:** terms (mã nguồn trang, "Last Modified: Jun 13, 2025"): "No materials from the Service may be
  copied, reproduced, modified, republished, downloaded, uploaded, posted, transmitted, or distributed in any
  form or by any means without Metaculus's prior written permission" và cấm dùng để huấn luyện AI.

---

## C. Nguồn thay thế

### C.1 Điện theo giờ nhiều khách hàng
Monash `electricity_hourly` (Zenodo 4656140): "an aggregated version of the original dataset used by Lai et al.
(2017). It contains 321 hourly time series from 2012 to 2014." [CHẠY] md5 khớp Zenodo.

### C.2 Chuỗi kinh tế Mỹ không qua FRED
Tải hai lần cách nhau ~5 phút, sha256 giống nhau [CHẠY bởi agent, tác giả tải lần ba cùng sha]; tệp "hiện hành"
bị ghi đè mỗi kỳ công bố → bắt buộc mirror.

| Chuỗi FRED | Nguồn gốc | URL | Điều khoản (trích) |
|---|---|---|---|
| CPIAUCSL | BLS `CUSR0000SA0` | download.bls.gov/pub/time.series/cu/cu.data.1.AllItems | "everything that we publish … is in the public domain … we do ask that you cite the Bureau of Labor Statistics as the source" (bls.gov/opub/copyright-information.htm) |
| UNRATE | BLS `LNS14000000` | chỉ có trong ln.data.1.AllData (390 MB) hoặc API v1 (JSON có `responseTime` đổi mỗi lần) | như trên — **nguồn tải chốt ở Phase 3** |
| GDPC1 | BEA `A191RX` | apps.bea.gov/national/Release/TXT/NipaDataQ.txt | "Unless stated otherwise, the information posted on the BEA web site is in the public domain and may be used or reproduced without specific permission." (bea.gov/help/faq/145) |
| POPTHM | BEA `B230RC` | …/NipaDataM.txt | như trên |
| INDPRO | FRB G.17 `IP.B50001.S` | federalreserve.gov/datadownload (gói, 2000–2024) | "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission." (federalreserve.gov/disclaimer.htm) |
| DEXUSEU | FRB H.10 `RXI$US_N.B.EU` | như trên | như trên |
| DCOILWTICO | EIA `RWTC` | eia.gov/dnav/pet/hist_xls/RWTCd.xls | EIA public domain (B.4) |
| RSAFS/RSXFS | Census MARTS | **CHƯA XÁC MINH** — census.gov chặn (Cloudflare 403) từ mạng soạn; API cần key miễn phí | — |
| ALFRED vintage GDP | Philadelphia Fed RTDSM `ROUTPUTQvQd.xlsx` | philadelphiafed.org/-/media/…/real-time-data/data-files/xlsx/ | "The content provided on this website may be used for informational, educational, and research purposes only." — trang ghi "Copyright 2026. All rights reserved." → không mirror |
| FRED-MD | — | trang McCracken không có điều khoản riêng; site St. Louis Fed: "may be used for research and informational purposes only" | coi như chịu điều khoản FRED → không dùng |

[CHẠY] BLS trả **403** cho User-Agent không có thông tin liên hệ (cả UA trình duyệt), trả 200 khi UA có email →
`lay_du_lieu.py` thêm biến `KHOA_FORECASTING_LIEN_HE` + trường danh mục `can_lien_he`.

---

## D. Công thức và thuật toán cho `tools/khung/`

### D.1 M5 RMSSE / WRMSSE
M5 Competitors' Guide (https://github.com/Mcompetitions/M5-methods): mẫu số RMSSE "computed only for the
time-periods for which the examined product(s) are actively sold, i.e., the periods following the first non-zero
demand"; trọng số "computed using the last 28 observations of the training sample (sum of units sold multiplied
by their respective price)"; "K is set equal to 12, with the weights of the series being computed so that they
sum to one at each aggregation level". 12 cấp, tổng 42.840 chuỗi. Ví dụ trong Guide mang hệ số 1/K → mọi trọng số
cộng lại bằng 1. Bài tổng kết M5 (IJF 38(4) 2022): "all aggregation levels are equally weighted".
Cài đặt tham chiếu `datasetsforecast.m5.M5Evaluation`: mẫu số `x = x[np.argmax(x!=0):]`. **utilsforecast.rmsse KHÔNG
bỏ số 0 đầu** → không đúng M5. `tv.danh_gia.rmsse(tu_khac_0=True)` theo Guide.

### D.2 CRPS từ mẫu
Gneiting & Raftery (2007) eq. 21 dạng kernel; CRPS "reduces to the absolute error if F is a deterministic
forecast". scoringrules 0.11.0 (mã `core/crps/_approx.py`): `crps_ensemble(..., estimator="qd")` mặc định; "nrg" =
e₁ − ½Σ|xᵢ−xⱼ|/M², "fair" = e₁ − ½Σ|xᵢ−xⱼ|/(M(M−1)); [CHẠY bởi agent] qd = nrg = int = properscoring; pwm = fair.
Ferro (2014): "The usual … continuous ranked probability scores for ensemble forecasts are shown to be unfair,
while adjusted versions of these scores are shown to be fair." [CHẠY] `tv.danh_gia.crps_mau` khớp
`scoringrules.crps_ensemble` (nrg, fair) tới 1e-9. properscoring 0.1 (2015) báo SyntaxWarning trên Python 3.12.

### D.3 WIS
Bracher et al. (2021), arXiv 2005.12881, eq. 1 và eq. 4 ("with the weights wk from equation (2) the WIS can also
be expressed as" dạng quantile). Hub chuẩn "K = 11 prediction intervals with α1 = 0.02, α2 = 0.05, α3 = 0.1, …,
α11 = 0.9" (23 quantile). [CHẠY] `wis` = `wis_quantile` = 1,67 trên ví dụ Phụ lục D.

### D.4 Diebold–Mariano
Diebold (2015, JBES 33(1)): "DM is a test for comparing forecasts, not models." Harvey, Leybourne & Newbold (1997,
IJF 13) — bài gốc sau tường phí; công thức DM* = DM·√((n+1−2h+h(h−1)/n)/n) so với t(n−1) đối chiếu qua hai cài đặt:
R `forecast::dm.test` (`DM2.R`: phương sai `(γ0 + 2Σγk)/n`, `acf(type="covariance")` chia n; phương sai âm và h>1
→ cảnh báo "Proceeding with horizon h=1") và Python `dieboldmariano` 1.1.0 (ném lỗi thay vì lùi về h=1).
→ `tv.backtest.diebold_mariano` làm như R. [CHẠY] khớp số tính tay Phase 0 (DM −1,4550; HLN −1,4367, p 0,1588).

### D.5 Backtest rolling origin
FPP3 §5.10: "This procedure is sometimes known as 'evaluation on a rolling forecasting origin' because the
'origin' at which the forecast is based rolls forward in time." Bergmeir, Hyndman & Koo (2018): "in the case of a
purely autoregressive model, the use of standard K-fold CV is possible as long as the models considered have
uncorrelated errors." statsforecast 2.1.1 `cross_validation`: `test_size = h + step_size*(n_windows-1)`, cutoff
`range(-test_size, -h+1, step_size)`, `input_size=None` = expanding, "refit … If an integer n, refits every n
windows". utilsforecast `backtest_splits`: `step_size` mặc định = h. sklearn 1.9.1 `TimeSeriesSplit(gap=)`:
"Number of samples to exclude from the end of each train set before the test set."
→ `tv.backtest`: cửa sổ cuối kết thúc ở ds cuối, `buoc` mặc định h, `gap`, `cua_so_train` (sliding), `refit`
True/False/k theo cùng ngữ nghĩa statsforecast.

### D.6 Rò rỉ dữ liệu
Kapoor & Narayanan (2023, Patterns 4:100804; arXiv 2207.07048): "[L3.1] Temporal leakage. When an ML model is
used to make predictions about a future outcome of interest, the test set should not contain any data from a
date before the training set." Các loại liên quan: "[L1.2] Pre-processing on training and test set", "[L3.2]
Nonindependence between train and test samples".
Phát hiện tự động — gần nhất với cách của `tv.ro_ri`:
- Fonseca (2026, arXiv 2607.04958) định nghĩa look-ahead bias "using information from after a decision epoch to
  make the decision at that epoch"; đánh giá "a two-run differential detector that re-executes the pipeline on
  perturbed future data at sampled epochs and flags a change" — bỏ lọt "18 (54.5%)" trên 33 lỗi cài đối kháng;
  "absence of detection is not proof of absence."
- Saggese & Smith (2025, arXiv 2512.23977) Causify DataFlow: so kết quả batch với streaming.
Không tìm thấy nguồn đặt tên "truncation test" → docstring `ro_ri.py` mô tả cơ chế, không gán tên có trích dẫn;
tài liệu buổi 13 phải nói rõ "không bắt được ≠ không rò".

### D.7 Biểu đồ
- **PIT dữ liệu đếm:** Czado, Gneiting & Held (2009, Biometrics 65): "Here we propose a non-randomized yet uniform
  version of the PIT histogram"; "We prefer to use the non-randomized approach"; "Typically, J = 10 or J = 20
  are good choices." → `tv.ve.pit_histogram` nhận cặp (P_duoi, P_tren); [CHẠY] dự báo Poisson đúng phân phối cho
  cột trong 1 ± 0,15.
- **CORP reliability diagram:** Dimitriadis, Gneiting & Jordan (2021, PNAS 118(8)): "CORP is based on
  non-parametric isotonic regression and implemented via the Pool-adjacent-violators (PAV) algorithm" →
  `reliability_diagram(cach="corp")` mặc định, `cach="bin"` kiểu cổ điển.
- matplotlib 3.11.2: `plt.rc_context` / `matplotlib.style.context` "Context manager for using style settings
  temporarily".

---

## E. Kết quả chạy

- `python tools/kiem_khung.py` [CHẠY 2026-09-17]: hồ sơ **pandas3** (numpy 2.5.3, pandas 3.0.5, scipy 1.18.1,
  matplotlib 3.11.2, scikit-learn 1.9.1) — 65 đạt, 3 bỏ qua (test đối chiếu cần utilsforecast/scoringrules);
  hồ sơ **nixtla** (pandas 2.3.3 + utilsforecast 0.2.16 + scoringrules 0.11.0) — 68 đạt.
- Hồ sơ nixtla in 16 DeprecationWarning "The 'generic' unit for NumPy timedelta is deprecated" phát ra bên trong
  pandas 2.3.3 với numpy 2.5.3 → rủi ro khi nâng numpy; lock chốt nên hiện không ảnh hưởng.
- **Tải toàn danh mục trên cache trắng** [CHẠY 2026-09-17, `tai_danh_muc.py --may-trang`, Python 3.12.3, thư viện chuẩn]:
  **46/46 bộ đã chốt khớp sha256**; bỏ qua `uci-electricity-load`, `m5-kaggle` (cho_sha256). Nhóm không-UCI 41 bộ:
  579,3 MB tải, 18,2 phút (nhật ký `nhat-ky-tai/2026-09-17-205922.md`). Nhóm UCI 5 bộ: 86,7 MB, 3,5 phút
  (`2026-09-17-222430.md`).
- Lần chạy UCI đầu (song song với nhóm kia): 3/5 bộ lỗi "lỗi mạng" sau 6–40 phút ở 3–6 KB/s — máy chủ UCI cắt kết
  nối giữa lúc truyền và không hỗ trợ Range. Chạy lại riêng sau đó: tải 45 MB trong < 60 s. → `lay_du_lieu.py` thêm
  thử lại khi đứt giữa chừng; tốc độ UCI dao động mạnh nên bộ UCI vẫn cần mirror.
- `mirror_hf.py --chuan-bi` [CHẠY]: dựng đúng 34 bộ còn trong cache kèm thẻ dữ liệu; chưa đẩy lên (không có token).
