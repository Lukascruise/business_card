from django.utils import timezone
from rest_framework import serializers

from core.domain.errors import ValidationMessages


class ShareTokenCreateRequestSerializer(serializers.Serializer):
    expires_at = serializers.DateTimeField()

    def validate_expires_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(ValidationMessages.EXPIRES_AT_FUTURE)
        return value


class LegacyShareTokenCreateRequestSerializer(ShareTokenCreateRequestSerializer):
    card_id = serializers.UUIDField()


class ShareTokenCreateResponseSerializer(serializers.Serializer):
    share_token = serializers.CharField()
    expires_at = serializers.DateTimeField()


class LegacyShareTokenCreateResponseSerializer(serializers.Serializer):
    token_id = serializers.UUIDField()
    share_token = serializers.CharField()
    expires_at = serializers.DateTimeField()


class ShareTokenDeactivateResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
