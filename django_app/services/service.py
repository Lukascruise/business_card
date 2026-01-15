from django.db import transaction
from django.forms.models import model_to_dict
from django_app.infra.r2_adapter import R2Client
from django_app.models.card import Card
from django_app.models.card_img import CardImage
from django_app.models.card_event import CardEvent


class CardCreateService:
    @staticmethod
    def execute(user, image_file, card_data):
        r2 = R2Client()

        with transaction.atomic():
            # 1. Card 생성
            card = Card.objects.create(
                owner=user,
                name=card_data.get("name"),
                company=card_data.get("company"),
                position=card_data.get("position"),
                email=card_data.get("email"),
                phone=card_data.get("phone"),
            )

            # 2. R2 이미지 업로드 및 CardImage 생성
            r2_key = f"cards/{user.id}/{card.id}/{image_file.name}"
            r2.upload_file(image_file, r2_key)

            card_img = CardImage.objects.create(
                card=card,
                image_path=r2_key,
                raw_ocr_result={},  # MVP 단계에서는 빈 딕셔너리로 초기화
            )

            # 3. CardEvent(CREATE) 기록
            CardEvent.objects.create(
                card=card, event_type="CREATE", snapshot=model_to_dict(card)
            )

            return card
