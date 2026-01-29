from rest_framework import serializers

from django_app.card.models.card_snapshot import CardSnapshot


class CardSnapshotSerializer(serializers.ModelSerializer):
    card_id = serializers.UUIDField(source="card.id", read_only=True)

    class Meta:
        model = CardSnapshot
        fields = ["id", "card_id", "schema_version", "data", "created_at"]
        read_only_fields = ["id", "card_id", "schema_version", "data", "created_at"]
