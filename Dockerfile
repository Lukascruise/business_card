
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
# 캐시된 .venv에 gunicorn 등 새 의존성 반영 (Render 빌드 캐시 대비)
RUN /bin/uv sync --frozen --no-cache
# 빌드 캐시로 .venv에 gunicorn이 빠지는 경우 방지 (uv venv에는 pip 없음 → uv 사용)
RUN /bin/uv pip install gunicorn
# gunicorn 미찾음(exit 127) 방지: 설치 위치 확인 후 entrypoint에서 절대경로로 실행
RUN test -x /app/.venv/bin/gunicorn || (echo "gunicorn not found in venv" && exit 1)

ENV PATH="/bin:/app/.venv/bin:$PATH"

# ENTRYPOINT 고정 → Render Docker Command를 비우면 이 스크립트만 실행. gunicorn은 uv pip install로 반드시 설치됨.
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD []
