from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.role == "admin":
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.role == "moderator":
            return True
        return False


class IsUser(permissions.BasePermission):
    """If list or post new"""
    def has_permission(self, request, view):
        if request.user.role == "user":
            return True
        return False
