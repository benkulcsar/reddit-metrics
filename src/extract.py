from __future__ import annotations

import logging
from datetime import datetime

import common.config as config
from common.models import RedditPost
from common.reddit_client import AbstractRedditClient
from common.reddit_client import RedditClient
from common.s3_client import AbstractS3Client
from common.s3_client import S3Client
from common.utils import estimate_downvotes
from common.utils import get_s3_object_key
from common.utils import is_aws_env


POST_FETCH_COUNT = 100

if is_aws_env():
    S3_EXTRACT_PREFIX = "reddit-posts"
else:
    S3_EXTRACT_PREFIX = "reddit-posts-local-run"


if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_new_submissions_from_reddit(
    reddit_client: AbstractRedditClient,
    subreddit_list: list[str],
) -> list[dict]:
    """
    Returns a list that includes the newest submissions from each subreddit in subreddit_list
    """

    submission_list = []

    logger.info(f"Fetching submissions from the following subreddits: {subreddit_list}")

    for subreddit_name in subreddit_list:
        logger.info(f"Fetching new submissions from: r/{subreddit_name}")
        subreddit_submission_list = reddit_client.fetch_new_submissions(
            subreddit_name=subreddit_name,
            fetch_count=POST_FETCH_COUNT,
        )
        submission_list.extend(subreddit_submission_list)
    return submission_list


def convert_submission_to_reddit_post(submission: dict) -> RedditPost:
    """
    Converts a dictionary representing a PRAW submission object to a RedditPost object
    """

    # Reddit API doesn't send the number of downvotes, so it is estimated.
    downvotes_estimated = estimate_downvotes(upvotes=submission["ups"], upvote_ratio=submission["upvote_ratio"])
    post_dt = datetime.utcfromtimestamp(submission.get("extracted_utc", 0.0))

    reddit_post = RedditPost(
        post_id=submission["id"],
        subreddit_name=submission.get("subreddit_display_name", ""),
        upvote_ratio=submission.get("upvote_ratio", 0.0),
        upvotes=submission.get("ups", 0),
        downvotes_original=submission.get("downs", 0),
        downvotes_estimated=downvotes_estimated,
        awards=submission.get("total_awards_received", 0),
        created_utc=submission.get("created_utc", 0.0),
        extracted_utc=submission.get("extracted_utc", 0.0),
        year=str(post_dt.year),
        month=str(post_dt.month).zfill(2),
        day=str(post_dt.day).zfill(2),
        hour=str(post_dt.hour).zfill(2),
    )
    return reddit_post


def upload_reddit_posts_to_s3(
    s3_client: AbstractS3Client,
    reddit_post_list: list[RedditPost],
    exec_datetime: datetime,
) -> None:
    """
    Builds the S3 prefix and object name and uploads a list of reddit posts to S3 using the s3_client.
    """
    s3_object_key = get_s3_object_key(prefix=S3_EXTRACT_PREFIX, dt=exec_datetime)
    s3_client.upload_dataclass_object_list_to_s3(
        dataclass_object_list=reddit_post_list,
        s3_bucket_name=config.get_s3_bucket_name(),
        s3_object_key=s3_object_key,
    )


def extract() -> None:
    logger.info("Starting extract task")

    exec_datetime = datetime.utcnow()
    logger.info(f"""Execution time (UTC): {exec_datetime.isoformat(sep=" ", timespec='seconds')}""")

    logger.info("Connecting to Reddit API")
    reddit_client = RedditClient(
        reddit_client_id=config.get_reddit_client_id(),
        reddit_client_secret=config.get_reddit_client_secret(),
        reddit_user_agent=config.get_reddit_user_agent(),
    )

    reddit_submission_list = fetch_new_submissions_from_reddit(
        reddit_client=reddit_client,
        subreddit_list=config.get_subreddit_list(),
    )

    logger.info("Converting Reddit submissions to RedditPost objects")
    reddit_post_list = [convert_submission_to_reddit_post(submission) for submission in reddit_submission_list]

    logger.info("Uploading RedditPost objects to S3")
    s3_client = S3Client()
    upload_reddit_posts_to_s3(
        s3_client=s3_client,
        reddit_post_list=reddit_post_list,
        exec_datetime=exec_datetime,
    )

    logger.info("Extract task done")


def lambda_handler(event, context):
    extract()


if __name__ == "__main__" and not is_aws_env():
    logger.info("Extract task run from shell")
    extract()
