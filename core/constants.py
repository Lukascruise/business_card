"""
API·에러·스토리지 관련 상수.
응답 키, 에러 페이로드 키, 저장소 경로 등 하드코딩 제거용.
"""

# --- API 응답 키 (프론트엔드 계약과 공유) ---


class ApiKeys:
    ACCESS_TOKEN = "access_token"
    USER_ID = "user_id"
    TOKEN_ID = "token_id"
    SHARE_TOKEN = "share_token"
    EXPIRES_AT = "expires_at"
    STATUS = "status"
    CARD_ID = "card_id"
    COLLECTION_ID = "collection_id"
    UPLOAD_URL = "upload_url"
    IMAGE_URL = "image_url"


# --- 에러 응답 페이로드 키 (custom_exception_handler) ---


class ErrorResponseKeys:
    SUCCESS = "success"
    ERROR = "error"
    CODE = "code"
    MESSAGE = "message"
    DETAIL = "detail"


# --- API status 값 ---


class ApiStatus:
    DEACTIVATED = "deactivated"


# --- 스토리지 경로 ---


class StoragePaths:
    CARDS_BASE = "cards"
    SHARES_PREFIX = "shares"
    ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


# --- Presigned URL 만료 (초) ---

PRESIGNED_URL_EXPIRES_IN = 3600


# --- CardEvent meta 등 내부 키 ---


class CardEventMeta:
    ORIGIN = "origin"
    ORIGIN_WEB_API = "web_api"
    SNAPSHOT_ID = "snapshot_id"
    HAS_IMAGE = "has_image"


CARD_SNAPSHOT_SCHEMA_VERSION = 1

# --- 검증 (전화번호 등) ---
# 전화번호: 숫자만 저장·검증 (010 + 2~9 + 6~7자리). 프론트에서 하이픈 포맷 표시.
PHONE_REGEX = r"^010[2-9]\d{6,7}$"
