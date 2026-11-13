from hypothesis import given, strategies as st
from weather_alert import parse_reading, wind_category, rainfall_spread

@given(st.text() | st.none())
def test_parse_reading_no_crash(s):

@given(st.text() | st.none())
def test_wind_category_no_crash(s):

@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
