"""디버그용 미들웨어: 400 원인 추적 (ALLOWED_HOSTS 등)."""

import json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import DisallowedHost

DEBUG_LOG_PATH = Path(settings.BASE_DIR) / ".cursor" / "debug.log"


def _debug_log(
    location: str, message: str, data: dict, hypothesis_id: str = "A"
) -> None:
    # #region agent log
    try:
        payload = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": __import__("time", fromlist=["time"]).time() * 1000,
        }
        DEBUG_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        print(f"[debug] {json.dumps(payload, ensure_ascii=False)}", flush=True)
    except Exception:
        pass
    # #endregion


class DebugRequestLogMiddleware:
    """요청 path / Host / ALLOWED_HOSTS 로깅 (400 DisallowedHost 등 원인 추적)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = getattr(request, "path", "") or ""
        # #region agent log
        if "/v1/cards/" in path and path.rstrip("/").split("/")[-1] not in (
            "",
            "cards",
        ):
            try:
                host = request.get_host()
                allowed = list(getattr(settings, "ALLOWED_HOSTS", []) or [])
                _debug_log(
                    "core/middleware.py:DebugRequestLogMiddleware",
                    "card request host check",
                    {
                        "path": path,
                        "host": host,
                        "allowed_hosts": allowed,
                        "host_in_allowed": host in allowed,
                    },
                    "A",
                )
            except DisallowedHost as e:
                _debug_log(
                    "core/middleware.py:DebugRequestLogMiddleware",
                    "DisallowedHost",
                    {
                        "path": path,
                        "exception": str(e),
                        "allowed_hosts": list(
                            getattr(settings, "ALLOWED_HOSTS", []) or []
                        ),
                    },
                    "A",
                )
                raise
        # #endregion
        return self.get_response(request)
