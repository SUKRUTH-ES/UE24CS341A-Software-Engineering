"""Lab 6 - Branch coverage tests for weather_alert.py.

Name: ES Sukruth | SRN: PES1UG24CS160 | Repo: SETAPESU26/L6_L7_32_weather_alert

Goal: make every decision in weather_alert.py evaluate to BOTH True and
False (>= 90% branch coverage). The code-coverage suite already reached 100%
line coverage but left two branches unexercised:

  * 28->30  heat_alert: `humidity > 40` was never False
  * 44->41  overall_alert: `SEVERITY[alert] > SEVERITY[worst]` was never
            False inside the loop (alerts were always in rising order)

This file closes both gaps and also tests every threshold at its exact
boundary value (>= vs >), where off-by-one bugs usually hide.
"""
import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


# ---- starter tests (from the assigned repo) ----
def test_calm_wind():
    assert wind_alert(10) == "none"


def test_no_alerts():
    assert overall_alert([]) == "none"


# ---- wind_alert: each `if` True and False, at the boundaries ----
@pytest.mark.parametrize("speed, expected", [
    (89, "warning"),    # speed >= 89 True (boundary)
    (88, "watch"),      # >= 89 False, >= 62 True
    (62, "watch"),      # boundary
    (61, "advisory"),   # >= 62 False, >= 39 True
    (39, "advisory"),   # boundary
    (38, "none"),       # all three False
    (0, "none"),
])
def test_wind_alert_branches(speed, expected):
    assert wind_alert(speed) == expected


# ---- rain_alert: outer and nested `if` both ways ----
@pytest.mark.parametrize("mm, saturated, expected", [
    (50, True, "warning"),     # >= 50 True,  saturated True (boundary)
    (50, False, "watch"),      # >= 50 True,  saturated False
    (49, True, "watch"),       # >= 50 False, >= 10 True, saturated True
    (10, False, "advisory"),   # >= 10 True (boundary), saturated False
    (9, True, "none"),         # both thresholds False (soil ignored)
    (0, False, "none"),
])
def test_rain_alert_branches(mm, saturated, expected):
    assert rain_alert(mm, saturated) == expected


# ---- heat_alert: humidity adjustment taken and skipped ----
def test_heat_humidity_not_above_40_skips_adjustment():
    # humidity > 40 is False -> index stays at temp_c (branch 28->30)
    assert heat_alert(35, 40) == "advisory"
    assert heat_alert(34, 10) == "none"


def test_heat_humidity_above_40_raises_index():
    # same temperature, higher humidity pushes it up a level
    assert heat_alert(34, 30) == "none"
    assert heat_alert(34, 60) == "advisory"    # 34 + 2.0 = 36.0


@pytest.mark.parametrize("temp, humidity, expected", [
    (45, 20, "warning"),    # index >= 45 True (boundary, no adjustment)
    (40, 90, "warning"),    # 40 + 5.0 = 45.0 (boundary via adjustment)
    (44, 40, "watch"),      # >= 45 False, >= 40 True
    (40, 0, "watch"),       # boundary
    (39, 40, "advisory"),   # >= 40 False, >= 35 True
    (35, 0, "advisory"),    # boundary
    (34, 40, "none"),       # all three False
])
def test_heat_alert_thresholds(temp, humidity, expected):
    assert heat_alert(temp, humidity) == expected


# ---- overall_alert: loop, membership check and comparison both ways ----
def test_overall_worst_first_then_lower_ignored():
    # comparison False inside the loop (branch 44->41)
    assert overall_alert(["warning", "advisory", "none"]) == "warning"


def test_overall_equal_severity_does_not_replace():
    assert overall_alert(["watch", "watch"]) == "watch"


def test_overall_rising_order_updates_worst():
    assert overall_alert(["advisory", "watch", "warning"]) == "warning"


def test_overall_only_none():
    assert overall_alert(["none"]) == "none"


def test_overall_unknown_alert_raises():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["storm"])


def test_overall_unknown_after_valid_still_raises():
    with pytest.raises(ValueError):
        overall_alert(["watch", "WARNING"])   # case-sensitive lookup


def test_overall_combines_real_classifiers():
    alerts = [wind_alert(70), rain_alert(60, True), heat_alert(30, 20)]
    assert overall_alert(alerts) == "warning"
