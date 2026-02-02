from __future__ import annotations

import json
import os
import re
from pathlib import Path
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
    # #region agent log
    if response and response.status_code == 400:
        _log_path = Path(settings.BASE_DIR) / ".cursor" / "debug.log"
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "D",
                "location": "core/services/drf_exception_handler.py",
                "message": "400 from exception handler",
                "data": {
                    "exc_type": type(exc).__name__,
                    "path": getattr(
                        context.get("request") if context else None, "path", None
                    ),
                },
                "timestamp": __import__("time", fromlist=["time"]).time() * 1000,
            }
            _log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(_log_path, "a", encoding="utf-8") as _f:
                _f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            print(f"[debug] {json.dumps(payload, ensure_ascii=False)}", flush=True)
        except Exception:
            pass
    # #endregion
    _add_cors_headers_to_response(response, context)
    return response
