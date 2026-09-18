# Phase 15 — Buổi 34–37 · Foundation model và LLM 🔲

Quy ước + chuẩn dễ hiểu: `todos/quy-uoc.md`. Tiêu đề + **prompt copy-paste** của phase này: `todos.md` ở gốc repo (mục "Phase 15"). Trạng thái ✅/🔲 ở tiêu đề phải khớp với tiêu đề trong `todos.md`.

Hệ sinh thái đổi nhanh nhất khoá — **research của phase này quan trọng nhất**.

| Buổi | Research | Tài liệu | Code | Lab | Quiz | Đọc thử | PDF |
|---|---|---|---|---|---|---|---|
| 34 Foundation model | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 35 Fine-tune & benchmark | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 36 LLM & agent | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| 37 Dự báo sự kiện bằng LLM | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

Bắt buộc:
- Buổi 34: so zero-shot **chỉ trên dữ liệu sau ngày phát hành model**; đo thời gian + RAM trên CPU; context length
- Buổi 35: ít nhất một ca foundation model **thua** LightGBM, giải thích; tính lại xếp hạng benchmark chỉ trên task sạch rò rỉ; conformal hoá quantile
- Buổi 36: test tự động "không bịa số" (mọi con số trong báo cáo LLM có trong output công cụ); agent không được tự chọn tập test;
  **bản ghi phản hồi LLM** để chấm không cần API key; nhánh model mở chạy local
- Buổi 37: Brier score **chỉ trên câu hỏi resolve sau mốc cắt kiến thức**, đo "khoảng rò rỉ"; học viên tự dự báo
  và chấm calibration của chính mình; so với baseline thị trường. **Cột mốc M6**
