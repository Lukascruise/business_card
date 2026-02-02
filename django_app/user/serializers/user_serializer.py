from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.domain.errors import ValidationMessages

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            "required": ValidationMessages.EMAIL_REQUIRED,
            "invalid": ValidationMessages.EMAIL_INVALID_FORMAT,
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "required": ValidationMessages.PASSWORD_REQUIRED,
            "min_length": ValidationMessages.PASSWORD_MIN_LENGTH,
        },
    )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(ValidationMessages.EMAIL_ALREADY_USED)
        return value


class SignupResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    user_id = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            "required": ValidationMessages.EMAIL_REQUIRED,
            "invalid": ValidationMessages.EMAIL_INVALID_FORMAT,
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            "required": ValidationMessages.PASSWORD_REQUIRED,
        },
    )


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="id", read_only=True)
    name = serializers.CharField(source="nickname", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["user_id", "email", "name", "bio", "updated_at"]
        read_only_fields = ["user_id", "email", "updated_at"]
