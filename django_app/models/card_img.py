from django.db import models
import uuid
from django_app.models.card import Card


class CardImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="images")

    image_path = models.CharField(max_length=500)
    raw_ocr_result = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card_images"
