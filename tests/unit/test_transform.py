from __future__ import annotations

import pandas as pd
from common.models import RedditMetricSet
from common.s3_client import FakeS3Client
from transform import calculate_metric_sets
from transform import convert_df_to_metric_set_list
from transform import get_reddit_posts_dataframe_from_s3
from transform import S3_EXTRACT_PREFIX
from transform import S3_TRANSFORM_PREFIX
from transform import upload_metric_set_list_to_s3


def test_get_reddit_posts_dataframe_from_s3(reddit_posts, reddit_posts_df):
    fake_s3_client = FakeS3Client()
    fake_s3_client.upload_dataclass_object_list_to_s3(
        dataclass_object_list=reddit_posts,
        s3_bucket_name="test",
        s3_object_key="test",
    )

    test_reddit_posts_df = get_reddit_posts_dataframe_from_s3(s3_client=fake_s3_client, bucket="test", key="test")

    pd.testing.assert_frame_equal(test_reddit_posts_df, reddit_posts_df)


def test_calculate_metric_sets(reddit_posts_df, previous_reddit_posts_df, metric_sets_df):

    calculated_metrics = calculate_metric_sets(current_df=reddit_posts_df, previous_df=previous_reddit_posts_df)
    pd.testing.assert_frame_equal(calculated_metrics.sort_index(axis=1), metric_sets_df.sort_index(axis=1))


def test_convert_df_to_metric_set_list(metric_sets_df, metric_set_list):
    test_metric_set = convert_df_to_metric_set_list(df=metric_sets_df, transformed_timestamp=1.0)
    test_metric_set == metric_set_list


def test_upload_metric_set_list_to_s3(metric_set_list):
    fake_s3_client = FakeS3Client()

    upload_metric_set_list_to_s3(
        s3_client=fake_s3_client,
        metric_set_list=metric_set_list,
        bucket="test",
        posts_object_key=S3_EXTRACT_PREFIX,
    )

    assert metric_set_list == fake_s3_client.download_from_s3_to_dataclass_object_list(
        dataclass_type=RedditMetricSet,
        s3_bucket_name="test",
        s3_object_key=S3_TRANSFORM_PREFIX,
    )
