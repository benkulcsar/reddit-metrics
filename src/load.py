from __future__ import annotations

import logging
import urllib

import common.config as config
from common.s3_client import S3Client
from common.utils import is_aws_env

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load(s3_bucket, s3_key) -> None:
    logger.info("Starting load task")

    gcs_bucket = config.get_gcs_bucket_name()
    gcs_key = s3_key

    s3_client = S3Client()

    logger.info(f"Transferring from S3: {s3_bucket}/{s3_key}")
    logger.info(f"Transferring to GCS: {gcs_bucket}/{gcs_key}")

    s3_client.transfer_object_from_s3_to_gcs(
        s3_bucket_name=s3_bucket,
        s3_object_key=s3_key,
        gcs_bucket_name=gcs_bucket,
        gcs_object_key=gcs_key,
        gcp_access_key=config.get_gcp_access_key_id(),
        gcp_secret_access_key=config.get_gcp_secret_access_key_id(),
    )

    logger.info("Load task done")


def lambda_handler(event, context):
    if event.get("Records"):
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
        load(s3_bucket=bucket, s3_key=key)

    # This enables running multiple load tasks by triggering the lambda manually with a custom test event:
    # {"Backfill":["bucket":"bucket_name","key":"obj_key1","bucket":"bucket_name","key":"obj_key2"]}
    elif event.get("Backfill"):
        for backfill in event["Backfill"]:
            load(s3_bucket=backfill.get("bucket"), s3_key=backfill.get("key"))


if __name__ == "__main__" and not is_aws_env():
    logger.info("Transform task run from shell")

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", help="Bucket of the transfer object.")
    parser.add_argument("-k", "--key", help="Key of the transfer object.")
    args = vars(parser.parse_args())

    load(s3_bucket=args.get("bucket"), s3_key=args.get("key"))
