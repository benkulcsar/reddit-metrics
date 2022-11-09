from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from datetime import datetime

from praw import Reddit


class AbstractRedditClient(ABC):
    """
    Wrapper class for the PRAW client to access the Reddit API.
    """

    @abstractmethod
    def fetch_new_submissions(self, subreddit_name: str, fetch_count: int = 100) -> list[dict]:
        """
        Fetches the most recent N submissions (i.e. posts) from a subreddit.
        N (fetch_count) is 100 by default which is the maximum allowed by the Reddit API.
        """
        pass


class RedditClient(AbstractRedditClient):
    def __init__(
        self,
        reddit_client_id: str,
        reddit_client_secret: str,
        reddit_user_agent: str,
    ):
        self.reddit = Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent,
        )

    def fetch_new_submissions(self, subreddit_name: str, fetch_count: int = 100) -> list[dict]:
        fetch_count = min(fetch_count, 100)
        fetch_count = max(fetch_count, 1)

        submission_generator = self.reddit.subreddit(subreddit_name).new(limit=fetch_count)

        return [
            {
                "id": submission.id,
                "subreddit_display_name": submission.subreddit.display_name,
                "upvote_ratio": submission.upvote_ratio,
                "ups": submission.ups,
                "downs": submission.downs,
                "total_awards_received": submission.total_awards_received,
                "created_utc": submission.created_utc,
                "extracted_utc": datetime.utcnow().timestamp(),
            }
            for submission in submission_generator
        ]


class FakeRedditClient(ABC):
    def __init__(self, test_submissions: list[dict]):
        self.test_submissions = test_submissions

    def fetch_new_submissions(self, subreddit_name: str, fetch_count: int = 100) -> list[dict]:
        filtered_submissions = [
            submission
            for submission in self.test_submissions
            if submission.get("subreddit_display_name") == subreddit_name
        ]
        sorted_filtered_submissions = sorted(filtered_submissions, key=lambda x: x.get("created_utc"))  # type: ignore
        return sorted_filtered_submissions[:fetch_count]
