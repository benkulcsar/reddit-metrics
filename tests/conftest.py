from __future__ import annotations

import pytest
from models import RedditPost


@pytest.fixture
def reddit_submission():
    return {
        "id": "abc",
        "subreddit_display_name": "r/def",
        "upvote_ratio": 0.75,
        "ups": 3,
        "downs": 0,
        "total_awards_received": 0,
        "created_utc": 1.0,
        "extracted_utc": 1.0,
    }


@pytest.fixture
def reddit_post():
    return RedditPost(
        post_id="abc",
        subreddit_name="r/def",
        upvote_ratio=0.75,
        upvotes=3,
        downvotes_original=0,
        downvotes_estimated=1,
        awards=0,
        created_utc=1.0,
        extracted_utc=1.0,
    )
