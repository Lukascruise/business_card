from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


def trigger_error(request):
    """Sentry 연동 확인용: 500 발생 → Sentry에 전송 (테스트 후 제거)."""
    _ = 1 / 0  # ZeroDivisionError → Sentry 전송


urlpatterns = [
    path("sentry-debug/", trigger_error),  # type: ignore[arg-type]
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("api/v1/cards/", include("django_app.card.urls.url")),
    path("v1/", include("config.v1_urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
