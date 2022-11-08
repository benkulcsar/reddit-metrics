from __future__ import annotations

import logging
import urllib
from datetime import datetime

import pandas as pd
from clients.s3_client import S3Client
from models import RedditPost
from utils import get_previous_s3_key
from utils import is_aws_env

TMP_PREFIX = "reddit-posts/year=2022/month=11/day=08"
TMP_CURRENT_RAW = "hour=08.csv"
TMP_PREVIOUS_RAW = "hour=07.csv"
TMP_CURRENT_TARGET = "s3://benkl-reddit/reddit-stats-local-run/year=2022/month=11/day=08/hour=07.csv"

if is_aws_env():
    S3_EXTRACT_PREFIX = "reddit-posts"
    S3_TRANSFORM_PREFIX = "reddit-stats"
else:
    S3_EXTRACT_PREFIX = "reddit-posts"
    S3_TRANSFORM_PREFIX = "reddit-stats-local-run"


if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def transform(bucket, key) -> None:
    logger.info("Starting transform task")

    exec_datetime = datetime.utcnow()
    logger.info(f"""Execution time (UTC): {exec_datetime.isoformat(sep=" ", timespec='seconds')}""")

    previous_key = get_previous_s3_key(key)

    s3_client = S3Client()

    reddit_posts = s3_client.download_from_s3_to_dataclass_object_list(
        dataclass_type=RedditPost,
        s3_bucket_name=bucket,
        s3_object_key=key,
    )
    prev_reddit_posts = s3_client.download_from_s3_to_dataclass_object_list(
        dataclass_type=RedditPost,
        s3_bucket_name=bucket,
        s3_object_key=previous_key,
    )

    cols_to_keep = ["post_id", "subreddit_name", "upvotes", "downvotes_estimated"]

    current_df = pd.DataFrame([post.__dict__ for post in reddit_posts])
    previous_df = pd.DataFrame([post.__dict__ for post in prev_reddit_posts])

    dfm = current_df[cols_to_keep].merge(
        previous_df[cols_to_keep],
        on=["post_id", "subreddit_name"],
        how="left",
        suffixes=("_new", "_old"),
    )
    dfm = dfm.fillna(0)
    dfm["up_delta"] = dfm.upvotes_new - dfm.upvotes_old
    dfm["down_delta"] = dfm.downvotes_estimated_new - dfm.downvotes_estimated_old
    dfm["up_delta"] = dfm["up_delta"].apply(lambda x: max(x, 0))
    dfm["down_delta"] = dfm["down_delta"].apply(lambda x: max(x, 0))

    dfm = dfm.groupby("subreddit_name")[["up_delta", "down_delta"]].agg("sum")
    dfm["upvr"] = dfm.up_delta / (dfm.up_delta + dfm.down_delta)
    dfm["hour"] = "08"

    dfm.to_csv("agg_3.csv")

    logger.info("Transform task done")


def lambda_handler(context, event):
    if event.get("Records"):
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    elif event.get("Extracts"):
        bucket = event["Extracts"][0]["bucket"]
        key = event["Extracts"][0]["key"]
    transform(bucket, key)


if __name__ == "__main__" and not is_aws_env():
    logger.info("Transform task run from shell")
    transform("benkl-reddit", "reddit-posts/year=2022/month=11/day=08/hour=07.csv")
