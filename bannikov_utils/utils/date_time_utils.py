import datetime
import re
from typing import List


def parse_datetime_sec(datetime_as_str: str,
                   datetime_patterns: List[str],
                   timezone=None
                   ) -> datetime.datetime:
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
    second = int(parsed.group("seconds"))
    millisecond = 0

    datetime_ = datetime.datetime(
        year,
        month,
        day,
        hour,
        minute,
        second,
        millisecond,
        tzinfo=timezone
    )
    return datetime_