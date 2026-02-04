from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from core.domain.errors import EMS, BusinessException
from django_app.card.models.card import Card
from django_app.card.models.user_collection import UserCollection

if TYPE_CHECKING:
    from django_app.user.models import User

_User = get_user_model()


class CollectionService:
    """수집 도메인: '이 행위가 의미 있는지' 검증(400)은 서비스 책임."""

    @staticmethod
    def list_collections(*, user: User) -> QuerySet[UserCollection]:
        """내 보관함 목록 (수집 시점 최신순)."""
        return (
            UserCollection.objects.filter(user=user)
            .select_related("card")
            .prefetch_related("card__images")
            .order_by("-collected_at")
        )

    @staticmethod
    @transaction.atomic
    def collect(*, user: User, card: Card) -> UserCollection:
        if card.owner == user:
            raise BusinessException(*EMS.COLLECTION_CANNOT_COLLECT_OWN)

        if UserCollection.objects.filter(user=user, card=card).exists():
            raise BusinessException(*EMS.COLLECTION_ALREADY_COLLECTED)

        collection = UserCollection.objects.create(user=user, card=card)
        return collection

    @staticmethod
    def delete_collection(*, user: User, collection_id: str) -> None:
        """보관함에서 삭제. 본인 수집 건만 삭제 가능."""
        collection = UserCollection.objects.filter(id=collection_id, user=user).first()
        if collection is None:
            raise BusinessException(
                *EMS.COLLECTION_NOT_FOUND
            )  # 404, 본인 건이 아니어도 동일 응답
        collection.delete()
