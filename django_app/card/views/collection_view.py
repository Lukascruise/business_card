from typing import cast

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import ApiKeys
from django_app.card.models.card import Card
from django_app.card.serializers.collection_serializer import (
    CollectionCreateResponseSerializer,
    CollectionCreateSerializer,
    CollectionItemSerializer,
)
from django_app.card.services.collection_service import CollectionService


@extend_schema_view(
    get=extend_schema(
        responses={200: CollectionItemSerializer(many=True)},
        tags=["collections"],
        summary="보관함 목록",
    ),
    post=extend_schema(
        request=CollectionCreateSerializer,
        responses={201: CollectionCreateResponseSerializer},
        tags=["collections"],
        summary="명함 수집(보관함에 추가)",
    ),
)
class CollectionCreateView(APIView):
    """보관함: GET 목록, POST 수집 (/v1/collections)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = CollectionService.list_collections(user=request.user)
        serializer = CollectionItemSerializer(qs, many=True)
        return Response(serializer.data)

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


class CollectionDeleteView(APIView):
    """보관함에서 삭제 DELETE /v1/collections/<collection_id>."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["collections"],
        summary="보관함에서 삭제",
        responses={204: None},
    )
    def delete(self, request, collection_id):
        CollectionService.delete_collection(
            user=request.user, collection_id=str(collection_id)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
