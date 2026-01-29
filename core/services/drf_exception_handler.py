from __future__ import annotations

from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from core.domain.errors import BusinessException


def custom_exception_handler(exc: Exception, context: dict[str, Any] | None):
    if isinstance(exc, BusinessException):
        return Response(
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

    return drf_exception_handler(exc, context)
