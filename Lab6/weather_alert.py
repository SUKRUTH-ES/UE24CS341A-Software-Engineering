SEVERITY = {"none": 0, "advisory": 1, "watch": 2, "warning": 3}


def wind_alert(speed_kmh):
    if speed_kmh >= 89:
        return "warning"
    if speed_kmh >= 62:
        return "watch"
    if speed_kmh >= 39:
        return "advisory"
    return "none"


def rain_alert(mm_per_hour, soil_saturated):
    if mm_per_hour >= 50:
        if soil_saturated:
            return "warning"
        return "watch"
    if mm_per_hour >= 10:
        if soil_saturated:
            return "watch"
        return "advisory"
    return "none"


def heat_alert(temp_c, humidity):
    index = temp_c
    if humidity > 40:
        index += (humidity - 40) * 0.1
    if index >= 45:
        return "warning"
    if index >= 40:
        return "watch"
    if index >= 35:
        return "advisory"
    return "none"


def overall_alert(alerts):
    worst = "none"
    for alert in alerts:
        if alert not in SEVERITY:
            raise ValueError("unknown alert")
        if SEVERITY[alert] > SEVERITY[worst]:
            worst = alert
    return worst
