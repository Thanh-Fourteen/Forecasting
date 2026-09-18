# Nghiên cứu sư phạm — viết tài liệu kỹ thuật cho người tự học

**Ngày research:** 2026-09-18 · **Người đọc mục tiêu:** biết Python cơ bản + toán phổ thông, chưa học thống kê
đại học, tự học một mình. **Mục đích:** làm căn cứ cho quy tắc D1–D12 (`todos/quy-uoc.md`, mục "Chuẩn dễ hiểu") và
`tools/CHUAN-DE-HIEU.md`.

Quy ước: chỉ ghi điều đã đọc được trong nguồn. "Đọc toàn văn" = đã tải và đọc văn bản gốc; "đọc tóm tắt" = chỉ
đọc abstract/trang giới thiệu. Nguồn không truy cập được ghi rõ ở cuối mỗi mục.

---

## 1. Worked example effect và expertise reversal

**Phát hiện chính**
- Worked example = lời giải đầy đủ của một bài để người học nghiên cứu. Hiệu ứng được báo cáo đầu tiên ở đại số
  (Sweller & Cooper 1985). Học từ ví dụ giải sẵn giúp dựng kiến thức và chuyển giao tốt hơn tự giải bài tương
  đương — với người mới (Sweller et al. 2019, đọc toàn văn).
- Ví dụ tốt có các phần **gắn liền nhau** (chữ đặt trong/cạnh hình), **đánh dấu mục tiêu con** (subgoal) bằng nhãn
  hoặc tách mỗi nhóm bước ra một dòng; mỗi loại bài nên có **nhiều ví dụ**, đổi hình thức (Atkinson et al. 2000,
  đọc toàn văn). Catrambone: chỉ cần tách nhóm bước thành dòng riêng đã hiệu quả gần bằng dán nhãn.
- Người học hay chỉ lướt ví dụ. **Câu nhắc tự giải thích** (self-explanation prompt: "vì sao bước này đúng?")
  làm ví dụ hiệu quả hơn, nếu tổng tải không quá sức (Sweller et al. 2019).
- **Fading**: bài 1 giải đủ → bài 2 bỏ bước cuối → bài 3 bỏ hai bước cuối → bài 4 tự giải (backward fading).
  Cách này tốt hơn cặp ví dụ–bài tập (Renkl & Atkinson 2003, đọc toàn văn; Renkl et al. 2002, đọc tóm tắt).
- **Expertise reversal**: hỗ trợ cần cho người mới có thể thành thừa, thậm chí có hại, với người đã giỏi
  (Kalyuga et al. 2003, đọc toàn văn). Với tài liệu ít tương tác phần tử (học định nghĩa), tự tạo câu trả lời lại
  tốt hơn xem đáp án (Chen et al., dẫn trong Sweller et al. 2019).

**Hệ quả cho tài liệu khoá này**
- Mỗi khái niệm có **một ví dụ số nhỏ giải từng bước** trước khi đưa công thức tổng quát (D2).
- Bước tính tách dòng, mỗi dòng một mục tiêu con có nhãn ngắn ("Bước 1 — tính sai số").
- Sau ví dụ giải đủ: một bài "điền bước cuối" rồi một bài tự làm ("Tự kiểm tra", D10).
- Thêm câu hỏi "vì sao?" ngay trong ví dụ, không chỉ ở cuối.
- Buổi càng về sau (≥ buổi 20) càng bớt giải chi tiết những thứ đã thành thạo — tránh expertise reversal.

**Nguồn**
- Sweller, van Merriënboer & Paas (2019). *Cognitive Architecture and Instructional Design: 20 Years Later*.
  Educ. Psychol. Rev. 31, 261–292. https://leadinglearner.me/wp-content/uploads/2019/02/sweller2019_article_cognitivearchitectureandinstru.pdf (truy cập 2026-09-18)
- Atkinson, Derry, Renkl & Wortham (2000). *Learning from Examples: Instructional Principles from the Worked
  Examples Research*. Rev. Educ. Res. 70(2), 181–214. https://assess.ucr.edu/sites/default/files/2019-02/atkinsonderryrenklwortham_2000.pdf (2026-09-18)
- Renkl & Atkinson (2003). *Structuring the Transition From Example Study to Problem Solving…*. Educ. Psychol.
  38(1), 15–22. https://mrbartonmaths.com/resourcesnew/8.%20Research/Explicit%20Instruction/Structuring%20the%20Transition%20From%20Example%20Study%20to%20Problem%20Solving.pdf (2026-09-18)
- Renkl, Atkinson, Maier & Staley (2002). *From example study to problem solving: Smooth transitions help
  learning*. J. Exp. Educ. 70, 293–315 — chỉ đọc tóm tắt qua kết quả tìm kiếm.
- Kalyuga, Ayres, Chandler & Sweller (2003). *The Expertise Reversal Effect*. Educ. Psychol. 38(1), 23–31.
  https://mrbartonmaths.com/resourcesnew/8.%20Research/Explicit%20Instruction/The%20Expertise%20Reversal%20Effect.pdf (2026-09-18)
- Sweller & Cooper (1985) — không đọc bản gốc; thông tin lấy từ Sweller et al. 2019.

## 2. Cognitive load theory (CLT)

**Phát hiện chính**
- Bộ nhớ làm việc hẹp; kiến thức đã có trong bộ nhớ dài hạn gom nhiều phần tử thành một khối. Vì vậy **mức tương
  tác phần tử** (element interactivity — số thứ phải giữ cùng lúc trong đầu) phụ thuộc cả tài liệu lẫn người học
  (Sweller et al. 2019).
- **Split-attention**: hai nguồn thông tin không tự đứng được (hình + câu giải thích) mà để xa nhau → người học phải
  tự ghép trong đầu → tải cao, học kém. Sửa: đặt câu giải thích ngay trong/cạnh hình (Tarmizi & Sweller 1988, dẫn
  trong Sweller et al. 2019).
- **Redundancy**: hai nguồn cùng nội dung, mỗi nguồn tự hiểu được (hình tuần hoàn máu + đoạn văn nói y hệt) → chỉ
  một nguồn học tốt hơn cả hai. Nhắc lại nguyên văn không vô hại.
- **Isolated elements**: thông tin quá phức tạp → dạy từng phần tử riêng trước, rồi mới dạy cách chúng ghép vào nhau;
  tương tự sắp xếp đơn giản → phức tạp.
- **Guidance fading**: hướng dẫn nhiều ở đầu khoá, giảm dần khi người học tiến bộ.

**Hệ quả cho tài liệu khoá này**
- Ký hiệu công thức giải thích **ngay dưới công thức**, không đẩy sang Phụ lục (chống split-attention; D3).
- "Cách đọc hình" đặt **sát dưới hình**, trỏ vào chi tiết cụ thể trên hình (D8). Chú thích màu viết trên hình.
- Không nói một ý hai lần bằng hai dạng tương đương (bảng + đoạn văn đọc lại từng ô). "Đọc bảng" chỉ nói so sánh và
  kết luận, không đọc lại số (D8).
- Một đoạn không dồn nhiều số và nhiều từ mới cùng lúc: mỗi số, mỗi từ mới là một phần tử phải giữ (D7).
  *Con số "≤ 3 số/đoạn" là quy ước của khoá, không có nguồn nào cho đúng số 3.*
- Khái niệm khó (quantile, ACF) dạy các mảnh riêng trước (sắp xếp, vị trí, tỉ lệ) rồi mới ghép (isolated elements; D2).

**Nguồn** — Sweller et al. (2019), như mục 1. Bản gốc Tarmizi & Sweller (1988), Chandler & Sweller (1991) không đọc.

## 3. Concreteness fading

**Phát hiện chính**
- Bắt đầu bằng vật cụ thể, rồi **có chủ ý và dần dần** chuyển sang ký hiệu trừu tượng — kết hợp ưu điểm của cả hai
  thay vì chọn một (Fyfe et al. 2014, đọc tóm tắt).
- Ba bậc theo Bruner: enactive (vật thật/thao tác) → iconic (hình vẽ) → symbolic (ký hiệu). Ví dụ: quả táo thật →
  hình quả táo → chữ số (Kokkonen & Schalk 2021, đọc toàn văn).
- Lợi ích nêu trong tổng quan: ký hiệu được hiểu qua vật cụ thể; có hình ảnh nhớ được khi ký hiệu mất nghĩa; giúp
  nhận ra tính chất chung, tổng quát hoá được (Fyfe et al. 2014, tóm tắt).
- Cảnh báo: trình tự này có thể không tổng quát như người ta nghĩ; loại biểu diễn và mục tiêu khác nhau theo môn.
  Điểm then chốt là **nối rõ** giữa các biểu diễn, không chỉ xếp chúng nối tiếp (Kokkonen & Schalk 2021).

**Hệ quả**
- Khuôn D2: *ví dụ số nhỏ tính tay → hình → công thức* là đúng bậc enactive → iconic → symbolic.
- Mỗi lần chuyển bậc có **câu nối**: "trên hình, điểm đỏ chính là số 4 ta vừa tính"; "trong công thức, $q$ là
  điểm đỏ đó".
- Dùng cùng một bộ số nhỏ xuyên suốt ba bậc, không đổi ví dụ giữa chừng.

**Nguồn**
- Fyfe, McNeil, Son & Goldstone (2014). *Concreteness Fading in Mathematics and Science Instruction: a Systematic
  Review*. Educ. Psychol. Rev. 26(1), 9–25. https://link.springer.com/article/10.1007/s10648-014-9249-3 —
  **toàn văn không truy cập được** (Springer chặn, ResearchGate 403); chỉ đọc tóm tắt qua ERIC/kết quả tìm kiếm.
- Kokkonen & Schalk (2021). *One Instructional Sequence Fits all? A Conceptual Analysis of the Applicability of
  Concreteness Fading…*. Educ. Psychol. Rev. https://d-nb.info/1223824624/34 (2026-09-18)

## 4. Signaling và các nguyên tắc đa phương tiện (Mayer)

**Phát hiện chính**
- Signaling: học tốt hơn khi có **dấu hiệu làm nổi phần chính và cấu trúc** của nội dung. Meta-analysis 103 nghiên
  cứu, 12.201 người: signaling có lợi cho ghi nhớ và chuyển giao, giảm tải nhận thức; kiến thức nền không phải yếu
  tố điều tiết quan trọng (Schneider et al. 2018, đọc tóm tắt).
- Spatial contiguity: chữ và hình tương ứng đặt **gần nhau** thì học tốt hơn.
- Coherence: bỏ chi tiết thừa, gây xao nhãng. Pre-training: làm quen **khái niệm và từ khoá chính trước** khi vào bài.
  Segmenting: chia bài thành đoạn ngắn, người học tự bước tiếp. Personalization: giọng văn trò chuyện thân mật.

**Hệ quả**
- "Cách đọc hình" chính là signaling bằng lời: chỉ mắt nhìn vào đâu, theo thứ tự trục → màu → điểm chính → kết luận (D8).
- Tiêu đề hình nói kết luận (đã có ở quy tắc 12) — là một dạng signaling.
- Bảng "Từ mới trong buổi" đầu Lý thuyết = pre-training (D1).
- Mục chi tiết học thuật đưa vào hộp "Nâng cao"/"Đọc thêm" = coherence (D9).
- Mỗi mục ngắn, có "Tóm lại" + "Tự kiểm tra" = segmenting (D2, D10).

**Nguồn**
- Schneider, Beege, Nebel & Rey (2018). *A meta-analysis of how signaling affects learning with media*. Educ. Res.
  Rev. 23, 1–24. https://www.sciencedirect.com/science/article/abs/pii/S1747938X17300581 — chỉ đọc tóm tắt.
- Mayer (2024). *The Past, Present, and Future of the Cognitive Theory of Multimedia Learning*. Educ. Psychol. Rev.
  36, 8. https://link.springer.com/article/10.1007/s10648-023-09842-1 — **toàn văn không tải được**; định nghĩa
  các nguyên tắc lấy từ bảng kiểm của University of Pittsburgh:
  https://teaching.pitt.edu/wp-content/uploads/2023/03/multimedia-principles-checklist.pdf (nguồn thứ cấp, 2026-09-18).

## 5. Cách các nguồn dạy giỏi giải thích

**FPP3 (Hyndman & Athanasopoulos)**
- *Forecast distribution* (§5.5): bắt đầu từ ý "bất định được biểu diễn bằng một phân phối xác suất", rồi mới
  khoảng dự báo = dự báo điểm ± $c$ × độ lệch chuẩn, kèm bảng hệ số $c$. Ví dụ xuyên suốt: giá đóng cửa Google,
  đi từ dự báo 1 bước → nhiều bước → bootstrap (mô phỏng 5 đường tương lai, lấy percentile).
  **§5.5 không định nghĩa quantile.**
- *Quantile* (§5.9) được định nghĩa **qua một hình đã quen**: cận dưới khoảng 80% là percentile 10 (quantile 0,1),
  "nên ta kỳ vọng giá trị thật nằm dưới cận này khoảng 10% số lần". Sau đó mới đến pinball loss; với $p=0{,}5$ nó
  bằng sai số tuyệt đối. Ý hay để mượn: **định nghĩa quantile bằng tần suất "nằm dưới"**, gắn vào hình khoảng.
- *ACF* (§2.8): định nghĩa bằng lời (tương quan giữa chuỗi và chính nó lùi $k$ bước) → công thức $r_k$ → tính trên
  dữ liệu bia quý → vẽ correlogram → quy tắc đọc: xu hướng = ACF lớn ở độ trễ nhỏ rồi giảm chậm; mùa vụ = đỉnh ở bội
  số chu kỳ; cả hai = hình "vỏ sò". §2.9: với nhiễu trắng, **95% cột nằm trong** $\pm 1{,}96/\sqrt{T}$.
- *Tính dừng* (§9.1): cho 9 hình, hỏi "chuỗi nào dừng?", rồi loại trừ từng lý do (mùa vụ, xu hướng, phương sai tăng).
  Nói rõ chỗ dễ nhầm: chuỗi có chu kỳ không cố định vẫn dừng.
- *Rò rỉ*: FPP nhấn "đánh giá bằng dự báo thật" (§5.8): residual trên tập huấn luyện không cho biết sai số tương lai;
  "error" không có nghĩa là lỗi, mà là phần không dự báo được.

**Seeing Theory (Brown University)** — tương tác trực quan (D3.js), đi theo: biến ngẫu nhiên (định nghĩa hình thức)
→ phân phối rời rạc/liên tục (thanh trượt, xu/xúc xắc, CDF tô màu cam) → định lý giới hạn trung tâm (mô phỏng).
**Không có mục riêng cho quantile.** Bài học mượn: cho người học *lấy mẫu và thấy* phân phối hiện ra trước khi đọc
công thức.

**3Blue1Brown** — video CLT mở bằng bảng Galton đơn giản → xúc xắc → phân phối của tổng → mới đến công thức Gauss
(theo trang tóm tắt; **không xem được video**). Bài binomial "Probabilities of probabilities" (2020): trang chỉ có
siêu dữ liệu, **không đọc được nội dung**.

**StatQuest** — video *Quantiles and Percentiles, Clearly Explained!!!* (2017-11-06). **Không truy cập được nội
dung** (trang statquest.org 404, YouTube không trả transcript). Không ghi gì về trình tự của video này.

**Hệ quả**
- Quantile dạy theo FPP §5.9: sắp dãy số nhỏ → "bao nhiêu phần nằm dưới" → nối sang cận dưới/cận trên của khoảng
  → rồi mới đến pinball loss.
- ACF dạy theo FPP: lời → ví dụ số nhỏ độ trễ 1 → correlogram → quy tắc đọc hình; nói trước "5% cột vượt dải là
  bình thường với nhiễu trắng".
- Tính dừng dạy bằng bài "chọn hình" + loại trừ lý do, trước khi nói ADF/KPSS.

**Nguồn** (truy cập 2026-09-18): https://otexts.com/fpp3/prediction-intervals.html · /distaccuracy.html · /acf.html ·
/wn.html · /stationarity.html · /accuracy.html · https://seeing-theory.brown.edu/probability-distributions/index.html ·
https://www.3blue1brown.com/lessons/binomial-distributions/ · https://statquest.org/statquest-quantiles-and-percentiles-clearly-explained/ (404).

## 6. Hiểu lầm phổ biến — nguồn tổng quát

- P-value **không** là xác suất giả thuyết đúng; "không có ý nghĩa thống kê" **không** có nghĩa là hiệu ứng nhỏ;
  một khoảng tin cậy 95% cụ thể **không** có "95% khả năng chứa giá trị thật" (Greenland et al. 2016, đọc toàn văn).
- "Luật số nhỏ": tin mẫu nhỏ giống tổng thể; lẫn phân phối mẫu với phân phối tổng thể (Castro Sotos et al. 2007).
- Tương quan ≠ nhân quả; biến gây nhiễu (kem–đuối nước, cùng do nhiệt độ). Nhưng biến không gây ra $y$ **vẫn có thể
  giúp dự báo** $y$ (FPP §7.8).
- Hai chuỗi cùng có xu hướng trông như liên quan (hồi quy giả: hành khách Úc ~ lúa Guinea) (FPP §7.3).
- Granger causality chỉ là "đi trước + giúp dự báo", không phải nhân quả; bỏ sót biến chung → dương tính giả
  (Wikipedia, Granger causality).
- Rò rỉ = thông tin về mục tiêu mà lúc dự báo **chưa được phép có**. Dấu hiệu kinh điển: kết quả "tốt quá mức tin".
  Thi INFORMS 2010: ~30 đội AUC > 0,9 nhờ dữ liệu tương lai. Cách tránh: gắn thời điểm cho mọi quan sát, cắt học/đoán
  theo thời gian — "no-time-machine" (Kaufman et al. 2012, đọc toàn văn).
- Rò rỉ trong chuỗi thời gian còn đến từ làm trơn, phân rã, chuẩn hoá, tính đặc trưng **trên cả chuỗi** trước khi
  cắt; và từ chọn sai tầm dự báo (dùng thống kê cả ngày cho mô hình "ngày mai") (Hewamalage et al. 2023).
- Phân loại 8 kiểu rò rỉ; 294 bài báo ở 17 lĩnh vực bị ảnh hưởng; có mục riêng "temporal leakage" và "tiền xử lý
  trên cả train lẫn test" (Kapoor & Narayanan 2023, đọc toàn văn).

**Nguồn** (truy cập 2026-09-18)
- Greenland et al. (2016). *Statistical tests, P values, confidence intervals, and power: a guide to
  misinterpretations*. Eur. J. Epidemiol. 31, 337–350. https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/
- Castro Sotos et al. (2007). *Students' misconceptions of statistical inference*. Educ. Res. Rev. 2(2), 98–113.
  http://mintlinz.pbworks.com/w/file/fetch/96929061/Sotos-2007-Misconceptions.pdf
- Kaufman, Rosset, Perlich & Stitelman (2012). *Leakage in Data Mining: Formulation, Detection, and Avoidance*.
  ACM TKDD 6(4). https://www.cs.umb.edu/~ding/history/470_670_fall_2011/papers/cs670_Tran_PreferredPaper_LeakingInDataMining.pdf
- Hewamalage, Ackermann & Bergmeir (2023). *Forecast evaluation for data scientists: common pitfalls and best
  practices*. DMKD. https://arxiv.org/abs/2203.10716
- Kapoor & Narayanan (2023). *Leakage and the reproducibility crisis in machine-learning-based science*. Patterns
  4, 100804. https://hbiostat.org/papers/kap23lea.pdf
- FPP3 §7.3 https://otexts.com/fpp3/regression-evaluation.html, §7.8 https://otexts.com/fpp3/causality.html
- https://en.wikipedia.org/wiki/Granger_causality

## 7. Newsvendor critical fractile

**Phát hiện chính**
- Bán hàng dễ hỏng, đặt một lần. Cuối kỳ hoặc **thừa** (hàng không bán được) hoặc **thiếu** (khách muốn mua mà hết).
  Chi phí thiếu mỗi đơn vị $C_u$ = lãi bị mất; chi phí thừa $C_o$ = giá mua − giá thanh lý.
- Lượng đặt tối ưu là **quantile của nhu cầu** tại mức $C_u/(C_u+C_o)$. Ví dụ MetricGate: $C_u=10$, $C_o=3$ →
  $10/13 \approx 0{,}769$. Ví dụ Wikipedia: giá bán 7, giá mua 5, không thanh lý → $2/7 \approx 0{,}285$.
- Lập luận "thêm một đơn vị" (Wikipedia): đặt thêm cho tới khi xác suất đáp ứng đủ nhu cầu đạt tỉ lệ này; quá điểm
  đó, chi phí hàng thêm vượt lợi nhuận kỳ vọng thêm.
- Lưu ý: trang MetricGate viết khi thừa đắt thì tỉ lệ "giảm về 0,5" — **sai**; theo chính công thức, tỉ lệ giảm về 0.

**Hệ quả (mẫu cho buổi 1 mục 4.8)**
- Nói rõ đơn vị: "thiếu" = lượng mua < nhu cầu thực (kWh); "thừa" = lượng mua > nhu cầu thực.
- Tính từng bước với số của khoá: thiếu 1 kWh mất 4, thừa 1 kWh mất 1 → $4/(4+1)=0{,}8$.
- Lập luận bằng lời có thay số: "mua thêm 1 kWh: nếu lẽ ra thiếu thì tránh được 4, nếu lẽ ra thừa thì mất 1. Đáng mua
  thêm chừng nào khả năng *còn thiếu* × 4 lớn hơn khả năng *đã thừa* × 1, tức tới khi 80% khả năng nhu cầu nằm dưới."
- Nối với quantile theo FPP §5.9: "quantile 0,8 = mức mà 80% số lần thực tế nằm dưới".

**Nguồn** (truy cập 2026-09-18): https://en.wikipedia.org/wiki/Newsvendor_model ·
https://metricgate.com/docs/newsvendor-critical-fractile/ (nguồn phổ thông, có lỗi nêu trên).

---

## Hiểu lầm phổ biến theo buổi 1–13

| Buổi · khái niệm | Hiểu lầm | Tài liệu nên phòng thế nào | Nguồn |
|---|---|---|---|
| 1 · baseline | Mô hình phức tạp mặc nhiên hơn phương pháp đơn giản | So mọi mô hình với naive/seasonal naive; nói "không hơn thì bỏ" | FPP §5.2; Hewamalage 2023 |
| 1 · dự báo điểm vs phân phối | Dự báo = một con số; residual nhỏ = dự báo tốt | Luôn kèm khoảng; phân biệt residual (train) với forecast error (test) | FPP §5.5, §5.8 |
| 1 · "error" | Error là "lỗi" của người làm | Định nghĩa: sai số = thực tế − dự báo, phần không đoán được | FPP §5.8 |
| 2 · quantile | Quantile 0,8 = "80% giá trị lớn nhất" hoặc = 80% của giá trị | Định nghĩa bằng "80% số lần nằm dưới", ví dụ dãy 1–5 | FPP §5.9 |
| 2 · khoảng | Khoảng 95% cụ thể có 95% khả năng chứa giá trị thật (khoảng tin cậy) | Tách khoảng dự báo (cho giá trị tương lai) khỏi khoảng tin cậy (cho tham số) | Greenland 2016 |
| 2 · mẫu nhỏ | Mẫu nhỏ phản ánh đúng tổng thể | Mô phỏng nhiều mẫu nhỏ, cho thấy dao động | Castro Sotos 2007 |
| 2 · bootstrap | Khoảng bootstrap luôn đúng | Nói giả định: residual không tương quan | FPP §5.5 |
| 3 · DST | Mỗi giờ địa phương xảy ra đúng một lần | Ví dụ giờ 01:00 lặp lại khi lùi giờ (`fold`); lưu UTC | Python docs `zoneinfo` |
| 4 · đọc biểu đồ | Hình dự báo đè lên thực tế là "bằng chứng" mô hình tốt | Luôn kèm benchmark + chỉ số; "Cách đọc hình" | Hewamalage 2023 |
| 5 · Box-Cox | Biến đổi ngược cho ra trung bình | Biến đổi ngược cho **trung vị**; cần hiệu chỉnh nếu muốn trung bình (trung vị không cộng được) | FPP §5.6 |
| 6 · phân rã | Thành phần mùa của phân rã cổ điển thay đổi theo năm | Nói rõ giả định mùa cố định; đường MA không có giá trị ở hai đầu | FPP §3.4 |
| 6/12 · MA trung tâm | Làm trơn là vô hại | MA trung tâm dùng giá trị **sau** thời điểm → rò rỉ nếu làm trước khi cắt | FPP §3.3; Hewamalage 2023 |
| 7 · ACF | Mọi cột vượt dải xanh đều có ý nghĩa | Nhiễu trắng vẫn có ~5% cột vượt | FPP §2.9 |
| 7 · tính dừng | Có chu kỳ thì không dừng | Chu kỳ không cố định độ dài vẫn dừng | FPP §9.1 |
| 7 · ADF/KPSS | Hai test cùng giả thuyết H0 | ADF: H0 có unit root; KPSS: H0 dừng; bảng 4 trường hợp | statsmodels; FPP §9.1 |
| 7 · p-value | p = xác suất H0 đúng; p > 0,05 = không có hiệu ứng | Hộp "Mượn trước" giải nghĩa p-value | Greenland 2016 |
| 8 · tương quan | Tương quan = nhân quả; không nhân quả thì vô dụng cho dự báo | Ví dụ kem–đuối nước; nói rõ vẫn dùng dự báo được | FPP §7.8 |
| 8 · tương quan chuỗi | Hai chuỗi có xu hướng tương quan cao là có liên hệ | Hồi quy giả; khử xu hướng/sai phân trước khi tính | FPP §7.3 |
| 8 · Granger | "Granger-cause" = gây ra | Gọi là "đi trước và giúp dự báo"; cảnh báo biến chung | Wikipedia Granger |
| 9 · đặc trưng chuỗi | Tính đặc trưng trên cả chuỗi là an toàn | Chỉ tính trên phần train / cửa sổ quá khứ | Hewamalage 2023 |
| 10 · dữ liệu thiếu | Thiếu là ngẫu nhiên, điền đại là được | Hỏi "vì sao thiếu" (ngày lễ đóng cửa → hôm sau tăng) | FPP §13.9 |
| 11 · ngoại lai | Ngoại lai = lỗi, xoá đi | Ngoại lai có thể là lỗi **hoặc** chỉ bất thường thật | FPP §13.9 |
| 12 · aliasing | Lấy mẫu thưa (bỏ bớt điểm) chỉ mất chi tiết | Tần số cao hơn Nyquist hiện thành dao động giả tần số thấp; lọc trước khi hạ tần | Wikipedia Aliasing |
| 13 · rò rỉ | Tách ngẫu nhiên train/test là đủ | Cắt theo thời gian; gắn mốc thời gian cho từng feature; kết quả quá đẹp → nghi rò rỉ | Kaufman 2012; Kapoor 2023 |
| 13 · tiền xử lý | Chuẩn hoá/điền thiếu trên cả bộ dữ liệu trước khi cắt là bình thường | Fit mọi bước tiền xử lý chỉ trên train | Kapoor 2023 [L1.2] |

Nguồn thêm: Python `zoneinfo` https://docs.python.org/3/library/zoneinfo.html · statsmodels ADF/KPSS
https://www.statsmodels.org/stable/examples/notebooks/generated/stationarity_detrending_adf_kpss.html ·
FPP §3.3–3.4, §5.6, §13.9 · https://en.wikipedia.org/wiki/Aliasing (truy cập 2026-09-18).

---

## Ánh xạ sang quy tắc D1–D12

| Quy tắc | Nguồn ủng hộ |
|---|---|
| D1 Từ mới + bảng | Pre-training principle (Mayer; bảng kiểm Pitt). Isolated elements: học phần tử trước khi học tương tác (Sweller 2019). |
| D2 Khuôn vấn đề → … → tóm lại | Concreteness fading: cụ thể → hình → ký hiệu, có câu nối (Fyfe 2014; Kokkonen & Schalk 2021). Worked example trước bài tập (Sweller 2019; Atkinson 2000). |
| D3 Ký hiệu + câu có thay số | Split-attention: giải thích đặt ngay cạnh thứ cần giải thích (Sweller 2019). Ví dụ có mục tiêu con rõ (Atkinson 2000). |
| D4 Không nói lửng | FPP §5.8 định nghĩa "error" và quy ước dấu ngay tại chỗ; Greenland 2016 cho thấy định nghĩa tắt gây hiểu sai tràn lan. |
| D5 Chưa dạy chưa dùng / "Mượn trước" | Element interactivity: phần tử chưa có trong bộ nhớ dài hạn làm tăng tải (Sweller 2019). Pre-training (Mayer). |
| D6 Không chen trích tiếng Anh | Redundancy + split-attention: hai ngôn ngữ cùng nội dung buộc người đọc tự đối chiếu (suy từ Sweller 2019; không có nghiên cứu trực tiếp về trích song ngữ). |
| D7 Câu ngắn, ≤ 3 số/đoạn | Giới hạn bộ nhớ làm việc, element interactivity (Sweller 2019). Ngưỡng "3" là quy ước của khoá, không có nguồn. |
| D8 "Cách đọc hình"/"Đọc bảng" | Signaling (Schneider 2018 meta-analysis; Mayer). Spatial contiguity: đặt ngay dưới hình. FPP §2.8 luôn có quy tắc đọc ACF. |
| D9 ≤ 6 khái niệm | Coherence principle (bỏ chi tiết thừa); element interactivity. Số 6 là quy ước của khoá. |
| D10 "Tự kiểm tra" | Practice testing là một trong hai kỹ thuật hiệu quả nhất (Dunlosky et al. 2013). Fading: bước cuối để người học tự làm (Renkl & Atkinson 2003). |
| D11 Lab nói trước/sau mỗi bước | Self-explanation prompts (Sweller 2019); signaling; segmenting (Mayer). |
| D12 Quiz giải thích vì sao | Feedback nên nói "cái gì, thế nào, vì sao" — elaborated feedback (Shute 2008). |

Nguồn thêm (truy cập 2026-09-18):
- Dunlosky, Rawson, Marsh, Nathan & Willingham (2013). *Improving Students' Learning With Effective Learning
  Techniques*. PSPI 14(1). Bản phổ thông American Educator: https://files.eric.ed.gov/fulltext/EJ1021069.pdf
- Shute (2008). *Focus on Formative Feedback*. Rev. Educ. Res. 78(1), 153–189.
  https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf

---

## Baseline "Đọc thử" (Phase 5, 2026-09-18)

Chạy BƯỚC CUỐI (prompt ở `tools/CHUAN-DE-HIEU.md` mục "Prompt đọc thử") trên **bản cũ** của buổi 1, 7, 12. Mỗi buổi
một subagent mới, chỉ mở `tai-lieu.md` + `kiem-tra.md` đã bỏ đáp án, không web. Quiz chấm theo đáp án trong
`kiem-tra.md`. Cột `kiem_de_hieu` là tổng vi phạm máy đếm được trên bản cũ.

| Buổi | Chặn | Khó | Nhỏ | Quiz | Khái niệm "KHÔNG GIẢI THÍCH ĐƯỢC" | `kiem_de_hieu` |
|---|---|---|---|---|---|---|
| 01 (bản cũ) | 9 | 21 | 30 | 10/10 | quantile & chi phí lệch (4.8) | 75 |
| 07 (bản cũ) | 12 | 30 | 18 | 10/10 * | nghiệm đơn vị; một phần Ljung-Box, PACF | 75 |
| 12 (bản cũ) | 11 | 36 | 13 | 10/10 | wavelet; đo trễ bằng tương quan | 66 |
| **01 mục 4.8 — mẫu chuẩn mới** | **0** | 7 → sửa hết | 6 | tự kiểm tra đúng | không có | 4.8 sạch trừ 2 cờ cấp buổi |

\* Đáp án câu 5 buổi 7 **sai**: ghi $\bar y = 6$, $r_1 = 0$; dãy 4, 6, 8, 6, 4, 6, 8, 6, 4 có tổng 52, trung bình
52/9 ≈ 5,78, $r_1 ≈ 0{,}020$, $r_2 ≈ −0{,}800$ (tính lại bằng Python 2026-09-18). Subagent tính đúng. Ghi vào
`phan-hoi-hoc-vien.md` cho Phase 7.

**Kiểm độ nhạy của prompt.** Subagent buổi 1 bắt đủ **4 chỗ người dùng đã phải hỏi ChatGPT** ở mục 4.8: "4 lần"
so với gì (#18), quantile không định nghĩa (#39), $F^{-1}$ và vì sao $C_u/(C_u+C_o)$ (#40), dấu và cách tính +0,455
(#42) — đều ở mức "chặn". Prompt đủ nhạy, không phải sửa.

**Bài học về tiêu chí đạt.**
1. **Quiz không phân biệt được**: cả ba bản cũ đều 10/10 dù 9–12 chỗ chặn. Subagent làm được quiz bằng cách
   khớp chữ trong tài liệu mà không hiểu. Quiz ≥ 9/10 chỉ là điều kiện cần. Tiêu chí chính phải là **0 chỗ chặn** và
   **mục B không có "KHÔNG GIẢI THÍCH ĐƯỢC"**.
2. Subagent đọc kỹ ghi rất nhiều mục "nhỏ" (tới 30). Đặt ngưỡng: **0 chặn, ≤ 5 khó** mỗi buổi; "nhỏ" sửa khi rẻ.
3. **Chỗ chặn lặp lại ở cả ba buổi = kiến thức thống kê nền dùng mà không định nghĩa**: phân phối, quantile,
   phương sai/độ lệch chuẩn, tương quan, kiểm định (H0, p-value, mức ý nghĩa), ký hiệu MAE/RMSE. Phase 6 phải dạy kỹ
   các khái niệm này ở buổi 2, và mọi buổi sau phải nhắc lại chúng (mục 2 hoặc hộp "Mượn trước").
4. Chỗ chặn thứ hai: **khái niệm trung tâm không có định nghĩa bằng lời** (nghiệm đơn vị ở buổi 7, wavelet và
   periodogram ở buổi 12), chỉ có tên + công thức + trích tiếng Anh.
5. Mẫu chuẩn 4.8 viết theo D2 đưa số chặn từ 5 (thuộc 4.8) về 0 ngay lượt đầu. Vòng hai còn bắt được **một câu
   sai số học của chính tác giả** ("8 trên 10 ngày" trong khi đúng là 9/10). Vậy đọc thử cũng là kiểm lỗi nội dung.

**Tóm tắt chỗ chặn bản cũ (để Phase 6–8 dùng lại, không phải đọc thử lại từ đầu):**
- **Buổi 1**: công thức MAE ở mục 2 không giải thích ký hiệu; "gốc dự báo $T$" và $\hat y_{T+h}$ ở 4.5 chưa định
  nghĩa, không có ví dụ giờ cụ thể; 4.8 (đã sửa); "MAE nhắm trung vị" ở mục 6 không giải thích; bài tập 3 đòi tính
  quantile mà tài liệu chưa dạy.
- **Buổi 7**: ACF định nghĩa bằng "tương quan" chưa học; AR(1), $\phi$ dùng trước định nghĩa; Ljung-Box dùng kiểm
  định, H0, p-value, $\chi^2$ chưa học; "nghiệm đơn vị" không định nghĩa; "low power", I(0)/I(1), "unit MA root" nằm
  trong trích tiếng Anh; sai phân $\Delta y_t$ không định nghĩa ở mục 2; ngưỡng sai phân thừa −0,5 hay −0,45 không
  thống nhất (mục 4.5 và mục 8).
- **Buổi 12**: MAE/RMSE không định nghĩa; MAD và $\sigma$ không giải thích; phương sai (định nghĩa phổ công suất),
  periodogram, lọc thông thấp, IIR/dải qua, nhiễu trắng, wavelet (thang, hệ số) không định nghĩa; đo trễ bằng tương
  quan; câu trích tiếng Anh của `filtfilt`, SavGol, Hamilton mang ý chính; "10 cấu hình" bộ lọc không liệt kê.
