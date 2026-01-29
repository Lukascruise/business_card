from typing import cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import ApiKeys
from django_app.user.models import User
from django_app.user.permissions.auth_permission import IsNotAuthenticated
from django_app.user.serializers.user_serializer import (
    SignupResponseSerializer,
    SignupSerializer,
    UserProfileSerializer,
)
from django_app.user.services.auth_service import AuthService


@extend_schema(
    request=SignupSerializer,
    responses={201: SignupResponseSerializer},
    tags=["auth"],
)
class SignupView(APIView):
    """회원가입 (이메일 + 비밀번호)"""

    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, str], serializer.validated_data)

        user, token = AuthService.signup(
            email=data["email"],
            password=data["password"],
        )

        return Response(
            {
                ApiKeys.ACCESS_TOKEN: token.key,
                ApiKeys.USER_ID: str(user.pk),
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["user"])
class UserProfileView(RetrieveUpdateAPIView):
    """기본 프로필 조회/업데이트"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self) -> User:  # pyright: ignore[reportIncompatibleMethodOverride]
        return cast(User, self.request.user)
