from rest_framework import status, viewsets
from rest_framework.response import Response

from django_app.card.models.card import Card
from django_app.card.serializers.card_serializer import CardSerializer
from django_app.card.services.card_service import CardService


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        # 번역 (HTTP -> Python Dict)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 이미지 파일, JSON 데이터 모두를 서비스에 통째로 넘김
        card = CardService.create_card(
            owner=request.user,
            data=serializer.validated_data,
            files=request.FILES,  # 파일 처리 주권을 서비스에 넘김
        )

        return Response(self.get_serializer(card).data, status=status.HTTP_201_CREATED)
