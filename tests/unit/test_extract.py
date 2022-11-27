from __future__ import annotations

from datetime import datetime

import common.config as config
from common.reddit_client import FakeRedditClient
from common.s3_client import FakeS3Client
from common.utils import get_s3_object_key
from extract import convert_submission_to_reddit_post
from extract import fetch_new_submissions_from_reddit
from extract import S3_EXTRACT_PREFIX
from extract import upload_reddit_posts_to_s3


def test_fetch_new_posts_from_reddit(reddit_submissions):
    fake_reddit_client = FakeRedditClient(reddit_submissions)
    fetch_subs = fetch_new_submissions_from_reddit(reddit_client=fake_reddit_client, subreddit_list=["r/abc", "r/def"])
    fetch_none = fetch_new_submissions_from_reddit(reddit_client=fake_reddit_client, subreddit_list=["r/xyz"])
    assert sorted(fetch_subs, key=lambda d: d.get("id")) == sorted(reddit_submissions, key=lambda d: d.get("id"))
    assert fetch_none == []


def test_convert_submission_to_reddit_post(reddit_submissions, reddit_posts):
    for reddit_submission, reddit_post in zip(reddit_submissions, reddit_posts):
        converted_reddit_post = convert_submission_to_reddit_post(reddit_submission)
        assert converted_reddit_post == reddit_post


def test_upload_reddit_posts_to_s3(reddit_posts):
    exec_datetime = datetime(2022, 11, 1, 14, 15)

    fake_s3_client = FakeS3Client()
    upload_reddit_posts_to_s3(
        s3_client=fake_s3_client,
        reddit_post_list=reddit_posts,
        exec_datetime=exec_datetime,
    )
    assert len(fake_s3_client.uploaded) == 1

    bucket_name = config.get_s3_bucket_name()
    object_key = get_s3_object_key(dt=exec_datetime, prefix=S3_EXTRACT_PREFIX)
    expected_key = f"{bucket_name}/{object_key}"

    assert fake_s3_client.uploaded.get(expected_key) == reddit_posts
