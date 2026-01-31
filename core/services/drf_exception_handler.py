from __future__ import annotations

import os
import re
from typing import Any

from django.conf import settings
from django.db import IntegrityError, ProgrammingError
from rest_framework.response import Response
from rest_framework.status import HTTP_409_CONFLICT, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.views import exception_handler as drf_exception_handler

from core.domain.errors import BusinessException, ErrorCode, ErrorMessages


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
        response = Response(
            {
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "detail": exc.detail,
                },
            },
            status=exc.status_code,
        )
        _add_cors_headers_to_response(response, context)
        return response

    if isinstance(exc, IntegrityError):
        # PostgreSQL unique violation (23505); signup에서 이메일 중복 시 409 반환
        cause = getattr(exc, "__cause__", None)
        pgcode = getattr(cause, "pgcode", None) if cause else None
        if pgcode == "23505":
            code, msg, status = ErrorMessages.AUTH_EMAIL_ALREADY_USED
            response = Response(
                {
                    "success": False,
                    "error": {"code": code, "message": msg, "detail": None},
                },
                status=status,
            )
        else:
            response = Response(
                {
                    "success": False,
                    "error": {
                        "code": ErrorCode.INTERNAL_SERVER_ERROR,
                        "message": "데이터 충돌이 발생했습니다.",
                        "detail": None,
                    },
                },
                status=HTTP_409_CONFLICT,
            )
        _add_cors_headers_to_response(response, context)
        return response

    if isinstance(exc, ProgrammingError):
        if os.getenv("SENTRY_DSN"):
            import sentry_sdk

            sentry_sdk.capture_exception(exc)
        response = Response(
            {
                "success": False,
                "error": {
                    "code": ErrorCode.INTERNAL_SERVER_ERROR,
                    "message": "DB 스키마가 준비되지 않았습니다. 마이그레이션을 실행해 주세요.",
                    "detail": None,
                },
            },
            status=HTTP_503_SERVICE_UNAVAILABLE,
        )
        _add_cors_headers_to_response(response, context)
        return response

    response = drf_exception_handler(exc, context)
    if response is None:
        if os.getenv("SENTRY_DSN"):
            import sentry_sdk

            sentry_sdk.capture_exception(exc)
        response = Response(
            {
                "success": False,
                "error": {
                    "code": ErrorCode.INTERNAL_SERVER_ERROR,
                    "message": "서버 오류가 발생했습니다.",
                    "detail": None,
                },
            },
            status=500,
        )
    elif response.status_code >= 500 and os.getenv("SENTRY_DSN"):
        import sentry_sdk

        sentry_sdk.capture_exception(exc)
    _add_cors_headers_to_response(response, context)
    return response
