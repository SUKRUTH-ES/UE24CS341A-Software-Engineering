def parse_reading(text):
    temp, humidity = text.split('/')
    return float(temp), int(humidity)

def wind_category(speed_text):
    speed = int(speed_text)
    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'

def rainfall_spread(readings_csv):
    readings = [float(r) for r in readings_csv.split(',')]
    return max(readings) - min(readings)

def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    print("Temperature and Humidity:", result)

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    print("Wind Category:", result)

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    print("Rainfall Spread:", result)

if __name__ == "__main__":
    main()
