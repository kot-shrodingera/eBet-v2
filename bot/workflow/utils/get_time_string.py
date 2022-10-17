from datetime import timedelta


def get_time_string(timedelta: timedelta) -> str:
    seconds = timedelta.seconds
    hours = seconds // 3600 + 24 * timedelta.days
    seconds = seconds - ((hours - 24 * timedelta.days) * 3600)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}'
