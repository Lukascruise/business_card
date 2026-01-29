from __future__ import annotations

from typing import TypedDict

from django.conf import settings

from core.domain.storage.paths import CardPathGenerator
from django_app.card.infra.r2_adapter import R2StorageAdapter


class PresignedUploadResult(TypedDict):
    upload_url: str
    image_url: str
    key: str


class MediaService:
    @staticmethod
    def create_presigned_upload(
        *, filename: str, file_type: str | None
    ) -> PresignedUploadResult:
        key = CardPathGenerator.generate_image_key(filename)
        r2 = R2StorageAdapter()
        upload_url = r2.generate_presigned_put_url(key, content_type=file_type)

        cdn = settings.CDN_BASE_URL.rstrip("/")
        image_url = f"{cdn}/{key.lstrip('/')}"

        return {"upload_url": upload_url, "image_url": image_url, "key": key}
