from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

import boto3
from dataclass_csv import DataclassReader
from dataclass_csv import DataclassWriter

if TYPE_CHECKING:
    from models import BaseDataclass


class AbstractS3Client(ABC):
    @abstractmethod
    def upload_dataclass_object_list_to_s3(
        self,
        dataclass_object_list: list[BaseDataclass],
        s3_bucket_name: str,
        s3_object_key: str,
    ) -> None:
        """
        Saves a list of dataclass objects in a csv file in /tmp/ and uploads the file to s3.
        """
        pass

    @abstractmethod
    def download_from_s3_to_dataclass_object_list(
        self,
        dataclass_type: type[BaseDataclass],
        s3_bucket_name: str,
        s3_object_key: str,
    ) -> list[BaseDataclass]:
        """
        Downloads a csv file from S3, saves it in /tmp/ and converts it into a list of dataclass objects
        """
        pass

    @abstractmethod
    def transfer_object_from_s3_to_gcs(
        self,
        s3_bucket_name: str,
        s3_object_key: str,
        gcs_bucket_name: str,
        gcs_object_key: str,
        gcp_access_key: str,
        gcp_secret_access_key: str,
    ) -> None:
        """Transfer an object from an S3 bucket to Google Cloud Storage bucket"""
        pass


class S3Client(AbstractS3Client):
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def upload_dataclass_object_list_to_s3(
        self,
        dataclass_object_list: list[BaseDataclass],
        s3_bucket_name: str,
        s3_object_key: str,
    ) -> None:

        file_name_with_path = "/tmp/to_s3.csv"
        with open(file_name_with_path, "w") as file:
            writer = DataclassWriter(file, dataclass_object_list, type(dataclass_object_list[0]))
            writer.write()

        self.s3_client.upload_file(file_name_with_path, s3_bucket_name, s3_object_key)

    def download_from_s3_to_dataclass_object_list(
        self,
        dataclass_type: type[BaseDataclass],
        s3_bucket_name: str,
        s3_object_key: str,
    ) -> list[BaseDataclass]:

        file_name_with_path = "/tmp/from_s3.csv"
        self.s3_client.download_file(s3_bucket_name, s3_object_key, file_name_with_path)

        with open(file_name_with_path, "r") as file:
            dataclass_list = list(DataclassReader(file, dataclass_type))

        return dataclass_list

    def transfer_object_from_s3_to_gcs(
        self,
        s3_bucket_name: str,
        s3_object_key: str,
        gcs_bucket_name: str,
        gcs_object_key: str,
        gcp_access_key: str,
        gcp_secret_access_key: str,
    ) -> None:
        gcs_client = boto3.client(
            "s3",
            region_name="auto",
            endpoint_url="https://storage.googleapis.com",
            aws_access_key_id=gcp_access_key,
            aws_secret_access_key=gcp_secret_access_key,
        )

        object_to_transfer = self.s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
        gcs_client.upload_fileobj(
            object_to_transfer["Body"],
            gcs_bucket_name,
            gcs_object_key,
        )


class FakeS3Client(ABC):
    def __init__(self):
        self.uploaded = {}  # type: dict[str, list[BaseDataclass]]
        self.transferred_to_gcs = {}  # type: dict[str, list[BaseDataclass]]

    def upload_dataclass_object_list_to_s3(
        self,
        dataclass_object_list: list[BaseDataclass],
        s3_bucket_name: str,
        s3_object_key: str,
    ) -> None:
        self.uploaded[f"{s3_bucket_name}/{s3_object_key}"] = dataclass_object_list

    def download_from_s3_to_dataclass_object_list(
        self,
        dataclass_type: type[BaseDataclass],
        s3_bucket_name: str,
        s3_object_key: str,
    ) -> list[BaseDataclass]:
        return self.uploaded[f"{s3_bucket_name}/{s3_object_key}"]

    def transfer_object_from_s3_to_gcs(
        self,
        s3_bucket_name: str,
        s3_object_key: str,
        gcs_bucket_name: str,
        gcs_object_key: str,
        gcp_access_key: str,
        gcp_secret_access_key: str,
    ) -> None:
        """Transfer an object from an S3 bucket to Google Cloud Storage bucket"""
        self.transferred_to_gcs[f"{gcs_bucket_name}/{gcs_object_key}"] = self.uploaded[
            f"{s3_bucket_name}/{s3_object_key}"
        ]
