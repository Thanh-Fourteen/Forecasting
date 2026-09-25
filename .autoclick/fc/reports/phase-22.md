# phase 22

_2026-09-24 10:45:02_

Phase 22 is done: sessions 22 and 23 are written and pass every check, and Phase 22 is marked ✅ in `todos.md`, `todos/phase-22.md` and `todos/tong-quan.md`. Nothing is committed yet.

**Your two notes during the phase:**
- **Rewritten notes (`note-viet-lai.md`):** both sessions' notes are now in my own words, about 500 words each. Each section is a few sentences, an everyday comparison and a "Nhớ:" line, with only the key numbers (they match `tai-lieu.md`).
- **The rule:** I updated it in `todos/quy-uoc.md` (V.7 and the Definition of Done), `CLAUDE.md`, `todos/phase-49.md` and the Phase 49–52 prompts. It now reads "own words, short, easy, about 500–700 words", with sessions 22–23 as the template. I also saved it to memory. The notes for sessions 1–9 were written before this rule and are longer.

**Needs your OK — dataset change for session 23.** Session 23 uses UCI Online Retail II (500 products × 604 selling days) instead of M5. This machine has no Kaggle account that has accepted the M5 rules, so M5 has no sha256 in the catalogue and can't be included. The phase plan already named this dataset as the fallback. M5 is now homework for learners with a Kaggle account, and I updated the roadmap. Tell me if you'd rather wait for M5.

| | Session 22 — forecasting as regression | Session 23 — gradient boosting |
|---|---|---|
| Data | 10,000 Wikipedia pages (Web Traffic) | 500 products, Online Retail II |
| Length | 4,115 words, 13-page PDF | 4,105 words, 13-page PDF |
| Readability checker | 0 flags | 0 flags |
| Read-through as new learner | round 1: 0 blocking, 3 hard → round 2: 0 / 0 | round 1: 0 blocking, 3 hard → round 2: 0 / 0 |
| Grader | answer key 10/10 green; `code/` fails 4/10, exactly the deliberate holes | answer key 7/7 green; `code/` fails 2/7, exactly the deliberate holes |
| Clean-machine run (fresh uv and data caches) | passes, 4.4 min | passes, 2.0 min |

The clean-machine timings reused the saved backtest and tuning results. On a first run, the 10,000-page backtest takes 5–15 minutes and each Optuna study 3–10 minutes, depending on the machine.

**Main results (from real runs, seed 0):**
- **Session 22:** one LightGBM model for all 10,000 pages beats a separate AutoETS per page. Average RMSSE is 0.916 vs 0.951; seasonal naive is 1.099. Page by page it only wins 58% of the time, and near 50% on very low-traffic pages, which the lesson states plainly.
- **Session 22, the deliberate leak:** the direct strategy built with lag 1 for every horizon looks falsely better (0.477 vs 0.511 honest).
- **Session 23, loss function:** switching from squared loss to Tweedie improves WRMSSE from 0.709 to 0.680.
- **Session 23, tuning:** with default settings, Tweedie does not beat AutoETS (0.680 vs 0.674). It only wins once tuned by Optuna with time-based folds (0.669). Tuning with shuffled KFold gives 0.678, which does not.
- **Session 23, explaining one forecast (SHAP):** product 22659 on 1/12/2011 was forecast at 251 units against 6 actual.
- **Session 23, effect of price (partial dependence):** unconstrained, predicted sales *rise* with price (wrong direction). Forcing "higher price never raises the forecast" fixes the direction at no accuracy cost (WRMSSE 0.678).

**Other changes:**
- **SHAP without the `shap` package:** it can't be installed alongside numpy 2.5.3, so I used LightGBM's built-in version, which uses the same algorithm.
- **Smaller local model in session 22:** AutoETS runs without a trend component. The full search is about 6× slower on this machine, and on 300 pages the error was nearly the same.
- **Glossary (Phụ lục E):** added 6 new terms. Sessions 15 and 22–23 still pass; sessions 2 and 5 had checker flags before this phase.
- **`tools/dong_goi.py`:** it now leaves `lab/du-lieu/cache/` out of the learner zip. These are results from my machine, and the code rebuilds them when missing.
- **Phase 49 status:** it was ✅ in `todos.md` but still 🔲 in `tong-quan.md`. I aligned it, so the total is now 24/53.

**Next:** Phase 23 (session 24 + mid-course project 2).

Sources:
- [Montero-Manso & Hyndman 2021](https://arxiv.org/abs/2008.00444)
- [Taieb et al. 2012](https://arxiv.org/abs/1108.3259)
- [M5 accuracy results](https://statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf)
- [Bergmeir, Hyndman & Koo 2018](https://robjhyndman.com/publications/cv-time-series/)
- [LightGBM parameters](https://lightgbm.readthedocs.io/en/latest/Parameters.html)
- [mlforecast releases](https://github.com/Nixtla/mlforecast/releases)
- [Optuna releases](https://github.com/optuna/optuna/releases)
- [Damato et al. 2026](https://arxiv.org/abs/2601.14031)
