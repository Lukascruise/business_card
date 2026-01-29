from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.domain.errors import ValidationMessages

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(ValidationMessages.EMAIL_ALREADY_USED)
        return value


class SignupResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    user_id = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="id", read_only=True)
    name = serializers.CharField(source="nickname", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["user_id", "email", "name", "bio", "updated_at"]
        read_only_fields = ["user_id", "email", "updated_at"]
