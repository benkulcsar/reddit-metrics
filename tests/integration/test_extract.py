from __future__ import annotations

from datetime import datetime

import config as config
from clients.reddit_client import FakeRedditClient
from clients.s3_client import FakeS3Client
from extract import convert_submission_to_reddit_post
from extract import fetch_new_submissions_from_reddit
from extract import S3_DATA_PREFIX
from extract import upload_reddit_posts_to_s3
from utils import get_s3_object_name_and_partition_prefix


def test_extract(reddit_submission, reddit_post):
    exec_datetime = datetime(2022, 10, 1, 2, 15)

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
        exec_datetime=exec_datetime,
    )

    assert len(fake_s3_client.uploaded) == 1

    bucket_name = config.get_s3_bucket_name()
    name, prefix = get_s3_object_name_and_partition_prefix(dt=exec_datetime)
    expected_key = f"{bucket_name}/{S3_DATA_PREFIX}/{prefix}/{name}"

    assert fake_s3_client.uploaded.get(expected_key) == [reddit_post]
