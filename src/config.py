from __future__ import annotations

import os


def get_reddit_client_id():
    return os.environ["TF_VAR_REDDIT_CLIENT_ID"]


def get_reddit_client_secret():
    return os.environ["TF_VAR_REDDIT_CLIENT_SECRET"]


def get_s3_bucket_name():
    return os.environ["TF_VAR_REDDIT_S3_BUCKET"]


def get_reddit_user_agent():
    return "Icedruid/0.0.1"


def get_subreddit_list():
    return sorted(
        [
            "python",
            "java",
            "dataisbeautiful",
            "dataengineering",
            "cscareerquestions",
            "cscareerquestionseu",
            "analytics",
            "aws",
            "linux",
            "ubuntu",
            "programming",
            "learnprogramming",
            "learnpython",
            "linuxquestions",
        ],
    )
