from rest_framework import serializers

from django_app.models.card_snapshot import CardSnapshot


class CardSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardSnapshot
        fields = ["id", "card", "access_key", "expires_at", "created_at"]
        read_only_fields = ["id", "card", "created_at"]
