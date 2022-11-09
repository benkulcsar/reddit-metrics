from __future__ import annotations

from datetime import datetime

import pytest
from common.utils import estimate_downvotes
from common.utils import get_date_parts_from_datetime
from common.utils import get_previous_s3_key
from common.utils import get_s3_object_key


@pytest.mark.parametrize(
    "upvotes,upvote_ratio,expected_downvotes",
    [
        (3, 0.75, 1),
        (10, 1.0, 0),
        (0, 1.0, 0),
        (0, 0.0, 0),
        (1, 0.0, 0),
        (8, 0.7273, 3),
        (1, 0.1111, 8),
        (9999, 0.9999, 1),
    ],
)
def test_estimate_downvotes(upvotes, upvote_ratio, expected_downvotes):
    assert estimate_downvotes(upvotes, upvote_ratio) == expected_downvotes


@pytest.mark.parametrize(
    "datetime_input,expected_output",
    [
        (datetime(2022, 10, 1, 5), ("2022", "10", "01", "05")),
        (datetime(2022, 10, 1, 5, 59, 59, 99), ("2022", "10", "01", "05")),
        (datetime(2022, 10, 1, 6, 0, 0), ("2022", "10", "01", "06")),
        (datetime(1999, 1, 31, 22, 30), ("1999", "01", "31", "22")),
        (datetime(2023, 11, 11, 11), ("2023", "11", "11", "11")),
    ],
)
def test_get_date_parts_from_datetime(datetime_input, expected_output):
    assert get_date_parts_from_datetime(datetime_input) == expected_output


@pytest.mark.parametrize(
    "dt,prefix,expected_output",
    [
        (datetime(2022, 10, 1, 5), "random/prefix", "random/prefix/year=2022/month=10/day=01/hour=05.csv"),
        (datetime(2023, 1, 1, 23), "", "year=2023/month=01/day=01/hour=23.csv"),
        (datetime(2022, 11, 1, 12, 55, 44), "a/b/c/d", "a/b/c/d/year=2022/month=11/day=01/hour=12.csv"),
    ],
)
def test_get_s3_object_key(dt, prefix, expected_output):
    assert get_s3_object_key(dt=dt, prefix=prefix) == expected_output


@pytest.mark.parametrize(
    "key,expected_previous_key",
    [
        ("random/prefix/year=2022/month=10/day=01/hour=05.csv", "random/prefix/year=2022/month=10/day=01/hour=04.csv"),
        ("year=2022/month=10/day=01/hour=05.csv", "year=2022/month=10/day=01/hour=04.csv"),
        ("a/b/c/year=2022/month=10/day=01/hour=00.csv", "a/b/c/year=2022/month=09/day=30/hour=23.csv"),
        ("a/b/c/year=2022/month=01/day=01/hour=00.csv", "a/b/c/year=2021/month=12/day=31/hour=23.csv"),
    ],
)
def test_get_previous_s3_key(key, expected_previous_key):
    assert get_previous_s3_key(key) == expected_previous_key
