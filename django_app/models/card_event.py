import uuid

from django.db import models

from django_app.models.card import Card


class CardEvent(models.Model):
    objects: models.Manager["CardEvent"]

    class EventType(models.TextChoices):
        CREATE = "CREATE", "Created"
        UPDATE = "UPDATE", "Updated"
        DELETE = "DELETE", "Deleted"
        IMAGE_ADDED = "IMAGE_ADDED", "Image Added"
        SHARED = "SHARED", "Shared"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="events",
    )

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
    )

    # 이벤트에 대한 최소 메타 정보(스냅샷제거 event와 분리)
    meta = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card_events"
        indexes = [
            models.Index(fields=["card", "created_at"]),
        ]
