from enum import StrEnum
from typing import Any


class ErrorCode(StrEnum):
    """시스템 통합 에러 코드. API 응답 error.code 및 프론트 표시용."""

    CARD_NOT_FOUND = "CARD.NOT_FOUND"
    AUTH_INVALID_TOKEN = "AUTH.INVALID_TOKEN"
    AUTH_EMAIL_ALREADY_USED = "AUTH.EMAIL_ALREADY_USED"
    AUTH_INVALID_CREDENTIALS = "AUTH.INVALID_CREDENTIALS"
    R2_UPLOAD_FAILED = "IMG.R2_UPLOAD_FAILED"
    INTERNAL_SERVER_ERROR = "COMMON.INTERNAL_ERROR"
    INVALID_IMAGE_EXTENSION = "IMG.INVALID_EXTENSION"
    INVALID_PHONE_FORMAT = "CARD.INVALID_PHONE"
    COLLECTION_CANNOT_COLLECT_OWN = "COLLECTION.CANNOT_COLLECT_OWN"
    COLLECTION_ALREADY_COLLECTED = "COLLECTION.ALREADY_COLLECTED"
    COLLECTION_NOT_FOUND = "COLLECTION.NOT_FOUND"
    # 핸들러에서 사용 (DB/공통)
    DATA_CONFLICT = "COMMON.DATA_CONFLICT"
    DB_SCHEMA_NOT_READY = "COMMON.DB_SCHEMA_NOT_READY"
    VALIDATION_ERROR = "COMMON.VALIDATION_ERROR"


class BusinessException(Exception):
    """비즈니스 로직 중 발생하는 예외 클래스"""

    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        status_code: int = 400,
        detail: Any = None,
    ):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class ErrorMessages:
    CARD_NOT_FOUND = (ErrorCode.CARD_NOT_FOUND, "명함을 찾을 수 없습니다.", 404)
    AUTH_INVALID_TOKEN = (
        ErrorCode.AUTH_INVALID_TOKEN,
        "인증 정보가 유효하지 않습니다.",
        401,
    )
    AUTH_EMAIL_ALREADY_USED = (
        ErrorCode.AUTH_EMAIL_ALREADY_USED,
        "이미 사용 중인 이메일입니다.",
        409,
    )
    AUTH_INVALID_CREDENTIALS = (
        ErrorCode.AUTH_INVALID_CREDENTIALS,
        "이메일 또는 비밀번호가 올바르지 않습니다.",
        401,
    )
    R2_UPLOAD_FAILED = (
        ErrorCode.R2_UPLOAD_FAILED,
        "이미지 업로드에 실패했습니다.",
        502,
    )
    INVALID_IMAGE_EXTENSION = (
        ErrorCode.INVALID_IMAGE_EXTENSION,
        "허용되지 않는 이미지 확장자입니다.",
        400,
    )
    INVALID_PHONE_FORMAT = (
        ErrorCode.INVALID_PHONE_FORMAT,
        "전화번호 형식이 올바르지 않습니다.",
        400,
    )
    COLLECTION_CANNOT_COLLECT_OWN = (
        ErrorCode.COLLECTION_CANNOT_COLLECT_OWN,
        "자기 명함은 수집할 수 없습니다.",
        400,
    )
    COLLECTION_ALREADY_COLLECTED = (
        ErrorCode.COLLECTION_ALREADY_COLLECTED,
        "이미 수집한 명함입니다.",
        400,
    )
    COLLECTION_NOT_FOUND = (
        ErrorCode.COLLECTION_NOT_FOUND,
        "수집한 명함을 찾을 수 없습니다.",
        404,
    )
    # 핸들러 전용 (IntegrityError, ProgrammingError, 기타)
    INTERNAL_SERVER_ERROR = (
        ErrorCode.INTERNAL_SERVER_ERROR,
        "서버 오류가 발생했습니다.",
        500,
    )
    DATA_CONFLICT = (
        ErrorCode.DATA_CONFLICT,
        "데이터 충돌이 발생했습니다.",
        409,
    )
    DB_SCHEMA_NOT_READY = (
        ErrorCode.DB_SCHEMA_NOT_READY,
        "DB 스키마가 준비되지 않았습니다. 마이그레이션을 실행해 주세요.",
        503,
    )
    VALIDATION_ERROR = (
        ErrorCode.VALIDATION_ERROR,
        "입력값을 확인해 주세요.",
        400,
    )


EMS = ErrorMessages


class ValidationMessages:
    """시리얼라이저 등에서 쓰는 검증 메시지 (ErrorMessages와 통일)"""

    PHONE_INVALID = EMS.INVALID_PHONE_FORMAT[1]
    EMAIL_ALREADY_USED = "이미 사용 중인 이메일입니다."
    EMAIL_REQUIRED = "이메일을 입력해 주세요."
    EMAIL_INVALID_FORMAT = "이메일 형식이 올바르지 않습니다."
    PASSWORD_REQUIRED = "비밀번호를 입력해 주세요."
    PASSWORD_MIN_LENGTH = "비밀번호는 8자 이상이어야 합니다."
    EXPIRES_AT_FUTURE = "만료 시각은 미래여야 합니다."
