import uuid

from django.conf import settings
from django.db import models

from django_app.models.card import Card


class CardImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="images")

    image_path = models.CharField(max_length=500)
    raw_ocr_result = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card_images"

    @property
    def image_url(self) -> str:
        return f"{settings.CDN_BASE_URL}/{self.image_path}"
