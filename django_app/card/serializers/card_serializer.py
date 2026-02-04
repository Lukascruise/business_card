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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        first_img = instance.images.first()
        data["image_url"] = first_img.image_url if first_img else None
        return data

    def validate_phone(self, value):
        if not value:
            return ""
        digits = re.sub(r"\D", "", value)
        if not digits:
            return ""
        if not re.match(PHONE_REGEX, digits):
            raise serializers.ValidationError(ValidationMessages.PHONE_INVALID)
        return digits
