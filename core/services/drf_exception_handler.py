from __future__ import annotations

import os
import re
from typing import Any

from django.conf import settings
from django.db import IntegrityError, ProgrammingError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from core.domain.errors import BusinessException, ErrorMessages


def _error_response(
    code: Any, message: str, status: int, detail: Any = None
) -> Response:
    """공통 에러 응답 형식 (프론트 계약: success, error.code, error.message, error.detail)."""
    return Response(
        {
            "success": False,
            "error": {"code": code, "message": message, "detail": detail},
        },
        status=status,
    )


def _first_validation_message(data: dict) -> str:
    """DRF 검증 에러 body에서 첫 번째 메시지 추출."""
    if not data:
        return ErrorMessages.VALIDATION_ERROR[1]
    for key, value in data.items():
        if isinstance(value, list) and value:
            return str(value[0]) if isinstance(value[0], str) else str(value[0])
        if isinstance(value, str):
            return value
    return ErrorMessages.VALIDATION_ERROR[1]


def _add_cors_headers_to_response(
    response: Response, context: dict[str, Any] | None
) -> None:
    """에러 응답에도 CORS 헤더가 붙도록 보장 (브라우저가 응답 본문을 읽을 수 있게)."""
    if not context:
        return
    request = context.get("request")
    if not request:
        return
    origin = request.META.get("HTTP_ORIGIN")
    if not origin:
        return
    allowed = getattr(settings, "CORS_ALLOWED_ORIGINS", []) or []
    if origin in allowed:
        response["Access-Control-Allow-Origin"] = origin
        return
    for pattern in getattr(settings, "CORS_ALLOWED_ORIGIN_REGEXES", []) or []:
        if re.match(pattern, origin):
            response["Access-Control-Allow-Origin"] = origin
            return


def custom_exception_handler(exc: Exception, context: dict[str, Any] | None):
    if isinstance(exc, BusinessException):
        response = _error_response(
            exc.error_code, exc.message, exc.status_code, exc.detail
        )
        _add_cors_headers_to_response(response, context)
        return response

    if isinstance(exc, IntegrityError):
        # PostgreSQL unique violation (23505); signup에서 이메일 중복 시 409 반환
        cause = getattr(exc, "__cause__", None)
        pgcode = getattr(cause, "pgcode", None) if cause else None
        if pgcode == "23505":
            code, msg, status = ErrorMessages.AUTH_EMAIL_ALREADY_USED
        else:
            code, msg, status = ErrorMessages.DATA_CONFLICT
        response = _error_response(code, msg, status, None)
        _add_cors_headers_to_response(response, context)
        return response

    if isinstance(exc, ProgrammingError):
        if os.getenv("SENTRY_DSN"):
            import sentry_sdk

            sentry_sdk.capture_exception(exc)
        code, msg, status = ErrorMessages.DB_SCHEMA_NOT_READY
        response = _error_response(code, msg, status, None)
        _add_cors_headers_to_response(response, context)
        return response

    response = drf_exception_handler(exc, context)
    if response is None:
        if os.getenv("SENTRY_DSN"):
            import sentry_sdk

            sentry_sdk.capture_exception(exc)
        code, msg, status = ErrorMessages.INTERNAL_SERVER_ERROR
        response = _error_response(code, msg, status, None)
    else:
        if response.status_code >= 500 and os.getenv("SENTRY_DSN"):
            import sentry_sdk

            sentry_sdk.capture_exception(exc)
        # DRF 400 검증 에러 등 → 동일 형식으로 정규화 (프론트가 항상 error.message 사용 가능하도록)
        if response.status_code == 400 and response.data:
            try:
                first_msg = _first_validation_message(response.data)
                code, _, _ = ErrorMessages.VALIDATION_ERROR
                response = _error_response(code, first_msg, 400, response.data)
            except Exception:
                code, msg, status = ErrorMessages.VALIDATION_ERROR
                response = _error_response(code, msg, status, response.data)
    _add_cors_headers_to_response(response, context)
    return response
