from rest_framework import permissions


class IsCardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and obj.owner == request.user
        )
