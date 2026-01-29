from typing import cast

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import ApiKeys
from django_app.card.models.card import Card
from django_app.card.serializers.collection_serializer import (
    CollectionCreateResponseSerializer,
    CollectionCreateSerializer,
)
from django_app.card.services.collection_service import CollectionService


@extend_schema(
    request=CollectionCreateSerializer,
    responses={201: CollectionCreateResponseSerializer},
    tags=["collections"],
)
class CollectionCreateView(APIView):
    """상대 명함 저장 (/v1/collections). View: 인증+Permission, Service 호출, 예외→HTTP 매핑."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CollectionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = cast(dict[str, object], serializer.validated_data)
        card = get_object_or_404(Card, id=data["card_id"])
        collection = CollectionService.collect(user=request.user, card=card)

        return Response(
            {ApiKeys.COLLECTION_ID: str(collection.id)},
            status=status.HTTP_201_CREATED,
        )
