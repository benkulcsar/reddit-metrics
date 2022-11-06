from __future__ import annotations

import os
from datetime import datetime
from typing import Optional


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


def get_s3_object_name_and_partition_prefix(dt: Optional[datetime] = None) -> tuple[str, str]:
    """
    Assuming partitioning by year+month+day, using the hour as the object (file) name
    and saving in csv format: the method returns an S3 prefix for the partition and a name for the object (file).
    """
    if not dt:
        dt = datetime.utcnow()
    year, month, day, hour = get_date_parts_from_datetime(dt)
    partition_prefix = f"year={year}/month={month}/day={day}"
    object_name = f"hour={hour}.csv"
    return object_name, partition_prefix


def is_aws_env() -> bool:
    """
    True if running in AWS (e.g. lambda), otherwise false.
    """
    return os.environ.get("AWS_EXECUTION_ENV") is not None
