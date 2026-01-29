import datetime
from typing import cast

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import ApiKeys, ApiStatus
from django_app.card.models.card import Card
from django_app.card.models.card_share import CardShareToken
from django_app.card.models.card_snapshot import CardSnapshot
from django_app.card.permissions.card_permission import IsCardOwner
from django_app.card.permissions.share_permission import IsShareTokenCardOwner
from django_app.card.serializers.card_snapshot_serializer import CardSnapshotSerializer
from django_app.card.serializers.share_serializer import (
    LegacyShareTokenCreateRequestSerializer,
    LegacyShareTokenCreateResponseSerializer,
    ShareTokenCreateRequestSerializer,
    ShareTokenCreateResponseSerializer,
    ShareTokenDeactivateResponseSerializer,
)
from django_app.card.services.share_service import ShareService


@extend_schema(
    request=LegacyShareTokenCreateRequestSerializer,
    responses={201: LegacyShareTokenCreateResponseSerializer},
    tags=["share"],
)
class ShareTokenCreateView(APIView):
    """(레거시) 보안 공유 토큰 생성: body에 card_id/expires_at"""

    permission_classes = [IsAuthenticated, IsCardOwner]

    def post(self, request):
        serializer = LegacyShareTokenCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = cast(dict[str, object], serializer.validated_data)
        card = get_object_or_404(Card, id=data["card_id"])
        self.check_object_permissions(request, card)

        token = ShareService.create_token(
            card=card, expires_at=cast(datetime.datetime, data["expires_at"])
        )

        return Response(
            {
                ApiKeys.TOKEN_ID: str(token.id),
                ApiKeys.SHARE_TOKEN: token.access_key,
                ApiKeys.EXPIRES_AT: token.expires_at,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["share"], responses={200: CardSnapshotSerializer})
class SharedCardView(RetrieveAPIView):
    """공유 토큰을 통한 무인증 명함 조회 (비인증)"""

    serializer_class = CardSnapshotSerializer
    authentication_classes: list[type[BaseAuthentication]] = []
    permission_classes = [AllowAny]

    def get_object(self) -> CardSnapshot:  # pyright: ignore[reportIncompatibleMethodOverride]
        access_key = self.kwargs["access_key"]
        return ShareService.get_snapshot_by_access_key(access_key=access_key)


@extend_schema(
    request=ShareTokenCreateRequestSerializer,
    responses={201: ShareTokenCreateResponseSerializer},
    tags=["share"],
)
class CardTokenCreateView(APIView):
    """시간 제한 공유 토큰 생성 (/v1/cards/{id}/tokens)"""

    permission_classes = [IsAuthenticated, IsCardOwner]

    def post(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)
        self.check_object_permissions(request, card)

        serializer = ShareTokenCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = cast(dict[str, object], serializer.validated_data)
        token = ShareService.create_token(
            card=card, expires_at=cast(datetime.datetime, data["expires_at"])
        )

        return Response(
            {
                ApiKeys.SHARE_TOKEN: token.access_key,
                ApiKeys.EXPIRES_AT: token.expires_at,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    responses={200: ShareTokenDeactivateResponseSerializer},
    tags=["share"],
)
class ShareTokenDeactivateView(APIView):
    """토큰 즉시 무효화 (/v1/tokens/{id}/deactivate)"""

    permission_classes = [IsAuthenticated, IsShareTokenCardOwner]

    def patch(self, request, token_id):
        token = get_object_or_404(
            CardShareToken.objects.select_related("card"),
            id=token_id,
        )
        self.check_object_permissions(request, token)

        ShareService.deactivate_token(token=token)

        return Response(
            {ApiKeys.STATUS: ApiStatus.DEACTIVATED},
            status=status.HTTP_200_OK,
        )
