from __future__ import annotations

import os
import boto3


def get_reddit_client_id():
    return os.environ["TF_VAR_REDDIT_CLIENT_ID"]


def get_reddit_client_secret():
    return os.environ["TF_VAR_REDDIT_CLIENT_SECRET"]


def get_s3_bucket_name():
    return os.environ["TF_VAR_REDDIT_S3_BUCKET"]


def get_reddit_user_agent():
    return "Icedruid/0.0.1"


def get_gcp_access_key_id():
    return os.environ["TF_VAR_GCP_ACCESS_KEY"]


def get_gcp_secret_access_key_id():
    return os.environ["TF_VAR_GCP_SECRET_ACCESS_KEY"]


def get_gcs_bucket_name():
    return os.environ["TF_VAR_REDDIT_S3_BUCKET"]


def get_extract_prefix():
    return "reddit-posts"


def get_transform_prefix():
    return "reddit-metrics"


def get_post_fetch_count():
    return 100


def get_subreddit_list():
    ssm = boto3.client("ssm")
    parameter = ssm.get_parameter(Name="SubredditList", WithDecryption=True)
    return sorted(parameter["Parameter"]["Value"].split(","))
