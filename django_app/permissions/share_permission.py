from rest_framework import permissions


class IsActiveToken(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_active and not obj.is_expired
