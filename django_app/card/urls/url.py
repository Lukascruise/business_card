from django.urls import include, path
from rest_framework.routers import DefaultRouter

from django_app.card.views.card_view import CardViewSet
from django_app.card.views.media_view import PresignedUrlView
from django_app.card.views.share_view import SharedCardView, ShareTokenCreateView

router = DefaultRouter()
router.register("", CardViewSet, basename="card")

urlpatterns = [
    # Cloudflare R2 직접 업로드용 주소 발급
    path("presigned-url/", PresignedUrlView.as_view(), name="presigned-url"),
    # 보안 공유를 위한 토큰 생성
    path("share/", ShareTokenCreateView.as_view(), name="share-token-create"),
    # 공유 토큰을 통한 무인증 명함 조회 (lookup_field: access_key)
    path("shared/<str:access_key>/", SharedCardView.as_view(), name="shared-card-view"),
    # 명함 CRUD (Router가 생성하는 URL 포함)
    path("", include(router.urls)),
]
