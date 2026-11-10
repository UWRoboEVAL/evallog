# CSE583 Project Description

2026-11-04

## Overview

**evallog** is a pip-installable Python package (CLI + Python API) for robot policy evaluation. After every trial it tells the researcher, for each policy comparison, whether to keep going or stop, while keeping the chance of a false conclusion below a chosen level (e.g. 5%). It works with live trials (logged one at a time) and with existing records (replayed in order).

- Project type: **Type 3 (Create a Tool)**, with an optional **Type 2 dataset**: a cleaned, unified trial-level dataset built from our LIBERO rollouts and RoboArena records.
- Contribution: we use existing statistical methods; what is new is putting them inside the evaluation workflow, across many comparisons at once, for both live and existing records.
- Name: the package and repo are both **evallog**. The PyPI name "roboeval" is taken by an unrelated VLA simulation harness that outputs per-episode success but does no statistics, so our GitHub repo will be renamed from roboeval to evallog.

## Motivation

**Users:** robot-learning researchers who compare policies in simulation and on physical hardware.

Real-robot trials are slow and need a human operator, so papers usually report only 20–40 trials with no statistical guarantee (Badithela et al., 2025). Results often go into a hand-typed spreadsheet. This causes three problems:

| Problem | What goes wrong |
|---|---|
| No uncertainty | "75% vs 60%" over 20 trials each is called a win, but the confidence intervals overlap heavily. |
| Invalid stopping | Running more trials when results are close, then re-testing, is a form of p-hacking that breaks the guarantee (Snyder et al., RSS 2025). |
| Lost context | Initial conditions, failure modes and checkpoint IDs live in free-text notes, so trials cannot be paired across policies or audited later. |

Further evidence:

- A survey of 13 recent real-robot VLA papers found typical samples of 10–20 trials per condition, and none reported confidence intervals or paired tests (PhAIL, arXiv 2605.29710).
- Best-practice recommendations exist (Kress-Gazit et al., "Robot Learning as an Empirical Science", arXiv 2409.09491), but no lightweight tool applies them during evaluation.

Existing tools do not cover this need:

| Tool | What it does | Why it does not cover our need |
|---|---|---|
| fieldtrial (Apache-2.0) | Full framework for planning and running real-robot studies: operator console, randomized blocks, blinding, group-sequential and anytime-valid stopping | Sequential stopping supports only two arms; no per-task sequential decisions across many tasks; explicitly not for simulation benchmarks; heavy (web server, runners); not designed to analyze existing records such as RoboArena or published results; first released Oct 2026 and not yet run on a real robot |
| STEP (TRI, RSS 2025) | Sequential test for two policies | Binary success only; reference code is CC BY-NC 4.0 (non-commercial), so we will not use it |
| N-SCORE (RSS 2026) | Sequential test supporting partial credit | The repo has no license file, so we will not use its code; cited as related work only |
| HF Robot Policy Evaluation Harness | Bayesian comparison on an uploaded CSV | Works only after the fact; no live stopping decisions |
| roboeval (PyPI) | Runs policy rollouts across simulators and outputs per-episode success | No statistics. Complementary: a possible future input source |
| W&B / MLflow | Track training runs | Not trials; no pairing or stopping rules |
| Spreadsheets | What labs actually use | No statistics, no schema |

**Our gap:** a lightweight library that (1) analyzes many policy comparisons at once with multiple-comparison control, (2) works on both live trials and existing records, (3) supports binary success and partial-progress scores, and (4) plugs into existing evaluation scripts.

## Approach

evallog is a `pip install`-able package with a CLI and a Python API. Example session:

```bash
evallog init my-study
cd my-study
evallog add --policy B --task cup --success 1 --pair t3-init07
evallog status
evallog report
```

The Python API mirrors the CLI: `Study("my-study").add(policy="B", ...)`.

### Study folder

A study is a folder with `study.yaml` (settings), `trials.csv` (append-only; corrections are added as new rows) and `reports/`. `study.yaml` fields: `study_id`, `baseline`, `policies`, `tasks`, `metric` (success | progress), `alpha` (default 0.05), `delta` (default 0.10), `max_trials` (default 100), `correction` (fwer | fdr).

### Statistics

- **Method:** anytime-valid betting confidence sequences (Waudby-Smith & Ramdas, JRSS-B 2024), valid no matter how often results are checked. They work for any outcome in [0, 1], so both binary success and progress scores. Paired comparisons use the per-pair difference mapped to [0, 1].
- **Implementation:** we implement it ourselves and verify against the reference package confseq (MIT). confseq only supports Python ≤ 3.10, so we generate its outputs once in a separate environment and store them as test fixtures.
- **Paired vs. unpaired:** sequential decisions support paired comparisons only. Unpaired aggregate results (papers) use fixed-sample methods (Wilson / Clopper-Pearson intervals; Fisher or Barnard exact test).
- **Multiple comparisons:** default Bonferroni (family-wise error control, alpha/K per comparison); optional e-BH (false discovery rate). The set of comparisons K is fixed in `study.yaml` before data collection.
- **Metrics:** LIBERO uses binary success. RoboArena uses both: the progress score is primary, and success is shown alongside to demonstrate how partial credit can stop earlier. delta is interpreted on the chosen metric's scale.

Four possible conclusions per comparison:

| Conclusion | Rule |
|---|---|
| B better | Interval entirely above 0 |
| A better | Interval entirely below 0 |
| No meaningful difference | Interval entirely within −delta..+delta |
| Inconclusive | max_trials reached |

### Components

Four components, one owner each:

| Component | What it does | Input → Output |
|---|---|---|
| Data import | RoboArena importer, CSV importer, paper-results table, policy-name alias table, schema validation | Raw files → trial table |
| LIBERO rollouts & logger | `scripts/run_libero.py`, pi0.5 variants, `evallog add` and Python API, TrialStore | Simulator / user → trial table |
| Statistics engine | Confidence sequences, paired comparison, Bonferroni and e-BH, decision rules, confseq-based tests, error-rate simulations | Trial table + settings → intervals and decisions |
| Report & dashboard | Replay (time order and random orders), HTML report, later Streamlit | Decisions → tables, plots, report |

### Interfaces and storage

Three interfaces are fixed in week 1: (a) the trial table schema, (b) the stats engine input/output, (c) the `study.yaml` schema.

Trial table schema (one row = one trial of one policy):

| Fields | Columns |
|---|---|
| Required | trial_id, study_id, source (real \| sim \| roboarena), timestamp, policy, task, success (0/1) |
| Optional | progress (0–1), pair_id, condition_id, failure_mode, evaluator, seed, machine, software_version |

RoboArena pair-level fields (preference, free-text reason) go in a separate pair table. Storage is CSV behind a TrialStore interface, so a SQLite backend can be added later without changing other modules.

### Report

| Phase | Form | Contents |
|---|---|---|
| 1 (before Dec 1) | Static HTML report | Status table (one row per comparison: colored decision, trial count, interval) and an evidence plot (interval narrowing over trials, stopping point marked) |
| 2 | Streamlit dashboard | Adds policy comparison plots with error bars, failure-mode counts, filters, a replay animation, and a page with buttons to log a trial (calling the same `Study.add` API) |

### Repo structure

Follows the course example uwseds/entropy_plus:

- `src/evallog/`: `schema.py`, `io/`, `logger.py`, `stats/`, `replay.py`, `report/`, `cli.py`
- `tests/` at top level, `docs/`, `examples/`, `data/` (small files only), `scripts/run_libero.py`
- `pyproject.toml`, `environment.yaml` (conda, Python 3.12), `.github/workflows/`

LIBERO and LeRobot live in a separate `scripts/environment-libero.yaml` and are not package dependencies. Large raw data (RoboArena dumps, full LIBERO rollouts) stay outside the repo; only small samples are committed.

### Scope

| | Items |
|---|---|
| Extensible (if time allows) | Pre-study planning of how many trials are needed (power analysis); a full operator interface in the GUI; a database (SQLite) backend |
| Out of scope | Controlling robots or running rollouts inside evallog; video capture; training-time metrics; Isaac Sim; training new policies; new statistical methods; using STEP or N-SCORE code; unpaired sequential comparisons; blinding; trial scheduling; new real-robot trials or our lab's real-robot data (possible bonus only with PI approval) |

## Dataset & Evaluation

### Data sources

| Source | Role | Details |
|---|---|---|
| LIBERO rollouts (LeRobot policies on LIBERO) | Main simulation dataset (we generate it); per-task, paired, multi-policy demo | Policies: variants of lerobot/pi05_libero_finetuned (reported 97.5% average on LIBERO's four suites) with controlled degradation (e.g. action-noise levels, shorter action-chunk execution), giving known strong-to-weak gaps without training.<br><br>Initial run: LIBERO-10, 3 variants × 10 tasks × 50 fixed initial states = 1,500 rollouts, after a 20-rollout pilot to measure time per rollout.<br><br>Run on three teammates' Linux machines, split by task (each machine runs all variants for its tasks, so pairs never cross machines), with a pinned LeRobot version, checkpoint revision and seeds, one shared script, and a 20-episode cross-machine consistency check before the full run.<br><br>Results are saved once as CSV; all later analysis is offline (no GPU needed). |
| RoboArena (public) | Real-robot dataset | Distributed, double-blind pairwise A/B evaluations of policies on DROID Franka arms; each policy gets a 0–100 progress score, plus a preference and a free-text reason (arXiv 2506.18123; data dumps on Hugging Face under RoboArena).<br><br>Import: each A/B evaluation becomes two trial rows sharing a pair_id; progress = score / 100; success = (score == 100).<br><br>Open, to verify: file format and fields of the latest dump, list of policies, number of evaluations. |
| Published paper results (we curate) | Reported results, analyzed with fixed-sample methods and used in the dataset joins | 5–10 papers, 20–40 rows. Only results that report trial counts are included; rows without counts are excluded and listed. The final paper list is chosen after confirming which policies appear in RoboArena. |
| Simulated Bernoulli trials | Not a dataset; statistics validation only | Used only to validate the statistics, because the true answer is known. |

### Dataset joins

The course's two-dataset requirement is met by joining on normalized policy name:

| Join | Question |
|---|---|
| Paper-reported LIBERO numbers vs. our LIBERO rollouts | Are reported success rates inside our intervals? |
| Paper claims ("A beats B") vs. RoboArena head-to-head results | Does the direction agree? Tasks differ, so only direction is compared, not magnitude. |

### Replay protocol

RoboArena is replayed in timestamp order (the real order). LIBERO is replayed in many random orders (e.g. 1,000, fixed seed) to report the distribution of stopping times and how often the early decision matches the full-data result. Saved trials are reported as hypothetical savings.

### Validation

Each check uses 10,000 simulated sessions:

1. 95% intervals contain the true success rate in about 95% of sessions.
2. When two policies are equal, the comparison test's Type I error stays at or below alpha.
3. At equal power, sequential stopping needs fewer trials than a fixed-sample test, in the same direction STEP reports.

## Timeline

Course dates:

| Dates | Work |
|---|---|
| Nov 5–9 | Fix the three interfaces; repo skeleton and CI; download RoboArena and verify its fields; install LIBERO on three Linux machines and run the 20-rollout pilot |
| Nov 10 | Components design due |
| Nov 10–17 | Technology Review prep; minimum working path: CSV import → single paired confidence sequence → printed decision |
| Nov 17 | Technology Review |
| Nov 17–25 | RoboArena importer; multiple comparisons and corrections; four decisions; full LIBERO run (finish before Thanksgiving) |
| Dec 1 | Standups and instructor consultation; the full pipeline must be demoable |
| Dec 1–10 | HTML report, random-order replay experiments, error-rate validation, tests and CI |
| Dec 10–15 | Feature freeze, docs, example notebooks, presentation |
| Dec 16 | Final presentation |

### Open items

- Verify RoboArena data format, fields, policy list and size.
- Finalize the paper list after the RoboArena policy list is known.
- Rename the GitHub repo from roboeval to evallog.
- Assign component owners and course documents.
- Decide the Technology Review topic and the detailed test plan.

## Team & Responsibilities

Each component has one owner, who also reviews PRs for the neighboring component. Each owner edits only the matching sections of this doc; to change someone else's section, leave a comment instead of editing it directly. Every change goes through a pull request with at least one reviewer.

| Component | Owner | Doc sections |
|---|---|---|
| Data import | *TBD* | Dataset & Evaluation (data sources, joins) |
| LIBERO rollouts & logger | *Hao(?* | Approach (study folder, logger, storage) |
| Statistics engine | *TBD* | Approach (statistics), Dataset & Evaluation (validation) |
| Report & dashboard | *TBD* | Approach (report), Overview |

## References

- Badithela et al., 2025. [arxiv.org/abs/2510.04354](https://arxiv.org/abs/2510.04354)
- Snyder et al., STEP, RSS 2025. [arxiv.org/abs/2503.10966](https://arxiv.org/abs/2503.10966)
- N-SCORE, RSS 2026. [roboticsconference.org/program/papers/76](https://roboticsconference.org/program/papers/76)
- fieldtrial. [github.com/rokbenko/fieldtrial](https://github.com/rokbenko/fieldtrial)
- RoboArena. [arxiv.org/abs/2506.18123](https://arxiv.org/abs/2506.18123)
- LeRobot LIBERO docs. [huggingface.co/docs/lerobot/libero](https://huggingface.co/docs/lerobot/libero)
- confseq. [pypi.org/project/confseq](https://pypi.org/project/confseq)
- Waudby-Smith & Ramdas, "Estimating means of bounded random variables by betting", JRSS-B 2024. [arxiv.org/abs/2010.09686](https://arxiv.org/abs/2010.09686)
- Kress-Gazit et al., "Robot Learning as an Empirical Science". [arxiv.org/abs/2409.09491](https://arxiv.org/abs/2409.09491)
- PhAIL. [arxiv.org/abs/2605.29710](https://arxiv.org/abs/2605.29710)
- roboeval. [pypi.org/project/roboeval](https://pypi.org/project/roboeval)
- uwseds/entropy_plus. [github.com/uwseds/entropy_plus](https://github.com/uwseds/entropy_plus)
