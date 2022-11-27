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


def test_extract(reddit_submissions, reddit_posts):
    exec_datetime = datetime(2022, 10, 1, 2, 15)

    fake_reddit_client = FakeRedditClient(reddit_submissions)
    fake_s3_client = FakeS3Client()
    reddit_submission_list = fetch_new_submissions_from_reddit(
        reddit_client=fake_reddit_client,
        subreddit_list=["r/abc", "r/def"],
    )

    reddit_post_list = [convert_submission_to_reddit_post(submission) for submission in reddit_submission_list]

    upload_reddit_posts_to_s3(
        s3_client=fake_s3_client,
        reddit_post_list=reddit_post_list,
        exec_datetime=exec_datetime,
    )

    assert len(fake_s3_client.uploaded) == 1

    bucket_name = config.get_s3_bucket_name()
    object_key = get_s3_object_key(dt=exec_datetime, prefix=S3_EXTRACT_PREFIX)
    expected_key = f"{bucket_name}/{object_key}"
    uploaded_reddit_posts = fake_s3_client.uploaded.get(expected_key)

    assert sorted(uploaded_reddit_posts, key=lambda d: d.post_id) == sorted(reddit_posts, key=lambda d: d.post_id)
