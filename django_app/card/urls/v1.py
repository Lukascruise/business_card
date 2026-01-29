from django.urls import include, path
from rest_framework.routers import DefaultRouter

from django_app.card.views.card_view import CardViewSet
from django_app.card.views.collection_view import CollectionCreateView
from django_app.card.views.media_view import PresignedUrlView
from django_app.card.views.share_view import (
    CardTokenCreateView,
    SharedCardView,
    ShareTokenDeactivateView,
)

router = DefaultRouter()
router.register("cards", CardViewSet, basename="card")

urlpatterns = [
    path("media/presigned-url", PresignedUrlView.as_view(), name="presigned-url"),
    # 상대 명함 저장
    path("collections", CollectionCreateView.as_view(), name="collection-create"),
    # 보안 공유 토큰 발급
    path(
        "cards/<uuid:card_id>/tokens",
        CardTokenCreateView.as_view(),
        name="token-create",
    ),
    # 토큰 즉시 무효화
    path(
        "tokens/<uuid:token_id>/deactivate",
        ShareTokenDeactivateView.as_view(),
        name="token-deactivate",
    ),
    # MVP: 공유 토큰을 통한 무인증 명함 조회
    path("s/<str:access_key>", SharedCardView.as_view(), name="shared-card-view"),
    # 명함 CRUD
    path("", include(router.urls)),
]
