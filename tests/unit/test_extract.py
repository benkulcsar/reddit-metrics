from __future__ import annotations

from datetime import datetime

import config as config
from clients.reddit_client import FakeRedditClient
from clients.s3_client import FakeS3Client
from extract import convert_submission_to_reddit_post
from extract import fetch_new_submissions_from_reddit
from extract import S3_EXTRACT_PREFIX
from extract import upload_reddit_posts_to_s3
from utils import get_s3_object_name_and_partition_prefix


def test_fetch_new_posts_from_reddit(reddit_submission):
    fake_reddit_client = FakeRedditClient([reddit_submission])
    fetch_one = fetch_new_submissions_from_reddit(reddit_client=fake_reddit_client, subreddit_list=["r/def"])
    fetch_none = fetch_new_submissions_from_reddit(reddit_client=fake_reddit_client, subreddit_list=["r/xyz"])
    assert fetch_one == [reddit_submission]
    assert fetch_none == []


def test_convert_submission_to_reddit_post(reddit_submission, reddit_post):
    converted_reddit_post = convert_submission_to_reddit_post(reddit_submission)
    assert converted_reddit_post == reddit_post


def test_upload_reddit_posts_to_s3(reddit_post):
    exec_datetime = datetime(2022, 11, 1, 14, 15)

    fake_s3_client = FakeS3Client()
    upload_reddit_posts_to_s3(
        s3_client=fake_s3_client,
        reddit_post_list=[reddit_post],
        exec_datetime=exec_datetime,
    )
    assert len(fake_s3_client.uploaded) == 1

    bucket_name = config.get_s3_bucket_name()
    name, prefix = get_s3_object_name_and_partition_prefix(dt=exec_datetime)
    expected_key = f"{bucket_name}/{S3_EXTRACT_PREFIX}/{prefix}/{name}"

    assert fake_s3_client.uploaded.get(expected_key) == [reddit_post]
