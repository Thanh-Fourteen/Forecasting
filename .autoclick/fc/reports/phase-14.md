# phase 14

_2026-09-19 04:01:18_

Written for: you, as the person running the course build.

Phase 14 is done and ticked ✅ in `todos.md`, `todos/phase-14.md` and `todos/tong-quan.md`. Nothing is committed.

| | Before | After |
|---|---|---|
| **Buổi 13** `tai-lieu.md` | 2,392 words, 44 checker flags, 8 blockers, 9 theory sections | 4,042 words, **0 flags**, 0 blockers, 6 sections, PDF 14 pages |
| Leak tables | no hand-worked example | each leak type has a 6-row table with the peeking cells in bold: centered rolling, rolling without shift, lag < h, whole-series z-score, target encoding, two-sided interpolation |
| Notebook / quiz | no notebook; the old quiz contradicted itself (question 2) and had a wrong number (1.33 instead of 1.32) | new `code/lab.ipynb`, run on `code/`; the quiz has 10 questions with every answer re-computed in Python |
| Lab | — | `kiem_tra_lab.py 13` passes: `code/` fails 4/13 tests as intended, the answer key passes 13/13; the independence check, ruff and zip listing are clean |
| **Project 1 brief** | 1,130 words; the example JSON was exactly error L1 (5 points given away); said "24 hours ahead" while the code uses 24 steps of 30 minutes | 1,067 words; neutral example (checked that it is not a real error); "12 giờ tới (24 bước 30 phút)"; points to the rubric instead of repeating it; hints are generic |
| **Phụ lục D** | 1,716 words; examples for only a few metrics; many English quotes | 2,596 words; every metric has a 5-number hand example plus "dùng khi / bẫy"; English quotes removed; PDF 7 pages |

Three things I did beyond "chỉ viết lại đề + rubric". Please check them:

1. **I changed the error-detection grader** (`giam-khao/cham_phat_hien.py`). The old version gave 3 points for the error type alone. Since the brief names all six types, listing the six types with made-up locations scored 18/30. Now an entry only counts if the type and the file are right and its time range overlaps the real error, allowing ±3 days. Anything else is a false report (−2). I tested it: the made-up list now scores 0 and the correct answers score 30. `RUBRIC.md` describes the new rule.
2. **Diffing against the original data finds all six errors.** `python lab.py up` downloads the clean source data, so a learner could compare it with the dirty files. The brief now forbids this and says errors found that way score nothing. Graders can't enforce that. The real fix is to remove the original datasets from the project's `lab/nen.toml` if `lab.py check` doesn't need them, but I didn't change the lab setup without asking you.
3. **Small comment fixes in the project skeleton:** `code/feature.py` now states the horizon as 12 hours, and `code/lam_sach.py` no longer points to a section of buổi 10 that doesn't exist. Also rewrote `code/README.md`.

The error answers and the model solution stay in `giam-khao/`, which the zip leaves out. The zip does include the dirty data in `phat/du-lieu/`.

Next is Phase 15: an independent read-through of buổi 9–13, the project brief and Phụ lục D, in a new session.
