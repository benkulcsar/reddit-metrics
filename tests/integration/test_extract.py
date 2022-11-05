from __future__ import annotations

from clients.reddit_client import FakeRedditClient
from clients.s3_client import FakeS3Client
from extract import convert_submission_to_reddit_post
from extract import fetch_new_submissions_from_reddit
from extract import upload_reddit_posts_to_s3


def test_extract(reddit_submission, reddit_post):
    fake_reddit_client = FakeRedditClient([reddit_submission])
    fake_s3_client = FakeS3Client()
    reddit_submission_list = fetch_new_submissions_from_reddit(
        reddit_client=fake_reddit_client,
        subreddit_list=["r/def"],
    )

    reddit_post_list = [convert_submission_to_reddit_post(submission) for submission in reddit_submission_list]

    upload_reddit_posts_to_s3(
        s3_client=fake_s3_client,
        reddit_post_list=reddit_post_list,
    )

    assert len(fake_s3_client.uploaded) == 1
    key = list(fake_s3_client.uploaded.keys())[0]
    assert fake_s3_client.uploaded.get(key) == [reddit_post]
