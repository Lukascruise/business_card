import json
from pathlib import Path

from django.conf import settings
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_app.card.models.card import Card
from django_app.card.permissions.card_permission import IsCardOwner
from django_app.card.serializers.card_serializer import CardSerializer
from django_app.card.services.card_service import CardService


@extend_schema_view(
    list=extend_schema(tags=["cards"], summary="명함 목록"),
    create=extend_schema(tags=["cards"], summary="명함 생성"),
    retrieve=extend_schema(tags=["cards"], summary="명함 상세"),
    update=extend_schema(tags=["cards"], summary="명함 수정"),
    partial_update=extend_schema(tags=["cards"], summary="명함 부분 수정"),
    destroy=extend_schema(tags=["cards"], summary="명함 삭제"),
)
class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsCardOwner]

    def get_queryset(self) -> QuerySet[Card]:  # pyright: ignore[reportIncompatibleMethodOverride]
        return Card.objects.filter(owner=self.request.user).order_by("-updated_at")

    def retrieve(self, request, *args, **kwargs):
        # #region agent log
        _debug_log_path = Path(settings.BASE_DIR) / ".cursor" / "debug.log"
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "B",
                "location": "django_app/card/views/card_view.py:retrieve",
                "message": "card retrieve entered",
                "data": {"path": request.path, "pk": kwargs.get("pk")},
                "timestamp": __import__("time", fromlist=["time"]).time() * 1000,
            }
            _debug_log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(_debug_log_path, "a", encoding="utf-8") as _f:
                _f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            print(f"[debug] {json.dumps(payload, ensure_ascii=False)}", flush=True)
        except Exception:
            pass
        # #endregion
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card = CardService.create_card(
            owner=request.user,
            card_data=serializer.validated_data,
        )
        return Response(self.get_serializer(card).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        card = self.get_object()

        serializer = self.get_serializer(card, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        updated = CardService.update_card(
            card=card, update_data=serializer.validated_data
        )
        return Response(self.get_serializer(updated).data, status=status.HTTP_200_OK)
