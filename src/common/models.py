from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BaseDataclass:
    year: str
    month: str
    day: str
    hour: str


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


@dataclass
class RedditMetricSet(BaseDataclass):
    subreddit_name: str
    upvotes: int
    downvotes: int
    upvote_ratio: float
    transformed_utc: float
