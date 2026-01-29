import uuid

from django.conf import settings
from django.db import models

from django_app.card.models.card import Card


class UserCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collections",
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="collected_by",
    )
    collected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_collections"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "card"], name="uq_user_card_collect"
            )
        ]
        indexes = [
            models.Index(fields=["user", "collected_at"]),
        ]
