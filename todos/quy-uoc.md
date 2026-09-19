# Quy ước xây khoá — đọc trước khi làm bất kỳ phase nào

Tách từ `todos.md` (2026-09-18). `todos.md` chỉ giữ tiêu đề + trạng thái + prompt của mỗi phase; chi tiết từng phase ở
`todos/phase-NN.md`; tiến độ, thứ tự, ước lượng, rủi ro ở `todos/tong-quan.md`.


## Giao thức research — BẮT BUỘC trước mọi phase

Lĩnh vực này đổi rất nhanh (foundation model, LLM, thư viện Nixtla ra bản mới vài tháng một lần).
Kiến thức trong lộ trình chỉ đúng tới ngày rà soát. **Mọi prompt phase trong `todos.md` mở đầu bằng
lệnh chạy khối này — không được bỏ qua, kể cả khi thấy mình đã biết chủ đề:**

```text
BƯỚC 0 — RESEARCH TRƯỚC KHI VIẾT (bắt buộc, không bỏ qua):
1. Với TỪNG buổi/chủ đề của phase: WebSearch + WebFetch tài liệu chính thức, bài báo gốc,
   bài tổng quan và bài phản biện mới nhất (ưu tiên 12 tháng gần đây).
2. Xác minh: phiên bản thư viện mới nhất + API còn đúng (đọc changelog, không đoán);
   dataset còn tải được, URL, dung lượng, GIẤY PHÉP; model/benchmark có bản mới không.
3. Tìm khái niệm/kỹ thuật lộ trình còn THIẾU hoặc đã LỖI THỜI; tìm lỗi hiểu sai phổ biến
   của chủ đề để đưa vào mục "Lỗi thường gặp".
4. Ghi vào buoi-NN/NGHIEN-CUU.md: ngày research, nguồn (URL + ngày truy cập), phiên bản đã
   xác minh, phát hiện mới, điểm lệch so với lộ trình, quyết định đưa/không đưa vào buổi.
5. Lệch lớn (thêm/bỏ chủ đề, đổi dataset, thư viện hỏng) → cập nhật lo-trinh + todos TRƯỚC,
   báo lại người dùng, rồi mới soạn. Lệch nhỏ → ghi trong NGHIEN-CUU.md và làm tiếp.
6. Không viết một câu lý thuyết nào mà chưa đối chiếu được với ít nhất một nguồn đáng tin.
```

## Chuẩn dễ hiểu — BẮT BUỘC cho mọi tài liệu học viên đọc (thêm 2026-09-18)

**Vì sao có mục này.** Người dùng tự học buổi 1–13 và báo: *"tài liệu khó hiểu quá, tôi phải đi search lại
ChatGPT"*. Ví dụ buổi 1 mục 4.8 (dự báo điểm và chi phí lệch): 12 dòng dùng liền "phân phối", "quantile",
"newsvendor", "chi phí thiếu/thừa", "quantile 0,8 của sai số là +0,455" mà **không định nghĩa từ nào**; "thiếu"
không nói thiếu cái gì so với cái gì; câu trích tiếng Anh chen giữa đoạn; ý chính nằm trong công thức (PDF render
công thức thành ảnh → copy ra mất sạch, câu còn lại vô nghĩa); 6 con số trong 3 câu. Người dùng phải hỏi
ChatGPT mới hiểu "thiếu = điện mua ít hơn nhu cầu thực", "quantile 0,8 = mốc mà 80% giá trị nằm dưới", "vì
sao lại là 0,8 = 4/(4+1)".

**Nguyên nhân gốc (sửa ở gốc, không vá từng câu):**
1. Giới hạn 2.500–4.000 chữ + 8–10 mục lý thuyết/buổi → mỗi khái niệm chỉ còn một đoạn nén chặt.
2. Viết như ghi chú nghiên cứu cho người đã biết: trích nguồn **thay cho** giải thích.
3. Dùng khái niệm trước khi dạy (quantile ở buổi 1, buổi 2 mới dạy).
4. Definition of Done chỉ kiểm bằng máy (test, số trang) — không có bước "người mới đọc có hiểu không".

**Người đọc mục tiêu:** biết Python cơ bản + toán phổ thông; **chưa** học thống kê đại học; **chưa** biết
forecasting; tự học một mình, không có giảng viên bên cạnh. **Tiêu chí: đọc xong không phải tra ngoài.**

**Quy tắc D1–D13** (chi tiết + ví dụ trước/sau: `tools/CHUAN-DE-HIEU.md`, làm ở Phase 5; D13 thêm ở Phase 7):

| # | Quy tắc |
|---|---|
| D1 | **Từ mới**: lần đầu xuất hiện → định nghĩa bằng lời thường ngay câu đó hoặc câu kế (1–2 câu) + ví dụ đời thường. Thuật ngữ tiếng Anh giữ nguyên nhưng lần đầu phải kèm nghĩa tiếng Việt. Đầu mục Lý thuyết có bảng **"Từ mới trong buổi"** (thuật ngữ · nghĩa một câu · ví dụ) |
| D2 | **Khuôn mỗi khái niệm** (thay nhịp cũ): *Vấn đề* (câu hỏi thực tế nào cần nó) → *Trực giác* (ví dụ đời thường) → **Ví dụ số nhỏ tính tay** (5–10 số, cầm bút làm được) → *Hình* → *Công thức* → *Nói bằng lời* → *NumPy* → *Thư viện* → *Dữ liệu thật* → **Tóm lại** (1–3 câu in đậm) |
| D3 | **Công thức**: mọi ký hiệu giải thích ngay dưới ("$q$ là …"); ngay sau là một câu diễn đạt công thức bằng lời **có thay số**. Công thức không bao giờ mang ý chính một mình |
| D4 | **Không nói lửng**: "thiếu/thừa", "sai số dương", "cao hơn", "tốt hơn" luôn nói rõ *so với cái gì, đơn vị gì*. Quy ước dấu sai số (sai số = thực tế − dự báo) nhắc lại mỗi lần dùng dấu |
| D5 | **Chưa dạy thì chưa dùng.** Buộc phải dùng sớm → hộp **"Mượn trước"**: 2–4 câu + ví dụ số nhỏ + "buổi N học kỹ" (chỉ nhắc tên buổi, không trỏ file) |
| D6 | **Trích nguồn**: không chen trích nguyên văn tiếng Anh vào lý thuyết. Diễn giải tiếng Việt, nguồn ghi gọn trong ngoặc (FPP §5.2). Nguyên văn chỉ khi câu chữ gốc quan trọng — tối đa 1 lần/mục, kèm bản dịch. Lịch sử, tên bài báo, định lý → "Đọc thêm" |
| D7 | **Mật độ**: câu ≤ ~30 chữ, một ý một câu; một đoạn ≤ 3 con số **kết quả** — nhiều hơn thì làm bảng (phép tính từng bước và dãy dữ liệu của ví dụ nhỏ không tính); không viết tắt tự chế ("TB 4 tuần" → "trung bình của 4 tuần trước, cùng giờ") |
| D8 | **Mỗi hình** có khối "Cách đọc hình" theo thứ tự: trục ngang → trục dọc (đơn vị) → màu/đường nào là gì → nhìn vào đâu → kết luận. **Mỗi bảng kết quả** có "Đọc bảng": so dòng nào với dòng nào, kết luận, vì sao |
| D9 | **≤ 6 khái niệm chính** trong Lý thuyết. Phần học thuật/mở rộng → hộp **"Nâng cao — có thể bỏ qua lần đọc đầu"** hoặc "Đọc thêm". Hết chỗ thì **bỏ bớt nội dung, không nén chữ** |
| D10 | Mỗi mục lý thuyết kết thúc bằng 1 câu **"Tự kiểm tra"**, đáp án trong `<details>` |
| D11 | **Lab**: trước mỗi bước nói "bước này để làm gì / sẽ thấy gì"; sau bước nói "thấy X nghĩa là Y, thấy Z thì kiểm lại …" |
| D12 | **Quiz**: đáp án giải thích *vì sao đúng* và *vì sao các lựa chọn khác sai*; trả lời được chỉ bằng tài liệu buổi đó |
| D13 | **Gọn — mỗi ý nói một lần** (thêm 2026-09-18, xem dưới). Dễ hiểu nhờ *đúng chỗ*, không nhờ *nhiều chữ* |

**D13 — Gọn (thêm 2026-09-18).** Người dùng đọc bản viết lại buổi 1–3: *"dễ hiểu hơn nhưng dài dòng quá"*. Nguyên nhân:
mỗi vòng đọc thử chỉ **thêm** giải thích, không ai **bỏ**; khuôn D2 bị hiểu là phải đủ 10 bước cho mọi khái niệm.
Sau Phase 6, buổi 1–3 có 6.900–9.000 chữ ngoài bảng/code (19–22 trang), Phụ lục B 12.500 chữ / 30 trang. Quy tắc:
- **Mỗi ý một lần.** Không nói lại cùng ý ở "Vấn đề", thân bài, "Tóm lại", Lab và "Lỗi thường gặp". "Tóm lại" ≤ 3 câu,
  không chép lại câu phía trên; Lab trỏ về khái niệm ("xem M3") thay vì giải thích lại.
- **Không câu rỗng**: bỏ câu dẫn/rào đón/chuyển tiếp không mang thông tin ("Như đã nói ở trên", "Điều quan trọng cần
  lưu ý là", "Trong phần này ta sẽ tìm hiểu", "Nói cách khác" rồi nói lại y hệt), bỏ lời khen/nhấn ("rất quan trọng").
- **Một ví dụ đủ thì không thêm cái thứ hai.** Ví dụ thứ hai chỉ khi nó cho thấy điều ví dụ đầu không cho thấy.
- **Khuôn D2 là trần, không phải sàn**: bước nào không thêm hiểu biết thì bỏ (NumPy và thư viện gộp làm một khối; khái
  niệm đơn giản không cần hình riêng). Chỉ "ví dụ số nhỏ" và "Tóm lại" là bắt buộc.
- **Không giải thích cái người đọc đã biết** (Python cơ bản, toán phổ thông) hay cái buổi này không dùng.
- **Sửa chỗ khó bằng cách viết lại câu đó cho rõ, không chèn thêm đoạn.** Mỗi lần thêm chữ sau đọc thử phải tìm chỗ bỏ bù.
- **Phép thử mỗi đoạn**: "Bỏ đoạn này thì học viên mất gì?" — không mất gì → xoá; mất một câu → giữ đúng một câu đó.
- **Tường minh quá cũng là khó hiểu** (người dùng, 2026-09-18). Giải thích mọi cờ lệnh, mọi ngoại lệ, mọi chi tiết phụ
  làm ý chính chìm mất. Chỉ viết cái người đọc cần để hiểu ý chính hoặc làm bước tiếp theo; chi tiết còn lại để trong
  code/comment hoặc bỏ.
- **Công cụ phải giải thích dài thì sửa công cụ, không viết thêm.** Ví dụ: lệnh `env -u VIRTUAL_ENV uv run --no-sync
  --project 00-nen python …` cần 4 gạch giải thích → thay bằng `python lab.py chay …`; Makefile + jupytext → `lab.py`
  + `code/lab.ipynb` phát sẵn.

**Độ dài mới** (từ Phase 7, thay 4.000–9.000): `tai-lieu.md` **3.500–6.500 chữ** ngoài bảng/code, PDF **10–18 trang**; phụ lục
≤ 18 trang. Phase 7 đo lại trên buổi 1–3 đã rút gọn rồi chốt số trong `kiem_de_hieu.py` + `xuat_pdf.py --kiem`.

**Độ dài Phase 5–6** (thay 2.500–4.000 chữ / 10–16 trang; từ Phase 7 thay bằng trần D13 ở trên): `tai-lieu.md` **4.000–9.000 chữ** (đếm chữ ngoài bảng và code — `kiem_de_hieu.py`, mã `do_dai`), PDF **12–24 trang**.
Giới hạn thật là số khái niệm (D9), không phải số chữ.

**Phản hồi của người học:** `phan-hoi-hoc-vien.md` ở gốc repo — người dùng ghi đoạn khó hiểu khi học (buổi, mục,
câu, đã phải hỏi gì). Mọi phase soạn/viết lại **đọc file này trước**.

Mọi prompt phase soạn nội dung từ Phase 5 trở đi trỏ tới khối này — **không tick ✅ khi chưa đạt**:

```text
BƯỚC CUỐI — ĐỌC THỬ NHƯ HỌC VIÊN MỚI (bắt buộc trước khi tick ✅):
1. Đọc phan-hoi-hoc-vien.md — mọi đoạn người dùng đã báo khó hiểu của buổi này phải được sửa.
2. Tự rà tai-lieu.md theo D1–D13 (todos/quy-uoc.md mục "Chuẩn dễ hiểu", tools/CHUAN-DE-HIEU.md) và
   chạy tools/kiem_de_hieu.py NN; sửa hết.
3. TỰ ĐỌC THỬ (không dùng subagent) — một lượt riêng, đọc lại TOÀN BỘ tai-lieu.md bằng Read từ đầu tới cuối,
   đóng vai học viên mới theo đúng checklist "Prompt đọc thử" trong tools/CHUAN-DE-HIEU.md (biết Python + toán
   phổ thông, chưa học thống kê đại học; tại mỗi đoạn chỉ được dùng những gì tài liệu đã viết TRƯỚC đoạn đó; mọi
   ý dựa vào hiểu biết ngoài tài liệu là chỗ vướng). Ghi ra: (A) bảng chỗ vướng chặn/khó/nhỏ; (B) giải thích lại
   từng khái niệm chính bằng một ví dụ số MỚI tự nghĩ; (C) với từng câu quiz, chỉ ra câu/mục tài liệu chứa căn cứ
   trả lời (không có căn cứ = câu hỏng); (E) chỗ thấy dài/lặp.
   Chống thiên vị của người viết: tính lại MỌI con số và đáp án quiz bằng Python/output thật (đọc thử đã bắt được
   đáp án sai, câu sai số học, và 3 lỗi do chính việc cắt gây ra); với từng thuật ngữ, grep vị trí định nghĩa
   đầu tiên so với vị trí dùng đầu tiên; không đánh giá "hiểu được" dựa trên việc mình đã biết.
4. Đạt khi: 0 chỗ CHẶN; ≤ 5 chỗ KHÓ; mục B không khái niệm nào giải thích không nổi; mọi câu quiz có căn cứ
   trong tài liệu (quiz là điều kiện cần — bản cũ buổi 1, 7, 12 đều làm được quiz dù 9–12 chỗ chặn).
   Chưa đạt → sửa → tự đọc thử lại một lượt MỚI, toàn bộ tài liệu (không chỉ chỗ vừa sửa).
   Sửa chỗ vướng bằng cách viết lại câu cho rõ, KHÔNG chèn thêm đoạn (D13).
5. TỰ RÀ GỌN (D13) — sau khi đọc thử đạt, một lượt đọc RIÊNG với vai biên tập viên theo checklist "Prompt biên
   tập gọn" trong tools/CHUAN-DE-HIEU.md: liệt kê đoạn lặp ý / câu rỗng / ví dụ thừa / bước khuôn D2 thừa /
   giải thích điều đã biết, mỗi chỗ kèm đề xuất cắt; tôn trọng danh sách KHÔNG được cắt. Cắt xong:
   kiem_de_hieu.py sạch (kể cả trần độ dài), rồi tự đọc thử lại (bước 3) để chắc cắt không làm hỏng hiểu.
   Đạt khi: lượt rà cuối còn ≤ 3 chỗ thừa đáng kể VÀ đọc thử vẫn đạt bước 4.
6. Ghi vào buoi-NN/NGHIEN-CUU.md mục "Đọc thử": ngày, số vòng, chặn/khó/nhỏ, quiz, số chữ trước/sau rà gọn,
   đã sửa thế nào.
```

## KHỐI CHUNG — mọi prompt phase trong `todos.md` chạy theo khối này (2026-09-18)

Prompt từng phase chỉ ghi phần **riêng**; mọi yêu cầu chung nằm ở đây. Không dùng subagent: mỗi phase soạn chỉ 1–2 buổi;
sau mỗi cụm có phase **DT** (đọc thử độc lập, phiên mới); cụm đổi nhanh có phase **RS** (research riêng) trước khi soạn. Đọc trước: `CLAUDE.md`, mục này, `todos/phase-NN.md`
(checklist + "Bắt buộc"), `phan-hoi-hoc-vien.md`, `tools/CHUAN-DE-HIEU.md`. Phase viết lại: đọc thêm mục "Đọc thử"/"Rút gọn"
trong `NGHIEN-CUU.md` buổi 1–3 (chỗ đã sửa, đã cắt).

**R — Research (BƯỚC 0, không bỏ qua).** Buổi mới: đủ 6 bước "Giao thức research" (trên) + "Research riêng" trong prompt.
Viết lại: research sư phạm — mỗi khái niệm chính 2–3 cách giải thích tốt + hiểu lầm phổ biến, ghi `NGHIEN-CUU.md` mục
"Research viết lại" (nguồn + ngày); chỉ rà phiên bản khi đổi code. Lệch lớn so với lộ trình → cập nhật lo-trinh + todos và
**báo người dùng TRƯỚC** khi soạn.

**V — Viết, từng buổi.**
1. Viết lại: đọc thử bản cũ trước (baseline chỗ vướng + quiz).
2. ≤ 6 khái niệm chính; thừa → "Nâng cao"/"Đọc thêm"/bỏ. Không nén chữ, không độn chữ.
3. D1–D13 ngay từ đầu: bảng "Từ mới"; ví dụ số nhỏ tính tay TRƯỚC dữ liệu thật; công thức + ký hiệu + "Nói bằng lời" có thay
   số; mỗi hình "Cách đọc hình" 5 bước (bước 5 là câu kết luận thật, không "như tiêu đề"); mỗi bảng số "Đọc bảng" (so gì →
   kết luận, không kể lại ô); mỗi mục "Tóm lại" ≤ 3 câu + "Tự kiểm tra"; chưa dạy → "Mượn trước".
4. **Dễ hiểu nhưng gọn**: mỗi ý một lần; khuôn D2 là trần; không câu rỗng. **Tường minh quá cũng là khó hiểu**: chỉ viết cái
   cần để hiểu ý chính hoặc làm bước kế, không giải thích mọi cờ/ngoại lệ. **Công cụ cần giải thích dài → sửa công cụ.** Sửa
   chỗ vướng bằng viết lại câu, không chèn đoạn. Không bỏ ngày/số cụ thể chỉ để qua bộ đếm.
5. Trần 3.500–6.500 chữ ngoài bảng/code, PDF 10–18 trang. Chỉ vượt khi đọc thử chứng minh cắt thêm làm khó hiểu lại — ghi lý do
   trong `NGHIEN-CUU.md` (tiền lệ: buổi 2, +44 chữ).
6. `kiem-tra.md` 10 câu (4 nhắc lại, 4 vận dụng, 2 đọc biểu đồ/bảng tìm chỗ sai); đáp án nói vì sao đúng + vì sao lựa chọn
   khác sai; trả lời được chỉ bằng tài liệu buổi đó.

**L — Lab.** Theo `CLAUDE.md` "Quy tắc soạn nội dung": buổi tự chứa; nền sinh bằng `sinh_nen.py` (không sửa tay `00-nen/`,
`lab/lab.py`); chỗ hở cố ý đúng bảng cuối file — `code/` sai đúng chỗ, `dap-an/` sửa; từ buổi 12 `cham/` có test rò rỉ; mọi
số từ lần chạy thật (seed); hình sinh bằng `dap-an/ve_hinh.py`; chốt phiên bản/revision; CPU chạy được; dữ liệu có giấy phép
trong danh mục; mọi mô hình so seasonal naive trên backtest rolling origin; foundation model/LLM chỉ đánh giá sau mốc cắt.
Học viên chạy `python lab.py up [--pip] | check [--dap-an] | notebook | down` (conda/pip qua `--pip`). Code Lab trong
`code/lab.ipynb` (soạn bằng `tools/nb.py`, commit không output); tài liệu trỏ "ô bước N" + output cần đọc, không chép code dài,
không giải thích cờ lệnh. Viết lại: GIỮ NGUYÊN chỗ hở, `cham/`, `00-nen/`, dữ liệu, số cũ.

**Đ — Tự đọc thử + tự rà gọn (BƯỚC CUỐI; KHÔNG dùng subagent; không tick ✅ khi chưa đạt).** Chạy khối "BƯỚC CUỐI" ở mục
"Chuẩn dễ hiểu": lượt đọc riêng vai học viên mới theo checklist "Prompt đọc thử" → 0 chặn, ≤ 5 khó, mọi câu quiz có căn cứ trong
tài liệu, không khái niệm giải thích không nổi; rồi lượt đọc riêng vai biên tập viên theo "Prompt biên tập gọn" → ≤ 3 chỗ thừa
đáng kể. Mỗi lượt đọc lại TOÀN BỘ file, chỉ dùng những gì tài liệu đã viết trước chỗ đang đọc; tính lại mọi con số/đáp án bằng
Python/output thật. **Mọi lượt cắt/sửa sau đó → tự đọc thử lại** (Phase 7: 3 lỗi do chính việc cắt gây ra). Cắt lặp, câu rỗng
thì an toàn; cắt mắt xích "vì sao" thì đọc thử bắt lại. Văn bản không phải buổi (đề, rubric, câu hỏi, README): tự đọc trong vai
học viên đã học tới buổi tương ứng, viết lại được đúng "làm gì, nộp gì, chấm thế nào", 0 chỗ mơ hồ; rà gọn ≤ 3; không lặp giữa
đề/rubric/hướng dẫn.

**DT — Phase đọc thử độc lập** (sau mỗi cụm buổi; thay cho "mắt mới" của subagent). Dán prompt trong **phiên MỚI**
(`/clear` hoặc chat mới — không mang ngữ cảnh phiên soạn). Với từng tài liệu của cụm, theo thứ tự:
1. Tạo bản quiz bỏ đáp án (lệnh ở `tools/CHUAN-DE-HIEU.md`). Chỉ mở `tai-lieu.md` + bản quiz đó; **KHÔNG** mở `dap-an/`,
   `NGHIEN-CUU.md`, `code/`, `kiem-tra.md` gốc trước khi viết xong đánh giá.
2. Đọc toàn bộ theo checklist "Prompt đọc thử", làm quiz **mù**; viết bảng A–E vào `NGHIEN-CUU.md` mục "Đọc thử độc lập".
3. Rồi mới mở đáp án chấm quiz (kiểm cả đáp án của ta bằng Python), sửa chỗ vướng (viết lại câu), tự rà gọn, chạy X.
Đạt: 0 chặn, ≤ 5 khó, quiz mù ≥ 9/10, ≤ 3 chỗ thừa. Có sửa → tự đọc thử lại toàn bộ tài liệu đó. Tài liệu chưa đạt thì phase
DT chưa ✅. Văn bản không phải buổi: viết lại được đúng "làm gì, nộp gì, chấm thế nào", 0 chỗ mơ hồ.

**RS — Phase research riêng** (cụm đổi nhanh: deep learning, foundation model & LLM). Chỉ research, chưa soạn: đủ 6 bước
"Giao thức research" + danh sách trong prompt, cho từng buổi của cụm; ghi `buoi-NN/NGHIEN-CUU.md` (tạo thư mục buổi từ
khuôn nếu chưa có) + bảng "lộ trình ↔ hiện tại ↔ quyết định"; lệch lớn → cập nhật lo-trinh + todos, **báo người dùng**.
Phase soạn sau đọc các `NGHIEN-CUU.md` đó và chỉ rà bổ sung (research cũ hơn 1 tháng thì rà lại phần phiên bản/model).

**X — Xong phase.** `ruff check .` → `kiem_de_hieu.py NN` (0 vi phạm hoặc có lý do) → `kiem_tra_lab.py NN` (đáp án xanh, `code/`
đỏ đúng chỗ, `lab.ipynb` chạy hết; check < 10 phút CPU 4 nhân) → `kiem_tra_doc_lap.sh` → `xuat_pdf.py NN` + `--kiem` → ghi
`NGHIEN-CUU.md` mục "Đọc thử" (vòng, chặn/khó/nhỏ, quiz, chữ/trang trước → sau) → 🔲→✅ ở `todos.md` + `phase-NN.md` +
`tong-quan.md` → báo người dùng bảng trước/sau.

## Cấu trúc thư mục đích

```text
.                                   gốc repo /home/tony/Tony/Forecasting/
├── README.md                       bản đồ khoá, bảng 44 buổi, học theo cụm
├── CLAUDE.md                       quy tắc soạn nội dung cho phiên làm việc sau
├── todos.md                        tiêu đề + trạng thái + prompt mỗi phase (autoclick theo dõi)
├── todos/quy-uoc.md                quy ước này
├── todos/tong-quan.md              Progress Summary, thứ tự làm, ước lượng, rủi ro
├── todos/phase-NN.md               chi tiết từng phase (checklist, "Bắt buộc", ghi chú research)
├── phan-hoi-hoc-vien.md            người học ghi đoạn khó hiểu — mọi phase soạn/viết lại đọc trước
├── lo-trinh/                       lộ trình 44 buổi (.md + .pdf)
├── MOI-TRUONG.md                   cài uv/Python/Jupyter, API key OpenAQ/EIA/Kaggle, Ollama — Linux/macOS/WSL2
├── phu-luc/                        phụ lục dùng chung, mọi buổi TRỎ TỚI thay vì lặp lại
│   ├── A-python-chuoi-thoi-gian.md
│   ├── B-xac-suat-toi-thieu.md
│   ├── C-so-tay-doc-bieu-do.md     mỗi loại biểu đồ: đọc gì, bẫy gì, ví dụ đúng/sai
│   ├── D-cong-thuc-chi-so.md       MAE…CRPS, WIS, Brier — công thức + khi nào dùng
│   ├── E-tu-dien-thuat-ngu.md
│   └── F-nguon-du-lieu.md          MỌI bộ dữ liệu: URL, giấy phép, được mirror không, sha256
├── buoi-01/ … buoi-44/             MỖI THƯ MỤC TỰ CHỨA — không trỏ ra ngoài chính nó
│   ├── tai-lieu.md                 NGUỒN của PDF  ← chỉ sửa ở đây
│   ├── <CHU-DE>-buoi-NN.pdf        sinh ra
│   ├── NGHIEN-CUU.md               nhật ký research (BƯỚC 0) — KHÔNG vào zip
│   ├── hinh/                       ảnh dùng trong tài liệu, sinh bằng dap-an/ve_hinh.py (không vẽ tay)
│   ├── code/                       ĐIỂM XUẤT PHÁT chạy được (có chỗ hở cố ý), .py dạng percent
│   │   └── README.md
│   ├── dap-an/                     bản hoàn chỉnh — KHÔNG vào zip
│   ├── lab/
│   │   ├── nen.toml                buổi cần thư viện nào, bộ dữ liệu nào (VIẾT TAY — nguồn của 00-nen/)
│   │   ├── 00-nen/                 NỀN của buổi (sinh bằng tools/sinh_nen.py)
│   │   │   ├── pyproject.toml      phụ thuộc CHỐT phiên bản
│   │   │   ├── uv.lock
│   │   │   ├── du-lieu.toml        URL + sha256 + giấy phép + khoảng thời gian cố định
│   │   │   ├── tv/                 thư viện trợ giúp COPY từ tools/khung/, cài editable — `import tv`
│   │   │   ├── lay_du_lieu.py      BẢN SAO tools/lay_du_lieu.py
│   │   │   └── requirements.txt    cùng phiên bản, cho người dùng conda/pip (lab.py up --pip)
│   │   ├── du-lieu/raw/            dữ liệu đã kiểm sha256, chỉ đọc (gitignore)
│   │   ├── cham/                   test_*.py — bộ chấm của `python lab.py check`
│   │   └── lab.py                  SINH TỰ ĐỘNG: up [--pip] / check [--dap-an] / chay / notebook / down
│   └── kiem-tra.md                 10 câu quiz + đáp án trong <details>
├── du-an-giua-chang/
│   ├── 01-eda-lam-sach/            đề, rubric, bộ chấm, lỗi cài sẵn (giám khảo giữ)
│   └── 02-thi-du-bao/              đề, rubric, bộ chấm dữ liệu tương lai, leaderboard
├── du-an-cuoi/                     3 đề A/B/C, rubric 100+20, bộ chấm, "ngày dữ liệu hỏng"
├── danh-gia/                       ngân hàng câu hỏi, đề giữa khoá, đề cuối khoá
├── phat-de/                        sinh ra: buoi-NN.zip (gitignore)
├── pyproject.toml                  cấu hình ruff (KHÔNG phải dự án, KHÔNG workspace)
└── tools/
    ├── NGHIEN-CUU.md               research Phase 0
    ├── CHUAN-DE-HIEU.md            chuẩn dễ hiểu D1–D13, ví dụ trước/sau, mẫu chuẩn, prompt đọc thử + biên tập gọn
    ├── kiem_de_hieu.py             kiểm máy phần đo được của D1–D13
    ├── requirements.txt            phụ thuộc của bộ công cụ
    ├── nen/phien-ban.toml          phiên bản CHUNG mọi thư viện + exclude-newer + [[rang_buoc]]
    ├── khuon-buoi/                 khuôn một buổi: cp -r tools/khuon-buoi buoi-NN
    ├── xuat_pdf.py                 md → PDF: công thức LaTeX → SVG, ảnh, bìa + mục lục, --kiem số trang
    ├── dong_goi.py                 zip cho học viên, loại dap-an/, NGHIEN-CUU.md, lời giải
    ├── sinh_nen.py                 sinh buoi-NN/lab/00-nen/ từ tools/khung/ + danh mục dữ liệu
    ├── lay_du_lieu.py              tải theo du-lieu.toml, kiểm sha256, cache ~/.cache/khoa-forecasting/
    ├── kiem_tra_doc_lap.sh         CHẶN tham chiếu chéo, phụ thuộc không chốt, dữ liệu không sha256
    ├── kiem_tra_lab.py             chạy lab.py up/check/down + code/lab.ipynb mọi buổi, in bảng
    ├── kiem_ro_ri.py               kiểm rò rỉ tương lai tự động (dùng trong cham/ của mọi buổi)
    ├── khung/                      NGUỒN của tv/: ve.py, danh_gia.py, backtest.py, ro_ri.py, du_lieu.py
    └── du-lieu/danh-muc.toml       danh mục gốc mọi bộ dữ liệu của khoá
```

## Nguyên tắc nội dung

1. **Mỗi buổi tự chứa — không có ngoại lệ.** Buổi N **không đọc một byte nào ngoài `buoi-NN/`**
   (trừ cache dữ liệu tải về có kiểm sha256). Không `../buoi-06/...`, không "dùng lại dữ liệu đã
   làm sạch ở buổi trước", không import từ `tools/`. Học viên nghỉ một buổi vẫn học được.
2. **Cơ chế `lab/00-nen/`** — nền của buổi:
   - `pyproject.toml` + `uv.lock` **riêng mỗi buổi**, Python 3.12, chỉ cài thư viện buổi đó cần
   - `du-lieu.toml`: mỗi bộ dữ liệu có URL, **sha256**, giấy phép, **khoảng thời gian cố định**
     (không "lấy tới hôm nay" — trừ bài dự báo trực tiếp có ghi rõ)
   - `tv/` là **bản copy** của `tools/khung/`, sinh bằng `python tools/sinh_nen.py N`.
     Sửa khung → chạy lại tool cho mọi buổi, **không sửa tay trong tv/**
   - Buổi cần dữ liệu đã xử lý (ví dụ PM2.5 đã làm sạch) → **tự làm sạch trong 00-nen/** hoặc tải
     bản mirror có sha256, không đọc từ buổi khác
3. **Phụ thuộc là kiến thức, không phải file** — cần kiến thức buổi khác thì trỏ `phu-luc/` hoặc
   tóm tắt tại chỗ.
4. **Chỗ hở cố ý** — `code/` phải sai đúng chỗ bài học hôm đó sửa (bảng dưới). Chỗ hở phổ biến
   nhất của khoá này là **rò rỉ tương lai** và **đánh giá không trung thực** — `code/` phải cho
   kết quả *đẹp giả tạo* để học viên tự phát hiện. Đừng sửa trước giờ dạy.
5. **Mọi lệnh và mọi con số trong tài liệu phải đã chạy thật.** Không có "sai số giảm khoảng 20%"
   viết cho đẹp — con số lấy từ output thật, ghi seed.
6. **Chốt phiên bản** — mọi thư viện chốt trong `uv.lock`, mọi model chốt theo **revision/commit
   trên Hugging Face**, mọi LLM chốt tên model đầy đủ có ngày. Không `latest`.
7. **Dữ liệu và giấy phép** —
   - CC BY / CC0 / public domain: được **mirror** (Hugging Face Datasets của khoá) kèm ghi nguồn → lab ổn định
   - Giấy phép cấm phân phối lại (Kaggle M5…): học viên **tự tải** bằng tài khoản mình; luôn có dữ liệu dự phòng mở
   - Không commit dữ liệu vào git. Ghi đủ ở Phụ lục F
8. **Chạy được bằng CPU** — mọi lab có nhánh CPU. GPU chỉ làm nhanh hơn. Buổi 36–37: nhánh model
   mở chạy local + **bản ghi phản hồi LLM** (`ghi-am/`) để chấm lại không cần API key.
9. **Tái lập** — seed cố định, `python lab.py check` chạy hai lần ra cùng kết quả (DL/LLM: cho phép sai số
   nhỏ có ghi ngưỡng trong test).
10. **Tài liệu tiếng Việt, thuật ngữ kỹ thuật giữ nguyên tiếng Anh** (backtest, seasonal naive,
    quantile, drift...). Thuật ngữ thống nhất theo Phụ lục E.
11. **Khung tài liệu mỗi buổi** (bắt buộc đủ **9 mục**):
    Mục tiêu → Nhắc lại buổi trước → **Trạng thái đầu buổi** → Lý thuyết → Lab từng bước →
    Lỗi thường gặp & cách chẩn đoán → Bài tập về nhà → Tiêu chí "Xong khi" → Đọc thêm.
    - *Lý thuyết* mỗi khái niệm theo khuôn D2 (mục "Chuẩn dễ hiểu"): **vấn đề → trực giác → ví dụ số nhỏ tính
      tay → hình → công thức ($$...$$) → nói bằng lời → NumPy → thư viện → dữ liệu thật → tóm lại**; mở đầu bằng
      bảng "Từ mới trong buổi"; ≤ 6 khái niệm chính
    - *Nhắc lại buổi trước* đủ để **không cần** mở lại buổi trước
    - *Trạng thái đầu buổi* là bảng liệt kê chính xác sau `python lab.py up`: dữ liệu nào (file, số dòng,
      khoảng thời gian, sha256 rút gọn), môi trường (Python + thư viện chính), `code/` có gì,
      **cái gì đang cố tình sai và triệu chứng nhìn thấy**
    - *Đọc thêm* trỏ chương FPP tương ứng (bảng đối chiếu trong lộ trình) + bài báo gốc
12. **Hình ảnh** — mọi biểu đồ trong tài liệu sinh bằng script trong `dap-an/ve_hinh.py`, lưu
    `hinh/*.png` (150 dpi). Biểu đồ phải qua chính chuẩn của buổi 4: tiêu đề nói kết luận, trục có đơn vị.
13. **Độ dài** — `tai-lieu.md` 3.500–6.500 chữ ngoài bảng/code (`kiem_de_hieu.py`, chốt ở Phase 7), PDF 10–18 trang
    (`python tools/xuat_pdf.py --kiem`). Giới hạn thật là **≤ 6 khái niệm chính** — thừa thì bỏ bớt hoặc chuyển
    "Nâng cao", **không nén chữ** (bài học 2026-09-18: nén 10 khái niệm vào 4.000 chữ làm người dùng phải hỏi ChatGPT)
    — và **không độn chữ** (bài học 2026-09-18: viết lại buổi 1–3 lên 9.000–12.000 chữ thì dài dòng, D13).
14. **Dễ hiểu và gọn là tiêu chí nghiệm thu**, ngang với test xanh — theo D1–D13 và BƯỚC CUỐI "Đọc thử" + "Rà gọn"
    (mục "Chuẩn dễ hiểu").

## Deliverable của MỖI buổi (Definition of Done)

- [ ] **`NGHIEN-CUU.md`** — BƯỚC 0 đã chạy: nguồn có ngày, phiên bản đã xác minh, điểm lệch
- [ ] `tai-lieu.md` đủ **9 mục**, có "Trạng thái đầu buổi", công thức render đúng trong PDF
- [ ] **Đạt D1–D13** (`tools/kiem_de_hieu.py NN` sạch, trong trần độ dài) và **rà gọn đạt** (≤ 3 chỗ thừa) và **đọc thử đạt** (tự đọc, không subagent): 0 chỗ chặn, ≤ 5
      chỗ khó, không khái niệm nào giải thích không nổi, mọi câu quiz có căn cứ trong tài liệu; ghi mục "Đọc thử" trong
      `NGHIEN-CUU.md`; đã xử lý `phan-hoi-hoc-vien.md`
- [ ] `code/` chạy được, có chỗ hở cố ý, có `README.md` ngắn
- [ ] `dap-an/` là bản đã sửa, `python lab.py check --dap-an` xanh
- [ ] `lab/00-nen/` dựng đúng nền **từ máy trắng** (`uv sync --frozen` + dữ liệu qua sha256)
- [ ] `lab/lab.py` chạy `up` / `check` / `down` (và `up --pip`); `up` < 10 phút khi đã có cache, `check` < 10 phút trên CPU 4 nhân
- [ ] `lab/cham/` có **test rò rỉ** (dùng `kiem_ro_ri`) cho mọi buổi từ 12 trở đi
- [ ] `kiem-tra.md` 10 câu: 4 nhắc lại khái niệm, 4 vận dụng (tính/chọn phương pháp), **2 đọc
      biểu đồ/bảng kết quả tìm chỗ sai**; đáp án trong `<details>`
- [ ] `ruff check` sạch; `code/lab.ipynb` phát sẵn, commit không output, chạy hết không lỗi
- [ ] `tools/kiem_tra_doc_lap.sh` xanh
- [ ] PDF sinh ra, mở kiểm tra bảng, khối code, **công thức**, ảnh; 10–18 trang
- [ ] Chạy thử toàn bộ lab trên **máy/venv trắng** một lần trước khi tick ✅

## 44 buổi, tên PDF và chỗ hở cố ý

| Buổi | Chủ đề | PDF | Chỗ hở cố ý trong `code/` |
|---|---|---|---|
| 01 | Forecasting là gì | `GIOI-THIEU-buoi-01.pdf` | Đánh giá dự báo trên chính dữ liệu đã dùng để làm nó; không có baseline |
| 02 | Xác suất & thống kê | `XAC-SUAT-THONG-KE-buoi-02.pdf` | Khoảng "±1.96σ" cho dữ liệu lệch phải, bootstrap i.i.d. cho dữ liệu tự tương quan |
| 03 | Dữ liệu thời gian | `DU-LIEU-THOI-GIAN-buoi-03.pdf` | Timestamp naive, thời tiết lệch múi giờ 5 giờ, resample làm mất giờ DST |
| 04 | Đọc & vẽ biểu đồ | `BIEU-DO-buoi-04.pdf` | Chỉ có biểu đồ đường thô + trục kép + trục y cắt; bỏ lỡ mùa vụ tuần |
| 05 | Biến đổi & điều chỉnh | `BIEN-DOI-DIEU-CHINH-buoi-05.pdf` | So tháng không chỉnh số ngày/lạm phát; log–exp không hiệu chỉnh bias |
| 06 | Phân rã | `PHAN-RA-buoi-06.pdf` | Classical decomposition chu kỳ 24 cho dữ liệu có mùa vụ tuần |
| 07 | Tự tương quan & tính dừng | `TU-TUONG-QUAN-buoi-07.pdf` | Kết luận "dừng" chỉ bằng ADF, sai phân thừa |
| 08 | Tương quan giữa các chuỗi | `TUONG-QUAN-CHEO-buoi-08.pdf` | Kết luận từ Pearson giữa hai chuỗi có xu hướng; CCF chưa prewhiten; Granger = nhân quả |
| 09 | Đặc trưng & khả năng dự báo | `DAC-TRUNG-CHUOI-buoi-09.pdf` | Tune mô hình đều cho mọi chuỗi, kể cả chuỗi entropy cao không dự báo được |
| 10 | Làm sạch & dữ liệu thiếu | `LAM-SACH-DU-LIEU-buoi-10.pdf` | `fillna(0)` cho cảm biến mất tín hiệu; bỏ qua mốc thời gian thiếu hẳn; nội suy hai chiều trước khi chia tập |
| 11 | Ngoại lai & điểm gãy | `NGOAI-LAI-DIEM-GAY-buoi-11.pdf` | Xoá mọi điểm > 3σ toàn chuỗi — xoá luôn Tết; không phát hiện level shift COVID |
| 12 | Khử nhiễu & miền tần số | `KHU-NHIEU-TAN-SO-buoi-12.pdf` | Feature từ rolling centered + `filtfilt` → backtest đẹp giả tạo; hạ mẫu không lọc gây aliasing |
| 13 | Feature & chống rò rỉ | `FEATURE-RO-RI-buoi-13.pdf` | Rolling không `shift`, scaler fit toàn bộ, nhiệt độ thực tế thay nhiệt độ dự báo, lễ âm lịch hardcode 1 năm |
| 14 | Baseline & chỉ số | `BASELINE-CHI-SO-buoi-14.pdf` | Báo cáo MAPE cho chuỗi có số 0 (âm thầm bỏ giá trị vô hạn); không có seasonal naive; mẫu số MASE/RMSSE lấy trên đoạn đang chấm |
| 15 | Backtesting | `BACKTEST-buoi-15.pdf` | `train_test_split(shuffle=True)`, tune và báo cáo trên cùng cửa sổ; Diebold–Mariano bỏ tự tương quan khi h > 1 |
| 16 | ETS & Theta | `ETS-THETA-buoi-16.pdf` | Holt-Winters cộng cho chuỗi có biên độ mùa vụ tăng theo mức; SES khớp bằng mức đã cập nhật (α → 1, SSE = 0) |
| 17 | ARIMA | `ARIMA-buoi-17.pdf` | auto-ARIMA tắt mùa vụ trên dữ liệu tháng (`season_length=1`); không kiểm phần dư, nên mô hình tự chọn quên phần mùa vụ vẫn "ổn" |
| 18 | Hồi quy động | `HOI-QUY-DONG-buoi-18.pdf` | Hồi quy thường có phần dư tự tương quan, p-value "đẹp" (hành khách EU ~ sản lượng Mỹ, p = 3·10⁻¹⁶); Prophet mặc định không khai Tết |
| 19 | Nhu cầu gián đoạn | `NHU-CAU-GIAN-DOAN-buoi-19.pdf` | Chuỗi 76% số 0 chấm bằng MAE và MAPE bỏ tháng 0, chọn theo MAE → "không nhập hàng"; TSB tự viết chỉ cập nhật xác suất ở tháng có bán (không giảm khi mặt hàng ngừng bán) |
| 20 | Đa biến & nowcasting | `DA-BIEN-STATE-SPACE-buoi-20.pdf` | Không kiểm cointegration (hạng luôn 0) → VAR trên sai phân cho dầu–xăng; nowcast đọc vintage mới nhất (số đã sửa, đủ 3 tháng ngay từ tháng đầu) |
| 21 | Tài chính & biến động | `TAI-CHINH-GARCH-buoi-21.pdf` | Demo mạng nơ-ron "đoán giá chính xác 99%" (chuẩn hoá cả chuỗi, chia ngẫu nhiên, chỉ báo R², không có naive — thực chất thua naive); VaR 99% chuẩn với độ lệch chuẩn cố định (Kupiec bác) |
| 22 | Dự báo thành hồi quy | `ML-HOI-QUY-buoi-22.pdf` | Chiến lược direct dùng lag 1 cho h = 7; cây quyết định trên chuỗi có xu hướng không sai phân |
| 23 | Gradient boosting | `GRADIENT-BOOSTING-buoi-23.pdf` | LightGBM L2 cho dữ liệu đếm thưa; Optuna tune bằng KFold ngẫu nhiên |
| 24 | Ensemble & AutoML | `ENSEMBLE-AUTOML-buoi-24.pdf` | Chọn "mô hình tốt nhất" trong 30 mô hình trên chính tập báo cáo |
| 25 | Dự báo xác suất | `DU-BAO-XAC-SUAT-buoi-25.pdf` | Khoảng từ phần dư trong mẫu giả định chuẩn (coverage thật ~60%); quantile crossing |
| 26 | Conformal | `CONFORMAL-buoi-26.pdf` | Split conformal cố định trên chuỗi có drift → coverage trượt dần |
| 27 | Bayes & GP | `BAYES-GP-buoi-27.pdf` | Prior mặc định quá rộng, không prior predictive check; dùng posterior có divergence |
| 28 | Dự báo phân cấp | `PHAN-CAP-buoi-28.pdf` | Dự báo độc lập từng cấp — tổng cửa hàng ≠ dự báo toàn công ty |
| 29 | Nền DL | `DEEP-LEARNING-NEN-buoi-29.pdf` | Cắt cửa sổ trước khi chia tập (chồng lấn train/val); scaler fit toàn bộ |
| 30 | N-BEATS … TiDE | `NBEATS-TFT-buoi-30.pdf` | Nhiệt độ thực tế khai là `futr_exog` |
| 31 | Transformer | `TRANSFORMER-buoi-31.pdf` | Bảng benchmark `drop_last=True`, không có seasonal naive/DLinear |
| 32 | Mô hình sinh | `MO-HINH-SINH-buoi-32.pdf` | Mô hình sinh chép nguyên chuỗi train; chỉ chấm fidelity |
| 33 | Không gian–thời gian & thời tiết AI | `KHONG-GIAN-THOI-TIET-buoi-33.pdf` | Kiểm chứng AIFS bằng điểm lưới gần nhất, không hiệu chỉnh; đánh giá trên năm có trong tập huấn luyện |
| 34 | Foundation model | `FOUNDATION-MODEL-buoi-34.pdf` | So zero-shot trên dataset nằm trong tập huấn luyện trước; context 64 điểm cho dữ liệu giờ |
| 35 | Fine-tune & benchmark | `FINE-TUNE-BENCHMARK-buoi-35.pdf` | Fine-tune toàn bộ trên 200 điểm; covariate lệch 1 bước thời gian |
| 36 | LLM & agent | `LLM-AGENT-buoi-36.pdf` | Agent tự chọn tập test; báo cáo LLM có con số không có trong kết quả công cụ |
| 37 | Dự báo sự kiện bằng LLM | `DU-BAO-SU-KIEN-buoi-37.pdf` | Backtest bot trên câu hỏi resolve trước mốc cắt kiến thức; search không lọc ngày |
| 38 | Tác động can thiệp | `TAC-DONG-CAN-THIEP-buoi-38.pdf` | So trước/sau đơn giản, bỏ qua mùa vụ và xu hướng |
| 39 | Kịch bản & what-if | `KICH-BAN-WHAT-IF-buoi-39.pdf` | Partial dependence của mô hình dự báo dùng làm độ co giãn giá (sai dấu) |
| 40 | Dự báo → quyết định | `DU-BAO-QUYET-DINH-buoi-40.pdf` | Đặt hàng = dự báo trung bình; chọn mô hình theo MASE |
| 41 | Pipeline tái lập | `PIPELINE-TAI-LAP-buoi-41.pdf` | Notebook chạy tay, join không point-in-time, không kiểm schema, mỗi lần chạy một kết quả |
| 42 | Phục vụ quy mô lớn | `PHUC-VU-QUY-MO-buoi-42.pdf` | Vòng for tuần tự 145.000 chuỗi; API load mô hình mỗi request |
| 43 | Giám sát & drift | `GIAM-SAT-DRIFT-buoi-43.pdf` | Không giám sát đầu vào; cảnh báo dựa trên MAPE ngày (ồn); retrain cố định |
| 44 | Dự án cuối | `DU-AN-CUOI-buoi-44.pdf` | — |
