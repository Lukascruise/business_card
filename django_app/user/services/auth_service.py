from __future__ import annotations

from typing import cast

from rest_framework.authtoken.models import Token

from django_app.user.models import User
from django_app.user.models.user import UserManager


class AuthService:
    @staticmethod
    def signup(*, email: str, password: str) -> tuple[User, Token]:
        manager = cast(UserManager, User.objects)
        user = manager.create_user(email=email, password=password)
        token = Token.objects.create(user=user)
        return user, token
