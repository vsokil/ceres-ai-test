import boto3
from typing import List
from botocore.config import Config

from botocore import UNSIGNED


class S3Client:
    def __init__(
            self,
            bucket_name: str,
            region_name: str,
    ):

        self.bucket = bucket_name

        self.s3 = boto3.client(
            "s3",
            region_name=region_name,
            config=Config(signature_version=UNSIGNED),
        )

    def list_tiff_images(self, prefix: str = "") -> List[str]:
        tiff_files = []
        continuation = None

        while True:
            params = {
                "Bucket": self.bucket,
                "Prefix": prefix,
                "MaxKeys": 1000,
            }

            if continuation:
                params["ContinuationToken"] = continuation

            response = self.s3.list_objects_v2(**params)

            if "Contents" not in response:
                break

            for obj in response["Contents"]:
                key = obj["Key"].lower()
                if key.endswith(".tiff") or key.endswith(".tif"):
                    tiff_files.append(obj["Key"])

            if response.get("IsTruncated"):
                continuation = response["NextContinuationToken"]
            else:
                break

        return tiff_files

    def download_file(self, key: str, local_path: str) -> None:
        try:
            self.s3.download_file(self.bucket, key, local_path)
        except Exception as e:
            print(f"Failed to download '{key}': {e}")
            raise

    def upload_file(self, local_path: str, key: str) -> None:
        try:
            self.s3.upload_file(local_path, self.bucket, key)
        except Exception as e:
            print(f"Failed to upload '{local_path}': {e}")
            raise
