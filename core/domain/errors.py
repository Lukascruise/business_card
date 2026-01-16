from enum import StrEnum
from typing import Any


class ErrorCode(StrEnum):
    """Mypy 에러를 해결하기 위한 시스템 통합 에러 코드"""

    CARD_NOT_FOUND = "CARD.NOT_FOUND"
    AUTH_INVALID_TOKEN = "AUTH.INVALID_TOKEN"
    R2_UPLOAD_FAILED = "IMG.R2_UPLOAD_FAILED"
    INTERNAL_SERVER_ERROR = "COMMON.INTERNAL_ERROR"


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
    R2_UPLOAD_FAILED = (
        ErrorCode.R2_UPLOAD_FAILED,
        "이미지 업로드에 실패했습니다.",
        502,
    )


EMS = ErrorMessages
