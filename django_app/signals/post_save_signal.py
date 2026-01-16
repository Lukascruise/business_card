from django.db.models.signals import post_save
from django.dispatch import receiver

from django_app.models.card import Card
from django_app.models.card_event import CardEvent


@receiver(post_save, sender=Card)
def record_card_event(sender, instance, created, **kwargs):
    CardEvent.objects.create(
        card=instance,
        event_type=(
            CardEvent.EventType.CREATE if created else CardEvent.EventType.UPDATE
        ),
        snapshot={
            "schema_version": 1,
            "card": {
                "id": str(instance.id),
                "name": instance.name,
                "company": instance.company,
                "position": instance.position,
                "email": instance.email,
                "phone": instance.phone,
            },
        },
    )
