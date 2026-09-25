# phase 27

_2026-09-25 09:19:27_

Phase 27 is done: sessions 25–28 all pass the independent read-through, and it's ticked ✅ in `todos.md`, [phase-27.md](todos/phase-27.md) and `tong-quan.md`. One required item is still waiting: grading the real mid-course project 2 submission can't run until 2026-10-09 (today is 25/9), so I moved it to Phase 32.

I read each session fresh, with only `tai-lieu.md` and the quiz with answers removed. I recalculated every number and quiz answer in Python or by hand. Then I fixed the problems by rewriting sentences, not adding paragraphs.

| Session | Blind quiz | Blocking / hard / minor before → after | Words | PDF |
|---|---|---|---|---|
| 25 | 10/10 | 0 / 3 / 3 → 0 / 0 / 0 | 4.337 → 4.375 | 14 tr |
| 26 | 10/10 | 0 / 1 / 4 → 0 / 0 / 1 | 3.649 → 3.661 | 12 tr |
| 27 | 10/10 | 0 / 2 / 4 → 0 / 0 / 0 | 4.146 → 4.212 | 13 tr |
| 28 | 10/10 | 0 / 3 / 4 → 0 / 0 / 2 | 3.544 → 3.620 | 11 tr |

The answer keys had no wrong answers. The main fixes:
- **Session 25:** Lab step 2 made 1.866 hours and 21,9% look like two separate results, but they are the same count. "ngày thường nóng" now says Monday–Friday, which matches the code. I added the missing link between "proper" and "a calibrated model doesn't always win". The median in WIS is now $q_{0,5}$ so it no longer clashes with $m$ in CRPS.
- **Session 26:** the glossary said "sai số lớn thứ 9", which contradicted the body (the 9th error in ascending order). I also explained why the MAPIE snippet uses 168-hour blocks while section 4.4 says 24.
- **Session 27:** `Normal(0, 10)`, "~" and "Gauss" were used without ever being defined. I added two lines to the recap section. The "8 trường" example is now explained in one sentence before it is used.
- **Session 28:**
  - The MinT "hand calculation" only gave the result. It is now a real hand calculation: split the discrepancy in the ratio 4 : 1 : 1, checked against NumPy.
  - "Chệch" (bias) is now defined.
  - The text said MinT "shrink" pulls the covariance matrix toward its diagonal; I reworded that in plain terms. The library estimates how much to shrink, so it isn't the fixed one half our own `G_mint` uses.

**One issue is still open in session 28.** In the coverage table, the in-sample rows are scored on 3 cutoffs × 8 quarters, but the out-of-sample rows on 17 cutoffs × 4 quarters. The text compared them as if they were the same test. I now state this in the text and say the comparison is only approximate. Scoring both on the same 17 cutoffs would need changes to `dap-an/` and `cham/`, so I haven't done it. Tell me if you want it.

All four labs pass `kiem_tra_lab.py`: answers green, `code/` red in the intended places, notebooks run to the end. `kiem_tra_doc_lap.sh` passes, `ruff` is clean and `kiem_de_hieu.py` finds 0 issues. Each session's `NGHIEN-CUU.md` now has an "Đọc thử độc lập" section with the full findings. Nothing is committed.
