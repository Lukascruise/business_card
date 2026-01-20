import re

from rest_framework import serializers

from django_app.models.card import Card


class CardSerializer(serializers.ModelSerializer):
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    owner_id = serializers.UUIDField(source="owner.id", read_only=True)

    def validate_phone(self, value):
        if value:
            phone_regex = r"^010-[2-9]\d{2,3}-\d{4}$"
            if not re.match(phone_regex, value):
                raise serializers.ValidationError(
                    "전화번호 형식이 올바르지 않습니다. 국번은 2~9로 시작해야 합니다."
                )
        return value
