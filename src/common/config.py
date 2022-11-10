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


def get_gcp_access_key_id():
    return os.environ["TF_VAR_GCP_ACCESS_KEY"]


def get_gcp_secret_access_key_id():
    return os.environ["TF_VAR_GCP_SECRET_ACCESS_KEY"]


def get_gcs_bucket_name():
    return os.environ["TF_VAR_REDDIT_S3_BUCKET"]


def get_subreddit_list():
    return sorted(
        [
            "canada",
            "europe",
            "nyc",
            "China",
            "sanfrancisco",
            "london",
            "LosAngeles",
            "glasgow",
            "Edinburgh",
            "chicago",
            "IndiaSpeaks",
            "HongKong",
            "ukraine",
            "germany",
            "spain",
            "greece",
            "ireland",
            "hungary",
            "Turkey",
            "thenetherlands",
            "Romania",
            "portugal",
            "india",
            "manchester",
            "Dublin",
            "paris",
            "Barcelona",
            "berlin",
            "Munich",
            "Madrid",
            "Amsterdam",
            "politics",
            "CryptoCurrency",
            "wallstreetbets",
            "Bitcoin",
            "atheism",
            "StockMarket",
            "ethtrader",
            "CryptoMoonShots",
            "conspiracy",
            "elonmusk",
            "southpark",
            "childfree",
            "ethereum",
            "python",
        ],
    )
