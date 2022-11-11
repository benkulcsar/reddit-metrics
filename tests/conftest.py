from __future__ import annotations

import pandas as pd
import pytest
from common.models import RedditMetricSet
from common.models import RedditPost


@pytest.fixture
def reddit_submissions():
    return [
        {
            "id": "x",
            "subreddit_display_name": "r/abc",
            "upvote_ratio": 0.9,
            "ups": 90,
            "downs": 0,
            "total_awards_received": 0,
            "created_utc": 1.0,
            "extracted_utc": 1667920961.127697,
        },
        {
            "id": "y",
            "subreddit_display_name": "r/abc",
            "upvote_ratio": 0.3,
            "ups": 30,
            "downs": 0,
            "total_awards_received": 0,
            "created_utc": 1.0,
            "extracted_utc": 1667920961.127697,
        },
        {
            "id": "z",
            "subreddit_display_name": "r/def",
            "upvote_ratio": 0.5,
            "ups": 5,
            "downs": 0,
            "total_awards_received": 0,
            "created_utc": 1.0,
            "extracted_utc": 1667920961.127697,
        },
    ]


@pytest.fixture
def reddit_posts():
    return [
        RedditPost(
            post_id="x",
            subreddit_name="r/abc",
            upvote_ratio=0.9,
            upvotes=90,
            downvotes_original=0,
            downvotes_estimated=10,
            awards=0,
            created_utc=1.0,
            extracted_utc=1667920961.127697,
            partition_year="2022",
            partition_month="11",
            partition_day="08",
            partition_hour="15",
        ),
        RedditPost(
            post_id="y",
            subreddit_name="r/abc",
            upvote_ratio=0.3,
            upvotes=30,
            downvotes_original=0,
            downvotes_estimated=70,
            awards=0,
            created_utc=1.0,
            extracted_utc=1667920961.127697,
            partition_year="2022",
            partition_month="11",
            partition_day="08",
            partition_hour="15",
        ),
        RedditPost(
            post_id="z",
            subreddit_name="r/def",
            upvote_ratio=0.5,
            upvotes=5,
            downvotes_original=0,
            downvotes_estimated=5,
            awards=0,
            created_utc=1.0,
            extracted_utc=1667920961.127697,
            partition_year="2022",
            partition_month="11",
            partition_day="08",
            partition_hour="15",
        ),
    ]


@pytest.fixture
def previous_reddit_posts(reddit_posts):
    prev_rps = reddit_posts
    for i in range(len(prev_rps)):
        prev_rps[i].hour = 14

    prev_rps[0].upvotes -= 5
    prev_rps[0].downvotes_estimated -= 5

    prev_rps[1].upvotes -= 15
    prev_rps[1].downvotes_estimated -= 0

    prev_rps[2].upvotes -= 1
    prev_rps[2].downvotes_estimated -= 1

    return prev_rps


@pytest.fixture
def metric_set_list():
    return [
        RedditMetricSet(
            subreddit_name="r/abc",
            upvotes=20,
            downvotes=5,
            upvote_ratio=0.8,
            transformed_utc=1.0,
            partition_year="2022",
            partition_month="11",
            partition_day="08",
            partition_hour="15",
        ),
        RedditMetricSet(
            subreddit_name="r/def",
            upvotes=1,
            downvotes=1,
            upvote_ratio=0.5,
            transformed_utc=1.0,
            partition_year="2022",
            partition_month="11",
            partition_day="08",
            partition_hour="15",
        ),
    ]


@pytest.fixture
def reddit_posts_df(reddit_posts):
    return pd.DataFrame([post.__dict__ for post in reddit_posts])


@pytest.fixture
def previous_reddit_posts_df(previous_reddit_posts):
    return pd.DataFrame([post.__dict__ for post in previous_reddit_posts])


@pytest.fixture
def metric_sets_df(metric_set_list):
    columns = [
        "subreddit_name",
        "partition_year",
        "partition_month",
        "partition_day",
        "partition_hour",
        "up_delta",
        "down_delta",
        "upvote_ratio",
    ]
    data = [
        ["r/abc", "2022", "11", "08", "15", 20, 5, 0.8],
        ["r/def", "2022", "11", "08", "15", 1, 1, 0.5],
    ]
    return pd.DataFrame(data=data, columns=columns)
