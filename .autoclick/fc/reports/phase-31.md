# phase 31

_2026-09-28 15:02:17_

Phase 31 is done: buổi 9–13 each have a `tu-hoc.ipynb` notebook and concept figures. All five notebooks run with 0 errors. I checked every number against the document and looked at all 33 figures, both as images and in the PDFs. Nothing is committed yet.

| Buổi | Cells / concept boxes / figures | PDF pages | Readability check |
|---|---|---|---|
| 9 | 58 / 20 / 7 | 17 → 18 | 0 → 0 |
| 10 | 53 / 17 / 6 | 14 → 16 | 2 → 2 (same) |
| 11 | 57 / 19 / 6 | 13 → 15 | 1 → 1 (same) |
| 12 | 55 / 18 / 8 | 13 → 16 | 2 → 2 (same) |
| 13 | 58 / 13 / 6 | 14 → 16 | 2 → 2 (same) |

I wrote buổi 9 myself. Buổi 10–13 were drafted by four background agents, with notebook runs taken one at a time because the machine had only ~7 GB free. I then reviewed their figures and numbers myself. Every row is ticked in `todos/phase-31.md` and `todos.md`.

**Other changes:**
- **Document fixes:**
  - Buổi 9 said 18 features go into PCA, but the code uses 15, because one constant series makes three columns NaN. I corrected the text, the new-words table and `NGHIEN-CUU.md`.
  - Buổi 11 said "mười lăm tháng" (15 months); it is 16, and I fixed it.
- **Two bugs in `sinh.py`:**
  - It didn't re-export the PDF when only a figure image changed. It now does.
  - Two figures placed after the same paragraph were inserted in reverse order. That is fixed, and buổi 12's order is corrected.
- **Data and environment:**
  - Added descriptions of 10 new datasets to `tools/tu_hoc/du_lieu.toml`.
  - Installed `dtaidistance`, `ruptures`, `pywavelets` and `holidays` into the shared pandas3 environment. Buổi 12's `NGHIEN-CUU.md` still lists PyWavelets 1.8.0, but the shared version table installs 1.10.0; all numbers still match.
- **Length:** the notebooks are 3.600–4.300 words, a bit longer than buổi 8. Much of that is the required concept boxes and the auto-generated dataset descriptions, so I kept them.

**Problems in the lesson content that need your decision (I didn't fix them):**
1. **Buổi 11, wrong change-point date.** The answer code runs PELT with `ruptures`' default `jump=5`, so change points can only land on multiples of 5. The "2/2020" COVID break is an artifact of that. With `jump=1` the agent got 4/2020 and 6/2021, and 56 break points instead of 43 on the raw series. Fixing it means changing `dap-an`, `code`, `tai-lieu.md` and the figures, then re-running the lab. I think it's worth a small follow-up phase.
2. **Buổi 13, Tết low point.** The document and figure `tet-di-dong` say the low of 0,62 falls on mùng 1. In the data it falls the day before (dates are in UTC), and mùng 1 is 0,63. The notebook states it correctly.
3. **Buổi 13, homework 3.** It names `Demand (MW) (Imputed)` as the corrected column, but the corrected column is `Demand (MW) (Adjusted)`. For ERCOT 2024 the raw and corrected series are identical, so the exercise as written shows no difference. The notebook uses the WALC region instead.
4. **Buổi 9 chart title.** `khong-gian-dac-trung.png` still says "18 đặc trưng" in its title. I fixed the script that draws it, but it only updates once the buổi 9 lab environment is set up.
5. **Homework you may want to check.** Buổi 10's homework 2 and 3 describe no concrete setup, so the agent chose one. Homework 2 deletes 30% of readings at the windiest hours and 3% elsewhere; homework 3 uses a naive forecast one hour ahead.
