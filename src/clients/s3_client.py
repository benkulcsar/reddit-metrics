from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

import boto3
from dataclass_csv import DataclassWriter

if TYPE_CHECKING:
    from models import BaseDataclass


class AbstractS3Client(ABC):
    @abstractmethod
    def upload_dataclass_object_list_to_s3(
        self,
        dataclass_object_list: list[BaseDataclass],
        s3_bucket_name: str,
        s3_prefix: str,
        s3_object_name: str,
    ) -> None:
        """
        Saves a list of dataclass objects in a csv file in /tmp/ and uploads the file to s3.
        """
        pass


class S3Client(AbstractS3Client):
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def upload_dataclass_object_list_to_s3(
        self,
        dataclass_object_list: list[BaseDataclass],
        s3_bucket_name: str,
        s3_prefix: str,
        s3_object_name: str,
    ) -> None:

        file_name_with_path = "/tmp/" + s3_object_name
        with open(file_name_with_path, "w") as file:
            writer = DataclassWriter(file, dataclass_object_list, type(dataclass_object_list[0]))
            writer.write()

        s3_object_name_with_prefix = f"{s3_prefix}/{s3_object_name}"
        self.s3_client.upload_file(file_name_with_path, s3_bucket_name, s3_object_name_with_prefix)


class FakeS3Client(ABC):
    def __init__(self):
        self.uploaded = {}  # type: dict[str, list[BaseDataclass]]

    def upload_dataclass_object_list_to_s3(
        self,
        dataclass_object_list: list[BaseDataclass],
        s3_bucket_name: str,
        s3_prefix: str,
        s3_object_name: str,
    ) -> None:
        self.uploaded[f"{s3_bucket_name}/{s3_prefix}/{s3_object_name}"] = dataclass_object_list
