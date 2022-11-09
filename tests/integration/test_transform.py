from __future__ import annotations

from common.models import RedditMetricSet
from common.s3_client import FakeS3Client
from transform import calculate_metric_sets
from transform import convert_df_to_metric_set_list
from transform import get_reddit_posts_dataframe_from_s3
from transform import S3_EXTRACT_PREFIX
from transform import S3_TRANSFORM_PREFIX
from transform import upload_metric_set_list_to_s3


def test_transform(reddit_posts, previous_reddit_posts):

    bucket = "test"
    key = f"{S3_EXTRACT_PREFIX}/test"
    prev_key = f"{S3_EXTRACT_PREFIX}/test_previous"
    transformed_key = f"{S3_TRANSFORM_PREFIX}/test"

    fake_s3_client = FakeS3Client()
    fake_s3_client.upload_dataclass_object_list_to_s3(
        dataclass_object_list=reddit_posts,
        s3_bucket_name=bucket,
        s3_object_key=key,
    )

    fake_s3_client.upload_dataclass_object_list_to_s3(
        dataclass_object_list=reddit_posts,
        s3_bucket_name=bucket,
        s3_object_key=prev_key,
    )

    reddit_posts_df = get_reddit_posts_dataframe_from_s3(s3_client=fake_s3_client, bucket=bucket, key=key)
    prev_reddit_posts_df = get_reddit_posts_dataframe_from_s3(s3_client=fake_s3_client, bucket=bucket, key=prev_key)

    metric_sets_df = calculate_metric_sets(current_df=reddit_posts_df, previous_df=prev_reddit_posts_df)
    metric_set_list = convert_df_to_metric_set_list(
        df=metric_sets_df,
        transformed_timestamp=1.0,
    )

    upload_metric_set_list_to_s3(
        s3_client=fake_s3_client,
        metric_set_list=metric_set_list,
        bucket=bucket,
        posts_object_key=key,
    )

    assert metric_set_list == fake_s3_client.download_from_s3_to_dataclass_object_list(
        dataclass_type=RedditMetricSet,
        s3_bucket_name=bucket,
        s3_object_key=transformed_key,
    )
