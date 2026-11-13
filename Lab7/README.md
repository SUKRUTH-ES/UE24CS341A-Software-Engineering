# Lab 7 — Fuzzing for Input Validation Bugs (Hypothesis)

**Name:** ES Sukruth
**SRN:** PES1UG24CS160
**Assigned repo:** `SETAPESU26/L6_L7_32_weather_alert` (folder `lab7/`)
**Submitted in:** `SUKRUTH-ES/UE24CS341A-Software-Engineering`
**Script under test:** `weather_alert.py`. This is the handout's `processor.py`, under the name used in the assigned repo.

## Results

| | Original script (`before/`) | Fixed script |
|---|---|---|
| Fuzz test results | **7 failed**, 3 passed | **10 passed** (also rerun with 3 different random seeds) |
| Distinct failures found by Hypothesis | 14 (table below) | 0 |
| `python weather_alert.py` with bad input such as `hello` | crashes with `ValueError` traceback | prints `Invalid reading: ...` and continues |
| `python weather_alert.py` with the example input | `(35.5, 80)`, `advisory`, `8.0` | same, unchanged |

## Deliverables

| Deliverable | File |
|---|---|
| Fixed application script | `weather_alert.py` |
| Completed Hypothesis test file | `test_weather_alert.py` |
| PDF with the four screenshots | `PES1UG24CS160_Lab7_FuzzTesting.pdf` |
| Screenshots | `screenshots/` |
| Original buggy script (unchanged) | `before/weather_alert.py` |
| Starter test file from the repo (unchanged) | `before/starter_tests.py` |
| Copy of the completed tests, to run against the original | `before/test_weather_alert.py` |
| Test log: original script (7 failed) | `before/fuzz_failures_before.txt` |
| Test log: fixed script (10 passed) | `fuzz_results_after.txt` |

## How to run

```bash
pip install hypothesis pytest

# Original, buggy version
cd before
python weather_alert.py
python -m pytest test_weather_alert.py

# Fixed version
cd ..
python weather_alert.py
python -m pytest test_weather_alert.py
```

## The tests (`test_weather_alert.py`)

**No-crash fuzzing (the starter's three tests, completed).** Each function gets random Unicode text and
`None`, and must not raise. Hypothesis seldom produces a string shaped like `35.5/80` or `2,5.5,10` by
chance, so I also added generators that build strings in that shape from awkward pieces: huge integers,
`nan`, `inf`, `1e999`, blanks and short random text. One more test feeds all three functions values
that aren't strings at all (`int`, `float`, `bool`, `bytes`, `list`, `None`).

**Behaviour properties.** Not crashing isn't enough: a wrong answer has to fail too.
- `parse_reading` gives back exactly the temperature and humidity it was given, for any valid input. When it
  returns a result, the temperature is finite and the humidity is between 0 and 100.
- `wind_category` matches the 39 and 89 km/h thresholds for every speed from 0 to 400, and rejects negative speeds.
- `rainfall_spread` equals `max - min` for any list of valid readings, and its result is never `nan`, `inf` or negative.

## Bugs found by fuzzing

All 14 were found by Hypothesis and shrunk to the minimal input shown.

| # | Function | Failing input | What happened (original code) | Kind |
|---|---|---|---|---|
| 1 | `parse_reading` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | crash |
| 2 | `parse_reading` | `''` (no `/`) | `ValueError: not enough values to unpack` | crash |
| 3 | `parse_reading` | `'/'` | `ValueError: could not convert string to float: ''` | crash |
| 4 | `parse_reading` | `b''` (bytes) | `TypeError: a bytes-like object is required` | crash |
| 5 | `parse_reading` | `'0/-1'` | returned humidity **-1**, accepted silently | wrong result |
| 6 | `parse_reading` | `'NAN/0'` | returned temperature **nan**, accepted silently | wrong result |
| 7 | `wind_category` | `None` | `TypeError: int() argument must be ... not 'NoneType'` | crash |
| 8 | `wind_category` | `''` | `ValueError: invalid literal for int()` | crash |
| 9 | `wind_category` | `'-1'` | graded a negative wind speed as `'none'` | wrong result |
| 10 | `rainfall_spread` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | crash |
| 11 | `rainfall_spread` | `''` | `ValueError: could not convert string to float: ''` | crash |
| 12 | `rainfall_spread` | `'NAN'` / `'INF'` | returned **nan** as the spread | wrong result |
| 13 | all three | non-string values (`int`, `list`, ...) | assorted `AttributeError` / `TypeError` | crash |
| 14 | `main()` | any of the above, typed at the prompt | the whole program stops with a traceback | crash |

The same causes also break these inputs, checked by hand: `'1/2/3'` (too many values), `'1,,3'` (blank
entry), `'abc'`, and `'1e999'` (which becomes `inf`). The fixed version rejects all of them.

## Fixes (`weather_alert.py`)

The approach is defensive programming. Each function checks its input and returns **`None` for anything
invalid**, so it never raises. `main()` checks for `None` and prints a clear message instead of a traceback.

| Function | Validation added |
|---|---|
| `parse_reading` | must be a `str` with exactly one `/`; temperature must be a **finite** float between -100 and 100 °C; humidity must be a whole number between 0 and 100 |
| `wind_category` | must be a `str` or `int` (not `bool`) holding a whole number between 0 and 500 km/h. The 39 and 89 thresholds are unchanged |
| `rainfall_spread` | must be a `str`; every comma-separated entry must be a **finite** number ≥ 0. Empty input and blank entries are rejected |
| `main()` | prints `Invalid ...: <what is expected>` when a function returns `None` |

`ValueError` and `TypeError` are caught only where a conversion can fail. There is no blanket
`except Exception`, so real programming errors would still surface. Valid input gives exactly the same
output as before.

## Observations

- Four of the 14 bugs **don't crash** (rows 5, 6, 9 and 12). They return nonsense, such as negative humidity, a `nan` temperature,
  or a grade for a negative wind speed. A crash-only fuzz test can't see them; the behaviour properties caught them.
- The starter's `st.text() | st.none()` input found the crashes within a few examples. The humidity and
  `nan` bugs needed the shaped generators, because random text almost never contains a valid `number/number`.
- The original `wind_category` has no `watch` level, unlike the Lab 6 module, which had one at 62 km/h. This
  isn't an input-validation bug, so I left the grading logic as it was.

## Note on screenshots

All four screenshots in `screenshots/` and in the PDF are real captures of the terminal.
