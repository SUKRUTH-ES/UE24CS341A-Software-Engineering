import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

#Example test cases:
def test_calm_wind():
    assert wind_alert(10) == "none"

def test_no_alerts():
    assert overall_alert([]) == "none"

#Write the rest of the test cases so that the code is 90- 100% covered.
