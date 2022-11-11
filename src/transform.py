from __future__ import annotations

import logging
import urllib
from datetime import datetime

import common.config as config
import pandas as pd
from common.models import RedditMetricSet
from common.models import RedditPost
from common.s3_client import AbstractS3Client
from common.s3_client import S3Client
from common.utils import get_previous_s3_key
from common.utils import is_aws_env


S3_EXTRACT_PREFIX = config.get_extract_prefix()
S3_TRANSFORM_PREFIX = config.get_transform_prefix()


if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_reddit_posts_dataframe_from_s3(s3_client: AbstractS3Client, bucket: str, key: str) -> pd.DataFrame:
    """
    Returns previously extracted post list from S3 as a Pandas dataframe
    """
    reddit_posts = s3_client.download_from_s3_to_dataclass_object_list(
        dataclass_type=RedditPost,
        s3_bucket_name=bucket,
        s3_object_key=key,
    )

    return pd.DataFrame([post.__dict__ for post in reddit_posts])


def calculate_metric_sets(current_df: pd.DataFrame, previous_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the upvotes and downvotes since the previous snapshot, groups them by subreddit
    Returns a dataframe with metrics aggregates at subreddit level
    """

    cols_to_keep_current = [
        "post_id",
        "subreddit_name",
        "upvotes",
        "downvotes_estimated",
        "partition_year",
        "partition_month",
        "partition_day",
        "partition_hour",
    ]
    cols_to_keep_previous = ["post_id", "upvotes", "downvotes_estimated"]

    joined_df = current_df[cols_to_keep_current].merge(
        previous_df[cols_to_keep_previous],
        on=["post_id"],
        how="left",
        suffixes=("_new", "_old"),
    )
    joined_df = joined_df.fillna(0)

    joined_df["up_delta"] = joined_df.upvotes_new - joined_df.upvotes_old
    joined_df["down_delta"] = joined_df.downvotes_estimated_new - joined_df.downvotes_estimated_old
    joined_df["up_delta"] = joined_df["up_delta"].apply(lambda x: max(x, 0))
    joined_df["down_delta"] = joined_df["down_delta"].apply(lambda x: max(x, 0))

    grouped_df = joined_df.groupby(
        [
            "subreddit_name",
            "partition_year",
            "partition_month",
            "partition_day",
            "partition_hour",
        ],
    )[["up_delta", "down_delta"]].agg(
        "sum",
    )
    grouped_df["upvote_ratio"] = grouped_df.up_delta / (grouped_df.up_delta + grouped_df.down_delta)

    return grouped_df.reset_index()


def convert_df_to_metric_set_list(df: pd.DataFrame, transformed_timestamp: float) -> RedditMetricSet:
    """
    Converts a Pandas dataframe representing metric sets into a list of RedditMetricSet objects
    """
    metric_set_list = []
    for _, row in df.iterrows():
        reddit_metric_set = RedditMetricSet(
            subreddit_name=row.subreddit_name,
            upvotes=int(row.up_delta),
            downvotes=int(row.down_delta),
            upvote_ratio=round(row.upvote_ratio, 4),
            partition_year=row.partition_year,
            partition_month=row.partition_month,
            partition_day=row.partition_day,
            partition_hour=row.partition_hour,
            transformed_utc=transformed_timestamp,
        )
        metric_set_list.append(reddit_metric_set)
    return metric_set_list


def upload_metric_set_list_to_s3(
    s3_client: AbstractS3Client,
    metric_set_list: list[RedditMetricSet],
    bucket: str,
    posts_object_key: str,
) -> None:
    """
    Uploads a list of RedditMetricSet objects to S3
    """

    if S3_EXTRACT_PREFIX not in posts_object_key:
        transformed_object_key = f"temp_transformed/{posts_object_key}"
    else:
        transformed_object_key = posts_object_key.replace(S3_EXTRACT_PREFIX, S3_TRANSFORM_PREFIX)

    s3_client.upload_dataclass_object_list_to_s3(
        dataclass_object_list=metric_set_list,
        s3_bucket_name=bucket,
        s3_object_key=transformed_object_key,
    )


def transform(bucket, key) -> None:
    logger.info("Starting transform task")

    exec_datetime = datetime.utcnow()
    logger.info(f"""Execution time (UTC): {exec_datetime.isoformat(sep=" ", timespec='seconds')}""")

    s3_client = S3Client()
    prev_key = get_previous_s3_key(key)

    logger.info(f"Fetching posts from S3: {bucket}/{key}")
    reddit_posts_df = get_reddit_posts_dataframe_from_s3(s3_client=s3_client, bucket=bucket, key=key)
    logger.info(f"Fetching previous posts from S3: {bucket}/{prev_key}")
    prev_reddit_posts_df = get_reddit_posts_dataframe_from_s3(s3_client=s3_client, bucket=bucket, key=prev_key)

    logger.info("Transforming and aggregating")
    metric_sets_df = calculate_metric_sets(current_df=reddit_posts_df, previous_df=prev_reddit_posts_df)
    metric_set_list = convert_df_to_metric_set_list(
        df=metric_sets_df,
        transformed_timestamp=round(exec_datetime.timestamp(), 0),
    )

    logger.info("Uploading transformed and aggregated data to S3")
    upload_metric_set_list_to_s3(
        s3_client=s3_client,
        metric_set_list=metric_set_list,
        bucket=bucket,
        posts_object_key=key,
    )

    logger.info("Transform task done")


def lambda_handler(event, context):
    if event.get("Records"):
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
        transform(bucket, key)

    # This enables running multiple load tasks by triggering the lambda manually with a custom test event:
    # {"Backfill":["bucket":"bucket_name","key":"obj_key1","bucket":"bucket_name","key":"obj_key2"]}
    elif event.get("Backfill"):
        for backfill in event["Backfill"]:
            transform(s3_bucket=backfill.get("bucket"), s3_key=backfill.get("key"))


if __name__ == "__main__" and not is_aws_env():
    logger.info("Transform task run from shell")

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", help="Bucket of the extract object.")
    parser.add_argument("-k", "--key", help="Key of the extract object.")
    args = vars(parser.parse_args())

    transform(bucket=args.get("bucket"), key=args.get("key"))
