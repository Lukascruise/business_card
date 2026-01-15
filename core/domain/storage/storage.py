import uuid
from typing import Any, Protocol


class StoragePresignerPort(Protocol):
    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str: ...


class StoragePathGenerator:
    @staticmethod
    def generate_card_image_path(user_id: Any, original_filename: str) -> str:
        ext = original_filename.split(".")[-1] if "." in original_filename else "bin"
        return f"cards/{user_id}/{uuid.uuid4()}.{ext}"

    @staticmethod
    def generate_share_token_path(token_id: str) -> str:
        return f"shares/{token_id}"
