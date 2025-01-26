from datetime import datetime, timedelta

import pytz

moscow_tz = pytz.timezone("Europe/Moscow")

CURRENT_DATETIME = datetime.now(moscow_tz)


def finish_time(minutes):
    new_time = CURRENT_DATETIME + timedelta(minutes=minutes)

    formatted_time = new_time.strftime("%H:%M")
    return formatted_time
