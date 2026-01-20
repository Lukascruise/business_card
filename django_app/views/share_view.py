from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from core.domain.errors import EMS, BusinessException
from django_app.models.card_share import CardShareToken
from django_app.permissions.share_permission import IsActiveToken
from django_app.serializers.card_share_serializer import CardShareTokenSerializer
from django_app.serializers.card_snapshot_serializer import CardSnapshotSerializer


class ShareTokenCreateView(CreateAPIView):
    """보안 공유를 위한 시간 제한 토큰 생성"""

    queryset = CardShareToken.objects.all()
    serializer_class = CardShareTokenSerializer
    permission_classes = [IsAuthenticated]


class SharedCardView(RetrieveAPIView):
    """공유 토큰을 통한 무인증 명함 조회"""

    queryset = CardShareToken.objects.filter(is_active=True)
    serializer_class = CardSnapshotSerializer
    lookup_field = "access_key"
    permission_classes = [IsActiveToken]

    def get_object(self):
        obj = super().get_object()
        if obj.is_expired:  # 만료 여부 체크
            raise BusinessException(*EMS.AUTH_INVALID_TOKEN)
        return obj.snapshot  # 스냅샷 데이터 반환
