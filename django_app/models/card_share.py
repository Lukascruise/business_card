import secrets
import uuid

from django.db import models
from django.utils import timezone

from django_app.models.card import Card
from django_app.models.card_snapshot import CardSnapshot


def generate_access_key() -> str:
    return secrets.token_urlsafe(32)


class CardShareToken(models.Model):
    objects: models.Manager["CardShareToken"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="share_tokens",
    )

    snapshot = models.ForeignKey(
        CardSnapshot,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="share_tokens",
    )

    access_key = models.CharField(
        max_length=100,
        unique=True,
        default=generate_access_key,
    )

    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    class Meta:
        db_table = "card_share_tokens"
        indexes = [
            models.Index(
                fields=["access_key"],
                condition=models.Q(is_active=True),
                name="idx_active_share_token",
            ),
        ]
