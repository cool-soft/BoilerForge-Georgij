import datetime
import math
import re

import numpy as np

import column_names
from column_names import SOFT_M_TIMESTAMP


def round_datetime(src_datetime, time_tick_in_seconds):
    src_timestamp = src_datetime.timestamp()
    rounded_timestamp = math.ceil(src_timestamp / time_tick_in_seconds) * time_tick_in_seconds
    rounded_datetime = datetime.datetime.fromtimestamp(rounded_timestamp, tz=src_datetime.tzinfo)
    return rounded_datetime


def parse_datetime(datetime_as_str, datetime_patterns, timezone=None):
    for pattern in datetime_patterns:
        parsed = re.match(pattern, datetime_as_str)
        if parsed is not None:
            break
    else:
        raise ValueError("Date and time are not matched using existing patterns")

    year = int(parsed.group("year"))
    month = int(parsed.group("month"))
    day = int(parsed.group("day"))
    hour = int(parsed.group("hours"))
    minute = int(parsed.group("minutes"))
    second = 0
    millisecond = 0

    datetime_ = datetime.datetime(year, month, day, hour, minute, second, millisecond, tzinfo=timezone)
    return datetime_


def parse_time(time_as_str, time_parse_pattern):
    parsed = re.match(time_parse_pattern, time_as_str)
    hour = int(parsed.group("hour"))
    minute = int(parsed.group("min"))
    second = int(parsed.group("sec"))
    time = datetime.time(hour=hour, minute=minute, second=second)
    return time


def arithmetic_round(number):
    number_floor = math.floor(number)
    if number - number_floor < 0.5:
        rounded_number = number_floor
    else:
        rounded_number = number_floor + 1
    return rounded_number


def float_converter(value):
    if isinstance(value, str):
        value = value.replace(",", ".")
    value = float(value)
    return value


def average_values(x, window_len=4, window='hanning'):
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    if window_len < 3:
        return x

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]

    if window == 'flat':
        w = np.ones(window_len, 'd')
    else:
        w = getattr(np, window)(window_len)

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y[(window_len // 2 - 1 + (window_len % 2)):-(window_len // 2)]
    # return y


def filter_by_timestamp_closed(df, start_datetime, end_datetime):
    df = df[
        (df[column_names.TIMESTAMP] >= start_datetime) &
        (df[column_names.TIMESTAMP] <= end_datetime)
    ]
    return df
