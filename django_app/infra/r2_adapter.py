import boto3
from django.conf import settings
from core.domain.storage.storage import StoragePresignerPort


class R2StorageAdapter(StoragePresignerPort):
    def __init__(self) -> None:
        self.account_id = settings.R2_ACCOUNT_ID
        self.access_key = settings.R2_ACCESS_KEY_ID
        self.secret_key = settings.R2_SECRET_ACCESS_KEY
        self.bucket_name = settings.R2_BUCKET_NAME
        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"

        self.s3 = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="auto",
        )

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": key.lstrip("/")},
            ExpiresIn=expires_in,
        )

    def upload_file(self, file: Any, key: str) -> str:
        self.s3.upload_fileobj(file, self.bucket_name, key.lstrip("/"))
        return key

    def delete_file(self, key: str) -> None:
        if key:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key.lstrip("/"))
