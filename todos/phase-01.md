# Phase 1 — Khung trợ giúp và danh mục dữ liệu ✅

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 1"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Mọi buổi đều copy khung này vào `tv/` và đều tải dữ liệu qua danh mục này. Sai ở đây là sửa 44 lần.

- [x] **Research Phase 1** — `tools/du-lieu/NGHIEN-CUU.md` (2026-09-17): giấy phép trích nguyên văn ~30 nguồn, công thức
      M5/CRPS/WIS/DM-HLN, backtest, rò rỉ, PIT/CORP. **Lệch lớn đã sửa lộ trình + todos:** FRED cấm dùng cho ML → lấy từ
      BLS/BEA/Fed Board/EIA + Philadelphia Fed (vintage); NOAA ISD Nội Bài dừng + WMO Res 40 → GHCNh; METR-LA không giấy
      phép → Monash Traffic; UCI 321 quá chậm → Monash electricity hourly; Tourism Australia = tsibble GPL-3
- [x] `tools/khung/ve.py` — `bo_bieu_do_chan_doan()` (8 biểu đồ, tự nhận dữ liệu giờ/ngày/tháng), fan chart, PIT histogram
      (không ngẫu nhiên cho dữ liệu đếm — Czado et al. 2009), reliability diagram CORP (PAV) + kiểu bin, small multiples
- [x] `tools/khung/danh_gia.py` — MAE, RMSE, ME, MAPE, sMAPE, WAPE, MASE, RMSSE (+ M5 từ lần bán đầu), WRMSSE, pinball,
      Winkler, coverage, WIS (2 dạng), CRPS mẫu (nrg/fair) + đóng cho chuẩn, Brier + phân rã Murphy, log score, PIT mẫu,
      `bang_chi_so` nhiều chuỗi. **Đối chiếu số khớp utilsforecast 0.2.16 và scoringrules 0.11.0** (ghi rõ khác biệt quy ước)
- [x] `tools/khung/backtest.py` — rolling origin có `gap`, sliding/expanding, `refit` True/False/k (như statsforecast), bảng
      dài có `cutoff`, `buoc_h`; chặn dự báo thừa/thiếu dòng; `diebold_mariano` bản HLN, lùi về h=1 khi phương sai âm (như R)
- [x] **`tools/khung/ro_ri.py`** — `kiem_ro_ri`: cắt tương lai + **nhiễu mục tiêu theo tầm h** (bắt rolling không shift, lag < h);
      `kiem_chia_tap`, `kiem_scaler`, `kiem_chong_lan`. **11 ca phải bắt + 11 ca phải cho qua** + test kiểm phụ
- [x] `tools/khung/du_lieu.py` — `doc_du_lieu(ten)` dạng dài (đọc .tsf Monash, hoặc khai `dang_dai` trong danh mục), `doc_tho`
- [x] `tools/kiem_khung.py` — test khung ở 2 hồ sơ: pandas 3.0.5 (65 đạt, 3 bỏ qua) và pandas 2.3.3 + Nixtla (68 đạt)
- [x] `lab/nen.toml` thêm `khung_bo` — buổi dạy tự viết công cụ không nhận lời giải trong `tv/`
- [x] **`tools/du-lieu/danh-muc.toml`** — 56 bộ (**55 đã chốt sha256**; chỉ còn `m5-kaggle` chờ chấp nhận luật Kaggle) +
      8 nguồn ghi rõ KHÔNG tải tự động (FRED, OpenAQ VN, ISD, BTS, METR-LA, Dominick's, Metaculus, fev/GIFT-Eval)
- [x] **Rà giấy phép từng bộ** — trích nguyên văn trong NGHIEN-CUU.md mục B và trường `trich_giay_phep`
- [x] **Mirror** bộ được phép lên Hugging Face Datasets — **XONG 2026-09-18**: `Tony2202/khoa-forecasting-du-lieu`
      (công khai), commit `105db7d8d51c8ff1229ec06c363f641417124bf3`, **49 bộ / 614 MB**, tệp giữ nguyên byte, thẻ dữ liệu
      ghi giấy phép + nguồn + sha256 từng bộ. 49 dòng `url_mirror` đã vào `danh-muc.toml`; `lay_du_lieu.py` thử mirror trước.
      Kiểm trên cache trắng: 4/4 bộ khớp sha256 (Online Retail II 18,4 s qua mirror thay vì ~5 giờ từ UCI).
      Lần đẩy thứ hai (commit `829f0fab55a5fb5a0b483976d60c402efb2e355a`) thêm `uci-electricity-load`:
      đã tải đủ 261.335.609 byte từ UCI và **chốt sha256** — bộ cuối cùng còn treo từ Phase 1
- [x] Bộ dự phòng mở cho mọi bộ bị hạn chế (M5 → Online Retail II / Car Parts; METR-LA → Traffic hourly; ISD → GHCNh;
      OpenAQ VN → UCI Beijing + Open-Meteo Hà Nội; Metaculus → ForecastBench; Dominick's → Online Retail II)
- [x] `phu-luc/F-nguon-du-lieu.md` sinh từ danh mục (`tools/du-lieu/sinh_phu_luc_f.py`) + PDF
- [ ] Còn cho phase sau: công cụ trích bảng BTS (Phase 4/10); bộ con fev-bench (Phase 15).
      **Đã giải quyết:** Census bán lẻ + BLS thất nghiệp (Phase 3, đã vào danh mục); OpenAQ VN → BỎ (v3 bắt buộc key cho
      mọi endpoint, v2 HTTP 410 — Phase 4 thay bằng GHCNh Nội Bài + Open-Meteo).
      **Còn chặn:** M5 — tài khoản Kaggle `thanh14` đã có key nhưng **chưa chấp nhận luật cuộc thi**
      (`403` từ kagglehub 2026-09-18); cần bấm Join tại kaggle.com/competitions/m5-forecasting-accuracy/rules rồi chạy
      `tools/lay_du_lieu.py` cho buổi 23 để chốt sha256
- [x] **Test: tải toàn bộ danh mục trên cache trắng (`tai_danh_muc.py --may-trang`) — 46/46 bộ đã chốt khớp sha256 (100%)**;
      tải về 666 MB (đặt vào lab ~1,29 GB sau giải nén); nhóm thường 18,2 phút, nhóm UCI 3,5 phút (lần chạy trước UCI
      đứt kết nối giữa chừng → thêm thử lại khi đang truyền). Bỏ qua đúng 2 bộ `cho_sha256`
