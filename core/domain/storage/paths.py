import uuid
from typing import Any


class CardPathGenerator:
    """명함 관련 리소스 경로 생성기"""

    BASE_DIR = "cards"

    @staticmethod
    def generate_image_key(user_id: Any, card_id: Any, original_name: str) -> str:
        """명함 이미지 업로드 경로: cards/{user_id}/{card_id}/{uuid}.ext"""
        ext = original_name.split(".")[-1] if "." in original_name else "bin"
        unique_id = uuid.uuid4()
        return f"{CardPathGenerator.BASE_DIR}/{user_id}/{card_id}/{unique_id}.{ext}"

    @staticmethod
    def generate_snapshot_path(card_id: Any, snapshot_id: Any) -> str:
        """스냅샷 백업 경로 (필요 시)"""
        return f"snapshots/{card_id}/{snapshot_id}.json"
