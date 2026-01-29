from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import transaction

from core.domain.errors import EMS, BusinessException
from django_app.card.models.card import Card
from django_app.card.models.user_collection import UserCollection

if TYPE_CHECKING:
    from django_app.user.models import User

_User = get_user_model()


class CollectionService:
    """수집 도메인: '이 행위가 의미 있는지' 검증(400)은 서비스 책임."""

    @staticmethod
    @transaction.atomic
    def collect(*, user: User, card: Card) -> UserCollection:
        if card.owner == user:
            raise BusinessException(*EMS.COLLECTION_CANNOT_COLLECT_OWN)

        if UserCollection.objects.filter(user=user, card=card).exists():
            raise BusinessException(*EMS.COLLECTION_ALREADY_COLLECTED)

        collection = UserCollection.objects.create(user=user, card=card)
        return collection
