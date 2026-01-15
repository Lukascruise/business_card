import uuid
from django.db import models
from django_app.models.card import Card


class CardEvent(models.Model):
    EVENT_TYPES = [
        ("CREATE", "Created"),
        ("UPDATE", "Updated"),
        ("DELETE", "Deleted"),
        ("IMAGE_ADDED", "Image Added"),
        ("SHARED", "Shared"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="events",
    )

    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    snapshot = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card_events"
