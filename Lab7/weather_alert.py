"""Weather alert helpers, hardened against invalid input (Lab 7 fixed version).

Every function returns None when its input is invalid instead of raising,
so a bad reading can never crash the program. The bugs fixed here were
found by fuzzing with Hypothesis (see test_weather_alert.py and README.md).
"""
import math

MIN_TEMP_C, MAX_TEMP_C = -100.0, 100.0   # wider than any recorded air temperature
MAX_WIND_KMH = 500                       # wider than any recorded wind gust


def _to_finite_float(text):
    """Return text as a finite float, or None if it isn't one."""
    try:
        value = float(text)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def parse_reading(text):
    """Parse 'temperature/humidity', e.g. '35.5/80' -> (35.5, 80).

    Returns None unless the input is a string with exactly one '/', a
    finite temperature between -100 and 100 C, and a whole-number
    humidity between 0 and 100 %.
    """
    if not isinstance(text, str):
        return None
    parts = text.split("/")
    if len(parts) != 2:
        return None
    temp = _to_finite_float(parts[0])
    try:
        humidity = int(parts[1])
    except ValueError:
        return None
    if temp is None or not MIN_TEMP_C <= temp <= MAX_TEMP_C:
        return None
    if not 0 <= humidity <= 100:
        return None
    return temp, humidity


def wind_category(speed_text):
    """Grade a wind speed in km/h: 'none', 'advisory' (>= 39) or 'warning' (>= 89).

    Accepts a whole-number string (or int). Returns None for anything that
    isn't a whole number between 0 and 500.
    """
    if isinstance(speed_text, bool):
        return None
    if isinstance(speed_text, int):
        speed = speed_text
    elif isinstance(speed_text, str):
        try:
            speed = int(speed_text)
        except ValueError:
            return None
    else:
        return None
    if not 0 <= speed <= MAX_WIND_KMH:
        return None
    if speed >= 89:
        return "warning"
    if speed >= 39:
        return "advisory"
    return "none"


def rainfall_spread(readings_csv):
    """Return max - min of comma-separated hourly rainfall readings in mm.

    Returns None unless every reading is a finite number >= 0 (so empty
    input, blank entries like '1,,3', text, nan and inf are all rejected).
    """
    if not isinstance(readings_csv, str):
        return None
    readings = []
    for part in readings_csv.split(","):
        value = _to_finite_float(part)
        if value is None or value < 0:
            return None
        readings.append(value)
    return max(readings) - min(readings)


def main():
    """Read three values from the user and show each result."""
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    if result is None:
        print("Invalid reading: use temperature/humidity, e.g. 35.5/80 (humidity 0-100)")
    else:
        print("Temperature and Humidity:", result)

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    if result is None:
        print("Invalid wind speed: enter a whole number from 0 to 500")
    else:
        print("Wind Category:", result)

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    if result is None:
        print("Invalid rainfall list: enter numbers >= 0 separated by commas, e.g. 2,5.5,10")
    else:
        print("Rainfall Spread:", result)


if __name__ == "__main__":
    main()
