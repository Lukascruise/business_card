from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_app.models.card import Card
from django_app.permissions.card_permission import IsCardOwner
from django_app.serializers.card_serializer import CardSerializer
from django_app.services.service import CardCreateService


class CardViewSet(viewsets.ModelViewSet):
    """명함 CRUD 및 이미지 기반 생성 ViewSet"""

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsCardOwner]

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """이미지 업로드와 명함 생성을 원자적으로 처리"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_file = request.FILES.get("image")
        if not image_file:
            return Response(
                {"error": "이미지 파일이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Service 호출 시 Signal에 의해 Event와 Snapshot이 자동 생성
        card = CardCreateService.execute(
            user=request.user,
            image_file=image_file,
            card_data=serializer.validated_data,
        )

        return Response(self.get_serializer(card).data, status=status.HTTP_201_CREATED)
