import os
import uuid

from core.domain.errors import EMS, BusinessException


class CardPathGenerator:
    BASE_DIR = "cards"
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

    @classmethod
    def generate_image_key(cls, original_filename: str) -> str:
        ext = os.path.splitext(original_filename)[1].lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise BusinessException(*EMS.INVALID_IMAGE_EXTENSION)

        folder_uuid = uuid.uuid4()
        file_uuid = uuid.uuid4()
        return f"{cls.BASE_DIR}/{folder_uuid}/{file_uuid}{ext}"

    @classmethod
    def generate_share_token_path(cls, card_id: str) -> str:
        return f"shares/{card_id}/{uuid.uuid4()}"
