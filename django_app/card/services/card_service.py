from __future__ import annotations

import re
from typing import TYPE_CHECKING, TypedDict, cast

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

from core.constants import CARD_SNAPSHOT_SCHEMA_VERSION, PHONE_REGEX, CardEventMeta
from core.domain.errors import EMS, BusinessException
from django_app.card.models.card import Card
from django_app.card.models.card_event import CardEvent
from django_app.card.models.card_img import CardImage
from django_app.card.models.card_snapshot import CardSnapshot

if TYPE_CHECKING:
    from django_app.user.models import User

_User = get_user_model()


class _CardDataInput(TypedDict, total=False):
    name: str
    company: str | None
    position: str | None
    email: str | None
    phone: str | None
    bio: str | None
    image_url: str | None


def _image_url_to_storage_key(image_url: str | None) -> str | None:
    """image_url → R2 스토리지 key 변환. CDN base 제거 또는 그대로 key로 사용."""
    if not image_url:
        return None
    cdn = settings.CDN_BASE_URL.rstrip("/")
    if image_url.startswith(f"{cdn}/"):
        return image_url[len(cdn) + 1 :]
    return image_url


class CardService:
    @staticmethod
    def validate_phone_format(phone: str | None) -> None:
        if not phone:
            return
        digits = re.sub(r"\D", "", phone)
        if digits and not re.match(PHONE_REGEX, digits):
            raise BusinessException(*EMS.INVALID_PHONE_FORMAT)

    @staticmethod
    @transaction.atomic
    def create_card(owner: User, card_data: _CardDataInput) -> Card:
        data = dict(card_data)
        image_url = cast(str | None, data.pop("image_url", None))
        image_key = _image_url_to_storage_key(image_url)

        CardService.validate_phone_format(cast(str | None, data.get("phone")))

        card = Card.objects.create(owner=owner, **data)

        if image_key:
            CardImage.objects.create(card=card, image_path=image_key, raw_ocr_result={})

        snapshot_data = {
            "name": card.name,
            "company": card.company,
            "position": card.position,
            "email": card.email,
            "phone": card.phone,
            "bio": card.bio,
        }
        snapshot = CardSnapshot.objects.create(
            card=card, data=snapshot_data, schema_version=CARD_SNAPSHOT_SCHEMA_VERSION
        )

        CardEvent.objects.create(
            card=card,
            event_type=CardEvent.EventType.CREATE,
            meta={
                CardEventMeta.SNAPSHOT_ID: str(snapshot.id),
                CardEventMeta.ORIGIN: CardEventMeta.ORIGIN_WEB_API,
                CardEventMeta.HAS_IMAGE: bool(image_key),
            },
        )

        return card

    @staticmethod
    @transaction.atomic
    def update_card(card: Card, update_data: _CardDataInput) -> Card:
        data = dict(update_data)
        data.pop("image_url", None)  # update 시 image_url 무시

        if "phone" in data:
            CardService.validate_phone_format(cast(str | None, data["phone"]))

        for key, value in data.items():
            setattr(card, key, value)
        card.save()

        snapshot_data = {
            "name": card.name,
            "company": card.company,
            "position": card.position,
            "email": card.email,
            "phone": card.phone,
            "bio": card.bio,
        }
        snapshot = CardSnapshot.objects.create(
            card=card, data=snapshot_data, schema_version=CARD_SNAPSHOT_SCHEMA_VERSION
        )

        CardEvent.objects.create(
            card=card,
            event_type=CardEvent.EventType.UPDATE,
            meta={CardEventMeta.SNAPSHOT_ID: str(snapshot.id)},
        )

        return card
