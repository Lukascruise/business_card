from rest_framework import serializers

from django_app.models.card_share import CardShareToken


class CardShareTokenSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = CardShareToken
        fields = [
            "id",
            "card",
            "access_key",
            "expires_at",
            "is_active",
            "is_expired",
        ]
        read_only_fields = ["id", "access_key"]

    card = serializers.PrimaryKeyRelatedField(read_only=True)
