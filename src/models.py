from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BaseDataclass:
    pass


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
