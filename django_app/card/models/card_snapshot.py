import uuid

from django.db import models

from django_app.card.models.card import Card


class CardSnapshot(models.Model):
    objects: models.Manager["CardSnapshot"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="snapshots",
    )

    schema_version = models.PositiveSmallIntegerField(default=1)

    data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card_snapshots"
        ordering = ["-created_at"]
