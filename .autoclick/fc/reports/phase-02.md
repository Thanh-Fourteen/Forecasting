# phase 2

_2026-09-17 23:39:24_

Phase 2 is done: lessons 01, 02 and 03 are finished and checked.

**Final checks**
- `tools/kiem_tra_doc_lap.sh`: all 3 lessons are self-contained.
- `ruff check .`: clean.
- `xuat_pdf.py 1 2 3` then `--kiem`: each of the three PDFs is **10 pages**.

**Grader results**

| Lesson | `code/` (should fail) | `dap-an/` (should pass) | Deliberate flaw → symptom students see |
|---|---|---|---|
| 01 | 4/8 pass | 8/8 | Model scored on data it was fitted on, no baseline → reports MAE 0.380, looks excellent |
| 02 | 3/8 pass | 8/8 | ±1.96σ on skewed data; i.i.d. bootstrap → a "95%" CI holds the true mean only 60% of the time |
| 03 | 1/11 pass | 11/11 | Naive timestamps, 4–5 h time-zone offset (4 in March), resample loses the DST hour → New York "hottest at 20h" |

**Lesson 1 (just finished)**
- **Data:** hourly UCI household power. A "calendar table" model (average by week of year × weekday × hour) is fitted on all data and scores **0.380**. Scored honestly with rolling forecasts from each 2010 Monday, it scores **0.508**, which loses to a simple average of the same hour over the last 4 weeks (**0.490**).
- **Aggregating to weekly totals flips the ranking:** calendar table 16.4 kWh vs 4-week average 27.9. This is taught as "granularity decides how you score" and ties to box 4 of the forecasting problem sheet.
- **Asymmetric cost** (shortfall 4 : surplus 1): adding the 0.8 quantile of 2009 errors cuts cost by 18.6% even though MAE gets 37% worse.
- **Materials:** the 6-box problem sheet template, the M1–M6 lessons table, a 10-question quiz and 5 figures.

**Deviations (all recorded in each NGHIEN-CUU.md)**
- **Lesson 2, medium (roadmap and todos already updated):** the ±1.96σ interval built from 2011 covers only 72.5% of 2012 because the level rose. Switching to empirical quantiles doesn't fix it (70.1%). Quantiles fix the shape of the tails; block bootstrap fixes the confidence interval of the mean. These are two separate problems.
- **Lesson 1, minor:**
  - FPP lists 4 predictability factors, not 3.
  - The four famous conclusions ("simple methods are not worse than complex ones", etc.) come from **M1**; M3 only supported them.
  - M2 has only a secondary summary, because the original paper returned 403.
  - M7 is left out because there is no official source.
- **Lesson 3, minor:**
  - It uses two months of data, March and November 2024, to cover both DST changes.
  - The main symptom is "hottest at 20h" instead of the roadmap's rain example.
  - The zone lookup has 265 zones, not the roadmap's 263.
  - Open-Meteo's `timezone=` parameter is wrong around DST, so the course always downloads in UTC.

Still blocked from earlier phases: the Hugging Face mirror (needs your consent to publish) and Kaggle. Nothing has been committed.

Sources used to verify M1/M2:
- [Hyndman – forecasting competitions](https://robjhyndman.com/hyndsight/forecasting-competitions/)
- [Open Forecasting – role of M competitions](https://openforecast.org/2024/03/14/the-role-of-m-competitions-in-forecasting/)
- [IIF – M2-Competition](https://forecasters.org/resources/time-series-data/m2-competition/)
- [ScienceDirect – M2 paper](https://www.sciencedirect.com/science/article/abs/pii/016920709390044N)
