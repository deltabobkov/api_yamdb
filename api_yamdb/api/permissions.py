from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.role == 'moderator':
            return True
        return False


class IsUser(permissions.BasePermission):
    '''If list or post new'''

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.role == 'user':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'PATCH' or request.method == 'DELETE':
            if request.user == obj.author:
                return True
            return False
        return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class NonAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'moderator':
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False
