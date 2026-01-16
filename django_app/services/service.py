from django.db import transaction

from django_app.infra.r2_adapter import R2StorageAdapter
from django_app.models.card import Card
from django_app.models.card_img import CardImage


class CardCreateService:
    @staticmethod
    def execute(user, image_file, card_data):
        r2 = R2StorageAdapter()

        with transaction.atomic():
            card = Card.objects.create(
                owner=user,
                name=card_data.get("name"),
                company=card_data.get("company"),
                position=card_data.get("position"),
                email=card_data.get("email"),
                phone=card_data.get("phone"),
            )

            r2_key = f"cards/{user.id}/{card.id}/{image_file.name}"
            r2.upload_file(image_file, r2_key)

            CardImage.objects.create(
                card=card,
                image_path=r2_key,
                raw_ocr_result={},
            )

            return card
