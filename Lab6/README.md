# Lab 6 — Code and Branch Coverage Analysis

**Name:** ES Sukruth
**SRN:** PES1UG24CS160
**Assigned repo:** `SETAPESU26/L6_L7_32_weather_alert` (folder `lab6/`)
**Submitted in:** `SUKRUTH-ES/UE24CS341A-Software-Engineering`
**Module under test:** `weather_alert.py` (Weather Alert Classifier: wind, rain, heat and overall alert levels)

## Results (for `weather_alert.py`)

| Test suite | Tests | Line coverage | Branch coverage | Missing branches |
|---|---|---|---|---|
| Starter `test_weather_alert.py` (given) | 2 | 32% (12/38) | 24% | most of the module |
| `CodeCoverageTest_PES1UG24CS160_weather_alert.py` | 16 | **100%** (38/38) | 97% | `28->30`, `44->41` |
| `BranchCoverageTest_PES1UG24CS160_weather_alert.py` | 31 | **100%** (38/38) | **100%** (28/28) | none |

Target was at least 90% for each type. Both targets are met, and all tests pass.

## Deliverables

| Deliverable | File |
|---|---|
| Code coverage test cases | `CodeCoverageTest_PES1UG24CS160_weather_alert.py` |
| Branch coverage test cases | `BranchCoverageTest_PES1UG24CS160_weather_alert.py` |
| Code coverage screenshot (≥ 90%) | `screenshots/02_code_coverage.png` |
| Branch coverage screenshot (≥ 90%) | `screenshots/04_branch_coverage.png` |
| Starter baseline, for reference | `screenshots/01_starter_baseline.png` |
| Line tests under `--branch`, showing the gap | `screenshots/03_code_tests_branch_view.png` |
| Raw terminal output for each screenshot | `screenshots/*.txt` |
| Module and starter test (unchanged, from the assigned repo) | `weather_alert.py`, `test_weather_alert.py` |

Commit 1 adds the code coverage tests and their screenshot. Commit 2 adds the branch coverage tests and their screenshot.

## How to run

```bash
pip install coverage pytest

# Code (line) coverage
python -m coverage run -m pytest CodeCoverageTest_PES1UG24CS160_weather_alert.py
python -m coverage report -m

# Branch coverage
python -m coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS160_weather_alert.py
python -m coverage report -m
```

## Analysis

### Step 1: code (line) coverage

The two starter tests only called `wind_alert(10)` and `overall_alert([])`, so
the whole of `rain_alert` and `heat_alert` never ran, along with every other
return in `wind_alert` and the body of the loop in `overall_alert`.

`CodeCoverageTest_...` adds one test for each `return` statement that hadn't
run yet:

- `wind_alert`: warning, watch and advisory.
- `rain_alert`: all five outcomes (heavy or moderate rain, with soil saturated or not, and light rain).
- `heat_alert`: all four levels. Every one of these tests uses humidity 60, so the humidity-adjustment line runs.
- `overall_alert`: a list that raises the worst level, and an unknown alert that raises `ValueError`.

That gives **100% line coverage**.

### Step 2: why 100% line coverage was not enough

Running the same 16 tests with `--branch` gives **97%** branch coverage, with two
partial branches (`screenshots/03_code_tests_branch_view.png`):

| Branch | Code | Outcome that never ran |
|---|---|---|
| `28->30` | `if humidity > 40:` in `heat_alert` | **False**: every heat test had humidity above 40, so the path that skips the adjustment was never tested |
| `44->41` | `if SEVERITY[alert] > SEVERITY[worst]:` in `overall_alert` | **False**: the alerts were always in rising order, so the case where a later alert is *not* worse was never tested |

Every line ran, but these two decisions were only ever true. This is the
false sense of security from line coverage that the handout describes. A bug
in either untested path (for example, adding the humidity bonus whatever the
humidity, or always overwriting `worst`) would have passed every test.

### Step 3: branch coverage

`BranchCoverageTest_...` closes both gaps and makes every decision evaluate both ways:

- **`heat_alert`**: humidity at or below 40 (`heat_alert(35, 40)`, `heat_alert(34, 10)`), plus a pair of
  tests with the same temperature to show the humidity bonus moving it up a level
  (`heat_alert(34, 30)` gives "none", `heat_alert(34, 60)` gives "advisory").
- **`overall_alert`**: worst alert first, then lower ones (`["warning", "advisory", "none"]`); equal severities
  (`["watch", "watch"]`, where the strict `>` doesn't replace); an unknown alert after a valid one;
  and the case-sensitive lookup (`"WARNING"` is rejected).
- **Boundary values**: every threshold is tested at its exact value and one below it
  (wind 89/88, 62/61, 39/38; rain 50/49, 10/9; heat index 45, 40, 35), because a `>=` written as `>`
  is the most likely bug in this kind of code.
- **Integration**: the three classifiers' outputs fed into `overall_alert`.

That gives **100% branch coverage (28/28 branches)**. Line coverage stays at 100%.

### Observations

- `wind_alert` and `rain_alert` use early `return`s, so for them line coverage already implied full
  branch coverage. The gaps only appeared where an `if` has no `else` and execution falls through
  (`heat_alert` line 28, and the loop in `overall_alert`).
- Path coverage is stricter still. `overall_alert` takes a different path for each order of
  inputs, so it has unboundedly many paths. 100% branch coverage doesn't mean every path was tested.
- Coverage only shows which code ran. It doesn't show the results were right. Every test here
  asserts an exact expected value, so the 100% figures come with real checks.

## Note on screenshots

The PNGs in `screenshots/` were rendered from the real terminal output of the commands shown in
them, run on this machine (Python 3.14.0, pytest 9.2.0, coverage 7.17.2). The same output is saved
next to each PNG as `.txt`.
