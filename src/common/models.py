"""
The dataclasses are defined to document the schemas in a way that can be understood by both humans and machines.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BaseDataclass:
    partition_year: str
    partition_month: str
    partition_day: str
    partition_hour: str


@dataclass
class RedditPost(BaseDataclass):
    post_id: str
    subreddit_name: str
    upvote_ratio: float
    upvotes: int
    downvotes_original: int
    downvotes_estimated: int
    awards: int
    created_utc: float
    extracted_utc: float
    comment_count: int = 0


@dataclass
class RedditMetricSet(BaseDataclass):
    subreddit_name: str
    upvotes: int
    downvotes: int
    upvote_ratio: float
    posts: int
    comments: int
    transformed_utc: float
