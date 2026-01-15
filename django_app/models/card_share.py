import uuid
from django.db import models
from django.utils import timezone
from django_app.models.card import Card


class CardShareToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name="share_tokens"
    )

    access_key = models.CharField(max_length=100, unique=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        db_table = "card_share_tokens"
