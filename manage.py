import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "장고안깔림"
            "도커 컨테이너 안에서 실행하세요 (docker compose exec web ...)\n"
            "로컬이라면 uv sync하고 가상환경(source .venv/bin/activate) 켜세요"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
