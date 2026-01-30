FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

FROM python:3.13-slim
COPY --from=builder /bin/uv /bin/uvx /bin/
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/bin:/app/.venv/bin:$PATH"

# Render: PORT 주입. 로컬 Docker: 미설정 시 8000 사용.
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
