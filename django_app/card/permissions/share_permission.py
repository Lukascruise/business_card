from rest_framework import permissions


class IsActiveToken(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]
        return obj.is_active and not obj.is_expired


class IsShareTokenCardOwner(permissions.BasePermission):
    """
    ShareToken 관련 작업 권한:
    - 토큰이 가리키는 card의 owner만 허용
    """

    def has_object_permission(self, request, view, obj) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(obj, "card", None) is not None
            and obj.card.owner == request.user
        )
