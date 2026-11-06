"""Lab 6 - Code (line) coverage tests for weather_alert.py.

Name: ES Sukruth | SRN: PES1UG24CS160 | Repo: SETAPESU26/L6_L7_32_weather_alert

Goal: execute every line of weather_alert.py at least once (>= 90% line
coverage). Each test is chosen to reach a `return` / statement that the
starter tests never reached. Branch coverage is NOT the goal here, so some
decision outcomes are deliberately left untested (see the branch file).
"""
import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


# ---- starter tests (from the assigned repo) ----
def test_calm_wind():
    assert wind_alert(10) == "none"


def test_no_alerts():
    assert overall_alert([]) == "none"


# ---- wind_alert: reach every return line ----
def test_wind_warning():
    assert wind_alert(100) == "warning"


def test_wind_watch():
    assert wind_alert(70) == "watch"


def test_wind_advisory():
    assert wind_alert(45) == "advisory"


# ---- rain_alert: reach every return line ----
def test_rain_heavy_saturated_warning():
    assert rain_alert(60, True) == "warning"


def test_rain_heavy_dry_watch():
    assert rain_alert(60, False) == "watch"


def test_rain_moderate_saturated_watch():
    assert rain_alert(20, True) == "watch"


def test_rain_moderate_dry_advisory():
    assert rain_alert(20, False) == "advisory"


def test_rain_light_none():
    assert rain_alert(5, False) == "none"


# ---- heat_alert: reach every line (all use humidity > 40) ----
def test_heat_warning():
    assert heat_alert(44, 60) == "warning"     # 44 + 2.0 = 46.0


def test_heat_watch():
    assert heat_alert(39, 60) == "watch"       # 39 + 2.0 = 41.0


def test_heat_advisory():
    assert heat_alert(34, 60) == "advisory"    # 34 + 2.0 = 36.0


def test_heat_none():
    assert heat_alert(20, 60) == "none"        # 20 + 2.0 = 22.0


# ---- overall_alert: reach the update line and the raise line ----
def test_overall_picks_worst():
    assert overall_alert(["advisory", "warning"]) == "warning"


def test_overall_unknown_alert_raises():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["storm"])
