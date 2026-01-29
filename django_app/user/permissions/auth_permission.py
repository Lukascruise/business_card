from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """
    이미 인증된 사용자는 차단하고, 익명 사용자만 허용.
    - 예: 회원가입/로그인 엔드포인트
    """

    def has_permission(self, request, view) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]
        return not bool(request.user and request.user.is_authenticated)
