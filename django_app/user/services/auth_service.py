from __future__ import annotations

from typing import cast

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from core.domain.errors import BusinessException, ErrorMessages
from django_app.user.models import User
from django_app.user.models.user import UserManager


class AuthService:
    @staticmethod
    def signup(*, email: str, password: str) -> tuple[User, Token]:
        manager = cast(UserManager, User.objects)
        user = manager.create_user(email=email, password=password)
        token = Token.objects.create(user=user)
        return user, token

    @staticmethod
    def login(*, email: str, password: str) -> tuple[User, Token]:
        user = authenticate(username=email, password=password)
        if user is None:
            raise BusinessException(*ErrorMessages.AUTH_INVALID_CREDENTIALS)
        token, _ = Token.objects.get_or_create(user=user)
        return cast(User, user), token
