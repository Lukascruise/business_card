#!/bin/sh
set -e
uv run python manage.py migrate --noinput
# PATH 의존 없이 venv 내 gunicorn 직접 실행 (Render 빌드 캐시 시 gunicorn 미찾음 방지)
exec /app/.venv/bin/gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
