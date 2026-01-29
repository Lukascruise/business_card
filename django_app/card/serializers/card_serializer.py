import re

from rest_framework import serializers

from core.constants import PHONE_REGEX
from core.domain.errors import ValidationMessages
from django_app.card.models.card import Card


class CardSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(
        required=False, allow_null=True, write_only=True, allow_blank=True
    )

    class Meta:
        model = Card
        fields = [
            "id",
            "owner_id",
            "name",
            "company",
            "position",
            "email",
            "phone",
            "bio",
            "image_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner_id", "created_at", "updated_at"]

    owner_id = serializers.UUIDField(source="owner.id", read_only=True)

    def validate_phone(self, value):
        if value and not re.match(PHONE_REGEX, value):
            raise serializers.ValidationError(ValidationMessages.PHONE_INVALID)
        return value
