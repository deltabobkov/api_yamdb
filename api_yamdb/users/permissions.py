from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1:
            return True
        if request.user.is_staff:
            return True
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 3:
            return True
        return False


class IsUser(permissions.BasePermission):
    """If list or post new"""
    def has_permission(self, request, view):
        if request.user.role == 2:
            return True
        return False