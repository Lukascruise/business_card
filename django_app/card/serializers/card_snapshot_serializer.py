from rest_framework import serializers

from django_app.card.models.card_snapshot import CardSnapshot


class CardSnapshotSerializer(serializers.ModelSerializer):
    card_id = serializers.UUIDField(source="card.id", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CardSnapshot
        fields = ["id", "card_id", "schema_version", "data", "image_url", "created_at"]
        read_only_fields = [
            "id",
            "card_id",
            "schema_version",
            "data",
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj: CardSnapshot):
        first = obj.card.images.first()
        return first.image_url if first else None
