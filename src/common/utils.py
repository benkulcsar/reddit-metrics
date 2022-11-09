from __future__ import annotations

import os
from datetime import datetime
from datetime import timedelta


def estimate_downvotes(upvotes: int, upvote_ratio: float) -> int:
    """
    Estimates the number of downvotes based on the number of upvotes and the upvote ratio
    """
    if upvote_ratio == 0.0:
        estimated_downvotes = 0.0
    else:
        # rearranged: upvote_ratio = upvotes / (upvotes + downvotes)
        estimated_downvotes = upvotes / upvote_ratio - upvotes
    return int(round(estimated_downvotes))


def get_date_parts_from_datetime(dt: datetime) -> tuple[str, str, str, str]:
    """
    Helper function to get different parts of a date as double-digit strings
    """
    year = f"{dt.year}"
    month = f"{dt.month:02d}"
    day = f"{dt.day:02d}"
    hour = f"{dt.hour:02d}"
    return year, month, day, hour


def get_s3_object_key(prefix: str, dt: datetime) -> str:
    """
    Assuming partitioning by year+month+day, using the hour as the object (file) name and saving in csv format:
    the method returns an S3 object key based on a prefix and a datetime object.
    """
    year, month, day, hour = get_date_parts_from_datetime(dt)
    partition_prefix = f"year={year}/month={month}/day={day}"
    object_name = f"hour={hour}.csv"

    if len(prefix) > 0:
        return f"{prefix}/{partition_prefix}/{object_name}"
    else:
        return f"{partition_prefix}/{object_name}"


def is_aws_env() -> bool:
    """
    True if running in AWS (e.g. lambda), otherwise false.
    """
    return os.environ.get("AWS_EXECUTION_ENV") is not None


# TEST!
def get_previous_s3_key(key: str) -> str:
    year_start = key.find("year=") + len("year=")
    year_end = year_start + 4

    month_start = key.find("month=") + len("month=")
    month_end = month_start + 2

    day_start = key.find("day=") + len("day=")
    day_end = day_start + 2

    hour_start = key.find("hour=") + len("hour=")
    hour_end = hour_start + 2

    dt = datetime(
        int(key[year_start:year_end]),
        int(key[month_start:month_end]),
        int(key[day_start:day_end]),
        int(key[hour_start:hour_end]),
    )

    previous_dt = dt + timedelta(hours=-1)

    previous_key = (
        key[0:year_start]
        + str(previous_dt.year)
        + key[year_end:month_start]
        + str(previous_dt.month).zfill(2)
        + key[month_end:day_start]
        + str(previous_dt.day).zfill(2)
        + key[day_end:hour_start]
        + str(previous_dt.hour).zfill(2)
        + key[hour_end:]
    )
    return previous_key
