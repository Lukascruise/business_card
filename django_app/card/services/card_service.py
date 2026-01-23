import re

from django.db import transaction

from core.domain.errors import EMS, BusinessException
from django_app.card.models.card import Card
from django_app.card.models.card_event import CardEvent
from django_app.card.models.card_img import CardImage
from django_app.card.models.card_snapshot import CardSnapshot


class CardService:
    @staticmethod
    def validate_phone_format(phone: str | None):
        if phone:
            phone_regex = r"^010-[2-9]\d{3}-\d{4}$"
            if not re.match(phone_regex, phone):
                raise BusinessException(*EMS.INVALID_PHONE_FORMAT)

    @staticmethod
    @transaction.atomic
    def create_card(owner, card_data: dict, image_key: str | None = None) -> Card:
        CardService.validate_phone_format(card_data.get("phone"))

        card = Card.objects.create(owner=owner, **card_data)

        if image_key:
            CardImage.objects.create(card=card, image_path=image_key, raw_ocr_result={})

        snapshot_data = {
            "name": card.name,
            "company": card.company,
            "position": card.position,
            "email": card.email,
            "phone": card.phone,
        }
        snapshot = CardSnapshot.objects.create(
            card=card, data=snapshot_data, schema_version=1
        )

        CardEvent.objects.create(
            card=card,
            event_type=CardEvent.EventType.CREATE,
            meta={
                "snapshot_id": str(snapshot.id),
                "origin": "web_api",
                "has_image": bool(image_key),
            },
        )

        return card

    @staticmethod
    @transaction.atomic
    def update_card(card: Card, update_data: dict) -> Card:
        if "phone" in update_data:
            CardService.validate_phone_format(update_data["phone"])

        for key, value in update_data.items():
            setattr(card, key, value)
        card.save()

        snapshot_data = {
            "name": card.name,
            "company": card.company,
            "position": card.position,
            "email": card.email,
            "phone": card.phone,
        }
        snapshot = CardSnapshot.objects.create(
            card=card, data=snapshot_data, schema_version=1
        )

        CardEvent.objects.create(
            card=card,
            event_type=CardEvent.EventType.UPDATE,
            meta={"snapshot_id": str(snapshot.id)},
        )

        return card
