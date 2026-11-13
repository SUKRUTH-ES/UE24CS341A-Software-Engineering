"""Lab 7 - Fuzz testing weather_alert.py with Hypothesis.

Name: ES Sukruth | SRN: PES1UG24CS160 | Repo: SETAPESU26/L6_L7_32_weather_alert

Two kinds of property are checked for each of the three functions:

1. No-crash fuzzing (the three starter tests, completed): throw random text
   and None at the function. It may reject bad input by returning None, but
   it must never raise.
2. Behaviour properties: for well-formed input the result must be correct,
   and for any input the result must be in the allowed set of values.
"""
import math

from hypothesis import given, settings, strategies as st
from weather_alert import parse_reading, wind_category, rainfall_spread

FUZZ = settings(max_examples=500)

# Any value at all: text, None, numbers, bytes, lists, ...
anything = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.binary(), st.lists(st.text()),
)

# Random text rarely looks like "35.5/80" or "2,5.5,10", so also build inputs
# with the right shape out of awkward pieces: huge numbers, nan, inf, blanks.
token = st.one_of(
    st.integers().map(str), st.floats().map(str), st.text(max_size=3),
    st.sampled_from(["nan", "inf", "-inf", "", " ", "1e999", "-0"]),
)
reading_like = st.tuples(token, token).map("/".join)
csv_like = st.lists(token, max_size=6).map(",".join)


# ---------------------------------------------------------------------------
# 1. No-crash fuzz tests (starter tests from the assigned repo, completed)
# ---------------------------------------------------------------------------
@FUZZ
@given(st.text() | st.none() | reading_like)
def test_parse_reading_no_crash(s):
    try:
        parse_reading(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_reading crashed on {s!r} with: {type(e).__name__}: {e}"


@FUZZ
@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    try:
        wind_category(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"wind_category crashed on {s!r} with: {type(e).__name__}: {e}"


@FUZZ
@given(st.text() | st.none() | csv_like)
def test_rainfall_spread_no_crash(s):
    try:
        rainfall_spread(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"rainfall_spread crashed on {s!r} with: {type(e).__name__}: {e}"


# Wider fuzzing: inputs that are not even strings.
@FUZZ
@given(anything)
def test_all_functions_survive_any_type(value):
    for fn in (parse_reading, wind_category, rainfall_spread):
        try:
            fn(value)
        except Exception as e:  # pylint: disable=broad-except
            assert False, f"{fn.__name__} crashed on {value!r} with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 2. Behaviour properties
# ---------------------------------------------------------------------------
# parse_reading -------------------------------------------------------------
@given(st.floats(min_value=-90, max_value=60, allow_nan=False),
       st.integers(min_value=0, max_value=100))
def test_parse_reading_valid_roundtrip(temp, humidity):
    assert parse_reading(f"{temp}/{humidity}") == (temp, humidity)


@FUZZ
@given(st.text() | st.none() | reading_like)
def test_parse_reading_result_is_sane(s):
    try:
        result = parse_reading(s)
    except Exception:  # pylint: disable=broad-except
        return  # crashes are reported by the no-crash test above
    if result is not None:
        temp, humidity = result
        assert math.isfinite(temp), f"non-finite temperature from {s!r}"
        assert 0 <= humidity <= 100, f"humidity {humidity} out of range from {s!r}"


# wind_category -------------------------------------------------------------
@given(st.integers(min_value=0, max_value=400))
def test_wind_category_matches_thresholds(speed):
    expected = "warning" if speed >= 89 else "advisory" if speed >= 39 else "none"
    assert wind_category(str(speed)) == expected


@given(st.integers(max_value=-1))
def test_wind_category_rejects_negative_speed(speed):
    assert wind_category(str(speed)) is None, f"negative speed {speed} was graded"


# rainfall_spread -----------------------------------------------------------
@given(st.lists(st.floats(min_value=0, max_value=500, allow_nan=False), min_size=1))
def test_rainfall_spread_valid_values(values):
    csv = ",".join(str(v) for v in values)
    assert rainfall_spread(csv) == max(values) - min(values)


@FUZZ
@given(st.text() | st.none() | csv_like)
def test_rainfall_spread_result_is_sane(s):
    try:
        result = rainfall_spread(s)
    except Exception:  # pylint: disable=broad-except
        return  # crashes are reported by the no-crash test above
    if result is not None:
        assert math.isfinite(result), f"non-finite spread {result} from {s!r}"
        assert result >= 0, f"negative spread {result} from {s!r}"
